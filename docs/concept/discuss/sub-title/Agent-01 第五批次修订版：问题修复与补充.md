## 🧑‍💻 User




---
## 🤖 Assistant


# 第五批次修订版：问题修复与补充

## 修订说明

根据您提出的5个低-中等优先级问题，我将逐一进行修复和补充。

---

## 问题1修复：HVAC系统季节切换高级控制策略

```yaml
Seasonal_Control_Advanced:

  identity:
    name: HVAC季节切换高级控制策略
    description: 根据气候区域和医疗特殊需求的季节性控制
    version: 2.0
    last_updated: 2024
    applicable_systems:
      - HVAC-CHP
      - HVAC-AHU
      - HVAC-FCU

  # ========================================
  # 气候区域差异化配置
  # ========================================
  climate_regions:
    
    northern_china:
      name: 北方严寒/寒冷地区
      representative_cities:
        - 哈尔滨
        - 沈阳
        - 北京
        - 石家庄
      heating_degree_days: {value: ">3000", unit: "℃·d"}
      
      schedule:
        cooling_start:
          calendar: "05/01"
          condition: 室外温度>18℃连续5天
        cooling_end:
          calendar: "09/30"
          condition: 室外温度<15℃连续3天
        heating_start:
          calendar: "10/15"
          condition: 室外温度<12℃连续3天
        heating_end:
          calendar: "04/15"
          condition: 室外温度>10℃连续5天
          
      characteristics:
        winter_outdoor_temp: {value: "-20~0", unit: ℃}
        heating_duration: {value: "5-6", unit: "月"}
        cooling_duration: {value: "3-4", unit: "月"}
        transition_period: 较短（1-2周）
        
    central_china:
      name: 夏热冬冷地区
      representative_cities:
        - 上海
        - 武汉
        - 南京
        - 杭州
      heating_degree_days: {value: "1500-3000", unit: "℃·d"}
      
      schedule:
        cooling_start:
          calendar: "04/15"
          condition: 室外温度>20℃连续3天
        cooling_end:
          calendar: "10/15"
          condition: 室外温度<18℃连续3天
        heating_start:
          calendar: "11/15"
          condition: 室外温度<8℃连续3天
        heating_end:
          calendar: "03/15"
          condition: 室外温度>12℃连续5天
          
      characteristics:
        winter_outdoor_temp: {value: "0~10", unit: ℃}
        heating_duration: {value: "3-4", unit: "月"}
        cooling_duration: {value: "5-6", unit: "月"}
        transition_period: 较长（3-4周）
        high_humidity: 夏季高湿，除湿需求大
        
    southern_china:
      name: 夏热冬暖地区
      representative_cities:
        - 广州
        - 深圳
        - 海南
        - 福州
      heating_degree_days: {value: "<1500", unit: "℃·d"}
      
      schedule:
        cooling_start:
          calendar: "04/01"
          condition: 室外温度>22℃连续3天
        cooling_end:
          calendar: "11/30"
          condition: 室外温度<20℃连续5天
        heating_start:
          calendar: "12/15"
          condition: 室外温度<10℃连续3天（罕见）
        heating_end:
          calendar: "02/15"
          condition: 室外温度>15℃连续3天
          
      characteristics:
        winter_outdoor_temp: {value: "5~15", unit: ℃}
        heating_duration: {value: "0-2", unit: "月"}
        cooling_duration: {value: "7-9", unit: "月"}
        transition_period: 很短或无
        dehumidification: 全年除湿需求
        
    plateau_region:
      name: 高原地区
      representative_cities:
        - 拉萨
        - 西宁
        - 昆明
      altitude: {value: ">2000", unit: m}
      
      schedule:
        cooling_start:
          calendar: "06/01"
          condition: 室外温度>15℃连续5天
        cooling_end:
          calendar: "09/15"
          condition: 室外温度<12℃连续3天
        heating_start:
          calendar: "09/20"
          condition: 室外温度<10℃连续3天
        heating_end:
          calendar: "05/30"
          condition: 室外温度>12℃连续5天
          
      characteristics:
        diurnal_range: 日温差大（15-20℃）
        solar_radiation: 强
        year_round_heating: 高海拔地区可能全年需要加热
        
  # ========================================
  # 医疗关键区域例外处理
  # ========================================
  medical_areas_exception:
    
    description: 关键医疗区域独立于季节切换，全年保持环境稳定
    
    exempt_areas:
      MED-OR:
        name: 手术室
        year_round_behavior:
          cooling: 全年供冷（设备散热+恒温需求）
          heating: 按需供热（冬季或寒冷时段）
        temperature:
          setpoint: {value: 22, unit: ℃}
          range: {value: "20-26", unit: ℃}
        independent_source:
          type: 独立风冷冷热水机组
          capacity: {value: 200, unit: kW}
          backup_for: 主冷热源故障或季节切换期
          
      MED-ICU:
        name: 重症监护室
        year_round_behavior:
          cooling: 全年供冷（监护设备散热）
          heating: 按需供热
        temperature:
          setpoint: {value: 24, unit: ℃}
          range: {value: "22-26", unit: ℃}
        independent_source:
          shared_with: MED-OR（同一备用冷源）
          
      MED-LAB:
        name: 检验科/实验室
        year_round_behavior:
          cooling: 全年供冷（仪器散热+样本保存）
          heating: 按需
        temperature:
          setpoint: {value: 22, unit: ℃}
          stability: {value: "±1", unit: ℃}
        independent_source:
          type: 精密空调或独立小冷机
          
      PHARMACY:
        name: 药房/药库
        year_round_behavior:
          cooling: 全年供冷（药品恒温）
          heating: 防冻
        temperature:
          setpoint: {value: 20, unit: ℃}
          range: {value: "15-25", unit: ℃}
          
      DATA_CENTER:
        name: 数据中心机房
        year_round_behavior:
          cooling: 全年供冷（IT设备散热）
          heating: 无需
        temperature:
          setpoint: {value: 22, unit: ℃}
          range: {value: "18-27", unit: ℃}
        independent_source:
          type: 精密空调
          redundancy: N+1
          
  # ========================================
  # 过渡季节控制策略
  # ========================================
  transition_period_strategy:
    
    definition:
      duration: {value: "2-4", unit: "周"}
      condition: 室外温度在12-18℃波动
      characteristic: 日间需冷、夜间需热
      
    system_behavior:
      four_pipe_system:
        description: 四管制系统可同时供冷供热
        chw_supply: {value: 7, unit: ℃, status: "持续供应"}
        hw_supply: {value: 50, unit: ℃, status: "持续供应"}
        zone_control: 各区域按需选择冷/热
        
      two_pipe_system:
        description: 两管制系统需要切换
        changeover_frequency: 尽量减少（每周最多1次）
        method: 根据天气预报提前切换
        intermediate: 可仅供应温水（30-35℃）
        
    zone_separation:
      principle: 医疗区与普通区分离控制
      
      medical_zone:
        areas:
          - 手术室区域
          - ICU区域
          - 急诊区域
        supply: 独立冷热源，全年稳定
        changeover: 不参与季节切换
        
      general_zone:
        areas:
          - 门诊
          - 病房
          - 办公
          - 后勤
        supply: 主冷热源
        changeover: 正常季节切换
        
    cost_optimization:
      strategies:
        free_cooling:
          trigger: 室外温度<室内设定-3℃
          method: 增加新风比例，减少机械制冷
          saving: 冷机能耗降低50%+
          
        night_purge:
          trigger: 夜间室外温度<18℃
          method: 夜间开窗或加大新风
          purpose: 预冷建筑蓄冷
          
        chw_reset:
          trigger: 过渡季节低负荷
          method: 提高冷冻水供水温度（7→10℃）
          benefit: 提高冷机COP
          
        hw_reset:
          trigger: 过渡季节低负荷
          method: 降低热水供水温度（60→45℃）
          benefit: 减少锅炉燃气消耗
          
        avoid_simultaneous:
          principle: 避免主管路同时供冷热
          method:
            - 过渡季节关闭一侧
            - 或采用分时供应（日间冷、夜间热）
```

---

## 问题2修复：新风分配系统完整设计

```yaml
Fresh_Air_Distribution_System:

  identity:
    name: FCU房间新风分配系统
    description: 定义新风从MAU到FCU房间的完整分配路径
    version: 1.0
    last_updated: 2024
    applicable_systems:
      - HVAC-AHU（MAU新风机组）
      - HVAC-FCU

  # ========================================
  # 系统架构层级
  # ========================================
  system_architecture:
    
    tier_1_central_processing:
      name: 集中新风处理
      equipment: 新风处理机组（MAU）
      location: 设备层/屋顶/地下室
      
      processing_sequence:
        step_1:
          name: 进气段
          components:
            - 新风百叶
            - 防雨罩
            - 防虫网
        step_2:
          name: 初效过滤
          filter: G4
          pressure_drop: {value: "50-100", unit: Pa}
        step_3:
          name: 热回收（可选）
          type: 全热交换器
          efficiency: {value: ">60", unit: "%"}
        step_4:
          name: 表冷/加热
          coil: 冷热盘管
          output_temp:
            summer: {value: 16, unit: ℃}
            winter: {value: 28, unit: ℃}
        step_5:
          name: 加湿（冬季）
          type: 干蒸汽加湿
          target: {value: 40, unit: "%RH"}
        step_6:
          name: 中效过滤
          filter: F7/F8
          pressure_drop: {value: "100-150", unit: Pa}
        step_7:
          name: 送风段
          fan: 离心风机（变频）
          
      output_parameters:
        temperature:
          summer: {value: 18, unit: ℃}
          winter: {value: 24, unit: ℃}
          transition: {value: 22, unit: ℃}
        humidity: {value: "45-55", unit: "%RH"}
        filtration: F7/F8
        
    tier_2_main_distribution:
      name: 主新风管网
      description: 从MAU到各楼层的主干管
      
      duct_parameters:
        material: 镀锌钢板
        thickness: {value: "0.75-1.2", unit: mm}
        insulation:
          material: 橡塑保温
          thickness: {value: 20, unit: mm}
          purpose: 防冷凝
        fire_damper:
          location: 穿越防火分区处
          rating: 70℃易熔片
          
      main_riser:
        description: 新风竖井/立管
        size: 根据服务楼层风量计算
        velocity: {value: "6-8", unit: "m/s"}
        location: 管井内
        
      floor_branch:
        description: 楼层水平主管
        size: 根据楼层风量计算
        velocity: {value: "5-7", unit: "m/s"}
        routing: 走廊吊顶上方
        
    tier_3_floor_header:
      name: 楼层新风分集器
      description: 楼层新风分配中心
      
      equipment:
        header_box:
          name: 新风分配箱
          material: 镀锌钢板
          size: 根据楼层风量
          location: 管井或走廊吊顶
          
        components:
          total_damper:
            name: 楼层总风阀
            type: 电动调节阀
            control: BA联动
          branch_dampers:
            name: 分支调节阀
            type: 手动/电动
            quantity: 每个房间支路一个
          measuring_station:
            name: 风量测量装置
            type: 皮托管阵列/文丘里
            purpose: 调试平衡
            
      control_points:
        sensors:
          - point_id: FH_FA_FLOW
            point_name: 楼层新风总量
            point_type: AI
            unit: "m³/h"
          - point_id: FH_FA_TEMP
            point_name: 新风温度
            point_type: AI
            unit: ℃
        commands:
          - point_id: FH_DAMPER
            point_name: 总风阀开度
            point_type: AO
            range: [0, 100]
            
    tier_4_room_terminal:
      name: 房间新风末端
      description: 新风进入房间的方式
      
      methods:
        method_1:
          name: 新风接入FCU回风口
          description: 新风管接入FCU吸风口，与回风混合
          
          advantages:
            - 新风与回风在FCU内混合均匀
            - 无需额外送风口
            - FCU处理后送出
            
          disadvantages:
            - FCU回风管需要开孔接入
            - 新风量受FCU风量限制
            - 可能影响FCU过滤器寿命
            
          installation:
            connection: DN100-DN150软接头
            position: FCU回风口侧面
            damper: 手动调节阀（调试用）
            
          applicable: 一般病房、办公室
          
        method_2:
          name: 房间壁面独立新风口
          description: 新风通过墙面风口直接进入房间
          
          advantages:
            - 与FCU完全独立
            - 新风直接进入房间
            - FCU故障不影响新风
            
          disadvantages:
            - 可能产生气流短路
            - 冬季冷风感
            - 需要合理布置位置
            
          installation:
            diffuser: 单层百叶风口
            position: 窗户对面墙（远离FCU送风口）
            height: 距地2.2m以上
            velocity: {value: "<2", unit: "m/s"}
            
          applicable: 需要大新风量的房间
          
        method_3:
          name: 吊顶散流器供新风（推荐）
          description: 新风通过吊顶散流器送入房间
          
          advantages:
            - 避免气流短路
            - 与FCU送风相近方式
            - 新风分布均匀
            
          disadvantages:
            - 吊顶开孔增加
            - 需要额外新风支管
            - 防火分区需设防火阀
            
          installation:
            diffuser: 方形散流器/条缝风口
            size: {value: "150×150 - 300×300", unit: mm}
            position: 远离FCU送风口
            fire_damper: 穿越防火分区时设置
            
          applicable: VIP病房、精密控制区域
          
        recommended_selection:
          general_ward: method_1（接入FCU回风口）
          isolation_ward: method_3（独立新风口）
          vip_room: method_3
          office: method_1或method_2
          
  # ========================================
  # 新风量计算与分配
  # ========================================
  fresh_air_calculation:
    
    per_person_requirement:
      standard: GB 50736-2012
      hospital_values:
        ward: {value: 30, unit: "m³/h/人"}
        outpatient: {value: 30, unit: "m³/h/人"}
        office: {value: 30, unit: "m³/h/人"}
        lobby: {value: 20, unit: "m³/h/人"}
        
    design_occupancy:
      single_ward:
        area: {value: 20, unit: "m²"}
        persons: {value: 2, unit: "人"}
        fresh_air: {value: 60, unit: "m³/h"}
      double_ward:
        area: {value: 30, unit: "m²"}
        persons: {value: 3, unit: "人"}
        fresh_air: {value: 90, unit: "m³/h"}
      multi_ward:
        area: {value: 50, unit: "m²"}
        persons: {value: 5, unit: "人"}
        fresh_air: {value: 150, unit: "m³/h"}
      private_office:
        area: {value: 15, unit: "m²"}
        persons: {value: 1, unit: "人"}
        fresh_air: {value: 30, unit: "m³/h"}
        
    minimum_background_ventilation:
      description: 无人时背景通风
      rate: {value: 0.5, unit: "次/h"}
      purpose: 维持室内空气新鲜
      control: 定时器或CO2传感器
      
    total_calculation:
      floor_total: 各房间新风量之和 × 1.1（余量系数）
      building_total: 各楼层之和 × 1.05（管道漏风）
      mau_capacity: 建筑总量 × 1.1（设计余量）
      
  # ========================================
  # 防短路设计
  # ========================================
  short_circuit_prevention:
    
    definition: |
      气流短路指新风送入后未充分混合即被排出或回风，
      导致新风效果不佳。
      
    prevention_measures:
      layout_principle:
        - 新风口与回风口（FCU吸风口）距离>3m
        - 新风送入高度与回风高度不同
        - 新风顺着气流主方向送入
        
      diffuser_selection:
        - 新风口选用低速送风型
        - 避免直吹人体
        - 与FCU送风方向一致或协调
        
      fcu_location:
        - FCU回风口朝向房间内部
        - 避免FCU送风直接对着门/窗
        
      computational_verification:
        method: CFD模拟
        criteria:
          换气效率: ">60%"
          空气龄: "<120s"
          不满意率: "<10%"
          
  # ========================================
  # 新风系统控制
  # ========================================
  control_strategy:
    
    constant_volume:
      description: 定风量新风系统
      method: MAU变频风机维持总风量恒定
      floor_damper: 固定开度（调试后锁定）
      applicable: 一般病房、办公区
      
    demand_controlled:
      description: 需求控制通风（DCV）
      method: 根据CO2浓度调节新风量
      
      sensors:
        co2:
          location: 典型房间或回风管
          setpoint: {value: 800, unit: ppm}
          range: {value: "400-1000", unit: ppm}
        occupancy:
          type: 人体感应/人数统计
          purpose: 无人时减少新风
          
      control:
        co2_high: 增加新风量
        co2_low: 减少新风量（不低于最小值）
        unoccupied: 最小背景通风
        
      applicable: 会议室、大厅、变人数区域
      
    schedule_based:
      description: 时间表控制
      method: 按作息时间调节
      
      schedule:
        occupied_hours:
          time: "07:00-21:00"
          fresh_air: 100%设计值
        unoccupied_hours:
          time: "21:00-07:00"
          fresh_air: 30%设计值（背景通风）
        pre_occupancy:
          time: 提前30分钟
          fresh_air: 100%
          purpose: 预通风
```

---

## 问题3修复：消防电梯基站位置规范

```yaml
Fire_Elevator_Base_Station:

  identity:
    name: 消防电梯基站位置规范
    description: 定义消防电梯及普通电梯火灾时的基站返回规则
    version: 1.0
    last_updated: 2024
    applicable_systems:
      - ELEC-EL

  # ========================================
  # 基站定义与标准要求
  # ========================================
  base_station_definition:
    
    standard_rule:
      reference: GB 7588-2020
      requirement: |
        消防电梯应在首层设置消防员入口和操作盘。
        火灾时，电梯应能返回到消防员入口层（基站）。
        
    base_floor_principle:
      primary: 首层（室外直通层）
      alternate: 室外地面层（如果首层不是）
      
    exceptions:
      - 当首层为着火层时，可返回首层以上或以下一层
      - 特殊建筑可根据消防设计调整
      
  # ========================================
  # 医院特殊情况处理
  # ========================================
  hospital_special_cases:
    
    case_1:
      name: 地下室着火（发电机房/停车场）
      fire_location: B1或B2层
      
      behavior:
        non_fire_elevators:
          destination: 首层
          action: 返回首层，开门后停止
        fire_elevator:
          destination: 首层待命
          action: 消防员可手动控制下行
          note: 消防电梯可下行至地下层
          
      control_logic:
        step_1: 火灾信号（B层）
        step_2: 所有电梯取消B层停靠
        step_3: 非消防电梯返回首层停止
        step_4: 消防电梯在首层待命
        step_5: 消防员持钥匙可控制至任意层
        
    case_2:
      name: 屋顶机房着火
      fire_location: 屋顶层或设备层
      
      behavior:
        all_elevators:
          destination: 首层或顶层以下一层
          action: 避开着火层
        fire_elevator:
          destination: 首层
          action: 待命，可手动上行
          
      control_logic:
        step_1: 火灾信号（顶层）
        step_2: 所有电梯取消顶层停靠
        step_3: 返回首层
        step_4: 消防员可手动控制
        
    case_3:
      name: 首层着火
      fire_location: 首层（正常基站层）
      
      behavior:
        alternate_base:
          primary: 2层（首层以上一层）
          secondary: B1层（首层以下一层）
          selection: 根据消防预案和建筑布局
        all_elevators:
          destination: 替代基站层
          action: 开门后停止
          
      control_logic:
        step_1: 火灾信号（首层）
        step_2: 系统识别首层着火
        step_3: 切换基站至2层
        step_4: 所有电梯返回2层
        step_5: 消防电梯在2层待命
        
    case_4:
      name: 住院楼中层着火
      fire_location: 中间楼层（如5层）
      
      behavior:
        non_fire_elevators:
          destination: 首层
          action: 标准迫降
        fire_elevator:
          destination: 首层
          action: 待命，消防员可上行
          
      control_logic:
        step_1: 火灾信号（5层）
        step_2: 取消5层及相邻层停靠
        step_3: 所有电梯返回首层
        step_4: 消防电梯供消防员使用
        
  # ========================================
  # 完整控制逻辑
  # ========================================
  fire_mode_control_logic:
    
    trigger_conditions:
      - FIRE-FAS火灾确认信号
      - 消防控制室手动触发
      - 电梯机房烟感报警
      
    control_sequence:
      t_0:
        event: 接收火灾确认信号
        action: 进入消防模式
        
      t_1:
        event: 识别着火层
        action: 标记禁停楼层
        
      t_2:
        event: 确定基站位置
        logic: |
          IF 着火层 ≠ 首层 THEN
            基站 = 首层
          ELSE IF 着火层 = 首层 THEN
            基站 = 2层 或 B1层
          END IF
          
      t_3:
        event: 电梯运行控制
        action:
          all_elevators:
            - 取消所有外呼
            - 取消轿内指令（除紧急）
            - 就近停靠开门
            
      t_4:
        event: 乘客疏散
        action:
          - 语音播报："火灾，请从楼梯疏散"
          - 保持开门30秒
          - 确认无人后关门
          
      t_5:
        event: 返回基站
        action:
          non_fire_elevators:
            - 运行至基站层
            - 开门停止
            - 切断运行电源（可选）
          fire_elevator:
            - 运行至基站层
            - 待命
            - 显示"消防专用"
            
      t_6:
        event: 消防员操作
        action:
          - 消防员到达基站
          - 使用消防钥匙/卡片
          - 控制消防电梯运行
          
    prohibited_actions:
      - 消防电梯不响应普通呼叫
      - 不自动停靠着火层
      - 不自动开门（消防员手动控制）
      
  # ========================================
  # 消防电梯专用功能
  # ========================================
  fire_elevator_features:
    
    control_panel:
      location: 首层电梯厅
      functions:
        - 消防开关（钥匙操作）
        - 楼层选择按钮
        - 开/关门按钮
        - 通讯对讲
        
    car_features:
      fire_button:
        location: 轿厢操作盘
        function: 消防专用控制
      priority_key:
        type: 消防钥匙开关
        function: 切换至消防控制
      direct_control:
        description: 持续按住楼层按钮运行
        purpose: 精确控制，防止误操作
        
    operation_mode:
      normal_mode:
        control: 自动群控
        response: 响应所有呼叫
      fire_mode:
        control: 消防员手动
        response: 仅响应轿内消防按钮
        
  # ========================================
  # 冗余与备份
  # ========================================
  redundancy_measures:
    
    backup_communication:
      primary:
        type: 五方对讲系统
        parties:
          - 轿厢
          - 机房
          - 轿顶
          - 底坑
          - 消防控制室
      backup:
        type: 手持无线电
        location: 消防电梯轿厢内
        channel: 消防专用频道
        
    power_supply:
      normal:
        source: 市电
        from: ELEC-LV-MAIN
      backup:
        source: 应急电源
        from: ELEC-EPS
        switchover: {value: "<15", unit: s}
      duration:
        requirement: {value: ">2", unit: h}
        typical: {value: "8+", unit: h}
        
    water_protection:
      description: 消防电梯井道防水
      measures:
        - 井道底部设集水坑
        - 配置排水泵
        - 井道门防水密封
        - 底坑排水能力>10m³/h
        
  # ========================================
  # 测试与维护
  # ========================================
  testing_requirements:
    
    periodic_test:
      frequency: 每月1次
      content:
        - 消防开关功能测试
        - 迫降功能测试
        - 对讲系统测试
        - 应急电源切换测试
        
    annual_drill:
      frequency: 每年1次
      content:
        - 完整消防联动测试
        - 消防员实际操作演练
        - 疏散配合演练
        
    documentation:
      - 测试记录表
      - 故障记录
      - 维修记录
```

---

## 问题4修复：HVAC与消防系统联动

```yaml
CHP_Fire_Interlock:

  identity:
    name: 冷热源与消防系统联动规范
    description: 定义火灾情况下HVAC-CHP系统的响应
    version: 1.0
    last_updated: 2024
    applicable_systems:
      - HVAC-CHP
      - HVAC-AHU
      - HVAC-FCU
      - FIRE-FAS

  # ========================================
  # 联动信号定义
  # ========================================
  interlock_signals:
    
    from_fire_system:
      signal_1:
        name: FIRE_CONFIRM
        description: 火灾确认信号
        from: FIRE-FAS
        type: 干接点
        
      signal_2:
        name: FIRE_FLOOR
        description: 着火楼层信号
        from: FIRE-FAS
        type: 数字信号（楼层编号）
        
      signal_3:
        name: SMOKE_EXHAUST_START
        description: 排烟系统启动信号
        from: FIRE-EXH
        type: 干接点
        
    to_hvac_system:
      signal_1:
        name: HVAC_FIRE_MODE
        description: HVAC消防模式
        to: INT-BA
        action: 触发HVAC消防响应
        
  # ========================================
  # 分区响应策略
  # ========================================
  response_by_zone:
    
    fire_floor:
      name: 着火楼层
      description: 发生火灾的楼层
      
      ahu_response:
        action: 停止该楼层AHU
        sequence:
          step_1: 关闭送风机
          step_2: 关闭回风机
          step_3: 关闭新风阀
          step_4: 关闭送回风阀
        purpose: 防止助燃和烟气扩散
        exception: 如有加压送风，保持运行
        
      fcu_response:
        action: 停止该楼层所有FCU
        sequence:
          step_1: 关闭冷/热水电动阀
          step_2: 停止风机（可选）
        purpose: 减少气流扰动
        
      chw_hw_response:
        action: 关闭该楼层冷热水供应阀
        sequence:
          step_1: 关闭楼层分水器电动阀
          step_2: 保持回水阀开启（循环）
        purpose: 隔离该楼层，防止水损
        note: 保持回水循环防止冷机过热
        
    adjacent_floors:
      name: 相邻楼层（上下各1层）
      description: 着火层上下相邻楼层
      
      ahu_response:
        action: 继续运行或降低风量
        mode: 最小新风模式
        purpose: 维持正压，防止烟气侵入
        
      fcu_response:
        action: 继续正常运行
        monitoring: 监测室温变化
        
      chw_response:
        action: 正常供应
        monitoring:
          parameter: 冷冻水供回水温度
          alarm: 温度升高>3℃时报警
          
    other_floors:
      name: 其他楼层
      description: 未受火灾直接影响的楼层
      
      hvac_response:
        action: 正常运行
        adjustment: 可根据冷热源容量调整
        
    critical_areas:
      name: 关键医疗区域
      description: 手术室、ICU、检验科等
      
      priority: 最高（确保持续运行）
      
      MED-OR:
        name: 手术室
        response:
          step_1: 评估火灾位置与手术室的关系
          step_2:
            if_fire_distant: 继续手术，启动备用冷源
            if_fire_adjacent: 准备转移患者
          step_3: 切换至独立备用冷源
          step_4: 通知手术团队
          step_5: 记录切换时间
          
      MED-ICU:
        name: ICU
        response:
          step_1: 确保供冷供热不中断
          step_2: 启动独立备用冷源
          step_3: 通知医护人员
          
      MED-LAB:
        name: 检验科
        response:
          step_1: 保护样本和仪器
          step_2: 切换至备用冷源
          step_3: 如需疏散，先保存样本
          
  # ========================================
  # 控制时序
  # ========================================
  control_sequence:
    
    timeline:
      t_0s:
        event: 火灾探测器动作
        system: FIRE-FAS
        
      t_30s:
        event: 火灾确认（人工或自动）
        system: FIRE-FAS
        action: 发出火灾确认信号
        
      t_32s:
        event: 联动信号发送
        system: FIRE-FAS
        to: INT-BA
        content:
          - FIRE_CONFIRM
          - FIRE_FLOOR
          
      t_35s:
        event: INT-BA接收并处理
        system: INT-BA
        action: 识别火灾模式，确定响应策略
        
      t_40s:
        event: 着火楼层HVAC停止
        system: HVAC
        action:
          - 关闭着火楼层AHU
          - 关闭着火楼层FCU水阀
          - 关闭楼层冷热水供应阀
          
      t_60s:
        event: 关键区域备用冷源启动
        system: HVAC-CHP（备用）
        action:
          - 启动独立风冷冷热水机组
          - 切换MED-OR/MED-ICU至备用源
          
      t_120s:
        event: 系统稳定
        status:
          - 着火楼层HVAC已隔离
          - 关键区域备用冷源运行
          - 其他楼层正常运行
          
      t_varies:
        event: 主冷机负荷调整
        system: HVAC-CHP
        action:
          - 减少着火楼层负荷后，主冷机减载
          - 群控系统自动调整运行台数
          
  # ========================================
  # 冷热源系统响应
  # ========================================
  chp_system_response:
    
    chiller_response:
      immediate:
        - 继续运行（不停机）
        - 减少着火楼层负荷后自动减载
      monitoring:
        - 冷冻水供回水温度
        - 冷却水温度
        - 冷机负荷率
      alarm:
        - 供水温度>12℃：警告
        - 供水温度>15℃：启动备用冷机
        
    boiler_response:
      immediate:
        - 继续运行（不停机）
        - 减少着火楼层热负荷
      safety:
        - 如锅炉房区域着火，立即停止锅炉
        - 切断燃气供应
        
    pump_response:
      chw_pump:
        action: 继续运行
        adjustment: 根据压差自动调速
      hw_pump:
        action: 继续运行
        adjustment: 根据压差自动调速
      cw_pump:
        action: 继续运行（冷机运行时）
        
    cooling_tower:
      action: 继续运行（冷机运行时）
      
  # ========================================
  # 备用冷源切换
  # ========================================
  backup_source_switchover:
    
    trigger_conditions:
      - 主冷源故障
      - 主冷源区域着火
      - 主冷冻水温度>12℃持续5分钟
      
    backup_equipment:
      type: 独立风冷冷热水机组
      capacity: {value: 200, unit: kW}
      location: 屋顶或独立机房
      served_areas:
        - MED-OR（手术室）
        - MED-ICU（ICU）
        - MED-LAB（检验科，可选）
        
    switchover_sequence:
      step_1:
        action: 启动备用冷源机组
        time: {value: 30, unit: s}
      step_2:
        action: 开启备用源出口阀
        time: {value: 10, unit: s}
      step_3:
        action: 关闭主源接入阀
        time: {value: 10, unit: s}
      step_4:
        action: 确认备用源供水正常
        parameter: 供水温度<10℃
      step_5:
        action: 通知相关人员
        method: BA系统报警+短信
        
    total_switchover_time: {value: "<120", unit: s}
    
    cold_water_buffer:
      description: 切换期间的冷水缓冲
      method: 关键区域管路蓄水量
      duration: {value: "2-3", unit: min}
      note: 确保切换期间无明显温升
      
  # ========================================
  # 火灾后恢复
  # ========================================
  post_fire_recovery:
    
    trigger: 火灾确认解除信号
    source: FIRE-FAS（手动复位）
    
    recovery_sequence:
      step_1:
        action: 确认火灾已扑灭
        verifier: 消防队/安全员
        documentation: 火灾解除确认书
        
      step_2:
        action: 消防系统复位
        includes:
          - 排烟系统停止
          - 加压送风停止
          - 消防电梯返回正常模式
          
      step_3:
        action: 检查着火楼层HVAC设备
        content:
          - 设备损坏情况
          - 管道完整性
          - 电气安全
        duration: {value: "30-60", unit: min}
        
      step_4:
        action: 逐步恢复着火楼层HVAC
        sequence:
          - 开启冷热水供应阀
          - 启动AHU（先低速）
          - 开启FCU水阀
          - 恢复正常运行
        note: 逐步恢复，避免冲击
        
      step_5:
        action: 关键区域备用冷源切回主源
        sequence:
          - 确认主冷源正常
          - 开启主源接入阀
          - 关闭备用源出口阀
          - 停止备用冷源机组
        note: 主源稳定后再切换
        
      step_6:
        action: 全院HVAC恢复正常群控
        status: 正常运行模式
        
    documentation:
      - 火灾时间
      - HVAC响应记录
      - 设备损坏报告
      - 恢复时间
      - 经验总结
```

---

## 问题5修复：FCU冷凝水排放系统

```yaml
Condensate_Drain_System:

  identity:
    name: FCU冷凝水排放系统
    description: 定义风机盘管冷凝水的完整排放链路
    version: 1.0
    last_updated: 2024
    applicable_systems:
      - HVAC-FCU

  # ========================================
  # 系统设计原则
  # ========================================
  design_principles:
    
    purpose:
      - 收集FCU运行时产生的冷凝水
      - 安全排放至排水系统
      - 防止积水、漏水、溢出
      - 避免滋生细菌/霉菌
      
    requirements:
      - 重力自流为主，避免积水
      - 管道保温防止二次冷凝
      - 设置水封/存水弯防臭
      - 关键区域设置溢流报警
      
  # ========================================
  # 冷凝水产生量
  # ========================================
  condensate_generation:
    
    calculation:
      formula: |
        冷凝水量 = 空气处理量 × (进口含湿量 - 出口含湿量)
      
    typical_values:
      small_fcu:
        cooling_capacity: {value: 3.5, unit: kW}
        condensate: {value: "0.5-1.0", unit: "L/h"}
      medium_fcu:
        cooling_capacity: {value: 7, unit: kW}
        condensate: {value: "1.0-2.0", unit: "L/h"}
      large_fcu:
        cooling_capacity: {value: 14, unit: kW}
        condensate: {value: "2.0-4.0", unit: "L/h"}
        
    influencing_factors:
      - 室内湿度（湿度高→冷凝水多）
      - 冷冻水温度（温度低→冷凝水多）
      - FCU运行时间
      - 季节（夏季>其他季节）
      
  # ========================================
  # 排放系统设计
  # ========================================
  drain_system_design:
    
    fcu_drain_pan:
      name: FCU集水盘
      material:
        options:
          - 镀锌钢板（喷涂防腐）
          - 不锈钢
          - ABS塑料
        recommendation: 不锈钢或ABS（医院推荐）
      insulation:
        required: true
        material: 橡塑保温
        thickness: {value: 10, unit: mm}
        purpose: 防止盘外冷凝
      slope:
        direction: 向排水口倾斜
        value: {value: ">1", unit: "%"}
      drain_outlet:
        size: DN20
        position: 最低点
        
    condensate_drain_pipe:
      name: 冷凝水排水管
      
      material:
        options:
          - UPVC（常用）
          - HDPE（柔韧性好）
          - PPR（耐低温）
        recommendation: UPVC或HDPE
        
      sizing:
        principle: 根据FCU数量和冷凝水量
        typical_sizes:
          single_fcu: DN20
          branch_pipe: DN25-DN32
          floor_main: DN40-DN50
          riser: DN50-DN75
          
      slope:
        horizontal_pipe: {value: ">2", unit: "%"}
        note: 确保重力自流
        
      insulation:
        required: true
        material: 橡塑保温
        thickness: {value: 10, unit: mm}
        purpose: 防止管外冷凝
        
    routing_methods:
      method_1:
        name: 立管式集中排放（推荐）
        description: 各楼层冷凝水汇集至专用立管
        
        configuration:
          floor_branch:
            description: 楼层水平支管
            slope: 2%
            connection: 各FCU排水口
          riser:
            description: 冷凝水立管
            location: 管井内
            size: DN50-DN75
          bottom_outlet:
            description: 底部排出
            connection: 污水排水系统
            
        advantages:
          - 集中管理
          - 便于维护
          - 减少堵塞风险
        disadvantages:
          - 需要专用管井空间
          
      method_2:
        name: 分散就近排放
        description: 各FCU冷凝水就近接入卫生间排水
        
        configuration:
          drain_route:
            description: FCU→附近卫生间地漏
            distance: {value: "<5", unit: m}
          trap:
            description: 存水弯
            purpose: 防臭
            
        advantages:
          - 管路短
          - 不需要专用立管
        disadvantages:
          - 分散，难以统一管理
          - 可能影响卫生间
          
    trap_water_seal:
      name: 存水弯/水封
      purpose: 防止排水管臭气倒流
      
      configuration:
        p_trap:
          name: P型存水弯
          location: 每台FCU排水口后
          seal_depth: {value: 50, unit: mm}
        s_trap:
          name: S型存水弯
          application: 特殊安装条件
          
      maintenance:
        issue: 长期不用导致水封干涸
        prevention:
          - 定期补水
          - 使用自动补水装置
          - 空调不运行时保持少量通风
          
  # ========================================
  # 楼层集水系统
  # ========================================
  floor_collection_system:
    
    for_high_rise:
      description: 高层建筑冷凝水收集
      
      floor_header:
        name: 楼层冷凝水汇集管
        size: DN40-DN50
        slope: 2%
        location: 走廊吊顶
        
      cleanout:
        name: 检查口
        interval: {value: 15, unit: m}
        purpose: 清通堵塞
        
    for_basement:
      description: 地下室冷凝水收集
      
      sump_pit:
        name: 集水坑
        size:
          length: {value: 1.0, unit: m}
          width: {value: 0.8, unit: m}
          depth: {value: 0.6, unit: m}
        volume: {value: "0.5-1.0", unit: "m³"}
        location: 地下室最低点
        
      sump_pump:
        name: 潜水排水泵
        type: 小型潜水泵
        flow: {value: 5, unit: "m³/h"}
        head: {value: 10, unit: m}
        quantity: 2台（1用1备）
        control:
          method: 液位开关
          start: 高液位
          stop: 低液位
          alarm: 超高液位
          
      discharge:
        destination: 污水排水系统
        pipe_size: DN50
        check_valve: required
        
  # ========================================
  # 溢出保护
  # ========================================
  overflow_protection:
    
    water_level_switch:
      name: 集水盘水位开关
      type: 浮球开关/电容式开关
      location: FCU集水盘内
      
      trigger_levels:
        normal: 0-30%水位
        warning: 50%水位
        alarm: 80%水位
        
    alarm_response:
      level_warning:
        action:
          - 本地蜂鸣器提示（可听）
          - BA系统显示警告
        operator_action: 检查排水是否通畅
        
      level_alarm:
        action:
          step_1: 关闭该FCU冷水阀
          step_2: 继续运行风机（帮助蒸发）
          step_3: BA系统报警
          step_4: 通知维修人员
        purpose: 防止溢出
        
      recovery:
        condition: 水位恢复正常
        action:
          step_1: 维修人员检查并清理堵塞
          step_2: 手动复位报警
          step_3: 恢复FCU正常运行
          
    secondary_drain:
      name: 备用排水口
      description: 主排水堵塞时的溢流通道
      
      configuration:
        location: 集水盘较高位置
        size: DN20
        route: 独立排水管或接入主排水
        indicator: 如有水流出，表示主排水堵塞
        
  # ========================================
  # 医疗区域特殊要求
  # ========================================
  medical_area_special:
    
    standard_ward:
      name: 普通病房
      
      requirements:
        - 冷凝水不能积存
        - 排水管保温防冷凝
        - 设置溢流报警
        
      drain_system:
        method: 集中立管排放
        outlet: 污水处理系统
        retention_time: {value: "<1", unit: h}
        note: 冷凝水不积存
        
    isolation_ward:
      name: 隔离病房/负压病房
      
      special_requirements:
        - 冷凝水单独收集
        - 消毒处理后排放
        - 防止交叉感染
        
      drain_system:
        collection:
          description: 隔离病房FCU冷凝水独立收集
          tank: 专用消毒收集罐
          capacity: {value: 50, unit: L}
        treatment:
          method: 化学消毒（次氯酸钠）
          contact_time: {value: 30, unit: min}
          concentration: {value: 500, unit: "mg/L"}
        discharge:
          destination: 消毒后进入污水系统
          monitoring: 记录消毒和排放
          
    operating_room:
      name: 手术室
      
      special_requirements:
        - 不产生冷凝水（设计要求）
        - 空调系统采用干盘管或无冷凝设计
        - 如有冷凝，立即排走
        
      drain_system:
        design: 尽量避免冷凝
        backup: 如有冷凝水，直接排入专用管道
        
    icu:
      name: ICU
      
      drain_system:
        method: 与普通病房类似
        additional:
          - 加强保温
          - 双重溢流保护
          - 快速响应报警
          
  # ========================================
  # 维护与清洁
  # ========================================
  maintenance_cleaning:
    
    routine_maintenance:
      frequency: 每月1次
      content:
        - 检查集水盘清洁度
        - 检查排水管通畅
        - 清理存水弯
        - 测试水位开关
        
    deep_cleaning:
      frequency: 每年1次（夏季前）
      content:
        - 集水盘消毒清洗
        - 排水管路冲洗
        - 更换老化密封件
        - 检查保温层完整性
        
    blockage_clearing:
      trigger: 排水不畅或溢流报警
      method:
        step_1: 关闭FCU冷水阀
        step_2: 清理集水盘杂物
        step_3: 疏通排水管（使用疏通器）
        step_4: 冲洗管路
        step_5: 恢复运行，观察
        
    hygiene_control:
      purpose: 防止细菌/霉菌滋生
      measures:
        - 保持排水通畅，不积水
        - 定期消毒集水盘
        - 使用抑菌型集水盘（可选）
        - 空调停用期间保持通风干燥
```

---

# 第五批次修订版完成

## 修订总结

| 问题ID | 描述 | 修复状态 | 修复文档 |
|--------|------|----------|----------|
| P1 | HVAC季节切换时间界定模糊 | ✅ 已修复 | Seasonal_Control_Advanced |
| P2 | 新风分配系统不完整 | ✅ 已修复 | Fresh_Air_Distribution_System |
| P3 | 消防电梯基站位置不清 | ✅ 已修复 | Fire_Elevator_Base_Station |
| P4 | HVAC与消防系统联动缺失 | ✅ 已修复 | CHP_Fire_Interlock |
| P5 | FCU冷凝水排放不完整 | ✅ 已修复 | Condensate_Drain_System |

## 新增/更新文档清单

| 文档名称 | 类型 | 描述 |
|----------|------|------|
| Seasonal_Control_Advanced | 新增 | HVAC季节切换高级控制策略（气候区域+医疗例外） |
| Fresh_Air_Distribution_System | 新增 | FCU房间新风分配完整系统设计 |
| Fire_Elevator_Base_Station | 新增 | 消防电梯基站位置规范 |
| CHP_Fire_Interlock | 新增 | 冷热源与消防系统联动规范 |
| Condensate_Drain_System | 新增 | FCU冷凝水排放系统完整设计 |

---

**下一步：** 请确认第五批次修订版内容，我将继续输出第六批次（最后一批）：
1. PLUMB-RW 雨水系统
2. ELEC-LTG 照明系统
3. 系统间完整依赖关系总图
4. 跨系统联动场景汇总
5. 数据点统计与分类

---