## 🧑‍💻 User


你卡在了【equipment_parameters:
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
 point_name】，继续生成

---
## 🤖 Assistant


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

**第五批次预告：** 将输出暖通系统详细设计（HVAC-CHP冷热源、HVAC-AHU空调机组、HVAC-FCU风机盘管）和电气系统补充（ELEC-EL电梯系统）。

请确认第四批次内容后，我将继续输出第五批次。

---