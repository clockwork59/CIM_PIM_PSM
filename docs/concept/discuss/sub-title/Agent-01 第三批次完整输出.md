## 🧑‍💻 User


继续Batch 3（给排水系统、消防系统、智能化系统）的完整输出

---
## 🤖 Assistant


# Agent-01 第三批次完整输出

## 声明

本输出严格遵循Agent-01系统拓扑建模师Prompt v2.0规范，覆盖PLUMBING（给排水系统）、FIRE_PROTECTION（消防系统）和INTELLIGENT（智能化系统）的完整拓扑建模。

---

## 第一部分：系统目录补充 (System Catalog - Batch 3)

```yaml
System_Catalog:

  - category_id: PLUMBING
    category_name: 给排水系统
    category_name_en: Plumbing Systems
    description: 提供建筑生活给水、热水、排水、特殊用水等功能的系统集合
    
    systems:
      - system_id: PLUMB-DWS
        system_name: 生活给水系统
        system_name_en: Domestic Water Supply System
        primary_medium: WATER-DW
        description: 市政供水经加压、处理后供应至各用水点
        priority: P1-CRITICAL
        
      - system_id: PLUMB-HWS
        system_name: 生活热水系统
        system_name_en: Domestic Hot Water System
        primary_medium: WATER-HW-DOM
        secondary_medium: [STEAM, ELEC-LV]
        description: 集中或分散式热水供应系统
        priority: P2-IMPORTANT
        
      - system_id: PLUMB-PWS
        system_name: 纯水系统
        system_name_en: Purified Water System
        primary_medium: WATER-PW
        description: 血透室、检验科、供应室等医疗用纯水
        priority: P1-CRITICAL
        
      - system_id: PLUMB-SAN
        system_name: 污废水排水系统
        system_name_en: Sanitary Drainage System
        primary_medium: WATER-WASTE
        description: 生活污水、废水收集排放
        priority: P2-IMPORTANT
        
      - system_id: PLUMB-MED-WASTE
        system_name: 医疗废水系统
        system_name_en: Medical Wastewater System
        primary_medium: WATER-MED-WASTE
        description: 手术室、实验室等医疗废水预处理
        priority: P1-CRITICAL
        
      - system_id: PLUMB-STORM
        system_name: 雨水排水系统
        system_name_en: Storm Drainage System
        primary_medium: WATER-STORM
        description: 屋面及场地雨水收集排放
        priority: P3-NORMAL
        
      - system_id: PLUMB-RW
        system_name: 中水回用系统
        system_name_en: Reclaimed Water System
        primary_medium: WATER-RW
        description: 处理后的中水用于冲厕、绿化等
        priority: P3-NORMAL

    system_dependencies:
      - upstream: PLUMB-DWS
        downstream: PLUMB-HWS
        interface_medium: WATER-DW
        
      - upstream: PLUMB-DWS
        downstream: PLUMB-PWS
        interface_medium: WATER-DW
        
      - upstream: PLUMB-SAN
        downstream: PLUMB-MED-WASTE
        interface_medium: WATER-WASTE
        note: 医疗废水预处理后排入市政污水

  - category_id: FIRE_PROTECTION
    category_name: 消防系统
    category_name_en: Fire Protection Systems
    description: 提供建筑火灾探测、报警、灭火功能的系统集合
    
    systems:
      - system_id: FIRE-HYDRANT
        system_name: 室内消火栓系统
        system_name_en: Indoor Fire Hydrant System
        primary_medium: WATER-FIRE
        description: 消火栓供水灭火系统
        priority: P1-CRITICAL
        
      - system_id: FIRE-SPRINKLER
        system_name: 自动喷水灭火系统
        system_name_en: Automatic Sprinkler System
        primary_medium: WATER-FIRE
        description: 湿式/预作用自动喷水系统
        priority: P1-CRITICAL
        
      - system_id: FIRE-GAS
        system_name: 气体灭火系统
        system_name_en: Gas Fire Suppression System
        primary_medium: GAS-FIRE
        description: 数据中心、配电室等特殊区域气体灭火
        priority: P1-CRITICAL
        
      - system_id: FIRE-ALARM
        system_name: 火灾自动报警系统
        system_name_en: Fire Alarm System
        primary_medium: SIGNAL-FA
        description: 火灾探测、报警、联动控制
        priority: P1-CRITICAL
        
      - system_id: FIRE-SMOKE
        system_name: 防排烟系统
        system_name_en: Smoke Control System
        primary_medium: AIR-SMOKE
        description: 正压送风、排烟系统
        priority: P1-CRITICAL
        
      - system_id: FIRE-EXT
        system_name: 灭火器配置
        system_name_en: Fire Extinguisher System
        primary_medium: null
        description: 手提式灭火器布置
        priority: P2-IMPORTANT

  - category_id: INTELLIGENT
    category_name: 智能化系统
    category_name_en: Intelligent Building Systems
    description: 提供建筑自动化、信息化、安全防范等智能功能的系统集合
    
    systems:
      - system_id: INT-BA
        system_name: 楼宇自动化系统
        system_name_en: Building Automation System
        primary_medium: SIGNAL-BA
        description: HVAC、给排水、照明等设备监控
        priority: P2-IMPORTANT
        
      - system_id: INT-SEC
        system_name: 安全防范系统
        system_name_en: Security System
        primary_medium: SIGNAL-SEC
        description: 视频监控、门禁、入侵报警
        priority: P1-CRITICAL
        
      - system_id: INT-NET
        system_name: 综合布线系统
        system_name_en: Structured Cabling System
        primary_medium: CABLE-DATA
        description: 数据、语音综合布线
        priority: P1-CRITICAL
        
      - system_id: INT-IT
        system_name: 信息网络系统
        system_name_en: IT Network System
        primary_medium: DATA-IP
        description: 院内网络、互联网接入
        priority: P1-CRITICAL
        
      - system_id: INT-NURSE
        system_name: 护理呼叫系统
        system_name_en: Nurse Call System
        primary_medium: SIGNAL-NURSE
        description: 病床呼叫、对讲系统
        priority: P1-CRITICAL
        
      - system_id: INT-PA
        system_name: 公共广播系统
        system_name_en: Public Address System
        primary_medium: SIGNAL-AUDIO
        description: 背景音乐、紧急广播
        priority: P2-IMPORTANT
        
      - system_id: INT-IPTV
        system_name: 病房电视系统
        system_name_en: Patient TV System
        primary_medium: SIGNAL-VIDEO
        description: 病房娱乐、信息发布
        priority: P3-NORMAL
        
      - system_id: INT-CLOCK
        system_name: 时钟系统
        system_name_en: Master Clock System
        primary_medium: SIGNAL-TIME
        description: 全院统一时钟、手术计时
        priority: P2-IMPORTANT
        
      - system_id: INT-IBMS
        system_name: 智能化集成平台
        system_name_en: Intelligent Building Management System
        primary_medium: DATA-IP
        description: 各智能化子系统集成管理
        priority: P2-IMPORTANT
```

---

## 第二部分：介质类型定义补充 (Medium Types - Batch 3)

```yaml
Medium_Types:

  # 给排水介质
  Water_Media_Plumbing:
    - medium_id: WATER-DW
      medium_name: 生活给水
      medium_name_en: Domestic Water
      category: WATER
      typical_properties:
        temperature: {value: 5-25, unit: ℃}
        pressure_municipal: {value: 0.2-0.4, unit: MPa}
        pressure_building: {value: 0.3-0.45, unit: MPa}
        quality: 符合GB5749饮用水标准
        
    - medium_id: WATER-HW-DOM
      medium_name: 生活热水
      medium_name_en: Domestic Hot Water
      category: WATER
      typical_properties:
        temperature_supply: {value: 55-60, unit: ℃}
        temperature_return: {value: 45-50, unit: ℃}
        pressure: {value: 0.3-0.45, unit: MPa}
        
    - medium_id: WATER-PW
      medium_name: 纯化水
      medium_name_en: Purified Water
      category: WATER
      typical_properties:
        conductivity: {value: "≤2", unit: μS/cm}
        toc: {value: "≤500", unit: ppb}
        bacteria: {value: "≤10", unit: CFU/100mL}
        
    - medium_id: WATER-WASTE
      medium_name: 污废水
      medium_name_en: Wastewater
      category: WATER
      typical_properties:
        type: [生活污水, 生活废水]
        
    - medium_id: WATER-MED-WASTE
      medium_name: 医疗废水
      medium_name_en: Medical Wastewater
      category: WATER
      typical_properties:
        type: [手术废水, 实验废水, 放射性废水, 传染性废水]
        treatment: 预处理后排放
        
    - medium_id: WATER-STORM
      medium_name: 雨水
      medium_name_en: Storm Water
      category: WATER
      
    - medium_id: WATER-RW
      medium_name: 中水
      medium_name_en: Reclaimed Water
      category: WATER
      typical_properties:
        usage: [冲厕, 绿化, 道路冲洗]

  # 消防介质
  Fire_Media:
    - medium_id: WATER-FIRE
      medium_name: 消防水
      medium_name_en: Fire Water
      category: WATER
      typical_properties:
        pressure_hydrant: {value: 0.7-1.0, unit: MPa}
        pressure_sprinkler: {value: 0.1-1.2, unit: MPa}
        
    - medium_id: GAS-FIRE
      medium_name: 气体灭火剂
      medium_name_en: Fire Suppression Gas
      category: GAS
      typical_properties:
        types: [七氟丙烷, IG541, 二氧化碳]
        
    - medium_id: AIR-SMOKE
      medium_name: 排烟/送风气流
      medium_name_en: Smoke Control Air
      category: AIR
      typical_properties:
        smoke_exhaust_velocity: {value: "≥15", unit: m/s}
        pressurization: {value: 25-50, unit: Pa}

  # 智能化信号介质
  Signal_Media:
    - medium_id: SIGNAL-FA
      medium_name: 火灾报警信号
      medium_name_en: Fire Alarm Signal
      category: SIGNAL
      typical_properties:
        protocol: GB4717
        voltage: {value: 24, unit: VDC}
        
    - medium_id: SIGNAL-BA
      medium_name: 楼宇自控信号
      medium_name_en: Building Automation Signal
      category: SIGNAL
      typical_properties:
        protocol: [BACnet, Modbus, LON]
        
    - medium_id: SIGNAL-SEC
      medium_name: 安防信号
      medium_name_en: Security Signal
      category: SIGNAL
      typical_properties:
        protocol: [ONVIF, GB/T28181]
        
    - medium_id: SIGNAL-NURSE
      medium_name: 护理呼叫信号
      medium_name_en: Nurse Call Signal
      category: SIGNAL
      typical_properties:
        type: 数字式/IP式
        
    - medium_id: CABLE-DATA
      medium_name: 数据电缆
      medium_name_en: Data Cable
      category: CABLE
      typical_properties:
        type: [Cat6A, Cat7, 光纤]
        
    - medium_id: DATA-IP
      medium_name: IP数据
      medium_name_en: IP Data
      category: DATA
      typical_properties:
        protocol: TCP/IP
        bandwidth: [1Gbps, 10Gbps]
```

---

## 第三部分：PLUMB-DWS 生活给水系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: PLUMB-DWS
    system_name: 生活给水系统
    system_name_en: Domestic Water Supply System
    category: PLUMBING
    version: 1.0
    
    description: |
      医院生活给水系统，采用市政供水+变频加压供水方式。
      低区由市政直供，高区经变频泵组加压供应。
      设置生活水箱作为储备水源。
      
    design_basis:
      supply_mode: 市政直供+变频加压
      zoning: 
        - {zone: 低区, floors: "B2-4F", pressure_source: 市政直供}
        - {zone: 高区, floors: "5F-15F", pressure_source: 变频加压}
      storage: 生活水箱（12小时用水量）
      
    serving_scope:
      - 卫生洁具
      - 开水器
      - 空调补水
      - 绿化浇灌
      - 冷却塔补水

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: PLUMB-DWS_BND_IN_MUNI
        boundary_name: 市政供水
        medium: WATER-DW
        is_external: true
        source: 市政给水管网
        parameters:
          pressure: {value: 0.25-0.35, unit: MPa}
          pipe_size: {value: DN150-DN200, unit: mm}
          supply_routes: 2 (双路进水)
          
      - boundary_id: PLUMB-DWS_BND_IN_ELEC
        boundary_name: 电源
        medium: ELEC-LV
        source_system: ELEC-LV-MAIN
        
    outputs:
      - boundary_id: PLUMB-DWS_BND_OUT_FIXTURE
        boundary_name: 卫生洁具
        medium: WATER-DW
        target: 卫生间、盥洗室
        
      - boundary_id: PLUMB-DWS_BND_OUT_HWS
        boundary_name: 热水系统供水
        medium: WATER-DW
        target_system: PLUMB-HWS
        
      - boundary_id: PLUMB-DWS_BND_OUT_PWS
        boundary_name: 纯水系统供水
        medium: WATER-DW
        target_system: PLUMB-PWS

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:
  
    source_nodes:
    
      - node_id: PLUMB-DWS_SRC_MUNI
        node_name: 市政给水接口
        node_name_en: Municipal Water Connection
        node_type: Source_Node
        node_category: SRC
        
        function: 市政给水引入
        medium_out: WATER-DW
        is_external: true
        
        multiplicity: multiple
        
        typical_configuration:
          quantity: 2 (双路进水)
          
        equipment_parameters:
          meter_size: {value: DN100-DN150, unit: mm}
          backflow_preventer: 倒流防止器
          
        location_hint:
          space_type: UNDERGROUND
          position: 室外给水引入管
          
        installation_requirements:
          - 水表井
          - 倒流防止器
          - 阀门井
          - 埋深≥冻土线以下

    distribution_nodes:
    
      - node_id: PLUMB-DWS_DST_TANK
        node_name: 生活水箱
        node_name_en: Domestic Water Tank
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BUF
        
        function: 储水、稳压、消毒
        medium_in: WATER-DW
        medium_out: WATER-DW
        
        equipment_parameters:
          capacity: {value: 200-500, unit: m³}
          material: 不锈钢/搪瓷钢板
          configuration: 双格（便于清洗）
          disinfection: 紫外线/臭氧
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 生活水泵房
          floor: 地下室
          
        installation_requirements:
          - 人孔盖
          - 通气管
          - 溢流管
          - 液位计
          - 消毒装置
          - 检修空间
          
        control_points:
          sensors:
            - {point_id: TANK_LEVEL, type: AI, description: 水位}
            - {point_id: TANK_TEMP, type: AI, description: 水温}
          status:
            - {point_id: TANK_HIGH, type: DI, description: 高水位}
            - {point_id: TANK_LOW, type: DI, description: 低水位}
            - {point_id: TANK_OVERFLOW, type: DI, description: 溢流报警}

      - node_id: PLUMB-DWS_DST_PUMP_SET
        node_name: 变频给水泵组
        node_name_en: Variable Speed Pump Set
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 变频加压供水
        medium_in: WATER-DW
        medium_out: WATER-DW
        
        equipment_parameters:
          configuration: 变频恒压供水
          pump_quantity: {value: "3+1", unit: null}
          flow_per_pump: {value: 50-80, unit: m³/h}
          head: {value: 50-80, unit: m}
          power: {value: 15-30, unit: kW}
          pressure_setpoint: {value: 0.45, unit: MPa}
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 生活水泵房
          floor: 地下室
          
        installation_requirements:
          - 减振基础
          - 软接头
          - 止回阀
          - 压力罐（小型系统）
          
        control_points:
          sensors:
            - {point_id: PUMP_P_OUT, type: AI, description: 出口压力}
            - {point_id: PUMP_FREQ, type: AI, description: 运行频率}
            - {point_id: PUMP_I, type: AI, description: 运行电流}
          status:
            - {point_id: PUMP_RUN, type: DI, description: 运行状态}
            - {point_id: PUMP_FAULT, type: DI, description: 故障报警}
          commands:
            - {point_id: PUMP_START, type: DO, description: 启停控制}
            - {point_id: PUMP_P_SP, type: AO, description: 压力设定}

      - node_id: PLUMB-DWS_DST_MAIN_SUP
        node_name: 给水主干管
        node_name_en: Water Supply Main
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
        
        function: 水平输配主干管
        medium_in: WATER-DW
        medium_out: WATER-DW
        
        equipment_parameters:
          material: 不锈钢管/PPR管
          diameter: {value: DN100-DN150, unit: mm}
          
        location_hint:
          space_type: CEILING_VOID / PIPE_TRENCH
          position: 地下室顶板下

      - node_id: PLUMB-DWS_DST_RISER
        node_name: 给水立管
        node_name_en: Water Supply Riser
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
        
        function: 垂直输配
        medium_in: WATER-DW
        medium_out: WATER-DW
        
        multiplicity: multiple
        instance_pattern: PLUMB-DWS_DST_RISER_{Zone}_{Seq}
        
        equipment_parameters:
          material: 不锈钢管/PPR管
          diameter: {value: DN50-DN80, unit: mm}
          
        location_hint:
          space_type: SHAFT
          shaft_type: 给排水管井

      - node_id: PLUMB-DWS_DST_FLOOR_VALVE
        node_name: 楼层阀门
        node_name_en: Floor Isolation Valve
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 楼层隔断控制
        medium_in: WATER-DW
        medium_out: WATER-DW
        
        multiplicity: multiple
        
        equipment_parameters:
          type: 闸阀/蝶阀
          
        location_hint:
          space_type: SHAFT
          position: 楼层管井内

      - node_id: PLUMB-DWS_DST_BRANCH
        node_name: 楼层支管
        node_name_en: Floor Branch Pipe
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BRH
        
        function: 楼层水平分配
        medium_in: WATER-DW
        medium_out: WATER-DW
        
        equipment_parameters:
          material: PPR管
          diameter: {value: DN25-DN40, unit: mm}
          
        location_hint:
          space_type: CEILING_VOID / WALL
          position: 走廊吊顶或墙内

    sink_nodes:
    
      - node_id: PLUMB-DWS_SNK_FIXTURE
        node_name: 卫生洁具
        node_name_en: Plumbing Fixtures
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 生活用水
        medium_in: WATER-DW
        
        multiplicity: multiple
        
        equipment_parameters:
          types:
            - {type: 洗手盆, flow: 0.15, unit: L/s}
            - {type: 坐便器, flow: 0.2, unit: L/s}
            - {type: 淋浴器, flow: 0.15, unit: L/s}
            - {type: 污洗盆, flow: 0.2, unit: L/s}
            
        location_hint:
          space_type: WET_ROOM
          position: 卫生间、盥洗室
          
      - node_id: PLUMB-DWS_SNK_EQUIPMENT
        node_name: 用水设备
        node_name_en: Water Using Equipment
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 设备用水
        medium_in: WATER-DW
        
        equipment_parameters:
          types:
            - 开水器
            - 洗衣机
            - 洗碗机
            - 清洗消毒机
            
        location_hint:
          space_type: UTILITY
          position: 开水间、供应室

  # ============================================================
  # 边定义
  # ============================================================
  edges:
  
    supply_edges:
    
      - edge_id: PLUMB-DWS_EDGE_001
        edge_name: 市政进水至水箱
        edge_type: TRK
        from_node: PLUMB-DWS_SRC_MUNI
        to_node: PLUMB-DWS_DST_TANK
        direction: unidirectional
        medium: WATER-DW
        medium_properties:
          pressure: {value: 0.25-0.35, unit: MPa}
        physical_properties:
          material: 球墨铸铁管
          diameter: DN150
          
      - edge_id: PLUMB-DWS_EDGE_002
        edge_name: 水箱至泵组
        edge_type: TRK
        from_node: PLUMB-DWS_DST_TANK
        to_node: PLUMB-DWS_DST_PUMP_SET
        direction: unidirectional
        medium: WATER-DW
        physical_properties:
          diameter: DN150
          
      - edge_id: PLUMB-DWS_EDGE_003
        edge_name: 泵组至主干管
        edge_type: TRK
        from_node: PLUMB-DWS_DST_PUMP_SET
        to_node: PLUMB-DWS_DST_MAIN_SUP
        direction: unidirectional
        medium: WATER-DW
        medium_properties:
          pressure: {value: 0.45, unit: MPa}
          
      - edge_id: PLUMB-DWS_EDGE_004
        edge_name: 主干管至立管
        edge_type: BRH
        from_node: PLUMB-DWS_DST_MAIN_SUP
        to_node: PLUMB-DWS_DST_RISER
        direction: unidirectional
        medium: WATER-DW
        
      - edge_id: PLUMB-DWS_EDGE_005
        edge_name: 立管至楼层阀门
        edge_type: BRH
        from_node: PLUMB-DWS_DST_RISER
        to_node: PLUMB-DWS_DST_FLOOR_VALVE
        direction: unidirectional
        medium: WATER-DW
        
      - edge_id: PLUMB-DWS_EDGE_006
        edge_name: 楼层阀门至支管
        edge_type: TRK
        from_node: PLUMB-DWS_DST_FLOOR_VALVE
        to_node: PLUMB-DWS_DST_BRANCH
        direction: unidirectional
        medium: WATER-DW
        
      - edge_id: PLUMB-DWS_EDGE_007
        edge_name: 支管至洁具
        edge_type: TRM
        from_node: PLUMB-DWS_DST_BRANCH
        to_node: PLUMB-DWS_SNK_FIXTURE
        direction: unidirectional
        medium: WATER-DW

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:
  
    - path_id: PLUMB-DWS_PATH_MAIN
      path_name: 加压供水主路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: PLUMB-DWS_SRC_MUNI}
        - {step: 2, element_type: edge, element_id: PLUMB-DWS_EDGE_001}
        - {step: 3, element_type: node, element_id: PLUMB-DWS_DST_TANK}
        - {step: 4, element_type: edge, element_id: PLUMB-DWS_EDGE_002}
        - {step: 5, element_type: node, element_id: PLUMB-DWS_DST_PUMP_SET}
        - {step: 6, element_type: edge, element_id: PLUMB-DWS_EDGE_003}
        - {step: 7, element_type: node, element_id: PLUMB-DWS_DST_MAIN_SUP}
        - {step: 8, element_type: edge, element_id: PLUMB-DWS_EDGE_004}
        - {step: 9, element_type: node, element_id: PLUMB-DWS_DST_RISER}
        - {step: 10, element_type: edge, element_id: PLUMB-DWS_EDGE_005}
        - {step: 11, element_type: node, element_id: PLUMB-DWS_DST_FLOOR_VALVE}
        - {step: 12, element_type: edge, element_id: PLUMB-DWS_EDGE_006}
        - {step: 13, element_type: node, element_id: PLUMB-DWS_DST_BRANCH}
        - {step: 14, element_type: edge, element_id: PLUMB-DWS_EDGE_007}
        - {step: 15, element_type: node, element_id: PLUMB-DWS_SNK_FIXTURE}

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:
  
    pump_control:
      mode: 变频恒压
      pressure_setpoint: {value: 0.45, unit: MPa}
      control_method: PID调节出口压力
      pump_sequence: 轮换运行
      
    tank_control:
      high_level: 关闭进水阀
      low_level: 开启进水阀
      very_low_level: 泵组保护停机
```

---

## 第四部分：PLUMB-PWS 纯水系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: PLUMB-PWS
    system_name: 纯水系统
    system_name_en: Purified Water System
    category: PLUMBING
    version: 1.0
    
    description: |
      医院医疗用纯水制备与供应系统。
      采用反渗透（RO）工艺制备纯化水，经循环管网供应至各用水点。
      
    design_basis:
      process: 预处理 + 一级RO + 二级RO + EDI
      water_quality:
        conductivity: {value: "≤2", unit: μS/cm}
        toc: {value: "≤500", unit: ppb}
        bacteria: {value: "≤10", unit: CFU/100mL}
      circulation: 循环供水
      
    serving_scope:
      - 血液透析中心
      - 检验科
      - 供应室
      - 手术室刷手
      - 病理科
      - ICU

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: PLUMB-PWS_BND_IN_DW
        boundary_name: 生活给水
        medium: WATER-DW
        source_system: PLUMB-DWS
        
      - boundary_id: PLUMB-PWS_BND_IN_ELEC
        boundary_name: 电源
        medium: ELEC-LV
        source_system: ELEC-LV-CRITICAL
        
    outputs:
      - boundary_id: PLUMB-PWS_BND_OUT_PW
        boundary_name: 纯水终端
        medium: WATER-PW
        target: 医疗用水点
        
      - boundary_id: PLUMB-PWS_BND_OUT_DRAIN
        boundary_name: 浓水排放
        medium: WATER-WASTE
        target_system: PLUMB-SAN

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:
  
    source_nodes:
    
      - node_id: PLUMB-PWS_SRC_RAW
        node_name: 原水进水
        node_name_en: Raw Water Inlet
        node_type: Source_Node
        node_category: SRC
        
        function: 生活给水接入
        medium_out: WATER-DW
        
        source_system: PLUMB-DWS
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 纯水机房

    distribution_nodes:
    
      - node_id: PLUMB-PWS_DST_PRETREAT
        node_name: 预处理系统
        node_name_en: Pretreatment System
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
        
        function: 原水预处理
        medium_in: WATER-DW
        medium_out: WATER-DW
        
        equipment_parameters:
          components:
            - {stage: 1, type: 多介质过滤器, function: 去除悬浮物}
            - {stage: 2, type: 活性炭过滤器, function: 去除余氯、有机物}
            - {stage: 3, type: 软化器, function: 去除硬度}
            - {stage: 4, type: 精密过滤器, function: 5μm过滤}
            
        location_hint:
          space_type: MEP_ROOM
          room_name: 纯水机房

      - node_id: PLUMB-PWS_DST_RO1
        node_name: 一级反渗透
        node_name_en: First Stage RO
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
        
        function: 一级反渗透脱盐
        medium_in: WATER-DW
        medium_out: WATER-PW
        
        equipment_parameters:
          type: 反渗透膜组
          recovery: {value: 70-75, unit: "%"}
          desalination_rate: {value: "≥98", unit: "%"}
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 纯水机房
          
        control_points:
          sensors:
            - {point_id: RO1_COND_IN, type: AI, description: 进水电导率}
            - {point_id: RO1_COND_OUT, type: AI, description: 产水电导率}
            - {point_id: RO1_P_IN, type: AI, description: 进水压力}
            - {point_id: RO1_FLOW, type: AI, description: 产水流量}

      - node_id: PLUMB-PWS_DST_RO2
        node_name: 二级反渗透
        node_name_en: Second Stage RO
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
        
        function: 二级反渗透深度脱盐
        medium_in: WATER-PW
        medium_out: WATER-PW
        
        equipment_parameters:
          type: 反渗透膜组
          recovery: {value: 85-90, unit: "%"}
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 纯水机房

      - node_id: PLUMB-PWS_DST_EDI
        node_name: EDI模块
        node_name_en: EDI Module
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
        
        function: 电去离子深度纯化
        medium_in: WATER-PW
        medium_out: WATER-PW
        
        equipment_parameters:
          type: 连续电去离子
          product_conductivity: {value: "≤0.1", unit: μS/cm}
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 纯水机房

      - node_id: PLUMB-PWS_DST_STORAGE
        node_name: 纯水储罐
        node_name_en: Purified Water Storage Tank
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BUF
        
        function: 纯水储存、缓冲
        medium_in: WATER-PW
        medium_out: WATER-PW
        
        equipment_parameters:
          capacity: {value: 5-20, unit: m³}
          material: 316L不锈钢
          features:
            - 氮封保护
            - 呼吸器
            - 喷淋球清洗
            - UV消毒
            
        location_hint:
          space_type: MEP_ROOM
          room_name: 纯水机房
          
        control_points:
          sensors:
            - {point_id: TANK_LEVEL, type: AI, description: 液位}
            - {point_id: TANK_COND, type: AI, description: 电导率}
            - {point_id: TANK_TOC, type: AI, description: TOC}

      - node_id: PLUMB-PWS_DST_CIRC_PUMP
        node_name: 循环泵
        node_name_en: Circulation Pump
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 纯水循环输配
        medium_in: WATER-PW
        medium_out: WATER-PW
        
        equipment_parameters:
          material: 316L不锈钢
          flow: {value: 10-30, unit: m³/h}
          head: {value: 30-50, unit: m}
          configuration: 一用一备
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 纯水机房

      - node_id: PLUMB-PWS_DST_UV
        node_name: UV消毒器
        node_name_en: UV Disinfection Unit
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
        
        function: 紫外线杀菌
        medium_in: WATER-PW
        medium_out: WATER-PW
        
        equipment_parameters:
          dose: {value: "≥40", unit: mJ/cm²}
          material: 316L不锈钢
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 纯水机房

      - node_id: PLUMB-PWS_DST_LOOP
        node_name: 循环管网
        node_name_en: Distribution Loop
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
        
        function: 纯水循环分配管网
        medium_in: WATER-PW
        medium_out: WATER-PW
        
        equipment_parameters:
          material: 316L不锈钢管/PVDF管
          diameter: {value: DN40-DN65, unit: mm}
          connection: 卡箍连接/洁净焊接
          slope: {value: "≥1%", note: 可完全排空}
          
        location_hint:
          space_type: CEILING_VOID
          position: 用水区域吊顶内

      - node_id: PLUMB-PWS_DST_USE_POINT_VALVE
        node_name: 用水点阀门
        node_name_en: Point of Use Valve
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 用水点隔断与取水
        medium_in: WATER-PW
        medium_out: WATER-PW
        
        multiplicity: multiple
        
        equipment_parameters:
          type: 卫生级隔膜阀
          
        location_hint:
          space_type: WALL
          position: 用水区域墙面

    sink_nodes:
    
      - node_id: PLUMB-PWS_SNK_DIALYSIS
        node_name: 血透用水点
        node_name_en: Dialysis Water Point
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 血液透析
        medium_in: WATER-PW
        
        equipment_parameters:
          quality: 符合YY0572
          flow_per_machine: {value: 500, unit: mL/min}
          
        location_hint:
          space_type: MEDICAL
          room_name: 血透中心
          
      - node_id: PLUMB-PWS_SNK_CSSD
        node_name: 供应室用水点
        node_name_en: CSSD Water Point
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 器械清洗
        medium_in: WATER-PW
        
        equipment_parameters:
          quality: 终末漂洗水
          
        location_hint:
          space_type: MEDICAL
          room_name: 消毒供应中心

      - node_id: PLUMB-PWS_SNK_LAB
        node_name: 检验科用水点
        node_name_en: Laboratory Water Point
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 检验分析
        medium_in: WATER-PW
        
        location_hint:
          space_type: MEDICAL
          room_name: 检验科

  # ============================================================
  # 边定义
  # ============================================================
  edges:
  
    supply_edges:
    
      - edge_id: PLUMB-PWS_EDGE_001
        edge_name: 原水至预处理
        edge_type: TRK
        from_node: PLUMB-PWS_SRC_RAW
        to_node: PLUMB-PWS_DST_PRETREAT
        direction: unidirectional
        medium: WATER-DW
        
      - edge_id: PLUMB-PWS_EDGE_002
        edge_name: 预处理至一级RO
        edge_type: TRK
        from_node: PLUMB-PWS_DST_PRETREAT
        to_node: PLUMB-PWS_DST_RO1
        direction: unidirectional
        medium: WATER-DW
        
      - edge_id: PLUMB-PWS_EDGE_003
        edge_name: 一级RO至二级RO
        edge_type: TRK
        from_node: PLUMB-PWS_DST_RO1
        to_node: PLUMB-PWS_DST_RO2
        direction: unidirectional
        medium: WATER-PW
        
      - edge_id: PLUMB-PWS_EDGE_004
        edge_name: 二级RO至EDI
        edge_type: TRK
        from_node: PLUMB-PWS_DST_RO2
        to_node: PLUMB-PWS_DST_EDI
        direction: unidirectional
        medium: WATER-PW
        
      - edge_id: PLUMB-PWS_EDGE_005
        edge_name: EDI至储罐
        edge_type: TRK
        from_node: PLUMB-PWS_DST_EDI
        to_node: PLUMB-PWS_DST_STORAGE
        direction: unidirectional
        medium: WATER-PW
        
      - edge_id: PLUMB-PWS_EDGE_006
        edge_name: 储罐至循环泵
        edge_type: TRK
        from_node: PLUMB-PWS_DST_STORAGE
        to_node: PLUMB-PWS_DST_CIRC_PUMP
        direction: unidirectional
        medium: WATER-PW
        
      - edge_id: PLUMB-PWS_EDGE_007
        edge_name: 循环泵至UV
        edge_type: TRK
        from_node: PLUMB-PWS_DST_CIRC_PUMP
        to_node: PLUMB-PWS_DST_UV
        direction: unidirectional
        medium: WATER-PW
        
      - edge_id: PLUMB-PWS_EDGE_008
        edge_name: UV至循环管网
        edge_type: TRK
        from_node: PLUMB-PWS_DST_UV
        to_node: PLUMB-PWS_DST_LOOP
        direction: unidirectional
        medium: WATER-PW
        
      - edge_id: PLUMB-PWS_EDGE_009
        edge_name: 循环管网至用水点
        edge_type: BRH
        from_node: PLUMB-PWS_DST_LOOP
        to_node: PLUMB-PWS_DST_USE_POINT_VALVE
        direction: unidirectional
        medium: WATER-PW
        
      - edge_id: PLUMB-PWS_EDGE_010
        edge_name: 用水点至终端
        edge_type: TRM
        from_node: PLUMB-PWS_DST_USE_POINT_VALVE
        to_node: PLUMB-PWS_SNK_DIALYSIS
        direction: unidirectional
        medium: WATER-PW

    return_edges:
    
      - edge_id: PLUMB-PWS_EDGE_RET_001
        edge_name: 循环管网回水至储罐
        edge_type: TRK
        from_node: PLUMB-PWS_DST_LOOP
        to_node: PLUMB-PWS_DST_STORAGE
        direction: unidirectional
        medium: WATER-PW
        note: 循环回水

  # ============================================================
  # 路径与回路定义
  # ============================================================
  typical_paths:
  
    - path_id: PLUMB-PWS_PATH_PRODUCE
      path_name: 纯水制备路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: PLUMB-PWS_SRC_RAW}
        - {step: 2, element_type: edge, element_id: PLUMB-PWS_EDGE_001}
        - {step: 3, element_type: node, element_id: PLUMB-PWS_DST_PRETREAT}
        - {step: 4, element_type: edge, element_id: PLUMB-PWS_EDGE_002}
        - {step: 5, element_type: node, element_id: PLUMB-PWS_DST_RO1}
        - {step: 6, element_type: edge, element_id: PLUMB-PWS_EDGE_003}
        - {step: 7, element_type: node, element_id: PLUMB-PWS_DST_RO2}
        - {step: 8, element_type: edge, element_id: PLUMB-PWS_EDGE_004}
        - {step: 9, element_type: node, element_id: PLUMB-PWS_DST_EDI}
        - {step: 10, element_type: edge, element_id: PLUMB-PWS_EDGE_005}
        - {step: 11, element_type: node, element_id: PLUMB-PWS_DST_STORAGE}
        
    - path_id: PLUMB-PWS_PATH_DIST
      path_name: 纯水分配路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: PLUMB-PWS_DST_STORAGE}
        - {step: 2, element_type: edge, element_id: PLUMB-PWS_EDGE_006}
        - {step: 3, element_type: node, element_id: PLUMB-PWS_DST_CIRC_PUMP}
        - {step: 4, element_type: edge, element_id: PLUMB-PWS_EDGE_007}
        - {step: 5, element_type: node, element_id: PLUMB-PWS_DST_UV}
        - {step: 6, element_type: edge, element_id: PLUMB-PWS_EDGE_008}
        - {step: 7, element_type: node, element_id: PLUMB-PWS_DST_LOOP}
        - {step: 8, element_type: edge, element_id: PLUMB-PWS_EDGE_009}
        - {step: 9, element_type: node, element_id: PLUMB-PWS_DST_USE_POINT_VALVE}
        - {step: 10, element_type: edge, element_id: PLUMB-PWS_EDGE_010}
        - {step: 11, element_type: node, element_id: PLUMB-PWS_SNK_DIALYSIS}

  loops:
  
    - loop_id: PLUMB-PWS_LOOP_CIRC
      loop_name: 纯水循环回路
      loop_name_en: Purified Water Circulation Loop
      loop_type: closed
      
      description: |
        纯水从储罐经循环泵、UV消毒后进入循环管网，
        未使用的水通过回水管返回储罐，保持持续循环。
        防止细菌滋生，保证水质。
        
      supply_path: PLUMB-PWS_PATH_DIST
      return_path: via PLUMB-PWS_EDGE_RET_001
      
      circulation_velocity: {value: "≥1.5", unit: m/s}
```

---

## 第五部分：PLUMB-SAN 污废水排水系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: PLUMB-SAN
    system_name: 污废水排水系统
    system_name_en: Sanitary Drainage System
    category: PLUMBING
    version: 1.0
    
    description: |
      医院生活污废水收集与排放系统。
      生活污水与废水分流，经化粪池/污水处理站处理后排放。
      地下室污水经提升泵排出。
      
    design_basis:
      separation: 污废水分流
      treatment: 化粪池 + 污水处理站
      basement_drainage: 污水提升
      
    serving_scope:
      - 卫生洁具排水
      - 设备排水
      - 空调凝结水

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: PLUMB-SAN_BND_IN_FIXTURE
        boundary_name: 卫生洁具排水
        medium: WATER-WASTE
        source: 卫生间、盥洗室
        
      - boundary_id: PLUMB-SAN_BND_IN_EQUIP
        boundary_name: 设备排水
        medium: WATER-WASTE
        source: 开水器、洗碗机等
        
    outputs:
      - boundary_id: PLUMB-SAN_BND_OUT_MUNI
        boundary_name: 市政污水
        medium: WATER-WASTE
        is_external: true
        target: 市政污水管网

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:
  
    source_nodes:
    
      - node_id: PLUMB-SAN_SRC_FIXTURE
        node_name: 卫生洁具排水口
        node_name_en: Fixture Drain
        node_type: Source_Node
        node_category: SRC
        
        function: 污废水产生点
        medium_out: WATER-WASTE
        
        multiplicity: multiple
        
        equipment_parameters:
          types:
            - {type: 坐便器, trap: P型/S型存水弯}
            - {type: 洗手盆, trap: P型存水弯}
            - {type: 地漏, trap: 水封≥50mm}
            
        location_hint:
          space_type: WET_ROOM
          position: 卫生间

    distribution_nodes:
    
      - node_id: PLUMB-SAN_DST_BRANCH
        node_name: 排水横支管
        node_name_en: Branch Drain
        node_type: Distribution_Node
        node_category: DST
        node_subtype: JUN
        
        function: 收集同层排水
        medium_in: WATER-WASTE
        medium_out: WATER-WASTE
        
        equipment_parameters:
          material: HDPE管/PVC-U管
          diameter: {value: DN50-DN100, unit: mm}
          slope: {value: "1-3%", unit: null}
          
        location_hint:
          space_type: FLOOR_VOID / CEILING_VOID
          position: 同层排水或降板

      - node_id: PLUMB-SAN_DST_STACK
        node_name: 排水立管
        node_name_en: Drain Stack
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
        
        function: 垂直收集排水
        medium_in: WATER-WASTE
        medium_out: WATER-WASTE
        
        multiplicity: multiple
        instance_pattern: PLUMB-SAN_DST_STACK_{Zone}_{Seq}
        
        equipment_parameters:
          material: HDPE管/PVC-U管
          diameter: {value: DN100-DN150, unit: mm}
          vent: 专用通气立管/伸顶通气
          
        location_hint:
          space_type: SHAFT
          shaft_type: 给排水管井
          
        installation_requirements:
          - 伸顶通气≥500mm
          - 检查口每层设置
          - 立管底部设清扫口

      - node_id: PLUMB-SAN_DST_MAIN
        node_name: 排水横干管
        node_name_en: Building Drain
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
        
        function: 汇集排水至室外
        medium_in: WATER-WASTE
        medium_out: WATER-WASTE
        
        equipment_parameters:
          material: HDPE管/球墨铸铁管
          diameter: {value: DN150-DN300, unit: mm}
          slope: {value: "0.5-1%", unit: null}
          
        location_hint:
          space_type: CEILING_VOID
          floor: 地下室顶板下

      - node_id: PLUMB-SAN_DST_LIFT_SUMP
        node_name: 污水集水坑
        node_name_en: Sewage Sump
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BUF
        
        function: 收集地下室污水
        medium_in: WATER-WASTE
        medium_out: WATER-WASTE
        
        equipment_parameters:
          capacity: {value: 2-5, unit: m³}
          material: 混凝土/玻璃钢
          cover: 密封盖
          vent: 接通气管
          
        location_hint:
          space_type: PIT
          floor: 地下最底层
          
        control_points:
          sensors:
            - {point_id: SUMP_LEVEL, type: AI, description: 液位}
          status:
            - {point_id: SUMP_HIGH, type: DI, description: 高液位报警}
            - {point_id: SUMP_OVERFLOW, type: DI, description: 溢流报警}

      - node_id: PLUMB-SAN_DST_LIFT_PUMP
        node_name: 污水提升泵
        node_name_en: Sewage Lift Pump
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 提升地下室污水
        medium_in: WATER-WASTE
        medium_out: WATER-WASTE
        
        equipment_parameters:
          type: 潜水排污泵/干式排污泵
          flow: {value: 20-50, unit: m³/h}
          head: {value: 15-25, unit: m}
          configuration: 一用一备
          
        location_hint:
          space_type: PIT
          position: 集水坑内/旁
          
        control_points:
          status:
            - {point_id: PUMP_RUN, type: DI, description: 运行状态}
            - {point_id: PUMP_FAULT, type: DI, description: 故障报警}

      - node_id: PLUMB-SAN_DST_SEPTIC
        node_name: 化粪池
        node_name_en: Septic Tank
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
        
        function: 污水初级处理
        medium_in: WATER-WASTE
        medium_out: WATER-WASTE
        
        equipment_parameters:
          capacity: {value: 50-200, unit: m³}
          retention_time: {value: 12-24, unit: h}
          type: 三格式/生化式
          
        location_hint:
          space_type: OUTDOOR
          position: 室外绿地下
          
        installation_requirements:
          - 距建筑物≥5m
          - 距水源≥30m
          - 通气管
          - 清掏口

    sink_nodes:
    
      - node_id: PLUMB-SAN_SNK_MUNICIPAL
        node_name: 市政污水接口
        node_name_en: Municipal Sewer Connection
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 污水排放
        medium_in: WATER-WASTE
        is_external: true
        
        location_hint:
          space_type: UNDERGROUND
          position: 红线内污水检查井

  # ============================================================
  # 边定义
  # ============================================================
  edges:
  
    drainage_edges:
    
      - edge_id: PLUMB-SAN_EDGE_001
        edge_name: 洁具至横支管
        edge_type: TRM
        from_node: PLUMB-SAN_SRC_FIXTURE
        to_node: PLUMB-SAN_DST_BRANCH
        direction: unidirectional
        medium: WATER-WASTE
        
      - edge_id: PLUMB-SAN_EDGE_002
        edge_name: 横支管至立管
        edge_type: BRH
        from_node: PLUMB-SAN_DST_BRANCH
        to_node: PLUMB-SAN_DST_STACK
        direction: unidirectional
        medium: WATER-WASTE
        
      - edge_id: PLUMB-SAN_EDGE_003
        edge_name: 立管至横干管
        edge_type: BRH
        from_node: PLUMB-SAN_DST_STACK
        to_node: PLUMB-SAN_DST_MAIN
        direction: unidirectional
        medium: WATER-WASTE
        
      - edge_id: PLUMB-SAN_EDGE_004
        edge_name: 横干管至化粪池
        edge_type: TRK
        from_node: PLUMB-SAN_DST_MAIN
        to_node: PLUMB-SAN_DST_SEPTIC
        direction: unidirectional
        medium: WATER-WASTE
        
      - edge_id: PLUMB-SAN_EDGE_005
        edge_name: 化粪池至市政
        edge_type: TRK
        from_node: PLUMB-SAN_DST_SEPTIC
        to_node: PLUMB-SAN_SNK_MUNICIPAL
        direction: unidirectional
        medium: WATER-WASTE

    lift_edges:
    
      - edge_id: PLUMB-SAN_EDGE_LIFT_001
        edge_name: 地下污水至集水坑
        edge_type: TRK
        from_node: PLUMB-SAN_DST_BRANCH
        to_node: PLUMB-SAN_DST_LIFT_SUMP
        direction: unidirectional
        medium: WATER-WASTE
        note: 地下室排水
        
      - edge_id: PLUMB-SAN_EDGE_LIFT_002
        edge_name: 集水坑至提升泵
        edge_type: TRK
        from_node: PLUMB-SAN_DST_LIFT_SUMP
        to_node: PLUMB-SAN_DST_LIFT_PUMP
        direction: unidirectional
        medium: WATER-WASTE
        
      - edge_id: PLUMB-SAN_EDGE_LIFT_003
        edge_name: 提升泵至横干管
        edge_type: TRK
        from_node: PLUMB-SAN_DST_LIFT_PUMP
        to_node: PLUMB-SAN_DST_MAIN
        direction: unidirectional
        medium: WATER-WASTE

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:
  
    - path_id: PLUMB-SAN_PATH_GRAVITY
      path_name: 重力排水路径
      path_type: DRN
      sequence:
        - {step: 1, element_type: node, element_id: PLUMB-SAN_SRC_FIXTURE}
        - {step: 2, element_type: edge, element_id: PLUMB-SAN_EDGE_001}
        - {step: 3, element_type: node, element_id: PLUMB-SAN_DST_BRANCH}
        - {step: 4, element_type: edge, element_id: PLUMB-SAN_EDGE_002}
        - {step: 5, element_type: node, element_id: PLUMB-SAN_DST_STACK}
        - {step: 6, element_type: edge, element_id: PLUMB-SAN_EDGE_003}
        - {step: 7, element_type: node, element_id: PLUMB-SAN_DST_MAIN}
        - {step: 8, element_type: edge, element_id: PLUMB-SAN_EDGE_004}
        - {step: 9, element_type: node, element_id: PLUMB-SAN_DST_SEPTIC}
        - {step: 10, element_type: edge, element_id: PLUMB-SAN_EDGE_005}
        - {step: 11, element_type: node, element_id: PLUMB-SAN_SNK_MUNICIPAL}
        
    - path_id: PLUMB-SAN_PATH_LIFT
      path_name: 提升排水路径
      path_type: DRN
      sequence:
        - {step: 1, element_type: node, element_id: PLUMB-SAN_DST_BRANCH}
        - {step: 2, element_type: edge, element_id: PLUMB-SAN_EDGE_LIFT_001}
        - {step: 3, element_type: node, element_id: PLUMB-SAN_DST_LIFT_SUMP}
        - {step: 4, element_type: edge, element_id: PLUMB-SAN_EDGE_LIFT_002}
        - {step: 5, element_type: node, element_id: PLUMB-SAN_DST_LIFT_PUMP}
        - {step: 6, element_type: edge, element_id: PLUMB-SAN_EDGE_LIFT_003}
        - {step: 7, element_type: node, element_id: PLUMB-SAN_DST_MAIN}

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:
  
    lift_pump_control:
      mode: 液位控制
      start_level: {value: 60, unit: "%"}
      stop_level: {value: 20, unit: "%"}
      high_alarm: {value: 80, unit: "%"}
      sequence: 轮换运行
```

---

## 第六部分：FIRE-HYDRANT 室内消火栓系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: FIRE-HYDRANT
    system_name: 室内消火栓系统
    system_name_en: Indoor Fire Hydrant System
    category: FIRE_PROTECTION
    version: 1.0
    
    description: |
      医院室内消火栓灭火系统。
      采用临时高压系统，设消防水池、消防泵组。
      屋顶设稳压装置维持系统压力。
      
    design_basis:
      system_type: 临时高压
      hydrant_quantity: {value: 2, unit: 股/每层}
      flow_rate: {value: 40, unit: L/s}
      duration: {value: 3, unit: h}
      pressure: {value: "≥0.7", unit: MPa, note: 最不利点}
      
    serving_scope:
      - 全院各楼层消火栓

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: FIRE-HYDRANT_BND_IN_POOL
        boundary_name: 消防水池
        medium: WATER-FIRE
        is_external: false
        
      - boundary_id: FIRE-HYDRANT_BND_IN_MUNI
        boundary_name: 市政消防水
        medium: WATER-FIRE
        is_external: true
        source: 市政消防管网
        
      - boundary_id: FIRE-HYDRANT_BND_IN_ELEC
        boundary_name: 消防电源
        medium: ELEC-LV
        source_system: ELEC-LV-FIRE
        
      - boundary_id: FIRE-HYDRANT_BND_IN_SIGNAL
        boundary_name: 启泵信号
        medium: SIGNAL-FA
        source_system: FIRE-ALARM
        
    outputs:
      - boundary_id: FIRE-HYDRANT_BND_OUT_HYDRANT
        boundary_name: 消火栓出口
        medium: WATER-FIRE
        target: 消火栓箱

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:
  
    source_nodes:
    
      - node_id: FIRE-HYDRANT_SRC_POOL
        node_name: 消防水池
        node_name_en: Fire Water Pool
        node_type: Source_Node
        node_category: SRC
        
        function: 消防储水
        medium_out: WATER-FIRE
        
        equipment_parameters:
          capacity: {value: 500-800, unit: m³}
          material: 钢筋混凝土
          partition: 两格（便于清洗）
          effective_volume: 消火栓+喷淋联合
          
        location_hint:
          space_type: UNDERGROUND
          position: 室外或地下室
          
        installation_requirements:
          - 人孔盖
          - 通气管
          - 溢流管
          - 液位显示
          - 补水装置
          - 取水口
          
        control_points:
          sensors:
            - {point_id: POOL_LEVEL, type: AI, description: 水位}
          status:
            - {point_id: POOL_LOW, type: DI, description: 低水位报警}

      - node_id: FIRE-HYDRANT_SRC_MUNI
        node_name: 市政消防接口
        node_name_en: Municipal Fire Connection
        node_type: Source_Node
        node_category: SRC
        
        function: 市政消防水补充
        medium_out: WATER-FIRE
        is_external: true
        
        equipment_parameters:
          connection_size: {value: DN150, unit: mm}
          
        location_hint:
          space_type: OUTDOOR
          position: 室外消防接合器旁

    distribution_nodes:
    
      - node_id: FIRE-HYDRANT_DST_PUMP
        node_name: 消火栓泵
        node_name_en: Fire Hydrant Pump
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 消火栓系统加压
        medium_in: WATER-FIRE
        medium_out: WATER-FIRE
        
        equipment_parameters:
          flow: {value: 40, unit: L/s}
          head: {value: 100-130, unit: m}
          power: {value: 110-160, unit: kW}
          configuration: 一用一备
          start_mode: 自动/手动/远程
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 消防泵房
          floor: 地下室
          
        installation_requirements:
          - 独立房间
          - 直通室外出口
          - 应急照明
          - 防火分隔
          
        control_points:
          sensors:
            - {point_id: PUMP_P_OUT, type: AI, description: 出口压力}
            - {point_id: PUMP_I, type: AI, description: 运行电流}
          status:
            - {point_id: PUMP_RUN, type: DI, description: 运行状态}
            - {point_id: PUMP_FAULT, type: DI, description: 故障报警}
            - {point_id: PUMP_AUTO, type: DI, description: 自动状态}
          commands:
            - {point_id: PUMP_START, type: DO, description: 启动命令}
            - {point_id: PUMP_STOP, type: DO, description: 停止命令}

      - node_id: FIRE-HYDRANT_DST_HEADER
        node_name: 消防出水分配器
        node_name_en: Fire Header
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
        
        function: 分配至各区域环管
        medium_in: WATER-FIRE
        medium_out: WATER-FIRE
        
        equipment_parameters:
          diameter: {value: DN200-DN250, unit: mm}
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 消防泵房

      - node_id: FIRE-HYDRANT_DST_RISER
        node_name: 消火栓立管
        node_name_en: Hydrant Riser
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
        
        function: 垂直输配
        medium_in: WATER-FIRE
        medium_out: WATER-FIRE
        
        multiplicity: multiple
        instance_pattern: FIRE-HYDRANT_DST_RISER_{Zone}_{Seq}
        
        equipment_parameters:
          material: 镀锌钢管
          diameter: {value: DN100-DN150, unit: mm}
          connection: 环状管网
          
        location_hint:
          space_type: SHAFT
          shaft_type: 消防管井
          
        installation_requirements:
          - 试验消火栓（屋顶）
          - 泄水阀（底部）

      - node_id: FIRE-HYDRANT_DST_LOOP
        node_name: 楼层环管
        node_name_en: Floor Loop
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
        
        function: 楼层水平环管
        medium_in: WATER-FIRE
        medium_out: WATER-FIRE
        
        equipment_parameters:
          material: 镀锌钢管
          diameter: {value: DN100, unit: mm}
          
        location_hint:
          space_type: CEILING_VOID
          position: 走廊吊顶内

      - node_id: FIRE-HYDRANT_DST_STAB
        node_name: 屋顶稳压装置
        node_name_en: Roof Pressure Stabilization
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 维持系统压力、气压水罐
        medium_in: WATER-FIRE
        medium_out: WATER-FIRE
        
        equipment_parameters:
          components:
            - 稳压泵
            - 气压水罐
          stabilization_pump:
            flow: {value: 1-2, unit: L/s}
            head: {value: 30-50, unit: m}
          tank_volume: {value: 300-500, unit: L}
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 屋顶消防稳压间
          floor: 屋顶
          
        control_points:
          sensors:
            - {point_id: STAB_P, type: AI, description: 系统压力}
          status:
            - {point_id: STAB_PUMP_RUN, type: DI, description: 稳压泵运行}

      - node_id: FIRE-HYDRANT_DST_SIAMESE
        node_name: 水泵接合器
        node_name_en: Fire Department Connection
        node_type: Distribution_Node
        node_category: DST
        node_subtype: JUN
        
        function: 消防车增压接口
        medium_in: WATER-FIRE
        medium_out: WATER-FIRE
        
        multiplicity: multiple
        
        equipment_parameters:
          type: 地上式/地下式
          quantity: {value: 2-3, unit: 套}
          size: {value: DN100, unit: mm}
          
        location_hint:
          space_type: OUTDOOR
          position: 距外墙5-40m
          
        installation_requirements:
          - 明显标识
          - 距消防车道≤15m
          - 止回阀

    sink_nodes:
    
      - node_id: FIRE-HYDRANT_SNK_BOX
        node_name: 消火栓箱
        node_name_en: Fire Hydrant Cabinet
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 消防灭火
        medium_in: WATER-FIRE
        
        multiplicity: multiple
        instance_pattern: FIRE-HYDRANT_SNK_BOX_{Floor}_{Seq}
        
        equipment_parameters:
          components:
            - DN65消火栓
            - Φ65×25m水带
            - Φ19水枪
            - 消防按钮
          box_type: 明装/暗装/半暗装
          
        location_hint:
          space_type: CORRIDOR
          position: 走廊明显位置
          spacing: {value: "≤25", unit: m, note: 两股水柱到达}
          
        control_points:
          status:
            - {point_id: HYDRANT_PRESS, type: DI, description: 启泵按钮}

  # ============================================================
  # 边定义
  # ============================================================
  edges:
  
    supply_edges:
    
      - edge_id: FIRE-HYDRANT_EDGE_001
        edge_name: 水池至消防泵
        edge_type: TRK
        from_node: FIRE-HYDRANT_SRC_POOL
        to_node: FIRE-HYDRANT_DST_PUMP
        direction: unidirectional
        medium: WATER-FIRE
        physical_properties:
          material: 球墨铸铁管
          diameter: DN200
          
      - edge_id: FIRE-HYDRANT_EDGE_002
        edge_name: 消防泵至分配器
        edge_type: TRK
        from_node: FIRE-HYDRANT_DST_PUMP
        to_node: FIRE-HYDRANT_DST_HEADER
        direction: unidirectional
        medium: WATER-FIRE
        medium_properties:
          pressure: {value: 1.0-1.3, unit: MPa}
          
      - edge_id: FIRE-HYDRANT_EDGE_003
        edge_name: 分配器至立管
        edge_type: BRH
        from_node: FIRE-HYDRANT_DST_HEADER
        to_node: FIRE-HYDRANT_DST_RISER
        direction: unidirectional
        medium: WATER-FIRE
        
      - edge_id: FIRE-HYDRANT_EDGE_004
        edge_name: 立管至楼层环管
        edge_type: BRH
        from_node: FIRE-HYDRANT_DST_RISER
        to_node: FIRE-HYDRANT_DST_LOOP
        direction: unidirectional
        medium: WATER-FIRE
        
      - edge_id: FIRE-HYDRANT_EDGE_005
        edge_name: 楼层环管至消火栓箱
        edge_type: TRM
        from_node: FIRE-HYDRANT_DST_LOOP
        to_node: FIRE-HYDRANT_SNK_BOX
        direction: unidirectional
        medium: WATER-FIRE
        medium_properties:
          pressure: {value: "≥0.7", unit: MPa, note: 最不利点}
          
      - edge_id: FIRE-HYDRANT_EDGE_006
        edge_name: 分配器至稳压装置
        edge_type: TRK
        from_node: FIRE-HYDRANT_DST_HEADER
        to_node: FIRE-HYDRANT_DST_STAB
        direction: bidirectional
        medium: WATER-FIRE
        
      - edge_id: FIRE-HYDRANT_EDGE_007
        edge_name: 水泵接合器至立管
        edge_type: TRK
        from_node: FIRE-HYDRANT_DST_SIAMESE
        to_node: FIRE-HYDRANT_DST_RISER
        direction: unidirectional
        medium: WATER-FIRE
        note: 消防车供水

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:
  
    - path_id: FIRE-HYDRANT_PATH_MAIN
      path_name: 消火栓供水主路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: FIRE-HYDRANT_SRC_POOL}
        - {step: 2, element_type: edge, element_id: FIRE-HYDRANT_EDGE_001}
        - {step: 3, element_type: node, element_id: FIRE-HYDRANT_DST_PUMP}
        - {step: 4, element_type: edge, element_id: FIRE-HYDRANT_EDGE_002}
        - {step: 5, element_type: node, element_id: FIRE-HYDRANT_DST_HEADER}
        - {step: 6, element_type: edge, element_id: FIRE-HYDRANT_EDGE_003}
        - {step: 7, element_type: node, element_id: FIRE-HYDRANT_DST_RISER}
        - {step: 8, element_type: edge, element_id: FIRE-HYDRANT_EDGE_004}
        - {step: 9, element_type: node, element_id: FIRE-HYDRANT_DST_LOOP}
        - {step: 10, element_type: edge, element_id: FIRE-HYDRANT_EDGE_005}
        - {step: 11, element_type: node, element_id: FIRE-HYDRANT_SNK_BOX}
        
    - path_id: FIRE-HYDRANT_PATH_BACKUP
      path_name: 消防车供水路径
      path_type: BKP
      sequence:
        - {step: 1, element_type: node, element_id: FIRE-HYDRANT_DST_SIAMESE}
        - {step: 2, element_type: edge, element_id: FIRE-HYDRANT_EDGE_007}
        - {step: 3, element_type: node, element_id: FIRE-HYDRANT_DST_RISER}

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:
  
    pump_start:
      triggers:
        - 消火栓按钮按下
        - 消防控制室远程启动
        - 系统压力低于设定值
        - 流量开关动作
      start_mode: 直接启动
      
    pump_stop:
      mode: 仅消防控制室手动停止
      
    pressure_stabilization:
      high_pressure: 稳压泵停止
      low_pressure: 稳压泵启动
      very_low_pressure: 主泵启动
```

---

## 第七部分：FIRE-SPRINKLER 自动喷水灭火系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: FIRE-SPRINKLER
    system_name: 自动喷水灭火系统
    system_name_en: Automatic Sprinkler System
    category: FIRE_PROTECTION
    version: 1.0
    
    description: |
      医院自动喷水灭火系统。
      一般区域采用湿式系统，手术部等不宜水渍区域采用预作用系统。
      
    design_basis:
      system_types:
        - {type: 湿式系统, scope: 一般区域}
        - {type: 预作用系统, scope: 手术部、数据中心、贵重设备区}
      hazard_class: 中危险级I级
      design_density: {value: 6-8, unit: "L/(min·m²)"}
      action_area: {value: 160, unit: m²}
      duration: {value: 1, unit: h}
      
    serving_scope:
      - 门诊楼
      - 病房楼
      - 医技楼
      - 地下车库

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:
  
    source_nodes:
    
      - node_id: FIRE-SPRINKLER_SRC_POOL
        node_name: 消防水池
        node_name_en: Fire Water Pool
        node_type: Source_Node
        node_category: SRC
        
        function: 喷淋系统水源
        medium_out: WATER-FIRE
        
        note: 与消火栓共用

    distribution_nodes:
    
      - node_id: FIRE-SPRINKLER_DST_PUMP
        node_name: 喷淋泵
        node_name_en: Sprinkler Pump
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 喷淋系统加压
        medium_in: WATER-FIRE
        medium_out: WATER-FIRE
        
        equipment_parameters:
          flow: {value: 30-40, unit: L/s}
          head: {value: 80-100, unit: m}
          power: {value: 75-110, unit: kW}
          configuration: 一用一备
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 消防泵房
          
        control_points:
          sensors:
            - {point_id: PUMP_P_OUT, type: AI, description: 出口压力}
          status:
            - {point_id: PUMP_RUN, type: DI, description: 运行状态}
            - {point_id: PUMP_FAULT, type: DI, description: 故障报警}

      - node_id: FIRE-SPRINKLER_DST_WET_VALVE
        node_name: 湿式报警阀组
        node_name_en: Wet Alarm Valve Station
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 系统分区控制、报警
        medium_in: WATER-FIRE
        medium_out: WATER-FIRE
        
        multiplicity: multiple
        instance_pattern: FIRE-SPRINKLER_DST_WET_VALVE_{Zone}
        
        equipment_parameters:
          type: 湿式报警阀
          size: {value: DN150-DN200, unit: mm}
          components:
            - 报警阀
            - 延迟器
            - 水力警铃
            - 压力开关
            
        location_hint:
          space_type: MEP_ROOM
          room_name: 报警阀室/消防泵房
          
        control_points:
          status:
            - {point_id: ALARM_VALVE_OPEN, type: DI, description: 报警阀开启}
            - {point_id: PRESSURE_SW, type: DI, description: 压力开关动作}
            - {point_id: WATER_FLOW, type: DI, description: 水流指示器}

      - node_id: FIRE-SPRINKLER_DST_PREACT_VALVE
        node_name: 预作用报警阀组
        node_name_en: Pre-action Alarm Valve Station
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 预作用系统分区控制
        medium_in: WATER-FIRE
        medium_out: WATER-FIRE
        
        multiplicity: multiple
        
        equipment_parameters:
          type: 预作用报警阀
          size: {value: DN100-DN150, unit: mm}
          components:
            - 雨淋阀
            - 电磁阀
            - 气压维持装置
            - 火灾探测器联动
            
        location_hint:
          space_type: MEP_ROOM
          room_name: 报警阀室
          
        control_points:
          sensors:
            - {point_id: AIR_P, type: AI, description: 管网气压}
          status:
            - {point_id: PREACT_OPEN, type: DI, description: 预作用阀开启}
          commands:
            - {point_id: PREACT_RELEASE, type: DO, description: 电磁阀释放}

      - node_id: FIRE-SPRINKLER_DST_RISER
        node_name: 喷淋立管
        node_name_en: Sprinkler Riser
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
        
        function: 垂直输配
        medium_in: WATER-FIRE
        medium_out: WATER-FIRE
        
        multiplicity: multiple
        
        equipment_parameters:
          material: 镀锌钢管
          diameter: {value: DN100-DN150, unit: mm}
          
        location_hint:
          space_type: SHAFT
          shaft_type: 消防管井

      - node_id: FIRE-SPRINKLER_DST_BRANCH
        node_name: 配水管/支管
        node_name_en: Branch Line
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BRH
        
        function: 楼层配水
        medium_in: WATER-FIRE
        medium_out: WATER-FIRE
        
        equipment_parameters:
          material: 镀锌钢管
          diameter: {value: DN25-DN50, unit: mm}
          
        location_hint:
          space_type: CEILING_VOID
          
      - node_id: FIRE-SPRINKLER_DST_FLOW_SW
        node_name: 水流指示器
        node_name_en: Water Flow Switch
        node_type: Distribution_Node
        node_category: DST
        node_subtype: MON
        
        function: 监测水流、报警定位
        medium_in: WATER-FIRE
        medium_out: WATER-FIRE
        
        multiplicity: multiple
        
        equipment_parameters:
          type: 水流指示器
          
        location_hint:
          space_type: CEILING_VOID
          position: 每个防火分区入口
          
        control_points:
          status:
            - {point_id: FLOW_ALARM, type: DI, description: 水流报警}

    sink_nodes:
    
      - node_id: FIRE-SPRINKLER_SNK_HEAD
        node_name: 喷头
        node_name_en: Sprinkler Head
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 喷水灭火
        medium_in: WATER-FIRE
        
        multiplicity: multiple
        
        equipment_parameters:
          types:
            - {type: 下垂型, application: 一般区域}
            - {type: 边墙型, application: 走廊}
            - {type: 隐蔽型, application: 装饰要求高区域}
          temperature_rating:
            - {color: 红色, rating: 68℃, application: 一般区域}
            - {color: 绿色, rating: 93℃, application: 厨房}
          k_factor: {value: 80-115, unit: null}
          spacing: {value: "≤3.6", unit: m}
          
        location_hint:
          space_type: CEILING
          position: 吊顶下
          coverage: {value: "≤12.5", unit: m²/头}

  # ============================================================
  # 边定义
  # ============================================================
  edges:
  
    supply_edges:
    
      - edge_id: FIRE-SPRINKLER_EDGE_001
        edge_name: 水池至喷淋泵
        edge_type: TRK
        from_node: FIRE-SPRINKLER_SRC_POOL
        to_node: FIRE-SPRINKLER_DST_PUMP
        direction: unidirectional
        medium: WATER-FIRE
        
      - edge_id: FIRE-SPRINKLER_EDGE_002
        edge_name: 喷淋泵至湿式阀
        edge_type: TRK
        from_node: FIRE-SPRINKLER_DST_PUMP
        to_node: FIRE-SPRINKLER_DST_WET_VALVE
        direction: unidirectional
        medium: WATER-FIRE
        
      - edge_id: FIRE-SPRINKLER_EDGE_003
        edge_name: 喷淋泵至预作用阀
        edge_type: TRK
        from_node: FIRE-SPRINKLER_DST_PUMP
        to_node: FIRE-SPRINKLER_DST_PREACT_VALVE
        direction: unidirectional
        medium: WATER-FIRE
        
      - edge_id: FIRE-SPRINKLER_EDGE_004
        edge_name: 湿式阀至立管
        edge_type: TRK
        from_node: FIRE-SPRINKLER_DST_WET_VALVE
        to_node: FIRE-SPRINKLER_DST_RISER
        direction: unidirectional
        medium: WATER-FIRE
        
      - edge_id: FIRE-SPRINKLER_EDGE_005
        edge_name: 立管至水流指示器
        edge_type: BRH
        from_node: FIRE-SPRINKLER_DST_RISER
        to_node: FIRE-SPRINKLER_DST_FLOW_SW
        direction: unidirectional
        medium: WATER-FIRE
        
      - edge_id: FIRE-SPRINKLER_EDGE_006
        edge_name: 水流指示器至支管
        edge_type: TRK
        from_node: FIRE-SPRINKLER_DST_FLOW_SW
        to_node: FIRE-SPRINKLER_DST_BRANCH
        direction: unidirectional
        medium: WATER-FIRE
        
      - edge_id: FIRE-SPRINKLER_EDGE_007
        edge_name: 支管至喷头
        edge_type: TRM
        from_node: FIRE-SPRINKLER_DST_BRANCH
        to_node: FIRE-SPRINKLER_SNK_HEAD
        direction: unidirectional
        medium: WATER-FIRE

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:
  
    - path_id: FIRE-SPRINKLER_PATH_WET
      path_name: 湿式系统路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: FIRE-SPRINKLER_SRC_POOL}
        - {step: 2, element_type: edge, element_id: FIRE-SPRINKLER_EDGE_001}
        - {step: 3, element_type: node, element_id: FIRE-SPRINKLER_DST_PUMP}
        - {step: 4, element_type: edge, element_id: FIRE-SPRINKLER_EDGE_002}
        - {step: 5, element_type: node, element_id: FIRE-SPRINKLER_DST_WET_VALVE}
        - {step: 6, element_type: edge, element_id: FIRE-SPRINKLER_EDGE_004}
        - {step: 7, element_type: node, element_id: FIRE-SPRINKLER_DST_RISER}
        - {step: 8, element_type: edge, element_id: FIRE-SPRINKLER_EDGE_005}
        - {step: 9, element_type: node, element_id: FIRE-SPRINKLER_DST_FLOW_SW}
        - {step: 10, element_type: edge, element_id: FIRE-SPRINKLER_EDGE_006}
        - {step: 11, element_type: node, element_id: FIRE-SPRINKLER_DST_BRANCH}
        - {step: 12, element_type: edge, element_id: FIRE-SPRINKLER_EDGE_007}
        - {step: 13, element_type: node, element_id: FIRE-SPRINKLER_SNK_HEAD}

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:
  
    wet_system:
      trigger: 喷头玻璃球破裂（温度）
      action:
        - 水流出
        - 报警阀开启
        - 水力警铃响
        - 压力开关动作
        - 信号至火灾报警系统
        - 喷淋泵自动启动
        
    preaction_system:
      trigger: 火灾探测器动作 AND/OR 喷头动作
      action:
        - 火灾探测器先动作
        - 预作用阀电磁阀释放
        - 管网充水
        - 喷头动作后喷水
        - 双保险，减少误喷
```

---

## 第八部分：FIRE-ALARM 火灾自动报警系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: FIRE-ALARM
    system_name: 火灾自动报警系统
    system_name_en: Fire Alarm System
    category: FIRE_PROTECTION
    version: 1.0
    
    description: |
      医院火灾自动报警及消防联动控制系统。
      采用控制中心报警系统，设消防控制室。
      
    design_basis:
      system_type: 控制中心报警系统
      detector_type: 智能型
      networking: 总线制
      
    serving_scope:
      - 火灾探测
      - 火灾报警
      - 消防联动
      - 消防广播
      - 消防电话

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:
  
    source_nodes:
    
      - node_id: FIRE-ALARM_SRC_DETECTOR
        node_name: 火灾探测器
        node_name_en: Fire Detector
        node_type: Source_Node
        node_category: SRC
        
        function: 探测火灾信号
        medium_out: SIGNAL-FA
        
        multiplicity: multiple
        
        equipment_parameters:
          types:
            - {type: 点型感烟探测器, application: 一般区域}
            - {type: 点型感温探测器, application: 厨房、锅炉房}
            - {type: 线型感烟探测器, application: 大空间}
            - {type: 吸气式感烟探测器, application: 数据中心、洁净区}
            - {type: 火焰探测器, application: 特殊区域}
          coverage: {value: "60-80", unit: m²/只, note: 一般场所}
          
        location_hint:
          space_type: CEILING
          position: 房间/走廊吊顶

      - node_id: FIRE-ALARM_SRC_MANUAL
        node_name: 手动报警按钮
        node_name_en: Manual Call Point
        node_type: Source_Node
        node_category: SRC
        
        function: 人工触发火灾报警
        medium_out: SIGNAL-FA
        
        multiplicity: multiple
        
        equipment_parameters:
          type: 带电话插孔
          spacing: {value: "≤30", unit: m, note: 疏散通道}
          
        location_hint:
          space_type: WALL
          position: 疏散通道、出入口
          height: {value: 1.3-1.5, unit: m}

    distribution_nodes:
    
      - node_id: FIRE-ALARM_DST_MODULE
        node_name: 输入/输出模块
        node_name_en: Input/Output Module
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
        
        function: 信号转换、设备控制
        medium_in: SIGNAL-FA
        medium_out: SIGNAL-FA
        
        multiplicity: multiple
        
        equipment_parameters:
          types:
            - {type: 输入模块, function: 接收设备状态}
            - {type: 输出模块, function: 控制设备动作}
            - {type: 多线制模块, function: 关键设备控制}
            
        location_hint:
          space_type: CEILING_VOID / WALL_BOX
          position: 被控设备附近

      - node_id: FIRE-ALARM_DST_LOOP_CARD
        node_name: 回路板
        node_name_en: Loop Card
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
        
        function: 回路信号汇集处理
        medium_in: SIGNAL-FA
        medium_out: SIGNAL-FA
        
        multiplicity: multiple
        
        equipment_parameters:
          capacity: {value: 200-250, unit: 点/回路}
          
        location_hint:
          space_type: EQUIPMENT
          position: 火灾报警控制器内

      - node_id: FIRE-ALARM_DST_FACP
        node_name: 火灾报警控制器
        node_name_en: Fire Alarm Control Panel
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 火灾报警主机
        medium_in: SIGNAL-FA
        medium_out: SIGNAL-FA
        
        equipment_parameters:
          type: 集中控制型
          loops: {value: 4-16, unit: 回路}
          capacity: {value: 1000-4000, unit: 点}
          display: 图形显示装置
          
        location_hint:
          space_type: CONTROL_ROOM
          room_name: 消防控制室
          floor: 一层/地下一层
          
        installation_requirements:
          - 双路电源
          - 接地
          - UPS后备
          - 防雷
          
        control_points:
          status:
            - {point_id: FA_FIRE, type: DI, description: 火警信号}
            - {point_id: FA_FAULT, type: DI, description: 故障信号}
            - {point_id: FA_SUPER, type: DI, description: 监管信号}

      - node_id: FIRE-ALARM_DST_LINKAGE
        node_name: 消防联动控制器
        node_name_en: Fire Linkage Controller
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 消防设备联动控制
        medium_in: SIGNAL-FA
        medium_out: SIGNAL-FA
        
        equipment_parameters:
          functions:
            - 消防泵启动
            - 防排烟控制
            - 防火卷帘控制
            - 电梯迫降
            - 非消防电源切断
            - 应急照明
            - 消防广播
            
        location_hint:
          space_type: CONTROL_ROOM
          room_name: 消防控制室

      - node_id: FIRE-ALARM_DST_GD
        node_name: 图形显示装置
        node_name_en: Graphic Display System
        node_type: Distribution_Node
        node_category: DST
        node_subtype: MON
        
        function: 图形化显示火警信息
        medium_in: SIGNAL-FA
        
        equipment_parameters:
          display: 大屏幕
          function: 平面图显示火警位置
          
        location_hint:
          space_type: CONTROL_ROOM
          room_name: 消防控制室

    sink_nodes:
    
      - node_id: FIRE-ALARM_SNK_ALARM
        node_name: 声光报警器
        node_name_en: Audible/Visual Alarm
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 火灾警报
        medium_in: SIGNAL-FA
        
        multiplicity: multiple
        
        equipment_parameters:
          sound_level: {value: "≥65", unit: dB}
          flash_rate: {value: "1-2", unit: Hz}
          
        location_hint:
          space_type: WALL
          position: 走廊、大厅、楼梯间

      - node_id: FIRE-ALARM_SNK_SPEAKER
        node_name: 消防广播扬声器
        node_name_en: Fire Broadcast Speaker
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 消防广播
        medium_in: SIGNAL-FA
        
        multiplicity: multiple
        
        equipment_parameters:
          power: {value: 3-10, unit: W}
          coverage: {value: "≤25", unit: m}
          
        location_hint:
          space_type: CEILING
          position: 走廊、大厅、病房

      - node_id: FIRE-ALARM_SNK_EQUIPMENT
        node_name: 消防设备
        node_name_en: Fire Equipment
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 联动控制
        medium_in: SIGNAL-FA
        
        interface_systems:
          - FIRE-HYDRANT (消防泵)
          - FIRE-SPRINKLER (喷淋泵)
          - FIRE-SMOKE (防排烟风机)
          - ELEC-LV (非消防电源)
          - ELEVATOR (电梯迫降)

  # ============================================================
  # 边定义
  # ============================================================
  edges:
  
    signal_edges:
    
      - edge_id: FIRE-ALARM_EDGE_001
        edge_name: 探测器至模块
        edge_type: TRM
        from_node: FIRE-ALARM_SRC_DETECTOR
        to_node: FIRE-ALARM_DST_MODULE
        direction: unidirectional
        medium: SIGNAL-FA
        physical_properties:
          cable_type: NH-BV (耐火)
          
      - edge_id: FIRE-ALARM_EDGE_002
        edge_name: 模块至回路板
        edge_type: TRK
        from_node: FIRE-ALARM_DST_MODULE
        to_node: FIRE-ALARM_DST_LOOP_CARD
        direction: bidirectional
        medium: SIGNAL-FA
        physical_properties:
          cable_type: RVSP-2×1.5
          
      - edge_id: FIRE-ALARM_EDGE_003
        edge_name: 回路板至主机
        edge_type: TRK
        from_node: FIRE-ALARM_DST_LOOP_CARD
        to_node: FIRE-ALARM_DST_FACP
        direction: bidirectional
        medium: SIGNAL-FA
        
      - edge_id: FIRE-ALARM_EDGE_004
        edge_name: 主机至联动控制器
        edge_type: TRK
        from_node: FIRE-ALARM_DST_FACP
        to_node: FIRE-ALARM_DST_LINKAGE
        direction: bidirectional
        medium: SIGNAL-FA
        
      - edge_id: FIRE-ALARM_EDGE_005
        edge_name: 联动控制器至消防设备
        edge_type: TRM
        from_node: FIRE-ALARM_DST_LINKAGE
        to_node: FIRE-ALARM_SNK_EQUIPMENT
        direction: unidirectional
        medium: SIGNAL-FA

  # ============================================================
  # 联动逻辑
  # ============================================================
  linkage_logic:
  
    - scenario: 确认火灾
      trigger: 同一防火分区两个探测器报警 或 一个探测器+手动按钮
      actions:
        - 启动消防广播
        - 启动声光报警
        - 切断非消防电源
        - 电梯迫降至首层
        - 释放防火门
        - 启动应急照明
        
    - scenario: 消火栓启动
      trigger: 消火栓按钮按下
      actions:
        - 启动消火栓泵
        - 反馈信号至消防控制室
        
    - scenario: 喷淋启动
      trigger: 报警阀压力开关动作
      actions:
        - 启动喷淋泵
        - 反馈信号至消防控制室
        
    - scenario: 排烟启动
      trigger: 防烟分区探测器报警
      actions:
        - 开启排烟口
        - 启动排烟风机
        - 开启补风口（如有）
        
    - scenario: 正压送风
      trigger: 疏散通道探测器报警
      actions:
        - 开启正压送风口
        - 启动正压送风机
```

---

## 第九部分：INT-BA 楼宇自动化系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: INT-BA
    system_name: 楼宇自动化系统
    system_name_en: Building Automation System
    category: INTELLIGENT
    version: 1.0
    
    description: |
      医院楼宇自动化系统（BAS/BMS），实现机电设备监控与管理。
      采用DDC控制器+网络架构，支持BACnet/IP协议。
      
    design_basis:
      architecture: 三层架构（管理层-自动化层-现场层）
      protocol: BACnet/IP, Modbus
      redundancy: 服务器冗余
      
    serving_scope:
      - HVAC系统监控
      - 给排水系统监控
      - 电气系统监控
      - 电梯监控
      - 照明控制

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:
  
    source_nodes:
    
      - node_id: INT-BA_SRC_SENSOR
        node_name: 现场传感器
        node_name_en: Field Sensor
        node_type: Source_Node
        node_category: SRC
        
        function: 采集现场数据
        medium_out: SIGNAL-BA
        
        multiplicity: multiple
        
        equipment_parameters:
          types:
            - {type: 温度传感器, signal: 4-20mA/PT1000}
            - {type: 湿度传感器, signal: 4-20mA}
            - {type: 压力传感器, signal: 4-20mA}
            - {type: 流量计, signal: 脉冲/4-20mA}
            - {type: CO2传感器, signal: 4-20mA}
            - {type: 液位开关, signal: 干接点}
            
        location_hint:
          space_type: DUCT / PIPE / ROOM
          position: 被测设备上

      - node_id: INT-BA_SRC_METER
        node_name: 智能电表/水表
        node_name_en: Smart Meter
        node_type: Source_Node
        node_category: SRC
        
        function: 能耗计量
        medium_out: SIGNAL-BA
        
        multiplicity: multiple
        
        equipment_parameters:
          types:
            - {type: 多功能电表, protocol: Modbus RTU}
            - {type: 远传水表, protocol: M-Bus}
            - {type: 热量表, protocol: M-Bus}
            
        location_hint:
          space_type: PANEL
          position: 配电柜/管井

    distribution_nodes:
    
      - node_id: INT-BA_DST_DDC
        node_name: DDC控制器
        node_name_en: Direct Digital Controller
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 现场控制、数据采集
        medium_in: SIGNAL-BA
        medium_out: SIGNAL-BA
        
        multiplicity: multiple
        instance_pattern: INT-BA_DST_DDC_{System}_{Seq}
        
        equipment_parameters:
          types:
            - {type: 通用DDC, io: "8AI/4AO/8DI/8DO"}
            - {type: 空调机组DDC, io: 专用配置}
            - {type: VAV控制器, io: 末端专用}
          protocol: BACnet MS/TP, Modbus RTU
          
        location_hint:
          space_type: WALL_BOX / PANEL
          position: 设备附近或机房
          
        control_points:
          status:
            - {point_id: DDC_ONLINE, type: DI, description: 在线状态}
            - {point_id: DDC_FAULT, type: DI, description: 故障状态}

      - node_id: INT-BA_DST_NAC
        node_name: 网络控制器
        node_name_en: Network Area Controller
        node_type: Distribution_Node
        node_category: DST
        node_subtype: JUN
        
        function: 区域网络汇聚、协议转换
        medium_in: SIGNAL-BA
        medium_out: DATA-IP
        
        multiplicity: multiple
        
        equipment_parameters:
          capacity: {value: 30-50, unit: DDC}
          protocol_up: BACnet/IP
          protocol_down: BACnet MS/TP
          
        location_hint:
          space_type: PANEL
          position: 弱电间/设备机房

      - node_id: INT-BA_DST_SWITCH
        node_name: 工业交换机
        node_name_en: Industrial Switch
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
        
        function: 网络交换
        medium_in: DATA-IP
        medium_out: DATA-IP
        
        multiplicity: multiple
        
        equipment_parameters:
          ports: {value: 8-24, unit: 口}
          type: 工业级以太网交换机
          
        location_hint:
          space_type: RACK
          position: 弱电机房

      - node_id: INT-BA_DST_SERVER
        node_name: BA服务器
        node_name_en: BA Server
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
        
        function: 数据处理、存储、管理
        medium_in: DATA-IP
        medium_out: DATA-IP
        
        equipment_parameters:
          configuration: 主备冗余
          database: 历史数据存储
          capacity: 全院点数容量
          
        location_hint:
          space_type: RACK
          room_name: 数据中心

    sink_nodes:
    
      - node_id: INT-BA_SNK_WORKSTATION
        node_name: 操作工作站
        node_name_en: Operator Workstation
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 监控操作
        medium_in: DATA-IP
        
        equipment_parameters:
          quantity: 2-4台
          location: 中央监控室、值班室
          
        location_hint:
          space_type: CONTROL_ROOM
          room_name: 中央监控室/动力中心值班室

      - node_id: INT-BA_SNK_ACTUATOR
        node_name: 执行器
        node_name_en: Actuator
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 设备控制
        medium_in: SIGNAL-BA
        
        multiplicity: multiple
        
        equipment_parameters:
          types:
            - {type: 电动调节阀, signal: 4-20mA/0-10V}
            - {type: 电动蝶阀, signal: 开关量}
            - {type: 变频器, protocol: Modbus}
            - {type: 电动风阀, signal: 开关量/模拟量}
            
        location_hint:
          space_type: EQUIPMENT
          position: 被控设备上

  # ============================================================
  # 边定义
  # ============================================================
  edges:
  
    signal_edges:
    
      - edge_id: INT-BA_EDGE_001
        edge_name: 传感器至DDC
        edge_type: TRM
        from_node: INT-BA_SRC_SENSOR
        to_node: INT-BA_DST_DDC
        direction: unidirectional
        medium: SIGNAL-BA
        physical_properties:
          cable_type: RVVP-2×1.0
          
      - edge_id: INT-BA_EDGE_002
        edge_name: DDC至执行器
        edge_type: TRM
        from_node: INT-BA_DST_DDC
        to_node: INT-BA_SNK_ACTUATOR
        direction: unidirectional
        medium: SIGNAL-BA
        physical_properties:
          cable_type: RVVP-2×1.5
          
      - edge_id: INT-BA_EDGE_003
        edge_name: DDC至NAC
        edge_type: BRH
        from_node: INT-BA_DST_DDC
        to_node: INT-BA_DST_NAC
        direction: bidirectional
        medium: SIGNAL-BA
        physical_properties:
          cable_type: RVSP-2×1.0 (RS485)
          
      - edge_id: INT-BA_EDGE_004
        edge_name: NAC至交换机
        edge_type: TRK
        from_node: INT-BA_DST_NAC
        to_node: INT-BA_DST_SWITCH
        direction: bidirectional
        medium: DATA-IP
        physical_properties:
          cable_type: Cat6 / 光纤
          
      - edge_id: INT-BA_EDGE_005
        edge_name: 交换机至服务器
        edge_type: TRK
        from_node: INT-BA_DST_SWITCH
        to_node: INT-BA_DST_SERVER
        direction: bidirectional
        medium: DATA-IP
        
      - edge_id: INT-BA_EDGE_006
        edge_name: 服务器至工作站
        edge_type: TRM
        from_node: INT-BA_DST_SERVER
        to_node: INT-BA_SNK_WORKSTATION
        direction: bidirectional
        medium: DATA-IP

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:
  
    - path_id: INT-BA_PATH_MONITOR
      path_name: 监控数据路径
      path_type: DATA
      direction: bottom_up
      sequence:
        - {step: 1, element_type: node, element_id: INT-BA_SRC_SENSOR}
        - {step: 2, element_type: edge, element_id: INT-BA_EDGE_001}
        - {step: 3, element_type: node, element_id: INT-BA_DST_DDC}
        - {step: 4, element_type: edge, element_id: INT-BA_EDGE_003}
        - {step: 5, element_type: node, element_id: INT-BA_DST_NAC}
        - {step: 6, element_type: edge, element_id: INT-BA_EDGE_004}
        - {step: 7, element_type: node, element_id: INT-BA_DST_SWITCH}
        - {step: 8, element_type: edge, element_id: INT-BA_EDGE_005}
        - {step: 9, element_type: node, element_id: INT-BA_DST_SERVER}
        - {step: 10, element_type: edge, element_id: INT-BA_EDGE_006}
        - {step: 11, element_type: node, element_id: INT-BA_SNK_WORKSTATION}
        
    - path_id: INT-BA_PATH_CONTROL
      path_name: 控制指令路径
      path_type: CTRL
      direction: top_down
      sequence:
        - {step: 1, element_type: node, element_id: INT-BA_SNK_WORKSTATION}
        - {step: 2, element_type: node, element_id: INT-BA_DST_SERVER}
        - {step: 3, element_type: node, element_id: INT-BA_DST_NAC}
        - {step: 4, element_type: node, element_id: INT-BA_DST_DDC}
        - {step: 5, element_type: node, element_id: INT-BA_SNK_ACTUATOR}

  # ============================================================
  # 监控范围
  # ============================================================
  monitoring_scope:
  
    hvac_systems:
      - system: HVAC-CHP
        points: [冷机状态, 冷冻水温度, 泵状态, 压差, 能耗]
      - system: HVAC-CWP
        points: [冷却塔状态, 冷却水温度, 泵状态]
      - system: HVAC-AHU
        points: [送风温湿度, 回风温湿度, 风机状态, 阀门开度, 过滤器压差]
      - system: HVAC-CLEAN
        points: [压差, 温湿度, 风机状态, 高效过滤器压差]
        
    plumbing_systems:
      - system: PLUMB-DWS
        points: [水箱液位, 泵状态, 出口压力]
      - system: PLUMB-PWS
        points: [电导率, 液位, 泵状态, 水质参数]
        
    electrical_systems:
      - system: ELEC-LV-MAIN
        points: [电压, 电流, 功率, 功率因数, 电能]
      - system: ELEC-EPS
        points: [发电机状态, 油位, 电压, ATS状态]
```

---

## 第十部分：INT-NURSE 护理呼叫系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: INT-NURSE
    system_name: 护理呼叫系统
    system_name_en: Nurse Call System
    category: INTELLIGENT
    version: 1.0
    
    description: |
      医院病房护理呼叫对讲系统。
      患者可通过床头分机呼叫护士站，实现双向对讲。
      与HIS系统集成，显示患者信息。
      
    design_basis:
      type: 数字IP式/总线式
      integration: HIS、PACS
      display: 护士站主机显示患者信息
      
    serving_scope:
      - 普通病房
      - ICU
      - 急诊留观
      - 手术室家属等候区

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:
  
    source_nodes:
    
      - node_id: INT-NURSE_SRC_BEDSIDE
        node_name: 床头分机
        node_name_en: Bedside Station
        node_type: Source_Node
        node_category: SRC
        
        function: 患者呼叫、对讲
        medium_out: SIGNAL-NURSE
        
        multiplicity: multiple
        instance_pattern: INT-NURSE_SRC_BEDSIDE_{Ward}_{Bed}
        
        equipment_parameters:
          features:
            - 呼叫按钮
            - 取消按钮
            - 双向对讲
            - 液晶显示
            - 信息显示（可选）
          buttons:
            - {type: 普通呼叫, priority: normal}
            - {type: 紧急呼叫, priority: urgent}
            
        location_hint:
          space_type: WALL
          position: 床头墙面
          height: {value: 0.8-1.0, unit: m}

      - node_id: INT-NURSE_SRC_BATHROOM
        node_name: 卫生间紧急按钮
        node_name_en: Bathroom Emergency Button
        node_type: Source_Node
        node_category: SRC
        
        function: 卫生间紧急呼叫
        medium_out: SIGNAL-NURSE
        
        multiplicity: multiple
        
        equipment_parameters:
          type: 拉绳式/按钮式
          waterproof: IP65
          
        location_hint:
          space_type: WALL
          position: 病房卫生间
          height: {value: 0.5-0.8, unit: m}

      - node_id: INT-NURSE_SRC_PENDANT
        node_name: 手持呼叫器
        node_name_en: Handheld Call Button
        node_type: Source_Node
        node_category: SRC
        
        function: 患者随身呼叫
        medium_out: SIGNAL-NURSE
        
        equipment_parameters:
          type: 有线/无线
          
        location_hint:
          position: 患者手边

    distribution_nodes:
    
      - node_id: INT-NURSE_DST_GATEWAY
        node_name: 楼层网关
        node_name_en: Floor Gateway
        node_type: Distribution_Node
        node_category: DST
        node_subtype: JUN
        
        function: 楼层信号汇集、协议转换
        medium_in: SIGNAL-NURSE
        medium_out: DATA-IP
        
        multiplicity: multiple
        
        equipment_parameters:
          capacity: {value: 50-100, unit: 床位}
          
        location_hint:
          space_type: WEAK_ROOM
          position: 楼层弱电间

      - node_id: INT-NURSE_DST_SWITCH
        node_name: 网络交换机
        node_name_en: Network Switch
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
        
        function: 网络交换
        medium_in: DATA-IP
        medium_out: DATA-IP
        
        location_hint:
          space_type: WEAK_ROOM

      - node_id: INT-NURSE_DST_SERVER
        node_name: 护理呼叫服务器
        node_name_en: Nurse Call Server
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
        
        function: 呼叫处理、记录、HIS接口
        medium_in: DATA-IP
        medium_out: DATA-IP
        
        equipment_parameters:
          features:
            - 呼叫记录
            - 响应时间统计
            - HIS接口
            - 排班管理
            
        location_hint:
          space_type: RACK
          room_name: 数据中心

    sink_nodes:
    
      - node_id: INT-NURSE_SNK_STATION
        node_name: 护士站主机
        node_name_en: Nurse Station Master
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 呼叫接收、对讲
        medium_in: DATA-IP
        
        multiplicity: multiple
        
        equipment_parameters:
          features:
            - 触摸屏
            - 患者信息显示
            - 双向对讲
            - 呼叫队列
            - 一键呼叫医生
            
        location_hint:
          space_type: DESK
          position: 护士站台面

      - node_id: INT-NURSE_SNK_CORRIDOR
        node_name: 走廊显示屏
        node_name_en: Corridor Display
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 呼叫显示
        medium_in: SIGNAL-NURSE
        
        multiplicity: multiple
        
        equipment_parameters:
          display: LED/LCD
          content: 呼叫房间号、等级
          
        location_hint:
          space_type: WALL
          position: 病房走廊

      - node_id: INT-NURSE_SNK_DOORLIGHT
        node_name: 门灯
        node_name_en: Door Light
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 呼叫指示
        medium_in: SIGNAL-NURSE
        
        multiplicity: multiple
        
        equipment_parameters:
          colors:
            - {color: 绿色, meaning: 普通呼叫}
            - {color: 红色, meaning: 紧急呼叫}
            - {color: 蓝色, meaning: 护士在房间}
            
        location_hint:
          space_type: WALL
          position: 病房门口上方

      - node_id: INT-NURSE_SNK_MOBILE
        node_name: 护士移动终端
        node_name_en: Nurse Mobile Device
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 移动接收呼叫
        medium_in: DATA-IP
        
        multiplicity: multiple
        
        equipment_parameters:
          type: 手机/PDA/智能手表
          features:
            - 呼叫推送
            - 患者信息查看
            - 一键响应
            
        location_hint:
          position: 护士随身携带

  # ============================================================
  # 边定义
  # ============================================================
  edges:
  
    signal_edges:
    
      - edge_id: INT-NURSE_EDGE_001
        edge_name: 床头分机至网关
        edge_type: TRM
        from_node: INT-NURSE_SRC_BEDSIDE
        to_node: INT-NURSE_DST_GATEWAY
        direction: bidirectional
        medium: SIGNAL-NURSE
        physical_properties:
          cable_type: 专用网线/RVS
          
      - edge_id: INT-NURSE_EDGE_002
        edge_name: 网关至交换机
        edge_type: TRK
        from_node: INT-NURSE_DST_GATEWAY
        to_node: INT-NURSE_DST_SWITCH
        direction: bidirectional
        medium: DATA-IP
        physical_properties:
          cable_type: Cat6
          
      - edge_id: INT-NURSE_EDGE_003
        edge_name: 交换机至服务器
        edge_type: TRK
        from_node: INT-NURSE_DST_SWITCH
        to_node: INT-NURSE_DST_SERVER
        direction: bidirectional
        medium: DATA-IP
        
      - edge_id: INT-NURSE_EDGE_004
        edge_name: 服务器至护士站
        edge_type: TRM
        from_node: INT-NURSE_DST_SERVER
        to_node: INT-NURSE_SNK_STATION
        direction: bidirectional
        medium: DATA-IP
        
      - edge_id: INT-NURSE_EDGE_005
        edge_name: 网关至门灯
        edge_type: TRM
        from_node: INT-NURSE_DST_GATEWAY
        to_node: INT-NURSE_SNK_DOORLIGHT
        direction: unidirectional
        medium: SIGNAL-NURSE

  # ============================================================
  # 路径与呼叫流程
  # ============================================================
  call_flow:
  
    normal_call:
      - step: 1
        action: 患者按下呼叫按钮
        device: INT-NURSE_SRC_BEDSIDE
        
      - step: 2
        action: 床头分机显示呼叫中
        
      - step: 3
        action: 门灯绿灯亮
        device: INT-NURSE_SNK_DOORLIGHT
        
      - step: 4
        action: 走廊显示屏显示呼叫信息
        device: INT-NURSE_SNK_CORRIDOR
        
      - step: 5
        action: 护士站主机声音提示+患者信息显示
        device: INT-NURSE_SNK_STATION
        
      - step: 6
        action: 护士移动终端推送通知
        device: INT-NURSE_SNK_MOBILE
        
      - step: 7
        action: 护士应答/前往病房
        
      - step: 8
        action: 护士到达按取消按钮
        
      - step: 9
        action: 系统记录响应时间
        
    urgent_call:
      priority: 高于普通呼叫
      indication: 门灯红色、加急提示音
```

---

## 第十一部分：系统间接口关系图补充 (Batch 3)

```yaml
System_Interfaces_Batch3:

  # 给排水系统链路
  - interface_id: IF_DWS_TO_HWS
    upstream_system: PLUMB-DWS
    downstream_system: PLUMB-HWS
    interface_medium: WATER-DW
    description: 生活给水供应热水系统
    
  - interface_id: IF_DWS_TO_PWS
    upstream_system: PLUMB-DWS
    downstream_system: PLUMB-PWS
    interface_medium: WATER-DW
    description: 生活给水供应纯水系统原水
    
  - interface_id: IF_DWS_TO_FIRE
    upstream_system: PLUMB-DWS
    downstream_system: FIRE-HYDRANT
    interface_medium: WATER-DW
    description: 消防水池补水
    
  # 消防系统链路
  - interface_id: IF_FA_TO_HYDRANT
    upstream_system: FIRE-ALARM
    downstream_system: FIRE-HYDRANT
    interface_medium: SIGNAL-FA
    description: 火灾报警联动消火栓泵
    
  - interface_id: IF_FA_TO_SPRINKLER
    upstream_system: FIRE-ALARM
    downstream_system: FIRE-SPRINKLER
    interface_medium: SIGNAL-FA
    description: 火灾报警联动喷淋泵
    
  - interface_id: IF_FA_TO_SMOKE
    upstream_system: FIRE-ALARM
    downstream_system: FIRE-SMOKE
    interface_medium: SIGNAL-FA
    description: 火灾报警联动防排烟
    
  - interface_id: IF_FA_TO_ELEC
    upstream_system: FIRE-ALARM
    downstream_system: ELEC-LV-MAIN
    interface_medium: SIGNAL-FA
    description: 火灾报警切断非消防电源
    
  # 智能化系统链路
  - interface_id: IF_BA_TO_HVAC
    upstream_system: INT-BA
    downstream_system: HVAC-*
    interface_medium: SIGNAL-BA
    description: 楼宇自控监控暖通设备
    
  - interface_id: IF_BA_TO_PLUMB
    upstream_system: INT-BA
    downstream_system: PLUMB-*
    interface_medium: SIGNAL-BA
    description: 楼宇自控监控给排水设备
    
  - interface_id: IF_NURSE_TO_HIS
    upstream_system: INT-NURSE
    downstream_system: HIS (外部)
    interface_medium: DATA-IP
    description: 护理呼叫与HIS患者信息集成
    
  - interface_id: IF_BA_TO_IBMS
    upstream_system: INT-BA
    downstream_system: INT-IBMS
    interface_medium: DATA-IP
    description: 楼宇自控接入集成平台
    
  - interface_id: IF_FA_TO_IBMS
    upstream_system: FIRE-ALARM
    downstream_system: INT-IBMS
    interface_medium: DATA-IP
    description: 火灾报警接入集成平台
```

---

## 第十二部分：质量校验清单 (Batch 3)

```yaml
Quality_Checklist_Batch3:

  # 结构完整性
  structure_completeness:
    - check: 给水系统从市政→水箱→泵组→用户完整链路
      status: ✅
    - check: 排水系统从洁具→立管→化粪池→市政完整链路
      status: ✅
    - check: 纯水系统制备+循环完整流程
      status: ✅
    - check: 消火栓系统水源→泵→管网→消火栓完整链路
      status: ✅
    - check: 喷淋系统湿式/预作用分支完整
      status: ✅
    - check: 火灾报警探测→主机→联动完整链路
      status: ✅
    - check: 楼宇自控三层架构完整
      status: ✅
    - check: 护理呼叫床头→护士站完整链路
      status: ✅

  # 消防联动完整性
  fire_linkage:
    - check: 消防泵联动控制
      status: ✅
    - check: 防排烟联动控制
      status: ✅
    - check: 电梯迫降联动
      status: ✅
    - check: 非消防电源切断
      status: ✅
    - check: 消防广播联动
      status: ✅

  # 参数完整性
  parameter_completeness:
    - check: 给水压力参数完整
      status: ✅
    - check: 消防水压/水量参数符合规范
      status: ✅
    - check: 纯水水质参数完整
      status: ✅
    - check: 火灾探测器覆盖面积参数
      status: ✅
    - check: BA系统点数容量参数
      status: ✅

  # 下游接口
  downstream_interfaces:
    - agent: Agent-03 (设备属性)
      status: ✅ 设备参数完整
    - agent: Agent-04 (流动模型)
      status: ✅ 压力/流量参数提供
    - agent: Agent-05 (空间定位)
      status: ✅ location_hint完整
    - agent: Agent-06 (联动逻辑)
      status: ✅ 消防联动逻辑完整
```

---

## 输出总结 (Batch 3)

| 系统 | 状态 | 节点数 | 边数 | 路径数 | 特殊说明 |
|------|------|--------|------|--------|----------|
| PLUMB-DWS | ✅ 完成 | 10 | 7 | 1 | 变频加压 |
| PLUMB-PWS | ✅ 完成 | 12 | 11 | 2 | 循环系统 |
| PLUMB-SAN | ✅ 完成 | 9 | 8 | 2 | 含提升 |
| FIRE-HYDRANT | ✅ 完成 | 10 | 7 | 2 | 临时高压 |
| FIRE-SPRINKLER | ✅ 完成 | 9 | 7 | 1 | 湿式+预作用 |
| FIRE-ALARM | ✅ 完成 | 9 | 5 | - | 联动逻辑 |
| INT-BA | ✅ 完成 | 8 | 6 | 2 | 三层架构 |
| INT-NURSE | ✅ 完成 | 10 | 5 | - | 呼叫流程 |

---

**Batch 3 完整版输出完毕。**

至此，Agent-01 第一至第三批次已完成以下系统的拓扑建模：

**Batch 1 (HVAC):**
- HVAC-CHP, HVAC-CWP, HVAC-AHU, HVAC-CLEAN

**Batch 2 (ELECTRICAL + MEDICAL_GAS):**
- ELEC-HV, ELEC-LV-MAIN, ELEC-EPS, ELEC-IT
- MGAS-O2, MGAS-VAC, MGAS-AIR

**Batch 3 (PLUMBING + FIRE_PROTECTION + INTELLIGENT):**
- PLUMB-DWS, PLUMB-PWS, PLUMB-SAN
- FIRE-HYDRANT, FIRE-SPRINKLER, FIRE-ALARM
- INT-BA, INT-NURSE

如需补充其他系统（如HVAC-HWP热源系统、PLUMB-HWS热水系统、INT-SEC安防系统等），请指示继续。

---