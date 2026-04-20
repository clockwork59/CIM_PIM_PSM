# Agent-01 第二批次完整输出

## 声明

本输出严格遵循Agent-01系统拓扑建模师Prompt v2.0规范，覆盖ELECTRICAL（电气系统）和MEDICAL_GAS（医疗气体系统）的完整拓扑建模。

---

## 第一部分：系统目录补充 (System Catalog - Batch 2)

```yaml
System_Catalog:

  - category_id: ELECTRICAL
    category_name: 电气系统
    category_name_en: Electrical Systems
    description: 提供建筑电力供应、配电、照明、应急电源等功能的系统集合
  
    systems:
      - system_id: ELEC-HV
        system_name: 高压配电系统
        system_name_en: High Voltage Distribution System
        primary_medium: ELEC-HV
        secondary_medium: [CTRL-SCADA]
        description: 10kV高压进线、高压开关柜、变压器一次侧
        priority: P1-CRITICAL
      
      - system_id: ELEC-LV-MAIN
        system_name: 低压主配电系统
        system_name_en: Low Voltage Main Distribution System
        primary_medium: ELEC-LV
        secondary_medium: [CTRL-BA]
        description: 变压器二次侧、低压主配电柜、母联、馈电回路
        priority: P1-CRITICAL
      
      - system_id: ELEC-LV-NORMAL
        system_name: 普通动力配电系统
        system_name_en: Normal Power Distribution System
        primary_medium: ELEC-LV
        description: 普通用电设备的楼层配电、终端配电
        priority: P2-IMPORTANT
      
      - system_id: ELEC-LV-CRITICAL
        system_name: 重要负荷配电系统
        system_name_en: Critical Power Distribution System
        primary_medium: ELEC-LV
        description: 手术室、ICU、急诊等重要医疗区域配电
        priority: P1-CRITICAL
      
      - system_id: ELEC-EPS
        system_name: 应急电源系统
        system_name_en: Emergency Power Supply System
        primary_medium: ELEC-EPS
        secondary_medium: [FUEL-DIESEL]
        description: 柴油发电机组及应急配电系统
        priority: P1-CRITICAL
      
      - system_id: ELEC-UPS
        system_name: 不间断电源系统
        system_name_en: Uninterruptible Power Supply System
        primary_medium: ELEC-UPS
        description: UPS及其配电系统，为IT设备、医疗设备提供不间断电源
        priority: P1-CRITICAL
      
      - system_id: ELEC-IT
        system_name: 隔离电源系统
        system_name_en: Isolated Power System
        primary_medium: ELEC-IT
        description: 手术室、ICU专用隔离电源系统（IT系统）
        priority: P1-CRITICAL
      
      - system_id: ELEC-LIGHT
        system_name: 照明系统
        system_name_en: Lighting System
        primary_medium: ELEC-LV
        description: 普通照明、应急照明、疏散指示
        priority: P2-IMPORTANT
      
      - system_id: ELEC-GROUND
        system_name: 接地系统
        system_name_en: Grounding System
        primary_medium: GROUND
        description: 防雷接地、保护接地、医疗设备等电位接地
        priority: P1-CRITICAL

    system_dependencies:
      - upstream: ELEC-HV
        downstream: ELEC-LV-MAIN
        interface_medium: ELEC-HV/ELEC-LV
        interface_equipment: 变压器
      
      - upstream: ELEC-LV-MAIN
        downstream: ELEC-LV-NORMAL
        interface_medium: ELEC-LV
      
      - upstream: ELEC-LV-MAIN
        downstream: ELEC-LV-CRITICAL
        interface_medium: ELEC-LV
      
      - upstream: ELEC-EPS
        downstream: ELEC-LV-MAIN
        interface_medium: ELEC-EPS
        interface_equipment: ATS自动转换开关
      
      - upstream: ELEC-LV-CRITICAL
        downstream: ELEC-UPS
        interface_medium: ELEC-LV
      
      - upstream: ELEC-LV-CRITICAL
        downstream: ELEC-IT
        interface_medium: ELEC-LV
        interface_equipment: 隔离变压器

  - category_id: MEDICAL_GAS
    category_name: 医疗气体系统
    category_name_en: Medical Gas Systems
    description: 提供医疗用气体（氧气、压缩空气、负压吸引、笑气等）的供应系统
  
    systems:
      - system_id: MGAS-O2
        system_name: 医用氧气系统
        system_name_en: Medical Oxygen System
        primary_medium: GAS-O2
        description: 液氧储罐/汇流排、减压、管网输送至终端
        priority: P1-CRITICAL
      
      - system_id: MGAS-VAC
        system_name: 医用负压吸引系统
        system_name_en: Medical Vacuum System
        primary_medium: GAS-VAC
        description: 真空泵站、负压管网至终端
        priority: P1-CRITICAL
      
      - system_id: MGAS-AIR
        system_name: 医用压缩空气系统
        system_name_en: Medical Compressed Air System
        primary_medium: GAS-AIR
        description: 空压机、干燥净化、管网至终端
        priority: P1-CRITICAL
      
      - system_id: MGAS-N2O
        system_name: 笑气系统
        system_name_en: Nitrous Oxide System
        primary_medium: GAS-N2O
        description: N2O汇流排、管网至手术室
        priority: P2-IMPORTANT
      
      - system_id: MGAS-N2
        system_name: 医用氮气系统
        system_name_en: Medical Nitrogen System
        primary_medium: GAS-N2
        description: 氮气汇流排/制氮机、管网至终端
        priority: P2-IMPORTANT
      
      - system_id: MGAS-CO2
        system_name: 医用二氧化碳系统
        system_name_en: Medical Carbon Dioxide System
        primary_medium: GAS-CO2
        description: CO2汇流排、管网至手术室（腹腔镜用）
        priority: P2-IMPORTANT
      
      - system_id: MGAS-AGSS
        system_name: 麻醉废气排放系统
        system_name_en: Anesthetic Gas Scavenging System
        primary_medium: GAS-AGSS
        description: 麻醉废气收集、输送、排放系统
        priority: P1-CRITICAL

    system_dependencies:
      - upstream: ELEC-LV-CRITICAL
        downstream: MGAS-O2
        interface_medium: ELEC-LV
        description: 液氧储罐电加热、报警系统供电
      
      - upstream: ELEC-LV-CRITICAL
        downstream: MGAS-VAC
        interface_medium: ELEC-LV
        description: 真空泵供电
      
      - upstream: ELEC-LV-CRITICAL
        downstream: MGAS-AIR
        interface_medium: ELEC-LV
        description: 空压机供电
```

---

## 第二部分：介质类型定义补充 (Medium Types - Batch 2)

```yaml
Medium_Types:

  # 电力介质
  Electrical_Media:
    - medium_id: ELEC-HV
      medium_name: 高压电
      medium_name_en: High Voltage
      category: ELECTRICAL
      typical_properties:
        voltage: {value: 10, unit: kV}
        frequency: {value: 50, unit: Hz}
        phases: 3
      
    - medium_id: ELEC-LV
      medium_name: 低压动力电
      medium_name_en: Low Voltage Power
      category: ELECTRICAL
      typical_properties:
        voltage: {value: 380/220, unit: V}
        frequency: {value: 50, unit: Hz}
        phases: "3P+N+PE"
      
    - medium_id: ELEC-EPS
      medium_name: 应急电源
      medium_name_en: Emergency Power Supply
      category: ELECTRICAL
      typical_properties:
        voltage: {value: 380/220, unit: V}
        source: 柴油发电机
        startup_time: {value: "≤15", unit: s}
      
    - medium_id: ELEC-UPS
      medium_name: 不间断电源
      medium_name_en: Uninterruptible Power Supply
      category: ELECTRICAL
      typical_properties:
        voltage: {value: 380/220, unit: V}
        backup_time: {value: 15-30, unit: min}
        transfer_time: {value: 0, unit: ms}
      
    - medium_id: ELEC-IT
      medium_name: 隔离电源
      medium_name_en: Isolated Power (IT System)
      category: ELECTRICAL
      typical_properties:
        voltage: {value: 220, unit: V}
        grounding: 不接地系统
        insulation_monitor: 必需
      
    - medium_id: GROUND
      medium_name: 接地
      medium_name_en: Grounding
      category: ELECTRICAL
      typical_properties:
        resistance: {value: "≤1", unit: Ω}

  # 医疗气体介质
  Medical_Gas_Media:
    - medium_id: GAS-O2
      medium_name: 医用氧气
      medium_name_en: Medical Oxygen
      category: MEDICAL_GAS
      typical_properties:
        purity: {value: "≥99.5", unit: "%"}
        pressure_source: {value: 0.8-1.0, unit: MPa}
        pressure_terminal: {value: 0.4-0.5, unit: MPa}
        color_code: 白色
      
    - medium_id: GAS-VAC
      medium_name: 医用负压
      medium_name_en: Medical Vacuum
      category: MEDICAL_GAS
      typical_properties:
        pressure: {value: -40 ~ -60, unit: kPa}
        flow_per_terminal: {value: 40, unit: L/min}
        color_code: 黄色
      
    - medium_id: GAS-AIR
      medium_name: 医用压缩空气
      medium_name_en: Medical Compressed Air
      category: MEDICAL_GAS
      typical_properties:
        pressure_source: {value: 0.7-0.8, unit: MPa}
        pressure_terminal: {value: 0.4-0.5, unit: MPa}
        dew_point: {value: "≤-40", unit: ℃}
        oil_content: {value: "≤0.1", unit: "mg/m³"}
        color_code: 黑白相间
      
    - medium_id: GAS-N2O
      medium_name: 笑气
      medium_name_en: Nitrous Oxide
      category: MEDICAL_GAS
      typical_properties:
        purity: {value: "≥99", unit: "%"}
        pressure_terminal: {value: 0.4-0.5, unit: MPa}
        color_code: 蓝色
      
    - medium_id: GAS-N2
      medium_name: 医用氮气
      medium_name_en: Medical Nitrogen
      category: MEDICAL_GAS
      typical_properties:
        purity: {value: "≥99.5", unit: "%"}
        pressure_terminal: {value: 0.4-0.8, unit: MPa}
        color_code: 黑色
      
    - medium_id: GAS-CO2
      medium_name: 医用二氧化碳
      medium_name_en: Medical Carbon Dioxide
      category: MEDICAL_GAS
      typical_properties:
        purity: {value: "≥99.5", unit: "%"}
        pressure_terminal: {value: 0.4-0.5, unit: MPa}
        color_code: 灰色
      
    - medium_id: GAS-AGSS
      medium_name: 麻醉废气
      medium_name_en: Anesthetic Gas Scavenging
      category: MEDICAL_GAS
      typical_properties:
        pressure: {value: -25 ~ -50, unit: mmH2O}
        flow_per_terminal: {value: 50, unit: L/min}
```

---

## 第三部分：ELEC-HV 高压配电系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: ELEC-HV
    system_name: 高压配电系统
    system_name_en: High Voltage Distribution System
    category: ELECTRICAL
    version: 1.0
  
    description: |
      医院10kV高压配电系统，负责从市政电网引入高压电源，
      经高压开关柜分配至各变压器，为全院提供电力供应基础。
      采用双路电源供电，确保供电可靠性。
    
    design_basis:
      voltage_level: {value: 10, unit: kV}
      supply_mode: 双路独立电源
      main_connection: 单母线分段
      total_capacity: {value: 10000-20000, unit: kVA}
    
    serving_scope:
      - ELEC-LV-MAIN (低压主配电)

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: ELEC-HV_BND_IN_GRID1
        boundary_name: 市电一路
        medium: ELEC-HV
        is_external: true
        source: 市政电网变电站A
        parameters:
          voltage: {value: 10, unit: kV}
          capacity: {value: 10000, unit: kVA}
        
      - boundary_id: ELEC-HV_BND_IN_GRID2
        boundary_name: 市电二路
        medium: ELEC-HV
        is_external: true
        source: 市政电网变电站B
        parameters:
          voltage: {value: 10, unit: kV}
          capacity: {value: 10000, unit: kVA}
        
    outputs:
      - boundary_id: ELEC-HV_BND_OUT_TRANS
        boundary_name: 变压器高压侧
        medium: ELEC-HV
        target_system: ELEC-LV-MAIN
        interface_point: 变压器一次侧

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:

    source_nodes:
  
      - node_id: ELEC-HV_SRC_GRID1
        node_name: 市电进线1
        node_name_en: Utility Power Incoming Line 1
        node_type: Source_Node
        node_category: SRC
      
        function: 一路市电引入
        medium_out: ELEC-HV
        is_external: true
      
        equipment_parameters:
          voltage: {value: 10, unit: kV}
          cable_type: YJV22-3×240
        
        location_hint:
          space_type: UNDERGROUND
          position: 高压电缆沟/直埋
          entry_point: 变电所高压室
        
      - node_id: ELEC-HV_SRC_GRID2
        node_name: 市电进线2
        node_name_en: Utility Power Incoming Line 2
        node_type: Source_Node
        node_category: SRC
      
        function: 二路市电引入
        medium_out: ELEC-HV
        is_external: true
      
        equipment_parameters:
          voltage: {value: 10, unit: kV}
          cable_type: YJV22-3×240
          path_requirement: 与一路不同路由
        
        location_hint:
          space_type: UNDERGROUND
          position: 高压电缆沟/直埋（独立路由）
          entry_point: 变电所高压室

    distribution_nodes:
  
      - node_id: ELEC-HV_DST_INCB1
        node_name: 高压进线柜1
        node_name_en: HV Incoming Panel 1
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 一路电源接入、保护、计量
        medium_in: ELEC-HV
        medium_out: ELEC-HV
      
        equipment_parameters:
          type: 高压开关柜
          rated_voltage: {value: 12, unit: kV}
          rated_current: {value: 1250, unit: A}
          breaking_capacity: {value: 31.5, unit: kA}
          switch_type: 真空断路器
          metering: CT/PT计量
          protection: [过流, 速断, 零序]
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 高压配电室
          position: 进线端
        
        installation_requirements:
          - 防火分隔
          - 通风散热
          - 安全距离
          - 接地系统
          - 防误闭锁
        
        control_points:
          sensors:
            - {point_id: HV_V_L1, type: AI, description: A相电压}
            - {point_id: HV_V_L2, type: AI, description: B相电压}
            - {point_id: HV_V_L3, type: AI, description: C相电压}
            - {point_id: HV_I_L1, type: AI, description: A相电流}
            - {point_id: HV_I_L2, type: AI, description: B相电流}
            - {point_id: HV_I_L3, type: AI, description: C相电流}
            - {point_id: HV_P, type: AI, description: 有功功率}
            - {point_id: HV_Q, type: AI, description: 无功功率}
          status:
            - {point_id: CB_STATUS, type: DI, description: 断路器状态}
            - {point_id: CB_TRIP, type: DI, description: 保护跳闸}
          commands:
            - {point_id: CB_CTRL, type: DO, description: 断路器控制}

      - node_id: ELEC-HV_DST_INCB2
        node_name: 高压进线柜2
        node_name_en: HV Incoming Panel 2
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 二路电源接入、保护、计量
        medium_in: ELEC-HV
        medium_out: ELEC-HV
      
        equipment_parameters:
          type: 高压开关柜
          rated_voltage: {value: 12, unit: kV}
          rated_current: {value: 1250, unit: A}
          breaking_capacity: {value: 31.5, unit: kA}
          switch_type: 真空断路器
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 高压配电室

      - node_id: ELEC-HV_DST_BUS1
        node_name: 高压母线段I
        node_name_en: HV Bus Section I
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 高压配电汇流分配（I段）
        medium_in: ELEC-HV
        medium_out: ELEC-HV
      
        equipment_parameters:
          type: 封闭母线
          rated_voltage: {value: 12, unit: kV}
          rated_current: {value: 1250, unit: A}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 高压配电室

      - node_id: ELEC-HV_DST_BUS2
        node_name: 高压母线段II
        node_name_en: HV Bus Section II
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 高压配电汇流分配（II段）
        medium_in: ELEC-HV
        medium_out: ELEC-HV
      
        equipment_parameters:
          type: 封闭母线
          rated_voltage: {value: 12, unit: kV}
          rated_current: {value: 1250, unit: A}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 高压配电室

      - node_id: ELEC-HV_DST_TIE
        node_name: 母联柜
        node_name_en: Bus Tie Panel
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 两段母线联络，实现电源互备
        medium_in: ELEC-HV
        medium_out: ELEC-HV
      
        equipment_parameters:
          type: 高压开关柜
          rated_voltage: {value: 12, unit: kV}
          rated_current: {value: 1250, unit: A}
          switch_type: 真空断路器
          operation_mode: 手动/自动
          interlock: 与两路进线互锁
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 高压配电室
          position: I段与II段母线之间
        
        control_points:
          sensors:
            - {point_id: TIE_I, type: AI, description: 母联电流}
          status:
            - {point_id: TIE_CB_STATUS, type: DI, description: 母联开关状态}
          commands:
            - {point_id: TIE_CB_CTRL, type: DO, description: 母联开关控制}

      - node_id: ELEC-HV_DST_FEEDER
        node_name: 高压馈线柜
        node_name_en: HV Feeder Panel
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 向变压器馈电
        medium_in: ELEC-HV
        medium_out: ELEC-HV
      
        multiplicity: multiple
        instance_pattern: ELEC-HV_DST_FEEDER_{NN}
      
        typical_configuration:
          quantity: 6-10
        
        equipment_parameters:
          type: 高压开关柜
          rated_voltage: {value: 12, unit: kV}
          rated_current: {value: 630, unit: A}
          switch_type: 真空断路器/负荷开关
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 高压配电室

    sink_nodes:
  
      - node_id: ELEC-HV_SNK_TRANS
        node_name: 变压器高压侧
        node_name_en: Transformer HV Side
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 电压变换
        medium_in: ELEC-HV
      
        interface_system: ELEC-LV-MAIN
      
        multiplicity: multiple
        instance_pattern: ELEC-HV_SNK_TRANS_{NN}
      
        typical_configuration:
          quantity: 4-6
          capacity_each: {value: 1600-2500, unit: kVA}
        
        equipment_parameters:
          type: 干式变压器/油浸变压器
          ratio: "10/0.4kV"
          connection: Dyn11
          impedance: {value: 6, unit: "%"}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 变压器室

  # ============================================================
  # 边定义
  # ============================================================
  edges:

    supply_edges:
  
      - edge_id: ELEC-HV_EDGE_001
        edge_name: 市电1至进线柜1
        edge_type: TRK
        from_node: ELEC-HV_SRC_GRID1
        to_node: ELEC-HV_DST_INCB1
        direction: unidirectional
        medium: ELEC-HV
        medium_properties:
          voltage: {value: 10, unit: kV}
        physical_properties:
          cable_type: YJV22-3×240
        
      - edge_id: ELEC-HV_EDGE_002
        edge_name: 市电2至进线柜2
        edge_type: TRK
        from_node: ELEC-HV_SRC_GRID2
        to_node: ELEC-HV_DST_INCB2
        direction: unidirectional
        medium: ELEC-HV
        physical_properties:
          cable_type: YJV22-3×240
        
      - edge_id: ELEC-HV_EDGE_003
        edge_name: 进线柜1至母线I段
        edge_type: TRK
        from_node: ELEC-HV_DST_INCB1
        to_node: ELEC-HV_DST_BUS1
        direction: unidirectional
        medium: ELEC-HV
      
      - edge_id: ELEC-HV_EDGE_004
        edge_name: 进线柜2至母线II段
        edge_type: TRK
        from_node: ELEC-HV_DST_INCB2
        to_node: ELEC-HV_DST_BUS2
        direction: unidirectional
        medium: ELEC-HV
      
      - edge_id: ELEC-HV_EDGE_005
        edge_name: 母线I段至母联柜
        edge_type: TRK
        from_node: ELEC-HV_DST_BUS1
        to_node: ELEC-HV_DST_TIE
        direction: bidirectional
        medium: ELEC-HV
      
      - edge_id: ELEC-HV_EDGE_006
        edge_name: 母联柜至母线II段
        edge_type: TRK
        from_node: ELEC-HV_DST_TIE
        to_node: ELEC-HV_DST_BUS2
        direction: bidirectional
        medium: ELEC-HV
      
      - edge_id: ELEC-HV_EDGE_007
        edge_name: 母线I段至馈线柜
        edge_type: BRH
        from_node: ELEC-HV_DST_BUS1
        to_node: ELEC-HV_DST_FEEDER
        direction: unidirectional
        medium: ELEC-HV
      
      - edge_id: ELEC-HV_EDGE_008
        edge_name: 母线II段至馈线柜
        edge_type: BRH
        from_node: ELEC-HV_DST_BUS2
        to_node: ELEC-HV_DST_FEEDER
        direction: unidirectional
        medium: ELEC-HV
      
      - edge_id: ELEC-HV_EDGE_009
        edge_name: 馈线柜至变压器
        edge_type: TRM
        from_node: ELEC-HV_DST_FEEDER
        to_node: ELEC-HV_SNK_TRANS
        direction: unidirectional
        medium: ELEC-HV
        physical_properties:
          cable_type: YJV22-3×120

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:

    - path_id: ELEC-HV_PATH_MAIN1
      path_name: 一路电源供电路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: ELEC-HV_SRC_GRID1}
        - {step: 2, element_type: edge, element_id: ELEC-HV_EDGE_001}
        - {step: 3, element_type: node, element_id: ELEC-HV_DST_INCB1}
        - {step: 4, element_type: edge, element_id: ELEC-HV_EDGE_003}
        - {step: 5, element_type: node, element_id: ELEC-HV_DST_BUS1}
        - {step: 6, element_type: edge, element_id: ELEC-HV_EDGE_007}
        - {step: 7, element_type: node, element_id: ELEC-HV_DST_FEEDER}
        - {step: 8, element_type: edge, element_id: ELEC-HV_EDGE_009}
        - {step: 9, element_type: node, element_id: ELEC-HV_SNK_TRANS}
      
    - path_id: ELEC-HV_PATH_MAIN2
      path_name: 二路电源供电路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: ELEC-HV_SRC_GRID2}
        - {step: 2, element_type: edge, element_id: ELEC-HV_EDGE_002}
        - {step: 3, element_type: node, element_id: ELEC-HV_DST_INCB2}
        - {step: 4, element_type: edge, element_id: ELEC-HV_EDGE_004}
        - {step: 5, element_type: node, element_id: ELEC-HV_DST_BUS2}
        - {step: 6, element_type: edge, element_id: ELEC-HV_EDGE_008}
        - {step: 7, element_type: node, element_id: ELEC-HV_DST_FEEDER}
        - {step: 8, element_type: edge, element_id: ELEC-HV_EDGE_009}
        - {step: 9, element_type: node, element_id: ELEC-HV_SNK_TRANS}
      
    - path_id: ELEC-HV_PATH_BACKUP
      path_name: 母联备用路径
      path_type: BKP
      description: 一路失电时，通过母联向另一段母线供电
      sequence:
        - {step: 1, element_type: node, element_id: ELEC-HV_DST_BUS1}
        - {step: 2, element_type: edge, element_id: ELEC-HV_EDGE_005}
        - {step: 3, element_type: node, element_id: ELEC-HV_DST_TIE}
        - {step: 4, element_type: edge, element_id: ELEC-HV_EDGE_006}
        - {step: 5, element_type: node, element_id: ELEC-HV_DST_BUS2}

  # ============================================================
  # 回路定义
  # ============================================================
  loops:

    - loop_id: ELEC-HV_LOOP_RING
      loop_name: 高压环网
      loop_name_en: HV Ring Network
      loop_type: open_ring
    
      description: |
        双路电源+母联形成开环运行的环网结构。
        正常运行时母联断开，两路电源分列运行；
        一路故障时母联合闸，由另一路供电。
      
      normal_operation:
        mode: 分列运行
        tie_status: 断开
      
      fault_operation:
        mode: 母联合闸
        auto_transfer: true
        transfer_time: {value: "<3", unit: s}

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:

    protection_scheme:
      - protection: 过流保护
        setting: 1.2-1.5倍额定电流
        delay: 0.5-1s
      
      - protection: 速断保护
        setting: 6-8倍额定电流
        delay: 瞬时
      
      - protection: 零序保护
        setting: 10-30A
        delay: 0.3-0.5s
      
    auto_transfer:
      - scenario: 一路失电
        action: 母联自动合闸
        condition: 另一路正常
        delay: {value: 1-3, unit: s}
      
      - scenario: 一路恢复
        action: 母联分闸，恢复分列
        delay: {value: 30, unit: s}
```

---

## 第四部分：ELEC-LV-MAIN 低压主配电系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: ELEC-LV-MAIN
    system_name: 低压主配电系统
    system_name_en: Low Voltage Main Distribution System
    category: ELECTRICAL
    version: 1.0
  
    description: |
      医院低压主配电系统，包含变压器二次侧、低压配电柜、母联、
      各类馈电回路（普通动力、重要负荷、消防负荷等）。
      采用单母线分段接线，具备应急电源接入能力。
    
    design_basis:
      voltage_level: {value: "380/220", unit: V}
      main_connection: 单母线分段
      total_capacity: {value: 10000-20000, unit: kVA}
    
    serving_scope:
      - ELEC-LV-NORMAL (普通动力)
      - ELEC-LV-CRITICAL (重要负荷)
      - ELEC-EPS (应急电源接入)
      - ELEC-UPS (UPS供电)
      - HVAC系统动力
      - 电梯动力
      - 消防负荷

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: ELEC-LV_BND_IN_TRANS
        boundary_name: 变压器低压侧
        medium: ELEC-LV
        source_system: ELEC-HV
        interface_point: 变压器二次侧
      
      - boundary_id: ELEC-LV_BND_IN_EPS
        boundary_name: 应急电源输入
        medium: ELEC-EPS
        source_system: ELEC-EPS
        interface_point: ATS开关
      
    outputs:
      - boundary_id: ELEC-LV_BND_OUT_NORMAL
        boundary_name: 普通负荷馈电
        medium: ELEC-LV
        target_system: ELEC-LV-NORMAL
      
      - boundary_id: ELEC-LV_BND_OUT_CRITICAL
        boundary_name: 重要负荷馈电
        medium: ELEC-LV
        target_system: ELEC-LV-CRITICAL
      
      - boundary_id: ELEC-LV_BND_OUT_FIRE
        boundary_name: 消防负荷馈电
        medium: ELEC-LV
        target_system: ELEC-FIRE

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:

    source_nodes:
  
      - node_id: ELEC-LV_SRC_TRANS
        node_name: 变压器低压侧
        node_name_en: Transformer LV Side
        node_type: Source_Node
        node_category: SRC
      
        function: 提供低压电源
        medium_out: ELEC-LV
      
        multiplicity: multiple
        instance_pattern: ELEC-LV_SRC_TRANS_{NN}
      
        typical_configuration:
          quantity: 4-6
          capacity_each: {value: 1600-2500, unit: kVA}
        
        equipment_parameters:
          type: 干式变压器
          ratio: "10/0.4kV"
          connection: Dyn11
          cooling: AN/AF
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 变压器室
        
        installation_requirements:
          - 通风散热
          - 温度监测
          - 防火隔离
          - 检修通道
        
        control_points:
          sensors:
            - {point_id: TRANS_TEMP_A, type: AI, description: A相绕组温度}
            - {point_id: TRANS_TEMP_B, type: AI, description: B相绕组温度}
            - {point_id: TRANS_TEMP_C, type: AI, description: C相绕组温度}
          status:
            - {point_id: TRANS_TEMP_ALARM, type: DI, description: 超温报警}
            - {point_id: TRANS_FAN_RUN, type: DI, description: 风机运行}

      - node_id: ELEC-LV_SRC_EPS
        node_name: 应急电源输入
        node_name_en: Emergency Power Input
        node_type: Source_Node
        node_category: SRC
      
        function: 市电故障时提供应急电源
        medium_out: ELEC-EPS
      
        interface_system: ELEC-EPS
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室

    distribution_nodes:
  
      - node_id: ELEC-LV_DST_INCB
        node_name: 低压进线柜
        node_name_en: LV Incoming Panel
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 变压器出线接入、主断路器
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        multiplicity: multiple
        instance_pattern: ELEC-LV_DST_INCB_{NN}
      
        typical_configuration:
          quantity: 与变压器数量对应
        
        equipment_parameters:
          type: 低压开关柜 (GGD/GCS/GCK)
          rated_voltage: {value: 400, unit: V}
          rated_current: {value: 3200-4000, unit: A}
          breaking_capacity: {value: 65-80, unit: kA}
          switch_type: 万能式断路器
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室
        
        control_points:
          sensors:
            - {point_id: LV_V_AB, type: AI, description: AB线电压}
            - {point_id: LV_V_BC, type: AI, description: BC线电压}
            - {point_id: LV_V_CA, type: AI, description: CA线电压}
            - {point_id: LV_I_A, type: AI, description: A相电流}
            - {point_id: LV_I_B, type: AI, description: B相电流}
            - {point_id: LV_I_C, type: AI, description: C相电流}
            - {point_id: LV_P, type: AI, description: 有功功率}
            - {point_id: LV_Q, type: AI, description: 无功功率}
            - {point_id: LV_PF, type: AI, description: 功率因数}
          status:
            - {point_id: INCB_CB_STATUS, type: DI, description: 主断路器状态}
            - {point_id: INCB_TRIP, type: DI, description: 跳闸信号}

      - node_id: ELEC-LV_DST_BUS1
        node_name: 低压母线段I
        node_name_en: LV Bus Section I
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 低压配电汇流分配（I段）
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        equipment_parameters:
          type: 封闭母线/母排
          rated_voltage: {value: 400, unit: V}
          rated_current: {value: 4000, unit: A}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室

      - node_id: ELEC-LV_DST_BUS2
        node_name: 低压母线段II
        node_name_en: LV Bus Section II
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 低压配电汇流分配（II段）
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        equipment_parameters:
          type: 封闭母线/母排
          rated_voltage: {value: 400, unit: V}
          rated_current: {value: 4000, unit: A}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室

      - node_id: ELEC-LV_DST_TIE
        node_name: 低压母联柜
        node_name_en: LV Bus Tie Panel
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 两段母线联络
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        equipment_parameters:
          type: 低压开关柜
          rated_current: {value: 3200, unit: A}
          switch_type: 万能式断路器
          operation_mode: 手动/自动
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室

      - node_id: ELEC-LV_DST_ATS
        node_name: ATS自动转换开关
        node_name_en: Automatic Transfer Switch
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 市电/应急电源自动切换
        medium_in: [ELEC-LV, ELEC-EPS]
        medium_out: ELEC-LV
      
        multiplicity: multiple
        instance_pattern: ELEC-LV_DST_ATS_{NN}
      
        typical_configuration:
          quantity: 2-4（按负荷等级分类）
          types:
            - {id: ATS_CRITICAL, name: 重要负荷ATS, transfer_time: "<15s"}
            - {id: ATS_FIRE, name: 消防负荷ATS, transfer_time: "<15s"}
          
        equipment_parameters:
          type: 双电源自动转换开关
          rated_current: {value: 800-1600, unit: A}
          transfer_time: {value: "<15", unit: s}
          mode: 自投自复
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室
        
        control_points:
          sensors:
            - {point_id: ATS_V_MAIN, type: AI, description: 主电源电压}
            - {point_id: ATS_V_BACKUP, type: AI, description: 备用电源电压}
          status:
            - {point_id: ATS_POS, type: DI, description: 当前电源位置}
            - {point_id: ATS_MAIN_OK, type: DI, description: 主电源正常}
            - {point_id: ATS_BACKUP_OK, type: DI, description: 备用电源正常}

      - node_id: ELEC-LV_DST_FEEDER_NORMAL
        node_name: 普通负荷馈电柜
        node_name_en: Normal Load Feeder Panel
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 普通负荷配电
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 低压开关柜
          typical_circuits: [照明, 插座, 普通空调, 普通设备]
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室

      - node_id: ELEC-LV_DST_FEEDER_CRITICAL
        node_name: 重要负荷馈电柜
        node_name_en: Critical Load Feeder Panel
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 重要医疗区域配电
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 低压开关柜
          typical_circuits: [手术室, ICU, 急诊, 医疗设备, 净化空调]
          power_source: 双电源（市电+应急）
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室

      - node_id: ELEC-LV_DST_FEEDER_FIRE
        node_name: 消防负荷馈电柜
        node_name_en: Fire Load Feeder Panel
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 消防设备专用配电
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        equipment_parameters:
          type: 低压开关柜
          typical_circuits: [消防泵, 喷淋泵, 排烟风机, 正压风机, 消防电梯]
          power_source: 双电源（市电+应急）
          cable_requirement: 耐火电缆
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室

      - node_id: ELEC-LV_DST_FEEDER_HVAC
        node_name: 暖通动力馈电柜
        node_name_en: HVAC Power Feeder Panel
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 冷冻机组、水泵、空调箱等暖通设备供电
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        equipment_parameters:
          type: 低压开关柜
          typical_circuits: [冷水机组, 冷冻泵, 冷却泵, 冷却塔, AHU, 净化AHU]
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室/冷冻机房配电间

    sink_nodes:
  
      - node_id: ELEC-LV_SNK_FLOOR_DB
        node_name: 楼层配电箱
        node_name_en: Floor Distribution Board
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 楼层配电
        medium_in: ELEC-LV
      
        multiplicity: multiple
        instance_pattern: ELEC-LV_SNK_FLOOR_DB_{Bldg}_{Floor}
      
        location_hint:
          space_type: SHAFT
          shaft_type: 电气竖井
        
      - node_id: ELEC-LV_SNK_EQUIPMENT
        node_name: 动力设备
        node_name_en: Power Equipment
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 动力消耗
        medium_in: ELEC-LV
      
        interface_systems: [HVAC-CHP, HVAC-CWP, HVAC-AHU, ELEVATOR]

  # ============================================================
  # 边定义
  # ============================================================
  edges:

    supply_edges:
  
      - edge_id: ELEC-LV_EDGE_001
        edge_name: 变压器至进线柜
        edge_type: TRK
        from_node: ELEC-LV_SRC_TRANS
        to_node: ELEC-LV_DST_INCB
        direction: unidirectional
        medium: ELEC-LV
        physical_properties:
          cable_type: 母排/低压电缆
        
      - edge_id: ELEC-LV_EDGE_002
        edge_name: 进线柜至母线I段
        edge_type: TRK
        from_node: ELEC-LV_DST_INCB
        to_node: ELEC-LV_DST_BUS1
        direction: unidirectional
        medium: ELEC-LV
      
      - edge_id: ELEC-LV_EDGE_003
        edge_name: 进线柜至母线II段
        edge_type: TRK
        from_node: ELEC-LV_DST_INCB
        to_node: ELEC-LV_DST_BUS2
        direction: unidirectional
        medium: ELEC-LV
      
      - edge_id: ELEC-LV_EDGE_004
        edge_name: 母线I段至母联
        edge_type: TRK
        from_node: ELEC-LV_DST_BUS1
        to_node: ELEC-LV_DST_TIE
        direction: bidirectional
        medium: ELEC-LV
      
      - edge_id: ELEC-LV_EDGE_005
        edge_name: 母联至母线II段
        edge_type: TRK
        from_node: ELEC-LV_DST_TIE
        to_node: ELEC-LV_DST_BUS2
        direction: bidirectional
        medium: ELEC-LV
      
      - edge_id: ELEC-LV_EDGE_006
        edge_name: 应急电源至ATS
        edge_type: TRK
        from_node: ELEC-LV_SRC_EPS
        to_node: ELEC-LV_DST_ATS
        direction: unidirectional
        medium: ELEC-EPS
      
      - edge_id: ELEC-LV_EDGE_007
        edge_name: 母线至ATS（市电侧）
        edge_type: BRH
        from_node: ELEC-LV_DST_BUS1
        to_node: ELEC-LV_DST_ATS
        direction: unidirectional
        medium: ELEC-LV
      
      - edge_id: ELEC-LV_EDGE_008
        edge_name: ATS至重要负荷馈电柜
        edge_type: TRK
        from_node: ELEC-LV_DST_ATS
        to_node: ELEC-LV_DST_FEEDER_CRITICAL
        direction: unidirectional
        medium: ELEC-LV
      
      - edge_id: ELEC-LV_EDGE_009
        edge_name: ATS至消防馈电柜
        edge_type: TRK
        from_node: ELEC-LV_DST_ATS
        to_node: ELEC-LV_DST_FEEDER_FIRE
        direction: unidirectional
        medium: ELEC-LV
      
      - edge_id: ELEC-LV_EDGE_010
        edge_name: 母线至普通负荷馈电柜
        edge_type: BRH
        from_node: ELEC-LV_DST_BUS1
        to_node: ELEC-LV_DST_FEEDER_NORMAL
        direction: unidirectional
        medium: ELEC-LV
      
      - edge_id: ELEC-LV_EDGE_011
        edge_name: 母线至暖通馈电柜
        edge_type: BRH
        from_node: ELEC-LV_DST_BUS1
        to_node: ELEC-LV_DST_FEEDER_HVAC
        direction: unidirectional
        medium: ELEC-LV
      
      - edge_id: ELEC-LV_EDGE_012
        edge_name: 馈电柜至楼层配电箱
        edge_type: TRM
        from_node: ELEC-LV_DST_FEEDER_NORMAL
        to_node: ELEC-LV_SNK_FLOOR_DB
        direction: unidirectional
        medium: ELEC-LV
        physical_properties:
          cable_type: YJV/NH-YJV
          routing: 电气竖井

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:

    - path_id: ELEC-LV_PATH_NORMAL
      path_name: 普通负荷供电路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: ELEC-LV_SRC_TRANS}
        - {step: 2, element_type: edge, element_id: ELEC-LV_EDGE_001}
        - {step: 3, element_type: node, element_id: ELEC-LV_DST_INCB}
        - {step: 4, element_type: edge, element_id: ELEC-LV_EDGE_002}
        - {step: 5, element_type: node, element_id: ELEC-LV_DST_BUS1}
        - {step: 6, element_type: edge, element_id: ELEC-LV_EDGE_010}
        - {step: 7, element_type: node, element_id: ELEC-LV_DST_FEEDER_NORMAL}
        - {step: 8, element_type: edge, element_id: ELEC-LV_EDGE_012}
        - {step: 9, element_type: node, element_id: ELEC-LV_SNK_FLOOR_DB}
      
    - path_id: ELEC-LV_PATH_CRITICAL
      path_name: 重要负荷供电路径（市电）
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: ELEC-LV_SRC_TRANS}
        - {step: 2, element_type: edge, element_id: ELEC-LV_EDGE_001}
        - {step: 3, element_type: node, element_id: ELEC-LV_DST_INCB}
        - {step: 4, element_type: edge, element_id: ELEC-LV_EDGE_002}
        - {step: 5, element_type: node, element_id: ELEC-LV_DST_BUS1}
        - {step: 6, element_type: edge, element_id: ELEC-LV_EDGE_007}
        - {step: 7, element_type: node, element_id: ELEC-LV_DST_ATS}
        - {step: 8, element_type: edge, element_id: ELEC-LV_EDGE_008}
        - {step: 9, element_type: node, element_id: ELEC-LV_DST_FEEDER_CRITICAL}
      
    - path_id: ELEC-LV_PATH_EPS
      path_name: 应急电源供电路径
      path_type: BKP
      sequence:
        - {step: 1, element_type: node, element_id: ELEC-LV_SRC_EPS}
        - {step: 2, element_type: edge, element_id: ELEC-LV_EDGE_006}
        - {step: 3, element_type: node, element_id: ELEC-LV_DST_ATS}
        - {step: 4, element_type: edge, element_id: ELEC-LV_EDGE_008}
        - {step: 5, element_type: node, element_id: ELEC-LV_DST_FEEDER_CRITICAL}

  # ============================================================
  # 回路定义
  # ============================================================
  loops:

    - loop_id: ELEC-LV_LOOP_RING
      loop_name: 低压母线环网
      loop_type: open_ring
    
      description: |
        低压双母线分段运行，母联正常断开。
        单台变压器故障时可通过母联切换至另一段母线供电。
      
    - loop_id: ELEC-LV_LOOP_DUAL_SOURCE
      loop_name: 双电源回路
      loop_type: redundant
    
      description: |
        重要负荷和消防负荷采用双电源供电（市电+应急电源）。
        通过ATS实现自动切换。
```

---

## 第五部分：ELEC-EPS 应急电源系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: ELEC-EPS
    system_name: 应急电源系统
    system_name_en: Emergency Power Supply System
    category: ELECTRICAL
    version: 1.0
  
    description: |
      医院柴油发电机应急电源系统。
      市电失电时自动启动，为重要负荷和消防负荷提供应急供电。
    
    design_basis:
      capacity: {value: 2000-4000, unit: kW}
      configuration: "2×100%或3×50%"
      startup_time: {value: "≤15", unit: s}
      continuous_operation: {value: "≥12", unit: h}
    
    serving_scope:
      - 手术室
      - ICU
      - 急诊
      - 消防设备
      - 电梯（部分）
      - 应急照明

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: ELEC-EPS_BND_IN_FUEL
        boundary_name: 柴油燃料
        medium: FUEL-DIESEL
        is_external: true
      
      - boundary_id: ELEC-EPS_BND_IN_START
        boundary_name: 启动信号
        medium: CTRL-SIGNAL
        source_system: ELEC-LV-MAIN
        trigger: 市电失电
      
    outputs:
      - boundary_id: ELEC-EPS_BND_OUT_POWER
        boundary_name: 应急电源输出
        medium: ELEC-EPS
        target_system: ELEC-LV-MAIN
        interface_point: ATS

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:

    source_nodes:
  
      - node_id: ELEC-EPS_SRC_FUEL_TANK
        node_name: 日用油箱
        node_name_en: Day Tank
        node_type: Source_Node
        node_category: SRC
      
        function: 储存柴油燃料
        medium_out: FUEL-DIESEL
      
        equipment_parameters:
          capacity: {value: 1000-3000, unit: L}
          material: 双层钢制
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 发电机房
          position: 发电机旁
        
        installation_requirements:
          - 防火隔离
          - 漏油检测
          - 通气管
          - 油位显示
        
      - node_id: ELEC-EPS_SRC_GEN
        node_name: 柴油发电机组
        node_name_en: Diesel Generator Set
        node_type: Source_Node
        node_category: SRC
      
        function: 将燃料化学能转换为电能
        medium_in: FUEL-DIESEL
        medium_out: ELEC-EPS
      
        multiplicity: multiple
        instance_pattern: ELEC-EPS_SRC_GEN_{NN}
      
        typical_configuration:
          quantity: 2-3
          redundancy: "N+1"
        
        equipment_parameters:
          capacity_each: {value: 1000-2000, unit: kW}
          voltage: {value: 400, unit: V}
          frequency: {value: 50, unit: Hz}
          power_factor: {value: 0.8, unit: null}
          startup_time: {value: "≤10", unit: s}
          fuel_consumption: {value: 200-400, unit: "L/h"}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 发电机房
          floor: 地下或首层独立
        
        installation_requirements:
          - 减振基础
          - 进排风系统
          - 排烟系统
          - 消声措施
          - 吊装通道
          - 检修空间
        
        control_points:
          sensors:
            - {point_id: GEN_V, type: AI, description: 输出电压}
            - {point_id: GEN_I, type: AI, description: 输出电流}
            - {point_id: GEN_F, type: AI, description: 输出频率}
            - {point_id: GEN_P, type: AI, description: 输出功率}
            - {point_id: GEN_RPM, type: AI, description: 转速}
            - {point_id: GEN_OIL_P, type: AI, description: 机油压力}
            - {point_id: GEN_WATER_T, type: AI, description: 冷却水温}
            - {point_id: GEN_FUEL_L, type: AI, description: 油箱液位}
          status:
            - {point_id: GEN_RUN, type: DI, description: 运行状态}
            - {point_id: GEN_READY, type: DI, description: 就绪状态}
            - {point_id: GEN_FAULT, type: DI, description: 故障报警}
            - {point_id: GEN_OVERLOAD, type: DI, description: 过载报警}
          commands:
            - {point_id: GEN_START, type: DO, description: 启动命令}
            - {point_id: GEN_STOP, type: DO, description: 停机命令}
            - {point_id: GEN_TEST, type: DO, description: 测试命令}

    distribution_nodes:
  
      - node_id: ELEC-EPS_DST_GCB
        node_name: 发电机出线柜
        node_name_en: Generator Circuit Breaker Panel
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 发电机输出保护与并联
        medium_in: ELEC-EPS
        medium_out: ELEC-EPS
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 低压开关柜
          rated_current: {value: 3200, unit: A}
          protection: [过流, 短路, 逆功率, 欠压]
          sync_function: true
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 发电机房配电间

      - node_id: ELEC-EPS_DST_SYNC_BUS
        node_name: 并机母线
        node_name_en: Synchronizing Bus
        node_type: Distribution_Node
        node_category: DST
        node_subtype: JUN
      
        function: 多台发电机并联运行
        medium_in: ELEC-EPS
        medium_out: ELEC-EPS
      
        equipment_parameters:
          rated_voltage: {value: 400, unit: V}
          rated_current: {value: 5000, unit: A}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 发电机房配电间

      - node_id: ELEC-EPS_DST_MAIN_CB
        node_name: 应急电源总出线柜
        node_name_en: EPS Main Output Panel
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 应急电源总输出保护
        medium_in: ELEC-EPS
        medium_out: ELEC-EPS
      
        equipment_parameters:
          type: 低压开关柜
          rated_current: {value: 4000, unit: A}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 发电机房配电间

    sink_nodes:
  
      - node_id: ELEC-EPS_SNK_ATS
        node_name: ATS备用电源侧
        node_name_en: ATS Backup Power Side
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 电力输出
        medium_in: ELEC-EPS
      
        interface_system: ELEC-LV-MAIN
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室

  # ============================================================
  # 边定义
  # ============================================================
  edges:

    supply_edges:
  
      - edge_id: ELEC-EPS_EDGE_001
        edge_name: 油箱至发电机
        edge_type: TRK
        from_node: ELEC-EPS_SRC_FUEL_TANK
        to_node: ELEC-EPS_SRC_GEN
        direction: unidirectional
        medium: FUEL-DIESEL
        physical_properties:
          pipe_material: 无缝钢管
        
      - edge_id: ELEC-EPS_EDGE_002
        edge_name: 发电机至出线柜
        edge_type: TRK
        from_node: ELEC-EPS_SRC_GEN
        to_node: ELEC-EPS_DST_GCB
        direction: unidirectional
        medium: ELEC-EPS
        physical_properties:
          cable_type: YJV-4×240+1×120
        
      - edge_id: ELEC-EPS_EDGE_003
        edge_name: 出线柜至并机母线
        edge_type: TRK
        from_node: ELEC-EPS_DST_GCB
        to_node: ELEC-EPS_DST_SYNC_BUS
        direction: unidirectional
        medium: ELEC-EPS
      
      - edge_id: ELEC-EPS_EDGE_004
        edge_name: 并机母线至总出线
        edge_type: TRK
        from_node: ELEC-EPS_DST_SYNC_BUS
        to_node: ELEC-EPS_DST_MAIN_CB
        direction: unidirectional
        medium: ELEC-EPS
      
      - edge_id: ELEC-EPS_EDGE_005
        edge_name: 总出线至ATS
        edge_type: TRK
        from_node: ELEC-EPS_DST_MAIN_CB
        to_node: ELEC-EPS_SNK_ATS
        direction: unidirectional
        medium: ELEC-EPS
        physical_properties:
          cable_type: NH-YJV-4×240+1×120
          routing: 电缆桥架

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:

    - path_id: ELEC-EPS_PATH_MAIN
      path_name: 应急供电主路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: ELEC-EPS_SRC_FUEL_TANK}
        - {step: 2, element_type: edge, element_id: ELEC-EPS_EDGE_001}
        - {step: 3, element_type: node, element_id: ELEC-EPS_SRC_GEN}
        - {step: 4, element_type: edge, element_id: ELEC-EPS_EDGE_002}
        - {step: 5, element_type: node, element_id: ELEC-EPS_DST_GCB}
        - {step: 6, element_type: edge, element_id: ELEC-EPS_EDGE_003}
        - {step: 7, element_type: node, element_id: ELEC-EPS_DST_SYNC_BUS}
        - {step: 8, element_type: edge, element_id: ELEC-EPS_EDGE_004}
        - {step: 9, element_type: node, element_id: ELEC-EPS_DST_MAIN_CB}
        - {step: 10, element_type: edge, element_id: ELEC-EPS_EDGE_005}
        - {step: 11, element_type: node, element_id: ELEC-EPS_SNK_ATS}

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:

    startup_sequence:
      - step: 1
        condition: 市电失电信号
        action: 发送启动命令至发电机
      
      - step: 2
        condition: 发电机接收启动命令
        action: 预热、启动发动机
        duration: {value: "3-5", unit: s}
      
      - step: 3
        condition: 转速稳定、电压建立
        action: 发电机出线柜合闸
        duration: {value: "5-8", unit: s}
      
      - step: 4
        condition: 多台发电机需并联
        action: 同期并网
      
      - step: 5
        condition: 应急电源母线建立
        action: ATS切换至应急电源
        total_time: {value: "≤15", unit: s}
      
    return_sequence:
      - step: 1
        condition: 市电恢复且稳定30s
        action: ATS切换回市电
      
      - step: 2
        condition: ATS完成切换
        action: 发电机空载运行冷却
        duration: {value: 3-5, unit: min}
      
      - step: 3
        action: 发电机停机
      
    test_mode:
      frequency: 每月一次
      duration: {value: 15-30, unit: min}
      load: 带载测试
```

---

## 第六部分：ELEC-IT 隔离电源系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: ELEC-IT
    system_name: 隔离电源系统
    system_name_en: Isolated Power System (IT System)
    category: ELECTRICAL
    version: 1.0
  
    description: |
      医院手术室、ICU等医疗场所专用隔离电源系统。
      采用隔离变压器构成IT系统（不接地系统），
      配置绝缘监测装置，确保医疗安全。
    
    design_basis:
      application: 2类医疗场所
      voltage: {value: 220, unit: V}
      grounding: 不接地系统（IT系统）
      insulation_monitor: 必配
    
    serving_scope:
      - 手术室医疗设备插座
      - ICU医疗设备插座
      - 心导管室
      - DSA手术室

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: ELEC-IT_BND_IN_LV
        boundary_name: 低压电源输入
        medium: ELEC-LV
        source_system: ELEC-LV-CRITICAL
        parameters:
          voltage: {value: "380/220", unit: V}
          source: 双电源（经ATS）
        
    outputs:
      - boundary_id: ELEC-IT_BND_OUT_IT
        boundary_name: 隔离电源输出
        medium: ELEC-IT
        target: 医疗设备插座

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:

    source_nodes:
  
      - node_id: ELEC-IT_SRC_LV
        node_name: 隔离电源输入
        node_name_en: IT System Input
        node_type: Source_Node
        node_category: SRC
      
        function: 接收低压电源
        medium_out: ELEC-LV
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 手术部电气间

    distribution_nodes:
  
      - node_id: ELEC-IT_DST_ISO_TRANS
        node_name: 隔离变压器
        node_name_en: Isolation Transformer
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
      
        function: 电气隔离，构成IT系统
        medium_in: ELEC-LV
        medium_out: ELEC-IT
      
        multiplicity: multiple
        instance_pattern: ELEC-IT_DST_ISO_TRANS_OT{NN}
      
        typical_configuration:
          quantity: 每间手术室1台
        
        equipment_parameters:
          capacity: {value: 8-10, unit: kVA}
          ratio: "1:1"
          voltage: {value: "220/220", unit: V}
          insulation_class: F
          temperature_rise: {value: 100, unit: K}
        
        location_hint:
          space_type: WALL_CABINET
          position: 手术室外墙嵌入式安装
        
        installation_requirements:
          - 嵌墙安装
          - 防护等级IP21
          - 散热通风
          - 检修门
        
      - node_id: ELEC-IT_DST_IMD
        node_name: 绝缘监测装置
        node_name_en: Insulation Monitoring Device
        node_type: Distribution_Node
        node_category: DST
        node_subtype: MON
      
        function: 监测IT系统对地绝缘电阻
        medium_in: ELEC-IT
      
        multiplicity: multiple
      
        equipment_parameters:
          monitoring_range: {value: "1-500", unit: kΩ}
          alarm_threshold: {value: 50, unit: kΩ}
          response_time: {value: "<5", unit: s}
        
        location_hint:
          space_type: WALL_CABINET
          position: 与隔离变压器同位置
        
        control_points:
          sensors:
            - {point_id: IMD_R, type: AI, description: 绝缘电阻值}
            - {point_id: IMD_LOAD, type: AI, description: 负载电流}
          status:
            - {point_id: IMD_ALARM, type: DI, description: 绝缘故障报警}
            - {point_id: IMD_FAULT, type: DI, description: 装置故障}
          outputs:
            - {point_id: IMD_DISPLAY, description: 本地显示面板}
            - {point_id: IMD_REMOTE, description: 远程报警信号}

      - node_id: ELEC-IT_DST_IT_PANEL
        node_name: 隔离电源配电箱
        node_name_en: IT System Distribution Panel
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: IT系统输出配电
        medium_in: ELEC-IT
        medium_out: ELEC-IT
      
        multiplicity: multiple
      
        equipment_parameters:
          circuits: {value: 6-12, unit: 回路}
          rated_current: {value: 10-20, unit: A, per_circuit: true}
          rcbo: false  # IT系统不使用RCD
        
        location_hint:
          space_type: WALL_CABINET
          position: 与隔离变压器同位置

    sink_nodes:
  
      - node_id: ELEC-IT_SNK_OUTLET
        node_name: 医疗设备插座
        node_name_en: Medical Equipment Outlet
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 医疗设备供电
        medium_in: ELEC-IT
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 医用插座
          grounding: 等电位连接
          color_code: 绿色/蓝色
        
        location_hint:
          space_type: WALL
          position: 手术室墙面/吊塔

  # ============================================================
  # 边定义
  # ============================================================
  edges:

    supply_edges:
  
      - edge_id: ELEC-IT_EDGE_001
        edge_name: 电源输入至隔离变压器
        edge_type: TRK
        from_node: ELEC-IT_SRC_LV
        to_node: ELEC-IT_DST_ISO_TRANS
        direction: unidirectional
        medium: ELEC-LV
        physical_properties:
          cable_type: YJV-3×6
        
      - edge_id: ELEC-IT_EDGE_002
        edge_name: 隔离变压器至IMD
        edge_type: BRH
        from_node: ELEC-IT_DST_ISO_TRANS
        to_node: ELEC-IT_DST_IMD
        direction: unidirectional
        medium: ELEC-IT
        note: 监测连接
      
      - edge_id: ELEC-IT_EDGE_003
        edge_name: 隔离变压器至配电箱
        edge_type: TRK
        from_node: ELEC-IT_DST_ISO_TRANS
        to_node: ELEC-IT_DST_IT_PANEL
        direction: unidirectional
        medium: ELEC-IT
      
      - edge_id: ELEC-IT_EDGE_004
        edge_name: 配电箱至医疗插座
        edge_type: TRM
        from_node: ELEC-IT_DST_IT_PANEL
        to_node: ELEC-IT_SNK_OUTLET
        direction: unidirectional
        medium: ELEC-IT
        physical_properties:
          cable_type: BV-3×2.5

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:

    - path_id: ELEC-IT_PATH_MAIN
      path_name: 隔离电源供电路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: ELEC-IT_SRC_LV}
        - {step: 2, element_type: edge, element_id: ELEC-IT_EDGE_001}
        - {step: 3, element_type: node, element_id: ELEC-IT_DST_ISO_TRANS}
        - {step: 4, element_type: edge, element_id: ELEC-IT_EDGE_003}
        - {step: 5, element_type: node, element_id: ELEC-IT_DST_IT_PANEL}
        - {step: 6, element_type: edge, element_id: ELEC-IT_EDGE_004}
        - {step: 7, element_type: node, element_id: ELEC-IT_SNK_OUTLET}

  # ============================================================
  # 安全逻辑
  # ============================================================
  safety_logic:

    insulation_fault_handling:
      - condition: 绝缘电阻 < 50kΩ
        action: 
          - 本地声光报警
          - 远程报警至护士站
          - 不切断电源（这是IT系统核心优势）
        reason: 第一次故障不会导致危险电流
      
      - condition: 第二次绝缘故障
        action:
          - 紧急报警
          - 人工检查处理
        
    equipotential_bonding:
      - 手术台
      - 无影灯
      - 吊塔
      - 医疗设备外壳
      - 金属门框窗框
      bonding_resistance: {value: "≤0.1", unit: Ω}
```

---

## 第七部分：MGAS-O2 医用氧气系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: MGAS-O2
    system_name: 医用氧气系统
    system_name_en: Medical Oxygen System
    category: MEDICAL_GAS
    version: 1.0
  
    description: |
      医院中心供氧系统，采用液氧储罐+汇流排备用方式供气。
      经减压、过滤后通过管网输送至全院各医疗区域终端。
    
    design_basis:
      supply_mode: 液氧主供 + 汇流排备用
      terminal_pressure: {value: 0.4-0.5, unit: MPa}
      purity: {value: "≥99.5", unit: "%"}
    
    serving_scope:
      - 手术室
      - ICU
      - 急诊
      - 病房
      - 门诊治疗室

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: MGAS-O2_BND_IN_LOX
        boundary_name: 液氧供应
        medium: LOX
        is_external: true
        source: 液氧槽车
      
      - boundary_id: MGAS-O2_BND_IN_CYL
        boundary_name: 氧气瓶组
        medium: GAS-O2
        is_external: true
        source: 高压氧气瓶
      
      - boundary_id: MGAS-O2_BND_IN_ELEC
        boundary_name: 电源
        medium: ELEC-LV
        source_system: ELEC-LV-CRITICAL
      
    outputs:
      - boundary_id: MGAS-O2_BND_OUT_O2
        boundary_name: 氧气终端
        medium: GAS-O2
        target: 医疗设备/治疗带

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:

    source_nodes:
  
      - node_id: MGAS-O2_SRC_LOX_TANK
        node_name: 液氧储罐
        node_name_en: Liquid Oxygen Tank
        node_type: Source_Node
        node_category: SRC
      
        function: 液氧储存与气化
        medium_in: LOX
        medium_out: GAS-O2
      
        is_external: false
      
        equipment_parameters:
          capacity: {value: 5-20, unit: m³}
          working_pressure: {value: 1.6, unit: MPa}
          evaporator_type: 空温式/电加热
          daily_evaporation: {value: 0.3-0.5, unit: "%"}
        
        location_hint:
          space_type: OUTDOOR
          position: 室外液氧站
        
        installation_requirements:
          - 防火间距 ≥ 10m
          - 防雷接地
          - 围栏防护
          - 禁止明火标识
          - 消防设施
          - 防晒棚（可选）
        
        control_points:
          sensors:
            - {point_id: LOX_LEVEL, type: AI, description: 液位}
            - {point_id: LOX_PRESSURE, type: AI, description: 储罐压力}
            - {point_id: O2_OUT_PRESSURE, type: AI, description: 出口压力}
          status:
            - {point_id: LOX_LOW_LEVEL, type: DI, description: 低液位报警}
            - {point_id: LOX_HIGH_PRESSURE, type: DI, description: 高压报警}

      - node_id: MGAS-O2_SRC_MANIFOLD
        node_name: 氧气汇流排
        node_name_en: Oxygen Cylinder Manifold
        node_type: Source_Node
        node_category: SRC
      
        function: 高压氧气瓶组减压供气（备用气源）
        medium_in: GAS-O2 (高压)
        medium_out: GAS-O2
      
        equipment_parameters:
          configuration: 双组自动切换
          cylinders_per_group: {value: 10-20, unit: 瓶}
          inlet_pressure: {value: 15, unit: MPa}
          outlet_pressure: {value: 0.8-1.0, unit: MPa}
        
        location_hint:
          space_type: OUTDOOR / MEP_ROOM
          room_name: 汇流排间
        
        installation_requirements:
          - 通风良好
          - 防火分隔
          - 禁止油脂
          - 气瓶固定
        
        control_points:
          sensors:
            - {point_id: MAN_PRESSURE_L, type: AI, description: 左组压力}
            - {point_id: MAN_PRESSURE_R, type: AI, description: 右组压力}
          status:
            - {point_id: MAN_SWITCHOVER, type: DI, description: 切换指示}
            - {point_id: MAN_LOW_PRESSURE, type: DI, description: 低压报警}

    distribution_nodes:
  
      - node_id: MGAS-O2_DST_AUTO_SWITCH
        node_name: 气源自动切换装置
        node_name_en: Automatic Source Switchover
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 液氧/汇流排自动切换
        medium_in: GAS-O2
        medium_out: GAS-O2
      
        equipment_parameters:
          mode: 自动切换（液氧优先）
          switchover_pressure: {value: 0.6, unit: MPa}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 供气站
        
        control_points:
          sensors:
            - {point_id: SW_IN_P1, type: AI, description: 主气源压力}
            - {point_id: SW_IN_P2, type: AI, description: 备用气源压力}
          status:
            - {point_id: SW_SOURCE, type: DI, description: 当前气源}
            - {point_id: SW_ALARM, type: DI, description: 切换报警}

      - node_id: MGAS-O2_DST_MAIN_VALVE
        node_name: 总阀门
        node_name_en: Main Shut-off Valve
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 系统总控制阀
        medium_in: GAS-O2
        medium_out: GAS-O2
      
        equipment_parameters:
          type: 截止阀
          size: {value: DN50-DN80, unit: mm}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 供气站

      - node_id: MGAS-O2_DST_FIRST_REG
        node_name: 一级减压
        node_name_en: First Stage Pressure Regulator
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 高压减至中压
        medium_in: GAS-O2
        medium_out: GAS-O2
      
        equipment_parameters:
          inlet_pressure: {value: 0.8-1.0, unit: MPa}
          outlet_pressure: {value: 0.5-0.6, unit: MPa}
          configuration: 一用一备
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 供气站

      - node_id: MGAS-O2_DST_MAIN_PIPE
        node_name: 氧气主管
        node_name_en: Oxygen Main Pipe
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
      
        function: 水平输配主干管
        medium_in: GAS-O2
        medium_out: GAS-O2
      
        equipment_parameters:
          material: 脱脂铜管/不锈钢管
          diameter: {value: DN50-DN80, unit: mm}
        
        location_hint:
          space_type: CEILING_VOID / PIPE_TRENCH
          position: 地下室或走廊吊顶

      - node_id: MGAS-O2_DST_RISER
        node_name: 氧气立管
        node_name_en: Oxygen Riser
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 垂直输配
        medium_in: GAS-O2
        medium_out: GAS-O2
      
        multiplicity: multiple
        instance_pattern: MGAS-O2_DST_RISER_{Zone}
      
        equipment_parameters:
          material: 脱脂铜管/不锈钢管
          diameter: {value: DN25-DN40, unit: mm}
        
        location_hint:
          space_type: SHAFT
          shaft_type: 医气管井

      - node_id: MGAS-O2_DST_ZONE_VALVE
        node_name: 区域阀门箱
        node_name_en: Zone Valve Box
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 区域控制与二级减压
        medium_in: GAS-O2
        medium_out: GAS-O2
      
        multiplicity: multiple
        instance_pattern: MGAS-O2_DST_ZONE_VALVE_{Floor}_{Zone}
      
        equipment_parameters:
          components: [截止阀, 减压阀, 压力表, 报警接口]
          inlet_pressure: {value: 0.5-0.6, unit: MPa}
          outlet_pressure: {value: 0.4-0.45, unit: MPa}
        
        location_hint:
          space_type: WALL_CABINET
          position: 护士站附近走廊
        
        control_points:
          sensors:
            - {point_id: ZONE_PRESSURE, type: AI, description: 区域压力}
          status:
            - {point_id: ZONE_LOW_P, type: DI, description: 低压报警}
            - {point_id: ZONE_HIGH_P, type: DI, description: 高压报警}

      - node_id: MGAS-O2_DST_FLOOR_PIPE
        node_name: 楼层支管
        node_name_en: Floor Branch Pipe
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BRH
      
        function: 楼层水平分配
        medium_in: GAS-O2
        medium_out: GAS-O2
      
        equipment_parameters:
          material: 脱脂铜管
          diameter: {value: DN15-DN25, unit: mm}
        
        location_hint:
          space_type: CEILING_VOID
          position: 病房走廊吊顶

    sink_nodes:
  
      - node_id: MGAS-O2_SNK_TERMINAL
        node_name: 氧气终端
        node_name_en: Oxygen Terminal Outlet
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 氧气供应
        medium_in: GAS-O2
      
        multiplicity: multiple
        instance_pattern: MGAS-O2_SNK_TERMINAL_{Floor}_{Room}_{Seq}
      
        equipment_parameters:
          type: 快速接头
          standard: 德标DIN/美标DISS/国标
          flow_rate: {value: 10-15, unit: L/min}
          terminal_pressure: {value: 0.4-0.5, unit: MPa}
          color_code: 白色
        
        location_hint:
          space_type: WALL / HEADWALL / PENDANT
          position: 床头设备带、手术室吊塔
        
        typical_quantity:
          per_bed_icu: 2
          per_bed_ward: 1
          per_or: 4

  # ============================================================
  # 边定义
  # ============================================================
  edges:

    supply_edges:
  
      - edge_id: MGAS-O2_EDGE_001
        edge_name: 液氧站至切换装置
        edge_type: TRK
        from_node: MGAS-O2_SRC_LOX_TANK
        to_node: MGAS-O2_DST_AUTO_SWITCH
        direction: unidirectional
        medium: GAS-O2
        medium_properties:
          pressure: {value: 0.8-1.0, unit: MPa}
        physical_properties:
          material: 铜管
          diameter: DN40
        
      - edge_id: MGAS-O2_EDGE_002
        edge_name: 汇流排至切换装置
        edge_type: TRK
        from_node: MGAS-O2_SRC_MANIFOLD
        to_node: MGAS-O2_DST_AUTO_SWITCH
        direction: unidirectional
        medium: GAS-O2
        medium_properties:
          pressure: {value: 0.8-1.0, unit: MPa}
        
      - edge_id: MGAS-O2_EDGE_003
        edge_name: 切换装置至总阀门
        edge_type: TRK
        from_node: MGAS-O2_DST_AUTO_SWITCH
        to_node: MGAS-O2_DST_MAIN_VALVE
        direction: unidirectional
        medium: GAS-O2
      
      - edge_id: MGAS-O2_EDGE_004
        edge_name: 总阀门至一级减压
        edge_type: TRK
        from_node: MGAS-O2_DST_MAIN_VALVE
        to_node: MGAS-O2_DST_FIRST_REG
        direction: unidirectional
        medium: GAS-O2
        medium_properties:
          pressure: {value: 0.8-1.0, unit: MPa}
        
      - edge_id: MGAS-O2_EDGE_005
        edge_name: 一级减压至主管
        edge_type: TRK
        from_node: MGAS-O2_DST_FIRST_REG
        to_node: MGAS-O2_DST_MAIN_PIPE
        direction: unidirectional
        medium: GAS-O2
        medium_properties:
          pressure: {value: 0.5-0.6, unit: MPa}
        
      - edge_id: MGAS-O2_EDGE_006
        edge_name: 主管至立管
        edge_type: BRH
        from_node: MGAS-O2_DST_MAIN_PIPE
        to_node: MGAS-O2_DST_RISER
        direction: unidirectional
        medium: GAS-O2
      
      - edge_id: MGAS-O2_EDGE_007
        edge_name: 立管至区域阀门箱
        edge_type: BRH
        from_node: MGAS-O2_DST_RISER
        to_node: MGAS-O2_DST_ZONE_VALVE
        direction: unidirectional
        medium: GAS-O2
      
      - edge_id: MGAS-O2_EDGE_008
        edge_name: 区域阀门箱至楼层支管
        edge_type: TRK
        from_node: MGAS-O2_DST_ZONE_VALVE
        to_node: MGAS-O2_DST_FLOOR_PIPE
        direction: unidirectional
        medium: GAS-O2
        medium_properties:
          pressure: {value: 0.4-0.45, unit: MPa}
        
      - edge_id: MGAS-O2_EDGE_009
        edge_name: 楼层支管至终端
        edge_type: TRM
        from_node: MGAS-O2_DST_FLOOR_PIPE
        to_node: MGAS-O2_SNK_TERMINAL
        direction: unidirectional
        medium: GAS-O2
        medium_properties:
          pressure: {value: 0.4-0.5, unit: MPa}

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:

    - path_id: MGAS-O2_PATH_MAIN
      path_name: 氧气主供路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: MGAS-O2_SRC_LOX_TANK}
        - {step: 2, element_type: edge, element_id: MGAS-O2_EDGE_001}
        - {step: 3, element_type: node, element_id: MGAS-O2_DST_AUTO_SWITCH}
        - {step: 4, element_type: edge, element_id: MGAS-O2_EDGE_003}
        - {step: 5, element_type: node, element_id: MGAS-O2_DST_MAIN_VALVE}
        - {step: 6, element_type: edge, element_id: MGAS-O2_EDGE_004}
        - {step: 7, element_type: node, element_id: MGAS-O2_DST_FIRST_REG}
        - {step: 8, element_type: edge, element_id: MGAS-O2_EDGE_005}
        - {step: 9, element_type: node, element_id: MGAS-O2_DST_MAIN_PIPE}
        - {step: 10, element_type: edge, element_id: MGAS-O2_EDGE_006}
        - {step: 11, element_type: node, element_id: MGAS-O2_DST_RISER}
        - {step: 12, element_type: edge, element_id: MGAS-O2_EDGE_007}
        - {step: 13, element_type: node, element_id: MGAS-O2_DST_ZONE_VALVE}
        - {step: 14, element_type: edge, element_id: MGAS-O2_EDGE_008}
        - {step: 15, element_type: node, element_id: MGAS-O2_DST_FLOOR_PIPE}
        - {step: 16, element_type: edge, element_id: MGAS-O2_EDGE_009}
        - {step: 17, element_type: node, element_id: MGAS-O2_SNK_TERMINAL}
      
    - path_id: MGAS-O2_PATH_BACKUP
      path_name: 氧气备用路径
      path_type: BKP
      description: 液氧故障时，汇流排自动接管供气
      sequence:
        - {step: 1, element_type: node, element_id: MGAS-O2_SRC_MANIFOLD}
        - {step: 2, element_type: edge, element_id: MGAS-O2_EDGE_002}
        - {step: 3, element_type: node, element_id: MGAS-O2_DST_AUTO_SWITCH}
        # 后续路径与主路径相同

  # ============================================================
  # 回路/冗余定义
  # ============================================================
  loops:

    - loop_id: MGAS-O2_LOOP_DUAL_SOURCE
      loop_name: 双气源冗余
      loop_type: redundant
    
      description: |
        液氧为主气源，汇流排为备用气源。
        液氧压力低于设定值时自动切换至汇流排。
        液氧恢复后自动切回。
      
      primary_source: MGAS-O2_SRC_LOX_TANK
      backup_source: MGAS-O2_SRC_MANIFOLD
      switchover_node: MGAS-O2_DST_AUTO_SWITCH
      switchover_pressure: {value: 0.6, unit: MPa}

  # ============================================================
  # 报警与监控
  # ============================================================
  alarm_system:

    alarm_stations:
      - location: 供气站
        alarms: [液位低, 压力异常, 气源切换]
      
      - location: 护士站（每区域）
        alarms: [区域压力低, 区域压力高]
      
      - location: 中央监控室
        alarms: [所有报警汇总]
      
    alarm_levels:
      - level: 高优先级
        conditions: [液位极低, 压力极低, 系统故障]
        response: 声光报警 + 远程通知
      
      - level: 中优先级
        conditions: [液位低, 气源切换]
        response: 声光报警
      
      - level: 低优先级
        conditions: [液位预警]
        response: 指示灯
```

---

## 第八部分：MGAS-VAC 医用负压吸引系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: MGAS-VAC
    system_name: 医用负压吸引系统
    system_name_en: Medical Vacuum System
    category: MEDICAL_GAS
    version: 1.0
  
    description: |
      医院中心负压吸引系统，采用真空泵机组产生负压，
      通过管网输送至各医疗区域终端，用于吸引手术废液、痰液等。
    
    design_basis:
      vacuum_level: {value: -40 ~ -60, unit: kPa}
      flow_per_terminal: {value: 40, unit: L/min}
      pump_configuration: "N+1备用"
    
    serving_scope:
      - 手术室
      - ICU
      - 急诊
      - 病房
      - 门诊治疗室

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: MGAS-VAC_BND_IN_ELEC
        boundary_name: 电源
        medium: ELEC-LV
        source_system: ELEC-LV-CRITICAL
      
    outputs:
      - boundary_id: MGAS-VAC_BND_OUT_VAC
        boundary_name: 负压终端
        medium: GAS-VAC
        target: 医疗设备/治疗带
      
      - boundary_id: MGAS-VAC_BND_OUT_EXHAUST
        boundary_name: 废气排放
        medium: AIR-EA
        is_external: true
        target: 大气

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:

    source_nodes:
  
      - node_id: MGAS-VAC_SRC_PUMP
        node_name: 真空泵组
        node_name_en: Vacuum Pump Set
        node_type: Source_Node
        node_category: SRC
      
        function: 产生负压
        medium_out: GAS-VAC
      
        multiplicity: multiple
        instance_pattern: MGAS-VAC_SRC_PUMP_{NN}
      
        typical_configuration:
          quantity: 3-4
          redundancy: "N+1"
        
        equipment_parameters:
          type: 油封旋片泵/水环泵/干式无油泵
          capacity_each: {value: 100-250, unit: m³/h}
          ultimate_vacuum: {value: -85, unit: kPa}
          working_vacuum: {value: -60, unit: kPa}
          power: {value: 7.5-15, unit: kW}
          noise: {value: "≤75", unit: dB(A)}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 负压泵房
          floor: 地下室或设备层
        
        installation_requirements:
          - 通风良好
          - 减振基础
          - 废气排放接口
          - 噪声控制
        
        control_points:
          sensors:
            - {point_id: VAC_PUMP_I, type: AI, description: 运行电流}
            - {point_id: VAC_PUMP_TEMP, type: AI, description: 泵温}
          status:
            - {point_id: VAC_PUMP_RUN, type: DI, description: 运行状态}
            - {point_id: VAC_PUMP_FAULT, type: DI, description: 故障报警}
          commands:
            - {point_id: VAC_PUMP_START, type: DO, description: 启停控制}

    distribution_nodes:
  
      - node_id: MGAS-VAC_DST_RECEIVER
        node_name: 真空罐
        node_name_en: Vacuum Receiver Tank
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BUF
      
        function: 缓冲储存、稳定真空度
        medium_in: GAS-VAC
        medium_out: GAS-VAC
      
        equipment_parameters:
          capacity: {value: 500-1500, unit: L}
          working_pressure: {value: -60, unit: kPa}
          material: 不锈钢
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 负压泵房
        
        control_points:
          sensors:
            - {point_id: VAC_TANK_P, type: AI, description: 罐内真空度}

      - node_id: MGAS-VAC_DST_BACTERIA_FILTER
        node_name: 细菌过滤器
        node_name_en: Bacterial Filter
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
      
        function: 过滤细菌、防止交叉污染
        medium_in: GAS-VAC
        medium_out: GAS-VAC
      
        equipment_parameters:
          filter_efficiency: {value: "≥99.97%@0.3μm", unit: null}
          replacement_cycle: {value: 6-12, unit: 月}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 负压泵房

      - node_id: MGAS-VAC_DST_MAIN_PIPE
        node_name: 负压主管
        node_name_en: Vacuum Main Pipe
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
      
        function: 水平输配主干管
        medium_in: GAS-VAC
        medium_out: GAS-VAC
      
        equipment_parameters:
          material: 镀锌钢管/不锈钢管
          diameter: {value: DN65-DN100, unit: mm}
          slope: {value: "≥3‰", note: 向泵房方向倾斜}
        
        location_hint:
          space_type: CEILING_VOID / PIPE_TRENCH

      - node_id: MGAS-VAC_DST_RISER
        node_name: 负压立管
        node_name_en: Vacuum Riser
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 垂直输配
        medium_in: GAS-VAC
        medium_out: GAS-VAC
      
        multiplicity: multiple
      
        equipment_parameters:
          material: 镀锌钢管/不锈钢管
          diameter: {value: DN40-DN50, unit: mm}
        
        location_hint:
          space_type: SHAFT
          shaft_type: 医气管井

      - node_id: MGAS-VAC_DST_ZONE_VALVE
        node_name: 区域阀门箱
        node_name_en: Zone Valve Box
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 区域控制
        medium_in: GAS-VAC
        medium_out: GAS-VAC
      
        multiplicity: multiple
      
        equipment_parameters:
          components: [截止阀, 真空表, 报警接口]
        
        location_hint:
          space_type: WALL_CABINET
          position: 护士站附近走廊
        
        control_points:
          sensors:
            - {point_id: ZONE_VAC, type: AI, description: 区域真空度}
          status:
            - {point_id: ZONE_VAC_LOW, type: DI, description: 真空度低报警}

      - node_id: MGAS-VAC_DST_FLOOR_PIPE
        node_name: 楼层支管
        node_name_en: Floor Branch Pipe
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BRH
      
        function: 楼层水平分配
        medium_in: GAS-VAC
        medium_out: GAS-VAC
      
        equipment_parameters:
          material: 镀锌钢管
          diameter: {value: DN25-DN32, unit: mm}
        
        location_hint:
          space_type: CEILING_VOID

    sink_nodes:
  
      - node_id: MGAS-VAC_SNK_TERMINAL
        node_name: 负压吸引终端
        node_name_en: Vacuum Terminal Outlet
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 负压吸引
        medium_in: GAS-VAC
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 快速接头
          flow_rate: {value: 40, unit: L/min}
          vacuum_level: {value: -40 ~ -60, unit: kPa}
          color_code: 黄色
        
        location_hint:
          space_type: WALL / HEADWALL / PENDANT
          position: 床头设备带、手术室吊塔
        
        typical_quantity:
          per_bed_icu: 2
          per_bed_ward: 1
          per_or: 3

      - node_id: MGAS-VAC_SNK_EXHAUST
        node_name: 废气排放口
        node_name_en: Exhaust Outlet
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 废气排放
        medium_in: AIR-EA
        is_external: true
      
        location_hint:
          space_type: EXTERIOR
          position: 屋顶（远离新风口）
          height: ≥ 3m高于屋面

  # ============================================================
  # 边定义
  # ============================================================
  edges:

    supply_edges:
  
      - edge_id: MGAS-VAC_EDGE_001
        edge_name: 真空罐至真空泵
        edge_type: TRK
        from_node: MGAS-VAC_DST_RECEIVER
        to_node: MGAS-VAC_SRC_PUMP
        direction: unidirectional
        medium: GAS-VAC
        note: 抽气方向（被抽气体流向）
      
      - edge_id: MGAS-VAC_EDGE_002
        edge_name: 过滤器至真空罐
        edge_type: TRK
        from_node: MGAS-VAC_DST_BACTERIA_FILTER
        to_node: MGAS-VAC_DST_RECEIVER
        direction: unidirectional
        medium: GAS-VAC
      
      - edge_id: MGAS-VAC_EDGE_003
        edge_name: 主管至过滤器
        edge_type: TRK
        from_node: MGAS-VAC_DST_MAIN_PIPE
        to_node: MGAS-VAC_DST_BACTERIA_FILTER
        direction: unidirectional
        medium: GAS-VAC
      
      - edge_id: MGAS-VAC_EDGE_004
        edge_name: 立管至主管
        edge_type: BRH
        from_node: MGAS-VAC_DST_RISER
        to_node: MGAS-VAC_DST_MAIN_PIPE
        direction: unidirectional
        medium: GAS-VAC
      
      - edge_id: MGAS-VAC_EDGE_005
        edge_name: 区域阀门箱至立管
        edge_type: BRH
        from_node: MGAS-VAC_DST_ZONE_VALVE
        to_node: MGAS-VAC_DST_RISER
        direction: unidirectional
        medium: GAS-VAC
      
      - edge_id: MGAS-VAC_EDGE_006
        edge_name: 楼层支管至区域阀门箱
        edge_type: TRK
        from_node: MGAS-VAC_DST_FLOOR_PIPE
        to_node: MGAS-VAC_DST_ZONE_VALVE
        direction: unidirectional
        medium: GAS-VAC
      
      - edge_id: MGAS-VAC_EDGE_007
        edge_name: 终端至楼层支管
        edge_type: TRM
        from_node: MGAS-VAC_SNK_TERMINAL
        to_node: MGAS-VAC_DST_FLOOR_PIPE
        direction: unidirectional
        medium: GAS-VAC
        note: 被抽气体从终端流向主管
      
      - edge_id: MGAS-VAC_EDGE_008
        edge_name: 真空泵废气排放
        edge_type: TRK
        from_node: MGAS-VAC_SRC_PUMP
        to_node: MGAS-VAC_SNK_EXHAUST
        direction: unidirectional
        medium: AIR-EA

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:

    - path_id: MGAS-VAC_PATH_MAIN
      path_name: 负压吸引路径
      path_type: SUP
      description: 气体流动方向：终端→泵房
      sequence:
        - {step: 1, element_type: node, element_id: MGAS-VAC_SNK_TERMINAL}
        - {step: 2, element_type: edge, element_id: MGAS-VAC_EDGE_007}
        - {step: 3, element_type: node, element_id: MGAS-VAC_DST_FLOOR_PIPE}
        - {step: 4, element_type: edge, element_id: MGAS-VAC_EDGE_006}
        - {step: 5, element_type: node, element_id: MGAS-VAC_DST_ZONE_VALVE}
        - {step: 6, element_type: edge, element_id: MGAS-VAC_EDGE_005}
        - {step: 7, element_type: node, element_id: MGAS-VAC_DST_RISER}
        - {step: 8, element_type: edge, element_id: MGAS-VAC_EDGE_004}
        - {step: 9, element_type: node, element_id: MGAS-VAC_DST_MAIN_PIPE}
        - {step: 10, element_type: edge, element_id: MGAS-VAC_EDGE_003}
        - {step: 11, element_type: node, element_id: MGAS-VAC_DST_BACTERIA_FILTER}
        - {step: 12, element_type: edge, element_id: MGAS-VAC_EDGE_002}
        - {step: 13, element_type: node, element_id: MGAS-VAC_DST_RECEIVER}
        - {step: 14, element_type: edge, element_id: MGAS-VAC_EDGE_001}
        - {step: 15, element_type: node, element_id: MGAS-VAC_SRC_PUMP}
      
    - path_id: MGAS-VAC_PATH_EXHAUST
      path_name: 废气排放路径
      path_type: EXH
      sequence:
        - {step: 1, element_type: node, element_id: MGAS-VAC_SRC_PUMP}
        - {step: 2, element_type: edge, element_id: MGAS-VAC_EDGE_008}
        - {step: 3, element_type: node, element_id: MGAS-VAC_SNK_EXHAUST}

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:

    pump_control:
      mode: 真空度控制
      setpoint:
        start: {value: -50, unit: kPa, note: 真空度降至此值启动备用泵}
        stop: {value: -65, unit: kPa, note: 真空度达此值停止运行泵}
      sequence: 轮换运行（均衡磨损）
    
    alarm_logic:
      - condition: 真空度 > -40kPa
        level: 高优先级
        action: 声光报警 + 启动全部泵
      
      - condition: 真空度 > -50kPa
        level: 中优先级
        action: 报警 + 启动备用泵
      
      - condition: 泵故障
        level: 高优先级
        action: 声光报警 + 启动备用泵
```

---

## 第九部分：MGAS-AIR 医用压缩空气系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: MGAS-AIR
    system_name: 医用压缩空气系统
    system_name_en: Medical Compressed Air System
    category: MEDICAL_GAS
    version: 1.0
  
    description: |
      医院医用压缩空气系统，采用无油空压机产生压缩空气，
      经干燥、过滤净化后通过管网输送至各医疗区域终端。
      用于呼吸机驱动、气动工具等医疗用途。
    
    design_basis:
      supply_pressure: {value: 0.7-0.8, unit: MPa}
      terminal_pressure: {value: 0.4-0.5, unit: MPa}
      dew_point: {value: "≤-40", unit: ℃}
      oil_content: {value: "≤0.1", unit: "mg/m³"}
      particle: {value: "≤0.5", unit: μm}
    
    serving_scope:
      - 手术室
      - ICU
      - 急诊
      - NICU
      - 呼吸治疗

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: MGAS-AIR_BND_IN_ATM
        boundary_name: 大气
        medium: AIR-OA
        is_external: true
      
      - boundary_id: MGAS-AIR_BND_IN_ELEC
        boundary_name: 电源
        medium: ELEC-LV
        source_system: ELEC-LV-CRITICAL
      
    outputs:
      - boundary_id: MGAS-AIR_BND_OUT_AIR
        boundary_name: 压缩空气终端
        medium: GAS-AIR
        target: 医疗设备

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:

    source_nodes:
  
      - node_id: MGAS-AIR_SRC_INTAKE
        node_name: 进气口
        node_name_en: Air Intake
        node_type: Source_Node
        node_category: SRC
      
        function: 吸入大气
        medium_out: AIR-OA
        is_external: true
      
        equipment_parameters:
          filter: 初效过滤
          position: 远离污染源
        
        location_hint:
          space_type: EXTERIOR
          position: 室外洁净区域
          height: ≥ 2m
        
      - node_id: MGAS-AIR_SRC_COMPRESSOR
        node_name: 无油空压机
        node_name_en: Oil-free Air Compressor
        node_type: Source_Node
        node_category: SRC
      
        function: 压缩空气产生
        medium_in: AIR-OA
        medium_out: GAS-AIR
      
        multiplicity: multiple
        instance_pattern: MGAS-AIR_SRC_COMPRESSOR_{NN}
      
        typical_configuration:
          quantity: 3
          redundancy: "N+1"
        
        equipment_parameters:
          type: 无油涡旋式/螺杆式
          capacity_each: {value: 1-3, unit: m³/min}
          discharge_pressure: {value: 0.8, unit: MPa}
          power: {value: 7.5-22, unit: kW}
          noise: {value: "≤75", unit: dB(A)}
          oil_free: true
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 空压机房
        
        installation_requirements:
          - 通风良好
          - 减振基础
          - 进气过滤
          - 噪声控制
        
        control_points:
          sensors:
            - {point_id: COMP_P, type: AI, description: 排气压力}
            - {point_id: COMP_I, type: AI, description: 运行电流}
            - {point_id: COMP_TEMP, type: AI, description: 排气温度}
          status:
            - {point_id: COMP_RUN, type: DI, description: 运行状态}
            - {point_id: COMP_FAULT, type: DI, description: 故障报警}
          commands:
            - {point_id: COMP_START, type: DO, description: 启停控制}

    distribution_nodes:
  
      - node_id: MGAS-AIR_DST_RECEIVER
        node_name: 储气罐
        node_name_en: Air Receiver Tank
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BUF
      
        function: 缓冲储存、稳定压力
        medium_in: GAS-AIR
        medium_out: GAS-AIR
      
        equipment_parameters:
          capacity: {value: 1000-3000, unit: L}
          working_pressure: {value: 1.0, unit: MPa}
          material: 碳钢
          drain: 自动排水器
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 空压机房
        
      - node_id: MGAS-AIR_DST_DRYER
        node_name: 冷冻式干燥机
        node_name_en: Refrigerated Air Dryer
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
      
        function: 冷却除湿
        medium_in: GAS-AIR
        medium_out: GAS-AIR
      
        equipment_parameters:
          type: 冷冻式
          capacity: {value: 3-10, unit: m³/min}
          outlet_dew_point: {value: 2-10, unit: ℃}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 空压机房

      - node_id: MGAS-AIR_DST_ADSORB_DRYER
        node_name: 吸附式干燥机
        node_name_en: Desiccant Air Dryer
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
      
        function: 深度干燥
        medium_in: GAS-AIR
        medium_out: GAS-AIR
      
        equipment_parameters:
          type: 无热再生/加热再生
          capacity: {value: 3-10, unit: m³/min}
          outlet_dew_point: {value: "-40 ~ -70", unit: ℃}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 空压机房

      - node_id: MGAS-AIR_DST_FILTER_SET
        node_name: 过滤器组
        node_name_en: Filter Set
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
      
        function: 多级过滤净化
        medium_in: GAS-AIR
        medium_out: GAS-AIR
      
        equipment_parameters:
          stages:
            - {stage: 1, type: 除水过滤器, efficiency: "液滴≤0.1ppm"}
            - {stage: 2, type: 除油过滤器, efficiency: "油雾≤0.01ppm"}
            - {stage: 3, type: 除菌过滤器, efficiency: "≥99.99%@0.01μm"}
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 空压机房

      - node_id: MGAS-AIR_DST_REGULATOR
        node_name: 一级减压阀
        node_name_en: First Stage Regulator
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 压力调节
        medium_in: GAS-AIR
        medium_out: GAS-AIR
      
        equipment_parameters:
          inlet_pressure: {value: 0.7-0.8, unit: MPa}
          outlet_pressure: {value: 0.5-0.6, unit: MPa}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 空压机房

      - node_id: MGAS-AIR_DST_MAIN_PIPE
        node_name: 压缩空气主管
        node_name_en: Compressed Air Main Pipe
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
      
        function: 水平输配主干管
        medium_in: GAS-AIR
        medium_out: GAS-AIR
      
        equipment_parameters:
          material: 脱脂铜管/不锈钢管
          diameter: {value: DN40-DN65, unit: mm}
        
        location_hint:
          space_type: CEILING_VOID / PIPE_TRENCH

      - node_id: MGAS-AIR_DST_RISER
        node_name: 压缩空气立管
        node_name_en: Compressed Air Riser
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 垂直输配
        medium_in: GAS-AIR
        medium_out: GAS-AIR
      
        multiplicity: multiple
      
        equipment_parameters:
          material: 脱脂铜管/不锈钢管
          diameter: {value: DN25-DN32, unit: mm}
        
        location_hint:
          space_type: SHAFT
          shaft_type: 医气管井

      - node_id: MGAS-AIR_DST_ZONE_VALVE
        node_name: 区域阀门箱
        node_name_en: Zone Valve Box
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 区域控制与二级减压
        medium_in: GAS-AIR
        medium_out: GAS-AIR
      
        multiplicity: multiple
      
        equipment_parameters:
          components: [截止阀, 减压阀, 压力表, 报警接口]
          outlet_pressure: {value: 0.4-0.5, unit: MPa}
        
        location_hint:
          space_type: WALL_CABINET
          position: 护士站附近走廊

      - node_id: MGAS-AIR_DST_FLOOR_PIPE
        node_name: 楼层支管
        node_name_en: Floor Branch Pipe
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BRH
      
        function: 楼层水平分配
        medium_in: GAS-AIR
        medium_out: GAS-AIR
      
        equipment_parameters:
          material: 脱脂铜管
          diameter: {value: DN15-DN20, unit: mm}
        
        location_hint:
          space_type: CEILING_VOID

    sink_nodes:
  
      - node_id: MGAS-AIR_SNK_TERMINAL
        node_name: 压缩空气终端
        node_name_en: Compressed Air Terminal Outlet
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 压缩空气供应
        medium_in: GAS-AIR
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 快速接头
          terminal_pressure: {value: 0.4-0.5, unit: MPa}
          color_code: 黑白相间
        
        location_hint:
          space_type: WALL / HEADWALL / PENDANT
          position: 床头设备带、手术室吊塔
        
        typical_quantity:
          per_bed_icu: 2
          per_bed_ward: 1
          per_or: 2

  # ============================================================
  # 边定义
  # ============================================================
  edges:

    supply_edges:
  
      - edge_id: MGAS-AIR_EDGE_001
        edge_name: 进气口至空压机
        edge_type: TRK
        from_node: MGAS-AIR_SRC_INTAKE
        to_node: MGAS-AIR_SRC_COMPRESSOR
        direction: unidirectional
        medium: AIR-OA
      
      - edge_id: MGAS-AIR_EDGE_002
        edge_name: 空压机至储气罐
        edge_type: TRK
        from_node: MGAS-AIR_SRC_COMPRESSOR
        to_node: MGAS-AIR_DST_RECEIVER
        direction: unidirectional
        medium: GAS-AIR
        medium_properties:
          pressure: {value: 0.8, unit: MPa}
        
      - edge_id: MGAS-AIR_EDGE_003
        edge_name: 储气罐至冷干机
        edge_type: TRK
        from_node: MGAS-AIR_DST_RECEIVER
        to_node: MGAS-AIR_DST_DRYER
        direction: unidirectional
        medium: GAS-AIR
      
      - edge_id: MGAS-AIR_EDGE_004
        edge_name: 冷干机至吸干机
        edge_type: TRK
        from_node: MGAS-AIR_DST_DRYER
        to_node: MGAS-AIR_DST_ADSORB_DRYER
        direction: unidirectional
        medium: GAS-AIR
      
      - edge_id: MGAS-AIR_EDGE_005
        edge_name: 吸干机至过滤器组
        edge_type: TRK
        from_node: MGAS-AIR_DST_ADSORB_DRYER
        to_node: MGAS-AIR_DST_FILTER_SET
        direction: unidirectional
        medium: GAS-AIR
      
      - edge_id: MGAS-AIR_EDGE_006
        edge_name: 过滤器组至减压阀
        edge_type: TRK
        from_node: MGAS-AIR_DST_FILTER_SET
        to_node: MGAS-AIR_DST_REGULATOR
        direction: unidirectional
        medium: GAS-AIR
      
      - edge_id: MGAS-AIR_EDGE_007
        edge_name: 减压阀至主管
        edge_type: TRK
        from_node: MGAS-AIR_DST_REGULATOR
        to_node: MGAS-AIR_DST_MAIN_PIPE
        direction: unidirectional
        medium: GAS-AIR
        medium_properties:
          pressure: {value: 0.5-0.6, unit: MPa}
        
      - edge_id: MGAS-AIR_EDGE_008
        edge_name: 主管至立管
        edge_type: BRH
        from_node: MGAS-AIR_DST_MAIN_PIPE
        to_node: MGAS-AIR_DST_RISER
        direction: unidirectional
        medium: GAS-AIR
      
      - edge_id: MGAS-AIR_EDGE_009
        edge_name: 立管至区域阀门箱
        edge_type: BRH
        from_node: MGAS-AIR_DST_RISER
        to_node: MGAS-AIR_DST_ZONE_VALVE
        direction: unidirectional
        medium: GAS-AIR
      
      - edge_id: MGAS-AIR_EDGE_010
        edge_name: 区域阀门箱至楼层支管
        edge_type: TRK
        from_node: MGAS-AIR_DST_ZONE_VALVE
        to_node: MGAS-AIR_DST_FLOOR_PIPE
        direction: unidirectional
        medium: GAS-AIR
        medium_properties:
          pressure: {value: 0.4-0.5, unit: MPa}
        
      - edge_id: MGAS-AIR_EDGE_011
        edge_name: 楼层支管至终端
        edge_type: TRM
        from_node: MGAS-AIR_DST_FLOOR_PIPE
        to_node: MGAS-AIR_SNK_TERMINAL
        direction: unidirectional
        medium: GAS-AIR

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:

    - path_id: MGAS-AIR_PATH_MAIN
      path_name: 压缩空气主路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: MGAS-AIR_SRC_INTAKE}
        - {step: 2, element_type: edge, element_id: MGAS-AIR_EDGE_001}
        - {step: 3, element_type: node, element_id: MGAS-AIR_SRC_COMPRESSOR}
        - {step: 4, element_type: edge, element_id: MGAS-AIR_EDGE_002}
        - {step: 5, element_type: node, element_id: MGAS-AIR_DST_RECEIVER}
        - {step: 6, element_type: edge, element_id: MGAS-AIR_EDGE_003}
        - {step: 7, element_type: node, element_id: MGAS-AIR_DST_DRYER}
        - {step: 8, element_type: edge, element_id: MGAS-AIR_EDGE_004}
        - {step: 9, element_type: node, element_id: MGAS-AIR_DST_ADSORB_DRYER}
        - {step: 10, element_type: edge, element_id: MGAS-AIR_EDGE_005}
        - {step: 11, element_type: node, element_id: MGAS-AIR_DST_FILTER_SET}
        - {step: 12, element_type: edge, element_id: MGAS-AIR_EDGE_006}
        - {step: 13, element_type: node, element_id: MGAS-AIR_DST_REGULATOR}
        - {step: 14, element_type: edge, element_id: MGAS-AIR_EDGE_007}
        - {step: 15, element_type: node, element_id: MGAS-AIR_DST_MAIN_PIPE}
        - {step: 16, element_type: edge, element_id: MGAS-AIR_EDGE_008}
        - {step: 17, element_type: node, element_id: MGAS-AIR_DST_RISER}
        - {step: 18, element_type: edge, element_id: MGAS-AIR_EDGE_009}
        - {step: 19, element_type: node, element_id: MGAS-AIR_DST_ZONE_VALVE}
        - {step: 20, element_type: edge, element_id: MGAS-AIR_EDGE_010}
        - {step: 21, element_type: node, element_id: MGAS-AIR_DST_FLOOR_PIPE}
        - {step: 22, element_type: edge, element_id: MGAS-AIR_EDGE_011}
        - {step: 23, element_type: node, element_id: MGAS-AIR_SNK_TERMINAL}

  # ============================================================
  # 气体质量监控
  # ============================================================
  quality_monitoring:

    parameters:
      - parameter: 露点温度
        limit: {value: "≤-40", unit: ℃}
        monitoring_point: 干燥机出口
      
      - parameter: 含油量
        limit: {value: "≤0.1", unit: "mg/m³"}
        monitoring_point: 过滤器出口
      
      - parameter: 颗粒物
        limit: {value: "≤0.5", unit: μm}
        monitoring_point: 过滤器出口
      
      - parameter: CO含量
        limit: {value: "≤5", unit: ppm}
        monitoring_point: 主管
      
    alarm_conditions:
      - condition: 露点超标
        action: 报警 + 检查干燥机
      
      - condition: 压差过高
        action: 报警 + 更换过滤器
```

---

## 第十部分：系统间接口关系图补充

```yaml
System_Interfaces_Batch2:

  # 电气系统链路
  - interface_id: IF_HV_TO_LV
    upstream_system: ELEC-HV
    downstream_system: ELEC-LV-MAIN
    interface_equipment: 变压器
    interface_medium: ELEC-HV → ELEC-LV
  
  - interface_id: IF_EPS_TO_LV
    upstream_system: ELEC-EPS
    downstream_system: ELEC-LV-MAIN
    interface_equipment: ATS自动转换开关
    interface_medium: ELEC-EPS
  
  - interface_id: IF_LV_TO_IT
    upstream_system: ELEC-LV-CRITICAL
    downstream_system: ELEC-IT
    interface_equipment: 隔离变压器
    interface_medium: ELEC-LV → ELEC-IT
  
  # 医疗气体系统与电气系统
  - interface_id: IF_ELEC_TO_O2
    upstream_system: ELEC-LV-CRITICAL
    downstream_system: MGAS-O2
    interface_medium: ELEC-LV
    purpose: 液氧气化器加热、监控报警系统
  
  - interface_id: IF_ELEC_TO_VAC
    upstream_system: ELEC-LV-CRITICAL
    downstream_system: MGAS-VAC
    interface_medium: ELEC-LV
    purpose: 真空泵动力
  
  - interface_id: IF_ELEC_TO_AIR
    upstream_system: ELEC-LV-CRITICAL
    downstream_system: MGAS-AIR
    interface_medium: ELEC-LV
    purpose: 空压机、干燥机动力
  
  # 医疗气体终端汇聚
  - interface_id: IF_MGAS_TO_HEADWALL
    upstream_systems: [MGAS-O2, MGAS-VAC, MGAS-AIR]
    downstream_system: 床头设备带
    interface_medium: [GAS-O2, GAS-VAC, GAS-AIR]
    location: 病房、ICU床头
  
  - interface_id: IF_MGAS_TO_PENDANT
    upstream_systems: [MGAS-O2, MGAS-VAC, MGAS-AIR, MGAS-N2O, MGAS-AGSS]
    downstream_system: 手术室吊塔
    interface_medium: [GAS-O2, GAS-VAC, GAS-AIR, GAS-N2O, GAS-AGSS]
    location: 手术室
```

---

## 第十一部分：质量校验清单 (Batch 2)

```yaml
Quality_Checklist_Batch2:

  # 结构完整性
  structure_completeness:
    - check: 所有电气系统形成完整供电链路（HV→LV→终端）
      status: ✅
    - check: 应急电源系统具备完整的启动和转换逻辑
      status: ✅
    - check: 隔离电源系统包含绝缘监测
      status: ✅
    - check: 医疗气体系统具备双气源/冗余设计
      status: ✅
    - check: 负压吸引系统路径方向正确（终端→泵房）
      status: ✅

  # 安全设计
  safety_design:
    - check: 电气系统分级保护完整
      status: ✅
    - check: IT系统安全逻辑明确
      status: ✅
    - check: 医疗气体报警系统完整
      status: ✅
    - check: 冗余/备用路径已定义
      status: ✅

  # 参数完整性
  parameter_completeness:
    - check: 电气设备容量参数完整
      status: ✅
    - check: 医疗气体压力等级明确
      status: ✅
    - check: 控制点位已定义
      status: ✅
    - check: 安装要求已说明
      status: ✅

  # 下游接口
  downstream_interfaces:
    - agent: Agent-03 (设备属性)
      status: ✅ 设备参数完整
    - agent: Agent-04 (流动模型)
      status: ✅ 压力/流量参数提供
    - agent: Agent-05 (空间定位)
      status: ✅ location_hint完整
```

---

## 输出总结 (Batch 2)

| 系统 | 状态 | 节点数 | 边数 | 路径数 | 特殊说明 |
|------|------|--------|------|--------|----------|
| ELEC-HV | ✅ 完成 | 9 | 9 | 3 | 双电源+母联 |
| ELEC-LV-MAIN | ✅ 完成 | 14 | 12 | 3 | 含ATS转换 |
| ELEC-EPS | ✅ 完成 | 7 | 5 | 1 | 启停逻辑 |
| ELEC-IT | ✅ 完成 | 6 | 4 | 1 | 绝缘监测 |
| MGAS-O2 | ✅ 完成 | 12 | 9 | 2 | 双气源冗余 |
| MGAS-VAC | ✅ 完成 | 10 | 8 | 2 | 含排气路径 |
| MGAS-AIR | ✅ 完成 | 14 | 11 | 1 | 完整净化链 |

---

# 第二部分：Batch 2 补充文档 (电气/医疗气体系统补充)

## 2.1 ELEC-LV-MAIN 低压主配电系统补充

```yaml
System_Topology_Patch:

  system_id: ELEC-LV-MAIN
  patch_version: 1.1
  patch_description: 补充楼层配电详细节点、UPS接口、照明接口

  # ============================================================
  # 新增节点
  # ============================================================
  additional_nodes:

    distribution_nodes:
  
      - node_id: ELEC-LV_DST_FLOOR_MDB
        node_name: 楼层总配电箱
        node_name_en: Floor Main Distribution Board
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 楼层配电总控
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        multiplicity: multiple
        instance_pattern: ELEC-LV_DST_FLOOR_MDB_{Bldg}_{Floor}
      
        equipment_parameters:
          type: 配电箱
          rated_current: {value: 400-630, unit: A}
          circuits: {value: 20-40, unit: 回路}
          metering: 分项计量
        
        location_hint:
          space_type: SHAFT
          shaft_type: 电气竖井
          position: 每层核心筒
        
        control_points:
          sensors:
            - {point_id: FLOOR_V, type: AI, description: 电压}
            - {point_id: FLOOR_I, type: AI, description: 电流}
            - {point_id: FLOOR_P, type: AI, description: 功率}
            - {point_id: FLOOR_KWH, type: AI, description: 电能}
          status:
            - {point_id: FLOOR_TRIP, type: DI, description: 跳闸报警}

      - node_id: ELEC-LV_DST_AREA_DB
        node_name: 区域配电箱
        node_name_en: Area Distribution Board
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 功能区域配电
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        multiplicity: multiple
        instance_pattern: ELEC-LV_DST_AREA_DB_{Floor}_{Area}
      
        equipment_parameters:
          type: 配电箱
          rated_current: {value: 100-250, unit: A}
        
        location_hint:
          space_type: WALL_BOX
          position: 各功能区域入口

      - node_id: ELEC-LV_DST_UPS_FEED
        node_name: UPS馈电柜
        node_name_en: UPS Feeder Panel
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 向UPS系统馈电
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        equipment_parameters:
          type: 低压开关柜
          rated_current: {value: 400-800, unit: A}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: UPS机房/低压配电室
        
        interface_system: ELEC-UPS

      - node_id: ELEC-LV_DST_LIGHT_FEED
        node_name: 照明馈电柜
        node_name_en: Lighting Feeder Panel
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 照明系统总配电
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        equipment_parameters:
          type: 低压开关柜
          circuits: 
            - 普通照明
            - 应急照明
            - 疏散指示
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室
        
        interface_system: ELEC-LIGHT

    sink_nodes:
  
      - node_id: ELEC-LV_SNK_TERMINAL
        node_name: 终端用电点
        node_name_en: Terminal Load
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 电力消耗
        medium_in: ELEC-LV
      
        multiplicity: multiple
      
        equipment_parameters:
          types:
            - 插座
            - 设备直接供电
            - 照明灯具

  # ============================================================
  # 新增边
  # ============================================================
  additional_edges:

    - edge_id: ELEC-LV_EDGE_TO_FLOOR
      edge_name: 馈电柜至楼层配电
      edge_type: TRK
      from_node: ELEC-LV_DST_FEEDER_NORMAL
      to_node: ELEC-LV_DST_FLOOR_MDB
      direction: unidirectional
      medium: ELEC-LV
      physical_properties:
        cable_type: YJV
        routing: 电气竖井
      
    - edge_id: ELEC-LV_EDGE_TO_AREA
      edge_name: 楼层配电至区域
      edge_type: BRH
      from_node: ELEC-LV_DST_FLOOR_MDB
      to_node: ELEC-LV_DST_AREA_DB
      direction: unidirectional
      medium: ELEC-LV
      physical_properties:
        cable_type: YJV
        routing: 走廊桥架
      
    - edge_id: ELEC-LV_EDGE_TO_UPS
      edge_name: 至UPS馈电
      edge_type: TRK
      from_node: ELEC-LV_DST_FEEDER_CRITICAL
      to_node: ELEC-LV_DST_UPS_FEED
      direction: unidirectional
      medium: ELEC-LV
    
    - edge_id: ELEC-LV_EDGE_TO_LIGHT
      edge_name: 至照明馈电
      edge_type: TRK
      from_node: ELEC-LV_DST_BUS1
      to_node: ELEC-LV_DST_LIGHT_FEED
      direction: unidirectional
      medium: ELEC-LV

  # ============================================================
  # 补充系统边界
  # ============================================================
  additional_boundary:

    outputs:
      - boundary_id: ELEC-LV_BND_OUT_UPS
        boundary_name: UPS系统供电
        medium: ELEC-LV
        target_system: ELEC-UPS
      
      - boundary_id: ELEC-LV_BND_OUT_LIGHT
        boundary_name: 照明系统供电
        medium: ELEC-LV
        target_system: ELEC-LIGHT
```

## 2.2 ELEC-EPS 应急电源系统补充

```yaml
System_Topology_Patch:

  system_id: ELEC-EPS
  patch_version: 1.1
  patch_description: 补充柴油储罐安全要求、巡检要求

  # ============================================================
  # 节点属性补充
  # ============================================================
  node_patches:

    - node_id: ELEC-EPS_SRC_FUEL_TANK
      additional_properties:
      
        safety_requirements:
          fire_protection:
            - 储油间防火分隔（耐火极限2h）
            - 配置灭火器
            - 禁止明火标识
          spill_control:
            - 设置围堰/集油坑
            - 容积≥储罐容量110%
            - 防渗漏材料
          ventilation:
            - 机械通风
            - 换气次数≥6次/h
            - 防爆风机
          leak_detection:
            - 油位监测
            - 漏油传感器
            - 报警至消防控制室
          
        maintenance_requirements:
          inspection:
            frequency: 每周
            items:
              - 油位检查
              - 泄漏检查
              - 通气管检查
              - 阀门状态
          fuel_replacement:
            frequency: 每6个月
            reason: 柴油存放过久品质下降

      additional_control_points:
        sensors:
          - {point_id: FUEL_LEVEL, type: AI, description: 油位}
          - {point_id: FUEL_LEAK, type: DI, description: 漏油检测}
        status:
          - {point_id: FUEL_LOW, type: DI, description: 低油位报警}
          - {point_id: FUEL_HIGH, type: DI, description: 高油位报警}

  # ============================================================
  # 新增节点 - 室外储油罐（大容量备用）
  # ============================================================
  additional_nodes:

    source_nodes:
  
      - node_id: ELEC-EPS_SRC_MAIN_TANK
        node_name: 室外储油罐
        node_name_en: Outdoor Fuel Storage Tank
        node_type: Source_Node
        node_category: SRC
      
        function: 大容量柴油储存
        medium_out: FUEL-DIESEL
      
        equipment_parameters:
          capacity: {value: 10000-30000, unit: L}
          type: 地上/地下卧式储罐
          material: 双层钢制
        
        location_hint:
          space_type: OUTDOOR
          position: 室外独立储罐区
        
        installation_requirements:
          - 防火间距≥12m
          - 防雷接地
          - 围堰
          - 消防设施
          - 卸油接口
          - 液位计量
        
        control_points:
          sensors:
            - {point_id: MAIN_TANK_LEVEL, type: AI, description: 主罐油位}
          status:
            - {point_id: MAIN_TANK_LOW, type: DI, description: 低油位}

  additional_edges:

    - edge_id: ELEC-EPS_EDGE_MAIN_TO_DAY
      edge_name: 主油罐至日用油箱
      edge_type: TRK
      from_node: ELEC-EPS_SRC_MAIN_TANK
      to_node: ELEC-EPS_SRC_FUEL_TANK
      direction: unidirectional
      medium: FUEL-DIESEL
      physical_properties:
        pipe_material: 无缝钢管
      
  # ============================================================
  # 补充控制逻辑
  # ============================================================
  additional_control_logic:

    fuel_transfer:
      description: 主油罐至日用油箱自动补油
      trigger: 日用油箱液位 < 50%
      action: 启动输油泵
      stop: 日用油箱液位 > 90%
    
    low_fuel_alarm:
      level_1:
        condition: 日用油箱 < 30%
        action: 报警提示
      level_2:
        condition: 日用油箱 < 15%
        action: 紧急报警+通知维护
```

## 2.3 MGAS系统补充 - 终端设备带/吊塔接口

```yaml
System_Topology_Patch:

  system_id: MGAS-O2
  patch_version: 1.1
  patch_description: 补充设备带/吊塔终端汇聚节点

  # ============================================================
  # 新增节点
  # ============================================================
  additional_nodes:

    sink_nodes:
  
      - node_id: MGAS-O2_SNK_HEADWALL
        node_name: 床头设备带
        node_name_en: Headwall Unit
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 医疗气体终端集成
        medium_in: [GAS-O2, GAS-VAC, GAS-AIR]
      
        multiplicity: multiple
        instance_pattern: MGAS-O2_SNK_HEADWALL_{Floor}_{Room}_{Bed}
      
        equipment_parameters:
          type: 床头设备带
          integrated_services:
            - 医用氧气终端
            - 负压吸引终端
            - 压缩空气终端
            - 电源插座
            - 网络接口
            - 护理呼叫
            - 阅读灯
          terminal_per_bed:
            O2: 1
            VAC: 1
            AIR: 1 (部分)
          
        location_hint:
          space_type: WALL
          position: 病床床头
          height: {value: 1.2-1.5, unit: m}
        
      - node_id: MGAS-O2_SNK_PENDANT
        node_name: 手术室吊塔
        node_name_en: OR Ceiling Pendant
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 手术室医疗气体终端集成
        medium_in: [GAS-O2, GAS-VAC, GAS-AIR, GAS-N2O, GAS-CO2, GAS-AGSS]
      
        multiplicity: multiple
        instance_pattern: MGAS-O2_SNK_PENDANT_OR{NN}_{Side}
      
        equipment_parameters:
          type: 手术吊塔
          configuration: 双吊塔/三吊塔
          integrated_services:
            - 医用氧气终端 ×2-4
            - 负压吸引终端 ×2-3
            - 压缩空气终端 ×2
            - 笑气终端 ×1
            - CO2终端 ×1 (腔镜室)
            - 麻醉废气收集 ×2
            - 电源插座 (多规格)
            - 网络接口
            - 设备挂载
          
        location_hint:
          space_type: CEILING
          position: 手术床两侧
          height: 可升降

---
# 同样为MGAS-VAC和MGAS-AIR添加设备带/吊塔终端引用
System_Topology_Patch:

  system_id: MGAS-VAC
  patch_version: 1.1

  additional_boundary:
    outputs:
      - boundary_id: MGAS-VAC_BND_OUT_HEADWALL
        boundary_name: 床头设备带终端
        medium: GAS-VAC
        target_node: MGAS-O2_SNK_HEADWALL
        note: 与O2共用设备带节点
      
      - boundary_id: MGAS-VAC_BND_OUT_PENDANT
        boundary_name: 手术室吊塔终端
        medium: GAS-VAC
        target_node: MGAS-O2_SNK_PENDANT
        note: 与O2共用吊塔节点

---
System_Topology_Patch:

  system_id: MGAS-AIR
  patch_version: 1.1

  additional_boundary:
    outputs:
      - boundary_id: MGAS-AIR_BND_OUT_HEADWALL
        boundary_name: 床头设备带终端
        medium: GAS-AIR
        target_node: MGAS-O2_SNK_HEADWALL
      
      - boundary_id: MGAS-AIR_BND_OUT_PENDANT
        boundary_name: 手术室吊塔终端
        medium: GAS-AIR
        target_node: MGAS-O2_SNK_PENDANT
```

---
