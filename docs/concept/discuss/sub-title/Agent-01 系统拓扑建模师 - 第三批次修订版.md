## 🧑‍💻 User




---
## 🤖 Assistant


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
 interface_id: IF

---