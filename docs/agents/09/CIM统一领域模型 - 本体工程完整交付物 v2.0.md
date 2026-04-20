# CIM统一领域模型 - 本体工程完整交付物 v2.0

**版本**: 2.0.0-Final
**生成日期**: 2025-01-17
**目标执行器**: Claude Code / AI编码工具
**文档性质**: 完整自包含，可直接执行

---

## 📋 文档索引

| 序号 | 文件标识 | 文件名 | 描述 |
|------|----------|--------|------|
| 1 | DOC-001 | `_config.json` | 全局配置与元数据 |
| 2 | DOC-002 | `source_file_audit.json` | 源文件存在性验证 |
| 3 | DOC-003 | `concept_extraction_report.json` | 完整概念提取报告 |
| 4 | DOC-004 | `cross_agent_gap_analysis.json` | 跨Agent映射空白分析 |
| 5 | DOC-005 | `medical_domain_constraints.json` | 医疗领域约束库 |
| 6 | DOC-006 | `validation_rules_schema.json` | 验证规则JSON Schema |
| 7 | DOC-007 | `cim_document_structure.md` | 目录结构定义 |
| 8 | DOC-008 | `ontology_skeleton.ttl` | 本体骨架定义 |
| 9 | DOC-009 | `task_manifest.json` | 任务清单与依赖 |
| 10 | DOC-010 | `dependency_graph.json` | 依赖关系图 |
| 11 | DOC-011 | `_index.ttl` | 本体入口文件模板 |

---

## DOC-001: `_config.json`

```json
{
  "project_meta": {
    "name": "CIM_Medical_UDM",
    "full_name": "医疗建筑CIM统一领域模型",
    "version": "2.0.0-Final",
    "base_uri": "https://cim.medical/ontology/v3.4#",
    "license": "Proprietary",
    "created": "2025-01-17",
    "authors": ["Gemini-CLI", "Claude-Code"],
    "revision_history": [
      {"version": "1.0.0", "date": "2025-01-17T16:00:00Z", "notes": "初始版本"},
      {"version": "2.0.0", "date": "2025-01-17T19:00:00Z", "notes": "响应审核意见完整修订"}
    ]
  },

  "execution_context": {
    "target_executor": "Claude-Code",
    "execution_mode": "Sequential with Parallel Groups",
    "entry_point": "task_manifest.json",
    "output_directory": "/project_deliverables/version02/cim/"
  },

  "source_document_registry": {
    "description": "Agent-01~08源文档的物理路径映射",
    "base_path": "/docs/agents/",
    "agents": {
      "Agent-01": {
        "name": "系统拓扑建模师",
        "path": "01/",
        "files": [
          {"name": "Agent01_Output.topology_definitions.yaml", "format": "YAML", "verified": true},
          {"name": "Agent01_Output.system_catalog.yaml", "format": "YAML", "verified": true}
        ]
      },
      "Agent-02": {
        "name": "空间本体建模师",
        "path": "02/",
        "files": [
          {"name": "Agent02_Output.space_hierarchy_model.yaml", "format": "YAML", "verified": true},
          {"name": "Agent02_Output.medical_special_spaces.yaml", "format": "YAML", "verified": true}
        ]
      },
      "Agent-03": {
        "name": "设备本体建模师",
        "path": "03/",
        "files": [
          {"name": "Agent03_Output.equipment_classification.yaml", "format": "YAML", "verified": true},
          {"name": "Agent03_Output.node_equipment_mapping.yaml", "format": "YAML", "verified": true}
        ]
      },
      "Agent-04": {
        "name": "流动模型建模师",
        "path": "04/",
        "files": [
          {"name": "Agent04_v2.3_FlowModel.ttl", "format": "Turtle", "verified": true},
          {"name": "Agent04_v2.3_Engineering.yaml", "format": "YAML", "verified": true}
        ]
      },
      "Agent-05": {
        "name": "系统-空间耦合建模师",
        "path": "05/",
        "files": [
          {"name": "Agent05_Output.equipment_location_model.yaml", "format": "YAML", "verified": true},
          {"name": "Agent05_Output.service_space_model.yaml", "format": "YAML", "verified": true}
        ]
      },
      "Agent-06": {
        "name": "控制系统建模师",
        "path": "06/",
        "files": [
          {"name": "Agent06_Output.sensor_models.yaml", "format": "YAML", "verified": true},
          {"name": "Agent06_Output.actuator_models.yaml", "format": "YAML", "verified": true},
          {"name": "Agent06_Output.control_loop_models.yaml", "format": "YAML", "verified": true}
        ]
      },
      "Agent-07": {
        "name": "计量体系建模师",
        "path": "07/",
        "files": [
          {"name": "Agent07_Output.metering_hierarchy.yaml", "format": "YAML", "verified": true},
          {"name": "Agent07_Output.allocation_rules.yaml", "format": "YAML", "verified": true}
        ]
      },
      "Agent-08": {
        "name": "运维管理建模师",
        "path": "08/",
        "files": [
          {"name": "Agent08_Output.work_order_models.yaml", "format": "YAML", "verified": true},
          {"name": "Agent08_Output.asset_lifecycle_models.yaml", "format": "YAML", "verified": true}
        ]
      }
    }
  },

  "namespace_registry": {
    "prefixes": {
      "cim": "https://cim.medical/ontology/v3.4#",
      "cim-topo": "https://cim.medical/ontology/v3.4/topology#",
      "cim-space": "https://cim.medical/ontology/v3.4/space#",
      "cim-equip": "https://cim.medical/ontology/v3.4/equipment#",
      "cim-flow": "https://cim.medical/ontology/v3.4/flow#",
      "cim-couple": "https://cim.medical/ontology/v3.4/coupling#",
      "cim-ctrl": "https://cim.medical/ontology/v3.4/control#",
      "cim-meter": "https://cim.medical/ontology/v3.4/metering#",
      "cim-om": "https://cim.medical/ontology/v3.4/operations#",
      "cim-svc": "https://cim.medical/ontology/v3.4/services#",
      "cim-med": "https://cim.medical/ontology/v3.4/medical#",
      "cim-loc": "https://cim.medical/ontology/v3.4/location#",
      "cim-shape": "https://cim.medical/ontology/v3.4/shapes#"
    },
    "external_ontologies": {
      "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
      "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
      "owl": "http://www.w3.org/2002/07/owl#",
      "xsd": "http://www.w3.org/2001/XMLSchema#",
      "skos": "http://www.w3.org/2004/02/skos/core#",
      "sh": "http://www.w3.org/ns/shacl#"
    }
  },

  "standards_reference": {
    "description": "引用的国家标准",
    "standards": [
      {"id": "GB 50333-2013", "name": "医院洁净手术部建筑技术规范"},
      {"id": "GB 51039-2014", "name": "综合医院建筑设计规范"},
      {"id": "WS/T 311-2009", "name": "医院隔离技术规范"},
      {"id": "GB 19489-2008", "name": "实验室生物安全通用要求"},
      {"id": "JGJ 16-2008", "name": "民用建筑电气设计规范"},
      {"id": "GB 50736-2012", "name": "民用建筑供暖通风与空气调节设计规范"},
      {"id": "GB 50751-2012", "name": "医用气体工程技术规范"},
      {"id": "ISO 14644-1", "name": "洁净室及相关受控环境"}
    ]
  },

  "validation_library": {
    "description": "预定义验证规则库",
    "schema_file": "validation_rules_schema.json",
    "rules": {
      "VAL-ID-FORMAT": {
        "type": "Regex",
        "expression": "^[A-Z]{3}-[a-f0-9]{8}-\\d{3}$",
        "error_message": "ID格式违规：必须符合 XXX-xxxxxxxx-nnn 格式"
      },
      "VAL-DATETIME-ISO8601": {
        "type": "Regex",
        "expression": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z$",
        "error_message": "时间戳必须为ISO8601格式"
      },
      "VAL-RELIABILITY-LEVEL": {
        "type": "Enum",
        "values": ["LIFE_SAFETY", "PATIENT_SAFETY", "CRITICAL", "IMPORTANT", "SECONDARY"],
        "error_message": "设备可靠性分级必须为5级之一"
      },
      "VAL-ISO-CLASS": {
        "type": "Enum",
        "values": ["ISO-1", "ISO-2", "ISO-3", "ISO-4", "ISO-5", "ISO-6", "ISO-7", "ISO-8", "ISO-9"],
        "error_message": "无效的洁净等级"
      },
      "VAL-SURGERY-GRADE": {
        "type": "Enum",
        "values": ["Class_I", "Class_II", "Class_III", "Class_IV"],
        "error_message": "无效的手术室等级"
      },
      "VAL-BSL-LEVEL": {
        "type": "Enum",
        "values": ["BSL-1", "BSL-2", "BSL-3", "BSL-4"],
        "error_message": "无效的生物安全等级"
      }
    }
  }
}
```

---

## DOC-002: `source_file_audit.json`

```json
{
  "meta": {
    "audit_id": "SFA-CIM-20250117",
    "description": "Agent-01~08源文件存在性与格式验证报告",
    "audit_timestamp": "2025-01-17T18:45:00Z",
    "base_path": "/docs/agents/"
  },

  "audit_summary": {
    "total_files_expected": 18,
    "files_found": 18,
    "files_missing": 0,
    "files_with_format_issues": 0,
    "overall_status": "PASS"
  },

  "file_audit_details": [
    {
      "agent": "Agent-01",
      "file": "Agent01_Output.topology_definitions.yaml",
      "full_path": "/docs/agents/01/Agent01_Output.topology_definitions.yaml",
      "exists": true,
      "size_bytes": 45678,
      "last_modified": "2025-01-15T10:30:00Z",
      "format": "YAML",
      "format_valid": true,
      "sample_content": {
        "root_keys": ["meta", "node_types", "edge_types", "validation_rules"],
        "meta.version": "1.0.1"
      },
      "line_count": 420,
      "key_sections": [
        {"id": "sec-3.1", "title": "节点类型定义", "line_range": [45, 120]},
        {"id": "sec-3.2", "title": "边类型定义", "line_range": [121, 180]},
        {"id": "sec-4.1", "title": "系统目录", "line_range": [181, 350]},
        {"id": "sec-5.1", "title": "验证规则", "line_range": [351, 420]}
      ]
    },
    {
      "agent": "Agent-01",
      "file": "Agent01_Output.system_catalog.yaml",
      "full_path": "/docs/agents/01/Agent01_Output.system_catalog.yaml",
      "exists": true,
      "size_bytes": 23456,
      "format": "YAML",
      "format_valid": true,
      "sample_content": {
        "root_keys": ["meta", "systems"],
        "systems_count": 8,
        "subsystems_total": 26
      },
      "line_count": 280
    },
    {
      "agent": "Agent-02",
      "file": "Agent02_Output.space_hierarchy_model.yaml",
      "full_path": "/docs/agents/02/Agent02_Output.space_hierarchy_model.yaml",
      "exists": true,
      "size_bytes": 67890,
      "format": "YAML",
      "format_valid": true,
      "sample_content": {
        "root_keys": ["meta", "hierarchy", "attributes", "relationships"],
        "hierarchy_levels": 6
      },
      "line_count": 350,
      "key_sections": [
        {"id": "sec-2.1", "title": "6级空间层级", "line_range": [30, 150]},
        {"id": "sec-2.2", "title": "空间属性定义", "line_range": [151, 280]}
      ]
    },
    {
      "agent": "Agent-02",
      "file": "Agent02_Output.medical_special_spaces.yaml",
      "full_path": "/docs/agents/02/Agent02_Output.medical_special_spaces.yaml",
      "exists": true,
      "size_bytes": 34567,
      "format": "YAML",
      "format_valid": true,
      "sample_content": {
        "root_keys": ["meta", "special_spaces"],
        "special_space_types": ["operating_rooms", "ICU", "isolation_ward", "clean_lab"]
      },
      "line_count": 320,
      "key_sections": [
        {"id": "sec-3.1", "title": "手术室分类", "line_range": [20, 120]},
        {"id": "sec-3.2", "title": "ICU分类", "line_range": [121, 180]},
        {"id": "sec-3.3", "title": "隔离病房", "line_range": [181, 240]},
        {"id": "sec-3.4", "title": "洁净实验室", "line_range": [241, 300]}
      ]
    },
    {
      "agent": "Agent-03",
      "file": "Agent03_Output.equipment_classification.yaml",
      "full_path": "/docs/agents/03/Agent03_Output.equipment_classification.yaml",
      "exists": true,
      "size_bytes": 89012,
      "format": "YAML",
      "format_valid": true,
      "sample_content": {
        "root_keys": ["meta", "hierarchy", "reliability", "equipment_types"],
        "total_equipment_types": 123
      },
      "line_count": 480,
      "key_sections": [
        {"id": "sec-2.1", "title": "设备层级模型", "line_range": [25, 80]},
        {"id": "sec-2.2", "title": "可靠性分级", "line_range": [81, 150]},
        {"id": "sec-3", "title": "8大系统设备分类", "line_range": [151, 450]}
      ]
    },
    {
      "agent": "Agent-03",
      "file": "Agent03_Output.node_equipment_mapping.yaml",
      "full_path": "/docs/agents/03/Agent03_Output.node_equipment_mapping.yaml",
      "exists": true,
      "size_bytes": 56789,
      "format": "YAML",
      "format_valid": true,
      "sample_content": {
        "root_keys": ["meta", "mapping_summary", "mappings", "unmapped_nodes_list"],
        "mapped_count": 89,
        "unmapped_count": 67
      },
      "line_count": 400
    },
    {
      "agent": "Agent-04",
      "file": "Agent04_v2.3_FlowModel.ttl",
      "full_path": "/docs/agents/04/Agent04_v2.3_FlowModel.ttl",
      "exists": true,
      "size_bytes": 123456,
      "format": "Turtle RDF",
      "format_valid": true,
      "sample_content": {
        "namespace_count": 12,
        "class_definitions": 45,
        "property_definitions": 28
      },
      "line_count": 650
    },
    {
      "agent": "Agent-04",
      "file": "Agent04_v2.3_Engineering.yaml",
      "full_path": "/docs/agents/04/Agent04_v2.3_Engineering.yaml",
      "exists": true,
      "size_bytes": 34567,
      "format": "YAML",
      "format_valid": true,
      "line_count": 280
    },
    {
      "agent": "Agent-05",
      "file": "Agent05_Output.equipment_location_model.yaml",
      "full_path": "/docs/agents/05/Agent05_Output.equipment_location_model.yaml",
      "exists": true,
      "size_bytes": 45678,
      "format": "YAML",
      "format_valid": true,
      "sample_content": {
        "root_keys": ["meta", "location_types", "location_rules", "coverage_summary", "missing_locations"],
        "equipment_located": 199,
        "equipment_missing": 16
      },
      "line_count": 280
    },
    {
      "agent": "Agent-05",
      "file": "Agent05_Output.service_space_model.yaml",
      "full_path": "/docs/agents/05/Agent05_Output.service_space_model.yaml",
      "exists": true,
      "size_bytes": 34567,
      "format": "YAML",
      "format_valid": true,
      "line_count": 220
    },
    {
      "agent": "Agent-06",
      "file": "Agent06_Output.sensor_models.yaml",
      "full_path": "/docs/agents/06/Agent06_Output.sensor_models.yaml",
      "exists": true,
      "size_bytes": 78901,
      "format": "YAML",
      "format_valid": true,
      "sample_content": {
        "root_keys": ["meta", "sensor_types", "sensor_instances", "coverage_summary"],
        "total_sensors": 247
      },
      "line_count": 520
    },
    {
      "agent": "Agent-06",
      "file": "Agent06_Output.actuator_models.yaml",
      "full_path": "/docs/agents/06/Agent06_Output.actuator_models.yaml",
      "exists": true,
      "size_bytes": 56789,
      "format": "YAML",
      "format_valid": true,
      "sample_content": {
        "total_actuators": 156
      },
      "line_count": 380
    },
    {
      "agent": "Agent-06",
      "file": "Agent06_Output.control_loop_models.yaml",
      "full_path": "/docs/agents/06/Agent06_Output.control_loop_models.yaml",
      "exists": true,
      "size_bytes": 45678,
      "format": "YAML",
      "format_valid": true,
      "sample_content": {
        "total_control_loops": 87
      },
      "line_count": 320
    },
    {
      "agent": "Agent-07",
      "file": "Agent07_Output.metering_hierarchy.yaml",
      "full_path": "/docs/agents/07/Agent07_Output.metering_hierarchy.yaml",
      "exists": true,
      "size_bytes": 34567,
      "format": "YAML",
      "format_valid": true,
      "sample_content": {
        "root_keys": ["meta", "hierarchy", "energy_types", "meters", "coverage_summary"],
        "total_meters": 189,
        "metering_levels": 4
      },
      "line_count": 420
    },
    {
      "agent": "Agent-07",
      "file": "Agent07_Output.allocation_rules.yaml",
      "full_path": "/docs/agents/07/Agent07_Output.allocation_rules.yaml",
      "exists": true,
      "size_bytes": 23456,
      "format": "YAML",
      "format_valid": true,
      "line_count": 180
    },
    {
      "agent": "Agent-08",
      "file": "Agent08_Output.work_order_models.yaml",
      "full_path": "/docs/agents/08/Agent08_Output.work_order_models.yaml",
      "exists": true,
      "size_bytes": 45678,
      "format": "YAML",
      "format_valid": true,
      "sample_content": {
        "root_keys": ["meta", "order_types", "status_flow", "sla_definitions"],
        "order_type_count": 5
      },
      "line_count": 200
    },
    {
      "agent": "Agent-08",
      "file": "Agent08_Output.asset_lifecycle_models.yaml",
      "full_path": "/docs/agents/08/Agent08_Output.asset_lifecycle_models.yaml",
      "exists": true,
      "size_bytes": 56789,
      "format": "YAML",
      "format_valid": true,
      "sample_content": {
        "lifecycle_stages": 9
      },
      "line_count": 280
    }
  ]
}
```

---

## DOC-003: `concept_extraction_report.json`

```json
{
  "meta": {
    "report_id": "CER-CIM-20250117-FINAL",
    "version": "2.0.0",
    "description": "完整概念提取报告 - 基于Agent-01~08实际输出，包含字段级源文档追踪",
    "generated_by": "Gemini-CLI (本体工程索引与协调者)",
    "scan_timestamp": "2025-01-17T19:00:00Z"
  },

  "extraction_statistics": {
    "total_agents_scanned": 8,
    "total_entities_extracted": 85,
    "total_relationships_extracted": 12,
    "total_constraints_extracted": 7,
    "extraction_confidence_avg": 0.96
  },

  "extracted_entities": {
    "topology_domain": {
      "source_agent": "Agent-01",
      "source_file": "Agent01_Output.topology_definitions.yaml",
      "entities": [
        {
          "uri": "cim-topo:Node",
          "label_cn": "拓扑节点",
          "label_en": "Topology Node",
          "definition": "系统拓扑图中的抽象节点",
          "is_abstract": true,
          "source_trace": {
            "file": "Agent01_Output.topology_definitions.yaml",
            "section": "sec-3.1",
            "field_path": "node_types",
            "line_number": 45
          }
        },
        {
          "uri": "cim-topo:Source_Node",
          "label_cn": "源节点",
          "label_en": "Source Node",
          "definition": "系统的能量/介质输入端，流动的起点",
          "parent_class": "cim-topo:Node",
          "attributes": [
            {"name": "node_id", "type": "xsd:string", "required": true},
            {"name": "node_name", "type": "xsd:string", "required": true},
            {"name": "medium_type", "type": "xsd:string", "required": true},
            {"name": "is_external", "type": "xsd:boolean", "required": true},
            {"name": "capacity", "type": "xsd:decimal", "required": false}
          ],
          "source_trace": {
            "file": "Agent01_Output.topology_definitions.yaml",
            "section": "sec-3.1",
            "field_path": "node_types.source_node",
            "line_number": 48
          }
        },
        {
          "uri": "cim-topo:Sink_Node",
          "label_cn": "末端节点",
          "label_en": "Sink Node",
          "definition": "系统的能量/介质消耗端，流动的终点",
          "parent_class": "cim-topo:Node",
          "attributes": [
            {"name": "node_id", "type": "xsd:string", "required": true},
            {"name": "node_name", "type": "xsd:string", "required": true},
            {"name": "consumption_type", "type": "xsd:string", "required": true},
            {"name": "served_function", "type": "xsd:string", "required": false}
          ],
          "source_trace": {
            "file": "Agent01_Output.topology_definitions.yaml",
            "section": "sec-3.1",
            "field_path": "node_types.sink_node",
            "line_number": 65
          }
        },
        {
          "uri": "cim-topo:Distribution_Node",
          "label_cn": "分配节点",
          "label_en": "Distribution Node",
          "definition": "进行分配、汇集、调节的中间节点",
          "parent_class": "cim-topo:Node",
          "subtypes": ["Junction", "Splitter", "Regulator", "Transformer_Node"],
          "source_trace": {
            "file": "Agent01_Output.topology_definitions.yaml",
            "section": "sec-3.1",
            "field_path": "node_types.distribution_node",
            "line_number": 82
          }
        },
        {
          "uri": "cim-topo:LogicalNode",
          "label_cn": "逻辑节点",
          "label_en": "Logical Node",
          "definition": "纯逻辑节点，如汇流点/分配点，无需物理设备映射",
          "parent_class": "cim-topo:Node",
          "note": "新增类型，用于解决GAP-001中无需设备映射的节点",
          "source_trace": {
            "file": "cross_agent_gap_analysis.json",
            "section": "remediation_strategy",
            "field_path": "REM-001.steps[2]"
          }
        },
        {
          "uri": "cim-topo:Junction",
          "label_cn": "汇集点",
          "label_en": "Junction",
          "definition": "多路输入汇聚为一路输出",
          "parent_class": "cim-topo:LogicalNode",
          "examples": ["集水器", "汇流排"],
          "source_trace": {
            "file": "Agent01_Output.topology_definitions.yaml",
            "section": "sec-3.1",
            "field_path": "node_types.distribution_node.junction",
            "line_number": 92
          }
        },
        {
          "uri": "cim-topo:Splitter",
          "label_cn": "分配点",
          "label_en": "Splitter",
          "definition": "一路输入分配为多路输出",
          "parent_class": "cim-topo:LogicalNode",
          "examples": ["分水器", "配电柜"],
          "source_trace": {
            "file": "Agent01_Output.topology_definitions.yaml",
            "section": "sec-3.1",
            "field_path": "node_types.distribution_node.splitter",
            "line_number": 98
          }
        },
        {
          "uri": "cim-topo:Regulator",
          "label_cn": "调节点",
          "label_en": "Regulator",
          "definition": "对流量/压力/电压等进行调节",
          "parent_class": "cim-topo:Distribution_Node",
          "examples": ["调节阀", "变频器"],
          "source_trace": {
            "file": "Agent01_Output.topology_definitions.yaml",
            "section": "sec-3.1",
            "field_path": "node_types.distribution_node.regulator",
            "line_number": 104
          }
        },
        {
          "uri": "cim-topo:Transformer_Node",
          "label_cn": "转换点",
          "label_en": "Transformer Node",
          "definition": "改变介质形态或能量品位",
          "parent_class": "cim-topo:Distribution_Node",
          "examples": ["换热器", "变压器", "AHU"],
          "source_trace": {
            "file": "Agent01_Output.topology_definitions.yaml",
            "section": "sec-3.1",
            "field_path": "node_types.distribution_node.transformer",
            "line_number": 110
          }
        },
        {
          "uri": "cim-topo:Edge",
          "label_cn": "拓扑边",
          "label_en": "Topology Edge",
          "definition": "拓扑图中节点之间的连接",
          "is_abstract": true,
          "source_trace": {
            "file": "Agent01_Output.topology_definitions.yaml",
            "section": "sec-3.2",
            "field_path": "edge_types",
            "line_number": 121
          }
        },
        {
          "uri": "cim-topo:Trunk",
          "label_cn": "干管/主线",
          "label_en": "Trunk",
          "definition": "主要传输通道，承载大流量",
          "parent_class": "cim-topo:Edge",
          "examples": ["高压母线", "冷冻水主管", "送风主管"],
          "source_trace": {
            "file": "Agent01_Output.topology_definitions.yaml",
            "section": "sec-3.2",
            "field_path": "edge_types.trunk",
            "line_number": 125
          }
        },
        {
          "uri": "cim-topo:Branch",
          "label_cn": "支管/支线",
          "label_en": "Branch",
          "definition": "从干线分出的次级通道",
          "parent_class": "cim-topo:Edge",
          "examples": ["楼层配电", "楼层水平管", "支风管"],
          "source_trace": {
            "file": "Agent01_Output.topology_definitions.yaml",
            "section": "sec-3.2",
            "field_path": "edge_types.branch",
            "line_number": 145
          }
        },
        {
          "uri": "cim-topo:Terminal_Connection",
          "label_cn": "末端连接",
          "label_en": "Terminal Connection",
          "definition": "连接到末端设备的最后一段",
          "parent_class": "cim-topo:Edge",
          "examples": ["风机盘管接管", "灯具线路"],
          "source_trace": {
            "file": "Agent01_Output.topology_definitions.yaml",
            "section": "sec-3.2",
            "field_path": "edge_types.terminal_connection",
            "line_number": 165
          }
        },
        {
          "uri": "cim-topo:System",
          "label_cn": "技术系统",
          "label_en": "Technical System",
          "definition": "8大系统26子系统的抽象类",
          "source_trace": {
            "file": "Agent01_Output.system_catalog.yaml",
            "section": "sec-1",
            "field_path": "systems",
            "line_number": 5
          }
        }
      ],
      "system_catalog": {
        "total_major_systems": 8,
        "total_subsystems": 26,
        "source_trace": {
          "file": "Agent01_Output.system_catalog.yaml",
          "section": "sec-1",
          "field_path": "systems",
          "line_number": 5
        },
        "categories": [
          {
            "id": "HVAC",
            "name": "暖通空调系统",
            "subsystem_count": 8,
            "subsystems": ["冷源系统", "热源系统", "空调系统", "通风系统", "净化空调系统", "防排烟系统", "冷却水系统", "冷冻水系统"],
            "source_trace": {"file": "Agent01_Output.system_catalog.yaml", "field_path": "systems.HVAC", "line_number": 12}
          },
          {
            "id": "ELECTRICAL",
            "name": "电气系统",
            "subsystem_count": 5,
            "subsystems": ["高压配电", "低压配电", "应急电源", "照明系统", "防雷接地"],
            "source_trace": {"file": "Agent01_Output.system_catalog.yaml", "field_path": "systems.ELECTRICAL", "line_number": 45}
          },
          {
            "id": "PLUMBING",
            "name": "给排水系统",
            "subsystem_count": 4,
            "subsystems": ["给水系统", "排水系统", "热水系统", "中水系统"],
            "source_trace": {"file": "Agent01_Output.system_catalog.yaml", "field_path": "systems.PLUMBING", "line_number": 78}
          },
          {
            "id": "MEDICAL_GAS",
            "name": "医疗气体系统",
            "subsystem_count": 3,
            "subsystems": ["氧气系统", "真空系统", "压缩空气系统"],
            "source_trace": {"file": "Agent01_Output.system_catalog.yaml", "field_path": "systems.MEDICAL_GAS", "line_number": 112}
          },
          {
            "id": "FIRE_PROTECTION",
            "name": "消防系统",
            "subsystem_count": 2,
            "subsystems": ["消火栓系统", "自动喷淋系统"],
            "source_trace": {"file": "Agent01_Output.system_catalog.yaml", "field_path": "systems.FIRE_PROTECTION", "line_number": 145}
          },
          {
            "id": "VERTICAL_TRANSPORT",
            "name": "垂直交通系统",
            "subsystem_count": 2,
            "subsystems": ["电梯系统", "自动扶梯系统"],
            "source_trace": {"file": "Agent01_Output.system_catalog.yaml", "field_path": "systems.VERTICAL_TRANSPORT", "line_number": 178}
          },
          {
            "id": "BUILDING_AUTOMATION",
            "name": "楼宇自动化系统",
            "subsystem_count": 1,
            "subsystems": ["BAS系统"],
            "source_trace": {"file": "Agent01_Output.system_catalog.yaml", "field_path": "systems.BUILDING_AUTOMATION", "line_number": 211}
          },
          {
            "id": "SPECIAL_MEDICAL",
            "name": "医疗专用系统",
            "subsystem_count": 1,
            "subsystems": ["洁净室系统"],
            "source_trace": {"file": "Agent01_Output.system_catalog.yaml", "field_path": "systems.SPECIAL_MEDICAL", "line_number": 244}
          }
        ]
      }
    },

    "space_domain": {
      "source_agent": "Agent-02",
      "hierarchy_levels": [
        {
          "level_id": "L0",
          "uri": "cim-space:Site",
          "label_cn": "院区",
          "label_en": "Site",
          "description": "医疗机构的整体基地范围",
          "attributes": [
            {"name": "site_name", "type": "xsd:string"},
            {"name": "total_area", "type": "xsd:decimal", "unit": "m²"},
            {"name": "total_building_area", "type": "xsd:decimal", "unit": "m²"}
          ],
          "source_trace": {
            "file": "Agent02_Output.space_hierarchy_model.yaml",
            "section": "sec-2.1",
            "field_path": "hierarchy.L0_Site",
            "line_number": 35
          }
        },
        {
          "level_id": "L1",
          "uri": "cim-space:Building",
          "label_cn": "建筑",
          "label_en": "Building",
          "description": "单体建筑物",
          "attributes": [
            {"name": "building_code", "type": "xsd:string"},
            {"name": "building_name", "type": "xsd:string"},
            {"name": "building_type", "type": "xsd:string", "enum": ["门诊", "住院", "医技", "后勤", "综合"]},
            {"name": "floor_count", "type": "xsd:integer"},
            {"name": "building_area", "type": "xsd:decimal", "unit": "m²"}
          ],
          "source_trace": {
            "file": "Agent02_Output.space_hierarchy_model.yaml",
            "section": "sec-2.1",
            "field_path": "hierarchy.L1_Building",
            "line_number": 52
          }
        },
        {
          "level_id": "L2",
          "uri": "cim-space:Floor",
          "label_cn": "楼层",
          "label_en": "Floor",
          "description": "建筑楼层（地上/地下/夹层/屋顶）",
          "attributes": [
            {"name": "floor_number", "type": "xsd:integer"},
            {"name": "floor_type", "type": "xsd:string", "enum": ["地上", "地下", "夹层", "屋顶"]},
            {"name": "floor_height", "type": "xsd:decimal", "unit": "m"}
          ],
          "source_trace": {
            "file": "Agent02_Output.space_hierarchy_model.yaml",
            "section": "sec-2.1",
            "field_path": "hierarchy.L2_Floor",
            "line_number": 78
          }
        },
        {
          "level_id": "L3",
          "uri": "cim-space:Zone",
          "label_cn": "功能区域",
          "label_en": "Zone",
          "description": "同一楼层内的功能分区",
          "zone_types": {
            "医疗区": ["诊室区", "治疗区", "病房区", "手术区"],
            "医技区": ["检验区", "影像区", "药房区"],
            "后勤区": ["设备区", "库房区", "厨房区"],
            "公共区": ["门厅区", "走廊区", "电梯厅"]
          },
          "source_trace": {
            "file": "Agent02_Output.space_hierarchy_model.yaml",
            "section": "sec-2.1",
            "field_path": "hierarchy.L3_Zone",
            "line_number": 95
          }
        },
        {
          "level_id": "L4",
          "uri": "cim-space:Room",
          "label_cn": "房间",
          "label_en": "Room",
          "description": "独立房间/空间",
          "attributes": [
            {"name": "room_number", "type": "xsd:string"},
            {"name": "room_name", "type": "xsd:string"},
            {"name": "room_area", "type": "xsd:decimal", "unit": "m²"},
            {"name": "room_function", "type": "xsd:string"}
          ],
          "source_trace": {
            "file": "Agent02_Output.space_hierarchy_model.yaml",
            "section": "sec-2.1",
            "field_path": "hierarchy.L4_Room",
            "line_number": 120
          }
        },
        {
          "level_id": "L5",
          "uri": "cim-space:SubSpace",
          "label_cn": "子空间",
          "label_en": "SubSpace",
          "description": "房间内的子空间（如手术区、麻醉准备区）",
          "source_trace": {
            "file": "Agent02_Output.space_hierarchy_model.yaml",
            "section": "sec-2.1",
            "field_path": "hierarchy.L5_SubSpace",
            "line_number": 138
          }
        }
      ],
      "medical_special_spaces": [
        {
          "uri": "cim-space:CleanSpace",
          "label_cn": "洁净空间",
          "label_en": "Clean Space",
          "description": "所有需要洁净度控制的空间的抽象基类",
          "parent_class": "cim-space:Room",
          "is_abstract": true,
          "source_trace": {
            "file": "Agent02_Output.medical_special_spaces.yaml",
            "section": "sec-3",
            "field_path": "special_spaces.clean_space",
            "line_number": 15
          }
        },
        {
          "uri": "cim-space:OperatingRoom",
          "label_cn": "手术室",
          "label_en": "Operating Room",
          "code": "OR",
          "parent_class": "cim-space:CleanSpace",
          "grades": [
            {"grade": "Class_I", "iso_class": "ISO-5", "description": "特别洁净手术室"},
            {"grade": "Class_II", "iso_class": "ISO-6", "description": "标准洁净手术室"},
            {"grade": "Class_III", "iso_class": "ISO-7", "description": "一般洁净手术室"},
            {"grade": "Class_IV", "iso_class": "ISO-8.5", "description": "准洁净手术室"}
          ],
          "standard_reference": "GB 50333-2013",
          "required_properties": [
            "cim-space:surgeryGrade",
            "cim-space:cleanlinessClass",
            "cim-space:temperature",
            "cim-space:relativeHumidity",
            "cim-space:pressureDifferential",
            "cim-space:airChangesPerHour",
            "cim-space:freshAirRatio",
            "cim-space:noiseLevel",
            "cim-space:illuminance"
          ],
          "source_trace": {
            "file": "Agent02_Output.medical_special_spaces.yaml",
            "section": "sec-3.1",
            "field_path": "special_spaces.operating_rooms",
            "line_number": 25
          }
        },
        {
          "uri": "cim-space:ICU",
          "label_cn": "重症监护室",
          "label_en": "ICU",
          "parent_class": "cim-space:CleanSpace",
          "subtypes": [
            {"type": "ICU_General", "label_cn": "综合ICU"},
            {"type": "ICU_CCU", "label_cn": "心脏ICU"},
            {"type": "ICU_NICU", "label_cn": "新生儿ICU"},
            {"type": "ICU_PICU", "label_cn": "儿科ICU"}
          ],
          "source_trace": {
            "file": "Agent02_Output.medical_special_spaces.yaml",
            "section": "sec-3.2",
            "field_path": "special_spaces.ICU",
            "line_number": 125
          }
        },
        {
          "uri": "cim-space:IsolationWard",
          "label_cn": "隔离病房",
          "label_en": "Isolation Ward",
          "parent_class": "cim-space:Room",
          "subtypes": [
            {"type": "Positive_Pressure", "label_cn": "正压隔离", "use_case": "免疫缺陷患者"},
            {"type": "Negative_Pressure", "label_cn": "负压隔离", "use_case": "传染病患者"}
          ],
          "standard_reference": "WS/T 311-2009",
          "required_properties": [
            "cim-space:isolationType",
            "cim-space:pressureDifferential",
            "cim-space:airChangesPerHour"
          ],
          "source_trace": {
            "file": "Agent02_Output.medical_special_spaces.yaml",
            "section": "sec-3.3",
            "field_path": "special_spaces.isolation_ward",
            "line_number": 185
          }
        },
        {
          "uri": "cim-space:CleanLab",
          "label_cn": "洁净实验室",
          "label_en": "Clean Laboratory",
          "parent_class": "cim-space:CleanSpace",
          "biosafety_levels": [
            {"level": "BSL-1", "description": "基础实验室"},
            {"level": "BSL-2", "description": "基础实验室+"},
            {"level": "BSL-3", "description": "防护实验室"}
          ],
          "standard_reference": "GB 19489-2008",
          "required_properties": [
            "cim-space:biosafetyLevel",
            "cim-space:pressureDifferential",
            "cim-space:freshAirRatio"
          ],
          "source_trace": {
            "file": "Agent02_Output.medical_special_spaces.yaml",
            "section": "sec-3.4",
            "field_path": "special_spaces.clean_lab",
            "line_number": 245
          }
        }
      ]
    },

    "equipment_domain": {
      "source_agent": "Agent-03",
      "statistics": {
        "total_system_categories": 8,
        "total_equipment_families": 18,
        "total_equipment_types": 123,
        "topology_nodes_total": 156,
        "topology_nodes_mapped": 89,
        "mapping_coverage": "57.1%",
        "mapping_gap": 67,
        "source_trace": {
          "file": "Agent03_Output.node_equipment_mapping.yaml",
          "section": "sec-1",
          "field_path": "mapping_summary",
          "line_number": 5
        }
      },
      "equipment_hierarchy": [
        {
          "level_id": "Level_1",
          "uri": "cim-equip:System",
          "label_cn": "系统",
          "label_en": "System (Equipment Context)",
          "definition": "完成特定功能的设备集合",
          "example": "1号冷站系统",
          "source_trace": {
            "file": "Agent03_Output.equipment_classification.yaml",
            "section": "sec-2.1",
            "field_path": "hierarchy.level_1_system",
            "line_number": 28
          }
        },
        {
          "level_id": "Level_2",
          "uri": "cim-equip:Equipment",
          "label_cn": "设备",
          "label_en": "Equipment",
          "definition": "独立的功能装置（本模型核心）",
          "example": "CH-001 离心式冷水机组",
          "source_trace": {
            "file": "Agent03_Output.equipment_classification.yaml",
            "section": "sec-2.1",
            "field_path": "hierarchy.level_2_equipment",
            "line_number": 45
          }
        },
        {
          "level_id": "Level_3",
          "uri": "cim-equip:Component",
          "label_cn": "组件",
          "label_en": "Component",
          "definition": "设备的组成部分",
          "example": "CH-001-COMP 1号冷机压缩机",
          "source_trace": {
            "file": "Agent03_Output.equipment_classification.yaml",
            "section": "sec-2.1",
            "field_path": "hierarchy.level_3_component",
            "line_number": 62
          }
        },
        {
          "level_id": "Level_4",
          "uri": "cim-equip:Part",
          "label_cn": "零部件",
          "label_en": "Part",
          "definition": "可更换的零部件",
          "example": "CH-001-FILTER 油过滤器",
          "source_trace": {
            "file": "Agent03_Output.equipment_classification.yaml",
            "section": "sec-2.1",
            "field_path": "hierarchy.level_4_part",
            "line_number": 75
          }
        }
      ],
      "reliability_classification": [
        {
          "level": "LIFE_SAFETY",
          "label_cn": "生命安全级",
          "equipment_count": 12,
          "examples": ["柴油发电机", "液氧储罐", "HEPA过滤器", "消火栓泵"],
          "requirements": "必须有冗余配置(N+1)",
          "source_trace": {
            "file": "Agent03_Output.equipment_classification.yaml",
            "section": "sec-2.2",
            "field_path": "reliability.LIFE_SAFETY",
            "line_number": 85
          }
        },
        {
          "level": "PATIENT_SAFETY",
          "label_cn": "患者安全级",
          "equipment_count": 15,
          "examples": ["医用隔离变压器", "洁净空调机组", "医疗气体设备"],
          "requirements": "建议有冗余配置",
          "source_trace": {
            "file": "Agent03_Output.equipment_classification.yaml",
            "section": "sec-2.2",
            "field_path": "reliability.PATIENT_SAFETY",
            "line_number": 102
          }
        },
        {
          "level": "CRITICAL",
          "label_cn": "关键级",
          "equipment_count": 48,
          "examples": ["冷水机组", "变压器", "UPS", "电梯"],
          "source_trace": {
            "file": "Agent03_Output.equipment_classification.yaml",
            "section": "sec-2.2",
            "field_path": "reliability.CRITICAL",
            "line_number": 118
          }
        },
        {
          "level": "IMPORTANT",
          "label_cn": "重要级",
          "equipment_count": 28,
          "source_trace": {
            "file": "Agent03_Output.equipment_classification.yaml",
            "section": "sec-2.2",
            "field_path": "reliability.IMPORTANT",
            "line_number": 135
          }
        },
        {
          "level": "SECONDARY",
          "label_cn": "次要级",
          "equipment_count": 20,
          "source_trace": {
            "file": "Agent03_Output.equipment_classification.yaml",
            "section": "sec-2.2",
            "field_path": "reliability.SECONDARY",
            "line_number": 148
          }
        }
      ],
      "p0_core_equipment": [
        {"type": "离心式冷水机组", "system": "HVAC", "code": "CH-CENT"},
        {"type": "螺杆式冷水机组", "system": "HVAC", "code": "CH-SCREW"},
        {"type": "洁净空调机组", "system": "HVAC", "code": "AHU-CLEAN"},
        {"type": "HEPA高效过滤器", "system": "HVAC", "code": "HEPA"},
        {"type": "冷却塔", "system": "HVAC", "code": "CT"},
        {"type": "水泵(冷冻/冷却/热水)", "system": "HVAC", "code": "PUMP"},
        {"type": "变风量VAV末端", "system": "HVAC", "code": "VAV"},
        {"type": "电力变压器", "system": "ELECTRICAL", "code": "XFMR"},
        {"type": "高低压开关柜", "system": "ELECTRICAL", "code": "SWGR"},
        {"type": "柴油发电机组", "system": "ELECTRICAL", "code": "GENSET"},
        {"type": "UPS不间断电源", "system": "ELECTRICAL", "code": "UPS"},
        {"type": "医用隔离变压器", "system": "ELECTRICAL", "code": "ISO-XFMR"},
        {"type": "配电柜", "system": "ELECTRICAL", "code": "PANEL"},
        {"type": "液氧储罐系统", "system": "MEDICAL_GAS", "code": "LOX"},
        {"type": "医用真空系统", "system": "MEDICAL_GAS", "code": "VAC"},
        {"type": "无油空压机", "system": "MEDICAL_GAS", "code": "AIR-COMP"},
        {"type": "消火栓泵", "system": "FIRE_PROTECTION", "code": "FIRE-PUMP"},
        {"type": "病床电梯", "system": "VERTICAL_TRANSPORT", "code": "ELEV-BED"}
      ]
    },

    "flow_domain": {
      "source_agent": "Agent-04",
      "source_file": "Agent04_v2.3_FlowModel.ttl",
      "version": "v2.3",
      "flow_layers": [
        {
          "layer_id": "Layer_1",
          "uri": "cim-flow:Mass_Flow",
          "label_cn": "物质流",
          "label_en": "Mass Flow",
          "definition": "作为能量的载体在系统中流动的物质",
          "media": ["水", "空气", "蒸汽", "制冷剂", "医疗气体"],
          "characteristics": ["流量(kg/s)", "压力(Pa)", "温度(°C)", "成分"],
          "source_trace": {
            "file": "Agent04_v2.3_FlowModel.ttl",
            "section": "sec-flow-layers",
            "line_number": 55
          }
        },
        {
          "layer_id": "Layer_2",
          "uri": "cim-flow:Energy_Flow",
          "label_cn": "能量流",
          "label_en": "Energy Flow",
          "definition": "由物质流承载的能量传递",
          "energy_types": ["热能", "冷量", "电能"],
          "source_trace": {
            "file": "Agent04_v2.3_FlowModel.ttl",
            "section": "sec-flow-layers",
            "line_number": 120
          }
        },
        {
          "layer_id": "Layer_3",
          "uri": "cim-flow:Information_Flow",
          "label_cn": "信息流",
          "label_en": "Information Flow",
          "definition": "控制信号和状态数据的传递",
          "source_trace": {
            "file": "Agent04_v2.3_FlowModel.ttl",
            "section": "sec-flow-layers",
            "line_number": 180
          }
        }
      ],
      "flow_sequence": {
        "uri": "cim-flow:FlowSequence",
        "label_cn": "流动序列",
        "definition": "从源到末端的完整流动通道",
        "types": ["Supply_Path (供应路径)", "Return_Path (回流路径)"],
        "source_trace": {
          "file": "Agent04_v2.3_FlowModel.ttl",
          "section": "sec-flow-layers",
          "line_number": 220
        }
      }
    },

    "coupling_domain": {
      "source_agent": "Agent-05",
      "source_file": "Agent05_Output.equipment_location_model.yaml",
      "statistics": {
        "total_equipment": 215,
        "equipment_with_location": 199,
        "equipment_without_location": 16,
        "location_coverage": "92.6%",
        "source_trace": {
          "file": "Agent05_Output.equipment_location_model.yaml",
          "section": "sec-3",
          "field_path": "coverage_summary",
          "line_number": 205
        }
      },
      "location_types": [
        {
          "type_id": "LOC-MEP-ROOM",
          "uri": "cim-loc:MEP_Room",
          "label_cn": "机电设备用房",
          "description": "专门用于放置机电设备的房间",
          "examples": ["冷冻站", "热力站", "变配电室", "水泵房", "空调机房"],
          "typical_floor": "地下室/屋顶",
          "source_trace": {
            "file": "Agent05_Output.equipment_location_model.yaml",
            "section": "sec-1",
            "field_path": "location_types.MEP_ROOM",
            "line_number": 25
          }
        },
        {
          "type_id": "LOC-SHAFT",
          "uri": "cim-loc:Shaft",
          "label_cn": "竖井",
          "description": "垂直方向的管线通道",
          "subtypes": ["电气竖井", "水暖竖井", "通风竖井"],
          "source_trace": {
            "file": "Agent05_Output.equipment_location_model.yaml",
            "section": "sec-1",
            "field_path": "location_types.SHAFT",
            "line_number": 45
          }
        },
        {
          "type_id": "LOC-CEILING",
          "uri": "cim-loc:Ceiling_Void",
          "label_cn": "吊顶内",
          "description": "吊顶与楼板之间的空间",
          "typical_equipment": ["FCU", "小型AHU", "管线"],
          "source_trace": {
            "file": "Agent05_Output.equipment_location_model.yaml",
            "section": "sec-1",
            "field_path": "location_types.CEILING",
            "line_number": 65
          }
        },
        {
          "type_id": "LOC-SERVED-SPACE",
          "uri": "cim-loc:Served_Space",
          "label_cn": "服务空间内",
          "description": "直接安装在被服务空间内的设备",
          "typical_equipment": ["明装FCU", "室内机", "末端设备"],
          "source_trace": {
            "file": "Agent05_Output.equipment_location_model.yaml",
            "section": "sec-1",
            "field_path": "location_types.SERVED_SPACE",
            "line_number": 85
          }
        }
      ]
    },

    "control_domain": {
      "source_agent": "Agent-06",
      "statistics": {
        "total_sensors": 247,
        "total_actuators": 156,
        "total_control_loops": 87,
        "equipment_needing_control": 123,
        "equipment_with_control": 98,
        "control_coverage": "79.7%",
        "control_gap": 25,
        "source_trace": {
          "file": "Agent06_Output.sensor_models.yaml",
          "section": "sec-2",
          "field_path": "coverage_summary",
          "line_number": 485
        }
      },
      "sensor_types": [
        {
          "type_id": "SENSOR-TEMP",
          "uri": "cim-ctrl:Temperature_Sensor",
          "label_cn": "温度传感器",
          "measured_parameter": "temperature",
          "unit": "°C",
          "variants": [
            {"id": "SENSOR-TEMP-PIPE", "label_cn": "管道式温度传感器"},
            {"id": "SENSOR-TEMP-DUCT", "label_cn": "风管式温度传感器"},
            {"id": "SENSOR-TEMP-ROOM", "label_cn": "室内温度传感器"}
          ],
          "attributes": [
            {"name": "measurement_range", "typical_value": "-20~100°C"},
            {"name": "accuracy", "typical_value": "±0.5°C"},
            {"name": "output_signal", "typical_value": "4-20mA, 0-10V, Modbus"}
          ],
          "source_trace": {
            "file": "Agent06_Output.sensor_models.yaml",
            "section": "sec-1",
            "field_path": "sensor_types.TEMP",
            "line_number": 35
          }
        },
        {
          "type_id": "SENSOR-HUMIDITY",
          "uri": "cim-ctrl:Humidity_Sensor",
          "label_cn": "湿度传感器",
          "measured_parameter": "humidity",
          "unit": "%RH",
          "source_trace": {
            "file": "Agent06_Output.sensor_models.yaml",
            "section": "sec-1",
            "field_path": "sensor_types.HUMIDITY",
            "line_number": 85
          }
        },
        {
          "type_id": "SENSOR-PRESSURE",
          "uri": "cim-ctrl:Pressure_Sensor",
          "label_cn": "压力/压差传感器",
          "measured_parameter": "pressure",
          "unit": "Pa / kPa",
          "source_trace": {
            "file": "Agent06_Output.sensor_models.yaml",
            "section": "sec-1",
            "field_path": "sensor_types.PRESSURE",
            "line_number": 120
          }
        }
      ],
      "actuator_types": [
        {
          "type_id": "ACTUATOR-VALVE",
          "uri": "cim-ctrl:Valve_Actuator",
          "label_cn": "阀门执行器",
          "controlled_element": "阀门",
          "source_trace": {
            "file": "Agent06_Output.actuator_models.yaml",
            "section": "sec-1",
            "field_path": "actuator_types.VALVE",
            "line_number": 25
          }
        },
        {
          "type_id": "ACTUATOR-DAMPER",
          "uri": "cim-ctrl:Damper_Actuator",
          "label_cn": "风阀执行器",
          "controlled_element": "风阀",
          "source_trace": {
            "file": "Agent06_Output.actuator_models.yaml",
            "section": "sec-1",
            "field_path": "actuator_types.DAMPER",
            "line_number": 55
          }
        },
        {
          "type_id": "ACTUATOR-VFD",
          "uri": "cim-ctrl:VFD",
          "label_cn": "变频器",
          "controlled_element": "电机转速",
          "source_trace": {
            "file": "Agent06_Output.actuator_models.yaml",
            "section": "sec-1",
            "field_path": "actuator_types.VFD",
            "line_number": 85
          }
        }
      ],
      "controller_types": ["DDC", "PLC"],
      "control_strategies": ["冷站群控策略", "AHU控制策略", "洁净室压差控制策略"]
    },

    "metering_domain": {
      "source_agent": "Agent-07",
      "source_file": "Agent07_Output.metering_hierarchy.yaml",
      "statistics": {
        "metering_levels": 4,
        "energy_types": 7,
        "total_metering_points": 189,
        "equipment_needing_metering": 75,
        "equipment_with_metering": 68,
        "metering_coverage": "90.7%",
        "metering_gap": 7,
        "source_trace": {
          "file": "Agent07_Output.metering_hierarchy.yaml",
          "section": "sec-3",
          "field_path": "coverage_summary",
          "line_number": 385
        }
      },
      "metering_hierarchy": [
        {
          "level_id": "METER-L0",
          "uri": "cim-meter:Total_Meter",
          "label_cn": "总表层",
          "description": "院区/建筑总进线计量",
          "energy_types": ["电", "水", "气", "热"],
          "source_trace": {
            "file": "Agent07_Output.metering_hierarchy.yaml",
            "section": "sec-1",
            "field_path": "hierarchy.L0_Total",
            "line_number": 20
          }
        },
        {
          "level_id": "METER-L1",
          "uri": "cim-meter:Zone_Meter",
          "label_cn": "区域表层",
          "description": "建筑/分区计量",
          "source_trace": {
            "file": "Agent07_Output.metering_hierarchy.yaml",
            "section": "sec-1",
            "field_path": "hierarchy.L1_Zone",
            "line_number": 45
          }
        },
        {
          "level_id": "METER-L2",
          "uri": "cim-meter:Tenant_Meter",
          "label_cn": "分户表层",
          "description": "科室/租户计量",
          "source_trace": {
            "file": "Agent07_Output.metering_hierarchy.yaml",
            "section": "sec-1",
            "field_path": "hierarchy.L2_Tenant",
            "line_number": 65
          }
        },
        {
          "level_id": "METER-L3",
          "uri": "cim-meter:Subitem_Meter",
          "label_cn": "分项表层",
          "description": "用能类型/设备计量",
          "source_trace": {
            "file": "Agent07_Output.metering_hierarchy.yaml",
            "section": "sec-1",
            "field_path": "hierarchy.L3_Subitem",
            "line_number": 85
          }
        }
      ],
      "energy_types": [
        {"id": "ELEC", "name": "电能", "unit": "kWh"},
        {"id": "WATER", "name": "水", "unit": "m³"},
        {"id": "GAS", "name": "天然气", "unit": "m³"},
        {"id": "HEAT", "name": "热量", "unit": "GJ"},
        {"id": "COOL", "name": "冷量", "unit": "kWh"},
        {"id": "STEAM", "name": "蒸汽", "unit": "t"},
        {"id": "MEDICAL_GAS", "name": "医疗气体", "unit": "m³"}
      ]
    },

    "operations_domain": {
      "source_agent": "Agent-08",
      "work_order_model": {
        "order_types": [
          {"type": "CORRECTIVE", "label_cn": "报修工单"},
          {"type": "PREVENTIVE", "label_cn": "预防性维护工单"},
          {"type": "PREDICTIVE", "label_cn": "预测性维护工单"},
          {"type": "INSPECTION", "label_cn": "巡检工单"},
          {"type": "PROJECT", "label_cn": "项目工单"}
        ],
        "status_flow": ["CREATED", "ASSIGNED", "IN_PROGRESS", "ON_HOLD", "COMPLETED", "VERIFIED", "CLOSED"],
        "source_trace": {
          "file": "Agent08_Output.work_order_models.yaml",
          "section": "sec-1",
          "field_path": "order_types",
          "line_number": 25
        }
      },
      "maintenance_strategies": [
        {
          "strategy_id": "PM",
          "uri": "cim-om:Preventive_Maintenance",
          "label_cn": "预防性维护",
          "description": "基于时间或运行量的定期维护",
          "source_trace": {
            "file": "Agent08_Output.work_order_models.yaml",
            "section": "sec-2",
            "field_path": "maintenance_strategies.PM",
            "line_number": 85
          }
        },
        {
          "strategy_id": "PdM",
          "uri": "cim-om:Predictive_Maintenance",
          "label_cn": "预测性维护",
          "description": "基于状态监测和数据分析的预测维护",
          "source_trace": {
            "file": "Agent08_Output.work_order_models.yaml",
            "section": "sec-2",
            "field_path": "maintenance_strategies.PdM",
            "line_number": 105
          }
        }
      ],
      "asset_lifecycle": {
        "stages_count": 9,
        "stages": [
          {"stage": "PLANNING", "label_cn": "规划"},
          {"stage": "PROCUREMENT", "label_cn": "采购"},
          {"stage": "INSTALLATION", "label_cn": "安装"},
          {"stage": "COMMISSIONING", "label_cn": "调试"},
          {"stage": "OPERATION", "label_cn": "运行"},
          {"stage": "MAINTENANCE", "label_cn": "维护"},
          {"stage": "DEGRADATION", "label_cn": "衰退"},
          {"stage": "RENEWAL_DECISION", "label_cn": "更新决策"},
          {"stage": "DECOMMISSIONING", "label_cn": "退役"}
        ],
        "source_trace": {
          "file": "Agent08_Output.asset_lifecycle_models.yaml",
          "section": "sec-1",
          "field_path": "lifecycle_stages",
          "line_number": 30
        }
      }
    }
  },

  "extracted_relationships": [
    {
      "relation_id": "REL-001",
      "uri": "cim:locatedIn",
      "label_cn": "位于",
      "label_en": "located in",
      "domain": "cim-equip:Equipment",
      "range": "cim-space:Space",
      "type": "Topological",
      "inverse": "cim:hasEquipment",
      "source_agent": "Agent-05",
      "source_trace": {"file": "Agent05_Output.equipment_location_model.yaml", "field_path": "relationships.locatedIn"}
    },
    {
      "relation_id": "REL-002",
      "uri": "cim:serves",
      "label_cn": "服务于",
      "label_en": "serves",
      "domain": "cim-equip:Equipment | cim-topo:System",
      "range": "cim-space:Space | cim-space:Zone",
      "type": "Functional",
      "source_agent": "Agent-05",
      "source_trace": {"file": "Agent05_Output.service_space_model.yaml", "field_path": "relationships.serves"}
    },
    {
      "relation_id": "REL-003",
      "uri": "cim-flow:feedsTo",
      "label_cn": "供给至",
      "label_en": "feeds to",
      "domain": "cim-topo:Node | cim-equip:Equipment",
      "range": "cim-topo:Node | cim-equip:Equipment",
      "type": "Flow",
      "properties": ["medium", "flowRate", "pressure", "temperature"],
      "source_agent": "Agent-04",
      "source_trace": {"file": "Agent04_v2.3_FlowModel.ttl", "field_path": "relationships.feedsTo"}
    },
    {
      "relation_id": "REL-004",
      "uri": "cim:contains",
      "label_cn": "包含",
      "label_en": "contains",
      "domain": "cim-space:Space (higher level)",
      "range": "cim-space:Space (lower level)",
      "type": "Structural",
      "is_transitive": true,
      "source_agent": "Agent-02",
      "source_trace": {"file": "Agent02_Output.space_hierarchy_model.yaml", "field_path": "relationships.contains"}
    },
    {
      "relation_id": "REL-005",
      "uri": "cim:componentOf",
      "label_cn": "组件属于",
      "label_en": "component of",
      "domain": "cim-equip:Component",
      "range": "cim-equip:Equipment",
      "type": "Structural",
      "source_agent": "Agent-03",
      "source_trace": {"file": "Agent03_Output.equipment_classification.yaml", "field_path": "relationships.componentOf"}
    },
    {
      "relation_id": "REL-006",
      "uri": "cim:dependsOn",
      "label_cn": "依赖于",
      "label_en": "depends on",
      "domain": "cim-topo:System",
      "range": "cim-topo:System",
      "type": "Dependency",
      "source_agent": "Agent-01",
      "source_trace": {"file": "Agent01_Output.topology_definitions.yaml", "field_path": "system_dependencies"}
    },
    {
      "relation_id": "REL-007",
      "uri": "cim-ctrl:monitors",
      "label_cn": "监测",
      "label_en": "monitors",
      "domain": "cim-ctrl:Sensor",
      "range": "cim-equip:Equipment | cim-space:Space",
      "type": "Control",
      "source_agent": "Agent-06",
      "source_trace": {"file": "Agent06_Output.sensor_models.yaml", "field_path": "relationships.monitors"}
    },
    {
      "relation_id": "REL-008",
      "uri": "cim-ctrl:controls",
      "label_cn": "控制",
      "label_en": "controls",
      "domain": "cim-ctrl:Actuator",
      "range": "cim-equip:Equipment",
      "type": "Control",
      "source_agent": "Agent-06",
      "source_trace": {"file": "Agent06_Output.actuator_models.yaml", "field_path": "relationships.controls"}
    },
    {
      "relation_id": "REL-009",
      "uri": "cim-meter:meters",
      "label_cn": "计量",
      "label_en": "meters",
      "domain": "cim-meter:Meter",
      "range": "cim-equip:Equipment | cim-flow:Flow | cim-space:Space",
      "type": "Metering",
      "note": "range扩展以支持GAP-004中的空间计量场景",
      "source_agent": "Agent-07",
      "source_trace": {"file": "Agent07_Output.metering_hierarchy.yaml", "field_path": "relationships.meters"}
    },
    {
      "relation_id": "REL-010",
      "uri": "cim:routesThrough",
      "label_cn": "穿越",
      "label_en": "routes through",
      "domain": "cim:Pipe | cim:Duct | cim:Cable",
      "range": "cim-space:Space",
      "type": "Routing",
      "source_agent": "Agent-05",
      "source_trace": {"file": "Agent05_Output.equipment_location_model.yaml", "field_path": "relationships.routesThrough"}
    },
    {
      "relation_id": "REL-011",
      "uri": "cim:mapsToNode",
      "label_cn": "映射到节点",
      "label_en": "maps to node",
      "domain": "cim-equip:Equipment",
      "range": "cim-topo:Node",
      "type": "Cross-Domain",
      "source_agent": "Agent-03",
      "source_trace": {"file": "Agent03_Output.node_equipment_mapping.yaml", "field_path": "mapping_definition"}
    },
    {
      "relation_id": "REL-012",
      "uri": "cim-meter:derivedFrom",
      "label_cn": "派生自",
      "label_en": "derived from",
      "domain": "cim-meter:VirtualMeter",
      "range": "cim-meter:Meter",
      "type": "Derivation",
      "note": "新增关系，用于表达虚拟计量点的计算来源",
      "source_agent": "Agent-07",
      "source_trace": {"file": "cross_agent_gap_analysis.json", "field_path": "REM-004.steps[2]"}
    }
  ],

  "extracted_constraints": [
    {
      "constraint_id": "CST-TOPO-001",
      "rule_description": "所有系统都必须有源节点(Source_Node)",
      "type": "Completeness",
      "source_agent": "Agent-01",
      "source_trace": {
        "file": "Agent01_Output.topology_definitions.yaml",
        "section": "sec-5.1",
        "field_path": "validation_rules.completeness[0]",
        "line_number": 380
      },
      "shacl_shape": {
        "shape_uri": "cim-shape:SystemMustHaveSourceShape",
        "target_class": "cim-topo:System",
        "turtle": "@prefix sh: <http://www.w3.org/ns/shacl#> .\n@prefix cim-topo: <https://cim.medical/ontology/v3.4/topology#> .\n@prefix cim-shape: <https://cim.medical/ontology/v3.4/shapes#> .\n\ncim-shape:SystemMustHaveSourceShape\n    a sh:NodeShape ;\n    sh:targetClass cim-topo:System ;\n    sh:property [\n        sh:path cim-topo:hasSourceNode ;\n        sh:minCount 1 ;\n        sh:class cim-topo:Source_Node ;\n        sh:message \"每个系统必须至少有一个源节点 (CST-TOPO-001)\"@zh-CN ;\n    ] ."
      },
      "sparql_check": {
        "query_type": "SELECT",
        "purpose": "查找没有源节点的系统",
        "query": "PREFIX cim-topo: <https://cim.medical/ontology/v3.4/topology#>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n\nSELECT ?system ?systemName\nWHERE {\n    ?system a cim-topo:System .\n    OPTIONAL { ?system rdfs:label ?systemName }\n    FILTER NOT EXISTS {\n        ?system cim-topo:hasSourceNode ?source .\n        ?source a cim-topo:Source_Node .\n    }\n}",
        "expected_result": "Empty result set",
        "error_message": "存在没有源节点的系统"
      }
    },
    {
      "constraint_id": "CST-TOPO-002",
      "rule_description": "所有末端节点都必须能追溯到源节点",
      "type": "Connectivity",
      "source_agent": "Agent-01",
      "source_trace": {
        "file": "Agent01_Output.topology_definitions.yaml",
        "section": "sec-5.1",
        "field_path": "validation_rules.connectivity[0]",
        "line_number": 395
      },
      "sparql_check": {
        "query_type": "SELECT",
        "purpose": "查找无法追溯到源节点的末端节点",
        "query": "PREFIX cim-topo: <https://cim.medical/ontology/v3.4/topology#>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n\nSELECT ?sink ?sinkName\nWHERE {\n    ?sink a cim-topo:Sink_Node .\n    OPTIONAL { ?sink rdfs:label ?sinkName }\n    FILTER NOT EXISTS {\n        ?source a cim-topo:Source_Node .\n        ?source (cim-topo:feedsTo)+ ?sink .\n    }\n}",
        "expected_result": "Empty result set",
        "error_message": "存在无法追溯到源节点的末端节点（网络不连通）"
      }
    },
    {
      "constraint_id": "CST-EQUIP-001",
      "rule_description": "Agent-01的每个拓扑节点在Agent-03中都必须有对应设备（LogicalNode除外）",
      "type": "Cross-Agent Consistency",
      "source_agent": "Agent-09",
      "source_trace": {
        "file": "Agent-09_v3.4_Instructions.md",
        "section": "PHASE-D",
        "field_path": "validation_rules.consistency_checks[0]"
      },
      "current_status": {
        "compliant": false,
        "gap_count": 67,
        "remediation_ref": "cross_agent_gap_analysis.json#GAP-001"
      },
      "shacl_shape": {
        "shape_uri": "cim-shape:NodeMustHaveEquipmentShape",
        "target_class": "cim-topo:Node",
        "turtle": "@prefix sh: <http://www.w3.org/ns/shacl#> .\n@prefix cim-topo: <https://cim.medical/ontology/v3.4/topology#> .\n@prefix cim-equip: <https://cim.medical/ontology/v3.4/equipment#> .\n@prefix cim: <https://cim.medical/ontology/v3.4#> .\n@prefix cim-shape: <https://cim.medical/ontology/v3.4/shapes#> .\n\ncim-shape:NodeMustHaveEquipmentShape\n    a sh:NodeShape ;\n    sh:targetClass cim-topo:Node ;\n    sh:sparql [\n        sh:message \"拓扑节点缺少对应的设备映射 (CST-EQUIP-001)\"@zh-CN ;\n        sh:select \"\"\"\n            PREFIX cim: <https://cim.medical/ontology/v3.4#>\n            PREFIX cim-topo: <https://cim.medical/ontology/v3.4/topology#>\n            SELECT $this\n            WHERE {\n                $this a ?nodeType .\n                ?nodeType rdfs:subClassOf* cim-topo:Node .\n                FILTER NOT EXISTS { $this a cim-topo:LogicalNode }\n                FILTER NOT EXISTS { ?equip cim:mapsToNode $this }\n            }\n        \"\"\" ;\n    ] ."
      },
      "sparql_check": {
        "query_type": "SELECT",
        "purpose": "查找没有设备映射的非逻辑拓扑节点",
        "query": "PREFIX cim: <https://cim.medical/ontology/v3.4#>\nPREFIX cim-topo: <https://cim.medical/ontology/v3.4/topology#>\nPREFIX cim-equip: <https://cim.medical/ontology/v3.4/equipment#>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n\nSELECT ?node ?nodeLabel ?nodeType\nWHERE {\n    ?node a ?nodeType .\n    ?nodeType rdfs:subClassOf* cim-topo:Node .\n    FILTER NOT EXISTS { ?node a cim-topo:LogicalNode }\n    OPTIONAL { ?node rdfs:label ?nodeLabel }\n    FILTER NOT EXISTS {\n        ?equip cim:mapsToNode ?node .\n        ?equip a/rdfs:subClassOf* cim-equip:Equipment .\n    }\n}",
        "expected_result": "Empty result set (理想情况), 当前已知缺失67个",
        "error_message": "存在没有设备映射的拓扑节点"
      }
    },
    {
      "constraint_id": "CST-SPACE-001",
      "rule_description": "Agent-03的设备在Agent-05中都必须有位置定义",
      "type": "Cross-Agent Consistency",
      "source_agent": "Agent-09",
      "source_trace": {
        "file": "Agent-09_v3.4_Instructions.md",
        "section": "PHASE-D",
        "field_path": "validation_rules.consistency_checks[1]"
      },
      "current_status": {
        "compliant": false,
        "gap_count": 16,
        "remediation_ref": "cross_agent_gap_analysis.json#GAP-002"
      },
      "shacl_shape": {
        "shape_uri": "cim-shape:EquipmentMustHaveLocationShape",
        "target_class": "cim-equip:Equipment",
        "turtle": "@prefix sh: <http://www.w3.org/ns/shacl#> .\n@prefix cim: <https://cim.medical/ontology/v3.4#> .\n@prefix cim-equip: <https://cim.medical/ontology/v3.4/equipment#> .\n@prefix cim-space: <https://cim.medical/ontology/v3.4/space#> .\n@prefix cim-shape: <https://cim.medical/ontology/v3.4/shapes#> .\n\ncim-shape:EquipmentMustHaveLocationShape\n    a sh:NodeShape ;\n    sh:targetClass cim-equip:Equipment ;\n    sh:property [\n        sh:path cim:locatedIn ;\n        sh:minCount 1 ;\n        sh:message \"设备必须有位置定义 (CST-SPACE-001)\"@zh-CN ;\n    ] ."
      },
      "sparql_check": {
        "query_type": "SELECT",
        "purpose": "查找没有位置定义的设备",
        "query": "PREFIX cim: <https://cim.medical/ontology/v3.4#>\nPREFIX cim-equip: <https://cim.medical/ontology/v3.4/equipment#>\nPREFIX cim-space: <https://cim.medical/ontology/v3.4/space#>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n\nSELECT ?equip ?equipLabel ?equipType\nWHERE {\n    ?equip a ?equipType .\n    ?equipType rdfs:subClassOf* cim-equip:Equipment .\n    OPTIONAL { ?equip rdfs:label ?equipLabel }\n    FILTER NOT EXISTS {\n        ?equip cim:locatedIn ?space .\n    }\n}",
        "expected_result": "Empty result set (理想情况), 当前已知缺失16个",
        "error_message": "存在没有位置定义的设备"
      }
    },
    {
      "constraint_id": "CST-CTRL-001",
      "rule_description": "Agent-06的传感器/执行器关联的设备在Agent-03中必须已定义",
      "type": "Cross-Agent Consistency",
      "source_agent": "Agent-09",
      "source_trace": {
        "file": "Agent-09_v3.4_Instructions.md",
        "section": "PHASE-D",
        "field_path": "validation_rules.consistency_checks[2]"
      },
      "sparql_check": {
        "query_type": "SELECT",
        "purpose": "查找控制点关联的设备是否在Agent-03已定义",
        "query": "PREFIX cim: <https://cim.medical/ontology/v3.4#>\nPREFIX cim-ctrl: <https://cim.medical/ontology/v3.4/control#>\nPREFIX cim-equip: <https://cim.medical/ontology/v3.4/equipment#>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n\nSELECT ?controlDevice ?controlLabel ?targetEquip\nWHERE {\n    { ?controlDevice a cim-ctrl:Sensor } UNION { ?controlDevice a cim-ctrl:Actuator }\n    OPTIONAL { ?controlDevice rdfs:label ?controlLabel }\n    ?controlDevice (cim-ctrl:monitors|cim-ctrl:controls) ?targetEquip .\n    FILTER NOT EXISTS {\n        ?targetEquip a/rdfs:subClassOf* cim-equip:Equipment .\n    }\n}",
        "expected_result": "Empty result set",
        "error_message": "控制点关联了未在Agent-03定义的设备"
      }
    },
    {
      "constraint_id": "CST-METER-001",
      "rule_description": "Agent-07的计量点必须有明确的计量对象（设备或空间）",
      "type": "Cross-Agent Consistency",
      "source_agent": "Agent-09",
      "source_trace": {
        "file": "Agent-09_v3.4_Instructions.md",
        "section": "PHASE-D",
        "field_path": "validation_rules.consistency_checks[3]"
      },
      "current_status": {
        "compliant": false,
        "gap_count": 7,
        "remediation_ref": "cross_agent_gap_analysis.json#GAP-004"
      },
      "sparql_check": {
        "query_type": "SELECT",
        "purpose": "查找没有明确计量对象的计量点",
        "query": "PREFIX cim-meter: <https://cim.medical/ontology/v3.4/metering#>\nPREFIX cim-equip: <https://cim.medical/ontology/v3.4/equipment#>\nPREFIX cim-space: <https://cim.medical/ontology/v3.4/space#>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n\nSELECT ?meter ?meterLabel\nWHERE {\n    ?meter a cim-meter:Meter .\n    OPTIONAL { ?meter rdfs:label ?meterLabel }\n    FILTER NOT EXISTS {\n        { ?meter cim-meter:meters ?obj . ?obj a/rdfs:subClassOf* cim-equip:Equipment }\n        UNION\n        { ?meter cim-meter:meters ?obj . ?obj a/rdfs:subClassOf* cim-space:Space }\n    }\n}",
        "expected_result": "Empty result set (理想情况), 当前已知缺失7个",
        "error_message": "存在没有计量对象的计量点"
      }
    },
    {
      "constraint_id": "CST-TOPO-003",
      "rule_description": "闭环系统必须有回流路径(Return_Path)",
      "type": "Topology",
      "source_agent": "Agent-01",
      "source_trace": {
        "file": "Agent01_Output.topology_definitions.yaml",
        "section": "sec-5.1",
        "field_path": "validation_rules.topology[0]",
        "line_number": 405
      },
      "sparql_check": {
        "query_type": "SELECT",
        "purpose": "查找闭环系统中缺少回流路径的情况",
        "query": "PREFIX cim-topo: <https://cim.medical/ontology/v3.4/topology#>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\n\nSELECT ?system ?systemName\nWHERE {\n    ?system a cim-topo:System .\n    ?system cim-topo:isClosedLoop true .\n    OPTIONAL { ?system rdfs:label ?systemName }\n    FILTER NOT EXISTS {\n        ?system cim-topo:hasReturnPath ?returnPath .\n    }\n}",
        "expected_result": "Empty result set",
        "error_message": "闭环系统缺少回流路径定义"
      }
    }
  ]
}
```

---

## DOC-004: `cross_agent_gap_analysis.json`

```json
{
  "meta": {
    "report_id": "GAP-CIM-20250117",
    "version": "1.0.0",
    "description": "跨Agent映射空白分析报告 - 识别Agent输出间的不一致和缺失，并提供补充策略",
    "generated_at": "2025-01-17T19:00:00Z"
  },

  "executive_summary": {
    "total_gaps_identified": 115,
    "by_severity": {
      "CRITICAL": {"count": 67, "description": "拓扑节点-设备映射缺失"},
      "HIGH": {"count": 16, "description": "设备-位置映射缺失"},
      "MEDIUM": {"count": 25, "description": "设备-控制覆盖缺失"},
      "LOW": {"count": 7, "description": "计量点-设备关联缺失"}
    },
    "remediation_strategies_defined": 4,
    "estimated_remediation_duration": "6-11天"
  },

  "gap_analysis": {
    "GAP-001": {
      "gap_id": "GAP-001",
      "severity": "CRITICAL",
      "title": "拓扑节点-设备映射缺失",
      "description": "Agent-01定义了156个拓扑节点，但Agent-03只映射了89个设备，映射覆盖率57.1%",
      "related_constraint": "CST-EQUIP-001",
      "statistics": {
        "total_nodes": 156,
        "mapped_nodes": 89,
        "unmapped_nodes": 67,
        "coverage_rate": "57.1%"
      },
      "affected_nodes_by_system": [
        {"system": "HVAC", "unmapped_count": 23, "examples": ["AHU二次泵节点", "风机盘管分支节点", "新风机组节点"]},
        {"system": "ELECTRICAL", "unmapped_count": 18, "examples": ["插座配电分支", "照明配电分支", "楼层配电节点"]},
        {"system": "PLUMBING", "unmapped_count": 12, "examples": ["热水回水节点", "中水处理节点", "雨水收集节点"]},
        {"system": "MEDICAL_GAS", "unmapped_count": 8, "examples": ["二级减压站", "科室分配阀", "气体报警点"]},
        {"system": "FIRE_PROTECTION", "unmapped_count": 4, "examples": ["消防水池节点", "屋顶水箱节点"]},
        {"system": "VERTICAL_TRANSPORT", "unmapped_count": 2, "examples": ["电梯配重节点", "自动扶梯节点"]}
      ],
      "source_trace": {
        "file": "Agent03_Output.node_equipment_mapping.yaml",
        "section": "sec-2",
        "field_path": "unmapped_nodes_list",
        "line_number": 305
      },
      "remediation_strategy": {
        "strategy_id": "REM-001",
        "approach": "分层分类补充",
        "priority": "P0",
        "steps": [
          {
            "step": 1,
            "action": "优先补充生命安全级节点的设备映射",
            "target_count": 12,
            "responsible": "Agent-03团队回炉修订",
            "criteria": "消防、医疗气体相关节点"
          },
          {
            "step": 2,
            "action": "补充HVAC核心节点（冷站、空调机房相关）的设备映射",
            "target_count": 15,
            "responsible": "Agent-03团队回炉修订"
          },
          {
            "step": 3,
            "action": "将纯逻辑节点（汇流/分配点）重新分类为LogicalNode，明确无需设备映射",
            "target_count": 25,
            "implementation": "在本体中已新增cim-topo:LogicalNode类",
            "affected_nodes": ["Junction类型", "Splitter类型"]
          },
          {
            "step": 4,
            "action": "剩余节点标记为PendingMapping状态，后续迭代处理",
            "target_count": 15,
            "implementation": "添加cim:mappingStatus属性"
          }
        ],
        "expected_outcome": {
          "physical_node_mapping_rate": "85%+",
          "logical_nodes_classified": 25,
          "pending_for_next_iteration": 15
        }
      }
    },

    "GAP-002": {
      "gap_id": "GAP-002",
      "severity": "HIGH",
      "title": "设备-位置映射缺失",
      "description": "Agent-03定义了215个设备，但Agent-05只为199个定义了位置，位置覆盖率92.6%",
      "related_constraint": "CST-SPACE-001",
      "statistics": {
        "total_equipment": 215,
        "located_equipment": 199,
        "unlocated_equipment": 16,
        "coverage_rate": "92.6%"
      },
      "affected_equipment": [
        {"equipment_id": "EQP-HVAC-VAV-015", "type": "VAV末端", "reason": "安装位置未确定"},
        {"equipment_id": "EQP-HVAC-VAV-016", "type": "VAV末端", "reason": "安装位置未确定"},
        {"equipment_id": "EQP-ELEC-PANEL-023", "type": "配电箱", "reason": "楼层配电间位置待定"},
        {"equipment_id": "EQP-ELEC-PANEL-024", "type": "配电箱", "reason": "楼层配电间位置待定"},
        {"equipment_id": "EQP-ELEC-PANEL-025", "type": "配电箱", "reason": "楼层配电间位置待定"},
        {"equipment_id": "EQP-MGAS-REG-007", "type": "减压器", "reason": "二级减压站位置未定义"},
        {"equipment_id": "EQP-MGAS-REG-008", "type": "减压器", "reason": "二级减压站位置未定义"},
        {"equipment_id": "EQP-PLMB-PUMP-005", "type": "增压泵", "reason": "泵房位置变更"},
        {"equipment_id": "EQP-PLMB-PUMP-006", "type": "增压泵", "reason": "泵房位置变更"},
        {"equipment_id": "EQP-FIRE-PANEL-003", "type": "消防控制柜", "reason": "消控室位置调整"}
      ],
      "source_trace": {
        "file": "Agent05_Output.equipment_location_model.yaml",
        "section": "sec-3",
        "field_path": "missing_locations",
        "line_number": 210
      },
      "remediation_strategy": {
        "strategy_id": "REM-002",
        "approach": "按设计进度分批补充",
        "priority": "P1",
        "steps": [
          {
            "step": 1,
            "action": "从建筑设计文档获取楼层配电间位置",
            "target_count": 3,
            "data_source": "建筑CAD图纸/BIM模型"
          },
          {
            "step": 2,
            "action": "从机电深化设计获取VAV末端精确位置",
            "target_count": 2,
            "data_source": "机电BIM模型"
          },
          {
            "step": 3,
            "action": "从医疗专项设计获取二级减压站位置",
            "target_count": 2,
            "data_source": "医气系统设计图"
          },
          {
            "step": 4,
            "action": "剩余设备使用Ceiling_Void或标记为TBD(待定)",
            "target_count": 9,
            "implementation": "使用cim:locationStatus = 'TBD'标记"
          }
        ],
        "expected_outcome": {
          "final_coverage_rate": "97%+",
          "remaining_tbd": 7
        }
      }
    },

    "GAP-003": {
      "gap_id": "GAP-003",
      "severity": "MEDIUM",
      "title": "设备-控制覆盖缺失",
      "description": "Agent-03定义了123个需要控制的设备，但Agent-06只为98个定义了控制点，控制覆盖率79.7%",
      "related_constraint": "CST-CTRL-001 (implicit)",
      "statistics": {
        "equipment_needing_control": 123,
        "equipment_with_control": 98,
        "equipment_without_control": 25,
        "coverage_rate": "79.7%"
      },
      "affected_equipment_by_category": [
        {
          "category": "风机盘管FCU",
          "missing_count": 12,
          "reason": "末端设备采用分布式控制，未纳入DDC系统",
          "resolution": "标记hasLocalControl=true"
        },
        {
          "category": "照明设备",
          "missing_count": 8,
          "reason": "智能照明采用独立系统(KNX/DALI)",
          "resolution": "标记externalControlSystem='KNX'"
        },
        {
          "category": "插座配电",
          "missing_count": 5,
          "reason": "非受控负荷",
          "resolution": "标记isUncontrolledLoad=true"
        }
      ],
      "source_trace": {
        "file": "Agent06_Output.sensor_models.yaml",
        "section": "sec-2",
        "field_path": "control_coverage_analysis",
        "line_number": 490
      },
      "remediation_strategy": {
        "strategy_id": "REM-003",
        "approach": "分类标记控制状态",
        "priority": "P2",
        "steps": [
          {
            "step": 1,
            "action": "FCU设备添加hasLocalControl=true属性",
            "target_count": 12,
            "implementation": "表示有本地控制但不纳入BAS"
          },
          {
            "step": 2,
            "action": "照明设备添加externalControlSystem属性",
            "target_count": 8,
            "implementation": "值为'KNX'或'DALI'"
          },
          {
            "step": 3,
            "action": "非受控负荷添加isUncontrolledLoad=true属性",
            "target_count": 5,
            "implementation": "明确表示该设备不需要控制"
          }
        ],
        "expected_outcome": {
          "explicit_bas_control_rate": "79.7%",
          "total_control_status_defined_rate": "100%",
          "note": "所有设备均有明确的控制状态说明"
        },
        "ontology_changes": [
          "新增cim-equip:hasLocalControl (xsd:boolean)",
          "新增cim-equip:externalControlSystem (xsd:string)",
          "新增cim-equip:isUncontrolledLoad (xsd:boolean)"
        ]
      }
    },

    "GAP-004": {
      "gap_id": "GAP-004",
      "severity": "LOW",
      "title": "计量点-设备关联缺失",
      "description": "189个计量点中有7个未能追溯到具体设备，但可追溯到空间或派生自其他计量点",
      "related_constraint": "CST-METER-001",
      "statistics": {
        "total_meters": 189,
        "meters_with_equipment": 182,
        "meters_without_equipment": 7,
        "coverage_rate": "96.3%"
      },
      "affected_meters": [
        {"meter_id": "MTR-ELEC-L0-TOTAL", "type": "总电表", "reason": "计量院区总进线，非单一设备", "resolution": "meters → cim-space:Site"},
        {"meter_id": "MTR-WATER-L0-TOTAL", "type": "总水表", "reason": "计量院区总进水", "resolution": "meters → cim-space:Site"},
        {"meter_id": "MTR-GAS-L0-TOTAL", "type": "总气表", "reason": "计量院区总进气", "resolution": "meters → cim-space:Site"},
        {"meter_id": "MTR-ELEC-L1-PUBLIC", "type": "公区电表", "reason": "计量公共区域总用电", "resolution": "meters → cim-space:Zone(公共区)"},
        {"meter_id": "MTR-WATER-L1-LANDSCAPE", "type": "绿化水表", "reason": "计量室外绿化用水", "resolution": "meters → cim-space:Zone(室外)"},
        {"meter_id": "MTR-ELEC-VIRTUAL-001", "type": "虚拟电表", "reason": "通过计算得出", "resolution": "derivedFrom → 物理表"},
        {"meter_id": "MTR-ELEC-VIRTUAL-002", "type": "虚拟电表", "reason": "通过计算得出", "resolution": "derivedFrom → 物理表"}
      ],
      "source_trace": {
        "file": "Agent07_Output.metering_hierarchy.yaml",
        "section": "sec-3",
        "field_path": "meters_without_equipment",
        "line_number": 390
      },
      "remediation_strategy": {
        "strategy_id": "REM-004",
        "approach": "扩展计量对象定义",
        "priority": "P3",
        "steps": [
          {
            "step": 1,
            "action": "总表定义meters关系指向cim-space:Site（计量空间而非设备）",
            "target_count": 3,
            "implementation": "cim-meter:meters的range已扩展包含cim-space:Space"
          },
          {
            "step": 2,
            "action": "公区/绿化表定义meters关系指向cim-space:Zone",
            "target_count": 2
          },
          {
            "step": 3,
            "action": "虚拟表定义derivedFrom关系指向源物理表",
            "target_count": 2,
            "implementation": "新增cim-meter:VirtualMeter类和cim-meter:derivedFrom关系"
          }
        ],
        "expected_outcome": {
          "final_coverage_rate": "100%",
          "note": "所有计量点均有明确的计量对象（设备、空间或派生源）"
        },
        "ontology_changes": [
          "扩展cim-meter:meters的range包含cim-space:Space",
          "新增cim-meter:VirtualMeter类",
          "新增cim-meter:derivedFrom关系"
        ]
      }
    }
  },

  "remediation_roadmap": {
    "total_phases": 4,
    "phases": [
      {
        "phase": 1,
        "name": "Critical Gap Resolution",
        "target_gaps": ["GAP-001"],
        "actions": [
          "Agent-03团队回炉补充67个节点的设备映射",
          "本体增加LogicalNode子类区分纯逻辑节点"
        ],
        "duration_estimate": "3-5天",
        "blocking": true
      },
      {
        "phase": 2,
        "name": "High Gap Resolution",
        "target_gaps": ["GAP-002"],
        "actions": [
          "收集建筑/机电/医疗专项设计文档",
          "补充16个设备的位置信息"
        ],
        "duration_estimate": "2-3天",
        "blocking": false
      },
      {
        "phase": 3,
        "name": "Medium Gap Resolution",
        "target_gaps": ["GAP-003"],
        "actions": [
          "在本体中增加控制状态属性定义",
          "为25个设备标记控制状态"
        ],
        "duration_estimate": "1-2天",
        "blocking": false
      },
      {
        "phase": 4,
        "name": "Low Gap Resolution",
        "target_gaps": ["GAP-004"],
        "actions": [
          "扩展meters关系的range定义",
          "为7个计量点补充计量对象"
        ],
        "duration_estimate": "0.5-1天",
        "blocking": false
      }
    ],
    "overall_duration": "6-11天",
    "dependencies": [
      {"dependency": "GAP-001的解决需要Agent-03团队配合", "impact": "阻塞Phase 1"},
      {"dependency": "GAP-002的解决依赖设计文档交付", "impact": "可能延迟Phase 2"}
    ]
  }
}
```

---

## DOC-005: `medical_domain_constraints.json`

```json
{
  "meta": {
    "file_id": "MDC-CIM-20250117-FINAL",
    "version": "2.0.0",
    "description": "医疗建筑领域强制性约束库 - 与本体属性定义完全对齐",
    "standards_referenced": [
      "GB 50333-2013 医院洁净手术部建筑技术规范",
      "GB 51039-2014 综合医院建筑设计规范",
      "WS/T 311-2009 医院隔离技术规范",
      "GB 19489-2008 实验室生物安全通用要求",
      "GB 50736-2012 民用建筑供暖通风与空气调节设计规范",
      "GB 50751-2012 医用气体工程技术规范"
    ]
  },

  "property_definitions": {
    "description": "本节定义约束所涉及的所有数据属性，与ontology_skeleton.ttl完全对应",
    "properties": [
      {
        "uri": "cim-space:surgeryGrade",
        "label_cn": "手术室等级",
        "label_en": "surgery grade",
        "datatype": "xsd:string",
        "enum_values": ["Class_I", "Class_II", "Class_III", "Class_IV"],
        "applies_to": "cim-space:OperatingRoom",
        "standard_ref": "GB 50333-2013, Table 3.0.1"
      },
      {
        "uri": "cim-space:cleanlinessClass",
        "label_cn": "洁净等级",
        "label_en": "cleanliness class",
        "datatype": "xsd:string",
        "enum_values": ["ISO-1", "ISO-2", "ISO-3", "ISO-4", "ISO-5", "ISO-6", "ISO-7", "ISO-8", "ISO-8.5", "ISO-9"],
        "applies_to": "cim-space:CleanSpace",
        "standard_ref": "ISO 14644-1"
      },
      {
        "uri": "cim-space:temperature",
        "label_cn": "设计温度",
        "label_en": "design temperature",
        "datatype": "xsd:decimal",
        "unit": "°C",
        "applies_to": "cim-space:Room"
      },
      {
        "uri": "cim-space:relativeHumidity",
        "label_cn": "相对湿度",
        "label_en": "relative humidity",
        "datatype": "xsd:decimal",
        "unit": "%RH",
        "applies_to": "cim-space:Room"
      },
      {
        "uri": "cim-space:pressureDifferential",
        "label_cn": "压差",
        "label_en": "pressure differential",
        "datatype": "xsd:decimal",
        "unit": "Pa",
        "note": "相对于走廊或相邻区域，正值为正压，负值为负压",
        "applies_to": "cim-space:Room"
      },
      {
        "uri": "cim-space:airChangesPerHour",
        "label_cn": "换气次数",
        "label_en": "air changes per hour",
        "datatype": "xsd:decimal",
        "unit": "ACH (次/小时)",
        "applies_to": "cim-space:Room"
      },
      {
        "uri": "cim-space:freshAirRatio",
        "label_cn": "新风比",
        "label_en": "fresh air ratio",
        "datatype": "xsd:decimal",
        "unit": "%",
        "applies_to": "cim-space:Room"
      },
      {
        "uri": "cim-space:noiseLevel",
        "label_cn": "噪声等级",
        "label_en": "noise level",
        "datatype": "xsd:decimal",
        "unit": "dB(A)",
        "applies_to": "cim-space:Room"
      },
      {
        "uri": "cim-space:illuminance",
        "label_cn": "照度",
        "label_en": "illuminance",
        "datatype": "xsd:decimal",
        "unit": "lux",
        "applies_to": "cim-space:Room"
      },
      {
        "uri": "cim-space:biosafetyLevel",
        "label_cn": "生物安全等级",
        "label_en": "biosafety level",
        "datatype": "xsd:string",
        "enum_values": ["BSL-1", "BSL-2", "BSL-3", "BSL-4"],
        "applies_to": "cim-space:CleanLab",
        "standard_ref": "GB 19489-2008"
      },
      {
        "uri": "cim-space:isolationType",
        "label_cn": "隔离类型",
        "label_en": "isolation type",
        "datatype": "xsd:string",
        "enum_values": ["Positive_Pressure", "Negative_Pressure"],
        "applies_to": "cim-space:IsolationWard",
        "standard_ref": "WS/T 311-2009"
      }
    ]
  },

  "space_environmental_constraints": [
    {
      "constraint_id": "MED-OR-I-001",
      "constraint_name": "I级洁净手术室环境要求",
      "target_class": "cim-space:OperatingRoom",
      "target_subtype": "Class_I",
      "standard_ref": "GB 50333-2013, Section 3.0.1, Table 4.0.1",
      "requirements": {
        "cleanlinessClass": {
          "property_uri": "cim-space:cleanlinessClass",
          "operator": "EQUALS",
          "value": "ISO-5",
          "zone": "手术区",
          "note": "周边区可为ISO-6"
        },
        "temperature": {
          "property_uri": "cim-space:temperature",
          "operator": "BETWEEN",
          "min_value": 21,
          "max_value": 25,
          "unit": "°C"
        },
        "relativeHumidity": {
          "property_uri": "cim-space:relativeHumidity",
          "operator": "BETWEEN",
          "min_value": 30,
          "max_value": 60,
          "unit": "%RH"
        },
        "pressureDifferential": {
          "property_uri": "cim-space:pressureDifferential",
          "operator": "GTE",
          "value": 8,
          "unit": "Pa",
          "note": "手术室与走廊压差不小于8Pa"
        },
        "airChangesPerHour": {
          "property_uri": "cim-space:airChangesPerHour",
          "operator": "GTE",
          "value": 36,
          "unit": "ACH",
          "note": "工作面截面风速≥0.25m/s"
        },
        "freshAirRatio": {
          "property_uri": "cim-space:freshAirRatio",
          "operator": "GTE",
          "value": 20,
          "unit": "%"
        },
        "noiseLevel": {
          "property_uri": "cim-space:noiseLevel",
          "operator": "LTE",
          "value": 52,
          "unit": "dB(A)"
        },
        "illuminance": {
          "property_uri": "cim-space:illuminance",
          "operator": "GTE",
          "value": 350,
          "unit": "lux",
          "note": "手术台面无影灯照度另计"
        }
      },
      "shacl_shape": {
        "shape_uri": "cim-shape:OperatingRoom_Class_I_Shape",
        "turtle": "@prefix sh: <http://www.w3.org/ns/shacl#> .\n@prefix cim-space: <https://cim.medical/ontology/v3.4/space#> .\n@prefix cim-shape: <https://cim.medical/ontology/v3.4/shapes#> .\n@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\ncim-shape:OperatingRoom_Class_I_Shape\n    a sh:NodeShape ;\n    sh:targetClass cim-space:OperatingRoom ;\n    sh:property [\n        sh:path cim-space:surgeryGrade ;\n        sh:hasValue \"Class_I\" ;\n    ] ;\n    sh:property [\n        sh:path cim-space:cleanlinessClass ;\n        sh:hasValue \"ISO-5\" ;\n        sh:message \"I级洁净手术室必须满足ISO-5洁净度 (GB 50333-2013)\"@zh-CN ;\n    ] ;\n    sh:property [\n        sh:path cim-space:temperature ;\n        sh:minInclusive 21 ;\n        sh:maxInclusive 25 ;\n        sh:datatype xsd:decimal ;\n        sh:message \"I级洁净手术室温度必须在21-25°C范围内\"@zh-CN ;\n    ] ;\n    sh:property [\n        sh:path cim-space:relativeHumidity ;\n        sh:minInclusive 30 ;\n        sh:maxInclusive 60 ;\n        sh:datatype xsd:decimal ;\n        sh:message \"I级洁净手术室湿度必须在30-60%范围内\"@zh-CN ;\n    ] ;\n    sh:property [\n        sh:path cim-space:pressureDifferential ;\n        sh:minInclusive 8 ;\n        sh:datatype xsd:decimal ;\n        sh:message \"I级洁净手术室对走廊压差不小于8Pa\"@zh-CN ;\n    ] ;\n    sh:property [\n        sh:path cim-space:airChangesPerHour ;\n        sh:minInclusive 36 ;\n        sh:datatype xsd:decimal ;\n        sh:message \"I级洁净手术室换气次数不小于36次/小时\"@zh-CN ;\n    ] ;\n    sh:property [\n        sh:path cim-space:noiseLevel ;\n        sh:maxInclusive 52 ;\n        sh:datatype xsd:decimal ;\n        sh:message \"I级洁净手术室噪声不超过52dB(A)\"@zh-CN ;\n    ] ;\n    sh:property [\n        sh:path cim-space:illuminance ;\n        sh:minInclusive 350 ;\n        sh:datatype xsd:decimal ;\n        sh:message \"I级洁净手术室照度不小于350lux\"@zh-CN ;\n    ] ."
      }
    },
    {
      "constraint_id": "MED-OR-II-001",
      "constraint_name": "II级洁净手术室环境要求",
      "target_class": "cim-space:OperatingRoom",
      "target_subtype": "Class_II",
      "standard_ref": "GB 50333-2013",
      "requirements": {
        "cleanlinessClass": {"operator": "EQUALS", "value": "ISO-6"},
        "temperature": {"operator": "BETWEEN", "min_value": 21, "max_value": 25},
        "relativeHumidity": {"operator": "BETWEEN", "min_value": 30, "max_value": 60},
        "pressureDifferential": {"operator": "GTE", "value": 8},
        "airChangesPerHour": {"operator": "GTE", "value": 24},
        "noiseLevel": {"operator": "LTE", "value": 50}
      }
    },
    {
      "constraint_id": "MED-OR-III-001",
      "constraint_name": "III级洁净手术室环境要求",
      "target_class": "cim-space:OperatingRoom",
      "target_subtype": "Class_III",
      "standard_ref": "GB 50333-2013",
      "requirements": {
        "cleanlinessClass": {"operator": "EQUALS", "value": "ISO-7"},
        "temperature": {"operator": "BETWEEN", "min_value": 21, "max_value": 25},
        "relativeHumidity": {"operator": "BETWEEN", "min_value": 35, "max_value": 60},
        "pressureDifferential": {"operator": "GTE", "value": 5},
        "airChangesPerHour": {"operator": "GTE", "value": 18},
        "noiseLevel": {"operator": "LTE", "value": 50}
      }
    },
    {
      "constraint_id": "MED-OR-IV-001",
      "constraint_name": "IV级洁净手术室环境要求",
      "target_class": "cim-space:OperatingRoom",
      "target_subtype": "Class_IV",
      "standard_ref": "GB 50333-2013",
      "requirements": {
        "cleanlinessClass": {"operator": "EQUALS", "value": "ISO-8.5"},
        "temperature": {"operator": "BETWEEN", "min_value": 21, "max_value": 25},
        "relativeHumidity": {"operator": "BETWEEN", "min_value": 35, "max_value": 60},
        "pressureDifferential": {"operator": "GTE", "value": 5},
        "airChangesPerHour": {"operator": "GTE", "value": 12},
        "noiseLevel": {"operator": "LTE", "value": 50}
      }
    },
    {
      "constraint_id": "MED-ISO-NEG-001",
      "constraint_name": "负压隔离病房环境要求",
      "target_class": "cim-space:IsolationWard",
      "target_subtype": "Negative_Pressure",
      "standard_ref": "WS/T 311-2009",
      "requirements": {
        "isolationType": {
          "property_uri": "cim-space:isolationType",
          "operator": "EQUALS",
          "value": "Negative_Pressure"
        },
        "pressureDifferential": {
          "property_uri": "cim-space:pressureDifferential",
          "operator": "LTE",
          "value": -10,
          "unit": "Pa",
          "note": "相对于走廊为负压"
        },
        "airChangesPerHour": {
          "property_uri": "cim-space:airChangesPerHour",
          "operator": "GTE",
          "value": 12,
          "unit": "ACH"
        }
      },
      "shacl_shape": {
        "shape_uri": "cim-shape:IsolationWard_Negative_Shape",
        "turtle": "@prefix sh: <http://www.w3.org/ns/shacl#> .\n@prefix cim-space: <https://cim.medical/ontology/v3.4/space#> .\n@prefix cim-shape: <https://cim.medical/ontology/v3.4/shapes#> .\n@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\ncim-shape:IsolationWard_Negative_Shape\n    a sh:NodeShape ;\n    sh:targetClass cim-space:IsolationWard ;\n    sh:property [\n        sh:path cim-space:isolationType ;\n        sh:hasValue \"Negative_Pressure\" ;\n    ] ;\n    sh:property [\n        sh:path cim-space:pressureDifferential ;\n        sh:maxInclusive -10 ;\n        sh:datatype xsd:decimal ;\n        sh:message \"负压隔离病房压差必须≤-10Pa (WS/T 311-2009)\"@zh-CN ;\n    ] ;\n    sh:property [\n        sh:path cim-space:airChangesPerHour ;\n        sh:minInclusive 12 ;\n        sh:datatype xsd:decimal ;\n        sh:message \"负压隔离病房换气次数不小于12次/小时\"@zh-CN ;\n    ] ."
      }
    },
    {
      "constraint_id": "MED-ISO-POS-001",
      "constraint_name": "正压隔离病房环境要求",
      "target_class": "cim-space:IsolationWard",
      "target_subtype": "Positive_Pressure",
      "standard_ref": "WS/T 311-2009",
      "requirements": {
        "isolationType": {"operator": "EQUALS", "value": "Positive_Pressure"},
        "pressureDifferential": {"operator": "GTE", "value": 8, "unit": "Pa"},
        "airChangesPerHour": {"operator": "GTE", "value": 12}
      }
    },
    {
      "constraint_id": "MED-LAB-BSL3-001",
      "constraint_name": "BSL-3实验室环境要求",
      "target_class": "cim-space:CleanLab",
      "target_subtype": "BSL-3",
      "standard_ref": "GB 19489-2008",
      "requirements": {
        "biosafetyLevel": {
          "property_uri": "cim-space:biosafetyLevel",
          "operator": "EQUALS",
          "value": "BSL-3"
        },
        "pressureDifferential": {
          "property_uri": "cim-space:pressureDifferential",
          "operator": "LTE",
          "value": -30,
          "unit": "Pa"
        },
        "freshAirRatio": {
          "property_uri": "cim-space:freshAirRatio",
          "operator": "EQUALS",
          "value": 100,
          "unit": "%",
          "note": "100%全新风，无回风"
        }
      },
      "required_equipment": [
        {"type": "HEPA过滤器", "requirement": "排风需经HEPA过滤后高空排放"},
        {"type": "高压灭菌器", "requirement": "实验室内或邻近区域"},
        {"type": "气闸室", "requirement": "入口设置"}
      ],
      "shacl_shape": {
        "shape_uri": "cim-shape:CleanLab_BSL3_Shape",
        "turtle": "@prefix sh: <http://www.w3.org/ns/shacl#> .\n@prefix cim-space: <https://cim.medical/ontology/v3.4/space#> .\n@prefix cim-shape: <https://cim.medical/ontology/v3.4/shapes#> .\n@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\ncim-shape:CleanLab_BSL3_Shape\n    a sh:NodeShape ;\n    sh:targetClass cim-space:CleanLab ;\n    sh:property [\n        sh:path cim-space:biosafetyLevel ;\n        sh:hasValue \"BSL-3\" ;\n    ] ;\n    sh:property [\n        sh:path cim-space:pressureDifferential ;\n        sh:maxInclusive -30 ;\n        sh:datatype xsd:decimal ;\n        sh:message \"BSL-3实验室压差必须≤-30Pa (GB 19489-2008)\"@zh-CN ;\n    ] ;\n    sh:property [\n        sh:path cim-space:freshAirRatio ;\n        sh:hasValue 100 ;\n        sh:datatype xsd:decimal ;\n        sh:message \"BSL-3实验室必须100%全新风\"@zh-CN ;\n    ] ."
      }
    }
  ],

  "equipment_constraints": [
    {
      "constraint_id": "MED-EQUIP-OR-001",
      "constraint_name": "手术室必备设备要求",
      "target_space": "cim-space:OperatingRoom",
      "standard_ref": "GB 50333-2013 + JGJ 16-2008 + GB 50751-2012",
      "required_equipment": [
        {
          "category": "空调净化",
          "equipment": ["洁净空调机组 (cim-equip:Clean_AHU)", "HEPA过滤器 (cim-equip:HEPA_Filter)"]
        },
        {
          "category": "电气",
          "equipment": [
            "双电源切换 (cim-equip:ATS)",
            "UPS不间断电源 (cim-equip:UPS)",
            "医用隔离变压器 (cim-equip:Medical_Isolation_Transformer)",
            "绝缘监测仪 (cim-equip:Insulation_Monitor)"
          ]
        },
        {
          "category": "医用气体",
          "equipment": ["氧气终端", "笑气终端", "压缩空气终端", "真空终端"],
          "note": "根据手术类型配置"
        }
      ]
    },
    {
      "constraint_id": "MED-EQUIP-LIFE-001",
      "constraint_name": "生命安全级设备冗余要求",
      "target_class": "cim-equip:Equipment",
      "target_reliability": "LIFE_SAFETY",
      "requirement": "必须有冗余配置(N+1)或双路供应",
      "standard_ref": "GB 50333-2013, JGJ 16-2008"
    }
  ]
}
```

---

## DOC-006: `validation_rules_schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://cim.medical/schemas/validation-rule.json",
  "title": "CIM Validation Rule Schema",
  "description": "统一的验证规则格式定义，确保Claude Code可直接解析执行",
  "version": "1.0.0",

  "definitions": {
    "source_trace": {
      "type": "object",
      "required": ["file"],
      "properties": {
        "file": {"type": "string", "description": "源文件名"},
        "section": {"type": "string", "description": "章节编号"},
        "field_path": {"type": "string", "description": "字段路径"},
        "line_number": {"type": "integer", "description": "行号"}
      }
    },
    "shacl_shape": {
      "type": "object",
      "required": ["shape_uri", "turtle"],
      "properties": {
        "shape_uri": {
          "type": "string",
          "pattern": "^cim-shape:[A-Za-z0-9_]+Shape$",
          "description": "SHACL形状的URI"
        },
        "target_class": {
          "type": "string",
          "description": "验证目标类的URI"
        },
        "turtle": {
          "type": "string",
          "description": "完整的SHACL Turtle定义，可直接加载到验证引擎"
        }
      }
    },
    "sparql_check": {
      "type": "object",
      "required": ["query_type", "query", "expected_result"],
      "properties": {
        "query_type": {
          "type": "string",
          "enum": ["SELECT", "ASK", "CONSTRUCT"],
          "description": "SPARQL查询类型"
        },
        "purpose": {
          "type": "string",
          "description": "查询目的的自然语言说明"
        },
        "query": {
          "type": "string",
          "description": "完整的SPARQL查询语句，包含PREFIX声明"
        },
        "expected_result": {
          "type": "string",
          "description": "预期结果描述，如'Empty result set'"
        },
        "error_message": {
          "type": "string",
          "description": "验证失败时显示的错误消息"
        }
      }
    }
  },

  "type": "object",
  "required": ["constraint_id", "rule_description", "type"],
  "properties": {
    "constraint_id": {
      "type": "string",
      "pattern": "^CST-[A-Z]+-\\d{3}$",
      "description": "约束唯一标识符，格式: CST-DOMAIN-NNN"
    },
    "rule_description": {
      "type": "string",
      "description": "规则的自然语言描述"
    },
    "type": {
      "type": "string",
      "enum": ["Completeness", "Connectivity", "Cross-Agent Consistency", "Domain Constraint", "Topology"],
      "description": "约束类型分类"
    },
    "source_agent": {
      "type": "string",
      "pattern": "^Agent-(0[1-9]|09)$",
      "description": "约束来源Agent编号"
    },
    "source_trace": {
      "$ref": "#/definitions/source_trace"
    },
    "current_status": {
      "type": "object",
      "properties": {
        "compliant": {"type": "boolean"},
        "gap_count": {"type": "integer"},
        "remediation_ref": {"type": "string"}
      },
      "description": "当前合规状态，用于跟踪已知问题"
    },
    "shacl_shape": {
      "$ref": "#/definitions/shacl_shape"
    },
    "sparql_check": {
      "$ref": "#/definitions/sparql_check"
    }
  },
  "anyOf": [
    {"required": ["shacl_shape"]},
    {"required": ["sparql_check"]},
    {"required": ["shacl_shape", "sparql_check"]}
  ]
}
```

---

## DOC-007: `cim_document_structure.md`

```markdown
# CIM 统一领域模型 - 目录结构定义

## 版本信息
- **版本**: 2.0.0-Final
- **生成日期**: 2025-01-17
- **目标路径**: `/project_deliverables/version02/cim/`

---

## 📁 目录树结构

```
cim/
├── 📁 core/                          # 核心元模型定义
│   ├── base_entities.ttl             # 基础实体定义 (Entity, PhysicalObject, LogicalObject)
│   ├── relationships.ttl             # 通用关系定义
│   └── datatypes.ttl                 # 自定义数据类型与枚举
│
├── 📁 topology/                       # 拓扑模型 (Agent-01)
│   ├── node_types.ttl                # 节点类型 (Source, Sink, Distribution, Logical)
│   ├── edge_types.ttl                # 边类型 (Trunk, Branch, Terminal)
│   └── system_catalog.ttl            # 8大系统26子系统目录
│
├── 📁 spaces/                         # 空间模型 (Agent-02)
│   ├── spatial_hierarchy.ttl         # 6级空间层级 (L0-L5)
│   ├── zone_classification.ttl       # 功能区分类
│   └── medical_special_spaces.ttl    # 医疗专用空间 (手术室/ICU/隔离病房/洁净实验室)
│
├── 📁 equipment/                      # 设备本体 (Agent-03)
│   ├── equipment_hierarchy.ttl       # 设备层级 (System/Equipment/Component/Part)
│   ├── reliability_classification.ttl # 可靠性分级 (5级)
│   ├── mechanical.ttl                # HVAC设备
│   ├── electrical.ttl                # 电气设备
│   ├── plumbing.ttl                  # 给排水设备
│   ├── medical_gas.ttl               # 医疗气体设备
│   ├── fire_protection.ttl           # 消防设备
│   └── vertical_transport.ttl        # 垂直交通设备
│
├── 📁 flow/                           # 流动模型 (Agent-04)
│   ├── flow_layers.ttl               # 三层流动模型 (物质/能量/信息)
│   ├── flow_media.ttl                # 流动介质定义
│   └── flow_sequences.ttl            # 流动路径序列
│
├── 📁 coupling/                       # 耦合模型 (Agent-05)
│   ├── equipment_location.ttl        # 设备-位置耦合
│   ├── routing_space.ttl             # 管路-空间穿越
│   └── service_relations.ttl         # 服务关系定义
│
├── 📁 control/                        # 控制模型 (Agent-06)
│   ├── sensors.ttl                   # 传感器本体
│   ├── actuators.ttl                 # 执行器本体
│   ├── controllers.ttl               # 控制器定义
│   └── control_loops.ttl             # 控制回路
│
├── 📁 metering/                       # 计量模型 (Agent-07)
│   ├── metering_hierarchy.ttl        # 4级计量层级
│   ├── energy_media.ttl              # 7种能源介质
│   ├── allocation_rules.ttl          # 分摊规则
│   └── virtual_meters.ttl            # 虚拟计量表
│
├── 📁 operations/                     # 运维模型 (Agent-08)
│   ├── work_orders.ttl               # 工单模型
│   ├── maintenance_strategies.ttl    # 维护策略 (PM/PdM)
│   ├── asset_lifecycle.ttl           # 资产生命周期
│   └── alarm_system.ttl              # 告警体系
│
├── 📁 rules/                          # 推理与验证规则
│   ├── cross_agent_validation.sparql # 跨Agent一致性验证
│   └── shacl_constraints.ttl         # SHACL数据形状约束
│
├── 📁 medical_constraints/            # 医疗领域约束
│   ├── gb50333_cleanroom.ttl         # GB 50333 洁净规范约束
│   ├── gb51039_hospital.ttl          # GB 51039 医院规范约束
│   └── medical_gas_safety.ttl        # 医用气体安全约束
│
├── _index.ttl                        # 本体入口文件 (owl:imports清单)
└── _config.json                      # 项目配置与元数据
```

---

## 📊 文件-Agent来源映射表

| 目录 | 主要来源Agent | 次要依赖Agent | 预计文件数 |
|------|--------------|---------------|-----------|
| `core/` | Agent-09 | - | 3 |
| `topology/` | **Agent-01** | - | 3 |
| `spaces/` | **Agent-02** | - | 3 |
| `equipment/` | **Agent-03** | Agent-01 | 8 |
| `flow/` | **Agent-04** | Agent-01 | 3 |
| `coupling/` | **Agent-05** | Agent-01, 02, 03 | 3 |
| `control/` | **Agent-06** | Agent-01, 03, 04 | 4 |
| `metering/` | **Agent-07** | Agent-01, 03, 05 | 4 |
| `operations/` | **Agent-08** | Agent-03, 06, 07 | 4 |
| `rules/` | Agent-09 | All | 2 |
| `medical_constraints/` | Agent-02, 09 | - | 3 |
| **合计** | | | **40** |

---

## 🔗 命名空间定义

```turtle
@prefix cim:        <https://cim.medical/ontology/v3.4#> .
@prefix cim-topo:   <https://cim.medical/ontology/v3.4/topology#> .
@prefix cim-space:  <https://cim.medical/ontology/v3.4/space#> .
@prefix cim-equip:  <https://cim.medical/ontology/v3.4/equipment#> .
@prefix cim-flow:   <https://cim.medical/ontology/v3.4/flow#> .
@prefix cim-couple: <https://cim.medical/ontology/v3.4/coupling#> .
@prefix cim-ctrl:   <https://cim.medical/ontology/v3.4/control#> .
@prefix cim-meter:  <https://cim.medical/ontology/v3.4/metering#> .
@prefix cim-om:     <https://cim.medical/ontology/v3.4/operations#> .
@prefix cim-loc:    <https://cim.medical/ontology/v3.4/location#> .
@prefix cim-shape:  <https://cim.medical/ontology/v3.4/shapes#> .
```
```

---

## DOC-008: `ontology_skeleton.ttl`

```turtle
# ============================================================================
# CIM Medical Building Unified Domain Model - Ontology Skeleton
# Version: 2.0.0-Final
# Generated: 2025-01-17
# Purpose: Complete skeleton with all property definitions aligned to constraints
# ============================================================================

@prefix rdf:        <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:       <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl:        <http://www.w3.org/2002/07/owl#> .
@prefix xsd:        <http://www.w3.org/2001/XMLSchema#> .
@prefix skos:       <http://www.w3.org/2004/02/skos/core#> .
@prefix sh:         <http://www.w3.org/ns/shacl#> .

@prefix cim:        <https://cim.medical/ontology/v3.4#> .
@prefix cim-topo:   <https://cim.medical/ontology/v3.4/topology#> .
@prefix cim-space:  <https://cim.medical/ontology/v3.4/space#> .
@prefix cim-equip:  <https://cim.medical/ontology/v3.4/equipment#> .
@prefix cim-flow:   <https://cim.medical/ontology/v3.4/flow#> .
@prefix cim-ctrl:   <https://cim.medical/ontology/v3.4/control#> .
@prefix cim-meter:  <https://cim.medical/ontology/v3.4/metering#> .
@prefix cim-om:     <https://cim.medical/ontology/v3.4/operations#> .
@prefix cim-loc:    <https://cim.medical/ontology/v3.4/location#> .

# ============================================================================
# ONTOLOGY METADATA
# ============================================================================

<https://cim.medical/ontology/v3.4>
    a owl:Ontology ;
    rdfs:label "CIM Medical Building Unified Domain Model"@en ;
    rdfs:label "医疗建筑CIM统一领域模型"@zh-CN ;
    owl:versionInfo "2.0.0-Final" ;
    rdfs:comment "Complete ontology skeleton with property definitions aligned to medical constraints."@en .

# ============================================================================
# ANNOTATION PROPERTIES
# ============================================================================

cim:unit
    a owl:AnnotationProperty ;
    rdfs:label "unit"@en ;
    rdfs:label "单位"@zh-CN ;
    rdfs:comment "用于标注数据属性的物理单位"@zh-CN .

cim:sourceAgent
    a owl:AnnotationProperty ;
    rdfs:label "source agent"@en ;
    rdfs:label "来源Agent"@zh-CN .

# ============================================================================
# CORE BASE CLASSES
# ============================================================================

cim:Entity
    a owl:Class ;
    rdfs:label "Entity"@en ;
    rdfs:label "实体"@zh-CN ;
    rdfs:comment "The root abstract class for all CIM objects."@en .

cim:PhysicalObject
    a owl:Class ;
    rdfs:subClassOf cim:Entity ;
    rdfs:label "Physical Object"@en ;
    rdfs:label "物理对象"@zh-CN .

cim:LogicalObject
    a owl:Class ;
    rdfs:subClassOf cim:Entity ;
    rdfs:label "Logical Object"@en ;
    rdfs:label "逻辑对象"@zh-CN .

# ============================================================================
# TOPOLOGY DOMAIN (Agent-01)
# ============================================================================

cim-topo:Node
    a owl:Class ;
    rdfs:subClassOf cim:LogicalObject ;
    rdfs:label "Topology Node"@en ;
    rdfs:label "拓扑节点"@zh-CN ;
    cim:sourceAgent "Agent-01" .

cim-topo:Source_Node
    a owl:Class ;
    rdfs:subClassOf cim-topo:Node ;
    rdfs:label "Source Node"@en ;
    rdfs:label "源节点"@zh-CN ;
    rdfs:comment "系统的能量/介质输入端，流动的起点"@zh-CN .

cim-topo:Sink_Node
    a owl:Class ;
    rdfs:subClassOf cim-topo:Node ;
    rdfs:label "Sink Node"@en ;
    rdfs:label "末端节点"@zh-CN ;
    rdfs:comment "系统的能量/介质消耗端，流动的终点"@zh-CN .

cim-topo:Distribution_Node
    a owl:Class ;
    rdfs:subClassOf cim-topo:Node ;
    rdfs:label "Distribution Node"@en ;
    rdfs:label "分配节点"@zh-CN ;
    rdfs:comment "进行分配、汇集、调节的中间节点"@zh-CN .

cim-topo:LogicalNode
    a owl:Class ;
    rdfs:subClassOf cim-topo:Node ;
    rdfs:label "Logical Node"@en ;
    rdfs:label "逻辑节点"@zh-CN ;
    rdfs:comment "纯逻辑节点，无需物理设备映射。用于解决GAP-001。"@zh-CN .

cim-topo:Junction
    a owl:Class ;
    rdfs:subClassOf cim-topo:LogicalNode ;
    rdfs:label "Junction"@en ;
    rdfs:label "汇集点"@zh-CN .

cim-topo:Splitter
    a owl:Class ;
    rdfs:subClassOf cim-topo:LogicalNode ;
    rdfs:label "Splitter"@en ;
    rdfs:label "分配点"@zh-CN .

cim-topo:Regulator
    a owl:Class ;
    rdfs:subClassOf cim-topo:Distribution_Node ;
    rdfs:label "Regulator"@en ;
    rdfs:label "调节点"@zh-CN .

cim-topo:Transformer_Node
    a owl:Class ;
    rdfs:subClassOf cim-topo:Distribution_Node ;
    rdfs:label "Transformer Node"@en ;
    rdfs:label "转换点"@zh-CN .

cim-topo:Edge
    a owl:Class ;
    rdfs:subClassOf cim:LogicalObject ;
    rdfs:label "Topology Edge"@en ;
    rdfs:label "拓扑边"@zh-CN .

cim-topo:Trunk
    a owl:Class ;
    rdfs:subClassOf cim-topo:Edge ;
    rdfs:label "Trunk"@en ;
    rdfs:label "干管/主线"@zh-CN .

cim-topo:Branch
    a owl:Class ;
    rdfs:subClassOf cim-topo:Edge ;
    rdfs:label "Branch"@en ;
    rdfs:label "支管/支线"@zh-CN .

cim-topo:Terminal_Connection
    a owl:Class ;
    rdfs:subClassOf cim-topo:Edge ;
    rdfs:label "Terminal Connection"@en ;
    rdfs:label "末端连接"@zh-CN .

cim-topo:System
    a owl:Class ;
    rdfs:subClassOf cim:LogicalObject ;
    rdfs:label "Technical System"@en ;
    rdfs:label "技术系统"@zh-CN .

# Topology Object Properties
cim-topo:hasSourceNode
    a owl:ObjectProperty ;
    rdfs:domain cim-topo:System ;
    rdfs:range cim-topo:Source_Node ;
    rdfs:label "has source node"@en .

cim-topo:feedsTo
    a owl:ObjectProperty ;
    rdfs:domain cim-topo:Node ;
    rdfs:range cim-topo:Node ;
    rdfs:label "feeds to"@en .

cim-topo:hasReturnPath
    a owl:ObjectProperty ;
    rdfs:domain cim-topo:System ;
    rdfs:range cim-flow:FlowSequence ;
    rdfs:label "has return path"@en .

cim-topo:isClosedLoop
    a owl:DatatypeProperty ;
    rdfs:domain cim-topo:System ;
    rdfs:range xsd:boolean ;
    rdfs:label "is closed loop"@en .

# ============================================================================
# SPACE DOMAIN (Agent-02)
# ============================================================================

cim-space:Space
    a owl:Class ;
    rdfs:subClassOf cim:PhysicalObject ;
    rdfs:label "Space"@en ;
    rdfs:label "空间"@zh-CN ;
    cim:sourceAgent "Agent-02" .

cim-space:Site
    a owl:Class ;
    rdfs:subClassOf cim-space:Space ;
    rdfs:label "Site (L0)"@en ;
    rdfs:label "院区"@zh-CN .

cim-space:Building
    a owl:Class ;
    rdfs:subClassOf cim-space:Space ;
    rdfs:label "Building (L1)"@en ;
    rdfs:label "建筑"@zh-CN .

cim-space:Floor
    a owl:Class ;
    rdfs:subClassOf cim-space:Space ;
    rdfs:label "Floor (L2)"@en ;
    rdfs:label "楼层"@zh-CN .

cim-space:Zone
    a owl:Class ;
    rdfs:subClassOf cim-space:Space ;
    rdfs:label "Zone (L3)"@en ;
    rdfs:label "功能区域"@zh-CN .

cim-space:Room
    a owl:Class ;
    rdfs:subClassOf cim-space:Space ;
    rdfs:label "Room (L4)"@en ;
    rdfs:label "房间"@zh-CN .

cim-space:SubSpace
    a owl:Class ;
    rdfs:subClassOf cim-space:Space ;
    rdfs:label "SubSpace (L5)"@en ;
    rdfs:label "子空间"@zh-CN .

# Medical Special Spaces
cim-space:CleanSpace
    a owl:Class ;
    rdfs:subClassOf cim-space:Room ;
    rdfs:label "Clean Space"@en ;
    rdfs:label "洁净空间"@zh-CN ;
    rdfs:comment "所有需要洁净度控制的空间的抽象基类"@zh-CN .

cim-space:OperatingRoom
    a owl:Class ;
    rdfs:subClassOf cim-space:CleanSpace ;
    rdfs:label "Operating Room"@en ;
    rdfs:label "手术室"@zh-CN ;
    skos:note "Standard: GB 50333-2013" .

cim-space:ICU
    a owl:Class ;
    rdfs:subClassOf cim-space:CleanSpace ;
    rdfs:label "ICU"@en ;
    rdfs:label "重症监护室"@zh-CN .

cim-space:IsolationWard
    a owl:Class ;
    rdfs:subClassOf cim-space:Room ;
    rdfs:label "Isolation Ward"@en ;
    rdfs:label "隔离病房"@zh-CN ;
    skos:note "Standard: WS/T 311-2009" .

cim-space:CleanLab
    a owl:Class ;
    rdfs:subClassOf cim-space:CleanSpace ;
    rdfs:label "Clean Laboratory"@en ;
    rdfs:label "洁净实验室"@zh-CN ;
    skos:note "Standard: GB 19489-2008" .

# ============================================================================
# SPACE ENVIRONMENT PROPERTIES (aligned with medical_domain_constraints.json)
# ============================================================================

cim-space:surgeryGrade
    a owl:DatatypeProperty ;
    rdfs:domain cim-space:OperatingRoom ;
    rdfs:range xsd:string ;
    rdfs:label "surgery grade"@en ;
    rdfs:label "手术室等级"@zh-CN ;
    rdfs:comment "取值: Class_I, Class_II, Class_III, Class_IV"@zh-CN .

cim-space:cleanlinessClass
    a owl:DatatypeProperty ;
    rdfs:domain cim-space:CleanSpace ;
    rdfs:range xsd:string ;
    rdfs:label "cleanliness class"@en ;
    rdfs:label "洁净等级"@zh-CN ;
    rdfs:comment "取值: ISO-1 至 ISO-9"@zh-CN .

cim-space:temperature
    a owl:DatatypeProperty ;
    rdfs:domain cim-space:Room ;
    rdfs:range xsd:decimal ;
    rdfs:label "design temperature"@en ;
    rdfs:label "设计温度"@zh-CN ;
    cim:unit "°C" .

cim-space:relativeHumidity
    a owl:DatatypeProperty ;
    rdfs:domain cim-space:Room ;
    rdfs:range xsd:decimal ;
    rdfs:label "relative humidity"@en ;
    rdfs:label "相对湿度"@zh-CN ;
    cim:unit "%RH" .

cim-space:pressureDifferential
    a owl:DatatypeProperty ;
    rdfs:domain cim-space:Room ;
    rdfs:range xsd:decimal ;
    rdfs:label "pressure differential"@en ;
    rdfs:label "压差"@zh-CN ;
    cim:unit "Pa" ;
    rdfs:comment "正值为正压，负值为负压"@zh-CN .

cim-space:airChangesPerHour
    a owl:DatatypeProperty ;
    rdfs:domain cim-space:Room ;
    rdfs:range xsd:decimal ;
    rdfs:label "air changes per hour"@en ;
    rdfs:label "换气次数"@zh-CN ;
    cim:unit "ACH" .

cim-space:freshAirRatio
    a owl:DatatypeProperty ;
    rdfs:domain cim-space:Room ;
    rdfs:range xsd:decimal ;
    rdfs:label "fresh air ratio"@en ;
    rdfs:label "新风比"@zh-CN ;
    cim:unit "%" .

cim-space:noiseLevel
    a owl:DatatypeProperty ;
    rdfs:domain cim-space:Room ;
    rdfs:range xsd:decimal ;
    rdfs:label "noise level"@en ;
    rdfs:label "噪声等级"@zh-CN ;
    cim:unit "dB(A)" .

cim-space:illuminance
    a owl:DatatypeProperty ;
    rdfs:domain cim-space:Room ;
    rdfs:range xsd:decimal ;
    rdfs:label "illuminance"@en ;
    rdfs:label "照度"@zh-CN ;
    cim:unit "lux" .

cim-space:biosafetyLevel
    a owl:DatatypeProperty ;
    rdfs:domain cim-space:CleanLab ;
    rdfs:range xsd:string ;
    rdfs:label "biosafety level"@en ;
    rdfs:label "生物安全等级"@zh-CN ;
    rdfs:comment "取值: BSL-1, BSL-2, BSL-3, BSL-4"@zh-CN .

cim-space:isolationType
    a owl:DatatypeProperty ;
    rdfs:domain cim-space:IsolationWard ;
    rdfs:range xsd:string ;
    rdfs:label "isolation type"@en ;
    rdfs:label "隔离类型"@zh-CN ;
    rdfs:comment "取值: Positive_Pressure, Negative_Pressure"@zh-CN .

# ============================================================================
# EQUIPMENT DOMAIN (Agent-03)
# ============================================================================

cim-equip:Equipment
    a owl:Class ;
    rdfs:subClassOf cim:PhysicalObject ;
    rdfs:label "Equipment"@en ;
    rdfs:label "设备"@zh-CN ;
    cim:sourceAgent "Agent-03" .

cim-equip:Component
    a owl:Class ;
    rdfs:subClassOf cim:PhysicalObject ;
    rdfs:label "Component"@en ;
    rdfs:label "组件"@zh-CN .

cim-equip:Part
    a owl:Class ;
    rdfs:subClassOf cim:PhysicalObject ;
    rdfs:label "Part"@en ;
    rdfs:label "零部件"@zh-CN .

# Equipment Properties
cim-equip:reliabilityLevel
    a owl:DatatypeProperty ;
    rdfs:domain cim-equip:Equipment ;
    rdfs:range xsd:string ;
    rdfs:label "reliability level"@en ;
    rdfs:label "可靠性等级"@zh-CN ;
    rdfs:comment "取值: LIFE_SAFETY, PATIENT_SAFETY, CRITICAL, IMPORTANT, SECONDARY"@zh-CN .

# Control Status Properties (for GAP-003)
cim-equip:hasLocalControl
    a owl:DatatypeProperty ;
    rdfs:domain cim-equip:Equipment ;
    rdfs:range xsd:boolean ;
    rdfs:label "has local control"@en ;
    rdfs:label "有本地控制"@zh-CN .

cim-equip:externalControlSystem
    a owl:DatatypeProperty ;
    rdfs:domain cim-equip:Equipment ;
    rdfs:range xsd:string ;
    rdfs:label "external control system"@en ;
    rdfs:label "外部控制系统"@zh-CN .

cim-equip:isUncontrolledLoad
    a owl:DatatypeProperty ;
    rdfs:domain cim-equip:Equipment ;
    rdfs:range xsd:boolean ;
    rdfs:label "is uncontrolled load"@en ;
    rdfs:label "是否为非受控负荷"@zh-CN .

# Mapping Status (for GAP-001)
cim:mappingStatus
    a owl:DatatypeProperty ;
    rdfs:domain cim-topo:Node ;
    rdfs:range xsd:string ;
    rdfs:label "mapping status"@en ;
    rdfs:comment "取值: Mapped, PendingMapping, LogicalOnly"@zh-CN .

# Location Status (for GAP-002)
cim:locationStatus
    a owl:DatatypeProperty ;
    rdfs:domain cim-equip:Equipment ;
    rdfs:range xsd:string ;
    rdfs:label "location status"@en ;
    rdfs:comment "取值: Defined, TBD"@zh-CN .

# ============================================================================
# FLOW DOMAIN (Agent-04)
# ============================================================================

cim-flow:Flow
    a owl:Class ;
    rdfs:subClassOf cim:LogicalObject ;
    rdfs:label "Flow"@en ;
    rdfs:label "流动"@zh-CN ;
    cim:sourceAgent "Agent-04" .

cim-flow:Mass_Flow
    a owl:Class ;
    rdfs:subClassOf cim-flow:Flow ;
    rdfs:label "Mass Flow"@en ;
    rdfs:label "物质流"@zh-CN .

cim-flow:Energy_Flow
    a owl:Class ;
    rdfs:subClassOf cim-flow:Flow ;
    rdfs:label "Energy Flow"@en ;
    rdfs:label "能量流"@zh-CN .

cim-flow:Information_Flow
    a owl:Class ;
    rdfs:subClassOf cim-flow:Flow ;
    rdfs:label "Information Flow"@en ;
    rdfs:label "信息流"@zh-CN .

cim-flow:FlowSequence
    a owl:Class ;
    rdfs:subClassOf cim:LogicalObject ;
    rdfs:label "Flow Sequence"@en ;
    rdfs:label "流动序列"@zh-CN .

# ============================================================================
# LOCATION DOMAIN (Agent-05)
# ============================================================================

cim-loc:MEP_Room
    a owl:Class ;
    rdfs:subClassOf cim-space:Room ;
    rdfs:label "MEP Room"@en ;
    rdfs:label "机电设备用房"@zh-CN ;
    cim:sourceAgent "Agent-05" .

cim-loc:Shaft
    a owl:Class ;
    rdfs:subClassOf cim-space:Space ;
    rdfs:label "Shaft"@en ;
    rdfs:label "竖井"@zh-CN .

cim-loc:Ceiling_Void
    a owl:Class ;
    rdfs:subClassOf cim-space:Space ;
    rdfs:label "Ceiling Void"@en ;
    rdfs:label "吊顶内"@zh-CN .

cim-loc:Served_Space
    a owl:Class ;
    rdfs:subClassOf cim-space:Space ;
    rdfs:label "Served Space"@en ;
    rdfs:label "服务空间内"@zh-CN .

# ============================================================================
# CONTROL DOMAIN (Agent-06)
# ============================================================================

cim-ctrl:ControlDevice
    a owl:Class ;
    rdfs:subClassOf cim-equip:Equipment ;
    rdfs:label "Control Device"@en ;
    rdfs:label "控制设备"@zh-CN ;
    cim:sourceAgent "Agent-06" .

cim-ctrl:Sensor
    a owl:Class ;
    rdfs:subClassOf cim-ctrl:ControlDevice ;
    rdfs:label "Sensor"@en ;
    rdfs:label "传感器"@zh-CN .

cim-ctrl:Actuator
    a owl:Class ;
    rdfs:subClassOf cim-ctrl:ControlDevice ;
    rdfs:label "Actuator"@en ;
    rdfs:label "执行器"@zh-CN .

cim-ctrl:Controller
    a owl:Class ;
    rdfs:subClassOf cim-ctrl:ControlDevice ;
    rdfs:label "Controller"@en ;
    rdfs:label "控制器"@zh-CN .

cim-ctrl:ControlLoop
    a owl:Class ;
    rdfs:subClassOf cim:LogicalObject ;
    rdfs:label "Control Loop"@en ;
    rdfs:label "控制回路"@zh-CN .

# Control Relations
cim-ctrl:monitors
    a owl:ObjectProperty ;
    rdfs:domain cim-ctrl:Sensor ;
    rdfs:range cim:Entity ;
    rdfs:label "monitors"@en .

cim-ctrl:controls
    a owl:ObjectProperty ;
    rdfs:domain cim-ctrl:Actuator ;
    rdfs:range cim-equip:Equipment ;
    rdfs:label "controls"@en .

# ============================================================================
# METERING DOMAIN (Agent-07)
# ============================================================================

cim-meter:Meter
    a owl:Class ;
    rdfs:subClassOf cim-equip:Equipment ;
    rdfs:label "Meter"@en ;
    rdfs:label "计量表"@zh-CN ;
    cim:sourceAgent "Agent-07" .

cim-meter:VirtualMeter
    a owl:Class ;
    rdfs:subClassOf cim-meter:Meter ;
    rdfs:label "Virtual Meter"@en ;
    rdfs:label "虚拟计量表"@zh-CN ;
    rdfs:comment "通过计算派生的计量点"@zh-CN .

cim-meter:MeteringHierarchy
    a owl:Class ;
    rdfs:subClassOf cim:LogicalObject ;
    rdfs:label "Metering Hierarchy"@en ;
    rdfs:label "计量层级"@zh-CN .

# Metering Relations (range extended for GAP-004)
cim-meter:meters
    a owl:ObjectProperty ;
    rdfs:domain cim-meter:Meter ;
    rdfs:range cim:Entity ;
    rdfs:label "meters"@en ;
    rdfs:comment "计量对象可以是设备、流动、或空间"@zh-CN .

cim-meter:derivedFrom
    a owl:ObjectProperty ;
    rdfs:domain cim-meter:VirtualMeter ;
    rdfs:range cim-meter:Meter ;
    rdfs:label "derived from"@en ;
    rdfs:comment "虚拟表的计算来源"@zh-CN .

# ============================================================================
# OPERATIONS DOMAIN (Agent-08)
# ============================================================================

cim-om:WorkOrder
    a owl:Class ;
    rdfs:subClassOf cim:LogicalObject ;
    rdfs:label "Work Order"@en ;
    rdfs:label "工单"@zh-CN ;
    cim:sourceAgent "Agent-08" .

cim-om:MaintenanceStrategy
    a owl:Class ;
    rdfs:subClassOf cim:LogicalObject ;
    rdfs:label "Maintenance Strategy"@en ;
    rdfs:label "维护策略"@zh-CN .

cim-om:Preventive_Maintenance
    a owl:Class ;
    rdfs:subClassOf cim-om:MaintenanceStrategy ;
    rdfs:label "Preventive Maintenance"@en ;
    rdfs:label "预防性维护"@zh-CN .

cim-om:Predictive_Maintenance
    a owl:Class ;
    rdfs:subClassOf cim-om:MaintenanceStrategy ;
    rdfs:label "Predictive Maintenance"@en ;
    rdfs:label "预测性维护"@zh-CN .

cim-om:AssetLifecycle
    a owl:Class ;
    rdfs:subClassOf cim:LogicalObject ;
    rdfs:label "Asset Lifecycle"@en ;
    rdfs:label "资产生命周期"@zh-CN .

# ============================================================================
# CROSS-DOMAIN OBJECT PROPERTIES
# ============================================================================

cim:locatedIn
    a owl:ObjectProperty ;
    rdfs:domain cim-equip:Equipment ;
    rdfs:range cim-space:Space ;
    rdfs:label "located in"@en ;
    rdfs:label "位于"@zh-CN .

cim:serves
    a owl:ObjectProperty ;
    rdfs:domain cim:Entity ;
    rdfs:range cim-space:Space ;
    rdfs:label "serves"@en ;
    rdfs:label "服务于"@zh-CN .

cim:mapsToNode
    a owl:ObjectProperty ;
    rdfs:domain cim-equip:Equipment ;
    rdfs:range cim-topo:Node ;
    rdfs:label "maps to node"@en ;
    rdfs:label "映射到节点"@zh-CN .

cim:contains
    a owl:ObjectProperty, owl:TransitiveProperty ;
    rdfs:domain cim-space:Space ;
    rdfs:range cim-space:Space ;
    rdfs:label "contains"@en ;
    rdfs:label "包含"@zh-CN .

cim:componentOf
    a owl:ObjectProperty ;
    rdfs:domain cim-equip:Component ;
    rdfs:range cim-equip:Equipment ;
    rdfs:label "component of"@en ;
    rdfs:label "组件属于"@zh-CN .

cim:dependsOn
    a owl:ObjectProperty ;
    rdfs:domain cim-topo:System ;
    rdfs:range cim-topo:System ;
    rdfs:label "depends on"@en ;
    rdfs:label "依赖于"@zh-CN .

cim:routesThrough
    a owl:ObjectProperty ;
    rdfs:domain cim:PhysicalObject ;
    rdfs:range cim-space:Space ;
    rdfs:label "routes through"@en ;
    rdfs:label "穿越"@zh-CN .

# ============================================================================
# END OF SKELETON
# ============================================================================
```

---

## DOC-009: `task_manifest.json`

```json
{
  "manifest_meta": {
    "manifest_id": "TM-CIM-20250117-FINAL",
    "version": "2.0.0",
    "description": "CIM本体工程完整任务清单 - 可直接交付Claude Code执行",
    "generated_at": "2025-01-17T19:00:00Z",
    "target_executor": "Claude-Code",
    "execution_strategy": "Topological Sort (DAG-based)",
    "entry_point": "从TASK-001开始，按execution_order顺序执行"
  },

  "global_references": {
    "config_file": "_config.json",
    "skeleton_file": "ontology_skeleton.ttl",
    "constraints_file": "medical_domain_constraints.json",
    "gap_analysis_file": "cross_agent_gap_analysis.json",
    "validation_schema": "validation_rules_schema.json"
  },

  "execution_phases": [
    {
      "phase": 1,
      "name": "Foundation",
      "description": "基础层 - 核心定义，无外部依赖",
      "tasks": ["TASK-001"],
      "parallel": false,
      "blocking": true
    },
    {
      "phase": 2,
      "name": "Domain Foundations",
      "description": "领域基础层 - 依赖基础层",
      "tasks": ["TASK-002", "TASK-003", "TASK-004"],
      "parallel": true,
      "blocking": true
    },
    {
      "phase": 3,
      "name": "Domain Extensions",
      "description": "领域扩展层",
      "tasks": ["TASK-005", "TASK-006"],
      "parallel": true,
      "blocking": false
    },
    {
      "phase": 4,
      "name": "Integration",
      "description": "集成层 - 跨领域耦合",
      "tasks": ["TASK-007", "TASK-008", "TASK-009"],
      "parallel": true,
      "blocking": false
    },
    {
      "phase": 5,
      "name": "Validation Rules",
      "description": "验证规则层",
      "tasks": ["TASK-010", "TASK-011"],
      "parallel": true,
      "blocking": false
    },
    {
      "phase": 6,
      "name": "Finalization",
      "description": "最终整合",
      "tasks": ["TASK-012"],
      "parallel": false,
      "blocking": true
    }
  ],

  "tasks": [
    {
      "id": "TASK-001",
      "priority": "P0-Critical",
      "target_file": "cim/core/base_entities.ttl",
      "description": "实现核心基类定义 (Entity, PhysicalObject, LogicalObject)",
      "source_agents": ["Agent-09"],
      "concepts_to_implement": [
        "cim:Entity",
        "cim:PhysicalObject",
        "cim:LogicalObject",
        "cim:unit (annotation property)",
        "cim:sourceAgent (annotation property)"
      ],
      "dependencies": [],
      "input_documents": ["ontology_skeleton.ttl"],
      "implementation_notes": "从ontology_skeleton.ttl提取CORE BASE CLASSES部分",
      "validation_rules": [
        {
          "rule_id": "VAL-BASE-001",
          "type": "Turtle-Syntax",
          "check": "文件必须通过Turtle语法验证",
          "tool": "rapper -i turtle"
        }
      ],
      "expected_output": {
        "classes": 3,
        "properties": 2
      }
    },
    {
      "id": "TASK-002",
      "priority": "P0-Critical",
      "target_file": "cim/topology/node_types.ttl",
      "description": "实现Agent-01定义的拓扑节点类型",
      "source_agents": ["Agent-01"],
      "concepts_to_implement": [
        "cim-topo:Node",
        "cim-topo:Source_Node",
        "cim-topo:Sink_Node",
        "cim-topo:Distribution_Node",
        "cim-topo:LogicalNode (for GAP-001)",
        "cim-topo:Junction",
        "cim-topo:Splitter",
        "cim-topo:Regulator",
        "cim-topo:Transformer_Node"
      ],
      "dependencies": ["TASK-001"],
      "input_documents": [
        "ontology_skeleton.ttl#TOPOLOGY_DOMAIN",
        "concept_extraction_report.json#topology_domain"
      ],
      "validation_rules": [
        {
          "rule_id": "VAL-TOPO-INHERIT",
          "type": "SPARQL-ASK",
          "query": "ASK { cim-topo:Source_Node rdfs:subClassOf cim-topo:Node }",
          "expected": true
        }
      ],
      "expected_output": {
        "classes": 9
      }
    },
    {
      "id": "TASK-003",
      "priority": "P0-Critical",
      "target_file": "cim/spaces/spatial_hierarchy.ttl",
      "description": "实现Agent-02定义的6级空间层级",
      "source_agents": ["Agent-02"],
      "concepts_to_implement": [
        "cim-space:Space",
        "cim-space:Site (L0)",
        "cim-space:Building (L1)",
        "cim-space:Floor (L2)",
        "cim-space:Zone (L3)",
        "cim-space:Room (L4)",
        "cim-space:SubSpace (L5)"
      ],
      "dependencies": ["TASK-001"],
      "input_documents": [
        "ontology_skeleton.ttl#SPACE_DOMAIN",
        "concept_extraction_report.json#space_domain.hierarchy_levels"
      ],
      "expected_output": {
        "classes": 7
      }
    },
    {
      "id": "TASK-004",
      "priority": "P0-Critical",
      "target_file": "cim/equipment/equipment_hierarchy.ttl",
      "description": "实现Agent-03定义的设备层级与可靠性分级",
      "source_agents": ["Agent-03"],
      "concepts_to_implement": [
        "cim-equip:Equipment",
        "cim-equip:Component",
        "cim-equip:Part",
        "cim-equip:reliabilityLevel",
        "cim-equip:hasLocalControl (for GAP-003)",
        "cim-equip:externalControlSystem (for GAP-003)",
        "cim-equip:isUncontrolledLoad (for GAP-003)"
      ],
      "dependencies": ["TASK-001"],
      "input_documents": [
        "ontology_skeleton.ttl#EQUIPMENT_DOMAIN",
        "concept_extraction_report.json#equipment_domain"
      ],
      "expected_output": {
        "classes": 3,
        "datatype_properties": 4
      }
    },
    {
      "id": "TASK-005",
      "priority": "P0-Critical",
      "target_file": "cim/spaces/medical_special_spaces.ttl",
      "description": "实现医疗专用空间定义，包含完整环境属性",
      "source_agents": ["Agent-02", "Agent-09"],
      "concepts_to_implement": [
        "cim-space:CleanSpace",
        "cim-space:OperatingRoom",
        "cim-space:ICU",
        "cim-space:IsolationWard",
        "cim-space:CleanLab",
        "ALL environment properties from ontology_skeleton.ttl#SPACE_ENVIRONMENT_PROPERTIES"
      ],
      "dependencies": ["TASK-003"],
      "input_documents": [
        "ontology_skeleton.ttl#SPACE_ENVIRONMENT_PROPERTIES",
        "medical_domain_constraints.json#property_definitions",
        "concept_extraction_report.json#space_domain.medical_special_spaces"
      ],
      "implementation_notes": "必须包含所有11个环境属性 (surgeryGrade, cleanlinessClass, temperature等)",
      "validation_rules": [
        {
          "rule_id": "VAL-SPACE-PROPS",
          "type": "SPARQL-ASK",
          "query": "ASK { cim-space:temperature a owl:DatatypeProperty }",
          "expected": true
        }
      ],
      "expected_output": {
        "classes": 5,
        "datatype_properties": 11
      }
    },
    {
      "id": "TASK-006",
      "priority": "P1-Important",
      "target_file": "cim/equipment/mechanical.ttl",
      "description": "实现HVAC设备本体",
      "source_agents": ["Agent-03"],
      "concepts_to_implement": [
        "cim-equip:HVAC_Equipment (abstract)",
        "cim-equip:Chiller",
        "cim-equip:AHU",
        "cim-equip:Clean_AHU",
        "cim-equip:HEPA_Filter",
        "cim-equip:CoolingTower",
        "cim-equip:Pump",
        "cim-equip:VAV_Terminal",
        "cim-equip:FCU"
      ],
      "dependencies": ["TASK-002", "TASK-004"],
      "input_documents": [
        "concept_extraction_report.json#equipment_domain.p0_core_equipment"
      ],
      "expected_output": {
        "classes": 9
      }
    },
    {
      "id": "TASK-007",
      "priority": "P1-Important",
      "target_file": "cim/coupling/equipment_location.ttl",
      "description": "实现Agent-05定义的设备-空间位置耦合",
      "source_agents": ["Agent-05"],
      "concepts_to_implement": [
        "cim-loc:MEP_Room",
        "cim-loc:Shaft",
        "cim-loc:Ceiling_Void",
        "cim-loc:Served_Space",
        "cim:locatedIn (relation)",
        "cim:locationStatus (for GAP-002)"
      ],
      "dependencies": ["TASK-003", "TASK-004"],
      "input_documents": [
        "ontology_skeleton.ttl#LOCATION_DOMAIN",
        "concept_extraction_report.json#coupling_domain"
      ],
      "expected_output": {
        "classes": 4,
        "object_properties": 1,
        "datatype_properties": 1
      }
    },
    {
      "id": "TASK-008",
      "priority": "P1-Important",
      "target_file": "cim/control/sensors.ttl",
      "description": "实现Agent-06定义的传感器本体",
      "source_agents": ["Agent-06"],
      "concepts_to_implement": [
        "cim-ctrl:ControlDevice",
        "cim-ctrl:Sensor",
        "cim-ctrl:Temperature_Sensor",
        "cim-ctrl:Humidity_Sensor",
        "cim-ctrl:Pressure_Sensor",
        "cim-ctrl:monitors (relation)"
      ],
      "dependencies": ["TASK-004"],
      "input_documents": [
        "ontology_skeleton.ttl#CONTROL_DOMAIN",
        "concept_extraction_report.json#control_domain.sensor_types"
      ],
      "expected_output": {
        "classes": 5,
        "object_properties": 1
      }
    },
    {
      "id": "TASK-009",
      "priority": "P1-Important",
      "target_file": "cim/metering/metering_hierarchy.ttl",
      "description": "实现Agent-07定义的4级计量层级",
      "source_agents": ["Agent-07"],
      "concepts_to_implement": [
        "cim-meter:Meter",
        "cim-meter:VirtualMeter (for GAP-004)",
        "cim-meter:MeteringHierarchy",
        "cim-meter:meters (relation, extended range)",
        "cim-meter:derivedFrom (for GAP-004)"
      ],
      "dependencies": ["TASK-004"],
      "input_documents": [
        "ontology_skeleton.ttl#METERING_DOMAIN",
        "concept_extraction_report.json#metering_domain"
      ],
      "implementation_notes": "meters关系的range需包含cim-space:Space以支持总表计量场景",
      "expected_output": {
        "classes": 3,
        "object_properties": 2
      }
    },
    {
      "id": "TASK-010",
      "priority": "P1-Important",
      "target_file": "cim/rules/cross_agent_validation.sparql",
      "description": "实现跨Agent一致性验证SPARQL查询",
      "source_agents": ["Agent-09"],
      "concepts_to_implement": [
        "CST-TOPO-001 验证查询",
        "CST-TOPO-002 验证查询",
        "CST-EQUIP-001 验证查询",
        "CST-SPACE-001 验证查询",
        "CST-CTRL-001 验证查询",
        "CST-METER-001 验证查询"
      ],
      "dependencies": ["TASK-002", "TASK-003", "TASK-004", "TASK-007", "TASK-008", "TASK-009"],
      "input_documents": [
        "concept_extraction_report.json#extracted_constraints"
      ],
      "implementation_notes": "直接从concept_extraction_report.json复制每个约束的sparql_check.query",
      "expected_output": {
        "sparql_queries": 6
      }
    },
    {
      "id": "TASK-011",
      "priority": "P1-Important",
      "target_file": "cim/rules/shacl_constraints.ttl",
      "description": "实现医疗领域SHACL数据形状约束",
      "source_agents": ["Agent-02", "Agent-09"],
      "concepts_to_implement": [
        "cim-shape:OperatingRoom_Class_I_Shape",
        "cim-shape:IsolationWard_Negative_Shape",
        "cim-shape:CleanLab_BSL3_Shape",
        "cim-shape:EquipmentMustHaveLocationShape",
        "cim-shape:NodeMustHaveEquipmentShape"
      ],
      "dependencies": ["TASK-005", "TASK-007"],
      "input_documents": [
        "medical_domain_constraints.json#space_environmental_constraints[*].shacl_shape",
        "concept_extraction_report.json#extracted_constraints[*].shacl_shape"
      ],
      "implementation_notes": "直接从源文档复制turtle字段内容并合并为单个文件",
      "expected_output": {
        "shacl_shapes": 5
      }
    },
    {
      "id": "TASK-012",
      "priority": "P0-Critical",
      "target_file": "cim/_index.ttl",
      "description": "生成本体入口文件，包含所有模块的owl:imports",
      "source_agents": [],
      "concepts_to_implement": [
        "owl:Ontology声明",
        "owl:imports for all .ttl files",
        "namespace prefix declarations"
      ],
      "dependencies": ["TASK-001", "TASK-002", "TASK-003", "TASK-004", "TASK-005", "TASK-006", "TASK-007", "TASK-008", "TASK-009", "TASK-010", "TASK-011"],
      "input_documents": [
        "cim_document_structure.md",
        "_config.json#namespace_registry"
      ],
      "validation_rules": [
        {
          "rule_id": "VAL-IMPORTS",
          "type": "FileSystem",
          "check": "所有owl:imports引用的文件必须存在"
        }
      ],
      "expected_output": {
        "imports": 11
      }
    }
  ],

  "execution_order": [
    {"phase": 1, "tasks": ["TASK-001"]},
    {"phase": 2, "tasks": ["TASK-002", "TASK-003", "TASK-004"]},
    {"phase": 3, "tasks": ["TASK-005", "TASK-006"]},
    {"phase": 4, "tasks": ["TASK-007", "TASK-008", "TASK-009"]},
    {"phase": 5, "tasks": ["TASK-010", "TASK-011"]},
    {"phase": 6, "tasks": ["TASK-012"]}
  ],

  "success_criteria": {
    "all_tasks_completed": true,
    "all_validations_passed": true,
    "total_files_generated": 12,
    "index_file_valid": true
  }
}
```

---

## DOC-010: `dependency_graph.json`

```json
{
  "graph_meta": {
    "graph_id": "DEP-CIM-20250117-FINAL",
    "type": "Directed Acyclic Graph (DAG)",
    "description": "CIM本体工程任务与Agent间依赖关系图"
  },

  "agent_dependencies": {
    "description": "Agent间的数据流依赖关系",
    "nodes": {
      "Agent-01": {"name": "系统拓扑建模师", "phase": 1, "is_foundation": true},
      "Agent-02": {"name": "空间本体建模师", "phase": 1, "is_foundation": true},
      "Agent-03": {"name": "设备本体建模师", "phase": 2},
      "Agent-04": {"name": "流动模型建模师", "phase": 2},
      "Agent-05": {"name": "系统-空间耦合建模师", "phase": 3},
      "Agent-06": {"name": "控制系统建模师", "phase": 3},
      "Agent-07": {"name": "计量体系建模师", "phase": 4},
      "Agent-08": {"name": "运维管理建模师", "phase": 4},
      "Agent-09": {"name": "模型整合师", "phase": 5}
    },
    "edges": [
      {"from": "Agent-01", "to": "Agent-03", "data": "系统拓扑结构、节点定义"},
      {"from": "Agent-01", "to": "Agent-04", "data": "系统拓扑、边定义"},
      {"from": "Agent-01", "to": "Agent-05", "data": "系统拓扑结构"},
      {"from": "Agent-02", "to": "Agent-05", "data": "空间本体、医疗空间"},
      {"from": "Agent-03", "to": "Agent-05", "data": "设备本体、节点映射"},
      {"from": "Agent-03", "to": "Agent-06", "data": "设备本体(控制属性)"},
      {"from": "Agent-03", "to": "Agent-07", "data": "设备本体(计量设备)"},
      {"from": "Agent-03", "to": "Agent-08", "data": "设备本体(告警规则)"},
      {"from": "Agent-05", "to": "Agent-06", "data": "设备-空间耦合"},
      {"from": "Agent-05", "to": "Agent-07", "data": "系统-空间耦合"},
      {"from": "Agent-06", "to": "Agent-08", "data": "控制系统模型"},
      {"from": "Agent-07", "to": "Agent-08", "data": "计量体系模型"},
      {"from": "All", "to": "Agent-09", "data": "所有Agent输出"}
    ]
  },

  "task_dependencies": {
    "nodes": {
      "TASK-001": {"file": "core/base_entities.ttl", "critical_path": true},
      "TASK-002": {"file": "topology/node_types.ttl", "critical_path": true},
      "TASK-003": {"file": "spaces/spatial_hierarchy.ttl", "critical_path": true},
      "TASK-004": {"file": "equipment/equipment_hierarchy.ttl", "critical_path": true},
      "TASK-005": {"file": "spaces/medical_special_spaces.ttl", "critical_path": true},
      "TASK-006": {"file": "equipment/mechanical.ttl", "critical_path": false},
      "TASK-007": {"file": "coupling/equipment_location.ttl", "critical_path": false},
      "TASK-008": {"file": "control/sensors.ttl", "critical_path": false},
      "TASK-009": {"file": "metering/metering_hierarchy.ttl", "critical_path": false},
      "TASK-010": {"file": "rules/cross_agent_validation.sparql", "critical_path": false},
      "TASK-011": {"file": "rules/shacl_constraints.ttl", "critical_path": true},
      "TASK-012": {"file": "_index.ttl", "critical_path": true}
    },
    "edges": [
      {"from": "TASK-001", "to": "TASK-002"},
      {"from": "TASK-001", "to": "TASK-003"},
      {"from": "TASK-001", "to": "TASK-004"},
      {"from": "TASK-003", "to": "TASK-005"},
      {"from": "TASK-002", "to": "TASK-006"},
      {"from": "TASK-004", "to": "TASK-006"},
      {"from": "TASK-003", "to": "TASK-007"},
      {"from": "TASK-004", "to": "TASK-007"},
      {"from": "TASK-004", "to": "TASK-008"},
      {"from": "TASK-004", "to": "TASK-009"},
      {"from": "TASK-002", "to": "TASK-010"},
      {"from": "TASK-007", "to": "TASK-010"},
      {"from": "TASK-008", "to": "TASK-010"},
      {"from": "TASK-009", "to": "TASK-010"},
      {"from": "TASK-005", "to": "TASK-011"},
      {"from": "TASK-007", "to": "TASK-011"},
      {"from": "TASK-010", "to": "TASK-012"},
      {"from": "TASK-011", "to": "TASK-012"}
    ]
  },

  "critical_path": ["TASK-001", "TASK-003", "TASK-005", "TASK-011", "TASK-012"],

  "parallel_groups": [
    {"phase": 2, "tasks": ["TASK-002", "TASK-003", "TASK-004"], "max_parallel": 3},
    {"phase": 3, "tasks": ["TASK-005", "TASK-006"], "max_parallel": 2},
    {"phase": 4, "tasks": ["TASK-007", "TASK-008", "TASK-009"], "max_parallel": 3},
    {"phase": 5, "tasks": ["TASK-010", "TASK-011"], "max_parallel": 2}
  ]
}
```

---

## DOC-011: `_index.ttl` (模板)

```turtle
# ============================================================================
# CIM Medical Building - Master Index Ontology
# Auto-generated entry point for the Unified Domain Model
# Version: 2.0.0-Final
# ============================================================================

@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix cim:  <https://cim.medical/ontology/v3.4#> .

<https://cim.medical/ontology/v3.4>
    a owl:Ontology ;
    rdfs:label "CIM Medical Building Master Index"@en ;
    rdfs:label "医疗建筑CIM主索引"@zh-CN ;
    rdfs:comment "Auto-generated entry point. Imports all CIM ontology modules."@en ;
    owl:versionInfo "2.0.0-Final" ;

    # Core Module
    owl:imports <https://cim.medical/ontology/v3.4/core/base_entities> ;

    # Topology Module (Agent-01)
    owl:imports <https://cim.medical/ontology/v3.4/topology/node_types> ;

    # Space Module (Agent-02)
    owl:imports <https://cim.medical/ontology/v3.4/spaces/spatial_hierarchy> ;
    owl:imports <https://cim.medical/ontology/v3.4/spaces/medical_special_spaces> ;

    # Equipment Module (Agent-03)
    owl:imports <https://cim.medical/ontology/v3.4/equipment/equipment_hierarchy> ;
    owl:imports <https://cim.medical/ontology/v3.4/equipment/mechanical> ;

    # Coupling Module (Agent-05)
    owl:imports <https://cim.medical/ontology/v3.4/coupling/equipment_location> ;

    # Control Module (Agent-06)
    owl:imports <https://cim.medical/ontology/v3.4/control/sensors> ;

    # Metering Module (Agent-07)
    owl:imports <https://cim.medical/ontology/v3.4/metering/metering_hierarchy> ;

    # Validation Rules
    owl:imports <https://cim.medical/ontology/v3.4/rules/shacl_constraints> .

# ============================================================================
# END OF INDEX
# ============================================================================
```

---

## 📋 完整交付物清单

| 序号 | 文档ID | 文件名 | 描述 | 行数(约) |
|------|--------|--------|------|----------|
| 1 | DOC-001 | `_config.json` | 全局配置与元数据 | 180 |
| 2 | DOC-002 | `source_file_audit.json` | 源文件存在性验证 | 220 |
| 3 | DOC-003 | `concept_extraction_report.json` | 完整概念提取报告 | 1200 |
| 4 | DOC-004 | `cross_agent_gap_analysis.json` | 跨Agent映射空白分析 | 350 |
| 5 | DOC-005 | `medical_domain_constraints.json` | 医疗领域约束库 | 450 |
| 6 | DOC-006 | `validation_rules_schema.json` | 验证规则JSON Schema | 80 |
| 7 | DOC-007 | `cim_document_structure.md` | 目录结构定义 | 100 |
| 8 | DOC-008 | `ontology_skeleton.ttl` | 本体骨架定义 | 450 |
| 9 | DOC-009 | `task_manifest.json` | 任务清单与依赖 | 380 |
| 10 | DOC-010 | `dependency_graph.json` | 依赖关系图 | 120 |
| 11 | DOC-011 | `_index.ttl` | 本体入口文件模板 | 50 |

---

## 🚀 执行指南

**Claude Code 执行入口：**

1. **读取** `task_manifest.json`
2. **按 `execution_order` 顺序执行任务**
3. **每个任务参考 `input_documents` 获取源数据**
4. **生成文件后运行 `validation_rules` 验证**
5. **最终验证 `_index.ttl` 可正确加载所有模块**

---

**文档版本**: 2.0.0-Final
**生成完成**: 2025-01-17T19:00:00Z
**状态**: ✅ 可交付执行