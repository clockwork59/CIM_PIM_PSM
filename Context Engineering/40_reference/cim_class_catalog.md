# CIM 类目录 (Class Catalog)

**文档 ID**: `CIMU-REF-01-类目录`
**版本**: v4.0 | 545 owl:Class
**最后更新**: 2026-05-11

---

## 概述

CIM v4.0 TBox 包含 **545 个 owl:Class**，分布在 17+ 命名空间中。
本目录按命名空间汇总各域的类数量、关键类和来源文件。

---

## 命名空间-类目录

| # | 命名空间 | 类数量 | 关键类 | 来源文件 |
|---|----------|--------|--------|----------|
| 1 | `cim-equip` | 94 | AirHandlingUnit, Chiller, Transformer, Switchgear, UPS, SmokeDetector, OxygenManifold | `equipment/mechanical.ttl`, `equipment/electrical.ttl` |
| 2 | `cim-f` | 56 | Continuant, Occurrent, FlowProcess, Quality, Function, Role, BFO entity | `ontology/layer0_foundational.ttl` |
| 3 | `cim-space` | 47 | Building, Floor, Zone, Room, SurgeryRoom, ICU, EmergencyRoom, MechanicalRoom | `spaces/medical_special_spaces.ttl` |
| 4 | `cim-pt` | 43 | TemperatureSensor, HumiditySensor, PressureSensor, FlowSensor, CO2Sensor, PowerSensor, Setpoint | `control/sensors.ttl` |
| 5 | `cim-d` | 41 | DesignRequirement, PerformanceCriteria, LOD, LOI, designTag | `ontology/layer3_design.ttl` |
| 6 | `cim-o` | 38 | AssetRecord, MaintenanceOrder, AlarmRecord, EnergyConsumption, WorkOrder | `ontology/layer4_operational.ttl` |
| 7 | `cim-cs` | 37 | DDCStrategy, SequenceOfOperation, SmokeExhaustStrategy, MedicalGasStrategy, PIDLoop | `ontology/layer4_control_strategies.ttl` |
| 8 | `cim-flow` | 31 | FlowPath, FlowSegment, MassFlow, EnergyFlow, InformationFlow, ConnectionPoint | `ontology/layer1_conceptual.ttl` |
| 9 | `cim-med` | 28 | ChilledWater, HotWater, Steam, Oxygen, MedicalAir, N2O, Refrigerant | `ontology/layer2_reference.ttl` |
| 10 | `cim-se` | 26 | SecurityEvent, FireEvent, ActionChain, ActionNode, ResponderRole, BASCommand, EmergencyPlan | `ontology/layer4_security_event.ttl` |
| 11 | `cim-ctrl` | 21 | Sensor, Actuator, ControlLoop, Damper, Valve, VFD | `control/sensors.ttl` |
| 12 | `cim-cmms` | 13 | WorkOrder, PreventiveMaintenance, CorrectiveMaintenance, SparePart, Technician | `ontology/layer4_cmms.ttl` |
| 13 | `cim` | 12 | System, Equipment, Space, Point, Flow, Relationship | `ontology_skeleton.ttl` |
| 14 | `cim-fas` | 12 | FireAlarmPanel, SprinklerHead, FirePump, FireDamper, EmergencyLighting | `ontology/layer4_fas_security.ttl` |
| 15 | `cim-ref` | 11 | Standard, Regulation, CodeReference, GB50333, WS435, IEC60364 | `ontology/layer2_reference.ttl` |
| 16 | `cim-bacnet` | 9 | AnalogInput, AnalogOutput, BinaryInput, BinaryOutput, MultiStateInput | `ontology/bridge/bridge_bacnet.ttl` |
| 17 | 其他 | ~25 | bridge classes, alignment axioms | `ontology/bridge/*.ttl` |
| | **合计** | **545** | | |

---

## 按功能域分布

```
HVAC/电气/医气/消防/照明 (cim-equip)      ████████████████████  94
BFO过程/性质/功能/角色 (cim-f)             ████████████████      56
空间层级+医疗专用 (cim-space)              █████████████         47
数据点Sensor/Setpoint (cim-pt)             ████████████          43
设计需求/性能准则 (cim-d)                  ███████████           41
资产/维护/告警/能耗 (cim-o)                ██████████            38
DDC控制策略+排烟/医气 (cim-cs)             ██████████            37
流动模型Mass/Energy/Info (cim-flow)        ████████              31
流体介质 (cim-med)                         ███████               28
安全事件处置 (cim-se)                      ███████               26
传感器/执行器 (cim-ctrl)                   █████                 21
CMMS工单 (cim-cmms)                        ████                  13
核心 (cim)                                 ███                   12
FAS消防设备 (cim-fas)                      ███                   12
参考/标准 (cim-ref)                        ███                   11
BACnet协议 (cim-bacnet)                    ██                     9
其他 (bridge/alignment)                    ██████                ~25
```

---

## TBox 文件索引

所有 TBox 文件位于 `project_deliverables/version02/cim/ontology/`:

| 文件 | 层级 | 主要内容 |
|------|------|----------|
| `layer0_foundational.ttl` | L0 基础层 | BFO 2020 对齐, Continuant/Occurrent |
| `layer1_conceptual.ttl` | L1 概念层 | FlowPath, ConnectionPoint, 流动模型 |
| `layer2_reference.ttl` | L2 参考层 | Medium, Standard, 介质与标准 |
| `layer3_design.ttl` | L3 设计层 | DesignRequirement, LOD/LOI |
| `layer4_operational.ttl` | L4 运营层 | AlarmRecord, WorkOrder, Energy |
| `layer4_control_strategies.ttl` | L4 控制层 | DDC策略, 排烟/医气控制 |
| `layer4_security_event.ttl` | L4 安全层 | SecurityEvent, ActionChain, EmergencyPlan |
| `layer4_fas_security.ttl` | L4 FAS层 | 消防设备子类 |
| `layer4_cmms.ttl` | L4 CMMS层 | ISO 14224 工单模型 |
| `_index_v4.ttl` | 索引 | owl:imports 全部模块 |
| `bridge/bridge_ifc.ttl` | 桥接 | IFC4 equivalentClass |
| `bridge/bridge_brick.ttl` | 桥接 | Brick 1.3 ~60 equivalentClass |
| `bridge/bridge_ashrae223p.ttl` | 桥接 | ASHRAE 223P Medium/ConnectionPoint |
| `bridge/bridge_fso.ttl` | 桥接 | FSO v0.1.0 35 equipment + SPARQL |
| `bridge/bridge_bacnet.ttl` | 桥接 | BACnet 9 object types |

---

## 版本历史

| 版本 | 日期 | 类数量 | 变更 |
|------|------|--------|------|
| v3.4 | 2026-04 | 156 | 初始发布 (M1) |
| v4.0 | 2026-05-11 | 545 | +安全事件+控制策略+FAS+CMMS+bridge |
