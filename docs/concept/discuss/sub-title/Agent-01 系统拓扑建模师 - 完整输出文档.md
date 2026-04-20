## 🧑‍💻 User


那么将Batch 1-7整合为一份完整的输出，同时根据你的检查结果，做适当的增补和完善

---
## 🤖 Assistant


由于内容非常庞大（46个系统的完整拓扑定义），我将分多个部分输出完整的整合文档。

---

# Agent-01 系统拓扑建模师 - 完整输出文档

## 文档信息

```yaml
Document_Metadata:
  title: 医院机电系统拓扑模型完整定义
  version: 2.0.0
  schema_version: "2.0"
  created_date: 2024-01-15
  last_updated: 2024-01-15
  author: Agent-01 系统拓扑建模师
  
  scope:
    building_type: 综合医院
    scale: 800-1200床
    systems_count: 46
    
  document_structure:
    - Part 1: 总则与目录
    - Part 2: 介质类型定义
    - Part 3: HVAC系统拓扑 (11系统)
    - Part 4: ELECTRICAL系统拓扑 (9系统)
    - Part 5: PLUMBING系统拓扑 (7系统)
    - Part 6: FIRE_PROTECTION系统拓扑 (5系统)
    - Part 7: MEDICAL_GAS系统拓扑 (8系统)
    - Part 8: INTELLIGENT系统拓扑 (8系统)
    - Part 9: 跨系统接口矩阵
    - Part 10: 全局验证与索引
```

---

# Part 1: 总则与目录

## 1.1 系统完整目录

```yaml
System_Catalog:

  # ==========================================================================
  # HVAC 暖通空调系统 (11个系统)
  # ==========================================================================
  - category_id: HVAC
    category_name: 暖通空调系统
    category_name_en: HVAC Systems
    
    systems:
      # P1-CRITICAL
      - system_id: HVAC-CHP
        system_name: 冷热源系统
        system_name_en: Chiller/Heater Plant System
        priority: P1-CRITICAL
        primary_medium: [CHW, HW]
        
      - system_id: HVAC-CHW
        system_name: 冷冻水系统
        system_name_en: Chilled Water System
        priority: P1-CRITICAL
        primary_medium: CHW
        
      - system_id: HVAC-HW
        system_name: 热水系统
        system_name_en: Heating Water System
        priority: P1-CRITICAL
        primary_medium: HW
        
      - system_id: HVAC-CW
        system_name: 冷却水系统
        system_name_en: Condenser Water System
        priority: P1-CRITICAL
        primary_medium: CW
        
      - system_id: HVAC-AHU
        system_name: 组合式空调系统
        system_name_en: Air Handling Unit System
        priority: P1-CRITICAL
        primary_medium: [AIR-SA, AIR-RA]
        
      - system_id: HVAC-CLEAN
        system_name: 洁净空调系统
        system_name_en: Clean Room HVAC System
        priority: P1-CRITICAL
        primary_medium: AIR-CLEAN
        
      # P2-IMPORTANT
      - system_id: HVAC-FCU
        system_name: 风机盘管系统
        system_name_en: Fan Coil Unit System
        priority: P2-IMPORTANT
        primary_medium: [CHW, AIR-SA]
        
      - system_id: HVAC-PAU
        system_name: 新风机组系统
        system_name_en: Primary Air Unit System
        priority: P2-IMPORTANT
        primary_medium: [AIR-OA, AIR-SA]
        
      - system_id: HVAC-EXHAUST
        system_name: 排风系统
        system_name_en: Exhaust Air System
        priority: P2-IMPORTANT
        primary_medium: AIR-EA
        
      - system_id: HVAC-SMOKE
        system_name: 防排烟系统
        system_name_en: Smoke Control System
        priority: P1-CRITICAL
        primary_medium: AIR-SMOKE
        
      - system_id: HVAC-VENT
        system_name: 普通通风系统
        system_name_en: General Ventilation System
        priority: P2-IMPORTANT
        primary_medium: AIR-EA

  # ==========================================================================
  # ELECTRICAL 电气系统 (9个系统)
  # ==========================================================================
  - category_id: ELECTRICAL
    category_name: 电气系统
    category_name_en: Electrical Systems
    
    systems:
      # P1-CRITICAL
      - system_id: ELEC-HV
        system_name: 高压配电系统
        system_name_en: High Voltage Distribution System
        priority: P1-CRITICAL
        primary_medium: ELEC-HV
        
      - system_id: ELEC-LV-MAIN
        system_name: 低压主配电系统
        system_name_en: Low Voltage Main Distribution System
        priority: P1-CRITICAL
        primary_medium: ELEC-LV
        
      - system_id: ELEC-EPS
        system_name: 应急电源系统
        system_name_en: Emergency Power Supply System
        priority: P1-CRITICAL
        primary_medium: ELEC-EPS
        
      - system_id: ELEC-UPS
        system_name: 不间断电源系统
        system_name_en: Uninterruptible Power Supply System
        priority: P1-CRITICAL
        primary_medium: ELEC-UPS
        
      - system_id: ELEC-IT
        system_name: 隔离电源系统
        system_name_en: Isolated Power System
        priority: P1-CRITICAL
        primary_medium: ELEC-IT
        
      - system_id: ELEC-GROUND
        system_name: 接地与防雷系统
        system_name_en: Grounding and Lightning Protection System
        priority: P1-CRITICAL
        primary_medium: GROUND
        
      # P2-IMPORTANT
      - system_id: ELEC-LIGHT
        system_name: 照明系统
        system_name_en: Lighting System
        priority: P2-IMPORTANT
        primary_medium: ELEC-LV
        
      - system_id: ELEC-SPD
        system_name: 电涌保护系统
        system_name_en: Surge Protection Device System
        priority: P2-IMPORTANT
        primary_medium: ELEC-LV
        
      # P3-OPTIONAL
      - system_id: ELEC-SOLAR
        system_name: 光伏发电系统
        system_name_en: Photovoltaic Power System
        priority: P3-OPTIONAL
        primary_medium: ELEC-DC

  # ==========================================================================
  # PLUMBING 给排水系统 (7个系统)
  # ==========================================================================
  - category_id: PLUMBING
    category_name: 给排水系统
    category_name_en: Plumbing Systems
    
    systems:
      # P1-CRITICAL
      - system_id: PLUMB-DWS
        system_name: 生活给水系统
        system_name_en: Domestic Water Supply System
        priority: P1-CRITICAL
        primary_medium: WATER-DW
        
      - system_id: PLUMB-HWS
        system_name: 生活热水系统
        system_name_en: Domestic Hot Water System
        priority: P1-CRITICAL
        primary_medium: WATER-HW
        
      - system_id: PLUMB-SAN
        system_name: 污废水排水系统
        system_name_en: Sanitary Drainage System
        priority: P1-CRITICAL
        primary_medium: WATER-SAN
        
      # P2-IMPORTANT
      - system_id: PLUMB-PURE
        system_name: 纯水系统
        system_name_en: Purified Water System
        priority: P2-IMPORTANT
        primary_medium: WATER-PURE
        
      - system_id: PLUMB-POOL
        system_name: 水池水箱系统
        system_name_en: Water Storage System
        priority: P2-IMPORTANT
        primary_medium: WATER-DW
        
      # P3-OPTIONAL
      - system_id: PLUMB-STORM
        system_name: 雨水排水系统
        system_name_en: Storm Water Drainage System
        priority: P3-OPTIONAL
        primary_medium: WATER-STORM
        
      - system_id: PLUMB-RW
        system_name: 中水回用系统
        system_name_en: Reclaimed Water System
        priority: P3-OPTIONAL
        primary_medium: WATER-RW

  # ==========================================================================
  # FIRE_PROTECTION 消防系统 (5个系统)
  # ==========================================================================
  - category_id: FIRE_PROTECTION
    category_name: 消防系统
    category_name_en: Fire Protection Systems
    
    systems:
      # P1-CRITICAL
      - system_id: FIRE-HYDRANT
        system_name: 消火栓系统
        system_name_en: Fire Hydrant System
        priority: P1-CRITICAL
        primary_medium: WATER-FIRE
        
      - system_id: FIRE-SPRINKLER
        system_name: 自动喷淋系统
        system_name_en: Automatic Sprinkler System
        priority: P1-CRITICAL
        primary_medium: WATER-FIRE
        
      - system_id: FIRE-ALARM
        system_name: 火灾自动报警系统
        system_name_en: Fire Alarm System
        priority: P1-CRITICAL
        primary_medium: SIGNAL-FA
        
      - system_id: FIRE-GAS
        system_name: 气体灭火系统
        system_name_en: Gas Fire Suppression System
        priority: P1-CRITICAL
        primary_medium: GAS-FIRE
        
      # 注：FIRE-SMOKE与HVAC-SMOKE共用
      - system_id: FIRE-SMOKE
        system_name: 防排烟系统
        system_name_en: Smoke Control System
        priority: P1-CRITICAL
        reference: HVAC-SMOKE

  # ==========================================================================
  # MEDICAL_GAS 医疗气体系统 (8个系统)
  # ==========================================================================
  - category_id: MEDICAL_GAS
    category_name: 医疗气体系统
    category_name_en: Medical Gas Systems
    
    systems:
      # P1-CRITICAL
      - system_id: MGAS-O2
        system_name: 医用氧气系统
        system_name_en: Medical Oxygen System
        priority: P1-CRITICAL
        primary_medium: GAS-O2
        
      - system_id: MGAS-VAC
        system_name: 医用负压吸引系统
        system_name_en: Medical Vacuum System
        priority: P1-CRITICAL
        primary_medium: GAS-VAC
        
      - system_id: MGAS-AIR
        system_name: 医用压缩空气系统
        system_name_en: Medical Compressed Air System
        priority: P1-CRITICAL
        primary_medium: GAS-AIR
        
      - system_id: MGAS-AGSS
        system_name: 麻醉废气排放系统
        system_name_en: Anesthetic Gas Scavenging System
        priority: P1-CRITICAL
        primary_medium: GAS-AGSS
        
      # P2-IMPORTANT
      - system_id: MGAS-N2O
        system_name: 笑气系统
        system_name_en: Nitrous Oxide System
        priority: P2-IMPORTANT
        primary_medium: GAS-N2O
        
      - system_id: MGAS-N2
        system_name: 医用氮气系统
        system_name_en: Medical Nitrogen System
        priority: P2-IMPORTANT
        primary_medium: GAS-N2
        
      - system_id: MGAS-CO2
        system_name: 医用二氧化碳系统
        system_name_en: Medical Carbon Dioxide System
        priority: P2-IMPORTANT
        primary_medium: GAS-CO2
        
      # P3-OPTIONAL
      - system_id: MGAS-SPECIAL
        system_name: 特殊气体系统
        system_name_en: Special Gas System
        priority: P3-OPTIONAL
        primary_medium: [GAS-He, GAS-Ar]
        note: 氦气、氩气等特殊医用气体

  # ==========================================================================
  # INTELLIGENT 智能化系统 (8个系统)
  # ==========================================================================
  - category_id: INTELLIGENT
    category_name: 智能化系统
    category_name_en: Intelligent Building Systems
    
    systems:
      # P1-CRITICAL
      - system_id: INT-BA
        system_name: 楼宇自控系统
        system_name_en: Building Automation System
        priority: P1-CRITICAL
        primary_medium: DATA-BA
        
      - system_id: INT-NURSE
        system_name: 护理呼叫系统
        system_name_en: Nurse Call System
        priority: P1-CRITICAL
        primary_medium: SIGNAL-NURSE
        
      # P2-IMPORTANT
      - system_id: INT-SEC
        system_name: 安防监控系统
        system_name_en: Security System
        priority: P2-IMPORTANT
        primary_medium: DATA-IP
        
      - system_id: INT-NET
        system_name: 综合布线与网络系统
        system_name_en: Structured Cabling and Network System
        priority: P2-IMPORTANT
        primary_medium: DATA-IP
        
      - system_id: INT-PA
        system_name: 公共广播系统
        system_name_en: Public Address System
        priority: P2-IMPORTANT
        primary_medium: SIGNAL-AUDIO
        
      - system_id: INT-CLOCK
        system_name: 时钟系统
        system_name_en: Master Clock System
        priority: P2-IMPORTANT
        primary_medium: SIGNAL-TIME
        
      - system_id: INT-IBMS
        system_name: 智能化集成平台
        system_name_en: Intelligent Building Management System
        priority: P2-IMPORTANT
        primary_medium: DATA-IP
        
      # P3-OPTIONAL
      - system_id: INT-IPTV
        system_name: 病房电视系统
        system_name_en: Inpatient IPTV System
        priority: P3-OPTIONAL
        primary_medium: DATA-IP
```

## 1.2 优先级分布统计

```yaml
Priority_Distribution:

  P1-CRITICAL:
    count: 18
    systems:
      - HVAC-CHP, HVAC-CHW, HVAC-HW, HVAC-CW, HVAC-AHU, HVAC-CLEAN, HVAC-SMOKE
      - ELEC-HV, ELEC-LV-MAIN, ELEC-EPS, ELEC-UPS, ELEC-IT, ELEC-GROUND
      - PLUMB-DWS, PLUMB-HWS, PLUMB-SAN
      - FIRE-HYDRANT, FIRE-SPRINKLER, FIRE-ALARM, FIRE-GAS
      - MGAS-O2, MGAS-VAC, MGAS-AIR, MGAS-AGSS
      - INT-BA, INT-NURSE
      
  P2-IMPORTANT:
    count: 15
    systems:
      - HVAC-FCU, HVAC-PAU, HVAC-EXHAUST, HVAC-VENT
      - ELEC-LIGHT, ELEC-SPD
      - PLUMB-PURE, PLUMB-POOL
      - MGAS-N2O, MGAS-N2, MGAS-CO2
      - INT-SEC, INT-NET, INT-PA, INT-CLOCK, INT-IBMS
      
  P3-OPTIONAL:
    count: 5
    systems:
      - ELEC-SOLAR
      - PLUMB-STORM, PLUMB-RW
      - MGAS-SPECIAL
      - INT-IPTV
```

---

# Part 2: 介质类型定义

```yaml
Medium_Types:

  # ==========================================================================
  # 水介质 (Water Media)
  # ==========================================================================
  Water_Media:
  
    - medium_id: CHW
      medium_name: 冷冻水
      medium_name_en: Chilled Water
      category: HVAC
      typical_properties:
        supply_temperature: {value: 7, unit: ℃}
        return_temperature: {value: 12, unit: ℃}
        delta_t: {value: 5, unit: ℃}
        pressure: {value: 0.4-0.8, unit: MPa}
      color_code: 绿色
      
    - medium_id: HW
      medium_name: 空调热水
      medium_name_en: Heating Water
      category: HVAC
      typical_properties:
        supply_temperature: {value: 60, unit: ℃}
        return_temperature: {value: 50, unit: ℃}
        delta_t: {value: 10, unit: ℃}
        pressure: {value: 0.4-0.8, unit: MPa}
      color_code: 红色
      
    - medium_id: CW
      medium_name: 冷却水
      medium_name_en: Condenser Water
      category: HVAC
      typical_properties:
        supply_temperature: {value: 32, unit: ℃}
        return_temperature: {value: 37, unit: ℃}
        delta_t: {value: 5, unit: ℃}
        pressure: {value: 0.3-0.5, unit: MPa}
      color_code: 蓝绿色
      
    - medium_id: WATER-DW
      medium_name: 生活给水
      medium_name_en: Domestic Water
      category: PLUMBING
      typical_properties:
        temperature: {value: 5-25, unit: ℃}
        pressure: {value: 0.15-0.35, unit: MPa}
        quality: GB 5749生活饮用水标准
      color_code: 蓝色
      
    - medium_id: WATER-HW
      medium_name: 生活热水
      medium_name_en: Domestic Hot Water
      category: PLUMBING
      typical_properties:
        supply_temperature: {value: 55-60, unit: ℃}
        return_temperature: {value: 50, unit: ℃}
        pressure: {value: 0.15-0.35, unit: MPa}
      color_code: 红色
      
    - medium_id: WATER-SAN
      medium_name: 污废水
      medium_name_en: Sanitary Water
      category: PLUMBING
      typical_properties:
        type: 重力流
        pH: {value: 6-9, unit: null}
      color_code: 黑色
      
    - medium_id: WATER-STORM
      medium_name: 雨水
      medium_name_en: Storm Water
      category: PLUMBING
      typical_properties:
        type: 重力流
      color_code: 灰色
      
    - medium_id: WATER-RW
      medium_name: 中水
      medium_name_en: Reclaimed Water
      category: PLUMBING
      typical_properties:
        quality: GB/T 18920城市杂用水标准
        usage: [冲厕, 绿化, 道路冲洗]
      color_code: 浅绿色
      
    - medium_id: WATER-FIRE
      medium_name: 消防水
      medium_name_en: Fire Water
      category: FIRE_PROTECTION
      typical_properties:
        pressure_hydrant: {value: 0.35-0.5, unit: MPa}
        pressure_sprinkler: {value: 0.1-0.15, unit: MPa}
      color_code: 红色
      
    - medium_id: WATER-PURE
      medium_name: 纯水
      medium_name_en: Purified Water
      category: PLUMBING
      typical_properties:
        resistivity: {value: ">10", unit: MΩ·cm}
        toc: {value: "<500", unit: ppb}
        bacteria: {value: "<100", unit: CFU/mL}
      color_code: 白色

  # ==========================================================================
  # 空气介质 (Air Media)
  # ==========================================================================
  Air_Media:
  
    - medium_id: AIR-OA
      medium_name: 室外新风
      medium_name_en: Outdoor Air
      category: HVAC
      typical_properties:
        temperature: 室外设计参数
        humidity: 室外设计参数
      
    - medium_id: AIR-SA
      medium_name: 送风
      medium_name_en: Supply Air
      category: HVAC
      typical_properties:
        temperature_summer: {value: 14-18, unit: ℃}
        temperature_winter: {value: 35-45, unit: ℃}
        
    - medium_id: AIR-RA
      medium_name: 回风
      medium_name_en: Return Air
      category: HVAC
      typical_properties:
        temperature_summer: {value: 25-27, unit: ℃}
        temperature_winter: {value: 18-22, unit: ℃}
        
    - medium_id: AIR-EA
      medium_name: 排风
      medium_name_en: Exhaust Air
      category: HVAC
      typical_properties:
        destination: 室外排放
        
    - medium_id: AIR-CLEAN
      medium_name: 洁净送风
      medium_name_en: Clean Room Supply Air
      category: HVAC
      typical_properties:
        cleanliness_levels:
          - {class: ISO5, particles: "≤3520/m³@0.5μm"}
          - {class: ISO6, particles: "≤35200/m³@0.5μm"}
          - {class: ISO7, particles: "≤352000/m³@0.5μm"}
          - {class: ISO8, particles: "≤3520000/m³@0.5μm"}
          
    - medium_id: AIR-SMOKE
      medium_name: 烟气
      medium_name_en: Smoke
      category: FIRE_PROTECTION
      typical_properties:
        exhaust_velocity: {value: "≥15", unit: m/s}
        temperature: {value: 280, unit: ℃, note: 设计温度}

  # ==========================================================================
  # 电力介质 (Electrical Media)
  # ==========================================================================
  Electrical_Media:
  
    - medium_id: ELEC-HV
      medium_name: 高压电
      medium_name_en: High Voltage
      category: ELECTRICAL
      typical_properties:
        voltage: {value: 10, unit: kV}
        frequency: {value: 50, unit: Hz}
        phases: 3
        
    - medium_id: ELEC-LV
      medium_name: 低压电
      medium_name_en: Low Voltage
      category: ELECTRICAL
      typical_properties:
        voltage: {value: "380/220", unit: V}
        frequency: {value: 50, unit: Hz}
        system: "3P+N+PE"
        
    - medium_id: ELEC-EPS
      medium_name: 应急电源
      medium_name_en: Emergency Power
      category: ELECTRICAL
      typical_properties:
        voltage: {value: "380/220", unit: V}
        source: 柴油发电机
        startup_time: {value: "≤15", unit: s}
        
    - medium_id: ELEC-UPS
      medium_name: 不间断电源
      medium_name_en: UPS Power
      category: ELECTRICAL
      typical_properties:
        voltage: {value: "380/220", unit: V}
        backup_time: {value: 15-30, unit: min}
        transfer_time: {value: 0, unit: ms}
        
    - medium_id: ELEC-IT
      medium_name: 隔离电源
      medium_name_en: Isolated Power
      category: ELECTRICAL
      typical_properties:
        voltage: {value: 220, unit: V}
        grounding: 不接地系统
        insulation_monitor: 必需
        application: 2类医疗场所
        
    - medium_id: ELEC-DC
      medium_name: 直流电
      medium_name_en: DC Power
      category: ELECTRICAL
      typical_properties:
        voltage: {value: 48-750, unit: V}
        source: [光伏, 蓄电池]
        
    - medium_id: GROUND
      medium_name: 接地
      medium_name_en: Ground
      category: ELECTRICAL
      typical_properties:
        resistance: {value: "≤1", unit: Ω}
        types: [防雷接地, 保护接地, 功能接地, 等电位联结]

  # ==========================================================================
  # 医疗气体介质 (Medical Gas Media)
  # ==========================================================================
  Medical_Gas_Media:
  
    - medium_id: GAS-O2
      medium_name: 医用氧气
      medium_name_en: Medical Oxygen
      category: MEDICAL_GAS
      typical_properties:
        purity: {value: "≥99.5", unit: "%"}
        pressure_source: {value: 0.8-1.0, unit: MPa}
        pressure_terminal: {value: 0.4-0.5, unit: MPa}
        color_code: 白色
        standard: YY/T 0187
        
    - medium_id: GAS-VAC
      medium_name: 医用负压
      medium_name_en: Medical Vacuum
      category: MEDICAL_GAS
      typical_properties:
        pressure: {value: "-40 ~ -60", unit: kPa}
        flow_per_terminal: {value: 40, unit: L/min}
        color_code: 黄色
        
    - medium_id: GAS-AIR
      medium_name: 医用压缩空气
      medium_name_en: Medical Compressed Air
      category: MEDICAL_GAS
      typical_properties:
        pressure_terminal: {value: 0.4-0.5, unit: MPa}
        dew_point: {value: "≤-40", unit: ℃}
        oil_content: {value: "≤0.1", unit: mg/m³}
        particle: {value: "≤0.5", unit: μm}
        color_code: 黑白相间
        
    - medium_id: GAS-N2O
      medium_name: 笑气
      medium_name_en: Nitrous Oxide
      category: MEDICAL_GAS
      typical_properties:
        purity: {value: "≥99", unit: "%"}
        pressure_terminal: {value: 0.4-0.5, unit: MPa}
        color_code: 蓝色
        
    - medium_id: GAS-N2
      medium_name: 医用氮气
      medium_name_en: Medical Nitrogen
      category: MEDICAL_GAS
      typical_properties:
        purity: {value: "≥99.5", unit: "%"}
        pressure_terminal: {value: 0.4-0.8, unit: MPa}
        color_code: 黑色
        
    - medium_id: GAS-CO2
      medium_name: 医用二氧化碳
      medium_name_en: Medical Carbon Dioxide
      category: MEDICAL_GAS
      typical_properties:
        purity: {value: "≥99.5", unit: "%"}
        pressure_terminal: {value: 0.4-0.5, unit: MPa}
        color_code: 灰色
        application: 腹腔镜手术
        
    - medium_id: GAS-AGSS
      medium_name: 麻醉废气
      medium_name_en: Anesthetic Gas Scavenging
      category: MEDICAL_GAS
      typical_properties:
        pressure: {value: "-25 ~ -50", unit: mmH2O}
        flow_per_terminal: {value: 50, unit: L/min}
        
    - medium_id: GAS-He
      medium_name: 医用氦气
      medium_name_en: Medical Helium
      category: MEDICAL_GAS
      typical_properties:
        purity: {value: "≥99.99", unit: "%"}
        application: [MRI冷却, 肺功能检测]
        
    - medium_id: GAS-Ar
      medium_name: 医用氩气
      medium_name_en: Medical Argon
      category: MEDICAL_GAS
      typical_properties:
        purity: {value: "≥99.99", unit: "%"}
        application: 氩气刀手术

  # ==========================================================================
  # 控制与信号介质 (Control & Signal Media)
  # ==========================================================================
  Control_Signal_Media:
  
    - medium_id: DATA-IP
      medium_name: IP数据
      medium_name_en: IP Data
      category: INTELLIGENT
      typical_properties:
        protocol: TCP/IP
        speed: {value: "100M/1G/10G", unit: bps}
        
    - medium_id: DATA-BA
      medium_name: 楼控数据
      medium_name_en: BAS Data
      category: INTELLIGENT
      typical_properties:
        protocols: [BACnet, Modbus, LonWorks]
        
    - medium_id: SIGNAL-FA
      medium_name: 火警信号
      medium_name_en: Fire Alarm Signal
      category: FIRE_PROTECTION
      typical_properties:
        type: 二总线/四总线
        
    - medium_id: SIGNAL-NURSE
      medium_name: 护理呼叫信号
      medium_name_en: Nurse Call Signal
      category: INTELLIGENT
      typical_properties:
        levels: [普通呼叫, 紧急呼叫, 医护呼叫]
        
    - medium_id: SIGNAL-TIME
      medium_name: 时间信号
      medium_name_en: Time Signal
      category: INTELLIGENT
      typical_properties:
        source: [GPS, 北斗, NTP]
        accuracy: {value: "±0.5", unit: "秒/天"}
        
    - medium_id: SIGNAL-AUDIO
      medium_name: 音频信号
      medium_name_en: Audio Signal
      category: INTELLIGENT
      typical_properties:
        frequency: {value: 50-15000, unit: Hz}
        
    - medium_id: SIGNAL-VIDEO
      medium_name: 视频信号
      medium_name_en: Video Signal
      category: INTELLIGENT
      typical_properties:
        resolution: [1080P, 4K]
        protocol: [RTSP, ONVIF]
```

---

# Part 3: HVAC系统拓扑

## 3.1 HVAC-CHP 冷热源系统

```yaml
System_Topology:

# ============================================================
# 系统标识
# ============================================================
identity:
 system_id: HVAC-CHP
 system_name: 冷热源系统
 system_name_en: Chiller/Heater Plant System
 category: HVAC
 priority: P1-CRITICAL
 schema_version: "2.0"
 version: 2.0.0

 description: |
 医院中央冷热源系统，采用电制冷冷水机组+燃气锅炉的复合模式。
 夏季供冷、冬季供热、过渡季可自然冷却。
 为全院空调系统提供冷冻水和空调热水。

 design_basis:
 cooling_load: {value: 5000-8000, unit: kW, note: 单体建筑}
 heating_load: {value: 3000-5000, unit: kW}
 chw_supply: {value: 7, unit: ℃}
 chw_return: {value: 12, unit: ℃}
 hw_supply: {value: 60, unit: ℃}
 hw_return: {value: 50, unit: ℃}

 operating_modes:
 - mode: SUMMER
 description: 夏季制冷模式
 active_equipment: [冷水机组, 冷却塔]
 output: CHW

 - mode: WINTER
 description: 冬季供热模式
 active_equipment: [燃气锅炉]
 output: HW

 - mode: TRANSITION
 description: 过渡季节模式
 active_equipment: 按需运行
 output: [CHW, HW]

 serving_scope:
 - HVAC-CHW (冷冻水系统)
 - HVAC-HW (热水系统)
 - HVAC-CW (冷却水系统)

# ============================================================
# 系统边界
# ============================================================
boundary:
 inputs:
 - boundary_id: HVAC-CHP_BND_IN_ELEC
 boundary_name: 动力电源
 medium: ELEC-LV
 source_system: ELEC-LV-MAIN
 parameters:
 voltage: {value: 380, unit: V}
 note: 冷水机组/水泵动力

 - boundary_id: HVAC-CHP_BND_IN_GAS
 boundary_name: 燃气供应
 medium: GAS-NG
 is_external: true
 source: 市政燃气管网
 parameters:
 pressure: {value: 0.02-0.2, unit: MPa}

 - boundary_id: HVAC-CHP_BND_IN_WATER
 boundary_name: 补水
 medium: WATER-DW
 source_system: PLUMB-DWS

 - boundary_id: HVAC-CHP_BND_IN_CTRL
 boundary_name: 控制信号
 medium: DATA-BA
 source_system: INT-BA

 outputs:
 - boundary_id: HVAC-CHP_BND_OUT_CHW
 boundary_name: 冷冻水供应
 medium: CHW
 target_system: HVAC-CHW
 parameters:
 temperature: {value: 7, unit: ℃}

 - boundary_id: HVAC-CHP_BND_OUT_HW
 boundary_name: 热水供应
 medium: HW
 target_system: HVAC-HW
 parameters:
 temperature: {value: 60, unit: ℃}

# ============================================================
# 节点定义
# ============================================================
nodes:

 # ----------------------------------------------------------
 # 源节点 (Source Nodes)
 # ----------------------------------------------------------
 source_nodes:

 - node_id: HVAC-CHP_SRC_CHILLER
 node_name: 冷水机组
 node_name_en: Chiller
 node_type: Source_Node
 node_category: SRC

 function: 制取冷冻水
 medium_in: [ELEC-LV, CW]
 medium_out: CHW

 multiplicity: multiple
 instance_pattern: HVAC-CHP_SRC_CHILLER_{NN}

 typical_configuration:
 quantity: 3-4
 redundancy: "N+1"
 total_capacity: {value: 5000-8000, unit: kW}
 capacity_each: {value: 1500-2500, unit: kW}

 equipment_parameters:
 type: 离心式/螺杆式
 refrigerant: R134a
 cop: {value: 5.5-6.5, unit: null}
 evaporator:
 chw_flow: {value: 250-400, unit: m³/h}
 chw_inlet: {value: 12, unit: ℃}
 chw_outlet: {value: 7, unit: ℃}
 condenser:
 cw_flow: {value: 300-500, unit: m³/h}
 cw_inlet: {value: 32, unit: ℃}
 cw_outlet: {value: 37, unit: ℃}
 power: {value: 300-500, unit: kW}

 location_hint:
 space_type: MEP_ROOM
 room_name: 冷冻机房
 floor: 地下一层
 area: {value: 600-1000, unit: m²}

 installation_requirements:
 - 设备基础及减振
 - 检修通道 ≥1.5m
 - 吊装孔预留
 - 排水沟
 - 通风换气
 - 隔声降噪

 control_points:
 sensors:
 - {point_id: CHILLER_CHWST, type: AI, description: 冷冻水供水温度}
 - {point_id: CHILLER_CHWRT, type: AI, description: 冷冻水回水温度}
 - {point_id: CHILLER_CWST, type: AI, description: 冷却水供水温度}
 - {point_id: CHILLER_CWRT, type: AI, description: 冷却水回水温度}
 - {point_id: CHILLER_LOAD, type: AI, description: 负荷率, unit: "%"}
 - {point_id: CHILLER_POWER, type: AI, description: 运行功率, unit: kW}
 - {point_id: CHILLER_CURRENT, type: AI, description: 运行电流, unit: A}
 status:
 - {point_id: CHILLER_RUN, type: DI, description: 运行状态}
 - {point_id: CHILLER_FAULT, type: DI, description: 故障报警}
 - {point_id: CHILLER_ALARM, type: DI, description: 一般报警}
 - {point_id: CHILLER_REMOTE, type: DI, description: 远程/就地}
 commands:
 - {point_id: CHILLER_START, type: DO, description: 启动命令}
 - {point_id: CHILLER_STOP, type: DO, description: 停止命令}
 setpoints:
 - {point_id: CHILLER_CHWST_SP, type: AO, description: 冷冻水温度设定}
 - {point_id: CHILLER_LOAD_LIMIT, type: AO, description: 负荷限制}

 - node_id: HVAC-CHP_SRC_BOILER
 node_name: 燃气热水锅炉
 node_name_en: Gas Fired Hot Water Boiler
 node_type: Source_Node
 node_category: SRC

 function: 制取空调热水
 medium_in: [GAS-NG, WATER-DW]
 medium_out: HW

 multiplicity: multiple
 instance_pattern: HVAC-CHP_SRC_BOILER_{NN}

---