# CIM 安全事件建模案例 — L2 电气火灾处置

**文档 ID**: `CIMU-CASE-05-安全事件建模`
**最后更新**: 2026-05-11

---

## 场景概述

**场景**: 某三甲医院内科楼 5F 配电室烟感探测器触发报警，系统判定为 L2 级电气火灾事件。
**目标**: 展示 CIM SecurityEvent 本体如何建模完整的 10 步应急处置流程。
**数据文件**: `project_deliverables/version02/simulation/scenario/smoke_alarm_drill.ttl`

---

## TBox 类映射

CIM `layer4_security_event.ttl` 定义了安全事件处置的全要素本体：

| CIM TBox 类 | 命名空间 | 场景中的作用 |
|-------------|----------|-------------|
| `cim-se:SecurityEvent` | security_event | 安全事件基类 (BFO Occurrent) |
| `cim-se:FireEvent` | security_event | 火灾事件子类 |
| `cim-se:EmergencyPlan` | security_event | 应急预案模板 |
| `cim-se:FireResponsePlan` | security_event | 火灾处置预案子类 |
| `cim-se:ActionChain` | security_event | 有序动作序列容器 |
| `cim-se:ActionNode` | security_event | 单个可执行原子动作 |
| `cim-se:ResponderRole` | security_event | 响应者角色 (操作员/技术员/安保) |
| `cim-se:BASCommand` | security_event | BAS 联动指令基类 |
| `cim-se:PowerCutoffCommand` | security_event | 切断电源指令 |
| `cim-se:BroadcastCommand` | security_event | 区域广播指令 |
| `cim-se:TriggerCondition` | security_event | 预案触发条件 |
| `cim-se:EventSeverityLevel` | security_event | 事件严重等级 (L1/L2/L3) |

---

## 10 步动作链 (ActionChain)

以下是 `smoke_alarm_drill.ttl` 中定义的 L2 电气火灾处置动作链：

| # | ActionNode | 动作名称 | 执行方式 | 角色 | 时限(s) | BAS指令 |
|---|-----------|----------|----------|------|---------|---------|
| 1 | ACTION-001 | 确认火情 | 人工确认 | ControlRoomOperator | 120 | - |
| 2 | ACTION-002 | 切断电源 | 自动执行 | - | 30 | PowerCutoffCommand |
| 3 | ACTION-003 | 启动灭火 | 人工执行 | ElectricalTechnician | 300 | - |
| 4 | ACTION-004 | 区域广播 | 自动执行 | - | 10 | BroadcastCommand |
| 5 | ACTION-005 | 启动疏散 | 人工执行 | SecurityTeamLeader | 600 | - |
| 6 | ACTION-006 | 打开门禁 | 自动执行 | - | 5 | DoorReleaseCommand |
| 7 | ACTION-007 | 电梯迫降 | 自动执行 | - | 10 | ElevatorRecallCommand |
| 8 | ACTION-008 | 通知消防 | 人工执行 | ControlRoomOperator | 60 | - |
| 9 | ACTION-009 | 现场指挥 | 人工执行 | SecurityTeamLeader | 600 | - |
| 10 | ACTION-010 | 事件闭环 | 人工确认 | ControlRoomOperator | - | - |

**总处置时间**: 840s < 900s (L2 时限)
**BAS 联动指令**: 4 条自动指令

---

## ABox 实例片段

```turtle
# 安全事件实例 (FireEvent)
inst:EVT-20240115-001 a cim-se:FireEvent ;
    cim-se:eventID "EVT-20240115-001" ;
    cim-se:hasSeverityLevel cim-se:SeverityL2 ;
    cim-se:hasEventStatus cim-se:StatusInProgress ;
    cim-se:triggeredByAlarm inst:ALARM-20240115-001 ;
    cim-se:occursInSpace inst:5F-ELECTRICAL-ROOM ;
    cim-se:matchesPlan inst:PLAN-FIRE-L2-001 .

# 动作链容器 (ActionChain)
inst:AC-FIRE-L2-001 a cim-se:ActionChain ;
    cim-se:hasActionNode inst:ACTION-001, inst:ACTION-002, ... inst:ACTION-010 .

# 动作节点示例 (ActionNode — 切断电源)
inst:ACTION-002 a cim-se:ActionNode ;
    cim-se:actionSequence "2"^^xsd:integer ;
    cim-se:actionTimeLimit "30"^^xsd:integer ;
    cim-se:hasExecutionMode cim-se:AutomaticExecution ;
    cim-se:dependsOnAction inst:ACTION-001 ;
    cim-se:issuesBASCommand inst:CMD-POWER-CUT-001 .

inst:CMD-POWER-CUT-001 a cim-se:PowerCutoffCommand ;
    rdfs:label "切断内科楼5F配电室非消防电源"@zh-CN .
```

---

## 5 态状态机

SecurityEvent 具有完整的 5 态状态机生命周期：

```
待确认 → 已确认 → 处理中 → 已闭环 → 已归档
 (Pending)  (Confirmed) (InProgress) (Closed) (Archived)
```

每个状态转换由 ActionNode 的完成驱动，MVP EventEngine 实现了这一状态机。

---

## 相关文件

- TBox 定义: `project_deliverables/version02/cim/ontology/layer4_security_event.ttl`
- ABox 场景: `project_deliverables/version02/simulation/scenario/smoke_alarm_drill.ttl`
- MVP 引擎: `project_deliverables/version02/mvp/engine/event_engine.py`
- 术语表: `Context Engineering/40_reference/glossary.md`
