## 🧑‍💻 User


你卡在了【System_Topology:
identity:
 system_id: HVAC-FCU
 system_name: 风机盘管系统
 system_name_en: Fan Coil Unit System
 system_category: HVAC
 system_type: 暖通-末端
 priority_level: P3-GENERAL

 description: |
 医院风机盘管空调系统，服务于病房、办公室等独立控制区域。
 系统由冷热水管路、风机盘管机组、温控器等组成。
 各房间独立控制，灵活性高，适用于负荷特性差异大的区域。
 配合新】。继续

---
## 🤖 Assistant


继续生成 HVAC-FCU 风机盘管系统：

```yaml
System_Topology:

  identity:
    system_id: HVAC-FCU
    system_name: 风机盘管系统
    system_name_en: Fan Coil Unit System
    system_category: HVAC
    system_type: 暖通-末端
    priority_level: P3-GENERAL
    
    description: |
      医院风机盘管空调系统，服务于病房、办公室等独立控制区域。
      系统由冷热水管路、风机盘管机组、温控器等组成。
      各房间独立控制，灵活性高，适用于负荷特性差异大的区域。
      配合新风系统使用，满足室内空气品质要求。
      病房区域采用四管制系统，可同时供冷供热。
      
    design_basis:
      system_type:
        two_pipe: 两管制（供冷或供热）
        four_pipe: 四管制（同时供冷供热，病房推荐）
      fresh_air:
        source: 独立新风系统
        volume: {value: "≥30", unit: "m³/h/人"}
      temperature:
        summer: {value: "24-26", unit: ℃}
        winter: {value: "20-24", unit: ℃}
      noise:
        ward: {value: "≤35", unit: "dB(A)"}
        office: {value: "≤40", unit: "dB(A)"}
    
    parent_system: HVAC-CHP
    
    design_standards:
      - GB 50736-2012 民用建筑供暖通风与空气调节设计规范
      - GB 51039-2014 综合医院建筑设计规范
      - JGJ 71-2004 洁净室施工及验收规范
    
    version: 1.0
    last_updated: 2024

  boundary:
    inputs:
      - boundary_id: HVAC-FCU_IN_001
        name: 冷冻水
        from_system: HVAC-CHP
        medium: WATER-CHW
        parameters:
          supply_temp: {value: 7, unit: ℃}
          return_temp: {value: 12, unit: ℃}
          
      - boundary_id: HVAC-FCU_IN_002
        name: 热水
        from_system: HVAC-CHP
        medium: WATER-HW
        parameters:
          supply_temp: {value: 60, unit: ℃}
          return_temp: {value: 50, unit: ℃}
          
      - boundary_id: HVAC-FCU_IN_003
        name: 电力
        from_system: ELEC-LV
        medium: ELEC-LV
        parameters:
          voltage: 220V AC
          
      - boundary_id: HVAC-FCU_IN_004
        name: 新风
        from_system: HVAC-AHU（新风机组）
        medium: AIR-FA
        
      - boundary_id: HVAC-FCU_IN_005
        name: 控制信号
        from_system: INT-BA
        medium: SIGNAL-BMS
        
    outputs:
      - boundary_id: HVAC-FCU_OUT_001
        name: 空调效果
        to_system: 室内空间
        medium: CONDITIONED_AIR
        
      - boundary_id: HVAC-FCU_OUT_002
        name: 状态反馈
        to_system: INT-BA
        medium: SIGNAL-BMS

  nodes:
  
    source_nodes:
    
      - node_id: HVAC-FCU_SRC_CHW_RISER
        node_name: 冷冻水立管
        node_name_en: Chilled Water Riser
        node_type: Source_Node
        node_category: SRC
        
        function: 楼层冷冻水供应
        medium_in: WATER-CHW
        medium_out: WATER-CHW
        
        is_boundary_input: true
        
        equipment_parameters:
          source: HVAC-CHP分水器
          pipe:
            material: 焊接钢管
            insulation: 橡塑保温
            size: {value: "DN80-DN150", unit: mm}
          accessories:
            - 电动调节阀
            - 压力表
            - 温度计
            - 排气阀
            - 泄水阀
            
        location_hint:
          space_type: 管井
          position: 每个防火分区

      - node_id: HVAC-FCU_SRC_HW_RISER
        node_name: 热水立管
        node_name_en: Hot Water Riser
        node_type: Source_Node
        node_category: SRC
        
        function: 楼层热水供应
        medium_in: WATER-HW
        medium_out: WATER-HW
        
        is_boundary_input: true
        
        equipment_parameters:
          source: HVAC-CHP分水器
          pipe:
            material: 焊接钢管
            insulation: 岩棉保温
            size: {value: "DN50-DN100", unit: mm}
            
        location_hint:
          space_type: 管井

      - node_id: HVAC-FCU_SRC_FRESH_AIR
        node_name: 新风供应
        node_name_en: Fresh Air Supply
        node_type: Source_Node
        node_category: SRC
        
        function: 为FCU区域提供新风
        medium_in: AIR-FA
        medium_out: AIR-FA
        
        is_boundary_input: true
        
        equipment_parameters:
          source: 新风机组（HVAC-AHU）
          distribution:
            type: 新风支管
            method: 接入FCU或独立送风口
            
        location_hint:
          space_type: 吊顶
          distribution: 各房间

    distribution_nodes:
    
      - node_id: HVAC-FCU_DST_FLOOR_HEADER
        node_name: 楼层分集水器
        node_name_en: Floor Header
        node_type: Distribution_Node
        node_subtype: PIP
        node_category: DST
        
        function: 楼层冷热水分配
        medium_in: WATER-CHW/HW
        medium_out: WATER-CHW/HW
        
        multiplicity: multiple
        instance_pattern: HVAC-FCU_DST_HEADER_{Floor}
        
        equipment_parameters:
          types:
            chw_header:
              name: 冷水分集水器
              size: DN100
              outlets: {value: "8-12", unit: "路"}
            hw_header:
              name: 热水分集水器
              size: DN80
              outlets: {value: "8-12", unit: "路"}
          accessories:
            - 电动调节阀（每路）
            - 平衡阀
            - 压力表
            - 温度计
            - 排气阀
            
        control_points:
          sensors:
            - point_id: FH_CHW_SUPPLY_TEMP
              point_name: 冷水供水温度
              point_type: AI
              unit: ℃
            - point_id: FH_CHW_RETURN_TEMP
              point_name: 冷水回水温度
              point_type: AI
              unit: ℃
          status:
            - point_id: FH_VALVE_POS
              point_name: 总阀位置
              point_type: AI
              unit: "%"
        
        location_hint:
          space_type: 管井/设备间
          floor: 每层

      - node_id: HVAC-FCU_DST_FCU
        node_name: 风机盘管机组
        node_name_en: Fan Coil Unit
        node_type: Distribution_Node
        node_subtype: FCU
        node_category: DST
        
        function: 室内空气调节
        medium_in: WATER-CHW/HW + AIR-RA
        medium_out: AIR-SA
        
        multiplicity: multiple
        instance_pattern: HVAC-FCU_DST_FCU_{Building}_{Floor}_{Room}
        typical_quantity: {value: "500-1500", unit: "台", note: "大型医院"}
        
        equipment_parameters:
          types:
            ceiling_concealed:
              name: 卧式暗装
              application: 病房、办公室
              installation: 吊顶内
              noise: {value: "≤32", unit: "dB(A)"}
            ceiling_exposed:
              name: 卧式明装
              application: 走廊、辅助用房
              installation: 吊顶下
            vertical:
              name: 立式明装
              application: 过渡空间
              installation: 地面/窗下
            cassette:
              name: 四出风嵌入式
              application: 大空间、大厅
              installation: 吊顶嵌入
              
          capacity_range:
            small: {value: "2.5-3.5", unit: kW, note: "小房间"}
            medium: {value: "5-7", unit: kW, note: "标准病房"}
            large: {value: "10-14", unit: kW, note: "大房间"}
            
          components:
            coil:
              cooling: 铜管铝翅片（2排）
              heating: 铜管铝翅片（1-2排）
              note: 四管制分开
            fan:
              type: 离心风机
              speed: 三速（高/中/低）
              motor: 电容运转电机
            filter:
              type: 初效过滤器
              efficiency: G3/G4
              washable: true
            drain_pan:
              material: 镀锌板/ABS
              insulation: 保温处理
              
          control:
            thermostat: 室内温控器
            valve:
              type: 电动二通阀
              control: 开关式/比例式
            fan_speed: 三速可调
            
        control_points:
          sensors:
            - point_id: FCU_ROOM_TEMP
              point_name: 室内温度
              point_type: AI
              unit: ℃
              location: 室内温控器
          status:
            - point_id: FCU_RUN
              point_name: 风机运行
              point_type: DI
            - point_id: FCU_SPEED
              point_name: 风机档位
              point_type: DI
              values: [高, 中, 低, 停]
            - point_id: FCU_VALVE_CHW
              point_name: 冷水阀状态
              point_type: DI
            - point_id: FCU_VALVE_HW
              point_name: 热水阀状态
              point_type: DI
          commands:
            - point_id: FCU_ON_OFF
              point_name: 启停控制
              point_type: DO
            - point_id: FCU_SPEED_SP
              point_name: 风速设定
              point_type: AO
              values: [0, 1, 2, 3]
            - point_id: FCU_TEMP_SP
              point_name: 温度设定
              point_type: AO
              range: [16, 30]
              
        alarms:
          - alarm_id: ALM_FCU_FILTER
            alarm_name: 过滤器脏堵
            severity: LOW
            trigger: 运行时间>2000h
          - alarm_id: ALM_FCU_DRAIN
            alarm_name: 冷凝水盘溢出
            severity: MEDIUM
            trigger: 水位开关动作
        
        location_hint:
          space_type: 病房/办公室
          installation: 吊顶内

      - node_id: HVAC-FCU_DST_THERMOSTAT
        node_name: 室内温控器
        node_name_en: Room Thermostat
        node_type: Distribution_Node
        node_subtype: CTR
        node_category: DST
        
        function: 室内温度控制和设定
        medium_in: SIGNAL
        medium_out: CONTROL
        
        multiplicity: multiple
        instance_pattern: HVAC-FCU_DST_THERMO_{Room}
        
        equipment_parameters:
          types:
            basic:
              name: 基础温控器
              features:
                - 温度设定（16-30℃）
                - 风速选择（高/中/低/自动）
                - 模式选择（制冷/制热/通风）
                - 开关控制
            smart:
              name: 智能温控器
              features:
                - LCD显示
                - 时间表编程
                - 网络通讯（BACnet/Modbus）
                - 人体感应
                - 窗磁联动
            medical:
              name: 医用温控器
              features:
                - 抗菌面板
                - 锁定功能（防患者误操作）
                - 中央集控接口
                - 紧急模式
                
          control_logic:
            cooling:
              - 室温>设定+0.5℃ → 开冷水阀
              - 室温<设定-0.5℃ → 关冷水阀
            heating:
              - 室温<设定-0.5℃ → 开热水阀
              - 室温>设定+0.5℃ → 关热水阀
            fan:
              - 自动模式：根据温差调节风速
              - 手动模式：按设定风速运行
              
        control_points:
          sensors:
            - point_id: TC_ROOM_TEMP
              point_name: 室内温度
              point_type: AI
              unit: ℃
            - point_id: TC_SETPOINT
              point_name: 设定温度
              point_type: AI
              unit: ℃
          status:
            - point_id: TC_MODE
              point_name: 运行模式
              point_type: DI
              values: [制冷, 制热, 通风, 停止]
            - point_id: TC_FAN_SPEED
              point_name: 风速档位
              point_type: DI
          commands:
            - point_id: TC_SETPOINT_SP
              point_name: 远程温度设定
              point_type: AO
              range: [16, 30]
            - point_id: TC_LOCK
              point_name: 面板锁定
              point_type: DO
        
        location_hint:
          space_type: 室内墙面
          height: {value: 1.4, unit: m}
          position: 远离热源和直射阳光

      - node_id: HVAC-FCU_DST_WATER_VALVE
        node_name: 电动二通阀
        node_name_en: Motorized Two-way Valve
        node_type: Distribution_Node
        node_subtype: VLV
        node_category: DST
        
        function: 控制FCU冷热水通断
        medium_in: WATER-CHW/HW
        medium_out: WATER-CHW/HW
        
        multiplicity: multiple
        instance_pattern: 每台FCU配1-2个（四管制2个）
        
        equipment_parameters:
          types:
            on_off:
              name: 开关式电动阀
              control: 开/关两位控制
              actuator: 热电执行器
              response_time: {value: 3, unit: min}
              application: 一般区域
            modulating:
              name: 比例式电动阀
              control: 0-100%比例控制
              actuator: 电动执行器
              response_time: {value: 30, unit: s}
              application: 精密控制区域
              
          size: {value: "DN15-DN25", unit: mm}
          pressure: {value: 1.6, unit: MPa}
          
        control_points:
          status:
            - point_id: VALVE_OPEN
              point_name: 阀门开启
              point_type: DI
          commands:
            - point_id: VALVE_CMD
              point_name: 阀门控制
              point_type: DO
        
        location_hint:
          space_type: FCU进水管处
          note: 靠近FCU

    sink_nodes:
    
      - node_id: HVAC-FCU_SNK_WARD
        node_name: 病房空间
        node_name_en: Patient Ward
        node_type: Sink_Node
        node_category: SNK
        
        function: 病房空调环境
        medium_in: AIR-SA
        medium_out: CONDITIONED_ENVIRONMENT
        
        is_boundary_output: true
        
        multiplicity: multiple
        instance_pattern: HVAC-FCU_SNK_WARD_{Building}_{Floor}_{Room}
        typical_quantity: {value: "300-800", unit: "间"}
        
        equipment_parameters:
          ward_types:
            single:
              name: 单人病房
              area: {value: 20, unit: "m²"}
              fcu_capacity: {value: 3.5, unit: kW}
              fresh_air: {value: 80, unit: "m³/h"}
            double:
              name: 双人病房
              area: {value: 30, unit: "m²"}
              fcu_capacity: {value: 5, unit: kW}
              fresh_air: {value: 120, unit: "m³/h"}
            multi:
              name: 多人病房
              area: {value: 50, unit: "m²"}
              fcu_capacity: {value: 7, unit: kW}
              fresh_air: {value: 200, unit: "m³/h"}
            vip:
              name: VIP病房
              area: {value: 40, unit: "m²"}
              fcu_capacity: {value: 7, unit: kW}
              fresh_air: {value: 150, unit: "m³/h"}
              special: 独立控制+高档装修
              
          environment:
            temperature:
              summer: {value: "24-26", unit: ℃}
              winter: {value: "22-24", unit: ℃}
              adjustable: "±2℃"
            humidity: {value: "40-60", unit: "%RH"}
            noise: {value: "≤35", unit: "dB(A)"}
            
        location_hint:
          space_type: 住院楼
          floors: 多层

      - node_id: HVAC-FCU_SNK_OFFICE
        node_name: 办公空间
        node_name_en: Office Space
        node_type: Sink_Node
        node_category: SNK
        
        function: 办公区域空调
        medium_in: AIR-SA
        medium_out: CONDITIONED_ENVIRONMENT
        
        is_boundary_output: true
        
        equipment_parameters:
          office_types:
            private_office:
              name: 独立办公室
              area: {value: "15-30", unit: "m²"}
              fcu_capacity: {value: "3.5-5", unit: kW}
            open_office:
              name: 开放办公区
              area: {value: "100-300", unit: "m²"}
              fcu: 多台FCU或AHU服务
            conference:
              name: 会议室
              area: {value: "30-80", unit: "m²"}
              fcu_capacity: {value: "7-14", unit: kW}
              fresh_air: 加大新风量
              
          environment:
            temperature: {value: "22-26", unit: ℃}
            noise: {value: "≤40", unit: "dB(A)"}
            
        location_hint:
          space_type: 行政办公楼

  edges:
  
    water_distribution:
      - edge_id: HVAC-FCU_EDGE_001
        edge_name: 立管至楼层分水器
        edge_type: PIP
        from_node: HVAC-FCU_SRC_CHW_RISER
        to_node: HVAC-FCU_DST_FLOOR_HEADER
        direction: unidirectional
        medium: WATER-CHW
        pipe_parameters:
          material: 焊接钢管
          insulation: 橡塑保温
          
      - edge_id: HVAC-FCU_EDGE_002
        edge_name: 分水器至FCU
        edge_type: PIP
        from_node: HVAC-FCU_DST_FLOOR_HEADER
        to_node: HVAC-FCU_DST_FCU
        direction: bidirectional
        medium: WATER-CHW
        pipe_parameters:
          material: 镀锌钢管/PPR管
          size: DN20-DN32

    air_flow:
      - edge_id: HVAC-FCU_EDGE_011
        edge_name: 新风至FCU
        edge_type: DUC
        from_node: HVAC-FCU_SRC_FRESH_AIR
        to_node: HVAC-FCU_DST_FCU
        direction: unidirectional
        medium: AIR-FA
        note: 新风接入FCU回风口
        
      - edge_id: HVAC-FCU_EDGE_012
        edge_name: FCU至房间
        edge_type: AIR
        from_node: HVAC-FCU_DST_FCU
        to_node: HVAC-FCU_SNK_WARD
        direction: unidirectional
        medium: AIR-SA

    control:
      - edge_id: HVAC-FCU_EDGE_021
        edge_name: 温控器至FCU
        edge_type: SIG
        from_node: HVAC-FCU_DST_THERMOSTAT
        to_node: HVAC-FCU_DST_FCU
        direction: unidirectional
        medium: SIGNAL-CONTROL
        
      - edge_id: HVAC-FCU_EDGE_022
        edge_name: 温控器至电动阀
        edge_type: SIG
        from_node: HVAC-FCU_DST_THERMOSTAT
        to_node: HVAC-FCU_DST_WATER_VALVE
        direction: unidirectional
        medium: SIGNAL-CONTROL

  typical_paths:
  
    - path_id: HVAC-FCU_PATH_COOLING
      path_name: 病房制冷路径
      path_type: HVAC
      description: 夏季病房空调制冷
      sequence:
        - step: 1
          node: HVAC-FCU_SRC_CHW_RISER
          action: 冷冻水从立管供应
        - step: 2
          node: HVAC-FCU_DST_FLOOR_HEADER
          action: 楼层分配
        - step: 3
          node: HVAC-FCU_DST_WATER_VALVE
          action: 温控开阀
        - step: 4
          node: HVAC-FCU_DST_FCU
          action: 室内空气经盘管冷却
        - step: 5
          node: HVAC-FCU_SNK_WARD
          action: 冷风送入病房

    - path_id: HVAC-FCU_PATH_CONTROL
      path_name: 温度控制路径
      path_type: CTR
      description: 室内温度闭环控制
      sequence:
        - step: 1
          node: HVAC-FCU_DST_THERMOSTAT
          action: 检测室温
        - step: 2
          action: 与设定值比较
        - step: 3
          node: HVAC-FCU_DST_WATER_VALVE
          action: 控制阀门开关
        - step: 4
          node: HVAC-FCU_DST_FCU
          action: 风机运行送风
        - step: 5
          node: HVAC-FCU_SNK_WARD
          action: 室温接近设定值

  control_logic:
  
    individual_room_control:
      name: 单房间独立控制
      description: 每个房间温控器独立控制
      
      control_sequence:
        cooling_mode:
          condition: 室温 > 设定温度 + 死区
          action:
            - 开启冷水阀
            - 根据温差选择风速
            - 持续监测室温
          stop_condition: 室温 < 设定温度 - 死区
          
        heating_mode:
          condition: 室温 < 设定温度 - 死区
          action:
            - 开启热水阀
            - 根据温差选择风速
          stop_condition: 室温 > 设定温度 + 死区
          
        deadband:
          value: {value: 1, unit: ℃}
          purpose: 防止频繁启停
          
    central_override:
      name: 中央集控覆盖
      description: BA系统远程控制
      
      functions:
        temperature_limit:
          description: 限制设定温度范围
          summer: {value: "24-28", unit: ℃}
          winter: {value: "18-24", unit: ℃}
          purpose: 节能管理
          
        schedule_control:
          description: 按时间表控制
          occupied: 正常运行
          unoccupied: 温度放宽/停止
          
        emergency_stop:
          description: 紧急停止所有FCU
          trigger: 火灾报警/水管爆裂
          action: 关闭所有电动阀
          
    window_interlock:
      name: 开窗联锁
      description: 开窗时停止空调
      
      trigger: 窗磁传感器检测到开窗
      action:
        - 关闭电动阀
        - 停止风机（可选）
      recovery: 窗关闭后延时5分钟恢复
      purpose: 节能+防止冷凝
      
    condensate_protection:
      name: 冷凝水保护
      description: 防止冷凝水盘溢出
      
      detection: 水位开关
      action:
        - 报警
        - 关闭冷水阀
        - 继续运行风机排水
      recovery: 人工清理后复位
      
    filter_maintenance:
      name: 过滤器维护提醒
      description: 基于运行时间的维护提醒
      
      trigger: 累计运行 > 2000小时
      action: 维护提醒
      reset: 清洗/更换后手动复位

  alarm_protection:
  
    fcu_alarms:
      - alarm_id: ALM_FCU_DRAIN_OVERFLOW
        alarm_name: 冷凝水溢出
        severity: MEDIUM
        trigger: 水位开关动作
        action: 关冷水阀，通知维修
        
      - alarm_id: ALM_FCU_OFFLINE
        alarm_name: FCU离线
        severity: LOW
        trigger: 通讯中断>10分钟
        action: 检查通讯线路
        
    system_alarms:
      - alarm_id: ALM_FCU_LOW_WATER_TEMP
        alarm_name: 冷冻水温度高
        severity: MEDIUM
        trigger: 供水温度>14℃
        action: 检查冷源
        
      - alarm_id: ALM_FCU_PIPE_LEAK
        alarm_name: 水管泄漏
        severity: HIGH
        trigger: 楼层用水量异常
        action: 关闭楼层阀门，检修

  dependencies:
    
    upstream_dependencies:
      - dependency_id: DEP_FCU_CHW
        from_system: HVAC-CHP
        dependency_type: COOLING
        criticality: HIGH
        
      - dependency_id: DEP_FCU_HW
        from_system: HVAC-CHP
        dependency_type: HEATING
        criticality: HIGH
        
      - dependency_id: DEP_FCU_POWER
        from_system: ELEC-LV
        dependency_type: POWER_SUPPLY
        criticality: MEDIUM
        
      - dependency_id: DEP_FCU_FA
        from_system: HVAC-AHU
        dependency_type: FRESH_AIR
        criticality: MEDIUM
        
    downstream_dependencies:
      - dependency_id: DEP_TO_WARDS
        to_system: 病房
        dependency_type: CONDITIONED_AIR
        criticality: MEDIUM
        
      - dependency_id: DEP_TO_OFFICES
        to_system: 办公室
        dependency_type: CONDITIONED_AIR
        criticality: LOW
```

---

## 系统 5.4: ELEC-EL 电梯系统

```yaml
System_Topology:

  identity:
    system_id: ELEC-EL
    system_name: 电梯系统
    system_name_en: Elevator System
    system_category: ELEC
    system_type: 电气-垂直运输
    priority_level: P2-BUSINESS_CRITICAL
    
    description: |
      医院电梯系统，提供人员和物资的垂直运输服务。
      包括客梯、病床梯、担架梯、货梯、消防电梯等多种类型。
      系统与门禁、火灾报警、BA系统联动。
      电梯具有群控功能，优化调度，减少等候时间。
      医院电梯需考虑感染控制、洁污分流等特殊需求。
      
    design_basis:
      elevator_types:
        passenger:
          name: 客梯
          capacity: {value: "1000-1600", unit: kg}
          speed: {value: "1.5-2.5", unit: "m/s"}
          application: 门诊、行政
        bed:
          name: 病床梯
          capacity: {value: "1600-2000", unit: kg}
          car_size: {value: "1400×2400", unit: mm}
          speed: {value: "1.0-1.5", unit: "m/s"}
          application: 住院楼
        stretcher:
          name: 担架梯
          capacity: {value: "1350-1600", unit: kg}
          car_depth: {value: "≥2100", unit: mm}
          application: 急诊、手术
        freight:
          name: 货梯
          capacity: {value: "2000-3000", unit: kg}
          speed: {value: "0.5-1.0", unit: "m/s"}
          application: 物资运输
        fire:
          name: 消防电梯
          capacity: {value: "≥1000", unit: kg}
          speed: {value: "≥1.0", unit: "m/s"}
          special: 消防专用，火灾时可用
          
      traffic_analysis:
        peak_hour: "08:00-09:00"
        handling_capacity: {value: "≥12", unit: "%", note: "5分钟处理量"}
        waiting_time: {value: "<60", unit: s}
        
    design_standards:
      - GB 7588-2020 电梯制造与安装安全规范
      - GB 50763-2012 无障碍设计规范
      - GB 51039-2014 综合医院建筑设计规范
      - GB 50016-2014 建筑设计防火规范
    
    version: 1.0
    last_updated: 2024

  boundary:
    inputs:
      - boundary_id: ELEC-EL_IN_001
        name: 电力供应
        from_system: ELEC-LV-MAIN
        medium: ELEC-LV
        parameters:
          voltage: 380V AC
          note: 三相动力电源
          
      - boundary_id: ELEC-EL_IN_002
        name: 应急电源
        from_system: ELEC-EPS
        medium: ELEC-LV
        parameters:
          for: 消防电梯/病床梯
          
      - boundary_id: ELEC-EL_IN_003
        name: 火灾信号
        from_system: FIRE-FAS
        medium: SIGNAL-FIRE
        
      - boundary_id: ELEC-EL_IN_004
        name: 门禁控制
        from_system: INT-SEC
        medium: SIGNAL-ACCESS
        
      - boundary_id: ELEC-EL_IN_005
        name: 监控信号
        from_system: INT-BA
        medium: SIGNAL-BMS
        
    outputs:
      - boundary_id: ELEC-EL_OUT_001
        name: 垂直运输服务
        to_system: 建筑各层
        medium: TRANSPORT
        
      - boundary_id: ELEC-EL_OUT_002
        name: 状态反馈
        to_system: INT-BA
        medium: SIGNAL-BMS
        
      - boundary_id: ELEC-EL_OUT_003
        name: 视频监控
        to_system: INT-SEC
        medium: VIDEO

  nodes:
  
    source_nodes:
    
      - node_id: ELEC-EL_SRC_POWER
        node_name: 电梯电源
        node_name_en: Elevator Power Supply
        node_type: Source_Node
        node_category: SRC
        
        function: 为电梯系统提供电力
        medium_in: ELEC-LV
        medium_out: ELEC-LV
        
        is_boundary_input: true
        
        equipment_parameters:
          normal_power:
            source: 低压配电室
            voltage: 380V AC
            capacity: 根据电梯数量
          emergency_power:
            source: EPS/发电机
            for: 消防电梯、病床梯
            switchover: {value: "<15", unit: s}
          ups:
            for: 电梯控制系统
            duration: {value: 30, unit: min}
            
        location_hint:
          space_type: 电梯机房
          position: 屋顶或地下

      - node_id: ELEC-EL_SRC_FIRE_SIGNAL
        node_name: 火灾信号输入
        node_name_en: Fire Signal Input
        node_type: Source_Node
        node_category: SRC
        
        function: 接收火灾报警信号
        medium_in: SIGNAL-FIRE
        medium_out: SIGNAL-FIRE
        
        is_boundary_input: true
        
        equipment_parameters:
          source: FIRE-FAS
          signals:
            - 火灾确认信号
            - 着火层信号
            - 消防控制室手动信号
            
        location_hint:
          space_type: 电梯控制柜

    distribution_nodes:
    
      - node_id: ELEC-EL_DST_MACHINE_ROOM
        node_name: 电梯机房
        node_name_en: Elevator Machine Room
        node_type: Distribution_Node
        node_subtype: EQP
        node_category: DST
        
        function: 电梯驱动和控制
        medium_in: ELEC-LV
        medium_out: MECHANICAL_POWER
        
        multiplicity: multiple
        instance_pattern: ELEC-EL_DST_MACHINEROOM_{Group}
        
        equipment_parameters:
          types:
            geared:
              name: 有机房曳引电梯
              traction: 曳引机+减速箱
              location: 屋顶机房
              application: 中低速电梯
            gearless:
              name: 无齿轮曳引电梯
              traction: 永磁同步曳引机
              location: 屋顶机房
              application: 高速电梯
            mrl:
              name: 无机房电梯
              traction: 薄型曳引机
              location: 井道顶部
              application: 空间受限
              
          components:
            traction_machine:
              type: 永磁同步/异步
              power: {value: "10-50", unit: kW}
              control: 变频调速
            controller:
              type: 微机控制
              function:
                - 运行控制
                - 群控调度
                - 故障诊断
                - 远程监控
            governor:
              type: 限速器
              function: 超速保护
            buffer:
              type: 液压/弹簧缓冲器
              location: 井道底部
              
          environment:
            temperature: {value: "5-40", unit: ℃}
            ventilation: 机械通风
            fire_rating: 耐火1h
            
        control_points:
          sensors:
            - point_id: MR_TEMP
              point_name: 机房温度
              point_type: AI
              unit: ℃
          status:
            - point_id: MR_POWER
              point_name: 主电源状态
              point_type: DI
            - point_id: MR_EMERGENCY_POWER
              point_name: 应急电源状态
              point_type: DI
          alarms:
            - point_id: MR_HIGH_TEMP
              alarm_name: 机房温度高
              trigger: ">40℃"
              severity: MEDIUM
        
        location_hint:
          space_type: 电梯机房
          floor: 屋顶

      - node_id: ELEC-EL_DST_CAR
        node_name: 电梯轿厢
        node_name_en: Elevator Car
        node_type: Distribution_Node
        node_subtype: EQP
        node_category: DST
        
        function: 载运乘客和货物
        medium_in: MECHANICAL_POWER
        medium_out: TRANSPORT
        
        multiplicity: multiple
        instance_pattern: ELEC-EL_DST_CAR_{Type}_{Seq}
        typical_quantity: {value: "10-30", unit: "台", note: "大型医院"}
        
        equipment_parameters:
          types:
            passenger_car:
              name: 客梯轿厢
              capacity: {value: 1350, unit: kg}
              persons: {value: 18, unit: "人"}
              size:
                width: {value: 1600, unit: mm}
                depth: {value: 1500, unit: mm}
                height: {value: 2400, unit: mm}
              door:
                type: 中分双折门
                width: {value: 900, unit: mm}
              finish: 不锈钢/装饰板
              
            bed_car:
              name: 病床梯轿厢
              capacity: {value: 1600, unit: kg}
              size:
                width: {value: 1400, unit: mm}
                depth: {value: 2400, unit: mm}
                height: {value: 2400, unit: mm}
              door:
                type: 旁开双扇门
                width: {value: 1200, unit: mm}
              special:
                - 加宽加深
                - 防撞护墙
                - 专用呼叫
                
            stretcher_car:
              name: 担架梯轿厢
              capacity: {value: 1350, unit: kg}
              size:
                width: {value: 1100, unit: mm}
                depth: {value: 2100, unit: mm}
                height: {value: 2400, unit: mm}
              door:
                type: 贯通门（前后开门）
                width: {value: 900, unit: mm}
              special: 急救担架进出
              
            freight_car:
              name: 货梯轿厢
              capacity: {value: 2500, unit: kg}
              size:
                width: {value: 2000, unit: mm}
                depth: {value: 2500, unit: mm}
                height: {value: 2400, unit: mm}
              door:
                type: 中分双折门/垂直滑门
                width: {value: 1500, unit: mm}
              floor: 钢板花纹地面
              
            fire_car:
              name: 消防电梯轿厢
              capacity: {value: 1350, unit: kg}
              special:
                - 消防专用按钮
                - 返回基站功能
                - 专用通讯
                - 防水措施
                
          common_features:
            lighting:
              normal: LED顶灯
              emergency: 应急照明（3h）
            ventilation:
              type: 强制通风
              rate: {value: 20, unit: "次/h"}
            intercom:
              type: 五方对讲
              parties: [轿厢, 机房, 轿顶, 底坑, 管理中心]
            display:
              type: LCD/LED
              content: [楼层, 方向, 载重, 消息]
            camera:
              type: 半球摄像机
              storage: 30天
            button:
              type: 触摸/机械按钮
              accessibility: 盲文+语音报站
              
        control_points:
          sensors:
            - point_id: CAR_LOAD
              point_name: 轿厢载重
              point_type: AI
              unit: kg
            - point_id: CAR_POSITION
              point_name: 轿厢位置
              point_type: AI
              unit: 层
          status:
            - point_id: CAR_DOOR_OPEN
              point_name: 轿门开启
              point_type: DI
            - point_id: CAR_DIRECTION
              point_name: 运行方向
              point_type: DI
              values: [上行, 下行, 停止]
            - point_id: CAR_MODE
              point_name: 运行模式
              point_type: DI
              values: [正常, 消防, 检修, 故障]
          alarms:
            - point_id: CAR_OVERLOAD
              alarm_name: 超载
              severity: MEDIUM
            - point_id: CAR_TRAPPED
              alarm_name: 困人
              severity: CRITICAL
        
        location_hint:
          space_type: 电梯井道

      - node_id: ELEC-EL_DST_CONTROLLER
        node_name: 电梯群控系统
        node_name_en: Elevator Group Controller
        node_type: Distribution_Node
        node_subtype: CTR
        node_category: DST
        
        function: 多台电梯智能调度
        medium_in: SIGNAL
        medium_out: CONTROL
        
        multiplicity: multiple
        instance_pattern: ELEC-EL_DST_GROUPCTRL_{Zone}
        
        equipment_parameters:
          type: 智能群控系统
          control_range: {value: "2-8", unit: "台/组"}
          
          algorithms:
            call_assignment:
              name: 呼叫分配算法
              method:
                - 最近电梯优先
                - 载重平衡
                - 方向优化
                - 等候时间最小
            traffic_prediction:
              name: 交通预测
              method:
                - 历史数据学习
                - 高峰时段预判
                - 提前调度
            energy_saving:
              name: 节能模式
              method:
                - 低峰期减少运行台数
                - 待机层优化
                - 再生制动能量回收
                
          functions:
            normal_mode:
              - 智能派梯
              - 满载直驶
              - 高峰分区
            special_modes:
              vip_priority:
                name: VIP优先
                trigger: 刷卡/指定层站
              medical_priority:
                name: 医疗优先
                trigger: 急救按钮
                action: 最近电梯直达
              cleaning_mode:
                name: 清洁模式
                application: 夜间清洁
                action: 指定电梯独立运行
                
        control_points:
          sensors:
            - point_id: GROUP_WAIT_TIME
              point_name: 平均等候时间
              point_type: AI
              unit: s
            - point_id: GROUP_UTILIZATION
              point_name: 利用率
              point_type: AI
              unit: "%"
          status:
            - point_id: GROUP_ACTIVE_CARS
              point_name: 运行台数
              point_type: AI
              unit: "台"
          commands:
            - point_id: GROUP_MODE
              point_name: 群控模式
              point_type: DO
              values: [正常, 高峰上行, 高峰下行, 节能]
        
        location_hint:
          space_type: 电梯机房/控制室

      - node_id: ELEC-EL_DST_LANDING
        node_name: 电梯层站
        node_name_en: Elevator Landing
        node_type: Distribution_Node
        node_subtype: TRM
        node_category: DST
        
        function: 各层乘梯入口
        medium_in: 乘客
        medium_out: 乘客
        
        multiplicity: multiple
        instance_pattern: ELEC-EL_DST_LANDING_{Floor}
        
        equipment_parameters:
          components:
            landing_door:
              type: 层门
              material: 不锈钢/喷塑钢板
              fire_rating: 乙级防火门
              interlock: 门锁联锁
            call_button:
              type: 呼梯按钮
              style: 触摸/机械
              accessibility: 盲文
            display:
              type: 楼层显示器
              content: [轿厢位置, 方向, 满载]
            indicator:
              type: 到站灯/声音
              function: 提示电梯到达
              
          accessibility:
            - 盲文按钮
            - 语音播报
            - 低位按钮（≤1.1m）
            - 轮椅空间
            
          special_features:
            card_reader:
              type: IC卡/人脸识别
              function: 门禁联动
              application: 限制楼层
            emergency_button:
              type: 紧急呼叫
              location: 首层/重点层
              
        control_points:
          status:
            - point_id: LANDING_CALL_UP
              point_name: 上行呼叫
              point_type: DI
            - point_id: LANDING_CALL_DOWN
              point_name: 下行呼叫
              point_type: DI
            - point_id: LANDING_DOOR_OPEN
              point_name: 层门开启
              point_type: DI
        
        location_hint:
          space_type: 各层电梯厅
          floors: 所有服务楼层

    sink_nodes:
    
      - node_id: ELEC-EL_SNK_SERVICE
        node_name: 电梯运输服务
        node_name_en: Elevator Transport Service
        node_type: Sink_Node
        node_category: SNK
        
        function: 提供垂直运输
        medium_in: TRANSPORT
        medium_out: SERVICE
        
        is_boundary_output: true
        
        equipment_parameters:
          service_areas:
            outpatient_building:
              name: 门诊楼
              elevators:
                passenger: {value: 4, unit: "台"}
                stretcher: {value: 2, unit: "台"}
              floors: "B2-6F"
            inpatient_building:
              name: 住院楼
              elevators:
                bed: {value: 6, unit: "台"}
                passenger: {value: 2, unit: "台"}
                freight: {value: 2, unit: "台"}
              floors: "B1-15F"
            emergency_building:
              name: 急诊楼
              elevators:
                stretcher: {value: 2, unit: "台"}
                passenger: {value: 2, unit: "台"}
              floors: "B1-5F"
            medical_technology:
              name: 医技楼
              elevators:
                bed: {value: 2, unit: "台"}
                passenger: {value: 2, unit: "台"}
              floors: "B2-4F"
              
          service_metrics:
            waiting_time:
              average: {value: "<45", unit: s}
              peak: {value: "<90", unit: s}
            handling_capacity: {value: "≥12", unit: "%/5min"}
            availability: {value: ">99", unit: "%"}
            
        location_hint:
          space_type: 全院

  edges:
  
    power_edges:
      - edge_id: ELEC-EL_EDGE_001
        edge_name: 电源至机房
        edge_type: CAB
        from_node: ELEC-EL_SRC_POWER
        to_node: ELEC-EL_DST_MACHINE_ROOM
        direction: unidirectional
        medium: ELEC-LV
        
    mechanical_edges:
      - edge_id: ELEC-EL_EDGE_011
        edge_name: 机房至轿厢
        edge_type: MECH
        from_node: ELEC-EL_DST_MACHINE_ROOM
        to_node: ELEC-EL_DST_CAR
        direction: unidirectional
        medium: MECHANICAL_POWER
        note: 曳引绳/钢带传动
        
    control_edges:
      - edge_id: ELEC-EL_EDGE_021
        edge_name: 群控至轿厢
        edge_type: SIG
        from_node: ELEC-EL_DST_CONTROLLER
        to_node: ELEC-EL_DST_CAR
        direction: bidirectional
        medium: SIGNAL-CONTROL
        
      - edge_id: ELEC-EL_EDGE_022
        edge_name: 层站至群控
        edge_type: SIG
        from_node: ELEC-EL_DST_LANDING
        to_node: ELEC-EL_DST_CONTROLLER
        direction: unidirectional
        medium: SIGNAL-CALL

  typical_paths:
  
    - path_id: ELEC-EL_PATH_NORMAL
      path_name: 正常运行路径
      path_type: TRANS
      description: 乘客正常乘梯
      sequence:
        - step: 1
          node: ELEC-EL_DST_LANDING
          action: 乘客按下呼梯按钮
        - step: 2
          node: ELEC-EL_DST_CONTROLLER
          action: 群控系统分配电梯
        - step: 3
          node: ELEC-EL_DST_CAR
          action: 轿厢响应，到达层站
        - step: 4
          node: ELEC-EL_DST_LANDING
          action: 开门，乘客进入
        - step: 5
          node: ELEC-EL_DST_CAR
          action: 乘客按目的楼层
        - step: 6
          node: ELEC-EL_DST_CAR
          action: 轿厢运行至目的层
        - step: 7
          action: 开门，乘客离开

    - path_id: ELEC-EL_PATH_FIRE
      path_name: 消防运行路径
      path_type: FIRE
      description: 火灾时电梯迫降
      sequence:
        - step: 1
          node: ELEC-EL_SRC_FIRE_SIGNAL
          action: 接收火灾确认信号
        - step: 2
          node: ELEC-EL_DST_CONTROLLER
          action: 触发消防模式
        - step: 3
          node: ELEC-EL_DST_CAR
          action: 所有电梯就近停靠
        - step: 4
          node: ELEC-EL_DST_CAR
          action: 开门疏散乘客
        - step: 5
          node: ELEC-EL_DST_CAR
          action: 非消防电梯返回基站停止
        - step: 6
          node: ELEC-EL_DST_CAR
          action: 消防电梯供消防员使用

    - path_id: ELEC-EL_PATH_EMERGENCY
      path_name: 医疗紧急路径
      path_type: MED
      description: 急救患者优先运送
      sequence:
        - step: 1
          node: ELEC-EL_DST_LANDING
          action: 按下医疗紧急按钮
        - step: 2
          node: ELEC-EL_DST_CONTROLLER
          action: 触发医疗优先模式
        - step: 3
          node: ELEC-EL_DST_CAR
          action: 最近病床梯/担架梯响应
        - step: 4
          node: ELEC-EL_DST_CAR
          action: 直达呼叫层（不停靠其他层）
        - step: 5
          action: 优先运送患者

  control_logic:
  
    fire_mode:
      name: 消防模式
      description: 火灾时电梯控制
      
      trigger:
        - FIRE-FAS火灾确认信号
        - 消防控制室手动触发
        
      response:
        non_fire_elevators:
          step_1: 取消所有呼叫
          step_2: 就近楼层停靠
          step_3: 开门疏散乘客
          step_4: 返回基站（通常为首层）
          step_5: 关门停止运行
          step_6: 切断电源（手动）
          
        fire_elevator:
          step_1: 进入消防专用模式
          step_2: 仅响应轿内消防按钮
          step_3: 由消防员控制运行
          
      interlock:
        - 不响应普通呼叫
        - 不停靠着火层
        - 可手动控制至任意层
        
    medical_priority:
      name: 医疗优先模式
      description: 急救患者紧急运送
      
      trigger:
        - 医疗紧急按钮
        - 急诊呼叫
        - 手术室呼叫
        
      response:
        - 最近病床梯/担架梯响应
        - 直接到达呼叫层
        - 不停靠中间层站
        - 到达后保持开门
        
      timeout: {value: 3, unit: min, note: "自动恢复正常"}
      
    access_control:
      name: 门禁联动
      description: 与门禁系统联动控制楼层
      
      function:
        floor_restriction:
          - 刷卡后开放对应楼层
          - 未授权楼层按钮无效
        vip_service:
          - VIP卡优先派梯
          - 专用楼层直达
        time_control:
          - 夜间部分楼层锁定
          - 周末减少服务楼层
          
    energy_saving:
      name: 节能模式
      description: 低峰期节能运行
      
      trigger: 
        low_traffic: 连续10分钟无呼叫
        night_time: "22:00-06:00"
        
      actions:
        - 减少运行台数
        - 待机电梯关闭照明/空调
        - 电梯停靠在优化楼层
        
      recovery:
        trigger: 有呼叫时
        time: {value: "<30", unit: s}
        
    trapped_rescue:
      name: 困人救援
      description: 电梯困人时的应急处理
      
      detection:
        - 乘客按下紧急按钮
        - 轿厢长时间不动
        - 通讯呼叫
        
      response:
        step_1: 五方对讲确认
        step_2: 通知监控中心
        step_3: 派遣救援人员
        step_4: 启动应急照明和通风
        step_5: ARD（自动救援装置）运行至最近层开门
        step_6: 人工解救（如ARD失效）
        
      record:
        - 困人时间
        - 救援响应时间
        - 原因分析

  alarm_protection:
  
    elevator_alarms:
      - alarm_id: ALM_EL_TRAPPED
        alarm_name: 电梯困人
        severity: CRITICAL
        trigger: 紧急按钮/通讯呼叫
        action: 立即救援
        response_time: {value: "<30", unit: min}
        
      - alarm_id: ALM_EL_FAULT
        alarm_name: 电梯故障
        severity: HIGH
        trigger: 控制系统检测故障
        action: 停止运行，通知维修
        
      - alarm_id: ALM_EL_OVERLOAD
        alarm_name: 超载报警
        severity: MEDIUM
        trigger: 载重>额定110%
        action: 蜂鸣提示，不关门
        
      - alarm_id: ALM_EL_DOOR_FAULT
        alarm_name: 门故障
        severity: MEDIUM
        trigger: 开关门超时
        action: 报警，检修
        
    system_alarms:
      - alarm_id: ALM_EL_POWER_FAIL
        alarm_name: 电源故障
        severity: HIGH
        trigger: 主电源失电
        action: 切换应急电源
        
      - alarm_id: ALM_EL_COMM_FAIL
        alarm_name: 通讯故障
        severity: MEDIUM
        trigger: 与监控中心通讯中断
        action: 本地运行，通知检查

  dependencies:
    
    upstream_dependencies:
      - dependency_id: DEP_EL_POWER
        from_system: ELEC-LV-MAIN
        dependency_type: POWER_SUPPLY
        criticality: CRITICAL
        
      - dependency_id: DEP_EL_EPS
        from_system: ELEC-EPS
        dependency_type: EMERGENCY_POWER
        criticality: HIGH
        for: 消防电梯/病床梯
        
      - dependency_id: DEP_EL_FAS
        from_system: FIRE-FAS
        dependency_type: FIRE_SIGNAL
        criticality: CRITICAL
        description: 火灾联动
        
      - dependency_id: DEP_EL_SEC
        from_system: INT-SEC
        dependency_type: ACCESS_CONTROL
        criticality: MEDIUM
        description: 门禁联动
        
    downstream_dependencies:
      - dependency_id: DEP_TO_BA
        to_system: INT-BA
        dependency_type: MONITORING
        criticality: MEDIUM
        description: 运行监控
        
      - dependency_id: DEP_TO_SEC_VIDEO
        to_system: INT-SEC
        dependency_type: VIDEO
        criticality: MEDIUM
        description: 轿厢视频监控
```

---

# 第五批次输出完成

## 本批次系统总结

| 系统ID | 系统名称 | 类别 | 优先级 |
|--------|----------|------|--------|
| HVAC-CHP | 冷热源系统 | 暖通 | P1-任务关键 |
| HVAC-AHU | 空调机组系统 | 暖通 | P2-业务关键 |
| HVAC-FCU | 风机盘管系统 | 暖通 | P3-一般 |
| ELEC-EL | 电梯系统 | 电气 | P2-业务关键 |

## 暖通系统层级关系

```
HVAC-CHP（冷热源）
  ├── 冷水机组 → 冷冻水7℃
  ├── 锅炉 → 热水60℃
  ├── 冷却塔 → 冷却水散热
  └── 水泵 → 输送动力
        │
        ├── → HVAC-AHU（空调机组）
        │     ├── 新风处理
        │     ├── 组合式空调箱
        │     ├── 全热回收
        │     └── VAV末端
        │
        ├── → HVAC-FCU（风机盘管）
        │     ├── 病房区域
        │     ├── 办公区域
        │     └── 独立控制
        │
        ├── → MED-OR（手术室空调）
        └── → MED-ICU（ICU空调）
```

## 电梯系统联动关系

```
ELEC-EL（电梯系统）
  ├── ← ELEC-LV（正常电源）
  ├── ← ELEC-EPS（应急电源 → 消防梯/病床梯）
  ├── ← FIRE-FAS（火灾联动 → 迫降/消防模式）
  ├── ← INT-SEC（门禁联动 → 楼层控制）
  ├── → INT-BA（状态监控）
  └── → INT-SEC（视频监控）
```

---

## 五批次完成系统汇总

| 批次 | 系统数量 | 系统列表 |
|------|----------|----------|
| 第一批 | 5个 | MGAS-O2, MGAS-VAC, MGAS-AIR, ELEC-HV, ELEC-LV |
| 第二批 | 5个 | ELEC-EPS, ELEC-UPS, PLUMB-DWS, PLUMB-HWS, PLUMB-SAN |
| 第三批 | 4个 | INT-BA, INT-SEC, INT-NUR, MGAS-N2O |
| 第四批 | 6个 | FIRE-FAS, FIRE-SPS, FIRE-EXH, MED-OR, MED-ICU, MED-LAB |
| 第五批 | 4个 | HVAC-CHP, HVAC-AHU, HVAC-FCU, ELEC-EL |

**总计：24个系统**

---

**第六批次预告：** 将输出剩余系统和综合集成内容：
1. PLUMB-RW 雨水系统
2. ELEC-LTG 照明系统
3. 系统间完整依赖关系总图
4. 跨系统联动场景汇总
5. 数据点统计与分类

请确认第五批次内容后，我将继续输出第六批次（最后一批）。

---