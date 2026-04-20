# Agent-01 系统拓扑建模师 - 第四批次：消防系统 + 医疗专业系统

## 第四批次：消防系统 + 医疗专业系统（6个系统）

---

# 消防系统（3个系统）

## 系统 4.1: FIRE-FAS 火灾自动报警系统

```yaml
System_Topology:

  # ========================================
  # IDENTITY SECTION - 系统标识
  # ========================================
  identity:
    system_id: FIRE-FAS
    system_name: 火灾自动报警系统
    system_name_en: Fire Alarm System
    system_category: FIRE
    system_type: 消防-报警
    priority_level: P0-LIFE_SAFETY
  
    description: |
      医院火灾自动报警系统，是保障人员生命和财产安全的核心系统。
      系统自动探测火灾信号，发出报警并联动相关消防设施。
      采用集中报警控制系统，设置消防控制室进行24小时监控。
      联动控制包括：消防广播、消防电话、防排烟、消防电梯、
      非消防电源切断、防火门/卷帘、消防水系统等。
    
    design_basis:
      system_type: 集中报警系统（一类高层公共建筑）
      protection_level: 一级
      detection_coverage: 全院所有区域
      response_time: {value: "<30", unit: s, note: "探测到报警"}
      false_alarm_prevention: 双探测器确认/智能算法
    
    child_systems:
      - FIRE-SPS   # 消防给水系统
      - FIRE-EXH   # 防排烟系统
    
    linked_systems:
      - INT-BA: 空调联动
      - INT-SEC: 门禁联动
      - ELEC-LV-MAIN: 非消防电源切断
      - ELEC-EPS: 消防电源保障
  
    design_standards:
      - GB 50116-2013 火灾自动报警系统设计规范
      - GB 50016-2014 建筑设计防火规范（2018年版）
      - GB 50898-2013 细水雾灭火系统技术规范
      - GB 51039-2014 综合医院建筑设计规范
      - GB 25506-2010 消防控制室通用技术要求
  
    version: 1.0
    last_updated: 2024

  # ========================================
  # BOUNDARY SECTION - 系统边界
  # ========================================
  boundary:
  
    inputs:
      - boundary_id: FIRE-FAS_IN_001
        name: 火灾探测信号
        from_system: 各类火灾探测器
        medium: SIGNAL-SLC
        description: 回路总线信号
      
      - boundary_id: FIRE-FAS_IN_002
        name: 手动报警信号
        from_system: 手动报警按钮
        medium: SIGNAL-SLC
      
      - boundary_id: FIRE-FAS_IN_003
        name: 消防设施反馈
        from_system: 消防联动设施
        medium: SIGNAL-SLC/IO
        description: 水流指示器、压力开关、阀门状态等
      
      - boundary_id: FIRE-FAS_IN_004
        name: 消防电源
        from_system: ELEC-EPS
        medium: ELEC-LV
        parameters:
          voltage: {value: 220/380, unit: V}
          backup: 消防专用UPS/蓄电池
        
    outputs:
      - boundary_id: FIRE-FAS_OUT_001
        name: 火灾报警信号
        to_system: 消防广播/声光报警
        medium: SIGNAL-AUDIO/LIGHT
      
      - boundary_id: FIRE-FAS_OUT_002
        name: 联动控制信号
        to_system: 各消防联动设施
        medium: SIGNAL-SLC/IO
      
      - boundary_id: FIRE-FAS_OUT_003
        name: 城市消防远程监控
        to_system: 119指挥中心
        medium: SIGNAL-NET
        protocol: GA 503协议

  # ========================================
  # NODES SECTION - 节点定义
  # ========================================
  nodes:

    source_nodes:
  
      - node_id: FIRE-FAS_SRC_SMOKE_DETECTOR
        node_name: 点型感烟探测器
        node_name_en: Photoelectric Smoke Detector
        node_type: Source_Node
        node_category: SRC
      
        function: 探测烟雾浓度，早期发现火灾
        medium_in: SMOKE
        medium_out: SIGNAL-SLC
      
        is_boundary_input: true
      
        multiplicity: multiple
        instance_pattern: FIRE-FAS_SRC_SMOKE_{Building}_{Floor}_{Zone}_{Seq}
        typical_quantity: {value: "2000-5000", unit: "只", note: "大型医院"}
      
        equipment_parameters:
          type: 智能点型光电感烟探测器
          sensitivity: 
            levels: [1, 2, 3]
            adjustable: true
          technology: 光电散射型
          coverage: 
            general: {value: 60, unit: "m²", note: "一般场所"}
            corridor: {value: 15, unit: m, note: "走道长度"}
          response_time: {value: "<20", unit: s}
          mtbf: {value: ">100000", unit: h}
          power: 总线供电
          address: 可编址
          indicator: LED状态灯
          self_diagnosis: 污染/故障自检
        
        installation_requirements:
          height: 
            general: "吊顶下0.3m内"
            beam: "梁间设置规则"
          spacing:
            max: {value: 11.2, unit: m, note: "一般场所"}
            edge: {value: 5.6, unit: m, note: "距墙边"}
          avoid:
            - 空调送风口附近1.5m
            - 蒸汽/烟雾发生处
            - 潮湿/粉尘/腐蚀环境
          
        control_points:
          status:
            - point_id: SMOKE_ALARM
              point_name: 烟感报警
              point_type: DI
            - point_id: SMOKE_FAULT
              point_name: 烟感故障
              point_type: DI
            - point_id: SMOKE_CONTAMINATION
              point_name: 烟感污染
              point_type: DI
      
        location_hint:
          space_type: 所有室内空间
          exclusions: [卫生间, 淋浴间, 游泳池]
          special: |
            手术室：采用极早期烟雾探测
            配电室：采用吸气式烟感

      - node_id: FIRE-FAS_SRC_HEAT_DETECTOR
        node_name: 点型感温探测器
        node_name_en: Heat Detector
        node_type: Source_Node
        node_category: SRC
      
        function: 探测环境温度异常升高
        medium_in: HEAT
        medium_out: SIGNAL-SLC
      
        multiplicity: multiple
      
        equipment_parameters:
          types:
            fixed_temp:
              description: 定温探测器
              threshold: {value: 57, unit: ℃, note: "一级"}
              application: 厨房/锅炉房
            rate_of_rise:
              description: 差温探测器
              sensitivity: {value: 8, unit: "℃/min"}
              application: 一般场所
            combined:
              description: 差定温复合探测器
              application: 推荐使用
          coverage: {value: 20, unit: "m²", note: "一般场所"}
        
        installation_requirements:
          application:
            - 厨房
            - 锅炉房
            - 发电机房
            - 配电室（作为感烟补充）
            - 车库
          
        location_hint:
          space_type: 高温/烟雾干扰场所

      - node_id: FIRE-FAS_SRC_BEAM_DETECTOR
        node_name: 线型光束感烟探测器
        node_name_en: Beam Smoke Detector
        node_type: Source_Node
        node_category: SRC
      
        function: 大空间烟雾探测
        medium_in: SMOKE
        medium_out: SIGNAL-SLC
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 反射式线型光束感烟探测器
          range: {value: "10-100", unit: m}
          height: {value: "6-12", unit: m, note: "安装高度"}
          application:
            - 中庭
            - 大厅
            - 地下车库
          components:
            - 发射器/接收器一体机
            - 反射板
          
        location_hint:
          space_type: 大空间
          height: ">6m"

      - node_id: FIRE-FAS_SRC_ASPIRATING
        node_name: 吸气式烟雾探测器
        node_name_en: Aspirating Smoke Detector
        node_type: Source_Node
        node_category: SRC
      
        function: 极早期烟雾探测
        medium_in: AIR_SAMPLE
        medium_out: SIGNAL-SLC
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 激光吸气式烟雾探测系统
          sensitivity: {value: "0.001-20", unit: "%obs/m"}
          sampling:
            pipe_length: {value: "<200", unit: m}
            holes: {value: "≤25", unit: "个/区"}
          response_time: {value: "<60", unit: s}
          application:
            - 数据中心/机房
            - 贵重设备房
            - 洁净室
            - 手术室（部分）
          
        location_hint:
          space_type: 关键设备区域
          note: 对烟雾极敏感场所

      - node_id: FIRE-FAS_SRC_MANUAL_CALL_POINT
        node_name: 手动报警按钮
        node_name_en: Manual Call Point
        node_type: Source_Node
        node_category: SRC
      
        function: 人工发现火灾时手动报警
        medium_in: USER_INPUT
        medium_out: SIGNAL-SLC
      
        multiplicity: multiple
        instance_pattern: FIRE-FAS_SRC_MCP_{Building}_{Floor}_{Zone}
      
        equipment_parameters:
          type: 可复位手动报警按钮
          operation: 按下玻璃/按钮触发
          reset: 专用钥匙复位
          indicator: LED指示灯
          address: 可编址
        
        installation_requirements:
          location:
            - 各防火分区出入口
            - 楼梯口
            - 走道（间距≤30m）
            - 消防电梯前室
          height: {value: "1.3-1.5", unit: m, note: "距地高度"}
          marking: 明显标识
        
        control_points:
          status:
            - point_id: MCP_ALARM
              point_name: 手报报警
              point_type: DI
              priority: 高于自动探测
      
        location_hint:
          space_type: 走道/出口
          spacing: "≤30m"

      - node_id: FIRE-FAS_SRC_WATER_FLOW
        node_name: 水流指示器
        node_name_en: Water Flow Indicator
        node_type: Source_Node
        node_category: SRC
      
        function: 检测喷淋系统水流动作
        medium_in: WATER_FLOW
        medium_out: SIGNAL-SLC/IO
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 法兰式水流指示器
          size: {value: "DN50-DN200", unit: mm}
          action_flow: {value: 15, unit: "L/min"}
          delay: {value: "2-90", unit: s, note: "可调延时"}
          output: 无源触点
        
        installation:
          location: 每个楼层喷淋管道
          orientation: 水平安装
        
        control_points:
          status:
            - point_id: WFI_ACTION
              point_name: 水流动作
              point_type: DI
              meaning: 喷淋已启动
      
        location_hint:
          space_type: 管井/吊顶内

      - node_id: FIRE-FAS_SRC_PRESSURE_SWITCH
        node_name: 压力开关
        node_name_en: Pressure Switch
        node_type: Source_Node
        node_category: SRC
      
        function: 检测消防管道压力变化
        medium_in: WATER_PRESSURE
        medium_out: SIGNAL-IO
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 报警阀组压力开关
          setting: 系统工作压力
          output: 无源触点
          application:
            - 湿式报警阀组
            - 预作用报警阀组
            - 雨淋阀组
          
        control_points:
          status:
            - point_id: PS_ACTION
              point_name: 压力开关动作
              point_type: DI
              meaning: 报警阀已开启
      
        location_hint:
          space_type: 消防水泵房

      - node_id: FIRE-FAS_SRC_VALVE_POSITION
        node_name: 阀门位置开关
        node_name_en: Valve Position Switch
        node_type: Source_Node
        node_category: SRC
      
        function: 监视消防阀门开闭状态
        medium_in: VALVE_POSITION
        medium_out: SIGNAL-SLC/IO
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 信号阀位置开关
          monitored_valves:
            - 消防水泵出口阀
            - 分区控制阀
            - 水箱出水阀
            - 室内消火栓阀
          output: 无源触点（常开/常闭）
          alarm: 阀门关闭时报警
        
        control_points:
          status:
            - point_id: VALVE_CLOSED
              point_name: 阀门关闭报警
              point_type: DI
              normal: 开（无报警）
      
        location_hint:
          space_type: 消防水泵房/管井

    distribution_nodes:
  
      - node_id: FIRE-FAS_DST_LOOP_CARD
        node_name: 回路卡/总线模块
        node_name_en: Loop Card / SLC Module
        node_type: Distribution_Node
        node_subtype: CTR
        node_category: DST
      
        function: 管理回路设备，信号采集和传输
        medium_in: SIGNAL-SLC
        medium_out: SIGNAL-INTERNAL
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 双回路卡/单回路卡
          capacity: {value: "198-250", unit: "点/回路"}
          cable: 阻燃双绞线（树形/环形）
          isolation: 短路隔离器保护
          communication: 数字总线通讯
        
        location_hint:
          space_type: 消防控制室
          position: 安装在火灾报警控制器内

      - node_id: FIRE-FAS_DST_FIRE_ALARM_PANEL
        node_name: 火灾报警控制器
        node_name_en: Fire Alarm Control Panel
        node_type: Distribution_Node
        node_subtype: CTR
        node_category: DST
      
        function: 火灾报警系统核心控制设备
        medium_in: SIGNAL-INTERNAL
        medium_out: SIGNAL-SLC/IO
      
        equipment_parameters:
          type: 集中火灾报警控制器
          capacity:
            loops: {value: "≥8", unit: "回路"}
            points: {value: "≥1584", unit: "点"}
          display:
            lcd: 大屏液晶显示
            led: 各类状态指示
          operation:
            keyboard: 汉字输入
            printer: 内置/外置打印机
          power:
            main: 220V AC
            backup: 24V DC蓄电池
            backup_time: {value: ">24", unit: h}
          communication:
            network: CAN总线/以太网
            remote: GA 503协议
          features:
            - 火警优先
            - 二次报警确认
            - 故障诊断
            - 历史记录
            - 联动编程
          
        control_points:
          status:
            - point_id: FACP_FIRE_ALARM
              point_name: 火警状态
              point_type: DI
            - point_id: FACP_FAULT
              point_name: 系统故障
              point_type: DI
            - point_id: FACP_SUPERVISORY
              point_name: 监管异常
              point_type: DI
            - point_id: FACP_AC_FAIL
              point_name: 主电故障
              point_type: DI
            - point_id: FACP_BATTERY_LOW
              point_name: 备电低
              point_type: DI
          commands:
            - point_id: FACP_SILENCE
              point_name: 消音
              point_type: DO
            - point_id: FACP_RESET
              point_name: 复位
              point_type: DO
      
        location_hint:
          space_type: 消防控制室
          position: 主控制台
          note: 24小时有人值班

      - node_id: FIRE-FAS_DST_LINKAGE_CONTROLLER
        node_name: 消防联动控制器
        node_name_en: Fire Linkage Controller
        node_type: Distribution_Node
        node_subtype: CTR
        node_category: DST
      
        function: 控制各类消防联动设施
        medium_in: SIGNAL-INTERNAL
        medium_out: SIGNAL-SLC/IO
      
        equipment_parameters:
          type: 消防联动控制器（可与报警控制器一体）
          controlled_devices:
            - 消防水泵（启动）
            - 防排烟风机（启动）
            - 防火门/卷帘（关闭）
            - 消防电梯（迫降）
            - 非消防电源（切断）
            - 消防广播（启动）
            - 疏散指示（启动）
          control_method:
            automatic: 报警联动自动控制
            manual: 手动直接控制
            remote: 远程多线制控制
          power: 消防专用电源
        
        control_logic:
          fire_confirmation:
            method: 两个独立探测器报警确认
            or: 一个探测器+手报
            action: 启动联动程序
          linkage_sequence:
            - step: 1
              action: 发出火灾报警声光
            - step: 2
              action: 切断非消防电源
            - step: 3
              action: 迫降消防电梯
            - step: 4
              action: 关闭防火门/卷帘
            - step: 5
              action: 启动排烟风机
            - step: 6
              action: 启动消防广播
            - step: 7
              action: 等待水流信号启动消防泵
      
        location_hint:
          space_type: 消防控制室

      - node_id: FIRE-FAS_DST_GRAPHIC_TERMINAL
        node_name: 图形显示装置
        node_name_en: Graphic Display Terminal
        node_type: Distribution_Node
        node_subtype: DIS
        node_category: DST
      
        function: 图形化显示火灾报警和设备状态
        medium_in: SIGNAL-ETH
        medium_out: DISPLAY
      
        equipment_parameters:
          type: 消防图形显示系统
          display: 大屏显示器/拼接屏
          software: CRT图形软件
          features:
            - 建筑平面图显示
            - 报警点位置标注
            - 联动设备状态
            - 历史记录查询
            - 打印输出
          integration: 与火灾报警控制器通讯
        
        location_hint:
          space_type: 消防控制室
          position: 值班台前方

      - node_id: FIRE-FAS_DST_FIRE_PHONE
        node_name: 消防电话系统
        node_name_en: Fire Telephone System
        node_type: Distribution_Node
        node_subtype: COM
        node_category: DST
      
        function: 火灾时的应急通讯
        medium_in: SIGNAL-TEL
        medium_out: SIGNAL-TEL
      
        equipment_parameters:
          type: 消防电话总机
          capacity: {value: "≥50", unit: "门"}
          extensions:
            - 消防电话分机（消防控制室）
            - 消防电话插孔（各层）
            - 手持消防电话
          features:
            - 优先呼叫
            - 群呼功能
            - 录音功能
          
        installation:
          locations:
            - 消防控制室
            - 消防水泵房
            - 发电机房
            - 配电室
            - 防排烟机房
            - 消防电梯轿厢
            - 各层手报旁
          
        location_hint:
          space_type: 消防控制室/各消防设备房

      - node_id: FIRE-FAS_DST_FIRE_BROADCAST
        node_name: 消防广播系统
        node_name_en: Emergency Broadcast System
        node_type: Distribution_Node
        node_subtype: COM
        node_category: DST
      
        function: 火灾时的人员疏散广播
        medium_in: SIGNAL-AUDIO
        medium_out: SIGNAL-AUDIO
      
        equipment_parameters:
          type: 消防广播控制器
          power: {value: "≥500", unit: W}
          zones: 按防火分区/楼层分区
          speakers:
            type: 扬声器/吸顶喇叭
            power: {value: "3-10", unit: W}
            coverage: {value: 15, unit: m, note: "服务半径"}
          features:
            - 背景音乐平时播放
            - 火灾时强制切换
            - 分区广播
            - 预录疏散语音
            - 话筒直接广播
          priority: 消防广播最高优先级
        
        control_logic:
          fire_activation:
            trigger: 火灾确认
            action:
              - 自动启动消防广播
              - 切断背景音乐
              - 播放疏散录音
              - 可手动话筒广播
          broadcast_sequence:
            - 首先：着火层及相邻上下层
            - 随后：全楼广播
          
        location_hint:
          space_type: 消防控制室/所有公共区域

      - node_id: FIRE-FAS_DST_OUTPUT_MODULE
        node_name: 输出模块
        node_name_en: Output Module
        node_type: Distribution_Node
        node_subtype: CTR
        node_category: DST
      
        function: 联动控制输出
        medium_in: SIGNAL-SLC
        medium_out: SIGNAL-IO
      
        multiplicity: multiple
      
        equipment_parameters:
          types:
            single_output:
              description: 单输出模块
              outputs: 1
            multi_output:
              description: 多输出模块
              outputs: 4-8
          output_type:
            - 无源触点（常开/常闭）
            - 有源DC24V
          capacity: {value: 2, unit: A}
          application:
            - 防火门释放
            - 防火卷帘控制
            - 排烟阀开启
            - 非消防电源切断
            - 空调联动
          
        location_hint:
          space_type: 被控设备附近

      - node_id: FIRE-FAS_DST_INPUT_MODULE
        node_name: 输入模块
        node_name_en: Input Module
        node_type: Distribution_Node
        node_subtype: MON
        node_category: DST
      
        function: 采集设备反馈信号
        medium_in: SIGNAL-IO
        medium_out: SIGNAL-SLC
      
        multiplicity: multiple
      
        equipment_parameters:
          types:
            single_input:
              outputs: 1
            multi_input:
              outputs: 4-8
          input_type: 无源触点
          monitoring:
            - 水泵运行反馈
            - 风机运行反馈
            - 阀门位置反馈
            - 防火门状态
          
        location_hint:
          space_type: 被监视设备附近

    sink_nodes:
  
      - node_id: FIRE-FAS_SNK_SOUNDER_BEACON
        node_name: 火灾声光报警器
        node_name_en: Sounder Beacon
        node_type: Sink_Node
        node_category: SNK
      
        function: 发出火灾声光报警
        medium_in: SIGNAL-SLC
        medium_out: SOUND/LIGHT
      
        is_boundary_output: true
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 编址式火灾声光警报器
          sound:
            level: {value: "≥85", unit: dB}
            pattern: 脉冲式
          light:
            color: 红色
            flash: 频闪
          power: 总线供电/本地DC24V
        
        installation:
          location:
            - 走道
            - 大厅
            - 楼梯口
            - 出入口
          height: {value: "2.2-2.5", unit: m}
          spacing: {value: "≤25", unit: m}
        
        location_hint:
          space_type: 走道/公共区域

      - node_id: FIRE-FAS_SNK_EXIT_SIGN
        node_name: 消防应急疏散指示
        node_name_en: Emergency Exit Sign
        node_type: Sink_Node
        node_category: SNK
      
        function: 指示疏散方向和出口
        medium_in: ELEC-LV / SIGNAL-SLC
        medium_out: LIGHT
      
        is_boundary_output: true
      
        multiplicity: multiple
      
        equipment_parameters:
          types:
            exit_sign:
              description: 安全出口标志灯
              location: 安全出口上方
            direction_sign:
              description: 疏散指示标志灯
              location: 走道两侧
            floor_embedded:
              description: 地埋疏散指示灯
              location: 地面
          features:
            - 常亮指示
            - 应急供电（≥90分钟）
            - 智能疏散（可选）
          power:
            main: AC220V
            backup: 内置蓄电池
          
        installation:
          exit_sign: 出口上方0.1m
          direction_sign:
            height: {value: "≤1.0", unit: m}
            spacing: {value: "≤10", unit: m}
          
        location_hint:
          space_type: 走道/出口

      - node_id: FIRE-FAS_SNK_CONTROL_ROOM
        node_name: 消防控制室
        node_name_en: Fire Control Room
        node_type: Sink_Node
        node_category: SNK
      
        function: 消防系统监控和指挥中心
        medium_in: SIGNAL-SLC/ETH
        medium_out: COMMAND
      
        is_boundary_output: true
      
        equipment_parameters:
          location: 首层或地下一层（便于人员进出）
          area: {value: "≥25", unit: "m²"}
          equipment:
            - 火灾报警控制器
            - 联动控制器
            - 图形显示装置
            - 消防电话总机
            - 消防广播控制器
            - 消防设备电源
            - 手动直接控制盘
            - 消防值班电话（119直通）
          environment:
            - 独立房间
            - 耐火极限≥2h
            - 设置独立空调
            - 24小时有人值班
          documentation:
            - 值班记录
            - 设备台账
            - 操作规程
            - 应急预案
          
        location_hint:
          space_type: 消防控制室
          floor: 1F或B1
          access: 直通室外

      - node_id: FIRE-FAS_SNK_REMOTE_CENTER
        node_name: 城市消防远程监控中心
        node_name_en: Remote Fire Monitoring Center
        node_type: Sink_Node
        node_category: SNK
      
        function: 远程接收火灾报警信息
        medium_in: SIGNAL-NET
        medium_out: 119指挥调度
      
        is_boundary_output: true
      
        equipment_parameters:
          protocol: GA 503消防远程监控系统传输协议
          transmitter: 用户信息传输装置
          data_transmitted:
            - 火灾报警信息
            - 故障信息
            - 联动设备状态
            - 消防水压/水位
          
        location_hint:
          space_type: 外部系统

  # ========================================
  # EDGES SECTION - 边/连接定义
  # ========================================
  edges:

    detection_edges:
      - edge_id: FIRE-FAS_EDGE_001
        edge_name: 探测器至回路卡
        edge_type: CAB
        from_node: FIRE-FAS_SRC_SMOKE_DETECTOR
        to_node: FIRE-FAS_DST_LOOP_CARD
        direction: bidirectional
        medium: SIGNAL-SLC
        cable_parameters:
          type: ZR-RVS 2×1.5
          note: 阻燃双绞线
        multiplicity: multiple
      
      - edge_id: FIRE-FAS_EDGE_002
        edge_name: 手报至回路卡
        edge_type: CAB
        from_node: FIRE-FAS_SRC_MANUAL_CALL_POINT
        to_node: FIRE-FAS_DST_LOOP_CARD
        direction: bidirectional
        medium: SIGNAL-SLC
        multiplicity: multiple

    control_edges:
      - edge_id: FIRE-FAS_EDGE_011
        edge_name: 回路卡至报警控制器
        edge_type: INTERNAL
        from_node: FIRE-FAS_DST_LOOP_CARD
        to_node: FIRE-FAS_DST_FIRE_ALARM_PANEL
        direction: bidirectional
        medium: SIGNAL-INTERNAL
      
      - edge_id: FIRE-FAS_EDGE_012
        edge_name: 报警控制器至联动控制器
        edge_type: INTERNAL
        from_node: FIRE-FAS_DST_FIRE_ALARM_PANEL
        to_node: FIRE-FAS_DST_LINKAGE_CONTROLLER
        direction: bidirectional
        medium: SIGNAL-INTERNAL
      
      - edge_id: FIRE-FAS_EDGE_013
        edge_name: 联动控制器至输出模块
        edge_type: CAB
        from_node: FIRE-FAS_DST_LINKAGE_CONTROLLER
        to_node: FIRE-FAS_DST_OUTPUT_MODULE
        direction: unidirectional
        medium: SIGNAL-SLC
        multiplicity: multiple

    feedback_edges:
      - edge_id: FIRE-FAS_EDGE_021
        edge_name: 水流指示器至输入模块
        edge_type: CAB
        from_node: FIRE-FAS_SRC_WATER_FLOW
        to_node: FIRE-FAS_DST_INPUT_MODULE
        direction: unidirectional
        medium: SIGNAL-IO
        multiplicity: multiple

    output_edges:
      - edge_id: FIRE-FAS_EDGE_031
        edge_name: 至声光报警器
        edge_type: CAB
        from_node: FIRE-FAS_DST_LOOP_CARD
        to_node: FIRE-FAS_SNK_SOUNDER_BEACON
        direction: unidirectional
        medium: SIGNAL-SLC
        multiplicity: multiple

  # ========================================
  # TYPICAL PATHS SECTION
  # ========================================
  typical_paths:

    - path_id: FIRE-FAS_PATH_DETECTION
      path_name: 火灾探测报警路径
      path_type: DET
      description: 从探测器发现火灾到发出报警
      sequence:
        - step: 1
          node: FIRE-FAS_SRC_SMOKE_DETECTOR
          action: 探测到烟雾
          time: "0"
        - step: 2
          node: FIRE-FAS_DST_LOOP_CARD
          action: 信号采集和传输
          time: "<5秒"
        - step: 3
          node: FIRE-FAS_DST_FIRE_ALARM_PANEL
          action: 报警确认和显示
          time: "<10秒"
        - step: 4
          node: FIRE-FAS_SNK_SOUNDER_BEACON
          action: 声光报警
          time: "<15秒"
        - step: 5
          node: FIRE-FAS_SNK_CONTROL_ROOM
          action: 值班人员确认
          time: "<30秒"
      total_time: "<30秒"

    - path_id: FIRE-FAS_PATH_LINKAGE
      path_name: 消防联动控制路径
      path_type: CTR
      description: 火灾确认后的联动控制
      sequence:
        - step: 1
          node: FIRE-FAS_DST_FIRE_ALARM_PANEL
          action: 两个探测器确认火灾
        - step: 2
          node: FIRE-FAS_DST_LINKAGE_CONTROLLER
          action: 启动联动程序
        - step: 3
          node: FIRE-FAS_DST_OUTPUT_MODULE
          action: 输出控制信号
        - step: 4
          action: 各联动设备响应
          details:
            - 防火门关闭
            - 排烟风机启动
            - 消防广播启动
            - 消防电梯迫降
            - 非消防电源切断

  # ========================================
  # CONTROL LOGIC SECTION
  # ========================================
  control_logic:

    fire_confirmation:
      name: 火灾确认逻辑
      description: 防止误报的确认机制
    
      confirmation_methods:
        method_1:
          description: 同一防火分区两个探测器报警
          logic: Detector_A AND Detector_B
          note: 可以是两个烟感，或烟感+温感
        
        method_2:
          description: 一个探测器+手动报警
          logic: Detector AND Manual_Call_Point
          note: 手报优先级高
        
        method_3:
          description: 水流指示器+压力开关
          logic: Water_Flow AND Pressure_Switch
          note: 喷淋动作确认
        
      single_detector_action:
        description: 单个探测器报警
        action:
          - 发出预警信号（声音较轻）
          - 显示报警位置
          - 等待确认
        timeout: 60秒无确认则升级为火警
      
    linkage_control:
      name: 联动控制逻辑
      description: 火灾确认后的自动联动
    
      linkage_matrix:
        - trigger: 火灾确认
          action: 消防广播（着火层及相邻层）
          delay: 0秒
        
        - trigger: 火灾确认
          action: 声光报警器（着火层）
          delay: 0秒
        
        - trigger: 火灾确认
          action: 切断非消防电源（着火层）
          delay: 0秒
        
        - trigger: 火灾确认
          action: 消防电梯迫降至首层
          delay: 0秒
        
        - trigger: 火灾确认
          action: 关闭空调送回风（着火层）
          delay: 0秒
          signal_to: INT-BA
        
        - trigger: 火灾确认
          action: 开启排烟阀和排烟风机
          delay: 0秒
        
        - trigger: 火灾确认
          action: 释放防火门（保持常闭）
          delay: 0秒
        
        - trigger: 火灾确认
          action: 降落防火卷帘
          delay: 0秒（一步降）/ 二步降（有人时）
        
        - trigger: 火灾确认
          action: 门禁释放
          delay: 0秒
          signal_to: INT-SEC
        
        - trigger: 水流指示器+压力开关
          action: 启动消防水泵
          delay: 0秒
        
    manual_override:
      name: 手动优先控制
      description: 手动控制优先于自动控制
    
      direct_control:
        description: 消防控制室手动直接控制
        devices:
          - 消防水泵启停
          - 防排烟风机启停
          - 消防广播开关
          - 疏散指示控制
        method: 多线制直接控制
        note: 不经过总线，硬线直连
      
      priority: 手动 > 自动

  # ========================================
  # ALARM & PROTECTION
  # ========================================
  alarm_protection:
  
    fire_alarms:
      - alarm_id: ALM_FIRE_ALARM
        alarm_name: 火灾报警
        severity: CRITICAL
        trigger: 火灾确认条件满足
        action:
          - 声光报警
          - 启动联动
          - 通知消防控制室
          - 上传远程监控中心
        
      - alarm_id: ALM_FIRE_PRE_ALARM
        alarm_name: 火灾预警
        severity: HIGH
        trigger: 单个探测器报警
        action:
          - 预警提示
          - 等待确认
        
    system_alarms:
      - alarm_id: ALM_FAS_FAULT
        alarm_name: 系统故障
        severity: HIGH
        trigger: 设备故障/通讯故障
        action: 故障声光提示
      
      - alarm_id: ALM_FAS_POWER_FAIL
        alarm_name: 主电故障
        severity: HIGH
        trigger: AC电源失电
        action: 切换备电，报警
      
      - alarm_id: ALM_FAS_BATTERY_LOW
        alarm_name: 备电不足
        severity: MEDIUM
        trigger: 蓄电池电压低
        action: 报警，检查/更换电池

  # ========================================
  # DEPENDENCIES
  # ========================================
  dependencies:
  
    upstream_dependencies:
      - dependency_id: DEP_FIRE_POWER
        from_system: ELEC-EPS
        dependency_type: POWER_SUPPLY
        criticality: CRITICAL
        description: 消防专用电源
        backup: 蓄电池>24小时
      
    downstream_dependencies:
      - dependency_id: DEP_TO_SPS
        to_system: FIRE-SPS
        dependency_type: CONTROL
        criticality: CRITICAL
        description: 消防水泵联动控制
      
      - dependency_id: DEP_TO_EXH
        to_system: FIRE-EXH
        dependency_type: CONTROL
        criticality: CRITICAL
        description: 防排烟联动控制
      
      - dependency_id: DEP_TO_BA
        to_system: INT-BA
        dependency_type: LINKAGE
        criticality: HIGH
        description: 空调联动控制
        signal_type: 硬接点
      
      - dependency_id: DEP_TO_SEC
        to_system: INT-SEC
        dependency_type: LINKAGE
        criticality: HIGH
        description: 门禁联动控制
        signal_type: 硬接点
```

---

## 系统 4.2: FIRE-SPS 消防给水系统

```yaml
System_Topology:

  identity:
    system_id: FIRE-SPS
    system_name: 消防给水系统
    system_name_en: Fire Suppression Water System
    system_category: FIRE
    system_type: 消防-给水
    priority_level: P0-LIFE_SAFETY
  
    description: |
      医院消防给水系统，包括室内消火栓系统、自动喷水灭火系统。
      系统由消防水池、消防水泵、消防管网、消火栓、喷淋头等组成。
      设置稳压设施保持系统压力，火灾时自动或手动启动消防泵加压供水。
      医院重点区域（如资料室、配电室）可配置气体灭火系统。
  
    design_basis:
      systems:
        - 室内消火栓系统
        - 自动喷水灭火系统（湿式）
        - 气体灭火系统（重点区域）
      fire_duration: {value: 2, unit: h, note: "火灾延续时间"}
      design_flow:
        hydrant: {value: 40, unit: "L/s", note: "室内消火栓"}
        sprinkler: {value: 30, unit: "L/s", note: "自动喷水"}
      water_reserve:
        hydrant: {value: 288, unit: "m³", note: "40L/s×2h"}
        sprinkler: {value: 216, unit: "m³", note: "30L/s×1h+补充"}
        total: {value: 504, unit: "m³"}
    
    parent_system: FIRE-FAS
  
    design_standards:
      - GB 50016-2014 建筑设计防火规范
      - GB 50084-2017 自动喷水灭火系统设计规范
      - GB 50974-2014 消防给水及消火栓系统技术规范
      - GB 50370-2005 气体灭火系统设计规范
  
    version: 1.0
    last_updated: 2024

  boundary:
    inputs:
      - boundary_id: FIRE-SPS_IN_001
        name: 消防水源
        from_system: 市政给水/天然水源
        medium: WATER-FIRE
        parameters:
          source_1: 市政给水管（DN150双路）
          source_2: 消防水池储水
        
      - boundary_id: FIRE-SPS_IN_002
        name: 启泵控制信号
        from_system: FIRE-FAS
        medium: SIGNAL-IO
      
      - boundary_id: FIRE-SPS_IN_003
        name: 消防电源
        from_system: ELEC-EPS
        medium: ELEC-LV
      
    outputs:
      - boundary_id: FIRE-SPS_OUT_001
        name: 消火栓供水
        to_system: 室内消火栓
        medium: WATER-FIRE
      
      - boundary_id: FIRE-SPS_OUT_002
        name: 喷淋供水
        to_system: 自动喷水灭火系统
        medium: WATER-FIRE
      
      - boundary_id: FIRE-SPS_OUT_003
        name: 状态反馈
        to_system: FIRE-FAS
        medium: SIGNAL-IO

  nodes:

    source_nodes:
  
      - node_id: FIRE-SPS_SRC_FIRE_TANK
        node_name: 消防水池
        node_name_en: Fire Water Tank
        node_type: Source_Node
        node_category: SRC
      
        function: 储存消防用水
        medium_in: WATER-PW
        medium_out: WATER-FIRE
      
        is_boundary_input: true
      
        equipment_parameters:
          type: 钢筋混凝土水池
          volume:
            effective: {value: 504, unit: "m³"}
            actual: {value: 600, unit: "m³", note: "含死水区"}
          configuration:
            - 分为两格，各50%容量
            - 可独立使用
          water_level:
            high: {value: 3.5, unit: m}
            low: {value: 0.5, unit: m}
            effective_depth: {value: 3.0, unit: m}
          inlet:
            source: 市政给水
            pipe: DN150双路进水
            control: 浮球阀+电动阀
            refill_time: {value: 48, unit: h}
          accessories:
            - 通气管
            - 人孔
            - 溢流管
            - 排污管
            - 液位计
            - 水位标尺
          
        control_points:
          sensors:
            - point_id: TANK_LEVEL
              point_name: 消防水池液位
              point_type: AI
              unit: m
              range: [0, 4]
            - point_id: TANK_LEVEL_PERCENT
              point_name: 消防水池液位百分比
              point_type: AI
              unit: "%"
          status:
            - point_id: TANK_HIGH_LEVEL
              point_name: 高液位
              point_type: DI
            - point_id: TANK_LOW_LEVEL
              point_name: 低液位报警
              point_type: DI
              alarm: true
            - point_id: TANK_CRITICAL_LOW
              point_name: 极低液位报警
              point_type: DI
              alarm: true
              severity: CRITICAL
            
        level_settings:
          high: {value: 95, unit: "%", action: "停止补水"}
          normal: {value: "50-90", unit: "%"}
          low: {value: 30, unit: "%", action: "低液位报警"}
          critical: {value: 15, unit: "%", action: "极低液位报警"}
      
        location_hint:
          space_type: 地下室/室外地下
          floor: B2或室外
          note: 与生活水池分开设置

      - node_id: FIRE-SPS_SRC_HYDRANT_CONNECTION
        node_name: 水泵接合器
        node_name_en: Fire Department Connection
        node_type: Source_Node
        node_category: SRC
      
        function: 消防车向室内管网补水加压
        medium_in: WATER-FIRE (external)
        medium_out: WATER-FIRE
      
        equipment_parameters:
          type: 地上式/墙壁式水泵接合器
          quantity: 
            hydrant: 2组
            sprinkler: 2组
          size: DN100
          components:
            - 接口（消防车接头）
            - 止回阀
            - 安全阀
            - 闸阀
            - 放水阀
          marking: 明显标识（消火栓/喷淋）
        
        installation:
          location: 建筑外墙/室外
          distance_to_hydrant: {value: "15-40", unit: m}
          height: {value: "0.7-1.0", unit: m}
          access: 便于消防车停靠
        
        location_hint:
          space_type: 室外
          position: 靠近消防车道

    distribution_nodes:
  
      - node_id: FIRE-SPS_DST_HYDRANT_PUMP
        node_name: 消火栓泵组
        node_name_en: Fire Hydrant Pump Set
        node_type: Distribution_Node
        node_subtype: PMP
        node_category: DST
      
        function: 为室内消火栓系统加压供水
        medium_in: WATER-FIRE
        medium_out: WATER-FIRE
      
        equipment_parameters:
          type: 卧式单级离心泵
          quantity: "2台（一用一备）"
          flow: {value: 40, unit: "L/s"}
          head: {value: 100, unit: m, note: "根据建筑高度"}
          motor:
            power: {value: 75, unit: kW}
            voltage: 380V
          control:
            main: 自动（消防联动）
            backup: 手动（消防控制室/泵房）
            mechanical: 机械应急启动
          accessories:
            - 吸水管（DN200）
            - 出水管（DN150）
            - 压力表
            - 止回阀
            - 闸阀/蝶阀
            - 泄压阀
            - 软接头
          
        control_points:
          sensors:
            - point_id: HP_OUT_PRESSURE
              point_name: 消火栓泵出口压力
              point_type: AI
              unit: MPa
              range: [0, 1.6]
            - point_id: HP_CURRENT_1
              point_name: 1#泵电流
              point_type: AI
              unit: A
            - point_id: HP_CURRENT_2
              point_name: 2#泵电流
              point_type: AI
              unit: A
          status:
            - point_id: HP1_RUN
              point_name: 1#消火栓泵运行
              point_type: DI
            - point_id: HP2_RUN
              point_name: 2#消火栓泵运行
              point_type: DI
            - point_id: HP1_FAULT
              point_name: 1#泵故障
              point_type: DI
            - point_id: HP2_FAULT
              point_name: 2#泵故障
              point_type: DI
            - point_id: HP_AUTO_MODE
              point_name: 自动模式
              point_type: DI
          commands:
            - point_id: HP1_START
              point_name: 1#泵启动
              point_type: DO
            - point_id: HP2_START
              point_name: 2#泵启动
              point_type: DO
            - point_id: HP1_STOP
              point_name: 1#泵停止
              point_type: DO
              note: 仅允许手动停止，需确认火灾已扑灭
            
        start_conditions:
          automatic:
            - 消防控制室远程启动
            - 消火栓按钮启动
            - 高位水箱低液位联动
          manual:
            - 泵房现场手动启动
            - 机械应急启动
          
        protection:
          overload: 过载保护
          phase_loss: 缺相保护
          note: 消防泵不设过载停泵保护
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 消防水泵房
          floor: B1或B2

      - node_id: FIRE-SPS_DST_SPRINKLER_PUMP
        node_name: 喷淋泵组
        node_name_en: Sprinkler Pump Set
        node_type: Distribution_Node
        node_subtype: PMP
        node_category: DST
      
        function: 为自动喷水灭火系统加压供水
        medium_in: WATER-FIRE
        medium_out: WATER-FIRE
      
        equipment_parameters:
          type: 卧式单级离心泵
          quantity: "2台（一用一备）"
          flow: {value: 30, unit: "L/s"}
          head: {value: 80, unit: m}
          motor:
            power: {value: 55, unit: kW}
            voltage: 380V
          control:
            main: 自动（报警阀压力开关联动）
            backup: 手动
            mechanical: 机械应急启动
          
        control_points:
          sensors:
            - point_id: SP_OUT_PRESSURE
              point_name


继续生成 FIRE-SPS 消防给水系统：

```yaml
        control_points:
          sensors:
            - point_id: SP_OUT_PRESSURE
              point_name: 喷淋泵出口压力
              point_type: AI
              unit: MPa
              range: [0, 1.6]
            - point_id: SP_CURRENT_1
              point_name: 1#喷淋泵电流
              point_type: AI
              unit: A
            - point_id: SP_CURRENT_2
              point_name: 2#喷淋泵电流
              point_type: AI
              unit: A
          status:
            - point_id: SP1_RUN
              point_name: 1#喷淋泵运行
              point_type: DI
            - point_id: SP2_RUN
              point_name: 2#喷淋泵运行
              point_type: DI
            - point_id: SP1_FAULT
              point_name: 1#喷淋泵故障
              point_type: DI
            - point_id: SP2_FAULT
              point_name: 2#喷淋泵故障
              point_type: DI
            - point_id: SP_AUTO_MODE
              point_name: 自动模式
              point_type: DI
          commands:
            - point_id: SP1_START
              point_name: 1#喷淋泵启动
              point_type: DO
            - point_id: SP2_START
              point_name: 2#喷淋泵启动
              point_type: DO
            - point_id: SP1_STOP
              point_name: 1#喷淋泵停止
              point_type: DO
              note: 仅允许手动停止
            
        start_conditions:
          automatic:
            - 报警阀组压力开关动作
            - 消防控制室远程启动
            - 高位水箱低液位联动
          manual:
            - 泵房现场手动启动
            - 机械应急启动
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 消防水泵房
          floor: B1或B2

      - node_id: FIRE-SPS_DST_JOCKEY_PUMP
        node_name: 稳压泵组
        node_name_en: Jockey Pump Set
        node_type: Distribution_Node
        node_subtype: PMP
        node_category: DST
      
        function: 维持消防管网常备压力
        medium_in: WATER-FIRE
        medium_out: WATER-FIRE
      
        equipment_parameters:
          type: 立式多级离心泵
          quantity: "2台（一用一备）"
          flow: {value: 1, unit: "L/s"}
          head: {value: 110, unit: m, note: "略高于消防泵"}
          motor:
            power: {value: 3, unit: kW}
            voltage: 380V
          control:
            method: 压力开关自动控制
            pressure_setting:
              start: {value: 0.85, unit: MPa, note: "系统压力下限"}
              stop: {value: 1.0, unit: MPa, note: "系统压力上限"}
          tank:
            type: 气压罐
            volume: {value: 300, unit: L}
            precharge: {value: 0.6, unit: MPa}
          
        control_points:
          sensors:
            - point_id: JP_PRESSURE
              point_name: 稳压管网压力
              point_type: AI
              unit: MPa
          status:
            - point_id: JP1_RUN
              point_name: 1#稳压泵运行
              point_type: DI
            - point_id: JP2_RUN
              point_name: 2#稳压泵运行
              point_type: DI
          commands:
            - point_id: JP_AUTO
              point_name: 自动模式
              point_type: DO
            
        control_logic:
          normal_operation:
            - 管网压力<0.85MPa → 启动稳压泵
            - 管网压力>1.0MPa → 停止稳压泵
          frequent_start_alarm:
            trigger: 30分钟内启动>3次
            meaning: 可能有泄漏
            action: 报警
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 消防水泵房

      - node_id: FIRE-SPS_DST_ALARM_VALVE
        node_name: 湿式报警阀组
        node_name_en: Wet Alarm Valve Assembly
        node_type: Distribution_Node
        node_subtype: VLV
        node_category: DST
      
        function: 喷淋系统分区控制和报警
        medium_in: WATER-FIRE
        medium_out: WATER-FIRE
      
        multiplicity: multiple
        instance_pattern: FIRE-SPS_DST_ALARMVALVE_{Zone}
        typical_quantity: {value: "4-8", unit: "组", note: "按保护面积分区"}
      
        equipment_parameters:
          type: 湿式报警阀
          size: DN150
          components:
            - 报警阀本体
            - 延迟器
            - 水力警铃
            - 压力开关
            - 试验阀
            - 排水阀
            - 信号阀（阀位监视）
          coverage: {value: "≤800", unit: "个喷头/阀"}
        
        control_points:
          status:
            - point_id: AV_PRESSURE_SWITCH
              point_name: 压力开关动作
              point_type: DI
              action: 启动喷淋泵
            - point_id: AV_SIGNAL_VALVE
              point_name: 信号阀状态
              point_type: DI
              normal: 开
              alarm: 关闭时报警
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 报警阀室/消防水泵房
          note: 便于维护

      - node_id: FIRE-SPS_DST_ROOF_TANK
        node_name: 屋顶消防水箱
        node_name_en: Roof Fire Water Tank
        node_type: Distribution_Node
        node_subtype: TNK
        node_category: DST
      
        function: 提供初期灭火用水和维持系统压力
        medium_in: WATER-FIRE
        medium_out: WATER-FIRE
      
        equipment_parameters:
          type: 不锈钢组合水箱
          volume:
            effective: {value: 18, unit: "m³", note: "一类高层公建"}
            hydrant: {value: 12, unit: "m³"}
            sprinkler: {value: 6, unit: "m³"}
          installation:
            height: {value: 屋顶, note: "最高处"}
            static_pressure: 满足最不利点要求
          accessories:
            - 进水管（生活给水补水）
            - 出水管（消火栓/喷淋）
            - 溢流管
            - 排污管
            - 液位计
            - 人孔
            - 保温
          
        control_points:
          sensors:
            - point_id: ROOF_TANK_LEVEL
              point_name: 屋顶水箱液位
              point_type: AI
              unit: "%"
          status:
            - point_id: ROOF_TANK_LOW
              point_name: 低液位报警
              point_type: DI
              trigger: "<50%"
              action: 报警，联动启动消防泵
            - point_id: ROOF_TANK_EMPTY
              point_name: 空箱报警
              point_type: DI
              trigger: "<10%"
              severity: CRITICAL
            
        control_logic:
          fire_initial:
            description: 火灾初期10分钟内由屋顶水箱供水
            duration: {value: 10, unit: min}
            note: 在消防泵启动前保障供水
      
        location_hint:
          space_type: ROOF
          room_name: 屋顶消防水箱间

    sink_nodes:
  
      - node_id: FIRE-SPS_SNK_INDOOR_HYDRANT
        node_name: 室内消火栓
        node_name_en: Indoor Fire Hydrant
        node_type: Sink_Node
        node_category: SNK
      
        function: 人工灭火水源
        medium_in: WATER-FIRE
        medium_out: WATER-JET
      
        is_boundary_output: true
      
        multiplicity: multiple
        instance_pattern: FIRE-SPS_SNK_HYDRANT_{Building}_{Floor}_{Zone}
      
        equipment_parameters:
          type: 单阀单出口消火栓
          box:
            type: 明装/暗装消火栓箱
            size: {value: "800×650×240", unit: mm}
            material: 钢板/玻璃
          components:
            - 消火栓（DN65）
            - 水带（DN65×25m）
            - 水枪（19mm）
            - 消防卷盘（可选）
            - 启泵按钮
            - 指示灯
          flow: {value: 5, unit: "L/s"}
          充实水柱: {value: "≥10", unit: m}
        
        installation:
          spacing: {value: "≤30", unit: m}
          location:
            - 楼梯口
            - 走道
            - 前室
            - 公共区域
          height: {value: 1.1, unit: m, note: "栓口距地"}
        
        control_points:
          status:
            - point_id: HYDRANT_BUTTON
              point_name: 消火栓启泵按钮
              point_type: DI
              action: 启动消火栓泵
      
        location_hint:
          space_type: 走道/公共区域
          spacing: "≤30m"

      - node_id: FIRE-SPS_SNK_SPRINKLER_HEAD
        node_name: 自动喷水灭火喷头
        node_name_en: Automatic Sprinkler Head
        node_type: Sink_Node
        node_category: SNK
      
        function: 自动探测并扑灭火灾
        medium_in: WATER-FIRE
        medium_out: WATER-SPRAY
      
        is_boundary_output: true
      
        multiplicity: multiple
        instance_pattern: FIRE-SPS_SNK_SPRINKLER_{Building}_{Floor}_{Zone}_{Seq}
        typical_quantity: {value: "3000-8000", unit: "只"}
      
        equipment_parameters:
          types:
            standard:
              name: 标准喷头
              k_factor: 80
              temperature: {value: 68, unit: ℃}
              coverage: {value: "12.5", unit: "m²"}
              application: 一般区域
            concealed:
              name: 隐蔽式喷头
              feature: 装饰盖板
              application: 装修要求高
            sidewall:
              name: 边墙型喷头
              application: 走道/小房间
            extended:
              name: 扩展覆盖喷头
              coverage: {value: "36", unit: "m²"}
              application: 大空间
          action_temperature:
            general: {value: 68, unit: ℃}
            high_temp: {value: 93, unit: ℃, note: "厨房等"}
          response:
            standard: 标准响应
            fast: 快速响应（医院建议）
          
        installation:
          spacing:
            max: {value: 3.6, unit: m}
            edge: {value: 1.8, unit: m}
          clearance:
            below_ceiling: {value: "75-150", unit: mm}
            from_beam: 规范要求
          avoid:
            - 灯具下方
            - 空调风口
            - 遮挡物
          
        hazard_level:
          hospital_areas:
            light: 
              - 办公室
              - 病房
              - 门诊
            ordinary_1:
              - 走道
              - 候诊区
            ordinary_2:
              - 厨房
              - 洗衣房
              - 仓库
      
        location_hint:
          space_type: 所有室内区域
          exclusions: [配电室, 发电机房, 手术室（部分）]
          note: 配电室等采用气体灭火

      - node_id: FIRE-SPS_SNK_GAS_SUPPRESSION
        node_name: 气体灭火系统
        node_name_en: Gas Fire Suppression System
        node_type: Sink_Node
        node_category: SNK
      
        function: 不适用水灭火区域的灭火
        medium_in: GAS-EXTINGUISHANT
        medium_out: GAS-EXTINGUISHANT
      
        is_boundary_output: true
      
        multiplicity: multiple
      
        equipment_parameters:
          types:
            sevoflurane:
              name: 七氟丙烷灭火系统
              agent: HFC-227ea
              concentration: {value: "8-10", unit: "%"}
              discharge_time: {value: 10, unit: s}
              application: 
                - 数据机房
                - 配电室
                - 档案室
            ig541:
              name: IG541惰性气体灭火系统
              composition: "N2 52% + Ar 40% + CO2 8%"
              concentration: {value: "37-43", unit: "%"}
              discharge_time: {value: 60, unit: s}
              application:
                - 贵重设备房
          components:
            - 灭火剂瓶组
            - 驱动气体瓶组
            - 选择阀
            - 喷嘴
            - 集流管
            - 气体灭火控制器
            - 声光报警器
            - 紧急启停按钮
          detection:
            - 感烟探测器（双回路交叉）
            - 感温探测器
          control:
            automatic: 两个探测器确认后自动喷放
            manual: 手动启动/停止
            delay: {value: 30, unit: s, note: "人员疏散延时"}
          safety:
            - 疏散标志
            - 声光报警
            - 喷放前警告
            - 门外警告灯
          
        control_points:
          status:
            - point_id: GAS_READY
              point_name: 系统就绪
              point_type: DI
            - point_id: GAS_DISCHARGED
              point_name: 已喷放
              point_type: DI
            - point_id: GAS_LOW_PRESSURE
              point_name: 瓶组压力低
              point_type: DI
          commands:
            - point_id: GAS_MANUAL_START
              point_name: 手动启动
              point_type: DO
            - point_id: GAS_ABORT
              point_name: 紧急停止
              point_type: DO
      
        location_hint:
          space_type: 
            - 数据中心机房
            - 高低压配电室
            - 发电机房
            - UPS室
            - 档案库房
            - 贵重设备房

  edges:

    supply_edges:
      - edge_id: FIRE-SPS_EDGE_001
        edge_name: 水池至消火栓泵
        edge_type: PIP
        from_node: FIRE-SPS_SRC_FIRE_TANK
        to_node: FIRE-SPS_DST_HYDRANT_PUMP
        direction: unidirectional
        medium: WATER-FIRE
        pipe_parameters:
          material: 镀锌钢管/不锈钢管
          size: DN200
        
      - edge_id: FIRE-SPS_EDGE_002
        edge_name: 水池至喷淋泵
        edge_type: PIP
        from_node: FIRE-SPS_SRC_FIRE_TANK
        to_node: FIRE-SPS_DST_SPRINKLER_PUMP
        direction: unidirectional
        medium: WATER-FIRE
        pipe_parameters:
          size: DN150

    distribution_edges:
      - edge_id: FIRE-SPS_EDGE_011
        edge_name: 消火栓泵至竖管
        edge_type: PIP
        from_node: FIRE-SPS_DST_HYDRANT_PUMP
        to_node: FIRE-SPS_SNK_INDOOR_HYDRANT
        direction: unidirectional
        medium: WATER-FIRE
        pipe_parameters:
          size: DN150（主管）→DN100（竖管）→DN65（支管）
          pressure_class: {value: 1.6, unit: MPa}
        
      - edge_id: FIRE-SPS_EDGE_012
        edge_name: 喷淋泵至报警阀
        edge_type: PIP
        from_node: FIRE-SPS_DST_SPRINKLER_PUMP
        to_node: FIRE-SPS_DST_ALARM_VALVE
        direction: unidirectional
        medium: WATER-FIRE
      
      - edge_id: FIRE-SPS_EDGE_013
        edge_name: 报警阀至喷头
        edge_type: PIP
        from_node: FIRE-SPS_DST_ALARM_VALVE
        to_node: FIRE-SPS_SNK_SPRINKLER_HEAD
        direction: unidirectional
        medium: WATER-FIRE
        multiplicity: multiple

  typical_paths:

    - path_id: FIRE-SPS_PATH_SPRINKLER_ACTION
      path_name: 自动喷水灭火路径
      path_type: FIR
      description: 从喷头动作到灭火
      sequence:
        - step: 1
          node: FIRE-SPS_SNK_SPRINKLER_HEAD
          action: 喷头受热爆破
          trigger: 温度≥68℃
        - step: 2
          node: FIRE-SPS_DST_ALARM_VALVE
          action: 报警阀开启，水力警铃响
        - step: 3
          node: FIRE-SPS_DST_ALARM_VALVE
          action: 压力开关动作
          signal_to: FIRE-FAS
        - step: 4
          node: FIRE-SPS_DST_SPRINKLER_PUMP
          action: 喷淋泵自动启动
          time: "<30秒"
        - step: 5
          action: 持续喷水灭火
        
    - path_id: FIRE-SPS_PATH_HYDRANT_ACTION
      path_name: 消火栓灭火路径
      path_type: FIR
      description: 人工使用消火栓灭火
      sequence:
        - step: 1
          node: FIRE-SPS_SNK_INDOOR_HYDRANT
          action: 按下启泵按钮
        - step: 2
          node: FIRE-SPS_DST_HYDRANT_PUMP
          action: 消火栓泵启动
        - step: 3
          node: FIRE-SPS_SNK_INDOOR_HYDRANT
          action: 打开消火栓阀门，使用水带灭火

  control_logic:

    sprinkler_pump_control:
      name: 喷淋泵启动控制
      description: 多条件联动启动
    
      start_conditions:
        condition_1:
          trigger: 压力开关动作
          priority: 1
          response: 自动启动
        condition_2:
          trigger: 消防控制室远程启动
          priority: 2
          response: 手动启动
        condition_3:
          trigger: 屋顶水箱低液位
          priority: 3
          response: 联动启动
        condition_4:
          trigger: 泵房现场手动
          priority: 4
          response: 就地启动
        
      stop_control:
        method: 仅允许手动停止
        location: 消防控制室/泵房
        confirmation: 确认火灾已扑灭
        note: 消防泵不设自动停止
      
    hydrant_pump_control:
      name: 消火栓泵启动控制
    
      start_conditions:
        condition_1:
          trigger: 消火栓按钮启动
          priority: 1
        condition_2:
          trigger: 消防控制室远程启动
          priority: 2
        condition_3:
          trigger: 屋顶水箱低液位
          priority: 3
        
    jockey_pump_control:
      name: 稳压泵自动控制
    
      logic:
        start: 系统压力 < 0.85MPa
        stop: 系统压力 > 1.0MPa
        alternation: 两台泵轮换运行
      
      alarm:
        frequent_start:
          threshold: 30分钟内启动>3次
          meaning: 系统可能泄漏
          action: 报警
        
    gas_suppression_control:
      name: 气体灭火控制
    
      detection:
        first_detector: 预警
        second_detector: 确认，进入30秒延时
      
      sequence:
        - step: 1
          action: 两个探测器报警确认
        - step: 2
          action: 发出声光报警"即将喷放"
        - step: 3
          action: 关闭防护区空调/通风
        - step: 4
          action: 关闭防护区门窗
        - step: 5
          action: 30秒延时倒计时
        - step: 6
          action: 延时结束，喷放灭火剂
        - step: 7
          action: 喷放完成，门外亮"禁止入内"灯
        
      abort:
        trigger: 紧急停止按钮
        action: 中止喷放程序
        window: 延时期间内有效

  alarm_protection:

    system_alarms:
      - alarm_id: ALM_TANK_LOW
        alarm_name: 消防水池低液位
        severity: HIGH
        trigger: 液位<30%
        action: 检查补水
      
      - alarm_id: ALM_TANK_CRITICAL
        alarm_name: 消防水池极低液位
        severity: CRITICAL
        trigger: 液位<15%
        action: 紧急补水
      
      - alarm_id: ALM_PUMP_FAULT
        alarm_name: 消防泵故障
        severity: CRITICAL
        trigger: 泵故障信号
        action: 检修/切换备用泵
      
      - alarm_id: ALM_VALVE_CLOSED
        alarm_name: 信号阀关闭
        severity: HIGH
        trigger: 阀门位置反馈为关
        action: 检查并开启阀门
      
      - alarm_id: ALM_JOCKEY_FREQUENT
        alarm_name: 稳压泵频繁启动
        severity: MEDIUM
        trigger: 30分钟内启动>3次
        action: 检查系统泄漏

  dependencies:
  
    upstream_dependencies:
      - dependency_id: DEP_SPS_WATER
        from_system: 市政给水/消防水池
        dependency_type: WATER_SUPPLY
        criticality: CRITICAL
      
      - dependency_id: DEP_SPS_POWER
        from_system: ELEC-EPS
        dependency_type: POWER_SUPPLY
        criticality: CRITICAL
        backup: 双电源末端切换
      
      - dependency_id: DEP_SPS_FAS
        from_system: FIRE-FAS
        dependency_type: CONTROL
        criticality: HIGH
        description: 接收启泵信号
      
    downstream_dependencies:
      - dependency_id: DEP_TO_FAS_FEEDBACK
        to_system: FIRE-FAS
        dependency_type: FEEDBACK
        criticality: HIGH
        description: 泵运行/阀门状态反馈
```

---

## 系统 4.3: FIRE-EXH 防排烟系统

```yaml
System_Topology:

  identity:
    system_id: FIRE-EXH
    system_name: 防排烟系统
    system_name_en: Smoke Control System
    system_category: FIRE
    system_type: 消防-防排烟
    priority_level: P0-LIFE_SAFETY
  
    description: |
      医院防排烟系统，用于火灾时排除烟气、保障疏散通道安全。
      包括机械排烟系统和机械加压送风系统。
      排烟系统：将烟气排出建筑，降低烟气浓度。
      加压送风：对楼梯间、前室加压，阻止烟气进入。
      系统与火灾报警系统联动，自动或手动启动。
    
    design_basis:
      smoke_exhaust:
        exhaust_volume: {value: 60, unit: "次/h", note: "换气次数"}
        exhaust_temp: {value: 280, unit: ℃, note: "排烟风机耐温"}
        smoke_zone: {value: "≤500", unit: "m²", note: "防烟分区"}
      pressurization:
        stairwell: {value: "40-50", unit: Pa, note: "楼梯间正压"}
        vestibule: {value: "25-30", unit: Pa, note: "前室正压"}
        air_velocity: {value: "≥0.7", unit: "m/s", note: "门洞风速"}
  
    parent_system: FIRE-FAS
  
    design_standards:
      - GB 51251-2017 建筑防烟排烟系统技术标准
      - GB 50016-2014 建筑设计防火规范
  
    version: 1.0
    last_updated: 2024

  boundary:
    inputs:
      - boundary_id: FIRE-EXH_IN_001
        name: 联动控制信号
        from_system: FIRE-FAS
        medium: SIGNAL-IO
      
      - boundary_id: FIRE-EXH_IN_002
        name: 消防电源
        from_system: ELEC-EPS
        medium: ELEC-LV
      
      - boundary_id: FIRE-EXH_IN_003
        name: 新风/室外空气
        from_system: ATMOSPHERE
        medium: AIR-OA
      
    outputs:
      - boundary_id: FIRE-EXH_OUT_001
        name: 排出烟气
        to_system: ATMOSPHERE
        medium: AIR-SMOKE
      
      - boundary_id: FIRE-EXH_OUT_002
        name: 状态反馈
        to_system: FIRE-FAS
        medium: SIGNAL-IO

  nodes:

    source_nodes:
  
      - node_id: FIRE-EXH_SRC_FRESH_AIR
        node_name: 室外新风取风口
        node_name_en: Fresh Air Intake
        node_type: Source_Node
        node_category: SRC
      
        function: 加压送风系统的新风入口
        medium_in: AIR-OA
        medium_out: AIR-FA
      
        is_boundary_input: true
      
        equipment_parameters:
          type: 防雨百叶风口
          location: 室外/屋顶
          requirements:
            - 远离排烟口（≥10m）
            - 远离污染源
            - 避免受火焰威胁
          protection: 防雨、防虫网
        
        location_hint:
          space_type: 室外
          position: 建筑外墙/屋顶

    distribution_nodes:
  
      - node_id: FIRE-EXH_DST_EXHAUST_FAN
        node_name: 排烟风机
        node_name_en: Smoke Exhaust Fan
        node_type: Distribution_Node
        node_subtype: FAN
        node_category: DST
      
        function: 抽排火灾烟气
        medium_in: AIR-SMOKE
        medium_out: AIR-SMOKE
      
        multiplicity: multiple
        instance_pattern: FIRE-EXH_DST_EXHAUSTFAN_{Zone}
      
        equipment_parameters:
          type: 轴流式排烟风机/离心式排烟风机
          configuration: 单速/双速
          flow:
            design: {value: 30000, unit: "m³/h", note: "典型单台"}
            reserve: 20%
          pressure: {value: 600, unit: Pa}
          motor:
            power: {value: 22, unit: kW}
            protection: IP55
          temperature:
            rated: {value: 280, unit: ℃}
            duration: {value: 0.5, unit: h}
          accessories:
            - 排烟防火阀（280℃熔断）
            - 软接头
            - 止回阀
            - 消声器
          
        control_points:
          status:
            - point_id: SEF_RUN
              point_name: 排烟风机运行
              point_type: DI
            - point_id: SEF_FAULT
              point_name: 排烟风机故障
              point_type: DI
            - point_id: SEF_DAMPER_OPEN
              point_name: 出口防火阀开启
              point_type: DI
          commands:
            - point_id: SEF_START
              point_name: 排烟风机启动
              point_type: DO
            - point_id: SEF_STOP
              point_name: 排烟风机停止
              point_type: DO
            
        control_logic:
          start_condition:
            - 所属防烟分区火灾确认
            - 排烟阀开启信号
            - 消防控制室手动启动
          stop_condition:
            - 280℃排烟防火阀熔断（自动停）
            - 消防控制室手动停止
            - 火灾结束复位
          interlock:
            - 送风机先停，排烟机后停
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 排烟机房
          note: 每个防火分区设置

      - node_id: FIRE-EXH_DST_PRESS_FAN
        node_name: 加压送风机
        node_name_en: Pressurization Fan
        node_type: Distribution_Node
        node_subtype: FAN
        node_category: DST
      
        function: 对楼梯间和前室加压防烟
        medium_in: AIR-FA
        medium_out: AIR-PRESS
      
        multiplicity: multiple
        instance_pattern: FIRE-EXH_DST_PRESSFAN_{Stairwell}
      
        equipment_parameters:
          type: 轴流式/混流式加压送风机
          configuration: 双速（常用）
          capacity:
            stairwell: {value: 20000, unit: "m³/h"}
            vestibule: {value: 15000, unit: "m³/h"}
          pressure:
            stairwell: {value: "40-50", unit: Pa}
            vestibule: {value: "25-30", unit: Pa}
          motor:
            power: {value: 15, unit: kW}
            protection: IP55
          temperature: 常温运行
          accessories:
            - 70℃防火阀
            - 止回阀
            - 软接头
          
        control_points:
          status:
            - point_id: PF_RUN
              point_name: 加压风机运行
              point_type: DI
            - point_id: PF_FAULT
              point_name: 加压风机故障
              point_type: DI
            - point_id: PF_SPEED
              point_name: 风机转速档位
              point_type: AI
          commands:
            - point_id: PF_START
              point_name: 加压风机启动
              point_type: DO
            - point_id: PF_SPEED_SET
              point_name: 风机调速
              point_type: AO
            
        control_logic:
          start_condition:
            - 火灾确认（任一楼层）
            - 消防控制室手动启动
          operation:
            stage_1: 高速运行（火灾层及相邻层开门时）
            stage_2: 低速运行（维持压力）
          stop_condition:
            - 消防控制室手动停止
            - 火灾结束复位
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 加压送风机房/屋顶
          position: 楼梯间顶部或底部

      - node_id: FIRE-EXH_DST_SMOKE_DAMPER
        node_name: 排烟阀/排烟口
        node_name_en: Smoke Exhaust Damper
        node_type: Distribution_Node
        node_subtype: DMP
        node_category: DST
      
        function: 控制排烟区域，开启时排出烟气
        medium_in: AIR-SMOKE
        medium_out: AIR-SMOKE
      
        multiplicity: multiple
        instance_pattern: FIRE-EXH_DST_SMOKEDAMPER_{Floor}_{Zone}
      
        equipment_parameters:
          type: 电动排烟阀/排烟口
          size: 
            typical: {value: "500×400", unit: mm}
            range: "根据风量计算"
          features:
            - 常闭（平时）
            - 电动/手动开启
            - 280℃熔断自动关闭
            - 开启信号反馈
          coverage: {value: "≤60", unit: m, note: "排烟口服务半径"}
        
        control_points:
          status:
            - point_id: SD_OPEN
              point_name: 排烟阀开启
              point_type: DI
            - point_id: SD_FUSED
              point_name: 熔断关闭
              point_type: DI
          commands:
            - point_id: SD_OPEN_CMD
              point_name: 开启排烟阀
              point_type: DO
            
        control_logic:
          open_condition:
            - 所属防烟分区火灾确认
            - 现场手动开启
            - 消防控制室远程开启
          close_condition:
            - 280℃熔断（不可恢复，需更换）
            - 消防控制室远程关闭
          linkage:
            - 排烟阀开启 → 联动启动排烟风机
      
        location_hint:
          space_type: 走道/房间顶部
          installation: 吊顶上方

      - node_id: FIRE-EXH_DST_PRESS_DAMPER
        node_name: 加压送风口
        node_name_en: Pressurization Air Outlet
        node_type: Distribution_Node
        node_subtype: DMP
        node_category: DST
      
        function: 向楼梯间/前室送入加压空气
        medium_in: AIR-PRESS
        medium_out: AIR-PRESS
      
        multiplicity: multiple
        instance_pattern: FIRE-EXH_DST_PRESSDAMPER_{Stairwell}_{Floor}
      
        equipment_parameters:
          types:
            stairwell:
              name: 楼梯间送风口
              type: 常开百叶风口
              note: 自垂百叶防倒流
            vestibule:
              name: 前室送风口
              type: 常闭电动风口
              operation: 火灾时开启
          size: 根据风量计算
        
        control_points:
          status:
            - point_id: PD_OPEN
              point_name: 送风口开启
              point_type: DI
          commands:
            - point_id: PD_OPEN_CMD
              point_name: 开启送风口
              point_type: DO
            
        control_logic:
          stairwell: 常开，无控制
          vestibule:
            open: 着火层及相邻上下两层
            linkage: 联动加压风机
      
        location_hint:
          space_type: 楼梯间/前室
          height: {value: 2.0, unit: m}

      - node_id: FIRE-EXH_DST_FIRE_DAMPER
        node_name: 防火阀
        node_name_en: Fire Damper
        node_type: Distribution_Node
        node_subtype: DMP
        node_category: DST
      
        function: 防止火灾通过风管蔓延
        medium_in: AIR
        medium_out: AIR
      
        multiplicity: multiple
      
        equipment_parameters:
          types:
            fd_70:
              name: 70℃防火阀
              application: 穿越防火分区的通风管道
              action: 70℃熔断关闭，联动关闭风机
            fd_280:
              name: 280℃排烟防火阀
              application: 排烟管道出口
              action: 280℃熔断关闭，联动关闭排烟风机
          features:
            - 常开（平时）
            - 熔断后自动关闭
            - 手动复位
            - 关闭信号反馈
          
        control_points:
          status:
            - point_id: FD_CLOSED
              point_name: 防火阀关闭
              point_type: DI
              action: 联动关闭风机
            
        control_logic:
          action:
            70℃: 熔断关闭 → 联动关闭送排风机
            280℃: 熔断关闭 → 联动关闭排烟风机
          reset: 手动复位后方可重新使用
      
        location_hint:
          space_type: 防火分区边界
          position: 穿墙/穿楼板处

    sink_nodes:
  
      - node_id: FIRE-EXH_SNK_EXHAUST_OUTLET
        node_name: 排烟出口
        node_name_en: Smoke Exhaust Outlet
        node_type: Sink_Node
        node_category: SNK
      
        function: 烟气排至室外
        medium_in: AIR-SMOKE
        medium_out: AIR-SMOKE (外排)
      
        is_boundary_output: true
      
        equipment_parameters:
          type: 排烟风帽/百叶
          location: 屋顶或外墙高处
          requirements:
            - 距可燃物≥3m
            - 距进风口≥10m
            - 防雨构造
          
        location_hint:
          space_type: 室外
          position: 屋顶

      - node_id: FIRE-EXH_SNK_PROTECTED_SPACE
        node_name: 受保护空间
        node_name_en: Protected Space
        node_type: Sink_Node
        node_category: SNK
      
        function: 疏散通道维持正压无烟
        medium_in: AIR-PRESS
        medium_out: 正压环境
      
        is_boundary_output: true
      
        equipment_parameters:
          spaces:
            - 防烟楼梯间
            - 前室/合用前室
            - 避难层/避难间
          pressure_requirements:
            stairwell: {value: "40-50", unit: Pa}
            vestibule: {value: "25-30", unit: Pa}
            refuge: {value: "≥15", unit: Pa}
          door_force: {value: "≤60", unit: N, note: "门开启力"}
        
        location_hint:
          space_type: 疏散通道

  edges:

    exhaust_edges:
      - edge_id: FIRE-EXH_EDGE_001
        edge_name: 烟气至排烟阀
        edge_type: DUC
        from_node: 着火区域
        to_node: FIRE-EXH_DST_SMOKE_DAMPER
        direction: unidirectional
        medium: AIR-SMOKE
      
      - edge_id: FIRE-EXH_EDGE_002
        edge_name: 排烟阀至排烟风机
        edge_type: DUC
        from_node: FIRE-EXH_DST_SMOKE_DAMPER
        to_node: FIRE-EXH_DST_EXHAUST_FAN
        direction: unidirectional
        medium: AIR-SMOKE
        duct_parameters:
          material: 镀锌钢板/耐火风管
          fire_rating: {value: 1.0, unit: h}
        
      - edge_id: FIRE-EXH_EDGE_003
        edge_name: 排烟风机至室外
        edge_type: DUC
        from_node: FIRE-EXH_DST_EXHAUST_FAN
        to_node: FIRE-EXH_SNK_EXHAUST_OUTLET
        direction: unidirectional
        medium: AIR-SMOKE

    pressurization_edges:
      - edge_id: FIRE-EXH_EDGE_011
        edge_name: 室外至加压风机
        edge_type: DUC
        from_node: FIRE-EXH_SRC_FRESH_AIR
        to_node: FIRE-EXH_DST_PRESS_FAN
        direction: unidirectional
        medium: AIR-FA
      
      - edge_id: FIRE-EXH_EDGE_012
        edge_name: 加压风机至送风口
        edge_type: DUC
        from_node: FIRE-EXH_DST_PRESS_FAN
        to_node: FIRE-EXH_DST_PRESS_DAMPER
        direction: unidirectional
        medium: AIR-PRESS
        duct_parameters:
          material: 镀锌钢板
          fire_rating: 无特殊要求（送风）
        
      - edge_id: FIRE-EXH_EDGE_013
        edge_name: 送风口至保护空间
        edge_type: DUC
        from_node: FIRE-EXH_DST_PRESS_DAMPER
        to_node: FIRE-EXH_SNK_PROTECTED_SPACE
        direction: unidirectional
        medium: AIR-PRESS

  typical_paths:

    - path_id: FIRE-EXH_PATH_EXHAUST
      path_name: 机械排烟路径
      path_type: FIR
      description: 火灾时排除烟气
      sequence:
        - step: 1
          node: FIRE-FAS
          action: 火灾确认
        - step: 2
          node: FIRE-EXH_DST_SMOKE_DAMPER
          action: 着火区排烟阀开启
        - step: 3
          node: FIRE-EXH_DST_EXHAUST_FAN
          action: 排烟风机启动
        - step: 4
          node: FIRE-EXH_SNK_EXHAUST_OUTLET
          action: 烟气排至室外
        
    - path_id: FIRE-EXH_PATH_PRESSURIZATION
      path_name: 加压送风路径
      path_type: FIR
      description: 保护疏散通道
      sequence:
        - step: 1
          node: FIRE-FAS
          action: 火灾确认
        - step: 2
          node: FIRE-EXH_DST_PRESS_DAMPER
          action: 前室送风口开启
        - step: 3
          node: FIRE-EXH_DST_PRESS_FAN
          action: 加压风机启动
        - step: 4
          node: FIRE-EXH_SNK_PROTECTED_SPACE
          action: 楼梯间/前室维持正压

  control_logic:

    smoke_exhaust_control:
      name: 机械排烟控制逻辑
      description: 火灾确认后的排烟联动
    
      sequence:
        - step: 1
          trigger: 防烟分区内火灾确认
          action: 开启该区排烟阀
        - step: 2
          trigger: 排烟阀开启反馈
          action: 启动对应排烟风机
        - step: 3
          action: 持续排烟
        - step: 4
          trigger: 280℃防火阀熔断
          action: 自动停止排烟风机
        
      interlocks:
        - 排烟阀必须开启才能启动排烟风机
        - 排烟风机启动后，关闭该区空调送回风
        - 排烟防火阀熔断后，联锁停止排烟风机
      
    pressurization_control:
      name: 加压送风控制逻辑
      description: 保护疏散通道不被烟气侵入
    
      sequence:
        - step: 1
          trigger: 任一楼层火灾确认
          action: 启动楼梯间加压风机
        - step: 2
          trigger: 火灾确认
          action: 开启着火层及相邻层前室送风口
        - step: 3
          action: 维持正压
          pressure:
            stairwell: "40-50Pa"
            vestibule: "25-30Pa"
        - step: 4
          trigger: 门开启
          action: 风机高速运行
        - step: 5
          trigger: 门关闭
          action: 风机低速运行
        
      interlocks:
        - 加压系统与排烟系统不在同一区域同时运行
        - 前室送风口常闭，火灾时开启
        - 楼梯间送风口常开
      
    fire_damper_control:
      name: 防火阀联动控制
    
      fd_70:
        trigger: 70℃熔断
        action:
          - 阀门自动关闭
          - 反馈关闭信号
          - 联动关闭该系统送排风机
        
      fd_280:
        trigger: 280℃熔断
        action:
          - 阀门自动关闭
          - 反馈关闭信号
          - 联动关闭该系统排烟风机

  alarm_protection:

    system_alarms:
      - alarm_id: ALM_EXHAUST_FAN_FAULT
        alarm_name: 排烟风机故障
        severity: CRITICAL
        trigger: 故障信号/启动后无运行反馈
        action: 检修/启动备用
      
      - alarm_id: ALM_PRESS_FAN_FAULT
        alarm_name: 加压风机故障
        severity: CRITICAL
        trigger: 故障信号
        action: 检修
      
      - alarm_id: ALM_DAMPER_FAULT
        alarm_name: 排烟阀故障
        severity: HIGH
        trigger: 开启命令后无反馈
        action: 现场检查
      
      - alarm_id: ALM_FIRE_DAMPER_CLOSED
        alarm_name: 防火阀熔断关闭
        severity: HIGH
        trigger: 阀门关闭信号
        action: 确认火灾位置

  dependencies:
  
    upstream_dependencies:
      - dependency_id: DEP_EXH_FAS
        from_system: FIRE-FAS
        dependency_type: CONTROL
        criticality: CRITICAL
        description: 接收火灾联动信号
      
      - dependency_id: DEP_EXH_POWER
        from_system: ELEC-EPS
        dependency_type: POWER_SUPPLY
        criticality: CRITICAL
        backup: 双电源末端切换
      
    downstream_dependencies:
      - dependency_id: DEP_TO_FAS_FEEDBACK
        to_system: FIRE-FAS
        dependency_type: FEEDBACK
        criticality: HIGH
        description: 风机和阀门状态反馈
```

---

# 医疗专业系统（3个系统）

## 系统 4.4: MED-OR 手术室环境控制系统

```yaml
System_Topology:

  identity:
    system_id: MED-OR
    system_name: 手术室环境控制系统
    system_name_en: Operating Room Environment Control System
    system_category: MED
    system_type: 医疗-洁净环境
    priority_level: P1-MISSION_CRITICAL
  
    description: |
      手术室洁净环境控制系统，是保障手术安全的核心系统。
      系统控制手术室的洁净度、温湿度、压力梯度、新风量等环境参数。
      采用层流送风技术，确保手术区域空气洁净。
      与医用气体、照明、对讲等系统集成，实现手术室综合管理。
    
    design_basis:
      cleanliness_levels:
        class_100: 
          name: I级手术室
          application: 器官移植、心脏手术
          cleanliness: "≤100粒/m³(≥0.5μm)"
          airflow: 层流
        class_1000:
          name: II级手术室
          application: 骨科、眼科、神经外科
          cleanliness: "≤1000粒/m³"
          airflow: 层流/乱流
        class_10000:
          name: III级手术室
          application: 普外科、妇产科
          cleanliness: "≤10000粒/m³"
          airflow: 乱流
        class_100000:
          name: IV级手术室
          application: 感染手术
          cleanliness: "≤100000粒/m³"
          airflow: 负压
        
      environment_parameters:
        temperature: {value: "22-25", unit: ℃, note: "可调21-27"}
        humidity: {value: "40-60", unit: "%RH"}
        pressure:
          positive: {value: "+8 to +15", unit: Pa}
          negative: {value: "-5 to -10", unit: Pa, note: "感染手术室"}
        fresh_air: {value: "≥60", unit: "m³/h/人"}
        air_changes: {value: "20-40", unit: "次/h"}
        noise: {value: "≤52", unit: dB(A)}
  
    linked_systems:
      - HVAC-AHU: 空调机组
      - MGAS-O2/VAC/AIR: 医用气体
      - ELEC-EPS: 应急电源
      - INT-BA: 楼宇自控
  
    design_standards:
      - GB 50333-2013 医院洁净手术部建筑技术规范
      - GB 51039-2014 综合医院建筑设计规范
      - YY/T 0506 医疗器械洁净工作台
  
    version: 1.0
    last_updated: 2024

  boundary:
    inputs:
      - boundary_id: MED-OR_IN_001
        name: 空调冷热源
        from_system: HVAC-CHP
        medium: WATER-CHW/HW
      
      - boundary_id: MED-OR_IN_002
        name: 医用气体
        from_system: MGAS
        medium: GAS-O2/VAC/AIR/N2O
      
      - boundary_id: MED-OR_IN_003
        name: 电源
        from_system: ELEC-LV/EPS
        medium: ELEC-LV
      
      - boundary_id: MED-OR_IN_004
        name: 控制信号
        from_system: INT-BA
        medium: SIGNAL-BMS
      
    outputs:
      - boundary_id: MED-OR_OUT_001
        name: 洁净环境
        to_system: 手术室空间
        medium: AIR-CLEAN
      
      - boundary_id: MED-OR_OUT_002
        name: 状态反馈
        to_system: INT-BA
        medium: SIGNAL-BMS

  nodes:

    source_nodes:
  
      - node_id: MED-OR_SRC_CHILLED_WATER
        node_name: 冷冻水供应
        node_name_en: Chilled Water Supply
        node_type: Source_Node
        node_category: SRC
      
        function: 为手术室空调提供冷源
        medium_in: WATER-CHW
        medium_out: WATER-CHW
      
        is_boundary_input: true
      
        equipment_parameters:
          source: HVAC-CHP冷水机组
          supply_temp: {value: 7, unit: ℃}
          return_temp: {value: 12, unit: ℃}
          redundancy: 双路供水
          backup: 独立冷源（可选）
        
        location_hint:
          space_type: 管井
          supply_from: 空调机房

      - node_id: MED-OR_SRC_FRESH_AIR
        node_name: 新风取风
        node_name_en: Fresh Air Intake
        node_type: Source_Node
        node_category: SRC
      
        function: 提供手术室新风
        medium_in: AIR-OA
        medium_out: AIR-FA
      
        is_boundary_input: true
      
        equipment_parameters:
          location: 屋顶或高处外墙
          treatment:
            - 初效过滤
            - 中效过滤
            - 加热/冷却
          requirements:
            - 远离污染源
            - 高于地面3m以上
          
        location_hint:
          space_type: 室外

    distribution_nodes:
  
      - node_id: MED-OR_DST_MAU
        node_name: 新风处理机组
        node_name_en: Makeup Air Unit
        node_type: Distribution_Node
        node_subtype: AHU
        node_category: DST
      
        function: 处理手术室新风
        medium_in: AIR-OA
        medium_out: AIR-FA
      
        equipment_parameters:
          type: 组合式空调机组（新风段）
          capacity: {value: 10000, unit: "m³/h", note: "典型"}
          components:
            - 初效过滤器（G4）
            - 中效过滤器（F7）
            - 表冷器
            - 加热器
            - 加湿器
            - 风机
          features:
            - 全新风运行
            - 变频调速
            - 温湿度联合控制
          
        control_points:
          sensors:
            - point_id: MAU_SUPPLY_TEMP
              point_name: 新风送风温度
              point_type: AI
              unit: ℃
            - point_id: MAU_SUPPLY_RH
              point_name: 新风送风湿度
              point_type: AI
              unit: "%RH"
            - point_id: MAU_FILTER_DP
              point_name: 过滤器压差
              point_type: AI
              unit: Pa
          status:
            - point_id: MAU_RUN
              point_name: 机组运行
              point_type: DI
          commands:
            - point_id: MAU_START
              point_name: 机组启动
              point_type: DO
            - point_id: MAU_TEMP_SP
              point_name: 温度设定
              point_type: AO
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 手术部空调机房

      - node_id: MED-OR_DST_AHU
        node_name: 手术室空调机组
        node_name_en: Operating Room AHU
        node_type: Distribution_Node
        node_subtype: AHU
        node_category: DST
      
        function: 为手术室提供洁净空调
        medium_in: AIR-FA + AIR-RA
        medium_out: AIR-CLEAN
      
        multiplicity: multiple
        instance_pattern: MED-OR_DST_AHU_{Zone}
      
        equipment_parameters:
          type: 组合式洁净空调机组
          configuration: 循环风+新风
          capacity: {value: 15000, unit: "m³/h", note: "服务2-3间手术室"}
          components:
            - 混合段
            - 初效过滤器（G4）
            - 中效过滤器（F7）
            - 表冷器（双排管）
            - 加热器
            - 加湿器
            - 送风机（变频）
            - 消声段
          features:
            - 大风量循环
            - 变频调速
            - 温湿度精确控制
            - 过滤器压差监测
          
        control_points:
          sensors:
            - point_id: AHU_SUPPLY_TEMP
              point_name: 送风温度
              point_type: AI
              unit: ℃
            - point_id: AHU_SUPPLY_RH
              point_name: 送风湿度
              point_type: AI
              unit: "%RH"
            - point_id: AHU_RETURN_TEMP
              point_name: 回风温度
              point_type: AI
              unit: ℃
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
          status:
            - point_id: AHU_RUN
              point_name: 机组运行
              point_type: DI
            - point_id: AHU_FAULT
              point_name: 机组故障
              point_type: DI
          commands:
            - point_id: AHU_START
              point_name: 机组启动
              point_type: DO
            - point_id: AHU_TEMP_SP
              point_name: 送风温度设定
              point_type: AO
            - point_id: AHU_RH_SP
              point_name: 送风湿度设定
              point_type: AO
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 手术部空调机房

      - node_id: MED-OR_DST_HEPA_BOX
        node_name: 高效送风口
        node_name_en: HEPA Filter Diffuser
        node_type: Distribution_Node
        node_subtype: TRM
        node_category: DST
      
        function: 末端高效过滤，层流送风
        medium_in: AIR-CLEAN
        medium_out: AIR-ULTRA_CLEAN
      
        multiplicity: multiple
        instance_pattern: MED-OR_DST_HEPA_{OR}_{Seq}
      
        equipment_parameters:
          types:
            laminar_flow:
              name: 层流天花
              application: I/II级手术室
              size: {value: "2400×2600", unit: mm, note: "典型"}
              velocity: {value: "0.25-0.45", unit: "m/s"}
              hepa: H14级
            diffuser:
              name: 高效送风口
              application: III/IV级手术室
              size: {value: "484×484", unit: mm}
              hepa: H13级
          features:
            - 高效过滤器（HEPA）
            - 压差监测
            - 可更换滤芯
            - 层流送风（I/II级）
          
        control_points:
          sensors:
            - point_id: HEPA_DP
              point_name: HEPA压差
              point_type: AI
              unit: Pa
              normal: {value: "200-600", unit: Pa}
              alarm_high: {value: ">600", unit: Pa, note: "需更换"}
          status:
            - point_id: HEPA_BLOCKED
              point_name: 过滤器堵塞
              point_type: DI
              trigger: 压差>600Pa
      
        location_hint:
          space_type: 手术室天花
          position: 手术区正上方

      - node_id: MED-OR_DST_EXHAUST
        node_name: 排风口/回风口
        node_name_en: Exhaust/Return Air Grille
        node_type: Distribution_Node
        node_subtype: TRM
        node_category: DST
      
        function: 排风/回风，维持压力梯度
        medium_in: AIR-ROOM
        medium_out: AIR-EXHAUST/RA
      
        multiplicity: multiple
      
        equipment_parameters:
          types:
            return:
              name: 回风口
              location: 手术室四周下方
              height: {value: "0.1-0.5", unit: m}
              application: 正压手术室
            exhaust:
              name: 排风口
              location: 手术室四周下方
              application: 负压手术室（感染）
          sizing: 保证压力梯度和换气次数
        
        location_hint:
          space_type: 手术室墙面下部

      - node_id: MED-OR_DST_PRESSURE_CONTROL
        node_name: 压力控制系统
        node_name_en: Pressure Control System
        node_type: Distribution_Node
        node_subtype: CTR
        node_category: DST
      
        function: 维持手术室压力梯度
        medium_in: SIGNAL
        medium_out: CONTROL
      
        equipment_parameters:
          method: 余压阀/变频调节
          devices:
            pressure_sensor:
              type: 微差压传感器
              range: {value: "±50", unit: Pa}
              accuracy: {value: "±1", unit: Pa}
            pressure_damper:
              type: 电动余压阀
              control: 自动调节
            
        control_points:
          sensors:
            - point_id: OR_PRESSURE
              point_name: 手术室压力
              point_type: AI
              unit: Pa
              range: [-20, 30]
            - point_id: OR_PRESSURE_DIFF
              point_name: 压力差（相对走道）
              point_type: AI
              unit: Pa
          status:
            - point_id: PRESSURE_NORMAL
              point_name: 压力正常
              point_type: DI
            - point_id: PRESSURE_ALARM
              point_name: 压力异常
              point_type: DI
          commands:
            - point_id: PRESSURE_SP
              point_name: 压力设定
              point_type: AO
            
        control_logic:
          positive_pressure:
            application: 普通手术室
            setpoint: "+8 to +15Pa"
            control: 调节送风量/排风量
          negative_pressure:
            application: 感染手术室
            setpoint: "-5 to -10Pa"
            control: 增加排风量
          gradient:
            principle: 手术室>洁净走道>清洁走道>污物走道
            step: "5-10Pa"
      
        location_hint:
          space_type: 每间手术室

      - node_id: MED-OR_DST_CONTROL_PANEL
        node_name: 手术室控制面板
        node_name_en: Operating Room Control Panel
        node_type: Distribution_Node
        node_subtype: CTR
        node_category: DST
      
        function: 手术室环境参数显示和控制
        medium_in: SIGNAL-BMS
        medium_out: DISPLAY/CONTROL
      
        multiplicity: multiple
        instance_pattern: MED-OR_DST_PANEL_{OR}
      
        equipment_parameters:
          type: 嵌墙式触摸屏控制面板
          size: {value: 10.1, unit: inch}
          features:
            - 温度显示/设定
            - 湿度显示/设定
            - 压力显示
            - 计时功能
            - 医用气体压力显示
            - 一键启动/停止
          material: 抗菌不锈钢面板
          protection: IP65
          installation: 墙面嵌入
        
        control_points:
          display:
            - 温度（实际/设定）
            - 湿度（实际/设定）
            - 压力差
            - 手术计时
            - 气体压力
          control:
            - 温度设定（±3℃）
            - 湿度设定（±10%RH）
            - 一键启动
            - 一键停止
      
        location_hint:
          space_type: 手术室墙面
          position: 方便操作处

    sink_nodes:
  
      - node_id: MED-OR_SNK_OPERATING_ROOM
        node_name: 手术室
        node_name_en: Operating Room
        node_type: Sink_Node
        node_category: SNK
      
        function: 手术操作空间
        medium_in: AIR-ULTRA_CLEAN
        medium_out: CLEAN_ENVIRONMENT
      
        is_boundary_output: true
      
        multiplicity: multiple
        instance_pattern: MED-OR_SNK_OR_{Seq}
        typical_quantity: {value: "10-30", unit: "间", note: "大型医院"}
      
        equipment_parameters:
          classification:
            class_I:
              area: {value: "≥40", unit: "m²"}
              height: {value: 3.0, unit: m}
              application: 器官移植、心脏手术
            class_II:
              area: {value: "≥35", unit: "m²"}
              height: {value: 2.8, unit: m}
              application: 骨科、眼科
            class_III:
              area: {value: "≥30", unit: "m²"}
              height: {value: 2.7, unit: m}
              application: 普外科
            class_IV:
              area: {value: "≥25", unit: "m²"}
              height: {value: 2.6, unit: m}
              application: 感染手术
          environment:
            temperature: "22-25℃"
            humidity: "40-60%RH"
            cleanliness: 按级别
            pressure: 按类型
          facilities:
            - 无影灯
            - 吊塔（气体/电源）
            - 手术床
            - 观片灯
            - 书写台
            - 净化送风天花
          
        location_hint:
          space_type: 手术部
          floor: 专用楼层

      - node_id: MED-OR_SNK_SUPPORT_ROOMS
        node_name: 手术辅助用房
        node_name_en: Support Rooms
        node_type: Sink_Node
        node_category: SNK
      
        function: 手术相关辅助空间
        medium_in: AIR-CLEAN
        medium_out: CLEAN_ENVIRONMENT
      
        is_boundary_output: true
      
        equipment_parameters:
          rooms:
            prep_room:
              name: 准备室
              cleanliness: 10万级
              pressure: 正压
            scrub_room:
              name: 刷手间
              cleanliness: 30万级
              pressure: 正压
            anesthesia_room:
              name: 麻醉准备室
              cleanliness: 10万级
              pressure: 正压
            clean_corridor:
              name: 洁净走道
              cleanliness: 10万级
              pressure: 正压（低于手术室）
            soiled_corridor:
              name: 污物走道
              cleanliness: 无要求
              pressure: 负压
            
        location_hint:
          space_type: 手术部

  edges:

    air_supply_edges:
      - edge_id: MED-OR_EDGE_001
        edge_name: 新风至新风机组
        edge_type: DUC
        from_node: MED-OR_SRC_FRESH_AIR
        to_node: MED-OR_DST_MAU
        direction: unidirectional
        medium: AIR-OA
      
      - edge_id: MED-OR_EDGE_002
        edge_name: 新风机组至空调机组
        edge_type: DUC
        from_node: MED-OR_DST_MAU
        to_node: MED-OR_DST_AHU
        direction: unidirectional
        medium: AIR-FA
      
      - edge_id: MED-OR_EDGE_003
        edge_name: 空调机组至高效送风口
        edge_type: DUC
        from_node: MED-OR_DST_AHU
        to_node: MED-OR_DST_HEPA_BOX
        direction: unidirectional
        medium: AIR-CLEAN
        duct_parameters:
          material: 镀锌钢板（内壁光滑）
          sealing: 密封处理
        
      - edge_id: MED-OR_EDGE_004
        edge_name: 高效送风口至手术室
        edge_type: AIR
        from_node: MED-OR_DST_HEPA_BOX
        to_node: MED-OR_SNK_OPERATING_ROOM
        direction: unidirectional
        medium: AIR-ULTRA_CLEAN

    return_edges:
      - edge_id: MED-OR_EDGE_011
        edge_name: 手术室至回风口
        edge_type: AIR
        from_node: MED-OR_SNK_OPERATING_ROOM
        to_node: MED-OR_DST_EXHAUST
        direction: unidirectional
        medium: AIR-ROOM
      
      - edge_id: MED-OR_EDGE_012
        edge_name: 回风至空调机组
        edge_type: DUC
        from_node: MED-OR_DST_EXHAUST
        to_node: MED-OR_DST_AHU
        direction: unidirectional
        medium: AIR-RA

    chilled_water_edges:
      - edge_id: MED-OR_EDGE_021
        edge_name: 冷水至空调机组
        edge_type: PIP
        from_node: MED-OR_SRC_CHILLED_WATER
        to_node: MED-OR_DST_AHU
        direction: bidirectional
        medium: WATER-CHW

  typical_paths:

    - path_id: MED-OR_PATH_SUPPLY
      path_name: 洁净空气供应路径
      path_type: HVAC
      description: 从室外新风到手术室洁净空气
      sequence:
        - step: 1
          node: MED-OR_SRC_FRESH_AIR
          action: 取新风
        - step: 2
          node: MED-OR_DST_MAU
          action: 新风处理（G4+F7过滤、调温调湿）
        - step: 3
          node: MED-OR_DST_AHU
          action: 与回风混合，再处理
        - step: 4
          node: MED-OR_DST_HEPA_BOX
          action: HEPA高效过滤
        - step: 5
          node: MED-OR_SNK_OPERATING_ROOM
          action: 层流送风至手术区

    - path_id: MED-OR_PATH_CONTROL
      path_name: 环境控制路径
      path_type: CTR
      description: 温湿度和压力控制
      sequence:
        - step: 1
          node: MED-OR_DST_CONTROL_PANEL
          action: 医护人员设定参数
        - step: 2
          node: MED-OR_DST_PRESSURE_CONTROL
          action: 采集当前环境参数
        - step: 3
          node: MED-OR_DST_AHU
          action: 调节送风量、温湿度
        - step: 4
          node: MED-OR_SNK_OPERATING_ROOM
          action: 环境参数达到设定值

  control_logic:

    temperature_control:
      name: 温度控制
      description: 手术室温度精确控制
    
      setpoint:
        range: {value: "21-27", unit: ℃}
        default: {value: 24, unit: ℃}
        adjustment: 医护人员可调
      
      control_method:
        type: PID闭环控制
        actuator: 冷/热水阀
        response: {value: "<5", unit: min}
        accuracy: {value: "±1", unit: ℃}
      
      interlock:
        - 低于18℃报警
        - 高于30℃报警
      
    humidity_control:
      name: 湿度控制
      description: 手术室湿度控制
    
      setpoint:
        range: {value: "40-60", unit: "%RH"}
        default: {value: 50, unit: "%RH"}
      
      control_method:
        dehumidify: 表冷器除湿
        humidify: 蒸汽加湿器
        accuracy: {value: "±5", unit: "%RH"}
      
      interlock:
        - 低于30%RH报警
        - 高于70%RH报警
      
    pressure_control:
      name: 压力梯度控制
      description: 维持手术室正压或负压
    
      positive_pressure:
        application: 普通手术室
        setpoint: {value: "+10", unit: Pa}
        range: {value: "+8 to +15", unit: Pa}
      
      negative_pressure:
        application: 感染手术室
        setpoint: {value: "-8", unit: Pa}
        range: {value: "-5 to -10", unit: Pa}
      
      control_method:
        type: 送排风量平衡
        actuator: 变频风机/电动风阀
        response: {value: "<30", unit: s}
      
      pressure_gradient:
        sequence: 手术室 > 洁净走道 > 清洁区 > 污物区
        step: {value: "5-10", unit: Pa}
      
    startup_sequence:
      name: 手术室启动顺序
      description: 手术开始前的系统启动
    
      before_surgery:
        time: {value: 30, unit: min, note: "提前启动"}
        sequence:
          - step: 1
            action: 启动空调机组
          - step: 2
            action: 检查温湿度
          - step: 3
            action: 检查压力梯度
          - step: 4
            action: 检查医用气体压力
          - step: 5
            action: 确认参数合格，允许手术
          
    shutdown_sequence:
      name: 手术室关机顺序
      description: 手术结束后的系统关闭
    
      after_surgery:
        delay: {value: 15, unit: min, note: "延迟关闭"}
        sequence:
          - step: 1
            action: 手术结束信号
          - step: 2
            action: 继续运行15分钟自净
          - step: 3
            action: 切换至值班模式（低速运行）
            or: 完全关闭（夜间）
          
    filter_management:
      name: 过滤器管理
      description: 过滤器堵塞监测和更换提醒
    
      monitoring:
        - location: 初效过滤器
          dp_alarm: {value: 150, unit: Pa}
          action: 更换提醒
        - location: 中效过滤器
          dp_alarm: {value: 250, unit: Pa}
          action: 更换提醒
        - location: HEPA过滤器
          dp_alarm: {value: 600, unit: Pa}
          action: 必须更换
        
      replacement_record:
        - 更换日期
        - 累计运行时间
        - 更换人员

  alarm_protection:

    environment_alarms:
      - alarm_id: ALM_OR_TEMP_HIGH
        alarm_name: 手术室温度过高
        severity: HIGH
        trigger: 温度>28℃
        action: 检查空调系统
      
      - alarm_id: ALM_OR_TEMP_LOW
        alarm_name: 手术室温度过低
        severity: HIGH
        trigger: 温度<20℃
        action: 检查空调系统
      
      - alarm_id: ALM_OR_RH_HIGH
        alarm_name: 手术室湿度过高
        severity: MEDIUM
        trigger: 湿度>65%RH
        action: 检查除湿
      
      - alarm_id: ALM_OR_PRESSURE_LOSS
        alarm_name: 手术室压力丢失
        severity: HIGH
        trigger: 正压手术室压力<5Pa
        action: 检查送排风系统
      
      - alarm_id: ALM_OR_NEGATIVE_FAIL
        alarm_name: 负压手术室压力异常
        severity: CRITICAL
        trigger: 负压手术室压力>0Pa
        action: 立即检查，防止感染扩散
      
    equipment_alarms:
      - alarm_id: ALM_AHU_FAULT
        alarm_name: 空调机组故障
        severity: CRITICAL
        trigger: 机组故障信号
        action: 启动备用/检修
      
      - alarm_id: ALM_HEPA_BLOCKED
        alarm_name: HEPA过滤器堵塞
        severity: HIGH
        trigger: HEPA压差>600Pa
        action: 更换过滤器

  dependencies:
  
    upstream_dependencies:
      - dependency_id: DEP_OR_CHILLED
        from_system: HVAC-CHP
        dependency_type: COOLING
        criticality: HIGH
        backup: 应急独立冷源（可选）
      
      - dependency_id: DEP_OR_POWER
        from_system: ELEC-EPS
        dependency_type: POWER_SUPPLY
        criticality: CRITICAL
        backup: UPS/发电机
      
      - dependency_id: DEP_OR_GAS
        from_system: MGAS
        dependency_type: MEDICAL_GAS
        criticality: CRITICAL
      
    downstream_dependencies:
      - dependency_id: DEP_TO_BA
        to_system: INT-BA
        dependency_type: MONITORING
        criticality: HIGH
        description: 环境参数监控
```

---

## 系统 4.5: MED-ICU 重症监护环境系统

```yaml
System_Topology:

  identity:
    system_id: MED-ICU
    system_name: 重症监护环境系统
    system_name_en: ICU Environment Control System
    system_category: MED
    system_type: 医疗-洁净环境
    priority_level: P1-MISSION_CRITICAL
  
    description: |
      重症监护病房（ICU）环境控制系统，保障危重患者的治疗环境。
      包括温湿度控制、空气洁净度控制、压力控制、噪声控制等。
      ICU通常分为普通ICU和隔离ICU，隔离ICU需要负压控制。
      系统与医用气体、监护设备、护士呼叫等系统集成。
    
    design_basis:
      environment_parameters:
        temperature: {value: "22-26", unit: ℃}
        humidity: {value: "40-60", unit: "%RH"}
        cleanliness: {value: 10000, unit: "粒/m³", note: "万级"}
        pressure:
          general_icu: {value: "+5", unit: Pa, note: "正压"}
          isolation_icu: {value: "-5 to -10", unit: Pa, note: "负压"}
        fresh_air: {value: "≥60", unit: "m³/h/人"}
        air_changes: {value: "10-15", unit: "次/h"}
        noise: {value: "≤45", unit: dB(A), note: "白天"}
    
      bed_configuration:
        open_ward: 
          description: 开放式ICU
          beds_per_room: "6-12床"
          area_per_bed: {value: "≥15", unit: "m²"}
        single_room:
          description: 单间ICU
          beds_per_room: 1床
          area_per_bed: {value: "≥20", unit: "m²"}
          application: 隔离患者
  
    linked_systems:
      - HVAC-AHU: 空调机组
      - MGAS-O2/VAC/AIR: 医用气体
      - INT-NUR: 护士呼叫
      - ELEC-EPS: 应急电源
  
    design_standards:
      - GB 51039-2014 综合医院建筑设计规范
      - GB 50333-2013 医院洁净手术部建筑技术规范（参考）
      - 重症医学科建设与管理指南
  
    version: 1.0
    last_updated: 2024

  boundary:
    inputs:
      - boundary_id: MED-ICU_IN_001
        name: 空调冷热源
        from_system: HVAC-CHP
        medium: WATER-CHW/HW
      
      - boundary_id: MED-ICU_IN_002
        name: 医用气体
        from_system: MGAS
        medium: GAS-O2/VAC/AIR
      
      - boundary_id: MED-ICU_IN_003
        name: 电源
        from_system: ELEC-LV/EPS
        medium: ELEC-LV
      
    outputs:
      - boundary_id: MED-ICU_OUT_001
        name: 洁净环境
        to_system: ICU病房
        medium: AIR-CLEAN

  nodes:

    source_nodes:
  
      - node_id: MED-ICU_SRC_SUPPLY
        node_name: 冷热源供应
        node_name_en: Chilled/Hot Water Supply
        node_type: Source_Node
        node_category: SRC
      
        function: 为ICU空调提供冷热源
        medium_in: WATER-CHW/HW
        medium_out: WATER-CHW/HW
      
        is_boundary_input: true
      
        equipment_parameters:
          source: HVAC-CHP
          redundancy: 双路供水
        
        location_hint:
          space_type: 管井

    distribution_nodes:
  
      - node_id: MED-ICU_DST_AHU
        node_name: ICU空调机组
        node_name_en: ICU Air Handling Unit
        node_type: Distribution_Node
        node_subtype: AHU
        node_category: DST
      
        function: 为ICU提供洁净空调空气
        medium_in: AIR-OA + AIR-RA
        medium_out: AIR-CLEAN
      
        equipment_parameters:
          type: 组合式洁净空调机组
          configuration: 新风+回风
          capacity: {value: 20000, unit: "m³/h", note: "典型"}
          components:
            - 新风段（初效+中效）
            - 混合段
            - 表冷器
            - 加热器
            - 加湿器
            - 送风机（变频）
            - 中效过滤器（F8）
            - 消声段
          features:
            - 全年供冷/供热
            - 变频调速
            - 备用机组（推荐）
          
        control_points:
          sensors:
            - point_id: ICU_AHU_SUPPLY_TEMP
              point_name: 送风温度
              point_type: AI
              unit: ℃
            - point_id: ICU_AHU_SUPPLY_RH
              point_name: 送风湿度
              point_type: AI
              unit: "%RH"
          status:
            - point_id: ICU_AHU_RUN
              point_name: 机组运行
              point_type: DI
          commands:
            - point_id: ICU_AHU_START
              point_name: 机组启动
              point_type: DO
      
        location_hint:
          space_type: MEP_ROOM
          room_name: ICU空调机房

      - node_id: MED-ICU_DST_HEPA
        node_name: ICU高效送风口
        node_name_en: ICU HEPA Diffuser
        node_type: Distribution_Node
        node_subtype: TRM
        node_category: DST
      
        function: 末端高效过滤
        medium_in: AIR-CLEAN
        medium_out: AIR-HEPA_FILTERED
      
        multiplicity: multiple
      
        equipment_parameters:
          type: 高效送风口
          hepa: H13级
          size: {value: "610×610", unit: mm}
        
        control_points:
          sensors:
            - point_id: ICU_HEPA_DP
              point_name: HEPA压差
              point_type: AI
              unit: Pa
      
        location_hint:
          space_type: ICU病房天花

      - node_id: MED-ICU_DST_ISOLATION_ROOM
        node_name: 隔离病房压力控制
        node_name_en: Isolation Room Pressure Control
        node_type: Distribution_Node
        node_subtype: CTR
        node_category: DST
      
        function: 负压隔离病房压力控制
        medium_in: AIR
        medium_out: AIR
      
        multiplicity: multiple
        instance_pattern: MED-ICU_DST_ISOLATION_{Seq}
      
        equipment_parameters:
          type: 负压隔离系统
          components:
            - 送风量调节阀
            - 排风量调节阀
            - 压力传感器
            - 可视化压差计
            - 入口缓冲间
          features:
            - 负压维持 -5 to -10Pa
            - 双门互锁缓冲间
            - 独立排风（直接室外）
            - HEPA过滤排风
          
        control_points:
          sensors:
            - point_id: ISO_PRESSURE
              point_name: 隔离病房压力
              point_type: AI
              unit: Pa
              setpoint: -8
              alarm_high: ">0Pa"
          status:
            - point_id: ISO_DOOR_INTERLOCK
              point_name: 双门互锁状态
              point_type: DI
            - point_id: ISO_NEGATIVE_OK
              point_name: 负压正常
              point_type: DI
          alarms:
            - point_id: ALM_ISO_PRESSURE_LOSS
              point_name: 负压丢失报警
              point_type: DI
              severity: CRITICAL
            
        control_logic:
          negative_pressure:
            method: 排风量>送风量
            difference: {value: "10-15", unit: "%"}
          door_interlock:
            rule: 两道门不能同时开启
            alarm: 同时开启时报警
          exhaust_treatment:
            method: HEPA过滤后直接室外排放
            note: 不得回风
      
        location_hint:
          space_type: ICU隔离病房

      - node_id: MED-ICU_DST_BED_UNIT
        node_name: 床头设备带
        node_name_en: Bed Head Unit
        node_type: Distribution_Node
        node_subtype: TRM
        node_category: DST
      
        function: 床旁医用气体和电源接口
        medium_in: GAS-O2/VAC/AIR + ELEC
        medium_out: 终端供应
      
        multiplicity: multiple
        instance_pattern: MED-ICU_DST_BHU_{Bed}
      
        equipment_parameters:
          type: ICU吊桥/床头带
          gas_outlets:
            O2: {value: 2, unit: "个"}
            VAC: {value: 2, unit: "个"}
            AIR: {value: 1, unit: "个"}
          electrical:
            outlets: {value: "8-12", unit: "个"}
            type: 医用插座
            circuit: 独立回路
          monitoring:
            - 气体压力显示
            - 流量显示（可选）
          accessories:
            - 输液架
            - 监护仪支架
            - 照明灯
            - 呼叫按钮
          
        control_points:
          sensors:
            - point_id: BHU_O2_PRESSURE
              point_name: 床旁氧气压力
              point_type: AI
              unit: MPa
            - point_id: BHU_VAC_PRESSURE
              point_name: 床旁负压吸引
              point_type: AI
              unit: kPa
          status:
            - point_id: BHU_GAS_ALARM
              point_name: 气体报警
              point_type: DI
      
        location_hint:
          space_type: ICU床位上方

    sink_nodes:
  
      - node_id: MED-ICU_SNK_ICU_WARD
        node_name: ICU病房
        node_name_en: ICU Ward
        node_type: Sink_Node
        node_category: SNK
      
        function: 重症患者治疗空间
        medium_in: AIR-CLEAN + GAS
        medium_out: TREATMENT_ENVIRONMENT
      
        is_boundary_output: true
      
        multiplicity: multiple
      
        equipment_parameters:
          types:
            open_icu:
              name: 开放式ICU
              beds: "6-12床"
              area_per_bed: {value: "≥15", unit: "m²"}
              monitoring: 中央监护站
            single_icu:
              name: 单间ICU
              beds: 1床
              area_per_bed: {value: "≥20", unit: "m²"}
              application: 重症/隔离
            isolation_icu:
              name: 负压隔离ICU
              beds: 1床
              pressure: 负压
              application: 传染病患者
          environment:
            temperature: "22-26℃"
            humidity: "40-60%RH"
            cleanliness: 万级
            noise: "<45dB(A)"
            lighting: "100-500lux"
          facilities:
            - 床头设备带
            - 监护仪
            - 呼吸机接口
            - 护士呼叫
          
        location_hint:
          space_type: ICU病区

  typical_paths:

    - path_id: MED-ICU_PATH_SUPPLY
      path_name: ICU空气供应路径
      path_type: HVAC
      sequence:
        - step: 1
          node: MED-ICU_SRC_SUPPLY
          action: 冷热水供应
        - step: 2
          node: MED-ICU_DST_AHU
          action: 空气处理
        - step: 3
          node: MED-ICU_DST_HEPA
          action: 高效过滤
        - step: 4
          node: MED-ICU_SNK_ICU_WARD
          action: 送达ICU病房

    - path_id: MED-ICU_PATH_ISOLATION
      path_name: 隔离病房负压路径
      path_type: CTR
      sequence:
        - step: 1
          node: MED-ICU_DST_AHU
          action: 送风
        - step: 2
          node: MED-ICU_DST_ISOLATION_ROOM
          action: 负压控制
        - step: 3
          action: HEPA过滤排风
        - step: 4
          action: 室外直排

  control_logic:

    temperature_humidity_control:
      name: ICU温湿度控制
      setpoint:
        temperature: {value: "24", unit: ℃, range: "22-26"}
        humidity: {value: "50", unit: "%RH", range: "40-60"}
      method: 空调机组+FCU局部调节
      accuracy:
        temperature: {value: "±1", unit: ℃}
        humidity: {value: "±5", unit: "%RH"}
      
    isolation_pressure_control:
      name: 隔离病房压力控制
      setpoint: {value: "-8", unit: Pa}
      range: {value: "-5 to -10", unit: Pa}
      method: 送排风量差控制
      interlock:
        - 双门互锁
        - 压力丢失报警
        - 排风HEPA状态监测
      
    continuous_operation:
      name: 24小时连续运行
      requirement: ICU空调系统24×7运行
      redundancy:
        - 备用机组
        - 双路冷源
        - 应急电源

  alarm_protection:

    environment_alarms:
      - alarm_id: ALM_ICU_TEMP_HIGH
        alarm_name: ICU温度过高
        severity: HIGH
        trigger: ">28℃"
      
      - alarm_id: ALM_ICU_ISO_PRESSURE
        alarm_name: 隔离病房负压丢失
        severity: CRITICAL
        trigger: 负压病房压力>0Pa
        action: 立即检查，防止交叉感染
      
      - alarm_id: ALM_ICU_DOOR_INTERLOCK
        alarm_name: 双门互锁失效
        severity: HIGH
        trigger: 两道门同时开启
      
    equipment_alarms:
      - alarm_id: ALM_ICU_AHU_FAULT
        alarm_name: ICU空调故障
        severity: CRITICAL
        action: 启动备用机组

  dependencies:
  
    upstream_dependencies:
      - dependency_id: DEP_ICU_HVAC
        from_system: HVAC-CHP
        dependency_type: COOLING_HEATING
        criticality: CRITICAL
      
      - dependency_id: DEP_ICU_POWER
        from_system: ELEC-EPS
        dependency_type: POWER_SUPPLY
        criticality: CRITICAL
      
      - dependency_id: DEP_ICU_GAS
        from_system: MGAS
        dependency_type: MEDICAL_GAS
        criticality: CRITICAL
```

---

## 系统 4.6: MED-LAB 检验科专用系统

```yaml
System_Topology:

  identity:
    system_id: MED-LAB
    system_name: 检验科专用系统
    system_name_en: Clinical Laboratory System
    system_category: MED
    system_type: 医疗-检验
    priority_level: P2-BUSINESS_CRITICAL
  
    description: |
      检验科专用机电系统，为临床检验提供环境保障。
      包括实验室通风系统、纯水系统、废水处理系统、
      生物安全柜排风系统等。
      实验室分区管理，保障生物安全和检验质量。
    
    design_basis:
      lab_classification:
        bsl_1:
          name: 一级生物安全实验室
          application: 常规临床检验
          requirements: 基本防护
        bsl_2:
          name: 二级生物安全实验室
          application: 病原微生物检验
          requirements: 负压+BSC
        bsl_3:
          name: 三级生物安全实验室
          application: 高致病性病原体（如有）
          requirements: 严格负压+HEPA
        
      environment:
        temperature: {value: "20-26", unit: ℃}
        humidity: {value: "30-70", unit: "%RH"}
        ventilation: {value: "6-12", unit: "次/h"}
        pressure:
          general: 微正压或常压
          bsl_2: 负压
        
    design_standards:
      - WS 233-2017 临床实验室安全标准
      - GB 19489-2008 实验室生物安全通用要求
      - GB 50346-2011 生物安全实验室建筑技术规范
  
    version: 1.0
    last_updated: 2024

  boundary:
    inputs:
      - boundary_id: MED-LAB_IN_001
        name: 市政给水
        from_system: PLUMB-DWS
        medium: WATER-PW
      
      - boundary_id: MED-LAB_IN_002
        name: 空调系统
        from_system: HVAC-AHU
        medium: AIR
      
      - boundary_id: MED-LAB_IN_003
        name: 电力
        from_system: ELEC-LV
        medium: ELEC-LV
      
    outputs:
      - boundary_id: MED-LAB_OUT_001
        name: 实验室废水
        to_system: 废水处理系统
        medium: WATER-WASTE
      
      - boundary_id: MED-LAB_OUT_002
        name: 排风
        to_system: 室外
        medium: AIR-EXHAUST

  nodes:

    source_nodes:
  
      - node_id: MED-LAB_SRC_WATER
        node_name: 实验室供水
        node_name_en: Laboratory Water Supply
        node_type: Source_Node
        node_category: SRC
      
        function: 为实验室提供用水
        medium_in: WATER-PW
        medium_out: WATER-LAB
      
        is_boundary_input: true
      
        equipment_parameters:
          types:
            city_water:
              name: 市政自来水
              application: 一般清洗
            pure_water:
              name: 纯水
              application: 实验用水
            ultrapure_water:
              name: 超纯水
              application: 分析仪器
            
        location_hint:
          space_type: 管井/纯水站

    distribution_nodes:
  
      - node_id: MED-LAB_DST_PURE_WATER
        node_name: 纯水制备系统
        node_name_en: Pure Water System
        node_type: Distribution_Node
        node_subtype: WTR
        node_category: DST
      
        function: 制备实验室纯水
        medium_in: WATER-PW
        medium_out: WATER-PURE
      
        equipment_parameters:
          type: 反渗透+EDI纯水系统
          capacity: {value: 1000, unit: "L/h"}
          water_quality:
            type_1:
              name: 超纯水
              resistivity: {value: ">18", unit: "MΩ·cm"}
              application: 高精度分析
            type_2:
              name: 分析纯水
              resistivity: {value: ">1", unit: "MΩ·cm"}
              application: 一般实验
            type_3:
              name: 实验纯水
              resistivity: {value: ">0.1", unit: "MΩ·cm"}
              application: 清洗/配液
          components:
            - 预处理（砂滤、活性炭、软化）
            - 反渗透（RO）
            - EDI电去离子
            - 超纯化（可选）
            - 储水箱
            - 分配泵
            - 终端纯化器
          
        control_points:
          sensors:
            - point_id: PW_CONDUCTIVITY
              point_name: 纯水电导率
              point_type: AI
              unit: "μS/cm"
            - point_id: PW_FLOW
              point_name: 纯水流量
              point_type: AI
              unit: "L/h"
            - point_id: PW_TANK_LEVEL
              point_name: 储水箱液位
              point_type: AI
              unit: "%"
          status:
            - point_id: PW_SYSTEM_RUN
              point_name: 系统运行
              point_type: DI
            - point_id: PW_QUALITY_OK
              point_name: 水质合格
              point_type: DI
          alarms:
            - point_id: ALM_PW_QUALITY
              point_name: 水质不合格
              point_type: DI
              severity: HIGH
      
        location_hint:
          space_type: MEP_ROOM
          room_name: 纯水站

      - node_id: MED-LAB_DST_BSC
        node_name: 生物安全柜
        node_name_en: Biological Safety Cabinet
        node_type: Distribution_Node
        node_subtype: EQP
        node_category: DST
      
        function: 提供生物安全操作环境
        medium_in: AIR-ROOM
        medium_out: AIR-FILTERED
      
        multiplicity: multiple
        instance_pattern: MED-LAB_DST_BSC_{Lab}_{Seq}
      
        equipment_parameters:
          types:
            class_II_A2:
              name: II级A2型生物安全柜
              recirculation: {value: 70, unit: "%"}
              exhaust: {value: 30, unit: "%"}
              application: 常规微生物
              exhaust_method: 室内排放/外排
            class_II_B2:
              name: II级B2型生物安全柜
              recirculation: {value: 0, unit: "%"}
              exhaust: {value: 100, unit: "%"}
              application: 化学危害/放射性
              exhaust_method: 必须外排
          features:
            - HEPA过滤（送风和排风）
            - 负压操作区
            - 下降气流速度0.3-0.5m/s
            - 紫外灯消毒
            - 气流报警
          
        control_points:
          sensors:
            - point_id: BSC_AIRFLOW
              point_name: 下降气流速度
              point_type: AI
              unit: "m/s"
            - point_id: BSC_WINDOW_POS
              point_name: 窗口位置
              point_type: AI
              unit: "%"
          status:
            - point_id: BSC_RUN
              point_name: 运行状态
              point_type: DI
            - point_id: BSC_AIRFLOW_ALARM
              point_name: 气流报警
              point_type: DI
          alarms:
            - point_id: ALM_BSC_AIRFLOW
              point_name: 气流异常
              point_type: DI
              severity: HIGH
      
        location_hint:
          space_type: 微生物实验室

      - node_id: MED-LAB_DST_EXHAUST
        node_name: 实验室排风系统
        node_name_en: Laboratory Exhaust System
        node_type: Distribution_Node
        node_subtype: FAN
        node_category: DST
      
        function: 实验室通风排风
        medium_in: AIR-LAB
        medium_out: AIR-EXHAUST
      
        equipment_parameters:
          types:
            general_exhaust:
              name: 一般排风
              application: 普通实验区
              treatment: 无特殊处理
            fume_hood_exhaust:
              name: 通风柜排风
              application: 化学实验
              treatment: 必要时活性炭/喷淋
            bsc_exhaust:
              name: 生物安全柜排风
              application: 微生物实验
              treatment: HEPA过滤
          features:
            - 变频调速
            - 负压维持
            - 排风处理（视需要）
          
        control_points:
          sensors:
            - point_id: LAB_EXHAUST_FLOW
              point_name: 排风量
              point_type: AI
              unit: "m³/h"
          status:
            - point_id: LAB_EXHAUST_RUN
              point_name: 排风机运行
              point_type: DI
          commands:
            - point_id: LAB_EXHAUST_START
              point_name: 启动排风
              point_type: DO
      
        location_hint:
          space_type: 屋顶/机房

      - node_id: MED-LAB_DST_WASTEWATER
        node_name: 实验室废水处理
        node_name_en: Laboratory Wastewater Treatment
        node_type: Distribution_Node
        node_subtype: WTR
        node_category: DST
      
        function: 处理实验室废水
        medium_in: WATER-WASTE
        medium_out: WATER-TREATED
      
        equipment_parameters:
          type: 实验室废水处理系统
          capacity: {value: 10, unit: "m³/d"}
          treatment:
            stages:
              - 预处理（格栅、调节池）
              - 中和（酸碱废水）
              - 氧化（有机物）
              - 消毒（生物性废水）
              - 沉淀
            outlet_standard: GB 8978-1996 三级标准
          waste_types:
            - 酸碱废水
            - 有机废水
            - 生物性废水
            - 重金属废水（单独收集）
          
        control_points:
          sensors:
            - point_id: WW_PH
              point_name: 出水pH值
              point_type: AI
              unit: pH
            - point_id: WW_COD
              point_name: 出水COD
              point_type: AI
              unit: "mg/L"
            - point_id: WW_TANK_LEVEL
              point_name: 集水池液位
              point_type: AI
              unit: "%"
          status:
            - point_id: WW_SYSTEM_RUN
              point_name: 系统运行
              point_type: DI
            - point_id: WW_QUALITY_OK
              point_name: 出水合格
              point_type: DI
          alarms:
            - point_id: ALM_WW_PH
              point_name: pH超标
              point_type: DI
              severity: HIGH
      
        location_hint:
          space_type: 地下室/室外
          room_name: 废水处理站

      - node_id: MED-LAB_DST_FUME_HOOD
        node_name: 通风柜
        node_name_en: Fume Hood
        node_type: Distribution_Node
        node_subtype: EQP
        node_category: DST
      
        function: 化学实验操作防护
        medium_in: AIR-ROOM
        medium_out: AIR-EXHAUST
      
        multiplicity: multiple
        instance_pattern: MED-LAB_DST_FUMEHOOD_{Lab}_{Seq}
      
        equipment_parameters:
          type: 桌上型/落地型通风柜
          face_velocity: {value: "0.4-0.6", unit: "m/s"}
          exhaust_volume: {value: 1000, unit: "m³/h", note: "典型"}
          features:
            - VAV变风量控制
            - 面风速监测
            - 门位置监测
            - 低风速报警
          
        control_points:
          sensors:
            - point_id: FH_FACE_VELOCITY
              point_name: 面风速
              point_type: AI
              unit: "m/s"
            - point_id: FH_SASH_POS
              point_name: 门位置
              point_type: AI
              unit: "%"
          status:
            - point_id: FH_RUN
              point_name: 排风运行
              point_type: DI
          alarms:
            - point_id: ALM_FH_LOW_VELOCITY
              point_name: 面风速过低
              point_type: DI
              severity: HIGH
      
        location_hint:
          space_type: 化学实验室

    sink_nodes:
  
      - node_id: MED-LAB_SNK_LABS
        node_name: 检验实验室
        node_name_en: Clinical Laboratories
        node_type: Sink_Node
        node_category: SNK
      
        function: 临床检验操作空间
        medium_in: AIR + WATER + ELEC
        medium_out: LABORATORY_ENVIRONMENT
      
        is_boundary_output: true
      
        multiplicity: multiple
      
        equipment_parameters:
          lab_types:
            clinical_chemistry:
              name: 临床化学实验室
              equipment: 生化分析仪
              water: 纯水
              exhaust: 一般排风
            hematology:
              name: 血液学实验室
              equipment: 血细胞分析仪
              water: 纯水
            microbiology:
              name: 微生物实验室
              equipment: 培养箱、生物安全柜
              biosafety: BSL-2
              exhaust: HEPA过滤排风
            molecular:
              name: 分子生物学实验室
              equipment: PCR仪、测序仪
              biosafety: BSL-2
              special: 分区布局（防污染）
            immunology:
              name: 免疫学实验室
              equipment: 化学发光仪
              water: 超纯水
          common_requirements:
            - 稳定电源（UPS）
            - 纯水供应
            - 实验台排水
            - 通风系统
          
        location_hint:
          space_type: 检验科

  edges:

    water_edges:
      - edge_id: MED-LAB_EDGE_001
        edge_name: 市政水至纯水站
        edge_type: PIP
        from_node: MED-LAB_SRC_WATER
        to_node: MED-LAB_DST_PURE_WATER
        direction: unidirectional
        medium: WATER-PW
      
      - edge_id: MED-LAB_EDGE_002
        edge_name: 纯水至实验室
        edge_type: PIP
        from_node: MED-LAB_DST_PURE_WATER
        to_node: MED-LAB_SNK_LABS
        direction: unidirectional
        medium: WATER-PURE
        pipe_parameters:
          material: PVDF/不锈钢316L
          note: 避免污染

    exhaust_edges:
      - edge_id: MED-LAB_EDGE_011
        edge_name: 生物安全柜至排风
        edge_type: DUC
        from_node: MED-LAB_DST_BSC
        to_node: MED-LAB_DST_EXHAUST
        direction: unidirectional
        medium: AIR-FILTERED
        duct_parameters:
          material: 不锈钢
          note: 气密性要求高
        
      - edge_id: MED-LAB_EDGE_012
        edge_name: 通风柜至排风
        edge_type: DUC
        from_node: MED-LAB_DST_FUME_HOOD
        to_node: MED-LAB_DST_EXHAUST
        direction: unidirectional
        medium: AIR-EXHAUST

    wastewater_edges:
      - edge_id: MED-LAB_EDGE_021
        edge_name: 实验室废水至处理站
        edge_type: PIP
        from_node: MED-LAB_SNK_LABS
        to_node: MED-LAB_DST_WASTEWATER
        direction: unidirectional
        medium: WATER-WASTE
        pipe_parameters:
          material: HDPE/UPVC
          note: 耐腐蚀

  typical_paths:

    - path_id: MED-LAB_PATH_PURE_WATER
      path_name: 纯水供应路径
      path_type: WAT
      sequence:
        - step: 1
          node: MED-LAB_SRC_WATER
          action: 市政供水
        - step: 2
          node: MED-LAB_DST_PURE_WATER
          action: RO+EDI处理
        - step: 3
          node: MED-LAB_SNK_LABS
          action: 供应实验室

    - path_id: MED-LAB_PATH_BSC_EXHAUST
      path_name: 生物安全柜排风路径
      path_type: HVAC
      sequence:
        - step: 1
          node: MED-LAB_DST_BSC
          action: HEPA过滤
        - step: 2
          node: MED-LAB_DST_EXHAUST
          action: 排风机排出
        - step: 3
          action: 室外高空排放

  control_logic:

    pure_water_control:
      name: 纯水系统控制
    
      production:
        trigger: 储水箱液位<50%
        action: 启动制水
        stop: 储水箱液位>90%
      
      quality_control:
        monitoring: 电导率实时监测
        action:
          conductivity_high: 排放至废水，不供应
          conductivity_normal: 正常供应
        
    lab_ventilation_control:
      name: 实验室通风控制
    
      general_lab:
        mode: 定风量或VAV
        pressure: 微正压或常压
      
      biosafety_lab:
        mode: VAV变风量
        pressure: 负压
        control: 送排风联动
        interlock: 排风先开后关
      
    fume_hood_control:
      name: 通风柜控制
    
      vav_control:
        method: 根据门位置调节排风量
        principle: 维持面风速0.5m/s
      
      alarm:
        low_velocity:
          threshold: {value: 0.3, unit: "m/s"}
          action: 声光报警
          meaning: 防护不足
        
    wastewater_control:
      name: 废水处理控制
    
      batch_treatment:
        trigger: 集水池液位>70%
        sequence:
          - 中和（调pH至6-9）
          - 氧化（加药）
          - 消毒（加氯）
          - 沉淀
          - 排放（合格后）
        
      quality_check:
        before_discharge:
          - pH: 6-9
          - COD: <300mg/L（三级标准）
        if_unqualified: 回流再处理

  alarm_protection:

    water_system_alarms:
      - alarm_id: ALM_PW_QUALITY
        alarm_name: 纯水水质不合格
        severity: HIGH
        trigger: 电导率超标
        action: 停止供水，检查系统
      
      - alarm_id: ALM_PW_TANK_LOW
        alarm_name: 纯水箱液位低
        severity: MEDIUM
        trigger: 液位<20%
        action: 加快制水
      
    ventilation_alarms:
      - alarm_id: ALM_BSC_AIRFLOW
        alarm_name: 生物安全柜气流异常
        severity: HIGH
        trigger: 下降气流<0.25m/s
        action: 停止操作，检修
      
      - alarm_id: ALM_FH_LOW_VELOCITY
        alarm_name: 通风柜面风速低
        severity: HIGH
        trigger: 面风速<0.3m/s
        action: 停止操作
      
      - alarm_id: ALM_LAB_PRESSURE
        alarm_name: BSL实验室正压
        severity: CRITICAL
        trigger: BSL-2实验室压力>0Pa
        action: 立即检查排风系统
      
    wastewater_alarms:
      - alarm_id: ALM_WW_PH
        alarm_name: 废水pH超标
        severity: HIGH
        trigger: pH<5或pH>10
        action: 禁止排放
      
      - alarm_id: ALM_WW_OVERFLOW
        alarm_name: 集水池溢流
        severity: CRITICAL
        trigger: 液位>95%
        action: 紧急排放/停止排水

  dependencies:
  
    upstream_dependencies:
      - dependency_id: DEP_LAB_WATER
        from_system: PLUMB-DWS
        dependency_type: WATER_SUPPLY
        criticality: HIGH
      
      - dependency_id: DEP_LAB_HVAC
        from_system: HVAC-AHU
        dependency_type: VENTILATION
        criticality: HIGH
      
      - dependency_id: DEP_LAB_POWER
        from_system: ELEC-LV
        dependency_type: POWER_SUPPLY
        criticality: HIGH
        backup: UPS
      
    downstream_dependencies:
      - dependency_id: DEP_TO_WASTEWATER
        to_system: PLUMB-SAN
        dependency_type: DRAINAGE
        criticality: HIGH
        note: 经处理后排入污水系统
```

---

# 第四批次输出完成

## 本批次系统总结

| 系统ID | 系统名称 | 类别 | 优先级 |
|--------|----------|------|--------|
| FIRE-FAS | 火灾自动报警系统 | 消防 | P0-生命安全 |
| FIRE-SPS | 消防给水系统 | 消防 | P0-生命安全 |
| FIRE-EXH | 防排烟系统 | 消防 | P0-生命安全 |
| MED-OR | 手术室环境控制系统 | 医疗专业 | P1-任务关键 |
| MED-ICU | 重症监护环境系统 | 医疗专业 | P1-任务关键 |
| MED-LAB | 检验科专用系统 | 医疗专业 | P2-业务关键 |

## 关键联动关系

```
FIRE-FAS（火灾报警）
  ├── → FIRE-SPS（消防泵联动）
  ├── → FIRE-EXH（防排烟联动）
  ├── → INT-BA（空调联动关闭）
  ├── → INT-SEC（门禁联动释放）
  └── → ELEC-LV（非消防电源切断）

MED-OR/ICU（洁净环境）
  ├── ← HVAC-CHP（冷热源）
  ├── ← MGAS（医用气体）
  ├── ← ELEC-EPS（应急电源）
  └── → INT-BA（环境监控）
```

---

# 第四批次修订版：问题修复与补充

## 修订说明

根据您提出的5个中等优先级问题，我将逐一进行修复和补充。

---

## 问题1修复：FIRE-FAS与INT-BA/INT-NUR的报警优先级完善

```yaml
Unified_Alarm_Priority_Framework:

  identity:
    name: 医院机电系统统一报警优先级框架
    description: 定义所有系统报警的优先级和共存处理规则
    version: 2.0
    last_updated: 2024
    note: 整合第三批次和第四批次的报警优先级定义

  # ========================================
  # 报警等级定义（完整版）
  # ========================================
  alarm_levels:
  
    level_0_life_safety:
      name: 生命安全级
      priority: 最高
      systems:
        - FIRE-FAS: 火灾报警
        - MGAS-O2: 氧气中断/危急低压
        - ELEC-EPS: 全院失电（发电机也失效）
      display:
        mode: 全屏闪烁
        color: 红色
        animation: 持续闪烁（1Hz）
      audio:
        type: 火警音/紧急警报
        volume: 最大
        mute_allowed: false
      override: 不可被任何其他报警覆盖
    
    level_1_patient_emergency:
      name: 患者紧急级
      priority: 次高
      systems:
        - INT-NUR: 紧急呼叫（红色按钮）
        - MGAS: 气体低压预警
      display:
        mode: 主显示区（如有Level_0则缩小显示）
        color: 红色/橙色
        animation: 闪烁（0.5Hz）
      audio:
        type: 紧急呼叫音
        volume: 高
        mute_allowed: true
        mute_duration: {value: 60, unit: s}
      override: 可被Level_0部分覆盖
    
    level_2_critical_equipment:
      name: 关键设备级
      priority: 中高
      systems:
        - INT-SEC: 入侵报警
        - INT-BA: 关键设备故障（冷机/水泵）
        - ELEC: 市电单路故障
        - PLUMB: 供水中断
      display:
        mode: 次要显示区
        color: 橙色/黄色
      audio:
        type: 设备报警音
        volume: 中
        mute_allowed: true
      override: 可被Level_0/1覆盖
    
    level_3_warning:
      name: 警告级
      priority: 中
      systems:
        - INT-NUR: 普通呼叫（黄色按钮）
        - INT-BA: 参数异常
        - HVAC: 温度偏差
      display:
        mode: 状态栏/列表
        color: 黄色
      audio:
        type: 提示音
        volume: 低
        mute_allowed: true
      
    level_4_info:
      name: 信息级
      priority: 最低
      systems:
        - 维护提醒
        - 护理确认
        - 一般事件
      display:
        mode: 日志/通知区
        color: 蓝色/灰色
      audio:
        type: 无或轻微提示
    
  # ========================================
  # 报警共存处理规则
  # ========================================
  alarm_coexistence:
  
    scenario_1_fire_and_emergency_call:
      trigger: 火灾报警 AND 紧急呼叫 同时发生
      probability: 低但非零（火灾时患者可能按紧急按钮）
    
      handling:
        display_layout:
          main_area: 火灾报警（占80%屏幕）
          sub_area: 紧急呼叫信息（右下角20%）
          switch_allowed: false（火灾期间不允许切换到其他视图）
        
        audio_handling:
          primary: 火灾警报音
          secondary: 紧急呼叫音（降低音量）
          mixing: 交替播放（火灾5秒 + 呼叫1秒）
        
        notification:
          fire_team: 消防控制室/119
          medical_team: 护士站/值班医生
          content: |
            火灾地点：{火灾区域}
            同时发生紧急呼叫：{床位号}
            请协调处理
          
        action_priority:
          step_1: 通知消防人员处理火灾
          step_2: 通知医护人员评估紧急呼叫患者
          step_3: 如火灾区域与呼叫区域相同，优先疏散患者
          step_4: 记录两个事件的时间戳和处理过程
        
      note: 火灾疏散优先，但不能忽视患者紧急情况
    
    scenario_2_fire_and_equipment_fault:
      trigger: 火灾报警 AND 设备故障 同时发生
    
      handling:
        display_layout:
          main_area: 火灾报警（100%）
          sub_area: 设备故障信息隐藏（后台记录）
        
        action:
          - 火灾处理完成后再处理设备故障
          - 设备故障不显示，但会记录到日志
        
    scenario_3_multiple_emergency_calls:
      trigger: 多个紧急呼叫 同时发生
    
      handling:
        display_layout:
          mode: 列表显示（按时间顺序）
          highlight: 最新呼叫闪烁
        
        audio_handling:
          mode: 单一报警音（不重叠）
          count_indication: 语音提示"有{N}个紧急呼叫"
        
        action:
          - 按呼叫时间顺序响应
          - 或按患者危重程度响应（需人工判断）
        
    scenario_4_gas_alarm_and_fire:
      trigger: 医用气体报警 AND 火灾 同时发生
    
      handling:
        display: 同时显示（均为Level_0/1）
        action:
          - 火灾处理优先
          - 医用气体报警同步处理（防止氧气助燃）
          - 通知气体系统操作员准备关闭气源
        
  # ========================================
  # 显示屏幕分区规则
  # ========================================
  display_partition:
  
    normal_mode:
      main_area: 80%（系统状态总览）
      alarm_area: 15%（报警列表）
      status_bar: 5%（时间/通讯状态）
    
    level_0_alarm_mode:
      main_area: 100%（火灾报警全屏）
      sub_window: 右下角可缩小显示其他Level_1报警
    
    level_1_alarm_mode:
      main_area: 60%（报警详情）
      alarm_list: 30%（其他报警列表）
      status_bar: 10%
    
  # ========================================
  # 报警音频混合规则
  # ========================================
  audio_mixing:
  
    max_simultaneous_sounds: 2
    mixing_rules:
      - 不同级别：高级别压制低级别
      - 同级别：交替播放
      - Level_0：独占音频输出
    
    volume_reduction:
      when_coexisting:
        primary: 100%
        secondary: 50%
```

---

## 问题2修复：FIRE-SPS消防泵智能停泵逻辑

```yaml
# 在FIRE-SPS系统中补充以下内容

FIRE_SPS_Pump_Stop_Logic:

  identity:
    name: 消防泵停泵控制逻辑
    description: 定义消防泵停止的条件和流程
    version: 1.1
  
  # ========================================
  # 停泵原则
  # ========================================
  stop_principles:
  
    basic_rule: |
      消防泵不设自动停泵保护（过载除外）
      只允许手动停泵
      目的：防止火灾期间泵被误关闭
    
    exceptions:
      - 280℃防火阀熔断导致的系统隔离
      - 主控制器发出的紧急停泵命令
      - 消防水池极低液位保护（防泵干烧）
    
  # ========================================
  # 手动停泵流程
  # ========================================
  manual_stop_procedure:
  
    authorized_personnel:
      - 消防控制室值班人员
      - 消防队负责人
      - 医院安全管理员
    
    stop_sequence:
      step_1:
        action: 现场确认火灾已扑灭
        verifier: 消防队/安全员
        documentation: 填写《火灾扑灭确认单》
      
      step_2:
        action: 消防控制室发出停泵预警
        display: 显示"准备停泵，请确认"
        duration: {value: 5, unit: min, note: "预警等待时间"}
      
      step_3:
        action: 现场再次确认无复燃风险
        method: 
          - 红外热成像检查
          - 人工巡查
      
      step_4:
        action: 消防队长/安全员签字确认
        document: 《消防泵停泵确认书》
        content:
          - 火灾时间
          - 扑灭时间
          - 确认人员签字
          - 停泵授权
        
      step_5:
        action: 消防控制室执行手动停泵
        operator: 值班人员
        record: 系统自动记录停泵时间
      
      step_6:
        action: 系统切换至稳压模式
        pump: 稳压泵恢复自动运行
        pressure: 维持系统常备压力
      
    minimum_duration:
      from_alarm_reset: {value: 30, unit: min}
      note: 火灾报警复位后至少运行30分钟
    
  # ========================================
  # 智能降速保护
  # ========================================
  intelligent_speed_reduction:
  
    purpose: 防止长时间高压运行造成水管爆裂和水资源浪费
  
    trigger_conditions:
      condition_1:
        name: 火灾报警信号复位超时
        trigger: 火灾报警复位 > 60分钟
        and: 无水流指示器动作（无喷淋动作）
      
      condition_2:
        name: 系统压力持续高压
        trigger: 出口压力 > 设计压力120%
        duration: > 30分钟
      
    action:
      mode: 自动降速至稳压模式
      speed: 降至额定转速30%
      pressure: 维持0.8-1.0MPa
    
    restrictions:
      - 如有水流指示器动作，不降速
      - 如有手动报警，不降速
      - 仅作为防水损保护，不替代正常停泵
    
    alarm:
      type: 提醒
      message: "消防泵已自动降速，请确认是否需要停泵"
    
  # ========================================
  # 干烧保护
  # ========================================
  dry_run_protection:
  
    trigger:
      water_tank_level: < 10%
      or: 吸水管压力 < 0.02MPa
    
    action:
      step_1: 发出"消防水源不足"报警
      step_2: 延时30秒
      step_3: 如液位仍低，自动停泵（防干烧）
      step_4: 报警升级为"消防泵干烧保护停泵"
    
    recovery:
      condition: 液位恢复 > 30%
      action: 允许手动重启
      note: 不自动启动，需人工确认
    
  # ========================================
  # 停泵后检查
  # ========================================
  post_stop_inspection:
  
    immediate:
      - 检查管网有无泄漏
      - 检查阀门状态
      - 检查稳压系统恢复正常
    
    within_24h:
      - 消防泵试运行测试
      - 记录运行时长和能耗
      - 检查水箱补水情况
    
    documentation:
      - 火灾事件报告
      - 消防泵运行记录
      - 停泵确认书存档
```

---

## 问题3修复：MED-OR/MED-ICU季节性参数调整

```yaml
# 在MED-OR和MED-ICU系统中补充以下内容

Seasonal_Environmental_Control:

  identity:
    name: 洁净环境季节性控制策略
    description: 根据季节和室外条件调整手术室/ICU环境参数
    version: 1.0
    applicable_systems:
      - MED-OR
      - MED-ICU
    
  # ========================================
  # 季节模式定义
  # ========================================
  seasonal_modes:
  
    winter_mode:
      trigger:
        outdoor_temp: {value: "<5", unit: ℃}
        duration: {value: 24, unit: h, note: "持续低温"}
        or: 手动切换
      
      parameters:
        MED-OR:
          temperature:
            default: {value: 25, unit: ℃}
            range: {value: "23-27", unit: ℃}
          humidity:
            default: {value: 50, unit: "%RH"}
            range: {value: "45-55", unit: "%RH"}
          fresh_air:
            mode: 最小新风量
            reason: 减少加热能耗
          
        MED-ICU:
          temperature:
            default: {value: 25, unit: ℃}
            range: {value: "24-26", unit: ℃}
          humidity:
            default: {value: 50, unit: "%RH"}
            range: {value: "45-55", unit: "%RH"}
          
      control_adjustments:
        heating_priority: 高
        cooling_priority: 低
        humidification: 需加强（冬季干燥）
        note: 北方地区尤其需要加湿
      
    summer_mode:
      trigger:
        outdoor_temp: {value: ">28", unit: ℃}
        duration: {value: 24, unit: h}
        or: 手动切换
      
      parameters:
        MED-OR:
          temperature:
            default: {value: 23, unit: ℃}
            range: {value: "21-25", unit: ℃}
          humidity:
            default: {value: 50, unit: "%RH"}
            range: {value: "45-55", unit: "%RH"}
            note: 南方需加强除湿
          
        MED-ICU:
          temperature:
            default: {value: 24, unit: ℃}
            range: {value: "22-26", unit: ℃}
          humidity:
            default: {value: 50, unit: "%RH"}
          
      control_adjustments:
        cooling_priority: 高
        heating_priority: 低
        dehumidification: 需加强（夏季湿度高）
        fresh_air: 可增加（利用全热回收）
      
    transition_mode:
      trigger:
        outdoor_temp: {value: "5-28", unit: ℃}
        season: 春季（3-4月）或秋季（10-11月）
      
      parameters:
        MED-OR:
          temperature:
            default: {value: 24, unit: ℃}
            range: {value: "22-26", unit: ℃}
          humidity:
            default: {value: 50, unit: "%RH"}
            range: {value: "40-60", unit: "%RH"}
          
      control_adjustments:
        mode: 自动切换冷热
        deadband: {value: 2, unit: ℃, note: "防止频繁切换"}
        fresh_air: 可利用自然冷源
      
    extreme_cold_mode:
      trigger:
        outdoor_temp: {value: "<-10", unit: ℃}
        region: 北方/高寒地区
      
      parameters:
        MED-OR:
          temperature:
            default: {value: 26, unit: ℃}
            range: {value: "24-28", unit: ℃}
          humidity:
            default: {value: 55, unit: "%RH"}
            note: 更高湿度补偿室内干燥
          
      control_adjustments:
        fresh_air: 最小新风（仅满足换气）
        preheating: 加强新风预热
        humidification: 最大能力运行
        anti_freeze: 启用防冻保护
      
    high_humidity_mode:
      trigger:
        outdoor_humidity: {value: ">80", unit: "%RH"}
        region: 南方/沿海地区
        season: 梅雨季节
      
      parameters:
        MED-OR:
          humidity:
            target: {value: 50, unit: "%RH"}
            max_allowed: {value: 60, unit: "%RH"}
          
      control_adjustments:
        dehumidification: 最大能力
        reheat: 必要时再热（除湿后升温）
        fresh_air: 适当减少（减少湿负荷）
      
  # ========================================
  # 季节切换策略
  # ========================================
  mode_transition:
  
    automatic_switch:
      enabled: true
      based_on: 室外温度24小时平均值
      smooth_transition: true
    
    transition_period:
      duration: {value: "2-3", unit: "周"}
      method: 逐步调整参数
      step:
        temperature: {value: 0.5, unit: "℃/天"}
        humidity: {value: 2, unit: "%RH/天"}
      note: 避免参数突变造成设备冲击
    
    manual_override:
      allowed: true
      authority: 设备管理人员
      log: 记录切换原因和时间
    
  # ========================================
  # 地区差异配置
  # ========================================
  regional_settings:
  
    north_china:
      winter_duration: 11月-3月
      key_challenges:
        - 低温
        - 干燥
      focus: 加热+加湿
    
    south_china:
      summer_duration: 5月-10月
      key_challenges:
        - 高温
        - 高湿
      focus: 冷却+除湿
    
    coastal:
      year_round:
        humidity: 高
        salt_corrosion: 需考虑
      focus: 除湿+防腐
    
    plateau:
      altitude: {value: ">2000", unit: m}
      key_challenges:
        - 低气压
        - 温差大
      focus: 压力补偿（可选）
    
  # ========================================
  # 能耗优化
  # ========================================
  energy_optimization:
  
    free_cooling:
      trigger: 室外温度 < 室内设定-3℃
      action: 增加新风比例
      benefit: 减少机械制冷
    
    heat_recovery:
      type: 全热交换器
      efficiency: {value: ">70", unit: "%"}
      benefit: 回收排风能量
    
    night_setback:
      applicable: 非手术时段
      temperature_range: 放宽至 20-28℃
      humidity_range: 放宽至 35-65%RH
      note: 手术前30分钟恢复标准参数
```

---

## 问题4修复：消防系统与医用气体的交互

```yaml
Fire_Medical_Gas_Coordination:

  identity:
    name: 消防与医用气体系统协调规范
    description: 定义火灾情况下医用气体系统的处理策略
    version: 1.0
  
  # ========================================
  # 氧气储存区火灾防护
  # ========================================
  oxygen_storage_fire_protection:
  
    storage_type:
      liquid_oxygen:
        location: 室外独立区域
        distance_to_building: {value: "≥7.5", unit: m}
        fire_protection:
          - 周边设置隔离带
          - 远离可燃物
          - 设置消火栓（手动灭火）
          - 禁止使用水喷淋（液氧低温危险）
        special_agent: 干粉灭火器（附近配置）
      
      cylinder_manifold:
        location: 室内汇流排间
        fire_protection:
          - 独立防火分区
          - 耐火极限≥2h
          - 设置喷淋系统（标准喷淋）
          - 设置手提CO2灭火器
          - 气体泄漏检测器
        ventilation:
          type: 机械排风
          rate: {value: 12, unit: "次/h"}
          purpose: 防止气体积聚
        
    fire_scenario_response:
      scenario: 氧气储存区着火
    
      immediate_actions:
        step_1:
          action: 触发火灾报警
          system: FIRE-FAS
        
        step_2:
          action: 关闭氧气源阀门
          method: 手动（液氧区）/ 电动阀（汇流排）
          executor: 医用气体值班人员
          note: 切断气源防止火势扩大
        
        step_3:
          action: 切换至备用气源
          if_available: 另一组汇流排
          notification: 广播"氧气源切换，临床注意"
        
        step_4:
          action: 启用床旁备用氧气瓶
          duration: {value: 15, unit: min, note: "典型床旁氧气瓶"}
          applicable: 手术室、ICU患者
        
        step_5:
          action: 消防队灭火
          method: 干粉/CO2（氧气区专用）
          avoid: 不使用水（液氧区）
        
    supply_continuity:
      principle: 医用氧气不能中断
      backup_layers:
        layer_1: 管道切换至备用汇流排
        layer_2: 床旁氧气瓶
        layer_3: 转运氧气瓶
      max_interruption: {value: 0, unit: min, note: "不允许中断"}
    
  # ========================================
  # 手术室/ICU火灾时的医用气体处理
  # ========================================
  clinical_area_fire_gas_handling:
  
    scenario_1:
      name: 火灾发生在手术室
    
      immediate_actions:
        hvac:
          - 关闭手术室新风
          - 启动排烟（如该区域有）
        
        medical_gas:
          - 氧气继续供应（不能停）
          - 负压吸引继续供应
          - 压缩空气继续供应
          note: 手术中患者可能正在使用呼吸机
        
        patient_handling:
          option_1: 
            condition: 火灾可控，患者可继续手术
            action: 密切监测，准备转移
          option_2:
            condition: 火灾严重，需立即转移
            action: |
              1. 使用便携式呼吸机
              2. 携带氧气瓶
              3. 转移至安全区域手术室
              4. 记录转移时间
            
        gas_source_check:
          - 确认气源区域未受火灾影响
          - 如气源区域有风险，准备切换
        
    scenario_2:
      name: 火灾发生在ICU
    
      immediate_actions:
        similar_to: 手术室火灾处理
      
        additional:
          - ICU患者多数依赖呼吸机
          - 优先保障氧气和负压
          - 准备便携式设备
        
        evacuation_gas:
          transfer_equipment:
            - 便携式呼吸机
            - 氧气瓶
            - 手动复苏器
          oxygen_duration: {value: 30, unit: min, note: "每个氧气瓶"}
        
    scenario_3:
      name: 火灾发生在普通病区（非气体依赖区）
    
      gas_handling:
        action: 按正常疏散程序
        gas_system: 无特殊处理
        note: 普通病区患者通常不依赖管道气体
      
  # ========================================
  # 冷却水优先级
  # ========================================
  cooling_water_priority:
  
    context: |
      消防用水、空调用水、医用气体冷却水可能共用水源
      火灾时可能造成水压下降
    
    priority_order:
      priority_1:
        use: 消防灭火
        system: FIRE-SPS
        note: 最高优先级，生命安全
      
      priority_2:
        use: 手术室/ICU空调
        system: MED-OR, MED-ICU
        note: 维持关键医疗区域环境
      
      priority_3:
        use: 医用气体压缩机冷却
        system: MGAS-AIR
        note: 可短时承受温度升高
      
      priority_4:
        use: 一般空调
        system: HVAC
        note: 可暂时降低或停止
      
    water_shortage_response:
      trigger: 消防水池液位 < 50%
      or: 冷却水供水压力 < 0.15MPa
    
      actions:
        step_1:
          action: 停止一般空调冷却塔补水
          saving: 约30%用水量
        
        step_2:
          action: MGAS-AIR压缩机进入保护模式
          method: 降低运行负荷
          temperature: 允许升高至80℃
        
        step_3:
          action: 确保消防用水优先
          method: 消防水池独立供水
        
        step_4:
          action: 手术室/ICU冷水由备用冷水机供应
          if_available: 独立冷源
        
  # ========================================
  # 联动信号定义
  # ========================================
  linkage_signals:
  
    fire_to_mgas:
      signal_1:
        name: FIRE_ALARM_GAS_AREA
        meaning: 气体区域火灾报警
        from: FIRE-FAS
        to: MGAS监控系统
        action: 准备切换气源
      
      signal_2:
        name: FIRE_ALARM_CLINICAL
        meaning: 临床区域火灾报警
        from: FIRE-FAS
        to: MGAS监控系统
        action: 监测气体供应，准备备用设备
      
    mgas_to_fire:
      signal_1:
        name: GAS_LEAK_ALARM
        meaning: 气体泄漏报警
        from: MGAS
        to: FIRE-FAS
        action: 加强该区域火灾监测
        note: 氧气泄漏增加火灾风险
      
  # ========================================
  # 培训和演练要求
  # ========================================
  training_requirements:
  
    personnel:
      - 消防控制室值班人员
      - 医用气体值班人员
      - 手术室/ICU护士长
      - 设备科人员
    
    drill_frequency:
      fire_gas_coordination: 每年1次
      content:
        - 火灾报警响应
        - 气源切换操作
        - 床旁氧气瓶使用
        - 患者转移演练（模拟）
      
    documentation:
      - 演练记录
      - 问题整改
      - 预案更新
```

---

## 问题5修复：FIRE-EXH排烟风机高温保护与应急措施

```yaml
# 在FIRE-EXH系统中补充以下内容

High_Temperature_Protection_Strategy:

  identity:
    name: 防排烟系统高温保护与应急策略
    description: 定义排烟系统在高温下的保护措施和应急方案
    version: 1.1
  
  # ========================================
  # 排烟风机耐温设计
  # ========================================
  exhaust_fan_temperature_rating:
  
    design_parameters:
      rated_temperature: {value: 280, unit: ℃}
      rated_duration: {value: 0.5, unit: h, note: "30分钟"}
      standard: GB 13935《消防排烟风机耐高温试验方法》
    
    temperature_timeline:
      0-10min:
        expected_temp: {value: "100-200", unit: ℃}
        fan_status: 正常运行
      
      10-20min:
        expected_temp: {value: "200-280", unit: ℃}
        fan_status: 正常运行
        note: 火灾应在此期间被控制
      
      20-30min:
        expected_temp: {value: "~280", unit: ℃}
        fan_status: 临界运行
        alarm: 排烟温度接近极限
      
      30min+:
        expected_temp: {value: ">280", unit: ℃}
        fan_status: 可能损坏
        action: 防火阀熔断，风机停止
      
    design_margin:
      actual_capacity: 通常可耐受300℃短时
      note: 但不作为设计依据
    
  # ========================================
  # 280℃防火阀熔断后的应急措施
  # ========================================
  post_fusible_link_activation:
  
    trigger:
      condition: 排烟防火阀温度达到280℃
      action: 易熔片熔断，阀门自动关闭
    
    immediate_consequences:
      排烟通道: 关闭
      排烟风机: 联锁停止
      机械排烟: 失效
    
    backup_measures:
    
      natural_smoke_exhaust:
        description: 自然排烟作为应急补充
        components:
          - 可开启外窗
          - 排烟天窗
          - 中庭自然排烟口
        activation:
          method: 自动/手动开启
          trigger: 机械排烟失效信号
        effectiveness:
          compared_to_mechanical: {value: "30-50", unit: "%"}
          note: 远低于机械排烟，仅作为应急
        
      emergency_windows:
        location: 每个防火分区
        area: {value: "≥2", unit: "%", note: "楼地面积的2%"}
        operation:
          automatic: 收到信号自动开启
          manual: 手动把手
        opening_height: {value: "≥1.0", unit: m}
      
      smoke_shaft:
        description: 自然排烟竖井
        location: 中心位置
        cross_section: 根据层数和面积计算
        operation: 被动排烟（热压驱动）
      
    fire_service_support:
      description: 消防队正压送风排烟
      method:
        - 消防车正压风机
        - 从楼梯间向建筑内送正压空气
        - 推动烟气从破损窗口排出
      effectiveness: 中等
      note: 需消防队现场操作
    
  # ========================================
  # 排烟管道高温保护
  # ========================================
  smoke_duct_protection:
  
    duct_construction:
      material: 镀锌钢板
      thickness: {value: "1.2-2.0", unit: mm}
      fire_resistance: {value: 1.0, unit: h}
    
    insulation:
      material: 岩棉（A级不燃）
      thickness: {value: 50, unit: mm}
      density: {value: "≥80", unit: "kg/m³"}
      facing: 铝箔贴面
    
    high_temperature_test:
      requirement: 
        temperature: {value: 280, unit: ℃}
        duration: {value: 0.5, unit: h}
      additional:
        short_term: 可耐受1000℃冲击（<5分钟）
        standard: GB 50016对排烟管道的要求
      
    insulation_degradation:
      risk: 长期高温可能导致保温层脱落
      prevention:
        - 使用耐高温固定件
        - 定期检查保温层完整性
        - 保温层外加保护罩
      
    inspection:
      frequency: 每年1次
      content:
        - 保温层完整性
        - 固定件牢固性
        - 管道密封性
        - 防火阀动作灵活性
      
  # ========================================
  # 超时运行保护
  # ========================================
  extended_operation_protection:
  
    design_assumption:
      fire_control_time: {value: "<30", unit: min}
      note: 火灾应在30分钟内被控制
    
    if_fire_exceeds_30min:
    
      scenario_analysis:
        cause:
          - 大型火灾
          - 可燃物过多
          - 消防系统故障
          - 消防队响应延迟
        
      system_behavior:
        排烟风机: 已停止（防火阀熔断）
        机械排烟: 失效
        building_response:
          - 依靠自然排烟
          - 疏散应已完成
          - 消防队现场灭火
        
      documented_expectation: |
        设计假设火灾在30分钟内被控制
        超过30分钟属于极端情况
        此时人员应已疏散完成
        消防队接管灭火工作
      
    monitoring:
      exhaust_temp_alarm:
        threshold_1: {value: 200, unit: ℃}
        action_1: 预警
        threshold_2: {value: 260, unit: ℃}
        action_2: 警告"接近极限"
        threshold_3: {value: 280, unit: ℃}
        action_3: 防火阀熔断
      
      duration_alarm:
        threshold: {value: 25, unit: min}
        action: 提醒"排烟系统接近设计极限"
      
  # ========================================
  # 应急预案要点
  # ========================================
  emergency_plan_highlights:
  
    mechanical_exhaust_failure:
      name: 机械排烟失效应急预案
    
      trigger:
        - 排烟防火阀熔断
        - 排烟风机故障
        - 排烟管道严重损坏
      
      actions:
        step_1:
          action: 确认人员疏散进度
          target: 确保所有人员已撤离着火区
        
        step_2:
          action: 开启应急排烟窗口
          method: 自动/手动
          location: 着火层及相邻层
        
        step_3:
          action: 消防队设置排烟点
          method: 选择合适窗口进行破拆排烟
        
        step_4:
          action: 加强楼梯间加压
          method: 维持加压送风
          purpose: 防止烟气进入疏散通道
        
        step_5:
          action: 消防队正压送风
          method: 消防车风机
          location: 楼梯间入口
        
    drill_requirements:
      frequency: 每年1次
      content:
        - 模拟排烟系统故障
        - 应急窗口开启测试
        - 消防队配合演练
      
  # ========================================
  # 设计优化建议
  # ========================================
  design_recommendations:
  
    redundancy:
      suggestion: 关键区域设置双排烟系统
      applicable: 大型医院、高层医院
      method:
        - 两组独立排烟风机
        - 两条独立排烟管道
        - 任一系统可独立运行
      
    enhanced_natural_exhaust:
      suggestion: 增加自然排烟能力
      method:
        - 增加可开启外窗面积
        - 设置排烟天窗
        - 中庭设计考虑烟气控制
      
    early_detection:
      suggestion: 采用极早期烟雾探测
      method:
        - 吸气式烟感
        - 空气采样探测
      benefit: 更早发现火灾，减少烟气产生
    
    smoke_compartmentation:
      suggestion: 缩小防烟分区
      method: 防烟分区<400m²
      benefit: 限制烟气扩散范围
```

---

## 
