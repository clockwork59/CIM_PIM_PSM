## 🧑‍💻 User


补充极少数特殊系统或进行系统间关联矩阵、全局验证等工作

---
## 🤖 Assistant


# Agent-01 Batch 7 完整输出

## Batch 7 系统清单

```yaml
Batch_7_Systems:
  
  category: 特殊系统补充 + 系统间关联矩阵 + 全局验证
  
  contents:
    part_1_special_systems:
      - MGAS-He: 氦气系统
      - MGAS-Ar: 氩气系统
      - ELEC-SOLAR: 光伏发电系统
      - HVAC-RADIANT: 辐射供暖制冷系统
      - PLUMB-PURE: 纯水系统
      
    part_2_cross_system_matrix:
      - 系统间介质交换矩阵
      - 系统间控制信号矩阵
      - 系统间联动逻辑矩阵
      - 跨系统边界接口清单
      
    part_3_global_validation:
      - 节点完整性验证
      - 边完整性验证
      - 路径连通性验证
      - 介质一致性验证
      - 命名规范验证
```

---

# 第一部分：特殊系统补充

## 7.1 MGAS-He 氦气系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: MGAS-He
    system_name: 氦气系统
    system_name_en: Helium Gas System
    category: MEDICAL_GAS
    priority: P3-OPTIONAL
    version: 1.0
    
    description: |
      医院医用氦气系统，主要用于MRI超导磁体冷却。
      氦气作为液态冷却剂维持超导磁体的超低温状态。
      
    design_basis:
      purity: {value: "≥99.999", unit: "%", note: 高纯氦}
      form: 液态氦（LHe）
      temperature: {value: 4.2, unit: K, note: 沸点}
      application: MRI超导磁体冷却
      
    serving_scope:
      - MRI机房
      - 科研实验室（如有）

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: MGAS-He_BND_IN_SUPPLY
        boundary_name: 液氦供应
        medium: GAS-He-LIQUID
        is_external: true
        source: 液氦供应商
        
    outputs:
      - boundary_id: MGAS-He_BND_OUT_VENT
        boundary_name: 氦气排放
        medium: GAS-He
        is_external: true
        target: 大气（屋顶排放）

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:
  
    source_nodes:
    
      - node_id: MGAS-He_SRC_DEWAR
        node_name: 液氦杜瓦罐
        node_name_en: Liquid Helium Dewar
        node_type: Source_Node
        node_category: SRC
        
        function: 液氦储存与供应
        medium_out: GAS-He-LIQUID
        
        equipment_parameters:
          type: 移动式液氦杜瓦罐
          capacity: {value: 100-500, unit: L}
          insulation: 真空绝热
          pressure: {value: 0.05-0.1, unit: MPa}
          supplier: 定期配送
          
        location_hint:
          space_type: OUTDOOR / MEP_ROOM
          position: MRI机房外专用存放区
          requirement: 通风良好，远离火源
          
        note: |
          液氦通常由专业供应商定期配送和加注，
          不需要院内永久性存储设施。

    distribution_nodes:
    
      - node_id: MGAS-He_DST_TRANSFER
        node_name: 液氦加注接口
        node_name_en: LHe Transfer Interface
        node_type: Distribution_Node
        node_category: DST
        node_subtype: JUN
        
        function: 液氦加注连接
        medium_in: GAS-He-LIQUID
        medium_out: GAS-He-LIQUID
        
        equipment_parameters:
          type: 真空绝热加注管路
          interface: 快速连接头
          
        location_hint:
          space_type: ROOM
          position: MRI机房外
          
      - node_id: MGAS-He_DST_MRI_CRYOSTAT
        node_name: MRI低温恒温器
        node_name_en: MRI Cryostat
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BUF
        
        function: 超导磁体冷却
        medium_in: GAS-He-LIQUID
        medium_out: GAS-He
        
        equipment_parameters:
          type: 超导磁体低温系统
          components:
            - 液氦容器
            - 热屏蔽层
            - 真空绝热层
            - 冷头（零蒸发系统）
          capacity: {value: 1000-2000, unit: L}
          boil_off: {value: 0, unit: L/day, note: 零蒸发系统}
          
        location_hint:
          space_type: EQUIPMENT
          position: MRI设备内部
          
        control_points:
          sensors:
            - {point_id: MRI_He_LEVEL, type: AI, description: 液氦液位}
            - {point_id: MRI_He_PRESS, type: AI, description: 氦压力}
            - {point_id: MRI_MAGNET_TEMP, type: AI, description: 磁体温度}
          status:
            - {point_id: MRI_He_LOW, type: DI, description: 液氦低液位}
            - {point_id: MRI_QUENCH, type: DI, description: 失超报警}

      - node_id: MGAS-He_DST_VENT_PIPE
        node_name: 氦气排放管
        node_name_en: Helium Vent Pipe
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
        
        function: 失超时氦气紧急排放
        medium_in: GAS-He
        medium_out: GAS-He
        
        equipment_parameters:
          type: 失超排放管道
          material: 不锈钢
          diameter: {value: DN150-DN200, unit: mm}
          design: 承受快速升压
          
        location_hint:
          space_type: SHAFT / EXTERIOR
          position: MRI机房至屋顶
          
        installation_requirements:
          - 最短路径至室外
          - 无弯头或少弯头
          - 防止积水
          - 隔热防冻

    sink_nodes:
    
      - node_id: MGAS-He_SNK_VENT
        node_name: 屋顶排放口
        node_name_en: Roof Vent Outlet
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 氦气排放
        medium_in: GAS-He
        is_external: true
        
        equipment_parameters:
          type: 排放帽
          height: {value: "≥3", unit: m, note: 高于屋面}
          
        location_hint:
          space_type: EXTERIOR
          position: 屋顶
          requirement: 远离新风口和人员活动区

  # ============================================================
  # 边定义
  # ============================================================
  edges:
  
    supply_edges:
    
      - edge_id: MGAS-He_EDGE_001
        edge_name: 杜瓦至加注接口
        edge_type: TRK
        from_node: MGAS-He_SRC_DEWAR
        to_node: MGAS-He_DST_TRANSFER
        direction: unidirectional
        medium: GAS-He-LIQUID
        note: 临时连接，加注时使用
        
      - edge_id: MGAS-He_EDGE_002
        edge_name: 加注至MRI低温系统
        edge_type: TRK
        from_node: MGAS-He_DST_TRANSFER
        to_node: MGAS-He_DST_MRI_CRYOSTAT
        direction: unidirectional
        medium: GAS-He-LIQUID

    vent_edges:
    
      - edge_id: MGAS-He_EDGE_003
        edge_name: MRI至排放管
        edge_type: TRK
        from_node: MGAS-He_DST_MRI_CRYOSTAT
        to_node: MGAS-He_DST_VENT_PIPE
        direction: unidirectional
        medium: GAS-He
        
      - edge_id: MGAS-He_EDGE_004
        edge_name: 排放管至屋顶
        edge_type: TRK
        from_node: MGAS-He_DST_VENT_PIPE
        to_node: MGAS-He_SNK_VENT
        direction: unidirectional
        medium: GAS-He

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:
  
    - path_id: MGAS-He_PATH_FILL
      path_name: 液氦加注路径
      path_type: SUP
      mode: 定期加注
      sequence:
        - {step: 1, element_type: node, element_id: MGAS-He_SRC_DEWAR}
        - {step: 2, element_type: node, element_id: MGAS-He_DST_TRANSFER}
        - {step: 3, element_type: node, element_id: MGAS-He_DST_MRI_CRYOSTAT}
        
    - path_id: MGAS-He_PATH_QUENCH
      path_name: 失超排放路径
      path_type: EMG
      mode: 紧急排放
      sequence:
        - {step: 1, element_type: node, element_id: MGAS-He_DST_MRI_CRYOSTAT}
        - {step: 2, element_type: node, element_id: MGAS-He_DST_VENT_PIPE}
        - {step: 3, element_type: node, element_id: MGAS-He_SNK_VENT}

  # ============================================================
  # 安全与报警
  # ============================================================
  safety_and_alarm:
  
    quench_emergency:
      description: MRI失超紧急处理
      trigger: 超导磁体失超
      consequences:
        - 液氦快速蒸发
        - 大量氦气释放
        - 房间内氧气浓度下降
      response:
        - 自动排放至室外
        - 人员立即撤离
        - 通风系统加强
        - 氧浓度监测报警
        
    oxygen_monitoring:
      location: MRI机房
      setpoint:
        warning: {value: 19.5, unit: "%"}
        alarm: {value: 18, unit: "%"}
      action:
        - 声光报警
        - 联动通风
        - 禁止进入
        
    helium_level_monitoring:
      normal: 定期监测液位
      low_level:
        warning: 提前安排加注
        critical: 准备停机保护
```

---

## 7.2 MGAS-Ar 氩气系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: MGAS-Ar
    system_name: 氩气系统
    system_name_en: Argon Gas System
    category: MEDICAL_GAS
    priority: P3-OPTIONAL
    version: 1.0
    
    description: |
      医院医用氩气系统，主要用于氩气刀（氩等离子凝固术）、
      氩氦刀冷冻消融等治疗设备。
      
    design_basis:
      purity: {value: "≥99.99", unit: "%"}
      supply_pressure: {value: 0.4-0.6, unit: MPa}
      source: 瓶装氩气
      
    serving_scope:
      - 内镜中心（氩等离子凝固）
      - 介入手术室（氩氦刀）
      - 肿瘤治疗中心

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: MGAS-Ar_BND_IN_SUPPLY
        boundary_name: 氩气气源
        medium: GAS-Ar
        is_external: true
        source: 氩气钢瓶
        
    outputs:
      - boundary_id: MGAS-Ar_BND_OUT_TERM
        boundary_name: 氩气终端
        medium: GAS-Ar
        target: 使用点

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:
  
    source_nodes:
    
      - node_id: MGAS-Ar_SRC_CYLINDER
        node_name: 氩气钢瓶组
        node_name_en: Argon Cylinder Manifold
        node_type: Source_Node
        node_category: SRC
        
        function: 氩气气源
        medium_out: GAS-Ar
        
        equipment_parameters:
          type: 汇流排系统
          configuration: 双排（主+备）
          cylinders_per_bank: {value: 4-6, unit: 瓶}
          cylinder_volume: {value: 40, unit: L}
          cylinder_pressure: {value: 15, unit: MPa}
          switchover: 自动切换
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 医气汇流排间
          
        control_points:
          sensors:
            - {point_id: Ar_BANK_P, type: AI, description: 气瓶组压力}
          status:
            - {point_id: Ar_BANK_SEL, type: DI, description: 主备切换}
            - {point_id: Ar_LOW_P, type: DI, description: 低压报警}

    distribution_nodes:
    
      - node_id: MGAS-Ar_DST_REGULATOR
        node_name: 减压稳压器
        node_name_en: Pressure Regulator
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 一级减压
        medium_in: GAS-Ar
        medium_out: GAS-Ar
        
        equipment_parameters:
          type: 一级减压器
          inlet_pressure: {value: 15, unit: MPa}
          outlet_pressure: {value: 0.8-1.0, unit: MPa}
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 医气汇流排间

      - node_id: MGAS-Ar_DST_MAIN_PIPE
        node_name: 氩气主管
        node_name_en: Argon Main Pipe
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
        
        function: 氩气主干输送
        medium_in: GAS-Ar
        medium_out: GAS-Ar
        
        equipment_parameters:
          material: 无缝不锈钢管/脱脂紫铜管
          diameter: {value: DN15-DN20, unit: mm}
          pressure_rating: {value: 1.6, unit: MPa}
          
        location_hint:
          space_type: CEILING_VOID / SHAFT
          position: 管道井/吊顶内

      - node_id: MGAS-Ar_DST_ZONE_VALVE
        node_name: 区域阀
        node_name_en: Zone Valve Box
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 区域控制与二次减压
        medium_in: GAS-Ar
        medium_out: GAS-Ar
        
        multiplicity: multiple
        
        equipment_parameters:
          components:
            - 截止阀
            - 二级减压器
            - 压力表
            - 泄压阀
          outlet_pressure: {value: 0.4-0.6, unit: MPa}
          
        location_hint:
          space_type: WALL_BOX
          position: 内镜中心/介入手术室走廊
          
        control_points:
          sensors:
            - {point_id: Ar_ZONE_P, type: AI, description: 区域压力}

      - node_id: MGAS-Ar_DST_BRANCH
        node_name: 氩气支管
        node_name_en: Argon Branch Pipe
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BRH
        
        function: 分配至终端
        medium_in: GAS-Ar
        medium_out: GAS-Ar
        
        multiplicity: multiple
        
        equipment_parameters:
          material: 无缝不锈钢管/脱脂紫铜管
          diameter: {value: DN10-DN15, unit: mm}
          
        location_hint:
          space_type: CEILING_VOID
          position: 内镜室/介入手术室吊顶

    sink_nodes:
    
      - node_id: MGAS-Ar_SNK_TERMINAL
        node_name: 氩气终端
        node_name_en: Argon Terminal
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 氩气使用
        medium_in: GAS-Ar
        
        multiplicity: multiple
        
        equipment_parameters:
          type: 快速接头
          color_code: 根据标准
          pressure: {value: 0.4-0.6, unit: MPa}
          
        location_hint:
          space_type: WALL / EQUIPMENT
          position: 内镜室/介入手术室
          
        typical_locations:
          - 消化内镜中心
          - 呼吸内镜中心
          - 介入手术室

      - node_id: MGAS-Ar_SNK_APC
        node_name: 氩等离子凝固设备
        node_name_en: Argon Plasma Coagulator
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 氩等离子凝固治疗
        medium_in: GAS-Ar
        
        equipment_parameters:
          type: APC氩气刀
          flow: {value: 0.5-8, unit: L/min}
          power: {value: 1-120, unit: W}
          application:
            - 内镜止血
            - 肿瘤消融
            - 组织切除
            
        location_hint:
          space_type: EQUIPMENT
          position: 内镜检查室

      - node_id: MGAS-Ar_SNK_CRYOABLATION
        node_name: 氩氦刀设备
        node_name_en: Argon-Helium Cryoablation System
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 冷冻消融治疗
        medium_in: GAS-Ar
        
        equipment_parameters:
          type: 氩氦刀冷冻消融系统
          principle: 氩气冷冻（-140℃）+ 氦气复温
          flow: 高流量
          application:
            - 肝癌
            - 肺癌
            - 肾癌
            - 前列腺癌
            
        location_hint:
          space_type: EQUIPMENT
          position: 介入手术室

  # ============================================================
  # 边定义
  # ============================================================
  edges:
  
    supply_edges:
    
      - edge_id: MGAS-Ar_EDGE_001
        edge_name: 钢瓶至减压器
        edge_type: TRK
        from_node: MGAS-Ar_SRC_CYLINDER
        to_node: MGAS-Ar_DST_REGULATOR
        direction: unidirectional
        medium: GAS-Ar
        
      - edge_id: MGAS-Ar_EDGE_002
        edge_name: 减压器至主管
        edge_type: TRK
        from_node: MGAS-Ar_DST_REGULATOR
        to_node: MGAS-Ar_DST_MAIN_PIPE
        direction: unidirectional
        medium: GAS-Ar
        
      - edge_id: MGAS-Ar_EDGE_003
        edge_name: 主管至区域阀
        edge_type: BRH
        from_node: MGAS-Ar_DST_MAIN_PIPE
        to_node: MGAS-Ar_DST_ZONE_VALVE
        direction: unidirectional
        medium: GAS-Ar
        
      - edge_id: MGAS-Ar_EDGE_004
        edge_name: 区域阀至支管
        edge_type: BRH
        from_node: MGAS-Ar_DST_ZONE_VALVE
        to_node: MGAS-Ar_DST_BRANCH
        direction: unidirectional
        medium: GAS-Ar
        
      - edge_id: MGAS-Ar_EDGE_005
        edge_name: 支管至终端
        edge_type: TRM
        from_node: MGAS-Ar_DST_BRANCH
        to_node: MGAS-Ar_SNK_TERMINAL
        direction: unidirectional
        medium: GAS-Ar
        
      - edge_id: MGAS-Ar_EDGE_006
        edge_name: 终端至APC设备
        edge_type: TRM
        from_node: MGAS-Ar_SNK_TERMINAL
        to_node: MGAS-Ar_SNK_APC
        direction: unidirectional
        medium: GAS-Ar

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:
  
    - path_id: MGAS-Ar_PATH_MAIN
      path_name: 氩气供应路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: MGAS-Ar_SRC_CYLINDER}
        - {step: 2, element_type: node, element_id: MGAS-Ar_DST_REGULATOR}
        - {step: 3, element_type: node, element_id: MGAS-Ar_DST_MAIN_PIPE}
        - {step: 4, element_type: node, element_id: MGAS-Ar_DST_ZONE_VALVE}
        - {step: 5, element_type: node, element_id: MGAS-Ar_DST_BRANCH}
        - {step: 6, element_type: node, element_id: MGAS-Ar_SNK_TERMINAL}
        - {step: 7, element_type: node, element_id: MGAS-Ar_SNK_APC}

  # ============================================================
  # 报警逻辑
  # ============================================================
  alarm_logic:
  
    low_pressure:
      bank:
        warning: {value: 3, unit: MPa}
        alarm: {value: 2, unit: MPa}
      supply:
        warning: {value: 0.35, unit: MPa}
        alarm: {value: 0.3, unit: MPa}
```

---

## 7.3 ELEC-SOLAR 光伏发电系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: ELEC-SOLAR
    system_name: 光伏发电系统
    system_name_en: Photovoltaic Power System
    category: ELECTRICAL
    priority: P3-OPTIONAL
    version: 1.0
    
    description: |
      医院屋顶光伏发电系统，利用太阳能发电，
      实现节能减排和电费节约。采用自发自用、余电上网模式。
      
    design_basis:
      mode: 自发自用、余电上网
      capacity: 根据屋顶面积
      efficiency: 单晶硅组件效率20%+
      inverter: 组串式/集中式
      
    serving_scope:
      - 建筑屋顶
      - 车棚顶部
      - 幕墙（BIPV）

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: ELEC-SOLAR_BND_IN_SUN
        boundary_name: 太阳辐射
        medium: ENERGY-SOLAR
        is_external: true
        source: 太阳
        
    outputs:
      - boundary_id: ELEC-SOLAR_BND_OUT_GRID
        boundary_name: 并网电力
        medium: ELEC-AC
        target_system: ELEC-HV
        
      - boundary_id: ELEC-SOLAR_BND_OUT_LOAD
        boundary_name: 自用电力
        medium: ELEC-AC
        target_system: ELEC-LV-MAIN

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:
  
    source_nodes:
    
      - node_id: ELEC-SOLAR_SRC_ARRAY
        node_name: 光伏阵列
        node_name_en: PV Array
        node_type: Source_Node
        node_category: SRC
        
        function: 光电转换
        medium_out: ELEC-DC
        
        equipment_parameters:
          type: 单晶硅光伏组件
          power_per_panel: {value: 400-600, unit: Wp}
          efficiency: {value: "≥20", unit: "%"}
          total_capacity: {value: 100-1000, unit: kWp}
          installation:
            - 屋顶支架安装
            - 车棚顶安装
            - BIPV幕墙
            
        location_hint:
          space_type: EXTERIOR
          position: 建筑屋顶/车棚
          
        control_points:
          sensors:
            - {point_id: PV_IRRAD, type: AI, description: 太阳辐照度}
            - {point_id: PV_TEMP, type: AI, description: 组件温度}
            - {point_id: PV_V_DC, type: AI, description: 直流电压}
            - {point_id: PV_I_DC, type: AI, description: 直流电流}

    distribution_nodes:
    
      - node_id: ELEC-SOLAR_DST_COMBINER
        node_name: 光伏汇流箱
        node_name_en: PV Combiner Box
        node_type: Distribution_Node
        node_category: DST
        node_subtype: JUN
        
        function: 光伏组串汇流
        medium_in: ELEC-DC
        medium_out: ELEC-DC
        
        multiplicity: multiple
        
        equipment_parameters:
          type: 直流汇流箱
          inputs: {value: 8-16, unit: 路}
          voltage: {value: 1000-1500, unit: VDC}
          protection:
            - 直流断路器
            - 防雷保护
            - 反接保护
            
        location_hint:
          space_type: EXTERIOR
          position: 光伏阵列附近
          
        control_points:
          sensors:
            - {point_id: CB_V, type: AI, description: 汇流电压}
            - {point_id: CB_I, type: AI, description: 汇流电流}
          status:
            - {point_id: CB_FAULT, type: DI, description: 故障报警}

      - node_id: ELEC-SOLAR_DST_INVERTER
        node_name: 光伏逆变器
        node_name_en: PV Inverter
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
        
        function: DC-AC转换
        medium_in: ELEC-DC
        medium_out: ELEC-AC
        
        multiplicity: multiple
        instance_pattern: ELEC-SOLAR_DST_INVERTER_{Seq}
        
        equipment_parameters:
          type: 组串式逆变器/集中式逆变器
          power: {value: 50-500, unit: kW}
          efficiency: {value: "≥98", unit: "%"}
          mppt: 多路MPPT
          features:
            - 防孤岛保护
            - 低电压穿越
            - 无功补偿
            
        location_hint:
          space_type: MEP_ROOM / EXTERIOR
          position: 配电室/屋顶
          
        control_points:
          sensors:
            - {point_id: INV_P, type: AI, description: 输出功率}
            - {point_id: INV_V_AC, type: AI, description: 交流电压}
            - {point_id: INV_I_AC, type: AI, description: 交流电流}
            - {point_id: INV_PF, type: AI, description: 功率因数}
            - {point_id: INV_TEMP, type: AI, description: 逆变器温度}
          status:
            - {point_id: INV_RUN, type: DI, description: 运行状态}
            - {point_id: INV_FAULT, type: DI, description: 故障报警}
            - {point_id: INV_GRID, type: DI, description: 并网状态}

      - node_id: ELEC-SOLAR_DST_AC_COMBINER
        node_name: 交流汇流柜
        node_name_en: AC Combiner Cabinet
        node_type: Distribution_Node
        node_category: DST
        node_subtype: JUN
        
        function: 逆变器交流汇流
        medium_in: ELEC-AC
        medium_out: ELEC-AC
        
        equipment_parameters:
          type: 交流汇流配电柜
          voltage: {value: 0.4, unit: kV}
          protection:
            - 交流断路器
            - 防雷保护
            
        location_hint:
          space_type: MEP_ROOM
          room_name: 光伏配电室

      - node_id: ELEC-SOLAR_DST_GRID_CONNECT
        node_name: 并网点
        node_name_en: Grid Connection Point
        node_type: Distribution_Node
        node_category: DST
        node_subtype: JUN
        
        function: 光伏并网接入
        medium_in: ELEC-AC
        medium_out: ELEC-AC
        
        equipment_parameters:
          type: 并网柜
          voltage: {value: 0.4-10, unit: kV}
          components:
            - 并网开关
            - 计量装置
            - 保护装置
            - 通讯装置
            
        location_hint:
          space_type: MEP_ROOM
          room_name: 高低压配电室
          
        control_points:
          sensors:
            - {point_id: GRID_P, type: AI, description: 并网功率}
            - {point_id: GRID_E, type: AI, description: 发电量}
          status:
            - {point_id: GRID_CONNECT, type: DI, description: 并网状态}

      - node_id: ELEC-SOLAR_DST_MONITOR
        node_name: 光伏监控系统
        node_name_en: PV Monitoring System
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 光伏系统监控
        medium_in: DATA-IP
        medium_out: DATA-IP
        
        equipment_parameters:
          type: 光伏监控平台
          functions:
            - 实时监测
            - 发电统计
            - 故障诊断
            - 远程运维
            - 收益分析
            
        location_hint:
          space_type: RACK
          room_name: 监控室/数据中心

    sink_nodes:
    
      - node_id: ELEC-SOLAR_SNK_LOAD
        node_name: 院内负荷
        node_name_en: Hospital Load
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 自发自用
        medium_in: ELEC-AC
        
        target_system: ELEC-LV-MAIN
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室

      - node_id: ELEC-SOLAR_SNK_GRID
        node_name: 市电电网
        node_name_en: Utility Grid
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 余电上网
        medium_in: ELEC-AC
        is_external: true
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 高压配电室

  # ============================================================
  # 边定义
  # ============================================================
  edges:
  
    dc_edges:
    
      - edge_id: ELEC-SOLAR_EDGE_001
        edge_name: 光伏阵列至汇流箱
        edge_type: TRK
        from_node: ELEC-SOLAR_SRC_ARRAY
        to_node: ELEC-SOLAR_DST_COMBINER
        direction: unidirectional
        medium: ELEC-DC
        physical_properties:
          cable: 光伏专用电缆
          
      - edge_id: ELEC-SOLAR_EDGE_002
        edge_name: 汇流箱至逆变器
        edge_type: TRK
        from_node: ELEC-SOLAR_DST_COMBINER
        to_node: ELEC-SOLAR_DST_INVERTER
        direction: unidirectional
        medium: ELEC-DC

    ac_edges:
    
      - edge_id: ELEC-SOLAR_EDGE_003
        edge_name: 逆变器至交流汇流
        edge_type: TRK
        from_node: ELEC-SOLAR_DST_INVERTER
        to_node: ELEC-SOLAR_DST_AC_COMBINER
        direction: unidirectional
        medium: ELEC-AC
        
      - edge_id: ELEC-SOLAR_EDGE_004
        edge_name: 交流汇流至并网点
        edge_type: TRK
        from_node: ELEC-SOLAR_DST_AC_COMBINER
        to_node: ELEC-SOLAR_DST_GRID_CONNECT
        direction: unidirectional
        medium: ELEC-AC
        
      - edge_id: ELEC-SOLAR_EDGE_005
        edge_name: 并网点至院内负荷
        edge_type: TRK
        from_node: ELEC-SOLAR_DST_GRID_CONNECT
        to_node: ELEC-SOLAR_SNK_LOAD
        direction: unidirectional
        medium: ELEC-AC
        
      - edge_id: ELEC-SOLAR_EDGE_006
        edge_name: 并网点至电网
        edge_type: TRK
        from_node: ELEC-SOLAR_DST_GRID_CONNECT
        to_node: ELEC-SOLAR_SNK_GRID
        direction: bidirectional
        medium: ELEC-AC
        note: 余电上网时向外送电

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:
  
    - path_id: ELEC-SOLAR_PATH_SELF_USE
      path_name: 自发自用路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: ELEC-SOLAR_SRC_ARRAY}
        - {step: 2, element_type: node, element_id: ELEC-SOLAR_DST_COMBINER}
        - {step: 3, element_type: node, element_id: ELEC-SOLAR_DST_INVERTER}
        - {step: 4, element_type: node, element_id: ELEC-SOLAR_DST_AC_COMBINER}
        - {step: 5, element_type: node, element_id: ELEC-SOLAR_DST_GRID_CONNECT}
        - {step: 6, element_type: node, element_id: ELEC-SOLAR_SNK_LOAD}

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:
  
    mppt_control:
      description: 最大功率点跟踪
      method: 扰动观察法/电导增量法
      
    power_control:
      modes:
        - 最大功率模式
        - 限功率模式
        - 无功补偿模式
        
    protection:
      anti_islanding: 防孤岛保护
      lvrt: 低电压穿越
      overvoltage: 过压保护
      overcurrent: 过流保护
```

---

## 7.4 HVAC-RADIANT 辐射供暖制冷系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: HVAC-RADIANT
    system_name: 辐射供暖制冷系统
    system_name_en: Radiant Heating and Cooling System
    category: HVAC
    priority: P3-OPTIONAL
    version: 1.0
    
    description: |
      医院辐射供暖制冷系统，通过地板、天花板或墙面辐射
      进行供暖和制冷，提供舒适的热环境，适用于大空间。
      
    design_basis:
      heating:
        surface_temp: {value: 29-35, unit: ℃}
        water_temp: {value: 35-45, unit: ℃}
      cooling:
        surface_temp: {value: 18-20, unit: ℃}
        water_temp: {value: 16-18, unit: ℃}
      application: 门诊大厅、病房等
      
    serving_scope:
      - 门诊大厅
      - 候诊区
      - VIP病房
      - 康复中心

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: HVAC-RADIANT_BND_IN_CHW
        boundary_name: 冷冻水
        medium: WATER-CHW
        source_system: HVAC-CHP
        note: 制冷用水温较高16-18℃
        
      - boundary_id: HVAC-RADIANT_BND_IN_HW
        boundary_name: 热水
        medium: WATER-HW
        source_system: HVAC-HWP
        note: 供暖用水温较低35-45℃
        
      - boundary_id: HVAC-RADIANT_BND_IN_ELEC
        boundary_name: 电源
        medium: ELEC-LV
        source_system: ELEC-LV-MAIN
        
    outputs:
      - boundary_id: HVAC-RADIANT_BND_OUT_HEAT
        boundary_name: 辐射热
        medium: ENERGY-THERMAL
        target: 室内空间

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:
  
    source_nodes:
    
      - node_id: HVAC-RADIANT_SRC_CHW
        node_name: 冷冻水接口
        node_name_en: Chilled Water Interface
        node_type: Source_Node
        node_category: SRC
        
        function: 冷冻水接入（辐射制冷）
        medium_out: WATER-CHW
        
        source_system: HVAC-CHP
        
        equipment_parameters:
          water_temp: {value: 16-18, unit: ℃, note: 高于露点}
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 空调机房

      - node_id: HVAC-RADIANT_SRC_HW
        node_name: 热水接口
        node_name_en: Hot Water Interface
        node_type: Source_Node
        node_category: SRC
        
        function: 热水接入（辐射供暖）
        medium_out: WATER-HW
        
        source_system: HVAC-HWP
        
        equipment_parameters:
          water_temp: {value: 35-45, unit: ℃, note: 低温热水}
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 换热站

    distribution_nodes:
    
      - node_id: HVAC-RADIANT_DST_MIXING
        node_name: 混水装置
        node_name_en: Mixing Unit
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 水温调节混合
        medium_in: [WATER-CHW, WATER-HW]
        medium_out: WATER-RADIANT
        
        equipment_parameters:
          type: 混水中心
          components:
            - 循环泵
            - 混水阀
            - 温度传感器
            - 旁通阀
          control: 根据室温调节水温
          
        location_hint:
          space_type: MEP_ROOM
          position: 分集水器附近
          
        control_points:
          sensors:
            - {point_id: MIX_T_SUP, type: AI, description: 供水温度}
            - {point_id: MIX_T_RET, type: AI, description: 回水温度}
          commands:
            - {point_id: MIX_VALVE, type: AO, description: 混水阀开度}

      - node_id: HVAC-RADIANT_DST_MANIFOLD
        node_name: 分集水器
        node_name_en: Manifold
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
        
        function: 水路分配
        medium_in: WATER-RADIANT
        medium_out: WATER-RADIANT
        
        multiplicity: multiple
        instance_pattern: HVAC-RADIANT_DST_MANIFOLD_{Zone}
        
        equipment_parameters:
          type: 分集水器
          loops: {value: 6-12, unit: 回路}
          components:
            - 分水器
            - 集水器
            - 流量调节阀
            - 排气阀
            - 泄水阀
            
        location_hint:
          space_type: WALL_BOX
          position: 各分区集中位置
          
        control_points:
          sensors:
            - {point_id: MAN_T, type: AI, description: 供水温度}

      - node_id: HVAC-RADIANT_DST_FLOOR_LOOP
        node_name: 地板辐射盘管
        node_name_en: Floor Radiant Loop
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRM
        
        function: 地板辐射换热
        medium_in: WATER-RADIANT
        medium_out: WATER-RADIANT
        
        multiplicity: multiple
        
        equipment_parameters:
          type: PE-RT/PE-Xa地暖管
          diameter: {value: 16-20, unit: mm}
          spacing: {value: 150-300, unit: mm}
          layout: 回形/蛇形
          covering: 回填层+面层
          
        location_hint:
          space_type: FLOOR
          position: 楼地面内
          
        installation_requirements:
          - 保温层
          - 反射膜
          - 盘管固定
          - 回填层
          - 伸缩缝

      - node_id: HVAC-RADIANT_DST_CEILING_PANEL
        node_name: 天花辐射板
        node_name_en: Ceiling Radiant Panel
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRM
        
        function: 天花辐射换热
        medium_in: WATER-RADIANT
        medium_out: WATER-RADIANT
        
        multiplicity: multiple
        
        equipment_parameters:
          type: 金属辐射天花板
          material: 铝板+铜管
          size: {value: "600×600/600×1200", unit: mm}
          capacity: {value: 50-100, unit: W/m²}
          
        location_hint:
          space_type: CEILING
          position: 天花板
          
        note: 适用于制冷为主的区域

      - node_id: HVAC-RADIANT_DST_CONDENSATION_CTRL
        node_name: 露点控制系统
        node_name_en: Condensation Control System
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 防止辐射面结露
        medium_in: SIGNAL
        medium_out: CTRL
        
        equipment_parameters:
          type: 露点温度控制器
          sensors:
            - 室内温度
            - 室内湿度
            - 供水温度
          control: 提高供水温度高于露点
          
        location_hint:
          space_type: PANEL
          position: 控制柜
          
        control_points:
          sensors:
            - {point_id: DP_T, type: AI, description: 露点温度}
            - {point_id: ROOM_RH, type: AI, description: 室内湿度}
          commands:
            - {point_id: DP_CTRL, type: AO, description: 水温调节}

    sink_nodes:
    
      - node_id: HVAC-RADIANT_SNK_ROOM
        node_name: 辐射供暖制冷区域
        node_name_en: Radiant Conditioned Zone
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 辐射热/冷
        medium_in: ENERGY-THERMAL
        
        multiplicity: multiple
        
        typical_zones:
          - 门诊大厅
          - 候诊区
          - VIP病房
          
        location_hint:
          space_type: ROOM

  # ============================================================
  # 边定义
  # ============================================================
  edges:
  
    supply_edges:
    
      - edge_id: HVAC-RADIANT_EDGE_001
        edge_name: 冷热水至混水装置
        edge_type: TRK
        from_node: HVAC-RADIANT_SRC_CHW
        to_node: HVAC-RADIANT_DST_MIXING
        direction: unidirectional
        medium: WATER-CHW
        
      - edge_id: HVAC-RADIANT_EDGE_002
        edge_name: 混水至分集水器
        edge_type: TRK
        from_node: HVAC-RADIANT_DST_MIXING
        to_node: HVAC-RADIANT_DST_MANIFOLD
        direction: unidirectional
        medium: WATER-RADIANT
        
      - edge_id: HVAC-RADIANT_EDGE_003
        edge_name: 分集水器至地板盘管
        edge_type: BRH
        from_node: HVAC-RADIANT_DST_MANIFOLD
        to_node: HVAC-RADIANT_DST_FLOOR_LOOP
        direction: unidirectional
        medium: WATER-RADIANT
        
      - edge_id: HVAC-RADIANT_EDGE_004
        edge_name: 分集水器至天花辐射板
        edge_type: BRH
        from_node: HVAC-RADIANT_DST_MANIFOLD
        to_node: HVAC-RADIANT_DST_CEILING_PANEL
        direction: unidirectional
        medium: WATER-RADIANT

    thermal_edges:
    
      - edge_id: HVAC-RADIANT_EDGE_005
        edge_name: 地板辐射至房间
        edge_type: TRM
        from_node: HVAC-RADIANT_DST_FLOOR_LOOP
        to_node: HVAC-RADIANT_SNK_ROOM
        direction: unidirectional
        medium: ENERGY-THERMAL
        
      - edge_id: HVAC-RADIANT_EDGE_006
        edge_name: 天花辐射至房间
        edge_type: TRM
        from_node: HVAC-RADIANT_DST_CEILING_PANEL
        to_node: HVAC-RADIANT_SNK_ROOM
        direction: unidirectional
        medium: ENERGY-THERMAL

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:
  
    - path_id: HVAC-RADIANT_PATH_FLOOR
      path_name: 地板辐射路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: HVAC-RADIANT_SRC_HW}
        - {step: 2, element_type: node, element_id: HVAC-RADIANT_DST_MIXING}
        - {step: 3, element_type: node, element_id: HVAC-RADIANT_DST_MANIFOLD}
        - {step: 4, element_type: node, element_id: HVAC-RADIANT_DST_FLOOR_LOOP}
        - {step: 5, element_type: node, element_id: HVAC-RADIANT_SNK_ROOM}

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:
  
    water_temp_control:
      heating:
        setpoint: 根据室外温度调节（气候补偿）
        range: {value: "35-45", unit: ℃}
        
      cooling:
        setpoint: 露点温度 + 2℃
        range: {value: "16-20", unit: ℃}
        
    condensation_prevention:
      trigger: 供水温度 ≤ 露点温度 + 1℃
      action:
        - 提高供水温度
        - 降低室内湿度（配合新风除湿）
        - 必要时关闭辐射制冷
```

---

## 7.5 PLUMB-PURE 纯水系统拓扑

```yaml
System_Topology:

# ============================================================
# 系统标识
# ============================================================
identity:
 system_id: PLUMB-PURE
 system_name: 纯水系统
 system_name_en: Purified Water System
 category: PLUMBING
 priority: P3-OPTIONAL
 version: 1.0

 description: |
 医院纯化水系统，为中心供应室（CSSD）、制剂室、
 检验科等提供符合药典要求的纯化水。

 design_basis:
 quality: 中国药典纯化水标准
 conductivity: {value: "≤5.1", unit: μS/cm}
 TOC: {value: "≤500", unit: ppb}
 endotoxin: {value: "≤0.25", unit: EU/mL, note: 根据用途}

 serving_scope:
 - 中心供应室（CSSD）
 - 制剂室
 - 检验科
 - 病理科
 - 血透中心

# ============================================================
# 系统边界
# ============================================================
boundary:
 inputs:
 - boundary_id: PLUMB-PURE_BND_IN_WATER
 boundary_name: 市政自来水
 medium: WATER-DOMESTIC
 source_system: PLUMB-CW

 - boundary_id: PLUMB-PURE_BND_IN_ELEC
 boundary_name: 电源
 medium: ELEC-LV
 source_system: ELEC-LV-MAIN

 outputs:
 - boundary_id: PLUMB-PURE_BND_OUT_PW
 boundary_name: 纯化水
 medium: WATER-PURE
 target: 用水点

 - boundary_id: PLUMB-PURE_BND_OUT_DRAIN
 boundary_name: 浓水排放
 medium: WATER-WASTE
 target_system: PLUMB-SW

# ============================================================
# 节点定义
# ============================================================
nodes:

 source_nodes:

 - node_id: PLUMB-PURE_SRC_WATER
 node_name: 原水接口
 node_name_en: Raw Water Interface
 node_type: Source_Node
 node_category: SRC

 function: 市政水接入
 medium_out: WATER-DOMESTIC

 source_system: PLUMB-CW

 location_hint:
 space_type: MEP_ROOM
 room_name: 纯水站

 distribution_nodes:

 - node_id: PLUMB-PURE_DST_PRETREAT
 node_name: 预处理系统
 node_name_en: Pretreatment System
 node_type: Distribution_Node
 node_category: DST
 node_subtype: TRF

 function: 原水预处理
 medium_in: WATER-DOMESTIC
 medium_out: WATER-PRETREATED

 equipment_parameters:
 components:
 - 原水箱
 - 原水泵
 - 多介质过滤器
 - 活性炭过滤器
 - 软水器
 - 精密过滤器
 functions:
 - 去除悬浮物
 - 去除余氯
 - 去除硬度
 - 预过滤

 location_hint:
 space_type: MEP_ROOM
 room_name: 纯水站

 control_points:
 sensors:
 - {point_id: PRE_P, type: AI, description: 过滤器压差}
 - {point_id: PRE_CL, type: AI, description: 余氯}

 - node_id: PLUMB-PURE_DST_RO
 node_name: 反渗透系统
 node_name_en: Reverse Osmosis System
 node_type: Distribution_Node
 node_category: DST
 node_subtype: TRF

 function: 反渗透脱盐
 medium_in: WATER-PRETREATED
 medium_out: [WATER-RO, WATER-CONCENTRATE]

 equipment_parameters:
 type: 双级RO系统
 stages: 2级
 recovery: {value: 70-75, unit: "%"}
 rejection: {value: "≥99", unit: "%"}
 capacity: {value: 0.5-5, unit: m³/h}

 location_hint:
 space_type: MEP_ROOM
 room_name: 纯水站

 control_points:
 sensors:
 - {point_id: RO_COND_IN, type: AI, description: 进水电导率}
 - {point_id: RO_COND_OUT, type: AI, description: 产水电导率}
 - {point_id: RO_P_IN, type: AI, description: 进水压力}
 - {point_id: RO_Q, type: AI, description: 产水流量}
 status:
 - {point_id: RO_RUN, type: DI, description: 运行状态}
 - {point_id: RO_ALARM, type: DI, description: 故障报警}

 - node_id: PLUMB-PURE_DST_EDI
 node_name: EDI系统
 node_name_en: EDI System
 node_type: Distribution_Node
 node_category: DST
 node_subtype: TRF

 function: 电去离子深度处理
 medium_in: WATER-RO
 medium_out: WATER-PURE

 equipment_parameters:
 type: EDI电去离子装置
 conductivity_out: {value: "≤0.1", unit: μS/cm}
 resistivity: {value: "≥10", unit: MΩ·cm}

 location_hint:
 space_type: MEP_ROOM
 room_name: 纯水站

 control_points:
 sensors:
 - {point_id: EDI_COND, type: AI, description: 产水电导率}
 - {point_id: EDI_RES, type: AI, description: 电阻率}

 - node_id: PLUMB-PURE_DST_STORAGE
 node_name: 纯水储罐
 node_name_en: Purified Water Storage Tank
 node_type: Distribution_Node
 node_category: DST
 node_subtype: BUF

 function: 纯水储存
 medium_in: WATER-PURE
 medium_out: WATER-PURE

 equipment_parameters:
 type: 不锈钢储罐
 material: 316L不锈钢
 capacity: {value: 1-10, unit: m³}
 features:
 - 氮封保护
 - 呼吸器
 - 液位计
 - 喷淋球（CIP）

 location_hint:
 space_type: MEP_ROOM
 room_name: 纯水站

 control_points:
 sensors:
 - {point_id: TANK_LEVEL, type: AI, description: 液位}

 - node_id: PLUMB-PURE_DST_PUMP
 node_name: 纯水分配泵
 node_name_en: Distribution Pump
 node_type: Distribution_Node
 node_category: DST
 node_subtype: REG

 function: 纯水加压分配
 medium_in: WATER-PURE
 medium_out: WATER-PURE

 equipment_parameters:
 type: 不锈钢卫生泵
 material: 316L
 flow: {value: 2-10, unit: m³/h}
 head: {value: 20-40, unit: m}

 location_hint:
 space_type: MEP_ROOM
 room_name: 纯水站

 - node_id: PLUMB-PURE_DST_UV
 node_name: 紫外消毒器
 node_name_en: UV Sterilizer
 node_type: Distribution_Node
 node_category: DST
 node_subtype: TRF

 function: 紫外线杀菌
 medium_in: WATER-PURE
 medium_out: WATER-PURE

 equipment_parameters:
 type: 紫外线消毒器
 wavelength: {value: 254, unit: nm}
 dose: {value: "≥40", unit: mJ/cm²}
 material: 316L

 location_hint:
 space_type: MEP_ROOM
 room_name: 纯水站

 - node_id: PLUMB-PURE_DST_LOOP
 node_name: 纯水循环管路
 node_name_en: Purified Water Loop
 node_type: Distribution_Node
 node_category: DST
 node_subtype: TRK

 function: 纯水循环分配
 medium_in: WATER-PURE
 medium_out: WATER-PURE

 equipment_parameters:
 type: 循环管路系统
 material: 316L不锈钢
 welding: 自动焊接
 slope: {value: 0.5, unit: "%"}
 velocity: {value: 1-3, unit: m/s}
 features:
 - 循环回流
 - 无死角设计
 - 卫生级阀门

 location_hint:
 space_type: CEILING_VOID

 installation_requirements:
 - 倾斜坡度确保自排空
 - 最短支管长度
 - 卫生级连接

 - node_id: PLUMB-PURE_DST_TERMINAL
 node_name: 纯水取水点
 node_name_en: Purified Water Use Point
 node_type: Distribution_Node
 node_category: DST
 node_subtype: TRM

 function: 纯水取用
 medium_in: WATER-PURE
 medium_out: WATER-PURE

 multiplicity: multiple

 equipment_parameters:
 type: 卫生级取水阀
 material: 316L

 location_hint:
 space_type: WALL
 position: 使用区域墙面

 sink_nodes:

 - node_id: PLUMB-PURE_SNK_CSSD
 node_name: 中心供应室用水
 node_name_en: CSSD Use Point
 node_type: Sink_Node
 node_category: SNK

 consumption_type: CSSD清洗消毒
 medium_in: WATER-PURE

 equipment_parameters:
 applications:
 - 清洗消毒机
 - 超声清洗机
 - 手工清洗

 location_hint:
 space_type: ROOM
 room_name: 中心供应室

 - node_id: PLUMB-PURE_SNK_LAB
 node_name: 检验科用水
 node_name_en: Laboratory Use Point
 node_type: Sink_Node
 node_category: SNK

 consumption_type: 检验分析
 medium_in: WATER-PURE

 equipment_parameters:
 applications:
 - 生化分析仪
 - 试剂配制
 - 器皿冲洗

 location_hint:
 space_type: ROOM
 room_name: 检验科

 - node_id: PLUMB-PURE_SNK_DRAIN
 node_name: 浓水排放
 node_name_en: Concentrate Drain
 node_type: Sink_Node
 node_category: SNK

 consumption_type: 废水排放
 medium_in: WATER-CONCENTRATE

 target_system: PLUMB-SW

 location_hint:
 space_type: DRAIN
 position: 就近排水点

# ============================================================
# 边定义
# ============================================================
edges:

 treatment_edges:

 - edge_id: PLUMB-PURE_EDGE_001
 edge_name: 原水至预处理
 edge_type: TRK
 from_node: PLUMB-PURE_SRC_WATER
 to_node: PLUMB-PURE_DST_PRETREAT
 direction: unidirectional
 medium: WATER-DOMESTIC

 - edge_id: PLUMB-PURE_EDGE_002
 edge_name: 预处理至RO
 edge_type: TRK
 from_node: PLUMB-PURE_DST_PRETREAT
 to_node: PLUMB-PURE_DST_RO
 direction: unidirectional
 medium: WATER-PRETREATED

 - edge_id: PLUMB-PURE_EDGE_003
 edge_name: RO至EDI
 edge_type: TRK
 from_node: PLUMB-PURE_DST_RO
 to_node: PLUMB-PURE_DST_EDI
 direction: unidirectional
 medium: WATER-RO

 - edge_id: PLUMB-PURE_EDGE_004
 edge_name: EDI至储罐
 edge_type: TRK
 from_node: PLUMB-PURE_DST_EDI
 to_node: PLUMB-PURE_DST_STORAGE
 direction: unidirectional
 medium: WATER-PURE

 distribution_edges:

 - edge_id: PLUMB-PURE_EDGE_005
 edge_name: 储罐至分配泵
 edge_type: TRK
 from_node: PLUMB-PURE_DST_STORAGE
 to_node: PLUMB-PURE_DST_PUMP
 direction: unidirectional
 medium: WATER-PURE

 - edge_id: PLUMB-PURE_EDGE_006
 edge_name: 分配泵至UV
 edge_type: TRK
 from_node: PLUMB-PURE_DST_PUMP
 to_node: PLUMB-PURE_DST_UV
 direction: unidirectional
 medium: WATER-PURE

 - edge_id: PLUMB-PURE_EDGE_007
 edge_name: UV至循环管路
 edge_type: TRK
 from_node: PLUMB-PURE_DST_UV
 to_node: PLUMB-PURE_DST_LOOP
 direction: unidirectional
 medium: WATER-PURE

 - edge_id: PLUMB-PURE_EDGE_008
 edge_name: 循环管路至取水点
 edge_type: BRH
 from_node: PLUMB-PURE_DST_LOOP
 to_node: PLUMB-PURE_DST_TERMINAL
 direction: unidirectional
 medium: WATER-PURE

 - edge_id: PLUMB-PURE_EDGE_009
 edge_name: 取水点至CSSD
 edge_type: TRM
 from_node: PLUMB-PURE_DST_TERMINAL
 to_node: PLUMB-PURE_SNK_CSSD
 direction: unidirectional
 medium: WATER-PURE

 return_edge:

 - edge_id: PLUMB-PURE_EDGE_010
 edge_name: 循环回

---