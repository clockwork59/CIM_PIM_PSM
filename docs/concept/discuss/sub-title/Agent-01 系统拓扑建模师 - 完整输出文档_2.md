## 🧑‍💻 User


继续输出第三批次

---
## 🤖 Assistant


# Agent-01 系统拓扑建模师 - 完整输出文档

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

**下一批次预告：** Batch 4 将输出消防系统（FIRE-FAS、FIRE-SPS）和医疗专业系统（MED-OR手术室环境、MED-LAB检验科专用系统等）。

请确认第三批次内容后，我将继续输出第四批次。

---