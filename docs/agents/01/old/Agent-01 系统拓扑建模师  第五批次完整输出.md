# Agent-01 Batch 5 完整输出

## Batch 5 系统清单

```yaml
Batch_5_Systems:

  category: P2-IMPORTANT 优先级系统

  systems:
    - HVAC-FCU: 风机盘管系统
    - HVAC-NEG: 负压隔离系统
    - HVAC-PAU: 新风机组系统
    - INT-SEC: 安全防范系统
    - INT-NET: 综合布线系统
    - INT-IT: 信息网络系统
    - INT-PA: 公共广播系统
```

---

## 5.1 HVAC-FCU 风机盘管系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: HVAC-FCU
    system_name: 风机盘管系统
    system_name_en: Fan Coil Unit System
    category: HVAC
    version: 1.0
  
    description: |
      医院风机盘管空调系统，为病房、门诊、办公等区域提供末端空调。
      采用两管制或四管制系统，配合新风系统使用。
    
    design_basis:
      pipe_system: 四管制（医院推荐）/ 两管制
      water_temp:
        cooling: {supply: 7, return: 12, unit: ℃}
        heating: {supply: 50, return: 40, unit: ℃}
      control: 室内温控器独立控制
    
    serving_scope:
      - 普通病房
      - 门诊诊室
      - 医技用房
      - 办公用房
      - 公共走廊

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: HVAC-FCU_BND_IN_CHW
        boundary_name: 冷冻水供水
        medium: WATER-CHW
        source_system: HVAC-CHP
        parameters:
          temperature: {value: 7, unit: ℃}
        
      - boundary_id: HVAC-FCU_BND_IN_HW
        boundary_name: 热水供水
        medium: WATER-HW
        source_system: HVAC-HWP
        parameters:
          temperature: {value: 50, unit: ℃}
        
      - boundary_id: HVAC-FCU_BND_IN_FA
        boundary_name: 新风
        medium: AIR-OA
        source_system: HVAC-PAU
        note: 新风由独立新风系统提供
      
      - boundary_id: HVAC-FCU_BND_IN_ELEC
        boundary_name: 电源
        medium: ELEC-LV
        source_system: ELEC-LV-MAIN
      
    outputs:
      - boundary_id: HVAC-FCU_BND_OUT_AIR
        boundary_name: 送风
        medium: AIR-SA
        target: 室内空间
      
      - boundary_id: HVAC-FCU_BND_OUT_CHW
        boundary_name: 冷冻水回水
        medium: WATER-CHW
        target_system: HVAC-CHP
      
      - boundary_id: HVAC-FCU_BND_OUT_HW
        boundary_name: 热水回水
        medium: WATER-HW
        target_system: HVAC-HWP

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:

    source_nodes:
  
      - node_id: HVAC-FCU_SRC_CHW
        node_name: 冷冻水接口
        node_name_en: Chilled Water Interface
        node_type: Source_Node
        node_category: SRC
      
        function: 冷冻水系统接入
        medium_out: WATER-CHW
      
        source_system: HVAC-CHP
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房

      - node_id: HVAC-FCU_SRC_HW
        node_name: 热水接口
        node_name_en: Hot Water Interface
        node_type: Source_Node
        node_category: SRC
      
        function: 热水系统接入
        medium_out: WATER-HW
      
        source_system: HVAC-HWP
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 锅炉房

      - node_id: HVAC-FCU_SRC_RA
        node_name: 室内回风
        node_name_en: Room Return Air
        node_type: Source_Node
        node_category: SRC
      
        function: 室内空气回风
        medium_out: AIR-RA
      
        location_hint:
          space_type: ROOM
          position: 室内下部/侧回风

    distribution_nodes:
  
      - node_id: HVAC-FCU_DST_CHW_RISER
        node_name: 冷冻水立管
        node_name_en: Chilled Water Riser
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
      
        function: 冷冻水垂直分配
        medium_in: WATER-CHW
        medium_out: WATER-CHW
      
        multiplicity: multiple
        instance_pattern: HVAC-FCU_DST_CHW_RISER_{Zone}_{Seq}
      
        equipment_parameters:
          material: 镀锌钢管/无缝钢管
          diameter_supply: {value: DN80-DN100, unit: mm}
          diameter_return: {value: DN80-DN100, unit: mm}
          insulation: 橡塑保温+防潮层
        
        location_hint:
          space_type: SHAFT
          shaft_type: 空调水管井

      - node_id: HVAC-FCU_DST_HW_RISER
        node_name: 热水立管
        node_name_en: Hot Water Riser
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
      
        function: 热水垂直分配
        medium_in: WATER-HW
        medium_out: WATER-HW
      
        multiplicity: multiple
      
        equipment_parameters:
          material: 镀锌钢管/无缝钢管
          diameter_supply: {value: DN50-DN80, unit: mm}
          diameter_return: {value: DN50-DN80, unit: mm}
          insulation: 橡塑保温
        
        location_hint:
          space_type: SHAFT
          shaft_type: 空调水管井

      - node_id: HVAC-FCU_DST_FLOOR_HEADER
        node_name: 楼层分集水器
        node_name_en: Floor Header
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 楼层水平分配
        medium_in: [WATER-CHW, WATER-HW]
        medium_out: [WATER-CHW, WATER-HW]
      
        multiplicity: multiple
        instance_pattern: HVAC-FCU_DST_FLOOR_HEADER_{Floor}
      
        equipment_parameters:
          type: 分集水器
          material: 镀锌钢管
          branches: 8-12路
          valves: 每路阀门
        
        location_hint:
          space_type: SHAFT / CEILING_VOID
          position: 楼层管井或吊顶
        
        control_points:
          sensors:
            - {point_id: HEADER_T_CHW, type: AI, description: 冷水温度}
            - {point_id: HEADER_T_HW, type: AI, description: 热水温度}

      - node_id: HVAC-FCU_DST_BRANCH
        node_name: FCU支管
        node_name_en: FCU Branch Pipe
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BRH
      
        function: 至各FCU末端
        medium_in: [WATER-CHW, WATER-HW]
        medium_out: [WATER-CHW, WATER-HW]
      
        multiplicity: multiple
      
        equipment_parameters:
          material: 镀锌钢管/PPR管
          diameter: {value: DN20-DN32, unit: mm}
        
        location_hint:
          space_type: CEILING_VOID
          position: 走廊/房间吊顶内

      - node_id: HVAC-FCU_DST_VALVE_SET
        node_name: FCU阀组
        node_name_en: FCU Valve Assembly
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: FCU前端阀门控制
        medium_in: [WATER-CHW, WATER-HW]
        medium_out: [WATER-CHW, WATER-HW]
      
        multiplicity: multiple
      
        equipment_parameters:
          components:
            - 截止阀（检修用）
            - 过滤器
            - 电动两通阀
            - 平衡阀（可选）
          control_valve: 电动两通阀（温控器控制）
        
        location_hint:
          space_type: CEILING_VOID
          position: FCU旁

      - node_id: HVAC-FCU_DST_UNIT
        node_name: 风机盘管机组
        node_name_en: Fan Coil Unit
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
      
        function: 空气处理末端
        medium_in: [WATER-CHW, WATER-HW, AIR-RA]
        medium_out: AIR-SA
      
        multiplicity: multiple
        instance_pattern: HVAC-FCU_DST_UNIT_{Floor}_{Room}
      
        equipment_parameters:
          type: 卧式暗装/立式明装/卡式
          capacity: {value: 3.5-14, unit: kW}
          air_flow: {value: 340-2380, unit: m³/h}
          coil: 四管制（冷热盘管分离）
          fan: 三速风机
          filter: 初效过滤器
        
        location_hint:
          space_type: CEILING_VOID / WALL
          position: 房间吊顶内/窗台下
        
        control_points:
          sensors:
            - {point_id: FCU_T_RA, type: AI, description: 回风温度}
          status:
            - {point_id: FCU_FAN_RUN, type: DI, description: 风机状态}
            - {point_id: FCU_FAN_SPEED, type: DI, description: 风速档位}
          commands:
            - {point_id: FCU_VALVE_CHW, type: DO, description: 冷水阀开关}
            - {point_id: FCU_VALVE_HW, type: DO, description: 热水阀开关}
            - {point_id: FCU_FAN_CMD, type: DO, description: 风机启停}

      - node_id: HVAC-FCU_DST_THERMOSTAT
        node_name: 室内温控器
        node_name_en: Room Thermostat
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 室内温度控制
        medium_in: SIGNAL
        medium_out: CTRL
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 液晶温控器
          functions:
            - 温度设定
            - 风速选择
            - 模式选择（制冷/制热）
            - 开关控制
          setpoint_range: {value: "16-30", unit: ℃}
        
        location_hint:
          space_type: WALL
          position: 房间门口内侧
          height: {value: 1.2-1.5, unit: m}
        
        control_points:
          sensors:
            - {point_id: RM_T, type: AI, description: 室内温度}
            - {point_id: RM_T_SP, type: AI, description: 设定温度}
          status:
            - {point_id: RM_MODE, type: DI, description: 运行模式}

    sink_nodes:
  
      - node_id: HVAC-FCU_SNK_ROOM
        node_name: 空调房间
        node_name_en: Conditioned Room
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 空调送风
        medium_in: AIR-SA
      
        multiplicity: multiple
      
        typical_rooms:
          - 病房
          - 诊室
          - 办公室
          - 护士站
        
        location_hint:
          space_type: ROOM

      - node_id: HVAC-FCU_SNK_CHW_RET
        node_name: 冷冻水回水
        node_name_en: Chilled Water Return
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 冷冻水回水
        medium_in: WATER-CHW
      
        target_system: HVAC-CHP

      - node_id: HVAC-FCU_SNK_HW_RET
        node_name: 热水回水
        node_name_en: Hot Water Return
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 热水回水
        medium_in: WATER-HW
      
        target_system: HVAC-HWP

  # ============================================================
  # 边定义
  # ============================================================
  edges:

    chilled_water_edges:
  
      - edge_id: HVAC-FCU_EDGE_CHW_001
        edge_name: 冷冻水至立管
        edge_type: TRK
        from_node: HVAC-FCU_SRC_CHW
        to_node: HVAC-FCU_DST_CHW_RISER
        direction: unidirectional
        medium: WATER-CHW
      
      - edge_id: HVAC-FCU_EDGE_CHW_002
        edge_name: 立管至楼层分集水器
        edge_type: BRH
        from_node: HVAC-FCU_DST_CHW_RISER
        to_node: HVAC-FCU_DST_FLOOR_HEADER
        direction: unidirectional
        medium: WATER-CHW
      
      - edge_id: HVAC-FCU_EDGE_CHW_003
        edge_name: 分集水器至支管
        edge_type: BRH
        from_node: HVAC-FCU_DST_FLOOR_HEADER
        to_node: HVAC-FCU_DST_BRANCH
        direction: unidirectional
        medium: WATER-CHW
      
      - edge_id: HVAC-FCU_EDGE_CHW_004
        edge_name: 支管至阀组
        edge_type: TRK
        from_node: HVAC-FCU_DST_BRANCH
        to_node: HVAC-FCU_DST_VALVE_SET
        direction: unidirectional
        medium: WATER-CHW
      
      - edge_id: HVAC-FCU_EDGE_CHW_005
        edge_name: 阀组至FCU
        edge_type: TRM
        from_node: HVAC-FCU_DST_VALVE_SET
        to_node: HVAC-FCU_DST_UNIT
        direction: unidirectional
        medium: WATER-CHW

    hot_water_edges:
  
      - edge_id: HVAC-FCU_EDGE_HW_001
        edge_name: 热水至立管
        edge_type: TRK
        from_node: HVAC-FCU_SRC_HW
        to_node: HVAC-FCU_DST_HW_RISER
        direction: unidirectional
        medium: WATER-HW
      
      - edge_id: HVAC-FCU_EDGE_HW_002
        edge_name: 热水立管至分集水器
        edge_type: BRH
        from_node: HVAC-FCU_DST_HW_RISER
        to_node: HVAC-FCU_DST_FLOOR_HEADER
        direction: unidirectional
        medium: WATER-HW
      
      - edge_id: HVAC-FCU_EDGE_HW_005
        edge_name: 热水阀组至FCU
        edge_type: TRM
        from_node: HVAC-FCU_DST_VALVE_SET
        to_node: HVAC-FCU_DST_UNIT
        direction: unidirectional
        medium: WATER-HW

    air_edges:
  
      - edge_id: HVAC-FCU_EDGE_AIR_001
        edge_name: 回风至FCU
        edge_type: TRM
        from_node: HVAC-FCU_SRC_RA
        to_node: HVAC-FCU_DST_UNIT
        direction: unidirectional
        medium: AIR-RA
      
      - edge_id: HVAC-FCU_EDGE_AIR_002
        edge_name: FCU送风至房间
        edge_type: TRM
        from_node: HVAC-FCU_DST_UNIT
        to_node: HVAC-FCU_SNK_ROOM
        direction: unidirectional
        medium: AIR-SA

    return_water_edges:
  
      - edge_id: HVAC-FCU_EDGE_CHW_RET
        edge_name: 冷冻水回水
        edge_type: TRK
        from_node: HVAC-FCU_DST_UNIT
        to_node: HVAC-FCU_SNK_CHW_RET
        direction: unidirectional
        medium: WATER-CHW
      
      - edge_id: HVAC-FCU_EDGE_HW_RET
        edge_name: 热水回水
        edge_type: TRK
        from_node: HVAC-FCU_DST_UNIT
        to_node: HVAC-FCU_SNK_HW_RET
        direction: unidirectional
        medium: WATER-HW

    control_edges:
  
      - edge_id: HVAC-FCU_EDGE_CTRL
        edge_name: 温控器至阀组
        edge_type: CTRL
        from_node: HVAC-FCU_DST_THERMOSTAT
        to_node: HVAC-FCU_DST_VALVE_SET
        direction: unidirectional
        medium: SIGNAL

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:

    - path_id: HVAC-FCU_PATH_COOLING
      path_name: 制冷水路径
      path_type: SUP
      mode: 制冷工况
      sequence:
        - {step: 1, element_type: node, element_id: HVAC-FCU_SRC_CHW}
        - {step: 2, element_type: node, element_id: HVAC-FCU_DST_CHW_RISER}
        - {step: 3, element_type: node, element_id: HVAC-FCU_DST_FLOOR_HEADER}
        - {step: 4, element_type: node, element_id: HVAC-FCU_DST_BRANCH}
        - {step: 5, element_type: node, element_id: HVAC-FCU_DST_VALVE_SET}
        - {step: 6, element_type: node, element_id: HVAC-FCU_DST_UNIT}
        - {step: 7, element_type: node, element_id: HVAC-FCU_SNK_ROOM}
      
    - path_id: HVAC-FCU_PATH_HEATING
      path_name: 供热水路径
      path_type: SUP
      mode: 供热工况
      sequence:
        - {step: 1, element_type: node, element_id: HVAC-FCU_SRC_HW}
        - {step: 2, element_type: node, element_id: HVAC-FCU_DST_HW_RISER}
        - {step: 3, element_type: node, element_id: HVAC-FCU_DST_FLOOR_HEADER}
        - {step: 4, element_type: node, element_id: HVAC-FCU_DST_BRANCH}
        - {step: 5, element_type: node, element_id: HVAC-FCU_DST_VALVE_SET}
        - {step: 6, element_type: node, element_id: HVAC-FCU_DST_UNIT}
        - {step: 7, element_type: node, element_id: HVAC-FCU_SNK_ROOM}

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:

    thermostat_control:
      mode_selection:
        cooling:
          condition: 室温 > 设定值 + 死区
          action: 开启冷水阀
        heating:
          condition: 室温 < 设定值 - 死区
          action: 开启热水阀
        dead_band: {value: 1, unit: ℃}
      
    fan_speed_control:
      mode: 手动三速 / 自动变速
      speeds: [高速, 中速, 低速]
      auto_logic: 根据温差自动调速
    
    valve_control:
      type: 开关控制 / 比例控制
      on_off: 温控器触点控制
      proportional: 0-10V模拟量控制
    
    centralized_override:
      description: BA系统集中控制
      functions:
        - 远程启停
        - 设定值限制
        - 时间表控制
        - 夜间节能模式
```

---

## 5.2 HVAC-NEG 负压隔离系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: HVAC-NEG
    system_name: 负压隔离系统
    system_name_en: Negative Pressure Isolation System
    category: HVAC
    version: 1.0
  
    description: |
      医院负压隔离病房空调系统，用于传染病、呼吸道疾病等
      需要隔离的患者区域。通过维持负压防止病原体外溢。
    
    design_basis:
      pressure_gradient:
        - {area: 污染区, pressure: -30, unit: Pa, ref: 清洁走廊}
        - {area: 半污染区, pressure: -15, unit: Pa}
        - {area: 清洁区, pressure: 0, unit: Pa}
      air_changes: {value: 12-15, unit: ACH}
      exhaust: 100%排风，无回风
      filtration: 排风HEPA过滤
    
    serving_scope:
      - 发热门诊
      - 传染病病房
      - 隔离ICU
      - 负压手术室

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: HVAC-NEG_BND_IN_OA
        boundary_name: 室外新风
        medium: AIR-OA
        is_external: true
      
      - boundary_id: HVAC-NEG_BND_IN_CHW
        boundary_name: 冷冻水
        medium: WATER-CHW
        source_system: HVAC-CHP
      
      - boundary_id: HVAC-NEG_BND_IN_HW
        boundary_name: 热水
        medium: WATER-HW
        source_system: HVAC-HWP
      
      - boundary_id: HVAC-NEG_BND_IN_ELEC
        boundary_name: 电源
        medium: ELEC-LV
        source_system: ELEC-LV-CRITICAL
        note: 关键负荷，双电源供电
      
    outputs:
      - boundary_id: HVAC-NEG_BND_OUT_EA
        boundary_name: 排风
        medium: AIR-EA
        is_external: true
        target: 大气（高空排放）

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:

    source_nodes:
  
      - node_id: HVAC-NEG_SRC_OA
        node_name: 新风入口
        node_name_en: Outdoor Air Intake
        node_type: Source_Node
        node_category: SRC
      
        function: 室外新风引入
        medium_out: AIR-OA
        is_external: true
      
        equipment_parameters:
          type: 防雨百叶
          screen: 防虫网
        
        location_hint:
          space_type: EXTERIOR
          position: 清洁区屋顶/外墙
          requirement: 远离排风口≥20m

    distribution_nodes:
  
      - node_id: HVAC-NEG_DST_AHU
        node_name: 负压区空调机组
        node_name_en: Negative Pressure AHU
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
      
        function: 新风处理
        medium_in: [AIR-OA, WATER-CHW, WATER-HW]
        medium_out: AIR-SA
      
        equipment_parameters:
          type: 全新风空调机组
          components:
            - 初效过滤器(G4)
            - 中效过滤器(F7)
            - 表冷器
            - 加热器
            - 加湿器
            - 高效过滤器(H13)
            - 送风机
          air_flow: {value: 5000-15000, unit: m³/h}
          total_pressure: {value: 800-1200, unit: Pa}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 空调机房
          position: 独立机房或楼顶
        
        installation_requirements:
          - 全新风运行
          - 无回风
          - 独立排水
          - 便于消毒
        
        control_points:
          sensors:
            - {point_id: AHU_T_SA, type: AI, description: 送风温度}
            - {point_id: AHU_H_SA, type: AI, description: 送风湿度}
            - {point_id: AHU_DP_FILTER, type: AI, description: 过滤器压差}
          status:
            - {point_id: AHU_FAN_RUN, type: DI, description: 风机状态}
            - {point_id: AHU_FILTER_ALARM, type: DI, description: 过滤器报警}
          commands:
            - {point_id: AHU_START, type: DO, description: 启停控制}

      - node_id: HVAC-NEG_DST_SA_MAIN
        node_name: 送风主管
        node_name_en: Supply Air Main Duct
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
      
        function: 送风主干输送
        medium_in: AIR-SA
        medium_out: AIR-SA
      
        equipment_parameters:
          material: 镀锌钢板风管
          insulation: 内保温
        
        location_hint:
          space_type: CEILING_VOID
          position: 清洁走廊吊顶

      - node_id: HVAC-NEG_DST_SA_HEPA
        node_name: 送风HEPA
        node_name_en: Supply Air HEPA Unit
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
      
        function: 送风末端高效过滤
        medium_in: AIR-SA
        medium_out: AIR-SA
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 高效送风口
          filter: H13/H14
          efficiency: {value: "≥99.97", unit: "%", note: "@0.3μm"}
        
        location_hint:
          space_type: CEILING
          position: 病房天花板
        
        control_points:
          sensors:
            - {point_id: HEPA_DP, type: AI, description: 压差}
          status:
            - {point_id: HEPA_ALARM, type: DI, description: 堵塞报警}

      - node_id: HVAC-NEG_DST_ROOM
        node_name: 负压隔离病房
        node_name_en: Negative Pressure Isolation Room
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRM
      
        function: 隔离病房空间
        medium_in: AIR-SA
        medium_out: AIR-RA
      
        multiplicity: multiple
        instance_pattern: HVAC-NEG_DST_ROOM_{Floor}_{Seq}
      
        equipment_parameters:
          pressure: {value: -30, unit: Pa, ref: 走廊}
          air_changes: {value: 12-15, unit: ACH}
          airlock: 设置缓冲间
        
        location_hint:
          space_type: ROOM
          room_type: 负压隔离病房
        
        control_points:
          sensors:
            - {point_id: ROOM_P, type: AI, description: 房间压力}
            - {point_id: ROOM_T, type: AI, description: 房间温度}
            - {point_id: ROOM_H, type: AI, description: 房间湿度}
          status:
            - {point_id: ROOM_P_ALARM, type: DI, description: 压力异常报警}

      - node_id: HVAC-NEG_DST_EA_HEPA
        node_name: 排风HEPA
        node_name_en: Exhaust Air HEPA Unit
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
      
        function: 排风高效过滤
        medium_in: AIR-RA
        medium_out: AIR-EA
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 排风高效过滤箱
          filter: H13/H14
          features:
            - 袋进袋出更换
            - 原位消毒接口
            - 压差监测
          
        location_hint:
          space_type: CEILING_VOID / EXTERIOR
          position: 排风管道上
        
        installation_requirements:
          - 便于安全更换
          - 消毒灭菌接口
          - 压差监测
        
        control_points:
          sensors:
            - {point_id: EA_HEPA_DP, type: AI, description: 压差}
          status:
            - {point_id: EA_HEPA_ALARM, type: DI, description: 堵塞报警}

      - node_id: HVAC-NEG_DST_EA_FAN
        node_name: 排风机
        node_name_en: Exhaust Fan
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 排风抽吸、维持负压
        medium_in: AIR-EA
        medium_out: AIR-EA
      
        equipment_parameters:
          type: 离心风机（变频）
          air_flow: {value: 6000-18000, unit: m³/h}
          total_pressure: {value: 600-1000, unit: Pa}
          power: {value: 7.5-22, unit: kW}
          control: 变频调速
          redundancy: 一用一备
        
        location_hint:
          space_type: MEP_ROOM / OUTDOOR
          position: 屋顶排风机房
        
        installation_requirements:
          - 独立排风机房
          - 负压保护
          - 应急发电机供电
        
        control_points:
          sensors:
            - {point_id: EA_FAN_FREQ, type: AI, description: 运行频率}
            - {point_id: EA_FAN_DP, type: AI, description: 风机压差}
          status:
            - {point_id: EA_FAN_RUN, type: DI, description: 运行状态}
            - {point_id: EA_FAN_FAULT, type: DI, description: 故障报警}
          commands:
            - {point_id: EA_FAN_START, type: DO, description: 启停控制}
            - {point_id: EA_FAN_FREQ_SP, type: AO, description: 频率设定}

      - node_id: HVAC-NEG_DST_PRESSURE_CTRL
        node_name: 压力控制器
        node_name_en: Pressure Controller
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 负压自动控制
        medium_in: SIGNAL
        medium_out: CTRL
      
        equipment_parameters:
          type: 压差控制器
          control_method: PID
          setpoint: {value: -30, unit: Pa}
        
        location_hint:
          space_type: WALL
          position: 病房入口

    sink_nodes:
  
      - node_id: HVAC-NEG_SNK_EXHAUST
        node_name: 排风出口
        node_name_en: Exhaust Air Outlet
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 污染空气排放
        medium_in: AIR-EA
        is_external: true
      
        equipment_parameters:
          type: 高空排放
          height: {value: "≥3", unit: m, note: 高于屋面}
        
        location_hint:
          space_type: EXTERIOR
          position: 屋顶高空
          requirement: 远离新风口、人员活动区≥20m

  # ============================================================
  # 边定义
  # ============================================================
  edges:

    supply_edges:
  
      - edge_id: HVAC-NEG_EDGE_SA_001
        edge_name: 新风至AHU
        edge_type: TRK
        from_node: HVAC-NEG_SRC_OA
        to_node: HVAC-NEG_DST_AHU
        direction: unidirectional
        medium: AIR-OA
      
      - edge_id: HVAC-NEG_EDGE_SA_002
        edge_name: AHU至送风主管
        edge_type: TRK
        from_node: HVAC-NEG_DST_AHU
        to_node: HVAC-NEG_DST_SA_MAIN
        direction: unidirectional
        medium: AIR-SA
      
      - edge_id: HVAC-NEG_EDGE_SA_003
        edge_name: 送风主管至HEPA
        edge_type: BRH
        from_node: HVAC-NEG_DST_SA_MAIN
        to_node: HVAC-NEG_DST_SA_HEPA
        direction: unidirectional
        medium: AIR-SA
      
      - edge_id: HVAC-NEG_EDGE_SA_004
        edge_name: HEPA至病房
        edge_type: TRM
        from_node: HVAC-NEG_DST_SA_HEPA
        to_node: HVAC-NEG_DST_ROOM
        direction: unidirectional
        medium: AIR-SA

    exhaust_edges:
  
      - edge_id: HVAC-NEG_EDGE_EA_001
        edge_name: 病房至排风HEPA
        edge_type: TRM
        from_node: HVAC-NEG_DST_ROOM
        to_node: HVAC-NEG_DST_EA_HEPA
        direction: unidirectional
        medium: AIR-RA
      
      - edge_id: HVAC-NEG_EDGE_EA_002
        edge_name: HEPA至排风机
        edge_type: TRK
        from_node: HVAC-NEG_DST_EA_HEPA
        to_node: HVAC-NEG_DST_EA_FAN
        direction: unidirectional
        medium: AIR-EA
      
      - edge_id: HVAC-NEG_EDGE_EA_003
        edge_name: 排风机至排放口
        edge_type: TRK
        from_node: HVAC-NEG_DST_EA_FAN
        to_node: HVAC-NEG_SNK_EXHAUST
        direction: unidirectional
        medium: AIR-EA

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:

    - path_id: HVAC-NEG_PATH_SA
      path_name: 送风路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: HVAC-NEG_SRC_OA}
        - {step: 2, element_type: edge, element_id: HVAC-NEG_EDGE_SA_001}
        - {step: 3, element_type: node, element_id: HVAC-NEG_DST_AHU}
        - {step: 4, element_type: edge, element_id: HVAC-NEG_EDGE_SA_002}
        - {step: 5, element_type: node, element_id: HVAC-NEG_DST_SA_MAIN}
        - {step: 6, element_type: edge, element_id: HVAC-NEG_EDGE_SA_003}
        - {step: 7, element_type: node, element_id: HVAC-NEG_DST_SA_HEPA}
        - {step: 8, element_type: edge, element_id: HVAC-NEG_EDGE_SA_004}
        - {step: 9, element_type: node, element_id: HVAC-NEG_DST_ROOM}
      
    - path_id: HVAC-NEG_PATH_EA
      path_name: 排风路径
      path_type: EXH
      sequence:
        - {step: 1, element_type: node, element_id: HVAC-NEG_DST_ROOM}
        - {step: 2, element_type: edge, element_id: HVAC-NEG_EDGE_EA_001}
        - {step: 3, element_type: node, element_id: HVAC-NEG_DST_EA_HEPA}
        - {step: 4, element_type: edge, element_id: HVAC-NEG_EDGE_EA_002}
        - {step: 5, element_type: node, element_id: HVAC-NEG_DST_EA_FAN}
        - {step: 6, element_type: edge, element_id: HVAC-NEG_EDGE_EA_003}
        - {step: 7, element_type: node, element_id: HVAC-NEG_SNK_EXHAUST}

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:

    pressure_control:
      description: 负压自动控制
      method: 送排风量差控制
    
      control_loop:
        sensor: 病房压差传感器
        setpoint: {value: -30, unit: Pa}
        actuator: 排风机变频
      
      logic: |
        排风量 > 送风量 → 形成负压
        通过调节排风机频率维持压差稳定
      
    interlocking:
      startup_sequence:
        - step: 1
          action: 启动送风机
        - step: 2
          delay: {value: 30, unit: s}
          action: 启动排风机
        - step: 3
          action: 压差控制生效
        
      shutdown_sequence:
        - step: 1
          action: 停止排风机
        - step: 2
          delay: {value: 30, unit: s}
          action: 停止送风机
        
      reason: 先送后排、先停排后停送，防止正压污染
    
    alarm_management:
      pressure_high:
        condition: 压差 > -10Pa
        level: 紧急
        action: 声光报警、增加排风
      
      pressure_low:
        condition: 压差 < -50Pa
        level: 告警
        action: 减少排风
      
      fan_failure:
        condition: 送风或排风机故障
        action: 
          - 启动备用风机
          - 紧急报警
          - 考虑疏散患者
        
    filter_management:
      hepa_replacement:
        trigger: 压差超过初始值2倍
        procedure:
          - 消毒HEPA表面
          - 袋进袋出更换
          - 安全处置废旧滤芯
```

---

## 5.3 HVAC-PAU 新风机组系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: HVAC-PAU
    system_name: 新风机组系统
    system_name_en: Primary Air Unit System
    category: HVAC
    version: 1.0
  
    description: |
      医院新风处理系统，为FCU区域提供处理后的新风。
      承担新风负荷和部分湿负荷，与FCU配合使用。
    
    design_basis:
      fresh_air: 按人员新风量或换气次数
      treatment: 过滤、冷却（除湿）、加热、加湿
      supply_mode: 直接送入房间或与FCU回风混合
    
    serving_scope:
      - FCU服务区域
      - 病房区
      - 门诊区
      - 办公区

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: HVAC-PAU_BND_IN_OA
        boundary_name: 室外新风
        medium: AIR-OA
        is_external: true
      
      - boundary_id: HVAC-PAU_BND_IN_CHW
        boundary_name: 冷冻水
        medium: WATER-CHW
        source_system: HVAC-CHP
      
      - boundary_id: HVAC-PAU_BND_IN_HW
        boundary_name: 热水
        medium: WATER-HW
        source_system: HVAC-HWP
      
      - boundary_id: HVAC-PAU_BND_IN_ELEC
        boundary_name: 电源
        medium: ELEC-LV
        source_system: ELEC-LV-MAIN
      
    outputs:
      - boundary_id: HVAC-PAU_BND_OUT_SA
        boundary_name: 新风送风
        medium: AIR-SA
        target: 室内空间/FCU区域

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:

    source_nodes:
  
      - node_id: HVAC-PAU_SRC_OA
        node_name: 新风入口
        node_name_en: Outdoor Air Intake
        node_type: Source_Node
        node_category: SRC
      
        function: 室外新风引入
        medium_out: AIR-OA
        is_external: true
      
        equipment_parameters:
          type: 防雨百叶+电动风阀
        
        location_hint:
          space_type: EXTERIOR
          position: 外墙/屋顶
          height: {value: "≥2", unit: m}

    distribution_nodes:
  
      - node_id: HVAC-PAU_DST_UNIT
        node_name: 新风机组
        node_name_en: Primary Air Unit
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
      
        function: 新风处理
        medium_in: [AIR-OA, WATER-CHW, WATER-HW]
        medium_out: AIR-SA
      
        multiplicity: multiple
        instance_pattern: HVAC-PAU_DST_UNIT_{Zone}_{Seq}
      
        equipment_parameters:
          type: 组合式空调机组（新风处理段）
          components:
            - 新风阀
            - 初效过滤(G4)
            - 中效过滤(F7)
            - 表冷器
            - 再热器（可选）
            - 加湿器
            - 送风机
          air_flow: {value: 5000-20000, unit: m³/h}
          total_pressure: {value: 600-900, unit: Pa}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 新风机房
        
        control_points:
          sensors:
            - {point_id: PAU_T_OA, type: AI, description: 新风温度}
            - {point_id: PAU_T_SA, type: AI, description: 送风温度}
            - {point_id: PAU_H_SA, type: AI, description: 送风湿度}
            - {point_id: PAU_DP_FILTER, type: AI, description: 过滤器压差}
          status:
            - {point_id: PAU_FAN_RUN, type: DI, description: 风机状态}
          commands:
            - {point_id: PAU_START, type: DO, description: 启停控制}
            - {point_id: PAU_CC_VALVE, type: AO, description: 冷水阀开度}
            - {point_id: PAU_HC_VALVE, type: AO, description: 热水阀开度}

      - node_id: HVAC-PAU_DST_SA_MAIN
        node_name: 新风主管
        node_name_en: Primary Air Main Duct
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
      
        function: 新风水平输送
        medium_in: AIR-SA
        medium_out: AIR-SA
      
        equipment_parameters:
          material: 镀锌钢板风管
          insulation: 外保温
        
        location_hint:
          space_type: CEILING_VOID
          position: 走廊吊顶

      - node_id: HVAC-PAU_DST_SA_RISER
        node_name: 新风立管
        node_name_en: Primary Air Riser
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
      
        function: 新风垂直输送
        medium_in: AIR-SA
        medium_out: AIR-SA
      
        multiplicity: multiple
      
        equipment_parameters:
          material: 镀锌钢板风管
          insulation: 外保温
        
        location_hint:
          space_type: SHAFT
          shaft_type: 新风井

      - node_id: HVAC-PAU_DST_SA_BRANCH
        node_name: 新风支管
        node_name_en: Primary Air Branch
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BRH
      
        function: 新风分配至各房间
        medium_in: AIR-SA
        medium_out: AIR-SA
      
        multiplicity: multiple
      
        equipment_parameters:
          material: 镀锌钢板/复合风管
        
        location_hint:
          space_type: CEILING_VOID

      - node_id: HVAC-PAU_DST_DIFFUSER
        node_name: 新风口
        node_name_en: Primary Air Diffuser
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRM
      
        function: 新风送入房间
        medium_in: AIR-SA
        medium_out: AIR-SA
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 条缝风口/散流器
        
        location_hint:
          space_type: CEILING
          position: 房间天花板

    sink_nodes:
  
      - node_id: HVAC-PAU_SNK_ROOM
        node_name: 新风服务区域
        node_name_en: Primary Air Served Zone
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 新风供应
        medium_in: AIR-SA
      
        multiplicity: multiple
      
        location_hint:
          space_type: ROOM

  # ============================================================
  # 边定义
  # ============================================================
  edges:

    supply_edges:
  
      - edge_id: HVAC-PAU_EDGE_001
        edge_name: 新风入口至机组
        edge_type: TRK
        from_node: HVAC-PAU_SRC_OA
        to_node: HVAC-PAU_DST_UNIT
        direction: unidirectional
        medium: AIR-OA
      
      - edge_id: HVAC-PAU_EDGE_002
        edge_name: 机组至新风主管
        edge_type: TRK
        from_node: HVAC-PAU_DST_UNIT
        to_node: HVAC-PAU_DST_SA_MAIN
        direction: unidirectional
        medium: AIR-SA
      
      - edge_id: HVAC-PAU_EDGE_003
        edge_name: 新风主管至立管
        edge_type: BRH
        from_node: HVAC-PAU_DST_SA_MAIN
        to_node: HVAC-PAU_DST_SA_RISER
        direction: unidirectional
        medium: AIR-SA
      
      - edge_id: HVAC-PAU_EDGE_004
        edge_name: 新风立管至支管
        edge_type: BRH
        from_node: HVAC-PAU_DST_SA_RISER
        to_node: HVAC-PAU_DST_SA_BRANCH
        direction: unidirectional
        medium: AIR-SA
      
      - edge_id: HVAC-PAU_EDGE_005
        edge_name: 新风支管至风口
        edge_type: TRM
        from_node: HVAC-PAU_DST_SA_BRANCH
        to_node: HVAC-PAU_DST_DIFFUSER
        direction: unidirectional
        medium: AIR-SA
      
      - edge_id: HVAC-PAU_EDGE_006
        edge_name: 风口至房间
        edge_type: TRM
        from_node: HVAC-PAU_DST_DIFFUSER
        to_node: HVAC-PAU_SNK_ROOM
        direction: unidirectional
        medium: AIR-SA

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:

    - path_id: HVAC-PAU_PATH_MAIN
      path_name: 新风供应路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: HVAC-PAU_SRC_OA}
        - {step: 2, element_type: node, element_id: HVAC-PAU_DST_UNIT}
        - {step: 3, element_type: node, element_id: HVAC-PAU_DST_SA_MAIN}
        - {step: 4, element_type: node, element_id: HVAC-PAU_DST_SA_RISER}
        - {step: 5, element_type: node, element_id: HVAC-PAU_DST_SA_BRANCH}
        - {step: 6, element_type: node, element_id: HVAC-PAU_DST_DIFFUSER}
        - {step: 7, element_type: node, element_id: HVAC-PAU_SNK_ROOM}

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:

    supply_temperature_control:
      summer:
        mode: 除湿再热 / 露点控制
        coil_setpoint: {value: 12-14, unit: ℃, note: 露点温度}
        reheat: 根据需要
      
      winter:
        mode: 加热加湿
        supply_temp: {value: 18-22, unit: ℃}
      
      transition:
        mode: 送风温度随室外温度调整
      
    fan_control:
      mode: 定风量 / 变风量
      constant_volume: 风机恒速运行
      variable_volume: 根据CO2浓度调节
    
    coordination_with_fcu:
      description: 新风与FCU配合运行
      requirements:
        - PAU承担新风负荷和部分湿负荷
        - FCU承担室内显热负荷
        - 新风经PAU处理后送入房间
```

---

## 5.4 INT-SEC 安全防范系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: INT-SEC
    system_name: 安全防范系统
    system_name_en: Security System
    category: INTELLIGENT
    version: 1.0
  
    description: |
      医院安全防范系统，包括视频监控、门禁控制、入侵报警、
      访客管理等子系统，实现全院安全监控与管理。
    
    design_basis:
      video_storage: {value: 30, unit: 天}
      resolution: {value: 200万像素, note: 最低要求}
      access_control: 分级管理
      integration: 与火灾报警、护士呼叫联动
    
    serving_scope:
      - 出入口
      - 公共区域
      - 药房/库房
      - 机房
      - 婴儿室
      - 精神科

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: INT-SEC_BND_IN_NET
        boundary_name: 网络接入
        medium: DATA-IP
        source_system: INT-NET
      
      - boundary_id: INT-SEC_BND_IN_ELEC
        boundary_name: 电源
        medium: ELEC-LV
        source_system: ELEC-LV-MAIN
      
      - boundary_id: INT-SEC_BND_IN_FA
        boundary_name: 火灾报警联动
        medium: SIGNAL-FA
        source_system: FIRE-ALARM
      
    outputs:
      - boundary_id: INT-SEC_BND_OUT_IBMS
        boundary_name: 集成平台接口
        medium: DATA-IP
        target_system: INT-IBMS

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:

    source_nodes:
  
      - node_id: INT-SEC_SRC_CAMERA
        node_name: 监控摄像机
        node_name_en: Surveillance Camera
        node_type: Source_Node
        node_category: SRC
      
        function: 视频图像采集
        medium_out: SIGNAL-VIDEO
      
        multiplicity: multiple
        instance_pattern: INT-SEC_SRC_CAMERA_{Location}_{Seq}
      
        equipment_parameters:
          types:
            - {type: 枪型摄像机, application: 走廊、出入口}
            - {type: 半球摄像机, application: 室内}
            - {type: 球型摄像机, application: 大厅、室外}
            - {type: 人脸识别摄像机, application: 主要出入口}
          resolution: {value: "≥200万像素", unit: null}
          features:
            - 宽动态
            - 红外/星光夜视
            - H.265编码
          
        location_hint:
          space_type: CEILING / WALL / POLE
        
        typical_locations:
          - 主要出入口
          - 门诊大厅
          - 住院部大厅
          - 走廊
          - 电梯轿厢
          - 停车场
          - 药房
          - 财务室
          - 婴儿室

      - node_id: INT-SEC_SRC_READER
        node_name: 门禁读卡器
        node_name_en: Access Control Reader
        node_type: Source_Node
        node_category: SRC
      
        function: 身份识别
        medium_out: SIGNAL-SEC
      
        multiplicity: multiple
        instance_pattern: INT-SEC_SRC_READER_{Location}_{Seq}
      
        equipment_parameters:
          types:
            - {type: IC卡读卡器, application: 一般区域}
            - {type: 人脸识别, application: 重要区域}
            - {type: 指纹识别, application: 特殊区域}
            - {type: 密码键盘, application: 辅助验证}
          
        location_hint:
          space_type: WALL
          height: {value: 1.2-1.4, unit: m}
        
        typical_locations:
          - 手术部
          - ICU
          - 药房
          - 财务室
          - 机房
          - 婴儿室
          - 精神科

      - node_id: INT-SEC_SRC_SENSOR
        node_name: 入侵探测器
        node_name_en: Intrusion Detector
        node_type: Source_Node
        node_category: SRC
      
        function: 入侵检测
        medium_out: SIGNAL-SEC
      
        multiplicity: multiple
      
        equipment_parameters:
          types:
            - {type: 红外探测器, application: 室内}
            - {type: 红外对射, application: 周界}
            - {type: 门磁, application: 门窗}
            - {type: 震动探测器, application: 保险柜}
            - {type: 紧急按钮, application: 收费处}
          
        location_hint:
          space_type: WALL / CEILING / DOOR
        
        typical_locations:
          - 药品库
          - 财务室
          - 档案室
          - 周界围墙

      - node_id: INT-SEC_SRC_INTERCOM
        node_name: 可视对讲终端
        node_name_en: Video Intercom Terminal
        node_type: Source_Node
        node_category: SRC
      
        function: 访客可视对讲
        medium_out: SIGNAL-SEC
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 可视对讲门口机
          features:
            - 视频通话
            - 刷卡开门
            - 访客登记
          
        location_hint:
          space_type: WALL
          position: 入口门外

    distribution_nodes:
  
      - node_id: INT-SEC_DST_DOOR_CTRL
        node_name: 门禁控制器
        node_name_en: Door Access Controller
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 门禁点位控制
        medium_in: SIGNAL-SEC
        medium_out: [SIGNAL-SEC, CTRL]
      
        multiplicity: multiple
        instance_pattern: INT-SEC_DST_DOOR_CTRL_{Zone}_{Seq}
      
        equipment_parameters:
          type: 四门/八门控制器
          capacity: {value: 4-8, unit: 门}
          interfaces:
            - 读卡器接口
            - 电锁输出
            - 门磁输入
            - 开门按钮输入
          
        location_hint:
          space_type: WEAK_ROOM / CEILING_VOID
          position: 受控门附近
        
        control_points:
          status:
            - {point_id: DOOR_OPEN, type: DI, description: 开门状态}
            - {point_id: DOOR_ALARM, type: DI, description: 非法开门}
            - {point_id: DOOR_TIMEOUT, type: DI, description: 门超时未关}
          commands:
            - {point_id: DOOR_UNLOCK, type: DO, description: 远程开门}

      - node_id: INT-SEC_DST_ALARM_PANEL
        node_name: 报警主机
        node_name_en: Alarm Panel
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 报警信号处理
        medium_in: SIGNAL-SEC
        medium_out: SIGNAL-SEC
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 总线制报警主机
          zones: {value: 8-64, unit: 防区}
        
        location_hint:
          space_type: WEAK_ROOM
          position: 楼层弱电间

      - node_id: INT-SEC_DST_NVR
        node_name: 网络硬盘录像机
        node_name_en: Network Video Recorder
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BUF
      
        function: 视频录像存储
        medium_in: SIGNAL-VIDEO
        medium_out: DATA-IP
      
        multiplicity: multiple
        instance_pattern: INT-SEC_DST_NVR_{Zone}_{Seq}
      
        equipment_parameters:
          channels: {value: 32-64, unit: 路}
          storage: {value: 48-96, unit: TB}
          redundancy: RAID5/RAID6
          retention: {value: 30, unit: 天}
        
        location_hint:
          space_type: RACK
          room_name: 弱电机房/安防机房
        
        control_points:
          sensors:
            - {point_id: NVR_DISK, type: AI, description: 磁盘使用率}
          status:
            - {point_id: NVR_RECORD, type: DI, description: 录像状态}
            - {point_id: NVR_FAULT, type: DI, description: 故障报警}

      - node_id: INT-SEC_DST_VMS
        node_name: 视频管理平台
        node_name_en: Video Management System
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
      
        function: 视频统一管理
        medium_in: DATA-IP
        medium_out: DATA-IP
      
        equipment_parameters:
          type: 视频综合管理平台
          functions:
            - 实时预览
            - 录像回放
            - 智能分析
            - 电子地图
            - 报警联动
          capacity: {value: 500-2000, unit: 路}
        
        location_hint:
          space_type: RACK
          room_name: 数据中心

      - node_id: INT-SEC_DST_ACS
        node_name: 门禁管理系统
        node_name_en: Access Control System
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
      
        function: 门禁统一管理
        medium_in: DATA-IP
        medium_out: DATA-IP
      
        equipment_parameters:
          type: 门禁管理软件
          functions:
            - 人员管理
            - 权限管理
            - 时间计划
            - 事件记录
            - 考勤统计
          
        location_hint:
          space_type: RACK
          room_name: 数据中心

      - node_id: INT-SEC_DST_ACCESS
        node_name: 门禁联动接口
        node_name_en: Access Control Interface
        node_type: Distribution_Node
        node_category: DST
        node_subtype: JUN
      
        function: 门禁与消防联动
        medium_in: SIGNAL-FA
        medium_out: CTRL
      
        interface_system:


# Agent-01 Batch 5 完整输出（续）

## 5.4 INT-SEC 安全防范系统拓扑（续）

```yaml
      - node_id: INT-SEC_DST_ACCESS
        node_name: 门禁联动接口
        node_name_en: Access Control Interface
        node_type: Distribution_Node
        node_category: DST
        node_subtype: JUN
      
        function: 门禁与消防联动
        medium_in: SIGNAL-FA
        medium_out: CTRL
      
        interface_system: FIRE-ALARM
      
        equipment_parameters:
          type: 联动模块
          functions:
            - 火灾时释放疏散门
            - 保持门禁记录
            - 消防确认后恢复
          
        location_hint:
          space_type: PANEL
          position: 门禁控制器旁

    sink_nodes:
  
      - node_id: INT-SEC_SNK_MONITOR
        node_name: 安防监控中心
        node_name_en: Security Operation Center
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 安防监控管理
        medium_in: DATA-IP
      
        equipment_parameters:
          components:
            - 监控工作站
            - 大屏显示系统
            - 报警处置终端
            - 对讲管理终端
          staffing: 24小时值班
        
        location_hint:
          space_type: ROOM
          room_name: 安防监控室/消控室
          position: 一层或地下室
        
      - node_id: INT-SEC_SNK_LOCK
        node_name: 电子锁具
        node_name_en: Electronic Lock
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 门锁控制
        medium_in: CTRL
      
        multiplicity: multiple
      
        equipment_parameters:
          types:
            - {type: 电磁锁, application: 玻璃门}
            - {type: 电插锁, application: 木门/金属门}
            - {type: 电锁口, application: 防火门}
          power: {value: 12/24, unit: VDC}
          fail_safe: 断电开门（疏散门）
        
        location_hint:
          space_type: DOOR
          position: 门框上方/侧边

  # ============================================================
  # 边定义
  # ============================================================
  edges:

    video_edges:
  
      - edge_id: INT-SEC_EDGE_CAM_001
        edge_name: 摄像机至交换机
        edge_type: TRK
        from_node: INT-SEC_SRC_CAMERA
        to_node: INT-NET_DST_ACCESS_SW
        direction: unidirectional
        medium: DATA-IP
        physical_properties:
          cable: CAT6/光纤
          poe: IEEE 802.3af/at
        cross_system: true
        target_system: INT-NET
      
      - edge_id: INT-SEC_EDGE_CAM_002
        edge_name: 交换机至NVR
        edge_type: TRK
        from_node: INT-NET_DST_ACCESS_SW
        to_node: INT-SEC_DST_NVR
        direction: unidirectional
        medium: DATA-IP
      
      - edge_id: INT-SEC_EDGE_CAM_003
        edge_name: NVR至视频平台
        edge_type: TRK
        from_node: INT-SEC_DST_NVR
        to_node: INT-SEC_DST_VMS
        direction: unidirectional
        medium: DATA-IP
      
      - edge_id: INT-SEC_EDGE_CAM_004
        edge_name: 视频平台至监控中心
        edge_type: TRM
        from_node: INT-SEC_DST_VMS
        to_node: INT-SEC_SNK_MONITOR
        direction: unidirectional
        medium: DATA-IP

    access_edges:
  
      - edge_id: INT-SEC_EDGE_ACC_001
        edge_name: 读卡器至控制器
        edge_type: TRK
        from_node: INT-SEC_SRC_READER
        to_node: INT-SEC_DST_DOOR_CTRL
        direction: bidirectional
        medium: SIGNAL-SEC
        physical_properties:
          protocol: Wiegand/RS485/OSDP
        
      - edge_id: INT-SEC_EDGE_ACC_002
        edge_name: 控制器至电锁
        edge_type: TRM
        from_node: INT-SEC_DST_DOOR_CTRL
        to_node: INT-SEC_SNK_LOCK
        direction: unidirectional
        medium: CTRL
      
      - edge_id: INT-SEC_EDGE_ACC_003
        edge_name: 控制器至门禁系统
        edge_type: TRK
        from_node: INT-SEC_DST_DOOR_CTRL
        to_node: INT-SEC_DST_ACS
        direction: bidirectional
        medium: DATA-IP
      
      - edge_id: INT-SEC_EDGE_ACC_004
        edge_name: 门禁系统至监控中心
        edge_type: TRM
        from_node: INT-SEC_DST_ACS
        to_node: INT-SEC_SNK_MONITOR
        direction: unidirectional
        medium: DATA-IP

    alarm_edges:
  
      - edge_id: INT-SEC_EDGE_ALM_001
        edge_name: 探测器至报警主机
        edge_type: TRK
        from_node: INT-SEC_SRC_SENSOR
        to_node: INT-SEC_DST_ALARM_PANEL
        direction: unidirectional
        medium: SIGNAL-SEC
        physical_properties:
          protocol: 总线制/有线
        
      - edge_id: INT-SEC_EDGE_ALM_002
        edge_name: 报警主机至监控中心
        edge_type: TRK
        from_node: INT-SEC_DST_ALARM_PANEL
        to_node: INT-SEC_SNK_MONITOR
        direction: unidirectional
        medium: DATA-IP

    interlock_edges:
  
      - edge_id: INT-SEC_EDGE_FA_001
        edge_name: 消防联动信号
        edge_type: CTRL
        from_node: FIRE-ALARM_DST_LINKAGE
        to_node: INT-SEC_DST_ACCESS
        direction: unidirectional
        medium: SIGNAL-FA
        cross_system: true
        source_system: FIRE-ALARM
      
      - edge_id: INT-SEC_EDGE_FA_002
        edge_name: 联动至门禁控制器
        edge_type: CTRL
        from_node: INT-SEC_DST_ACCESS
        to_node: INT-SEC_DST_DOOR_CTRL
        direction: unidirectional
        medium: CTRL

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:

    - path_id: INT-SEC_PATH_VIDEO
      path_name: 视频监控路径
      path_type: MON
      sequence:
        - {step: 1, element_type: node, element_id: INT-SEC_SRC_CAMERA}
        - {step: 2, element_type: edge, element_id: INT-SEC_EDGE_CAM_001}
        - {step: 3, element_type: node, element_id: INT-NET_DST_ACCESS_SW}
        - {step: 4, element_type: edge, element_id: INT-SEC_EDGE_CAM_002}
        - {step: 5, element_type: node, element_id: INT-SEC_DST_NVR}
        - {step: 6, element_type: edge, element_id: INT-SEC_EDGE_CAM_003}
        - {step: 7, element_type: node, element_id: INT-SEC_DST_VMS}
        - {step: 8, element_type: edge, element_id: INT-SEC_EDGE_CAM_004}
        - {step: 9, element_type: node, element_id: INT-SEC_SNK_MONITOR}
      
    - path_id: INT-SEC_PATH_ACCESS
      path_name: 门禁控制路径
      path_type: CTRL
      sequence:
        - {step: 1, element_type: node, element_id: INT-SEC_SRC_READER}
        - {step: 2, element_type: edge, element_id: INT-SEC_EDGE_ACC_001}
        - {step: 3, element_type: node, element_id: INT-SEC_DST_DOOR_CTRL}
        - {step: 4, element_type: edge, element_id: INT-SEC_EDGE_ACC_002}
        - {step: 5, element_type: node, element_id: INT-SEC_SNK_LOCK}

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:

    access_control:
      normal_mode:
        - 刷卡/人脸验证
        - 权限校验
        - 时间计划校验
        - 开门/拒绝
      
      anti_passback:
        description: 防尾随
        mode: 进出刷卡
      
      multi_authentication:
        description: 多重认证
        application: 高安全区域
        methods: [卡+密码, 卡+指纹, 卡+人脸]
      
    fire_interlock:
      trigger: 火灾报警确认
      action:
        - 释放所有疏散门
        - 保持门禁记录
        - 状态上报监控中心
      restore: 火警解除后手动恢复
    
    video_linkage:
      alarm_trigger:
        - 门禁报警
        - 入侵报警
        - 紧急按钮
      action:
        - 联动摄像机预置位
        - 弹出实时画面
        - 开始录像标记
        - 声光报警提示
      
    alarm_handling:
      workflow:
        - step: 1
          action: 报警触发
        - step: 2
          action: 监控中心收到报警
        - step: 3
          action: 联动视频弹窗
        - step: 4
          action: 值班人员确认
        - step: 5
          action: 处置/派单
        - step: 6
          action: 事件闭环
```

---

## 5.5 INT-NET 综合布线系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: INT-NET
    system_name: 综合布线系统
    system_name_en: Structured Cabling System
    category: INTELLIGENT
    version: 1.0
  
    description: |
      医院综合布线系统，为语音、数据、视频等信息传输提供物理通道。
      采用星型拓扑结构，支持千兆/万兆网络传输。
    
    design_basis:
      standard: TIA/EIA-568, ISO/IEC 11801
      category: CAT6A/CAT6（水平）, OS2光纤（主干）
      capacity: 信息点预留20%冗余
    
    serving_scope:
      - 数据网络
      - 语音通信
      - 视频监控
      - 楼宇自控
      - 医疗信息系统

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: INT-NET_BND_IN_EXTERNAL
        boundary_name: 外部网络接入
        medium: DATA-FIBER
        is_external: true
        source: 运营商/专网
      
    outputs:
      - boundary_id: INT-NET_BND_OUT_TERM
        boundary_name: 信息点位
        medium: DATA-COPPER/DATA-FIBER
        target: 终端设备

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:

    source_nodes:
  
      - node_id: INT-NET_SRC_EXTERNAL
        node_name: 外部网络接入
        node_name_en: External Network Entry
        node_type: Source_Node
        node_category: SRC
      
        function: 外部网络引入
        medium_out: DATA-FIBER
        is_external: true
      
        equipment_parameters:
          type: 光纤接入
          fiber_count: {value: 24-48, unit: 芯}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 进线间

    distribution_nodes:
  
      - node_id: INT-NET_DST_MDF
        node_name: 总配线架
        node_name_en: Main Distribution Frame
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 网络主配线
        medium_in: DATA-FIBER
        medium_out: DATA-FIBER
      
        equipment_parameters:
          type: 光纤配线架（ODF）+ 铜缆配线架
          fiber_capacity: {value: 144-288, unit: 芯}
          copper_capacity: {value: 200-500, unit: 对}
          rack: 19英寸标准机柜
        
        location_hint:
          space_type: RACK
          room_name: 中心机房/网络机房
        
        components:
          - ODF光纤配线架
          - 铜缆配线架
          - 理线器
          - 标识系统

      - node_id: INT-NET_DST_IDF
        node_name: 楼层配线架
        node_name_en: Intermediate Distribution Frame
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 楼层配线分配
        medium_in: DATA-FIBER
        medium_out: [DATA-FIBER, DATA-COPPER]
      
        multiplicity: multiple
        instance_pattern: INT-NET_DST_IDF_{Bldg}_{Floor}
      
        equipment_parameters:
          type: 楼层配线柜
          fiber_capacity: {value: 24-48, unit: 芯}
          copper_capacity: {value: 48-96, unit: 口}
          rack: 壁挂/落地机柜
        
        location_hint:
          space_type: WEAK_ROOM
          room_name: 楼层弱电间
        
        installation_requirements:
          - 防尘防潮
          - 空调或通风
          - UPS供电
          - 接地
        
        components:
          - 光纤配线盒
          - 铜缆配线架
          - 网络交换机空间
          - 理线器

      - node_id: INT-NET_DST_BACKBONE_FIBER
        node_name: 主干光缆
        node_name_en: Backbone Fiber Cable
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
      
        function: 主干光纤传输
        medium_in: DATA-FIBER
        medium_out: DATA-FIBER
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 室内单模光缆
          fiber_type: OS2 G.652D
          fiber_count: {value: 12-24, unit: 芯}
        
        location_hint:
          space_type: SHAFT
          shaft_type: 弱电竖井
        
        physical_properties:
          routing: MDF至各IDF
          length: 根据建筑高度

      - node_id: INT-NET_DST_HORIZONTAL
        node_name: 水平布线
        node_name_en: Horizontal Cabling
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
      
        function: 楼层水平布线
        medium_in: DATA-COPPER
        medium_out: DATA-COPPER
      
        multiplicity: multiple
      
        equipment_parameters:
          cable_type: CAT6A UTP/STP
          max_length: {value: 90, unit: m}
        
        location_hint:
          space_type: CEILING_VOID / CABLE_TRAY
          position: 走廊桥架/吊顶

      - node_id: INT-NET_DST_OUTLET
        node_name: 信息插座
        node_name_en: Information Outlet
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRM
      
        function: 终端接入点
        medium_in: DATA-COPPER
        medium_out: DATA-COPPER
      
        multiplicity: multiple
        instance_pattern: INT-NET_DST_OUTLET_{Floor}_{Room}_{Seq}
      
        equipment_parameters:
          type: 双口/四口面板
          module: RJ45模块
          category: CAT6A
        
        location_hint:
          space_type: WALL
          height: {value: 0.3, unit: m, note: 地插/墙插}
        
        typical_density:
          - {room_type: 办公室, density: "2口/工位"}
          - {room_type: 病房, density: "4口/床位"}
          - {room_type: 诊室, density: "4-6口"}
          - {room_type: 护士站, density: "8-12口"}

      - node_id: INT-NET_DST_ACCESS_SW
        node_name: 接入层交换机
        node_name_en: Access Switch
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
      
        function: 终端设备接入
        medium_in: [DATA-FIBER, DATA-COPPER]
        medium_out: DATA-COPPER
      
        multiplicity: multiple
        instance_pattern: INT-NET_DST_ACCESS_SW_{Bldg}_{Floor}_{Seq}
      
        equipment_parameters:
          type: 千兆接入交换机
          ports: {value: 24-48, unit: 口}
          uplink: 万兆光口
          features:
            - PoE/PoE+
            - VLAN
            - 网管功能
          
        location_hint:
          space_type: RACK
          room_name: 楼层弱电间
        
        note: 此节点属于INT-IT系统，但物理位置在综合布线配线间

    sink_nodes:
  
      - node_id: INT-NET_SNK_TERMINAL
        node_name: 终端设备
        node_name_en: Terminal Device
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 网络接入
        medium_in: DATA-COPPER
      
        multiplicity: multiple
      
        equipment_parameters:
          types:
            - 计算机
            - IP电话
            - 打印机
            - 医疗设备
            - 监控摄像机
            - 门禁设备
            - 无线AP

  # ============================================================
  # 边定义
  # ============================================================
  edges:

    backbone_edges:
  
      - edge_id: INT-NET_EDGE_BB_001
        edge_name: 外部接入至MDF
        edge_type: TRK
        from_node: INT-NET_SRC_EXTERNAL
        to_node: INT-NET_DST_MDF
        direction: bidirectional
        medium: DATA-FIBER
      
      - edge_id: INT-NET_EDGE_BB_002
        edge_name: MDF至主干光缆
        edge_type: TRK
        from_node: INT-NET_DST_MDF
        to_node: INT-NET_DST_BACKBONE_FIBER
        direction: bidirectional
        medium: DATA-FIBER
      
      - edge_id: INT-NET_EDGE_BB_003
        edge_name: 主干光缆至IDF
        edge_type: TRK
        from_node: INT-NET_DST_BACKBONE_FIBER
        to_node: INT-NET_DST_IDF
        direction: bidirectional
        medium: DATA-FIBER

    horizontal_edges:
  
      - edge_id: INT-NET_EDGE_HZ_001
        edge_name: IDF至水平布线
        edge_type: BRH
        from_node: INT-NET_DST_IDF
        to_node: INT-NET_DST_HORIZONTAL
        direction: bidirectional
        medium: DATA-COPPER
      
      - edge_id: INT-NET_EDGE_HZ_002
        edge_name: 水平布线至信息插座
        edge_type: TRM
        from_node: INT-NET_DST_HORIZONTAL
        to_node: INT-NET_DST_OUTLET
        direction: bidirectional
        medium: DATA-COPPER
      
      - edge_id: INT-NET_EDGE_HZ_003
        edge_name: 信息插座至终端
        edge_type: TRM
        from_node: INT-NET_DST_OUTLET
        to_node: INT-NET_SNK_TERMINAL
        direction: bidirectional
        medium: DATA-COPPER
        physical_properties:
          cable: 跳线
          max_length: {value: 5, unit: m}

    switch_edges:
  
      - edge_id: INT-NET_EDGE_SW_001
        edge_name: IDF至接入交换机
        edge_type: TRK
        from_node: INT-NET_DST_IDF
        to_node: INT-NET_DST_ACCESS_SW
        direction: bidirectional
        medium: DATA-COPPER
        physical_properties:
          type: 跳线连接

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:

    - path_id: INT-NET_PATH_DATA
      path_name: 数据传输路径
      path_type: DATA
      sequence:
        - {step: 1, element_type: node, element_id: INT-NET_SRC_EXTERNAL}
        - {step: 2, element_type: edge, element_id: INT-NET_EDGE_BB_001}
        - {step: 3, element_type: node, element_id: INT-NET_DST_MDF}
        - {step: 4, element_type: edge, element_id: INT-NET_EDGE_BB_002}
        - {step: 5, element_type: node, element_id: INT-NET_DST_BACKBONE_FIBER}
        - {step: 6, element_type: edge, element_id: INT-NET_EDGE_BB_003}
        - {step: 7, element_type: node, element_id: INT-NET_DST_IDF}
        - {step: 8, element_type: edge, element_id: INT-NET_EDGE_HZ_001}
        - {step: 9, element_type: node, element_id: INT-NET_DST_HORIZONTAL}
        - {step: 10, element_type: edge, element_id: INT-NET_EDGE_HZ_002}
        - {step: 11, element_type: node, element_id: INT-NET_DST_OUTLET}
        - {step: 12, element_type: edge, element_id: INT-NET_EDGE_HZ_003}
        - {step: 13, element_type: node, element_id: INT-NET_SNK_TERMINAL}

  # ============================================================
  # 设计规范
  # ============================================================
  design_standards:

    cable_specifications:
      horizontal:
        type: CAT6A U/FTP
        max_length: {value: 90, unit: m}
        bandwidth: {value: 500, unit: MHz}
      
      backbone:
        type: OS2 单模光纤
        fiber_count: {value: 12-24, unit: 芯/缆}
      
    outlet_density:
      office: {value: 2, unit: "口/10m²"}
      ward: {value: 4-6, unit: "口/床"}
      nurse_station: {value: 8-12, unit: 口}
      exam_room: {value: 4-6, unit: 口}
    
    labeling:
      format: "建筑-楼层-房间-插座序号"
      example: "A-03-301-01"
    
    testing:
      permanent_link: 每条链路测试
      parameters:
        - 插入损耗
        - 近端串扰
        - 回波损耗
        - 传输延迟
```

---

## 5.6 INT-IT 信息网络系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: INT-IT
    system_name: 信息网络系统
    system_name_en: Information Network System
    category: INTELLIGENT
    version: 1.0
  
    description: |
      医院信息网络系统，构建院内有线和无线网络基础设施。
      支持HIS/PACS/LIS等医疗信息系统运行。
      实现内外网隔离、安全防护。
    
    design_basis:
      network_separation:
        - 医疗专网（内网）
        - 办公网络
        - 互联网（外网）
        - 设备网络
      bandwidth: 核心万兆、接入千兆
      wireless: 全院覆盖
    
    serving_scope:
      - HIS医院信息系统
      - PACS影像系统
      - LIS检验系统
      - EMR电子病历
      - 办公自动化
      - 互联网接入

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: INT-IT_BND_IN_CABLING
        boundary_name: 综合布线
        medium: DATA-FIBER
        source_system: INT-NET
      
      - boundary_id: INT-IT_BND_IN_INTERNET
        boundary_name: 互联网接入
        medium: DATA-FIBER
        is_external: true
        source: ISP运营商
      
      - boundary_id: INT-IT_BND_IN_ELEC
        boundary_name: 电源
        medium: ELEC-UPS
        source_system: ELEC-UPS
      
    outputs:
      - boundary_id: INT-IT_BND_OUT_APP
        boundary_name: 应用系统接口
        medium: DATA-IP
        target: 各业务应用系统

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:

    source_nodes:
  
      - node_id: INT-IT_SRC_INTERNET
        node_name: 互联网出口
        node_name_en: Internet Gateway
        node_type: Source_Node
        node_category: SRC
      
        function: 互联网接入
        medium_out: DATA-IP
        is_external: true
      
        equipment_parameters:
          bandwidth: {value: 1-10, unit: Gbps}
          redundancy: 双线路
        
        location_hint:
          space_type: RACK
          room_name: 网络机房

    distribution_nodes:
  
      - node_id: INT-IT_DST_FIREWALL
        node_name: 防火墙
        node_name_en: Firewall
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 网络边界安全防护
        medium_in: DATA-IP
        medium_out: DATA-IP
      
        equipment_parameters:
          type: 下一代防火墙
          throughput: {value: 20-40, unit: Gbps}
          features:
            - 状态检测
            - 入侵防护
            - 应用识别
            - VPN
          configuration: 双机热备
        
        location_hint:
          space_type: RACK
          room_name: 网络机房
        
        control_points:
          sensors:
            - {point_id: FW_CPU, type: AI, description: CPU利用率}
            - {point_id: FW_SESSION, type: AI, description: 会话数}
          status:
            - {point_id: FW_HA, type: DI, description: 主备状态}
            - {point_id: FW_ATTACK, type: DI, description: 攻击告警}

      - node_id: INT-IT_DST_CORE_SW
        node_name: 核心交换机
        node_name_en: Core Switch
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 网络核心交换
        medium_in: DATA-IP
        medium_out: DATA-IP
      
        equipment_parameters:
          type: 模块化核心交换机
          backplane: {value: "≥10", unit: Tbps}
          ports:
            - {type: 40GE, count: 8-16}
            - {type: 10GE, count: 48-96}
          features:
            - VSS/堆叠
            - VLAN
            - 三层路由
            - QoS
          redundancy: 双核心
        
        location_hint:
          space_type: RACK
          room_name: 核心机房
        
        control_points:
          sensors:
            - {point_id: CORE_CPU, type: AI, description: CPU利用率}
            - {point_id: CORE_MEM, type: AI, description: 内存利用率}
            - {point_id: CORE_TEMP, type: AI, description: 设备温度}
          status:
            - {point_id: CORE_PORT, type: DI, description: 端口状态}
            - {point_id: CORE_STACK, type: DI, description: 堆叠状态}

      - node_id: INT-IT_DST_AGGR_SW
        node_name: 汇聚交换机
        node_name_en: Aggregation Switch
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 楼层汇聚
        medium_in: DATA-IP
        medium_out: DATA-IP
      
        multiplicity: multiple
        instance_pattern: INT-IT_DST_AGGR_SW_{Bldg}_{Zone}
      
        equipment_parameters:
          type: 万兆汇聚交换机
          uplink: 40GE×2
          downlink: 10GE×24-48
          features:
            - 堆叠
            - VLAN
            - QoS
          
        location_hint:
          space_type: RACK
          room_name: 楼层弱电间/汇聚机房

      - node_id: INT-IT_DST_ACCESS_SW
        node_name: 接入交换机
        node_name_en: Access Switch
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRM
      
        function: 终端接入
        medium_in: DATA-IP
        medium_out: DATA-IP
      
        multiplicity: multiple
        instance_pattern: INT-IT_DST_ACCESS_SW_{Bldg}_{Floor}_{Seq}
      
        equipment_parameters:
          type: 千兆接入交换机
          ports: {value: 24-48, unit: 口}
          uplink: 10GE×2
          features:
            - PoE+ (IEEE 802.3at)
            - VLAN
            - 网管
          
        location_hint:
          space_type: RACK
          room_name: 楼层弱电间

      - node_id: INT-IT_DST_WIRELESS_CTRL
        node_name: 无线控制器
        node_name_en: Wireless LAN Controller
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 无线网络管理
        medium_in: DATA-IP
        medium_out: DATA-IP
      
        equipment_parameters:
          type: 无线控制器
          ap_capacity: {value: 500-2000, unit: 台}
          throughput: {value: 40-100, unit: Gbps}
          features:
            - AP管理
            - 漫游切换
            - 射频管理
            - 用户认证
          redundancy: 双机热备
        
        location_hint:
          space_type: RACK
          room_name: 核心机房

      - node_id: INT-IT_DST_WIRELESS_AP
        node_name: 无线接入点
        node_name_en: Wireless Access Point
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRM
      
        function: 无线信号覆盖
        medium_in: DATA-IP
        medium_out: SIGNAL-WIFI
      
        multiplicity: multiple
        instance_pattern: INT-IT_DST_WIRELESS_AP_{Floor}_{Zone}_{Seq}
      
        equipment_parameters:
          type: 企业级AP
          standard: WiFi 6 (802.11ax)
          bands: 2.4GHz + 5GHz
          concurrent_users: {value: 50-100, unit: 用户}
          poe: IEEE 802.3at
        
        location_hint:
          space_type: CEILING
          position: 走廊/大厅吊顶
          spacing: {value: 15-25, unit: m}
        
        typical_density:
          - {area: 门诊大厅, density: "1台/200m²"}
          - {area: 病房走廊, density: "1台/25m"}
          - {area: 诊室区, density: "1台/300m²"}

      - node_id: INT-IT_DST_SERVER_SW
        node_name: 服务器交换机
        node_name_en: Server Switch
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 数据中心服务器接入
        medium_in: DATA-IP
        medium_out: DATA-IP
      
        equipment_parameters:
          type: 数据中心交换机
          ports: 10GE/25GE×48
          uplink: 100GE×4
          features:
            - 低延迟
            - 大缓存
            - VXLAN
          
        location_hint:
          space_type: RACK
          room_name: 数据中心

      - node_id: INT-IT_DST_NAC
        node_name: 网络准入控制
        node_name_en: Network Access Control
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 终端准入安全
        medium_in: DATA-IP
        medium_out: DATA-IP
      
        equipment_parameters:
          type: NAC系统
          functions:
            - 终端认证
            - 健康检查
            - 访客管理
            - 设备注册
          
        location_hint:
          space_type: RACK
          room_name: 网络机房

    sink_nodes:
  
      - node_id: INT-IT_SNK_SERVER
        node_name: 服务器
        node_name_en: Server
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 业务处理
        medium_in: DATA-IP
      
        multiplicity: multiple
      
        equipment_parameters:
          types:
            - HIS服务器
            - PACS服务器
            - LIS服务器
            - 数据库服务器
            - 虚拟化服务器
          
        location_hint:
          space_type: RACK
          room_name: 数据中心

      - node_id: INT-IT_SNK_TERMINAL
        node_name: 网络终端
        node_name_en: Network Terminal
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 网络访问
        medium_in: DATA-IP
      
        multiplicity: multiple
      
        equipment_parameters:
          types:
            - 医生工作站
            - 护士工作站
            - 自助终端
            - 移动终端

      - node_id: INT-IT_SNK_WIRELESS
        node_name: 无线终端
        node_name_en: Wireless Terminal
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 无线接入
        medium_in: SIGNAL-WIFI
      
        multiplicity: multiple
      
        equipment_parameters:
          types:
            - 移动查房设备
            - 移动护理设备
            - 患者终端

  # ============================================================
  # 边定义
  # ============================================================
  edges:

    internet_edges:
  
      - edge_id: INT-IT_EDGE_NET_001
        edge_name: 互联网至防火墙
        edge_type: TRK
        from_node: INT-IT_SRC_INTERNET
        to_node: INT-IT_DST_FIREWALL
        direction: bidirectional
        medium: DATA-IP
      
      - edge_id: INT-IT_EDGE_NET_002
        edge_name: 防火墙至核心交换机
        edge_type: TRK
        from_node: INT-IT_DST_FIREWALL
        to_node: INT-IT_DST_CORE_SW
        direction: bidirectional
        medium: DATA-IP

    core_edges:
  
      - edge_id: INT-IT_EDGE_CORE_001
        edge_name: 核心至汇聚
        edge_type: TRK
        from_node: INT-IT_DST_CORE_SW
        to_node: INT-IT_DST_AGGR_SW
        direction: bidirectional
        medium: DATA-IP
        physical_properties:
          link: 40GE
          redundancy: 双上联
        
      - edge_id: INT-IT_EDGE_CORE_002
        edge_name: 核心至服务器交换机
        edge_type: TRK
        from_node: INT-IT_DST_CORE_SW
        to_node: INT-IT_DST_SERVER_SW
        direction: bidirectional
        medium: DATA-IP
        physical_properties:
          link: 100GE

    access_edges:
  
      - edge_id: INT-IT_EDGE_ACC_001
        edge_name: 汇聚至接入
        edge_type: TRK
        from_node: INT-IT_DST_AGGR_SW
        to_node: INT-IT_DST_ACCESS_SW
        direction: bidirectional
        medium: DATA-IP
        physical_properties:
          link: 10GE
          redundancy: 双上联
        
      - edge_id: INT-IT_EDGE_ACC_002
        edge_name: 接入至终端
        edge_type: TRM
        from_node: INT-IT_DST_ACCESS_SW
        to_node: INT-IT_SNK_TERMINAL
        direction: bidirectional
        medium: DATA-IP
        physical_properties:
          link: 1GE

    wireless_edges:
  
      - edge_id: INT-IT_EDGE_WL_001
        edge_name: 核心至无线控制器
        edge_type: TRK
        from_node: INT-IT_DST_CORE_SW
        to_node: INT-IT_DST_WIRELESS_CTRL
        direction: bidirectional
        medium: DATA-IP
      
      - edge_id: INT-IT_EDGE_WL_002
        edge_name: 接入交换机至AP
        edge_type: TRM
        from_node: INT-IT_DST_ACCESS_SW
        to_node: INT-IT_DST_WIRELESS_AP
        direction: bidirectional
        medium: DATA-IP
        physical_properties:
          poe: IEEE 802.3at
        
      - edge_id: INT-IT_EDGE_WL_003
        edge_name: AP至无线终端
        edge_type: TRM
        from_node: INT-IT_DST_WIRELESS_AP
        to_node: INT-IT_SNK_WIRELESS
        direction: bidirectional
        medium: SIGNAL-WIFI

    server_edges:
  
      - edge_id: INT-IT_EDGE_SRV_001
        edge_name: 服务器交换机至服务器
        edge_type: TRM
        from_node: INT-IT_DST_SERVER_SW
        to_node: INT-IT_SNK_SERVER
        direction: bidirectional
        medium: DATA-IP
        physical_properties:
          link: 10GE/25GE

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:

    - path_id: INT-IT_PATH_INTERNET
      path_name: 互联网访问路径
      path_type: DATA
      sequence:
        - {step: 1, element_type: node, element_id: INT-IT_SNK_TERMINAL}
        - {step: 2, element_type: node, element_id: INT-IT_DST_ACCESS_SW}
        - {step: 3, element_type: node, element_id: INT-IT_DST_AGGR_SW}
        - {step: 4, element_type: node, element_id: INT-IT_DST_CORE_SW}
        - {step: 5, element_type: node, element_id: INT-IT_DST_FIREWALL}
        - {step: 6, element_type: node, element_id: INT-IT_SRC_INTERNET}
      
    - path_id: INT-IT_PATH_INTRANET
      path_name: 内网业务路径
      path_type: DATA
      sequence:
        - {step: 1, element_type: node, element_id: INT-IT_SNK_TERMINAL}
        - {step: 2, element_type: node, element_id: INT-IT_DST_ACCESS_SW}
        - {step: 3, element_type: node, element_id: INT-IT_DST_AGGR_SW}
        - {step: 4, element_type: node, element_id: INT-IT_DST_CORE_SW}
        - {step: 5, element_type: node, element_id: INT-IT_DST_SERVER_SW}
        - {step: 6, element_type: node, element_id: INT-IT_SNK_SERVER}

  # ============================================================
  # 网络安全设计
  # ============================================================
  security_design:

    network_segmentation:
      zones:
        - zone: 医疗内网
          vlan_range: 10-99
          purpose: HIS/PACS/EMR
          isolation: 严格隔离
        
        - zone: 办公网络
          vlan_range: 100-199
          purpose: 办公OA
          isolation: 逻辑隔离
        
        - zone: 设备网络
          vlan_range: 200-299
          purpose: 医疗设备
          isolation: 逻辑隔离
        
        - zone: 访客网络
          vlan_range: 900-999
          purpose: 患者/访客WiFi
          isolation: 完全隔离
        
    access_control:
      nac:
        - 终端准入认证
        - 终端健康检查
        - 访客管理
      
      802.1x:
        - 有线端口认证
        - 无线用户认证
```

---

## 5.7 INT-PA 公共广播系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: INT-PA
    system_name: 公共广播系统
    system_name_en: Public Address System
    category: INTELLIGENT
    version: 1.0
  
    description: |
      医院公共广播系统，实现背景音乐播放、信息广播、
      紧急广播（消防联动）等功能。
    
    design_basis:
      background_music: 分区控制、音量可调
      announcement: 分区寻呼、定时广播
      emergency: 消防优先、强制切入
    
    serving_scope:
      - 门诊大厅
      - 候诊区
      - 走廊
      - 病房（可选）
      - 地下车库

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: INT-PA_BND_IN_AUDIO
        boundary_name: 音源输入
        medium: SIGNAL-AUDIO
        source: 播放设备、话筒
      
      - boundary_id: INT-PA_BND_IN_FA
        boundary_name: 消防联动信号
        medium: SIGNAL-FA
        source_system: FIRE-ALARM
      
      - boundary_id: INT-PA_BND_IN_ELEC
        boundary_name: 电源
        medium: ELEC-LV
        source_system: ELEC-LV-MAIN
      
    outputs:
      - boundary_id: INT-PA_BND_OUT_AUDIO
        boundary_name: 音频输出
        medium: SIGNAL-AUDIO
        target: 扬声器

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:

    source_nodes:
  
      - node_id: INT-PA_SRC_PLAYER
        node_name: 音源播放器
        node_name_en: Audio Player
        node_type: Source_Node
        node_category: SRC
      
        function: 背景音乐播放
        medium_out: SIGNAL-AUDIO
      
        equipment_parameters:
          type: 数字音源播放器
          sources:
            - CD/DVD
            - USB/SD卡
            - 网络音频
            - FM收音
          format: MP3/WAV/FLAC
        
        location_hint:
          space_type: RACK
          room_name: 广播机房

      - node_id: INT-PA_SRC_MIC
        node_name: 广播话筒
        node_name_en: Announcement Microphone
        node_type: Source_Node
        node_category: SRC
      
        function: 人工广播
        medium_out: SIGNAL-AUDIO
      
        multiplicity: multiple
      
        equipment_parameters:
          types:
            - {type: 桌面话筒, location: 总控室}
            - {type: 手持话筒, location: 分控点}
            - {type: 紧急话筒, location: 消控室}
          features:
            - 分区选择
            - 优先级
            - PTT按键
          
        location_hint:
          space_type: DESK
        
        typical_locations:
          - 总服务台
          - 消防控制室
          - 安保室

      - node_id: INT-PA_SRC_FIRE_AUDIO
        node_name: 消防广播音源
        node_name_en: Fire Emergency Audio Source
        node_type: Source_Node
        node_category: SRC
      
        function: 消防疏散语音
        medium_out: SIGNAL-AUDIO
      
        interface_system: FIRE-ALARM
      
        equipment_parameters:
          type: 消防广播主机内置
          content:
            - 预录疏散语音
            - 消防紧急广播
          priority: 最高
        
        location_hint:
          space_type: PANEL
          room_name: 消防控制室

    distribution_nodes:
  
      - node_id: INT-PA_DST_MIXER
        node_name: 调音台
        node_name_en: Audio Mixer
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 音频混合处理
        medium_in: SIGNAL-AUDIO
        medium_out: SIGNAL-AUDIO
      
        equipment_parameters:
          type: 数字调音台
          channels: {value: 8-16, unit: 路}
          functions:
            - 音量调节
            - 均衡处理
            - 音源选择
          
        location_hint:
          space_type: RACK
          room_name: 广播机房

      - node_id: INT-PA_DST_MATRIX
        node_name: 广播矩阵
        node_name_en: Audio Matrix
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 分区控制
        medium_in: SIGNAL-AUDIO
        medium_out: SIGNAL-AUDIO
      
        equipment_parameters:
          type: 数字音频矩阵
          inputs: {value: 8-16, unit: 路}
          outputs: {value: 16-64, unit: 区}
          functions:
            - 分区路由
            - 定时控制
            - 优先级管理
            - 消防联动
          
        location_hint:
          space_type: RACK
          room_name: 广播机房
        
        control_points:
          sensors:
            - {point_id: MATRIX_INPUT, type: AI, description: 输入电平}
          status:
            - {point_id: MATRIX_ZONE, type: DI, description: 分区状态}
            - {point_id: MATRIX_FIRE, type: DI, description: 消防模式}

      - node_id: INT-PA_DST_AMPLIFIER
        node_name: 功率放大器
        node_name_en: Power Amplifier
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 音频功率放大
        medium_in: SIGNAL-AUDIO
        medium_out: SIGNAL-AUDIO
      
        multiplicity: multiple
        instance_pattern: INT-PA_DST_AMPLIFIER_{Zone}
      
        equipment_parameters:
          type: 定压功放
          power: {value: 120-500, unit: W}
          output: {value: 100, unit: V}
          backup: 主备切换
        
        location_hint:
          space_type: RACK
          room_name: 广播机房/楼层弱电间
        
        control_points:
          sensors:
            - {point_id: AMP_POWER, type: AI, description: 输出功率}
          status:
            - {point_id: AMP_RUN, type: DI, description: 运行状态}
            - {point_id: AMP_FAULT, type: DI, description: 故障报警}

      - node_id: INT-PA_DST_FIRE_CHANNEL
        node_name: 消防广播通道
        node_name_en: Fire Broadcast Channel
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 消防广播强制切入
        medium_in: [SIGNAL-AUDIO, SIGNAL-FA]
        medium_out: SIGNAL-AUDIO
      
        interface_system: FIRE-ALARM
      
        equipment_parameters:
          priority: 最高
          override: 强制切入所有分区
          control: 消防联动
        
        location_hint:
          space_type: PANEL
          room_name: 消防控制室

      - node_id: INT-PA_DST_ZONE_CTRL
        node_name: 分区控制器
        node_name_en: Zone Controller
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 分区音量控制
        medium_in: SIGNAL-AUDIO
        medium_out: SIGNAL-AUDIO
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 分区控制面板
          functions:
            - 本地音量调节
            - 音源选择
            - 开关控制
          
        location_hint:
          space_type: WALL
          position: 各功能区入口

      - node_id: INT-PA_DST_SPEAKER_LINE
        node_name: 扬声器线路
        node_name_en: Speaker Line
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
      
        function: 音频线路分配
        medium_in: SIGNAL-AUDIO
        medium_out: SIGNAL-AUDIO
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 定压线路（100V）
          cable: RVV 2×1.5mm²
        
        location_hint:
          space_type: CEILING_VOID
          position: 吊顶内线管

    sink_nodes:
  
      - node_id: INT-PA_SNK_SPEAKER
        node_name: 扬声器
        node_name_en: Speaker
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 声音输出
        medium_in: SIGNAL-AUDIO
      
        multiplicity: multiple
        instance_pattern: INT-PA_SNK_SPEAKER_{Floor}_{Zone}_{Seq}
      
        equipment_parameters:
          types:
            - {type: 吸顶扬声器, power: "3-6W", application: 走廊/大厅}
            - {type: 壁挂扬声器, power: "6-10W", application: 候诊区}
            - {type: 音柱, power: "20-40W", application: 室外}
          input: 定压100V
        
        location_hint:
          space_type: CEILING / WALL
        
        typical_spacing:
          - {area: 走廊, spacing: "8-10m"}
          - {area: 大厅, spacing: "10-15m"}
          - {area: 候诊区, spacing: "按面积计算"}

  # ============================================================
  # 边定义
  # ============================================================
  edges:

    source_edges:
  
      - edge_id: INT-PA_EDGE_SRC_001
        edge_name: 音源至调音台
        edge_type: TRK
        from_node: INT-PA_SRC_PLAYER
        to_node: INT-PA_DST_MIXER
        direction: unidirectional
        medium: SIGNAL-AUDIO
      
      - edge_id: INT-PA_EDGE_SRC_002
        edge_name: 话筒至调音台
        edge_type: TRK
        from_node: INT-PA_SRC_MIC
        to_node: INT-PA_DST_MIXER
        direction: unidirectional
        medium: SIGNAL-AUDIO

    processing_edges:
  
      - edge_id: INT-PA_EDGE_PROC_001
        edge_name: 调音台至矩阵
        edge_type: TRK
        from_node: INT-PA_DST_MIXER
        to_node: INT-PA_DST_MATRIX
        direction: unidirectional
        medium: SIGNAL-AUDIO
      
      - edge_id: INT-PA_EDGE_PROC_002
        edge_name: 矩阵至功放
        edge_type: BRH
        from_node: INT-PA_DST_MATRIX
        to_node: INT-PA_DST_AMPLIFIER
        direction: unidirectional
        medium: SIGNAL-AUDIO

    output_edges:
  
      - edge_id: INT-PA_EDGE_OUT_001
        edge_name: 功放至扬声器线路
        edge_type: TRK
        from_node: INT-PA_DST_AMPLIFIER
        to_node: INT-PA_DST_SPEAKER_LINE
        direction: unidirectional
        medium: SIGNAL-AUDIO
      
      - edge_id: INT-PA_EDGE_OUT_002
        edge_name: 扬声器线路至扬声器
        edge_type: TRM
        from_node: INT-PA_DST_SPEAKER_LINE
        to_node: INT-PA_SNK_SPEAKER
        direction: unidirectional
        medium: SIGNAL-AUDIO

    fire_edges:
  
      - edge_id: INT-PA_EDGE_FIRE_001
        edge_name: 消防联动信号
        edge_type: CTRL
        from_node: FIRE-ALARM_DST_LINKAGE
        to_node: INT-PA_DST_FIRE_CHANNEL
        direction: unidirectional
        medium: SIGNAL-FA
        cross_system: true
        source_system: FIRE-ALARM
      
      - edge_id: INT-PA_EDGE_FIRE_002
        edge_name: 消防音源至广播通道
        edge_type: TRK
        from_node: INT-PA_SRC_FIRE_AUDIO
        to_node: INT-PA_DST_FIRE_CHANNEL
        direction: unidirectional
        medium: SIGNAL-AUDIO
      
      - edge_id: INT-PA_EDGE_FIRE_003
        edge_name: 消防广播至矩阵
        edge_type: TRK
        from_node: INT-PA_DST_FIRE_CHANNEL
        to_node: INT-PA_DST_MATRIX
        direction: unidirectional
        medium: SIGNAL-AUDIO
        note: 强制切入，优先级最高

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:

    - path_id: INT-PA_PATH_BGM
      path_name: 背景音乐路径
      path_type: AUDIO
      mode: 正常广播
      sequence:
        - {step: 1, element_type: node, element_id: INT-PA_SRC_PLAYER}
        - {step: 2, element_type: edge, element_id: INT-PA_EDGE_SRC_001}
        - {step: 3, element_type: node, element_id: INT-PA_DST_MIXER}
        - {step: 4, element_type: edge, element_id: INT-PA_EDGE_PROC_001}
        - {step: 5, element_type: node, element_id: INT-PA_DST_MATRIX}
        - {step: 6, element_type: edge, element_id: INT-PA_EDGE_PROC_002}
        - {step: 7, element_type: node, element_id: INT-PA_DST_AMPLIFIER}
        - {step: 8, element_type: edge, element_id: INT-PA_EDGE_OUT_001}
        - {step: 9, element_type: node, element_id: INT-PA_DST_SPEAKER_LINE}
        - {step: 10, element_type: edge, element_id: INT-PA_EDGE_OUT_002}
        - {step: 11, element_type: node, element_id: INT-PA_SNK_SPEAKER}
      
    - path_id: INT-PA_PATH_FIRE
      path_name: 消防广播路径
      path_type: AUDIO
      mode: 消防联动
      priority: 最高
      sequence:
        - {step: 1, element_type: node, element_id: INT-PA_SRC_FIRE_AUDIO}
        - {step: 2, element_type: edge, element_id: INT-PA_EDGE_FIRE_002}
        - {step: 3, element_type: node, element_id: INT-PA_DST_FIRE_CHANNEL}
        - {step: 4, element_type: edge, element_id: INT-PA_EDGE_FIRE_003}
        - {step: 5, element_type: node, element_id: INT-PA_DST_MATRIX}
        - {step: 6, element_type: node, element_id: INT-PA_DST_AMPLIFIER}
        - {step: 7, element_type: node, element_id: INT-PA_SNK_SPEAKER}

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:

    priority_management:
      levels:
        - {priority: 1, source: 消防广播, override: 强制全区}
        - {priority: 2, source: 紧急话筒, override: 可选分区}
        - {priority: 3, source: 业务寻呼, override: 本分区}
        - {priority: 4, source: 背景音乐, override: 无}
      
    fire_linkage:
      trigger: FIRE-ALARM火灾确认信号
      action:
        - 切断所有背景音乐
        - 强制切入消防广播
        - 按疏散顺序播放语音
        - 可手动插入紧急广播
      sequence:
        - 首先广播着火层
        - 然后广播上层
        - 最后广播下层
        - 循环播放疏散指引
      
    time_schedule:
      description: 定时播放控制
      examples:
        - {time: "07:30", action: 开启背景音乐}
        - {time: "08:00", action: 门诊开诊提示}
        - {time: "12:00", action: 午间休息提示}
        - {time: "17:30", action: 门诊结束提示}
        - {time: "21:00", action: 关闭背景音乐}
      
    volume_control:
      method: 分区独立调节
      range: {value: "0-100", unit: "%"}
      night_mode: 自动降低音量
```

---

## Batch 5 输出总结

```yaml
Batch_5_Summary:

  completed_systems:
    - system_id: HVAC-FCU
      nodes: 14
      edges: 14
      paths: 2
      description: 风机盘管系统
    
    - system_id: HVAC-NEG
      nodes: 11
      edges: 7
      paths: 2
      description: 负压隔离系统
    
    - system_id: HVAC-PAU
      nodes: 8
      edges: 6
      paths: 1
      description: 新风机组系统
    
    - system_id: INT-SEC
      nodes: 14
      edges: 12
      paths: 2
      description: 安全防范系统
    
    - system_id: INT-NET
      nodes: 9
      edges: 9
      paths: 1
      description: 综合布线系统
    
    - system_id: INT-IT
      nodes: 14
      edges: 12
      paths: 2
      description: 信息网络系统
    
    - system_id: INT-PA
      nodes: 12
      edges: 10
      paths: 2
      description: 公共广播系统

  total_batch_5:
    systems: 7
    nodes: 82
    edges: 70
  
  grand_total_all_batches:
    batches: 5
    systems: 33
    estimated_nodes: 362+
    estimated_edges: 310+
```

---

## 系统完整性更新

```yaml
System_Completeness_Update:

  completed_rate_by_priority:
    P1_CRITICAL: 
      total: 18
      completed: 18
      rate: 100%
    
    P2_IMPORTANT:
      total: 14
      completed: 11
      rate: 78.6%
      remaining:
        - HVAC-VENT: 普通通风系统
        - INT-CLOCK: 时钟系统
        - INT-IBMS: 智能化集成平台
      
    P3_OPTIONAL:
      total: 5
      completed: 0
      rate: 0%
      remaining:
        - PLUMB-STORM: 雨水排水系统
        - PLUMB-RW: 中水回用系统
        - INT-IPTV: 病房电视系统
        - MGAS-N2: 氮气系统
        - MGAS-CO2: 二氧化碳系统
```

---

**Batch 5 完成。**

