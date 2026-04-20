## 🧑‍💻 User


第一就以上检查结论，你需要以如下方式完成补充：1、对已经完成的部分进行补充的（如Batch 1的hvac的补充），分别给出Batch 1补充文档、Batch 2补充文档和Batch 3补充文档；2、在Batch 1-3之外尚未提及的系统，新建Batch 4并进行完整的输出。

---
## 🤖 Assistant


# Agent-01 系统补充与扩展输出

## 概述

根据完整性审查报告，本文档包含两部分：
1. **Batch 1-3 补充文档**：对已完成系统的接口、节点、边进行补充
2. **Batch 4 完整输出**：新增缺失的关键系统

---

# 第一部分：Batch 1 补充文档 (HVAC系统补充)

## 1.1 HVAC-CHP 冷源系统补充

```yaml
System_Topology_Patch:

  system_id: HVAC-CHP
  patch_version: 1.1
  patch_description: 补充热水系统接口、冷热切换逻辑

  # ============================================================
  # 新增节点
  # ============================================================
  additional_nodes:
  
    distribution_nodes:
    
      - node_id: HVAC-CHP_DST_HW_INTERFACE
        node_name: 热水系统接口
        node_name_en: Hot Water System Interface
        node_type: Distribution_Node
        node_category: DST
        node_subtype: JUN
        
        function: 冷热水系统切换/混合接口
        medium_in: [WATER-CHW, WATER-HW]
        medium_out: WATER-CHW  # 统一为空调水
        
        equipment_parameters:
          type: 冷热水切换阀组
          configuration: 三通阀/两位切换
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 冷冻机房
          position: 分水器前端
          
        control_points:
          sensors:
            - {point_id: CHW_HW_T, type: AI, description: 切换后水温}
          status:
            - {point_id: CHW_HW_MODE, type: DI, description: 当前模式(冷/热)}
          commands:
            - {point_id: CHW_HW_SW, type: DO, description: 冷热切换命令}

  # ============================================================
  # 新增边
  # ============================================================
  additional_edges:
  
    - edge_id: HVAC-CHP_EDGE_HW_IN
      edge_name: 热水系统供水接入
      edge_type: TRK
      from_node: HVAC-HWP_DST_HEADER_SUP  # 引用热源系统
      to_node: HVAC-CHP_DST_HW_INTERFACE
      direction: unidirectional
      medium: WATER-HW
      cross_system: true
      target_system: HVAC-HWP
      
    - edge_id: HVAC-CHP_EDGE_HW_OUT
      edge_name: 热水系统回水返回
      edge_type: TRK
      from_node: HVAC-CHP_DST_HW_INTERFACE
      to_node: HVAC-HWP_DST_HEADER_RET  # 引用热源系统
      direction: unidirectional
      medium: WATER-HW
      cross_system: true
      target_system: HVAC-HWP
      
    - edge_id: HVAC-CHP_EDGE_HW_TO_HEADER
      edge_name: 热水接口至分水器
      edge_type: TRK
      from_node: HVAC-CHP_DST_HW_INTERFACE
      to_node: HVAC-CHP_DST_HEADER_SUP
      direction: unidirectional
      medium: WATER-CHW
      note: 冬季工况时热水经此边进入空调水系统

  # ============================================================
  # 补充控制逻辑
  # ============================================================
  additional_control_logic:
  
    seasonal_changeover:
      description: 冷热水季节切换逻辑
      
      cooling_mode:
        condition: 室外温度 > 18℃ 且 连续3天
        action:
          - 关闭热水系统接口阀门
          - 开启冷水机组
          - 切换至制冷模式
          
      heating_mode:
        condition: 室外温度 < 12℃ 且 连续3天
        action:
          - 关闭冷水机组
          - 开启热水系统接口阀门
          - 切换至供热模式
          
      transition_mode:
        condition: 室外温度 12-18℃
        action:
          - 根据建筑负荷需求切换
          - 可同时运行冷热源(不同区域)

  # ============================================================
  # 补充系统边界
  # ============================================================
  additional_boundary:
  
    inputs:
      - boundary_id: HVAC-CHP_BND_IN_HW
        boundary_name: 热水系统供水
        medium: WATER-HW
        source_system: HVAC-HWP
        parameters:
          temperature: {value: 50-60, unit: ℃}
          
    outputs:
      - boundary_id: HVAC-CHP_BND_OUT_HW
        boundary_name: 热水系统回水
        medium: WATER-HW
        target_system: HVAC-HWP
```

## 1.2 HVAC-AHU 空调风系统补充

```yaml
System_Topology_Patch:

  system_id: HVAC-AHU
  patch_version: 1.1
  patch_description: 补充再热盘管节点、热水接口、消防联动

  # ============================================================
  # 新增节点
  # ============================================================
  additional_nodes:
  
    distribution_nodes:
    
      - node_id: HVAC-AHU_DST_REHEAT_COIL
        node_name: 再热盘管
        node_name_en: Reheat Coil
        node_type: Distribution_Node
        node_category: DST
        node_subtype: HEX
        
        function: 送风再加热（冬季或除湿后再热）
        medium_in: [AIR-SA, WATER-HW]
        medium_out: AIR-SA
        
        multiplicity: optional
        note: 仅部分AHU配置再热盘管
        
        equipment_parameters:
          type: 热水盘管
          rows: {value: 2, unit: 排}
          water_velocity: {value: 0.8-1.2, unit: m/s}
          
        location_hint:
          space_type: AHU_INTERNAL
          position: 冷却盘管下游、加湿段上游
          
        control_points:
          sensors:
            - {point_id: RH_AIR_T_OUT, type: AI, description: 再热后空气温度}
            - {point_id: RH_WATER_T_IN, type: AI, description: 热水进水温度}
            - {point_id: RH_WATER_T_OUT, type: AI, description: 热水回水温度}
          commands:
            - {point_id: RH_VALVE, type: AO, description: 再热阀开度}
            
      - node_id: HVAC-AHU_DST_HW_VALVE
        node_name: 热水阀组
        node_name_en: Hot Water Valve Assembly
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 热水流量调节
        medium_in: WATER-HW
        medium_out: WATER-HW
        
        equipment_parameters:
          components:
            - 电动两通阀/三通阀
            - 平衡阀
            - 过滤器
            - 软接头
            
        location_hint:
          space_type: MEP_ROOM
          position: 空调机房热水管道

    sink_nodes:
    
      - node_id: HVAC-AHU_SNK_FIRE_INTERLOCK
        node_name: 消防联动接口
        node_name_en: Fire Interlock Interface
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 联动控制信号
        medium_in: SIGNAL-FA
        
        interface_system: FIRE-ALARM
        
        function: 接收火灾报警信号，执行停机/关阀
        
        location_hint:
          space_type: PANEL
          position: AHU控制柜

  # ============================================================
  # 新增边
  # ============================================================
  additional_edges:
  
    hot_water_edges:
    
      - edge_id: HVAC-AHU_EDGE_HW_SUP
        edge_name: 热水供水至阀组
        edge_type: TRK
        from_node: HVAC-HWP_DST_AHU_BRANCH  # 热源系统分支
        to_node: HVAC-AHU_DST_HW_VALVE
        direction: unidirectional
        medium: WATER-HW
        cross_system: true
        target_system: HVAC-HWP
        
      - edge_id: HVAC-AHU_EDGE_HW_COIL
        edge_name: 阀组至再热盘管
        edge_type: TRK
        from_node: HVAC-AHU_DST_HW_VALVE
        to_node: HVAC-AHU_DST_REHEAT_COIL
        direction: unidirectional
        medium: WATER-HW
        
      - edge_id: HVAC-AHU_EDGE_HW_RET
        edge_name: 再热盘管回水
        edge_type: TRK
        from_node: HVAC-AHU_DST_REHEAT_COIL
        to_node: HVAC-HWP_DST_AHU_BRANCH  # 热源系统回水
        direction: unidirectional
        medium: WATER-HW
        cross_system: true
        target_system: HVAC-HWP

    fire_interlock_edges:
    
      - edge_id: HVAC-AHU_EDGE_FIRE_SIG
        edge_name: 消防联动信号
        edge_type: CTRL
        from_node: FIRE-ALARM_DST_LINKAGE
        to_node: HVAC-AHU_SNK_FIRE_INTERLOCK
        direction: unidirectional
        medium: SIGNAL-FA
        cross_system: true
        source_system: FIRE-ALARM

  # ============================================================
  # 补充典型路径
  # ============================================================
  additional_paths:
  
    - path_id: HVAC-AHU_PATH_REHEAT
      path_name: 再热工况送风路径
      path_type: SUP
      condition: 冬季或除湿后再热
      sequence:
        - {step: 1, element_type: node, element_id: HVAC-AHU_SRC_OA}
        - {step: 2, element_type: node, element_id: HVAC-AHU_DST_FILTER}
        - {step: 3, element_type: node, element_id: HVAC-AHU_DST_COOL_COIL}
        - {step: 4, element_type: node, element_id: HVAC-AHU_DST_REHEAT_COIL}  # 新增
        - {step: 5, element_type: node, element_id: HVAC-AHU_DST_HUM}
        - {step: 6, element_type: node, element_id: HVAC-AHU_DST_FAN}
        - {step: 7, element_type: node, element_id: HVAC-AHU_SNK_ROOM}

  # ============================================================
  # 补充控制逻辑
  # ============================================================
  additional_control_logic:
  
    reheat_control:
      mode: 温度控制
      setpoint: 送风温度设定值
      control_method: PID调节再热阀开度
      
      sequence:
        winter:
          - 冷却盘管关闭或微开除湿
          - 再热盘管开启
          - 根据送风温度调节阀开度
          
        dehumidification:
          - 冷却盘管开启除湿
          - 再热盘管开启
          - 先冷却除湿，后再热升温
          
    fire_interlock:
      trigger: FIRE-ALARM火灾确认信号
      action:
        - AHU风机停止
        - 新风阀关闭
        - 回风阀关闭
        - 冷热水阀关闭
      priority: 最高优先级
      restore: 仅手动复位

  # ============================================================
  # 补充系统边界
  # ============================================================
  additional_boundary:
  
    inputs:
      - boundary_id: HVAC-AHU_BND_IN_HW
        boundary_name: 热水供水
        medium: WATER-HW
        source_system: HVAC-HWP
        parameters:
          temperature: {value: 50-60, unit: ℃}
          
      - boundary_id: HVAC-AHU_BND_IN_FA
        boundary_name: 消防联动信号
        medium: SIGNAL-FA
        source_system: FIRE-ALARM
```

## 1.3 HVAC-CLEAN 洁净空调系统补充

```yaml
System_Topology_Patch:

  system_id: HVAC-CLEAN
  patch_version: 1.1
  patch_description: 补充加热盘管热水接口、消防联动、麻醉废气排放接口

  # ============================================================
  # 新增节点
  # ============================================================
  additional_nodes:
  
    distribution_nodes:
    
      - node_id: HVAC-CLEAN_DST_HEAT_COIL
        node_name: 加热盘管
        node_name_en: Heating Coil
        node_type: Distribution_Node
        node_category: DST
        node_subtype: HEX
        
        function: 冬季预热/再热
        medium_in: [AIR-MA, WATER-HW]
        medium_out: AIR-MA
        
        equipment_parameters:
          type: 热水盘管
          rows: {value: 2-4, unit: 排}
          capacity: 根据热负荷计算
          
        location_hint:
          space_type: AHU_INTERNAL
          position: 表冷器下游或新风预热位置
          
        control_points:
          sensors:
            - {point_id: HEAT_AIR_T_OUT, type: AI, description: 加热后温度}
          commands:
            - {point_id: HEAT_VALVE, type: AO, description: 热水阀开度}

      - node_id: HVAC-CLEAN_DST_AGSS_INTERFACE
        node_name: 麻醉废气排放接口
        node_name_en: AGSS Interface
        node_type: Distribution_Node
        node_category: DST
        node_subtype: JUN
        
        function: 麻醉废气接入排风系统
        medium_in: GAS-AGSS
        medium_out: AIR-EA
        
        equipment_parameters:
          type: 接口管道
          dilution_ratio: 1:10 (废气:排风)
          
        location_hint:
          space_type: CEILING_VOID
          position: 手术室排风主管接口处
          
        interface_system: MGAS-AGSS

    sink_nodes:
    
      - node_id: HVAC-CLEAN_SNK_FIRE_INTERLOCK
        node_name: 消防联动接口
        node_name_en: Fire Interlock Interface
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 联动控制信号
        medium_in: SIGNAL-FA
        
        interface_system: FIRE-ALARM
        
        location_hint:
          space_type: PANEL
          position: 净化空调控制柜

  # ============================================================
  # 新增边
  # ============================================================
  additional_edges:
  
    hot_water_edges:
    
      - edge_id: HVAC-CLEAN_EDGE_HW_SUP
        edge_name: 热水供水
        edge_type: TRK
        from_node: HVAC-HWP_DST_CLEAN_BRANCH
        to_node: HVAC-CLEAN_DST_HEAT_COIL
        direction: unidirectional
        medium: WATER-HW
        cross_system: true
        target_system: HVAC-HWP
        
      - edge_id: HVAC-CLEAN_EDGE_HW_RET
        edge_name: 热水回水
        edge_type: TRK
        from_node: HVAC-CLEAN_DST_HEAT_COIL
        to_node: HVAC-HWP_DST_CLEAN_BRANCH
        direction: unidirectional
        medium: WATER-HW
        cross_system: true
        target_system: HVAC-HWP

    agss_edges:
    
      - edge_id: HVAC-CLEAN_EDGE_AGSS_IN
        edge_name: 麻醉废气接入
        edge_type: BRH
        from_node: MGAS-AGSS_DST_MAIN_PIPE
        to_node: HVAC-CLEAN_DST_AGSS_INTERFACE
        direction: unidirectional
        medium: GAS-AGSS
        cross_system: true
        source_system: MGAS-AGSS
        
      - edge_id: HVAC-CLEAN_EDGE_AGSS_OUT
        edge_name: 麻醉废气排放
        edge_type: TRK
        from_node: HVAC-CLEAN_DST_AGSS_INTERFACE
        to_node: HVAC-CLEAN_DST_EA_MAIN
        direction: unidirectional
        medium: AIR-EA
        note: 废气稀释后经排风主管排放

    fire_interlock_edges:
    
      - edge_id: HVAC-CLEAN_EDGE_FIRE_SIG
        edge_name: 消防联动信号
        edge_type: CTRL
        from_node: FIRE-ALARM_DST_LINKAGE
        to_node: HVAC-CLEAN_SNK_FIRE_INTERLOCK
        direction: unidirectional
        medium: SIGNAL-FA
        cross_system: true
        source_system: FIRE-ALARM

  # ============================================================
  # 补充控制逻辑
  # ============================================================
  additional_control_logic:
  
    heating_control:
      mode: 温度控制
      winter_preheat:
        condition: 新风温度 < 5℃
        action: 新风预热阀开启
        setpoint: 混合空气温度 ≥ 12℃
        
      reheat:
        condition: 除湿后或冬季
        action: 再热阀开启
        setpoint: 送风温度设定值
        
    agss_coordination:
      description: 麻醉废气与排风协调
      requirements:
        - 排风量 ≥ 10倍AGSS流量
        - 排风机运行时AGSS方可排放
        - AGSS压力监测
        
    fire_interlock:
      trigger: FIRE-ALARM火灾确认信号
      action:
        - 送风机停止
        - 排风机停止
        - 新风阀关闭
        - 排风阀关闭
        - AGSS接口阀关闭
      special_note: |
        手术进行中火灾时的特殊处理：
        1. 优先患者安全转移
        2. 净化系统可延迟关闭（30-60秒）
        3. 需与医疗流程协调
      restore: 仅手动复位
```

## 1.4 HVAC系统补充 - 新增介质类型

```yaml
Additional_Medium_Types:

  - medium_id: WATER-HW
    medium_name: 空调热水
    medium_name_en: HVAC Hot Water
    category: WATER
    typical_properties:
      temperature_supply: {value: 50-60, unit: ℃}
      temperature_return: {value: 40-50, unit: ℃}
      pressure: {value: 0.4-0.8, unit: MPa}
      delta_t: {value: 10-15, unit: ℃}
```

---

# 第二部分：Batch 2 补充文档 (电气/医疗气体系统补充)

## 2.1 ELEC-LV-MAIN 低压主配电系统补充

```yaml
System_Topology_Patch:

  system_id: ELEC-LV-MAIN
  patch_version: 1.1
  patch_description: 补充楼层配电详细节点、UPS接口、照明接口

  # ============================================================
  # 新增节点
  # ============================================================
  additional_nodes:
  
    distribution_nodes:
    
      - node_id: ELEC-LV_DST_FLOOR_MDB
        node_name: 楼层总配电箱
        node_name_en: Floor Main Distribution Board
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
        
        function: 楼层配电总控
        medium_in: ELEC-LV
        medium_out: ELEC-LV
        
        multiplicity: multiple
        instance_pattern: ELEC-LV_DST_FLOOR_MDB_{Bldg}_{Floor}
        
        equipment_parameters:
          type: 配电箱
          rated_current: {value: 400-630, unit: A}
          circuits: {value: 20-40, unit: 回路}
          metering: 分项计量
          
        location_hint:
          space_type: SHAFT
          shaft_type: 电气竖井
          position: 每层核心筒
          
        control_points:
          sensors:
            - {point_id: FLOOR_V, type: AI, description: 电压}
            - {point_id: FLOOR_I, type: AI, description: 电流}
            - {point_id: FLOOR_P, type: AI, description: 功率}
            - {point_id: FLOOR_KWH, type: AI, description: 电能}
          status:
            - {point_id: FLOOR_TRIP, type: DI, description: 跳闸报警}

      - node_id: ELEC-LV_DST_AREA_DB
        node_name: 区域配电箱
        node_name_en: Area Distribution Board
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
        
        function: 功能区域配电
        medium_in: ELEC-LV
        medium_out: ELEC-LV
        
        multiplicity: multiple
        instance_pattern: ELEC-LV_DST_AREA_DB_{Floor}_{Area}
        
        equipment_parameters:
          type: 配电箱
          rated_current: {value: 100-250, unit: A}
          
        location_hint:
          space_type: WALL_BOX
          position: 各功能区域入口

      - node_id: ELEC-LV_DST_UPS_FEED
        node_name: UPS馈电柜
        node_name_en: UPS Feeder Panel
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 向UPS系统馈电
        medium_in: ELEC-LV
        medium_out: ELEC-LV
        
        equipment_parameters:
          type: 低压开关柜
          rated_current: {value: 400-800, unit: A}
          
        location_hint:
          space_type: MEP_ROOM
          room_name: UPS机房/低压配电室
          
        interface_system: ELEC-UPS

      - node_id: ELEC-LV_DST_LIGHT_FEED
        node_name: 照明馈电柜
        node_name_en: Lighting Feeder Panel
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
        
        function: 照明系统总配电
        medium_in: ELEC-LV
        medium_out: ELEC-LV
        
        equipment_parameters:
          type: 低压开关柜
          circuits: 
            - 普通照明
            - 应急照明
            - 疏散指示
            
        location_hint:
          space_type: MEP_ROOM
          room_name: 低压配电室
          
        interface_system: ELEC-LIGHT

    sink_nodes:
    
      - node_id: ELEC-LV_SNK_TERMINAL
        node_name: 终端用电点
        node_name_en: Terminal Load
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 电力消耗
        medium_in: ELEC-LV
        
        multiplicity: multiple
        
        equipment_parameters:
          types:
            - 插座
            - 设备直接供电
            - 照明灯具

  # ============================================================
  # 新增边
  # ============================================================
  additional_edges:
  
    - edge_id: ELEC-LV_EDGE_TO_FLOOR
      edge_name: 馈电柜至楼层配电
      edge_type: TRK
      from_node: ELEC-LV_DST_FEEDER_NORMAL
      to_node: ELEC-LV_DST_FLOOR_MDB
      direction: unidirectional
      medium: ELEC-LV
      physical_properties:
        cable_type: YJV
        routing: 电气竖井
        
    - edge_id: ELEC-LV_EDGE_TO_AREA
      edge_name: 楼层配电至区域
      edge_type: BRH
      from_node: ELEC-LV_DST_FLOOR_MDB
      to_node: ELEC-LV_DST_AREA_DB
      direction: unidirectional
      medium: ELEC-LV
      physical_properties:
        cable_type: YJV
        routing: 走廊桥架
        
    - edge_id: ELEC-LV_EDGE_TO_UPS
      edge_name: 至UPS馈电
      edge_type: TRK
      from_node: ELEC-LV_DST_FEEDER_CRITICAL
      to_node: ELEC-LV_DST_UPS_FEED
      direction: unidirectional
      medium: ELEC-LV
      
    - edge_id: ELEC-LV_EDGE_TO_LIGHT
      edge_name: 至照明馈电
      edge_type: TRK
      from_node: ELEC-LV_DST_BUS1
      to_node: ELEC-LV_DST_LIGHT_FEED
      direction: unidirectional
      medium: ELEC-LV

  # ============================================================
  # 补充系统边界
  # ============================================================
  additional_boundary:
  
    outputs:
      - boundary_id: ELEC-LV_BND_OUT_UPS
        boundary_name: UPS系统供电
        medium: ELEC-LV
        target_system: ELEC-UPS
        
      - boundary_id: ELEC-LV_BND_OUT_LIGHT
        boundary_name: 照明系统供电
        medium: ELEC-LV
        target_system: ELEC-LIGHT
```

## 2.2 ELEC-EPS 应急电源系统补充

```yaml
System_Topology_Patch:

  system_id: ELEC-EPS
  patch_version: 1.1
  patch_description: 补充柴油储罐安全要求、巡检要求

  # ============================================================
  # 节点属性补充
  # ============================================================
  node_patches:
  
    - node_id: ELEC-EPS_SRC_FUEL_TANK
      additional_properties:
        
        safety_requirements:
          fire_protection:
            - 储油间防火分隔（耐火极限2h）
            - 配置灭火器
            - 禁止明火标识
          spill_control:
            - 设置围堰/集油坑
            - 容积≥储罐容量110%
            - 防渗漏材料
          ventilation:
            - 机械通风
            - 换气次数≥6次/h
            - 防爆风机
          leak_detection:
            - 油位监测
            - 漏油传感器
            - 报警至消防控制室
            
        maintenance_requirements:
          inspection:
            frequency: 每周
            items:
              - 油位检查
              - 泄漏检查
              - 通气管检查
              - 阀门状态
          fuel_replacement:
            frequency: 每6个月
            reason: 柴油存放过久品质下降

      additional_control_points:
        sensors:
          - {point_id: FUEL_LEVEL, type: AI, description: 油位}
          - {point_id: FUEL_LEAK, type: DI, description: 漏油检测}
        status:
          - {point_id: FUEL_LOW, type: DI, description: 低油位报警}
          - {point_id: FUEL_HIGH, type: DI, description: 高油位报警}

  # ============================================================
  # 新增节点 - 室外储油罐（大容量备用）
  # ============================================================
  additional_nodes:
  
    source_nodes:
    
      - node_id: ELEC-EPS_SRC_MAIN_TANK
        node_name: 室外储油罐
        node_name_en: Outdoor Fuel Storage Tank
        node_type: Source_Node
        node_category: SRC
        
        function: 大容量柴油储存
        medium_out: FUEL-DIESEL
        
        equipment_parameters:
          capacity: {value: 10000-30000, unit: L}
          type: 地上/地下卧式储罐
          material: 双层钢制
          
        location_hint:
          space_type: OUTDOOR
          position: 室外独立储罐区
          
        installation_requirements:
          - 防火间距≥12m
          - 防雷接地
          - 围堰
          - 消防设施
          - 卸油接口
          - 液位计量
          
        control_points:
          sensors:
            - {point_id: MAIN_TANK_LEVEL, type: AI, description: 主罐油位}
          status:
            - {point_id: MAIN_TANK_LOW, type: DI, description: 低油位}

  additional_edges:
  
    - edge_id: ELEC-EPS_EDGE_MAIN_TO_DAY
      edge_name: 主油罐至日用油箱
      edge_type: TRK
      from_node: ELEC-EPS_SRC_MAIN_TANK
      to_node: ELEC-EPS_SRC_FUEL_TANK
      direction: unidirectional
      medium: FUEL-DIESEL
      physical_properties:
        pipe_material: 无缝钢管
        
  # ============================================================
  # 补充控制逻辑
  # ============================================================
  additional_control_logic:
  
    fuel_transfer:
      description: 主油罐至日用油箱自动补油
      trigger: 日用油箱液位 < 50%
      action: 启动输油泵
      stop: 日用油箱液位 > 90%
      
    low_fuel_alarm:
      level_1:
        condition: 日用油箱 < 30%
        action: 报警提示
      level_2:
        condition: 日用油箱 < 15%
        action: 紧急报警+通知维护
```

## 2.3 MGAS系统补充 - 终端设备带/吊塔接口

```yaml
System_Topology_Patch:

  system_id: MGAS-O2
  patch_version: 1.1
  patch_description: 补充设备带/吊塔终端汇聚节点

  # ============================================================
  # 新增节点
  # ============================================================
  additional_nodes:
  
    sink_nodes:
    
      - node_id: MGAS-O2_SNK_HEADWALL
        node_name: 床头设备带
        node_name_en: Headwall Unit
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 医疗气体终端集成
        medium_in: [GAS-O2, GAS-VAC, GAS-AIR]
        
        multiplicity: multiple
        instance_pattern: MGAS-O2_SNK_HEADWALL_{Floor}_{Room}_{Bed}
        
        equipment_parameters:
          type: 床头设备带
          integrated_services:
            - 医用氧气终端
            - 负压吸引终端
            - 压缩空气终端
            - 电源插座
            - 网络接口
            - 护理呼叫
            - 阅读灯
          terminal_per_bed:
            O2: 1
            VAC: 1
            AIR: 1 (部分)
            
        location_hint:
          space_type: WALL
          position: 病床床头
          height: {value: 1.2-1.5, unit: m}
          
      - node_id: MGAS-O2_SNK_PENDANT
        node_name: 手术室吊塔
        node_name_en: OR Ceiling Pendant
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 手术室医疗气体终端集成
        medium_in: [GAS-O2, GAS-VAC, GAS-AIR, GAS-N2O, GAS-CO2, GAS-AGSS]
        
        multiplicity: multiple
        instance_pattern: MGAS-O2_SNK_PENDANT_OR{NN}_{Side}
        
        equipment_parameters:
          type: 手术吊塔
          configuration: 双吊塔/三吊塔
          integrated_services:
            - 医用氧气终端 ×2-4
            - 负压吸引终端 ×2-3
            - 压缩空气终端 ×2
            - 笑气终端 ×1
            - CO2终端 ×1 (腔镜室)
            - 麻醉废气收集 ×2
            - 电源插座 (多规格)
            - 网络接口
            - 设备挂载
            
        location_hint:
          space_type: CEILING
          position: 手术床两侧
          height: 可升降

---
# 同样为MGAS-VAC和MGAS-AIR添加设备带/吊塔终端引用
System_Topology_Patch:

  system_id: MGAS-VAC
  patch_version: 1.1
  
  additional_boundary:
    outputs:
      - boundary_id: MGAS-VAC_BND_OUT_HEADWALL
        boundary_name: 床头设备带终端
        medium: GAS-VAC
        target_node: MGAS-O2_SNK_HEADWALL
        note: 与O2共用设备带节点
        
      - boundary_id: MGAS-VAC_BND_OUT_PENDANT
        boundary_name: 手术室吊塔终端
        medium: GAS-VAC
        target_node: MGAS-O2_SNK_PENDANT
        note: 与O2共用吊塔节点

---
System_Topology_Patch:

  system_id: MGAS-AIR
  patch_version: 1.1
  
  additional_boundary:
    outputs:
      - boundary_id: MGAS-AIR_BND_OUT_HEADWALL
        boundary_name: 床头设备带终端
        medium: GAS-AIR
        target_node: MGAS-O2_SNK_HEADWALL
        
      - boundary_id: MGAS-AIR_BND_OUT_PENDANT
        boundary_name: 手术室吊塔终端
        medium: GAS-AIR
        target_node: MGAS-O2_SNK_PENDANT
```

---

# 第三部分：Batch 3 补充文档 (给排水/消防/智能化补充)

## 3.1 PLUMB-DWS 生活给水系统补充

```yaml
System_Topology_Patch:

  system_id: PLUMB-DWS
  patch_version: 1.1
  patch_description: 补充水质监测点位、热水系统接口

  # ============================================================
  # 节点属性补充
  # ============================================================
  node_patches:
  
    - node_id: PLUMB-DWS_DST_TANK
      additional_control_points:
        sensors:
          - {point_id: TANK_CL, type: AI, description: 余氯}
          - {point_id: TANK_TURB, type: AI, description: 浊度}
          - {point_id: TANK_PH, type: AI, description: pH值}
        status:
          - {point_id: TANK_CL_LOW, type: DI, description: 余氯过低报警}
          - {point_id: TANK_TURB_HIGH, type: DI, description: 浊度超标报警}
          
    - node_id: PLUMB-DWS_DST_PUMP_SET
      additional_control_points:
        sensors:
          - {point_id: PUMP_Q, type: AI, description: 瞬时流量}
          - {point_id: PUMP_Q_TOT, type: AI, description: 累计流量}

  # ============================================================
  # 新增节点
  # ============================================================
  additional_nodes:
  
    distribution_nodes:
    
      - node_id: PLUMB-DWS_DST_HWS_FEED
        node_name: 热水系统供水点
        node_name_en: HWS Feed Point
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BRH
        
        function: 向热水系统供应冷水
        medium_in: WATER-DW
        medium_out: WATER-DW
        
        equipment_parameters:
          components:
            - 截止阀
            - 止回阀
            - 压力表
            
        location_hint:
          space_type: MEP_ROOM
          room_name: 热水机房
          
        interface_system: PLUMB-HWS

      - node_id: PLUMB-DWS_DST_FIRE_MAKEUP
        node_name: 消防水池补水点
        node_name_en: Fire Pool Makeup Point
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BRH
        
        function: 消防水池补水
        medium_in: WATER-DW
        medium_out: WATER-DW
        
        equipment_parameters:
          type: 自动补水阀
          control: 液位控制
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 消防水池
          
        interface_system: FIRE-HYDRANT

  # ============================================================
  # 新增边
  # ============================================================
  additional_edges:
  
    - edge_id: PLUMB-DWS_EDGE_TO_HWS
      edge_name: 至热水系统
      edge_type: BRH
      from_node: PLUMB-DWS_DST_MAIN_SUP
      to_node: PLUMB-DWS_DST_HWS_FEED
      direction: unidirectional
      medium: WATER-DW
      cross_system: true
      target_system: PLUMB-HWS
      
    - edge_id: PLUMB-DWS_EDGE_TO_FIRE
      edge_name: 至消防水池
      edge_type: BRH
      from_node: PLUMB-DWS_SRC_MUNI
      to_node: PLUMB-DWS_DST_FIRE_MAKEUP
      direction: unidirectional
      medium: WATER-DW
      cross_system: true
      target_system: FIRE-HYDRANT

  # ============================================================
  # 补充系统边界
  # ============================================================
  additional_boundary:
  
    outputs:
      - boundary_id: PLUMB-DWS_BND_OUT_HWS
        boundary_name: 热水系统冷水供应
        medium: WATER-DW
        target_system: PLUMB-HWS
        
      - boundary_id: PLUMB-DWS_BND_OUT_FIRE_MAKEUP
        boundary_name: 消防水池补水
        medium: WATER-DW
        target_system: FIRE-HYDRANT
```

## 3.2 PLUMB-PWS 纯水系统补充

```yaml
System_Topology_Patch:

  system_id: PLUMB-PWS
  patch_version: 1.1
  patch_description: 补充在线监测点位

  # ============================================================
  # 节点属性补充
  # ============================================================
  node_patches:
  
    - node_id: PLUMB-PWS_DST_STORAGE
      additional_control_points:
        sensors:
          - {point_id: TANK_BACTERIA, type: AI, description: 细菌监测(在线)}
          - {point_id: TANK_ENDOTOXIN, type: AI, description: 内毒素监测}
        note: 在线细菌监测或定期取样检测
        
    - node_id: PLUMB-PWS_DST_LOOP
      additional_control_points:
        sensors:
          - {point_id: LOOP_COND, type: AI, description: 循环管网电导率}
          - {point_id: LOOP_TOC, type: AI, description: 循环管网TOC}
          - {point_id: LOOP_TEMP, type: AI, description: 循环水温}
          - {point_id: LOOP_FLOW, type: AI, description: 循环流量}
        monitoring_points:
          - 供水端
          - 回水端
          - 最远端

  # ============================================================
  # 新增节点 - 消毒/灭菌
  # ============================================================
  additional_nodes:
  
    distribution_nodes:
    
      - node_id: PLUMB-PWS_DST_SANITIZE
        node_name: 消毒系统
        node_name_en: Sanitization System
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
        
        function: 系统定期消毒/灭菌
        medium_in: WATER-PW
        medium_out: WATER-PW
        
        equipment_parameters:
          methods:
            - {type: 热水消毒, temp: 80-85℃, duration: 1h}
            - {type: 臭氧消毒, concentration: 0.5ppm, duration: 2h}
            - {type: 化学消毒, agent: 过氧化氢, concentration: 500ppm}
          frequency: 每周/每月
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 纯水机房
          
  # ============================================================
  # 补充控制逻辑
  # ============================================================
  additional_control_logic:
  
    water_quality_alarm:
      conductivity:
        warning: {value: 1.5, unit: μS/cm}
        alarm: {value: 2.0, unit: μS/cm}
        action: 停止供水、检查RO/EDI
        
      toc:
        warning: {value: 400, unit: ppb}
        alarm: {value: 500, unit: ppb}
        
      bacteria:
        limit: {value: 10, unit: CFU/100mL}
        action: 消毒处理
        
    sanitization_schedule:
      hot_water_sanitization:
        frequency: 每周
        duration: {value: 1, unit: h}
        temperature: {value: 80-85, unit: ℃}
        
      ozone_sanitization:
        frequency: 每月
        duration: {value: 2, unit: h}
```

## 3.3 FIRE-ALARM 火灾报警系统补充

```yaml
System_Topology_Patch:

  system_id: FIRE-ALARM
  patch_version: 1.1
  patch_description: 补充与HVAC-SMOKE、ELEC-LIGHT、INT-PA的联动

  # ============================================================
  # 新增边（联动边）
  # ============================================================
  additional_edges:
  
    linkage_edges:
    
      - edge_id: FIRE-ALARM_EDGE_TO_SMOKE
        edge_name: 联动防排烟系统
        edge_type: CTRL
        from_node: FIRE-ALARM_DST_LINKAGE
        to_node: HVAC-SMOKE_DST_CONTROL  # 引用防排烟系统
        direction: unidirectional
        medium: SIGNAL-FA
        cross_system: true
        target_system: HVAC-SMOKE
        
      - edge_id: FIRE-ALARM_EDGE_TO_LIGHT
        edge_name: 联动应急照明
        edge_type: CTRL
        from_node: FIRE-ALARM_DST_LINKAGE
        to_node: ELEC-LIGHT_DST_EMERGENCY  # 引用照明系统
        direction: unidirectional
        medium: SIGNAL-FA
        cross_system: true
        target_system: ELEC-LIGHT
        
      - edge_id: FIRE-ALARM_EDGE_TO_PA
        edge_name: 联动消防广播
        edge_type: CTRL
        from_node: FIRE-ALARM_DST_LINKAGE
        to_node: INT-PA_DST_FIRE_CHANNEL  # 引用公共广播系统
        direction: unidirectional
        medium: SIGNAL-FA
        cross_system: true
        target_system: INT-PA
        
      - edge_id: FIRE-ALARM_EDGE_TO_ELEVATOR
        edge_name: 联动电梯迫降
        edge_type: CTRL
        from_node: FIRE-ALARM_DST_LINKAGE
        to_node: ELEVATOR_FIRE_RETURN  # 电梯系统
        direction: unidirectional
        medium: SIGNAL-FA
        cross_system: true
        target_system: ELEVATOR
        
      - edge_id: FIRE-ALARM_EDGE_TO_ACCESS
        edge_name: 联动门禁释放
        edge_type: CTRL
        from_node: FIRE-ALARM_DST_LINKAGE
        to_node: INT-SEC_DST_ACCESS  # 安防系统门禁
        direction: unidirectional
        medium: SIGNAL-FA
        cross_system: true
        target_system: INT-SEC

  # ============================================================
  # 补充联动逻辑
  # ============================================================
  additional_linkage_logic:
  
    smoke_control_linkage:
      trigger: 防烟分区火灾确认
      actions:
        - open: 该区域排烟口
        - start: 排烟风机
        - open: 补风口（如有）
        - start: 补风机（如有）
        - close: 防火阀（火灾蔓延时）
      feedback: 排烟风机运行状态
      
    pressurization_linkage:
      trigger: 疏散楼梯间/前室火灾确认
      actions:
        - open: 正压送风口
        - start: 正压送风机
      pressure_target: {value: 25-50, unit: Pa}
      
    emergency_lighting_linkage:
      trigger: 火灾确认或市电断电
      actions:
        - switch: 应急照明切换至备用电源
        - illuminate: 疏散指示灯
        - timing: 持续时间≥90min
        
    pa_linkage:
      trigger: 火灾确认
      actions:
        - override: 接管背景音乐
        - broadcast: 火灾疏散语音
        - mode: 分区域顺序广播
      priority: 消防广播最高优先级
      
    access_linkage:
      trigger: 火灾确认
      actions:
        - release: 疏散通道门禁
        - unlock: 常闭防火门（疏散用）
        - record: 保持门禁记录
```

## 3.4 INT-BA 楼宇自动化系统补充

```yaml
System_Topology_Patch:

  system_id: INT-BA
  patch_version: 1.1
  patch_description: 补充与INT-NET的物理层接口、扩展监控范围

  # ============================================================
  # 新增节点
  # ============================================================
  additional_nodes:
  
    distribution_nodes:
    
      - node_id: INT-BA_DST_NETWORK_INTERFACE
        node_name: 网络基础设施接口
        node_name_en: Network Infrastructure Interface
        node_type: Distribution_Node
        node_category: DST
        node_subtype: JUN
        
        function: BA系统网络接入点
        medium_in: DATA-IP
        medium_out: DATA-IP
        
        equipment_parameters:
          type: 网络接口模块
          isolation: BA专网/VLAN隔离
          
        location_hint:
          space_type: RACK
          room_name: 弱电机房
          
        interface_system: INT-NET

  # ============================================================
  # 补充监控范围
  # ============================================================
  additional_monitoring_scope:
  
    hvac_additions:
      - system: HVAC-HWP
        points: [锅炉/热泵状态, 热水温度, 泵状态, 能耗]
        priority: 新增后补充
        
      - system: HVAC-FCU
        points: [风机状态, 阀门开度, 室温]
        priority: 新增后补充
        
      - system: HVAC-SMOKE
        points: [风机状态, 风阀状态, 压差]
        priority: 新增后补充
        
    plumbing_additions:
      - system: PLUMB-HWS
        points: [热水温度, 回水温度, 循环泵状态]
        priority: 新增后补充
        
    electrical_additions:
      - system: ELEC-UPS
        points: [输入电压, 输出电压, 电池电量, 运行状态]
        priority: 新增后补充
        
    medical_gas_additions:
      - system: MGAS-O2
        points: [液位, 压力, 气源状态]
        integration: 通过独立医气监控系统接入
        
      - system: MGAS-VAC
        points: [真空度, 泵状态]
        
      - system: MGAS-AIR
        points: [压力, 露点, 空压机状态]

  # ============================================================
  # 补充系统边界
  # ============================================================
  additional_boundary:
  
    inputs:
      - boundary_id: INT-BA_BND_IN_NET
        boundary_name: 网络基础设施
        medium: DATA-IP
        source_system: INT-NET
        
    outputs:
      - boundary_id: INT-BA_BND_OUT_IBMS
        boundary_name: 集成平台接口
        medium: DATA-IP
        target_system: INT-IBMS
        protocol: BACnet/IP, OPC-UA
```

---

# 第四部分：Batch 4 完整输出 - 新增系统

## Batch 4 系统清单

```yaml
Batch_4_Systems:
  
  - HVAC-HWP: 热源系统
  - HVAC-SMOKE: 防排烟系统  
  - PLUMB-HWS: 生活热水系统
  - ELEC-UPS: 不间断电源系统
  - MGAS-AGSS: 麻醉废气排放系统
  - PLUMB-MED-WASTE: 医疗废水系统
  - FIRE-GAS: 气体灭火系统
```

---

## 4.1 HVAC-HWP 热源系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: HVAC-HWP
    system_name: 热源系统
    system_name_en: Hot Water Plant System
    category: HVAC
    version: 1.0
    
    description: |
      医院空调供暖热源系统，采用燃气锅炉或空气源热泵作为热源，
      通过热水管网为空调末端、生活热水系统提供热量。
      
    design_basis:
      heat_source: 燃气热水锅炉 / 空气源热泵
      supply_temperature: {value: 50-60, unit: ℃}
      return_temperature: {value: 40-50, unit: ℃}
      capacity: 根据热负荷计算
      
    serving_scope:
      - HVAC-AHU (再热盘管)
      - HVAC-FCU (供暖)
      - HVAC-CLEAN (加热盘管)
      - PLUMB-HWS (生活热水换热)

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: HVAC-HWP_BND_IN_GAS
        boundary_name: 天然气供应
        medium: GAS-NG
        is_external: true
        source: 市政燃气管网
        note: 燃气锅炉方案
        
      - boundary_id: HVAC-HWP_BND_IN_ELEC
        boundary_name: 电源
        medium: ELEC-LV
        source_system: ELEC-LV-MAIN
        note: 热泵方案
        
      - boundary_id: HVAC-HWP_BND_IN_WATER
        boundary_name: 补水
        medium: WATER-DW
        source_system: PLUMB-DWS
        
    outputs:
      - boundary_id: HVAC-HWP_BND_OUT_HW
        boundary_name: 热水供水
        medium: WATER-HW
        target_systems: [HVAC-CHP, HVAC-AHU, HVAC-FCU, HVAC-CLEAN]
        
      - boundary_id: HVAC-HWP_BND_OUT_HWS
        boundary_name: 生活热水换热
        medium: WATER-HW
        target_system: PLUMB-HWS

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:
  
    source_nodes:
    
      - node_id: HVAC-HWP_SRC_BOILER
        node_name: 燃气热水锅炉
        node_name_en: Gas-fired Hot Water Boiler
        node_type: Source_Node
        node_category: SRC
        
        function: 燃气燃烧产生热水
        medium_in: [GAS-NG, WATER-HW-RET]
        medium_out: WATER-HW
        
        multiplicity: multiple
        instance_pattern: HVAC-HWP_SRC_BOILER_{NN}
        
        typical_configuration:
          quantity: 2-3
          redundancy: "N+1"
          
        equipment_parameters:
          type: 真空热水锅炉/常压热水锅炉/承压热水锅炉
          capacity_each: {value: 2-4, unit: MW}
          efficiency: {value: "≥95", unit: "%"}
          supply_temp: {value: 60, unit: ℃}
          return_temp: {value: 50, unit: ℃}
          gas_consumption: 根据容量计算
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 锅炉房
          floor: 地下室或独立建筑
          
        installation_requirements:
          - 防火分隔
          - 燃气泄漏检测
          - 通风换气
          - 烟囱排放
          - 防爆电气
          - 检修通道
          
        control_points:
          sensors:
            - {point_id: BOILER_T_SUP, type: AI, description: 出水温度}
            - {point_id: BOILER_T_RET, type: AI, description: 回水温度}
            - {point_id: BOILER_P, type: AI, description: 压力}
            - {point_id: BOILER_FIRE, type: AI, description: 火焰信号}
            - {point_id: BOILER_GAS_P, type: AI, description: 燃气压力}
            - {point_id: BOILER_FLUE_T, type: AI, description: 烟气温度}
          status:
            - {point_id: BOILER_RUN, type: DI, description: 运行状态}
            - {point_id: BOILER_FAULT, type: DI, description: 故障报警}
            - {point_id: BOILER_FLAME, type: DI, description: 点火失败}
            - {point_id: GAS_LEAK, type: DI, description: 燃气泄漏}
          commands:
            - {point_id: BOILER_START, type: DO, description: 启停控制}
            - {point_id: BOILER_LOAD, type: AO, description: 负荷调节}

      - node_id: HVAC-HWP_SRC_ASHP
        node_name: 空气源热泵
        node_name_en: Air Source Heat Pump
        node_type: Source_Node
        node_category: SRC
        
        function: 从空气中提取热量
        medium_in: [AIR-OA, WATER-HW-RET, ELEC-LV]
        medium_out: WATER-HW
        
        multiplicity: multiple
        instance_pattern: HVAC-HWP_SRC_ASHP_{NN}
        
        typical_configuration:
          quantity: 3-6
          redundancy: "N+1"
          note: 可作为锅炉的替代或补充方案
          
        equipment_parameters:
          type: 空气源热泵机组
          capacity_each: {value: 200-500, unit: kW}
          cop: {value: "≥3.5", unit: null, condition: 工况7℃}
          supply_temp: {value: 50-55, unit: ℃}
          power: {value: 80-150, unit: kW}
          
        location_hint:
          space_type: OUTDOOR
          position: 屋顶或室外地面
          
        installation_requirements:
          - 通风良好
          - 减振基础
          - 冬季化霜排水
          - 噪声控制
          
        control_points:
          sensors:
            - {point_id: ASHP_T_SUP, type: AI, description: 出水温度}
            - {point_id: ASHP_T_RET, type: AI, description: 回水温度}
            - {point_id: ASHP_T_OA, type: AI, description: 室外温度}
            - {point_id: ASHP_I, type: AI, description: 运行电流}
          status:
            - {point_id: ASHP_RUN, type: DI, description: 运行状态}
            - {point_id: ASHP_FAULT, type: DI, description: 故障报警}
            - {point_id: ASHP_DEFROST, type: DI, description: 化霜状态}
          commands:
            - {point_id: ASHP_START, type: DO, description: 启停控制}

    distribution_nodes:
    
      - node_id: HVAC-HWP_DST_HWP
        node_name: 热水循环泵
        node_name_en: Hot Water Circulation Pump
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 热水循环输配
        medium_in: WATER-HW
        medium_out: WATER-HW
        
        multiplicity: multiple
        instance_pattern: HVAC-HWP_DST_HWP_{NN}
        
        typical_configuration:
          quantity: 2-3
          redundancy: 一用一备
          
        equipment_parameters:
          type: 离心泵（变频）
          flow: {value: 100-300, unit: m³/h}
          head: {value: 25-35, unit: m}
          power: {value: 22-55, unit: kW}
          control: 变频调速
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 锅炉房/热泵机房
          
        control_points:
          sensors:
            - {point_id: HWP_FREQ, type: AI, description: 运行频率}
            - {point_id: HWP_I, type: AI, description: 运行电流}
            - {point_id: HWP_DP, type: AI, description: 进出口压差}
          status:
            - {point_id: HWP_RUN, type: DI, description: 运行状态}
            - {point_id: HWP_FAULT, type: DI, description: 故障报警}
          commands:
            - {point_id: HWP_START, type: DO, description: 启停控制}
            - {point_id: HWP_FREQ_SP, type: AO, description: 频率设定}

      - node_id: HVAC-HWP_DST_HEADER_SUP
        node_name: 热水供水分水器
        node_name_en: Hot Water Supply Header
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
        
        function: 热水供水分配
        medium_in: WATER-HW
        medium_out: WATER-HW
        
        equipment_parameters:
          material: 无缝钢管
          diameter: {value: DN200-DN300, unit: mm}
          branches:
            - 空调热水供水
            - 生活热水换热
            
        location_hint:
          space_type: MEP_ROOM
          room_name: 锅炉房
          
        control_points:
          sensors:
            - {point_id: HW_SUP_T, type: AI, description: 供水温度}
            - {point_id: HW_SUP_P, type: AI, description: 供水压力}

      - node_id: HVAC-HWP_DST_HEADER_RET
        node_name: 热水回水集水器
        node_name_en: Hot Water Return Header
        node_type: Distribution_Node
        node_category: DST
        node_subtype: JUN
        
        function: 热水回水汇集
        medium_in: WATER-HW
        medium_out: WATER-HW
        
        equipment_parameters:
          material: 无缝钢管
          diameter: {value: DN200-DN300, unit: mm}
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 锅炉房
          
        control_points:
          sensors:
            - {point_id: HW_RET_T, type: AI, description: 回水温度}
            - {point_id: HW_RET_P, type: AI, description: 回水压力}

      - node_id: HVAC-HWP_DST_MAKEUP
        node_name: 补水定压装置
        node_name_en: Makeup Water & Pressurization Unit
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 系统补水、定压
        medium_in: WATER-DW
        medium_out: WATER-HW
        
        equipment_parameters:
          type: 定压补水装置
          components:
            - 补水泵
            - 定压罐/膨胀罐
            - 软化水装置
            - 控制器
          pressure_setpoint: 系统静压+5-10m
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 锅炉房
          
        control_points:
          sensors:
            - {point_id: MAKEUP_P, type: AI, description: 系统压力}
            - {point_id: MAKEUP_LEVEL, type: AI, description: 补水箱液位}
          status:
            - {point_id: MAKEUP_PUMP_RUN, type: DI, description: 补水泵运行}
            - {point_id: MAKEUP_LOW_P, type: DI, description: 低压报警}

      - node_id: HVAC-HWP_DST_AHU_BRANCH
        node_name: AHU热水分支
        node_name_en: AHU Hot Water Branch
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BRH
        
        function: 向空调机组供热水
        medium_in: WATER-HW
        medium_out: WATER-HW
        
        equipment_parameters:
          valve: 电动调节阀/平衡阀
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 锅炉房
          
        interface_systems: [HVAC-AHU, HVAC-CLEAN]

      - node_id: HVAC-HWP_DST_FCU_BRANCH
        node_name: FCU热水分支
        node_name_en: FCU Hot Water Branch
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BRH
        
        function: 向风机盘管供热水
        medium_in: WATER-HW
        medium_out: WATER-HW
        
        equipment_parameters:
          valve: 平衡阀
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 锅炉房
          
        interface_system: HVAC-FCU

      - node_id: HVAC-HWP_DST_HWS_HEX
        node_name: 生活热水换热器
        node_name_en: DHW Heat Exchanger
        node_type: Distribution_Node
        node_category: DST
        node_subtype: HEX
        
        function: 热水系统与生活热水换热
        medium_in: [WATER-HW, WATER-DW]
        medium_out: [WATER-HW, WATER-HW-DOM]
        
        equipment_parameters:
          type: 板式换热器/容积式换热器
          capacity: 根据生活热水负荷
          primary_temp: {value: "60/50", unit: ℃}
          secondary_temp: {value: "55/10", unit: ℃}
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 热水机房
          
        interface_system: PLUMB-HWS
        
        control_points:
          sensors:
            - {point_id: HEX_T_HW_IN, type: AI, description: 一次侧进水温度}
            - {point_id: HEX_T_HW_OUT, type: AI, description: 一次侧出水温度}
            - {point_id: HEX_T_DHW_OUT, type: AI, description: 二次侧出水温度}
          commands:
            - {point_id: HEX_VALVE, type: AO, description: 一次侧阀开度}

    sink_nodes:
    
      - node_id: HVAC-HWP_SNK_AHU
        node_name: AHU热水用户
        node_name_en: AHU Hot Water User
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 空调加热
        medium_in: WATER-HW
        
        interface_system: HVAC-AHU
        
      - node_id: HVAC-HWP_SNK_FCU
        node_name: FCU热水用户
        node_name_en: FCU Hot Water User
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 末端供暖
        medium_in: WATER-HW
        
        interface_system: HVAC-FCU
        
      - node_id: HVAC-HWP_SNK_DHW
        node_name: 生活热水
        node_name_en: DHW User
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 生活热水加热
        medium_in: WATER-HW
        
        interface_system: PLUMB-HWS

  # ============================================================
  # 边定义
  # ============================================================
  edges:
  
    supply_edges:
    
      - edge_id: HVAC-HWP_EDGE_001
        edge_name: 锅炉至循环泵
        edge_type: TRK
        from_node: HVAC-HWP_SRC_BOILER
        to_node: HVAC-HWP_DST_HWP
        direction: unidirectional
        medium: WATER-HW
        medium_properties:
          temperature: {value: 60, unit: ℃}
          
      - edge_id: HVAC-HWP_EDGE_002
        edge_name: 循环泵至分水器
        edge_type: TRK
        from_node: HVAC-HWP_DST_HWP
        to_node: HVAC-HWP_DST_HEADER_SUP
        direction: unidirectional
        medium: WATER-HW
        
      - edge_id: HVAC-HWP_EDGE_003
        edge_name: 分水器至AHU分支
        edge_type: BRH
        from_node: HVAC-HWP_DST_HEADER_SUP
        to_node: HVAC-HWP_DST_AHU_BRANCH
        direction: unidirectional
        medium: WATER-HW
        
      - edge_id: HVAC-HWP_EDGE_004
        edge_name: 分水器至FCU分支
        edge_type: BRH
        from_node: HVAC-HWP_DST_HEADER_SUP
        to_node: HVAC-HWP_DST_FCU_BRANCH
        direction: unidirectional
        medium: WATER-HW
        
      - edge_id: HVAC-HWP_EDGE_005
        edge_name: 分水器至生活热水换热器
        edge_type: BRH
        from_node: HVAC-HWP_DST_HEADER_SUP
        to_node: HVAC-HWP_DST_HWS_HEX
        direction: unidirectional
        medium: WATER-HW
        
      - edge_id: HVAC-HWP_EDGE_006
        edge_name: AHU分支至AHU用户
        edge_type: TRM
        from_node: HVAC-HWP_DST_AHU_BRANCH
        to_node: HVAC-HWP_SNK_AHU
        direction: unidirectional
        medium: WATER-HW
        cross_system: true
        target_system: HVAC-AHU
        
      - edge_id: HVAC-HWP_EDGE_007
        edge_name: FCU分支至FCU用户
        edge_type: TRM
        from_node: HVAC-HWP_DST_FCU_BRANCH
        to_node: HVAC-HWP_SNK_FCU
        direction: unidirectional
        medium: WATER-HW
        cross_system: true
        target_system: HVAC-FCU
        
      - edge_id: HVAC-HWP_EDGE_008
        edge_name: 换热器至生活热水
        edge_type: TRM
        from_node: HVAC-HWP_DST_HWS_HEX
        to_node: HVAC-HWP_SNK_DHW
        direction: unidirectional
        medium: WATER-HW-DOM
        cross_system: true
        target_system: PLUMB-HWS

    return_edges:
    
      - edge_id: HVAC-HWP_EDGE_RET_001
        edge_name: AHU用户回水
        edge_type: TRM
        from_node: HVAC-HWP_SNK_AHU
        to_node: HVAC-HWP_DST_AHU_BRANCH
        direction: unidirectional
        medium: WATER-HW
        
      - edge_id: HVAC-HWP_EDGE_RET_002
        edge_name: FCU用户回水
        edge_type: TRM
        from_node: HVAC-HWP_SNK_FCU
        to_node: HVAC-HWP_DST_FCU_BRANCH
        direction: unidirectional
        medium: WATER-HW
        
      - edge_id: HVAC-HWP_EDGE_RET_003
        edge_name: 各分支至集水器
        edge_type: TRK
        from_node: HVAC-HWP_DST_AHU_BRANCH
        to_node: HVAC-HWP_DST_HEADER_RET
        direction: unidirectional
        medium: WATER-HW
        
      - edge_id: HVAC-HWP_EDGE_RET_004
        edge_name: 集水器至锅炉
        edge_type: TRK
        from_node: HVAC-HWP_DST_HEADER_RET
        to_node: HVAC-HWP_SRC_BOILER
        direction: unidirectional
        medium: WATER-HW
        medium_properties:
          temperature: {value: 50, unit: ℃}

    makeup_edges:
    
      - edge_id: HVAC-HWP_EDGE_MAKEUP
        edge_name: 补水至系统
        edge_type: BRH
        from_node: HVAC-HWP_DST_MAKEUP
        to_node: HVAC-HWP_DST_HEADER_RET
        direction: unidirectional
        medium: WATER-HW

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:
  
    - path_id: HVAC-HWP_PATH_AHU
      path_name: AHU供热路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: HVAC-HWP_SRC_BOILER}
        - {step: 2, element_type: edge, element_id: HVAC-HWP_EDGE_001}
        - {step: 3, element_type: node, element_id: HVAC-HWP_DST_HWP}
        - {step: 4, element_type: edge, element_id: HVAC-HWP_EDGE_002}
        - {step: 5, element_type: node, element_id: HVAC-HWP_DST_HEADER_SUP}
        - {step: 6, element_type: edge, element_id: HVAC-HWP_EDGE_003}
        - {step: 7, element_type: node, element_id: HVAC-HWP_DST_AHU_BRANCH}
        - {step: 8, element_type: edge, element_id: HVAC-HWP_EDGE_006}
        - {step: 9, element_type: node, element_id: HVAC-HWP_SNK_AHU}

  # ============================================================
  # 回路定义
  # ============================================================
  loops:
  
    - loop_id: HVAC-HWP_LOOP_MAIN
      loop_name: 热水主循环回路
      loop_name_en: Hot Water Main Loop
      loop_type: closed
      
      description: |
        热源产生热水→循环泵加压→分水器分配→各用户→回水集水器→热源
        
      delta_t: {value: 10, unit: ℃}
      design_flow: 根据负荷计算

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:
  
    boiler_staging:
      description: 锅炉台数控制
      control_parameter: 回水温度或热负荷
      
      stage_up:
        condition: 供水温度 < 设定值-3℃ 且 运行锅炉满负荷
        action: 启动下一台锅炉
        delay: {value: 5, unit: min}
        
      stage_down:
        condition: 运行锅炉负荷 < 30% 且 持续15分钟
        action: 停止一台锅炉
        
    pump_control:
      mode: 变频恒压差控制
      setpoint: 最不利用户所需压差
      method: PID调节泵频率
      
    temperature_control:
      supply_temp_setpoint:
        mode: 室外温度补偿
        outdoor_high: {value: 10, unit: ℃, supply: 45, unit: ℃}
        outdoor_low: {value: -10, unit: ℃, supply: 60, unit: ℃}
        
    safety_interlock:
      low_water_level:
        action: 锅炉停机
      high_temperature:
        action: 锅炉停机
      gas_leak:
        action: 切断燃气、锅炉停机、报警
      flame_failure:
        action: 锅炉停机、报警
```

---

## 4.2 HVAC-SMOKE 防排烟系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: HVAC-SMOKE
    system_name: 防排烟系统
    system_name_en: Smoke Control System
    category: HVAC
    subcategory: FIRE_PROTECTION
    version: 1.0
    
    description: |
      医院防排烟系统，包括机械排烟系统和机械加压送风系统。
      用于火灾时排除烟气、保护疏散通道。
      与火灾自动报警系统联动。
      
    design_basis:
      smoke_exhaust:
        velocity: {value: "≥15", unit: m/s}
        temp_rating: {value: 280, unit: ℃}
        duration: {value: 2, unit: h}
      pressurization:
        pressure_diff: {value: 25-50, unit: Pa}
        door_air_velocity: {value: "≥0.7", unit: m/s}
      
    serving_scope:
      - 无窗房间/走廊
      - 地下室
      - 防烟楼梯间
      - 前室/合用前室

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: HVAC-SMOKE_BND_IN_ELEC
        boundary_name: 消防电源
        medium: ELEC-LV
        source_system: ELEC-LV-FIRE
        note: 双电源供电
        
      - boundary_id: HVAC-SMOKE_BND_IN_FA
        boundary_name: 火灾报警联动信号
        medium: SIGNAL-FA
        source_system: FIRE-ALARM
        
    outputs:
      - boundary_id: HVAC-SMOKE_BND_OUT_EXHAUST
        boundary_name: 烟气排放
        medium: AIR-SMOKE
        is_external: true
        target: 大气
        
      - boundary_id: HVAC-SMOKE_BND_OUT_SUPPLY
        boundary_name: 加压送风
        medium: AIR-FA
        target: 疏散通道

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:
  
    source_nodes:
    
      - node_id: HVAC-SMOKE_SRC_OA
        node_name: 加压送风进风口
        node_name_en: Pressurization Air Intake
        node_type: Source_Node
        node_category: SRC
        
        function: 加压送风新风入口
        medium_out: AIR-OA
        is_external: true
        
        equipment_parameters:
          type: 百叶风口
          position: 正压区（远离火源）
          
        location_hint:
          space_type: EXTERIOR
          position: 屋顶或外墙
          height: 距地面≥2m
          requirement: 距排烟口≥6m

      - node_id: HVAC-SMOKE_SRC_PRESS_FAN
        node_name: 正压送风机
        node_name_en: Pressurization Fan
        node_type: Source_Node
        node_category: SRC
        
        function: 向疏散通道加压送风
        medium_in: AIR-OA
        medium_out: AIR-FA
        
        multiplicity: multiple
        instance_pattern: HVAC-SMOKE_SRC_PRESS_FAN_{Zone}
        
        equipment_parameters:
          type: 轴流风机/离心风机
          flow: {value: 10000-30000, unit: m³/h}
          pressure: {value: 500-1000, unit: Pa}
          power: {value: 15-55, unit: kW}
          temperature: 常温
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 加压送风机房
          position: 屋顶或避难层
          
        installation_requirements:
          - 280℃×2h防火阀
          - 双电源供电
          - 消防联动控制
          - 手动控制按钮
          
        control_points:
          sensors:
            - {point_id: PRESS_DP, type: AI, description: 楼梯间压差}
          status:
            - {point_id: PRESS_FAN_RUN, type: DI, description: 运行状态}
            - {point_id: PRESS_FAN_FAULT, type: DI, description: 故障报警}
          commands:
            - {point_id: PRESS_FAN_START, type: DO, description: 启动命令}
            - {point_id: PRESS_FAN_STOP, type: DO, description: 停止命令}

    distribution_nodes:
    
      - node_id: HVAC-SMOKE_DST_PRESS_SHAFT
        node_name: 加压送风竖井
        node_name_en: Pressurization Shaft
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
        
        function: 垂直送风通道
        medium_in: AIR-FA
        medium_out: AIR-FA
        
        multiplicity: multiple
        
        equipment_parameters:
          material: 混凝土/砖
          fire_rating: 耐火极限≥2h
          
        location_hint:
          space_type: SHAFT
          shaft_type: 正压送风井
          position: 紧邻楼梯间

      - node_id: HVAC-SMOKE_DST_PRESS_OUTLET
        node_name: 加压送风口
        node_name_en: Pressurization Air Outlet
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRM
        
        function: 向楼梯间/前室送风
        medium_in: AIR-FA
        medium_out: AIR-FA
        
        multiplicity: multiple
        instance_pattern: HVAC-SMOKE_DST_PRESS_OUTLET_{Floor}
        
        equipment_parameters:
          type: 常闭多叶送风口
          actuator: 电动/电磁
          open_signal: 火灾联动
          
        location_hint:
          space_type: WALL
          position: 楼梯间或前室墙面
          height: {value: 2.0-2.5, unit: m}
          
        control_points:
          status:
            - {point_id: OUTLET_OPEN, type: DI, description: 开启状态}
          commands:
            - {point_id: OUTLET_CMD, type: DO, description: 开启命令}

      - node_id: HVAC-SMOKE_DST_EXHAUST_FAN
        node_name: 排烟风机
        node_name_en: Smoke Exhaust Fan
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 机械排烟
        medium_in: AIR-SMOKE
        medium_out: AIR-SMOKE
        
        multiplicity: multiple
        instance_pattern: HVAC-SMOKE_DST_EXHAUST_FAN_{Zone}
        
        equipment_parameters:
          type: 排烟风机（耐高温）
          flow: {value: 20000-50000, unit: m³/h}
          pressure: {value: 600-1200, unit: Pa}
          power: {value: 30-90, unit: kW}
          temperature_rating: {value: 280, unit: ℃}
          duration: {value: 2, unit: h}
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 排烟机房
          position: 屋顶
          
        installation_requirements:
          - 耐高温风机
          - 双电源供电
          - 消防联动控制
          - 手动控制按钮
          
        control_points:
          sensors:
            - {point_id: EXH_TEMP, type: AI, description: 排烟温度}
          status:
            - {point_id: EXH_FAN_RUN, type: DI, description: 运行状态}
            - {point_id: EXH_FAN_FAULT, type: DI, description: 故障报警}
          commands:
            - {point_id: EXH_FAN_START, type: DO, description: 启动命令}

      - node_id: HVAC-SMOKE_DST_EXHAUST_SHAFT
        node_name: 排烟竖井
        node_name_en: Smoke Exhaust Shaft
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
        
        function: 垂直排烟通道
        medium_in: AIR-SMOKE
        medium_out: AIR-SMOKE
        
        multiplicity: multiple
        
        equipment_parameters:
          material: 混凝土/砖
          fire_rating: 耐火极限≥2h
          
        location_hint:
          space_type: SHAFT
          shaft_type: 排烟井

      - node_id: HVAC-SMOKE_DST_EXHAUST_INLET
        node_name: 排烟口
        node_name_en: Smoke Exhaust Inlet
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRM
        
        function: 排烟入口
        medium_in: AIR-SMOKE
        medium_out: AIR-SMOKE
        
        multiplicity: multiple
        instance_pattern: HVAC-SMOKE_DST_EXHAUST_INLET_{Floor}_{Zone}
        
        equipment_parameters:
          type: 常闭排烟口/排烟阀
          actuator: 电动/手动复位
          temperature_fuse: 280℃熔断
          
        location_hint:
          space_type: CEILING
          position: 走廊/房间吊顶
          height: 储烟仓内
          spacing: {value: "≤30", unit: m}
          
        control_points:
          status:
            - {point_id: INLET_OPEN, type: DI, description: 开启状态}
          commands:
            - {point_id: INLET_CMD, type: DO, description: 开启命令}

      - node_id: HVAC-SMOKE_DST_FIRE_DAMPER
        node_name: 防火阀
        node_name_en: Fire Damper
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 火灾时切断风管
        medium_in: AIR
        medium_out: AIR
        
        multiplicity: multiple
        
        equipment_parameters:
          types:
            - {type: 70℃防火阀, application: 空调风管穿越防火分区}
            - {type: 280℃排烟防火阀, application: 排烟风管}
          action: 温度熔断自动关闭
          reset: 手动复位
          
        location_hint:
          space_type: DUCT
          position: 穿越防火分隔处
          
        control_points:
          status:
            - {point_id: FD_CLOSE, type: DI, description: 关闭信号}

      - node_id: HVAC-SMOKE_DST_CONTROL
        node_name: 防排烟控制柜
        node_name_en: Smoke Control Panel
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 防排烟设备控制中心
        medium_in: SIGNAL-FA
        medium_out: CTRL
        
        equipment_parameters:
          functions:
            - 火灾联动控制
            - 手动控制
            - 状态反馈
            - 故障报警
            
        location_hint:
          space_type: MEP_ROOM
          room_name: 风机房/消防控制室
          
        interface_system: FIRE-ALARM

    sink_nodes:
    
      - node_id: HVAC-SMOKE_SNK_EXHAUST
        node_name: 排烟排放口
        node_name_en: Smoke Exhaust Outlet
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 烟气排放
        medium_in: AIR-SMOKE
        is_external: true
        
        location_hint:
          space_type: EXTERIOR
          position: 屋顶
          height: 距屋面≥2m
          requirement: 距可燃物≥6m
          
      - node_id: HVAC-SMOKE_SNK_STAIR
        node_name: 防烟楼梯间
        node_name_en: Smoke-proof Stairwell
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 加压保护
        medium_in: AIR-FA
        
        parameters:
          pressure_diff: {value: 40-50, unit: Pa}
          
      - node_id: HVAC-SMOKE_SNK_VESTIBULE
        node_name: 前室/合用前室
        node_name_en: Vestibule
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 加压保护
        medium_in: AIR-FA
        
        parameters:
          pressure_diff: {value: 25-30, unit: Pa}

  # ============================================================
  # 边定义
  # ============================================================
  edges:
  
    pressurization_edges:
    
      - edge_id: HVAC-SMOKE_EDGE_001
        edge_name: 进风口至正压风机
        edge_type: TRK
        from_node: HVAC-SMOKE_SRC_OA
        to_node: HVAC-SMOKE_SRC_PRESS_FAN
        direction: unidirectional
        medium: AIR-OA
        
      - edge_id: HVAC-SMOKE_EDGE_002
        edge_name: 正压风机至竖井
        edge_type: TRK
        from_node: HVAC-SMOKE_SRC_PRESS_FAN
        to_node: HVAC-SMOKE_DST_PRESS_SHAFT
        direction: unidirectional
        medium: AIR-FA
        
      - edge_id: HVAC-SMOKE_EDGE_003
        edge_name: 竖井至送风口
        edge_type: BRH
        from_node: HVAC-SMOKE_DST_PRESS_SHAFT
        to_node: HVAC-SMOKE_DST_PRESS_OUTLET
        direction: unidirectional
        medium: AIR-FA
        
      - edge_id: HVAC-SMOKE_EDGE_004
        edge_name: 送风口至楼梯间
        edge_type: TRM
        from_node: HVAC-SMOKE_DST_PRESS_OUTLET
        to_node: HVAC-SMOKE_SNK_STAIR
        direction: unidirectional
        medium: AIR-FA

    exhaust_edges:
    
      - edge_id: HVAC-SMOKE_EDGE_011
        edge_name: 排烟口至竖井
        edge_type: TRM
        from_node: HVAC-SMOKE_DST_EXHAUST_INLET
        to_node: HVAC-SMOKE_DST_EXHAUST_SHAFT
        direction: unidirectional
        medium: AIR-SMOKE
        
      - edge_id: HVAC-SMOKE_EDGE_012
        edge_name: 竖井至排烟风机
        edge_type: TRK
        from_node: HVAC-SMOKE_DST_EXHAUST_SHAFT
        to_node: HVAC-SMOKE_DST_EXHAUST_FAN
        direction: unidirectional
        medium: AIR-SMOKE
        
      - edge_id: HVAC-SMOKE_EDGE_013
        edge_name: 排烟风机至排放口
        edge_type: TRK
        from_node: HVAC-SMOKE_DST_EXHAUST_FAN
        to_node: HVAC-SMOKE_SNK_EXHAUST
        direction: unidirectional
        medium: AIR-SMOKE

    control_edges:
    
      - edge_id: HVAC-SMOKE_EDGE_FA
        edge_name: 火灾报警联动
        edge_type: CTRL
        from_node: FIRE-ALARM_DST_LINKAGE
        to_node: HVAC-SMOKE_DST_CONTROL
        direction: unidirectional
        medium: SIGNAL-FA
        cross_system: true
        source_system: FIRE-ALARM

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:
  
    - path_id: HVAC-SMOKE_PATH_PRESS
      path_name: 加压送风路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: HVAC-SMOKE_SRC_OA}
        - {step: 2, element_type: edge, element_id: HVAC-SMOKE_EDGE_001}
        - {step: 3, element_type: node, element_id: HVAC-SMOKE_SRC_PRESS_FAN}
        - {step: 4, element_type: edge, element_id: HVAC-SMOKE_EDGE_002}
        - {step: 5, element_type: node, element_id: HVAC-SMOKE_DST_PRESS_SHAFT}
        - {step: 6, element_type: edge, element_id: HVAC-SMOKE_EDGE_003}
        - {step: 7, element_type: node, element_id: HVAC-SMOKE_DST_PRESS_OUTLET}
        - {step: 8, element_type: edge, element_id: HVAC-SMOKE_EDGE_004}
        - {step: 9, element_type: node, element_id: HVAC-SMOKE_SNK_STAIR}
        
    - path_id: HVAC-SMOKE_PATH_EXHAUST
      path_name: 机械排烟路径
      path_type: EXH
      sequence:
        - {step: 1, element_type: node, element_id: HVAC-SMOKE_DST_EXHAUST_INLET}
        - {step: 2, element_type: edge, element_id: HVAC-SMOKE_EDGE_011}
        - {step: 3, element_type: node, element_id: HVAC-SMOKE_DST_EXHAUST_SHAFT}
        - {step: 4, element_type: edge, element_id: HVAC-SMOKE_EDGE_012}
        - {step: 5, element_type: node, element_id: HVAC-SMOKE_DST_EXHAUST_FAN}
        - {step: 6, element_type: edge, element_id: HVAC-SMOKE_EDGE_013}
        - {step: 7, element_type: node, element_id: HVAC-SMOKE_SNK_EXHAUST}

  # ============================================================
  # 联动控制逻辑
  # ============================================================
  control_logic:
  
    pressurization_sequence:
      trigger: 防烟楼梯间/前室区域火灾确认
      actions:
        - step: 1
          action: 开启着火层及相邻层送风口
        - step: 2
          action: 启动正压送风机
        - step: 3
          action: 检测楼梯间压差
          target: {value: 40-50, unit: Pa}
          
    exhaust_sequence:
      trigger: 防烟分区火灾确认
      actions:
        - step: 1
          action: 开启着火区域排烟口
        - step: 2
          action: 启动排烟风机
        - step: 3
          action: 开启补风设施（如有）
          
    temperature_protection:
      condition: 排烟温度 > 280℃
      action:
        - 排烟防火阀熔断关闭
        - 排烟风机停止
        - 发送信号至消防控制室
        
    pressure_control:
      method: 旁通阀/变频调节
      target: 维持设计压差
      avoid: 压差过大致疏散门无法开启
```

---

## 4.3 PLUMB-HWS 生活热水系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: PLUMB-HWS
    system_name: 生活热水系统
    system_name_en: Domestic Hot Water System
    category: PLUMBING
    version: 1.0
    
    description: |
      医院生活热水供应系统，采用集中换热+循环供水方式。
      通过热水循环保证即开即热。
      
    design_basis:
      supply_temperature: {value: 55-60, unit: ℃}
      return_temperature: {value: 45-50, unit: ℃}
      circulation: 24小时循环
      anti_legionella: 定期高温消毒
      
    serving_scope:
      - 病房淋浴/盥洗
      - 手术刷手
      - 供应室
      - 厨房

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: PLUMB-HWS_BND_IN_CW
        boundary_name: 冷水供应
        medium: WATER-DW
        source_system: PLUMB-DWS
        
      - boundary_id: PLUMB-HWS_BND_IN_HEAT
        boundary_name: 热源
        medium: WATER-HW
        source_system: HVAC-HWP
        
      - boundary_id: PLUMB-HWS_BND_IN_ELEC
        boundary_name: 电源
        medium: ELEC-LV
        source_system: ELEC-LV-MAIN
        
    outputs:
      - boundary_id: PLUMB-HWS_BND_OUT_HW
        boundary_name: 热水终端
        medium: WATER-HW-DOM
        target: 卫生洁具

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:
  
    source_nodes:
    
      - node_id: PLUMB-HWS_SRC_CW
        node_name: 冷水进水
        node_name_en: Cold Water Inlet
        node_type: Source_Node
        node_category: SRC
        
        function: 生活冷水接入
        medium_out: WATER-DW
        
        source_system: PLUMB-DWS
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 热水机房

      - node_id: PLUMB-HWS_SRC_HEAT
        node_name: 热源接入
        node_name_en: Heat Source Input
        node_type: Source_Node
        node_category: SRC
        
        function: 热水/蒸汽热源接入
        medium_out: WATER-HW
        
        source_system: HVAC-HWP
        
        location_hint:
          space_type: MEP_ROOM
          room_name: 热水机房

    distribution_nodes:
    
      - node_id: PLUMB-HWS_DST_HEX
        node_name: 热水换热器
        node_name_en: DHW Heat Exchanger
        node_type: Distribution_Node
        node_category: DST
        node_subtype: HEX
        
        function: 加热生活冷水
        medium_in: [WATER-DW, WATER-HW]
        medium_out: [WATER-HW-DOM, WATER-HW]
        
        multiplicity: multiple
        
        typical_configuration:
          quantity: 2
          redundancy: 一用一备/并联
          
        equipment_parameters:
          type: 板式换热器/容积式换热器
          capacity: 根据热水负荷
          primary_temp: {value: "60/50", unit: ℃}
          secondary_temp: {value: "55/10", unit: ℃}
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 热水机房
          
        control_points:
          sensors:
            - {point_id: HEX_T_CW_IN, type: AI, description: 冷水进水温度}
            - {point_id: HEX_T_HW_OUT, type: AI, description: 热水出水温度}
          commands:
            - {point_id: HEX_VALVE, type: AO, description: 一次侧阀开度}

      - node_id: PLUMB-HWS_DST_STORAGE
        node_name: 热水储罐
        node_name_en: Hot Water Storage Tank
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BUF
        
        function: 热水储存、缓冲
        medium_in: WATER-HW-DOM
        medium_out: WATER-HW-DOM
        
        equipment_parameters:
          capacity: {value: 5-20, unit: m³}
          material: 不锈钢
          insulation: 聚氨酯保温
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 热水机房
          
        control_points:
          sensors:
            - {point_id: TANK_T, type: AI, description: 罐内温度}
            - {point_id: TANK_LEVEL, type: AI, description: 液位}

      - node_id: PLUMB-HWS_DST_CIRC_PUMP
        node_name: 热水循环泵
        node_name_en: DHW Circulation Pump
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 热水循环
        medium_in: WATER-HW-DOM
        medium_out: WATER-HW-DOM
        
        equipment_parameters:
          configuration: 一用一备
          flow: {value: 10-30, unit: m³/h}
          head: {value: 20-30, unit: m}
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 热水机房
          
        control_points:
          status:
            - {point_id: CIRC_PUMP_RUN, type: DI, description: 运行状态}

      - node_id: PLUMB-HWS_DST_MAIN_SUP
        node_name: 热水供水主管
        node_name_en: Hot Water Supply Main
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
        
        function: 热水水平输配
        medium_in: WATER-HW-DOM
        medium_out: WATER-HW-DOM
        
        equipment_parameters:
          material: 不锈钢管/PPR管
          insulation: 橡塑保温
          diameter: {value: DN65-DN100, unit: mm}
          
        location_hint:
          space_type: CEILING_VOID / PIPE_TRENCH

      - node_id: PLUMB-HWS_DST_MAIN_RET
        node_name: 热水回水主管
        node_name_en: Hot Water Return Main
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
        
        function: 热水循环回水
        medium_in: WATER-HW-DOM
        medium_out: WATER-HW-DOM
        
        equipment_parameters:
          material: 不锈钢管/PPR管
          insulation: 橡塑保温
          diameter: {value: DN32-DN50, unit: mm}
          
        location_hint:
          space_type: CEILING_VOID / PIPE_TRENCH

      - node_id: PLUMB-HWS_DST_RISER
        node_name: 热水立管
        node_name_en: Hot Water Riser
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
        
        function: 垂直输配
        medium_in: WATER-HW-DOM
        medium_out: WATER-HW-DOM
        
        multiplicity: multiple
        
        equipment_parameters:
          material: 不锈钢管/PPR管
          diameter: {value: DN32-DN50, unit: mm}
          
        location_hint:
          space_type: SHAFT
          shaft_type: 给排水管井

      - node_id: PLUMB-HWS_DST_BRANCH
        node_name: 热水支管
        node_name_en: Hot Water Branch
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BRH
        
        function: 楼层分配
        medium_in: WATER-HW-DOM
        medium_out: WATER-HW-DOM
        
        equipment_parameters:
          material: PPR管
          diameter: {value: DN20-DN32, unit: mm}
          
        location_hint:
          space_type: CEILING_VOID / WALL

      - node_id: PLUMB-HWS_DST_TMV
        node_name: 恒温混水阀
        node_name_en: Thermostatic Mixing Valve
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 冷热水混合、防烫伤
        medium_in: [WATER-HW-DOM, WATER-DW]
        medium_out: WATER-MIXED
        
        multiplicity: multiple
        
        equipment_parameters:
          outlet_temp: {value: 38-43, unit: ℃}
          anti_scald: true
          
        location_hint:
          space_type: WALL_BOX
          position: 淋浴间入口

    sink_nodes:
    
      - node_id: PLUMB-HWS_SNK_FIXTURE
        node_name: 热水终端
        node_name_en: Hot Water Fixture
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 热水使用
        medium_in: WATER-HW-DOM
        
        multiplicity: multiple
        
        equipment_parameters:
          types:
            - 淋浴器
            - 洗手盆
            - 污洗盆
            
        location_hint:
          space_type: WET_ROOM

  # ============================================================
  # 边定义
  # ============================================================
  edges:
  
    supply_edges:
    
      - edge_id: PLUMB-HWS_EDGE_001
        edge_name: 冷水至换热器
        edge_type: TRK
        from_node: PLUMB-HWS_SRC_CW
        to_node: PLUMB-HWS_DST_HEX
        direction: unidirectional
        medium: WATER-DW
        
      - edge_id: PLUMB-HWS_EDGE_002
        edge_name: 热源至换热器
        edge_type: TRK
        from_node: PLUMB-HWS_SRC_HEAT
        to_node: PLUMB-HWS_DST_HEX
        direction: unidirectional
        medium: WATER-HW
        
      - edge_id: PLUMB-HWS_EDGE_003
        edge_name: 换热器至储罐
        edge_type: TRK
        from_node: PLUMB-HWS_DST_HEX
        to_node: PLUMB-HWS_DST_STORAGE
        direction: unidirectional
        medium: WATER-HW-DOM
        
      - edge_id: PLUMB-HWS_EDGE_004
        edge_name: 储罐至循环泵
        edge_type: TRK
        from_node: PLUMB-HWS_DST_STORAGE
        to_node: PLUMB-HWS_DST_CIRC_PUMP
        direction: unidirectional
        medium: WATER-HW-DOM
        
      - edge_id: PLUMB-HWS_EDGE_005
        edge_name: 循环泵至供水主管
        edge_type: TRK
        from_node: PLUMB-HWS_DST_CIRC_PUMP
        to_node: PLUMB-HWS_DST_MAIN_SUP
        direction: unidirectional
        medium: WATER-HW-DOM
        
      - edge_id: PLUMB-HWS_EDGE_006
        edge_name: 供水主管至立管
        edge_type: BRH
        from_node: PLUMB-HWS_DST_MAIN_SUP
        to_node: PLUMB-HWS_DST_RISER
        direction: unidirectional
        medium: WATER-HW-DOM
        
      - edge_id: PLUMB-HWS_EDGE_007
        edge_name: 立管至支管
        edge_type: BRH
        from_node: PLUMB-HWS_DST_RISER
        to_node: PLUMB-HWS_DST_BRANCH
        direction: unidirectional
        medium: WATER-HW-DOM
        
      - edge_id: PLUMB-HWS_EDGE_008
        edge_name: 支管至终端
        edge_type: TRM
        from_node: PLUMB-HWS_DST_BRANCH
        to_node: PLUMB-HWS_SNK_FIXTURE
        direction: unidirectional
        medium: WATER-HW-DOM

    return_edges:
    
      - edge_id: PLUMB-HWS_EDGE_RET_001
        edge_name: 立管回水至回水主管
        edge_type: TRK
        from_node: PLUMB-HWS_DST_RISER
        to_node: PLUMB-HWS_DST_MAIN_RET
        direction: unidirectional
        medium: WATER-HW-DOM
        
      - edge_id: PLUMB-HWS_EDGE_RET_002
        edge_name: 回水主管至储罐
        edge_type: TRK
        from_node: PLUMB-HWS_DST_MAIN_RET
        to_node: PLUMB-HWS_DST_STORAGE
        direction: unidirectional
        medium: WATER-HW-DOM

  # ============================================================
  # 路径与回路
  # ============================================================
  typical_paths:
  
    - path_id: PLUMB-HWS_PATH_SUP
      path_name: 热水供水路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: PLUMB-HWS_SRC_CW}
        - {step: 2, element_type: node, element_id: PLUMB-HWS_DST_HEX}
        - {step: 3, element_type: node, element_id: PLUMB-HWS_DST_STORAGE}
        - {step: 4, element_type: node, element_id: PLUMB-HWS_DST_CIRC_PUMP}
        - {step: 5, element_type: node, element_id: PLUMB-HWS_DST_MAIN_SUP}
        - {step: 6, element_type: node, element_id: PLUMB-HWS_DST_RISER}
        - {step: 7, element_type: node, element_id: PLUMB-HWS_DST_BRANCH}
        - {step: 8, element_type: node, element_id: PLUMB-HWS_SNK_FIXTURE}

  loops:
  
    - loop_id: PLUMB-HWS_LOOP_CIRC
      loop_name: 热水循环回路
      loop_name_en: DHW Circulation Loop
      loop_type: closed
      
      description: |
        热水从储罐经循环泵、供水主管、立管至最远端，
        未使用的热水通过回水管返回储罐，保持水温。
        
      circulation: 24小时
      velocity: {value: "≥0.5", unit: m/s}

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:
  
    temperature_control:
      setpoint: {value: 55-60, unit: ℃}
      sensor: 储罐或出水温度
      control: 一次侧阀开度调节
      
    anti_legionella:
      description: 军团菌防控
      measures:
        - 储水温度≥55℃
        - 定期高温消毒（70℃×10min）
        - 避免死水段
        - 回水温度≥50℃
        
    circulation_control:
      mode: 24小时循环
      pump_control: 连续运行或时间控制
```

---

## 4.4 ELEC-UPS 不间断电源系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: ELEC-UPS
    system_name: 不间断电源系统
    system_name_en: Uninterruptible Power Supply System
    category: ELECTRICAL
    version: 1.0
    
    description: |
      医院不间断电源系统，为数据中心、医疗信息系统、手术室监护设备等
      关键负荷提供不间断、高质量的电源供应。
      
    design_basis:
      capacity: 根据负荷计算
      backup_time: {value: 15-30, unit: min}
      configuration: "N+1冗余或2N"
      
    serving_scope:
      - 数据中心
      - HIS/PACS服务器
      - 手术室监护设备
      - ICU监护设备
      - 检验设备

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: ELEC-UPS_BND_IN_AC
        boundary_name: 市电输入
        medium: ELEC-LV
        source_system: ELEC-LV-CRITICAL
        note: 经ATS双电源供电
        
    outputs:
      - boundary_id: ELEC-UPS_BND_OUT_UPS
        boundary_name: UPS输出
        medium: ELEC-UPS
        target: 关键IT/医疗设备

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:
  
    source_nodes:
    
      - node_id: ELEC-UPS_SRC_AC_INPUT
        node_name: UPS输入配电
        node_name_en: UPS Input Distribution
        node_type: Source_Node
        node_category: SRC
        
        function: 市电接入
        medium_out: ELEC-LV
        
        source_system: ELEC-LV-MAIN
        
        location_hint:
          space_type: MEP_ROOM
          room_name: UPS机房

    distribution_nodes:
    
      - node_id: ELEC-UPS_DST_UPS_UNIT
        node_name: UPS主机
        node_name_en: UPS Unit
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
        
        function: 电源转换、不间断供电
        medium_in: ELEC-LV
        medium_out: ELEC-UPS
        
        multiplicity: multiple
        instance_pattern: ELEC-UPS_DST_UPS_UNIT_{NN}
        
        typical_configuration:
          quantity: 2-4
          redundancy: "N+1"
          parallel: true
          
        equipment_parameters:
          type: 在线双变换式
          capacity_each: {value: 100-300, unit: kVA}
          input_voltage: {value: "380/220", unit: V}
          output_voltage: {value: "380/220", unit: V}
          efficiency: {value: "≥94", unit: "%"}
          power_factor: {value: 0.9, unit: null}
          transfer_time: {value: 0, unit: ms}
          
        location_hint:
          space_type: MEP_ROOM
          room_name: UPS机房
          floor: 地下室/设备层
          
        installation_requirements:
          - 空调温控（18-25℃）
          - 防尘
          - 承重检查
          - 进出线通道
          - 维护通道
          
        control_points:
          sensors:
            - {point_id: UPS_V_IN, type: AI, description: 输入电压}
            - {point_id: UPS_V_OUT, type: AI, description: 输出电压}
            - {point_id: UPS_I_OUT, type: AI, description: 输出电流}
            - {point_id: UPS_LOAD, type: AI, description: 负载率}
            - {point_id: UPS_BAT_V, type: AI, description: 电池电压}
            - {point_id: UPS_BAT_CAP, type: AI, description: 电池剩余容量}
            - {point_id: UPS_TEMP, type: AI, description: 内部温度}
          status:
            - {point_id: UPS_MODE, type: DI, description: 运行模式}
            - {point_id: UPS_BYPASS, type: DI, description: 旁路状态}
            - {point_id: UPS_FAULT, type: DI, description: 故障报警}
            - {point_id: UPS_BAT_LOW, type: DI, description: 电池低电量}
            - {point_id: UPS_OVERLOAD, type: DI, description: 过载报警}

      - node_id: ELEC-UPS_DST_BATTERY
        node_name: 蓄电池组
        node_name_en: Battery Bank
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BUF
        
        function: 储能、后备供电
        medium_in: ELEC-DC
        medium_out: ELEC-DC
        
        multiplicity: multiple
        
        equipment_parameters:
          type: 阀控密封铅酸电池/锂电池
          voltage: {value: 384-480, unit: VDC}
          capacity: 根据后备时间计算
          backup_time: {value: 15-30, unit: min}
          
        location_hint:
          space_type: MEP_ROOM
          room_name: UPS机房/电池室
          
        installation_requirements:
          - 电池架
          - 通风换气
          - 温度控制（20-25℃）
          - 防酸处理（铅酸电池）
          - 承重验算
          - 消防措施
          
        control_points:
          sensors:
            - {point_id: BAT_V, type: AI, description: 总电压}
            - {point_id: BAT_I, type: AI, description: 充放电电流}
            - {point_id: BAT_TEMP, type: AI, description: 电池温度}
            - {point_id: BAT_SOC, type: AI, description: 剩余容量}
          status:
            - {point_id: BAT_CHARGING, type: DI, description: 充电状态}
            - {point_id: BAT_FAULT, type: DI, description: 电池故障}

      - node_id: ELEC-UPS_DST_STS
        node_name: 静态转换开关
        node_name_en: Static Transfer Switch
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: UPS输出切换/并联
        medium_in: ELEC-UPS
        medium_out: ELEC-UPS
        
        equipment_parameters:
          type: 静态转换开关
          transfer_time: {value: "<4", unit: ms}
          
        location_hint:
          space_type: MEP_ROOM
          room_name: UPS机房
          
        note: 2N系统时使用

      - node_id: ELEC-UPS_DST_OUTPUT_PANEL
        node_name: UPS输出配电柜
        node_name_en: UPS Output Distribution Panel
        node_type: Distribution_Node
        node_category: DST
        node_subtype: SPL
        
        function: UPS输出配电分配
        medium_in: ELEC-UPS
        medium_out: ELEC-UPS
        
        equipment_parameters:
          type: 低压开关柜
          rated_current: {value: 400-800, unit: A}
          circuits: 多回路分配
          
        location_hint:
          space_type: MEP_ROOM
          room_name: UPS机房
          
        control_points:
          sensors:
            - {point_id: UPS_OUT_V, type: AI, description: 输出电压}
            - {point_id: UPS_OUT_P, type: AI, description: 输出功率}

      - node_id: ELEC-UPS_DST_PDU
        node_name: 机架配电单元
        node_name_en: Power Distribution Unit
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRM
        
        function: 机柜级配电
        medium_in: ELEC-UPS
        medium_out: ELEC-UPS
        
        multiplicity: multiple
        
        equipment_parameters:
          type: 智能PDU
          outlets: {value: 20-42, unit: 位}
          metering: 分路计量
          
        location_hint:
          space_type: RACK
          position: 机柜内

    sink_nodes:
    
      - node_id: ELEC-UPS_SNK_IT
        node_name: IT设备
        node_name_en: IT Equipment
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: IT负载
        medium_in: ELEC-UPS
        
        equipment_parameters:
          types:
            - 服务器
            - 存储设备
            - 网络设备
            
        location_hint:
          space_type: RACK
          room_name: 数据中心

      - node_id: ELEC-UPS_SNK_MEDICAL
        node_name: 医疗设备
        node_name_en: Medical Equipment
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 医疗负载
        medium_in: ELEC-UPS
        
        equipment_parameters:
          types:
            - 监护仪
            - 输液泵
            - 呼吸机电子控制部分
            
        location_hint:
          space_type: MEDICAL
          position: 手术室、ICU

  # ============================================================
  # 边定义
  # ============================================================
  edges:
  
    supply_edges:
    
      - edge_id: ELEC-UPS_EDGE_001
        edge_name: 输入配电至UPS
        edge_type: TRK
        from_node: ELEC-UPS_SRC_AC_INPUT
        to_node: ELEC-UPS_DST_UPS_UNIT
        direction: unidirectional
        medium: ELEC-LV
        
      - edge_id: ELEC-UPS_EDGE_002
        edge_name: 电池至UPS
        edge_type: TRK
        from_node: ELEC-UPS_DST_BATTERY
        to_node: ELEC-UPS_DST_UPS_UNIT
        direction: bidirectional
        medium: ELEC-DC
        note: 充电/放电双向
        
      - edge_id: ELEC-UPS_EDGE_003
        edge_name: UPS至输出柜
        edge_type: TRK
        from_node: ELEC-UPS_DST_UPS_UNIT
        to_node: ELEC-UPS_DST_OUTPUT_PANEL
        direction: unidirectional
        medium: ELEC-UPS
        
      - edge_id: ELEC-UPS_EDGE_004
        edge_name: 输出柜至PDU
        edge_type: BRH
        from_node: ELEC-UPS_DST_OUTPUT_PANEL
        to_node: ELEC-UPS_DST_PDU
        direction: unidirectional
        medium: ELEC-UPS
        
      - edge_id: ELEC-UPS_EDGE_005
        edge_name: PDU至IT设备
        edge_type: TRM
        from_node: ELEC-UPS_DST_PDU
        to_node: ELEC-UPS_SNK_IT
        direction: unidirectional
        medium: ELEC-UPS

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:
  
    - path_id: ELEC-UPS_PATH_NORMAL
      path_name: 正常供电路径
      path_type: SUP
      mode: 市电正常
      sequence:
        - {step: 1, element_type: node, element_id: ELEC-UPS_SRC_AC_INPUT}
        - {step: 2, element_type: edge, element_id: ELEC-UPS_EDGE_001}
        - {step: 3, element_type: node, element_id: ELEC-UPS_DST_UPS_UNIT}
        - {step: 4, element_type: edge, element_id: ELEC-UPS_EDGE_003}
        - {step: 5, element_type: node, element_id: ELEC-UPS_DST_OUTPUT_PANEL}
        - {step: 6, element_type: edge, element_id: ELEC-UPS_EDGE_004}
        - {step: 7, element_type: node, element_id: ELEC-UPS_DST_PDU}
        - {step: 8, element_type: edge, element_id: ELEC-UPS_EDGE_005}
        - {step: 9, element_type: node, element_id: ELEC-UPS_SNK_IT}
        
    - path_id: ELEC-UPS_PATH_BATTERY
      path_name: 电池供电路径
      path_type: BKP
      mode: 市电中断
      sequence:
        - {step: 1, element_type: node, element_id: ELEC-UPS_DST_BATTERY}
        - {step: 2, element_type: edge, element_id: ELEC-UPS_EDGE_002}
        - {step: 3, element_type: node, element_id: ELEC-UPS_DST_UPS_UNIT}
        - {step: 4, element_type: edge, element_id: ELEC-UPS_EDGE_003}
        - {step: 5, element_type: node, element_id: ELEC-UPS_DST_OUTPUT_PANEL}

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:
  
    operating_modes:
      normal:
        description: 市电正常
        operation: 整流→逆变→输出
        battery_state: 浮充
        
      battery:
        description: 市电中断
        operation: 电池→逆变→输出
        trigger: 输入电压异常
        transfer_time: {value: 0, unit: ms}
        
      bypass:
        description: 旁路模式
        operation: 市电直接输出
        trigger: UPS维护或故障
        
    battery_management:
      float_charge: 浮充电压根据温度补偿
      equalize_charge: 定期均衡充电
      discharge_protection: 低电压保护
      
    alarm_logic:
      - condition: 市电异常
        level: 告警
        action: 切换至电池
        
      - condition: 电池低电量
        level: 预警
        action: 通知运维人员
        
      - condition: 电池耗尽
        level: 紧急
        action: 有序关机保护
```

---

## 4.5 MGAS-AGSS 麻醉废气排放系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: MGAS-AGSS
    system_name: 麻醉废气排放系统
    system_name_en: Anesthetic Gas Scavenging System
    category: MEDICAL_GAS
    version: 1.0
    
    description: |
      手术室麻醉废气收集与排放系统，
      收集麻醉机呼出废气，通过管网排至室外或接入排风系统。
      保护手术室内医护人员健康。
      
    design_basis:
      vacuum_level: {value: -25 ~ -50, unit: mmH2O}
      flow_per_terminal: {value: 50, unit: L/min}
      disposal: 高空排放或接入排风
      
    serving_scope:
      - 手术室
      - 产房
      - 胃肠镜室

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: MGAS-AGSS_BND_IN_WASTE
        boundary_name: 麻醉废气
        medium: GAS-AGSS
        source: 麻醉机排气口
        
    outputs:
      - boundary_id: MGAS-AGSS_BND_OUT_EXHAUST
        boundary_name: 废气排放
        medium: AIR-EA
        is_external: true
        target: 大气/排风系统

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:
  
    source_nodes:
    
      - node_id: MGAS-AGSS_SRC_TERMINAL
        node_name: 麻醉废气收集终端
        node_name_en: AGSS Collection Terminal
        node_type: Source_Node
        node_category: SRC
        
        function: 收集麻醉机废气
        medium_out: GAS-AGSS
        
        multiplicity: multiple
        instance_pattern: MGAS-AGSS_SRC_TERMINAL_OR{NN}_{Seq}
        
        equipment_parameters:
          type: 快速接头
          color_code: 紫色
          flow: {value: 50, unit: L/min}
          quantity_per_or: 2
          
        location_hint:
          space_type: PENDANT
          position: 手术室吊塔
          
        typical_quantity:
          per_or: 2

    distribution_nodes:
    
      - node_id: MGAS-AGSS_DST_INTERFACE
        node_name: 麻醉机接口装置
        node_name_en: Anesthesia Machine Interface
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 连接麻醉机APL阀排气
        medium_in: GAS-AGSS
        medium_out: GAS-AGSS
        
        multiplicity: multiple
        
        equipment_parameters:
          type: 开放式/闭合式
          flow_indicator: 有
          adjustment: 流量调节
          
        location_hint:
          space_type: EQUIPMENT
          position: 麻醉机上

      - node_id: MGAS-AGSS_DST_BRANCH
        node_name: 废气支管
        node_name_en: AGSS Branch Pipe
        node_type: Distribution_Node
        node_category: DST
        node_subtype: BRH
        
        function: 收集手术室废气
        medium_in: GAS-AGSS
        medium_out: GAS-AGSS
        
        equipment_parameters:
          material: 铜管/不锈钢管
          diameter: {value: DN25-DN32, unit: mm}
          
        location_hint:
          space_type: CEILING_VOID
          position: 手术室吊顶内

      - node_id: MGAS-AGSS_DST_MAIN_PIPE
        node_name: 废气主管
        node_name_en: AGSS Main Pipe
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
        
        function: 汇集废气
        medium_in: GAS-AGSS
        medium_out: GAS-AGSS
        
        equipment_parameters:
          material: 镀锌钢管/不锈钢管
          diameter: {value: DN50-DN80, unit: mm}
          slope: {value: "≥3‰", note: 向泵站倾斜}
          
        location_hint:
          space_type: CEILING_VOID / SHAFT
          position: 手术部走廊吊顶

      - node_id: MGAS-AGSS_DST_PUMP
        node_name: 废气排放泵
        node_name_en: AGSS Exhaust Pump
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 产生负压、抽排废气
        medium_in: GAS-AGSS
        medium_out: AIR-EA
        
        equipment_parameters:
          type: 专用AGSS泵/真空泵
          flow: {value: 500-1000, unit: L/min}
          vacuum: {value: -50, unit: mmH2O}
          power: {value: 0.5-2, unit: kW}
          configuration: 一用一备
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 医气机房/屋顶
          
        installation_requirements:
          - 通风良好
          - 远离人员区域
          
        control_points:
          sensors:
            - {point_id: AGSS_VAC, type: AI, description: 负压值}
          status:
            - {point_id: AGSS_PUMP_RUN, type: DI, description: 运行状态}
            - {point_id: AGSS_PUMP_FAULT, type: DI, description: 故障报警}

      - node_id: MGAS-AGSS_DST_DILUTION
        node_name: 稀释接口
        node_name_en: Dilution Interface
        node_type: Distribution_Node
        node_category: DST
        node_subtype: JUN
        
        function: 废气与排风混合稀释
        medium_in: [GAS-AGSS, AIR-EA]
        medium_out: AIR-EA
        
        equipment_parameters:
          dilution_ratio: "≥1:10"
          
        location_hint:
          space_type: CEILING_VOID
          position: 排风主管接入点
          
        interface_system: HVAC-CLEAN
        
        note: 接入净化空调排风系统方案

    sink_nodes:
    
      - node_id: MGAS-AGSS_SNK_EXHAUST
        node_name: 废气排放口
        node_name_en: AGSS Exhaust Outlet
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 废气排放
        medium_in: AIR-EA
        is_external: true
        
        location_hint:
          space_type: EXTERIOR
          position: 屋顶高空排放
          height: ≥ 3m高于屋面
          requirement: 远离新风口、人员活动区

  # ============================================================
  # 边定义
  # ============================================================
  edges:
  
    collection_edges:
    
      - edge_id: MGAS-AGSS_EDGE_001
        edge_name: 终端至接口装置
        edge_type: TRM
        from_node: MGAS-AGSS_SRC_TERMINAL
        to_node: MGAS-AGSS_DST_INTERFACE
        direction: unidirectional
        medium: GAS-AGSS
        physical_properties:
          type: 软管连接
          
      - edge_id: MGAS-AGSS_EDGE_002
        edge_name: 接口装置至支管
        edge_type: TRK
        from_node: MGAS-AGSS_DST_INTERFACE
        to_node: MGAS-AGSS_DST_BRANCH
        direction: unidirectional
        medium: GAS-AGSS
        
      - edge_id: MGAS-AGSS_EDGE_003
        edge_name: 支管至主管
        edge_type: BRH
        from_node: MGAS-AGSS_DST_BRANCH
        to_node: MGAS-AGSS_DST_MAIN_PIPE
        direction: unidirectional
        medium: GAS-AGSS

    exhaust_edges_option_1:
      description: 方案一：独立AGSS泵排放
      
      - edge_id: MGAS-AGSS_EDGE_004A
        edge_name: 主管至AGSS泵
        edge_type: TRK
        from_node: MGAS-AGSS_DST_MAIN_PIPE
        to_node: MGAS-AGSS_DST_PUMP
        direction: unidirectional
        medium: GAS-AGSS
        
      - edge_id: MGAS-AGSS_EDGE_005A
        edge_name: AGSS泵至排放口
        edge_type: TRK
        from_node: MGAS-AGSS_DST_PUMP
        to_node: MGAS-AGSS_SNK_EXHAUST
        direction: unidirectional
        medium: AIR-EA

    exhaust_edges_option_2:
      description: 方案二：接入排风系统
      
      - edge_id: MGAS-AGSS_EDGE_004B
        edge_name: 主管至稀释接口
        edge_type: TRK
        from_node: MGAS-AGSS_DST_MAIN_PIPE
        to_node: MGAS-AGSS_DST_DILUTION
        direction: unidirectional
        medium: GAS-AGSS
        
      - edge_id: MGAS-AGSS_EDGE_005B
        edge_name: 稀释接口至排风系统
        edge_type: TRK
        from_node: MGAS-AGSS_DST_DILUTION
        to_node: HVAC-CLEAN_DST_EA_MAIN
        direction: unidirectional
        medium: AIR-EA
        cross_system: true
        target_system: HVAC-CLEAN

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:
  
    - path_id: MGAS-AGSS_PATH_MAIN
      path_name: 麻醉废气排放路径
      path_type: EXH
      sequence:
        - {step: 1, element_type: node, element_id: MGAS-AGSS_SRC_TERMINAL}
        - {step: 2, element_type: edge, element_id: MGAS-AGSS_EDGE_001}
        - {step: 3, element_type: node, element_id: MGAS-AGSS_DST_INTERFACE}
        - {step: 4, element_type: edge, element_id: MGAS-AGSS_EDGE_002}
        - {step: 5, element_type: node, element_id: MGAS-AGSS_DST_BRANCH}
        - {step: 6, element_type: edge, element_id: MGAS-AGSS_EDGE_003}
        - {step: 7, element_type: node, element_id: MGAS-AGSS_DST_MAIN_PIPE}
        - {step: 8, element_type: edge, element_id: MGAS-AGSS_EDGE_004A}
        - {step: 9, element_type: node, element_id: MGAS-AGSS_DST_PUMP}
        - {step: 10, element_type: edge, element_id: MGAS-AGSS_EDGE_005A}
        - {step: 11, element_type: node, element_id: MGAS-AGSS_SNK_EXHAUST}

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:
  
    pump_control:
      mode: 连续运行或联动运行
      interlock: 手术室使用时AGSS泵运行
      
    vacuum_control:
      setpoint: {value: -30 ~ -50, unit: mmH2O}
      alarm: 负压过低/过高
      
    safety_interlock:
      hvac_coordination:
        condition: 接入排风系统方案
        requirement: 排风机运行时AGSS方可排放
        ratio: AGSS流量 ≤ 排风量×10%
```

---

## 4.6 PLUMB-MED-WASTE 医疗废水系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: PLUMB-MED-WASTE
    system_name: 医疗废水系统
    system_name_en: Medical Wastewater System
    category: PLUMBING
    version: 1.0
    
    description: |
      医院医疗废水预处理系统，收集手术室、实验室、放射科等
      特殊医疗区域的废水，经预处理后排入污水处理站或市政管网。
      
    design_basis:
      wastewater_types:
        - 手术废水
        - 实验室废水
        - 传染病房废水
        - 放射性废水（另设）
      treatment: 消毒+预处理
      
    serving_scope:
      - 手术室
      - 检验科
      - 病理科
      - ICU
      - 传染病区

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: PLUMB-MED-WASTE_BND_IN_WASTE
        boundary_name: 医疗废水
        medium: WATER-MED-WASTE
        source: 医疗区域排水
        
    outputs:
      - boundary_id: PLUMB-MED-WASTE_BND_OUT_SAN
        boundary_name: 预处理后废水
        medium: WATER-WASTE
        target_system: PLUMB-SAN

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:
  
    source_nodes:
    
      - node_id: PLUMB-MED-WASTE_SRC_OR
        node_name: 手术室排水
        node_name_en: OR Drain
        node_type: Source_Node
        node_category: SRC
        
        function: 手术废水收集
        medium_out: WATER-MED-WASTE
        
        multiplicity: multiple
        
        equipment_parameters:
          type: 手术区域排水
          contains: 血液、体液、冲洗水
          
        location_hint:
          space_type: FLOOR
          position: 手术室地面排水

      - node_id: PLUMB-MED-WASTE_SRC_LAB
        node_name: 实验室排水
        node_name_en: Laboratory Drain
        node_type: Source_Node
        node_category: SRC
        
        function: 实验废水收集
        medium_out: WATER-MED-WASTE
        
        multiplicity: multiple
        
        equipment_parameters:
          type: 实验室排水
          contains: 化学试剂、生物样品残液
          
        location_hint:
          space_type: COUNTER
          position: 实验台水槽

      - node_id: PLUMB-MED-WASTE_SRC_INFECT
        node_name: 传染病区排水
        node_name_en: Infectious Ward Drain
        node_type: Source_Node
        node_category: SRC
        
        function: 传染性废水收集
        medium_out: WATER-MED-WASTE
        
        multiplicity: multiple
        
        equipment_parameters:
          type: 传染病房排水
          contains: 可能含病原体
          
        location_hint:
          space_type: WET_ROOM
          position: 传染病区卫生间

    distribution_nodes:
    
      - node_id: PLUMB-MED-WASTE_DST_STACK
        node_name: 医疗废水立管
        node_name_en: Medical Waste Stack
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
        
        function: 垂直收集
        medium_in: WATER-MED-WASTE
        medium_out: WATER-MED-WASTE
        
        multiplicity: multiple
        
        equipment_parameters:
          material: HDPE管
          diameter: {value: DN100-DN150, unit: mm}
          
        location_hint:
          space_type: SHAFT
          shaft_type: 污水管井

      - node_id: PLUMB-MED-WASTE_DST_MAIN
        node_name: 医疗废水横干管
        node_name_en: Medical Waste Main
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
        
        function: 汇集至处理站
        medium_in: WATER-MED-WASTE
        medium_out: WATER-MED-WASTE
        
        equipment_parameters:
          material: HDPE管
          diameter: {value: DN150-DN200, unit: mm}
          slope: {value: "0.5-1%", unit: null}
          
        location_hint:
          space_type: CEILING_VOID / TRENCH
          position: 地下室

      - node_id: PLUMB-MED-WASTE_DST_PRETREAT
        node_name: 预处理池
        node_name_en: Pretreatment Tank
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
        
        function: 废水预处理
        medium_in: WATER-MED-WASTE
        medium_out: WATER-WASTE
        
        equipment_parameters:
          type: 预处理池
          components:
            - 调节池
            - 消毒池
            - 沉淀池
          capacity: 按日排水量设计
          retention_time: {value: 1-2, unit: h}
          
        location_hint:
          space_type: OUTDOOR / UNDERGROUND
          position: 污水处理站区域
          
        installation_requirements:
          - 密封防臭
          - 通气管
          - 检修通道
          - 防腐处理

      - node_id: PLUMB-MED-WASTE_DST_DISINFECT
        node_name: 消毒装置
        node_name_en: Disinfection Unit
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRF
        
        function: 废水消毒
        medium_in: WATER-MED-WASTE
        medium_out: WATER-WASTE
        
        equipment_parameters:
          methods:
            - {type: 次氯酸钠, dose: 30-50mg/L}
            - {type: 二氧化氯, dose: 20-30mg/L}
            - {type: 臭氧, dose: 10-20mg/L}
          contact_time: {value: 30-60, unit: min}
          residual_chlorine: {value: 0.5-1.0, unit: mg/L}
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 污水处理站
          
        control_points:
          sensors:
            - {point_id: CL_DOSE, type: AI, description: 加药量}
            - {point_id: CL_RESIDUAL, type: AI, description: 余氯}
            - {point_id: PH, type: AI, description: pH值}
          status:
            - {point_id: DOSE_PUMP_RUN, type: DI, description: 加药泵运行}

      - node_id: PLUMB-MED-WASTE_DST_SAMPLE
        node_name: 取样井
        node_name_en: Sampling Manhole
        node_type: Distribution_Node
        node_category: DST
        node_subtype: MON
        
        function: 水质取样检测
        medium_in: WATER-WASTE
        medium_out: WATER-WASTE
        
        equipment_parameters:
          sampling: 定期取样检测
          parameters: [pH, COD, BOD, 余氯, 大肠杆菌]
          
        location_hint:
          space_type: OUTDOOR
          position: 排放前检查井

    sink_nodes:
    
      - node_id: PLUMB-MED-WASTE_SNK_SEPTIC
        node_name: 化粪池/污水站
        node_name_en: Septic Tank / WWTP
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 进一步处理或排放
        medium_in: WATER-WASTE
        
        interface_system: PLUMB-SAN
        
        location_hint:
          space_type: OUTDOOR
          position: 污水处理站

  # ============================================================
  # 边定义
  # ============================================================
  edges:
  
    collection_edges:
    
      - edge_id: PLUMB-MED-WASTE_EDGE_001
        edge_name: 手术室至立管
        edge_type: TRM
        from_node: PLUMB-MED-WASTE_SRC_OR
        to_node: PLUMB-MED-WASTE_DST_STACK
        direction: unidirectional
        medium: WATER-MED-WASTE
        
      - edge_id: PLUMB-MED-WASTE_EDGE_002
        edge_name: 实验室至立管
        edge_type: TRM
        from_node: PLUMB-MED-WASTE_SRC_LAB
        to_node: PLUMB-MED-WASTE_DST_STACK
        direction: unidirectional
        medium: WATER-MED-WASTE
        
      - edge_id: PLUMB-MED-WASTE_EDGE_003
        edge_name: 传染区至立管
        edge_type: TRM
        from_node: PLUMB-MED-WASTE_SRC_INFECT
        to_node: PLUMB-MED-WASTE_DST_STACK
        direction: unidirectional
        medium: WATER-MED-WASTE
        
      - edge_id: PLUMB-MED-WASTE_EDGE_004
        edge_name: 立管至横干管
        edge_type: BRH
        from_node: PLUMB-MED-WASTE_DST_STACK
        to_node: PLUMB-MED-WASTE_DST_MAIN
        direction: unidirectional
        medium: WATER-MED-WASTE

    treatment_edges:
    
      - edge_id: PLUMB-MED-WASTE_EDGE_005
        edge_name: 横干管至预处理池
        edge_type: TRK
        from_node: PLUMB-MED-WASTE_DST_MAIN
        to_node: PLUMB-MED-WASTE_DST_PRETREAT
        direction: unidirectional
        medium: WATER-MED-WASTE
        
      - edge_id: PLUMB-MED-WASTE_EDGE_006
        edge_name: 预处理池至消毒
        edge_type: TRK
        from_node: PLUMB-MED-WASTE_DST_PRETREAT
        to_node: PLUMB-MED-WASTE_DST_DISINFECT
        direction: unidirectional
        medium: WATER-MED-WASTE
        
      - edge_id: PLUMB-MED-WASTE_EDGE_007
        edge_name: 消毒至取样井
        edge_type: TRK
        from_node: PLUMB-MED-WASTE_DST_DISINFECT
        to_node: PLUMB-MED-WASTE_DST_SAMPLE
        direction: unidirectional
        medium: WATER-WASTE
        
      - edge_id: PLUMB-MED-WASTE_EDGE_008
        edge_name: 取样井至化粪池
        edge_type: TRK
        from_node: PLUMB-MED-WASTE_DST_SAMPLE
        to_node: PLUMB-MED-WASTE_SNK_SEPTIC
        direction: unidirectional
        medium: WATER-WASTE
        cross_system: true
        target_system: PLUMB-SAN

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:
  
    - path_id: PLUMB-MED-WASTE_PATH_MAIN
      path_name: 医疗废水处理路径
      path_type: DRN
      sequence:
        - {step: 1, element_type: node, element_id: PLUMB-MED-WASTE_SRC_OR}
        - {step: 2, element_type: edge, element_id: PLUMB-MED-WASTE_EDGE_001}
        - {step: 3, element_type: node, element_id: PLUMB-MED-WASTE_DST_STACK}
        - {step: 4, element_type: edge, element_id: PLUMB-MED-WASTE_EDGE_004}
        - {step: 5, element_type: node, element_id: PLUMB-MED-WASTE_DST_MAIN}
        - {step: 6, element_type: edge, element_id: PLUMB-MED-WASTE_EDGE_005}
        - {step: 7, element_type: node, element_id: PLUMB-MED-WASTE_DST_PRETREAT}
        - {step: 8, element_type: edge, element_id: PLUMB-MED-WASTE_EDGE_006}
        - {step: 9, element_type: node, element_id: PLUMB-MED-WASTE_DST_DISINFECT}
        - {step: 10, element_type: edge, element_id: PLUMB-MED-WASTE_EDGE_007}
        - {step: 11, element_type: node, element_id: PLUMB-MED-WASTE_DST_SAMPLE}
        - {step: 12, element_type: edge, element_id: PLUMB-MED-WASTE_EDGE_008}
        - {step: 13, element_type: node, element_id: PLUMB-MED-WASTE_SNK_SEPTIC}

  # ============================================================
  # 合规要求
  # ============================================================
  regulatory_requirements:
  
    discharge_standards:
      reference: GB18466 医疗机构水污染物排放标准
      parameters:
        - {parameter: pH, limit: "6-9"}
        - {parameter: COD, limit: "≤250mg/L", note: 预处理标准}
        - {parameter: BOD5, limit: "≤100mg/L"}
        - {parameter: 粪大肠杆菌, limit: "≤5000MPN/L"}
        - {parameter: 余氯, limit: "0.5-1.0mg/L", note: 接触消毒后}
        
    special_waste:
      radioactive:
        description: 放射性废水单独收集处理
        retention_time: 根据同位素半衰期
        
      infectious:
        description: 传染性废水需强化消毒
        chlorine_dose: 增加50%
```

---

## 4.7 FIRE-GAS 气体灭火系统拓扑

```yaml
System_Topology:

  # ============================================================
  # 系统标识
  # ============================================================
  identity:
    system_id: FIRE-GAS
    system_name: 气体灭火系统
    system_name_en: Gas Fire Suppression System
    category: FIRE_PROTECTION
    version: 1.0
    
    description: |
      医院气体灭火系统，用于数据中心、配电室等不宜用水灭火的区域。
      采用七氟丙烷、IG541等洁净气体灭火剂。
      
    design_basis:
      agents:
        - {type: 七氟丙烷, code: HFC-227ea, concentration: "8-10%"}
        - {type: IG541, concentration: "37.5-43%"}
      system_type: 全淹没
      discharge_time: {value: "≤10", unit: s}
      
    serving_scope:
      - 数据中心
      - 高低压配电室
      - UPS机房
      - 发电机控制室

  # ============================================================
  # 系统边界
  # ============================================================
  boundary:
    inputs:
      - boundary_id: FIRE-GAS_BND_IN_FA
        boundary_name: 火灾报警信号
        medium: SIGNAL-FA
        source_system: FIRE-ALARM
        
    outputs:
      - boundary_id: FIRE-GAS_BND_OUT_AGENT
        boundary_name: 灭火剂释放
        medium: GAS-FIRE
        target: 被保护区域

  # ============================================================
  # 节点定义
  # ============================================================
  nodes:
  
    source_nodes:
    
      - node_id: FIRE-GAS_SRC_CYLINDER
        node_name: 灭火剂钢瓶组
        node_name_en: Agent Cylinder Bank
        node_type: Source_Node
        node_category: SRC
        
        function: 储存灭火剂
        medium_out: GAS-FIRE
        
        multiplicity: multiple
        instance_pattern: FIRE-GAS_SRC_CYLINDER_{Zone}
        
        equipment_parameters:
          agent: 七氟丙烷/IG541
          cylinder_volume: {value: 70-180, unit: L}
          pressure: {value: 2.5-4.2, unit: MPa, note: 七氟丙烷}
          quantity: 根据保护区计算
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 钢瓶间
          position: 被保护区域附近
          
        installation_requirements:
          - 防火分隔
          - 通风
          - 温度控制（0-50℃）
          - 压力监测
          - 明显标识
          
        control_points:
          sensors:
            - {point_id: CYL_P, type: AI, description: 钢瓶压力}
            - {point_id: CYL_WEIGHT, type: AI, description: 钢瓶重量}
          status:
            - {point_id: CYL_LOW_P, type: DI, description: 压力低报警}
            - {point_id: CYL_LEAK, type: DI, description: 泄漏报警}

    distribution_nodes:
    
      - node_id: FIRE-GAS_DST_SELECTOR
        node_name: 选择阀
        node_name_en: Selector Valve
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 选择灭火区域
        medium_in: GAS-FIRE
        medium_out: GAS-FIRE
        
        multiplicity: multiple
        
        equipment_parameters:
          type: 电磁选择阀
          size: {value: DN50-DN80, unit: mm}
          
        location_hint:
          space_type: MEP_ROOM
          room_name: 钢瓶间
          
        control_points:
          status:
            - {point_id: SEL_OPEN, type: DI, description: 开启状态}
          commands:
            - {point_id: SEL_CMD, type: DO, description: 开启命令}

      - node_id: FIRE-GAS_DST_PIPE
        node_name: 灭火剂管道
        node_name_en: Agent Pipe
        node_type: Distribution_Node
        node_category: DST
        node_subtype: TRK
        
        function: 灭火剂输送
        medium_in: GAS-FIRE
        medium_out: GAS-FIRE
        
        equipment_parameters:
          material: 无缝钢管
          diameter: {value: DN25-DN80, unit: mm}
          
        location_hint:
          space_type: CEILING_VOID
          position: 被保护区域上方

      - node_id: FIRE-GAS_DST_CONTROL
        node_name: 气体灭火控制器
        node_name_en: Gas Suppression Controller
        node_type: Distribution_Node
        node_category: DST
        node_subtype: REG
        
        function: 系统控制、联动
        medium_in: SIGNAL-FA
        medium_out: CTRL
        
        equipment_parameters:
          functions:
            - 火灾探测确认
            - 声光报警
            - 延时启动
            - 紧急启动/停止
            - 设备联动
            
        location_hint:
          space_type: WALL
          position: 被保护区域入口
          
        control_points:
          status:
            - {point_id: GAS_FIRE, type: DI, description: 火灾确认}
            - {point_id: GAS_RELEASE, type: DI, description: 释放信号}
            - {point_id: GAS_FAULT, type: DI, description: 系统故障}
          commands:
            - {point_id: GAS_MANUAL, type: DO, description: 手动启动}
            - {point_id: GAS_ABORT, type: DO, description: 紧急停止}

    sink_nodes:
    
      - node_id: FIRE-GAS_SNK_NOZZLE
        node_name: 喷嘴
        node_name_en: Discharge Nozzle
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 灭火剂释放
        medium_in: GAS-FIRE
        
        multiplicity: multiple
        
        equipment_parameters:
          type: 全淹没喷嘴
          coverage: 根据保护区计算
          
        location_hint:
          space_type: CEILING
          position: 被保护区域吊顶
          
      - node_id: FIRE-GAS_SNK_ZONE
        node_name: 被保护区域
        node_name_en: Protected Zone
        node_type: Sink_Node
        node_category: SNK
        
        consumption_type: 灭火保护
        medium_in: GAS-FIRE
        
        multiplicity: multiple
        instance_pattern: FIRE-GAS_SNK_ZONE_{ZoneName}
        
        typical_zones:
          - 数据中心机房
          - 高压配电室
          - 低压配电室
          - UPS机房

  # ============================================================
  # 边定义
  # ============================================================
  edges:
  
    supply_edges:
    
      - edge_id: FIRE-GAS_EDGE_001
        edge_name: 钢瓶至选择阀
        edge_type: TRK
        from_node: FIRE-GAS_SRC_CYLINDER
        to_node: FIRE-GAS_DST_SELECTOR
        direction: unidirectional
        medium: GAS-FIRE
        
      - edge_id: FIRE-GAS_EDGE_002
        edge_name: 选择阀至管道
        edge_type: TRK
        from_node: FIRE-GAS_DST_SELECTOR
        to_node: FIRE-GAS_DST_PIPE
        direction: unidirectional
        medium: GAS-FIRE
        
      - edge_id: FIRE-GAS_EDGE_003
        edge_name: 管道至喷嘴
        edge_type: TRM
        from_node: FIRE-GAS_DST_PIPE
        to_node: FIRE-GAS_SNK_NOZZLE
        direction: unidirectional
        medium: GAS-FIRE

    control_edges:
    
      - edge_id: FIRE-GAS_EDGE_FA
        edge_name: 火灾报警联动
        edge_type: CTRL
        from_node: FIRE-ALARM_DST_LINKAGE
        to_node: FIRE-GAS_DST_CONTROL
        direction: unidirectional
        medium: SIGNAL-FA
        cross_system: true
        source_system: FIRE-ALARM

  # ============================================================
  # 路径定义
  # ============================================================
  typical_paths:
  
    - path_id: FIRE-GAS_PATH_MAIN
      path_name: 气体灭火释放路径
      path_type: SUP
      sequence:
        - {step: 1, element_type: node, element_id: FIRE-GAS_SRC_CYLINDER}
        - {step: 2, element_type: edge, element_id: FIRE-GAS_EDGE_001}
        - {step: 3, element_type: node, element_id: FIRE-GAS_DST_SELECTOR}
        - {step: 4, element_type: edge, element_id: FIRE-GAS_EDGE_002}
        - {step: 5, element_type: node, element_id: FIRE-GAS_DST_PIPE}
        - {step: 6, element_type: edge, element_id: FIRE-GAS_EDGE_003}
        - {step: 7, element_type: node, element_id: FIRE-GAS_SNK_NOZZLE}

  # ============================================================
  # 控制逻辑
  # ============================================================
  control_logic:
  
    release_sequence:
      trigger: 同一防护区两个独立探测器报警
      
      actions:
        - step: 1
          action: 火灾确认
          
        - step: 2
          action: 声光报警启动
          
        - step: 3
          action: 关闭空调、通风
          
        - step: 4
          action: 关闭防护区门窗
          
        - step: 5
          action: 延时计时开始
          delay: {value: 30, unit: s}
          purpose: 人员疏散
          
        - step: 6
          action: 开启选择阀
          
        - step: 7
          action: 释放灭火剂
          duration: {value: "≤10", unit: s}
          
        - step: 8
          action: 维持灭火剂浓度
          duration: {value: "≥10", unit: min}
          
    abort_function:
      trigger: 紧急停止按钮
      action: 中断释放程序
      timing: 仅在延时期间有效
      
    manual_release:
      mode: 机械应急启动
      location: 钢瓶间门口
      
    post_release:
      actions:
        - 通风换气（人工启动）
        - 系统复位
        - 钢瓶更换/充装
```

---

## Batch 4 输出总结

```yaml
Batch_4_Summary:

  completed_systems:
    - system_id: HVAC-HWP
      nodes: 12
      edges: 12
      paths: 1
      loops: 1
      
    - system_id: HVAC-SMOKE
      nodes: 12
      edges: 11
      paths: 2
      
    - system_id: PLUMB-HWS
      nodes: 12
      edges: 10
      paths: 1
      loops: 1
      
    - system_id: ELEC-UPS
      nodes: 9
      edges: 5
      paths: 2
      
    - system_id: MGAS-AGSS
      nodes: 8
      edges: 7
      paths: 1
      
    - system_id: PLUMB-MED-WASTE
      nodes: 9
      edges: 8
      paths: 1
      
    - system_id: FIRE-GAS
      nodes: 7
      edges: 4
      paths: 1

  total_batch_4:
    systems: 7
    nodes: 69
    edges: 57
    
  grand_total_all_batches:
    batches: 4
    systems: 26
    estimated_nodes: 280+
    estimated_edges: 240+
```

---

**Batch 1-3 补充文档及Batch 4完整输出完毕。**

如需继续补充P2-IMPORTANT系统（如HVAC-FCU、HVAC-NEG、INT-SEC、INT-NET等），请指示启动Batch 5。

---