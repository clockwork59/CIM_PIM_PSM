## 🧑‍💻 User


启动Batch 5

---
## 🤖 Assistant


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

---