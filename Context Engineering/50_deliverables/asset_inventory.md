# 资产清单 (Asset Inventory)

**文档 ID**: `CIMU-DLVR-02-资产清单`
**最后更新**: 2026-05-11

---

## 概述

CIM 项目全部技术资产位于 `project_deliverables/version02/`，共 **95+ 文件**。
以下按类别列出完整清单。

---

## 1. TBox 本体文件 (15 files)

| # | 文件路径 | 层级 | 主要内容 |
|---|----------|------|----------|
| 1 | `cim/ontology/layer0_foundational.ttl` | L0 | BFO 2020 对齐 |
| 2 | `cim/ontology/layer1_conceptual.ttl` | L1 | FlowPath, ConnectionPoint |
| 3 | `cim/ontology/layer2_reference.ttl` | L2 | Medium, Standard |
| 4 | `cim/ontology/layer3_design.ttl` | L3 | DesignRequirement, LOD/LOI |
| 5 | `cim/ontology/layer4_operational.ttl` | L4 | AlarmRecord, WorkOrder |
| 6 | `cim/ontology/layer4_control_strategies.ttl` | L4 | DDC, 排烟/医气策略 |
| 7 | `cim/ontology/layer4_security_event.ttl` | L4 | SecurityEvent, ActionChain |
| 8 | `cim/ontology/layer4_fas_security.ttl` | L4 | FAS 消防设备 |
| 9 | `cim/ontology/layer4_cmms.ttl` | L4 | ISO 14224 工单 |
| 10 | `cim/ontology/_index_v4.ttl` | 索引 | owl:imports 全模块 |
| 11 | `cim/ontology/bridge/bridge_ifc.ttl` | 桥接 | IFC4 映射 |
| 12 | `cim/ontology/bridge/bridge_brick.ttl` | 桥接 | Brick 1.3 映射 |
| 13 | `cim/ontology/bridge/bridge_ashrae223p.ttl` | 桥接 | ASHRAE 223P 映射 |
| 14 | `cim/ontology/bridge/bridge_fso.ttl` | 桥接 | FSO 映射 |
| 15 | `cim/ontology/bridge/bridge_bacnet.ttl` | 桥接 | BACnet 映射 |

**合计**: 545 owl:Class, 5395 TBox triples

---

## 2. ABox 实例文件 (9 files)

| # | 文件路径 | 内容 |
|---|----------|------|
| 1 | `cim/abox/nbu_medical_clinic_instances.ttl` | 宣武医院 IFC→CIM 实例 |
| 2 | `cim/abox/nbu_pset_enrichment.ttl` | 属性集扩充实例 |
| 3 | `cim/abox/nbu_fas_instances.ttl` | FAS 消防设备实例 |
| 4 | `cim/abox/nbu_security_events.ttl` | 安全事件实例 |
| 5 | `cim/abox/nbu_cmms_workorders.ttl` | CMMS 工单实例 |
| 6 | `cim/abox/nbu_bas_readings.ttl` | BAS 读数 (合并) |
| 7 | `cim/abox/nbu_bas_readings_t0.ttl` | BAS 读数 T0 |
| 8 | `cim/abox/nbu_bas_readings_t1.ttl` | BAS 读数 T1 |
| 9 | `cim/abox/nbu_bas_readings_t2.ttl` | BAS 读数 T2 |

**合计**: 1210+ instances

---

## 3. 其他 CIM 模块文件

| # | 文件路径 | 内容 |
|---|----------|------|
| 1 | `cim/ontology_skeleton.ttl` | 本体骨架 (核心12类) |
| 2 | `cim/_index.ttl` | 总索引 |
| 3 | `cim/equipment/mechanical.ttl` | 机械设备层级 |
| 4 | `cim/equipment/electrical.ttl` | 电气设备层级 |
| 5 | `cim/equipment/equipment_hierarchy.ttl` | 设备总层级 |
| 6 | `cim/spaces/medical_special_spaces.ttl` | 医疗专用空间 |
| 7 | `cim/control/sensors.ttl` | 传感器/执行器 |
| 8 | `cim/coupling/equipment_location.ttl` | 设备-空间耦合 |
| 9 | `cim/metering/metering_hierarchy.ttl` | 计量层级 |
| 10 | `cim/flow/` | 流动模型 (目录) |
| 11 | `cim/rules/shacl_constraints.ttl` | SHACL 约束 |
| 12 | `cim/rules/cross_agent_validation.sparql` | 交叉验证 SPARQL |

---

## 4. 仿真系统 (21 files)

| 类别 | 文件 | 说明 |
|------|------|------|
| 核心引擎 | `simulation/core/stage_gate_engine.py` | 阶段门验证引擎 |
| | `simulation/core/ontology_loader.py` | 本体加载器 |
| | `simulation/core/namespace_registry.py` | 命名空间注册表 |
| 验证器 | `simulation/validators/shacl_compliance.py` | SHACL 合规检查 |
| | `simulation/validators/flow_topology.py` | 流动拓扑验证 |
| | `simulation/validators/conservation_engine.py` | 守恒定律验证 |
| | `simulation/validators/bfo_prereq.py` | BFO 前提验证 |
| | `simulation/validators/lod_loi_checker.py` | LOD/LOI 检查 |
| | `simulation/validators/event_response_validator.py` | 事件响应验证 |
| 仿真器 | `simulation/bas_bacnet_simulator.py` | BAS/BACnet 仿真 |
| | `simulation/cmms_simulator.py` | CMMS 工单仿真 |
| | `simulation/run_simulation.py` | 仿真运行入口 |
| 场景 | `simulation/scenario/chiller_plant.ttl` | 冷站场景 |
| | `simulation/scenario/ward_floor_5f.ttl` | 病房楼5F场景 |
| | `simulation/scenario/surgical_wing.ttl` | 手术区场景 |
| | `simulation/scenario/smoke_alarm_drill.ttl` | 烟感报警演练场景 |

---

## 5. 平台部署 (17 files)

| 类别 | 文件 | 说明 |
|------|------|------|
| Docker | `platform/docker/fuseki-config.ttl` | Fuseki 配置 |
| 加载脚本 | `platform/load_named_graphs.py` | Named Graph 加载 |
| API | `platform/api/main.py` | FastAPI 后端 |
| 前端 | `platform/frontend/index.html` | 主仪表盘 |
| | `platform/frontend/index_mvp.html` | MVP 仪表盘 |
| SPARQL | `platform/queries/chiller_plant_status.sparql` | 冷站状态 |
| | `platform/queries/floor_dashboard.sparql` | 楼层仪表盘 |
| | `platform/queries/equipment_lifecycle.sparql` | 设备生命周期 |
| | `platform/queries/energy_anomaly.sparql` | 能耗异常 |
| | `platform/queries/maintenance_due_30d.sparql` | 30天维保 |
| | `platform/queries/bas_trend_24h.sparql` | BAS 24h趋势 |
| | `platform/queries/fas_zone_status.sparql` | FAS 区域状态 |
| | `platform/queries/ifc_bas_cmms_triangle.sparql` | 3源联邦 |
| | `platform/queries/eq_full_status.sparql` | 设备完整状态 |

---

## 6. MVP 安防系统 (12 files)

| 类别 | 文件 | 说明 |
|------|------|------|
| 引擎 | `mvp/engine/sim_clock.py` | 仿真时钟 |
| | `mvp/engine/event_engine.py` | 事件引擎 |
| | `mvp/engine/event_state_machine.py` | 5态状态机 |
| | `mvp/engine/action_chain_executor.py` | 动作链执行器 |
| | `mvp/engine/situation_report.py` | 态势报告 |
| | `mvp/engine/api_mvp_extension.py` | API 扩展 |
| 场景 | `mvp/scenario/smoke_alarm_scenario.py` | 烟感报警场景 |
| 平台 | `mvp/platform/index.html` | MVP 可视化平台 |

---

## 7. 元数据与配置

| 文件 | 说明 |
|------|------|
| `cim/data_dictionary.yaml` | 数据字典 |
| `cim/global_id_registry.yaml` | 全局 ID 注册表 |
| `cim/cross_references.yaml` | 交叉引用 |
| `cim/dependency_graph.json` | 依赖图 |
| `cim/cim_meta_schema.json` | 元模式 |
| `cim/task_manifest.json` | 任务清单 |
| `cim/source_file_audit.json` | 源文件审计 |
| `cim/validation_rules_schema.json` | 验证规则模式 |
| `cim/cross_agent_gap_analysis.json` | Agent 差距分析 |
| `cim/maintenance_schedule_matrix.yaml` | 维保排程矩阵 |
| `cim/alarm_rule_instances.yaml` | 告警规则实例 |

---

## 相关文件

- 里程碑总结: `Context Engineering/50_deliverables/milestone_summary.md`
- 架构图: `Context Engineering/50_deliverables/architecture_diagram.md`
