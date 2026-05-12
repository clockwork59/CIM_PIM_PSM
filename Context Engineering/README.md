# CIM统一领域模型文档导航

**文档体系 ID**: `CIMU-CENG-DOMAIN-V2`
**面向受众**: 医疗建筑模型专家、BIM工程师、数据工程师、架构师、系统运维专家
**最后更新**: 2026-05-11

**项目状态**: M1 ✅ M2 ✅ M3 ✅ M4 ✅ M5 ✅ MVP ✅
**核心指标**: 545 owl:Class | 61,941 triples | 3 data sources | 12-step validation

---

## 项目里程碑

| 里程碑 | 状态 | 关键交付物 | 度量指标 |
|--------|------|-----------|----------|
| M1 | ✅ | CIM v4.0 TBox (4层+5桥接) | 545 classes, 5395 triples |
| M2 | ✅ | IFC→CIM ABox 转换 | 1210 instances, SHACL=0 |
| M3 | ✅ | 3源联邦 SPARQL | 5/5 queries |
| M4 | ✅ | PIM 平台 (Fuseki+API) | 61,941 triples, 10/10 |
| M5 | ✅ | PSM 实例化 (FAS) | 28/28 validation |
| MVP | ✅ | 安防可视化平台 | L2 fire, 10/10 actions |

详见 [50_deliverables/milestone_summary.md](./50_deliverables/milestone_summary.md)

---

## 文档地图

### [00_foundations/](./00_foundations/) - 理论基础 (11篇)

**核心本体 (必读)**:
- [03_cim_ontology_introduction.md](./00_foundations/03_cim_ontology_introduction.md) - CIM本体导论
- [04_cim_pim_psm_architecture.md](./00_foundations/04_cim_pim_psm_architecture.md) - CIM-PIM-PSM三层架构详解
- [10_ontology_integration.md](./00_foundations/10_ontology_integration.md) - 本体整合(BIM/IFC/Brick/REC/ASHRAE)

**概念体系**:
- [01_vision_and_goals.md](./00_foundations/01_vision_and_goals.md) - 愿景与目标
- [02_cim_manifesto.md](./00_foundations/02_cim_manifesto.md) - CIM宣言：从实体到数字孪生
- [05_system_taxonomy.md](./00_foundations/05_system_taxonomy.md) - 医疗建筑系统分类体系
- [06_space_hierarchy.md](./00_foundations/06_space_hierarchy.md) - 建筑空间层级模型
- [07_flow_models.md](./00_foundations/07_flow_models.md) - 流动模型：物质-能量-信息
- [08_topology_theory.md](./00_foundations/08_topology_theory.md) - 拓扑网络理论
- [09_control_systems.md](./00_foundations/09_control_systems.md) - 控制系统与计量体系
- [11_resource_role.md](./00_foundations/11_resource_role.md) - 资源、角色与权限
- [12_value_proposition.md](./00_foundations/12_value_proposition.md) - 价值主张与ROI

### [10_guides/](./10_guides/) - 实践指南 (6篇)

- [01_stakeholder_guide.md](./10_guides/01_stakeholder_guide.md) - 利益相关方指南
- [02_bim_engineer_guide.md](./10_guides/02_bim_engineer_guide.md) - BIM工程师实施指南
- [03_data_engineer_guide.md](./10_guides/03_data_engineer_guide.md) - 数据工程师接入指南
- [04_architect_guide.md](./10_guides/04_architect_guide.md) - 架构师指南
- [05_researcher_guide.md](./10_guides/05_researcher_guide.md) - 研究员与分析师指南
- [06_knowledge_contributor_guide.md](./10_guides/06_knowledge_contributor_guide.md) - 知识贡献者指南

### [20_templates/](./20_templates/) - 模板库 (5篇)

- [system_topology_template.md](./20_templates/system_topology_template.md) - 系统拓扑模板
- [space_definition_template.md](./20_templates/space_definition_template.md) - 空间定义模板
- [equipment_modeling_template.md](./20_templates/equipment_modeling_template.md) - 设备建模模板
- [flow_path_template.md](./20_templates/flow_path_template.md) - 流动路径模板
- [control_loop_template.md](./20_templates/control_loop_template.md) - 控制回路模板

### [30_examples/](./30_examples/) - 案例研究 (5篇)

- [cim_operating_room_modeling.md](./30_examples/cim_operating_room_modeling.md) - 手术室环境控制CIM建模案例
- [cim_pim_psm_transformation_chain.md](./30_examples/cim_pim_psm_transformation_chain.md) - CIM-PIM-PSM 完整变换链
- [healthcare_core_ontology.md](./30_examples/healthcare_core_ontology.md) - 医疗核心本体案例
- [hvac_pim_interoperability.md](./30_examples/hvac_pim_interoperability.md) - HVAC PIM互操作案例
- [cim_security_event_modeling.md](./30_examples/cim_security_event_modeling.md) - **L2电气火灾安全事件建模案例** (NEW)

### [40_reference/](./40_reference/) - 参考资料 (4篇)

- [cim_class_catalog.md](./40_reference/cim_class_catalog.md) - **CIM 545类目录** — 按命名空间汇总全部 owl:Class
- [standards_alignment.md](./40_reference/standards_alignment.md) - **11项标准对齐映射** — IFC/Brick/ASHRAE/FSO/BACnet/BFO/ISO
- [glossary.md](./40_reference/glossary.md) - **术语表** — 40+ 中英术语定义
- [validation_pipeline.md](./40_reference/validation_pipeline.md) - **12步验证管线** — 从IFC到MVP端到端

### [50_deliverables/](./50_deliverables/) - 交付成果 (3篇)

- [milestone_summary.md](./50_deliverables/milestone_summary.md) - **M1-M5+MVP 里程碑总结** — 进度、交付物、度量
- [asset_inventory.md](./50_deliverables/asset_inventory.md) - **资产清单** — 95+ 文件完整索引
- [architecture_diagram.md](./50_deliverables/architecture_diagram.md) - **架构图** — CIM-PIM-PSM + Named Graph + MVP

---

## 快速开始

### 路径 A: 了解项目

1. **了解愿景**: 从 [01_vision_and_goals](./00_foundations/01_vision_and_goals.md) 开始
2. **理解本体**: 阅读 [03_cim_ontology_introduction](./00_foundations/03_cim_ontology_introduction.md)
3. **掌握架构**: 学习 [04_cim_pim_psm_architecture](./00_foundations/04_cim_pim_psm_architecture.md)
4. **看看案例**: 查阅 [30_examples/](./30_examples/)

### 路径 B: 查看成果

1. **里程碑总览**: 阅读 [milestone_summary.md](./50_deliverables/milestone_summary.md)
2. **资产清单**: 浏览 [asset_inventory.md](./50_deliverables/asset_inventory.md) 了解全部文件
3. **架构图**: 查看 [architecture_diagram.md](./50_deliverables/architecture_diagram.md) 理解系统全貌
4. **类目录**: 查阅 [cim_class_catalog.md](./40_reference/cim_class_catalog.md) 了解 545 类分布

---

## 文档统计

- **总文档数**: 37 篇 (.md files in Context Engineering/)
- **理论基础**: 11 篇 (00_foundations/)
- **实践指南**: 6 篇 (10_guides/)
- **模板库**: 5 篇 (20_templates/)
- **案例研究**: 5 篇 (30_examples/)
- **参考资料**: 4 篇 (40_reference/)
- **交付成果**: 3 篇 (50_deliverables/)
- **最后更新**: 2026-05-11

---

## 相关资源

- **项目计划**: [plans/项目总控计划.md](../plans/项目总控计划.md)
- **Agent体系**: [docs/agents/](../docs/agents/) (9 个专业Agent定义)
- **技术资产**: [project_deliverables/version02/](../project_deliverables/version02/) (95+ 文件)
- **可视化**: [codex/](../codex/) (HTML 交互式可视化)
- **项目根 README**: [CLAUDE.md](../CLAUDE.md) (项目总体说明)
