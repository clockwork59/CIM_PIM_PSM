## 🧑‍💻 User


继续输出第六批次

---
## 🤖 Assistant


# 第六批次：最终系统与综合集成

## 系统 6.1: PLUMB-RW 雨水排水系统

```yaml
System_Topology:

  identity:
    system_id: PLUMB-RW
    system_name: 雨水排水系统
    system_name_en: Rainwater Drainage System
    system_category: PLUMB
    system_type: 给排水-雨水
    priority_level: P3-GENERAL
    
    description: |
      医院建筑雨水排水系统，收集屋面、露台、广场等区域雨水并排放。
      采用重力流排水为主，必要时设置雨水泵站。
      设置雨水收集回用系统，用于绿化灌溉和道路冲洗。
      系统设计满足暴雨重现期要求，防止内涝。
      
    design_basis:
      rainfall:
        design_return_period: {value: 50, unit: "年", note: "重要公共建筑"}
        rainfall_intensity:
          formula: "q = 167A₁(1+C·lgP)/(t+b)ⁿ"
          note: 根据当地暴雨强度公式
        duration: {value: 5, unit: min}
      roof_area:
        total: {value: 15000, unit: "m²", note: "典型大型医院"}
      runoff_coefficient:
        roof: {value: 0.9}
        pavement: {value: 0.85}
        green: {value: 0.15}
        
    design_standards:
      - GB 50015-2019 建筑给水排水设计标准
      - GB 50014-2021 室外排水设计标准
      - GB 50400-2016 建筑与小区雨水控制及利用工程技术规范
      - 海绵城市建设技术指南
    
    version: 1.0
    last_updated: 2024

  boundary:
    inputs:
      - boundary_id: PLUMB-RW_IN_001
        name: 屋面雨水
        from_system: 建筑屋面
        medium: WATER-RAIN
        
      - boundary_id: PLUMB-RW_IN_002
        name: 露台雨水
        from_system: 室外露台/平台
        medium: WATER-RAIN
        
      - boundary_id: PLUMB-RW_IN_003
        name: 场地雨水
        from_system: 室外场地
        medium: WATER-RAIN
        
      - boundary_id: PLUMB-RW_IN_004
        name: 电力供应
        from_system: ELEC-LV
        medium: ELEC-LV
        parameters:
          for: 雨水泵站
          
    outputs:
      - boundary_id: PLUMB-RW_OUT_001
        name: 市政雨水管网
        to_system: 市政雨水
        medium: WATER-RAIN
        
      - boundary_id: PLUMB-RW_OUT_002
        name: 雨水回用
        to_system: 绿化/道路冲洗
        medium: WATER-RECLAIM
        
      - boundary_id: PLUMB-RW_OUT_003
        name: 状态反馈
        to_system: INT-BA
        medium: SIGNAL-BMS

  nodes:
  
    source_nodes:
    
      - node_id: PLUMB-RW_SRC_ROOF
        node_name: 屋面雨水收集
        node_name_en: Roof Rainwater Collection
        node_type: Source_Node
        node_category: SRC
        
        function: 收集屋面雨水
        medium_in: RAIN
        medium_out: WATER-RAIN
        
        is_boundary_input: true
        
        equipment_parameters:
          roof_types:
            flat_roof:
              name: 平屋面
              slope: {value: "1-3", unit: "%"}
              drainage: 有组织排水
            sloped_roof:
              name: 坡屋面
              slope: {value: ">10", unit: "%"}
              drainage: 檐沟收集
            green_roof:
              name: 绿化屋面
              drainage: 蓄排水板+溢流
              retention: {value: 50, unit: "mm"}
              
          collection_components:
            roof_drain:
              name: 雨水斗
              type:
                gravity: 重力式雨水斗
                siphon: 虹吸式雨水斗
              material: 铸铁/不锈钢
              size: DN75-DN150
              strainer: 防叶片格栅
            gutter:
              name: 天沟/檐沟
              material: 镀锌钢板/不锈钢
              size: 根据汇水面积
              slope: {value: ">0.5", unit: "%"}
            overflow:
              name: 溢流口
              purpose: 超设计暴雨时溢流
              size: 不小于雨水斗
              
        design_calculation:
          flow_rate:
            formula: "Q = ψ × q × F / 10000"
            parameters:
              ψ: 径流系数
              q: 暴雨强度 (L/s·ha)
              F: 汇水面积 (m²)
            
        location_hint:
          space_type: 屋面
          distribution: 按汇水分区布置

      - node_id: PLUMB-RW_SRC_GROUND
        node_name: 场地雨水收集
        node_name_en: Ground Rainwater Collection
        node_type: Source_Node
        node_category: SRC
        
        function: 收集场地雨水
        medium_in: RAIN
        medium_out: WATER-RAIN
        
        is_boundary_input: true
        
        equipment_parameters:
          collection_facilities:
            catch_basin:
              name: 雨水口
              type: 平箅式/立箅式
              grate: 铸铁/球墨铸铁
              size: 400×600mm
              capacity: {value: 20, unit: "L/s"}
              spacing: {value: "25-50", unit: m}
            trench_drain:
              name: 线性排水沟
              material: 树脂混凝土
              width: {value: 150, unit: mm}
              grate: 不锈钢格栅
              application: 广场、入口
            permeable_pavement:
              name: 透水铺装
              type: 透水砖/透水混凝土
              infiltration: {value: ">1", unit: "mm/min"}
              application: 停车场、人行道
              
          sponge_city_facilities:
            rain_garden:
              name: 雨水花园
              purpose: 滞留、净化
              depth: {value: 150, unit: mm}
            bioswale:
              name: 植草沟
              purpose: 传输、净化
              slope: {value: "1-4", unit: "%"}
            detention_pond:
              name: 滞留塘
              purpose: 调蓄峰值流量
              volume: 根据设计计算
              
        location_hint:
          space_type: 室外场地
          areas: 停车场、广场、道路

    distribution_nodes:
    
      - node_id: PLUMB-RW_DST_GRAVITY_SYSTEM
        node_name: 重力流排水系统
        node_name_en: Gravity Drainage System
        node_type: Distribution_Node
        node_subtype: PIP
        node_category: DST
        
        function: 重力排放屋面雨水
        medium_in: WATER-RAIN
        medium_out: WATER-RAIN
        
        equipment_parameters:
          system_type: 重力流内排水
          
          components:
            vertical_stack:
              name: 雨水立管
              material: HDPE/铸铁
              size: {value: "DN100-DN150", unit: mm}
              location: 建筑内管井
              quantity: 按汇水分区
            horizontal_pipe:
              name: 雨水横管
              material: HDPE/铸铁
              size: {value: "DN150-DN300", unit: mm}
              location: 地下室顶板下/室外埋地
              slope: {value: ">1", unit: "%"}
            check_valve:
              name: 逆止阀
              location: 出户管
              purpose: 防止市政倒灌
              
          design_parameters:
            max_flow_velocity: {value: 3, unit: "m/s"}
            min_slope: {value: 1, unit: "%"}
            fullness: {value: "<0.8"}
            
        location_hint:
          space_type: 建筑内/地下

      - node_id: PLUMB-RW_DST_SIPHON_SYSTEM
        node_name: 虹吸式排水系统
        node_name_en: Siphonic Drainage System
        node_type: Distribution_Node
        node_subtype: PIP
        node_category: DST
        
        function: 虹吸原理快速排水
        medium_in: WATER-RAIN
        medium_out: WATER-RAIN
        
        equipment_parameters:
          system_type: 虹吸式屋面雨水排水
          
          principle: |
            利用虹吸原理，管道满流运行，
            排水能力大，管径小，不需要坡度。
            
          components:
            siphon_drain:
              name: 虹吸雨水斗
              type: 气水分离型
              material: HDPE/不锈钢
              features:
                - 防涡流
                - 气水分离
                - 自清洁
            siphon_pipe:
              name: 虹吸管道
              material: HDPE（热熔连接）
              pressure_rating: PN10
              features:
                - 满流设计
                - 无需坡度
                - 可水平敷设
            transition_point:
              name: 虹吸/重力转换点
              location: 建筑底部
              function: 虹吸转为重力流
              
          advantages:
            - 管径小（比重力流小30-50%）
            - 横管无需坡度
            - 排水能力大
            - 适合大跨度屋面
            
          design_parameters:
            design_depth: {value: 55, unit: mm, note: "斗前水深"}
            max_negative_pressure: {value: -80, unit: kPa}
            flow_velocity: {value: "3-10", unit: "m/s"}
            
        applicable: 大型裙房屋面、门诊大厅屋面
        
        location_hint:
          space_type: 大跨度屋面

      - node_id: PLUMB-RW_DST_PUMP_STATION
        node_name: 雨水提升泵站
        node_name_en: Rainwater Pump Station
        node_type: Distribution_Node
        node_subtype: PMP
        node_category: DST
        
        function: 提升低洼区域雨水
        medium_in: WATER-RAIN
        medium_out: WATER-RAIN
        
        multiplicity: optional
        condition: 当雨水无法重力排放时设置
        
        equipment_parameters:
          application:
            - 地下室车道入口
            - 下沉广场
            - 低于市政管网标高区域
            
          components:
            sump:
              name: 集水池
              material: 钢筋混凝土
              volume: 根据来水量计算
              depth: {value: ">1.5", unit: m}
            pump:
              name: 潜水排污泵
              type: 潜水轴流泵/混流泵
              quantity: {value: "≥2", unit: "台", note: "1用1备"}
              material: 铸铁/不锈钢
              capacity: 根据汇水面积
            level_control:
              name: 液位控制
              type: 浮球开关/超声波液位计
              levels:
                start: 高液位
                stop: 低液位
                alarm: 超高液位
            check_valve:
              name: 止回阀
              location: 泵出口
            gate_valve:
              name: 闸阀
              location: 泵进出口
              
          control_logic:
            normal:
              - 水位达到启动液位→启动1台泵
              - 水位继续上升→启动2台泵
              - 水位下降至停止液位→停泵
            alarm:
              - 超高液位报警
              - 泵故障报警
            alternation:
              - 双泵交替运行
              - 故障自动切换
              
        control_points:
          sensors:
            - point_id: RW_SUMP_LEVEL
              point_name: 集水池液位
              point_type: AI
              unit: m
          status:
            - point_id: RW_PUMP_RUN
              point_name: 雨水泵运行
              point_type: DI
          alarms:
            - point_id: RW_HIGH_LEVEL
              alarm_name: 液位超高
              severity: HIGH
        
        location_hint:
          space_type: 地下室/室外
          position: 汇水最低点

      - node_id: PLUMB-RW_DST_RECLAIM
        node_name: 雨水收集回用系统
        node_name_en: Rainwater Harvesting System
        node_type: Distribution_Node
        node_subtype: TRT
        node_category: DST
        
        function: 雨水收集处理回用
        medium_in: WATER-RAIN
        medium_out: WATER-RECLAIM
        
        multiplicity: optional
        condition: 节水要求或海绵城市要求
        
        equipment_parameters:
          system_components:
            initial_diversion:
              name: 初期雨水弃流装置
              function: 弃除初期污染雨水
              volume: {value: "2-5", unit: "mm降雨"}
              method: 容积式/流量式
            storage_tank:
              name: 雨水蓄水池
              material: 钢筋混凝土/PP模块
              volume:
                calculation: 根据汇水面积和回用量
                typical: {value: "200-500", unit: "m³"}
              location: 地下
            treatment:
              name: 雨水处理设备
              process:
                - 格栅过滤
                - 沉淀
                - 过滤（砂滤/膜滤）
                - 消毒（次氯酸钠）
              output_quality: 符合《城市污水再生利用 城市杂用水水质》
            supply_pump:
              name: 雨水供水泵
              type: 变频供水
              pressure: 根据供水点需求
            monitoring:
              parameters:
                - 浊度
                - pH
                - 余氯
                
          reuse_applications:
            greening:
              name: 绿化灌溉
              percentage: {value: 60, unit: "%"}
            road_washing:
              name: 道路冲洗
              percentage: {value: 20, unit: "%"}
            car_wash:
              name: 洗车
              percentage: {value: 10, unit: "%"}
            toilet_flushing:
              name: 冲厕（可选）
              percentage: {value: 10, unit: "%"}
              note: 需要独立中水管道
              
        control_points:
          sensors:
            - point_id: RW_TANK_LEVEL
              point_name: 蓄水池液位
              point_type: AI
              unit: m
            - point_id: RW_TURBIDITY
              point_name: 浊度
              point_type: AI
              unit: NTU
          status:
            - point_id: RW_SUPPLY_PUMP
              point_name: 供水泵运行
              point_type: DI
              
        location_hint:
          space_type: 地下室/室外
          area: 绿化带附近

    sink_nodes:
    
      - node_id: PLUMB-RW_SNK_MUNICIPAL
        node_name: 市政雨水管网
        node_name_en: Municipal Storm Sewer
        node_type: Sink_Node
        node_category: SNK
        
        function: 排入市政雨水系统
        medium_in: WATER-RAIN
        medium_out: WATER-RAIN
        
        is_boundary_output: true
        
        equipment_parameters:
          connection:
            point: 院区雨水出口
            pipe_size: {value: "DN400-DN600", unit: mm}
            check_valve: required
            
          requirements:
            elevation: 高于市政管网
            flow_control: 必要时设置调蓄
            water_quality: 符合排放标准
            
        location_hint:
          space_type: 院区边界
          connection: 市政雨水井

      - node_id: PLUMB-RW_SNK_REUSE
        node_name: 雨水回用点
        node_name_en: Rainwater Reuse Point
        node_type: Sink_Node
        node_category: SNK
        
        function: 雨水回用末端
        medium_in: WATER-RECLAIM
        medium_out: WATER-RECLAIM
        
        is_boundary_output: true
        
        equipment_parameters:
          outlets:
            irrigation_valve:
              name: 绿化灌溉阀门
              type: 电磁阀
              control: 定时/智能灌溉
              location: 绿化带
            wash_tap:
              name: 冲洗龙头
              type: 自闭式水嘴
              marking: "非饮用水"标识
              location: 道路边、停车场
              
        location_hint:
          space_type: 室外绑定化区域

  edges:
  
    collection_edges:
      - edge_id: PLUMB-RW_EDGE_001
        edge_name: 屋面至雨水斗
        edge_type: SURFACE
        from_node: 屋面
        to_node: PLUMB-RW_SRC_ROOF
        direction: unidirectional
        medium: RAIN
        
    drainage_edges:
      - edge_id: PLUMB-RW_EDGE_011
        edge_name: 雨水立管
        edge_type: PIP
        from_node: PLUMB-RW_SRC_ROOF
        to_node: PLUMB-RW_DST_GRAVITY_SYSTEM
        direction: unidirectional
        medium: WATER-RAIN
        
      - edge_id: PLUMB-RW_EDGE_012
        edge_name: 出户雨水管
        edge_type: PIP
        from_node: PLUMB-RW_DST_GRAVITY_SYSTEM
        to_node: PLUMB-RW_SNK_MUNICIPAL
        direction: unidirectional
        medium: WATER-RAIN

  typical_paths:
  
    - path_id: PLUMB-RW_PATH_GRAVITY
      path_name: 重力排水路径
      path_type: DRAIN
      description: 屋面雨水重力排放
      sequence:
        - step: 1
          node: PLUMB-RW_SRC_ROOF
          action: 雨水斗收集屋面雨水
        - step: 2
          node: PLUMB-RW_DST_GRAVITY_SYSTEM
          action: 立管、横管输送
        - step: 3
          node: PLUMB-RW_SNK_MUNICIPAL
          action: 排入市政雨水管

    - path_id: PLUMB-RW_PATH_RECLAIM
      path_name: 雨水回用路径
      path_type: RECLAIM
      description: 雨水收集处理回用
      sequence:
        - step: 1
          node: PLUMB-RW_SRC_ROOF
          action: 收集初期弃流后的雨水
        - step: 2
          node: PLUMB-RW_DST_RECLAIM
          action: 蓄水、处理、消毒
        - step: 3
          node: PLUMB-RW_SNK_REUSE
          action: 供绿化灌溉使用

  control_logic:
  
    pump_station_control:
      name: 雨水泵站控制
      description: 液位控制启停泵
      
      control_sequence:
        start_1:
          trigger: 液位>启动1
          action: 启动1#泵
        start_2:
          trigger: 液位>启动2
          action: 启动2#泵
        stop:
          trigger: 液位<停止
          action: 停止所有泵
        alarm:
          trigger: 液位>报警
          action: 超高液位报警
          
    reclaim_system_control:
      name: 雨水回用控制
      description: 雨水收集和供水控制
      
      control_sequence:
        collection:
          - 初期雨水弃流（前2mm降雨）
          - 弃流后雨水进入蓄水池
          - 池满后溢流至市政
        treatment:
          - 蓄水池液位>处理启动→启动处理设备
          - 清水池满→停止处理
        supply:
          - 用水信号→启动供水泵
          - 变频恒压供水
          - 蓄水池液位低→切换至自来水

  alarm_protection:
  
    drainage_alarms:
      - alarm_id: ALM_RW_OVERFLOW
        alarm_name: 雨水溢流
        severity: MEDIUM
        trigger: 屋面溢流口有水流出
        action: 检查排水系统
        
      - alarm_id: ALM_RW_PUMP_FAIL
        alarm_name: 雨水泵故障
        severity: HIGH
        trigger: 泵运行信号与液位矛盾
        action: 检修泵，启动备用
        
      - alarm_id: ALM_RW_HIGH_LEVEL
        alarm_name: 集水池超高液位
        severity: CRITICAL
        trigger: 液位超限
        action: 紧急排水，防止内涝

  dependencies:
    
    upstream_dependencies:
      - dependency_id: DEP_RW_POWER
        from_system: ELEC-LV
        dependency_type: POWER_SUPPLY
        criticality: MEDIUM
        for: 雨水泵站
        
    downstream_dependencies:
      - dependency_id: DEP_TO_MUNICIPAL
        to_system: 市政雨水
        dependency_type: DRAINAGE
        criticality: MEDIUM
```

---

## 系统 6.2: ELEC-LTG 照明系统

```yaml
System_Topology:

  identity:
    system_id: ELEC-LTG
    system_name: 照明系统
    system_name_en: Lighting System
    system_category: ELEC
    system_type: 电气-照明
    priority_level: P2-BUSINESS_CRITICAL
    
    description: |
      医院照明系统，包括一般照明、应急照明、装饰照明等。
      根据不同医疗功能区域的照明需求进行差异化设计。
      与智能控制系统集成，实现节能和场景控制。
      应急照明系统确保疏散和关键区域的持续照明。
      
    design_basis:
      illuminance_standards:
        operating_room:
          general: {value: 750, unit: lux}
          surgical_field: {value: "20000-160000", unit: lux}
        treatment_room: {value: 500, unit: lux}
        ward: {value: 100, unit: lux}
        corridor: {value: 100, unit: lux}
        lobby: {value: 200, unit: lux}
        office: {value: 300, unit: lux}
      color_temperature:
        operating_room: {value: 4000, unit: K}
        ward: {value: 3000, unit: K}
        public_area: {value: 4000, unit: K}
      color_rendering:
        medical_area: {value: ">90", unit: Ra}
        general_area: {value: ">80", unit: Ra}
        
    design_standards:
      - GB 50034-2013 建筑照明设计标准
      - GB 51039-2014 综合医院建筑设计规范
      - GB 17945-2010 消防应急照明和疏散指示系统
      - GB 50016-2014 建筑设计防火规范
    
    version: 1.0
    last_updated: 2024

  boundary:
    inputs:
      - boundary_id: ELEC-LTG_IN_001
        name: 正常电源
        from_system: ELEC-LV
        medium: ELEC-LV
        parameters:
          voltage: 220V AC
          
      - boundary_id: ELEC-LTG_IN_002
        name: 应急电源
        from_system: ELEC-EPS
        medium: ELEC-LV
        parameters:
          for: 应急照明和疏散指示
          
      - boundary_id: ELEC-LTG_IN_003
        name: 控制信号
        from_system: INT-BA
        medium: SIGNAL-BMS
        
      - boundary_id: ELEC-LTG_IN_004
        name: 火灾信号
        from_system: FIRE-FAS
        medium: SIGNAL-FIRE
        
    outputs:
      - boundary_id: ELEC-LTG_OUT_001
        name: 照明效果
        to_system: 建筑空间
        medium: LIGHT
        
      - boundary_id: ELEC-LTG_OUT_002
        name: 状态反馈
        to_system: INT-BA
        medium: SIGNAL-BMS

  nodes:
  
    source_nodes:
    
      - node_id: ELEC-LTG_SRC_NORMAL
        node_name: 正常照明电源
        node_name_en: Normal Lighting Power
        node_type: Source_Node
        node_category: SRC
        
        function: 为一般照明提供电源
        medium_in: ELEC-LV
        medium_out: ELEC-LV
        
        is_boundary_input: true
        
        equipment_parameters:
          source: 低压配电室照明配电柜
          voltage: 220V AC
          circuit: 照明配电箱
          
        location_hint:
          space_type: 配电室
          distribution: 各楼层照明配电箱

      - node_id: ELEC-LTG_SRC_EMERGENCY
        node_name: 应急照明电源
        node_name_en: Emergency Lighting Power
        node_type: Source_Node
        node_category: SRC
        
        function: 为应急照明提供电源
        medium_in: ELEC-LV
        medium_out: ELEC-LV
        
        is_boundary_input: true
        
        equipment_parameters:
          sources:
            eps:
              name: EPS应急电源
              capacity: 根据应急照明负荷
              duration: {value: "≥90", unit: min}
            battery:
              name: 灯具自带蓄电池
              type: 磷酸铁锂/镍氢
              duration: {value: "≥90", unit: min}
          switching_time: {value: "<5", unit: s}
          
        location_hint:
          space_type: EPS室/各灯具

    distribution_nodes:
    
      - node_id: ELEC-LTG_DST_PANEL
        node_name: 照明配电箱
        node_name_en: Lighting Distribution Panel
        node_type: Distribution_Node
        node_subtype: DST
        node_category: DST
        
        function: 照明电源分配
        medium_in: ELEC-LV
        medium_out: ELEC-LV
        
        multiplicity: multiple
        instance_pattern: ELEC-LTG_DST_PANEL_{Building}_{Floor}_{Zone}
        
        equipment_parameters:
          type: 照明配电箱
          enclosure: IP30（室内）
          
          circuits:
            general_lighting:
              name: 一般照明回路
              voltage: 220V
              breaker: C型MCB
              capacity: {value: "16-32", unit: A}
            emergency_lighting:
              name: 应急照明回路
              voltage: 220V
              source: EPS或双电源
            controlled_lighting:
              name: 受控照明回路
              control: 智能控制模块
              
          smart_features:
            relay_module:
              name: 智能继电器模块
              protocol: KNX/Modbus
              function: 回路开关控制
            dimming_module:
              name: 调光模块
              type: 0-10V/DALI
              function: 亮度调节
              
        control_points:
          status:
            - point_id: LP_MAIN_CB
              point_name: 总开关状态
              point_type: DI
            - point_id: LP_CIRCUIT_STATUS
              point_name: 回路状态
              point_type: DI
          commands:
            - point_id: LP_CIRCUIT_CMD
              point_name: 回路控制
              point_type: DO
        
        location_hint:
          space_type: 电气管井/走廊
          floor: 每层

      - node_id: ELEC-LTG_DST_GENERAL
        node_name: 一般照明灯具
        node_name_en: General Lighting Fixtures
        node_type: Distribution_Node
        node_subtype: LTG
        node_category: DST
        
        function: 一般区域照明
        medium_in: ELEC-LV
        medium_out: LIGHT
        
        multiplicity: multiple
        instance_pattern: 根据区域类型
        
        equipment_parameters:
          fixture_types:
            panel_light:
              name: LED平板灯
              power: {value: "24-48", unit: W}
              size: 600×600mm / 300×1200mm
              application: 办公室、走廊、病房
              features:
                - 无频闪
                - 高显色（Ra>90）
                - 防眩光（UGR<19）
            downlight:
              name: LED筒灯
              power: {value: "7-20", unit: W}
              size: Φ100-Φ200mm
              application: 大厅、走廊
            linear_light:
              name: LED线条灯
              power: {value: "15-40", unit: "W/m"}
              application: 走廊、指示
            pendant_light:
              name: 吊灯
              power: {value: "varies", unit: W}
              application: 大厅、餐厅
              
          lamp_parameters:
            led:
              efficacy: {value: ">100", unit: "lm/W"}
              lifespan: {value: 50000, unit: h}
              color_temp: {value: "3000-6000", unit: K}
              cri: {value: ">80", unit: Ra}
              
          control:
            switch: 传统开关
            dimming: 可调光（0-10V/DALI）
            sensor: 人体感应/光感
            schedule: 定时控制
            
        location_hint:
          space_type: 各功能房间
          mounting: 嵌入式/明装/吊装

      - node_id: ELEC-LTG_DST_MEDICAL
        node_name: 医疗专用照明
        node_name_en: Medical Specialty Lighting
        node_type: Distribution_Node
        node_subtype: LTG
        node_category: DST
        
        function: 医疗专业照明
        medium_in: ELEC-LV
        medium_out: LIGHT
        
        multiplicity: multiple
        
        equipment_parameters:
          fixture_types:
            surgical_light:
              name: 手术无影灯
              type: LED/卤素
              illuminance: {value: "20000-160000", unit: lux}
              color_temp: {value: "3500-5000", unit: K}
              cri: {value: ">95", unit: Ra}
              features:
                - 无影
                - 冷光（低热辐射）
                - 可调焦距
                - 可调色温
              mounting: 吊顶/壁挂
              backup_power: UPS供电
              
            examination_light:
              name: 检查灯
              type: LED
              illuminance: {value: "10000-50000", unit: lux}
              application: 诊室、治疗室
              features:
                - 可移动
                - 聚光/散光可调
                
            reading_light:
              name: 床头阅读灯
              power: {value: "5-10", unit: W}
              color_temp: {value: 3000, unit: K}
              control: 床头开关
              application: 病房
              
            night_light:
              name: 夜间照明灯
              power: {value: "1-3", unit: W}
              illuminance: {value: "5-10", unit: lux}
              application: 病房、走廊
              features:
                - 脚踢线安装
                - 自动亮度调节
                
            observation_light:
              name: 观察灯
              power: {value: "10-20", unit: W}
              color_temp: {value: 4000, unit: K}
              application: ICU、NICU
              features:
                - 可调光
                - 不干扰患者睡眠
                
        location_hint:
          space_type: 医疗功能区

      - node_id: ELEC-LTG_DST_EMERGENCY
        node_name: 应急照明系统
        node_name_en: Emergency Lighting System
        node_type: Distribution_Node
        node_subtype: EMR
        node_category: DST
        
        function: 火灾及停电时照明
        medium_in: ELEC-LV
        medium_out: LIGHT
        
        multiplicity: multiple
        instance_pattern: 全院分布
        
        equipment_parameters:
          system_architecture:
            centralized:
              name: 集中控制型
              description: A型应急照明（消防联动）
              controller: 应急照明控制器
              communication: 二总线
              features:
                - 集中监控
                - 智能疏散
                - 消防联动
            distributed:
              name: 分散型
              description: 自带蓄电池灯具
              battery: 灯具内置
              duration: {value: "≥90", unit: min}
              
          fixture_types:
            emergency_luminaire:
              name: 应急照明灯
              type: LED
              power: {value: "3-10", unit: W}
              illuminance: {value: "≥1", unit: lux}
              mounting: 吊装/壁挂
              spacing: {value: "<20", unit: m}
              location:
                - 走廊
                - 楼梯间
                - 设备房
                - 关键功能房间
                
            exit_sign:
              name: 疏散指示标志
              type: LED
              power: {value: "1-3", unit: W}
              luminance: {value: "≥5", unit: "cd/m²"}
              visibility: {value: "≥20", unit: m}
              types:
                - 安全出口标志
                - 疏散方向标志
                - 楼层标志
              location:
                - 安全出口上方
                - 走廊转弯处
                - 交叉路口
                
            floor_marking:
              name: 地面疏散标志
              type: 蓄光型/电致发光
              location: 走廊地面
              spacing: {value: "<3", unit: m}
              application: 大型公共区域
              
          intelligent_evacuation:
            name: 智能疏散系统
            components:
              main_controller:
                name: 应急照明控制器
                location: 消防控制室
                function:
                  - 系统监控
                  - 故障检测
                  - 消防联动
                  - 疏散路径规划
              area_controller:
                name: 区域控制器
                location: 各防火分区
                function:
                  - 区域监控
                  - 就地控制
              luminaires:
                name: 可寻址灯具
                feature: 双向通讯
                function:
                  - 方向可变
                  - 状态反馈
                  - 故障报告
                  
            operation_modes:
              normal:
                description: 平时状态
                luminaires: 充电待机
                signs: 常亮指示
              fire_mode:
                description: 火灾状态
                trigger: FAS火灾信号
                action:
                  - 所有应急灯亮
                  - 疏散指示按计算路径指向
                  - 着火区域指示改变方向
              blackout:
                description: 停电状态
                trigger: 正常电源失电
                action: 应急灯自动点亮
                
        control_points:
          status:
            - point_id: EL_SYSTEM_STATUS
              point_name: 系统状态
              point_type: DI
              values: [正常, 故障, 应急]
            - point_id: EL_BATTERY_STATUS
              point_name: 电池状态
              point_type: DI
          commands:
            - point_id: EL_FIRE_MODE
              point_name: 消防模式
              point_type: DI
              from: FIRE-FAS
        
        location_hint:
          space_type: 全院
          distribution: 疏散通道/关键区域

      - node_id: ELEC-LTG_DST_CONTROL
        node_name: 智能照明控制系统
        node_name_en: Intelligent Lighting Control System
        node_type: Distribution_Node
        node_subtype: CTR
        node_category: DST
        
        function: 照明智能控制
        medium_in: SIGNAL
        medium_out: CONTROL
        
        equipment_parameters:
          system_type: 智能照明控制系统
          protocol:
            field_bus:
              - KNX
              - DALI
              - Modbus
            integration: BACnet（与BA集成）
            
          components:
            central_controller:
              name: 照明主控制器
              location: BA机房
              function:
                - 全院照明监控
                - 场景控制
                - 定时控制
                - 能耗统计
            area_controller:
              name: 区域控制器
              location: 各楼层/区域
              function:
                - 区域照明控制
                - 传感器采集
            field_devices:
              switch_actuator:
                name: 开关执行器
                type: 继电器模块
                channels: {value: "4-12", unit: "路"}
              dimming_actuator:
                name: 调光执行器
                type: 0-10V/DALI
                channels: {value: "4-8", unit: "路"}
              sensor:
                types:
                  - 人体感应传感器
                  - 照度传感器
                  - 多功能面板
                  
          control_strategies:
            time_schedule:
              name: 时间表控制
              description: 按作息时间开关
              application: 公共区域、办公室
              example:
                - "07:00 开启公共区域照明"
                - "18:00 调暗非必要区域"
                - "22:00 切换夜间模式"
                
            occupancy_sensing:
              name: 人体感应控制
              description: 检测人员进入/离开
              application: 走廊、卫生间、会议室
              parameters:
                detection_range: {value: 8, unit: m}
                hold_time: {value: "5-15", unit: min}
                
            daylight_harvesting:
              name: 日光补偿控制
              description: 根据自然光调节人工照明
              application: 窗边区域
              parameters:
                target_illuminance: {value: 300, unit: lux}
                control_band: {value: "±50", unit: lux}
                
            scene_control:
              name: 场景控制
              description: 预设照明场景
              scenes:
                ward_day:
                  name: 病房-日间
                  illuminance: {value: 100, unit: lux}
                  color_temp: {value: 4000, unit: K}
                ward_night:
                  name: 病房-夜间
                  illuminance: {value: 10, unit: lux}
                  color_temp: {value: 2700, unit: K}
                examination:
                  name: 检查模式
                  illuminance: {value: 500, unit: lux}
                  color_temp: {value: 5000, unit: K}
                cleaning:
                  name: 清洁模式
                  illuminance: {value: 300, unit: lux}
                  duration: {value: 30, unit: min}
                  
        control_points:
          sensors:
            - point_id: LCS_ILLUMINANCE
              point_name: 环境照度
              point_type: AI
              unit: lux
            - point_id: LCS_OCCUPANCY
              point_name: 人员在场
              point_type: DI
          commands:
            - point_id: LCS_SCENE
              point_name: 场景切换
              point_type: DO
            - point_id: LCS_DIMMING
              point_name: 调光控制
              point_type: AO
              range: [0, 100]
        
        location_hint:
          space_type: BA机房/各区域

    sink_nodes:
    
      - node_id: ELEC-LTG_SNK_SPACE
        node_name: 照明空间
        node_name_en: Illuminated Space
        node_type: Sink_Node
        node_category: SNK
        
        function: 接受照明效果
        medium_in: LIGHT
        medium_out: ILLUMINATED_ENVIRONMENT
        
        is_boundary_output: true
        
        equipment_parameters:
          space_categories:
            medical_treatment:
              areas:
                - 手术室
                - 诊室
                - 治疗室
                - 检查室
              requirements:
                - 高照度
                - 高显色性
                - 无频闪
                - 专业灯具
            patient_care:
              areas:
                - 病房
                - ICU
                - 观察室
              requirements:
                - 舒适照明
                - 夜间照明
                - 分区控制
                - 患者个人控制
            public_circulation:
              areas:
                - 门诊大厅
                - 走廊
                - 电梯厅
              requirements:
                - 均匀照明
                - 节能控制
                - 应急照明
            support_service:
              areas:
                - 办公室
                - 会议室
                - 餐厅
                - 库房
              requirements:
                - 标准照明
                - 智能控制
                
        location_hint:
          space_type: 全院建筑空间

  edges:
  
    power_edges:
      - edge_id: ELEC-LTG_EDGE_001
        edge_name: 正常电源至配电箱
        edge_type: CAB
        from_node: ELEC-LTG_SRC_NORMAL
        to_node: ELEC-LTG_DST_PANEL
        direction: unidirectional
        medium: ELEC-LV
        
      - edge_id: ELEC-LTG_EDGE_002
        edge_name: 配电箱至灯具
        edge_type: CAB
        from_node: ELEC-LTG_DST_PANEL
        to_node: ELEC-LTG_DST_GENERAL
        direction: unidirectional
        medium: ELEC-LV

    control_edges:
      - edge_id: ELEC-LTG_EDGE_011
        edge_name: 控制系统至配电箱
        edge_type: SIG
        from_node: ELEC-LTG_DST_CONTROL
        to_node: ELEC-LTG_DST_PANEL
        direction: unidirectional
        medium: SIGNAL-CONTROL

  typical_paths:
  
    - path_id: ELEC-LTG_PATH_NORMAL
      path_name: 正常照明路径
      path_type: PWR
      description: 正常供电照明
      sequence:
        - step: 1
          node: ELEC-LTG_SRC_NORMAL
          action: 从低压配电供电
        - step: 2
          node: ELEC-LTG_DST_PANEL
          action: 配电箱分配
        - step: 3
          node: ELEC-LTG_DST_GENERAL
          action: 灯具点亮
        - step: 4
          node: ELEC-LTG_SNK_SPACE
          action: 空间照明

    - path_id: ELEC-LTG_PATH_EMERGENCY
      path_name: 应急照明路径
      path_type: EMR
      description: 火灾或停电时应急照明
      sequence:
        - step: 1
          trigger: 火灾信号或停电
        - step: 2
          node: ELEC-LTG_SRC_EMERGENCY
          action: EPS或电池供电
        - step: 3
          node: ELEC-LTG_DST_EMERGENCY
          action: 应急灯具点亮
        - step: 4
          node: 疏散通道
          action: 提供疏散照明

  control_logic:
  
    daily_schedule:
      name: 日常时间表控制
      description: 按医院作息自动控制
      
      schedule:
        "06:30":
          action: 开启公共区域照明
          areas: 走廊、大厅、电梯厅
        "07:00":
          action: 开启诊室照明
          areas: 门诊、医技
        "08:00":
          action: 全部照明正常
        "18:00":
          action: 关闭部分照明
          areas: 非必要办公区
        "21:00":
          action: 切换夜间模式
          areas: 病房（降低照度）
        "22:00":
          action: 公共区域减光
          areas: 走廊（50%亮度）
          
    fire_interlock:
      name: 消防联动
      description: 火灾时照明控制
      
      trigger: FIRE-FAS火灾确认信号
      
      response:
        emergency_lighting:
          action: 所有应急照明点亮
          mode: 100%亮度
        evacuation_signs:
          action: 疏散指示启动
          mode: 智能疏散（如有）
        non_fire_floors:
          action: 保持正常照明
          purpose: 避免恐慌

  alarm_protection:
  
    lighting_alarms:
      - alarm_id: ALM_LTG_LAMP_FAIL
        alarm_name: 灯具故障
        severity: LOW
        trigger: 灯具不亮/闪烁
        action: 更换灯具
        
      - alarm_id: ALM_LTG_CIRCUIT_TRIP
        alarm_name: 照明回路跳闸
        severity: MEDIUM
        trigger: 回路断路器跳闸
        action: 检查短路/过载
        
      - alarm_id: ALM_LTG_EMERGENCY_FAIL
        alarm_name: 应急照明故障
        severity: HIGH
        trigger: 应急灯自检失败
        action: 立即检修

  dependencies:
    
    upstream_dependencies:
      - dependency_id: DEP_LTG_NORMAL
        from_system: ELEC-LV
        dependency_type: POWER_SUPPLY
        criticality: HIGH
        
      - dependency_id: DEP_LTG_EMERGENCY
        from_system: ELEC-EPS
        dependency_type: EMERGENCY_POWER
        criticality: CRITICAL
        
      - dependency_id: DEP_LTG_FAS
        from_system: FIRE-FAS
        dependency_type: FIRE_SIGNAL
        criticality: CRITICAL
        
      - dependency_id: DEP_LTG_BA
        from_system: INT-BA
        dependency_type: CONTROL
        criticality: MEDIUM
```

---

## 系统间完整依赖关系总图

```yaml
System_Dependency_Matrix:

  identity:
    name: 医院机电系统依赖关系总图
    description: 展示所有系统间的依赖和联动关系
    version: 1.0
    total_systems: 26
    last_updated: 2024

  # ========================================
  # 系统清单
  # ========================================
  system_inventory:
    
    electrical_systems:
      - id: ELEC-HV
        name: 高压配电系统
        priority: P1
      - id: ELEC-LV
        name: 低压配电系统
        priority: P1
      - id: ELEC-EPS
        name: 应急电源系统
        priority: P1
      - id: ELEC-UPS
        name: 不间断电源系统
        priority: P1
      - id: ELEC-EL
        name: 电梯系统
        priority: P2
      - id: ELEC-LTG
        name: 照明系统
        priority: P2
        
    hvac_systems:
      - id: HVAC-CHP
        name: 冷热源系统
        priority: P1
      - id: HVAC-AHU
        name: 空调机组系统
        priority: P2
      - id: HVAC-FCU
        name: 风机盘管系统
        priority: P3
        
    plumbing_systems:
      - id: PLUMB-DWS
        name: 生活给水系统
        priority: P2
      - id: PLUMB-HWS
        name: 生活热水系统
        priority: P3
      - id: PLUMB-SAN
        name: 污废水系统
        priority: P2
      - id: PLUMB-RW
        name: 雨水排水系统
        priority: P3
        
    medical_gas_systems:
      - id: MGAS-O2
        name: 医用氧气系统
        priority: P1
      - id: MGAS-VAC
        name: 医用负压系统
        priority: P1
      - id: MGAS-AIR
        name: 医用压缩空气系统
        priority: P1
      - id: MGAS-N2O
        name: 笑气系统
        priority: P2
        
    fire_protection_systems:
      - id: FIRE-FAS
        name: 火灾自动报警系统
        priority: P1
      - id: FIRE-SPS
        name: 自动喷水灭火系统
        priority: P1
      - id: FIRE-EXH
        name: 防排烟系统
        priority: P1
        
    integration_systems:
      - id: INT-BA
        name: 楼宇自动化系统
        priority: P2
      - id: INT-SEC
        name: 安防系统
        priority: P2
      - id: INT-NUR
        name: 护理呼叫系统
        priority: P2
        
    medical_environment_systems:
      - id: MED-OR
        name: 手术室净化系统
        priority: P1
      - id: MED-ICU
        name: ICU净化系统
        priority: P1
      - id: MED-LAB
        name: 检验科通风系统
        priority: P2

  # ========================================
  # 电力依赖关系（Power Dependencies）
  # ========================================
  power_dependencies:
    
    primary_power_chain:
      description: 主电源供应链
      flow:
        - from: 市电
          to: ELEC-HV
          type: PRIMARY
        - from: ELEC-HV
          to: ELEC-LV
          type: TRANSFORM
        - from: ELEC-LV
          to: ALL_SYSTEMS
          type: DISTRIBUTION
          
    emergency_power_chain:
      description: 应急电源供应链
      flow:
        - from: ELEC-LV
          to: ELEC-EPS
          type: CHARGING
        - from: ELEC-EPS
          to: CRITICAL_LOADS
          type: BACKUP
          targets:
            - ELEC-EL（消防电梯）
            - ELEC-LTG（应急照明）
            - FIRE-FAS
            - FIRE-EXH
            - MGAS-O2
            - MGAS-VAC
            - MED-OR
            - MED-ICU
            
    ups_power_chain:
      description: UPS电源供应链
      flow:
        - from: ELEC-LV
          to: ELEC-UPS
          type: CHARGING
        - from: ELEC-UPS
          to: IT_LOADS
          type: UNINTERRUPTED
          targets:
            - INT-BA（控制器）
            - INT-SEC（服务器）
            - INT-NUR（主机）
            - FIRE-FAS（主机）
            - 手术室设备
            
  # ========================================
  # 冷热源依赖关系（Thermal Dependencies）
  # ========================================
  thermal_dependencies:
    
    cooling_chain:
      description: 冷源供应链
      flow:
        - from: HVAC-CHP
          to: HVAC-AHU
          type: CHW_SUPPLY
        - from: HVAC-CHP
          to: HVAC-FCU
          type: CHW_SUPPLY
        - from: HVAC-CHP
          to: MED-OR
          type: CHW_SUPPLY
        - from: HVAC-CHP
          to: MED-ICU
          type: CHW_SUPPLY
        - from: HVAC-CHP
          to: MED-LAB
          type: CHW_SUPPLY
          
    heating_chain:
      description: 热源供应链
      flow:
        - from: HVAC-CHP
          to: HVAC-AHU
          type: HW_SUPPLY
        - from: HVAC-CHP
          to: HVAC-FCU
          type: HW_SUPPLY
        - from: HVAC-CHP
          to: PLUMB-HWS
          type: STEAM/HW_SUPPLY
          
    air_conditioning_chain:
      description: 空调供应链
      flow:
        - from: HVAC-AHU
          to: MED-OR
          type: CONDITIONED_AIR
        - from: HVAC-AHU
          to: MED-ICU
          type: CONDITIONED_AIR
        - from: HVAC-AHU
          to: MED-LAB
          type: CONDITIONED_AIR
        - from: HVAC-FCU
          to: WARDS
          type: CONDITIONED_AIR
          
  # ========================================
  # 消防联动关系（Fire Protection Interlocks）
  # ========================================
  fire_interlocks:
    
    fas_master:
      description: FAS作为消防主控系统
      sends_to:
        - target: ELEC-EL
          signal: FIRE_CONFIRM
          action: 电梯迫降/消防模式
        - target: FIRE-SPS
          signal: FIRE_CONFIRM
          action: 喷淋泵启动
        - target: FIRE-EXH
          signal: FIRE_CONFIRM
          action: 排烟系统启动
        - target: HVAC-AHU
          signal: FIRE_CONFIRM
          action: 空调停止/新风关闭
        - target: HVAC-FCU
          signal: FIRE_CONFIRM
          action: 着火层FCU停止
        - target: ELEC-LTG
          signal: FIRE_CONFIRM
          action: 应急照明启动
        - target: INT-BA
          signal: FIRE_CONFIRM
          action: 广播疏散/状态显示
        - target: INT-SEC
          signal: FIRE_CONFIRM
          action: 门禁紧急开启
          
    fire_floor_isolation:
      description: 着火楼层隔离
      actions:
        - system: HVAC-AHU
          action: 关闭着火区域AHU
        - system: HVAC-FCU
          action: 关闭着火区域水阀
        - system: HVAC-CHP
          action: 关闭着火楼层供水阀
        - system: FIRE-EXH
          action: 开启着火区域排烟
          
  # ========================================
  # 医疗气体依赖关系（Medical Gas Dependencies）
  # ========================================
  medical_gas_dependencies:
    
    primary_users:
      MED-OR:
        requires:
          - MGAS-O2（氧气）
          - MGAS-VAC（负压）
          - MGAS-AIR（压缩空气）
          - MGAS-N2O（笑气）
      MED-ICU:
        requires:
          - MGAS-O2
          - MGAS-VAC
          - MGAS-AIR
      WARDS:
        requires:
          - MGAS-O2
          - MGAS-VAC
          
    alarm_integration:
      from: MGAS-ALL
      to: INT-NUR
      signals:
        - 区域报警盘状态
        - 气源压力异常
        - 真空度异常
        
  # ========================================
  # 楼宇自动化集成（BA Integration）
  # ========================================
  ba_integration:
    
    monitored_systems:
      mechanical:
        - HVAC-CHP（完全控制）
        - HVAC-AHU（完全控制）
        - HVAC-FCU（监控+温度设定）
        - MED-OR（监控）
        - MED-ICU（监控）
        - MED-LAB（监控）
      electrical:
        - ELEC-LV（监控）
        - ELEC-EPS（监控）
        - ELEC-UPS（监控）
        - ELEC-EL（监控）
        - ELEC-LTG（完全控制）
      plumbing:
        - PLUMB-DWS（监控）
        - PLUMB-HWS（监控+控制）
        - PLUMB-SAN（监控）
        - PLUMB-RW（监控）
      medical_gas:
        - MGAS-O2（监控）
        - MGAS-VAC（监控）
        - MGAS-AIR（监控）
      fire:
        - FIRE-FAS（信号接收）
        - FIRE-SPS（监控）
        - FIRE-EXH（监控）
        
    integration_protocols:
      primary: BACnet IP
      secondary:
        - Modbus TCP
        - OPC UA
      legacy:
        - Modbus RTU
        - Lonworks

  # ========================================
  # 依赖关系矩阵
  # ========================================
  dependency_matrix:
    
    format: |
      行：依赖方（需要...的系统）
      列：被依赖方（提供...的系统）
      值：依赖类型和关键程度
      
    matrix:
      # ELEC-HV依赖
      ELEC-HV:
        市电: {type: PRIMARY, criticality: CRITICAL}
        
      # ELEC-LV依赖
      ELEC-LV:
        ELEC-HV: {type: POWER, criticality: CRITICAL}
        
      # ELEC-EPS依赖
      ELEC-EPS:
        ELEC-LV: {type: CHARGING, criticality: HIGH}
        
      # ELEC-UPS依赖
      ELEC-UPS:
        ELEC-LV: {type: CHARGING, criticality: HIGH}
        ELEC-EPS: {type: BACKUP, criticality: HIGH}
        
      # ELEC-EL依赖
      ELEC-EL:
        ELEC-LV: {type: POWER, criticality: CRITICAL}
        ELEC-EPS: {type: BACKUP, criticality: HIGH}
        FIRE-FAS: {type: INTERLOCK, criticality: CRITICAL}
        INT-SEC: {type: CONTROL, criticality: MEDIUM}
        
      # ELEC-LTG依赖
      ELEC-LTG:
        ELEC-LV: {type: POWER, criticality: HIGH}
        ELEC-EPS: {type: BACKUP, criticality: HIGH}
        FIRE-FAS: {type: INTERLOCK, criticality: CRITICAL}
        INT-BA: {type: CONTROL, criticality: MEDIUM}
        
      # HVAC-CHP依赖
      HVAC-CHP:
        ELEC-LV: {type: POWER, criticality: CRITICAL}
        ELEC-EPS: {type: BACKUP, criticality: HIGH}
        PLUMB-DWS: {type: WATER, criticality: HIGH}
        INT-BA: {type: CONTROL, criticality: HIGH}
        FIRE-FAS: {type: INTERLOCK, criticality: HIGH}
        
      # HVAC-AHU依赖
      HVAC-AHU:
        ELEC-LV: {type: POWER, criticality: HIGH}
        HVAC-CHP: {type: CHW_HW, criticality: HIGH}
        INT-BA: {type: CONTROL, criticality: HIGH}
        FIRE-FAS: {type: INTERLOCK, criticality: CRITICAL}
        
      # HVAC-FCU依赖
      HVAC-FCU:
        ELEC-LV: {type: POWER, criticality: MEDIUM}
        HVAC-CHP: {type: CHW_HW, criticality: HIGH}
        HVAC-AHU: {type: FRESH_AIR, criticality: MEDIUM}
        INT-BA: {type: CONTROL, criticality: LOW}
        
      # MED-OR依赖
      MED-OR:
        ELEC-LV: {type: POWER, criticality: CRITICAL}
        ELEC-EPS: {type: BACKUP, criticality: CRITICAL}
        ELEC-UPS: {type: BACKUP, criticality: CRITICAL}
        HVAC-CHP: {type: CHW_HW, criticality: CRITICAL}
        HVAC-AHU: {type: CONDITIONED_AIR, criticality: CRITICAL}
        MGAS-O2: {type: MEDICAL_GAS, criticality: CRITICAL}
        MGAS-VAC: {type: MEDICAL_GAS, criticality: CRITICAL}
        MGAS-AIR: {type: MEDICAL_GAS, criticality: CRITICAL}
        MGAS-N2O: {type: MEDICAL_GAS, criticality: HIGH}
        INT-BA: {type: MONITOR, criticality: MEDIUM}
        
      # MED-ICU依赖
      MED-ICU:
        ELEC-LV: {type: POWER, criticality: CRITICAL}
        ELEC-EPS: {type: BACKUP, criticality: CRITICAL}
        ELEC-UPS: {type: BACKUP, criticality: CRITICAL}
        HVAC-CHP: {type: CHW_HW, criticality: CRITICAL}
        HVAC-AHU: {type: CONDITIONED_AIR, criticality: CRITICAL}
        MGAS-O2: {type: MEDICAL_GAS, criticality: CRITICAL}
        MGAS-VAC: {type: MEDICAL_GAS, criticality: CRITICAL}
        MGAS-AIR: {type: MEDICAL_GAS, criticality: HIGH}
        INT-NUR: {type: NURSE_CALL, criticality: CRITICAL}
        
      # FIRE-FAS依赖
      FIRE-FAS:
        ELEC-LV: {type: POWER, criticality: CRITICAL}
        ELEC-UPS: {type: BACKUP, criticality: CRITICAL}
        
      # FIRE-SPS依赖
      FIRE-SPS:
        ELEC-LV: {type: POWER, criticality: CRITICAL}
        ELEC-EPS: {type: BACKUP, criticality: CRITICAL}
        PLUMB-DWS: {type: WATER, criticality: CRITICAL}
        FIRE-FAS: {type: INTERLOCK, criticality: CRITICAL}
        
      # FIRE-EXH依赖
      FIRE-EXH:
        ELEC-LV: {type: POWER, criticality: CRITICAL}
        ELEC-EPS: {type: BACKUP, criticality: CRITICAL}
        FIRE-FAS: {type: INTERLOCK, criticality: CRITICAL}
        
      # INT-BA依赖
      INT-BA:
        ELEC-LV: {type: POWER, criticality: HIGH}
        ELEC-UPS: {type: BACKUP, criticality: HIGH}
        FIRE-FAS: {type: INTERLOCK, criticality: HIGH}
```

---

## 跨系统联动场景汇总

```yaml
Cross_System_Scenarios:

  identity:
    name: 跨系统联动场景汇总
    description: 涉及多个系统协同的典型运行场景
    version: 1.0
    last_updated: 2024

  scenarios:
  
    # ========================================
    # 场景1：火灾应急响应
    # ========================================
    - scenario_id: SCN_FIRE_EMERGENCY
      scenario_name: 火灾应急响应
      trigger: 火灾报警确认
      priority: CRITICAL
      
      participating_systems:
        - FIRE-FAS（主控）
        - FIRE-SPS
        - FIRE-EXH
        - ELEC-EL
        - ELEC-LTG
        - HVAC-AHU
        - HVAC-FCU
        - HVAC-CHP
        - INT-BA
        - INT-SEC
        
      sequence:
        t_0:
          event: 火灾探测器动作
          system: FIRE-FAS
          
        t_30s:
          event: 火灾确认
          system: FIRE-FAS
          action: 发出联动信号
          
        t_32s:
          event: 电梯迫降
          system: ELEC-EL
          action: 就近停靠，返回基站
          
        t_35s:
          event: 排烟启动
          system: FIRE-EXH
          action: 开启排烟阀和排烟风机
          
        t_35s:
          event: 加压送风
          system: FIRE-EXH
          action: 开启楼梯间加压风机
          
        t_40s:
          event: 空调停止
          system: HVAC-AHU
          action: 关闭着火区域AHU
          
        t_40s:
          event: FCU关闭
          system: HVAC-FCU
          action: 关闭着火楼层水阀
          
        t_45s:
          event: 应急照明
          system: ELEC-LTG
          action: 所有应急灯点亮
          
        t_45s:
          event: 疏散指示
          system: ELEC-LTG
          action: 智能疏散系统启动
          
        t_50s:
          event: 喷淋启动
          system: FIRE-SPS
          action: 着火区域喷头动作
          
        t_60s:
          event: 门禁开启
          system: INT-SEC
          action: 所有防火门解锁
          
        t_60s:
          event: 广播疏散
          system: INT-BA
          action: 消防广播启动
          
      post_fire_recovery:
        trigger: 消防确认火灾扑灭
        sequence:
          - 消防系统复位
          - 排烟系统停止
          - HVAC系统逐步恢复
          - 电梯恢复正常
          - 门禁恢复正常
          
    # ========================================
    # 场景2：市电中断应急响应
    # ========================================
    - scenario_id: SCN_POWER_OUTAGE
      scenario_name: 市电中断应急响应
      trigger: 市电失电
      priority: CRITICAL
      
      participating_systems:
        - ELEC-HV
        - ELEC-LV
        - ELEC-EPS
        - ELEC-UPS
        - ELEC-EL
        - ELEC-LTG
        - HVAC-CHP
        - MED-OR
        - MED-ICU
        - MGAS-O2
        - MGAS-VAC
        - INT-BA
        
      sequence:
        t_0:
          event: 市电失电
          system: ELEC-HV
          detection: 失压保护动作
          
        t_0~15s:
          event: UPS接管
          system: ELEC-UPS
          action: 无缝切换，IT负载不中断
          loads:
            - BA系统控制器
            - 手术室关键设备
            - ICU监护设备
            - 消防主机
            
        t_10s:
          event: 发电机启动
          system: ELEC-EPS
          action: 柴油发电机自启动
          
        t_15s:
          event: 发电机并网
          system: ELEC-EPS
          action: ATS切换至发电机
          
        t_15~30s:
          event: EPS负载恢复
          action: 分批恢复EPS负载
          loads:
            - 消防电梯
            - 应急照明
            - 手术室空调
            - ICU空调
            - 医用气体机组
            
        t_30s:
          event: 应急照明
          system: ELEC-LTG
          action: 应急灯已点亮（EPS供电）
          
        t_60s:
          event: 冷热源调整
          system: HVAC-CHP
          action:
            - 关闭非关键冷机
            - 保留关键区域冷源
            - 电锅炉停止，切换燃气锅炉
            
        ongoing:
          event: 监控管理
          system: INT-BA
          action:
            - 监控发电机运行
            - 优化负载分配
            - 记录事件
            
      power_restoration:
        trigger: 市电恢复
        sequence:
          - 确认市电稳定（5分钟）
          - ATS切换回市电
          - 逐步恢复正常负载
          - 发电机冷却后停止
          - UPS恢复充电
          
    # ========================================
    # 场景3：手术室紧急启用
    # ========================================
    - scenario_id: SCN_OR_EMERGENCY_START
      scenario_name: 手术室紧急启用
      trigger: 急诊手术请求
      priority: HIGH
      
      participating_systems:
        - MED-OR
        - HVAC-CHP
        - HVAC-AHU
        - MGAS-O2
        - MGAS-VAC
        - MGAS-AIR
        - MGAS-N2O
        - ELEC-LTG
        - INT-BA
        
      sequence:
        t_0:
          event: 急诊手术请求
          system: 临床系统
          action: 指定手术室
          
        t_0:
          event: 启动手术室
          system: INT-BA
          action: 触发手术室启动程序
          
        t_0~5min:
          event: 空调启动
          system: MED-OR + HVAC-AHU
          action:
            - 启动手术室AHU
            - 建立正压
            - 温湿度调节
            
        t_5min:
          event: 洁净度达标
          system: MED-OR
          verification:
            - 压差≥5Pa
            - 换气次数≥20次/h
            - 温度22±2℃
            
        t_0~2min:
          event: 医用气体确认
          system: MGAS-ALL
          verification:
            - O2压力正常
            - VAC真空度正常
            - AIR压力正常
            - N2O压力正常（如需）
            
        t_0~1min:
          event: 照明就绪
          system: ELEC-LTG
          action:
            - 无影灯预热
            - 一般照明100%
            
        t_5min:
          event: 手术室就绪
          system: INT-BA
          action: 确认就绪，通知手术团队
          
    # ========================================
    # 场景4：夏季高峰负荷管理
    # ========================================
    - scenario_id: SCN_PEAK_LOAD_SUMMER
      scenario_name: 夏季高峰负荷管理
      trigger: 室外温度>35℃ 或 电力负荷>90%
      priority: MEDIUM
      
      participating_systems:
        - HVAC-CHP
        - HVAC-AHU
        - HVAC-FCU
        - ELEC-LV
        - ELEC-LTG
        - INT-BA
        
      sequence:
        t_0:
          event: 高峰负荷检测
          system: INT-BA
          trigger: 室外>35℃ 或 电力>90%
          
        t_0:
          event: 负荷优化启动
          system: INT-BA
          action: 触发负荷削减程序
          
        t_1min:
          event: 冷源优化
          system: HVAC-CHP
          action:
            - 启动所有冷机（冰蓄冷放冷）
            - 冷冻水供水温度维持7℃
            - 冷却塔全速运行
            
        t_2min:
          event: 温度设定调整
          system: HVAC-FCU
          action:
            - 非关键区域温度设定+2℃
            - 关键区域（手术室/ICU）不变
            
        t_3min:
          event: 照明负荷削减
          system: ELEC-LTG
          action:
            - 公共区域照明降至80%
            - 关闭装饰照明
            - 利用自然光的区域降至60%
            
        t_5min:
          event: 非关键设备降载
          system: INT-BA
          action:
            - 电热水器暂停
            - 非关键电梯减速
            
        ongoing:
          event: 持续监控
          system: INT-BA
          action:
            - 监控室温和电力
            - 根据情况动态调整
            
      recovery:
        trigger: 室外<32℃ 或 电力<80%
        action: 逐步恢复正常设定
        
    # ========================================
    # 场景5：负压隔离病房启用
    # ========================================
    - scenario_id: SCN_ISOLATION_WARD_ACTIVATE
      scenario_name: 负压隔离病房启用
      trigger: 传染病患者入院
      priority: HIGH
      
      participating_systems:
        - HVAC-AHU（隔离区新风机组）
        - HVAC-FCU（隔离区）
        - FIRE-EXH（排风）
        - MGAS-O2
        - MGAS-VAC
        - INT-BA
        - INT-NUR
        
      sequence:
        t_0:
          event: 隔离病房启用请求
          system: 临床系统
          
        t_0:
          event: 启动隔离模式
          system: INT-BA
          action: 触发隔离病房启动程序
          
        t_1min:
          event: 排风启动
          system: 隔离区排风系统
          action:
            - 启动排风机
            - 建立负压
            
        t_2min:
          event: 新风启动
          system: HVAC-AHU（隔离区）
          action:
            - 启动新风机组
            - 100%新风，无回风
            
        t_3min:
          event: 负压建立
          system: 隔离病房
          verification:
            - 负压≥-5Pa（相对走廊）
            - 气流从走廊→病房→卫生间→排风
            
        t_3min:
          event: FCU调节
          system: HVAC-FCU
          action:
            - 温度设定24℃
            - 独立控制
            
        t_5min:
          event: 医用气体确认
          system: MGAS-O2, MGAS-VAC
          verification: 压力正常
          
        t_5min:
          event: 护理呼叫就绪
          system: INT-NUR
          action: 确认呼叫系统正常
          
        t_5min:
          event: 隔离病房就绪
          system: INT-BA
          action: 通知临床可收治患者

  # ========================================
  # 场景汇总表
  # ========================================
  scenario_summary:
    
    - id: SCN_FIRE_EMERGENCY
      name: 火灾应急响应
      trigger: 火灾确认
      systems: 10个
      priority: CRITICAL
      response_time: <60s
      
    - id: SCN_POWER_OUTAGE
      name: 市电中断应急
      trigger: 市电失电
      systems: 12个
      priority: CRITICAL
      response_time: <15s（UPS）, <30s（EPS）
      
    - id: SCN_OR_EMERGENCY_START
      name: 手术室紧急启用
      trigger: 急诊手术请求
      systems: 9个
      priority: HIGH
      response_time: <5min
      
    - id: SCN_PEAK_LOAD_SUMMER
      name: 夏季高峰负荷管理
      trigger: 高温/高负荷
      systems: 6个
      priority: MEDIUM
      response_time: <5min
      
    - id: SCN_ISOLATION_WARD_ACTIVATE
      name: 负压隔离病房启用
      trigger: 传染病患者入院
      systems: 7个
      priority: HIGH
      response_time: <5min
```

---

## 数据点统计与分类

```yaml
Data_Point_Statistics:

  identity:
    name: 医院机电系统数据点统计
    description: 各系统监控点数统计和分类
    version: 1.0
    last_updated: 2024

  # ========================================
  # 总体统计
  # ========================================
  overall_statistics:
    
    total_systems: 26
    
    estimated_total_points:
      small_hospital:
        beds: 300
        total_points: {value: "8,000-12,000", unit: "点"}
      medium_hospital:
        beds: 600
        total_points: {value: "15,000-25,000", unit: "点"}
      large_hospital:
        beds: 1000
        total_points: {value: "30,000-50,000", unit: "点"}
        
    point_type_distribution:
      AI: {percentage: 35, description: "模拟量输入（温度、压力、流量等）"}
      AO: {percentage: 15, description: "模拟量输出（阀门开度、频率等）"}
      DI: {percentage: 35, description: "数字量输入（状态、报警等）"}
      DO: {percentage: 15, description: "数字量输出（启停命令等）"}

  # ========================================
  # 各系统点数估算
  # ========================================
  system_point_estimates:
    
    # 电气系统
    electrical_systems:
      
      ELEC-HV:
        name: 高压配电系统
        base_points:
          per_switch: {value: 15, note: "电压、电流、功率、状态、报警"}
          per_transformer: {value: 20}
        typical_quantity:
          switches: 10
          transformers: 4
        estimated_total: {value: "200-300", unit: "点"}
        
      ELEC-LV:
        name: 低压配电系统
        base_points:
          per_panel: {value: 25, note: "进线、馈线、状态"}
          per_feeder: {value: 5}
        typical_quantity:
          panels: 50
          feeders: 500
        estimated_total: {value: "3,000-4,000", unit: "点"}
        
      ELEC-EPS:
        name: 应急电源系统
        base_points:
          generator: {value: 100, note: "发动机+发电机+控制"}
          ats: {value: 20}
          eps_cabinet: {value: 30}
        typical_quantity:
          generators: 2
          ats: 10
          eps_cabinets: 20
        estimated_total: {value: "600-800", unit: "点"}
        
      ELEC-UPS:
        name: UPS系统
        base_points:
          per_ups: {value: 50, note: "输入、输出、电池、报警"}
        typical_quantity:
          ups_units: 10
        estimated_total: {value: "400-600", unit: "点"}
        
      ELEC-EL:
        name: 电梯系统
        base_points:
          per_elevator: {value: 30, note: "位置、状态、故障、能耗"}
        typical_quantity:
          elevators: 20
        estimated_total: {value: "500-700", unit: "点"}
        
      ELEC-LTG:
        name: 照明系统
        base_points:
          per_panel: {value: 15}
          per_zone: {value: 5}
        typical_quantity:
          panels: 100
          zones: 300
        estimated_total: {value: "2,000-3,000", unit: "点"}
        
    # 暖通系统
    hvac_systems:
      
      HVAC-CHP:
        name: 冷热源系统
        base_points:
          per_chiller: {value: 80, note: "运行参数+控制+报警"}
          per_boiler: {value: 60}
          per_cooling_tower: {value: 30}
          per_pump: {value: 15}
          header_system: {value: 100}
        typical_quantity:
          chillers: 4
          boilers: 3
          cooling_towers: 4
          pumps: 20
        estimated_total: {value: "800-1,200", unit: "点"}
        
      HVAC-AHU:
        name: 空调机组系统
        base_points:
          per_ahu: {value: 40, note: "温湿度、风阀、风机、过滤器"}
          per_mau: {value: 35}
          per_fau: {value: 25}
        typical_quantity:
          ahu: 30
          mau: 10
          fau: 20
        estimated_total: {value: "1,500-2,500", unit: "点"}
        
      HVAC-FCU:
        name: 风机盘管系统
        base_points:
          per_fcu: {value: 5, note: "温度、开关、阀门（简化监控）"}
          per_floor_header: {value: 20}
        typical_quantity:
          fcu: 800
          floor_headers: 20
        estimated_total: {value: "4,000-5,000", unit: "点"}
        note: FCU数量多，点数占比大
        
    # 给排水系统
    plumbing_systems:
      
      PLUMB-DWS:
        name: 生活给水系统
        base_points:
          per_pump_set: {value: 30}
          per_tank: {value: 15}
          per_zone: {value: 10}
        typical_quantity:
          pump_sets: 5
          tanks: 4
          zones: 10
        estimated_total: {value: "250-400", unit: "点"}
        
      PLUMB-HWS:
        name: 生活热水系统
        base_points:
          per_heater: {value: 25}
          per_circulation_pump: {value: 10}
        typical_quantity:
          heaters: 4
          pumps: 8
        estimated_total: {value: "150-250", unit: "点"}
        
      PLUMB-SAN:
        name: 污废水系统
        base_points:
          per_sump: {value: 20}
          per_treatment: {value: 30}
        typical_quantity:
          sumps: 10
          treatment: 2
        estimated_total: {value: "200-300", unit: "点"}
        
      PLUMB-RW:
        name: 雨水系统
        base_points:
          per_pump_station: {value: 20}
          reclaim_system: {value: 50}
        typical_quantity:
          pump_stations: 3
          reclaim: 1
        estimated_total: {value: "100-150", unit: "点"}
        
    # 医用气体系统
    medical_gas_systems:
      
      MGAS-O2:
        name: 医用氧气系统
        base_points:
          source: {value: 50, note: "液氧罐+汇流排+切换"}
          per_area_alarm: {value: 15}
          per_zone_valve: {value: 5}
        typical_quantity:
          area_alarms: 20
          zone_valves: 50
        estimated_total: {value: "400-600", unit: "点"}
        
      MGAS-VAC:
        name: 医用负压系统
        base_points:
          vacuum_station: {value: 60}
          per_area_alarm: {value: 15}
        typical_quantity:
          area_alarms: 15
        estimated_total: {value: "250-350", unit: "点"}
        
      MGAS-AIR:
        name: 医用压缩空气系统
        base_points:
          compressor_station: {value: 50}
          per_area_alarm: {value: 15}
        typical_quantity:
          area_alarms: 10
        estimated_total: {value: "150-250", unit: "点"}
        
      MGAS-N2O:
        name: 笑气系统
        base_points:
          source: {value: 20}
          per_area_alarm: {value: 10}
        typical_quantity:
          area_alarms: 5
        estimated_total: {value: "50-100", unit: "点"}
        
    # 消防系统
    fire_protection_systems:
      
      FIRE-FAS:
        name: 火灾自动报警系统
        base_points:
          per_detector: {value: 1, note: "报警点"}
          per_module: {value: 2, note: "控制模块"}
          per_panel: {value: 20}
        typical_quantity:
          detectors: 3000
          modules: 500
          panels: 10
        estimated_total: {value: "4,000-5,000", unit: "点"}
        note: 探测器数量大
        
      FIRE-SPS:
        name: 自动喷水灭火系统
        base_points:
          per_pump: {value: 25}
          per_zone: {value: 15}
          per_alarm_valve: {value: 10}
        typical_quantity:
          pumps: 4
          zones: 10
          alarm_valves: 15
        estimated_total: {value: "300-400", unit: "点"}
        
      FIRE-EXH:
        name: 防排烟系统
        base_points:
          per_smoke_exhaust_fan: {value: 15}
          per_pressurization_fan: {value: 15}
          per_damper: {value: 3}
        typical_quantity:
          exhaust_fans: 15
          pressurization_fans: 10
          dampers: 100
        estimated_total: {value: "600-800", unit: "点"}
        
    # 智能化系统
    integration_systems:
      
      INT-BA:
        name: 楼宇自动化系统
        points: "汇总其他系统点数"
        own_points:
          servers: {value: 20}
          workstations: {value: 10}
          gateways: {value: 50}
        estimated_own_total: {value: "100-200", unit: "点"}
        
      INT-SEC:
        name: 安防系统
        base_points:
          per_camera: {value: 5}
          per_access_point: {value: 8}
          per_intrusion_zone: {value: 3}
        typical_quantity:
          cameras: 200
          access_points: 100
          intrusion_zones: 50
        estimated_total: {value: "2,000-2,500", unit: "点"}
        
      INT-NUR:
        name: 护理呼叫系统
        base_points:
          per_bed: {value: 3}
          per_nurse_station: {value: 15}
        typical_quantity:
          beds: 600
          nurse_stations: 30
        estimated_total: {value: "2,000-2,500", unit: "点"}
        
    # 医疗环境系统
    medical_environment_systems:
      
      MED-OR:
        name: 手术室净化系统
        base_points:
          per_or: {value: 80, note: "温湿度、压差、洁净度、照明等"}
        typical_quantity:
          operating_rooms: 15
        estimated_total: {value: "1,000-1,500", unit: "点"}
        
      MED-ICU:
        name: ICU净化系统
        base_points:
          per_bed: {value: 30}
          common: {value: 100}
        typical_quantity:
          beds: 30
        estimated_total: {value: "800-1,200", unit: "点"}
        
      MED-LAB:
        name: 检验科通风系统
        base_points:
          per_fume_hood: {value: 10}
          per_biosafety_cabinet: {value: 15}
          exhaust_system: {value: 50}
        typical_quantity:
          fume_hoods: 20
          biosafety_cabinets: 10
        estimated_total: {value: "300-500", unit: "点"}

  # ========================================
  # 点数汇总表
  # ========================================
  point_summary_table:
    
    by_category:
      电气系统:
        systems: 6
        points: {value: "6,700-9,400", unit: "点"}
        percentage: 25%
      暖通系统:
        systems: 3
        points: {value: "6,300-8,700", unit: "点"}
        percentage: 25%
      给排水系统:
        systems: 4
        points: {value: "700-1,100", unit: "点"}
        percentage: 3%
      医用气体系统:
        systems: 4
        points: {value: "850-1,300", unit: "点"}
        percentage: 4%
      消防系统:
        systems: 3
        points: {value: "4,900-6,200", unit: "点"}
        percentage: 18%
      智能化系统:
        systems: 3
        points: {value: "4,100-5,200", unit: "点"}
        percentage: 15%
      医疗环境系统:
        systems: 3
        points: {value: "2,100-3,200", unit: "点"}
        percentage: 10%
        
    total:
      systems: 26
      points: {value: "25,650-35,100", unit: "点"}
      typical_large_hospital: {value: "30,000", unit: "点"}

  # ========================================
  # 点位命名规范
  # ========================================
  point_naming_convention:
    
    format: "{System}_{Building}_{Floor}_{Equipment}_{PointType}_{PointName}"
    
    examples:
      - "HVAC-CHP_MB_B1_CH01_AI_CHWST"
        # 冷热源系统_主楼_B1层_1号冷机_模拟量输入_冷冻水供水温度
      - "ELEC-LV_OB_1F_LP01_DI_MAINCB"
        # 低压配电_门诊楼_1层_1号照明箱_数字量输入_总开关状态
      - "MGAS-O2_IB_5F_ZV01_DO_OPEN"
        # 医用氧气_住院楼_5层_1号区域阀_数字量输出_开启
        
    abbreviations:
      buildings:
        MB: Main Building（主楼）
        OB: Outpatient Building（门诊楼）
        IB: Inpatient Building（住院楼）
        EB: Emergency Building（急诊楼）
      point_types:
        AI: Analog Input
        AO: Analog Output
        DI: Digital Input
        DO: Digital Output
      common_points:
        ST: Supply Temperature
        RT: Return Temperature
        SP: Setpoint
        STS: Status
        ALM: Alarm
        CMD: Command
```

---

# 第六批次（最终批次）完成

## 本批次系统总结

| 系统ID | 系统名称 | 类别 | 优先级 |
|--------|----------|------|--------|
| PLUMB-RW | 雨水排水系统 | 给排水 | P3-一般 |
| ELEC-LTG | 照明系统 | 电气 | P2-业务关键 |

## 本批次综合文档

| 文档名称 | 描述 |
|----------|------|
| System_Dependency_Matrix | 26个系统间完整依赖关系 |
| Cross_System_Scenarios | 5个跨系统联动场景 |
| Data_Point_Statistics | 全院数据点统计与分类 |

---

# 全部输出完成总结

## 六批次输出汇总

| 批次 | 系统/文档 | 数量 |
|------|-----------|------|
| 第一批 | MGAS-O2, MGAS-VAC, MGAS-AIR, ELEC-HV, ELEC-LV | 5个系统 |
| 第二批 | ELEC-EPS, ELEC-UPS, PLUMB-DWS, PLUMB-HWS, PLUMB-SAN | 5个系统 |
| 第三批 | INT-BA, INT-SEC, INT-NUR, MGAS-N2O | 4个系统 |
| 第四批 | FIRE-FAS, FIRE-SPS, FIRE-EXH, MED-OR, MED-ICU, MED-LAB | 6个系统 |
| 第五批 | HVAC-CHP, HVAC-AHU, HVAC-FCU, ELEC-EL + 5个修订文档 | 4个系统+5个补充 |
| 第六批 | PLUMB-RW, ELEC-LTG + 3个综合文档 | 2个系统+3个综合 |

## 系统完整清单（26个系统）

| 序号 | 系统ID | 系统名称 | 类别 | 优先级 |
|------|--------|----------|------|--------|
| 1 | ELEC-HV | 高压配电系统 | 电气 | P1 |
| 2 | ELEC-LV | 低压配电系统 | 电气 | P1 |
| 3 | ELEC-EPS | 应急电源系统 | 电气 | P1 |
| 4 | ELEC-UPS | 不间断电源系统 | 电气 | P1 |
| 5 | ELEC-EL | 电梯系统 | 电气 | P2 |
| 6 | ELEC-LTG | 照明系统 | 电气 | P2 |
| 7 | HVAC-CHP | 冷热源系统 | 暖通 | P1 |
| 8 | HVAC-AHU | 空调机组系统 | 暖通 | P2 |
| 9 | HVAC-FCU | 风机盘管系统 | 暖通 | P3 |
| 10 | PLUMB-DWS | 生活给水系统 | 给排水 | P2 |
| 11 | PLUMB-HWS | 生活热水系统 | 给排水 | P3 |
| 12 | PLUMB-SAN | 污废水系统 | 给排水 | P2 |
| 13 | PLUMB-RW | 雨水排水系统 | 给排水 | P3 |
| 14 | MGAS-O2 | 医用氧气系统 | 医用气体 | P1 |
| 15 | MGAS-VAC | 医用负压系统 | 医用气体 | P1 |
| 16 | MGAS-AIR | 医用压缩空气系统 | 医用气体 | P1 |
| 17 | MGAS-N2O | 笑气系统 | 医用气体 | P2 |
| 18 | FIRE-FAS | 火灾自动报警系统 | 消防 | P1 |
| 19 | FIRE-SPS | 自动喷水灭火系统 | 消防 | P1 |
| 20 | FIRE-EXH | 防排烟系统 | 消防 | P1 |
| 21 | INT-BA | 楼宇自动化系统 | 智能化 | P2 |
| 22 | INT-SEC | 安防系统 | 智能化 | P2 |
| 23 | INT-NUR | 护理呼叫系统 | 智能化 | P2 |
| 24 | MED-OR | 手术室净化系统 | 医疗环境 | P1 |
| 25 | MED-ICU | ICU净化系统 | 医疗环境 | P1 |
| 26 | MED-LAB | 检验科通风系统 | 医疗环境 | P2 |

## 补充/修订文档清单

| 文档名称 | 批次 | 描述 |
|----------|------|------|
| Seasonal_Control_Advanced | 第五批修订 | HVAC季节切换高级控制策略 |
| Fresh_Air_Distribution_System | 第五批修订 | FCU新风分配系统设计 |
| Fire_Elevator_Base_Station | 第五批修订 | 消防电梯基站位置规范 |
| CHP_Fire_Interlock | 第五批修订 | 冷热源与消防联动规范 |
| Condensate_Drain_System | 第五批修订 | FCU冷凝水排放系统 |
| System_Dependency_Matrix | 第六批 | 系统间依赖关系总图 |
| Cross_System_Scenarios | 第六批 | 跨系统联动场景汇总 |
| Data_Point_Statistics | 第六批 | 数据点统计与分类 |

---

**全部内容输出完毕。** 如需任何补充、修改或进一步细化，请随时告知。

---