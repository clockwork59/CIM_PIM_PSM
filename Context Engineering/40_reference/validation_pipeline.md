# 验证管线 (Validation Pipeline)

**文档 ID**: `CIMU-REF-04-验证管线`
**最后更新**: 2026-05-11

---

## 概述

CIM 项目采用 **12 步验证管线**，覆盖从 IFC 源数据到 MVP 端到端的全链路质量保证。
每一步均有明确的输入、工具、通过标准和输出。

---

## 12 步验证流程

| 步骤 | 名称 | 输入 | 工具/方法 | 通过标准 | 里程碑 |
|------|------|------|-----------|----------|--------|
| **Step 1** | IFC 模型检查 | IFC 文件 | IfcOpenShell + 自定义脚本 | 几何/属性完整 | M2 |
| **Step 2** | IFC 属性集验证 | IFC PSet | Python validator | 必选 PSet 齐全 | M2 |
| **Step 3** | IFC 空间层级验证 | IFC spatial | Python validator | Building→Floor→Room 完整 | M2 |
| **Step 4** | IFC 系统分类验证 | IFC system | Python validator | MEP 系统分类正确 | M2 |
| **Step 5** | IFC 关系验证 | IFC rel | Python validator | ContainedIn/ConnectedTo 完整 | M2 |
| **Step 6** | IFC→CIM ABox 转换 | IFC + TBox | 6 Python 转换脚本 | 1210 实例, 0 遗漏 | M2 |
| **Step 7** | pyshacl 全量验证 | ABox + SHACL | pyshacl | Conformance=True, 0 violations | M2 |
| **Step 8** | owl:Class 计数 | TBox 全部 TTL | rdflib + SPARQL | 545 classes | M1 |
| **Step 9** | 3源联邦 SPARQL | IFC+BAS+CMMS graphs | Apache Jena Fuseki | 5/5 queries pass | M3 |
| **Step 10** | 平台验证 | Named Graphs + API | Docker + REST API + SPARQL | 61941 triples, 10/10 queries | M4 |
| **Step 11** | API + 前端测试 | FastAPI + HTML | curl + browser | 所有端点 200, 前端渲染 | M5 |
| **Step 12** | MVP 端到端 | 仿真引擎 + 可视化 | event_engine + HTML platform | L2 fire, 10/10 actions, 840s < 900s | MVP |

---

## 验证工具链

```
IFC File
  |
  v
Step 1-5: IfcOpenShell + Python validators
  |
  v
Step 6: ifc_to_cim_converter.py (6 modules)
  |
  v
Step 7: pyshacl --shacl shacl_constraints.ttl
  |
  v
Step 8: rdflib SPARQL SELECT (COUNT ?class)
  |
  v
Step 9: Fuseki + federation SPARQL (3 Named Graphs)
  |
  v
Step 10: Docker compose + API integration test
  |
  v
Step 11: FastAPI endpoint test + frontend render
  |
  v
Step 12: SimClock + EventEngine + ActionChainExecutor
```

---

## 关键验证指标

| 指标 | 目标值 | 实测值 | 状态 |
|------|--------|--------|------|
| owl:Class 总数 | >= 500 | 545 | PASS |
| SHACL violations | 0 | 0 | PASS |
| ABox 实例数 | >= 1000 | 1210 | PASS |
| 三元组总数 | >= 50000 | 61941 | PASS |
| 联邦查询 | 5/5 | 5/5 | PASS |
| 平台 SPARQL | 10/10 | 10/10 | PASS |
| FAS 验证 | 28/28 | 28/28 | PASS |
| MVP 动作链 | 10/10 | 10/10 | PASS |
| MVP 处置时间 | < 900s | 840s | PASS |

---

## 相关文件

- SHACL 约束: `project_deliverables/version02/cim/rules/shacl_constraints.ttl`
- SPARQL 查询: `project_deliverables/version02/cim/rules/cross_agent_validation.sparql`
- 平台查询: `project_deliverables/version02/platform/queries/*.sparql`
- 仿真验证: `project_deliverables/version02/simulation/validators/`
