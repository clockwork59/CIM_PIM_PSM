# CIM 知识图谱 RAG 策略

## 核心问题

CIM 知识图谱有 61,941 个三元组, 序列化为 TTL 约 ~80,000 tokens。
没有任何 Agent 的上下文窗口应该容纳全部。如何按需检索？

## 检索策略对比

| 策略 | Token 成本 | 延迟 | 适用场景 |
|------|-----------|------|---------|
| 全量 TBox 加载 | ~15,000 | 高 | 初始建模 (需要完整类层次) |
| SPARQL 按需检索 | ~500-2,000 | 低 | 增量修改 (只查相关子图) |
| Named Graph 选择性加载 | ~3,000-8,000 | 中 | 跨源联邦 (选择性加载 2-3 图) |
| Memory 历史召回 | ~200-500 | 极低 | 重复任务 (复用历史经验) |
| CONSTRUCT 子图裁剪 | ~1,000-5,000 | 低 | Agent 特定视图 (定制子图) |

## 检索模式

### 模式 1: TBox 子图裁剪

Agent 只需要本体的一个子集。用 SPARQL CONSTRUCT 裁剪出精确子图:

```sparql
# 为 Agent-06 裁剪控制相关的类定义
CONSTRUCT {
  ?class rdfs:subClassOf ?parent .
  ?class rdfs:label ?label .
  ?class rdfs:comment ?desc .
}
WHERE {
  ?class rdfs:subClassOf* cim:Sensor .
  ?class rdfs:label ?label .
  OPTIONAL { ?class rdfs:comment ?desc }
}
```

从 545 个类中裁剪出约 80 个控制相关类, token 从 15,000 降到 ~2,500。

### 模式 2: ABox 实例检索

通过 SPARQL SELECT 获取具体实例数据:

```sparql
# Agent-08 查询过期维保工单
SELECT ?wo ?equipment ?dueDate ?status WHERE {
  GRAPH <graph/cmms> {
    ?wo a cim-cmms:WorkOrder ;
        cim-cmms:targetEquipment ?equipment ;
        cim-cmms:dueDate ?dueDate ;
        cim-cmms:status ?status .
    FILTER (?dueDate < NOW() && ?status != "COMPLETED")
  }
}
```

返回约 10-30 条记录, 而非加载全部 nbu_cmms_workorders.ttl (~4,000 三元组)。

### 模式 3: 跨图联合查询

Named Graph 允许选择性加载多个数据源:

```sparql
# MVP EventEngine: 联合 FAS + BAS + Event 三个图
SELECT ?detector ?reading ?event WHERE {
  GRAPH <graph/fas> {
    ?detector a cim-fas:SmokeDetector ;
              cim-space:locatedIn ?room .
  }
  GRAPH <graph/bas/t2> {
    ?reading cim-bas:monitoredBy ?detector ;
             cim-bas:value ?val .
    FILTER (?val > ?threshold)
  }
  OPTIONAL {
    GRAPH <graph/event> {
      ?event cim-event:triggeredBy ?detector .
    }
  }
}
```

只加载 3 个图 (FAS + BAS/t2 + Event), 跳过不相关的 CMMS 和 IFC 图。

### 模式 4: 验证结果反馈

SHACL/仿真结果作为上下文反馈给 Agent 进行自修复:

```
Agent-03 生成 equipment_hierarchy.ttl
  ↓
pyshacl 验证, 发现 3 个 SHACL violation
  ↓
违规报告注入 Agent-03 的上下文:
  "以下实例缺少必需属性 cim:hasTag:
   inst:AHU_01, inst:Pump_03, inst:Chiller_02"
  ↓
Agent-03 修复并重新生成
```

这形成了一个**上下文反馈回路**: 输出的验证结果成为下一轮的输入上下文。

### 模式 5: Memory 历史召回

从 `memory/` 检索历史经验, 避免重复错误:

```
memory/MEMORY.md 记录:
  - 审计反馈模式: 先原型后全量、数字必须实测、ID对照治理规范
  - 关键文件路径索引

当 Agent 执行类似任务时, 将相关记忆注入上下文:
  "历史经验: 生成 ABox 时, 数量必须来自实测 (rdflib count),
   不得基于估算。参考 H-001 修复报告。"
```

## 检索决策树

```
Agent 需要上下文?
  │
  ├── 需要本体结构? ──→ 是 ──→ TBox 变化了吗?
  │                              ├── 否 ──→ 使用缓存的 TBox 子集
  │                              └── 是 ──→ CONSTRUCT 重新裁剪
  │
  ├── 需要实例数据? ──→ 是 ──→ SPARQL SELECT 按需检索
  │
  ├── 需要跨源数据? ──→ 是 ──→ Named Graph 联合查询
  │
  ├── 需要验证反馈? ──→ 是 ──→ 加载最近的 SHACL 报告
  │
  └── 需要历史经验? ──→ 是 ──→ 从 memory/ 召回相关模式
```

## Token 预算控制

| 上下文组件 | 硬上限 | 超限策略 |
|-----------|--------|---------|
| TBox 子集 | 5,000 tokens | CONSTRUCT 进一步裁剪 |
| ABox 查询结果 | 3,000 tokens | LIMIT 子句 + 分页 |
| 验证报告 | 1,000 tokens | 只返回 violation, 不返回 pass |
| Memory | 500 tokens | 只召回最相关的 3 条 |
| 总计 | 15,000 tokens | 超出则降级为摘要模式 |
