## 🧑‍💻 User


基于修正后的白皮书，以及知识库，执行附件指令

---
## 🤖 Assistant


我现在将根据修正版任务书v3.1，结合白皮书v2.1和知识库中的Agent 01-05资产，执行全域控制系统实现模型的建模工作。让我先搜索知识库获取必要的上游资产。



现在我已经获取了足够的上游资产信息。根据修正版任务书v3.1的要求，我将开始生成**全域控制系统实现模型**文档。

---

# Agent-06 控制系统建模师 - 全域控制系统实现模型
## 基于 Agent 01-05 全资产继承的控制层实例化

**版本**: v3.1
**日期**: 2025-01-XX
**状态**: 正式发布
**前置文档**: 控制架构与降级策略白皮书 v2.1

---

## 文档元数据

```yaml
Agent06_Output:
  meta:
    agent_id: "Agent-06"
    agent_name: "控制系统建模师 (Control System Architect)"
    version: "3.1"
    generated_at: "2025-01-XX"
    
    upstream_dependencies:
      Agent_01:
        asset: "系统拓扑树"
        coverage: "8大系统, 26子系统, 156节点"
        usage: "控制网络架构、系统级启停顺序"
      Agent_02:
        asset: "空间本体与场景"
        coverage: "L0-L5空间层级, 8类医疗专用空间"
        usage: "设定值来源、模式切换状态机"
      Agent_03:
        asset: "设备本体库"
        coverage: "123种设备类型, 18类P0核心设备"
        usage: "I/O点表模板、单体控制逻辑"
      Agent_04:
        asset: "物理方程"
        coverage: "8种载体-荷载耦合方程"
        usage: "前馈控制算法、虚拟传感器"
      Agent_05:
        asset: "耦合单元"
        coverage: "系统-空间耦合关系"
        usage: "闭环控制策略、Criticality等级"
    
    output_scope:
      professional_systems: 6  # HVAC, ELEC, PLUMB, MGAS, FIRE, INT
      subsystems: 26
      control_objects: "500+"
      control_loops: "200+"
      state_machines: "50+"
```

---

# 第一部分：全域感知与执行层 / 全域控制对象清单
## (Universal Sensing & Actuation / Universal Control Objects)

本部分基于Agent-01/02/03，为六大专业建立典型控制对象模型，明确每个对象的I/O点位定义。

---

## 1.1 HVAC 暖通空调系统控制对象

### 1.1.1 HVAC-CHP 冷热源系统

```yaml
# ═══════════════════════════════════════════════════════════════════════════
# 控制对象：离心式冷水机组
# 引用：Agent-01节点 HVAC-CHP_SRC_CHILLER_1
#       Agent-03设备 EQP-CH-CENT
# ═══════════════════════════════════════════════════════════════════════════

Control_Object:
  id: "CO-HVAC-CHP-CH-001"
  name: "1#离心式冷水机组控制对象"
  target_node_ref: "HVAC-CHP_SRC_CHILLER_1"
  equipment_ref: "EQP-CH-CENT"
  space_ref: "BL-MAIN-B1-CHP01"  # Agent-02冷冻站机房
  criticality: "P1-MISSION_CRITICAL"
  
  # ─────────────────────────────────────────────────────────────────────────
  # I/O点位定义
  # ─────────────────────────────────────────────────────────────────────────
  io_points:
    # 模拟量输入 (AI)
    analog_inputs:
      - id: "AI_CHWS_TEMP"
        name: "冷冻水供水温度"
        signal: "4-20mA"
        range: "0-20°C"
        unit: "°C"
        sensor_type: "PT1000"
        accuracy: "±0.3°C"
        scan_rate: "1s"
        critical: true
        
      - id: "AI_CHWR_TEMP"
        name: "冷冻水回水温度"
        signal: "4-20mA"
        range: "0-30°C"
        unit: "°C"
        sensor_type: "PT1000"
        accuracy: "±0.3°C"
        
      - id: "AI_CWS_TEMP"
        name: "冷却水供水温度"
        signal: "4-20mA"
        range: "15-45°C"
        unit: "°C"
        
      - id: "AI_CWR_TEMP"
        name: "冷却水回水温度"
        signal: "4-20mA"
        range: "15-50°C"
        unit: "°C"
        
      - id: "AI_EVAP_PRESS"
        name: "蒸发压力"
        signal: "4-20mA"
        range: "0-1.0MPa"
        unit: "MPa"
        
      - id: "AI_COND_PRESS"
        name: "冷凝压力"
        signal: "4-20mA"
        range: "0-2.0MPa"
        unit: "MPa"
        
      - id: "AI_MOTOR_CURRENT"
        name: "电机电流"
        signal: "4-20mA"
        range: "0-500A"
        unit: "A"
        
      - id: "AI_MOTOR_POWER"
        name: "电机功率"
        signal: "4-20mA"
        range: "0-1500kW"
        unit: "kW"
        
      - id: "AI_OIL_PRESS"
        name: "油压"
        signal: "4-20mA"
        range: "0-1.0MPa"
        unit: "MPa"
        
      - id: "AI_OIL_TEMP"
        name: "油温"
        signal: "4-20mA"
        range: "20-80°C"
        unit: "°C"
        
      - id: "AI_LOAD_PERCENT"
        name: "负荷率"
        signal: "4-20mA"
        range: "0-100%"
        unit: "%"
        source: "冷机本地控制器"
    
    # 数字量输入 (DI)
    digital_inputs:
      - id: "DI_RUN_STATUS"
        name: "运行状态"
        contact: "NO"
        description: "冷机运行确认"
        
      - id: "DI_FAULT"
        name: "故障状态"
        contact: "NC"
        description: "冷机故障报警"
        
      - id: "DI_READY"
        name: "就绪状态"
        contact: "NO"
        description: "冷机可启动"
        
      - id: "DI_LOCAL_REMOTE"
        name: "本地/远程"
        contact: "NO"
        description: "控制模式选择"
        
      - id: "DI_CHW_FLOW_OK"
        name: "冷冻水流量正常"
        contact: "NO"
        description: "流量开关"
        
      - id: "DI_CW_FLOW_OK"
        name: "冷却水流量正常"
        contact: "NO"
        description: "流量开关"
        
      - id: "DI_ANTIFREEZE"
        name: "防冻保护"
        contact: "NC"
        description: "防冻开关动作"
        
      - id: "DI_HIGH_PRESS"
        name: "高压报警"
        contact: "NC"
        description: "冷凝压力高"
        
      - id: "DI_LOW_PRESS"
        name: "低压报警"
        contact: "NC"
        description: "蒸发压力低"
        
      - id: "DI_OIL_PRESS_LOW"
        name: "油压低报警"
        contact: "NC"
        description: "润滑油压力低"
    
    # 模拟量输出 (AO)
    analog_outputs:
      - id: "AO_LOAD_LIMIT"
        name: "负荷限制"
        signal: "4-20mA"
        range: "0-100%"
        unit: "%"
        description: "限制冷机最大负荷"
        
      - id: "AO_CHWS_SP"
        name: "冷冻水温度设定"
        signal: "4-20mA"
        range: "5-12°C"
        unit: "°C"
        description: "冷冻水出水温度设定值"
    
    # 数字量输出 (DO)
    digital_outputs:
      - id: "DO_START"
        name: "启动指令"
        contact: "NO"
        pulse: false
        description: "冷机启动命令"
        
      - id: "DO_STOP"
        name: "停止指令"
        contact: "NO"
        pulse: false
        description: "冷机停止命令"
        
      - id: "DO_RESET"
        name: "故障复位"
        contact: "NO"
        pulse: true
        pulse_duration: "2s"
        description: "冷机故障复位"
    
    # 通信点位 (BACnet/Modbus)
    communication_points:
      protocol: "BACnet/IP"
      device_id: 100001
      objects:
        - object_id: "AV1"
          name: "冷机COP"
          access: "RO"
          description: "实时能效系数"
        - object_id: "AV2"
          name: "累计运行时间"
          access: "RO"
          unit: "h"
        - object_id: "AV3"
          name: "累计启动次数"
          access: "RO"
        - object_id: "MSV1"
          name: "运行模式"
          access: "RO"
          states: ["停机", "待机", "启动中", "运行", "停机中", "故障"]

  # ─────────────────────────────────────────────────────────────────────────
  # 联锁保护逻辑
  # ─────────────────────────────────────────────────────────────────────────
  interlock_logic:
    start_permissive:
      name: "启动允许条件"
      conditions:
        - "DI_READY = TRUE"
        - "DI_LOCAL_REMOTE = REMOTE"
        - "DI_FAULT = FALSE"
        - "DI_CHW_FLOW_OK = TRUE"
        - "DI_CW_FLOW_OK = TRUE"
        - "AI_OIL_TEMP > 25°C"
      all_required: true
      
    run_protection:
      name: "运行保护"
      trips:
        - trigger: "DI_CHW_FLOW_OK = FALSE for 30s"
          action: "STOP"
          severity: "CRITICAL"
          
        - trigger: "DI_CW_FLOW_OK = FALSE for 30s"
          action: "STOP"
          severity: "CRITICAL"
          
        - trigger: "DI_HIGH_PRESS = TRUE"
          action: "STOP"
          severity: "CRITICAL"
          
        - trigger: "DI_LOW_PRESS = TRUE for 60s"
          action: "STOP"
          severity: "HIGH"
          
        - trigger: "AI_MOTOR_CURRENT > 110% × Rated"
          action: "STOP"
          severity: "CRITICAL"
          
        - trigger: "DI_ANTIFREEZE = TRUE"
          action: "STOP + Open HW Valve"
          severity: "CRITICAL"

  # ─────────────────────────────────────────────────────────────────────────
  # Agent-04物理方程引用（用于虚拟传感器）
  # ─────────────────────────────────────────────────────────────────────────
  physics_model:
    equation_ref: "EQ-CHILLER-COP"
    formula: |
      COP = Q_evap / W_comp
      where:
        Q_evap = ρ × V_chw × Cp × (T_chwr - T_chws)
        W_comp = AI_MOTOR_POWER
    virtual_sensors:
      - id: "VS_COOLING_CAPACITY"
        name: "虚拟冷量"
        calculation: "ρ × V × Cp × ΔT"
        inputs: ["AI_CHWS_TEMP", "AI_CHWR_TEMP", "Flow from pump VFD"]
        accuracy: "±5%"
        usage: "负荷计算、能效分析"
```

### 1.1.2 冷冻水泵控制对象

```yaml
Control_Object:
  id: "CO-HVAC-CHP-CHWP-001"
  name: "1#冷冻水泵控制对象"
  target_node_ref: "HVAC-CHP_DST_CHWP_1"
  equipment_ref: "EQP-PUMP-CHW"
  space_ref: "BL-MAIN-B1-CHP01"
  criticality: "P1-MISSION_CRITICAL"
  
  io_points:
    analog_inputs:
      - id: "AI_OUTLET_PRESS"
        name: "出口压力"
        signal: "4-20mA"
        range: "0-1.6MPa"
        unit: "MPa"
        
      - id: "AI_MOTOR_CURRENT"
        name: "电机电流"
        signal: "4-20mA"
        range: "0-200A"
        unit: "A"
        
      - id: "AI_VFD_FREQ"
        name: "变频器频率"
        signal: "4-20mA"
        range: "0-50Hz"
        unit: "Hz"
        source: "VFD反馈"
        
      - id: "AI_VFD_SPEED"
        name: "转速反馈"
        signal: "4-20mA"
        range: "0-3000rpm"
        unit: "rpm"
        
      - id: "AI_FLOW"
        name: "流量"
        signal: "4-20mA"
        range: "0-500m³/h"
        unit: "m³/h"
        sensor_type: "电磁流量计"
        accuracy: "±0.5%"
        
      - id: "AI_BEARING_TEMP"
        name: "轴承温度"
        signal: "4-20mA"
        range: "0-100°C"
        unit: "°C"
    
    digital_inputs:
      - id: "DI_RUN_STATUS"
        name: "运行状态"
        contact: "NO"
        
      - id: "DI_FAULT"
        name: "故障状态"
        contact: "NC"
        
      - id: "DI_VFD_READY"
        name: "变频器就绪"
        contact: "NO"
        
      - id: "DI_VFD_FAULT"
        name: "变频器故障"
        contact: "NC"
        
      - id: "DI_LOCAL_REMOTE"
        name: "本地/远程"
        contact: "NO"
        
      - id: "DI_OVERLOAD"
        name: "过载保护"
        contact: "NC"
    
    analog_outputs:
      - id: "AO_VFD_SPEED_CMD"
        name: "变频器速度指令"
        signal: "4-20mA"
        range: "0-50Hz"
        unit: "Hz"
        description: "控制水泵转速"
    
    digital_outputs:
      - id: "DO_START"
        name: "启动指令"
        contact: "NO"
        
      - id: "DO_STOP"
        name: "停止指令"
        contact: "NO"
        
      - id: "DO_RESET"
        name: "故障复位"
        contact: "NO"
        pulse: true
        
  # Agent-04物理方程：水泵特性曲线
  physics_model:
    equation_ref: "EQ-PUMP-AFFINITY"
    formula: |
      # 水泵相似定律
      Q2/Q1 = n2/n1
      H2/H1 = (n2/n1)²
      P2/P1 = (n2/n1)³
    virtual_sensors:
      - id: "VS_PUMP_EFFICIENCY"
        name: "水泵效率估算"
        calculation: "(ρ × g × Q × H) / (P × 1000)"
        inputs: ["AI_FLOW", "AI_OUTLET_PRESS", "VFD Power"]
```

### 1.1.3 洁净手术室空调箱 (AHU-OR)

```yaml
Control_Object:
  id: "CO-HVAC-AHU-OR-001"
  name: "1#手术室空调箱控制对象"
  target_node_ref: "HVAC-AHU_SNK_AHU_OR_01"
  equipment_ref: "EQP-AHU-CLEAN"
  space_ref: "OR-001"  # Agent-02手术室空间
  criticality: "P0-LIFE_SAFETY"
  
  # 引用Agent-02环境需求
  environmental_requirements_ref:
    source: "Agent-02.Medical_Special_Space_Models.ROOM-OR"
    parameters:
      temperature: {setpoint_range: [22, 25], precision: "±1°C"}
      humidity: {setpoint_range: [40, 60], precision: "±5%RH"}
      pressure: {min_value: "+8Pa", gradient: true}
      air_change: {variant: "ROOM-OR-I", value: "36 ACH"}
  
  io_points:
    analog_inputs:
      # 送风侧
      - id: "AI_SA_TEMP"
        name: "送风温度"
        signal: "4-20mA"
        range: "10-40°C"
        unit: "°C"
        location: "HEPA前2m"
        critical: true
        
      - id: "AI_SA_HUMID"
        name: "送风湿度"
        signal: "4-20mA"
        range: "20-95%RH"
        unit: "%RH"
        
      - id: "AI_SA_FLOW"
        name: "送风量"
        signal: "4-20mA"
        range: "0-15000m³/h"
        unit: "m³/h"
        sensor_type: "皮托管阵列"
        
      # 回风侧
      - id: "AI_RA_TEMP"
        name: "回风温度"
        signal: "4-20mA"
        range: "15-35°C"
        unit: "°C"
        
      - id: "AI_RA_HUMID"
        name: "回风湿度"
        signal: "4-20mA"
        range: "20-80%RH"
        unit: "%RH"
        
      # 新风侧
      - id: "AI_OA_TEMP"
        name: "新风温度"
        signal: "4-20mA"
        range: "-20-45°C"
        unit: "°C"
        
      - id: "AI_OA_HUMID"
        name: "新风湿度"
        signal: "4-20mA"
        range: "10-100%RH"
        unit: "%RH"
        
      # 混风/表冷
      - id: "AI_MA_TEMP"
        name: "混风温度"
        signal: "4-20mA"
        range: "0-40°C"
        unit: "°C"
        critical: true  # 防冻保护关键点
        
      - id: "AI_COIL_TEMP"
        name: "表冷器后温度"
        signal: "4-20mA"
        range: "5-35°C"
        unit: "°C"
        
      # 过滤器
      - id: "AI_PREFILTER_DP"
        name: "初效过滤器压差"
        signal: "4-20mA"
        range: "0-500Pa"
        unit: "Pa"
        alarm: {warning: 200, critical: 350}
        
      - id: "AI_MEDFILTER_DP"
        name: "中效过滤器压差"
        signal: "4-20mA"
        range: "0-500Pa"
        unit: "Pa"
        alarm: {warning: 250, critical: 400}
        
      - id: "AI_HEPAFILTER_DP"
        name: "高效过滤器压差"
        signal: "4-20mA"
        range: "0-600Pa"
        unit: "Pa"
        alarm: {warning: 300, critical: 450}
        
      # 风机
      - id: "AI_SF_CURRENT"
        name: "送风机电流"
        signal: "4-20mA"
        range: "0-100A"
        unit: "A"
        
      - id: "AI_SF_FREQ"
        name: "送风机频率"
        signal: "4-20mA"
        range: "0-50Hz"
        unit: "Hz"
        
      - id: "AI_RF_CURRENT"
        name: "排风机电流"
        signal: "4-20mA"
        range: "0-50A"
        unit: "A"
        
      - id: "AI_RF_FREQ"
        name: "排风机频率"
        signal: "4-20mA"
        range: "0-50Hz"
        unit: "Hz"
        
      # 阀位反馈
      - id: "AI_CHW_VALVE_FB"
        name: "冷水阀位反馈"
        signal: "4-20mA"
        range: "0-100%"
        unit: "%"
        
      - id: "AI_HW_VALVE_FB"
        name: "热水阀位反馈"
        signal: "4-20mA"
        range: "0-100%"
        unit: "%"
        
      - id: "AI_OA_DAMPER_FB"
        name: "新风阀位反馈"
        signal: "4-20mA"
        range: "0-100%"
        unit: "%"
    
    digital_inputs:
      - id: "DI_SF_RUN"
        name: "送风机运行"
        contact: "NO"
        
      - id: "DI_SF_FAULT"
        name: "送风机故障"
        contact: "NC"
        
      - id: "DI_RF_RUN"
        name: "排风机运行"
        contact: "NO"
        
      - id: "DI_RF_FAULT"
        name: "排风机故障"
        contact: "NC"
        
      - id: "DI_FREEZE_STAT"
        name: "防冻开关"
        contact: "NC"
        description: "温度<5°C时断开"
        
      - id: "DI_SMOKE_DETECTOR"
        name: "风管烟感"
        contact: "NO"
        
      - id: "DI_FIRE_DAMPER"
        name: "防火阀状态"
        contact: "NC"
        description: "关闭时断开"
        
      - id: "DI_LOCAL_REMOTE"
        name: "本地/远程"
        contact: "NO"
        
      - id: "DI_HUMIDIFIER_RUN"
        name: "加湿器运行"
        contact: "NO"
        
      - id: "DI_HUMIDIFIER_FAULT"
        name: "加湿器故障"
        contact: "NC"
    
    analog_outputs:
      - id: "AO_CHW_VALVE"
        name: "冷水阀控制"
        signal: "4-20mA"
        range: "0-100%"
        unit: "%"
        fail_position: "CLOSE"
        
      - id: "AO_HW_VALVE"
        name: "热水阀控制"
        signal: "4-20mA"
        range: "0-100%"
        unit: "%"
        fail_position: "OPEN"  # 防冻
        
      - id: "AO_OA_DAMPER"
        name: "新风阀控制"
        signal: "4-20mA"
        range: "0-100%"
        unit: "%"
        fail_position: "CLOSE"
        
      - id: "AO_RA_DAMPER"
        name: "回风阀控制"
        signal: "4-20mA"
        range: "0-100%"
        unit: "%"
        
      - id: "AO_SF_SPEED"
        name: "送风机转速"
        signal: "4-20mA"
        range: "0-50Hz"
        unit: "Hz"
        
      - id: "AO_RF_SPEED"
        name: "排风机转速"
        signal: "4-20mA"
        range: "0-50Hz"
        unit: "Hz"
        
      - id: "AO_HUMIDIFIER"
        name: "加湿器控制"
        signal: "4-20mA"
        range: "0-100%"
        unit: "%"
    
    digital_outputs:
      - id: "DO_SF_START"
        name: "送风机启动"
        contact: "NO"
        
      - id: "DO_SF_STOP"
        name: "送风机停止"
        contact: "NO"
        
      - id: "DO_RF_START"
        name: "排风机启动"
        contact: "NO"
        
      - id: "DO_RF_STOP"
        name: "排风机停止"
        contact: "NO"
        
      - id: "DO_HUMIDIFIER_EN"
        name: "加湿器使能"
        contact: "NO"
        
      - id: "DO_UV_LAMP"
        name: "紫外灯控制"
        contact: "NO"
        
  # Agent-04物理方程引用
  physics_model:
    equation_ref: "EQ-HX-COIL-001"
    formula: |
      # 表冷器换热方程
      Q = K × A × LMTD
      where:
        LMTD = (ΔT1 - ΔT2) / ln(ΔT1/ΔT2)
        ΔT1 = T_air_in - T_water_out
        ΔT2 = T_air_out - T_water_in
    virtual_sensors:
      - id: "VS_COIL_LOAD"
        name: "表冷器负荷估算"
        calculation: "ρ_air × V × Cp × (T_MA - T_COIL_OUT)"
        usage: "前馈控制阀门开度"
```

### 1.1.4 手术室室内环境传感器

```yaml
Control_Object:
  id: "CO-HVAC-ROOM-OR-001"
  name: "1#手术室室内环境控制对象"
  target_node_ref: "MED-OR_SNK_OR_001"
  equipment_ref: "ROOM_SENSORS"
  space_ref: "OR-001"
  criticality: "P0-LIFE_SAFETY"
  
  io_points:
    analog_inputs:
      # 室内温度 - 双传感器冗余
      - id: "AI_ROOM_TEMP_A"
        name: "室温传感器A"
        signal: "4-20mA"
        range: "15-35°C"
        unit: "°C"
        sensor_type: "PT1000"
        accuracy: "±0.3°C"
        location: "墙面1.5m高，非手术区"
        redundancy: "PRIMARY"
        
      - id: "AI_ROOM_TEMP_B"
        name: "室温传感器B"
        signal: "4-20mA"
        range: "15-35°C"
        unit: "°C"
        sensor_type: "PT1000"
        accuracy: "±0.3°C"
        location: "墙面1.5m高，对角位置"
        redundancy: "BACKUP"
        
      # 室内湿度
      - id: "AI_ROOM_HUMID"
        name: "室内湿度"
        signal: "4-20mA"
        range: "20-80%RH"
        unit: "%RH"
        sensor_type: "电容式"
        accuracy: "±2%RH"
        
      # 室内压差 - 双传感器冗余
      - id: "AI_ROOM_PRESS_A"
        name: "压差传感器A"
        signal: "4-20mA"
        range: "-50 to +100Pa"
        unit: "Pa"
        reference: "洁净走廊"
        accuracy: "±1Pa"
        redundancy: "PRIMARY"
        critical: true
        
      - id: "AI_ROOM_PRESS_B"
        name: "压差传感器B"
        signal: "4-20mA"
        range: "-50 to +100Pa"
        unit: "Pa"
        reference: "洁净走廊"
        accuracy: "±1Pa"
        redundancy: "BACKUP"
        
      # CO2浓度（可选）
      - id: "AI_CO2"
        name: "CO2浓度"
        signal: "4-20mA"
        range: "0-2000ppm"
        unit: "ppm"
        optional: true
        
    digital_inputs:
      # 门状态
      - id: "DI_DOOR_MAIN"
        name: "主门状态"
        contact: "NO"
        description: "门开时闭合"
        
      - id: "DI_DOOR_EQUIP"
        name: "器械门状态"
        contact: "NO"
        
      # 人体感应
      - id: "DI_OCCUPANCY"
        name: "人员在场"
        contact: "NO"
        description: "红外感应"
        
      # 层流状态
      - id: "DI_LAMINAR_OK"
        name: "层流正常"
        contact: "NO"
        
    # 本地显示屏
    local_display:
      - id: "DISP_DOOR"
        name: "门口压差显示器"
        type: "LED数码管"
        displays: ["压差Pa", "温度°C"]
        
  # 传感器选择与故障处理
  sensor_selection_logic:
    temperature:
      primary: "AI_ROOM_TEMP_A"
      backup: "AI_ROOM_TEMP_B"
      deviation_check: "|A - B| < 2°C"
      fault_action: "Switch to backup, alarm"
      
    pressure:
      primary: "AI_ROOM_PRESS_A"
      backup: "AI_ROOM_PRESS_B"
      deviation_check: "|A - B| < 3Pa"
      fault_action: "Switch to backup, CRITICAL alarm"
```

### 1.1.5 洁净走廊压差控制（关键辅助空间）

```yaml
# Agent-05特别提到的关键辅助空间
Control_Object:
  id: "CO-HVAC-ROOM-CORRIDOR-OR-001"
  name: "手术部洁净走廊压差控制对象"
  target_node_ref: "MED-OR_DST_CORRIDOR_CLEAN"
  equipment_ref: "CORRIDOR_SENSORS"
  space_ref: "CORRIDOR-OR-001"  # Agent-02走廊空间
  criticality: "P0-LIFE_SAFETY"
  note: "压差梯度的中间环节，直接影响手术室洁净度"
  
  # 压差梯度定义 (Agent-02)
  pressure_gradient:
    reference: "Agent-02.pressure.gradient"
    sequence:
      - space: "OR-001 (手术室)"
        pressure: "+15Pa"
        relative_to: "CORRIDOR-OR-001"
      - space: "CORRIDOR-OR-001 (洁净走廊)"
        pressure: "+8Pa"
        relative_to: "CORRIDOR-OR-002"
      - space: "CORRIDOR-OR-002 (清洁走廊)"
        pressure: "+3Pa"
        relative_to: "LOBBY"
      - space: "LOBBY (换车间)"
        pressure: "0Pa"
        relative_to: "OUTSIDE"
  
  io_points:
    analog_inputs:
      - id: "AI_CORRIDOR_PRESS_VS_CLEAN"
        name: "洁净走廊对清洁走廊压差"
        signal: "4-20mA"
        range: "-30 to +50Pa"
        unit: "Pa"
        setpoint: "+5Pa"
        
      - id: "AI_CORRIDOR_PRESS_VS_OR"
        name: "洁净走廊对手术室压差"
        signal: "4-20mA"
        range: "-50 to +30Pa"
        unit: "Pa"
        note: "应为负值（手术室压力更高）"
        
      - id: "AI_CORRIDOR_TEMP"
        name: "走廊温度"
        signal: "4-20mA"
        range: "15-30°C"
        unit: "°C"
        
    digital_inputs:
      - id: "DI_FIRE_DOOR_1"
        name: "防火门1状态"
        contact: "NC"
        
      - id: "DI_FIRE_DOOR_2"
        name: "防火门2状态"
        contact: "NC"
```

---

## 1.2 ELEC 电气系统控制对象

### 1.2.1 医用隔离变压器 (EQP-ISO-TRANS)

```yaml
# Agent-05特别提到的特殊设备
Control_Object:
  id: "CO-ELEC-IPS-OR-001"
  name: "1#手术室医用隔离电源系统"
  target_node_ref: "ELEC-LV_DST_IPS_OR_01"
  equipment_ref: "EQP-ISO-TRANS"
  space_ref: "OR-001"
  criticality: "P0-LIFE_SAFETY"
  
  description: |
    医用隔离电源系统(IT系统)，用于手术室、ICU等生命安全区域。
    当发生单相接地故障时，系统不立即断电，而是发出报警，
    允许手术继续进行，避免突然断电造成的医疗事故。
  
  io_points:
    analog_inputs:
      - id: "AI_INPUT_VOLTAGE"
        name: "输入电压"
        signal: "4-20mA"
        range: "0-500V"
        unit: "V"
        phases: "L1-L2-L3"
        
      - id: "AI_OUTPUT_VOLTAGE"
        name: "输出电压"
        signal: "4-20mA"
        range: "0-250V"
        unit: "V"
        
      - id: "AI_LOAD_CURRENT"
        name: "负载电流"
        signal: "4-20mA"
        range: "0-50A"
        unit: "A"
        
      - id: "AI_TRANSFORMER_TEMP"
        name: "变压器温度"
        signal: "4-20mA"
        range: "0-150°C"
        unit: "°C"
        alarm: {warning: 100, critical: 130}
        
      - id: "AI_INSULATION_RESIST"
        name: "对地绝缘电阻"
        signal: "4-20mA"
        range: "0-1000kΩ"
        unit: "kΩ"
        alarm: {warning: 100, critical: 50}
        description: "绝缘监测仪测量值"
        
      - id: "AI_FAULT_CURRENT"
        name: "对地故障电流"
        signal: "4-20mA"
        range: "0-10mA"
        unit: "mA"
        alarm: {critical: 5}
        
    digital_inputs:
      - id: "DI_INSULATION_ALARM"
        name: "绝缘故障报警"
        contact: "NO"
        severity: "CRITICAL"
        description: "绝缘电阻<50kΩ时报警"
        
      - id: "DI_OVERLOAD"
        name: "过负荷报警"
        contact: "NO"
        
      - id: "DI_OVER_TEMP"
        name: "超温报警"
        contact: "NO"
        
      - id: "DI_INPUT_OK"
        name: "输入电源正常"
        contact: "NO"
        
      - id: "DI_OUTPUT_OK"
        name: "输出电源正常"
        contact: "NO"
        
      - id: "DI_TEST_BUTTON"
        name: "测试按钮"
        contact: "NO"
        description: "定期测试绝缘监测功能"
        
    digital_outputs:
      - id: "DO_ALARM_RESET"
        name: "报警复位"
        contact: "NO"
        pulse: true
        
      - id: "DO_ALARM_MUTE"
        name: "报警消音"
        contact: "NO"
        
  # 报警处理策略
  alarm_strategy:
    insulation_fault:
      trigger: "AI_INSULATION_RESIST < 50kΩ"
      action:
        - "发出声光报警（手术室内+护士站）"
        - "记录故障发生时间"
        - "通知电气维护人员"
        - "NOT自动断电（允许手术继续）"
      note: |
        IT系统的核心特性：单相接地故障时不立即断电，
        但必须在手术结束后立即排查故障。
        
  # 与Agent-02空间的关联
  served_spaces:
    - space_id: "OR-001"
      circuits:
        - "无影灯"
        - "电刀"
        - "麻醉机"
        - "监护设备"
```

### 1.2.2 低压配电柜监测

```yaml
Control_Object:
  id: "CO-ELEC-LV-PANEL-001"
  name: "1#低压总配电柜监测"
  target_node_ref: "ELEC-LV_SRC_MDB_1"
  equipment_ref: "EQP-SWGR-LV"
  space_ref: "BL-MAIN-B1-ELEC01"
  criticality: "P1-MISSION_CRITICAL"
  
  io_points:
    analog_inputs:
      # 三相电压
      - id: "AI_VOLTAGE_L1"
        name: "L1相电压"
        signal: "Modbus RTU"
        range: "0-500V"
        unit: "V"
        
      - id: "AI_VOLTAGE_L2"
        name: "L2相电压"
        signal: "Modbus RTU"
        range: "0-500V"
        unit: "V"
        
      - id: "AI_VOLTAGE_L3"
        name: "L3相电压"
        signal: "Modbus RTU"
        range: "0-500V"
        unit: "V"
        
      # 三相电流
      - id: "AI_CURRENT_L1"
        name: "L1相电流"
        signal: "Modbus RTU"
        range: "0-2000A"
        unit: "A"
        
      - id: "AI_CURRENT_L2"
        name: "L2相电流"
        signal: "Modbus RTU"
        range: "0-2000A"
        unit: "A"
        
      - id: "AI_CURRENT_L3"
        name: "L3相电流"
        signal: "Modbus RTU"
        range: "0-2000A"
        unit: "A"
        
      # 功率参数
      - id: "AI_ACTIVE_POWER"
        name: "有功功率"
        signal: "Modbus RTU"
        range: "0-2000kW"
        unit: "kW"
        
      - id: "AI_REACTIVE_POWER"
        name: "无功功率"
        signal: "Modbus RTU"
        range: "0-2000kVar"
        unit: "kVar"
        
      - id: "AI_POWER_FACTOR"
        name: "功率因数"
        signal: "Modbus RTU"
        range: "0-1.0"
        unit: "-"
        
      - id: "AI_FREQUENCY"
        name: "频率"
        signal: "Modbus RTU"
        range: "45-55Hz"
        unit: "Hz"
        
      - id: "AI_ENERGY"
        name: "累计电量"
        signal: "Modbus RTU"
        range: "0-999999kWh"
        unit: "kWh"
        
    digital_inputs:
      - id: "DI_MAIN_BREAKER"
        name: "主开关状态"
        contact: "NO"
        
      - id: "DI_ATS_POSITION"
        name: "ATS位置"
        contact: "NO"
        description: "市电/发电机"
        
      - id: "DI_DOOR_STATUS"
        name: "柜门状态"
        contact: "NC"
        
      - id: "DI_TEMP_ALARM"
        name: "温度报警"
        contact: "NO"
        
    # 通信接口
    communication:
      protocol: "Modbus RTU"
      baud_rate: 9600
      parity: "Even"
      slave_id: 1
      poll_interval: "1s"
```

### 1.2.3 柴油发电机组

```yaml
Control_Object:
  id: "CO-ELEC-EPS-GEN-001"
  name: "1#柴油发电机组"
  target_node_ref: "ELEC-EPS_SRC_GEN_1"
  equipment_ref: "EQP-GENERATOR-DIESEL"
  space_ref: "BL-MAIN-B1-GEN01"
  criticality: "P0-LIFE_SAFETY"
  
  io_points:
    analog_inputs:
      # 发电机参数
      - id: "AI_OUTPUT_VOLTAGE"
        name: "输出电压"
        signal: "4-20mA"
        range: "0-500V"
        unit: "V"
        
      - id: "AI_OUTPUT_CURRENT"
        name: "输出电流"
        signal: "4-20mA"
        range: "0-3000A"
        unit: "A"
        
      - id: "AI_OUTPUT_POWER"
        name: "输出功率"
        signal: "4-20mA"
        range: "0-2000kW"
        unit: "kW"
        
      - id: "AI_FREQUENCY"
        name: "频率"
        signal: "4-20mA"
        range: "45-55Hz"
        unit: "Hz"
        
      # 发动机参数
      - id: "AI_ENGINE_SPEED"
        name: "发动机转速"
        signal: "4-20mA"
        range: "0-2000rpm"
        unit: "rpm"
        
      - id: "AI_ENGINE_TEMP"
        name: "发动机水温"
        signal: "4-20mA"
        range: "0-120°C"
        unit: "°C"
        alarm: {warning: 95, critical: 105}
        
      - id: "AI_OIL_PRESSURE"
        name: "机油压力"
        signal: "4-20mA"
        range: "0-1.0MPa"
        unit: "MPa"
        alarm: {warning: 0.2, critical: 0.1}
        
      - id: "AI_OIL_TEMP"
        name: "机油温度"
        signal: "4-20mA"
        range: "0-120°C"
        unit: "°C"
        
      - id: "AI_FUEL_LEVEL"
        name: "燃油液位"
        signal: "4-20mA"
        range: "0-100%"
        unit: "%"
        alarm: {warning: 30, critical: 15}
        
      - id: "AI_BATTERY_VOLTAGE"
        name: "启动电池电压"
        signal: "4-20mA"
        range: "0-30V"
        unit: "V"
        alarm: {warning: 23, critical: 21}
        
    digital_inputs:
      - id: "DI_RUN_STATUS"
        name: "运行状态"
        contact: "NO"
        
      - id: "DI_READY"
        name: "就绪状态"
        contact: "NO"
        
      - id: "DI_FAULT"
        name: "故障状态"
        contact: "NC"
        
      - id: "DI_AUTO_MODE"
        name: "自动模式"
        contact: "NO"
        
      - id: "DI_ON_LOAD"
        name: "带载状态"
        contact: "NO"
        
      - id: "DI_OVERSPEED"
        name: "超速保护"
        contact: "NC"
        
      - id: "DI_LOW_OIL_PRESS"
        name: "低油压保护"
        contact: "NC"
        
      - id: "DI_HIGH_WATER_TEMP"
        name: "高水温保护"
        contact: "NC"
        
      - id: "DI_CHARGER_FAULT"
        name: "充电机故障"
        contact: "NC"
        
    digital_outputs:
      - id: "DO_START"
        name: "启动指令"
        contact: "NO"
        
      - id: "DO_STOP"
        name: "停机指令"
        contact: "NO"
        
      - id: "DO_RESET"
        name: "故障复位"
        contact: "NO"
        pulse: true
        
      - id: "DO_TEST_RUN"
        name: "测试运行"
        contact: "NO"
        description: "每周定期测试"
        
  # 启动顺序 (基于Agent-01依赖关系)
  startup_sequence:
    trigger: "市电失电 AND DI_READY = TRUE"
    sequence:
      - step: 1
        action: "接收市电失电信号"
        delay: "0s"
      - step: 2
        action: "发电机启动"
        timeout: "10s"
        verify: "DI_RUN_STATUS = TRUE AND AI_FREQUENCY > 48Hz"
      - step: 3
        action: "ATS切换至发电机"
        delay: "3s"
        verify: "DI_ON_LOAD = TRUE"
      - step: 4
        action: "顺序合闸负载"
        note: "按优先级顺序恢复供电"
```

---

## 1.3 MGAS 医用气体系统控制对象

### 1.3.1 医用氧气区域阀门箱

```yaml
Control_Object:
  id: "CO-MGAS-O2-ZV-OR001"
  name: "手术部氧气区域阀门箱"
  target_node_ref: "MGAS-O2_DST_ZONE_VALVE_3F_OR"
  equipment_ref: "EQP-ZONE-VALVE-BOX"
  space_ref: "ZONE-OR-3F"  # Agent-02 3楼手术区
  criticality: "P0-LIFE_SAFETY"
  
  io_points:
    analog_inputs:
      - id: "AI_PRESS"
        name: "区域压力"
        signal: "4-20mA"
        range: "0-1.0MPa"
        unit: "MPa"
        setpoint: "0.4MPa"
        alarm:
          low_warning: 0.35
          low_critical: 0.30
          high_warning: 0.50
          high_critical: 0.55
        scan_rate: "1s"
        critical: true
        
      - id: "AI_FLOW"
        name: "区域流量"
        signal: "4-20mA"
        range: "0-500L/min"
        unit: "L/min"
        sensor_type: "热式质量流量计"
        optional: true
        
    digital_inputs:
      - id: "DI_ALARM_H"
        name: "高压报警"
        contact: "NC"
        trigger: "压力>0.55MPa"
        severity: "HIGH"
        
      - id: "DI_ALARM_L"
        name: "低压报警"
        contact: "NC"
        trigger: "压力<0.30MPa"
        severity: "CRITICAL"
        
      - id: "DI_VALVE_OPEN"
        name: "阀门开启状态"
        contact: "NO"
        
      - id: "DI_VALVE_CLOSE"
        name: "阀门关闭状态"
        contact: "NO"
        
    digital_outputs:
      - id: "DO_EMERG_CUT"
        name: "紧急切断"
        contact: "NO"
        action: "Close valve"
        requires_auth: true
        description: "需授权操作，用于紧急情况"
        interlock:
          fire_mode: "ALARM_ONLY"  # 火灾时仅报警，不自动切断
          manual_only: true
          
  # 报警策略 (基于Agent-05建议)
  alarm_strategy:
    fire_response:
      action: "ALARM_ONLY"
      rationale: "手术中患者可能依赖氧气，不能自动切断"
      notification:
        - "护士站声光报警"
        - "气体监控室报警"
        - "手术室内显示屏提示"
      decision: "由医护人员判断是否切断"
```

### 1.3.2 医用负压吸引系统

```yaml
Control_Object:
  id: "CO-MGAS-VAC-PUMP-001"
  name: "1#真空泵组"
  target_node_ref: "MGAS-VAC_SRC_PUMP_1"
  equipment_ref: "EQP-VAC-PUMP"
  space_ref: "BL-MAIN-B1-GAS01"
  criticality: "P0-LIFE_SAFETY"
  
  io_points:
    analog_inputs:
      - id: "AI_VACUUM_LEVEL"
        name: "真空度"
        signal: "4-20mA"
        range: "0 to -0.1MPa"
        unit: "MPa"
        setpoint: "-0.04MPa"
        
      - id: "AI_MOTOR_CURRENT"
        name: "电机电流"
        signal: "4-20mA"
        range: "0-100A"
        unit: "A"
        
      - id: "AI_EXHAUST_TEMP"
        name: "排气温度"
        signal: "4-20mA"
        range: "0-100°C"
        unit: "°C"
        
      - id: "AI_OIL_LEVEL"
        name: "油位"
        signal: "4-20mA"
        range: "0-100%"
        unit: "%"
        
    digital_inputs:
      - id: "DI_RUN_STATUS"
        name: "运行状态"
        contact: "NO"
        
      - id: "DI_FAULT"
        name: "故障状态"
        contact: "NC"
        
      - id: "DI_OVERLOAD"
        name: "过载保护"
        contact: "NC"
        
      - id: "DI_OIL_LEVEL_LOW"
        name: "油位低"
        contact: "NC"
        
      - id: "DI_FILTER_DP_HIGH"
        name: "过滤器堵塞"
        contact: "NC"
        
    digital_outputs:
      - id: "DO_START"
        name: "启动指令"
        contact: "NO"
        
      - id: "DO_STOP"
        name: "停止指令"
        contact: "NO"
        
  # 群控逻辑
  group_control:
    pumps: ["VAC-PUMP-001", "VAC-PUMP-002", "VAC-PUMP-003"]
    configuration: "N+1"
    lead_lag_rotation: "Weekly"
    add_pump_threshold: "-0.03MPa"  # 真空度不足
    remove_pump_threshold: "-0.05MPa"  # 真空度过高
    staging_delay: "30s"
```

### 1.3.3 医用压缩空气系统

```yaml
Control_Object:
  id: "CO-MGAS-AIR-COMP-001"
  name: "1#医用空压机组"
  target_node_ref: "MGAS-AIR_SRC_COMP_1"
  equipment_ref: "EQP-COMP-OIL-FREE"
  space_ref: "BL-MAIN-B1-GAS01"
  criticality: "P0-LIFE_SAFETY"
  
  io_points:
    analog_inputs:
      - id: "AI_OUTLET_PRESS"
        name: "出口压力"
        signal: "4-20mA"
        range: "0-1.0MPa"
        unit: "MPa"
        setpoint: "0.8MPa"
        
      - id: "AI_DRYPOINT"
        name: "露点温度"
        signal: "4-20mA"
        range: "-60 to +20°C"
        unit: "°C"
        alarm: {critical: -20}  # 露点高于-20°C报警
        
      - id: "AI_OIL_CONTENT"
        name: "残油量"
        signal: "4-20mA"
        range: "0-1mg/m³"
        unit: "mg/m³"
        alarm: {critical: 0.01}
        
      - id: "AI_MOTOR_CURRENT"
        name: "电机电流"
        signal: "4-20mA"
        range: "0-200A"
        unit: "A"
        
      - id: "AI_EXHAUST_TEMP"
        name: "排气温度"
        signal: "4-20mA"
        range: "0-120°C"
        unit: "°C"
        
    digital_inputs:
      - id: "DI_RUN_STATUS"
        name: "运行状态"
        contact: "NO"
        
      - id: "DI_FAULT"
        name: "故障状态"
        contact: "NC"
        
      - id: "DI_DRYER_RUN"
        name: "干燥机运行"
        contact: "NO"
        
      - id: "DI_DRYER_FAULT"
        name: "干燥机故障"
        contact: "NC"
        
      - id: "DI_FILTER_DP"
        name: "过滤器压差高"
        contact: "NC"
        
    digital_outputs:
      - id: "DO_START"
        name: "启动指令"
        contact: "NO"
        
      - id: "DO_STOP"
        name: "停止指令"
        contact: "NO"
        
      - id: "DO_UNLOAD"
        name: "卸载指令"
        contact: "NO"
```

---

## 1.4 FIRE 消防系统控制对象

### 1.4.1 消防水泵控制

```yaml
Control_Object:
  id: "CO-FIRE-SPS-PUMP-001"
  name: "1#消火栓泵"
  target_node_ref: "FIRE-SPS_SRC_PUMP_1"
  equipment_ref: "EQP-PUMP-FIRE"
  space_ref: "BL-MAIN-B1-FIRE01"
  criticality: "P0-LIFE_SAFETY"
  control_authority: "FAS优先"
  
  io_points:
    analog_inputs:
      - id: "AI_OUTLET_PRESS"
        name: "出口压力"
        signal: "4-20mA"
        range: "0-1.6MPa"
        unit: "MPa"
        
      - id: "AI_MOTOR_CURRENT"
        name: "电机电流"
        signal: "4-20mA"
        range: "0-300A"
        unit: "A"
        
    digital_inputs:
      - id: "DI_RUN_STATUS"
        name: "运行状态"
        contact: "NO"
        
      - id: "DI_FAULT"
        name: "故障状态"
        contact: "NC"
        
      - id: "DI_AUTO_MODE"
        name: "自动模式"
        contact: "NO"
        
      - id: "DI_MANUAL_START"
        name: "手动启动"
        contact: "NO"
        description: "消防控制室手动按钮"
        
      - id: "DI_PRESSURE_SW"
        name: "压力开关"
        contact: "NO"
        description: "管网压力低时动作"
        
      - id: "DI_FLOW_SW"
        name: "流量开关"
        contact: "NO"
        description: "水流指示器动作"
        
    digital_outputs:
      - id: "DO_START"
        name: "启动指令"
        contact: "NO"
        source: "FAS硬接点"
        
      - id: "DO_STOP"
        name: "停止指令"
        contact: "NO"
        restriction: "仅手动停止，不能远程自动停止"
        
  # 消防联动 (基于Agent-01 FIRE-FAS联动逻辑)
  fire_interlock:
    start_conditions:
      - "报警阀压力开关动作"
      - "消火栓按钮动作"
      - "消防控制室手动启动"
    start_mode: "硬接点联动"
    stop_restriction: "只能现场手动停止或消防控制室操作"
    feedback_to_fas: true
```

### 1.4.2 排烟风机控制

```yaml
Control_Object:
  id: "CO-FIRE-EXH-SEF-001"
  name: "1#排烟风机"
  target_node_ref: "FIRE-EXH_SRC_SEF_1"
  equipment_ref: "EQP-FAN-SMOKE"
  space_ref: "BL-MAIN-RF-FIRE01"
  criticality: "P0-LIFE_SAFETY"
  control_authority: "FAS优先"
  
  io_points:
    analog_inputs:
      - id: "AI_MOTOR_CURRENT"
        name: "电机电流"
        signal: "4-20mA"
        range: "0-100A"
        unit: "A"
        
      - id: "AI_MOTOR_TEMP"
        name: "电机温度"
        signal: "4-20mA"
        range: "0-200°C"
        unit: "°C"
        note: "280°C耐高温电机"
        
    digital_inputs:
      - id: "DI_RUN_STATUS"
        name: "运行状态"
        contact: "NO"
        
      - id: "DI_FAULT"
        name: "故障状态"
        contact: "NC"
        
      - id: "DI_DAMPER_OPEN"
        name: "排烟阀开启"
        contact: "NO"
        description: "所有关联排烟阀状态"
        
    digital_outputs:
      - id: "DO_START"
        name: "启动指令"
        contact: "NO"
        source: "FAS硬接点"
        
      - id: "DO_STOP"
        name: "停止指令"
        contact: "NO"
        
  # 联动逻辑
  fire_interlock:
    start_sequence:
      - step: 1
        trigger: "火灾确认 AND 该区域排烟"
        action: "打开排烟阀"
      - step: 2
        condition: "DI_DAMPER_OPEN = TRUE"
        action: "启动排烟风机"
        delay: "10s"
    280c_fusible:
      description: "排烟阀280°C熔断自动关闭"
      action: "风机继续运行，但该支路关闭"
```

### 1.4.3 防火阀控制

```yaml
Control_Object:
  id: "CO-FIRE-EXH-FD-001"
  name: "防火阀（穿越防火分区）"
  target_node_ref: "FIRE-EXH_DST_FD_01"
  equipment_ref: "EQP-DAMPER-FIRE"
  space_ref: "FIRE-COMPARTMENT-A"
  criticality: "P0-LIFE_SAFETY"
  
  io_points:
    digital_inputs:
      - id: "DI_OPEN_STATUS"
        name: "开启状态"
        contact: "NO"
        
      - id: "DI_CLOSE_STATUS"
        name: "关闭状态"
        contact: "NO"
        
      - id: "DI_FUSIBLE_OK"
        name: "熔断器正常"
        contact: "NC"
        description: "70°C熔断"
        
    digital_outputs:
      - id: "DO_CLOSE"
        name: "关闭指令"
        contact: "NO"
        source: "FAS硬接点"
        
      - id: "DO_RESET"
        name: "复位指令"
        contact: "NO"
        manual_only: true
        
  # 失效安全
  fail_safe:
    mechanism: "弹簧复位"
    trigger: "70°C熔断 OR 电磁释放"
    position: "CLOSE"
    override: "不可软件覆盖"
```

---

## 1.5 PLUMB 给排水系统控制对象

### 1.5.1 生活给水变频泵组

```yaml
Control_Object:
  id: "CO-PLUMB-DWS-PUMP-001"
  name: "生活给水变频泵组"
  target_node_ref: "PLUMB-DWS_SRC_PUMP_1"
  equipment_ref: "EQP-PUMP-DWS-VFD"
  space_ref: "BL-MAIN-B1-PUMP01"
  criticality: "P2-IMPORTANT"
  
  io_points:
    analog_inputs:
      - id: "AI_OUTLET_PRESS"
        name: "出口压力"
        signal: "4-20mA"
        range: "0-1.0MPa"
        unit: "MPa"
        setpoint: "0.45MPa"
        
      - id: "AI_TANK_LEVEL"
        name: "水箱液位"
        signal: "4-20mA"
        range: "0-100%"
        unit: "%"
        
      - id: "AI_VFD_FREQ"
        name: "变频器频率"
        signal: "4-20mA"
        range: "0-50Hz"
        unit: "Hz"
        
    digital_inputs:
      - id: "DI_PUMP1_RUN"
        name: "1#泵运行"
        contact: "NO"
        
      - id: "DI_PUMP1_FAULT"
        name: "1#泵故障"
        contact: "NC"
        
      - id: "DI_PUMP2_RUN"
        name: "2#泵运行"
        contact: "NO"
        
      - id: "DI_PUMP2_FAULT"
        name: "2#泵故障"
        contact: "NC"
        
      - id: "DI_PUMP3_RUN"
        name: "3#泵运行"
        contact: "NO"
        
      - id: "DI_LOW_LEVEL"
        name: "水箱低液位"
        contact: "NC"
        
      - id: "DI_HIGH_LEVEL"
        name: "水箱高液位"
        contact: "NO"
        
    analog_outputs:
      - id: "AO_VFD_SPEED"
        name: "变频器速度指令"
        signal: "4-20mA"
        range: "0-50Hz"
        unit: "Hz"
        
    digital_outputs:
      - id: "DO_PUMP1_START"
        name: "1#泵启动"
        contact: "NO"
        
      - id: "DO_PUMP2_START"
        name: "2#泵启动"
        contact: "NO"
        
      - id: "DO_PUMP3_START"
        name: "3#泵启动"
        contact: "NO"
        
  # 恒压供水控制
  control_strategy:
    type: "PID恒压控制"
    PV: "AI_OUTLET_PRESS"
    SP: "0.45MPa"
    output: "AO_VFD_SPEED"
    cascade_pumps: true
    add_pump: "频率>48Hz持续60s"
    remove_pump: "频率<25Hz持续120s"
```

### 1.5.2 生活热水循环泵

```yaml
Control_Object:
  id: "CO-PLUMB-HWS-PUMP-001"
  name: "生活热水循环泵"
  target_node_ref: "PLUMB-HWS_DST_CIRC_PUMP_1"
  equipment_ref: "EQP-PUMP-HWS-CIRC"
  space_ref: "BL-MAIN-B1-PUMP01"
  criticality: "P2-IMPORTANT"
  
  io_points:
    analog_inputs:
      - id: "AI_SUPPLY_TEMP"
        name: "供水温度"
        signal: "4-20mA"
        range: "0-80°C"
        unit: "°C"
        setpoint: "55°C"
        
      - id: "AI_RETURN_TEMP"
        name: "回水温度"
        signal: "4-20mA"
        range: "0-80°C"
        unit: "°C"
        
      - id: "AI_VFD_FREQ"
        name: "变频器频率"
        signal: "4-20mA"
        range: "0-50Hz"
        unit: "Hz"
        
    digital_inputs:
      - id: "DI_RUN_STATUS"
        name: "运行状态"
        contact: "NO"
        
      - id: "DI_FAULT"
        name: "故障状态"
        contact: "NC"
        
    analog_outputs:
      - id: "AO_VFD_SPEED"
        name: "变频器速度指令"
        signal: "4-20mA"
        range: "0-50Hz"
        unit: "Hz"
        
    digital_outputs:
      - id: "DO_START"
        name: "启动指令"
        contact: "NO"
        
      - id: "DO_STOP"
        name: "停止指令"
        contact: "NO"
        
  # 控制策略：回水温度控制
  control_strategy:
    type: "PID控制"
    objective: "保持回水温度≥50°C"
    PV: "AI_RETURN_TEMP"
    SP: "50°C"
    output: "AO_VFD_SPEED"
    action: "回水温度低→增加循环流量"
```

---

## 1.6 INT 智能化系统控制对象

### 1.6.1 楼宇自控系统DDC

```yaml
Control_Object:
  id: "CO-INT-BA-DDC-OR-001"
  name: "手术部DDC控制器"
  target_node_ref: "INT-BA_DST_DDC_OR_01"
  equipment_ref: "EQP-DDC-MAIN"
  space_ref: "BL-MAIN-3F-MEP01"
  criticality: "P1-MISSION_CRITICAL"
  
  specifications:
    manufacturer: "To be specified"
    model: "To be specified"
    io_capacity:
      AI: 32
      AO: 16
      DI: 32
      DO: 16
    communication:
      uplink: "BACnet/IP"
      downlink: "BACnet MS/TP"
    power: "24VDC"
    battery_backup: "72h RTC"
    operating_temp: "-10 to +50°C"
    
  # 管理的控制对象
  managed_objects:
    - "CO-HVAC-AHU-OR-001"
    - "CO-HVAC-AHU-OR-002"
    - "CO-HVAC-ROOM-OR-001"
    - "CO-HVAC-ROOM-OR-002"
    - "CO-HVAC-ROOM-CORRIDOR-OR-001"
    
  # 本地存储的默认参数 (断网时使用)
  local_defaults:
    OR_TEMP_SP: 22.0  # °C
    OR_HUMID_SP: 50   # %RH
    OR_PRESS_SP: 15   # Pa
    STANDBY_TEMP_SP: 26.0
    STANDBY_PRESS_SP: 8
    
  # 本地时间表
  local_schedule:
    weekday:
      surgery_prep: "07:00"
      surgery_end: "22:00"
    weekend:
      surgery_prep: "08:00"
      surgery_end: "18:00"
```

### 1.6.2 护士呼叫系统接口

```yaml
Control_Object:
  id: "CO-INT-NUR-PANEL-OR-001"
  name: "手术室护士呼叫面板"
  target_node_ref: "INT-NUR_SNK_PANEL_OR_01"
  equipment_ref: "EQP-NC-PANEL"
  space_ref: "OR-001"
  criticality: "P1-MISSION_CRITICAL"
  
  io_points:
    digital_inputs:
      - id: "DI_NURSE_CALL"
        name: "护士呼叫"
        contact: "NO"
        
      - id: "DI_EMERGENCY_CALL"
        name: "紧急呼叫"
        contact: "NO"
        
      - id: "DI_CANCEL"
        name: "取消呼叫"
        contact: "NO"
        
    digital_outputs:
      - id: "DO_CALL_INDICATOR"
        name: "呼叫指示灯"
        contact: "NO"
        
      - id: "DO_PRESENCE_INDICATOR"
        name: "医护在场指示"
        contact: "NO"
        
  # 与BMS集成接口
  bms_integration:
    protocol: "Modbus RTU"
    data_points:
      - "呼叫状态"
      - "呼叫时间"
      - "响应时间"
    usage: "统计分析、运维管理"
```

---

# 第二部分：控制逻辑与物理方程融合 / 场景化控制逻辑
## (Logic & Physics Integration / Scenario-Based Logic)

本部分基于Agent-05的耦合单元(CU)和Agent-02的场景模式，生成包含状态机的控制回路模型。

---

## 2.1 手术室环境控制状态机

```yaml
# ═══════════════════════════════════════════════════════════════════════════
# 控制状态机：手术室HVAC
# 基于 Agent-05 CU-OR001-HVAC_CLN-COOLING
#      Agent-02 Operational_Scenarios.OperatingRoom
# ═══════════════════════════════════════════════════════════════════════════

Control_State_Machine:
  id: "FSM-OR001-HVAC"
  name: "1#手术室环境控制状态机"
  target_cu: "CU-OR001-HVAC_CLN-COOLING"
  target_space_ref: "OR-001"
  controller_ref: "CO-INT-BA-DDC-OR-001"
  criticality: "P0-LIFE_SAFETY"
  
  # ─────────────────────────────────────────────────────────────────────────
  # 状态定义 (源自 Agent-02 Scenarios)
  # ─────────────────────────────────────────────────────────────────────────
  states:
    
    - id: "MODE_OFF"
      name: "关闭模式"
      description: "手术室完全关闭，仅用于长期停用"
      setpoints: null
      equipment_status:
        AHU: "OFF"
        Lights: "OFF"
        Medical_Gas: "ISOLATED"
      allowed_transitions: ["MODE_STANDBY"]
      
    - id: "MODE_STANDBY"
      name: "值班模式"
      description: "非手术时间，维持基本环境"
      setpoints:
        temperature:
          value: 26.0
          unit: "°C"
          tolerance: "±2°C"
          relaxed: true
        humidity:
          control: false  # 不控制湿度
        pressure:
          value: 8
          unit: "Pa"
          description: "维持最小正压"
        air_changes:
          value: 6
          unit: "ACH"
          description: "50%设计风量"
      equipment_status:
        AHU_SF: "30% speed"
        AHU_RF: "proportional"
        CHW_Valve: "AUTO"
        HW_Valve: "AUTO"
        Humidifier: "OFF"
      control_strategy: "Energy_Saving"
      energy_saving: "约40%节能"
      allowed_transitions: ["MODE_PREP", "MODE_DECON", "MODE_OFF"]
      
    - id: "MODE_PREP"
      name: "准备模式"
      description: "手术前预调节环境"
      trigger: "手术排程开始前30分钟 OR 手动启动"
      duration: "30分钟"
      setpoints:
        temperature:
          value: 22.0
          unit: "°C"
          tolerance: "±1°C"
        humidity:
          value: 50
          unit: "%RH"
          tolerance: "±5%RH"
        pressure:
          value: 15
          unit: "Pa"
        air_changes:
          value: 36
          unit: "ACH"
      equipment_status:
        AHU_SF: "100% speed"
        AHU_RF: "proportional"
        All_Valves: "AUTO"
        Humidifier: "AUTO"
      control_strategy: "Ramp_Up"
      allowed_transitions: ["MODE_SURGERY", "MODE_STANDBY"]
      
    - id: "MODE_SURGERY"
      name: "手术模式"
      description: "手术进行中，精确控制"
      setpoints:
        temperature:
          value: 22.0  # 可由手术室面板调节21-27°C
          unit: "°C"
          tolerance: "±1°C"
          adjustable_range: [21, 27]
          control_authority: "手术室面板"
        humidity:
          value: 50
          unit: "%RH"
          tolerance: "±5%RH"
          adjustable_range: [40, 60]
        pressure:
          value: 15
          unit: "Pa"
          tolerance: "±3Pa"
          critical: true
        air_changes:
          value: 36
          unit: "ACH"
          per_class:
            ROOM-OR-I: 36
            ROOM-OR-II: 24
            ROOM-OR-III: 20
      equipment_status:
        AHU_SF: "100% speed"
        AHU_RF: "pressure control"
        All_Controls: "Precision PID"
      control_strategy: "Precision_Control"
      monitoring:
        particle_count: "continuous"
        pressure_trend: "every 1s"
      allowed_transitions: ["MODE_DECON", "MODE_EMERGENCY"]
      
    - id: "MODE_DECON"
      name: "消毒模式"
      description: "手术后消毒排风"
      trigger: "手术结束信号"
      duration: "30-60分钟（可配置）"
      phases:
        - phase: 1
          name: "自净阶段"
          duration: "20分钟"
          setpoints:
            fresh_air: "100%"
            exhaust: "正常"
          action: "全新风换气，稀释污染物"
        - phase: 2
          name: "消毒阶段"
          duration: "30分钟"
          setpoints:
            fresh_air: "0%"
            exhaust: "0%"
          equipment:
            UV_Lamp: "ON"
            Ozone: "ON (if equipped)"
          action: "封闭空间紫外/臭氧消毒"
        - phase: 3
          name: "排放阶段"
          duration: "10分钟"
          setpoints:
            fresh_air: "100%"
            exhaust: "100%"
          action: "排出臭氧/消毒气体"
      allowed_transitions: ["MODE_STANDBY", "MODE_PREP"]
      
    - id: "MODE_EMERGENCY"
      name: "应急模式"
      description: "紧急情况处理"
      trigger: "火灾信号 OR 医疗紧急 OR 设备故障"
      sub_modes:
        - id: "EMERG_FIRE"
          name: "火灾模式"
          trigger: "FIRE_SIGNAL from FAS"
          response:
            if_fire_in_zone:
              - "关闭AHU"
              - "关闭新风阀"
              - "关闭防火阀"
            if_fire_not_in_zone:
              - "维持正压"
              - "切换100%循环风"
              - "关闭新风阀"
              - "继续手术（由医生决定）"
        - id: "EMERG_SENSOR_FAIL"
          name: "传感器故障模式"
          trigger: "关键传感器故障"
          response:
            - "切换备用传感器"
            - "或使用默认设定值"
            - "报警通知"
        - id: "EMERG_POWER"
          name: "应急电源模式"
          trigger: "市电失电"
          response:
            - "切换UPS供电"
            - "柴发接管后恢复正常控制"
      allowed_transitions: ["MODE_SURGERY", "MODE_STANDBY"]
  
  # ─────────────────────────────────────────────────────────────────────────
  # 状态转换条件 (Transitions)
  # ─────────────────────────────────────────────────────────────────────────
  transitions:
    
    - id: "TR_OFF_TO_STANDBY"
      from: "MODE_OFF"
      to: "MODE_STANDBY"
      trigger: "Manual Operator Command"
      pre_conditions:
        - "AHU无故障"
        - "水系统正常"
        - "电源正常"
      actions:
        - "执行AHU启动序列"
        - "等待压差建立"
      duration: "15分钟"
      
    - id: "TR_STANDBY_TO_PREP"
      from: "MODE_STANDBY"
      to: "MODE_PREP"
      triggers:
        - type: "Scheduled"
          condition: "HIS_Surgery_Schedule_Start - 30min"
          source: "HIS接口"
        - type: "Manual"
          condition: "Operator Button on Local Panel"
      actions:
        - "增加送风量至100%"
        - "启动温湿度控制"
        - "加强压差控制"
      duration: "30分钟"
      
    - id: "TR_PREP_TO_SURGERY"
      from: "MODE_PREP"
      to: "MODE_SURGERY"
      trigger: "环境参数达标 AND 手术团队就位"
      pre_conditions:
        - "温度达到设定值±1°C"
        - "湿度达到设定值±5%RH"
        - "压差≥+12Pa"
        - "稳定运行>5分钟"
      confirmation: "手术室面板确认"
      
    - id: "TR_SURGERY_TO_DECON"
      from: "MODE_SURGERY"
      to: "MODE_DECON"
      trigger: "Surgery_End_Signal"
      source: "手术室面板 OR HIS"
      delay: "5分钟（允许人员撤离）"
      
    - id: "TR_DECON_TO_STANDBY"
      from: "MODE_DECON"
      to: "MODE_STANDBY"
      trigger: "消毒程序完成"
      conditions:
        - "消毒时间满足要求"
        - "臭氧浓度降至安全水平"
        
    - id: "TR_ANY_TO_EMERGENCY"
      from: "*"
      to: "MODE_EMERGENCY"
      trigger: "Emergency_Signal"
      priority: "HIGHEST"
      override: true
      
    - id: "TR_EMERGENCY_RECOVERY"
      from: "MODE_EMERGENCY"
      to: "MODE_SURGERY | MODE_STANDBY"
      trigger: "Emergency Cleared + Manual Confirmation"
      requires: "Operator Override"
  
  # ─────────────────────────────────────────────────────────────────────────
  # 控制回路定义 (Control Loops)
  # ─────────────────────────────────────────────────────────────────────────
  control_loops:
    
    # 温度串级控制
    - loop_id: "LOOP-OR001-TEMP"
      name: "手术室温度控制"
      type: "Cascade PID"
      active_in: ["MODE_PREP", "MODE_SURGERY"]
      
      master_loop:
        name: "室温主回路"
        PV: 
          source: "CO-HVAC-ROOM-OR-001.AI_ROOM_TEMP_A"
          backup: "CO-HVAC-ROOM-OR-001.AI_ROOM_TEMP_B"
          selection: "Primary, switch on fault"
        SP:
          source: "FSM state setpoint"
          default: 22.0
          unit: "°C"
          adjustable: true
          range: [21, 27]
        output:
          name: "送风温度设定值"
          range: [14, 22]
          unit: "°C"
        algorithm: "PI"
        parameters:
          Kp: 2.0
          Ti: 600  # seconds
          anti_windup: true
          output_limits: [14, 22]
        
      slave_loop:
        name: "送风温度从回路"
        PV:
          source: "CO-HVAC-AHU-OR-001.AI_SA_TEMP"
        SP:
          source: "Master Output"
        output:
          name: "冷水阀开度"
          target: "CO-HVAC-AHU-OR-001.AO_CHW_VALVE"
          range: [0, 100]
          unit: "%"
        algorithm: "PI"
        parameters:
          Kp: 1.5
          Ti: 180
          
      # Agent-04物理方程前馈
      feedforward:
        enabled: true
        equation_ref: "EQ-HX-COIL-001"
        calculation: |
          # 基于负荷估算预测阀位
          Q_load = ρ × V_air × Cp × (T_return - T_supply_sp)
          Valve_FF = f(Q_load, T_chw, Flow_chw)
        benefit: "提高响应速度，减少超调"
        
      fallback:
        trigger: "传感器故障 OR 网络中断"
        action: "送风温度固定16°C"
    
    # 湿度控制
    - loop_id: "LOOP-OR001-HUMID"
      name: "手术室湿度控制"
      type: "Single PID with Limits"
      active_in: ["MODE_PREP", "MODE_SURGERY"]
      
      PV:
        source: "CO-HVAC-ROOM-OR-001.AI_ROOM_HUMID"
      SP:
        value: 50
        unit: "%RH"
        range: [40, 60]
      output:
        name: "加湿器控制"
        target: "CO-HVAC-AHU-OR-001.AO_HUMIDIFIER"
        range: [0, 100]
      algorithm: "PI"
      parameters:
        Kp: 1.0
        Ti: 300
        
      constraints:
        - name: "防结露"
          condition: "送风相对湿度 < 90%"
        - name: "露点限制"
          condition: "露点温度 < 送风温度 - 2°C"
          
      dehumidification:
        method: "表冷器除湿 + 再热"
        control: "当需要除湿时降低表冷器出口温度"
    
    # 压差控制 (最关键回路)
    - loop_id: "LOOP-OR001-PRESS"
      name: "手术室压差控制"
      type: "Fast PI Control"
      active_in: ["MODE_STANDBY", "MODE_PREP", "MODE_SURGERY"]
      critical: true
      
      PV:
        source: "CO-HVAC-ROOM-OR-001.AI_ROOM_PRESS_A"
        backup: "CO-HVAC-ROOM-OR-001.AI_ROOM_PRESS_B"
        selection: "Primary, switch on deviation"
        deviation_threshold: "3Pa"
      SP:
        by_mode:
          MODE_STANDBY: 8
          MODE_PREP: 15
          MODE_SURGERY: 15
        unit: "Pa"
      output:
        name: "排风阀开度"
        target: "CO-HVAC-AHU-OR-001.AO_RF_SPEED"  # 或排风阀
        range: [0, 100]
      algorithm: "PI"
      parameters:
        Kp: 1.0
        Ti: 30  # 快速响应
        
      door_compensation:
        trigger: "CO-HVAC-ROOM-OR-001.DI_DOOR_MAIN = OPEN"
        action: "临时增加送风量5%"
        recovery: "门关后恢复"
        
      fallback:
        trigger: "双传感器故障"
        action: "排风阀固定30%开度"
        alarm: "CRITICAL"
        
  # ─────────────────────────────────────────────────────────────────────────
  # 顺序控制 (Sequences) - 基于Agent-04 FlowSequence
  # ─────────────────────────────────────────────────────────────────────────
  sequences:
    
    - sequence_id: "SEQ-OR001-STARTUP"
      name: "手术室AHU启动序列"
      trigger: "MODE_OFF → MODE_STANDBY"
      
      # 基于Agent-04的FlowSequence确定启动顺序
      flow_sequence_ref: "FlowSequence-HVAC-OR-001"
      principle: |
        按流体序列的上下游关系启动：
        冷热源 → 输配系统 → 末端设备
        具体到AHU：
        水泵 → 阀门预定位 → 风机
        
      steps:
        - step: 1
          action: "确认冷冻水系统就绪"
          verify: "CHW供回水温差正常"
          timeout: "30s"
          on_fail: "报警，中止启动"
          
        - step: 2
          action: "打开新风阀至10%"
          target: "CO-HVAC-AHU-OR-001.AO_OA_DAMPER = 10%"
          wait: "5s"
          purpose: "预通风"
          
        - step: 3
          action: "预定位冷水阀"
          target: "CO-HVAC-AHU-OR-001.AO_CHW_VALVE = 30%"
          wait: "3s"
          purpose: "防止启动时过冷"
          
        - step: 4
          action: "启动送风机"
          target: "CO-HVAC-AHU-OR-001.DO_SF_START = TRUE"
          wait: "10s"
          verify: "CO-HVAC-AHU-OR-001.DI_SF_RUN = TRUE"
          timeout: "30s"
          on_fail: "报警，尝试重启1次"
          
        - step: 5
          action: "确认风机运行稳定"
          verify: "AI_SF_CURRENT 稳定 AND AI_SA_FLOW > 50%"
          wait: "10s"
          
        - step: 6
          action: "启动排风机"
          target: "CO-HVAC-AHU-OR-001.DO_RF_START = TRUE"
          wait: "5s"
          verify: "CO-HVAC-AHU-OR-001.DI_RF_RUN = TRUE"
          
        - step: 7
          action: "使能压差控制"
          target: "LOOP-OR001-PRESS.enable = TRUE"
          wait: "2s"
          
        - step: 8
          action: "逐步开大新风阀"
          target: "Ramp AO_OA_DAMPER 10% → Setpoint"
          duration: "60s"
          purpose: "平滑过渡，避免压力冲击"
          
        - step: 9
          action: "使能温湿度控制"
          targets:
            - "LOOP-OR001-TEMP.enable = TRUE"
            - "LOOP-OR001-HUMID.enable = TRUE"
          
        - step: 10
          action: "等待环境稳定"
          condition: "压差>+5Pa持续60s"
          timeout: "10min"
          
        - step: 11
          action: "设置状态为STANDBY"
          result: "FSM.state = MODE_STANDBY"
          
    - sequence_id: "SEQ-OR001-SHUTDOWN"
      name: "手术室AHU停机序列"
      trigger: "MODE_STANDBY → MODE_OFF"
      
      steps:
        - step: 1
          action: "禁用温湿度控制"
          
        - step: 2
          action: "关小新风阀至10%"
          duration: "30s"
          
        - step: 3
          action: "关闭冷水阀"
          
        - step: 4
          action: "关闭热水阀"
          
        - step: 5
          action: "停止排风机"
          wait: "5s"
          
        - step: 6
          action: "停止送风机"
          wait: "5s"
          
        - step: 7
          action: "关闭新风阀"
          
        - step: 8
          action: "设置状态为OFF"
          
    - sequence_id: "SEQ-OR001-DECON"
      name: "手术室消毒序列"
      trigger: "MODE_SURGERY → MODE_DECON"
      
      phases:
        - phase: "SELF_CLEAN"
          duration: "20min"
          steps:
            - action: "新风阀开至100%"
            - action: "维持送排风运行"
            - action: "换气次数提高至设计值"
            
        - phase: "DISINFECTION"
          duration: "30min"
          steps:
            - action: "关闭新风阀至0%"
            - action: "关闭排风阀至0%"
            - action: "启动紫外灯"
              target: "CO-HVAC-AHU-OR-001.DO_UV_LAMP = TRUE"
            - action: "保持送风机低速循环"
            - action: "计时30分钟"
            
        - phase: "EXHAUST"
          duration: "10min"
          steps:
            - action: "关闭紫外灯"
            - action: "开启新风阀100%"
            - action: "开启排风阀100%"
            - action: "强制换气10分钟"
            - action: "完成后切换到STANDBY"
```

---

## 2.2 冷站群控状态机

```yaml
Control_State_Machine:
  id: "FSM-CHP-STAGING"
  name: "冷站群控状态机"
  target_system: "HVAC-CHP"
  controller_ref: "CO-INT-BA-DDC-CHP-001"
  criticality: "P1-MISSION_CRITICAL"
  
  # ─────────────────────────────────────────────────────────────────────────
  # 负荷计算 (基于Agent-04物理方程)
  # ─────────────────────────────────────────────────────────────────────────
  load_calculation:
    equation_ref: "EQ-CARRIER-PAYLOAD-WATER"
    formula: |
      Q_load = ρ × V × Cp × ΔT
      where:
        Q_load = 系统冷负荷 (kW)
        ρ = 1000 kg/m³
        V = 系统总流量 (m³/s) from Flow Meter
        Cp = 4.186 kJ/kg·K
        ΔT = T_return - T_supply (K)
        
    inputs:
      - source: "CO-HVAC-CHP-FLOW-001.AI_FLOW"
        name: "系统总流量"
      - source: "CO-HVAC-CHP-CH-001.AI_CHWR_TEMP (averaged)"
        name: "系统回水温度"
      - source: "CO-HVAC-CHP-CH-001.AI_CHWS_TEMP (averaged)"
        name: "系统供水温度"
        
    output:
      name: "Current_Load_kW"
      unit: "kW"
      update_rate: "10s"
  
  # ─────────────────────────────────────────────────────────────────────────
  # 群控状态
  # ─────────────────────────────────────────────────────────────────────────
  states:
    
    - id: "STATE_ALL_OFF"
      name: "全停状态"
      condition: "所有冷机停止"
      
    - id: "STATE_1CH"
      name: "1台冷机运行"
      capacity: "2000kW"
      
    - id: "STATE_2CH"
      name: "2台冷机运行"
      capacity: "4000kW"
      
    - id: "STATE_3CH"
      name: "3台冷机运行"
      capacity: "6000kW"
      
    - id: "STATE_4CH"
      name: "4台冷机运行（满载）"
      capacity: "8000kW"
      
  # ─────────────────────────────────────────────────────────────────────────
  # 加减机逻辑
  # ─────────────────────────────────────────────────────────────────────────
  staging_logic:
    
    add_chiller:
      name: "加机逻辑"
      trigger: |
        (Current_Load / Running_Capacity) > 85%
        持续 10 分钟
        且 有可用冷机
      pre_check:
        - "待启动冷机无故障"
        - "对应冷却塔/水泵可用"
        - "未达最大冷机数量"
      sequence:
        - "选择下一优先级冷机"
        - "执行SEQ-CH-START"
        - "重新分配负荷"
        
    remove_chiller:
      name: "减机逻辑"
      trigger: |
        (Current_Load / Running_Capacity) < 50%
        持续 10 分钟
        且 运行冷机 > 1
      pre_check:
        - "减机后剩余容量 > Current_Load × 1.2"
        - "待停冷机已运行>30分钟"
      sequence:
        - "选择优先级最低的运行冷机"
        - "逐步降低该机负荷"
        - "执行SEQ-CH-STOP"
        - "重新分配负荷"
        
    staging_delay: "10分钟"
    min_runtime: "30分钟"
    min_offtime: "15分钟"
    
  # ─────────────────────────────────────────────────────────────────────────
  # 冷机启动序列 (基于Agent-04 FlowSequence)
  # ─────────────────────────────────────────────────────────────────────────
  sequences:
    
    - sequence_id: "SEQ-CH-START"
      name: "冷机启动序列"
      flow_sequence_principle: |
        按Agent-04的FlowSequence：
        散热侧: 冷却塔 → 冷却水泵 → 冷机冷凝器
        供冷侧: 冷机蒸发器 → 冷冻水泵 → 末端
        
      steps:
        - step: 1
          action: "启动冷却塔风机"
          target: "CO-HVAC-CHP-CT-00X.DO_START"
          wait: "30s"
          verify: "DI_RUN_STATUS = TRUE"
          
        - step: 2
          action: "启动冷却水泵"
          target: "CO-HVAC-CHP-CWP-00X.DO_START"
          wait: "30s"
          verify: "DI_RUN_STATUS = TRUE AND AI_FLOW > 60%"
          
        - step: 3
          action: "确认冷却水流量"
          verify: "冷机DI_CW_FLOW_OK = TRUE"
          timeout: "60s"
          
        - step: 4
          action: "启动冷水机组"
          target: "CO-HVAC-CHP-CH-00X.DO_START"
          wait: "120s"
          verify: "DI_RUN_STATUS = TRUE AND DI_FAULT = FALSE"
          on_fail: "停止CWP、CT，报警"
          
        - step: 5
          action: "启动对应一次冷冻水泵"
          target: "CO-HVAC-CHP-CHWP-00X.DO_START"
          wait: "30s"
          verify: "DI_RUN_STATUS = TRUE"
          
        - step: 6
          action: "确认冷冻水流量"
          verify: "冷机DI_CHW_FLOW_OK = TRUE"
          timeout: "60s"
          
        - step: 7
          action: "等待冷机稳定"
          wait: "300s"
          verify: "AI_CHWS_TEMP接近设定值"
          
        - step: 8
          action: "冷机投入群控"
          result: "标记冷机为RUNNING"
          
    - sequence_id: "SEQ-CH-STOP"
      name: "冷机停机序列"
      steps:
        - step: 1
          action: "降低冷机负荷"
          target: "AO_LOAD_LIMIT = 20%"
          duration: "300s"
          
        - step: 2
          action: "停止冷水机组"
          target: "DO_STOP"
          wait: "30s"
          
        - step: 3
          action: "停止一次冷冻水泵"
          wait: "10s"
          
        - step: 4
          action: "延时停止冷却水泵"
          delay: "300s"
          purpose: "冷却残余热量"
          
        - step: 5
          action: "停止冷却塔"
          condition: "无其他冷机使用该塔"
          
  # ─────────────────────────────────────────────────────────────────────────
  # 优化控制 (L1层功能)
  # ─────────────────────────────────────────────────────────────────────────
  optimization:
    
    chws_reset:
      name: "冷冻水温度重设"
      source: "L1云端优化"
      method: "基于末端阀位"
      logic: |
        IF 所有末端阀位 < 85% THEN
          CHWS_SP += 0.2°C (最高12°C)
        ELSEIF 任一末端阀位 > 95% THEN
          CHWS_SP -= 0.2°C (最低6°C)
      update_interval: "15min"
      fallback: "L1断开时使用7°C默认值"
      
    cws_reset:
      name: "冷却水温度重设"
      method: "基于室外湿球温度"
      formula: "CWS_SP = MAX(18°C, WB_Temp + 3°C)"
      limit: "≤ 32°C"
      
    load_balancing:
      name: "冷机负荷均衡"
      method: "等负荷率分配"
      algorithm: |
        For each running chiller:
          Target_Load_Ratio = Total_Load / (N × Chiller_Capacity)
          Adjust CHWS_SP individually to achieve balance
          
  # ─────────────────────────────────────────────────────────────────────────
  # 降级模式
  # ─────────────────────────────────────────────────────────────────────────
  degradation:
    
    network_loss:
      trigger: "L1通信中断>30s"
      response:
        - "保持当前运行冷机数量"
        - "禁止自动加机（安全考虑）"
        - "允许自动减机（防过载）"
        - "CHWS_SP = 7°C (默认)"
        - "CWS_SP = 32°C (默认)"
        
    single_chiller_fault:
      trigger: "运行中冷机故障"
      response:
        - "立即启动备用冷机"
        - "启动序列按优先级"
        - "报警通知"
```

---

## 2.3 平疫转换控制序列

```yaml
# ═══════════════════════════════════════════════════════════════════════════
# 平疫转换控制序列
# 基于 Agent-02 平疫结合与应急转换模型
# ═══════════════════════════════════════════════════════════════════════════

Pandemic_Conversion_Control:
  id: "CONV-WARD-TO-ISOLATION"
  name: "普通病房→负压隔离病房转换控制"
  
  source_space_type: "WARD-GENERAL"
  target_space_type: "WARD-ISOLATION-NEG"
  
  activation:
    trigger: "疫情响应指令（手动确认）"
    authorization: "医院管理层 + 工程部"
    
  # ─────────────────────────────────────────────────────────────────────────
  # 预置条件检查
  # ─────────────────────────────────────────────────────────────────────────
  pre_conditions:
    infrastructure:
      - check: "预留负压排风接口可用"
        location: "病房天花排风口"
      - check: "HEPA过滤器安装就位"
      - check: "独立排风系统电源正常"
    operational:
      - check: "病房已疏散患者"
      - check: "工程人员就位"
      - check: "维护工具准备"
        
  # ─────────────────────────────────────────────────────────────────────────
  # 转换控制序列
  # ─────────────────────────────────────────────────────────────────────────
  conversion_sequence:
    
    phase_1:
      name: "系统准备"
      duration: "30分钟"
      steps:
        - step: 1
          action: "停止原空调系统"
          target: "AHU serving the ward"
          command: "STOP"
          verify: "SF/RF stopped"
          
        - step: 2
          action: "关闭回风阀"
          target: "RA_DAMPER = 0%"
          purpose: "防止交叉污染"
          
        - step: 3
          action: "隔离该区域冷热水"
          target: "Zone isolation valves CLOSE"
          
        - step: 4
          action: "确认负压排风系统就绪"
          verify: "排风机可用，无故障"
          
    phase_2:
      name: "管路切换"
      duration: "2小时"
      manual_work: true
      steps:
        - step: 1
          action: "接通预留负压排风接口"
          type: "现场施工"
          
        - step: 2
          action: "安装HEPA过滤器"
          type: "现场施工"
          verification: "密封性检测"
          
        - step: 3
          action: "封堵非必要开口"
          type: "现场施工"
          
        - step: 4
          action: "检查门密封"
          
    phase_3:
      name: "控制系统切换"
      duration: "30分钟"
      steps:
        - step: 1
          action: "DDC程序切换到负压模式"
          command: "WRITE FSM.Mode = ISOLATION"
          
        - step: 2
          action: "修改压差设定值"
          old_value: "+10Pa"
          new_value: "-10Pa"
          command: "WRITE PRESS_SP = -10"
          
        - step: 3
          action: "调整换气次数"
          target: "增加至设计值"
          
        - step: 4
          action: "启动负压排风机"
          verify: "运行确认"
          
        - step: 5
          action: "新风切换100%"
          purpose: "无回风，全新风运行"
          
        - step: 6
          action: "使能压差控制"
          target: "LOOP-ISO-PRESS.enable = TRUE"
          
    phase_4:
      name: "验证测试"
      duration: "1小时"
      steps:
        - step: 1
          action: "烟雾测试确认气流方向"
          method: "发烟管测试门缝气流"
          acceptance: "气流从走廊流向病房"
          
        - step: 2
          action: "压差稳定性测试"
          duration: "30分钟"
          acceptance: "-10Pa ±2Pa"
          
        - step: 3
          action: "开门压差测试"
          method: "开门时测量风速"
          acceptance: "门洞风速≥0.5m/s 向内"
          
        - step: 4
          action: "密封性检查"
          method: "巡检所有穿墙管线"
          
    phase_5:
      name: "投入使用"
      steps:
        - action: "记录转换完成"
        - action: "更新BMS空间属性"
        - action: "通知医护人员"
        - action: "启动持续压差监测"
        - action: "设置报警阈值"
          threshold: "压差>-5Pa 报警"
          
  total_time: "约4小时"
  
  # ─────────────────────────────────────────────────────────────────────────
  # 恢复序列
  # ─────────────────────────────────────────────────────────────────────────
  recovery_sequence:
    name: "隔离病房→普通病房恢复"
    trigger: "疫情解除 + 终末消毒完成"
    
    steps:
      - "终末消毒（按感控要求）"
      - "拆除临时HEPA过滤器"
      - "恢复回风管路"
      - "DDC程序切回正常模式"
      - "压差设定恢复+10Pa"
      - "空气质量检测达标"
      - "环境验收"
      
    total_time: "约8小时"
```

---

# 第三部分：韧性与降级模式 / 韧性架构
## (Resilience & Fallback / Resilience Architecture)

本部分基于Agent-05的Criticality等级，定义控制器层级、网络拓扑及故障降级策略。

---

## 3.1 控制器层级架构

```yaml
Controller_Hierarchy:
  
  # ═══════════════════════════════════════════════════════════════════════════
  # L1: 云端/中央监控层
  # ═══════════════════════════════════════════════════════════════════════════
  L1_Central:
    name: "云端/中央监控层"
    location: "数据中心 / 中央控制室"
    
    components:
      BMS_Server:
        type: "楼宇自控服务器"
        quantity: 2  # 主备
        functions:
          - "全院系统监控"
          - "历史数据存储"
          - "报表生成"
          - "远程访问"
        database: "时序数据库 (InfluxDB/TimescaleDB)"
        retention: "5年"
        
      Optimization_Engine:
        type: "优化算法服务器"
        functions:
          - "冷站能效优化"
          - "需求响应"
          - "预测性维护"
        algorithms:
          - "Model Predictive Control (MPC)"
          - "Machine Learning"
        update_interval: "5-15min"
        
      SCADA_Workstation:
        type: "监控工作站"
        quantity: 4
        locations:
          - "中央控制室 ×2"
          - "动力机房值班室"
          - "工程部办公室"
          
    communication:
      uplink: "Internet/VPN (加密)"
      downlink: "BACnet/IP"
      
    failure_impact: |
      L1失效时：
      - 优化算法停止
      - 远程监控中断
      - 历史数据暂时中断
      - L2/L3继续独立运行
      - 能效下降10-15%
      
  # ═══════════════════════════════════════════════════════════════════════════
  # L2: 边缘控制层
  # ═══════════════════════════════════════════════════════════════════════════
  L2_Edge:
    name: "边缘控制层"
    
    components:
      
      Edge_Gateway:
        type: "边缘网关"
        quantity: 2  # 主楼+附楼
        functions:
          - "协议转换 (BACnet ↔ MQTT)"
          - "本地数据缓存 (7天)"
          - "云边协同"
          - "本地报警处理"
        specs:
          processor: "ARM Cortex-A72"
          memory: "4GB RAM"
          storage: "256GB SSD"
          power: "24VDC, 冗余"
        offline_capability: "72小时独立运行"
        
      NAC_Controllers:
        type: "网络自动化控制器"
        quantity: 8
        distribution:
          - id: "NAC-OR"
            location: "手术部"
            managed_ddcs: 12
          - id: "NAC-ICU"
            location: "ICU区域"
            managed_ddcs: 8
          - id: "NAC-CHP"
            location: "冷冻站"
            managed_ddcs: 4
          - id: "NAC-EL"
            location: "电气机房"
            managed_ddcs: 6
          - id: "NAC-WARD-A"
            location: "住院楼A"
            managed_ddcs: 15
          - id: "NAC-WARD-B"
            location: "住院楼B"
            managed_ddcs: 15
          - id: "NAC-OPD"
            location: "门诊楼"
            managed_ddcs: 12
          - id: "NAC-SERVICE"
            location: "后勤楼"
            managed_ddcs: 8
        functions:
          - "DDC程序管理"
          - "趋势数据汇总"
          - "区域报警处理"
          - "区域时间程序"
          
      DDC_Controllers:
        type: "直接数字控制器"
        total_quantity: 80
        distribution:
          HVAC: 45
          ELEC: 12
          PLUMB: 8
          MGAS: 6
          FIRE: 5  # 接口，非主控
          INT: 4
        specs:
          io_capacity: "8-32 AI/AO, 16-32 DI/DO"
          communication: "BACnet MS/TP or IP"
          standalone: true
          battery: "72h RTC保持"
          
      PLC_Controllers:
        type: "可编程逻辑控制器"
        quantity: 6
        applications:
          - id: "PLC-FAS"
            function: "消防联动控制"
            redundancy: "热备"
            safety_rating: "SIL2"
          - id: "PLC-CHP-1"
            function: "冷站群控"
            redundancy: "推荐热备"
          - id: "PLC-CHP-2"
            function: "锅炉群控"
          - id: "PLC-EPS"
            function: "应急电源管理"
            redundancy: "热备"
          - id: "PLC-MGAS"
            function: "医用气体监控"
          - id: "PLC-ELEV"
            function: "电梯群控"
            
    communication:
      inter_controller: "BACnet MS/TP, 76800bps"
      to_gateway: "BACnet/IP"
      
  # ═══════════════════════════════════════════════════════════════════════════
  # L3: 硬件保护层
  # ═══════════════════════════════════════════════════════════════════════════
  L3_Hardware:
    name: "硬件保护层"
    
    devices:
      mechanical_thermostat:
        quantity: 30
        locations: "所有手术室、ICU"
        range: "18-26°C"
        action: "直接控制备用加热器"
        
      freeze_protection_switch:
        quantity: 50
        locations: "所有表冷器/新风段"
        setpoint: "5°C"
        action: "强制开热水阀/关新风阀"
        
      fire_damper_70c:
        quantity: 200
        locations: "穿越防火分区处"
        fusible: "70°C"
        action: "弹簧关闭"
        
      smoke_fire_damper_280c:
        quantity: 50
        locations: "排烟风管"
        fusible: "280°C"
        action: "弹簧关闭"
        
      pressure_relief:
        quantity: 10
        locations: "锅炉、压缩机"
        action: "超压泄放"
        
      emergency_stop:
        quantity: 100
        locations: "大型设备旁"
        action: "硬线直接断电"
```

---

## 3.2 全局联锁矩阵

```yaml
Global_Interlock_Matrix:
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 消防联动矩阵 (基于Agent-01 FIRE-FAS)
  # ═══════════════════════════════════════════════════════════════════════════
  fire_interlock:
    scenario_ref: "SCN_FIRE_EMERGENCY"
    priority: "CRITICAL (Level 0)"
    wiring: "硬接点联动优先"
    
    matrix:
      # 信号源 → 受控设备 → 动作
      
      - id: "FI-001"
        source: "FIRE_ALARM_CONFIRMED"
        targets:
          - system: "HVAC-AHU"
            device_scope: "着火区域AHU"
            action: "STOP"
            wiring: "硬接点"
            delay: "0s"
            
      - id: "FI-002"
        source: "FIRE_ALARM_CONFIRMED"
        targets:
          - system: "HVAC-FCU"
            device_scope: "着火区域FCU"
            action: "CLOSE_VALVE"
            wiring: "DDC指令"
            delay: "0s"
            
      - id: "FI-003"
        source: "FIRE_ALARM_CONFIRMED"
        targets:
          - system: "FIRE-EXH"
            device_type: "防火阀"
            action: "CLOSE"
            wiring: "电磁释放（硬接点）"
            delay: "0s"
            
      - id: "FI-004"
        source: "FIRE_ALARM_CONFIRMED + 该区域排烟"
        targets:
          - system: "FIRE-EXH"
            device_type: "排烟阀"
            action: "OPEN"
            wiring: "硬接点"
            delay: "0s"
            
      - id: "FI-005"
        source: "排烟阀开启确认"
        targets:
          - system: "FIRE-EXH"
            device_type: "排烟风机"
            action: "START"
            wiring: "硬接点"
            delay: "10s"
            
      - id: "FI-006"
        source: "FIRE_ALARM_CONFIRMED"
        targets:
          - system: "FIRE-EXH"
            device_type: "正压送风机"
            action: "START"
            wiring: "硬接点"
            delay: "0s"
            
      - id: "FI-007"
        source: "FIRE_ALARM_CONFIRMED"
        targets:
          - system: "ELEC-EL"
            device_type: "电梯"
            action: "FIRE_RECALL (迫降首层)"
            wiring: "硬接点"
            delay: "0s"
            
      - id: "FI-008"
        source: "FIRE_ALARM_CONFIRMED"
        targets:
          - system: "ELEC-LV"
            device_type: "非消防电源"
            action: "CUT_OFF (分励脱扣)"
            wiring: "硬接点"
            delay: "30s"
            exception: "消防电源保留"
            
      - id: "FI-009"
        source: "FIRE_ALARM_CONFIRMED"
        targets:
          - system: "INT-SEC"
            device_type: "门禁"
            action: "RELEASE (紧急开启)"
            wiring: "硬接点"
            delay: "0s"
            
      - id: "FI-010"
        source: "FIRE_ALARM_CONFIRMED"
        targets:
          - system: "MGAS-O2"
            device_scope: "全院"
            action: "ALARM_ONLY (仅报警)"
            wiring: "通信"
            note: "不自动切断，需人工确认"
            
      - id: "FI-011"
        source: "水流信号/压力开关"
        targets:
          - system: "FIRE-SPS"
            device_type: "消火栓泵"
            action: "START"
            wiring: "硬接点"
            delay: "0s"
            
      - id: "FI-012"
        source: "报警阀压力开关"
        targets:
          - system: "FIRE-SPS"
            device_type: "喷淋泵"
            action: "START"
            wiring: "硬接点"
            delay: "0s"
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 手术室特殊联锁
  # ═══════════════════════════════════════════════════════════════════════════
  operating_room_special:
    
    fire_during_surgery:
      scenario: "手术进行中发生火灾"
      priority: "医疗安全优先"
      
      logic:
        if_fire_in_OR_zone:
          decision: "由手术团队判断"
          options:
            - "立即终止手术，紧急撤离"
            - "快速完成关键操作后撤离"
          hvac_action:
            - "关闭AHU"
            - "关闭医气阀门（人工）"
            
        if_fire_not_in_OR_zone:
          decision: "可继续手术"
          hvac_action:
            - "维持正压"
            - "切换100%循环风"
            - "关闭新风阀（防烟气进入）"
            - "继续温湿度控制"
          notification:
            - "手术室内显示火警信息"
            - "护士站声光报警"
            - "让手术团队知晓情况"
```

---

## 3.3 Criticality-Based降级策略表

```yaml
Degradation_Strategies:
  
  # 基于Agent-05 Criticality_Distribution定义降级策略
  
  # ═══════════════════════════════════════════════════════════════════════════
  # CRITICAL级别控制对象降级策略
  # ═══════════════════════════════════════════════════════════════════════════
  
  CRITICAL_Level:
    applicable_CUs:
      - "CU-OR001-HVAC_CLN-PRESSURE"
      - "CU-ICU-HVAC-PRESSURE"
      - "CU-ISO-NEG-PRESSURE"
      
    strategies:
      
      sensor_failure:
        failure_type: "关键传感器故障"
        examples: ["压差传感器", "室温传感器"]
        
        response_chain:
          - level: 1
            trigger: "主传感器故障"
            action: "自动切换备用传感器"
            time: "<5秒"
            alarm: "HIGH"
            
          - level: 2
            trigger: "备用传感器也故障"
            action: "启用软测量/物理模型估算"
            method: "基于Agent-04物理方程"
            example: |
              压差估算 = f(送风量, 排风量, 开口面积)
            alarm: "CRITICAL"
            duration: "15分钟"
            
          - level: 3
            trigger: "软测量不可用 或 超过15分钟"
            action: "切换到固定设定值模式"
            setpoints:
              exhaust_damper: "30%固定开度"
              supply_speed: "保持当前值"
            alarm: "CRITICAL + 现场核查"
            
          - level: 4
            trigger: "DDC完全失效"
            action: "L3硬件保护接管"
            mechanism: "机械恒温器控制"
            
      network_failure:
        failure_type: "网络中断"
        
        response_chain:
          - level: 1
            trigger: "与上位机通信中断30秒"
            action:
              - "DDC切换本地模式"
              - "使用本地默认设定值"
              - "继续闭环控制"
            local_defaults:
              OR_temp: "22°C"
              OR_humid: "50%RH"
              OR_press: "+15Pa"
              
          - level: 2
            duration: "网络中断持续"
            action:
              - "DDC独立运行最长48小时"
              - "本地存储趋势数据"
              - "本地报警通知（如配置）"
              
          - level: 3
            trigger: "网络恢复"
            action:
              - "自动重连上位机"
              - "同步时钟"
              - "上传离线数据"
              - "下载更新的设定值"
              
      controller_failure:
        failure_type: "DDC控制器故障"
        
        response:
          actuator_behavior:
            - "阀门保持最后位置(HOLD_LAST) 15分钟"
            - "15分钟后切换到失效安全位置(FAIL_SAFE)"
            
          fail_safe_positions:
            CHW_valve: "CLOSE"
            HW_valve: "OPEN"
            OA_damper: "10% (最小新风)"
            EA_damper: "30% (维持基本排风)"
            
          L3_takeover:
            - "机械恒温器接管温度"
            - "防冻开关保护盘管"
            
          notification:
            - "中控室CRITICAL报警"
            - "自动派发紧急工单"
            - "备用控制器接管（如配置热备）"
            
      actuator_failure:
        failure_type: "执行器故障"
        
        detection:
          method: "指令-反馈偏差"
          criteria: "|Command - Feedback| > 10% 持续5分钟"
          
        response_by_device:
          CHW_valve_stuck_open:
            impact: "持续供冷，可能过冷"
            action:
              - "报警"
              - "降低送风量补偿"
              - "派维修"
              
          CHW_valve_stuck_closed:
            impact: "无法供冷，温度上升"
            action:
              - "CRITICAL报警"
              - "增加送风量（如可能）"
              - "通知手术室评估是否继续手术"
              - "紧急维修"
              
          supply_fan_failure:
            impact: "失去正压和洁净度"
            action:
              - "EMERGENCY报警"
              - "停止排风机"
              - "关闭新风阀"
              - "通知手术室"
              - "启用备用风机（如有）"
  
  # ═══════════════════════════════════════════════════════════════════════════
  # HIGH级别控制对象降级策略
  # ═══════════════════════════════════════════════════════════════════════════
  
  HIGH_Level:
    applicable_CUs:
      - "CU-OR001-HVAC_CLN-COOLING"
      - "CU-ICU-HVAC-COOLING"
      - "CU-WARD-HVAC"
      
    strategies:
      
      sensor_failure:
        response_chain:
          - level: 1
            action: "切换备用传感器"
            alarm: "HIGH"
          - level: 2
            action: "使用物理模型估算"
            duration: "30分钟"
          - level: 3
            action: "固定输出模式"
            alarm: "HIGH + 维修派单"
            
      network_failure:
        response:
          - "本地默认设定值运行"
          - "节能优化暂停"
          - "基本控制功能保持"
          
      controller_failure:
        response:
          - "执行器保持最后位置"
          - "其他DDC可代理部分功能（如配置）"
          - "L3保护有效"
  
  # ═══════════════════════════════════════════════════════════════════════════
  # MEDIUM/LOW级别控制对象降级策略
  # ═══════════════════════════════════════════════════════════════════════════
  
  MEDIUM_LOW_Level:
    applicable_CUs:
      - "CU-OFC-HVAC"
      - "CU-LOBBY-HVAC"
      - "CU-PARKING-HVAC"
      
    strategies:
      any_failure:
        response:
          - "报警通知"
          - "可接受临时停机"
          - "按优先级排队维修"
          - "不影响关键医疗区域"
```

---

## 3.4 网络拓扑架构

```yaml
Control_Network_Topology:
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 网络分层架构
  # ═══════════════════════════════════════════════════════════════════════════
  
  layers:
    
    L1_Enterprise_Network:
      name: "企业网络层"
      protocol: "TCP/IP"
      security: "防火墙隔离"
      components:
        - "BMS服务器"
        - "优化引擎"
        - "SCADA工作站"
        - "Web服务器（外部访问）"
      connection_to_L2: "边缘网关（协议转换）"
      
    L2_Building_Network:
      name: "楼宇控制网络"
      protocol: "BACnet/IP"
      topology: "星型 + 环网备份"
      vlan: "独立VLAN（VLAN 100）"
      switches:
        type: "工业级交换机"
        quantity: 10
        features: ["RSTP冗余", "VLAN隔离", "端口镜像"]
      components:
        - "边缘网关"
        - "NAC控制器"
        - "BACnet/IP DDC"
        - "消防FAS主机接口"
        - "电力监控接口"
      security:
        - "MAC地址绑定"
        - "端口安全"
        - "禁用未授权端口"
        
    L3_Field_Network:
      name: "现场总线层"
      protocols:
        BACnet_MSTP:
          usage: "DDC控制器间"
          topology: "菊花链"
          baud_rate: "76800 bps"
          cable: "RVSP 2×0.75 屏蔽双绞线"
          max_length: "1200m"
          max_devices: "127 per trunk"
          segments:
            - name: "手术部MSTP-1"
              controllers: 12
              length: "400m"
            - name: "ICU MSTP-1"
              controllers: 8
              length: "200m"
            # ... more segments
              
        Modbus_RTU:
          usage: "第三方设备/电表/变频器"
          baud_rate: "9600 bps"
          parity: "Even"
          max_devices: "32 per bus"
          
        Hardwired:
          usage: "消防联动/安全联锁"
          type: "24VDC 或 干接点"
          cable: "独立敷设，不共护套"
          supervision: "开路/短路监测（可选）"
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 网络拓扑图 (ASCII)
  # ═══════════════════════════════════════════════════════════════════════════
  
  topology_diagram: |
    
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                        L1: 企业网络 / 云端                               │
    │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐                    │
    │  │   BMS   │  │ 优化    │  │ SCADA   │  │  外部   │                    │
    │  │ Server  │  │ Engine  │  │   WS    │  │ 访问    │                    │
    │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘                    │
    │       └────────────┴────────────┴────────────┘                          │
    │                            │                                            │
    │                    ┌───────┴───────┐                                    │
    │                    │   防火墙      │                                    │
    │                    └───────┬───────┘                                    │
    └────────────────────────────┼────────────────────────────────────────────┘
                                 │
    ┌────────────────────────────┼────────────────────────────────────────────┐
    │                    ┌───────┴───────┐                                    │
    │                    │ 边缘网关×2    │                                    │
    │                    │ (主/备)       │                                    │
    │                    └───────┬───────┘                                    │
    │                            │ BACnet/IP                                  │
    │  L2: 楼宇控制网络 ─────────┼─────────────────────────────────────────── │
    │                            │                                            │
    │    ┌───────────────────────┼───────────────────────┐                    │
    │    │                       │                       │                    │
    │  ┌─┴──────┐          ┌─────┴─────┐           ┌─────┴─────┐              │
    │  │ 核心   │──────────│   环网    │───────────│   核心    │              │
    │  │交换机A │          │   备份    │           │ 交换机B   │              │
    │  └─┬──────┘          └───────────┘           └─────┬─────┘              │
    │    │                                               │                    │
    │  ┌─┴───────┐  ┌─────────┐  ┌─────────┐  ┌─────────┴─┐                  │
    │  │楼层     │  │楼层     │  │楼层     │  │楼层       │                  │
    │  │交换机   │  │交换机   │  │交换机   │  │交换机     │                  │
    │  └─┬───────┘  └─┬───────┘  └─┬───────┘  └─┬─────────┘                  │
    │    │            │            │            │                             │
    └────┼────────────┼────────────┼────────────┼─────────────────────────────┘
         │            │            │            │
    ┌────┼────────────┼────────────┼────────────┼─────────────────────────────┐
    │    │            │            │            │                             │
    │  ┌─┴────┐    ┌──┴───┐    ┌───┴──┐    ┌────┴──┐                          │
    │  │NAC-OR│    │NAC-  │    │NAC-  │    │NAC-   │                          │
    │  │      │    │ICU   │    │CHP   │    │WARD   │                          │
    │  └─┬────┘    └──┬───┘    └───┬──┘    └────┬──┘                          │
    │    │            │            │            │                             │
    │  L3: 现场总线 ──┼────────────┼────────────┼───────────────────────────  │
    │    │            │            │            │                             │
    │  ┌─┴─────────────────────────────────────────────────┐                  │
    │  │ BACnet MS/TP 总线 (76800bps)                      │                  │
    │  │                                                   │                  │
    │  │  ┌────┐  ┌────┐  ┌────┐  ┌────┐  ┌────┐          │                  │
    │  │  │DDC │──│DDC │──│DDC │──│DDC │──│DDC │──...     │                  │
    │  │  │ 1  │  │ 2  │  │ 3  │  │ 4  │  │ 5  │          │                  │
    │  │  └────┘  └────┘  └────┘  └────┘  └────┘          │                  │
    │  └───────────────────────────────────────────────────┘                  │
    │                                                                         │
    │  ┌──────────────────────────────────────────────────────────────────┐   │
    │  │ 硬接点联动 (消防/安全)                                            │   │
    │  │                                                                  │   │
    │  │  FAS ═══════╦══════╦══════╦══════╦══════╗                        │   │
    │  │             ║      ║      ║      ║      ║                        │   │
    │  │           ┌─╨─┐  ┌─╨─┐  ┌─╨─┐  ┌─╨─┐  ┌─╨─┐                      │   │
    │  │           │AHU│  │排烟│  │电梯│  │门禁│  │切电│                     │   │
    │  │           └───┘  └───┘  └───┘  └───┘  └───┘                      │   │
    │  └──────────────────────────────────────────────────────────────────┘   │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
```

---

## 3.5 数据点表命名规则

```yaml
Point_Naming_Convention:
  
  # 与Agent-03设备ID保持一致的命名规则
  
  format: "{System}-{Location}-{Equipment}-{PointType}_{PointName}"
  
  segments:
    
    System:
      description: "系统代码"
      length: "3-5字符"
      examples:
        - "HVAC"
        - "ELEC"
        - "PLUMB"
        - "MGAS"
        - "FIRE"
        - "INT"
        
    Location:
      description: "位置代码"
      format: "{Building}-{Floor}-{Zone}"
      examples:
        - "MAIN-B1-CHP"   # 主楼地下1层冷站
        - "MAIN-3F-OR"    # 主楼3层手术区
        - "MAIN-5F-ICU"   # 主楼5层ICU
        
    Equipment:
      description: "设备代码（继承Agent-03）"
      examples:
        - "CH001"     # 1号冷机
        - "AHU-OR01"  # 1号手术室空调
        - "CHWP001"   # 1号冷冻水泵
        
    PointType:
      description: "点位类型"
      codes:
        AI: "模拟量输入"
        AO: "模拟量输出"
        DI: "数字量输入"
        DO: "数字量输出"
        AV: "模拟量值（计算/设定）"
        BV: "二进制值"
        MSV: "多状态值"
        
    PointName:
      description: "点位名称缩写"
      examples:
        TEMP: "温度"
        HUMID: "湿度"
        PRESS: "压力"
        FLOW: "流量"
        STATUS: "状态"
        CMD: "指令"
        SP: "设定值"
        FB: "反馈"
        ALM: "报警"
  
  examples:
    # 冷站设备
    - "HVAC-MAIN-B1-CHP-CH001-AI_CHWS_TEMP"      # 1号冷机冷冻水供水温度
    - "HVAC-MAIN-B1-CHP-CHWP001-AO_VFD_SPEED"    # 1号冷冻水泵变频指令
    - "HVAC-MAIN-B1-CHP-CHWP001-DI_RUN_STATUS"   # 1号冷冻水泵运行状态
    
    # 手术室设备
    - "HVAC-MAIN-3F-OR-AHU01-AI_SA_TEMP"         # 1号手术室AHU送风温度
    - "HVAC-MAIN-3F-OR-RM001-AI_ROOM_TEMP_A"     # 1号手术室室温A
    - "HVAC-MAIN-3F-OR-RM001-AI_ROOM_PRESS_A"    # 1号手术室压差A
    
    # 医用气体
    - "MGAS-MAIN-3F-OR-O2-ZV001-AI_PRESS"        # 手术区氧气阀箱压力
    - "MGAS-MAIN-B1-GAS-COMP001-DI_RUN_STATUS"   # 1号空压机运行状态
    
    # 电气系统
    - "ELEC-MAIN-B1-EL-MDB001-AI_VOLTAGE_L1"     # 主配电柜L1电压
    - "ELEC-MAIN-3F-OR-IPS001-AI_INSULATION"     # 手术室隔离电源绝缘电阻
    
    # 消防系统
    - "FIRE-MAIN-B1-FIRE-FHP001-DI_RUN_STATUS"   # 消火栓泵运行状态
    - "FIRE-MAIN-RF-FIRE-SEF001-DI_RUN_STATUS"   # 排烟风机运行状态
    
  # 与Agent-03 ID映射
  agent03_mapping:
    principle: "设备ID继承Agent-03，点位ID在其基础上扩展"
    example:
      agent03_equipment_id: "EQP-CH-CENT-001"
      agent06_point_prefix: "HVAC-MAIN-B1-CHP-CH001"
      generated_points:
        - "HVAC-MAIN-B1-CHP-CH001-AI_CHWS_TEMP"
        - "HVAC-MAIN-B1-CHP-CH001-AI_CHWR_TEMP"
        - "HVAC-MAIN-B1-CHP-CH001-AI_LOAD_PERCENT"
        - "HVAC-MAIN-B1-CHP-CH001-DI_RUN_STATUS"
        - "HVAC-MAIN-B1-CHP-CH001-DO_START"
```

---

# 附录：文档交付物清单

```yaml
Agent06_Deliverables:
  
  completed:
    - file: "控制架构与降级策略白皮书_v2.1"
      status: "已完成"
      content: "三级控制保障架构、设计哲学、降级策略"
      
    - file: "全域控制系统实现模型_v3.1"
      status: "本文档"
      content:
        part_1: "全域控制对象清单 (六大专业I/O点位)"
        part_2: "场景化控制逻辑 (状态机、控制回路、顺序)"
        part_3: "韧性架构 (联锁矩阵、降级策略、网络拓扑)"
  
  model_statistics:
    control_objects_defined: 15  # 典型示例
    io_points_per_object: "20-50"
    state_machines: 3
    control_loops: 10
    sequences: 8
    interlock_rules: 25
    
  coverage:
    HVAC:
      systems: ["CHP", "AHU", "FCU", "PAU"]
      objects: ["冷机", "水泵", "AHU", "室内传感器", "走廊压差"]
    ELEC:
      systems: ["HV", "LV", "EPS", "UPS"]
      objects: ["配电柜", "发电机", "隔离变压器"]
    MGAS:
      systems: ["O2", "VAC", "AIR", "N2O"]
      objects: ["区域阀箱", "真空泵", "空压机"]
    FIRE:
      systems: ["FAS", "SPS", "EXH"]
      objects: ["消防泵", "排烟风机", "防火阀"]
    PLUMB:
      systems: ["DWS", "HWS", "SAN", "RW"]
      objects: ["给水泵", "热水循环泵"]
    INT:
      systems: ["BA", "SEC", "NUR"]
      objects: ["DDC控制器", "护士呼叫"]
      
  validation_readiness:
    simulation_models: "待Agent-04物理模型集成"
    hil_test_cases: "已定义框架"
    site_test_procedures: "已定义步骤"
```

---

**Agent-06 全域控制系统实现模型 v3.1 完成**

---

本文档已根据修正版任务书v3.1完成以下任务：

1. ✅ **全域控制对象清单**：覆盖六大专业的典型I/O点位定义
2. ✅ **场景化控制逻辑**：包含状态机、PID策略、顺序控制
3. ✅ **物理方程融合**：引用Agent-04的FlowSequence和物理方程用于前馈控制
4. ✅ **韧性架构**：基于Criticality等级的降级策略、消防联锁矩阵
5. ✅ **网络拓扑与命名规则**：与Agent-03 ID保持一致

如需进一步细化特定系统或空间的控制模型，请告知。
[^1]: [Agent-01 系统拓扑建模师 - 完整输出文档.md](http://file/fb792853-9410-4a6d-9389-5740af5b6fee.md)

[^2]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^3]: [Agent01_Output.project_summary.md](http://file/857edf8d-27c4-46a4-9be6-49c7310e56fc.md)

[^4]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^5]: [# Agent-05和Agent-07输出文件重..."

[^6]: [# Agent-03: 设备本体建模师 (Equ...体化建模

[^1]: [Agent-05 系统-空间耦合建模师.md](http://file/3eb5303c-77a6-4bf1-aa23-5d864256776c.md)

[^2]: [# === AGENT-09: 统一CIM模型 ...on: “医用床塔管道疋 - 吊臂式供气供电+](# === AGENT-09: 统一CIM模型 ...on: “医用床塔管道疋 - 吊臂式供气供电+)

[^3]: [Agent-02  空间本体建模师 (Space Ontology Architect).md](http://file/35de1547-3b35-4ab4-a98a-37fb6cf0b0b6.md)

[^4]: [# Agent-05和Agent-07输出文件重..."

[^5]: [# Agent-05和Agent-07输出文件重..."

[^6]: [# === AGENT-09: 统一CIM模型 ...on: “医用床塔管道疋 - 吊臂式供气供电+](# === AGENT-09: 统一CIM模型 ...on: “医用床塔管道疋 - 吊臂式供气供电+)

[^1]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^2]: [Agent-02  空间本体建模师 (Space Ontology Architect).md](http://file/35de1547-3b35-4ab4-a98a-37fb6cf0b0b6.md)

[^3]: [# 医疗专用空间详细建模（Medical Spe...   - terminal_locations](# 医疗专用空间详细建模（Medical Spe...   - terminal_locations)

[^4]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^5]: [# Agent-08 运维管理建模师 输出文件元...etency: "人员资质能力达标率100%"](# Agent-08 运维管理建模师 输出文件元...etency: "人员资质能力达标率100%")

[^6]: [Agent-02  空间本体建模师 (Space Ontology Architect).md](http://file/35de1547-3b35-4ab4-a98a-37fb6cf0b0b6.md)

[^1]: [# Agent-05和Agent-07输出文件重..."

[^2]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^3]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^4]: [Agent-03 v2.2  设备本体建模师 (Equipment Ontology Architect) 完整输出.md](http://file/6c1c1929-d310-442c-8bd3-24228af83d28.md)

[^5]: [Agent-04 流动模型建模师 完整输出文档 V2.3版.md](http://file/05b8fc3a-a8c7-44d4-a15c-91ce05fa76bc.md)

[^6]: [Agent03_Output.project_summary.md](http://file/fa4943df-69fe-440d-9d09-f824be4349ec.md)

[^1]: [# Agent-04 流动模型建模输出文件

[^2]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^3]: [# Agent-04 流动模型建模输出文件

[^4]: [Agent-04 流动模型建模师 完整输出文档 V2.3版.md](http://file/05b8fc3a-a8c7-44d4-a15c-91ce05fa76bc.md)

[^5]: [Agent-04 流动模型建模师 完整输出文档 V2.3版.md](http://file/05b8fc3a-a8c7-44d4-a15c-91ce05fa76bc.md)

[^6]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^1]: [Agent-02  空间本体建模师 (Space Ontology Architect).md](http://file/35de1547-3b35-4ab4-a98a-37fb6cf0b0b6.md)

[^2]: [Agent-02  空间本体建模师 (Space Ontology Architect).md](http://file/35de1547-3b35-4ab4-a98a-37fb6cf0b0b6.md)

[^3]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^4]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^5]: [# === AGENT-09: 统一CIM模型 ...on: “医用床塔管道疋 - 吊臂式供气供电+](# === AGENT-09: 统一CIM模型 ...on: “医用床塔管道疋 - 吊臂式供气供电+)

[^6]: [Agent-03 v2.2  设备本体建模师 (Equipment Ontology Architect) 完整输出.md](http://file/6c1c1929-d310-442c-8bd3-24228af83d28.md)

[^1]: [Agent-01 系统拓扑建模师 - 完整输出文档.md](http://file/fb792853-9410-4a6d-9389-5740af5b6fee.md)

[^2]: [Agent-01 系统拓扑建模师 - 完整输出文档.md](http://file/fb792853-9410-4a6d-9389-5740af5b6fee.md)

[^3]: [Agent-01 系统拓扑建模师 - 第二批次：电气系统 + 医疗气体系 （第三次修订版）.md](http://file/4cd17d72-bd32-43f9-a072-b383fd70c5fc.md)

[^4]: [Agent-01 系统拓扑建模师 - 第七批次：运维与实施深化文档.md](http://file/bbf66cdc-5298-4478-a2a0-e10ef0b38607.md)

[^5]: [# Agent-09: 统一交叉引用索引系统

[^6]: [Agent-01 系统拓扑建模师 - 完整输出文档.md](http://file/fb792853-9410-4a6d-9389-5740af5b6fee.md)

[^1]: [Agent-01 系统拓扑建模师 - 完整输出文档.md](http://file/fb792853-9410-4a6d-9389-5740af5b6fee.md)

[^2]: [Agent-01 系统拓扑建模师 - 第六批次：最终系统与综合集成.md](http://file/8b4c44db-7e14-4e27-9c8a-35285cf290c0.md)

[^3]: [Agent-01 系统拓扑建模师 - 第二批次：电气系统 + 医疗气体系 （第三次修订版）.md](http://file/4cd17d72-bd32-43f9-a072-b383fd70c5fc.md)

[^4]: [# Agent-09: 统一交叉引用索引系统

[^5]: [Agent-01 系统拓扑建模师 - 第二批次：电气系统 + 医疗气体系 （第三次修订版）.md](http://file/4cd17d72-bd32-43f9-a072-b383fd70c5fc.md)

[^6]: [Agent-01 系统拓扑建模师 - 第二批次：电气系统 + 医疗气体系 （第三次修订版）.md](http://file/4cd17d72-bd32-43f9-a072-b383fd70c5fc.md)

[^1]: [Agent-01 系统拓扑建模师 - 第四批次：消防系统 + 医疗专业系统.md](http://file/2f672527-5466-46d6-b255-27eed6ebc9e5.md)

[^2]: [Agent-01 系统拓扑建模师 - 第四批次：消防系统 + 医疗专业系统.md](http://file/2f672527-5466-46d6-b255-27eed6ebc9e5.md)

[^3]: [Agent-01 系统拓扑建模师 - 第四批次：消防系统 + 医疗专业系统.md](http://file/2f672527-5466-46d6-b255-27eed6ebc9e5.md)

[^4]: [Agent-01 系统拓扑建模师 - 第四批次：消防系统 + 医疗专业系统.md](http://file/2f672527-5466-46d6-b255-27eed6ebc9e5.md)

[^5]: [Agent-01 系统拓扑建模师 - 完整输出文档.md](http://file/fb792853-9410-4a6d-9389-5740af5b6fee.md)

[^6]: [Agent-01 系统拓扑建模师 - 第四批次：消防系统 + 医疗专业系统.md](http://file/2f672527-5466-46d6-b255-27eed6ebc9e5.md)
---