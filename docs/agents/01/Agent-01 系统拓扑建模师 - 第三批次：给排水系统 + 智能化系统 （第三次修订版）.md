# Agent-01 系统拓扑建模师 - 第三批次：给排水系统 + 智能化系统 （第三次修订版）

## 第三批次：给排水系统 + 智能化系统（6个系统）

---

# 给排水系统（3个系统）

## 系统 3.1: PLUMB-DWS 生活给水系统

```yaml
System_Topology:

  # ========================================
  # IDENTITY SECTION - 系统标识
  # ========================================
  identity:
    system_id: PLUMB-DWS
    system_name: 生活给水系统
    system_name_en: Domestic Water Supply System
    system_category: PLUMB
    system_type: 给水
    priority_level: P1-CRITICAL
  
    description: |
      医院生活给水系统，为全院提供符合饮用水标准的冷水。
      系统采用市政供水+变频加压方式，设置高位水箱或气压罐保证供水稳定性。
      供水范围包括卫生洁具、饮用水点、医疗辅助用水等。
      医院对水质和供水可靠性要求高，需设置水质消毒和备用供水措施。
  
    design_basis:
      water_source: 市政自来水（双路进水）
      supply_pressure: 
        municipal: {value: "0.25-0.35", unit: MPa}
        building_min: {value: 0.1, unit: MPa, note: "最不利点"}
        building_max: {value: 0.35, unit: MPa, note: "卫生洁具最大"}
      water_quality: GB 5749-2022 生活饮用水卫生标准
      daily_consumption: {value: 400, unit: "L/(床·d)", note: "综合医院用水定额"}
      peak_hour_factor: 2.5
      fire_reserve: 与消防水池分开设置
  
    child_systems:
      - PLUMB-HWS  # 热水系统
    
    related_systems:
      - MGAS-AIR   # 医用压缩空气用水
      - HVAC-CHP   # 冷却塔补水
      - FIRE-SPS   # 消防水池补水
  
    design_standards:
      - GB 50015-2019 建筑给水排水设计标准
      - GB 50849-2014 传染病医院建筑设计规范
      - GB 51039-2014 综合医院建筑设计规范
      - GB 5749-2022 生活饮用水卫生标准
      - CJJ 140-2010 二次供水工程技术规程
  
    version: 1.0
    last_updated: 2024

  # ========================================
  # BOUNDARY SECTION - 系统边界
  # ========================================
  boundary:
  
    inputs:
      - boundary_id: PLUMB-DWS_IN_001
        name: 市政给水一路
        from_system: EXTERNAL_MUNICIPAL_WATER_1
        medium: WATER-PW
        parameters:
          pressure: {value: "0.25-0.35", unit: MPa}
          quality: 符合GB 5749
        
      - boundary_id: PLUMB-DWS_IN_002
        name: 市政给水二路
        from_system: EXTERNAL_MUNICIPAL_WATER_2
        medium: WATER-PW
        parameters:
          pressure: {value: "0.25-0.35", unit: MPa}
        note: 双路供水保证可靠性
      
      - boundary_id: PLUMB-DWS_IN_003
        name: 电力供应
        from_system: ELEC-LV-MAIN
        medium: ELEC-LV
        note: 加压泵电源
      
    outputs:
      - boundary_id: PLUMB-DWS_OUT_001
        name: 卫生洁具冷水
        to_system: 卫生间/开水间
        medium: WATER-PW
        parameters:
          pressure: {value: "0.1-0.35", unit: MPa}
        
      - boundary_id: PLUMB-DWS_OUT_002
        name: 热水系统冷水源
        to_system: PLUMB-HWS
        to_node: PLUMB-HWS_SRC_CW_IN
        medium: WATER-PW
      
      - boundary_id: PLUMB-DWS_OUT_003
        name: 冷却塔补水
        to_system: HVAC-CHP
        medium: WATER-PW
      
      - boundary_id: PLUMB-DWS_OUT_004
        name: 直饮水系统
        to_system: 直饮水机
        medium: WATER-PW

  # ========================================
  # NODES SECTION - 节点定义
  # ========================================
  nodes:

    source_nodes:
  
      - node_id: PLUMB-DWS_SRC_MUNICIPAL_1
        node_name: 市政给水接口一
        node_name_en: Municipal Water Connection 1
        node_type: Source_Node
        node_category: SRC
      
        function: 接收市政自来水（一路）
        medium_in: WATER-PW
        medium_out: WATER-PW
      
        is_boundary_input: true
        source: 市政供水管网
      
        equipment_parameters:
          pipe_size: {value: "DN150-DN200", unit: mm}
          water_meter: 
            type: 远传水表（IC卡/NB-IoT）
            size: DN150
            accuracy: ±2%
          isolation_valve: 闸阀/蝶阀
          check_valve: 倒流防止器
          strainer: Y型过滤器
        
        control_points:
          sensors:
            - point_id: MW1_FLOW
              point_name: 进水流量
              point_type: AI
              unit: "m³/h"
              range: [0, 200]
            - point_id: MW1_PRESSURE
              point_name: 进水压力
              point_type: AI
              unit: MPa
              range: [0, 0.6]
            - point_id: MW1_TOTAL_FLOW
              point_name: 累计用水量
              point_type: AI
              unit: "m³"
          status:
            - point_id: MW1_AVAILABLE
              point_name: 一路供水正常
              point_type: DI
            - point_id: MW1_LOW_PRESSURE
              point_name: 一路低压报警
              point_type: DI
      
        location_hint:
          space_type: OUTDOOR
          position: 建筑红线内，市政接驳点
          depth: 地下埋设
        
        installation_requirements:
          - 设置水表井
          - 倒流防止器（防止污染市政管网）
          - 与消防引入管分开设置
          - 间距符合规范要求

      - node_id: PLUMB-DWS_SRC_MUNICIPAL_2
        node_name: 市政给水接口二
        node_name_en: Municipal Water Connection 2
        node_type: Source_Node
        node_category: SRC
      
        function: 接收市政自来水（二路）
        medium_in: WATER-PW
        medium_out: WATER-PW
      
        is_boundary_input: true
      
        equipment_parameters:
          pipe_size: {value: "DN150-DN200", unit: mm}
          water_meter: 远传水表
        
        control_points:
          sensors:
            - point_id: MW2_FLOW
              point_name: 进水流量
              point_type: AI
              unit: "m³/h"
            - point_id: MW2_PRESSURE
              point_name: 进水压力
              point_type: AI
              unit: MPa
          status:
            - point_id: MW2_AVAILABLE
              point_name: 二路供水正常
              point_type: DI
      
        location_hint:
          space_type: OUTDOOR
          position: 与一路分开引入

    distribution_nodes:
  
      - node_id: PLUMB-DWS_DST_TANK
        node_name: 生活水箱
        node_name_en: Domestic Water Tank
        node_type: Distribution_Node
        node_subtype: BUF
        node_category: DST
      
        function: 储存生活用水，调节供需
        medium_in: WATER-PW
        medium_out: WATER-PW
      
        equipment_parameters:
          type: 不锈钢组合式水箱
          material: SUS304不锈钢
          volume: 
            effective: {value: 100, unit: "m³", note: "按日用水量10-15%"}
            total: {value: 120, unit: "m³"}
          dimensions: "10m×6m×2m（L×W×H）"
          configuration: 分格设置（至少2格），便于清洗检修
          accessories:
            - 进水浮球阀/电动阀
            - 溢流管（DN100，设防虫网）
            - 排污管（DN80）
            - 通气管（DN50，设防虫网）
            - 液位计
            - 人孔（带锁）
          insulation: 必要时保温防冻
        
        water_quality_protection:
          - 水箱顶部高于周围地面500mm
          - 设置防污染措施
          - 定期清洗消毒（每半年至少一次）
          - 水质监测
      
        control_points:
          sensors:
            - point_id: TANK_LEVEL
              point_name: 水箱液位
              point_type: AI
              unit: "%"
              range: [0, 100]
            - point_id: TANK_LEVEL_M
              point_name: 水箱液位（米）
              point_type: AI
              unit: m
              range: [0, 2.5]
            - point_id: TANK_TEMP
              point_name: 水箱水温
              point_type: AI
              unit: ℃
              range: [0, 40]
            - point_id: TANK_CHLORINE
              point_name: 余氯浓度
              point_type: AI
              unit: "mg/L"
              range: [0, 1]
              note: 水质监测（可选）
          status:
            - point_id: TANK_HIGH_LEVEL
              point_name: 高液位报警
              point_type: DI
            - point_id: TANK_LOW_LEVEL
              point_name: 低液位报警
              point_type: DI
            - point_id: TANK_OVERFLOW
              point_name: 溢流报警
              point_type: DI
          commands:
            - point_id: TANK_INLET_VALVE
              point_name: 进水阀控制
              point_type: DO
              note: 电动进水阀（备用）
      
        level_settings:
          high_level: {value: 95, unit: "%", action: "关闭进水阀，报警"}
          start_filling: {value: 70, unit: "%", action: "开启进水阀"}
          stop_filling: {value: 90, unit: "%", action: "关闭进水阀"}
          low_level: {value: 30, unit: "%", action: "报警"}
          emergency_low: {value: 15, unit: "%", action: "停泵保护，紧急报警"}
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 生活水泵房/水箱间
          floor: B1或屋顶
          note: 不宜设在有污染风险的区域上方

      - node_id: PLUMB-DWS_DST_PUMP_STATION
        node_name: 生活给水加压泵组
        node_name_en: Domestic Water Booster Pump Station
        node_type: Distribution_Node
        node_subtype: PMP
        node_category: DST
      
        function: 加压供水至各楼层
        medium_in: WATER-PW
        medium_out: WATER-PW
      
        equipment_parameters:
          type: 变频恒压供水设备
          pump_type: 立式多级离心泵
          quantity: "3台（两用一备）"
          single_flow: {value: 50, unit: "m³/h"}
          single_head: {value: 60, unit: m}
          motor_power: {value: 15, unit: kW}
          vfd: 
            type: 变频器
            quantity: 2台
            control: 恒压变频控制
          pressure_tank:
            type: 隔膜式气压罐
            volume: {value: 500, unit: L}
            preset_pressure: {value: 0.4, unit: MPa}
          base: 混凝土基础+减振垫
        
        control_mode:
          primary: 恒压变频控制
          setpoint: {value: 0.45, unit: MPa, note: "出口恒压"}
          logic: |
            1. 一台泵变频运行，根据压力调节转速
            2. 流量增大，频率达上限时，启动第二台工频
            3. 流量减小，停止工频泵
            4. 定期轮换主备泵
      
        control_points:
          sensors:
            - point_id: PUMP_OUT_PRESSURE
              point_name: 出口压力
              point_type: AI
              unit: MPa
              range: [0, 1.0]
            - point_id: PUMP_IN_PRESSURE
              point_name: 进口压力
              point_type: AI
              unit: MPa
              range: [0, 0.5]
            - point_id: PUMP1_CURRENT
              point_name: 1#泵电流
              point_type: AI
              unit: A
            - point_id: PUMP2_CURRENT
              point_name: 2#泵电流
              point_type: AI
              unit: A
            - point_id: PUMP3_CURRENT
              point_name: 3#泵电流
              point_type: AI
              unit: A
            - point_id: PUMP_FLOW
              point_name: 供水流量
              point_type: AI
              unit: "m³/h"
            - point_id: VFD_FREQ
              point_name: 变频器频率
              point_type: AI
              unit: Hz
          status:
            - point_id: PUMP1_RUN
              point_name: 1#泵运行
              point_type: DI
            - point_id: PUMP2_RUN
              point_name: 2#泵运行
              point_type: DI
            - point_id: PUMP3_RUN
              point_name: 3#泵运行
              point_type: DI
            - point_id: PUMP1_FAULT
              point_name: 1#泵故障
              point_type: DI
            - point_id: PUMP2_FAULT
              point_name: 2#泵故障
              point_type: DI
            - point_id: PUMP3_FAULT
              point_name: 3#泵故障
              point_type: DI
            - point_id: VFD_FAULT
              point_name: 变频器故障
              point_type: DI
            - point_id: PUMP_LOW_PRESSURE
              point_name: 出口低压报警
              point_type: DI
            - point_id: PUMP_HIGH_PRESSURE
              point_name: 出口高压报警
              point_type: DI
          commands:
            - point_id: PUMP1_START
              point_name: 1#泵启动
              point_type: DO
            - point_id: PUMP2_START
              point_name: 2#泵启动
              point_type: DO
            - point_id: PUMP3_START
              point_name: 3#泵启动
              point_type: DO
            - point_id: PUMP_MODE
              point_name: 控制模式
              point_type: DO
              values: [AUTO, MANUAL]
          setpoints:
            - point_id: PUMP_PRESSURE_SP
              point_name: 出口压力设定
              point_type: AO
              unit: MPa
              range: [0.3, 0.6]
              default: 0.45
      
        protection:
          dry_run: 
            detection: 进口压力<0.05MPa
            action: 停泵保护
          overcurrent:
            detection: 电流>额定值120%
            action: 跳闸保护
          low_pressure:
            detection: 出口压力<0.25MPa持续30秒
            action: 报警
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 生活水泵房
          floor: B1
          area_requirement: {value: ">40", unit: "m²"}
        
        installation_requirements:
          - 减振基础
          - 软接头
          - 压力表/止回阀/闸阀
          - 排水设施
          - 通风设施

      - node_id: PLUMB-DWS_DST_RISER
        node_name: 给水立管
        node_name_en: Water Supply Riser
        node_type: Distribution_Node
        node_subtype: TRK
        node_category: DST
      
        function: 垂直输送给水至各楼层
        medium_in: WATER-PW
        medium_out: WATER-PW
      
        multiplicity: multiple
        instance_pattern: PLUMB-DWS_DST_RISER_{Zone}_{Seq}
        typical_quantity: {value: "10-20", unit: "根", note: "按分区"}
      
        equipment_parameters:
          material: 
            options:
              - 不锈钢管（薄壁）
              - PPR管
              - 衬塑钢管
            recommended: 不锈钢管
          diameter: {value: "DN50-DN100", unit: mm}
          connection: 
            stainless: 卡压连接/焊接
            ppr: 热熔连接
          insulation: 
            type: 橡塑保温
            thickness: {value: 20, unit: mm}
            purpose: 防结露
          support: 每层设管道支架
        
        location_hint:
          space_type: SHAFT
          shaft_type: 给排水管井
          position: 靠近用水点

      - node_id: PLUMB-DWS_DST_FLOOR_HEADER
        node_name: 楼层给水横管
        node_name_en: Floor Water Distribution Pipe
        node_type: Distribution_Node
        node_subtype: BRH
        node_category: DST
      
        function: 楼层内水平输送至各用水点
        medium_in: WATER-PW
        medium_out: WATER-PW
      
        multiplicity: multiple
        instance_pattern: PLUMB-DWS_DST_FLOOR_{Floor}_{Zone}
      
        equipment_parameters:
          material: 不锈钢管/PPR管
          diameter: {value: "DN25-DN50", unit: mm}
          insulation: 橡塑保温（吊顶内）
          slope: ">0.003（向泄水点）"
        
        location_hint:
          space_type: CEILING_VOID
          position: 走廊吊顶内

      - node_id: PLUMB-DWS_DST_PRV
        node_name: 减压阀组
        node_name_en: Pressure Reducing Valve Station
        node_type: Distribution_Node
        node_subtype: REG
        node_category: DST
      
        function: 高层建筑分区供水，减压至合适压力
        medium_in: WATER-PW
        medium_out: WATER-PW
      
        multiplicity: multiple
        instance_pattern: PLUMB-DWS_DST_PRV_{Zone}
        note: 超过6层或供水压力>0.35MPa时设置
      
        equipment_parameters:
          type: 可调式减压阀
          inlet_pressure: {value: 0.5, unit: MPa}
          outlet_pressure: {value: 0.3, unit: MPa}
          configuration: 一用一备并联
          bypass: 设旁通阀
          accessories:
            - 进口闸阀
            - 出口闸阀
            - 进口压力表
            - 出口压力表
            - Y型过滤器
      
        control_points:
          sensors:
            - point_id: PRV_IN_P
              point_name: 进口压力
              point_type: AI
              unit: MPa
            - point_id: PRV_OUT_P
              point_name: 出口压力
              point_type: AI
              unit: MPa
      
        location_hint:
          space_type: SHAFT
          shaft_type: 给排水管井
          position: 分区起始层

      - node_id: PLUMB-DWS_DST_UV_STERILIZER
        node_name: 紫外线消毒器
        node_name_en: UV Sterilizer
        node_type: Distribution_Node
        node_subtype: TRT
        node_category: DST
      
        function: 二次供水消毒，保证水质安全
        medium_in: WATER-PW
        medium_out: WATER-PW
      
        equipment_parameters:
          type: 管道式紫外线消毒器
          capacity: {value: 50, unit: "m³/h"}
          uv_dose: {value: ">40", unit: "mJ/cm²"}
          lamp_type: 低压汞灯/中压汞灯
          lamp_life: {value: 9000, unit: h}
          housing: 不锈钢316L
        
        control_points:
          sensors:
            - point_id: UV_INTENSITY
              point_name: 紫外线强度
              point_type: AI
              unit: "mW/cm²"
            - point_id: UV_LAMP_HOURS
              point_name: 灯管累计时间
              point_type: AI
              unit: h
          status:
            - point_id: UV_ON
              point_name: 消毒器运行
              point_type: DI
            - point_id: UV_LAMP_FAULT
              point_name: 灯管故障
              point_type: DI
            - point_id: UV_INTENSITY_LOW
              point_name: 强度低报警
              point_type: DI
          commands:
            - point_id: UV_ENABLE
              point_name: 消毒器启停
              point_type: DO
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 水泵房
          position: 泵组出口后

    sink_nodes:
  
      - node_id: PLUMB-DWS_SNK_FIXTURE
        node_name: 卫生洁具给水点
        node_name_en: Plumbing Fixture Water Point
        node_type: Sink_Node
        node_category: SNK
      
        function: 供水至卫生洁具
        medium_in: WATER-PW
        medium_out: WATER-PW (to fixture)
      
        is_boundary_output: true
      
        multiplicity: multiple
        instance_pattern: PLUMB-DWS_SNK_FIXTURE_{Floor}_{Room}_{Type}
        typical_quantity: 大量
      
        fixture_types:
          - type: 洗脸盆
            flow: {value: 0.15, unit: "L/s"}
            pressure_min: {value: 0.05, unit: MPa}
          - type: 大便器（冲洗阀）
            flow: {value: 1.2, unit: "L/s"}
            pressure_min: {value: 0.1, unit: MPa}
          - type: 大便器（水箱）
            flow: {value: 0.1, unit: "L/s"}
            pressure_min: {value: 0.05, unit: MPa}
          - type: 淋浴器
            flow: {value: 0.15, unit: "L/s"}
            pressure_min: {value: 0.05, unit: MPa}
          - type: 洗涤盆
            flow: {value: 0.2, unit: "L/s"}
            pressure_min: {value: 0.05, unit: MPa}
      
        location_hint:
          space_type: 卫生间/开水间/污洗间

      - node_id: PLUMB-DWS_SNK_HWS_SOURCE
        node_name: 热水系统冷水接口
        node_name_en: HWS Cold Water Connection
        node_type: Sink_Node
        node_category: SNK
      
        function: 向热水系统供应冷水
        medium_in: WATER-PW
        medium_out: WATER-PW
      
        is_boundary_output: true
        target_system: PLUMB-HWS
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 热水机房

      - node_id: PLUMB-DWS_SNK_COOLING_TOWER
        node_name: 冷却塔补水接口
        node_name_en: Cooling Tower Makeup Water Connection
        node_type: Sink_Node
        node_category: SNK
      
        function: 向冷却塔补充蒸发损失水
        medium_in: WATER-PW
        medium_out: WATER-PW
      
        is_boundary_output: true
        target_system: HVAC-CHP
      
        equipment_parameters:
          control: 浮球阀/电磁阀
          water_treatment: 加药装置（阻垢、杀菌）
      
        location_hint:
          space_type: 屋面/设备平台

  # ========================================
  # EDGES SECTION - 边/连接定义
  # ========================================
  edges:

    inlet_edges:
      - edge_id: PLUMB-DWS_EDGE_001
        edge_name: 市政一路至水箱
        edge_type: PIP
        from_node: PLUMB-DWS_SRC_MUNICIPAL_1
        to_node: PLUMB-DWS_DST_TANK
        direction: unidirectional
        medium: WATER-PW
        pipe_parameters:
          material: 球墨铸铁管/PE管
          diameter: DN150
          laying: 地下埋设
        
      - edge_id: PLUMB-DWS_EDGE_002
        edge_name: 市政二路至水箱
        edge_type: PIP
        from_node: PLUMB-DWS_SRC_MUNICIPAL_2
        to_node: PLUMB-DWS_DST_TANK
        direction: unidirectional
        medium: WATER-PW
        note: 双路进水，互为备用

    supply_edges:
      - edge_id: PLUMB-DWS_EDGE_011
        edge_name: 水箱至泵组
        edge_type: PIP
        from_node: PLUMB-DWS_DST_TANK
        to_node: PLUMB-DWS_DST_PUMP_STATION
        direction: unidirectional
        medium: WATER-PW
        pipe_parameters:
          material: 不锈钢管
          diameter: DN150
        
      - edge_id: PLUMB-DWS_EDGE_012
        edge_name: 泵组至消毒器
        edge_type: PIP
        from_node: PLUMB-DWS_DST_PUMP_STATION
        to_node: PLUMB-DWS_DST_UV_STERILIZER
        direction: unidirectional
        medium: WATER-PW
      
      - edge_id: PLUMB-DWS_EDGE_013
        edge_name: 消毒器至立管
        edge_type: PIP
        from_node: PLUMB-DWS_DST_UV_STERILIZER
        to_node: PLUMB-DWS_DST_RISER
        direction: unidirectional
        medium: WATER-PW
        multiplicity: multiple
      
      - edge_id: PLUMB-DWS_EDGE_014
        edge_name: 立管至减压阀
        edge_type: PIP
        from_node: PLUMB-DWS_DST_RISER
        to_node: PLUMB-DWS_DST_PRV
        direction: unidirectional
        medium: WATER-PW
        optional: true
        note: 高层分区时设置
      
      - edge_id: PLUMB-DWS_EDGE_015
        edge_name: 立管/减压阀至楼层横管
        edge_type: PIP
        from_node: PLUMB-DWS_DST_RISER
        to_node: PLUMB-DWS_DST_FLOOR_HEADER
        direction: unidirectional
        medium: WATER-PW
        multiplicity: multiple
      
      - edge_id: PLUMB-DWS_EDGE_016
        edge_name: 楼层横管至洁具
        edge_type: PIP
        from_node: PLUMB-DWS_DST_FLOOR_HEADER
        to_node: PLUMB-DWS_SNK_FIXTURE
        direction: unidirectional
        medium: WATER-PW
        multiplicity: multiple

  # ========================================
  # TYPICAL PATHS SECTION
  # ========================================
  typical_paths:

    - path_id: PLUMB-DWS_PATH_MAIN
      path_name: 生活给水主路径
      path_type: SUP
      description: 市政水→水箱→泵组→立管→用水点
      sequence:
        - step: 1
          node: PLUMB-DWS_SRC_MUNICIPAL_1
          action: 市政进水
          parameters:
            pressure: "0.25-0.35MPa"
        - step: 2
          node: PLUMB-DWS_DST_TANK
          action: 水箱储存调节
        - step: 3
          node: PLUMB-DWS_DST_PUMP_STATION
          action: 变频加压
          parameters:
            outlet_pressure: 0.45MPa
        - step: 4
          node: PLUMB-DWS_DST_UV_STERILIZER
          action: 紫外线消毒
        - step: 5
          node: PLUMB-DWS_DST_RISER
          action: 立管输送
        - step: 6
          node: PLUMB-DWS_DST_FLOOR_HEADER
          action: 楼层分配
        - step: 7
          node: PLUMB-DWS_SNK_FIXTURE
          action: 用水点供水
          parameters:
            pressure: "0.1-0.35MPa"

  # ========================================
  # CONTROL LOGIC SECTION
  # ========================================
  control_logic:

    tank_level_control:
      name: 水箱液位控制
      description: 水箱进水自动控制
    
      control_method: 浮球阀+电动阀双重控制
    
      float_valve:
        description: 机械浮球阀（主控）
        action: 自动开关进水
        start_filling: 液位下降时自动开启
        stop_filling: 液位到达设定值时关闭
      
      electric_valve:
        description: 电动阀（备用/远控）
        control_logic: |
          1. 液位<70%：开启电动进水阀
          2. 液位>90%：关闭电动进水阀
          3. 液位>95%：高液位报警
          4. 液位<15%：紧急低液位报警
        
    pump_control:
      name: 加压泵组控制
      description: 变频恒压供水控制
    
      constant_pressure_control:
        setpoint: {value: 0.45, unit: MPa}
        control_logic: |
          1. PID控制变频泵转速，维持出口压力恒定
          2. 当变频泵频率达50Hz仍不能满足压力，启动第二台工频
          3. 当压力过高或流量很小，停止工频泵
          4. 夜间低峰时段可降低压力设定值节能
          5. 定期轮换主备泵（每周或按运行时间）
      
      pump_rotation:
        description: 泵组轮换
        method: 按累计运行时间轮换
        interval: 每168小时（一周）或手动
      
      protection:
        dry_run_protection:
          condition: 水箱液位<15%
          action: 停泵保护，防止干转
        low_pressure_protection:
          condition: 出口压力<0.25MPa持续30秒
          action: 报警，检查原因
        high_pressure_protection:
          condition: 出口压力>0.55MPa
          action: 停泵，检查管路
        
    water_quality_control:
      name: 水质控制
      description: 保证二次供水水质
    
      uv_sterilization:
        operation: 与泵组联动，泵运行时消毒器运行
        monitoring: 监测紫外线强度
        alarm: 强度低于阈值报警
      
      residual_chlorine:
        monitoring: 定期检测余氯浓度
        requirement: {value: "0.05-0.5", unit: "mg/L"}
        action: 余氯过低时考虑补氯
      
      tank_cleaning:
        frequency: 每6个月清洗一次
        procedure: 排空、清洗、消毒、检测合格后投入使用
        record: 保留清洗记录

  # ========================================
  # ALARM & PROTECTION
  # ========================================
  alarm_protection:
  
    critical_alarms:
      - alarm_id: ALM_DWS_NO_WATER
        alarm_name: 市政断水
        severity: CRITICAL
        trigger: 双路进水压力均<0.1MPa
        action: 报警，依赖水箱存水，通知相关部门
      
      - alarm_id: ALM_DWS_TANK_EMPTY
        alarm_name: 水箱空
        severity: CRITICAL
        trigger: 水箱液位<10%
        action: 停泵保护，紧急报警
      
      - alarm_id: ALM_DWS_PUMP_ALL_FAIL
        alarm_name: 泵组全部故障
        severity: CRITICAL
        trigger: 所有泵故障
        action: 紧急报警，无法供水
      
    high_alarms:
      - alarm_id: ALM_DWS_LOW_PRESSURE
        alarm_name: 供水压力低
        severity: HIGH
        trigger: 出口压力<0.3MPa持续1分钟
        action: 报警，检查泵组
      
      - alarm_id: ALM_DWS_UV_FAIL
        alarm_name: 消毒器故障
        severity: HIGH
        trigger: 紫外线强度低或消毒器停止
        action: 报警，检修消毒器

  # ========================================
  # DEPENDENCIES
  # ========================================
  dependencies:
  
    upstream_dependencies:
      - dependency_id: DEP_MUNICIPAL
        from_system: EXTERNAL_MUNICIPAL_WATER
        dependency_type: WATER_SUPPLY
        criticality: CRITICAL
        description: 市政自来水供应
      
      - dependency_id: DEP_POWER
        from_system: ELEC-LV-MAIN
        dependency_type: POWER_SUPPLY
        criticality: HIGH
        description: 加压泵电源
        failure_impact: 泵无法运行，依赖水箱余水靠重力供水
      
    downstream_dependencies:
      - dependency_id: DEP_HWS
        to_system: PLUMB-HWS
        dependency_type: COLD_WATER
        criticality: HIGH
      
      - dependency_id: DEP_HVAC
        to_system: HVAC-CHP
        dependency_type: MAKEUP_WATER
        criticality: MEDIUM
```

---

## 系统 3.2: PLUMB-HWS 生活热水系统

```yaml
System_Topology:

  identity:
    system_id: PLUMB-HWS
    system_name: 生活热水系统
    system_name_en: Domestic Hot Water System
    system_category: PLUMB
    system_type: 热水
    priority_level: P2-IMPORTANT
  
    description: |
      医院生活热水系统，为病房、手术室、洗衣房等提供热水。
      采用集中热水供应方式，热源为锅炉房蒸汽/热水或空气源热泵。
      系统设置机械循环，保证热水供应即开即热。
      医院对热水温度稳定性要求高，需防止军团菌滋生。
  
    design_basis:
      supply_temperature: {value: 55, unit: ℃, note: "供水温度"}
      return_temperature: {value: 50, unit: ℃, note: "回水温度"}
      storage_temperature: {value: 60, unit: ℃, note: "储热温度，防止军团菌"}
      terminal_temperature: {value: 45, unit: ℃, note: "使用点温度"}
      daily_consumption: {value: 60, unit: "L/(床·d)", note: "热水定额"}
    
    parent_system: PLUMB-DWS
  
    design_standards:
      - GB 50015-2019 建筑给水排水设计标准
      - GB 51039-2014 综合医院建筑设计规范
  
    version: 1.0
    last_updated: 2024

  boundary:
    inputs:
      - boundary_id: PLUMB-HWS_IN_001
        name: 冷水供应
        from_system: PLUMB-DWS
        from_node: PLUMB-DWS_SNK_HWS_SOURCE
        medium: WATER-PW
      
      - boundary_id: PLUMB-HWS_IN_002
        name: 热源（蒸汽/热水）
        from_system: HVAC-CHP / STEAM
        medium: STEAM / HW
        parameters:
          steam_pressure: {value: 0.3, unit: MPa}
          hw_temperature: {value: 80, unit: ℃}
        
    outputs:
      - boundary_id: PLUMB-HWS_OUT_001
        name: 热水用水点
        to_system: 卫生间/淋浴间
        medium: WATER-HW
        parameters:
          temperature: {value: 55, unit: ℃}

  nodes:

    source_nodes:
  
      - node_id: PLUMB-HWS_SRC_CW_IN
        node_name: 冷水进水接口
        node_name_en: Cold Water Inlet
        node_type: Source_Node
        node_category: SRC
      
        function: 接收生活冷水
        medium_in: WATER-PW
        medium_out: WATER-PW
      
        is_boundary_input: true
        source_system: PLUMB-DWS
      
        equipment_parameters:
          pipe_size: DN80
          components:
            - 闸阀
            - 止回阀
            - 水表
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 热水机房

      - node_id: PLUMB-HWS_SRC_HEAT_IN
        node_name: 热源接口
        node_name_en: Heat Source Connection
        node_type: Source_Node
        node_category: SRC
      
        function: 接收蒸汽或热水热源
        medium_in: STEAM / HW
        medium_out: STEAM / HW
      
        is_boundary_input: true
      
        equipment_parameters:
          steam:
            pipe_size: DN50
            pressure: {value: 0.3, unit: MPa}
          hot_water:
            pipe_size: DN65
            temperature: {value: 80, unit: ℃}
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 热水机房

    distribution_nodes:
  
      - node_id: PLUMB-HWS_DST_HEATER
        node_name: 热水加热设备
        node_name_en: Water Heater
        node_type: Distribution_Node
        node_subtype: TRF
        node_category: DST
      
        function: 将冷水加热至设定温度
        medium_in: [WATER-PW, STEAM/HW]
        medium_out: WATER-HW
      
        equipment_parameters:
          type: 半容积式换热器/容积式换热器
          alternative: 空气源热泵热水机组
        
          steam_exchanger:
            type: 半容积式
            capacity: {value: 1000, unit: L}
            heating_surface: {value: 5, unit: "m²"}
            steam_consumption: {value: 200, unit: "kg/h"}
            outlet_temp: {value: 60, unit: ℃}
          
          heat_pump:
            type: 空气源热泵
            heating_capacity: {value: 100, unit: kW}
            cop: {value: 3.5, note: "名义工况"}
            outlet_temp: {value: 55, unit: ℃}
          
        control_points:
          sensors:
            - point_id: HW_OUTLET_TEMP
              point_name: 热水出口温度
              point_type: AI
              unit: ℃
              range: [0, 80]
            - point_id: HW_INLET_TEMP
              point_name: 冷水进口温度
              point_type: AI
              unit: ℃
            - point_id: STEAM_PRESSURE
              point_name: 蒸汽压力
              point_type: AI
              unit: MPa
              optional: true
          status:
            - point_id: HEATER_ON
              point_name: 加热运行
              point_type: DI
            - point_id: HEATER_FAULT
              point_name: 加热故障
              point_type: DI
            - point_id: HIGH_TEMP_ALARM
              point_name: 超温报警
              point_type: DI
          commands:
            - point_id: HEATER_ENABLE
              point_name: 加热启停
              point_type: DO
            - point_id: STEAM_VALVE
              point_name: 蒸汽阀开度
              point_type: AO
              unit: "%"
              range: [0, 100]
          setpoints:
            - point_id: HW_TEMP_SP
              point_name: 热水温度设定
              point_type: AO
              unit: ℃
              range: [45, 65]
              default: 60
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 热水机房
          floor: B1或屋顶

      - node_id: PLUMB-HWS_DST_STORAGE_TANK
        node_name: 热水储罐
        node_name_en: Hot Water Storage Tank
        node_type: Distribution_Node
        node_subtype: BUF
        node_category: DST
      
        function: 储存热水，调节峰值需求
        medium_in: WATER-HW
        medium_out: WATER-HW
      
        equipment_parameters:
          type: 不锈钢保温储罐
          volume: {value: 5000, unit: L, note: "按1小时峰值用量"}
          material: SUS304不锈钢
          insulation: 聚氨酯发泡，厚度50mm
          heat_loss: {value: "<0.3", unit: "℃/h"}
          accessories:
            - 温度计
            - 安全阀
            - 排污阀
            - 人孔
          
        control_points:
          sensors:
            - point_id: TANK_HW_TEMP_TOP
              point_name: 储罐顶部温度
              point_type: AI
              unit: ℃
            - point_id: TANK_HW_TEMP_MID
              point_name: 储罐中部温度
              point_type: AI
              unit: ℃
            - point_id: TANK_HW_TEMP_BOT
              point_name: 储罐底部温度
              point_type: AI
              unit: ℃
            - point_id: TANK_HW_LEVEL
              point_name: 储罐液位
              point_type: AI
              unit: "%"
      
        anti_legionella:
          description: 防军团菌措施
          storage_temp: {value: ">60", unit: ℃}
          periodic_heating:
            frequency: 每周至少一次
            target_temp: {value: 70, unit: ℃}
            duration: 保持1小时
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 热水机房

      - node_id: PLUMB-HWS_DST_SUPPLY_PUMP
        node_name: 热水供水泵
        node_name_en: Hot Water Supply Pump
        node_type: Distribution_Node
        node_subtype: PMP
        node_category: DST
      
        function: 热水供水加压
        medium_in: WATER-HW
        medium_out: WATER-HW
      
        equipment_parameters:
          type: 立式离心泵
          quantity: "2台（一用一备）"
          flow: {value: 20, unit: "m³/h"}
          head: {value: 35, unit: m}
          motor_power: {value: 5.5, unit: kW}
          material: 耐高温材质
        
        control_points:
          sensors:
            - point_id: HW_SUPPLY_P
              point_name: 供水压力
              point_type: AI
              unit: MPa
          status:
            - point_id: HW_PUMP1_RUN
              point_name: 1#泵运行
              point_type: DI
            - point_id: HW_PUMP1_FAULT
              point_name: 1#泵故障
              point_type: DI
          commands:
            - point_id: HW_PUMP1_START
              point_name: 1#泵启动
              point_type: DO
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 热水机房

      - node_id: PLUMB-HWS_DST_CIRC_PUMP
        node_name: 热水循环泵
        node_name_en: Hot Water Circulation Pump
        node_type: Distribution_Node
        node_subtype: PMP
        node_category: DST
      
        function: 热水管道循环，保持管道温度
        medium_in: WATER-HW
        medium_out: WATER-HW
      
        equipment_parameters:
          type: 屏蔽泵/离心泵
          quantity: "2台（一用一备）"
          flow: {value: 8, unit: "m³/h", note: "循环流量约为供水量30-50%"}
          head: {value: 15, unit: m}
          motor_power: {value: 1.5, unit: kW}
        
        control_points:
          sensors:
            - point_id: HW_RETURN_TEMP
              point_name: 回水温度
              point_type: AI
              unit: ℃
          status:
            - point_id: CIRC_PUMP1_RUN
              point_name: 循环泵1运行
              point_type: DI
          commands:
            - point_id: CIRC_PUMP1_START
              point_name: 循环泵1启动
              point_type: DO
      
        control_mode:
          description: 循环泵控制
          options:
            - 24小时连续运行
            - 定时运行（用水高峰时段）
            - 温控运行（回水温度低于设定值时运行）
          recommended: 温控运行（节能）
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 热水机房

      - node_id: PLUMB-HWS_DST_SUPPLY_RISER
        node_name: 热水供水立管
        node_name_en: Hot Water Supply Riser
        node_type: Distribution_Node
        node_subtype: TRK
        node_category: DST
      
        function: 热水竖向供应
        medium_in: WATER-HW
        medium_out: WATER-HW
      
        multiplicity: multiple
      
        equipment_parameters:
          material: 不锈钢管/PPR热水管
          diameter: {value: "DN32-DN65", unit: mm}
          insulation:
            type: 橡塑保温
            thickness: {value: 30, unit: mm}
            note: 必须保温，减少热损失
          
        location_hint:
          space_type: SHAFT

      - node_id: PLUMB-HWS_DST_RETURN_RISER
        node_name: 热水回水立管
        node_name_en: Hot Water Return Riser
        node_type: Distribution_Node
        node_subtype: TRK
        node_category: DST
      
        function: 热水循环回水
        medium_in: WATER-HW
        medium_out: WATER-HW
      
        multiplicity: multiple
      
        equipment_parameters:
          material: 不锈钢管/PPR热水管
          diameter: {value: "DN20-DN40", unit: mm}
          insulation: 橡塑保温30mm
        
        location_hint:
          space_type: SHAFT

      - node_id: PLUMB-HWS_DST_TMV
        node_name: 恒温混水阀
        node_name_en: Thermostatic Mixing Valve
        node_type: Distribution_Node
        node_subtype: REG
        node_category: DST
      
        function: 混合冷热水至安全使用温度
        medium_in: [WATER-HW, WATER-PW]
        medium_out: WATER-MW
      
        multiplicity: multiple
        instance_pattern: PLUMB-HWS_DST_TMV_{Floor}_{Zone}
      
        equipment_parameters:
          type: 恒温混水阀
          inlet_hot: {value: 55, unit: ℃}
          inlet_cold: {value: 15, unit: ℃}
          outlet: {value: 42, unit: ℃, note: "防烫伤"}
          fail_safe: 热水失压时自动关闭（防冷激）
          anti_scald: 超温保护
        
        control_points:
          sensors:
            - point_id: TMV_OUT_TEMP
              point_name: 出口温度
              point_type: AI
              unit: ℃
      
        location_hint:
          space_type: SHAFT
          position: 各用水区域入口

    sink_nodes:
  
      - node_id: PLUMB-HWS_SNK_FIXTURE
        node_name: 热水用水点
        node_name_en: Hot Water Fixture
        node_type: Sink_Node
        node_category: SNK
      
        function: 供应热水至用水器具
        medium_in: WATER-HW / WATER-MW
        medium_out: WATER-HW (to fixture)
      
        is_boundary_output: true
      
        multiplicity: multiple
      
        fixture_types:
          - type: 淋浴器
            temperature: {value: 38-42, unit: ℃}
          - type: 洗脸盆
            temperature: {value: 40-45, unit: ℃}
          - type: 洗涤盆
            temperature: {value: 45-50, unit: ℃}
          - type: 手术室洗手池
            temperature: {value: 40, unit: ℃, note: "恒温控制"}
          
        location_hint:
          space_type: 卫生间/淋浴间/手术室

  edges:

    cold_water_edges:
      - edge_id: PLUMB-HWS_EDGE_001
        edge_name: 冷水至加热器
        edge_type: PIP
        from_node: PLUMB-HWS_SRC_CW_IN
        to_node: PLUMB-HWS_DST_HEATER
        direction: unidirectional
        medium: WATER-PW

    heating_edges:
      - edge_id: PLUMB-HWS_EDGE_002
        edge_name: 热源至加热器
        edge_type: PIP
        from_node: PLUMB-HWS_SRC_HEAT_IN
        to_node: PLUMB-HWS_DST_HEATER
        direction: unidirectional
        medium: STEAM/HW
      
      - edge_id: PLUMB-HWS_EDGE_003
        edge_name: 加热器至储罐
        edge_type: PIP
        from_node: PLUMB-HWS_DST_HEATER
        to_node: PLUMB-HWS_DST_STORAGE_TANK
        direction: unidirectional
        medium: WATER-HW

    supply_edges:
      - edge_id: PLUMB-HWS_EDGE_011
        edge_name: 储罐至供水泵
        edge_type: PIP
        from_node: PLUMB-HWS_DST_STORAGE_TANK
        to_node: PLUMB-HWS_DST_SUPPLY_PUMP
        direction: unidirectional
        medium: WATER-HW
      
      - edge_id: PLUMB-HWS_EDGE_012
        edge_name: 供水泵至供水立管
        edge_type: PIP
        from_node: PLUMB-HWS_DST_SUPPLY_PUMP
        to_node: PLUMB-HWS_DST_SUPPLY_RISER
        direction: unidirectional
        medium: WATER-HW
        multiplicity: multiple
      
      - edge_id: PLUMB-HWS_EDGE_013
        edge_name: 供水立管至混水阀
        edge_type: PIP
        from_node: PLUMB-HWS_DST_SUPPLY_RISER
        to_node: PLUMB-HWS_DST_TMV
        direction: unidirectional
        medium: WATER-HW
      
      - edge_id: PLUMB-HWS_EDGE_014
        edge_name: 混水阀至用水点
        edge_type: PIP
        from_node: PLUMB-HWS_DST_TMV
        to_node: PLUMB-HWS_SNK_FIXTURE
        direction: unidirectional
        medium: WATER-MW
        multiplicity: multiple

    return_edges:
      - edge_id: PLUMB-HWS_EDGE_021
        edge_name: 立管末端至回水立管
        edge_type: PIP
        from_node: PLUMB-HWS_DST_SUPPLY_RISER
        to_node: PLUMB-HWS_DST_RETURN_RISER
        direction: unidirectional
        medium: WATER-HW
        note: 循环回水
      
      - edge_id: PLUMB-HWS_EDGE_022
        edge_name: 回水立管至循环泵
        edge_type: PIP
        from_node: PLUMB-HWS_DST_RETURN_RISER
        to_node: PLUMB-HWS_DST_CIRC_PUMP
        direction: unidirectional
        medium: WATER-HW
      
      - edge_id: PLUMB-HWS_EDGE_023
        edge_name: 循环泵至储罐
        edge_type: PIP
        from_node: PLUMB-HWS_DST_CIRC_PUMP
        to_node: PLUMB-HWS_DST_STORAGE_TANK
        direction: unidirectional
        medium: WATER-HW

  typical_paths:

    - path_id: PLUMB-HWS_PATH_SUPPLY
      path_name: 热水供水路径
      path_type: SUP
      sequence:
        - step: 1
          node: PLUMB-HWS_SRC_CW_IN
          action: 冷水进入
        - step: 2
          node: PLUMB-HWS_DST_HEATER
          action: 加热至60℃
        - step: 3
          node: PLUMB-HWS_DST_STORAGE_TANK
          action: 储存待用
        - step: 4
          node: PLUMB-HWS_DST_SUPPLY_PUMP
          action: 加压供水
        - step: 5
          node: PLUMB-HWS_DST_SUPPLY_RISER
          action: 立管输送
        - step: 6
          node: PLUMB-HWS_DST_TMV
          action: 混水降温至42℃
        - step: 7
          node: PLUMB-HWS_SNK_FIXTURE
          action: 用水点供应

    - path_id: PLUMB-HWS_PATH_RETURN
      path_name: 热水循环路径
      path_type: RET
      sequence:
        - step: 1
          node: PLUMB-HWS_DST_SUPPLY_RISER
          action: 立管末端
        - step: 2
          node: PLUMB-HWS_DST_RETURN_RISER
          action: 回水收集
        - step: 3
          node: PLUMB-HWS_DST_CIRC_PUMP
          action: 循环泵输送
        - step: 4
          node: PLUMB-HWS_DST_STORAGE_TANK
          action: 回到储罐

  control_logic:

    temperature_control:
      name: 热水温度控制
      description: 维持热水供水温度稳定
    
      heater_control:
        control_variable: 加热器出口温度
        setpoint: {value: 60, unit: ℃}
        method: 调节蒸汽阀开度
        pid_parameters:
          kp: 2.0
          ki: 0.3
          kd: 0
        
      storage_temp_control:
        monitoring: 储罐顶/中/底部温度
        action: |
          1. 顶部温度<55℃时加热
          2. 顶部温度>65℃时停止加热
          3. 夜间可降低温度设定值节能
        
    circulation_control:
      name: 循环泵控制
      description: 保证热水即开即热
    
      temperature_based:
        description: 回水温度控制
        start_condition: 回水温度<45℃
        stop_condition: 回水温度>50℃
      
      time_based:
        description: 定时运行（备选）
        schedule:
          - period: "06:00-22:00"
            mode: 连续运行
          - period: "22:00-06:00"
            mode: 间歇运行（每小时运行15分钟）
          
    anti_legionella:
      name: 防军团菌控制
      description: 定期高温杀菌
    
      periodic_heating:
        frequency: 每周日凌晨2:00
        procedure:
          - step: 1
            action: 加热储罐水温至70℃
          - step: 2
            action: 保持70℃运行1小时
          - step: 3
            action: 开启循环泵，高温水流经全部管道
          - step: 4
            action: 恢复正常温度设定
        warning: 需通知用户避免高温烫伤
      
    anti_scald:
      name: 防烫伤保护
      description: 混水阀和终端防烫措施
    
      tmv_setting:
        max_outlet_temp: {value: 45, unit: ℃}
        fail_safe: 热水失压时切断出水
      
      terminal_protection:
        - 淋浴恒温龙头限温
        - 儿科/老年科区域特殊限温（40℃）

  alarm_protection:
  
    critical_alarms:
      - alarm_id: ALM_HWS_NO_HOT_WATER
        alarm_name: 无热水供应
        severity: HIGH
        trigger: 供水温度<40℃持续10分钟
        action: 检查加热设备和热源
      
      - alarm_id: ALM_HWS_OVERTEMP
        alarm_name: 热水超温
        severity: HIGH
        trigger: 储罐温度>75℃
        action: 停止加热，报警

  dependencies:
  
    upstream_dependencies:
      - dependency_id: DEP_CW
        from_system: PLUMB-DWS
        dependency_type: COLD_WATER
        criticality: HIGH
      
      - dependency_id: DEP_HEAT
        from_system: HVAC-CHP / STEAM
        dependency_type: HEAT_SOURCE
        criticality: HIGH
```

---

## 系统 3.3: PLUMB-SAN 排水系统

```yaml
System_Topology:

  identity:
    system_id: PLUMB-SAN
    system_name: 排水系统
    system_name_en: Sanitary Drainage System
    system_category: PLUMB
    system_type: 排水
    priority_level: P1-CRITICAL
  
    description: |
      医院排水系统，收集全院生活污水、医疗废水并输送至污水处理站。
      系统包括普通生活污水、医疗污水、传染科污水（需单独收集预处理）。
      污水经院内污水处理站处理达标后排入市政污水管网。
      医院排水系统须符合医疗废水排放标准，防止交叉污染。
  
    design_basis:
      sewage_type:
        - 普通生活污水
        - 医疗污水
        - 传染科污水（单独处理）
        - 实验室废水（单独处理）
      discharge_standard: GB 18466-2005 医疗机构水污染物排放标准
      daily_sewage: {value: 350, unit: "L/(床·d)", note: "排水量约为给水量85%"}
    
    related_systems:
      - PLUMB-DWS   # 给水系统
      - PLUMB-HWS   # 热水系统
      - ENV-STP     # 污水处理站
  
    design_standards:
      - GB 50015-2019 建筑给水排水设计标准
      - GB 51039-2014 综合医院建筑设计规范
      - GB 18466-2005 医疗机构水污染物排放标准
      - GB 50849-2014 传染病医院建筑设计规范
  
    version: 1.0
    last_updated: 2024

  boundary:
    inputs:
      - boundary_id: PLUMB-SAN_IN_001
        name: 卫生洁具排水
        from_system: 卫生间
        medium: SEWAGE
      
      - boundary_id: PLUMB-SAN_IN_002
        name: 医疗废水
        from_system: 医疗功能区
        medium: MEDICAL-SEWAGE
        note: 含消毒剂、药物残留等
      
      - boundary_id: PLUMB-SAN_IN_003
        name: 传染科污水
        from_system: 传染科/发热门诊
        medium: INFECTIOUS-SEWAGE
        note: 需预处理
      
    outputs:
      - boundary_id: PLUMB-SAN_OUT_001
        name: 污水至处理站
        to_system: ENV-STP
        medium: SEWAGE
      
      - boundary_id: PLUMB-SAN_OUT_002
        name: 处理后达标排放
        to_system: EXTERNAL_MUNICIPAL_SEWER
        medium: TREATED-SEWAGE
        parameters:
          quality: 符合GB 18466

  nodes:

    source_nodes:
  
      - node_id: PLUMB-SAN_SRC_FIXTURE
        node_name: 卫生洁具排水口
        node_name_en: Sanitary Fixture Drain
        node_type: Source_Node
        node_category: SRC
      
        function: 收集卫生洁具排水
        medium_in: SEWAGE
        medium_out: SEWAGE
      
        is_boundary_input: true
      
        multiplicity: multiple
        instance_pattern: PLUMB-SAN_SRC_FIXTURE_{Floor}_{Room}_{Type}
      
        fixture_types:
          - type: 洗脸盆
            trap: P型存水弯
          - type: 大便器
            trap: 自带水封
          - type: 小便器
            trap: 自带水封
          - type: 地漏
            trap: 水封地漏（水封≥50mm）
          - type: 淋浴
            trap: 水封地漏
          
        water_seal_requirement:
          depth: {value: "≥50", unit: mm}
          purpose: 防止臭气返溢
        
        location_hint:
          space_type: 卫生间/淋浴间

      - node_id: PLUMB-SAN_SRC_MEDICAL
        node_name: 医疗废水排放点
        node_name_en: Medical Wastewater Discharge Point
        node_type: Source_Node
        node_category: SRC
      
        function: 收集医疗区域废水
        medium_in: MEDICAL-SEWAGE
        medium_out: MEDICAL-SEWAGE
      
        is_boundary_input: true
      
        multiplicity: multiple
      
        sources:
          - 手术室污物
          - 产房废水
          - 检验科废液
          - 病理科废液
          - 透析废液
          - 内镜清洗废水
        
        special_treatment:
          - 含汞废液单独收集
          - 放射性废液单独处理
          - 化学试剂中和处理
        
        location_hint:
          space_type: 医疗功能区

      - node_id: PLUMB-SAN_SRC_INFECTIOUS
        node_name: 传染科污水排放点
        node_name_en: Infectious Ward Wastewater Discharge
        node_type: Source_Node
        node_category: SRC
      
        function: 收集传染科/发热门诊污水
        medium_in: INFECTIOUS-SEWAGE
        medium_out: INFECTIOUS-SEWAGE
      
        is_boundary_input: true
      
        multiplicity: multiple
      
        special_requirements:
          - 独立收集管道
          - 密封设计
          - 预消毒处理
          - 管道防腐蚀
        
        location_hint:
          space_type: 传染科/发热门诊

    distribution_nodes:
  
      - node_id: PLUMB-SAN_DST_BRANCH
        node_name: 排水支管
        node_name_en: Drainage Branch Pipe
        node_type: Distribution_Node
        node_subtype: BRH
        node_category: DST
      
        function: 收集洁具排水汇入立管
        medium_in: SEWAGE
        medium_out: SEWAGE
      
        multiplicity: multiple
      
        equipment_parameters:
          material: UPVC排水管/HDPE管
          diameter: {value: "DN50-DN100", unit: mm}
          slope: {value: "≥0.02", note: "坡向立管"}
          connection: 粘接/热熔
        
        location_hint:
          space_type: CEILING_VOID / FLOOR_VOID
          position: 卫生间楼板下

      - node_id: PLUMB-SAN_DST_STACK
        node_name: 排水立管
        node_name_en: Drainage Stack
        node_type: Distribution_Node
        node_subtype: TRK
        node_category: DST
      
        function: 垂直输送污水至室外
        medium_in: SEWAGE
        medium_out: SEWAGE
      
        multiplicity: multiple
        instance_pattern: PLUMB-SAN_DST_STACK_{Zone}_{Seq}
      
        equipment_parameters:
          material: UPVC排水管/HDPE管/铸铁管
          diameter: {value: "DN100-DN150", unit: mm}
          vent:
            type: 专用通气立管
            diameter: DN75-DN100
            connection: 每层通气支管连接
            termination: 屋面通气帽（高于屋面≥0.5m）
          cleanout: 
            location: 每层设检查口
            height: 距地1.0m
          support: 每层设管道支架
        
        vent_system:
          description: 通气系统
          purpose: 
            - 平衡管内气压
            - 防止水封被破坏
            - 排除管内臭气
          configuration:
            - 专用通气立管（推荐）
            - 或环形通气管
            - 或H管通气系统
          
        location_hint:
          space_type: SHAFT
          shaft_type: 给排水管井

      - node_id: PLUMB-SAN_DST_HORIZONTAL_MAIN
        node_name: 室外排水横干管
        node_name_en: Outdoor Drainage Main
        node_type: Distribution_Node
        node_subtype: TRK
        node_category: DST
      
        function: 收集各立管排水，输送至化粪池/污水处理站
        medium_in: SEWAGE
        medium_out: SEWAGE
      
        equipment_parameters:
          material: HDPE双壁波纹管/UPVC
          diameter: {value: "DN200-DN400", unit: mm}
          slope: {value: "≥0.005", note: "坡向化粪池/处理站"}
          buried_depth: {value: "≥0.7", unit: m}
          inspection_well:
            spacing: {value: "≤30", unit: m}
            type: 检查井
          
        location_hint:
          space_type: UNDERGROUND
          position: 室外埋地

      - node_id: PLUMB-SAN_DST_SEPTIC_TANK
        node_name: 化粪池
        node_name_en: Septic Tank
        node_type: Distribution_Node
        node_subtype: TRT
        node_category: DST
      
        function: 初级沉淀处理
        medium_in: SEWAGE
        medium_out: SEWAGE
      
        equipment_parameters:
          type: 玻璃钢化粪池/钢筋混凝土化粪池
          effective_volume: {value: 100, unit: "m³", note: "按日污水量计算"}
          retention_time: {value: 12, unit: h}
          chambers: 三格式
          cover: 可开启检查盖
          vent: 通气管
        
        maintenance:
          cleaning_frequency: 每6个月清掏一次
          sludge_disposal: 交有资质单位处理
        
        location_hint:
          space_type: UNDERGROUND
          position: 室外绿地下

      - node_id: PLUMB-SAN_DST_LIFT_STATION
        node_name: 污水提升泵站
        node_name_en: Sewage Lift Station
        node_type: Distribution_Node
        node_subtype: PMP
        node_category: DST
      
        function: 提升地下室污水
        medium_in: SEWAGE
        medium_out: SEWAGE
      
        optional: true
        condition: 地下室无法重力排放时设置
      
        equipment_parameters:
          type: 潜水排污泵
          quantity: "2台（一用一备）"
          flow: {value: 30, unit: "m³/h"}
          head: {value: 15, unit: m}
          motor_power: {value: 5.5, unit: kW}
          collection_pit:
            type: 玻璃钢集水坑
            volume: {value: 2, unit: "m³"}
            cover: 密封盖板
            vent: 通气管
          control: 液位浮球控制
        
        control_points:
          sensors:
            - point_id: LIFT_PIT_LEVEL
              point_name: 集水坑液位
              point_type: AI
              unit: "%"
          status:
            - point_id: LIFT_PUMP1_RUN
              point_name: 1#泵运行
              point_type: DI
            - point_id: LIFT_HIGH_LEVEL
              point_name: 高液位报警
              point_type: DI
            - point_id: LIFT_OVERFLOW
              point_name: 溢流报警
              point_type: DI
          commands:
            - point_id: LIFT_PUMP1_START
              point_name: 1#泵启动
              point_type: DO
      
        level_settings:
          start_level: 70%
          stop_level: 20%
          alarm_level: 90%
          overflow_level: 95%
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 污水泵房
          floor: B2/B1

      - node_id: PLUMB-SAN_DST_INFECTIOUS_PRETREAT
        node_name: 传染科污水预处理池
        node_name_en: Infectious Wastewater Pretreatment Tank
        node_type: Distribution_Node
        node_subtype: TRT
        node_category: DST
      
        function: 传染科污水预消毒处理
        medium_in: INFECTIOUS-SEWAGE
        medium_out: SEWAGE
      
        equipment_parameters:
          type: 接触消毒池
          volume: {value: 50, unit: "m³"}
          retention_time: {value: "≥1.5", unit: h}
          disinfectant: 次氯酸钠/二氧化氯
          dosing:
            type: 自动加药设备
            chlorine_residual: {value: "≥6.5", unit: "mg/L", note: "接触1.5h后"}
          mixing: 机械搅拌或水力混合
        
        control_points:
          sensors:
            - point_id: INF_CHLORINE
              point_name: 余氯浓度
              point_type: AI
              unit: "mg/L"
            - point_id: INF_PH
              point_name: pH值
              point_type: AI
              range: [6, 9]
          status:
            - point_id: INF_DOSING_ON
              point_name: 加药运行
              point_type: DI
          commands:
            - point_id: INF_DOSING_ENABLE
              point_name: 加药启停
              point_type: DO
      
        location_hint:
          space_type: UNDERGROUND
          position: 传染科附近室外

    sink_nodes:
  
      - node_id: PLUMB-SAN_SNK_STP
        node_name: 污水处理站入口
        node_name_en: Wastewater Treatment Plant Inlet
        node_type: Sink_Node
        node_category: SNK
      
        function: 污水进入污水处理站
        medium_in: SEWAGE
        medium_out: SEWAGE
      
        is_boundary_output: true
        target_system: ENV-STP
      
        location_hint:
          space_type: OUTDOOR
          position: 污水处理站入口

      - node_id: PLUMB-SAN_SNK_MUNICIPAL
        node_name: 市政排水接口
        node_name_en: Municipal Sewer Connection
        node_type: Sink_Node
        node_category: SNK
      
        function: 处理后污水排入市政管网
        medium_in: TREATED-SEWAGE
        medium_out: TREATED-SEWAGE
      
        is_boundary_output: true
        target: 市政污水管网
      
        discharge_requirements:
          standard: GB 18466-2005 表2 综合医疗机构排放标准
          COD: {value: "≤250", unit: "mg/L"}
          BOD5: {value: "≤100", unit: "mg/L"}
          SS: {value: "≤60", unit: "mg/L"}
          ammonia_nitrogen: {value: "≤45", unit: "mg/L"}
          total_residual_chlorine: {value: "≤0.5", unit: "mg/L"}
          fecal_coliform: {value: "≤5000", unit: "MPN/L"}
        
        location_hint:
          space_type: OUTDOOR
          position: 建筑红线内

  edges:

    collection_edges:
      - edge_id: PLUMB-SAN_EDGE_001
        edge_name: 洁具至支管
        edge_type: PIP
        from_node: PLUMB-SAN_SRC_FIXTURE
        to_node: PLUMB-SAN_DST_BRANCH
        direction: unidirectional
        medium: SEWAGE
        multiplicity: multiple
      
      - edge_id: PLUMB-SAN_EDGE_002
        edge_name: 支管至立管
        edge_type: PIP
        from_node: PLUMB-SAN_DST_BRANCH
        to_node: PLUMB-SAN_DST_STACK
        direction: unidirectional
        medium: SEWAGE
        multiplicity: multiple

    main_edges:
      - edge_id: PLUMB-SAN_EDGE_011
        edge_name: 立管至横干管
        edge_type: PIP
        from_node: PLUMB-SAN_DST_STACK
        to_node: PLUMB-SAN_DST_HORIZONTAL_MAIN
        direction: unidirectional
        medium: SEWAGE
        multiplicity: multiple
      
      - edge_id: PLUMB-SAN_EDGE_012
        edge_name: 横干管至化粪池
        edge_type: PIP
        from_node: PLUMB-SAN_DST_HORIZONTAL_MAIN
        to_node: PLUMB-SAN_DST_SEPTIC_TANK
        direction: unidirectional
        medium: SEWAGE
      
      - edge_id: PLUMB-SAN_EDGE_013
        edge_name: 化粪池至污水站
        edge_type: PIP
        from_node: PLUMB-SAN_DST_SEPTIC_TANK
        to_node: PLUMB-SAN_SNK_STP
        direction: unidirectional
        medium: SEWAGE

    infectious_edges:
      - edge_id: PLUMB-SAN_EDGE_021
        edge_name: 传染科污水至预处理池
        edge_type: PIP
        from_node: PLUMB-SAN_SRC_INFECTIOUS
        to_node: PLUMB-SAN_DST_INFECTIOUS_PRETREAT
        direction: unidirectional
        medium: INFECTIOUS-SEWAGE
      
      - edge_id: PLUMB-SAN_EDGE_022
        edge_name: 预处理后至污水站
        edge_type: PIP
        from_node: PLUMB-SAN_DST_INFECTIOUS_PRETREAT
        to_node: PLUMB-SAN_SNK_STP
        direction: unidirectional
        medium: SEWAGE

  typical_paths:

    - path_id: PLUMB-SAN_PATH_NORMAL
      path_name: 普通污水排放路径
      path_type: DRN
      sequence:
        - step: 1
          node: PLUMB-SAN_SRC_FIXTURE
          action: 洁具排水
        - step: 2
          node: PLUMB-SAN_DST_BRANCH
          action: 支管收集
        - step: 3
          node: PLUMB-SAN_DST_STACK
          action: 立管输送
        - step: 4
          node: PLUMB-SAN_DST_HORIZONTAL_MAIN
          action: 横干管输送
        - step: 5
          node: PLUMB-SAN_DST_SEPTIC_TANK
          action: 化粪池沉淀
        - step: 6
          node: PLUMB-SAN_SNK_STP
          action: 进入污水处理站

    - path_id: PLUMB-SAN_PATH_INFECTIOUS
      path_name: 传染科污水处理路径
      path_type: DRN
      sequence:
        - step: 1
          node: PLUMB-SAN_SRC_INFECTIOUS
          action: 传染科排水
        - step: 2
          node: PLUMB-SAN_DST_INFECTIOUS_PRETREAT
          action: 预消毒处理
          parameters:
            chlorine_contact: 1.5h
            residual_chlorine: ">6.5mg/L"
        - step: 3
          node: PLUMB-SAN_SNK_STP
          action: 进入污水处理站

  control_logic:

    lift_pump_control:
      name: 污水提升泵控制
      description: 液位控制自动启停
    
      control_logic: |
        1. 液位上升至70%，启动1#泵
        2. 液位继续上升至80%，启动2#泵（如1#运行中）
        3. 液位下降至20%，停止所有泵
        4. 液位达90%，高液位报警
        5. 液位达95%，溢流报警
        6. 泵组定期轮换
      
      protection:
        dry_run: 液位低于10%禁止启动
        overcurrent: 电流过大时保护停机
      
    infectious_pretreat_control:
      name: 传染科预处理控制
      description: 消毒加药控制
    
      control_logic: |
        1. 检测进水流量和余氯浓度
        2. 自动调节加药量保持余氯≥6.5mg/L
        3. 接触时间≥1.5小时后方可排出
        4. 出水余氯超标时延长接触时间
        5. 定期检测粪大肠菌群

  alarm_protection:
  
    critical_alarms:
      - alarm_id: ALM_SAN_OVERFLOW
        alarm_name: 污水溢流
        severity: CRITICAL
        trigger: 集水坑/化粪池溢流
        action: 紧急报警，停止排放
      
      - alarm_id: ALM_SAN_PUMP_FAIL
        alarm_name: 提升泵故障
        severity: HIGH
        trigger: 所有提升泵故障
        action: 报警，立即检修
      
      - alarm_id: ALM_SAN_INF_DISCHARGE
        alarm_name: 传染科污水异常排放
        severity: CRITICAL
        trigger: 余氯不达标但污水已排出
        action: 紧急报警，通知卫生部门

  dependencies:
  
    upstream_dependencies:
      - dependency_id: DEP_FIXTURES
        from_system: 卫生设施
        dependency_type: WASTEWATER
        criticality: MEDIUM
      
    downstream_dependencies:
      - dependency_id: DEP_STP
        to_system: ENV-STP
        dependency_type: WASTEWATER
        criticality: HIGH
      
      - dependency_id: DEP_MUNICIPAL
        to_system: EXTERNAL_MUNICIPAL_SEWER
        dependency_type: DISCHARGE
        criticality: CRITICAL
```

---

# 智能化系统（3个系统）

## 系统 3.4: INT-BA 楼宇自动化系统

```yaml
System_Topology:

  identity:
    system_id: INT-BA
    system_name: 楼宇自动化系统
    system_name_en: Building Automation System
    system_category: INT
    system_type: 智能化-楼宇自控
    priority_level: P1-CRITICAL
  
    description: |
      医院楼宇自动化系统（BAS/BMS），对全院机电设备进行集中监控和管理。
      系统覆盖HVAC、给排水、电力、电梯等设备的监测、控制和能源管理。
      通过DDC控制器实现自动控制，通过中央管理站实现集中监控。
      支持与医院其他信息系统（HIS、安防等）的集成。
  
    design_basis:
      architecture: 三层架构（管理层-自动化层-现场层）
      protocol:
        field: BACnet MS/TP, Modbus RTU
        automation: BACnet IP, Modbus TCP
        management: BACnet/IP, OPC UA
      monitoring_scope:
        - HVAC系统
        - 给排水系统
        - 电力系统（电力监控）
        - 电梯系统（状态监视）
        - 医用气体（压力监测）
      control_points: {value: 10000, unit: "点", note: "典型大型医院"}
    
    monitored_systems:
      - HVAC-CHP
      - HVAC-CHW
      - HVAC-HW
      - HVAC-AHU
      - HVAC-PAU
      - HVAC-FCU
      - PLUMB-DWS
      - PLUMB-HWS
      - PLUMB-SAN
      - ELEC-HV
      - ELEC-LV-MAIN
      - ELEC-EPS
      - MGAS-O2
      - MGAS-VAC
      - MGAS-AIR
  
    design_standards:
      - GB 50314-2015 智能建筑设计标准
      - GB 50189-2015 公共建筑节能设计标准
      - JGJ/T 334-2014 建筑设备监控系统工程技术规范
      - ISO 16484 楼宇自动化和控制系统
  
    version: 1.0
    last_updated: 2024

  boundary:
    inputs:
      - boundary_id: INT-BA_IN_001
        name: 现场设备信号
        from_system: 各机电系统
        medium: SIGNAL-IO
        description: DDC采集的传感器信号和设备状态
      
      - boundary_id: INT-BA_IN_002
        name: 电力系统信号
        from_system: ELEC-HV / ELEC-LV-MAIN / ELEC-EPS
        medium: SIGNAL-485/MODBUS
        description: 电力仪表和保护装置通讯
      
      - boundary_id: INT-BA_IN_003
        name: 医用气体信号
        from_system: MGAS-O2 / MGAS-VAC / MGAS-AIR
        medium: SIGNAL-485
        description: 气体报警器通讯
      
    outputs:
      - boundary_id: INT-BA_OUT_001
        name: 设备控制信号
        to_system: 各机电系统
        medium: SIGNAL-IO
        description: DDC输出的控制命令
      
      - boundary_id: INT-BA_OUT_002
        name: 上层系统接口
        to_system: 医院综合管理平台/HIS
        medium: SIGNAL-ETH/API
        description: 与上层系统的数据交互

  nodes:

    source_nodes:
  
      - node_id: INT-BA_SRC_FIELD_DEVICE
        node_name: 现场传感器/执行器
        node_name_en: Field Devices (Sensors/Actuators)
        node_type: Source_Node
        node_category: SRC
      
        function: 采集现场数据，执行控制命令
        medium_in: PHYSICAL (温度/压力/流量等)
        medium_out: SIGNAL-IO
      
        is_boundary_input: true
      
        multiplicity: multiple
        typical_quantity: 数千个
      
        device_types:
          sensors:
            temperature:
              types: [管道型, 风管型, 房间型, 浸入型]
              range: [-20, 100]℃
              accuracy: ±0.5℃
              output: 4-20mA / PT1000 / NTC
            humidity:
              types: [风管型, 房间型]
              range: [0, 100]%RH
              accuracy: ±3%RH
              output: 4-20mA / 0-10V
            pressure:
              types: [水管压力, 风管压力, 压差]
              range: 按应用
              output: 4-20mA
            flow:
              types: [电磁流量计, 超声波流量计]
              output: 4-20mA / 脉冲
            level:
              types: [液位开关, 连续液位]
              output: DI / 4-20mA
            co2:
              range: [0, 2000]ppm
              output: 4-20mA / 0-10V
            
          actuators:
            valve:
              types: [电动二通阀, 电动三通阀, 电动蝶阀]
              control: 开关型(DO) / 调节型(AO)
              signal: 0-10V / 4-20mA
            damper:
              types: [电动风阀]
              control: 开关型 / 调节型
              signal: 0-10V
            vfd:
              interface: RS485/Modbus
              control: 启停/频率设定
            motor_starter:
              types: [接触器, 软启动器]
              control: DO
              feedback: DI
            
        location_hint:
          space_type: 各机电设备及管道

      - node_id: INT-BA_SRC_POWER_METER
        node_name: 电力仪表
        node_name_en: Power Meters
        node_type: Source_Node
        node_category: SRC
      
        function: 采集电力参数
        medium_in: ELEC
        medium_out: SIGNAL-485/ETH
      
        multiplicity: multiple
      
        parameters_monitored:
          - 三相电压/电流
          - 有功/无功功率
          - 功率因数
          - 电能（kWh）
          - 需量
          - 谐波
        
        communication:
          protocol: Modbus RTU/TCP
          baud_rate: 9600/19200
        
        location_hint:
          space_type: 配电室/配电箱

      - node_id: INT-BA_SRC_GAS_ALARM
        node_name: 医用气体报警器
        node_name_en: Medical Gas Alarm Panel
        node_type: Source_Node
        node_category: SRC
      
        function: 接收医用气体系统报警信息
        medium_in: SIGNAL-485
        medium_out: SIGNAL-485
      
        multiplicity: multiple
      
        monitored_alarms:
          - O2压力高/低
          - VAC真空度低
          - AIR压力高/低
          - N2O压力高/低
          - 气源切换报警
        
        communication:
          protocol: RS485/Modbus
        
        location_hint:
          space_type: 气体站房/护士站

    distribution_nodes:
  
      - node_id: INT-BA_DST_DDC
        node_name: 直接数字控制器（DDC）
        node_name_en: Direct Digital Controller
        node_type: Distribution_Node
        node_subtype: CTR
        node_category: DST
      
        function: 现场控制和数据采集
        medium_in: SIGNAL-IO
        medium_out: SIGNAL-ETH/485
      
        multiplicity: multiple
        instance_pattern: INT-BA_DST_DDC_{Building}_{Floor}_{Seq}
        typical_quantity: {value: "50-100", unit: "台", note: "大型医院"}
      
        equipment_parameters:
          type: 可编程DDC控制器
          brand: "主流品牌（施耐德/霍尼韦尔/江森/西门子等）"
          io_capacity:
            ai: {value: "8-16", unit: "点"}
            ao: {value: "4-8", unit: "点"}
            di: {value: "8-16", unit: "点"}
            do: {value: "8-16", unit: "点"}
          expandable: true
          cpu: 32位处理器
          memory: {value: "≥512", unit: KB}
          program_storage: 非易失存储
          communication:
            downlink: RS485 (Modbus/BACnet MS/TP)
            uplink: Ethernet (BACnet/IP)
          power: 24V AC/DC
        
        features:
          - 独立运行能力（断网不影响控制）
          - PID控制算法
          - 时间程序
          - 趋势记录
          - 报警处理
        
        control_points:
          status:
            - point_id: DDC_ONLINE
              point_name: DDC在线状态
              point_type: DI
            - point_id: DDC_FAULT
              point_name: DDC故障
              point_type: DI
          commands:
            - point_id: DDC_RESTART
              point_name: DDC重启
              point_type: DO
      
        location_hint:
          space_type: MEP_ROOM / SHAFT
          position: 就近设备区域
          enclosure: 防护等级IP54箱体

      - node_id: INT-BA_DST_NAC
        node_name: 网络自动化控制器（NAC）
        node_name_en: Network Automation Controller
        node_type: Distribution_Node
        node_subtype: CTR
        node_category: DST
      
        function: 区域控制器，管理多个DDC
        medium_in: SIGNAL-ETH
        medium_out: SIGNAL-ETH
      
        multiplicity: multiple
        instance_pattern: INT-BA_DST_NAC_{Building}_{Zone}
        typical_quantity: {value: "5-10", unit: "台"}
      
        equipment_parameters:
          type: 网络控制器/楼层控制器
          managed_ddcs: {value: "10-30", unit: "台"}
          communication:
            to_ddc: BACnet/IP 或 BACnet MS/TP
            to_server: BACnet/IP, TCP/IP
          features:
            - DDC程序下载/管理
            - 趋势数据汇总
            - 区域报警处理
            - 区域时间程序
            - 断网独立运行
          
        location_hint:
          space_type: 弱电间/设备机房
          floor: 各楼层或区域

      - node_id: INT-BA_DST_NETWORK_SWITCH
        node_name: 自控网络交换机
        node_name_en: BA Network Switch
        node_type: Distribution_Node
        node_subtype: NET
        node_category: DST
      
        function: 自控系统专用网络传输
        medium_in: SIGNAL-ETH
        medium_out: SIGNAL-ETH
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 工业以太网交换机
          ports: 8/16/24口
          speed: 10/100/1000Mbps
          features:
            - VLAN支持
            - 环网冗余（如需要）
            - 网管功能
          environment: 工业级温度范围
        
        network_design:
          topology: 星型/环型
          separation: 独立于办公网络
        
        location_hint:
          space_type: 弱电间
          position: 各楼层

      - node_id: INT-BA_DST_SERVER
        node_name: BA服务器
        node_name_en: BA Server
        node_type: Distribution_Node
        node_subtype: SRV
        node_category: DST
      
        function: 中央数据处理和存储
        medium_in: SIGNAL-ETH
        medium_out: SIGNAL-ETH
      
        equipment_parameters:
          type: 工业服务器
          configuration:
            cpu: Xeon 8核
            memory: {value: 32, unit: GB}
            storage: 
              - SSD 500GB（系统/程序）
              - HDD 2TB RAID（历史数据）
            network: 双千兆网卡
            os: Windows Server / Linux
          redundancy: 双机热备（推荐）
          ups: 不间断电源保护
        
        software:
          - BMS管理软件
          - 历史数据库
          - 报表系统
          - Web发布服务
          - OPC服务器
        
        location_hint:
          space_type: 弱电机房/监控中心
          environment: 恒温恒湿，精密空调

    sink_nodes:
  
      - node_id: INT-BA_SNK_WORKSTATION
        node_name: 操作员工作站
        node_name_en: Operator Workstation
        node_type: Sink_Node
        node_category: SNK
      
        function: 人机交互界面，监控和操作
        medium_in: SIGNAL-ETH
        medium_out: HMI
      
        multiplicity: multiple
        instance_pattern: INT-BA_SNK_WS_{Location}
      
        equipment_parameters:
          type: 工程工作站/工控机
          configuration:
            cpu: i7/i9
            memory: {value: 16, unit: GB}
            storage: SSD 512GB
            display: 双屏/大屏
            network: 千兆网卡
            ups: 后备电源
          software:
            - BMS客户端软件
            - 图形化界面
            - 报警管理
            - 趋势查看
            - 报表生成
          
        location:
          - 监控中心（主工作站）
          - 设备机房（值班工作站）
          - 工程部（维护工作站）
        
        location_hint:
          space_type: 监控中心/值班室

      - node_id: INT-BA_SNK_WEB_CLIENT
        node_name: Web客户端
        node_name_en: Web Client
        node_type: Sink_Node
        node_category: SNK
      
        function: 远程监控访问
        medium_in: SIGNAL-ETH (HTTP/HTTPS)
        medium_out: WEB
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 浏览器客户端
          access: 院内网络/VPN
          features:
            - 实时数据查看
            - 报警通知
            - 趋势分析
            - 报表查看
          security:
            - 用户认证
            - 权限管理
            - 操作日志
          
        location_hint:
          space_type: 办公室/移动设备

      - node_id: INT-BA_SNK_INTEGRATION
        node_name: 系统集成接口
        node_name_en: System Integration Interface
        node_type: Sink_Node
        node_category: SNK
      
        function: 与上层系统对接
        medium_in: SIGNAL-ETH
        medium_out: API/OPC
      
        is_boundary_output: true
      
        integration_targets:
          - system: 医院综合管理平台
            protocol: API/Web Service
            data: 能耗数据、设备状态、报警信息
          - system: HIS（医院信息系统）
            protocol: HL7/FHIR（如需要）
            data: 手术室环境参数
          - system: 安防系统
            protocol: API
            data: 联动信号
          - system: 消防系统
            protocol: 硬接点/RS485
            data: 火灾联动
          
        location_hint:
          space_type: 弱电机房

  edges:

    field_edges:
      - edge_id: INT-BA_EDGE_001
        edge_name: 传感器至DDC
        edge_type: CAB
        from_node: INT-BA_SRC_FIELD_DEVICE
        to_node: INT-BA_DST_DDC
        direction: unidirectional
        medium: SIGNAL-IO
        cable_parameters:
          type: RVVP屏蔽电缆
          size: "2×1.0 / 2×1.5mm²"
        multiplicity: multiple
      
      - edge_id: INT-BA_EDGE_002
        edge_name: DDC至执行器
        edge_type: CAB
        from_node: INT-BA_DST_DDC
        to_node: INT-BA_SRC_FIELD_DEVICE
        direction: unidirectional
        medium: SIGNAL-IO
        cable_parameters:
          type: RVVP屏蔽电缆
        multiplicity: multiple

    network_edges:
      - edge_id: INT-BA_EDGE_011
        edge_name: DDC至交换机
        edge_type: NET
        from_node: INT-BA_DST_DDC
        to_node: INT-BA_DST_NETWORK_SWITCH
        direction: bidirectional
        medium: SIGNAL-ETH
        cable_parameters:
          type: Cat6 UTP/STP
      
      - edge_id: INT-BA_EDGE_012
        edge_name: NAC至交换机
        edge_type: NET
        from_node: INT-BA_DST_NAC
        to_node: INT-BA_DST_NETWORK_SWITCH
        direction: bidirectional
        medium: SIGNAL-ETH
      
      - edge_id: INT-BA_EDGE_013
        edge_name: 交换机至服务器
        edge_type: NET
        from_node: INT-BA_DST_NETWORK_SWITCH
        to_node: INT-BA_DST_SERVER
        direction: bidirectional
        medium: SIGNAL-ETH
        cable_parameters:
          type: 光纤（主干）/ Cat6（接入）
      
      - edge_id: INT-BA_EDGE_014
        edge_name: 服务器至工作站
        edge_type: NET
        from_node: INT-BA_DST_SERVER
        to_node: INT-BA_SNK_WORKSTATION
        direction: bidirectional
        medium: SIGNAL-ETH

    integration_edges:
      - edge_id: INT-BA_EDGE_021
        edge_name: 电力仪表至DDC/NAC
        edge_type: NET
        from_node: INT-BA_SRC_POWER_METER
        to_node: INT-BA_DST_DDC
        direction: unidirectional
        medium: SIGNAL-485
        protocol: Modbus RTU
      
      - edge_id: INT-BA_EDGE_022
        edge_name: 医用气体报警至DDC
        edge_type: NET
        from_node: INT-BA_SRC_GAS_ALARM
        to_node: INT-BA_DST_DDC
        direction: unidirectional
        medium: SIGNAL-485
        protocol: Modbus RTU

  typical_paths:

    - path_id: INT-BA_PATH_MONITOR
      path_name: 设备监控路径
      path_type: MON
      description: 从现场设备到操作员界面的监控数据流
      sequence:
        - step: 1
          node: INT-BA_SRC_FIELD_DEVICE
          action: 传感器采集数据
        - step: 2
          node: INT-BA_DST_DDC
          action: A/D转换，数据处理
        - step: 3
          node: INT-BA_DST_NETWORK_SWITCH
          action: 网络传输
        - step: 4
          node: INT-BA_DST_SERVER
          action: 数据存储和处理
        - step: 5
          node: INT-BA_SNK_WORKSTATION
          action: 界面显示
      data_flow:
        direction: 上行
        refresh_rate: 1-5秒

    - path_id: INT-BA_PATH_CONTROL
      path_name: 设备控制路径
      path_type: CTR
      description: 从操作界面到现场设备的控制命令流
      sequence:
        - step: 1
          node: INT-BA_SNK_WORKSTATION
          action: 操作员发出命令
        - step: 2
          node: INT-BA_DST_SERVER
          action: 命令验证和转发
        - step: 3
          node: INT-BA_DST_NETWORK_SWITCH
          action: 网络传输
        - step: 4
          node: INT-BA_DST_DDC
          action: 命令解析和执行
        - step: 5
          node: INT-BA_SRC_FIELD_DEVICE
          action: 执行器动作
      data_flow:
        direction: 下行
        response_time: "<1秒"

  control_logic:

    hvac_integration:
      name: HVAC系统集成控制
      description: 空调系统的集成监控和优化控制
    
      monitored_systems:
        - system: HVAC-CHP
          points:
            - 冷水机组运行状态/故障/参数
            - 冷冻水泵/冷却水泵状态
            - 冷却塔风机状态
            - 水温/压力/流量
          control:
            - 冷水机组群控优化
            - 泵组轮换和变频控制
            - 冷却塔风机群控
          
        - system: HVAC-AHU
          points:
            - 风机运行状态/故障
            - 送回风温湿度
            - 过滤器压差
            - 风阀开度
          control:
            - 送风温度控制
            - 新风比控制
            - 时间程序
          
        - system: HVAC-FCU
          points:
            - FCU运行状态
            - 房间温度
          control:
            - 房间温度设定
            - 时间程序
          
      optimization:
        - 冷热源群控优化
        - 变频泵节能控制
        - 过渡季新风利用
        - 夜间预冷/预热
      
    electrical_monitoring:
      name: 电力系统监控
      description: 电力参数监测和能耗管理
    
      monitored_parameters:
        - 变压器负荷和温度
        - 主进线电压/电流/功率
        - 各回路电能计量
        - 功率因数
        - 谐波含量
      
      energy_management:
        - 分项计量（照明/空调/动力/特殊）
        - 能耗统计报表
        - 需量管理
        - 异常用能报警
      
    alarm_management:
      name: 报警管理
      description: 统一报警处理和通知
    
      alarm_classification:
        level_1_emergency:
          examples: [设备严重故障, 安全相关报警]
          notification: 短信/电话/声光
          response: 立即处理
        level_2_critical:
          examples: [设备故障, 参数超限]
          notification: 短信/界面弹窗
          response: 尽快处理
        level_3_warning:
          examples: [参数预警, 维护提醒]
          notification: 界面显示
          response: 计划处理
        
      alarm_actions:
        - 界面弹窗和声音提示
        - 短信/邮件通知相关人员
        - 报警记录和统计
        - 联动控制（如火灾时关闭空调）

  alarm_protection:
  
    critical_alarms:
      - alarm_id: ALM_BA_SERVER_DOWN
        alarm_name: BA服务器故障
        severity: HIGH
        trigger: 服务器离线
        action: 切换至备用服务器，通知IT
      
      - alarm_id: ALM_BA_DDC_OFFLINE
        alarm_name: DDC离线
        severity: MEDIUM
        trigger: DDC通讯中断>5分钟
        action: 检查网络和DDC
      
      - alarm_id: ALM_BA_CRITICAL_EQUIP
        alarm_name: 关键设备故障
        severity: CRITICAL
        trigger: 冷水机组/水泵/发电机等故障
        action: 立即通知维护人员

  dependencies:
  
    upstream_dependencies:
      - dependency_id: DEP_POWER
        from_system: ELEC-LV-MAIN
        dependency_type: POWER_SUPPLY
        criticality: HIGH
        description: DDC和网络设备电源
      
      - dependency_id: DEP_NETWORK
        from_system: IT-NETWORK
        dependency_type: NETWORK
        criticality: HIGH
        description: 网络基础设施
      
    downstream_dependencies:
      - dependency_id: DEP_HVAC_CONTROL
        to_system: HVAC-CHP/AHU/FCU
        dependency_type: CONTROL
        criticality: HIGH
      
      - dependency_id: DEP_PLUMB_MONITOR
        to_system: PLUMB-DWS/HWS
        dependency_type: MONITORING
        criticality: MEDIUM
```

---

## 系统 3.5: INT-NUR 护士呼叫系统

```yaml
System_Topology:

  identity:
    system_id: INT-NUR
    system_name: 护士呼叫系统
    system_name_en: Nurse Call System
    system_category: INT
    system_type: 智能化-护理通讯
    priority_level: P0-LIFE_SAFETY
  
    description: |
      医院护士呼叫系统，是患者与医护人员沟通的关键系统。
      患者通过床旁呼叫按钮向护士站发出呼叫请求，护士可通过分机与患者通话。
      系统支持普通呼叫、紧急呼叫、护理完成确认等功能。
      现代护士呼叫系统集成信息发布、护理信息管理等功能。
  
    design_basis:
      system_type: IP数字护士呼叫系统
      coverage: 全院病房、ICU、手术室等
      response_time: {value: "<1", unit: s, note: "呼叫响应"}
      backup: 主机冗余，断网不影响区域呼叫
    
    related_systems:
      - HIS: 医院信息系统（患者信息同步）
      - INT-PA: 公共广播（紧急广播联动）
      - ELEC-EPS: 应急电源（备用供电）
  
    design_standards:
      - GB 50314-2015 智能建筑设计标准
      - GB 51039-2014 综合医院建筑设计规范
      - YY 0709-2009 医用电气设备报警系统
  
    version: 1.0
    last_updated: 2024

  boundary:
    inputs:
      - boundary_id: INT-NUR_IN_001
        name: 患者呼叫信号
        from_system: 病床/卫生间
        medium: SIGNAL-CALL
      
      - boundary_id: INT-NUR_IN_002
        name: 患者信息
        from_system: HIS
        medium: DATA-HL7
        description: 患者姓名、床位、护理级别等
      
      - boundary_id: INT-NUR_IN_003
        name: 电力供应
        from_system: ELEC-LV-MAIN
        medium: ELEC-LV
      
    outputs:
      - boundary_id: INT-NUR_OUT_001
        name: 呼叫显示/声音
        to_system: 护士站/走廊
        medium: SIGNAL-AV
      
      - boundary_id: INT-NUR_OUT_002
        name: 护理记录
        to_system: HIS
        medium: DATA-HL7

  nodes:

    source_nodes:
  
      - node_id: INT-NUR_SRC_BED_UNIT
        node_name: 床旁呼叫单元
        node_name_en: Bedside Call Unit
        node_type: Source_Node
        node_category: SRC
      
        function: 患者呼叫和信息显示
        medium_in: USER_INPUT
        medium_out: SIGNAL-IP
      
        is_boundary_input: true
      
        multiplicity: multiple
        instance_pattern: INT-NUR_SRC_BED_{Ward}_{Room}_{Bed}
        typical_quantity: 按床位数
      
        equipment_parameters:
          type: 床旁分机/床头屏
          features:
            call_button:
              types: [普通呼叫, 紧急呼叫]
              indicator: LED灯显示呼叫状态
            display:
              size: {value: "7-10", unit: "寸"}
              content: 患者信息、日期时间、护理信息
            speaker_mic:
              function: 与护士站双向通话
              volume: 可调节
            cancel_button:
              function: 取消呼叫
            nurse_confirm:
              function: 护理到场确认
              method: 按键或刷卡
          power: PoE供电或本地电源
          communication: Ethernet / RS485
          mounting: 床头设备带/墙面
        
        control_points:
          inputs:
            - point_id: BED_CALL
              point_name: 普通呼叫按钮
              point_type: DI
            - point_id: BED_EMERGENCY
              point_name: 紧急呼叫按钮
              point_type: DI
            - point_id: BED_CANCEL
              point_name: 取消按钮
              point_type: DI
            - point_id: BED_NURSE_PRESENT
              point_name: 护理到场
              point_type: DI
          outputs:
            - point_id: BED_INDICATOR
              point_name: 呼叫指示灯
              point_type: DO
            - point_id: BED_DISPLAY
              point_name: 显示内容
              point_type: TEXT
      
        location_hint:
          space_type: 病房
          position: 床头（每床一个）
          height: 距床面0.5-0.8m

      - node_id: INT-NUR_SRC_BATHROOM_CALL
        node_name: 卫生间呼叫按钮
        node_name_en: Bathroom Call Button
        node_type: Source_Node
        node_category: SRC
      
        function: 卫生间紧急呼叫
        medium_in: USER_INPUT
        medium_out: SIGNAL-IO
      
        multiplicity: multiple
        instance_pattern: INT-NUR_SRC_BATH_{Ward}_{Room}
      
        equipment_parameters:
          type: 防水呼叫按钮
          protection: IP65
          features:
            - 拉绳式呼叫
            - 按钮式呼叫
            - 复位按钮
          indicator: LED指示灯
          color: 红色
          power: 总线供电
        
        control_points:
          inputs:
            - point_id: BATH_EMERGENCY
              point_name: 卫生间紧急呼叫
              point_type: DI
              priority: 紧急
      
        location_hint:
          space_type: 卫生间
          position: 坐便器旁、淋浴区
          height: 距地0.4-0.6m（拉绳垂至地面）

      - node_id: INT-NUR_SRC_CORRIDOR_BTN
        node_name: 走廊呼叫取消按钮
        node_name_en: Corridor Cancel Button
        node_type: Source_Node
        node_category: SRC
      
        function: 走廊确认/取消呼叫
        medium_in: USER_INPUT
        medium_out: SIGNAL-IO
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 门灯/门口机
          features:
            - 呼叫指示灯
            - 护理到场确认
            - 取消按钮
          display: 可选LCD显示患者信息
        
        location_hint:
          space_type: 病房门口
          position: 门口上方或侧面

    distribution_nodes:
  
      - node_id: INT-NUR_DST_FLOOR_HOST
        node_name: 楼层主机
        node_name_en: Floor Host Unit
        node_type: Distribution_Node
        node_subtype: CTR
        node_category: DST
      
        function: 楼层呼叫信号汇集和处理
        medium_in: SIGNAL-IP / SIGNAL-IO
        medium_out: SIGNAL-IP
      
        multiplicity: multiple
        instance_pattern: INT-NUR_DST_FLOOR_{Building}_{Floor}
      
        equipment_parameters:
          type: 楼层控制器/网关
          capacity: {value: "≥64", unit: "床位"}
          communication:
            uplink: Ethernet (TCP/IP)
            downlink: RS485 / CAN / Ethernet
          features:
            - 呼叫信号采集
            - 语音通话处理
            - 本地存储（断网时）
            - 独立运行能力
          power: 220V AC + 电池备份
        
        location_hint:
          space_type: 护士站/弱电间
          floor: 各楼层

      - node_id: INT-NUR_DST_NURSE_STATION
        node_name: 护士站主机
        node_name_en: Nurse Station Master Unit
        node_type: Distribution_Node
        node_subtype: HMI
        node_category: DST
      
        function: 护士站呼叫显示和处理
        medium_in: SIGNAL-IP
        medium_out: SIGNAL-AV
      
        multiplicity: multiple
        instance_pattern: INT-NUR_DST_NS_{Ward}
      
        equipment_parameters:
          type: 护士站主机/大屏
          display:
            size: {value: "22-32", unit: "寸"}
            content:
              - 全病区床位布局
              - 呼叫状态（颜色区分）
              - 患者信息
              - 呼叫时间和等待时长
          audio:
            speaker: 内置扬声器
            microphone: 内置麦克风
            handset: 可选手柄
          features:
            - 一键应答
            - 呼叫广播
            - 呼叫转移
            - 护理计时
            - 报表统计
          communication: Ethernet
        
        control_points:
          inputs:
            - point_id: NS_ANSWER
              point_name: 应答按钮
              point_type: DI
            - point_id: NS_BROADCAST
              point_name: 广播按钮
              point_type: DI
          outputs:
            - point_id: NS_DISPLAY
              point_name: 显示屏
              point_type: DISPLAY
            - point_id: NS_AUDIO
              point_name: 声音提示
              point_type: AUDIO
      
        location_hint:
          space_type: 护士站
          position: 护士工作台

      - node_id: INT-NUR_DST_CORRIDOR_DISPLAY
        node_name: 走廊显示屏
        node_name_en: Corridor Display
        node_type: Distribution_Node
        node_subtype: DIS
        node_category: DST
      
        function: 走廊呼叫显示
        medium_in: SIGNAL-IP
        medium_out: SIGNAL-AV
      
        multiplicity: multiple
      
        equipment_parameters:
          type: LCD显示屏
          size: {value: "10-15", unit: "寸"}
          content:
            - 呼叫床位号
            - 呼叫类型（颜色）
            - 等待时间
          audio: 提示音
          mounting: 走廊墙面/吊顶
        
        location_hint:
          space_type: 走廊
          position: 护士站外、病区入口

      - node_id: INT-NUR_DST_SERVER
        node_name: 护士呼叫服务器
        node_name_en: Nurse Call Server
        node_type: Distribution_Node
        node_subtype: SRV
        node_category: DST
      
        function: 系统管理和数据存储
        medium_in: SIGNAL-IP
        medium_out: SIGNAL-IP / DATA
      
        equipment_parameters:
          type: 服务器（或云平台）
          functions:
            - 系统配置管理
            - 呼叫记录存储
            - 报表生成
            - HIS接口
            - 移动终端服务
          redundancy: 双机热备
          database: SQL Server / MySQL
        
        location_hint:
          space_type: 弱电机房

    sink_nodes:
  
      - node_id: INT-NUR_SNK_MOBILE
        node_name: 移动终端
        node_name_en: Mobile Terminal
        node_type: Sink_Node
        node_category: SNK
      
        function: 护士移动接收呼叫
        medium_in: SIGNAL-WIFI
        medium_out: USER_OUTPUT
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 智能手机/PDA/对讲机
          features:
            - 呼叫推送通知
            - 语音通话
            - 护理确认
            - 患者信息查看
          app: 护士呼叫APP
        
        location_hint:
          space_type: 移动

      - node_id: INT-NUR_SNK_DOOR_LIGHT
        node_name: 门灯
        node_name_en: Door Light
        node_type: Sink_Node
        node_category: SNK
      
        function: 病房门口呼叫指示
        medium_in: SIGNAL-IO
        medium_out: LIGHT
      
        multiplicity: multiple
        instance_pattern: INT-NUR_SNK_DOOR_{Ward}_{Room}
      
        equipment_parameters:
          type: 多色门灯
          colors:
            green: 正常/无呼叫
            red: 紧急呼叫
            yellow: 普通呼叫
            blue: 护理中/输液
          mounting: 病房门口上方
        
        location_hint:
          space_type: 病房门口
          height: 门上方

  edges:

    bedside_edges:
      - edge_id: INT-NUR_EDGE_001
        edge_name: 床旁单元至楼层主机
        edge_type: NET
        from_node: INT-NUR_SRC_BED_UNIT
        to_node: INT-NUR_DST_FLOOR_HOST
        direction: bidirectional
        medium: SIGNAL-IP
        cable_parameters:
          type: Cat6 UTP
        multiplicity: multiple
      
      - edge_id: INT-NUR_EDGE_002
        edge_name: 卫生间呼叫至楼层主机
        edge_type: CAB
        from_node: INT-NUR_SRC_BATHROOM_CALL
        to_node: INT-NUR_DST_FLOOR_HOST
        direction: unidirectional
        medium: SIGNAL-IO
        cable_parameters:
          type: RVV/RVVP
        multiplicity: multiple

    floor_edges:
      - edge_id: INT-NUR_EDGE_011
        edge_name: 楼层主机至护士站
        edge_type: NET
        from_node: INT-NUR_DST_FLOOR_HOST
        to_node: INT-NUR_DST_NURSE_STATION
        direction: bidirectional
        medium: SIGNAL-IP
      
      - edge_id: INT-NUR_EDGE_012
        edge_name: 楼层主机至走廊显示
        edge_type: NET
        from_node: INT-NUR_DST_FLOOR_HOST
        to_node: INT-NUR_DST_CORRIDOR_DISPLAY
        direction: unidirectional
        medium: SIGNAL-IP
      
      - edge_id: INT-NUR_EDGE_013
        edge_name: 楼层主机至门灯
        edge_type: CAB
        from_node: INT-NUR_DST_FLOOR_HOST
        to_node: INT-NUR_SNK_DOOR_LIGHT
        direction: unidirectional
        medium: SIGNAL-IO
        multiplicity: multiple

    server_edges:
      - edge_id: INT-NUR_EDGE_021
        edge_name: 楼层主机至服务器
        edge_type: NET
        from_node: INT-NUR_DST_FLOOR_HOST
        to_node: INT-NUR_DST_SERVER
        direction: bidirectional
        medium: SIGNAL-IP
      
      - edge_id: INT-NUR_EDGE_022
        edge_name: 服务器至移动终端
        edge_type: WIFI
        from_node: INT-NUR_DST_SERVER
        to_node: INT-NUR_SNK_MOBILE
        direction: bidirectional
        medium: SIGNAL-WIFI

  typical_paths:

    - path_id: INT-NUR_PATH_NORMAL_CALL
      path_name: 普通呼叫路径
      path_type: CALL
      sequence:
        - step: 1
          node: INT-NUR_SRC_BED_UNIT
          action: 患者按下呼叫按钮
        - step: 2
          node: INT-NUR_DST_FLOOR_HOST
          action: 信号处理和转发
        - step: 3
          node: INT-NUR_DST_NURSE_STATION
          action: 护士站显示呼叫，声音提示
        - step: 4
          node: INT-NUR_SNK_DOOR_LIGHT
          action: 门灯亮黄色
        - step: 5
          node: INT-NUR_DST_CORRIDOR_DISPLAY
          action: 走廊显示呼叫床位
        - step: 6
          node: INT-NUR_SNK_MOBILE
          action: 护士手机APP推送
      response_time: "<1秒"

    - path_id: INT-NUR_PATH_EMERGENCY
      path_name: 紧急呼叫路径
      path_type: CALL
      sequence:
        - step: 1
          node: INT-NUR_SRC_BATHROOM_CALL
          action: 患者拉紧急呼叫绳
        - step: 2
          node: INT-NUR_DST_FLOOR_HOST
          action: 识别为紧急呼叫
        - step: 3
          node: INT-NUR_DST_NURSE_STATION
          action: 护士站紧急报警（声光）
        - step: 4
          node: INT-NUR_SNK_DOOR_LIGHT
          action: 门灯亮红色闪烁
        - step: 5
          node: INT-NUR_SNK_MOBILE
          action: 护士手机紧急推送
      priority: 最高优先级
      alarm: 持续报警直至确认

  control_logic:

    call_priority:
      name: 呼叫优先级
      levels:
        emergency:
          priority: 1
          color: 红色
          sound: 紧急报警音
          sources: [卫生间紧急呼叫, 床旁紧急按钮]
        urgent:
          priority: 2
          color: 橙色
          sound: 急促提示音
          sources: [输液报警]
        normal:
          priority: 3
          color: 黄色
          sound: 普通提示音
          sources: [普通呼叫]
        info:
          priority: 4
          color: 蓝色
          sound: 无
          sources: [护理中指示]
        
    response_management:
      name: 响应管理
    
      response_timing:
        start: 呼叫发起
        nurse_arrive: 护理到场确认
        complete: 护理完成确认
      
      timeout_escalation:
        level_1:
          time: 60s
          action: 显示呼叫等待时间
        level_2:
          time: 180s
          action: 声音提示升级
        level_3:
          time: 300s
          action: 通知护士长
        
    nurse_presence:
      name: 护理到场管理
    
      confirm_methods:
        - 床旁确认按钮
        - 护士工作牌刷卡
        - 走廊门口确认
      
      status_indication:
        present: 护理中（蓝灯）
        complete: 护理完成（灯灭）

  alarm_protection:
  
    critical_alarms:
      - alarm_id: ALM_NUR_EMERGENCY
        alarm_name: 紧急呼叫
        severity: CRITICAL
        trigger: 紧急呼叫按钮/拉绳
        action: 立即响应，持续报警
      
      - alarm_id: ALM_NUR_NO_RESPONSE
        alarm_name: 呼叫超时无响应
        severity: HIGH
        trigger: 呼叫超过5分钟无响应
        action: 通知护士长
      
      - alarm_id: ALM_NUR_SYSTEM_FAIL
        alarm_name: 系统故障
        severity: CRITICAL
        trigger: 服务器或网络故障
        action: 切换备用，通知维护

  dependencies:
  
    upstream_dependencies:
      - dependency_id: DEP_POWER
        from_system: ELEC-LV-MAIN
        dependency_type: POWER_SUPPLY
        criticality: CRITICAL
        backup: UPS后备
      
      - dependency_id: DEP_NETWORK
        from_system: IT-NETWORK
        dependency_type: NETWORK
        criticality: HIGH
      
      - dependency_id: DEP_HIS
        from_system: HIS
        dependency_type: DATA
        criticality: MEDIUM
        description: 患者信息同步
      
    downstream_dependencies:
      - dependency_id: DEP_NURSING
        to_system: 护理服务
        dependency_type: COMMUNICATION
        criticality: CRITICAL
```

---

## 系统 3.6: INT-SEC 安防系统

```yaml
System_Topology:

  identity:
    system_id: INT-SEC
    system_name: 安防系统
    system_name_en: Security System
    system_category: INT
    system_type: 智能化-安全防范
    priority_level: P1-CRITICAL
  
    description: |
      医院安全防范系统，包括视频监控（CCTV）、入侵报警、门禁控制等子系统。
      保障医院人员、财产和信息安全，维护正常医疗秩序。
      系统与消防、BA等系统联动，实现综合安防管理。
  
    design_basis:
      subsystems:
        - 视频监控系统（CCTV）
        - 入侵报警系统（IAS）
        - 门禁控制系统（ACS）
        - 访客管理系统
        - 电子巡更系统
      storage: {value: 30, unit: "天", note: "视频存储"}
      coverage: 全院公共区域、重要区域
    
    related_systems:
      - FIRE-FAS: 火灾报警联动
      - INT-BA: 楼宇自控联动
      - INT-NUR: 护士呼叫（紧急联动）
  
    design_standards:
      - GB 50314-2015 智能建筑设计标准
      - GB 50348-2018 安全防范工程技术标准
      - GB 50395-2007 视频安防监控系统工程设计规范
      - GB 50396-2007 出入口控制系统工程设计规范
  
    version: 1.0
    last_updated: 2024

  boundary:
    inputs:
      - boundary_id: INT-SEC_IN_001
        name: 视频信号
        from_system: 摄像机
        medium: VIDEO-IP
      
      - boundary_id: INT-SEC_IN_002
        name: 报警信号
        from_system: 探测器
        medium: SIGNAL-IO
      
      - boundary_id: INT-SEC_IN_003
        name: 门禁刷卡
        from_system: 读卡器
        medium: SIGNAL-WEIGAND
      
      - boundary_id: INT-SEC_IN_004
        name: 消防联动信号
        from_system: FIRE-FAS
        medium: SIGNAL-IO
      
    outputs:
      - boundary_id: INT-SEC_OUT_001
        name: 门锁控制
        to_system: 电锁
        medium: SIGNAL-IO
      
      - boundary_id: INT-SEC_OUT_002
        name: 报警输出
        to_system: 声光报警器
        medium: SIGNAL-IO
      
      - boundary_id: INT-SEC_OUT_003
        name: 视频显示
        to_system: 监控中心
        medium: VIDEO-IP

  nodes:

    source_nodes:
  
      - node_id: INT-SEC_SRC_CAMERA
        node_name: 网络摄像机
        node_name_en: IP Camera
        node_type: Source_Node
        node_category: SRC
      
        function: 视频图像采集
        medium_in: LIGHT
        medium_out: VIDEO-IP
      
        is_boundary_input: true
      
        multiplicity: multiple
        instance_pattern: INT-SEC_SRC_CAM_{Building}_{Floor}_{Seq}
        typical_quantity: {value: "300-500", unit: "台", note: "大型医院"}
      
        equipment_parameters:
          types:
            fixed_dome:
              description: 固定半球
              resolution: 2MP-4MP
              lens: 2.8-12mm
              application: 室内走廊、大厅
            ptz:
              description: 球型摄像机
              resolution: 2MP-4MP
              zoom: 20-30倍
              application: 室外、大范围区域
            bullet:
              description: 枪型摄像机
              resolution: 2MP-8MP
              lens: 定焦/变焦
              application: 室外周界、出入口
          common_features:
            - H.265编码
            - 宽动态(WDR)
            - 低照度
            - 红外夜视
            - PoE供电
          special_requirements:
            surgery_room: 高清、可冲洗
            icu: 隐私保护功能
            entrance: 人脸识别
          
        deployment_areas:
          - 出入口（主入口、急诊入口、地下车库）
          - 走廊（医疗区、住院部）
          - 大厅（门诊大厅、住院大厅）
          - 电梯（轿厢内、厅门口）
          - 药房/收费处
          - 手术室外/ICU外
          - 周界（围墙、停车场）
          - 重要设备区（机房、配电室）
        
        location_hint:
          space_type: 各公共区域
          height: 2.5-3.5m

      - node_id: INT-SEC_SRC_DETECTOR
        node_name: 入侵探测器
        node_name_en: Intrusion Detector
        node_type: Source_Node
        node_category: SRC
      
        function: 入侵检测报警
        medium_in: PHYSICAL
        medium_out: SIGNAL-IO
      
        is_boundary_input: true
      
        multiplicity: multiple
      
        equipment_parameters:
          types:
            pir:
              description: 被动红外探测器
              coverage: 12m×12m
              application: 室内
            dual_tech:
              description: 双鉴探测器
              technology: 红外+微波
              application: 重要区域
            magnetic:
              description: 门磁开关
              application: 门窗
            vibration:
              description: 振动探测器
              application: 保险柜、文件柜
            perimeter:
              description: 周界探测
              technology: 红外对射/电子围栏
              application: 室外周界
            
        deployment_areas:
          - 财务室
          - 药库
          - 贵重设备存放室
          - 信息机房
          - 档案室
          - 周界
        
        location_hint:
          space_type: 重要房间/周界

      - node_id: INT-SEC_SRC_CARD_READER
        node_name: 门禁读卡器
        node_name_en: Access Control Reader
        node_type: Source_Node
        node_category: SRC
      
        function: 身份识别和权限验证
        medium_in: CARD/BIO
        medium_out: SIGNAL-WEIGAND
      
        is_boundary_input: true
      
        multiplicity: multiple
        instance_pattern: INT-SEC_SRC_READER_{Building}_{Floor}_{Door}
      
        equipment_parameters:
          types:
            ic_card:
              technology: Mifare/CPU卡
              frequency: 13.56MHz
              application: 普通门禁
            biometric:
              technology: 指纹/人脸
              application: 高安全区域
            qr_code:
              technology: 二维码
              application: 访客通道
          output: Wiegand 26/34
          protection: IP65（室外）
        
        deployment_areas:
          - 医院主入口（员工通道）
          - 住院部入口
          - 手术室入口
          - ICU/CCU入口
          - 新生儿科入口
          - 药房/药库
          - 信息机房
          - 配电室/弱电间
          - 行政办公区
        
        location_hint:
          space_type: 门禁点
          height: 1.2-1.4m

    distribution_nodes:
  
      - node_id: INT-SEC_DST_NVR
        node_name: 网络硬盘录像机
        node_name_en: Network Video Recorder
        node_type: Distribution_Node
        node_subtype: SRV
        node_category: DST
      
        function: 视频录制和存储
        medium_in: VIDEO-IP
        medium_out: VIDEO-IP
      
        multiplicity: multiple
        instance_pattern: INT-SEC_DST_NVR_{Zone}_{Seq}
      
        equipment_parameters:
          type: 网络硬盘录像机
          channels: 32/64路
          resolution: 4K解码
          storage:
            capacity: {value: "8-16", unit: TB}
            raid: RAID5/RAID6
            duration: {value: 30, unit: "天"}
          features:
            - 智能检索
            - 人脸识别（可选）
            - 行为分析（可选）
          network: 千兆/万兆
        
        location_hint:
          space_type: 弱电机房/监控中心

      - node_id: INT-SEC_DST_ACCESS_CONTROLLER
        node_name: 门禁控制器
        node_name_en: Access Controller
        node_type: Distribution_Node
        node_subtype: CTR
        node_category: DST
      
        function: 门禁逻辑控制
        medium_in: SIGNAL-WEIGAND
        medium_out: SIGNAL-IO
      
        multiplicity: multiple
        instance_pattern: INT-SEC_DST_AC_{Building}_{Floor}
      
        equipment_parameters:
          type: 门禁控制器
          doors: 1/2/4门
          capacity: {value: "≥10000", unit: "张卡"}
          records: {value: "≥100000", unit: "条"}
          features:
            - 防潜回
            - 首卡开门
            - 多卡开门
            - 联动输出
          communication: TCP/IP / RS485
          power: 12V DC
          backup_battery: 4小时后备
        
        fire_linkage:
          description: 消防联动
          signal: FIRE-FAS干接点信号
          action: 断电开门（紧急疏散）
        
        location_hint:
          space_type: 弱电间
          floor: 各楼层

      - node_id: INT-SEC_DST_ALARM_HOST
        node_name: 报警主机
        node_name_en: Alarm Control Panel
        node_type: Distribution_Node
        node_subtype: CTR
        node_category: DST
      
        function: 入侵报警信号处理
        medium_in: SIGNAL-IO
        medium_out: SIGNAL-IP
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 报警控制主机
          zones: 8/16/32防区
          features:
            - 布撤防控制
            - 防区编程
            - 报警联动
            - 事件记录
          communication: TCP/IP / GPRS
          power: 220V AC + 蓄电池
        
        location_hint:
          space_type: 监控中心/弱电间

      - node_id: INT-SEC_DST_MANAGEMENT_PLATFORM
        node_name: 安防管理平台
        node_name_en: Security Management Platform
        node_type: Distribution_Node
        node_subtype: SRV
        node_category: DST
      
        function: 安防系统综合管理
        medium_in: SIGNAL-IP
        medium_out: SIGNAL-IP / VIDEO
      
        equipment_parameters:
          type: 综合安防管理平台
          architecture: B/S + C/S
          modules:
            - 视频管理（VMS）
            - 门禁管理
            - 报警管理
            - 访客管理
            - 巡更管理
            - 智能分析
          server:
            cpu: Xeon 8核
            memory: {value: 64, unit: GB}
            storage: SAS阵列
          features:
            - 统一界面
            - GIS地图
            - 报警联动
            - 报表统计
            - 移动APP
          
        integration:
          - system: FIRE-FAS
            type: 联动
            action: 火灾时自动调取火警区域摄像机
          - system: INT-BA
            type: 联动
            action: 入侵报警时开启区域照明
          - system: HIS
            type: 数据
            action: 员工信息同步
          
        location_hint:
          space_type: 弱电机房/监控中心

    sink_nodes:
  
      - node_id: INT-SEC_SNK_MONITOR_CENTER
        node_name: 监控中心
        node_name_en: Security Control Center
        node_type: Sink_Node
        node_category: SNK
      
        function: 安防系统人机界面
        medium_in: VIDEO-IP / SIGNAL-IP
        medium_out: DISPLAY / AUDIO
      
        equipment_parameters:
          display:
            video_wall:
              size: "3×4 LCD拼接屏"
              resolution: 4K
            workstation: 3-5台操作电脑
          audio:
            intercom: 对讲设备
            alarm: 报警扬声器
          furniture:
            console: 控制台
            chair: 值班椅
          environment:
            lighting: 可调光照明
            ac: 24小时空调
          
        operation:
          mode: 24小时值班
          personnel: 2人/班
        
        location_hint:
          space_type: 监控中心
          floor: 1F或B1
          area: {value: ">50", unit: "m²"}

      - node_id: INT-SEC_SNK_DOOR_LOCK
        node_name: 电锁
        node_name_en: Electric Lock
        node_type: Sink_Node
        node_category: SNK
      
        function: 门控制执行
        medium_in: SIGNAL-IO
        medium_out: MECHANICAL
      
        is_boundary_output: true
      
        multiplicity: multiple
      
        equipment_parameters:
          types:
            electric_strike:
              description: 电锁口
              application: 玻璃门/木门
              fail_mode: 断电开门（常用）
            magnetic_lock:
              description: 电磁锁
              holding_force: 280kg
              application: 玻璃门
              fail_mode: 断电开门
            motor_lock:
              description: 电机锁
              application: 防盗门
              fail_mode: 可选
          power: 12V DC
        
        location_hint:
          space_type: 门禁点

      - node_id: INT-SEC_SNK_ALARM_DEVICE
        node_name: 声光报警器
        node_name_en: Audio-Visual Alarm Device
        node_type: Sink_Node
        node_category: SNK
      
        function: 报警警示
        medium_in: SIGNAL-IO
        medium_out: LIGHT / SOUND
      
        is_boundary_output: true
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 声光报警器
          sound: {value: ">100", unit: "dB"}
          light: LED频闪
          color: 红色
          power: 12V DC
        
        location_hint:
          space_type: 报警区域

  edges:

    video_edges:
      - edge_id: INT-SEC_EDGE_001
        edge_name: 摄像机至NVR
        edge_type: NET
        from_node: INT-SEC_SRC_CAMERA
        to_node: INT-SEC_DST_NVR
        direction: unidirectional
        medium: VIDEO-IP
        cable_parameters:
          type: Cat6 UTP
        multiplicity: multiple
      
      - edge_id: INT-SEC_EDGE_002
        edge_name: NVR至管理平台
        edge_type: NET
        from_node: INT-SEC_DST_NVR
        to_node: INT-SEC_DST_MANAGEMENT_PLATFORM
        direction: bidirectional
        medium: SIGNAL-IP

    access_edges:
      - edge_id: INT-SEC_EDGE_011
        edge_name: 读卡器至控制器
        edge_type: CAB
        from_node: INT-SEC_SRC_CARD_READER
        to_node: INT-SEC_DST_ACCESS_CONTROLLER
        direction: unidirectional
        medium: SIGNAL-WEIGAND
        cable_parameters:
          type: RVV/RVVP
        multiplicity: multiple
      
      - edge_id: INT-SEC_EDGE_012
        edge_name: 控制器至电锁
        edge_type: CAB
        from_node: INT-SEC_DST_ACCESS_CONTROLLER
        to_node: INT-SEC_SNK_DOOR_LOCK
        direction: unidirectional
        medium: SIGNAL-IO
        multiplicity: multiple
      
      - edge_id: INT-SEC_EDGE_013
        edge_name: 控制器至管理平台
        edge_type: NET
        from_node: INT-SEC_DST_ACCESS_CONTROLLER
        to_node: INT-SEC_DST_MANAGEMENT_PLATFORM
        direction: bidirectional
        medium: SIGNAL-IP

    alarm_edges:
      - edge_id: INT-SEC_EDGE_021
        edge_name: 探测器至报警主机
        edge_type: CAB
        from_node: INT-SEC_SRC_DETECTOR
        to_node: INT-SEC_DST_ALARM_HOST
        direction: unidirectional
        medium: SIGNAL-IO
        cable_parameters:
          type: RVV 4×0.5
        multiplicity: multiple
      
      - edge_id: INT-SEC_EDGE_022
        edge_name: 报警主机至声光报警器
        edge_type: CAB
        from_node: INT-SEC_DST_ALARM_HOST
        to_node: INT-SEC_SNK_ALARM_DEVICE
        direction: unidirectional
        medium: SIGNAL-IO
      
      - edge_id: INT-SEC_EDGE_023
        edge_name: 报警主机至管理平台
        edge_type: NET
        from_node: INT-SEC_DST_ALARM_HOST
        to_node: INT-SEC_DST_MANAGEMENT_PLATFORM
        direction: bidirectional
        medium: SIGNAL-IP

    display_edges:
      - edge_id: INT-SEC_EDGE_031
        edge_name: 管理平台至监控中心
        edge_type: NET
        from_node: INT-SEC_DST_MANAGEMENT_PLATFORM
        to_node: INT-SEC_SNK_MONITOR_CENTER
        direction: bidirectional
        medium: VIDEO-IP / SIGNAL-IP

  typical_paths:

    - path_id: INT-SEC_PATH_ACCESS
      path_name: 门禁通行路径
      path_type: CTR
      sequence:
        - step: 1
          node: INT-SEC_SRC_CARD_READER
          action: 员工刷卡
        - step: 2
          node: INT-SEC_DST_ACCESS_CONTROLLER
          action: 验证权限
        - step: 3
          node: INT-SEC_SNK_DOOR_LOCK
          action: 开门（如授权）
        - step: 4
          node: INT-SEC_DST_MANAGEMENT_PLATFORM
          action: 记录通行事件
      response_time: "<1秒"

    - path_id: INT-SEC_PATH_INTRUSION
      path_name: 入侵报警路径
      path_type: ALM
      sequence:
        - step: 1
          node: INT-SEC_SRC_DETECTOR
          action: 探测器触发
        - step: 2
          node: INT-SEC_DST_ALARM_HOST
          action: 报警信号处理
        - step: 3
          node: INT-SEC_SNK_ALARM_DEVICE
          action: 现场声光报警
        - step: 4
          node: INT-SEC_DST_MANAGEMENT_PLATFORM
          action: 上传报警信息
        - step: 5
          node: INT-SEC_SNK_MONITOR_CENTER
          action: 显示报警，调取视频
      response_time: "<3秒"

  control_logic:

    fire_linkage:
      name: 消防联动控制
      description: 火灾时门禁系统联动
    
      trigger:
        signal: 消防系统干接点信号
        source: FIRE-FAS
      
      action:
        - 疏散通道门禁断电开门
        - 保留重要区域门禁（如药库）
        - 记录联动事件
        - 调取火警区域摄像机
      
    access_control_rules:
      name: 门禁控制规则
    
      time_schedule:
        description: 时间计划
        examples:
          - 工作时间自由通行
          - 非工作时间刷卡通行
          - 深夜时段多重认证
        
      area_rules:
        description: 区域规则
        examples:
          - 手术室：特定人员+时段授权
          - 药库：多人多卡
          - ICU：护理人员+家属限时
        
      anti_passback:
        description: 防潜回
        logic: 进入记录后才能刷卡离开
      
    video_intelligent:
      name: 视频智能分析
    
      functions:
        - 人脸识别（黑/白名单）
        - 人群聚集检测
        - 徘徊检测
        - 物品遗留检测
        - 越界检测（周界）
      
      alarm_linkage:
        trigger: 智能分析触发
        action:
          - 弹出报警视频
          - 记录抓拍图片
          - 推送报警信息

  alarm_protection:
  
    critical_alarms:
      - alarm_id: ALM_SEC_INTRUSION
        alarm_name: 入侵报警
        severity: CRITICAL
        trigger: 布防状态下探测器触发
        action: 声光报警，监控中心处理
      
      - alarm_id: ALM_SEC_DOOR_FORCED
        alarm_name: 门禁强行开门
        severity: HIGH
        trigger: 未授权开门（门磁触发）
        action: 报警，调取视频
      
      - alarm_id: ALM_SEC_CAMERA_OFFLINE
        alarm_name: 摄像机离线
        severity: MEDIUM
        trigger: 摄像机视频丢失
        action: 通知维护

  dependencies:
  
    upstream_dependencies:
      - dependency_id: DEP_POWER
        from_system: ELEC-LV-MAIN
        dependency_type: POWER_SUPPLY
        criticality: CRITICAL
        backup: UPS后备
      
      - dependency_id: DEP_NETWORK
        from_system: IT-NETWORK
        dependency_type: NETWORK
        criticality: HIGH
      
      - dependency_id: DEP_FIRE
        from_system: FIRE-FAS
        dependency_type: LINKAGE
        criticality: HIGH
      
    downstream_dependencies:
      - dependency_id: DEP_ACCESS
        to_system: 门禁点
        dependency_type: CONTROL
        criticality: HIGH
```

---

# 第三批次输出完成

## 批次总结

| 系统ID | 系统名称 | 类别 | 优先级 | 主要特点 |
|--------|----------|------|--------|----------|
| PLUMB-DWS | 生活给水系统 | PLUMB | P1 | 双路市政进水、变频加压、二次消毒 |
| PLUMB-HWS | 生活热水系统 | PLUMB | P2 | 热水循环、防军团菌、恒温混水 |
| PLUMB-SAN | 排水系统 | PLUMB | P1 | 普通/医疗/传染分流、预消毒处理 |
| INT-BA | 楼宇自动化系统 | INT | P1 | 三层架构、DDC控制、能源管理 |
| INT-NUR | 护士呼叫系统 | INT | P0 | 三级呼叫优先级、移动终端、HIS集成 |
| INT-SEC | 安防系统 | INT | P1 | 视频/门禁/报警集成、消防联动 |

## 关键控制逻辑覆盖

| 系统 | 关键控制逻辑 |
|------|--------------|
| PLUMB-DWS | 水箱液位控制、变频恒压供水、水质控制 |
| PLUMB-HWS | 热水温度控制、循环泵控制、防军团菌周期加热、防烫伤保护 |
| PLUMB-SAN | 污水提升泵控制、传染科预消毒控制 |
| INT-BA | HVAC集成控制、电力监控、统一报警管理 |
| INT-NUR | 呼叫优先级、响应超时升级、护理到场管理 |
| INT-SEC | 消防联动、门禁规则、视频智能分析 |

---

# Agent-01 系统拓扑建模师 - 第三批次修订版

## 修订说明

根据评审意见，本次修订重点解决以下问题：
- **P1**: PLUMB-DWS与PLUMB-HWS的冷热水平衡
- **P2**: INT-BA与INT-NUR的优先级冲突
- **P3**: INT-SEC门禁与消防疏散的矛盾
- **P4**: INT-BA的DDC独立运行与系统联动的平衡
- **P5**: PLUMB-HWS的防军团菌周期加热与患者舒适度
- **P6**: INT-SEC的人脸识别隐私问题
- **P7**: PLUMB-DWS故障时对MGAS-AIR的影响

同时新增：
- **系统间接口规范**
- **关键依赖关系表**
- **跨系统协调矩阵**

---

# 给排水系统修订

## 系统 3.1: PLUMB-DWS 生活给水系统（P1/P7修订补充）

在原有内容基础上，补充以下控制逻辑和依赖关系：

```yaml
  # ========================================
  # CONTROL LOGIC SECTION - 补充冷热水平衡
  # ========================================
  control_logic:

    # === 原有控制逻辑保留 ===
    tank_level_control:
      # ... 原有内容 ...
  
    pump_control:
      # ... 原有内容 ...
  
    water_quality_control:
      # ... 原有内容 ...
  
    # === P1修复：冷热水平衡控制 ===
    cold_hot_water_balance:
      name: 冷热水压力平衡控制
      description: 确保混水点冷热水压力匹配，防止温度波动
    
      problem_statement: |
        PLUMB-DWS设计供水压力恒定0.45MPa
        PLUMB-HWS的热水供水压力约0.3-0.35MPa
        两系统独立控制，可能造成冷热水压力不平衡
      
      risk_scenarios:
        - scenario: 冷水压力突增
          cause: 用水低峰期，泵出口压力升高
          effect: 混水阀出水偏冷
          impact: 患者体验差
        
        - scenario: 冷水压力下降
          cause: 用水高峰期，多点同时用水
          effect: 混水阀出水偏热
          impact: 烫伤风险
        
        - scenario: 热水循环停止
          cause: 循环泵故障
          effect: 热水管道温度下降
          impact: 出水先冷后热
    
      solution_design:
        primary_solution:
          name: 冷水减压+压力平衡阀组合
        
          cold_water_prv:
            description: 热水系统冷水进口设减压阀
            location: PLUMB-HWS_SRC_CW_IN节点
            inlet_pressure: {value: 0.45, unit: MPa}
            outlet_pressure: {value: 0.35, unit: MPa, note: "略高于热水压力"}
            device: 可调式减压阀
            sizing: 按热水系统最大需求流量
          
          tmv_selection:
            description: 选用压力平衡型混水阀
            feature: 内置压力平衡机构
            function: 自动调节冷热水流量比例
            response_time: {value: "<1", unit: s}
            temperature_stability: {value: "±2", unit: ℃}
            standard: ASSE 1016 / EN 1111
          
          pressure_monitoring:
            description: 关键点压力监测
            points:
              - location: 热水系统冷水进口
                setpoint: 0.35MPa
                alarm_low: 0.25MPa
                alarm_high: 0.45MPa
              - location: 热水供水主管
                setpoint: 0.30MPa
                alarm_low: 0.20MPa
                alarm_high: 0.40MPa
      
        alternative_solution:
          name: 统一加压方案
          description: 冷热水共用一套加压系统
          configuration: |
            1. 冷水泵组出口分两路
            2. 一路直接供冷水
            3. 另一路经热水系统后供热水
            4. 两路末端压力自然平衡
          advantage: 压力绝对平衡
          disadvantage: 系统复杂度增加
          note: 适用于新建项目
    
      control_points:
        sensors:
          - point_id: CW_PRESSURE_HWS_IN
            point_name: 热水系统冷水进口压力
            point_type: AI
            unit: MPa
            range: [0, 0.6]
            normal: 0.35
          
          - point_id: CW_HW_PRESSURE_DIFF
            point_name: 冷热水压力差
            point_type: CAL
            unit: MPa
            calculation: CW_PRESSURE_HWS_IN - HW_SUPPLY_P
            normal_range: [-0.05, 0.1]
          
          - point_id: TMV_TEMP_STABILITY
            point_name: 混水出口温度波动
            point_type: CAL
            unit: ℃/min
            calculation: 温度变化率（5分钟滑动窗口）
            requirement: "<0.5"
          
        status:
          - point_id: CW_HW_BALANCE_OK
            point_name: 冷热水平衡正常
            point_type: DI
            logic: |
              CW_HW_PRESSURE_DIFF在正常范围内
              且TMV_TEMP_STABILITY<0.5
            
        alarms:
          - point_id: ALM_PRESSURE_IMBALANCE
            point_name: 冷热水压力失衡
            severity: HIGH
            trigger: |
              CW_HW_PRESSURE_DIFF > 0.15MPa 或 < -0.1MPa
              持续超过2分钟
            action: 报警，检查减压阀和泵组
    
      integration_with_hws:
        description: 与热水系统的协调
        data_sharing:
          to_hws:
            - 冷水进口压力
            - 冷水流量
          from_hws:
            - 热水供水压力
            - 循环泵状态
        coordination: 通过INT-BA系统实现数据交换

    # === P7修复：对MGAS-AIR的保障 ===
    critical_water_users_protection:
      name: 关键用水保障
      description: 保障医用气体冷却水等关键用水需求
    
      critical_users:
        - user: MGAS-AIR压缩空气冷却
          dependency_type: 冷却水
          failure_tolerance: 4小时
          priority: 1
        
        - user: HVAC-CHP冷却塔
          dependency_type: 补水
          failure_tolerance: 2小时
          priority: 1
        
        - user: 热水系统
          dependency_type: 冷水源
          failure_tolerance: 1小时
          priority: 2
        
        - user: 一般卫生洁具
          dependency_type: 生活用水
          failure_tolerance: 4小时
          priority: 3
    
      failure_cascade_prevention:
        scenario: PLUMB-DWS主供水故障
      
        stage_1_warning:
          trigger: 水箱液位<50%
          actions:
            - 报警通知设备科
            - 检查市政进水状态
            - 准备启用备用措施
          
        stage_2_protection:
          trigger: 水箱液位<30%
          actions:
            - 发出高级报警
            - 关闭非关键用水（绿化、洗车等）
            - 保持关键用水（医疗、生活）
            - 通知冷却塔进入节水模式
          
        stage_3_emergency:
          trigger: 水箱液位<15%
          actions:
            - 发出紧急报警
            - 停止热水系统供水（保留储水）
            - 仅保留关键医疗用水
            - 通知MGAS-AIR系统准备应急
            - 联系消防水池应急补水（如允许）
    
      mgas_air_specific_protection:
        description: 医用压缩空气冷却水专项保障
      
        monitoring:
          - point_id: COOLING_WATER_FLOW
            point_name: 压缩空气冷却水流量
            point_type: AI
            unit: "m³/h"
            alarm_low: "低于设计值80%"
          
          - point_id: COMPRESSOR_COOLING_TEMP
            point_name: 压缩空气冷却器出口温度
            point_type: AI
            unit: ℃
            normal: "<25"
            warning: ">30"
            alarm: ">35"
      
        backup_measures:
          measure_1:
            name: 冷却塔备用补水接口
            equipment: 应急补水接口（DN50）
            source: 消防水池/移动水车
            activation: 手动阀门开启
            duration: 可维持4-8小时
          
          measure_2:
            name: 冷却水循环独立
            description: |
              冷却水系统设置独立储水
              不完全依赖实时补水
            storage: {value: 10, unit: "m³"}
            note: 可独立运行2-3小时
          
        coordination_signal:
          to_mgas_air:
            signal: DWS_COOLING_WATER_ALERT
            meaning: 冷却水供应受威胁
            action: MGAS-AIR系统启动节能/保护模式
          
          from_mgas_air:
            signal: AIR_COOLING_DEMAND
            meaning: 压缩机冷却水需求状态
            action: 优先保障冷却水供应

  # ========================================
  # DEPENDENCIES SECTION - 修订依赖关系
  # ========================================
  dependencies:
  
    upstream_dependencies:
      # ... 原有内容保留 ...
    
    downstream_dependencies:
      # ... 原有内容保留 ...
    
      - dependency_id: DEP_MGAS_COOLING
        to_system: MGAS-AIR
        dependency_type: COOLING_WATER
        criticality: HIGH
        description: 医用压缩空气冷却水供应
        failure_tolerance: {value: 4, unit: h}
        backup_measure: 冷却塔备用补水接口
```

---

## 系统 3.2: PLUMB-HWS 生活热水系统（P1/P5修订补充）

```yaml
  # ========================================
  # CONTROL LOGIC SECTION - 补充防军团菌优化
  # ========================================
  control_logic:

    # === 原有控制逻辑保留 ===
    temperature_control:
      # ... 原有内容 ...
  
    circulation_control:
      # ... 原有内容 ...
  
    # === P1修复：与冷水系统协调 ===
    cold_water_coordination:
      name: 与冷水系统压力协调
      description: 接收冷水系统减压后的供水
    
      inlet_prv:
        location: PLUMB-HWS_SRC_CW_IN
        inlet_pressure: {value: 0.45, unit: MPa}
        outlet_pressure: {value: 0.35, unit: MPa}
        type: 弹簧式减压阀
        sizing: DN80
        maintenance: 每年检查校准
      
      pressure_monitoring:
        point: CW_IN_PRESSURE
        setpoint: 0.35MPa
        alarm_low: 0.25MPa
        alarm_high: 0.45MPa
      
      integration:
        receive_from_dws:
          - 冷水供水压力（PLUMB-DWS出口）
          - 冷水供水状态
        send_to_dws:
          - 热水系统冷水需求状态
          - 热水循环泵状态

    # === P5修复：防军团菌优化方案 ===
    anti_legionella_refined:
      name: 防军团菌优化控制
      description: 安全且有效的周期性杀菌方案
    
      current_risk_analysis:
        scenario: 凌晨2:00开始全系统加热至70℃
        risks:
          - risk_1:
              description: ICU/新生儿科24小时可能用热水
              consequence: 加热期间若用水，70℃热水直接到终端
              severity: 严重烫伤
          - risk_2:
              description: 恒温混水阀可能失效
              consequence: 输入70℃时混水阀无法有效降温
              severity: 烫伤
          - risk_3:
              description: 管道热膨胀
              consequence: 快速升温可能导致接头泄漏
              severity: 中等
    
      improved_solution:
        name: 隔离循环加热法
        description: 加热期间隔离供水，仅循环杀菌
      
        pre_conditions:
          time_window: "02:00-04:30（非高峰）"
          notice: 提前在护士站/值班室显示通知
        
        procedure:
          phase_1_preparation:
            time: "01:55-02:00"
            actions:
              - 在护士站显示"热水系统维护中"
              - 检查无紧急热水需求
              - 确认循环泵正常
            duration: 5分钟
          
          phase_2_isolation:
            time: "02:00-02:05"
            actions:
              - 关闭热水供水泵
              - 关闭所有区域供水阀（电动阀）
              - 仅保留储罐-循环泵回路
            duration: 5分钟
            monitoring:
              - 确认供水阀全关
              - 确认供水压力降至0
            
          phase_3_heating:
            time: "02:05-03:00"
            actions:
              - 启动加热至70℃
              - 循环泵运行
              - 70℃热水在储罐-循环管道内循环
              - 管道温度逐步升至65℃以上
            duration: 55分钟
            monitoring:
              - 储罐温度
              - 循环回水温度
              - 管道各点温度（如有）
            target:
              tank_temp: ">70℃持续30分钟"
              return_temp: ">65℃"
            
          phase_4_cooling:
            time: "03:00-03:45"
            actions:
              - 停止加热
              - 循环泵继续运行
              - 注入冷水降温
              - 温度降至55℃
            duration: 45分钟
            monitoring:
              - 储罐温度下降曲线
              - 出口温度稳定性
            target:
              tank_temp: "<58℃"
              outlet_temp: "55±2℃"
            
          phase_5_recovery:
            time: "03:45-04:00"
            actions:
              - 开启区域供水阀
              - 启动供水泵
              - 取消"维护中"通知
              - 恢复正常供水
            duration: 15分钟
            verification:
              - 各终端出水温度正常
              - 压力恢复正常
              - 无异常报警
      
        safety_interlocks:
          interlock_1:
            name: 供水隔离确认
            logic: |
              加热启动前必须确认：
              - 供水泵已停止
              - 区域供水阀已关闭
              - 供水压力<0.05MPa
            failure_action: 禁止加热启动
          
          interlock_2:
            name: 紧急中断
            trigger:
              - 任一区域供水阀异常开启
              - 供水泵异常启动
              - 温度>75℃
            action: 立即停止加热，切换至应急模式
          
          interlock_3:
            name: 超时保护
            trigger: 加热阶段超过90分钟
            action: 强制进入冷却阶段
      
        control_points:
          status:
            - point_id: LEGIONELLA_CYCLE_ACTIVE
              point_name: 防菌周期运行中
              point_type: DI
            
            - point_id: SUPPLY_ISOLATED
              point_name: 供水已隔离
              point_type: DI
            
            - point_id: HEATING_PHASE
              point_name: 当前阶段
              point_type: AI
              values: [准备, 隔离, 加热, 冷却, 恢复, 完成]
            
          commands:
            - point_id: LEGIONELLA_MANUAL_START
              point_name: 手动启动防菌周期
              point_type: DO
              note: 仅限维护人员
            
            - point_id: LEGIONELLA_EMERGENCY_STOP
              point_name: 紧急中断
              point_type: DO
      
        scheduling:
          automatic:
            frequency: 每周日凌晨2:00
            enabled: true
          manual:
            available: true
            authorization: 维护工程师
          skip_conditions:
            - 上周已执行且水质检测合格
            - 医院有重大活动（需提前设置）
          
        documentation:
          auto_record:
            - 执行时间
            - 各阶段温度曲线
            - 完成状态
            - 异常事件
          retention: 2年
          report: 每月汇总报告

    # === 原有anti_scald保留并增强 ===
    anti_scald_enhanced:
      name: 防烫伤保护（增强版）
      description: 多层次防烫伤措施
    
      layer_1_source:
        description: 储罐出口限温
        method: 储罐出口设限温阀
        max_temp: {value: 60, unit: ℃}
        note: 正常运行时不超过60℃
        exception: 防菌加热期间供水隔离
      
      layer_2_zone:
        description: 区域混水阀
        method: 每个区域入口设恒温混水阀
        outlet_temp: {value: 45, unit: ℃}
        type: 压力平衡型恒温阀
        fail_safe: 热水失压时自动关闭
      
      layer_3_terminal:
        description: 终端恒温龙头
        method: 淋浴器/洗手池设恒温龙头
        outlet_temp: {value: "38-42", unit: ℃}
        feature: 防烫锁定功能
      
      special_areas:
        pediatrics:
          max_temp: {value: 40, unit: ℃}
          method: 区域混水阀设定40℃
        geriatrics:
          max_temp: {value: 40, unit: ℃}
          method: 区域混水阀设定40℃
        psychiatric:
          max_temp: {value: 38, unit: ℃}
          method: 恒温龙头锁定38℃
          note: 防止患者调节温度
        
      monitoring:
        - point_id: HW_MAX_TEMP_VIOLATION
          point_name: 热水超温事件
          point_type: DI
          trigger: 任一终端温度>50℃
          action: 立即报警，记录事件
```

---

# 智能化系统修订

## 系统 3.4: INT-BA 楼宇自动化系统（P2/P4修订补充）

```yaml
  # ========================================
  # CONTROL LOGIC SECTION - 补充优先级和独立运行
  # ========================================
  control_logic:

    # === 原有控制逻辑保留 ===
    hvac_integration:
      # ... 原有内容 ...
  
    electrical_monitoring:
      # ... 原有内容 ...
  
    # === P2修复：系统间告警优先级 ===
    cross_system_alarm_priority:
      name: 跨系统告警优先级管理
      description: 定义INT-BA与其他系统的告警优先级关系
    
      priority_hierarchy:
        level_0_life_critical:
          description: 生命安全级（不可覆盖）
          systems:
            - FIRE-FAS: 火灾报警
            - INT-NUR: 紧急呼叫（红色）
            - MGAS: 医用气体危急
          display_rule: 全屏显示，持续闪烁
          audio_rule: 最高音量报警
          override: 不可被任何其他报警覆盖
        
        level_1_critical:
          description: 关键设备级
          systems:
            - INT-BA: 关键设备故障（冷水机/水泵/发电机）
            - INT-SEC: 入侵报警
            - INT-NUR: 普通呼叫（黄色）
          display_rule: 主显示区域
          audio_rule: 报警音（可静音60秒）
          override: 可被Level_0覆盖
        
        level_2_warning:
          description: 警告级
          systems:
            - INT-BA: 一般设备警告
            - INT-SEC: 门禁异常
            - PLUMB: 水压/水质警告
          display_rule: 次要显示区域（右下角）
          audio_rule: 提示音（可静音）
          override: 可被Level_0/1覆盖
        
        level_3_info:
          description: 信息级
          systems:
            - INT-BA: 维护提醒
            - INT-NUR: 护理确认
          display_rule: 状态栏
          audio_rule: 无
          override: 可被任何更高级别覆盖
    
      display_conflict_resolution:
        rule_1:
          scenario: INT-NUR紧急呼叫 + INT-BA设备故障
          resolution: |
            - 主屏显示INT-NUR紧急呼叫
            - INT-BA设备故障显示在右下角小窗
            - 两个报警音叠加播放
          rationale: 患者生命优先于设备
        
        rule_2:
          scenario: FIRE-FAS火灾 + 任何其他报警
          resolution: |
            - 全屏显示火灾报警
            - 其他报警暂时隐藏（记录中）
            - 仅播放火灾报警音
          rationale: 火灾疏散优先于一切
        
        rule_3:
          scenario: 多个同级别报警
          resolution: |
            - 按时间顺序排列显示
            - 最新报警在最前
            - 可滚动查看
          rationale: 先发生的可能已在处理
    
      implementation:
        unified_alarm_manager:
          location: INT-BA服务器
          function: 统一接收和处理所有系统告警
          integration:
            - INT-NUR: API接口
            - INT-SEC: API接口
            - FIRE-FAS: 硬接点+网络
            - MGAS: 网络接口
          processing:
            - 接收告警
            - 判断优先级
            - 分配显示资源
            - 触发声音报警
            - 记录日志
          
        display_resource_pool:
          screens:
            - 监控中心大屏（共享）
            - 各工作站屏幕
            - 护士站屏幕
          allocation:
            - 根据优先级动态分配
            - 高优先级可抢占低优先级
            - 释放后自动恢复

    # === P4修复：DDC独立运行策略 ===
    network_independent_strategy:
      name: DDC网络独立运行策略
      description: 确保网络故障时DDC仍能正常控制
    
      independent_operation_capability:
        description: DDC独立运行能力
        features:
          - 完整的控制程序存储在DDC本地
          - 断网后继续执行控制逻辑
          - 本地时间程序继续运行
          - 报警信息本地存储，联网后上传
        
        limitations:
          - 失去远程监控能力
          - 失去群控优化功能
          - 时间程序可能漂移（长期断网）
    
      critical_signal_transmission:
        description: 关键联动信号的传输方式
      
        fire_linkage:
          signal: FIRE-FAS火灾报警
          primary: 网络通讯（TCP/IP）
          fallback: 硬接点干触点（直连DDC）
          action: 关闭空调风机，开启排烟
          failsafe: |
            1. DDC设置"火灾输入点"
            2. FIRE-FAS干接点直接连接到DDC DI
            3. 无论网络状态，干接点触发即执行
          verification: 每月测试一次干接点联动
        
        security_linkage:
          signal: INT-SEC入侵报警
          primary: 网络通讯
          action: 开启区域照明
          failsafe: |
            1. 入侵报警可通过网络触发
            2. 网络故障时，手动控制照明
            3. 安保人员现场处理
          note: 安保联动非生命安全，可依赖网络
        
        gas_alarm_linkage:
          signal: MGAS气体报警
          primary: 网络通讯（Modbus）
          fallback: 硬接点（用于危急报警）
          action: 报警显示
          note: 医用气体系统自身有独立报警
    
      ddc_failsafe_program:
        name: DDC失网保护程序
        description: 网络中断时的运行模式
      
        detection:
          method: DDC定期向服务器发送心跳
          timeout: 5分钟无响应判定为断网
        
        failsafe_mode_activation:
          trigger: 断网超过5分钟
          actions:
            - 记录断网事件
            - 切换至失网保护模式
            - 本地显示"离线运行"状态
          
        failsafe_control_rules:
          hvac:
            chiller: 保持恒温运行（不优化）
            chilled_water_pump: 保持当前状态
            cooling_tower: 保持当前状态
            ahu: 保持基础通风（不节能）
            fcu: 保持当前设定温度
            note: 失去优化控制，能效下降约10-15%
          
          lighting:
            rule: 按时间程序运行
            override: 现场开关可覆盖
          
          other:
            rule: 保持当前状态
          
        fire_signal_handling:
          description: 失网状态下的火灾处理
          logic: |
            1. FIRE信号通过硬接点到达DDC
            2. DDC检测到火灾DI触发
            3. 立即执行火灾联动：
               - 关闭空调风机
               - 开启排烟风机（如受DDC控制）
               - 关闭新风阀
               - 记录事件
          verification: 每月断网测试火灾联动
        
        recovery:
          detection: 服务器心跳恢复
          delay: 确认连接稳定30秒
          actions:
            - 上传离线期间的数据和报警
            - 恢复远程监控
            - 恢复优化控制
            - 记录恢复事件
    
      hardware_requirements:
        fire_di_allocation:
          description: 每个DDC预留火灾联动输入点
          quantity: 至少1个DI
          wiring: FIRE-FAS干接点信号直接接入
        
        network_redundancy:
          description: 关键DDC网络冗余
          method: 双网口或环网
          applicable: 控制关键设备的DDC
        
        local_power_backup:
          description: DDC本地电源后备
          method: 24V DC + 蓄电池
          duration: 4小时
          note: 确保断电后仍能发送报警

    # === 原有alarm_management增强 ===
    alarm_management:
      # ... 原有内容保留 ...
    
      # 新增与其他系统的集成
      cross_system_integration:
        int_nur_interface:
          protocol: API (REST)
          data_exchange:
            receive: 护士呼叫状态、紧急呼叫事件
            send: 设备状态（如病房空调）
          priority_handling: INT-NUR优先于INT-BA显示
        
        int_sec_interface:
          protocol: API (REST)
          data_exchange:
            receive: 入侵报警、门禁异常
            send: 区域设备联动状态
          linkage: 入侵报警→区域照明开启
        
        fire_fas_interface:
          protocol: 硬接点 + 网络
          data_exchange:
            receive: 火灾报警、消防联动信号
            send: 设备状态
          linkage: 火灾→关闭空调，开启排烟
          priority: 最高优先级
```

---

## 系统 3.5: INT-NUR 护士呼叫系统（P2修订补充）

```yaml
  # ========================================
  # CONTROL LOGIC SECTION - 补充优先级协调
  # ========================================
  control_logic:

    # === 原有控制逻辑保留 ===
    call_priority:
      # ... 原有内容 ...
  
    response_management:
      # ... 原有内容 ...
  
    nurse_presence:
      # ... 原有内容 ...
  
    # === P2修复：与BA系统的协调 ===
    ba_system_coordination:
      name: 与楼宇自控系统协调
      description: 处理INT-NUR与INT-BA的显示冲突
    
      display_priority:
        description: 显示优先级声明
        principle: |
          护士呼叫系统的紧急呼叫属于生命安全级别
          其优先级高于楼宇自控系统的设备告警
        
        priority_claim:
          int_nur_emergency: Level_0 (生命安全)
          int_nur_normal: Level_1 (关键)
          int_ba_critical: Level_1 (关键)
          int_ba_warning: Level_2 (警告)
        
      conflict_handling:
        scenario_1:
          description: 紧急呼叫期间设备告警
          handling: |
            1. INT-NUR紧急呼叫占据主显示区
            2. INT-BA设备告警显示在次要区域
            3. 两者声音同时播放（可区分音调）
          implementation:
            - INT-NUR通知INT-BA"紧急模式"
            - INT-BA收到后缩小显示区域
            - 紧急呼叫结束后释放显示资源
          
        scenario_2:
          description: 护士正在处理BA告警时发生呼叫
          handling: |
            1. BA告警界面自动最小化
            2. 护士呼叫界面弹出
            3. BA告警保持在后台
            4. 呼叫处理完成后可恢复BA界面
          implementation:
            - 屏幕分区管理
            - 窗口优先级控制
          
      shared_display_rules:
        护士站大屏:
          primary: INT-NUR呼叫状态
          secondary: INT-BA设备状态（简化）
          layout: 左侧70%呼叫，右侧30%设备
        
        护士站工作站:
          primary: 当前操作系统
          popup: 高优先级报警弹窗
          rule: 紧急呼叫必须弹窗
        
      data_sharing:
        int_nur_to_ba:
          - 呼叫状态（正常/忙碌/紧急）
          - 护士值班状态
        int_ba_to_nur:
          - 病房温湿度
          - 设备运行状态
        
      integration_api:
        endpoint: "/api/v1/alarm/priority"
        methods:
          - POST /claim_priority: 声明优先级
          - GET /current_priority: 查询当前优先级
          - POST /release_priority: 释放优先级
```

---

## 系统 3.6: INT-SEC 安防系统（P3/P6修订补充）

```yaml
  # ========================================
  # CONTROL LOGIC SECTION - 补充消防联动和隐私保护
  # ========================================
  control_logic:

    # === 原有控制逻辑保留 ===
    access_control_rules:
      # ... 原有内容 ...
  
    video_intelligent:
      # ... 原有内容 ...
  
    # === P3修复：消防联动优化 ===
    fire_linkage_enhanced:
      name: 消防联动增强控制
      description: 确保火灾时疏散通道畅通无阻
    
      problem_addressed:
        issue: 防潜回功能在火灾时可能阻碍疏散
        scenario: |
          员工刷卡进入后未刷卡离开（防潜回锁定）
          火灾发生时，可能被困
        
      improved_logic:
        phase_0_normal:
          description: 正常状态
          anti_passback: 启用
          access_control: 正常运行
        
        phase_1_fire_detection:
          trigger: 收到FIRE-FAS火灾信号
          time: 0秒
          actions:
            - 立即取消所有防潜回限制
            - 所有读卡器进入"自由通行"模式
            - 记录"火灾联动启动"事件
          verification: 防潜回状态检查
          
        phase_2_forced_unlock:
          trigger: 火灾信号持续30秒
          actions:
            - 如任何读卡器仍在等待刷卡，强制开门
            - 不等待刷卡完成
            - 发送"强制开门"通知
          purpose: 防止刷卡过程中被困
        
        phase_3_power_cut:
          trigger: 火灾信号持续60秒
          actions:
            - 疏散通道所有门锁断电开门
            - 保留特殊区域门禁（见例外清单）
            - 记录所有门锁状态
          purpose: 保证通道完全畅通
        
        phase_4_recovery:
          trigger: FIRE-FAS复位信号
          delay: 确认复位信号稳定30秒
          actions:
            - 逐步恢复门禁控制
            - 恢复防潜回功能
            - 生成火灾联动报告
    
      exception_list:
        maintained_during_fire:
          - 药库（单向可出）
          - 毒麻药品柜（锁定）
          - 财务金库（锁定）
          - 放射源库（锁定）
        logic: |
          这些区域的门锁不受火灾联动影响
          但出口方向可自由通行（单向）
        
      hardware_requirements:
        fire_signal_connection:
          method: 干接点硬连接
          path: FIRE-FAS → 门禁控制器
          bypass_network: true
          note: 不依赖网络，确保可靠性
        
        fail_safe_lock:
          type: 断电开门型电锁
          applicable: 所有疏散通道门
          verification: 每月断电测试
        
        ups_backup:
          purpose: 确保火灾时门禁控制器有电
          duration: 4小时
          function: 执行联动逻辑，记录事件
        
      testing_requirements:
        monthly_test:
          - 模拟火灾信号
          - 验证防潜回是否禁用
          - 验证30秒后强制开门
          - 验证60秒后断电开门
          - 验证例外区域锁定
        
        documentation:
          - 测试时间
          - 测试结果
          - 异常情况
          - 整改措施

    # === P6修复：隐私保护要求 ===
    privacy_protection:
      name: 隐私保护与合规
      description: 人脸识别和视频监控的隐私保护措施
    
      regulatory_compliance:
        applicable_regulations:
          - 《中华人民共和国个人信息保护法》
          - 《医疗卫生机构医学伦理审查办法》
          - GB/T 35273-2020 个人信息安全规范
          - 医院内部隐私保护政策
        
      privacy_impact_assessment:
        required: true
        frequency: 每年一次，或系统变更时
        content:
          - 人脸识别必要性评估
          - 替代技术可行性分析
          - 数据保护措施评估
          - 知情同意程序评估
        
      informed_consent:
        patient_notification:
          methods:
            - 门诊挂号时书面告知
            - 住院协议中明确条款
            - 病区内张贴告示
            - 摄像机附近标识
          content: |
            本院使用视频监控和人脸识别技术
            用于安全管理和身份识别
            您的个人信息将受到严格保护
          
        opt_out_option:
          available: true
          procedure: |
            1. 患者可申请不录入人脸
            2. 需接受替代身份识别（IC卡）
            3. 部分高安全区域可能无法进入
          record: 保留书面申请
        
        staff_consent:
          method: 入职协议中包含同意条款
          scope: 明确人脸识别用途和范围
        
      data_protection_measures:
        storage_security:
          encryption: AES-256加密存储
          location: 本地服务器（不上传云端）
          access_control: 仅授权安保人员可访问
        
        retention_policy:
          video_footage:
            general: 30天自动删除
            incident: 保留至事件处理完成
          face_data:
            patient: 出院后30天删除
            staff: 离职后30天删除
            visitor: 离开后7天删除
          
        access_logging:
          requirement: 所有查询记录日志
          content:
            - 查询人
            - 查询时间
            - 查询目标
            - 查询原因
          review: 每月审计异常查询
        
      scope_limitation:
        prohibited_uses:
          - 广告推送
          - 商业营销
          - 医疗隐私关联
          - 行动追踪（无安全理由）
        
        permitted_uses:
          - 出入口安全管理
          - 黑名单人员识别
          - 安全事件调查
          - 紧急情况人员定位
        
      technical_safeguards:
        data_isolation:
          description: 人脸系统与HIS物理隔离
          implementation: 独立网络和服务器
          purpose: 防止人脸与医疗信息关联
        
        minimal_data:
          description: 使用模板而非照片
          implementation: 仅存储人脸特征值
          purpose: 降低泄露风险
        
        anonymization:
          description: 视频存储匿名化处理
          implementation: 非必要区域人脸模糊
          applicable: 一般公共区域
        
      area_specific_policies:
        patient_areas:
          method: 门禁卡+RFID优先
          face_recognition: 仅出入口，不追踪
          rationale: 患者隐私优先
        
        staff_areas:
          method: 可用人脸识别
          requirement: 知情同意
          logging: 完整访问日志
        
        high_security_areas:
          method: 多因素认证（卡+人脸）
          face_recognition: 1:1验证（非识别）
          rationale: 安全性优先
        
      incident_response:
        data_breach:
          procedure:
            - 立即隔离受影响系统
            - 评估泄露范围
            - 通知受影响个人
            - 报告监管机构
            - 采取补救措施
          timeline: 72小时内报告
        
      audit_requirements:
        internal_audit:
          frequency: 每季度
          scope: 访问日志、权限设置、数据保留
        
        external_audit:
          frequency: 每年
          scope: 合规性、安全性、隐私保护
```

---

# 新增：跨系统协调规范

## 系统间接口规范

```yaml
Cross_System_Interface_Specification:

  identity:
    name: 医院机电系统间接口规范
    description: 定义各系统间的数据交换和联动接口
    version: 1.0
    last_updated: 2024

   # ========================================
  # 电力系统与其他系统的接口
  # ========================================
  electrical_interfaces:
  
    elec_to_plumb:
      interface_id: IF-ELEC-PLUMB-001
      name: 电力系统至给排水系统接口
      description: 电力系统向给排水设备供电及状态共享
    
      power_supply:
        from: ELEC-LV-MAIN
        to: 
          - PLUMB-DWS加压泵组
          - PLUMB-HWS热水泵组
          - PLUMB-SAN污水提升泵
        circuit_type: 动力配电
        backup: 应急电源（发电机）
        priority: 一级负荷
      
      signal_exchange:
        elec_to_plumb:
          - signal: POWER_NORMAL
            type: DI
            meaning: 市电正常
          - signal: POWER_FAIL
            type: DI
            meaning: 市电失电
          - signal: GEN_RUNNING
            type: DI
            meaning: 发电机运行
        plumb_to_elec:
          - signal: PUMP_TOTAL_LOAD
            type: AI
            meaning: 泵组总负荷
            unit: kW
          
      failure_handling:
        scenario: 电力中断
        plumb_response:
          - 泵组停止运行
          - 依赖水箱余水重力供水
          - 等待发电机恢复供电
        recovery_sequence:
          - 发电机启动后15秒
          - 给水泵组恢复运行
          - 热水泵组恢复运行
          - 污水泵组恢复运行

    elec_to_mgas:
      interface_id: IF-ELEC-MGAS-001
      name: 电力系统至医用气体系统接口
      description: 电力系统保障医用气体设备供电
    
      power_supply:
        from: ELEC-EPS (UPS)
        to:
          - MGAS监控报警系统
          - MGAS阀门控制器
        circuit_type: 不间断电源
        priority: 生命支持负荷
      
        from: ELEC-LV-MAIN（应急母线）
        to:
          - MGAS-VAC真空泵
          - MGAS-AIR压缩机
        circuit_type: 动力配电
        backup: 发电机15秒内恢复
        priority: 一级负荷
      
      signal_exchange:
        elec_to_mgas:
          - signal: UPS_BATTERY_LOW
            type: DI
            meaning: UPS电池电量低
            action: MGAS系统准备应急
          - signal: POWER_QUALITY
            type: AI
            meaning: 电源质量指数
        mgas_to_elec:
          - signal: MGAS_CRITICAL_ALARM
            type: DI
            meaning: 医用气体危急报警
            action: 优先保障MGAS设备供电

    elec_to_hvac:
      interface_id: IF-ELEC-HVAC-001
      name: 电力系统至暖通系统接口
      description: 电力系统保障暖通设备供电
    
      power_supply:
        main_equipment:
          - 冷水机组（大负荷）
          - 冷冻水泵/冷却水泵
          - 空调箱/新风机组
          - 冷却塔风机
        circuit_type: 动力配电
        priority: 二级负荷
      
      signal_exchange:
        elec_to_hvac:
          - signal: DEMAND_LIMIT
            type: AI
            meaning: 需量限制指令
            action: HVAC降低负荷
          - signal: PEAK_SHAVING
            type: DI
            meaning: 削峰信号
            action: 关闭非关键冷机
        hvac_to_elec:
          - signal: HVAC_TOTAL_LOAD
            type: AI
            meaning: 暖通总负荷
            unit: kW

  # ========================================
  # 给排水系统与其他系统的接口
  # ========================================
  plumbing_interfaces:
  
    plumb_to_hvac:
      interface_id: IF-PLUMB-HVAC-001
      name: 给排水至暖通系统接口
      description: 冷却塔补水和空调冷凝水排放
    
      water_supply:
        from: PLUMB-DWS
        to: HVAC-CHP冷却塔
        type: 补水
        control: 浮球阀自动补水
        monitoring:
          - 补水流量
          - 补水阀状态
        
      drainage:
        from: HVAC空调设备（冷凝水）
        to: PLUMB-SAN
        type: 排水
        note: 空调冷凝水汇入生活排水系统
      
      signal_exchange:
        plumb_to_hvac:
          - signal: MAKEUP_WATER_AVAILABLE
            type: DI
            meaning: 补水可用
          - signal: MAKEUP_WATER_PRESSURE
            type: AI
            meaning: 补水压力
            unit: MPa
        hvac_to_plumb:
          - signal: COOLING_TOWER_LEVEL
            type: AI
            meaning: 冷却塔液位
            unit: "%"

    plumb_to_mgas:
      interface_id: IF-PLUMB-MGAS-001
      name: 给排水至医用气体系统接口
      description: 压缩空气冷却水供应
    
      water_supply:
        from: PLUMB-DWS（经冷却塔）
        to: MGAS-AIR压缩机冷却器
        type: 冷却水
      
      signal_exchange:
        plumb_to_mgas:
          - signal: COOLING_WATER_AVAILABLE
            type: DI
            meaning: 冷却水可用
          - signal: COOLING_WATER_FLOW
            type: AI
            meaning: 冷却水流量
            unit: "m³/h"
          - signal: DWS_COOLING_WATER_ALERT
            type: DI
            meaning: 冷却水供应预警
            action: MGAS-AIR进入保护模式
        mgas_to_plumb:
          - signal: AIR_COOLING_DEMAND
            type: AI
            meaning: 压缩机冷却需求
            action: 优先保障冷却水

  # ========================================
  # 智能化系统间的接口
  # ========================================
  intelligent_interfaces:
  
    ba_to_nur:
      interface_id: IF-BA-NUR-001
      name: 楼宇自控至护士呼叫接口
      description: BA与护士呼叫系统的协调
    
      integration_method:
        protocol: REST API
        endpoint: "/api/v1/integration"
        authentication: Token-based
      
      data_exchange:
        ba_to_nur:
          - data: 病房环境参数
            content: 温度、湿度
            purpose: 护士站显示
            frequency: 每分钟
          - data: 设备故障告警
            content: 空调/照明故障
            purpose: 护士知晓
            priority: Level_2
        nur_to_ba:
          - data: 护理区域状态
            content: 忙碌/空闲
            purpose: 优化空调控制
          - data: 紧急呼叫状态
            content: 正在进行紧急呼叫
            purpose: 抢占显示优先级
          
      priority_coordination:
        rule: INT-NUR紧急呼叫 > INT-BA设备告警
        implementation:
          - NUR发送priority_claim请求
          - BA缩小告警显示区域
          - NUR发送priority_release释放
          - BA恢复正常显示

    ba_to_sec:
      interface_id: IF-BA-SEC-001
      name: 楼宇自控至安防系统接口
      description: BA与安防系统的联动
    
      integration_method:
        protocol: REST API / OPC UA
      
      data_exchange:
        ba_to_sec:
          - data: 区域设备状态
            content: 照明开关状态
          - data: 人员检测
            content: 房间占用状态（如有）
        sec_to_ba:
          - data: 入侵报警
            content: 报警区域
            action: BA开启区域照明
          - data: 门禁状态
            content: 开关门状态
          
      linkage_rules:
        intrusion_lighting:
          trigger: INT-SEC入侵报警
          action: INT-BA开启报警区域全部照明
          duration: 持续30分钟或手动取消
        
        after_hours_lighting:
          trigger: INT-SEC门禁刷卡（非工作时间）
          action: INT-BA开启该区域照明
          duration: 15分钟后自动关闭

    ba_to_fire:
      interface_id: IF-BA-FIRE-001
      name: 楼宇自控至消防系统接口
      description: 火灾联动控制
    
      integration_method:
        primary: 硬接点（干触点）
        secondary: 网络通讯
        note: 硬接点确保可靠性
      
      signal_exchange:
        fire_to_ba:
          hardwired:
            - signal: FIRE_ALARM
              type: DI
              meaning: 火灾报警（总信号）
              wiring: FIRE-FAS干接点→DDC
            - signal: FIRE_FLOOR_ZONE
              type: DI（多点）
              meaning: 分层/分区火灾信号
          network:
            - signal: FIRE_DETAIL
              content: 详细火警信息
              purpose: 显示和记录
            
      linkage_actions:
        fire_alarm_received:
          actions:
            - 关闭空调系统送回风机
            - 关闭新风/排风阀门
            - 开启排烟风机（如受BA控制）
            - 电梯迫降至首层
            - 开启疏散通道照明
            - 记录联动事件
          verification: 每月测试

    sec_to_fire:
      interface_id: IF-SEC-FIRE-001
      name: 安防系统至消防系统接口
      description: 消防联动下的门禁控制
    
      integration_method:
        primary: 硬接点（干触点）
        note: 必须使用硬接点，确保可靠性
      
      signal_exchange:
        fire_to_sec:
          - signal: FIRE_EVACUATION
            type: DI
            meaning: 火灾疏散信号
            wiring: FIRE-FAS干接点→门禁控制器
          
      linkage_actions:
        fire_evacuation:
          phase_1: # 0秒
            action: 取消防潜回，进入自由通行模式
          phase_2: # 30秒
            action: 强制开启刷卡中的门
          phase_3: # 60秒
            action: 疏散通道门锁断电开门
          exception: 药库/财务等特殊区域保持锁定
          recovery: 消防复位后逐步恢复

  # ========================================
  # 医用气体系统与其他系统的接口
  # ========================================
  medical_gas_interfaces:
  
    mgas_to_ba:
      interface_id: IF-MGAS-BA-001
      name: 医用气体至楼宇自控接口
      description: 医用气体监控集成到BA
    
      integration_method:
        protocol: Modbus TCP / RS485
      
      data_exchange:
        mgas_to_ba:
          - data: 气体压力
            systems: [O2, VAC, AIR, N2O]
            purpose: 集中监控
          - data: 气源状态
            content: 液氧液位、汇流排状态
          - data: 报警信息
            priority: 根据严重程度
          
      alarm_handling:
        mgas_critical:
          meaning: 医用气体危急（如O2中断）
          priority: Level_0
          ba_action: 最高优先级显示
        mgas_warning:
          meaning: 医用气体预警
          priority: Level_2
          ba_action: 正常报警处理

    mgas_to_nur:
      interface_id: IF-MGAS-NUR-001
      name: 医用气体至护士呼叫接口
      description: 护士站气体报警显示
    
      integration_method:
        protocol: 硬接点 / 网络
      
      signal_exchange:
        mgas_to_nur:
          - signal: ZONE_GAS_ALARM
            type: DI
            meaning: 本区域气体报警
            display: 护士站报警屏
          
      display_rules:
        location: 护士站气体报警显示面板
        content:
          - 气体类型
          - 报警类型（压力高/低/故障）
          - 报警区域
        priority: 高于普通设备告警

  # ========================================
  # 接口测试与验证要求
  # ========================================
  interface_testing:
  
    commissioning_tests:
      description: 调试阶段接口测试
      scope:
        - 所有硬接点联动
        - 网络通讯连通性
        - 数据交换正确性
        - 联动动作执行
      documentation: 测试报告
    
    periodic_tests:
      fire_linkage:
        frequency: 每月
        scope: BA关闭空调、SEC门禁释放
        method: 模拟火灾信号（与消防配合）
      
      gas_alarm:
        frequency: 每季度
        scope: 气体报警至BA/NUR显示
        method: 模拟低压报警
      
      power_transfer:
        frequency: 每月
        scope: 发电机切换后各系统恢复
        method: 模拟市电失电
      
    documentation:
      test_records: 保留2年
      issue_tracking: 问题整改记录
      configuration_management: 接口配置变更记录
```

---

## 关键依赖关系表

```yaml
Critical_Dependency_Matrix:

  identity:
    name: 医院机电系统关键依赖关系表
    description: 列出系统间的关键依赖，用于故障影响分析和应急规划
    version: 1.0

  # ========================================
  # 依赖关系矩阵
  # ========================================
  dependencies:

    # === 电力系统依赖 ===
    - dep_id: DEP-001
      source_system: ELEC-LV-MAIN
      target_system: PLUMB-DWS
      dependency_type: 电力供应
      criticality: HIGH
      failure_tolerance: 30分钟
      failure_impact: 加压泵停止，依赖水箱余水
      backup_measure: 发电机15秒内恢复
      recovery_priority: 2
    
    - dep_id: DEP-002
      source_system: ELEC-EPS
      target_system: MGAS-O2（监控）
      dependency_type: 不间断电源
      criticality: CRITICAL
      failure_tolerance: 0
      failure_impact: 失去监控和报警能力
      backup_measure: UPS后备30分钟
      recovery_priority: 1
    
    - dep_id: DEP-003
      source_system: ELEC-LV-MAIN
      target_system: MGAS-VAC
      dependency_type: 电力供应
      criticality: HIGH
      failure_tolerance: 10分钟
      failure_impact: 真空泵停止，真空度下降
      backup_measure: 发电机15秒内恢复
      recovery_priority: 1
    
    - dep_id: DEP-004
      source_system: ELEC-LV-MAIN
      target_system: MGAS-AIR
      dependency_type: 电力供应
      criticality: HIGH
      failure_tolerance: 15分钟
      failure_impact: 压缩机停止，储气罐供气
      backup_measure: 发电机15秒内恢复
      recovery_priority: 1
    
    - dep_id: DEP-005
      source_system: ELEC-LV-MAIN
      target_system: HVAC-CHP
      dependency_type: 电力供应
      criticality: MEDIUM
      failure_tolerance: 2小时
      failure_impact: 空调停止，温度逐渐变化
      backup_measure: 部分设备发电机供电
      recovery_priority: 3
    
    - dep_id: DEP-006
      source_system: ELEC-EPS
      target_system: INT-BA
      dependency_type: 不间断电源
      criticality: HIGH
      failure_tolerance: 5分钟
      failure_impact: 失去集中监控能力
      backup_measure: DDC独立运行
      recovery_priority: 2
    
    - dep_id: DEP-007
      source_system: ELEC-EPS
      target_system: INT-NUR
      dependency_type: 不间断电源
      criticality: CRITICAL
      failure_tolerance: 0
      failure_impact: 护士呼叫失效
      backup_measure: UPS后备4小时，楼层主机独立运行
      recovery_priority: 1
    
    - dep_id: DEP-008
      source_system: ELEC-EPS
      target_system: INT-SEC
      dependency_type: 不间断电源
      criticality: HIGH
      failure_tolerance: 4小时
      failure_impact: 门禁/视频失效
      backup_measure: 控制器本地电池后备
      recovery_priority: 2

    # === 给排水系统依赖 ===
    - dep_id: DEP-011
      source_system: PLUMB-DWS
      target_system: PLUMB-HWS
      dependency_type: 冷水供应
      criticality: HIGH
      failure_tolerance: 1小时
      failure_impact: 热水系统无冷水源
      backup_measure: 热水储罐可供1小时
      recovery_priority: 2
    
    - dep_id: DEP-012
      source_system: PLUMB-DWS
      target_system: HVAC-CHP
      dependency_type: 冷却塔补水
      criticality: MEDIUM
      failure_tolerance: 2小时
      failure_impact: 冷却塔液位下降
      backup_measure: 冷却塔储水可用2小时
      recovery_priority: 3
    
    - dep_id: DEP-013
      source_system: PLUMB-DWS
      target_system: MGAS-AIR
      dependency_type: 冷却水
      criticality: HIGH
      failure_tolerance: 4小时
      failure_impact: 压缩空气温度升高
      backup_measure: 应急补水接口
      recovery_priority: 2

    # === 暖通系统依赖 ===
    - dep_id: DEP-021
      source_system: HVAC-CHP
      target_system: PLUMB-HWS
      dependency_type: 热源（热水/蒸汽）
      criticality: MEDIUM
      failure_tolerance: 4小时
      failure_impact: 热水温度下降
      backup_measure: 储热罐、备用电加热
      recovery_priority: 3

    # === 网络/IT依赖 ===
    - dep_id: DEP-031
      source_system: IT-NETWORK
      target_system: INT-BA
      dependency_type: 网络通讯
      criticality: MEDIUM
      failure_tolerance: 无限制
      failure_impact: 失去远程监控，DDC独立运行
      backup_measure: DDC本地控制
      recovery_priority: 3
    
    - dep_id: DEP-032
      source_system: IT-NETWORK
      target_system: INT-NUR
      dependency_type: 网络通讯
      criticality: MEDIUM
      failure_tolerance: 无限制
      failure_impact: 楼层内呼叫正常，跨楼层/移动终端失效
      backup_measure: 楼层主机独立运行
      recovery_priority: 2
    
    - dep_id: DEP-033
      source_system: IT-NETWORK
      target_system: INT-SEC
      dependency_type: 网络通讯
      criticality: MEDIUM
      failure_tolerance: 无限制
      failure_impact: 门禁本地运行，视频无法远程查看
      backup_measure: 控制器本地存储和控制
      recovery_priority: 2

  # ========================================
  # 故障场景影响分析
  # ========================================
  failure_scenarios:
  
    scenario_1:
      name: 双路市电全失
      affected_systems:
        immediate:
          - HVAC全部停止
          - 一般照明熄灭
        after_15s:
          - 发电机启动，应急负荷恢复
          - MGAS泵组恢复
          - PLUMB泵组恢复
        battery_backup:
          - INT-BA: UPS 30分钟
          - INT-NUR: UPS 4小时
          - INT-SEC: 本地电池4小时
          - MGAS监控: UPS 30分钟
      critical_path: 发电机必须在15秒内启动
      escalation: 发电机失败则启动《全院停电应急预案》
    
    scenario_2:
      name: 市政供水中断
      affected_systems:
        immediate: 无
        after_4h:
          - 水箱耗尽
          - 加压泵停止
        after_6h:
          - 热水系统停止
          - 冷却塔补水中断
        after_8h:
          - MGAS-AIR冷却不足
      critical_path: 4小时内恢复供水或启用应急水源
      escalation: 启动《供水中断应急预案》
    
    scenario_3:
      name: 火灾
      affected_systems:
        immediate:
          - INT-SEC门禁释放
          - INT-BA关闭空调
          - 排烟系统启动
          - 疏散照明开启
        coordination: FIRE-FAS主导联动
      critical_path: 疏散通道畅通
    
    scenario_4:
      name: 网络全面故障
      affected_systems:
        immediate:
          - INT-BA失去集中监控（DDC独立运行）
          - INT-NUR跨楼层失效（楼层内正常）
          - INT-SEC失去远程监控（本地控制正常）
        not_affected:
          - MGAS（独立报警系统）
          - ELEC（独立保护系统）
          - HVAC（DDC本地控制）
      critical_path: 无生命安全风险
      escalation: IT部门网络恢复

  # ========================================
  # 恢复优先级
  # ========================================
  recovery_priorities:
  
    priority_1:
      name: 生命安全
      systems:
        - MGAS-O2（医用氧气）
        - MGAS-VAC（医用负压）
        - INT-NUR（护士呼叫）
        - ELEC-EPS（应急电源）
      max_downtime: 0-15秒
    
    priority_2:
      name: 关键医疗支持
      systems:
        - MGAS-AIR（医用压缩空气）
        - PLUMB-DWS（生活给水）
        - INT-BA（楼宇自控）
        - INT-SEC（安防系统）
      max_downtime: 15秒-30分钟
    
    priority_3:
      name: 舒适性支持
      systems:
        - HVAC-CHP（冷热源）
        - PLUMB-HWS（热水）
        - 一般照明
      max_downtime: 2-4小时
    
    priority_4:
      name: 非关键系统
      systems:
        - 绿化灌溉
        - 景观照明
      max_downtime: 无限制
```

---

## 跨系统协调矩阵

```yaml
Cross_System_Coordination_Matrix:

  identity:
    name: 医院机电系统协调矩阵
    description: 定义系统间在各场景下的协调行为
    version: 1.0

  # ========================================
  # 正常运行协调
  # ========================================
  normal_operation:
  
    energy_optimization:
      coordinator: INT-BA
      participants: [HVAC-CHP, ELEC-LV-MAIN, PLUMB-DWS]
      coordination:
        - BA根据负荷预测优化冷机启停
        - BA根据电价信号调整用电策略
        - BA监控各系统能耗数据
      data_flow:
        - ELEC→BA: 实时电力数据
        - HVAC→BA: 冷热源运行数据
        - PLUMB→BA: 水泵运行数据
        - BA→各系统: 优化控制指令
      
    comfort_control:
      coordinator: INT-BA
      participants: [HVAC-AHU, HVAC-FCU, PLUMB-HWS]
      coordination:
        - BA根据人员检测调整空调
        - BA根据时间程序控制温度
        - BA监控室内环境参数
      
    security_integration:
      coordinator: INT-SEC
      participants: [INT-BA, INT-NUR]
      coordination:
        - SEC检测异常→BA开启照明
        - SEC门禁状态→NUR显示（访客管理）

  # ========================================
  # 应急场景协调
  # ========================================
  emergency_scenarios:
  
    fire_emergency:
      trigger: FIRE-FAS火灾报警
      coordinator: FIRE-FAS
    
      coordination_matrix:
        - target: INT-BA
          action: 关闭空调，开启排烟，开启疏散照明
          signal_type: 硬接点
          response_time: 立即
        
        - target: INT-SEC
          action: 取消防潜回，开启疏散通道
          signal_type: 硬接点
          response_time: 立即
        
        - target: INT-NUR
          action: 显示火灾报警
          signal_type: 网络
          response_time: 1秒
        
        - target: ELEC-LV
          action: 电梯迫降
          signal_type: 硬接点
          response_time: 立即
        
        - target: MGAS
          action: 无直接联动（气体系统独立）
          note: 消防人员手动关闭气源（如需要）
        
    power_failure:
      trigger: ELEC-LV-MAIN双路市电失电
      coordinator: ELEC-EPS
    
      coordination_matrix:
        - target: ELEC-EPS
          action: 发电机自动启动
          response_time: 15秒
        
        - target: INT-BA
          action: 报警显示，DDC切换至失网模式（如需要）
          response_time: 即时
        
        - target: MGAS-VAC/AIR
          action: 泵组停止，等待发电机恢复
          response_time: 15秒后恢复
        
        - target: PLUMB-DWS
          action: 泵组停止，水箱供水
          response_time: 15秒后泵组恢复
        
        - target: INT-NUR
          action: UPS后备供电
          response_time: 无中断
        
    water_failure:
      trigger: PLUMB-DWS双路市政断水
      coordinator: INT-BA
    
      coordination_matrix:
        - target: PLUMB-DWS
          action: 依赖水箱存水
          duration: 约4小时
        
        - target: PLUMB-HWS
          action: 减少热水供应
          response_time: 液位<50%时
        
        - target: HVAC-CHP
          action: 冷却塔进入节水模式
          response_time: 液位<30%时
        
        - target: MGAS-AIR
          action: 监控冷却水状态
          response_time: 收到预警信号时
        
    gas_emergency:
      trigger: MGAS-O2系统压力危急
      coordinator: MGAS报警系统
    
      coordination_matrix:
        - target: INT-BA
          action: 最高优先级显示
          response_time: 1秒
        
        - target: INT-NUR
          action: 护士站报警显示
          response_time: 1秒
        
        - target: 临床科室
          action: 床旁氧气瓶备用
          response_time: 人工响应

  # ========================================
  # 告警优先级总表
  # ========================================
  alarm_priority_summary:
  
    level_0_life_safety:
      description: 生命安全级（最高）
      alarms:
        - FIRE-FAS: 火灾报警
        - INT-NUR: 紧急呼叫（红色）
        - MGAS-O2: 氧气中断
        - ELEC-EPS: 全部电源故障
      display: 全屏，持续闪烁
      audio: 最高音量，不可静音
      override: 不可被覆盖
    
    level_1_critical:
      description: 关键级
      alarms:
        - INT-NUR: 普通呼叫（黄色）
        - INT-SEC: 入侵报警
        - INT-BA: 关键设备故障
        - MGAS: 气体低压预警
        - ELEC: 市电单路故障
      display: 主显示区
      audio: 报警音，可静音60秒
      override: 可被Level_0覆盖
    
    level_2_warning:
      description: 警告级
      alarms:
        - INT-BA: 设备参数异常
        - INT-SEC: 门禁异常
        - PLUMB: 水压/水质预警
        - HVAC: 空调参数异常
      display: 次要区域
      audio: 提示音，可静音
      override: 可被Level_0/1覆盖
    
    level_3_info:
      description: 信息级
      alarms:
        - INT-BA: 维护提醒
        - INT-NUR: 护理确认
        - 一般事件记录
      display: 状态栏
      audio: 无
      override: 可被任何更高级别覆盖

  # ========================================
  # 通信故障处理
  # ========================================
  communication_failure:
  
    network_failure:
      description: 网络通讯中断
      affected: 所有网络依赖的系统间通讯
    
      system_behavior:
        INT-BA:
          action: DDC切换至独立运行模式
          capability: 本地控制正常，失去优化和集中监控
        
        INT-NUR:
          action: 楼层主机独立运行
          capability: 楼层内呼叫正常，跨楼层/移动终端失效
        
        INT-SEC:
          action: 控制器本地运行
          capability: 门禁正常，视频本地存储，无法远程查看
        
      critical_linkage_protection:
        fire_linkage: 硬接点不受影响
        gas_alarm: 独立报警系统不受影响
        power_alarm: 独立保护不受影响
      
    hardwired_signal_failure:
      description: 硬接点信号故障
      detection: DDC检测信号异常
      action: 报警，人工检查
      criticality: 高（可能影响安全联动）
```

# 

