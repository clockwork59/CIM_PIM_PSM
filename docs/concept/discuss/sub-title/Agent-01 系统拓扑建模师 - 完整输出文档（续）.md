## 🧑‍💻 User


你卡在了【- node_id: HVAC-CHP_SRC_BOILER
 node_name: 燃气热水锅炉
 node_name_en: Gas Fired Hot Water Boiler
 node_type: Source_Node
 node_category: SRC

 function: 制取空调热水
 medium_in: [GAS-NG, WATER-DW]
 medium_out: HW

 multiplicity: multiple
 instance_pattern: HVAC-CHP_SRC_BOILER_{NN}】继续输出‘Agent-01 系统拓扑建模师 - 完整输出文档’

---
## 🤖 Assistant


# Agent-01 系统拓扑建模师 - 完整输出文档（续）

## 继续：HVAC-CHP 冷热源系统拓扑

### Source Nodes（续）

```yaml
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
          type: 真空热水锅炉/常压热水锅炉
          thermal_efficiency: ">95%"
          fuel_type: 天然气
          hw_supply_temp: {value: 60, unit: ℃}
          hw_return_temp: {value: 50, unit: ℃}
          pressure_rating: {value: 1.0, unit: MPa}
          turndown_ratio: "5:1"
          nox_emission: "<30mg/m³"
        
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
          commands:
            - point_id: BOILER_START
              point_name: 锅炉启停命令
              point_type: DO
          setpoints:
            - point_id: BOILER_HW_SETPOINT
              point_name: 热水供水温度设定
              point_type: AO
              unit: ℃
              range: [45, 70]
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 锅炉房
          floor: B1/1F
          area_requirement: ">200m²"
        
        installation_requirements:
          - 防火间距符合GB 50016要求
          - 独立燃气调压间
          - 烟囱高度≥15m或高于周边建筑
          - 防爆要求区域
          - 可燃气体探测器
          - 紧急切断阀

      - node_id: HVAC-CHP_SRC_ASHP
        node_name: 空气源热泵机组
        node_name_en: Air Source Heat Pump Unit
        node_type: Source_Node
        node_category: SRC
        
        function: 制取空调冷/热水（过渡季/辅助）
        medium_in: AIR-OA
        medium_out: [CHW, HW]
        
        multiplicity: multiple
        instance_pattern: HVAC-CHP_SRC_ASHP_{NN}
        typical_configuration:
          quantity: 2
          redundancy: "N+1"
          capacity_each: {value: 500, unit: kW}
        
        equipment_parameters:
          type: 风冷模块化热泵机组
          cooling_capacity: {value: 500, unit: kW}
          heating_capacity: {value: 550, unit: kW}
          cop_cooling: ">3.2"
          cop_heating: ">3.5"
          chw_supply_temp: {value: 7, unit: ℃}
          hw_supply_temp: {value: 45, unit: ℃}
          ambient_range: [-15, 43]
        
        control_points:
          sensors:
            - point_id: ASHP_WT
              point_name: 出水温度
              point_type: AI
              unit: ℃
          status:
            - point_id: ASHP_RUN
              point_name: 机组运行状态
              point_type: DI
            - point_id: ASHP_MODE
              point_name: 制冷/制热模式
              point_type: DI
            - point_id: ASHP_FAULT
              point_name: 机组故障状态
              point_type: DI
          commands:
            - point_id: ASHP_START
              point_name: 机组启停命令
              point_type: DO
            - point_id: ASHP_MODE_CMD
              point_name: 模式切换命令
              point_type: DO
        
        location_hint:
          space_type: OUTDOOR
          position: 裙房屋面/室外地面
          area_requirement: ">100m²"
        
        installation_requirements:
          - 通风良好
          - 设备基础减振
          - 检修通道≥1.2m
          - 噪音控制措施

    # ========================================
    # Distribution Nodes - 传输/调节/分配节点
    # ========================================
    distribution_nodes:
    
      # === 冷冻水系统分配节点 ===
      - node_id: HVAC-CHP_DST_CHW_PRI_PUMP
        node_name: 冷冻水一次泵
        node_name_en: Chilled Water Primary Pump
        node_type: Distribution_Node
        node_subtype: TRF
        node_category: DST
        
        function: 冷水机组侧冷冻水循环
        medium_in: CHW
        medium_out: CHW
        
        multiplicity: multiple
        instance_pattern: HVAC-CHP_DST_CHW_PRI_PUMP_{NN}
        typical_configuration:
          quantity: 4
          redundancy: "一机一泵+1备用"
        
        equipment_parameters:
          type: 卧式离心泵
          flow_rate: {value: 180, unit: "m³/h"}
          head: {value: 25, unit: mH2O}
          power: {value: 22, unit: kW}
          motor_efficiency: ">IE3"
          control_type: 工频运行
        
        control_points:
          status:
            - point_id: CHW_PRI_PUMP_RUN
              point_name: 泵运行状态
              point_type: DI
            - point_id: CHW_PRI_PUMP_FAULT
              point_name: 泵故障状态
              point_type: DI
          commands:
            - point_id: CHW_PRI_PUMP_START
              point_name: 泵启停命令
              point_type: DO
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房
          position: 冷水机组出水侧

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
        
        equipment_parameters:
          type: 卧式离心泵
          flow_rate: {value: 200, unit: "m³/h"}
          head: {value: 32, unit: mH2O}
          power: {value: 37, unit: kW}
          motor_efficiency: ">IE3"
          control_type: 变频调节
          vfd_range: "25Hz-50Hz"
        
        control_points:
          sensors:
            - point_id: CHW_SEC_PUMP_FREQ
              point_name: 泵运行频率
              point_type: AI
              unit: Hz
              range: [0, 50]
          status:
            - point_id: CHW_SEC_PUMP_RUN
              point_name: 泵运行状态
              point_type: DI
            - point_id: CHW_SEC_PUMP_FAULT
              point_name: 泵故障状态
              point_type: DI
          commands:
            - point_id: CHW_SEC_PUMP_START
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
          type: 分水器
          diameter: {value: DN400, unit: mm}
          material: 无缝钢管
          outlets: 6-8路
          pressure_rating: {value: 1.6, unit: MPa}
          insulation: 橡塑保温40mm
        
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
          type: 集水器
          diameter: {value: DN400, unit: mm}
          material: 无缝钢管
          inlets: 6-8路
          pressure_rating: {value: 1.6, unit: MPa}
          insulation: 橡塑保温40mm
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房
          position: 中央位置

      - node_id: HVAC-CHP_DST_CHW_BYPASS
        node_name: 冷冻水旁通阀
        node_name_en: Chilled Water Bypass Valve
        node_type: Distribution_Node
        node_subtype: REG
        node_category: DST
        
        function: 调节一二次侧流量平衡，保护冷水机组
        medium_in: CHW
        medium_out: CHW
        
        equipment_parameters:
          type: 电动压差旁通阀
          diameter: {value: DN200, unit: mm}
          control_signal: "4-20mA"
          cv_value: 适配系统流量
        
        control_points:
          sensors:
            - point_id: CHW_BYPASS_POS
              point_name: 旁通阀开度
              point_type: AI
              unit: "%"
              range: [0, 100]
            - point_id: CHW_DP
              point_name: 供回水压差
              point_type: AI
              unit: kPa
              range: [0, 200]
          setpoints:
            - point_id: CHW_DP_SP
              point_name: 压差设定值
              point_type: AO
              unit: kPa
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房
          position: 分集水器之间

      # === 热水系统分配节点 ===
      - node_id: HVAC-CHP_DST_HW_PRI_PUMP
        node_name: 热水一次泵
        node_name_en: Hot Water Primary Pump
        node_type: Distribution_Node
        node_subtype: TRF
        node_category: DST
        
        function: 锅炉侧热水循环
        medium_in: HW
        medium_out: HW
        
        multiplicity: multiple
        instance_pattern: HVAC-CHP_DST_HW_PRI_PUMP_{NN}
        typical_configuration:
          quantity: 3
          redundancy: "一机一泵"
        
        equipment_parameters:
          type: 卧式离心泵
          flow_rate: {value: 120, unit: "m³/h"}
          head: {value: 20, unit: mH2O}
          power: {value: 15, unit: kW}
          motor_efficiency: ">IE3"
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
            - point_id: HW_PRI_PUMP_START
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
          type: 卧式离心泵
          flow_rate: {value: 150, unit: "m³/h"}
          head: {value: 28, unit: mH2O}
          power: {value: 22, unit: kW}
          motor_efficiency: ">IE3"
          control_type: 变频调节
          vfd_range: "25Hz-50Hz"
        
        control_points:
          sensors:
            - point_id: HW_SEC_PUMP_FREQ
              point_name: 泵运行频率
              point_type: AI
              unit: Hz
              range: [0, 50]
          status:
            - point_id: HW_SEC_PUMP_RUN
              point_name: 泵运行状态
              point_type: DI
            - point_id: HW_SEC_PUMP_FAULT
              point_name: 泵故障状态
              point_type: DI
          commands:
            - point_id: HW_SEC_PUMP_START
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
          diameter: {value: DN300, unit: mm}
          material: 无缝钢管
          outlets: 4-6路
          pressure_rating: {value: 1.6, unit: MPa}
          insulation: 橡塑保温50mm
        
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
          diameter: {value: DN300, unit: mm}
          material: 无缝钢管
          inlets: 4-6路
          pressure_rating: {value: 1.6, unit: MPa}
          insulation: 橡塑保温50mm
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 锅炉房/换热站
          position: 中央位置

      # === 冷却水系统分配节点 ===
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
          redundancy: "一机一泵+1备用"
        
        equipment_parameters:
          type: 卧式离心泵
          flow_rate: {value: 250, unit: "m³/h"}
          head: {value: 28, unit: mH2O}
          power: {value: 37, unit: kW}
          motor_efficiency: ">IE3"
          control_type: 工频/变频可选
        
        control_points:
          status:
            - point_id: CW_PUMP_RUN
              point_name: 泵运行状态
              point_type: DI
            - point_id: CW_PUMP_FAULT
              point_name: 泵故障状态
              point_type: DI
          commands:
            - point_id: CW_PUMP_START
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
          cooling_capacity: {value: 1200, unit: kW}
          flow_rate: {value: 250, unit: "m³/h"}
          inlet_temp: {value: 37, unit: ℃}
          outlet_temp: {value: 32, unit: ℃}
          wet_bulb_temp: {value: 28, unit: ℃}
          fan_power: {value: 11, unit: kW}
          noise_level: "<65dB(A)@1m"
          drift_loss: "<0.001%"
        
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
          commands:
            - point_id: CT_FAN_START
              point_name: 冷却塔风机启停命令
              point_type: DO
        
        location_hint:
          space_type: OUTDOOR
          position: 裙房屋面/室外专区
          area_requirement: ">300m²"
        
        installation_requirements:
          - 远离新风口≥10m
          - 设置隔声围栏
          - 排水设施完善
          - 防坠落措施
          - 冬季防冻措施

      # === 补水定压节点 ===
      - node_id: HVAC-CHP_DST_CHW_EXPANSION
        node_name: 冷冻水定压补水装置
        node_name_en: CHW Pressurization & Makeup Unit
        node_type: Distribution_Node
        node_subtype: BUF
        node_category: DST
        
        function: 冷冻水系统定压补水、膨胀吸收
        medium_in: WATER-DW
        medium_out: CHW
        
        equipment_parameters:
          type: 全自动定压补水装置
          tank_volume: {value: 600, unit: L}
          makeup_flow: {value: 5, unit: "m³/h"}
          set_pressure: {value: 0.3, unit: MPa}
          pressure_range: {value: "0.25-0.35", unit: MPa}
        
        control_points:
          sensors:
            - point_id: CHW_SYS_PRESS
              point_name: 冷冻水系统压力
              point_type: AI
              unit: MPa
              range: [0, 1.0]
          status:
            - point_id: CHW_MAKEUP_RUN
              point_name: 补水泵运行状态
              point_type: DI
            - point_id: CHW_LOW_PRESS
              point_name: 系统低压报警
              point_type: DI
            - point_id: CHW_HIGH_PRESS
              point_name: 系统高压报警
              point_type: DI
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房
          position: 系统最低点附近

      - node_id: HVAC-CHP_DST_HW_EXPANSION
        node_name: 热水定压补水装置
        node_name_en: HW Pressurization & Makeup Unit
        node_type: Distribution_Node
        node_subtype: BUF
        node_category: DST
        
        function: 热水系统定压补水、膨胀吸收
        medium_in: WATER-DW
        medium_out: HW
        
        equipment_parameters:
          type: 全自动定压补水装置
          tank_volume: {value: 800, unit: L}
          makeup_flow: {value: 5, unit: "m³/h"}
          set_pressure: {value: 0.35, unit: MPa}
          pressure_range: {value: "0.30-0.40", unit: MPa}
        
        control_points:
          sensors:
            - point_id: HW_SYS_PRESS
              point_name: 热水系统压力
              point_type: AI
              unit: MPa
              range: [0, 1.0]
          status:
            - point_id: HW_MAKEUP_RUN
              point_name: 补水泵运行状态
              point_type: DI
            - point_id: HW_LOW_PRESS
              point_name: 系统低压报警
              point_type: DI
            - point_id: HW_HIGH_PRESS
              point_name: 系统高压报警
              point_type: DI
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 锅炉房
          position: 系统最低点附近

      # === 水处理节点 ===
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
            - 电化学除垢
            - 自动加药
            - 旁滤净化
          flow_rate: {value: 50, unit: "m³/h"}
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 水处理间/冷冻机房
          position: 冷却水回水管旁路

    # ========================================
    # Sink Nodes - 消耗终端节点
    # ========================================
    sink_nodes:
    
      - node_id: HVAC-CHP_SNK_CHW_RISER
        node_name: 冷冻水区域立管接口
        node_name_en: CHW Zone Riser Connection
        node_type: Sink_Node
        node_category: SNK
        
        function: 连接至各区域冷冻水立管
        medium_in: CHW
        medium_out: CHW
        
        multiplicity: multiple
        instance_pattern: HVAC-CHP_SNK_CHW_RISER_{Zone}
        typical_quantity: 6-8 zones
        
        downstream_system: HVAC-CHW
        
        interface_parameters:
          pipe_size: DN100-DN150
          isolation_valve: 电动蝶阀
          balancing_valve: 动态平衡阀
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房
          position: 分水器出口

      - node_id: HVAC-CHP_SNK_HW_RISER
        node_name: 热水区域立管接口
        node_name_en: HW Zone Riser Connection
        node_type: Sink_Node
        node_category: SNK
        
        function: 连接至各区域热水立管
        medium_in: HW
        medium_out: HW
        
        multiplicity: multiple
        instance_pattern: HVAC-CHP_SNK_HW_RISER_{Zone}
        typical_quantity: 4-6 zones
        
        downstream_system: HVAC-HW
        
        interface_parameters:
          pipe_size: DN80-DN125
          isolation_valve: 电动蝶阀
          balancing_valve: 动态平衡阀
        
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
        edge_name: 冷水机组至一次泵
        edge_type: TRK
        from_node: HVAC-CHP_SRC_CHILLER
        to_node: HVAC-CHP_DST_CHW_PRI_PUMP
        direction: unidirectional
        medium: CHW
        medium_state:
          temperature: {value: 7, unit: ℃}
          pressure: {value: 0.5, unit: MPa}
          flow_direction: supply
        pipe_parameters:
          material: 无缝钢管
          diameter: DN200
          insulation: 橡塑保温50mm
        
      - edge_id: HVAC-CHP_EDGE_002
        edge_name: 一次泵至分水器
        edge_type: TRK
        from_node: HVAC-CHP_DST_CHW_PRI_PUMP
        to_node: HVAC-CHP_DST_CHW_HEADER_S
        direction: unidirectional
        medium: CHW
        pipe_parameters:
          material: 无缝钢管
          diameter: DN200
          insulation: 橡塑保温50mm

      - edge_id: HVAC-CHP_EDGE_003
        edge_name: 分水器至二次泵
        edge_type: TRK
        from_node: HVAC-CHP_DST_CHW_HEADER_S
        to_node: HVAC-CHP_DST_CHW_SEC_PUMP
        direction: unidirectional
        medium: CHW
        pipe_parameters:
          material: 无缝钢管
          diameter: DN250
          insulation: 橡塑保温50mm

      - edge_id: HVAC-CHP_EDGE_004
        edge_name: 二次泵至区域立管
        edge_type: BRH
        from_node: HVAC-CHP_DST_CHW_SEC_PUMP
        to_node: HVAC-CHP_SNK_CHW_RISER
        direction: unidirectional
        medium: CHW
        multiplicity: multiple
        pipe_parameters:
          material: 无缝钢管
          diameter: DN100-DN150
          insulation: 橡塑保温40mm

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
          diameter: DN100-DN150
          insulation: 橡塑保温40mm

      - edge_id: HVAC-CHP_EDGE_012
        edge_name: 集水器至冷水机组
        edge_type: TRK
        from_node: HVAC-CHP_DST_CHW_HEADER_R
        to_node: HVAC-CHP_SRC_CHILLER
        direction: unidirectional
        medium: CHW
        pipe_parameters:
          material: 无缝钢管
          diameter: DN250
          insulation: 橡塑保温50mm

    # === 旁通路径边 ===
    bypass_edges:
    
      - edge_id: HVAC-CHP_EDGE_021
        edge_name: 冷冻水旁通管
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
        edge_name: 锅炉至一次泵
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
          diameter: DN150
          insulation: 橡塑保温60mm

      - edge_id: HVAC-CHP_EDGE_032
        edge_name: 一次泵至分水器
        edge_type: TRK
        from_node: HVAC-CHP_DST_HW_PRI_PUMP
        to_node: HVAC-CHP_DST_HW_HEADER_S
        direction: unidirectional
        medium: HW
        pipe_parameters:
          material: 无缝钢管
          diameter: DN150
          insulation: 橡塑保温60mm

      - edge_id: HVAC-CHP_EDGE_033
        edge_name: 分水器至二次泵
        edge_type: TRK
        from_node: HVAC-CHP_DST_HW_HEADER_S
        to_node: HVAC-CHP_DST_HW_SEC_PUMP
        direction: unidirectional
        medium: HW
        pipe_parameters:
          material: 无缝钢管
          diameter: DN200
          insulation: 橡塑保温60mm

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
          diameter: DN80-DN125
          insulation: 橡塑保温50mm

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
          diameter: DN80-DN125
          insulation: 橡塑保温50mm

      - edge_id: HVAC-CHP_EDGE_042
        edge_name: 集水器至锅炉
        edge_type: TRK
        from_node: HVAC-CHP_DST_HW_HEADER_R
        to_node: HVAC-CHP_SRC_BOILER
        direction: unidirectional
        medium: HW
        pipe_parameters:
          material: 无缝钢管
          diameter: DN200
          insulation: 橡塑保温60mm

    # === 冷却水路径边 ===
    cw_edges:
    
      - edge_id: HVAC-CHP_EDGE_051
        edge_name: 冷水机组冷凝器至冷却水泵
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
          diameter: DN250
          insulation: 无

      - edge_id: HVAC-CHP_EDGE_052
        edge_name: 冷却水泵至冷却塔
        edge_type: TRK
        from_node: HVAC-CHP_DST_CW_PUMP
        to_node: HVAC-CHP_DST_COOLING_TOWER
        direction: unidirectional
        medium: CW
        pipe_parameters:
          material: 无缝钢管/镀锌钢管
          diameter: DN250
          insulation: 室外段保温

      - edge_id: HVAC-CHP_EDGE_053
        edge_name: 冷却塔至冷水机组冷凝器
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
          diameter: DN250
          insulation: 室外段保温

    # === 补水路径边 ===
    makeup_edges:
    
      - edge_id: HVAC-CHP_EDGE_061
        edge_name: 软化水至冷冻水补水装置
        edge_type: TRM
        from_node: EXTERNAL_SOFTENED_WATER
        to_node: HVAC-CHP_DST_CHW_EXPANSION
        direction: unidirectional
        medium: WATER-DW
        is_boundary_edge: true
        pipe_parameters:
          diameter: DN32

      - edge_id: HVAC-CHP_EDGE_062
        edge_name: 冷冻水补水装置至系统
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
        medium: WATER-DW
        is_boundary_edge: true
        pipe_parameters:
          diameter: DN32

      - edge_id: HVAC-CHP_EDGE_064
        edge_name: 热水补水装置至系统
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
          action: 一次侧冷冻水循环
        - step: 3
          node: HVAC-CHP_DST_CHW_HEADER_S
          action: 供水分配
        - step: 4
          node: HVAC-CHP_DST_CHW_SEC_PUMP
          action: 变频加压送水
        - step: 5
          node: HVAC-CHP_SNK_CHW_RISER
          action: 送至各区域立管
      operating_conditions:
        season: 夏季
        supply_temp: 7℃
        return_temp: 12℃
        delta_t: 5℃

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
          action: 汇集回水
        - step: 3
          node: HVAC-CHP_SRC_CHILLER
          action: 回到蒸发器再冷却
      operating_conditions:
        season: 夏季
        return_temp: 12℃

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
          action: 一次侧热水循环
        - step: 3
          node: HVAC-CHP_DST_HW_HEADER_S
          action: 供水分配
        - step: 4
          node: HVAC-CHP_DST_HW_SEC_PUMP
          action: 变频加压送水
        - step: 5
          node: HVAC-CHP_SNK_HW_RISER
          action: 送至各区域立管
      operating_conditions:
        season: 冬季
        supply_temp: 60℃
        return_temp: 50℃
        delta_t: 10℃

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
          action: 冷却水循环
        - step: 3
          node: HVAC-CHP_DST_COOLING_TOWER
          action: 蒸发散热降温至32℃
        - step: 4
          node: HVAC-CHP_SRC_CHILLER
          action: 回到冷凝器吸热
      operating_conditions:
        season: 夏季
        supply_temp: 32℃
        return_temp: 37℃
        delta_t: 5℃

    - path_id: HVAC-CHP_PATH_CHW_BYPASS
      path_name: 冷冻水旁通路径
      path_type: BYP
      description: 一二次泵流量不平衡时的旁通调节
      sequence:
        - step: 1
          node: HVAC-CHP_DST_CHW_HEADER_S
          action: 供水侧
        - step: 2
          node: HVAC-CHP_DST_CHW_BYPASS
          action: 压差旁通调节
        - step: 3
          node: HVAC-CHP_DST_CHW_HEADER_R
          action: 汇入回水侧
      trigger_conditions:
        - 二次泵流量<一次泵流量
        - 供回水压差超过设定值

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
      control_strategy:
        type: 定流量
        description: 一次泵与冷水机组联动，一机一泵运行

    - loop_id: HVAC-CHP_LOOP_CHW_SECONDARY
      loop_name: 冷冻水二次侧回路
      loop_type: 变流量回路
      description: 分集水器至用户侧的二次循环
      nodes_in_loop:
        - HVAC-CHP_DST_CHW_HEADER_S
        - HVAC-CHP_DST_CHW_SEC_PUMP
        - HVAC-CHP_SNK_CHW_RISER
        - HVAC-CHP_DST_CHW_HEADER_R
      control_strategy:
        type: 变流量
        control_variable: 供回水压差
        setpoint: 80-120kPa
        description: 根据末端负荷变化调节二次泵频率

    - loop_id: HVAC-CHP_LOOP_CW
      loop_name: 冷却水回路
      loop_type: 定流量/变流量可选
      description: 冷凝器与冷却塔之间的冷却水循环
      nodes_in_loop:
        - HVAC-CHP_SRC_CHILLER
        - HVAC-CHP_DST_CW_PUMP
        - HVAC-CHP_DST_COOLING_TOWER
      control_strategy:
        type: 一机一泵
        description: 冷却水泵与冷水机组联动

  # ========================================
  # CONTROL LOGIC SECTION - 控制逻辑定义
  # ========================================
  control_logic:
  
    system_startup_sequence:
      name: 制冷系统启动顺序
      mode: cooling
      sequence:
        - step: 1
          action: 启动冷却塔风机
          delay: 0s
        - step: 2
          action: 启动冷却水泵
          delay: 30s
          condition: 冷却塔风机运行确认
        - step: 3
          action: 启动冷水机组
          delay: 60s
          condition: 冷却水流量确认
        - step: 4
          action: 启动冷冻水一次泵
          delay: 30s
          condition: 冷水机组运行确认
        - step: 5
          action: 启动冷冻水二次泵
          delay: 30s
          condition: 一次泵运行确认
    
    system_shutdown_sequence:
      name: 制冷系统停机顺序
      mode: cooling
      sequence:
        - step: 1
          action: 停止冷冻水二次泵
          delay: 0s
        - step: 2
          action: 停止冷冻水一次泵
          delay: 30s
        - step: 3
          action: 停止冷水机组
          delay: 30s
        - step: 4
          action: 停止冷却水泵
          delay: 120s
          note: 延时散热
        - step: 5
          action: 停止冷却塔风机
          delay: 60s

    chiller_staging:
      name: 冷水机组台数控制
      control_logic: |
        1. 根据系统冷负荷计算需要的机组容量
        2. 机组加载：当运行机组负载率>85%且持续15分钟，加载一台机组
        3. 机组卸载：当运行机组负载率<50%且持续15分钟，卸载一台机组
        4. 机组轮换：累计运行时间均衡控制
        5. 故障切换：机组故障时自动启用备用机组

    secondary_pump_control:
      name: 二次泵变频控制
      control_variable: 供回水压差
      setpoint: 100kPa
      pid_parameters:
        kp: 1.5
        ki: 0.1
        kd: 0
      frequency_range: [25, 50]
      control_logic: |
        1. 实测压差低于设定值，提高频率
        2. 实测压差高于设定值，降低频率
        3. 最小频率限制25Hz
        4. 压差设定值可根据负荷情况优化

    bypass_valve_control:
      name: 旁通阀控制
      control_variable: 一二次侧流量差
      control_logic: |
        1. 监测一次侧流量和二次侧流量
        2. 当一次侧流量>二次侧流量时，开启旁通阀
        3. 旁通阀开度根据流量差进行PID调节
        4. 保证一次侧流量不低于机组最小流量要求

---

## 系统 1.2: HVAC-CHW 冷冻水输配系统

```yaml
System_Topology:

# ========================================
# IDENTITY SECTION - 系统标识
# ========================================
identity:
 system_id: HVAC-CHW
 system_name: 冷冻水输配系统
 system_name_en: Chilled Water Distribution System
 system_category: HVAC
 system_type: 水系统
 priority_level: P1-CRITICAL

 description: |
 医院冷冻水输配系统，负责将冷冻机房的冷冻水输送至各区域的空调末端设备。
 系统采用变流量控制，通过楼层/区域分支向各AHU、FCU供应7℃/12℃冷冻水。

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

 version: 1.0
 last_updated: 2024

# ========================================
# BOUNDARY SECTION - 系统边界
# ========================================
boundary:

 inputs:
 - boundary_id: HVAC-CHW_IN_001
 name: 冷冻水供水输入
 from_system: HVAC-CHP
 from_node: HVAC-CHP_SNK_CHW_RISER
 medium: CHW
 parameters:
 temperature: {value: 7, unit: ℃}
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
 name: 冷冻水末端接口(AHU)
 to_system: HVAC-AHU
 medium: CHW

 - boundary_id: HVAC-CHW_OUT_003
 name: 冷冻水末端接口(FCU)
 to_system: HVAC-FCU
 medium: CHW

# ========================================
# NODES SECTION - 节点定义
# ========================================
nodes:

 # === Source Nodes ===
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
 typical_quantity: 6-8 zones

 equipment_parameters:
 pipe_size: DN100-DN150
 isolation_valve: 电动蝶阀

 location_hint:
 space_type: SHAFT
 shaft_type: 空调水管井
 position: 每个区域立管底部

 # === Distribution Nodes ===
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

 equipment_parameters:
 material: 无缝钢管
 diameter: DN100-DN150
 insulation: 橡塑保温40mm

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
 material: 无缝钢管
 diameter: DN80-DN100
 outlets: 4-8路
 insulation: 橡塑保温30mm

 location_hint:
 space_type: SHAFT
 shaft_type: 空调水管井
 position: 每层管井内

 - node_id: HVAC-CHW_DST_BRANCH
 node_name: 楼层支管
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
 diameter: DN50-DN80
 insulation: 橡塑保温25mm

 location_hint:
 space_type: CEILING_VOID
 position: 走廊吊顶内

 - node_id: HVAC-CHW_DST_VALVE
 node_name: 动态平衡阀
 node_name_en: Dynamic Balancing Valve
 node_type: Distribution_Node
 node_subtype: REG
 node_category: DST

 function: 流量平衡调节
 medium_in: CHW
 medium_out: CHW

 multiplicity: multiple

 equipment_parameters:
 type: 动态压差平衡阀
 diameter: DN25-DN80
 differential_pressure_range: 20-400kPa

 control_points:
 sensors:
 - point_id: BAL_VALVE_FLOW
 point_name: 流量
 point_type: AI
 unit: "m³/h"

 location_hint:
 space_type: CEILING_VOID
 position: 立管分支处

 # === Sink Nodes ===
 sink_nodes:

 - node_id: HVAC-CHW_SNK_AHU_COIL
 node_name: 空调箱盘管接口
 node_name_en: AHU Coil Connection
 node_type: Sink_Node
 node_category: SNK

 function: 连接至空调箱冷冻水盘管
 medium_in: CHW
 medium_out: CHW

 multiplicity: multiple
 instance_pattern: HVAC-CHW_SNK_AHU_COIL_{Floor}_{Seq}

 downstream_system: HVAC-AHU

 interface_parameters:
 pipe_size: DN50-DN80
 control_valve: 电动二通阀

 location_hint:
 space_type: MEP_ROOM
 room_name: 空调机房

 - node_id: HVAC-CHW_SNK_FCU_COIL
 node_name: 风机盘管接口
 node_name_en: FCU Coil Connection
 node_type: Sink_Node
 node_category: SNK

 function: 连接至风机盘管冷冻水盘管
 medium_in: CHW
 medium_out: CHW

 multiplicity: multiple
 instance_pattern: HVAC-CHW_SNK_FCU_COIL_{Floor}_{Room}
 typical_quantity: 大量（按房间数）

 downstream_system: HVAC-FCU

 interface_parameters:
 pipe_size: DN20-DN32
 control_valve: 电动二通阀/电热阀

 location_hint:
 space_type: CEILING_VOID
 position: 各功能房间吊顶内

 - node_id: HVAC-CHW_SNK_PAU_COIL
 node_name: 新风机组盘管接口
 node_name_en: PAU Coil Connection
 node_type: Sink_Node
 node_category: SNK

 function: 连接至新风机组冷冻水盘管
 medium_in: CHW
 medium_out: CHW

 multiplicity: multiple
 instance_pattern: HVAC-CHW_SNK_PAU_COIL_{Floor}_{Seq}

 downstream_system: HVAC-PAU

 interface_parameters:
 pipe_size: DN40-DN65
 control_valve: 电动二通阀

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

 location_hint:
 space_type: SHAFT
 shaft_type: 空调水管井
 position: 每个区域立管底部

# ========================================
# EDGES SECTION - 边/连接定义
# ========================================
edges:

 supply_edges:

 - edge_id: HVAC-CHW_EDGE_001
 edge_name: 立管入口至立管
 edge_type: TRK
 from_node: HVAC-CHW_SRC_RISER_IN
 to_node: HVAC-CHW_DST_RISER
 direction: unidirectional
 medium: CHW

 - edge_id: HVAC-CHW_EDGE_002
 edge_name: 立管至楼层分水器
 edge_type: BRH
 from_node: HVAC-CHW_DST_RISER
 to_node: HVAC-CHW_DST_FLOOR_HEADER
 direction: unidirectional
 medium: CHW
 multiplicity: multiple

 - edge_id: HVAC-CHW_EDGE_003
 edge_name: 分水器至支管
 edge_type: BRH
 from_node: HVAC-CHW_DST_FLOOR_HEADER
 to_node: HVAC-CHW_DST_BRANCH
 direction: unidirectional
 medium: CHW
 multiplicity: multiple

 - edge_id: HVAC-CHW_EDGE_004
 edge_name: 支管至AHU接口
 edge_type: TRM
 from_node: HVAC-CHW_DST_BRANCH
 to_node: HVAC-CHW_SNK_AHU_COIL
 direction: unidirectional
 medium: CHW

 - edge_id: HVAC-CHW_EDGE_005
 edge_name: 支管至FCU接口
 edge_type: TRM
 from_node: HVAC-CHW_DST_BRANCH
 to_node: HVAC-CHW_SNK_FCU_COIL
 direction: unidirectional
 medium: CHW
 multiplicity: multiple

 - edge_id: HVAC-CHW_EDGE_006
 edge_name: 支管至PAU接口
 edge_type: TRM
 from_node: HVAC-CHW_DST_BRANCH
 to_node: HVAC-CHW_SNK_PAU_COIL
 direction: unidirectional
 medium: CHW

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
 edge_name: 支管回水至集水器
 edge_type: BRH
 from_node: HVAC-CHW_DST_BRANCH
 to_node: HVAC-CHW_DST_FLOOR_HEADER
 direction: unidirectional
 medium: CHW
 note: return_pipe

 - edge_id: HVAC-CHW_EDGE_014
 edge_name: 集水器至立管回水
 edge_type: TRK
 from_node: HVAC-CHW_DST_FLOOR_HEADER
 to_node: HVAC-CHW_DST_RISER
 direction: unidirectional
 medium: CHW
 note: return_pipe

 - edge_id: HVAC-CHW_EDGE_015
 edge_name: 立管回水至出口
 edge_type: TRK
 from_node: HVAC-CHW_DST_RISER
 to_node: HVAC-CHW_SNK_RISER_OUT
 direction: unidirectional
 medium: CHW
 note: return_pipe

# ========================================
# TYPICAL PATHS SECTION - 典型路径
# ========================================
typical_paths:

 - path_id: HVAC-CHW_PATH_TO_AHU
 path_name: 冷冻水至空调箱路径
 path_type: SUP
 sequence:
 - step: 1
 node: HVAC-CHW_SRC_RISER_IN
 action: 接收冷热源供水
 - step: 2
 node: HVAC-CHW_DST_RISER
 action: 垂直输送
 - step: 3
 node: HVAC-CHW_DST_FLOOR_HEADER
 action: 楼层分配
 - step: 4
 node: HVAC-CHW_DST_BRANCH
 action: 水平输送
 - step: 5
 node: HVAC-CHW_SNK_AHU_COIL
 action: 送达AHU盘管

 - path_id: HVAC-CHW_PATH_TO_FCU
 path_name: 冷冻水至风机盘管路径
 path_type: SUP
 sequence:
 - step: 1
 node: HVAC-CHW_SRC_RISER_IN
 action: 接收冷热源供水
 - step: 2
 node: HVAC-CHW_DST_RISER
 action: 垂直输送
 - step: 3
 node: HVAC-CHW_DST_FLOOR_HEADER
 action: 楼层分配
 - step: 4
 node: HVAC-CHW_DST_BRANCH
 action: 水平输送
 - step: 5
 node: HVAC-CHW_SNK_FCU_COIL
 action: 送达FCU盘管
```

---

## 系统 1.3: HVAC-HW 热水输配系统

```yaml
System_Topology:

identity:
 system_id: HVAC-HW
 system_name: 热水输配系统
 system_name_en: Hot Water Distribution System
 system_category: HVAC
 system_type: 水系统
 priority_level: P1-CRITICAL

 description: |
 医院热水输配系统，负责将锅炉房的空调热水输送至各区域的空调末端设备。
 系统采用变流量控制，通过楼层/区域分支向各AHU、FCU供应60℃/50℃热水。

 parent_system: HVAC-CHP
 child_systems:
 - HVAC-AHU
 - HVAC-FCU
 - HVAC-PAU

 version: 1.0
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
 pressure: {value: 0.35-0.45, unit: MPa}

 outputs:
 - boundary_id: HVAC-HW_OUT_001
 name: 热水回水输出
 to_system: HVAC-CHP
 medium: HW
 parameters:
 temperature: {value: 50, unit: ℃}

 - boundary_id: HVAC-HW_OUT_002
 name: 热水末端接口
 to_system: HVAC-AHU/FCU
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
 instance_pattern: HVAC-HW_DST_RISER_{Zone}_{S/R}

 equipment_parameters:
 material: 无缝钢管
 diameter: DN80-DN125
 insulation: 橡塑保温50mm

 location_hint:
 space_type: SHAFT
 shaft_type: 空调水管井

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
 instance_pattern: HVAC-HW_DST_FLOOR_HEADER_{Floor}_{Zone}

 equipment_parameters:
 material: 无缝钢管
 diameter: DN65-DN80
 outlets: 4-6路
 insulation: 橡塑保温40mm

 location_hint:
 space_type: SHAFT
 shaft_type: 空调水管井

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
 diameter: DN40-DN65
 insulation: 橡塑保温30mm

 location_hint:
 space_type: CEILING_VOID
 position: 走廊吊顶内

 sink_nodes:

 - node_id: HVAC-HW_SNK_AHU_COIL
 node_name: 空调箱热水盘管接口
 node_name_en: AHU HW Coil Connection
 node_type: Sink_Node
 node_category: SNK

 function: 连接至空调箱热水盘管
 medium_in: HW
 medium_out: HW

 multiplicity: multiple
 downstream_system: HVAC-AHU

 interface_parameters:
 pipe_size: DN40-DN65
 control_valve: 电动二通阀

 location_hint:
 space_type: MEP_ROOM
 room_name: 空调机房

 - node_id: HVAC-HW_SNK_FCU_COIL
 node_name: 风机盘管热水接口
 node_name_en: FCU HW Coil Connection
 node_type: Sink_Node
 node_category: SNK

 function: 连接至风机盘管热水盘管
 medium_in: HW
 medium_out: HW

 multiplicity: multiple
 downstream_system: HVAC-FCU

 interface_parameters:
 pipe_size: DN20-DN32
 control_valve: 电动二通阀/电热阀

 location_hint:
 space_type: CEILING_VOID

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
 shaft_type: 空调水管井

edges:

 supply_edges:
 - edge_id: HVAC-HW_EDGE_001
 edge_name: 立管入口至立管
 edge_type: TRK
 from_node: HVAC-HW_SRC_RISER_IN
 to_node: HVAC-HW_DST_RISER
 direction: unidirectional
 medium: HW

 - edge_id: HVAC-HW_EDGE_002
 edge_name: 立管至楼层分水器
 edge_type: BRH
 from_node: HVAC-HW_DST_RISER
 to_node: HVAC-HW_DST_FLOOR_HEADER
 direction: unidirectional
 medium: HW
 multiplicity: multiple

 - edge_id: HVAC-HW_EDGE_003
 edge_name: 分水器至支管
 edge_type: BRH
 from_node: HVAC-HW_DST_FLOOR_HEADER
 to_node: HVAC-HW_DST_BRANCH
 direction: unidirectional
 medium: HW

 - edge_id: HVAC-HW_EDGE_004
 edge_name: 支管至AHU接口
 edge_type: TRM
 from_node: HVAC-HW_DST_BRANCH
 to_node: HVAC-HW_SNK_AHU_COIL
 direction: unidirectional
 medium: HW

 - edge_id: HVAC-HW_EDGE_005
 edge_name: 支管至FCU接口
 edge_type: TRM
 from_node: HVAC-HW_DST_BRANCH
 to_node: HVAC-HW_SNK_FCU_COIL
 direction: unidirectional
 medium: HW
 multiplicity: multiple

 return_edges:
 - edge_id: HVAC-HW_EDGE_011
 edge_name: 末端回水至支管
 edge_type: TRM
 from_node: HVAC-HW_SNK_AHU_COIL
 to_node: HVAC-HW_DST_BRANCH
 direction: unidirectional
 medium: HW
 note: return_pipe

 - edge_id: HVAC-HW_EDGE_012
 edge_name: 支管回水至集水器
 edge_type: BRH
 from_node: HVAC-HW_DST_BRANCH
 to_node: HVAC-HW_DST_FLOOR_HEADER
 direction: unidirectional
 medium: HW
 note: return_pipe

 - edge_id: HVAC-HW_EDGE_013
 edge_name: 集水器至立管回水
 edge_type: TRK
 from_node: HVAC-HW_DST_FLOOR_HEADER
 to_node: HVAC-HW_DST_RISER
 direction: unidirectional
 medium: HW
 note: return_pipe

 - edge_id: HVAC-HW_EDGE_014
 edge_name: 立管回水至出口
 edge_type: TRK
 from_node: HVAC-HW_DST_RISER
 to_node: HVAC-HW_SNK_RISER_OUT
 direction: unidirectional
 medium: HW
 note: return_pipe

typical_paths:

 - path_id: HVAC-HW_PATH_TO_AHU
 path_name: 热水至空调箱路径
 path_type: SUP
 sequence:
 - step: 1
 node: HVAC-HW_SRC_RISER_IN
 action: 接收热水供水
 - step: 2
 node: HVAC-HW_DST_RISER
 action: 垂直输送
 - step: 3
 node: HVAC-HW_DST_FLOOR_HEADER
 action: 楼层分配
 - step: 4
 node: HVAC-HW_DST_BRANCH
 action: 水平输送
 - step: 5
 node: HVAC-HW_SNK_AHU_COIL
 action: 送达AHU热水盘管
```

---

## 系统 1.4: HVAC-AHU 空调箱系统

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

 design_standards:
 - GB 50736-2012 民用建筑供暖通风与空气调节设计规范
 - GB 51039-2014 综合医院建筑设计规范
 - GB 50333-2013 医院洁净手术部建筑技术规范

 version: 1.0
 last_updated: 2024

boundary:
 inputs:
 - boundary_id: HVAC-AHU_IN_001
 name: 室外新风
 from_system: EXTERNAL
 medium: AIR-OA
 parameters:
 condition: 室外状态

 - boundary_id: HVAC-AHU_IN_002
 name: 冷冻水供水
 from_system: HVAC-CHW
 medium: CHW

 - boundary_id: HVAC-AHU_IN_003
 name: 热水供水
 from_system: HVAC-HW
 medium: HW

 - boundary_id: HVAC-AHU_IN_004
 name: 蒸汽/加湿水
 from_system: PLUMB-HWS / STEAM
 medium: STEAM/WATER

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
 air_volume: {value: 5000-50000, unit: "m³/h"}
 external_static_pressure: {value: 400-800, unit: Pa}
 sections:
 - 新回风混合段
 - 初效过滤段
 - 表冷/加热段
 - 加湿段
 - 中效过滤段
 - 送风机段
 - 均流段
 - 消声段
 fan_type: 后向离心风机/EC风机
 motor_power: {value: 5.5-45, unit: kW}
 vfd: true

 control_points:
 sensors:
 - point_id: AHU_SAT
 point_name: 送风温度
 point_type: AI
 unit: ℃
 range: [0, 50]
 - point_id: AHU_RAT
 point_name: 回风温度
 point_type: AI
 unit: ℃
 range: [0, 50]
 - point_id: AHU_SAH
 point_name: 送风湿度
 point_type: AI
 unit: "%RH"
 range: [0, 100]
 - point_id: AHU_OAT
 point_name: 新风温度
 point_type: AI
 unit: ℃
 range: [-20, 50]
 - point_id: AHU_FILTER_DP
 point_name: 过滤器压差
 point_type: AI
 unit: Pa
 range: [0, 500]
 - point_id: AHU_FAN_FREQ
 point_name: 风机频率
 point_type: AI
 unit: Hz
 range: [0, 50]
 status:
 - point_id: AHU_FAN_RUN
 point_name: 风机运行状态
 point_type: DI
 - point_id: AHU_FAN_FAULT
 point_name: 风机故障状态
 point_type: DI
 - point_id: AHU_FILTER_ALARM
 point_name: 过滤器堵塞报警
 point_type: DI
 commands:
 - point_id: AHU_FAN_START
 point_name: 风机启停命令
 point_type: DO
 - point_id: AHU_OA_DAMPER
 point_name: 新风阀开度
 point_type: AO
 unit: "%"
 - point_id: AHU_RA_DAMPER
 point_name: 回风阀开度
 point_type: AO
 unit: "%"
 - point_id: AHU_CHW_VALVE
 point_name: 冷水阀开度
 point_type: AO
 unit: "%"
 - point_id: AHU_HW_VALVE
 point_name: 热水阀开度
 point_type: AO
 unit: "%"
 setpoints:
 - point_id: AHU_SAT_SP
 point_name: 送风温度设定
 point_type: AO
 unit: ℃
 - point_id: AHU_FAN_FREQ_SP
 point_name: 风机频率设定
 point_type: AO
 unit: Hz

 location_hint:
 space_type: MEP_ROOM
 room_name: 空调机房
 floor: 各楼层/设备层
 area_requirement: ">30m²/台"

 - node_id: HVAC-AHU_DST_SA_DUCT_MAIN
 node_name: 送风主风道
 node_name_en: Supply Air Main Duct
 node_type: Distribution_Node
 node_subtype: TRK
 node_category: DST

 function: 送风主管输送
 medium_in: AIR-SA
 medium_out: AIR-SA

 multiplicity: multiple

 equipment_parameters:
 type: 镀锌钢板风管
 thickness: 0.75-1.2mm
 insulation: 橡塑保温25mm（外保温）

 location_hint:
 space_type: CEILING_VOID
 position: 主走廊吊顶内

 - node_id: HVAC-AHU_DST_SA_DUCT_BRANCH
 node_name: 送风支风道
 node_name_en: Supply Air Branch Duct
 node_type: Distribution_Node
 node_subtype: BRH
 node_category: DST

 function: 送风支管分配
 medium_in: AIR-SA
 medium_out: AIR-SA

 multiplicity: multiple

 equipment_parameters:
 type: 镀锌钢板风管
 thickness: 0.6-0.75mm
 insulation: 橡塑保温20mm

 location_hint:
 space_type: CEILING_VOID
 position: 房间吊顶内

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
 control_signal: "0-10V"
 with_reheat: optional

 control_points:
 sensors:
 - point_id: VAV_FLOW
 point_name: 风量
 point_type: AI
 unit: "m³/h"
 - point_id: ZONE_TEMP
 point_name: 区域温度
 point_type: AI
 unit: ℃
 commands:
 - point_id: VAV_DAMPER
 point_name: 风阀开度
 point_type: AO
 unit: "%"
 setpoints:
 - point_id: ZONE_TEMP_SP
 point_name: 区域温度设定
 point_type: AO
 unit: ℃

 location_hint:
 space_type: CEILING_VOID
 position: 送风支管上

 - node_id: HVAC-AHU_DST_RA_DUCT
 node_name: 回风风道
 node_name_en: Return Air Duct
 node_type: Distribution_Node
 node_subtype: TRK
 node_category: DST

 function: 回风输送
 medium_in: AIR-RA
 medium_out: AIR-RA

 multiplicity: multiple

 equipment_parameters:
 type: 镀锌钢板风管
 thickness: 0.6-0.75mm
 insulation: 无/局部保温

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
 typical_quantity: 大量

 equipment_parameters:
 type: 散流器/格栅风口/旋流风口
 material: 铝合金
 sizes: 300x300, 600x600等
 adjustable: true

 location_hint:
 space_type: CEILING
 position: 各功能房间天花

 - node_id: HVAC-AHU_SNK_EA_OUTLET
 node_name: 排风出口
 node_name_en: Exhaust Air Outlet
 node_type: Sink_Node
 node_category: SNK

 function: 排风排放
 medium_in: AIR-EA
 medium_out: AIR-EA (to outdoor)

 is_boundary_output: true

 multiplicity: multiple

 equipment_parameters:
 type: 防雨百叶
 material: 铝合金

 location_hint:
 space_type: EXTERIOR
 position: 建筑外墙/屋面

edges:

 supply_edges:
 - edge_id: HVAC-AHU_EDGE_001
 edge_name: 新风口至AHU
 edge_type: TRK
 from_node: HVAC-AHU_SRC_OA_INTAKE
 to_node: HVAC-AHU_DST_AHU
 direction: unidirectional
 medium: AIR-OA

 - edge_id: HVAC-AHU_EDGE_002
 edge_name: 回风口至AHU
 edge_type: TRK
 from_node: HVAC-AHU_SRC_RA_GRILLE
 to_node: HVAC-AHU_DST_RA_DUCT
 direction: unidirectional
 medium: AIR-RA

 - edge_id: HVAC-AHU_EDGE_003
 edge_name: 回风管至AHU
 edge_type: TRK
 from_node: HVAC-AHU_DST_RA_DUCT
 to_node: HVAC-AHU_DST_AHU
 direction: unidirectional
 medium: AIR-RA

 - edge_id: HVAC-AHU_EDGE_004
 edge_name: AHU至送风主管
 edge_type: TRK
 from_node: HVAC-AHU_DST_AHU
 to_node: HVAC-AHU_DST_SA_DUCT_MAIN
 direction: unidirectional
 medium: AIR-SA

 - edge_id: HVAC-AHU_EDGE_005
 edge_name: 主管至支管
 edge_type: BRH
 from_node: HVAC-AHU_DST_SA_DUCT_MAIN
 to_node: HVAC-AHU_DST_SA_DUCT_BRANCH
 direction: unidirectional
 medium: AIR-SA
 multiplicity: multiple

 - edge_id: HVAC-AHU_EDGE_006
 edge_name: 支管至VAV
 edge_type: TRM
 from_node: HVAC-AHU_DST_SA_DUCT_BRANCH
 to_node: HVAC-AHU_DST_VAV
 direction: unidirectional
 medium: AIR-SA

 - edge_id: HVAC-AHU_EDGE_007
 edge_name: VAV至送风口
 edge_type: TRM
 from_node: HVAC-AHU_DST_VAV
 to_node: HVAC-AHU_SNK_SA_DIFFUSER
 direction: unidirectional
 medium: AIR-SA
 multiplicity: multiple

typical_paths:

 - path_id: HVAC-AHU_PATH_SUPPLY
 path_name: 空调箱送风路径
 path_type: SUP
 sequence:
 - step: 1
 node: HVAC-AHU_SRC_OA_INTAKE
 action: 新风采集
 - step: 2
 node: HVAC-AHU_DST_AHU
 action: 空气处理（混合、过滤、调温调湿）
 - step: 3
 node: HVAC-AHU_DST_SA_DUCT_MAIN
 action: 主风道输送
 - step: 4
 node: HVAC-AHU_DST_SA_DUCT_BRANCH
 action: 支风道分配
 - step: 5
 node: HVAC-AHU_DST_VAV
 action: 风量调节
 - step: 6
 node: HVAC-AHU_SNK_SA_DIFFUSER
 action: 送入房间

 - path_id: HVAC-AHU_PATH_RETURN
 path_name: 空调箱回风路径
 path_type: RET
 sequence:
 - step: 1
 node: HVAC-AHU_SRC_RA_GRILLE
 action: 回风采集
 - step: 2
 node: HVAC-AHU_DST_RA_DUCT
 action: 回风输送
 - step: 3
 node: HVAC-AHU_DST_AHU
 action: 进入AHU混合

control_logic:

 supply_air_temp_control:
 name: 送风温度控制
 control_logic: |
 1. PID控制冷/热水阀开度维持送风温度设定值
 2. 夏季：调节冷水阀，送风温度目标12-16℃
 3. 冬季：调节热水阀，送风温度目标30-40℃
 4. 过渡季：优先利用新风免费冷却

 fresh_air_ratio_control:
 name: 新风比控制
 control_logic: |
 1. 最小新风量保证（按人员或面积计算）
 2. 过渡季节全新风运行（新风温度适宜时）
 3. CO2浓度监测调节新风量（需求控制通风）
 4. 新风阀与回风阀、排风阀联动

 vav_control:
 name: VAV末端控制
 control_logic: |
 1. 区域温度反馈控制风阀开度
 2. 最小风量设定（换气次数保证）
 3. 静压复位优化AHU风机能耗
```

---

## 系统 1.5: HVAC-FCU 风机盘管系统

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
 医院风机盘管系统，用于病房、办公室、诊室等小空间的分散式空调。
 风机盘管接收冷/热水，配合新风系统为房间提供空调效果。
 采用两管制或四管制系统，支持房间独立温度控制。

 parent_system: HVAC-CHW / HVAC-HW

 version: 1.0
 last_updated: 2024

boundary:
 inputs:
 - boundary_id: HVAC-FCU_IN_001
 name: 冷冻水供水
 from_system: HVAC-CHW
 medium: CHW

 - boundary_id: HVAC-FCU_IN_002
 name: 热水供水（四管制）
 from_system: HVAC-HW
 medium: HW

 - boundary_id: HVAC-FCU_IN_003
 name: 新风
 from_system: HVAC-PAU
 medium: AIR-OA

 outputs:
 - boundary_id: HVAC-FCU_OUT_001
 name: 送风
 to_system: 空调房间
 medium: AIR-SA

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

 source_system: HVAC-CHW

 location_hint:
 space_type: CEILING_VOID

 - node_id: HVAC-FCU_SRC_HW_IN
 node_name: 热水供水接口
 node_name_en: HW Supply Connection
 node_type: Source_Node
 node_category: SRC

 function: 接收热水（四管制时）
 medium_in: HW
 medium_out: HW

 source_system: HVAC-HW
 optional: true # 两管制时无此节点

 location_hint:
 space_type: CEILING_VOID

 - node_id: HVAC-FCU_SRC_OA_IN
 node_name: 新风接口
 node_name_en: Fresh Air Connection
 node_type: Source_Node
 node_category: SRC

 function: 接收处理后的新风
 medium_in: AIR-OA
 medium_out: AIR-OA

 source_system: HVAC-PAU

 location_hint:
 space_type: CEILING_VOID

 distribution_nodes:

 - node_id: HVAC-FCU_DST_FCU
 node_name: 风机盘管
 node_name_en: Fan Coil Unit
 node_type: Distribution_Node
 node_subtype: TRF
 node_category: DST

 function: 房间空气冷却/加热
 medium_in: [CHW, HW, AIR-RA]
 medium_out: AIR-SA

 multiplicity: multiple
 instance_pattern: HVAC-FCU_DST_FCU_{Floor}_{Room}
 typical_quantity: 大量（按房间数）

 equipment_parameters:
 type: 卧式暗装/立式明装/卡式
 cooling_capacity: {value: 2.5-7.1, unit: kW}
 heating_capacity: {value: 3.0-8.5, unit: kW}
 air_volume: {value: 340-1700, unit: "m³/h"}
 fan_speed: 三档调速/无级变速
 coil_rows: 2排或3排
 water_pressure_drop: {value: 20-40, unit: kPa}
 noise_level: "<40dB(A)"

 control_points:
 sensors:
 - point_id: FCU_ROOM_TEMP
 point_name: 房间温度
 point_type: AI
 unit: ℃
 range: [0, 40]
 status:
 - point_id: FCU_RUN
 point_name: FCU运行状态
 point_type: DI
 commands:
 - point_id: FCU_FAN_SPEED
 point_name: 风机档位
 point_type: AO
 unit: "档位"
 - point_id: FCU_CHW_VALVE
 point_name: 冷水阀
 point_type: DO/AO
 - point_id: FCU_HW_VALVE
 point_name: 热水阀
 point_type: DO/AO
 setpoints:
 - point_id: FCU_ROOM_TEMP_SP
 point_name: 房间温度设定
 point_type: AO
 unit: ℃
 range: [18, 28]

 location_hint:
 space_type: CEILING_VOID
 position: 各功能房间吊顶内
 alternatives:
 - 窗下地面（立式）
 - 吊顶中央（卡式）

 sink_nodes:

 - node_id: HVAC-FCU_SNK_SA_OUTLET
 node_name: 送风口
 node_name_en: Supply Air Outlet
 node_type: Sink_Node
 node_category: SNK

 function: 向房间送风
 medium_in: AIR-SA
 medium_out: AIR-SA (to room)

 multiplicity: multiple
 instance_pattern: HVAC-FCU_SNK_SA_OUTLET_{Floor}_{Room}

 equipment_parameters:
 type: 铝合金送风口/风口面板
 size: 与FCU匹配

 location_hint:
 space_type: CEILING
 position: 房间天花

 - node_id: HVAC-FCU_SNK_RA_INLET
 node_name: 回风口
 node_name_en: Return Air Inlet
 node_type: Sink_Node
 node_category: SNK

 function: 房间回风入口
 medium_in: AIR-RA
 medium_out: AIR-RA (to FCU)

 multiplicity: multiple

 equipment_parameters:
 type: 回风格栅/FCU回风口

 location_hint:
 space_type: CEILING
 position: FCU回风侧

 - node_id: HVAC-FCU_SNK_CHW_OUT
 node_name: 冷冻水回水接口
 node_name_en: CHW Return Connection
 node_type: Sink_Node
 node_category: SNK

 function: 冷冻水回水
 medium_in: CHW
 medium_out: CHW

 target_system: HVAC-CHW

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
 medium: AIR-OA

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
 sequence:
 - step: 1
 node: HVAC-FCU_SRC_OA_IN
 action: 新风送入
 - step: 2
 node: HVAC-FCU_SNK_RA_INLET
 action: 回风吸入
 - step: 3
 node: HVAC-FCU_DST_FCU
 action: 混合、冷却/加热
 - step: 4
 node: HVAC-FCU_SNK_SA_OUTLET
 action: 送入房间

control_logic:

 room_temperature_control:
 name: 房间温度控制
 control_logic: |
 1. 房间温度传感器反馈控制
 2. 与温度设定值比较，调节水阀开度
 3. 两管制：季节切换冷/热水
 4. 四管制：同时供冷热水，自动选择
 5. 风机档位根据负荷调节

 occupancy_control:
 name: 人员感应控制
 control_logic: |
 1. 人体感应器检测房间占用
 2. 无人时降低运行档位或停机
 3. 有人时恢复设定运行状态
 4. 配合门窗开关联动
```

---

## 系统 1.6: HVAC-PAU 新风机组系统

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
 是保证医院室内空气品质和正压控制的关键系统。

 parent_system: HVAC-CHW / HVAC-HW
 child_systems:
 - HVAC-FCU

 design_standards:
 - GB 50736-2012 民用建筑供暖通风与空气调节设计规范
 - GB 51039-2014 综合医院建筑设计规范

 version: 1.0
 last_updated: 2024

boundary:
 inputs:
 - boundary_id: HVAC-PAU_IN_001
 name: 室外新风
 from_system: EXTERNAL
 medium: AIR-OA

 - boundary_id: HVAC-PAU_IN_002
 name: 冷冻水供水
 from_system: HVAC-CHW
 medium: CHW

 - boundary_id: HVAC-PAU_IN_003
 name: 热水供水
 from_system: HVAC-HW
 medium: HW

 outputs:
 - boundary_id: HVAC-PAU_OUT_001
 name: 处理后新风
 to_system: HVAC-FCU / 房间
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

 equipment_parameters:
 type: 防雨百叶
 material: 铝合金
 mesh: 防虫网

 location_hint:
 space_type: EXTERIOR
 position: 建筑外墙
 height_requirement: ">3m from ground"

 installation_requirements:
 - 远离排风口≥10m
 - 远离污染源
 - 远离冷却塔

 distribution_nodes:

 - node_id: HVAC-PAU_DST_PAU
 node_name: 新风机组
 node_name_en: Primary Air Unit
 node_type: Distribution_Node
 node_subtype: TRF
 node_category: DST

 function: 新风处理（过滤、调温调湿）
 medium_in: [AIR-OA, CHW, HW]
 medium_out: AIR-SA

 multiplicity: multiple
 instance_pattern: HVAC-PAU_DST_PAU_{Floor}_{Seq}

 equipment_parameters:
 type: 全新风空调机组
 air_volume: {value: 2000-20000, unit: "m³/h"}
 external_static_pressure: {value: 300-600, unit: Pa}
 sections:
 - 新风段
 - 初效过滤段
 - 表冷/加热段
 - 加湿段（可选）
 - 中效过滤段
 - 送风机段
 - 消声段
 fan_type: 后向离心风机/EC风机
 vfd: true
 heat_recovery: optional # 可选配热回收

 control_points:
 sensors:
 - point_id: PAU_SAT
 point_name: 送风温度
 point_type: AI
 unit: ℃
 - point_id: PAU_SAH
 point_name: 送风湿度
 point_type: AI
 unit: "%RH"
 - point_id: PAU_OAT
 point_name: 新风温度
 point_type: AI
 unit: ℃
 - point_id: PAU_FILTER_DP
 point_name: 过滤器压差
 point_type: AI
 unit: Pa
 status:
 - point_id: PAU_FAN_RUN
 point_name: 风机运行状态
 point_type: DI
 - point_id: PAU_FAN_FAULT
 point_name: 风机故障状态
 point_type: DI
 commands:
 - point_id: PAU_FAN_START
 point_name: 风机启停命令
 point_type: DO
 - point_id: PAU_CHW_VALVE
 point_name: 冷水阀开度
 point_type: AO
 unit: "%"
 - point_id: PAU_HW_VALVE
 point_name: 热水阀开度
 point_type: AO
 unit: "%"
 setpoints:
 - point_id: PAU_SAT_SP
 point_name: 送风温度设定
 point_type: AO
 unit: ℃

 location_hint:
 space_type: MEP_ROOM
 room_name: 新风机房
 floor: 各楼层
 area_requirement: ">15m²/台"

 - node_id: HVAC-PAU_DST_SA_DUCT
 node_name: 新风管道
 node_name_en: Fresh Air Duct
 node_type: Distribution_Node
 node_subtype: TRK
 node_category: DST

 function: 新风输送
 medium_in: AIR-SA
 medium_out: AIR-SA

 multiplicity: multiple

 equipment_parameters:
 type: 镀锌钢板风管
 thickness: 0.6-1.0mm
 insulation: 橡塑保温25mm

 location_hint:
 space_type: CEILING_VOID

 sink_nodes:

 - node_id: HVAC-PAU_SNK_FCU_OA
 node_name: FCU新风接口
 node_name_en: FCU Fresh Air Connection
 node_type: Sink_Node
 node_category: SNK

 function: 新风送至FCU混合
 medium_in: AIR-SA
 medium_out: AIR-SA

 multiplicity: multiple
 instance_pattern: HVAC-PAU_SNK_FCU_OA_{Floor}_{Room}

 target_system: HVAC-FCU

 equipment_parameters:
 connection: 送风软管/静压箱

 location_hint:
 space_type: CEILING_VOID

 - node_id: HVAC-PAU_SNK_SA_DIFFUSER
 node_name: 新风送风口
 node_name_en: Fresh Air Diffuser
 node_type: Sink_Node
 node_category: SNK

 function: 新风直接送入房间
 medium_in: AIR-SA
 medium_out: AIR-SA (to room)

 multiplicity: multiple

 equipment_parameters:
 type: 散流器/送风口

 location_hint:
 space_type: CEILING

edges:

 supply_edges:
 - edge_id: HVAC-PAU_EDGE_001
 edge_name: 新风口至PAU
 edge_type: TRK
 from_node: HVAC-PAU_SRC_OA_INTAKE
 to_node: HVAC-PAU_DST_PAU
 direction: unidirectional
 medium: AIR-OA

 - edge_id: HVAC-PAU_EDGE_002
 edge_name: PAU至新风管道
 edge_type: TRK
 from_node: HVAC-PAU_DST_PAU
 to_node: HVAC-PAU_DST_SA_DUCT
 direction: unidirectional
 medium: AIR-SA

 - edge_id: HVAC-PAU_EDGE_003
 edge_name: 新风管至FCU接口
 edge_type: TRM
 from_node: HVAC-PAU_DST_SA_DUCT
 to_node: HVAC-PAU_SNK_FCU_OA
 direction: unidirectional
 medium: AIR-SA
 multiplicity: multiple

 - edge_id: HVAC-PAU_EDGE_004
 edge_name: 新风管至送风口
 edge_type: TRM
 from_node: HVAC-PAU_DST_SA_DUCT
 to_node: HVAC-PAU_SNK_SA_DIFFUSER
 direction: unidirectional
 medium: AIR-SA
 multiplicity: multiple

typical_paths:

 - path_id: HVAC-PAU_PATH_TO_FCU
 path_name: 新风至FCU路径
 path_type: SUP
 sequence:
 - step: 1
 node: HVAC-PAU_SRC_OA_INTAKE
 action: 新风采集
 - step: 2
 node: HVAC-PAU_DST_PAU
 action: 新风处理
 - step: 3
 node: HVAC-PAU_DST_SA_DUCT
 action: 新风输送
 - step: 4
 node: HVAC-PAU_SNK_FCU_OA
 action: 送达FCU
```

---

# 第一批次输出完成

## 批次总结

| 系统ID | 系统名称 | 节点数 | 边数 | 典型路径数 |
|--------|----------|--------|------|------------|
| HVAC-CHP | 冷热源系统 | ~18 | ~16 | 5 |
| HVAC-CHW | 冷冻水输配系统 | ~10 | ~10 | 2 |
| HVAC-HW | 热水输配系统 | ~9 | ~9 | 1 |
| HVAC-AHU | 空调箱系统 | ~12 | ~7 | 2 |
| HVAC-FCU | 风机盘管系统 | ~8 | ~5 | 1 |
| HVAC-PAU | 新风机组系统 | ~6 | ~4 | 1 |

**下一批次预告：** Batch 2 将输出电气系统（ELEC-HV、ELEC-LV-MAIN、ELEC-EPS）和医疗气体核心系统（MGAS-O2、MGAS-VAC、MGAS-AIR、MGAS-N2O）。

---

请确认第一批次内容后，我将继续输出第二批次。

---