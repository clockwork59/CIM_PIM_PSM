# 态势感知报告 (Situation Awareness Report)

**事件ID**: EVT-20240115-001
**事件类型**: FireEvent
**严重等级**: L2
**发生位置**: 内科楼5F配电室
**触发设备**: SD-5F-ER-001
**事件时间**: 2026-05-10T15:00:27.109782
**当前状态**: 已归档
**匹配预案**: PLAN-FIRE-L2-001 (L2级电气火灾处置预案)

## KPI 指标

| 指标 | 值 |
|------|-----|
| 总动作数 | 10 |
| 已完成 | 10 |
| 已超时 | 0 |
| 仿真总时长 | 840.0s |
| 等级时限 | 900s |
| 时限达标 | PASS |
| 实际运行耗时 | 0.201s |

## 动作执行进度

| # | 动作 | Action | 角色 | 模式 | 时限(s) | 耗时(s) | 达标 | 状态 |
|---|------|--------|------|------|---------|---------|------|------|
| 1 | 确认火情 | Confirm Fire | ControlRoomOperator | ManualConfirmation | 120 | 84.0 | Y | ✅ COMPLETED   已完成 |
| 2 | 切断电源 | Power Cutoff | SYSTEM | AutomaticExecution | 30 | 9.0 | Y | ✅ COMPLETED   已完成 |
| 3 | 启动灭火 | Fire Suppression | ElectricalTechnician | ManualExecution | 300 | 210.0 | Y | ✅ COMPLETED   已完成 |
| 4 | 区域广播 | Area Broadcast | SYSTEM | AutomaticExecution | 10 | 3.0 | Y | ✅ COMPLETED   已完成 |
| 5 | 启动疏散 | Evacuation | SecurityTeamLeader | ManualExecution | 600 | 420.0 | Y | ✅ COMPLETED   已完成 |
| 6 | 打开门禁 | Door Release | SYSTEM | AutomaticExecution | 10 | 3.0 | Y | ✅ COMPLETED   已完成 |
| 7 | 电梯迫降 | Elevator Recall | SYSTEM | AutomaticExecution | 30 | 9.0 | Y | ✅ COMPLETED   已完成 |
| 8 | 通知医护 | Notify Medical Staff | SYSTEM | AutomaticExecution | 30 | 9.0 | Y | ✅ COMPLETED   已完成 |
| 9 | 拨打119 | Call 119 | ControlRoomOperator | ManualConfirmation | 120 | 84.0 | Y | ✅ COMPLETED   已完成 |
| 10 | 通知领导 | Notify Management | SYSTEM | AutomaticExecution | 30 | 9.0 | Y | ✅ COMPLETED   已完成 |

## BAS 联动指令 (4 commands)

| # | 指令 | 来源动作 | 下发时间 |
|---|------|----------|----------|
| 1 | PowerCutoffCommand | [2] 切断电源 | 2026-05-10T15:00:27.160269 |
| 2 | BroadcastCommand | [4] 区域广播 | 2026-05-10T15:00:27.160329 |
| 3 | ElevatorRecallCommand | [7] 电梯迫降 | 2026-05-10T15:00:27.160344 |
| 4 | DoorReleaseCommand | [6] 打开门禁 | 2026-05-10T15:00:27.160383 |

## 人员调度 (3 roles)

| 角色 | 调度标签 | 执行动作 |
|------|----------|----------|
| ControlRoomOperator | 中控值班员 | [1] 确认火情, [9] 拨打119 |
| ElectricalTechnician | 电工班 | [3] 启动灭火 |
| SecurityTeamLeader | 保安队长 | [5] 启动疏散 |

## 事件状态转换 (4 transitions)

| # | 从 | 到 | 时间 |
|---|----|----|------|
| 1 | 待确认 | 已确认 | 2026-05-10T15:00:27.110013 |
| 2 | 已确认 | 处理中 | 2026-05-10T15:00:27.110024 |
| 3 | 处理中 | 已闭环 | 2026-05-10T15:00:27.311109 |
| 4 | 已闭环 | 已归档 | 2026-05-10T15:00:27.311119 |

## 事件时间线 (20 entries)

```
  2026-05-10T15:00:27  [ 1] 确认火情     START -> 中控值班员
  2026-05-10T15:01:51  [ 1] 确认火情     COMPLETE [84.0s] OK
  2026-05-10T15:00:27  [ 2] 切断电源     START -> SYSTEM
  2026-05-10T15:00:36  [ 2] 切断电源     COMPLETE [9.0s] OK
  2026-05-10T15:00:27  [ 4] 区域广播     START -> SYSTEM
  2026-05-10T15:00:30  [ 4] 区域广播     COMPLETE [3.0s] OK
  2026-05-10T15:00:27  [ 7] 电梯迫降     START -> SYSTEM
  2026-05-10T15:00:36  [ 7] 电梯迫降     COMPLETE [9.0s] OK
  2026-05-10T15:00:27  [ 8] 通知医护     START -> SYSTEM
  2026-05-10T15:00:36  [ 8] 通知医护     COMPLETE [9.0s] OK
  2026-05-10T15:00:27  [10] 通知领导     START -> SYSTEM
  2026-05-10T15:00:36  [10] 通知领导     COMPLETE [9.0s] OK
  2026-05-10T15:00:27  [ 3] 启动灭火     START -> 电工班
  2026-05-10T15:00:27  [ 5] 启动疏散     START -> 保安队长
  2026-05-10T15:00:27  [ 6] 打开门禁     START -> SYSTEM
  2026-05-10T15:00:30  [ 6] 打开门禁     COMPLETE [3.0s] OK
  2026-05-10T15:03:57  [ 3] 启动灭火     COMPLETE [210.0s] OK
  2026-05-10T15:00:27  [ 9] 拨打119    START -> 中控值班员
  2026-05-10T15:01:51  [ 9] 拨打119    COMPLETE [84.0s] OK
  2026-05-10T15:07:27  [ 5] 启动疏散     COMPLETE [420.0s] OK
```

---
*Generated: 2026-05-10T15:00:27*
*Plan: PLAN-FIRE-L2-001 V2.1*
*Ontology: cim-se:SituationAwareness / cim-se:EventClosureReport*
