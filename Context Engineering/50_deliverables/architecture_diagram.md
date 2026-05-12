# 架构图 (Architecture Diagrams)

**文档 ID**: `CIMU-DLVR-03-架构图`
**最后更新**: 2026-05-11

---

## 1. CIM-PIM-PSM 三层架构

```
┌─────────────────────────────────────────────────────────┐
│                    CIM (Common Information Model)        │
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
                          │ owl:imports + SHACL
                          v
┌─────────────────────────────────────────────────────────┐
│                    PIM (Platform-Independent Model)       │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  IFC ABox    │  │  BAS ABox    │  │  CMMS ABox   │  │
│  │ 1210 instances│  │ 时序读数     │  │ 工单实例     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐                     │
│  │  FAS ABox    │  │ Security ABox│                     │
│  │ 消防实例     │  │ 安全事件     │                     │
│  └──────────────┘  └──────────────┘                     │
│                                                         │
│  61,941 triples  |  3 data sources                      │
└─────────────────────────┬───────────────────────────────┘
                          │ Named Graphs + SPARQL
                          v
┌─────────────────────────────────────────────────────────┐
│                    PSM (Platform-Specific Model)          │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Apache Jena Fuseki (Docker)                      │   │
│  │  ┌────────────────────────────────────────────┐   │   │
│  │  │ Named Graphs:                              │   │   │
│  │  │  <graph:ifc>  <graph:bas>  <graph:cmms>    │   │   │
│  │  │  <graph:fas>  <graph:security>             │   │   │
│  │  └────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ FastAPI     │  │ 9 SPARQL     │  │ HTML前端     │   │
│  │ REST API    │  │ 查询模板     │  │ Dashboard    │   │
│  └─────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────┘
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
