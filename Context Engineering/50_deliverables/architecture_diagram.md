# 架构图 (Architecture Diagrams)

**文档 ID**: `CIMU-DLVR-03-架构图`
**最后更新**: 2026-05-13

---

> **MBSE 说明**: CIM-PIM-PSM 是 MBSE（基于模型的系统工程）的三个抽象层级，
> 不是三个独立产出物。CIM 约束 PIM，PIM 约束 PSM，PSM 可替换。
> 详见 [04_cim_pim_psm_architecture.md](../00_foundations/04_cim_pim_psm_architecture.md)

---

## 1. CIM-PIM-PSM 三层架构 (MBSE 视角)

```
┌─────────────────────────────────────────────────────────┐
│  CIM (领域知识层) — 不依赖任何支持系统                     │
│  "医疗建筑的世界是什么样的"                                │
│  545 owl:Class · 本体 · 标准 · 惯例 · FMEA · 预案知识     │
│  ← 最稳定，年级变化                                       │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │ Layer 0  │  │ Layer 1  │  │ Layer 2  │  │Layer3-4│ │
│  │ BFO基础  │  │ 概念层   │  │ 参考层   │  │设计+运营│ │
│  │Continuant│  │FlowPath  │  │ Medium   │  │Alarm   │ │
│  │Occurrent │  │ConnPoint │  │ Standard │  │WorkOrder│ │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘ │
│                                                         │
│  ┌─────────────── Bridge Ontologies ──────────────────┐ │
│  │ IFC4 | Brick 1.3 | ASHRAE 223P | FSO | BACnet    │ │
│  └────────────────────────────────────────────────────┘ │
│                                                         │
│  545 owl:Class  |  5,395 TBox triples                   │
└─────────────────────────┬───────────────────────────────┘
                          │ CIM 约束 PIM (owl:imports + SHACL)
                          v
┌─────────────────────────────────────────────────────────┐
│  PIM (系统工程层) — CIM 的工程化，与技术无关               │
│  "系统需要什么功能、怎么验证"                              │
│  仿真引擎 · 状态机 · Named Graph · SPARQL · 验证管线      │
│  ← 中等稳定，月级迭代                                     │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ 12步验证管线  │  │ 守恒引擎    │  │ 联邦SPARQL   │  │
│  │ validation   │  │ conservation │  │ federation   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Named Graph  │  │ 状态机      │  │ 异常检测逻辑  │  │
│  │ 架构设计     │  │ 5态模型     │  │ anomaly det. │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                         │
│  9 SPARQL queries  |  5 named graphs  |  state machine  │
└─────────────────────────┬───────────────────────────────┘
                          │ PIM 约束 PSM (Named Graphs + 技术选型)
                          v
┌─────────────────────────────────────────────────────────┐
│  PSM (项目实例层) — PIM 的实例化，面向现实约束              │
│  "用什么技术、装什么数据"                                  │
│  Fuseki · FastAPI · NBU 1210实例 · BAS · CMMS · HTML     │
│  ← 最易变，日/时级更新                                     │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Apache Jena Fuseki (Docker)                      │   │
│  │  ┌────────────────────────────────────────────┐   │   │
│  │  │ Named Graphs (ABox 数据装载):              │   │   │
│  │  │  <graph:ifc>  1210 instances               │   │   │
│  │  │  <graph:bas>  1055 BAS points              │   │   │
│  │  │  <graph:cmms> 735 work orders              │   │   │
│  │  │  <graph:fas>  62 FAS instances             │   │   │
│  │  │  <graph:security> 安全事件                  │   │   │
│  │  └────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ FastAPI     │  │ SimClock +   │  │ HTML前端     │   │
│  │ REST API    │  │ EventEngine  │  │ Dashboard    │   │
│  └─────────────┘  └──────────────┘  └──────────────┘   │
│                                                         │
│  61,941 triples  |  3 data sources  |  PSM 可替换       │
└─────────────────────────────────────────────────────────┘

分层依赖: CIM 约束 PIM → PIM 约束 PSM → PSM 可替换
复用价值: 同一 CIM+PIM 映射到不同医院的 PSM
```

---

## 2. Named Graph 布局

```
Fuseki Dataset: /cim-medical
│
├── <https://cim.medical/graph/tbox>
│   └── 15 TBox TTL files (545 classes)
│
├── <https://cim.medical/graph/ifc>
│   └── nbu_medical_clinic_instances.ttl
│   └── nbu_pset_enrichment.ttl
│
├── <https://cim.medical/graph/bas>
│   └── nbu_bas_readings.ttl
│   └── nbu_bas_readings_t0/t1/t2.ttl
│
├── <https://cim.medical/graph/cmms>
│   └── nbu_cmms_workorders.ttl
│
├── <https://cim.medical/graph/fas>
│   └── nbu_fas_instances.ttl
│
└── <https://cim.medical/graph/security>
    └── nbu_security_events.ttl
```

---

## 3. MVP 安防系统架构

```
┌─────────────────────────────────────────────────────┐
│                   MVP 可视化平台                      │
│                  (index.html)                         │
│                                                     │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐         │
│  │ 事件面板  │ │ 动作链面板│ │ 态势面板  │         │
│  │EventPanel │ │ActionPanel│ │ SitReport │         │
│  └─────┬─────┘ └─────┬─────┘ └─────┬─────┘         │
│        │              │              │               │
│        └──────────────┼──────────────┘               │
│                       │ REST API                     │
└───────────────────────┼─────────────────────────────┘
                        │
┌───────────────────────┼─────────────────────────────┐
│  FastAPI + MVP Extension                             │
│                       │                              │
│  ┌────────────────────┼────────────────────────┐     │
│  │            EventEngine                       │     │
│  │                    │                         │     │
│  │  ┌─────────┐ ┌────┴─────┐ ┌──────────────┐ │     │
│  │  │SimClock │ │StateMach │ │ActionChain   │ │     │
│  │  │ 仿真时钟│ │ 5态状态机│ │Executor      │ │     │
│  │  └─────────┘ └──────────┘ │ 10动作节点   │ │     │
│  │                           └──────────────┘ │     │
│  └─────────────────────────────────────────────┘     │
│                       │                              │
│  ┌────────────────────┼────────────────────────┐     │
│  │         CIM TBox + ABox (RDF)               │     │
│  │  SecurityEvent → FireEvent → ActionChain    │     │
│  │  → ActionNode(x10) → BASCommand(x4)        │     │
│  └─────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────┘

L2 电气火灾处置流程:
  烟感触发 → 确认火情(120s) → 切断电源(30s) → 启动灭火(300s)
  → 区域广播(10s) → 启动疏散(600s) → 打开门禁(5s)
  → 电梯迫降(10s) → 通知消防(60s) → 现场指挥(600s) → 事件闭环
  
  BAS 联动指令: PowerCutoff | Broadcast | DoorRelease | ElevatorRecall
  总处置时间: 840s < 900s (L2时限)
```

---

## 相关文件

- 三层架构详解: `Context Engineering/00_foundations/04_cim_pim_psm_architecture.md`
- 里程碑总结: `Context Engineering/50_deliverables/milestone_summary.md`
- 资产清单: `Context Engineering/50_deliverables/asset_inventory.md`
