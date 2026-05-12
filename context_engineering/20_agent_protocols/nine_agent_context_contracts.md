# 9-Agent 上下文契约

## 设计原则

每个 CIM Agent 的上下文契约定义三件事:
1. **输入上下文**: Agent 在推理时需要的信息 (TBox 子集, ABox 数据, 工具)
2. **输出上下文**: Agent 产生的信息 (TTL 文件, 验证报告, ID 注册表)
3. **传递规则**: 输出如何成为下游 Agent 的输入上下文

## Agent 间的上下文流动

```
Agent-01 (System Topology)
  输入: layer1_conceptual.ttl (介质/连接点), IFC 系统列表
  输出: 系统拓扑图, 系统 ID 注册表
  ──→ Agent-04 (Flow), Agent-05 (Coupling)

Agent-02 (Space Ontology)
  输入: IFC 空间层级, GB50333 空间标准
  输出: 空间层次树 (Building→Floor→Zone→Room), 功能分类
  ──→ Agent-05 (Coupling), Agent-08 (O&M)

Agent-03 (Equipment)
  输入: layer2_reference.ttl 设备类, bridge_brick.ttl 映射, IFC 设备清单
  输出: equipment_hierarchy.ttl, mechanical.ttl, electrical.ttl, 属性字典
  ──→ Agent-04/05/06/07

Agent-04 (Flow Model)
  输入: Agent-01 拓扑 + Agent-03 设备 + layer1_conceptual.ttl 流动类
  输出: 质量流/能量流/信息流路径
  ──→ Agent-05 (Coupling), Agent-07 (Metering)

Agent-05 (System-Space Coupling)
  输入: Agent-01 拓扑 + Agent-02 空间 + Agent-03 设备
  输出: equipment_location.ttl, 系统-空间耦合矩阵
  ──→ Agent-06 (Control), Agent-09 (Validation)

Agent-06 (Control System)
  输入: layer4_control_strategies.ttl + Agent-03 设备 + BAS 读数
  输出: sensors.ttl, 控制回路定义
  ──→ Agent-07 (Metering), Agent-09 (Validation)

Agent-07 (Metering System)
  输入: Agent-04 流动路径 + Agent-06 传感器 + 计费标准
  输出: metering_hierarchy.ttl, 计量分摊模型
  ──→ Agent-08 (O&M), Agent-09 (Validation)

Agent-08 (O&M Management)
  输入: Agent-03 设备 + Agent-02 空间 + nbu_cmms_workorders.ttl
  输出: 告警规则, 维保计划, 工单模板
  ──→ Agent-09 (Validation)

Agent-09 (Integration Validator)
  输入: ALL -- Agent-01~08 的全部输出 + 全量 TBox + 全量 ABox
  工具: pyshacl, SPARQL 验证, 仿真引擎
  输出: 验证报告, 缺口矩阵, 修复建议
```

## 上下文依赖图

```
        Agent-01 ──────────┐
            │               │
        Agent-02 ───┐       │
            │       │       │
        Agent-03 ───┤       │
            │       │       │
            ▼       ▼       ▼
        Agent-04  Agent-05
            │       │
            ▼       ▼
        Agent-06 ◄──┘
            │
            ▼
        Agent-07
            │
            ▼
        Agent-08
            │
            ▼
        Agent-09 ◄── (汇聚全部)
```

**关键路径**: Agent-01/02/03 可并行执行; Agent-04/05 依赖前三者;
Agent-06/07/08 顺序依赖; Agent-09 汇聚全部。

## 详细上下文契约

### Agent-01: System Topology Architect

```yaml
agent_id: Agent-01
agent_name: 系统拓扑建模师
context_input:
  required:
    - source: ontology/layer1_conceptual.ttl
      subset: "PART A -- 介质类 + PART B -- 连接点"
      token_budget: 3000
    - source: IFC 系统清单
      subset: "IfcSystem, IfcDistributionSystem"
      token_budget: 2000
  optional:
    - source: bridge/bridge_ifc.ttl
      subset: "IFC-to-CIM 系统映射"
      token_budget: 1500
context_output:
  files:
    - topology/system_topology.ttl
    - global_id_registry.yaml (系统 ID 部分)
  format: Turtle (RDF)
  handoff_to: [Agent-04, Agent-05]
quality_gate:
  shacl_violation: 0
  orphan_systems: 0
  id_uniqueness: 100%
```

### Agent-03: Equipment Ontology Architect

```yaml
agent_id: Agent-03
agent_name: 设备本体建模师
context_input:
  required:
    - source: ontology/layer2_reference.ttl
      subset: "设备类层次 (HVAC/Electrical/Plumbing/MedicalGas/FireProtection)"
      token_budget: 5000
    - source: bridge/bridge_brick.ttl
      subset: "owl:equivalentClass 映射"
      token_budget: 1500
    - source: IFC 设备清单
      subset: "IfcDistributionElement 子类实例"
      token_budget: 3000
  optional:
    - source: bridge/bridge_ashrae223p.ttl
      subset: "ASHRAE 设备标签映射"
      token_budget: 1000
    - source: data_dictionary.yaml
      subset: "设备属性定义"
      token_budget: 1500
context_output:
  files:
    - equipment/equipment_hierarchy.ttl
    - equipment/mechanical.ttl
    - equipment/electrical.ttl
  format: Turtle (RDF)
  validation: pyshacl against rules/shacl_constraints.ttl
  handoff_to: [Agent-04, Agent-05, Agent-06, Agent-07]
quality_gate:
  shacl_violation: 0
  orphan_instances: 0
  brick_alignment: ">= 90%"
```

### Agent-06: Control System Architect

```yaml
agent_id: Agent-06
agent_name: 控制系统建模师
context_input:
  required:
    - source: ontology/layer4_control_strategies.ttl
      subset: "控制回路类, 传感器类, 执行器类"
      token_budget: 3000
    - source: Agent-03 输出 (equipment_hierarchy.ttl)
      subset: "设备实例 ID 列表"
      token_budget: 2000
    - source: abox/nbu_bas_readings_t0.ttl
      subset: "BACnet 点位 (1,055 BACnet points)"
      token_budget: 4000
  optional:
    - source: bridge/bridge_bacnet.ttl
      subset: "BACnet-to-CIM 点位映射"
      token_budget: 1500
context_output:
  files:
    - control/sensors.ttl
  format: Turtle (RDF)
  handoff_to: [Agent-07, Agent-09]
quality_gate:
  shacl_violation: 0
  dangling_sensor: 0
  control_loop_completeness: "每回路必须有 sensor + actuator + setpoint"
```

### Agent-09: Integration Validator

```yaml
agent_id: Agent-09
agent_name: 模型整合验证师
context_input:
  required:
    - source: ALL Agent outputs (Agent-01 ~ Agent-08)
      token_budget: 30000
    - source: ontology/_index_v4.ttl (完整导入链)
      token_budget: 15000
    - source: rules/shacl_constraints.ttl
      token_budget: 3000
    - source: rules/cross_agent_validation.sparql
      token_budget: 2000
  tools:
    - pyshacl (SHACL 验证)
    - rdflib (图操作)
    - SPARQL endpoint (联合查询)
context_output:
  files:
    - cross_agent_gap_analysis.json
    - source_file_audit.json
    - COMPLETION_REPORT.md
  format: JSON + Markdown
  handoff_to: [人工审计, MVP 系统]
quality_gate:
  12_step_pipeline: "ALL PASS"
  cross_agent_reference_integrity: 100%
  named_graph_isolation: "无跨图泄漏"
```

## 上下文传递协议

### 协议 1: 文件传递 (当前实现)

Agent 输出写入 `project_deliverables/version02/cim/`, 下游 Agent 从同一路径读取。

优点: 简单, 可审计
缺点: 全文件传递, 无子集裁剪

### 协议 2: SPARQL 传递 (目标实现)

Agent 输出加载到 Named Graph, 下游 Agent 通过 SPARQL 检索所需子集。

优点: 按需检索, token 高效
缺点: 需要 SPARQL 端点运行

### 协议 3: 混合传递 (推荐)

- TBox 传递: 文件传递 (变化少, 可缓存)
- ABox 传递: SPARQL 检索 (变化多, 按需获取)
- 验证结果: 文件传递 (需要完整报告)
