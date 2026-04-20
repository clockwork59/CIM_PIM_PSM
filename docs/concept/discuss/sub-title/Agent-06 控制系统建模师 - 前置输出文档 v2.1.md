## 🧑‍💻 User


这份任务指令书非常详尽且结构清晰，明确了 Agent-06 的角色定位、上下游依赖以及具体的输出规范。但作为技术评审，我仍有一些改进建议：

优点：

角色定位清晰：明确了 Agent-06 作为“执行者”和“架构师”的双重身份，强调了“业务定义意图，物理定义限制，控制实现目标”的核心理念。

依赖关系明确：清晰地列出了与 Agent-01、03、04、05 的依赖关系，确保了模型的一致性和连贯性。

输出规范具体：YAML 格式的输出规范定义了传感器、执行器、控制回路和序列模型的详细结构，便于后续的自动化生成和验证。

强调韧性设计：特别强调了“降级模式”和“边缘计算”，这对于医疗建筑这种高可靠性要求的场景至关重要。

分阶段实施：将任务分解为三个阶段，逐步推进，降低了实施难度。

改进建议：

1. 增强对 Agent-02 的引用：

虽然你在“上游依赖”中提到了 Agent-05，但 Agent-02（空间本体）对于控制策略的制定同样重要。例如：

空间类型（如手术室、ICU、普通病房）直接决定了控制精度和响应速度的要求。

运营场景（如手术中、消毒、非工作时间）直接影响控制模式的切换。

平疫结合是当前医疗建筑的重要需求，Agent-02 中定义的平疫转换逻辑需要在 Agent-06 中落地为具体的控制序列。

建议：在“上游依赖”中显式增加 Agent-02，并在“任务要求”中明确要求基于 Agent-02 的空间定义和场景模式来设计控制逻辑。

2. 细化“边缘计算架构”：

虽然提到了边缘计算，但目前的描述比较笼统。建议进一步明确：

边缘节点的定义：是 DDC、PLC 还是边缘网关？

边缘计算的能力：不仅是实时控制，还应包括本地数据缓存、简单的故障诊断和报警处理。

云边协同机制：云端下发优化参数，边缘上传状态数据，两者如何同步和交互。

3. 强化“物理实现”的约束：

虽然强调了“物理实现”，但在输出规范中还可以更具体一些。例如：

传感器安装位置：除了文本描述，是否可以引入坐标或相对位置的定义？

执行器特性：除了线性/等百分比，是否需要考虑死区、滞后等非线性特性？

通信协议：明确支持的通信协议（BACnet、Modbus、OPC UA 等），以及协议转换的逻辑。

4. 完善“降级模式”的定义：

目前的降级模式主要针对网络中断和传感器故障。建议增加对控制器故障和执行器故障的考虑：

控制器故障：当 DDC/PLC 宕机时，执行器应保持在什么状态？是否需要硬件级的联锁保护？

执行器故障：当阀门卡死或风机故障时，控制系统应如何响应？是报警停机还是切换备用设备？

5. 增加“验证与测试”环节：

控制系统的设计需要经过严格的验证和测试。建议在任务要求中增加：

仿真验证：利用 Agent-04 的物理模型进行控制逻辑的仿真验证。

硬件在环测试 (HIL)：如果有条件，可以进行 HIL 测试，验证控制系统与物理设备的兼容性。

总结：

这份任务指令书已经非常出色，只需在上述几个方面进行微调和补充，就能更好地指导 Agent-06 完成高质量的控制系统建模工作。特别是加强对 Agent-02 的引用，将使控制系统更加贴合医疗业务的实际需求。

---
## 🤖 Assistant


您的技术评审意见非常专业和中肯。我需要根据这5条改进建议，对白皮书进行修订和补充。让我先搜索知识库中关于Agent-02空间本体的相关内容。



我需要继续搜索更多关于Agent-02的空间运营场景、平疫转换等详细内容。



我需要继续搜索Agent-02中关于运营场景模式和空间环境要求的详细定义。



我需要继续搜索关于边缘计算架构和通信协议的详细内容。



现在我已经获取了足够的信息来根据技术评审意见修订白皮书。我将输出**白皮书修订版**，整合5条改进建议。

---

# 控制架构与降级策略白皮书（修订版）
## Agent-06 控制系统建模师 - 前置输出文档 v2.1

**版本**: v2.1 (修订版)
**日期**: 2025-01-XX
**状态**: 技术评审后修订发布
**修订说明**: 根据技术评审意见整合5项改进建议

---

## 修订说明

根据技术评审意见，本修订版在v2.0基础上进行了以下增强：

| 序号 | 改进建议 | 修订内容 | 章节 |
|------|----------|----------|------|
| 1 | 增强对Agent-02的引用 | 新增"空间-控制策略映射"章节，显式引用Agent-02空间本体和运营场景 | 第七章 |
| 2 | 细化边缘计算架构 | 细化边缘节点定义、云边协同机制 | 第二章(增强) |
| 3 | 强化物理实现约束 | 增加传感器安装位置规范、执行器非线性特性、通信协议规范 | 第八章 |
| 4 | 完善降级模式定义 | 增加控制器故障、执行器故障的降级策略 | 第五章(增强) |
| 5 | 增加验证与测试环节 | 新增仿真验证和HIL测试框架 | 第九章 |

---

## 摘要

本白皮书阐述医院建筑自动化控制系统在极端情况下的可用性保障策略。基于"分层自治、逐级降级、本质安全"的核心设计哲学，建立覆盖云端(L1)、边缘(L2)、硬件(L3)三级保障的韧性控制架构，确保在网络中断、传感器失效、控制器宕机、执行器故障等故障工况下，关键医疗区域（特别是手术室、ICU）仍能维持最低安全运行边界。

**v2.1新增**: 本版本显式引入Agent-02空间本体模型作为控制策略的业务输入，确保控制逻辑与医疗运营场景深度耦合；细化边缘计算架构与云边协同机制；完善控制器和执行器故障的降级策略；增加验证与测试框架。

---

## 第一章 设计哲学与原则

*(保持v2.0内容不变)*

### 1.1 核心格言

> **"业务定义意图，物理定义限制，控制实现目标。"**

### 1.2 三大设计原则

```yaml
Design_Principles:
  
  Principle_1:
    name: "关键回路本地化 (Critical Loop Localization)"
    description: |
      所有P0/P1级别的控制回路必须能够在完全断网条件下独立运行。
      边缘控制器(DDC/PLC)必须具备完整的本地控制逻辑，不依赖上位机。
  
  Principle_2:
    name: "故障安全设计 (Fail-Safe Design)"
    description: |
      每个执行器必须定义明确的失效安全位置(Fail-Safe Position)。
      传感器故障时必须有备用策略(物理备用或软测量)。
      控制器故障时执行器必须保持安全状态。
      执行器故障时必须有检测机制和替代方案。
  
  Principle_3:
    name: "渐进式降级 (Graceful Degradation)"
    description: |
      系统故障时不是"全开或全关"的二元选择，而是逐级降级：
      正常模式 → 节能模式 → 基础模式 → 安全模式 → 应急模式
```

### 1.3 上游依赖声明（v2.1增强）

```yaml
Upstream_Dependencies:
  
  Agent_01:
    name: "系统拓扑建模师"
    provides:
      - "8大系统26子系统156节点的拓扑结构"
      - "系统边界与接口定义"
      - "消防联动信号源(FIRE-FAS)"
    usage_in_Agent06:
      - "控制点位与系统节点的映射"
      - "消防联动矩阵的信号来源"
      - "系统间联锁关系"
  
  Agent_02:
    name: "空间本体建模师"
    provides:
      - "空间层级模型(L0-L5)"
      - "空间分类体系(手术室/ICU/隔离病房等)"
      - "环境需求参数(温度/湿度/压力/换气次数)"
      - "运营场景模式(手术中/消毒/值班/平疫转换)"
      - "设备配置与末端位置"
    usage_in_Agent06:
      - "控制目标设定值来源"
      - "控制精度与响应速度要求"
      - "运行模式切换逻辑"
      - "平疫转换控制序列"
    critical_interfaces:
      - "get_environmental_requirements(space_id)"
      - "get_operation_modes(space_id)"
      - "get_conversion_procedures(source_type, target_type)"
  
  Agent_03:
    name: "设备本体建模师"
    provides:
      - "123种设备类型的本体模型"
      - "设备控制属性与联锁关系"
      - "设备通信协议与接口"
    usage_in_Agent06:
      - "传感器与执行器的选型规格"
      - "设备联锁逻辑设计"
      - "设备通信配置"
  
  Agent_04:
    name: "流动模型建模师"
    provides:
      - "FlowSequence流动模型"
      - "物理方程(热力学/流体力学)"
      - "载体-荷载耦合关系"
    usage_in_Agent06:
      - "控制算法的物理基础"
      - "软测量算法的理论支撑"
      - "仿真验证的物理模型"
  
  Agent_05:
    name: "耦合关系建模师"
    provides:
      - "CouplingUnit耦合单元定义"
      - "Criticality可靠性等级"
      - "系统-空间耦合关系"
    usage_in_Agent06:
      - "控制优先级确定"
      - "冗余配置需求"
      - "降级策略设计"
```

---

## 第二章 三级控制保障架构（v2.1增强）

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
                            ┌────────▼────────┐
                            │   边缘网关层    │  ← v2.1新增
                            │  Edge Gateway   │
                            └────────┬────────┘
                                     │
┌────────────────────────────────────┼────────────────────────────────────────┐
│                              L2: 边缘控制器层                                │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         DDC/PLC 控制器集群                           │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │   │
│  │  │ DDC-OR  │  │ DDC-ICU │  │ DDC-CHP │  │ DDC-AHU │  │ PLC-FAS │   │   │
│  │  │ 手术室  │  │ 重症室  │  │ 冷热源  │  │ 空调机组 │  │ 消防    │   │   │
│  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘   │   │
│  └───────┴────────────┴────────────┴────────────┴────────────┴─────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
┌────────────────────────────────────┼────────────────────────────────────────┐
│                              L3: 硬件保护层                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  机械恒温器  │  │   防冻开关   │  │  防火阀熔断  │  │ 压差安全阀   │    │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 边缘计算架构（v2.1新增细化）

```yaml
Edge_Computing_Architecture:
  
  # ═══════════════════════════════════════════════════════════════
  # 边缘节点定义
  # ═══════════════════════════════════════════════════════════════
  
  edge_node_types:
    
    type_1_edge_gateway:
      name: "边缘网关 (Edge Gateway)"
      role: "云边协同核心节点"
      deployment: "每栋建筑1-2台"
      capabilities:
        compute:
          - "本地数据缓存 (≥7天历史数据)"
          - "协议转换 (BACnet ↔ MQTT/HTTP)"
          - "数据预处理与压缩"
          - "简单故障诊断算法"
          - "本地报警处理与通知"
        storage:
          type: "SSD"
          capacity: "≥256GB"
          retention: "7天完整数据 + 90天关键数据"
        communication:
          uplink: "以太网/4G/5G to Cloud"
          downlink: "BACnet/IP to NAC/DDC"
        resilience:
          offline_mode: "支持72小时独立运行"
          data_sync: "网络恢复后自动同步"
      hardware_spec:
        processor: "ARM Cortex-A72 或 x86"
        memory: "≥4GB RAM"
        os: "Linux-based RTOS"
        power: "24VDC, 冗余电源"
        environment: "工业级 -20°C to +60°C"
    
    type_2_nac:
      name: "网络自动化控制器 (NAC)"
      role: "区域控制管理"
      deployment: "每楼层或每区域1台"
      capabilities:
        compute:
          - "DDC程序下载/管理"
          - "趋势数据汇总"
          - "区域报警处理"
          - "区域时间程序"
          - "断网独立运行"
        managed_ddcs: "10-30台"
        communication:
          uplink: "BACnet/IP to Gateway"
          downlink: "BACnet/IP 或 MS/TP to DDC"
    
    type_3_ddc:
      name: "直接数字控制器 (DDC)"
      role: "末端实时控制"
      deployment: "每系统/每区域"
      capabilities:
        control:
          - "PID控制算法"
          - "顺序控制逻辑"
          - "联锁保护"
          - "本地时间程序"
        io_points:
          ai: "8-16点"
          ao: "4-8点"
          di: "8-16点"
          do: "8-16点"
        communication:
          protocol: "BACnet MS/TP 或 IP"
          baud_rate: "76800 bps"
        resilience:
          standalone: "断网不影响控制"
          program_retention: "掉电保持"
          battery_backup: "≥72小时 RTC"
    
    type_4_plc:
      name: "可编程逻辑控制器 (PLC)"
      role: "高可靠性安全控制"
      deployment: "消防联动/冷站群控/应急系统"
      capabilities:
        control:
          - "硬实时控制 (<10ms)"
          - "安全联锁 (SIL2/SIL3)"
          - "冗余配置 (热备)"
        communication:
          protocol: "Modbus RTU/TCP, Profinet"
        resilience:
          redundancy: "CPU热备/IO冗余"
          safety_rating: "SIL2/SIL3"
  
  # ═══════════════════════════════════════════════════════════════
  # 云边协同机制
  # ═══════════════════════════════════════════════════════════════
  
  cloud_edge_collaboration:
    
    data_flow_uplink:
      name: "边缘→云端数据流"
      content:
        realtime:
          data: "关键状态量/报警"
          interval: "1-5秒"
          protocol: "MQTT QoS1"
        periodic:
          data: "趋势数据/统计值"
          interval: "1-15分钟"
          protocol: "MQTT QoS0 或 HTTP"
        event:
          data: "报警/状态变化"
          trigger: "事件驱动"
          protocol: "MQTT QoS2"
      compression:
        method: "死区压缩 + LZ4"
        ratio: "典型5:1"
    
    data_flow_downlink:
      name: "云端→边缘数据流"
      content:
        setpoint_optimization:
          data: "优化后的设定值"
          example: "冷冻水温度优化值"
          frequency: "5-15分钟"
        schedule_update:
          data: "时间表/模式切换"
          frequency: "按需"
        parameter_tuning:
          data: "PID参数/报警阈值"
          frequency: "低频"
        firmware_update:
          data: "控制器程序更新"
          frequency: "维护窗口"
    
    synchronization:
      time_sync:
        protocol: "NTP/SNTP"
        accuracy: "±100ms"
        source: "云端NTP服务器 → 边缘网关 → DDC"
      data_sync:
        offline_handling:
          edge_action: "本地缓存所有数据"
          cloud_action: "标记离线期间"
          recovery: "网络恢复后增量同步"
          conflict_resolution: "边缘数据优先（实测值）"
    
    failover_mechanism:
      cloud_unavailable:
        detection: "心跳超时30秒"
        edge_response:
          - "切换到本地默认设定值"
          - "继续本地控制逻辑"
          - "本地报警通知（短信/声光）"
          - "缓存所有数据"
        display: "HMI显示'云端离线'"
      edge_gateway_unavailable:
        detection: "NAC/DDC检测网关离线"
        nac_response:
          - "独立运行"
          - "点对点通信"
          - "本地存储数据"
        cloud_response: "标记该区域离线"
  
  # ═══════════════════════════════════════════════════════════════
  # 通信协议栈（v2.1新增）
  # ═══════════════════════════════════════════════════════════════
  
  communication_protocol_stack:
    
    layer_1_cloud:
      protocols:
        - name: "MQTT"
          usage: "遥测数据上传"
          broker: "云端MQTT Broker"
          topics:
            telemetry: "building/{id}/telemetry/{point}"
            alarm: "building/{id}/alarm/{level}"
            command: "building/{id}/command/{device}"
          qos:
            telemetry: "QoS0/QoS1"
            alarm: "QoS2"
            command: "QoS1"
        - name: "HTTP/REST"
          usage: "配置管理/历史查询"
          security: "HTTPS + OAuth2"
        - name: "OPC UA"
          usage: "与IT系统集成"
          security: "SignAndEncrypt"
    
    layer_2_building:
      protocols:
        - name: "BACnet/IP"
          usage: "主控制器间通讯"
          port: "47808 (0xBAC0)"
          bbmd: "每栋建筑1台"
          services:
            - "ReadProperty / WriteProperty"
            - "SubscribeCOV"
            - "ConfirmedEventNotification"
            - "WhoIs / IAm"
    
    layer_3_field:
      protocols:
        - name: "BACnet MS/TP"
          usage: "末端控制器通讯"
          baud_rate: "76800 bps"
          cable: "屏蔽双绞线 RVSP 2×0.75"
          max_length: "1200m"
          termination: "120Ω at both ends"
        - name: "Modbus RTU"
          usage: "第三方设备/电表"
          baud_rate: "9600/19200"
          parity: "Even"
        - name: "硬接点"
          usage: "消防联动/安全联锁"
          type: "干接点/有源接点"
          voltage: "24VDC"
    
    protocol_conversion:
      location: "边缘网关"
      conversions:
        - from: "BACnet/IP"
          to: "MQTT"
          direction: "双向"
        - from: "Modbus TCP"
          to: "BACnet/IP"
          direction: "双向"
        - from: "BACnet/IP"
          to: "OPC UA"
          direction: "只读"
```

---

## 第三章 手术室三级控制保障

*(保持v2.0内容)*

---

## 第四章 冷站群控逻辑

*(保持v2.0内容)*

---

## 第五章 安全与降级策略（v2.1增强）

### 5.1 消防联动矩阵

*(保持v2.0内容)*

### 5.2 断网/传感器故障对策

*(保持v2.0内容)*

### 5.3 控制器故障对策（v2.1新增）

```yaml
Controller_Failure_Strategies:
  
  # ═══════════════════════════════════════════════════════════════
  # DDC控制器故障
  # ═══════════════════════════════════════════════════════════════
  
  ddc_failure:
    
    failure_modes:
      - mode: "DDC完全宕机"
        cause: ["电源故障", "硬件损坏", "程序死循环"]
        detection:
          method: "心跳超时"
          timeout: "60秒"
          detector: "NAC/边缘网关"
        
      - mode: "DDC通信中断"
        cause: ["网线断开", "端口故障", "地址冲突"]
        detection:
          method: "通信超时"
          timeout: "30秒"
        
      - mode: "DDC程序异常"
        cause: ["逻辑错误", "数据溢出"]
        detection:
          method: "输出值异常检测"
          criteria: "输出值超出合理范围持续5分钟"
    
    response_by_area:
      
      operating_room:
        controller: "DDC-OR-xxx"
        criticality: "P0-LIFE_SAFETY"
        
        immediate_response:
          - action: "执行器保持最后位置(HOLD_LAST)"
            duration: "15分钟"
            applicable: ["阀门", "变频器"]
          - action: "风机保持运行"
            mechanism: "接触器自保持"
          - action: "L3硬件保护激活"
            details:
              - "机械恒温器接管温度控制"
              - "防冻开关保护盘管"
          - action: "报警通知"
            recipients: ["中控室", "设备科", "护士站"]
            method: ["界面弹窗", "短信", "声光"]
        
        extended_response:
          trigger: "故障持续>15分钟"
          actions:
            - "执行器切换到安全位置(FAIL_SAFE)"
            - "送风阀: 保持最后位置或全开"
            - "排风阀: 30%固定开度(维持正压)"
            - "冷水阀: 50%开度(防止过热)"
            - "热水阀: 弹簧复位开启(冬季防冻)"
        
        manual_intervention:
          - "现场手动模式切换"
          - "本地HMI操作(如可用)"
          - "备用控制器接管(如配置)"
        
        recovery:
          - "控制器自动重启尝试(3次)"
          - "加载保存的运行参数"
          - "30秒内恢复自动控制"
          - "记录故障日志"
      
      chiller_plant:
        controller: "DDC-CHP-001"
        criticality: "P1-MISSION_CRITICAL"
        
        immediate_response:
          - action: "冷机保持当前状态"
            mechanism: "本地控制面板独立运行"
          - action: "禁止自动加减机"
          - action: "水泵保持运行"
          - action: "冷却塔风机保持当前频率"
        
        extended_response:
          trigger: "故障持续>30分钟"
          actions:
            - "逐台手动检查冷机运行状态"
            - "必要时人工现场操作"
        
        redundancy_option:
          - "热备DDC自动接管(推荐配置)"
          - "切换时间<10秒"
      
      general_ahu:
        controller: "DDC-AHU-xxx"
        criticality: "P2-IMPORTANT"
        
        response:
          - "执行器保持最后位置"
          - "按时间表判断是否应运行"
          - "非工作时间可接受停机"
    
    hardware_interlock_backup:
      description: "当DDC失效时，硬件联锁仍然有效"
      examples:
        - interlock: "防冻保护"
          mechanism: "防冻开关直接控制热水阀"
          independent_of: "DDC"
        - interlock: "消防联动"
          mechanism: "FAS硬接点直接控制接触器"
          independent_of: "DDC"
        - interlock: "过载保护"
          mechanism: "热继电器直接断开电机"
          independent_of: "DDC"
  
  # ═══════════════════════════════════════════════════════════════
  # NAC/边缘网关故障
  # ═══════════════════════════════════════════════════════════════
  
  nac_gateway_failure:
    
    nac_failure:
      impact: "该区域DDC无法被上位机访问"
      ddc_behavior:
        - "所有DDC继续独立运行"
        - "DDC间P2P通信仍可用(如配置)"
        - "本地控制逻辑不受影响"
      workaround:
        - "直接通过笔记本连接DDC"
        - "使用备用NAC(如配置)"
    
    edge_gateway_failure:
      impact: "该建筑与云端断开"
      local_behavior:
        - "NAC继续管理DDC"
        - "本地报警仍可处理"
        - "数据本地缓存"
      cloud_behavior:
        - "标记该建筑离线"
        - "历史数据出现间隙"
      recovery:
        - "网关重启/更换"
        - "数据增量同步"
  
  # ═══════════════════════════════════════════════════════════════
  # PLC控制器故障
  # ═══════════════════════════════════════════════════════════════
  
  plc_failure:
    
    fire_plc:
      controller: "PLC-FAS"
      criticality: "P0-LIFE_SAFETY"
      redundancy: "必须配置热备"
      failover_time: "<1秒"
      backup_mechanism:
        - "双CPU热备，自动切换"
        - "IO模块独立，不受CPU切换影响"
        - "硬接点联动独立于PLC逻辑"
    
    chiller_plc:
      controller: "PLC-CHP (如使用)"
      redundancy: "推荐热备"
      failover_time: "<10秒"
      fallback:
        - "冷机本地控制面板可独立运行"
        - "人工现场操作作为最终后备"
```

### 5.4 执行器故障对策（v2.1新增）

```yaml
Actuator_Failure_Strategies:
  
  # ═══════════════════════════════════════════════════════════════
  # 执行器故障类型与检测
  # ═══════════════════════════════════════════════════════════════
  
  failure_types:
    
    valve_failures:
      - type: "阀门卡死(Stuck)"
        cause: ["机械卡涩", "执行器损坏", "异物阻塞"]
        detection:
          method: "指令-反馈偏差"
          criteria: |
            |Command - Feedback| > 10% 持续 5分钟
            AND 指令有变化
          sensor: "阀位反馈传感器"
        
      - type: "阀门关不严(Leakage)"
        cause: ["密封老化", "阀芯磨损"]
        detection:
          method: "下游温度异常"
          criteria: |
            阀门指令=0% 但 下游温度变化
          
      - type: "执行器失电"
        cause: ["电源故障", "线路断开"]
        detection:
          method: "反馈信号丢失"
          behavior: "弹簧复位到安全位置"
    
    damper_failures:
      - type: "风阀卡死"
        detection:
          method: "指令-反馈偏差"
          criteria: "|Command - Feedback| > 15%"
      - type: "执行器脱落"
        detection:
          method: "反馈值突变到0或100%"
    
    fan_failures:
      - type: "风机故障停机"
        cause: ["电机烧毁", "轴承损坏", "过载保护"]
        detection:
          method: "运行状态反馈"
          sensors: ["电流互感器", "运行反馈触点"]
      - type: "VFD故障"
        detection:
          method: "VFD故障码读取"
          protocol: "Modbus/BACnet"
    
    pump_failures:
      - type: "水泵故障"
        detection:
          - "运行状态反馈"
          - "电流异常"
          - "出口压力/流量异常"
      - type: "干转保护"
        detection: "运行但流量=0持续30秒"
        action: "立即停泵"
  
  # ═══════════════════════════════════════════════════════════════
  # 执行器故障响应策略
  # ═══════════════════════════════════════════════════════════════
  
  response_strategies:
    
    valve_stuck:
      scenario: "控制阀卡死无法调节"
      
      chw_valve_stuck_open:
        impact: "持续供冷，可能过冷"
        response:
          immediate:
            - "报警: HIGH"
            - "尝试多次开关动作(3次)"
          if_still_stuck:
            - "调节送风量补偿(降低风量减少冷量)"
            - "如有备用盘管，切换使用"
            - "派维修工单"
          workaround: "通过送风温度设定值补偿"
      
      chw_valve_stuck_closed:
        impact: "无法供冷，温度上升"
        response:
          immediate:
            - "报警: CRITICAL"
            - "尝试多次开关动作"
          if_still_stuck:
            - "增加送风量(如可能)"
            - "启用备用机组(如有)"
            - "降低室内热负荷(非必要设备关闭)"
            - "手动打开阀门(现场)"
          for_operating_room: "评估是否需要暂停手术"
      
      hw_valve_stuck_closed:
        impact: "无法供热，冬季有冻裂风险"
        response:
          immediate:
            - "报警: CRITICAL"
            - "关闭新风阀减少热负荷"
          if_still_stuck:
            - "L3防冻开关接管"
            - "手动打开阀门"
    
    fan_failure:
      scenario: "送风机故障停机"
      
      or_supply_fan_failure:
        impact: "手术室失去正压和洁净度"
        response:
          immediate:
            - "报警: EMERGENCY"
            - "停止排风机(保持正压)"
            - "关闭新风阀"
            - "通知手术室护士站"
          decision:
            ongoing_surgery: "评估是否继续（由医生决定）"
            no_surgery: "禁止新手术安排"
          recovery:
            - "切换到备用风机(如配置)"
            - "紧急维修"
      
      general_ahu_fan_failure:
        impact: "该区域无空调"
        response:
          - "报警: HIGH"
          - "关闭该AHU所有阀门"
          - "检查是否有备用"
          - "派维修工单"
    
    pump_failure:
      scenario: "冷冻水泵故障"
      
      primary_pump_failure:
        impact: "对应冷机无法运行"
        response:
          - "停止对应冷机"
          - "其他冷机继续运行"
          - "系统容量下降"
      
      secondary_pump_failure:
        impact: "冷冻水输配能力下降"
        response:
          - "其他泵增速补偿(如有余量)"
          - "如负荷超过能力，按优先级限制末端"
  
  # ═══════════════════════════════════════════════════════════════
  # 执行器冗余配置
  # ═══════════════════════════════════════════════════════════════
  
  redundancy_configuration:
    
    critical_areas:
      operating_room:
        supply_fan: "N+1 (一用一备或双风机)"
        chw_valve: "可考虑旁通阀"
        pressure_control: "双排风阀独立控制"
      
      icu:
        supply_fan: "N+1"
        isolation_damper: "独立控制"
      
      chiller_plant:
        chillers: "N+1"
        pumps: "N+1"
        cooling_towers: "N+1"
    
    non_critical_areas:
      general_ward: "按需，无强制冗余"
      office: "无冗余要求"
```

---

## 第六章 总结与实施建议

*(保持v2.0内容，增加新章节引用)*

---

## 第七章 空间-控制策略映射（v2.1新增）

本章显式引用Agent-02空间本体模型，将空间类型和运营场景映射到控制策略。

```yaml
Space_Control_Mapping:
  
  # ═══════════════════════════════════════════════════════════════
  # 空间类型与控制精度要求
  # ═══════════════════════════════════════════════════════════════
  
  space_type_control_requirements:
    
    operating_room:
      space_ref: "Agent-02.MedicalSpaces.OperatingRoom"
      space_code: "OR"
      cleanliness_classes: ["I级", "II级", "III级", "IV级"]
      
      control_precision:
        temperature:
          setpoint_range: "21-27°C"
          default_setpoint: "22°C"
          tolerance: "±1°C"
          response_time: "<15分钟 达到设定值"
          control_algorithm: "Cascade PID"
        humidity:
          setpoint_range: "40-60%RH"
          default_setpoint: "50%RH"
          tolerance: "±5%RH"
          response_time: "<30分钟"
          control_algorithm: "PID with limits"
        pressure:
          setpoint: "+15Pa (vs corridor)"
          tolerance: "±3Pa"
          response_time: "<30秒"
          control_algorithm: "Fast PI"
          critical: true
        air_changes:
          class_I: "≥36 ACH"
          class_II: "≥24 ACH"
          class_III: "≥18 ACH"
      
      control_priority: "P0-LIFE_SAFETY"
      sensor_redundancy: "必须"
      local_override: "必须"
    
    icu:
      space_ref: "Agent-02.MedicalSpaces.ICU"
      space_code: "ICU"
      
      control_precision:
        temperature:
          setpoint_range: "22-26°C"
          default_setpoint: "24°C"
          tolerance: "±1°C"
        humidity:
          setpoint_range: "40-60%RH"
          tolerance: "±5%RH"
        pressure:
          setpoint: "+10Pa"
          tolerance: "±3Pa"
      
      control_priority: "P0-LIFE_SAFETY"
      sensor_redundancy: "推荐"
    
    negative_pressure_isolation:
      space_ref: "Agent-02.MedicalSpaces.IsolationRoom"
      space_code: "ISO-NEG"
      
      control_precision:
        temperature:
          setpoint_range: "22-26°C"
          tolerance: "±1°C"
        pressure:
          setpoint: "-10Pa (vs corridor)"
          tolerance: "±2Pa"
          critical: true
          note: "负压防止病原体外泄"
        air_changes: "≥12 ACH, 100%新风"
      
      control_priority: "P0-LIFE_SAFETY"
      special_requirements:
        - "独立排风系统"
        - "HEPA过滤排放"
        - "压差连续监测"
    
    general_ward:
      space_ref: "Agent-02.MedicalSpaces.Ward"
      space_code: "WARD"
      
      control_precision:
        temperature:
          setpoint_range: "22-26°C"
          tolerance: "±2°C"
        humidity:
          range: "40-65%RH"
          tolerance: "±10%RH"
      
      control_priority: "P2-IMPORTANT"
      sensor_redundancy: "不要求"
    
    office_admin:
      space_ref: "Agent-02.GeneralSpaces.Office"
      space_code: "OFC"
      
      control_precision:
        temperature:
          setpoint_range: "20-26°C"
          tolerance: "±2°C"
      
      control_priority: "P3-NORMAL"
  
  # ═══════════════════════════════════════════════════════════════
  # 运营场景与控制模式映射
  # ═══════════════════════════════════════════════════════════════
  
  operation_mode_mapping:
    
    operating_room_modes:
      ref: "Agent-02.OperationalScenarios.OperatingRoom"
      
      modes:
        - mode_id: "OR_MODE_SURGERY"
          name: "手术模式"
          trigger: "手术排程 或 手动启动"
          duration: "手术开始前30分钟 → 手术结束后15分钟"
          control_setpoints:
            temperature: "22°C (可调21-27°C)"
            humidity: "50%RH"
            pressure: "+15Pa"
            air_changes: "按洁净等级"
            fresh_air_ratio: "100%"
          control_behavior:
            - "全速运行"
            - "严格压差控制"
            - "连续洁净度监测"
        
        - mode_id: "OR_MODE_STANDBY"
          name: "值班模式"
          trigger: "手术结束后15分钟 且 无后续排程"
          control_setpoints:
            temperature: "24°C"
            humidity: "不控制"
            pressure: "+8Pa (降低)"
            air_changes: "50%设计值"
          control_behavior:
            - "低速运行"
            - "节能为主"
            - "保持基本正压"
          energy_saving: "约40%"
        
        - mode_id: "OR_MODE_DISINFECTION"
          name: "消毒模式"
          trigger: "手动启动 或 定时程序"
          duration: "30-60分钟"
          control_setpoints:
            temperature: "不控制"
            pressure: "0Pa (封闭)"
            fresh_air: "0% (全封闭)"
          control_behavior:
            - "关闭新风阀"
            - "关闭排风阀"
            - "启动紫外线/臭氧消毒"
            - "消毒完成后强排换气"
        
        - mode_id: "OR_MODE_OFF"
          name: "关闭模式"
          trigger: "非工作时间 且 无排程"
          control_setpoints:
            all_systems: "停止"
          note: "仅限于非关键手术室"
    
    icu_modes:
      ref: "Agent-02.OperationalScenarios.ICU"
      
      modes:
        - mode_id: "ICU_MODE_NORMAL"
          name: "正常模式"
          control_setpoints:
            temperature: "24°C"
            humidity: "50%RH"
            pressure: "+10Pa"
          features: "24小时连续运行"
        
        - mode_id: "ICU_MODE_ISOLATION"
          name: "隔离模式"
          trigger: "感染患者入住"
          control_setpoints:
            pressure: "-5Pa (切换为负压)"
            fresh_air: "100%"
          control_behavior:
            - "切换压差控制方向"
            - "增加换气次数"
            - "启动HEPA排风"
  
  # ═══════════════════════════════════════════════════════════════
  # 平疫转换控制序列（v2.1新增）
  # ═══════════════════════════════════════════════════════════════
  
  pandemic_conversion_sequences:
    ref: "Agent-02.PandemicConversion"
    
    ward_to_isolation_conversion:
      name: "普通病房→负压隔离病房转换"
      trigger: "疫情响应指令"
      
      pre_conditions:
        - "病房已疏散患者"
        - "预留负压系统已安装"
        - "工程人员就位"
      
      conversion_sequence:
        - step: 1
          name: "系统准备"
          duration: "30分钟"
          actions:
            - "停止原空调系统"
            - "关闭回风阀"
            - "检查负压排风系统"
        
        - step: 2
          name: "管路切换"
          duration: "2小时"
          actions:
            - "接通预留负压排风接口"
            - "安装HEPA过滤器"
            - "封堵非必要开口"
          manual_work: true
        
        - step: 3
          name: "控制切换"
          duration: "30分钟"
          actions:
            - "DDC程序切换到负压模式"
            - "压差设定值: +10Pa → -10Pa"
            - "排风量增加到设计值"
            - "新风改为100%"
          ddc_operation:
            - command: "WRITE Mode = ISOLATION"
            - command: "WRITE Pressure_SP = -10"
        
        - step: 4
          name: "验证测试"
          duration: "1小时"
          actions:
            - "烟雾测试确认气流方向"
            - "压差稳定性测试(±2Pa)"
            - "密封性检查"
          acceptance_criteria:
            pressure_differential: "-10Pa ±2Pa"
            airflow_direction: "从走廊流向病房"
        
        - step: 5
          name: "投入使用"
          actions:
            - "记录转换完成"
            - "通知医护人员"
            - "启动持续监测"
      
      total_time: "约4小时"
      
      recovery_sequence:
        name: "隔离病房→普通病房恢复"
        steps:
          - "终末消毒"
          - "拆除临时设施"
          - "DDC程序切回正常模式"
          - "环境验收"
        total_time: "约8小时"
    
    fever_clinic_activation:
      name: "发热门诊启用"
      ref: "Agent-02.EmergencyAreas.FeverClinic"
      
      design_basis:
        pre_installed:
          - "独立空调系统"
          - "负压控制系统"
          - "独立排风（HEPA过滤）"
        activation_time: "<2小时"
      
      activation_sequence:
        - step: 1
          actions:
            - "启动独立空调机组"
            - "启动负压排风机"
        - step: 2
          actions:
            - "确认负压建立(-5Pa)"
            - "确认气流方向正确"
        - step: 3
          actions:
            - "开放就诊区域"
```

---

## 第八章 物理实现约束规范（v2.1新增）

```yaml
Physical_Implementation_Constraints:
  
  # ═══════════════════════════════════════════════════════════════
  # 传感器安装位置规范
  # ═══════════════════════════════════════════════════════════════
  
  sensor_installation_standards:
    
    room_temperature_sensor:
      type: "室内温度传感器"
      
      location_requirements:
        height: "1.5m (距地)"
        wall_distance: "≥0.3m (距墙)"
        avoid:
          - "直射阳光"
          - "空调出风口直吹"
          - "发热设备附近"
          - "门窗附近气流干扰"
        recommended_wall: "内墙，避免外墙"
      
      operating_room_specific:
        location: "非手术区墙面"
        avoid: "层流送风区正下方"
        mounting: "嵌入式，防碰撞"
      
      coordinate_reference:
        format: "(X, Y, Z) 相对于房间原点"
        origin: "房间左下角地面"
        example:
          room_size: "6m × 5m × 3m"
          sensor_position: "(0.3, 2.5, 1.5)"
          meaning: "距左墙0.3m，距前墙2.5m，高1.5m"
    
    duct_temperature_sensor:
      type: "风管温度传感器"
      
      location_requirements:
        downstream_distance: "≥10倍管径(直管段)"
        upstream_distance: "≥3倍管径"
        insertion_depth: "1/3管径"
        orientation: "逆流方向倾斜15°"
      
      for_supply_air:
        position: "送风机出口 或 HEPA前"
        purpose: "控制送风温度"
      
      for_return_air:
        position: "回风口内 或 回风管"
        purpose: "监测室内热负荷"
      
      for_mixed_air:
        position: "新风与回风混合后2m"
        purpose: "防冻保护"
    
    pressure_differential_sensor:
      type: "压差传感器"
      
      location_requirements:
        high_port: "被测空间(正压侧)"
        low_port: "参考空间(走廊)"
        tubing:
          material: "铜管或硬塑料管"
          length: "<15m"
          slope: "向传感器倾斜(防冷凝水)"
        sampling_point:
          avoid: "门缝附近(气流扰动)"
          height: "1.5-2.0m"
      
      operating_room_specific:
        reference: "洁净走廊"
        redundancy: "双传感器"
        display: "门口压差显示器"
    
    flow_sensor:
      type: "风量传感器"
      
      location_requirements:
        upstream_straight: "≥7.5倍管径"
        downstream_straight: "≥3倍管径"
        method:
          - name: "皮托管阵列"
            accuracy: "±3%"
            suitable: "大管径"
          - name: "热式风速"
            accuracy: "±5%"
            suitable: "小管径"
  
  # ═══════════════════════════════════════════════════════════════
  # 执行器特性规范
  # ═══════════════════════════════════════════════════════════════
  
  actuator_characteristics:
    
    control_valve:
      
      characteristic_curves:
        - type: "等百分比 (Equal Percentage)"
          application: "温度控制、大范围调节"
          behavior: "小开度时流量变化小，大开度时变化大"
          suitable_for: ["冷水阀", "热水阀"]
        
        - type: "线性 (Linear)"
          application: "流量控制、压差恒定场景"
          behavior: "开度与流量成正比"
          suitable_for: ["旁通阀", "定压差系统"]
        
        - type: "快开 (Quick Opening)"
          application: "开关控制"
          behavior: "小开度即有大流量"
          suitable_for: ["电磁阀", "安全阀"]
      
      non_linear_considerations:
        dead_band:
          definition: "阀门开始动作的最小信号变化"
          typical_value: "1-3%"
          control_impact: "PID输出<死区时无响应"
          compensation: "增加积分作用"
        
        hysteresis:
          definition: "正向与反向行程的偏差"
          typical_value: "1-2%"
          control_impact: "正反向控制精度不一致"
          compensation: "位置反馈闭环"
        
        stiction:
          definition: "静摩擦导致的卡滞"
          typical_value: "阀门老化后增加"
          detection: "周期性抖动测试"
          maintenance: "定期润滑"
        
        response_time:
          definition: "从0%到100%的全行程时间"
          typical_value:
            small_valve: "30-60秒"
            large_valve: "60-120秒"
          control_impact: "快速扰动响应受限"
      
      fail_safe_position:
        mechanism:
          spring_return: "弹簧复位"
          capacitor_drive: "电容驱动"
        positions:
          CHW_valve: "CLOSE (防止过冷)"
          HW_valve: "OPEN (防冻)"
          Steam_valve: "CLOSE (安全)"
    
    damper_actuator:
      
      characteristics:
        non_linearity:
          description: "风阀开度与风量非线性关系"
          curve: "S形曲线"
          compensation: "分段线性化或查表"
        
        leakage:
          closed_position: "0.5-3% 泄漏"
          impact: "最小新风量控制精度"
      
      fail_safe_position:
        OA_damper: "CLOSE (防冻、防雨)"
        RA_damper: "OPEN (保持送风)"
        EA_damper: "按设计确定"
        Fire_damper: "CLOSE (机械熔断)"
    
    vfd_characteristics:
      
      speed_range:
        min: "20-30% (取决于电机)"
        max: "100% (或超频110%)"
        note: "低于最小频率电机过热"
      
      response_time:
        acceleration: "5-30秒 (可调)"
        deceleration: "5-30秒 (可调)"
        control_impact: "快速负荷变化响应受限"
      
      harmonics:
        issue: "变频器产生谐波"
        mitigation: "进线电抗器、谐波滤波器"
  
  # ═══════════════════════════════════════════════════════════════
  # 通信协议详细规范
  # ═══════════════════════════════════════════════════════════════
  
  communication_protocol_specs:
    
    bacnet_ip:
      standard: "ASHRAE 135-2020"
      port: "47808 (UDP)"
      addressing:
        device_id: "唯一，0-4194302"
        network: "0-65534"
      object_types_used:
        - "AI (Analog Input) - 传感器"
        - "AO (Analog Output) - 模拟量输出"
        - "AV (Analog Value) - 设定值/参数"
        - "BI (Binary Input) - 状态输入"
        - "BO (Binary Output) - 指令输出"
        - "BV (Binary Value) - 逻辑值"
        - "MSV (Multi-State Value) - 模式"
        - "Schedule - 时间表"
        - "TrendLog - 趋势记录"
      services_required:
        mandatory: ["ReadProperty", "WriteProperty", "WhoIs", "IAm"]
        recommended: ["SubscribeCOV", "ReadPropertyMultiple"]
      
    bacnet_mstp:
      standard: "ASHRAE 135-2020"
      baud_rate: "76800 bps (recommended)"
      wiring:
        cable: "屏蔽双绞线 RVSP 2×0.75"
        topology: "菊花链"
        max_length: "1200m"
        stub_length: "<1.5m"
        termination: "120Ω at both ends"
      addressing:
        mac: "0-127"
        master: "0-127"
        max_master: "127"
      
    modbus_rtu:
      standard: "Modbus.org specification"
      baud_rate: "9600 或 19200"
      parity: "Even (偶校验)"
      data_bits: "8"
      stop_bits: "1"
      addressing:
        slave_id: "1-247"
      function_codes:
        - "03: Read Holding Registers"
        - "04: Read Input Registers"
        - "06: Write Single Register"
        - "16: Write Multiple Registers"
      wiring:
        cable: "屏蔽双绞线"
        termination: "120Ω"
      
    modbus_tcp:
      port: "502"
      unit_id: "1-247"
      timeout: "1000ms"
      retries: "3"
    
    hardwired_points:
      fire_interlock:
        signal_type: "干接点 或 有源24VDC"
        wiring: "独立电缆，不共用护套"
        supervision: "开路/短路监测(可选)"
      
      safety_interlock:
        signal_type: "干接点"
        configuration: "常开或常闭(按安全设计)"
        example:
          freeze_stat: "常闭，低温时断开"
          smoke_detector: "常开，报警时闭合"
```

---

## 第九章 验证与测试框架（v2.1新增）

```yaml
Verification_Testing_Framework:
  
  # ═══════════════════════════════════════════════════════════════
  # 仿真验证（利用Agent-04物理模型）
  # ═══════════════════════════════════════════════════════════════
  
  simulation_verification:
    
    purpose: |
      在实际实施前，利用Agent-04的物理模型验证控制逻辑的正确性和稳定性。
    
    simulation_platform:
      options:
        - name: "MATLAB/Simulink"
          usage: "控制算法开发与验证"
          components: ["PID调参", "状态机仿真", "故障注入"]
        - name: "EnergyPlus + Python"
          usage: "建筑能耗与环境仿真"
          components: ["热负荷计算", "温湿度响应"]
        - name: "Modelica/Dymola"
          usage: "多物理域仿真"
          components: ["HVAC系统", "流体网络"]
    
    test_scenarios:
      
      scenario_1_normal_operation:
        name: "正常运行工况"
        tests:
          - name: "温度阶跃响应"
            input: "设定值从22°C阶跃到24°C"
            expected:
              settling_time: "<15分钟"
              overshoot: "<10%"
              steady_state_error: "<0.5°C"
          - name: "负荷扰动响应"
            input: "突增50%冷负荷"
            expected:
              max_deviation: "<2°C"
              recovery_time: "<10分钟"
          - name: "压差控制稳定性"
            input: "开关门扰动"
            expected:
              recovery_time: "<30秒"
              max_deviation: "<5Pa"
      
      scenario_2_mode_transition:
        name: "模式切换"
        tests:
          - name: "手术模式→值班模式"
            verify:
              - "切换过程平滑"
              - "无设备频繁启停"
              - "压差维持正值"
          - name: "平疫转换"
            verify:
              - "负压建立时间"
              - "无交叉污染风险"
      
      scenario_3_fault_injection:
        name: "故障注入测试"
        tests:
          - name: "传感器失效"
            fault: "温度传感器信号丢失"
            expected:
              - "5秒内检测故障"
              - "自动切换备用传感器"
              - "报警生成"
          - name: "网络中断"
            fault: "DDC与上位机断开"
            expected:
              - "DDC继续本地控制"
              - "使用默认设定值"
          - name: "执行器故障"
            fault: "冷水阀卡死"
            expected:
              - "检测指令-反馈偏差"
              - "报警生成"
              - "送风量补偿"
      
      scenario_4_extreme_conditions:
        name: "极端工况"
        tests:
          - name: "夏季极端高温"
            condition: "室外温度40°C"
            verify: "室内温度可控"
          - name: "冬季极端低温"
            condition: "室外温度-20°C"
            verify: "无冻裂风险"
    
    simulation_output:
      - "控制参数推荐值(PID参数)"
      - "报警阈值验证"
      - "故障响应时间验证"
      - "能耗预测"
  
  # ═══════════════════════════════════════════════════════════════
  # 硬件在环测试 (HIL)
  # ═══════════════════════════════════════════════════════════════
  
  hardware_in_loop_testing:
    
    purpose: |
      验证实际控制器(DDC/PLC)与仿真环境的集成，确保控制程序在实际硬件上正确运行。
    
    hil_architecture:
      components:
        - name: "实时仿真器"
          function: "模拟物理过程(传感器信号输出)"
          examples: ["dSPACE", "NI PXI", "Speedgoat"]
        - name: "被测控制器"
          function: "实际DDC/PLC"
          state: "运行正式控制程序"
        - name: "IO接口"
          function: "连接仿真器与控制器"
          types: ["模拟量4-20mA", "数字量24VDC", "通信BACnet"]
        - name: "测试管理软件"
          function: "自动化测试执行与记录"
    
    hil_test_cases:
      
      case_1_io_verification:
        name: "IO信号验证"
        tests:
          - "所有AI点精度验证(±0.5%)"
          - "所有AO点响应验证"
          - "所有DI/DO状态验证"
          - "通信点位完整性"
      
      case_2_control_loop:
        name: "控制回路验证"
        tests:
          - name: "温度PID响应"
            method:
              - "仿真器输出温度信号"
              - "控制器计算输出"
              - "验证阀门开度变化"
          - name: "压差控制响应"
            method:
              - "仿真器模拟开门扰动"
              - "验证控制器调节速度"
      
      case_3_sequence_logic:
        name: "顺序逻辑验证"
        tests:
          - name: "手术室启动序列"
            method: "步进执行，验证每步条件和动作"
          - name: "冷机加减机逻辑"
            method: "模拟负荷变化，验证启停顺序"
      
      case_4_interlock:
        name: "联锁逻辑验证"
        tests:
          - name: "消防联动"
            method: "模拟火灾信号，验证设备响应"
          - name: "防冻保护"
            method: "模拟低温信号，验证保护动作"
      
      case_5_failure_mode:
        name: "故障模式验证"
        tests:
          - name: "传感器故障处理"
            method: "断开传感器信号，验证切换逻辑"
          - name: "通信故障处理"
            method: "断开网络，验证本地运行"
    
    hil_output:
      - "测试报告(通过/失败)"
      - "控制程序验证签章"
      - "发现问题清单"
      - "参数调整记录"
  
  # ═══════════════════════════════════════════════════════════════
  # 现场调试测试 (FAT/SAT)
  # ═══════════════════════════════════════════════════════════════
  
  field_testing:
    
    factory_acceptance_test:
      name: "工厂验收测试 (FAT)"
      location: "控制器厂家工厂"
      content:
        - "控制器硬件检查"
        - "程序下载验证"
        - "IO点位测试"
        - "通信测试"
        - "基本控制逻辑测试"
    
    site_acceptance_test:
      name: "现场验收测试 (SAT)"
      location: "项目现场"
      phases:
        
        phase_1_pre_functional:
          name: "预功能测试"
          content:
            - "控制器上电检查"
            - "网络连通性测试"
            - "所有硬接点验证"
            - "传感器校准"
        
        phase_2_functional:
          name: "功能测试"
          content:
            - "控制回路单体调试"
            - "PID参数整定"
            - "顺序逻辑验证"
            - "联锁逻辑验证"
        
        phase_3_integrated:
          name: "综合测试"
          content:
            - "系统联动测试"
            - "模式切换测试"
            - "消防联动测试"
            - "网络中断测试"
        
        phase_4_performance:
          name: "性能测试"
          content:
            - "控制精度验证"
            - "响应时间测量"
            - "稳定性测试(72小时)"
  
  # ═══════════════════════════════════════════════════════════════
  # 降级模式专项测试
  # ═══════════════════════════════════════════════════════════════
  
  degradation_mode_testing:
    
    test_1_network_loss:
      name: "网络断开测试"
      procedure:
        - step: "断开DDC与上位机网络"
        - step: "观察48小时"
        - step: "记录关键参数变化"
        - step: "恢复网络"
        - step: "验证数据同步"
      acceptance:
        - "关键区域参数偏差<5%"
        - "无设备异常停机"
        - "报警正确生成"
    
    test_2_sensor_failure:
      name: "传感器故障测试"
      procedure:
        - step: "断开温度传感器"
        - step: "验证自动切换备用"
        - step: "验证报警生成"
        - step: "验证控制持续"
      acceptance:
        - "5秒内检测故障"
        - "10秒内切换备用"
        - "控制精度略降但可接受"
    
    test_3_controller_failure:
      name: "控制器故障测试"
      procedure:
        - step: "模拟DDC宕机(断电)"
        - step: "验证执行器位置"
        - step: "验证L3保护动作"
        - step: "验证报警通知"
      acceptance:
        - "执行器保持安全位置"
        - "机械恒温器接管(如配置)"
        - "报警在60秒内送达"
    
    test_4_fire_interlock:
      name: "消防联动测试"
      procedure:
        - step: "触发消防测试信号"
        - step: "验证所有设备响应"
        - step: "记录响应时间"
        - step: "复位并验证恢复"
      acceptance:
        - "所有设备正确动作"
        - "响应时间<10秒"
        - "硬接点联动独立于DDC"
```

---

## 第十章 总结

### 修订版核心增强点

| 评审建议 | 修订响应 | 价值 |
|----------|----------|------|
| Agent-02引用 | 新增第七章"空间-控制策略映射"，显式引用Agent-02 | 控制逻辑与医疗业务深度耦合 |
| 边缘计算细化 | 第二章增加边缘节点类型、云边协同机制 | 架构清晰可实施 |
| 物理实现约束 | 新增第八章，定义传感器位置、执行器特性、协议规范 | 提高实施精度 |
| 降级模式完善 | 第五章增加控制器故障、执行器故障策略 | 全面覆盖故障场景 |
| 验证测试 | 新增第九章，包含仿真、HIL、现场测试框架 | 确保控制逻辑正确性 |

### 文档交付物清单

```yaml
Deliverables:
  whitepaper:
    file: "Agent06_Output.control_architecture_whitepaper_v2.1"
    status: "完成"
  
  pending_yaml_models:
    - file: "Agent06_Output.sensor_models"
      status: "待输出"
    - file: "Agent06_Output.actuator_models"
      status: "待输出"
    - file: "Agent06_Output.control_loop_models"
      status: "待输出"
    - file: "Agent06_Output.sequence_models"
      status: "待输出"
    - file: "Agent06_Output.resilience_strategies"
      status: "待输出"
    - file: "Agent06_Output.fire_interlock_matrix"
      status: "待输出"
    - file: "Agent06_Output.network_topology"
      status: "待输出"
    - file: "Agent06_Output.point_list"
      status: "待输出"
```

---

**白皮书修订版 v2.1 完成**

---

请问是否继续输出具体的YAML模型（传感器模型、执行器模型、控制回路模型等）？
[^1]: [Agent-02 空间本体建模师.md](http://file/0b71f550-e6e1-4425-b182-791293384a4b.md)

[^2]: [# 医疗建筑空间本体模型元数据（Medical ...tion: "结合具体医疗项目案例进行实例化"](# 医疗建筑空间本体模型元数据（Medical ...tion: "结合具体医疗项目案例进行实例化")

[^3]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^4]: [# Agent-08 运维管理建模师 输出文件元...etency: "人员资质能力达标率100%"](# Agent-08 运维管理建模师 输出文件元...etency: "人员资质能力达标率100%")

[^5]: [Agent-02  空间本体建模师 (Space Ontology Architect).md](http://file/35de1547-3b35-4ab4-a98a-37fb6cf0b0b6.md)

[^6]: [# 医疗建筑技术系统拓扑建模项目

[^1]: [Agent-02  空间本体建模师 (Space Ontology Architect).md](http://file/35de1547-3b35-4ab4-a98a-37fb6cf0b0b6.md)

[^2]: [Agent-02  空间本体建模师 (Space Ontology Architect).md](http://file/35de1547-3b35-4ab4-a98a-37fb6cf0b0b6.md)

[^3]: [Agent-02  空间本体建模师 (Space Ontology Architect).md](http://file/35de1547-3b35-4ab4-a98a-37fb6cf0b0b6.md)

[^4]: [Agent-03 v2.2  设备本体建模师 (Equipment Ontology Architect) 完整输出.md](http://file/6c1c1929-d310-442c-8bd3-24228af83d28.md)

[^5]: [Agent-02  空间本体建模师 (Space Ontology Architect).md](http://file/35de1547-3b35-4ab4-a98a-37fb6cf0b0b6.md)

[^6]: [# Agent-08 运维管理建模师 输出文件元...etency: "人员资质能力达标率100%"](# Agent-08 运维管理建模师 输出文件元...etency: "人员资质能力达标率100%")

[^1]: [# 医疗专用空间详细建模（Medical Spe...   - terminal_locations](# 医疗专用空间详细建模（Medical Spe...   - terminal_locations)

[^2]: [Agent-01 系统拓扑建模师 - 第四批次：消防系统 + 医疗专业系统.md](http://file/2f672527-5466-46d6-b255-27eed6ebc9e5.md)

[^3]: [# 运维管理模型 - 综合交付物总结

# Ag...筑的智能运维提供强有力的技术支撑和管理规范。"](# 运维管理模型 - 综合交付物总结

# Ag...筑的智能运维提供强有力的技术支撑和管理规范。")

[^4]: [Agent-01 系统拓扑建模师 - 完整输出文档.md](http://file/fb792853-9410-4a6d-9389-5740af5b6fee.md)

[^5]: [Agent-01 系统拓扑建模师 - 完整输出文档.md](http://file/fb792853-9410-4a6d-9389-5740af5b6fee.md)

[^6]: [# 医疗建筑空间分类体系（Healthcare ..."防振动", "UPS供电", "患者通话"]](# 医疗建筑空间分类体系（Healthcare ..."防振动", "UPS供电", "患者通话"])

[^1]: [Agent-01 系统拓扑建模师 - 完整输出文档.md](http://file/fb792853-9410-4a6d-9389-5740af5b6fee.md)

[^2]: [Agent-01 系统拓扑建模师 - 完整输出文档.md](http://file/fb792853-9410-4a6d-9389-5740af5b6fee.md)

[^3]: [Agent-01 系统拓扑建模师 - 完整输出文档.md](http://file/fb792853-9410-4a6d-9389-5740af5b6fee.md)

[^4]: [Agent-01 系统拓扑建模师 - 第七批次：运维与实施深化文档.md](http://file/bbf66cdc-5298-4478-a2a0-e10ef0b38607.md)

[^5]: [Agent-01 系统拓扑建模师 - 第三批次：给排水系统 + 智能化系统 （第三次修订版）.md](http://file/2c5c22aa-538a-48f4-a855-217265a1ca20.md)

[^6]: [Agent-01 系统拓扑建模师 - 第三批次：给排水系统 + 智能化系统 （第三次修订版）.md](http://file/2c5c22aa-538a-48f4-a855-217265a1ca20.md)
---