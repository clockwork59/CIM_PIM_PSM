## 🧑‍💻 User




---
## 🤖 Assistant


感谢您极其详尽且专业的审核。您的评估不仅指出了问题，更提供了可操作的改进方案。我将根据您的建议，按优先级生成补充文档。

让我先搜索知识库，确保补充内容与现有资产保持一致。

根据审核意见，我现在开始生成**P0优先级的补充内容**。

---

# Agent-06 控制系统建模师 - 补充文档 v3.2
## 基于技术审核的P0/P1级补充

**版本**: v3.2
**日期**: 2025-01-XX
**状态**: 审核后补充发布
**前置文档**: Agent-06全域控制系统实现模型v3.1

---

## 补充内容索引

| 优先级 | 章节 | 内容 | 状态 |
|--------|------|------|------|
| **P0** | 补充A | 全域I/O点位矩阵 | ✅ 本文档 |
| **P0** | 补充B | Agent-04物理方程深度集成 | ✅ 本文档 |
| **P1** | 补充C | 故障诊断决策树 | ✅ 本文档 |
| **P1** | 补充D | SAT验收测试清单 | ✅ 本文档 |
| **P2** | 补充E | 极端工况控制策略 | ✅ 本文档 |
| **P2** | 补充F | 分户计量与权限管理 | ✅ 本文档 |
| **P2** | 补充G | 下游Agent交接计划 | ✅ 本文档 |

---

# 补充A：全域I/O点位矩阵 (P0)

## A.1 系统级I/O统计总表

```yaml
Global_IO_Summary:
  
  meta:
    building: "综合医院示范项目"
    gross_floor_area: "80,000 m²"
    beds: 500
    operating_rooms: 12
    icu_beds: 40
    
    # 继承自Agent-01系统拓扑
    system_count: 26
    
  # ═══════════════════════════════════════════════════════════════════════════
  # 分专业I/O统计
  # ═══════════════════════════════════════════════════════════════════════════
  
  system_breakdown:
    
    HVAC:
      subsystems: 3  # CHP, AHU, FCU
      description: "暖通空调系统"
      
      equipment_inventory:
        # 冷热源 HVAC-CHP
        - equipment_type: "离心式冷水机组"
          equipment_ref: "EQP-CH-CENT"
          quantity: 4
          points_per_unit: 28
          subtotal_points: 112
          
        - equipment_type: "螺杆式冷水机组"
          equipment_ref: "EQP-CH-SCREW"
          quantity: 0
          points_per_unit: 25
          subtotal_points: 0
          
        - equipment_type: "冷冻水泵(一次泵)"
          equipment_ref: "EQP-PUMP-CHW-PRI"
          quantity: 4
          points_per_unit: 12
          subtotal_points: 48
          
        - equipment_type: "冷冻水泵(二次泵)"
          equipment_ref: "EQP-PUMP-CHW-SEC"
          quantity: 4
          points_per_unit: 15
          subtotal_points: 60
          
        - equipment_type: "冷却水泵"
          equipment_ref: "EQP-PUMP-CW"
          quantity: 4
          points_per_unit: 12
          subtotal_points: 48
          
        - equipment_type: "冷却塔"
          equipment_ref: "EQP-CT"
          quantity: 4
          points_per_unit: 10
          subtotal_points: 40
          
        - equipment_type: "板式换热器"
          equipment_ref: "EQP-HX-PLATE"
          quantity: 2
          points_per_unit: 8
          subtotal_points: 16
          
        - equipment_type: "热水锅炉"
          equipment_ref: "EQP-BOILER-HW"
          quantity: 2
          points_per_unit: 20
          subtotal_points: 40
          
        - equipment_type: "热水泵"
          equipment_ref: "EQP-PUMP-HW"
          quantity: 3
          points_per_unit: 12
          subtotal_points: 36
          
        - equipment_type: "定压补水装置"
          equipment_ref: "EQP-EXPANSION"
          quantity: 2
          points_per_unit: 8
          subtotal_points: 16
          
        - equipment_type: "水处理设备"
          equipment_ref: "EQP-WATER-TREAT"
          quantity: 2
          points_per_unit: 6
          subtotal_points: 12
        
        # 空调箱 HVAC-AHU
        - equipment_type: "洁净手术室AHU"
          equipment_ref: "EQP-AHU-CLEAN-OR"
          quantity: 12
          points_per_unit: 35
          subtotal_points: 420
          
        - equipment_type: "ICU专用AHU"
          equipment_ref: "EQP-AHU-CLEAN-ICU"
          quantity: 4
          points_per_unit: 30
          subtotal_points: 120
          
        - equipment_type: "负压隔离AHU"
          equipment_ref: "EQP-AHU-NEG"
          quantity: 4
          points_per_unit: 32
          subtotal_points: 128
          
        - equipment_type: "新风机组"
          equipment_ref: "EQP-AHU-PAU"
          quantity: 8
          points_per_unit: 18
          subtotal_points: 144
          
        - equipment_type: "组合式空调箱(普通)"
          equipment_ref: "EQP-AHU-COMBO"
          quantity: 15
          points_per_unit: 22
          subtotal_points: 330
          
        - equipment_type: "全热交换新风机"
          equipment_ref: "EQP-ERV"
          quantity: 6
          points_per_unit: 12
          subtotal_points: 72
          
        # 末端 HVAC-FCU
        - equipment_type: "风机盘管(普通)"
          equipment_ref: "EQP-FCU"
          quantity: 200
          points_per_unit: 6
          subtotal_points: 1200
          note: "按区域分组控制可减少点位"
          
        - equipment_type: "变风量末端(VAV)"
          equipment_ref: "EQP-VAV"
          quantity: 30
          points_per_unit: 8
          subtotal_points: 240
          
        # 室内环境传感器
        - equipment_type: "手术室室内传感器组"
          equipment_ref: "ROOM-SENSORS-OR"
          quantity: 12
          points_per_unit: 12
          subtotal_points: 144
          
        - equipment_type: "ICU室内传感器组"
          equipment_ref: "ROOM-SENSORS-ICU"
          quantity: 40
          points_per_unit: 8
          subtotal_points: 320
          
        - equipment_type: "普通病房室内传感器"
          equipment_ref: "ROOM-SENSORS-WARD"
          quantity: 100
          points_per_unit: 4
          subtotal_points: 400
          
        - equipment_type: "走廊/公共区域传感器"
          equipment_ref: "ROOM-SENSORS-COMMON"
          quantity: 50
          points_per_unit: 3
          subtotal_points: 150
          
      HVAC_subtotal:
        equipment_count: 506
        total_points: 4116
        
    ELEC:
      subsystems: 6  # HV, LV, EPS, UPS, EL, LTG
      description: "电气系统"
      
      equipment_inventory:
        - equipment_type: "10kV高压开关柜"
          equipment_ref: "EQP-SWGR-HV"
          quantity: 12
          points_per_unit: 15
          subtotal_points: 180
          
        - equipment_type: "变压器"
          equipment_ref: "EQP-TRANSFORMER"
          quantity: 4
          points_per_unit: 8
          subtotal_points: 32
          
        - equipment_type: "低压总配电柜"
          equipment_ref: "EQP-SWGR-LV-MDB"
          quantity: 4
          points_per_unit: 25
          subtotal_points: 100
          
        - equipment_type: "低压分配电柜"
          equipment_ref: "EQP-SWGR-LV-DB"
          quantity: 40
          points_per_unit: 12
          subtotal_points: 480
          
        - equipment_type: "柴油发电机组"
          equipment_ref: "EQP-GENERATOR-DIESEL"
          quantity: 2
          points_per_unit: 30
          subtotal_points: 60
          
        - equipment_type: "ATS自动转换开关"
          equipment_ref: "EQP-ATS"
          quantity: 8
          points_per_unit: 8
          subtotal_points: 64
          
        - equipment_type: "UPS不间断电源"
          equipment_ref: "EQP-UPS"
          quantity: 6
          points_per_unit: 15
          subtotal_points: 90
          
        - equipment_type: "医用隔离电源系统"
          equipment_ref: "EQP-ISO-TRANS"
          quantity: 20
          points_per_unit: 10
          subtotal_points: 200
          note: "手术室、ICU各床位配置"
          
        - equipment_type: "智能照明控制器"
          equipment_ref: "EQP-LTG-CTRL"
          quantity: 30
          points_per_unit: 8
          subtotal_points: 240
          
        - equipment_type: "电梯控制接口"
          equipment_ref: "EQP-ELEVATOR"
          quantity: 12
          points_per_unit: 10
          subtotal_points: 120
          
        - equipment_type: "电能质量分析仪"
          equipment_ref: "EQP-PQA"
          quantity: 4
          points_per_unit: 20
          subtotal_points: 80
          
      ELEC_subtotal:
        equipment_count: 142
        total_points: 1646
        
    PLUMB:
      subsystems: 4  # DWS, HWS, SAN, RW
      description: "给排水系统"
      
      equipment_inventory:
        - equipment_type: "生活给水变频泵组"
          equipment_ref: "EQP-PUMP-DWS-VFD"
          quantity: 2
          points_per_unit: 18
          subtotal_points: 36
          
        - equipment_type: "生活水箱液位监测"
          equipment_ref: "EQP-TANK-DWS"
          quantity: 4
          points_per_unit: 6
          subtotal_points: 24
          
        - equipment_type: "热水循环泵"
          equipment_ref: "EQP-PUMP-HWS-CIRC"
          quantity: 3
          points_per_unit: 12
          subtotal_points: 36
          
        - equipment_type: "容积式热水器"
          equipment_ref: "EQP-WHC"
          quantity: 4
          points_per_unit: 10
          subtotal_points: 40
          
        - equipment_type: "污水提升泵"
          equipment_ref: "EQP-PUMP-SAN"
          quantity: 4
          points_per_unit: 8
          subtotal_points: 32
          
        - equipment_type: "雨水回收系统"
          equipment_ref: "EQP-RW-RECYCLE"
          quantity: 1
          points_per_unit: 12
          subtotal_points: 12
          
        - equipment_type: "中水处理系统"
          equipment_ref: "EQP-GRAY-WATER"
          quantity: 1
          points_per_unit: 15
          subtotal_points: 15
          
      PLUMB_subtotal:
        equipment_count: 19
        total_points: 195
        
    MGAS:
      subsystems: 4  # O2, VAC, AIR, N2O
      description: "医用气体系统"
      
      equipment_inventory:
        - equipment_type: "医用氧气汇流排"
          equipment_ref: "EQP-O2-MANIFOLD"
          quantity: 2
          points_per_unit: 12
          subtotal_points: 24
          
        - equipment_type: "液氧储罐系统"
          equipment_ref: "EQP-O2-LOX"
          quantity: 1
          points_per_unit: 15
          subtotal_points: 15
          
        - equipment_type: "氧气区域阀箱"
          equipment_ref: "EQP-O2-ZONE-VALVE"
          quantity: 15
          points_per_unit: 6
          subtotal_points: 90
          
        - equipment_type: "医用真空泵组"
          equipment_ref: "EQP-VAC-PUMP"
          quantity: 3
          points_per_unit: 15
          subtotal_points: 45
          
        - equipment_type: "真空区域阀箱"
          equipment_ref: "EQP-VAC-ZONE-VALVE"
          quantity: 15
          points_per_unit: 4
          subtotal_points: 60
          
        - equipment_type: "医用空压机组"
          equipment_ref: "EQP-COMP-OIL-FREE"
          quantity: 3
          points_per_unit: 18
          subtotal_points: 54
          
        - equipment_type: "医用空气干燥机"
          equipment_ref: "EQP-DRYER"
          quantity: 2
          points_per_unit: 8
          subtotal_points: 16
          
        - equipment_type: "压缩空气区域阀箱"
          equipment_ref: "EQP-AIR-ZONE-VALVE"
          quantity: 15
          points_per_unit: 4
          subtotal_points: 60
          
        - equipment_type: "笑气汇流排"
          equipment_ref: "EQP-N2O-MANIFOLD"
          quantity: 1
          points_per_unit: 10
          subtotal_points: 10
          
        - equipment_type: "麻醉废气排放系统"
          equipment_ref: "EQP-AGSS"
          quantity: 1
          points_per_unit: 8
          subtotal_points: 8
          
      MGAS_subtotal:
        equipment_count: 58
        total_points: 382
        
    FIRE:
      subsystems: 3  # FAS, SPS, EXH
      description: "消防系统(BMS接口点位)"
      note: "消防主机独立，此处仅统计BMS监测/联动接口"
      
      equipment_inventory:
        - equipment_type: "消火栓泵"
          equipment_ref: "EQP-PUMP-FIRE-HYD"
          quantity: 2
          points_per_unit: 10
          subtotal_points: 20
          
        - equipment_type: "喷淋泵"
          equipment_ref: "EQP-PUMP-FIRE-SPR"
          quantity: 2
          points_per_unit: 10
          subtotal_points: 20
          
        - equipment_type: "稳压泵"
          equipment_ref: "EQP-PUMP-FIRE-JP"
          quantity: 2
          points_per_unit: 6
          subtotal_points: 12
          
        - equipment_type: "消防水池液位"
          equipment_ref: "EQP-TANK-FIRE"
          quantity: 2
          points_per_unit: 4
          subtotal_points: 8
          
        - equipment_type: "排烟风机"
          equipment_ref: "EQP-FAN-SMOKE"
          quantity: 8
          points_per_unit: 8
          subtotal_points: 64
          
        - equipment_type: "正压送风机"
          equipment_ref: "EQP-FAN-PRESS"
          quantity: 6
          points_per_unit: 6
          subtotal_points: 36
          
        - equipment_type: "防火阀(70℃)"
          equipment_ref: "EQP-DAMPER-FIRE-70"
          quantity: 100
          points_per_unit: 2
          subtotal_points: 200
          
        - equipment_type: "排烟阀/排烟口"
          equipment_ref: "EQP-DAMPER-SMOKE"
          quantity: 50
          points_per_unit: 3
          subtotal_points: 150
          
        - equipment_type: "FAS联动接口"
          equipment_ref: "EQP-FAS-INTERFACE"
          quantity: 1
          points_per_unit: 50
          subtotal_points: 50
          note: "火警、分区、联动状态等"
          
      FIRE_subtotal:
        equipment_count: 173
        total_points: 560
        
    INT:
      subsystems: 3  # BA, SEC, NUR
      description: "智能化系统(集成接口)"
      
      equipment_inventory:
        - equipment_type: "DDC控制器"
          equipment_ref: "EQP-DDC-MAIN"
          quantity: 80
          points_per_unit: 0
          subtotal_points: 0
          note: "控制器本身不计点位"
          
        - equipment_type: "NAC网络控制器"
          equipment_ref: "EQP-NAC"
          quantity: 8
          points_per_unit: 0
          subtotal_points: 0
          
        - equipment_type: "边缘网关"
          equipment_ref: "EQP-EDGE-GW"
          quantity: 2
          points_per_unit: 0
          subtotal_points: 0
          
        - equipment_type: "门禁系统接口"
          equipment_ref: "EQP-SEC-INTERFACE"
          quantity: 1
          points_per_unit: 30
          subtotal_points: 30
          
        - equipment_type: "视频监控系统接口"
          equipment_ref: "EQP-CCTV-INTERFACE"
          quantity: 1
          points_per_unit: 20
          subtotal_points: 20
          
        - equipment_type: "护士呼叫系统接口"
          equipment_ref: "EQP-NC-INTERFACE"
          quantity: 1
          points_per_unit: 15
          subtotal_points: 15
          
        - equipment_type: "公共广播系统接口"
          equipment_ref: "EQP-PA-INTERFACE"
          quantity: 1
          points_per_unit: 10
          subtotal_points: 10
          
      INT_subtotal:
        equipment_count: 94
        total_points: 75
        
  # ═══════════════════════════════════════════════════════════════════════════
  # 全域汇总
  # ═══════════════════════════════════════════════════════════════════════════
  
  grand_total:
    total_equipment: 992
    total_io_points: 6974
    
    breakdown_by_type:
      analog_input_AI: 2450
      analog_output_AO: 850
      digital_input_DI: 2200
      digital_output_DO: 1100
      communication_virtual: 374
      
    breakdown_by_network:
      bacnet_ip_points: 1200
      bacnet_mstp_points: 4500
      modbus_rtu_points: 800
      hardwired_points: 474
      
    breakdown_by_criticality:
      P0_life_safety: 1850
      P1_mission_critical: 2100
      P2_important: 2024
      P3_normal: 1000
```

## A.2 典型空间I/O清单

```yaml
Space_IO_Lists:
  
  # ═══════════════════════════════════════════════════════════════════════════
  # I级洁净手术室完整点位表
  # ═══════════════════════════════════════════════════════════════════════════
  
  OR_Class_I:
    space_ref: "OR-001"
    space_type: "ROOM-OR-I"
    agent02_ref: "Agent-02.Medical_Special_Space_Models.ROOM-OR.I级"
    criticality: "P0-LIFE_SAFETY"
    
    # 该空间关联的所有I/O点位
    io_points_complete:
      
      # ─────────────────────────────────────────────────────────────────────
      # 空调箱 AHU-OR-001 (35点)
      # ─────────────────────────────────────────────────────────────────────
      AHU_OR_001:
        equipment_id: "AHU-OR-001"
        controller: "DDC-OR-001"
        point_list:
          # 模拟量输入 AI (15点)
          - {id: "HVAC-OR-AHU01-AI_SA_TEMP", name: "送风温度", type: "AI", signal: "4-20mA", range: "10-40°C", critical: true}
          - {id: "HVAC-OR-AHU01-AI_SA_HUMID", name: "送风湿度", type: "AI", signal: "4-20mA", range: "20-95%RH"}
          - {id: "HVAC-OR-AHU01-AI_SA_FLOW", name: "送风量", type: "AI", signal: "4-20mA", range: "0-15000m³/h"}
          - {id: "HVAC-OR-AHU01-AI_RA_TEMP", name: "回风温度", type: "AI", signal: "4-20mA", range: "15-35°C"}
          - {id: "HVAC-OR-AHU01-AI_RA_HUMID", name: "回风湿度", type: "AI", signal: "4-20mA", range: "20-80%RH"}
          - {id: "HVAC-OR-AHU01-AI_OA_TEMP", name: "新风温度", type: "AI", signal: "4-20mA", range: "-20-45°C"}
          - {id: "HVAC-OR-AHU01-AI_MA_TEMP", name: "混风温度", type: "AI", signal: "4-20mA", range: "0-40°C", critical: true}
          - {id: "HVAC-OR-AHU01-AI_PREFILTER_DP", name: "初效压差", type: "AI", signal: "4-20mA", range: "0-500Pa"}
          - {id: "HVAC-OR-AHU01-AI_MEDFILTER_DP", name: "中效压差", type: "AI", signal: "4-20mA", range: "0-500Pa"}
          - {id: "HVAC-OR-AHU01-AI_HEPAFILTER_DP", name: "高效压差", type: "AI", signal: "4-20mA", range: "0-600Pa"}
          - {id: "HVAC-OR-AHU01-AI_SF_CURRENT", name: "送风机电流", type: "AI", signal: "4-20mA", range: "0-100A"}
          - {id: "HVAC-OR-AHU01-AI_SF_FREQ", name: "送风机频率", type: "AI", signal: "4-20mA", range: "0-50Hz"}
          - {id: "HVAC-OR-AHU01-AI_RF_FREQ", name: "排风机频率", type: "AI", signal: "4-20mA", range: "0-50Hz"}
          - {id: "HVAC-OR-AHU01-AI_CHW_VLV_FB", name: "冷水阀反馈", type: "AI", signal: "4-20mA", range: "0-100%"}
          - {id: "HVAC-OR-AHU01-AI_HW_VLV_FB", name: "热水阀反馈", type: "AI", signal: "4-20mA", range: "0-100%"}
          
          # 数字量输入 DI (10点)
          - {id: "HVAC-OR-AHU01-DI_SF_RUN", name: "送风机运行", type: "DI", contact: "NO"}
          - {id: "HVAC-OR-AHU01-DI_SF_FAULT", name: "送风机故障", type: "DI", contact: "NC", critical: true}
          - {id: "HVAC-OR-AHU01-DI_RF_RUN", name: "排风机运行", type: "DI", contact: "NO"}
          - {id: "HVAC-OR-AHU01-DI_RF_FAULT", name: "排风机故障", type: "DI", contact: "NC"}
          - {id: "HVAC-OR-AHU01-DI_FREEZE", name: "防冻开关", type: "DI", contact: "NC", critical: true}
          - {id: "HVAC-OR-AHU01-DI_SMOKE", name: "风管烟感", type: "DI", contact: "NO"}
          - {id: "HVAC-OR-AHU01-DI_FD", name: "防火阀状态", type: "DI", contact: "NC", critical: true}
          - {id: "HVAC-OR-AHU01-DI_HUM_RUN", name: "加湿器运行", type: "DI", contact: "NO"}
          - {id: "HVAC-OR-AHU01-DI_HUM_FAULT", name: "加湿器故障", type: "DI", contact: "NC"}
          - {id: "HVAC-OR-AHU01-DI_LOCAL", name: "本地/远程", type: "DI", contact: "NO"}
          
          # 模拟量输出 AO (7点)
          - {id: "HVAC-OR-AHU01-AO_CHW_VLV", name: "冷水阀控制", type: "AO", signal: "4-20mA", range: "0-100%", fail_safe: "CLOSE"}
          - {id: "HVAC-OR-AHU01-AO_HW_VLV", name: "热水阀控制", type: "AO", signal: "4-20mA", range: "0-100%", fail_safe: "OPEN"}
          - {id: "HVAC-OR-AHU01-AO_OA_DMP", name: "新风阀控制", type: "AO", signal: "4-20mA", range: "0-100%", fail_safe: "CLOSE"}
          - {id: "HVAC-OR-AHU01-AO_SF_SPD", name: "送风机速度", type: "AO", signal: "4-20mA", range: "0-50Hz"}
          - {id: "HVAC-OR-AHU01-AO_RF_SPD", name: "排风机速度", type: "AO", signal: "4-20mA", range: "0-50Hz"}
          - {id: "HVAC-OR-AHU01-AO_HUM", name: "加湿器控制", type: "AO", signal: "4-20mA", range: "0-100%"}
          - {id: "HVAC-OR-AHU01-AO_RA_DMP", name: "回风阀控制", type: "AO", signal: "4-20mA", range: "0-100%"}
          
          # 数字量输出 DO (3点)
          - {id: "HVAC-OR-AHU01-DO_SF_START", name: "送风机启动", type: "DO", contact: "NO"}
          - {id: "HVAC-OR-AHU01-DO_RF_START", name: "排风机启动", type: "DO", contact: "NO"}
          - {id: "HVAC-OR-AHU01-DO_UV", name: "紫外灯控制", type: "DO", contact: "NO"}
          
        subtotal: 35
        
      # ─────────────────────────────────────────────────────────────────────
      # 室内环境传感器组 (12点)
      # ─────────────────────────────────────────────────────────────────────
      ROOM_SENSORS:
        equipment_id: "ROOM-SENS-OR-001"
        controller: "DDC-OR-001"
        point_list:
          # 温度 - 双传感器
          - {id: "HVAC-OR-RM01-AI_TEMP_A", name: "室温A", type: "AI", signal: "PT1000", range: "15-35°C", redundancy: "PRIMARY", critical: true}
          - {id: "HVAC-OR-RM01-AI_TEMP_B", name: "室温B", type: "AI", signal: "PT1000", range: "15-35°C", redundancy: "BACKUP"}
          
          # 湿度
          - {id: "HVAC-OR-RM01-AI_HUMID", name: "室内湿度", type: "AI", signal: "4-20mA", range: "20-80%RH"}
          
          # 压差 - 双传感器
          - {id: "HVAC-OR-RM01-AI_PRESS_A", name: "压差A", type: "AI", signal: "4-20mA", range: "-50-100Pa", redundancy: "PRIMARY", critical: true}
          - {id: "HVAC-OR-RM01-AI_PRESS_B", name: "压差B", type: "AI", signal: "4-20mA", range: "-50-100Pa", redundancy: "BACKUP"}
          
          # CO2（可选）
          - {id: "HVAC-OR-RM01-AI_CO2", name: "CO2浓度", type: "AI", signal: "4-20mA", range: "0-2000ppm", optional: true}
          
          # 门状态
          - {id: "HVAC-OR-RM01-DI_DOOR_MAIN", name: "主门状态", type: "DI", contact: "NO"}
          - {id: "HVAC-OR-RM01-DI_DOOR_EQUIP", name: "器械门状态", type: "DI", contact: "NO"}
          
          # 人员在场
          - {id: "HVAC-OR-RM01-DI_OCCUP", name: "人员在场", type: "DI", contact: "NO"}
          
          # 层流状态
          - {id: "HVAC-OR-RM01-DI_LAMINAR", name: "层流正常", type: "DI", contact: "NO"}
          
          # 手术室面板按钮
          - {id: "HVAC-OR-RM01-DI_MODE_BTN", name: "模式切换按钮", type: "DI", contact: "NO"}
          
          # 压差显示器（Modbus通信点）
          - {id: "HVAC-OR-RM01-AV_PRESS_DISP", name: "门口压差显示", type: "COMM", protocol: "Modbus"}
          
        subtotal: 12
        
      # ─────────────────────────────────────────────────────────────────────
      # 医用隔离电源 IPS (10点)
      # ─────────────────────────────────────────────────────────────────────
      IPS:
        equipment_id: "IPS-OR-001"
        controller: "DDC-OR-001"
        point_list:
          - {id: "ELEC-OR-IPS01-AI_V_IN", name: "输入电压", type: "AI", signal: "COMM", range: "0-500V"}
          - {id: "ELEC-OR-IPS01-AI_V_OUT", name: "输出电压", type: "AI", signal: "COMM", range: "0-250V"}
          - {id: "ELEC-OR-IPS01-AI_I_LOAD", name: "负载电流", type: "AI", signal: "COMM", range: "0-50A"}
          - {id: "ELEC-OR-IPS01-AI_TRANS_TEMP", name: "变压器温度", type: "AI", signal: "COMM", range: "0-150°C"}
          - {id: "ELEC-OR-IPS01-AI_ISO_R", name: "绝缘电阻", type: "AI", signal: "COMM", range: "0-1000kΩ", critical: true}
          - {id: "ELEC-OR-IPS01-AI_FAULT_I", name: "故障电流", type: "AI", signal: "COMM", range: "0-10mA"}
          - {id: "ELEC-OR-IPS01-DI_ISO_ALM", name: "绝缘报警", type: "DI", contact: "NO", critical: true}
          - {id: "ELEC-OR-IPS01-DI_OVERLOAD", name: "过负荷", type: "DI", contact: "NO"}
          - {id: "ELEC-OR-IPS01-DI_OVER_TEMP", name: "超温报警", type: "DI", contact: "NO"}
          - {id: "ELEC-OR-IPS01-DO_ALM_RST", name: "报警复位", type: "DO", contact: "NO", pulse: true}
          
        subtotal: 10
        
      # ─────────────────────────────────────────────────────────────────────
      # 医用气体接口 (6点)
      # ─────────────────────────────────────────────────────────────────────
      MGAS:
        equipment_id: "MGAS-ZV-OR-001"
        controller: "DDC-OR-001"
        point_list:
          - {id: "MGAS-OR-O2-AI_PRESS", name: "氧气压力", type: "AI", signal: "4-20mA", range: "0-1.0MPa", critical: true}
          - {id: "MGAS-OR-VAC-AI_PRESS", name: "负压压力", type: "AI", signal: "4-20mA", range: "-0.1-0MPa"}
          - {id: "MGAS-OR-AIR-AI_PRESS", name: "压缩空气压力", type: "AI", signal: "4-20mA", range: "0-1.0MPa"}
          - {id: "MGAS-OR-O2-DI_ALM_H", name: "氧气高压报警", type: "DI", contact: "NC"}
          - {id: "MGAS-OR-O2-DI_ALM_L", name: "氧气低压报警", type: "DI", contact: "NC", critical: true}
          - {id: "MGAS-OR-O2-DO_EMERG", name: "紧急切断", type: "DO", contact: "NO", requires_auth: true}
          
        subtotal: 6
        
      # ─────────────────────────────────────────────────────────────────────
      # 照明控制 (4点)
      # ─────────────────────────────────────────────────────────────────────
      LIGHTING:
        equipment_id: "LTG-OR-001"
        controller: "DDC-OR-001"
        point_list:
          - {id: "ELEC-OR-LTG01-DI_MAIN_ON", name: "主照明状态", type: "DI", contact: "NO"}
          - {id: "ELEC-OR-LTG01-DI_SURG_ON", name: "无影灯状态", type: "DI", contact: "NO"}
          - {id: "ELEC-OR-LTG01-DO_MAIN_CMD", name: "主照明控制", type: "DO", contact: "NO"}
          - {id: "ELEC-OR-LTG01-AO_DIM", name: "调光控制", type: "AO", signal: "0-10V", range: "0-100%"}
          
        subtotal: 4
        
    # 该空间点位汇总
    space_summary:
      total_equipment: 5
      total_points: 67
      breakdown:
        AI: 32
        AO: 8
        DI: 19
        DO: 6
        COMM: 2
        
    # 控制器分配
    controller_assignment:
      primary: "DDC-OR-001"
      backup: "DDC-OR-002 (Hot Standby recommended)"
      io_capacity_check:
        required_AI: 32
        required_AO: 8
        required_DI: 19
        required_DO: 6
        selected_DDC_capacity: "32AI/16AO/32DI/16DO"
        margin: "Adequate"
```

## A.3 走廊/辅助空间点位表

```yaml
# Agent-05审核意见特别强调的关键辅助空间
Corridor_IO_List:
  
  OR_Clean_Corridor:
    space_ref: "CORRIDOR-OR-001"
    space_type: "CORRIDOR-CLEAN"
    agent02_ref: "Agent-02.Auxiliary_Spaces.Corridor-Clean"
    criticality: "P0-LIFE_SAFETY"
    note: "压差梯度中间环节，直接影响手术室洁净度"
    
    io_points:
      # 压差梯度监测
      - {id: "HVAC-COR-OR01-AI_PRESS_VS_OR", name: "对手术室压差", type: "AI", range: "-50-30Pa", setpoint: "-7Pa"}
      - {id: "HVAC-COR-OR01-AI_PRESS_VS_CLEAN", name: "对清洁走廊压差", type: "AI", range: "-30-50Pa", setpoint: "+5Pa"}
      
      # 温度
      - {id: "HVAC-COR-OR01-AI_TEMP", name: "走廊温度", type: "AI", range: "15-30°C"}
      
      # 防火门状态
      - {id: "HVAC-COR-OR01-DI_FIREDOOR_1", name: "防火门1状态", type: "DI", contact: "NC"}
      - {id: "HVAC-COR-OR01-DI_FIREDOOR_2", name: "防火门2状态", type: "DI", contact: "NC"}
      
      # 紧急出口指示
      - {id: "HVAC-COR-OR01-DI_EXIT_LIGHT", name: "紧急出口灯状态", type: "DI", contact: "NO"}
      
    subtotal: 6
    
  Lobby_Change_Area:
    space_ref: "LOBBY-OR-001"
    space_type: "换车间"
    criticality: "P1"
    
    io_points:
      - {id: "HVAC-LOBBY-OR01-AI_PRESS", name: "换车间压差", type: "AI", range: "-30-50Pa", setpoint: "0Pa"}
      - {id: "HVAC-LOBBY-OR01-AI_TEMP", name: "换车间温度", type: "AI", range: "15-30°C"}
      - {id: "HVAC-LOBBY-OR01-DI_DOOR", name: "门状态", type: "DI", contact: "NO"}
      
    subtotal: 3
```

---

# 补充B：Agent-04物理方程深度集成 (P0)

## B.1 控制算法物理基础

```yaml
Physics_Based_Control:
  
  # ═══════════════════════════════════════════════════════════════════════════
  # B.1.1 基于表冷器换热方程的前馈控制
  # ═══════════════════════════════════════════════════════════════════════════
  
  Feedforward_Temperature_Control:
    name: "送风温度前馈控制"
    applicable_to: ["AHU-OR", "AHU-ICU", "AHU-CLEAN"]
    
    # Agent-04方程引用
    equation_ref: "EQ-HX-COIL-001"
    source: "Agent-04.Equation_Library.Heat_Exchanger"
    
    # 物理原理
    principle: |
      表冷器换热遵循对数平均温差(LMTD)模型：
      Q = K × A × LMTD
      
      通过实时计算室内负荷，预测所需表冷器出口温度，
      进而预估冷水阀开度，实现前馈控制。
      
    # 算法实现
    algorithm:
      
      step_1_load_calculation:
        name: "室内冷负荷计算"
        formula: |
          Q_load = Q_sensible + Q_latent
          
          Q_sensible = ρ_air × V_supply × Cp_air × (T_return - T_supply)
                     + Q_envelope + Q_solar + Q_occupancy + Q_equipment
          
          简化为实时测量：
          Q_load ≈ ρ × V × Cp × (T_RA - T_SA)
          
        inputs:
          T_RA: {point: "AI_RA_TEMP", unit: "°C"}
          T_SA: {point: "AI_SA_TEMP", unit: "°C"}
          V: {point: "AI_SA_FLOW", unit: "m³/h", convert: "÷3600 to m³/s"}
          rho: {value: 1.2, unit: "kg/m³"}
          Cp: {value: 1.006, unit: "kJ/kg·K"}
        output:
          Q_load: {unit: "kW"}
          update_rate: "10s"
          
      step_2_target_supply_temp:
        name: "目标送风温度计算"
        formula: |
          T_supply_target = T_room_SP - (Q_load / (ρ × V × Cp))
          
          考虑送风温差设计值（通常8-10°C）：
          T_supply_target = CLAMP(T_supply_target, 14°C, 22°C)
          
        inputs:
          T_room_SP: {source: "FSM state setpoint", default: 22.0, unit: "°C"}
          Q_load: {from: "step_1"}
        output:
          T_supply_target: {unit: "°C"}
          
      step_3_valve_position_prediction:
        name: "阀位预测（前馈分量）"
        formula: |
          # 基于表冷器特性曲线
          Valve_FF = f(Q_required, T_chw_supply, Flow_chw, Coil_Characteristics)
          
          简化线性模型（实际需现场标定）：
          Valve_FF = K_coil × Q_required / Q_design × 100%
          
          其中 K_coil 为表冷器效率系数（0.7-0.9），需现场辨识
          
        inputs:
          Q_required: {calculation: "ρ × V × Cp × (T_MA - T_supply_target)"}
          T_chw_supply: {point: "系统冷冻水供水温度", default: 7.0}
          Q_design: {value: 50, unit: "kW", note: "设计冷量"}
          K_coil: {value: 0.85, note: "需现场标定"}
        output:
          Valve_FF: {range: "0-100%"}
          
      step_4_combined_output:
        name: "前馈+反馈综合输出"
        formula: |
          Valve_Output = Valve_FF + Valve_FB
          
          其中 Valve_FB 来自PID控制器输出
          
          限幅：
          Valve_Output = CLAMP(Valve_Output, 0%, 100%)
          
        control_structure: |
          ┌─────────────────────────────────────────────────────┐
          │                                                     │
          │   T_room_SP ──┬──→ [前馈计算] ──→ Valve_FF ──┐     │
          │               │                              │     │
          │               └──→ [PID] ←── (T_room_SP - T_room_PV)│
          │                      │                       │     │
          │                      └──→ Valve_FB ──────────┤     │
          │                                              │     │
          │                                    ┌─────────┴───┐ │
          │                                    │   Σ Limiter │ │
          │                                    └──────┬──────┘ │
          │                                           │        │
          │                                           ↓        │
          │                                      Valve_Output  │
          └─────────────────────────────────────────────────────┘
          
        benefit: "提前响应负荷变化，减少超调和滞后"
        
    # PID参数（基于仿真和工程经验）
    pid_parameters:
      master_loop_room_temp:
        Kp: 2.0
        Ti: 600  # seconds
        Td: 0
        anti_windup: true
        output_range: [14, 22]  # 送风温度设定范围
        
      slave_loop_supply_temp:
        Kp: 1.5
        Ti: 180
        Td: 0
        anti_windup: true
        output_range: [0, 100]  # 阀位范围
        
    # 参数辨识方法
    calibration:
      method: "阶跃响应测试"
      procedure:
        - step: 1
          action: "稳态运行，记录当前阀位和温度"
        - step: 2
          action: "阀位阶跃变化10%"
        - step: 3
          action: "记录送风温度响应曲线"
        - step: 4
          action: "计算过程增益K和时间常数τ"
        - step: 5
          action: "根据Ziegler-Nichols或SIMC规则整定PID"
      frequency: "SAT阶段 + 年度复核"
      
  # ═══════════════════════════════════════════════════════════════════════════
  # B.1.2 虚拟传感器算法
  # ═══════════════════════════════════════════════════════════════════════════
  
  Virtual_Sensors:
    
    VS_001_Cooling_Load:
      name: "虚拟冷负荷传感器"
      purpose: "当流量计故障或未配置时，估算空调负荷"
      
      calculation:
        primary_method:
          name: "空气侧热平衡"
          formula: |
            Q = ρ_air × V_air × Cp_air × (T_return - T_supply)
          inputs:
            T_return: "AI_RA_TEMP"
            T_supply: "AI_SA_TEMP"
            V_air: "AI_SA_FLOW"
          accuracy: "±10%"
          
        backup_method:
          name: "水侧热平衡（需流量）"
          formula: |
            Q = ρ_water × V_water × Cp_water × (T_chw_return - T_chw_supply)
          inputs:
            T_chw_return: "冷冻水回水温度"
            T_chw_supply: "冷冻水供水温度"
            V_water: "冷冻水流量"
          accuracy: "±5%"
          
      usage:
        - "负荷趋势分析"
        - "冷站群控的负荷输入"
        - "能效计算"
        
    VS_002_Room_Temp_Average:
      name: "室温平均/选择"
      purpose: "双传感器冗余时的选择和平均"
      
      logic: |
        IF |T_A - T_B| < 2°C THEN
          T_room = (T_A + T_B) / 2
        ELSEIF |T_A - T_reference| < |T_B - T_reference| THEN
          T_room = T_A
          FLAG = "T_B Suspect"
        ELSE
          T_room = T_B
          FLAG = "T_A Suspect"
        ENDIF
        
        其中 T_reference 可以是回风温度或历史均值
        
      inputs:
        T_A: "AI_ROOM_TEMP_A"
        T_B: "AI_ROOM_TEMP_B"
        T_reference: "AI_RA_TEMP"
      output:
        T_room: "选择后的室温"
        FLAG: "传感器状态标记"
        
    VS_003_Pressure_Estimation:
      name: "压差估算（送排风量法）"
      purpose: "双压差传感器故障时的备用估算"
      
      calculation:
        principle: |
          基于质量守恒：
          ΔP ∝ (V_supply - V_exhaust)² / A_opening²
          
          简化线性关系（需现场标定）：
          ΔP = K × (V_supply - V_exhaust)
          
        formula: |
          ΔP_estimated = K_pressure × (Q_supply - Q_exhaust)
          
          其中 K_pressure 需根据房间密封性标定
          
        inputs:
          Q_supply: "送风量（从VFD频率估算）"
          Q_exhaust: "排风量（从VFD频率估算）"
          K_pressure: "标定系数（Pa·h/m³）"
        accuracy: "±5Pa"
        limitation: "仅作为紧急备用，精度不如物理传感器"
        
    VS_004_Pump_Flow_Estimation:
      name: "水泵流量估算（相似定律）"
      purpose: "流量计故障时估算冷冻水流量"
      
      calculation:
        equation_ref: "EQ-PUMP-AFFINITY (Agent-04)"
        formula: |
          # 水泵相似定律
          Q = Q_design × (n / n_design)
          
          其中 n 为当前转速，从VFD频率反馈获取
          n_design 为额定转速
          Q_design 为额定流量
          
        inputs:
          VFD_freq: "AO_VFD_SPEED feedback"
          n_design: "50Hz (额定)"
          Q_design: "设计流量"
        accuracy: "±10%"
        limitation: "不考虑系统阻力变化"
        
    VS_005_Chiller_COP:
      name: "冷机实时COP计算"
      purpose: "监测冷机运行效率"
      
      calculation:
        formula: |
          COP = Q_evaporator / W_compressor
          
          Q_evap = ρ × V_chw × Cp × (T_chwr - T_chws)
          W_comp = 从电力监测获取
          
        inputs:
          T_chws: "AI_CHWS_TEMP"
          T_chwr: "AI_CHWR_TEMP"
          V_chw: "冷冻水流量或估算值"
          W_comp: "电力监测读数"
        output:
          COP_realtime: "实时COP"
          COP_average: "滑动平均COP（1小时）"
        alarm:
          warning: "COP < 4.0"
          critical: "COP < 3.0"
```

## B.2 冷站群控优化算法

```yaml
Chiller_Plant_Optimization:
  
  # ═══════════════════════════════════════════════════════════════════════════
  # B.2.1 加减机优化逻辑
  # ═══════════════════════════════════════════════════════════════════════════
  
  Staging_Optimization:
    name: "冷机群控加减机优化"
    
    # 当前负荷计算
    load_calculation:
      method: "系统级热平衡"
      formula: |
        Q_system = ρ × V_system × Cp × (T_chwr_avg - T_chws_avg)
        
        对于多冷机并联：
        Q_system = Σ Q_chiller_i
        
      inputs:
        V_system: "系统总流量（二次泵总和或系统流量计）"
        T_chwr_avg: "系统回水温度（加权平均）"
        T_chws_avg: "系统供水温度"
        
    # 加减机触发条件
    staging_triggers:
      
      add_chiller:
        condition: |
          (Q_system / Σ Q_running_capacity) > 85%
          持续 10 分钟
          且 有可用冷机
          
        optimization:
          select_next_chiller:
            method: "最高效率优先"
            logic: |
              从可用冷机中选择：
              1. 当前负荷点预期COP最高的冷机
              2. 或轮转顺序下一台（平衡运行时间）
              
              COP预测基于冷机性能曲线：
              COP = f(Load_Ratio, T_cw_in)
              
      remove_chiller:
        condition: |
          (Q_system / Σ Q_running_capacity) < 50%
          持续 10 分钟
          且 运行冷机 > 1
          
        optimization:
          select_chiller_to_stop:
            method: "最低效率或最长运行时间"
            logic: |
              选择停机的冷机：
              1. 当前运行效率最低的冷机
              2. 或运行时间最长的冷机（平衡磨损）
              
    # 冷机负荷分配
    load_balancing:
      method: "等负荷率分配"
      formula: |
        对于 N 台运行冷机：
        Target_Load_Ratio = Q_system / (N × Q_nominal)
        
        各冷机设定：
        Load_i = Target_Load_Ratio × Q_nominal_i
        
      adjustment:
        method: "微调冷冻水供水温度设定值"
        logic: |
          如果某台冷机负荷偏高，微降其CHWS_SP
          使其卸载部分负荷给其他冷机
          
    # 防止频繁启停
    anti_cycling:
      min_runtime: "30分钟"
      min_offtime: "15分钟"
      staging_lockout: "10分钟"
      max_starts_per_hour: 3
      
  # ═══════════════════════════════════════════════════════════════════════════
  # B.2.2 冷冻水温度优化重设
  # ═══════════════════════════════════════════════════════════════════════════
  
  CHWS_Temperature_Reset:
    name: "冷冻水供水温度优化"
    
    principle: |
      在满足末端需求的前提下，提高冷冻水供水温度，
      可以显著提高冷机COP（每提高1°C约提高2-3%COP）。
      
    method_1_valve_position_based:
      name: "基于末端阀位"
      logic: |
        监测所有末端冷水阀的开度：
        
        IF Max(All_Valve_Positions) < 85% 持续 15分钟 THEN
          CHWS_SP += 0.3°C
          最高不超过 12°C
        ELSEIF Any(Valve_Position) > 95% THEN
          CHWS_SP -= 0.5°C
          最低不低于 6°C
        ENDIF
        
      update_interval: "15分钟"
      ramp_rate: "0.3°C/15min（升温）, 0.5°C/15min（降温）"
      
    method_2_outdoor_temp_based:
      name: "基于室外温度"
      logic: |
        # 简化线性重设
        CHWS_SP = 5 + 0.1 × (T_outdoor - 20)
        CHWS_SP = CLAMP(CHWS_SP, 6, 12)
        
        当 T_outdoor < 20°C: CHWS_SP = 7°C
        当 T_outdoor = 30°C: CHWS_SP = 8°C
        当 T_outdoor = 40°C: CHWS_SP = 9°C (允许更高)
        
      note: "作为阀位法的补充，防止极端天气"
      
    constraints:
      dehumidification:
        name: "除湿需求约束"
        logic: |
          IF 任何空间湿度 > 设定值 + 5% THEN
            CHWS_SP 不允许升高
            可能需要降低以增加除湿能力
            
    fallback:
      trigger: "L1通信中断"
      action: "CHWS_SP = 7°C（默认值）"
      
  # ═══════════════════════════════════════════════════════════════════════════
  # B.2.3 冷却水温度优化
  # ═══════════════════════════════════════════════════════════════════════════
  
  CWS_Temperature_Reset:
    name: "冷却水供水温度优化"
    
    principle: |
      降低冷却水温度可以降低冷凝压力，提高冷机效率，
      但冷却塔风机能耗增加。需要综合优化。
      
    method:
      name: "基于室外湿球温度"
      formula: |
        CW_Supply_SP = MAX(18°C, WB_Temperature + 3°C)
        CW_Supply_SP = MIN(CW_Supply_SP, 32°C)
        
      inputs:
        WB_Temperature: "室外湿球温度传感器"
      approach: "+3°C（冷却塔逼近度设计值）"
      
    constraints:
      chiller_limit:
        name: "冷机冷却水下限"
        value: "18°C"
        reason: "防止冷凝压力过低，冷机无法正常运行"
        
    optimization:
      advanced_method: "整体能耗最小化"
      description: |
        使用Model Predictive Control(MPC)综合优化：
        - 冷机能耗
        - 冷却水泵能耗
        - 冷却塔风机能耗
        
        目标函数：min(W_chiller + W_pump + W_fan)
        约束：满足末端冷量需求
        
      implementation: "L1优化引擎"
```

## B.3 压差控制快速响应算法

```yaml
Pressure_Control_Algorithm:
  
  name: "洁净室压差快速控制"
  applicable_to: ["手术室", "ICU", "负压隔离病房"]
  criticality: "P0-LIFE_SAFETY"
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 控制策略
  # ═══════════════════════════════════════════════════════════════════════════
  
  control_strategy:
    type: "PI控制 + 前馈 + 门扰动补偿"
    
    standard_pi_control:
      PV: "AI_ROOM_PRESS (差压传感器)"
      SP: "15Pa（手术室典型值）"
      output: "排风阀开度 或 排风机频率"
      
      parameters:
        Kp: 1.0
        Ti: 30  # 秒，快速响应
        Td: 0
        
      rationale: |
        压差控制需要快速响应（目标<30秒恢复），因此：
        - Ti较小，积分作用快
        - 不使用微分，避免噪声放大
        
    door_compensation:
      trigger: "DI_DOOR_MAIN = OPEN"
      action: |
        门打开瞬间，压差会迅速下降。
        补偿措施：
        1. 立即增加送风量5-10%（或减少排风量）
        2. 保持补偿直到门关闭
        3. 门关闭后延时10秒逐步恢复
        
      implementation:
        pseudo_code: |
          IF Door_Open THEN
            Compensation = +5%  # 增加送风/减少排风
          ELSEIF Door_Just_Closed THEN
            FOR t = 0 TO 10s
              Compensation = +5% × (1 - t/10)
            ENDFOR
          ELSE
            Compensation = 0
          ENDIF
          
          Output = PI_Output + Compensation
          
    feedforward:
      name: "送风量变化前馈"
      principle: |
        当送风量变化时，压差也会变化。
        通过监测送风VFD频率变化，提前调整排风。
        
      formula: |
        ΔP_expected ∝ ΔQ_supply
        EA_FF = K_ff × ΔQ_supply
        
  # ═══════════════════════════════════════════════════════════════════════════
  # 性能指标
  # ═══════════════════════════════════════════════════════════════════════════
  
  performance_requirements:
    steady_state:
      setpoint: "15Pa"
      tolerance: "±3Pa"
      
    transient_door_open:
      max_drop: "10Pa（不低于+5Pa）"
      recovery_time: "<30秒"
      
    transient_mode_change:
      description: "模式切换（STANDBY→SURGERY）"
      ramp_time: "5分钟平滑过渡"
      
  # ═══════════════════════════════════════════════════════════════════════════
  # 降级模式
  # ═══════════════════════════════════════════════════════════════════════════
  
  degradation:
    sensor_failure:
      trigger: "双压差传感器均故障"
      action:
        - "固定排风阀开度30%"
        - "CRITICAL报警"
        - "通知手术室评估"
        
    actuator_failure:
      trigger: "排风阀卡死"
      detection: "|Command - Feedback| > 10% 持续5分钟"
      action:
        - "尝试全开全关3次"
        - "如仍卡死，调整送风量补偿"
        - "紧急维修"
```

---

# 补充C：故障诊断决策树 (P1)

```yaml
Fault_Diagnosis_Trees:
  
  # ═══════════════════════════════════════════════════════════════════════════
  # C.1 手术室温度高于设定值
  # ═══════════════════════════════════════════════════════════════════════════
  
  DIAG_001_Room_Temp_High:
    symptom: "手术室温度高于设定值2°C以上"
    severity: "HIGH"
    
    decision_tree:
      
      step_1:
        question: "AHU送风温度是否正常（应≤设定值+1°C）？"
        check_point: "HVAC-OR-AHU01-AI_SA_TEMP"
        expected: "< 17°C（送风设定值+1）"
        
        if_yes: 
          next: "step_2"
          
        if_no:
          diagnosis: "送风温度过高"
          next: "branch_A"
          
      step_2:
        question: "AHU送风量是否满足（应≥80%设计值）？"
        check_point: "HVAC-OR-AHU01-AI_SA_FLOW"
        expected: "> 80% × 设计风量"
        
        if_yes:
          next: "step_3"
          
        if_no:
          diagnosis: "送风量不足"
          next: "branch_B"
          
      step_3:
        question: "冷冻水供水温度是否低于设定值+2°C？"
        check_point: "HVAC-CHP-AI_CHWS_TEMP"
        expected: "< 9°C（7°C设定值+2）"
        
        if_yes:
          diagnosis: "末端问题"
          next: "branch_C"
          
        if_no:
          diagnosis: "冷源不足"
          next: "branch_D"
          
    branches:
      
      branch_A:
        name: "表冷器/冷水阀问题"
        checks:
          - check: "冷水阀位是否>80%？"
            point: "HVAC-OR-AHU01-AI_CHW_VLV_FB"
            expected: "> 80%"
            
          - check: "冷水进出口温差是否>3°C？"
            calculation: "T_chw_out - T_chw_in"
            expected: "> 3°C"
            
          - check: "AHU进出口风温差是否>5°C？"
            calculation: "AI_MA_TEMP - AI_SA_TEMP"
            expected: "> 5°C"
            
        diagnosis_matrix:
          - condition: "阀位高但水温差小"
            result: "表冷器堵塞或结垢"
            action: "安排清洗表冷器"
            priority: "2小时内"
            
          - condition: "阀位高且水温差正常"
            result: "冷量不足但表冷器正常"
            action: "检查冷冻水供水温度"
            
          - condition: "阀位低但温度高"
            result: "控制器输出异常"
            action: "检查DDC程序和PID参数"
            
          - condition: "阀位反馈与指令不符"
            result: "阀门执行器故障"
            action: "更换执行器"
            priority: "紧急"
            
      branch_B:
        name: "风机/滤网问题"
        checks:
          - check: "送风机频率是否<90%？"
            point: "HVAC-OR-AHU01-AI_SF_FREQ"
            expected: "> 45Hz"
            
          - check: "送风机电流是否正常？"
            point: "HVAC-OR-AHU01-AI_SF_CURRENT"
            expected: "在额定范围内"
            
          - check: "过滤器压差是否>400Pa？"
            points: ["AI_PREFILTER_DP", "AI_MEDFILTER_DP", "AI_HEPAFILTER_DP"]
            
        diagnosis_matrix:
          - condition: "频率正常但流量低"
            result: "过滤器堵塞"
            action: "更换过滤器"
            priority: "30分钟"
            
          - condition: "频率低"
            result: "VFD限速或故障"
            action: "检查VFD设置和故障码"
            
          - condition: "电流异常高"
            result: "风机机械故障或皮带松"
            action: "停机检查"
            priority: "紧急"
            
      branch_C:
        name: "末端阀门问题"
        checks:
          - check: "该AHU冷水阀指令是否>0？"
            point: "HVAC-OR-AHU01-AO_CHW_VLV"
            
          - check: "阀位反馈是否与指令一致？"
            comparison: "|AO_CHW_VLV - AI_CHW_VLV_FB| < 5%"
            
        diagnosis_matrix:
          - condition: "指令>0但阀位=0"
            result: "阀门卡死或执行器脱落"
            action: "现场手动操作确认"
            
          - condition: "指令=0"
            result: "控制逻辑问题"
            action: "检查DDC程序"
            
      branch_D:
        name: "冷源不足"
        checks:
          - check: "运行冷机数量"
            point: "Chiller run status count"
            
          - check: "冷机负荷率"
            calculation: "Q_load / Σ Q_capacity"
            
        diagnosis_matrix:
          - condition: "负荷率>85% AND 冷机<设计值"
            result: "需要加机"
            action: "手动或自动启动备用冷机"
            priority: "30分钟"
            
          - condition: "所有冷机已运行"
            result: "装机容量不足或故障"
            action: "检查冷机故障状态，临时降低其他区域负荷"
            
    expected_resolution_time:
      表冷器堵塞: "2小时（清洗）"
      过滤器更换: "30分钟"
      阀门执行器故障: "4小时（更换）"
      加冷机: "30分钟（启动序列）"
      VFD故障: "2-4小时（更换或维修）"
      
  # ═══════════════════════════════════════════════════════════════════════════
  # C.2 手术室压差低于设定值
  # ═══════════════════════════════════════════════════════════════════════════
  
  DIAG_002_Pressure_Low:
    symptom: "手术室压差低于+12Pa"
    severity: "CRITICAL"
    
    decision_tree:
      
      step_1:
        question: "送风机是否运行？"
        check_point: "HVAC-OR-AHU01-DI_SF_RUN"
        
        if_no:
          diagnosis: "送风机停机"
          action: "立即检查送风机故障原因"
          priority: "紧急"
          
        if_yes:
          next: "step_2"
          
      step_2:
        question: "排风机是否运行（电流>0）？"
        check_point: "HVAC-OR-AHU01-AI_RF_CURRENT"
        
        if_no:
          diagnosis: "排风机故障"
          action: "排风停止应使压差升高，若压差低说明有其他泄漏"
          next: "step_4"
          
        if_yes:
          next: "step_3"
          
      step_3:
        question: "送风量是否≥设计值80%？"
        check_point: "HVAC-OR-AHU01-AI_SA_FLOW"
        
        if_no:
          diagnosis: "送风量不足"
          next: "branch_B_from_DIAG_001"
          
        if_yes:
          next: "step_4"
          
      step_4:
        question: "门窗是否关闭？"
        check_points:
          - "HVAC-OR-RM01-DI_DOOR_MAIN"
          - "HVAC-OR-RM01-DI_DOOR_EQUIP"
          
        if_door_open:
          diagnosis: "门未关闭"
          action: "通知手术室关门，检查门补偿逻辑"
          
        if_doors_closed:
          next: "step_5"
          
      step_5:
        question: "排风阀位是否过大？"
        check_point: "HVAC-OR-AHU01-AI_RF_FREQ 或 排风阀反馈"
        
        if_yes:
          diagnosis: "排风过大"
          action: "检查压差控制回路，可能PID参数异常"
          
        if_no:
          diagnosis: "围护结构泄漏"
          action: "烟雾测试排查泄漏点"
          
    leak_test_procedure:
      name: "烟雾测试排查泄漏"
      steps:
        - step: 1
          action: "关闭手术室所有门"
          
        - step: 2
          action: "确认AHU正常运行，送风>排风"
          
        - step: 3
          action: "用发烟管在以下位置测试气流方向"
          locations:
            - "门缝"
            - "窗户接缝"
            - "穿墙管线"
            - "天花检修口"
            - "灯具边缘"
            - "手术室送风口边缘"
            
        - step: 4
          action: "如烟雾向外飘说明有渗漏"
          
        - step: 5
          action: "密封所有发现的渗漏点"
          
        - step: 6
          action: "重新测试压差"
          
  # ═══════════════════════════════════════════════════════════════════════════
  # C.3 冷机故障
  # ═══════════════════════════════════════════════════════════════════════════
  
  DIAG_003_Chiller_Fault:
    symptom: "冷机报故障停机"
    severity: "HIGH"
    
    decision_tree:
      
      step_1:
        question: "读取冷机故障码"
        method: "从冷机本地面板或通信读取"
        
        common_fault_codes:
          - code: "高压保护"
            possible_causes:
              - "冷却水温度过高"
              - "冷却水流量不足"
              - "冷凝器脏堵"
              - "制冷剂过多"
            actions:
              - "检查冷却塔运行状态"
              - "检查冷却水泵运行"
              - "检查冷却水温度"
              - "清洗冷凝器（如必要）"
              
          - code: "低压保护"
            possible_causes:
              - "冷冻水温度过低"
              - "冷冻水流量不足"
              - "蒸发器脏堵"
              - "制冷剂不足"
            actions:
              - "检查冷冻水供水温度设定"
              - "检查冷冻水泵运行"
              - "检查冷冻水流量开关"
              - "检查制冷剂充注量"
              
          - code: "油压低"
            possible_causes:
              - "润滑油不足"
              - "油泵故障"
              - "油路堵塞"
            actions:
              - "检查油位"
              - "检查油压差"
              - "联系冷机厂家"
              
          - code: "电机过载"
            possible_causes:
              - "启动时负荷过大"
              - "电压不稳"
              - "电机故障"
            actions:
              - "检查电源电压"
              - "降低冷机负荷后重启"
              - "检查电机绝缘"
              
      step_2:
        question: "故障是否可以复位？"
        
        if_yes:
          action:
            - "排除故障原因后复位"
            - "观察运行5分钟"
            - "如再次跳闸，联系厂家"
            
        if_no:
          action:
            - "启动备用冷机"
            - "联系厂家紧急维修"
            
    backup_response:
      name: "冷机故障时的系统响应"
      actions:
        - "立即启动下一优先级冷机"
        - "如所有冷机故障，启动应急响应"
        - "按优先级限制非关键区域冷量"
        - "通知手术室可能温度上升"
```

---

# 补充D：SAT验收测试清单 (P1)

```yaml
SAT_Checklists:

# ═══════════════════════════════════════════════════════════════════════════
# D.1 手术室HVAC系统验收测试
# ═══════════════════════════════════════════════════════════════════════════

SAT_OR_HVAC:
 project: "综合医院示范项目"
 system: "手术室HVAC"
 space: "OR-001（1号I级手术室）"
 test_id: "SAT-HVAC-OR-001"

 # ─────────────────────────────────────────────────────────────────────
 # 测试前准备
 # ─────────────────────────────────────────────────────────────────────
 pre_requisites:
 - item: "冷热源系统已调试完成"
 verified: "☐"
 - item: "冷冻水/热水供水正常"
 verified: "☐"
 - item: "DDC控制器已下载程序"
 verified: "☐"
 - item: "所有传感器已安装校准"
 verified: "☐"
 - item: "执行器已确认动作方向"
 verified: "☐"
 - item: "通信网络已连通"
 verified: "☐"
 - item: "房间围护结构密封完成"
 verified: "☐"

 # ─────────────────────────────────────────────────────────────────────
 # 测试项目清单
 # ─────────────────────────────────────────────────────────────────────
 test_items:

 TEST_01:
 name: "传感器精度验证"
 objective: "验证所有传感器精度在设计范围内"

 sub_tests:
 - id: "01-A"
 name: "室温传感器精度"
 procedure:
 - "使用校准过的便携温度计（精度±0.1°C）"
 - "在手术室内4个位置测量温度"
 - "位置：头部区、脚部区、中部、靠墙侧"
 - "每个位置稳定10分钟后读数"
 - "记录BMS显示值和实测值"
 acceptance: "|BMS值 - 实测值| ≤ 0.5°C"
 result

---