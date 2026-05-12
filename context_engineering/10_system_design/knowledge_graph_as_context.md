# 知识图谱作为上下文基础设施

## 核心观点

CIM 知识图谱不仅是数据存储, 更是 AI Agent 的**上下文基础设施**。
每个 Named Graph 是一个上下文分区, SPARQL 是上下文检索语言。

## CIM Named Graph = 上下文分区

9 个 Named Graph, 61,941 个三元组, 按语义域隔离:

| Named Graph | 三元组数 | 上下文用途 | 典型消费者 |
|-------------|---------|----------|-----------|
| `graph/tbox` | ~12,000 | Agent 推理的领域语义 (545 owl:Class) | 所有 Agent |
| `graph/ifc` | ~8,000 | 静态 BIM 实体: 空间/设备/系统 | Agent-01/02/03 |
| `graph/bas/t0` | ~6,000 | BAS 基线读数 (正常态) | Agent-06/07 |
| `graph/bas/t1` | ~6,000 | BAS 快照 (异常态) | Agent-06/07 |
| `graph/bas/t2` | ~6,000 | BAS 快照 (告警态) | Agent-06/07/MVP |
| `graph/cmms` | ~4,000 | 维保历史: 工单/故障/维修 | Agent-08 |
| `graph/fas` | ~5,000 | FAS 设备拓扑: 62 探测器/控制器 | MVP EventEngine |
| `graph/event` | ~3,000 | 安全事件状态: 26 类 SecurityEvent | MVP 态势中心 |
| `graph/pset` | ~5,941 | PropertySet 扩展属性 | Agent-03/05 |

### 上下文隔离原则

每个 Agent 只加载它需要的 Named Graph:

```
Agent-06 (Control) 需要:
  graph/tbox          -> 控制策略类定义
  graph/bas/t0        -> 正常基线对比
  graph/bas/t1 或 t2  -> 当前运行状态

Agent-06 不需要:
  graph/cmms          -> 维保历史 (与控制无关)
  graph/event         -> 安全事件 (由 MVP 消费)
```

上下文隔离减少 token 消耗, 同时降低 Agent 被无关信息干扰的风险。

## SPARQL 作为上下文检索

不是 "全量加载 TTL", 而是 "按需 SPARQL 检索":

### 示例: Agent-03 检索某楼层的所有设备

```sparql
PREFIX cim-d: <urn:cim:design:>
PREFIX cim-space: <urn:cim:space:>
PREFIX inst: <urn:cim:instance:>

SELECT ?equip ?type ?tag WHERE {
  ?equip a ?type ;
         cim-d:designTag ?tag .
  ?equip cim-space:locatedIn ?room .
  ?room cim-space:isPartOf inst:Floor_5F .
}
```

返回约 50 行, 替代加载整个 ABox (数千行) -- **token 节省 99%**。

### 示例: MVP EventEngine 扫描当前告警

```sparql
PREFIX cim-event: <urn:cim:event:>

SELECT ?event ?severity ?location ?timestamp WHERE {
  GRAPH <graph/event> {
    ?event a cim-event:SecurityEvent ;
           cim-event:severity ?severity ;
           cim-event:location ?location ;
           cim-event:timestamp ?timestamp .
    FILTER (?severity IN ("CRITICAL", "HIGH"))
  }
}
ORDER BY DESC(?timestamp)
LIMIT 20
```

返回 20 条高优先级事件 -- MVP 态势中心只需要这些, 不需要全部事件历史。

## 上下文服务架构

```
┌─────────────────────────────────────────────────┐
│                  Agent Runtime                    │
│                                                   │
│  Agent-03: "给我 5F 的设备"                       │
│       │                                           │
│       ▼                                           │
│  SPARQL Endpoint ──→ Named Graph Router           │
│       │                    │                      │
│       │     ┌──────────────┼──────────────┐       │
│       ▼     ▼              ▼              ▼       │
│   graph/tbox  graph/ifc  graph/bas/*  graph/fas   │
│                                                   │
│  返回: 裁剪后的子图 (~500 tokens)                  │
│  而非: 全量 ABox (~15,000 tokens)                  │
└─────────────────────────────────────────────────┘
```

## 上下文缓存策略

| 上下文类型 | 变化频率 | 缓存策略 |
|-----------|---------|---------|
| TBox (本体结构) | 低 (按版本发布) | 长期缓存, 版本号失效 |
| IFC 静态数据 | 极低 (建筑不变) | 持久缓存 |
| BAS 运行数据 | 高 (3 快照/天) | 短期缓存, t0/t1/t2 轮换 |
| CMMS 维保数据 | 中 (月度更新) | 中期缓存, 月度刷新 |
| 安全事件 | 实时 | 不缓存, 每次查询 |

## 与 FastAPI 端点的关系

6 个 REST 端点将 SPARQL 检索封装为 HTTP 服务:

| 端点 | 返回的上下文 | 消费者 |
|------|------------|--------|
| `/api/equipment/{floor}` | 楼层设备列表 | Agent-03, 可视化 |
| `/api/topology/{system}` | 系统拓扑子图 | Agent-01/04 |
| `/api/alerts/active` | 当前活跃告警 | MVP EventEngine |
| `/api/validation/report` | SHACL 验证结果 | Agent-09 |
| `/api/sparql` | 任意 SPARQL 查询 | 所有 Agent |
| `/api/graph/{name}` | 指定 Named Graph | 按需加载 |

这些端点本质上是**上下文服务 API** -- 将知识图谱的检索能力暴露给 Agent 运行时。
