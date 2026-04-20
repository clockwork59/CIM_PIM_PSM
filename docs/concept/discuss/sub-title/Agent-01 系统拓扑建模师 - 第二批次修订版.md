## 🧑‍💻 User


立即对第二部分展开修订

---
## 🤖 Assistant


# Agent-01 系统拓扑建模师 - 第二批次修订版

## 修订说明

根据评审意见，本次修订重点解决以下高优先级缺陷：
- **E1**: 发电机黑启动失败处理逻辑
- **E2**: UPS电池SOC分级管理
- **E3**: 低压系统黑启动详细时序
- **G1**: 医用气体备用源耗尽保护
- **G2**: 医用气体终端反向污染防护
- **G3**: 医用氧气纯度监测
- **G4**: 手术室O2/VAC协调逻辑
- **E4**: 变压器冷却系统控制

---

# 电气系统（修订版）

## 系统 2.1: ELEC-HV 高压配电系统（修订版 - 关键补充）

在原有内容基础上，补充以下控制逻辑：

```yaml
  # ========================================
  # CONTROL LOGIC SECTION - 控制逻辑（修订补充）
  # ========================================
  control_logic:
  
    # === 原有内容保留 ===
    auto_transfer_switch:
      # ... 原有内容 ...
    
    protection_coordination:
      # ... 原有内容 ...
    
    # === E1修复：高压系统故障恢复逻辑 ===
    fault_recovery_logic:
      name: 高压系统故障恢复逻辑
      description: 双路市电故障后的恢复策略
      
      single_utility_failure:
        description: 单路市电故障
        detection:
          voltage_threshold: "<70%额定值"
          duration: "持续2秒"
        recovery_sequence:
          - step: 1
            action: 故障路进线断路器分闸
            time: 0.5s
          - step: 2
            action: 确认母线失压
            time: 0.3s
          - step: 3
            action: 母联断路器合闸
            time: 0.5s
            condition: 另一路电源正常
          - step: 4
            action: 故障母线恢复供电
            note: 由正常路经母联供电
        total_time: "<3秒"
        
      dual_utility_failure:
        description: 双路市电同时故障
        detection: 两路进线电压均<70%额定值
        action: 立即启动发电机
        escalation: 通知值班人员和电力公司
        
      utility_recovery_after_generator:
        description: 发电机运行中市电恢复
        procedure:
          - step: 1
            action: 确认市电电压/频率稳定
            duration: 30s
          - step: 2
            action: 合闸市电进线断路器
            condition: 市电正常持续30秒
          - step: 3
            action: 同期并列（如允许）或先断后合
            note: 医院通常采用"先断后合"避免并列风险
          - step: 4
            action: 发电机卸载并停机
            delay: 冷却运行3分钟后停机
        mode: 可选自动/手动

    # === 保护动作后的闭锁逻辑 ===
    protection_lockout:
      name: 保护动作闭锁逻辑
      description: 保护动作后防止误合闸
      
      lockout_conditions:
        - 短路保护动作
        - 差动保护动作
        - 接地保护动作
        
      lockout_action:
        - 断路器分闸后闭锁
        - 禁止远程合闸
        - 必须现场人工确认后解锁
        - 故障录波记录保存
        
      unlock_procedure:
        - step: 1
          action: 现场检查故障原因
        - step: 2
          action: 确认故障已排除
        - step: 3
          action: 手动复位保护装置
        - step: 4
          action: 解除闭锁
        - step: 5
          action: 试送电（可远程操作）
```

---

## 系统 2.2: ELEC-LV-MAIN 低压配电主系统（修订版）

```yaml
System_Topology:

  identity:
    system_id: ELEC-LV-MAIN
    system_name: 低压配电主系统
    system_name_en: Low Voltage Main Distribution System
    # ... 原有identity内容保留 ...
    
    version: 2.0
    revision_notes: |
      v2.0: 补充黑启动时序、变压器冷却控制、负荷分级切电
      v1.0: 初始版本

  # ... boundary, nodes, edges 原有内容保留 ...

  # ========================================
  # CONTROL LOGIC SECTION - 控制逻辑（完整修订版）
  # ========================================
  control_logic:
  
    # === E3修复：完整黑启动时序 ===
    black_start_sequence:
      name: 低压系统黑启动时序
      description: 双路市电全失后的应急启动完整流程
      
      trigger:
        condition: 双路市电均失压
        detection: 
          - ATS主电源失压
          - ATS备用电源失压
          - 持续时间>3秒
      
      phase_1_detection:
        name: 失电检测与确认
        steps:
          - step: 1
            time: "T+0s"
            action: ATS检测到主电源失压
            sensor: ATS1_MAIN_AVAIL = OFF
          - step: 2
            time: "T+0.5s"
            action: ATS检测到备用电源也失压
            sensor: ATS1_BACKUP_AVAIL = OFF
          - step: 3
            time: "T+3s"
            action: 确认双路市电全失（防误判）
            condition: 持续3秒无恢复
          - step: 4
            time: "T+3s"
            action: 发送启动信号至发电机控制器
            signal: GEN_START_CMD = ON
      
      phase_2_generator_start:
        name: 发电机启动
        steps:
          - step: 5
            time: "T+3.5s"
            action: 发电机控制器接收启动信号
          - step: 6
            time: "T+4s"
            action: 燃油预供、预热（如有）
          - step: 7
            time: "T+5s"
            action: 启动马达启动发动机
          - step: 8
            time: "T+8s"
            action: 发动机达到额定转速（1500rpm）
            verification: GEN_SPEED ≈ 1500rpm
          - step: 9
            time: "T+10s"
            action: 发电机电压/频率稳定
            verification: |
              GEN_V = 400V ±5%
              GEN_FREQ = 50Hz ±1Hz
      
      phase_3_connection:
        name: 发电机并网
        steps:
          - step: 10
            time: "T+11s"
            action: 发电机出口断路器合闸
            location: 发电机房内
            condition: 电压频率合格
          - step: 11
            time: "T+12s"
            action: 确认发电机向母线供电
            verification: GEN_PANEL_CB_ON = ON
          - step: 12
            time: "T+13s"
            action: ATS切换至发电机侧
            verification: ATS1_POS = BACKUP
          - step: 13
            time: "T+14s"
            action: 应急母线恢复供电
            verification: BUS_E1电压正常
      
      phase_4_load_staging:
        name: 分级加载
        description: 防止发电机过载掉频
        steps:
          - step: 14
            time: "T+15s"
            action: 第一级负荷合闸
            loads: 
              - UPS输入（手术室、ICU）
              - 消防设备
              - 应急照明
            load_percentage: 30%
          - step: 15
            time: "T+20s"
            action: 第二级负荷合闸
            loads:
              - 电梯（至少1台）
              - 重要医疗设备
            load_percentage: 60%
          - step: 16
            time: "T+25s"
            action: 第三级负荷合闸
            loads:
              - 其他应急负荷
            load_percentage: 80-100%
          - step: 17
            time: "T+30s"
            action: 系统稳定运行
            verification: |
              发电机负载率<90%
              频率稳定在50Hz±0.5Hz
      
      total_time: "<30秒（从失电到全部应急负荷恢复）"
      critical_time: "<15秒（一级重要负荷恢复）"
      
      frequency_protection:
        description: 发电机过载保护
        underfrequency_threshold: 
          warning: 49Hz
          trip: 47Hz
        action_on_underfrequency:
          - 自动切除非关键负荷
          - 防止发电机失速
        load_shedding_priority:
          1: 非关键照明
          2: 普通电梯
          3: 空调系统（部分）
          note: UPS/消防/生命支持设备不可切除

    # === E1修复：发电机启动失败处理 ===
    generator_start_failure_handling:
      name: 发电机启动失败处理
      description: 发电机启动失败后的应急措施
      
      failure_detection:
        condition: 启动命令发出后10秒内未检测到运行
        detection: GEN_START_CMD = ON 且 GEN_RUN = OFF 持续10秒
        
      auto_retry:
        max_attempts: 3
        interval: 10s
        sequence:
          - attempt: 1
            time: "T+10s后"
            action: 第一次重试
          - attempt: 2
            time: "T+20s后"
            action: 第二次重试
          - attempt: 3
            time: "T+30s后"
            action: 第三次重试（最后一次）
      
      single_generator_failure:
        description: 双机配置时单机故障
        action:
          - step: 1
            action: 停止故障机组重试
          - step: 2
            action: 立即启动备用机组
          - step: 3
            action: 备用机组带全部应急负荷
          - step: 4
            action: 报警通知维护人员
        recovery_time: 额外增加5-8秒
      
      all_generators_failure:
        description: 所有发电机均启动失败（极端情况）
        trigger: 所有机组3次重试均失败
        immediate_actions:
          - action: 触发EMERGENCY级别报警
            target: 医院总指挥中心、设备科、院办
          - action: 启动医院应急预案
            plan: 《全院停电应急预案》
        contingency_measures:
          - measure: UPS电池继续供电
            duration: 15-30分钟
          - measure: 联系外部移动发电车
            response_time: 期望30分钟内到达
          - measure: 关键手术转移至有电区域
          - measure: 呼吸机等生命支持设备手动操作
        notification:
          - 值班院领导
          - 设备科负责人
          - 电力公司（请求优先恢复）
          - 卫生主管部门（重大事件上报）
      
      parallel_sync_failure:
        description: 双机并联同期失败
        condition: 同期条件不满足持续30秒
        action:
          - step: 1
            action: 放弃并联，1#机组单独带负荷
          - step: 2
            action: 2#机组停机待命
          - step: 3
            action: 报警通知维护人员检查同期装置
        fallback: 单机运行模式

    # === 发电机自动停机（原有内容优化）===
    generator_auto_stop:
      name: 发电机自动停机逻辑
      
      trigger:
        condition: 市电恢复正常
        detection: ATS主电源恢复正常持续30秒
        
      pre_transfer_check:
        description: 切换前检查
        checks:
          - item: 市电电压
            requirement: 380V ±10%
            duration: 稳定30秒
          - item: 市电频率
            requirement: 50Hz ±1Hz
            duration: 稳定30秒
          - item: 市电相序
            requirement: 正确
      
      transfer_sequence:
        description: 切回市电流程
        method: 先断后合（非同期切换）
        steps:
          - step: 1
            action: 确认市电稳定30秒
          - step: 2
            action: ATS分闸发电机侧
          - step: 3
            action: 短暂失电（<100ms）
            note: UPS保证关键负荷不中断
          - step: 4
            action: ATS合闸市电侧
          - step: 5
            action: 应急母线由市电供电
      
      cool_down_sequence:
        description: 发电机冷却停机
        steps:
          - step: 1
            action: 发电机出口断路器分闸
          - step: 2
            action: 发电机空载运行
            duration: 180s（3分钟）
            purpose: 冷却发动机，保护涡轮增压器
          - step: 3
            action: 发电机停机
          - step: 4
            action: 冷却风机继续运行
            duration: 60s
          - step: 5
            action: 系统恢复待机状态
            verification: GEN_READY = ON

    # === E4修复：变压器冷却系统控制 ===
    transformer_cooling_control:
      name: 变压器冷却系统控制
      description: 干式变压器风冷系统控制逻辑
      
      temperature_based_control:
        description: 基于温度的风机控制
        normal_operation:
          fan_start_temp: 100℃
          fan_stop_temp: 85℃
          hysteresis: 15℃
        forced_cooling:
          condition: 温度>120℃
          action: 强制风机高速运行
        
      load_based_control:
        description: 基于负载的风机控制
        low_load:
          condition: 负载率<50%
          action: 风机可停止
        medium_load:
          condition: 负载率50-80%
          action: 风机低速运行
        high_load:
          condition: 负载率>80%
          action: 风机高速运行
        overload:
          condition: 负载率>100%
          action: 风机全速+报警
      
      seasonal_strategy:
        summer:
          description: 夏季策略（环境温度>30℃）
          fan_start_temp: 90℃
          fan_stop_temp: 75℃
          preemptive: 负载率>60%时提前启动
        winter:
          description: 冬季策略（环境温度<10℃）
          fan_start_temp: 110℃
          fan_stop_temp: 90℃
          note: 可减少风机运行时间
        transition:
          description: 过渡季
          follow_normal: true
      
      protection:
        overtemperature_warning:
          threshold: 130℃
          action: 报警，强制风冷
        overtemperature_alarm:
          threshold: 145℃
          action: 高级报警，准备切换
        overtemperature_trip:
          threshold: 155℃
          action: 变压器保护跳闸
          note: 需减少该变压器负荷或切换至备用
      
      control_points:
        - point_id: TX_TEMP_MAX
          point_name: 变压器最高温度
          point_type: AI
          unit: ℃
          note: 取三相最高值
        - point_id: TX_FAN_MODE
          point_name: 风机控制模式
          point_type: AO
          values: [OFF, LOW, HIGH, AUTO]
        - point_id: TX_FAN_FAULT
          point_name: 风机故障
          point_type: DI

    # === 负荷分级管理 ===
    load_classification_management:
      name: 负荷分级管理
      description: 按重要程度对负荷进行分级管理
      
      classification:
        level_0_life_critical:
          name: 生命攸关负荷
          examples:
            - 手术室医疗设备
            - ICU/CCU监护设备
            - 呼吸机
            - 血液透析机
          power_source: 市电 + 发电机 + UPS
          max_interruption: 0ms
          shedding_allowed: false
          
        level_1_critical:
          name: 一级重要负荷
          examples:
            - 急诊抢救室设备
            - 新生儿科设备
            - 产房设备
            - 消防设备
            - 电梯（至少1台）
          power_source: 市电 + 发电机
          max_interruption: 15s
          shedding_allowed: false
          
        level_2_important:
          name: 二级重要负荷
          examples:
            - 普通病房照明
            - 医技科室设备
            - 药房冷藏设备
          power_source: 市电 + 发电机（可延迟）
          max_interruption: 30s
          shedding_allowed: 极端情况可
          
        level_3_general:
          name: 三级一般负荷
          examples:
            - 行政办公区
            - 后勤区域
            - 空调系统（非关键）
          power_source: 市电
          max_interruption: 无限制
          shedding_allowed: true

      emergency_load_shedding:
        description: 紧急切负荷策略
        trigger:
          - 发电机过载（负载率>100%）
          - 发电机频率下降（<48Hz）
          - 电池电量过低（UPS）
        shedding_sequence:
          - step: 1
            shed: 三级负荷
            action: 切除非关键照明、空调
          - step: 2
            shed: 部分二级负荷
            action: 保留关键二级负荷
          - step: 3
            shed: 不可再切
            action: 仅保留生命攸关和一级负荷
            note: 此时必须解决电源问题
```

---

## 系统 2.3: ELEC-EPS 应急电源系统（修订版 - UPS电池管理）

```yaml
  # ========================================
  # CONTROL LOGIC SECTION - 控制逻辑（E2修复补充）
  # ========================================
  control_logic:
  
    # === 原有控制逻辑保留 ===
    generator_parallel_operation:
      # ... 原有内容 ...
    
    ups_operation_mode:
      # ... 原有内容 ...
    
    # === E2修复：电池分级管理 ===
    battery_soc_management:
      name: UPS电池分级管理
      description: 根据电池剩余电量采取分级措施
      
      soc_levels:
        level_normal:
          range: "80-100%"
          status: 正常
          action: 无特殊动作
          display: 绿色
          
        level_warning:
          range: "50-80%"
          status: 预警
          action:
            - 提醒值班人员关注
            - 检查发电机是否启动
            - 准备非关键负荷切除
          display: 黄色
          
        level_alert:
          range: "20-50%"
          status: 告急
          action:
            - 报警通知相关人员
            - 切除非生命支持负荷
            - 优先保证ICU/手术室
            - 检查发电机启动状态
          display: 橙色
          shed_loads:
            - 非关键工作站
            - 普通照明（保留应急照明）
            - 非关键医疗设备
          
        level_critical:
          range: "10-20%"
          status: 危急
          action:
            - CRITICAL报警
            - 仅保留生命支持设备
            - 通知手术室准备转移患者
            - 通知ICU手动接管呼吸机
          display: 红色
          remaining_loads:
            - 生命支持设备（呼吸机等）
            - 手术室核心设备
            - 监护仪
            - 应急照明
          
        level_shutdown:
          range: "<10%"
          status: 即将关机
          action:
            - 有序关闭剩余非生命攸关设备
            - 保护性关机（防止设备损坏）
            - 发出最终警告
          display: 红色闪烁
          note: 剩余约1-2分钟供电时间
          
        level_exhausted:
          range: "<5%"
          status: 电池耗尽
          action:
            - UPS自动关机
            - 保护电池防止过放
          note: 此时生命支持设备应已切换至其他电源或手动模式
      
      generator_coordination:
        description: 发电机与UPS协调
        scenario_1:
          condition: 市电失电，发电机正常启动
          action:
            - 发电机启动后立即给UPS供电
            - UPS转为市电模式（由发电机供电）
            - 开始给电池充电
            - 电池恢复至80%以上后恢复全部负荷
          timeline:
            - "T+0": 市电失电，UPS电池放电
            - "T+15s": 发电机启动，UPS切换至发电机供电
            - "T+15s起": 电池开始充电
            - "约30min后": 电池恢复至80%
            
        scenario_2:
          condition: 市电失电，发电机启动失败
          action:
            - UPS持续电池放电
            - 启动SOC分级管理
            - 等待发电机重试或外部电源
          critical_time: 15-30分钟（视电池容量）
      
      low_temperature_derating:
        description: 低温环境电池容量折减
        derating_table:
          - temp: "25℃"
            capacity: "100%"
          - temp: "20℃"
            capacity: "95%"
          - temp: "10℃"
            capacity: "85%"
          - temp: "0℃"
            capacity: "70%"
          - temp: "-10℃"
            capacity: "55%"
        monitoring:
          sensor: UPS1_BATTERY_TEMP
          alarm_low: 10℃
          alarm_high: 40℃
        mitigation:
          - UPS机房保持空调运行
          - 电池室温度监控
          - 冬季加强保温
      
      battery_health_monitoring:
        description: 电池健康监测
        parameters:
          - name: 内阻
            normal: "<2mΩ/cell"
            warning: ">3mΩ/cell"
            action: 准备更换
          - name: 容量
            normal: ">80%标称"
            warning: "<80%标称"
            action: 更换电池
          - name: 浮充电压
            normal: "2.25-2.30V/cell"
            abnormal: 偏离>0.1V
            action: 检查充电器
        test_schedule:
          monthly: 放电测试（30%DOD）
          quarterly: 容量测试
          annually: 内阻测试
          
      charging_management:
        description: 充电管理
        float_charge:
          voltage: "2.27V/cell"
          purpose: 长期浮充保持满电
        equalize_charge:
          voltage: "2.35V/cell"
          duration: 8-12小时
          frequency: 每3个月或深放电后
          purpose: 均衡各单体电压
        fast_charge:
          trigger: 电池放电后
          current_limit: "0.1C"
          end_condition: 电压达到2.35V/cell
        temperature_compensation:
          coefficient: "-3mV/℃/cell"
          reference: 25℃
```

---

# 医疗气体系统（修订版）

## 系统 2.4: MGAS-O2 医用氧气系统（完整修订版）

```yaml
System_Topology:

  identity:
    system_id: MGAS-O2
    system_name: 医用氧气系统
    system_name_en: Medical Oxygen System
    # ... 原有identity内容保留 ...
    
    version: 2.0
    revision_notes: |
      v2.0: 补充备用源耗尽保护、纯度监测、终端反污染防护、手术室协调
      v1.0: 初始版本

  # ... 原有boundary内容保留 ...

  nodes:
  
    # ... 原有source_nodes内容保留 ...
    
    distribution_nodes:
    
      # ... 原有汽化器、一级减压等节点保留 ...
      
      # === G3修复：新增氧气纯度监测节点 ===
      - node_id: MGAS-O2_DST_PURITY_MONITOR
        node_name: 氧气纯度监测装置
        node_name_en: Oxygen Purity Monitor
        node_type: Distribution_Node
        node_subtype: MON
        node_category: DST
        
        function: 监测供气氧气纯度，确保符合药典标准
        medium_in: O2-GAS
        medium_out: SIGNAL
        
        equipment_parameters:
          type: 顺磁式氧分析仪
          measurement_range: {value: "0-100", unit: "%O2"}
          accuracy: ±0.5%
          response_time: {value: "<5", unit: s}
          sampling_point: 一级减压后主管
          display: 数字显示+远传
          calibration: 每季度校准
        
        control_points:
          sensors:
            - point_id: O2_PURITY
              point_name: 氧气纯度
              point_type: AI
              unit: "%"
              range: [0, 100]
              normal_range: [99.5, 100]
            - point_id: O2_PURITY_TREND
              point_name: 纯度趋势
              point_type: AI
              unit: "%/h"
              note: 检测纯度下降速率
          status:
            - point_id: O2_PURITY_LOW_WARN
              point_name: 纯度低预警
              point_type: DI
              threshold: "<99.0%持续5分钟"
            - point_id: O2_PURITY_LOW_ALARM
              point_name: 纯度低报警
              point_type: DI
              threshold: "<98.0%持续1分钟"
            - point_id: O2_PURITY_CRITICAL
              point_name: 纯度危急
              point_type: DI
              threshold: "<95.0%"
        
        alarm_settings:
          warning:
            threshold: {value: 99.0, unit: "%"}
            duration: 5分钟
            action: 报警提示，准备切换气源
          alarm:
            threshold: {value: 98.0, unit: "%"}
            duration: 1分钟
            action: 报警，自动切换至汇流排
          critical:
            threshold: {value: 95.0, unit: "%"}
            duration: 立即
            action: 紧急报警，停止液氧供气，切换备用
        
        action_on_low_purity:
          sequence:
            - step: 1
              action: 触发纯度低报警
              notification: 气体站值班室、护士站
            - step: 2
              action: 自动切换至汇流排供气
              condition: 汇流排压力正常
            - step: 3
              action: 隔离故障液氧系统
              method: 关闭液氧至主管阀门
            - step: 4
              action: 通知检修排查原因
              possible_causes:
                - 液氧储罐进水/污染
                - 汽化器故障
                - 管道泄漏混入空气
                - 减压阀故障
            - step: 5
              action: 确认纯度恢复后方可切回液氧
              requirement: 纯度≥99.5%持续10分钟
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 氧气站房/气体机房
          position: 一级减压后主管旁
          note: 需便于日常检查和校准

      # === 原有报警装置节点保留，增强报警逻辑 ===
      - node_id: MGAS-O2_DST_ALARM_PANEL
        # ... 原有内容保留，补充以下 ...
        
        enhanced_features:
          purity_integration:
            description: 集成纯度报警
            display: 显示当前氧气纯度
            alarm: 与纯度监测联动
          
          predictive_warning:
            description: 预测性预警
            logic: |
              1. 监测液氧消耗速率
              2. 预测剩余可用时间
              3. 提前发出补充提醒
            warning_threshold: 预计剩余<24小时

    sink_nodes:
    
      # === G2修复：终端防污染设计 ===
      - node_id: MGAS-O2_SNK_TERMINAL
        node_name: 氧气终端
        node_name_en: Oxygen Outlet Terminal
        node_type: Sink_Node
        node_category: SNK
        
        function: 床旁/手术室氧气使用点
        medium_in: O2-GAS
        medium_out: O2-GAS (to patient)
        
        is_boundary_output: true
        
        multiplicity: multiple
        instance_pattern: MGAS-O2_SNK_TERMINAL_{Floor}_{Room}_{Seq}
        typical_quantity: 大量（按床位数）
        
        equipment_parameters:
          type: 快速插拔式终端
          standard: 德标DIN/国标GB
          gas_specific: 氧气专用（不可互换）
          color_coding: 绿色
          flow_rate: {value: "0-15", unit: "L/min"}
          outlet_pressure: {value: 0.4, unit: MPa, tolerance: ±0.05}
          
          # === G2修复：防污染设计 ===
          anti_contamination_features:
            check_valve:
              type: 内置单向阀
              function: 防止气体回流
              cracking_pressure: {value: 0.01, unit: MPa}
              note: 即使接错也不会反向污染管道
            
            self_sealing:
              type: 自封闭机构
              function: 拔出时自动关闭，防止外界污染进入
              
            quick_disconnect:
              type: 快速插拔接头
              function: 气体专用接头，不同气体不可互换
              standard: ISO 5359
              
            dust_cap:
              type: 防尘盖
              function: 不使用时保护终端
              material: 抗菌塑料
          
          contamination_prevention_design:
            standard: ISO 7396-1 Part 2
            features:
              - 终端插座设计防止非医疗器具插入
              - 气体专用颜色和形状编码
              - 使用后自动吹扫功能（可选）
          
          mounting:
            - 设备带
            - 吊塔
            - 墙面
        
        user_guidelines:
          pre_use:
            - 检查终端外观清洁
            - 移除防尘盖
            - 短暂开启吹扫（1-2秒）
          during_use:
            - 定期检查连接牢固
            - 观察流量计显示
          post_use:
            - 拔出连接器
            - 盖好防尘盖
            - 终端表面消毒
          prohibited:
            - 禁止使用损坏的终端
            - 禁止自行改装接头
            - 禁止将终端用于非医疗用途
        
        maintenance:
          daily: 外观检查，清洁消毒
          weekly: 功能测试（压力、流量）
          monthly: 单向阀功能检查
          yearly: 更换密封件
        
        location_hint:
          space_type: 病房/手术室/ICU
          position: 床头设备带/吊塔
          height: 距地1.4m（设备带）

  # ========================================
  # CONTROL LOGIC SECTION - 控制逻辑（G1/G4修复）
  # ========================================
  control_logic:
  
    # === 原有控制逻辑保留 ===
    source_auto_switching:
      # ... 原有内容保留 ...
    
    manifold_switching:
      # ... 原有内容保留 ...
    
    three_level_alarm:
      # ... 原有内容保留 ...
    
    # === G1修复：备用源耗尽保护 ===
    backup_source_depletion_protection:
      name: 备用气源耗尽应急保护
      description: 液氧和汇流排均即将耗尽时的应急措施
      
      monitoring:
        lox_level:
          warning: 20%
          alarm: 15%
          critical: 10%
        manifold_pressure:
          warning: 2MPa（单侧）
          alarm: 1MPa（单侧）
          critical: 0.5MPa（双侧均低）
      
      stage_1_early_warning:
        trigger: 液氧液位<20% 或 汇流排单侧<2MPa
        actions:
          - action: 发出预警
            target: 气体站值班室
          - action: 联系液氧供应商确认配送时间
          - action: 清点备用气瓶数量
          - action: 准备应急氧气瓶
      
      stage_2_alert:
        trigger: 液氧液位<15% 或 切换至汇流排供气
        actions:
          - action: 发出警报
            target: 气体站、护士站、设备科
          - action: 确认液氧配送车辆出发
          - action: 核实各科室氧气使用情况
          - action: 非急需患者减少用氧
          - action: 床旁应急氧气瓶检查就绪
      
      stage_3_critical:
        trigger: |
          液氧耗尽 且 汇流排双侧均<1MPa
          或 系统压力跌至<0.3MPa
        actions:
          - step: 1
            action: 触发CRITICAL报警
            target: 医院总指挥中心、院办、医务科
          - step: 2
            action: 启动《氧气供应中断应急预案》
          - step: 3
            action: 通知各科室启用床旁应急氧气瓶
          - step: 4
            action: 优先保障ICU、手术室、急诊
          - step: 5
            action: 暂停非急需患者用氧
          - step: 6
            action: 联系周边医院借调氧气
          - step: 7
            action: 液氧公司紧急配送（1小时内）
        
        triage_priority:
          priority_1_life_critical:
            areas: ICU、手术室、急诊抢救室
            action: 床旁氧气瓶全力保障
          priority_2_critical:
            areas: 新生儿科、产房、CCU
            action: 床旁氧气瓶
          priority_3_important:
            areas: 普通病房（呼吸科等）
            action: 按需使用，降低流量
          priority_4_general:
            areas: 门诊、康复科
            action: 暂停供氧
      
      stage_4_recovery:
        trigger: 新液氧/气瓶补充到位
        actions:
          - step: 1
            action: 确认新气源正常
          - step: 2
            action: 切换至新气源
          - step: 3
            action: 系统压力恢复正常
          - step: 4
            action: 逐步恢复各科室供氧
          - step: 5
            action: 解除应急状态
          - step: 6
            action: 填写应急事件报告
      
      time_budget:
        description: 时间预算
        calculation: |
          汇流排10瓶×40L×15MPa = 6000L液态 = 约6000Nm³气态
          峰值消耗2000L/min = 120Nm³/h
          理论可用时间 = 6000/120 = 50小时（满配）
          实际预留安全余量 = 10小时（仅1侧）
        requirement: 
          - 液氧补充必须在汇流排耗尽前到达
          - 预留至少4小时应急时间
      
      pressure_continuity:
        description: 切换过程压力连续性
        problem: 切换时主管压力可能波动
        solution:
          - 设置蓄压罐（缓冲罐）
          - 切换阀门平稳过渡
          - 一级减压阀组一用一备
        requirement: 切换过程中主管压力≥0.35MPa
        verification: 定期切换演练测试

    # === G4修复：手术室医用气体协调 ===
    operating_room_gas_coordination:
      name: 手术室医用气体协调控制
      description: 氧气与负压吸引的协调监控
      
      pre_procedure_check:
        description: 术前检查清单
        checklist:
          - item: 氧气压力
            requirement: "≥0.4MPa"
            source: O2_ZONE_PRESSURE
          - item: 负压真空度
            requirement: "≤-0.03MPa"
            source: VAC_ZONE_PRESSURE
          - item: 压缩空气压力
            requirement: "≥0.4MPa"
            source: AIR_ZONE_P
          - item: 笑气压力（如使用）
            requirement: "≥0.4MPa"
            source: N2O_ZONE_P
        verification:
          method: 手术室控制面板一键检测
          display: 绿灯=正常，红灯=异常
          record: 自动记录检测结果
        blocking_condition:
          description: 阻止手术开始条件
          condition: 任一气体不合格
          action: 
            - 禁止开始新手术
            - 报警通知维护人员
            - 正在进行手术继续，做好应急准备
      
      during_procedure_monitoring:
        description: 术中持续监测
        monitoring:
          O2_pressure:
            normal: ">0.35MPa"
            warning: "0.30-0.35MPa"
            alarm: "<0.30MPa"
          VAC_vacuum:
            normal: "<-0.03MPa"
            warning: "-0.02~-0.03MPa"
            alarm: ">-0.02MPa"
        display: 手术室内压力显示屏
        refresh_rate: 实时更新
        
      failure_scenarios:
        O2_failure:
          trigger: 手术室氧气压力<0.25MPa
          immediate_actions:
            - step: 1
              action: 声光报警（手术室内）
            - step: 2
              action: 通知麻醉医生
            - step: 3
              action: 启用麻醉机内置氧气备份
              note: 麻醉机通常配备小型氧气瓶
            - step: 4
              action: 准备床旁应急氧气瓶
            - step: 5
              action: 通知气体站排查故障
          surgical_response:
            - 暂停非紧急操作
            - 优先完成关键步骤
            - 必要时提前结束手术
            
        VAC_failure:
          trigger: 手术室负压真空度>-0.02MPa
          immediate_actions:
            - step: 1
              action: 声光报警
            - step: 2
              action: 通知手术医生
            - step: 3
              action: 启用手动吸引器
              equipment: 脚踏式吸引器/手动负压球
            - step: 4
              action: 通知气体站排查
          surgical_response:
            - 手动清理术野
            - 如无法控制出血，考虑暂停
            
        both_failure:
          trigger: 氧气和负压同时故障
          severity: CRITICAL
          actions:
            - step: 1
              action: 最高级别报警
            - step: 2
              action: 启动所有应急设备
            - step: 3
              action: 评估是否继续手术
            - step: 4
              action: 院领导决策
          decision_factors:
            - 手术进行阶段
            - 患者状态
            - 应急设备可用性
            - 故障恢复预期时间
      
      cross_system_coordination:
        description: 跨系统协调信号
        signals:
          MGAS_O2_to_MGAS_VAC:
            - O2供应正常状态
            - O2故障报警
          MGAS_VAC_to_MGAS_O2:
            - VAC供应正常状态
            - VAC故障报警
          integration_point: 楼宇自控系统（INT-BA）
          display: 手术室护士站总览屏

    # === 纯度监测联动控制 ===
    purity_monitoring_control:
      name: 氧气纯度监测联动
      description: 纯度异常时的自动响应
      
      monitoring:
        sensor: MGAS-O2_DST_PURITY_MONITOR
        normal_range: "99.5%-100%"
        sampling_interval: 连续监测
        
      control_logic:
        warning_level:
          condition: 纯度<99.0%持续5分钟
          action:
            - 发出预警
            - 记录事件
            - 准备切换
        alarm_level:
          condition: 纯度<98.0%持续1分钟
          action:
            - 发出报警
            - 自动切换至汇流排
            - 关闭液氧系统阀门
            - 通知维护人员
        critical_level:
          condition: 纯度<95.0%
          action:
            - 立即切换气源
            - CRITICAL报警
            - 停止液氧系统
            - 调查原因
      
      recovery:
        condition: 故障排除，纯度恢复
        procedure:
          - step: 1
            action: 确认纯度≥99.5%稳定10分钟
          - step: 2
            action: 手动确认可切回液氧
          - step: 3
            action: 逐步切换回液氧系统
          - step: 4
            action: 监测24小时确认稳定

  # ========================================
  # ALARM & PROTECTION - 报警与保护（增强）
  # ========================================
  alarm_protection:
    
    critical_alarms:
      # ... 原有报警保留 ...
      
      # === 新增纯度报警 ===
      - alarm_id: ALM_O2_PURITY_LOW
        alarm_name: 氧气纯度低报警
        severity: HIGH
        trigger: O2_PURITY < 98%
        action: 自动切换汇流排，通知维护
        
      - alarm_id: ALM_O2_PURITY_CRITICAL
        alarm_name: 氧气纯度危急
        severity: CRITICAL
        trigger: O2_PURITY < 95%
        action: 立即停止液氧供气，紧急报警
        
      # === 新增气源耗尽报警 ===
      - alarm_id: ALM_O2_SOURCE_DEPLETING
        alarm_name: 气源即将耗尽
        severity: CRITICAL
        trigger: 液氧<10% 且 汇流排双侧<1MPa
        action: 启动应急预案，全院通知
```

---

## 系统 2.5: MGAS-VAC 医用负压吸引系统（修订版 - 关键补充）

```yaml
  # ========================================
  # CONTROL LOGIC - 控制逻辑（修订补充）
  # ========================================
  control_logic:
  
    # === 原有pump_control保留 ===
    pump_control:
      # ... 原有内容 ...
    
    # === G4修复：与氧气系统协调 ===
    oxygen_system_coordination:
      name: 与氧气系统协调
      description: 负压系统状态同步至氧气系统监控
      
      status_sharing:
        signals_to_o2_system:
          - VAC_SYSTEM_OK: 负压系统正常
          - VAC_LOW_VACUUM: 真空度不足
          - VAC_PUMP_FAULT: 泵组故障
        integration: 通过INT-BA系统集成
        
      joint_monitoring:
        location: 手术室护士站
        display: 统一显示O2/VAC/AIR状态
        alarm: 任一系统故障时联合报警
    
    # === 备用策略增强 ===
    backup_strategy:
      name: 负压系统备用策略
      
      pump_redundancy:
        configuration: "2+1（两用一备）"
        auto_failover:
          trigger: 运行泵故障
          action: 自动启动备用泵
          time: "<5秒"
          
      manual_backup:
        equipment: 脚踏式吸引器
        location: 每间手术室
        purpose: 真空泵全部故障时手动吸引
        maintenance: 每月检查功能完好
        
      mobile_vacuum:
        equipment: 移动式电动吸引器
        quantity: 4台
        location: 设备科库房
        purpose: 应急调配
        
      cross_connection:
        description: 与其他真空系统的应急连接
        note: |
          大型医院可能有多个真空泵站
          紧急时可通过阀门切换连通
```

---

## 系统间协调逻辑（新增章节）

```yaml
# ========================================
# 跨系统协调逻辑
# ========================================
Cross_System_Coordination:

  identity:
    name: 医院关键系统协调逻辑
    description: 定义电气与医疗气体系统间的关键交互
    version: 1.0

  # === 电力系统与医疗气体系统协调 ===
  power_gas_coordination:
    
    normal_operation:
      description: 正常运行时的监控
      monitoring:
        - 电力系统状态 → 医用气体控制室
        - 医用气体压力 → 楼宇自控中心
      display: 统一能源管理平台
      
    power_failure_impact:
      description: 电力故障对医疗气体的影响
      
      affected_equipment:
        MGAS_O2:
          affected: 
            - 液氧汽化器电伴热（冬季）
            - 报警系统
            - 监控设备
          not_affected:
            - 液氧储罐（被动）
            - 汇流排（被动）
            - 管道供气（靠压力）
          action: 确保报警系统有UPS后备
          
        MGAS_VAC:
          affected:
            - 真空泵（核心设备）
            - 报警系统
          impact: 真空泵停止，真空度逐渐下降
          buffer_time: 约5-10分钟（取决于储气罐容积和使用量）
          action: 
            - 真空泵接应急电源
            - 准备手动吸引器
            
        MGAS_AIR:
          affected:
            - 空气压缩机（核心设备）
            - 干燥机
            - 过滤器
          impact: 压缩空气逐渐下降
          buffer_time: 约10-15分钟（取决于储气罐容积）
          action:
            - 压缩机接应急电源
            - 非关键压缩空气可暂停
            
    generator_startup_sequence:
      description: 发电机启动后医疗气体设备恢复顺序
      sequence:
        - priority: 1
          equipment: UPS（含医疗设备）
          time: 立即
        - priority: 2
          equipment: 真空泵
          time: T+15s
          reason: 手术室吸引关键
        - priority: 3
          equipment: 空气压缩机
          time: T+20s
        - priority: 4
          equipment: 氧气监控报警
          time: T+25s
          note: 氧气供应本身不受影响
          
    mutual_monitoring:
      description: 互相监控信号
      signals:
        ELEC_to_MGAS:
          - POWER_NORMAL: 市电正常
          - POWER_FAIL: 市电失电
          - GEN_RUNNING: 发电机运行
          - GEN_FAIL: 发电机故障
        MGAS_to_ELEC:
          - O2_CRITICAL: 氧气系统危急
          - VAC_CRITICAL: 负压系统危急
          - AIR_CRITICAL: 压缩空气危急
      action_on_signal:
        POWER_FAIL_received:
          - 医用气体系统记录事件
          - 准备应急响应
          - 延长报警静音防止误报
        O2_CRITICAL_sent:
          - 优先保障医用气体设备供电
          - 必要时切除非关键负荷

  # === 手术室综合协调 ===
  operating_room_coordination:
    
    pre_surgery_checklist:
      description: 手术前综合检查
      items:
        electricity:
          - 市电正常 / 发电机就绪
          - UPS电池充足（>80%）
          - 手术室配电正常
        medical_gas:
          - 氧气压力≥0.4MPa
          - 氧气纯度≥99.5%
          - 负压真空度≤-0.03MPa
          - 压缩空气≥0.4MPa
          - 笑气（如需要）≥0.4MPa
        backup:
          - 床旁氧气瓶就位
          - 手动吸引器就位
          - 应急照明正常
      result:
        all_pass: 允许手术
        any_fail: 禁止开始新手术
        
    during_surgery_monitoring:
      description: 术中持续监控
      display: 手术室控制面板
      parameters:
        - 电力状态（市电/发电机/UPS）
        - 氧气压力和纯度
        - 负压真空度
        - 压缩空气压力
      alarm: 声光报警（可静音但不可关闭）
      
    emergency_response:
      description: 紧急情况响应矩阵
      scenarios:
        power_fail_gen_ok:
          impact: 短暂中断（<15秒）
          action: 继续手术
        power_fail_gen_fail:
          impact: 依赖UPS（15-30分钟）
          action: 
            - 评估手术阶段
            - 尽快完成关键步骤
            - 必要时提前结束
        o2_fail:
          impact: 患者供氧中断风险
          action:
            - 床旁氧气瓶接手
            - 麻醉师接管呼吸
            - 评估继续/终止
        vac_fail:
          impact: 术野积血无法清理
          action:
            - 手动吸引器
            - 加快止血
            - 必要时暂停
        multiple_fail:
          impact: 极端情况
          action:
            - 院领导决策
            - 优先保护患者生命
            - 启动最高级应急预案

  # === 报警整合 ===
  alarm_integration:
    
    unified_alarm_center:
      location: 医院总控室/安防中心
      systems_integrated:
        - ELEC-HV
        - ELEC-LV-MAIN
        - ELEC-EPS
        - MGAS-O2
        - MGAS-VAC
        - MGAS-AIR
        - MGAS-N2O
        - HVAC-CHP
        - INT-BA
      display: 统一监控大屏
      
    alarm_priority:
      level_1_emergency:
        examples:
          - 双路市电全失且发电机故障
          - 氧气系统完全中断
          - 多系统同时故障
        response: 
          - 自动通知院领导
          - 启动医院应急预案
          - 全院广播
          
      level_2_critical:
        examples:
          - 单路市电故障
          - 氧气纯度低
          - 发电机单机故障
        response:
          - 通知设备科/值班人员
          - 准备应急措施
          
      level_3_high:
        examples:
          - 液氧低液位
          - 变压器超温
          - 过滤器堵塞
        response:
          - 通知维护人员
          - 安排检修
          
      level_4_warning:
        examples:
          - 设备运行时间超标
          - 电池需要测试
          - 定期维护提醒
        response:
          - 记录事件
          - 安排维护计划
```

---

# 第二批次修订完成

## 修订总结

| 缺陷ID | 描述 | 修复状态 | 修复位置 |
|--------|------|----------|----------|
| E1 | 发电机黑启动失败处理 | ✅ 已修复 | ELEC-LV-MAIN: generator_start_failure_handling |
| E2 | UPS电池SOC分级管理 | ✅ 已修复 | ELEC-EPS: battery_soc_management |
| E3 | 低压系统黑启动时序 | ✅ 已修复 | ELEC-LV-MAIN: black_start_sequence |
| E4 | 变压器冷却系统控制 | ✅ 已修复 | ELEC-LV-MAIN: transformer_cooling_control |
| G1 | 备用源耗尽保护 | ✅ 已修复 | MGAS-O2: backup_source_depletion_protection |
| G2 | 终端反向污染防护 | ✅ 已修复 | MGAS-O2_SNK_TERMINAL: anti_contamination_features |
| G3 | 氧气纯度监测 | ✅ 已修复 | MGAS-O2_DST_PURITY_MONITOR + purity_monitoring_control |
| G4 | 手术室O2/VAC协调 | ✅ 已修复 | MGAS-O2: operating_room_gas_coordination |

## 新增内容

1. **跨系统协调逻辑章节** (Cross_System_Coordination)
 - 电力与医疗气体系统协调
 - 手术室综合协调
 - 报警整合

2. **负荷分级管理** (load_classification_management)
 - 四级负荷分类
 - 紧急切负荷策略

3. **电池健康监测** (battery_health_monitoring)
 - 内阻、容量、电压监测
 - 测试计划

---

**下一批次预告：** Batch 3 将输出给排水系统（PLUMB-DWS、PLUMB-HWS、PLUMB-SAN）和智能化系统核心（INT-BA、INT-NUR、INT-SEC）。

请确认第二批次修订版内容后，我将继续输出第三批次。

---