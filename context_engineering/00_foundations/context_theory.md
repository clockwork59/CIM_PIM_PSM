# Context Engineering 理论基础

## 1. 上下文的定义

上下文 (Context) 不等于 提示词 (Prompt)。上下文是 AI Agent 在推理时接收的**完整信息负载**。

提示词是上下文的一个子集。上下文还包括系统指令、工具定义、检索结果、记忆、
对话历史等一切影响 Agent 输出的信息。

### CIM 项目中的上下文组件

| 上下文组件 | CIM 项目中的实现 | Token 预算 |
|-----------|----------------|-----------|
| 系统提示 (System Prompt) | `CLAUDE.md` (项目规范 + 9-Agent 架构) | ~2,000 |
| 领域知识 (Domain Knowledge) | TBox TTL 片段 (按需从 15 个 TTL 文件加载) | ~5,000-15,000 |
| 实例数据 (Instance Data) | ABox SPARQL 查询结果 (从 9 个 ABox 文件检索) | ~2,000-8,000 |
| 少样本示例 (Few-shot Examples) | 已验证的建模模式 (手术室、FAS 等) | ~1,000-3,000 |
| 工具定义 (Tool Definitions) | SPARQL 端点 / pyshacl / rdflib 接口 | ~500-1,000 |
| 记忆 (Memory) | `memory/` 持久化 + `MEMORY.md` 会话状态 | ~500-2,000 |
| 约束 (Constraints) | `shacl_constraints.ttl` + 治理规范 | ~1,000 |

**总预算**: 单次 Agent 调用约 12,000-32,000 tokens 的上下文窗口。

## 2. 上下文质量公式

```
Q(C) = Relevance(C) * Completeness(C) * Efficiency(C)
```

- **Relevance (相关性)**: 上下文中有多少与当前任务相关？无关信息 = 噪声。
  - 实测: TBox 裁剪后相关性 ~70%, 全量加载仅 ~15%
- **Completeness (完整性)**: 任务所需的信息是否都在上下文中？缺失 = 盲区。
  - 实测: 545 owl:Class 覆盖全部 BIM 实体类型
- **Efficiency (效率)**: 用了多少 token 传递了多少信息？token ROI。
  - 实测: SPARQL 按需检索 vs 全量加载, token 节省 99%

### 反模式

| 反模式 | 症状 | CIM 项目中的表现 |
|--------|------|-----------------|
| 上下文过载 | Agent 忽略关键信息 | 加载全部 15 个 TBox 文件给 Agent-06 (它只需要 control_strategies) |
| 上下文饥饿 | Agent 产生幻觉 | 不提供 bridge_brick.ttl, Agent-03 自行编造 Brick 映射 |
| 上下文过时 | Agent 基于旧数据决策 | 使用 t0 时刻的 BAS 读数, 但系统已进入 t2 告警状态 |
| 上下文冲突 | Agent 输出自相矛盾 | TBox 定义 cim:Chiller 但 ABox 使用 cim:ColdWaterUnit |

## 3. CIM 项目的上下文层级

```
Level 0: 项目元数据
  ├── CLAUDE.md (项目规范)
  ├── memory/MEMORY.md (会话状态: M1-M5✅ MVP✅)
  └── plans/项目总控计划.md (里程碑)

Level 1: 本体框架
  ├── _index_v4.ttl (导入链, 17 命名空间)
  ├── layer0_foundational.ttl (基础概念)
  └── layer1_conceptual.ttl (介质/连接点)

Level 2: 领域子图 (按任务裁剪的 TBox 子集)
  ├── layer2_reference.ttl (设备参考类)
  ├── layer3_design.ttl (设计态属性)
  ├── layer4_operational.ttl (运行态属性)
  ├── layer4_fas_security.ttl (FAS 安防)
  ├── layer4_cmms.ttl (维保)
  └── layer4_control_strategies.ttl (控制策略)

Level 3: 实例数据 (SPARQL 查询结果)
  ├── nbu_medical_clinic_instances.ttl (诊所设备实例)
  ├── nbu_fas_instances.ttl (62 个 FAS 探测器)
  ├── nbu_bas_readings_t0/t1/t2.ttl (BAS 快照)
  ├── nbu_cmms_workorders.ttl (维保工单)
  └── nbu_security_events.ttl (安全事件)

Level 4: 验证反馈
  ├── shacl_constraints.ttl (SHACL 形状)
  ├── cross_agent_validation.sparql (5 个验证查询)
  └── 12-step validation pipeline 结果

Level 5: 历史经验
  ├── memory/ 审计修复模式
  └── H-001 等修复报告 (先原型后全量原则)
```

## 4. 上下文 vs 微调 vs RAG

| 方法 | 延迟 | 适用场景 | CIM 项目应用 |
|------|------|---------|-------------|
| 上下文工程 | 即时 | 任务特定的信息注入 | Agent 每次调用的 TBox 子集 |
| RAG | 毫秒级 | 大规模知识库检索 | SPARQL 从 61,941 三元组中检索 |
| 微调 | 小时级 | 持久化领域知识 | 不适用 (本体变化频繁) |

对于 CIM 项目, **上下文工程 + SPARQL-RAG** 是最优组合:
- 本体结构通过上下文注入 (变化少, 结构固定)
- 实例数据通过 SPARQL 检索 (变化多, 按需获取)

## 5. Token 经济学

545 owl:Class 全量序列化约 ~45,000 tokens。没有 Agent 需要全部 545 个类。

| Agent | 需要的类子集 | 估计 Token | 占全量的比例 |
|-------|------------|-----------|------------|
| Agent-01 (Topology) | 系统类 + 连接点 (~60 类) | ~5,000 | 11% |
| Agent-03 (Equipment) | 设备层次 (~120 类) | ~10,000 | 22% |
| Agent-06 (Control) | 传感器 + 控制策略 (~80 类) | ~7,000 | 16% |
| Agent-09 (Integration) | 全量 (验证用) | ~45,000 | 100% |

只有 Agent-09 需要全量上下文, 其余 Agent 的上下文裁剪可节省 78-89% 的 token。
