# Agent-01 系统拓扑建模师 - 第二批次：电气系统 + 医疗气体系 （第三次修订版）

## 第二批次：电气系统 + 医疗气体系统（8个系统）

---

# 电气系统（3个系统）

## 系统 2.1: ELEC-HV 高压配电系统

```yaml
System_Topology:

  # ========================================
  # IDENTITY SECTION - 系统标识
  # ========================================
  identity:
    system_id: ELEC-HV
    system_name: 高压配电系统
    system_name_en: High Voltage Distribution System
    system_category: ELEC
    system_type: 高压配电
    priority_level: P0-LIFE_SAFETY
  
    description: |
      医院高压配电系统，接收市电10kV电源，通过高压开关柜分配至各变压器。
      系统采用双路市电进线+柴油发电机组的供电模式，确保医院一级负荷供电可靠性。
      高压系统是医院电力供应的源头，其可靠性直接关系到医院运营安全。
  
    design_basis:
      voltage_level: {value: 10, unit: kV}
      system_frequency: {value: 50, unit: Hz}
      neutral_grounding: 小电阻接地/不接地
      short_circuit_current: {value: 25, unit: kA, note: "系统短路容量"}
      total_installed_capacity: {value: 8000, unit: kVA, note: "变压器总装机容量"}
      power_supply_category: 一级负荷（特别重要）
    
    child_systems:
      - ELEC-LV-MAIN  # 低压配电总系统
      - ELEC-EPS      # 应急电源系统
  
    related_systems:
      - INT-BA        # 楼宇自控（电力监控）
      - FIRE-FAS      # 火灾报警（联动切电）
  
    design_standards:
      - GB 50052-2009 供配电系统设计规范
      - GB 50054-2011 低压配电设计规范
      - GB 51348-2019 民用建筑电气设计标准
      - GB 50016-2014 建筑设计防火规范
      - JGJ 312-2013 医疗建筑电气设计规范
  
    version: 1.0
    last_updated: 2024

  # ========================================
  # BOUNDARY SECTION - 系统边界
  # ========================================
  boundary:
  
    inputs:
      - boundary_id: ELEC-HV_IN_001
        name: 市电一路进线
        from_system: EXTERNAL_UTILITY_1
        medium: ELEC-HV
        parameters:
          voltage: {value: 10, unit: kV}
          capacity: {value: 10000, unit: kVA, note: "供电容量"}
          source: 变电站A（独立电源）
        note: 来自不同变电站的独立电源
      
      - boundary_id: ELEC-HV_IN_002
        name: 市电二路进线
        from_system: EXTERNAL_UTILITY_2
        medium: ELEC-HV
        parameters:
          voltage: {value: 10, unit: kV}
          capacity: {value: 10000, unit: kVA}
          source: 变电站B（独立电源）
        note: 来自不同变电站的独立电源
      
      - boundary_id: ELEC-HV_IN_003
        name: 柴油发电机高压输出
        from_system: ELEC-EPS
        from_node: ELEC-EPS_SRC_GENERATOR
        medium: ELEC-HV
        parameters:
          voltage: {value: 10, unit: kV, note: "高压发电机组"}
        optional: true
        note: 大型医院可能采用高压发电机
        
    outputs:
      - boundary_id: ELEC-HV_OUT_001
        name: 变压器高压侧输入
        to_system: ELEC-LV-MAIN
        to_node: ELEC-LV-MAIN_SRC_TRANSFORMER
        medium: ELEC-HV
        parameters:
          voltage: {value: 10, unit: kV}

  # ========================================
  # NODES SECTION - 节点定义
  # ========================================
  nodes:

    # ========================================
    # Source Nodes - 电源输入节点
    # ========================================
    source_nodes:
  
      - node_id: ELEC-HV_SRC_UTILITY_1
        node_name: 市电一路进线
        node_name_en: Utility Power Incoming Line 1
        node_type: Source_Node
        node_category: SRC
      
        function: 接收市电一路10kV电源
        medium_in: ELEC-HV
        medium_out: ELEC-HV
      
        is_boundary_input: true
        source: 市电（变电站A）
      
        equipment_parameters:
          cable_type: 高压电缆（YJV22-10kV）
          cable_size: {value: "3×240", unit: "mm²"}
          cable_route: 直埋/电缆沟
          cable_length: {value: 500, unit: m, note: "典型值"}
          arrester: 避雷器
          potential_transformer: 电压互感器
          current_transformer: 电流互感器
      
        control_points:
          sensors:
            - point_id: UTILITY1_V_A
              point_name: A相电压
              point_type: AI
              unit: kV
              range: [0, 12]
            - point_id: UTILITY1_V_B
              point_name: B相电压
              point_type: AI
              unit: kV
            - point_id: UTILITY1_V_C
              point_name: C相电压
              point_type: AI
              unit: kV
            - point_id: UTILITY1_I_A
              point_name: A相电流
              point_type: AI
              unit: A
              range: [0, 1000]
            - point_id: UTILITY1_P
              point_name: 有功功率
              point_type: AI
              unit: kW
            - point_id: UTILITY1_Q
              point_name: 无功功率
              point_type: AI
              unit: kvar
            - point_id: UTILITY1_PF
              point_name: 功率因数
              point_type: AI
              range: [0, 1]
            - point_id: UTILITY1_FREQ
              point_name: 频率
              point_type: AI
              unit: Hz
              range: [45, 55]
          status:
            - point_id: UTILITY1_AVAILABLE
              point_name: 一路电源正常
              point_type: DI
            - point_id: UTILITY1_FAULT
              point_name: 一路电源故障
              point_type: DI
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 10kV配电室
          floor: B1/1F
          position: 进线柜

      - node_id: ELEC-HV_SRC_UTILITY_2
        node_name: 市电二路进线
        node_name_en: Utility Power Incoming Line 2
        node_type: Source_Node
        node_category: SRC
      
        function: 接收市电二路10kV电源
        medium_in: ELEC-HV
        medium_out: ELEC-HV
      
        is_boundary_input: true
        source: 市电（变电站B）
      
        equipment_parameters:
          cable_type: 高压电缆（YJV22-10kV）
          cable_size: {value: "3×240", unit: "mm²"}
          cable_route: 直埋/电缆沟
      
        control_points:
          sensors:
            - point_id: UTILITY2_V_A
              point_name: A相电压
              point_type: AI
              unit: kV
            - point_id: UTILITY2_I_A
              point_name: A相电流
              point_type: AI
              unit: A
            - point_id: UTILITY2_P
              point_name: 有功功率
              point_type: AI
              unit: kW
          status:
            - point_id: UTILITY2_AVAILABLE
              point_name: 二路电源正常
              point_type: DI
            - point_id: UTILITY2_FAULT
              point_name: 二路电源故障
              point_type: DI
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 10kV配电室
          floor: B1/1F
          position: 进线柜

    # ========================================
    # Distribution Nodes - 配电节点
    # ========================================
    distribution_nodes:
  
      - node_id: ELEC-HV_DST_INCOMER_1
        node_name: 高压进线柜1
        node_name_en: HV Incomer Panel 1
        node_type: Distribution_Node
        node_subtype: SWG
        node_category: DST
      
        function: 一路市电进线开关及保护
        medium_in: ELEC-HV
        medium_out: ELEC-HV
      
        equipment_parameters:
          type: 高压开关柜（KYN28A-12）
          rated_voltage: {value: 12, unit: kV}
          rated_current: {value: 1250, unit: A}
          breaking_capacity: {value: 31.5, unit: kA}
          switch_type: 真空断路器
          protection_relay: 微机综合保护
          pt_ratio: "10000/100V"
          ct_ratio: "600/5A"
      
        control_points:
          status:
            - point_id: INCOMER1_CB_ON
              point_name: 断路器合闸状态
              point_type: DI
            - point_id: INCOMER1_CB_OFF
              point_name: 断路器分闸状态
              point_type: DI
            - point_id: INCOMER1_FAULT
              point_name: 保护动作
              point_type: DI
            - point_id: INCOMER1_READY
              point_name: 合闸就绪
              point_type: DI
          commands:
            - point_id: INCOMER1_CB_CLOSE
              point_name: 合闸命令
              point_type: DO
            - point_id: INCOMER1_CB_OPEN
              point_name: 分闸命令
              point_type: DO
      
        protection_settings:
          overcurrent: {setting: 600, unit: A, delay: 0.5, unit_delay: s}
          short_circuit: {setting: 3000, unit: A, delay: 0, note: "瞬时"}
          ground_fault: {setting: 10, unit: A, delay: 0.5, unit_delay: s}
          undervoltage: {setting: 70, unit: "%", delay: 2, unit_delay: s}
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 10kV配电室
          position: 进线柜区

      - node_id: ELEC-HV_DST_INCOMER_2
        node_name: 高压进线柜2
        node_name_en: HV Incomer Panel 2
        node_type: Distribution_Node
        node_subtype: SWG
        node_category: DST
      
        function: 二路市电进线开关及保护
        medium_in: ELEC-HV
        medium_out: ELEC-HV
      
        equipment_parameters:
          type: 高压开关柜（KYN28A-12）
          rated_voltage: {value: 12, unit: kV}
          rated_current: {value: 1250, unit: A}
          breaking_capacity: {value: 31.5, unit: kA}
          switch_type: 真空断路器
      
        control_points:
          status:
            - point_id: INCOMER2_CB_ON
              point_name: 断路器合闸状态
              point_type: DI
            - point_id: INCOMER2_CB_OFF
              point_name: 断路器分闸状态
              point_type: DI
            - point_id: INCOMER2_FAULT
              point_name: 保护动作
              point_type: DI
          commands:
            - point_id: INCOMER2_CB_CLOSE
              point_name: 合闸命令
              point_type: DO
            - point_id: INCOMER2_CB_OPEN
              point_name: 分闸命令
              point_type: DO
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 10kV配电室
          position: 进线柜区

      - node_id: ELEC-HV_DST_TIE_BREAKER
        node_name: 高压母联柜
        node_name_en: HV Bus Tie Panel
        node_type: Distribution_Node
        node_subtype: SWG
        node_category: DST
      
        function: 两段高压母线联络开关
        medium_in: ELEC-HV
        medium_out: ELEC-HV
      
        equipment_parameters:
          type: 高压开关柜（KYN28A-12）
          rated_voltage: {value: 12, unit: kV}
          rated_current: {value: 1250, unit: A}
          breaking_capacity: {value: 31.5, unit: kA}
          switch_type: 真空断路器
          interlock: 与两路进线电气/机械联锁
      
        control_points:
          status:
            - point_id: TIE_CB_ON
              point_name: 母联断路器合闸状态
              point_type: DI
            - point_id: TIE_CB_OFF
              point_name: 母联断路器分闸状态
              point_type: DI
            - point_id: TIE_INTERLOCK_OK
              point_name: 联锁条件满足
              point_type: DI
          commands:
            - point_id: TIE_CB_CLOSE
              point_name: 合闸命令
              point_type: DO
            - point_id: TIE_CB_OPEN
              point_name: 分闸命令
              point_type: DO
      
        operation_mode:
          normal: |
            两路进线均正常时，母联断开
            一段母线由一路进线供电
            二段母线由二路进线供电
          backup: |
            一路进线故障时，自动合母联
            由另一路进线带全部负荷
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 10kV配电室
          position: 两段母线之间

      - node_id: ELEC-HV_DST_BUS_1
        node_name: 高压一段母线
        node_name_en: HV Bus Section 1
        node_type: Distribution_Node
        node_subtype: BUS
        node_category: DST
      
        function: 高压一段母线
        medium_in: ELEC-HV
        medium_out: ELEC-HV
      
        equipment_parameters:
          type: 矩形铜母排
          rated_voltage: {value: 12, unit: kV}
          rated_current: {value: 1250, unit: A}
          bus_size: "60×10mm"
          insulation: 热缩套管
          color_coding: 黄/绿/红（A/B/C相）
      
        connected_feeders:
          - ELEC-HV_DST_FEEDER_T1
          - ELEC-HV_DST_FEEDER_T2
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 10kV配电室
          position: 开关柜顶部母线室

      - node_id: ELEC-HV_DST_BUS_2
        node_name: 高压二段母线
        node_name_en: HV Bus Section 2
        node_type: Distribution_Node
        node_subtype: BUS
        node_category: DST
      
        function: 高压二段母线
        medium_in: ELEC-HV
        medium_out: ELEC-HV
      
        equipment_parameters:
          type: 矩形铜母排
          rated_voltage: {value: 12, unit: kV}
          rated_current: {value: 1250, unit: A}
      
        connected_feeders:
          - ELEC-HV_DST_FEEDER_T3
          - ELEC-HV_DST_FEEDER_T4
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 10kV配电室

      - node_id: ELEC-HV_DST_FEEDER_T1
        node_name: 变压器1馈线柜
        node_name_en: Transformer 1 Feeder Panel
        node_type: Distribution_Node
        node_subtype: SWG
        node_category: DST
      
        function: 1#变压器高压侧进线开关
        medium_in: ELEC-HV
        medium_out: ELEC-HV
      
        multiplicity: single
        instance_pattern: ELEC-HV_DST_FEEDER_T{N}
      
        equipment_parameters:
          type: 高压开关柜（KYN28A-12）
          rated_voltage: {value: 12, unit: kV}
          rated_current: {value: 630, unit: A}
          breaking_capacity: {value: 31.5, unit: kA}
          switch_type: 真空断路器
          protection_relay: 变压器保护（差动、速断、过流、零序）
      
        control_points:
          status:
            - point_id: FEEDER_T1_CB_ON
              point_name: 断路器合闸状态
              point_type: DI
            - point_id: FEEDER_T1_CB_OFF
              point_name: 断路器分闸状态
              point_type: DI
            - point_id: FEEDER_T1_FAULT
              point_name: 保护动作
              point_type: DI
          commands:
            - point_id: FEEDER_T1_CB_CLOSE
              point_name: 合闸命令
              point_type: DO
            - point_id: FEEDER_T1_CB_OPEN
              point_name: 分闸命令
              point_type: DO
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 10kV配电室
          position: 馈线柜区

      - node_id: ELEC-HV_DST_FEEDER_T2
        node_name: 变压器2馈线柜
        node_name_en: Transformer 2 Feeder Panel
        node_type: Distribution_Node
        node_subtype: SWG
        node_category: DST
      
        function: 2#变压器高压侧进线开关
        medium_in: ELEC-HV
        medium_out: ELEC-HV
      
        equipment_parameters:
          type: 高压开关柜（KYN28A-12）
          rated_voltage: {value: 12, unit: kV}
          rated_current: {value: 630, unit: A}
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 10kV配电室

      - node_id: ELEC-HV_DST_FEEDER_T3
        node_name: 变压器3馈线柜
        node_name_en: Transformer 3 Feeder Panel
        node_type: Distribution_Node
        node_subtype: SWG
        node_category: DST
      
        function: 3#变压器高压侧进线开关
        medium_in: ELEC-HV
        medium_out: ELEC-HV
      
        equipment_parameters:
          type: 高压开关柜（KYN28A-12）
          rated_voltage: {value: 12, unit: kV}
          rated_current: {value: 630, unit: A}
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 10kV配电室

      - node_id: ELEC-HV_DST_FEEDER_T4
        node_name: 变压器4馈线柜
        node_name_en: Transformer 4 Feeder Panel
        node_type: Distribution_Node
        node_subtype: SWG
        node_category: DST
      
        function: 4#变压器高压侧进线开关
        medium_in: ELEC-HV
        medium_out: ELEC-HV
      
        equipment_parameters:
          type: 高压开关柜（KYN28A-12）
          rated_voltage: {value: 12, unit: kV}
          rated_current: {value: 630, unit: A}
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 10kV配电室

      - node_id: ELEC-HV_DST_PT_CABINET
        node_name: 高压计量柜
        node_name_en: HV Metering Panel
        node_type: Distribution_Node
        node_subtype: MET
        node_category: DST
      
        function: 高压电能计量及电压测量
        medium_in: ELEC-HV
        medium_out: SIGNAL
      
        equipment_parameters:
          type: 高压计量柜
          pt_ratio: "10000/100V"
          ct_ratio: "按实际配置"
          meter_class: 0.5级
          meter_type: 多功能电力仪表
      
        control_points:
          sensors:
            - point_id: HV_ENERGY_IMPORT
              point_name: 进口有功电能
              point_type: AI
              unit: kWh
            - point_id: HV_ENERGY_EXPORT
              point_name: 出口有功电能
              point_type: AI
              unit: kWh
            - point_id: HV_DEMAND_MAX
              point_name: 最大需量
              point_type: AI
              unit: kW
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 10kV配电室

    # ========================================
    # Sink Nodes - 输出节点
    # ========================================
    sink_nodes:
  
      - node_id: ELEC-HV_SNK_TRANSFORMER_1
        node_name: 1#变压器高压接口
        node_name_en: Transformer 1 HV Connection
        node_type: Sink_Node
        node_category: SNK
      
        function: 连接至1#变压器高压侧
        medium_in: ELEC-HV
        medium_out: ELEC-HV
      
        is_boundary_output: true
        target_system: ELEC-LV-MAIN
        target_node: ELEC-LV-MAIN_SRC_TRANSFORMER_1
      
        equipment_parameters:
          cable_type: 高压电缆
          cable_size: "3×120mm²"
          termination: 热缩终端头
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 变压器室
          position: 1#变压器高压侧

      - node_id: ELEC-HV_SNK_TRANSFORMER_2
        node_name: 2#变压器高压接口
        node_name_en: Transformer 2 HV Connection
        node_type: Sink_Node
        node_category: SNK
      
        function: 连接至2#变压器高压侧
        medium_in: ELEC-HV
        medium_out: ELEC-HV
      
        is_boundary_output: true
        target_system: ELEC-LV-MAIN
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 变压器室

      - node_id: ELEC-HV_SNK_TRANSFORMER_3
        node_name: 3#变压器高压接口
        node_name_en: Transformer 3 HV Connection
        node_type: Sink_Node
        node_category: SNK
      
        function: 连接至3#变压器高压侧
        medium_in: ELEC-HV
        medium_out: ELEC-HV
      
        is_boundary_output: true
        target_system: ELEC-LV-MAIN
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 变压器室

      - node_id: ELEC-HV_SNK_TRANSFORMER_4
        node_name: 4#变压器高压接口
        node_name_en: Transformer 4 HV Connection
        node_type: Sink_Node
        node_category: SNK
      
        function: 连接至4#变压器高压侧
        medium_in: ELEC-HV
        medium_out: ELEC-HV
      
        is_boundary_output: true
        target_system: ELEC-LV-MAIN
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 变压器室

  # ========================================
  # EDGES SECTION - 边/连接定义
  # ========================================
  edges:

    incoming_edges:
  
      - edge_id: ELEC-HV_EDGE_001
        edge_name: 一路进线电缆
        edge_type: CAB
        from_node: ELEC-HV_SRC_UTILITY_1
        to_node: ELEC-HV_DST_INCOMER_1
        direction: unidirectional
        medium: ELEC-HV
        cable_parameters:
          type: YJV22-10kV
          size: "3×240mm²"
          length: {value: 500, unit: m}
          laying: 电缆沟/直埋
      
      - edge_id: ELEC-HV_EDGE_002
        edge_name: 二路进线电缆
        edge_type: CAB
        from_node: ELEC-HV_SRC_UTILITY_2
        to_node: ELEC-HV_DST_INCOMER_2
        direction: unidirectional
        medium: ELEC-HV
        cable_parameters:
          type: YJV22-10kV
          size: "3×240mm²"
          length: {value: 500, unit: m}

    bus_edges:
  
      - edge_id: ELEC-HV_EDGE_011
        edge_name: 进线柜1至一段母线
        edge_type: BUS
        from_node: ELEC-HV_DST_INCOMER_1
        to_node: ELEC-HV_DST_BUS_1
        direction: unidirectional
        medium: ELEC-HV
      
      - edge_id: ELEC-HV_EDGE_012
        edge_name: 进线柜2至二段母线
        edge_type: BUS
        from_node: ELEC-HV_DST_INCOMER_2
        to_node: ELEC-HV_DST_BUS_2
        direction: unidirectional
        medium: ELEC-HV
      
      - edge_id: ELEC-HV_EDGE_013
        edge_name: 一段母线至母联
        edge_type: BUS
        from_node: ELEC-HV_DST_BUS_1
        to_node: ELEC-HV_DST_TIE_BREAKER
        direction: bidirectional
        medium: ELEC-HV
      
      - edge_id: ELEC-HV_EDGE_014
        edge_name: 二段母线至母联
        edge_type: BUS
        from_node: ELEC-HV_DST_BUS_2
        to_node: ELEC-HV_DST_TIE_BREAKER
        direction: bidirectional
        medium: ELEC-HV

    feeder_edges:
  
      - edge_id: ELEC-HV_EDGE_021
        edge_name: 一段母线至T1馈线
        edge_type: BUS
        from_node: ELEC-HV_DST_BUS_1
        to_node: ELEC-HV_DST_FEEDER_T1
        direction: unidirectional
        medium: ELEC-HV
      
      - edge_id: ELEC-HV_EDGE_022
        edge_name: 一段母线至T2馈线
        edge_type: BUS
        from_node: ELEC-HV_DST_BUS_1
        to_node: ELEC-HV_DST_FEEDER_T2
        direction: unidirectional
        medium: ELEC-HV
      
      - edge_id: ELEC-HV_EDGE_023
        edge_name: 二段母线至T3馈线
        edge_type: BUS
        from_node: ELEC-HV_DST_BUS_2
        to_node: ELEC-HV_DST_FEEDER_T3
        direction: unidirectional
        medium: ELEC-HV
      
      - edge_id: ELEC-HV_EDGE_024
        edge_name: 二段母线至T4馈线
        edge_type: BUS
        from_node: ELEC-HV_DST_BUS_2
        to_node: ELEC-HV_DST_FEEDER_T4
        direction: unidirectional
        medium: ELEC-HV

    transformer_edges:
  
      - edge_id: ELEC-HV_EDGE_031
        edge_name: T1馈线至变压器1
        edge_type: CAB
        from_node: ELEC-HV_DST_FEEDER_T1
        to_node: ELEC-HV_SNK_TRANSFORMER_1
        direction: unidirectional
        medium: ELEC-HV
        cable_parameters:
          type: YJV22-10kV
          size: "3×120mm²"
          length: {value: 30, unit: m}
      
      - edge_id: ELEC-HV_EDGE_032
        edge_name: T2馈线至变压器2
        edge_type: CAB
        from_node: ELEC-HV_DST_FEEDER_T2
        to_node: ELEC-HV_SNK_TRANSFORMER_2
        direction: unidirectional
        medium: ELEC-HV
      
      - edge_id: ELEC-HV_EDGE_033
        edge_name: T3馈线至变压器3
        edge_type: CAB
        from_node: ELEC-HV_DST_FEEDER_T3
        to_node: ELEC-HV_SNK_TRANSFORMER_3
        direction: unidirectional
        medium: ELEC-HV
      
      - edge_id: ELEC-HV_EDGE_034
        edge_name: T4馈线至变压器4
        edge_type: CAB
        from_node: ELEC-HV_DST_FEEDER_T4
        to_node: ELEC-HV_SNK_TRANSFORMER_4
        direction: unidirectional
        medium: ELEC-HV

  # ========================================
  # TYPICAL PATHS SECTION - 典型路径
  # ========================================
  typical_paths:

    - path_id: ELEC-HV_PATH_NORMAL_1
      path_name: 一路供电正常路径
      path_type: SUP
      description: 一路市电经一段母线供电至1#、2#变压器
      sequence:
        - step: 1
          node: ELEC-HV_SRC_UTILITY_1
          action: 10kV市电一路进线
        - step: 2
          node: ELEC-HV_DST_INCOMER_1
          action: 进线开关（合闸）
        - step: 3
          node: ELEC-HV_DST_BUS_1
          action: 一段母线配电
        - step: 4
          node: ELEC-HV_DST_FEEDER_T1 / ELEC-HV_DST_FEEDER_T2
          action: 变压器馈线开关
        - step: 5
          node: ELEC-HV_SNK_TRANSFORMER_1 / ELEC-HV_SNK_TRANSFORMER_2
          action: 供电至变压器
      operating_conditions:
        mode: 正常运行
        utility1_status: 正常
        tie_breaker: 分闸

    - path_id: ELEC-HV_PATH_NORMAL_2
      path_name: 二路供电正常路径
      path_type: SUP
      description: 二路市电经二段母线供电至3#、4#变压器
      sequence:
        - step: 1
          node: ELEC-HV_SRC_UTILITY_2
          action: 10kV市电二路进线
        - step: 2
          node: ELEC-HV_DST_INCOMER_2
          action: 进线开关（合闸）
        - step: 3
          node: ELEC-HV_DST_BUS_2
          action: 二段母线配电
        - step: 4
          node: ELEC-HV_DST_FEEDER_T3 / ELEC-HV_DST_FEEDER_T4
          action: 变压器馈线开关
        - step: 5
          node: ELEC-HV_SNK_TRANSFORMER_3 / ELEC-HV_SNK_TRANSFORMER_4
          action: 供电至变压器

    - path_id: ELEC-HV_PATH_BACKUP
      path_name: 备用供电路径（一路故障）
      path_type: BKP
      description: 一路故障时，二路经母联带全部负荷
      sequence:
        - step: 1
          node: ELEC-HV_SRC_UTILITY_2
          action: 10kV市电二路进线
        - step: 2
          node: ELEC-HV_DST_INCOMER_2
          action: 进线开关（合闸）
        - step: 3
          node: ELEC-HV_DST_BUS_2
          action: 二段母线
        - step: 4
          node: ELEC-HV_DST_TIE_BREAKER
          action: 母联开关（自动合闸）
        - step: 5
          node: ELEC-HV_DST_BUS_1
          action: 一段母线（由二路供电）
        - step: 6
          node: ELEC-HV_DST_FEEDER_T1 / ELEC-HV_DST_FEEDER_T2
          action: 变压器馈线开关
        - step: 7
          node: ELEC-HV_SNK_TRANSFORMER_1 / ELEC-HV_SNK_TRANSFORMER_2
          action: 供电至变压器
      trigger_conditions:
        - 一路进线电压<70%额定值持续2秒
        - 一路进线故障保护动作
      switching_time: "<3秒（自动切换）"

  # ========================================
  # LOOPS SECTION - 回路定义
  # ========================================
  loops:

    - loop_id: ELEC-HV_LOOP_BUS1
      loop_name: 一段母线供电回路
      loop_type: 高压配电回路
      nodes_in_loop:
        - ELEC-HV_SRC_UTILITY_1
        - ELEC-HV_DST_INCOMER_1
        - ELEC-HV_DST_BUS_1
        - ELEC-HV_DST_FEEDER_T1
        - ELEC-HV_DST_FEEDER_T2
        - ELEC-HV_SNK_TRANSFORMER_1
        - ELEC-HV_SNK_TRANSFORMER_2
      normal_source: ELEC-HV_SRC_UTILITY_1
      backup_source: ELEC-HV_SRC_UTILITY_2（经母联）

    - loop_id: ELEC-HV_LOOP_BUS2
      loop_name: 二段母线供电回路
      loop_type: 高压配电回路
      nodes_in_loop:
        - ELEC-HV_SRC_UTILITY_2
        - ELEC-HV_DST_INCOMER_2
        - ELEC-HV_DST_BUS_2
        - ELEC-HV_DST_FEEDER_T3
        - ELEC-HV_DST_FEEDER_T4
        - ELEC-HV_SNK_TRANSFORMER_3
        - ELEC-HV_SNK_TRANSFORMER_4
      normal_source: ELEC-HV_SRC_UTILITY_2
      backup_source: ELEC-HV_SRC_UTILITY_1（经母联）

  # ========================================
  # CONTROL LOGIC SECTION - 控制逻辑
  # ========================================
  control_logic:

    auto_transfer_switch:
      name: 高压自动切换（ATS）
      description: 双路进线自动切换逻辑
    
      normal_operation:
        description: 正常运行模式
        logic: |
          1. 两路进线分列运行
          2. 进线1供一段母线，进线2供二段母线
          3. 母联断路器保持分闸
          4. 两路进线互为备用
    
      utility1_failure:
        description: 一路失电切换
        trigger:
          - 一路电压<70%额定值持续2秒
          - 或一路保护动作跳闸
        sequence:
          - step: 1
            action: 检测一路失电
            delay: 2s
          - step: 2
            action: 分闸进线1断路器
            delay: 0.5s
          - step: 3
            action: 确认一段母线失压
            delay: 0.3s
          - step: 4
            action: 合闸母联断路器
            delay: 0.5s
            condition: 二路电源正常
          - step: 5
            action: 一段母线恢复供电
            note: 由二路电源经母联供电
        total_time: "<3.5秒"
    
      utility1_recovery:
        description: 一路恢复切换
        trigger: 一路电压恢复正常持续30秒
        sequence:
          - step: 1
            action: 确认一路电压正常
            delay: 30s
          - step: 2
            action: 分闸母联断路器
            delay: 0.5s
          - step: 3
            action: 合闸进线1断路器
            delay: 0.5s
          - step: 4
            action: 恢复分列运行
        mode: 手动/自动可选
    
      interlock_logic:
        description: 联锁逻辑
        rules:
          - rule: "进线1合闸 + 进线2合闸 → 母联必须分闸"
            note: 防止环网
          - rule: "母联合闸 → 只能有一路进线合闸"
          - rule: "任一断路器操作前检查联锁条件"

    protection_coordination:
      name: 保护配合
      description: 高压保护定值配合
    
      settings:
        incomer_overcurrent:
          pickup: "1.2×变压器额定电流之和"
          time: 0.5s
          note: 后备保护
        feeder_overcurrent:
          pickup: "1.2×单台变压器额定电流"
          time: 0.3s
          note: 主保护
        short_circuit:
          pickup: "按短路电流计算"
          time: 瞬时
          note: 速断保护
    
      coordination_principle: |
        1. 下级保护动作时间 < 上级保护动作时间
        2. 馈线保护先动作，进线保护后备
        3. 母联保护应与两段母线保护配合

  # ========================================
  # ALARM & PROTECTION SECTION
  # ========================================
  alarm_protection:
  
    critical_alarms:
      - alarm_id: ALM_HV_UTILITY1_FAIL
        alarm_name: 一路市电故障
        severity: CRITICAL
        trigger: UTILITY1_FAULT = ON 或 UTILITY1_V < 7kV
        action: 自动切换至二路供电
      
      - alarm_id: ALM_HV_UTILITY2_FAIL
        alarm_name: 二路市电故障
        severity: CRITICAL
        trigger: UTILITY2_FAULT = ON 或 UTILITY2_V < 7kV
        action: 自动切换至一路供电
      
      - alarm_id: ALM_HV_BOTH_FAIL
        alarm_name: 双路市电全失
        severity: EMERGENCY
        trigger: 两路进线均失电
        action: 启动柴油发电机
      
      - alarm_id: ALM_HV_PROTECTION_TRIP
        alarm_name: 高压保护动作
        severity: HIGH
        trigger: 任一断路器保护跳闸
        action: 隔离故障点，记录保护动作信息

  # ========================================
  # DEPENDENCIES SECTION
  # ========================================
  dependencies:
  
    upstream_dependencies:
      - dependency_id: DEP_UTILITY
        from_system: EXTERNAL_UTILITY
        dependency_type: POWER_SUPPLY
        criticality: CRITICAL
        description: 外部市电供应
        failure_impact: 需切换备用电源或启动发电机
      
    downstream_dependencies:
      - dependency_id: DEP_LV_MAIN
        to_system: ELEC-LV-MAIN
        dependency_type: POWER_SUPPLY
        criticality: CRITICAL
        description: 向低压系统供电
      
      - dependency_id: DEP_EPS_TRIGGER
        to_system: ELEC-EPS
        dependency_type: TRIGGER_SIGNAL
        criticality: CRITICAL
        description: 双路失电触发发电机启动
```

---

## 系统 2.2: ELEC-LV-MAIN 低压配电主系统

```yaml
System_Topology:

  identity:
    system_id: ELEC-LV-MAIN
    system_name: 低压配电主系统
    system_name_en: Low Voltage Main Distribution System
    system_category: ELEC
    system_type: 低压配电
    priority_level: P0-LIFE_SAFETY
  
    description: |
      医院低压配电主系统，接收变压器输出的0.4kV电源，通过低压配电柜向全院各用电设备供电。
      系统设置多段母线，分别供应一般负荷、重要负荷和特别重要负荷（接应急电源）。
      低压系统是医院电力分配的核心，负责向所有终端负荷提供可靠电源。
  
    design_basis:
      voltage_level: {value: 380/220, unit: V}
      system_frequency: {value: 50, unit: Hz}
      neutral_system: TN-S
      short_circuit_current: {value: 50, unit: kA, note: "母线短路电流"}
      load_categories:
        - category: 一级负荷（特别重要）
          description: 手术室、ICU、急诊抢救等
          backup: 双电源+UPS+柴发
        - category: 一级负荷
          description: 重要医疗设备、电梯等
          backup: 双电源+柴发
        - category: 二级负荷
          description: 一般医疗区域
          backup: 双电源
        - category: 三级负荷
          description: 办公、后勤等
          backup: 单电源
  
    parent_system: ELEC-HV
    child_systems:
      - ELEC-LV-FLOOR    # 楼层配电
      - ELEC-EPS         # 应急电源
      - ELEC-UPS         # 不间断电源
  
    design_standards:
      - GB 50054-2011 低压配电设计规范
      - GB 51348-2019 民用建筑电气设计标准
      - JGJ 312-2013 医疗建筑电气设计规范
      - IEC 60364 低压电气装置
  
    version: 1.0
    last_updated: 2024

  boundary:
    inputs:
      - boundary_id: ELEC-LV_IN_001
        name: 变压器低压输出
        from_system: ELEC-HV
        from_node: ELEC-HV_SNK_TRANSFORMER
        medium: ELEC-LV
        parameters:
          voltage: {value: 400, unit: V}
        
      - boundary_id: ELEC-LV_IN_002
        name: 柴油发电机输出
        from_system: ELEC-EPS
        from_node: ELEC-EPS_SNK_LV_OUTPUT
        medium: ELEC-LV
        parameters:
          voltage: {value: 400, unit: V}
        
    outputs:
      - boundary_id: ELEC-LV_OUT_001
        name: 楼层配电输出
        to_system: ELEC-LV-FLOOR
        medium: ELEC-LV
      
      - boundary_id: ELEC-LV_OUT_002
        name: 动力设备配电
        to_system: HVAC/PLUMB/ELEV
        medium: ELEC-LV
      
      - boundary_id: ELEC-LV_OUT_003
        name: UPS输入电源
        to_system: ELEC-UPS
        medium: ELEC-LV

  nodes:

    source_nodes:
  
      - node_id: ELEC-LV-MAIN_SRC_TRANSFORMER_1
        node_name: 1#干式变压器
        node_name_en: Dry-Type Transformer 1
        node_type: Source_Node
        node_category: SRC
      
        function: 10kV/0.4kV电压变换
        medium_in: ELEC-HV
        medium_out: ELEC-LV
      
        equipment_parameters:
          type: 干式变压器（SCB13）
          capacity: {value: 2000, unit: kVA}
          voltage_ratio: "10/0.4kV"
          vector_group: Dyn11
          impedance: {value: 6, unit: "%"}
          efficiency: ">99%"
          insulation_class: H级
          cooling: AN（自然风冷）/AF（强迫风冷）
          noise_level: {value: "<55", unit: "dB(A)"}
          temperature_rise: {value: 100, unit: K, note: "H级绝缘"}
      
        control_points:
          sensors:
            - point_id: TX1_TEMP_A
              point_name: A相绕组温度
              point_type: AI
              unit: ℃
              range: [0, 180]
            - point_id: TX1_TEMP_B
              point_name: B相绕组温度
              point_type: AI
              unit: ℃
            - point_id: TX1_TEMP_C
              point_name: C相绕组温度
              point_type: AI
              unit: ℃
            - point_id: TX1_LOAD
              point_name: 变压器负载率
              point_type: AI
              unit: "%"
              range: [0, 150]
          status:
            - point_id: TX1_OVERTEMP
              point_name: 超温报警
              point_type: DI
            - point_id: TX1_FAN_RUN
              point_name: 冷却风机运行
              point_type: DI
          commands:
            - point_id: TX1_FAN_CMD
              point_name: 冷却风机启停
              point_type: DO
      
        protection_settings:
          overtemperature_alarm: {value: 130, unit: ℃}
          overtemperature_trip: {value: 150, unit: ℃}
          fan_start_temp: {value: 100, unit: ℃}
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 变压器室
          floor: B1
          area_requirement: {value: ">30", unit: "m²/台"}
          ventilation: 自然通风或机械通风
      
        installation_requirements:
          - 干式变压器室独立设置
          - 防火门（甲级）
          - 通风散热设施
          - 安全距离符合规范
          - 接地系统可靠

      - node_id: ELEC-LV-MAIN_SRC_TRANSFORMER_2
        node_name: 2#干式变压器
        node_name_en: Dry-Type Transformer 2
        node_type: Source_Node
        node_category: SRC
        function: 10kV/0.4kV电压变换
        medium_in: ELEC-HV
        medium_out: ELEC-LV
        equipment_parameters:
          type: 干式变压器（SCB13）
          capacity: {value: 2000, unit: kVA}
          voltage_ratio: "10/0.4kV"
        location_hint:
          space_type: MEP_ROOM
          room_name: 变压器室

      - node_id: ELEC-LV-MAIN_SRC_TRANSFORMER_3
        node_name: 3#干式变压器
        node_name_en: Dry-Type Transformer 3
        node_type: Source_Node
        node_category: SRC
        function: 10kV/0.4kV电压变换
        medium_in: ELEC-HV
        medium_out: ELEC-LV
        equipment_parameters:
          type: 干式变压器（SCB13）
          capacity: {value: 2000, unit: kVA}
          voltage_ratio: "10/0.4kV"
        location_hint:
          space_type: MEP_ROOM
          room_name: 变压器室

      - node_id: ELEC-LV-MAIN_SRC_TRANSFORMER_4
        node_name: 4#干式变压器
        node_name_en: Dry-Type Transformer 4
        node_type: Source_Node
        node_category: SRC
        function: 10kV/0.4kV电压变换
        medium_in: ELEC-HV
        medium_out: ELEC-LV
        equipment_parameters:
          type: 干式变压器（SCB13）
          capacity: {value: 2000, unit: kVA}
          voltage_ratio: "10/0.4kV"
        location_hint:
          space_type: MEP_ROOM
          room_name: 变压器室

      - node_id: ELEC-LV-MAIN_SRC_GENERATOR
        node_name: 柴油发电机组
        node_name_en: Diesel Generator Set
        node_type: Source_Node
        node_category: SRC
      
        function: 应急电源供应
        medium_in: FUEL-DIESEL
        medium_out: ELEC-LV
      
        multiplicity: multiple
        instance_pattern: ELEC-LV-MAIN_SRC_GEN_{N}
        typical_configuration:
          quantity: 2
          redundancy: "N+1"
          parallel_operation: true
      
        equipment_parameters:
          type: 柴油发电机组
          prime_power: {value: 1600, unit: kW, note: "常用功率"}
          standby_power: {value: 2000, unit: kVA}
          voltage: {value: 400, unit: V}
          frequency: {value: 50, unit: Hz}
          power_factor: 0.8
          phases: 3
          engine_type: 柴油发动机
          fuel_consumption: {value: 280, unit: "L/h", note: "满载"}
          fuel_tank: {value: 1000, unit: L, note: "日用油箱"}
          cooling: 水冷
          starting_method: 电启动（双蓄电池）
          starting_time: {value: "<10", unit: s}
          load_acceptance: 
            step1: {load: 50, time: 0, unit: "%/s"}
            step2: {load: 80, time: 10, unit: "%/s"}
            step3: {load: 100, time: 20, unit: "%/s"}
          noise_level: {value: "<85", unit: "dB(A)@1m"}
          exhaust_emission: 符合国VI标准
      
        control_points:
          sensors:
            - point_id: GEN_V_A
              point_name: A相电压
              point_type: AI
              unit: V
              range: [0, 500]
            - point_id: GEN_I_A
              point_name: A相电流
              point_type: AI
              unit: A
              range: [0, 3000]
            - point_id: GEN_FREQ
              point_name: 频率
              point_type: AI
              unit: Hz
              range: [45, 55]
            - point_id: GEN_P
              point_name: 有功功率
              point_type: AI
              unit: kW
            - point_id: GEN_LOAD
              point_name: 负载率
              point_type: AI
              unit: "%"
            - point_id: GEN_FUEL_LEVEL
              point_name: 油位
              point_type: AI
              unit: "%"
            - point_id: GEN_COOLANT_TEMP
              point_name: 冷却液温度
              point_type: AI
              unit: ℃
            - point_id: GEN_OIL_PRESS
              point_name: 机油压力
              point_type: AI
              unit: kPa
            - point_id: GEN_SPEED
              point_name: 转速
              point_type: AI
              unit: rpm
          status:
            - point_id: GEN_READY
              point_name: 发电机就绪
              point_type: DI
            - point_id: GEN_RUN
              point_name: 发电机运行
              point_type: DI
            - point_id: GEN_FAULT
              point_name: 发电机故障
              point_type: DI
            - point_id: GEN_CB_ON
              point_name: 发电机出口开关合闸
              point_type: DI
            - point_id: GEN_AUTO_MODE
              point_name: 自动模式
              point_type: DI
          commands:
            - point_id: GEN_START_CMD
              point_name: 启动命令
              point_type: DO
            - point_id: GEN_STOP_CMD
              point_name: 停机命令
              point_type: DO
            - point_id: GEN_CB_CLOSE
              point_name: 出口开关合闸
              point_type: DO
            - point_id: GEN_CB_OPEN
              point_name: 出口开关分闸
              point_type: DO
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 柴油发电机房
          floor: B1/1F
          area_requirement: {value: ">100", unit: "m²"}
      
        installation_requirements:
          - 独立机房，防火分隔
          - 进排风系统
          - 排烟系统（室外排放）
          - 减振基础
          - 储油间（甲类）
          - 消防设施
          - 噪声控制

    distribution_nodes:
  
      - node_id: ELEC-LV-MAIN_DST_MCC_1
        node_name: 低压进线柜1
        node_name_en: LV Incomer Panel 1
        node_type: Distribution_Node
        node_subtype: SWG
        node_category: DST
      
        function: 1#变压器低压侧进线开关
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        equipment_parameters:
          type: 低压开关柜（GCS/GCK/MNS）
          rated_voltage: {value: 400, unit: V}
          rated_current: {value: 4000, unit: A}
          short_time_withstand: {value: 65, unit: kA, time: 1s}
          main_switch: 框架式断路器（ACB）
          protection: 电子脱扣器（三段保护）
      
        control_points:
          sensors:
            - point_id: MCC1_V
              point_name: 母线电压
              point_type: AI
              unit: V
            - point_id: MCC1_I
              point_name: 进线电流
              point_type: AI
              unit: A
            - point_id: MCC1_P
              point_name: 有功功率
              point_type: AI
              unit: kW
            - point_id: MCC1_PF
              point_name: 功率因数
              point_type: AI
          status:
            - point_id: MCC1_CB_ON
              point_name: 主开关合闸
              point_type: DI
            - point_id: MCC1_CB_OFF
              point_name: 主开关分闸
              point_type: DI
            - point_id: MCC1_FAULT
              point_name: 保护动作
              point_type: DI
          commands:
            - point_id: MCC1_CB_CLOSE
              point_name: 合闸命令
              point_type: DO
            - point_id: MCC1_CB_OPEN
              point_name: 分闸命令
              point_type: DO
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室
          floor: B1

      - node_id: ELEC-LV-MAIN_DST_MCC_2
        node_name: 低压进线柜2
        node_name_en: LV Incomer Panel 2
        node_type: Distribution_Node
        node_subtype: SWG
        node_category: DST
        function: 2#变压器低压侧进线开关
        medium_in: ELEC-LV
        medium_out: ELEC-LV
        equipment_parameters:
          type: 低压开关柜
          rated_current: {value: 4000, unit: A}
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室

      - node_id: ELEC-LV-MAIN_DST_MCC_3
        node_name: 低压进线柜3
        node_name_en: LV Incomer Panel 3
        node_type: Distribution_Node
        node_subtype: SWG
        node_category: DST
        function: 3#变压器低压侧进线开关
        medium_in: ELEC-LV
        medium_out: ELEC-LV
        equipment_parameters:
          type: 低压开关柜
          rated_current: {value: 4000, unit: A}
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室

      - node_id: ELEC-LV-MAIN_DST_MCC_4
        node_name: 低压进线柜4
        node_name_en: LV Incomer Panel 4
        node_type: Distribution_Node
        node_subtype: SWG
        node_category: DST
        function: 4#变压器低压侧进线开关
        medium_in: ELEC-LV
        medium_out: ELEC-LV
        equipment_parameters:
          type: 低压开关柜
          rated_current: {value: 4000, unit: A}
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室

      - node_id: ELEC-LV-MAIN_DST_GEN_PANEL
        node_name: 发电机进线柜
        node_name_en: Generator Incomer Panel
        node_type: Distribution_Node
        node_subtype: SWG
        node_category: DST
      
        function: 柴油发电机低压进线
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        equipment_parameters:
          type: 低压开关柜
          rated_current: {value: 4000, unit: A}
          ats_function: 与市电自动切换
      
        control_points:
          status:
            - point_id: GEN_PANEL_CB_ON
              point_name: 发电机开关合闸
              point_type: DI
            - point_id: GEN_PANEL_ATS_POS
              point_name: ATS位置（市电/发电）
              point_type: DI
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室

      - node_id: ELEC-LV-MAIN_DST_BUS_1
        node_name: 低压一段母线
        node_name_en: LV Bus Section 1
        node_type: Distribution_Node
        node_subtype: BUS
        node_category: DST
      
        function: 低压一段母线（一般负荷）
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        equipment_parameters:
          type: 铜母排
          rated_voltage: {value: 400, unit: V}
          rated_current: {value: 4000, unit: A}
          bus_size: "100×10mm×3"
      
        load_category: 二级/三级负荷
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室

      - node_id: ELEC-LV-MAIN_DST_BUS_2
        node_name: 低压二段母线
        node_name_en: LV Bus Section 2
        node_type: Distribution_Node
        node_subtype: BUS
        node_category: DST
        function: 低压二段母线（一般负荷）
        medium_in: ELEC-LV
        medium_out: ELEC-LV
        load_category: 二级/三级负荷
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室

      - node_id: ELEC-LV-MAIN_DST_BUS_E1
        node_name: 应急一段母线
        node_name_en: Emergency Bus Section 1
        node_type: Distribution_Node
        node_subtype: BUS
        node_category: DST
      
        function: 应急一段母线（重要负荷+发电机供电）
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        equipment_parameters:
          type: 铜母排
          rated_current: {value: 2500, unit: A}
      
        load_category: 一级负荷
        power_source:
          normal: 1#/2#变压器
          emergency: 柴油发电机
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室

      - node_id: ELEC-LV-MAIN_DST_BUS_E2
        node_name: 应急二段母线
        node_name_en: Emergency Bus Section 2
        node_type: Distribution_Node
        node_subtype: BUS
        node_category: DST
        function: 应急二段母线（重要负荷+发电机供电）
        medium_in: ELEC-LV
        medium_out: ELEC-LV
        load_category: 一级负荷
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室

      - node_id: ELEC-LV-MAIN_DST_TIE_1
        node_name: 低压母联柜1（一段-二段）
        node_name_en: LV Bus Tie Panel 1
        node_type: Distribution_Node
        node_subtype: SWG
        node_category: DST
      
        function: 一段与二段母线联络
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        equipment_parameters:
          type: 母联柜
          rated_current: {value: 2500, unit: A}
          switch_type: ACB
          interlock: 与进线开关联锁
      
        control_points:
          status:
            - point_id: TIE1_CB_ON
              point_name: 母联1合闸
              point_type: DI
            - point_id: TIE1_CB_OFF
              point_name: 母联1分闸
              point_type: DI
          commands:
            - point_id: TIE1_CB_CLOSE
              point_name: 合闸命令
              point_type: DO
            - point_id: TIE1_CB_OPEN
              point_name: 分闸命令
              point_type: DO
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室

      - node_id: ELEC-LV-MAIN_DST_TIE_E
        node_name: 应急母联柜
        node_name_en: Emergency Bus Tie Panel
        node_type: Distribution_Node
        node_subtype: SWG
        node_category: DST
        function: 应急一段与二段母线联络
        medium_in: ELEC-LV
        medium_out: ELEC-LV
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室

      - node_id: ELEC-LV-MAIN_DST_ATS_1
        node_name: 双电源切换柜1
        node_name_en: Automatic Transfer Switch 1
        node_type: Distribution_Node
        node_subtype: ATS
        node_category: DST
      
        function: 应急母线双电源自动切换
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        equipment_parameters:
          type: 双电源自动切换装置（ATSE）
          rated_current: {value: 2500, unit: A}
          transfer_type: PC级（自动切换）
          transfer_time: {value: "<3", unit: s, note: "常规切换"}
          withstand_current: {value: 65, unit: kA}
          interlock: 电气+机械双重联锁
      
        control_points:
          status:
            - point_id: ATS1_MAIN_ON
              point_name: 主电源开关合闸
              point_type: DI
            - point_id: ATS1_BACKUP_ON
              point_name: 备用电源开关合闸
              point_type: DI
            - point_id: ATS1_POS
              point_name: ATS位置（主/备）
              point_type: DI
            - point_id: ATS1_MAIN_AVAIL
              point_name: 主电源正常
              point_type: DI
            - point_id: ATS1_BACKUP_AVAIL
              point_name: 备用电源正常
              point_type: DI
          commands:
            - point_id: ATS1_TO_MAIN
              point_name: 切至主电源
              point_type: DO
            - point_id: ATS1_TO_BACKUP
              point_name: 切至备用电源
              point_type: DO
      
        switching_logic:
          main_to_backup:
            trigger: 主电源电压<85%额定值持续1秒
            action: 自动切换至备用电源
            time: <3s
          backup_to_main:
            trigger: 主电源恢复正常持续30秒
            action: 自动切回主电源
            mode: 可选自动/手动
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室

      # === 馈电柜（部分示例）===
      - node_id: ELEC-LV-MAIN_DST_FEEDER_HVAC
        node_name: 暖通动力配电柜
        node_name_en: HVAC Power Distribution Panel
        node_type: Distribution_Node
        node_subtype: MCC
        node_category: DST
      
        function: 暖通设备（冷水机组、水泵等）电源
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        equipment_parameters:
          type: 动力配电柜（MCC）
          rated_current: {value: 1000, unit: A}
          outgoing_circuits: 12-16路
          starter_type: 软启动/变频器
      
        served_equipment:
          - 冷水机组（3台，约500kW/台）
          - 冷冻水泵（4台，约45kW/台）
          - 冷却水泵（4台，约55kW/台）
          - 冷却塔风机（4台，约15kW/台）
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室
      
        downstream_system: HVAC-CHP

      - node_id: ELEC-LV-MAIN_DST_FEEDER_ELEV
        node_name: 电梯动力配电柜
        node_name_en: Elevator Power Distribution Panel
        node_type: Distribution_Node
        node_subtype: MCC
        node_category: DST
      
        function: 电梯电源
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        equipment_parameters:
          type: 动力配电柜
          rated_current: {value: 400, unit: A}
          outgoing_circuits: 8-12路
      
        served_equipment:
          - 客梯（8台）
          - 货梯（2台）
          - 消防电梯（2台）
      
        load_category: 一级负荷
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室

      - node_id: ELEC-LV-MAIN_DST_FEEDER_LIGHTING
        node_name: 照明总配电柜
        node_name_en: Lighting Main Distribution Panel
        node_type: Distribution_Node
        node_subtype: SWG
        node_category: DST
      
        function: 全院照明总配电
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        equipment_parameters:
          type: 照明配电柜
          rated_current: {value: 630, unit: A}
          outgoing_circuits: 16-24路
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室

      - node_id: ELEC-LV-MAIN_DST_FEEDER_UPS
        node_name: UPS输入配电柜
        node_name_en: UPS Input Distribution Panel
        node_type: Distribution_Node
        node_subtype: SWG
        node_category: DST
      
        function: UPS系统输入电源
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        equipment_parameters:
          type: 配电柜
          rated_current: {value: 400, unit: A}
      
        load_category: 一级负荷（特别重要）
        downstream_system: ELEC-UPS
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室

      - node_id: ELEC-LV-MAIN_DST_CAPACITOR
        node_name: 无功补偿柜
        node_name_en: Power Factor Correction Panel
        node_type: Distribution_Node
        node_subtype: PFC
        node_category: DST
      
        function: 无功功率补偿，提高功率因数
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        equipment_parameters:
          type: 自动无功补偿装置
          compensation_capacity: {value: 600, unit: kvar}
          compensation_steps: 12级
          capacitor_type: 低压干式电容器
          reactor: 7%串联电抗器（抑制谐波）
          controller: 智能无功补偿控制器
          target_pf: {value: ">0.95", note: "目标功率因数"}
      
        control_points:
          sensors:
            - point_id: PFC_PF
              point_name: 系统功率因数
              point_type: AI
              range: [0, 1]
            - point_id: PFC_Q
              point_name: 无功功率
              point_type: AI
              unit: kvar
            - point_id: PFC_STEPS
              point_name: 投入级数
              point_type: AI
          status:
            - point_id: PFC_FAULT
              point_name: 故障报警
              point_type: DI
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室

    sink_nodes:
  
      - node_id: ELEC-LV-MAIN_SNK_FLOOR_DB
        node_name: 楼层配电箱接口
        node_name_en: Floor Distribution Board Connection
        node_type: Sink_Node
        node_category: SNK
      
        function: 连接至各楼层配电箱
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        is_boundary_output: true
        target_system: ELEC-LV-FLOOR
      
        multiplicity: multiple
        instance_pattern: ELEC-LV-MAIN_SNK_FLOOR_DB_{Floor}
      
        location_hint:
          space_type: SHAFT
          shaft_type: 电气竖井

      - node_id: ELEC-LV-MAIN_SNK_HVAC
        node_name: 暖通设备接口
        node_name_en: HVAC Equipment Connection
        node_type: Sink_Node
        node_category: SNK
      
        function: 供电至暖通设备
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        is_boundary_output: true
        target_system: HVAC-CHP
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房

      - node_id: ELEC-LV-MAIN_SNK_ELEV
        node_name: 电梯设备接口
        node_name_en: Elevator Equipment Connection
        node_type: Sink_Node
        node_category: SNK
      
        function: 供电至电梯
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        is_boundary_output: true
        target_system: TRANS-ELEV
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 电梯机房

      - node_id: ELEC-LV-MAIN_SNK_UPS
        node_name: UPS设备接口
        node_name_en: UPS Equipment Connection
        node_type: Sink_Node
        node_category: SNK
      
        function: 供电至UPS系统
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        is_boundary_output: true
        target_system: ELEC-UPS
      
        location_hint:
          space_type: MEP_ROOM
          room_name: UPS机房

  edges:

    transformer_edges:
      - edge_id: ELEC-LV_EDGE_001
        edge_name: 1#变压器至进线柜1
        edge_type: CAB
        from_node: ELEC-LV-MAIN_SRC_TRANSFORMER_1
        to_node: ELEC-LV-MAIN_DST_MCC_1
        direction: unidirectional
        medium: ELEC-LV
        cable_parameters:
          type: 铜芯母线桥/电缆
          size: "3×(3×240)+2×120mm²"
          length: {value: 15, unit: m}
        
      - edge_id: ELEC-LV_EDGE_002
        edge_name: 2#变压器至进线柜2
        edge_type: CAB
        from_node: ELEC-LV-MAIN_SRC_TRANSFORMER_2
        to_node: ELEC-LV-MAIN_DST_MCC_2
        direction: unidirectional
        medium: ELEC-LV
      
      - edge_id: ELEC-LV_EDGE_003
        edge_name: 3#变压器至进线柜3
        edge_type: CAB
        from_node: ELEC-LV-MAIN_SRC_TRANSFORMER_3
        to_node: ELEC-LV-MAIN_DST_MCC_3
        direction: unidirectional
        medium: ELEC-LV
      
      - edge_id: ELEC-LV_EDGE_004
        edge_name: 4#变压器至进线柜4
        edge_type: CAB
        from_node: ELEC-LV-MAIN_SRC_TRANSFORMER_4
        to_node: ELEC-LV-MAIN_DST_MCC_4
        direction: unidirectional
        medium: ELEC-LV

    generator_edges:
      - edge_id: ELEC-LV_EDGE_011
        edge_name: 发电机至发电机柜
        edge_type: CAB
        from_node: ELEC-LV-MAIN_SRC_GENERATOR
        to_node: ELEC-LV-MAIN_DST_GEN_PANEL
        direction: unidirectional
        medium: ELEC-LV
        cable_parameters:
          type: 铜芯电缆（耐火）
          size: "3×(3×185)+2×95mm²"

    bus_edges:
      - edge_id: ELEC-LV_EDGE_021
        edge_name: 进线柜1至一段母线
        edge_type: BUS
        from_node: ELEC-LV-MAIN_DST_MCC_1
        to_node: ELEC-LV-MAIN_DST_BUS_1
        direction: unidirectional
        medium: ELEC-LV
      
      - edge_id: ELEC-LV_EDGE_022
        edge_name: 进线柜2至一段母线
        edge_type: BUS
        from_node: ELEC-LV-MAIN_DST_MCC_2
        to_node: ELEC-LV-MAIN_DST_BUS_1
        direction: unidirectional
        medium: ELEC-LV
        note: 双变压器供一段母线
      
      - edge_id: ELEC-LV_EDGE_023
        edge_name: 进线柜3至二段母线
        edge_type: BUS
        from_node: ELEC-LV-MAIN_DST_MCC_3
        to_node: ELEC-LV-MAIN_DST_BUS_2
        direction: unidirectional
        medium: ELEC-LV
      
      - edge_id: ELEC-LV_EDGE_024
        edge_name: 进线柜4至二段母线
        edge_type: BUS
        from_node: ELEC-LV-MAIN_DST_MCC_4
        to_node: ELEC-LV-MAIN_DST_BUS_2
        direction: unidirectional
        medium: ELEC-LV

    emergency_bus_edges:
      - edge_id: ELEC-LV_EDGE_031
        edge_name: 一段母线至ATS1
        edge_type: BUS
        from_node: ELEC-LV-MAIN_DST_BUS_1
        to_node: ELEC-LV-MAIN_DST_ATS_1
        direction: unidirectional
        medium: ELEC-LV
      
      - edge_id: ELEC-LV_EDGE_032
        edge_name: 发电机柜至ATS1
        edge_type: BUS
        from_node: ELEC-LV-MAIN_DST_GEN_PANEL
        to_node: ELEC-LV-MAIN_DST_ATS_1
        direction: unidirectional
        medium: ELEC-LV
      
      - edge_id: ELEC-LV_EDGE_033
        edge_name: ATS1至应急一段母线
        edge_type: BUS
        from_node: ELEC-LV-MAIN_DST_ATS_1
        to_node: ELEC-LV-MAIN_DST_BUS_E1
        direction: unidirectional
        medium: ELEC-LV

    feeder_edges:
      - edge_id: ELEC-LV_EDGE_041
        edge_name: 一段母线至暖通配电柜
        edge_type: CAB
        from_node: ELEC-LV-MAIN_DST_BUS_1
        to_node: ELEC-LV-MAIN_DST_FEEDER_HVAC
        direction: unidirectional
        medium: ELEC-LV
      
      - edge_id: ELEC-LV_EDGE_042
        edge_name: 应急母线至电梯配电柜
        edge_type: CAB
        from_node: ELEC-LV-MAIN_DST_BUS_E1
        to_node: ELEC-LV-MAIN_DST_FEEDER_ELEV
        direction: unidirectional
        medium: ELEC-LV
        note: 电梯接应急电源
      
      - edge_id: ELEC-LV_EDGE_043
        edge_name: 应急母线至UPS配电柜
        edge_type: CAB
        from_node: ELEC-LV-MAIN_DST_BUS_E1
        to_node: ELEC-LV-MAIN_DST_FEEDER_UPS
        direction: unidirectional
        medium: ELEC-LV

  typical_paths:

    - path_id: ELEC-LV_PATH_NORMAL
      path_name: 正常供电路径
      path_type: SUP
      description: 变压器至一般负荷的正常供电
      sequence:
        - step: 1
          node: ELEC-LV-MAIN_SRC_TRANSFORMER_1
          action: 10kV/0.4kV变压
        - step: 2
          node: ELEC-LV-MAIN_DST_MCC_1
          action: 进线开关
        - step: 3
          node: ELEC-LV-MAIN_DST_BUS_1
          action: 一段母线配电
        - step: 4
          node: ELEC-LV-MAIN_DST_FEEDER_HVAC
          action: 馈电至设备

    - path_id: ELEC-LV_PATH_EMERGENCY
      path_name: 应急供电路径（市电正常）
      path_type: SUP
      description: 市电正常时应急负荷的供电
      sequence:
        - step: 1
          node: ELEC-LV-MAIN_SRC_TRANSFORMER_1
          action: 变压器供电
        - step: 2
          node: ELEC-LV-MAIN_DST_MCC_1
          action: 进线开关
        - step: 3
          node: ELEC-LV-MAIN_DST_BUS_1
          action: 一段母线
        - step: 4
          node: ELEC-LV-MAIN_DST_ATS_1
          action: ATS选择主电源
        - step: 5
          node: ELEC-LV-MAIN_DST_BUS_E1
          action: 应急母线配电

    - path_id: ELEC-LV_PATH_GENERATOR
      path_name: 发电机供电路径
      path_type: BKP
      description: 市电失电时发电机供电
      sequence:
        - step: 1
          node: ELEC-LV-MAIN_SRC_GENERATOR
          action: 柴油发电机发电
        - step: 2
          node: ELEC-LV-MAIN_DST_GEN_PANEL
          action: 发电机开关
        - step: 3
          node: ELEC-LV-MAIN_DST_ATS_1
          action: ATS切换至备用
        - step: 4
          node: ELEC-LV-MAIN_DST_BUS_E1
          action: 应急母线供电
      trigger_conditions:
        - 双路市电均失电
        - ATS检测主电源失压
      switching_time: "<15秒（含发电机启动）"

  control_logic:

    generator_auto_start:
      name: 发电机自动启动逻辑
      trigger:
        condition: 双路市电失压
        detection: ATS主电源失压 AND 备用电源（另一路市电）失压
        delay: 3s
      sequence:
        - step: 1
          action: 发送启动信号至发电机控制器
          delay: 0s
        - step: 2
          action: 发电机预热（可选）
          delay: 依设置
        - step: 3
          action: 发电机启动
          time: "<10秒达到额定转速"
        - step: 4
          action: 发电机电压/频率稳定
          time: 2-3s
        - step: 5
          action: 发电机出口开关合闸
          delay: 0.5s
        - step: 6
          action: ATS切换至发电机
          delay: 0.5s
        - step: 7
          action: 应急母线恢复供电
          note: 总时间<15秒
    
      load_shedding:
        description: 分级加载
        logic: |
          1. 发电机启动后先带一级重要负荷
          2. 5秒后加载二级重要负荷
          3. 10秒后加载其他应急负荷
          4. 防止发电机冲击过载

    generator_auto_stop:
      name: 发电机自动停机逻辑
      trigger:
        condition: 市电恢复正常
        detection: ATS主电源恢复正常持续30秒
      sequence:
        - step: 1
          action: ATS切换回市电
          delay: 0s
        - step: 2
          action: 发电机出口开关分闸
          delay: 0.5s
        - step: 3
          action: 发电机空载运行散热
          time: 180s
        - step: 4
          action: 发电机停机
          delay: 0s
    
      cool_down:
        description: 冷却运行
        time: 3分钟
        purpose: 保护发动机

    low_voltage_ats_control:
      name: 低压ATS控制逻辑
    
      main_to_backup:
        trigger: 主电源电压<85%额定值持续1秒
        action: 切换至备用电源
        time: <3s
        interlock: 确保不并列运行
      
      backup_to_main:
        trigger: 主电源恢复正常持续30秒
        action: 切回主电源
        mode: 自动/手动可选
        time: <3s
      
      parallel_forbidden:
        description: 禁止并列
        logic: |
          主开关合闸时，备用开关必须分闸
          两路电源不得同时向负载供电

  alarm_protection:
  
    critical_alarms:
      - alarm_id: ALM_LV_ALL_FAIL
        alarm_name: 低压全失电
        severity: EMERGENCY
        trigger: 所有母线失压
        action: 立即启动发电机
      
      - alarm_id: ALM_GEN_FAIL
        alarm_name: 发电机启动失败
        severity: CRITICAL
        trigger: 发电机启动命令发出但10秒内未启动
        action: 尝试再次启动，报警通知
      
      - alarm_id: ALM_TRANSFORMER_OVERTEMP
        alarm_name: 变压器超温
        severity: HIGH
        trigger: 任一变压器温度>130℃
        action: 启动冷却风机，报警

  dependencies:
  
    upstream_dependencies:
      - dependency_id: DEP_HV
        from_system: ELEC-HV
        dependency_type: POWER_SUPPLY
        criticality: CRITICAL
        description: 高压电源（变压器高压侧）
      
      - dependency_id: DEP_FUEL
        from_system: EXTERNAL_FUEL
        dependency_type: FUEL_SUPPLY
        criticality: HIGH
        description: 柴油燃料供应
      
    downstream_dependencies:
      - dependency_id: DEP_FLOOR
        to_system: ELEC-LV-FLOOR
        dependency_type: POWER_SUPPLY
        criticality: CRITICAL
      
      - dependency_id: DEP_HVAC
        to_system: HVAC-CHP
        dependency_type: POWER_SUPPLY
        criticality: HIGH
      
      - dependency_id: DEP_UPS
        to_system: ELEC-UPS
        dependency_type: POWER_SUPPLY
        criticality: CRITICAL
```

---

## 系统 2.3: ELEC-EPS 应急电源系统

```yaml
System_Topology:

  identity:
    system_id: ELEC-EPS
    system_name: 应急电源系统
    system_name_en: Emergency Power System
    system_category: ELEC
    system_type: 应急电源
    priority_level: P0-LIFE_SAFETY
  
    description: |
      医院应急电源系统，包括柴油发电机组和UPS不间断电源。
      在市电失电时为一级负荷和特别重要负荷提供不间断电源保障。
      柴油发电机在10-15秒内启动供电，UPS提供毫秒级不间断切换。
  
    design_basis:
      generator_capacity: {value: 2×2000, unit: kVA, note: "双机并联"}
      ups_capacity: {value: 600, unit: kVA, note: "ICU/手术室等"}
      backup_time:
        generator: {value: 8, unit: h, note: "日用油箱"}
        ups: {value: 15-30, unit: min, note: "蓄电池"}
  
    parent_system: ELEC-LV-MAIN
  
    design_standards:
      - GB 50052-2009 供配电系统设计规范
      - JGJ 312-2013 医疗建筑电气设计规范
      - GB 50016-2014 建筑设计防火规范
  
    version: 1.0
    last_updated: 2024

  boundary:
    inputs:
      - boundary_id: ELEC-EPS_IN_001
        name: 柴油燃料
        from_system: EXTERNAL_FUEL
        medium: FUEL-DIESEL
        parameters:
          storage: {value: 8000, unit: L, note: "室外储油罐"}
          daily_tank: {value: 1000, unit: L/台}
        
      - boundary_id: ELEC-EPS_IN_002
        name: UPS输入电源
        from_system: ELEC-LV-MAIN
        from_node: ELEC-LV-MAIN_DST_FEEDER_UPS
        medium: ELEC-LV
      
      - boundary_id: ELEC-EPS_IN_003
        name: 发电机控制信号
        from_system: ELEC-LV-MAIN
        medium: SIGNAL-CTRL
        note: ATS失压信号触发发电机启动
      
    outputs:
      - boundary_id: ELEC-EPS_OUT_001
        name: 发电机低压输出
        to_system: ELEC-LV-MAIN
        to_node: ELEC-LV-MAIN_DST_GEN_PANEL
        medium: ELEC-LV
      
      - boundary_id: ELEC-EPS_OUT_002
        name: UPS输出电源
        to_system: 特别重要负荷
        medium: ELEC-LV-UPS
        parameters:
          voltage: {value: 380/220, unit: V}
          waveform: 纯正弦波

  nodes:

    source_nodes:
  
      - node_id: ELEC-EPS_SRC_FUEL_TANK
        node_name: 柴油储油罐
        node_name_en: Diesel Fuel Storage Tank
        node_type: Source_Node
        node_category: SRC
      
        function: 存储柴油燃料
        medium_in: FUEL-DIESEL
        medium_out: FUEL-DIESEL
      
        equipment_parameters:
          type: 卧式储油罐
          capacity: {value: 8000, unit: L}
          material: 钢制双层罐
          location: 室外埋地
          leak_detection: 渗漏报警
          vent: 呼吸阀
      
        control_points:
          sensors:
            - point_id: TANK_LEVEL
              point_name: 油位
              point_type: AI
              unit: "%"
              range: [0, 100]
          status:
            - point_id: TANK_LOW_LEVEL
              point_name: 低油位报警
              point_type: DI
            - point_id: TANK_LEAK
              point_name: 渗漏报警
              point_type: DI
      
        location_hint:
          space_type: OUTDOOR
          position: 室外埋地/地面
          distance: ">10m from building"

      - node_id: ELEC-EPS_SRC_GENERATOR_1
        node_name: 1#柴油发电机组
        node_name_en: Diesel Generator Set 1
        node_type: Source_Node
        node_category: SRC
      
        function: 应急发电
        medium_in: FUEL-DIESEL
        medium_out: ELEC-LV
      
        equipment_parameters:
          type: 柴油发电机组
          prime_power: {value: 1600, unit: kW}
          standby_power: {value: 2000, unit: kVA}
          voltage: {value: 400, unit: V}
          frequency: {value: 50, unit: Hz}
          power_factor: 0.8
          engine_brand: 进口柴油机
          generator_brand: 知名品牌无刷发电机
          cooling: 闭式水冷
          starting_method: 24V电启动（双蓄电池）
          starting_time: {value: "<8", unit: s}
          fuel_consumption: {value: 260, unit: "L/h", note: "满载"}
          noise_level: {value: "<95", unit: "dB(A)@1m"}
          parallel_capability: 支持并机运行
      
        control_points:
          sensors:
            - point_id: GEN1_V
              point_name: 输出电压
              point_type: AI
              unit: V
            - point_id: GEN1_I
              point_name: 输出电流
              point_type: AI
              unit: A
            - point_id: GEN1_F
              point_name: 频率
              point_type: AI
              unit: Hz
            - point_id: GEN1_P
              point_name: 有功功率
              point_type: AI
              unit: kW
            - point_id: GEN1_LOAD
              point_name: 负载率
              point_type: AI
              unit: "%"
            - point_id: GEN1_FUEL
              point_name: 日用油箱油位
              point_type: AI
              unit: "%"
            - point_id: GEN1_COOLANT_TEMP
              point_name: 冷却液温度
              point_type: AI
              unit: ℃
            - point_id: GEN1_OIL_PRESS
              point_name: 机油压力
              point_type: AI
              unit: kPa
            - point_id: GEN1_SPEED
              point_name: 转速
              point_type: AI
              unit: rpm
            - point_id: GEN1_BATTERY_V
              point_name: 启动电池电压
              point_type: AI
              unit: V
          status:
            - point_id: GEN1_READY
              point_name: 机组就绪
              point_type: DI
            - point_id: GEN1_RUN
              point_name: 机组运行
              point_type: DI
            - point_id: GEN1_FAULT
              point_name: 机组故障
              point_type: DI
            - point_id: GEN1_AUTO
              point_name: 自动模式
              point_type: DI
            - point_id: GEN1_CB_ON
              point_name: 出口开关合闸
              point_type: DI
          commands:
            - point_id: GEN1_START
              point_name: 启动命令
              point_type: DO
            - point_id: GEN1_STOP
              point_name: 停机命令
              point_type: DO
            - point_id: GEN1_CB_CLOSE
              point_name: 合闸命令
              point_type: DO
            - point_id: GEN1_CB_OPEN
              point_name: 分闸命令
              point_type: DO
      
        protection_settings:
          overspeed: {value: 1650, unit: rpm}
          low_oil_pressure: {value: 50, unit: kPa}
          high_coolant_temp: {value: 98, unit: ℃}
          overcurrent: {value: 110, unit: "%"}
          overvoltage: {value: 115, unit: "%"}
          undervoltage: {value: 85, unit: "%"}
          overfrequency: {value: 52, unit: Hz}
          underfrequency: {value: 48, unit: Hz}
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 柴油发电机房
          floor: B1/1F
          area_requirement: {value: ">60", unit: "m²/台"}
      
        installation_requirements:
          - 独立机房，2小时防火分隔
          - 减振基础（混凝土惯性基座+弹簧减振器）
          - 进风系统（新风量满足燃烧+散热）
          - 排风系统（散热）
          - 排烟管道（室外高空排放）
          - 噪声控制（消声器+隔声墙）
          - 日用油箱间（甲类）
          - 消防设施
          - 紧急停机按钮

      - node_id: ELEC-EPS_SRC_GENERATOR_2
        node_name: 2#柴油发电机组
        node_name_en: Diesel Generator Set 2
        node_type: Source_Node
        node_category: SRC
        function: 应急发电（与1#并机）
        medium_in: FUEL-DIESEL
        medium_out: ELEC-LV
        equipment_parameters:
          type: 柴油发电机组
          prime_power: {value: 1600, unit: kW}
          standby_power: {value: 2000, unit: kVA}
          parallel_capability: 支持并机运行
        location_hint:
          space_type: MEP_ROOM
          room_name: 柴油发电机房

      - node_id: ELEC-EPS_SRC_UPS_1
        node_name: 1#UPS主机
        node_name_en: UPS Unit 1
        node_type: Source_Node
        node_category: SRC
      
        function: 不间断电源供应
        medium_in: ELEC-LV
        medium_out: ELEC-LV-UPS
      
        multiplicity: multiple
        instance_pattern: ELEC-EPS_SRC_UPS_{N}
        typical_configuration:
          quantity: 2
          redundancy: "1+1冗余并机"
          total_capacity: {value: 600, unit: kVA}
      
        equipment_parameters:
          type: 在线式双变换UPS
          capacity: {value: 300, unit: kVA}
          input_voltage: {value: "380±20%", unit: V}
          output_voltage: {value: 380, unit: V, tolerance: ±1%}
          frequency: {value: 50, unit: Hz, tolerance: ±0.1%}
          power_factor_input: ">0.99"
          power_factor_output: "0.8-1.0"
          efficiency: ">96%"
          thd_output: "<3%"
          transfer_time: {value: 0, unit: ms, note: "零切换"}
          overload_capability: "125% 10min, 150% 1min"
          parallel_operation: 支持并机运行
          battery_type: 铅酸蓄电池/锂电池
          battery_backup_time: {value: 15, unit: min, note: "满载"}
      
        control_points:
          sensors:
            - point_id: UPS1_INPUT_V
              point_name: 输入电压
              point_type: AI
              unit: V
            - point_id: UPS1_OUTPUT_V
              point_name: 输出电压
              point_type: AI
              unit: V
            - point_id: UPS1_OUTPUT_I
              point_name: 输出电流
              point_type: AI
              unit: A
            - point_id: UPS1_LOAD
              point_name: 负载率
              point_type: AI
              unit: "%"
            - point_id: UPS1_BATTERY_V
              point_name: 蓄电池电压
              point_type: AI
              unit: V
            - point_id: UPS1_BATTERY_SOC
              point_name: 蓄电池剩余电量
              point_type: AI
              unit: "%"
            - point_id: UPS1_TEMP
              point_name: 机内温度
              point_type: AI
              unit: ℃
            - point_id: UPS1_RUNTIME
              point_name: 预计后备时间
              point_type: AI
              unit: min
          status:
            - point_id: UPS1_NORMAL
              point_name: 正常运行
              point_type: DI
            - point_id: UPS1_ON_BATTERY
              point_name: 电池放电
              point_type: DI
            - point_id: UPS1_ON_BYPASS
              point_name: 旁路运行
              point_type: DI
            - point_id: UPS1_FAULT
              point_name: 故障报警
              point_type: DI
            - point_id: UPS1_BATTERY_LOW
              point_name: 电池低电量
              point_type: DI
            - point_id: UPS1_OVERLOAD
              point_name: 过载报警
              point_type: DI
          commands:
            - point_id: UPS1_ON
              point_name: 开机命令
              point_type: DO
            - point_id: UPS1_OFF
              point_name: 关机命令
              point_type: DO
            - point_id: UPS1_BATTERY_TEST
              point_name: 电池测试
              point_type: DO
      
        location_hint:
          space_type: MEP_ROOM
          room_name: UPS机房
          floor: B1/1F
          area_requirement: {value: ">50", unit: "m²"}
          load_bearing: {value: ">1000", unit: "kg/m²", note: "蓄电池较重"}
      
        installation_requirements:
          - 独立UPS机房
          - 精密空调（温度18-28℃，湿度40-70%）
          - 防静电地板
          - 蓄电池室通风（铅酸电池产生氢气）
          - 消防设施（气体灭火）
          - 紧急关机按钮

    distribution_nodes:
  
      - node_id: ELEC-EPS_DST_GEN_SYNC
        node_name: 发电机并机柜
        node_name_en: Generator Synchronizing Panel
        node_type: Distribution_Node
        node_subtype: SWG
        node_category: DST
      
        function: 双机并联运行控制
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        equipment_parameters:
          type: 发电机并机柜
          rated_current: {value: 4000, unit: A}
          sync_controller: 自动同期装置
          load_sharing: 有功/无功功率分配
          protection: 逆功率、过流、差动
      
        control_points:
          status:
            - point_id: SYNC_READY
              point_name: 同期就绪
              point_type: DI
            - point_id: SYNC_SUCCESS
              point_name: 同期成功
              point_type: DI
            - point_id: LOAD_BALANCE
              point_name: 负荷均分
              point_type: DI
          sensors:
            - point_id: SYNC_FREQ_DIFF
              point_name: 频率差
              point_type: AI
              unit: Hz
            - point_id: SYNC_PHASE_DIFF
              point_name: 相位差
              point_type: AI
              unit: "°"
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 柴油发电机房

      - node_id: ELEC-EPS_DST_UPS_BYPASS
        node_name: UPS维护旁路柜
        node_name_en: UPS Maintenance Bypass Panel
        node_type: Distribution_Node
        node_subtype: SWG
        node_category: DST
      
        function: UPS维护时旁路供电
        medium_in: ELEC-LV
        medium_out: ELEC-LV-UPS
      
        equipment_parameters:
          type: 维护旁路柜
          rated_current: {value: 1000, unit: A}
          bypass_switch: 手动/自动切换
          interlock: 与UPS联锁
      
        control_points:
          status:
            - point_id: BYPASS_ACTIVE
              point_name: 旁路激活
              point_type: DI
      
        location_hint:
          space_type: MEP_ROOM
          room_name: UPS机房

      - node_id: ELEC-EPS_DST_UPS_OUTPUT
        node_name: UPS输出配电柜
        node_name_en: UPS Output Distribution Panel
        node_type: Distribution_Node
        node_subtype: SWG
        node_category: DST
      
        function: UPS输出配电分配
        medium_in: ELEC-LV-UPS
        medium_out: ELEC-LV-UPS
      
        equipment_parameters:
          type: 配电柜
          rated_current: {value: 1000, unit: A}
          outgoing_circuits: 16-24路
      
        served_loads:
          - 手术室设备电源
          - ICU/CCU医疗设备
          - 急诊抢救设备
          - 医学影像设备（CT/MRI）
          - 中心监护系统
          - 信息机房
      
        location_hint:
          space_type: MEP_ROOM
          room_name: UPS机房

    sink_nodes:
  
      - node_id: ELEC-EPS_SNK_LV_OUTPUT
        node_name: 发电机低压输出接口
        node_name_en: Generator LV Output Connection
        node_type: Sink_Node
        node_category: SNK
      
        function: 发电机输出至低压配电系统
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        is_boundary_output: true
        target_system: ELEC-LV-MAIN
        target_node: ELEC-LV-MAIN_DST_GEN_PANEL
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 柴油发电机房

      - node_id: ELEC-EPS_SNK_UPS_LOAD
        node_name: UPS负载接口
        node_name_en: UPS Load Connection
        node_type: Sink_Node
        node_category: SNK
      
        function: 供电至特别重要负荷
        medium_in: ELEC-LV-UPS
        medium_out: ELEC-LV-UPS
      
        is_boundary_output: true
      
        multiplicity: multiple
        instance_pattern: ELEC-EPS_SNK_UPS_LOAD_{Area}
      
        served_areas:
          - 手术室
          - ICU
          - 急诊抢救室
          - 信息机房
      
        location_hint:
          space_type: 各医疗区域

  edges:

    fuel_edges:
      - edge_id: ELEC-EPS_EDGE_001
        edge_name: 储油罐至发电机1
        edge_type: PIP
        from_node: ELEC-EPS_SRC_FUEL_TANK
        to_node: ELEC-EPS_SRC_GENERATOR_1
        direction: unidirectional
        medium: FUEL-DIESEL
        pipe_parameters:
          material: 镀锌钢管
          size: DN50
        
      - edge_id: ELEC-EPS_EDGE_002
        edge_name: 储油罐至发电机2
        edge_type: PIP
        from_node: ELEC-EPS_SRC_FUEL_TANK
        to_node: ELEC-EPS_SRC_GENERATOR_2
        direction: unidirectional
        medium: FUEL-DIESEL

    generator_edges:
      - edge_id: ELEC-EPS_EDGE_011
        edge_name: 发电机1至并机柜
        edge_type: CAB
        from_node: ELEC-EPS_SRC_GENERATOR_1
        to_node: ELEC-EPS_DST_GEN_SYNC
        direction: unidirectional
        medium: ELEC-LV
        cable_parameters:
          type: 铜芯电缆（耐火）
          size: "3×(3×185)+2×95mm²"
        
      - edge_id: ELEC-EPS_EDGE_012
        edge_name: 发电机2至并机柜
        edge_type: CAB
        from_node: ELEC-EPS_SRC_GENERATOR_2
        to_node: ELEC-EPS_DST_GEN_SYNC
        direction: unidirectional
        medium: ELEC-LV
      
      - edge_id: ELEC-EPS_EDGE_013
        edge_name: 并机柜至低压输出
        edge_type: CAB
        from_node: ELEC-EPS_DST_GEN_SYNC
        to_node: ELEC-EPS_SNK_LV_OUTPUT
        direction: unidirectional
        medium: ELEC-LV

    ups_edges:
      - edge_id: ELEC-EPS_EDGE_021
        edge_name: UPS1至旁路柜
        edge_type: CAB
        from_node: ELEC-EPS_SRC_UPS_1
        to_node: ELEC-EPS_DST_UPS_BYPASS
        direction: unidirectional
        medium: ELEC-LV-UPS
      
      - edge_id: ELEC-EPS_EDGE_022
        edge_name: 旁路柜至输出柜
        edge_type: CAB
        from_node: ELEC-EPS_DST_UPS_BYPASS
        to_node: ELEC-EPS_DST_UPS_OUTPUT
        direction: unidirectional
        medium: ELEC-LV-UPS
      
      - edge_id: ELEC-EPS_EDGE_023
        edge_name: 输出柜至负载
        edge_type: CAB
        from_node: ELEC-EPS_DST_UPS_OUTPUT
        to_node: ELEC-EPS_SNK_UPS_LOAD
        direction: unidirectional
        medium: ELEC-LV-UPS
        multiplicity: multiple

  typical_paths:

    - path_id: ELEC-EPS_PATH_GEN_STARTUP
      path_name: 发电机应急启动路径
      path_type: EMG
      description: 市电失电时发电机自动启动供电
      sequence:
        - step: 1
          action: ATS检测市电失压
          time: 3s
        - step: 2
          node: ELEC-EPS_SRC_GENERATOR_1
          action: 发电机启动
          time: 8s
        - step: 3
          node: ELEC-EPS_DST_GEN_SYNC
          action: 并机（如需要）
          time: 2s
        - step: 4
          node: ELEC-EPS_SNK_LV_OUTPUT
          action: 输出至低压系统
        - step: 5
          action: ATS切换至发电机
          time: 1s
      total_time: "<15s"

    - path_id: ELEC-EPS_PATH_UPS_BACKUP
      path_name: UPS电池放电路径
      path_type: BKP
      description: 市电失电时UPS电池立即放电
      sequence:
        - step: 1
          action: 市电中断（或发电机未启动期间）
        - step: 2
          node: ELEC-EPS_SRC_UPS_1
          action: 逆变器由电池供电（0ms切换）
        - step: 3
          node: ELEC-EPS_DST_UPS_OUTPUT
          action: 持续供电至负载
      backup_time: 15-30分钟

  control_logic:

    generator_parallel_operation:
      name: 双机并联运行控制
    
      sync_conditions:
        voltage_diff: {value: "<5", unit: "%"}
        frequency_diff: {value: "<0.5", unit: Hz}
        phase_diff: {value: "<10", unit: "°"}
      
      sequence:
        - step: 1
          action: 1#发电机先启动并合闸带负荷
        - step: 2
          action: 2#发电机启动
        - step: 3
          action: 调节2#频率使其略高于1#
          note: 使相位同步
        - step: 4
          action: 相位差<10°时合闸
        - step: 5
          action: 调节两机功率均分
        
      load_sharing:
        active_power: 按容量比例分配
        reactive_power: 下垂控制

    ups_operation_mode:
      name: UPS运行模式
    
      normal_mode:
        description: 正常在线模式
        path: "市电→整流器→逆变器→负载"
        battery_status: 浮充
        efficiency: ">96%"
      
      battery_mode:
        description: 电池放电模式
        trigger: 市电失电或超出允许范围
        path: "电池→逆变器→负载"
        transfer_time: 0ms
      
      bypass_mode:
        description: 旁路模式
        trigger: 逆变器故障或过载
        path: "市电→静态旁路→负载"
        transfer_time: "<4ms"
      
      maintenance_mode:
        description: 维护旁路模式
        trigger: 手动切换维护
        path: "市电→手动旁路→负载"
        note: UPS可完全隔离检修

    battery_management:
      name: 蓄电池管理
    
      charging:
        float_voltage: {value: 2.27, unit: "V/cell", note: "浮充电压"}
        equalize_voltage: {value: 2.35, unit: "V/cell", note: "均充电压"}
        temperature_compensation: "-3mV/℃/cell"
      
      monitoring:
        - 单体电压监测
        - 电池组总电压
        - 充放电电流
        - 电池温度
        - 内阻测试（定期）
      
      alarms:
        low_battery: {soc: 20, unit: "%"}
        battery_fault: 单体电压异常
        high_temp: {value: 40, unit: ℃}

  alarm_protection:
  
    critical_alarms:
      - alarm_id: ALM_GEN_START_FAIL
        alarm_name: 发电机启动失败
        severity: CRITICAL
        trigger: 启动命令发出10秒后未检测到运行
        action: 尝试启动备用机组
      
      - alarm_id: ALM_GEN_FAULT
        alarm_name: 发电机故障停机
        severity: CRITICAL
        trigger: 保护动作跳闸
        action: 隔离故障机组，启用备用
      
      - alarm_id: ALM_UPS_BATTERY_LOW
        alarm_name: UPS电池低电量
        severity: HIGH
        trigger: 电池剩余电量<20%
        action: 报警，准备切换或关闭非关键负荷
      
      - alarm_id: ALM_FUEL_LOW
        alarm_name: 柴油油位低
        severity: HIGH
        trigger: 储油罐油位<30%
        action: 通知补充燃油

  dependencies:
  
    upstream_dependencies:
      - dependency_id: DEP_FUEL
        from_system: EXTERNAL_FUEL
        dependency_type: FUEL_SUPPLY
        criticality: HIGH
        description: 柴油燃料供应
      
      - dependency_id: DEP_LV_INPUT
        from_system: ELEC-LV-MAIN
        dependency_type: POWER_SUPPLY
        criticality: MEDIUM
        description: UPS输入电源（正常时）
      
    downstream_dependencies:
      - dependency_id: DEP_LV_OUTPUT
        to_system: ELEC-LV-MAIN
        dependency_type: BACKUP_POWER
        criticality: CRITICAL
        description: 应急电源输出
      
      - dependency_id: DEP_CRITICAL_LOAD
        to_system: 医疗设备
        dependency_type: UPS_POWER
        criticality: CRITICAL
        description: 特别重要负荷不间断供电
```

---

# 医疗气体系统（4个系统）

## 系统 2.4: MGAS-O2 医用氧气系统

```yaml
System_Topology:

  identity:
    system_id: MGAS-O2
    system_name: 医用氧气系统
    system_name_en: Medical Oxygen System
    system_category: MGAS
    system_type: 医用气体-氧气
    priority_level: P0-LIFE_SAFETY
  
    description: |
      医院医用氧气集中供应系统，为全院提供符合药典标准的医用氧气。
      氧源采用液氧储罐+汇流排备用方式，确保供氧连续性。
      系统设置三级报警（气源、区域、床旁），保障患者用氧安全。
  
    design_basis:
      gas_type: 医用氧气（O2）
      purity: {value: ">99.5%", note: "符合《中国药典》"}
      supply_pressure: {value: 0.4, unit: MPa, tolerance: ±0.05}
      terminal_flow: {value: 10, unit: "L/min", note: "单终端最大流量"}
      peak_demand: {value: 2000, unit: "L/min", note: "全院峰值流量"}
  
    design_standards:
      - GB 50751-2012 医用气体工程技术规范
      - YY/T 0187-1994 医用中心供氧系统通用技术条件
      - 《中国药典》医用氧质量标准
      - GB 50016-2014 建筑设计防火规范
  
    version: 1.0
    last_updated: 2024

  boundary:
    inputs:
      - boundary_id: MGAS-O2_IN_001
        name: 液氧供应
        from_system: EXTERNAL_LOX
        medium: O2-LIQUID
        parameters:
          purity: ">99.5%"
          delivery: 槽车补充
        
      - boundary_id: MGAS-O2_IN_002
        name: 氧气瓶供应（备用）
        from_system: EXTERNAL_CYLINDER
        medium: O2-GAS
        parameters:
          purity: ">99.5%"
          pressure: {value: 15, unit: MPa}
      
    outputs:
      - boundary_id: MGAS-O2_OUT_001
        name: 病房氧气终端
        to_system: 医疗终端
        medium: O2-GAS
        parameters:
          pressure: {value: 0.4, unit: MPa}
        
      - boundary_id: MGAS-O2_OUT_002
        name: 手术室氧气终端
        to_system: 医疗终端
        medium: O2-GAS

  nodes:

    source_nodes:
  
      - node_id: MGAS-O2_SRC_LOX_TANK
        node_name: 液氧储罐
        node_name_en: Liquid Oxygen Tank
        node_type: Source_Node
        node_category: SRC
      
        function: 液态氧气储存
        medium_in: O2-LIQUID
        medium_out: O2-LIQUID
      
        equipment_parameters:
          type: 立式真空绝热储罐
          capacity: {value: 10, unit: "m³", note: "有效容积"}
          working_pressure: {value: 1.6, unit: MPa}
          design_pressure: {value: 2.0, unit: MPa}
          evaporation_rate: {value: "<0.5", unit: "%/d"}
          material: 不锈钢内胆+碳钢外壳
          insulation: 真空+珠光砂
          safety_valve: 双安全阀
          filling_connection: DN50快接
      
        control_points:
          sensors:
            - point_id: LOX_LEVEL
              point_name: 液位
              point_type: AI
              unit: "%"
              range: [0, 100]
            - point_id: LOX_PRESSURE
              point_name: 储罐压力
              point_type: AI
              unit: MPa
              range: [0, 2.0]
            - point_id: LOX_TEMP
              point_name: 液氧温度
              point_type: AI
              unit: ℃
              range: [-200, -150]
          status:
            - point_id: LOX_LOW_LEVEL
              point_name: 低液位报警
              point_type: DI
            - point_id: LOX_HIGH_PRESS
              point_name: 高压报警
              point_type: DI
            - point_id: LOX_SUPPLY_ON
              point_name: 供气状态
              point_type: DI
      
        location_hint:
          space_type: OUTDOOR
          position: 室外液氧站
          area_requirement: {value: ">100", unit: "m²"}
          clearance: 
            from_building: ">7.5m"
            from_road: ">5m"
            from_fire_hydrant: ">15m"
      
        installation_requirements:
          - 防火间距符合GB 50016
          - 围栏隔离（高度≥1.5m）
          - 导静电接地
          - 氧气浓度监测
          - 严禁烟火标志
          - 消防设施
          - 槽车充装区

      - node_id: MGAS-O2_SRC_MANIFOLD
        node_name: 氧气汇流排
        node_name_en: Oxygen Cylinder Manifold
        node_type: Source_Node
        node_category: SRC
      
        function: 氧气瓶组备用气源
        medium_in: O2-GAS
        medium_out: O2-GAS
      
        equipment_parameters:
          type: 双侧自动切换汇流排
          cylinder_per_side: 10瓶
          cylinder_volume: {value: 40, unit: L}
          cylinder_pressure: {value: 15, unit: MPa}
          auto_switching: 一侧用尽自动切换
          regulator: 一级减压（15MPa→1.0MPa）
      
        control_points:
          sensors:
            - point_id: MANIFOLD_PRESS_L
              point_name: 左侧压力
              point_type: AI
              unit: MPa
            - point_id: MANIFOLD_PRESS_R
              point_name: 右侧压力
              point_type: AI
              unit: MPa
            - point_id: MANIFOLD_OUTPUT_PRESS
              point_name: 输出压力
              point_type: AI
              unit: MPa
          status:
            - point_id: MANIFOLD_IN_USE
              point_name: 汇流排启用
              point_type: DI
            - point_id: MANIFOLD_LEFT_ACTIVE
              point_name: 左侧供气
              point_type: DI
            - point_id: MANIFOLD_RIGHT_ACTIVE
              point_name: 右侧供气
              point_type: DI
            - point_id: MANIFOLD_LOW_PRESS
              point_name: 低压报警
              point_type: DI
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 汇流排间/液氧站旁
          position: 独立设置
      
        installation_requirements:
          - 独立房间或室外设置
          - 良好通风
          - 防震固定
          - 气瓶间距≥50mm
          - 严禁烟火

    distribution_nodes:
  
      - node_id: MGAS-O2_DST_VAPORIZER
        node_name: 液氧汽化器
        node_name_en: LOX Vaporizer
        node_type: Distribution_Node
        node_subtype: TRF
        node_category: DST
      
        function: 液氧汽化为气态氧
        medium_in: O2-LIQUID
        medium_out: O2-GAS
      
        equipment_parameters:
          type: 空温式汽化器
          capacity: {value: 200, unit: "Nm³/h", note: "单台"}
          quantity: 2（一用一备）
          inlet_pressure: {value: 1.6, unit: MPa}
          outlet_pressure: {value: 1.5, unit: MPa}
          material: 铝合金翅片管
          temperature_drop: 环境温度下降约5℃
      
        control_points:
          sensors:
            - point_id: VAP_INLET_TEMP
              point_name: 进口温度
              point_type: AI
              unit: ℃
            - point_id: VAP_OUTLET_TEMP
              point_name: 出口温度
              point_type: AI
              unit: ℃
          status:
            - point_id: VAP_IN_SERVICE
              point_name: 在用状态
              point_type: DI
      
        location_hint:
          space_type: OUTDOOR
          position: 液氧储罐旁
          note: 需良好通风散热

      - node_id: MGAS-O2_DST_MAIN_REGULATOR
        node_name: 一级减压装置
        node_name_en: Primary Pressure Regulator
        node_type: Distribution_Node
        node_subtype: REG
        node_category: DST
      
        function: 高压氧气一级减压
        medium_in: O2-GAS
        medium_out: O2-GAS
      
        equipment_parameters:
          type: 气动先导式减压阀组
          inlet_pressure: {value: 1.5, unit: MPa}
          outlet_pressure: {value: 0.8, unit: MPa}
          capacity: {value: 300, unit: "Nm³/h"}
          quantity: "2（一用一备）"
          material: 铜合金（脱脂处理）
          safety_valve: 设置
          bypass_valve: 设置
      
        control_points:
          sensors:
            - point_id: REG1_INLET_P
              point_name: 进口压力
              point_type: AI
              unit: MPa
            - point_id: REG1_OUTLET_P
              point_name: 出口压力
              point_type: AI
              unit: MPa
          status:
            - point_id: REG1_HIGH_P_ALARM
              point_name: 高压报警
              point_type: DI
            - point_id: REG1_LOW_P_ALARM
              point_name: 低压报警
              point_type: DI
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 氧气站房/气体机房

      - node_id: MGAS-O2_DST_ALARM_PANEL
        node_name: 气源报警装置
        node_name_en: Source Alarm Panel
        node_type: Distribution_Node
        node_subtype: MON
        node_category: DST
      
        function: 气源区域压力监测报警
        medium_in: O2-GAS
        medium_out: SIGNAL
      
        equipment_parameters:
          type: 医用气体报警器
          alarm_level: 一级（气源）
          display: 数字压力显示
          alarm_output: 声光报警+远传
          power: 220V AC + 电池后备
      
        control_points:
          sensors:
            - point_id: O2_SRC_PRESSURE
              point_name: 气源压力
              point_type: AI
              unit: MPa
          status:
            - point_id: O2_SRC_HIGH_ALARM
              point_name: 高压报警
              point_type: DI
            - point_id: O2_SRC_LOW_ALARM
              point_name: 低压报警
              point_type: DI
      
        alarm_settings:
          high_pressure: {value: 0.5, unit: MPa}
          low_pressure: {value: 0.3, unit: MPa}
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 气体站房值班室
          note: 24小时有人值班处

      - node_id: MGAS-O2_DST_MAIN_PIPE
        node_name: 氧气主管
        node_name_en: Oxygen Main Pipe
        node_type: Distribution_Node
        node_subtype: TRK
        node_category: DST
      
        function: 氧气主管输送
        medium_in: O2-GAS
        medium_out: O2-GAS
      
        equipment_parameters:
          material: 脱脂紫铜管/不锈钢管
          diameter: {value: "DN50-DN80", unit: mm}
          wall_thickness: 按压力等级确定
          connection: 银钎焊/氩弧焊
          surface: 内壁清洗脱脂
          marking: 氧气标识（绿色）
      
        location_hint:
          space_type: SHAFT
          shaft_type: 医疗气体管井
          position: 建筑竖向贯通

      - node_id: MGAS-O2_DST_RISER
        node_name: 氧气立管
        node_name_en: Oxygen Riser
        node_type: Distribution_Node
        node_subtype: TRK
        node_category: DST
      
        function: 氧气竖向输送至各楼层
        medium_in: O2-GAS
        medium_out: O2-GAS
      
        multiplicity: multiple
        instance_pattern: MGAS-O2_DST_RISER_{Zone}
      
        equipment_parameters:
          material: 脱脂紫铜管
          diameter: {value: "DN25-DN40", unit: mm}
          support: 每层设管道支架
      
        location_hint:
          space_type: SHAFT
          shaft_type: 医疗气体管井

      - node_id: MGAS-O2_DST_ZONE_VALVE
        node_name: 区域阀门箱
        node_name_en: Zone Valve Box
        node_type: Distribution_Node
        node_subtype: REG
        node_category: DST
      
        function: 区域供气控制、二级减压及报警
        medium_in: O2-GAS
        medium_out: O2-GAS
      
        multiplicity: multiple
        instance_pattern: MGAS-O2_DST_ZONE_VALVE_{Floor}_{Zone}
      
        equipment_parameters:
          type: 区域阀门箱（含二级减压）
          components:
            - 区域截止阀
            - 减压阀（0.8MPa→0.4MPa）
            - 压力表
            - 安全阀
            - 区域报警器
          material: 不锈钢箱体
          mounting: 嵌墙安装
      
        control_points:
          sensors:
            - point_id: O2_ZONE_PRESSURE
              point_name: 区域压力
              point_type: AI
              unit: MPa
          status:
            - point_id: O2_ZONE_HIGH_ALARM
              point_name: 高压报警
              point_type: DI
            - point_id: O2_ZONE_LOW_ALARM
              point_name: 低压报警
              point_type: DI
            - point_id: O2_ZONE_VALVE_CLOSED
              point_name: 阀门关闭
              point_type: DI
      
        alarm_settings:
          high_pressure: {value: 0.5, unit: MPa}
          low_pressure: {value: 0.3, unit: MPa}
      
        location_hint:
          space_type: CORRIDOR
          position: 护士站附近走廊
          height: 距地1.5m

      - node_id: MGAS-O2_DST_BRANCH
        node_name: 氧气支管
        node_name_en: Oxygen Branch Pipe
        node_type: Distribution_Node
        node_subtype: BRH
        node_category: DST
      
        function: 楼层内水平输送至终端
        medium_in: O2-GAS
        medium_out: O2-GAS
      
        multiplicity: multiple
      
        equipment_parameters:
          material: 脱脂紫铜管
          diameter: {value: "DN10-DN20", unit: mm}
      
        location_hint:
          space_type: CEILING_VOID
          position: 走廊/病房吊顶内

    sink_nodes:
  
      - node_id: MGAS-O2_SNK_TERMINAL
        node_name: 氧气终端
        node_name_en: Oxygen Outlet Terminal
        node_type: Sink_Node
        node_category: SNK
      
        function: 床旁/手术室氧气使用点
        medium_in: O2-GAS
        medium_out: O2-GAS (to patient)
      
        is_boundary_output: true
      
        multiplicity: multiple
        instance_pattern: MGAS-O2_SNK_TERMINAL_{Floor}_{Room}_{Seq}
        typical_quantity: 大量（按床位数）
      
        equipment_parameters:
          type: 快速插拔式终端
          standard: 德标DIN/国标GB
          gas_specific: 氧气专用（不可互换）
          color_coding: 绿色
          flow_rate: {value: "0-15", unit: "L/min"}
          outlet_pressure: {value: 0.4, unit: MPa, tolerance: ±0.05}
          mounting:
            - 设备带
            - 吊塔
            - 墙面
      
        location_hint:
          space_type: 病房/手术室/ICU
          position: 床头设备带/吊塔
          height: 距地1.4m（设备带）

      - node_id: MGAS-O2_SNK_ANESTHESIA
        node_name: 麻醉机氧气接口
        node_name_en: Anesthesia Machine O2 Connection
        node_type: Sink_Node
        node_category: SNK
      
        function: 手术室麻醉机氧气供应
        medium_in: O2-GAS
        medium_out: O2-GAS (to equipment)
      
        is_boundary_output: true
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 设备接口终端
          flow_rate: {value: "0-30", unit: "L/min"}
          pressure: {value: 0.4, unit: MPa}
          connection: 软管连接至麻醉机
      
        location_hint:
          space_type: 手术室
          position: 吊塔/设备柱

  edges:

    source_edges:
      - edge_id: MGAS-O2_EDGE_001
        edge_name: 液氧储罐至汽化器
        edge_type: PIP
        from_node: MGAS-O2_SRC_LOX_TANK
        to_node: MGAS-O2_DST_VAPORIZER
        direction: unidirectional
        medium: O2-LIQUID
        pipe_parameters:
          material: 不锈钢真空管
          diameter: DN25
          insulation: 真空绝热
        
      - edge_id: MGAS-O2_EDGE_002
        edge_name: 汽化器至一级减压
        edge_type: PIP
        from_node: MGAS-O2_DST_VAPORIZER
        to_node: MGAS-O2_DST_MAIN_REGULATOR
        direction: unidirectional
        medium: O2-GAS
        pipe_parameters:
          material: 不锈钢管
          diameter: DN40
          pressure: 1.5MPa
        
      - edge_id: MGAS-O2_EDGE_003
        edge_name: 汇流排至一级减压
        edge_type: PIP
        from_node: MGAS-O2_SRC_MANIFOLD
        to_node: MGAS-O2_DST_MAIN_REGULATOR
        direction: unidirectional
        medium: O2-GAS
        note: 备用气源

    distribution_edges:
      - edge_id: MGAS-O2_EDGE_011
        edge_name: 一级减压至主管
        edge_type: PIP
        from_node: MGAS-O2_DST_MAIN_REGULATOR
        to_node: MGAS-O2_DST_MAIN_PIPE
        direction: unidirectional
        medium: O2-GAS
        pipe_parameters:
          material: 脱脂紫铜管
          diameter: DN50
          pressure: 0.8MPa
        
      - edge_id: MGAS-O2_EDGE_012
        edge_name: 主管至立管
        edge_type: PIP
        from_node: MGAS-O2_DST_MAIN_PIPE
        to_node: MGAS-O2_DST_RISER
        direction: unidirectional
        medium: O2-GAS
        multiplicity: multiple
      
      - edge_id: MGAS-O2_EDGE_013
        edge_name: 立管至区域阀门箱
        edge_type: PIP
        from_node: MGAS-O2_DST_RISER
        to_node: MGAS-O2_DST_ZONE_VALVE
        direction: unidirectional
        medium: O2-GAS
        multiplicity: multiple
      
      - edge_id: MGAS-O2_EDGE_014
        edge_name: 区域阀门箱至支管
        edge_type: PIP
        from_node: MGAS-O2_DST_ZONE_VALVE
        to_node: MGAS-O2_DST_BRANCH
        direction: unidirectional
        medium: O2-GAS
      
      - edge_id: MGAS-O2_EDGE_015
        edge_name: 支管至终端
        edge_type: PIP
        from_node: MGAS-O2_DST_BRANCH
        to_node: MGAS-O2_SNK_TERMINAL
        direction: unidirectional
        medium: O2-GAS
        multiplicity: multiple

  typical_paths:

    - path_id: MGAS-O2_PATH_LOX
      path_name: 液氧供气路径
      path_type: SUP
      description: 液氧储罐经汽化、减压至终端
      sequence:
        - step: 1
          node: MGAS-O2_SRC_LOX_TANK
          action: 液氧储存
          parameters:
            pressure: 1.6MPa
        - step: 2
          node: MGAS-O2_DST_VAPORIZER
          action: 液氧汽化
          parameters:
            inlet: -183℃
            outlet: 常温
        - step: 3
          node: MGAS-O2_DST_MAIN_REGULATOR
          action: 一级减压
          parameters:
            inlet: 1.5MPa
            outlet: 0.8MPa
        - step: 4
          node: MGAS-O2_DST_MAIN_PIPE
          action: 主管输送
        - step: 5
          node: MGAS-O2_DST_RISER
          action: 立管输送
        - step: 6
          node: MGAS-O2_DST_ZONE_VALVE
          action: 二级减压
          parameters:
            inlet: 0.8MPa
            outlet: 0.4MPa
        - step: 7
          node: MGAS-O2_DST_BRANCH
          action: 支管分配
        - step: 8
          node: MGAS-O2_SNK_TERMINAL
          action: 终端供气
          parameters:
            pressure: 0.4MPa

    - path_id: MGAS-O2_PATH_BACKUP
      path_name: 备用供气路径（汇流排）
      path_type: BKP
      description: 液氧用尽或故障时自动切换至汇流排
      sequence:
        - step: 1
          node: MGAS-O2_SRC_MANIFOLD
          action: 汇流排供气
          parameters:
            pressure: 1.0MPa（减压后）
        - step: 2
          node: MGAS-O2_DST_MAIN_REGULATOR
          action: 一级减压
        - step: 3
          node: 后续节点同主路径
      trigger_conditions:
        - 液氧储罐液位低于设定值
        - 液氧系统压力异常
        - 手动切换

  control_logic:

    source_auto_switching:
      name: 气源自动切换
      description: 液氧与汇流排自动切换
    
      normal_operation:
        primary_source: 液氧储罐
        backup_source: 汇流排
      
      auto_switch_to_backup:
        trigger:
          - 液氧液位<15%
          - 液氧出口压力<0.3MPa
          - 液氧系统故障
        action: 自动开启汇流排供气
      
      alarm: 切换时发出声光报警

    manifold_switching:
      name: 汇流排自动切换
      description: 左右两组自动切换
    
      logic: |
        1. 一侧气瓶组使用中
        2. 压力降至0.5MPa时，自动切换至另一侧
        3. 报警提示更换空瓶
        4. 更换后人工切换回

    three_level_alarm:
      name: 三级报警系统
    
      level_1_source:
        location: 气源站房值班室
        monitoring:
          - 液氧液位
          - 液氧压力
          - 汇流排压力
          - 减压后压力
        alarm_conditions:
          - 高压/低压
          - 低液位
          - 气源切换
        
      level_2_zone:
        location: 护士站
        monitoring:
          - 区域供气压力
        alarm_conditions:
          - 高压/低压
        
      level_3_bedside:
        location: 床旁设备带
        monitoring:
          - 终端供气状态
        alarm_conditions:
          - 使用超时
          - 流量异常

  alarm_protection:
  
    critical_alarms:
      - alarm_id: ALM_O2_LOX_LOW
        alarm_name: 液氧低液位
        severity: HIGH
        trigger: 液位<20%
        action: 通知补充液氧，准备切换汇流排
      
      - alarm_id: ALM_O2_SOURCE_FAIL
        alarm_name: 氧气源故障
        severity: CRITICAL
        trigger: 主备气源均故障
        action: 紧急通知，启动应急预案
      
      - alarm_id: ALM_O2_LOW_PRESSURE
        alarm_name: 氧气低压报警
        severity: HIGH
        trigger: 任一监测点压力<0.3MPa
        action: 检查系统，排除故障

  dependencies:
  
    upstream_dependencies:
      - dependency_id: DEP_LOX_SUPPLY
        from_system: EXTERNAL_LOX
        dependency_type: GAS_SUPPLY
        criticality: CRITICAL
        description: 液氧补充供应
      
      - dependency_id: DEP_CYLINDER
        from_system: EXTERNAL_CYLINDER
        dependency_type: BACKUP_GAS
        criticality: HIGH
        description: 氧气瓶备用供应
      
    downstream_dependencies:
      - dependency_id: DEP_PATIENT
        to_system: 医疗终端
        dependency_type: MEDICAL_GAS
        criticality: CRITICAL
        description: 患者用氧
```

---

## 系统 2.5: MGAS-VAC 医用负压吸引系统

```yaml
System_Topology:

  identity:
    system_id: MGAS-VAC
    system_name: 医用负压吸引系统
    system_name_en: Medical Vacuum System
    system_category: MGAS
    system_type: 医用气体-负压
    priority_level: P0-LIFE_SAFETY
  
    description: |
      医院医用负压吸引系统，为手术室、ICU、病房等提供持续稳定的负压吸引。
      用于术中吸引、痰液吸引、引流等医疗操作。
      真空泵站集中设置，管道输送至各终端。
  
    design_basis:
      vacuum_level: {value: -0.04, unit: MPa, note: "相对于大气压"}
      terminal_flow: {value: 30, unit: "L/min", note: "单终端最大流量"}
      peak_demand: {value: 500, unit: "L/min", note: "全院峰值流量"}
      recovery_time: {value: "<3", unit: s, note: "从0恢复至-0.04MPa"}
  
    design_standards:
      - GB 50751-2012 医用气体工程技术规范
      - ISO 7396-1 医用气体管道系统
  
    version: 1.0
    last_updated: 2024

  boundary:
    inputs:
      - boundary_id: MGAS-VAC_IN_001
        name: 电力供应
        from_system: ELEC-LV-MAIN
        medium: ELEC-LV
      
    outputs:
      - boundary_id: MGAS-VAC_OUT_001
        name: 负压吸引终端
        to_system: 医疗终端
        medium: VAC
        parameters:
          vacuum_level: {value: -0.04, unit: MPa}
        
      - boundary_id: MGAS-VAC_OUT_002
        name: 真空排气
        to_system: EXTERNAL
        medium: AIR-EXH
        note: 经过滤消毒后排放

  nodes:

    source_nodes:
  
      - node_id: MGAS-VAC_SRC_PUMP_STATION
        node_name: 真空泵站
        node_name_en: Vacuum Pump Station
        node_type: Source_Node
        node_category: SRC
      
        function: 产生医用负压
        medium_in: ELEC-LV
        medium_out: VAC
      
        equipment_parameters:
          type: 水环式真空泵/油封旋片泵/干式螺杆泵
          quantity: 3（两用一备）
          single_capacity: {value: 300, unit: "m³/h"}
          ultimate_vacuum: {value: -0.09, unit: MPa}
          motor_power: {value: 7.5, unit: kW}
          noise_level: {value: "<75", unit: "dB(A)"}
          running_mode: 轮换运行，均衡磨损
      
        control_points:
          sensors:
            - point_id: VAC_TANK_PRESSURE
              point_name: 真空罐压力
              point_type: AI
              unit: MPa
              range: [-0.1, 0]
            - point_id: VAC_PUMP1_CURRENT
              point_name: 1#泵电流
              point_type: AI
              unit: A
            - point_id: VAC_PUMP2_CURRENT
              point_name: 2#泵电流
              point_type: AI
              unit: A
            - point_id: VAC_PUMP3_CURRENT
              point_name: 3#泵电流
              point_type: AI
              unit: A
          status:
            - point_id: VAC_PUMP1_RUN
              point_name: 1#泵运行
              point_type: DI
            - point_id: VAC_PUMP2_RUN
              point_name: 2#泵运行
              point_type: DI
            - point_id: VAC_PUMP3_RUN
              point_name: 3#泵运行
              point_type: DI
            - point_id: VAC_PUMP1_FAULT
              point_name: 1#泵故障
              point_type: DI
            - point_id: VAC_PUMP2_FAULT
              point_name: 2#泵故障
              point_type: DI
            - point_id: VAC_PUMP3_FAULT
              point_name: 3#泵故障
              point_type: DI
            - point_id: VAC_LOW_VACUUM
              point_name: 真空度低报警
              point_type: DI
          commands:
            - point_id: VAC_PUMP1_START
              point_name: 1#泵启动
              point_type: DO
            - point_id: VAC_PUMP2_START
              point_name: 2#泵启动
              point_type: DO
            - point_id: VAC_PUMP3_START
              point_name: 3#泵启动
              point_type: DO
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 真空泵房
          floor: B1/屋面
          area_requirement: {value: ">30", unit: "m²"}
      
        installation_requirements:
          - 良好通风（换气≥10次/h）
          - 减振基础
          - 噪声控制
          - 排气管道引至室外
          - 排气口远离人员活动区

    distribution_nodes:
  
      - node_id: MGAS-VAC_DST_TANK
        node_name: 真空储气罐
        node_name_en: Vacuum Reservoir Tank
        node_type: Distribution_Node
        node_subtype: BUF
        node_category: DST
      
        function: 稳定真空度，缓冲用气波动
        medium_in: VAC
        medium_out: VAC
      
        equipment_parameters:
          type: 立式真空罐
          volume: {value: 1000, unit: L}
          working_pressure: {value: -0.1~0, unit: MPa}
          material: 碳钢+内防腐
          drain: 底部自动排液
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 真空泵房

      - node_id: MGAS-VAC_DST_FILTER
        node_name: 细菌过滤器
        node_name_en: Bacterial Filter
        node_type: Distribution_Node
        node_subtype: FLT
        node_category: DST
      
        function: 过滤吸引物，防止污染
        medium_in: VAC
        medium_out: VAC
      
        equipment_parameters:
          type: HEPA过滤器
          efficiency: ">99.97%@0.3μm"
          quantity: 2（一用一备）
          differential_pressure_alarm: {value: 500, unit: Pa}
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 真空泵房

      - node_id: MGAS-VAC_DST_MAIN_PIPE
        node_name: 负压主管
        node_name_en: Vacuum Main Pipe
        node_type: Distribution_Node
        node_subtype: TRK
        node_category: DST
      
        function: 负压主管输送
        medium_in: VAC
        medium_out: VAC
      
        equipment_parameters:
          material: 镀锌钢管/不锈钢管
          diameter: {value: "DN65-DN100", unit: mm}
          slope: ">0.5%（向真空泵方向）"
      
        location_hint:
          space_type: SHAFT
          shaft_type: 医疗气体管井

      - node_id: MGAS-VAC_DST_RISER
        node_name: 负压立管
        node_name_en: Vacuum Riser
        node_type: Distribution_Node
        node_subtype: TRK
        node_category: DST
      
        function: 负压竖向输送至各楼层
        medium_in: VAC
        medium_out: VAC
      
        multiplicity: multiple
        instance_pattern: MGAS-VAC_DST_RISER_{Zone}
      
        equipment_parameters:
          material: 镀锌钢管
          diameter: {value: "DN40-DN50", unit: mm}
      
        location_hint:
          space_type: SHAFT
          shaft_type: 医疗气体管井

      - node_id: MGAS-VAC_DST_ZONE_VALVE
        node_name: 区域阀门箱
        node_name_en: Zone Valve Box
        node_type: Distribution_Node
        node_subtype: REG
        node_category: DST
      
        function: 区域供气控制及报警
        medium_in: VAC
        medium_out: VAC
      
        multiplicity: multiple
        instance_pattern: MGAS-VAC_DST_ZONE_VALVE_{Floor}_{Zone}
      
        equipment_parameters:
          type: 区域阀门箱（负压）
          components:
            - 区域截止阀
            - 真空表
            - 区域报警器
      
        control_points:
          sensors:
            - point_id: VAC_ZONE_PRESSURE
              point_name: 区域真空度
              point_type: AI
              unit: MPa
          status:
            - point_id: VAC_ZONE_LOW_ALARM
              point_name: 真空度低报警
              point_type: DI
      
        alarm_settings:
          low_vacuum: {value: -0.02, unit: MPa, note: "真空度不足报警"}
      
        location_hint:
          space_type: CORRIDOR
          position: 护士站附近

      - node_id: MGAS-VAC_DST_BRANCH
        node_name: 负压支管
        node_name_en: Vacuum Branch Pipe
        node_type: Distribution_Node
        node_subtype: BRH
        node_category: DST
      
        function: 楼层内水平输送至终端
        medium_in: VAC
        medium_out: VAC
      
        multiplicity: multiple
      
        equipment_parameters:
          material: 镀锌钢管/不锈钢管
          diameter: {value: "DN15-DN25", unit: mm}
      
        location_hint:
          space_type: CEILING_VOID

    sink_nodes:
  
      - node_id: MGAS-VAC_SNK_TERMINAL
        node_name: 负压吸引终端
        node_name_en: Vacuum Outlet Terminal
        node_type: Sink_Node
        node_category: SNK
      
        function: 床旁/手术室负压使用点
        medium_in: VAC
        medium_out: VAC (to suction device)
      
        is_boundary_output: true
      
        multiplicity: multiple
        instance_pattern: MGAS-VAC_SNK_TERMINAL_{Floor}_{Room}_{Seq}
        typical_quantity: 大量（按床位数）
      
        equipment_parameters:
          type: 快速插拔式终端
          gas_specific: 负压专用
          color_coding: 黄色
          vacuum_level: {value: -0.04, unit: MPa}
          flow_rate: {value: "0-30", unit: "L/min"}
          mounting: 设备带/吊塔
      
        location_hint:
          space_type: 病房/手术室/ICU
          position: 床头设备带

  edges:

    pump_edges:
      - edge_id: MGAS-VAC_EDGE_001
        edge_name: 真空泵至储气罐
        edge_type: PIP
        from_node: MGAS-VAC_SRC_PUMP_STATION
        to_node: MGAS-VAC_DST_TANK
        direction: unidirectional
        medium: VAC
      
      - edge_id: MGAS-VAC_EDGE_002
        edge_name: 储气罐至过滤器
        edge_type: PIP
        from_node: MGAS-VAC_DST_TANK
        to_node: MGAS-VAC_DST_FILTER
        direction: unidirectional
        medium: VAC

    distribution_edges:
      - edge_id: MGAS-VAC_EDGE_011
        edge_name: 过滤器至主管
        edge_type: PIP
        from_node: MGAS-VAC_DST_FILTER
        to_node: MGAS-VAC_DST_MAIN_PIPE
        direction: unidirectional
        medium: VAC
      
      - edge_id: MGAS-VAC_EDGE_012
        edge_name: 主管至立管
        edge_type: PIP
        from_node: MGAS-VAC_DST_MAIN_PIPE
        to_node: MGAS-VAC_DST_RISER
        direction: unidirectional
        medium: VAC
        multiplicity: multiple
      
      - edge_id: MGAS-VAC_EDGE_013
        edge_name: 立管至区域阀门箱
        edge_type: PIP
        from_node: MGAS-VAC_DST_RISER
        to_node: MGAS-VAC_DST_ZONE_VALVE
        direction: unidirectional
        medium: VAC
      
      - edge_id: MGAS-VAC_EDGE_014
        edge_name: 区域阀门箱至支管
        edge_type: PIP
        from_node: MGAS-VAC_DST_ZONE_VALVE
        to_node: MGAS-VAC_DST_BRANCH
        direction: unidirectional
        medium: VAC
      
      - edge_id: MGAS-VAC_EDGE_015
        edge_name: 支管至终端
        edge_type: PIP
        from_node: MGAS-VAC_DST_BRANCH
        to_node: MGAS-VAC_SNK_TERMINAL
        direction: unidirectional
        medium: VAC
        multiplicity: multiple

  typical_paths:

    - path_id: MGAS-VAC_PATH_MAIN
      path_name: 负压吸引主路径
      path_type: SUP
      description: 真空泵至终端的负压供应
      sequence:
        - step: 1
          node: MGAS-VAC_SRC_PUMP_STATION
          action: 真空泵产生负压
        - step: 2
          node: MGAS-VAC_DST_TANK
          action: 真空储罐稳压缓冲
        - step: 3
          node: MGAS-VAC_DST_FILTER
          action: 细菌过滤
        - step: 4
          node: MGAS-VAC_DST_MAIN_PIPE
          action: 主管输送
        - step: 5
          node: MGAS-VAC_DST_RISER
          action: 立管输送
        - step: 6
          node: MGAS-VAC_DST_ZONE_VALVE
          action: 区域控制
        - step: 7
          node: MGAS-VAC_DST_BRANCH
          action: 支管分配
        - step: 8
          node: MGAS-VAC_SNK_TERMINAL
          action: 终端吸引

  control_logic:

    pump_control:
      name: 真空泵控制逻辑
    
      pressure_based:
        description: 压力控制启停
        start_pressure: {value: -0.03, unit: MPa, note: "真空度降至此值启动"}
        stop_pressure: {value: -0.06, unit: MPa, note: "真空度达到此值停止"}
      
      sequence:
        description: 泵组轮换
        logic: |
          1. 正常运行一台泵
          2. 真空度不足时自动启动第二台
          3. 泵组按累计运行时间轮换
          4. 故障时自动启用备用泵
        
      protection:
        - 电机过流保护
        - 运行超时保护
        - 连续启动次数限制

  alarm_protection:
  
    critical_alarms:
      - alarm_id: ALM_VAC_LOW
        alarm_name: 真空度低报警
        severity: HIGH
        trigger: 真空度>-0.02MPa
        action: 检查真空泵，增加运行台数
      
      - alarm_id: ALM_VAC_PUMP_ALL_FAIL
        alarm_name: 真空泵全故障
        severity: CRITICAL
        trigger: 所有真空泵故障
        action: 紧急通知，启动应急预案
```

---

## 系统 2.6: MGAS-AIR 医用压缩空气系统

```yaml
System_Topology:

  identity:
    system_id: MGAS-AIR
    system_name: 医用压缩空气系统
    system_name_en: Medical Compressed Air System
    system_category: MGAS
    system_type: 医用气体-压缩空气
    priority_level: P0-LIFE_SAFETY
  
    description: |
      医院医用压缩空气系统，为呼吸机、牙科设备、手术器械等提供洁净干燥的压缩空气。
      空气压缩机组产生压缩空气，经干燥、过滤后输送至各终端。
      系统需满足《中国药典》医用压缩空气质量标准。
  
    design_basis:
      gas_type: 医用压缩空气
      supply_pressure: {value: 0.4, unit: MPa}
      quality_grade:
        particles: "ISO 8573-1 Class 1"
        water: "露点-40℃"
        oil: "<0.01mg/m³"
      terminal_flow: {value: 100, unit: "L/min", note: "单终端最大流量"}
  
    design_standards:
      - GB 50751-2012 医用气体工程技术规范
      - ISO 8573-1 压缩空气质量等级
      - 《中国药典》医用压缩空气标准
  
    version: 1.0
    last_updated: 2024

  boundary:
    inputs:
      - boundary_id: MGAS-AIR_IN_001
        name: 新风进气
        from_system: EXTERNAL
        medium: AIR-OA
      
      - boundary_id: MGAS-AIR_IN_002
        name: 电力供应
        from_system: ELEC-LV-MAIN
        medium: ELEC-LV
      
    outputs:
      - boundary_id: MGAS-AIR_OUT_001
        name: 医用压缩空气终端
        to_system: 医疗终端
        medium: AIR-MED
        parameters:
          pressure: {value: 0.4, unit: MPa}
          quality: 符合药典标准

  nodes:

    source_nodes:
  
      - node_id: MGAS-AIR_SRC_COMPRESSOR
        node_name: 医用空气压缩机组
        node_name_en: Medical Air Compressor Station
        node_type: Source_Node
        node_category: SRC
      
        function: 产生医用压缩空气
        medium_in: AIR-OA
        medium_out: AIR-COMP
      
        equipment_parameters:
          type: 无油涡旋压缩机/无油螺杆压缩机
          quantity: 3（两用一备）
          single_capacity: {value: 1.5, unit: "m³/min"}
          working_pressure: {value: 0.8, unit: MPa}
          oil_free: true  # 无油压缩
          noise_level: {value: "<70", unit: "dB(A)"}
          cooling: 风冷/水冷
          intake_filter: 进气过滤器
      
        control_points:
          sensors:
            - point_id: COMP_OUTLET_P
              point_name: 排气压力
              point_type: AI
              unit: MPa
            - point_id: COMP_OUTLET_T
              point_name: 排气温度
              point_type: AI
              unit: ℃
            - point_id: COMP1_CURRENT
              point_name: 1#压缩机电流
              point_type: AI
              unit: A
            - point_id: COMP_RUN_HOURS
              point_name: 运行时间
              point_type: AI
              unit: h
          status:
            - point_id: COMP1_RUN
              point_name: 1#压缩机运行
              point_type: DI
            - point_id: COMP2_RUN
              point_name: 2#压缩机运行
              point_type: DI
            - point_id: COMP3_RUN
              point_name: 3#压缩机运行
              point_type: DI
            - point_id: COMP1_FAULT
              point_name: 1#压缩机故障
              point_type: DI
            - point_id: COMP_HIGH_TEMP
              point_name: 排气超温
              point_type: DI
          commands:
            - point_id: COMP1_START
              point_name: 1#压缩机启动
              point_type: DO
            - point_id: COMP2_START
              point_name: 2#压缩机启动
              point_type: DO
            - point_id: COMP3_START
              point_name: 3#压缩机启动
              point_type: DO
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 压缩空气站房
          floor: B1/屋面
          area_requirement: {value: ">40", unit: "m²"}
      
        installation_requirements:
          - 良好通风（散热）
          - 进气口远离污染源
          - 进气过滤
          - 减振基础
          - 排水设施

    distribution_nodes:
  
      - node_id: MGAS-AIR_DST_TANK
        node_name: 储气罐
        node_name_en: Air Receiver Tank
        node_type: Distribution_Node
        node_subtype: BUF
        node_category: DST
      
        function: 稳定压力，缓冲用气波动
        medium_in: AIR-COMP
        medium_out: AIR-COMP
      
        equipment_parameters:
          type: 立式储气罐
          volume: {value: 1500, unit: L}
          working_pressure: {value: 1.0, unit: MPa}
          material: 碳钢
          safety_valve: 双安全阀
          drain: 自动排水器
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 压缩空气站房

      - node_id: MGAS-AIR_DST_DRYER
        node_name: 冷冻式干燥机
        node_name_en: Refrigerated Air Dryer
        node_type: Distribution_Node
        node_subtype: TRF
        node_category: DST
      
        function: 压缩空气干燥除水
        medium_in: AIR-COMP
        medium_out: AIR-DRY
      
        equipment_parameters:
          type: 冷冻式干燥机 + 吸附式干燥机
          quantity: 2（一用一备）
          capacity: {value: 3, unit: "m³/min"}
          pressure_dew_point: {value: -40, unit: ℃}
          pressure_drop: {value: "<0.02", unit: MPa}
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 压缩空气站房

      - node_id: MGAS-AIR_DST_FILTER_GROUP
        node_name: 过滤器组
        node_name_en: Filter Group
        node_type: Distribution_Node
        node_subtype: FLT
        node_category: DST
      
        function: 多级过滤去除颗粒、油雾
        medium_in: AIR-DRY
        medium_out: AIR-MED
      
        equipment_parameters:
          type: 三级过滤
          stages:
            - stage: 1
              type: 预过滤器
              efficiency: "3μm"
            - stage: 2
              type: 精过滤器
              efficiency: "0.01μm"
            - stage: 3
              type: 活性炭过滤器
              function: 除油除味
          quantity: 2（一用一备）
          differential_pressure_alarm: {value: 0.05, unit: MPa}
      
        control_points:
          sensors:
            - point_id: FILTER_DP
              point_name: 过滤器压差
              point_type: AI
              unit: MPa
          status:
            - point_id: FILTER_ALARM
              point_name: 过滤器堵塞报警
              point_type: DI
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 压缩空气站房

      - node_id: MGAS-AIR_DST_REGULATOR
        node_name: 减压装置
        node_name_en: Pressure Regulator
        node_type: Distribution_Node
        node_subtype: REG
        node_category: DST
      
        function: 减压至供气压力
        medium_in: AIR-MED
        medium_out: AIR-MED
      
        equipment_parameters:
          type: 减压阀组
          inlet_pressure: {value: 0.8, unit: MPa}
          outlet_pressure: {value: 0.5, unit: MPa}
          quantity: 2（一用一备）
      
        control_points:
          sensors:
            - point_id: AIR_OUTLET_P
              point_name: 输出压力
              point_type: AI
              unit: MPa
          status:
            - point_id: AIR_HIGH_P_ALARM
              point_name: 高压报警
              point_type: DI
            - point_id: AIR_LOW_P_ALARM
              point_name: 低压报警
              point_type: DI
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 压缩空气站房

      - node_id: MGAS-AIR_DST_MAIN_PIPE
        node_name: 压缩空气主管
        node_name_en: Compressed Air Main Pipe
        node_type: Distribution_Node
        node_subtype: TRK
        node_category: DST
      
        function: 压缩空气主管输送
        medium_in: AIR-MED
        medium_out: AIR-MED
      
        equipment_parameters:
          material: 不锈钢管/脱脂铜管
          diameter: {value: "DN40-DN65", unit: mm}
      
        location_hint:
          space_type: SHAFT
          shaft_type: 医疗气体管井

      - node_id: MGAS-AIR_DST_RISER
        node_name: 压缩空气立管
        node_name_en: Compressed Air Riser
        node_type: Distribution_Node
        node_subtype: TRK
        node_category: DST
      
        function: 压缩空气竖向输送
        medium_in: AIR-MED
        medium_out: AIR-MED
      
        multiplicity: multiple
      
        equipment_parameters:
          material: 不锈钢管/脱脂铜管
          diameter: {value: "DN20-DN32", unit: mm}
      
        location_hint:
          space_type: SHAFT

      - node_id: MGAS-AIR_DST_ZONE_VALVE
        node_name: 区域阀门箱
        node_name_en: Zone Valve Box
        node_type: Distribution_Node
        node_subtype: REG
        node_category: DST
      
        function: 区域供气控制及二级减压
        medium_in: AIR-MED
        medium_out: AIR-MED
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 区域阀门箱
          components:
            - 区域截止阀
            - 减压阀（0.5MPa→0.4MPa）
            - 压力表
            - 区域报警器
      
        control_points:
          sensors:
            - point_id: AIR_ZONE_P
              point_name: 区域压力
              point_type: AI
              unit: MPa
          status:
            - point_id: AIR_ZONE_ALARM
              point_name: 区域报警
              point_type: DI
      
        location_hint:
          space_type: CORRIDOR

      - node_id: MGAS-AIR_DST_BRANCH
        node_name: 压缩空气支管
        node_name_en: Compressed Air Branch Pipe
        node_type: Distribution_Node
        node_subtype: BRH
        node_category: DST
      
        function: 楼层内水平输送
        medium_in: AIR-MED
        medium_out: AIR-MED
      
        multiplicity: multiple
      
        equipment_parameters:
          material: 不锈钢管/脱脂铜管
          diameter: {value: "DN10-DN20", unit: mm}
      
        location_hint:
          space_type: CEILING_VOID

    sink_nodes:
  
      - node_id: MGAS-AIR_SNK_TERMINAL
        node_name: 压缩空气终端
        node_name_en: Compressed Air Outlet Terminal
        node_type: Sink_Node
        node_category: SNK
      
        function: 床旁/手术室压缩空气使用点
        medium_in: AIR-MED
        medium_out: AIR-MED (to equipment)
      
        is_boundary_output: true
      
        multiplicity: multiple
        instance_pattern: MGAS-AIR_SNK_TERMINAL_{Floor}_{Room}_{Seq}
      
        equipment_parameters:
          type: 快速插拔式终端
          gas_specific: 压缩空气专用
          color_coding: 黄色/黑白
          pressure: {value: 0.4, unit: MPa}
          flow_rate: {value: "0-100", unit: "L/min"}
      
        location_hint:
          space_type: 病房/手术室
          position: 设备带/吊塔

      - node_id: MGAS-AIR_SNK_DENTAL
        node_name: 牙科压缩空气终端
        node_name_en: Dental Air Terminal
        node_type: Sink_Node
        node_category: SNK
      
        function: 牙科诊疗椅压缩空气供应
        medium_in: AIR-MED
        medium_out: AIR-MED (to dental unit)
      
        is_boundary_output: true
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 牙科用终端
          pressure: {value: 0.4, unit: MPa}
          flow_rate: {value: "0-60", unit: "L/min"}
      
        location_hint:
          space_type: 口腔科诊室

  edges:

    production_edges:
      - edge_id: MGAS-AIR_EDGE_001
        edge_name: 压缩机至储气罐
        edge_type: PIP
        from_node: MGAS-AIR_SRC_COMPRESSOR
        to_node: MGAS-AIR_DST_TANK
        direction: unidirectional
        medium: AIR-COMP
      
      - edge_id: MGAS-AIR_EDGE_002
        edge_name: 储气罐至干燥机
        edge_type: PIP
        from_node: MGAS-AIR_DST_TANK
        to_node: MGAS-AIR_DST_DRYER
        direction: unidirectional
        medium: AIR-COMP
      
      - edge_id: MGAS-AIR_EDGE_003
        edge_name: 干燥机至过滤器
        edge_type: PIP
        from_node: MGAS-AIR_DST_DRYER
        to_node: MGAS-AIR_DST_FILTER_GROUP
        direction: unidirectional
        medium: AIR-DRY
      
      - edge_id: MGAS-AIR_EDGE_004
        edge_name: 过滤器至减压装置
        edge_type: PIP
        from_node: MGAS-AIR_DST_FILTER_GROUP
        to_node: MGAS-AIR_DST_REGULATOR
        direction: unidirectional
        medium: AIR-MED

    distribution_edges:
      - edge_id: MGAS-AIR_EDGE_011
        edge_name: 减压装置至主管
        edge_type: PIP
        from_node: MGAS-AIR_DST_REGULATOR
        to_node: MGAS-AIR_DST_MAIN_PIPE
        direction: unidirectional
        medium: AIR-MED
      
      - edge_id: MGAS-AIR_EDGE_012
        edge_name: 主管至立管
        edge_type: PIP
        from_node: MGAS-AIR_DST_MAIN_PIPE
        to_node: MGAS-AIR_DST_RISER
        direction: unidirectional
        medium: AIR-MED
        multiplicity: multiple
      
      - edge_id: MGAS-AIR_EDGE_013
        edge_name: 立管至区域阀门箱
        edge_type: PIP
        from_node: MGAS-AIR_DST_RISER
        to_node: MGAS-AIR_DST_ZONE_VALVE
        direction: unidirectional
        medium: AIR-MED
      
      - edge_id: MGAS-AIR_EDGE_014
        edge_name: 区域阀门箱至支管
        edge_type: PIP
        from_node: MGAS-AIR_DST_ZONE_VALVE
        to_node: MGAS-AIR_DST_BRANCH
        direction: unidirectional
        medium: AIR-MED
      
      - edge_id: MGAS-AIR_EDGE_015
        edge_name: 支管至终端
        edge_type: PIP
        from_node: MGAS-AIR_DST_BRANCH
        to_node: MGAS-AIR_SNK_TERMINAL
        direction: unidirectional
        medium: AIR-MED
        multiplicity: multiple

  typical_paths:

    - path_id: MGAS-AIR_PATH_MAIN
      path_name: 医用压缩空气供应路径
      path_type: SUP
      sequence:
        - step: 1
          node: MGAS-AIR_SRC_COMPRESSOR
          action: 空气压缩
          parameters:
            outlet_pressure: 0.8MPa
        - step: 2
          node: MGAS-AIR_DST_TANK
          action: 储气缓冲
        - step: 3
          node: MGAS-AIR_DST_DRYER
          action: 干燥除水
          parameters:
            dew_point: -40℃
        - step: 4
          node: MGAS-AIR_DST_FILTER_GROUP
          action: 多级过滤
        - step: 5
          node: MGAS-AIR_DST_REGULATOR
          action: 一级减压
          parameters:
            outlet: 0.5MPa
        - step: 6
          node: MGAS-AIR_DST_MAIN_PIPE
          action: 主管输送
        - step: 7
          node: MGAS-AIR_DST_RISER
          action: 立管输送
        - step: 8
          node: MGAS-AIR_DST_ZONE_VALVE
          action: 二级减压
          parameters:
            outlet: 0.4MPa
        - step: 9
          node: MGAS-AIR_DST_BRANCH
          action: 支管分配
        - step: 10
          node: MGAS-AIR_SNK_TERMINAL
          action: 终端供气

  control_logic:

    compressor_control:
      name: 压缩机控制逻辑
    
      pressure_based:
        start_pressure: {value: 0.6, unit: MPa}
        stop_pressure: {value: 0.8, unit: MPa}
      
      sequence:
        logic: |
          1. 储气罐压力降至0.6MPa时启动第一台
          2. 压力继续下降至0.5MPa时启动第二台
          3. 压力达到0.8MPa时按顺序停止
          4. 轮换运行，均衡磨损
          5. 故障自动切换备用
```

---

## 系统 2.7: MGAS-N2O 笑气系统（简化版）

```yaml
System_Topology:

  identity:
    system_id: MGAS-N2O
    system_name: 笑气（一氧化二氮）系统
    system_name_en: Nitrous Oxide System
    system_category: MGAS
    system_type: 医用气体-笑气
    priority_level: P1-CRITICAL
  
    description: |
      医院医用一氧化二氮（笑气）供应系统，用于手术室麻醉。
      采用汇流排供气方式，供应压力与氧气系统一致。
      由于使用范围有限，通常仅在手术室区域设置终端。
  
    design_basis:
      gas_type: 医用一氧化二氮（N2O）
      purity: {value: ">99%", note: "符合药典标准"}
      supply_pressure: {value: 0.4, unit: MPa}
      usage_area: 手术室
  
    design_standards:
      - GB 50751-2012 医用气体工程技术规范
  
    version: 1.0
    last_updated: 2024

  boundary:
    inputs:
      - boundary_id: MGAS-N2O_IN_001
        name: 笑气气瓶供应
        from_system: EXTERNAL_CYLINDER
        medium: N2O-GAS
        parameters:
          purity: ">99%"
          pressure: {value: 4.5, unit: MPa, note: "液态N2O蒸气压"}
      
    outputs:
      - boundary_id: MGAS-N2O_OUT_001
        name: 手术室笑气终端
        to_system: 手术室
        medium: N2O-GAS
        parameters:
          pressure: {value: 0.4, unit: MPa}

  nodes:

    source_nodes:
  
      - node_id: MGAS-N2O_SRC_MANIFOLD
        node_name: 笑气汇流排
        node_name_en: N2O Cylinder Manifold
        node_type: Source_Node
        node_category: SRC
      
        function: 笑气气瓶组供气
        medium_in: N2O-GAS
        medium_out: N2O-GAS
      
        equipment_parameters:
          type: 双侧自动切换汇流排
          cylinder_per_side: 5瓶
          cylinder_volume: {value: 40, unit: L}
          auto_switching: true
          regulator: 一级减压（4.5MPa→1.0MPa）
          heating: 必要时设置加热装置（N2O气化吸热）
      
        control_points:
          sensors:
            - point_id: N2O_MANIFOLD_PRESS
              point_name: 输出压力
              point_type: AI
              unit: MPa
          status:
            - point_id: N2O_LOW_PRESS
              point_name: 低压报警
              point_type: DI
            - point_id: N2O_LEFT_ACTIVE
              point_name: 左侧供气
              point_type: DI
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 汇流排间
          note: 需通风良好，N2O有窒息风险

    distribution_nodes:
  
      - node_id: MGAS-N2O_DST_REGULATOR
        node_name: 笑气减压装置
        node_name_en: N2O Pressure Regulator
        node_type: Distribution_Node
        node_subtype: REG
        node_category: DST
      
        function: 二级减压
        medium_in: N2O-GAS
        medium_out: N2O-GAS
      
        equipment_parameters:
          type: 减压阀组
          inlet_pressure: {value: 1.0, unit: MPa}
          outlet_pressure: {value: 0.5, unit: MPa}
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 气体机房

      - node_id: MGAS-N2O_DST_PIPE
        node_name: 笑气管道
        node_name_en: N2O Pipe
        node_type: Distribution_Node
        node_subtype: TRK
        node_category: DST
      
        function: 笑气输送
        medium_in: N2O-GAS
        medium_out: N2O-GAS
      
        equipment_parameters:
          material: 脱脂紫铜管
          diameter: {value: "DN15-DN25", unit: mm}
          marking: 蓝色标识
      
        location_hint:
          space_type: CEILING_VOID
          position: 手术室区域

      - node_id: MGAS-N2O_DST_ZONE_VALVE
        node_name: 手术室区域阀门箱
        node_name_en: OR Zone Valve Box
        node_type: Distribution_Node
        node_subtype: REG
        node_category: DST
      
        function: 手术室区域供气控制
        medium_in: N2O-GAS
        medium_out: N2O-GAS
      
        equipment_parameters:
          type: 区域阀门箱（含三级减压）
          outlet_pressure: {value: 0.4, unit: MPa}
      
        control_points:
          sensors:
            - point_id: N2O_ZONE_P
              point_name: 区域压力
              point_type: AI
              unit: MPa
      
        location_hint:
          space_type: CORRIDOR
          position: 手术室走廊

    sink_nodes:
  
      - node_id: MGAS-N2O_SNK_TERMINAL
        node_name: 笑气终端
        node_name_en: N2O Outlet Terminal
        node_type: Sink_Node
        node_category: SNK
      
        function: 手术室麻醉用笑气终端
        medium_in: N2O-GAS
        medium_out: N2O-GAS (to anesthesia machine)
      
        is_boundary_output: true
      
        multiplicity: multiple
        instance_pattern: MGAS-N2O_SNK_TERMINAL_{OR_Seq}
        typical_quantity: 按手术室数量
      
        equipment_parameters:
          type: 快速插拔式终端
          gas_specific: 笑气专用（不可互换）
          color_coding: 蓝色
          pressure: {value: 0.4, unit: MPa}
      
        location_hint:
          space_type: 手术室
          position: 吊塔/设备柱

  edges:

    supply_edges:
      - edge_id: MGAS-N2O_EDGE_001
        edge_name: 汇流排至减压装置
        edge_type: PIP
        from_node: MGAS-N2O_SRC_MANIFOLD
        to_node: MGAS-N2O_DST_REGULATOR
        direction: unidirectional
        medium: N2O-GAS
      
      - edge_id: MGAS-N2O_EDGE_002
        edge_name: 减压装置至管道
        edge_type: PIP
        from_node: MGAS-N2O_DST_REGULATOR
        to_node: MGAS-N2O_DST_PIPE
        direction: unidirectional
        medium: N2O-GAS
      
      - edge_id: MGAS-N2O_EDGE_003
        edge_name: 管道至区域阀门箱
        edge_type: PIP
        from_node: MGAS-N2O_DST_PIPE
        to_node: MGAS-N2O_DST_ZONE_VALVE
        direction: unidirectional
        medium: N2O-GAS
      
      - edge_id: MGAS-N2O_EDGE_004
        edge_name: 区域阀门箱至终端
        edge_type: PIP
        from_node: MGAS-N2O_DST_ZONE_VALVE
        to_node: MGAS-N2O_SNK_TERMINAL
        direction: unidirectional
        medium: N2O-GAS
        multiplicity: multiple

  typical_paths:

    - path_id: MGAS-N2O_PATH_MAIN
      path_name: 笑气供应路径
      path_type: SUP
      sequence:
        - step: 1
          node: MGAS-N2O_SRC_MANIFOLD
          action: 汇流排供气
        - step: 2
          node: MGAS-N2O_DST_REGULATOR
          action: 一级减压
        - step: 3
          node: MGAS-N2O_DST_PIPE
          action: 管道输送
        - step: 4
          node: MGAS-N2O_DST_ZONE_VALVE
          action: 二级减压
        - step: 5
          node: MGAS-N2O_SNK_TERMINAL
          action: 终端供气
```

---

# 第二批次输出完成

## 批次总结

| 系统ID | 系统名称 | 类别 | 优先级 | 节点数 | 边数 |
|--------|----------|------|--------|--------|------|
| ELEC-HV | 高压配电系统 | ELEC | P0 | ~15 | ~12 |
| ELEC-LV-MAIN | 低压配电主系统 | ELEC | P0 | ~20 | ~15 |
| ELEC-EPS | 应急电源系统 | ELEC | P0 | ~10 | ~8 |
| MGAS-O2 | 医用氧气系统 | MGAS | P0 | ~12 | ~10 |
| MGAS-VAC | 医用负压吸引系统 | MGAS | P0 | ~10 | ~8 |
| MGAS-AIR | 医用压缩空气系统 | MGAS | P0 | ~12 | ~10 |
| MGAS-N2O | 笑气系统 | MGAS | P1 | ~6 | ~4 |

## 关键控制逻辑覆盖

| 系统 | 关键控制逻辑 |
|------|--------------|
| ELEC-HV | 高压自动切换(ATS)、保护配合 |
| ELEC-LV-MAIN | 发电机自动启动/停机、低压ATS控制、负荷分级 |
| ELEC-EPS | 双机并联运行、UPS运行模式、蓄电池管理 |
| MGAS-O2 | 气源自动切换、汇流排切换、三级报警 |
| MGAS-VAC | 真空泵压力控制、泵组轮换 |
| MGAS-AIR | 压缩机压力控制、轮换运行 |

---

# Agent-01 系统拓扑建模师 - 第二批次修订版

## 修订说明

根据评审意见，本次修订重点解决以下高优先级缺陷：
- **E1**: 发电机黑启动失败处理逻辑
- **E2**: UPS电池SOC分级管理
- **E3**: 低压系统黑启动详细时序
- **G1**: 医用气体备用源耗尽保护
- **G2**: 医用气体终端反向污染防护
- **G3**: 医用氧气纯度监测
- **G4**: 手术室O2/VAC协调逻辑
- **E4**: 变压器冷却系统控制

---

# 电气系统（修订版）

## 系统 2.1: ELEC-HV 高压配电系统（修订版 - 关键补充）

在原有内容基础上，补充以下控制逻辑：

```yaml
  # ========================================
  # CONTROL LOGIC SECTION - 控制逻辑（修订补充）
  # ========================================
  control_logic:

    # === 原有内容保留 ===
    auto_transfer_switch:
      # ... 原有内容 ...
  
    protection_coordination:
      # ... 原有内容 ...
  
    # === E1修复：高压系统故障恢复逻辑 ===
    fault_recovery_logic:
      name: 高压系统故障恢复逻辑
      description: 双路市电故障后的恢复策略
    
      single_utility_failure:
        description: 单路市电故障
        detection:
          voltage_threshold: "<70%额定值"
          duration: "持续2秒"
        recovery_sequence:
          - step: 1
            action: 故障路进线断路器分闸
            time: 0.5s
          - step: 2
            action: 确认母线失压
            time: 0.3s
          - step: 3
            action: 母联断路器合闸
            time: 0.5s
            condition: 另一路电源正常
          - step: 4
            action: 故障母线恢复供电
            note: 由正常路经母联供电
        total_time: "<3秒"
      
      dual_utility_failure:
        description: 双路市电同时故障
        detection: 两路进线电压均<70%额定值
        action: 立即启动发电机
        escalation: 通知值班人员和电力公司
      
      utility_recovery_after_generator:
        description: 发电机运行中市电恢复
        procedure:
          - step: 1
            action: 确认市电电压/频率稳定
            duration: 30s
          - step: 2
            action: 合闸市电进线断路器
            condition: 市电正常持续30秒
          - step: 3
            action: 同期并列（如允许）或先断后合
            note: 医院通常采用"先断后合"避免并列风险
          - step: 4
            action: 发电机卸载并停机
            delay: 冷却运行3分钟后停机
        mode: 可选自动/手动

    # === 保护动作后的闭锁逻辑 ===
    protection_lockout:
      name: 保护动作闭锁逻辑
      description: 保护动作后防止误合闸
    
      lockout_conditions:
        - 短路保护动作
        - 差动保护动作
        - 接地保护动作
      
      lockout_action:
        - 断路器分闸后闭锁
        - 禁止远程合闸
        - 必须现场人工确认后解锁
        - 故障录波记录保存
      
      unlock_procedure:
        - step: 1
          action: 现场检查故障原因
        - step: 2
          action: 确认故障已排除
        - step: 3
          action: 手动复位保护装置
        - step: 4
          action: 解除闭锁
        - step: 5
          action: 试送电（可远程操作）
```

---

## 系统 2.2: ELEC-LV-MAIN 低压配电主系统（修订版）

```yaml
System_Topology:

  identity:
    system_id: ELEC-LV-MAIN
    system_name: 低压配电主系统
    system_name_en: Low Voltage Main Distribution System
    # ... 原有identity内容保留 ...
  
    version: 2.0
    revision_notes: |
      v2.0: 补充黑启动时序、变压器冷却控制、负荷分级切电
      v1.0: 初始版本

  # ... boundary, nodes, edges 原有内容保留 ...

  # ========================================
  # CONTROL LOGIC SECTION - 控制逻辑（完整修订版）
  # ========================================
  control_logic:

    # === E3修复：完整黑启动时序 ===
    black_start_sequence:
      name: 低压系统黑启动时序
      description: 双路市电全失后的应急启动完整流程
    
      trigger:
        condition: 双路市电均失压
        detection: 
          - ATS主电源失压
          - ATS备用电源失压
          - 持续时间>3秒
    
      phase_1_detection:
        name: 失电检测与确认
        steps:
          - step: 1
            time: "T+0s"
            action: ATS检测到主电源失压
            sensor: ATS1_MAIN_AVAIL = OFF
          - step: 2
            time: "T+0.5s"
            action: ATS检测到备用电源也失压
            sensor: ATS1_BACKUP_AVAIL = OFF
          - step: 3
            time: "T+3s"
            action: 确认双路市电全失（防误判）
            condition: 持续3秒无恢复
          - step: 4
            time: "T+3s"
            action: 发送启动信号至发电机控制器
            signal: GEN_START_CMD = ON
    
      phase_2_generator_start:
        name: 发电机启动
        steps:
          - step: 5
            time: "T+3.5s"
            action: 发电机控制器接收启动信号
          - step: 6
            time: "T+4s"
            action: 燃油预供、预热（如有）
          - step: 7
            time: "T+5s"
            action: 启动马达启动发动机
          - step: 8
            time: "T+8s"
            action: 发动机达到额定转速（1500rpm）
            verification: GEN_SPEED ≈ 1500rpm
          - step: 9
            time: "T+10s"
            action: 发电机电压/频率稳定
            verification: |
              GEN_V = 400V ±5%
              GEN_FREQ = 50Hz ±1Hz
    
      phase_3_connection:
        name: 发电机并网
        steps:
          - step: 10
            time: "T+11s"
            action: 发电机出口断路器合闸
            location: 发电机房内
            condition: 电压频率合格
          - step: 11
            time: "T+12s"
            action: 确认发电机向母线供电
            verification: GEN_PANEL_CB_ON = ON
          - step: 12
            time: "T+13s"
            action: ATS切换至发电机侧
            verification: ATS1_POS = BACKUP
          - step: 13
            time: "T+14s"
            action: 应急母线恢复供电
            verification: BUS_E1电压正常
    
      phase_4_load_staging:
        name: 分级加载
        description: 防止发电机过载掉频
        steps:
          - step: 14
            time: "T+15s"
            action: 第一级负荷合闸
            loads: 
              - UPS输入（手术室、ICU）
              - 消防设备
              - 应急照明
            load_percentage: 30%
          - step: 15
            time: "T+20s"
            action: 第二级负荷合闸
            loads:
              - 电梯（至少1台）
              - 重要医疗设备
            load_percentage: 60%
          - step: 16
            time: "T+25s"
            action: 第三级负荷合闸
            loads:
              - 其他应急负荷
            load_percentage: 80-100%
          - step: 17
            time: "T+30s"
            action: 系统稳定运行
            verification: |
              发电机负载率<90%
              频率稳定在50Hz±0.5Hz
    
      total_time: "<30秒（从失电到全部应急负荷恢复）"
      critical_time: "<15秒（一级重要负荷恢复）"
    
      frequency_protection:
        description: 发电机过载保护
        underfrequency_threshold: 
          warning: 49Hz
          trip: 47Hz
        action_on_underfrequency:
          - 自动切除非关键负荷
          - 防止发电机失速
        load_shedding_priority:
          1: 非关键照明
          2: 普通电梯
          3: 空调系统（部分）
          note: UPS/消防/生命支持设备不可切除

    # === E1修复：发电机启动失败处理 ===
    generator_start_failure_handling:
      name: 发电机启动失败处理
      description: 发电机启动失败后的应急措施
    
      failure_detection:
        condition: 启动命令发出后10秒内未检测到运行
        detection: GEN_START_CMD = ON 且 GEN_RUN = OFF 持续10秒
      
      auto_retry:
        max_attempts: 3
        interval: 10s
        sequence:
          - attempt: 1
            time: "T+10s后"
            action: 第一次重试
          - attempt: 2
            time: "T+20s后"
            action: 第二次重试
          - attempt: 3
            time: "T+30s后"
            action: 第三次重试（最后一次）
    
      single_generator_failure:
        description: 双机配置时单机故障
        action:
          - step: 1
            action: 停止故障机组重试
          - step: 2
            action: 立即启动备用机组
          - step: 3
            action: 备用机组带全部应急负荷
          - step: 4
            action: 报警通知维护人员
        recovery_time: 额外增加5-8秒
    
      all_generators_failure:
        description: 所有发电机均启动失败（极端情况）
        trigger: 所有机组3次重试均失败
        immediate_actions:
          - action: 触发EMERGENCY级别报警
            target: 医院总指挥中心、设备科、院办
          - action: 启动医院应急预案
            plan: 《全院停电应急预案》
        contingency_measures:
          - measure: UPS电池继续供电
            duration: 15-30分钟
          - measure: 联系外部移动发电车
            response_time: 期望30分钟内到达
          - measure: 关键手术转移至有电区域
          - measure: 呼吸机等生命支持设备手动操作
        notification:
          - 值班院领导
          - 设备科负责人
          - 电力公司（请求优先恢复）
          - 卫生主管部门（重大事件上报）
    
      parallel_sync_failure:
        description: 双机并联同期失败
        condition: 同期条件不满足持续30秒
        action:
          - step: 1
            action: 放弃并联，1#机组单独带负荷
          - step: 2
            action: 2#机组停机待命
          - step: 3
            action: 报警通知维护人员检查同期装置
        fallback: 单机运行模式

    # === 发电机自动停机（原有内容优化）===
    generator_auto_stop:
      name: 发电机自动停机逻辑
    
      trigger:
        condition: 市电恢复正常
        detection: ATS主电源恢复正常持续30秒
      
      pre_transfer_check:
        description: 切换前检查
        checks:
          - item: 市电电压
            requirement: 380V ±10%
            duration: 稳定30秒
          - item: 市电频率
            requirement: 50Hz ±1Hz
            duration: 稳定30秒
          - item: 市电相序
            requirement: 正确
    
      transfer_sequence:
        description: 切回市电流程
        method: 先断后合（非同期切换）
        steps:
          - step: 1
            action: 确认市电稳定30秒
          - step: 2
            action: ATS分闸发电机侧
          - step: 3
            action: 短暂失电（<100ms）
            note: UPS保证关键负荷不中断
          - step: 4
            action: ATS合闸市电侧
          - step: 5
            action: 应急母线由市电供电
    
      cool_down_sequence:
        description: 发电机冷却停机
        steps:
          - step: 1
            action: 发电机出口断路器分闸
          - step: 2
            action: 发电机空载运行
            duration: 180s（3分钟）
            purpose: 冷却发动机，保护涡轮增压器
          - step: 3
            action: 发电机停机
          - step: 4
            action: 冷却风机继续运行
            duration: 60s
          - step: 5
            action: 系统恢复待机状态
            verification: GEN_READY = ON

    # === E4修复：变压器冷却系统控制 ===
    transformer_cooling_control:
      name: 变压器冷却系统控制
      description: 干式变压器风冷系统控制逻辑
    
      temperature_based_control:
        description: 基于温度的风机控制
        normal_operation:
          fan_start_temp: 100℃
          fan_stop_temp: 85℃
          hysteresis: 15℃
        forced_cooling:
          condition: 温度>120℃
          action: 强制风机高速运行
      
      load_based_control:
        description: 基于负载的风机控制
        low_load:
          condition: 负载率<50%
          action: 风机可停止
        medium_load:
          condition: 负载率50-80%
          action: 风机低速运行
        high_load:
          condition: 负载率>80%
          action: 风机高速运行
        overload:
          condition: 负载率>100%
          action: 风机全速+报警
    
      seasonal_strategy:
        summer:
          description: 夏季策略（环境温度>30℃）
          fan_start_temp: 90℃
          fan_stop_temp: 75℃
          preemptive: 负载率>60%时提前启动
        winter:
          description: 冬季策略（环境温度<10℃）
          fan_start_temp: 110℃
          fan_stop_temp: 90℃
          note: 可减少风机运行时间
        transition:
          description: 过渡季
          follow_normal: true
    
      protection:
        overtemperature_warning:
          threshold: 130℃
          action: 报警，强制风冷
        overtemperature_alarm:
          threshold: 145℃
          action: 高级报警，准备切换
        overtemperature_trip:
          threshold: 155℃
          action: 变压器保护跳闸
          note: 需减少该变压器负荷或切换至备用
    
      control_points:
        - point_id: TX_TEMP_MAX
          point_name: 变压器最高温度
          point_type: AI
          unit: ℃
          note: 取三相最高值
        - point_id: TX_FAN_MODE
          point_name: 风机控制模式
          point_type: AO
          values: [OFF, LOW, HIGH, AUTO]
        - point_id: TX_FAN_FAULT
          point_name: 风机故障
          point_type: DI

    # === 负荷分级管理 ===
    load_classification_management:
      name: 负荷分级管理
      description: 按重要程度对负荷进行分级管理
    
      classification:
        level_0_life_critical:
          name: 生命攸关负荷
          examples:
            - 手术室医疗设备
            - ICU/CCU监护设备
            - 呼吸机
            - 血液透析机
          power_source: 市电 + 发电机 + UPS
          max_interruption: 0ms
          shedding_allowed: false
        
        level_1_critical:
          name: 一级重要负荷
          examples:
            - 急诊抢救室设备
            - 新生儿科设备
            - 产房设备
            - 消防设备
            - 电梯（至少1台）
          power_source: 市电 + 发电机
          max_interruption: 15s
          shedding_allowed: false
        
        level_2_important:
          name: 二级重要负荷
          examples:
            - 普通病房照明
            - 医技科室设备
            - 药房冷藏设备
          power_source: 市电 + 发电机（可延迟）
          max_interruption: 30s
          shedding_allowed: 极端情况可
        
        level_3_general:
          name: 三级一般负荷
          examples:
            - 行政办公区
            - 后勤区域
            - 空调系统（非关键）
          power_source: 市电
          max_interruption: 无限制
          shedding_allowed: true

      emergency_load_shedding:
        description: 紧急切负荷策略
        trigger:
          - 发电机过载（负载率>100%）
          - 发电机频率下降（<48Hz）
          - 电池电量过低（UPS）
        shedding_sequence:
          - step: 1
            shed: 三级负荷
            action: 切除非关键照明、空调
          - step: 2
            shed: 部分二级负荷
            action: 保留关键二级负荷
          - step: 3
            shed: 不可再切
            action: 仅保留生命攸关和一级负荷
            note: 此时必须解决电源问题
```

---

## 系统 2.3: ELEC-EPS 应急电源系统（修订版 - UPS电池管理）

```yaml
  # ========================================
  # CONTROL LOGIC SECTION - 控制逻辑（E2修复补充）
  # ========================================
  control_logic:

    # === 原有控制逻辑保留 ===
    generator_parallel_operation:
      # ... 原有内容 ...
  
    ups_operation_mode:
      # ... 原有内容 ...
  
    # === E2修复：电池分级管理 ===
    battery_soc_management:
      name: UPS电池分级管理
      description: 根据电池剩余电量采取分级措施
    
      soc_levels:
        level_normal:
          range: "80-100%"
          status: 正常
          action: 无特殊动作
          display: 绿色
        
        level_warning:
          range: "50-80%"
          status: 预警
          action:
            - 提醒值班人员关注
            - 检查发电机是否启动
            - 准备非关键负荷切除
          display: 黄色
        
        level_alert:
          range: "20-50%"
          status: 告急
          action:
            - 报警通知相关人员
            - 切除非生命支持负荷
            - 优先保证ICU/手术室
            - 检查发电机启动状态
          display: 橙色
          shed_loads:
            - 非关键工作站
            - 普通照明（保留应急照明）
            - 非关键医疗设备
        
        level_critical:
          range: "10-20%"
          status: 危急
          action:
            - CRITICAL报警
            - 仅保留生命支持设备
            - 通知手术室准备转移患者
            - 通知ICU手动接管呼吸机
          display: 红色
          remaining_loads:
            - 生命支持设备（呼吸机等）
            - 手术室核心设备
            - 监护仪
            - 应急照明
        
        level_shutdown:
          range: "<10%"
          status: 即将关机
          action:
            - 有序关闭剩余非生命攸关设备
            - 保护性关机（防止设备损坏）
            - 发出最终警告
          display: 红色闪烁
          note: 剩余约1-2分钟供电时间
        
        level_exhausted:
          range: "<5%"
          status: 电池耗尽
          action:
            - UPS自动关机
            - 保护电池防止过放
          note: 此时生命支持设备应已切换至其他电源或手动模式
    
      generator_coordination:
        description: 发电机与UPS协调
        scenario_1:
          condition: 市电失电，发电机正常启动
          action:
            - 发电机启动后立即给UPS供电
            - UPS转为市电模式（由发电机供电）
            - 开始给电池充电
            - 电池恢复至80%以上后恢复全部负荷
          timeline:
            - "T+0": 市电失电，UPS电池放电
            - "T+15s": 发电机启动，UPS切换至发电机供电
            - "T+15s起": 电池开始充电
            - "约30min后": 电池恢复至80%
          
        scenario_2:
          condition: 市电失电，发电机启动失败
          action:
            - UPS持续电池放电
            - 启动SOC分级管理
            - 等待发电机重试或外部电源
          critical_time: 15-30分钟（视电池容量）
    
      low_temperature_derating:
        description: 低温环境电池容量折减
        derating_table:
          - temp: "25℃"
            capacity: "100%"
          - temp: "20℃"
            capacity: "95%"
          - temp: "10℃"
            capacity: "85%"
          - temp: "0℃"
            capacity: "70%"
          - temp: "-10℃"
            capacity: "55%"
        monitoring:
          sensor: UPS1_BATTERY_TEMP
          alarm_low: 10℃
          alarm_high: 40℃
        mitigation:
          - UPS机房保持空调运行
          - 电池室温度监控
          - 冬季加强保温
    
      battery_health_monitoring:
        description: 电池健康监测
        parameters:
          - name: 内阻
            normal: "<2mΩ/cell"
            warning: ">3mΩ/cell"
            action: 准备更换
          - name: 容量
            normal: ">80%标称"
            warning: "<80%标称"
            action: 更换电池
          - name: 浮充电压
            normal: "2.25-2.30V/cell"
            abnormal: 偏离>0.1V
            action: 检查充电器
        test_schedule:
          monthly: 放电测试（30%DOD）
          quarterly: 容量测试
          annually: 内阻测试
        
      charging_management:
        description: 充电管理
        float_charge:
          voltage: "2.27V/cell"
          purpose: 长期浮充保持满电
        equalize_charge:
          voltage: "2.35V/cell"
          duration: 8-12小时
          frequency: 每3个月或深放电后
          purpose: 均衡各单体电压
        fast_charge:
          trigger: 电池放电后
          current_limit: "0.1C"
          end_condition: 电压达到2.35V/cell
        temperature_compensation:
          coefficient: "-3mV/℃/cell"
          reference: 25℃
```

---

# 医疗气体系统（修订版）

## 系统 2.4: MGAS-O2 医用氧气系统（完整修订版）

```yaml
System_Topology:

  identity:
    system_id: MGAS-O2
    system_name: 医用氧气系统
    system_name_en: Medical Oxygen System
    # ... 原有identity内容保留 ...
  
    version: 2.0
    revision_notes: |
      v2.0: 补充备用源耗尽保护、纯度监测、终端反污染防护、手术室协调
      v1.0: 初始版本

  # ... 原有boundary内容保留 ...

  nodes:

    # ... 原有source_nodes内容保留 ...
  
    distribution_nodes:
  
      # ... 原有汽化器、一级减压等节点保留 ...
    
      # === G3修复：新增氧气纯度监测节点 ===
      - node_id: MGAS-O2_DST_PURITY_MONITOR
        node_name: 氧气纯度监测装置
        node_name_en: Oxygen Purity Monitor
        node_type: Distribution_Node
        node_subtype: MON
        node_category: DST
      
        function: 监测供气氧气纯度，确保符合药典标准
        medium_in: O2-GAS
        medium_out: SIGNAL
      
        equipment_parameters:
          type: 顺磁式氧分析仪
          measurement_range: {value: "0-100", unit: "%O2"}
          accuracy: ±0.5%
          response_time: {value: "<5", unit: s}
          sampling_point: 一级减压后主管
          display: 数字显示+远传
          calibration: 每季度校准
      
        control_points:
          sensors:
            - point_id: O2_PURITY
              point_name: 氧气纯度
              point_type: AI
              unit: "%"
              range: [0, 100]
              normal_range: [99.5, 100]
            - point_id: O2_PURITY_TREND
              point_name: 纯度趋势
              point_type: AI
              unit: "%/h"
              note: 检测纯度下降速率
          status:
            - point_id: O2_PURITY_LOW_WARN
              point_name: 纯度低预警
              point_type: DI
              threshold: "<99.0%持续5分钟"
            - point_id: O2_PURITY_LOW_ALARM
              point_name: 纯度低报警
              point_type: DI
              threshold: "<98.0%持续1分钟"
            - point_id: O2_PURITY_CRITICAL
              point_name: 纯度危急
              point_type: DI
              threshold: "<95.0%"
      
        alarm_settings:
          warning:
            threshold: {value: 99.0, unit: "%"}
            duration: 5分钟
            action: 报警提示，准备切换气源
          alarm:
            threshold: {value: 98.0, unit: "%"}
            duration: 1分钟
            action: 报警，自动切换至汇流排
          critical:
            threshold: {value: 95.0, unit: "%"}
            duration: 立即
            action: 紧急报警，停止液氧供气，切换备用
      
        action_on_low_purity:
          sequence:
            - step: 1
              action: 触发纯度低报警
              notification: 气体站值班室、护士站
            - step: 2
              action: 自动切换至汇流排供气
              condition: 汇流排压力正常
            - step: 3
              action: 隔离故障液氧系统
              method: 关闭液氧至主管阀门
            - step: 4
              action: 通知检修排查原因
              possible_causes:
                - 液氧储罐进水/污染
                - 汽化器故障
                - 管道泄漏混入空气
                - 减压阀故障
            - step: 5
              action: 确认纯度恢复后方可切回液氧
              requirement: 纯度≥99.5%持续10分钟
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 氧气站房/气体机房
          position: 一级减压后主管旁
          note: 需便于日常检查和校准

      # === 原有报警装置节点保留，增强报警逻辑 ===
      - node_id: MGAS-O2_DST_ALARM_PANEL
        # ... 原有内容保留，补充以下 ...
      
        enhanced_features:
          purity_integration:
            description: 集成纯度报警
            display: 显示当前氧气纯度
            alarm: 与纯度监测联动
        
          predictive_warning:
            description: 预测性预警
            logic: |
              1. 监测液氧消耗速率
              2. 预测剩余可用时间
              3. 提前发出补充提醒
            warning_threshold: 预计剩余<24小时

    sink_nodes:
  
      # === G2修复：终端防污染设计 ===
      - node_id: MGAS-O2_SNK_TERMINAL
        node_name: 氧气终端
        node_name_en: Oxygen Outlet Terminal
        node_type: Sink_Node
        node_category: SNK
      
        function: 床旁/手术室氧气使用点
        medium_in: O2-GAS
        medium_out: O2-GAS (to patient)
      
        is_boundary_output: true
      
        multiplicity: multiple
        instance_pattern: MGAS-O2_SNK_TERMINAL_{Floor}_{Room}_{Seq}
        typical_quantity: 大量（按床位数）
      
        equipment_parameters:
          type: 快速插拔式终端
          standard: 德标DIN/国标GB
          gas_specific: 氧气专用（不可互换）
          color_coding: 绿色
          flow_rate: {value: "0-15", unit: "L/min"}
          outlet_pressure: {value: 0.4, unit: MPa, tolerance: ±0.05}
        
          # === G2修复：防污染设计 ===
          anti_contamination_features:
            check_valve:
              type: 内置单向阀
              function: 防止气体回流
              cracking_pressure: {value: 0.01, unit: MPa}
              note: 即使接错也不会反向污染管道
          
            self_sealing:
              type: 自封闭机构
              function: 拔出时自动关闭，防止外界污染进入
            
            quick_disconnect:
              type: 快速插拔接头
              function: 气体专用接头，不同气体不可互换
              standard: ISO 5359
            
            dust_cap:
              type: 防尘盖
              function: 不使用时保护终端
              material: 抗菌塑料
        
          contamination_prevention_design:
            standard: ISO 7396-1 Part 2
            features:
              - 终端插座设计防止非医疗器具插入
              - 气体专用颜色和形状编码
              - 使用后自动吹扫功能（可选）
        
          mounting:
            - 设备带
            - 吊塔
            - 墙面
      
        user_guidelines:
          pre_use:
            - 检查终端外观清洁
            - 移除防尘盖
            - 短暂开启吹扫（1-2秒）
          during_use:
            - 定期检查连接牢固
            - 观察流量计显示
          post_use:
            - 拔出连接器
            - 盖好防尘盖
            - 终端表面消毒
          prohibited:
            - 禁止使用损坏的终端
            - 禁止自行改装接头
            - 禁止将终端用于非医疗用途
      
        maintenance:
          daily: 外观检查，清洁消毒
          weekly: 功能测试（压力、流量）
          monthly: 单向阀功能检查
          yearly: 更换密封件
      
        location_hint:
          space_type: 病房/手术室/ICU
          position: 床头设备带/吊塔
          height: 距地1.4m（设备带）

  # ========================================
  # CONTROL LOGIC SECTION - 控制逻辑（G1/G4修复）
  # ========================================
  control_logic:

    # === 原有控制逻辑保留 ===
    source_auto_switching:
      # ... 原有内容保留 ...
  
    manifold_switching:
      # ... 原有内容保留 ...
  
    three_level_alarm:
      # ... 原有内容保留 ...
  
    # === G1修复：备用源耗尽保护 ===
    backup_source_depletion_protection:
      name: 备用气源耗尽应急保护
      description: 液氧和汇流排均即将耗尽时的应急措施
    
      monitoring:
        lox_level:
          warning: 20%
          alarm: 15%
          critical: 10%
        manifold_pressure:
          warning: 2MPa（单侧）
          alarm: 1MPa（单侧）
          critical: 0.5MPa（双侧均低）
    
      stage_1_early_warning:
        trigger: 液氧液位<20% 或 汇流排单侧<2MPa
        actions:
          - action: 发出预警
            target: 气体站值班室
          - action: 联系液氧供应商确认配送时间
          - action: 清点备用气瓶数量
          - action: 准备应急氧气瓶
    
      stage_2_alert:
        trigger: 液氧液位<15% 或 切换至汇流排供气
        actions:
          - action: 发出警报
            target: 气体站、护士站、设备科
          - action: 确认液氧配送车辆出发
          - action: 核实各科室氧气使用情况
          - action: 非急需患者减少用氧
          - action: 床旁应急氧气瓶检查就绪
    
      stage_3_critical:
        trigger: |
          液氧耗尽 且 汇流排双侧均<1MPa
          或 系统压力跌至<0.3MPa
        actions:
          - step: 1
            action: 触发CRITICAL报警
            target: 医院总指挥中心、院办、医务科
          - step: 2
            action: 启动《氧气供应中断应急预案》
          - step: 3
            action: 通知各科室启用床旁应急氧气瓶
          - step: 4
            action: 优先保障ICU、手术室、急诊
          - step: 5
            action: 暂停非急需患者用氧
          - step: 6
            action: 联系周边医院借调氧气
          - step: 7
            action: 液氧公司紧急配送（1小时内）
      
        triage_priority:
          priority_1_life_critical:
            areas: ICU、手术室、急诊抢救室
            action: 床旁氧气瓶全力保障
          priority_2_critical:
            areas: 新生儿科、产房、CCU
            action: 床旁氧气瓶
          priority_3_important:
            areas: 普通病房（呼吸科等）
            action: 按需使用，降低流量
          priority_4_general:
            areas: 门诊、康复科
            action: 暂停供氧
    
      stage_4_recovery:
        trigger: 新液氧/气瓶补充到位
        actions:
          - step: 1
            action: 确认新气源正常
          - step: 2
            action: 切换至新气源
          - step: 3
            action: 系统压力恢复正常
          - step: 4
            action: 逐步恢复各科室供氧
          - step: 5
            action: 解除应急状态
          - step: 6
            action: 填写应急事件报告
    
      time_budget:
        description: 时间预算
        calculation: |
          汇流排10瓶×40L×15MPa = 6000L液态 = 约6000Nm³气态
          峰值消耗2000L/min = 120Nm³/h
          理论可用时间 = 6000/120 = 50小时（满配）
          实际预留安全余量 = 10小时（仅1侧）
        requirement: 
          - 液氧补充必须在汇流排耗尽前到达
          - 预留至少4小时应急时间
    
      pressure_continuity:
        description: 切换过程压力连续性
        problem: 切换时主管压力可能波动
        solution:
          - 设置蓄压罐（缓冲罐）
          - 切换阀门平稳过渡
          - 一级减压阀组一用一备
        requirement: 切换过程中主管压力≥0.35MPa
        verification: 定期切换演练测试

    # === G4修复：手术室医用气体协调 ===
    operating_room_gas_coordination:
      name: 手术室医用气体协调控制
      description: 氧气与负压吸引的协调监控
    
      pre_procedure_check:
        description: 术前检查清单
        checklist:
          - item: 氧气压力
            requirement: "≥0.4MPa"
            source: O2_ZONE_PRESSURE
          - item: 负压真空度
            requirement: "≤-0.03MPa"
            source: VAC_ZONE_PRESSURE
          - item: 压缩空气压力
            requirement: "≥0.4MPa"
            source: AIR_ZONE_P
          - item: 笑气压力（如使用）
            requirement: "≥0.4MPa"
            source: N2O_ZONE_P
        verification:
          method: 手术室控制面板一键检测
          display: 绿灯=正常，红灯=异常
          record: 自动记录检测结果
        blocking_condition:
          description: 阻止手术开始条件
          condition: 任一气体不合格
          action: 
            - 禁止开始新手术
            - 报警通知维护人员
            - 正在进行手术继续，做好应急准备
    
      during_procedure_monitoring:
        description: 术中持续监测
        monitoring:
          O2_pressure:
            normal: ">0.35MPa"
            warning: "0.30-0.35MPa"
            alarm: "<0.30MPa"
          VAC_vacuum:
            normal: "<-0.03MPa"
            warning: "-0.02~-0.03MPa"
            alarm: ">-0.02MPa"
        display: 手术室内压力显示屏
        refresh_rate: 实时更新
      
      failure_scenarios:
        O2_failure:
          trigger: 手术室氧气压力<0.25MPa
          immediate_actions:
            - step: 1
              action: 声光报警（手术室内）
            - step: 2
              action: 通知麻醉医生
            - step: 3
              action: 启用麻醉机内置氧气备份
              note: 麻醉机通常配备小型氧气瓶
            - step: 4
              action: 准备床旁应急氧气瓶
            - step: 5
              action: 通知气体站排查故障
          surgical_response:
            - 暂停非紧急操作
            - 优先完成关键步骤
            - 必要时提前结束手术
          
        VAC_failure:
          trigger: 手术室负压真空度>-0.02MPa
          immediate_actions:
            - step: 1
              action: 声光报警
            - step: 2
              action: 通知手术医生
            - step: 3
              action: 启用手动吸引器
              equipment: 脚踏式吸引器/手动负压球
            - step: 4
              action: 通知气体站排查
          surgical_response:
            - 手动清理术野
            - 如无法控制出血，考虑暂停
          
        both_failure:
          trigger: 氧气和负压同时故障
          severity: CRITICAL
          actions:
            - step: 1
              action: 最高级别报警
            - step: 2
              action: 启动所有应急设备
            - step: 3
              action: 评估是否继续手术
            - step: 4
              action: 院领导决策
          decision_factors:
            - 手术进行阶段
            - 患者状态
            - 应急设备可用性
            - 故障恢复预期时间
    
      cross_system_coordination:
        description: 跨系统协调信号
        signals:
          MGAS_O2_to_MGAS_VAC:
            - O2供应正常状态
            - O2故障报警
          MGAS_VAC_to_MGAS_O2:
            - VAC供应正常状态
            - VAC故障报警
          integration_point: 楼宇自控系统（INT-BA）
          display: 手术室护士站总览屏

    # === 纯度监测联动控制 ===
    purity_monitoring_control:
      name: 氧气纯度监测联动
      description: 纯度异常时的自动响应
    
      monitoring:
        sensor: MGAS-O2_DST_PURITY_MONITOR
        normal_range: "99.5%-100%"
        sampling_interval: 连续监测
      
      control_logic:
        warning_level:
          condition: 纯度<99.0%持续5分钟
          action:
            - 发出预警
            - 记录事件
            - 准备切换
        alarm_level:
          condition: 纯度<98.0%持续1分钟
          action:
            - 发出报警
            - 自动切换至汇流排
            - 关闭液氧系统阀门
            - 通知维护人员
        critical_level:
          condition: 纯度<95.0%
          action:
            - 立即切换气源
            - CRITICAL报警
            - 停止液氧系统
            - 调查原因
    
      recovery:
        condition: 故障排除，纯度恢复
        procedure:
          - step: 1
            action: 确认纯度≥99.5%稳定10分钟
          - step: 2
            action: 手动确认可切回液氧
          - step: 3
            action: 逐步切换回液氧系统
          - step: 4
            action: 监测24小时确认稳定

  # ========================================
  # ALARM & PROTECTION - 报警与保护（增强）
  # ========================================
  alarm_protection:
  
    critical_alarms:
      # ... 原有报警保留 ...
    
      # === 新增纯度报警 ===
      - alarm_id: ALM_O2_PURITY_LOW
        alarm_name: 氧气纯度低报警
        severity: HIGH
        trigger: O2_PURITY < 98%
        action: 自动切换汇流排，通知维护
      
      - alarm_id: ALM_O2_PURITY_CRITICAL
        alarm_name: 氧气纯度危急
        severity: CRITICAL
        trigger: O2_PURITY < 95%
        action: 立即停止液氧供气，紧急报警
      
      # === 新增气源耗尽报警 ===
      - alarm_id: ALM_O2_SOURCE_DEPLETING
        alarm_name: 气源即将耗尽
        severity: CRITICAL
        trigger: 液氧<10% 且 汇流排双侧<1MPa
        action: 启动应急预案，全院通知
```

---

## 系统 2.5: MGAS-VAC 医用负压吸引系统（修订版 - 关键补充）

```yaml
  # ========================================
  # CONTROL LOGIC - 控制逻辑（修订补充）
  # ========================================
  control_logic:

    # === 原有pump_control保留 ===
    pump_control:
      # ... 原有内容 ...
  
    # === G4修复：与氧气系统协调 ===
    oxygen_system_coordination:
      name: 与氧气系统协调
      description: 负压系统状态同步至氧气系统监控
    
      status_sharing:
        signals_to_o2_system:
          - VAC_SYSTEM_OK: 负压系统正常
          - VAC_LOW_VACUUM: 真空度不足
          - VAC_PUMP_FAULT: 泵组故障
        integration: 通过INT-BA系统集成
      
      joint_monitoring:
        location: 手术室护士站
        display: 统一显示O2/VAC/AIR状态
        alarm: 任一系统故障时联合报警
  
    # === 备用策略增强 ===
    backup_strategy:
      name: 负压系统备用策略
    
      pump_redundancy:
        configuration: "2+1（两用一备）"
        auto_failover:
          trigger: 运行泵故障
          action: 自动启动备用泵
          time: "<5秒"
        
      manual_backup:
        equipment: 脚踏式吸引器
        location: 每间手术室
        purpose: 真空泵全部故障时手动吸引
        maintenance: 每月检查功能完好
      
      mobile_vacuum:
        equipment: 移动式电动吸引器
        quantity: 4台
        location: 设备科库房
        purpose: 应急调配
      
      cross_connection:
        description: 与其他真空系统的应急连接
        note: |
          大型医院可能有多个真空泵站
          紧急时可通过阀门切换连通
```

---

## 系统间协调逻辑（新增章节）

```yaml
# ========================================
# 跨系统协调逻辑
# ========================================
Cross_System_Coordination:

  identity:
    name: 医院关键系统协调逻辑
    description: 定义电气与医疗气体系统间的关键交互
    version: 1.0

  # === 电力系统与医疗气体系统协调 ===
  power_gas_coordination:
  
    normal_operation:
      description: 正常运行时的监控
      monitoring:
        - 电力系统状态 → 医用气体控制室
        - 医用气体压力 → 楼宇自控中心
      display: 统一能源管理平台
    
    power_failure_impact:
      description: 电力故障对医疗气体的影响
    
      affected_equipment:
        MGAS_O2:
          affected: 
            - 液氧汽化器电伴热（冬季）
            - 报警系统
            - 监控设备
          not_affected:
            - 液氧储罐（被动）
            - 汇流排（被动）
            - 管道供气（靠压力）
          action: 确保报警系统有UPS后备
        
        MGAS_VAC:
          affected:
            - 真空泵（核心设备）
            - 报警系统
          impact: 真空泵停止，真空度逐渐下降
          buffer_time: 约5-10分钟（取决于储气罐容积和使用量）
          action: 
            - 真空泵接应急电源
            - 准备手动吸引器
          
        MGAS_AIR:
          affected:
            - 空气压缩机（核心设备）
            - 干燥机
            - 过滤器
          impact: 压缩空气逐渐下降
          buffer_time: 约10-15分钟（取决于储气罐容积）
          action:
            - 压缩机接应急电源
            - 非关键压缩空气可暂停
          
    generator_startup_sequence:
      description: 发电机启动后医疗气体设备恢复顺序
      sequence:
        - priority: 1
          equipment: UPS（含医疗设备）
          time: 立即
        - priority: 2
          equipment: 真空泵
          time: T+15s
          reason: 手术室吸引关键
        - priority: 3
          equipment: 空气压缩机
          time: T+20s
        - priority: 4
          equipment: 氧气监控报警
          time: T+25s
          note: 氧气供应本身不受影响
        
    mutual_monitoring:
      description: 互相监控信号
      signals:
        ELEC_to_MGAS:
          - POWER_NORMAL: 市电正常
          - POWER_FAIL: 市电失电
          - GEN_RUNNING: 发电机运行
          - GEN_FAIL: 发电机故障
        MGAS_to_ELEC:
          - O2_CRITICAL: 氧气系统危急
          - VAC_CRITICAL: 负压系统危急
          - AIR_CRITICAL: 压缩空气危急
      action_on_signal:
        POWER_FAIL_received:
          - 医用气体系统记录事件
          - 准备应急响应
          - 延长报警静音防止误报
        O2_CRITICAL_sent:
          - 优先保障医用气体设备供电
          - 必要时切除非关键负荷

  # === 手术室综合协调 ===
  operating_room_coordination:
  
    pre_surgery_checklist:
      description: 手术前综合检查
      items:
        electricity:
          - 市电正常 / 发电机就绪
          - UPS电池充足（>80%）
          - 手术室配电正常
        medical_gas:
          - 氧气压力≥0.4MPa
          - 氧气纯度≥99.5%
          - 负压真空度≤-0.03MPa
          - 压缩空气≥0.4MPa
          - 笑气（如需要）≥0.4MPa
        backup:
          - 床旁氧气瓶就位
          - 手动吸引器就位
          - 应急照明正常
      result:
        all_pass: 允许手术
        any_fail: 禁止开始新手术
      
    during_surgery_monitoring:
      description: 术中持续监控
      display: 手术室控制面板
      parameters:
        - 电力状态（市电/发电机/UPS）
        - 氧气压力和纯度
        - 负压真空度
        - 压缩空气压力
      alarm: 声光报警（可静音但不可关闭）
    
    emergency_response:
      description: 紧急情况响应矩阵
      scenarios:
        power_fail_gen_ok:
          impact: 短暂中断（<15秒）
          action: 继续手术
        power_fail_gen_fail:
          impact: 依赖UPS（15-30分钟）
          action: 
            - 评估手术阶段
            - 尽快完成关键步骤
            - 必要时提前结束
        o2_fail:
          impact: 患者供氧中断风险
          action:
            - 床旁氧气瓶接手
            - 麻醉师接管呼吸
            - 评估继续/终止
        vac_fail:
          impact: 术野积血无法清理
          action:
            - 手动吸引器
            - 加快止血
            - 必要时暂停
        multiple_fail:
          impact: 极端情况
          action:
            - 院领导决策
            - 优先保护患者生命
            - 启动最高级应急预案

  # === 报警整合 ===
  alarm_integration:
  
    unified_alarm_center:
      location: 医院总控室/安防中心
      systems_integrated:
        - ELEC-HV
        - ELEC-LV-MAIN
        - ELEC-EPS
        - MGAS-O2
        - MGAS-VAC
        - MGAS-AIR
        - MGAS-N2O
        - HVAC-CHP
        - INT-BA
      display: 统一监控大屏
    
    alarm_priority:
      level_1_emergency:
        examples:
          - 双路市电全失且发电机故障
          - 氧气系统完全中断
          - 多系统同时故障
        response: 
          - 自动通知院领导
          - 启动医院应急预案
          - 全院广播
        
      level_2_critical:
        examples:
          - 单路市电故障
          - 氧气纯度低
          - 发电机单机故障
        response:
          - 通知设备科/值班人员
          - 准备应急措施
        
      level_3_high:
        examples:
          - 液氧低液位
          - 变压器超温
          - 过滤器堵塞
        response:
          - 通知维护人员
          - 安排检修
        
      level_4_warning:
        examples:
          - 设备运行时间超标
          - 电池需要测试
          - 定期维护提醒
        response:
          - 记录事件
          - 安排维护计划
```

---

