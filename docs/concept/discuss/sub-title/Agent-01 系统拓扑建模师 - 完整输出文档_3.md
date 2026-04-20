## 🧑‍💻 User


继续输出第四批次

---
## 🤖 Assistant


# Agent-01 系统拓扑建模师 - 完整输出文档

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

---