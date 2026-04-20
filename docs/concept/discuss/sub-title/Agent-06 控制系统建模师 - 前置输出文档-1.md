## 🧑‍💻 User


那么，你是不是应该先输出白皮书？

---
## 🤖 Assistant


好的，我现在已经充分检索了知识库中的相关内容。根据任务书要求，我现在**首先输出"控制架构与降级策略白皮书"**。

---

# 控制架构与降级策略白皮书
## Agent-06 控制系统建模师 - 前置输出文档

**版本**: v2.0
**日期**: 2025-01-XX
**状态**: 正式发布

---

## 摘要

本白皮书阐述医院建筑自动化控制系统在极端情况下的可用性保障策略。基于"分层自治、逐级降级、本质安全"的核心设计哲学，建立覆盖云端(L1)、边缘(L2)、硬件(L3)三级保障的韧性控制架构，确保在网络中断、传感器失效、控制器宕机等故障工况下，关键医疗区域（特别是手术室、ICU）仍能维持最低安全运行边界。

---

## 第一章 设计哲学与原则

### 1.1 核心格言

> **"业务定义意图，物理定义限制，控制实现目标。"**

控制系统作为连接"业务需求"与"物理系统"的桥梁，其职责不是定义目标（Agent-05的职责），也不是定义物理特性（Agent-04的职责），而是设计一套**感知-决策-执行**的神经系统，确保物理系统在各种工况下逼近业务目标。

### 1.2 三大设计原则

```yaml
Design_Principles:
  
  Principle_1:
    name: "关键回路本地化 (Critical Loop Localization)"
    description: |
      所有P0/P1级别的控制回路必须能够在完全断网条件下独立运行。
      边缘控制器(DDC/PLC)必须具备完整的本地控制逻辑，不依赖上位机。
    rationale: |
      网络是最脆弱的环节。云端优化算法可以提升效率，但不能成为基础运行的依赖。
      当网络中断时，手术室的温度控制、压差控制必须继续正常工作。
    implementation:
      - "PID控制参数固化在本地DDC"
      - "安全联锁逻辑硬编码于PLC"
      - "默认安全设定值预置于控制器ROM"
      - "本地HMI可独立操作关键设备"
    validation_criteria:
      - "断开上位机连接48小时，关键区域环境参数偏差<5%"
      - "DDC重启后30秒内恢复自动控制"
  
  Principle_2:
    name: "故障安全设计 (Fail-Safe Design)"
    description: |
      每个执行器必须定义明确的失效安全位置(Fail-Safe Position)。
      传感器故障时必须有备用策略(物理备用或软测量)。
    rationale: |
      设备终会故障，问题是故障后系统处于什么状态。
      医院环境下，"安全状态"的定义因区域而异：
      - 手术室：保持正压、保持送风（防止污染）
      - 负压隔离病房：保持负压（防止泄漏）
      - 冷站：保持冷却（防止设备过热）
    implementation:
      - "所有阀门定义断电/断信号位置"
      - "关键参数配置双传感器冗余"
      - "软测量算法作为物理传感器备用"
      - "执行器配置手动超驰机构"
    validation_criteria:
      - "任意单点故障不导致关键功能丧失"
      - "故障状态在10秒内被检测并报警"
  
  Principle_3:
    name: "渐进式降级 (Graceful Degradation)"
    description: |
      系统故障时不是"全开或全关"的二元选择，而是逐级降级：
      正常模式 → 节能模式 → 基础模式 → 安全模式 → 应急模式
    rationale: |
      完全停机往往比部分功能降级更危险。
      例如：冷站全停会导致全院温度失控，但降低冷冻水温差可以减少冷量50%同时维持基本供冷。
    implementation:
      - "每种运行模式的控制策略预定义"
      - "模式切换条件和优先级明确"
      - "最低安全边界由硬件保障"
      - "降级过程可逆，自动恢复"
    validation_criteria:
      - "从正常模式到安全模式的切换时间<60秒"
      - "降级模式下关键功能保持率>80%"
```

### 1.3 医疗优先级矩阵

基于Agent-05定义的Criticality等级，建立控制资源分配优先级：

```yaml
Medical_Priority_Matrix:
  
  Priority_P0_LIFE_SAFETY:
    description: "生命安全级 - 失效直接威胁生命"
    areas:
      - "手术室 (MED-OR)"
      - "ICU (MED-ICU)"
      - "负压隔离病房"
      - "新生儿科"
    control_requirements:
      redundancy: "N+1"
      backup_power: "UPS + 发电机"
      network_independence: "必须"
      local_override: "必须"
      failover_time: "<10秒"
    resource_allocation:
      - "优先供冷/供热"
      - "独立控制回路"
      - "双传感器配置"
  
  Priority_P1_MISSION_CRITICAL:
    description: "任务关键级 - 失效影响医疗功能"
    areas:
      - "急诊科"
      - "检验科"
      - "药房"
      - "血库"
    control_requirements:
      redundancy: "N+1 recommended"
      backup_power: "发电机"
      network_independence: "推荐"
      failover_time: "<30秒"
  
  Priority_P2_IMPORTANT:
    description: "重要级 - 失效影响运营效率"
    areas:
      - "普通病房"
      - "门诊区域"
      - "医技科室"
    control_requirements:
      redundancy: "按需"
      backup_power: "部分"
      failover_time: "<5分钟"
  
  Priority_P3_NORMAL:
    description: "普通级 - 失效影响舒适性"
    areas:
      - "行政办公"
      - "后勤区域"
      - "公共大厅"
    control_requirements:
      redundancy: "无"
      backup_power: "无"
      note: "可接受临时停机"
```

---

## 第二章 三级控制保障架构

### 2.1 架构总览

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              L1: 云端/中控室层                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  能效优化   │  │  预测分析   │  │  报表统计   │  │  远程监控   │        │
│  │  Algorithm  │  │  Analytics  │  │  Reporting  │  │  SCADA      │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
│         │                │                │                │               │
│         └────────────────┴────────────────┴────────────────┘               │
│                                    │                                        │
│                            ┌───────▼───────┐                                │
│                            │   BACnet/IP   │  ← 网络中断时L1失效            │
│                            │   MQTT/HTTP   │    但L2/L3继续运行             │
│                            └───────┬───────┘                                │
└────────────────────────────────────┼────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              L2: 边缘控制器层                                │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         DDC/PLC 控制器集群                           │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │   │
│  │  │ DDC-OR  │  │ DDC-ICU │  │ DDC-CHP │  │ DDC-AHU │  │ PLC-FAS │   │   │
│  │  │ 手术室  │  │ 重症室  │  │ 冷热源  │  │ 空调机组 │  │ 消防    │   │   │
│  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘   │   │
│  │       │            │            │            │            │         │   │
│  │  本地逻辑:     本地逻辑:    本地逻辑:    本地逻辑:    本地逻辑:      │   │
│  │  - PID控制    - PID控制   - 群控逻辑  - 顺序控制  - 联动逻辑       │   │
│  │  - 压差控制   - 压差控制  - 加减机    - 新风控制  - 硬接点         │   │
│  │  - 联锁保护   - 联锁保护  - 防冻保护  - 防冻保护  - 优先级         │   │
│  │  - 默认设定值 - 默认设定值- 默认设定值- 默认设定值               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  关键特性:                                                                  │
│  ✓ 断网后独立运行     ✓ 本地HMI操作     ✓ 控制器间P2P通信               │
│  ✓ 电池保持(72h)     ✓ 看门狗保护      ✓ 自动重启恢复                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              L3: 硬件保护层                                  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         机械/电气安全装置                            │   │
│  │                                                                     │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │   │
│  │  │  机械恒温器  │  │   防冻开关   │  │  防火阀熔断  │              │   │
│  │  │  (手术室)    │  │  (表冷器)    │  │  (70°C/280°C)│              │   │
│  │  │  18-26°C    │  │  <5°C断开    │  │  自动关闭    │              │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │   │
│  │                                                                     │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │   │
│  │  │ 压差安全阀   │  │  安全泄压阀  │  │  紧急停止按钮│              │   │
│  │  │ (洁净室)     │  │  (锅炉/压缩机)│  │  (硬线直连) │              │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │   │
│  │                                                                     │   │
│  │  特性: 无需供电 | 无需通信 | 物理原理动作 | 不可被软件覆盖          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 各层级职责定义

```yaml
Control_Hierarchy:
  
  L1_Cloud_Central:
    name: "云端/中控室层"
    location: "数据中心/中央控制室"
    communication: "BACnet/IP, MQTT, HTTP/REST"
    functions:
      optimization:
        - name: "冷站能效优化"
          description: "基于负荷预测的冷机群控优化"
          algorithm: "Model Predictive Control (MPC)"
          benefit: "节能15-25%"
        - name: "需求响应"
          description: "响应电网峰谷信号调整负荷"
          algorithm: "Load Shifting"
        - name: "预测性维护"
          description: "基于设备运行数据预测故障"
          algorithm: "Machine Learning"
      analytics:
        - "能耗分析与对标"
        - "运行趋势分析"
        - "异常检测与诊断"
        - "报警统计与分析"
      supervision:
        - "全院系统状态监视"
        - "报警管理与通知"
        - "操作日志记录"
        - "报表生成"
    failure_impact: |
      L1失效时：
      - 优化算法停止，系统按L2本地逻辑运行
      - 远程监控中断，但本地HMI可用
      - 能效下降约10-15%，但基本功能不受影响
    recovery: "网络恢复后自动重连，历史数据补传"
  
  L2_Edge_Controller:
    name: "边缘控制器层"
    location: "各区域控制柜/机房"
    equipment: "DDC, PLC, 变频器"
    communication: "BACnet MS/TP, Modbus RTU, 硬接点"
    functions:
      closed_loop_control:
        - name: "PID控制"
          applications:
            - "温度控制 (送风/回风/室温)"
            - "湿度控制"
            - "压差控制"
            - "流量控制"
          parameters: "Kp, Ti, Td 固化于本地"
        - name: "串级控制"
          applications:
            - "室温-送风温度串级"
            - "室压-风量串级"
          benefit: "提高响应速度和稳定性"
      sequence_control:
        - name: "启停顺序"
          description: "设备安全启停程序"
          example: "冷机启动：冷却塔→冷却水泵→冷机→冷冻水泵"
        - name: "模式切换"
          description: "运行模式转换逻辑"
          example: "正常→消毒→值班"
      interlock_protection:
        - name: "联锁保护"
          examples:
            - "冷却水流量低→冷机停机"
            - "防冻温度低→热水阀开启"
            - "过滤器压差高→报警"
            - "风机故障→阀门关闭"
        - name: "消防联锁"
          source: "FAS硬接点信号"
          actions:
            - "关闭非消防风机"
            - "关闭防火阀"
            - "启动排烟风机"
    local_defaults:
      description: "网络中断时使用的默认设定值"
      values:
        operating_room_temp: "22°C"
        operating_room_humidity: "50%RH"
        operating_room_pressure: "+15Pa"
        icu_temp: "24°C"
        chw_supply_temp: "7°C"
        hw_supply_temp: "60°C"
    failure_impact: |
      单个DDC失效时：
      - 该区域控制中断
      - 执行器保持最后状态或安全位置
      - 其他区域不受影响
    recovery: "控制器重启后30秒内恢复控制"
  
  L3_Hardware_Protection:
    name: "硬件保护层"
    description: "最后一道防线，纯物理/电气保护"
    characteristics:
      - "无需供电（机械动作）"
      - "无需通信"
      - "不可被软件覆盖"
      - "定期校验"
    devices:
      mechanical_thermostat:
        application: "手术室、ICU"
        type: "双金属片式"
        range: "18-26°C"
        action: "直接控制加热阀"
        scenario: "当DDC完全失效时，机械恒温器接管温度控制"
      freeze_protection_switch:
        application: "表冷器、新风段"
        type: "低温断开开关"
        setpoint: "<5°C"
        action: 
          - "强制打开热水阀"
          - "关闭新风阀"
          - "停止送风机（可选）"
        scenario: "防止盘管冻裂"
      fire_damper_fusible_link:
        application: "穿越防火分区的风管"
        type: "易熔合金（70°C/280°C）"
        action: "弹簧驱动关闭阀片"
        scenario: "阻止火灾蔓延，无需任何控制信号"
      pressure_relief_valve:
        application: "锅炉、压缩机"
        type: "弹簧式安全阀"
        action: "超压自动开启泄放"
        scenario: "防止设备爆炸"
      emergency_stop:
        application: "大型设备"
        type: "硬线直连接触器"
        action: "直接切断电源"
        scenario: "紧急情况下人员可立即停机"
```

### 2.3 层级间通信与切换

```yaml
Inter_Layer_Communication:
  
  L1_L2_Interface:
    protocol: "BACnet/IP"
    data_exchange:
      L1_to_L2:
        - "优化设定值（如冷冻水温度优化值）"
        - "运行模式指令（如夜间节能模式）"
        - "时间表更新"
        - "参数调整"
      L2_to_L1:
        - "实时测量值"
        - "设备运行状态"
        - "报警信息"
        - "能耗数据"
    network_loss_behavior:
      detection: "心跳超时30秒"
      L2_action:
        - "切换到本地默认设定值"
        - "记录网络中断事件"
        - "继续按本地逻辑运行"
      recovery:
        - "网络恢复后自动重连"
        - "同步时钟"
        - "上传离线期间日志"
  
  L2_L3_Interface:
    type: "硬接点/直接机械连接"
    characteristics:
      - "无通信协议"
      - "物理信号或机械动作"
      - "L3始终处于监视状态"
    examples:
      - name: "防冻开关与热水阀"
        connection: "防冻开关常开触点串联在热水阀控制回路"
        behavior: "温度<5°C时，开关动作，无论DDC输出什么，热水阀强制开启"
      - name: "紧急停止与接触器"
        connection: "急停按钮串联在接触器线圈回路"
        behavior: "按下急停，电机立即断电，DDC无法覆盖"
  
  Degradation_Sequence:
    name: "渐进式降级序列"
    stages:
      - stage: 1
        name: "正常模式 (NORMAL)"
        condition: "所有系统正常"
        characteristics:
          - "L1优化算法激活"
          - "能效最优"
          - "全功能可用"
      - stage: 2
        name: "基础模式 (BASIC)"
        trigger: "L1通信中断"
        characteristics:
          - "L2本地控制"
          - "使用默认设定值"
          - "能效略降（10-15%）"
          - "基本功能完整"
      - stage: 3
        name: "安全模式 (SAFE)"
        trigger: "部分传感器失效"
        characteristics:
          - "切换到备用传感器或软测量"
          - "控制精度略降"
          - "加强报警"
      - stage: 4
        name: "保护模式 (PROTECTED)"
        trigger: "DDC失效"
        characteristics:
          - "执行器保持安全位置"
          - "L3硬件保护激活"
          - "需人工干预恢复"
      - stage: 5
        name: "应急模式 (EMERGENCY)"
        trigger: "完全断电"
        characteristics:
          - "UPS供电关键设备"
          - "发电机接管"
          - "最小功能维持"
```

---

## 第三章 手术室三级控制保障

### 3.1 手术室控制架构

手术室（MED-OR）作为P0级生命安全区域，必须具备完整的三级控制保障。

```yaml
Operating_Room_Control_Architecture:
  
  system_ref: "MED-OR (Agent-01)"
  coupling_ref: "CU-OR-HVAC-CLN (Agent-05)"
  
  environmental_requirements:
    temperature:
      setpoint: "22-25°C"
      adjustable_range: "21-27°C"
      tolerance: "±1°C"
      source: "GB50333-2013"
    humidity:
      range: "40-60%RH"
      tolerance: "±5%RH"
    pressure:
      value: "+15Pa"  # 相对走廊
      gradient: "手术室 > 洁净走廊 > 换车间 > 污物走廊"
      tolerance: "±3Pa"
    cleanliness:
      class_I: "≤100粒/m³ (≥0.5μm)"
      class_II: "≤1000粒/m³"
      class_III: "≤10000粒/m³"
    air_change:
      class_I: "≥36次/h"
      class_II: "≥24次/h"
      class_III: "≥18次/h"
  
  L1_Cloud_Functions:
    location: "中央控制室/BMS服务器"
    functions:
      - name: "手术排程优化"
        description: "根据手术排程预调节环境"
        input: "HIS手术排程接口"
        action: "提前30分钟启动预调"
      - name: "能效分析"
        description: "分析各手术室能耗"
        output: "月度能效报告"
      - name: "预测性维护"
        description: "HEPA过滤器寿命预测"
        basis: "压差趋势+运行时间"
      - name: "远程监控"
        description: "护士站/医生办公室查看状态"
    failure_mode:
      impact: "手术排程优化停止，基本控制不受影响"
      recovery: "网络恢复后自动恢复"
  
  L2_DDC_Control:
    controller: "DDC-OR-001"
    location: "手术部控制柜间"
    
    control_loops:
      - loop_id: "LOOP-OR-TEMP"
        name: "室温控制回路"
        structure: "Cascade PID"
        master:
          PV: "Room Temperature"
          SP: "Operator Setting (22°C default)"
          output: "Supply Air Temp Setpoint"
          algorithm: "PID"
          params: {Kp: 2.0, Ti: 600, Td: 0}
        slave:
          PV: "Supply Air Temperature"
          SP: "From Master Output"
          output: "CHW Valve Position"
          algorithm: "PI"
          params: {Kp: 1.5, Ti: 180}
        local_default:
          condition: "Network Loss OR Sensor Failure"
          action: "Supply Air Temp = 16°C (Fixed)"
      
      - loop_id: "LOOP-OR-RH"
        name: "湿度控制回路"
        structure: "Single PID with limits"
        PV: "Room Humidity"
        SP: "50%RH (default)"
        output: "Humidifier/Reheat control"
        constraints:
          - "露点温度 < 送风温度 - 2°C"
          - "送风相对湿度 < 90%"
        local_default:
          action: "Humidifier OFF, Reheat AUTO"
      
      - loop_id: "LOOP-OR-PRESSURE"
        name: "压差控制回路"
        structure: "PI Control"
        PV: "Room Pressure (vs Corridor)"
        SP: "+15Pa"
        output: "Exhaust Damper Position"
        algorithm: "PI"
        params: {Kp: 1.0, Ti: 30}
        critical: true
        note: "压差是洁净度的关键保障"
        local_default:
          action: "Exhaust Damper = 30% (固定开度)"
    
    sequence_logic:
      - sequence: "OR_STARTUP"
        steps:
          1: {action: "Open OA Damper to 10%", wait: "5s"}
          2: {action: "Start Supply Fan", wait: "10s"}
          3: {action: "Verify Fan Status = RUN", timeout: "30s"}
          4: {action: "Start Return Fan", wait: "5s"}
          5: {action: "Enable Pressure Control", wait: "2s"}
          6: {action: "Ramp OA Damper to Setpoint", duration: "60s"}
          7: {action: "Enable Temp/RH Control"}
          8: {action: "Wait for Room Conditions OK", timeout: "30min"}
          9: {action: "Set Status = READY"}
      
      - sequence: "OR_SHUTDOWN"
        steps:
          1: {action: "Disable Temp/RH Control"}
          2: {action: "Ramp OA Damper to 10%", duration: "30s"}
          3: {action: "Close CHW Valve"}
          4: {action: "Close HW Valve"}
          5: {action: "Stop Return Fan", wait: "5s"}
          6: {action: "Stop Supply Fan", wait: "5s"}
          7: {action: "Close OA Damper"}
          8: {action: "Set Status = OFF"}
    
    interlock_logic:
      - interlock: "Supply Fan Failure"
        condition: "SF_Status = OFF AND SF_Command = ON for 30s"
        actions:
          - "Stop Return Fan"
          - "Close OA Damper"
          - "Close CHW/HW Valves"
          - "Generate CRITICAL Alarm"
          - "Notify OR Nurse Station"
      
      - interlock: "Fire Alarm"
        condition: "FIRE_SIGNAL = TRUE from FAS"
        actions:
          - "Execute OR_EMERGENCY_SHUTDOWN"
          - "Close Fire Dampers"
          - "Open Smoke Exhaust (if designated)"
        priority: "HIGHEST - Cannot be overridden"
      
      - interlock: "Freeze Protection"
        condition: "Coil_Temp < 5°C"
        actions:
          - "Open HW Valve to 100%"
          - "Close OA Damper to 0%"
          - "Generate URGENT Alarm"
  
  L3_Hardware_Protection:
    devices:
      - device: "Mechanical Thermostat"
        location: "手术室内墙面"
        type: "双金属片式"
        range: "18-26°C"
        connection: "直接控制备用加热器"
        activation: "当DDC失效且温度<18°C或>26°C时动作"
        purpose: "确保即使DDC完全失效，室温仍在安全范围"
      
      - device: "Freeze Protection Switch"
        location: "表冷器后"
        type: "毛细管感温式"
        setpoint: "5°C"
        connection: "串联在新风阀控制回路"
        action:
          - "强制关闭新风阀"
          - "同时发送信号到DDC (如果可用)"
        purpose: "防止盘管冻裂"
      
      - device: "Fire Damper (70°C)"
        location: "穿越防火分区处"
        type: "易熔合金驱动"
        fusible_link: "70°C"
        action: "弹簧驱动关闭"
        purpose: "阻止火灾蔓延"
      
      - device: "Smoke Fire Damper (280°C)"
        location: "排烟风管"
        type: "电动+易熔"
        fusible_link: "280°C"
        action:
          normal: "电动开启用于排烟"
          failsafe: "280°C时熔断关闭"
        purpose: "排烟但防止高温蔓延"
      
      - device: "Pressure Relief Damper"
        location: "手术室送风总管"
        type: "重锤式"
        setpoint: "+50Pa"
        action: "超压自动开启泄放"
        purpose: "防止洁净区超压损坏门密封"
```

### 3.2 手术室传感器配置

```yaml
OR_Sensor_Configuration:
  
  temperature_sensors:
    - sensor_id: "SENS-OR001-RT"
      type: "Room Temperature"
      location: "手术室墙面，距地1.5m"
      mounting: "嵌入式"
      range: "15-35°C"
      accuracy: "±0.3°C"
      output: "PT1000"
      redundancy: "Dual Sensor"
      backup: "SENS-OR001-RT-B"
      failure_mode:
        detection: "deviation > 2°C from backup"
        action: "Switch to backup, alarm"
    
    - sensor_id: "SENS-OR001-SAT"
      type: "Supply Air Temperature"
      location: "送风总管，HEPA前2m"
      mounting: "插入式"
      range: "10-40°C"
      accuracy: "±0.3°C"
      output: "4-20mA"
      sampling_rate: "1s"
    
    - sensor_id: "SENS-OR001-RAT"
      type: "Return Air Temperature"
      location: "回风口内"
      mounting: "插入式"
      range: "15-35°C"
      accuracy: "±0.5°C"
      output: "4-20mA"
  
  humidity_sensors:
    - sensor_id: "SENS-OR001-RRH"
      type: "Room Humidity"
      location: "与室温传感器同位置"
      mounting: "嵌入式"
      range: "20-80%RH"
      accuracy: "±2%RH"
      output: "4-20mA"
    
    - sensor_id: "SENS-OR001-SARH"
      type: "Supply Air Humidity"
      location: "送风总管"
      range: "20-95%RH"
      accuracy: "±2%RH"
  
  pressure_sensors:
    - sensor_id: "SENS-OR001-RP"
      type: "Room Pressure (Differential)"
      reference: "洁净走廊"
      location: "手术室墙面"
      range: "-50 to +100 Pa"
      accuracy: "±1Pa"
      output: "4-20mA"
      critical: true
      redundancy: "Dual Sensor"
    
    - sensor_id: "SENS-OR001-FDP"
      type: "Filter Differential Pressure"
      location: "HEPA过滤器两侧"
      range: "0-500Pa"
      accuracy: "±5Pa"
      alarm_threshold:
        warning: "350Pa"
        critical: "450Pa"
        action: "更换过滤器"
  
  airflow_sensors:
    - sensor_id: "SENS-OR001-SAF"
      type: "Supply Air Flow"
      location: "送风总管"
      method: "Pitot Array"
      range: "0-5000 m³/h"
      accuracy: "±5%"
  
  particle_counter:
    - sensor_id: "SENS-OR001-PC"
      type: "Particle Counter"
      location: "手术区层流送风下方"
      channels: ["≥0.5μm", "≥5μm"]
      sampling: "每5分钟"
      alarm_threshold:
        class_I: "100粒/m³ (≥0.5μm)"
        class_II: "1000粒/m³"
      note: "非连续监测，定期采样"
  
  soft_sensors:
    - sensor_id: "SOFT-OR001-LOAD"
      type: "Cooling Load Estimation"
      calculation: |
        Q = ρ × V × Cp × (T_return - T_supply)
        where:
          ρ = 1.2 kg/m³ (air density)
          V = Supply Air Flow (m³/s)
          Cp = 1.006 kJ/kg·K
          T = Temperatures (°C)
      inputs: ["SENS-OR001-SAF", "SENS-OR001-SAT", "SENS-OR001-RAT"]
      output: "Estimated Cooling Load (kW)"
      usage: "负荷趋势分析，优化控制"
```

---

## 第四章 冷站群控逻辑

### 4.1 冷站系统概述

```yaml
Chiller_Plant_Overview:
  
  system_ref: "HVAC-CHP (Agent-01)"
  
  design_parameters:
    total_cooling_capacity: "8000 kW"
    chiller_configuration: "4 × 2000kW (N+1)"
    chw_design_temp:
      supply: "7°C"
      return: "12°C"
      delta_T: "5°C"
    cw_design_temp:
      supply: "32°C"
      return: "37°C"
    
  equipment:
    chillers:
      - id: "CH-001"
        type: "离心式"
        capacity: "2000kW"
        COP: "5.5"
        min_load: "25%"
        priority: 1
      - id: "CH-002"
        type: "离心式"
        capacity: "2000kW"
        COP: "5.5"
        min_load: "25%"
        priority: 2
      - id: "CH-003"
        type: "螺杆式"
        capacity: "2000kW"
        COP: "5.2"
        min_load: "20%"
        priority: 3
      - id: "CH-004"
        type: "螺杆式"
        capacity: "2000kW"
        COP: "5.2"
        min_load: "20%"
        priority: 4  # 备用
    
    primary_pumps:
      type: "定频一次泵"
      configuration: "一机一泵"
      flow: "400 m³/h each"
    
    secondary_pumps:
      type: "变频二次泵"
      quantity: 4
      configuration: "N+1"
      flow: "400 m³/h each (design)"
      vfd: true
    
    cooling_towers:
      type: "逆流式"
      quantity: 4
      configuration: "一机一塔"
      capacity: "2500kW each"
      fans: "变频"
```

### 4.2 冷机群控逻辑

```yaml
Chiller_Staging_Logic:
  
  controller: "DDC-CHP-001"
  location: "冷冻机房控制柜"
  
  load_calculation:
    method: "基于Agent-04物理方程"
    formula: |
      Q_load = ρ × V × Cp × ΔT
      where:
        Q_load = 系统冷负荷 (kW)
        ρ = 1000 kg/m³ (水密度)
        V = 系统总流量 (m³/s)
        Cp = 4.186 kJ/kg·K (水比热)
        ΔT = T_return - T_supply (K)
    inputs:
      - "SENS-CHP-CHW-FLOW (总冷冻水流量)"
      - "SENS-CHP-CHWR-TEMP (冷冻水回水温度)"
      - "SENS-CHP-CHWS-TEMP (冷冻水供水温度)"
    output: "Current_Load_kW"
  
  staging_parameters:
    add_chiller_threshold: "85%"  # 当前运行冷机总负荷率
    remove_chiller_threshold: "50%"
    staging_delay: "10 minutes"  # 防止频繁启停
    min_runtime: "30 minutes"  # 冷机最短运行时间
    min_offtime: "15 minutes"  # 冷机最短停机时间
  
  add_chiller_sequence:
    name: "加机程序"
    trigger: |
      (Current_Load / Running_Capacity) > 85%
      持续 10 分钟
    pre_conditions:
      - "有可启动的冷机"
      - "冷机无故障"
      - "对应冷却塔可用"
      - "对应水泵可用"
    steps:
      - step: 1
        action: "选择下一优先级冷机"
        logic: "按优先级顺序，选择第一台可用冷机"
      - step: 2
        action: "启动冷却塔风机"
        wait: "30s"
        verify: "风机运行确认"
      - step: 3
        action: "启动冷却水泵"
        wait: "30s"
        verify: "水泵运行确认 + 流量正常"
      - step: 4
        action: "启动冷水机组"
        wait: "120s"
        verify: "冷机运行确认 + 无故障"
      - step: 5
        action: "启动对应一次冷冻水泵"
        wait: "30s"
        verify: "水泵运行确认"
      - step: 6
        action: "重新分配负荷"
        logic: "均匀分配到所有运行冷机"
      - step: 7
        action: "确认稳定运行"
        wait: "300s"
        verify: "冷冻水温度在设定范围"
  
  remove_chiller_sequence:
    name: "减机程序"
    trigger: |
      (Current_Load / Running_Capacity) < 50%
      持续 10 分钟
      且运行冷机 > 1 台
    pre_conditions:
      - "减机后剩余容量能满足负荷"
      - "冷机已运行超过最短运行时间"
    steps:
      - step: 1
        action: "选择待停冷机"
        logic: "运行时间最长 或 效率最低"
      - step: 2
        action: "逐步减少该冷机负荷"
        duration: "300s"
        target: "负荷降至20%"
      - step: 3
        action: "停止冷水机组"
      - step: 4
        action: "停止对应一次冷冻水泵"
        wait: "10s"
      - step: 5
        action: "延时后停止冷却水泵"
        delay: "300s"
        reason: "冷却冷机残余热量"
      - step: 6
        action: "停止冷却塔风机"
        condition: "无其他冷机使用该塔"
      - step: 7
        action: "重新分配负荷"
  
  optimization_logic:
    chw_temp_reset:
      name: "冷冻水温度优化重设"
      method: "基于末端阀位"
      logic: |
        IF 所有末端阀位 < 85% THEN
          CHWS_Setpoint += 0.2°C (最高12°C)
        ELSEIF 任一末端阀位 > 95% THEN
          CHWS_Setpoint -= 0.2°C (最低6°C)
      source: "L1优化层"
      fallback: "L1断开时使用7°C默认值"
    
    condenser_water_temp_reset:
      name: "冷却水温度优化"
      method: "基于室外湿球温度"
      logic: |
        CW_Supply_Setpoint = MAX(18°C, 室外湿球 + 3°C)
      limit: "≤ 32°C"
  
  protection_logic:
    chiller_protection:
      - protection: "冷冻水流量低"
        condition: "CHW_Flow < 60% of design"
        action: "停止冷机，报警"
      - protection: "冷却水流量低"
        condition: "CW_Flow < 60% of design"
        action: "停止冷机，报警"
      - protection: "冷凝压力高"
        condition: "Condenser_Pressure > High_Limit"
        action: "增加冷却塔风速，必要时停机"
      - protection: "蒸发温度低"
        condition: "Evaporator_Temp < Low_Limit"
        action: "降低冷机负荷，防止结冰"
    
    freeze_protection:
      condition: "CHW_Temp < 4°C"
      actions:
        - "关闭所有冷机"
        - "开启热水旁通"
        - "CRITICAL 报警"
    
    pump_protection:
      - protection: "泵干转"
        condition: "Pump_Run AND Flow = 0 for 30s"
        action: "停止水泵，报警"
  
  local_defaults:
    network_loss_behavior:
      - "保持当前运行冷机数量"
      - "冷冻水温度设定值 = 7°C"
      - "冷却水温度设定值 = 32°C"
      - "禁止自动加机（安全考虑）"
      - "允许人工现场加机"
```

---

## 第五章 安全与降级策略

### 5.1 消防联动矩阵

```yaml
Fire_Interlock_Matrix:
  
  signal_source: "FIRE-FAS (Agent-01)"
  signal_types:
    - "FIRE_ALARM: 火灾确认信号"
    - "FIRE_FLOOR: 着火楼层号"
    - "SMOKE_ZONE: 防烟分区号"
  
  hvac_response:
    system: "HVAC-AHU (空调机组)"
    actions:
      - trigger: "FIRE_ALARM = TRUE"
        scope: "全院"
        action:
          - "所有空调机组停止"
          - "关闭所有新风阀"
          - "关闭所有回风阀"
        exception:
          - "正压送风机组保持待命"
          - "排烟风机系统由FAS控制"
        priority: "最高，不可覆盖"
    
      - trigger: "着火楼层识别"
        scope: "着火楼层"
        action:
          - "关闭该楼层所有AHU"
          - "关闭穿越防火分区的防火阀"
          - "关闭着火楼层水阀"
  
  chiller_plant_response:
    system: "HVAC-CHP (冷热源)"
    actions:
      - trigger: "FIRE_ALARM = TRUE"
        scope: "冷站"
        action:
          - "保持冷冻水泵运行"
          - "关闭着火楼层供水阀"
        rationale: "消防时可能仍需冷却关键设备"
        exception:
          - "如冷站本身着火，则全停"
  
  smoke_control_response:
    system: "FIRE-EXH (防排烟)"
    actions:
      - trigger: "FIRE_ALARM = TRUE"
        scope: "着火区域"
        action:
          - "开启排烟风机"
          - "开启排烟阀"
          - "开启正压送风机"
          - "开启楼梯间加压风阀"
        control: "由FAS直接控制（硬接点）"
  
  operating_room_special:
    system: "MED-OR (手术室)"
    scenario: "手术进行中发生火灾"
    actions:
      - step: 1
        action: "接收火灾确认信号"
        note: "由医护人员判断是否中断手术"
      - step: 2
        action: "如非本区火灾"
        response:
          - "维持正压状态"
          - "切换到100%循环风"
          - "关闭新风阀"
          - "继续手术"
      - step: 3
        action: "如本区火灾"
        response:
          - "立即中断手术"
          - "执行紧急撤离程序"
          - "关闭手术室AHU"
          - "关闭医气阀门"
    interlock_wiring: "FAS → 硬接点 → DDC-OR"
  
  interlock_matrix_table:
    # 设备/系统级联动矩阵
    format: "触发信号 → 受控设备 → 动作"
    entries:
      - id: "FI-001"
        trigger: "火灾确认"
        target: "AHU-xx"
        action: "停止"
        wiring: "硬接点"
        priority: "P0"
      - id: "FI-002"
        trigger: "火灾确认"
        target: "FCU-xx"
        action: "关闭水阀"
        wiring: "DDC指令"
        priority: "P1"
      - id: "FI-003"
        trigger: "火灾确认"
        target: "防火阀FD-xx"
        action: "关闭"
        wiring: "硬接点（电磁释放）"
        priority: "P0"
      - id: "FI-004"
        trigger: "火灾确认"
        target: "排烟风机SEF-xx"
        action: "启动"
        wiring: "硬接点"
        priority: "P0"
      - id: "FI-005"
        trigger: "火灾确认"
        target: "正压风机SPF-xx"
        action: "启动"
        wiring: "硬接点"
        priority: "P0"
      - id: "FI-006"
        trigger: "火灾确认"
        target: "电梯EL-xx"
        action: "迫降首层"
        wiring: "硬接点"
        priority: "P0"
      - id: "FI-007"
        trigger: "火灾确认"
        target: "非消防电源"
        action: "切断"
        wiring: "硬接点（分励脱扣）"
        priority: "P0"
      - id: "FI-008"
        trigger: "火灾确认"
        target: "应急照明EL-xx"
        action: "启动"
        wiring: "自动（电源切换）"
        priority: "P0"
      - id: "FI-009"
        trigger: "火灾确认"
        target: "门禁系统"
        action: "紧急开启"
        wiring: "硬接点"
        priority: "P0"
```

### 5.2 断网/传感器故障对策

```yaml
Fault_Tolerance_Strategies:
  
  network_failure:
    detection:
      method: "心跳超时"
      timeout: "30秒"
      confirmation: "连续3次心跳失败"
    
    response_by_system:
      operating_room:
        controller: "DDC-OR-xxx"
        action:
          - "切换到本地默认设定值"
          - "温度设定 = 22°C"
          - "湿度设定 = 50%RH"
          - "压差设定 = +15Pa"
          - "维持当前运行模式"
          - "本地HMI显示'网络断开'"
        duration: "可持续48小时"
        note: "UPS供电下可持续运行"
      
      chiller_plant:
        controller: "DDC-CHP-001"
        action:
          - "保持当前运行冷机"
          - "禁止自动加机"
          - "允许自动减机"
          - "冷冻水温度 = 7°C（默认）"
          - "冷却水温度 = 32°C（默认）"
        rationale: "防止网络恢复后负荷突变"
      
      general_ahu:
        controller: "DDC-AHU-xxx"
        action:
          - "按时间表运行（本地存储）"
          - "使用默认温度设定"
          - "节能模式暂停"
    
    recovery:
      trigger: "网络连接恢复"
      steps:
        - "自动重连BMS"
        - "同步时钟"
        - "上传离线日志"
        - "下载最新设定值"
        - "恢复优化控制"
  
  sensor_failure:
    detection_methods:
      - method: "范围检查"
        logic: "测量值超出物理可能范围"
        example: "温度 > 100°C 或 < -40°C"
      - method: "变化率检查"
        logic: "变化率超出物理可能"
        example: "室温1分钟内变化 > 5°C"
      - method: "一致性检查"
        logic: "相关传感器矛盾"
        example: "送风温度 < 冷冻水温度"
      - method: "偏差检查"
        logic: "冗余传感器偏差过大"
        example: "双传感器偏差 > 2°C"
    
    response_by_sensor_type:
      room_temperature:
        sensor: "SENS-OR001-RT"
        backup_strategy:
          primary: "切换到备用传感器 SENS-OR001-RT-B"
          secondary: "使用回风温度估算"
          tertiary: "使用送风温度+负荷估算（软测量）"
        fallback_value:
          method: "Hold Last Valid"
          duration: "15分钟"
          then: "切换到固定设定值模式"
        alarm: "HIGH - 传感器故障"
      
      supply_air_temperature:
        sensor: "SENS-OR001-SAT"
        backup_strategy:
          primary: "使用表冷器出口温度"
          secondary: "基于阀位和负荷估算"
        fallback_value: "16°C（安全值）"
        alarm: "HIGH"
      
      room_pressure:
        sensor: "SENS-OR001-RP"
        critical: true
        backup_strategy:
          primary: "切换到备用传感器"
          secondary: "固定排风阀开度模式"
        fallback_value: "排风阀 = 30%（经验值）"
        alarm: "CRITICAL - 需立即处理"
        note: "压差是洁净室关键参数"
      
      chw_flow:
        sensor: "SENS-CHP-CHW-FLOW"
        backup_strategy:
          primary: "基于泵频率和扬程曲线估算"
          secondary: "使用设计流量值"
        impact: "负荷计算精度下降"
        alarm: "MEDIUM"
    
    soft_sensor_fallback:
      description: "当物理传感器失效时，使用物理模型估算"
      examples:
        - parameter: "房间冷负荷"
          model: "Q = ρ × V × Cp × ΔT"
          inputs: ["风量", "送风温度", "回风温度"]
          accuracy: "±15%"
        - parameter: "冷冻水流量"
          model: "基于水泵特性曲线"
          inputs: ["泵频率", "进出口压差"]
          accuracy: "±10%"
  
  controller_failure:
    detection:
      method: "看门狗超时"
      timeout: "60秒"
      indicator: "控制器不响应"
    
    response:
      actuator_behavior:
        valves:
          - "CHW Valve: 保持最后位置 (HOLD_LAST)"
          - "HW Valve: 弹簧复位开启 (FAIL_OPEN)"
          - "OA Damper: 弹簧复位关闭 (FAIL_CLOSE)"
        fans:
          - "继续运行（接触器保持）"
          - "VFD保持最后频率"
        pumps:
          - "继续运行（除非联锁触发）"
      
      L3_takeover:
        - "机械恒温器接管温度控制"
        - "防冻开关保护盘管"
        - "紧急停止按钮可用"
      
      notification:
        - "中控室报警"
        - "自动派发维修工单"
        - "备用控制器自动接管（如配置）"
    
    recovery:
      - "控制器自动重启"
      - "加载保存的运行参数"
      - "30秒内恢复自动控制"
      - "记录故障日志"
```

---

## 第六章 总结与实施建议

### 6.1 白皮书核心要点

```yaml
Key_Takeaways:
  
  architecture:
    principle: "三级控制保障 (L1/L2/L3)"
    benefit: "任意单点故障不导致系统失控"
  
  philosophy:
    principle: "分层自治、逐级降级、本质安全"
    benefit: "渐进式降级而非二元崩溃"
  
  critical_areas:
    focus: "手术室、ICU作为P0优先级"
    measures:
      - "双传感器冗余"
      - "本地默认设定值"
      - "机械硬件后备"
      - "独立UPS供电"
  
  chiller_plant:
    strategy: "保守的加减机逻辑"
    measures:
      - "网络断开时禁止自动加机"
      - "10分钟延时防止频繁启停"
      - "本地7°C默认水温"
  
  fire_safety:
    strategy: "硬接点联动优先"
    measures:
      - "消防信号直接控制执行器"
      - "不经过网络"
      - "软件不可覆盖"
  
  sensor_failure:
    strategy: "多级备用"
    measures:
      - "物理备用传感器"
      - "软测量算法"
      - "保持最后有效值"
      - "切换到安全默认值"
```

### 6.2 实施检查清单

```yaml
Implementation_Checklist:
  
  design_phase:
    - item: "所有P0区域配置双传感器"
      responsible: "设计院"
      deliverable: "传感器点位图"
    - item: "定义所有执行器失效安全位置"
      responsible: "设计院"
      deliverable: "执行器规格书"
    - item: "消防联动采用硬接点"
      responsible: "设计院 + 消防顾问"
      deliverable: "消防联动矩阵"
  
  procurement_phase:
    - item: "DDC控制器具备本地存储"
      responsible: "采购"
      spec: "≥72小时程序保持"
    - item: "执行器配置弹簧复位"
      responsible: "采购"
      spec: "按失效安全位置要求"
    - item: "关键控制器配置电池后备"
      responsible: "采购"
      spec: "≥72小时数据保持"
  
  installation_phase:
    - item: "消防联动硬接点接线"
      responsible: "施工方"
      verification: "点对点测试"
    - item: "DDC默认参数预置"
      responsible: "调试工程师"
      verification: "断网测试"
    - item: "机械恒温器安装校验"
      responsible: "施工方"
      verification: "动作测试"
  
  commissioning_phase:
    - item: "断网48小时测试"
      responsible: "调试工程师"
      acceptance: "关键区域参数偏差<5%"
    - item: "单传感器故障测试"
      responsible: "调试工程师"
      acceptance: "自动切换备用"
    - item: "消防联动测试"
      responsible: "消防验收"
      acceptance: "所有设备正确动作"
    - item: "降级模式切换测试"
      responsible: "调试工程师"
      acceptance: "正常→基础→安全模式"
  
  operation_phase:
    - item: "定期默认参数审核"
      responsible: "运维"
      frequency: "每年"
    - item: "机械保护装置校验"
      responsible: "运维"
      frequency: "每季度"
    - item: "消防联动演练"
      responsible: "安保 + 运维"
      frequency: "每年"
```

---

## 附录A：术语定义

| 术语 | 英文 | 定义 |
|------|------|------|
| 失效安全位置 | Fail-Safe Position | 执行器在信号丢失或断电时应保持的位置 |
| 渐进式降级 | Graceful Degradation | 故障时系统逐级降低功能而非完全崩溃 |
| 软测量 | Soft Sensor | 基于物理模型和其他传感器数据估算参数 |
| 看门狗 | Watchdog | 监控控制器运行状态的定时器机制 |
| 硬接点 | Hard-wired Point | 直接电气连接，不经过通信网络 |
| 本地默认值 | Local Default Value | 网络中断时DDC使用的预设设定值 |

---

## 附录B：参考文献

1. GB50333-2013 医院洁净手术部建筑技术规范
2. GB51039-2014 综合医院建筑设计规范
3. GB50116-2013 火灾自动报警系统设计规范
4. ASHRAE Guideline 36-2021 高性能序列控制
5. Agent-01 系统拓扑建模师输出文档
6. Agent-03 设备本体建模师输出文档
7. Agent-04 流动模型建模师输出文档
8. Agent-05 耦合关系建模师输出文档

---

**白皮书结束**

---

接下来，我将开始输出具体的YAML模型（传感器模型、执行器模型、控制回路模型、序列模型等）。是否继续？
[^1]: [# 医疗专用空间详细建模（Medical Spe...   - terminal_locations](# 医疗专用空间详细建模（Medical Spe...   - terminal_locations)

[^2]: [# Agent-05和Agent-07输出文件重..."

[^3]: [Agent-01 系统拓扑建模师 - 完整输出文档.md](http://file/fb792853-9410-4a6d-9389-5740af5b6fee.md)

[^4]: [Agent-01 系统拓扑建模师 - 第四批次：消防系统 + 医疗专业系统.md](http://file/2f672527-5466-46d6-b255-27eed6ebc9e5.md)

[^5]: [# Agent-05和Agent-07输出文件重..."

[^6]: [# 医疗建筑空间分类体系（Healthcare ..."防振动", "UPS供电", "患者通话"]](# 医疗建筑空间分类体系（Healthcare ..."防振动", "UPS供电", "患者通话"])

[^1]: [# Agent-05和Agent-07输出文件重..."

[^2]: [Agent-01 系统拓扑建模师 - 第五批次：暖通系统详细设计 + 电梯系统.md](http://file/c8c2f0a4-41ac-41f1-bd84-627b22fbffd9.md)

[^3]: [Agent-01 系统拓扑建模师 - 完整输出文档.md](http://file/fb792853-9410-4a6d-9389-5740af5b6fee.md)

[^4]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^5]: [Agent-01 系统拓扑建模师 - 第一批次：HVAC核心系统 （第三次修订版）.md](http://file/407a8528-954f-47c2-86d1-accee6b470da.md)

[^6]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^1]: [# Agent-09: 统一交叉引用索引系统

[^2]: [Agent-01 系统拓扑建模师 - 第二批次：电气系统 + 医疗气体系 （第三次修订版）.md](http://file/4cd17d72-bd32-43f9-a072-b383fd70c5fc.md)

[^3]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^4]: [# Agent-05和Agent-07输出文件重..."

[^5]: [Agent-01 系统拓扑建模师 - 完整输出文档.md](http://file/fb792853-9410-4a6d-9389-5740af5b6fee.md)

[^6]: [Agent-01 系统拓扑建模师 - 第三批次：给排水系统 + 智能化系统 （第三次修订版）.md](http://file/2c5c22aa-538a-48f4-a855-217265a1ca20.md)

[^1]: [Agent-01 系统拓扑建模师 - 第六批次：最终系统与综合集成.md](http://file/8b4c44db-7e14-4e27-9c8a-35285cf290c0.md)

[^2]: [Agent-01 系统拓扑建模师 - 第四批次：消防系统 + 医疗专业系统.md](http://file/2f672527-5466-46d6-b255-27eed6ebc9e5.md)

[^3]: [Agent-01 系统拓扑建模师 - 完整输出文档.md](http://file/fb792853-9410-4a6d-9389-5740af5b6fee.md)

[^4]: [Agent-01 系统拓扑建模师 - 第四批次：消防系统 + 医疗专业系统.md](http://file/2f672527-5466-46d6-b255-27eed6ebc9e5.md)

[^5]: [Agent-01 系统拓扑建模师 - 第四批次：消防系统 + 医疗专业系统.md](http://file/2f672527-5466-46d6-b255-27eed6ebc9e5.md)

[^6]: [Agent-01 系统拓扑建模师 - 第七批次：运维与实施深化文档.md](http://file/bbf66cdc-5298-4478-a2a0-e10ef0b38607.md)

[^1]: [Agent-01 系统拓扑建模师 - 完整输出文档.md](http://file/fb792853-9410-4a6d-9389-5740af5b6fee.md)

[^2]: [Agent-01 系统拓扑建模师 - 第四批次：消防系统 + 医疗专业系统.md](http://file/2f672527-5466-46d6-b255-27eed6ebc9e5.md)

[^3]: [Agent-01 系统拓扑建模师 - 第四批次：消防系统 + 医疗专业系统.md](http://file/2f672527-5466-46d6-b255-27eed6ebc9e5.md)

[^4]: [Agent-01 系统拓扑建模师 - 第四批次：消防系统 + 医疗专业系统.md](http://file/2f672527-5466-46d6-b255-27eed6ebc9e5.md)

[^5]: [# Agent-05和Agent-07输出文件重..."

[^6]: [# Agent-09: 统一交叉引用索引系统
---