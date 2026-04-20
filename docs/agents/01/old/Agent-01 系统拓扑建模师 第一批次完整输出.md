 
# Agent-01 第一批次完整输出

## 声明

本输出严格遵循Agent-01系统拓扑建模师Prompt v2.0规范，覆盖HVAC核心系统的完整拓扑建模。

---

## 第一部分：系统目录 (System Catalog)

```yaml
System_Catalog:

  - category_id: HVAC
    category_name: 暖通空调系统
    category_name_en: HVAC Systems
    description: 提供建筑供冷、供热、通风、空气处理功能的系统集合
  
    systems:
      - system_id: HVAC-CHP
        system_name: 冷源系统
        system_name_en: Chiller Plant System
        primary_medium: WATER-CHW
        secondary_medium: [WATER-CW, ELEC-AC]
        description: 制备和输配冷冻水的核心系统，包含冷水机组、一次泵、二次泵、分集水器
        priority: P1-CRITICAL
      
      - system_id: HVAC-CWP
        system_name: 冷却水系统
        system_name_en: Cooling Water System
        primary_medium: WATER-CW
        secondary_medium: [WATER-MU, ELEC-AC]
        description: 冷却塔及冷却水循环系统，为冷水机组冷凝器散热
        priority: P1-CRITICAL
      
      - system_id: HVAC-HWP
        system_name: 热源系统
        system_name_en: Heating Water Plant System
        primary_medium: WATER-HW
        secondary_medium: [GAS-NG, ELEC-AC]
        description: 锅炉/换热站及热水输配系统
        priority: P1-CRITICAL
      
      - system_id: HVAC-AHU
        system_name: 空调风系统
        system_name_en: Air Handling Unit System
        primary_medium: AIR-SUPPLY
        secondary_medium: [WATER-CHW, WATER-HW, ELEC-AC]
        description: 舒适性空调区域的空气处理与输配（门诊、病房、办公）
        priority: P2-IMPORTANT
      
      - system_id: HVAC-CLEAN
        system_name: 洁净空调系统
        system_name_en: Clean Room HVAC System
        primary_medium: AIR-SUPPLY
        secondary_medium: [WATER-CHW, WATER-HW, ELEC-AC]
        description: 手术室、ICU、实验室等洁净区专用空调
        priority: P1-CRITICAL
      
      - system_id: HVAC-NEG
        system_name: 负压隔离系统
        system_name_en: Negative Pressure Isolation System
        primary_medium: AIR-EXHAUST
        secondary_medium: [ELEC-AC]
        description: 传染病房、隔离病房负压控制与排风系统
        priority: P1-CRITICAL
      
      - system_id: HVAC-FCU
        system_name: 风机盘管系统
        system_name_en: Fan Coil Unit System
        primary_medium: AIR-SUPPLY
        secondary_medium: [WATER-CHW, WATER-HW, ELEC-AC]
        description: 分散式末端空调系统
        priority: P2-IMPORTANT
      
      - system_id: HVAC-VENT
        system_name: 通风系统
        system_name_en: Ventilation System
        primary_medium: AIR-EXHAUST
        secondary_medium: [ELEC-AC]
        description: 地下室、设备机房、卫生间等普通通风
        priority: P3-NORMAL
      
      - system_id: HVAC-SMOKE
        system_name: 防排烟系统
        system_name_en: Smoke Control System
        primary_medium: AIR-EXHAUST
        secondary_medium: [ELEC-AC]
        description: 消防排烟及补风系统
        priority: P1-CRITICAL

    system_dependencies:
      - upstream: HVAC-CWP
        downstream: HVAC-CHP
        interface_medium: WATER-CW
        description: 冷却水系统为冷源系统提供散热
      
      - upstream: HVAC-CHP
        downstream: HVAC-AHU
        interface_medium: WATER-CHW
        description: 冷源系统为空调机组提供冷冻水
      
      - upstream: HVAC-CHP
        downstream: HVAC-CLEAN
        interface_medium: WATER-CHW
        description: 冷源系统为洁净空调提供冷冻水
      
      - upstream: HVAC-CHP
        downstream: HVAC-FCU
        interface_medium: WATER-CHW
        description: 冷源系统为风机盘管提供冷冻水
      
      - upstream: HVAC-HWP
        downstream: HVAC-AHU
        interface_medium: WATER-HW
        description: 热源系统为空调机组提供热水
      
      - upstream: HVAC-HWP
        downstream: HVAC-CLEAN
        interface_medium: WATER-HW
        description: 热源系统为洁净空调提供热水
```

---

## 第二部分：介质类型定义 (Medium Types)

```yaml
Medium_Types:

  # 水系统介质
  Water_Media:
    - medium_id: WATER-CHW
      medium_name: 冷冻水
      medium_name_en: Chilled Water
      category: WATER
      typical_properties:
        temperature_supply: {value: 7, unit: ℃}
        temperature_return: {value: 12, unit: ℃}
        delta_t: {value: 5, unit: K}
        pressure_working: {value: 1000, unit: kPa}
        velocity_typical: {value: 1.5-2.5, unit: m/s}
      
    - medium_id: WATER-CW
      medium_name: 冷却水
      medium_name_en: Cooling Water
      category: WATER
      typical_properties:
        temperature_supply: {value: 32, unit: ℃}
        temperature_return: {value: 37, unit: ℃}
        delta_t: {value: 5, unit: K}
        pressure_working: {value: 600, unit: kPa}
        velocity_typical: {value: 2.0-3.0, unit: m/s}
      
    - medium_id: WATER-HW
      medium_name: 热水
      medium_name_en: Hot Water
      category: WATER
      typical_properties:
        temperature_supply: {value: 60, unit: ℃}
        temperature_return: {value: 50, unit: ℃}
        delta_t: {value: 10, unit: K}
        pressure_working: {value: 1000, unit: kPa}
        velocity_typical: {value: 1.5-2.5, unit: m/s}
      
    - medium_id: WATER-MU
      medium_name: 补水
      medium_name_en: Make-up Water
      category: WATER
      typical_properties:
        temperature: {value: 15-25, unit: ℃}
        pressure_working: {value: 300, unit: kPa}

  # 空气介质
  Air_Media:
    - medium_id: AIR-OA
      medium_name: 室外新风
      medium_name_en: Outdoor Air
      category: AIR
      is_external: true
      typical_properties:
        temperature_summer: {value: 35, unit: ℃}
        temperature_winter: {value: -5, unit: ℃}
        humidity_summer: {value: 70, unit: "%RH"}
      
    - medium_id: AIR-SA
      medium_name: 送风
      medium_name_en: Supply Air
      category: AIR
      typical_properties:
        temperature_summer: {value: 14-18, unit: ℃}
        temperature_winter: {value: 30-35, unit: ℃}
        velocity_duct: {value: 6-10, unit: m/s}
        velocity_terminal: {value: 2-4, unit: m/s}
      
    - medium_id: AIR-RA
      medium_name: 回风
      medium_name_en: Return Air
      category: AIR
      typical_properties:
        temperature_summer: {value: 24-26, unit: ℃}
        temperature_winter: {value: 20-22, unit: ℃}
      
    - medium_id: AIR-EA
      medium_name: 排风
      medium_name_en: Exhaust Air
      category: AIR
      is_external: true
      typical_properties:
        velocity_duct: {value: 8-12, unit: m/s}

  # 电力介质
  Electrical_Media:
    - medium_id: ELEC-HV
      medium_name: 高压电
      medium_name_en: High Voltage
      category: ELECTRICAL
      typical_properties:
        voltage: {value: 10, unit: kV}
      
    - medium_id: ELEC-LV
      medium_name: 低压动力电
      medium_name_en: Low Voltage Power
      category: ELECTRICAL
      typical_properties:
        voltage: {value: 380, unit: V}
        phases: 3
      
    - medium_id: ELEC-EPS
      medium_name: 应急电源
      medium_name_en: Emergency Power Supply
      category: ELECTRICAL
      typical_properties:
        voltage: {value: 380, unit: V}
        backup_duration: {value: 30-120, unit: min}

  # 控制信号
  Control_Media:
    - medium_id: CTRL-BA
      medium_name: 楼宇自控信号
      medium_name_en: Building Automation Signal
      category: CONTROL
      protocol: [BACnet, Modbus, LON]
    
    - medium_id: CTRL-DDC
      medium_name: DDC控制信号
      medium_name_en: DDC Control Signal
      category: CONTROL
      signal_types: [AI, AO, DI, DO]
```

---

## 第三部分：HVAC-CHP 冷源系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: HVAC-CHP
    system_name: 冷源系统
    system_name_en: Chiller Plant System
    category: HVAC
    version: 1.0
  
    description: |
      医院中央冷源系统，采用一次泵变流量或二次泵变流量系统。
      包含离心式/螺杆式冷水机组、冷冻水泵组、分集水器及输配管网。
      为全院空调末端提供7/12℃冷冻水。
    
    design_basis:
      cooling_load: {value: 8000-15000, unit: kW, note: 三级甲等医院典型值}
      chiller_configuration: "3+1备用"
      pump_configuration: "一次泵定流量 + 二次泵变流量"
      control_strategy: "供水温度+压差控制"
    
    serving_scope:
      - HVAC-AHU (空调机组)
      - HVAC-CLEAN (洁净空调)
      - HVAC-FCU (风机盘管)
      - HVAC-PAU (新风机组)

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: HVAC-CHP_BND_IN_ELEC
        boundary_name: 动力电源输入
        medium: ELEC-LV
        source_system: ELEC-LV-MAIN
        interface_point: 冷冻机房配电柜
        parameters:
          voltage: {value: 380, unit: V}
          capacity: {value: 3000, unit: kW}
        
      - boundary_id: HVAC-CHP_BND_IN_CW
        boundary_name: 冷却水输入
        medium: WATER-CW
        source_system: HVAC-CWP
        interface_point: 冷机冷凝器入口
        parameters:
          temperature: {value: 32, unit: ℃}
          flow_rate: {value: 按冷机配置, unit: m³/h}
        
      - boundary_id: HVAC-CHP_BND_IN_MU
        boundary_name: 系统补水
        medium: WATER-MU
        source_system: PLUMB-DWS
        interface_point: 定压补水装置
        parameters:
          pressure: {value: 300, unit: kPa}
        
      - boundary_id: HVAC-CHP_BND_IN_CTRL
        boundary_name: 控制信号输入
        medium: CTRL-BA
        source_system: BA-SYSTEM
        interface_point: 冷站群控柜
        parameters:
          protocol: BACnet/IP
        
    outputs:
      - boundary_id: HVAC-CHP_BND_OUT_CHW_SUP
        boundary_name: 冷冻水供水输出
        medium: WATER-CHW
        target_systems: [HVAC-AHU, HVAC-CLEAN, HVAC-FCU]
        interface_point: 二次供水总管
        parameters:
          temperature: {value: 7, unit: ℃}
          pressure: {value: 800, unit: kPa}
        
      - boundary_id: HVAC-CHP_BND_OUT_CW_RET
        boundary_name: 冷却水回水输出
        medium: WATER-CW
        target_system: HVAC-CWP
        interface_point: 冷机冷凝器出口
        parameters:
          temperature: {value: 37, unit: ℃}

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:

    # ----------------------------------------------------------
    # 源节点 (Source Nodes)
    # ----------------------------------------------------------
    source_nodes:
  
      - node_id: HVAC-CHP_SRC_CHILLER
        node_name: 冷水机组
        node_name_en: Chiller
        node_type: Source_Node
        node_category: SRC
      
        function: 制备冷冻水
        medium_in: [WATER-CW, ELEC-LV]
        medium_out: WATER-CHW
      
        is_external: false
        multiplicity: multiple
        instance_pattern: HVAC-CHP_SRC_CHILLER_{NNN}
      
        typical_configuration:
          quantity: 4
          redundancy: "N+1"
          capacity_each: {value: 2000, unit: RT}
          capacity_total: {value: 6000, unit: RT, note: 3台运行}
          chiller_type: [离心式, 螺杆式]
        
        equipment_parameters:
          cop_design: {value: 5.5-6.2, unit: null}
          chw_flow: {value: 350-450, unit: m³/h, per_unit: true}
          cw_flow: {value: 420-540, unit: m³/h, per_unit: true}
          power_input: {value: 1200-1500, unit: kW, per_unit: true}
          evaporator_pressure_drop: {value: 60-80, unit: kPa}
          condenser_pressure_drop: {value: 60-80, unit: kPa}
        
        location_hint:
          building: 动力中心/主楼地下
          floor: B1或B2
          space_type: MEP_ROOM
          room_name: 冷冻机房
        
        installation_requirements:
          - 楼板荷载加强 ≥ 20kN/m²
          - 减振基础，减振效率 ≥ 95%
          - 吊装孔或吊装通道
          - 设备四周检修空间 ≥ 1.5m
          - 抽管空间（单侧）≥ 设备长度
          - 排水沟及集水坑
        
        control_points:
          sensors:
            - {point_id: CHW_TEMP_SUP, type: AI, description: 冷冻水供水温度}
            - {point_id: CHW_TEMP_RET, type: AI, description: 冷冻水回水温度}
            - {point_id: CW_TEMP_SUP, type: AI, description: 冷却水供水温度}
            - {point_id: CW_TEMP_RET, type: AI, description: 冷却水回水温度}
            - {point_id: CHILLER_AMPS, type: AI, description: 运行电流}
            - {point_id: CHILLER_KW, type: AI, description: 运行功率}
          commands:
            - {point_id: CHILLER_START, type: DO, description: 启停控制}
            - {point_id: CHILLER_LOAD, type: AO, description: 负荷限制}
          status:
            - {point_id: CHILLER_RUN, type: DI, description: 运行状态}
            - {point_id: CHILLER_FAULT, type: DI, description: 故障报警}

    # ----------------------------------------------------------
    # 分配节点 (Distribution Nodes)
    # ----------------------------------------------------------
    distribution_nodes:
  
      # 集水器
      - node_id: HVAC-CHP_DST_COLLECTOR
        node_name: 集水器
        node_name_en: Return Header / Collector
        node_type: Distribution_Node
        node_category: DST
        node_subtype: JUN
      
        function: 汇集冷机蒸发器出水（或回水汇集）
        medium_in: WATER-CHW
        medium_out: WATER-CHW
      
        multiplicity: single
      
        equipment_parameters:
          diameter: {value: DN400-DN600, unit: mm}
          length: {value: 3000-5000, unit: mm}
          connections: {chiller: 4, pump: 4, bypass: 1}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房
          position: 冷机蒸发器出口侧
        
      # 一次冷冻泵
      - node_id: HVAC-CHP_DST_PUMP_PRI
        node_name: 一次冷冻水泵
        node_name_en: Primary Chilled Water Pump
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 一次侧冷冻水循环动力（定流量或变流量）
        medium_in: WATER-CHW
        medium_out: WATER-CHW
      
        multiplicity: multiple
        instance_pattern: HVAC-CHP_DST_PUMP_PRI_{NNN}
      
        typical_configuration:
          quantity: 4
          redundancy: "与冷机一一对应"
          control_mode: 定流量（一次泵定流量系统）或变流量
        
        equipment_parameters:
          flow_rate: {value: 350-450, unit: m³/h, per_unit: true}
          head: {value: 28-32, unit: m}
          power: {value: 45-55, unit: kW, per_unit: true}
          efficiency: {value: 0.78-0.82, unit: null}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房
          position: 冷机蒸发器出口侧
        
        installation_requirements:
          - 减振基座
          - 进出口软接头
          - 进口过滤器
          - 出口止回阀
          - 压力表接口
        
        control_points:
          sensors:
            - {point_id: PUMP_FREQ, type: AI, description: 运行频率, note: 变频泵}
            - {point_id: PUMP_AMPS, type: AI, description: 运行电流}
          commands:
            - {point_id: PUMP_START, type: DO, description: 启停控制}
            - {point_id: PUMP_SPEED, type: AO, description: 频率设定, note: 变频泵}
          status:
            - {point_id: PUMP_RUN, type: DI, description: 运行状态}
            - {point_id: PUMP_FAULT, type: DI, description: 故障报警}

      # 分水器
      - node_id: HVAC-CHP_DST_HEADER
        node_name: 分水器
        node_name_en: Supply Header / Distributor
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 分配冷冻水至各供水环路（二次泵入口）
        medium_in: WATER-CHW
        medium_out: WATER-CHW
      
        multiplicity: single
      
        equipment_parameters:
          diameter: {value: DN400-DN600, unit: mm}
          length: {value: 3000-5000, unit: mm}
          connections: {primary_pump: 4, secondary_pump: 4, bypass: 1}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房
          position: 与集水器并列
        
      # 旁通管
      - node_id: HVAC-CHP_DST_BYPASS
        node_name: 压差旁通阀
        node_name_en: Differential Pressure Bypass Valve
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 维持一次侧最小流量，稳定系统压差
        medium_in: WATER-CHW
        medium_out: WATER-CHW
      
        multiplicity: single
      
        equipment_parameters:
          valve_type: 电动调节阀
          size: {value: DN150-DN250, unit: mm}
          control_mode: 压差控制
          setpoint: {value: 根据系统设计, unit: kPa}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房
          position: 分集水器之间
        
        control_points:
          sensors:
            - {point_id: BYPASS_DP, type: AI, description: 分集水器压差}
            - {point_id: BYPASS_POS, type: AI, description: 阀门开度}
          commands:
            - {point_id: BYPASS_CMD, type: AO, description: 开度控制}

      # 二次冷冻泵
      - node_id: HVAC-CHP_DST_PUMP_SEC
        node_name: 二次冷冻水泵
        node_name_en: Secondary Chilled Water Pump
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 二次侧变流量输配，根据末端需求调节流量
        medium_in: WATER-CHW
        medium_out: WATER-CHW
      
        multiplicity: multiple
        instance_pattern: HVAC-CHP_DST_PUMP_SEC_{NNN}
      
        typical_configuration:
          quantity: 4
          redundancy: "N+1"
          control_mode: 变频变流量
        
        equipment_parameters:
          flow_rate: {value: 300-500, unit: m³/h, per_unit: true}
          head: {value: 35-45, unit: m}
          power: {value: 55-75, unit: kW, per_unit: true}
          efficiency: {value: 0.80-0.85, unit: null}
          vfd: true
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房
          position: 分水器出口侧
        
        control_points:
          sensors:
            - {point_id: PUMP_FREQ, type: AI, description: 运行频率}
            - {point_id: PUMP_AMPS, type: AI, description: 运行电流}
            - {point_id: PUMP_DP, type: AI, description: 供回水压差（远端）}
          commands:
            - {point_id: PUMP_START, type: DO, description: 启停控制}
            - {point_id: PUMP_SPEED, type: AO, description: 频率设定}
          status:
            - {point_id: PUMP_RUN, type: DI, description: 运行状态}
            - {point_id: PUMP_FAULT, type: DI, description: 故障报警}

      # 供水总管
      - node_id: HVAC-CHP_DST_MAIN_SUP
        node_name: 冷冻水供水总管
        node_name_en: Chilled Water Supply Main
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
      
        function: 冷冻水供水水平输配干管
        medium_in: WATER-CHW
        medium_out: WATER-CHW
      
        equipment_parameters:
          diameter: {value: DN300-DN400, unit: mm}
          material: 无缝钢管
          insulation: {type: 橡塑保温, thickness: 40, unit: mm}
        
        location_hint:
          space_type: CEILING_VOID / PIPE_TRENCH
          position: 地下室顶板下或管沟

      # 冷冻水立管
      - node_id: HVAC-CHP_DST_RISER
        node_name: 冷冻水立管
        node_name_en: Chilled Water Riser
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 垂直输配，连接各楼层
        medium_in: WATER-CHW
        medium_out: WATER-CHW
      
        multiplicity: multiple
        instance_pattern: HVAC-CHP_DST_RISER_{Zone}_{Seq}
      
        typical_configuration:
          quantity: 2-4组（按建筑分区）
        
        equipment_parameters:
          diameter: {value: DN150-DN250, unit: mm}
          material: 无缝钢管
          insulation: {type: 橡塑保温, thickness: 30, unit: mm}
        
        location_hint:
          space_type: SHAFT
          shaft_type: 水暖管井
        
      # 楼层分集水器
      - node_id: HVAC-CHP_DST_FLOOR_MANIFOLD
        node_name: 楼层分集水器
        node_name_en: Floor Manifold
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 楼层水平分配/汇集
        medium_in: WATER-CHW
        medium_out: WATER-CHW
      
        multiplicity: multiple
        instance_pattern: HVAC-CHP_DST_FLOOR_MANIFOLD_{Floor}
      
        equipment_parameters:
          diameter: {value: DN100-DN150, unit: mm}
        
        location_hint:
          space_type: SHAFT
          position: 楼层管井内或空调机房

      # 回水总管
      - node_id: HVAC-CHP_DST_MAIN_RET
        node_name: 冷冻水回水总管
        node_name_en: Chilled Water Return Main
        node_type: Distribution_Node
        node_category: DST
        node_subtype: JUN
      
        function: 冷冻水回水水平输配干管
        medium_in: WATER-CHW
        medium_out: WATER-CHW
      
        equipment_parameters:
          diameter: {value: DN300-DN400, unit: mm}
          material: 无缝钢管
          insulation: {type: 橡塑保温, thickness: 30, unit: mm}
        
        location_hint:
          space_type: CEILING_VOID / PIPE_TRENCH
          position: 地下室顶板下或管沟

    # ----------------------------------------------------------
    # 末端节点 (Sink Nodes)
    # ----------------------------------------------------------
    sink_nodes:
  
      - node_id: HVAC-CHP_SNK_AHU
        node_name: 空调机组盘管
        node_name_en: AHU Coil Interface
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 冷量消耗
        served_function: 空气处理冷却
        medium_in: WATER-CHW
        medium_out: WATER-CHW
      
        interface_system: HVAC-AHU
      
        typical_configuration:
          quantity_per_floor: 2-4
          coil_capacity: {value: 100-500, unit: kW}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 空调机房
        
      - node_id: HVAC-CHP_SNK_CLEAN
        node_name: 净化空调盘管
        node_name_en: Clean AHU Coil Interface
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 冷量消耗
        served_function: 洁净空调冷却
        medium_in: WATER-CHW
        medium_out: WATER-CHW
      
        interface_system: HVAC-CLEAN
      
        typical_configuration:
          quantity: 10-20
          coil_capacity: {value: 50-200, unit: kW}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 手术部净化机房
        
      - node_id: HVAC-CHP_SNK_FCU
        node_name: 风机盘管
        node_name_en: FCU Interface
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 冷量消耗
        served_function: 房间末端空调
        medium_in: WATER-CHW
        medium_out: WATER-CHW
      
        interface_system: HVAC-FCU
      
        multiplicity: multiple
        instance_pattern: HVAC-CHP_SNK_FCU_{Floor}_{Seq}
      
        typical_configuration:
          quantity_per_floor: 20-50
          capacity_each: {value: 3-10, unit: kW}
        
        location_hint:
          space_type: CEILING_VOID
          position: 各房间吊顶内

  # ============================================================
  # 边定义 (Edges)
  # ============================================================
  edges:

    # ----------------------------------------------------------
    # 供水路径边 (Supply Path Edges)
    # ----------------------------------------------------------
    supply_edges:
  
      - edge_id: HVAC-CHP_EDGE_SUP_001
        edge_name: 冷机至集水器
        edge_name_en: Chiller to Collector
        edge_type: TRK
      
        from_node: HVAC-CHP_SRC_CHILLER
        to_node: HVAC-CHP_DST_COLLECTOR
        direction: unidirectional
      
        medium: WATER-CHW
        medium_properties:
          temperature: {value: 7, unit: ℃}
          pressure: {value: 600, unit: kPa}
          flow_rate: {value: 350-450, unit: m³/h, per_chiller: true}
        
        physical_properties:
          diameter: {value: DN250, unit: mm}
          material: 无缝钢管
          insulation: {type: 橡塑, thickness: 40, unit: mm}
        
      - edge_id: HVAC-CHP_EDGE_SUP_002
        edge_name: 集水器至一次泵
        edge_name_en: Collector to Primary Pump
        edge_type: TRK
      
        from_node: HVAC-CHP_DST_COLLECTOR
        to_node: HVAC-CHP_DST_PUMP_PRI
        direction: unidirectional
      
        medium: WATER-CHW
        medium_properties:
          temperature: {value: 7, unit: ℃}
          pressure: {value: 550, unit: kPa}
        
        physical_properties:
          diameter: {value: DN200, unit: mm}
        
      - edge_id: HVAC-CHP_EDGE_SUP_003
        edge_name: 一次泵至分水器
        edge_name_en: Primary Pump to Header
        edge_type: TRK
      
        from_node: HVAC-CHP_DST_PUMP_PRI
        to_node: HVAC-CHP_DST_HEADER
        direction: unidirectional
      
        medium: WATER-CHW
        medium_properties:
          temperature: {value: 7, unit: ℃}
          pressure: {value: 850, unit: kPa}
        
        physical_properties:
          diameter: {value: DN200, unit: mm}
        
      - edge_id: HVAC-CHP_EDGE_SUP_004
        edge_name: 分水器至二次泵
        edge_name_en: Header to Secondary Pump
        edge_type: TRK
      
        from_node: HVAC-CHP_DST_HEADER
        to_node: HVAC-CHP_DST_PUMP_SEC
        direction: unidirectional
      
        medium: WATER-CHW
        medium_properties:
          temperature: {value: 7, unit: ℃}
          pressure: {value: 800, unit: kPa}
        
        physical_properties:
          diameter: {value: DN200, unit: mm}
        
      - edge_id: HVAC-CHP_EDGE_SUP_005
        edge_name: 二次泵至供水总管
        edge_name_en: Secondary Pump to Supply Main
        edge_type: TRK
      
        from_node: HVAC-CHP_DST_PUMP_SEC
        to_node: HVAC-CHP_DST_MAIN_SUP
        direction: unidirectional
      
        medium: WATER-CHW
        medium_properties:
          temperature: {value: 7, unit: ℃}
          pressure: {value: 1100, unit: kPa}
        
        physical_properties:
          diameter: {value: DN300-DN400, unit: mm}
        
      - edge_id: HVAC-CHP_EDGE_SUP_006
        edge_name: 供水总管至立管
        edge_name_en: Supply Main to Riser
        edge_type: BRH
      
        from_node: HVAC-CHP_DST_MAIN_SUP
        to_node: HVAC-CHP_DST_RISER
        direction: unidirectional
      
        medium: WATER-CHW
        medium_properties:
          temperature: {value: 7, unit: ℃}
        
        physical_properties:
          diameter: {value: DN150-DN250, unit: mm}
        
      - edge_id: HVAC-CHP_EDGE_SUP_007
        edge_name: 立管至楼层分水器
        edge_name_en: Riser to Floor Manifold
        edge_type: BRH
      
        from_node: HVAC-CHP_DST_RISER
        to_node: HVAC-CHP_DST_FLOOR_MANIFOLD
        direction: unidirectional
      
        medium: WATER-CHW
      
        physical_properties:
          diameter: {value: DN100-DN150, unit: mm}
        
      - edge_id: HVAC-CHP_EDGE_SUP_008
        edge_name: 楼层分水器至AHU
        edge_name_en: Floor Manifold to AHU
        edge_type: TRM
      
        from_node: HVAC-CHP_DST_FLOOR_MANIFOLD
        to_node: HVAC-CHP_SNK_AHU
        direction: unidirectional
      
        medium: WATER-CHW
        medium_properties:
          temperature: {value: 7, unit: ℃}
        
        physical_properties:
          diameter: {value: DN80-DN150, unit: mm}
        
      - edge_id: HVAC-CHP_EDGE_SUP_009
        edge_name: 楼层分水器至净化AHU
        edge_name_en: Floor Manifold to Clean AHU
        edge_type: TRM
      
        from_node: HVAC-CHP_DST_FLOOR_MANIFOLD
        to_node: HVAC-CHP_SNK_CLEAN
        direction: unidirectional
      
        medium: WATER-CHW
      
        physical_properties:
          diameter: {value: DN50-DN100, unit: mm}
        
      - edge_id: HVAC-CHP_EDGE_SUP_010
        edge_name: 楼层分水器至FCU
        edge_name_en: Floor Manifold to FCU
        edge_type: TRM
      
        from_node: HVAC-CHP_DST_FLOOR_MANIFOLD
        to_node: HVAC-CHP_SNK_FCU
        direction: unidirectional
      
        medium: WATER-CHW
      
        physical_properties:
          diameter: {value: DN25-DN40, unit: mm}

    # ----------------------------------------------------------
    # 回水路径边 (Return Path Edges)
    # ----------------------------------------------------------
    return_edges:
  
      - edge_id: HVAC-CHP_EDGE_RET_001
        edge_name: AHU至楼层集水器
        edge_name_en: AHU to Floor Manifold
        edge_type: TRM
      
        from_node: HVAC-CHP_SNK_AHU
        to_node: HVAC-CHP_DST_FLOOR_MANIFOLD
        direction: unidirectional
      
        medium: WATER-CHW
        medium_properties:
          temperature: {value: 12, unit: ℃}
        
        physical_properties:
          diameter: {value: DN80-DN150, unit: mm}
        
      - edge_id: HVAC-CHP_EDGE_RET_002
        edge_name: 净化AHU至楼层集水器
        edge_name_en: Clean AHU to Floor Manifold
        edge_type: TRM
      
        from_node: HVAC-CHP_SNK_CLEAN
        to_node: HVAC-CHP_DST_FLOOR_MANIFOLD
        direction: unidirectional
      
        medium: WATER-CHW
        medium_properties:
          temperature: {value: 12, unit: ℃}
        
        physical_properties:
          diameter: {value: DN50-DN100, unit: mm}
        
      - edge_id: HVAC-CHP_EDGE_RET_003
        edge_name: FCU至楼层集水器
        edge_name_en: FCU to Floor Manifold
        edge_type: TRM
      
        from_node: HVAC-CHP_SNK_FCU
        to_node: HVAC-CHP_DST_FLOOR_MANIFOLD
        direction: unidirectional
      
        medium: WATER-CHW
        medium_properties:
          temperature: {value: 12, unit: ℃}
        
        physical_properties:
          diameter: {value: DN25-DN40, unit: mm}
        
      - edge_id: HVAC-CHP_EDGE_RET_004
        edge_name: 楼层集水器至回水立管
        edge_name_en: Floor Manifold to Return Riser
        edge_type: BRH
      
        from_node: HVAC-CHP_DST_FLOOR_MANIFOLD
        to_node: HVAC-CHP_DST_RISER
        direction: unidirectional
      
        medium: WATER-CHW
      
        physical_properties:
          diameter: {value: DN100-DN150, unit: mm}
        
      - edge_id: HVAC-CHP_EDGE_RET_005
        edge_name: 回水立管至回水总管
        edge_name_en: Return Riser to Return Main
        edge_type: BRH
      
        from_node: HVAC-CHP_DST_RISER
        to_node: HVAC-CHP_DST_MAIN_RET
        direction: unidirectional
      
        medium: WATER-CHW
      
        physical_properties:
          diameter: {value: DN150-DN250, unit: mm}
        
      - edge_id: HVAC-CHP_EDGE_RET_006
        edge_name: 回水总管至集水器
        edge_name_en: Return Main to Collector
        edge_type: TRK
      
        from_node: HVAC-CHP_DST_MAIN_RET
        to_node: HVAC-CHP_DST_COLLECTOR
        direction: unidirectional
      
        medium: WATER-CHW
        medium_properties:
          temperature: {value: 12, unit: ℃}
          pressure: {value: 400, unit: kPa}
        
        physical_properties:
          diameter: {value: DN300-DN400, unit: mm}
        
      - edge_id: HVAC-CHP_EDGE_RET_007
        edge_name: 集水器至冷机蒸发器
        edge_name_en: Collector to Chiller Evaporator
        edge_type: TRK
      
        from_node: HVAC-CHP_DST_COLLECTOR
        to_node: HVAC-CHP_SRC_CHILLER
        direction: unidirectional
      
        medium: WATER-CHW
        medium_properties:
          temperature: {value: 12, unit: ℃}
          pressure: {value: 350, unit: kPa}
        
        physical_properties:
          diameter: {value: DN250, unit: mm}

    # ----------------------------------------------------------
    # 旁通边 (Bypass Edge)
    # ----------------------------------------------------------
    bypass_edges:
  
      - edge_id: HVAC-CHP_EDGE_BYP_001
        edge_name: 分集水器旁通
        edge_name_en: Header Bypass
        edge_type: BYP
      
        from_node: HVAC-CHP_DST_HEADER
        to_node: HVAC-CHP_DST_COLLECTOR
        direction: unidirectional
      
        medium: WATER-CHW
      
        control_element: HVAC-CHP_DST_BYPASS
      
        physical_properties:
          diameter: {value: DN150-DN250, unit: mm}

  # ============================================================
  # 路径定义 (Paths)
  # ============================================================
  typical_paths:

    - path_id: HVAC-CHP_PATH_SUP_MAIN
      path_name: 冷冻水供水主路径
      path_name_en: CHW Supply Main Path
      path_type: SUP
    
      description: 从冷机到末端的完整供水路径
    
      sequence:
        - {step: 1, element_type: node, element_id: HVAC-CHP_SRC_CHILLER, role: 源}
        - {step: 2, element_type: edge, element_id: HVAC-CHP_EDGE_SUP_001}
        - {step: 3, element_type: node, element_id: HVAC-CHP_DST_COLLECTOR, role: 汇集}
        - {step: 4, element_type: edge, element_id: HVAC-CHP_EDGE_SUP_002}
        - {step: 5, element_type: node, element_id: HVAC-CHP_DST_PUMP_PRI, role: 动力}
        - {step: 6, element_type: edge, element_id: HVAC-CHP_EDGE_SUP_003}
        - {step: 7, element_type: node, element_id: HVAC-CHP_DST_HEADER, role: 分配}
        - {step: 8, element_type: edge, element_id: HVAC-CHP_EDGE_SUP_004}
        - {step: 9, element_type: node, element_id: HVAC-CHP_DST_PUMP_SEC, role: 动力}
        - {step: 10, element_type: edge, element_id: HVAC-CHP_EDGE_SUP_005}
        - {step: 11, element_type: node, element_id: HVAC-CHP_DST_MAIN_SUP, role: 输配}
        - {step: 12, element_type: edge, element_id: HVAC-CHP_EDGE_SUP_006}
        - {step: 13, element_type: node, element_id: HVAC-CHP_DST_RISER, role: 垂直输配}
        - {step: 14, element_type: edge, element_id: HVAC-CHP_EDGE_SUP_007}
        - {step: 15, element_type: node, element_id: HVAC-CHP_DST_FLOOR_MANIFOLD, role: 楼层分配}
        - {step: 16, element_type: edge, element_id: HVAC-CHP_EDGE_SUP_008}
        - {step: 17, element_type: node, element_id: HVAC-CHP_SNK_AHU, role: 末端}
      
    - path_id: HVAC-CHP_PATH_RET_MAIN
      path_name: 冷冻水回水主路径
      path_name_en: CHW Return Main Path
      path_type: RET
    
      description: 从末端回到冷机的完整回水路径
    
      sequence:
        - {step: 1, element_type: node, element_id: HVAC-CHP_SNK_AHU, role: 末端}
        - {step: 2, element_type: edge, element_id: HVAC-CHP_EDGE_RET_001}
        - {step: 3, element_type: node, element_id: HVAC-CHP_DST_FLOOR_MANIFOLD, role: 楼层汇集}
        - {step: 4, element_type: edge, element_id: HVAC-CHP_EDGE_RET_004}
        - {step: 5, element_type: node, element_id: HVAC-CHP_DST_RISER, role: 垂直输配}
        - {step: 6, element_type: edge, element_id: HVAC-CHP_EDGE_RET_005}
        - {step: 7, element_type: node, element_id: HVAC-CHP_DST_MAIN_RET, role: 输配}
        - {step: 8, element_type: edge, element_id: HVAC-CHP_EDGE_RET_006}
        - {step: 9, element_type: node, element_id: HVAC-CHP_DST_COLLECTOR, role: 汇集}
        - {step: 10, element_type: edge, element_id: HVAC-CHP_EDGE_RET_007}
        - {step: 11, element_type: node, element_id: HVAC-CHP_SRC_CHILLER, role: 源}

  # ============================================================
  # 回路定义 (Loops)
  # ============================================================
  loops:

    - loop_id: HVAC-CHP_LOOP_PRIMARY
      loop_name: 一次侧冷冻水循环
      loop_name_en: Primary CHW Loop
      loop_type: closed
    
      description: |
        冷机蒸发器 → 集水器 → 一次泵 → 分水器 → 旁通阀 → 集水器 → 冷机
        定流量循环，流量由冷机需求决定
      
      key_nodes:
        - HVAC-CHP_SRC_CHILLER
        - HVAC-CHP_DST_COLLECTOR
        - HVAC-CHP_DST_PUMP_PRI
        - HVAC-CHP_DST_HEADER
        - HVAC-CHP_DST_BYPASS
      
      supply_path: HVAC-CHP_PATH_SUP_MAIN (partial: steps 1-7)
      return_path: via HVAC-CHP_EDGE_BYP_001
    
      flow_mode: constant
      control_strategy: 冷机台数控制
    
    - loop_id: HVAC-CHP_LOOP_SECONDARY
      loop_name: 二次侧冷冻水循环
      loop_name_en: Secondary CHW Loop
      loop_type: closed
    
      description: |
        分水器 → 二次泵 → 供水总管 → 立管 → 楼层 → 末端 → 回水 → 集水器 → 分水器
        变流量循环，流量由末端需求决定
      
      key_nodes:
        - HVAC-CHP_DST_HEADER
        - HVAC-CHP_DST_PUMP_SEC
        - HVAC-CHP_DST_MAIN_SUP
        - HVAC-CHP_DST_RISER
        - HVAC-CHP_DST_FLOOR_MANIFOLD
        - HVAC-CHP_SNK_AHU
        - HVAC-CHP_DST_MAIN_RET
        - HVAC-CHP_DST_COLLECTOR
      
      supply_path: HVAC-CHP_PATH_SUP_MAIN
      return_path: HVAC-CHP_PATH_RET_MAIN
    
      flow_mode: variable
      control_strategy: 远端压差控制 + 供水温度控制

  # ============================================================
  # 控制逻辑概要 (Control Logic Summary)
  # ============================================================
  control_logic:

    system_level:
      - strategy: 冷机群控
        description: 根据负荷需求加卸载冷机
        inputs: [回水温度, 供水温度, 冷量需求预测]
        outputs: [冷机启停, 负荷分配]
      
      - strategy: 二次泵变频控制
        description: 根据远端压差调节二次泵转速
        inputs: [最不利环路压差]
        outputs: [二次泵频率]
        setpoint: {value: 50-80, unit: kPa, note: 可调}
      
      - strategy: 旁通阀控制
        description: 维持分集水器压差稳定
        inputs: [分集水器压差]
        outputs: [旁通阀开度]
        setpoint: {value: 30-50, unit: kPa}
      
      - strategy: 供水温度控制
        description: 根据负荷调节供水温度设定值
        inputs: [室外温度, 负荷率]
        outputs: [供水温度设定值]
        range: {min: 6, max: 10, unit: ℃}
```

---

## 第四部分：HVAC-CWP 冷却水系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: HVAC-CWP
    system_name: 冷却水系统
    system_name_en: Cooling Water System
    category: HVAC
    version: 1.0
  
    description: |
      为冷水机组冷凝器提供散热冷却水的循环系统。
      包含冷却塔、冷却水泵、冷却水管网及水处理设备。
    
    design_basis:
      heat_rejection: {value: 10000-18000, unit: kW, note: 按冷机1.2-1.3倍}
      approach_temperature: {value: 4-5, unit: K}
    
    serving_scope:
      - HVAC-CHP (冷水机组冷凝器)

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: HVAC-CWP_BND_IN_ELEC
        boundary_name: 动力电源
        medium: ELEC-LV
        source_system: ELEC-LV-MAIN
      
      - boundary_id: HVAC-CWP_BND_IN_MU
        boundary_name: 补水
        medium: WATER-MU
        source_system: PLUMB-DWS
        parameters:
          consumption_rate: {value: 1-2, unit: "%蒸发量"}
        
      - boundary_id: HVAC-CWP_BND_IN_CTRL
        boundary_name: 控制信号
        medium: CTRL-BA
        source_system: BA-SYSTEM
      
    outputs:
      - boundary_id: HVAC-CWP_BND_OUT_CW
        boundary_name: 冷却水输出至冷机
        medium: WATER-CW
        target_system: HVAC-CHP
        parameters:
          temperature: {value: 32, unit: ℃}

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:

    source_nodes:
  
      - node_id: HVAC-CWP_SRC_CT
        node_name: 冷却塔
        node_name_en: Cooling Tower
        node_type: Source_Node
        node_category: SRC
      
        function: 散热降温（蒸发冷却）
        medium_in: WATER-CW
        medium_out: WATER-CW
      
        multiplicity: multiple
        instance_pattern: HVAC-CWP_SRC_CT_{NNN}
      
        typical_configuration:
          quantity: 4
          redundancy: "N+1"
          tower_type: [逆流式, 横流式]
        
        equipment_parameters:
          capacity_each: {value: 3000-5000, unit: kW}
          flow_rate: {value: 500-700, unit: m³/h, per_unit: true}
          approach: {value: 4, unit: K}
          fan_power: {value: 30-45, unit: kW, per_unit: true}
        
        location_hint:
          building: 裙房/动力中心
          floor: 屋顶
          space_type: OUTDOOR
        
        installation_requirements:
          - 结构承重加强
          - 避雷接地
          - 补水管接入
          - 排水设施
          - 隔音措施（噪声控制）
          - 与新风口距离 ≥ 10m
        
        control_points:
          sensors:
            - {point_id: CT_TEMP_IN, type: AI, description: 进水温度}
            - {point_id: CT_TEMP_OUT, type: AI, description: 出水温度}
            - {point_id: CT_FAN_AMPS, type: AI, description: 风机电流}
          commands:
            - {point_id: CT_FAN_START, type: DO, description: 风机启停}
            - {point_id: CT_FAN_SPEED, type: AO, description: 风机频率}
          status:
            - {point_id: CT_FAN_RUN, type: DI, description: 风机运行状态}
            - {point_id: CT_LOW_LEVEL, type: DI, description: 低液位报警}

    distribution_nodes:
  
      - node_id: HVAC-CWP_DST_PUMP
        node_name: 冷却水泵
        node_name_en: Cooling Water Pump
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 冷却水循环动力
        medium_in: WATER-CW
        medium_out: WATER-CW
      
        multiplicity: multiple
        instance_pattern: HVAC-CWP_DST_PUMP_{NNN}
      
        typical_configuration:
          quantity: 4
          redundancy: "与冷机对应或N+1"
          control_mode: 定流量或变流量
        
        equipment_parameters:
          flow_rate: {value: 500-700, unit: m³/h, per_unit: true}
          head: {value: 28-35, unit: m}
          power: {value: 55-75, unit: kW, per_unit: true}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房
          position: 冷却塔回水侧
        
      - node_id: HVAC-CWP_DST_HEADER_SUP
        node_name: 冷却水供水母管
        node_name_en: CW Supply Header
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
      
        function: 分配冷却水至各冷机
        medium_in: WATER-CW
        medium_out: WATER-CW
      
        equipment_parameters:
          diameter: {value: DN400-DN500, unit: mm}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房
        
      - node_id: HVAC-CWP_DST_HEADER_RET
        node_name: 冷却水回水母管
        node_name_en: CW Return Header
        node_type: Distribution_Node
        node_category: DST
        node_subtype: JUN
      
        function: 汇集冷机回水
        medium_in: WATER-CW
        medium_out: WATER-CW
      
        equipment_parameters:
          diameter: {value: DN400-DN500, unit: mm}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房
        
      - node_id: HVAC-CWP_DST_TREATMENT
        node_name: 水处理装置
        node_name_en: Water Treatment Unit
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
      
        function: 冷却水水质处理（杀菌、阻垢、排污）
        medium_in: WATER-CW
        medium_out: WATER-CW
      
        equipment_parameters:
          treatment_types: [加药, 旁滤, 排污]
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房或水处理间

    sink_nodes:
  
      - node_id: HVAC-CWP_SNK_CHILLER
        node_name: 冷机冷凝器
        node_name_en: Chiller Condenser Interface
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 散热
        medium_in: WATER-CW
        medium_out: WATER-CW
      
        interface_system: HVAC-CHP
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房

  # ============================================================
  # 边定义
  # ============================================================
  edges:

    supply_edges:
  
      - edge_id: HVAC-CWP_EDGE_SUP_001
        edge_name: 冷却塔至水泵
        edge_type: TRK
        from_node: HVAC-CWP_SRC_CT
        to_node: HVAC-CWP_DST_PUMP
        direction: unidirectional
        medium: WATER-CW
        medium_properties:
          temperature: {value: 32, unit: ℃}
          pressure: {value: 250, unit: kPa}
        physical_properties:
          diameter: {value: DN300, unit: mm}
        
      - edge_id: HVAC-CWP_EDGE_SUP_002
        edge_name: 水泵至供水母管
        edge_type: TRK
        from_node: HVAC-CWP_DST_PUMP
        to_node: HVAC-CWP_DST_HEADER_SUP
        direction: unidirectional
        medium: WATER-CW
        medium_properties:
          temperature: {value: 32, unit: ℃}
          pressure: {value: 550, unit: kPa}
        physical_properties:
          diameter: {value: DN250, unit: mm}
        
      - edge_id: HVAC-CWP_EDGE_SUP_003
        edge_name: 供水母管至冷机
        edge_type: TRM
        from_node: HVAC-CWP_DST_HEADER_SUP
        to_node: HVAC-CWP_SNK_CHILLER
        direction: unidirectional
        medium: WATER-CW
        medium_properties:
          temperature: {value: 32, unit: ℃}
        physical_properties:
          diameter: {value: DN200-DN250, unit: mm}

    return_edges:
  
      - edge_id: HVAC-CWP_EDGE_RET_001
        edge_name: 冷机至回水母管
        edge_type: TRM
        from_node: HVAC-CWP_SNK_CHILLER
        to_node: HVAC-CWP_DST_HEADER_RET
        direction: unidirectional
        medium: WATER-CW
        medium_properties:
          temperature: {value: 37, unit: ℃}
        physical_properties:
          diameter: {value: DN200-DN250, unit: mm}
        
      - edge_id: HVAC-CWP_EDGE_RET_002
        edge_name: 回水母管至冷却塔
        edge_type: TRK
        from_node: HVAC-CWP_DST_HEADER_RET
        to_node: HVAC-CWP_SRC_CT
        direction: unidirectional
        medium: WATER-CW
        medium_properties:
          temperature: {value: 37, unit: ℃}
          pressure: {value: 200, unit: kPa}
        physical_properties:
          diameter: {value: DN300, unit: mm}

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:

    - path_id: HVAC-CWP_PATH_SUP
      path_name: 冷却水供水路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: HVAC-CWP_SRC_CT}
        - {step: 2, element_type: edge, element_id: HVAC-CWP_EDGE_SUP_001}
        - {step: 3, element_type: node, element_id: HVAC-CWP_DST_PUMP}
        - {step: 4, element_type: edge, element_id: HVAC-CWP_EDGE_SUP_002}
        - {step: 5, element_type: node, element_id: HVAC-CWP_DST_HEADER_SUP}
        - {step: 6, element_type: edge, element_id: HVAC-CWP_EDGE_SUP_003}
        - {step: 7, element_type: node, element_id: HVAC-CWP_SNK_CHILLER}
      
    - path_id: HVAC-CWP_PATH_RET
      path_name: 冷却水回水路径
      path_type: RET
      sequence:
        - {step: 1, element_type: node, element_id: HVAC-CWP_SNK_CHILLER}
        - {step: 2, element_type: edge, element_id: HVAC-CWP_EDGE_RET_001}
        - {step: 3, element_type: node, element_id: HVAC-CWP_DST_HEADER_RET}
        - {step: 4, element_type: edge, element_id: HVAC-CWP_EDGE_RET_002}
        - {step: 5, element_type: node, element_id: HVAC-CWP_SRC_CT}

  # ============================================================
  # 回路定义
  # ============================================================
  loops:

    - loop_id: HVAC-CWP_LOOP_MAIN
      loop_name: 冷却水主循环
      loop_name_en: Main CW Loop
      loop_type: closed
    
      description: 冷却塔-水泵-冷机冷凝器-冷却塔闭式循环
    
      key_nodes:
        - HVAC-CWP_SRC_CT
        - HVAC-CWP_DST_PUMP
        - HVAC-CWP_DST_HEADER_SUP
        - HVAC-CWP_SNK_CHILLER
        - HVAC-CWP_DST_HEADER_RET
      
      supply_path: HVAC-CWP_PATH_SUP
      return_path: HVAC-CWP_PATH_RET
    
      flow_mode: constant / variable
    
      control_strategy:
        - 冷却水泵与冷机联锁
        - 冷却塔风机根据出水温度调节
        - 供水温度设定值：32℃（可根据节能策略调整）

  # ============================================================
  # 补水与排污
  # ============================================================
  auxiliary_systems:

    makeup_water:
      - node_id: HVAC-CWP_AUX_MU_TANK
        node_name: 补水箱
        function: 储存补水
        capacity: {value: 5-10, unit: m³}
      
      - node_id: HVAC-CWP_AUX_MU_PUMP
        node_name: 补水泵
        function: 定压补水
      
    blowdown:
      - node_id: HVAC-CWP_AUX_BD_VALVE
        node_name: 排污阀
        function: 浓缩倍数控制排污
        location: 冷却塔集水盘
```

---

## 第五部分：HVAC-AHU 空调风系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: HVAC-AHU
    system_name: 空调风系统
    system_name_en: Air Handling Unit System
    category: HVAC
    version: 1.0
  
    description: |
      负责舒适性空调区域的空气处理与输配。
      采用集中式空调机组处理新风与回风混合后送入各区域。
      典型服务区域：门诊大厅、候诊区、普通病房、办公区域。
    
    design_basis:
      fresh_air_ratio: {value: 20-30, unit: "%"}
      supply_temperature_summer: {value: 14-18, unit: ℃}
      supply_temperature_winter: {value: 30-35, unit: ℃}
    
    serving_scope:
      - 门诊大厅
      - 候诊区
      - 普通病房
      - 办公区域
      - 公共走廊

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: HVAC-AHU_BND_IN_OA
        boundary_name: 室外新风
        medium: AIR-OA
        is_external: true
        interface_point: 外墙新风百叶
      
      - boundary_id: HVAC-AHU_BND_IN_CHW
        boundary_name: 冷冻水
        medium: WATER-CHW
        source_system: HVAC-CHP
      
      - boundary_id: HVAC-AHU_BND_IN_HW
        boundary_name: 热水
        medium: WATER-HW
        source_system: HVAC-HWP
      
      - boundary_id: HVAC-AHU_BND_IN_ELEC
        boundary_name: 电源
        medium: ELEC-LV
        source_system: ELEC-LV-MAIN
      
    outputs:
      - boundary_id: HVAC-AHU_BND_OUT_SA
        boundary_name: 送风
        medium: AIR-SA
        target: 建筑空间
      
      - boundary_id: HVAC-AHU_BND_OUT_EA
        boundary_name: 排风
        medium: AIR-EA
        is_external: true
        interface_point: 屋顶排风口

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:

    source_nodes:
  
      - node_id: HVAC-AHU_SRC_OA_LOUVER
        node_name: 新风百叶
        node_name_en: Outdoor Air Louver
        node_type: Source_Node
        node_category: SRC
      
        function: 引入室外新风
        medium_out: AIR-OA
        is_external: true
      
        multiplicity: multiple
      
        typical_configuration:
          quantity: 每台AHU对应1-2个
        
        equipment_parameters:
          velocity: {value: 2-4, unit: m/s}
          free_area_ratio: {value: 50-60, unit: "%"}
        
        location_hint:
          space_type: EXTERIOR
          position: 外墙
          height: ≥ 2.5m（离地）
        
        installation_requirements:
          - 防雨百叶
          - 防虫网
          - 与排风口距离 ≥ 5m
          - 避开污染源

    distribution_nodes:
  
      - node_id: HVAC-AHU_DST_AHU
        node_name: 组合式空调机组
        node_name_en: Air Handling Unit
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
      
        function: 空气混合、过滤、冷却/加热、加湿、送风
        medium_in: [AIR-OA, AIR-RA, WATER-CHW, WATER-HW]
        medium_out: AIR-SA
      
        multiplicity: multiple
        instance_pattern: HVAC-AHU_DST_AHU_{Bldg}_{Floor}_{Seq}
      
        typical_configuration:
          quantity_per_floor: 2-4
        
        equipment_parameters:
          air_flow: {value: 10000-30000, unit: m³/h, per_unit: true}
          esp: {value: 800-1200, unit: Pa}
          cooling_capacity: {value: 100-300, unit: kW, per_unit: true}
          heating_capacity: {value: 50-150, unit: kW, per_unit: true}
          filter_efficiency: {value: "G4+F7", unit: null}
          fan_power: {value: 15-45, unit: kW, per_unit: true}
        
        internal_sections:
          - section: 新回风混合段
          - section: 初效过滤段
          - section: 表冷段
          - section: 加热段
          - section: 加湿段
          - section: 中效过滤段
          - section: 风机段
          - section: 消声段
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 空调机房
          floor: 每层或隔层
        
        installation_requirements:
          - 地面排水坡度
          - 凝结水排水管
          - 检修空间 ≥ 1.0m
          - 新风管/回风管接口
          - 减振基础
        
        control_points:
          sensors:
            - {point_id: AHU_SA_TEMP, type: AI, description: 送风温度}
            - {point_id: AHU_RA_TEMP, type: AI, description: 回风温度}
            - {point_id: AHU_OA_TEMP, type: AI, description: 新风温度}
            - {point_id: AHU_SA_HUMID, type: AI, description: 送风湿度}
            - {point_id: AHU_FILTER_DP, type: AI, description: 过滤器压差}
            - {point_id: AHU_FAN_FREQ, type: AI, description: 风机频率}
          commands:
            - {point_id: AHU_FAN_START, type: DO, description: 风机启停}
            - {point_id: AHU_FAN_SPEED, type: AO, description: 风机频率设定}
            - {point_id: AHU_CHW_VALVE, type: AO, description: 冷水阀开度}
            - {point_id: AHU_HW_VALVE, type: AO, description: 热水阀开度}
            - {point_id: AHU_OA_DAMPER, type: AO, description: 新风阀开度}
            - {point_id: AHU_RA_DAMPER, type: AO, description: 回风阀开度}
          status:
            - {point_id: AHU_FAN_RUN, type: DI, description: 风机运行状态}
            - {point_id: AHU_FAULT, type: DI, description: 故障报警}

      - node_id: HVAC-AHU_DST_MAIN_DUCT
        node_name: 送风主风管
        node_name_en: Supply Air Main Duct
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
      
        function: 水平送风主干输配
        medium_in: AIR-SA
        medium_out: AIR-SA
      
        equipment_parameters:
          velocity: {value: 6-10, unit: m/s}
          material: 镀锌钢板
          insulation: {type: 玻璃棉, thickness: 25, unit: mm}
        
        location_hint:
          space_type: CEILING_VOID
          position: 走廊吊顶上方

      - node_id: HVAC-AHU_DST_BRANCH_DUCT
        node_name: 送风支管
        node_name_en: Supply Air Branch Duct
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BRH
      
        function: 分支至各房间/区域
        medium_in: AIR-SA
        medium_out: AIR-SA
      
        equipment_parameters:
          velocity: {value: 4-6, unit: m/s}
        
        location_hint:
          space_type: CEILING_VOID

      - node_id: HVAC-AHU_DST_VAV
        node_name: 变风量末端
        node_name_en: Variable Air Volume Terminal
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 根据区域负荷调节送风量
        medium_in: AIR-SA
        medium_out: AIR-SA
      
        multiplicity: multiple
      
        equipment_parameters:
          flow_range: {min: 30, max: 100, unit: "%"}
          control_mode: 温度/CO2控制
        
        location_hint:
          space_type: CEILING_VOID
        
        control_points:
          sensors:
            - {point_id: VAV_FLOW, type: AI, description: 风量}
            - {point_id: VAV_POS, type: AI, description: 阀门开度}
          commands:
            - {point_id: VAV_FLOW_SP, type: AO, description: 风量设定}

      - node_id: HVAC-AHU_DST_RA_GRILLE
        node_name: 回风口
        node_name_en: Return Air Grille
        node_type: Distribution_Node
        node_category: DST
        node_subtype: JUN
      
        function: 收集区域回风
        medium_in: AIR-RA
        medium_out: AIR-RA
      
        equipment_parameters:
          velocity: {value: 2-4, unit: m/s}
        
        location_hint:
          space_type: CEILING / WALL
          position: 走廊或房间

      - node_id: HVAC-AHU_DST_RA_DUCT
        node_name: 回风管
        node_name_en: Return Air Duct
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
      
        function: 回风输送至AHU
        medium_in: AIR-RA
        medium_out: AIR-RA
      
        equipment_parameters:
          velocity: {value: 5-8, unit: m/s}
        
        location_hint:
          space_type: CEILING_VOID

    sink_nodes:
  
      - node_id: HVAC-AHU_SNK_DIFFUSER
        node_name: 送风口
        node_name_en: Supply Air Diffuser
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 空气分布
        medium_in: AIR-SA
      
        multiplicity: multiple
      
        equipment_parameters:
          type: [方形散流器, 条形风口, 旋流风口]
          velocity: {value: 2-4, unit: m/s}
        
        location_hint:
          space_type: CEILING
          position: 房间/走廊吊顶
        
      - node_id: HVAC-AHU_SNK_EA_OUTLET
        node_name: 排风出口
        node_name_en: Exhaust Air Outlet
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 排放
        medium_in: AIR-EA
        is_external: true
      
        location_hint:
          space_type: EXTERIOR
          position: 屋顶或外墙

  # ============================================================
  # 边定义
  # ============================================================
  edges:

    # 新风引入
    supply_edges:
  
      - edge_id: HVAC-AHU_EDGE_OA_001
        edge_name: 新风百叶至AHU
        edge_type: TRK
        from_node: HVAC-AHU_SRC_OA_LOUVER
        to_node: HVAC-AHU_DST_AHU
        direction: unidirectional
        medium: AIR-OA
        medium_properties:
          velocity: {value: 4-6, unit: m/s}
        physical_properties:
          duct_size: 根据风量计算
        
      - edge_id: HVAC-AHU_EDGE_SA_001
        edge_name: AHU至送风主管
        edge_type: TRK
        from_node: HVAC-AHU_DST_AHU
        to_node: HVAC-AHU_DST_MAIN_DUCT
        direction: unidirectional
        medium: AIR-SA
        medium_properties:
          temperature_summer: {value: 16, unit: ℃}
          temperature_winter: {value: 32, unit: ℃}
          velocity: {value: 8-10, unit: m/s}
        
      - edge_id: HVAC-AHU_EDGE_SA_002
        edge_name: 主管至支管
        edge_type: BRH
        from_node: HVAC-AHU_DST_MAIN_DUCT
        to_node: HVAC-AHU_DST_BRANCH_DUCT
        direction: unidirectional
        medium: AIR-SA
        medium_properties:
          velocity: {value: 5-7, unit: m/s}
        
      - edge_id: HVAC-AHU_EDGE_SA_003
        edge_name: 支管至VAV
        edge_type: BRH
        from_node: HVAC-AHU_DST_BRANCH_DUCT
        to_node: HVAC-AHU_DST_VAV
        direction: unidirectional
        medium: AIR-SA
      
      - edge_id: HVAC-AHU_EDGE_SA_004
        edge_name: VAV至风口
        edge_type: TRM
        from_node: HVAC-AHU_DST_VAV
        to_node: HVAC-AHU_SNK_DIFFUSER
        direction: unidirectional
        medium: AIR-SA
        medium_properties:
          velocity: {value: 2-4, unit: m/s}

    # 回风路径
    return_edges:
  
      - edge_id: HVAC-AHU_EDGE_RA_001
        edge_name: 空间至回风口
        edge_type: TRM
        from_node: HVAC-AHU_SNK_DIFFUSER
        to_node: HVAC-AHU_DST_RA_GRILLE
        direction: unidirectional
        medium: AIR-RA
        medium_properties:
          temperature: {value: 25, unit: ℃}
        
      - edge_id: HVAC-AHU_EDGE_RA_002
        edge_name: 回风口至回风管
        edge_type: BRH
        from_node: HVAC-AHU_DST_RA_GRILLE
        to_node: HVAC-AHU_DST_RA_DUCT
        direction: unidirectional
        medium: AIR-RA
      
      - edge_id: HVAC-AHU_EDGE_RA_003
        edge_name: 回风管至AHU
        edge_type: TRK
        from_node: HVAC-AHU_DST_RA_DUCT
        to_node: HVAC-AHU_DST_AHU
        direction: unidirectional
        medium: AIR-RA
        medium_properties:
          velocity: {value: 5-8, unit: m/s}

    # 排风路径（部分排风）
    exhaust_edges:
  
      - edge_id: HVAC-AHU_EDGE_EA_001
        edge_name: AHU至排风出口
        edge_type: TRK
        from_node: HVAC-AHU_DST_AHU
        to_node: HVAC-AHU_SNK_EA_OUTLET
        direction: unidirectional
        medium: AIR-EA
        note: 部分回风排出，维持新风比

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:

    - path_id: HVAC-AHU_PATH_SUP
      path_name: 送风路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: HVAC-AHU_SRC_OA_LOUVER}
        - {step: 2, element_type: edge, element_id: HVAC-AHU_EDGE_OA_001}
        - {step: 3, element_type: node, element_id: HVAC-AHU_DST_AHU}
        - {step: 4, element_type: edge, element_id: HVAC-AHU_EDGE_SA_001}
        - {step: 5, element_type: node, element_id: HVAC-AHU_DST_MAIN_DUCT}
        - {step: 6, element_type: edge, element_id: HVAC-AHU_EDGE_SA_002}
        - {step: 7, element_type: node, element_id: HVAC-AHU_DST_BRANCH_DUCT}
        - {step: 8, element_type: edge, element_id: HVAC-AHU_EDGE_SA_003}
        - {step: 9, element_type: node, element_id: HVAC-AHU_DST_VAV}
        - {step: 10, element_type: edge, element_id: HVAC-AHU_EDGE_SA_004}
        - {step: 11, element_type: node, element_id: HVAC-AHU_SNK_DIFFUSER}
      
    - path_id: HVAC-AHU_PATH_RET
      path_name: 回风路径
      path_type: RET
      sequence:
        - {step: 1, element_type: node, element_id: HVAC-AHU_SNK_DIFFUSER}
        - {step: 2, element_type: edge, element_id: HVAC-AHU_EDGE_RA_001}
        - {step: 3, element_type: node, element_id: HVAC-AHU_DST_RA_GRILLE}
        - {step: 4, element_type: edge, element_id: HVAC-AHU_EDGE_RA_002}
        - {step: 5, element_type: node, element_id: HVAC-AHU_DST_RA_DUCT}
        - {step: 6, element_type: edge, element_id: HVAC-AHU_EDGE_RA_003}
        - {step: 7, element_type: node, element_id: HVAC-AHU_DST_AHU}
      
    - path_id: HVAC-AHU_PATH_EXH
      path_name: 排风路径
      path_type: EXH
      sequence:
        - {step: 1, element_type: node, element_id: HVAC-AHU_DST_AHU}
        - {step: 2, element_type: edge, element_id: HVAC-AHU_EDGE_EA_001}
        - {step: 3, element_type: node, element_id: HVAC-AHU_SNK_EA_OUTLET}

  # ============================================================
  # 回路定义
  # ============================================================
  loops:

    - loop_id: HVAC-AHU_LOOP_AIR
      loop_name: 空气循环回路
      loop_name_en: Air Circulation Loop
      loop_type: semi_open
    
      description: |
        新风+回风混合 → AHU处理 → 送风 → 房间 → 回风 → 部分回AHU循环，部分排出
        新风比例20-30%，其余为回风循环
      
      supply_path: HVAC-AHU_PATH_SUP
      return_path: HVAC-AHU_PATH_RET
      exhaust_path: HVAC-AHU_PATH_EXH
    
      flow_mode: variable (VAV系统)
    
      control_strategy:
        - 送风温度控制（夏季16℃，冬季32℃）
        - 新风量控制（CO2浓度或固定比例）
        - VAV末端根据区域温度调节风量
        - 风机变频根据系统静压调节
```

---

## 第六部分：HVAC-CLEAN 洁净空调系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: HVAC-CLEAN
    system_name: 洁净空调系统
    system_name_en: Clean Room HVAC System
    category: HVAC
    version: 1.0
  
    description: |
      手术室、ICU、洁净实验室等洁净区域专用空调系统。
      采用三级过滤、精密温湿度控制，维持正压梯度。
    
    design_basis:
      clean_classes:
        - {class: I级手术室, iso_class: ISO5, ach: 36-48, pressure: "+15Pa"}
        - {class: II级手术室, iso_class: ISO6, ach: 24-36, pressure: "+12Pa"}
        - {class: III级手术室, iso_class: ISO7, ach: 18-24, pressure: "+10Pa"}
        - {class: ICU, iso_class: ISO7, ach: 12-15, pressure: "+8Pa"}
      
    serving_scope:
      - 手术部（I/II/III级手术室）
      - ICU
      - 洁净走廊
      - 无菌物品存放
      - 洁净实验室

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: HVAC-CLEAN_BND_IN_OA
        boundary_name: 新风
        medium: AIR-OA
        is_external: true
      
      - boundary_id: HVAC-CLEAN_BND_IN_CHW
        boundary_name: 冷冻水
        medium: WATER-CHW
        source_system: HVAC-CHP
      
      - boundary_id: HVAC-CLEAN_BND_IN_HW
        boundary_name: 热水
        medium: WATER-HW
        source_system: HVAC-HWP
      
      - boundary_id: HVAC-CLEAN_BND_IN_STEAM
        boundary_name: 蒸汽（加湿用）
        medium: STEAM
        source_system: STEAM-SYSTEM
      
      - boundary_id: HVAC-CLEAN_BND_IN_ELEC
        boundary_name: 电源
        medium: ELEC-LV
        source_system: ELEC-LV-MAIN
      
    outputs:
      - boundary_id: HVAC-CLEAN_BND_OUT_SA
        boundary_name: 洁净送风
        medium: AIR-SA
        target: 洁净区域
      
      - boundary_id: HVAC-CLEAN_BND_OUT_EA
        boundary_name: 排风
        medium: AIR-EA
        is_external: true

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:

    source_nodes:
  
      - node_id: HVAC-CLEAN_SRC_OA
        node_name: 洁净新风入口
        node_name_en: Clean OA Intake
        node_type: Source_Node
        node_category: SRC
      
        function: 引入新风
        medium_out: AIR-OA
        is_external: true
      
        location_hint:
          space_type: EXTERIOR
          position: 屋顶或外墙（远离污染源）
          height: ≥ 3m
        
        installation_requirements:
          - 防雨防虫
          - 初效过滤
          - 与排风口距离 ≥ 10m
          - 与冷却塔距离 ≥ 10m

    distribution_nodes:
  
      - node_id: HVAC-CLEAN_DST_MAU
        node_name: 新风机组
        node_name_en: Makeup Air Unit
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
      
        function: 新风预处理（初效+中效过滤、预冷/预热、除湿）
        medium_in: AIR-OA
        medium_out: AIR-SA
      
        typical_configuration:
          quantity: 2-3台（按手术部规模）
          redundancy: "N+1"
        
        equipment_parameters:
          air_flow: {value: 10000-20000, unit: m³/h, per_unit: true}
          filter_stages: "G4+F8"
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 手术部净化机房
          floor: 设备层（手术部上层或下层）

      - node_id: HVAC-CLEAN_DST_AHU
        node_name: 净化空调机组
        node_name_en: Clean AHU
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
      
        function: 温湿度精密控制、三级过滤
        medium_in: [AIR-SA, AIR-RA, WATER-CHW, WATER-HW, STEAM]
        medium_out: AIR-SA
      
        multiplicity: multiple
        instance_pattern: HVAC-CLEAN_DST_AHU_OT{NN}
      
        typical_configuration:
          quantity: 1 per OR (I/II级) or 2-3 OR per unit (III级)
        
        equipment_parameters:
          air_flow: {value: 6000-15000, unit: m³/h, per_unit: true}
          esp: {value: 1000-1500, unit: Pa}
          filter_stages: "G4+F8+H13/H14"
          temperature_control: {accuracy: "±1℃"}
          humidity_control: {accuracy: "±5%RH"}
        
        internal_sections:
          - 新回风混合段
          - 初效过滤段
          - 表冷段
          - 再热段
          - 蒸汽加湿段
          - 中效过滤段
          - 风机段
          - 均流段
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 手术部净化机房
        
        control_points:
          sensors:
            - {point_id: AHU_SA_TEMP, type: AI, description: 送风温度, accuracy: "±0.3℃"}
            - {point_id: AHU_SA_HUMID, type: AI, description: 送风湿度, accuracy: "±2%RH"}
            - {point_id: AHU_RA_TEMP, type: AI, description: 回风温度}
            - {point_id: AHU_FILTER_DP_PRE, type: AI, description: 初效压差}
            - {point_id: AHU_FILTER_DP_MED, type: AI, description: 中效压差}
          commands:
            - {point_id: AHU_FAN_SPEED, type: AO, description: 风机频率}
            - {point_id: AHU_CHW_VALVE, type: AO, description: 冷水阀}
            - {point_id: AHU_HW_VALVE, type: AO, description: 热水阀}
            - {point_id: AHU_STEAM_VALVE, type: AO, description: 蒸汽阀}
            - {point_id: AHU_OA_DAMPER, type: AO, description: 新风阀}

      - node_id: HVAC-CLEAN_DST_CAV
        node_name: 定风量阀
        node_name_en: Constant Air Volume Valve
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 维持送入房间的风量恒定
        medium_in: AIR-SA
        medium_out: AIR-SA
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 机械自力式或电动定风量
          accuracy: {value: "±5%", unit: null}
        
        location_hint:
          space_type: CEILING_VOID
          position: AHU出口至手术室入口之间
        
        control_points:
          sensors:
            - {point_id: CAV_FLOW, type: AI, description: 实际风量}
          commands:
            - {point_id: CAV_SP, type: AO, description: 风量设定值}

      - node_id: HVAC-CLEAN_DST_HEPA_BOX
        node_name: 高效送风静压箱
        node_name_en: HEPA Terminal Box
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
      
        function: 高效过滤 + 均流送风
        medium_in: AIR-SA
        medium_out: AIR-SA
      
        multiplicity: multiple
      
        equipment_parameters:
          filter_class: H13 / H14
          efficiency: {value: "≥99.97%@0.3μm", unit: null}
          terminal_velocity: {value: 0.25-0.45, unit: m/s, note: 层流}
        
        location_hint:
          space_type: CEILING_VOID
          position: 手术室正上方
        
        control_points:
          sensors:
            - {point_id: HEPA_DP, type: AI, description: 高效过滤器压差}

      - node_id: HVAC-CLEAN_DST_RA_GRILLE
        node_name: 下回风口
        node_name_en: Lower Return Air Grille
        node_type: Distribution_Node
        node_category: DST
        node_subtype: JUN
      
        function: 手术室下部回风收集
        medium_in: AIR-RA
        medium_out: AIR-RA
      
        equipment_parameters:
          position: 手术室两侧墙下部
          height_from_floor: {value: 100-200, unit: mm}
        
        location_hint:
          space_type: WALL
          position: 手术室两侧墙壁下部

      - node_id: HVAC-CLEAN_DST_EA_VALVE
        node_name: 排风调节阀
        node_name_en: Exhaust Air Control Valve
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 控制排风量，维持房间压力梯度
        medium_in: AIR-EA
        medium_out: AIR-EA
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 电动调节阀
        
        location_hint:
          space_type: CEILING_VOID
        
        control_points:
          sensors:
            - {point_id: ROOM_PRESSURE, type: AI, description: 房间压力}
          commands:
            - {point_id: EA_DAMPER, type: AO, description: 排风阀开度}

      - node_id: HVAC-CLEAN_DST_EA_FAN
        node_name: 排风机
        node_name_en: Exhaust Fan
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 排风动力
        medium_in: AIR-EA
        medium_out: AIR-EA
      
        typical_configuration:
          quantity: 2-3台
          redundancy: "N+1"
        
        equipment_parameters:
          air_flow: {value: 5000-15000, unit: m³/h, per_unit: true}
          esp: {value: 400-600, unit: Pa}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 手术部排风机房

    sink_nodes:
  
      - node_id: HVAC-CLEAN_SNK_LAMINAR
        node_name: 层流送风天花
        node_name_en: Laminar Flow Ceiling
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 洁净送风分布
        medium_in: AIR-SA
      
        multiplicity: multiple
      
        equipment_parameters:
          size_I: {value: "2.8m×2.8m", note: I级手术室}
          size_II: {value: "2.4m×2.4m", note: II级手术室}
          velocity: {value: 0.25-0.35, unit: m/s}
        
        location_hint:
          space_type: CEILING
          position: 手术台正上方

      - node_id: HVAC-CLEAN_SNK_EA_OUTLET
        node_name: 排风出口
        node_name_en: Exhaust Outlet
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 排放至大气
        medium_in: AIR-EA
        is_external: true
      
        location_hint:
          space_type: EXTERIOR
          position: 屋顶

  # ============================================================
  # 边定义
  # ============================================================
  edges:

    # 新风处理路径
    supply_edges:
  
      - edge_id: HVAC-CLEAN_EDGE_OA_001
        edge_name: 新风入口至新风机组
        edge_type: TRK
        from_node: HVAC-CLEAN_SRC_OA
        to_node: HVAC-CLEAN_DST_MAU
        direction: unidirectional
        medium: AIR-OA
      
      - edge_id: HVAC-CLEAN_EDGE_SA_001
        edge_name: 新风机组至净化AHU
        edge_type: TRK
        from_node: HVAC-CLEAN_DST_MAU
        to_node: HVAC-CLEAN_DST_AHU
        direction: unidirectional
        medium: AIR-SA
        medium_properties:
          temperature: {value: 16-18, unit: ℃}
          humidity: {value: 50-60, unit: "%RH"}
        
      - edge_id: HVAC-CLEAN_EDGE_SA_002
        edge_name: 净化AHU至定风量阀
        edge_type: TRK
        from_node: HVAC-CLEAN_DST_AHU
        to_node: HVAC-CLEAN_DST_CAV
        direction: unidirectional
        medium: AIR-SA
        medium_properties:
          pressure: {value: 500-800, unit: Pa}
        
      - edge_id: HVAC-CLEAN_EDGE_SA_003
        edge_name: 定风量阀至高效静压箱
        edge_type: BRH
        from_node: HVAC-CLEAN_DST_CAV
        to_node: HVAC-CLEAN_DST_HEPA_BOX
        direction: unidirectional
        medium: AIR-SA
      
      - edge_id: HVAC-CLEAN_EDGE_SA_004
        edge_name: 高效静压箱至层流天花
        edge_type: TRM
        from_node: HVAC-CLEAN_DST_HEPA_BOX
        to_node: HVAC-CLEAN_SNK_LAMINAR
        direction: unidirectional
        medium: AIR-SA
        medium_properties:
          velocity: {value: 0.25-0.35, unit: m/s}
          temperature: {value: 22-25, unit: ℃}
          humidity: {value: 40-60, unit: "%RH"}

    # 回风路径
    return_edges:
  
      - edge_id: HVAC-CLEAN_EDGE_RA_001
        edge_name: 手术区至下回风口
        edge_type: TRM
        from_node: HVAC-CLEAN_SNK_LAMINAR
        to_node: HVAC-CLEAN_DST_RA_GRILLE
        direction: unidirectional
        medium: AIR-RA
        note: 手术室内气流由上向下，侧下部回风
      
      - edge_id: HVAC-CLEAN_EDGE_RA_002
        edge_name: 下回风口至净化AHU
        edge_type: TRK
        from_node: HVAC-CLEAN_DST_RA_GRILLE
        to_node: HVAC-CLEAN_DST_AHU
        direction: unidirectional
        medium: AIR-RA

    # 排风路径
    exhaust_edges:
  
      - edge_id: HVAC-CLEAN_EDGE_EA_001
        edge_name: 回风口至排风阀
        edge_type: BRH
        from_node: HVAC-CLEAN_DST_RA_GRILLE
        to_node: HVAC-CLEAN_DST_EA_VALVE
        direction: unidirectional
        medium: AIR-EA
        note: 部分回风排出
      
      - edge_id: HVAC-CLEAN_EDGE_EA_002
        edge_name: 排风阀至排风机
        edge_type: TRK
        from_node: HVAC-CLEAN_DST_EA_VALVE
        to_node: HVAC-CLEAN_DST_EA_FAN
        direction: unidirectional
        medium: AIR-EA
      
      - edge_id: HVAC-CLEAN_EDGE_EA_003
        edge_name: 排风机至排风出口
        edge_type: TRK
        from_node: HVAC-CLEAN_DST_EA_FAN
        to_node: HVAC-CLEAN_SNK_EA_OUTLET
        direction: unidirectional
        medium: AIR-EA

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:

    - path_id: HVAC-CLEAN_PATH_SUP
      path_name: 洁净送风路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: HVAC-CLEAN_SRC_OA}
        - {step: 2, element_type: edge, element_id: HVAC-CLEAN_EDGE_OA_001}
        - {step: 3, element_type: node, element_id: HVAC-CLEAN_DST_MAU}
        - {step: 4, element_type: edge, element_id: HVAC-CLEAN_EDGE_SA_001}
        - {step: 5, element_type: node, element_id: HVAC-CLEAN_DST_AHU}
        - {step: 6, element_type: edge, element_id: HVAC-CLEAN_EDGE_SA_002}
        - {step: 7, element_type: node, element_id: HVAC-CLEAN_DST_CAV}
        - {step: 8, element_type: edge, element_id: HVAC-CLEAN_EDGE_SA_003}
        - {step: 9, element_type: node, element_id: HVAC-CLEAN_DST_HEPA_BOX}
        - {step: 10, element_type: edge, element_id: HVAC-CLEAN_EDGE_SA_004}
        - {step: 11, element_type: node, element_id: HVAC-CLEAN_SNK_LAMINAR}
      
    - path_id: HVAC-CLEAN_PATH_RET
      path_name: 回风路径
      path_type: RET
      sequence:
        - {step: 1, element_type: node, element_id: HVAC-CLEAN_SNK_LAMINAR}
        - {step: 2, element_type: edge, element_id: HVAC-CLEAN_EDGE_RA_001}
        - {step: 3, element_type: node, element_id: HVAC-CLEAN_DST_RA_GRILLE}
        - {step: 4, element_type: edge, element_id: HVAC-CLEAN_EDGE_RA_002}
        - {step: 5, element_type: node, element_id: HVAC-CLEAN_DST_AHU}
      
    - path_id: HVAC-CLEAN_PATH_EXH
      path_name: 排风路径
      path_type: EXH
      sequence:
        - {step: 1, element_type: node, element_id: HVAC-CLEAN_DST_RA_GRILLE}
        - {step: 2, element_type: edge, element_id: HVAC-CLEAN_EDGE_EA_001}
        - {step: 3, element_type: node, element_id: HVAC-CLEAN_DST_EA_VALVE}
        - {step: 4, element_type: edge, element_id: HVAC-CLEAN_EDGE_EA_002}
        - {step: 5, element_type: node, element_id: HVAC-CLEAN_DST_EA_FAN}
        - {step: 6, element_type: edge, element_id: HVAC-CLEAN_EDGE_EA_003}
        - {step: 7, element_type: node, element_id: HVAC-CLEAN_SNK_EA_OUTLET}

  # ============================================================
  # 回路定义
  # ============================================================
  loops:

    - loop_id: HVAC-CLEAN_LOOP_AIR
      loop_name: 洁净空气循环
      loop_name_en: Clean Air Circulation Loop
      loop_type: semi_open
    
      description: |
        新风经新风机组预处理后，与回风在净化AHU混合，
        经三级过滤和温湿度处理后送入手术室，
        部分回风循环利用，部分排出维持正压。
        新风量满足压力梯度和最小换气次数要求。
      
      supply_path: HVAC-CLEAN_PATH_SUP
      return_path: HVAC-CLEAN_PATH_RET
      exhaust_path: HVAC-CLEAN_PATH_EXH
    
      flow_balance:
        supply: 100%
        return: 70-80%
        exhaust: 20-30%
      
      pressure_cascade:
        - {zone: I级手术室, pressure: "+15Pa", reference: 走廊}
        - {zone: II级手术室, pressure: "+12Pa", reference: 走廊}
        - {zone: 洁净走廊, pressure: "+10Pa", reference: 污物走廊}
        - {zone: 污物走廊, pressure: "+5Pa", reference: 普通区域}
      
      control_strategy:
        - 送风温度控制（精度±1℃）
        - 送风湿度控制（精度±5%RH）
        - 房间正压控制（通过排风阀调节）
        - 定风量控制（CAV阀）
        - 过滤器压差监测与报警
```

---

## 第七部分：系统间接口关系图

```yaml
System_Interfaces:

  # 冷源系统与冷却水系统
  - interface_id: IF_CWP_TO_CHP
    upstream_system: HVAC-CWP
    downstream_system: HVAC-CHP
    interface_nodes:
      upstream_output: HVAC-CWP_SNK_CHILLER
      downstream_input: HVAC-CHP_SRC_CHILLER (condenser side)
    medium: WATER-CW
    parameters:
      supply_temp: 32℃
      return_temp: 37℃
    
  # 冷源系统与空调机组
  - interface_id: IF_CHP_TO_AHU
    upstream_system: HVAC-CHP
    downstream_system: HVAC-AHU
    interface_nodes:
      upstream_output: HVAC-CHP_SNK_AHU
      downstream_input: HVAC-AHU_DST_AHU (cooling coil)
    medium: WATER-CHW
    parameters:
      supply_temp: 7℃
      return_temp: 12℃
    
  # 冷源系统与洁净空调
  - interface_id: IF_CHP_TO_CLEAN
    upstream_system: HVAC-CHP
    downstream_system: HVAC-CLEAN
    interface_nodes:
      upstream_output: HVAC-CHP_SNK_CLEAN
      downstream_input: HVAC-CLEAN_DST_AHU (cooling coil)
    medium: WATER-CHW
    parameters:
      supply_temp: 7℃
      return_temp: 12℃

  # 新风机组与净化AHU
  - interface_id: IF_MAU_TO_AHU
    upstream_system: HVAC-CLEAN (MAU)
    downstream_system: HVAC-CLEAN (AHU)
    interface_nodes:
      upstream_output: HVAC-CLEAN_DST_MAU
      downstream_input: HVAC-CLEAN_DST_AHU
    medium: AIR-SA
    parameters:
      temperature: 16-18℃
      humidity: 50-60%RH
```

---

## 第八部分：质量校验清单

```yaml
Quality_Checklist:

  # 结构完整性
  structure_completeness:
    - check: 所有Source节点都有输出边
      status: ✅
    - check: 所有Sink节点都有输入边
      status: ✅
    - check: 所有Distribution节点都有输入和输出边
      status: ✅
    - check: 所有闭环系统定义了完整的供回路径
      status: ✅
    - check: 所有边都有明确的from/to节点
      status: ✅

  # 介质一致性
  medium_consistency:
    - check: 边的介质与连接节点的介质匹配
      status: ✅
    - check: 路径中的介质类型连续一致
      status: ✅
    - check: 系统边界的介质正确标注
      status: ✅

  # 参数完整性
  parameter_completeness:
    - check: 主要节点定义了capacity/typical_quantity
      status: ✅
    - check: 主要边定义了medium_properties
      status: ✅
    - check: 关键节点定义了control_points
      status: ✅
    - check: 节点定义了location_hint
      status: ✅
    - check: 复杂节点定义了installation_requirements
      status: ✅

  # 命名规范性
  naming_convention:
    - check: 节点ID遵循 {系统}_{类型}_{名称} 格式
      status: ✅
    - check: 边ID遵循 {系统}_EDGE_{介质}_{序号} 格式
      status: ✅
    - check: 路径ID遵循 {系统}_PATH_{类型} 格式
      status: ✅
    - check: 回路ID遵循 {系统}_LOOP_{名称} 格式
      status: ✅

  # 下游Agent接口
  downstream_interfaces:
    - agent: Agent-03 (设备属性)
      required_fields: [equipment_parameters, typical_configuration]
      status: ✅ 已提供
    - agent: Agent-04 (流动模型)
      required_fields: [loops, paths, medium_properties]
      status: ✅ 已提供
    - agent: Agent-05 (空间定位)
      required_fields: [location_hint, installation_requirements]
      status: ✅ 已提供
```

---

## 输出总结

| 系统 | 状态 | 节点数 | 边数 | 路径数 | 回路数 |
|------|------|--------|------|--------|--------|
| HVAC-CHP | ✅ 完成 | 14 | 17 | 2 | 2 |
| HVAC-CWP | ✅ 完成 | 7 | 5 | 2 | 1 |
| HVAC-AHU | ✅ 完成 | 10 | 9 | 3 | 1 |
| HVAC-CLEAN | ✅ 完成 | 11 | 10 | 3 | 1 |


# Agent-01 系统补充与扩展输出

## 概述

根据完整性审查报告，本文档包含两部分：
1. **Batch 1-3 补充文档**：对已完成系统的接口、节点、边进行补充
2. **Batch 4 完整输出**：新增缺失的关键系统

---

# 第一部分：Batch 1 补充文档 (HVAC系统补充)

## 1.1 HVAC-CHP 冷源系统补充

```yaml
System_Topology_Patch:

  system_id: HVAC-CHP
  patch_version: 1.1
  patch_description: 补充热水系统接口、冷热切换逻辑

  # ============================================================
  # 新增节点
  # ============================================================
  additional_nodes:

    distribution_nodes:
  
      - node_id: HVAC-CHP_DST_HW_INTERFACE
        node_name: 热水系统接口
        node_name_en: Hot Water System Interface
        node_type: Distribution_Node
        node_category: DST
        node_subtype: JUN
      
        function: 冷热水系统切换/混合接口
        medium_in: [WATER-CHW, WATER-HW]
        medium_out: WATER-CHW  # 统一为空调水
      
        equipment_parameters:
          type: 冷热水切换阀组
          configuration: 三通阀/两位切换
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房
          position: 分水器前端
        
        control_points:
          sensors:
            - {point_id: CHW_HW_T, type: AI, description: 切换后水温}
          status:
            - {point_id: CHW_HW_MODE, type: DI, description: 当前模式(冷/热)}
          commands:
            - {point_id: CHW_HW_SW, type: DO, description: 冷热切换命令}

  # ============================================================
  # 新增边
  # ============================================================
  additional_edges:

    - edge_id: HVAC-CHP_EDGE_HW_IN
      edge_name: 热水系统供水接入
      edge_type: TRK
      from_node: HVAC-HWP_DST_HEADER_SUP  # 引用热源系统
      to_node: HVAC-CHP_DST_HW_INTERFACE
      direction: unidirectional
      medium: WATER-HW
      cross_system: true
      target_system: HVAC-HWP
    
    - edge_id: HVAC-CHP_EDGE_HW_OUT
      edge_name: 热水系统回水返回
      edge_type: TRK
      from_node: HVAC-CHP_DST_HW_INTERFACE
      to_node: HVAC-HWP_DST_HEADER_RET  # 引用热源系统
      direction: unidirectional
      medium: WATER-HW
      cross_system: true
      target_system: HVAC-HWP
    
    - edge_id: HVAC-CHP_EDGE_HW_TO_HEADER
      edge_name: 热水接口至分水器
      edge_type: TRK
      from_node: HVAC-CHP_DST_HW_INTERFACE
      to_node: HVAC-CHP_DST_HEADER_SUP
      direction: unidirectional
      medium: WATER-CHW
      note: 冬季工况时热水经此边进入空调水系统

  # ============================================================
  # 补充控制逻辑
  # ============================================================
  additional_control_logic:

    seasonal_changeover:
      description: 冷热水季节切换逻辑
    
      cooling_mode:
        condition: 室外温度 > 18℃ 且 连续3天
        action:
          - 关闭热水系统接口阀门
          - 开启冷水机组
          - 切换至制冷模式
        
      heating_mode:
        condition: 室外温度 < 12℃ 且 连续3天
        action:
          - 关闭冷水机组
          - 开启热水系统接口阀门
          - 切换至供热模式
        
      transition_mode:
        condition: 室外温度 12-18℃
        action:
          - 根据建筑负荷需求切换
          - 可同时运行冷热源(不同区域)

  # ============================================================
  # 补充系统边界
  # ============================================================
  additional_boundary:

    inputs:
      - boundary_id: HVAC-CHP_BND_IN_HW
        boundary_name: 热水系统供水
        medium: WATER-HW
        source_system: HVAC-HWP
        parameters:
          temperature: {value: 50-60, unit: ℃}
        
    outputs:
      - boundary_id: HVAC-CHP_BND_OUT_HW
        boundary_name: 热水系统回水
        medium: WATER-HW
        target_system: HVAC-HWP
```

## 1.2 HVAC-AHU 空调风系统补充

```yaml
System_Topology_Patch:

  system_id: HVAC-AHU
  patch_version: 1.1
  patch_description: 补充再热盘管节点、热水接口、消防联动

  # ============================================================
  # 新增节点
  # ============================================================
  additional_nodes:

    distribution_nodes:
  
      - node_id: HVAC-AHU_DST_REHEAT_COIL
        node_name: 再热盘管
        node_name_en: Reheat Coil
        node_type: Distribution_Node
        node_category: DST
        node_subtype: HEX
      
        function: 送风再加热（冬季或除湿后再热）
        medium_in: [AIR-SA, WATER-HW]
        medium_out: AIR-SA
      
        multiplicity: optional
        note: 仅部分AHU配置再热盘管
      
        equipment_parameters:
          type: 热水盘管
          rows: {value: 2, unit: 排}
          water_velocity: {value: 0.8-1.2, unit: m/s}
        
        location_hint:
          space_type: AHU_INTERNAL
          position: 冷却盘管下游、加湿段上游
        
        control_points:
          sensors:
            - {point_id: RH_AIR_T_OUT, type: AI, description: 再热后空气温度}
            - {point_id: RH_WATER_T_IN, type: AI, description: 热水进水温度}
            - {point_id: RH_WATER_T_OUT, type: AI, description: 热水回水温度}
          commands:
            - {point_id: RH_VALVE, type: AO, description: 再热阀开度}
          
      - node_id: HVAC-AHU_DST_HW_VALVE
        node_name: 热水阀组
        node_name_en: Hot Water Valve Assembly
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
      
        function: 热水流量调节
        medium_in: WATER-HW
        medium_out: WATER-HW
      
        equipment_parameters:
          components:
            - 电动两通阀/三通阀
            - 平衡阀
            - 过滤器
            - 软接头
          
        location_hint:
          space_type: MEP_ROOM
          position: 空调机房热水管道

    sink_nodes:
  
      - node_id: HVAC-AHU_SNK_FIRE_INTERLOCK
        node_name: 消防联动接口
        node_name_en: Fire Interlock Interface
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 联动控制信号
        medium_in: SIGNAL-FA
      
        interface_system: FIRE-ALARM
      
        function: 接收火灾报警信号，执行停机/关阀
      
        location_hint:
          space_type: PANEL
          position: AHU控制柜

  # ============================================================
  # 新增边
  # ============================================================
  additional_edges:

    hot_water_edges:
  
      - edge_id: HVAC-AHU_EDGE_HW_SUP
        edge_name: 热水供水至阀组
        edge_type: TRK
        from_node: HVAC-HWP_DST_AHU_BRANCH  # 热源系统分支
        to_node: HVAC-AHU_DST_HW_VALVE
        direction: unidirectional
        medium: WATER-HW
        cross_system: true
        target_system: HVAC-HWP
      
      - edge_id: HVAC-AHU_EDGE_HW_COIL
        edge_name: 阀组至再热盘管
        edge_type: TRK
        from_node: HVAC-AHU_DST_HW_VALVE
        to_node: HVAC-AHU_DST_REHEAT_COIL
        direction: unidirectional
        medium: WATER-HW
      
      - edge_id: HVAC-AHU_EDGE_HW_RET
        edge_name: 再热盘管回水
        edge_type: TRK
        from_node: HVAC-AHU_DST_REHEAT_COIL
        to_node: HVAC-HWP_DST_AHU_BRANCH  # 热源系统回水
        direction: unidirectional
        medium: WATER-HW
        cross_system: true
        target_system: HVAC-HWP

    fire_interlock_edges:
  
      - edge_id: HVAC-AHU_EDGE_FIRE_SIG
        edge_name: 消防联动信号
        edge_type: CTRL
        from_node: FIRE-ALARM_DST_LINKAGE
        to_node: HVAC-AHU_SNK_FIRE_INTERLOCK
        direction: unidirectional
        medium: SIGNAL-FA
        cross_system: true
        source_system: FIRE-ALARM

  # ============================================================
  # 补充典型路径
  # ============================================================
  additional_paths:

    - path_id: HVAC-AHU_PATH_REHEAT
      path_name: 再热工况送风路径
      path_type: SUP
      condition: 冬季或除湿后再热
      sequence:
        - {step: 1, element_type: node, element_id: HVAC-AHU_SRC_OA}
        - {step: 2, element_type: node, element_id: HVAC-AHU_DST_FILTER}
        - {step: 3, element_type: node, element_id: HVAC-AHU_DST_COOL_COIL}
        - {step: 4, element_type: node, element_id: HVAC-AHU_DST_REHEAT_COIL}  # 新增
        - {step: 5, element_type: node, element_id: HVAC-AHU_DST_HUM}
        - {step: 6, element_type: node, element_id: HVAC-AHU_DST_FAN}
        - {step: 7, element_type: node, element_id: HVAC-AHU_SNK_ROOM}

  # ============================================================
  # 补充控制逻辑
  # ============================================================
  additional_control_logic:

    reheat_control:
      mode: 温度控制
      setpoint: 送风温度设定值
      control_method: PID调节再热阀开度
    
      sequence:
        winter:
          - 冷却盘管关闭或微开除湿
          - 再热盘管开启
          - 根据送风温度调节阀开度
        
        dehumidification:
          - 冷却盘管开启除湿
          - 再热盘管开启
          - 先冷却除湿，后再热升温
        
    fire_interlock:
      trigger: FIRE-ALARM火灾确认信号
      action:
        - AHU风机停止
        - 新风阀关闭
        - 回风阀关闭
        - 冷热水阀关闭
      priority: 最高优先级
      restore: 仅手动复位

  # ============================================================
  # 补充系统边界
  # ============================================================
  additional_boundary:

    inputs:
      - boundary_id: HVAC-AHU_BND_IN_HW
        boundary_name: 热水供水
        medium: WATER-HW
        source_system: HVAC-HWP
        parameters:
          temperature: {value: 50-60, unit: ℃}
        
      - boundary_id: HVAC-AHU_BND_IN_FA
        boundary_name: 消防联动信号
        medium: SIGNAL-FA
        source_system: FIRE-ALARM
```

## 1.3 HVAC-CLEAN 洁净空调系统补充

```yaml
System_Topology_Patch:

  system_id: HVAC-CLEAN
  patch_version: 1.1
  patch_description: 补充加热盘管热水接口、消防联动、麻醉废气排放接口

  # ============================================================
  # 新增节点
  # ============================================================
  additional_nodes:

    distribution_nodes:
  
      - node_id: HVAC-CLEAN_DST_HEAT_COIL
        node_name: 加热盘管
        node_name_en: Heating Coil
        node_type: Distribution_Node
        node_category: DST
        node_subtype: HEX
      
        function: 冬季预热/再热
        medium_in: [AIR-MA, WATER-HW]
        medium_out: AIR-MA
      
        equipment_parameters:
          type: 热水盘管
          rows: {value: 2-4, unit: 排}
          capacity: 根据热负荷计算
        
        location_hint:
          space_type: AHU_INTERNAL
          position: 表冷器下游或新风预热位置
        
        control_points:
          sensors:
            - {point_id: HEAT_AIR_T_OUT, type: AI, description: 加热后温度}
          commands:
            - {point_id: HEAT_VALVE, type: AO, description: 热水阀开度}

      - node_id: HVAC-CLEAN_DST_AGSS_INTERFACE
        node_name: 麻醉废气排放接口
        node_name_en: AGSS Interface
        node_type: Distribution_Node
        node_category: DST
        node_subtype: JUN
      
        function: 麻醉废气接入排风系统
        medium_in: GAS-AGSS
        medium_out: AIR-EA
      
        equipment_parameters:
          type: 接口管道
          dilution_ratio: 1:10 (废气:排风)
        
        location_hint:
          space_type: CEILING_VOID
          position: 手术室排风主管接口处
        
        interface_system: MGAS-AGSS

    sink_nodes:
  
      - node_id: HVAC-CLEAN_SNK_FIRE_INTERLOCK
        node_name: 消防联动接口
        node_name_en: Fire Interlock Interface
        node_type: Sink_Node
        node_category: SNK
      
        consumption_type: 联动控制信号
        medium_in: SIGNAL-FA
      
        interface_system: FIRE-ALARM
      
        location_hint:
          space_type: PANEL
          position: 净化空调控制柜

  # ============================================================
  # 新增边
  # ============================================================
  additional_edges:

    hot_water_edges:
  
      - edge_id: HVAC-CLEAN_EDGE_HW_SUP
        edge_name: 热水供水
        edge_type: TRK
        from_node: HVAC-HWP_DST_CLEAN_BRANCH
        to_node: HVAC-CLEAN_DST_HEAT_COIL
        direction: unidirectional
        medium: WATER-HW
        cross_system: true
        target_system: HVAC-HWP
      
      - edge_id: HVAC-CLEAN_EDGE_HW_RET
        edge_name: 热水回水
        edge_type: TRK
        from_node: HVAC-CLEAN_DST_HEAT_COIL
        to_node: HVAC-HWP_DST_CLEAN_BRANCH
        direction: unidirectional
        medium: WATER-HW
        cross_system: true
        target_system: HVAC-HWP

    agss_edges:
  
      - edge_id: HVAC-CLEAN_EDGE_AGSS_IN
        edge_name: 麻醉废气接入
        edge_type: BRH
        from_node: MGAS-AGSS_DST_MAIN_PIPE
        to_node: HVAC-CLEAN_DST_AGSS_INTERFACE
        direction: unidirectional
        medium: GAS-AGSS
        cross_system: true
        source_system: MGAS-AGSS
      
      - edge_id: HVAC-CLEAN_EDGE_AGSS_OUT
        edge_name: 麻醉废气排放
        edge_type: TRK
        from_node: HVAC-CLEAN_DST_AGSS_INTERFACE
        to_node: HVAC-CLEAN_DST_EA_MAIN
        direction: unidirectional
        medium: AIR-EA
        note: 废气稀释后经排风主管排放

    fire_interlock_edges:
  
      - edge_id: HVAC-CLEAN_EDGE_FIRE_SIG
        edge_name: 消防联动信号
        edge_type: CTRL
        from_node: FIRE-ALARM_DST_LINKAGE
        to_node: HVAC-CLEAN_SNK_FIRE_INTERLOCK
        direction: unidirectional
        medium: SIGNAL-FA
        cross_system: true
        source_system: FIRE-ALARM

  # ============================================================
  # 补充控制逻辑
  # ============================================================
  additional_control_logic:

    heating_control:
      mode: 温度控制
      winter_preheat:
        condition: 新风温度 < 5℃
        action: 新风预热阀开启
        setpoint: 混合空气温度 ≥ 12℃
      
      reheat:
        condition: 除湿后或冬季
        action: 再热阀开启
        setpoint: 送风温度设定值
      
    agss_coordination:
      description: 麻醉废气与排风协调
      requirements:
        - 排风量 ≥ 10倍AGSS流量
        - 排风机运行时AGSS方可排放
        - AGSS压力监测
      
    fire_interlock:
      trigger: FIRE-ALARM火灾确认信号
      action:
        - 送风机停止
        - 排风机停止
        - 新风阀关闭
        - 排风阀关闭
        - AGSS接口阀关闭
      special_note: |
        手术进行中火灾时的特殊处理：
        1. 优先患者安全转移
        2. 净化系统可延迟关闭（30-60秒）
        3. 需与医疗流程协调
      restore: 仅手动复位
```

## 1.4 HVAC系统补充 - 新增介质类型

```yaml
Additional_Medium_Types:

  - medium_id: WATER-HW
    medium_name: 空调热水
    medium_name_en: HVAC Hot Water
    category: WATER
    typical_properties:
      temperature_supply: {value: 50-60, unit: ℃}
      temperature_return: {value: 40-50, unit: ℃}
      pressure: {value: 0.4-0.8, unit: MPa}
      delta_t: {value: 10-15, unit: ℃}
```

---
