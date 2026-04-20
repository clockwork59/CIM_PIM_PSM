## 🧑‍💻 User


你卡在了【 pure_steam:
 description: "纯蒸汽"
 purity: "符合药典标准"
 conductivity: "≤5 μS/cm"
 applications:
 - "灭菌器"
 - "药品生产"
 generation: "纯蒸汽发】，继续

---
## 🤖 Assistant


继续从蒸汽系统补充处接续输出：

---

```yaml
      pure_steam:
        description: "纯蒸汽"
        purity: "符合药典标准"
        conductivity: "≤5 μS/cm"
        applications:
          - "灭菌器"
          - "药品生产"
        generation: "纯蒸汽发生器"
        source_water: "纯化水/注射用水"

  # ═══════════════════════════════════════════════════════════════════════════
  # 蒸汽源配置
  # ═══════════════════════════════════════════════════════════════════════════
  
  steam_source_configuration:
    
    # ─────────────────────────────────────────────────────────────────────────
    # 方案一：燃气锅炉
    # ─────────────────────────────────────────────────────────────────────────
    
    option_1_gas_boiler:
      
      type: "燃气蒸汽锅炉"
      fuel: "天然气"
      
      configuration:
        capacity: "2-6 t/h"
        pressure: "0.7-1.0 MPa"
        quantity: "2-3台 (N+1)"
        location: "锅炉房 (独立建筑或地下室)"
        
      advantages:
        - "供汽量大"
        - "运行成本相对低"
        - "适合大型医院"
        
      requirements:
        gas_supply: "天然气接入"
        chimney: "烟囱排放"
        water_treatment: "软化水处理"
        boiler_room: "独立锅炉房"
        permits: "特种设备许可"
        
    # ─────────────────────────────────────────────────────────────────────────
    # 方案二：电蒸汽发生器
    # ─────────────────────────────────────────────────────────────────────────
    
    option_2_electric_generator:
      
      type: "电蒸汽发生器"
      energy: "电力"
      
      configuration:
        capacity: "100-500 kg/h"
        pressure: "0.4-0.7 MPa"
        quantity: "按需分布"
        location: "用汽点附近设备间"
        
      advantages:
        - "无需锅炉房"
        - "安装灵活"
        - "自动化程度高"
        - "清洁无排放"
        
      disadvantages:
        - "运行成本较高"
        - "容量有限"
        
      applications:
        - "中小型医院"
        - "无燃气条件"
        - "分散供汽"
        
      power_requirement:
        per_100kg: "75-80 kW"
        example: "500 kg/h ≈ 380 kW"

  # ═══════════════════════════════════════════════════════════════════════════
  # 纯蒸汽系统
  # ═══════════════════════════════════════════════════════════════════════════
  
  pure_steam_system:
    
    system_id: "STEAM-PURE"
    
    description: |
      用于直接接触灭菌物品的蒸汽，
      需满足药典规定的纯度要求。
      
    generation:
      
      equipment: "纯蒸汽发生器"
      
      principle: |
        将工业蒸汽或电加热纯化水，
        产生符合药典标准的纯蒸汽。
        
      types:
        - type: "蒸汽加热型"
          heat_source: "工业蒸汽"
          efficiency: "高"
          
        - type: "电加热型"
          heat_source: "电能"
          flexibility: "高"
          
      capacity_sizing:
        basis: "灭菌器峰值用量"
        typical: "200-500 kg/h"
        redundancy: "1+1"
        
    distribution:
      
      piping:
        material: "不锈钢316L"
        welding: "自动焊接"
        slope: "≥1%坡向疏水点"
        insulation: "不锈钢外护"
        
      pressure:
        generation: "0.4-0.5 MPa"
        terminal: "0.3-0.4 MPa"
        
    quality_monitoring:
      
      parameters:
        - "电导率 ≤5 μS/cm"
        - "不凝性气体 ≤3.5%"
        - "过热度 ≤25°C"
        - "干燥度 ≥0.95"
        
      sampling: "在线监测或定期取样"

  # ═══════════════════════════════════════════════════════════════════════════
  # 蒸汽分配系统
  # ═══════════════════════════════════════════════════════════════════════════
  
  steam_distribution:
    
    main_header:
      location: "锅炉房出口"
      pressure: "0.7-1.0 MPa"
      material: "碳钢无缝管"
      
    branch_systems:
      
      - branch: "供应室支路"
        pressure: "0.3-0.4 MPa"
        reduction: "减压阀组"
        steam_type: "纯蒸汽"
        consumers:
          - "脉动真空灭菌器"
          - "器械清洗机"
          
      - branch: "洗衣房支路"
        pressure: "0.5-0.7 MPa"
        steam_type: "工业蒸汽"
        consumers:
          - "洗衣机"
          - "烘干机"
          - "熨烫机"
          
      - branch: "厨房支路"
        pressure: "0.3-0.5 MPa"
        steam_type: "工业蒸汽"
        consumers:
          - "蒸饭车"
          - "蒸柜"
          - "洗碗机"
          
    condensate_system:
      
      collection: "凝结水回收"
      method: "闭式回收"
      return_to: "锅炉给水箱"
      recovery_rate: "≥80%"
      
      components:
        - "疏水阀 (每设备)"
        - "凝结水回收罐"
        - "凝结水泵"

  # ═══════════════════════════════════════════════════════════════════════════
  # 空间-蒸汽服务映射
  # ═══════════════════════════════════════════════════════════════════════════
  
  space_steam_mapping:
    
    - space: "供应室-灭菌区"
      steam_type: "纯蒸汽"
      pressure: "0.3-0.4 MPa"
      consumption: "100-150 kg/h/台"
      equipment_count: "2-4台灭菌器"
      
    - space: "洗衣房"
      steam_type: "工业蒸汽"
      pressure: "0.5-0.7 MPa"
      consumption: "200-500 kg/h"
      
    - space: "中心厨房"
      steam_type: "工业蒸汽"
      pressure: "0.3-0.5 MPa"
      consumption: "100-300 kg/h"
      
    - space: "空调机房 (加湿)"
      steam_type: "工业蒸汽"
      pressure: "0.2-0.3 MPa"
      consumption: "依负荷"
      note: "干蒸汽加湿器"
```

---

## 系统补充5：医用IT系统（隔离电源）

```yaml
Medical_IT_System:
  
  system_id: "ELEC-IT"
  system_name: "医用IT系统（隔离电源）"
  description: "为手术室等关键医疗区域提供安全隔离电源"
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 系统概述
  # ═══════════════════════════════════════════════════════════════════════════
  
  system_overview:
    
    purpose: |
      采用不接地供电系统(IT系统)，即使发生单相接地故障，
      系统仍可继续运行，同时配合绝缘监测报警，
      确保手术等关键医疗过程不中断。
      
    standards:
      - "IEC 60364-7-710"
      - "GB 16895.24"
      - "JGJ 312 (医疗建筑电气设计规范)"
      
    applicable_spaces:
      - space: "手术室"
        requirement: "必须"
      - space: "ICU"
        requirement: "必须"
      - space: "CCU"
        requirement: "必须"
      - space: "导管室"
        requirement: "必须"
      - space: "血液透析室"
        requirement: "推荐"
      - space: "分娩室"
        requirement: "推荐"
      - space: "早产儿室"
        requirement: "推荐"

  # ═══════════════════════════════════════════════════════════════════════════
  # 系统组成
  # ═══════════════════════════════════════════════════════════════════════════
  
  system_components:
    
    # ─────────────────────────────────────────────────────────────────────────
    # 医用隔离变压器
    # ─────────────────────────────────────────────────────────────────────────
    
    isolation_transformer:
      
      type: "医用隔离变压器"
      
      specifications:
        input: "380V/220V (TN-S系统)"
        output: "230V (IT系统)"
        capacity_range: "3.15-10 kVA"
        typical_capacities:
          - "3.15 kVA (小型手术室)"
          - "5 kVA (中型手术室)"
          - "8 kVA (大型手术室)"
          - "10 kVA (杂交手术室)"
          
      technical_requirements:
        insulation: "双重绝缘"
        coupling_capacitance: "≤500 pF"
        temperature_rise: "≤75K"
        leakage_current: "≤0.5 mA"
        
      configuration:
        primary: "接地 (TN-S)"
        secondary: "不接地 (IT)"
        shield: "静电屏蔽层"
        
      installation:
        location: "手术室配电间或邻近设备间"
        environment: "干燥、通风"
        access: "便于维护"
        
    # ─────────────────────────────────────────────────────────────────────────
    # 绝缘监测装置
    # ─────────────────────────────────────────────────────────────────────────
    
    insulation_monitor:
      
      type: "绝缘监测仪 (IMD)"
      
      function: |
        实时监测IT系统对地绝缘电阻，
        当绝缘电阻降至设定值以下时发出报警。
        
      specifications:
        monitoring_voltage: "AC 230V"
        alarm_threshold: "50 kΩ (可调)"
        response_time: "≤5s"
        measuring_current: "≤1 mA DC"
        
      alarm_outputs:
        visual: "黄色指示灯"
        audible: "蜂鸣器"
        remote: "干接点输出至BA系统"
        
    # ─────────────────────────────────────────────────────────────────────────
    # 外接报警显示
    # ─────────────────────────────────────────────────────────────────────────
    
    remote_alarm_display:
      
      type: "外接报警和显示装置"
      
      installation_location: "手术室内醒目位置"
      
      displays:
        - "IT系统电压"
        - "绝缘电阻值"
        - "变压器负载率"
        - "变压器温度"
        
      alarms:
        - event: "绝缘电阻低"
          indicator: "黄灯+蜂鸣"
        - event: "过负载"
          indicator: "红灯+蜂鸣"
        - event: "超温"
          indicator: "红灯+蜂鸣"
          
    # ─────────────────────────────────────────────────────────────────────────
    # 等电位联结
    # ─────────────────────────────────────────────────────────────────────────
    
    equipotential_bonding:
      
      description: "局部等电位联结"
      
      requirements:
        - "手术台、设备外壳、金属管道等均需联结"
        - "联结导体截面 ≥6 mm² Cu"
        - "等电位端子排设置在手术室内"
        - "联结电阻 ≤0.2 Ω"
        
      bonding_points:
        - "手术台"
        - "手术灯"
        - "吊塔/设备柱"
        - "医用气体终端"
        - "金属门框"
        - "金属管道"

  # ═══════════════════════════════════════════════════════════════════════════
  # 配电设计
  # ═══════════════════════════════════════════════════════════════════════════
  
  distribution_design:
    
    it_system_loads:
      description: "仅关键医疗设备接入IT系统"
      typical_loads:
        - "手术灯"
        - "监护仪"
        - "电刀"
        - "麻醉机"
        - "显微镜"
        - "其他直接用于病人的设备"
        
    non_it_loads:
      description: "非关键设备使用普通TN-S供电"
      typical_loads:
        - "一般照明"
        - "空调设备"
        - "观片灯"
        - "对讲设备"
        
    outlet_identification:
      it_outlets:
        color: "绿色面板"
        label: "IT系统"
        quantity: "依手术室大小，10-20个"
      normal_outlets:
        color: "白色面板"
        label: "普通电源"

  # ═══════════════════════════════════════════════════════════════════════════
  # 空间配置标准
  # ═══════════════════════════════════════════════════════════════════════════
  
  space_configuration_standards:
    
    - space_type: "普通手术室"
      transformer_capacity: "5 kVA"
      it_outlets: 12
      insulation_monitor: 1
      remote_display: 1
      
    - space_type: "大型手术室"
      transformer_capacity: "8 kVA"
      it_outlets: 16
      insulation_monitor: 1
      remote_display: 1
      
    - space_type: "杂交手术室"
      transformer_capacity: "10 kVA"
      it_outlets: 20
      insulation_monitor: 1
      remote_display: 1
      note: "另需普通电源供大型影像设备"
      
    - space_type: "ICU单元"
      configuration: "每2-3床共用一套"
      transformer_capacity: "5 kVA"
      it_outlets: "每床4-6个"
      
    - space_type: "分娩室"
      transformer_capacity: "3.15 kVA"
      it_outlets: 8
```

---

## 系统补充6：医用气体多源供应系统

```yaml
Medical_Gas_Multi_Source_System:
  
  system_id: "MGAS-MULTI"
  system_name: "医用气体多源供应系统"
  description: "关键医用气体的主备源切换与安全保障"
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 系统设计原则
  # ═══════════════════════════════════════════════════════════════════════════
  
  design_principles:
    
    - principle: "双源供应"
      description: "关键气体必须有主备两套气源"
      
    - principle: "自动切换"
      description: "主源故障时自动切换至备源"
      
    - principle: "不间断供应"
      description: "切换过程不影响终端供气"
      
    - principle: "分级保障"
      description: "不同区域不同保障级别"

  # ═══════════════════════════════════════════════════════════════════════════
  # 医用氧气多源系统
  # ═══════════════════════════════════════════════════════════════════════════
  
  oxygen_multi_source:
    
    system_id: "MGAS-O2-MULTI"
    
    # ─────────────────────────────────────────────────────────────────────────
    # 三源供应方案
    # ─────────────────────────────────────────────────────────────────────────
    
    three_source_configuration:
      
      primary_source:
        type: "液氧储罐系统"
        description: "主供气源"
        components:
          - "液氧储罐 (5-20 m³)"
          - "空温式汽化器"
          - "调压阀组"
        capacity: "满足7-15天用量"
        location: "室外液氧站"
        auto_refill: "液位低自动通知供应商"
        
      secondary_source:
        type: "氧气汇流排"
        description: "备用气源/调峰"
        components:
          - "高压钢瓶组 (10+10或20+20)"
          - "自动切换汇流排"
          - "减压调节阀组"
        capacity: "满足24-48小时用量"
        location: "氧气汇流排间"
        auto_switch: "液氧压力低时自动投入"
        
      emergency_source:
        type: "应急钢瓶组"
        description: "最后保障"
        components:
          - "独立钢瓶 (2-4瓶)"
          - "手动切换装置"
        location: "手术部/ICU就近"
        activation: "手动投入"
        purpose: "极端紧急情况"
        
    # ─────────────────────────────────────────────────────────────────────────
    # 自动切换逻辑
    # ─────────────────────────────────────────────────────────────────────────
    
    automatic_switching:
      
      normal_operation:
        active: "液氧系统"
        standby: "汇流排系统"
        
      switching_triggers:
        - trigger: "液氧压力 < 0.6 MPa"
          action: "切换至汇流排"
          alarm: "主源低压报警"
          
        - trigger: "液氧液位 < 20%"
          action: "预警通知补液"
          
        - trigger: "汇流排一组用完"
          action: "自动切换至另一组"
          alarm: "钢瓶更换提醒"
          
      switching_requirements:
        time: "≤3s"
        pressure_fluctuation: "≤10%"
        interruption: "无"
        
    # ─────────────────────────────────────────────────────────────────────────
    # 分区供应
    # ─────────────────────────────────────────────────────────────────────────
    
    zone_supply:
      
      - zone: "手术部"
        priority: "最高"
        zone_valve: "ZONE-O2-OR"
        emergency_backup: "有"
        
      - zone: "ICU"
        priority: "最高"
        zone_valve: "ZONE-O2-ICU"
        emergency_backup: "有"
        
      - zone: "急诊"
        priority: "高"
        zone_valve: "ZONE-O2-ER"
        
      - zone: "病房楼"
        priority: "中"
        zone_valve: "ZONE-O2-WARD"

  # ═══════════════════════════════════════════════════════════════════════════
  # 负压吸引多源系统
  # ═══════════════════════════════════════════════════════════════════════════
  
  vacuum_multi_source:
    
    system_id: "MGAS-VAC-MULTI"
    
    configuration:
      
      primary_system:
        type: "液环真空泵组"
        quantity: "3台 (2用1备)"
        capacity: "满足100%峰值负荷"
        
      backup_options:
        
        option_1:
          type: "移动式真空泵"
          quantity: 1
          location: "设备库房"
          activation: "应急启用"
          
        option_2:
          type: "手术室独立真空源"
          description: "手术室备用小型真空泵"
          location: "手术室设备间"
          serves: "本手术室"
          
    redundancy:
      pump_configuration: "N+1"
      auto_standby: true
      rotation: "自动轮换运行"
      
    monitoring:
      parameters:
        - "真空度"
        - "泵运行状态"
        - "储罐液位"
      alarm: "真空度不足报警"

  # ═══════════════════════════════════════════════════════════════════════════
  # 医用空气多源系统
  # ═══════════════════════════════════════════════════════════════════════════
  
  air_multi_source:
    
    system_id: "MGAS-AIR-MULTI"
    
    configuration:
      
      primary_system:
        type: "医用空压机组"
        quantity: "3台 (2用1备)"
        type_spec: "无油空压机"
        drying: "冷冻式干燥机 + 吸附式干燥机"
        
      backup_system:
        type: "高压钢瓶组"
        configuration: "10+10瓶汇流排"
        activation: "空压机故障时自动切换"
        duration: "4-8小时"
        
    air_quality:
      standard: "YY/T 0799"
      specifications:
        压力露点: "≤-40°C"
        含油量: "≤0.1 mg/m³"
        颗粒物: "≤0.5 μm, ≤20个/m³"
        CO: "≤5 ppm"
        CO2: "≤500 ppm"

  # ═══════════════════════════════════════════════════════════════════════════
  # 监控与报警系统
  # ═══════════════════════════════════════════════════════════════════════════
  
  monitoring_alarm_system:
    
    central_monitoring:
      location: "中心控制室/值班室"
      display: "医用气体监控屏"
      
    monitoring_points:
      
      - parameter: "供气压力"
        locations: "各气源出口、各楼层"
        alarm: "高压/低压报警"
        
      - parameter: "液氧液位"
        location: "液氧储罐"
        alarm: "低液位报警"
        
      - parameter: "汇流排状态"
        location: "各汇流排间"
        alarm: "切换报警"
        
      - parameter: "设备运行状态"
        locations: "真空泵、空压机"
        alarm: "故障报警"
        
    alarm_hierarchy:
      
      - level: "一级报警 (紧急)"
        events:
          - "供气压力异常"
          - "所有气源故障"
        response: "立即处理"
        notification: "电话+短信+声光"
        
      - level: "二级报警 (警告)"
        events:
          - "单一气源切换"
          - "液位低"
        response: "计划处理"
        notification: "短信+系统显示"
```

---

## 系统补充7：热水分级系统

```yaml
Hot_Water_Tiered_System:
  
  system_id: "PLUMB-HW-TIER"
  system_name: "热水分级供应系统"
  description: "医院不同用途热水的分级供应"
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 热水分级体系
  # ═══════════════════════════════════════════════════════════════════════════
  
  hot_water_classification:
    
    # ─────────────────────────────────────────────────────────────────────────
    # 一级热水：卫生热水
    # ─────────────────────────────────────────────────────────────────────────
    
    tier_1_sanitary:
      
      name: "卫生生活热水"
      temperature: "55-60°C (出水)"
      usage_temperature: "38-42°C (混合后)"
      
      applications:
        - space: "病房卫生间"
          usage: "洗浴、洗手"
        - space: "公共卫生间"
          usage: "洗手"
        - space: "医护更衣室"
          usage: "淋浴"
          
      supply_mode:
        type: "集中热水系统"
        circulation: "机械循环"
        return_temperature: "≥50°C"
        
      heat_source_options:
        - "锅炉热水"
        - "空气源热泵"
        - "太阳能+辅助热源"
        - "市政热力换热"
        
    # ─────────────────────────────────────────────────────────────────────────
    # 二级热水：医疗热水
    # ─────────────────────────────────────────────────────────────────────────
    
    tier_2_medical:
      
      name: "医疗用热水"
      temperature: "依用途不同"
      
      subtypes:
        
        - subtype: "外科洗手热水"
          temperature: "35-38°C"
          locations:
            - "手术室刷手间"
            - "ICU"
            - "产房"
          supply_mode: "局部恒温供水"
          control: "恒温混水阀"
          sensor: "感应式"
          
        - subtype: "婴儿沐浴热水"
          temperature: "37-38°C (精确)"
          locations:
            - "新生儿室"
            - "产房"
            - "NICU"
          supply_mode: "局部电热水器+恒温控制"
          precision: "±1°C"
          
        - subtype: "配奶用热水"
          temperature: "40-45°C"
          locations:
            - "NICU配奶间"
            - "新生儿配奶室"
          supply_mode: "专用开水器/恒温水浴"
          quality: "纯净水加热"
          
    # ─────────────────────────────────────────────────────────────────────────
    # 三级热水：工艺热水
    # ─────────────────────────────────────────────────────────────────────────
    
    tier_3_process:
      
      name: "工艺用热水"
      
      subtypes:
        
        - subtype: "洗衣房热水"
          temperature: "60-80°C"
          location: "洗衣房"
          consumption: "大量"
          heat_source: "蒸汽换热或锅炉直供"
          
        - subtype: "厨房热水"
          temperature: "55-60°C"
          location: "中心厨房"
          consumption: "大量"
          peak_demand: "就餐前后"
          
        - subtype: "供应室热水"
          temperature: "60-80°C"
          location: "消毒供应中心"
          purpose: "器械预洗"

  # ═══════════════════════════════════════════════════════════════════════════
  # 热水系统配置
  # ═══════════════════════════════════════════════════════════════════════════
  
  system_configurations:
    
    # ─────────────────────────────────────────────────────────────────────────
    # 集中热水系统
    # ─────────────────────────────────────────────────────────────────────────
    
    centralized_system:
      
      applicable_to: ["病房楼", "门诊楼"]
      
      components:
        
        heat_source:
          option_1:
            type: "空气源热泵"
            advantages: "节能、环保"
            cop: "3.0-4.0"
            capacity: "按峰值设计"
            redundancy: "N+1"
            
          option_2:
            type: "锅炉热水"
            advantages: "稳定可靠"
            fuel: "天然气/蒸汽"
            
          option_3:
            type: "太阳能+辅助热源"
            solar_fraction: "30-50%"
            auxiliary: "空气源热泵或电加热"
            
        storage:
          type: "承压保温水箱"
          material: "不锈钢304"
          capacity: "1-2小时峰值用量"
          insulation: "聚氨酯发泡"
          
        circulation:
          type: "机械循环"
          pump: "变频循环泵"
          control: "温控+定时"
          pipe_insulation: "全程保温"
          
    # ─────────────────────────────────────────────────────────────────────────
    # 局部热水系统
    # ─────────────────────────────────────────────────────────────────────────
    
    localized_system:
      
      applicable_to:
        - "外科刷手间"
        - "婴儿室"
        - "分散卫生间"
        
      equipment_types:
        
        - type: "即热式电热水器"
          power: "5-10 kW"
          advantages: "即开即热、不占空间"
          applications: "洗手、少量用水"
          
        - type: "储水式电热水器"
          capacity: "30-100 L"
          power: "2-3 kW"
          advantages: "水温稳定"
          applications: "淋浴、较大用水量"
          
        - type: "恒温混水阀"
          type_spec: "热力学恒温阀"
          output_temp: "可设定"
          precision: "±2°C"
          applications: "洗手池、淋浴"

  # ═══════════════════════════════════════════════════════════════════════════
  # 空间热水配置表
  # ═══════════════════════════════════════════════════════════════════════════
  
  space_hot_water_mapping:
    
    - space: "普通病房卫生间"
      supply_type: "集中热水"
      temperature: "55°C供/38°C用"
      outlets: "淋浴+洗手池"
      
    - space: "手术室刷手间"
      supply_type: "集中+恒温阀"
      temperature: "36°C (恒温)"
      outlets: "感应式洗手池"
      control: "膝/肘控"
      
    - space: "ICU"
      supply_type: "集中+恒温阀"
      temperature: "38°C"
      outlets: "洗手池"
      
    - space: "NICU"
      supply_type: "局部+精密恒温"
      temperature: "37°C ±1°C"
      outlets: "婴儿浴盆、洗手池"
      
    - space: "洗衣房"
      supply_type: "集中/蒸汽换热"
      temperature: "80°C"
      consumption: "500-1000 L/h"
      
    - space: "厨房"
      supply_type: "集中/锅炉"
      temperature: "60°C"
      consumption: "300-500 L/h (峰值)"

  # ═══════════════════════════════════════════════════════════════════════════
  # 防军团菌措施
  # ═══════════════════════════════════════════════════════════════════════════
  
  legionella_prevention:
    
    measures:
      - measure: "储水温度"
        requirement: "≥60°C"
        purpose: "抑制细菌生长"
        
      - measure: "回水温度"
        requirement: "≥50°C"
        purpose: "全系统保温"
        
      - measure: "热冲洗"
        method: "定期70°C热水冲洗"
        frequency: "每周或每月"
        duration: "末端出水5分钟"
        
      - measure: "避免死水"
        method: "循环系统设计"
        requirement: "消除死角、定期排放"
        
      - measure: "水质检测"
        frequency: "每年"
        standard: "军团菌检测"
```

---

## 系统补充8：照明分级系统

```yaml
Lighting_Tiered_System:

system_id: "ELEC-LIGHT-TIER"
system_name: "照明分级系统"
description: "医院不同区域照明的分级配置与控制"

# ═══════════════════════════════════════════════════════════════════════════
# 照明分级体系
# ═══════════════════════════════════════════════════════════════════════════

lighting_classification:

 # ─────────────────────────────────────────────────────────────────────────
 # 一级：手术/治疗照明
 # ─────────────────────────────────────────────────────────────────────────

 tier_1_surgical:

 name: "手术/治疗照明"
 criticality: "最高"

 applications:

 - space: "手术室术区"
 equipment: "手术无影灯"
 illuminance: "40,000-160,000 lx"
 specifications:
 color_temperature: "4000-4500 K"
 cri: "≥95"
 shadow_control: "无影设计"
 adjustable: "亮度/光斑可调"
 power_supply: "UPS"

 - space: "手术室一般区"
 type: "LED洁净面板灯"
 illuminance: "500-750 lx"
 specifications:
 color_temperature: "4000 K"
 cri: "≥90"
 cleanroom: "洁净室专用"
 control: "可调光"

 - space: "检查治疗"
 equipment: "检查灯"
 illuminance: "1,000-10,000 lx (局部)"
 types:
 - "落地检查灯"
 - "壁挂检查灯"
 - "头灯"

 # ─────────────────────────────────────────────────────────────────────────
 # 二级：医疗功能照明
 # ─────────────────────────────────────────────────────────────────────────

 tier_2_medical:

 name: "医疗功能照明"
 criticality: "高"

 applications:

 - space: "ICU"
 general: "200-300 lx"
 examination: "1,000 lx (可调)"
 night: "10-50 lx"
 specifications:
 color_temperature: "4000 K (日间)/3000 K (夜间)"
 control: "分组调光"
 circadian: "支持昼夜节律"

 - space: "病房"
 general: "100-200 lx"
 bed_light: "300 lx"
 night: "1-5 lx"
 specifications:
 color_temperature: "3000-4000 K"
 control: "床头独立控制"

 - space: "护士站"
 illuminance: "300-500 lx"
 task_light: "500-750 lx"
 specifications:
 glare_control: "UGR<19"

 - space: "诊室"
 general: "300 lx"
 examination: "1,000 lx (局部)"

 # ─────────────────────────────────────────────────────────────────────────
 # 三级：一般功能照明
 # ─────────────────────────────────────────────────────────────────────────

 tier_3_general:

 name: "一般功能照明"
 criticality: "中"

 applications:

 - space: "走廊"
 illuminance: "100-150 lx"
 night: "50 lx"
 control: "定时+感应"

 - space: "候诊区"
 illuminance: "200-300 lx"
 natural_light: "利用自然采光"

 - space: "办公室"
 illuminance: "300-500 lx"
 specifications:
 glare_control: "UGR<19"
 task_light: "可选"

 - space: "卫生间"
 illuminance: "100-150 lx"
 control: "感应控制"

 # ─────────────────────────────────────────────────────────────────────────
 # 四级：应急照明
 # ─────────────────────────────────────────────────────────────────────────

 tier_4_emergency:

 name: "应急照明"
 criticality: "安全关键"

 types:

 - type: "备用照明"
 purpose: "维持正常活动"
 illuminance: "正常照明10-100%"
 spaces:
 - "手术室: 50%以上"
 - "ICU: 50%以上"
 - "走廊: 10%以上"
 power_source: "柴油发电机"
 switch_time: "≤15s"

 - type: "疏散照明"
 purpose: "安全疏散"
 illuminance: "≥1 lx (地面)"
 components:
 - "疏散指示灯"
 - "出口标志"
 - "楼梯照明"
 power_source: "自带电池"
 duration: "≥90分钟"

 - type:

---