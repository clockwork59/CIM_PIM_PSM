## 🧑‍💻 User


我的问题是修订版是独立的文档还是需要和之前的文档合并使用？

---
## 🤖 Assistant


这是一个非常重要的问题。让我明确回答：

---

## 修订版文档的使用方式

### 结论：**混合使用** - 部分替换 + 部分新增

| 文档类型 | 处理方式 | 说明 |
|----------|----------|------|
| **替换型** | 用v2版本**完全替换**v1版本 | 内容已合并升级，v1可废弃 |
| **新增型** | v1版本中**不存在**，需添加 | 响应审核意见新增的文档 |
| **保留型** | v1版本**继续使用**，未修订 | 修订版未涉及的文档 |

---

## 具体文档对照表

### 🔄 替换型文档（用v2替换v1）

| v1文档 | v2文档 | 替换原因 |
|--------|--------|----------|
| `concept_extraction_report.json` | `concept_extraction_report_v2.json` | 增强了字段级源文档追踪 |
| `medical_domain_constraints.json` | `medical_domain_constraints_v2.json` | 补充了属性定义，与本体对齐 |
| `ontology_skeleton.ttl` | `ontology_skeleton_v2.ttl` | 增加了完整属性定义 |

### ➕ 新增型文档（v1不存在）

| 新增文档 | 用途 |
|----------|------|
| `cross_agent_gap_analysis.json` | 跨Agent映射空白分析与补充策略 |
| `source_file_audit.json` | 源文件存在性验证报告 |
| `validation_rules_schema.json` | 统一验证规则JSON Schema |

### ✅ 保留型文档（继续使用v1）

| v1文档 | 状态 |
|--------|------|
| `cim_document_structure.md` | 保留，未修订 |
| `task_manifest.json` | 保留，未修订 |
| `dependency_graph.json` | 保留，未修订 |
| `_config.json` | 保留，未修订 |
| `_index.ttl` | 保留，未修订 |

---

## 完整文档集合（合并后）

```
cim_deliverables/
├── concept_extraction_report_v2.json    # 替换v1
├── medical_domain_constraints_v2.json   # 替换v1
├── ontology_skeleton_v2.ttl             # 替换v1
├── cross_agent_gap_analysis.json        # 新增
├── source_file_audit.json               # 新增
├── validation_rules_schema.json         # 新增
├── cim_document_structure.md            # 保留v1
├── task_manifest.json                   # 保留v1
├── dependency_graph.json                # 保留v1
├── _config.json                         # 保留v1
└── _index.ttl                           # 保留v1
```

---

## 建议操作

1. **创建新目录** `v2/` 存放完整合并后的文档集
2. **废弃标记** 对v1中被替换的3个文档标记为 `DEPRECATED`
3. **版本号更新** 在 `_config.json` 中更新项目版本为 `0.3.0-Alpha`

---

**简短回答：修订版不是完全独立的，需要与v1文档合并使用。3个文档被替换，3个文档是新增，5个文档沿用v1版本。**

---