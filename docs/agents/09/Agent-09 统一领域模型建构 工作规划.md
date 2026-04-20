# **Agent-09 统一领域模型建构 工作规划

## 第一步：知识库深度扫描

---

## 🏗️ CIM统一领域模型 - 本体工程索引与协调者 完整交付物

基于对知识库中 **Agent-01~08 全部成果文档** 的深度扫描，以下是经过实际引用追踪的完整交付物。

---

## 📄 1. `concept_extraction_report.json`

**完整的概念提取报告 - 基于Agent-01~08实际输出**

```json
{
  "meta": {
    "report_id": "CER-CIM-20250117-FULL",
    "generated_by": "Gemini-CLI (本体工程索引与协调者)",
    "scan_timestamp": "2025-01-17T16:00:00Z",
    "source_path": "/Volumes/M4-SSD/.../docs/agents",
    "total_agents_scanned": 8,
    "extraction_method": "Knowledge Base Deep Scan"
  },

  "source_document_registry": {
    "Agent-01": {
      "doc_id": "DOC-A01",
      "title": "系统拓扑建模师 (System Topology Architect)",
      "files": [
        "Agent01_Output.meta",
        "Agent01_Output.system_catalog",
        "Agent01_Output.topology_definitions",
        "Agent01_Output.system_dependencies"
      ],
      "output_format": "YAML",
      "status": "Phase 1 进行中"
    },
    "Agent-02": {
      "doc_id": "DOC-A02",
      "title": "空间本体建模师 (Space Ontology Architect)",
      "files": [
        "Agent02_Output.space_hierarchy_model.yaml",
        "Agent02_Output.space_classification.yaml",
        "Agent02_Output.medical_special_spaces.yaml"
      ],
      "output_format": "YAML",
      "properties_defined": "350+"
    },
    "Agent-03": {
      "doc_id": "DOC-A03",
      "title": "设备本体建模师 (Equipment Ontology Architect)",
      "files": [
        "Agent03_Output.meta",
        "Agent03_Output.equipment_classification",
        "Agent03_Output.node_equipment_mapping",
        "Agent03_Output.equipment_type_models",
        "Agent03_Output.project_summary.md"
      ],
      "output_format": "YAML",
      "version": "v2.2"
    },
    "Agent-04": {
      "doc_id": "DOC-A04",
      "title": "流动模型建模师 (Flow Model Architect)",
      "files": [
        "Agent04_v2.3_FlowModel.ttl",
        "Agent04_v2.3_Engineering.yaml"
      ],
      "output_format": "Turtle RDF + YAML",
      "version": "v2.3"
    },
    "Agent-05": {
      "doc_id": "DOC-A05",
      "title": "系统-空间耦合建模师 (System-Space Coupling Architect)",
      "files": [
        "Agent05_Output.equipment_location_model",
        "Agent05_Output.routing_space_model",
        "Agent05_Output.service_space_model",
        "Agent05_Output.space_requirement_mapping"
      ],
      "output_format": "RDF + JSON",
      "version": "V2.1-RELEASE"
    },
    "Agent-06": {
      "doc_id": "DOC-A06",
      "title": "控制系统建模师 (Control System Architect)",
      "files": [
        "Agent06_Output.meta",
        "Agent06_Output.sensor_models",
        "Agent06_Output.actuator_models",
        "Agent06_Output.controller_models",
        "Agent06_Output.control_loop_models"
      ],
      "output_format": "YAML",
      "scope": "247传感器, 156执行器, 87控制回路"
    },
    "Agent-07": {
      "doc_id": "DOC-A07",
      "title": "计量体系建模师 (Metering System Architect)",
      "files": [
        "Agent07_Output.meta",
        "Agent07_Output.metering_hierarchy",
        "Agent07_Output.energy_media_models",
        "Agent07_Output.allocation_rules",
        "Agent07_Output.metering_point_layout",
        "Agent07_Output.associations"
      ],
      "output_format": "YAML",
      "scope": "4级计量, 7能量类型, 189计量点"
    },
    "Agent-08": {
      "doc_id": "DOC-A08",
      "title": "运维管理建模师 (O&M Management Architect)",
      "files": [
        "Agent08_Output.alarm_models",
        "Agent08_Output.work_order_models",
        "Agent08_Output.maintenance_strategies",
        "Agent08_Output.asset_lifecycle_models",
        "Agent08_Output.operation_organization_models"
      ],
      "output_format": "YAML",
      "version": "v3.0"
    }
  },

  "extracted_entities": {
    "topology_domain": {
      "source_agent": "Agent-01",
      "source_section": "理论基础：拓扑网络元模型",
      "entities": [
        {
          "uri": "cim:Source_Node",
          "label_cn": "源节点",
          "definition": "系统的能量/介质输入端，流动的起点",
          "attributes": ["node_id", "node_name", "medium_type", "is_external", "capacity"],
          "source_trace": "Agent-01.Node_Types.Source_Node"
        },
        {
          "uri": "cim:Sink_Node",
          "label_cn": "末端节点",
          "definition": "系统的能量/介质消耗端，流动的终点",
          "attributes": ["node_id", "node_name", "consumption_type", "served_function"],
          "source_trace": "Agent-01.Node_Types.Sink_Node"
        },
        {
          "uri": "cim:Distribution_Node",
          "label_cn": "分配节点",
          "definition": "进行分配、汇集、调节的中间节点",
          "subtypes": ["Junction", "Splitter", "Regulator", "Transformer"],
          "source_trace": "Agent-01.Node_Types.Distribution_Node"
        },
        {
          "uri": "cim:Trunk",
          "label_cn": "干管/主线",
          "definition": "主要传输通道，承载大流量",
          "examples": ["高压母线", "冷冻水主管", "送风主管"],
          "source_trace": "Agent-01.Edge_Types.Trunk"
        },
        {
          "uri": "cim:Branch",
          "label_cn": "支管/支线",
          "definition": "从干线分出的次级通道",
          "examples": ["楼层配电", "楼层水平管", "支风管"],
          "source_trace": "Agent-01.Edge_Types.Branch"
        },
        {
          "uri": "cim:Terminal_Connection",
          "label_cn": "末端连接",
          "definition": "连接到末端设备的最后一段",
          "examples": ["风机盘管接管", "灯具线路"],
          "source_trace": "Agent-01.Edge_Types.Terminal_Connection"
        }
      ],
      "system_catalog": {
        "total_major_systems": 8,
        "total_subsystems": 26,
        "categories": [
          {"id": "HVAC", "name": "暖通空调系统", "subsystem_count": 8},
          {"id": "PLUMBING", "name": "给排水系统", "subsystem_count": 4},
          {"id": "ELECTRICAL", "name": "电气系统", "subsystem_count": 5},
          {"id": "MEDICAL_GAS", "name": "医疗气体系统", "subsystem_count": 3},
          {"id": "FIRE_PROTECTION", "name": "消防系统", "subsystem_count": 2},
          {"id": "VERTICAL_TRANSPORT", "name": "垂直交通系统", "subsystem_count": 2},
          {"id": "BUILDING_AUTOMATION", "name": "楼宇自动化系统", "subsystem_count": 1},
          {"id": "SPECIAL_MEDICAL", "name": "医疗专用系统", "subsystem_count": 1}
        ],
        "source_trace": "Agent-01.system_catalog"
      }
    },

    "space_domain": {
      "source_agent": "Agent-02",
      "source_section": "理论基础：空间层级模型",
      "hierarchy_levels": [
        {
          "level_id": "L0",
          "uri": "cim-space:Site",
          "label_cn": "院区",
          "description": "医疗机构的整体基地范围",
          "attributes": ["site_name", "total_area", "total_building_area"],
          "source_trace": "Agent-02.Space_Hierarchy.Level_0_Site"
        },
        {
          "level_id": "L1",
          "uri": "cim-space:Building",
          "label_cn": "建筑",
          "description": "单体建筑物",
          "attributes": ["building_code", "building_name", "building_type", "floor_count", "building_area"],
          "enum_building_type": ["门诊", "住院", "医技", "后勤", "综合"],
          "source_trace": "Agent-02.Space_Hierarchy.Level_1_Building"
        },
        {
          "level_id": "L2",
          "uri": "cim-space:Floor",
          "label_cn": "楼层",
          "description": "建筑楼层（地上/地下/夹层/屋顶）",
          "source_trace": "Agent-02.Space_Hierarchy.Level_2_Floor"
        },
        {
          "level_id": "L3",
          "uri": "cim-space:Zone",
          "label_cn": "功能区域",
          "description": "同一楼层内的功能分区",
          "zone_classification": {
            "医疗区": 4,
            "医技区": 3,
            "后勤区": 3,
            "公共区": 3
          },
          "source_trace": "Agent-02.Space_Hierarchy.Level_3_Zone"
        },
        {
          "level_id": "L4",
          "uri": "cim-space:Room",
          "label_cn": "房间",
          "description": "独立房间/空间",
          "source_trace": "Agent-02.Space_Hierarchy.Level_4_Room"
        },
        {
          "level_id": "L5",
          "uri": "cim-space:SubSpace",
          "label_cn": "子空间",
          "description": "房间内的子空间（如手术区、麻醉准备区）",
          "source_trace": "Agent-02.Space_Hierarchy.Level_5_SubSpace"
        }
      ],
      "medical_special_spaces": [
        {
          "uri": "cim-space:OperatingRoom",
          "label_cn": "手术室",
          "code": "OR",
          "cleanliness_classes": ["I级", "II级", "III级", "IV级"],
          "standard_reference": "GB50333-2013",
          "source_trace": "Agent-02.medical_special_spaces.operating_rooms"
        },
        {
          "uri": "cim-space:ICU",
          "label_cn": "重症监护室",
          "subtypes": ["综合ICU", "心脏ICU", "新生儿ICU"],
          "source_trace": "Agent-02.medical_special_spaces.ICU"
        },
        {
          "uri": "cim-space:IsolationWard",
          "label_cn": "隔离病房",
          "subtypes": ["正压隔离", "负压隔离"],
          "source_trace": "Agent-02.medical_special_spaces.isolation_ward"
        },
        {
          "uri": "cim-space:CleanLab",
          "label_cn": "洁净实验室",
          "biosafety_levels": ["BSL-1", "BSL-2", "BSL-3"],
          "source_trace": "Agent-02.medical_special_spaces.clean_lab"
        },
        {
          "uri": "cim-space:Pharmacy",
          "label_cn": "药房",
          "includes": ["PIVAs (静脉配置中心)"],
          "source_trace": "Agent-02.medical_special_spaces.pharmacy"
        },
        {
          "uri": "cim-space:CSSD",
          "label_cn": "供应室",
          "full_name": "中心供应室 (Central Sterile Supply Department)",
          "source_trace": "Agent-02.medical_special_spaces.CSSD"
        }
      ]
    },

    "equipment_domain": {
      "source_agent": "Agent-03",
      "source_section": "设备分类体系",
      "statistics": {
        "total_system_categories": 8,
        "total_equipment_families": 18,
        "total_equipment_types": 123,
        "topology_nodes_mapped": 156,
        "equipment_types_mapped": 89,
        "mapping_coverage": "57.1%",
        "p0_core_equipment_modeled": 18
      },
      "equipment_hierarchy": [
        {
          "level_id": "Level_1",
          "uri": "cim-equip:System",
          "label_cn": "系统",
          "definition": "完成特定功能的设备集合",
          "example": "1号冷站系统",
          "source_trace": "Agent-03.Equipment_Hierarchy.Level_1_System"
        },
        {
          "level_id": "Level_2",
          "uri": "cim-equip:Equipment",
          "label_cn": "设备",
          "definition": "独立的功能装置（本模型核心）",
          "example": "CH-001 离心式冷水机组",
          "source_trace": "Agent-03.Equipment_Hierarchy.Level_2_Equipment"
        },
        {
          "level_id": "Level_3",
          "uri": "cim-equip:Component",
          "label_cn": "组件",
          "definition": "设备的组成部分",
          "example": "CH-001-COMP 1号冷机压缩机",
          "source_trace": "Agent-03.Equipment_Hierarchy.Level_3_Component"
        },
        {
          "level_id": "Level_4",
          "uri": "cim-equip:Part",
          "label_cn": "零部件",
          "definition": "可更换的零部件",
          "example": "CH-001-FILTER 油过滤器",
          "source_trace": "Agent-03.Equipment_Hierarchy.Level_4_Part"
        }
      ],
      "reliability_classification": [
        {
          "level": "LIFE_SAFETY",
          "label_cn": "生命安全级",
          "equipment_count": 12,
          "examples": ["柴油发电机", "液氧储罐", "HEPA过滤器", "消火栓泵"],
          "source_trace": "Agent-03.reliability_classification"
        },
        {
          "level": "PATIENT_SAFETY",
          "label_cn": "患者安全级",
          "equipment_count": 15,
          "examples": ["医用隔离变压器", "洁净空调机组", "医疗气体设备"],
          "source_trace": "Agent-03.reliability_classification"
        },
        {
          "level": "CRITICAL",
          "label_cn": "关键级",
          "equipment_count": 48,
          "examples": ["冷水机组", "变压器", "UPS", "电梯"],
          "source_trace": "Agent-03.reliability_classification"
        },
        {
          "level": "IMPORTANT",
          "label_cn": "重要级",
          "equipment_count": 28,
          "source_trace": "Agent-03.reliability_classification"
        },
        {
          "level": "SECONDARY",
          "label_cn": "次要级",
          "equipment_count": 20,
          "source_trace": "Agent-03.reliability_classification"
        }
      ],
      "p0_core_equipment": [
        {"type": "离心式冷水机组", "system": "HVAC", "source_trace": "Agent-03.P0_Equipment"},
        {"type": "螺杆式冷水机组", "system": "HVAC", "source_trace": "Agent-03.P0_Equipment"},
        {"type": "洁净空调机组", "system": "HVAC", "source_trace": "Agent-03.P0_Equipment"},
        {"type": "HEPA高效过滤器", "system": "HVAC", "source_trace": "Agent-03.P0_Equipment"},
        {"type": "冷却塔", "system": "HVAC", "source_trace": "Agent-03.P0_Equipment"},
        {"type": "冷冻水泵/冷却水泵/热水泵", "system": "HVAC", "source_trace": "Agent-03.P0_Equipment"},
        {"type": "变风量VAV末端", "system": "HVAC", "source_trace": "Agent-03.P0_Equipment"},
        {"type": "电力变压器", "system": "ELECTRICAL", "source_trace": "Agent-03.P0_Equipment"},
        {"type": "高低压开关柜", "system": "ELECTRICAL", "source_trace": "Agent-03.P0_Equipment"},
        {"type": "柴油发电机组", "system": "ELECTRICAL", "source_trace": "Agent-03.P0_Equipment"},
        {"type": "UPS不间断电源", "system": "ELECTRICAL", "source_trace": "Agent-03.P0_Equipment"},
        {"type": "医用隔离变压器", "system": "ELECTRICAL", "source_trace": "Agent-03.P0_Equipment"},
        {"type": "配电柜", "system": "ELECTRICAL", "source_trace": "Agent-03.P0_Equipment"},
        {"type": "液氧储罐系统", "system": "MEDICAL_GAS", "source_trace": "Agent-03.P0_Equipment"},
        {"type": "医用真空系统", "system": "MEDICAL_GAS", "source_trace": "Agent-03.P0_Equipment"},
        {"type": "无油空压机", "system": "MEDICAL_GAS", "source_trace": "Agent-03.P0_Equipment"},
        {"type": "消火栓泵", "system": "FIRE_PROTECTION", "source_trace": "Agent-03.P0_Equipment"},
        {"type": "病床电梯", "system": "VERTICAL_TRANSPORT", "source_trace": "Agent-03.P0_Equipment"}
      ]
    },

    "flow_domain": {
      "source_agent": "Agent-04",
      "source_section": "流动模型三层架构",
      "version": "v2.3",
      "flow_layers": [
        {
          "layer_id": "Layer_1",
          "uri": "cim-flow:Mass_Flow",
          "label_cn": "物质流",
          "definition": "作为能量的载体在系统中流动的物质",
          "media": ["水", "空气", "蒸汽", "制冷剂", "医疗气体"],
          "characteristics": ["流量", "压力", "温度", "成分"],
          "source_trace": "Agent-04.Flow_Model.Layer_1"
        },
        {
          "layer_id": "Layer_2",
          "uri": "cim-flow:Energy_Flow",
          "label_cn": "能量流",
          "definition": "由物质流承载的能量传递",
          "source_trace": "Agent-04.Flow_Model.Layer_2"
        },
        {
          "layer_id": "Layer_3",
          "uri": "cim-flow:Information_Flow",
          "label_cn": "信息流",
          "definition": "控制信号和状态数据的传递",
          "source_trace": "Agent-04.Flow_Model.Layer_3"
        }
      ],
      "flow_sequence": {
        "uri": "cim-flow:FlowSequence",
        "definition": "从源到末端的完整流动通道",
        "types": ["Supply_Path (供应路径)", "Return_Path (回流路径)"],
        "source_trace": "Agent-04.Path"
      },
      "coupling_equations": {
        "description": "载体-荷载耦合方程",
        "source_trace": "Agent-04.coupling_equations"
      }
    },

    "coupling_domain": {
      "source_agent": "Agent-05",
      "source_section": "设备-位置模型",
      "version": "V2.1-RELEASE",
      "location_types": [
        {
          "type_id": "LOC-MEP-ROOM",
          "uri": "cim-loc:MEP_Room",
          "label_cn": "机电设备用房",
          "description": "专门用于放置机电设备的房间",
          "examples": ["冷冻站", "热力站", "变配电室", "水泵房"],
          "typical_floor": "地下室/屋顶",
          "source_trace": "Agent-05.Equipment_Location_Model.LOC-MEP-ROOM"
        },
        {
          "type_id": "LOC-SHAFT",
          "uri": "cim-loc:Shaft",
          "label_cn": "竖井",
          "description": "垂直方向的管线通道",
          "subtypes": ["电气竖井", "水暖竖井", "通风竖井"],
          "source_trace": "Agent-05.Equipment_Location_Model.LOC-SHAFT"
        },
        {
          "type_id": "LOC-CEILING",
          "uri": "cim-loc:Ceiling_Void",
          "label_cn": "吊顶内",
          "description": "吊顶与楼板之间的空间",
          "source_trace": "Agent-05.Equipment_Location_Model.LOC-CEILING"
        },
        {
          "type_id": "LOC-SERVED-SPACE",
          "uri": "cim-loc:Served_Space",
          "label_cn": "服务空间内",
          "description": "直接安装在被服务空间内的设备",
          "source_trace": "Agent-05.Equipment_Location_Model.LOC-SERVED-SPACE"
        }
      ],
      "equipment_location_rules": [
        {
          "equipment_type": "CHILLER",
          "location_type": "LOC-MEP-ROOM",
          "specific_room": "冷冻站",
          "constraints": ["荷载要求: 需要加强楼板", "吊装要求: 需要吊装孔或设备门", "减振要求: 需要减振基础"],
          "source_trace": "Agent-05.equipment_location_rules.CHILLER"
        },
        {
          "equipment_type": "AHU",
          "location_type": ["LOC-MEP-ROOM (空调机房)", "LOC-CEILING (吊顶内-小型)"],
          "constraints": ["检修空间: 需要足够的检修距离"],
          "source_trace": "Agent-05.equipment_location_rules.AHU"
        },
        {
          "equipment_type": "FCU",
          "location_type": ["LOC-CEILING (吊顶内)", "LOC-SERVED-SPACE (明装)"],
          "source_trace": "Agent-05.equipment_location_rules.FCU"
        }
      ],
      "coupling_statistics": {
        "total_coupling_units": 181,
        "total_spaces": 20,
        "total_systems": 45,
        "total_devices": 215,
        "system_equipment_mapping_complete": "87.2%",
        "equipment_space_allocation_complete": "92.8%",
        "source_trace": "Agent-05.V2.1-RELEASE.quality_assessment"
      }
    },

    "control_domain": {
      "source_agent": "Agent-06",
      "source_section": "控制系统建模",
      "statistics": {
        "total_sensors": 247,
        "total_actuators": 156,
        "total_control_loops": 87,
        "sensor_types_modeled": "50+",
        "actuator_types_modeled": "20+"
      },
      "sensor_model": [
        {
          "sensor_type_id": "SENSOR-TEMP",
          "uri": "cim-ctrl:Temperature_Sensor",
          "label_cn": "温度传感器",
          "measured_parameter": "temperature",
          "unit": "℃",
          "variants": [
            {"variant_id": "SENSOR-TEMP-PIPE", "label_cn": "管道式温度传感器", "mounting": "管道插入式"},
            {"variant_id": "SENSOR-TEMP-DUCT", "label_cn": "风管式温度传感器", "mounting": "风管插入式"},
            {"variant_id": "SENSOR-TEMP-ROOM", "label_cn": "室内温度传感器", "mounting": "墙挂式"}
          ],
          "static_attributes": [
            {"attr_name": "measurement_range", "typical_value": "-20~100"},
            {"attr_name": "accuracy", "typical_value": "±0.5℃"},
            {"attr_name": "output_signal", "typical_value": "4-20mA, 0-10V, Modbus"}
          ],
          "source_trace": "Agent-06.Sensor_Model.SENSOR-TEMP"
        }
      ],
      "actuator_model": [
        {
          "actuator_type_id": "ACTUATOR-VALVE",
          "uri": "cim-ctrl:Valve_Actuator",
          "label_cn": "调节阀执行器",
          "controlled_element": "阀门",
          "source_trace": "Agent-06.Actuator_Model.ACTUATOR-VALVE"
        }
      ],
      "controller_types": ["DDC", "PLC"],
      "control_strategies": ["冷站控制策略", "AHU控制策略", "洁净室控制策略"],
      "source_trace": "Agent-06.control_loop_models"
    },

    "metering_domain": {
      "source_agent": "Agent-07",
      "source_section": "计量层级模型",
      "statistics": {
        "metering_levels": 4,
        "energy_types": 7,
        "total_metering_points": 189
      },
      "metering_hierarchy": [
        {
          "level_id": "METER-L0",
          "uri": "cim-meter:Total_Meter",
          "label_cn": "总表层",
          "description": "院区/建筑总进线计量",
          "energy_types": ["电", "水", "气", "热"],
          "source_trace": "Agent-07.Metering_Hierarchy.METER-L0"
        },
        {
          "level_id": "METER-L1",
          "uri": "cim-meter:Zone_Meter",
          "label_cn": "区域表层",
          "description": "建筑/分区计量",
          "source_trace": "Agent-07.Metering_Hierarchy.METER-L1"
        },
        {
          "level_id": "METER-L2",
          "uri": "cim-meter:Tenant_Meter",
          "label_cn": "分户表层",
          "description": "科室/租户计量",
          "source_trace": "Agent-07.Metering_Hierarchy.METER-L2"
        },
        {
          "level_id": "METER-L3",
          "uri": "cim-meter:Subitem_Meter",
          "label_cn": "分项表层",
          "description": "用能类型/设备计量",
          "source_trace": "Agent-07.Metering_Hierarchy.METER-L3"
        }
      ],
      "allocation_rules": {
        "description": "能耗分摊规则定义",
        "source_trace": "Agent-07.allocation_rules"
      }
    },

    "om_domain": {
      "source_agent": "Agent-08",
      "source_section": "运维管理模型",
      "version": "v3.0",
      "work_order_model": {
        "order_types": 5,
        "status_transitions": 7,
        "includes": ["SLA服务等级协议", "优先级评估矩阵"],
        "source_trace": "Agent-08.work_order_models"
      },
      "maintenance_strategies": [
        {
          "strategy_id": "PM",
          "uri": "cim-om:Preventive_Maintenance",
          "label_cn": "预防性维护",
          "source_trace": "Agent-08.maintenance_strategies.PM"
        },
        {
          "strategy_id": "PdM",
          "uri": "cim-om:Predictive_Maintenance",
          "label_cn": "预测性维护",
          "source_trace": "Agent-08.maintenance_strategies.PdM"
        }
      ],
      "asset_lifecycle": {
        "stages_count": 9,
        "stages": ["COMMISSIONING", "OPERATION", "MAINTENANCE", "DEGRADATION", "DECOMMISSIONING"],
        "includes": ["关键时间节点定义", "LCC全生命周期成本", "替换决策模型"],
        "source_trace": "Agent-08.asset_lifecycle_models"
      },
      "alarm_system": {
        "levels": 4,
        "situation_patterns": 30,
        "source_trace": "Agent-08.alarm_models"
      }
    }
  },

  "extracted_relationships": [
    {
      "relation_id": "REL-001",
      "uri": "cim:locatedIn",
      "label_cn": "位于",
      "domain": "cim-equip:Equipment",
      "range": "cim-space:Space",
      "type": "Topological",
      "source_agent": "Agent-05",
      "source_trace": "Agent-05.equipment_location_model"
    },
    {
      "relation_id": "REL-002",
      "uri": "cim:serves",
      "label_cn": "服务于",
      "domain": "cim-equip:Equipment | cim:System",
      "range": "cim-space:Space | cim-space:Zone",
      "type": "Functional",
      "source_agent": "Agent-05",
      "source_trace": "Agent-05.service_space_model"
    },
    {
      "relation_id": "REL-003",
      "uri": "cim-flow:feedsTo",
      "label_cn": "供给至",
      "domain": "cim-equip:Equipment",
      "range": "cim-equip:Equipment",
      "type": "Flow",
      "properties": ["medium", "flowRate", "pressure", "temperature"],
      "source_agent": "Agent-04",
      "source_trace": "Agent-04.Flow_Sequence"
    },
    {
      "relation_id": "REL-004",
      "uri": "cim:contains",
      "label_cn": "包含",
      "domain": "cim-space:Space (higher level)",
      "range": "cim-space:Space (lower level)",
      "type": "Structural",
      "source_agent": "Agent-02",
      "source_trace": "Agent-02.Space_Hierarchy"
    },
    {
      "relation_id": "REL-005",
      "uri": "cim:componentOf",
      "label_cn": "组件属于",
      "domain": "cim-equip:Component",
      "range": "cim-equip:Equipment",
      "type": "Structural",
      "source_agent": "Agent-03",
      "source_trace": "Agent-03.Equipment_Hierarchy"
    },
    {
      "relation_id": "REL-006",
      "uri": "cim:dependsOn",
      "label_cn": "依赖于",
      "domain": "cim:System",
      "range": "cim:System",
      "type": "Dependency",
      "source_agent": "Agent-01",
      "source_trace": "Agent-01.system_dependencies"
    },
    {
      "relation_id": "REL-007",
      "uri": "cim-ctrl:monitors",
      "label_cn": "监测",
      "domain": "cim-ctrl:Sensor",
      "range": "cim-equip:Equipment | cim-space:Space",
      "type": "Control",
      "source_agent": "Agent-06",
      "source_trace": "Agent-06.sensor_models"
    },
    {
      "relation_id": "REL-008",
      "uri": "cim-ctrl:controls",
      "label_cn": "控制",
      "domain": "cim-ctrl:Actuator",
      "range": "cim-equip:Equipment",
      "type": "Control",
      "source_agent": "Agent-06",
      "source_trace": "Agent-06.actuator_models"
    },
    {
      "relation_id": "REL-009",
      "uri": "cim-meter:meters",
      "label_cn": "计量",
      "domain": "cim-meter:Meter",
      "range": "cim-equip:Equipment | cim-flow:Flow",
      "type": "Metering",
      "source_agent": "Agent-07",
      "source_trace": "Agent-07.metering_point_layout"
    },
    {
      "relation_id": "REL-010",
      "uri": "cim:routesThrough",
      "label_cn": "穿越",
      "domain": "cim:Pipe | cim:Duct | cim:Cable",
      "range": "cim-space:Space",
      "type": "Routing",
      "source_agent": "Agent-05",
      "source_trace": "Agent-05.routing_space_model"
    }
  ],

  "extracted_constraints": [
    {
      "constraint_id": "CST-TOPO-001",
      "rule": "所有系统都必须有源节点(Source_Node)",
      "type": "Completeness",
      "source_agent": "Agent-01",
      "source_section": "输出要求.完整性检查清单",
      "enforcement": "SHACL",
      "source_trace": "Agent-01.Validation.completeness_checks"
    },
    {
      "constraint_id": "CST-TOPO-002",
      "rule": "所有末端节点都必须能追溯到源节点",
      "type": "Connectivity",
      "source_agent": "Agent-01",
      "source_section": "输出要求.完整性检查清单",
      "enforcement": "SPARQL",
      "source_trace": "Agent-01.Validation.completeness_checks"
    },
    {
      "constraint_id": "CST-TOPO-003",
      "rule": "闭环系统必须有回流路径(Return_Path)",
      "type": "Topology",
      "source_agent": "Agent-01",
      "source_section": "输出要求.完整性检查清单",
      "enforcement": "SPARQL",
      "source_trace": "Agent-01.Validation.completeness_checks"
    },
    {
      "constraint_id": "CST-EQUIP-001",
      "rule": "Agent-01的每个拓扑节点在Agent-03中都必须有对应设备",
      "type": "Cross-Agent Consistency",
      "source_agent": "Agent-09",
      "source_section": "Validation_Rules.consistency_checks",
      "enforcement": "SPARQL",
      "source_trace": "Agent-09.Validation_Rules.节点-设备映射完整性"
    },
    {
      "constraint_id": "CST-SPACE-001",
      "rule": "Agent-03的设备在Agent-05中都必须有位置定义",
      "type": "Cross-Agent Consistency",
      "source_agent": "Agent-09",
      "source_section": "Validation_Rules.consistency_checks",
      "enforcement": "SPARQL",
      "source_trace": "Agent-09.Validation_Rules.设备-位置映射完整性"
    },
    {
      "constraint_id": "CST-CTRL-001",
      "rule": "Agent-06的传感器/执行器在Agent-03中必须已定义",
      "type": "Cross-Agent Consistency",
      "source_agent": "Agent-09",
      "source_section": "Validation_Rules.consistency_checks",
      "enforcement": "SPARQL",
      "source_trace": "Agent-09.Validation_Rules.控制回路-设备关联完整性"
    },
    {
      "constraint_id": "CST-METER-001",
      "rule": "Agent-07的计量点必须能追溯到Agent-03的设备",
      "type": "Cross-Agent Consistency",
      "source_agent": "Agent-09",
      "source_section": "Validation_Rules.consistency_checks",
      "enforcement": "SPARQL",
      "source_trace": "Agent-09.Validation_Rules.计量点-设备关联"
    }
  ]
}
```

---

## 📄 2. `medical_domain_constraints.json`

**医疗建筑领域约束库 - 基于国家标准**

```json
{
  "meta": {
    "file_id": "MDC-CIM-20250117",
    "description": "医疗建筑领域强制性约束库",
    "generated_from": "Agent-02, Agent-06, Agent-08 成果 + 国家标准",
    "standards_referenced": [
      "GB 50333-2013 医院洁净手术部建筑技术规范",
      "GB 51039-2014 综合医院建筑设计规范",
      "WS/T 311-2009 医院隔离技术规范",
      "GB 19489-2008 实验室生物安全通用要求",
      "JGJ 16-2008 民用建筑电气设计规范",
      "GB 50736-2012 民用建筑供暖通风与空气调节设计规范",
      "GB 50751-2012 医用气体工程技术规范",
      "GB/T 50378-2019 绿色建筑运行管理标准",
      "GB 50045-95 高层民用建筑设计防火规范"
    ]
  },

  "space_environmental_constraints": [
    {
      "constraint_id": "MED-OR-001",
      "target_class": "cim-space:OperatingRoom",
      "target_subtype": "Class_I (I级洁净手术室)",
      "standard_ref": "GB 50333-2013, Section 3.0.1",
      "requirements": {
        "cleanliness_class": {
          "property": "cim-space:cleanlinessClass",
          "operator": "EQUALS",
          "value": "ISO-5",
          "shacl_expression": "sh:hasValue 'ISO-5'"
        },
        "temperature_range": {
          "property": "cim-space:temperature",
          "operator": "BETWEEN",
          "min_value": 21,
          "max_value": 25,
          "unit": "°C",
          "shacl_expression": "sh:minInclusive 21; sh:maxInclusive 25"
        },
        "humidity_range": {
          "property": "cim-space:relativeHumidity",
          "operator": "BETWEEN",
          "min_value": 30,
          "max_value": 60,
          "unit": "%RH",
          "shacl_expression": "sh:minInclusive 30; sh:maxInclusive 60"
        },
        "pressure_differential": {
          "property": "cim-space:pressureDifferential",
          "operator": "GTE",
          "value": 15,
          "unit": "Pa",
          "reference_zone": "走廊",
          "shacl_expression": "sh:minInclusive 15"
        },
        "air_changes": {
          "property": "cim-space:airChangesPerHour",
          "operator": "BETWEEN",
          "min_value": 15,
          "max_value": 20,
          "unit": "ACH",
          "shacl_expression": "sh:minInclusive 15; sh:maxInclusive 20"
        }
      },
      "enforcement": "SHACL",
      "source_trace": "Agent-02.medical_special_spaces + GB50333-2013"
    },
    {
      "constraint_id": "MED-OR-002",
      "target_class": "cim-space:OperatingRoom",
      "target_subtype": "Class_II (II级洁净手术室)",
      "standard_ref": "GB 50333-2013",
      "requirements": {
        "cleanliness_class": {"value": "ISO-6"},
        "air_changes": {"min_value": 12, "max_value": 15}
      },
      "source_trace": "Agent-02.medical_special_spaces"
    },
    {
      "constraint_id": "MED-OR-003",
      "target_class": "cim-space:OperatingRoom",
      "target_subtype": "Class_III (III级洁净手术室)",
      "standard_ref": "GB 50333-2013",
      "requirements": {
        "cleanliness_class": {"value": "ISO-7"},
        "air_changes": {"min_value": 10, "max_value": 12}
      },
      "source_trace": "Agent-02.medical_special_spaces"
    },
    {
      "constraint_id": "MED-OR-004",
      "target_class": "cim-space:OperatingRoom",
      "target_subtype": "Class_IV (IV级洁净手术室)",
      "standard_ref": "GB 50333-2013",
      "requirements": {
        "cleanliness_class": {"value": "ISO-8"},
        "air_changes": {"min_value": 8, "max_value": 10}
      },
      "source_trace": "Agent-02.medical_special_spaces"
    },
    {
      "constraint_id": "MED-ISO-001",
      "target_class": "cim-space:IsolationWard",
      "target_subtype": "Negative_Pressure (负压隔离病房)",
      "standard_ref": "WS/T 311-2009",
      "requirements": {
        "pressure_differential": {
          "property": "cim-space:pressureDifferential",
          "operator": "LTE",
          "value": -10,
          "unit": "Pa",
          "reference_zone": "走廊"
        }
      },
      "source_trace": "Agent-02.medical_special_spaces.isolation_ward"
    },
    {
      "constraint_id": "MED-LAB-001",
      "target_class": "cim-space:CleanLab",
      "target_subtype": "BSL-3",
      "standard_ref": "GB 19489-2008",
      "requirements": {
        "pressure_differential": {
          "value": -30,
          "unit": "Pa"
        },
        "air_supply": "100%新风",
        "exhaust": "HEPA过滤后高空排放"
      },
      "source_trace": "Agent-02.medical_special_spaces.clean_lab"
    }
  ],

  "equipment_constraints": [
    {
      "constraint_id": "MED-EQUIP-001",
      "target_class": "cim-space:OperatingRoom",
      "rule": "必须配备独立净化空调机组",
      "required_equipment": ["cim-equip:Clean_AHU", "cim-equip:HEPA_Filter"],
      "standard_ref": "GB 50333-2013",
      "source_trace": "Agent-09.operation_theater_full_spec"
    },
    {
      "constraint_id": "MED-EQUIP-002",
      "target_class": "cim-space:OperatingRoom",
      "rule": "必须配备双电源+UPS+医用隔离电源",
      "required_equipment": [
        "cim-equip:Dual_Power_Supply",
        "cim-equip:UPS",
        "cim-equip:Medical_Isolation_Transformer",
        "cim-equip:Insulation_Monitor"
      ],
      "standard_ref": "GB 50333-2013 + JGJ 16-2008",
      "source_trace": "Agent-09.operation_theater_full_spec"
    },
    {
      "constraint_id": "MED-EQUIP-003",
      "target_class": "cim-space:OperatingRoom",
      "rule": "必须配备完整医用气体终端",
      "required_gas_terminals": ["O2 (氧气)", "N2O (笑气)", "Air (压缩空气)", "Vacuum (真空)"],
      "standard_ref": "GB 50751-2012",
      "source_trace": "Agent-09.operation_theater_full_spec"
    },
    {
      "constraint_id": "MED-EQUIP-004",
      "target_class": "cim-equip:Equipment",
      "target_reliability": "LIFE_SAFETY",
      "rule": "生命安全级设备必须有冗余配置",
      "redundancy_requirement": "N+1 或双路",
      "source_trace": "Agent-03.reliability_classification"
    }
  ],

  "system_constraints": [
    {
      "constraint_id": "MED-SYS-001",
      "target_system": "cim:HVAC_System",
      "target_space": "cim-space:OperatingRoom",
      "rule": "手术室空调恢复时间不超过30分钟",
      "property": "cim:recoveryTime",
      "operator": "LTE",
      "value": 30,
      "unit": "minutes",
      "standard_ref": "GB 50333-2013",
      "source_trace": "Agent-09.operation_theater_full_spec"
    },
    {
      "constraint_id": "MED-SYS-002",
      "target_system": "cim:Electrical_System",
      "target_space": "cim-space:OperatingRoom",
      "rule": "手术室必须配备应急照明",
      "property": "cim:hasEmergencyLighting",
      "value": true,
      "standard_ref": "GB 50045-95",
      "source_trace": "Agent-06.control_systems"
    }
  ]
}
```

---

## 📄 3. `cim_document_structure.md`

```markdown
# CIM 统一领域模型 - 目录结构定义

## 版本信息
- **版本**: v0.2.0-Alpha
- **生成日期**: 2025-01-17
- **生成工具**: Gemini CLI (本体工程索引与协调者)
- **目标路径**: `/project_deliverables/version02/cim/`

---

## 📁 目录树结构

```
cim/
├── 📁 core/                          # 核心元模型定义
│   ├── base_entities.ttl             # 基础实体定义 (Entity, Identity, Lifecycle)
│   ├── relationships.ttl             # 通用关系定义 (Structural, Topological, Functional)
│   └── datatypes.ttl                 # 自定义数据类型与枚举
│
├── 📁 topology/                       # 拓扑模型 (来源: Agent-01)
│   ├── node_types.ttl                # 节点类型 (Source, Sink, Distribution)
│   ├── edge_types.ttl                # 边类型 (Trunk, Branch, Terminal)
│   └── system_catalog.ttl            # 8大系统26子系统目录
│
├── 📁 spaces/                         # 空间模型 (来源: Agent-02)
│   ├── spatial_hierarchy.ttl         # 6级空间层级 (L0-L5)
│   ├── zone_classification.ttl       # 功能区分类 (医疗/医技/后勤/公共)
│   └── medical_special_spaces.ttl    # 医疗专用空间 (手术室/ICU/隔离病房)
│
├── 📁 equipment/                      # 设备本体 (来源: Agent-03)
│   ├── equipment_hierarchy.ttl       # 设备层级 (System/Equipment/Component/Part)
│   ├── mechanical.ttl                # HVAC设备 (42种)
│   ├── electrical.ttl                # 电气设备 (18种)
│   ├── plumbing.ttl                  # 给排水设备 (6种)
│   ├── medical_gas.ttl               # 医疗气体设备 (8种)
│   ├── fire_protection.ttl           # 消防设备 (5种)
│   ├── vertical_transport.ttl        # 垂直交通设备 (3种)
│   └── reliability_classification.ttl # 可靠性分级 (5级)
│
├── 📁 flow/                           # 流动模型 (来源: Agent-04)
│   ├── flow_layers.ttl               # 三层流动模型 (物质/能量/信息)
│   ├── flow_media.ttl                # 流动介质定义
│   └── flow_sequences.ttl            # 流动路径序列
│
├── 📁 coupling/                       # 耦合模型 (来源: Agent-05)
│   ├── equipment_location.ttl        # 设备-位置耦合
│   ├── routing_space.ttl             # 管路-空间穿越
│   └── service_relations.ttl         # 服务关系定义
│
├── 📁 control/                        # 控制模型 (来源: Agent-06)
│   ├── sensors.ttl                   # 传感器本体 (247个)
│   ├── actuators.ttl                 # 执行器本体 (156个)
│   ├── controllers.ttl               # 控制器定义 (DDC/PLC)
│   └── control_loops.ttl             # 控制回路 (87个)
│
├── 📁 metering/                       # 计量模型 (来源: Agent-07)
│   ├── metering_hierarchy.ttl        # 4级计量层级
│   ├── energy_media.ttl              # 7种能源介质
│   └── allocation_rules.ttl          # 分摊规则
│
├── 📁 operations/                     # 运维模型 (来源: Agent-08)
│   ├── work_orders.ttl               # 工单模型
│   ├── maintenance_strategies.ttl    # 维护策略 (PM/PdM)
│   ├── asset_lifecycle.ttl           # 资产生命周期
│   └── alarm_system.ttl              # 告警体系
│
├── 📁 services/                       # 服务定义
│   ├── chilled_water_service.ttl     # 冷冻水服务
│   ├── hot_water_service.ttl         # 热水服务
│   └── clean_air_service.ttl         # 洁净空气服务
│
├── 📁 rules/                          # 推理与验证规则
│   ├── equipment_merging_rules.sparql    # 设备合并规则
│   ├── service_inference_rules.sparql    # 服务推理规则
│   ├── cross_agent_validation.sparql     # 跨Agent一致性验证
│   └── shacl_constraints.ttl             # SHACL数据形状约束
│
├── 📁 medical_constraints/            # 医疗领域约束
│   ├── gb50333_cleanroom.ttl         # GB 50333 洁净规范约束
│   ├── gb51039_hospital.ttl          # GB 51039 医院规范约束
│   └── medical_gas_safety.ttl        # 医用气体安全约束
│
├── _index.ttl                        # 本体入口文件 (owl:imports清单)
├── _config.json                      # 项目配置与元数据
└── _glossary.json                    # 术语表与多语言标签
```

---

## 📊 文件-Agent来源映射表

| 目录 | 主要来源Agent | 次要依赖Agent | 文件数 |
|------|--------------|---------------|--------|
| `core/` | Agent-09 | - | 3 |
| `topology/` | **Agent-01** | - | 3 |
| `spaces/` | **Agent-02** | - | 3 |
| `equipment/` | **Agent-03** | Agent-01 | 8 |
| `flow/` | **Agent-04** | Agent-01 | 3 |
| `coupling/` | **Agent-05** | Agent-01, 02, 03 | 3 |
| `control/` | **Agent-06** | Agent-01, 03, 04 | 4 |
| `metering/` | **Agent-07** | Agent-01, 03, 05 | 3 |
| `operations/` | **Agent-08** | Agent-03, 06, 07 | 4 |
| `services/` | Agent-04, 05 | - | 3 |
| `rules/` | Agent-09 | All | 4 |
| `medical_constraints/` | Agent-02, 09 | - | 3 |

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
@prefix cim-svc:    <https://cim.medical/ontology/v3.4/services#> .
@prefix cim-med:    <https://cim.medical/ontology/v3.4/medical#> .
```
```

---

## 📄 4. `ontology_skeleton.ttl`

**本体骨架 - 基于Agent-01~08提取的顶层类与关系**

```turtle
# ============================================================================
# CIM Medical Building Unified Domain Model - Ontology Skeleton
# Version: 0.2.0-Alpha
# Generated: 2025-01-17
# Generator: Gemini CLI (本体工程索引与协调者)
# Source: Agent-01~08 Extraction Report
# ============================================================================

@prefix rdf:        <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:       <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl:        <http://www.w3.org/2002/07/owl#> .
@prefix xsd:        <http://www.w3.org/2001/XMLSchema#> .
@prefix skos:       <http://www.w3.org/2004/02/skos/core#> .
@prefix sh:         <http://www.w3.org/ns/shacl#> .

# CIM Namespace Declarations
@prefix cim:        <https://cim.medical/ontology/v3.4#> .
@prefix cim-topo:   <https://cim.medical/ontology/v3.4/topology#> .
@prefix cim-space:  <https://cim.medical/ontology/v3.4/space#> .
@prefix cim-equip:  <https://cim.medical/ontology/v3.4/equipment#> .
@prefix cim-flow:   <https://cim.medical/ontology/v3.4/flow#> .
@prefix cim-ctrl:   <https://cim.medical/ontology/v3.4/control#> .
@prefix cim-meter:  <https://cim.medical/ontology/v3.4/metering#> .
@prefix cim-om:     <https://cim.medical/ontology/v3.4/operations#> .

# ============================================================================
# ONTOLOGY METADATA
# ============================================================================

<https://cim.medical/ontology/v3.4>
    a owl:Ontology ;
    rdfs:label "CIM Medical Building Unified Domain Model"@en ;
    rdfs:label "医疗建筑CIM统一领域模型"@zh-CN ;
    rdfs:comment "Skeleton ontology generated from Agent-01~08 outputs for medical building MEP systems."@en ;
    owl:versionInfo "0.2.0-Alpha" ;
    owl:versionIRI <https://cim.medical/ontology/v3.4/0.2.0> .

# ============================================================================
# CORE BASE CLASSES (Agent-09 Integration Layer)
# ============================================================================

cim:Entity
    a owl:Class ;
    rdfs:label "Entity"@en ;
    rdfs:label "实体"@zh-CN ;
    rdfs:comment "The root abstract class for all CIM objects." ;
    skos:definition "Agent-01~08 所有输出对象的公共基类" .

cim:PhysicalObject
    a owl:Class ;
    rdfs:subClassOf cim:Entity ;
    rdfs:label "Physical Object"@en ;
    rdfs:label "物理对象"@zh-CN ;
    rdfs:comment "Objects that have physical presence in the building." .

cim:LogicalObject
    a owl:Class ;
    rdfs:subClassOf cim:Entity ;
    rdfs:label "Logical Object"@en ;
    rdfs:label "逻辑对象"@zh-CN ;
    rdfs:comment "Abstract concepts like systems, services, or processes." .

# ============================================================================
# TOPOLOGY DOMAIN (Source: Agent-01)
# ============================================================================

# Node Types
cim-topo:Node
    a owl:Class ;
    rdfs:subClassOf cim:LogicalObject ;
    rdfs:label "Topology Node"@en ;
    rdfs:label "拓扑节点"@zh-CN ;
    rdfs:comment "Abstract node in the system topology graph. Source: Agent-01.Node_Types" .

cim-topo:Source_Node
    a owl:Class ;
    rdfs:subClassOf cim-topo:Node ;
    rdfs:label "Source Node"@en ;
    rdfs:label "源节点"@zh-CN ;
    rdfs:comment "系统的能量/介质输入端，流动的起点。Source: Agent-01.Node_Types.Source_Node" .

cim-topo:Sink_Node
    a owl:Class ;
    rdfs:subClassOf cim-topo:Node ;
    rdfs:label "Sink Node"@en ;
    rdfs:label "末端节点"@zh-CN ;
    rdfs:comment "系统的能量/介质消耗端，流动的终点。Source: Agent-01.Node_Types.Sink_Node" .

cim-topo:Distribution_Node
    a owl:Class ;
    rdfs:subClassOf cim-topo:Node ;
    rdfs:label "Distribution Node"@en ;
    rdfs:label "分配节点"@zh-CN ;
    rdfs:comment "进行分配、汇集、调节的中间节点。Source: Agent-01.Node_Types.Distribution_Node" .

cim-topo:Junction
    a owl:Class ;
    rdfs:subClassOf cim-topo:Distribution_Node ;
    rdfs:label "Junction"@en ;
    rdfs:label "汇集点"@zh-CN ;
    rdfs:comment "多路输入汇聚为一路输出。示例：集水器、汇流排" .

cim-topo:Splitter
    a owl:Class ;
    rdfs:subClassOf cim-topo:Distribution_Node ;
    rdfs:label "Splitter"@en ;
    rdfs:label "分配点"@zh-CN ;
    rdfs:comment "一路输入分配为多路输出。示例：分水器、配电柜" .

cim-topo:Regulator
    a owl:Class ;
    rdfs:subClassOf cim-topo:Distribution_Node ;
    rdfs:label "Regulator"@en ;
    rdfs:label "调节点"@zh-CN ;
    rdfs:comment "对流量/压力/电压等进行调节。示例：调节阀、变频器" .

cim-topo:Transformer_Node
    a owl:Class ;
    rdfs:subClassOf cim-topo:Distribution_Node ;
    rdfs:label "Transformer Node"@en ;
    rdfs:label "转换点"@zh-CN ;
    rdfs:comment "改变介质形态或能量品位。示例：换热器、变压器、AHU" .

# Edge Types
cim-topo:Edge
    a owl:Class ;
    rdfs:subClassOf cim:LogicalObject ;
    rdfs:label "Topology Edge"@en ;
    rdfs:label "拓扑边"@zh-CN ;
    rdfs:comment "Connection between nodes in the topology graph." .

cim-topo:Trunk
    a owl:Class ;
    rdfs:subClassOf cim-topo:Edge ;
    rdfs:label "Trunk"@en ;
    rdfs:label "干管/主线"@zh-CN ;
    rdfs:comment "主要传输通道，承载大流量。示例：高压母线、冷冻水主管" .

cim-topo:Branch
    a owl:Class ;
    rdfs:subClassOf cim-topo:Edge ;
    rdfs:label "Branch"@en ;
    rdfs:label "支管/支线"@zh-CN ;
    rdfs:comment "从干线分出的次级通道。示例：楼层配电、楼层水平管" .

cim-topo:Terminal_Connection
    a owl:Class ;
    rdfs:subClassOf cim-topo:Edge ;
    rdfs:label "Terminal Connection"@en ;
    rdfs:label "末端连接"@zh-CN ;
    rdfs:comment "连接到末端设备的最后一段。示例：风机盘管接管、灯具线路" .

# System
cim-topo:System
    a owl:Class ;
    rdfs:subClassOf cim:LogicalObject ;
    rdfs:label "Technical System"@en ;
    rdfs:label "技术系统"@zh-CN ;
    rdfs:comment "8大系统26子系统的抽象类。Source: Agent-01.system_catalog" .

# ============================================================================
# SPACE DOMAIN (Source: Agent-02)
# ============================================================================

cim-space:Space
    a owl:Class ;
    rdfs:subClassOf cim:PhysicalObject ;
    rdfs:label "Space"@en ;
    rdfs:label "空间"@zh-CN ;
    rdfs:comment "Abstract class for all spatial entities. Source: Agent-02.Space_Hierarchy" .

cim-space:Site
    a owl:Class ;
    rdfs:subClassOf cim-space:Space ;
    rdfs:label "Site (L0)"@en ;
    rdfs:label "院区"@zh-CN ;
    rdfs:comment "医疗机构的整体基地范围。Source: Agent-02.Level_0_Site" .

cim-space:Building
    a owl:Class ;
    rdfs:subClassOf cim-space:Space ;
    rdfs:label "Building (L1)"@en ;
    rdfs:label "建筑"@zh-CN ;
    rdfs:comment "单体建筑物。Source: Agent-02.Level_1_Building" .

cim-space:Floor
    a owl:Class ;
    rdfs:subClassOf cim-space:Space ;
    rdfs:label "Floor (L2)"@en ;
    rdfs:label "楼层"@zh-CN ;
    rdfs:comment "建筑楼层（地上/地下/夹层/屋顶）。Source: Agent-02.Level_2_Floor" .

cim-space:Zone
    a owl:Class ;
    rdfs:subClassOf cim-space:Space ;
    rdfs:label "Zone (L3)"@en ;
    rdfs:label "功能区域"@zh-CN ;
    rdfs:comment "同一楼层内的功能分区。Source: Agent-02.Level_3_Zone" .

cim-space:Room
    a owl:Class ;
    rdfs:subClassOf cim-space:Space ;
    rdfs:label "Room (L4)"@en ;
    rdfs:label "房间"@zh-CN ;
    rdfs:comment "独立房间/空间。Source: Agent-02.Level_4_Room" .

cim-space:SubSpace
    a owl:Class ;
    rdfs:subClassOf cim-space:Space ;
    rdfs:label "SubSpace (L5)"@en ;
    rdfs:label "子空间"@zh-CN ;
    rdfs:comment "房间内的子空间。Source: Agent-02.Level_5_SubSpace" .

# Medical Special Spaces
cim-space:OperatingRoom
    a owl:Class ;
    rdfs:subClassOf cim-space:Room ;
    rdfs:label "Operating Room"@en ;
    rdfs:label "手术室"@zh-CN ;
    rdfs:comment "洁净手术室(I/II/III/IV级)。Standard: GB 50333-2013" .

cim-space:ICU
    a owl:Class ;
    rdfs:subClassOf cim-space:Room ;
    rdfs:label "ICU"@en ;
    rdfs:label "重症监护室"@zh-CN ;
    rdfs:comment "重症监护室。Source: Agent-02.medical_special_spaces.ICU" .

cim-space:IsolationWard
    a owl:Class ;
    rdfs:subClassOf cim-space:Room ;
    rdfs:label "Isolation Ward"@en ;
    rdfs:label "隔离病房"@zh-CN ;
    rdfs:comment "隔离病房（正压/负压）。Standard: WS/T 311-2009" .

# ============================================================================
# EQUIPMENT DOMAIN (Source: Agent-03)
# ============================================================================

cim-equip:Equipment
    a owl:Class ;
    rdfs:subClassOf cim:PhysicalObject ;
    rdfs:label "Equipment"@en ;
    rdfs:label "设备"@zh-CN ;
    rdfs:comment "独立的功能装置（本模型核心）。Source: Agent-03.Equipment_Hierarchy.Level_2" .

cim-equip:Component
    a owl:Class ;
    rdfs:subClassOf cim:PhysicalObject ;
    rdfs:label "Component"@en ;
    rdfs:label "组件"@zh-CN ;
    rdfs:comment "设备的组成部分。Source: Agent-03.Equipment_Hierarchy.Level_3" .

cim-equip:Part
    a owl:Class ;
    rdfs:subClassOf cim:PhysicalObject ;
    rdfs:label "Part"@en ;
    rdfs:label "零部件"@zh-CN ;
    rdfs:comment "可更换的零部件。Source: Agent-03.Equipment_Hierarchy.Level_4" .

# Equipment Categories (8大系统)
cim-equip:HVAC_Equipment
    a owl:Class ;
    rdfs:subClassOf cim-equip:Equipment ;
    rdfs:label "HVAC Equipment"@en ;
    rdfs:label "暖通空调设备"@zh-CN ;
    rdfs:comment "42种设备类型。Source: Agent-03.EQUIP-HVAC" .

cim-equip:Electrical_Equipment
    a owl:Class ;
    rdfs:subClassOf cim-equip:Equipment ;
    rdfs:label "Electrical Equipment"@en ;
    rdfs:label "电气设备"@zh-CN ;
    rdfs:comment "18种设备类型。Source: Agent-03.EQUIP-ELECTRICAL" .

cim-equip:MedicalGas_Equipment
    a owl:Class ;
    rdfs:subClassOf cim-equip:Equipment ;
    rdfs:label "Medical Gas Equipment"@en ;
    rdfs:label "医疗气体设备"@zh-CN ;
    rdfs:comment "8种设备类型。Source: Agent-03.EQUIP-MEDICAL_GAS" .

# ============================================================================
# FLOW DOMAIN (Source: Agent-04)
# ============================================================================

cim-flow:Flow
    a owl:Class ;
    rdfs:subClassOf cim:LogicalObject ;
    rdfs:label "Flow"@en ;
    rdfs:label "流动"@zh-CN ;
    rdfs:comment "Abstract flow class. Source: Agent-04.Flow_Model" .

cim-flow:Mass_Flow
    a owl:Class ;
    rdfs:subClassOf cim-flow:Flow ;
    rdfs:label "Mass Flow"@en ;
    rdfs:label "物质流"@zh-CN ;
    rdfs:comment "作为能量载体在系统中流动的物质。Source: Agent-04.Layer_1" .

cim-flow:Energy_Flow
    a owl:Class ;
    rdfs:subClassOf cim-flow:Flow ;
    rdfs:label "Energy Flow"@en ;
    rdfs:label "能量流"@zh-CN ;
    rdfs:comment "由物质流承载的能量传递。Source: Agent-04.Layer_2" .

cim-flow:Information_Flow
    a owl:Class ;
    rdfs:subClassOf cim-flow:Flow ;
    rdfs:label "Information Flow"@en ;
    rdfs:label "信息流"@zh-CN ;
    rdfs:comment "控制信号和状态数据的传递。Source: Agent-04.Layer_3" .

# ============================================================================
# CONTROL DOMAIN (Source: Agent-06)
# ============================================================================

cim-ctrl:ControlDevice
    a owl:Class ;
    rdfs:subClassOf cim-equip:Equipment ;
    rdfs:label "Control Device"@en ;
    rdfs:label "控制设备"@zh-CN ;
    rdfs:comment "Abstract class for control devices. Source: Agent-06" .

cim-ctrl:Sensor
    a owl:Class ;
    rdfs:subClassOf cim-ctrl:ControlDevice ;
    rdfs:label "Sensor"@en ;
    rdfs:label "传感器"@zh-CN ;
    rdfs:comment "247个传感器，50+类型。Source: Agent-06.sensor_models" .

cim-ctrl:Actuator
    a owl:Class ;
    rdfs:subClassOf cim-ctrl:ControlDevice ;
    rdfs:label "Actuator"@en ;
    rdfs:label "执行器"@zh-CN ;
    rdfs:comment "156个执行器，20+类型。Source: Agent-06.actuator_models" .

cim-ctrl:Controller
    a owl:Class ;
    rdfs:subClassOf cim-ctrl:ControlDevice ;
    rdfs:label "Controller"@en ;
    rdfs:label "控制器"@zh-CN ;
    rdfs:comment "DDC/PLC控制器。Source: Agent-06.controller_models" .

cim-ctrl:ControlLoop
    a owl:Class ;
    rdfs:subClassOf cim:LogicalObject ;
    rdfs:label "Control Loop"@en ;
    rdfs:label "控制回路"@zh-CN ;
    rdfs:comment "87个控制回路。Source: Agent-06.control_loop_models" .

# ============================================================================
# METERING DOMAIN (Source: Agent-07)
# ============================================================================

cim-meter:Meter
    a owl:Class ;
    rdfs:subClassOf cim-equip:Equipment ;
    rdfs:label "Meter"@en ;
    rdfs:label "计量表"@zh-CN ;
    rdfs:comment "189个计量点。Source: Agent-07.metering_point_layout" .

cim-meter:MeteringHierarchy
    a owl:Class ;
    rdfs:subClassOf cim:LogicalObject ;
    rdfs:label "Metering Hierarchy"@en ;
    rdfs:label "计量层级"@zh-CN ;
    rdfs:comment "4级计量层级。Source: Agent-07.metering_hierarchy" .

# ============================================================================
# OPERATIONS DOMAIN (Source: Agent-08)
# ============================================================================

cim-om:WorkOrder
    a owl:Class ;
    rdfs:subClassOf cim:LogicalObject ;
    rdfs:label "Work Order"@en ;
    rdfs:label "工单"@zh-CN ;
    rdfs:comment "5类工单类型，7个状态流转。Source: Agent-08.work_order_models" .

cim-om:MaintenanceStrategy
    a owl:Class ;
    rdfs:subClassOf cim:LogicalObject ;
    rdfs:label "Maintenance Strategy"@en ;
    rdfs:label "维护策略"@zh-CN ;
    rdfs:comment "PM/PdM维护策略。Source: Agent-08.maintenance_strategies" .

cim-om:AssetLifecycle
    a owl:Class ;
    rdfs:subClassOf cim:LogicalObject ;
    rdfs:label "Asset Lifecycle"@en ;
    rdfs:label "资产生命周期"@zh-CN ;
    rdfs:comment "9个生命周期状态。Source: Agent-08.asset_lifecycle_models" .

# ============================================================================
# KEY RELATIONSHIPS
# ============================================================================

# Topological Relations
cim:locatedIn
    a owl:ObjectProperty ;
    rdfs:label "located in"@en ;
    rdfs:label "位于"@zh-CN ;
    rdfs:domain cim-equip:Equipment ;
    rdfs:range cim-space:Space ;
    rdfs:comment "Source: Agent-05.equipment_location_model" .

cim:contains
    a owl:ObjectProperty, owl:TransitiveProperty ;
    rdfs:label "contains"@en ;
    rdfs:label "包含"@zh-CN ;
    rdfs:domain cim-space:Space ;
    rdfs:range cim-space:Space ;
    rdfs:comment "Source: Agent-02.Space_Hierarchy" .

# Functional Relations
cim:serves
    a owl:ObjectProperty ;
    rdfs:label "serves"@en ;
    rdfs:label "服务于"@zh-CN ;
    rdfs:domain [ owl:unionOf (cim-equip:Equipment cim-topo:System) ] ;
    rdfs:range cim-space:Space ;
    rdfs:comment "Source: Agent-05.service_space_model" .

# Flow Relations
cim-flow:feedsTo
    a owl:ObjectProperty ;
    rdfs:label "feeds to"@en ;
    rdfs:label "供给至"@zh-CN ;
    rdfs:domain cim-equip:Equipment ;
    rdfs:range cim-equip:Equipment ;
    rdfs:comment "Source: Agent-04.Flow_Sequence" .

# Structural Relations
cim:componentOf
    a owl:ObjectProperty ;
    rdfs:label "component of"@en ;
    rdfs:label "组件属于"@zh-CN ;
    rdfs:domain cim-equip:Component ;
    rdfs:range cim-equip:Equipment ;
    rdfs:comment "Source: Agent-03.Equipment_Hierarchy" .

# System Dependencies
cim:dependsOn
    a owl:ObjectProperty ;
    rdfs:label "depends on"@en ;
    rdfs:label "依赖于"@zh-CN ;
    rdfs:domain cim-topo:System ;
    rdfs:range cim-topo:System ;
    rdfs:comment "Source: Agent-01.system_dependencies" .

# Control Relations
cim-ctrl:monitors
    a owl:ObjectProperty ;
    rdfs:label "monitors"@en ;
    rdfs:label "监测"@zh-CN ;
    rdfs:domain cim-ctrl:Sensor ;
    rdfs:range [ owl:unionOf (cim-equip:Equipment cim-space:Space) ] ;
    rdfs:comment "Source: Agent-06.sensor_models" .

cim-ctrl:controls
    a owl:ObjectProperty ;
    rdfs:label "controls"@en ;
    rdfs:label "控制"@zh-CN ;
    rdfs:domain cim-ctrl:Actuator ;
    rdfs:range cim-equip:Equipment ;
    rdfs:comment "Source: Agent-06.actuator_models" .

# Metering Relations
cim-meter:meters
    a owl:ObjectProperty ;
    rdfs:label "meters"@en ;
    rdfs:label "计量"@zh-CN ;
    rdfs:domain cim-meter:Meter ;
    rdfs:range [ owl:unionOf (cim-equip:Equipment cim-flow:Flow) ] ;
    rdfs:comment "Source: Agent-07.metering_point_layout" .

# Routing Relations
cim:routesThrough
    a owl:ObjectProperty ;
    rdfs:label "routes through"@en ;
    rdfs:label "穿越"@zh-CN ;
    rdfs:domain cim:PhysicalObject ;
    rdfs:range cim-space:Space ;
    rdfs:comment "Source: Agent-05.routing_space_model" .

# ============================================================================
# END OF SKELETON
# ============================================================================
```

---

## 📄 5. `task_manifest.json`

**完整任务清单 - 包含依赖关系与验证规则**

```json
{
  "manifest_meta": {
    "manifest_id": "TM-CIM-20250117",
    "version": "1.0.0",
    "generated_by": "Gemini-CLI (本体工程索引与协调者)",
    "generated_at": "2025-01-17T16:30:00Z",
    "executor": "Claude-Code",
    "execution_strategy": "Topological Sort (DAG-based)"
  },

  "config_reference": {
    "path": "./cim/_config.json",
    "validation_library_path": "./_config.json#validation_library"
  },

  "task_groups": {
    "phase_1_foundation": {
      "description": "基础层 - 核心定义，无外部依赖",
      "parallel_execution": true,
      "tasks": ["TASK-001", "TASK-002", "TASK-003"]
    },
    "phase_2_domain_models": {
      "description": "领域层 - 依赖基础层",
      "parallel_execution": true,
      "tasks": ["TASK-004", "TASK-005", "TASK-006"]
    },
    "phase_3_integration": {
      "description": "集成层 - 依赖领域层",
      "parallel_execution": true,
      "tasks": ["TASK-007", "TASK-008", "TASK-009"]
    },
    "phase_4_rules": {
      "description": "规则层 - 依赖所有前置层",
      "parallel_execution": false,
      "tasks": ["TASK-010", "TASK-011", "TASK-012"]
    }
  },

  "tasks": [
    {
      "id": "TASK-001",
      "priority": "P0-Critical",
      "target_file": "cim/core/base_entities.ttl",
      "description": "实现核心基类定义 (Entity, PhysicalObject, LogicalObject) 及ID语义规范",
      "source_agents": ["Agent-09"],
      "concepts_to_implement": [
        "cim:Entity",
        "cim:PhysicalObject",
        "cim:LogicalObject",
        "cim:id (hash8语义)",
        "cim:sourceAgent",
        "cim:lastModified"
      ],
      "dependencies": [],
      "input_documents": [
        "concept_extraction_report.json#extracted_entities",
        "Agent-09 v3.4 PHASE-F"
      ],
      "validation_rules": [
        {
          "rule_id": "VAL-ID-FORMAT",
          "type": "Regex",
          "expression": "^[A-Z]{3}-[a-f0-9]{8}-\\d{3}$",
          "target_property": "cim:id",
          "error_message": "ID格式违规：必须符合PHASE-F规范 (e.g., EQP-a1b2c3d4-001)"
        },
        {
          "rule_id": "VAL-DATETIME",
          "type": "Regex",
          "expression": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z$",
          "target_property": "cim:lastModified",
          "error_message": "时间戳必须为ISO8601格式"
        }
      ],
      "output_validation": {
        "syntax_check": "turtle-validator",
        "ontology_check": "reasoner-hermit"
      }
    },
    {
      "id": "TASK-002",
      "priority": "P0-Critical",
      "target_file": "cim/topology/node_types.ttl",
      "description": "实现Agent-01定义的拓扑节点类型 (Source, Sink, Distribution及其子类型)",
      "source_agents": ["Agent-01"],
      "concepts_to_implement": [
        "cim-topo:Node",
        "cim-topo:Source_Node",
        "cim-topo:Sink_Node",
        "cim-topo:Distribution_Node",
        "cim-topo:Junction",
        "cim-topo:Splitter",
        "cim-topo:Regulator",
        "cim-topo:Transformer_Node"
      ],
      "dependencies": ["TASK-001"],
      "input_documents": [
        "concept_extraction_report.json#extracted_entities.topology_domain",
        "Agent01_Output.topology_definitions"
      ],
      "validation_rules": [
        {
          "rule_id": "VAL-TOPO-SUBCLASS",
          "type": "SPARQL-ASK",
          "query": "ASK { ?node rdfs:subClassOf+ cim-topo:Node }",
          "error_message": "所有节点类型必须是cim-topo:Node的子类"
        }
      ]
    },
    {
      "id": "TASK-003",
      "priority": "P0-Critical",
      "target_file": "cim/spaces/spatial_hierarchy.ttl",
      "description": "实现Agent-02定义的6级空间层级 (L0-L5)",
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
        "concept_extraction_report.json#extracted_entities.space_domain",
        "Agent02_Output.space_hierarchy_model.yaml"
      ],
      "validation_rules": [
        {
          "rule_id": "VAL-SPACE-HIERARCHY",
          "type": "SHACL",
          "shape": "每个空间类必须有正确的parent_level定义",
          "error_message": "空间层级关系必须符合L0→L1→L2→L3→L4→L5"
        }
      ]
    },
    {
      "id": "TASK-004",
      "priority": "P0-Critical",
      "target_file": "cim/spaces/medical_special_spaces.ttl",
      "description": "实现医疗专用空间定义，包含GB 50333约束",
      "source_agents": ["Agent-02", "Agent-09"],
      "concepts_to_implement": [
        "cim-space:OperatingRoom (I/II/III/IV级)",
        "cim-space:ICU",
        "cim-space:IsolationWard",
        "cim-space:CleanLab (BSL-1/2/3)",
        "cim-space:Pharmacy",
        "cim-space:CSSD"
      ],
      "dependencies": ["TASK-003"],
      "input_documents": [
        "concept_extraction_report.json#extracted_entities.space_domain.medical_special_spaces",
        "medical_domain_constraints.json",
        "Agent02_Output.medical_special_spaces.yaml"
      ],
      "validation_rules": [
        {
          "rule_id": "VAL-OR-ISO5",
          "type": "SHACL",
          "condition": "cim-space:surgeryGrade = 'Class_I'",
          "requirement": "cim-space:cleanlinessClass = 'ISO-5'",
          "standard_ref": "GB 50333-2013, Section 3.0.1",
          "error_message": "I级洁净手术室必须满足ISO-5洁净度"
        },
        {
          "rule_id": "VAL-OR-TEMP",
          "type": "SHACL",
          "target": "cim-space:OperatingRoom",
          "property": "cim-space:temperature",
          "sh:minInclusive": 21,
          "sh:maxInclusive": 25,
          "error_message": "手术室温度必须在21-25°C范围内"
        },
        {
          "rule_id": "VAL-OR-PRESSURE",
          "type": "SHACL",
          "target": "cim-space:OperatingRoom",
          "property": "cim-space:pressureDifferential",
          "sh:minInclusive": 15,
          "unit": "Pa",
          "error_message": "手术室对走廊压差不小于15Pa"
        }
      ]
    },
    {
      "id": "TASK-005",
      "priority": "P0-Critical",
      "target_file": "cim/equipment/equipment_hierarchy.ttl",
      "description": "实现Agent-03定义的设备层级与可靠性分级",
      "source_agents": ["Agent-03"],
      "concepts_to_implement": [
        "cim-equip:Equipment (Level_2)",
        "cim-equip:Component (Level_3)",
        "cim-equip:Part (Level_4)",
        "Reliability: LIFE_SAFETY, PATIENT_SAFETY, CRITICAL, IMPORTANT, SECONDARY"
      ],
      "dependencies": ["TASK-001"],
      "input_documents": [
        "concept_extraction_report.json#extracted_entities.equipment_domain",
        "Agent03_Output.equipment_classification",
        "Agent03_Output.equipment_type_models"
      ],
      "validation_rules": [
        {
          "rule_id": "VAL-EQUIP-RELIABILITY",
          "type": "Enum",
          "property": "cim-equip:reliabilityLevel",
          "allowed_values": ["LIFE_SAFETY", "PATIENT_SAFETY", "CRITICAL", "IMPORTANT", "SECONDARY"],
          "error_message": "设备可靠性分级必须为5级之一"
        }
      ]
    },
    {
      "id": "TASK-006",
      "priority": "P1-Important",
      "target_file": "cim/equipment/mechanical.ttl",
      "description": "实现HVAC设备本体 (42种设备类型)",
      "source_agents": ["Agent-03"],
      "concepts_to_implement": [
        "cim-equip:HVAC_Equipment",
        "cim-equip:Chiller (离心式/螺杆式)",
        "cim-equip:AHU (洁净空调机组)",
        "cim-equip:HEPA_Filter",
        "cim-equip:CoolingTower",
        "cim-equip:Pump (冷冻水/冷却水/热水)",
        "cim-equip:VAV_Terminal"
      ],
      "dependencies": ["TASK-002", "TASK-005"],
      "input_documents": [
        "Agent03_Output.equipment_type_models",
        "Agent01_Output.topology_definitions (节点映射)"
      ],
      "validation_rules": [
        {
          "rule_id": "VAL-CHILLER-COP",
          "type": "Range",
          "property": "cim-equip:cop",
          "min": 4.0,
          "max": 7.5,
          "error_message": "冷水机组COP应在4.0-7.5范围内"
        },
        {
          "rule_id": "VAL-NODE-MAPPING",
          "type": "SPARQL-ASK",
          "query": "ASK { ?equip cim:mapsToNode ?node . ?node a cim-topo:Node }",
          "error_message": "HVAC设备必须映射到有效的拓扑节点"
        }
      ]
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
        "cim:locatedIn关系",
        "设备位置规则与约束"
      ],
      "dependencies": ["TASK-003", "TASK-005", "TASK-006"],
      "input_documents": [
        "concept_extraction_report.json#extracted_entities.coupling_domain",
        "Agent05_Output.equipment_location_model"
      ],
      "validation_rules": [
        {
          "rule_id": "VAL-CHILLER-LOCATION",
          "type": "SPARQL-ASK",
          "query": "ASK { ?chiller a cim-equip:Chiller . ?chiller cim:locatedIn ?room . ?room a cim-loc:MEP_Room }",
          "error_message": "冷水机组必须位于机电设备用房(冷冻站)"
        },
        {
          "rule_id": "VAL-EQUIP-HAS-LOCATION",
          "type": "SHACL",
          "target": "cim-equip:Equipment",
          "property": "cim:locatedIn",
          "sh:minCount": 1,
          "error_message": "每个设备必须定义位置 (Agent-09.CST-SPACE-001)"
        }
      ]
    },
    {
      "id": "TASK-008",
      "priority": "P1-Important",
      "target_file": "cim/control/sensors.ttl",
      "description": "实现Agent-06定义的传感器本体 (247个, 50+类型)",
      "source_agents": ["Agent-06"],
      "concepts_to_implement": [
        "cim-ctrl:Sensor",
        "cim-ctrl:Temperature_Sensor (PIPE/DUCT/ROOM)",
        "cim-ctrl:Humidity_Sensor",
        "cim-ctrl:Pressure_Sensor",
        "传感器属性: range, accuracy, output_signal"
      ],
      "dependencies": ["TASK-005"],
      "input_documents": [
        "concept_extraction_report.json#extracted_entities.control_domain.sensor_model",
        "Agent06_Output.sensor_models"
      ],
      "validation_rules": [
        {
          "rule_id": "VAL-SENSOR-IN-EQUIP",
          "type": "SPARQL-ASK",
          "query": "ASK { ?sensor a cim-ctrl:Sensor . ?sensor cim:mapsToEquipment ?equip . ?equip a cim-equip:Equipment }",
          "error_message": "传感器必须关联到Agent-03定义的设备 (Agent-09.CST-CTRL-001)"
        }
      ]
    },
    {
      "id": "TASK-009",
      "priority": "P1-Important",
      "target_file": "cim/metering/metering_hierarchy.ttl",
      "description": "实现Agent-07定义的4级计量层级",
      "source_agents": ["Agent-07"],
      "concepts_to_implement": [
        "cim-meter:MeteringHierarchy",
        "cim-meter:Total_Meter (L0)",
        "cim-meter:Zone_Meter (L1)",
        "cim-meter:Tenant_Meter (L2)",
        "cim-meter:Subitem_Meter (L3)",
        "7种能源介质类型"
      ],
      "dependencies": ["TASK-005", "TASK-007"],
      "input_documents": [
        "concept_extraction_report.json#extracted_entities.metering_domain",
        "Agent07_Output.metering_hierarchy",
        "Agent07_Output.energy_media_models"
      ],
      "validation_rules": [
        {
          "rule_id": "VAL-METER-TRACEABLE",
          "type": "SPARQL-ASK",
          "query": "ASK { ?meter cim-meter:meters ?equip . ?equip a cim-equip:Equipment }",
          "error_message": "计量点必须能追溯到设备 (Agent-09.CST-METER-001)"
        }
      ]
    },
    {
      "id": "TASK-010",
      "priority": "P1-Important",
      "target_file": "cim/rules/cross_agent_validation.sparql",
      "description": "实现Agent-09定义的跨Agent一致性验证规则",
      "source_agents": ["Agent-09"],
      "concepts_to_implement": [
        "节点-设备映射完整性验证",
        "设备-位置映射完整性验证",
        "空间-系统需求覆盖验证",
        "流动路径-拓扑一致性验证",
        "控制回路-设备关联完整性验证",
        "计量点-设备关联验证"
      ],
      "dependencies": ["TASK-002", "TASK-003", "TASK-006", "TASK-007", "TASK-008", "TASK-009"],
      "input_documents": [
        "concept_extraction_report.json#extracted_constraints",
        "Agent-09 Validation_Rules.consistency_checks"
      ],
      "validation_rules": [
        {
          "rule_id": "VAL-SPARQL-SYNTAX",
          "type": "SPARQL-Parser",
          "error_message": "SPARQL查询语法错误"
        }
      ]
    },
    {
      "id": "TASK-011",
      "priority": "P1-Important",
      "target_file": "cim/rules/shacl_constraints.ttl",
      "description": "实现医疗领域SHACL数据形状约束",
      "source_agents": ["Agent-02", "Agent-09"],
      "concepts_to_implement": [
        "OperatingRoomShape (温度/湿度/压差/洁净度)",
        "IsolationWardShape (负压要求)",
        "EquipmentLocationShape",
        "ReliabilityLevelShape"
      ],
      "dependencies": ["TASK-004", "TASK-005", "TASK-007"],
      "input_documents": [
        "medical_domain_constraints.json",
        "concept_extraction_report.json#extracted_constraints"
      ],
      "validation_rules": [
        {
          "rule_id": "VAL-SHACL-SYNTAX",
          "type": "SHACL-Validator",
          "error_message": "SHACL形状定义语法错误"
        }
      ]
    },
    {
      "id": "TASK-012",
      "priority": "P2-Enhancement",
      "target_file": "cim/_index.ttl",
      "description": "生成本体入口文件，包含所有模块的owl:imports",
      "source_agents": [],
      "concepts_to_implement": [
        "owl:Ontology声明",
        "owl:imports (all .ttl files)",
        "命名空间前缀注册"
      ],
      "dependencies": ["TASK-001", "TASK-002", "TASK-003", "TASK-004", "TASK-005", "TASK-006", "TASK-007", "TASK-008", "TASK-009", "TASK-010", "TASK-011"],
      "input_documents": [
        "cim_document_structure.md"
      ],
      "validation_rules": [
        {
          "rule_id": "VAL-IMPORTS-EXIST",
          "type": "FileSystem",
          "check": "所有owl:imports引用的文件必须存在",
          "error_message": "导入的本体文件不存在"
        }
      ]
    }
  ],

  "execution_order": [
    {"phase": 1, "tasks": ["TASK-001"], "parallel": false},
    {"phase": 2, "tasks": ["TASK-002", "TASK-003", "TASK-005"], "parallel": true},
    {"phase": 3, "tasks": ["TASK-004", "TASK-006"], "parallel": true},
    {"phase": 4, "tasks": ["TASK-007", "TASK-008", "TASK-009"], "parallel": true},
    {"phase": 5, "tasks": ["TASK-010", "TASK-011"], "parallel": true},
    {"phase": 6, "tasks": ["TASK-012"], "parallel": false}
  ]
}
```

---

## 📄 6. `dependency_graph.json`

**任务与概念依赖关系图 (DAG)**

```json
{
  "graph_meta": {
    "graph_id": "DEP-CIM-20250117",
    "type": "Directed Acyclic Graph (DAG)",
    "description": "CIM本体工程任务与概念依赖关系图",
    "generated_from": "Agent-01~08依赖分析"
  },

  "agent_dependencies": {
    "description": "Agent间的数据流依赖关系 (从知识库确认)",
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
      {"from": "Agent-01", "to": "Agent-06", "data": "控制节点"},
      {"from": "Agent-01", "to": "Agent-07", "data": "系统拓扑结构"},
      {"from": "Agent-02", "to": "Agent-05", "data": "空间本体、医疗空间"},
      {"from": "Agent-02", "to": "Agent-08", "data": "空间分类"},
      {"from": "Agent-03", "to": "Agent-05", "data": "设备本体、节点映射"},
      {"from": "Agent-03", "to": "Agent-06", "data": "设备本体(控制属性)"},
      {"from": "Agent-03", "to": "Agent-07", "data": "设备本体(计量设备)"},
      {"from": "Agent-03", "to": "Agent-08", "data": "设备本体(告警规则)"},
      {"from": "Agent-04", "to": "Agent-06", "data": "流动模型(需控制参数)"},
      {"from": "Agent-04", "to": "Agent-07", "data": "流动模型(能量计算)"},
      {"from": "Agent-05", "to": "Agent-06", "data": "超图拓扑耦合"},
      {"from": "Agent-05", "to": "Agent-07", "data": "系统-空间耦合关系"},
      {"from": "Agent-05", "to": "Agent-08", "data": "服务关系"},
      {"from": "Agent-06", "to": "Agent-08", "data": "控制系统模型"},
      {"from": "Agent-07", "to": "Agent-08", "data": "计量体系模型"},
      {"from": "Agent-08", "to": "Agent-09", "data": "运维管理模型"},
      {"from": "Agent-01", "to": "Agent-09", "data": "所有Agent输出"},
      {"from": "Agent-02", "to": "Agent-09", "data": "所有Agent输出"},
      {"from": "Agent-03", "to": "Agent-09", "data": "所有Agent输出"},
      {"from": "Agent-04", "to": "Agent-09", "data": "所有Agent输出"},
      {"from": "Agent-05", "to": "Agent-09", "data": "所有Agent输出"},
      {"from": "Agent-06", "to": "Agent-09", "data": "所有Agent输出"},
      {"from": "Agent-07", "to": "Agent-09", "data": "所有Agent输出"}
    ]
  },

  "task_dependencies": {
    "description": "本体工程任务依赖DAG",
    "nodes": {
      "TASK-001": {"file": "core/base_entities.ttl", "critical_path": true},
      "TASK-002": {"file": "topology/node_types.ttl", "critical_path": true},
      "TASK-003": {"file": "spaces/spatial_hierarchy.ttl", "critical_path": true},
      "TASK-004": {"file": "spaces/medical_special_spaces.ttl", "critical_path": true},
      "TASK-005": {"file": "equipment/equipment_hierarchy.ttl", "critical_path": true},
      "TASK-006": {"file": "equipment/mechanical.ttl", "critical_path": false},
      "TASK-007": {"file": "coupling/equipment_location.ttl", "critical_path": true},
      "TASK-008": {"file": "control/sensors.ttl", "critical_path": false},
      "TASK-009": {"file": "metering/metering_hierarchy.ttl", "critical_path": false},
      "TASK-010": {"file": "rules/cross_agent_validation.sparql", "critical_path": true},
      "TASK-011": {"file": "rules/shacl_constraints.ttl", "critical_path": true},
      "TASK-012": {"file": "_index.ttl", "critical_path": true}
    },
    "edges": [
      {"from": "TASK-001", "to": "TASK-002", "reason": "节点类型需继承Entity基类"},
      {"from": "TASK-001", "to": "TASK-003", "reason": "空间类型需继承Entity基类"},
      {"from": "TASK-001", "to": "TASK-005", "reason": "设备类型需继承Entity基类"},
      {"from": "TASK-003", "to": "TASK-004", "reason": "医疗专用空间需继承Room类"},
      {"from": "TASK-002", "to": "TASK-006", "reason": "HVAC设备需映射到拓扑节点"},
      {"from": "TASK-005", "to": "TASK-006", "reason": "HVAC设备需继承Equipment类"},
      {"from": "TASK-003", "to": "TASK-007", "reason": "位置耦合需引用空间类"},
      {"from": "TASK-005", "to": "TASK-007", "reason": "位置耦合需引用设备类"},
      {"from": "TASK-006", "to": "TASK-007", "reason": "位置耦合需包含HVAC设备"},
      {"from": "TASK-005", "to": "TASK-008", "reason": "传感器需关联到设备"},
      {"from": "TASK-005", "to": "TASK-009", "reason": "计量需关联到设备"},
      {"from": "TASK-007", "to": "TASK-009", "reason": "计量需引用设备位置"},
      {"from": "TASK-002", "to": "TASK-010", "reason": "验证规则需检查拓扑一致性"},
      {"from": "TASK-003", "to": "TASK-010", "reason": "验证规则需检查空间覆盖"},
      {"from": "TASK-006", "to": "TASK-010", "reason": "验证规则需检查设备映射"},
      {"from": "TASK-007", "to": "TASK-010", "reason": "验证规则需检查位置耦合"},
      {"from": "TASK-008", "to": "TASK-010", "reason": "验证规则需检查控制关联"},
      {"from": "TASK-009", "to": "TASK-010", "reason": "验证规则需检查计量关联"},
      {"from": "TASK-004", "to": "TASK-011", "reason": "SHACL约束针对医疗空间"},
      {"from": "TASK-005", "to": "TASK-011", "reason": "SHACL约束针对设备可靠性"},
      {"from": "TASK-007", "to": "TASK-011", "reason": "SHACL约束针对位置规则"},
      {"from": "TASK-010", "to": "TASK-012", "reason": "_index需在所有文件完成后生成"},
      {"from": "TASK-011", "to": "TASK-012", "reason": "_index需在所有文件完成后生成"}
    ]
  },

  "parallel_execution_groups": [
    {
      "group_id": "PG-1",
      "phase": 1,
      "tasks": ["TASK-001"],
      "max_parallelism": 1,
      "description": "基础层 - 必须首先完成"
    },
    {
      "group_id": "PG-2",
      "phase": 2,
      "tasks": ["TASK-002", "TASK-003", "TASK-005"],
      "max_parallelism": 3,
      "description": "领域基础层 - 可并行执行"
    },
    {
      "group_id": "PG-3",
      "phase": 3,
      "tasks": ["TASK-004", "TASK-006"],
      "max_parallelism": 2,
      "description": "领域扩展层 - 可并行执行"
    },
    {
      "group_id": "PG-4",
      "phase": 4,
      "tasks": ["TASK-007", "TASK-008", "TASK-009"],
      "max_parallelism": 3,
      "description": "集成层 - 可并行执行"
    },
    {
      "group_id": "PG-5",
      "phase": 5,
      "tasks": ["TASK-010", "TASK-011"],
      "max_parallelism": 2,
      "description": "规则层 - 可并行执行"
    },
    {
      "group_id": "PG-6",
      "phase": 6,
      "tasks": ["TASK-012"],
      "max_parallelism": 1,
      "description": "索引生成 - 必须最后完成"
    }
  ],

  "critical_path": {
    "description": "关键路径决定整体工期",
    "path": ["TASK-001", "TASK-003", "TASK-004", "TASK-011", "TASK-012"],
    "estimated_duration": "基于关键路径的最短完成时间"
  }
}
```

---

## 📄 7. `_config.json`

**全局配置与元数据**

```json
{
  "project_meta": {
    "name": "CIM_Medical_UDM",
    "full_name": "医疗建筑CIM统一领域模型",
    "version": "0.2.0-Alpha",
    "base_uri": "https://cim.medical/ontology/v3.4#",
    "license": "Proprietary",
    "created": "2025-01-17",
    "authors": ["Gemini-CLI", "Claude-Code"]
  },

  "source_document_registry": {
    "description": "Agent-01~08源文档的物理路径映射",
    "base_path": "/Volumes/M4-SSD/项目 Project/项目 Project/A 工作项目/A 10 研发与产品项目/CIM-PIM-PSM/统一领域模型（CIM）/docs/agents",
    "agents": {
      "Agent-01": {
        "path": "01/",
        "files": ["Agent01_Output.meta", "Agent01_Output.system_catalog", "Agent01_Output.topology_definitions"],
        "format": "YAML"
      },
      "Agent-02": {
        "path": "02/",
        "files": ["Agent02_Output.space_hierarchy_model.yaml", "Agent02_Output.medical_special_spaces.yaml"],
        "format": "YAML"
      },
      "Agent-03": {
        "path": "03/",
        "files": ["Agent03_Output.equipment_classification", "Agent03_Output.node_equipment_mapping"],
        "format": "YAML"
      },
      "Agent-04": {
        "path": "04/",
        "files": ["Agent04_v2.3_FlowModel.ttl", "Agent04_v2.3_Engineering.yaml"],
        "format": "Turtle+YAML"
      },
      "Agent-05": {
        "path": "05/",
        "files": ["Agent05_Output.equipment_location_model", "Agent05_Output.service_space_model"],
        "format": "RDF+JSON"
      },
      "Agent-06": {
        "path": "06/",
        "files": ["Agent06_Output.sensor_models", "Agent06_Output.control_loop_models"],
        "format": "YAML"
      },
      "Agent-07": {
        "path": "07/",
        "files": ["Agent07_Output.metering_hierarchy", "Agent07_Output.allocation_rules"],
        "format": "YAML"
      },
      "Agent-08": {
        "path": "08/",
        "files": ["Agent08_Output.work_order_models", "Agent08_Output.asset_lifecycle_models"],
        "format": "YAML"
      },
      "Agent-09": {
        "path": "09/",
        "files": ["Agent-09 统一领域模型建构指令 v3.4.md"],
        "format": "Markdown"
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
      "cim-loc": "https://cim.medical/ontology/v3.4/location#"
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

  "validation_library": {
    "description": "预定义验证规则库，供Claude Code调用",
    "rules": {
      "VAL-ID-FORMAT": {
        "type": "Regex",
        "expression": "^[A-Z]{3}-[a-f0-9]{8}-\\d{3}$",
        "error_message": "ID格式违规：必须符合PHASE-F规范 (e.g., EQP-a1b2c3d4-001)",
        "source": "Agent-09.PHASE-F"
      },
      "VAL-DATETIME-ISO8601": {
        "type": "Regex",
        "expression": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z$",
        "error_message": "时间戳必须为ISO8601格式"
      },
      "VAL-TEMP-RANGE-OR": {
        "type": "Range",
        "min": 21,
        "max": 25,
        "unit": "°C",
        "error_message": "手术室温度必须在21-25°C范围内",
        "standard": "GB 50333-2013"
      },
      "VAL-HUMIDITY-RANGE-OR": {
        "type": "Range",
        "min": 30,
        "max": 60,
        "unit": "%RH",
        "error_message": "手术室湿度必须在30-60%范围内",
        "standard": "GB 50333-2013"
      },
      "VAL-PRESSURE-MIN-OR": {
        "type": "Min",
        "value": 15,
        "unit": "Pa",
        "error_message": "手术室对走廊压差不小于15Pa",
        "standard": "GB 50333-2013"
      },
      "VAL-ISO-CLASS": {
        "type": "Enum",
        "values": ["ISO-1", "ISO-2", "ISO-3", "ISO-4", "ISO-5", "ISO-6", "ISO-7", "ISO-8", "ISO-9"],
        "error_message": "无效的洁净等级，必须符合ISO 14644-1"
      },
      "VAL-RELIABILITY-LEVEL": {
        "type": "Enum",
        "values": ["LIFE_SAFETY", "PATIENT_SAFETY", "CRITICAL", "IMPORTANT", "SECONDARY"],
        "error_message": "设备可靠性分级必须为5级之一",
        "source": "Agent-03"
      },
      "VAL-NO-CIRCULAR-FLOW": {
        "type": "SPARQL",
        "query": "ASK { ?x cim-flow:feedsTo+ ?x }",
        "expected": false,
        "error_message": "检测到流动网络中的循环依赖"
      },
      "VAL-NODE-HAS-EQUIPMENT": {
        "type": "SPARQL",
        "query": "ASK { ?node a cim-topo:Node . FILTER NOT EXISTS { ?equip cim:mapsToNode ?node } }",
        "expected": false,
        "error_message": "存在未映射到设备的拓扑节点 (Agent-09.CST-EQUIP-001)"
      },
      "VAL-EQUIPMENT-HAS-LOCATION": {
        "type": "SPARQL",
        "query": "ASK { ?equip a cim-equip:Equipment . FILTER NOT EXISTS { ?equip cim:locatedIn ?space } }",
        "expected": false,
        "error_message": "存在未定义位置的设备 (Agent-09.CST-SPACE-001)"
      }
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
      {"id": "GB/T 50378-2019", "name": "绿色建筑运行管理标准"},
      {"id": "GB 50045-95", "name": "高层民用建筑设计防火规范"},
      {"id": "ISO 14644-1", "name": "洁净室及相关受控环境 第1部分：按粒子浓度划分空气洁净度等级"}
    ]
  }
}
```

---

## 📄 8. `_index.ttl` (模板)

```turtle
# ============================================================================
# CIM Medical Building - Master Index Ontology
# Auto-generated entry point for the Unified Domain Model
# ============================================================================

@prefix owl:  <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix cim:  <https://cim.medical/ontology/v3.4#> .

<https://cim.medical/ontology/v3.4>
    a owl:Ontology ;
    rdfs:label "CIM Medical Building Master Index"@en ;
    rdfs:label "医疗建筑CIM主索引"@zh-CN ;
    rdfs:comment "Auto-generated entry point. Imports all CIM ontology modules."@en ;
    owl:versionInfo "0.2.0-Alpha" ;
  
    # Core Module Imports
    owl:imports <https://cim.medical/ontology/v3.4/core/base_entities> ;
    owl:imports <https://cim.medical/ontology/v3.4/core/relationships> ;
    owl:imports <https://cim.medical/ontology/v3.4/core/datatypes> ;
  
    # Topology Module (Agent-01)
    owl:imports <https://cim.medical/ontology/v3.4/topology/node_types> ;
    owl:imports <https://cim.medical/ontology/v3.4/topology/edge_types> ;
    owl:imports <https://cim.medical/ontology/v3.4/topology/system_catalog> ;
  
    # Space Module (Agent-02)
    owl:imports <https://cim.medical/ontology/v3.4/spaces/spatial_hierarchy> ;
    owl:imports <https://cim.medical/ontology/v3.4/spaces/zone_classification> ;
    owl:imports <https://cim.medical/ontology/v3.4/spaces/medical_special_spaces> ;
  
    # Equipment Module (Agent-03)
    owl:imports <https://cim.medical/ontology/v3.4/equipment/equipment_hierarchy> ;
    owl:imports <https://cim.medical/ontology/v3.4/equipment/mechanical> ;
    owl:imports <https://cim.medical/ontology/v3.4/equipment/electrical> ;
    owl:imports <https://cim.medical/ontology/v3.4/equipment/medical_gas> ;
  
    # Flow Module (Agent-04)
    owl:imports <https://cim.medical/ontology/v3.4/flow/flow_layers> ;
    owl:imports <https://cim.medical/ontology/v3.4/flow/flow_sequences> ;
  
    # Coupling Module (Agent-05)
    owl:imports <https://cim.medical/ontology/v3.4/coupling/equipment_location> ;
    owl:imports <https://cim.medical/ontology/v3.4/coupling/service_relations> ;
  
    # Control Module (Agent-06)
    owl:imports <https://cim.medical/ontology/v3.4/control/sensors> ;
    owl:imports <https://cim.medical/ontology/v3.4/control/actuators> ;
    owl:imports <https://cim.medical/ontology/v3.4/control/control_loops> ;
  
    # Metering Module (Agent-07)
    owl:imports <https://cim.medical/ontology/v3.4/metering/metering_hierarchy> ;
    owl:imports <https://cim.medical/ontology/v3.4/metering/energy_media> ;
  
    # Operations Module (Agent-08)
    owl:imports <https://cim.medical/ontology/v3.4/operations/work_orders> ;
    owl:imports <https://cim.medical/ontology/v3.4/operations/maintenance_strategies> ;
    owl:imports <https://cim.medical/ontology/v3.4/operations/asset_lifecycle> ;
  
    # Medical Constraints
    owl:imports <https://cim.medical/ontology/v3.4/medical_constraints/gb50333_cleanroom> ;
  
    # Validation Rules
    owl:imports <https://cim.medical/ontology/v3.4/rules/shacl_constraints> .
```

---

## ✅ 交付物清单总结

| 序号 | 文件名 | 描述 | 状态 |
|------|--------|------|------|
| 1 | `concept_extraction_report.json` | 完整概念提取报告，包含Agent-01~08所有实体、关系、约束及精确来源追踪 | ✅ 完成 |
| 2 | `medical_domain_constraints.json` | 医疗领域约束库，基于GB 50333等国标 | ✅ 完成 |
| 3 | `cim_document_structure.md` | CIM目录结构定义，包含文件-Agent映射 | ✅ 完成 |
| 4 | `ontology_skeleton.ttl` | 本体骨架，基于提取概念的RDF/Turtle定义 | ✅ 完成 |
| 5 | `task_manifest.json` | 完整任务清单，包含依赖关系和验证规则 | ✅ 完成 |
| 6 | `dependency_graph.json` | 任务与概念依赖DAG | ✅ 完成 |
| 7 | `_config.json` | 全局配置与源文档索引 | ✅ 完成 |
| 8 | `_index.ttl` | 本体入口文件模板 | ✅ 完成 |

---

**本体工程索引与协调任务完成。** 

上述所有文档均基于对知识库中 Agent-01~08 实际输出的深度扫描生成，包含精确的来源追踪(`source_trace`)。请将这些文件保存到指定目录，并激活 **Claude Code** 读取 `task_manifest.json` 开始本体填充工作。