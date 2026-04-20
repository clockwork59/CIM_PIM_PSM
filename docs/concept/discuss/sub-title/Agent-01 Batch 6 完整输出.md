## 🧑‍💻 User


继续

---
## 🤖 Assistant


# Agent-01 Batch 6 完整输出

## Batch 6 系统清单

```yaml
Batch_6_Systems:
  
  category: P2-IMPORTANT 剩余系统 + P3-OPTIONAL 可选系统
  
  systems:
    # P2 剩余
    - HVAC-VENT: 普通通风系统
    - INT-CLOCK: 时钟系统
    - INT-IBMS: 智能化集成平台
    
    # P3 可选
    - PLUMB-STORM: 雨水排水系统
    - PLUMB-RW: 中水回用系统
    - INT-IPTV: 病房电视系统
    - MGAS-N2: 氮气系统
    - MGAS-CO2: 二氧化碳系统
```

---

## 6.1 HVAC-VENT 普通通风系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: HVAC-VENT
    system_name: 普通通风系统
    system_name_en: General Ventilation System
    category: HVAC
    version: 1.0
    
    description: |
      医院普通机械通风系统，用于无空调要求但需要通风换气的区域。
      包括卫生间排风、设备房通风、厨房排风等。
      
    design_basis:
      bathroom_exhaust: {value: 10-15, unit: ACH}
      equipment_room: {value: 6-12, unit: ACH}
      kitchen_exhaust: 按灶台计算
      garage: {value: 6, unit: ACH}
      
    serving_scope:
      - 公共卫生间
      - 设备用房
      - 地下车库
      - 污物间
      - 库房

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: HVAC-VENT_BND_IN_OA
        boundary_name: 室外空气
        medium: AIR-OA
        is_external: true
        
      - boundary_id: HVAC-VENT_BND_IN_ELEC
        boundary_name: 电源
        medium: ELEC-LV
        source_system: ELEC-LV-MAIN
        
    outputs:
      - boundary_id: HVAC-VENT_BND_OUT_EA
        boundary_name: 排风
        medium: AIR-EA
        is_external: true
        target: 大气

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:
  
    source_nodes:
    
      - node_id: HVAC-VENT_SRC_OA
        node_name: 补风入口
        node_name_en: Makeup Air Inlet
        node_type: Source_Node
        node_category: SRC
        
        function: 补充新风
        medium_out: AIR-OA
        is_external: true
        
        equipment_parameters:
          type: 防雨百叶
          
        location_hint:
          space_type: EXTERIOR
          position: 外墙

      - node_id: HVAC-VENT_SRC_ROOM_AIR
        node_name: 室内空气
        node_name_en: Room Air
        node_type: Source_Node
        node_category: SRC
        
        function: 待排出空气
        medium_out: AIR-RA
        
        location_hint:
          space_type: ROOM
          position: 需通风区域

    distribution_nodes:
    
      - node_id: HVAC-VENT_DST_EXHAUST_FAN
        node_name: 排风机
        node_name_en: Exhaust Fan
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 机械排风
        medium_in: AIR-RA
        medium_out: AIR-EA
        
        multiplicity: multiple
        instance_pattern: HVAC-VENT_DST_EXHAUST_FAN_{Zone}_{Seq}
        
        equipment_parameters:
          types:
            - {type: 离心风机, application: 大风量排风}
            - {type: 轴流风机, application: 竖井排风}
            - {type: 混流风机, application: 中等风量}
            - {type: 管道风机, application: 小风量}
          air_flow: {value: 1000-20000, unit: m³/h}
          pressure: {value: 200-500, unit: Pa}
          
        location_hint:
          space_type: MEP_ROOM / EXTERIOR
          position: 屋顶/设备间
          
        control_points:
          status:
            - {point_id: EF_RUN, type: DI, description: 运行状态}
            - {point_id: EF_FAULT, type: DI, description: 故障报警}
          commands:
            - {point_id: EF_START, type: DO, description: 启停控制}

      - node_id: HVAC-VENT_DST_SUPPLY_FAN
        node_name: 送风机/补风机
        node_name_en: Supply/Makeup Fan
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 补风送入
        medium_in: AIR-OA
        medium_out: AIR-SA
        
        multiplicity: multiple
        
        equipment_parameters:
          types:
            - {type: 离心风机, application: 设备房补风}
            - {type: 轴流风机, application: 车库补风}
          air_flow: {value: 1000-30000, unit: m³/h}
          
        location_hint:
          space_type: MEP_ROOM / EXTERIOR
          position: 补风机房/进风井
          
        control_points:
          status:
            - {point_id: SF_RUN, type: DI, description: 运行状态}
          commands:
            - {point_id: SF_START, type: DO, description: 启停控制}

      - node_id: HVAC-VENT_DST_EXHAUST_DUCT
        node_name: 排风管道
        node_name_en: Exhaust Duct
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
        
        function: 排风输送
        medium_in: AIR-RA
        medium_out: AIR-EA
        
        multiplicity: multiple
        
        equipment_parameters:
          material: 镀锌钢板/玻璃钢（腐蚀环境）
          
        location_hint:
          space_type: CEILING_VOID / SHAFT
          position: 吊顶内/竖井

      - node_id: HVAC-VENT_DST_EXHAUST_GRILLE
        node_name: 排风口
        node_name_en: Exhaust Grille
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRM
        
        function: 排风入口
        medium_in: AIR-RA
        medium_out: AIR-RA
        
        multiplicity: multiple
        
        equipment_parameters:
          types:
            - {type: 单层百叶, application: 墙面}
            - {type: 方形散流器, application: 吊顶}
            - {type: 条缝风口, application: 吊顶}
          
        location_hint:
          space_type: WALL / CEILING
          position: 卫生间/设备间

      - node_id: HVAC-VENT_DST_TOILET_FAN
        node_name: 卫生间排风机
        node_name_en: Toilet Exhaust Fan
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 卫生间排风
        medium_in: AIR-RA
        medium_out: AIR-EA
        
        multiplicity: multiple
        instance_pattern: HVAC-VENT_DST_TOILET_FAN_{Zone}
        
        equipment_parameters:
          type: 静音管道风机/离心风机
          air_flow: {value: 500-5000, unit: m³/h}
          noise: {value: "≤45", unit: dB(A)}
          control: 定时/感应控制
          
        location_hint:
          space_type: CEILING_VOID / SHAFT
          position: 卫生间吊顶上方
          
        control_points:
          status:
            - {point_id: TF_RUN, type: DI, description: 运行状态}
          commands:
            - {point_id: TF_START, type: DO, description: 启停控制}

      - node_id: HVAC-VENT_DST_GARAGE_FAN
        node_name: 车库通风机
        node_name_en: Garage Ventilation Fan
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 地下车库通风
        medium_in: [AIR-RA, AIR-OA]
        medium_out: [AIR-EA, AIR-SA]
        
        multiplicity: multiple
        
        equipment_parameters:
          type: 诱导风机+排风机组合
          components:
            - 排风机
            - 补风机
            - 诱导风机
          control: CO浓度联动
          
        location_hint:
          space_type: CEILING
          position: 地下车库
          
        control_points:
          sensors:
            - {point_id: CO_CONC, type: AI, description: CO浓度}
          status:
            - {point_id: GF_RUN, type: DI, description: 运行状态}
          commands:
            - {point_id: GF_START, type: DO, description: 启停控制}

    sink_nodes:
    
      - node_id: HVAC-VENT_SNK_EXHAUST
        node_name: 排风出口
        node_name_en: Exhaust Outlet
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 污浊空气排放
        medium_in: AIR-EA
        is_external: true
        
        equipment_parameters:
          type: 屋顶风帽/排风百叶
          
        location_hint:
          space_type: EXTERIOR
          position: 屋顶/外墙

      - node_id: HVAC-VENT_SNK_ROOM
        node_name: 通风区域
        node_name_en: Ventilated Zone
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 补风供应
        medium_in: AIR-SA
        
        multiplicity: multiple
        
        typical_zones:
          - 设备用房
          - 地下车库
          - 厨房

  # ============================================================
  # 边定义
  # ============================================================
  edges:
  
    exhaust_edges:
    
      - edge_id: HVAC-VENT_EDGE_EX_001
        edge_name: 室内空气至排风口
        edge_type: TRM
        from_node: HVAC-VENT_SRC_ROOM_AIR
        to_node: HVAC-VENT_DST_EXHAUST_GRILLE
        direction: unidirectional
        medium: AIR-RA
        
      - edge_id: HVAC-VENT_EDGE_EX_002
        edge_name: 排风口至排风管
        edge_type: TRK
        from_node: HVAC-VENT_DST_EXHAUST_GRILLE
        to_node: HVAC-VENT_DST_EXHAUST_DUCT
        direction: unidirectional
        medium: AIR-RA
        
      - edge_id: HVAC-VENT_EDGE_EX_003
        edge_name: 排风管至排风机
        edge_type: TRK
        from_node: HVAC-VENT_DST_EXHAUST_DUCT
        to_node: HVAC-VENT_DST_EXHAUST_FAN
        direction: unidirectional
        medium: AIR-RA
        
      - edge_id: HVAC-VENT_EDGE_EX_004
        edge_name: 排风机至排放口
        edge_type: TRK
        from_node: HVAC-VENT_DST_EXHAUST_FAN
        to_node: HVAC-VENT_SNK_EXHAUST
        direction: unidirectional
        medium: AIR-EA

    supply_edges:
    
      - edge_id: HVAC-VENT_EDGE_SP_001
        edge_name: 新风入口至补风机
        edge_type: TRK
        from_node: HVAC-VENT_SRC_OA
        to_node: HVAC-VENT_DST_SUPPLY_FAN
        direction: unidirectional
        medium: AIR-OA
        
      - edge_id: HVAC-VENT_EDGE_SP_002
        edge_name: 补风机至通风区域
        edge_type: TRM
        from_node: HVAC-VENT_DST_SUPPLY_FAN
        to_node: HVAC-VENT_SNK_ROOM
        direction: unidirectional
        medium: AIR-SA

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:
  
    - path_id: HVAC-VENT_PATH_EXHAUST
      path_name: 排风路径
      path_type: EXH
      sequence:
        - {step: 1, element_type: node, element_id: HVAC-VENT_SRC_ROOM_AIR}
        - {step: 2, element_type: node, element_id: HVAC-VENT_DST_EXHAUST_GRILLE}
        - {step: 3, element_type: node, element_id: HVAC-VENT_DST_EXHAUST_DUCT}
        - {step: 4, element_type: node, element_id: HVAC-VENT_DST_EXHAUST_FAN}
        - {step: 5, element_type: node, element_id: HVAC-VENT_SNK_EXHAUST}

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:
  
    toilet_exhaust:
      modes:
        - {mode: 定时控制, schedule: "06:00-22:00连续运行"}
        - {mode: 感应控制, trigger: 人体感应器}
        - {mode: 手动控制, location: 卫生间开关}
        
    garage_ventilation:
      co_control:
        low_speed:
          condition: CO < 25ppm
          action: 低速运行或停止
        high_speed:
          condition: CO ≥ 25ppm
          action: 高速运行
        emergency:
          condition: CO ≥ 150ppm
          action: 全速运行 + 报警
          
    equipment_room:
      temperature_control:
        trigger: 室温 > 35℃
        action: 启动通风机
        stop: 室温 < 30℃
```

---

## 6.2 INT-CLOCK 时钟系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: INT-CLOCK
    system_name: 时钟系统
    system_name_en: Master Clock System
    category: INTELLIGENT
    version: 1.0
    
    description: |
      医院母钟系统，为全院提供统一、精确的标准时间。
      对医疗记录、用药时间、手术计时等具有重要意义。
      
    design_basis:
      accuracy: {value: "±0.5", unit: "秒/天"}
      sync_source: GPS/北斗/NTP
      display: 模拟/数字时钟
      
    serving_scope:
      - 手术室
      - ICU
      - 急诊
      - 护士站
      - 公共区域
      - 信息系统

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: INT-CLOCK_BND_IN_GPS
        boundary_name: GPS/北斗信号
        medium: SIGNAL-TIME
        is_external: true
        source: 卫星
        
      - boundary_id: INT-CLOCK_BND_IN_NET
        boundary_name: 网络接入
        medium: DATA-IP
        source_system: INT-NET
        
      - boundary_id: INT-CLOCK_BND_IN_ELEC
        boundary_name: 电源
        medium: ELEC-LV
        source_system: ELEC-LV-MAIN
        
    outputs:
      - boundary_id: INT-CLOCK_BND_OUT_TIME
        boundary_name: 标准时间信号
        medium: SIGNAL-TIME
        target: 子钟/信息系统

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:
  
    source_nodes:
    
      - node_id: INT-CLOCK_SRC_GPS
        node_name: GPS/北斗接收器
        node_name_en: GPS/BeiDou Receiver
        node_type: Source_Node
        node_category: SRC
        
        function: 卫星时间接收
        medium_out: SIGNAL-TIME
        is_external: true
        
        equipment_parameters:
          type: GPS/北斗双模接收机
          accuracy: {value: "±50", unit: ns}
          antenna: 室外安装
          
        location_hint:
          space_type: EXTERIOR
          position: 屋顶
          requirement: 开阔无遮挡

    distribution_nodes:
    
      - node_id: INT-CLOCK_DST_MASTER
        node_name: 母钟
        node_name_en: Master Clock
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
        
        function: 时间基准与分发
        medium_in: SIGNAL-TIME
        medium_out: SIGNAL-TIME
        
        equipment_parameters:
          type: 网络母钟
          time_source:
            - GPS/北斗
            - NTP服务器
            - 恒温晶振（后备）
          accuracy: {value: "±0.5", unit: "秒/天"}
          holdover: {value: 72, unit: h, note: 失去外部时间源后}
          outputs:
            - NTP/SNTP
            - RS485
            - 脉冲输出
            - IRIG-B
          redundancy: 双机热备
          
        location_hint:
          space_type: RACK
          room_name: 弱电机房
          
        control_points:
          sensors:
            - {point_id: CLOCK_OFFSET, type: AI, description: 时间偏差}
          status:
            - {point_id: CLOCK_GPS, type: DI, description: GPS锁定状态}
            - {point_id: CLOCK_SYNC, type: DI, description: 同步状态}
            - {point_id: CLOCK_FAULT, type: DI, description: 故障报警}

      - node_id: INT-CLOCK_DST_NTP_SERVER
        node_name: NTP时间服务器
        node_name_en: NTP Time Server
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
        
        function: 网络时间协议服务
        medium_in: SIGNAL-TIME
        medium_out: DATA-IP
        
        equipment_parameters:
          type: NTP服务器
          stratum: 1
          clients: 无限制
          protocol: NTP v4 / SNTP
          
        location_hint:
          space_type: RACK
          room_name: 数据中心
          
        note: 可与母钟集成或独立

      - node_id: INT-CLOCK_DST_DRIVER
        node_name: 子钟驱动器
        node_name_en: Slave Clock Driver
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
        
        function: 子钟信号分配
        medium_in: SIGNAL-TIME
        medium_out: SIGNAL-TIME
        
        multiplicity: multiple
        
        equipment_parameters:
          type: 子钟驱动模块
          capacity: {value: 30-50, unit: 台子钟}
          signal: RS485/脉冲
          
        location_hint:
          space_type: RACK
          room_name: 弱电机房/楼层弱电间

      - node_id: INT-CLOCK_DST_LINE
        node_name: 时钟总线
        node_name_en: Clock Bus
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
        
        function: 时钟信号传输
        medium_in: SIGNAL-TIME
        medium_out: SIGNAL-TIME
        
        multiplicity: multiple
        
        equipment_parameters:
          type: RS485总线/双绞线
          topology: 总线型
          
        location_hint:
          space_type: CABLE_TRAY
          position: 吊顶桥架

    sink_nodes:
    
      - node_id: INT-CLOCK_SNK_ANALOG
        node_name: 模拟子钟
        node_name_en: Analog Slave Clock
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 时间显示
        medium_in: SIGNAL-TIME
        
        multiplicity: multiple
        instance_pattern: INT-CLOCK_SNK_ANALOG_{Floor}_{Seq}
        
        equipment_parameters:
          type: 单面/双面模拟时钟
          diameter: {value: 300-500, unit: mm}
          display: 时/分/秒
          
        location_hint:
          space_type: WALL
          position: 走廊/大厅
          
        typical_locations:
          - 门诊大厅
          - 住院部大厅
          - 走廊
          - 等候区

      - node_id: INT-CLOCK_SNK_DIGITAL
        node_name: 数字子钟
        node_name_en: Digital Slave Clock
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 时间显示
        medium_in: SIGNAL-TIME
        
        multiplicity: multiple
        instance_pattern: INT-CLOCK_SNK_DIGITAL_{Floor}_{Seq}
        
        equipment_parameters:
          type: LED数字时钟
          display: 时:分:秒 + 日期
          features:
            - 日期显示
            - 温湿度显示（可选）
            - 倒计时功能（手术室）
            
        location_hint:
          space_type: WALL
          
        typical_locations:
          - 手术室
          - ICU
          - 急诊抢救室
          - 护士站

      - node_id: INT-CLOCK_SNK_OR_TIMER
        node_name: 手术室计时器
        node_name_en: OR Timer
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 手术计时
        medium_in: SIGNAL-TIME
        
        multiplicity: multiple
        
        equipment_parameters:
          type: 手术计时系统
          functions:
            - 标准时间显示
            - 手术时长计时
            - 麻醉时长计时
            - 分段计时
            - 倒计时
            
        location_hint:
          space_type: WALL
          position: 手术室观察窗旁

      - node_id: INT-CLOCK_SNK_IT_SYSTEM
        node_name: 信息系统
        node_name_en: IT System
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 系统时间同步
        medium_in: DATA-IP
        
        multiplicity: multiple
        
        equipment_parameters:
          types:
            - HIS服务器
            - PACS服务器
            - 门禁系统
            - 安防系统
            - BA系统
          protocol: NTP
          
        location_hint:
          space_type: RACK
          room_name: 数据中心

  # ============================================================
  # 边定义
  # ============================================================
  edges:
  
    time_source_edges:
    
      - edge_id: INT-CLOCK_EDGE_GPS_001
        edge_name: GPS至母钟
        edge_type: TRK
        from_node: INT-CLOCK_SRC_GPS
        to_node: INT-CLOCK_DST_MASTER
        direction: unidirectional
        medium: SIGNAL-TIME
        physical_properties:
          cable: 同轴电缆

    distribution_edges:
    
      - edge_id: INT-CLOCK_EDGE_DIST_001
        edge_name: 母钟至NTP服务器
        edge_type: TRK
        from_node: INT-CLOCK_DST_MASTER
        to_node: INT-CLOCK_DST_NTP_SERVER
        direction: unidirectional
        medium: SIGNAL-TIME
        
      - edge_id: INT-CLOCK_EDGE_DIST_002
        edge_name: 母钟至驱动器
        edge_type: TRK
        from_node: INT-CLOCK_DST_MASTER
        to_node: INT-CLOCK_DST_DRIVER
        direction: unidirectional
        medium: SIGNAL-TIME
        
      - edge_id: INT-CLOCK_EDGE_DIST_003
        edge_name: 驱动器至总线
        edge_type: BRH
        from_node: INT-CLOCK_DST_DRIVER
        to_node: INT-CLOCK_DST_LINE
        direction: unidirectional
        medium: SIGNAL-TIME

    terminal_edges:
    
      - edge_id: INT-CLOCK_EDGE_TERM_001
        edge_name: 总线至模拟子钟
        edge_type: TRM
        from_node: INT-CLOCK_DST_LINE
        to_node: INT-CLOCK_SNK_ANALOG
        direction: unidirectional
        medium: SIGNAL-TIME
        
      - edge_id: INT-CLOCK_EDGE_TERM_002
        edge_name: 总线至数字子钟
        edge_type: TRM
        from_node: INT-CLOCK_DST_LINE
        to_node: INT-CLOCK_SNK_DIGITAL
        direction: unidirectional
        medium: SIGNAL-TIME
        
      - edge_id: INT-CLOCK_EDGE_TERM_003
        edge_name: NTP至信息系统
        edge_type: TRM
        from_node: INT-CLOCK_DST_NTP_SERVER
        to_node: INT-CLOCK_SNK_IT_SYSTEM
        direction: unidirectional
        medium: DATA-IP

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:
  
    - path_id: INT-CLOCK_PATH_SLAVE
      path_name: 子钟同步路径
      path_type: SYNC
      sequence:
        - {step: 1, element_type: node, element_id: INT-CLOCK_SRC_GPS}
        - {step: 2, element_type: node, element_id: INT-CLOCK_DST_MASTER}
        - {step: 3, element_type: node, element_id: INT-CLOCK_DST_DRIVER}
        - {step: 4, element_type: node, element_id: INT-CLOCK_DST_LINE}
        - {step: 5, element_type: node, element_id: INT-CLOCK_SNK_DIGITAL}
        
    - path_id: INT-CLOCK_PATH_NTP
      path_name: NTP同步路径
      path_type: SYNC
      sequence:
        - {step: 1, element_type: node, element_id: INT-CLOCK_SRC_GPS}
        - {step: 2, element_type: node, element_id: INT-CLOCK_DST_MASTER}
        - {step: 3, element_type: node, element_id: INT-CLOCK_DST_NTP_SERVER}
        - {step: 4, element_type: node, element_id: INT-CLOCK_SNK_IT_SYSTEM}

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:
  
    time_source_selection:
      priority:
        - GPS/北斗
        - NTP上级服务器
        - 本地晶振
      failover: 自动切换
      
    sync_interval:
      slave_clocks: {value: 1, unit: min}
      ntp_clients: {value: 64-1024, unit: s, note: 动态调整}
      
    alarm_management:
      gps_loss:
        condition: GPS信号丢失
        action: 切换至晶振保持模式
        alarm: 告警
        
      sync_failure:
        condition: 子钟失步
        action: 重新同步
        alarm: 告警
```

---

## 6.3 INT-IBMS 智能化集成平台拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: INT-IBMS
    system_name: 智能化集成平台
    system_name_en: Intelligent Building Management System
    category: INTELLIGENT
    version: 1.0
    
    description: |
      医院智能化集成管理平台（IBMS），集成楼宇自控、安防、消防、
      医疗信息等多个子系统，实现统一监控、联动控制和数据分析。
      
    design_basis:
      integration_mode:
        - 深度集成（API/数据库）
        - 协议集成（BACnet/OPC等）
        - 硬接点集成
      visualization: 2D/3D可视化
      analysis: 能耗分析、运维分析
      
    integrated_systems:
      - INT-BA: 楼宇自控
      - INT-SEC: 安防系统
      - FIRE-ALARM: 消防报警
      - ELEC-LV-MAIN: 配电监控
      - MGAS: 医气监控
      - INT-PA: 公共广播
      - INT-CLOCK: 时钟系统

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: INT-IBMS_BND_IN_BA
        boundary_name: 楼宇自控数据
        medium: DATA-IP
        source_system: INT-BA
        protocol: BACnet/IP, OPC-UA
        
      - boundary_id: INT-IBMS_BND_IN_SEC
        boundary_name: 安防系统数据
        medium: DATA-IP
        source_system: INT-SEC
        
      - boundary_id: INT-IBMS_BND_IN_FA
        boundary_name: 消防报警数据
        medium: DATA-IP
        source_system: FIRE-ALARM
        
      - boundary_id: INT-IBMS_BND_IN_ELEC
        boundary_name: 配电监控数据
        medium: DATA-IP
        source_system: ELEC-LV-MAIN
        
      - boundary_id: INT-IBMS_BND_IN_NET
        boundary_name: 网络接入
        medium: DATA-IP
        source_system: INT-NET
        
    outputs:
      - boundary_id: INT-IBMS_BND_OUT_DISPLAY
        boundary_name: 可视化展示
        medium: SIGNAL-VIDEO
        target: 监控大屏/Web端/移动端
        
      - boundary_id: INT-IBMS_BND_OUT_CTRL
        boundary_name: 联动控制指令
        medium: DATA-IP
        target: 各子系统

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:
  
    source_nodes:
    
      - node_id: INT-IBMS_SRC_BA
        node_name: BA系统接口
        node_name_en: BA System Interface
        node_type: Source_Node
        node_category: SRC
        
        function: 楼宇自控数据接入
        medium_out: DATA-IP
        
        source_system: INT-BA
        
        equipment_parameters:
          protocol: BACnet/IP, OPC-UA
          data_types:
            - 设备状态
            - 运行参数
            - 报警信息
            - 能耗数据
            
        location_hint:
          space_type: RACK
          room_name: 数据中心

      - node_id: INT-IBMS_SRC_SEC
        node_name: 安防系统接口
        node_name_en: Security System Interface
        node_type: Source_Node
        node_category: SRC
        
        function: 安防系统数据接入
        medium_out: DATA-IP
        
        source_system: INT-SEC
        
        equipment_parameters:
          protocol: SDK/API
          data_types:
            - 视频流
            - 门禁事件
            - 报警信息
            
        location_hint:
          space_type: RACK
          room_name: 数据中心

      - node_id: INT-IBMS_SRC_FA
        node_name: 消防系统接口
        node_name_en: Fire Alarm Interface
        node_type: Source_Node
        node_category: SRC
        
        function: 消防报警数据接入
        medium_out: DATA-IP
        
        source_system: FIRE-ALARM
        
        equipment_parameters:
          protocol: 串口/网络
          data_types:
            - 火警信息
            - 设备状态
            - 联动反馈
            
        location_hint:
          space_type: RACK
          room_name: 数据中心

      - node_id: INT-IBMS_SRC_ELEC
        node_name: 配电监控接口
        node_name_en: Power Monitoring Interface
        node_type: Source_Node
        node_category: SRC
        
        function: 配电系统数据接入
        medium_out: DATA-IP
        
        source_system: ELEC-LV-MAIN
        
        equipment_parameters:
          protocol: Modbus TCP, IEC 61850
          data_types:
            - 电压/电流/功率
            - 电能计量
            - 开关状态
            - 报警信息

      - node_id: INT-IBMS_SRC_MGAS
        node_name: 医气监控接口
        node_name_en: Medical Gas Monitoring Interface
        node_type: Source_Node
        node_category: SRC
        
        function: 医疗气体数据接入
        medium_out: DATA-IP
        
        source_systems: [MGAS-O2, MGAS-VAC, MGAS-AIR]
        
        equipment_parameters:
          protocol: Modbus, 专有协议
          data_types:
            - 气源状态
            - 压力/液位
            - 报警信息

    distribution_nodes:
    
      - node_id: INT-IBMS_DST_GATEWAY
        node_name: 集成网关
        node_name_en: Integration Gateway
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
        
        function: 协议转换与数据采集
        medium_in: DATA-IP
        medium_out: DATA-IP
        
        multiplicity: multiple
        
        equipment_parameters:
          type: 协议转换网关
          protocols_in:
            - BACnet
            - Modbus
            - OPC
            - 私有协议
          protocols_out: 标准API/消息队列
          capacity: 视点位数量
          
        location_hint:
          space_type: RACK
          room_name: 数据中心

      - node_id: INT-IBMS_DST_DATABASE
        node_name: 数据库服务器
        node_name_en: Database Server
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BUF
        
        function: 数据存储
        medium_in: DATA-IP
        medium_out: DATA-IP
        
        equipment_parameters:
          type: 关系型/时序数据库
          components:
            - 实时数据库
            - 历史数据库
            - 报警数据库
            - 配置数据库
          storage: 根据数据量配置
          retention:
            realtime: {value: 7, unit: 天}
            historical: {value: 1-3, unit: 年}
            
        location_hint:
          space_type: RACK
          room_name: 数据中心
          
        control_points:
          sensors:
            - {point_id: DB_CPU, type: AI, description: CPU使用率}
            - {point_id: DB_DISK, type: AI, description: 磁盘使用率}

      - node_id: INT-IBMS_DST_APP_SERVER
        node_name: 应用服务器
        node_name_en: Application Server
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
        
        function: 业务逻辑处理
        medium_in: DATA-IP
        medium_out: DATA-IP
        
        equipment_parameters:
          type: 应用服务器集群
          functions:
            - 数据处理
            - 联动逻辑
            - 报警管理
            - 能耗分析
            - 报表生成
          redundancy: 负载均衡/热备
          
        location_hint:
          space_type: RACK
          room_name: 数据中心

      - node_id: INT-IBMS_DST_3D_ENGINE
        node_name: 3D可视化引擎
        node_name_en: 3D Visualization Engine
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
        
        function: 三维可视化渲染
        medium_in: DATA-IP
        medium_out: SIGNAL-VIDEO
        
        equipment_parameters:
          type: 3D渲染服务器
          features:
            - BIM模型加载
            - 实时数据叠加
            - 漫游浏览
            - 设备定位
            - 告警定位
          gpu: 高性能GPU
          
        location_hint:
          space_type: RACK
          room_name: 数据中心

      - node_id: INT-IBMS_DST_LINKAGE
        node_name: 联动控制引擎
        node_name_en: Linkage Control Engine
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 跨系统联动控制
        medium_in: DATA-IP
        medium_out: DATA-IP
        
        equipment_parameters:
          type: 规则引擎
          functions:
            - 联动规则定义
            - 事件触发
            - 动作执行
            - 结果反馈
          examples:
            - 火警→广播→门禁释放→空调停止
            - 下班→灯光关闭→空调关闭
            - 设备故障→短信通知→工单生成
            
        location_hint:
          space_type: SERVER
          room_name: 数据中心

      - node_id: INT-IBMS_DST_ANALYSIS
        node_name: 数据分析引擎
        node_name_en: Data Analysis Engine
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
        
        function: 数据分析与挖掘
        medium_in: DATA-IP
        medium_out: DATA-IP
        
        equipment_parameters:
          type: 分析平台
          functions:
            - 能耗分析
            - 设备效率分析
            - 故障预测
            - 优化建议
            - 报表生成
            
        location_hint:
          space_type: SERVER
          room_name: 数据中心

    sink_nodes:
    
      - node_id: INT-IBMS_SNK_DISPLAY
        node_name: 大屏显示系统
        node_name_en: Display Wall
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 可视化展示
        medium_in: SIGNAL-VIDEO
        
        equipment_parameters:
          type: LED/LCD拼接屏
          size: 根据机房空间
          resolution: 4K/8K
          content:
            - 系统概况
            - 报警列表
            - 能耗统计
            - 3D漫游
            
        location_hint:
          space_type: ROOM
          room_name: 监控中心

      - node_id: INT-IBMS_SNK_WORKSTATION
        node_name: 操作工作站
        node_name_en: Operator Workstation
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 操作管理
        medium_in: DATA-IP
        
        multiplicity: multiple
        
        equipment_parameters:
          type: 计算机工作站
          displays: 2-4屏
          functions:
            - 实时监控
            - 报警处置
            - 设备控制
            - 报表查询
            
        location_hint:
          space_type: DESK
          room_name: 监控中心

      - node_id: INT-IBMS_SNK_WEB
        node_name: Web/移动端
        node_name_en: Web/Mobile Client
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 远程访问
        medium_in: DATA-IP
        
        multiplicity: multiple
        
        equipment_parameters:
          platforms:
            - Web浏览器
            - iOS App
            - Android App
            - 微信小程序
          functions:
            - 信息查看
            - 报警推送
            - 远程控制（授权）
            - 报表下载

  # ============================================================
  # 边定义
  # ============================================================
  edges:
  
    integration_edges:
    
      - edge_id: INT-IBMS_EDGE_BA
        edge_name: BA系统至网关
        edge_type: TRK
        from_node: INT-IBMS_SRC_BA
        to_node: INT-IBMS_DST_GATEWAY
        direction: bidirectional
        medium: DATA-IP
        
      - edge_id: INT-IBMS_EDGE_SEC
        edge_name: 安防系统至网关
        edge_type: TRK
        from_node: INT-IBMS_SRC_SEC
        to_node: INT-IBMS_DST_GATEWAY
        direction: bidirectional
        medium: DATA-IP
        
      - edge_id: INT-IBMS_EDGE_FA
        edge_name: 消防系统至网关
        edge_type: TRK
        from_node: INT-IBMS_SRC_FA
        to_node: INT-IBMS_DST_GATEWAY
        direction: bidirectional
        medium: DATA-IP
        
      - edge_id: INT-IBMS_EDGE_ELEC
        edge_name: 配电系统至网关
        edge_type: TRK
        from_node: INT-IBMS_SRC_ELEC
        to_node: INT-IBMS_DST_GATEWAY
        direction: bidirectional
        medium: DATA-IP

    processing_edges:
    
      - edge_id: INT-IBMS_EDGE_GW_DB
        edge_name: 网关至数据库
        edge_type: TRK
        from_node: INT-IBMS_DST_GATEWAY
        to_node: INT-IBMS_DST_DATABASE
        direction: unidirectional
        medium: DATA-IP
        
      - edge_id: INT-IBMS_EDGE_DB_APP
        edge_name: 数据库至应用服务器
        edge_type: TRK
        from_node: INT-IBMS_DST_DATABASE
        to_node: INT-IBMS_DST_APP_SERVER
        direction: bidirectional
        medium: DATA-IP
        
      - edge_id: INT-IBMS_EDGE_APP_3D
        edge_name: 应用至3D引擎
        edge_type: TRK
        from_node: INT-IBMS_DST_APP_SERVER
        to_node: INT-IBMS_DST_3D_ENGINE
        direction: bidirectional
        medium: DATA-IP
        
      - edge_id: INT-IBMS_EDGE_APP_LINK
        edge_name: 应用至联动引擎
        edge_type: TRK
        from_node: INT-IBMS_DST_APP_SERVER
        to_node: INT-IBMS_DST_LINKAGE
        direction: bidirectional
        medium: DATA-IP

    output_edges:
    
      - edge_id: INT-IBMS_EDGE_DISPLAY
        edge_name: 3D引擎至大屏
        edge_type: TRM
        from_node: INT-IBMS_DST_3D_ENGINE
        to_node: INT-IBMS_SNK_DISPLAY
        direction: unidirectional
        medium: SIGNAL-VIDEO
        
      - edge_id: INT-IBMS_EDGE_WS
        edge_name: 应用至工作站
        edge_type: TRM
        from_node: INT-IBMS_DST_APP_SERVER
        to_node: INT-IBMS_SNK_WORKSTATION
        direction: bidirectional
        medium: DATA-IP
        
      - edge_id: INT-IBMS_EDGE_WEB
        edge_name: 应用至Web端
        edge_type: TRM
        from_node: INT-IBMS_DST_APP_SERVER
        to_node: INT-IBMS_SNK_WEB
        direction: bidirectional
        medium: DATA-IP

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:
  
    - path_id: INT-IBMS_PATH_MONITOR
      path_name: 数据监控路径
      path_type: MON
      sequence:
        - {step: 1, element_type: node, element_id: INT-IBMS_SRC_BA}
        - {step: 2, element_type: node, element_id: INT-IBMS_DST_GATEWAY}
        - {step: 3, element_type: node, element_id: INT-IBMS_DST_DATABASE}
        - {step: 4, element_type: node, element_id: INT-IBMS_DST_APP_SERVER}
        - {step: 5, element_type: node, element_id: INT-IBMS_DST_3D_ENGINE}
        - {step: 6, element_type: node, element_id: INT-IBMS_SNK_DISPLAY}
        
    - path_id: INT-IBMS_PATH_LINKAGE
      path_name: 联动控制路径
      path_type: CTRL
      sequence:
        - {step: 1, element_type: node, element_id: INT-IBMS_SRC_FA}
        - {step: 2, element_type: node, element_id: INT-IBMS_DST_GATEWAY}
        - {step: 3, element_type: node, element_id: INT-IBMS_DST_LINKAGE}
        - {step: 4, element_type: node, element_id: INT-IBMS_DST_GATEWAY}
        - {step: 5, element_type: node, element_id: target_system}

  # ============================================================
  # 联动规则示例
  # ============================================================
  linkage_rules:
  
    fire_emergency:
      name: 火灾联动
      trigger:
        system: FIRE-ALARM
        event: 火灾确认
      actions:
        - {target: INT-BA, action: 停止空调风机}
        - {target: HVAC-SMOKE, action: 启动排烟}
        - {target: INT-SEC, action: 释放疏散门禁}
        - {target: INT-PA, action: 播放疏散广播}
        - {target: ELEC-LIGHT, action: 开启应急照明}
        
    after_hours:
      name: 非工作时间
      trigger:
        type: schedule
        time: "22:00"
      actions:
        - {target: INT-BA, action: 空调夜间模式}
        - {target: ELEC-LIGHT, action: 关闭非必要照明}
        - {target: INT-SEC, action: 加强安防布防}
        
    equipment_fault:
      name: 设备故障
      trigger:
        system: INT-BA
        event: 关键设备故障
      actions:
        - {target: NOTIFICATION, action: 短信通知运维}
        - {target: CMMS, action: 生成维修工单}
        - {target: BACKUP, action: 切换备用设备}
```

---

## 6.4 PLUMB-STORM 雨水排水系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: PLUMB-STORM
    system_name: 雨水排水系统
    system_name_en: Storm Water Drainage System
    category: PLUMBING
    version: 1.0
    
    description: |
      医院雨水排水系统，收集建筑屋面及场地雨水，
      通过管网排入市政雨水系统或进行雨水收集利用。
      
    design_basis:
      design_storm: 根据当地暴雨强度公式
      return_period: {value: 5-10, unit: 年}
      roof_runoff: {value: 0.9, unit: 径流系数}
      
    serving_scope:
      - 建筑屋面
      - 露台/平台
      - 室外场地

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: PLUMB-STORM_BND_IN_RAIN
        boundary_name: 降雨
        medium: WATER-RAIN
        is_external: true
        source: 大气降水
        
    outputs:
      - boundary_id: PLUMB-STORM_BND_OUT_MUNI
        boundary_name: 市政雨水
        medium: WATER-STORM
        is_external: true
        target: 市政雨水管网
        
      - boundary_id: PLUMB-STORM_BND_OUT_RW
        boundary_name: 雨水收集
        medium: WATER-STORM
        target_system: PLUMB-RW
        note: 如有雨水回用系统

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:
  
    source_nodes:
    
      - node_id: PLUMB-STORM_SRC_ROOF
        node_name: 屋面集水
        node_name_en: Roof Collection
        node_type: Source_Node
        node_category: SRC
        
        function: 屋面雨水收集
        medium_out: WATER-STORM
        
        equipment_parameters:
          type: 屋面
          components:
            - 找坡层
            - 防水层
            - 保温层
            
        location_hint:
          space_type: EXTERIOR
          position: 建筑屋面

      - node_id: PLUMB-STORM_SRC_TERRACE
        node_name: 露台/平台集水
        node_name_en: Terrace Collection
        node_type: Source_Node
        node_category: SRC
        
        function: 露台雨水收集
        medium_out: WATER-STORM
        
        multiplicity: multiple
        
        location_hint:
          space_type: EXTERIOR
          position: 各层露台

    distribution_nodes:
    
      - node_id: PLUMB-STORM_DST_DRAIN
        node_name: 雨水斗
        node_name_en: Roof Drain
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRM
        
        function: 屋面雨水入口
        medium_in: WATER-STORM
        medium_out: WATER-STORM
        
        multiplicity: multiple
        
        equipment_parameters:
          types:
            - {type: 重力式雨水斗, application: 普通屋面}
            - {type: 虹吸式雨水斗, application: 大面积屋面}
          material: 铸铁/不锈钢
          
        location_hint:
          space_type: ROOF
          position: 屋面低点
          
        installation_requirements:
          - 设置在屋面最低点
          - 周边找坡
          - 防堵网罩

      - node_id: PLUMB-STORM_DST_STACK
        node_name: 雨水立管
        node_name_en: Storm Stack
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
        
        function: 雨水垂直排放
        medium_in: WATER-STORM
        medium_out: WATER-STORM
        
        multiplicity: multiple
        instance_pattern: PLUMB-STORM_DST_STACK_{Zone}_{Seq}
        
        equipment_parameters:
          types:
            - {type: 重力式, material: UPVC/铸铁, diameter: DN100-DN150}
            - {type: 虹吸式, material: HDPE, diameter: DN50-DN100}
            
        location_hint:
          space_type: SHAFT
          shaft_type: 雨水管井
          
        installation_requirements:
          - 室内立管保温防凝露
          - 伸缩节
          - 检查口

      - node_id: PLUMB-STORM_DST_HORIZONTAL
        node_name: 雨水横管
        node_name_en: Storm Horizontal Pipe
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
        
        function: 雨水水平汇集
        medium_in: WATER-STORM
        medium_out: WATER-STORM
        
        multiplicity: multiple
        
        equipment_parameters:
          material: UPVC/HDPE
          diameter: {value: DN150-DN300, unit: mm}
          slope: {value: "0.5-1%", unit: null}
          
        location_hint:
          space_type: CEILING_VOID / UNDERGROUND
          position: 悬吊管/埋地管

      - node_id: PLUMB-STORM_DST_MANHOLE
        node_name: 雨水检查井
        node_name_en: Storm Manhole
        node_type: Distribution_Node
        node_category: DST
        node_subtype: JUN
        
        function: 汇集/检修
        medium_in: WATER-STORM
        medium_out: WATER-STORM
        
        multiplicity: multiple
        
        equipment_parameters:
          type: 检查井
          material: 砖砌/预制混凝土
          
        location_hint:
          space_type: OUTDOOR
          position: 室外管道转弯/交汇处

      - node_id: PLUMB-STORM_DST_SIPHON_SYSTEM
        node_name: 虹吸雨水系统
        node_name_en: Siphonic Drainage System
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
        
        function: 虹吸式快速排水
        medium_in: WATER-STORM
        medium_out: WATER-STORM
        
        equipment_parameters:
          type: 虹吸雨水系统
          components:
            - 虹吸式雨水斗
            - HDPE管道
            - 消能装置
          features:
            - 快速排水
            - 管径小
            - 无需坡度
            
        location_hint:
          space_type: ROOF / SHAFT
          
        note: 可选系统，适用于大面积屋面

    sink_nodes:
    
      - node_id: PLUMB-STORM_SNK_MUNI
        node_name: 市政雨水接口
        node_name_en: Municipal Storm Connection
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 雨水排放
        medium_in: WATER-STORM
        is_external: true
        
        location_hint:
          space_type: OUTDOOR
          position: 用地红线附近

      - node_id: PLUMB-STORM_SNK_HARVEST
        node_name: 雨水收集池
        node_name_en: Rainwater Harvesting Tank
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 雨水回用
        medium_in: WATER-STORM
        
        interface_system: PLUMB-RW
        
        equipment_parameters:
          type: 雨水收集池/调蓄池
          capacity: 根据屋面面积计算
          
        location_hint:
          space_type: UNDERGROUND
          position: 室外绿地下
          
        note: 可选，配合雨水回用系统

  # ============================================================
  # 边定义
  # ============================================================
  edges:
  
    collection_edges:
    
      - edge_id: PLUMB-STORM_EDGE_001
        edge_name: 屋面至雨水斗
        edge_type: TRM
        from_node: PLUMB-STORM_SRC_ROOF
        to_node: PLUMB-STORM_DST_DRAIN
        direction: unidirectional
        medium: WATER-STORM
        
      - edge_id: PLUMB-STORM_EDGE_002
        edge_name: 雨水斗至立管
        edge_type: TRK
        from_node: PLUMB-STORM_DST_DRAIN
        to_node: PLUMB-STORM_DST_STACK
        direction: unidirectional
        medium: WATER-STORM
        
      - edge_id: PLUMB-STORM_EDGE_003
        edge_name: 立管至横管
        edge_type: TRK
        from_node: PLUMB-STORM_DST_STACK
        to_node: PLUMB-STORM_DST_HORIZONTAL
        direction: unidirectional
        medium: WATER-STORM
        
      - edge_id: PLUMB-STORM_EDGE_004
        edge_name: 横管至检查井
        edge_type: TRK
        from_node: PLUMB-STORM_DST_HORIZONTAL
        to_node: PLUMB-STORM_DST_MANHOLE
        direction: unidirectional
        medium: WATER-STORM
        
      - edge_id: PLUMB-STORM_EDGE_005
        edge_name: 检查井至市政
        edge_type: TRK
        from_node: PLUMB-STORM_DST_MANHOLE
        to_node: PLUMB-STORM_SNK_MUNI
        direction: unidirectional
        medium: WATER-STORM

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:
  
    - path_id: PLUMB-STORM_PATH_MAIN
      path_name: 雨水排放路径
      path_type: DRN
      sequence:
        - {step: 1, element_type: node, element_id: PLUMB-STORM_SRC_ROOF}
        - {step: 2, element_type: node, element_id: PLUMB-STORM_DST_DRAIN}
        - {step: 3, element_type: node, element_id: PLUMB-STORM_DST_STACK}
        - {step: 4, element_type: node, element_id: PLUMB-STORM_DST_HORIZONTAL}
        - {step: 5, element_type: node, element_id: PLUMB-STORM_DST_MANHOLE}
        - {step: 6, element_type: node, element_id: PLUMB-STORM_SNK_MUNI}
```

---

## 6.5 PLUMB-RW 中水回用系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: PLUMB-RW
    system_name: 中水回用系统
    system_name_en: Reclaimed Water System
    category: PLUMBING
    version: 1.0
    
    description: |
      医院中水回用系统，收集处理雨水和/或优质杂排水，
      处理后用于冲厕、绿化灌溉、道路冲洗等非饮用用途。
      
    design_basis:
      water_source:
        - 雨水
        - 冷却塔排污水
        - 空调冷凝水
      treatment: MBR/生化处理
      quality: GB/T 18920 城市杂用水水质标准
      
    serving_scope:
      - 卫生间冲厕
      - 绿化灌溉
      - 道路冲洗
      - 洗车

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: PLUMB-RW_BND_IN_STORM
        boundary_name: 雨水
        medium: WATER-STORM
        source_system: PLUMB-STORM
        
      - boundary_id: PLUMB-RW_BND_IN_COND
        boundary_name: 冷凝水
        medium: WATER-COND
        source_system: HVAC-AHU
        
      - boundary_id: PLUMB-RW_BND_IN_ELEC
        boundary_name: 电源
        medium: ELEC-LV
        source_system: ELEC-LV-MAIN
        
    outputs:
      - boundary_id: PLUMB-RW_BND_OUT_REUSE
        boundary_name: 中水供水
        medium: WATER-RW
        target: 杂用水点

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:
  
    source_nodes:
    
      - node_id: PLUMB-RW_SRC_STORM
        node_name: 雨水来源
        node_name_en: Storm Water Source
        node_type: Source_Node
        node_category: SRC
        
        function: 雨水收集
        medium_out: WATER-STORM
        
        source_system: PLUMB-STORM
        
        location_hint:
          space_type: OUTDOOR
          position: 雨水收集池

      - node_id: PLUMB-RW_SRC_COND
        node_name: 冷凝水来源
        node_name_en: Condensate Water Source
        node_type: Source_Node
        node_category: SRC
        
        function: 空调冷凝水收集
        medium_out: WATER-COND
        
        source_systems: [HVAC-AHU, HVAC-FCU]
        
        location_hint:
          space_type: MEP_ROOM
          position: 冷凝水收集装置

    distribution_nodes:
    
      - node_id: PLUMB-RW_DST_COLLECTION
        node_name: 原水收集池
        node_name_en: Raw Water Collection Tank
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BUF
        
        function: 原水储存
        medium_in: [WATER-STORM, WATER-COND]
        medium_out: WATER-RAW
        
        equipment_parameters:
          type: 地下收集池
          capacity: 根据日处理量
          components:
            - 格栅
            - 沉砂池
            - 初沉池
            
        location_hint:
          space_type: UNDERGROUND
          position: 中水处理站
          
        control_points:
          sensors:
            - {point_id: COLL_LEVEL, type: AI, description: 液位}

      - node_id: PLUMB-RW_DST_TREATMENT
        node_name: 中水处理设备
        node_name_en: Reclaimed Water Treatment Plant
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
        
        function: 污水处理
        medium_in: WATER-RAW
        medium_out: WATER-RW
        
        equipment_parameters:
          type: 一体化中水处理设备
          process:
            - 生化处理
            - MBR膜过滤
            - 消毒
          capacity: {value: 50-200, unit: m³/d}
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 中水处理站
          
        control_points:
          sensors:
            - {point_id: TREAT_PH, type: AI, description: pH值}
            - {point_id: TREAT_TURB, type: AI, description: 浊度}
            - {point_id: TREAT_CL, type: AI, description: 余氯}
          status:
            - {point_id: TREAT_RUN, type: DI, description: 运行状态}
            - {point_id: TREAT_FAULT, type: DI, description: 故障报警}

      - node_id: PLUMB-RW_DST_STORAGE
        node_name: 中水储水池
        node_name_en: Reclaimed Water Storage Tank
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BUF
        
        function: 处理后水储存
        medium_in: WATER-RW
        medium_out: WATER-RW
        
        equipment_parameters:
          type: 清水池
          capacity: 日用水量的30-50%
          material: 钢筋混凝土/不锈钢
          
        location_hint:
          space_type: UNDERGROUND
          position: 中水处理站
          
        control_points:
          sensors:
            - {point_id: STOR_LEVEL, type: AI, description: 液位}
            - {point_id: STOR_CL, type: AI, description: 余氯}

      - node_id: PLUMB-RW_DST_PUMP
        node_name: 中水供水泵
        node_name_en: Reclaimed Water Supply Pump
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 中水加压供水
        medium_in: WATER-RW
        medium_out: WATER-RW
        
        equipment_parameters:
          type: 恒压变频泵组
          configuration: 一用一备
          control: 恒压供水
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 中水泵房
          
        control_points:
          sensors:
            - {point_id: PUMP_P, type: AI, description: 出水压力}
            - {point_id: PUMP_Q, type: AI, description: 瞬时流量}
          status:
            - {point_id: PUMP_RUN, type: DI, description: 运行状态}

      - node_id: PLUMB-RW_DST_MAIN
        node_name: 中水主管
        node_name_en: Reclaimed Water Main
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
        
        function: 中水输配
        medium_in: WATER-RW
        medium_out: WATER-RW
        
        equipment_parameters:
          material: PE管/镀锌钢管
          color_code: 淡绿色标识
          
        location_hint:
          space_type: UNDERGROUND / CEILING_VOID
          
        installation_requirements:
          - 明显标识"中水 勿饮"
          - 与给水管分开敷设
          - 防止误接

    sink_nodes:
    
      - node_id: PLUMB-RW_SNK_TOILET
        node_name: 冲厕用水
        node_name_en: Toilet Flushing
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 卫生间冲厕
        medium_in: WATER-RW
        
        multiplicity: multiple
        
        location_hint:
          space_type: WET_ROOM
          position: 卫生间

      - node_id: PLUMB-RW_SNK_IRRIGATION
        node_name: 绿化灌溉
        node_name_en: Landscape Irrigation
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 绿化浇灌
        medium_in: WATER-RW
        
        location_hint:
          space_type: OUTDOOR
          position: 绿化带

      - node_id: PLUMB-RW_SNK_WASHING
        node_name: 道路冲洗
        node_name_en: Road Washing
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 道路/场地冲洗
        medium_in: WATER-RW
        
        location_hint:
          space_type: OUTDOOR
          position: 道路/停车场

  # ============================================================
  # 边定义
  # ============================================================
  edges:
  
    collection_edges:
    
      - edge_id: PLUMB-RW_EDGE_001
        edge_name: 雨水至收集池
        edge_type: TRK
        from_node: PLUMB-RW_SRC_STORM
        to_node: PLUMB-RW_DST_COLLECTION
        direction: unidirectional
        medium: WATER-STORM
        
      - edge_id: PLUMB-RW_EDGE_002
        edge_name: 冷凝水至收集池
        edge_type: TRK
        from_node: PLUMB-RW_SRC_COND
        to_node: PLUMB-RW_DST_COLLECTION
        direction: unidirectional
        medium: WATER-COND

    treatment_edges:
    
      - edge_id: PLUMB-RW_EDGE_003
        edge_name: 收集池至处理设备
        edge_type: TRK
        from_node: PLUMB-RW_DST_COLLECTION
        to_node: PLUMB-RW_DST_TREATMENT
        direction: unidirectional
        medium: WATER-RAW
        
      - edge_id: PLUMB-RW_EDGE_004
        edge_name: 处理设备至储水池
        edge_type: TRK
        from_node: PLUMB-RW_DST_TREATMENT
        to_node: PLUMB-RW_DST_STORAGE
        direction: unidirectional
        medium: WATER-RW

    supply_edges:
    
      - edge_id: PLUMB-RW_EDGE_005
        edge_name: 储水池至水泵
        edge_type: TRK
        from_node: PLUMB-RW_DST_STORAGE
        to_node: PLUMB-RW_DST_PUMP
        direction: unidirectional
        medium: WATER-RW
        
      - edge_id: PLUMB-RW_EDGE_006
        edge_name: 水泵至主管
        edge_type: TRK
        from_node: PLUMB-RW_DST_PUMP
        to_node: PLUMB-RW_DST_MAIN
        direction: unidirectional
        medium: WATER-RW
        
      - edge_id: PLUMB-RW_EDGE_007
        edge_name: 主管至冲厕
        edge_type: TRM
        from_node: PLUMB-RW_DST_MAIN
        to_node: PLUMB-RW_SNK_TOILET
        direction: unidirectional
        medium: WATER-RW

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:
  
    - path_id: PLUMB-RW_PATH_MAIN
      path_name: 中水处理供应路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: PLUMB-RW_SRC_STORM}
        - {step: 2, element_type: node, element_id: PLUMB-RW_DST_COLLECTION}
        - {step: 3, element_type: node, element_id: PLUMB-RW_DST_TREATMENT}
        - {step: 4, element_type: node, element_id: PLUMB-RW_DST_STORAGE}
        - {step: 5, element_type: node, element_id: PLUMB-RW_DST_PUMP}
        - {step: 6, element_type: node, element_id: PLUMB-RW_DST_MAIN}
        - {step: 7, element_type: node, element_id: PLUMB-RW_SNK_TOILET}

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:
  
    level_control:
      collection_tank:
        high: 停止进水
        low: 报警
        
      storage_tank:
        high: 停止处理
        low: 启用自来水补水
        
    water_quality:
      monitoring:
        - pH: 6.5-9.0
        - 浊度: ≤5NTU
        - 余氯: 0.2-1.0mg/L
      alarm:
        condition: 水质超标
        action: 停止供水，排放回处理
```

---

## 6.6 INT-IPTV 病房电视系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: INT-IPTV
    system_name: 病房电视系统
    system_name_en: Inpatient IPTV System
    category: INTELLIGENT
    version: 1.0
    
    description: |
      医院病房IPTV系统，为住院患者提供电视节目、
      点播娱乐、健康教育、医疗服务等综合信息服务。
      
    design_basis:
      content: 电视直播+点播+交互
      integration: 与HIS集成
      control: 护士站集中控制
      
    serving_scope:
      - 普通病房
      - VIP病房
      - 候诊区
      - 门诊大厅

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: INT-IPTV_BND_IN_CATV
        boundary_name: 有线电视信号
        medium: SIGNAL-CATV
        is_external: true
        source: 有线电视网络
        
      - boundary_id: INT-IPTV_BND_IN_NET
        boundary_name: 网络接入
        medium: DATA-IP
        source_system: INT-NET
        
      - boundary_id: INT-IPTV_BND_IN_HIS
        boundary_name: HIS接口
        medium: DATA-IP
        source: 医院信息系统
        
    outputs:
      - boundary_id: INT-IPTV_BND_OUT_TV
        boundary_name: 电视终端
        medium: DATA-IP
        target: 病房电视

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:
  
    source_nodes:
    
      - node_id: INT-IPTV_SRC_CATV
        node_name: 有线电视前端
        node_name_en: CATV Head-End
        node_type: Source_Node
        node_category: SRC
        
        function: 电视信号接入
        medium_out: SIGNAL-CATV
        is_external: true
        
        equipment_parameters:
          type: 有线电视接入
          channels: 50-100频道
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 弱电机房

      - node_id: INT-IPTV_SRC_CONTENT
        node_name: 点播内容服务器
        node_name_en: VOD Content Server
        node_type: Source_Node
        node_category: SRC
        
        function: 点播内容存储
        medium_out: DATA-IP
        
        equipment_parameters:
          type: 流媒体服务器
          storage: {value: 10-50, unit: TB}
          content:
            - 电影
            - 电视剧
            - 健康教育视频
            - 科室介绍
            
        location_hint:
          space_type: RACK
          room_name: 数据中心

    distribution_nodes:
    
      - node_id: INT-IPTV_DST_ENCODER
        node_name: 编码器
        node_name_en: Encoder
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
        
        function: CATV信号转IP
        medium_in: SIGNAL-CATV
        medium_out: DATA-IP
        
        equipment_parameters:
          type: 数字编码器
          channels: 50-100路
          format: H.264/H.265
          output: IPTV流
          
        location_hint:
          space_type: RACK
          room_name: IPTV机房

      - node_id: INT-IPTV_DST_SERVER
        node_name: IPTV服务器
        node_name_en: IPTV Server
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
        
        function: IPTV平台服务
        medium_in: DATA-IP
        medium_out: DATA-IP
        
        equipment_parameters:
          type: IPTV管理平台
          functions:
            - 用户管理
            - 节目管理
            - EPG电子节目单
            - 计费管理
            - 统计分析
          capacity: {value: 500-2000, unit: 终端}
          
        location_hint:
          space_type: RACK
          room_name: 数据中心

      - node_id: INT-IPTV_DST_INTERFACE
        node_name: HIS接口模块
        node_name_en: HIS Interface Module
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
        
        function: 与医院信息系统集成
        medium_in: DATA-IP
        medium_out: DATA-IP
        
        equipment_parameters:
          type: 接口服务
          integration:
            - 患者信息同步
            - 费用信息
            - 医嘱提醒
            - 满意度调查
            
        location_hint:
          space_type: RACK
          room_name: 数据中心

      - node_id: INT-IPTV_DST_NURSE_CTRL
        node_name: 护士站控制终端
        node_name_en: Nurse Station Control Terminal
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 集中控制管理
        medium_in: DATA-IP
        medium_out: DATA-IP
        
        multiplicity: multiple
        
        equipment_parameters:
          type: 护士站管理终端
          functions:
            - 批量开关机
            - 音量控制
            - 频道锁定
            - 紧急广播
            - 统一控制
            
        location_hint:
          space_type: DESK
          position: 护士站

    sink_nodes:
    
      - node_id: INT-IPTV_SNK_TV
        node_name: 病房电视终端
        node_name_en: Bedside TV Terminal
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 视频播放/交互
        medium_in: DATA-IP
        
        multiplicity: multiple
        instance_pattern: INT-IPTV_SNK_TV_{Floor}_{Room}_{Bed}
        
        equipment_parameters:
          type: 智能电视/机顶盒+电视
          size: {value: 22-32, unit: 英寸}
          features:
            - 电视直播
            - 点播
            - 健康教育
            - 医嘱查询
            - 呼叫护士
            - 满意度评价
            - 费用查询
          control: 遥控器/床头柜按键
          
        location_hint:
          space_type: ROOM
          position: 病床对面墙/悬臂支架
          
        typical_quantity:
          per_bed: 1

      - node_id: INT-IPTV_SNK_LOBBY
        node_name: 大厅信息屏
        node_name_en: Lobby Information Display
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 公共信息展示
        medium_in: DATA-IP
        
        multiplicity: multiple
        
        equipment_parameters:
          type: 大屏显示器
          size: {value: 55-75, unit: 英寸}
          content:
            - 电视直播
            - 医院宣传
            - 健康知识
            - 排队信息
            
        location_hint:
          space_type: ROOM
          position: 候诊区/大厅

  # ============================================================
  # 边定义
  # ============================================================
  edges:
  
    content_edges:
    
      - edge_id: INT-IPTV_EDGE_001
        edge_name: CATV至编码器
        edge_type: TRK
        from_node: INT-IPTV_SRC_CATV
        to_node: INT-IPTV_DST_ENCODER
        direction: unidirectional
        medium: SIGNAL-CATV
        
      - edge_id: INT-IPTV_EDGE_002
        edge_name: 编码器至服务器
        edge_type: TRK
        from_node: INT-IPTV_DST_ENCODER
        to_node: INT-IPTV_DST_SERVER
        direction: unidirectional
        medium: DATA-IP
        
      - edge_id: INT-IPTV_EDGE_003
        edge_name: 点播服务器至IPTV服务器
        edge_type: TRK
        from_node: INT-IPTV_SRC_CONTENT
        to_node: INT-IPTV_DST_SERVER
        direction: unidirectional
        medium: DATA-IP

    distribution_edges:
    
      - edge_id: INT-IPTV_EDGE_004
        edge_name: 服务器至网络
        edge_type: TRK
        from_node: INT-IPTV_DST_SERVER
        to_node: INT-NET_DST_CORE_SW
        direction: bidirectional
        medium: DATA-IP
        cross_system: true
        target_system: INT-NET
        
      - edge_id: INT-IPTV_EDGE_005
        edge_name: 网络至电视终端
        edge_type: TRM
        from_node: INT-NET_DST_ACCESS_SW
        to_node: INT-IPTV_SNK_TV
        direction: bidirectional
        medium: DATA-IP

    control_edges:
    
      - edge_id: INT-IPTV_EDGE_006
        edge_name: 护士站控制
        edge_type: CTRL
        from_node: INT-IPTV_DST_NURSE_CTRL
        to_node: INT-IPTV_SNK_TV
        direction: bidirectional
        medium: DATA-IP

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:
  
    - path_id: INT-IPTV_PATH_LIVE
      path_name: 电视直播路径
      path_type: STREAM
      sequence:
        - {step: 1, element_type: node, element_id: INT-IPTV_SRC_CATV}
        - {step: 2, element_type: node, element_id: INT-IPTV_DST_ENCODER}
        - {step: 3, element_type: node, element_id: INT-IPTV_DST_SERVER}
        - {step: 4, element_type: node, element_id: INT-IPTV_SNK_TV}

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:
  
    nurse_control:
      batch_operations:
        - 批量开关机
        - 批量调节音量
        - 批量锁定频道
        - 紧急消息推送
        
    patient_interaction:
      functions:
        - 电视/点播观看
        - 健康教育视频
        - 费用查询
        - 满意度评价
        - 呼叫护士
        - 订餐服务
        
    night_mode:
      trigger: 22:00
      action:
        - 自动降低音量
        - 限制部分频道
        - 提示熄灯休息
```

---

## 6.7 MGAS-N2 氮气系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: MGAS-N2
    system_name: 氮气系统
    system_name_en: Nitrogen Gas System
    category: MEDICAL_GAS
    version: 1.0
    
    description: |
      医院医用氮气系统，主要用于手术器械驱动（骨科动力设备）、
      冷冻治疗、实验室等场所。
      
    design_basis:
      purity: {value: "≥99.5", unit: "%"}
      supply_pressure: {value: 0.4-0.5, unit: MPa}
      source: 瓶装氮气/液氮
      
    serving_scope:
      - 骨科手术室（动力设备）
      - 眼科手术室
      - 皮肤科（冷冻治疗）
      - 实验室

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: MGAS-N2_BND_IN_SUPPLY
        boundary_name: 氮气气源
        medium: GAS-N2
        is_external: true
        source: 氮气钢瓶/液氮储罐
        
    outputs:
      - boundary_id: MGAS-N2_BND_OUT_TERM
        boundary_name: 氮气终端
        medium: GAS-N2
        target: 使用点

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:
  
    source_nodes:
    
      - node_id: MGAS-N2_SRC_CYLINDER
        node_name: 氮气钢瓶组
        node_name_en: Nitrogen Cylinder Manifold
        node_type: Source_Node
        node_category: SRC
        
        function: 氮气气源
        medium_out: GAS-N2
        
        equipment_parameters:
          type: 汇流排系统
          configuration: 双排（主+备）
          cylinders_per_bank: {value: 6-10, unit: 瓶}
          cylinder_volume: {value: 40, unit: L}
          cylinder_pressure: {value: 15, unit: MPa}
          switchover: 自动切换
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 医气汇流排间
          
        control_points:
          sensors:
            - {point_id: N2_BANK_P, type: AI, description: 气瓶组压力}
          status:
            - {point_id: N2_BANK_SEL, type: DI, description: 主备切换}
            - {point_id: N2_LOW_P, type: DI, description: 低压报警}

    distribution_nodes:
    
      - node_id: MGAS-N2_DST_REGULATOR
        node_name: 减压稳压器
        node_name_en: Pressure Regulator
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 一级减压
        medium_in: GAS-N2
        medium_out: GAS-N2
        
        equipment_parameters:
          type: 一级减压器
          inlet_pressure: {value: 15, unit: MPa}
          outlet_pressure: {value: 0.8-1.0, unit: MPa}
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 医气汇流排间

      - node_id: MGAS-N2_DST_MAIN_PIPE
        node_name: 氮气主管
        node_name_en: Nitrogen Main Pipe
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
        
        function: 氮气主干输送
        medium_in: GAS-N2
        medium_out: GAS-N2
        
        equipment_parameters:
          material: 无缝不锈钢管/脱脂紫铜管
          diameter: {value: DN20-DN25, unit: mm}
          pressure_rating: {value: 1.6, unit: MPa}
          
        location_hint:
          space_type: CEILING_VOID / SHAFT
          position: 管道井/吊顶内

      - node_id: MGAS-N2_DST_ZONE_VALVE
        node_name: 区域阀
        node_name_en: Zone Valve Box
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 区域控制
        medium_in: GAS-N2
        medium_out: GAS-N2
        
        multiplicity: multiple
        
        equipment_parameters:
          components:
            - 截止阀
            - 二级减压器
            - 压力表
            - 泄压阀
          outlet_pressure: {value: 0.4-0.5, unit: MPa}
          
        location_hint:
          space_type: WALL_BOX
          position: 手术部走廊
          
        control_points:
          sensors:
            - {point_id: N2_ZONE_P, type: AI, description: 区域压力}

      - node_id: MGAS-N2_DST_BRANCH
        node_name: 氮气支管
        node_name_en: Nitrogen Branch Pipe
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BRH
        
        function: 分配至终端
        medium_in: GAS-N2
        medium_out: GAS-N2
        
        multiplicity: multiple
        
        equipment_parameters:
          material: 无缝不锈钢管/脱脂紫铜管
          diameter: {value: DN15, unit: mm}
          
        location_hint:
          space_type: CEILING_VOID
          position: 手术室吊顶

    sink_nodes:
    
      - node_id: MGAS-N2_SNK_TERMINAL
        node_name: 氮气终端
        node_name_en: Nitrogen Terminal
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 氮气使用
        medium_in: GAS-N2
        
        multiplicity: multiple
        instance_pattern: MGAS-N2_SNK_TERMINAL_OR{NN}
        
        equipment_parameters:
          type: 快速接头
          color_code: 黑色
          pressure: {value: 0.4-0.5, unit: MPa}
          flow: 根据设备需求
          
        location_hint:
          space_type: WALL / PENDANT
          position: 手术室墙面/吊塔
          
        typical_locations:
          - 骨科手术室
          - 眼科手术室

      - node_id: MGAS-N2_SNK_CRYO
        node_name: 冷冻治疗设备
        node_name_en: Cryotherapy Equipment
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 冷冻治疗
        medium_in: GAS-N2
        
        location_hint:
          space_type: ROOM
          position: 皮肤科/眼科

  # ============================================================
  # 边定义
  # ============================================================
  edges:
  
    supply_edges:
    
      - edge_id: MGAS-N2_EDGE_001
        edge_name: 钢瓶至减压器
        edge_type: TRK
        from_node: MGAS-N2_SRC_CYLINDER
        to_node: MGAS-N2_DST_REGULATOR
        direction: unidirectional
        medium: GAS-N2
        
      - edge_id: MGAS-N2_EDGE_002
        edge_name: 减压器至主管
        edge_type: TRK
        from_node: MGAS-N2_DST_REGULATOR
        to_node: MGAS-N2_DST_MAIN_PIPE
        direction: unidirectional
        medium: GAS-N2
        
      - edge_id: MGAS-N2_EDGE_003
        edge_name: 主管至区域阀
        edge_type: BRH
        from_node: MGAS-N2_DST_MAIN_PIPE
        to_node: MGAS-N2_DST_ZONE_VALVE
        direction: unidirectional
        medium: GAS-N2
        
      - edge_id: MGAS-N2_EDGE_004
        edge_name: 区域阀至支管
        edge_type: BRH
        from_node: MGAS-N2_DST_ZONE_VALVE
        to_node: MGAS-N2_DST_BRANCH
        direction: unidirectional
        medium: GAS-N2
        
      - edge_id: MGAS-N2_EDGE_005
        edge_name: 支管至终端
        edge_type: TRM
        from_node: MGAS-N2_DST_BRANCH
        to_node: MGAS-N2_SNK_TERMINAL
        direction: unidirectional
        medium: GAS-N2

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:
  
    - path_id: MGAS-N2_PATH_MAIN
      path_name: 氮气供应路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: MGAS-N2_SRC_CYLINDER}
        - {step: 2, element_type: node, element_id: MGAS-N2_DST_REGULATOR}
        - {step: 3, element_type: node, element_id: MGAS-N2_DST_MAIN_PIPE}
        - {step: 4, element_type: node, element_id: MGAS-N2_DST_ZONE_VALVE}
        - {step: 5, element_type: node, element_id: MGAS-N2_DST_BRANCH}
        - {step: 6, element_type: node, element_id: MGAS-N2_SNK_TERMINAL}

  # ============================================================
  # 报警逻辑
  # ============================================================
  alarm_logic:
  
    low_pressure:
      bank:
        warning: {value: 3, unit: MPa}
        alarm: {value: 2, unit: MPa}
      supply:
        warning: {value: 0.35, unit: MPa}
        alarm: {value: 0.3, unit: MPa}
        
    bank_switchover:
      trigger: 主气瓶组压力 < 2MPa
      action: 自动切换至备用组
      notification: 通知更换钢瓶
```

---

## 6.8 MGAS-CO2 二氧化碳系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: MGAS-CO2
    system_name: 二氧化碳系统
    system_name_en: Carbon Dioxide Gas System
    category: MEDICAL_GAS
    version: 1.0
    
    description: |
      医院医用二氧化碳系统，主要用于腹腔镜手术（气腹）、
      冷冻治疗等。
      
    design_basis:
      purity: {value: "≥99.5", unit: "%", note: 医用级}
      supply_pressure: {value: 0.4-0.5, unit: MPa}
      source: 瓶装CO2/液态CO2
      
    serving_scope:
      - 腹腔镜手术室
      - 胸腔镜手术室
      - 宫腔镜室
      - 内镜中心

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: MGAS-CO2_BND_IN_SUPPLY
        boundary_name: CO2气源
        medium: GAS-CO2
        is_external: true
        source: CO2钢瓶/液态CO2储罐
        
    outputs:
      - boundary_id: MGAS-CO2_BND_OUT_TERM
        boundary_name: CO2终端
        medium: GAS-CO2
        target: 使用点

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:
  
    source_nodes:
    
      - node_id: MGAS-CO2_SRC_CYLINDER
        node_name: CO2钢瓶组
        node_name_en: CO2 Cylinder Manifold
        node_type: Source_Node
        node_category: SRC
        
        function: CO2气源
        medium_out: GAS-CO2
        
        equipment_parameters:
          type: 汇流排系统
          configuration: 双排（主+备）
          cylinders_per_bank: {value: 4-8, unit: 瓶}
          cylinder_volume: {value: 40, unit: L}
          cylinder_pressure: {value: 6-7, unit: MPa, note: 液态}
          switchover: 自动切换
          heater: 加热汽化器（液态CO2需要）
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 医气汇流排间
          
        control_points:
          sensors:
            - {point_id: CO2_BANK_P, type: AI, description: 气瓶组压力}
            - {point_id: CO2_BANK_W, type: AI, description: 气瓶重量}
          status:
            - {point_id: CO2_BANK_SEL, type: DI, description: 主备切换}
            - {point_id: CO2_LOW_P, type: DI, description: 低压报警}

    distribution_nodes:
    
      - node_id: MGAS-CO2_DST_REGULATOR
        node_name: 减压稳压器
        node_name_en: Pressure Regulator
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 一级减压
        medium_in: GAS-CO2
        medium_out: GAS-CO2
        
        equipment_parameters:
          type: 一级减压器
          inlet_pressure: {value: 6-7, unit: MPa}
          outlet_pressure: {value: 0.8-1.0, unit: MPa}
          heater: 防冻电加热（液态CO2）
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 医气汇流排间

      - node_id: MGAS-CO2_DST_MAIN_PIPE
        node_name: CO2主管
        node_name_en: CO2 Main Pipe
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
        
        function: CO2主干输送
        medium_in: GAS-CO2
        medium_out: GAS-CO2
        
        equipment_parameters:
          material: 无缝不锈钢管/脱脂紫铜管
          diameter: {value: DN15-DN20, unit: mm}
          pressure_rating: {value: 1.6, unit: MPa}
          
        location_hint:
          space_type: CEILING_VOID / SHAFT
          position: 管道井/吊顶内

      - node_id: MGAS-CO2_DST_ZONE_VALVE
        node_name: 区域阀
        node_name_en: Zone Valve Box
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 区域控制与二次减压
        medium_in: GAS-CO2
        medium_out: GAS-CO2
        
        multiplicity: multiple
        
        equipment_parameters:
          components:
            - 截止阀
            - 二级减压器
            - 压力表
            - 泄压阀
          outlet_pressure: {value: 0.4-0.5, unit: MPa}
          
        location_hint:
          space_type: WALL_BOX
          position: 内镜中心/手术部走廊
          
        control_points:
          sensors:
            - {point_id: CO2_ZONE_P, type: AI, description: 区域压力}

      - node_id: MGAS-CO2_DST_BRANCH
        node_name: CO2支管
        node_name_en: CO2 Branch Pipe
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BRH
        
        function: 分配至终端
        medium_in: GAS-CO2
        medium_out: GAS-CO2
        
        multiplicity: multiple
        
        equipment_parameters:
          material: 无缝不锈钢管/脱脂紫铜管
          diameter: {value: DN10-DN15, unit: mm}
          
        location_hint:
          space_type: CEILING_VOID
          position: 手术室/内镜室吊顶

    sink_nodes:
    
      - node_id: MGAS-CO2_SNK_TERMINAL
        node_name: CO2终端
        node_name_en: CO2 Terminal
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: CO2使用
        medium_in: GAS-CO2
        
        multiplicity: multiple
        instance_pattern: MGAS-CO2_SNK_TERMINAL_{Room}_{Seq}
        
        equipment_parameters:
          type: 快速接头
          color_code: 灰色
          pressure: {value: 0.4-0.5, unit: MPa}
          
        location_hint:
          space_type: WALL / PENDANT
          position: 手术室墙面/吊塔/内镜检查室
          
        typical_locations:
          - 腹腔镜手术室
          - 内镜中心
          - 宫腔镜室

      - node_id: MGAS-CO2_SNK_INSUFFLATOR
        node_name: 气腹机
        node_name_en: Insufflator
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 腹腔镜气腹
        medium_in: GAS-CO2
        
        equipment_parameters:
          type: 电子气腹机
          flow: {value: 0-40, unit: L/min}
          pressure: {value: 0-25, unit: mmHg}
          
        location_hint:
          space_type: EQUIPMENT
          position: 腹腔镜手术设备塔

  # ============================================================
  # 边定义
  # ============================================================
  edges:
  
    supply_edges:
    
      - edge_id: MGAS-CO2_EDGE_001
        edge_name: 钢瓶至减压器
        edge_type: TRK
        from_node: MGAS-CO2_SRC_CYLINDER
        to_node: MGAS-CO2_DST_REGULATOR
        direction: unidirectional
        medium: GAS-CO2
        
      - edge_id: MGAS-CO2_EDGE_002
        edge_name: 减压器至主管
        edge_type: TRK
        from_node: MGAS-CO2_DST_REGULATOR
        to_node: MGAS-CO2_DST_MAIN_PIPE
        direction: unidirectional
        medium: GAS-CO2
        
      - edge_id: MGAS-CO2_EDGE_003
        edge_name: 主管至区域阀
        edge_type: BRH
        from_node: MGAS-CO2_DST_MAIN_PIPE
        to_node: MGAS-CO2_DST_ZONE_VALVE
        direction: unidirectional
        medium: GAS-CO2
        
      - edge_id: MGAS-CO2_EDGE_004
        edge_name: 区域阀至支管
        edge_type: BRH
        from_node: MGAS-CO2_DST_ZONE_VALVE
        to_node: MGAS-CO2_DST_BRANCH
        direction: unidirectional
        medium: GAS-CO2
        
      - edge_id: MGAS-CO2_EDGE_005
        edge_name: 支管至终端
        edge_type: TRM
        from_node: MGAS-CO2_DST_BRANCH
        to_node: MGAS-CO2_SNK_TERMINAL
        direction: unidirectional
        medium: GAS-CO2
        
      - edge_id: MGAS-CO2_EDGE_006
        edge_name: 终端至气腹机
        edge_type: TRM
        from_node: MGAS-CO2_SNK_TERMINAL
        to_node: MGAS-CO2_SNK_INSUFFLATOR
        direction: unidirectional
        medium: GAS-CO2

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:
  
    - path_id: MGAS-CO2_PATH_MAIN
      path_name: CO2供应路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: MGAS-CO2_SRC_CYLINDER}
        - {step: 2, element_type: node, element_id: MGAS-CO2_DST_REGULATOR}
        - {step: 3, element_type: node, element_id: MGAS-CO2_DST_MAIN_PIPE}
        - {step: 4, element_type: node, element_id: MGAS-CO2_DST_ZONE_VALVE}
        - {step: 5, element_type: node, element_id: MGAS-CO2_DST_BRANCH}
        - {step: 6, element_type: node, element_id: MGAS-CO2_SNK_TERMINAL}
        - {step: 7, element_type: node, element_id: MGAS-CO2_SNK_INSUFFLATOR}

  # ============================================================
  # 报警逻辑
  # ============================================================
  alarm_logic:
  
    low_pressure:
      bank:
        warning: {value: 2, unit: MPa}
        alarm: {value: 1.5, unit: MPa}
      supply:
        warning: {value: 0.35, unit: MPa}
        alarm: {value: 0.3, unit: MPa}
        
    bank_switchover:
      trigger: 主气瓶组压力/重量低于阈值
      action: 自动切换至备用组
      notification: 通知更换钢瓶
      
    co2_leak_safety:
      note: |
        CO2泄漏可导致窒息，需要：
        1. 气瓶间通风良好
        2. 设置CO2浓度探测器
        3. 高浓度报警联动通风
```

---

## Batch 6 输出总结

```yaml
Batch_6_Summary:

  completed_systems:
  
    # P2 剩余系统
    - system_id: HVAC-VENT
      nodes: 10
      edges: 6
      paths: 1
      description: 普通通风系统
      
    - system_id: INT-CLOCK
      nodes: 10
      edges: 7
      paths: 2
      description: 时钟系统
      
    - system_id: INT-IBMS
      nodes: 15
      edges: 12
      paths: 2
      description: 智能化集成平台
      
    # P3 可选系统
    - system_id: PLUMB-STORM
      nodes: 8
      edges: 5
      paths: 1
      description: 雨水排水系统
      
    - system_id: PLUMB-RW
      nodes: 10
      edges: 7
      paths: 1
      description: 中水回用系统
      
    - system_id: INT-IPTV
      nodes: 9
      edges: 6
      paths: 1
      description: 病房电视系统
      
    - system_id: MGAS-N2
      nodes: 7
      edges: 5
      paths: 1
      description: 氮气系统
      
    - system_id: MGAS-CO2
      nodes: 8
      edges: 6
      paths: 1
      description: 二氧化碳系统

  total_batch_6:
    systems: 8
    nodes: 77
    edges: 54
```

---

## 全部系统完整性总结

```yaml
Complete_System_Summary:

  all_batches:
    - batch: 1
      systems: 6
      focus: HVAC核心系统
      
    - batch: 2
      systems: 6
      focus: 电气/医气核心系统
      
    - batch: 3
      systems: 6
      focus: 给排水/消防/智能化核心
      
    - batch: 4
      systems: 7
      focus: 补充关键系统
      
    - batch: 5
      systems: 7
      focus: P2重要系统
      
    - batch: 6
      systems: 8
      focus: P2剩余+P3可选系统

  total_completed:
    systems: 40
    estimated_nodes: 520+
    estimated_edges: 420+
    
  completion_rate:
    P1_CRITICAL: 100% (18/18)
    P2_IMPORTANT: 100% (14/14)
    P3_OPTIONAL: 100% (5/5 主要系统)
    
  remaining_optional:
    note: 以下系统为极少使用的可选系统，暂未建模
    systems:
      - MGAS-He: 氦气系统（极少医院配置）
      - MGAS-Ar: 氩气系统（极少医院配置）
      - ELEC-SOLAR: 光伏发电系统（根据项目配置）
      - HVAC-RADIANT: 辐射供暖/制冷系统（特殊区域）
```

---

**Batch 6 及全部系统拓扑建模完成。**

所有P1关键系统、P2重要系统、P3主要可选系统均已完成拓扑建模。如需补充极少数特殊系统或进行系统间关联矩阵、全局验证等工作，请继续指示。

---