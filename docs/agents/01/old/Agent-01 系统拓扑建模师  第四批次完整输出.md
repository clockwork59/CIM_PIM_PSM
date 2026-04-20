# 第四部分：Batch 4 完整输出 - 新增系统

## Batch 4 系统清单

```yaml
Batch_4_Systems:

  - HVAC-HWP: 热源系统
  - HVAC-SMOKE: 防排烟系统
  - PLUMB-HWS: 生活热水系统
  - ELEC-UPS: 不间断电源系统
  - MGAS-AGSS: 麻醉废气排放系统
  - PLUMB-MED-WASTE: 医疗废水系统
  - FIRE-GAS: 气体灭火系统
```

---

## 4.1 HVAC-HWP 热源系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: HVAC-HWP
    system_name: 热源系统
    system_name_en: Hot Water Plant System
    category: HVAC
    version: 1.0
  
    description: |
      医院空调供暖热源系统，采用燃气锅炉或空气源热泵作为热源，
      通过热水管网为空调末端、生活热水系统提供热量。
    
    design_basis:
      heat_source: 燃气热水锅炉 / 空气源热泵
      supply_temperature: {value: 50-60, unit: ℃}
      return_temperature: {value: 40-50, unit: ℃}
      capacity: 根据热负荷计算
    
    serving_scope:
      - HVAC-AHU (再热盘管)
      - HVAC-FCU (供暖)
      - HVAC-CLEAN (加热盘管)
      - PLUMB-HWS (生活热水换热)

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: HVAC-HWP_BND_IN_GAS
        boundary_name: 天然气供应
        medium: GAS-NG
        is_external: true
        source: 市政燃气管网
        note: 燃气锅炉方案
      
      - boundary_id: HVAC-HWP_BND_IN_ELEC
        boundary_name: 电源
        medium: ELEC-LV
        source_system: ELEC-LV-MAIN
        note: 热泵方案
      
      - boundary_id: HVAC-HWP_BND_IN_WATER
        boundary_name: 补水
        medium: WATER-DW
        source_system: PLUMB-DWS
      
    outputs:
      - boundary_id: HVAC-HWP_BND_OUT_HW
        boundary_name: 热水供水
        medium: WATER-HW
        target_systems: [HVAC-CHP, HVAC-AHU, HVAC-FCU, HVAC-CLEAN]
      
      - boundary_id: HVAC-HWP_BND_OUT_HWS
        boundary_name: 生活热水换热
        medium: WATER-HW
        target_system: PLUMB-HWS

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:

    source_nodes:
  
      - node_id: HVAC-HWP_SRC_BOILER
        node_name: 燃气热水锅炉
        node_name_en: Gas-fired Hot Water Boiler
        node_type: Source_Node
        node_category: SRC
      
        function: 燃气燃烧产生热水
        medium_in: [GAS-NG, WATER-HW-RET]
        medium_out: WATER-HW
      
        multiplicity: multiple
        instance_pattern: HVAC-HWP_SRC_BOILER_{NN}
      
        typical_configuration:
          quantity: 2-3
          redundancy: "N+1"
        
        equipment_parameters:
          type: 真空热水锅炉/常压热水锅炉/承压热水锅炉
          capacity_each: {value: 2-4, unit: MW}
          efficiency: {value: "≥95", unit: "%"}
          supply_temp: {value: 60, unit: ℃}
          return_temp: {value: 50, unit: ℃}
          gas_consumption: 根据容量计算
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 锅炉房
          floor: 地下室或独立建筑
        
        installation_requirements:
          - 防火分隔
          - 燃气泄漏检测
          - 通风换气
          - 烟囱排放
          - 防爆电气
          - 检修通道
        
        control_points:
          sensors:
            - {point_id: BOILER_T_SUP, type: AI, description: 出水温度}
            - {point_id: BOILER_T_RET, type: AI, description: 回水温度}
            - {point_id: BOILER_P, type: AI, description: 压力}
            - {point_id: BOILER_FIRE, type: AI, description: 火焰信号}
            - {point_id: BOILER_GAS_P, type: AI, description: 燃气压力}
            - {point_id: BOILER_FLUE_T, type: AI, description: 烟气温度}
          status:
            - {point_id: BOILER_RUN, type: DI, description: 运行状态}
            - {point_id: BOILER_FAULT, type: DI, description: 故障报警}
            - {point_id: BOILER_FLAME, type: DI, description: 点火失败}
            - {point_id: GAS_LEAK, type: DI, description: 燃气泄漏}
          commands:
            - {point_id: BOILER_START, type: DO, description: 启停控制}
            - {point_id: BOILER_LOAD, type: AO, description: 负荷调节}

      - node_id: HVAC-HWP_SRC_ASHP
        node_name: 空气源热泵
        node_name_en: Air Source Heat Pump
        node_type: Source_Node
        node_category: SRC
      
        function: 从空气中提取热量
        medium_in: [AIR-OA, WATER-HW-RET, ELEC-LV]
        medium_out: WATER-HW
      
        multiplicity: multiple
        instance_pattern: HVAC-HWP_SRC_ASHP_{NN}
      
        typical_configuration:
          quantity: 3-6
          redundancy: "N+1"
          note: 可作为锅炉的替代或补充方案
        
        equipment_parameters:
          type: 空气源热泵机组
          capacity_each: {value: 200-500, unit: kW}
          cop: {value: "≥3.5", unit: null, condition: 工况7℃}
          supply_temp: {value: 50-55, unit: ℃}
          power: {value: 80-150, unit: kW}
        
        location_hint:
          space_type: OUTDOOR
          position: 屋顶或室外地面
        
        installation_requirements:
          - 通风良好
          - 减振基础
          - 冬季化霜排水
          - 噪声控制
        
        control_points:
          sensors:
            - {point_id: ASHP_T_SUP, type: AI, description: 出水温度}
            - {point_id: ASHP_T_RET, type: AI, description: 回水温度}
            - {point_id: ASHP_T_OA, type: AI, description: 室外温度}
            - {point_id: ASHP_I, type: AI, description: 运行电流}
          status:
            - {point_id: ASHP_RUN, type: DI, description: 运行状态}
            - {point_id: ASHP_FAULT, type: DI, description: 故障报警}
            - {point_id: ASHP_DEFROST, type: DI, description: 化霜状态}
          commands:
            - {point_id: ASHP_START, type: DO, description: 启停控制}

    distribution_nodes:
  
      - node_id: HVAC-HWP_DST_HWP
        node_name: 热水循环泵
        node_name_en: Hot Water Circulation Pump
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 热水循环输配
        medium_in: WATER-HW
        medium_out: WATER-HW
      
        multiplicity: multiple
        instance_pattern: HVAC-HWP_DST_HWP_{NN}
      
        typical_configuration:
          quantity: 2-3
          redundancy: 一用一备
        
        equipment_parameters:
          type: 离心泵（变频）
          flow: {value: 100-300, unit: m³/h}
          head: {value: 25-35, unit: m}
          power: {value: 22-55, unit: kW}
          control: 变频调速
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 锅炉房/热泵机房
        
        control_points:
          sensors:
            - {point_id: HWP_FREQ, type: AI, description: 运行频率}
            - {point_id: HWP_I, type: AI, description: 运行电流}
            - {point_id: HWP_DP, type: AI, description: 进出口压差}
          status:
            - {point_id: HWP_RUN, type: DI, description: 运行状态}
            - {point_id: HWP_FAULT, type: DI, description: 故障报警}
          commands:
            - {point_id: HWP_START, type: DO, description: 启停控制}
            - {point_id: HWP_FREQ_SP, type: AO, description: 频率设定}

      - node_id: HVAC-HWP_DST_HEADER_SUP
        node_name: 热水供水分水器
        node_name_en: Hot Water Supply Header
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 热水供水分配
        medium_in: WATER-HW
        medium_out: WATER-HW
      
        equipment_parameters:
          material: 无缝钢管
          diameter: {value: DN200-DN300, unit: mm}
          branches:
            - 空调热水供水
            - 生活热水换热
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 锅炉房
        
        control_points:
          sensors:
            - {point_id: HW_SUP_T, type: AI, description: 供水温度}
            - {point_id: HW_SUP_P, type: AI, description: 供水压力}

      - node_id: HVAC-HWP_DST_HEADER_RET
        node_name: 热水回水集水器
        node_name_en: Hot Water Return Header
        node_type: Distribution_Node
        node_category: DST
        node_subtype: JUN
      
        function: 热水回水汇集
        medium_in: WATER-HW
        medium_out: WATER-HW
      
        equipment_parameters:
          material: 无缝钢管
          diameter: {value: DN200-DN300, unit: mm}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 锅炉房
        
        control_points:
          sensors:
            - {point_id: HW_RET_T, type: AI, description: 回水温度}
            - {point_id: HW_RET_P, type: AI, description: 回水压力}

      - node_id: HVAC-HWP_DST_MAKEUP
        node_name: 补水定压装置
        node_name_en: Makeup Water & Pressurization Unit
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 系统补水、定压
        medium_in: WATER-DW
        medium_out: WATER-HW
      
        equipment_parameters:
          type: 定压补水装置
          components:
            - 补水泵
            - 定压罐/膨胀罐
            - 软化水装置
            - 控制器
          pressure_setpoint: 系统静压+5-10m
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 锅炉房
        
        control_points:
          sensors:
            - {point_id: MAKEUP_P, type: AI, description: 系统压力}
            - {point_id: MAKEUP_LEVEL, type: AI, description: 补水箱液位}
          status:
            - {point_id: MAKEUP_PUMP_RUN, type: DI, description: 补水泵运行}
            - {point_id: MAKEUP_LOW_P, type: DI, description: 低压报警}

      - node_id: HVAC-HWP_DST_AHU_BRANCH
        node_name: AHU热水分支
        node_name_en: AHU Hot Water Branch
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BRH
      
        function: 向空调机组供热水
        medium_in: WATER-HW
        medium_out: WATER-HW
      
        equipment_parameters:
          valve: 电动调节阀/平衡阀
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 锅炉房
        
        interface_systems: [HVAC-AHU, HVAC-CLEAN]

      - node_id: HVAC-HWP_DST_FCU_BRANCH
        node_name: FCU热水分支
        node_name_en: FCU Hot Water Branch
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BRH
      
        function: 向风机盘管供热水
        medium_in: WATER-HW
        medium_out: WATER-HW
      
        equipment_parameters:
          valve: 平衡阀
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 锅炉房
        
        interface_system: HVAC-FCU

      - node_id: HVAC-HWP_DST_HWS_HEX
        node_name: 生活热水换热器
        node_name_en: DHW Heat Exchanger
        node_type: Distribution_Node
        node_category: DST
        node_subtype: HEX
      
        function: 热水系统与生活热水换热
        medium_in: [WATER-HW, WATER-DW]
        medium_out: [WATER-HW, WATER-HW-DOM]
      
        equipment_parameters:
          type: 板式换热器/容积式换热器
          capacity: 根据生活热水负荷
          primary_temp: {value: "60/50", unit: ℃}
          secondary_temp: {value: "55/10", unit: ℃}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 热水机房
        
        interface_system: PLUMB-HWS
      
        control_points:
          sensors:
            - {point_id: HEX_T_HW_IN, type: AI, description: 一次侧进水温度}
            - {point_id: HEX_T_HW_OUT, type: AI, description: 一次侧出水温度}
            - {point_id: HEX_T_DHW_OUT, type: AI, description: 二次侧出水温度}
          commands:
            - {point_id: HEX_VALVE, type: AO, description: 一次侧阀开度}

    sink_nodes:
  
      - node_id: HVAC-HWP_SNK_AHU
        node_name: AHU热水用户
        node_name_en: AHU Hot Water User
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 空调加热
        medium_in: WATER-HW
      
        interface_system: HVAC-AHU
      
      - node_id: HVAC-HWP_SNK_FCU
        node_name: FCU热水用户
        node_name_en: FCU Hot Water User
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 末端供暖
        medium_in: WATER-HW
      
        interface_system: HVAC-FCU
      
      - node_id: HVAC-HWP_SNK_DHW
        node_name: 生活热水
        node_name_en: DHW User
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 生活热水加热
        medium_in: WATER-HW
      
        interface_system: PLUMB-HWS

  # ============================================================
  # 边定义
  # ============================================================
  edges:

    supply_edges:
  
      - edge_id: HVAC-HWP_EDGE_001
        edge_name: 锅炉至循环泵
        edge_type: TRK
        from_node: HVAC-HWP_SRC_BOILER
        to_node: HVAC-HWP_DST_HWP
        direction: unidirectional
        medium: WATER-HW
        medium_properties:
          temperature: {value: 60, unit: ℃}
        
      - edge_id: HVAC-HWP_EDGE_002
        edge_name: 循环泵至分水器
        edge_type: TRK
        from_node: HVAC-HWP_DST_HWP
        to_node: HVAC-HWP_DST_HEADER_SUP
        direction: unidirectional
        medium: WATER-HW
      
      - edge_id: HVAC-HWP_EDGE_003
        edge_name: 分水器至AHU分支
        edge_type: BRH
        from_node: HVAC-HWP_DST_HEADER_SUP
        to_node: HVAC-HWP_DST_AHU_BRANCH
        direction: unidirectional
        medium: WATER-HW
      
      - edge_id: HVAC-HWP_EDGE_004
        edge_name: 分水器至FCU分支
        edge_type: BRH
        from_node: HVAC-HWP_DST_HEADER_SUP
        to_node: HVAC-HWP_DST_FCU_BRANCH
        direction: unidirectional
        medium: WATER-HW
      
      - edge_id: HVAC-HWP_EDGE_005
        edge_name: 分水器至生活热水换热器
        edge_type: BRH
        from_node: HVAC-HWP_DST_HEADER_SUP
        to_node: HVAC-HWP_DST_HWS_HEX
        direction: unidirectional
        medium: WATER-HW
      
      - edge_id: HVAC-HWP_EDGE_006
        edge_name: AHU分支至AHU用户
        edge_type: TRM
        from_node: HVAC-HWP_DST_AHU_BRANCH
        to_node: HVAC-HWP_SNK_AHU
        direction: unidirectional
        medium: WATER-HW
        cross_system: true
        target_system: HVAC-AHU
      
      - edge_id: HVAC-HWP_EDGE_007
        edge_name: FCU分支至FCU用户
        edge_type: TRM
        from_node: HVAC-HWP_DST_FCU_BRANCH
        to_node: HVAC-HWP_SNK_FCU
        direction: unidirectional
        medium: WATER-HW
        cross_system: true
        target_system: HVAC-FCU
      
      - edge_id: HVAC-HWP_EDGE_008
        edge_name: 换热器至生活热水
        edge_type: TRM
        from_node: HVAC-HWP_DST_HWS_HEX
        to_node: HVAC-HWP_SNK_DHW
        direction: unidirectional
        medium: WATER-HW-DOM
        cross_system: true
        target_system: PLUMB-HWS

    return_edges:
  
      - edge_id: HVAC-HWP_EDGE_RET_001
        edge_name: AHU用户回水
        edge_type: TRM
        from_node: HVAC-HWP_SNK_AHU
        to_node: HVAC-HWP_DST_AHU_BRANCH
        direction: unidirectional
        medium: WATER-HW
      
      - edge_id: HVAC-HWP_EDGE_RET_002
        edge_name: FCU用户回水
        edge_type: TRM
        from_node: HVAC-HWP_SNK_FCU
        to_node: HVAC-HWP_DST_FCU_BRANCH
        direction: unidirectional
        medium: WATER-HW
      
      - edge_id: HVAC-HWP_EDGE_RET_003
        edge_name: 各分支至集水器
        edge_type: TRK
        from_node: HVAC-HWP_DST_AHU_BRANCH
        to_node: HVAC-HWP_DST_HEADER_RET
        direction: unidirectional
        medium: WATER-HW
      
      - edge_id: HVAC-HWP_EDGE_RET_004
        edge_name: 集水器至锅炉
        edge_type: TRK
        from_node: HVAC-HWP_DST_HEADER_RET
        to_node: HVAC-HWP_SRC_BOILER
        direction: unidirectional
        medium: WATER-HW
        medium_properties:
          temperature: {value: 50, unit: ℃}

    makeup_edges:
  
      - edge_id: HVAC-HWP_EDGE_MAKEUP
        edge_name: 补水至系统
        edge_type: BRH
        from_node: HVAC-HWP_DST_MAKEUP
        to_node: HVAC-HWP_DST_HEADER_RET
        direction: unidirectional
        medium: WATER-HW

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:

    - path_id: HVAC-HWP_PATH_AHU
      path_name: AHU供热路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: HVAC-HWP_SRC_BOILER}
        - {step: 2, element_type: edge, element_id: HVAC-HWP_EDGE_001}
        - {step: 3, element_type: node, element_id: HVAC-HWP_DST_HWP}
        - {step: 4, element_type: edge, element_id: HVAC-HWP_EDGE_002}
        - {step: 5, element_type: node, element_id: HVAC-HWP_DST_HEADER_SUP}
        - {step: 6, element_type: edge, element_id: HVAC-HWP_EDGE_003}
        - {step: 7, element_type: node, element_id: HVAC-HWP_DST_AHU_BRANCH}
        - {step: 8, element_type: edge, element_id: HVAC-HWP_EDGE_006}
        - {step: 9, element_type: node, element_id: HVAC-HWP_SNK_AHU}

  # ============================================================
  # 回路定义
  # ============================================================
  loops:

    - loop_id: HVAC-HWP_LOOP_MAIN
      loop_name: 热水主循环回路
      loop_name_en: Hot Water Main Loop
      loop_type: closed
    
      description: |
        热源产生热水→循环泵加压→分水器分配→各用户→回水集水器→热源
      
      delta_t: {value: 10, unit: ℃}
      design_flow: 根据负荷计算

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:

    boiler_staging:
      description: 锅炉台数控制
      control_parameter: 回水温度或热负荷
    
      stage_up:
        condition: 供水温度 < 设定值-3℃ 且 运行锅炉满负荷
        action: 启动下一台锅炉
        delay: {value: 5, unit: min}
      
      stage_down:
        condition: 运行锅炉负荷 < 30% 且 持续15分钟
        action: 停止一台锅炉
      
    pump_control:
      mode: 变频恒压差控制
      setpoint: 最不利用户所需压差
      method: PID调节泵频率
    
    temperature_control:
      supply_temp_setpoint:
        mode: 室外温度补偿
        outdoor_high: {value: 10, unit: ℃, supply: 45, unit: ℃}
        outdoor_low: {value: -10, unit: ℃, supply: 60, unit: ℃}
      
    safety_interlock:
      low_water_level:
        action: 锅炉停机
      high_temperature:
        action: 锅炉停机
      gas_leak:
        action: 切断燃气、锅炉停机、报警
      flame_failure:
        action: 锅炉停机、报警
```

---

## 4.2 HVAC-SMOKE 防排烟系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: HVAC-SMOKE
    system_name: 防排烟系统
    system_name_en: Smoke Control System
    category: HVAC
    subcategory: FIRE_PROTECTION
    version: 1.0
  
    description: |
      医院防排烟系统，包括机械排烟系统和机械加压送风系统。
      用于火灾时排除烟气、保护疏散通道。
      与火灾自动报警系统联动。
    
    design_basis:
      smoke_exhaust:
        velocity: {value: "≥15", unit: m/s}
        temp_rating: {value: 280, unit: ℃}
        duration: {value: 2, unit: h}
      pressurization:
        pressure_diff: {value: 25-50, unit: Pa}
        door_air_velocity: {value: "≥0.7", unit: m/s}
    
    serving_scope:
      - 无窗房间/走廊
      - 地下室
      - 防烟楼梯间
      - 前室/合用前室

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: HVAC-SMOKE_BND_IN_ELEC
        boundary_name: 消防电源
        medium: ELEC-LV
        source_system: ELEC-LV-FIRE
        note: 双电源供电
      
      - boundary_id: HVAC-SMOKE_BND_IN_FA
        boundary_name: 火灾报警联动信号
        medium: SIGNAL-FA
        source_system: FIRE-ALARM
      
    outputs:
      - boundary_id: HVAC-SMOKE_BND_OUT_EXHAUST
        boundary_name: 烟气排放
        medium: AIR-SMOKE
        is_external: true
        target: 大气
      
      - boundary_id: HVAC-SMOKE_BND_OUT_SUPPLY
        boundary_name: 加压送风
        medium: AIR-FA
        target: 疏散通道

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:

    source_nodes:
  
      - node_id: HVAC-SMOKE_SRC_OA
        node_name: 加压送风进风口
        node_name_en: Pressurization Air Intake
        node_type: Source_Node
        node_category: SRC
      
        function: 加压送风新风入口
        medium_out: AIR-OA
        is_external: true
      
        equipment_parameters:
          type: 百叶风口
          position: 正压区（远离火源）
        
        location_hint:
          space_type: EXTERIOR
          position: 屋顶或外墙
          height: 距地面≥2m
          requirement: 距排烟口≥6m

      - node_id: HVAC-SMOKE_SRC_PRESS_FAN
        node_name: 正压送风机
        node_name_en: Pressurization Fan
        node_type: Source_Node
        node_category: SRC
      
        function: 向疏散通道加压送风
        medium_in: AIR-OA
        medium_out: AIR-FA
      
        multiplicity: multiple
        instance_pattern: HVAC-SMOKE_SRC_PRESS_FAN_{Zone}
      
        equipment_parameters:
          type: 轴流风机/离心风机
          flow: {value: 10000-30000, unit: m³/h}
          pressure: {value: 500-1000, unit: Pa}
          power: {value: 15-55, unit: kW}
          temperature: 常温
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 加压送风机房
          position: 屋顶或避难层
        
        installation_requirements:
          - 280℃×2h防火阀
          - 双电源供电
          - 消防联动控制
          - 手动控制按钮
        
        control_points:
          sensors:
            - {point_id: PRESS_DP, type: AI, description: 楼梯间压差}
          status:
            - {point_id: PRESS_FAN_RUN, type: DI, description: 运行状态}
            - {point_id: PRESS_FAN_FAULT, type: DI, description: 故障报警}
          commands:
            - {point_id: PRESS_FAN_START, type: DO, description: 启动命令}
            - {point_id: PRESS_FAN_STOP, type: DO, description: 停止命令}

    distribution_nodes:
  
      - node_id: HVAC-SMOKE_DST_PRESS_SHAFT
        node_name: 加压送风竖井
        node_name_en: Pressurization Shaft
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
      
        function: 垂直送风通道
        medium_in: AIR-FA
        medium_out: AIR-FA
      
        multiplicity: multiple
      
        equipment_parameters:
          material: 混凝土/砖
          fire_rating: 耐火极限≥2h
        
        location_hint:
          space_type: SHAFT
          shaft_type: 正压送风井
          position: 紧邻楼梯间

      - node_id: HVAC-SMOKE_DST_PRESS_OUTLET
        node_name: 加压送风口
        node_name_en: Pressurization Air Outlet
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRM
      
        function: 向楼梯间/前室送风
        medium_in: AIR-FA
        medium_out: AIR-FA
      
        multiplicity: multiple
        instance_pattern: HVAC-SMOKE_DST_PRESS_OUTLET_{Floor}
      
        equipment_parameters:
          type: 常闭多叶送风口
          actuator: 电动/电磁
          open_signal: 火灾联动
        
        location_hint:
          space_type: WALL
          position: 楼梯间或前室墙面
          height: {value: 2.0-2.5, unit: m}
        
        control_points:
          status:
            - {point_id: OUTLET_OPEN, type: DI, description: 开启状态}
          commands:
            - {point_id: OUTLET_CMD, type: DO, description: 开启命令}

      - node_id: HVAC-SMOKE_DST_EXHAUST_FAN
        node_name: 排烟风机
        node_name_en: Smoke Exhaust Fan
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 机械排烟
        medium_in: AIR-SMOKE
        medium_out: AIR-SMOKE
      
        multiplicity: multiple
        instance_pattern: HVAC-SMOKE_DST_EXHAUST_FAN_{Zone}
      
        equipment_parameters:
          type: 排烟风机（耐高温）
          flow: {value: 20000-50000, unit: m³/h}
          pressure: {value: 600-1200, unit: Pa}
          power: {value: 30-90, unit: kW}
          temperature_rating: {value: 280, unit: ℃}
          duration: {value: 2, unit: h}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 排烟机房
          position: 屋顶
        
        installation_requirements:
          - 耐高温风机
          - 双电源供电
          - 消防联动控制
          - 手动控制按钮
        
        control_points:
          sensors:
            - {point_id: EXH_TEMP, type: AI, description: 排烟温度}
          status:
            - {point_id: EXH_FAN_RUN, type: DI, description: 运行状态}
            - {point_id: EXH_FAN_FAULT, type: DI, description: 故障报警}
          commands:
            - {point_id: EXH_FAN_START, type: DO, description: 启动命令}

      - node_id: HVAC-SMOKE_DST_EXHAUST_SHAFT
        node_name: 排烟竖井
        node_name_en: Smoke Exhaust Shaft
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
      
        function: 垂直排烟通道
        medium_in: AIR-SMOKE
        medium_out: AIR-SMOKE
      
        multiplicity: multiple
      
        equipment_parameters:
          material: 混凝土/砖
          fire_rating: 耐火极限≥2h
        
        location_hint:
          space_type: SHAFT
          shaft_type: 排烟井

      - node_id: HVAC-SMOKE_DST_EXHAUST_INLET
        node_name: 排烟口
        node_name_en: Smoke Exhaust Inlet
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRM
      
        function: 排烟入口
        medium_in: AIR-SMOKE
        medium_out: AIR-SMOKE
      
        multiplicity: multiple
        instance_pattern: HVAC-SMOKE_DST_EXHAUST_INLET_{Floor}_{Zone}
      
        equipment_parameters:
          type: 常闭排烟口/排烟阀
          actuator: 电动/手动复位
          temperature_fuse: 280℃熔断
        
        location_hint:
          space_type: CEILING
          position: 走廊/房间吊顶
          height: 储烟仓内
          spacing: {value: "≤30", unit: m}
        
        control_points:
          status:
            - {point_id: INLET_OPEN, type: DI, description: 开启状态}
          commands:
            - {point_id: INLET_CMD, type: DO, description: 开启命令}

      - node_id: HVAC-SMOKE_DST_FIRE_DAMPER
        node_name: 防火阀
        node_name_en: Fire Damper
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 火灾时切断风管
        medium_in: AIR
        medium_out: AIR
      
        multiplicity: multiple
      
        equipment_parameters:
          types:
            - {type: 70℃防火阀, application: 空调风管穿越防火分区}
            - {type: 280℃排烟防火阀, application: 排烟风管}
          action: 温度熔断自动关闭
          reset: 手动复位
        
        location_hint:
          space_type: DUCT
          position: 穿越防火分隔处
        
        control_points:
          status:
            - {point_id: FD_CLOSE, type: DI, description: 关闭信号}

      - node_id: HVAC-SMOKE_DST_CONTROL
        node_name: 防排烟控制柜
        node_name_en: Smoke Control Panel
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 防排烟设备控制中心
        medium_in: SIGNAL-FA
        medium_out: CTRL
      
        equipment_parameters:
          functions:
            - 火灾联动控制
            - 手动控制
            - 状态反馈
            - 故障报警
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 风机房/消防控制室
        
        interface_system: FIRE-ALARM

    sink_nodes:
  
      - node_id: HVAC-SMOKE_SNK_EXHAUST
        node_name: 排烟排放口
        node_name_en: Smoke Exhaust Outlet
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 烟气排放
        medium_in: AIR-SMOKE
        is_external: true
      
        location_hint:
          space_type: EXTERIOR
          position: 屋顶
          height: 距屋面≥2m
          requirement: 距可燃物≥6m
        
      - node_id: HVAC-SMOKE_SNK_STAIR
        node_name: 防烟楼梯间
        node_name_en: Smoke-proof Stairwell
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 加压保护
        medium_in: AIR-FA
      
        parameters:
          pressure_diff: {value: 40-50, unit: Pa}
        
      - node_id: HVAC-SMOKE_SNK_VESTIBULE
        node_name: 前室/合用前室
        node_name_en: Vestibule
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 加压保护
        medium_in: AIR-FA
      
        parameters:
          pressure_diff: {value: 25-30, unit: Pa}

  # ============================================================
  # 边定义
  # ============================================================
  edges:

    pressurization_edges:
  
      - edge_id: HVAC-SMOKE_EDGE_001
        edge_name: 进风口至正压风机
        edge_type: TRK
        from_node: HVAC-SMOKE_SRC_OA
        to_node: HVAC-SMOKE_SRC_PRESS_FAN
        direction: unidirectional
        medium: AIR-OA
      
      - edge_id: HVAC-SMOKE_EDGE_002
        edge_name: 正压风机至竖井
        edge_type: TRK
        from_node: HVAC-SMOKE_SRC_PRESS_FAN
        to_node: HVAC-SMOKE_DST_PRESS_SHAFT
        direction: unidirectional
        medium: AIR-FA
      
      - edge_id: HVAC-SMOKE_EDGE_003
        edge_name: 竖井至送风口
        edge_type: BRH
        from_node: HVAC-SMOKE_DST_PRESS_SHAFT
        to_node: HVAC-SMOKE_DST_PRESS_OUTLET
        direction: unidirectional
        medium: AIR-FA
      
      - edge_id: HVAC-SMOKE_EDGE_004
        edge_name: 送风口至楼梯间
        edge_type: TRM
        from_node: HVAC-SMOKE_DST_PRESS_OUTLET
        to_node: HVAC-SMOKE_SNK_STAIR
        direction: unidirectional
        medium: AIR-FA

    exhaust_edges:
  
      - edge_id: HVAC-SMOKE_EDGE_011
        edge_name: 排烟口至竖井
        edge_type: TRM
        from_node: HVAC-SMOKE_DST_EXHAUST_INLET
        to_node: HVAC-SMOKE_DST_EXHAUST_SHAFT
        direction: unidirectional
        medium: AIR-SMOKE
      
      - edge_id: HVAC-SMOKE_EDGE_012
        edge_name: 竖井至排烟风机
        edge_type: TRK
        from_node: HVAC-SMOKE_DST_EXHAUST_SHAFT
        to_node: HVAC-SMOKE_DST_EXHAUST_FAN
        direction: unidirectional
        medium: AIR-SMOKE
      
      - edge_id: HVAC-SMOKE_EDGE_013
        edge_name: 排烟风机至排放口
        edge_type: TRK
        from_node: HVAC-SMOKE_DST_EXHAUST_FAN
        to_node: HVAC-SMOKE_SNK_EXHAUST
        direction: unidirectional
        medium: AIR-SMOKE

    control_edges:
  
      - edge_id: HVAC-SMOKE_EDGE_FA
        edge_name: 火灾报警联动
        edge_type: CTRL
        from_node: FIRE-ALARM_DST_LINKAGE
        to_node: HVAC-SMOKE_DST_CONTROL
        direction: unidirectional
        medium: SIGNAL-FA
        cross_system: true
        source_system: FIRE-ALARM

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:

    - path_id: HVAC-SMOKE_PATH_PRESS
      path_name: 加压送风路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: HVAC-SMOKE_SRC_OA}
        - {step: 2, element_type: edge, element_id: HVAC-SMOKE_EDGE_001}
        - {step: 3, element_type: node, element_id: HVAC-SMOKE_SRC_PRESS_FAN}
        - {step: 4, element_type: edge, element_id: HVAC-SMOKE_EDGE_002}
        - {step: 5, element_type: node, element_id: HVAC-SMOKE_DST_PRESS_SHAFT}
        - {step: 6, element_type: edge, element_id: HVAC-SMOKE_EDGE_003}
        - {step: 7, element_type: node, element_id: HVAC-SMOKE_DST_PRESS_OUTLET}
        - {step: 8, element_type: edge, element_id: HVAC-SMOKE_EDGE_004}
        - {step: 9, element_type: node, element_id: HVAC-SMOKE_SNK_STAIR}
      
    - path_id: HVAC-SMOKE_PATH_EXHAUST
      path_name: 机械排烟路径
      path_type: EXH
      sequence:
        - {step: 1, element_type: node, element_id: HVAC-SMOKE_DST_EXHAUST_INLET}
        - {step: 2, element_type: edge, element_id: HVAC-SMOKE_EDGE_011}
        - {step: 3, element_type: node, element_id: HVAC-SMOKE_DST_EXHAUST_SHAFT}
        - {step: 4, element_type: edge, element_id: HVAC-SMOKE_EDGE_012}
        - {step: 5, element_type: node, element_id: HVAC-SMOKE_DST_EXHAUST_FAN}
        - {step: 6, element_type: edge, element_id: HVAC-SMOKE_EDGE_013}
        - {step: 7, element_type: node, element_id: HVAC-SMOKE_SNK_EXHAUST}

  # ============================================================
  # 联动控制逻辑
  # ============================================================
  control_logic:

    pressurization_sequence:
      trigger: 防烟楼梯间/前室区域火灾确认
      actions:
        - step: 1
          action: 开启着火层及相邻层送风口
        - step: 2
          action: 启动正压送风机
        - step: 3
          action: 检测楼梯间压差
          target: {value: 40-50, unit: Pa}
        
    exhaust_sequence:
      trigger: 防烟分区火灾确认
      actions:
        - step: 1
          action: 开启着火区域排烟口
        - step: 2
          action: 启动排烟风机
        - step: 3
          action: 开启补风设施（如有）
        
    temperature_protection:
      condition: 排烟温度 > 280℃
      action:
        - 排烟防火阀熔断关闭
        - 排烟风机停止
        - 发送信号至消防控制室
      
    pressure_control:
      method: 旁通阀/变频调节
      target: 维持设计压差
      avoid: 压差过大致疏散门无法开启
```

---

## 4.3 PLUMB-HWS 生活热水系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: PLUMB-HWS
    system_name: 生活热水系统
    system_name_en: Domestic Hot Water System
    category: PLUMBING
    version: 1.0
  
    description: |
      医院生活热水供应系统，采用集中换热+循环供水方式。
      通过热水循环保证即开即热。
    
    design_basis:
      supply_temperature: {value: 55-60, unit: ℃}
      return_temperature: {value: 45-50, unit: ℃}
      circulation: 24小时循环
      anti_legionella: 定期高温消毒
    
    serving_scope:
      - 病房淋浴/盥洗
      - 手术刷手
      - 供应室
      - 厨房

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: PLUMB-HWS_BND_IN_CW
        boundary_name: 冷水供应
        medium: WATER-DW
        source_system: PLUMB-DWS
      
      - boundary_id: PLUMB-HWS_BND_IN_HEAT
        boundary_name: 热源
        medium: WATER-HW
        source_system: HVAC-HWP
      
      - boundary_id: PLUMB-HWS_BND_IN_ELEC
        boundary_name: 电源
        medium: ELEC-LV
        source_system: ELEC-LV-MAIN
      
    outputs:
      - boundary_id: PLUMB-HWS_BND_OUT_HW
        boundary_name: 热水终端
        medium: WATER-HW-DOM
        target: 卫生洁具

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:

    source_nodes:
  
      - node_id: PLUMB-HWS_SRC_CW
        node_name: 冷水进水
        node_name_en: Cold Water Inlet
        node_type: Source_Node
        node_category: SRC
      
        function: 生活冷水接入
        medium_out: WATER-DW
      
        source_system: PLUMB-DWS
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 热水机房

      - node_id: PLUMB-HWS_SRC_HEAT
        node_name: 热源接入
        node_name_en: Heat Source Input
        node_type: Source_Node
        node_category: SRC
      
        function: 热水/蒸汽热源接入
        medium_out: WATER-HW
      
        source_system: HVAC-HWP
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 热水机房

    distribution_nodes:
  
      - node_id: PLUMB-HWS_DST_HEX
        node_name: 热水换热器
        node_name_en: DHW Heat Exchanger
        node_type: Distribution_Node
        node_category: DST
        node_subtype: HEX
      
        function: 加热生活冷水
        medium_in: [WATER-DW, WATER-HW]
        medium_out: [WATER-HW-DOM, WATER-HW]
      
        multiplicity: multiple
      
        typical_configuration:
          quantity: 2
          redundancy: 一用一备/并联
        
        equipment_parameters:
          type: 板式换热器/容积式换热器
          capacity: 根据热水负荷
          primary_temp: {value: "60/50", unit: ℃}
          secondary_temp: {value: "55/10", unit: ℃}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 热水机房
        
        control_points:
          sensors:
            - {point_id: HEX_T_CW_IN, type: AI, description: 冷水进水温度}
            - {point_id: HEX_T_HW_OUT, type: AI, description: 热水出水温度}
          commands:
            - {point_id: HEX_VALVE, type: AO, description: 一次侧阀开度}

      - node_id: PLUMB-HWS_DST_STORAGE
        node_name: 热水储罐
        node_name_en: Hot Water Storage Tank
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BUF
      
        function: 热水储存、缓冲
        medium_in: WATER-HW-DOM
        medium_out: WATER-HW-DOM
      
        equipment_parameters:
          capacity: {value: 5-20, unit: m³}
          material: 不锈钢
          insulation: 聚氨酯保温
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 热水机房
        
        control_points:
          sensors:
            - {point_id: TANK_T, type: AI, description: 罐内温度}
            - {point_id: TANK_LEVEL, type: AI, description: 液位}

      - node_id: PLUMB-HWS_DST_CIRC_PUMP
        node_name: 热水循环泵
        node_name_en: DHW Circulation Pump
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 热水循环
        medium_in: WATER-HW-DOM
        medium_out: WATER-HW-DOM
      
        equipment_parameters:
          configuration: 一用一备
          flow: {value: 10-30, unit: m³/h}
          head: {value: 20-30, unit: m}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 热水机房
        
        control_points:
          status:
            - {point_id: CIRC_PUMP_RUN, type: DI, description: 运行状态}

      - node_id: PLUMB-HWS_DST_MAIN_SUP
        node_name: 热水供水主管
        node_name_en: Hot Water Supply Main
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
      
        function: 热水水平输配
        medium_in: WATER-HW-DOM
        medium_out: WATER-HW-DOM
      
        equipment_parameters:
          material: 不锈钢管/PPR管
          insulation: 橡塑保温
          diameter: {value: DN65-DN100, unit: mm}
        
        location_hint:
          space_type: CEILING_VOID / PIPE_TRENCH

      - node_id: PLUMB-HWS_DST_MAIN_RET
        node_name: 热水回水主管
        node_name_en: Hot Water Return Main
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
      
        function: 热水循环回水
        medium_in: WATER-HW-DOM
        medium_out: WATER-HW-DOM
      
        equipment_parameters:
          material: 不锈钢管/PPR管
          insulation: 橡塑保温
          diameter: {value: DN32-DN50, unit: mm}
        
        location_hint:
          space_type: CEILING_VOID / PIPE_TRENCH

      - node_id: PLUMB-HWS_DST_RISER
        node_name: 热水立管
        node_name_en: Hot Water Riser
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 垂直输配
        medium_in: WATER-HW-DOM
        medium_out: WATER-HW-DOM
      
        multiplicity: multiple
      
        equipment_parameters:
          material: 不锈钢管/PPR管
          diameter: {value: DN32-DN50, unit: mm}
        
        location_hint:
          space_type: SHAFT
          shaft_type: 给排水管井

      - node_id: PLUMB-HWS_DST_BRANCH
        node_name: 热水支管
        node_name_en: Hot Water Branch
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BRH
      
        function: 楼层分配
        medium_in: WATER-HW-DOM
        medium_out: WATER-HW-DOM
      
        equipment_parameters:
          material: PPR管
          diameter: {value: DN20-DN32, unit: mm}
        
        location_hint:
          space_type: CEILING_VOID / WALL

      - node_id: PLUMB-HWS_DST_TMV
        node_name: 恒温混水阀
        node_name_en: Thermostatic Mixing Valve
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 冷热水混合、防烫伤
        medium_in: [WATER-HW-DOM, WATER-DW]
        medium_out: WATER-MIXED
      
        multiplicity: multiple
      
        equipment_parameters:
          outlet_temp: {value: 38-43, unit: ℃}
          anti_scald: true
        
        location_hint:
          space_type: WALL_BOX
          position: 淋浴间入口

    sink_nodes:
  
      - node_id: PLUMB-HWS_SNK_FIXTURE
        node_name: 热水终端
        node_name_en: Hot Water Fixture
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 热水使用
        medium_in: WATER-HW-DOM
      
        multiplicity: multiple
      
        equipment_parameters:
          types:
            - 淋浴器
            - 洗手盆
            - 污洗盆
          
        location_hint:
          space_type: WET_ROOM

  # ============================================================
  # 边定义
  # ============================================================
  edges:

    supply_edges:
  
      - edge_id: PLUMB-HWS_EDGE_001
        edge_name: 冷水至换热器
        edge_type: TRK
        from_node: PLUMB-HWS_SRC_CW
        to_node: PLUMB-HWS_DST_HEX
        direction: unidirectional
        medium: WATER-DW
      
      - edge_id: PLUMB-HWS_EDGE_002
        edge_name: 热源至换热器
        edge_type: TRK
        from_node: PLUMB-HWS_SRC_HEAT
        to_node: PLUMB-HWS_DST_HEX
        direction: unidirectional
        medium: WATER-HW
      
      - edge_id: PLUMB-HWS_EDGE_003
        edge_name: 换热器至储罐
        edge_type: TRK
        from_node: PLUMB-HWS_DST_HEX
        to_node: PLUMB-HWS_DST_STORAGE
        direction: unidirectional
        medium: WATER-HW-DOM
      
      - edge_id: PLUMB-HWS_EDGE_004
        edge_name: 储罐至循环泵
        edge_type: TRK
        from_node: PLUMB-HWS_DST_STORAGE
        to_node: PLUMB-HWS_DST_CIRC_PUMP
        direction: unidirectional
        medium: WATER-HW-DOM
      
      - edge_id: PLUMB-HWS_EDGE_005
        edge_name: 循环泵至供水主管
        edge_type: TRK
        from_node: PLUMB-HWS_DST_CIRC_PUMP
        to_node: PLUMB-HWS_DST_MAIN_SUP
        direction: unidirectional
        medium: WATER-HW-DOM
      
      - edge_id: PLUMB-HWS_EDGE_006
        edge_name: 供水主管至立管
        edge_type: BRH
        from_node: PLUMB-HWS_DST_MAIN_SUP
        to_node: PLUMB-HWS_DST_RISER
        direction: unidirectional
        medium: WATER-HW-DOM
      
      - edge_id: PLUMB-HWS_EDGE_007
        edge_name: 立管至支管
        edge_type: BRH
        from_node: PLUMB-HWS_DST_RISER
        to_node: PLUMB-HWS_DST_BRANCH
        direction: unidirectional
        medium: WATER-HW-DOM
      
      - edge_id: PLUMB-HWS_EDGE_008
        edge_name: 支管至终端
        edge_type: TRM
        from_node: PLUMB-HWS_DST_BRANCH
        to_node: PLUMB-HWS_SNK_FIXTURE
        direction: unidirectional
        medium: WATER-HW-DOM

    return_edges:
  
      - edge_id: PLUMB-HWS_EDGE_RET_001
        edge_name: 立管回水至回水主管
        edge_type: TRK
        from_node: PLUMB-HWS_DST_RISER
        to_node: PLUMB-HWS_DST_MAIN_RET
        direction: unidirectional
        medium: WATER-HW-DOM
      
      - edge_id: PLUMB-HWS_EDGE_RET_002
        edge_name: 回水主管至储罐
        edge_type: TRK
        from_node: PLUMB-HWS_DST_MAIN_RET
        to_node: PLUMB-HWS_DST_STORAGE
        direction: unidirectional
        medium: WATER-HW-DOM

  # ============================================================
  # 路径与回路
  # ============================================================
  typical_paths:

    - path_id: PLUMB-HWS_PATH_SUP
      path_name: 热水供水路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: PLUMB-HWS_SRC_CW}
        - {step: 2, element_type: node, element_id: PLUMB-HWS_DST_HEX}
        - {step: 3, element_type: node, element_id: PLUMB-HWS_DST_STORAGE}
        - {step: 4, element_type: node, element_id: PLUMB-HWS_DST_CIRC_PUMP}
        - {step: 5, element_type: node, element_id: PLUMB-HWS_DST_MAIN_SUP}
        - {step: 6, element_type: node, element_id: PLUMB-HWS_DST_RISER}
        - {step: 7, element_type: node, element_id: PLUMB-HWS_DST_BRANCH}
        - {step: 8, element_type: node, element_id: PLUMB-HWS_SNK_FIXTURE}

  loops:

    - loop_id: PLUMB-HWS_LOOP_CIRC
      loop_name: 热水循环回路
      loop_name_en: DHW Circulation Loop
      loop_type: closed
    
      description: |
        热水从储罐经循环泵、供水主管、立管至最远端，
        未使用的热水通过回水管返回储罐，保持水温。
      
      circulation: 24小时
      velocity: {value: "≥0.5", unit: m/s}

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:

    temperature_control:
      setpoint: {value: 55-60, unit: ℃}
      sensor: 储罐或出水温度
      control: 一次侧阀开度调节
    
    anti_legionella:
      description: 军团菌防控
      measures:
        - 储水温度≥55℃
        - 定期高温消毒（70℃×10min）
        - 避免死水段
        - 回水温度≥50℃
      
    circulation_control:
      mode: 24小时循环
      pump_control: 连续运行或时间控制
```

---

## 4.4 ELEC-UPS 不间断电源系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: ELEC-UPS
    system_name: 不间断电源系统
    system_name_en: Uninterruptible Power Supply System
    category: ELECTRICAL
    version: 1.0
  
    description: |
      医院不间断电源系统，为数据中心、医疗信息系统、手术室监护设备等
      关键负荷提供不间断、高质量的电源供应。
    
    design_basis:
      capacity: 根据负荷计算
      backup_time: {value: 15-30, unit: min}
      configuration: "N+1冗余或2N"
    
    serving_scope:
      - 数据中心
      - HIS/PACS服务器
      - 手术室监护设备
      - ICU监护设备
      - 检验设备

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: ELEC-UPS_BND_IN_AC
        boundary_name: 市电输入
        medium: ELEC-LV
        source_system: ELEC-LV-CRITICAL
        note: 经ATS双电源供电
      
    outputs:
      - boundary_id: ELEC-UPS_BND_OUT_UPS
        boundary_name: UPS输出
        medium: ELEC-UPS
        target: 关键IT/医疗设备

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:

    source_nodes:
  
      - node_id: ELEC-UPS_SRC_AC_INPUT
        node_name: UPS输入配电
        node_name_en: UPS Input Distribution
        node_type: Source_Node
        node_category: SRC
      
        function: 市电接入
        medium_out: ELEC-LV
      
        source_system: ELEC-LV-MAIN
      
        location_hint:
          space_type: MEP_ROOM
          room_name: UPS机房

    distribution_nodes:
  
      - node_id: ELEC-UPS_DST_UPS_UNIT
        node_name: UPS主机
        node_name_en: UPS Unit
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
      
        function: 电源转换、不间断供电
        medium_in: ELEC-LV
        medium_out: ELEC-UPS
      
        multiplicity: multiple
        instance_pattern: ELEC-UPS_DST_UPS_UNIT_{NN}
      
        typical_configuration:
          quantity: 2-4
          redundancy: "N+1"
          parallel: true
        
        equipment_parameters:
          type: 在线双变换式
          capacity_each: {value: 100-300, unit: kVA}
          input_voltage: {value: "380/220", unit: V}
          output_voltage: {value: "380/220", unit: V}
          efficiency: {value: "≥94", unit: "%"}
          power_factor: {value: 0.9, unit: null}
          transfer_time: {value: 0, unit: ms}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: UPS机房
          floor: 地下室/设备层
        
        installation_requirements:
          - 空调温控（18-25℃）
          - 防尘
          - 承重检查
          - 进出线通道
          - 维护通道
        
        control_points:
          sensors:
            - {point_id: UPS_V_IN, type: AI, description: 输入电压}
            - {point_id: UPS_V_OUT, type: AI, description: 输出电压}
            - {point_id: UPS_I_OUT, type: AI, description: 输出电流}
            - {point_id: UPS_LOAD, type: AI, description: 负载率}
            - {point_id: UPS_BAT_V, type: AI, description: 电池电压}
            - {point_id: UPS_BAT_CAP, type: AI, description: 电池剩余容量}
            - {point_id: UPS_TEMP, type: AI, description: 内部温度}
          status:
            - {point_id: UPS_MODE, type: DI, description: 运行模式}
            - {point_id: UPS_BYPASS, type: DI, description: 旁路状态}
            - {point_id: UPS_FAULT, type: DI, description: 故障报警}
            - {point_id: UPS_BAT_LOW, type: DI, description: 电池低电量}
            - {point_id: UPS_OVERLOAD, type: DI, description: 过载报警}

      - node_id: ELEC-UPS_DST_BATTERY
        node_name: 蓄电池组
        node_name_en: Battery Bank
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BUF
      
        function: 储能、后备供电
        medium_in: ELEC-DC
        medium_out: ELEC-DC
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 阀控密封铅酸电池/锂电池
          voltage: {value: 384-480, unit: VDC}
          capacity: 根据后备时间计算
          backup_time: {value: 15-30, unit: min}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: UPS机房/电池室
        
        installation_requirements:
          - 电池架
          - 通风换气
          - 温度控制（20-25℃）
          - 防酸处理（铅酸电池）
          - 承重验算
          - 消防措施
        
        control_points:
          sensors:
            - {point_id: BAT_V, type: AI, description: 总电压}
            - {point_id: BAT_I, type: AI, description: 充放电电流}
            - {point_id: BAT_TEMP, type: AI, description: 电池温度}
            - {point_id: BAT_SOC, type: AI, description: 剩余容量}
          status:
            - {point_id: BAT_CHARGING, type: DI, description: 充电状态}
            - {point_id: BAT_FAULT, type: DI, description: 电池故障}

      - node_id: ELEC-UPS_DST_STS
        node_name: 静态转换开关
        node_name_en: Static Transfer Switch
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: UPS输出切换/并联
        medium_in: ELEC-UPS
        medium_out: ELEC-UPS
      
        equipment_parameters:
          type: 静态转换开关
          transfer_time: {value: "<4", unit: ms}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: UPS机房
        
        note: 2N系统时使用

      - node_id: ELEC-UPS_DST_OUTPUT_PANEL
        node_name: UPS输出配电柜
        node_name_en: UPS Output Distribution Panel
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: UPS输出配电分配
        medium_in: ELEC-UPS
        medium_out: ELEC-UPS
      
        equipment_parameters:
          type: 低压开关柜
          rated_current: {value: 400-800, unit: A}
          circuits: 多回路分配
        
        location_hint:
          space_type: MEP_ROOM
          room_name: UPS机房
        
        control_points:
          sensors:
            - {point_id: UPS_OUT_V, type: AI, description: 输出电压}
            - {point_id: UPS_OUT_P, type: AI, description: 输出功率}

      - node_id: ELEC-UPS_DST_PDU
        node_name: 机架配电单元
        node_name_en: Power Distribution Unit
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRM
      
        function: 机柜级配电
        medium_in: ELEC-UPS
        medium_out: ELEC-UPS
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 智能PDU
          outlets: {value: 20-42, unit: 位}
          metering: 分路计量
        
        location_hint:
          space_type: RACK
          position: 机柜内

    sink_nodes:
  
      - node_id: ELEC-UPS_SNK_IT
        node_name: IT设备
        node_name_en: IT Equipment
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: IT负载
        medium_in: ELEC-UPS
      
        equipment_parameters:
          types:
            - 服务器
            - 存储设备
            - 网络设备
          
        location_hint:
          space_type: RACK
          room_name: 数据中心

      - node_id: ELEC-UPS_SNK_MEDICAL
        node_name: 医疗设备
        node_name_en: Medical Equipment
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 医疗负载
        medium_in: ELEC-UPS
      
        equipment_parameters:
          types:
            - 监护仪
            - 输液泵
            - 呼吸机电子控制部分
          
        location_hint:
          space_type: MEDICAL
          position: 手术室、ICU

  # ============================================================
  # 边定义
  # ============================================================
  edges:

    supply_edges:
  
      - edge_id: ELEC-UPS_EDGE_001
        edge_name: 输入配电至UPS
        edge_type: TRK
        from_node: ELEC-UPS_SRC_AC_INPUT
        to_node: ELEC-UPS_DST_UPS_UNIT
        direction: unidirectional
        medium: ELEC-LV
      
      - edge_id: ELEC-UPS_EDGE_002
        edge_name: 电池至UPS
        edge_type: TRK
        from_node: ELEC-UPS_DST_BATTERY
        to_node: ELEC-UPS_DST_UPS_UNIT
        direction: bidirectional
        medium: ELEC-DC
        note: 充电/放电双向
      
      - edge_id: ELEC-UPS_EDGE_003
        edge_name: UPS至输出柜
        edge_type: TRK
        from_node: ELEC-UPS_DST_UPS_UNIT
        to_node: ELEC-UPS_DST_OUTPUT_PANEL
        direction: unidirectional
        medium: ELEC-UPS
      
      - edge_id: ELEC-UPS_EDGE_004
        edge_name: 输出柜至PDU
        edge_type: BRH
        from_node: ELEC-UPS_DST_OUTPUT_PANEL
        to_node: ELEC-UPS_DST_PDU
        direction: unidirectional
        medium: ELEC-UPS
      
      - edge_id: ELEC-UPS_EDGE_005
        edge_name: PDU至IT设备
        edge_type: TRM
        from_node: ELEC-UPS_DST_PDU
        to_node: ELEC-UPS_SNK_IT
        direction: unidirectional
        medium: ELEC-UPS

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:

    - path_id: ELEC-UPS_PATH_NORMAL
      path_name: 正常供电路径
      path_type: SUP
      mode: 市电正常
      sequence:
        - {step: 1, element_type: node, element_id: ELEC-UPS_SRC_AC_INPUT}
        - {step: 2, element_type: edge, element_id: ELEC-UPS_EDGE_001}
        - {step: 3, element_type: node, element_id: ELEC-UPS_DST_UPS_UNIT}
        - {step: 4, element_type: edge, element_id: ELEC-UPS_EDGE_003}
        - {step: 5, element_type: node, element_id: ELEC-UPS_DST_OUTPUT_PANEL}
        - {step: 6, element_type: edge, element_id: ELEC-UPS_EDGE_004}
        - {step: 7, element_type: node, element_id: ELEC-UPS_DST_PDU}
        - {step: 8, element_type: edge, element_id: ELEC-UPS_EDGE_005}
        - {step: 9, element_type: node, element_id: ELEC-UPS_SNK_IT}
      
    - path_id: ELEC-UPS_PATH_BATTERY
      path_name: 电池供电路径
      path_type: BKP
      mode: 市电中断
      sequence:
        - {step: 1, element_type: node, element_id: ELEC-UPS_DST_BATTERY}
        - {step: 2, element_type: edge, element_id: ELEC-UPS_EDGE_002}
        - {step: 3, element_type: node, element_id: ELEC-UPS_DST_UPS_UNIT}
        - {step: 4, element_type: edge, element_id: ELEC-UPS_EDGE_003}
        - {step: 5, element_type: node, element_id: ELEC-UPS_DST_OUTPUT_PANEL}

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:

    operating_modes:
      normal:
        description: 市电正常
        operation: 整流→逆变→输出
        battery_state: 浮充
      
      battery:
        description: 市电中断
        operation: 电池→逆变→输出
        trigger: 输入电压异常
        transfer_time: {value: 0, unit: ms}
      
      bypass:
        description: 旁路模式
        operation: 市电直接输出
        trigger: UPS维护或故障
      
    battery_management:
      float_charge: 浮充电压根据温度补偿
      equalize_charge: 定期均衡充电
      discharge_protection: 低电压保护
    
    alarm_logic:
      - condition: 市电异常
        level: 告警
        action: 切换至电池
      
      - condition: 电池低电量
        level: 预警
        action: 通知运维人员
      
      - condition: 电池耗尽
        level: 紧急
        action: 有序关机保护
```

---

## 4.5 MGAS-AGSS 麻醉废气排放系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: MGAS-AGSS
    system_name: 麻醉废气排放系统
    system_name_en: Anesthetic Gas Scavenging System
    category: MEDICAL_GAS
    version: 1.0
  
    description: |
      手术室麻醉废气收集与排放系统，
      收集麻醉机呼出废气，通过管网排至室外或接入排风系统。
      保护手术室内医护人员健康。
    
    design_basis:
      vacuum_level: {value: -25 ~ -50, unit: mmH2O}
      flow_per_terminal: {value: 50, unit: L/min}
      disposal: 高空排放或接入排风
    
    serving_scope:
      - 手术室
      - 产房
      - 胃肠镜室

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: MGAS-AGSS_BND_IN_WASTE
        boundary_name: 麻醉废气
        medium: GAS-AGSS
        source: 麻醉机排气口
      
    outputs:
      - boundary_id: MGAS-AGSS_BND_OUT_EXHAUST
        boundary_name: 废气排放
        medium: AIR-EA
        is_external: true
        target: 大气/排风系统

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:

    source_nodes:
  
      - node_id: MGAS-AGSS_SRC_TERMINAL
        node_name: 麻醉废气收集终端
        node_name_en: AGSS Collection Terminal
        node_type: Source_Node
        node_category: SRC
      
        function: 收集麻醉机废气
        medium_out: GAS-AGSS
      
        multiplicity: multiple
        instance_pattern: MGAS-AGSS_SRC_TERMINAL_OR{NN}_{Seq}
      
        equipment_parameters:
          type: 快速接头
          color_code: 紫色
          flow: {value: 50, unit: L/min}
          quantity_per_or: 2
        
        location_hint:
          space_type: PENDANT
          position: 手术室吊塔
        
        typical_quantity:
          per_or: 2

    distribution_nodes:
  
      - node_id: MGAS-AGSS_DST_INTERFACE
        node_name: 麻醉机接口装置
        node_name_en: Anesthesia Machine Interface
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 连接麻醉机APL阀排气
        medium_in: GAS-AGSS
        medium_out: GAS-AGSS
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 开放式/闭合式
          flow_indicator: 有
          adjustment: 流量调节
        
        location_hint:
          space_type: EQUIPMENT
          position: 麻醉机上

      - node_id: MGAS-AGSS_DST_BRANCH
        node_name: 废气支管
        node_name_en: AGSS Branch Pipe
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BRH
      
        function: 收集手术室废气
        medium_in: GAS-AGSS
        medium_out: GAS-AGSS
      
        equipment_parameters:
          material: 铜管/不锈钢管
          diameter: {value: DN25-DN32, unit: mm}
        
        location_hint:
          space_type: CEILING_VOID
          position: 手术室吊顶内

      - node_id: MGAS-AGSS_DST_MAIN_PIPE
        node_name: 废气主管
        node_name_en: AGSS Main Pipe
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
      
        function: 汇集废气
        medium_in: GAS-AGSS
        medium_out: GAS-AGSS
      
        equipment_parameters:
          material: 镀锌钢管/不锈钢管
          diameter: {value: DN50-DN80, unit: mm}
          slope: {value: "≥3‰", note: 向泵站倾斜}
        
        location_hint:
          space_type: CEILING_VOID / SHAFT
          position: 手术部走廊吊顶

      - node_id: MGAS-AGSS_DST_PUMP
        node_name: 废气排放泵
        node_name_en: AGSS Exhaust Pump
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 产生负压、抽排废气
        medium_in: GAS-AGSS
        medium_out: AIR-EA
      
        equipment_parameters:
          type: 专用AGSS泵/真空泵
          flow: {value: 500-1000, unit: L/min}
          vacuum: {value: -50, unit: mmH2O}
          power: {value: 0.5-2, unit: kW}
          configuration: 一用一备
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 医气机房/屋顶
        
        installation_requirements:
          - 通风良好
          - 远离人员区域
        
        control_points:
          sensors:
            - {point_id: AGSS_VAC, type: AI, description: 负压值}
          status:
            - {point_id: AGSS_PUMP_RUN, type: DI, description: 运行状态}
            - {point_id: AGSS_PUMP_FAULT, type: DI, description: 故障报警}

      - node_id: MGAS-AGSS_DST_DILUTION
        node_name: 稀释接口
        node_name_en: Dilution Interface
        node_type: Distribution_Node
        node_category: DST
        node_subtype: JUN
      
        function: 废气与排风混合稀释
        medium_in: [GAS-AGSS, AIR-EA]
        medium_out: AIR-EA
      
        equipment_parameters:
          dilution_ratio: "≥1:10"
        
        location_hint:
          space_type: CEILING_VOID
          position: 排风主管接入点
        
        interface_system: HVAC-CLEAN
      
        note: 接入净化空调排风系统方案

    sink_nodes:
  
      - node_id: MGAS-AGSS_SNK_EXHAUST
        node_name: 废气排放口
        node_name_en: AGSS Exhaust Outlet
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 废气排放
        medium_in: AIR-EA
        is_external: true
      
        location_hint:
          space_type: EXTERIOR
          position: 屋顶高空排放
          height: ≥ 3m高于屋面
          requirement: 远离新风口、人员活动区

  # ============================================================
  # 边定义
  # ============================================================
  edges:

    collection_edges:
  
      - edge_id: MGAS-AGSS_EDGE_001
        edge_name: 终端至接口装置
        edge_type: TRM
        from_node: MGAS-AGSS_SRC_TERMINAL
        to_node: MGAS-AGSS_DST_INTERFACE
        direction: unidirectional
        medium: GAS-AGSS
        physical_properties:
          type: 软管连接
        
      - edge_id: MGAS-AGSS_EDGE_002
        edge_name: 接口装置至支管
        edge_type: TRK
        from_node: MGAS-AGSS_DST_INTERFACE
        to_node: MGAS-AGSS_DST_BRANCH
        direction: unidirectional
        medium: GAS-AGSS
      
      - edge_id: MGAS-AGSS_EDGE_003
        edge_name: 支管至主管
        edge_type: BRH
        from_node: MGAS-AGSS_DST_BRANCH
        to_node: MGAS-AGSS_DST_MAIN_PIPE
        direction: unidirectional
        medium: GAS-AGSS

    exhaust_edges_option_1:
      description: 方案一：独立AGSS泵排放
    
      - edge_id: MGAS-AGSS_EDGE_004A
        edge_name: 主管至AGSS泵
        edge_type: TRK
        from_node: MGAS-AGSS_DST_MAIN_PIPE
        to_node: MGAS-AGSS_DST_PUMP
        direction: unidirectional
        medium: GAS-AGSS
      
      - edge_id: MGAS-AGSS_EDGE_005A
        edge_name: AGSS泵至排放口
        edge_type: TRK
        from_node: MGAS-AGSS_DST_PUMP
        to_node: MGAS-AGSS_SNK_EXHAUST
        direction: unidirectional
        medium: AIR-EA

    exhaust_edges_option_2:
      description: 方案二：接入排风系统
    
      - edge_id: MGAS-AGSS_EDGE_004B
        edge_name: 主管至稀释接口
        edge_type: TRK
        from_node: MGAS-AGSS_DST_MAIN_PIPE
        to_node: MGAS-AGSS_DST_DILUTION
        direction: unidirectional
        medium: GAS-AGSS
      
      - edge_id: MGAS-AGSS_EDGE_005B
        edge_name: 稀释接口至排风系统
        edge_type: TRK
        from_node: MGAS-AGSS_DST_DILUTION
        to_node: HVAC-CLEAN_DST_EA_MAIN
        direction: unidirectional
        medium: AIR-EA
        cross_system: true
        target_system: HVAC-CLEAN

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:

    - path_id: MGAS-AGSS_PATH_MAIN
      path_name: 麻醉废气排放路径
      path_type: EXH
      sequence:
        - {step: 1, element_type: node, element_id: MGAS-AGSS_SRC_TERMINAL}
        - {step: 2, element_type: edge, element_id: MGAS-AGSS_EDGE_001}
        - {step: 3, element_type: node, element_id: MGAS-AGSS_DST_INTERFACE}
        - {step: 4, element_type: edge, element_id: MGAS-AGSS_EDGE_002}
        - {step: 5, element_type: node, element_id: MGAS-AGSS_DST_BRANCH}
        - {step: 6, element_type: edge, element_id: MGAS-AGSS_EDGE_003}
        - {step: 7, element_type: node, element_id: MGAS-AGSS_DST_MAIN_PIPE}
        - {step: 8, element_type: edge, element_id: MGAS-AGSS_EDGE_004A}
        - {step: 9, element_type: node, element_id: MGAS-AGSS_DST_PUMP}
        - {step: 10, element_type: edge, element_id: MGAS-AGSS_EDGE_005A}
        - {step: 11, element_type: node, element_id: MGAS-AGSS_SNK_EXHAUST}

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:

    pump_control:
      mode: 连续运行或联动运行
      interlock: 手术室使用时AGSS泵运行
    
    vacuum_control:
      setpoint: {value: -30 ~ -50, unit: mmH2O}
      alarm: 负压过低/过高
    
    safety_interlock:
      hvac_coordination:
        condition: 接入排风系统方案
        requirement: 排风机运行时AGSS方可排放
        ratio: AGSS流量 ≤ 排风量×10%
```

---

## 4.6 PLUMB-MED-WASTE 医疗废水系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: PLUMB-MED-WASTE
    system_name: 医疗废水系统
    system_name_en: Medical Wastewater System
    category: PLUMBING
    version: 1.0
  
    description: |
      医院医疗废水预处理系统，收集手术室、实验室、放射科等
      特殊医疗区域的废水，经预处理后排入污水处理站或市政管网。
    
    design_basis:
      wastewater_types:
        - 手术废水
        - 实验室废水
        - 传染病房废水
        - 放射性废水（另设）
      treatment: 消毒+预处理
    
    serving_scope:
      - 手术室
      - 检验科
      - 病理科
      - ICU
      - 传染病区

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: PLUMB-MED-WASTE_BND_IN_WASTE
        boundary_name: 医疗废水
        medium: WATER-MED-WASTE
        source: 医疗区域排水
      
    outputs:
      - boundary_id: PLUMB-MED-WASTE_BND_OUT_SAN
        boundary_name: 预处理后废水
        medium: WATER-WASTE
        target_system: PLUMB-SAN

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:

    source_nodes:
  
      - node_id: PLUMB-MED-WASTE_SRC_OR
        node_name: 手术室排水
        node_name_en: OR Drain
        node_type: Source_Node
        node_category: SRC
      
        function: 手术废水收集
        medium_out: WATER-MED-WASTE
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 手术区域排水
          contains: 血液、体液、冲洗水
        
        location_hint:
          space_type: FLOOR
          position: 手术室地面排水

      - node_id: PLUMB-MED-WASTE_SRC_LAB
        node_name: 实验室排水
        node_name_en: Laboratory Drain
        node_type: Source_Node
        node_category: SRC
      
        function: 实验废水收集
        medium_out: WATER-MED-WASTE
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 实验室排水
          contains: 化学试剂、生物样品残液
        
        location_hint:
          space_type: COUNTER
          position: 实验台水槽

      - node_id: PLUMB-MED-WASTE_SRC_INFECT
        node_name: 传染病区排水
        node_name_en: Infectious Ward Drain
        node_type: Source_Node
        node_category: SRC
      
        function: 传染性废水收集
        medium_out: WATER-MED-WASTE
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 传染病房排水
          contains: 可能含病原体
        
        location_hint:
          space_type: WET_ROOM
          position: 传染病区卫生间

    distribution_nodes:
  
      - node_id: PLUMB-MED-WASTE_DST_STACK
        node_name: 医疗废水立管
        node_name_en: Medical Waste Stack
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
      
        function: 垂直收集
        medium_in: WATER-MED-WASTE
        medium_out: WATER-MED-WASTE
      
        multiplicity: multiple
      
        equipment_parameters:
          material: HDPE管
          diameter: {value: DN100-DN150, unit: mm}
        
        location_hint:
          space_type: SHAFT
          shaft_type: 污水管井

      - node_id: PLUMB-MED-WASTE_DST_MAIN
        node_name: 医疗废水横干管
        node_name_en: Medical Waste Main
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
      
        function: 汇集至处理站
        medium_in: WATER-MED-WASTE
        medium_out: WATER-MED-WASTE
      
        equipment_parameters:
          material: HDPE管
          diameter: {value: DN150-DN200, unit: mm}
          slope: {value: "0.5-1%", unit: null}
        
        location_hint:
          space_type: CEILING_VOID / TRENCH
          position: 地下室

      - node_id: PLUMB-MED-WASTE_DST_PRETREAT
        node_name: 预处理池
        node_name_en: Pretreatment Tank
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
      
        function: 废水预处理
        medium_in: WATER-MED-WASTE
        medium_out: WATER-WASTE
      
        equipment_parameters:
          type: 预处理池
          components:
            - 调节池
            - 消毒池
            - 沉淀池
          capacity: 按日排水量设计
          retention_time: {value: 1-2, unit: h}
        
        location_hint:
          space_type: OUTDOOR / UNDERGROUND
          position: 污水处理站区域
        
        installation_requirements:
          - 密封防臭
          - 通气管
          - 检修通道
          - 防腐处理

      - node_id: PLUMB-MED-WASTE_DST_DISINFECT
        node_name: 消毒装置
        node_name_en: Disinfection Unit
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
      
        function: 废水消毒
        medium_in: WATER-MED-WASTE
        medium_out: WATER-WASTE
      
        equipment_parameters:
          methods:
            - {type: 次氯酸钠, dose: 30-50mg/L}
            - {type: 二氧化氯, dose: 20-30mg/L}
            - {type: 臭氧, dose: 10-20mg/L}
          contact_time: {value: 30-60, unit: min}
          residual_chlorine: {value: 0.5-1.0, unit: mg/L}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 污水处理站
        
        control_points:
          sensors:
            - {point_id: CL_DOSE, type: AI, description: 加药量}
            - {point_id: CL_RESIDUAL, type: AI, description: 余氯}
            - {point_id: PH, type: AI, description: pH值}
          status:
            - {point_id: DOSE_PUMP_RUN, type: DI, description: 加药泵运行}

      - node_id: PLUMB-MED-WASTE_DST_SAMPLE
        node_name: 取样井
        node_name_en: Sampling Manhole
        node_type: Distribution_Node
        node_category: DST
        node_subtype: MON
      
        function: 水质取样检测
        medium_in: WATER-WASTE
        medium_out: WATER-WASTE
      
        equipment_parameters:
          sampling: 定期取样检测
          parameters: [pH, COD, BOD, 余氯, 大肠杆菌]
        
        location_hint:
          space_type: OUTDOOR
          position: 排放前检查井

    sink_nodes:
  
      - node_id: PLUMB-MED-WASTE_SNK_SEPTIC
        node_name: 化粪池/污水站
        node_name_en: Septic Tank / WWTP
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 进一步处理或排放
        medium_in: WATER-WASTE
      
        interface_system: PLUMB-SAN
      
        location_hint:
          space_type: OUTDOOR
          position: 污水处理站

  # ============================================================
  # 边定义
  # ============================================================
  edges:

    collection_edges:
  
      - edge_id: PLUMB-MED-WASTE_EDGE_001
        edge_name: 手术室至立管
        edge_type: TRM
        from_node: PLUMB-MED-WASTE_SRC_OR
        to_node: PLUMB-MED-WASTE_DST_STACK
        direction: unidirectional
        medium: WATER-MED-WASTE
      
      - edge_id: PLUMB-MED-WASTE_EDGE_002
        edge_name: 实验室至立管
        edge_type: TRM
        from_node: PLUMB-MED-WASTE_SRC_LAB
        to_node: PLUMB-MED-WASTE_DST_STACK
        direction: unidirectional
        medium: WATER-MED-WASTE
      
      - edge_id: PLUMB-MED-WASTE_EDGE_003
        edge_name: 传染区至立管
        edge_type: TRM
        from_node: PLUMB-MED-WASTE_SRC_INFECT
        to_node: PLUMB-MED-WASTE_DST_STACK
        direction: unidirectional
        medium: WATER-MED-WASTE
      
      - edge_id: PLUMB-MED-WASTE_EDGE_004
        edge_name: 立管至横干管
        edge_type: BRH
        from_node: PLUMB-MED-WASTE_DST_STACK
        to_node: PLUMB-MED-WASTE_DST_MAIN
        direction: unidirectional
        medium: WATER-MED-WASTE

    treatment_edges:
  
      - edge_id: PLUMB-MED-WASTE_EDGE_005
        edge_name: 横干管至预处理池
        edge_type: TRK
        from_node: PLUMB-MED-WASTE_DST_MAIN
        to_node: PLUMB-MED-WASTE_DST_PRETREAT
        direction: unidirectional
        medium: WATER-MED-WASTE
      
      - edge_id: PLUMB-MED-WASTE_EDGE_006
        edge_name: 预处理池至消毒
        edge_type: TRK
        from_node: PLUMB-MED-WASTE_DST_PRETREAT
        to_node: PLUMB-MED-WASTE_DST_DISINFECT
        direction: unidirectional
        medium: WATER-MED-WASTE
      
      - edge_id: PLUMB-MED-WASTE_EDGE_007
        edge_name: 消毒至取样井
        edge_type: TRK
        from_node: PLUMB-MED-WASTE_DST_DISINFECT
        to_node: PLUMB-MED-WASTE_DST_SAMPLE
        direction: unidirectional
        medium: WATER-WASTE
      
      - edge_id: PLUMB-MED-WASTE_EDGE_008
        edge_name: 取样井至化粪池
        edge_type: TRK
        from_node: PLUMB-MED-WASTE_DST_SAMPLE
        to_node: PLUMB-MED-WASTE_SNK_SEPTIC
        direction: unidirectional
        medium: WATER-WASTE
        cross_system: true
        target_system: PLUMB-SAN

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:

    - path_id: PLUMB-MED-WASTE_PATH_MAIN
      path_name: 医疗废水处理路径
      path_type: DRN
      sequence:
        - {step: 1, element_type: node, element_id: PLUMB-MED-WASTE_SRC_OR}
        - {step: 2, element_type: edge, element_id: PLUMB-MED-WASTE_EDGE_001}
        - {step: 3, element_type: node, element_id: PLUMB-MED-WASTE_DST_STACK}
        - {step: 4, element_type: edge, element_id: PLUMB-MED-WASTE_EDGE_004}
        - {step: 5, element_type: node, element_id: PLUMB-MED-WASTE_DST_MAIN}
        - {step: 6, element_type: edge, element_id: PLUMB-MED-WASTE_EDGE_005}
        - {step: 7, element_type: node, element_id: PLUMB-MED-WASTE_DST_PRETREAT}
        - {step: 8, element_type: edge, element_id: PLUMB-MED-WASTE_EDGE_006}
        - {step: 9, element_type: node, element_id: PLUMB-MED-WASTE_DST_DISINFECT}
        - {step: 10, element_type: edge, element_id: PLUMB-MED-WASTE_EDGE_007}
        - {step: 11, element_type: node, element_id: PLUMB-MED-WASTE_DST_SAMPLE}
        - {step: 12, element_type: edge, element_id: PLUMB-MED-WASTE_EDGE_008}
        - {step: 13, element_type: node, element_id: PLUMB-MED-WASTE_SNK_SEPTIC}

  # ============================================================
  # 合规要求
  # ============================================================
  regulatory_requirements:

    discharge_standards:
      reference: GB18466 医疗机构水污染物排放标准
      parameters:
        - {parameter: pH, limit: "6-9"}
        - {parameter: COD, limit: "≤250mg/L", note: 预处理标准}
        - {parameter: BOD5, limit: "≤100mg/L"}
        - {parameter: 粪大肠杆菌, limit: "≤5000MPN/L"}
        - {parameter: 余氯, limit: "0.5-1.0mg/L", note: 接触消毒后}
      
    special_waste:
      radioactive:
        description: 放射性废水单独收集处理
        retention_time: 根据同位素半衰期
      
      infectious:
        description: 传染性废水需强化消毒
        chlorine_dose: 增加50%
```

---

## 4.7 FIRE-GAS 气体灭火系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: FIRE-GAS
    system_name: 气体灭火系统
    system_name_en: Gas Fire Suppression System
    category: FIRE_PROTECTION
    version: 1.0
  
    description: |
      医院气体灭火系统，用于数据中心、配电室等不宜用水灭火的区域。
      采用七氟丙烷、IG541等洁净气体灭火剂。
    
    design_basis:
      agents:
        - {type: 七氟丙烷, code: HFC-227ea, concentration: "8-10%"}
        - {type: IG541, concentration: "37.5-43%"}
      system_type: 全淹没
      discharge_time: {value: "≤10", unit: s}
    
    serving_scope:
      - 数据中心
      - 高低压配电室
      - UPS机房
      - 发电机控制室

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: FIRE-GAS_BND_IN_FA
        boundary_name: 火灾报警信号
        medium: SIGNAL-FA
        source_system: FIRE-ALARM
      
    outputs:
      - boundary_id: FIRE-GAS_BND_OUT_AGENT
        boundary_name: 灭火剂释放
        medium: GAS-FIRE
        target: 被保护区域

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:

    source_nodes:
  
      - node_id: FIRE-GAS_SRC_CYLINDER
        node_name: 灭火剂钢瓶组
        node_name_en: Agent Cylinder Bank
        node_type: Source_Node
        node_category: SRC
      
        function: 储存灭火剂
        medium_out: GAS-FIRE
      
        multiplicity: multiple
        instance_pattern: FIRE-GAS_SRC_CYLINDER_{Zone}
      
        equipment_parameters:
          agent: 七氟丙烷/IG541
          cylinder_volume: {value: 70-180, unit: L}
          pressure: {value: 2.5-4.2, unit: MPa, note: 七氟丙烷}
          quantity: 根据保护区计算
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 钢瓶间
          position: 被保护区域附近
        
        installation_requirements:
          - 防火分隔
          - 通风
          - 温度控制（0-50℃）
          - 压力监测
          - 明显标识
        
        control_points:
          sensors:
            - {point_id: CYL_P, type: AI, description: 钢瓶压力}
            - {point_id: CYL_WEIGHT, type: AI, description: 钢瓶重量}
          status:
            - {point_id: CYL_LOW_P, type: DI, description: 压力低报警}
            - {point_id: CYL_LEAK, type: DI, description: 泄漏报警}

    distribution_nodes:
  
      - node_id: FIRE-GAS_DST_SELECTOR
        node_name: 选择阀
        node_name_en: Selector Valve
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 选择灭火区域
        medium_in: GAS-FIRE
        medium_out: GAS-FIRE
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 电磁选择阀
          size: {value: DN50-DN80, unit: mm}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 钢瓶间
        
        control_points:
          status:
            - {point_id: SEL_OPEN, type: DI, description: 开启状态}
          commands:
            - {point_id: SEL_CMD, type: DO, description: 开启命令}

      - node_id: FIRE-GAS_DST_PIPE
        node_name: 灭火剂管道
        node_name_en: Agent Pipe
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
      
        function: 灭火剂输送
        medium_in: GAS-FIRE
        medium_out: GAS-FIRE
      
        equipment_parameters:
          material: 无缝钢管
          diameter: {value: DN25-DN80, unit: mm}
        
        location_hint:
          space_type: CEILING_VOID
          position: 被保护区域上方

      - node_id: FIRE-GAS_DST_CONTROL
        node_name: 气体灭火控制器
        node_name_en: Gas Suppression Controller
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 系统控制、联动
        medium_in: SIGNAL-FA
        medium_out: CTRL
      
        equipment_parameters:
          functions:
            - 火灾探测确认
            - 声光报警
            - 延时启动
            - 紧急启动/停止
            - 设备联动
          
        location_hint:
          space_type: WALL
          position: 被保护区域入口
        
        control_points:
          status:
            - {point_id: GAS_FIRE, type: DI, description: 火灾确认}
            - {point_id: GAS_RELEASE, type: DI, description: 释放信号}
            - {point_id: GAS_FAULT, type: DI, description: 系统故障}
          commands:
            - {point_id: GAS_MANUAL, type: DO, description: 手动启动}
            - {point_id: GAS_ABORT, type: DO, description: 紧急停止}

    sink_nodes:
  
      - node_id: FIRE-GAS_SNK_NOZZLE
        node_name: 喷嘴
        node_name_en: Discharge Nozzle
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 灭火剂释放
        medium_in: GAS-FIRE
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 全淹没喷嘴
          coverage: 根据保护区计算
        
        location_hint:
          space_type: CEILING
          position: 被保护区域吊顶
        
      - node_id: FIRE-GAS_SNK_ZONE
        node_name: 被保护区域
        node_name_en: Protected Zone
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 灭火保护
        medium_in: GAS-FIRE
      
        multiplicity: multiple
        instance_pattern: FIRE-GAS_SNK_ZONE_{ZoneName}
      
        typical_zones:
          - 数据中心机房
          - 高压配电室
          - 低压配电室
          - UPS机房

  # ============================================================
  # 边定义
  # ============================================================
  edges:

    supply_edges:
  
      - edge_id: FIRE-GAS_EDGE_001
        edge_name: 钢瓶至选择阀
        edge_type: TRK
        from_node: FIRE-GAS_SRC_CYLINDER
        to_node: FIRE-GAS_DST_SELECTOR
        direction: unidirectional
        medium: GAS-FIRE
      
      - edge_id: FIRE-GAS_EDGE_002
        edge_name: 选择阀至管道
        edge_type: TRK
        from_node: FIRE-GAS_DST_SELECTOR
        to_node: FIRE-GAS_DST_PIPE
        direction: unidirectional
        medium: GAS-FIRE
      
      - edge_id: FIRE-GAS_EDGE_003
        edge_name: 管道至喷嘴
        edge_type: TRM
        from_node: FIRE-GAS_DST_PIPE
        to_node: FIRE-GAS_SNK_NOZZLE
        direction: unidirectional
        medium: GAS-FIRE

    control_edges:
  
      - edge_id: FIRE-GAS_EDGE_FA
        edge_name: 火灾报警联动
        edge_type: CTRL
        from_node: FIRE-ALARM_DST_LINKAGE
        to_node: FIRE-GAS_DST_CONTROL
        direction: unidirectional
        medium: SIGNAL-FA
        cross_system: true
        source_system: FIRE-ALARM

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:

    - path_id: FIRE-GAS_PATH_MAIN
      path_name: 气体灭火释放路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: FIRE-GAS_SRC_CYLINDER}
        - {step: 2, element_type: edge, element_id: FIRE-GAS_EDGE_001}
        - {step: 3, element_type: node, element_id: FIRE-GAS_DST_SELECTOR}
        - {step: 4, element_type: edge, element_id: FIRE-GAS_EDGE_002}
        - {step: 5, element_type: node, element_id: FIRE-GAS_DST_PIPE}
        - {step: 6, element_type: edge, element_id: FIRE-GAS_EDGE_003}
        - {step: 7, element_type: node, element_id: FIRE-GAS_SNK_NOZZLE}

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:

    release_sequence:
      trigger: 同一防护区两个独立探测器报警
    
      actions:
        - step: 1
          action: 火灾确认
        
        - step: 2
          action: 声光报警启动
        
        - step: 3
          action: 关闭空调、通风
        
        - step: 4
          action: 关闭防护区门窗
        
        - step: 5
          action: 延时计时开始
          delay: {value: 30, unit: s}
          purpose: 人员疏散
        
        - step: 6
          action: 开启选择阀
        
        - step: 7
          action: 释放灭火剂
          duration: {value: "≤10", unit: s}
        
        - step: 8
          action: 维持灭火剂浓度
          duration: {value: "≥10", unit: min}
        
    abort_function:
      trigger: 紧急停止按钮
      action: 中断释放程序
      timing: 仅在延时期间有效
    
    manual_release:
      mode: 机械应急启动
      location: 钢瓶间门口
    
    post_release:
      actions:
        - 通风换气（人工启动）
        - 系统复位
        - 钢瓶更换/充装
```

---

## Batch 4 输出总结

```yaml
Batch_4_Summary:

  completed_systems:
    - system_id: HVAC-HWP
      nodes: 12
      edges: 12
      paths: 1
      loops: 1
    
    - system_id: HVAC-SMOKE
      nodes: 12
      edges: 11
      paths: 2
    
    - system_id: PLUMB-HWS
      nodes: 12
      edges: 10
      paths: 1
      loops: 1
    
    - system_id: ELEC-UPS
      nodes: 9
      edges: 5
      paths: 2
    
    - system_id: MGAS-AGSS
      nodes: 8
      edges: 7
      paths: 1
    
    - system_id: PLUMB-MED-WASTE
      nodes: 9
      edges: 8
      paths: 1
    
    - system_id: FIRE-GAS
      nodes: 7
      edges: 4
      paths: 1

  total_batch_4:
    systems: 7
    nodes: 69
    edges: 57
  
  grand_total_all_batches:
    batches: 4
    systems: 26
    estimated_nodes: 280+
    estimated_edges: 240+
```

---
