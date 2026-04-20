## 🧑‍💻 User


你卡在了【parent_system: HVAC-CHW / HVAC-HW
 child_systems:
 - HVAC-FCU

 design_standards:
 - GB 50736-2012 民用建筑供暖通风与空气调节设计规范
 - GB 51039-2014 综合医院建筑设计规范
 - WS/】，继续输出

---
## 🤖 Assistant


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

**下一批次预告：** Batch 2 将输出电气系统（ELEC-HV、ELEC-LV-MAIN、ELEC-EPS）和医疗气体核心系统（MGAS-O2、MGAS-VAC、MGAS-AIR、MGAS-N2O）。

请确认第一批次第三版内容后，我将继续输出第二批次。

---