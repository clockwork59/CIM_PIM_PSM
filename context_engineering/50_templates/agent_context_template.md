# Agent 上下文契约模板

## 使用说明

每个 CIM Agent 必须定义自己的上下文契约。本模板是标准格式。
复制此模板, 填充具体 Agent 的信息。

## 模板

```yaml
# ============================================================
# Agent 上下文契约
# ============================================================

agent_id: Agent-XX
agent_name: [中文名称]
agent_role: [一句话职责描述]

# ------------------------------------------------------------
# 输入上下文 (Agent 在推理时接收的信息)
# ------------------------------------------------------------
context_input:
  required:
    - source: "[文件路径, 例: ontology/layer2_reference.ttl]"
      subset: "[需要的子集描述, 例: PART D -- 设备类扩展]"
      retrieval: "[file | sparql_select | sparql_construct | named_graph]"
      token_budget: 3000
      cache_ttl: "[long | medium | short | none]"

    - source: "[上游 Agent 输出, 例: Agent-01 → topology/system_topology.ttl]"
      subset: "[需要的子集]"
      retrieval: "sparql_select"
      token_budget: 2000
      cache_ttl: "short"

  optional:
    - source: "[可选上下文源]"
      subset: "[子集]"
      retrieval: "file"
      token_budget: 1500
      fallback: "[缺失时的替代策略, 例: 使用默认映射表]"

  memory:
    - source: "memory/MEMORY.md"
      subset: "[相关历史经验]"
      token_budget: 500

# ------------------------------------------------------------
# 工具 (Agent 可调用的工具)
# ------------------------------------------------------------
tools:
  - name: "sparql_query"
    description: "查询 Named Graph"
    endpoint: "/api/sparql"
  - name: "pyshacl_validate"
    description: "SHACL 形状验证"
    input: "[输出文件] against rules/shacl_constraints.ttl"
  # 按需添加更多工具

# ------------------------------------------------------------
# 输出上下文 (Agent 产生的信息)
# ------------------------------------------------------------
context_output:
  files:
    - path: "[输出文件路径, 例: equipment/mechanical.ttl]"
      format: "Turtle (RDF)"
      description: "[文件内容描述]"
    - path: "[第二个输出文件]"
      format: "[YAML | JSON | TTL | MD]"
      description: "[描述]"

  named_graph:
    target: "[输出加载到哪个 Named Graph, 例: graph/equipment]"

  handoff_to:
    - agent: "Agent-XX"
      what: "[传递什么信息]"
      how: "[file | named_graph | sparql]"

# ------------------------------------------------------------
# 质量门 (Quality Gate)
# ------------------------------------------------------------
quality_gate:
  shacl_violation: 0
  orphan_instances: 0
  # Agent 特定的质量指标:
  # - Agent-01: system_connectivity (所有系统连通)
  # - Agent-03: brick_alignment >= 90%
  # - Agent-06: control_loop_completeness (sensor+actuator+setpoint)
  # - Agent-09: 12_step_pipeline ALL PASS
  custom_metric_1: "[指标名]: [目标值]"

# ------------------------------------------------------------
# 上下文预算总结
# ------------------------------------------------------------
budget_summary:
  total_input_tokens: "[required + optional + memory 的总和]"
  total_output_tokens: "[输出文件的预估 token 数]"
  context_efficiency: "[相关 token / 总 token 的比率]"
```

## 填写指南

### source 字段

引用实际项目文件路径, 基于 `project_deliverables/version02/cim/`:

| 资产类型 | 路径模式 |
|---------|---------|
| TBox 本体 | `ontology/layer{0-4}_*.ttl`, `ontology/bridge/bridge_*.ttl` |
| ABox 实例 | `abox/nbu_*.ttl` |
| 验证规则 | `rules/shacl_constraints.ttl`, `rules/cross_agent_validation.sparql` |
| 元数据 | `data_dictionary.yaml`, `global_id_registry.yaml` |
| 上游 Agent | `Agent-XX → [该 Agent 的输出文件]` |

### retrieval 字段

| 方法 | 何时使用 | Token 效率 |
|------|---------|-----------|
| `file` | 小文件或需要完整内容 | 低 (全量加载) |
| `sparql_select` | 从大文件中检索少量记录 | 高 |
| `sparql_construct` | 需要裁剪本体子图 | 高 |
| `named_graph` | 加载整个语义分区 | 中 |

### cache_ttl 字段

| 值 | 含义 | 适用于 |
|----|------|--------|
| `long` | 版本级缓存 (TBox 不变就不刷新) | 本体结构 |
| `medium` | 月度刷新 | CMMS, 维保数据 |
| `short` | 每次查询刷新 | BAS 运行数据, 事件 |
| `none` | 不缓存 | 实时告警, 安全事件 |
