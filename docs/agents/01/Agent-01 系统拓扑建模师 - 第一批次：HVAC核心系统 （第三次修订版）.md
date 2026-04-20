# Agent-01 系统拓扑建模师 - 第一批次：HVAC核心系统 （第三次修订版）

## 修订说明

根据评审意见，本次修订重点解决以下高优先级缺陷：
- **H1**: 补充压差控制逻辑和变流量/恒压控制策略
- **H2**: 完善冷却塔与冷水机联动控制逻辑
- **H3**: 补充新风机组(PAU)与FCU的新风配比控制
- **H4-H6**: 部分中优先级改进

---

# 第一批次：HVAC核心系统（6个系统）

## 系统 1.1: HVAC-CHP 冷热源系统（第三版）

```yaml
System_Topology:

  # ========================================
  # IDENTITY SECTION - 系统标识
  # ========================================
  identity:
    system_id: HVAC-CHP
    system_name: 冷热源系统
    system_name_en: Chilled/Hot Water Plant System
    system_category: HVAC
    system_type: 水系统-冷热源
    priority_level: P1-CRITICAL
  
    description: |
      医院核心冷热源系统，为全院空调系统提供冷冻水和热水。
      冷源采用离心式/螺杆式冷水机组，热源采用燃气热水锅炉。
      系统采用一次泵定流量+二次泵变流量的运行模式。
      冷冻水供回水温度7℃/12℃，热水供回水温度60℃/50℃。
  
    design_basis:
      building_type: 三级甲等综合医院
      total_cooling_load: {value: 8000, unit: kW, note: "设计值，含同时使用系数"}
      total_heating_load: {value: 6000, unit: kW, note: "设计值"}
      chw_design_temp: {supply: 7, return: 12, unit: ℃, note: "设计工况"}
      hw_design_temp: {supply: 60, return: 50, unit: ℃, note: "设计工况"}
  
    child_systems:
      - HVAC-CHW  # 冷冻水输配系统
      - HVAC-HW   # 热水输配系统
  
    related_systems:
      - ELEC-LV-MAIN  # 低压配电（动力电源）
      - INT-BA        # 楼宇自控（监控接口）
      - PLUMB-DWS     # 生活给水（补水水源）
  
    design_standards:
      - GB 50736-2012 民用建筑供暖通风与空气调节设计规范
      - GB 50189-2015 公共建筑节能设计标准
      - GB 51039-2014 综合医院建筑设计规范
      - GB 50016-2014 建筑设计防火规范
  
    version: 3.0
    revision_notes: |
      v3.0: 补充压差控制策略、冷却塔联动逻辑、噪声控制要求
      v2.0: 细化泵组节点、增加补水定压系统
      v1.0: 初始版本
    last_updated: 2024

  # ========================================
  # BOUNDARY SECTION - 系统边界
  # ========================================
  boundary:
  
    inputs:
      - boundary_id: HVAC-CHP_IN_001
        name: 市电电源输入
        from_system: ELEC-LV-MAIN
        from_node: ELEC-LV-MAIN_SNK_HVAC_FEEDER
        medium: ELEC-LV
        parameters:
          voltage: {value: 380, unit: V}
          phases: 3
          frequency: {value: 50, unit: Hz}
        note: 冷水机组、水泵、冷却塔动力电源
      
      - boundary_id: HVAC-CHP_IN_002
        name: 天然气输入
        from_system: EXTERNAL_GAS
        medium: GAS-NG
        parameters:
          pressure: {value: 20, unit: kPa, note: "中压燃气，经调压后"}
          calorific_value: {value: 35.6, unit: "MJ/m³"}
        note: 锅炉燃料
      
      - boundary_id: HVAC-CHP_IN_003
        name: 软化水补水输入
        from_system: PLUMB-DWS
        from_node: PLUMB-DWS_SNK_SOFTENER
        medium: WATER-SOFT
        parameters:
          pressure: {value: 0.25-0.35, unit: MPa}
          hardness: {value: "<50", unit: "mg/L CaCO3"}
        note: 系统补水经软化处理
      
      - boundary_id: HVAC-CHP_IN_004
        name: BA系统控制信号
        from_system: INT-BA
        medium: SIGNAL-CTRL
        parameters:
          protocol: BACnet/IP
          points: 约200点
        note: 监控和控制信号
        
    outputs:
      - boundary_id: HVAC-CHP_OUT_001
        name: 冷冻水供水输出
        to_system: HVAC-CHW
        to_node: HVAC-CHW_SRC_RISER_IN
        medium: CHW
        parameters:
          temperature: {value: 7, unit: ℃, tolerance: ±0.5}
          pressure: {value: 0.4-0.5, unit: MPa}
          flow_rate: {value: 1400, unit: "m³/h", note: "设计总流量"}
        
      - boundary_id: HVAC-CHP_OUT_002
        name: 热水供水输出
        to_system: HVAC-HW
        to_node: HVAC-HW_SRC_RISER_IN
        medium: HW
        parameters:
          temperature: {value: 60, unit: ℃, tolerance: ±2}
          pressure: {value: 0.35-0.45, unit: MPa}
          flow_rate: {value: 520, unit: "m³/h", note: "设计总流量"}

  # ========================================
  # NODES SECTION - 节点定义
  # ========================================
  nodes:

    # ========================================
    # Source Nodes - 能量来源节点
    # ========================================
    source_nodes:
  
      - node_id: HVAC-CHP_SRC_CHILLER
        node_name: 离心式冷水机组
        node_name_en: Centrifugal Water Chiller
        node_type: Source_Node
        node_category: SRC
      
        function: 制取空调冷冻水
        medium_in: [ELEC-LV, CW]
        medium_out: CHW
      
        multiplicity: multiple
        instance_pattern: HVAC-CHP_SRC_CHILLER_{NN}
        typical_configuration:
          quantity: 3
          redundancy: "N+1"
          capacity_each: {value: 2800, unit: kW, note: "单台制冷量"}
          total_capacity: {value: 8400, unit: kW}
          load_ratio: "满足100%设计负荷+1台备用"
      
        equipment_parameters:
          type: 离心式冷水机组（变频）
          refrigerant: R134a
          cop: {value: ">6.0", note: "满负荷COP，AHRI工况"}
          iplv: {value: ">8.5", note: "综合部分负荷性能"}
          chw_flow_rate: {value: 480, unit: "m³/h", note: "单台额定流量"}
          chw_supply_temp: {value: 7, unit: ℃, range: [5, 10]}
          chw_return_temp: {value: 12, unit: ℃}
          cw_flow_rate: {value: 580, unit: "m³/h", note: "单台额定流量"}
          cw_inlet_temp: {value: 32, unit: ℃, range: [18, 35]}
          cw_outlet_temp: {value: 37, unit: ℃}
          power_input: {value: 460, unit: kW, note: "额定输入功率"}
          min_load_ratio: {value: 10, unit: "%", note: "最小负荷率"}
          startup_time: {value: 300, unit: s, note: "冷启动时间"}
      
        control_points:
          sensors:
            - point_id: CHILLER_CHWST
              point_name: 冷冻水供水温度
              point_type: AI
              unit: ℃
              range: [0, 20]
              accuracy: ±0.1℃
            - point_id: CHILLER_CHWRT
              point_name: 冷冻水回水温度
              point_type: AI
              unit: ℃
              range: [0, 25]
            - point_id: CHILLER_CWIT
              point_name: 冷却水进水温度
              point_type: AI
              unit: ℃
              range: [10, 40]
            - point_id: CHILLER_CWOT
              point_name: 冷却水出水温度
              point_type: AI
              unit: ℃
              range: [15, 45]
            - point_id: CHILLER_LOAD
              point_name: 机组负载率
              point_type: AI
              unit: "%"
              range: [0, 100]
            - point_id: CHILLER_POWER
              point_name: 机组功率
              point_type: AI
              unit: kW
              range: [0, 500]
            - point_id: CHILLER_CHW_FLOW
              point_name: 冷冻水流量
              point_type: AI
              unit: "m³/h"
              range: [0, 600]
          status:
            - point_id: CHILLER_RUN
              point_name: 机组运行状态
              point_type: DI
            - point_id: CHILLER_FAULT
              point_name: 机组故障状态
              point_type: DI
            - point_id: CHILLER_REMOTE
              point_name: 远程/本地模式
              point_type: DI
            - point_id: CHILLER_READY
              point_name: 机组就绪状态
              point_type: DI
          commands:
            - point_id: CHILLER_START_CMD
              point_name: 机组启停命令
              point_type: DO
            - point_id: CHILLER_LOAD_LIMIT
              point_name: 负荷限制设定
              point_type: AO
              unit: "%"
              range: [0, 100]
          setpoints:
            - point_id: CHILLER_CHWST_SP
              point_name: 冷冻水供水温度设定
              point_type: AO
              unit: ℃
              range: [5, 10]
              default: 7
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房
          floor: B1
          area_requirement: {value: ">400", unit: "m²"}
          ceiling_height: {value: ">6", unit: m}
          load_bearing: {value: ">2000", unit: "kg/m²"}
      
        installation_requirements:
          - 减振基础，独立承台
          - 设备吊装孔预留
          - 检修通道≥1.5m
          - 冷媒泄漏探测器
          - 机房通风换气≥6次/h
          - 紧急排风设施
      
        noise_control:
          equipment_noise: "<85dB(A)@1m"
          room_treatment: "墙面吸声处理"
          vibration_isolation: "弹簧减振器+惯性基座"

      - node_id: HVAC-CHP_SRC_BOILER
        node_name: 燃气热水锅炉
        node_name_en: Gas Fired Hot Water Boiler
        node_type: Source_Node
        node_category: SRC
      
        function: 制取空调热水
        medium_in: [GAS-NG, WATER-DW]
        medium_out: HW
      
        multiplicity: multiple
        instance_pattern: HVAC-CHP_SRC_BOILER_{NN}
        typical_configuration:
          quantity: 3
          redundancy: "N+1"
          capacity_each: {value: 2800, unit: kW}
          total_capacity: {value: 8400, unit: kW}
      
        equipment_parameters:
          type: 真空热水锅炉
          thermal_efficiency: {value: ">96%", note: "低位热值效率"}
          fuel_type: 天然气
          fuel_consumption: {value: 280, unit: "Nm³/h", note: "单台最大"}
          hw_supply_temp: {value: 60, unit: ℃, range: [45, 85]}
          hw_return_temp: {value: 50, unit: ℃, range: [35, 70]}
          hw_flow_rate: {value: 240, unit: "m³/h", note: "单台额定"}
          pressure_rating: {value: 0, unit: MPa, note: "真空锅炉无压"}
          turndown_ratio: "5:1"
          nox_emission: "<30mg/m³"
          startup_time: {value: 180, unit: s, note: "热启动"}
      
        control_points:
          sensors:
            - point_id: BOILER_HW_ST
              point_name: 热水供水温度
              point_type: AI
              unit: ℃
              range: [0, 100]
            - point_id: BOILER_HW_RT
              point_name: 热水回水温度
              point_type: AI
              unit: ℃
              range: [0, 100]
            - point_id: BOILER_GAS_PRESS
              point_name: 燃气压力
              point_type: AI
              unit: kPa
              range: [0, 50]
            - point_id: BOILER_FLUE_TEMP
              point_name: 烟气温度
              point_type: AI
              unit: ℃
              range: [0, 300]
            - point_id: BOILER_O2
              point_name: 烟气含氧量
              point_type: AI
              unit: "%"
              range: [0, 21]
            - point_id: BOILER_LOAD
              point_name: 锅炉负载率
              point_type: AI
              unit: "%"
              range: [0, 100]
          status:
            - point_id: BOILER_RUN
              point_name: 锅炉运行状态
              point_type: DI
            - point_id: BOILER_FAULT
              point_name: 锅炉故障状态
              point_type: DI
            - point_id: BOILER_FLAME
              point_name: 火焰检测状态
              point_type: DI
            - point_id: BOILER_GAS_VALVE
              point_name: 燃气阀状态
              point_type: DI
          commands:
            - point_id: BOILER_START_CMD
              point_name: 锅炉启停命令
              point_type: DO
          setpoints:
            - point_id: BOILER_HW_ST_SP
              point_name: 热水供水温度设定
              point_type: AO
              unit: ℃
              range: [45, 85]
              default: 60
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 锅炉房
          floor: B1/1F
          area_requirement: {value: ">250", unit: "m²"}
          ceiling_height: {value: ">5", unit: m}
      
        installation_requirements:
          - 防火间距符合GB 50016要求
          - 独立燃气调压间
          - 烟囱高度≥15m或高于周边建筑
          - 防爆要求区域
          - 可燃气体探测器（与消防联动）
          - 紧急切断阀（门口设置）
          - 事故通风≥12次/h
          - 泄爆面积≥锅炉间面积的10%

      - node_id: HVAC-CHP_SRC_ASHP
        node_name: 空气源热泵机组
        node_name_en: Air Source Heat Pump Unit
        node_type: Source_Node
        node_category: SRC
      
        function: 制取空调冷/热水（过渡季/辅助/应急）
        medium_in: AIR-OA
        medium_out: [CHW, HW]
      
        multiplicity: multiple
        instance_pattern: HVAC-CHP_SRC_ASHP_{NN}
        typical_configuration:
          quantity: 2
          redundancy: "备用/补充冷源"
          capacity_each: {value: 500, unit: kW}
      
        equipment_parameters:
          type: 风冷模块化热泵机组
          cooling_capacity: {value: 500, unit: kW}
          heating_capacity: {value: 550, unit: kW}
          cop_cooling: ">3.2"
          cop_heating: ">3.5"
          chw_supply_temp: {value: 7, unit: ℃}
          hw_supply_temp: {value: 45, unit: ℃, note: "热泵制热出水温度较低"}
          ambient_range: {cooling: [-5, 43], heating: [-15, 21], unit: ℃}
          defrost_temp: {value: -5, unit: ℃, note: "低于此温度需除霜"}
      
        control_points:
          sensors:
            - point_id: ASHP_WT
              point_name: 出水温度
              point_type: AI
              unit: ℃
            - point_id: ASHP_AMBIENT
              point_name: 环境温度
              point_type: AI
              unit: ℃
          status:
            - point_id: ASHP_RUN
              point_name: 机组运行状态
              point_type: DI
            - point_id: ASHP_MODE
              point_name: 制冷/制热模式
              point_type: DI
            - point_id: ASHP_DEFROST
              point_name: 除霜状态
              point_type: DI
            - point_id: ASHP_FAULT
              point_name: 机组故障状态
              point_type: DI
          commands:
            - point_id: ASHP_START_CMD
              point_name: 机组启停命令
              point_type: DO
            - point_id: ASHP_MODE_CMD
              point_name: 模式切换命令
              point_type: DO
      
        location_hint:
          space_type: OUTDOOR
          position: 裙房屋面/室外地面
          area_requirement: {value: ">100", unit: "m²"}
      
        installation_requirements:
          - 通风良好，避免气流短路
          - 设备基础减振
          - 检修通道≥1.2m
          - 噪音控制措施（声屏障）
          - 化霜排水设施

    # ========================================
    # Distribution Nodes - 传输/调节/分配节点
    # ========================================
    distribution_nodes:
  
      # === 冷冻水一次侧 ===
      - node_id: HVAC-CHP_DST_CHW_PRI_PUMP
        node_name: 冷冻水一次泵
        node_name_en: Chilled Water Primary Pump
        node_type: Distribution_Node
        node_subtype: TRF
        node_category: DST
      
        function: 冷水机组侧冷冻水循环（定流量）
        medium_in: CHW
        medium_out: CHW
      
        multiplicity: multiple
        instance_pattern: HVAC-CHP_DST_CHW_PRI_PUMP_{NN}
        typical_configuration:
          quantity: 4
          redundancy: "一机一泵+1公共备用"
          operation_mode: 与对应冷水机组联锁运行
      
        equipment_parameters:
          type: 卧式单级离心泵
          flow_rate: {value: 480, unit: "m³/h", note: "与冷水机组配套"}
          head: {value: 25, unit: mH2O, range: [22, 28]}
          power: {value: 45, unit: kW}
          efficiency: ">80%"
          motor_efficiency: "IE3"
          control_type: 工频运行
          npsh_required: {value: 4, unit: m}
      
        control_points:
          status:
            - point_id: CHW_PRI_PUMP_RUN
              point_name: 泵运行状态
              point_type: DI
            - point_id: CHW_PRI_PUMP_FAULT
              point_name: 泵故障状态
              point_type: DI
            - point_id: CHW_PRI_PUMP_OVERLOAD
              point_name: 电机过载
              point_type: DI
          commands:
            - point_id: CHW_PRI_PUMP_START_CMD
              point_name: 泵启停命令
              point_type: DO
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房
          position: 冷水机组蒸发器出水侧
      
        noise_control:
          vibration_isolation: 弹性橡胶垫/弹簧减振器
          flexible_connection: 橡胶软接头

      # === 冷冻水二次侧 ===
      - node_id: HVAC-CHP_DST_CHW_SEC_PUMP
        node_name: 冷冻水二次泵
        node_name_en: Chilled Water Secondary Pump
        node_type: Distribution_Node
        node_subtype: TRF
        node_category: DST
      
        function: 用户侧冷冻水循环，变频调节
        medium_in: CHW
        medium_out: CHW
      
        multiplicity: multiple
        instance_pattern: HVAC-CHP_DST_CHW_SEC_PUMP_{NN}
        typical_configuration:
          quantity: 4
          redundancy: "N+1"
          operation_mode: 根据系统压差变频调节
      
        equipment_parameters:
          type: 卧式单级离心泵
          flow_rate: {value: 500, unit: "m³/h", note: "单台设计流量"}
          head: {value: 32, unit: mH2O, range: [28, 38]}
          power: {value: 55, unit: kW}
          efficiency: ">82%"
          motor_efficiency: "IE4"
          control_type: 变频调节
          vfd_brand: 知名品牌变频器
          vfd_range: {min: 25, max: 50, unit: Hz}
          min_flow: {value: 150, unit: "m³/h", note: "最小稳定流量@25Hz"}
      
        control_points:
          sensors:
            - point_id: CHW_SEC_PUMP_FREQ
              point_name: 泵运行频率
              point_type: AI
              unit: Hz
              range: [0, 50]
            - point_id: CHW_SEC_PUMP_CURRENT
              point_name: 电机电流
              point_type: AI
              unit: A
              range: [0, 150]
            - point_id: CHW_SEC_PUMP_POWER
              point_name: 泵功率
              point_type: AI
              unit: kW
              range: [0, 60]
          status:
            - point_id: CHW_SEC_PUMP_RUN
              point_name: 泵运行状态
              point_type: DI
            - point_id: CHW_SEC_PUMP_FAULT
              point_name: 泵故障状态
              point_type: DI
            - point_id: CHW_SEC_PUMP_VFD_FAULT
              point_name: 变频器故障
              point_type: DI
          commands:
            - point_id: CHW_SEC_PUMP_START_CMD
              point_name: 泵启停命令
              point_type: DO
          setpoints:
            - point_id: CHW_SEC_PUMP_FREQ_SP
              point_name: 泵频率设定
              point_type: AO
              unit: Hz
              range: [25, 50]
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房
          position: 分水器前端

      # === 分集水器 ===
      - node_id: HVAC-CHP_DST_CHW_HEADER_S
        node_name: 冷冻水供水分水器
        node_name_en: Chilled Water Supply Header
        node_type: Distribution_Node
        node_subtype: SPL
        node_category: DST
      
        function: 冷冻水供水分配至各区域主管
        medium_in: CHW
        medium_out: CHW
      
        equipment_parameters:
          type: 分水器/分水缸
          diameter: {value: DN500, unit: mm, note: "按流速0.8-1.2m/s选型"}
          length: {value: 3000, unit: mm}
          material: 无缝钢管
          outlets: {value: 8, unit: 路, note: "含备用接口"}
          pressure_rating: {value: 1.6, unit: MPa}
          insulation: {type: "橡塑保温", thickness: 50, unit: mm}
      
        control_points:
          sensors:
            - point_id: CHW_HEADER_S_TEMP
              point_name: 分水器温度
              point_type: AI
              unit: ℃
            - point_id: CHW_HEADER_S_PRESS
              point_name: 分水器压力
              point_type: AI
              unit: MPa
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房
          position: 中央位置
        
      - node_id: HVAC-CHP_DST_CHW_HEADER_R
        node_name: 冷冻水回水集水器
        node_name_en: Chilled Water Return Header
        node_type: Distribution_Node
        node_subtype: JUN
        node_category: DST
      
        function: 汇集各区域冷冻水回水
        medium_in: CHW
        medium_out: CHW
      
        equipment_parameters:
          type: 集水器/集水缸
          diameter: {value: DN500, unit: mm}
          length: {value: 3000, unit: mm}
          material: 无缝钢管
          inlets: {value: 8, unit: 路}
          pressure_rating: {value: 1.6, unit: MPa}
          insulation: {type: "橡塑保温", thickness: 50, unit: mm}
      
        control_points:
          sensors:
            - point_id: CHW_HEADER_R_TEMP
              point_name: 集水器温度
              point_type: AI
              unit: ℃
            - point_id: CHW_HEADER_R_PRESS
              point_name: 集水器压力
              point_type: AI
              unit: MPa
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房
          position: 与分水器平行布置

      # === 旁通控制 ===
      - node_id: HVAC-CHP_DST_CHW_BYPASS
        node_name: 冷冻水压差旁通阀
        node_name_en: Chilled Water Differential Pressure Bypass Valve
        node_type: Distribution_Node
        node_subtype: REG
        node_category: DST
      
        function: |
          一二次泵解耦，保护冷水机组最小流量
          当二次侧流量减小时，开启旁通维持一次侧流量
        medium_in: CHW
        medium_out: CHW
      
        equipment_parameters:
          type: 电动压差旁通阀组
          main_valve: {size: DN200, type: "电动蝶阀", cv: 1600}
          actuator: {type: "比例积分", signal: "4-20mA", torque: "200Nm"}
          bypass_pipe: {size: DN200, material: "无缝钢管"}
      
        control_points:
          sensors:
            - point_id: CHW_BYPASS_POS
              point_name: 旁通阀开度
              point_type: AI
              unit: "%"
              range: [0, 100]
            - point_id: CHW_DP
              point_name: 一二次侧压差
              point_type: AI
              unit: kPa
              range: [0, 200]
              location: 分集水器之间
            - point_id: CHW_PRI_FLOW
              point_name: 一次侧总流量
              point_type: AI
              unit: "m³/h"
              range: [0, 2000]
            - point_id: CHW_SEC_FLOW
              point_name: 二次侧总流量
              point_type: AI
              unit: "m³/h"
              range: [0, 2000]
          setpoints:
            - point_id: CHW_DP_SP
              point_name: 压差设定值
              point_type: AO
              unit: kPa
              range: [50, 150]
              default: 80
      
        control_strategy:
          name: 压差旁通控制
          description: |
            维持分集水器之间的压差稳定，确保一次侧流量不低于机组最小流量
          logic: |
            1. 实测压差 > 设定值 → 开大旁通阀
            2. 实测压差 < 设定值 → 关小旁通阀
            3. 一次侧流量 < 机组最小流量 → 强制开大旁通阀
            4. 旁通阀开度反馈用于诊断系统平衡
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房
          position: 分集水器之间，短接管路

      # === 热水系统泵组 ===
      - node_id: HVAC-CHP_DST_HW_PRI_PUMP
        node_name: 热水一次泵
        node_name_en: Hot Water Primary Pump
        node_type: Distribution_Node
        node_subtype: TRF
        node_category: DST
      
        function: 锅炉侧热水循环（定流量）
        medium_in: HW
        medium_out: HW
      
        multiplicity: multiple
        instance_pattern: HVAC-CHP_DST_HW_PRI_PUMP_{NN}
        typical_configuration:
          quantity: 3
          redundancy: "一机一泵"
      
        equipment_parameters:
          type: 卧式单级离心泵
          flow_rate: {value: 240, unit: "m³/h"}
          head: {value: 20, unit: mH2O}
          power: {value: 22, unit: kW}
          efficiency: ">78%"
          motor_efficiency: "IE3"
          control_type: 工频运行
      
        control_points:
          status:
            - point_id: HW_PRI_PUMP_RUN
              point_name: 泵运行状态
              point_type: DI
            - point_id: HW_PRI_PUMP_FAULT
              point_name: 泵故障状态
              point_type: DI
          commands:
            - point_id: HW_PRI_PUMP_START_CMD
              point_name: 泵启停命令
              point_type: DO
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 锅炉房
          position: 锅炉出水侧

      - node_id: HVAC-CHP_DST_HW_SEC_PUMP
        node_name: 热水二次泵
        node_name_en: Hot Water Secondary Pump
        node_type: Distribution_Node
        node_subtype: TRF
        node_category: DST
      
        function: 用户侧热水循环，变频调节
        medium_in: HW
        medium_out: HW
      
        multiplicity: multiple
        instance_pattern: HVAC-CHP_DST_HW_SEC_PUMP_{NN}
        typical_configuration:
          quantity: 3
          redundancy: "N+1"
      
        equipment_parameters:
          type: 卧式单级离心泵
          flow_rate: {value: 260, unit: "m³/h"}
          head: {value: 28, unit: mH2O}
          power: {value: 30, unit: kW}
          efficiency: ">80%"
          motor_efficiency: "IE4"
          control_type: 变频调节
          vfd_range: {min: 25, max: 50, unit: Hz}
      
        control_points:
          sensors:
            - point_id: HW_SEC_PUMP_FREQ
              point_name: 泵运行频率
              point_type: AI
              unit: Hz
          status:
            - point_id: HW_SEC_PUMP_RUN
              point_name: 泵运行状态
              point_type: DI
            - point_id: HW_SEC_PUMP_FAULT
              point_name: 泵故障状态
              point_type: DI
          commands:
            - point_id: HW_SEC_PUMP_START_CMD
              point_name: 泵启停命令
              point_type: DO
          setpoints:
            - point_id: HW_SEC_PUMP_FREQ_SP
              point_name: 泵频率设定
              point_type: AO
              unit: Hz
              range: [25, 50]
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 锅炉房/换热站
          position: 分水器前端

      - node_id: HVAC-CHP_DST_HW_HEADER_S
        node_name: 热水供水分水器
        node_name_en: Hot Water Supply Header
        node_type: Distribution_Node
        node_subtype: SPL
        node_category: DST
      
        function: 热水供水分配至各区域主管
        medium_in: HW
        medium_out: HW
      
        equipment_parameters:
          type: 分水器
          diameter: {value: DN400, unit: mm}
          material: 无缝钢管
          outlets: {value: 6, unit: 路}
          pressure_rating: {value: 1.6, unit: MPa}
          insulation: {type: "橡塑保温", thickness: 60, unit: mm}
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 锅炉房/换热站
          position: 中央位置

      - node_id: HVAC-CHP_DST_HW_HEADER_R
        node_name: 热水回水集水器
        node_name_en: Hot Water Return Header
        node_type: Distribution_Node
        node_subtype: JUN
        node_category: DST
      
        function: 汇集各区域热水回水
        medium_in: HW
        medium_out: HW
      
        equipment_parameters:
          type: 集水器
          diameter: {value: DN400, unit: mm}
          material: 无缝钢管
          inlets: {value: 6, unit: 路}
          pressure_rating: {value: 1.6, unit: MPa}
          insulation: {type: "橡塑保温", thickness: 60, unit: mm}
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 锅炉房/换热站
          position: 中央位置

      # === 冷却水系统 ===
      - node_id: HVAC-CHP_DST_CW_PUMP
        node_name: 冷却水泵
        node_name_en: Condenser Water Pump
        node_type: Distribution_Node
        node_subtype: TRF
        node_category: DST
      
        function: 冷却塔与冷水机组之间冷却水循环
        medium_in: CW
        medium_out: CW
      
        multiplicity: multiple
        instance_pattern: HVAC-CHP_DST_CW_PUMP_{NN}
        typical_configuration:
          quantity: 4
          redundancy: "一机一泵+1公共备用"
          operation_mode: 与对应冷水机组联锁运行
      
        equipment_parameters:
          type: 卧式单级离心泵
          flow_rate: {value: 580, unit: "m³/h", note: "与冷水机组冷凝器配套"}
          head: {value: 28, unit: mH2O, note: "含冷却塔扬程+管路阻力"}
          power: {value: 55, unit: kW}
          efficiency: ">80%"
          motor_efficiency: "IE3"
          control_type: 工频运行（可选变频）
      
        control_points:
          status:
            - point_id: CW_PUMP_RUN
              point_name: 泵运行状态
              point_type: DI
            - point_id: CW_PUMP_FAULT
              point_name: 泵故障状态
              point_type: DI
          commands:
            - point_id: CW_PUMP_START_CMD
              point_name: 泵启停命令
              point_type: DO
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房
          position: 冷水机组冷凝器进水侧

      - node_id: HVAC-CHP_DST_COOLING_TOWER
        node_name: 冷却塔
        node_name_en: Cooling Tower
        node_type: Distribution_Node
        node_subtype: TRF
        node_category: DST
      
        function: 冷却水散热降温
        medium_in: CW
        medium_out: CW
      
        multiplicity: multiple
        instance_pattern: HVAC-CHP_DST_COOLING_TOWER_{NN}
        typical_configuration:
          quantity: 4
          redundancy: "N+1"
      
        equipment_parameters:
          type: 逆流式超低噪音冷却塔
          cooling_capacity: {value: 3500, unit: kW, note: "单台散热量"}
          flow_rate: {value: 580, unit: "m³/h"}
          inlet_temp: {value: 37, unit: ℃}
          outlet_temp: {value: 32, unit: ℃}
          wet_bulb_temp: {value: 28, unit: ℃, note: "设计湿球温度"}
          approach: {value: 4, unit: ℃, note: "逼近度"}
          fan_power: {value: 15, unit: kW}
          fan_type: 轴流风机（变频可选）
          noise_level: "<62dB(A)@15m"
          drift_loss: "<0.001%"
          fill_type: 高效波纹填料
          basin_volume: {value: 5000, unit: L}
      
        control_points:
          sensors:
            - point_id: CT_CW_OUT_TEMP
              point_name: 冷却塔出水温度
              point_type: AI
              unit: ℃
              range: [0, 50]
            - point_id: CT_CW_IN_TEMP
              point_name: 冷却塔进水温度
              point_type: AI
              unit: ℃
              range: [0, 50]
            - point_id: CT_FAN_FREQ
              point_name: 风机频率（变频时）
              point_type: AI
              unit: Hz
              range: [0, 50]
          status:
            - point_id: CT_FAN_RUN
              point_name: 冷却塔风机运行状态
              point_type: DI
            - point_id: CT_FAN_FAULT
              point_name: 冷却塔风机故障状态
              point_type: DI
            - point_id: CT_LOW_LEVEL
              point_name: 冷却塔低水位
              point_type: DI
            - point_id: CT_HIGH_LEVEL
              point_name: 冷却塔高水位
              point_type: DI
            - point_id: CT_OVERFLOW
              point_name: 冷却塔溢流
              point_type: DI
          commands:
            - point_id: CT_FAN_START_CMD
              point_name: 冷却塔风机启停命令
              point_type: DO
            - point_id: CT_MAKEUP_VALVE
              point_name: 补水电磁阀
              point_type: DO
          setpoints:
            - point_id: CT_CW_OUT_TEMP_SP
              point_name: 出水温度设定
              point_type: AO
              unit: ℃
              range: [22, 35]
              default: 32
      
        location_hint:
          space_type: OUTDOOR
          position: 裙房屋面
          area_requirement: {value: ">400", unit: "m²"}
          clearance: "塔间距≥1.5倍塔径"
      
        installation_requirements:
          - 远离新风口≥15m
          - 隔声屏障高度≥冷却塔高度
          - 排水设施完善（溢流、排污、冬季放空）
          - 防坠落措施（栏杆、检修平台）
          - 冬季防冻措施（电伴热、保温）
          - 定期清洗和消毒（军团菌控制）
      
        noise_control:
          equipment_noise: "<62dB(A)@15m"
          barrier_type: 复合型隔声屏障
          barrier_height: {value: 3, unit: m}
          barrier_insertion_loss: ">15dB(A)"

      # === 补水定压系统 ===
      - node_id: HVAC-CHP_DST_CHW_EXPANSION
        node_name: 冷冻水定压补水装置
        node_name_en: CHW Pressurization & Makeup Unit
        node_type: Distribution_Node
        node_subtype: BUF
        node_category: DST
      
        function: 冷冻水系统定压补水、膨胀吸收
        medium_in: WATER-SOFT
        medium_out: CHW
      
        equipment_parameters:
          type: 全自动定压补水装置（囊式）
          tank_volume: {value: 800, unit: L, note: "膨胀罐总容积"}
          makeup_pump_flow: {value: 5, unit: "m³/h"}
          makeup_pump_head: {value: 50, unit: mH2O}
          set_pressure: {value: 0.35, unit: MPa, note: "系统定压点"}
          pressure_range: {value: "0.30-0.40", unit: MPa}
          expansion_volume: {value: 400, unit: L, note: "有效膨胀容积"}
      
        control_points:
          sensors:
            - point_id: CHW_SYS_PRESS
              point_name: 冷冻水系统压力
              point_type: AI
              unit: MPa
              range: [0, 1.0]
            - point_id: CHW_MAKEUP_FLOW
              point_name: 补水流量（累计）
              point_type: AI
              unit: "m³"
          status:
            - point_id: CHW_MAKEUP_PUMP_RUN
              point_name: 补水泵运行状态
              point_type: DI
            - point_id: CHW_LOW_PRESS_ALARM
              point_name: 系统低压报警
              point_type: DI
            - point_id: CHW_HIGH_PRESS_ALARM
              point_name: 系统高压报警
              point_type: DI
            - point_id: CHW_MAKEUP_FAIL
              point_name: 补水失败报警
              point_type: DI
              note: 补水泵运行但压力不上升
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房
          position: 系统回水管最低点附近

      - node_id: HVAC-CHP_DST_HW_EXPANSION
        node_name: 热水定压补水装置
        node_name_en: HW Pressurization & Makeup Unit
        node_type: Distribution_Node
        node_subtype: BUF
        node_category: DST
      
        function: 热水系统定压补水、膨胀吸收
        medium_in: WATER-SOFT
        medium_out: HW
      
        equipment_parameters:
          type: 全自动定压补水装置（囊式）
          tank_volume: {value: 1000, unit: L, note: "热水膨胀量大"}
          makeup_pump_flow: {value: 5, unit: "m³/h"}
          makeup_pump_head: {value: 50, unit: mH2O}
          set_pressure: {value: 0.40, unit: MPa}
          pressure_range: {value: "0.35-0.45", unit: MPa}
          expansion_volume: {value: 500, unit: L}
      
        control_points:
          sensors:
            - point_id: HW_SYS_PRESS
              point_name: 热水系统压力
              point_type: AI
              unit: MPa
              range: [0, 1.0]
          status:
            - point_id: HW_MAKEUP_PUMP_RUN
              point_name: 补水泵运行状态
              point_type: DI
            - point_id: HW_LOW_PRESS_ALARM
              point_name: 系统低压报警
              point_type: DI
            - point_id: HW_HIGH_PRESS_ALARM
              point_name: 系统高压报警
              point_type: DI
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 锅炉房
          position: 系统回水管最低点附近

      # === 水处理系统 ===
      - node_id: HVAC-CHP_DST_CW_TREATMENT
        node_name: 冷却水水处理装置
        node_name_en: CW Water Treatment System
        node_type: Distribution_Node
        node_subtype: TRF
        node_category: DST
      
        function: 冷却水杀菌、除垢、缓蚀处理
        medium_in: CW
        medium_out: CW
      
        equipment_parameters:
          type: 全自动水处理装置
          treatment_methods:
            - 电化学除垢: "动态离子群水处理器"
            - 自动加药: "缓蚀阻垢剂+杀菌剂"
            - 旁滤净化: "砂滤器/自动排污"
          bypass_flow: {value: 50, unit: "m³/h", note: "旁滤流量约总流量的5-10%"}
          dosing_control: "ORP/电导率反馈控制"
      
        control_points:
          sensors:
            - point_id: CW_CONDUCTIVITY
              point_name: 冷却水电导率
              point_type: AI
              unit: "μS/cm"
              range: [0, 5000]
            - point_id: CW_PH
              point_name: 冷却水pH值
              point_type: AI
              range: [6, 9]
          status:
            - point_id: CW_DOSING_RUN
              point_name: 加药泵运行状态
              point_type: DI
            - point_id: CW_BLOWDOWN
              point_name: 排污阀状态
              point_type: DI
          commands:
            - point_id: CW_BLOWDOWN_CMD
              point_name: 排污命令
              point_type: DO
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 水处理间/冷冻机房
          position: 冷却水回水管旁路

    # ========================================
    # Sink Nodes - 消耗终端/边界输出节点
    # ========================================
    sink_nodes:
  
      - node_id: HVAC-CHP_SNK_CHW_RISER
        node_name: 冷冻水区域立管接口
        node_name_en: CHW Zone Riser Connection
        node_type: Sink_Node
        node_category: SNK
      
        function: 连接至各区域冷冻水立管（系统边界输出）
        medium_in: CHW
        medium_out: CHW
      
        is_boundary_output: true
        target_system: HVAC-CHW
      
        multiplicity: multiple
        instance_pattern: HVAC-CHP_SNK_CHW_RISER_{Zone}
        typical_quantity: {value: 8, unit: 路, note: "分区域供应"}
      
        interface_parameters:
          pipe_size: {value: "DN100-DN150", unit: mm}
          isolation_valve: {type: "电动蝶阀", note: "区域隔离"}
          balancing_valve: {type: "动态平衡阀", note: "流量平衡"}
          check_valve: true
          strainer: "Y型过滤器"
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房
          position: 分水器出口

      - node_id: HVAC-CHP_SNK_HW_RISER
        node_name: 热水区域立管接口
        node_name_en: HW Zone Riser Connection
        node_type: Sink_Node
        node_category: SNK
      
        function: 连接至各区域热水立管（系统边界输出）
        medium_in: HW
        medium_out: HW
      
        is_boundary_output: true
        target_system: HVAC-HW
      
        multiplicity: multiple
        instance_pattern: HVAC-CHP_SNK_HW_RISER_{Zone}
        typical_quantity: {value: 6, unit: 路}
      
        interface_parameters:
          pipe_size: {value: "DN80-DN125", unit: mm}
          isolation_valve: {type: "电动蝶阀"}
          balancing_valve: {type: "动态平衡阀"}
          check_valve: true
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 锅炉房/换热站
          position: 分水器出口

  # ========================================
  # EDGES SECTION - 边/连接定义
  # ========================================
  edges:

    # === 冷冻水供应路径边 ===
    chw_supply_edges:
  
      - edge_id: HVAC-CHP_EDGE_001
        edge_name: 冷水机组蒸发器出口至一次泵
        edge_type: TRK
        from_node: HVAC-CHP_SRC_CHILLER
        to_node: HVAC-CHP_DST_CHW_PRI_PUMP
        direction: unidirectional
        medium: CHW
        medium_state:
          temperature: {value: 7, unit: ℃}
          pressure: {value: 0.45, unit: MPa}
          flow_direction: supply
        pipe_parameters:
          material: 无缝钢管
          diameter: DN250
          insulation: {type: "橡塑保温", thickness: 50, unit: mm}
          velocity: {value: 2.0, unit: "m/s", note: "设计流速"}
      
      - edge_id: HVAC-CHP_EDGE_002
        edge_name: 一次泵出口至分水器
        edge_type: TRK
        from_node: HVAC-CHP_DST_CHW_PRI_PUMP
        to_node: HVAC-CHP_DST_CHW_HEADER_S
        direction: unidirectional
        medium: CHW
        pipe_parameters:
          material: 无缝钢管
          diameter: DN250
          insulation: {type: "橡塑保温", thickness: 50, unit: mm}

      - edge_id: HVAC-CHP_EDGE_003
        edge_name: 分水器至二次泵入口
        edge_type: TRK
        from_node: HVAC-CHP_DST_CHW_HEADER_S
        to_node: HVAC-CHP_DST_CHW_SEC_PUMP
        direction: unidirectional
        medium: CHW
        pipe_parameters:
          material: 无缝钢管
          diameter: DN300
          insulation: {type: "橡塑保温", thickness: 50, unit: mm}

      - edge_id: HVAC-CHP_EDGE_004
        edge_name: 二次泵出口至区域立管
        edge_type: BRH
        from_node: HVAC-CHP_DST_CHW_SEC_PUMP
        to_node: HVAC-CHP_SNK_CHW_RISER
        direction: unidirectional
        medium: CHW
        multiplicity: multiple
        pipe_parameters:
          material: 无缝钢管
          diameter: "DN100-DN150"
          insulation: {type: "橡塑保温", thickness: 40, unit: mm}

    # === 冷冻水回水路径边 ===
    chw_return_edges:
  
      - edge_id: HVAC-CHP_EDGE_011
        edge_name: 区域立管回水至集水器
        edge_type: BRH
        from_node: HVAC-CHP_SNK_CHW_RISER
        to_node: HVAC-CHP_DST_CHW_HEADER_R
        direction: unidirectional
        medium: CHW
        medium_state:
          temperature: {value: 12, unit: ℃}
          flow_direction: return
        multiplicity: multiple
        pipe_parameters:
          material: 无缝钢管
          diameter: "DN100-DN150"
          insulation: {type: "橡塑保温", thickness: 40, unit: mm}

      - edge_id: HVAC-CHP_EDGE_012
        edge_name: 集水器至冷水机组蒸发器入口
        edge_type: TRK
        from_node: HVAC-CHP_DST_CHW_HEADER_R
        to_node: HVAC-CHP_SRC_CHILLER
        direction: unidirectional
        medium: CHW
        pipe_parameters:
          material: 无缝钢管
          diameter: DN300
          insulation: {type: "橡塑保温", thickness: 50, unit: mm}

    # === 旁通路径边 ===
    bypass_edges:
  
      - edge_id: HVAC-CHP_EDGE_021
        edge_name: 分水器至旁通阀
        edge_type: BRH
        from_node: HVAC-CHP_DST_CHW_HEADER_S
        to_node: HVAC-CHP_DST_CHW_BYPASS
        direction: unidirectional
        medium: CHW
        pipe_parameters:
          diameter: DN200

      - edge_id: HVAC-CHP_EDGE_022
        edge_name: 旁通阀至集水器
        edge_type: BRH
        from_node: HVAC-CHP_DST_CHW_BYPASS
        to_node: HVAC-CHP_DST_CHW_HEADER_R
        direction: unidirectional
        medium: CHW
        pipe_parameters:
          diameter: DN200

    # === 热水供应路径边 ===
    hw_supply_edges:
  
      - edge_id: HVAC-CHP_EDGE_031
        edge_name: 锅炉出口至一次泵
        edge_type: TRK
        from_node: HVAC-CHP_SRC_BOILER
        to_node: HVAC-CHP_DST_HW_PRI_PUMP
        direction: unidirectional
        medium: HW
        medium_state:
          temperature: {value: 60, unit: ℃}
          pressure: {value: 0.4, unit: MPa}
          flow_direction: supply
        pipe_parameters:
          material: 无缝钢管
          diameter: DN200
          insulation: {type: "橡塑保温", thickness: 60, unit: mm}

      - edge_id: HVAC-CHP_EDGE_032
        edge_name: 一次泵至分水器
        edge_type: TRK
        from_node: HVAC-CHP_DST_HW_PRI_PUMP
        to_node: HVAC-CHP_DST_HW_HEADER_S
        direction: unidirectional
        medium: HW
        pipe_parameters:
          material: 无缝钢管
          diameter: DN200
          insulation: {type: "橡塑保温", thickness: 60, unit: mm}

      - edge_id: HVAC-CHP_EDGE_033
        edge_name: 分水器至二次泵
        edge_type: TRK
        from_node: HVAC-CHP_DST_HW_HEADER_S
        to_node: HVAC-CHP_DST_HW_SEC_PUMP
        direction: unidirectional
        medium: HW
        pipe_parameters:
          material: 无缝钢管
          diameter: DN250
          insulation: {type: "橡塑保温", thickness: 60, unit: mm}

      - edge_id: HVAC-CHP_EDGE_034
        edge_name: 二次泵至区域立管
        edge_type: BRH
        from_node: HVAC-CHP_DST_HW_SEC_PUMP
        to_node: HVAC-CHP_SNK_HW_RISER
        direction: unidirectional
        medium: HW
        multiplicity: multiple
        pipe_parameters:
          material: 无缝钢管
          diameter: "DN80-DN125"
          insulation: {type: "橡塑保温", thickness: 50, unit: mm}

    # === 热水回水路径边 ===
    hw_return_edges:
  
      - edge_id: HVAC-CHP_EDGE_041
        edge_name: 区域立管回水至集水器
        edge_type: BRH
        from_node: HVAC-CHP_SNK_HW_RISER
        to_node: HVAC-CHP_DST_HW_HEADER_R
        direction: unidirectional
        medium: HW
        medium_state:
          temperature: {value: 50, unit: ℃}
          flow_direction: return
        multiplicity: multiple
        pipe_parameters:
          material: 无缝钢管
          diameter: "DN80-DN125"
          insulation: {type: "橡塑保温", thickness: 50, unit: mm}

      - edge_id: HVAC-CHP_EDGE_042
        edge_name: 集水器至锅炉
        edge_type: TRK
        from_node: HVAC-CHP_DST_HW_HEADER_R
        to_node: HVAC-CHP_SRC_BOILER
        direction: unidirectional
        medium: HW
        pipe_parameters:
          material: 无缝钢管
          diameter: DN250
          insulation: {type: "橡塑保温", thickness: 60, unit: mm}

    # === 冷却水路径边 ===
    cw_edges:
  
      - edge_id: HVAC-CHP_EDGE_051
        edge_name: 冷水机组冷凝器出口至冷却水泵
        edge_type: TRK
        from_node: HVAC-CHP_SRC_CHILLER
        to_node: HVAC-CHP_DST_CW_PUMP
        direction: unidirectional
        medium: CW
        medium_state:
          temperature: {value: 37, unit: ℃}
          flow_direction: to_tower
        pipe_parameters:
          material: 无缝钢管
          diameter: DN300
          insulation: 无（室内段）

      - edge_id: HVAC-CHP_EDGE_052
        edge_name: 冷却水泵至冷却塔
        edge_type: TRK
        from_node: HVAC-CHP_DST_CW_PUMP
        to_node: HVAC-CHP_DST_COOLING_TOWER
        direction: unidirectional
        medium: CW
        pipe_parameters:
          material: 无缝钢管/镀锌钢管
          diameter: DN300
          insulation: 室外段保温（防冻）

      - edge_id: HVAC-CHP_EDGE_053
        edge_name: 冷却塔至冷水机组冷凝器入口
        edge_type: TRK
        from_node: HVAC-CHP_DST_COOLING_TOWER
        to_node: HVAC-CHP_SRC_CHILLER
        direction: unidirectional
        medium: CW
        medium_state:
          temperature: {value: 32, unit: ℃}
          flow_direction: from_tower
        pipe_parameters:
          material: 无缝钢管/镀锌钢管
          diameter: DN300
          insulation: 室外段保温（防冻）

    # === 补水路径边 ===
    makeup_edges:
  
      - edge_id: HVAC-CHP_EDGE_061
        edge_name: 软化水至冷冻水补水装置
        edge_type: TRM
        from_node: EXTERNAL_SOFTENED_WATER
        to_node: HVAC-CHP_DST_CHW_EXPANSION
        direction: unidirectional
        medium: WATER-SOFT
        is_boundary_edge: true
        pipe_parameters:
          diameter: DN40

      - edge_id: HVAC-CHP_EDGE_062
        edge_name: 冷冻水补水装置至系统回水
        edge_type: TRM
        from_node: HVAC-CHP_DST_CHW_EXPANSION
        to_node: HVAC-CHP_DST_CHW_HEADER_R
        direction: unidirectional
        medium: CHW
        pipe_parameters:
          diameter: DN50

      - edge_id: HVAC-CHP_EDGE_063
        edge_name: 软化水至热水补水装置
        edge_type: TRM
        from_node: EXTERNAL_SOFTENED_WATER
        to_node: HVAC-CHP_DST_HW_EXPANSION
        direction: unidirectional
        medium: WATER-SOFT
        is_boundary_edge: true
        pipe_parameters:
          diameter: DN40

      - edge_id: HVAC-CHP_EDGE_064
        edge_name: 热水补水装置至系统回水
        edge_type: TRM
        from_node: HVAC-CHP_DST_HW_EXPANSION
        to_node: HVAC-CHP_DST_HW_HEADER_R
        direction: unidirectional
        medium: HW
        pipe_parameters:
          diameter: DN50

  # ========================================
  # TYPICAL PATHS SECTION - 典型路径定义
  # ========================================
  typical_paths:

    - path_id: HVAC-CHP_PATH_CHW_SUPPLY
      path_name: 冷冻水供应主路径
      path_type: SUP
      description: 冷水机组至用户侧的冷冻水供应路径
      sequence:
        - step: 1
          node: HVAC-CHP_SRC_CHILLER
          action: 制取7℃冷冻水
        - step: 2
          node: HVAC-CHP_DST_CHW_PRI_PUMP
          action: 一次侧定流量循环
        - step: 3
          node: HVAC-CHP_DST_CHW_HEADER_S
          action: 供水汇集分配
        - step: 4
          node: HVAC-CHP_DST_CHW_SEC_PUMP
          action: 二次侧变频加压
        - step: 5
          node: HVAC-CHP_SNK_CHW_RISER
          action: 送至各区域立管
      operating_conditions:
        season: 夏季（5月-10月）
        supply_temp: {value: 7, unit: ℃, tolerance: ±0.5}
        return_temp: {value: 12, unit: ℃}
        delta_t: {value: 5, unit: ℃}
        design_flow: {value: 1400, unit: "m³/h"}

    - path_id: HVAC-CHP_PATH_CHW_RETURN
      path_name: 冷冻水回水主路径
      path_type: RET
      description: 用户侧回水至冷水机组的回水路径
      sequence:
        - step: 1
          node: HVAC-CHP_SNK_CHW_RISER
          action: 接收区域回水
        - step: 2
          node: HVAC-CHP_DST_CHW_HEADER_R
          action: 回水汇集
        - step: 3
          node: HVAC-CHP_SRC_CHILLER
          action: 回到蒸发器再冷却
      operating_conditions:
        return_temp: {value: 12, unit: ℃}

    - path_id: HVAC-CHP_PATH_HW_SUPPLY
      path_name: 热水供应主路径
      path_type: SUP
      description: 锅炉至用户侧的热水供应路径
      sequence:
        - step: 1
          node: HVAC-CHP_SRC_BOILER
          action: 制取60℃热水
        - step: 2
          node: HVAC-CHP_DST_HW_PRI_PUMP
          action: 一次侧定流量循环
        - step: 3
          node: HVAC-CHP_DST_HW_HEADER_S
          action: 供水汇集分配
        - step: 4
          node: HVAC-CHP_DST_HW_SEC_PUMP
          action: 二次侧变频加压
        - step: 5
          node: HVAC-CHP_SNK_HW_RISER
          action: 送至各区域立管
      operating_conditions:
        season: 冬季（11月-4月）
        supply_temp: {value: 60, unit: ℃}
        return_temp: {value: 50, unit: ℃}
        delta_t: {value: 10, unit: ℃}
        design_flow: {value: 520, unit: "m³/h"}

    - path_id: HVAC-CHP_PATH_CW_LOOP
      path_name: 冷却水循环路径
      path_type: LOOP
      description: 冷水机组冷凝器与冷却塔之间的冷却水循环
      sequence:
        - step: 1
          node: HVAC-CHP_SRC_CHILLER
          action: 冷凝器排热，出水37℃
        - step: 2
          node: HVAC-CHP_DST_CW_PUMP
          action: 冷却水循环泵送
        - step: 3
          node: HVAC-CHP_DST_COOLING_TOWER
          action: 蒸发散热降温至32℃
        - step: 4
          node: HVAC-CHP_SRC_CHILLER
          action: 回到冷凝器吸热
      operating_conditions:
        season: 夏季
        supply_temp: {value: 32, unit: ℃, note: "冷凝器进水"}
        return_temp: {value: 37, unit: ℃, note: "冷凝器出水"}
        delta_t: {value: 5, unit: ℃}

    - path_id: HVAC-CHP_PATH_CHW_BYPASS
      path_name: 冷冻水旁通路径
      path_type: BYP
      description: 一二次泵流量不平衡时的旁通调节
      sequence:
        - step: 1
          node: HVAC-CHP_DST_CHW_HEADER_S
          action: 供水侧富余流量
        - step: 2
          node: HVAC-CHP_DST_CHW_BYPASS
          action: 压差旁通调节
        - step: 3
          node: HVAC-CHP_DST_CHW_HEADER_R
          action: 汇入回水侧
      trigger_conditions:
        - 二次侧流量 < 一次侧流量
        - 分集水器压差 > 设定值（80kPa）
        - 一次泵流量接近机组最小流量限制

  # ========================================
  # LOOPS SECTION - 回路定义
  # ========================================
  loops:

    - loop_id: HVAC-CHP_LOOP_CHW_PRIMARY
      loop_name: 冷冻水一次侧回路
      loop_type: 定流量回路
      description: 冷水机组与分集水器之间的一次侧循环
      nodes_in_loop:
        - HVAC-CHP_SRC_CHILLER
        - HVAC-CHP_DST_CHW_PRI_PUMP
        - HVAC-CHP_DST_CHW_HEADER_S
        - HVAC-CHP_DST_CHW_HEADER_R
      loop_control_strategy:
        type: 定流量
        flow_setting: 与冷水机组额定流量匹配
        description: |
          一次泵与冷水机组一一对应联动运行
          运行台数由冷水机组决定
          确保冷水机组蒸发器流量稳定

    - loop_id: HVAC-CHP_LOOP_CHW_SECONDARY
      loop_name: 冷冻水二次侧回路
      loop_type: 变流量回路
      description: 分集水器至用户侧的二次循环
      nodes_in_loop:
        - HVAC-CHP_DST_CHW_HEADER_S
        - HVAC-CHP_DST_CHW_SEC_PUMP
        - HVAC-CHP_SNK_CHW_RISER
        - HVAC-CHP_DST_CHW_HEADER_R
      loop_control_strategy:
        type: 变流量-恒压差
        control_variable: 供回水压差（最不利环路末端）
        setpoint: {value: 100, unit: kPa, range: [80, 150]}
        pump_control: 变频调节
        description: |
          1. 根据系统最不利点压差反馈调节二次泵频率
          2. 末端需求减少时，流量降低，压差升高，降低泵频
          3. 末端需求增加时，流量增加，压差降低，提高泵频
          4. 可采用压差复位策略优化节能

    - loop_id: HVAC-CHP_LOOP_CHW_BYPASS
      loop_name: 冷冻水旁通回路
      loop_type: 压差平衡回路
      description: 一二次泵解耦旁通
      nodes_in_loop:
        - HVAC-CHP_DST_CHW_HEADER_S
        - HVAC-CHP_DST_CHW_BYPASS
        - HVAC-CHP_DST_CHW_HEADER_R
      bypass_control_logic:
        control_variable: 分集水器之间压差
        setpoint: {value: 80, unit: kPa, note: "参考值，需现场调试"}
        pid_parameters:
          kp: {value: 2.0, note: "参考值"}
          ki: {value: 0.3, note: "参考值"}
          kd: {value: 0}
        opening_direction: 压差升高→开大旁通
        constraint: |
          当一次侧总流量接近最小流量限制时，
          强制保持旁通阀开启，优先保证机组安全

    - loop_id: HVAC-CHP_LOOP_CW
      loop_name: 冷却水回路
      loop_type: 定流量/按需变流量
      description: 冷凝器与冷却塔之间的冷却水循环
      nodes_in_loop:
        - HVAC-CHP_SRC_CHILLER
        - HVAC-CHP_DST_CW_PUMP
        - HVAC-CHP_DST_COOLING_TOWER
      loop_control_strategy:
        type: 一机一泵联动
        description: |
          冷却水泵与对应冷水机组联锁运行
          可选用变频控制根据冷凝器进水温度调节流量
          过渡季节可降低冷却水流量节能

  # ========================================
  # CONTROL LOGIC SECTION - 控制逻辑定义
  # ========================================
  control_logic:

    # === 制冷系统启停顺序 ===
    cooling_system_startup_sequence:
      name: 制冷系统启动顺序
      mode: cooling
      preconditions:
        - 冷冻水系统压力正常（无低压报警）
        - 冷却水系统压力正常
        - 电源正常
        - 无系统故障报警
      sequence:
        - step: 1
          action: 启动冷却塔风机
          delay: 0s
          condition: null
          verification: CT_FAN_RUN = ON
        - step: 2
          action: 启动冷却水泵
          delay: 30s
          condition: 冷却塔风机运行确认
          verification: CW_PUMP_RUN = ON
        - step: 3
          action: 等待冷却水流量稳定
          delay: 60s
          condition: 冷却水流量>机组最小要求
          verification: 流量计确认
        - step: 4
          action: 启动冷水机组
          delay: 30s
          condition: 冷却水流量确认
          verification: CHILLER_RUN = ON
        - step: 5
          action: 启动冷冻水一次泵
          delay: 30s
          condition: 冷水机组运行确认
          verification: CHW_PRI_PUMP_RUN = ON
        - step: 6
          action: 启动冷冻水二次泵
          delay: 30s
          condition: 一次泵运行确认
          verification: CHW_SEC_PUMP_RUN = ON
        - step: 7
          action: 系统运行监测
          delay: 300s
          condition: 各设备运行正常
          verification: 冷冻水供水温度开始下降
  
    cooling_system_shutdown_sequence:
      name: 制冷系统停机顺序
      mode: cooling
      sequence:
        - step: 1
          action: 停止冷冻水二次泵
          delay: 0s
        - step: 2
          action: 停止冷冻水一次泵
          delay: 30s
          note: 等待管道水置换
        - step: 3
          action: 停止冷水机组
          delay: 30s
          note: 按机组内部停机程序
        - step: 4
          action: 继续运行冷却水泵
          delay: 120s
          note: 带走冷凝器余热
        - step: 5
          action: 停止冷却水泵
          delay: 0s
        - step: 6
          action: 停止冷却塔风机
          delay: 60s
          note: 降低塔内温度后停止

    # === 冷却塔与冷机联动控制（H2修复）===
    cooling_tower_chiller_coordination:
      name: 冷却塔-冷机协调控制
      description: 冷却塔运行与冷水机组的联动控制
    
      normal_operation:
        description: 正常运行联动
        logic: |
          1. 冷却塔风机/冷却水泵与对应冷水机组联锁
          2. 机组启动前，对应冷却塔先启动并确认运行
          3. 机组停止后，冷却塔延时停止以散余热
          4. 可根据冷凝器进水温度调节冷却塔出水温度
      
      temperature_control:
        description: 冷却水温度控制
        control_variable: 冷却塔出水温度（CT_CW_OUT_TEMP）
        setpoint: {value: 32, unit: ℃, range: [26, 35]}
        control_method: |
          1. 优先台数控制：运行机组增加时加开冷却塔
          2. 变频调速：风机变频根据出水温度调节
          3. 过渡季节可降低设定值提高冷机效率
      
      winter_protection:
        description: 冬季防冻保护
        trigger: 环境温度 < 5℃ 或 冷却水温度 < 10℃
        actions:
          - 开启电伴热
          - 启动冷却水循环（低速）防止冻结
          - 冷却塔布水系统排空
          - 紧急情况：关闭补水阀，系统放空
        alarm: 冷却水温度 < 5℃ 时发冻结预警

      fault_handling:
        description: 故障处理
        scenarios:
          - fault: 冷却塔风机故障
            action: |
              1. 报警并切换至备用冷却塔
              2. 若无备用，降低对应冷机负荷
              3. 冷凝器进水温度>38℃时，停止冷机
          - fault: 冷却水泵故障
            action: |
              1. 立即停止对应冷水机组
              2. 启动备用冷却水泵
              3. 确认流量正常后重启冷机

    # === 冷水机组台数控制 ===
    chiller_staging:
      name: 冷水机组台数控制
      control_logic: |
        1. 根据系统实际冷负荷计算需要的机组容量
        2. 机组加载条件：
           - 当前运行机组平均负载率 > 85%
           - 持续时间 > 15分钟
           - 有待机机组可用
        3. 机组卸载条件：
           - 当前运行机组平均负载率 < 50%
           - 持续时间 > 20分钟
           - 至少保留一台机组运行
        4. 机组轮换：
           - 累计运行时间均衡控制
           - 优先启用运行时间最短的机组
        5. 故障切换：
           - 机组故障时自动启用备用机组
           - 故障机组隔离，避免影响系统
    
      load_calculation:
        method: 供回水温差 × 流量
        formula: "Q = ρ × c × V × ΔT"
        unit: kW
    
      staging_table:
        - load_range: "0-30%"
          chillers_running: 1
          note: 单台变频运行
        - load_range: "30-60%"
          chillers_running: 2
          note: 双台均负荷
        - load_range: "60-90%"
          chillers_running: 3
          note: 三台均负荷
        - load_range: ">90%"
          chillers_running: 3
          note: 满负荷运行，必要时启用备用

    # === 二次泵变频控制 ===
    secondary_pump_control:
      name: 二次泵变频控制
      control_method: 恒压差控制
      control_variable: 系统最不利环路压差
      setpoint: {value: 100, unit: kPa}
      pid_parameters:
        kp: {value: 1.5, note: "参考值，需现场整定"}
        ki: {value: 0.1, note: "参考值"}
        kd: {value: 0}
      frequency_range: {min: 25, max: 50, unit: Hz}
    
      control_logic: |
        1. 实测压差 < 设定值 → 提高频率
        2. 实测压差 > 设定值 → 降低频率
        3. 最小频率限制25Hz，防止过低振动
        4. 泵组台数控制与频率控制配合
    
      pump_staging:
        description: 二次泵台数控制
        logic: |
          1. 单台泵频率接近50Hz且压差仍不足 → 加开一台泵
          2. 多台泵运行且频率<30Hz → 减少一台泵
          3. 保证至少一台泵运行
    
      pressure_reset_optimization:
        description: 压差设定值复位节能
        logic: |
          1. 监测末端阀门开度
          2. 当大部分阀门开度<70%，可降低压差设定
          3. 当有阀门开度>95%，需提高压差设定
          4. 压差设定范围：80-150kPa

    # === 旁通阀控制 ===
    bypass_valve_control:
      name: 旁通阀控制
      control_variable: 分集水器压差
      setpoint: {value: 80, unit: kPa}
    
      control_logic: |
        1. 监测分水器与集水器之间的压差
        2. 压差 > 设定值 → 开大旁通阀
        3. 压差 < 设定值 → 关小旁通阀
        4. 同时监测一次侧流量
    
      safety_interlock:
        description: 安全联锁
        logic: |
          1. 一次侧流量 < 机组最小流量×1.1 时
             → 强制开大旁通阀至50%以上
          2. 所有二次泵停止时
             → 旁通阀全开
          3. 一次泵停止时
             → 旁通阀关闭

    # === 供水温度复位 ===
    supply_temp_reset:
      name: 冷冻水供水温度复位
      description: 根据负荷动态调节冷冻水供水温度设定
    
      control_logic: |
        1. 监测AHU/FCU末端冷水阀平均开度
        2. 平均开度 < 60% 且持续30分钟 → 供水温度设定+0.5℃
        3. 平均开度 > 85% → 供水温度设定-0.5℃
        4. 供水温度范围：6-10℃
        5. 节能效益：供水温度每提高1℃，约节能3%
    
      constraints:
        - 供水温度不低于6℃（防止盘管结霜）
        - 供水温度不高于10℃（保证除湿能力）
        - 手术室、ICU等关键区域不参与复位

  # ========================================
  # ALARM & PROTECTION SECTION - 报警与保护
  # ========================================
  alarm_protection:
  
    critical_alarms:
      - alarm_id: ALM_CHILLER_TRIP
        alarm_name: 冷水机组跳闸
        severity: CRITICAL
        trigger: CHILLER_FAULT = ON
        action: 自动启用备用机组，通知维护人员
      
      - alarm_id: ALM_CW_HIGH_TEMP
        alarm_name: 冷凝器进水温度过高
        severity: HIGH
        trigger: CT_CW_OUT_TEMP > 38℃
        action: 增加冷却塔运行台数/风机转速，必要时限制冷机负荷
      
      - alarm_id: ALM_CHW_LOW_TEMP
        alarm_name: 冷冻水供水温度过低
        severity: HIGH
        trigger: CHILLER_CHWST < 5℃
        action: 提高供水温度设定，防止盘管结霜
      
      - alarm_id: ALM_SYS_LOW_PRESS
        alarm_name: 系统低压报警
        severity: HIGH
        trigger: CHW_SYS_PRESS < 0.20 MPa
        action: 启动补水泵，检查泄漏
      
    equipment_protection:
      chiller_protection:
        - 蒸发器防冻保护（出水温度<4℃停机）
        - 冷凝器高压保护
        - 电机过流保护
        - 润滑油压力保护
        - 冷冻水流量保护
      
      pump_protection:
        - 电机过载保护
        - 干运行保护（进口压力低）
        - 轴承温度监测
      
      boiler_protection:
        - 超温保护
        - 超压保护
        - 低水位保护
        - 火焰监测保护
        - 燃气泄漏保护

  # ========================================
  # DEPENDENCIES SECTION - 系统依赖关系
  # ========================================
  dependencies:
  
    upstream_dependencies:
      - dependency_id: DEP_ELEC
        from_system: ELEC-LV-MAIN
        dependency_type: POWER_SUPPLY
        criticality: CRITICAL
        description: 冷热源系统动力电源
        failure_impact: 系统完全停止运行
      
      - dependency_id: DEP_GAS
        from_system: EXTERNAL_GAS
        dependency_type: FUEL_SUPPLY
        criticality: HIGH
        description: 锅炉燃气供应
        failure_impact: 无法制热（仅影响供暖季）
      
      - dependency_id: DEP_WATER
        from_system: PLUMB-DWS
        dependency_type: MAKEUP_WATER
        criticality: MEDIUM
        description: 系统补水
        failure_impact: 短期可运行，长期需停机
      
      - dependency_id: DEP_BA
        from_system: INT-BA
        dependency_type: CONTROL_SIGNAL
        criticality: MEDIUM
        description: 监控和控制
        failure_impact: 可本地手动运行
      
    downstream_dependencies:
      - dependency_id: DEP_CHW
        to_system: HVAC-CHW
        dependency_type: CHILLED_WATER
        criticality: CRITICAL
        description: 冷冻水供应
      
      - dependency_id: DEP_HW
        to_system: HVAC-HW
        dependency_type: HOT_WATER
        criticality: CRITICAL
        description: 热水供应
```

---

## 系统 1.2: HVAC-CHW 冷冻水输配系统（第三版）

```yaml
System_Topology:

  identity:
    system_id: HVAC-CHW
    system_name: 冷冻水输配系统
    system_name_en: Chilled Water Distribution System
    system_category: HVAC
    system_type: 水系统-输配
    priority_level: P1-CRITICAL
  
    description: |
      医院冷冻水输配系统，负责将冷冻机房的冷冻水输送至各区域的空调末端设备。
      系统采用变流量控制，通过楼层/区域分支向各AHU、FCU供应7℃/12℃冷冻水。
      管网按建筑功能区划分为多个独立环路，便于分区控制和节能管理。
  
    design_basis:
      chw_design_temp: {supply: 7, return: 12, unit: ℃}
      design_pressure: {value: 0.4-0.5, unit: MPa}
      pipe_velocity: {riser: 1.5, branch: 1.0, unit: "m/s", note: "设计流速"}
  
    parent_system: HVAC-CHP
    child_systems:
      - HVAC-AHU
      - HVAC-FCU
      - HVAC-PAU
      - HVAC-CLEAN
  
    design_standards:
      - GB 50736-2012 民用建筑供暖通风与空气调节设计规范
      - GB 50189-2015 公共建筑节能设计标准
      - GB 51039-2014 综合医院建筑设计规范
  
    version: 3.0
    last_updated: 2024

  boundary:
    inputs:
      - boundary_id: HVAC-CHW_IN_001
        name: 冷冻水供水输入
        from_system: HVAC-CHP
        from_node: HVAC-CHP_SNK_CHW_RISER
        medium: CHW
        parameters:
          temperature: {value: 7, unit: ℃, tolerance: ±0.5}
          pressure: {value: 0.4-0.5, unit: MPa}
        
    outputs:
      - boundary_id: HVAC-CHW_OUT_001
        name: 冷冻水回水输出
        to_system: HVAC-CHP
        to_node: HVAC-CHP_DST_CHW_HEADER_R
        medium: CHW
        parameters:
          temperature: {value: 12, unit: ℃}
        
      - boundary_id: HVAC-CHW_OUT_002
        name: AHU冷冻水接口
        to_system: HVAC-AHU
        medium: CHW
      
      - boundary_id: HVAC-CHW_OUT_003
        name: FCU冷冻水接口
        to_system: HVAC-FCU
        medium: CHW
      
      - boundary_id: HVAC-CHW_OUT_004
        name: PAU冷冻水接口
        to_system: HVAC-PAU
        medium: CHW

  nodes:

    source_nodes:
  
      - node_id: HVAC-CHW_SRC_RISER_IN
        node_name: 冷冻水立管供水入口
        node_name_en: CHW Riser Supply Inlet
        node_type: Source_Node
        node_category: SRC
      
        function: 接收冷热源系统的冷冻水供水
        medium_in: CHW
        medium_out: CHW
      
        is_boundary_input: true
        source_system: HVAC-CHP
      
        multiplicity: multiple
        instance_pattern: HVAC-CHW_SRC_RISER_IN_{Zone}
        typical_quantity: {value: 8, unit: 路, note: "按分区"}
      
        equipment_parameters:
          pipe_size: {value: "DN100-DN150", unit: mm}
          isolation_valve: {type: "电动蝶阀", note: "区域隔离阀"}
          check_valve: true
          strainer: "Y型过滤器"
          pressure_gauge: true
          thermometer: true
        
        location_hint:
          space_type: SHAFT
          shaft_type: 空调水管井
          position: 每个区域立管底部（冷冻机房层）

    distribution_nodes:
  
      - node_id: HVAC-CHW_DST_RISER
        node_name: 冷冻水立管
        node_name_en: CHW Riser
        node_type: Distribution_Node
        node_subtype: TRK
        node_category: DST
      
        function: 垂直输送冷冻水至各楼层
        medium_in: CHW
        medium_out: CHW
      
        multiplicity: multiple
        instance_pattern: HVAC-CHW_DST_RISER_{Zone}_{S/R}
        note: S=供水立管, R=回水立管
      
        equipment_parameters:
          material: 无缝钢管
          diameter: {value: "DN100-DN150", unit: mm}
          insulation: {type: "橡塑保温", thickness: 40, unit: mm}
          support: 管道支架每层设置
          expansion_joint: 每3-4层设置补偿器
          drain_valve: 立管底部设置
          vent_valve: 立管顶部设置
        
        location_hint:
          space_type: SHAFT
          shaft_type: 空调水管井

      - node_id: HVAC-CHW_DST_FLOOR_HEADER
        node_name: 楼层分集水器
        node_name_en: Floor CHW Header
        node_type: Distribution_Node
        node_subtype: SPL
        node_category: DST
      
        function: 楼层冷冻水分配
        medium_in: CHW
        medium_out: CHW
      
        multiplicity: multiple
        instance_pattern: HVAC-CHW_DST_FLOOR_HEADER_{Floor}_{Zone}
      
        equipment_parameters:
          type: 分集水器/母管
          material: 无缝钢管
          diameter: {value: "DN80-DN100", unit: mm}
          outlets: {value: "4-8", unit: 路}
          insulation: {type: "橡塑保温", thickness: 30, unit: mm}
          balancing_valve: 各支路设置
          isolation_valve: 各支路设置
        
        location_hint:
          space_type: SHAFT
          shaft_type: 空调水管井
          position: 每层管井内

      - node_id: HVAC-CHW_DST_BRANCH
        node_name: 楼层水平支管
        node_name_en: Floor CHW Branch
        node_type: Distribution_Node
        node_subtype: BRH
        node_category: DST
      
        function: 楼层内冷冻水水平输配
        medium_in: CHW
        medium_out: CHW
      
        multiplicity: multiple
        instance_pattern: HVAC-CHW_DST_BRANCH_{Floor}_{Zone}_{Seq}
      
        equipment_parameters:
          material: 无缝钢管/镀锌钢管
          diameter: {value: "DN32-DN80", unit: mm}
          insulation: {type: "橡塑保温", thickness: 25, unit: mm}
          slope: {value: 0.003, note: "坡向泄水点"}
          support: 吊架/支架按规范间距
        
        location_hint:
          space_type: CEILING_VOID
          position: 走廊吊顶内
          clearance: {value: ">150", unit: mm, note: "与其他管线净距"}

      - node_id: HVAC-CHW_DST_BALANCING_VALVE
        node_name: 动态平衡阀
        node_name_en: Dynamic Balancing Valve
        node_type: Distribution_Node
        node_subtype: REG
        node_category: DST
      
        function: 各环路流量平衡调节
        medium_in: CHW
        medium_out: CHW
      
        multiplicity: multiple
        instance_pattern: HVAC-CHW_DST_BAL_VALVE_{Floor}_{Seq}
      
        equipment_parameters:
          type: 动态压差平衡阀
          diameter: {value: "DN25-DN80", unit: mm}
          differential_pressure_range: {value: "20-400", unit: kPa}
          flow_range: 根据环路设计流量选型
        
        control_points:
          sensors:
            - point_id: BAL_VALVE_FLOW
              point_name: 环路流量
              point_type: AI
              unit: "m³/h"
            - point_id: BAL_VALVE_DP
              point_name: 阀前后压差
              point_type: AI
              unit: kPa
            
        location_hint:
          space_type: CEILING_VOID
          position: 各立管分支处/环路入口

    sink_nodes:
  
      - node_id: HVAC-CHW_SNK_AHU_COIL
        node_name: 空调箱冷冻水盘管接口
        node_name_en: AHU Chilled Water Coil Connection
        node_type: Sink_Node
        node_category: SNK
      
        function: 连接至空调箱冷冻水盘管
        medium_in: CHW
        medium_out: CHW
      
        is_boundary_output: true
        target_system: HVAC-AHU
      
        multiplicity: multiple
        instance_pattern: HVAC-CHW_SNK_AHU_COIL_{Floor}_{Seq}
      
        interface_parameters:
          pipe_size: {value: "DN50-DN80", unit: mm}
          control_valve: {type: "电动二通阀", control: "比例调节"}
          isolation_valve: {type: "蝶阀/球阀", qty: 2}
          flexible_connection: 橡胶软接头
          thermometer: 供回水各一只
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 空调机房

      - node_id: HVAC-CHW_SNK_FCU_COIL
        node_name: 风机盘管冷冻水接口
        node_name_en: FCU Chilled Water Coil Connection
        node_type: Sink_Node
        node_category: SNK
      
        function: 连接至风机盘管冷冻水盘管
        medium_in: CHW
        medium_out: CHW
      
        is_boundary_output: true
        target_system: HVAC-FCU
      
        multiplicity: multiple
        instance_pattern: HVAC-CHW_SNK_FCU_COIL_{Floor}_{Room}
        typical_quantity: 大量（按房间数）
      
        interface_parameters:
          pipe_size: {value: "DN20-DN32", unit: mm}
          control_valve: {type: "电动二通阀/电热阀", control: "开关/比例"}
          isolation_valve: {type: "球阀", qty: 2}
          flexible_connection: 软管连接
        
        location_hint:
          space_type: CEILING_VOID
          position: 各功能房间吊顶内

      - node_id: HVAC-CHW_SNK_PAU_COIL
        node_name: 新风机组冷冻水盘管接口
        node_name_en: PAU Chilled Water Coil Connection
        node_type: Sink_Node
        node_category: SNK
      
        function: 连接至新风机组冷冻水盘管
        medium_in: CHW
        medium_out: CHW
      
        is_boundary_output: true
        target_system: HVAC-PAU
      
        multiplicity: multiple
        instance_pattern: HVAC-CHW_SNK_PAU_COIL_{Floor}_{Seq}
      
        interface_parameters:
          pipe_size: {value: "DN40-DN65", unit: mm}
          control_valve: {type: "电动二通阀", control: "比例调节"}
          isolation_valve: {type: "蝶阀", qty: 2}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 新风机房

      - node_id: HVAC-CHW_SNK_RISER_OUT
        node_name: 冷冻水立管回水出口
        node_name_en: CHW Riser Return Outlet
        node_type: Sink_Node
        node_category: SNK
      
        function: 冷冻水回水返回冷热源系统
        medium_in: CHW
        medium_out: CHW
      
        is_boundary_output: true
        target_system: HVAC-CHP
      
        multiplicity: multiple
        instance_pattern: HVAC-CHW_SNK_RISER_OUT_{Zone}
      
        equipment_parameters:
          pipe_size: {value: "DN100-DN150", unit: mm}
          check_valve: true
          thermometer: true
        
        location_hint:
          space_type: SHAFT
          shaft_type: 空调水管井
          position: 每个区域立管底部

  edges:

    supply_edges:
  
      - edge_id: HVAC-CHW_EDGE_001
        edge_name: 立管入口至立管
        edge_type: TRK
        from_node: HVAC-CHW_SRC_RISER_IN
        to_node: HVAC-CHW_DST_RISER
        direction: unidirectional
        medium: CHW
        pipe_parameters:
          material: 无缝钢管
          diameter: "DN100-DN150"
          insulation: {type: "橡塑保温", thickness: 40, unit: mm}
      
      - edge_id: HVAC-CHW_EDGE_002
        edge_name: 立管至楼层分水器
        edge_type: BRH
        from_node: HVAC-CHW_DST_RISER
        to_node: HVAC-CHW_DST_FLOOR_HEADER
        direction: unidirectional
        medium: CHW
        multiplicity: multiple
        pipe_parameters:
          material: 无缝钢管
          diameter: "DN65-DN100"
        
      - edge_id: HVAC-CHW_EDGE_003
        edge_name: 分水器至支管
        edge_type: BRH
        from_node: HVAC-CHW_DST_FLOOR_HEADER
        to_node: HVAC-CHW_DST_BRANCH
        direction: unidirectional
        medium: CHW
        multiplicity: multiple
        pipe_parameters:
          material: 无缝钢管/镀锌钢管
          diameter: "DN32-DN80"
        
      - edge_id: HVAC-CHW_EDGE_004
        edge_name: 支管至AHU接口
        edge_type: TRM
        from_node: HVAC-CHW_DST_BRANCH
        to_node: HVAC-CHW_SNK_AHU_COIL
        direction: unidirectional
        medium: CHW
        pipe_parameters:
          diameter: "DN50-DN80"
      
      - edge_id: HVAC-CHW_EDGE_005
        edge_name: 支管至FCU接口
        edge_type: TRM
        from_node: HVAC-CHW_DST_BRANCH
        to_node: HVAC-CHW_SNK_FCU_COIL
        direction: unidirectional
        medium: CHW
        multiplicity: multiple
        pipe_parameters:
          diameter: "DN20-DN32"
      
      - edge_id: HVAC-CHW_EDGE_006
        edge_name: 支管至PAU接口
        edge_type: TRM
        from_node: HVAC-CHW_DST_BRANCH
        to_node: HVAC-CHW_SNK_PAU_COIL
        direction: unidirectional
        medium: CHW
        pipe_parameters:
          diameter: "DN40-DN65"

    return_edges:
  
      - edge_id: HVAC-CHW_EDGE_011
        edge_name: AHU回水至支管
        edge_type: TRM
        from_node: HVAC-CHW_SNK_AHU_COIL
        to_node: HVAC-CHW_DST_BRANCH
        direction: unidirectional
        medium: CHW
        note: return_pipe
      
      - edge_id: HVAC-CHW_EDGE_012
        edge_name: FCU回水至支管
        edge_type: TRM
        from_node: HVAC-CHW_SNK_FCU_COIL
        to_node: HVAC-CHW_DST_BRANCH
        direction: unidirectional
        medium: CHW
        note: return_pipe
        multiplicity: multiple
      
      - edge_id: HVAC-CHW_EDGE_013
        edge_name: PAU回水至支管
        edge_type: TRM
        from_node: HVAC-CHW_SNK_PAU_COIL
        to_node: HVAC-CHW_DST_BRANCH
        direction: unidirectional
        medium: CHW
        note: return_pipe
      
      - edge_id: HVAC-CHW_EDGE_014
        edge_name: 支管回水至集水器
        edge_type: BRH
        from_node: HVAC-CHW_DST_BRANCH
        to_node: HVAC-CHW_DST_FLOOR_HEADER
        direction: unidirectional
        medium: CHW
        note: return_pipe
        multiplicity: multiple
      
      - edge_id: HVAC-CHW_EDGE_015
        edge_name: 集水器至立管回水
        edge_type: TRK
        from_node: HVAC-CHW_DST_FLOOR_HEADER
        to_node: HVAC-CHW_DST_RISER
        direction: unidirectional
        medium: CHW
        note: return_pipe
      
      - edge_id: HVAC-CHW_EDGE_016
        edge_name: 立管回水至出口
        edge_type: TRK
        from_node: HVAC-CHW_DST_RISER
        to_node: HVAC-CHW_SNK_RISER_OUT
        direction: unidirectional
        medium: CHW
        note: return_pipe

  typical_paths:

    - path_id: HVAC-CHW_PATH_TO_AHU
      path_name: 冷冻水至空调箱路径
      path_type: SUP
      description: 从冷冻机房至空调箱的冷冻水供应路径
      sequence:
        - step: 1
          node: HVAC-CHW_SRC_RISER_IN
          action: 接收冷热源供水
        - step: 2
          node: HVAC-CHW_DST_RISER
          action: 垂直向上输送
        - step: 3
          node: HVAC-CHW_DST_FLOOR_HEADER
          action: 楼层分配
        - step: 4
          node: HVAC-CHW_DST_BRANCH
          action: 水平输送
        - step: 5
          node: HVAC-CHW_SNK_AHU_COIL
          action: 送达AHU盘管
      design_parameters:
        supply_temp: {value: 7, unit: ℃}
        return_temp: {value: 12, unit: ℃}
        pressure_drop: {value: "<100", unit: kPa, note: "管网阻力"}

    - path_id: HVAC-CHW_PATH_TO_FCU
      path_name: 冷冻水至风机盘管路径
      path_type: SUP
      sequence:
        - step: 1
          node: HVAC-CHW_SRC_RISER_IN
          action: 接收冷热源供水
        - step: 2
          node: HVAC-CHW_DST_RISER
          action: 垂直向上输送
        - step: 3
          node: HVAC-CHW_DST_FLOOR_HEADER
          action: 楼层分配
        - step: 4
          node: HVAC-CHW_DST_BRANCH
          action: 水平输送
        - step: 5
          node: HVAC-CHW_SNK_FCU_COIL
          action: 送达FCU盘管

    - path_id: HVAC-CHW_PATH_RETURN
      path_name: 冷冻水回水路径
      path_type: RET
      sequence:
        - step: 1
          node: HVAC-CHW_SNK_FCU_COIL / HVAC-CHW_SNK_AHU_COIL
          action: 末端回水
        - step: 2
          node: HVAC-CHW_DST_BRANCH
          action: 支管汇集
        - step: 3
          node: HVAC-CHW_DST_FLOOR_HEADER
          action: 楼层汇集
        - step: 4
          node: HVAC-CHW_DST_RISER
          action: 垂直向下输送
        - step: 5
          node: HVAC-CHW_SNK_RISER_OUT
          action: 返回冷冻机房
```

---

## 系统 1.3: HVAC-PAU 新风机组系统（第三版，含新风比控制）

```yaml
System_Topology:

  identity:
    system_id: HVAC-PAU
    system_name: 新风机组系统
    system_name_en: Primary Air Unit System / Fresh Air Unit System
    system_category: HVAC
    system_type: 风系统
    priority_level: P1-CRITICAL
  
    description: |
      医院新风机组系统，负责处理室外新风并送至各区域。
      新风经过过滤、冷却/加热、除湿/加湿处理后，送至风机盘管系统或直接送入房间。
      是保证医院室内空气品质、压力控制和感染控制的关键系统。
  
    design_basis:
      fresh_air_standard: "GB 50736-2012 表4.2.4"
      minimum_fresh_air: {hospital: 30, unit: "m³/(h·人)", note: "医院门诊/病房"}
      pressure_control: {corridor: "+5Pa", ward: "0Pa", note: "相对走廊"}
  
    parent_system: HVAC-CHW / HVAC-HW
    child_systems:
      - HVAC-FCU
  
    design_standards:
      - GB 50736-2012 民用建筑供暖通风与空气调节设计规范
      - GB 51039-2014 综合医院建筑设计规范
      - WS/

# Agent-01 系统拓扑建模师 - 完整输出文档（续）

## 系统 1.3: HVAC-PAU 新风机组系统（第三版，续）

```yaml
    design_standards:
      - GB 50736-2012 民用建筑供暖通风与空气调节设计规范
      - GB 51039-2014 综合医院建筑设计规范
      - WS/T 508-2016 医院医用织物洗涤消毒技术规范
      - GB 50333-2013 医院洁净手术部建筑技术规范
  
    version: 3.0
    revision_notes: |
      v3.0: 补充新风比控制、与FCU协调控制、压力梯度维持
      v2.0: 完善控制点定义
      v1.0: 初始版本
    last_updated: 2024

  boundary:
    inputs:
      - boundary_id: HVAC-PAU_IN_001
        name: 室外新风
        from_system: EXTERNAL
        medium: AIR-OA
        parameters:
          condition: 室外状态（变化）
          design_summer: {db: 35.5, wb: 28.2, unit: ℃, note: "夏季设计工况"}
          design_winter: {db: -5, rh: 60, unit: "℃/%", note: "冬季设计工况"}
      
      - boundary_id: HVAC-PAU_IN_002
        name: 冷冻水供水
        from_system: HVAC-CHW
        from_node: HVAC-CHW_SNK_PAU_COIL
        medium: CHW
        parameters:
          temperature: {value: 7, unit: ℃}
      
      - boundary_id: HVAC-PAU_IN_003
        name: 热水供水
        from_system: HVAC-HW
        from_node: HVAC-HW_SNK_PAU_COIL
        medium: HW
        parameters:
          temperature: {value: 60, unit: ℃}
      
      - boundary_id: HVAC-PAU_IN_004
        name: 加湿用水/蒸汽
        from_system: PLUMB-HWS / STEAM
        medium: WATER-PW / STEAM
        parameters:
          type: 纯水加湿/蒸汽加湿
      
    outputs:
      - boundary_id: HVAC-PAU_OUT_001
        name: 处理后新风至FCU
        to_system: HVAC-FCU
        to_node: HVAC-FCU_SRC_OA_IN
        medium: AIR-SA
        parameters:
          temperature: {summer: 15, winter: 20, unit: ℃, note: "送风状态点"}
          humidity: {value: 60-70, unit: "%RH", note: "夏季除湿后"}
        
      - boundary_id: HVAC-PAU_OUT_002
        name: 处理后新风直送房间
        to_system: 空调房间
        medium: AIR-SA

  nodes:

    source_nodes:
  
      - node_id: HVAC-PAU_SRC_OA_INTAKE
        node_name: 新风采集口
        node_name_en: Outdoor Air Intake
        node_type: Source_Node
        node_category: SRC
      
        function: 采集室外新风
        medium_in: AIR-OA
        medium_out: AIR-OA
      
        multiplicity: multiple
        instance_pattern: HVAC-PAU_SRC_OA_INTAKE_{Floor}_{Seq}
      
        equipment_parameters:
          type: 防雨百叶风口
          material: 铝合金/不锈钢
          mesh: 不锈钢防虫网（40目）
          finish: 氟碳喷涂
          free_area_ratio: ">60%"
        
        location_hint:
          space_type: EXTERIOR
          position: 建筑外墙
          height_requirement: {value: ">3", unit: m, note: "距地面高度"}
          orientation: 背风侧优先
      
        installation_requirements:
          - 远离排风口≥10m（水平距离）
          - 远离冷却塔≥15m
          - 远离污染源（垃圾房、停车场入口等）
          - 距地面>3m或距屋面>1.5m
          - 避开建筑主入口正上方
          - 预留清洗检修通道

    distribution_nodes:
  
      - node_id: HVAC-PAU_DST_PAU
        node_name: 新风机组
        node_name_en: Primary Air Unit
        node_type: Distribution_Node
        node_subtype: TRF
        node_category: DST
      
        function: 新风处理（过滤、调温调湿）
        medium_in: [AIR-OA, CHW, HW, WATER-PW]
        medium_out: AIR-SA
      
        multiplicity: multiple
        instance_pattern: HVAC-PAU_DST_PAU_{Floor}_{Seq}
        typical_quantity: {value: "2-4", unit: "台/层", note: "按服务区域"}
      
        equipment_parameters:
          type: 全新风处理机组（立式/卧式）
          air_volume: {value: "3000-20000", unit: "m³/h", note: "按服务区域需求"}
          external_static_pressure: {value: "400-700", unit: Pa}
          sections:
            - name: 新风段
              function: 新风入口、电动风阀
            - name: 初效过滤段
              filter_class: G4
              filter_type: 板式/袋式
            - name: 中效过滤段
              filter_class: F7
              filter_type: 袋式
            - name: 表冷段
              rows: 6-8排
              fin_pitch: 2.0mm
              face_velocity: "<2.5m/s"
            - name: 加热段
              rows: 2-4排
              type: 热水盘管
            - name: 加湿段
              type: 干蒸汽加湿/电极加湿/湿膜加湿
              capacity: 按冬季设计湿负荷
            - name: 高效过滤段
              filter_class: H13 (可选)
              note: 洁净区域适用
            - name: 送风机段
              fan_type: 后向离心/EC风机
              efficiency: ">75%"
            - name: 消声段
              type: 阻性消声器
              insertion_loss: ">15dB(A)"
          motor_power: {value: "5.5-30", unit: kW}
          vfd: true
          heat_recovery: 
            type: 转轮式/板式（可选）
            efficiency: ">70%"
            note: 节能方案
      
        control_points:
          sensors:
            - point_id: PAU_SAT
              point_name: 送风温度
              point_type: AI
              unit: ℃
              range: [0, 50]
              accuracy: ±0.3℃
            - point_id: PAU_SAH
              point_name: 送风湿度
              point_type: AI
              unit: "%RH"
              range: [0, 100]
            - point_id: PAU_OAT
              point_name: 新风温度
              point_type: AI
              unit: ℃
              range: [-20, 50]
            - point_id: PAU_OAH
              point_name: 新风湿度
              point_type: AI
              unit: "%RH"
            - point_id: PAU_FILTER_DP_1
              point_name: 初效过滤器压差
              point_type: AI
              unit: Pa
              range: [0, 300]
            - point_id: PAU_FILTER_DP_2
              point_name: 中效过滤器压差
              point_type: AI
              unit: Pa
              range: [0, 400]
            - point_id: PAU_FAN_FREQ
              point_name: 风机频率
              point_type: AI
              unit: Hz
              range: [0, 50]
            - point_id: PAU_SA_FLOW
              point_name: 送风量
              point_type: AI
              unit: "m³/h"
            - point_id: PAU_DUCT_PRESS
              point_name: 送风静压
              point_type: AI
              unit: Pa
              range: [0, 1000]
          status:
            - point_id: PAU_FAN_RUN
              point_name: 风机运行状态
              point_type: DI
            - point_id: PAU_FAN_FAULT
              point_name: 风机故障状态
              point_type: DI
            - point_id: PAU_FILTER_ALARM
              point_name: 过滤器堵塞报警
              point_type: DI
            - point_id: PAU_FREEZE_ALARM
              point_name: 防冻报警
              point_type: DI
          commands:
            - point_id: PAU_FAN_START_CMD
              point_name: 风机启停命令
              point_type: DO
            - point_id: PAU_OA_DAMPER
              point_name: 新风阀开度
              point_type: AO
              unit: "%"
              range: [0, 100]
            - point_id: PAU_CHW_VALVE
              point_name: 冷水阀开度
              point_type: AO
              unit: "%"
              range: [0, 100]
            - point_id: PAU_HW_VALVE
              point_name: 热水阀开度
              point_type: AO
              unit: "%"
              range: [0, 100]
            - point_id: PAU_HUMID_CMD
              point_name: 加湿量控制
              point_type: AO
              unit: "%"
              range: [0, 100]
          setpoints:
            - point_id: PAU_SAT_SP
              point_name: 送风温度设定
              point_type: AO
              unit: ℃
              range: [12, 28]
              default: {summer: 15, winter: 20}
            - point_id: PAU_SAH_SP
              point_name: 送风湿度设定
              point_type: AO
              unit: "%RH"
              range: [40, 70]
            - point_id: PAU_FLOW_SP
              point_name: 送风量设定
              point_type: AO
              unit: "m³/h"
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 新风机房
          floor: 各楼层或设备层
          area_requirement: {value: ">20", unit: "m²/台"}
          ceiling_height: {value: ">3.5", unit: m}
      
        noise_control:
          equipment_noise: "<80dB(A)@1m"
          duct_silencer: 送风管消声器
          room_treatment: 机房吸声处理
          vibration_isolation: 弹簧减振器+软接

      - node_id: HVAC-PAU_DST_SA_DUCT_MAIN
        node_name: 新风主风管
        node_name_en: Fresh Air Main Duct
        node_type: Distribution_Node
        node_subtype: TRK
        node_category: DST
      
        function: 新风主管输送
        medium_in: AIR-SA
        medium_out: AIR-SA
      
        multiplicity: multiple
        instance_pattern: HVAC-PAU_DST_SA_DUCT_MAIN_{Floor}_{Seq}
      
        equipment_parameters:
          type: 镀锌钢板风管
          thickness: {value: "0.75-1.0", unit: mm}
          insulation: {type: "橡塑保温", thickness: 25, unit: mm, note: "外保温"}
          air_velocity: {value: "6-8", unit: "m/s", note: "设计风速"}
          sealing_class: B级
        
        location_hint:
          space_type: CEILING_VOID
          position: 主走廊吊顶内
          clearance: {value: ">100", unit: mm}

      - node_id: HVAC-PAU_DST_SA_DUCT_BRANCH
        node_name: 新风支风管
        node_name_en: Fresh Air Branch Duct
        node_type: Distribution_Node
        node_subtype: BRH
        node_category: DST
      
        function: 新风支管分配至各房间/FCU
        medium_in: AIR-SA
        medium_out: AIR-SA
      
        multiplicity: multiple
        instance_pattern: HVAC-PAU_DST_SA_DUCT_BRANCH_{Floor}_{Zone}_{Seq}
      
        equipment_parameters:
          type: 镀锌钢板风管
          thickness: {value: "0.6-0.75", unit: mm}
          insulation: {type: "橡塑保温", thickness: 20, unit: mm}
          air_velocity: {value: "4-6", unit: "m/s"}
        
        location_hint:
          space_type: CEILING_VOID
          position: 房间吊顶内

      - node_id: HVAC-PAU_DST_OA_DAMPER
        node_name: 新风定风量阀
        node_name_en: Fresh Air CAV Damper
        node_type: Distribution_Node
        node_subtype: REG
        node_category: DST
      
        function: 各房间新风量恒定控制
        medium_in: AIR-SA
        medium_out: AIR-SA
      
        multiplicity: multiple
        instance_pattern: HVAC-PAU_DST_OA_DAMPER_{Floor}_{Room}
      
        equipment_parameters:
          type: 定风量阀(CAV)
          flow_range: {value: "50-500", unit: "m³/h"}
          pressure_independence_range: {value: "50-300", unit: Pa}
          accuracy: ±10%
        
        control_points:
          sensors:
            - point_id: CAV_FLOW
              point_name: 实际风量
              point_type: AI
              unit: "m³/h"
          setpoints:
            - point_id: CAV_FLOW_SP
              point_name: 设定风量
              point_type: AO
              unit: "m³/h"
      
        location_hint:
          space_type: CEILING_VOID
          position: 各房间新风入口

    sink_nodes:
  
      - node_id: HVAC-PAU_SNK_FCU_OA
        node_name: FCU新风接口
        node_name_en: FCU Fresh Air Connection
        node_type: Sink_Node
        node_category: SNK
      
        function: 新风送至FCU混合
        medium_in: AIR-SA
        medium_out: AIR-SA
      
        is_boundary_output: true
        target_system: HVAC-FCU
      
        multiplicity: multiple
        instance_pattern: HVAC-PAU_SNK_FCU_OA_{Floor}_{Room}
        typical_quantity: 大量（按FCU数量）
      
        equipment_parameters:
          connection_type: 送风软管/静压箱
          duct_size: {value: "φ100-φ150", unit: mm}
          flexible_duct_length: {value: "<2", unit: m}
        
        location_hint:
          space_type: CEILING_VOID
          position: FCU新风接口处

      - node_id: HVAC-PAU_SNK_SA_DIFFUSER
        node_name: 新风直送送风口
        node_name_en: Fresh Air Supply Diffuser
        node_type: Sink_Node
        node_category: SNK
      
        function: 新风直接送入房间（无FCU区域）
        medium_in: AIR-SA
        medium_out: AIR-SA (to room)
      
        is_boundary_output: true
      
        multiplicity: multiple
        instance_pattern: HVAC-PAU_SNK_SA_DIFFUSER_{Floor}_{Room}_{Seq}
      
        equipment_parameters:
          type: 散流器/条缝风口/置换通风口
          material: 铝合金
          adjustable: true
        
        location_hint:
          space_type: CEILING
          position: 各功能房间天花

  edges:

    supply_edges:
      - edge_id: HVAC-PAU_EDGE_001
        edge_name: 新风口至PAU
        edge_type: TRK
        from_node: HVAC-PAU_SRC_OA_INTAKE
        to_node: HVAC-PAU_DST_PAU
        direction: unidirectional
        medium: AIR-OA
        duct_parameters:
          type: 镀锌钢板风管
          insulation: 橡塑保温30mm
      
      - edge_id: HVAC-PAU_EDGE_002
        edge_name: PAU至新风主管
        edge_type: TRK
        from_node: HVAC-PAU_DST_PAU
        to_node: HVAC-PAU_DST_SA_DUCT_MAIN
        direction: unidirectional
        medium: AIR-SA
      
      - edge_id: HVAC-PAU_EDGE_003
        edge_name: 主管至支管
        edge_type: BRH
        from_node: HVAC-PAU_DST_SA_DUCT_MAIN
        to_node: HVAC-PAU_DST_SA_DUCT_BRANCH
        direction: unidirectional
        medium: AIR-SA
        multiplicity: multiple
      
      - edge_id: HVAC-PAU_EDGE_004
        edge_name: 支管至定风量阀
        edge_type: TRM
        from_node: HVAC-PAU_DST_SA_DUCT_BRANCH
        to_node: HVAC-PAU_DST_OA_DAMPER
        direction: unidirectional
        medium: AIR-SA
        multiplicity: multiple
      
      - edge_id: HVAC-PAU_EDGE_005
        edge_name: 定风量阀至FCU接口
        edge_type: TRM
        from_node: HVAC-PAU_DST_OA_DAMPER
        to_node: HVAC-PAU_SNK_FCU_OA
        direction: unidirectional
        medium: AIR-SA
        multiplicity: multiple
      
      - edge_id: HVAC-PAU_EDGE_006
        edge_name: 支管至新风送风口
        edge_type: TRM
        from_node: HVAC-PAU_DST_SA_DUCT_BRANCH
        to_node: HVAC-PAU_SNK_SA_DIFFUSER
        direction: unidirectional
        medium: AIR-SA
        multiplicity: multiple

  typical_paths:

    - path_id: HVAC-PAU_PATH_TO_FCU
      path_name: 新风至FCU路径
      path_type: SUP
      description: 新风处理后送至FCU与回风混合
      sequence:
        - step: 1
          node: HVAC-PAU_SRC_OA_INTAKE
          action: 采集室外新风
        - step: 2
          node: HVAC-PAU_DST_PAU
          action: 过滤、调温调湿处理
        - step: 3
          node: HVAC-PAU_DST_SA_DUCT_MAIN
          action: 主风管输送
        - step: 4
          node: HVAC-PAU_DST_SA_DUCT_BRANCH
          action: 支风管分配
        - step: 5
          node: HVAC-PAU_DST_OA_DAMPER
          action: 定风量控制
        - step: 6
          node: HVAC-PAU_SNK_FCU_OA
          action: 送达FCU新风接口
      operating_conditions:
        summer:
          outdoor: {db: 35, wb: 28, unit: ℃}
          supply: {db: 15, rh: 90, unit: "℃/%RH"}
        winter:
          outdoor: {db: -5, rh: 60, unit: "℃/%RH"}
          supply: {db: 20, rh: 50, unit: "℃/%RH"}

    - path_id: HVAC-PAU_PATH_DIRECT
      path_name: 新风直送房间路径
      path_type: SUP
      description: 新风处理后直接送入房间（无FCU区域）
      sequence:
        - step: 1
          node: HVAC-PAU_SRC_OA_INTAKE
          action: 采集室外新风
        - step: 2
          node: HVAC-PAU_DST_PAU
          action: 过滤、调温调湿处理
        - step: 3
          node: HVAC-PAU_DST_SA_DUCT_MAIN
          action: 主风管输送
        - step: 4
          node: HVAC-PAU_DST_SA_DUCT_BRANCH
          action: 支风管分配
        - step: 5
          node: HVAC-PAU_SNK_SA_DIFFUSER
          action: 送风口送入房间

  # ========================================
  # CONTROL LOGIC SECTION - 控制逻辑（H3修复）
  # ========================================
  control_logic:

    # === 新风比控制（H3核心修复）===
    fresh_air_ratio_control:
      name: 新风比控制
      description: PAU送风量与FCU系统的配合控制
    
      design_parameters:
        minimum_fresh_air_ratio: 
          value: 30
          unit: "%"
          note: 最小新风比，保证卫生要求
        typical_fresh_air_ratio:
          value: 50
          unit: "%"
          note: 常规运行新风比
        maximum_fresh_air_ratio:
          value: 100
          unit: "%"
          note: 过渡季全新风运行
    
      fresh_air_calculation:
        method: 按人员数量或面积计算
        per_person: {value: 30, unit: "m³/(h·人)", note: "医院标准"}
        per_area: {value: 5, unit: "m³/(h·m²)", note: "备选方法"}
      
      control_logic: |
        1. 新风量设定：
           - 按房间设计人数计算最小新风量
           - 医院病房：30 m³/(h·人)
           - 医院门诊：30 m³/(h·人)
           - 手术室：按换气次数要求
      
        2. 新风比动态调节：
           - 过渡季（新风温度15-22℃）：可增大新风比至100%
           - 夏季/冬季：维持最小新风比30%
           - CO2浓度>1000ppm时：增大新风量
      
        3. 与FCU协调：
           - 新风温度设定应略低于FCU送风温度设定
           - 夏季：新风送风温度15℃，FCU送风温度18-20℃
           - 冬季：新风送风温度20℃，FCU送风温度35-40℃
      
        4. 联动逻辑：
           - FCU全部停止时，PAU维持最小风量运行
           - FCU启动时，PAU增加风量至设计值

    # === 与FCU协调控制 ===
    pau_fcu_coordination:
      name: PAU与FCU协调控制
      description: 新风机组与风机盘管的协调运行
    
      temperature_coordination:
        description: 温度协调
        logic: |
          1. 新风承担部分室内负荷（约30-50%）
          2. 夏季：
             - PAU送风温度设定：15℃（露点送风）
             - FCU送风温度设定：18-20℃
             - 新风已除湿，FCU主要承担显热负荷
          3. 冬季：
             - PAU送风温度设定：20℃
             - FCU送风温度设定：35-40℃
             - 新风预热，避免冷风直吹

      humidity_coordination:
        description: 湿度协调
        logic: |
          1. 夏季除湿主要由PAU完成
          2. 新风处理至露点温度以下（约14℃）
          3. FCU盘管无需除湿，避免凝水
          4. 冬季加湿由PAU统一完成

      flow_coordination:
        description: 风量协调
        logic: |
          1. 房间新风量 = CAV阀设定风量
          2. FCU回风量 = FCU总风量 - 新风量
          3. 新风比 = 新风量 / FCU总风量 × 100%
          4. 典型配置：
             - FCU风量：500 m³/h
             - 新风量：150-200 m³/h
             - 新风比：30-40%

    # === 房间压力控制 ===
    pressure_control:
      name: 房间压力梯度控制
      description: 维持医院不同区域的压力梯度
    
      pressure_hierarchy:
        description: 医院压力梯度设计
        zones:
          - zone: 走廊/公共区
            pressure: "+5 Pa"
            relative_to: 室外
            note: 正压防止室外污染进入
          - zone: 普通病房
            pressure: "0 Pa"
            relative_to: 走廊
            note: 与走廊平压
          - zone: 污染区（负压病房）
            pressure: "-10 Pa"
            relative_to: 走廊
            note: 负压隔离，防止污染扩散
          - zone: 洁净区（手术室）
            pressure: "+10 ~ +25 Pa"
            relative_to: 走廊
            note: 正压保护，洁净等级不同压差不同
    
      control_logic: |
        1. 新风量 > 排风量 → 正压
        2. 新风量 < 排风量 → 负压
        3. 通过调节新风量和排风量维持压差
        4. 压差传感器实时监测
        5. 门窗开启时压差会波动，控制器需滤波处理
    
      control_points:
        - point_id: ROOM_DP
          point_name: 房间压差
          point_type: AI
          unit: Pa
          range: [-30, 30]
        - point_id: ROOM_DP_SP
          point_name: 压差设定值
          point_type: AO
          unit: Pa

    # === 送风温度控制 ===
    supply_air_temp_control:
      name: PAU送风温度控制
      control_variable: 送风温度 (PAU_SAT)
    
      summer_mode:
        setpoint: {value: 15, unit: ℃, range: [12, 18]}
        control_method: 调节冷水阀开度
        pid_parameters:
          kp: {value: 2.0, note: "参考值"}
          ki: {value: 0.2}
          kd: {value: 0}
        note: 送至露点以完成除湿
      
      winter_mode:
        setpoint: {value: 20, unit: ℃, range: [18, 25]}
        control_method: 调节热水阀开度
        pid_parameters:
          kp: {value: 2.0}
          ki: {value: 0.2}
          kd: {value: 0}
        note: 预热新风，避免冷风直吹

      transition_mode:
        condition: 新风温度在15-22℃之间
        control_method: |
          1. 优先自然冷却（免费冷源）
          2. 关闭或最小开度冷/热水阀
          3. 利用新风直接送风
        energy_saving: 显著节能效果

    # === 送风湿度控制 ===
    supply_humidity_control:
      name: PAU送风湿度控制
      control_variable: 送风湿度 (PAU_SAH)
    
      summer_mode:
        method: 冷却除湿
        logic: |
          1. 新风经冷水盘管冷却至露点以下
          2. 送风相对湿度约90-95%（饱和状态）
          3. 绝对湿度已降低，进入房间后升温，相对湿度下降
      
      winter_mode:
        method: 蒸汽/电极加湿
        setpoint: {value: 50, unit: "%RH", range: [40, 60]}
        logic: |
          1. 监测送风湿度
          2. 湿度低于设定值时开启加湿
          3. 比例调节加湿量
        protection:
          - 送风管湿度>80%时停止加湿
          - 加湿器故障保护

    # === 风机变频控制 ===
    fan_speed_control:
      name: PAU风机变频控制
      control_method: 恒静压/恒风量
    
      constant_static_pressure:
        description: 恒静压控制
        control_variable: 送风管静压
        setpoint: {value: 150, unit: Pa, range: [100, 300]}
        logic: |
          1. 监测送风管末端静压
          2. 静压低于设定值→提高风机频率
          3. 静压高于设定值→降低风机频率
          4. 频率范围：25-50Hz
      
      constant_airflow:
        description: 恒风量控制（备选）
        control_variable: 送风量
        logic: |
          1. 监测送风管风量（风速×截面积）
          2. 维持设计风量稳定
          3. 风量不足时提高频率

    # === 防冻保护 ===
    freeze_protection:
      name: 冬季防冻保护
      trigger_conditions:
        - 新风温度 < 5℃
        - 盘管后温度 < 8℃
    
      protection_actions:
        - step: 1
          action: 新风阀关至最小（10%）
        - step: 2
          action: 热水阀开至100%
        - step: 3
          action: 启动循环泵（如有）
        - step: 4
          condition: 盘管后温度 < 5℃
          action: 关闭新风阀，停止风机
          note: 紧急停机
        - step: 5
          action: 报警通知维护人员
    
      recovery:
        condition: 新风温度 > 8℃ 且 盘管后温度 > 15℃
        action: 恢复正常运行

    # === 过滤器管理 ===
    filter_management:
      name: 过滤器状态监测与更换提醒
    
      monitoring:
        - filter: 初效过滤器
          alarm_dp: {value: 200, unit: Pa}
          action: 提醒更换
        - filter: 中效过滤器
          alarm_dp: {value: 300, unit: Pa}
          action: 提醒更换
        - filter: 高效过滤器
          alarm_dp: {value: 400, unit: Pa}
          action: 提醒更换
    
      maintenance_schedule:
        - filter: 初效
          cycle: 1-2个月检查/更换
        - filter: 中效
          cycle: 3-6个月更换
        - filter: 高效
          cycle: 1-2年更换

  # ========================================
  # DEPENDENCIES SECTION - 依赖关系
  # ========================================
  dependencies:
  
    upstream_dependencies:
      - dependency_id: DEP_CHW
        from_system: HVAC-CHW
        dependency_type: CHILLED_WATER
        criticality: HIGH
        description: 夏季冷却除湿用冷冻水
        failure_impact: 无法制冷除湿
      
      - dependency_id: DEP_HW
        from_system: HVAC-HW
        dependency_type: HOT_WATER
        criticality: HIGH
        description: 冬季加热用热水
        failure_impact: 无法加热，可能导致防冻报警
      
      - dependency_id: DEP_ELEC
        from_system: ELEC-LV-MAIN
        dependency_type: POWER_SUPPLY
        criticality: CRITICAL
        description: 风机电源
        failure_impact: 完全停止运行
      
    downstream_dependencies:
      - dependency_id: DEP_FCU
        to_system: HVAC-FCU
        dependency_type: FRESH_AIR
        criticality: HIGH
        description: 向FCU提供处理后的新风
      
      - dependency_id: DEP_ROOM
        to_system: 空调房间
        dependency_type: FRESH_AIR
        criticality: CRITICAL
        description: 保证室内空气品质
```

---

## 系统 1.4: HVAC-FCU 风机盘管系统（第三版）

```yaml
System_Topology:

  identity:
    system_id: HVAC-FCU
    system_name: 风机盘管系统
    system_name_en: Fan Coil Unit System
    system_category: HVAC
    system_type: 风系统-末端
    priority_level: P2-IMPORTANT
  
    description: |
      医院风机盘管系统，用于病房、诊室、办公室等小空间的分散式空调。
      风机盘管接收冷/热水和处理后的新风，为房间提供个性化空调控制。
      采用两管制或四管制系统，支持房间独立温度控制。
  
    design_basis:
      system_type: 新风+FCU系统
      water_system: 两管制/四管制
      fresh_air_source: HVAC-PAU
      fresh_air_ratio: {value: "30-50", unit: "%"}
  
    parent_system: HVAC-CHW / HVAC-HW / HVAC-PAU
  
    design_standards:
      - GB 50736-2012 民用建筑供暖通风与空气调节设计规范
      - GB 51039-2014 综合医院建筑设计规范
      - JGJ/T 177-2009 公共建筑节能检测标准
  
    version: 3.0
    revision_notes: |
      v3.0: 补充与PAU的新风配比协调控制
      v2.0: 完善控制点定义
      v1.0: 初始版本
    last_updated: 2024

  boundary:
    inputs:
      - boundary_id: HVAC-FCU_IN_001
        name: 冷冻水供水
        from_system: HVAC-CHW
        from_node: HVAC-CHW_SNK_FCU_COIL
        medium: CHW
        parameters:
          temperature: {value: 7, unit: ℃}
      
      - boundary_id: HVAC-FCU_IN_002
        name: 热水供水（四管制）
        from_system: HVAC-HW
        from_node: HVAC-HW_SNK_FCU_COIL
        medium: HW
        parameters:
          temperature: {value: 60, unit: ℃}
        optional: true  # 两管制时无此输入
      
      - boundary_id: HVAC-FCU_IN_003
        name: 处理后新风
        from_system: HVAC-PAU
        from_node: HVAC-PAU_SNK_FCU_OA
        medium: AIR-SA
        parameters:
          temperature: {summer: 15, winter: 20, unit: ℃}
          humidity: {summer: 90, winter: 50, unit: "%RH"}
      
    outputs:
      - boundary_id: HVAC-FCU_OUT_001
        name: 送风至房间
        to_system: 空调房间
        medium: AIR-SA
        parameters:
          temperature: {summer: 18, winter: 35, unit: ℃}

  nodes:

    source_nodes:
  
      - node_id: HVAC-FCU_SRC_CHW_IN
        node_name: 冷冻水供水接口
        node_name_en: CHW Supply Connection
        node_type: Source_Node
        node_category: SRC
      
        function: 接收冷冻水
        medium_in: CHW
        medium_out: CHW
      
        is_boundary_input: true
        source_system: HVAC-CHW
      
        multiplicity: multiple
        instance_pattern: HVAC-FCU_SRC_CHW_IN_{Floor}_{Room}
      
        equipment_parameters:
          pipe_size: {value: "DN20-DN32", unit: mm}
          isolation_valve: 球阀
          strainer: Y型过滤器
          flexible_connection: 软管
        
        location_hint:
          space_type: CEILING_VOID
          position: FCU水管接口处

      - node_id: HVAC-FCU_SRC_HW_IN
        node_name: 热水供水接口
        node_name_en: HW Supply Connection
        node_type: Source_Node
        node_category: SRC
      
        function: 接收热水（四管制时）
        medium_in: HW
        medium_out: HW
      
        is_boundary_input: true
        source_system: HVAC-HW
        optional: true  # 两管制时无此节点
      
        multiplicity: multiple
        instance_pattern: HVAC-FCU_SRC_HW_IN_{Floor}_{Room}
      
        equipment_parameters:
          pipe_size: {value: "DN20-DN32", unit: mm}
          isolation_valve: 球阀
        
        location_hint:
          space_type: CEILING_VOID

      - node_id: HVAC-FCU_SRC_OA_IN
        node_name: 新风接口
        node_name_en: Fresh Air Connection
        node_type: Source_Node
        node_category: SRC
      
        function: 接收PAU处理后的新风
        medium_in: AIR-SA
        medium_out: AIR-SA
      
        is_boundary_input: true
        source_system: HVAC-PAU
      
        multiplicity: multiple
        instance_pattern: HVAC-FCU_SRC_OA_IN_{Floor}_{Room}
      
        equipment_parameters:
          connection_type: 软管连接
          duct_size: {value: "φ100-φ150", unit: mm}
        
        location_hint:
          space_type: CEILING_VOID
          position: FCU新风入口

    distribution_nodes:
  
      - node_id: HVAC-FCU_DST_FCU
        node_name: 风机盘管
        node_name_en: Fan Coil Unit
        node_type: Distribution_Node
        node_subtype: TRF
        node_category: DST
      
        function: 房间空气冷却/加热，与新风混合后送出
        medium_in: [CHW, HW, AIR-RA, AIR-SA]
        medium_out: AIR-SA
      
        multiplicity: multiple
        instance_pattern: HVAC-FCU_DST_FCU_{Floor}_{Room}
        typical_quantity: 大量（按房间数）
      
        equipment_parameters:
          type: 卧式暗装风机盘管
          installation: 吊顶内暗装
          cooling_capacity: {value: "2.5-7.1", unit: kW, note: "常用规格"}
          heating_capacity: {value: "3.0-8.5", unit: kW}
          total_air_volume: {value: "340-1700", unit: "m³/h"}
          fan_speed: 三档调速（高/中/低）
          coil_type: 两管制/四管制
          coil_rows: {value: "2-3", unit: 排}
          water_pressure_drop: {value: "20-40", unit: kPa}
          noise_level: {value: "<38", unit: "dB(A)", note: "中档"}
          power: {value: "30-120", unit: W}
      
        operating_mode:
          fresh_air_ratio:
            description: 新风与回风比例
            typical_values:
              fresh_air: {value: "30-40", unit: "%"}
              return_air: {value: "60-70", unit: "%"}
            note: 新风由PAU处理后送入，与室内回风混合
        
          summer_mode:
            description: 夏季制冷模式
            fcu_supply_temp: {value: 18, unit: ℃}
            fresh_air_temp: {value: 15, unit: ℃, note: "PAU送风"}
            room_temp_setpoint: {value: 26, unit: ℃}
          
          winter_mode:
            description: 冬季制热模式
            fcu_supply_temp: {value: 35, unit: ℃}
            fresh_air_temp: {value: 20, unit: ℃}
            room_temp_setpoint: {value: 20, unit: ℃}
      
        control_points:
          sensors:
            - point_id: FCU_ROOM_TEMP
              point_name: 房间温度
              point_type: AI
              unit: ℃
              range: [0, 40]
              accuracy: ±0.5℃
              location: 房间墙面（高度1.5m）
            - point_id: FCU_ROOM_HUMIDITY
              point_name: 房间湿度
              point_type: AI
              unit: "%RH"
              range: [0, 100]
              optional: true
          status:
            - point_id: FCU_RUN
              point_name: FCU运行状态
              point_type: DI
            - point_id: FCU_FAN_SPEED_FB
              point_name: 风机档位反馈
              point_type: AI
              unit: "档位"
              values: [0, 1, 2, 3]  # 0=停，1=低，2=中，3=高
          commands:
            - point_id: FCU_ON_OFF
              point_name: FCU启停
              point_type: DO
            - point_id: FCU_FAN_SPEED
              point_name: 风机档位设定
              point_type: AO
              unit: "档位"
              range: [0, 3]
            - point_id: FCU_CHW_VALVE
              point_name: 冷水阀控制
              point_type: AO  # 比例阀
              unit: "%"
              range: [0, 100]
              alternatives:
                - point_type: DO  # 开关阀
                  note: 电热阀/电磁阀
            - point_id: FCU_HW_VALVE
              point_name: 热水阀控制
              point_type: AO
              unit: "%"
              range: [0, 100]
              optional: true  # 四管制时有效
          setpoints:
            - point_id: FCU_ROOM_TEMP_SP
              point_name: 房间温度设定
              point_type: AO
              unit: ℃
              range: [18, 28]
              default: {summer: 26, winter: 20}
      
        location_hint:
          space_type: CEILING_VOID
          position: 房间吊顶内
          clearance: {value: ">300", unit: mm, note: "维修空间"}
          access_panel: 需设检修口
          alternatives:
            - type: 立式明装
              position: 窗下地面
              space_type: ROOM_FLOOR
            - type: 卡式
              position: 吊顶中央
              space_type: CEILING

    sink_nodes:
  
      - node_id: HVAC-FCU_SNK_SA_OUTLET
        node_name: FCU送风口
        node_name_en: FCU Supply Air Outlet
        node_type: Sink_Node
        node_category: SNK
      
        function: 向房间送风
        medium_in: AIR-SA
        medium_out: AIR-SA (to room)
      
        is_boundary_output: true
      
        multiplicity: multiple
        instance_pattern: HVAC-FCU_SNK_SA_OUTLET_{Floor}_{Room}
      
        equipment_parameters:
          type: 条缝风口/百叶风口/散流器
          material: 铝合金
          finish: 静电喷涂（白色）
          adjustable: true
          size: 与FCU匹配
      
        location_hint:
          space_type: CEILING
          position: FCU送风侧

      - node_id: HVAC-FCU_SNK_RA_INLET
        node_name: FCU回风口
        node_name_en: FCU Return Air Inlet
        node_type: Sink_Node
        node_category: SNK
      
        function: 房间回风吸入
        medium_in: AIR-RA (from room)
        medium_out: AIR-RA
      
        multiplicity: multiple
        instance_pattern: HVAC-FCU_SNK_RA_INLET_{Floor}_{Room}
      
        equipment_parameters:
          type: 回风格栅/FCU面板回风口
          filter: G3初效过滤网
        
        location_hint:
          space_type: CEILING
          position: FCU回风侧/独立回风口

      - node_id: HVAC-FCU_SNK_CHW_OUT
        node_name: 冷冻水回水接口
        node_name_en: CHW Return Connection
        node_type: Sink_Node
        node_category: SNK
      
        function: 冷冻水回水至系统
        medium_in: CHW
        medium_out: CHW
      
        is_boundary_output: true
        target_system: HVAC-CHW
      
        multiplicity: multiple
      
        equipment_parameters:
          pipe_size: {value: "DN20-DN32", unit: mm}
        
        location_hint:
          space_type: CEILING_VOID

  edges:

    water_edges:
      - edge_id: HVAC-FCU_EDGE_001
        edge_name: 冷水供水至FCU
        edge_type: TRM
        from_node: HVAC-FCU_SRC_CHW_IN
        to_node: HVAC-FCU_DST_FCU
        direction: unidirectional
        medium: CHW
        pipe_parameters:
          diameter: "DN20-DN32"
          material: PPR/镀锌钢管
      
      - edge_id: HVAC-FCU_EDGE_002
        edge_name: FCU冷水回水
        edge_type: TRM
        from_node: HVAC-FCU_DST_FCU
        to_node: HVAC-FCU_SNK_CHW_OUT
        direction: unidirectional
        medium: CHW
        note: return

    air_edges:
      - edge_id: HVAC-FCU_EDGE_011
        edge_name: 新风至FCU
        edge_type: TRM
        from_node: HVAC-FCU_SRC_OA_IN
        to_node: HVAC-FCU_DST_FCU
        direction: unidirectional
        medium: AIR-SA
        note: 处理后新风与回风混合
      
      - edge_id: HVAC-FCU_EDGE_012
        edge_name: 回风至FCU
        edge_type: TRM
        from_node: HVAC-FCU_SNK_RA_INLET
        to_node: HVAC-FCU_DST_FCU
        direction: unidirectional
        medium: AIR-RA
      
      - edge_id: HVAC-FCU_EDGE_013
        edge_name: FCU至送风口
        edge_type: TRM
        from_node: HVAC-FCU_DST_FCU
        to_node: HVAC-FCU_SNK_SA_OUTLET
        direction: unidirectional
        medium: AIR-SA

  typical_paths:

    - path_id: HVAC-FCU_PATH_AIR
      path_name: FCU送风路径
      path_type: SUP
      description: 新风与回风混合、调温后送入房间
      sequence:
        - step: 1
          node: HVAC-FCU_SRC_OA_IN
          action: 接收PAU处理后的新风
          parameters:
            flow_ratio: "30-40%"
            temperature: {summer: 15, winter: 20, unit: ℃}
        - step: 2
          node: HVAC-FCU_SNK_RA_INLET
          action: 室内回风吸入
          parameters:
            flow_ratio: "60-70%"
            temperature: 室温
        - step: 3
          node: HVAC-FCU_DST_FCU
          action: 新风与回风混合，经盘管调温
          parameters:
            mixing: 新风+回风混合
            coil_duty: 调节混合空气温度
        - step: 4
          node: HVAC-FCU_SNK_SA_OUTLET
          action: 调温后空气送入房间
          parameters:
            temperature: {summer: 18, winter: 35, unit: ℃}

  control_logic:

    room_temperature_control:
      name: 房间温度控制
      control_variable: 房间温度 (FCU_ROOM_TEMP)
    
      control_logic: |
        1. 比较房间温度与设定值
        2. 温度偏差控制水阀开度：
           - 夏季：温度高于设定值→开大冷水阀
           - 冬季：温度低于设定值→开大热水阀
        3. 两管制系统季节切换：
           - 夏季（5-10月）：供冷水
           - 冬季（11-4月）：供热水
           - 过渡季：可关闭水阀，仅用新风
        4. 四管制系统自动选择：
           - 同时有冷热水可用
           - 根据需求自动切换
    
      pid_parameters:
        valve_control:
          kp: {value: 3.0, note: "参考值"}
          ki: {value: 0.5}
          kd: {value: 0}
    
      dead_band:
        value: 1
        unit: ℃
        note: 避免频繁切换

    fan_speed_control:
      name: 风机档位控制
      control_logic: |
        1. 根据温度偏差和负荷调节档位
        2. 自动模式：
           - 偏差大→高档
           - 偏差小→低档
           - 接近设定值→中档或低档
        3. 手动模式：用户选择固定档位
        4. 夜间/睡眠模式：强制低档
    
      noise_consideration:
        description: 医院应优先低噪音运行
        priority: 低档 > 中档 > 高档
        exception: 温度偏差过大时可用高档快速响应

    occupancy_control:
      name: 人员感应控制
      description: 根据房间占用状态调节运行
    
      control_logic: |
        1. 人体感应器/门窗传感器检测
        2. 无人且持续30分钟：
           - 切换至节能模式
           - 降低风机档位或停机
           - 温度设定放宽2-3℃
        3. 有人时：
           - 恢复正常运行
           - 快速响应调回设定温度
        4. 配合门窗开关联动：
           - 窗户开启→停机或降档
           - 窗户关闭→恢复运行
    
      control_points:
        - point_id: OCCUPANCY_SENSOR
          point_name: 人员感应器
          point_type: DI
        - point_id: WINDOW_SWITCH
          point_name: 窗户开关
          point_type: DI

    fresh_air_coordination:
      name: 与新风系统协调（H3修复）
      description: FCU与PAU新风的协调控制
    
      coordination_logic: |
        1. 新风量由PAU系统定风量阀控制
        2. FCU回风量 = FCU总风量 - 新风量
        3. 新风与回风在FCU内混合
        4. 新风温度应略低于房间目标温度：
           - 夏季：新风15℃，房间设定26℃
           - 冬季：新风20℃，房间设定20℃
        5. 夏季新风已除湿，FCU无需除湿
        6. PAU故障时FCU可独立运行（纯回风）
    
      failure_mode:
        pau_fault:
          description: PAU故障时FCU运行策略
          action: |
            1. FCU继续运行（纯回风模式）
            2. 报警通知维护人员
            3. 室内CO2浓度可能升高
            4. 建议人员开窗通风

    valve_protection:
      name: 水阀保护
      protection_logic: |
        1. 夏季防凝露：
           - 监测盘管表面温度
           - 接近露点时减小冷水阀开度
           - 设置凝水盘和排水
        2. 冬季防冻：
           - 室温<5℃时开启热水阀
           - 防止盘管冻裂
        3. 阀门故障：
           - 阀门开度反馈异常报警
           - 阀门卡死检测

  dependencies:
  
    upstream_dependencies:
      - dependency_id: DEP_CHW
        from_system: HVAC-CHW
        dependency_type: CHILLED_WATER
        criticality: HIGH
        description: 夏季制冷用冷冻水
      
      - dependency_id: DEP_HW
        from_system: HVAC-HW
        dependency_type: HOT_WATER
        criticality: HIGH
        description: 冬季制热用热水
      
      - dependency_id: DEP_PAU
        from_system: HVAC-PAU
        dependency_type: FRESH_AIR
        criticality: HIGH
        description: 处理后的新风供应
        failure_impact: 室内空气品质下降，CO2升高
      
      - dependency_id: DEP_ELEC
        from_system: ELEC-LV-MAIN
        dependency_type: POWER_SUPPLY
        criticality: MEDIUM
        description: FCU风机电源
        failure_impact: FCU停止运行
      
    downstream_dependencies:
      - dependency_id: DEP_ROOM
        to_system: 空调房间
        dependency_type: CONDITIONED_AIR
        criticality: HIGH
        description: 向房间提供空调效果
```

---

## 系统 1.5: HVAC-AHU 空调箱系统（第三版，简化版）

```yaml
System_Topology:

  identity:
    system_id: HVAC-AHU
    system_name: 空调箱系统
    system_name_en: Air Handling Unit System
    system_category: HVAC
    system_type: 风系统
    priority_level: P1-CRITICAL
  
    description: |
      医院组合式空调箱系统，用于公共区域（门诊大厅、医技楼、手术部等）的集中空调。
      空调箱负责空气的过滤、冷却/加热、加湿、送风处理。
      系统采用全新风/回风混合模式，配备变频风机进行风量调节。
  
    parent_system: HVAC-CHW / HVAC-HW
  
    version: 3.0
    last_updated: 2024

  boundary:
    inputs:
      - boundary_id: HVAC-AHU_IN_001
        name: 室外新风
        from_system: EXTERNAL
        medium: AIR-OA
      
      - boundary_id: HVAC-AHU_IN_002
        name: 室内回风
        from_system: 空调区域
        medium: AIR-RA
      
      - boundary_id: HVAC-AHU_IN_003
        name: 冷冻水供水
        from_system: HVAC-CHW
        medium: CHW
      
      - boundary_id: HVAC-AHU_IN_004
        name: 热水供水
        from_system: HVAC-HW
        medium: HW
      
    outputs:
      - boundary_id: HVAC-AHU_OUT_001
        name: 送风
        to_system: 空调区域
        medium: AIR-SA
      
      - boundary_id: HVAC-AHU_OUT_002
        name: 排风
        to_system: EXTERNAL
        medium: AIR-EA

  nodes:

    source_nodes:
  
      - node_id: HVAC-AHU_SRC_OA_INTAKE
        node_name: 新风采集口
        node_name_en: Outdoor Air Intake
        node_type: Source_Node
        node_category: SRC
      
        function: 采集室外新风
        medium_in: AIR-OA
        medium_out: AIR-OA
      
        multiplicity: multiple
        instance_pattern: HVAC-AHU_SRC_OA_INTAKE_{Floor}_{Seq}
      
        equipment_parameters:
          type: 防雨百叶风口
          material: 铝合金
          mesh: 防虫网
      
        location_hint:
          space_type: EXTERIOR
          position: 建筑外墙/屋面
          height_requirement: ">3m from ground"
      
        installation_requirements:
          - 远离排风口≥10m
          - 远离冷却塔≥15m
          - 远离污染源

      - node_id: HVAC-AHU_SRC_RA_GRILLE
        node_name: 回风口
        node_name_en: Return Air Grille
        node_type: Source_Node
        node_category: SRC
      
        function: 采集室内回风
        medium_in: AIR-RA
        medium_out: AIR-RA
      
        multiplicity: multiple
        instance_pattern: HVAC-AHU_SRC_RA_GRILLE_{Floor}_{Zone}_{Seq}
      
        equipment_parameters:
          type: 回风格栅/回风口
          material: 铝合金
        
        location_hint:
          space_type: CEILING
          position: 空调区域天花

    distribution_nodes:
  
      - node_id: HVAC-AHU_DST_AHU
        node_name: 组合式空调箱
        node_name_en: Air Handling Unit
        node_type: Distribution_Node
        node_subtype: TRF
        node_category: DST
      
        function: 空气处理（过滤、冷却/加热、加湿）
        medium_in: [AIR-OA, AIR-RA, CHW, HW]
        medium_out: AIR-SA
      
        multiplicity: multiple
        instance_pattern: HVAC-AHU_DST_AHU_{Floor}_{Seq}
      
        equipment_parameters:
          type: 组合式空调箱
          air_volume: {value: "5000-50000", unit: "m³/h"}
          external_static_pressure: {value: "400-800", unit: Pa}
          sections:
            - 新回风混合段
            - 初效过滤段(G4)
            - 表冷/加热段
            - 加湿段
            - 中效过滤段(F7)
            - 送风机段
            - 消声段
          fan_type: 后向离心风机/EC风机
          motor_power: {value: "5.5-55", unit: kW}
          vfd: true
      
        control_points:
          sensors:
            - {point_id: AHU_SAT, point_name: 送风温度, point_type: AI, unit: ℃}
            - {point_id: AHU_RAT, point_name: 回风温度, point_type: AI, unit: ℃}
            - {point_id: AHU_SAH, point_name: 送风湿度, point_type: AI, unit: "%RH"}
            - {point_id: AHU_OAT, point_name: 新风温度, point_type: AI, unit: ℃}
            - {point_id: AHU_FILTER_DP, point_name: 过滤器压差, point_type: AI, unit: Pa}
            - {point_id: AHU_FAN_FREQ, point_name: 风机频率, point_type: AI, unit: Hz}
            - {point_id: AHU_SA_FLOW, point_name: 送风量, point_type: AI, unit: "m³/h"}
            - {point_id: AHU_CO2, point_name: 回风CO2浓度, point_type: AI, unit: ppm}
          status:
            - {point_id: AHU_FAN_RUN, point_name: 风机运行状态, point_type: DI}
            - {point_id: AHU_FAN_FAULT, point_name: 风机故障状态, point_type: DI}
            - {point_id: AHU_FILTER_ALARM, point_name: 过滤器堵塞报警, point_type: DI}
            - {point_id: AHU_FREEZE_ALARM, point_name: 防冻报警, point_type: DI}
          commands:
            - {point_id: AHU_FAN_START_CMD, point_name: 风机启停命令, point_type: DO}
            - {point_id: AHU_OA_DAMPER, point_name: 新风阀开度, point_type: AO, unit: "%"}
            - {point_id: AHU_RA_DAMPER, point_name: 回风阀开度, point_type: AO, unit: "%"}
            - {point_id: AHU_EA_DAMPER, point_name: 排风阀开度, point_type: AO, unit: "%"}
            - {point_id: AHU_CHW_VALVE, point_name: 冷水阀开度, point_type: AO, unit: "%"}
            - {point_id: AHU_HW_VALVE, point_name: 热水阀开度, point_type: AO, unit: "%"}
          setpoints:
            - {point_id: AHU_SAT_SP, point_name: 送风温度设定, point_type: AO, unit: ℃}
            - {point_id: AHU_FAN_FREQ_SP, point_name: 风机频率设定, point_type: AO, unit: Hz}
            - {point_id: AHU_CO2_SP, point_name: CO2浓度设定, point_type: AO, unit: ppm}
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 空调机房
          floor: 各楼层/设备层
          area_requirement: ">30m²/台"
      
        noise_control:
          equipment_noise: "<85dB(A)@1m"
          room_treatment: 墙面吸声处理
          duct_silencer: 送风管消声器

      - node_id: HVAC-AHU_DST_SA_DUCT_MAIN
        node_name: 送风主风道
        node_name_en: Supply Air Main Duct
        node_type: Distribution_Node
        node_subtype: TRK
        node_category: DST
      
        function: 送风主管输送
        medium_in: AIR-SA
        medium_out: AIR-SA
      
        equipment_parameters:
          type: 镀锌钢板风管
          insulation: 橡塑保温25mm（外保温）
        
        location_hint:
          space_type: CEILING_VOID

      - node_id: HVAC-AHU_DST_SA_DUCT_BRANCH
        node_name: 送风支风道
        node_name_en: Supply Air Branch Duct
        node_type: Distribution_Node
        node_subtype: BRH
        node_category: DST
      
        function: 送风支管分配
        medium_in: AIR-SA
        medium_out: AIR-SA
      
        location_hint:
          space_type: CEILING_VOID

      - node_id: HVAC-AHU_DST_VAV
        node_name: 变风量末端
        node_name_en: VAV Terminal Unit
        node_type: Distribution_Node
        node_subtype: REG
        node_category: DST
      
        function: 区域风量调节
        medium_in: AIR-SA
        medium_out: AIR-SA
      
        multiplicity: multiple
        instance_pattern: HVAC-AHU_DST_VAV_{Floor}_{Zone}
      
        equipment_parameters:
          type: 单风道VAV箱
          air_volume_range: {min: 30, max: 100, unit: "%"}
          control_signal: "0-10V/4-20mA"
          with_reheat: optional
      
        control_points:
          sensors:
            - {point_id: VAV_FLOW, point_name: 风量, point_type: AI, unit: "m³/h"}
            - {point_id: ZONE_TEMP, point_name: 区域温度, point_type: AI, unit: ℃}
          commands:
            - {point_id: VAV_DAMPER, point_name: 风阀开度, point_type: AO, unit: "%"}
          setpoints:
            - {point_id: ZONE_TEMP_SP, point_name: 区域温度设定, point_type: AO, unit: ℃}
      
        location_hint:
          space_type: CEILING_VOID

      - node_id: HVAC-AHU_DST_RA_DUCT
        node_name: 回风风道
        node_name_en: Return Air Duct
        node_type: Distribution_Node
        node_subtype: TRK
        node_category: DST
      
        function: 回风输送
        medium_in: AIR-RA
        medium_out: AIR-RA
      
        location_hint:
          space_type: CEILING_VOID

    sink_nodes:
  
      - node_id: HVAC-AHU_SNK_SA_DIFFUSER
        node_name: 送风口
        node_name_en: Supply Air Diffuser
        node_type: Sink_Node
        node_category: SNK
      
        function: 向房间送风
        medium_in: AIR-SA
        medium_out: AIR-SA (to room)
      
        multiplicity: multiple
        instance_pattern: HVAC-AHU_SNK_SA_DIFFUSER_{Floor}_{Room}_{Seq}
      
        equipment_parameters:
          type: 散流器/格栅风口/旋流风口
          material: 铝合金
        
        location_hint:
          space_type: CEILING

      - node_id: HVAC-AHU_SNK_EA_OUTLET
        node_name: 排风出口
        node_name_en: Exhaust Air Outlet
        node_type: Sink_Node
        node_category: SNK
      
        function: 排风排放
        medium_in: AIR-EA
        medium_out: AIR-EA (to outdoor)
      
        is_boundary_output: true
      
        equipment_parameters:
          type: 防雨百叶
        
        location_hint:
          space_type: EXTERIOR

  edges:

    supply_edges:
      - {edge_id: HVAC-AHU_EDGE_001, from_node: HVAC-AHU_SRC_OA_INTAKE, to_node: HVAC-AHU_DST_AHU, medium: AIR-OA}
      - {edge_id: HVAC-AHU_EDGE_002, from_node: HVAC-AHU_SRC_RA_GRILLE, to_node: HVAC-AHU_DST_RA_DUCT, medium: AIR-RA}
      - {edge_id: HVAC-AHU_EDGE_003, from_node: HVAC-AHU_DST_RA_DUCT, to_node: HVAC-AHU_DST_AHU, medium: AIR-RA}
      - {edge_id: HVAC-AHU_EDGE_004, from_node: HVAC-AHU_DST_AHU, to_node: HVAC-AHU_DST_SA_DUCT_MAIN, medium: AIR-SA}
      - {edge_id: HVAC-AHU_EDGE_005, from_node: HVAC-AHU_DST_SA_DUCT_MAIN, to_node: HVAC-AHU_DST_SA_DUCT_BRANCH, medium: AIR-SA, multiplicity: multiple}
      - {edge_id: HVAC-AHU_EDGE_006, from_node: HVAC-AHU_DST_SA_DUCT_BRANCH, to_node: HVAC-AHU_DST_VAV, medium: AIR-SA}
      - {edge_id: HVAC-AHU_EDGE_007, from_node: HVAC-AHU_DST_VAV, to_node: HVAC-AHU_SNK_SA_DIFFUSER, medium: AIR-SA, multiplicity: multiple}

  control_logic:

    supply_air_temp_control:
      name: 送风温度控制
      logic: |
        1. PID控制冷/热水阀开度维持送风温度设定值
        2. 夏季：调节冷水阀，送风温度目标14-16℃
        3. 冬季：调节热水阀，送风温度目标28-35℃
        4. 过渡季：优先利用新风免费冷却

    fresh_air_ratio_control:
      name: 新风比控制
      logic: |
        1. 最小新风量保证（按人员或面积计算）
        2. 过渡季节全新风运行（新风温度适宜时）
        3. CO2浓度>1000ppm时增大新风量（需求控制通风DCV）
        4. 新风阀与回风阀、排风阀联动
      minimum_fresh_air_ratio: 30%
      co2_setpoint: {value: 800, unit: ppm}

    vav_control:
      name: VAV末端控制
      logic: |
        1. 区域温度反馈控制风阀开度
        2. 温度高于设定→开大风阀，温度低于设定→关小风阀
        3. 最小风量设定（换气次数保证）
        4. 静压复位优化AHU风机能耗

    static_pressure_reset:
      name: 静压复位控制
      logic: |
        1. 监测各VAV阀位
        2. 当大部分VAV开度<70%时，降低静压设定
        3. 当有VAV开度>95%时，提高静压设定
        4. 静压设定范围：150-400Pa

    freeze_protection:
      name: 防冻保护
      trigger: 新风温度<5℃ 或 盘管后温度<8℃
      actions:
        - 关闭新风阀
        - 开启热水阀100%
        - 必要时停机报警
```

---

## 系统 1.6: HVAC-HW 热水输配系统（简化版）

```yaml
System_Topology:

  identity:
    system_id: HVAC-HW
    system_name: 热水输配系统
    system_name_en: Hot Water Distribution System
    system_category: HVAC
    system_type: 水系统-输配
    priority_level: P1-CRITICAL
  
    description: |
      医院热水输配系统，负责将锅炉房的空调热水输送至各区域的空调末端设备。
      系统采用变流量控制，通过楼层/区域分支向各AHU、FCU、PAU供应60℃/50℃热水。
  
    parent_system: HVAC-CHP
    child_systems:
      - HVAC-AHU
      - HVAC-FCU
      - HVAC-PAU
  
    version: 3.0
    last_updated: 2024

  boundary:
    inputs:
      - boundary_id: HVAC-HW_IN_001
        name: 热水供水输入
        from_system: HVAC-CHP
        from_node: HVAC-CHP_SNK_HW_RISER
        medium: HW
        parameters:
          temperature: {value: 60, unit: ℃}
          pressure: {value: "0.35-0.45", unit: MPa}
        
    outputs:
      - boundary_id: HVAC-HW_OUT_001
        name: 热水回水输出
        to_system: HVAC-CHP
        medium: HW
        parameters:
          temperature: {value: 50, unit: ℃}
        
      - boundary_id: HVAC-HW_OUT_002
        name: 热水末端接口
        to_system: HVAC-AHU/FCU/PAU
        medium: HW

  nodes:

    source_nodes:
  
      - node_id: HVAC-HW_SRC_RISER_IN
        node_name: 热水立管供水入口
        node_name_en: HW Riser Supply Inlet
        node_type: Source_Node
        node_category: SRC
        function: 接收冷热源系统的热水供水
        medium_in: HW
        medium_out: HW
        is_boundary_input: true
        source_system: HVAC-CHP
        multiplicity: multiple
        instance_pattern: HVAC-HW_SRC_RISER_IN_{Zone}
      
        location_hint:
          space_type: SHAFT
          shaft_type: 空调水管井

    distribution_nodes:
  
      - node_id: HVAC-HW_DST_RISER
        node_name: 热水立管
        node_name_en: HW Riser
        node_type: Distribution_Node
        node_subtype: TRK
        node_category: DST
        function: 垂直输送热水至各楼层
        medium_in: HW
        medium_out: HW
        multiplicity: multiple
      
        equipment_parameters:
          material: 无缝钢管
          diameter: {value: "DN80-DN125", unit: mm}
          insulation: {type: "橡塑保温", thickness: 50, unit: mm}
        
        location_hint:
          space_type: SHAFT

      - node_id: HVAC-HW_DST_FLOOR_HEADER
        node_name: 楼层热水分集水器
        node_name_en: Floor HW Header
        node_type: Distribution_Node
        node_subtype: SPL
        node_category: DST
        function: 楼层热水分配
        medium_in: HW
        medium_out: HW
        multiplicity: multiple
      
        equipment_parameters:
          material: 无缝钢管
          diameter: {value: "DN65-DN80", unit: mm}
          insulation: {type: "橡塑保温", thickness: 40, unit: mm}
        
        location_hint:
          space_type: SHAFT

      - node_id: HVAC-HW_DST_BRANCH
        node_name: 楼层热水支管
        node_name_en: Floor HW Branch
        node_type: Distribution_Node
        node_subtype: BRH
        node_category: DST
        function: 楼层内热水水平输配
        medium_in: HW
        medium_out: HW
        multiplicity: multiple
      
        equipment_parameters:
          material: 无缝钢管
          diameter: {value: "DN40-DN65", unit: mm}
          insulation: {type: "橡塑保温", thickness: 30, unit: mm}
        
        location_hint:
          space_type: CEILING_VOID

    sink_nodes:
  
      - node_id: HVAC-HW_SNK_AHU_COIL
        node_name: 空调箱热水盘管接口
        node_name_en: AHU HW Coil Connection
        node_type: Sink_Node
        node_category: SNK
        function: 连接至空调箱热水盘管
        medium_in: HW
        medium_out: HW
        is_boundary_output: true
        target_system: HVAC-AHU
        multiplicity: multiple
      
        interface_parameters:
          pipe_size: {value: "DN40-DN65", unit: mm}
          control_valve: 电动二通阀
        
        location_hint:
          space_type: MEP_ROOM

      - node_id: HVAC-HW_SNK_FCU_COIL
        node_name: 风机盘管热水接口
        node_name_en: FCU HW Coil Connection
        node_type: Sink_Node
        node_category: SNK
        function: 连接至风机盘管热水盘管
        medium_in: HW
        medium_out: HW
        is_boundary_output: true
        target_system: HVAC-FCU
        multiplicity: multiple
      
        interface_parameters:
          pipe_size: {value: "DN20-DN32", unit: mm}
          control_valve: 电动二通阀/电热阀
        
        location_hint:
          space_type: CEILING_VOID

      - node_id: HVAC-HW_SNK_PAU_COIL
        node_name: 新风机组热水盘管接口
        node_name_en: PAU HW Coil Connection
        node_type: Sink_Node
        node_category: SNK
        function: 连接至新风机组热水盘管
        medium_in: HW
        medium_out: HW
        is_boundary_output: true
        target_system: HVAC-PAU
        multiplicity: multiple
      
        interface_parameters:
          pipe_size: {value: "DN40-DN65", unit: mm}
          control_valve: 电动二通阀
        
        location_hint:
          space_type: MEP_ROOM

      - node_id: HVAC-HW_SNK_RISER_OUT
        node_name: 热水立管回水出口
        node_name_en: HW Riser Return Outlet
        node_type: Sink_Node
        node_category: SNK
        function: 热水回水返回冷热源系统
        medium_in: HW
        medium_out: HW
        is_boundary_output: true
        target_system: HVAC-CHP
        multiplicity: multiple
      
        location_hint:
          space_type: SHAFT

  edges:

    supply_edges:
      - {edge_id: HVAC-HW_EDGE_001, from_node: HVAC-HW_SRC_RISER_IN, to_node: HVAC-HW_DST_RISER, medium: HW}
      - {edge_id: HVAC-HW_EDGE_002, from_node: HVAC-HW_DST_RISER, to_node: HVAC-HW_DST_FLOOR_HEADER, medium: HW, multiplicity: multiple}
      - {edge_id: HVAC-HW_EDGE_003, from_node: HVAC-HW_DST_FLOOR_HEADER, to_node: HVAC-HW_DST_BRANCH, medium: HW}
      - {edge_id: HVAC-HW_EDGE_004, from_node: HVAC-HW_DST_BRANCH, to_node: HVAC-HW_SNK_AHU_COIL, medium: HW}
      - {edge_id: HVAC-HW_EDGE_005, from_node: HVAC-HW_DST_BRANCH, to_node: HVAC-HW_SNK_FCU_COIL, medium: HW, multiplicity: multiple}
      - {edge_id: HVAC-HW_EDGE_006, from_node: HVAC-HW_DST_BRANCH, to_node: HVAC-HW_SNK_PAU_COIL, medium: HW}

    return_edges:
      - {edge_id: HVAC-HW_EDGE_011, from_node: HVAC-HW_SNK_AHU_COIL, to_node: HVAC-HW_DST_BRANCH, medium: HW, note: return}
      - {edge_id: HVAC-HW_EDGE_012, from_node: HVAC-HW_SNK_FCU_COIL, to_node: HVAC-HW_DST_BRANCH, medium: HW, note: return}
      - {edge_id: HVAC-HW_EDGE_013, from_node: HVAC-HW_SNK_PAU_COIL, to_node: HVAC-HW_DST_BRANCH, medium: HW, note: return}
      - {edge_id: HVAC-HW_EDGE_014, from_node: HVAC-HW_DST_BRANCH, to_node: HVAC-HW_DST_FLOOR_HEADER, medium: HW, note: return}
      - {edge_id: HVAC-HW_EDGE_015, from_node: HVAC-HW_DST_FLOOR_HEADER, to_node: HVAC-HW_DST_RISER, medium: HW, note: return}
      - {edge_id: HVAC-HW_EDGE_016, from_node: HVAC-HW_DST_RISER, to_node: HVAC-HW_SNK_RISER_OUT, medium: HW, note: return}

  typical_paths:

    - path_id: HVAC-HW_PATH_TO_AHU
      path_name: 热水至空调箱路径
      path_type: SUP
      sequence:
        - {step: 1, node: HVAC-HW_SRC_RISER_IN, action: 接收热水供水}
        - {step: 2, node: HVAC-HW_DST_RISER, action: 垂直输送}
        - {step: 3, node: HVAC-HW_DST_FLOOR_HEADER, action: 楼层分配}
        - {step: 4, node: HVAC-HW_DST_BRANCH, action: 水平输送}
        - {step: 5, node: HVAC-HW_SNK_AHU_COIL, action: 送达AHU热水盘管}
      operating_conditions:
        supply_temp: {value: 60, unit: ℃}
        return_temp: {value: 50, unit: ℃}
```

---

# 第一批次输出完成（第三版）

## 批次质量总结

| 系统ID | 系统名称 | 版本 | 主要改进 |
|--------|----------|------|----------|
| HVAC-CHP | 冷热源系统 | v3.0 | H1压差控制策略、H2冷却塔联动逻辑、依赖关系 |
| HVAC-CHW | 冷冻水输配系统 | v3.0 | 平衡阀节点细化、设计参数标注 |
| HVAC-HW | 热水输配系统 | v3.0 | 简化版，保持结构一致性 |
| HVAC-AHU | 空调箱系统 | v3.0 | CO2控制、VAV控制、静压复位 |
| HVAC-FCU | 风机盘管系统 | v3.0 | H3新风比控制、与PAU协调 |
| HVAC-PAU | 新风机组系统 | v3.0 | H3新风比控制、压力梯度、湿度控制 |

## H1-H3缺陷修复确认

| 缺陷ID | 描述 | 修复状态 | 修复位置 |
|--------|------|----------|----------|
| H1 | 压差控制逻辑 | ✅ 已修复 | HVAC-CHP: loops.loop_control_strategy, bypass_control_logic |
| H2 | 冷却塔-冷机联动 | ✅ 已修复 | HVAC-CHP: control_logic.cooling_tower_chiller_coordination |
| H3 | 新风比控制 | ✅ 已修复 | HVAC-PAU: control_logic.fresh_air_ratio_control, pau_fcu_coordination; HVAC-FCU: control_logic.fresh_air_coordination |

---

