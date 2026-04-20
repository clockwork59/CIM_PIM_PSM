# Agent-01 系统拓扑建模师 - 第五批次：暖通系统详细设计 + 电梯系统

## 第五批次：暖通系统详细设计 + 电梯系统（4个系统）

---

# 暖通系统（3个系统）

## 系统 5.1: HVAC-CHP 冷热源系统

```yaml
System_Topology:

  # ========================================
  # IDENTITY SECTION - 系统标识
  # ========================================
  identity:
    system_id: HVAC-CHP
    system_name: 冷热源系统
    system_name_en: Chiller and Heating Plant
    system_category: HVAC
    system_type: 暖通-冷热源
    priority_level: P1-MISSION_CRITICAL
  
    description: |
      医院中央冷热源系统，为全院空调系统提供冷冻水和热水。
      冷源：采用离心式/螺杆式冷水机组，配合冷却塔散热。
      热源：采用燃气锅炉/市政热力/空气源热泵。
      系统采用一次泵变流量或二次泵系统，实现高效节能运行。
      手术室、ICU等关键区域配置独立备用冷热源。
    
    design_basis:
      cooling:
        peak_load: {value: 8000, unit: kW, note: "典型大型医院"}
        chiller_config: "N+1冗余"
        chw_supply: {value: 7, unit: ℃}
        chw_return: {value: 12, unit: ℃}
        chw_delta_t: {value: 5, unit: ℃}
      
      heating:
        peak_load: {value: 5000, unit: kW}
        boiler_config: "N+1冗余"
        hw_supply: {value: 60, unit: ℃}
        hw_return: {value: 50, unit: ℃}
        hw_delta_t: {value: 10, unit: ℃}
      
      redundancy:
        critical_areas: 手术室/ICU独立备用冷源
        backup_time: {value: 2, unit: h}
      
    child_systems:
      - HVAC-AHU  # 空调机组
      - HVAC-FCU  # 风机盘管
      - MED-OR    # 手术室空调
      - MED-ICU   # ICU空调
  
    design_standards:
      - GB 50019-2015 工业建筑供暖通风与空气调节设计规范
      - GB 50736-2012 民用建筑供暖通风与空气调节设计规范
      - GB 51039-2014 综合医院建筑设计规范
  
    version: 1.0
    last_updated: 2024

  # ========================================
  # BOUNDARY SECTION - 系统边界
  # ========================================
  boundary:
  
    inputs:
      - boundary_id: HVAC-CHP_IN_001
        name: 电力供应
        from_system: ELEC-LV-MAIN
        medium: ELEC-LV
        parameters:
          voltage: {value: 380, unit: V}
          note: 冷机/水泵/冷却塔用电
        
      - boundary_id: HVAC-CHP_IN_002
        name: 天然气
        from_system: 市政燃气
        medium: GAS-NG
        parameters:
          pressure: {value: 0.2, unit: MPa}
          note: 燃气锅炉用
        
      - boundary_id: HVAC-CHP_IN_003
        name: 补水
        from_system: PLUMB-DWS
        medium: WATER-PW
        parameters:
          treatment: 软化处理
        
      - boundary_id: HVAC-CHP_IN_004
        name: 控制信号
        from_system: INT-BA
        medium: SIGNAL-BMS
      
    outputs:
      - boundary_id: HVAC-CHP_OUT_001
        name: 冷冻水供应
        to_system: HVAC-AHU/FCU
        medium: WATER-CHW
        parameters:
          supply_temp: {value: 7, unit: ℃}
        
      - boundary_id: HVAC-CHP_OUT_002
        name: 热水供应
        to_system: HVAC-AHU/FCU
        medium: WATER-HW
        parameters:
          supply_temp: {value: 60, unit: ℃}
        
      - boundary_id: HVAC-CHP_OUT_003
        name: 状态反馈
        to_system: INT-BA
        medium: SIGNAL-BMS

  # ========================================
  # NODES SECTION - 节点定义
  # ========================================
  nodes:

    source_nodes:
  
      - node_id: HVAC-CHP_SRC_POWER
        node_name: 冷热源电力供应
        node_name_en: CHP Power Supply
        node_type: Source_Node
        node_category: SRC
      
        function: 为冷热源设备提供电力
        medium_in: ELEC-LV
        medium_out: ELEC-LV
      
        is_boundary_input: true
      
        equipment_parameters:
          source: 低压配电室
          voltage: 380V AC
          capacity: {value: 3000, unit: kVA, note: "冷热源总容量"}
          redundancy: 双电源切换
        
        location_hint:
          space_type: 配电室
          supply_to: 冷热源机房

      - node_id: HVAC-CHP_SRC_GAS
        node_name: 天然气供应
        node_name_en: Natural Gas Supply
        node_type: Source_Node
        node_category: SRC
      
        function: 为燃气锅炉提供燃料
        medium_in: GAS-NG
        medium_out: GAS-NG
      
        is_boundary_input: true
      
        equipment_parameters:
          source: 市政燃气管网
          pressure:
            supply: {value: 0.2, unit: MPa}
            reduced: {value: 0.01, unit: MPa, note: "锅炉前"}
          metering: 燃气表计量
          safety:
            - 燃气泄漏探测器
            - 紧急切断阀
            - 通风设施
          
        location_hint:
          space_type: 室外调压站/锅炉房

      - node_id: HVAC-CHP_SRC_MAKEUP_WATER
        node_name: 系统补水
        node_name_en: Makeup Water
        node_type: Source_Node
        node_category: SRC
      
        function: 补充系统损失水量
        medium_in: WATER-PW
        medium_out: WATER-SOFT
      
        is_boundary_input: true
      
        equipment_parameters:
          source: 生活给水
          treatment:
            type: 软化处理
            hardness: {value: "<50", unit: "mg/L"}
          tank:
            type: 软化水箱
            volume: {value: 10, unit: "m³"}
          pump:
            type: 定压补水泵
            flow: {value: 5, unit: "m³/h"}
          
        control_points:
          sensors:
            - point_id: MAKEUP_LEVEL
              point_name: 软化水箱液位
              point_type: AI
              unit: "%"
            - point_id: SYSTEM_PRESSURE
              point_name: 系统定压压力
              point_type: AI
              unit: MPa
          status:
            - point_id: MAKEUP_PUMP_RUN
              point_name: 补水泵运行
              point_type: DI
      
        location_hint:
          space_type: 水处理间

    distribution_nodes:
  
      - node_id: HVAC-CHP_DST_CHILLER
        node_name: 冷水机组
        node_name_en: Chiller
        node_type: Distribution_Node
        node_subtype: EQP
        node_category: DST
      
        function: 制取冷冻水
        medium_in: ELEC-LV + WATER-CW
        medium_out: WATER-CHW
      
        multiplicity: multiple
        instance_pattern: HVAC-CHP_DST_CHILLER_{Seq}
        typical_quantity: {value: "3-5", unit: "台"}
      
        equipment_parameters:
          types:
            centrifugal:
              name: 离心式冷水机组
              capacity: {value: "1500-3000", unit: kW}
              cop: {value: "5.5-6.5", unit: ""}
              application: 大容量基载
              refrigerant: R134a
            screw:
              name: 螺杆式冷水机组
              capacity: {value: "500-1500", unit: kW}
              cop: {value: "4.5-5.5", unit: ""}
              application: 部分负荷/调峰
              refrigerant: R134a/R410A
          typical_config:
            - 离心机 2000kW × 3台
            - 螺杆机 1000kW × 2台（调峰+备用）
          
          operating_parameters:
            chw_supply: {value: 7, unit: ℃}
            chw_return: {value: 12, unit: ℃}
            cw_supply: {value: 32, unit: ℃, note: "冷却水进"}
            cw_return: {value: 37, unit: ℃, note: "冷却水出"}
          
          control:
            type: 变频调节/导叶调节
            capacity_control: 10%-100%
            staging: 自动加减机
          
        control_points:
          sensors:
            - point_id: CH_CHWS_TEMP
              point_name: 冷冻水供水温度
              point_type: AI
              unit: ℃
            - point_id: CH_CHWR_TEMP
              point_name: 冷冻水回水温度
              point_type: AI
              unit: ℃
            - point_id: CH_CWS_TEMP
              point_name: 冷却水供水温度
              point_type: AI
              unit: ℃
            - point_id: CH_CWR_TEMP
              point_name: 冷却水回水温度
              point_type: AI
              unit: ℃
            - point_id: CH_CURRENT
              point_name: 运行电流
              point_type: AI
              unit: A
            - point_id: CH_LOAD
              point_name: 负荷率
              point_type: AI
              unit: "%"
            - point_id: CH_POWER
              point_name: 运行功率
              point_type: AI
              unit: kW
          status:
            - point_id: CH_RUN
              point_name: 运行状态
              point_type: DI
            - point_id: CH_FAULT
              point_name: 故障状态
              point_type: DI
            - point_id: CH_REMOTE
              point_name: 远程/本地
              point_type: DI
          commands:
            - point_id: CH_START
              point_name: 启动命令
              point_type: DO
            - point_id: CH_STOP
              point_name: 停止命令
              point_type: DO
            - point_id: CH_CHWS_SP
              point_name: 冷冻水温度设定
              point_type: AO
              range: [5, 12]
            
        alarms:
          - alarm_id: ALM_CH_FAULT
            alarm_name: 冷机故障
            severity: HIGH
          - alarm_id: ALM_CH_LOW_CHWS
            alarm_name: 冷冻水供水温度低
            trigger: "<5℃"
            severity: MEDIUM
          - alarm_id: ALM_CH_HIGH_CWR
            alarm_name: 冷却水回水温度高
            trigger: ">40℃"
            severity: MEDIUM
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 制冷机房
          floor: B1或B2

      - node_id: HVAC-CHP_DST_BOILER
        node_name: 燃气热水锅炉
        node_name_en: Gas-fired Hot Water Boiler
        node_type: Distribution_Node
        node_subtype: EQP
        node_category: DST
      
        function: 制取采暖/空调热水
        medium_in: GAS-NG + WATER
        medium_out: WATER-HW
      
        multiplicity: multiple
        instance_pattern: HVAC-CHP_DST_BOILER_{Seq}
        typical_quantity: {value: "2-3", unit: "台"}
      
        equipment_parameters:
          type: 燃气真空热水锅炉/常压热水锅炉
          capacity: {value: 2000, unit: kW, note: "单台"}
          efficiency: {value: ">95", unit: "%"}
          fuel: 天然气
        
          operating_parameters:
            hw_supply: {value: 60, unit: ℃}
            hw_return: {value: 50, unit: ℃}
            max_temp: {value: 95, unit: ℃}
          
          safety_devices:
            - 超温保护
            - 超压保护
            - 缺水保护
            - 熄火保护
            - 燃气泄漏保护
          
          control:
            type: 比例调节燃烧器
            turndown_ratio: "10:1"
            staging: 自动加减机
          
        control_points:
          sensors:
            - point_id: BLR_HWS_TEMP
              point_name: 热水供水温度
              point_type: AI
              unit: ℃
            - point_id: BLR_HWR_TEMP
              point_name: 热水回水温度
              point_type: AI
              unit: ℃
            - point_id: BLR_EXHAUST_TEMP
              point_name: 排烟温度
              point_type: AI
              unit: ℃
            - point_id: BLR_LOAD
              point_name: 负荷率
              point_type: AI
              unit: "%"
          status:
            - point_id: BLR_RUN
              point_name: 运行状态
              point_type: DI
            - point_id: BLR_FAULT
              point_name: 故障状态
              point_type: DI
            - point_id: BLR_FLAME
              point_name: 火焰状态
              point_type: DI
          commands:
            - point_id: BLR_START
              point_name: 启动命令
              point_type: DO
            - point_id: BLR_STOP
              point_name: 停止命令
              point_type: DO
            - point_id: BLR_HWS_SP
              point_name: 热水温度设定
              point_type: AO
              range: [40, 80]
            
        alarms:
          - alarm_id: ALM_BLR_FAULT
            alarm_name: 锅炉故障
            severity: HIGH
          - alarm_id: ALM_BLR_HIGH_TEMP
            alarm_name: 超温保护
            trigger: ">95℃"
            severity: CRITICAL
          - alarm_id: ALM_BLR_NO_FLAME
            alarm_name: 熄火报警
            severity: HIGH
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 锅炉房
          floor: 地面层或屋顶

      - node_id: HVAC-CHP_DST_COOLING_TOWER
        node_name: 冷却塔
        node_name_en: Cooling Tower
        node_type: Distribution_Node
        node_subtype: EQP
        node_category: DST
      
        function: 冷却水散热
        medium_in: WATER-CW + AIR
        medium_out: WATER-CW
      
        multiplicity: multiple
        instance_pattern: HVAC-CHP_DST_CT_{Seq}
      
        equipment_parameters:
          type: 横流式/逆流式冷却塔
          capacity: {value: 2500, unit: kW, note: "单台散热量"}
          quantity: 与冷机匹配（N+1）
        
          design_conditions:
            wet_bulb: {value: 28, unit: ℃}
            approach: {value: 4, unit: ℃}
            cw_inlet: {value: 37, unit: ℃}
            cw_outlet: {value: 32, unit: ℃}
          
          fan:
            type: 变频风机
            power: {value: 22, unit: kW}
            control: 根据冷却水温度调速
          
          water_treatment:
            - 自动加药
            - 排污
            - 补水
          
        control_points:
          sensors:
            - point_id: CT_CWS_TEMP
              point_name: 冷却水出塔温度
              point_type: AI
              unit: ℃
            - point_id: CT_CWR_TEMP
              point_name: 冷却水进塔温度
              point_type: AI
              unit: ℃
            - point_id: CT_FAN_SPEED
              point_name: 风机转速
              point_type: AI
              unit: Hz
          status:
            - point_id: CT_FAN_RUN
              point_name: 风机运行
              point_type: DI
          commands:
            - point_id: CT_FAN_START
              point_name: 风机启动
              point_type: DO
            - point_id: CT_FAN_SPEED_SP
              point_name: 风机转速设定
              point_type: AO
      
        location_hint:
          space_type: ROOF
          position: 屋顶

      - node_id: HVAC-CHP_DST_CHWP
        node_name: 冷冻水泵
        node_name_en: Chilled Water Pump
        node_type: Distribution_Node
        node_subtype: PMP
        node_category: DST
      
        function: 输送冷冻水
        medium_in: WATER-CHW
        medium_out: WATER-CHW
      
        multiplicity: multiple
        instance_pattern: HVAC-CHP_DST_CHWP_{Seq}
      
        equipment_parameters:
          type: 卧式离心泵
          configuration:
            primary: 一次泵（对应冷机）
            secondary: 二次泵（变频，可选）
          flow: {value: 400, unit: "m³/h", note: "单台"}
          head: {value: 32, unit: m}
          motor:
            power: {value: 55, unit: kW}
            control: 变频调速
          
        control_points:
          sensors:
            - point_id: CHWP_FLOW
              point_name: 冷冻水流量
              point_type: AI
              unit: "m³/h"
            - point_id: CHWP_DP
              point_name: 供回水压差
              point_type: AI
              unit: kPa
            - point_id: CHWP_SPEED
              point_name: 泵转速
              point_type: AI
              unit: Hz
            - point_id: CHWP_CURRENT
              point_name: 运行电流
              point_type: AI
              unit: A
          status:
            - point_id: CHWP_RUN
              point_name: 运行状态
              point_type: DI
            - point_id: CHWP_FAULT
              point_name: 故障状态
              point_type: DI
          commands:
            - point_id: CHWP_START
              point_name: 启动命令
              point_type: DO
            - point_id: CHWP_SPEED_SP
              point_name: 转速设定
              point_type: AO
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 制冷机房

      - node_id: HVAC-CHP_DST_HWP
        node_name: 热水循环泵
        node_name_en: Hot Water Pump
        node_type: Distribution_Node
        node_subtype: PMP
        node_category: DST
      
        function: 输送采暖热水
        medium_in: WATER-HW
        medium_out: WATER-HW
      
        multiplicity: multiple
        instance_pattern: HVAC-CHP_DST_HWP_{Seq}
      
        equipment_parameters:
          type: 卧式离心泵
          flow: {value: 200, unit: "m³/h"}
          head: {value: 28, unit: m}
          motor:
            power: {value: 30, unit: kW}
            control: 变频调速
          
        control_points:
          sensors:
            - point_id: HWP_FLOW
              point_name: 热水流量
              point_type: AI
              unit: "m³/h"
            - point_id: HWP_SPEED
              point_name: 泵转速
              point_type: AI
              unit: Hz
          status:
            - point_id: HWP_RUN
              point_name: 运行状态
              point_type: DI
            - point_id: HWP_FAULT
              point_name: 故障状态
              point_type: DI
          commands:
            - point_id: HWP_START
              point_name: 启动命令
              point_type: DO
            - point_id: HWP_SPEED_SP
              point_name: 转速设定
              point_type: AO
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 锅炉房

      - node_id: HVAC-CHP_DST_CWP
        node_name: 冷却水泵
        node_name_en: Condenser Water Pump
        node_type: Distribution_Node
        node_subtype: PMP
        node_category: DST
      
        function: 输送冷却水
        medium_in: WATER-CW
        medium_out: WATER-CW
      
        multiplicity: multiple
        instance_pattern: HVAC-CHP_DST_CWP_{Seq}
      
        equipment_parameters:
          type: 卧式离心泵
          flow: {value: 500, unit: "m³/h"}
          head: {value: 28, unit: m}
          motor:
            power: {value: 55, unit: kW}
            control: 变频调速（可选）
          
        control_points:
          sensors:
            - point_id: CWP_FLOW
              point_name: 冷却水流量
              point_type: AI
              unit: "m³/h"
          status:
            - point_id: CWP_RUN
              point_name: 运行状态
              point_type: DI
            - point_id: CWP_FAULT
              point_name: 故障状态
              point_type: DI
          commands:
            - point_id: CWP_START
              point_name: 启动命令
              point_type: DO
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 制冷机房

      - node_id: HVAC-CHP_DST_HEADER
        node_name: 分水器/集水器
        node_name_en: Header
        node_type: Distribution_Node
        node_subtype: PIP
        node_category: DST
      
        function: 冷热水分配和汇集
        medium_in: WATER-CHW/HW
        medium_out: WATER-CHW/HW
      
        equipment_parameters:
          types:
            chw_supply_header:
              name: 冷冻水分水器
              size: DN400
              outlets: 6-8路
            chw_return_header:
              name: 冷冻水集水器
              size: DN400
              inlets: 6-8路
            hw_supply_header:
              name: 热水分水器
              size: DN250
              outlets: 4-6路
            hw_return_header:
              name: 热水集水器
              size: DN250
              inlets: 4-6路
          accessories:
            - 压力表
            - 温度计
            - 排气阀
            - 排污阀
          
        control_points:
          sensors:
            - point_id: HDR_CHW_SUPPLY_TEMP
              point_name: 冷冻水分水器温度
              point_type: AI
              unit: ℃
            - point_id: HDR_CHW_RETURN_TEMP
              point_name: 冷冻水集水器温度
              point_type: AI
              unit: ℃
            - point_id: HDR_HW_SUPPLY_TEMP
              point_name: 热水分水器温度
              point_type: AI
              unit: ℃
            - point_id: HDR_SUPPLY_PRESSURE
              point_name: 供水压力
              point_type: AI
              unit: kPa
            - point_id: HDR_RETURN_PRESSURE
              point_name: 回水压力
              point_type: AI
              unit: kPa
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 制冷机房/锅炉房

    sink_nodes:
  
      - node_id: HVAC-CHP_SNK_CHW_SUPPLY
        node_name: 冷冻水供应端
        node_name_en: Chilled Water Supply Terminal
        node_type: Sink_Node
        node_category: SNK
      
        function: 向空调末端供应冷冻水
        medium_in: WATER-CHW
        medium_out: WATER-CHW
      
        is_boundary_output: true
      
        equipment_parameters:
          supply_to:
            - HVAC-AHU: 空调机组
            - HVAC-FCU: 风机盘管
            - MED-OR: 手术室空调
            - MED-ICU: ICU空调
          parameters:
            temp: {value: 7, unit: ℃}
            pressure: {value: 400, unit: kPa}
          
        location_hint:
          space_type: 管井
          position: 各楼层

      - node_id: HVAC-CHP_SNK_HW_SUPPLY
        node_name: 热水供应端
        node_name_en: Hot Water Supply Terminal
        node_type: Sink_Node
        node_category: SNK
      
        function: 向空调末端供应热水
        medium_in: WATER-HW
        medium_out: WATER-HW
      
        is_boundary_output: true
      
        equipment_parameters:
          supply_to:
            - HVAC-AHU: 空调机组
            - HVAC-FCU: 风机盘管
            - MED-OR: 手术室空调
          parameters:
            temp: {value: 60, unit: ℃}
            pressure: {value: 300, unit: kPa}
          
        location_hint:
          space_type: 管井

  # ========================================
  # EDGES SECTION - 边/连接定义
  # ========================================
  edges:

    chiller_loop:
      - edge_id: HVAC-CHP_EDGE_001
        edge_name: 冷机至冷冻水泵
        edge_type: PIP
        from_node: HVAC-CHP_DST_CHILLER
        to_node: HVAC-CHP_DST_CHWP
        direction: unidirectional
        medium: WATER-CHW
        pipe_parameters:
          material: 焊接钢管
          insulation: 橡塑保温
          size: DN200
        
      - edge_id: HVAC-CHP_EDGE_002
        edge_name: 冷冻水泵至分水器
        edge_type: PIP
        from_node: HVAC-CHP_DST_CHWP
        to_node: HVAC-CHP_DST_HEADER
        direction: unidirectional
        medium: WATER-CHW
      
      - edge_id: HVAC-CHP_EDGE_003
        edge_name: 分水器至末端
        edge_type: PIP
        from_node: HVAC-CHP_DST_HEADER
        to_node: HVAC-CHP_SNK_CHW_SUPPLY
        direction: unidirectional
        medium: WATER-CHW

    cooling_water_loop:
      - edge_id: HVAC-CHP_EDGE_011
        edge_name: 冷却塔至冷却水泵
        edge_type: PIP
        from_node: HVAC-CHP_DST_COOLING_TOWER
        to_node: HVAC-CHP_DST_CWP
        direction: unidirectional
        medium: WATER-CW
      
      - edge_id: HVAC-CHP_EDGE_012
        edge_name: 冷却水泵至冷机
        edge_type: PIP
        from_node: HVAC-CHP_DST_CWP
        to_node: HVAC-CHP_DST_CHILLER
        direction: unidirectional
        medium: WATER-CW
      
      - edge_id: HVAC-CHP_EDGE_013
        edge_name: 冷机至冷却塔
        edge_type: PIP
        from_node: HVAC-CHP_DST_CHILLER
        to_node: HVAC-CHP_DST_COOLING_TOWER
        direction: unidirectional
        medium: WATER-CW

    heating_loop:
      - edge_id: HVAC-CHP_EDGE_021
        edge_name: 锅炉至热水泵
        edge_type: PIP
        from_node: HVAC-CHP_DST_BOILER
        to_node: HVAC-CHP_DST_HWP
        direction: unidirectional
        medium: WATER-HW
      
      - edge_id: HVAC-CHP_EDGE_022
        edge_name: 热水泵至分水器
        edge_type: PIP
        from_node: HVAC-CHP_DST_HWP
        to_node: HVAC-CHP_DST_HEADER
        direction: unidirectional
        medium: WATER-HW
      
      - edge_id: HVAC-CHP_EDGE_023
        edge_name: 分水器至末端
        edge_type: PIP
        from_node: HVAC-CHP_DST_HEADER
        to_node: HVAC-CHP_SNK_HW_SUPPLY
        direction: unidirectional
        medium: WATER-HW

  # ========================================
  # TYPICAL PATHS SECTION
  # ========================================
  typical_paths:

    - path_id: HVAC-CHP_PATH_COOLING
      path_name: 冷冻水供应路径
      path_type: HVAC
      description: 从冷机到末端的冷冻水供应
      sequence:
        - step: 1
          node: HVAC-CHP_DST_CHILLER
          action: 制取7℃冷冻水
        - step: 2
          node: HVAC-CHP_DST_CHWP
          action: 加压输送
        - step: 3
          node: HVAC-CHP_DST_HEADER
          action: 分配至各路
        - step: 4
          node: HVAC-CHP_SNK_CHW_SUPPLY
          action: 供应至末端

    - path_id: HVAC-CHP_PATH_CONDENSER
      path_name: 冷却水循环路径
      path_type: HVAC
      description: 冷却塔与冷机之间的冷却水循环
      sequence:
        - step: 1
          node: HVAC-CHP_DST_COOLING_TOWER
          action: 冷却水散热降温至32℃
        - step: 2
          node: HVAC-CHP_DST_CWP
          action: 加压输送至冷机
        - step: 3
          node: HVAC-CHP_DST_CHILLER
          action: 冷机冷凝器吸热，升温至37℃
        - step: 4
          node: HVAC-CHP_DST_COOLING_TOWER
          action: 回冷却塔散热

    - path_id: HVAC-CHP_PATH_HEATING
      path_name: 热水供应路径
      path_type: HVAC
      description: 从锅炉到末端的热水供应
      sequence:
        - step: 1
          node: HVAC-CHP_SRC_GAS
          action: 燃气供应
        - step: 2
          node: HVAC-CHP_DST_BOILER
          action: 燃烧制取60℃热水
        - step: 3
          node: HVAC-CHP_DST_HWP
          action: 加压输送
        - step: 4
          node: HVAC-CHP_DST_HEADER
          action: 分配至各路
        - step: 5
          node: HVAC-CHP_SNK_HW_SUPPLY
          action: 供应至末端

  # ========================================
  # CONTROL LOGIC SECTION
  # ========================================
  control_logic:

    chiller_staging:
      name: 冷机群控
      description: 多台冷机的优化运行
    
      staging_logic:
        load_based:
          description: 根据系统负荷加减机
          parameters:
            - chw_return_temp: 回水温度
            - chw_flow: 系统流量
            - calculated_load: 计算负荷
          thresholds:
            add_chiller: 当前冷机负荷>85%
            remove_chiller: 当前冷机负荷<50%
          
        sequence:
          add:
            - 确认待启冷机就绪
            - 提前5分钟启动冷却水泵和冷却塔
            - 启动冷机
            - 确认运行稳定后，负荷分配
          remove:
            - 逐步减少待停冷机负荷
            - 负荷降至20%以下，停止冷机
            - 延时5分钟后停止对应冷却水泵
          
        optimization:
          method: 运行效率优化
          principle: 优先运行高效率冷机
          consider:
            - 各机组COP实时值
            - 累计运行时间均衡
            - 维护周期
          
    chw_temperature_control:
      name: 冷冻水温度控制
      description: 控制冷冻水供水温度
    
      setpoint:
        design: {value: 7, unit: ℃}
        range: {value: "5-12", unit: ℃}
        reset: 根据室外温度重置
      
      reset_logic:
        name: 供水温度重置
        description: 低负荷时提高供水温度节能
        conditions:
          outdoor_temp: "<25℃"
          system_load: "<60%"
        reset_range:
          min: {value: 7, unit: ℃}
          max: {value: 10, unit: ℃}
        benefit: 提高冷机COP
      
    pump_control:
      name: 水泵变频控制
      description: 变流量系统的水泵控制
    
      primary_pump:
        method: 一一对应冷机
        control: 定频或变频
        note: 一次泵变流量系统
      
      secondary_pump:
        method: 压差控制
        setpoint: 最不利环路压差
        control: 变频调速
      
      differential_pressure:
        sensor_location: 最不利环路
        setpoint: {value: 50, unit: kPa}
        range: {value: "30-80", unit: kPa}
        reset: 根据阀门开度重置
      
    boiler_staging:
      name: 锅炉群控
      description: 多台锅炉的优化运行
    
      staging_logic:
        add_boiler: 当前锅炉负荷>85%
        remove_boiler: 当前锅炉负荷<40%
      
      modulation:
        method: 比例燃烧控制
        range: "10%-100%"
      
    seasonal_changeover:
      name: 季节切换
      description: 供冷/供热模式切换
    
      criteria:
        cooling_start:
          outdoor_temp: ">18℃连续3天"
          calendar: 约4月中旬
        heating_start:
          outdoor_temp: "<12℃连续3天"
          calendar: 约11月中旬
        
      transition_period:
        duration: 2周
        mode: 可同时供冷/供热（分区）
      
    backup_source:
      name: 备用冷热源控制
      description: 关键区域独立冷热源
    
      trigger:
        primary_fault: 主系统故障
        low_capacity: 主系统容量不足
      
      backup_areas:
        - MED-OR: 手术室
        - MED-ICU: ICU
      
      backup_equipment:
        type: 独立风冷冷热水机组
        capacity: {value: 200, unit: kW}
        startup_time: {value: 5, unit: min}

  # ========================================
  # ALARM & PROTECTION
  # ========================================
  alarm_protection:
  
    chiller_alarms:
      - alarm_id: ALM_CH_FAULT
        alarm_name: 冷机故障
        severity: HIGH
        action: 自动切换备用冷机
      
      - alarm_id: ALM_CH_ALL_FAULT
        alarm_name: 所有冷机故障
        severity: CRITICAL
        action: 启动备用冷源，通知维修
      
      - alarm_id: ALM_CH_LOW_FLOW
        alarm_name: 冷冻水流量低
        severity: HIGH
        trigger: 流量<最小保护流量
        action: 停机保护
      
    boiler_alarms:
      - alarm_id: ALM_BLR_FAULT
        alarm_name: 锅炉故障
        severity: HIGH
      
      - alarm_id: ALM_BLR_GAS_LEAK
        alarm_name: 燃气泄漏
        severity: CRITICAL
        action: 切断燃气，启动通风
      
    system_alarms:
      - alarm_id: ALM_LOW_CHW_PRESSURE
        alarm_name: 冷冻水压力低
        severity: MEDIUM
        trigger: 系统压力<150kPa
        action: 检查补水系统
      
      - alarm_id: ALM_HIGH_CHW_TEMP
        alarm_name: 冷冻水供水温度高
        severity: MEDIUM
        trigger: 供水温度>12℃
        action: 检查冷机负荷

  # ========================================
  # DEPENDENCIES
  # ========================================
  dependencies:
  
    upstream_dependencies:
      - dependency_id: DEP_CHP_POWER
        from_system: ELEC-LV-MAIN
        dependency_type: POWER_SUPPLY
        criticality: CRITICAL
        backup: 发电机供电
      
      - dependency_id: DEP_CHP_GAS
        from_system: 市政燃气
        dependency_type: FUEL_SUPPLY
        criticality: HIGH
        backup: 储罐（可选）
      
      - dependency_id: DEP_CHP_WATER
        from_system: PLUMB-DWS
        dependency_type: WATER_SUPPLY
        criticality: MEDIUM
      
    downstream_dependencies:
      - dependency_id: DEP_TO_AHU
        to_system: HVAC-AHU
        dependency_type: COOLING_HEATING
        criticality: HIGH
      
      - dependency_id: DEP_TO_FCU
        to_system: HVAC-FCU
        dependency_type: COOLING_HEATING
        criticality: MEDIUM
      
      - dependency_id: DEP_TO_OR
        to_system: MED-OR
        dependency_type: COOLING_HEATING
        criticality: CRITICAL
        backup: 独立备用冷源
```

---

## 系统 5.2: HVAC-AHU 空调机组系统

```yaml
System_Topology:

  identity:
    system_id: HVAC-AHU
    system_name: 空调机组系统
    system_name_en: Air Handling Unit System
    system_category: HVAC
    system_type: 暖通-空调机组
    priority_level: P2-BUSINESS_CRITICAL
  
    description: |
      医院集中式空调机组系统，服务于门诊大厅、候诊区、医技区等公共区域。
      系统包括新风处理机组、组合式空调机组、全热交换器等。
      提供过滤、加热、冷却、加湿、除湿等空气处理功能。
      与BA系统联网，实现温湿度自动控制和节能运行。
    
    design_basis:
      fresh_air: {value: "≥30", unit: "m³/h/人", note: "医疗建筑标准"}
      filtration:
        general: G4+F7
        medical: G4+F8+H13
      temperature:
        summer: {value: "24-26", unit: ℃}
        winter: {value: "20-24", unit: ℃}
      humidity: {value: "40-60", unit: "%RH"}
      noise: {value: "≤45", unit: "dB(A)"}
  
    parent_system: HVAC-CHP
  
    design_standards:
      - GB 50736-2012 民用建筑供暖通风与空气调节设计规范
      - GB 51039-2014 综合医院建筑设计规范
      - GB 50189-2015 公共建筑节能设计标准
  
    version: 1.0
    last_updated: 2024

  boundary:
    inputs:
      - boundary_id: HVAC-AHU_IN_001
        name: 冷冻水
        from_system: HVAC-CHP
        medium: WATER-CHW
      
      - boundary_id: HVAC-AHU_IN_002
        name: 热水
        from_system: HVAC-CHP
        medium: WATER-HW
      
      - boundary_id: HVAC-AHU_IN_003
        name: 电力
        from_system: ELEC-LV
        medium: ELEC-LV
      
      - boundary_id: HVAC-AHU_IN_004
        name: 室外新风
        from_system: ATMOSPHERE
        medium: AIR-OA
      
      - boundary_id: HVAC-AHU_IN_005
        name: 控制信号
        from_system: INT-BA
        medium: SIGNAL-BMS
      
    outputs:
      - boundary_id: HVAC-AHU_OUT_001
        name: 送风
        to_system: 室内空间
        medium: AIR-SA
      
      - boundary_id: HVAC-AHU_OUT_002
        name: 排风
        to_system: ATMOSPHERE
        medium: AIR-EA
      
      - boundary_id: HVAC-AHU_OUT_003
        name: 状态反馈
        to_system: INT-BA
        medium: SIGNAL-BMS

  nodes:

    source_nodes:
  
      - node_id: HVAC-AHU_SRC_OUTDOOR_AIR
        node_name: 室外新风
        node_name_en: Outdoor Air
        node_type: Source_Node
        node_category: SRC
      
        function: 提供新鲜空气
        medium_in: AIR-OA
        medium_out: AIR-OA
      
        is_boundary_input: true
      
        equipment_parameters:
          intake:
            type: 新风百叶
            location: 室外墙面/屋顶
            height: {value: ">3", unit: m, note: "高于地面"}
          protection:
            - 防雨百叶
            - 防虫网
            - 防鸟网
          distance:
            from_exhaust: {value: ">10", unit: m}
            from_cooling_tower: {value: ">15", unit: m}
          
        location_hint:
          space_type: 室外
          position: 建筑外墙

      - node_id: HVAC-AHU_SRC_CHW
        node_name: 冷冻水供应
        node_name_en: Chilled Water Supply
        node_type: Source_Node
        node_category: SRC
      
        function: 为空调机组提供冷源
        medium_in: WATER-CHW
        medium_out: WATER-CHW
      
        is_boundary_input: true
      
        equipment_parameters:
          from: HVAC-CHP分水器
          temp: {value: 7, unit: ℃}
        
        location_hint:
          space_type: 管井

      - node_id: HVAC-AHU_SRC_HW
        node_name: 热水供应
        node_name_en: Hot Water Supply
        node_type: Source_Node
        node_category: SRC
      
        function: 为空调机组提供热源
        medium_in: WATER-HW
        medium_out: WATER-HW
      
        is_boundary_input: true
      
        equipment_parameters:
          from: HVAC-CHP分水器
          temp: {value: 60, unit: ℃}
        
        location_hint:
          space_type: 管井

    distribution_nodes:
  
      - node_id: HVAC-AHU_DST_AHU
        node_name: 组合式空调机组
        node_name_en: Air Handling Unit
        node_type: Distribution_Node
        node_subtype: AHU
        node_category: DST
      
        function: 空气处理与输送
        medium_in: AIR-OA + AIR-RA + WATER-CHW/HW
        medium_out: AIR-SA
      
        multiplicity: multiple
        instance_pattern: HVAC-AHU_DST_AHU_{Zone}_{Seq}
        typical_quantity: {value: "20-50", unit: "台", note: "大型医院"}
      
        equipment_parameters:
          type: 组合式空调机组
          configurations:
            full_ahu:
              name: 全功能空调箱
              sections:
                - 新风段
                - 回风段
                - 混合段
                - 初效过滤段（G4）
                - 表冷段
                - 加热段
                - 加湿段
                - 中效过滤段（F7/F8）
                - 送风段
                - 消声段
              application: 门诊、医技、公共区
            mau:
              name: 新风处理机组
              sections:
                - 新风段
                - 初效过滤
                - 表冷/加热
                - 加湿
                - 中效过滤
                - 送风
              application: 新风预处理
        
          capacity_range:
            small: {value: "2000-5000", unit: "m³/h"}
            medium: {value: "5000-15000", unit: "m³/h"}
            large: {value: "15000-50000", unit: "m³/h"}
          
          fans:
            supply_fan:
              type: 离心风机/插入式风机
              motor: 变频调速
              efficiency: {value: ">75", unit: "%"}
            return_fan:
              type: 离心风机
              motor: 变频调速
              note: 大系统配置
            
          coils:
            cooling_coil:
              type: 铜管铝翅片
              rows: "4-8排"
              face_velocity: {value: "2.0-2.5", unit: "m/s"}
            heating_coil:
              type: 铜管铝翅片
              rows: "2-4排"
            
          humidifier:
            type: 干蒸汽加湿器
            capacity: 根据需求配置
          
        control_points:
          sensors:
            - point_id: AHU_SA_TEMP
              point_name: 送风温度
              point_type: AI
              unit: ℃
            - point_id: AHU_RA_TEMP
              point_name: 回风温度
              point_type: AI
              unit: ℃
            - point_id: AHU_OA_TEMP
              point_name: 新风温度
              point_type: AI
              unit: ℃
            - point_id: AHU_SA_RH
              point_name: 送风湿度
              point_type: AI
              unit: "%RH"
            - point_id: AHU_RA_RH
              point_name: 回风湿度
              point_type: AI
              unit: "%RH"
            - point_id: AHU_FILTER_DP_1
              point_name: 初效过滤器压差
              point_type: AI
              unit: Pa
            - point_id: AHU_FILTER_DP_2
              point_name: 中效过滤器压差
              point_type: AI
              unit: Pa
            - point_id: AHU_FAN_SPEED
              point_name: 风机转速
              point_type: AI
              unit: Hz
            - point_id: AHU_CHW_VALVE
              point_name: 冷水阀开度
              point_type: AI
              unit: "%"
            - point_id: AHU_HW_VALVE
              point_name: 热水阀开度
              point_type: AI
              unit: "%"
          status:
            - point_id: AHU_RUN
              point_name: 运行状态
              point_type: DI
            - point_id: AHU_FAULT
              point_name: 故障状态
              point_type: DI
            - point_id: AHU_FILTER_ALARM
              point_name: 过滤器报警
              point_type: DI
          commands:
            - point_id: AHU_START
              point_name: 启动命令
              point_type: DO
            - point_id: AHU_STOP
              point_name: 停止命令
              point_type: DO
            - point_id: AHU_SA_TEMP_SP
              point_name: 送风温度设定
              point_type: AO
              range: [12, 28]
            - point_id: AHU_FAN_SPEED_SP
              point_name: 风机转速设定
              point_type: AO
              range: [20, 50]
            - point_id: AHU_CHW_VALVE_SP
              point_name: 冷水阀开度设定
              point_type: AO
              range: [0, 100]
            - point_id: AHU_HW_VALVE_SP
              point_name: 热水阀开度设定
              point_type: AO
              range: [0, 100]
            - point_id: AHU_OA_DAMPER
              point_name: 新风阀开度
              point_type: AO
              range: [0, 100]
            
        alarms:
          - alarm_id: ALM_AHU_FAULT
            alarm_name: 机组故障
            severity: MEDIUM
          - alarm_id: ALM_AHU_FILTER
            alarm_name: 过滤器堵塞
            trigger: 压差>150Pa（初效）或>250Pa（中效）
            severity: LOW
          - alarm_id: ALM_AHU_LOW_TEMP
            alarm_name: 送风温度过低
            trigger: "<12℃"
            severity: MEDIUM
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 空调机房
          floor: 各楼层/设备层

      - node_id: HVAC-AHU_DST_HRU
        node_name: 全热交换器
        node_name_en: Heat Recovery Unit
        node_type: Distribution_Node
        node_subtype: AHU
        node_category: DST
      
        function: 新风排风热回收
        medium_in: AIR-OA + AIR-EA
        medium_out: AIR-FA + AIR-EA
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 转轮式/板式全热交换器
          efficiency:
            sensible: {value: ">70", unit: "%"}
            total: {value: ">60", unit: "%"}
          capacity: {value: "1000-10000", unit: "m³/h"}
        
          bypass:
            purpose: 过渡季节不需热回收时旁通
            control: 自动旁通阀
          
        control_points:
          sensors:
            - point_id: HRU_OA_TEMP
              point_name: 新风温度
              point_type: AI
              unit: ℃
            - point_id: HRU_SA_TEMP
              point_name: 送风温度
              point_type: AI
              unit: ℃
            - point_id: HRU_EA_TEMP
              point_name: 排风温度
              point_type: AI
              unit: ℃
          status:
            - point_id: HRU_RUN
              point_name: 运行状态
              point_type: DI
          commands:
            - point_id: HRU_START
              point_name: 启动命令
              point_type: DO
            - point_id: HRU_BYPASS
              point_name: 旁通控制
              point_type: DO
      
        location_hint:
          space_type: MEP_ROOM
          note: 与AHU配合使用

      - node_id: HVAC-AHU_DST_VAV_BOX
        node_name: 变风量末端
        node_name_en: VAV Box
        node_type: Distribution_Node
        node_subtype: TRM
        node_category: DST
      
        function: 变风量区域控制
        medium_in: AIR-SA
        medium_out: AIR-SA
      
        multiplicity: multiple
        instance_pattern: HVAC-AHU_DST_VAV_{Zone}
      
        equipment_parameters:
          types:
            single_duct:
              name: 单风道VAV箱
              application: 一般区域
            fan_powered:
              name: 风机驱动VAV箱
              application: 高负荷区域
            dual_duct:
              name: 双风道VAV箱
              application: 精密控制区域
          size: {value: "DN150-DN400", unit: mm}
        
          control:
            method: 压力无关型VAV
            actuator: 电动调节阀
            reheat: 热水再热盘管（可选）
          
        control_points:
          sensors:
            - point_id: VAV_FLOW
              point_name: 风量
              point_type: AI
              unit: "m³/h"
            - point_id: VAV_ZONE_TEMP
              point_name: 区域温度
              point_type: AI
              unit: ℃
          commands:
            - point_id: VAV_DAMPER
              point_name: 风阀开度
              point_type: AO
              range: [0, 100]
            - point_id: VAV_TEMP_SP
              point_name: 区域温度设定
              point_type: AO
      
        location_hint:
          space_type: 吊顶上方
          position: 各区域

      - node_id: HVAC-AHU_DST_DIFFUSER
        node_name: 送风口
        node_name_en: Supply Air Diffuser
        node_type: Distribution_Node
        node_subtype: TRM
        node_category: DST
      
        function: 送风末端分配
        medium_in: AIR-SA
        medium_out: AIR-SA
      
        multiplicity: multiple
      
        equipment_parameters:
          types:
            square_diffuser:
              name: 方形散流器
              size: {value: "300×300 - 600×600", unit: mm}
              application: 一般房间
            slot_diffuser:
              name: 条缝风口
              application: 大空间/走廊
            swirl_diffuser:
              name: 旋流风口
              application: 高空间
            laminar_diffuser:
              name: 层流送风口
              application: 洁净区域
          material: 铝合金/钢板喷塑
        
        location_hint:
          space_type: 吊顶
          pattern: 均匀布置

    sink_nodes:
  
      - node_id: HVAC-AHU_SNK_ROOM
        node_name: 空调房间
        node_name_en: Conditioned Space
        node_type: Sink_Node
        node_category: SNK
      
        function: 接收空调送风
        medium_in: AIR-SA
        medium_out: CONDITIONED_ENVIRONMENT
      
        is_boundary_output: true
      
        equipment_parameters:
          areas:
            outpatient_lobby:
              name: 门诊大厅
              area: {value: 2000, unit: "m²"}
              ahu_capacity: {value: 30000, unit: "m³/h"}
            waiting_area:
              name: 候诊区
              area: {value: 500, unit: "m²"}
              ahu_capacity: {value: 8000, unit: "m³/h"}
            pharmacy:
              name: 药房
              area: {value: 300, unit: "m²"}
              special: 恒温恒湿
            radiology:
              name: 放射科
              area: {value: 400, unit: "m²"}
              special: 设备散热
            laboratory:
              name: 检验科
              area: {value: 500, unit: "m²"}
              special: 通风换气
            
        environment_requirements:
          temperature:
            summer: {value: "24-26", unit: ℃}
            winter: {value: "20-24", unit: ℃}
          humidity: {value: "40-60", unit: "%RH"}
          fresh_air: {value: "≥30", unit: "m³/h/人"}
        
        location_hint:
          space_type: 空调区域

      - node_id: HVAC-AHU_SNK_EXHAUST
        node_name: 排风出口
        node_name_en: Exhaust Outlet
        node_type: Sink_Node
        node_category: SNK
      
        function: 排出室内废气
        medium_in: AIR-EA
        medium_out: AIR-EA
      
        is_boundary_output: true
      
        equipment_parameters:
          type: 排风百叶/风帽
          location: 屋顶/外墙
        
        location_hint:
          space_type: 室外

  edges:

    air_flow_edges:
      - edge_id: HVAC-AHU_EDGE_001
        edge_name: 新风至AHU
        edge_type: DUC
        from_node: HVAC-AHU_SRC_OUTDOOR_AIR
        to_node: HVAC-AHU_DST_AHU
        direction: unidirectional
        medium: AIR-OA
        duct_parameters:
          material: 镀锌钢板
          insulation: 保温棉
        
      - edge_id: HVAC-AHU_EDGE_002
        edge_name: AHU至VAV
        edge_type: DUC
        from_node: HVAC-AHU_DST_AHU
        to_node: HVAC-AHU_DST_VAV_BOX
        direction: unidirectional
        medium: AIR-SA
      
      - edge_id: HVAC-AHU_EDGE_003
        edge_name: VAV至送风口
        edge_type: DUC
        from_node: HVAC-AHU_DST_VAV_BOX
        to_node: HVAC-AHU_DST_DIFFUSER
        direction: unidirectional
        medium: AIR-SA
      
      - edge_id: HVAC-AHU_EDGE_004
        edge_name: 送风口至房间
        edge_type: AIR
        from_node: HVAC-AHU_DST_DIFFUSER
        to_node: HVAC-AHU_SNK_ROOM
        direction: unidirectional
        medium: AIR-SA

    water_flow_edges:
      - edge_id: HVAC-AHU_EDGE_011
        edge_name: 冷水至AHU
        edge_type: PIP
        from_node: HVAC-AHU_SRC_CHW
        to_node: HVAC-AHU_DST_AHU
        direction: bidirectional
        medium: WATER-CHW
      
      - edge_id: HVAC-AHU_EDGE_012
        edge_name: 热水至AHU
        edge_type: PIP
        from_node: HVAC-AHU_SRC_HW
        to_node: HVAC-AHU_DST_AHU
        direction: bidirectional
        medium: WATER-HW

  typical_paths:

    - path_id: HVAC-AHU_PATH_SUPPLY
      path_name: 空调送风路径
      path_type: HVAC
      description: 从室外到室内的送风路径
      sequence:
        - step: 1
          node: HVAC-AHU_SRC_OUTDOOR_AIR
          action: 新风进入
        - step: 2
          node: HVAC-AHU_DST_HRU
          action: 热回收预处理（可选）
        - step: 3
          node: HVAC-AHU_DST_AHU
          action: 过滤、冷却/加热、加湿
        - step: 4
          node: HVAC-AHU_DST_VAV_BOX
          action: 风量调节
        - step: 5
          node: HVAC-AHU_DST_DIFFUSER
          action: 送风分配
        - step: 6
          node: HVAC-AHU_SNK_ROOM
          action: 空调效果

  control_logic:

    supply_air_temp_control:
      name: 送风温度控制
      description: 控制AHU送风温度
    
      summer_mode:
        setpoint: {value: 14, unit: ℃, note: "送风温度"}
        method: 冷水阀调节
        cascade: 回风温度→送风温度
      
      winter_mode:
        setpoint: {value: 28, unit: ℃}
        method: 热水阀调节
      
      reset_logic:
        based_on: 室外温度/负荷
        range: {value: "12-18", unit: ℃}
      
    supply_air_pressure_control:
      name: 送风静压控制
      description: VAV系统的静压控制
    
      setpoint_method: 压力无关型
      sensor_location: 最不利环路
      setpoint: {value: 150, unit: Pa}
      control: 风机变频调速
    
      reset_logic:
        based_on: VAV箱开度反馈
        principle: 至少一个VAV箱开度>90%时维持静压
      
    economizer_control:
      name: 新风节能控制
      description: 过渡季节利用新风免费冷却
    
      enable_conditions:
        outdoor_enthalpy: 低于室内焓值
        outdoor_temp: {value: "12-22", unit: ℃}
      
      mode:
        minimum_oa: 最小新风比（正常模式）
        economizer: 100%新风（节能模式）
      
      control:
        damper: 新风阀0-100%
        interlock: 排风阀联动
      
    humidity_control:
      name: 湿度控制
      description: 加湿/除湿控制
    
      humidification:
        type: 干蒸汽加湿
        setpoint: {value: 40, unit: "%RH"}
        control: PID调节蒸汽阀
      
      dehumidification:
        method: 表冷器除湿
        reheat: 必要时再热
      
    schedule_control:
      name: 时间表控制
      description: 按作息时间运行
    
      weekday:
        start: "06:00"
        stop: "22:00"
        night_setback: 最小风量维持
      
      weekend:
        reduced_capacity: 50%风量
      
      pre_cooling:
        start: 提前30分钟启动
        purpose: 手术/会议前预冷

  alarm_protection:
  
    ahu_alarms:
      - alarm_id: ALM_AHU_FAN_FAULT
        alarm_name: 风机故障
        severity: HIGH
        action: 通知维修
      
      - alarm_id: ALM_AHU_FILTER_DIRTY
        alarm_name: 过滤器脏堵
        severity: LOW
        trigger: 压差超限
        action: 安排更换
      
      - alarm_id: ALM_AHU_FREEZE
        alarm_name: 防冻报警
        severity: HIGH
        trigger: 盘管温度<5℃
        action: 开启热水阀，停止风机
      
      - alarm_id: ALM_AHU_SMOKE
        alarm_name: 风管烟感报警
        severity: CRITICAL
        trigger: 风管烟感动作
        action: 停止AHU，联动消防

  dependencies:
  
    upstream_dependencies:
      - dependency_id: DEP_AHU_CHW
        from_system: HVAC-CHP
        dependency_type: COOLING
        criticality: HIGH
      
      - dependency_id: DEP_AHU_HW
        from_system: HVAC-CHP
        dependency_type: HEATING
        criticality: HIGH
      
      - dependency_id: DEP_AHU_POWER
        from_system: ELEC-LV
        dependency_type: POWER_SUPPLY
        criticality: HIGH
      
    downstream_dependencies:
      - dependency_id: DEP_TO_ROOMS
        to_system: 各功能房间
        dependency_type: CONDITIONED_AIR
        criticality: MEDIUM
```

---

## 系统 5.3: HVAC-FCU 风机盘管系统

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
      配合新

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

# 第五批次修订版：问题修复与补充

## 修订说明

根据您提出的5个低-中等优先级问题，我将逐一进行修复和补充。

---

## 问题1修复：HVAC系统季节切换高级控制策略

```yaml
Seasonal_Control_Advanced:

  identity:
    name: HVAC季节切换高级控制策略
    description: 根据气候区域和医疗特殊需求的季节性控制
    version: 2.0
    last_updated: 2024
    applicable_systems:
      - HVAC-CHP
      - HVAC-AHU
      - HVAC-FCU

  # ========================================
  # 气候区域差异化配置
  # ========================================
  climate_regions:
  
    northern_china:
      name: 北方严寒/寒冷地区
      representative_cities:
        - 哈尔滨
        - 沈阳
        - 北京
        - 石家庄
      heating_degree_days: {value: ">3000", unit: "℃·d"}
    
      schedule:
        cooling_start:
          calendar: "05/01"
          condition: 室外温度>18℃连续5天
        cooling_end:
          calendar: "09/30"
          condition: 室外温度<15℃连续3天
        heating_start:
          calendar: "10/15"
          condition: 室外温度<12℃连续3天
        heating_end:
          calendar: "04/15"
          condition: 室外温度>10℃连续5天
        
      characteristics:
        winter_outdoor_temp: {value: "-20~0", unit: ℃}
        heating_duration: {value: "5-6", unit: "月"}
        cooling_duration: {value: "3-4", unit: "月"}
        transition_period: 较短（1-2周）
      
    central_china:
      name: 夏热冬冷地区
      representative_cities:
        - 上海
        - 武汉
        - 南京
        - 杭州
      heating_degree_days: {value: "1500-3000", unit: "℃·d"}
    
      schedule:
        cooling_start:
          calendar: "04/15"
          condition: 室外温度>20℃连续3天
        cooling_end:
          calendar: "10/15"
          condition: 室外温度<18℃连续3天
        heating_start:
          calendar: "11/15"
          condition: 室外温度<8℃连续3天
        heating_end:
          calendar: "03/15"
          condition: 室外温度>12℃连续5天
        
      characteristics:
        winter_outdoor_temp: {value: "0~10", unit: ℃}
        heating_duration: {value: "3-4", unit: "月"}
        cooling_duration: {value: "5-6", unit: "月"}
        transition_period: 较长（3-4周）
        high_humidity: 夏季高湿，除湿需求大
      
    southern_china:
      name: 夏热冬暖地区
      representative_cities:
        - 广州
        - 深圳
        - 海南
        - 福州
      heating_degree_days: {value: "<1500", unit: "℃·d"}
    
      schedule:
        cooling_start:
          calendar: "04/01"
          condition: 室外温度>22℃连续3天
        cooling_end:
          calendar: "11/30"
          condition: 室外温度<20℃连续5天
        heating_start:
          calendar: "12/15"
          condition: 室外温度<10℃连续3天（罕见）
        heating_end:
          calendar: "02/15"
          condition: 室外温度>15℃连续3天
        
      characteristics:
        winter_outdoor_temp: {value: "5~15", unit: ℃}
        heating_duration: {value: "0-2", unit: "月"}
        cooling_duration: {value: "7-9", unit: "月"}
        transition_period: 很短或无
        dehumidification: 全年除湿需求
      
    plateau_region:
      name: 高原地区
      representative_cities:
        - 拉萨
        - 西宁
        - 昆明
      altitude: {value: ">2000", unit: m}
    
      schedule:
        cooling_start:
          calendar: "06/01"
          condition: 室外温度>15℃连续5天
        cooling_end:
          calendar: "09/15"
          condition: 室外温度<12℃连续3天
        heating_start:
          calendar: "09/20"
          condition: 室外温度<10℃连续3天
        heating_end:
          calendar: "05/30"
          condition: 室外温度>12℃连续5天
        
      characteristics:
        diurnal_range: 日温差大（15-20℃）
        solar_radiation: 强
        year_round_heating: 高海拔地区可能全年需要加热
      
  # ========================================
  # 医疗关键区域例外处理
  # ========================================
  medical_areas_exception:
  
    description: 关键医疗区域独立于季节切换，全年保持环境稳定
  
    exempt_areas:
      MED-OR:
        name: 手术室
        year_round_behavior:
          cooling: 全年供冷（设备散热+恒温需求）
          heating: 按需供热（冬季或寒冷时段）
        temperature:
          setpoint: {value: 22, unit: ℃}
          range: {value: "20-26", unit: ℃}
        independent_source:
          type: 独立风冷冷热水机组
          capacity: {value: 200, unit: kW}
          backup_for: 主冷热源故障或季节切换期
        
      MED-ICU:
        name: 重症监护室
        year_round_behavior:
          cooling: 全年供冷（监护设备散热）
          heating: 按需供热
        temperature:
          setpoint: {value: 24, unit: ℃}
          range: {value: "22-26", unit: ℃}
        independent_source:
          shared_with: MED-OR（同一备用冷源）
        
      MED-LAB:
        name: 检验科/实验室
        year_round_behavior:
          cooling: 全年供冷（仪器散热+样本保存）
          heating: 按需
        temperature:
          setpoint: {value: 22, unit: ℃}
          stability: {value: "±1", unit: ℃}
        independent_source:
          type: 精密空调或独立小冷机
        
      PHARMACY:
        name: 药房/药库
        year_round_behavior:
          cooling: 全年供冷（药品恒温）
          heating: 防冻
        temperature:
          setpoint: {value: 20, unit: ℃}
          range: {value: "15-25", unit: ℃}
        
      DATA_CENTER:
        name: 数据中心机房
        year_round_behavior:
          cooling: 全年供冷（IT设备散热）
          heating: 无需
        temperature:
          setpoint: {value: 22, unit: ℃}
          range: {value: "18-27", unit: ℃}
        independent_source:
          type: 精密空调
          redundancy: N+1
        
  # ========================================
  # 过渡季节控制策略
  # ========================================
  transition_period_strategy:
  
    definition:
      duration: {value: "2-4", unit: "周"}
      condition: 室外温度在12-18℃波动
      characteristic: 日间需冷、夜间需热
    
    system_behavior:
      four_pipe_system:
        description: 四管制系统可同时供冷供热
        chw_supply: {value: 7, unit: ℃, status: "持续供应"}
        hw_supply: {value: 50, unit: ℃, status: "持续供应"}
        zone_control: 各区域按需选择冷/热
      
      two_pipe_system:
        description: 两管制系统需要切换
        changeover_frequency: 尽量减少（每周最多1次）
        method: 根据天气预报提前切换
        intermediate: 可仅供应温水（30-35℃）
      
    zone_separation:
      principle: 医疗区与普通区分离控制
    
      medical_zone:
        areas:
          - 手术室区域
          - ICU区域
          - 急诊区域
        supply: 独立冷热源，全年稳定
        changeover: 不参与季节切换
      
      general_zone:
        areas:
          - 门诊
          - 病房
          - 办公
          - 后勤
        supply: 主冷热源
        changeover: 正常季节切换
      
    cost_optimization:
      strategies:
        free_cooling:
          trigger: 室外温度<室内设定-3℃
          method: 增加新风比例，减少机械制冷
          saving: 冷机能耗降低50%+
        
        night_purge:
          trigger: 夜间室外温度<18℃
          method: 夜间开窗或加大新风
          purpose: 预冷建筑蓄冷
        
        chw_reset:
          trigger: 过渡季节低负荷
          method: 提高冷冻水供水温度（7→10℃）
          benefit: 提高冷机COP
        
        hw_reset:
          trigger: 过渡季节低负荷
          method: 降低热水供水温度（60→45℃）
          benefit: 减少锅炉燃气消耗
        
        avoid_simultaneous:
          principle: 避免主管路同时供冷热
          method:
            - 过渡季节关闭一侧
            - 或采用分时供应（日间冷、夜间热）
```

---

## 问题2修复：新风分配系统完整设计

```yaml
Fresh_Air_Distribution_System:

  identity:
    name: FCU房间新风分配系统
    description: 定义新风从MAU到FCU房间的完整分配路径
    version: 1.0
    last_updated: 2024
    applicable_systems:
      - HVAC-AHU（MAU新风机组）
      - HVAC-FCU

  # ========================================
  # 系统架构层级
  # ========================================
  system_architecture:
  
    tier_1_central_processing:
      name: 集中新风处理
      equipment: 新风处理机组（MAU）
      location: 设备层/屋顶/地下室
    
      processing_sequence:
        step_1:
          name: 进气段
          components:
            - 新风百叶
            - 防雨罩
            - 防虫网
        step_2:
          name: 初效过滤
          filter: G4
          pressure_drop: {value: "50-100", unit: Pa}
        step_3:
          name: 热回收（可选）
          type: 全热交换器
          efficiency: {value: ">60", unit: "%"}
        step_4:
          name: 表冷/加热
          coil: 冷热盘管
          output_temp:
            summer: {value: 16, unit: ℃}
            winter: {value: 28, unit: ℃}
        step_5:
          name: 加湿（冬季）
          type: 干蒸汽加湿
          target: {value: 40, unit: "%RH"}
        step_6:
          name: 中效过滤
          filter: F7/F8
          pressure_drop: {value: "100-150", unit: Pa}
        step_7:
          name: 送风段
          fan: 离心风机（变频）
        
      output_parameters:
        temperature:
          summer: {value: 18, unit: ℃}
          winter: {value: 24, unit: ℃}
          transition: {value: 22, unit: ℃}
        humidity: {value: "45-55", unit: "%RH"}
        filtration: F7/F8
      
    tier_2_main_distribution:
      name: 主新风管网
      description: 从MAU到各楼层的主干管
    
      duct_parameters:
        material: 镀锌钢板
        thickness: {value: "0.75-1.2", unit: mm}
        insulation:
          material: 橡塑保温
          thickness: {value: 20, unit: mm}
          purpose: 防冷凝
        fire_damper:
          location: 穿越防火分区处
          rating: 70℃易熔片
        
      main_riser:
        description: 新风竖井/立管
        size: 根据服务楼层风量计算
        velocity: {value: "6-8", unit: "m/s"}
        location: 管井内
      
      floor_branch:
        description: 楼层水平主管
        size: 根据楼层风量计算
        velocity: {value: "5-7", unit: "m/s"}
        routing: 走廊吊顶上方
      
    tier_3_floor_header:
      name: 楼层新风分集器
      description: 楼层新风分配中心
    
      equipment:
        header_box:
          name: 新风分配箱
          material: 镀锌钢板
          size: 根据楼层风量
          location: 管井或走廊吊顶
        
        components:
          total_damper:
            name: 楼层总风阀
            type: 电动调节阀
            control: BA联动
          branch_dampers:
            name: 分支调节阀
            type: 手动/电动
            quantity: 每个房间支路一个
          measuring_station:
            name: 风量测量装置
            type: 皮托管阵列/文丘里
            purpose: 调试平衡
          
      control_points:
        sensors:
          - point_id: FH_FA_FLOW
            point_name: 楼层新风总量
            point_type: AI
            unit: "m³/h"
          - point_id: FH_FA_TEMP
            point_name: 新风温度
            point_type: AI
            unit: ℃
        commands:
          - point_id: FH_DAMPER
            point_name: 总风阀开度
            point_type: AO
            range: [0, 100]
          
    tier_4_room_terminal:
      name: 房间新风末端
      description: 新风进入房间的方式
    
      methods:
        method_1:
          name: 新风接入FCU回风口
          description: 新风管接入FCU吸风口，与回风混合
        
          advantages:
            - 新风与回风在FCU内混合均匀
            - 无需额外送风口
            - FCU处理后送出
          
          disadvantages:
            - FCU回风管需要开孔接入
            - 新风量受FCU风量限制
            - 可能影响FCU过滤器寿命
          
          installation:
            connection: DN100-DN150软接头
            position: FCU回风口侧面
            damper: 手动调节阀（调试用）
          
          applicable: 一般病房、办公室
        
        method_2:
          name: 房间壁面独立新风口
          description: 新风通过墙面风口直接进入房间
        
          advantages:
            - 与FCU完全独立
            - 新风直接进入房间
            - FCU故障不影响新风
          
          disadvantages:
            - 可能产生气流短路
            - 冬季冷风感
            - 需要合理布置位置
          
          installation:
            diffuser: 单层百叶风口
            position: 窗户对面墙（远离FCU送风口）
            height: 距地2.2m以上
            velocity: {value: "<2", unit: "m/s"}
          
          applicable: 需要大新风量的房间
        
        method_3:
          name: 吊顶散流器供新风（推荐）
          description: 新风通过吊顶散流器送入房间
        
          advantages:
            - 避免气流短路
            - 与FCU送风相近方式
            - 新风分布均匀
          
          disadvantages:
            - 吊顶开孔增加
            - 需要额外新风支管
            - 防火分区需设防火阀
          
          installation:
            diffuser: 方形散流器/条缝风口
            size: {value: "150×150 - 300×300", unit: mm}
            position: 远离FCU送风口
            fire_damper: 穿越防火分区时设置
          
          applicable: VIP病房、精密控制区域
        
        recommended_selection:
          general_ward: method_1（接入FCU回风口）
          isolation_ward: method_3（独立新风口）
          vip_room: method_3
          office: method_1或method_2
        
  # ========================================
  # 新风量计算与分配
  # ========================================
  fresh_air_calculation:
  
    per_person_requirement:
      standard: GB 50736-2012
      hospital_values:
        ward: {value: 30, unit: "m³/h/人"}
        outpatient: {value: 30, unit: "m³/h/人"}
        office: {value: 30, unit: "m³/h/人"}
        lobby: {value: 20, unit: "m³/h/人"}
      
    design_occupancy:
      single_ward:
        area: {value: 20, unit: "m²"}
        persons: {value: 2, unit: "人"}
        fresh_air: {value: 60, unit: "m³/h"}
      double_ward:
        area: {value: 30, unit: "m²"}
        persons: {value: 3, unit: "人"}
        fresh_air: {value: 90, unit: "m³/h"}
      multi_ward:
        area: {value: 50, unit: "m²"}
        persons: {value: 5, unit: "人"}
        fresh_air: {value: 150, unit: "m³/h"}
      private_office:
        area: {value: 15, unit: "m²"}
        persons: {value: 1, unit: "人"}
        fresh_air: {value: 30, unit: "m³/h"}
      
    minimum_background_ventilation:
      description: 无人时背景通风
      rate: {value: 0.5, unit: "次/h"}
      purpose: 维持室内空气新鲜
      control: 定时器或CO2传感器
    
    total_calculation:
      floor_total: 各房间新风量之和 × 1.1（余量系数）
      building_total: 各楼层之和 × 1.05（管道漏风）
      mau_capacity: 建筑总量 × 1.1（设计余量）
    
  # ========================================
  # 防短路设计
  # ========================================
  short_circuit_prevention:
  
    definition: |
      气流短路指新风送入后未充分混合即被排出或回风，
      导致新风效果不佳。
    
    prevention_measures:
      layout_principle:
        - 新风口与回风口（FCU吸风口）距离>3m
        - 新风送入高度与回风高度不同
        - 新风顺着气流主方向送入
      
      diffuser_selection:
        - 新风口选用低速送风型
        - 避免直吹人体
        - 与FCU送风方向一致或协调
      
      fcu_location:
        - FCU回风口朝向房间内部
        - 避免FCU送风直接对着门/窗
      
      computational_verification:
        method: CFD模拟
        criteria:
          换气效率: ">60%"
          空气龄: "<120s"
          不满意率: "<10%"
        
  # ========================================
  # 新风系统控制
  # ========================================
  control_strategy:
  
    constant_volume:
      description: 定风量新风系统
      method: MAU变频风机维持总风量恒定
      floor_damper: 固定开度（调试后锁定）
      applicable: 一般病房、办公区
    
    demand_controlled:
      description: 需求控制通风（DCV）
      method: 根据CO2浓度调节新风量
    
      sensors:
        co2:
          location: 典型房间或回风管
          setpoint: {value: 800, unit: ppm}
          range: {value: "400-1000", unit: ppm}
        occupancy:
          type: 人体感应/人数统计
          purpose: 无人时减少新风
        
      control:
        co2_high: 增加新风量
        co2_low: 减少新风量（不低于最小值）
        unoccupied: 最小背景通风
      
      applicable: 会议室、大厅、变人数区域
    
    schedule_based:
      description: 时间表控制
      method: 按作息时间调节
    
      schedule:
        occupied_hours:
          time: "07:00-21:00"
          fresh_air: 100%设计值
        unoccupied_hours:
          time: "21:00-07:00"
          fresh_air: 30%设计值（背景通风）
        pre_occupancy:
          time: 提前30分钟
          fresh_air: 100%
          purpose: 预通风
```

---

## 问题3修复：消防电梯基站位置规范

```yaml
Fire_Elevator_Base_Station:

  identity:
    name: 消防电梯基站位置规范
    description: 定义消防电梯及普通电梯火灾时的基站返回规则
    version: 1.0
    last_updated: 2024
    applicable_systems:
      - ELEC-EL

  # ========================================
  # 基站定义与标准要求
  # ========================================
  base_station_definition:
  
    standard_rule:
      reference: GB 7588-2020
      requirement: |
        消防电梯应在首层设置消防员入口和操作盘。
        火灾时，电梯应能返回到消防员入口层（基站）。
      
    base_floor_principle:
      primary: 首层（室外直通层）
      alternate: 室外地面层（如果首层不是）
    
    exceptions:
      - 当首层为着火层时，可返回首层以上或以下一层
      - 特殊建筑可根据消防设计调整
    
  # ========================================
  # 医院特殊情况处理
  # ========================================
  hospital_special_cases:
  
    case_1:
      name: 地下室着火（发电机房/停车场）
      fire_location: B1或B2层
    
      behavior:
        non_fire_elevators:
          destination: 首层
          action: 返回首层，开门后停止
        fire_elevator:
          destination: 首层待命
          action: 消防员可手动控制下行
          note: 消防电梯可下行至地下层
        
      control_logic:
        step_1: 火灾信号（B层）
        step_2: 所有电梯取消B层停靠
        step_3: 非消防电梯返回首层停止
        step_4: 消防电梯在首层待命
        step_5: 消防员持钥匙可控制至任意层
      
    case_2:
      name: 屋顶机房着火
      fire_location: 屋顶层或设备层
    
      behavior:
        all_elevators:
          destination: 首层或顶层以下一层
          action: 避开着火层
        fire_elevator:
          destination: 首层
          action: 待命，可手动上行
        
      control_logic:
        step_1: 火灾信号（顶层）
        step_2: 所有电梯取消顶层停靠
        step_3: 返回首层
        step_4: 消防员可手动控制
      
    case_3:
      name: 首层着火
      fire_location: 首层（正常基站层）
    
      behavior:
        alternate_base:
          primary: 2层（首层以上一层）
          secondary: B1层（首层以下一层）
          selection: 根据消防预案和建筑布局
        all_elevators:
          destination: 替代基站层
          action: 开门后停止
        
      control_logic:
        step_1: 火灾信号（首层）
        step_2: 系统识别首层着火
        step_3: 切换基站至2层
        step_4: 所有电梯返回2层
        step_5: 消防电梯在2层待命
      
    case_4:
      name: 住院楼中层着火
      fire_location: 中间楼层（如5层）
    
      behavior:
        non_fire_elevators:
          destination: 首层
          action: 标准迫降
        fire_elevator:
          destination: 首层
          action: 待命，消防员可上行
        
      control_logic:
        step_1: 火灾信号（5层）
        step_2: 取消5层及相邻层停靠
        step_3: 所有电梯返回首层
        step_4: 消防电梯供消防员使用
      
  # ========================================
  # 完整控制逻辑
  # ========================================
  fire_mode_control_logic:
  
    trigger_conditions:
      - FIRE-FAS火灾确认信号
      - 消防控制室手动触发
      - 电梯机房烟感报警
    
    control_sequence:
      t_0:
        event: 接收火灾确认信号
        action: 进入消防模式
      
      t_1:
        event: 识别着火层
        action: 标记禁停楼层
      
      t_2:
        event: 确定基站位置
        logic: |
          IF 着火层 ≠ 首层 THEN
            基站 = 首层
          ELSE IF 着火层 = 首层 THEN
            基站 = 2层 或 B1层
          END IF
        
      t_3:
        event: 电梯运行控制
        action:
          all_elevators:
            - 取消所有外呼
            - 取消轿内指令（除紧急）
            - 就近停靠开门
          
      t_4:
        event: 乘客疏散
        action:
          - 语音播报："火灾，请从楼梯疏散"
          - 保持开门30秒
          - 确认无人后关门
        
      t_5:
        event: 返回基站
        action:
          non_fire_elevators:
            - 运行至基站层
            - 开门停止
            - 切断运行电源（可选）
          fire_elevator:
            - 运行至基站层
            - 待命
            - 显示"消防专用"
          
      t_6:
        event: 消防员操作
        action:
          - 消防员到达基站
          - 使用消防钥匙/卡片
          - 控制消防电梯运行
        
    prohibited_actions:
      - 消防电梯不响应普通呼叫
      - 不自动停靠着火层
      - 不自动开门（消防员手动控制）
    
  # ========================================
  # 消防电梯专用功能
  # ========================================
  fire_elevator_features:
  
    control_panel:
      location: 首层电梯厅
      functions:
        - 消防开关（钥匙操作）
        - 楼层选择按钮
        - 开/关门按钮
        - 通讯对讲
      
    car_features:
      fire_button:
        location: 轿厢操作盘
        function: 消防专用控制
      priority_key:
        type: 消防钥匙开关
        function: 切换至消防控制
      direct_control:
        description: 持续按住楼层按钮运行
        purpose: 精确控制，防止误操作
      
    operation_mode:
      normal_mode:
        control: 自动群控
        response: 响应所有呼叫
      fire_mode:
        control: 消防员手动
        response: 仅响应轿内消防按钮
      
  # ========================================
  # 冗余与备份
  # ========================================
  redundancy_measures:
  
    backup_communication:
      primary:
        type: 五方对讲系统
        parties:
          - 轿厢
          - 机房
          - 轿顶
          - 底坑
          - 消防控制室
      backup:
        type: 手持无线电
        location: 消防电梯轿厢内
        channel: 消防专用频道
      
    power_supply:
      normal:
        source: 市电
        from: ELEC-LV-MAIN
      backup:
        source: 应急电源
        from: ELEC-EPS
        switchover: {value: "<15", unit: s}
      duration:
        requirement: {value: ">2", unit: h}
        typical: {value: "8+", unit: h}
      
    water_protection:
      description: 消防电梯井道防水
      measures:
        - 井道底部设集水坑
        - 配置排水泵
        - 井道门防水密封
        - 底坑排水能力>10m³/h
      
  # ========================================
  # 测试与维护
  # ========================================
  testing_requirements:
  
    periodic_test:
      frequency: 每月1次
      content:
        - 消防开关功能测试
        - 迫降功能测试
        - 对讲系统测试
        - 应急电源切换测试
      
    annual_drill:
      frequency: 每年1次
      content:
        - 完整消防联动测试
        - 消防员实际操作演练
        - 疏散配合演练
      
    documentation:
      - 测试记录表
      - 故障记录
      - 维修记录
```

---

## 问题4修复：HVAC与消防系统联动

```yaml
CHP_Fire_Interlock:

  identity:
    name: 冷热源与消防系统联动规范
    description: 定义火灾情况下HVAC-CHP系统的响应
    version: 1.0
    last_updated: 2024
    applicable_systems:
      - HVAC-CHP
      - HVAC-AHU
      - HVAC-FCU
      - FIRE-FAS

  # ========================================
  # 联动信号定义
  # ========================================
  interlock_signals:
  
    from_fire_system:
      signal_1:
        name: FIRE_CONFIRM
        description: 火灾确认信号
        from: FIRE-FAS
        type: 干接点
      
      signal_2:
        name: FIRE_FLOOR
        description: 着火楼层信号
        from: FIRE-FAS
        type: 数字信号（楼层编号）
      
      signal_3:
        name: SMOKE_EXHAUST_START
        description: 排烟系统启动信号
        from: FIRE-EXH
        type: 干接点
      
    to_hvac_system:
      signal_1:
        name: HVAC_FIRE_MODE
        description: HVAC消防模式
        to: INT-BA
        action: 触发HVAC消防响应
      
  # ========================================
  # 分区响应策略
  # ========================================
  response_by_zone:
  
    fire_floor:
      name: 着火楼层
      description: 发生火灾的楼层
    
      ahu_response:
        action: 停止该楼层AHU
        sequence:
          step_1: 关闭送风机
          step_2: 关闭回风机
          step_3: 关闭新风阀
          step_4: 关闭送回风阀
        purpose: 防止助燃和烟气扩散
        exception: 如有加压送风，保持运行
      
      fcu_response:
        action: 停止该楼层所有FCU
        sequence:
          step_1: 关闭冷/热水电动阀
          step_2: 停止风机（可选）
        purpose: 减少气流扰动
      
      chw_hw_response:
        action: 关闭该楼层冷热水供应阀
        sequence:
          step_1: 关闭楼层分水器电动阀
          step_2: 保持回水阀开启（循环）
        purpose: 隔离该楼层，防止水损
        note: 保持回水循环防止冷机过热
      
    adjacent_floors:
      name: 相邻楼层（上下各1层）
      description: 着火层上下相邻楼层
    
      ahu_response:
        action: 继续运行或降低风量
        mode: 最小新风模式
        purpose: 维持正压，防止烟气侵入
      
      fcu_response:
        action: 继续正常运行
        monitoring: 监测室温变化
      
      chw_response:
        action: 正常供应
        monitoring:
          parameter: 冷冻水供回水温度
          alarm: 温度升高>3℃时报警
        
    other_floors:
      name: 其他楼层
      description: 未受火灾直接影响的楼层
    
      hvac_response:
        action: 正常运行
        adjustment: 可根据冷热源容量调整
      
    critical_areas:
      name: 关键医疗区域
      description: 手术室、ICU、检验科等
    
      priority: 最高（确保持续运行）
    
      MED-OR:
        name: 手术室
        response:
          step_1: 评估火灾位置与手术室的关系
          step_2:
            if_fire_distant: 继续手术，启动备用冷源
            if_fire_adjacent: 准备转移患者
          step_3: 切换至独立备用冷源
          step_4: 通知手术团队
          step_5: 记录切换时间
        
      MED-ICU:
        name: ICU
        response:
          step_1: 确保供冷供热不中断
          step_2: 启动独立备用冷源
          step_3: 通知医护人员
        
      MED-LAB:
        name: 检验科
        response:
          step_1: 保护样本和仪器
          step_2: 切换至备用冷源
          step_3: 如需疏散，先保存样本
        
  # ========================================
  # 控制时序
  # ========================================
  control_sequence:
  
    timeline:
      t_0s:
        event: 火灾探测器动作
        system: FIRE-FAS
      
      t_30s:
        event: 火灾确认（人工或自动）
        system: FIRE-FAS
        action: 发出火灾确认信号
      
      t_32s:
        event: 联动信号发送
        system: FIRE-FAS
        to: INT-BA
        content:
          - FIRE_CONFIRM
          - FIRE_FLOOR
        
      t_35s:
        event: INT-BA接收并处理
        system: INT-BA
        action: 识别火灾模式，确定响应策略
      
      t_40s:
        event: 着火楼层HVAC停止
        system: HVAC
        action:
          - 关闭着火楼层AHU
          - 关闭着火楼层FCU水阀
          - 关闭楼层冷热水供应阀
        
      t_60s:
        event: 关键区域备用冷源启动
        system: HVAC-CHP（备用）
        action:
          - 启动独立风冷冷热水机组
          - 切换MED-OR/MED-ICU至备用源
        
      t_120s:
        event: 系统稳定
        status:
          - 着火楼层HVAC已隔离
          - 关键区域备用冷源运行
          - 其他楼层正常运行
        
      t_varies:
        event: 主冷机负荷调整
        system: HVAC-CHP
        action:
          - 减少着火楼层负荷后，主冷机减载
          - 群控系统自动调整运行台数
        
  # ========================================
  # 冷热源系统响应
  # ========================================
  chp_system_response:
  
    chiller_response:
      immediate:
        - 继续运行（不停机）
        - 减少着火楼层负荷后自动减载
      monitoring:
        - 冷冻水供回水温度
        - 冷却水温度
        - 冷机负荷率
      alarm:
        - 供水温度>12℃：警告
        - 供水温度>15℃：启动备用冷机
      
    boiler_response:
      immediate:
        - 继续运行（不停机）
        - 减少着火楼层热负荷
      safety:
        - 如锅炉房区域着火，立即停止锅炉
        - 切断燃气供应
      
    pump_response:
      chw_pump:
        action: 继续运行
        adjustment: 根据压差自动调速
      hw_pump:
        action: 继续运行
        adjustment: 根据压差自动调速
      cw_pump:
        action: 继续运行（冷机运行时）
      
    cooling_tower:
      action: 继续运行（冷机运行时）
    
  # ========================================
  # 备用冷源切换
  # ========================================
  backup_source_switchover:
  
    trigger_conditions:
      - 主冷源故障
      - 主冷源区域着火
      - 主冷冻水温度>12℃持续5分钟
    
    backup_equipment:
      type: 独立风冷冷热水机组
      capacity: {value: 200, unit: kW}
      location: 屋顶或独立机房
      served_areas:
        - MED-OR（手术室）
        - MED-ICU（ICU）
        - MED-LAB（检验科，可选）
      
    switchover_sequence:
      step_1:
        action: 启动备用冷源机组
        time: {value: 30, unit: s}
      step_2:
        action: 开启备用源出口阀
        time: {value: 10, unit: s}
      step_3:
        action: 关闭主源接入阀
        time: {value: 10, unit: s}
      step_4:
        action: 确认备用源供水正常
        parameter: 供水温度<10℃
      step_5:
        action: 通知相关人员
        method: BA系统报警+短信
      
    total_switchover_time: {value: "<120", unit: s}
  
    cold_water_buffer:
      description: 切换期间的冷水缓冲
      method: 关键区域管路蓄水量
      duration: {value: "2-3", unit: min}
      note: 确保切换期间无明显温升
    
  # ========================================
  # 火灾后恢复
  # ========================================
  post_fire_recovery:
  
    trigger: 火灾确认解除信号
    source: FIRE-FAS（手动复位）
  
    recovery_sequence:
      step_1:
        action: 确认火灾已扑灭
        verifier: 消防队/安全员
        documentation: 火灾解除确认书
      
      step_2:
        action: 消防系统复位
        includes:
          - 排烟系统停止
          - 加压送风停止
          - 消防电梯返回正常模式
        
      step_3:
        action: 检查着火楼层HVAC设备
        content:
          - 设备损坏情况
          - 管道完整性
          - 电气安全
        duration: {value: "30-60", unit: min}
      
      step_4:
        action: 逐步恢复着火楼层HVAC
        sequence:
          - 开启冷热水供应阀
          - 启动AHU（先低速）
          - 开启FCU水阀
          - 恢复正常运行
        note: 逐步恢复，避免冲击
      
      step_5:
        action: 关键区域备用冷源切回主源
        sequence:
          - 确认主冷源正常
          - 开启主源接入阀
          - 关闭备用源出口阀
          - 停止备用冷源机组
        note: 主源稳定后再切换
      
      step_6:
        action: 全院HVAC恢复正常群控
        status: 正常运行模式
      
    documentation:
      - 火灾时间
      - HVAC响应记录
      - 设备损坏报告
      - 恢复时间
      - 经验总结
```

---

## 问题5修复：FCU冷凝水排放系统

```yaml
Condensate_Drain_System:

  identity:
    name: FCU冷凝水排放系统
    description: 定义风机盘管冷凝水的完整排放链路
    version: 1.0
    last_updated: 2024
    applicable_systems:
      - HVAC-FCU

  # ========================================
  # 系统设计原则
  # ========================================
  design_principles:
  
    purpose:
      - 收集FCU运行时产生的冷凝水
      - 安全排放至排水系统
      - 防止积水、漏水、溢出
      - 避免滋生细菌/霉菌
    
    requirements:
      - 重力自流为主，避免积水
      - 管道保温防止二次冷凝
      - 设置水封/存水弯防臭
      - 关键区域设置溢流报警
    
  # ========================================
  # 冷凝水产生量
  # ========================================
  condensate_generation:
  
    calculation:
      formula: |
        冷凝水量 = 空气处理量 × (进口含湿量 - 出口含湿量)
    
    typical_values:
      small_fcu:
        cooling_capacity: {value: 3.5, unit: kW}
        condensate: {value: "0.5-1.0", unit: "L/h"}
      medium_fcu:
        cooling_capacity: {value: 7, unit: kW}
        condensate: {value: "1.0-2.0", unit: "L/h"}
      large_fcu:
        cooling_capacity: {value: 14, unit: kW}
        condensate: {value: "2.0-4.0", unit: "L/h"}
      
    influencing_factors:
      - 室内湿度（湿度高→冷凝水多）
      - 冷冻水温度（温度低→冷凝水多）
      - FCU运行时间
      - 季节（夏季>其他季节）
    
  # ========================================
  # 排放系统设计
  # ========================================
  drain_system_design:
  
    fcu_drain_pan:
      name: FCU集水盘
      material:
        options:
          - 镀锌钢板（喷涂防腐）
          - 不锈钢
          - ABS塑料
        recommendation: 不锈钢或ABS（医院推荐）
      insulation:
        required: true
        material: 橡塑保温
        thickness: {value: 10, unit: mm}
        purpose: 防止盘外冷凝
      slope:
        direction: 向排水口倾斜
        value: {value: ">1", unit: "%"}
      drain_outlet:
        size: DN20
        position: 最低点
      
    condensate_drain_pipe:
      name: 冷凝水排水管
    
      material:
        options:
          - UPVC（常用）
          - HDPE（柔韧性好）
          - PPR（耐低温）
        recommendation: UPVC或HDPE
      
      sizing:
        principle: 根据FCU数量和冷凝水量
        typical_sizes:
          single_fcu: DN20
          branch_pipe: DN25-DN32
          floor_main: DN40-DN50
          riser: DN50-DN75
        
      slope:
        horizontal_pipe: {value: ">2", unit: "%"}
        note: 确保重力自流
      
      insulation:
        required: true
        material: 橡塑保温
        thickness: {value: 10, unit: mm}
        purpose: 防止管外冷凝
      
    routing_methods:
      method_1:
        name: 立管式集中排放（推荐）
        description: 各楼层冷凝水汇集至专用立管
      
        configuration:
          floor_branch:
            description: 楼层水平支管
            slope: 2%
            connection: 各FCU排水口
          riser:
            description: 冷凝水立管
            location: 管井内
            size: DN50-DN75
          bottom_outlet:
            description: 底部排出
            connection: 污水排水系统
          
        advantages:
          - 集中管理
          - 便于维护
          - 减少堵塞风险
        disadvantages:
          - 需要专用管井空间
        
      method_2:
        name: 分散就近排放
        description: 各FCU冷凝水就近接入卫生间排水
      
        configuration:
          drain_route:
            description: FCU→附近卫生间地漏
            distance: {value: "<5", unit: m}
          trap:
            description: 存水弯
            purpose: 防臭
          
        advantages:
          - 管路短
          - 不需要专用立管
        disadvantages:
          - 分散，难以统一管理
          - 可能影响卫生间
        
    trap_water_seal:
      name: 存水弯/水封
      purpose: 防止排水管臭气倒流
    
      configuration:
        p_trap:
          name: P型存水弯
          location: 每台FCU排水口后
          seal_depth: {value: 50, unit: mm}
        s_trap:
          name: S型存水弯
          application: 特殊安装条件
        
      maintenance:
        issue: 长期不用导致水封干涸
        prevention:
          - 定期补水
          - 使用自动补水装置
          - 空调不运行时保持少量通风
        
  # ========================================
  # 楼层集水系统
  # ========================================
  floor_collection_system:
  
    for_high_rise:
      description: 高层建筑冷凝水收集
    
      floor_header:
        name: 楼层冷凝水汇集管
        size: DN40-DN50
        slope: 2%
        location: 走廊吊顶
      
      cleanout:
        name: 检查口
        interval: {value: 15, unit: m}
        purpose: 清通堵塞
      
    for_basement:
      description: 地下室冷凝水收集
    
      sump_pit:
        name: 集水坑
        size:
          length: {value: 1.0, unit: m}
          width: {value: 0.8, unit: m}
          depth: {value: 0.6, unit: m}
        volume: {value: "0.5-1.0", unit: "m³"}
        location: 地下室最低点
      
      sump_pump:
        name: 潜水排水泵
        type: 小型潜水泵
        flow: {value: 5, unit: "m³/h"}
        head: {value: 10, unit: m}
        quantity: 2台（1用1备）
        control:
          method: 液位开关
          start: 高液位
          stop: 低液位
          alarm: 超高液位
        
      discharge:
        destination: 污水排水系统
        pipe_size: DN50
        check_valve: required
      
  # ========================================
  # 溢出保护
  # ========================================
  overflow_protection:
  
    water_level_switch:
      name: 集水盘水位开关
      type: 浮球开关/电容式开关
      location: FCU集水盘内
    
      trigger_levels:
        normal: 0-30%水位
        warning: 50%水位
        alarm: 80%水位
      
    alarm_response:
      level_warning:
        action:
          - 本地蜂鸣器提示（可听）
          - BA系统显示警告
        operator_action: 检查排水是否通畅
      
      level_alarm:
        action:
          step_1: 关闭该FCU冷水阀
          step_2: 继续运行风机（帮助蒸发）
          step_3: BA系统报警
          step_4: 通知维修人员
        purpose: 防止溢出
      
      recovery:
        condition: 水位恢复正常
        action:
          step_1: 维修人员检查并清理堵塞
          step_2: 手动复位报警
          step_3: 恢复FCU正常运行
        
    secondary_drain:
      name: 备用排水口
      description: 主排水堵塞时的溢流通道
    
      configuration:
        location: 集水盘较高位置
        size: DN20
        route: 独立排水管或接入主排水
        indicator: 如有水流出，表示主排水堵塞
      
  # ========================================
  # 医疗区域特殊要求
  # ========================================
  medical_area_special:
  
    standard_ward:
      name: 普通病房
    
      requirements:
        - 冷凝水不能积存
        - 排水管保温防冷凝
        - 设置溢流报警
      
      drain_system:
        method: 集中立管排放
        outlet: 污水处理系统
        retention_time: {value: "<1", unit: h}
        note: 冷凝水不积存
      
    isolation_ward:
      name: 隔离病房/负压病房
    
      special_requirements:
        - 冷凝水单独收集
        - 消毒处理后排放
        - 防止交叉感染
      
      drain_system:
        collection:
          description: 隔离病房FCU冷凝水独立收集
          tank: 专用消毒收集罐
          capacity: {value: 50, unit: L}
        treatment:
          method: 化学消毒（次氯酸钠）
          contact_time: {value: 30, unit: min}
          concentration: {value: 500, unit: "mg/L"}
        discharge:
          destination: 消毒后进入污水系统
          monitoring: 记录消毒和排放
        
    operating_room:
      name: 手术室
    
      special_requirements:
        - 不产生冷凝水（设计要求）
        - 空调系统采用干盘管或无冷凝设计
        - 如有冷凝，立即排走
      
      drain_system:
        design: 尽量避免冷凝
        backup: 如有冷凝水，直接排入专用管道
      
    icu:
      name: ICU
    
      drain_system:
        method: 与普通病房类似
        additional:
          - 加强保温
          - 双重溢流保护
          - 快速响应报警
        
  # ========================================
  # 维护与清洁
  # ========================================
  maintenance_cleaning:
  
    routine_maintenance:
      frequency: 每月1次
      content:
        - 检查集水盘清洁度
        - 检查排水管通畅
        - 清理存水弯
        - 测试水位开关
      
    deep_cleaning:
      frequency: 每年1次（夏季前）
      content:
        - 集水盘消毒清洗
        - 排水管路冲洗
        - 更换老化密封件
        - 检查保温层完整性
      
    blockage_clearing:
      trigger: 排水不畅或溢流报警
      method:
        step_1: 关闭FCU冷水阀
        step_2: 清理集水盘杂物
        step_3: 疏通排水管（使用疏通器）
        step_4: 冲洗管路
        step_5: 恢复运行，观察
      
    hygiene_control:
      purpose: 防止细菌/霉菌滋生
      measures:
        - 保持排水通畅，不积水
        - 定期消毒集水盘
        - 使用抑菌型集水盘（可选）
        - 空调停用期间保持通风干燥
```

***

