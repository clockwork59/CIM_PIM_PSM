# 上下文质量度量

## 度量维度

| 维度 | 指标 | CIM 项目实测 | 度量方法 |
|------|------|------------|---------|
| **相关性** | 上下文中与任务相关的 token 占比 | ~70% (TBox 裁剪后) vs ~15% (全量加载) | 人工抽样 + Agent 输出质量对比 |
| **完整性** | 任务所需信息的覆盖率 | 100% (545 类全覆盖 BIM 实体) | `cross_agent_validation.sparql` 覆盖率查询 |
| **准确性** | 上下文中事实的正确率 | SHACL VIOLATION=0, pyshacl 4 文件实测 | `pyshacl` 自动验证 |
| **时效性** | 上下文数据的新鲜度 | BAS 3 快照/天 (t0/t1/t2), CMMS 月度更新 | 时间戳比对 |
| **效率** | token 利用率 (信息密度) | SPARQL 检索 vs 全量: 99% token 节省 | token 计数对比 |
| **一致性** | 跨 Agent 上下文的语义一致 | 9 Named Graph 无交叉污染 | Named Graph 隔离验证 |

## 验证管线作为上下文质量保证

12-step validation pipeline 本质上是上下文质量的端到端验证。
每一步验证的不仅是数据正确性, 更是**该步骤的上下文是否充分且准确**:

| Step | 验证内容 | 验证的上下文质量 |
|------|---------|----------------|
| step1 | IFC 文件解析 | 源数据可读性 (上下文可加载) |
| step2 | IFC 实体提取 | 源数据完整性 (无遗漏) |
| step3 | CIM 类映射 | 映射上下文的正确性 (bridge_*.ttl) |
| step4 | ID 生成与注册 | ID 上下文的唯一性 (global_id_registry) |
| step5 | 属性转换 | 属性字典上下文的覆盖率 (data_dictionary.yaml) |
| step6 | ABox 生成 | 生成上下文的一致性 (TBox-ABox 对齐) |
| step7 | SHACL 验证 | 形式化语义上下文的正确性 |
| step8 | 类计数审计 | 实测数据的准确性 (**反对估算**) |
| step9 | 三源联邦 | 跨上下文一致性 (IFC+BAS+CMMS) |
| step10 | Named Graph 加载 | 上下文分区的隔离性 (9 图无泄漏) |
| step11 | API 端点测试 | 上下文服务可用性 (6 REST 端点) |
| step12 | MVP 端到端 | 完整上下文链路 (L2 火灾 10 节点) |

## 上下文质量计分卡

### Agent 级评分

```
Agent-03 上下文质量评分:

  相关性: 8/10
    ✓ layer2_reference.ttl 裁剪为设备子集
    △ bridge_brick.ttl 中有 ~30% 非设备映射 (噪声)

  完整性: 10/10
    ✓ 120 设备类全覆盖
    ✓ 5 个设备大类: HVAC/Electrical/Plumbing/MedicalGas/FireProtection

  准确性: 10/10
    ✓ pyshacl 验证 equipment_hierarchy.ttl: 0 violation
    ✓ pyshacl 验证 mechanical.ttl: 0 violation

  时效性: 9/10
    ✓ TBox 基于最新 _index_v4.ttl
    △ IFC 设备清单未自动同步

  效率: 7/10
    ✓ SPARQL 检索替代全量加载
    △ 部分 Agent 仍使用文件传递 (可优化)

  总分: 44/50
```

### 系统级评分

| 指标 | 目标 | 实测 | 状态 |
|------|------|------|------|
| SHACL violation | 0 | 0 | PASS |
| 跨 Agent 引用完整性 | 100% | 100% | PASS |
| Named Graph 隔离 | 无泄漏 | 无泄漏 | PASS |
| 三元组总数 | > 50,000 | 61,941 | PASS |
| owl:Class 总数 | > 500 | 545 | PASS |
| MVP 端到端 | 10 节点通过 | 10 节点通过 | PASS |
| token 效率 (SPARQL vs 全量) | > 90% 节省 | 99% 节省 | PASS |

## 上下文退化检测

上下文质量会随时间退化。以下是检测信号:

| 退化信号 | 检测方法 | 修复动作 |
|---------|---------|---------|
| Agent 输出 SHACL violation 增加 | pyshacl 自动验证 | 检查 TBox 是否更新但 Agent 上下文未同步 |
| Agent 产生幻觉实体 | ABox 实例 vs TBox 类交叉验证 | 检查上下文是否缺少新增的类定义 |
| SPARQL 查询返回空 | 端点健康检查 | 检查 Named Graph 是否加载 |
| 跨 Agent 引用断裂 | cross_agent_validation.sparql | 检查上游 Agent 是否更新了 ID |
| MVP 事件链中断 | step12 端到端测试 | 检查 EventEngine 的上下文是否包含最新事件类 |

## 上下文质量改进周期

```
1. 度量 (Measure)
   运行 12-step pipeline, 记录每步结果

2. 诊断 (Diagnose)
   失败步骤 → 追溯到哪个 Agent 的上下文有问题

3. 修复 (Fix)
   调整上下文契约 (token 预算/源文件/裁剪策略)

4. 验证 (Verify)
   重新运行 pipeline, 确认修复有效

5. 固化 (Codify)
   更新 Agent 上下文契约 + memory/ 记录修复模式
```

这是一个持续改进循环, 不是一次性配置。上下文工程是运维活动, 不是设计活动。
