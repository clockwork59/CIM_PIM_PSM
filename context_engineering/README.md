# Context Engineering for CIM-PIM-PSM
# 医疗建筑知识图谱的上下文工程框架

> Context Engineering is the discipline of designing the **complete information payload**
> provided to an AI agent at inference time.
> -- davidkimai/Context-Engineering

## MBSE 架构基准: CIM-PIM-PSM

CIM-PIM-PSM 是 OMG 模型驱动架构 (MDA) 在 MBSE 中的实现逻辑，不是三个产出物，而是三个抽象层级：

| 层级 | 定义 | 本项目实现 | 关键特征 |
|------|------|-----------|---------|
| **CIM** | 领域知识 + 惯例认知，以本体和图谱表达 | 545类本体 + 6桥接 + FMEA + 标准准则 + 安全事件模型 | 不依赖任何支持系统 |
| **PIM** | 面向领域的系统方法/逻辑/组件/模块，CIM的工程化 | 仿真引擎 + 状态机 + 动作链 + Named Graph架构 + SPARQL模板 + 12步验证管线 | 与平台技术无关 |
| **PSM** | 具体落地项目的技术选型/实现/数据装载，PIM的实例化 | Fuseki + FastAPI + Docker + NBU 1,210实例 + BAS 1,055点 + HTML前端 | 面向现实的技术选择 |

### 资产归类

CIM 层（领域知识）:
- layer0-4 本体 (545 owl:Class) — 医疗建筑领域的形式化知识
- 6 桥接本体 — 行业标准间的惯例认知对齐
- GB50333/WS435/IEC60364 准则实例 — 行业规范=领域惯例
- FMEA 200+ 故障模式 — 运维领域经验知识
- BFO 生命周期过程链 — 设施演化的领域认知
- 安全事件26类 + 预案模型 — 安防领域的处置知识

PIM 层（系统工程）:
- 仿真引擎 (stage_gate_engine) — 验证方法的系统化
- 事件状态机 (5态转换) — 事件处置的系统方法
- 动作链执行器 (依赖拓扑) — 预案执行的系统逻辑
- Named Graph 9图架构 — 数据组织的系统设计
- SPARQL 查询模板 9条 — 系统功能的逻辑表达
- 12步验证管线 — 质量保证的系统方法
- 守恒方程引擎 — 物理验证的工程逻辑

PSM 层（项目实例）:
- Fuseki 4.10 + Docker — 具体技术选型
- FastAPI 6端点 — 具体技术实现
- NBU IFC→ABox 1,210实例 — 具体项目数据装载
- BAS 1,055 BACnet点位 — 具体仿真数据
- CMMS 735工单 — 具体工单数据
- HTML 可视化平台 — 具体前端实现

## Core Premise

Context Engineering is NOT documentation management. The `Context Engineering/` directory
in this repo is a document library. This `context_engineering/` directory defines **how
those documents -- and the knowledge graph -- are delivered to 9 CIM Agents at runtime**.

The distinction matters:
- Documentation tells humans what to do.
- Context Engineering tells AI agents what to know, when to know it, and how much of it to load.

## Framework: C = A(c1, c2, ..., cn)

Where:
- **C** = output quality (CIM ontology correctness, ABox completeness, SPARQL accuracy)
- **A** = AI Agent (Claude, GPT, or specialized CIM agent)
- **ci** = context components (TBox subset, ABox instances, standards text, few-shot examples, memory)

The quality of Agent output is a function of context quality, not model capability.
Two identical models with different context produce radically different ontologies.

## Project Scale

| Asset | Count | Source |
|-------|-------|--------|
| owl:Class definitions | 545 | 17 namespaces across `_index_v4.ttl` import chain |
| TBox TTL files | 15 | `ontology/layer0-4` + `bridge/` + `ontology_skeleton.ttl` |
| ABox TTL files | 9 | `abox/nbu_*.ttl` (clinic, FAS, BAS t0-t2, CMMS, events, pset) |
| Named Graphs | 9 | graph/tbox, graph/ifc, graph/bas/*, graph/cmms, graph/fas, graph/event |
| Total triples | 61,941 | Measured via `rdflib` graph enumeration |
| SPARQL queries | 14 | 9 business + 5 validation (`cross_agent_validation.sparql`) |
| Validation pipeline | 12 steps | step1 (IFC parse) through step12 (MVP end-to-end) |
| CIM Agents | 9 | Agent-01 (Topology) through Agent-09 (Integration) |
| MVP | L2 fire response | 10 action nodes, 5-state event machine, 62 FAS detectors |

## Directory Structure

### AI 系统设计 (00-40): 上下文工程框架

| Dir | Purpose | Analogy |
|-----|---------|---------|
| `00_foundations/` | Context theory + mathematical model | Atoms and Molecules |
| `10_system_design/` | CIM knowledge graph as context infrastructure | Cells and Organs |
| `20_agent_protocols/` | 9-Agent context contracts + handoff protocols | Neural Pathways |
| `30_memory_retrieval/` | Named Graph RAG + SPARQL as retrieval | Memory Systems |
| `40_evaluation/` | Context quality metrics + validation pipeline | Measurement |

### 领域上下文 (50-90): 医疗建筑领域知识

| Dir | Purpose | Key Question |
|-----|---------|-------------|
| `50_domain_context/` | 领域问题定义 + CIM 解决方案 | CIM 解决什么问题? |
| `60_data_architecture/` | TBox/ABox 分离 + Named Graph + ID 治理 | CIM 如何组织数据? |
| `70_application_support/` | 8 个 SPARQL 查询模式 + MVP 事件处置 | CIM 如何支撑应用? |
| `80_case_validation/` | 12 步验证流水线 + 全部实测结果 | CIM 如何证明有效? |
| `90_evolution/` | M6-M7 近期 + 中长期演进路线 | CIM 下一步去哪? |

### 已归档 (旧目录, 内容已迁移至 50-90)

| Dir | Status | Migrated To |
|-----|--------|-------------|
| `50_templates_old/` | 已迁移 | 上下文契约模板 → `70_application_support/` |
| `60_field_integration_old/` | 已迁移 | MVP 场栈 → `70_application_support/` + `80_case_validation/` |

## Quick Reference

### AI 系统设计

| File | What It Answers |
|------|-----------------|
| [context_theory.md](00_foundations/context_theory.md) | What is context? How is it different from a prompt? |
| [knowledge_graph_as_context.md](10_system_design/knowledge_graph_as_context.md) | How do Named Graphs serve as context partitions? |
| [nine_agent_context_contracts.md](20_agent_protocols/nine_agent_context_contracts.md) | What context does each Agent consume and produce? |
| [rag_strategy.md](30_memory_retrieval/rag_strategy.md) | When to SPARQL-retrieve vs full-load TTL? |
| [context_quality_metrics.md](40_evaluation/context_quality_metrics.md) | How do we measure context quality (beyond SHACL)? |

### 领域上下文

| File | What It Answers |
|------|-----------------|
| [medical_building_domain.md](50_domain_context/medical_building_domain.md) | What domain problem does CIM solve? (5 MEP systems, 3 data silos, standards gaps) |
| [data_organization.md](60_data_architecture/data_organization.md) | How does CIM organize data? (TBox/ABox, Named Graphs, ID governance) |
| [application_patterns.md](70_application_support/application_patterns.md) | How does CIM support applications? (8 SPARQL patterns, MVP event machine) |
| [validation_evidence.md](80_case_validation/validation_evidence.md) | How do we prove CIM works? (12-step pipeline, all test results) |
| [roadmap.md](90_evolution/roadmap.md) | Where does CIM go next? (M6-M7, real BAS, multi-site, AI) |

## Relationship to Existing Assets

```
Context Engineering/          <-- Document library (for humans)
  00_foundations/              Theory docs, vision, architecture
  10_guides/                  Role-specific guides
  ...

context_engineering/          <-- Runtime context design (for AI agents)
  00_foundations/              How context works
  20_agent_protocols/         What each Agent receives at inference time
  30_memory_retrieval/        How the knowledge graph serves context
  ...

project_deliverables/         <-- The actual knowledge graph
  version02/cim/
    ontology/                 TBox (15 TTL files, 545 classes)
    abox/                     ABox (9 TTL files, instances)
    rules/                    SHACL + SPARQL validation
```

Context Engineering bridges the gap between the knowledge graph (data) and the agents
(consumers). Without it, agents either get too much context (noise) or too little (blind spots).
