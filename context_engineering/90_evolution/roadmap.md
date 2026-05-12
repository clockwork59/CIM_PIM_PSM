# CIM 演进路线

> 本文档回答: CIM 从哪里来, 到哪里去。

## 已完成 (M1-M5 + MVP)

| 里程碑 | 内容 | 关键指标 | 状态 |
|--------|------|---------|------|
| M1 | 本体骨架 | 545 owl:Class, 15 TBox, ISO 19650 四层 | DONE |
| M2 | ABox 实例化 | 9 ABox 文件, 61,941 三元组, NBU 实测数据 | DONE |
| M3 | 三源联邦 | IFC+BAS+CMMS 联邦, 5/5 SPARQL, Q3 三角闭环 11 行 | DONE |
| M4 | 验证流水线 | 12 步 pipeline, SHACL VIOLATION=0, 仿真门控 CRITICAL=0 | DONE |
| M5 | 平台服务 | SPARQL 端点, Named Graph, 10/10 平台查询 PASS | DONE |
| MVP | 安防应用 | L2 电气火灾, 10 动作, 5 状态机, 4 BAS 指令, 840s<900s | DONE |

**总计**: 545 类, 61,941 三元组, 3 数据源, 12 步验证, 1 个端到端 MVP。

## 近期 (M6-M7)

### M6: 真实 BAS 接入

**目标**: 从仿真器 (SimClock + 静态快照) 迁移到真实 BAS 数据流。

- MQTT/OPC-UA 网关替代仿真 BACnet 数据
- 时序数据库 (InfluxDB/TimescaleDB) 替代 3 快照轮换
- Named Graph `graph/bas/*` 改为滑动窗口 (保留 24h 历史)
- BAS 点位自动发现 (BACnet Who-Is → CIM 实体匹配)

**验收**: 真实 BAS 数据流入 CIM, step7 联邦查询仍然通过。

### M7: 多医院站点

**目标**: 从单院 (NBU) 扩展到多院区。

- Named Graph 按站点隔离: `graph/{site}/ifc`, `graph/{site}/bas/*`
- 站点级 ID 前缀: `NBU-AHU-001`, `ZJU-AHU-001`
- 跨站点联邦查询 (同类设备对标分析)
- TBox 共享, ABox 按站点独立

**验收**: 2+ 站点数据共存, 跨站查询可用。

## 中期

### 实时推送

- WebSocket/SSE 替代轮询, BAS 数据实时推送到前端
- 事件驱动架构: BAS 报警 → CIM 事件写入 → 前端推送 (< 3s 延迟)
- Named Graph `graph/event` 改为事件流 (Kafka/NATS)

### 3D 数字孪生

- Three.js + CIM 空间语义 (Room/Zone/Floor 定位)
- IFC 几何渲染 + BAS 实时状态叠加
- 点击设备 → SPARQL 查询全状态 (eq_full_status 模式)

### AI 预测维护

- 基于 CMMS 历史 (故障间隔 MTBF) + BAS 趋势 (功率/温度漂移)
- 机器学习模型: 输入 = CIM 设备特征 + BAS 时序, 输出 = 故障概率
- 自动生成预防性工单 (CMMS 回写)

## 长期

### CIM 标准化

- 向 Brick Schema 社区贡献医疗建筑扩展 (医气/洁净度/生命安全分级)
- 向 ASHRAE 223P 提交医疗 HVAC 连接点模式
- 发布 CIM 医疗建筑本体为独立开源项目

### 行业推广

- 从单院到区域医疗建筑群 (城市级)
- 从医疗建筑到其他关键设施 (数据中心、实验室、洁净厂房)
- CIM 作为数字孪生平台的领域语义层标准

### 技术深化

- 图数据库 (Neo4j/GraphDB) 替代文件级 RDF 存储
- 联邦学习: 多院区模型共享知识、不共享数据
- 自然语言查询: "5楼手术室空调什么状态" → 自动生成 SPARQL
