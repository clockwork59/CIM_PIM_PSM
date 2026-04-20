# 医疗建筑技术系统拓扑模型集合

## HVAC-CHP 冷源系统节点-边拓扑模型

```yaml
system_info:
  system_id: "HVAC-CHP"
  system_name: "医疗建筑冷源系统"
  category: "HVAC"
  description: "医疗建筑中央制冷系统的拓扑结构模型"
  modeling_date: "2025-12-02"
  model_version: "v1.0"

system_boundary:
  input_boundary:
    electrical_power:
      interface: "35kV/10kV 高压配电"
      voltage_levels: ["10kV", "380V", "220V"]
      reliability_level: "一级负荷"
      backup_requirement: "柴油发电机组 + UPS"
      dependency: "ELECTRICAL-HV/S-EPS"
      measurement_point: "主开关柜进线"

    cooling_water_media:
      interface: "市政供水"
      pressure_range: "0.15-0.35 MPa"
      quality_requirement: "符合冷却后补水要求"
      backup_source: "自备水井或水箱"
      dependency: "PLUMBING-WSS"
      measurement_point: "冷却塔补水总管"

    external_environment:
      dry_bulb_temp: "35°C (夏季设计)"
      wet_bulb_temp: "28.2°C (夏季设计)"
      altitude: "按项目实际高度"
      seismic_zone: "按国家标准设防"
      wind_load: "按荷载规范"

  output_boundary:
    chilled_water_supply:
      supply_temp: "7°C"
      return_temp: "12°C"
      delta_t: "5°C"
      pressure_range: "0.2-0.8 MPa"
      flow_rate_available: "按设计负荷计算"
      quality: "闭式系统，防腐蚀处理"
      service_scope: "全建筑空调末端"
      measurement_point: "分水器各回路"

    cooling_tower_exhaust:
      air_flow_rate: "冷却塔设计风量"
      exit_vapor: "饱和湿空气排放"
      noise_level: "≤65dB(A) (边界噪声)"
      drift_loss: "≤0.005%循环水量"
      ambient_impact: "水雾、噪声、冷却塔军团菌防控"

    heat_rejection_to_atmosphere:
      heat_rejection_rate: "总排热量"
      coolant: "冷却水循环系统"
      environmental_impact: "城市热岛效应贡献"

    control_and_status_signals:
      BAS_interface: "MODBUS/BACnet协议"
      EMS_interface: "能源数据上传"
      data_points: "温度、压力、流量、功率、状态"
      network_requirement: "工业以太网"

  control_boundary:
    automation_scope: "全自动运行 + 远程监控"
    local_control: "现场PLC控制柜 "
    manual_override: "本地手动操作权限"
    safety_interlocks: "设备连锁保护"
    energy_optimization: "负荷预测 + 最优设备组合"

# 节点定义 - 源节点部分
nodes:
  # 主要冷源生产设备 - 一级源节点
  source_nodes:
    - node_id: "CHP-SR-01"  # SR = Source
      node_name: "冷水机组源节点 #1"
      node_type: "SOURCE"
      node_subtype: "PRIMARY_REFRIGERATION"
      equipment: "离心式冷水机组 1000RT"
      manufacturer_type: "离心式压缩机"
      refrigerant_type: "R-134a"
      rated_capacity: "1000 RT (3517 kW)"
      input_power: "620 kW"
      cop_rated: "5.67"
      part_load_performance:
        - "75%: COP = 6.1"
        - "50%: COP = 6.8"
        - "25%: COP = 5.2"
      environmental_conditions:
        condenser_water_inlet: "32°C"
        condenser_water_outlet: "37°C"
        chilled_water_inlet: "12°C"
        chilled_water_outlet: "7°C"
      controls:
        - capacity_control: "VFD变频 + 进口导叶"
        - temperature_control: "精确温度控制±0.5°C"
        - safety_control: "高低压保护、低温保护"
        - monitoring: "24点监测"

    - node_id: "CHP-SR-02"
      node_name: "冷水机组源节点 #2"
      node_type: "SOURCE"
      node_subtype: "PRIMARY_REFRIGERATION"
      equipment: "螺杆式冷水机组 500RT"
      manufacturer_type: "螺杆式压缩机"
      refrigerant_type: "R-134a"
      rated_capacity: "500 RT (1758 kW)"
      input_power: "315 kW"
      cop_rated: "5.58"
      environmental_conditions:
        condenser_water_inlet: "32°C"
        condenser_water_outlet: "37°C"
        chilled_water_inlet: "12°C"
        chilled_water_outlet: "7°C"
      operational_note: "用于部分负荷运行或备用"

    - node_id: "CHP-SR-03"
      node_name: "吸收式冷热水机组源节点"
      node_type: "SOURCE"
      node_subtype: "ABSORPTION_REFRIGERATION"
      equipment: "双效吸收式冷热水机组 300RT"
      thermal_energy_source: "蒸汽或热水"
      heat_input: "2200 kW"
      cooling_capacity: "300 RT (1055 kW)"
      thermal_cop: "1.2"
      electrical_power: "15 kW"
      operational_pattern: "利用夏季蒸汽free cooling"

    - node_id: "CHP-SR-CT-01"
      node_name: "冷却塔源节点 #1"
      node_type: "SOURCE"
      node_subtype: "HEAT_REJECTION"
      equipment: "机械通风冷却塔 500RT 2台"
      cooling_capacity_per_unit: "250 RT (879 kW)"
      water_flow_rate: "240 m³/h per unit"
      fan_power: "11 kW x 2"
      approach_temperature: "4-5°C"
      drift_rate: "≤0.005% circulating water"
      noise_level: "≤72dB(A) at 10m"
      water_treatment: "化学水处理 + 旁流水处理"
      plume_abatement: "消雾型冷却塔"

    - node_id: "CHP-SR-CT-02"
      node_name: "冷却塔源节点 #2"
      node_type: "SOURCE"
      node_subtype: "HEAT_REJECTION"
      equipment: "机械通风冷却塔 750RT 2台"
      cooling_capacity_per_unit: "375 RT (1318 kW)"
      water_flow_rate: "360 m³/h per unit"
      fan_power: "15 kW x 2"
      approach_temperature: "4-5°C"
      operational_pattern: "配合1000RT主机运行"

  # 分配节点 - 冷热水输配系统
  distribution_nodes:
    - node_id: "CHP-DIST-CHW-01"
      node_name: "冷冻水分水器主节点"
      node_type: "DISTRIBUTION"
      node_subtype: "CHILLED_WATER_DISTRIBUTION"
      equipment: "主冷冻水分水器 Φ1200mm"
      distribution_capacity: "5000 m³/h design"
      operating_pressure: "0.6 MPa"
      branches:
        - "门诊院区分配"
        - "住院院区分配"
        - "手术中心区分配"
        - "医技院区分配"
        - "行政区分配"
      flow_balancing: "静态平衡阀 + 动态平衡阀"
      temperature_control: "供回水总管温度监测"
      pressure_control: "压差旁通控制"
      insulation: "50mm难燃型泡沫玻璃保温"

    - node_id: "CHP-DIST-CHW-02"
      node_name: "门诊院区冷冻水分配节点"
      node_type: "DISTRIBUTION"
      node_subtype: "CHILLED_WATER_SECONDARY_DIST"
      equipment: "门诊分水器 Φ800mm"
      distribution_capacity: "1200 m³/h"
      service_areas:
        - "门诊大厅"
        - "诊室区域"
        - "候诊区"
        - "收费挂号区"
        - "药房"
      control_strategy: "变流量 + ΔT优化"
      differential_pressure: "50-150 kPa"
      meterinstallation: "电磁流量计 + 超声波热量表"

    - node_id: "CHP-DIST-CHW-03"
      node_name: "手术中心区冷冻水分配节点"
      node_type: "DISTRIBUTION"
      node_subtype: "CRITICAL_COOLING_DISTRIBUTION"
      equipment: "手术区专用分水器 Φ600mm"
      distribution_capacity: "800 m³/h"
      service_areas:
        - "手术室层流净化空调"
        - "ICU洁净空调"
        - "洁净走廊"
        - "洁净物品传递"
      reliability_level: "N+1冗余配置"
      control_precision: "±1°C温度控制"
      backup_capacity: "满足50%负荷备份"
      emergency_isolation: "可分区快速关闭"
      isolation_time: "≤30秒"

    - node_id: "CHP-DIST-CDW-01"
      node_name: "冷却水集水器主节点"
      node_type: "DISTRIBUTION"
      node_subtype: "CONDENSER_WATER_DISTRIBUTION"
      equipment: "冷却水集水器 Φ1400mm"
      collection_capacity: "6000 m³/h design"
      circulating_pump_connection: "3x75kW + 1x75kW备用"
      operating_temperature:
        supply: "32°C"
        return: "37°C"
      pressure_range: "0.3-0.5 MPa"
      filtration: "Y型过滤器 + 自动排污过滤器"
      water_quality_monitoring: "在线电导率 + pH值监测"
      chemical_treatment: "加药装置 + 自动排污"

    - node_id: "CHP-DIST-CT-01"
      node_name: "冷却塔分配节点"
      node_type: "DISTRIBUTION"
      node_subtype: "COOLING_TOWER_WATER_DISTRIBUTION"
      equipment: "冷却塔布水器 + 集水盘"
      distribution_capacity: "水侧: 6000 m³/h"
      air_side: "风机: 52 kW total"
      temperature_control:
        basin_temperature: "32°C 目标"
        fan_control: "变频 + 启停"
        approach_temperature: "4-5°C"
      water_treatment:
        dosage: "阻垢 + 缓蚀 + 杀菌灭藻"
        dosing_system: "自动加药装置"
        bleed_off: "定期排污"
      plume_control: "消雾型填料 + 除雾器"
      noise_control: "超低噪音风机 + 消声器"

  # 汇节点 - 最终使用终端
  sink_nodes:
    - node_id: "CHP-SINK-AHU-01"
      node_name: "门诊主空气处理机组"
      node_type: "SINK"
      node_subtype: "HVAC_TERMINAL_UNIT"
      equipment: "组合式空调机组 80000 m³/h"
      cooling_coil:
        capacity: "500 kW"
        max_water_flow: "86 m³/h"
        enthalpy_difference: "25 kJ/kg"
      air_side:
        total_airflow: "80000 m³/h"
        outdoor_air: "25% (20000 m³/h)"
        return_air: "75% (60000 m³/h)"
        fan_power: "30 kW (送风机) + 22 kW (回风机)"
      thermal_zones_served:
        - "门诊大厅 (2000 m²)"
        - "挂号收费 (300 m²)"
        - "门诊药房 (200 m²)"
        - "候诊区 (800 m²)"
      thermal_loads:
        sensible_cooling: "400 kW"
        latent_cooling: "100 kW"
        heating: "200 kW (热水盘管)"
      control_strategy:
        # economizer: "焓差 + CO2浓度" # Some symbols not allowed in comment
        temperature_control: "送风温度设定点"
        vav_control: "变风量末端控制"
        filtration: "初效G4 + 中效F7 + 亚高效H10"

    - node_id: "CHP-SINK-OR-01"
      node_name: "手术室层流净化空调"
      node_type: "SINK"
      node_subtype: "CRITICAL_CLEANROOM_UNIT"
      equipment: "手术室专用净化空调机组"
      cleanliness_level: "ISO 5级 (百级)"
      airflow_pattern: "顶棚层流送风 + 周边回风"
      volumetric_flow:
        laminar_zone: "0.25 m/s 面速"
        total_airflow: "15000 m³/h"
        air_changes_per_hour: "25 ACH"
      cooling_load:
        total_cooling: "42 kW"
        sensible_cooling: "35 kW"
        latent_cooling: "7 kW"
      thermal_environment:
        temperature_range: "22-25°C ±1°C"
        relative_humidity: "45-60% ±5%"
        pressure_differential: "+15-+30 Pa"
      served_spaces:
        - "骨科手术室 (60 m²)"
        - "心脏手术室 (80 m²)"
        - "神经外科手术室 (70 m²)"
      reliability_features:
        redundancy: "双风机系统"
        backup_cooling: "50% 备用冷量"
        failure_response: "自动切换备用"
        alarm_system: "温湿度、压差、风量实时报警"

    - node_id: "CHP-SINK-ICU-01"
      node_name: "重症监护病房空调终端"
      node_type: "SINK"
      node_subtype: "ICU_CRITICAL_CARE_ZONE"
      equipment: "ICU洁净末端组 + 独立新排风"
      zone_configuration:
        bed_count: "12床位"
        area: "400 m²"
        cleanliness: "ISO 7级 (万级)"
      cooling_analysis:
        internal_gain: "人员 120W/床位 + 设备 1.5kW/床位"
        envelope_load: "围护结构 15 W/m²"
        total_peak_cooling: "65 kW"
      air_distribution:
        air_changes: "18 ACH"
        outdoor_air: "30 m³/h·人 (40人)"
        airflow_pattern: "上送下回，避免直接吹向病人"
        pressure_control: "正压 +5~+10 Pa"
      temperature_control:
        range: "24±2°C"
        response_time: "温度变化 ≤2°C/h"
        control_strategy: "全空气系统 + 变风量末端"
      humidity_control:
        range: "50±10%"
        dehumidification: "深度除湿至 8°C 露点"
        humidification: "蒸汽加湿，加湿量 60 kg/h"

    - node_id: "CHP-SINK-PHARMACY-01"
      node_name: "医院药房空调终端"
      node_type: "SINK"
      node_subtype: "PHARMACEUTICAL_STORAGE_ZONE"
      equipment: "精密空调 + 医药冷库 + 阴凉库"
      space_division:
        ambient_pharmacy: "常温区 (≤30°C)"
        cool_storage: "阴凉区 (≤20°C)"
        cold_storage: "冷藏区 (2-8°C)"
        frozen_storage: "冷冻区 (-20°C)"
      cooling_loads:
        ambient_zone: "85 kW"
        cool_zone: "12 kW"
        cold_zone: "8 kW"
        frozen_zone: "5 kW"
      temperature_specifications:
        stability: "±1°C"
        uniformity: "±2°C"
        gradient: "ΔT≤3°C"
      humidity_specifications:
        relative_humidity: "45-75%"
        precision: "±5%"
      backup_requirements:
        cooling: "N+1 配置"
        power: "柴油发电机秒级切换"
        monitoring: "7x24温度监控 + SMS报警"

# 边定义 - 连接关系和流动路径
edges:
  # 主要供冷径 - 冷源到分配器
  supply_trunk_edges:
    - edge_id: "CHP-EDGE-TRUNK-01"
      edge_name: "冷水机组#1 → 主分水器"
      edge_type: "TRUNK"
      connection:
        from_node: "CHP-SR-01"
        to_node: "CHP-DIST-CHW-01"
      medium: "冷冻水"
      flow_direction: "供回双向循环"
      design_flow_rate: "605 m³/h"
      pipe_specification:
        diameter: "D530mm x 8mm"
        material: "20#无缝钢管"
        insulation: "难燃型泡沫玻璃 60mm"
        pressure_rating: "PN16"
      operating_conditions:
        supply_temperature: "7°C"
        return_temperature: "12°C"
        pressure_range: "0.6 MPa"
        velocity: "1.0-1.5 m/s"
        pressure_loss: "≤150 kPa/km"
      isolation:
        valves: "闸阀 + 软连接 + 止回阀"
        bypass: "带旁通管"
        expansion_joint: "波纹补偿器"

    - edge_id: "CHP-EDGE-TRUNK-02"
      edge_name: "冷水机组#2 → 主分水器"
      edge_type: "TRUNK"
      connection:
        from_node: "CHP-SR-02"
        to_node: "CHP-DIST-CHW-01"
      medium: "冷冻水"
      flow_rate: "302 m³/h"
      pipe_specification:
        diameter: "D426mm x 7mm"
        material: "20#无缝钢管"
        insulation: "难燃型泡沫玻璃 60mm"

    - edge_id: "CHP-EDGE-TRUNK-03"
      edge_name: "主分水器 → 各分区分配管路"
      edge_type: "TRUNK"
      connection:
        from_node: "CHP-DIST-CHW-01"
        to_node: "CHP-DIST-CHW-02"
      branches:
        - "门诊区分支"
        - "手术中心区分支"
        - "住院区分支"
        - "医技区分支"
      total_flow: "5000 m³/h"
      distribution_rations:
        outpatient_zone: "24%"
        operation_center: "16%"
        inpatient_zone: "35%"
        medical_tech_zone: "20%"
        administration: "5%"

    - edge_id: "CHP-EDGE-TRUNK-04"
      edge_name: "冷却塔#1 ↔ 冷却水循环泵"
      edge_type: "TRUNK"
      connection:
        from_node: "CHP-SR-CT-01"
        to_node: "CHP-DIST-CDW-01"
      medium: "冷却水"
      flow_rate: "2400 m³/h"
      pipe_material: "镀锌钢管"
      insulation: "柔性泡沫塑料保温 25mm"
      pressure_rating: "PN10"

    - edge_id: "CHP-EDGE-TRUNK-05"
      edge_name: "冷却塔#2 ↔ 冷却水循环泵"
      edge_type: "TRUNK"
      connection:
        from_node: "CHP-SR-CT-02"
        to_node: "CHP-DIST-CDW-01"
      flow_rate: "3600 m³/h"
      pipe_specification:
        diameter: "D820mm x 10mm"
        material: "螺旋钢管"

  # 分支边 - 从分水器到各末端空调机组
  branch_edges:
    - edge_id: "CHP-EDGE-BRANCH-01"
      edge_name: "门诊区分水器 ←→ 门诊主空调机组"
      edge_type: "BRANCH"
      connection:
        from_node: "CHP-DIST-CHW-02"
        to_node: "CHP-SINK-AHU-01"
      medium: "冷冻水"
      flow_rate: "86 m³/h"
      pipe_specification:
        diameter: "D219mm x 6mm"
        material: "20#无缝钢管"
        insulation: "聚苯乙烯管壳 50mm"
      operating_conditions:
        supply_temp: "7°C"
        return_temp: "12°C"
        design_pressure: "0.5 MPa"
      control_interface:
        - "二通调节阀 DN125"
        - "压差旁通阀 DN100"
        - "区域电动蝶阀 DN150"
      measurement:
        - "磁感应流量计"
        - "温度传感器 PT100"
        - "压力表"

    - edge_id: "CHP-EDGE-BRANCH-02"
      edge_name: "手术中心区专用冷却水分配"
      edge_type: "BRANCH"
      connection:
        from_node: "CHP-DIST-CHW-03"
        to_node: "CHP-SINK-OR-01"
      medium: "冷冻水"
      flow_rate: "35 m³/h"
      pipe_specification:
        diameter: "D159mm x 5mm"
        material: "304不锈钢"
        insulation: "阻燃橡塑保温 40mm"
      special_requirements:
        - "双层管道(泄漏监测)"
        - "分区快速隔离阀"
        - "应急旁通"
        - "压差自动控制"

    - edge_id: "CHP-EDGE-BRANCH-03"
      edge_name: "ICU区冷冻水分支"
      edge_type: "BRANCH"
      connection:
        from_node: "CHP-DIST-CHW-03"
        to_node: "CHP-SINK-ICU-01"
      flow_rate: "42 m³/h"
      pipe_diameter: "D194mm x 6mm"
      control_devices:
        - "VAV末端控制" ["Variable Air Volume control"]
        - "分区压差控制"
        - "应急快速关断"
      reliability_level: "医疗级可靠性"
      backup: "50% 冗余流量预留"

  # 终端边 - 供回水连接到各用电末端区域
  terminal_edges:
    - edge_id: "CHP-EDGE-TERM-01"
      edge_name: "冷却塔循环泵电气连接线"
      edge_type: "TERMINAL"
      connection:
        from_node: "CHP-DIST-CDW-01"
        to_node: "" # 电气系统接口
      power_type: "电动机动力"
      motor_power: "75 kW x 4 = 300 kW"
      electrical_specification:
        voltage: "380V/3P/50Hz"
        current: "158A (每电机)"
        starting_method: "VFD 软启动"
        power_factor: "≥0.85"
      control_interface:
        - "VFD变频器"
        - "就地/远程启动"
        - "功率、电流、状态信号"
        - "故障报警"

    - edge_id: "CHP-EDGE-TERM-02"
      edge_name: "冷水机组自控电气信号"
      edge_type: "TERMINAL"
      connection:
        from_node: "CHP-SR-01"
        to_node: ""  # BAS控制器接口
      signal_types:
        - "AI: 温度、压力、流量、电流"
        - "AO: 阀门开度、频率给定"
        - "DI: 运行状态、故障状态"
        - "DO: 启停命令、阀门命令"
      communication_protocol: "MODBUS TCP/IP"
      data_update_rate: "1s扫描"
      network_requirement: "千兆以太网"

topological_flows:
  primary_flow_paths:
    supply_path: # 冷水供应
      description: "冷水机组 → 分水器 → 空调机组 → 分集水器 → 回流"
      flow_rate: "605 + 302 = 907 m³/h (主机运行)"
      temperature_drop: "12 → 7°C"
      energy_transfer: "通过冷凝器/蒸发器交换热量"
      control_point: "机组启停 + 温度设定"
      monitoring: "24小时全程监控"

    return_path: # 冷水回流
      description: "空调机组回水 → 集水器 → 冷水机组蒸发器 → 回流"
      energy_content: "包含建筑热量"
      temperature_rise: "7 → 12°C"
      conditioning: "经过冷水机组蒸发器放热"

    cooling_tower_path: # 冷却水循环
      description: "冷却塔 → 冷凝器 → 循环泵 → 冷却塔"
      heat_rejection: "684 + 328 = 1012 kW"
      rejection_medium: "向大气放热 (蒸散 + 对流)"
      water_consumption: "蒸发 + 漂散 + 排污 ≈ 2% 循环水量"
      make_up_required: "连续补水"

backup_flow_paths:
    cross_connection:
      description: "多台冷水机组/冷却塔间交叉连接"
      operation_mode: "N+1 冗余运行"
      switching_time: "≤15分钟"
      reliability: "50% 冷量备份保障"

    emergency_bypass:
      description: "区域应急旁通路径"
      operation_mode: "维修工况或故障工况"
      manual_override: "本地操作 + 远程监控"
      isolation_capability: "分区独立运行"

# ASCII 拓扑图示
ascii_topology_diagram: |

        电气系统接口(ELECTRICAL)    冷却塔补水接口(PLUMBING)
                   │                        │
                   │ 高压配电               │ 市政供水
                   ▼                        ▼
    ======================================================
        ┌────────────────────────────────────────────┐
        │           HVAC-CHP 冷源系统拓扑            │
        │     Medical Building Chiller Plant       │
        └────────────────────────────────────────────┘

    ┌───────────┐   TRUNK-05      ┌───────────┐  TRUNK-04   ┌───────────┐
    │冷却塔#1   │←─────────────→│冷却水主分配│←─────────→│冷却塔#2   │
    │ SR-CT-01 │  冷却水回路 │  DIST-CDW  │ 冷却水回路 │ SR-CT-02 │
    └─────┬─────┘                └─────┬─────┘                └─────┬─────┘
          │ TRUNK-01,02                │ PRIMARY               TRUNK-03 │
          ▼                            ▼                            ▼
    ┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐
    │冷水机组#1 │   │冷水机组#2 │   │吸收式机#3 │   │冷冻水主分│   │冷冻水分区│
    │ SR-01     │   │ SR-02     │   │ SR-03     │   │ DIST-CHW  │  │ DIST-CHW  │
    └─────┬─────┘   └─────┬─────┘   └─────┬─────┘   └─────┬─────┘  └─────┬─────┘
          │               │               │               │              │
          └───────────────┴───────┐   ┌───┴───────────────┘              │
                                 ▼   ▼                                  │
                          供回双向循环路径                               │
                          CHILLED WATER SUPPLY & RETURN                     │
                                 │   │                                  │
                                 ▼   ▼                                  ▼
    ┌───────────┐   BRANCH-01    ┌───────────┐   BRANCH-02   ┌───────────┐  TERM-01,02
    │门诊主空调 │←─────────────→│手术室净化 │←─────────────→│ICU精密空调│← ───┐
    │ AHU-01    │   冷冻水     │ OR-01     │   冷冻水     │ ICU-01    │     │电气信号
    └───────────┘               └───────────┘               └───────────┘     ▼
                                                                               BAS/EMS
    ┌───────────┐    TERM-03    ┌───────────┐    TERM-04   ┌───────────┐
    │药房精密空调│←─────────────→│冷却塔循环泵│←─────────────→│冷水机组电 │ ←──┐
    │ PHARMACY  │   冷冻水     │ 300kW     │   电力      │气控制信号 │    │
    └───────────┘               └───────────┘               └───────────┘    ▼
                                                                            BAS/EMS

    LEGEND:
    =======
    🔄 TRUNK    : 主干连接 (大管径高容量)            │   SR   : 源节点 (Source)
    🔄 BRANCH   : 分支连接 (中等管径容量)            │   DIST : 分配节点 (Distribution)
    🔄 TERMINAL : 终端连接 (管径小容量低)            │   SINK : 汇节点 (Sink)
    🔄 三相议头 : 双向循环流量                   │   TERM : 终端连接 (Terminal)

    ○ 系统自动调节控制点                           ■ 用户调节接口点
    △ 故障切换点                                   ◆ 绝缘防护点

    DEPENDENCY CONNECTIONS:
    ====================
    ◀── 电力供应依赖 (ELECTRICAL-HV/EPS)  ──▶
    ◀── 给水补水依赖 (PLUMBING-WSS)      ──▶
    ◀── BAS控制依赖 (BUILDING_AUTOMATION) ──▶

    CONTROL TECHNOLOGY:
    =================
    1. 变转速(VFD)调节：水泵、风机、压缩机
    2. 变设定值(ΔT)调节：温度、压力、流量设定
    3. 组合优化控制：设备最优组合运行策略
    4. 预测控制：负荷预测 + 动态响应
    5. 故障自愈：冗余切换 + 降级运行

    ENERGY FLOW MONITORING:
    =====================
    A点: 供冷量测量 (流量计 + 温差 → 冷量)
    B点: 冷却水散热测量 (蒸汽冷凝前后温差 → 排热量)
    C点: 主要设备电功率测量 (功率计 → 效率计算)
    D点: 环境参数测量 (温湿度 → 效率环境修正)

model_validation:
  completeness_check:
    nodes: "包含源、分配、汇节点完整链条"
    edges: "供回双向回路完整"
    components: "主要设备部件级建模"
    control: "基本控制回路模型"
    monitoring: "主要监控点设置"

  consistency_check:
    flow_balance: "输入输出流量平衡验证 ✓"
    energy_balance: "冷热量平衡验证 ✓"
    pressure_balance: "管网压力平衡验证 ✓"
    control_logics: "控制逻辑一致性验证 ✓"

  compliance_check:
    regulatory: "符合 GB 50736、GB 50019标准"
    healthcare: "满足医疗建筑特殊要求"
    energy: "符合节能设计标准"
    safety: "满足安全运行要求"

next_topo_model_scope:
  candidates:
    - "HVAC-HTP 热源系统拓扑"
    - "ELECTRICAL-HV 高压配电系统拓扑"
    - "MEDICAL_GAS-O2 医用氧气系统拓扑"
    - "BUILDING_AUTOMATION-BAS 楼宇自控系统拓扑"