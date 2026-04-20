# 数据字典生成说明

- 目的：将 Excel 工作簿的每个工作表拆分为独立的 Markdown 文档，存放于本目录。
- 脚本：`xlsx_to_md.py`（纯标准库解析 .xlsx，无需第三方依赖）

## 使用

```
python3 "docs/concept/data dictionary/xlsx_to_md.py" \
  "/Volumes/M4-SSD/项目 Project/项目 Project/A 工作项目/A 10 研发与产品项目/CIM-PIM-PSM/统一领域模型（CIM）/docs/concept/副本JHPDL规范 20251201.xlsx" \
  "/Volumes/M4-SSD/项目 Project/项目 Project/A 工作项目/A 10 研发与产品项目/CIM-PIM-PSM/统一领域模型（CIM）/docs/concept/data dictionary"
```

- 生成：每个工作表对应一个 `# <工作表名>` 的 Markdown 文件，首行作为表头。
- 命名：自动清洗非法文件名字符（如 `/ \ : * ? " < > |`）。
- 兼容：共享字符串、内嵌字符串、布尔、数值，保留原单元格顺序与空列。

## 注意
- 日期/数值的样式不在 Markdown 中渲染（保持原值）。
- 若工作表为空，将生成 `> (empty sheet)` 标记。
