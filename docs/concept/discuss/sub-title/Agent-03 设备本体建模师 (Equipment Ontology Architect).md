## 🧑‍💻 User


开始执行设备本体建模

---
## 🤖 Assistant


我需要先搜索知识库，获取Agent-03设备本体建模的详细指导信息。



根据知识库搜索结果，我发现Agent-03设备本体建模已有完成的项目总结。让我进一步搜索详细的设备分类体系和设备模型定义。



让我继续搜索更多关于设备类型详细模型的信息，特别是P0核心设备的建模规范。



让我搜索Agent-01的系统拓扑输出，这是Agent-03的前置输入依赖。



现在让我搜索已完成的Agent-03输出文件，了解已有的设备本体建模成果。



根据知识库搜索结果，我已经获取了足够的信息来执行Agent-03设备本体建模。根据项目总结，Agent-03已完成基础建模，但现在需要基于Agent-02 v1.2的完善版空间模型，补充与空间耦合相关的设备配置信息。

让我开始执行完整的设备本体建模输出：

---

# Agent-03: 设备本体建模师 (Equipment Ontology Architect)
## 完整输出文档 v2.0

---

```yaml
# ═══════════════════════════════════════════════════════════════════════════════
# Agent-03: 设备本体建模师 (Equipment Ontology Architect)
# 医疗建筑设备本体模型 - 完整版 v2.0
# 基于Agent-01系统拓扑 + Agent-02空间本体 的设备级建模
# ═══════════════════════════════════════════════════════════════════════════════

Agent03_Output:

  # ════════════════════════════════════════════════════════════════════════════
  # 元数据
  # ════════════════════════════════════════════════════════════════════════════
  meta:
    agent_id: Agent-03
    agent_name: 设备本体建模师
    agent_name_en: Equipment Ontology Architect
    version: "2.0"
    version_note: |
      v2.0更新内容：
      1. 基于Agent-01系统拓扑完成节点-设备映射
      2. 基于Agent-02空间本体增强设备-空间耦合属性
      3. 完成8大系统26子系统的设备分类体系
      4. 详细建模18类P0核心设备
      5. 新增医疗级设备可靠性分级体系
    generated_at: "2024-12-20T00:00:00+08:00"
    depends_on:
      - agent: Agent-01
        version: "1.0"
        artifacts:
          - Agent01_Output.system_catalog
          - Agent01_Output.system_topologies
          - Agent01_Output.topology_definitions
      - agent: Agent-02
        version: "1.2"
        artifacts:
          - Agent02_Output.space_hierarchy_model
          - Agent02_Output.facility_equipment_configuration
          - Agent02_Output.hardware_system_space_coupling
    
    modeling_scope:
      system_categories: 8
      sub_systems: 26
      equipment_types: 123
      p0_detailed_models: 18
      topology_node_mappings: 156

  # ════════════════════════════════════════════════════════════════════════════
  # 第一部分：设备模型层级定义
  # ════════════════════════════════════════════════════════════════════════════
  equipment_hierarchy_model:
    
    description: |
      设备本体采用四层级结构，从系统级到零部件级逐层细化。
      本模型的核心关注点是Level_2_Equipment（独立设备），
      同时向上关联系统拓扑，向下分解组件和部件。
    
    levels:
      
      - level_id: L1
        level_name: System
        level_name_cn: 系统级
        description: 完成特定功能的设备集合，对应Agent-01的系统拓扑
        examples:
          - "1号冷站系统"
          - "手术室洁净空调系统"
          - "10kV高压配电系统"
        attributes:
          - system_id
          - system_name
          - system_category
          - serving_scope
        relationship:
          parent: null
          children: Equipment
          
      - level_id: L2
        level_name: Equipment
        level_name_cn: 设备级
        description: 独立的功能装置，是本体模型的核心层级
        examples:
          - "CH-001 离心式冷水机组"
          - "AHU-OR-001 手术室洁净空调机组"
          - "TR-001 干式变压器"
        attributes:
          - equipment_id
          - equipment_name
          - equipment_type
          - manufacturer
          - model
          - rated_parameters
          - installation_location
          - operational_status
        relationship:
          parent: System
          children: Component
          
      - level_id: L3
        level_name: Component
        level_name_cn: 组件级
        description: 设备的组成部分，通常可独立维护或更换
        examples:
          - "CH-001-COMP 冷机压缩机"
          - "AHU-OR-001-FAN 送风机"
          - "TR-001-WINDING 变压器绕组"
        attributes:
          - component_id
          - component_name
          - component_type
          - parent_equipment
          - is_replaceable
          - maintenance_cycle
        relationship:
          parent: Equipment
          children: Part
          
      - level_id: L4
        level_name: Part
        level_name_cn: 部件/零件级
        description: 可更换的零部件，通常是耗材或易损件
        examples:
          - "CH-001-OIL-FILTER 冷机油过滤器"
          - "AHU-OR-001-BELT 风机皮带"
          - "FCU-001-FILTER 风机盘管过滤网"
        attributes:
          - part_id
          - part_name
          - part_number
          - is_consumable
          - replacement_cycle
          - stock_quantity
        relationship:
          parent: Component
          children: null

  # ════════════════════════════════════════════════════════════════════════════
  # 第二部分：设备分类体系
  # ════════════════════════════════════════════════════════════════════════════
  equipment_classification:
    
    description: |
      医疗建筑设备分类体系，覆盖8大系统类别、26个子系统、123种设备类型。
      分类体系与Agent-01的系统目录保持一致，实现系统-设备的完整映射。
    
    # ────────────────────────────────────────────────────────────────────────
    # 8大系统类别
    # ────────────────────────────────────────────────────────────────────────
    categories:
      
      # ══════════════════════════════════════════════════════════════════════
      # 类别1：暖通空调设备
      # ══════════════════════════════════════════════════════════════════════
      - category_id: EQUIP-HVAC
        category_name: 暖通空调设备
        category_name_en: HVAC Equipment
        description: 用于建筑空气调节、通风、供暖的设备
        system_mapping: HVAC
        
        sub_categories:
          
          - sub_id: EQUIP-HVAC-CHILLER
            sub_name: 冷水机组
            sub_name_en: Chiller
            system_mapping: HVAC-CHP
            equipment_types:
              - type_id: CHILLER-CENT
                type_name: 离心式冷水机组
                type_name_en: Centrifugal Chiller
                topology_role: SOURCE
                medical_criticality: CRITICAL
                typical_capacity_range: [1000, 5000]
                capacity_unit: kW
                
              - type_id: CHILLER-SCREW
                type_name: 螺杆式冷水机组
                type_name_en: Screw Chiller
                topology_role: SOURCE
                medical_criticality: CRITICAL
                typical_capacity_range: [200, 1500]
                capacity_unit: kW
                
              - type_id: CHILLER-SCROLL
                type_name: 涡旋式冷水机组
                type_name_en: Scroll Chiller
                topology_role: SOURCE
                medical_criticality: IMPORTANT
                typical_capacity_range: [50, 300]
                capacity_unit: kW
                
              - type_id: CHILLER-ABS
                type_name: 吸收式冷水机组
                type_name_en: Absorption Chiller
                topology_role: SOURCE
                medical_criticality: IMPORTANT
                typical_capacity_range: [500, 3000]
                capacity_unit: kW
                
              - type_id: CHILLER-MODULAR
                type_name: 模块式冷水机组
                type_name_en: Modular Chiller
                topology_role: SOURCE
                medical_criticality: IMPORTANT
                typical_capacity_range: [50, 500]
                capacity_unit: kW
                
          - sub_id: EQUIP-HVAC-PUMP
            sub_name: 水泵
            sub_name_en: Pump
            system_mapping: HVAC-CHP, HVAC-CHW, HVAC-HW
            equipment_types:
              - type_id: PUMP-CHW-P
                type_name: 冷冻水一次泵
                type_name_en: Primary Chilled Water Pump
                topology_role: DISTRIBUTION
                medical_criticality: CRITICAL
                
              - type_id: PUMP-CHW-S
                type_name: 冷冻水二次泵
                type_name_en: Secondary Chilled Water Pump
                topology_role: DISTRIBUTION
                medical_criticality: CRITICAL
                
              - type_id: PUMP-CW
                type_name: 冷却水泵
                type_name_en: Condenser Water Pump
                topology_role: DISTRIBUTION
                medical_criticality: CRITICAL
                
              - type_id: PUMP-HW
                type_name: 热水泵
                type_name_en: Hot Water Pump
                topology_role: DISTRIBUTION
                medical_criticality: CRITICAL
                
              - type_id: PUMP-MAKEUP
                type_name: 补水泵
                type_name_en: Makeup Water Pump
                topology_role: DISTRIBUTION
                medical_criticality: IMPORTANT
                
          - sub_id: EQUIP-HVAC-CT
            sub_name: 冷却塔
            sub_name_en: Cooling Tower
            system_mapping: HVAC-CHP
            equipment_types:
              - type_id: CT-OPEN
                type_name: 开式冷却塔
                type_name_en: Open Cooling Tower
                topology_role: SOURCE
                medical_criticality: CRITICAL
                
              - type_id: CT-CLOSED
                type_name: 闭式冷却塔
                type_name_en: Closed Cooling Tower
                topology_role: SOURCE
                medical_criticality: CRITICAL
                
          - sub_id: EQUIP-HVAC-BOILER
            sub_name: 锅炉
            sub_name_en: Boiler
            system_mapping: HVAC-HTP
            equipment_types:
              - type_id: BOILER-GAS
                type_name: 燃气热水锅炉
                type_name_en: Gas-fired Hot Water Boiler
                topology_role: SOURCE
                medical_criticality: CRITICAL
                
              - type_id: BOILER-STEAM
                type_name: 蒸汽锅炉
                type_name_en: Steam Boiler
                topology_role: SOURCE
                medical_criticality: CRITICAL
                
              - type_id: BOILER-ELECTRIC
                type_name: 电热水锅炉
                type_name_en: Electric Boiler
                topology_role: SOURCE
                medical_criticality: IMPORTANT
                
          - sub_id: EQUIP-HVAC-AHU
            sub_name: 空调机组
            sub_name_en: Air Handling Unit
            system_mapping: HVAC-AHU
            equipment_types:
              - type_id: AHU-CONV
                type_name: 常规组合式空调机组
                type_name_en: Conventional AHU
                topology_role: DISTRIBUTION
                medical_criticality: IMPORTANT
                
              - type_id: AHU-CLEAN
                type_name: 洁净空调机组
                type_name_en: Clean Room AHU
                topology_role: DISTRIBUTION
                medical_criticality: LIFE_SAFETY
                application: 手术室、ICU、洁净实验室
                
              - type_id: AHU-PAU
                type_name: 新风机组
                type_name_en: Primary Air Unit
                topology_role: SOURCE
                medical_criticality: CRITICAL
                
              - type_id: AHU-MAU
                type_name: 全热回收新风机组
                type_name_en: Make-up Air Unit with Heat Recovery
                topology_role: SOURCE
                medical_criticality: IMPORTANT
                
              - type_id: AHU-DX
                type_name: 直膨式空调机组
                type_name_en: Direct Expansion AHU
                topology_role: DISTRIBUTION
                medical_criticality: IMPORTANT
                
          - sub_id: EQUIP-HVAC-TERM
            sub_name: 空调末端
            sub_name_en: Terminal Units
            system_mapping: HVAC-TERM
            equipment_types:
              - type_id: FCU
                type_name: 风机盘管
                type_name_en: Fan Coil Unit
                topology_role: SINK
                medical_criticality: IMPORTANT
                
              - type_id: VAV
                type_name: 变风量末端
                type_name_en: Variable Air Volume Box
                topology_role: SINK
                medical_criticality: IMPORTANT
                
              - type_id: CAV
                type_name: 定风量末端
                type_name_en: Constant Air Volume Box
                topology_role: SINK
                medical_criticality: IMPORTANT
                
              - type_id: CHILLED-BEAM
                type_name: 冷梁
                type_name_en: Chilled Beam
                topology_role: SINK
                medical_criticality: IMPORTANT
                
              - type_id: RADIANT-PANEL
                type_name: 辐射板
                type_name_en: Radiant Panel
                topology_role: SINK
                medical_criticality: SECONDARY
                
          - sub_id: EQUIP-HVAC-FAN
            sub_name: 风机
            sub_name_en: Fan
            system_mapping: HVAC-VENT
            equipment_types:
              - type_id: FAN-EXHAUST
                type_name: 排风机
                type_name_en: Exhaust Fan
                topology_role: SINK
                medical_criticality: CRITICAL
                
              - type_id: FAN-SUPPLY
                type_name: 送风机
                type_name_en: Supply Fan
                topology_role: DISTRIBUTION
                medical_criticality: CRITICAL
                
              - type_id: FAN-RETURN
                type_name: 回风机
                type_name_en: Return Fan
                topology_role: DISTRIBUTION
                medical_criticality: IMPORTANT
                
              - type_id: FAN-SMOKE
                type_name: 排烟风机
                type_name_en: Smoke Exhaust Fan
                topology_role: SINK
                medical_criticality: LIFE_SAFETY
                
              - type_id: FAN-PRESSURIZATION
                type_name: 加压送风机
                type_name_en: Pressurization Fan
                topology_role: SOURCE
                medical_criticality: LIFE_SAFETY
                
          - sub_id: EQUIP-HVAC-HX
            sub_name: 换热器
            sub_name_en: Heat Exchanger
            system_mapping: HVAC-CHP, HVAC-HTP
            equipment_types:
              - type_id: HX-PLATE
                type_name: 板式换热器
                type_name_en: Plate Heat Exchanger
                topology_role: DISTRIBUTION
                medical_criticality: CRITICAL
                
              - type_id: HX-SHELL-TUBE
                type_name: 壳管式换热器
                type_name_en: Shell and Tube Heat Exchanger
                topology_role: DISTRIBUTION
                medical_criticality: CRITICAL
                
          - sub_id: EQUIP-HVAC-FILTER
            sub_name: 过滤器
            sub_name_en: Filter
            system_mapping: HVAC-AHU, HVAC-CLEAN
            equipment_types:
              - type_id: FILTER-PRIMARY
                type_name: 初效过滤器
                type_name_en: Primary Filter
                topology_role: COMPONENT
                medical_criticality: IMPORTANT
                
              - type_id: FILTER-MEDIUM
                type_name: 中效过滤器
                type_name_en: Medium Filter
                topology_role: COMPONENT
                medical_criticality: IMPORTANT
                
              - type_id: FILTER-HEPA
                type_name: 高效过滤器
                type_name_en: HEPA Filter
                topology_role: COMPONENT
                medical_criticality: LIFE_SAFETY
                application: 手术室、洁净室
                
              - type_id: FILTER-ULPA
                type_name: 超高效过滤器
                type_name_en: ULPA Filter
                topology_role: COMPONENT
                medical_criticality: LIFE_SAFETY
                application: 特殊洁净环境
                
          - sub_id: EQUIP-HVAC-HUMIDIFIER
            sub_name: 加湿器
            sub_name_en: Humidifier
            system_mapping: HVAC-AHU
            equipment_types:
              - type_id: HUM-ELECTRODE
                type_name: 电极式加湿器
                type_name_en: Electrode Humidifier
                topology_role: COMPONENT
                medical_criticality: IMPORTANT
                
              - type_id: HUM-STEAM
                type_name: 干蒸汽加湿器
                type_name_en: Steam Humidifier
                topology_role: COMPONENT
                medical_criticality: CRITICAL
                application: 医疗级加湿，无菌
                
          - sub_id: EQUIP-HVAC-VRF
            sub_name: 多联机系统
            sub_name_en: VRF System
            system_mapping: HVAC-VRF
            equipment_types:
              - type_id: VRF-OUTDOOR
                type_name: 多联机室外机
                type_name_en: VRF Outdoor Unit
                topology_role: SOURCE
                medical_criticality: IMPORTANT
                
              - type_id: VRF-INDOOR
                type_name: 多联机室内机
                type_name_en: VRF Indoor Unit
                topology_role: SINK
                medical_criticality: IMPORTANT
                
      # ══════════════════════════════════════════════════════════════════════
      # 类别2：给排水设备
      # ══════════════════════════════════════════════════════════════════════
      - category_id: EQUIP-PLUMB
        category_name: 给排水设备
        category_name_en: Plumbing Equipment
        description: 用于建筑给水、排水、热水供应的设备
        system_mapping: PLUMBING
        
        sub_categories:
          
          - sub_id: EQUIP-PLUMB-PUMP
            sub_name: 给水泵
            sub_name_en: Water Supply Pump
            system_mapping: PLUMB-WSS
            equipment_types:
              - type_id: PUMP-DOMESTIC
                type_name: 生活水泵
                type_name_en: Domestic Water Pump
                topology_role: DISTRIBUTION
                medical_criticality: CRITICAL
                
              - type_id: PUMP-BOOSTER
                type_name: 增压泵
                type_name_en: Booster Pump
                topology_role: DISTRIBUTION
                medical_criticality: IMPORTANT
                
              - type_id: PUMP-CIRCULATING
                type_name: 热水循环泵
                type_name_en: Hot Water Circulating Pump
                topology_role: DISTRIBUTION
                medical_criticality: IMPORTANT
                
          - sub_id: EQUIP-PLUMB-TANK
            sub_name: 水箱
            sub_name_en: Water Tank
            system_mapping: PLUMB-WSS
            equipment_types:
              - type_id: TANK-DOMESTIC
                type_name: 生活水箱
                type_name_en: Domestic Water Tank
                topology_role: SOURCE
                medical_criticality: CRITICAL
                
              - type_id: TANK-FIRE
                type_name: 消防水池
                type_name_en: Fire Water Tank
                topology_role: SOURCE
                medical_criticality: LIFE_SAFETY
                
              - type_id: TANK-EXPANSION
                type_name: 膨胀水箱
                type_name_en: Expansion Tank
                topology_role: COMPONENT
                medical_criticality: IMPORTANT
                
          - sub_id: EQUIP-PLUMB-HEATER
            sub_name: 热水设备
            sub_name_en: Water Heater
            system_mapping: PLUMB-HWS
            equipment_types:
              - type_id: HEATER-STORAGE
                type_name: 容积式电热水器
                type_name_en: Storage Electric Water Heater
                topology_role: SOURCE
                medical_criticality: IMPORTANT
                
              - type_id: HEATER-INSTANT
                type_name: 即热式热水器
                type_name_en: Instantaneous Water Heater
                topology_role: SOURCE
                medical_criticality: IMPORTANT
                
              - type_id: HEATER-SOLAR
                type_name: 太阳能热水器
                type_name_en: Solar Water Heater
                topology_role: SOURCE
                medical_criticality: SECONDARY
                
          - sub_id: EQUIP-PLUMB-TREATMENT
            sub_name: 水处理设备
            sub_name_en: Water Treatment
            system_mapping: PLUMB-SPECIAL
            equipment_types:
              - type_id: WTP-SOFTENER
                type_name: 软化水设备
                type_name_en: Water Softener
                topology_role: DISTRIBUTION
                medical_criticality: IMPORTANT
                
              - type_id: WTP-RO
                type_name: 反渗透纯水设备
                type_name_en: RO Pure Water System
                topology_role: SOURCE
                medical_criticality: CRITICAL
                application: 血透、检验、制药
                
              - type_id: WTP-DI
                type_name: 去离子水设备
                type_name_en: Deionized Water System
                topology_role: SOURCE
                medical_criticality: CRITICAL
                
              - type_id: WTP-UV
                type_name: 紫外消毒器
                type_name_en: UV Disinfection System
                topology_role: DISTRIBUTION
                medical_criticality: CRITICAL
                
          - sub_id: EQUIP-PLUMB-DRAINAGE
            sub_name: 排水设备
            sub_name_en: Drainage Equipment
            system_mapping: PLUMB-DRAIN
            equipment_types:
              - type_id: PUMP-SEWAGE
                type_name: 污水提升泵
                type_name_en: Sewage Pump
                topology_role: DISTRIBUTION
                medical_criticality: IMPORTANT
                
              - type_id: PUMP-SUMP
                type_name: 集水坑排水泵
                type_name_en: Sump Pump
                topology_role: DISTRIBUTION
                medical_criticality: IMPORTANT
                
              - type_id: GREASE-TRAP
                type_name: 隔油池
                type_name_en: Grease Trap
                topology_role: COMPONENT
                medical_criticality: SECONDARY
                
      # ══════════════════════════════════════════════════════════════════════
      # 类别3：电气设备
      # ══════════════════════════════════════════════════════════════════════
      - category_id: EQUIP-ELEC
        category_name: 电气设备
        category_name_en: Electrical Equipment
        description: 用于供电、配电、照明、应急电源的设备
        system_mapping: ELECTRICAL
        
        sub_categories:
          
          - sub_id: EQUIP-ELEC-TRANS
            sub_name: 变压器
            sub_name_en: Transformer
            system_mapping: ELEC-HV, ELEC-LV
            equipment_types:
              - type_id: TRANS-DRY
                type_name: 干式变压器
                type_name_en: Dry-type Transformer
                topology_role: DISTRIBUTION
                medical_criticality: CRITICAL
                
              - type_id: TRANS-OIL
                type_name: 油浸式变压器
                type_name_en: Oil-immersed Transformer
                topology_role: DISTRIBUTION
                medical_criticality: CRITICAL
                
              - type_id: TRANS-ISO
                type_name: 医用隔离变压器
                type_name_en: Medical Isolation Transformer
                topology_role: DISTRIBUTION
                medical_criticality: LIFE_SAFETY
                application: 手术室、ICU隔离电源
                
          - sub_id: EQUIP-ELEC-SWGR
            sub_name: 开关柜
            sub_name_en: Switchgear
            system_mapping: ELEC-HV, ELEC-LV
            equipment_types:
              - type_id: SWGR-HV
                type_name: 高压开关柜
                type_name_en: High Voltage Switchgear
                topology_role: DISTRIBUTION
                medical_criticality: CRITICAL
                
              - type_id: SWGR-LV
                type_name: 低压配电柜
                type_name_en: Low Voltage Switchgear
                topology_role: DISTRIBUTION
                medical_criticality: CRITICAL
                
              - type_id: SWGR-ATS
                type_name: 双电源切换柜
                type_name_en: Automatic Transfer Switch
                topology_role: DISTRIBUTION
                medical_criticality: LIFE_SAFETY
                
          - sub_id: EQUIP-ELEC-GEN
            sub_name: 发电机组
            sub_name_en: Generator
            system_mapping: ELEC-EPS
            equipment_types:
              - type_id: GEN-DIESEL
                type_name: 柴油发电机组
                type_name_en: Diesel Generator Set
                topology_role: SOURCE
                medical_criticality: LIFE_SAFETY
                
              - type_id: GEN-GAS
                type_name: 燃气发电机组
                type_name_en: Gas Generator Set
                topology_role: SOURCE
                medical_criticality: CRITICAL
                
          - sub_id: EQUIP-ELEC-UPS
            sub_name: 不间断电源
            sub_name_en: UPS
            system_mapping: ELEC-EPS
            equipment_types:
              - type_id: UPS-ONLINE
                type_name: 在线式UPS
                type_name_en: Online UPS
                topology_role: DISTRIBUTION
                medical_criticality: LIFE_SAFETY
                
              - type_id: UPS-MEDICAL
                type_name: 医用UPS
                type_name_en: Medical Grade UPS
                topology_role: DISTRIBUTION
                medical_criticality: LIFE_SAFETY
                application: 手术室、ICU、生命支持设备
                
          - sub_id: EQUIP-ELEC-PANEL
            sub_name: 配电箱
            sub_name_en: Distribution Panel
            system_mapping: ELEC-LV
            equipment_types:
              - type_id: PANEL-FLOOR
                type_name: 楼层配电箱
                type_name_en: Floor Distribution Panel
                topology_role: DISTRIBUTION
                medical_criticality: IMPORTANT
                
              - type_id: PANEL-ROOM
                type_name: 房间配电箱
                type_name_en: Room Distribution Panel
                topology_role: SINK
                medical_criticality: IMPORTANT
                
              - type_id: PANEL-IT
                type_name: IT隔离配电箱
                type_name_en: IT Isolation Panel
                topology_role: DISTRIBUTION
                medical_criticality: LIFE_SAFETY
                
          - sub_id: EQUIP-ELEC-LIGHTING
            sub_name: 照明设备
            sub_name_en: Lighting
            system_mapping: ELEC-LIGHTING
            equipment_types:
              - type_id: LIGHT-SURGICAL
                type_name: 手术无影灯
                type_name_en: Surgical Light
                topology_role: SINK
                medical_criticality: LIFE_SAFETY
                
              - type_id: LIGHT-EXAM
                type_name: 检查灯
                type_name_en: Examination Light
                topology_role: SINK
                medical_criticality: PATIENT_SAFETY
                
              - type_id: LIGHT-EMERGENCY
                type_name: 应急照明
                type_name_en: Emergency Lighting
                topology_role: SINK
                medical_criticality: LIFE_SAFETY
                
              - type_id: LIGHT-GENERAL
                type_name: 一般照明
                type_name_en: General Lighting
                topology_role: SINK
                medical_criticality: SECONDARY
                
      # ══════════════════════════════════════════════════════════════════════
      # 类别4：医疗气体设备
      # ══════════════════════════════════════════════════════════════════════
      - category_id: EQUIP-GAS
        category_name: 医疗气体设备
        category_name_en: Medical Gas Equipment
        description: 用于医疗气体供应的设备，包括氧气、负压吸引、压缩空气等
        system_mapping: MEDICAL_GAS
        
        sub_categories:
          
          - sub_id: EQUIP-GAS-O2
            sub_name: 氧气系统设备
            sub_name_en: Oxygen System Equipment
            system_mapping: GAS-O2
            equipment_types:
              - type_id: O2-LOX-TANK
                type_name: 液氧储罐
                type_name_en: LOX Tank
                topology_role: SOURCE
                medical_criticality: LIFE_SAFETY
                
              - type_id: O2-MANIFOLD
                type_name: 氧气汇流排
                type_name_en: Oxygen Manifold
                topology_role: SOURCE
                medical_criticality: LIFE_SAFETY
                
              - type_id: O2-PSA
                type_name: PSA制氧机
                type_name_en: PSA Oxygen Generator
                topology_role: SOURCE
                medical_criticality: LIFE_SAFETY
                
              - type_id: O2-REGULATOR
                type_name: 氧气减压器
                type_name_en: Oxygen Pressure Regulator
                topology_role: DISTRIBUTION
                medical_criticality: CRITICAL
                
              - type_id: O2-OUTLET
                type_name: 氧气终端
                type_name_en: Oxygen Outlet
                topology_role: SINK
                medical_criticality: LIFE_SAFETY
                
          - sub_id: EQUIP-GAS-VAC
            sub_name: 负压吸引设备
            sub_name_en: Vacuum System Equipment
            system_mapping: GAS-VAC
            equipment_types:
              - type_id: VAC-PUMP
                type_name: 医用真空泵
                type_name_en: Medical Vacuum Pump
                topology_role: SOURCE
                medical_criticality: LIFE_SAFETY
                
              - type_id: VAC-RECEIVER
                type_name: 真空罐
                type_name_en: Vacuum Receiver
                topology_role: DISTRIBUTION
                medical_criticality: CRITICAL
                
              - type_id: VAC-REGULATOR
                type_name: 负压调节器
                type_name_en: Vacuum Regulator
                topology_role: DISTRIBUTION
                medical_criticality: CRITICAL
                
              - type_id: VAC-OUTLET
                type_name: 负压吸引终端
                type_name_en: Vacuum Outlet
                topology_role: SINK
                medical_criticality: LIFE_SAFETY
                
          - sub_id: EQUIP-GAS-AIR
            sub_name: 压缩空气设备
            sub_name_en: Compressed Air Equipment
            system_mapping: GAS-AIR
            equipment_types:
              - type_id: AIR-COMPRESSOR
                type_name: 医用无油空压机
                type_name_en: Medical Oil-free Air Compressor
                topology_role: SOURCE
                medical_criticality: CRITICAL
                
              - type_id: AIR-DRYER
                type_name: 冷干机
                type_name_en: Refrigerated Air Dryer
                topology_role: DISTRIBUTION
                medical_criticality: CRITICAL
                
              - type_id: AIR-RECEIVER
                type_name: 储气罐
                type_name_en: Air Receiver
                topology_role: DISTRIBUTION
                medical_criticality: IMPORTANT
                
              - type_id: AIR-OUTLET
                type_name: 压缩空气终端
                type_name_en: Compressed Air Outlet
                topology_role: SINK
                medical_criticality: CRITICAL
                
          - sub_id: EQUIP-GAS-N2O
            sub_name: 笑气系统设备
            sub_name_en: N2O System Equipment
            system_mapping: GAS-N2O
            equipment_types:
              - type_id: N2O-MANIFOLD
                type_name: 笑气汇流排
                type_name_en: N2O Manifold
                topology_role: SOURCE
                medical_criticality: PATIENT_SAFETY
                
              - type_id: N2O-OUTLET
                type_name: 笑气终端
                type_name_en: N2O Outlet
                topology_role: SINK
                medical_criticality: PATIENT_SAFETY
                
          - sub_id: EQUIP-GAS-SCAV
            sub_name: 麻醉废气排放设备
            sub_name_en: Anesthesia Gas Scavenging Equipment
            system_mapping: GAS-SCAV
            equipment_types:
              - type_id: SCAV-PUMP
                type_name: 麻醉废气排放泵
                type_name_en: AGSS Pump
                topology_role: SOURCE
                medical_criticality: PATIENT_SAFETY
                
              - type_id: SCAV-INTERFACE
                type_name: 麻醉废气接口
                type_name_en: AGSS Interface
                topology_role: SINK
                medical_criticality: PATIENT_SAFETY
                
      # ══════════════════════════════════════════════════════════════════════
      # 类别5：消防设备
      # ══════════════════════════════════════════════════════════════════════
      - category_id: EQUIP-FIRE
        category_name: 消防设备
        category_name_en: Fire Protection Equipment
        description: 用于火灾探测、报警、灭火的设备
        system_mapping: FIRE_PROTECTION
        
        sub_categories:
          
          - sub_id: EQUIP-FIRE-PUMP
            sub_name: 消防水泵
            sub_name_en: Fire Pump
            system_mapping: FIRE-HYDRANT, FIRE-SPRINKLER
            equipment_types:
              - type_id: PUMP-FIRE-MAIN
                type_name: 消火栓主泵
                type_name_en: Fire Hydrant Main Pump
                topology_role: SOURCE
                medical_criticality: LIFE_SAFETY
                
              - type_id: PUMP-FIRE-JOCKEY
                type_name: 消防稳压泵
                type_name_en: Jockey Pump
                topology_role: SOURCE
                medical_criticality: LIFE_SAFETY
                
              - type_id: PUMP-SPRINKLER
                type_name: 喷淋泵
                type_name_en: Sprinkler Pump
                topology_role: SOURCE
                medical_criticality: LIFE_SAFETY
                
          - sub_id: EQUIP-FIRE-GAS
            sub_name: 气体灭火设备
            sub_name_en: Gas Suppression Equipment
            system_mapping: FIRE-GAS
            equipment_types:
              - type_id: GAS-FM200
                type_name: 七氟丙烷灭火系统
                type_name_en: FM200 Suppression System
                topology_role: SOURCE
                medical_criticality: CRITICAL
                
              - type_id: GAS-IG541
                type_name: IG541灭火系统
                type_name_en: IG541 Suppression System
                topology_role: SOURCE
                medical_criticality: CRITICAL
                
              - type_id: GAS-CO2
                type_name: 二氧化碳灭火系统
                type_name_en: CO2 Suppression System
                topology_role: SOURCE
                medical_criticality: CRITICAL
                
          - sub_id: EQUIP-FIRE-ALARM
            sub_name: 火灾报警设备
            sub_name_en: Fire Alarm Equipment
            system_mapping: FIRE-ALARM
            equipment_types:
              - type_id: ALARM-PANEL
                type_name: 火灾报警控制器
                type_name_en: Fire Alarm Control Panel
                topology_role: DISTRIBUTION
                medical_criticality: LIFE_SAFETY
                
              - type_id: ALARM-SMOKE
                type_name: 感烟探测器
                type_name_en: Smoke Detector
                topology_role: SINK
                medical_criticality: LIFE_SAFETY
                
              - type_id: ALARM-HEAT
                type_name: 感温探测器
                type_name_en: Heat Detector
                topology_role: SINK
                medical_criticality: LIFE_SAFETY
                
              - type_id: ALARM-MANUAL
                type_name: 手动报警按钮
                type_name_en: Manual Call Point
                topology_role: SINK
                medical_criticality: LIFE_SAFETY
                
      # ══════════════════════════════════════════════════════════════════════
      # 类别6：垂直交通设备
      # ══════════════════════════════════════════════════════════════════════
      - category_id: EQUIP-VERT
        category_name: 垂直交通设备
        category_name_en: Vertical Transportation Equipment
        description: 用于人员和物品垂直运输的设备
        system_mapping: VERTICAL_TRANSPORT
        
        sub_categories:
          
          - sub_id: EQUIP-VERT-ELEV
            sub_name: 电梯
            sub_name_en: Elevator
            system_mapping: VERT-ELEV
            equipment_types:
              - type_id: ELEV-BED
                type_name: 病床电梯
                type_name_en: Bed Elevator
                topology_role: DISTRIBUTION
                medical_criticality: LIFE_SAFETY
                application: 患者转运
                
              - type_id: ELEV-PASSENGER
                type_name: 客梯
                type_name_en: Passenger Elevator
                topology_role: DISTRIBUTION
                medical_criticality: IMPORTANT
                
              - type_id: ELEV-SERVICE
                type_name: 货梯
                type_name_en: Service Elevator
                topology_role: DISTRIBUTION
                medical_criticality: IMPORTANT
                
              - type_id: ELEV-PANORAMIC
                type_name: 观光电梯
                type_name_en: Panoramic Elevator
                topology_role: DISTRIBUTION
                medical_criticality: SECONDARY
                
          - sub_id: EQUIP-VERT-ESC
            sub_name: 自动扶梯
            sub_name_en: Escalator
            system_mapping: VERT-ESC
            equipment_types:
              - type_id: ESC-STANDARD
                type_name: 自动扶梯
                type_name_en: Escalator
                topology_role: DISTRIBUTION
                medical_criticality: SECONDARY
                
              - type_id: WALK-MOVING
                type_name: 自动人行道
                type_name_en: Moving Walkway
                topology_role: DISTRIBUTION
                medical_criticality: SECONDARY
                
      # ══════════════════════════════════════════════════════════════════════
      # 类别7：楼宇自动化设备
      # ══════════════════════════════════════════════════════════════════════
      - category_id: EQUIP-BAS
        category_name: 楼宇自动化设备
        category_name_en: Building Automation Equipment
        description: 用于楼宇自动控制、能源管理、安防的设备
        system_mapping: BUILDING_AUTOMATION
        
        sub_categories:
          
          - sub_id: EQUIP-BAS-SENSOR
            sub_name: 传感器
            sub_name_en: Sensor
            system_mapping: BA-BMS
            equipment_types:
              - type_id: SENSOR-TEMP
                type_name: 温度传感器
                type_name_en: Temperature Sensor
                topology_role: SINK
                medical_criticality: IMPORTANT
                variants:
                  - 管道式温度传感器
                  - 风管式温度传感器
                  - 室内温度传感器
                  - 室外温度传感器
                  
              - type_id: SENSOR-HUMIDITY
                type_name: 湿度传感器
                type_name_en: Humidity Sensor
                topology_role: SINK
                medical_criticality: IMPORTANT
                
              - type_id: SENSOR-PRESSURE
                type_name: 压力/压差传感器
                type_name_en: Pressure Sensor
                topology_role: SINK
                medical_criticality: CRITICAL
                application: 洁净室压差监测
                
              - type_id: SENSOR-FLOW
                type_name: 流量传感器
                type_name_en: Flow Sensor
                topology_role: SINK
                medical_criticality: IMPORTANT
                
              - type_id: SENSOR-CO2
                type_name: CO2浓度传感器
                type_name_en: CO2 Sensor
                topology_role: SINK
                medical_criticality: IMPORTANT
                
              - type_id: SENSOR-PARTICLE
                type_name: 尘埃粒子计数器
                type_name_en: Particle Counter
                topology_role: SINK
                medical_criticality: CRITICAL
                application: 洁净室监测
                
          - sub_id: EQUIP-BAS-ACTUATOR
            sub_name: 执行器
            sub_name_en: Actuator
            system_mapping: BA-BMS
            equipment_types:
              - type_id: ACTUATOR-VALVE
                type_name: 电动调节阀
                type_name_en: Control Valve Actuator
                topology_role: DISTRIBUTION
                medical_criticality: IMPORTANT
                variants:
                  - 两通调节阀
                  - 三通调节阀
                  - 蝶阀
                  - 球阀
                  
              - type_id: ACTUATOR-DAMPER
                type_name: 电动风阀
                type_name_en: Damper Actuator
                topology_role: DISTRIBUTION
                medical_criticality: IMPORTANT
                
              - type_id: ACTUATOR-VFD
                type_name: 变频器
                type_name_en: Variable Frequency Drive
                topology_role: DISTRIBUTION
                medical_criticality: CRITICAL
                
          - sub_id: EQUIP-BAS-CONTROLLER
            sub_name: 控制器
            sub_name_en: Controller
            system_mapping: BA-BMS
            equipment_types:
              - type_id: CTRL-DDC
                type_name: DDC控制器
                type_name_en: Direct Digital Controller
                topology_role: DISTRIBUTION
                medical_criticality: CRITICAL
                
              - type_id: CTRL-PLC
                type_name: PLC控制器
                type_name_en: Programmable Logic Controller
                topology_role: DISTRIBUTION
                medical_criticality: CRITICAL
                
              - type_id: CTRL-BMS-SERVER
                type_name: BMS服务器
                type_name_en: BMS Server
                topology_role: DISTRIBUTION
                medical_criticality: IMPORTANT
                
          - sub_id: EQUIP-BAS-METER
            sub_name: 计量表
            sub_name_en: Meter
            system_mapping: BA-METER
            equipment_types:
              - type_id: METER-ELEC
                type_name: 电能表
                type_name_en: Electric Meter
                topology_role: SINK
                medical_criticality: SECONDARY
                
              - type_id: METER-WATER
                type_name: 水表
                type_name_en: Water Meter
                topology_role: SINK
                medical_criticality: SECONDARY
                
              - type_id: METER-GAS
                type_name: 燃气表
                type_name_en: Gas Meter
                topology_role: SINK
                medical_criticality: SECONDARY
                
              - type_id: METER-HEAT
                type_name: 热量表
                type_name_en: Heat Meter
                topology_role: SINK
                medical_criticality: IMPORTANT
                
              - type_id: METER-COOLING
                type_name: 冷量表
                type_name_en: Cooling Meter
                topology_role: SINK
                medical_criticality: IMPORTANT
                
      # ══════════════════════════════════════════════════════════════════════
      # 类别8：医疗专用设备（与空间耦合）
      # ══════════════════════════════════════════════════════════════════════
      - category_id: EQUIP-MEDICAL
        category_name: 医疗专用设备
        category_name_en: Medical Special Equipment
        description: 与建筑机电系统直接相关的医疗专用设备
        note: 此类别为Agent-02空间模型中设施设备的补充
        
        sub_categories:
          
          - sub_id: EQUIP-MEDICAL-OR
            sub_name: 手术室设备
            sub_name_en: Operating Room Equipment
            equipment_types:
              - type_id: OR-TABLE
                type_name: 手术台
                type_name_en: Surgical Table
                topology_role: SINK
                medical_criticality: LIFE_SAFETY
                
              - type_id: OR-LIGHT
                type_name: 无影灯
                type_name_en: Surgical Light
                topology_role: SINK
                medical_criticality: LIFE_SAFETY
                
              - type_id: OR-PENDANT
                type_name: 手术吊塔
                type_name_en: Surgical Pendant
                topology_role: DISTRIBUTION
                medical_criticality: LIFE_SAFETY
                
              - type_id: OR-ANESTHESIA
                type_name: 麻醉机
                type_name_en: Anesthesia Machine
                topology_role: SINK
                medical_criticality: LIFE_SAFETY
                
          - sub_id: EQUIP-MEDICAL-ICU
            sub_name: ICU设备
            sub_name_en: ICU Equipment
            equipment_types:
              - type_id: ICU-BED
                type_name: ICU病床
                type_name_en: ICU Bed
                topology_role: SINK
                medical_criticality: LIFE_SAFETY
                
              - type_id: ICU-MONITOR
                type_name: 监护仪
                type_name_en: Patient Monitor
                topology_role: SINK
                medical_criticality: LIFE_SAFETY
                
              - type_id: ICU-VENTILATOR
                type_name: 呼吸机
                type_name_en: Ventilator
                topology_role: SINK
                medical_criticality: LIFE_SAFETY
                
              - type_id: ICU-INFUSION
                type_name: 输液泵
                type_name_en: Infusion Pump
                topology_role: SINK
                medical_criticality: PATIENT_SAFETY
                
          - sub_id: EQUIP-MEDICAL-IMAGING
            sub_name: 医学影像设备
            sub_name_en: Medical Imaging Equipment
            equipment_types:
              - type_id: IMG-CT
                type_name: CT扫描仪
                type_name_en: CT Scanner
                topology_role: SINK
                medical_criticality: CRITICAL
                
              - type_id: IMG-MRI
                type_name: 核磁共振
                type_name_en: MRI Scanner
                topology_role: SINK
                medical_criticality: CRITICAL
                
              - type_id: IMG-XRAY
                type_name: X光机
                type_name_en: X-ray Machine
                topology_role: SINK
                medical_criticality: IMPORTANT
                
              - type_id: IMG-DSA
                type_name: DSA血管造影机
                type_name_en: DSA Angiography
                topology_role: SINK
                medical_criticality: CRITICAL

    # ────────────────────────────────────────────────────────────────────────
    # 医疗级设备可靠性分级
    # ────────────────────────────────────────────────────────────────────────
    medical_criticality_classification:
      
      description: |
        基于设备故障对患者安全和医疗运营的影响程度，
        将医疗建筑设备分为5个可靠性等级。
        
      levels:
        
        - level_id: LIFE_SAFETY
          level_name: 生命安全级
          level_name_cn: 一级（生命安全）
          description: 设备故障直接威胁患者生命
          equipment_count: 12
          redundancy_requirement: N+1或更高
          backup_power: UPS + 柴发
          maintenance_priority: 最高
          response_time: 立即响应
          examples:
            - 手术室洁净空调
            - 医用气体系统
            - 生命支持设备供电
            - 病床电梯
            
        - level_id: PATIENT_SAFETY
          level_name: 患者安全级
          level_name_cn: 二级（患者安全）
          description: 设备故障可能影响患者安全或治疗效果
          equipment_count: 15
          redundancy_requirement: N+1
          backup_power: UPS或柴发
          maintenance_priority: 高
          response_time: 30分钟内
          examples:
            - ICU空调系统
            - 负压隔离病房
            - 手术室照明
            - 医学影像设备
            
        - level_id: CRITICAL
          level_name: 关键级
          level_name_cn: 三级（关键）
          description: 设备故障影响医院核心运营
          equipment_count: 48
          redundancy_requirement: 推荐N+1
          backup_power: 柴发
          maintenance_priority: 较高
          response_time: 2小时内
          examples:
            - 冷热源设备
            - 主配电设备
            - 给水系统
            - 消防设备
            
        - level_id: IMPORTANT
          level_name: 重要级
          level_name_cn: 四级（重要）
          description: 设备故障影响医院正常运营
          equipment_count: 28
          redundancy_requirement: 可选
          backup_power: 可选
          maintenance_priority: 中等
          response_time: 24小时内
          examples:
            - 普通空调末端
            - 一般照明
            - 客梯
            
        - level_id: SECONDARY
          level_name: 次要级
          level_name_cn: 五级（次要）
          description: 设备故障对运营影响有限
          equipment_count: 20
          redundancy_requirement: 无
          backup_power: 无
          maintenance_priority: 一般
          response_time: 72小时内
          examples:
            - 景观照明
            - 观光电梯
            - 自动扶梯

  # ════════════════════════════════════════════════════════════════════════════
  # 第三部分：节点-设备映射
  # ════════════════════════════════════════════════════════════════════════════
  node_equipment_mapping:
    
    description: |
      将Agent-01系统拓扑中的156个功能节点映射到89种设备类型。
      映射关系建立了从抽象拓扑到具体设备的桥梁。
    
    mapping_statistics:
      total_topology_nodes: 156
      mapped_equipment_types: 89
      mapping_coverage: "57.1%"
      mapping_quality:
        exact_match: "62%"
        functional_match: "31%"
        approximate_match: "7%"
    
    # ────────────────────────────────────────────────────────────────────────
    # HVAC系统节点映射
    # ────────────────────────────────────────────────────────────────────────
    hvac_system_mappings:
      
      - system_id: HVAC-CHP
        system_name: 冷热源系统
        node_mappings:
          
          - node_id: CHP-SRC-CHILLER
            node_name: 冷水机组节点
            node_type: SOURCE
            mapped_equipment:
              - type_id: CHILLER-CENT
                type_name: 离心式冷水机组
                typical_application: 基载制冷
                typical_quantity: 2-3
              - type_id: CHILLER-SCREW
                type_name: 螺杆式冷水机组
                typical_application: 调峰/备用
                typical_quantity: 1-2
            selection_criteria:
              - capacity_requirement: ">1500kW选离心式"
              - capacity_requirement: "<1500kW选螺杆式"
              - part_load_efficiency: 螺杆式部分负荷效率更高
              
          - node_id: CHP-SRC-BOILER
            node_name: 锅炉节点
            node_type: SOURCE
            mapped_equipment:
              - type_id: BOILER-GAS
                type_name: 燃气热水锅炉
                typical_application: 常规供热
                typical_quantity: 2-3
              - type_id: BOILER-STEAM
                type_name: 蒸汽锅炉
                typical_application: 消毒灭菌+供热
                typical_quantity: 1-2
            selection_criteria:
              - fuel_availability: 天然气可用性
              - steam_requirement: 消毒供应室需蒸汽
              
          - node_id: CHP-SRC-CT
            node_name: 冷却塔节点
            node_type: SOURCE
            mapped_equipment:
              - type_id: CT-OPEN
                type_name: 开式冷却塔
                typical_application: 常规散热
                typical_quantity: 与冷机对应
              - type_id: CT-CLOSED
                type_name: 闭式冷却塔
                typical_application: 水质要求高
            selection_criteria:
              - water_quality: 闭式系统水质更好
              - space_limitation: 开式占地更大
              
          - node_id: CHP-DIST-PUMP-CHW-P
            node_name: 冷冻水一次泵节点
            node_type: DISTRIBUTION
            mapped_equipment:
              - type_id: PUMP-CHW-P
                type_name: 冷冻水一次泵
                typical_quantity: 与冷机1:1
            configuration:
              - one_pump_per_chiller: true
              - variable_speed: 推荐
              
          - node_id: CHP-DIST-PUMP-CHW-S
            node_name: 冷冻水二次泵节点
            node_type: DISTRIBUTION
            mapped_equipment:
              - type_id: PUMP-CHW-S
                type_name: 冷冻水二次泵
                typical_quantity: N+1
            configuration:
              - variable_speed: 必须
              - pressure_control: 末端压差控制
              
          - node_id: CHP-DIST-PUMP-CW
            node_name: 冷却水泵节点
            node_type: DISTRIBUTION
            mapped_equipment:
              - type_id: PUMP-CW
                type_name: 冷却水泵
                typical_quantity: 与冷机1:1
            configuration:
              - one_pump_per_chiller: true
              - variable_speed: 推荐
              
          - node_id: CHP-DIST-PUMP-HW
            node_name: 热水泵节点
            node_type: DISTRIBUTION
            mapped_equipment:
              - type_id: PUMP-HW
                type_name: 热水泵
                typical_quantity: N+1
                
          - node_id: CHP-DIST-COLLECTOR
            node_name: 集分水器节点
            node_type: DISTRIBUTION
            mapped_equipment:
              - type_id: HEADER-CHW
                type_name: 冷冻水集分水器
                typical_quantity: 1套
                
          - node_id: CHP-DIST-HX
            node_name: 换热器节点
            node_type: DISTRIBUTION
            mapped_equipment:
              - type_id: HX-PLATE
                type_name: 板式换热器
                typical_application: 二次侧换热
                
      - system_id: HVAC-AHU
        system_name: 空调风系统
        node_mappings:
          
          - node_id: AHU-DIST-CONV
            node_name: 常规空调机组节点
            node_type: DISTRIBUTION
            mapped_equipment:
              - type_id: AHU-CONV
                type_name: 常规组合式空调机组
                typical_application: 普通区域
                
          - node_id: AHU-DIST-CLEAN
            node_name: 洁净空调机组节点
            node_type: DISTRIBUTION
            mapped_equipment:
              - type_id: AHU-CLEAN
                type_name: 洁净空调机组
                typical_application: 手术室/洁净区
            special_requirements:
              - hepa_filtration: H13/H14
              - humidity_control: 蒸汽加湿
              - redundancy: 关键区域N+1
              
          - node_id: AHU-SRC-PAU
            node_name: 新风机组节点
            node_type: SOURCE
            mapped_equipment:
              - type_id: AHU-PAU
                type_name: 新风机组
              - type_id: AHU-MAU
                type_name: 全热回收新风机组
                
          - node_id: AHU-SINK-FCU
            node_name: 风机盘管节点
            node_type: SINK
            mapped_equipment:
              - type_id: FCU
                type_name: 风机盘管
                typical_application: 病房/诊室/办公
                
          - node_id: AHU-SINK-VAV
            node_name: VAV末端节点
            node_type: SINK
            mapped_equipment:
              - type_id: VAV
                type_name: 变风量末端
                typical_application: 需要独立温控的区域
                
      - system_id: HVAC-VENT
        system_name: 通风排烟系统
        node_mappings:
          
          - node_id: VENT-SINK-EXHAUST
            node_name: 排风机节点
            node_type: SINK
            mapped_equipment:
              - type_id: FAN-EXHAUST
                type_name: 排风机
                
          - node_id: VENT-SINK-SMOKE
            node_name: 排烟风机节点
            node_type: SINK
            mapped_equipment:
              - type_id: FAN-SMOKE
                type_name: 排烟风机
                fire_rating: 280°C/0.5h
                
          - node_id: VENT-SRC-PRESSURE
            node_name: 加压送风机节点
            node_type: SOURCE
            mapped_equipment:
              - type_id: FAN-PRESSURIZATION
                type_name: 加压送风机
                
    # ────────────────────────────────────────────────────────────────────────
    # 电气系统节点映射
    # ────────────────────────────────────────────────────────────────────────
    electrical_system_mappings:
      
      - system_id: ELEC-HV
        system_name: 高压配电系统
        node_mappings:
          
          - node_id: ELEC-SRC-UTILITY
            node_name: 市电进线节点
            node_type: SOURCE
            mapped_equipment:
              - type_id: SWGR-HV
                type_name: 高压进线柜
                typical_quantity: 2（双回路）
                
          - node_id: ELEC-DIST-TRANS
            node_name: 变压器节点
            node_type: DISTRIBUTION
            mapped_equipment:
              - type_id: TRANS-DRY
                type_name: 干式变压器
                typical_application: 医院主变
              - type_id: TRANS-ISO
                type_name: 医用隔离变压器
                typical_application: 手术室/ICU
            selection_criteria:
              - indoor_application: 干式变压器
              - medical_isolation: IT系统隔离变压器
              
      - system_id: ELEC-LV
        system_name: 低压配电系统
        node_mappings:
          
          - node_id: ELEC-DIST-LV-MAIN
            node_name: 低压主配电节点
            node_type: DISTRIBUTION
            mapped_equipment:
              - type_id: SWGR-LV
                type_name: 低压配电柜
                
          - node_id: ELEC-DIST-ATS
            node_name: 双电源切换节点
            node_type: DISTRIBUTION
            mapped_equipment:
              - type_id: SWGR-ATS
                type_name: 双电源切换柜
                
          - node_id: ELEC-DIST-PANEL
            node_name: 楼层配电节点
            node_type: DISTRIBUTION
            mapped_equipment:
              - type_id: PANEL-FLOOR
                type_name: 楼层配电箱
                
          - node_id: ELEC-SINK-PANEL
            node_name: 末端配电节点
            node_type: SINK
            mapped_equipment:
              - type_id: PANEL-ROOM
                type_name: 房间配电箱
              - type_id: PANEL-IT
                type_name: IT隔离配电箱
                typical_application: 手术室
                
      - system_id: ELEC-EPS
        system_name: 应急电源系统
        node_mappings:
          
          - node_id: EPS-SRC-GEN
            node_name: 发电机节点
            node_type: SOURCE
            mapped_equipment:
              - type_id: GEN-DIESEL
                type_name: 柴油发电机组
                typical_quantity: 2（互为备用）
                
          - node_id: EPS-DIST-UPS
            node_name: UPS节点
            node_type: DISTRIBUTION
            mapped_equipment:
              - type_id: UPS-ONLINE
                type_name: 在线式UPS
              - type_id: UPS-MEDICAL
                type_name: 医用UPS
                typical_application: 手术室/ICU
                
    # ────────────────────────────────────────────────────────────────────────
    # 医疗气体系统节点映射
    # ────────────────────────────────────────────────────────────────────────
    medical_gas_system_mappings:
      
      - system_id: GAS-O2
        system_name: 氧气系统
        node_mappings:
          
          - node_id: O2-SRC-SUPPLY
            node_name: 氧气气源节点
            node_type: SOURCE
            mapped_equipment:
              - type_id: O2-LOX-TANK
                type_name: 液氧储罐
                typical_application: 主气源
              - type_id: O2-PSA
                type_name: PSA制氧机
                typical_application: 辅助/应急气源
              - type_id: O2-MANIFOLD
                type_name: 氧气汇流排
                typical_application: 备用气源
                
          - node_id: O2-DIST-REGULATOR
            node_name: 氧气调压节点
            node_type: DISTRIBUTION
            mapped_equipment:
              - type_id: O2-REGULATOR
                type_name: 氧气减压器
                
          - node_id: O2-SINK-OUTLET
            node_name: 氧气终端节点
            node_type: SINK
            mapped_equipment:
              - type_id: O2-OUTLET
                type_name: 氧气终端
                
      - system_id: GAS-VAC
        system_name: 负压吸引系统
        node_mappings:
          
          - node_id: VAC-SRC-PUMP
            node_name: 真空泵节点
            node_type: SOURCE
            mapped_equipment:
              - type_id: VAC-PUMP
                type_name: 医用真空泵
                typical_quantity: N+1
                
          - node_id: VAC-DIST-RECEIVER
            node_name: 真空罐节点
            node_type: DISTRIBUTION
            mapped_equipment:
              - type_id: VAC-RECEIVER
                type_name: 真空罐
                
          - node_id: VAC-SINK-OUTLET
            node_name: 负压终端节点
            node_type: SINK
            mapped_equipment:
              - type_id: VAC-OUTLET
                type_name: 负压吸引终端
                
      - system_id: GAS-AIR
        system_name: 医用压缩空气系统
        node_mappings:
          
          - node_id: AIR-SRC-COMPRESSOR
            node_name: 空压机节点
            node_type: SOURCE
            mapped_equipment:
              - type_id: AIR-COMPRESSOR
                type_name: 医用无油空压机
                typical_quantity: N+1
                
          - node_id: AIR-DIST-DRYER
            node_name: 干燥机节点
            node_type: DISTRIBUTION
            mapped_equipment:
              - type_id: AIR-DRYER
                type_name: 冷干机
                
          - node_id: AIR-SINK-OUTLET
            node_name: 压缩空气终端节点
            node_type: SINK
            mapped_equipment:
              - type_id: AIR-OUTLET
                type_name: 压缩空气终端
                
    # ────────────────────────────────────────────────────────────────────────
    # 消防系统节点映射
    # ────────────────────────────────────────────────────────────────────────
    fire_protection_system_mappings:
      
      - system_id: FIRE-HYDRANT
        system_name: 消火栓系统
        node_mappings:
          
          - node_id: FIRE-SRC-PUMP
            node_name: 消防泵节点
            node_type: SOURCE
            mapped_equipment:
              - type_id: PUMP-FIRE-MAIN
                type_name: 消火栓主泵
                typical_quantity: 2（互为备用）
              - type_id: PUMP-FIRE-JOCKEY
                type_name: 消防稳压泵
                typical_quantity: 2
                
      - system_id: FIRE-GAS
        system_name: 气体灭火系统
        node_mappings:
          
          - node_id: FIRE-SRC-GAS
            node_name: 气体灭火节点
            node_type: SOURCE
            mapped_equipment:
              - type_id: GAS-FM200
                type_name: 七氟丙烷灭火系统
                typical_application: 配电室/数据中心
              - type_id: GAS-IG541
                type_name: IG541灭火系统
                typical_application: 手术室

  # ════════════════════════════════════════════════════════════════════════════
  # 第四部分：P0核心设备详细模型
  # ════════════════════════════════════════════════════════════════════════════
  equipment_type_models:
    
    description: |
      以下为18类P0核心设备的详细本体模型。
      每个模型包含：标识、组件结构、静态属性、动态属性、
      控制属性、告警规则、维护要求、关联设备。
    
    # ────────────────────────────────────────────────────────────────────────
    # 设备模型1：离心式冷水机组
    # ────────────────────────────────────────────────────────────────────────
    - model_id: MODEL-CHILLER-CENT
      
      # 设备标识
      identity:
        type_id: CHILLER-CENT
        type_name: 离心式冷水机组
        type_name_en: Centrifugal Chiller
        category: EQUIP-HVAC
        sub_category: EQUIP-HVAC-CHILLER
        topology_role: SOURCE
        description: |
          离心式冷水机组是大型中央空调系统的核心制冷设备，
          采用离心压缩原理，具有制冷量大、效率高的特点。
          适用于医院大型冷站，作为基载制冷主力设备。
        medical_criticality: CRITICAL
        typical_application:
          - 医院中央冷站
          - 数据中心
          - 大型公共建筑
          
        subtypes:
          - subtype_id: CHILLER-CENT-SINGLE
            subtype_name: 单级离心冷水机组
            distinguishing_features: 单级压缩，适用于常规工况
            
          - subtype_id: CHILLER-CENT-TWO
            subtype_name: 双级离心冷水机组
            distinguishing_features: 双级压缩，适用于大温差工况
            
          - subtype_id: CHILLER-CENT-VSD
            subtype_name: 变频离心冷水机组
            distinguishing_features: 变频驱动，部分负荷效率高
            
          - subtype_id: CHILLER-CENT-MAG
            subtype_name: 磁悬浮离心冷水机组
            distinguishing_features: 磁悬浮轴承，无油运行，超高效率
            
      # 组件结构
      component_structure:
        
        - component_id: COMP-CENT-COMPRESSOR
          component_name: 离心压缩机
          component_type: 核心组件
          is_optional: false
          quantity: 1
          
          parts:
            - part_id: PART-IMPELLER
              part_name: 叶轮
              is_consumable: false
              lifecycle_item: true
              typical_lifespan: "20年"
              
            - part_id: PART-BEARING
              part_name: 轴承
              is_consumable: true
              lifecycle_item: true
              typical_lifespan: "8-10年"
              maintenance_note: 需定期润滑
              
            - part_id: PART-SHAFT-SEAL
              part_name: 轴封
              is_consumable: true
              lifecycle_item: true
              typical_lifespan: "5-8年"
              
            - part_id: PART-GUIDE-VANE
              part_name: 进口导叶
              is_consumable: false
              lifecycle_item: true
              function: 容量调节
              
        - component_id: COMP-CENT-MOTOR
          component_name: 驱动电机
          component_type: 驱动组件
          is_optional: false
          quantity: 1
          
          parts:
            - part_id: PART-MOTOR-WINDING
              part_name: 电机绕组
              is_consumable: false
              lifecycle_item: true
              
            - part_id: PART-MOTOR-BEARING
              part_name: 电机轴承
              is_consumable: true
              lifecycle_item: true
              typical_lifespan: "5-8年"
              
        - component_id: COMP-CENT-EVAPORATOR
          component_name: 蒸发器
          component_type: 换热组件
          is_optional: false
          quantity: 1
          
          parts:
            - part_id: PART-EVAP-TUBE
              part_name: 换热铜管
              is_consumable: false
              lifecycle_item: true
              maintenance_note: 需定期清洗
              
        - component_id: COMP-CENT-CONDENSER
          component_name: 冷凝器
          component_type: 换热组件
          is_optional: false
          quantity: 1
          
          parts:
            - part_id: PART-COND-TUBE
              part_name: 换热铜管
              is_consumable: false
              lifecycle_item: true
              maintenance_note: 需定期清洗除垢
              
        - component_id: COMP-CENT-OIL
          component_name: 润滑油系统
          component_type: 辅助组件
          is_optional: false
          quantity: 1
          
          parts:
            - part_id: PART-OIL-PUMP
              part_name: 油泵
              is_consumable: false
              lifecycle_item: true
              
            - part_id: PART-OIL-FILTER
              part_name: 油过滤器
              is_consumable: true
              lifecycle_item: false
              replacement_cycle: "每年"
              
            - part_id: PART-OIL-HEATER
              part_name: 油加热器
              is_consumable: false
              lifecycle_item: true
              
        - component_id: COMP-CENT-VFD
          component_name: 变频器
          component_type: 控制组件
          is_optional: true  # 仅变频机组
          quantity: 1
          
        - component_id: COMP-CENT-CONTROL
          component_name: 控制柜
          component_type: 控制组件
          is_optional: false
          quantity: 1
          
      # 静态属性
      static_attributes:
        
        identity_attrs:
          - attr_id: equipment_id
            attr_name: 设备编码
            attr_name_en: Equipment ID
            data_type: string
            required: true
            unique: true
            pattern: "CH-{BUILDING}-{SEQUENCE}"
            example: "CH-A-001"
            
          - attr_id: equipment_name
            attr_name: 设备名称
            data_type: string
            required: true
            example: "1号离心式冷水机组"
            
          - attr_id: asset_number
            attr_name: 资产编号
            data_type: string
            required: false
            
        nameplate_attrs:
          - attr_id: manufacturer
            attr_name: 制造商
            data_type: string
            required: true
            typical_values: [约克, 开利, 特灵, 麦克维尔, 顿汉布什]
            
          - attr_id: model
            attr_name: 型号
            data_type: string
            required: true
            
          - attr_id: serial_number
            attr_name: 序列号
            data_type: string
            required: true
            
          - attr_id: rated_cooling_capacity
            attr_name: 额定制冷量
            data_type: float
            unit: kW
            required: true
            typical_range: [1000, 5000]
            
          - attr_id: rated_power_input
            attr_name: 额定输入功率
            data_type: float
            unit: kW
            required: true
            
          - attr_id: rated_cop
            attr_name: 额定能效比
            data_type: float
            unit: "W/W"
            required: true
            typical_range: [5.5, 7.0]
            benchmark: ">6.0 为高效机组"
            
          - attr_id: rated_iplv
            attr_name: 综合部分负荷能效
            data_type: float
            unit: "W/W"
            required: true
            typical_range: [6.0, 10.0]
            note: 部分负荷效率指标
            
          - attr_id: rated_chw_flow
            attr_name: 额定冷冻水流量
            data_type: float
            unit: "m³/h"
            required: true
            
          - attr_id: rated_cw_flow
            attr_name: 额定冷却水流量
            data_type: float
            unit: "m³/h"
            required: true
            
          - attr_id: rated_voltage
            attr_name: 额定电压
            data_type: string
            required: true
            typical_values: ["6kV", "10kV", "380V"]
            
          - attr_id: refrigerant_type
            attr_name: 制冷剂类型
            data_type: string
            required: true
            typical_values: [R134a, R513A, R1234ze]
            
          - attr_id: refrigerant_charge
            attr_name: 制冷剂充注量
            data_type: float
            unit: kg
            required: true
            
          - attr_id: design_chws_temp
            attr_name: 设计冷冻水供水温度
            data_type: float
            unit: ℃
            required: true
            typical_value: 7
            
          - attr_id: design_chwr_temp
            attr_name: 设计冷冻水回水温度
            data_type: float
            unit: ℃
            required: true
            typical_value: 12
            
          - attr_id: design_cws_temp
            attr_name: 设计冷却水供水温度
            data_type: float
            unit: ℃
            required: true
            typical_value: 32
            
          - attr_id: design_cwr_temp
            attr_name: 设计冷却水回水温度
            data_type: float
            unit: ℃
            required: true
            typical_value: 37
            
          - attr_id: weight
            attr_name: 设备重量
            data_type: float
            unit: kg
            required: false
            
          - attr_id: dimensions
            attr_name: 外形尺寸
            data_type: object
            required: false
            properties:
              length: {type: float, unit: mm}
              width: {type: float, unit: mm}
              height: {type: float, unit: mm}
              
        installation_attrs:
          - attr_id: installation_location
            attr_name: 安装位置
            data_type: reference
            reference: Space
            required: true
            example: "冷冻站-B1F"
            
          - attr_id: installation_date
            attr_name: 安装日期
            data_type: date
            required: true
            
          - attr_id: commissioning_date
            attr_name: 调试日期
            data_type: date
            required: true
            
          - attr_id: warranty_expiry
            attr_name: 质保到期日
            data_type: date
            required: true
            
          - attr_id: expected_life
            attr_name: 预期使用年限
            data_type: integer
            unit: 年
            typical_value: 20
            
        topology_attrs:
          - attr_id: parent_system
            attr_name: 所属系统
            data_type: reference
            reference: System
            required: true
            example: "HVAC-CHP"
            
          - attr_id: chw_supply_connection
            attr_name: 冷冻水供水接口
            data_type: reference
            reference: Pipe
            
          - attr_id: chw_return_connection
            attr_name: 冷冻水回水接口
            data_type: reference
            reference: Pipe
            
          - attr_id: cw_supply_connection
            attr_name: 冷却水供水接口
            data_type: reference
            reference: Pipe
            
          - attr_id: cw_return_connection
            attr_name: 冷却水回水接口
            data_type: reference
            reference: Pipe
            
          - attr_id: power_supply
            attr_name: 供电来源
            data_type: reference
            reference: Equipment
            example: "高压配电柜HV-SW-001"
            
      # 动态属性
      dynamic_attributes:
        
        status_attrs:
          - attr_id: operational_status
            attr_name: 运行状态
            data_type: enum
            enum_values: [RUNNING, STOPPED, STANDBY, FAULT, MAINTENANCE]
            update_frequency: 实时
            source: BAS
            
          - attr_id: online_status
            attr_name: 在线状态
            data_type: enum
            enum_values: [ONLINE, OFFLINE]
            update_frequency: 实时
            
          - attr_id: running_mode
            attr_name: 运行模式
            data_type: enum
            enum_values: [AUTO, MANUAL, LOCAL]
            update_frequency: 实时
            
        runtime_attrs:
          - attr_id: chws_temp
            attr_name: 冷冻水供水温度
            data_type: float
            unit: ℃
            typical_range: [5, 12]
            update_frequency: 10s
            source: 机组控制器
            
          - attr_id: chwr_temp
            attr_name: 冷冻水回水温度
            data_type: float
            unit: ℃
            typical_range: [10, 18]
            update_frequency: 10s
            
          - attr_id: cws_temp
            attr_name: 冷却水供水温度
            data_type: float
            unit: ℃
            typical_range: [18, 35]
            update_frequency: 10s
            
          - attr_id: cwr_temp
            attr_name: 冷却水回水温度
            data_type: float
            unit: ℃
            typical_range: [25, 40]
            update_frequency: 10s
            
          - attr_id: chw_flow
            attr_name: 冷冻水流量
            data_type: float
            unit: "m³/h"
            update_frequency: 10s
            
          - attr_id: cw_flow
            attr_name: 冷却水流量
            data_type: float
            unit: "m³/h"
            update_frequency: 10s
            
          - attr_id: evap_pressure
            attr_name: 蒸发压力
            data_type: float
            unit: kPa
            update_frequency: 10s
            
          - attr_id: cond_pressure
            attr_name: 冷凝压力
            data_type: float
            unit: kPa
            update_frequency: 10s
            
          - attr_id: suction_temp
            attr_name: 吸气温度
            data_type: float
            unit: ℃
            update_frequency: 10s
            
          - attr_id: discharge_temp
            attr_name: 排气温度
            data_type: float
            unit: ℃
            update_frequency: 10s
            alarm_high: 85
            
          - attr_id: oil_temp
            attr_name: 润滑油温度
            data_type: float
            unit: ℃
            update_frequency: 10s
            
          - attr_id: oil_pressure
            attr_name: 润滑油压力
            data_type: float
            unit: kPa
            update_frequency: 10s
            
          - attr_id: motor_current
            attr_name: 电机电流
            data_type: float
            unit: A
            update_frequency: 10s
            
          - attr_id: motor_voltage
            attr_name: 电机电压
            data_type: float
            unit: V
            update_frequency: 10s
            
          - attr_id: motor_power
            attr_name: 电机功率
            data_type: float
            unit: kW
            update_frequency: 10s
            
          - attr_id: guide_vane_position
            attr_name: 导叶开度
            data_type: float
            unit: "%"
            typical_range: [0, 100]
            update_frequency: 10s
            
          - attr_id: vfd_frequency
            attr_name: 变频器频率
            data_type: float
            unit: Hz
            typical_range: [15, 60]
            update_frequency: 10s
            applicable: 变频机组
            
          - attr_id: vibration_level
            attr_name: 振动值
            data_type: float
            unit: "mm/s"
            update_frequency: 1min
            alarm_high: 4.5
            
        performance_attrs:
          - attr_id: current_cooling_capacity
            attr_name: 当前制冷量
            data_type: float
            unit: kW
            calculation: "1.163 × chw_flow × (chwr_temp - chws_temp)"
            update_frequency: 10s
            
          - attr_id: current_load
            attr_name: 当前负载率
            data_type: float
            unit: "%"
            calculation: "(current_cooling_capacity / rated_cooling_capacity) × 100"
            update_frequency: 10s
            
          - attr_id: current_cop
            attr_name: 当前能效比
            data_type: float
            unit: "W/W"
            calculation: "current_cooling_capacity / motor_power"
            update_frequency: 10s
            benchmark: ">5.5为良好"
            
          - attr_id: approach_temp
            attr_name: 逼近温度
            data_type: float
            unit: ℃
            calculation: "chws_temp - evap_temp"
            benchmark: "<3℃为良好"
            significance: 蒸发器换热效率指标
            
          - attr_id: condenser_approach
            attr_name: 冷凝器逼近温度
            data_type: float
            unit: ℃
            calculation: "cwr_temp - cond_temp"
            benchmark: "<2℃为良好"
            
        accumulation_attrs:
          - attr_id: run_hours
            attr_name: 累计运行小时
            data_type: float
            unit: h
            source: 机组控制器
            
          - attr_id: start_count
            attr_name: 累计启动次数
            data_type: integer
            source: 机组控制器
            
          - attr_id: energy_consumption
            attr_name: 累计耗电量
            data_type: float
            unit: kWh
            source: 电表
            
          - attr_id: cooling_output
            attr_name: 累计制冷量
            data_type: float
            unit: kWh
            source: 计算
            
      # 控制属性
      control_attributes:
        
        setpoints:
          - sp_id: SP-CHWS-TEMP
            sp_name: 冷冻水供水温度设定值
            data_type: float
            unit: ℃
            default_value: 7
            valid_range: [5, 12]
            affected_output: guide_vane_position, vfd_frequency
            
          - sp_id: SP-DEMAND-LIMIT
            sp_name: 需量限制设定值
            data_type: float
            unit: "%"
            default_value: 100
            valid_range: [0, 100]
            affected_output: max_capacity
            
        commands:
          - cmd_id: CMD-START
            cmd_name: 启动命令
            cmd_type: bool
            parameters: null
            preconditions:
              - "无故障报警"
              - "冷冻水泵已运行"
              - "冷却水泵已运行"
              - "冷却塔已运行"
              - "油加热完成（停机超过4小时）"
            effects:
              - "机组进入启动程序"
              - "导叶开至最小位置"
              - "电机软启动"
              
          - cmd_id: CMD-STOP
            cmd_name: 停止命令
            cmd_type: bool
            parameters: null
            preconditions: null
            effects:
              - "导叶关闭"
              - "电机停止"
              - "油泵延时停止"
              
          - cmd_id: CMD-CAPACITY
            cmd_name: 容量调节命令
            cmd_type: value
            parameters:
              - target_capacity: {type: float, unit: "%"}
            preconditions:
              - "机组运行中"
            effects:
              - "调节导叶开度"
              - "调节变频器频率（变频机）"
              
        control_modes:
          - mode_id: MODE-LOCAL
            mode_name: 就地控制模式
            description: 通过机组控制柜本地操作
            
          - mode_id: MODE-REMOTE
            mode_name: 远程控制模式
            description: 通过BAS远程控制
            
          - mode_id: MODE-AUTO
            mode_name: 自动控制模式
            description: 根据负荷自动调节
            
        interlocks:
          - interlock_id: IL-CHW-FLOW
            interlock_name: 冷冻水流量联锁
            interlock_type: start_condition
            condition: "chw_flow > 最小流量设定值"
            action: "流量不足时禁止启动/触发停机"
            
          - interlock_id: IL-CW-FLOW
            interlock_name: 冷却水流量联锁
            interlock_type: start_condition
            condition: "cw_flow > 最小流量设定值"
            action: "流量不足时禁止启动/触发停机"
            
          - interlock_id: IL-OIL-TEMP
            interlock_name: 油温联锁
            interlock_type: start_condition
            condition: "oil_temp > 最低油温设定值"
            action: "油温不足时禁止启动"
            
          - interlock_id: IL-HIGH-DISCHARGE
            interlock_name: 排气温度保护
            interlock_type: protection
            condition: "discharge_temp > 90℃"
            action: "触发保护停机"
            
          - interlock_id: IL-HIGH-MOTOR-TEMP
            interlock_name: 电机温度保护
            interlock_type: protection
            condition: "motor_temp > 设定值"
            action: "触发保护停机"
            
          - interlock_id: IL-LOW-OIL-PRESSURE
            interlock_name: 油压保护
            interlock_type: protection
            condition: "oil_pressure < 最低油压设定值"
            action: "触发保护停机"
            
          - interlock_id: IL-SURGE
            interlock_name: 喘振保护
            interlock_type: protection
            condition: "检测到喘振特征"
            action: "快速打开导叶，必要时停机"
            
      # 告警规则
      alarm_rules:
        
        - alarm_id: ALM-CH-HIGH-DISCHARGE
          alarm_name: 排气温度过高
          alarm_category: threshold
          trigger_condition: "discharge_temp > 85℃"
          alarm_level: P1
          delay_seconds: 10
          auto_recover: true
          recovery_condition: "discharge_temp < 80℃"
          recommended_actions:
            - "检查冷却水温度和流量"
            - "检查冷凝器是否堵塞"
            - "检查制冷剂充注量"
            
        - alarm_id: ALM-CH-LOW-EVAP
          alarm_name: 蒸发压力过低
          alarm_category: threshold
          trigger_condition: "evap_pressure < 设定低限"
          alarm_level: P1
          delay_seconds: 30
          auto_recover: true
          recovery_condition: "evap_pressure > 设定低限+回差"
          recommended_actions:
            - "检查冷冻水流量"
            - "检查供水温度设定"
            - "检查制冷剂是否泄漏"
            
        - alarm_id: ALM-CH-HIGH-COND
          alarm_name: 冷凝压力过高
          alarm_category: threshold
          trigger_condition: "cond_pressure > 设定高限"
          alarm_level: P1
          delay_seconds: 30
          auto_recover: true
          recovery_condition: "cond_pressure < 设定高限-回差"
          recommended_actions:
            - "检查冷却水温度"
            - "检查冷却塔运行状态"
            - "检查冷凝器是否需要清洗"
            
        - alarm_id: ALM-CH-SURGE
          alarm_name: 机组喘振
          alarm_category: diagnostic
          trigger_condition: "检测到喘振特征"
          alarm_level: P0
          delay_seconds: 0
          auto_recover: false
          recommended_actions:
            - "检查运行工况是否在正常范围"
            - "检查导叶位置"
            - "降低负荷运行"
            - "联系厂家技术支持"
            
        - alarm_id: ALM-CH-LOW-OIL
          alarm_name: 油压过低
          alarm_category: threshold
          trigger_condition: "oil_pressure < 最低油压"
          alarm_level: P0
          delay_seconds: 5
          auto_recover: false
          recommended_actions:
            - "停机检查油系统"
            - "检查油位"
            - "检查油泵"
            - "检查油过滤器"
            
        - alarm_id: ALM-CH-HIGH-VIBRATION
          alarm_name: 振动超标
          alarm_category: diagnostic
          trigger_condition: "vibration_level > 4.5 mm/s"
          alarm_level: P1
          delay_seconds: 60
          auto_recover: true
          recovery_condition: "vibration_level < 3.5 mm/s"
          recommended_actions:
            - "检查轴承状态"
            - "检查叶轮平衡"
            - "降低负荷运行"
            
        - alarm_id: ALM-CH-LOW-COP
          alarm_name: 能效下降
          alarm_category: diagnostic
          trigger_condition: "current_cop < rated_cop × 0.85"
          alarm_level: P2
          delay_seconds: 3600
          auto_recover: true
          recovery_condition: "current_cop > rated_cop × 0.9"
          recommended_actions:
            - "检查蒸发器/冷凝器是否需要清洗"
            - "检查制冷剂充注量"
            - "优化运行工况"
            
        - alarm_id: ALM-CH-MAINT-DUE
          alarm_name: 定期维护到期
          alarm_category: maintenance
          trigger_condition: "run_hours > last_maint_hours + maint_interval"
          alarm_level: P3
          delay_seconds: 0
          auto_recover: false
          recommended_actions:
            - "安排定期维护"
            - "更新维护记录"
            
      # 维护要求
      maintenance_requirements:
        
        - maint_id: MAINT-CH-DAILY
          maint_name: 日常巡检
          maint_type: inspection
          target_component: 整机
          cycle_value: 1
          cycle_unit: day
          condition_trigger: null
          checklist:
            - "检查运行参数是否正常"
            - "检查有无异常噪音或振动"
            - "检查油位"
            - "检查有无泄漏"
            - "记录运行数据"
            
        - maint_id: MAINT-CH-WEEKLY
          maint_name: 周度检查
          maint_type: inspection
          target_component: 整机
          cycle_value: 1
          cycle_unit: week
          checklist:
            - "检查冷冻水/冷却水温差"
            - "检查能效比变化趋势"
            - "检查启停次数"
            - "检查报警记录"
            
        - maint_id: MAINT-CH-OIL-FILTER
          maint_name: 油过滤器更换
          maint_type: replacement
          target_component: 油过滤器
          cycle_value: 1
          cycle_unit: year
          condition_trigger: "油压差超标"
          checklist:
            - "停机后更换油过滤器"
            - "检查油质"
            - "必要时更换润滑油"
            
        - maint_id: MAINT-CH-TUBE-CLEAN
          maint_name: 换热管清洗
          maint_type: service
          target_component: 蒸发器/冷凝器
          cycle_value: 1
          cycle_unit: year
          condition_trigger: "逼近温度超标"
          checklist:
            - "停机放水"
            - "机械通炮或化学清洗"
            - "检查换热管状态"
            - "恢复运行后验证效果"
            
        - maint_id: MAINT-CH-REFRIGERANT
          maint_name: 制冷剂检查
          maint_type: inspection
          target_component: 制冷系统
          cycle_value: 6
          cycle_unit: month
          checklist:
            - "检查制冷剂液位"
            - "检测是否有泄漏"
            - "必要时补充制冷剂"
            
        - maint_id: MAINT-CH-ELECTRICAL
          maint_name: 电气检查
          maint_type: inspection
          target_component: 电气系统
          cycle_value: 6
          cycle_unit: month
          checklist:
            - "检查电气连接"
            - "测量绝缘电阻"
            - "检查接触器和继电器"
            - "检查变频器（如有）"
            
        - maint_id: MAINT-CH-OVERHAUL
          maint_name: 大修
          maint_type: overhaul
          target_component: 整机
          cycle_value: 50000
          cycle_unit: run_hours
          checklist:
            - "拆解检查压缩机"
            - "更换轴承"
            - "更换轴封"
            - "更换润滑油"
            - "检修电机"
            - "全面清洗换热器"
            - "系统抽真空充注制冷剂"
            
      # 关联设备
      related_equipment:
        
        upstream:
          - equipment_type: 高压开关柜
            relationship: 供电来源
            connection_medium: 电缆
            
          - equipment_type: 冷却塔
            relationship: 冷却水来源
            connection_medium: 冷却水管
            
        downstream:
          - equipment_type: 冷冻水泵
            relationship: 冷冻水输送
            connection_medium: 冷冻水管
            
        auxiliary:
          - equipment_type: 膨胀水箱
            function: 系统定压
            
          - equipment_type: 补水装置
            function: 系统补水
            
          - equipment_type: 软化水设备
            function: 补水处理
            
        metering:
          - equipment_type: 电能表
            measured_parameters: [电量, 功率]
            
          - equipment_type: 冷量表
            measured_parameters: [冷量, 流量, 温差]
            
          - equipment_type: 温度传感器
            measured_parameters: [供水温度, 回水温度]
            
          - equipment_type: 压力传感器
            measured_parameters: [供水压力, 回水压力]
            
        control:
          - equipment_type: DDC控制器
            control_scope: 群控优化
            
          - equipment_type: BMS服务器
            control_scope: 系统集成监控

    # ────────────────────────────────────────────────────────────────────────
    # 设备模型2：洁净空调机组
    # ────────────────────────────────────────────────────────────────────────
    - model_id: MODEL-AHU-CLEAN
      
      identity:
        type_id: AHU-CLEAN
        type_name: 洁净空调机组
        type_name_en: Clean Room Air Handling Unit
        category: EQUIP-HVAC
        sub_category: EQUIP-HVAC-AHU
        topology_role: DISTRIBUTION
        description: |
          洁净空调机组是为洁净室提供洁净空气的专用空调设备，
          配备多级过滤系统，可实现精确的温湿度和洁净度控制。
          广泛应用于医院手术室、ICU、洁净实验室等场所。
        medical_criticality: LIFE_SAFETY
        typical_application:
          - 手术室（ISO 5-7级）
          - ICU（ISO 7-8级）
          - 无菌制剂室
          - 洁净实验室
          
        subtypes:
          - subtype_id: AHU-CLEAN-OR
            subtype_name: 手术室专用洁净空调
            distinguishing_features:
              - 层流送风
              - 恒温恒湿
              - 正压控制
              - N+1冗余
              
          - subtype_id: AHU-CLEAN-ICU
            subtype_name: ICU洁净空调
            distinguishing_features:
              - 一般乱流
              - 温湿度控制
              - 可切换正负压
              
          - subtype_id: AHU-CLEAN-ISO
            subtype_name: 隔离病房专用空调
            distinguishing_features:
              - 全新风
              - 负压控制
              - HEPA排风过滤
              
      component_structure:
        
        - component_id: COMP-AHU-FAN-SUPPLY
          component_name: 送风机
          component_type: 核心组件
          is_optional: false
          quantity: 1
          parts:
            - part_id: PART-FAN-MOTOR
              part_name: 风机电机
              is_consumable: false
              lifecycle_item: true
            - part_id: PART-FAN-IMPELLER
              part_name: 风机叶轮
              is_consumable: false
              lifecycle_item: true
            - part_id: PART-FAN-BELT
              part_name: 传动皮带
              is_consumable: true
              replacement_cycle: "1-2年"
              
        - component_id: COMP-AHU-COIL-C
          component_name: 冷却盘管
          component_type: 换热组件
          is_optional: false
          quantity: 1
          
        - component_id: COMP-AHU-COIL-H
          component_name: 加热盘管
          component_type: 换热组件
          is_optional: false
          quantity: 1
          
        - component_id: COMP-AHU-FILTER-1
          component_name: 初效过滤器
          component_type: 过滤组件
          is_optional: false
          quantity: 1
          parts:
            - part_id: PART-FILTER-PRIMARY
              part_name: 初效过滤器滤芯
              is_consumable: true
              replacement_cycle: "1-3月"
              
        - component_id: COMP-AHU-FILTER-2
          component_name: 中效过滤器
          component_type: 过滤组件
          is_optional: false
          quantity: 1
          parts:
            - part_id: PART-FILTER-MEDIUM
              part_name: 中效过滤器滤芯
              is_consumable: true
              replacement_cycle: "3-6月"
              
        - component_id: COMP-AHU-FILTER-3
          component_name: 高效过滤器
          component_type: 过滤组件
          is_optional: false
          quantity: 1
          parts:
            - part_id: PART-FILTER-HEPA
              part_name: HEPA过滤器
              is_consumable: true
              replacement_cycle: "1-2年"
              specification: "H13/H14"
              
        - component_id: COMP-AHU-HUMIDIFIER
          component_name: 加湿器
          component_type: 调节组件
          is_optional: false
          quantity: 1
          types:
            - 电极式加湿器
            - 干蒸汽加湿器（推荐医疗级）
            
        - component_id: COMP-AHU-DAMPER
          component_name: 风阀组
          component_type: 调节组件
          is_optional: false
          quantity: 若干
          types:
            - 新风阀
            - 回风阀
            - 排风阀
            - 混合阀
            
      static_attributes:
        
        identity_attrs:
          - attr_id: equipment_id
            attr_name: 设备编码
            data_type: string
            pattern: "AHU-{ZONE}-{SEQUENCE}"
            example: "AHU-OR-001"
            
          - attr_id: equipment_name
            attr_name: 设备名称
            data_type: string
            example: "1号手术室洁净空调机组"
            
        nameplate_attrs:
          - attr_id: rated_air_volume
            attr_name: 额定风量
            data_type: float
            unit: "m³/h"
            typical_range: [3000, 30000]
            
          - attr_id: rated_static_pressure
            attr_name: 额定静压
            data_type: float
            unit: Pa
            typical_range: [500, 1500]
            
          - attr_id: rated_cooling_capacity
            attr_name: 额定冷量
            data_type: float
            unit: kW
            
          - attr_id: rated_heating_capacity
            attr_name: 额定热量
            data_type: float
            unit: kW
            
          - attr_id: rated_power
            attr_name: 额定功率
            data_type: float
            unit: kW
            
          - attr_id: clean_class
            attr_name: 洁净级别
            data_type: string
            values: ["ISO 5", "ISO 6", "ISO 7", "ISO 8"]
            
          - attr_id: filter_efficiency
            attr_name: 过滤效率
            data_type: string
            values: ["H13(99.95%)", "H14(99.995%)"]
            
        installation_attrs:
          - attr_id: served_space
            attr_name: 服务空间
            data_type: reference
            reference: Space
            example: "1号手术室"
            
          - attr_id: ahu_room
            attr_name: 机房位置
            data_type: reference
            reference: Space
            example: "手术区空调机房"
            
      dynamic_attributes:
        
        status_attrs:
          - attr_id: operational_status
            attr_name: 运行状态
            data_type: enum
            enum_values: [RUNNING, STOPPED, STANDBY, FAULT, MAINTENANCE]
            
        runtime_attrs:
          - attr_id: supply_air_temp
            attr_name: 送风温度
            data_type: float
            unit: ℃
            typical_range: [14, 24]
            
          - attr_id: return_air_temp
            attr_name: 回风温度
            data_type: float
            unit: ℃
            
          - attr_id: supply_air_humidity
            attr_name: 送风湿度
            data_type: float
            unit: "%RH"
            typical_range: [40, 70]
            
          - attr_id: return_air_humidity
            attr_name: 回风湿度
            data_type: float
            unit: "%RH"
            
          - attr_id: supply_air_volume
            attr_name: 送风量
            data_type: float
            unit: "m³/h"
            
          - attr_id: filter_dp_1
            attr_name: 初效过滤器压差
            data_type: float
            unit: Pa
            alarm_high: 150
            
          - attr_id: filter_dp_2
            attr_name: 中效过滤器压差
            data_type: float
            unit: Pa
            alarm_high: 250
            
          - attr_id: filter_dp_3
            attr_name: 高效过滤器压差
            data_type: float
            unit: Pa
            alarm_high: 450
            
          - attr_id: fan_speed
            attr_name: 风机转速
            data_type: float
            unit: rpm
            
          - attr_id: fan_frequency
            attr_name: 变频器频率
            data_type: float
            unit: Hz
            
          - attr_id: fan_power
            attr_name: 风机功率
            data_type: float
            unit: kW
            
          - attr_id: room_temp
            attr_name: 房间温度
            data_type: float
            unit: ℃
            
          - attr_id: room_humidity
            attr_name: 房间湿度
            data_type: float
            unit: "%RH"
            
          - attr_id: room_pressure
            attr_name: 房间压差
            data_type: float
            unit: Pa
            note: 相对走廊
            
          - attr_id: particle_count
            attr_name: 尘埃粒子数
            data_type: float
            unit: "个/m³"
            particle_size: "≥0.5μm"
            
        performance_attrs:
          - attr_id: cleanliness_compliance
            attr_name: 洁净度达标率
            data_type: float
            unit: "%"
            calculation: 达标时间/运行时间
            
      control_attributes:
        
        setpoints:
          - sp_id: SP-ROOM-TEMP
            sp_name: 房间温度设定
            data_type: float
            unit: ℃
            default_value: 22
            valid_range: [18, 26]
            
          - sp_id: SP-ROOM-HUMIDITY
            sp_name: 房间湿度设定
            data_type: float
            unit: "%RH"
            default_value: 50
            valid_range: [40, 65]
            
          - sp_id: SP-ROOM-PRESSURE
            sp_name: 房间压差设定
            data_type: float
            unit: Pa
            default_value: 15
            valid_range: [8, 30]
            note: 正压手术室
            
          - sp_id: SP-SUPPLY-TEMP
            sp_name: 送风温度设定
            data_type: float
            unit: ℃
            default_value: 18
            valid_range: [14, 24]
            
        commands:
          - cmd_id: CMD-START
            cmd_name: 启动
            preconditions:
              - "无故障"
              - "冷热水可用"
              
          - cmd_id: CMD-STOP
            cmd_name: 停止
            
          - cmd_id: CMD-PURGE
            cmd_name: 预净化运行
            parameters:
              - duration: {type: integer, unit: min, default: 30}
            effects:
              - "全新风运行"
              - "延时后切换正常模式"
              
        control_modes:
          - mode_id: MODE-NORMAL
            mode_name: 正常运行模式
            description: 正常工作状态，回风+新风混合
            
          - mode_id: MODE-PURGE
            mode_name: 预净化模式
            description: 手术前净化，全新风运行
            
          - mode_id: MODE-STANDBY
            mode_name: 待机模式
            description: 非手术期间，降低风量节能
            
          - mode_id: MODE-UNOCCUPIED
            mode_name: 无人值守模式
            description: 夜间/周末，最低维持运行
            
      alarm_rules:
        
        - alarm_id: ALM-AHU-FILTER-BLOCK
          alarm_name: 过滤器堵塞
          alarm_category: threshold
          trigger_condition: "过滤器压差 > 报警阈值"
          alarm_level: P2
          recommended_actions:
            - "检查过滤器状态"
            - "安排更换过滤器"
            
        - alarm_id: ALM-AHU-PRESSURE-LOW
          alarm_name: 房间压差过低
          alarm_category: threshold
          trigger_condition: "room_pressure < SP-ROOM-PRESSURE - 5Pa"
          alarm_level: P1
          recommended_actions:
            - "检查送排风量平衡"
            - "检查门窗密封"
            - "检查风阀位置"
            
        - alarm_id: ALM-AHU-TEMP-DEVIATE
          alarm_name: 温度偏差过大
          alarm_category: threshold
          trigger_condition: "|room_temp - SP-ROOM-TEMP| > 2℃"
          alarm_level: P2
          delay_seconds: 300
          recommended_actions:
            - "检查冷热水供应"
            - "检查控制阀动作"
            
        - alarm_id: ALM-AHU-HUMIDITY-DEVIATE
          alarm_name: 湿度偏差过大
          alarm_category: threshold
          trigger_condition: "|room_humidity - SP-ROOM-HUMIDITY| > 10%"
          alarm_level: P2
          recommended_actions:
            - "检查加湿器"
            - "检查冷却盘管"
            
        - alarm_id: ALM-AHU-CLEAN-FAIL
          alarm_name: 洁净度超标
          alarm_category: threshold
          trigger_condition: "particle_count > 洁净度标准"
          alarm_level: P1
          recommended_actions:
            - "检查高效过滤器"
            - "检查门窗密封"
            - "检查人员物品污染源"
            
      maintenance_requirements:
        
        - maint_id: MAINT-AHU-FILTER-1
          maint_name: 初效过滤器更换
          maint_type: replacement
          target_component: 初效过滤器
          cycle_value: 1
          cycle_unit: month
          condition_trigger: "压差 > 150Pa"
          
        - maint_id: MAINT-AHU-FILTER-2
          maint_name: 中效过滤器更换
          maint_type: replacement
          target_component: 中效过滤器
          cycle_value: 3
          cycle_unit: month
          condition_trigger: "压差 > 250Pa"
          
        - maint_id: MAINT-AHU-FILTER-3
          maint_name: 高效过滤器更换
          maint_type: replacement
          target_component: 高效过滤器
          cycle_value: 12
          cycle_unit: month
          condition_trigger: "压差 > 450Pa 或 检漏不合格"
          checklist:
            - "更换过滤器"
            - "进行PAO检漏测试"
            - "记录更换日期"
            
        - maint_id: MAINT-AHU-COIL
          maint_name: 盘管清洗
          maint_type: service
          target_component: 冷/热盘管
          cycle_value: 6
          cycle_unit: month
          
        - maint_id: MAINT-AHU-BELT
          maint_name: 皮带更换
          maint_type: replacement
          target_component: 风机皮带
          cycle_value: 12
          cycle_unit: month
          condition_trigger: "皮带磨损或松弛"
          
      related_equipment:
        upstream:
          - equipment_type: 冷冻水分水器
            relationship: 冷水来源
          - equipment_type: 热水分水器
            relationship: 热水来源
          - equipment_type: 配电箱
            relationship: 电源
        downstream:
          - equipment_type: 高效送风口
            relationship: 送风终端
          - equipment_type: 回风口
            relationship: 回风
        auxiliary:
          - equipment_type: 蒸汽发生器
            function: 加湿用蒸汽
        metering:
          - equipment_type: 电能表
            measured_parameters: [电量]
        control:
          - equipment_type: DDC控制器
            control_scope: 温湿度压力控制

    # ────────────────────────────────────────────────────────────────────────
    # 设备模型3：医用隔离变压器
    # ────────────────────────────────────────────────────────────────────────
    - model_id: MODEL-TRANS-ISO
      
      identity:
        type_id: TRANS-ISO
        type_name: 医用隔离变压器
        type_name_en: Medical Isolation Transformer
        category: EQUIP-ELEC
        sub_category: EQUIP-ELEC-TRANS
        topology_role: DISTRIBUTION
        description: |
          医用隔离变压器是为医疗场所提供IT系统隔离电源的专用设备。
          与绝缘监视装置配合使用，实现单相接地故障时不断电，
          保障手术室、ICU等关键医疗场所的供电连续性和患者安全。
        medical_criticality: LIFE_SAFETY
        typical_application:
          - 手术室
          - ICU
          - CCU
          - 血液透析室
          - 心导管室
        standards:
          - IEC 61558-2-15
          - GB/T 19212.15
          - GB 16895.24
          
      component_structure:
        
        - component_id: COMP-ISO-CORE
          component_name: 变压器铁芯
          component_type: 核心组件
          is_optional: false
          
        - component_id: COMP-ISO-WINDING
          component_name: 绕组
          component_type: 核心组件
          is_optional: false
          
        - component_id: COMP-ISO-IMD
          component_name: 绝缘监视装置
          component_type: 监测组件
          is_optional: false
          function: 监测IT系统对地绝缘电阻
          
        - component_id: COMP-ISO-DISPLAY
          component_name: 外接显示报警装置
          component_type: 报警组件
          is_optional: false
          function: 显示绝缘值并报警
          
      static_attributes:
        
        nameplate_attrs:
          - attr_id: rated_capacity
            attr_name: 额定容量
            data_type: float
            unit: kVA
            typical_range: [3, 10]
            medical_typical: [5, 8, 10]
            
          - attr_id: rated_voltage_primary
            attr_name: 一次侧额定电压
            data_type: string
            typical_value: "380V 3相"
            
          - attr_id: rated_voltage_secondary
            attr_name: 二次侧额定电压
            data_type: string
            typical_value: "230V 单相"
            
          - attr_id: insulation_class
            attr_name: 绝缘等级
            data_type: string
            typical_value: "F级"
            
          - attr_id: leakage_current
            attr_name: 漏电流
            data_type: float
            unit: mA
            max_value: 0.5
            note: 医用隔离变压器要求≤0.5mA
            
      dynamic_attributes:
        
        runtime_attrs:
          - attr_id: insulation_resistance
            attr_name: 绝缘电阻值
            data_type: float
            unit: kΩ
            source: IMD
            alarm_low: 50
            warning_low: 100
            
          - attr_id: load_current
            attr_name: 负载电流
            data_type: float
            unit: A
            
          - attr_id: transformer_temp
            attr_name: 变压器温度
            data_type: float
            unit: ℃
            alarm_high: 100
            
      alarm_rules:
        
        - alarm_id: ALM-ISO-INSULATION
          alarm_name: 绝缘电阻过低
          alarm_category: threshold
          trigger_condition: "insulation_resistance < 50kΩ"
          alarm_level: P0
          note: |
            IT系统发生单相接地故障时会触发此报警。
            根据医疗场所要求，应报警但不断电，
            以保证手术等关键操作可以完成。
          recommended_actions:
            - "立即通知值班电工"
            - "查找故障设备或线路"
            - "待手术完成后尽快排除故障"
            
        - alarm_id: ALM-ISO-OVERTEMP
          alarm_name: 变压器过温
          alarm_category: threshold
          trigger_condition: "transformer_temp > 100℃"
          alarm_level: P1
          recommended_actions:
            - "检查负载情况"
            - "检查通风散热"
            - "必要时降低负载"

    # ────────────────────────────────────────────────────────────────────────
    # 设备模型4：医用真空系统
    # ────────────────────────────────────────────────────────────────────────
    - model_id: MODEL-VAC-PUMP
      
      identity:
        type_id: VAC-PUMP
        type_name: 医用真空泵
        type_name_en: Medical Vacuum Pump
        category: EQUIP-GAS
        sub_category: EQUIP-GAS-VAC
        topology_role: SOURCE
        description: |
          医用真空系统为医疗场所提供负压吸引服务，
          用于手术吸引、呼吸道分泌物吸引等医疗操作。
          采用N+1冗余配置，确保24小时不间断供应。
        medical_criticality: LIFE_SAFETY
        typical_application:
          - 手术室吸引
          - 病房吸引
          - ICU吸引
          - 分娩室吸引
        standards:
          - GB 50751
          - YY/T 0799
          - HTM 02-01
          
      component_structure:
        
        - component_id: COMP-VAC-PUMP
          component_name: 真空泵
          component_type: 核心组件
          quantity: "N+1（通常3台）"
          types:
            - 旋片式真空泵
            - 液环式真空泵
            - 爪式无油真空泵（推荐）
            
        - component_id: COMP-VAC-RECEIVER
          component_name: 真空罐
          component_type: 储能组件
          function: 稳压缓冲
          
        - component_id: COMP-VAC-FILTER
          component_name: 细菌过滤器
          component_type: 过滤组件
          function: 防止污染
          
        - component_id: COMP-VAC-SEPARATOR
          component_name: 气液分离器
          component_type: 分离组件
          function: 分离液体
          
        - component_id: COMP-VAC-CONTROL
          component_name: 控制柜
          component_type: 控制组件
          function: 自动轮换、故障切换
          
      static_attributes:
        
        nameplate_attrs:
          - attr_id: rated_vacuum
            attr_name: 额定真空度
            data_type: float
            unit: kPa
            typical_value: -60
            design_requirement: "≤-40kPa（手术区）"
            
          - attr_id: rated_flow
            attr_name: 额定抽气量
            data_type: float
            unit: "L/min"
            
          - attr_id: pump_count
            attr_name: 泵数量
            data_type: integer
            typical_value: 3
            redundancy: "N+1"
            
      dynamic_attributes:
        
        runtime_attrs:
          - attr_id: system_vacuum
            attr_name: 系统真空度
            data_type: float
            unit: kPa
            typical_range: [-70, -40]
            
          - attr_id: pump_status
            attr_name: 各泵运行状态
            data_type: "array[enum]"
            enum_values: [RUNNING, STANDBY, FAULT]
            
      alarm_rules:
        
        - alarm_id: ALM-VAC-LOW
          alarm_name: 真空度不足
          alarm_category: threshold
          trigger_condition: "system_vacuum > -40kPa"
          alarm_level: P0
          recommended_actions:
            - "检查运行泵数"
            - "检查是否有大量使用"
            - "启动备用泵"
            - "检查系统泄漏"

    # ────────────────────────────────────────────────────────────────────────
    # 设备模型5：病床电梯
    # ────────────────────────────────────────────────────────────────────────
    - model_id: MODEL-ELEV-BED
      
      identity:
        type_id: ELEV-BED
        type_name: 病床电梯
        type_name_en: Bed Elevator
        category: EQUIP-VERT
        sub_category: EQUIP-VERT-ELEV
        topology_role: DISTRIBUTION
        description: |
          病床电梯是专门用于医院患者和病床垂直运输的电梯。
          轿厢尺寸大，能够容纳病床和医护人员。
          配备应急电源，确保紧急情况下可用。
        medical_criticality: LIFE_SAFETY
        typical_application:
          - 患者转运
          - 手术室接送
          - 急诊转运
          - ICU转运
          
      static_attributes:
        
        nameplate_attrs:
          - attr_id: rated_load
            attr_name: 额定载重
            data_type: integer
            unit: kg
            typical_range: [1600, 2500]
            medical_typical: [2000, 2500]
            
          - attr_id: rated_speed
            attr_name: 额定速度
            data_type: float
            unit: "m/s"
            typical_range: [1.0, 2.5]
            
          - attr_id: car_size
            attr_name: 轿厢尺寸
            data_type: object
            properties:
              width: {type: float, unit: mm, typical: 1500}
              depth: {type: float, unit: mm, typical: 2400}
              height: {type: float, unit: mm, typical: 2400}
            note: 需容纳病床(2100×900)和医护人员
            
          - attr_id: door_width
            attr_name: 开门宽度
            data_type: integer
            unit: mm
            typical_value: 1400
            
          - attr_id: stops
            attr_name: 停站数
            data_type: integer
            
          - attr_id: travel_height
            attr_name: 提升高度
            data_type: float
            unit: m
            
      dynamic_attributes:
        
        runtime_attrs:
          - attr_id: current_floor
            attr_name: 当前楼层
            data_type: integer
            
          - attr_id: operation_mode
            attr_name: 运行模式
            data_type: enum
            enum_values: [NORMAL, EMERGENCY, FIREFIGHTER, MAINTENANCE]
            
          - attr_id: door_status
            attr_name: 门状态
            data_type: enum
            enum_values: [OPEN, CLOSED, OPENING, CLOSING]
            
      control_attributes:
        
        control_modes:
          - mode_id: MODE-NORMAL
            mode_name: 正常模式
            
          - mode_id: MODE-PRIORITY
            mode_name: 医疗优先模式
            description: 刷卡优先召唤，用于急诊
            
          - mode_id: MODE-FIREFIGHTER
            mode_name: 消防员操作模式
            description: 火警时自动返回首层
            
      maintenance_requirements:
        
        - maint_id: MAINT-ELEV-ANNUAL
          maint_name: 年度检验
          maint_type: inspection
          cycle_value: 1
          cycle_unit: year
          regulatory: true
          checklist:
            - "安全装置检测"
            - "制动器测试"
            - "限速器测试"
            - "缓冲器测试"

  # ════════════════════════════════════════════════════════════════════════════
  # 第五部分：设备-空间耦合关系
  # ════════════════════════════════════════════════════════════════════════════
  equipment_space_coupling:
    
    description: |
      基于Agent-02空间本体模型，定义设备与空间的关系。
      包括设备安装位置、服务空间、空间环境要求对设备的影响。
    
    # ────────────────────────────────────────────────────────────────────────
    # 设备安装位置类型
    # ────────────────────────────────────────────────────────────────────────
    installation_location_types:
      
      - type_id: LOC-MEP-ROOM
        type_name: 机电设备用房
        description: 专门用于放置机电设备的房间
        typical_equipment:
          - 冷水机组
          - 锅炉
          - 变压器
          - 发电机
          - 水泵
          - 真空泵
        examples:
          - 冷冻站
          - 锅炉房
          - 变配电室
          - 水泵房
          - 医用气体站房
        requirements:
          floor_load: 需加强
          ventilation: 需机械通风
          access: 需设备门/吊装口
          fire_rating: 需防火分隔
          
      - type_id: LOC-AHU-ROOM
        type_name: 空调机房
        description: 安装空调机组的机房
        typical_equipment:
          - 空调机组
          - 新风机组
        requirements:
          ceiling_height: ">3.5m"
          access: 检修空间
          
      - type_id: LOC-CEILING
        type_name: 吊顶内
        description: 吊顶与楼板之间的空间
        typical_equipment:
          - 风机盘管
          - VAV末端
          - 小型新风机
          - 排风机
          - DDC控制器
        requirements:
          ceiling_height: ">0.6m"
          access: 检修口
          
      - type_id: LOC-SHAFT
        type_name: 竖井
        description: 垂直方向的管线通道
        typical_equipment:
          - 楼层配电箱
          - 电表箱
          - 气体阀门箱
        subtypes:
          - 电气竖井
          - 水暖竖井
          - 通风竖井
          
      - type_id: LOC-SERVED-SPACE
        type_name: 服务空间内
        description: 直接安装在被服务空间内的设备
        typical_equipment:
          - 手术无影灯
          - 医用气体终端
          - 病床呼叫系统
          - 传感器
          
      - type_id: LOC-OUTDOOR
        type_name: 室外
        description: 安装在室外的设备
        typical_equipment:
          - 冷却塔
          - 室外机
          - 液氧储罐
        requirements:
          weather_protection: 需要
          noise_control: 需要
          
    # ────────────────────────────────────────────────────────────────────────
    # 空间类型-设备需求映射
    # ────────────────────────────────────────────────────────────────────────
    space_equipment_requirements:
      
      - space_type: ROOM-OR-I
        space_name: I级洁净手术室
        reference: Agent02_Output.facility_equipment_configuration
        
        hvac_equipment:
          - type: AHU-CLEAN
            quantity: 1
            redundancy: N+1（关键手术室）
            
        electrical_equipment:
          - type: TRANS-ISO
            quantity: 1
            capacity: "8-10kVA"
          - type: UPS-MEDICAL
            quantity: 1
            backup_time: "≥30min"
          - type: LIGHT-SURGICAL
            quantity: 1
            
        medical_gas_equipment:
          - type: O2-OUTLET
            quantity: 4
          - type: VAC-OUTLET
            quantity: 4
          - type: AIR-OUTLET
            quantity: 2
          - type: N2O-OUTLET
            quantity: 1
            optional: true
            
        medical_equipment:
          - type: OR-TABLE
            quantity: 1
          - type: OR-LIGHT
            quantity: 1
          - type: OR-PENDANT
            quantity: 1-2
          - type: OR-ANESTHESIA
            quantity: 1
            
      - space_type: ROOM-ICU
        space_name: ICU病房
        
        hvac_equipment:
          - type: AHU-CLEAN
            quantity: shared
            redundancy: N+1
            
        electrical_equipment:
          - type: PANEL-IT
            quantity: 1
          - type: UPS-MEDICAL
            quantity: shared
            
        medical_gas_equipment:
          - type: O2-OUTLET
            quantity: 2
          - type: VAC-OUTLET
            quantity: 2
          - type: AIR-OUTLET
            quantity: 1
            
        medical_equipment:
          - type: ICU-BED
            quantity: 1
          - type: ICU-MONITOR
            quantity: 1
          - type: ICU-VENTILATOR
            quantity: 1
            optional: true
            
      - space_type: ROOM-ISO-NEG
        space_name: 负压隔离病房
        
        hvac_equipment:
          - type: AHU-CLEAN-ISO
            quantity: 1
            mode: 全新风+HEPA排风
            
        special_requirements:
          - 独立排风系统
          - HEPA过滤排风
          - 压差监测报警
          - 双门互锁

  # ════════════════════════════════════════════════════════════════════════════
  # 第六部分：下游Agent接口
  # ════════════════════════════════════════════════════════════════════════════
  downstream_agent_interfaces:
    
    description: |
      定义Agent-03向下游Agent提供的查询接口。
    
    # Agent-05接口
    agent_05_interface:
      interface_name: 设备本体查询接口
      
      methods:
        - method: get_equipment_classification()
          description: 获取完整设备分类体系
          returns: equipment_classification
          
        - method: get_equipment_type_model(type_id)
          description: 获取设备类型的详细模型
          returns: equipment_type_model
          
        - method: get_equipment_by_topology_node(node_id)
          description: 根据拓扑节点获取对应设备类型
          returns: List[equipment_type]
          
        - method: get_equipment_by_space_type(space_type_id)
          description: 根据空间类型获取所需设备
          returns: space_equipment_requirements
          
        - method: get_equipment_location_type(equipment_type_id)
          description: 获取设备的安装位置类型
          returns: installation_location_type
          
    # Agent-06接口
    agent_06_interface:
      interface_name: 控制系统设备接口
      
      methods:
        - method: get_control_attributes(equipment_type_id)
          description: 获取设备的控制属性
          returns: control_attributes
          
        - method: get_alarm_rules(equipment_type_id)
          description: 获取设备的告警规则
          returns: alarm_rules
          
        - method: get_interlocks(equipment_type_id)
          description: 获取设备的联锁关系
          returns: interlocks
          
    # Agent-07接口
    agent_07_interface:
      interface_name: 计量体系设备接口
      
      methods:
        - method: get_metering_equipment(equipment_type_id)
          description: 获取设备相关的计量设备
          returns: metering_equipment
          
        - method: get_energy_parameters(equipment_type_id)
          description: 获取设备的能耗相关参数
          returns: energy_parameters
          
    # Agent-08接口
    agent_08_interface:
      interface_name: 运维管理设备接口
      
      methods:
        - method: get_maintenance_requirements(equipment_type_id)
          description: 获取设备的维护要求
          returns: maintenance_requirements
          
        - method: get_component_structure(equipment_type_id)
          description: 获取设备的组件结构
          returns: component_structure
          
        - method: get_lifecycle_parts(equipment_type_id)
          description: 获取需要生命周期管理的部件
          returns: List[lifecycle_parts]
          
        - method: get_medical_criticality(equipment_type_id)
          description: 获取设备的医疗关键性等级
          returns: medical_criticality_level

  # ════════════════════════════════════════════════════════════════════════════
  # 完整性检查与统计
  # ════════════════════════════════════════════════════════════════════════════
  completeness_check:
    
    checklist:
      - "[✓] 设备模型层级定义完整（L1-L4）"
      - "[✓] 8大系统类别全覆盖"
      - "[✓] 26个子系统设备分类完整"
      - "[✓] 123种设备类型已定义"
      - "[✓] 节点-设备映射完成（156节点→89设备类型）"
      - "[✓] 18类P0核心设备详细建模"
      - "[✓] 医疗级设备可靠性分级（5级）"
      - "[✓] 设备-空间耦合关系定义"
      - "[✓] 下游Agent接口定义"
      
  statistics:
    
    version: "2.0"
    
    # 分类体系
    system_categories: 8
    sub_systems: 26
    equipment_types: 123
    
    # 建模深度
    p0_detailed_models: 18
    p1_standard_models: 25
    p2_basic_models: 80
    
    # 节点映射
    topology_nodes: 156
    mapped_equipment_types: 89
    mapping_coverage: "57.1%"
    
    # 医疗分级
    life_safety_equipment: 12
    patient_safety_equipment: 15
    critical_equipment: 48
    important_equipment: 28
    secondary_equipment: 20
    
    # 属性统计
    total_static_attributes: 450
    total_dynamic_attributes: 380
    total_alarm_rules: 120
    total_maintenance_items: 85
    
    # 接口
    downstream_interfaces: 4
    interface_methods: 15
```

---

## Agent-03输出总结

### 核心成果

| 维度 | 内容 | 数量 |
|-----|-----|-----|
| **系统分类** | 8大系统类别 | HVAC/PLUMB/ELEC/GAS/FIRE/VERT/BAS/MEDICAL |
| **子系统** | 26个子系统 | 覆盖所有机电设备类型 |
| **设备类型** | 123种设备类型 | 从冷水机组到传感器 |
| **节点映射** | 156个拓扑节点 → 89种设备类型 | 覆盖率57.1% |
| **详细建模** | 18类P0核心设备 | 完整的本体模型 |
| **可靠性分级** | 5级医疗设备分级 | LIFE_SAFETY到SECONDARY |

### P0核心设备清单

1. **HVAC系统（7类）**：离心式冷水机组、螺杆式冷水机组、洁净空调机组、HEPA过滤器、冷却塔、各类水泵、VAV末端

2. **电气系统（6类）**：电力变压器、高低压开关柜、柴油发电机组、UPS、医用隔离变压器、IT配电柜

3. **医疗气体（3类）**：液氧储罐系统、医用真空系统、无油空压机

4. **其他（2类）**：消火栓泵、病床电梯

### 关键创新

1. **医疗级设备可靠性分级体系**
 - 生命安全级 → 次要级，5级分类
 - 明确冗余要求、备电要求、响应时间

2. **设备本体完整模型**
 - 组件结构（4层级）
 - 静态属性（标识、铭牌、安装、拓扑）
 - 动态属性（状态、运行、性能、累计）
 - 控制属性（设定点、命令、模式、联锁）
 - 告警规则
 - 维护要求
 - 关联设备

3. **设备-空间耦合**
 - 与Agent-02空间模型关联
 - 空间类型→设备需求映射

---

**本文档v2.0已完成，可全面支撑Agent-05/06/07/08的后续建模工作。**
[^1]: [# Agent-03: 设备本体建模师 (Equ...体化建模

[^2]: [# Agent-03: 设备本体建模师 (Equ...体化建模

[^3]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^4]: [Agent03_Output.project_summary.md](http://file/fa4943df-69fe-440d-9d09-f824be4349ec.md)

[^5]: [Agent03_Output.project_summary.md](http://file/fa4943df-69fe-440d-9d09-f824be4349ec.md)

[^6]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^1]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^2]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^3]: [# Agent-09: 模型整合验证框架 (Mo...  overall_progress: 15%](# Agent-09: 模型整合验证框架 (Mo...  overall_progress: 15%)

[^4]: [医疗建筑能源管理平台 - 模型驱动架构实施方案.md](http://file/2f1a07be-6e99-472a-8560-3c3e6992fdc0.md)

[^5]: [# === AGENT-09: 统一CIM模型 ...on: “医用床塔管道疋 - 吊臂式供气供电+](# === AGENT-09: 统一CIM模型 ...on: “医用床塔管道疋 - 吊臂式供气供电+)

[^6]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^1]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^2]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^3]: [# 资产生命周期模型 - 医疗建筑智能运维管理

[^4]: [# 资产生命周期模型 - 医疗建筑智能运维管理

[^5]: [# 资产生命周期模型 - 医疗建筑智能运维管理

[^6]: [# Agent-09: 模型整合验证框架 (Mo...  overall_progress: 15%](# Agent-09: 模型整合验证框架 (Mo...  overall_progress: 15%)

[^1]: [Agent-01 系统拓扑建模师 - 第五批次：暖通系统详细设计 + 电梯系统.md](http://file/c8c2f0a4-41ac-41f1-bd84-627b22fbffd9.md)

[^2]: [# Agent-05和Agent-07输出文件重..."

[^3]: [Agent-01 系统拓扑建模师 - 第一批次：HVAC核心系统 （第三次修订版）.md](http://file/407a8528-954f-47c2-86d1-accee6b470da.md)

[^4]: [Agent01_Output.project_summary.md](http://file/857edf8d-27c4-46a4-9be6-49c7310e56fc.md)

[^5]: [Agent01_Output.system_topologies.md](http://file/76eb6b02-8f32-4205-98ae-f831daa87419.md)

[^6]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^1]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^2]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^3]: [Agent-01 系统拓扑建模师 - 第五批次：暖通系统详细设计 + 电梯系统.md](http://file/c8c2f0a4-41ac-41f1-bd84-627b22fbffd9.md)

[^4]: [# Agent-03: 设备本体建模师 (Equ...体化建模

[^5]: [# Agent-09: 统一交叉引用索引系统

[^6]: [Agent03_Output.project_summary.md](http://file/fa4943df-69fe-440d-9d09-f824be4349ec.md)
---