## 🧑‍💻 User


输出第五批次

---
## 🤖 Assistant


# Agent-01 系统拓扑建模师 - 完整输出文档

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

---