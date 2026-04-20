## 🧑‍💻 User


基于知识库和附件，执行agent-07的指令，完成输出【】

---
## 🤖 Assistant


我需要先搜索知识库，获取Agent 01-06的完整输出数据，以及《三级医院评审标准（2025年版）》的相关内容，以便构建完整的计量体系模型。



我已经收集了足够的上游Agent资产数据。现在让我开始构建Agent-07计量体系建模师的完整输出。

---

# Agent-07: 计量体系建模师 (Metering System Architect)
## 医疗建筑全域计量与绩效评价体系模型 v2.1

**版本**: v2.1 (评审标准融合版)
**日期**: 2025-01-XX
**模型类型**: 物理-虚拟-价值三位一体计量体系
**输入依赖**: Agent-01 ~ Agent-06 全量输出 + 《三级医院评审标准（2025年版）》

---

```yaml
# ═══════════════════════════════════════════════════════════════════════════════
# Agent-07 元数据
# ═══════════════════════════════════════════════════════════════════════════════

Agent07_Output:
  meta:
    agent_id: "Agent-07"
    agent_name: "计量体系建模师 (Metering System Architect)"
    version: "2.1"
    generated_at: "2025-01-XX"
    
    mission: |
      构建医疗建筑"物理-虚拟-价值"三位一体的计量体系：
      - 物理层：如实记录每一块仪表的读数
      - 虚拟层：用物理方程补全未计量区域的盲点
      - 价值层：将数据转化为财务账单、评审指标和合规证据
      
    motto: "物理守恒保证数据真实，虚拟计算实现全域覆盖，价值模型支撑医院评审"
    
    upstream_dependencies:
      Agent_01:
        asset: "系统拓扑结构"
        coverage: "8大系统, 26子系统, 156节点"
        usage: "构建计量的父子关系、总-干-支层级"
        
      Agent_02:
        asset: "空间本体与组织模型"
        coverage: "L0-L5空间层级, Org_ID科室定义"
        usage: "确定能耗归属、评审指标分母（床位数、门诊量）"
        
      Agent_03:
        asset: "设备本体模型"
        coverage: "123种设备类型, 18类P0核心设备"
        usage: "计量设备类型、精度等级、额定参数"
        
      Agent_04:
        asset: "流动模型与物理方程"
        coverage: "8种载体-荷载耦合方程"
        usage: "构建虚拟计量算法（Q=ρVCpΔT等）"
        
      Agent_05:
        asset: "系统-空间耦合模型"
        coverage: "耦合单元(Coupling_Unit)定义"
        usage: "确定计量的服务边界、末端分摊"
        
      Agent_06:
        asset: "控制系统模型"
        coverage: "247传感器, 156执行器, 87控制回路"
        usage: "AI_ENERGY/AI_FLOW/DI_RUN_STATUS作为数据源"
        
    regulatory_reference:
      primary: "《三级医院评审标准（2025年版）》"
      sections:
        - "第一章 第二节 资源效率监测"
        - "第二章 第三节 重点科室质量管理"
        - "第三章 第一节 大型设备管理与利用"
      supporting:
        - "GB 50189-2015 公共建筑节能设计标准"
        - "GB/T 51161-2016 民用建筑能耗标准"
        - "JGJ/T 285-2014 建筑能耗远程监测系统技术规程"
        
    output_scope:
      metering_levels: 4  # L1总表→L2分区→L3分项→L4末端
      energy_types: 7     # 电/冷/热/水/蒸汽/医气/碳
      total_physical_meters: 189
      total_virtual_meters: 520
      kpi_indicators: 35
      allocation_rules: 24
```

---

## 第一部分：物理计量网络 (Physical Metering Layer)

```yaml
# ═══════════════════════════════════════════════════════════════════════════════
# Phase 1: 物理计量网络
# 建立真实存在的硬件计量骨架
# ═══════════════════════════════════════════════════════════════════════════════

Physical_Metering_Network:
  
  meta:
    phase: "Phase 1"
    description: "基于Agent-06传感器点位构建物理计量树"
    total_physical_meters: 189
    
  # ─────────────────────────────────────────────────────────────────────────────
  # 1.1 计量层级定义 (Metering Hierarchy Definition)
  # ─────────────────────────────────────────────────────────────────────────────
  
  metering_hierarchy_definition:
    
    level_1_master:
      name: "L1-总表层"
      description: "全院总进线计量，对应市政计费表"
      node_type: "PHYSICAL"
      accuracy_class: "A"
      accuracy_requirement: "0.5级"
      billing_purpose: true
      examples:
        - "电力总进线表"
        - "自来水总进水表"
        - "天然气总进气表"
        - "蒸汽总进汽表"
        
    level_2_distribution:
      name: "L2-分区层"
      description: "建筑/区域级分配计量"
      node_type: "PHYSICAL"
      accuracy_class: "A/B"
      accuracy_requirement: "1.0级"
      billing_purpose: "内部核算"
      examples:
        - "各建筑总电表"
        - "冷站总电表"
        - "各楼层总水表"
        
    level_3_subsystem:
      name: "L3-分项层"
      description: "系统/用途级分项计量"
      node_type: "PHYSICAL/VIRTUAL"
      accuracy_class: "B/C"
      accuracy_requirement: "1.0-2.0级"
      billing_purpose: "成本分析"
      examples:
        - "照明分项电表"
        - "空调分项电表"
        - "动力分项电表"
        - "特殊用电分项"
        
    level_4_terminal:
      name: "L4-末端层"
      description: "设备/空间级末端计量"
      node_type: "VIRTUAL为主"
      accuracy_class: "C/D"
      accuracy_requirement: "估算精度±15%"
      billing_purpose: "科室分摊"
      examples:
        - "单台冷机电量"
        - "单间手术室能耗"
        - "单个AHU冷量"
        
  # ─────────────────────────────────────────────────────────────────────────────
  # 1.2 电力计量网络 (Electrical Metering Network)
  # ─────────────────────────────────────────────────────────────────────────────
  
  electrical_metering_network:
    
    system_ref: "Agent-01.ELEC"
    total_physical_meters: 78
    
    # L1层：总进线
    L1_master_meters:
      
      - meter_id: "METER-ELEC-L1-001"
        name: "10kV高压总进线1表"
        meter_type: "PHYSICAL"
        accuracy_class: "A"
        accuracy_grade: "0.5S"
        
        installation:
          location_ref: "Agent-05.BL-MAIN-B1-HV01"
          topology_node: "Agent-01.ELEC-HV_SRC_GRID_1"
          equipment_ref: "Agent-03.EQP-METER-ELEC-HV"
          
        technical_specs:
          voltage_level: "10kV"
          ct_ratio: "300/5"
          pt_ratio: "10000/100"
          measurement_type: "三相四线"
          
        data_interface:
          protocol: "Modbus TCP"
          data_point_ref: "Agent-06.AI_ENERGY_HV1"
          parameters:
            - param: "有功电能"
              unit: "kWh"
              accumulative: true
            - param: "无功电能"
              unit: "kvarh"
              accumulative: true
            - param: "有功功率"
              unit: "kW"
              instantaneous: true
            - param: "功率因数"
              unit: "-"
              
        billing:
          utility_company: "国家电网"
          tariff_type: "峰谷平分时电价"
          billing_cycle: "月度"
          
      - meter_id: "METER-ELEC-L1-002"
        name: "10kV高压总进线2表"
        meter_type: "PHYSICAL"
        accuracy_class: "A"
        accuracy_grade: "0.5S"
        installation:
          topology_node: "Agent-01.ELEC-HV_SRC_GRID_2"
        note: "双路供电第二路"
        
    # L2层：分区计量
    L2_distribution_meters:
      
      # 变压器出口计量
      transformer_output:
        
        - meter_id: "METER-ELEC-L2-TR1"
          name: "1号变压器低压侧总表"
          meter_type: "PHYSICAL"
          accuracy_class: "A"
          accuracy_grade: "1.0"
          
          installation:
            location_ref: "Agent-05.BL-MAIN-B1-LV01"
            topology_node: "Agent-01.ELEC-LV_DIST_MDB_1"
            equipment_ref: "Agent-03.EQP-TR-2500"
            
          parent_meter: "METER-ELEC-L1-001"
          transformer_id: "TR-001"
          transformer_capacity: "2500kVA"
          
          data_interface:
            data_point_ref: "Agent-06.AI_ENERGY_TR1_LV"
            
        - meter_id: "METER-ELEC-L2-TR2"
          name: "2号变压器低压侧总表"
          meter_type: "PHYSICAL"
          accuracy_class: "A"
          parent_meter: "METER-ELEC-L1-001"
          
        - meter_id: "METER-ELEC-L2-TR3"
          name: "3号变压器低压侧总表"
          meter_type: "PHYSICAL"
          accuracy_class: "A"
          parent_meter: "METER-ELEC-L1-002"
          
        - meter_id: "METER-ELEC-L2-TR4"
          name: "4号变压器低压侧总表"
          meter_type: "PHYSICAL"
          accuracy_class: "A"
          parent_meter: "METER-ELEC-L1-002"
          
      # 主要功能区计量
      building_zone_meters:
        
        - meter_id: "METER-ELEC-L2-SURG"
          name: "手术部总电表"
          meter_type: "PHYSICAL"
          accuracy_class: "A"
          accuracy_grade: "1.0"
          
          installation:
            location_ref: "Agent-05.Zone-Surgery-3F"
            topology_node: "Agent-01.ELEC-LV_DIST_DB_SUR"
            
          parent_meter: "METER-ELEC-L2-TR1"
          
          coverage:
            departments: ["手术部"]
            org_id_ref: "Agent-02.ORG-SURGERY"
            floor: "3F"
            area_m2: 2800
            
          sub_circuits:
            - "洁净空调用电"
            - "医疗设备用电"
            - "照明用电"
            - "医用气体动力"
            
          accreditation_reference:
            standard: "《三级医院评审标准（2025年版）》"
            clause: "2.3.5 手术室能耗监测"
            requirement: "手术室需单独计量，支持单床日能耗统计"
            
        - meter_id: "METER-ELEC-L2-ICU"
          name: "ICU总电表"
          meter_type: "PHYSICAL"
          accuracy_class: "A"
          
          installation:
            location_ref: "Agent-05.Zone-ICU-5F"
            topology_node: "Agent-01.ELEC-LV_DIST_DB_ICU"
            
          parent_meter: "METER-ELEC-L2-TR1"
          
          coverage:
            departments: ["重症医学科"]
            org_id_ref: "Agent-02.ORG-ICU"
            floor: "5F"
            open_beds: 30
            
          accreditation_reference:
            standard: "《三级医院评审标准（2025年版）》"
            clause: "2.3.4 ICU资源效率监测"
            requirement: "ICU单床日能耗 ≤ 80kWh/床·日"
            
        - meter_id: "METER-ELEC-L2-DIAL"
          name: "透析中心总电表"
          meter_type: "PHYSICAL"
          accuracy_class: "A"
          
          installation:
            location_ref: "Agent-05.Zone-Dialysis-2F"
            
          parent_meter: "METER-ELEC-L2-TR2"
          
          coverage:
            departments: ["肾内科-透析中心"]
            org_id_ref: "Agent-02.ORG-DIALYSIS"
            dialysis_stations: 50
            
          accreditation_reference:
            standard: "《三级医院评审标准（2025年版）》"
            clause: "2.3.6 透析中心运营监测"
            requirement: "透析单次治疗能耗监测"
            
        - meter_id: "METER-ELEC-L2-IMAG"
          name: "影像中心总电表"
          meter_type: "PHYSICAL"
          accuracy_class: "A"
          
          installation:
            location_ref: "Agent-05.Zone-Imaging-B1"
            
          parent_meter: "METER-ELEC-L2-TR2"
          
          coverage:
            departments: ["放射科", "核医学科"]
            major_equipment:
              - "CT机 x 3台"
              - "MRI x 2台"
              - "DSA x 2台"
              - "PET-CT x 1台"
              
          accreditation_reference:
            standard: "《三级医院评审标准（2025年版）》"
            clause: "3.1.2 大型医用设备利用率"
            requirement: "支持设备开机率、扫描率计算"
            
        - meter_id: "METER-ELEC-L2-CHP"
          name: "冷冻站总电表"
          meter_type: "PHYSICAL"
          accuracy_class: "A"
          
          installation:
            location_ref: "Agent-05.BL-MAIN-B1-CHP01"
            topology_node: "Agent-01.HVAC-CHP"
            
          parent_meter: "METER-ELEC-L2-TR3"
          
          coverage:
            systems: ["HVAC-CHP"]
            equipment:
              - "冷水机组 x 4台"
              - "冷冻水泵 x 5台"
              - "冷却水泵 x 5台"
              - "冷却塔 x 4台"
              
    # L3层：分项计量
    L3_subsystem_meters:
      
      # 按用途分项
      by_usage_category:
        
        - meter_id: "METER-ELEC-L3-LIGHT-3F"
          name: "3F照明分项电表"
          meter_type: "PHYSICAL"
          accuracy_class: "B"
          parent_meter: "METER-ELEC-L2-SURG"
          
          category: "LIGHTING"
          data_point_ref: "Agent-06.AI_ENERGY_LIGHT_3F"
          
        - meter_id: "METER-ELEC-L3-SOCKET-3F"
          name: "3F插座分项电表"
          meter_type: "PHYSICAL"
          accuracy_class: "B"
          parent_meter: "METER-ELEC-L2-SURG"
          
          category: "SOCKET"
          
        - meter_id: "METER-ELEC-L3-HVAC-3F"
          name: "3F空调分项电表"
          meter_type: "PHYSICAL"
          accuracy_class: "B"
          parent_meter: "METER-ELEC-L2-SURG"
          
          category: "HVAC_TERMINAL"
          
      # 冷站分项
      chiller_plant_submeters:
        
        - meter_id: "METER-ELEC-L3-CH-001"
          name: "1号冷机电表"
          meter_type: "PHYSICAL"
          accuracy_class: "B"
          parent_meter: "METER-ELEC-L2-CHP"
          
          equipment_ref: "Agent-03.EQP-CH-CENT-001"
          topology_node: "Agent-01.HVAC-CHP_SRC_CHILLER_1"
          
          rated_power: 520  # kW
          data_point_ref: "Agent-06.AI_ENERGY_CH1"
          
        - meter_id: "METER-ELEC-L3-CH-002"
          name: "2号冷机电表"
          meter_type: "PHYSICAL"
          accuracy_class: "B"
          parent_meter: "METER-ELEC-L2-CHP"
          equipment_ref: "Agent-03.EQP-CH-CENT-002"
          rated_power: 520
          
        - meter_id: "METER-ELEC-L3-CH-003"
          name: "3号冷机电表"
          meter_type: "PHYSICAL"
          accuracy_class: "B"
          parent_meter: "METER-ELEC-L2-CHP"
          rated_power: 520
          
        - meter_id: "METER-ELEC-L3-CH-004"
          name: "4号冷机电表"
          meter_type: "PHYSICAL"
          accuracy_class: "B"
          parent_meter: "METER-ELEC-L2-CHP"
          rated_power: 520
          
        - meter_id: "METER-ELEC-L3-CHWP"
          name: "冷冻水泵组电表"
          meter_type: "PHYSICAL"
          accuracy_class: "B"
          parent_meter: "METER-ELEC-L2-CHP"
          
          equipment_count: 5
          total_rated_power: 185  # kW
          
        - meter_id: "METER-ELEC-L3-CWP"
          name: "冷却水泵组电表"
          meter_type: "PHYSICAL"
          accuracy_class: "B"
          parent_meter: "METER-ELEC-L2-CHP"
          
          equipment_count: 5
          total_rated_power: 165  # kW
          
        - meter_id: "METER-ELEC-L3-CT"
          name: "冷却塔电表"
          meter_type: "PHYSICAL"
          accuracy_class: "B"
          parent_meter: "METER-ELEC-L2-CHP"
          
          equipment_count: 4
          total_rated_power: 60  # kW
          
  # ─────────────────────────────────────────────────────────────────────────────
  # 1.3 冷热量计量网络 (Thermal Metering Network)
  # ─────────────────────────────────────────────────────────────────────────────
  
  thermal_metering_network:
    
    system_ref: "Agent-01.HVAC"
    total_physical_meters: 42
    
    # 冷量计量
    cooling_metering:
      
      # L1层：冷站总冷量
      L1_total_cooling:
        
        - meter_id: "METER-CLG-L1-001"
          name: "冷站总冷量表"
          meter_type: "PHYSICAL"
          accuracy_class: "A"
          accuracy_grade: "2级"
          
          installation:
            location: "冷冻水总管供回水"
            topology_node: "Agent-01.HVAC-CHP_DIST_HEADER"
            
          technical_specs:
            meter_type: "超声波热量表"
            flow_range: "100-2000 m³/h"
            temp_sensor: "PT1000配对"
            
          data_interface:
            protocol: "M-Bus"
            data_point_ref: "Agent-06.AI_COOLING_TOTAL"
            parameters:
              - param: "累计冷量"
                unit: "kWh"
              - param: "瞬时冷量"
                unit: "kW"
              - param: "累计流量"
                unit: "m³"
              - param: "供水温度"
                unit: "°C"
              - param: "回水温度"
                unit: "°C"
                
      # L2层：分区冷量
      L2_zone_cooling:
        
        - meter_id: "METER-CLG-L2-SURG"
          name: "手术部冷量表"
          meter_type: "PHYSICAL"
          accuracy_class: "A"
          parent_meter: "METER-CLG-L1-001"
          
          installation:
            location: "手术部空调机房冷冻水入口"
            topology_node: "Agent-01.HVAC-AHU_Zone_Surgery"
            
          flow_range: "20-400 m³/h"
          
          accreditation_reference:
            clause: "2.3.5 手术室环境能耗"
            
        - meter_id: "METER-CLG-L2-ICU"
          name: "ICU冷量表"
          meter_type: "PHYSICAL"
          accuracy_class: "A"
          parent_meter: "METER-CLG-L1-001"
          
        - meter_id: "METER-CLG-L2-WARD"
          name: "住院楼冷量表"
          meter_type: "PHYSICAL"
          accuracy_class: "B"
          parent_meter: "METER-CLG-L1-001"
          
        - meter_id: "METER-CLG-L2-OPD"
          name: "门诊楼冷量表"
          meter_type: "PHYSICAL"
          accuracy_class: "B"
          parent_meter: "METER-CLG-L1-001"
          
      # L3层：AHU冷量
      L3_ahu_cooling:
        
        - meter_id: "METER-CLG-L3-AHU-OR01"
          name: "手术室1号AHU冷量表"
          meter_type: "PHYSICAL"
          accuracy_class: "B"
          parent_meter: "METER-CLG-L2-SURG"
          
          equipment_ref: "Agent-03.EQP-AHU-CLEAN-OR01"
          topology_node: "Agent-01.HVAC-AHU_SINK_AHU_OR01"
          
          serves_spaces:
            - "OR-01 (I级手术室)"
            - "OR-01-PREP (准备间)"
            - "OR-01-WASH (洗手间)"
            
        - meter_id: "METER-CLG-L3-AHU-OR02"
          name: "手术室2号AHU冷量表"
          meter_type: "PHYSICAL"
          accuracy_class: "B"
          parent_meter: "METER-CLG-L2-SURG"
          
        # ... 更多AHU冷量表
        
    # 热量计量
    heating_metering:
      
      - meter_id: "METER-HTG-L1-001"
        name: "热站总热量表"
        meter_type: "PHYSICAL"
        accuracy_class: "A"
        
        installation:
          location: "热水总管供回水"
          topology_node: "Agent-01.HVAC-HHP"
          
  # ─────────────────────────────────────────────────────────────────────────────
  # 1.4 水资源计量网络 (Water Metering Network)
  # ─────────────────────────────────────────────────────────────────────────────
  
  water_metering_network:
    
    system_ref: "Agent-01.PLUMB"
    total_physical_meters: 35
    
    # L1层：总进水
    L1_master_meters:
      
      - meter_id: "METER-WATER-L1-001"
        name: "市政自来水总进水表"
        meter_type: "PHYSICAL"
        accuracy_class: "A"
        
        installation:
          location: "水泵房市政进水总管"
          topology_node: "Agent-01.PLUMB-DWS_SRC_MUNICIPAL"
          
        technical_specs:
          meter_type: "超声波水表"
          nominal_diameter: "DN150"
          flow_range: "Q3=160 m³/h"
          
        billing:
          utility_company: "市自来水公司"
          tariff: "阶梯水价"
          
    # L2层：分区用水
    L2_zone_meters:
      
      - meter_id: "METER-WATER-L2-SURG"
        name: "手术部用水表"
        meter_type: "PHYSICAL"
        accuracy_class: "B"
        parent_meter: "METER-WATER-L1-001"
        
      - meter_id: "METER-WATER-L2-CW-MAKEUP"
        name: "冷却水补水表"
        meter_type: "PHYSICAL"
        accuracy_class: "B"
        parent_meter: "METER-WATER-L1-001"
        
        note: "用于计算冷却塔蒸发量和浓缩倍数"
        
  # ─────────────────────────────────────────────────────────────────────────────
  # 1.5 医用气体计量网络 (Medical Gas Metering Network)
  # ─────────────────────────────────────────────────────────────────────────────
  
  medical_gas_metering_network:
    
    system_ref: "Agent-01.MGAS"
    total_physical_meters: 28
    
    # 氧气计量
    oxygen_metering:
      
      - meter_id: "METER-O2-L1-001"
        name: "液氧储罐总出口流量计"
        meter_type: "PHYSICAL"
        accuracy_class: "A"
        
        installation:
          location: "液氧站汽化器出口"
          topology_node: "Agent-01.MGAS-O2_SRC_LOX"
          
        technical_specs:
          meter_type: "涡街流量计"
          gas_type: "O2"
          pressure: "0.4-0.5 MPa"
          
      - meter_id: "METER-O2-L2-SURG"
        name: "手术部氧气分区表"
        meter_type: "PHYSICAL"
        accuracy_class: "B"
        parent_meter: "METER-O2-L1-001"
        
      - meter_id: "METER-O2-L2-ICU"
        name: "ICU氧气分区表"
        meter_type: "PHYSICAL"
        accuracy_class: "B"
        parent_meter: "METER-O2-L1-001"
        
    # 真空计量
    vacuum_metering:
      
      - meter_id: "METER-VAC-L1-001"
        name: "真空泵站总流量计"
        meter_type: "PHYSICAL"
        accuracy_class: "B"
        
    # 压缩空气计量
    compressed_air_metering:
      
      - meter_id: "METER-AIR-L1-001"
        name: "空压机站总流量计"
        meter_type: "PHYSICAL"
        accuracy_class: "B"
        
  # ─────────────────────────────────────────────────────────────────────────────
  # 1.6 能量守恒校验规则 (Energy Conservation Validation)
  # ─────────────────────────────────────────────────────────────────────────────
  
  energy_conservation_validation:
    
    principle: |
      基于能量守恒定律：∑Sub_Meters ≤ Master_Meter × (1 + Loss_Factor)
      所有子表之和不应超过母表读数加上允许损耗
      
    validation_rules:
      
      # 电力守恒
      electrical_balance:
        
        - rule_id: "VAL-ELEC-001"
          name: "高压进线平衡"
          equation: |
            (METER-ELEC-L1-001 + METER-ELEC-L1-002) × η_TR 
            ≥ Σ(METER-ELEC-L2-TR1 + TR2 + TR3 + TR4)
          loss_factor:
            transformer_loss: "2-3%"
            line_loss: "1-2%"
          tolerance: "5%"
          alert_threshold: "8%"
          
        - rule_id: "VAL-ELEC-002"
          name: "变压器出口平衡"
          equation: |
            METER-ELEC-L2-TR1 ≥ Σ(所有下级L3表) × (1 - 3%)
          loss_factor: "3%"
          tolerance: "5%"
          
        - rule_id: "VAL-ELEC-003"
          name: "冷站电力平衡"
          equation: |
            METER-ELEC-L2-CHP ≥ 
            (METER-ELEC-L3-CH-001 + CH-002 + CH-003 + CH-004
             + METER-ELEC-L3-CHWP + CWP + CT) × 0.98
          loss_factor: "2%"
          
      # 冷量守恒
      cooling_balance:
        
        - rule_id: "VAL-CLG-001"
          name: "冷站总冷量平衡"
          equation: |
            METER-CLG-L1-001 ≥ 
            Σ(METER-CLG-L2-SURG + ICU + WARD + OPD) × 0.95
          loss_factor:
            pipe_loss: "3-5%"
            measurement_error: "2%"
          tolerance: "7%"
          
      # 水量守恒
      water_balance:
        
        - rule_id: "VAL-WATER-001"
          name: "总用水平衡"
          equation: |
            METER-WATER-L1-001 ≥ Σ(所有L2水表) × 0.95
          loss_factor: "5% (含漏损)"
          
    validation_frequency: "每小时自动校验"
    
    exception_handling:
      if_imbalance_detected:
        - action: "生成告警工单"
        - action: "标记数据为'待核实'"
        - action: "启动传感器诊断"
      if_meter_failure:
        - action: "启用虚拟计量替代"
        - action: "标记数据来源为'估算'"
```

---

## 第二部分：虚拟计量网络 (Virtual Metering Layer)

```yaml
# ═══════════════════════════════════════════════════════════════════════════════
# Phase 2: 虚拟计量网络
# 利用物理模型补全"最后一公里"的计量盲区
# ═══════════════════════════════════════════════════════════════════════════════

Virtual_Metering_Network:
  
  meta:
    phase: "Phase 2"
    description: "基于Agent-04物理方程构建虚拟计量"
    total_virtual_meters: 520
    
  # ─────────────────────────────────────────────────────────────────────────────
  # 2.1 虚拟计量精度分级 (Accuracy Classification)
  # ─────────────────────────────────────────────────────────────────────────────
  
  accuracy_classification:
    
    class_A:
      name: "物理高精度表"
      description: "用于计费的高精度物理仪表"
      accuracy: "0.5-1.0级"
      uncertainty: "±0.5-1.0%"
      usage: "对外计费、法定计量"
      trust_level: "HIGH"
      
    class_B:
      name: "物理普通表"
      description: "用于内部核算的标准物理仪表"
      accuracy: "1.0-2.0级"
      uncertainty: "±1.0-2.0%"
      usage: "分区计量、成本分析"
      trust_level: "MEDIUM-HIGH"
      
    class_C:
      name: "虚拟计量-强相关"
      description: "基于强相关物理参数的虚拟计算"
      calculation_basis: "流量计+温差（Q=ρVCpΔT）"
      uncertainty: "±5-10%"
      usage: "末端分摊、科室核算"
      trust_level: "MEDIUM"
      required_inputs:
        - "实测流量"
        - "实测温度（供回水）"
        
    class_D:
      name: "虚拟计量-估算"
      description: "基于额定功率和运行时间的估算"
      calculation_basis: "P_rated × Run_Hours × Load_Factor"
      uncertainty: "±15-25%"
      usage: "参考分析、趋势跟踪"
      trust_level: "LOW"
      required_inputs:
        - "设备额定功率（Agent-03）"
        - "运行状态（Agent-06.DI_RUN）"
        - "负载率估算"
        
  # ─────────────────────────────────────────────────────────────────────────────
  # 2.2 末端冷量虚拟计量 (Terminal Cooling Virtual Metering)
  # ─────────────────────────────────────────────────────────────────────────────
  
  terminal_cooling_virtual_metering:
    
    description: |
      针对未安装物理表的末端设备（FCU、VAV、AHU表冷器），
      利用Agent-04的热力学公式建立虚拟冷量表
      
    # FCU冷量虚拟表
    fcu_virtual_meters:
      
      template:
        meter_type: "VIRTUAL"
        accuracy_class: "C"
        
        equation_ref: "Agent-04.EQ-CARRIER-PAYLOAD-WATER"
        formula: |
          Q_cooling = ρ × V × Cp × (T_return - T_supply)
          
          其中:
            ρ = 1000 kg/m³ (水密度)
            V = 实测流量 m³/s (来自阀门开度+压差推算)
            Cp = 4.186 kJ/(kg·K) (水比热)
            T_return = 回水温度 °C
            T_supply = 供水温度 °C (取系统供水温度)
            
        data_sources:
          flow:
            primary: "Agent-06.AI_FLOW_FCU_xxx"
            fallback: "阀门开度 × 额定流量"
          temperature:
            supply: "Agent-06.AI_CHWS_TEMP (系统供水)"
            return: "Agent-06.AI_FCU_RETURN_xxx (如有)"
            fallback: "供水温度 + 5°C (经验值)"
            
      instances:
        
        # 手术室FCU（实际手术室通常用AHU，此处为辅助区域）
        surgery_support_fcu:
          
          - meter_id: "VMETER-CLG-FCU-SUR-001"
            name: "手术区走廊FCU-1虚拟冷量"
            meter_type: "VIRTUAL"
            accuracy_class: "C"
            
            parent_meter: "METER-CLG-L2-SURG"
            
            equipment_ref: "Agent-03.EQP-FCU-4P-001"
            coupling_unit_ref: "Agent-05.CU-FCU-SUR-CORR-01"
            
            serves_space:
              space_id: "Agent-02.ROOM-SUR-CORR-01"
              space_type: "洁净走廊"
              area_m2: 45
              
            calculation:
              flow_source: "阀门开度推算"
              valve_point: "Agent-06.AO_FCU_VALVE_SUR001"
              rated_flow: 1.2  # m³/h
              
            data_quality:
              uncertainty: "±8%"
              confidence: "MEDIUM"
              
        # ICU床旁FCU
        icu_bedside_fcu:
          
          - meter_id: "VMETER-CLG-FCU-ICU-001"
            name: "ICU-1号床区FCU虚拟冷量"
            meter_type: "VIRTUAL"
            accuracy_class: "C"
            
            parent_meter: "METER-CLG-L2-ICU"
            
            equipment_ref: "Agent-03.EQP-FCU-4P-ICU-001"
            
            serves_space:
              space_id: "Agent-02.ROOM-ICU-BED-01"
              bed_count: 1
              
          # 批量生成30个ICU床位FCU虚拟表
          - meter_id_pattern: "VMETER-CLG-FCU-ICU-{001-030}"
            count: 30
            parent_meter: "METER-CLG-L2-ICU"
            
        # 普通病房FCU
        ward_fcu:
          
          - meter_id_pattern: "VMETER-CLG-FCU-WARD-{001-200}"
            description: "住院楼病房FCU虚拟冷量表"
            count: 200
            meter_type: "VIRTUAL"
            accuracy_class: "D"  # 降级为D类（无流量实测）
            
            parent_meter: "METER-CLG-L2-WARD"
            
            calculation:
              method: "额定功率 × 运行时间 × 负载系数"
              rated_cooling: 3.5  # kW
              load_factor: 0.65
              run_status_point: "Agent-06.DI_FCU_RUN_{xxx}"
              
    # AHU表冷器冷量虚拟表
    ahu_coil_virtual_meters:
      
      template:
        meter_type: "VIRTUAL"
        accuracy_class: "C"
        
        equation_ref: "Agent-04.EQ-HX-COIL-001"
        formula: |
          Q_coil = ρ_water × V_water × Cp_water × (T_chwr - T_chws)
          
          验证:
          Q_coil ≈ ρ_air × V_air × (h_supply - h_return)
          
      instances:
        
        - meter_id: "VMETER-CLG-COIL-AHU-OR01"
          name: "手术室1号AHU表冷器虚拟冷量"
          meter_type: "VIRTUAL"
          accuracy_class: "C"
          
          equipment_ref: "Agent-03.EQP-AHU-CLEAN-OR01"
          topology_node: "Agent-01.HVAC-AHU_SINK_AHU_OR01"
          
          # 如果有物理冷量表，则此虚拟表用于校验
          physical_meter_ref: "METER-CLG-L3-AHU-OR01"
          purpose: "VALIDATION"
          
          data_sources:
            water_flow: "Agent-06.AI_FLOW_AHU_OR01"
            water_temp_supply: "Agent-06.AI_CHWS_TEMP"
            water_temp_return: "Agent-06.AI_AHU_OR01_CHWR"
            air_flow: "Agent-06.AI_SUPPLY_AIR_FLOW_OR01"
            air_temp_supply: "Agent-06.AI_SUPPLY_AIR_TEMP_OR01"
            air_temp_return: "Agent-06.AI_RETURN_AIR_TEMP_OR01"
            
  # ─────────────────────────────────────────────────────────────────────────────
  # 2.3 设备电量虚拟计量 (Equipment Power Virtual Metering)
  # ─────────────────────────────────────────────────────────────────────────────
  
  equipment_power_virtual_metering:
    
    description: |
      针对未单独装表的设备，基于Agent-03额定功率
      和Agent-06运行状态进行虚拟计量
      
    # 电机类设备
    motor_driven_equipment:
      
      template:
        meter_type: "VIRTUAL"
        accuracy_class: "D"
        
        formula: |
          E = P_rated × η × LF × t
          
          其中:
            P_rated = 额定功率 kW (来自Agent-03)
            η = 电机效率 (典型0.85-0.95)
            LF = 负载系数 (来自VFD频率或工况判断)
            t = 运行时间 h (来自Agent-06.DI_RUN累计)
            
      instances:
        
        # AHU风机电量
        ahu_fan_power:
          
          - meter_id: "VMETER-ELEC-FAN-AHU-OR01"
            name: "手术室1号AHU送风机虚拟电量"
            meter_type: "VIRTUAL"
            accuracy_class: "D"
            
            parent_meter: "METER-ELEC-L3-HVAC-3F"
            
            equipment_ref: "Agent-03.EQP-AHU-CLEAN-OR01.supply_fan"
            
            parameters:
              rated_power: 22  # kW
              motor_efficiency: 0.92
              vfd_equipped: true
              
            data_sources:
              run_status: "Agent-06.DI_AHU_OR01_RUN"
              vfd_frequency: "Agent-06.AI_AHU_OR01_FAN_FREQ"
              
            calculation:
              load_factor_formula: "(VFD_Freq / 50)³"  # 风机定律
              
          - meter_id_pattern: "VMETER-ELEC-FAN-AHU-OR{02-12}"
            count: 11
            description: "其余手术室AHU风机虚拟电量"
            
        # 水泵电量（已有物理表的，此处做校验）
        pump_power:
          
          - meter_id: "VMETER-ELEC-PUMP-CHWP-001"
            name: "1号冷冻水泵虚拟电量"
            meter_type: "VIRTUAL"
            accuracy_class: "C"  # 有VFD频率，精度较高
            
            parent_meter: "METER-ELEC-L3-CHWP"
            purpose: "VALIDATION"
            
            equipment_ref: "Agent-03.EQP-PUMP-CHW-001"
            
            parameters:
              rated_power: 37  # kW
              motor_efficiency: 0.93
              vfd_equipped: true
              
            data_sources:
              run_status: "Agent-06.DI_CHWP1_RUN"
              vfd_frequency: "Agent-06.AI_CHWP1_FREQ"
              
    # 大型医疗设备
    major_medical_equipment:
      
      description: |
        CT/MRI/DSA等大型设备的虚拟电量计量，
        用于支持评审标准中的"设备利用率"指标
        
      instances:
        
        - meter_id: "VMETER-ELEC-CT-001"
          name: "1号CT虚拟电量"
          meter_type: "VIRTUAL"
          accuracy_class: "D"
          
          parent_meter: "METER-ELEC-L2-IMAG"
          
          equipment_ref: "Agent-03.EQP-CT-64SLICE-001"
          equipment_name: "飞利浦64排CT"
          
          parameters:
            rated_power: 120  # kW
            standby_power: 8  # kW
            scan_power: 80    # kW (平均扫描功率)
            
          data_sources:
            run_status: "Agent-06.DI_CT1_POWER_ON"
            scan_status: "Agent-06.DI_CT1_SCANNING"
            
          calculation:
            power_state_mapping:
              OFF: 0
              STANDBY: 8  # kW
              SCANNING: 80  # kW
              WARMING: 40  # kW
              
          accreditation_support:
            kpi: "设备开机利用率"
            formula: "Σ(扫描时间) / Σ(开机时间)"
            reference: "《三级医院评审标准》3.1.2"
            
        - meter_id: "VMETER-ELEC-MRI-001"
          name: "1号MRI虚拟电量"
          meter_type: "VIRTUAL"
          accuracy_class: "D"
          
          equipment_ref: "Agent-03.EQP-MRI-3T-001"
          
          parameters:
            rated_power: 200  # kW
            standby_power: 25  # kW (含梯度冷却)
            scan_power: 150   # kW
            
          data_sources:
            run_status: "Agent-06.DI_MRI1_POWER_ON"
            scan_status: "Agent-06.DI_MRI1_SCANNING"
            
  # ─────────────────────────────────────────────────────────────────────────────
  # 2.4 空间能耗虚拟计量 (Space Energy Virtual Metering)
  # ─────────────────────────────────────────────────────────────────────────────
  
  space_energy_virtual_metering:
    
    description: |
      为每个房间/空间建立虚拟能耗表，
      作为科室分摊和评审指标的基础
      
    # 手术室空间能耗
    operating_room_energy:
      
      - meter_id: "VMETER-SPACE-OR-01"
        name: "1号手术室综合能耗"
        meter_type: "VIRTUAL"
        accuracy_class: "C"
        
        space_ref: "Agent-02.ROOM-OR-CLASS-I-01"
        coupling_unit_ref: "Agent-05.CU-AHU-OR-01"
        
        energy_components:
          
          electricity:
            sources:
              - component: "洁净空调送风机"
                meter_ref: "VMETER-ELEC-FAN-AHU-OR01"
                allocation: "100%"
              - component: "表冷器冷冻水泵分摊"
                meter_ref: "VMETER-ELEC-PUMP-CHWP-{001-005}"
                allocation_rule: "按冷量比例"
              - component: "照明"
                meter_ref: "按面积分摊"
                area_factor: 52  # m²
              - component: "医疗设备"
                meter_ref: "估算"
                typical_value: 5  # kWh/手术
                
          cooling:
            sources:
              - component: "AHU表冷器冷量"
                meter_ref: "VMETER-CLG-COIL-AHU-OR01"
                allocation: "100%"
                
          medical_gas:
            sources:
              - component: "氧气"
                meter_ref: "VMETER-O2-OR-01"
              - component: "负压吸引"
                meter_ref: "VMETER-VAC-OR-01"
              - component: "压缩空气"
                meter_ref: "VMETER-AIR-OR-01"
                
        kpi_output:
          - kpi: "单台手术能耗"
            unit: "kWh/台"
          - kpi: "单间单日能耗"
            unit: "kWh/间·日"
            
        accreditation_reference:
          clause: "2.3.5"
          requirement: "手术室单台次能耗监测"
          
      - meter_id_pattern: "VMETER-SPACE-OR-{02-12}"
        count: 11
        description: "其余手术室综合能耗虚拟表"
        
    # ICU床位能耗
    icu_bed_energy:
      
      - meter_id: "VMETER-SPACE-ICU-BED-01"
        name: "ICU-1号床位综合能耗"
        meter_type: "VIRTUAL"
        accuracy_class: "C"
        
        space_ref: "Agent-02.ROOM-ICU-BED-01"
        
        energy_components:
          electricity:
            sources:
              - component: "床旁设备"
                typical_value: 8  # kWh/日
              - component: "照明分摊"
                allocation_rule: "按床位数"
              - component: "空调分摊"
                allocation_rule: "按面积"
                
        kpi_output:
          - kpi: "ICU单床日能耗"
            unit: "kWh/床·日"
            
        accreditation_reference:
          clause: "2.3.4"
          requirement: "ICU单床日资源消耗≤80kWh"
          
      - meter_id_pattern: "VMETER-SPACE-ICU-BED-{02-30}"
        count: 29
        
    # 透析站点能耗
    dialysis_station_energy:
      
      - meter_id: "VMETER-SPACE-DIAL-STAT-01"
        name: "透析1号站点综合能耗"
        meter_type: "VIRTUAL"
        accuracy_class: "D"
        
        space_ref: "Agent-02.ROOM-DIAL-STATION-01"
        
        energy_components:
          electricity:
            sources:
              - component: "透析机"
                rated_power: 1.5  # kW
              - component: "水处理分摊"
                allocation_rule: "按站点数"
                
        kpi_output:
          - kpi: "单次透析能耗"
            unit: "kWh/次"
            
      - meter_id_pattern: "VMETER-SPACE-DIAL-STAT-{02-50}"
        count: 49
```

---

## 第三部分：财务分摊逻辑 (Financial Allocation Layer)

```yaml
# ═══════════════════════════════════════════════════════════════════════════════
# Phase 3: 财务分摊逻辑
# 解决"公摊"问题，实现科室级全成本核算
# ═══════════════════════════════════════════════════════════════════════════════

Financial_Allocation_Model:
  
  meta:
    phase: "Phase 3"
    description: "建立计量节点到科室的归属映射和分摊算法"
    total_allocation_rules: 24
    cost_centers_covered: 45
    
  # ─────────────────────────────────────────────────────────────────────────────
  # 3.1 科室-计量映射 (Department-Meter Mapping)
  # ─────────────────────────────────────────────────────────────────────────────
  
  department_meter_mapping:
    
    mapping_principle: |
      每个计量点（物理或虚拟）必须映射到唯一的成本中心，
      公共系统能耗按规则分摊
      
    direct_mapping:
      description: "直接归属的计量点"
      
      mappings:
        
        - meter_id: "METER-ELEC-L2-SURG"
          org_id: "Agent-02.ORG-SURGERY"
          org_name: "手术部"
          cost_center: "CC-SURGERY"
          allocation_type: "DIRECT"
          allocation_ratio: 1.0
          
        - meter_id: "METER-ELEC-L2-ICU"
          org_id: "Agent-02.ORG-ICU"
          org_name: "重症医学科"
          cost_center: "CC-ICU"
          allocation_type: "DIRECT"
          allocation_ratio: 1.0
          
        - meter_id: "METER-ELEC-L2-DIAL"
          org_id: "Agent-02.ORG-DIALYSIS"
          org_name: "透析中心"
          cost_center: "CC-DIALYSIS"
          allocation_type: "DIRECT"
          allocation_ratio: 1.0
          
        - meter_id: "METER-ELEC-L2-IMAG"
          org_id: "Agent-02.ORG-RADIOLOGY"
          org_name: "放射科"
          cost_center: "CC-RADIOLOGY"
          allocation_type: "DIRECT"
          allocation_ratio: 1.0
          
    shared_mapping:
      description: "需要分摊的公共系统"
      
      shared_systems:
        - "冷冻站"
        - "热力站"
        - "水泵房"
        - "公共照明"
        - "电梯"
        - "消防系统"
        
  # ─────────────────────────────────────────────────────────────────────────────
  # 3.2 分摊算法库 (Allocation Algorithm Library)
  # ─────────────────────────────────────────────────────────────────────────────
  
  allocation_algorithms:
    
    # 算法1：冷站公摊
    algorithm_1_chiller_plant:
      
      algorithm_id: "ALLOC-CHP-001"
      name: "冷站能耗分摊算法"
      description: |
        基于末端虚拟冷量的比例，将冷站总电耗分摊给各科室
        
      inputs:
        numerator:
          source: "虚拟冷量表 (Phase 2)"
          examples:
            - "VMETER-CLG-COIL-AHU-OR01"
            - "VMETER-CLG-FCU-ICU-{001-030}"
        denominator:
          source: "冷站总冷量表"
          meter: "METER-CLG-L1-001"
        energy_to_allocate:
          source: "冷站总电表"
          meter: "METER-ELEC-L2-CHP"
          
      formula: |
        E_dept = E_CHP × (Q_dept / Q_total)
        
        其中:
          E_dept = 分摊给科室的冷站电耗 (kWh)
          E_CHP = 冷站总电耗 (kWh)
          Q_dept = 科室末端冷量 (kWh_th)
          Q_total = 冷站总供冷量 (kWh_th)
          
      example_calculation:
        scenario: "2024年7月"
        data:
          E_CHP: 450000  # kWh
          Q_total: 2800000  # kWh_th
          Q_surgery: 280000  # kWh_th (手术部)
          Q_icu: 140000  # kWh_th (ICU)
        result:
          E_surgery: 45000  # kWh
          E_icu: 22500  # kWh
          
      allocation_frequency: "月度"
      
    # 算法2：加权面积分摊
    algorithm_2_weighted_area:
      
      algorithm_id: "ALLOC-AREA-001"
      name: "加权面积分摊算法"
      description: |
        对于无法按冷量/用电量直接计量的公共区域能耗，
        按加权面积分摊，不同空间类型赋予不同权重
        
      weight_factors:
        
        # 洁净区域权重高
        cleanroom_weights:
          - space_type: "ISO 5级洁净区（层流手术室）"
            weight: 3.0
            rationale: "24小时高换气次数，能耗密度高"
          - space_type: "ISO 6级洁净区"
            weight: 2.5
          - space_type: "ISO 7级洁净区（ICU）"
            weight: 2.0
          - space_type: "ISO 8级洁净区"
            weight: 1.5
            
        # 特殊区域权重
        special_area_weights:
          - space_type: "数据中心/机房"
            weight: 4.0
          - space_type: "影像检查室（CT/MRI）"
            weight: 2.5
          - space_type: "实验室"
            weight: 2.0
          - space_type: "药房/药库"
            weight: 1.5
            
        # 一般区域
        general_area_weights:
          - space_type: "诊室"
            weight: 1.2
          - space_type: "病房"
            weight: 1.0
          - space_type: "办公室"
            weight: 1.0
          - space_type: "走廊/公共区"
            weight: 0.8
          - space_type: "楼梯间/卫生间"
            weight: 0.5
            
      formula: |
        E_dept = E_shared × (A_dept × W_dept) / Σ(A_i × W_i)
        
        其中:
          A_dept = 科室面积 (m²)
          W_dept = 科室加权系数
          
      example_calculation:
        scenario: "公共照明电耗分摊"
        data:
          E_shared: 50000  # kWh/月
          surgery:
            area: 2800  # m²
            weight: 2.5  # 含洁净走廊
          icu:
            area: 1200
            weight: 2.0
          ward:
            area: 15000
            weight: 1.0
        calculation:
          total_weighted_area: "2800×2.5 + 1200×2.0 + 15000×1.0 = 24400"
          surgery_share: "50000 × 7000/24400 = 14344 kWh"
          
    # 算法3：时间分摊
    algorithm_3_time_based:
      
      algorithm_id: "ALLOC-TIME-001"
      name: "时间分摊算法"
      description: |
        对于多科室共用的设备，基于使用时间进行分摊
        典型应用：共用CT/MRI、共用手术室
        
      data_sources:
        schedule_system: "HIS手术排程/检查排程"
        run_log: "Agent-06设备运行日志"
        
      formula: |
        E_dept = E_equipment × (T_dept / T_total)
        
        其中:
          T_dept = 科室使用时间 (h)
          T_total = 设备总运行时间 (h)
          
      example:
        equipment: "CT-001"
        month: "2024-07"
        total_run_hours: 400
        usage_by_dept:
          - dept: "急诊科"
            hours: 120
            share: "30%"
          - dept: "神经外科"
            hours: 80
            share: "20%"
          - dept: "骨科"
            hours: 60
            share: "15%"
          - dept: "其他"
            hours: 140
            share: "35%"
            
    # 算法4：床日分摊
    algorithm_4_bed_day:
      
      algorithm_id: "ALLOC-BEDDAY-001"
      name: "床日分摊算法"
      description: |
        按实际占用床日数分摊住院区公共能耗
        
      data_sources:
        bed_days: "HIS床位管理系统"
        
      formula: |
        E_dept = E_inpatient_common × (BD_dept / BD_total)
        
        其中:
          BD_dept = 科室床日数
          BD_total = 全院床日数
          
    # 算法5：人流量分摊
    algorithm_5_traffic:
      
      algorithm_id: "ALLOC-TRAFFIC-001"
      name: "人流量分摊算法"
      description: |
        按就诊/到访人数分摊门诊区公共能耗
        
      data_sources:
        outpatient_visits: "HIS门诊挂号系统"
        people_counter: "智能人流计数系统"
        
  # ─────────────────────────────────────────────────────────────────────────────
  # 3.3 分摊规则配置 (Allocation Rule Configuration)
  # ─────────────────────────────────────────────────────────────────────────────
  
  allocation_rules:
    
    - rule_id: "RULE-ALLOC-001"
      name: "冷站电耗分摊"
      source_meter: "METER-ELEC-L2-CHP"
      algorithm: "ALLOC-CHP-001"
      target_cost_centers: "ALL"
      frequency: "月度"
      
    - rule_id: "RULE-ALLOC-002"
      name: "热站电耗分摊"
      source_meter: "METER-ELEC-L2-HHP"
      algorithm: "ALLOC-CHP-001"  # 同冷站逻辑
      target_cost_centers: "ALL"
      frequency: "月度"
      
    - rule_id: "RULE-ALLOC-003"
      name: "公共区域照明分摊"
      source_meter: "METER-ELEC-L3-LIGHT-COMMON"
      algorithm: "ALLOC-AREA-001"
      weight_profile: "general_area_weights"
      target_cost_centers: "ALL"
      frequency: "月度"
      
    - rule_id: "RULE-ALLOC-004"
      name: "电梯能耗分摊"
      source_meter: "METER-ELEC-L3-ELEVATOR"
      algorithm: "ALLOC-TRAFFIC-001"
      target_cost_centers: "ALL"
      frequency: "月度"
      
    - rule_id: "RULE-ALLOC-005"
      name: "CT共用分摊"
      source_meter: "VMETER-ELEC-CT-001"
      algorithm: "ALLOC-TIME-001"
      target_cost_centers: ["急诊科", "神经外科", "骨科", "普外科"]
      frequency: "月度"
      
    - rule_id: "RULE-ALLOC-006"
      name: "住院楼公共能耗分摊"
      source_meter: "METER-ELEC-L3-WARD-COMMON"
      algorithm: "ALLOC-BEDDAY-001"
      target_cost_centers: "INPATIENT_DEPTS"
      frequency: "月度"
      
  # ─────────────────────────────────────────────────────────────────────────────
  # 3.4 科室能耗账单 (Department Energy Bill)
  # ─────────────────────────────────────────────────────────────────────────────
  
  department_energy_bill:
    
    template:
      bill_id: "BILL-{YYYY}-{MM}-{DEPT_CODE}"
      
      sections:
        
        direct_consumption:
          name: "直接能耗"
          items:
            - item: "电力直接用量"
              source: "直属电表读数"
            - item: "冷量直接用量"
              source: "直属冷量表读数"
            - item: "水直接用量"
              source: "直属水表读数"
              
        allocated_consumption:
          name: "分摊能耗"
          items:
            - item: "冷站分摊"
              source: "RULE-ALLOC-001"
            - item: "热站分摊"
              source: "RULE-ALLOC-002"
            - item: "公共照明分摊"
              source: "RULE-ALLOC-003"
            - item: "电梯分摊"
              source: "RULE-ALLOC-004"
              
        total_consumption:
          name: "能耗合计"
          calculation: "直接 + 分摊"
          
        cost_calculation:
          name: "费用计算"
          items:
            - item: "电费"
              formula: "电量 × 综合电价"
            - item: "水费"
              formula: "水量 × 水价"
            - item: "燃气费"
              formula: "气量 × 气价"
              
        kpi_section:
          name: "效率指标"
          items:
            - kpi: "单床日能耗"
            - kpi: "人均能耗"
            - kpi: "同比变化"
            
    example_bill:
      bill_id: "BILL-2024-07-SURGERY"
      period: "2024年7月"
      department: "手术部"
      
      direct_consumption:
        electricity:
          meter: "METER-ELEC-L2-SURG"
          value: 125000
          unit: "kWh"
        cooling:
          meter: "METER-CLG-L2-SURG"
          value: 280000
          unit: "kWh_th"
          
      allocated_consumption:
        chiller_plant:
          rule: "RULE-ALLOC-001"
          value: 45000
          unit: "kWh"
          ratio: "10%"
        public_lighting:
          rule: "RULE-ALLOC-003"
          value: 3500
          unit: "kWh"
          ratio: "7%"
          
      total:
        electricity: 173500  # kWh
        cooling: 280000  # kWh_th
        
      cost:
        electricity: 138800  # 元 (0.8元/kWh)
        total: 145000  # 元
        
      kpi:
        surgeries_count: 650
        energy_per_surgery: 267  # kWh/台
        yoy_change: "-3.2%"
```

---

## 第四部分：评审指标与绩效建模 (Accreditation & Performance Layer)

```yaml
# ═══════════════════════════════════════════════════════════════════════════════
# Phase 4: 评审指标与绩效建模
# 直接响应《三级医院评审标准（2025年版）》的数据监测要求
# ═══════════════════════════════════════════════════════════════════════════════

Accreditation_Performance_Model:
  
  meta:
    phase: "Phase 4"
    description: "构建符合评审标准的绩效指标体系"
    total_kpi_indicators: 35
    accreditation_clauses_covered: 12
    
  # ─────────────────────────────────────────────────────────────────────────────
  # 4.1 资源效率指标 (Resource Efficiency KPIs)
  # ─────────────────────────────────────────────────────────────────────────────
  
  resource_efficiency_kpis:
    
    # 全院综合指标
    hospital_wide_kpis:
      
      - kpi_id: "KPI-EFF-001"
        name: "每门诊人次能耗"
        name_en: "Energy Consumption per Outpatient Visit"
        
        accreditation_reference:
          standard: "《三级医院评审标准（2025年版）》"
          chapter: "第一章"
          section: "第二节 资源效率监测"
          clause: "1.2.3.1"
          requirement: "医院应建立资源效率监测体系，定期统计每门诊人次能耗"
          
        calculation:
          formula: |
            KPI = E_outpatient_total / N_outpatient_visits
            
          numerator:
            description: "门诊区域总能耗"
            source: "Phase 3分摊后门诊区电+冷+热"
            meters:
              - "METER-ELEC-L2-OPD及分摊"
              - "METER-CLG-L2-OPD"
            unit: "kWh (标准煤当量)"
            conversion: "电×1.0 + 冷×0.3 + 热×0.35"
            
          denominator:
            description: "门诊人次"
            source: "HIS门诊挂号系统"
            api: "HIS.Outpatient.GetVisitCount(period)"
            unit: "人次"
            
        unit: "kWh/人次"
        
        target:
          excellent: "< 8"
          good: "8-12"
          acceptable: "12-15"
          poor: "> 15"
          
        frequency: "月度"
        
        trend_analysis:
          baseline: "2024年同期"
          yoy_target: "下降3%"
          
      - kpi_id: "KPI-EFF-002"
        name: "每住院床日能耗"
        name_en: "Energy Consumption per Inpatient Bed-Day"
        
        accreditation_reference:
          clause: "1.2.3.2"
          requirement: "住院区域能耗应按床日统计"
          
        calculation:
          formula: "KPI = E_inpatient_total / BD_total"
          
          numerator:
            description: "住院区域总能耗"
            source: "住院楼电+冷+热+医气"
            
          denominator:
            description: "实际占用床日数"
            source: "HIS床位管理系统"
            
        unit: "kWh/床·日"
        
        target:
          excellent: "< 60"
          good: "60-80"
          acceptable: "80-100"
          poor: "> 100"
          
      - kpi_id: "KPI-EFF-003"
        name: "万元收入能耗"
        name_en: "Energy Consumption per 10,000 RMB Revenue"
        
        accreditation_reference:
          clause: "1.2.3.3"
          requirement: "建立能耗与业务产出的关联分析"
          
        calculation:
          formula: "KPI = E_hospital_total / (Revenue_total / 10000)"
          
          numerator:
            description: "全院总能耗"
            source: "L1总表汇总"
            
          denominator:
            description: "医疗收入（万元）"
            source: "财务系统"
            
        unit: "kWh/万元"
        
        target:
          excellent: "< 200"
          good: "200-300"
          acceptable: "300-400"
          poor: "> 400"
          
      - kpi_id: "KPI-EFF-004"
        name: "单位建筑面积能耗"
        name_en: "Energy Use Intensity (EUI)"
        
        accreditation_reference:
          clause: "1.2.3.4"
          supporting_standard: "GB/T 51161-2016"
          
        calculation:
          formula: "KPI = E_total / A_total"
          
          numerator:
            description: "全院总能耗（折标煤）"
            
          denominator:
            description: "建筑总面积"
            source: "Agent-02.建筑面积"
            value: 180000  # m²
            
        unit: "kWh/(m²·a)"
        
        target:
          hospital_benchmark: "100-150 kWh/(m²·a)"
          
    # 能效比指标
    efficiency_ratio_kpis:
      
      - kpi_id: "KPI-EFF-005"
        name: "冷站综合COP"
        name_en: "Chiller Plant Comprehensive COP"
        
        accreditation_reference:
          clause: "1.2.4.1"
          requirement: "冷源系统能效监测"
          
        calculation:
          formula: "COP = Q_cooling / E_chiller_plant"
          
          numerator:
            description: "冷站总供冷量"
            meter: "METER-CLG-L1-001"
            unit: "kWh_th"
            
          denominator:
            description: "冷站总电耗"
            meter: "METER-ELEC-L2-CHP"
            unit: "kWh_e"
            
        unit: "-"
        
        target:
          excellent: "> 4.5"
          good: "4.0-4.5"
          acceptable: "3.5-4.0"
          poor: "< 3.5"
          
  # ─────────────────────────────────────────────────────────────────────────────
  # 4.2 重点科室监测指标 (Key Department Monitoring KPIs)
  # ─────────────────────────────────────────────────────────────────────────────
  
  key_department_kpis:
    
    # ICU指标
    icu_kpis:
      
      - kpi_id: "KPI-ICU-001"
        name: "ICU单床日电力消耗强度"
        name_en: "ICU Electricity Intensity per Bed-Day"
        
        accreditation_reference:
          standard: "《三级医院评审标准（2025年版）》"
          chapter: "第二章"
          section: "第三节 重点科室质量管理"
          clause: "2.3.4"
          requirement: "ICU资源利用效率监测，单床日能耗应有监测和分析"
          
        calculation:
          formula: "KPI = E_ICU_total / BD_ICU"
          
          numerator:
            description: "ICU总电耗（含分摊）"
            meters:
              direct: "METER-ELEC-L2-ICU"
              allocated: "冷站分摊 + 公共分摊"
              
          denominator:
            description: "ICU占用床日"
            source: "HIS"
            api: "HIS.ICU.GetBedDays(period)"
            typical_value: 850  # 30床×95%×30天
            
        unit: "kWh/床·日"
        
        target:
          excellent: "< 60"
          good: "60-80"
          acceptable: "80-100"
          alert: "> 100"
          
        monitoring:
          frequency: "日报"
          alert_threshold: "> 100 kWh/床·日"
          
      - kpi_id: "KPI-ICU-002"
        name: "ICU环境达标率"
        name_en: "ICU Environmental Compliance Rate"
        
        accreditation_reference:
          clause: "2.3.4.2"
          requirement: "ICU环境参数应持续达标"
          
        calculation:
          formula: "CR = T_compliant / T_total × 100%"
          
          parameters:
            temperature: "22-26°C"
            humidity: "40-60%RH"
            pressure: "正压 ≥ 5Pa"
            
          data_source: "Agent-06.AI_ROOM_TEMP/HUMID/PRESS"
          
        unit: "%"
        target: "> 99.5%"
        
    # 手术室指标
    surgery_kpis:
      
      - kpi_id: "KPI-OR-001"
        name: "单台手术能耗"
        name_en: "Energy Consumption per Surgery"
        
        accreditation_reference:
          clause: "2.3.5"
          requirement: "手术室资源利用效率监测"
          
        calculation:
          formula: "KPI = E_surgery_total / N_surgeries"
          
          numerator:
            description: "手术部总能耗"
            meters:
              direct: "METER-ELEC-L2-SURG + METER-CLG-L2-SURG"
              medical_gas: "METER-O2-L2-SURG + METER-VAC-L2-SURG"
              
          denominator:
            description: "手术台次"
            source: "HIS手术排程系统"
            
        unit: "kWh/台"
        
        target:
          typical_range: "200-400 kWh/台"
          depends_on: "手术类型、时长"
          
      - kpi_id: "KPI-OR-002"
        name: "手术室环境恢复时间"
        name_en: "OR Environment Recovery Time"
        
        accreditation_reference:
          clause: "2.3.5.3"
          requirement: "手术室周转效率"
          
        calculation:
          description: "从手术结束到环境参数恢复达标的时间"
          data_source: "Agent-06控制系统日志"
          
        unit: "分钟"
        target: "< 20分钟"
        
      - kpi_id: "KPI-OR-003"
        name: "手术室压差达标率"
        name_en: "OR Pressure Differential Compliance Rate"
        
        accreditation_reference:
          clause: "2.3.5.2"
          requirement: "洁净手术室压差梯度监测"
          
        calculation:
          formula: "CR = T(ΔP≥要求) / T_total × 100%"
          
          requirements:
            class_I_OR: "≥ 8 Pa"
            class_II_OR: "≥ 5 Pa"
            class_III_OR: "≥ 5 Pa"
            
        unit: "%"
        target: "> 99.9%"
        
    # 透析中心指标
    dialysis_kpis:
      
      - kpi_id: "KPI-DIAL-001"
        name: "单次透析能耗"
        name_en: "Energy Consumption per Dialysis Session"
        
        accreditation_reference:
          clause: "2.3.6"
          requirement: "透析中心运营效率监测"
          
        calculation:
          formula: "KPI = E_dialysis_total / N_sessions"
          
          numerator:
            description: "透析中心总能耗"
            meters:
              - "METER-ELEC-L2-DIAL"
              - "METER-WATER-L2-DIAL"
              
          denominator:
            description: "透析人次"
            source: "透析管理系统"
            
        unit: "kWh/人次"
        
        target:
          typical: "15-25 kWh/人次"
          
      - kpi_id: "KPI-DIAL-002"
        name: "透析用水效率"
        name_en: "Dialysis Water Efficiency"
        
        calculation:
          formula: "KPI = V_water / N_sessions"
          
        unit: "L/人次"
        target: "< 500 L/人次"
        
  # ─────────────────────────────────────────────────────────────────────────────
  # 4.3 大型设备利用率指标 (Major Equipment Utilization KPIs)
  # ─────────────────────────────────────────────────────────────────────────────
  
  major_equipment_kpis:
    
    description: |
      利用Agent-06的设备状态数据，识别大型医用设备的
      "待机"与"扫描"状态，计算真实利用率
      
    accreditation_reference:
      standard: "《三级医院评审标准（2025年版）》"
      chapter: "第三章"
      section: "第一节 大型设备管理与利用"
      clause: "3.1.2"
      requirement: "大型医用设备开机利用率应达到规定标准"
      
    # CT利用率
    ct_utilization:
      
      - kpi_id: "KPI-CT-001"
        name: "CT开机率"
        name_en: "CT Power-On Rate"
        
        calculation:
          formula: "KPI = T_power_on / T_available × 100%"
          
          numerator:
            description: "设备开机时间"
            data_source: "Agent-06.DI_CT1_POWER_ON"
            calculation: "累计DI=1的时间"
            
          denominator:
            description: "可用工作时间"
            value: "8:00-22:00, 工作日"
            hours_per_day: 14
            
        unit: "%"
        target: "> 85%"
        
      - kpi_id: "KPI-CT-002"
        name: "CT扫描利用率"
        name_en: "CT Scanning Utilization Rate"
        
        calculation:
          formula: "KPI = T_scanning / T_power_on × 100%"
          
          numerator:
            description: "实际扫描时间"
            data_source: "Agent-06.DI_CT1_SCANNING"
            
          denominator:
            description: "开机时间"
            
        unit: "%"
        target: "> 60%"
        
        analysis:
          low_utilization_causes:
            - "患者准备时间长"
            - "报告等待"
            - "设备故障"
            - "排程不合理"
            
      - kpi_id: "KPI-CT-003"
        name: "CT单次检查能耗"
        name_en: "Energy per CT Scan"
        
        calculation:
          formula: "KPI = E_CT / N_scans"
          
          numerator:
            description: "CT总电耗"
            meter: "VMETER-ELEC-CT-001"
            
          denominator:
            description: "检查人次"
            source: "PACS/RIS系统"
            
        unit: "kWh/次"
        target: "< 3 kWh/次"
        
    # MRI利用率
    mri_utilization:
      
      - kpi_id: "KPI-MRI-001"
        name: "MRI开机率"
        name_en: "MRI Power-On Rate"
        
        calculation:
          formula: "KPI = T_power_on / T_available × 100%"
          
        unit: "%"
        target: "> 90%"
        note: "MRI通常保持长时间开机（冷却需要）"
        
      - kpi_id: "KPI-MRI-002"
        name: "MRI扫描利用率"
        name_en: "MRI Scanning Utilization Rate"
        
        calculation:
          formula: "KPI = T_scanning / T_available × 100%"
          
        unit: "%"
        target: "> 50%"
        
      - kpi_id: "KPI-MRI-003"
        name: "MRI待机能耗占比"
        name_en: "MRI Standby Energy Ratio"
        
        calculation:
          formula: "KPI = E_standby / E_total × 100%"
          
          purpose: "监测MRI待机能耗，推动节能调度"
          
        unit: "%"
        benchmark: "典型值30-40%"
        
    # DSA利用率
    dsa_utilization:
      
      - kpi_id: "KPI-DSA-001"
        name: "DSA开机利用率"
        
        target: "> 70%"
        
  # ─────────────────────────────────────────────────────────────────────────────
  # 4.4 KPI仪表盘配置 (KPI Dashboard Configuration)
  # ─────────────────────────────────────────────────────────────────────────────
  
  kpi_dashboard:
    
    executive_dashboard:
      name: "院领导能效驾驶舱"
      refresh_rate: "每日"
      
      tiles:
        - tile: "全院能耗趋势"
          kpis: ["KPI-EFF-001", "KPI-EFF-002", "KPI-EFF-003"]
          chart_type: "趋势折线图"
          
        - tile: "科室能耗排名"
          data: "科室月度能耗排名"
          chart_type: "柱状图"
          
        - tile: "评审指标达标率"
          kpis: "所有评审相关KPI"
          chart_type: "仪表盘"
          
        - tile: "异常告警"
          data: "能耗异常事件"
          chart_type: "列表"
          
    department_dashboard:
      name: "科室能效看板"
      
      tiles:
        - tile: "科室本月能耗"
          breakdown: "电/冷/水/气"
          
        - tile: "业务指标"
          kpis: "单床日/单人次能耗"
          
        - tile: "环境达标率"
          kpis: "温湿度/压差达标"
          
        - tile: "同比环比"
          comparison: "vs上月/vs去年同期"
          
    equipment_dashboard:
      name: "大型设备效能看板"
      
      tiles:
        - tile: "设备开机状态"
          data: "实时状态"
          
        - tile: "利用率统计"
          kpis: ["KPI-CT-001", "KPI-MRI-001", "KPI-DSA-001"]
          
        - tile: "能耗分析"
          breakdown: "待机/扫描"
```

---

## 第五部分：数据可信与证据链构建 (Trust & Evidence Layer)

```yaml
# ═══════════════════════════════════════════════════════════════════════════════
# Phase 5: 数据可信与证据链构建
# 确保数据可追溯，经得起评审专家的现场核查
# ═══════════════════════════════════════════════════════════════════════════════

Data_Trust_Evidence_Model:
  
  meta:
    phase: "Phase 5"
    description: "构建数据质量保障和合规证据体系"
    
  # ─────────────────────────────────────────────────────────────────────────────
  # 5.1 数据清洗规则 (Data Cleansing Rules)
  # ─────────────────────────────────────────────────────────────────────────────
  
  data_cleansing_rules:
    
    principle: |
      确保进入分析的数据真实可靠，
      异常数据需标记处理而非简单丢弃
      
    # 异常值过滤
    outlier_filtering:
      
      - rule_id: "CLEAN-001"
        name: "零值异常过滤"
        description: "识别非正常的零值读数"
        
        conditions:
          - "连续零值超过设定时间"
          - "零值期间设备显示运行状态"
          
        time_thresholds:
          electrical_meter: "15分钟"
          thermal_meter: "30分钟"
          water_meter: "60分钟"
          
        actions:
          - action: "标记为'传感器故障'"
          - action: "触发设备诊断工单"
          - action: "启用备用计量方式"
          
      - rule_id: "CLEAN-002"
        name: "极值异常过滤"
        description: "识别超出物理可能范围的读数"
        
        rules:
          temperature:
            chilled_water: "2-15°C"
            cooling_water: "20-45°C"
            room_temp: "15-35°C"
            action_if_out: "使用上一有效值"
            
          pressure:
            chilled_water: "0.1-1.0 MPa"
            medical_gas: "0.3-0.6 MPa"
            
          power:
            rule: "不超过额定功率的120%"
            action_if_out: "标记为'可疑'"
            
      - rule_id: "CLEAN-003"
        name: "跳变异常过滤"
        description: "识别不合理的突变"
        
        rules:
          energy_meter:
            max_hourly_change: "200% of average"
            action: "二次确认或人工审核"
            
          flow_meter:
            max_change_per_minute: "50%"
            
    # 停电检修期间数据处理
    outage_handling:
      
      - rule_id: "CLEAN-004"
        name: "计划停电数据标记"
        description: "计划停电期间的数据处理"
        
        trigger:
          source: "运维工单系统"
          event_type: "PLANNED_OUTAGE"
          
        actions:
          - "标记受影响计量点"
          - "数据标签: PLANNED_OUTAGE"
          - "该时段数据不计入能效计算"
          
      - rule_id: "CLEAN-005"
        name: "非计划停电数据处理"
        description: "意外停电的数据处理"
        
        trigger:
          source: "Agent-06告警系统"
          event_type: "POWER_FAILURE"
          
        actions:
          - "记录停电时间段"
          - "恢复后检查计量表"
          - "必要时进行数据修正"
          
  # ─────────────────────────────────────────────────────────────────────────────
  # 5.2 断点补全策略 (Data Interpolation Strategy)
  # ─────────────────────────────────────────────────────────────────────────────
  
  data_interpolation:
    
    principle: |
      当Agent-06数据中断时，使用合理的插值算法补全，
      并明确标注"估算数据"标签
      
    strategies:
      
      - strategy_id: "INTERP-001"
        name: "短期中断线性插值"
        applicable: "中断时间 < 30分钟"
        
        algorithm: "LINEAR"
        formula: "V(t) = V(t1) + (V(t2) - V(t1)) × (t - t1) / (t2 - t1)"
        
        data_label: "INTERPOLATED_LINEAR"
        confidence: "HIGH"
        
      - strategy_id: "INTERP-002"
        name: "中期中断历史同期替代"
        applicable: "中断时间 30分钟 - 4小时"
        
        algorithm: "HISTORICAL_SAME_PERIOD"
        source: "上周同一时段数据"
        
        data_label: "INTERPOLATED_HISTORICAL"
        confidence: "MEDIUM"
        
      - strategy_id: "INTERP-003"
        name: "长期中断平均值替代"
        applicable: "中断时间 > 4小时"
        
        algorithm: "ROLLING_AVERAGE"
        window: "过去7天同类工况平均"
        
        data_label: "ESTIMATED_AVERAGE"
        confidence: "LOW"
        
        additional_action:
          - "生成数据质量告警"
          - "人工审核后才能用于计费"
          
    labeling:
      data_source_labels:
        MEASURED: "实测数据"
        INTERPOLATED_LINEAR: "线性插值"
        INTERPOLATED_HISTORICAL: "历史替代"
        ESTIMATED_AVERAGE: "平均估算"
        VIRTUAL_CALCULATED: "虚拟计算"
        MANUAL_ENTRY: "人工录入"
        
      audit_requirements:
        MEASURED: "无需审核"
        INTERPOLATED_LINEAR: "自动记录"
        INTERPOLATED_HISTORICAL: "周报汇总"
        ESTIMATED_AVERAGE: "需人工确认"
        MANUAL_ENTRY: "双人确认"
        
  # ─────────────────────────────────────────────────────────────────────────────
  # 5.3 合规证据快照 (Compliance Evidence Snapshot)
  # ─────────────────────────────────────────────────────────────────────────────
  
  compliance_evidence:
    
    description: |
      为评审提供可验证的数字化证据，
      支持依法执业的合规证明
      
    # 环境达标率证据
    environmental_compliance:
      
      - evidence_id: "EVID-ENV-001"
        name: "手术室环境达标率证据包"
        
        accreditation_reference:
          standard: "《三级医院评审标准（2025年版）》"
          clause: "2.3.5.2"
          requirement: "洁净手术室环境参数应持续达标"
          
        parameters:
          - parameter: "温度"
            requirement: "22-25°C"
            tolerance: "±1°C"
            
          - parameter: "相对湿度"
            requirement: "40-60%RH"
            tolerance: "±5%RH"
            
          - parameter: "压差"
            requirement:
              class_I: "≥ 8 Pa (对走廊)"
              class_II: "≥ 5 Pa"
              cascade: "正压梯度"
              
          - parameter: "换气次数"
            requirement:
              class_I: "≥ 36次/h"
              class_II: "≥ 24次/h"
              
        calculation:
          formula: |
            Compliance_Rate = Σ(Time_in_range) / Σ(Total_monitoring_time) × 100%
            
          data_source: "Agent-06.AI_ROOM_TEMP/HUMID/PRESS"
          sampling_interval: "1分钟"
          
        report_generation:
          frequency: "每日自动生成"
          format: "PDF + Excel"
          content:
            - "当日达标率统计"
            - "不达标时段明细"
            - "原因分析"
            - "趋势图表"
            
        evidence_retention: "10年"
        
      - evidence_id: "EVID-ENV-002"
        name: "ICU环境达标率证据包"
        
        parameters:
          - parameter: "温度"
            requirement: "22-26°C"
          - parameter: "相对湿度"
            requirement: "40-60%RH"
          - parameter: "压差"
            requirement: "正压 ≥ 5Pa"
            
      - evidence_id: "EVID-ENV-003"
        name: "负压隔离病房达标率证据包"
        
        parameters:
          - parameter: "压差"
            requirement: "负压 ≤ -5Pa (对走廊)"
          - parameter: "换气次数"
            requirement: "≥ 12次/h"
            
    # 设备运行证据
    equipment_operation_evidence:
      
      - evidence_id: "EVID-EQP-001"
        name: "大型设备运行日志"
        
        content:
          - "每日开关机时间"
          - "扫描/检查记录"
          - "故障停机时间"
          - "利用率计算"
          
        data_source:
          - "Agent-06.DI_xxx_POWER_ON"
          - "Agent-06.DI_xxx_SCANNING"
          - "PACS/RIS检查记录"
          
      - evidence_id: "EVID-EQP-002"
        name: "关键设备告警记录"
        
        content:
          - "告警时间"
          - "告警等级"
          - "响应时间"
          - "处理结果"
          
    # 能耗数据证据
    energy_data_evidence:
      
      - evidence_id: "EVID-ENERGY-001"
        name: "能耗数据完整性报告"
        
        content:
          - "数据采集完整率"
          - "数据质量分析"
          - "异常处理记录"
          - "插值/估算标记"
          
        quality_metrics:
          data_completeness: "> 99.5%"
          data_accuracy: "Class A/B表 > 99%"
          
      - evidence_id: "EVID-ENERGY-002"
        name: "能源审计证据包"
        
        content:
          - "月度能耗报表"
          - "同比环比分析"
          - "节能措施记录"
          - "效果验证"
          
  # ─────────────────────────────────────────────────────────────────────────────
  # 5.4 数据血缘追溯 (Data Lineage Tracing)
  # ─────────────────────────────────────────────────────────────────────────────
  
  data_lineage:
    
    principle: |
      任何一个KPI指标都能追溯到原始计量数据，
      形成完整的证据链
      
    lineage_model:
      
      example_kpi: "KPI-EFF-002 (每住院床日能耗)"
      
      trace_path:
        
        level_1_kpi:
          id: "KPI-EFF-002"
          formula: "E_inpatient / BD_total"
          
        level_2_aggregation:
          numerator:
            calculation: "Σ(各楼层能耗)"
            components:
              - "METER-ELEC-L2-WARD"
              - "METER-CLG-L2-WARD"
              - "分摊能耗"
          denominator:
            source: "HIS.GetBedDays()"
            
        level_3_allocation:
          chiller_allocation:
            rule: "RULE-ALLOC-001"
            source: "METER-ELEC-L2-CHP"
            basis: "METER-CLG-L2-WARD / METER-CLG-L1-001"
            
        level_4_physical_meter:
          meters:
            - id: "METER-ELEC-L2-WARD"
              type: "PHYSICAL"
              accuracy: "1.0级"
              last_calibration: "2024-06-15"
              
        level_5_raw_data:
          data_points:
            - point_id: "Agent-06.AI_ENERGY_WARD"
              timestamp: "2024-07-01 00:00:00"
              value: 125000
              unit: "kWh"
              source_label: "MEASURED"
              
    audit_query:
      description: "支持任意时点数据的溯源查询"
      api: "DataLineage.Trace(kpi_id, timestamp)"
      output:
        - "原始读数"
        - "数据来源"
        - "处理步骤"
        - "计算公式"
        - "责任人"
```

---

## 第六部分：系统集成与接口 (System Integration & Interfaces)

```yaml
# ═══════════════════════════════════════════════════════════════════════════════
# Part 6: 系统集成与接口
# 定义计量体系与外部系统的数据交互
# ═══════════════════════════════════════════════════════════════════════════════

System_Integration:
  
  # ─────────────────────────────────────────────────────────────────────────────
  # 6.1 上游数据接口 (Upstream Data Interfaces)
  # ─────────────────────────────────────────────────────────────────────────────
  
  upstream_interfaces:
    
    # BMS/BA系统接口
    bms_interface:
      protocol: "BACnet/IP, Modbus TCP, OPC UA"
      data_types:
        - "AI: 电能、冷量、流量、温度、压力"
        - "DI: 设备运行状态"
      frequency: "1分钟采集"
      
    # 电力监控系统接口
    power_monitoring:
      protocol: "Modbus TCP, IEC 61850"
      data_types:
        - "电能累计值"
        - "功率因数"
        - "三相电压电流"
      frequency: "实时"
      
    # HIS接口
    his_interface:
      protocol: "HL7 FHIR, Web Service"
      data_types:
        - "门诊人次"
        - "住院床日"
        - "手术台次"
        - "检查人次"
      frequency: "每日同步"
      
  # ─────────────────────────────────────────────────────────────────────────────
  # 6.2 下游输出接口 (Downstream Output Interfaces)
  # ─────────────────────────────────────────────────────────────────────────────
  
  downstream_interfaces:
    
    # 财务系统接口
    finance_interface:
      data_output:
        - "科室能耗账单"
        - "分摊明细"
      format: "Excel, API"
      frequency: "月度"
      
    # 运维系统接口
    omis_interface:
      data_output:
        - "设备能效异常告警"
        - "预测性维护信号"
      format: "JSON/MQTT"
      frequency: "实时"
      
    # 评审数据接口
    accreditation_interface:
      data_output:
        - "KPI指标报表"
        - "达标率证明"
        - "证据快照"
      format: "PDF, Excel"
      frequency: "按需生成"
```

---

## 第七部分：交付物汇总 (Deliverables Summary)

```yaml
# ═══════════════════════════════════════════════════════════════════════════════
# Agent-07 交付物汇总
# ═══════════════════════════════════════════════════════════════════════════════

Agent07_Deliverables_Summary:
  
  meta:
    version: "2.1"
    total_parts: 7
    accreditation_aligned: true
    
  deliverable_inventory:
    
    part_1_physical_metering:
      content:
        - "4级计量层级定义"
        - "189个物理计量点"
        - "能量守恒校验规则"
      key_outputs:
        - "电力计量网络 (78点)"
        - "冷热量计量网络 (42点)"
        - "水资源计量网络 (35点)"
        - "医用气体计量网络 (28点)"
        
    part_2_virtual_metering:
      content:
        - "精度分级体系 (A/B/C/D)"
        - "520个虚拟计量点"
        - "物理方程应用"
      key_outputs:
        - "FCU冷量虚拟表 (230+)"
        - "AHU冷量虚拟表 (50+)"
        - "设备电量虚拟表 (100+)"
        - "空间能耗虚拟表 (140+)"
        
    part_3_financial_allocation:
      content:
        - "科室-计量映射"
        - "5类分摊算法"
        - "24条分摊规则"
      key_outputs:
        - "冷站公摊算法"
        - "加权面积算法"
        - "时间分摊算法"
        - "科室能耗账单模板"
        
    part_4_performance_kpis:
      content:
        - "35个KPI指标"
        - "12条评审条款对应"
      key_outputs:
        - "资源效率指标 (5个)"
        - "ICU指标 (2个)"
        - "手术室指标 (3个)"
        - "透析中心指标 (2个)"
        - "大型设备利用率指标 (8个)"
        
    part_5_data_trust:
      content:
        - "数据清洗规则"
        - "断点补全策略"
        - "合规证据快照"
        - "数据血缘追溯"
      key_outputs:
        - "5条清洗规则"
        - "3类插值策略"
        - "环境达标率证据包"
        - "数据溯源模型"
        
    part_6_integration:
      content:
        - "上下游接口定义"
      key_outputs:
        - "BMS/HIS/财务接口"
        
  cross_references:
    
    to_agent_01:
      - "系统拓扑结构 → 计量父子关系"
      - "节点ID引用"
      
    to_agent_02:
      - "Org_ID → 成本中心"
      - "Space_Type → 加权系数"
      - "床位数/面积 → 分摊分母"
      
    to_agent_03:
      - "设备额定功率 → 虚拟计量"
      - "计量设备类型"
      
    to_agent_04:
      - "Q=ρVCpΔT → 冷量虚拟计量"
      - "载体荷载方程 → 能量计算"
      
    to_agent_05:
      - "Coupling_Unit → 服务边界"
      - "末端-空间关系 → 分摊"
      
    to_agent_06:
      - "AI_ENERGY → 物理计量数据源"
      - "AI_FLOW → 流量数据"
      - "DI_RUN → 运行时间计算"
      
  accreditation_coverage:
    
    standard: "《三级医院评审标准（2025年版）》"
    
    covered_clauses:
      - clause: "1.2.3 资源效率监测"
        kpis: ["KPI-EFF-001", "KPI-EFF-002", "KPI-EFF-003", "KPI-EFF-004"]
        
      - clause: "2.3.4 ICU资源效率"
        kpis: ["KPI-ICU-001", "KPI-ICU-002"]
        
      - clause: "2.3.5 手术室管理"
        kpis: ["KPI-OR-001", "KPI-OR-002", "KPI-OR-003"]
        
      - clause: "2.3.6 透析中心"
        kpis: ["KPI-DIAL-001", "KPI-DIAL-002"]
        
      - clause: "3.1.2 大型设备利用率"
        kpis: ["KPI-CT-001", "KPI-CT-002", "KPI-MRI-001", "KPI-DSA-001"]
        
  implementation_guidance:
    
    phase_1_foundation:
      duration: "2个月"
      activities:
        - "物理计量表安装确认"
        - "BMS数据接口对接"
        - "基础数据采集"
        
    phase_2_virtual:
      duration: "3个月"
      activities:
        - "虚拟计量算法实现"
        - "精度验证与标定"
        - "守恒校验上线"
        
    phase_3_allocation:
      duration: "2个月"
      activities:
        - "分摊规则配置"
        - "科室账单生成"
        - "财务系统对接"
        
    phase_4_kpi:
      duration: "2个月"
      activities:
        - "KPI指标开发"
        - "仪表盘上线"
        - "评审证据包生成"
        
  validation_checklist:
    
    data_quality:
      - "物理计量点采集完整率 > 99.5%"
      - "虚拟计量精度验证通过"
      - "守恒校验偏差 < 5%"
      
    functional:
      - "科室账单可按时生成"
      - "KPI指标计算正确"
      - "证据快照可追溯"
      
    accreditation:
      - "所有评审条款有数据支撑"
      - "达标率可自动计算"
      - "证据包可一键导出"
```

---

**Agent-07 计量体系建模师 - 医疗建筑全域计量与绩效评价体系模型 v2.1 完成**

本模型构建了"物理-虚拟-价值"三位一体的计量体系：

1. **物理层**：189个物理计量点，4级层级结构，能量守恒校验
2. **虚拟层**：520个虚拟计量点，基于Agent-04物理方程，精度分级(A/B/C/D)
3. **价值层**：24条分摊规则，35个KPI指标，12条评审条款对应

直接响应《三级医院评审标准（2025年版）》的资源效率、重点科室监测、大型设备利用率等要求，形成可追溯的数字化证据链。
[^1]: [# Agent-03: 设备本体建模师 (Equ...体化建模

[^2]: [Agent01_Output.project_summary.md](http://file/857edf8d-27c4-46a4-9be6-49c7310e56fc.md)

[^3]: [Agent03_Output.project_summary.md](http://file/fa4943df-69fe-440d-9d09-f824be4349ec.md)

[^4]: [Agent-02  空间本体建模师 (Space Ontology Architect).md](http://file/35de1547-3b35-4ab4-a98a-37fb6cf0b0b6.md)

[^5]: [Agent-03 v2.2  设备本体建模师 (Equipment Ontology Architect) 完整输出.md](http://file/6c1c1929-d310-442c-8bd3-24228af83d28.md)

[^6]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^1]: [# Agent-04 流动模型建模输出文件

[^2]: [# === AGENT-09: 统一CIM模型 ...on: “医用床塔管道疋 - 吊臂式供气供电+](# === AGENT-09: 统一CIM模型 ...on: “医用床塔管道疋 - 吊臂式供气供电+)

[^3]: [# === AGENT-09: 统一CIM模型 ...on: “医用床塔管道疋 - 吊臂式供气供电+](# === AGENT-09: 统一CIM模型 ...on: “医用床塔管道疋 - 吊臂式供气供电+)

[^4]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^5]: [Agent-04 流动模型建模师.md](http://file/3094e4ad-51ff-454c-9b4b-08c31b4417c0.md)

[^6]: [Agent-06 控制系统建模师 - 全域控制系统实现模型.md](http://file/5a6e11cb-9f76-4857-ac58-500ed17fad40.md)

[^1]: [# 运维管理模型 - 综合交付物总结

# Ag...筑的智能运维提供强有力的技术支撑和管理规范。"](# 运维管理模型 - 综合交付物总结

# Ag...筑的智能运维提供强有力的技术支撑和管理规范。")

[^2]: [# 维护策略模型 - 医疗建筑智能运维管理

#..._verification: "连续验证确认"](# 维护策略模型 - 医疗建筑智能运维管理

#..._verification: "连续验证确认")

[^3]: [Agent-01 系统拓扑建模师 - 完整输出文档.md](http://file/fb792853-9410-4a6d-9389-5740af5b6fee.md)

[^4]: [医疗建筑能源管理平台（修订版 v3.0）.md](http://file/662d8d43-0edf-43b6-a3b8-288c6d5818db.md)

[^5]: [Agent-01 系统拓扑建模师 - 第六批次：最终系统与综合集成.md](http://file/8b4c44db-7e14-4e27-9c8a-35285cf290c0.md)

[^6]: [# Agent-05和Agent-07输出文件重..."

[^1]: [Agent-02  空间本体建模师 (Space Ontology Architect).md](http://file/35de1547-3b35-4ab4-a98a-37fb6cf0b0b6.md)

[^2]: [# Agent-05和Agent-07输出文件重..."

[^3]: [Agent-05 系统-空间耦合建模师.md](http://file/3eb5303c-77a6-4bf1-aa23-5d864256776c.md)

[^4]: [# Agent-07: 计量体系建模师 - 元数...筑能耗远程监测系统技术规程》"

[^5]: [# === AGENT-09: 统一CIM模型 ...on: “医用床塔管道疋 - 吊臂式供气供电+](# === AGENT-09: 统一CIM模型 ...on: “医用床塔管道疋 - 吊臂式供气供电+)

[^6]: [# Agent-05和Agent-07输出文件重..."

[^1]: [# === AGENT-09: 统一CIM模型 ...on: “医用床塔管道疋 - 吊臂式供气供电+](# === AGENT-09: 统一CIM模型 ...on: “医用床塔管道疋 - 吊臂式供气供电+)

[^2]: [Agent-06 控制系统建模师 - 全域控制系统实现模型.md](http://file/5a6e11cb-9f76-4857-ac58-500ed17fad40.md)

[^3]: [Agent-06 控制系统建模师 - 全域控制系统实现模型.md](http://file/5a6e11cb-9f76-4857-ac58-500ed17fad40.md)

[^4]: [Agent-01 系统拓扑建模师 - 第二批次：电气系统 + 医疗气体系 （第三次修订版）.md](http://file/4cd17d72-bd32-43f9-a072-b383fd70c5fc.md)

[^5]: [# Agent-05和Agent-07输出文件重..."

[^6]: [# Agent-06 控制系统建模师 输出文件元...ion: "基于工程实际运行参数进行模型验证"](# Agent-06 控制系统建模师 输出文件元...ion: "基于工程实际运行参数进行模型验证")

[^1]: [AGENT-05 V2.1-RELEASE 最终发布文档.md](http://file/1b6473f6-fd9c-4a20-babe-cafb56b0d6e8.md)

[^2]: [# Agent-04 流动模型建模输出文件

[^3]: [Agent-04 流动模型建模师 完整输出文档 V2.3版.md](http://file/05b8fc3a-a8c7-44d4-a15c-91ce05fa76bc.md)

[^4]: [AGENT-05 V2.1-RELEASE 最终发布文档.md](http://file/1b6473f6-fd9c-4a20-babe-cafb56b0d6e8.md)

[^5]: [Agent-06 控制系统建模师 - 全域控制系统实现模型.md](http://file/5a6e11cb-9f76-4857-ac58-500ed17fad40.md)

[^6]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)
---