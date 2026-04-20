## 🧑‍💻 User




---
## 🤖 Assistant


感谢您的深刻分析和明确指导。我现在按照您提出的修正框架，立即执行**Priority 1**的三项任务：

---

# AGENT-05 V2.0 架构重构
## 基于超图拓扑与三流动耦合的系统-空间融合模型

---

```yaml
# ═══════════════════════════════════════════════════════════════════════════════
#                    AGENT-05 V2.0 架构重构
#                    HYPERGRAPH TOPOLOGY + THREE-FLOW COUPLING
#                    系统-空间超图拓扑耦合模型
# ═══════════════════════════════════════════════════════════════════════════════

Document_Metadata:
  document_id: "Agent05_V2.0_Restructured"
  version: "2.0-ALPHA"
  restructure_date: "2025-01-15"
  status: "Priority 1 实施中"
  
  paradigm_shift:
    from: "平面多对多映射"
    to: "超图拓扑 + 三流动耦合"
    
  key_improvements:
    - "通用耦合单元数据结构 (DML)"
    - "超图拓扑保持性验证"
    - "物质流-能量流-信息流显式建模"
    - "Agent-02空间功能-行为场景融合"
    - "Agent-04物理方程引用"
```

---

# Part 2: 通用统一耦合单元数据结构 (DML)

```yaml
# ═══════════════════════════════════════════════════════════════════════════════
#                    PART 2: UNIVERSAL COUPLING UNIT DATA STRUCTURE
#                    通用耦合单元数据模型语言 (CU-DML)
# ═══════════════════════════════════════════════════════════════════════════════

Coupling_Unit_Data_Model_Language:
  
  # ─────────────────────────────────────────────────────────────────────────────
  # 2.1 耦合单元基本定义
  # ─────────────────────────────────────────────────────────────────────────────
  
  Section_2_1_Basic_Definition:
    
    definition: |
      耦合单元(Coupling Unit, CU)是医疗建筑系统-空间融合的基本原子单位。
      每个CU描述一个空间节点与一个系统节点之间的完整服务关系，
      包含物质流、能量流、信息流三个维度的完整表达。
      
    design_principles:
      - principle: "拓扑保持性"
        description: "CU必须显式引用Agent-01的系统拓扑和Agent-02的空间拓扑"
      - principle: "三流动完备性"
        description: "每个CU必须包含物质流、能量流、信息流的完整定义"
      - principle: "行为场景绑定"
        description: "CU必须关联Agent-02定义的空间功能-行为场景"
      - principle: "物理方程引用"
        description: "CU应引用Agent-04的物理模型方程"
      - principle: "可计算性"
        description: "CU的所有属性应支持数值计算和仿真"
        
    naming_convention:
      pattern: "CU-{SPACE_ID}-{SYSTEM_ID}-{FLOW_TYPE}"
      examples:
        - "CU-OR001-HVAC_CLN-COOLING"
        - "CU-ICU001-MGAS_O2-SUPPLY"
        - "CU-NICU-ELEC_UPS-POWER"
      components:
        SPACE_ID: "Agent-02定义的空间标识符"
        SYSTEM_ID: "Agent-01定义的系统标识符"
        FLOW_TYPE: "主导流动类型或服务类型"

  # ─────────────────────────────────────────────────────────────────────────────
  # 2.2 耦合单元数据结构模式 (Schema)
  # ─────────────────────────────────────────────────────────────────────────────
  
  Section_2_2_Coupling_Unit_Schema:
    
    schema_version: "2.0"
    
    CouplingUnit:
      
      # ═══════════════════════════════════════════════════════════════════════
      # 标识与元数据
      # ═══════════════════════════════════════════════════════════════════════
      
      identity:
        unit_id:
          type: "string"
          pattern: "CU-{SPACE_ID}-{SYSTEM_ID}-{FLOW_TYPE}"
          required: true
          description: "耦合单元唯一标识符"
          
        unit_name:
          type: "string"
          required: true
          description: "耦合单元人类可读名称"
          example: "手术室OR-001冷却服务耦合"
          
        unit_class:
          type: "enum"
          values: ["HVAC", "MGAS", "ELEC", "PLUMB", "FIRE", "INT", "MULTI"]
          required: true
          description: "耦合单元所属系统大类"
          
        criticality_grade:
          type: "enum"
          values: ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
          required: true
          description: "关键性等级"
          
      # ═══════════════════════════════════════════════════════════════════════
      # 拓扑节点绑定
      # ═══════════════════════════════════════════════════════════════════════
      
      topology_binding:
        
        space_node:
          node_id:
            type: "string"
            source: "Agent-02"
            required: true
            description: "空间节点ID（来自Agent-02空间模型）"
            
          space_type:
            type: "string"
            source: "Agent-02"
            required: true
            description: "空间类型分类"
            example: "手术室-I级"
            
          space_topology_path:
            type: "string"
            source: "Agent-02"
            required: true
            description: "空间在建筑拓扑中的路径"
            example: "Building/Floor3/SurgicalDept/OR-Zone/OR-001"
            
          parent_spaces:
            type: "array[string]"
            source: "Agent-02"
            description: "上级空间节点"
            
          adjacent_spaces:
            type: "array[string]"
            source: "Agent-02"
            description: "相邻空间节点"
            
        system_node:
          node_id:
            type: "string"
            source: "Agent-01"
            required: true
            description: "系统节点ID（来自Agent-01系统模型）"
            
          system_type:
            type: "string"
            source: "Agent-01"
            required: true
            description: "系统类型"
            example: "HVAC-CLN (洁净空调)"
            
          system_topology_path:
            type: "string"
            source: "Agent-01"
            required: true
            description: "系统在MEP拓扑中的路径"
            example: "MEP/HVAC/ColdSource/ChillerPlant/CHP-001"
            
          upstream_systems:
            type: "array[string]"
            source: "Agent-01"
            description: "上游系统节点"
            
          downstream_systems:
            type: "array[string]"
            source: "Agent-01"
            description: "下游系统节点"
            
        device_nodes:
          type: "array[DeviceNode]"
          source: "Agent-03"
          description: "关联的设备节点列表"
          
          DeviceNode:
            device_id: "string"
            device_type: "string"
            device_location: "string"
            device_role: "enum[SOURCE, DISTRIBUTION, TERMINAL, CONTROL, SENSOR]"
            
      # ═══════════════════════════════════════════════════════════════════════
      # Agent-02 功能行为场景绑定
      # ═══════════════════════════════════════════════════════════════════════
      
      functional_behavior_binding:
        
        behavior_scenario:
          scenario_id:
            type: "string"
            source: "Agent-02"
            required: true
            description: "行为场景ID"
            
          scenario_name:
            type: "string"
            source: "Agent-02"
            required: true
            description: "行为场景名称"
            example: "手术进行中"
            
          scenario_phase:
            type: "string"
            source: "Agent-02"
            description: "场景阶段"
            example: "术中-体外循环期"
            
          actors:
            type: "array[string]"
            source: "Agent-02"
            description: "参与者列表"
            example: ["外科医生", "麻醉医生", "灌注师", "护士"]
            
        environmental_requirement:
          requirement_id:
            type: "string"
            source: "Agent-02"
            required: true
            
          parameters:
            type: "array[EnvironmentalParameter]"
            required: true
            
            EnvironmentalParameter:
              parameter_name:
                type: "string"
                required: true
                example: "temperature"
              target_value:
                type: "number"
                required: true
                example: 22
              unit:
                type: "string"
                required: true
                example: "°C"
              tolerance:
                type: "number"
                required: true
                example: 0.5
              control_precision:
                type: "enum"
                values: ["PRECISION", "STANDARD", "COARSE"]
                example: "PRECISION"
              priority:
                type: "enum"
                values: ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
                example: "CRITICAL"
                
        behavior_trigger:
          trigger_type:
            type: "enum"
            values: ["CONTINUOUS", "EVENT_BASED", "SCHEDULED", "CONDITION_BASED"]
            required: true
            
          trigger_condition:
            type: "string"
            description: "触发条件表达式"
            example: "scenario.phase == '术中' AND oxygen_demand > threshold"
            
          trigger_source:
            type: "enum"
            values: ["MEDICAL_PROCESS", "SENSOR", "SCHEDULE", "MANUAL", "EMERGENCY"]
            
      # ═══════════════════════════════════════════════════════════════════════
      # 三流动耦合定义 (核心)
      # ═══════════════════════════════════════════════════════════════════════
      
      three_flow_coupling:
        
        # ─────────────────────────────────────────────────────────────────────
        # 物质流
        # ─────────────────────────────────────────────────────────────────────
        
        material_flow:
          
          enabled:
            type: "boolean"
            required: true
            description: "是否存在物质流"
            
          carrier:
            type: "string"
            required_if: "enabled == true"
            description: "物质载体"
            examples: ["冷冻水", "冷却水", "氧气", "压缩空气", "蒸汽", "电缆", "污水"]
            
          carrier_properties:
            type: "object"
            description: "载体物理属性"
            properties:
              medium_type:
                type: "enum"
                values: ["LIQUID", "GAS", "SOLID", "ELECTRICAL"]
              phase:
                type: "string"
                example: "液态"
              composition:
                type: "string"
                example: "纯水 + 乙二醇15%"
                
          flow_path:
            origin:
              type: "string"
              required: true
              description: "起点位置"
              example: "B1层冷冻站CH-001"
            destination:
              type: "string"
              required: true
              description: "终点位置"
              example: "3F手术室OR-001 AHU-OR-001"
            route:
              type: "array[string]"
              description: "途经路径"
              example: ["B1竖井", "3F水平管廊", "手术部管井"]
            pipe_id:
              type: "string"
              source: "Agent-04"
              description: "管路ID引用"
              
          flow_parameters:
            flow_rate:
              value: "number"
              unit: "string"
              example: { value: 150, unit: "m³/h" }
            velocity:
              value: "number"
              unit: "string"
              example: { value: 1.5, unit: "m/s" }
            pressure:
              supply_pressure:
                value: "number"
                unit: "string"
              return_pressure:
                value: "number"
                unit: "string"
              pressure_drop:
                value: "number"
                unit: "string"
                
          lifecycle_phases:
            type: "object"
            required: true
            description: "物质流全生命周期"
            
            supply:
              description: "供给阶段"
              source_capacity:
                type: "number"
                unit: "string"
              supply_condition:
                type: "object"
                properties:
                  temperature: "number"
                  pressure: "number"
                  quality: "string"
                  
            consumption:
              description: "消耗阶段"
              consumption_rate:
                type: "number"
                unit: "string"
              consumption_pattern:
                type: "enum"
                values: ["CONTINUOUS", "INTERMITTENT", "PEAK_VALLEY"]
              peak_demand:
                type: "number"
                unit: "string"
              average_demand:
                type: "number"
                unit: "string"
                
            return_or_discharge:
              description: "回收或排放阶段"
              return_type:
                type: "enum"
                values: ["CLOSED_LOOP", "OPEN_DISCHARGE", "TREATMENT_REQUIRED", "NONE"]
              return_condition:
                type: "object"
                properties:
                  temperature: "number"
                  pressure: "number"
                  quality: "string"
              treatment:
                type: "string"
                description: "处理要求"
                example: "消毒后排放"
                
          agent04_physics_ref:
            equation_id:
              type: "string"
              source: "Agent-04"
              description: "物理方程引用"
              example: "EQ-FLUID-BERNOULLI-001"
            model_type:
              type: "string"
              example: "Darcy-Weisbach管道压降模型"
              
        # ─────────────────────────────────────────────────────────────────────
        # 能量流
        # ─────────────────────────────────────────────────────────────────────
        
        energy_flow:
          
          enabled:
            type: "boolean"
            required: true
            description: "是否存在能量流"
            
          energy_form:
            type: "enum"
            values: ["THERMAL_COOLING", "THERMAL_HEATING", "ELECTRICAL", "PNEUMATIC", "HYDRAULIC", "RADIANT"]
            required_if: "enabled == true"
            description: "能量形式"
            
          energy_carrier:
            type: "string"
            description: "能量载体（与物质流载体关联）"
            example: "冷冻水"
            
          source_specification:
            source_capacity:
              type: "number"
              unit: "string"
              description: "源端供能能力"
              example: { value: 600, unit: "kW" }
            source_condition:
              type: "object"
              description: "源端能量品质"
              example:
                supply_temperature: 7
                return_temperature: 12
                unit: "°C"
                
          demand_specification:
            design_demand:
              type: "number"
              unit: "string"
              description: "设计需求"
              example: { value: 50, unit: "kW" }
            peak_demand:
              type: "number"
              unit: "string"
              description: "峰值需求"
            average_demand:
              type: "number"
              unit: "string"
              description: "平均需求"
            demand_profile:
              type: "string"
              description: "需求曲线类型"
              example: "手术日高峰型"
              
          energy_balance:
            supply_energy:
              type: "number"
              unit: "string"
              description: "供给能量"
            consumed_energy:
              type: "number"
              unit: "string"
              description: "消耗能量"
            conversion_efficiency:
              type: "number"
              unit: "%"
              description: "转换效率"
              example: 98
            losses:
              type: "object"
              description: "损耗分解"
              properties:
                transmission_loss:
                  value: "number"
                  unit: "%"
                conversion_loss:
                  value: "number"
                  unit: "%"
                  
          surplus_handling:
            surplus_type:
              type: "enum"
              values: ["WASTE_HEAT", "EXCESS_COOLING", "REGENERATIVE", "NONE"]
              description: "余能类型"
            handling_method:
              type: "string"
              description: "处理方式"
              example: "回水进入回水管网，热量回收利用"
            recovery_efficiency:
              type: "number"
              unit: "%"
              
          agent04_physics_ref:
            equation_id:
              type: "string"
              source: "Agent-04"
              example: "EQ-THERMO-HEAT-TRANSFER-001"
            model_type:
              type: "string"
              example: "热交换器NTU-ε模型"
              
        # ─────────────────────────────────────────────────────────────────────
        # 信息流
        # ─────────────────────────────────────────────────────────────────────
        
        information_flow:
          
          enabled:
            type: "boolean"
            required: true
            description: "是否存在信息流"
            
          control_mode:
            type: "enum"
            values: ["OPEN_LOOP", "CLOSED_LOOP", "CASCADE", "FEEDFORWARD", "HYBRID"]
            required_if: "enabled == true"
            description: "控制模式"
            
          sensing_layer:
            sensors:
              type: "array[Sensor]"
              description: "传感器列表"
              
              Sensor:
                sensor_id:
                  type: "string"
                  required: true
                sensor_type:
                  type: "string"
                  required: true
                  example: "温度传感器"
                measured_parameter:
                  type: "string"
                  required: true
                  example: "supply_air_temperature"
                location:
                  type: "string"
                  required: true
                  example: "AHU-OR-001送风口"
                accuracy:
                  type: "number"
                  unit: "string"
                  example: { value: 0.1, unit: "°C" }
                sampling_rate:
                  type: "number"
                  unit: "string"
                  example: { value: 1, unit: "Hz" }
                protocol:
                  type: "string"
                  example: "BACnet/IP"
                  
          transmission_layer:
            network_type:
              type: "enum"
              values: ["BACNET", "MODBUS", "LONWORKS", "KNX", "PROPRIETARY", "WIRELESS"]
            transmission_path:
              type: "string"
              description: "信号传输路径"
              example: "传感器→DDC控制器→BACnet网络→BA主站"
            latency:
              type: "number"
              unit: "string"
              description: "传输延迟"
              example: { value: 100, unit: "ms" }
              
          control_layer:
            controller:
              controller_id:
                type: "string"
                required: true
              controller_type:
                type: "string"
                required: true
                example: "DDC控制器"
              control_algorithm:
                type: "string"
                required: true
                example: "PID温度控制"
              control_parameters:
                type: "object"
                description: "控制参数"
                example:
                  Kp: 2.5
                  Ki: 0.1
                  Kd: 0.5
                  setpoint: 22
                  deadband: 0.5
                  
          actuation_layer:
            actuators:
              type: "array[Actuator]"
              description: "执行器列表"
              
              Actuator:
                actuator_id:
                  type: "string"
                  required: true
                actuator_type:
                  type: "string"
                  required: true
                  example: "电动调节阀"
                controlled_parameter:
                  type: "string"
                  required: true
                  example: "冷冻水流量"
                location:
                  type: "string"
                  required: true
                  example: "AHU-OR-001冷冻水入口"
                range:
                  type: "object"
                  example:
                    min: 0
                    max: 100
                    unit: "%"
                response_time:
                  type: "number"
                  unit: "string"
                  example: { value: 30, unit: "s" }
                  
          feedback_loop:
            loop_type:
              type: "enum"
              values: ["SINGLE_LOOP", "MULTI_LOOP", "CASCADE", "RATIO"]
              required: true
            loop_description:
              type: "string"
              description: "反馈回路描述"
              example: "送风温度→PID控制器→冷冻水阀开度→送风温度"
            stability:
              type: "enum"
              values: ["STABLE", "MARGINALLY_STABLE", "OSCILLATORY"]
            response_characteristics:
              type: "object"
              properties:
                rise_time:
                  value: "number"
                  unit: "string"
                settling_time:
                  value: "number"
                  unit: "string"
                overshoot:
                  value: "number"
                  unit: "%"
                  
          alarm_management:
            alarms:
              type: "array[Alarm]"
              
              Alarm:
                alarm_id:
                  type: "string"
                alarm_condition:
                  type: "string"
                  example: "supply_temperature > 25°C"
                severity:
                  type: "enum"
                  values: ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]
                notification:
                  type: "array[string]"
                  example: ["BA主站", "手术室显示屏", "值班手机"]
                response_action:
                  type: "string"
                  example: "自动切换备用AHU"
                  
      # ═══════════════════════════════════════════════════════════════════════
      # 可靠性与冗余
      # ═══════════════════════════════════════════════════════════════════════
      
      reliability:
        
        reliability_grade:
          type: "enum"
          values: ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
          required: true
          description: "可靠性等级"
          
        availability_target:
          type: "number"
          unit: "%"
          description: "可用性目标"
          example: 99.99
          
        redundancy:
          redundancy_type:
            type: "enum"
            values: ["N+1", "2N", "NONE"]
          backup_system:
            type: "string"
            description: "备用系统"
          switchover_time:
            type: "number"
            unit: "string"
            description: "切换时间"
            example: { value: 0, unit: "s" }
            
        failure_mode:
          failure_scenarios:
            type: "array[FailureScenario]"
            
            FailureScenario:
              scenario_name:
                type: "string"
              probability:
                type: "number"
              impact:
                type: "enum"
                values: ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
              mitigation:
                type: "string"
                
      # ═══════════════════════════════════════════════════════════════════════
      # 验证与审计
      # ═══════════════════════════════════════════════════════════════════════
      
      validation:
        
        topology_validation:
          space_topology_preserved:
            type: "boolean"
            required: true
          system_topology_preserved:
            type: "boolean"
            required: true
          cross_reference_valid:
            type: "boolean"
            required: true
            
        three_flow_completeness:
          material_flow_complete:
            type: "boolean"
            required: true
          energy_flow_complete:
            type: "boolean"
            required: true
          information_flow_complete:
            type: "boolean"
            required: true
            
        agent_cross_reference:
          agent01_ref_valid:
            type: "boolean"
          agent02_ref_valid:
            type: "boolean"
          agent03_ref_valid:
            type: "boolean"
          agent04_ref_valid:
            type: "boolean"
```

---

# Part 3: 超图拓扑耦合模型

```yaml
# ═══════════════════════════════════════════════════════════════════════════════
#                    PART 3: HYPERGRAPH TOPOLOGY COUPLING MODEL
#                    超图拓扑耦合模型
# ═══════════════════════════════════════════════════════════════════════════════

Hypergraph_Coupling_Model:
  
  # ─────────────────────────────────────────────────────────────────────────────
  # 3.1 多维超图定义
  # ─────────────────────────────────────────────────────────────────────────────
  
  Section_3_1_Hypergraph_Definition:
    
    formal_definition: |
      医疗建筑系统-空间耦合超图 H = (V, E, A) 定义如下：
      
      V = V_space ∪ V_system ∪ V_device  (节点集)
        - V_space: 空间节点集（源自Agent-02，保持空间拓扑）
        - V_system: 系统节点集（源自Agent-01，保持系统拓扑）
        - V_device: 设备节点集（源自Agent-03）
        
      E = {e₁, e₂, ..., eₙ}  (超边集)
        - 每条超边 eᵢ ⊆ V 代表一个完整的耦合单元
        - 超边连接多个不同类型的节点
        
      A: E → (M × N × I)  (超边属性映射)
        - M: 物质流属性
        - N: 能量流属性
        - I: 信息流属性
        
    mathematical_notation:
      node_sets:
        V_space: "{s₁, s₂, ..., sₘ} where sᵢ ∈ Agent-02.Spaces"
        V_system: "{y₁, y₂, ..., yₙ} where yⱼ ∈ Agent-01.Systems"
        V_device: "{d₁, d₂, ..., dₖ} where dₖ ∈ Agent-03.Devices"
        
      hyperedge_definition: |
        eᵢ = (sₐ, yᵦ, D_subset) where:
        - sₐ ∈ V_space: 被服务的空间节点
        - yᵦ ∈ V_system: 提供服务的系统节点
        - D_subset ⊆ V_device: 参与的设备节点集
        
      attribute_triple:
        A(eᵢ) = (Mᵢ, Nᵢ, Iᵢ) where:
        - Mᵢ: MaterialFlow (物质流完整定义)
        - Nᵢ: EnergyFlow (能量流完整定义)
        - Iᵢ: InformationFlow (信息流完整定义)
        
    hypergraph_properties:
      - property: "多层关联"
        description: "单条超边可连接3层节点（空间、系统、设备）"
      - property: "属性丰富"
        description: "每条超边携带三流动完整属性"
      - property: "拓扑保持"
        description: "子图分别保持Agent-01/02的原始拓扑"

  # ─────────────────────────────────────────────────────────────────────────────
  # 3.2 节点集定义
  # ─────────────────────────────────────────────────────────────────────────────
  
  Section_3_2_Node_Sets:
    
    space_nodes_V_space:
      
      source: "Agent-02 空间模型"
      
      topology_preservation: |
        空间节点集必须保持Agent-02定义的空间拓扑结构：
        - 建筑层级: Building → Floor → Department → Zone → Room
        - 邻接关系: 空间之间的物理邻接
        - 功能分区: 洁净区/污染区/辅助区
        
      node_structure:
        space_node:
          node_id: "string (Agent-02定义)"
          node_type: "SPACE"
          space_type: "string (如：手术室-I级)"
          hierarchy_level: "enum [BUILDING, FLOOR, DEPARTMENT, ZONE, ROOM]"
          parent_node: "string (上级空间)"
          child_nodes: "array[string] (下级空间)"
          adjacent_nodes: "array[string] (相邻空间)"
          functional_zone: "string (功能分区)"
          agent02_behavior_scenarios: "array[string] (行为场景ID)"
          
      key_space_nodes_example:
        - node_id: "OR-001"
          space_type: "手术室-I级-心外"
          hierarchy_path: "Building/3F/SurgicalDept/OR-Zone/OR-001"
          parent: "OR-Zone"
          adjacent: ["OR-002", "Corridor-OR", "Scrub-001"]
          functional_zone: "洁净区-核心"
          
    system_nodes_V_system:
      
      source: "Agent-01 系统模型"
      
      topology_preservation: |
        系统节点集必须保持Agent-01定义的系统拓扑结构：
        - 系统层级: 大系统 → 子系统 → 设备组
        - 能流关系: 源-干-支-终端
        - 冗余关系: 主备关系
        
      node_structure:
        system_node:
          node_id: "string (Agent-01定义)"
          node_type: "SYSTEM"
          system_type: "string (如：HVAC-CLN)"
          hierarchy_level: "enum [MAJOR_SYSTEM, SUBSYSTEM, EQUIPMENT_GROUP]"
          parent_system: "string (上级系统)"
          child_systems: "array[string] (下级系统)"
          upstream_systems: "array[string] (上游系统-能流)"
          downstream_systems: "array[string] (下游系统-能流)"
          redundant_pair: "string (冗余对)"
          
      key_system_nodes_example:
        - node_id: "HVAC-CLN-OR"
          system_type: "洁净空调-手术部"
          hierarchy_path: "MEP/HVAC/CLN/HVAC-CLN-OR"
          parent: "HVAC-CLN"
          upstream: ["HVAC-CHP (冷源)", "HVAC-HWS (热源)"]
          downstream: ["各手术室终端"]
          
    device_nodes_V_device:
      
      source: "Agent-03 设备模型"
      
      node_structure:
        device_node:
          node_id: "string (Agent-03定义)"
          node_type: "DEVICE"
          device_type: "string (如：组合式空调机组)"
          role: "enum [SOURCE, DISTRIBUTION, TERMINAL, CONTROL, SENSOR]"
          parent_system: "string (所属系统)"
          location: "string (安装位置)"
          served_spaces: "array[string] (服务的空间)"
          
      key_device_nodes_example:
        - node_id: "AHU-OR-001"
          device_type: "组合式空调机组"
          role: "DISTRIBUTION"
          parent_system: "HVAC-CLN-OR"
          location: "3F空调机房"
          served_spaces: ["OR-001", "OR-002"]

  # ─────────────────────────────────────────────────────────────────────────────
  # 3.3 超边集定义
  # ─────────────────────────────────────────────────────────────────────────────
  
  Section_3_3_Hyperedge_Set:
    
    hyperedge_structure:
      
      hyperedge:
        edge_id: "string (唯一标识)"
        edge_name: "string (描述性名称)"
        coupling_unit_id: "string (关联的耦合单元ID)"
        
        connected_nodes:
          space_node: "string (空间节点ID)"
          system_node: "string (系统节点ID)"
          device_nodes: "array[string] (设备节点ID列表)"
          
        flow_attributes:
          material_flow: "MaterialFlowAttribute"
          energy_flow: "EnergyFlowAttribute"
          information_flow: "InformationFlowAttribute"
          
        criticality: "enum [CRITICAL, HIGH, MEDIUM, LOW]"
        reliability_requirement: "number (可用性%)"
        
    hyperedge_examples:
      
      - edge_id: "HE-OR001-HVAC-CLN-COOLING"
        edge_name: "手术室OR-001洁净冷却服务"
        coupling_unit_id: "CU-OR001-HVAC_CLN-COOLING"
        
        connected_nodes:
          space_node: "OR-001"
          system_node: "HVAC-CLN-OR"
          device_nodes: 
            - "CH-001 (冷水机)"
            - "CHWP-001 (冷冻水泵)"
            - "AHU-OR-001 (空调机组)"
            - "TS-OR-001 (温度传感器)"
            - "CV-OR-001 (冷冻水阀)"
            
        flow_attributes:
          material_flow:
            carrier: "冷冻水"
            path: "CH-001→CHWP-001→AHU-OR-001→CH-001"
            flow_rate: "150 m³/h"
            lifecycle: "闭式循环"
          energy_flow:
            form: "冷量"
            supply: "600 kW @ 7°C"
            demand: "50 kW"
            efficiency: "98%"
          information_flow:
            sensors: ["TS-OR-001送风温度", "TS-OR-002回风温度"]
            controller: "DDC-HVAC-001"
            actuators: ["CV-OR-001冷冻水阀"]
            loop: "送风温度PID控制"
            
        criticality: "CRITICAL"
        reliability_requirement: 99.99
        
      - edge_id: "HE-OR001-MGAS-O2-SUPPLY"
        edge_name: "手术室OR-001氧气供应服务"
        coupling_unit_id: "CU-OR001-MGAS_O2-SUPPLY"
        
        connected_nodes:
          space_node: "OR-001"
          system_node: "MGAS-O2"
          device_nodes:
            - "LOX-001 (液氧储罐)"
            - "VAP-001 (汽化器)"
            - "REG-001 (减压器)"
            - "ZV-OR-001 (区域阀)"
            - "OT-OR-001 (氧气终端)"
            - "PS-OR-001 (压力传感器)"
            
        flow_attributes:
          material_flow:
            carrier: "医用氧气"
            path: "LOX-001→VAP-001→REG-001→ZV-OR-001→OT-OR-001"
            flow_rate: "15 L/min (终端)"
            lifecycle: "开式供应"
          energy_flow:
            form: "气体压力能"
            supply: "400 kPa @ 汇流排"
            demand: "400 kPa @ 终端"
            losses: "管道压降 5%"
          information_flow:
            sensors: ["PS-OR-001终端压力", "PS-MAIN主管压力"]
            controller: "MGAS-MC-001"
            actuators: ["切换阀 (自动切换)"]
            alarms: ["低压报警 < 350 kPa"]
            
        criticality: "CRITICAL"
        reliability_requirement: 99.999

  # ─────────────────────────────────────────────────────────────────────────────
  # 3.4 拓扑保持性验证
  # ─────────────────────────────────────────────────────────────────────────────
  
  Section_3_4_Topology_Preservation:
    
    verification_requirements:
      
      space_topology_preservation:
        requirement: |
          超图中的空间节点子图必须与Agent-02的空间拓扑同构：
          - 保持层级关系 (parent-child)
          - 保持邻接关系 (adjacent)
          - 保持功能分区 (functional zone)
          
        verification_method:
          - step: "提取超图中的空间节点子图 G_space"
          - step: "从Agent-02获取原始空间拓扑 T_space"
          - step: "验证 G_space ≅ T_space (图同构)"
          - step: "验证所有边和属性保持一致"
          
        verification_status:
          for_space: "OR-001"
          hierarchy_preserved: true
          adjacent_preserved: true
          functional_zone_preserved: true
          
      system_topology_preservation:
        requirement: |
          超图中的系统节点子图必须与Agent-01的系统拓扑同构：
          - 保持系统层级 (major → sub → equipment)
          - 保持能流关系 (upstream → downstream)
          - 保持冗余关系 (redundant pair)
          
        verification_method:
          - step: "提取超图中的系统节点子图 G_system"
          - step: "从Agent-01获取原始系统拓扑 T_system"
          - step: "验证 G_system ≅ T_system (图同构)"
          - step: "验证能流方向和冗余关系"
          
        verification_status:
          for_system: "HVAC-CLN-OR"
          hierarchy_preserved: true
          energy_flow_preserved: true
          redundancy_preserved: true
          
      cross_topology_consistency:
        requirement: |
          超边连接的节点必须满足语义一致性：
          - 系统节点确实服务于连接的空间节点
          - 设备节点确实属于连接的系统节点
          - 设备节点确实位于或服务于连接的空间节点
          
        verification_method:
          - step: "对每条超边 e = (s, y, D)"
          - step: "验证 y.serves(s) == true"
          - step: "验证 ∀d ∈ D: d.belongs_to(y) == true"
          - step: "验证 ∀d ∈ D: d.serves(s) || d.located_in(s)"

  # ─────────────────────────────────────────────────────────────────────────────
  # 3.5 超图可视化模型
  # ─────────────────────────────────────────────────────────────────────────────
  
  Section_3_5_Visualization:
    
    visualization_layers:
      
      layer_1_space_topology:
        description: "空间拓扑层（底层）"
        display: "建筑平面/剖面视图"
        nodes: "空间节点（房间、区域）"
        edges: "邻接关系、层级关系"
        color_scheme:
          critical_spaces: "红色"
          clinical_spaces: "蓝色"
          support_spaces: "绿色"
          
      layer_2_system_topology:
        description: "系统拓扑层（中层）"
        display: "系统流程图"
        nodes: "系统节点"
        edges: "能流关系、冗余关系"
        color_scheme:
          hvac_systems: "天蓝色"
          electrical_systems: "黄色"
          medical_gas_systems: "绿色"
          plumbing_systems: "深蓝色"
          
      layer_3_coupling_hyperedges:
        description: "耦合超边层（顶层）"
        display: "三维耦合关系图"
        hyperedges: "跨层连接线"
        attributes: "物质流/能量流/信息流标注"
        color_scheme:
          material_flow: "蓝色虚线"
          energy_flow: "红色实线"
          information_flow: "绿色点线"
          
    visualization_example:
      title: "手术室OR-001超图耦合可视化"
      
      ascii_representation: |
        
        ┌─────────────────────── Layer 3: 耦合超边 ───────────────────────┐
        │                                                                  │
        │   [CU-OR001-HVAC_CLN]─────[CU-OR001-MGAS_O2]─────[CU-OR001-ELEC] │
        │         │                       │                      │        │
        │         │ M:冷冻水              │ M:氧气               │ M:电缆  │
        │         │ E:冷量                │ E:压力能             │ E:电能  │
        │         │ I:温度控制            │ I:压力监测           │ I:负荷  │
        │         │                       │                      │        │
        └─────────┼───────────────────────┼──────────────────────┼────────┘
                  │                       │                      │
        ┌─────────┼───────── Layer 2: 系统拓扑 ──────────────────┼────────┐
        │         ▼                       ▼                      ▼        │
        │   [HVAC-CLN-OR]           [MGAS-O2]              [ELEC-UPS]     │
        │      │    │                  │                      │           │
        │   [CHP]  [AHU]            [LOX]──[VAP]──[REG]    [UPS]──[IT]   │
        │                                                                  │
        └─────────────────────────────────────────────────────────────────┘
                  │                       │                      │
        ┌─────────┼───────── Layer 1: 空间拓扑 ──────────────────┼────────┐
        │         ▼                       ▼                      ▼        │
        │   ┌─────────────────────────────────────────────────────────┐   │
        │   │                         OR-001                          │   │
        │   │                    (手术室-I级-心外)                    │   │
        │   │   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │   │
        │   │   │ 层流区  │  │ 手术台  │  │ 设备区  │  │ 麻醉区  │   │   │
        │   │   └─────────┘  └─────────┘  └─────────┘  └─────────┘   │   │
        │   └─────────────────────────────────────────────────────────┘   │
        │         │                                              │        │
        │   [OR-002]◄──Adjacent──►[Corridor-OR]◄──Adjacent──►[Scrub-001] │
        │                                                                  │
        └─────────────────────────────────────────────────────────────────┘
```

---

# Part 4: Agent-02融合模块

```yaml
# ═══════════════════════════════════════════════════════════════════════════════
#                    PART 4: AGENT-02 INTEGRATION MODULE
#                    Agent-02 空间功能-行为场景融合模块
# ═══════════════════════════════════════════════════════════════════════════════

Agent02_Integration_Module:
  
  # ─────────────────────────────────────────────────────────────────────────────
  # 4.1 空间功能-行为场景导入
  # ─────────────────────────────────────────────────────────────────────────────
  
  Section_4_1_Behavior_Scenario_Import:
    
    import_interface:
      source: "Agent-02 医疗工艺流程模型"
      format: "YAML/JSON"
      update_frequency: "与Agent-02同步"
      
    imported_data_structure:
      
      SpaceBehaviorScenario:
        scenario_id: "string"
        space_id: "string (关联空间)"
        scenario_name: "string"
        scenario_type: "enum [MEDICAL_PROCEDURE, DAILY_OPERATION, EMERGENCY, MAINTENANCE]"
        
        actors:
          type: "array[Actor]"
          Actor:
            role: "string"
            count: "number"
            skill_requirement: "string"
            
        timeline:
          type: "array[Phase]"
          Phase:
            phase_id: "string"
            phase_name: "string"
            duration: "number (minutes)"
            start_condition: "string"
            end_condition: "string"
            
        equipment_usage:
          type: "array[EquipmentUse]"
          EquipmentUse:
            equipment_type: "string"
            usage_phase: "array[string] (phase_ids)"
            power_demand: "number (kW)"
            gas_demand: "object {O2, VAC, AIR, N2O, CO2}"
            
        environmental_requirements_by_phase:
          type: "map[phase_id → EnvironmentalRequirement]"
          
    imported_scenarios_for_priority_spaces:
      
      # ═══════════════════════════════════════════════════════════════════════
      # 手术室 OR-001 行为场景
      # ═══════════════════════════════════════════════════════════════════════
      
      OR_001_Scenarios:
        
        - scenario_id: "SCN-OR001-CARDIAC-SURGERY"
          space_id: "OR-001"
          scenario_name: "心脏外科手术"
          scenario_type: "MEDICAL_PROCEDURE"
          
          actors:
            - role: "主刀医生"
              count: 1
            - role: "一助"
              count: 1
            - role: "麻醉医生"
              count: 1
            - role: "灌注师"
              count: 1
            - role: "器械护士"
              count: 1
            - role: "巡回护士"
              count: 2
              
          timeline:
            - phase_id: "P1-PREP"
              phase_name: "术前准备"
              duration: 30
              start_condition: "手术室已清洁消毒"
              end_condition: "患者入室"
              
            - phase_id: "P2-ANESTHESIA"
              phase_name: "麻醉诱导"
              duration: 30
              start_condition: "患者入室"
              end_condition: "麻醉完成，体位摆放完毕"
              
            - phase_id: "P3-PRE-CPB"
              phase_name: "术前准备-建立监测"
              duration: 30
              start_condition: "麻醉完成"
              end_condition: "体外循环准备就绪"
              
            - phase_id: "P4-CPB-ON"
              phase_name: "体外循环期"
              duration: 120
              start_condition: "体外循环启动"
              end_condition: "心脏复跳"
              
            - phase_id: "P5-CPB-WEAN"
              phase_name: "撤离体外循环"
              duration: 60
              start_condition: "心脏复跳"
              end_condition: "完全撤离体外循环"
              
            - phase_id: "P6-CLOSE"
              phase_name: "关胸止血"
              duration: 60
              start_condition: "撤离体外循环"
              end_condition: "手术结束"
              
            - phase_id: "P7-TRANSFER"
              phase_name: "转运"
              duration: 15
              start_condition: "手术结束"
              end_condition: "患者离开手术室"
              
          equipment_usage:
            - equipment_type: "体外循环机"
              usage_phase: ["P4-CPB-ON", "P5-CPB-WEAN"]
              power_demand: 20
              gas_demand:
                O2: "10 L/min"
                
            - equipment_type: "麻醉机"
              usage_phase: ["P2-ANESTHESIA", "P3-PRE-CPB", "P4-CPB-ON", "P5-CPB-WEAN", "P6-CLOSE"]
              power_demand: 0.5
              gas_demand:
                O2: "8 L/min"
                N2O: "4 L/min"
                AIR: "2 L/min"
                
            - equipment_type: "无影灯"
              usage_phase: ["P3-PRE-CPB", "P4-CPB-ON", "P5-CPB-WEAN", "P6-CLOSE"]
              power_demand: 0.8
              
            - equipment_type: "电刀"
              usage_phase: ["P3-PRE-CPB", "P4-CPB-ON", "P5-CPB-WEAN", "P6-CLOSE"]
              power_demand: 0.5
              
            - equipment_type: "监护仪"
              usage_phase: ["P2-ANESTHESIA", "P3-PRE-CPB", "P4-CPB-ON", "P5-CPB-WEAN", "P6-CLOSE", "P7-TRANSFER"]
              power_demand: 0.2
              
          environmental_requirements_by_phase:
            
            P1-PREP:
              temperature:
                setpoint: 22
                tolerance: 2
                unit: "°C"
              humidity:
                setpoint: 50
                tolerance: 10
                unit: "%"
              pressure:
                setpoint: 15
                unit: "Pa"
                reference: "相对洁净走廊"
              cleanliness:
                class: "ISO5"
                laminar_flow: "ON"
              lighting:
                level: "HIGH"
                lux: 500
                
            P2-ANESTHESIA:
              temperature:
                setpoint: 24
                tolerance: 1
                unit: "°C"
              humidity:
                setpoint: 50
                tolerance: 10
                unit: "%"
              pressure:
                setpoint: 15
                unit: "Pa"
              oxygen_demand:
                fio2: "100%"
                flow: "8 L/min"
                
            P4-CPB-ON:
              temperature:
                setpoint: 18
                tolerance: 1
                unit: "°C"
                note: "低温心脏停跳，需要降温"
              humidity:
                setpoint: 50
                tolerance: 5
                unit: "%"
              cooling_demand:
                type: "INCREASED"
                reason: "体外循环机散热 + 房间降温"
                additional_load: 30
                unit: "kW"
              power_demand:
                type: "PEAK"
                ecmo_power: 20
                unit: "kW"
                note: "体外循环机必须UPS保障"
                
            P5-CPB-WEAN:
              temperature:
                setpoint: 22
                tolerance: 1
                unit: "°C"
                note: "逐步复温"
              transition:
                from_temp: 18
                to_temp: 22
                rate: "1°C/10min"
                
      # ═══════════════════════════════════════════════════════════════════════
      # ICU 行为场景
      # ═══════════════════════════════════════════════════════════════════════
      
      ICU_001_Scenarios:
        
        - scenario_id: "SCN-ICU001-POST-CARDIAC"
          space_id: "ICU-001"
          scenario_name: "心外术后监护"
          scenario_type: "MEDICAL_PROCEDURE"
          
          actors:
            - role: "ICU主治医生"
              count: 1
            - role: "ICU护士"
              count: 2
              note: "1:1或1:2护理"
              
          timeline:
            - phase_id: "P1-ADMIT"
              phase_name: "术后转入"
              duration: 30
              
            - phase_id: "P2-STABILIZE"
              phase_name: "稳定期"
              duration: 360
              
            - phase_id: "P3-WEAN-VENT"
              phase_name: "脱机"
              duration: 120
              
            - phase_id: "P4-TRANSFER"
              phase_name: "转出"
              duration: 30
              
          environmental_requirements_by_phase:
            
            P1-ADMIT:
              temperature:
                setpoint: 24
                tolerance: 1
                unit: "°C"
                note: "术后患者保温"
              pressure:
                setpoint: 10
                unit: "Pa"
              oxygen_demand:
                type: "MECHANICAL_VENTILATION"
                fio2: "60-100%"
                
            P2-STABILIZE:
              temperature:
                setpoint: 24
                tolerance: 1
                unit: "°C"
              humidity:
                setpoint: 50
                tolerance: 10
                unit: "%"
              circadian_lighting:
                enabled: true
                daytime_cct: 5000
                nighttime_cct: 2700
                
            P3-WEAN-VENT:
              oxygen_demand:
                type: "REDUCING"
                note: "逐步降低FiO2，准备脱机"

  # ─────────────────────────────────────────────────────────────────────────────
  # 4.2 环境参数需求→系统响应映射
  # ─────────────────────────────────────────────────────────────────────────────
  
  Section_4_2_Requirement_Response_Mapping:
    
    mapping_principle: |
      每个空间环境参数需求必须映射到具体的系统响应：
      需求(Agent-02) → 耦合单元(Agent-05) → 系统配置(Agent-01) → 设备动作(Agent-03)
      
    requirement_response_pairs:
      
      # ─────────────────────────────────────────────────────────────────────────
      # 温度控制映射
      # ─────────────────────────────────────────────────────────────────────────
      
      temperature_control_mappings:
        
        - mapping_id: "MAP-OR001-TEMP"
          
          requirement:
            source: "Agent-02"
            space: "OR-001"
            parameter: "temperature"
            scenario: "心脏外科手术"
            phase: "P4-CPB-ON (体外循环期)"
            value: 18
            tolerance: 1
            unit: "°C"
            priority: "CRITICAL"
            
          system_responses:
            
            - response_id: "RSP-OR001-TEMP-1"
              system: "HVAC-CHP (冷冻站)"
              role: "冷源供给"
              coupling_unit: "CU-OR001-HVAC_CHP-COOLING"
              
              actions:
                - action: "确保冷冻水供水温度"
                  parameter: "supply_water_temp"
                  setpoint: 7
                  unit: "°C"
                  control_method: "冷水机组温度控制"
                  
                - action: "确保冷冻水流量"
                  parameter: "chilled_water_flow"
                  setpoint: 150
                  unit: "m³/h"
                  control_method: "变频泵调节"
                  
              three_flow_impact:
                material_flow: "冷冻水流量增加至设计值"
                energy_flow: "冷量供给 50 kW → 80 kW (增加30kW)"
                information_flow: "冷水机组负荷指令增加"
                
            - response_id: "RSP-OR001-TEMP-2"
              system: "HVAC-CLN-OR (洁净空调)"
              role: "送风温度调节"
              coupling_unit: "CU-OR001-HVAC_CLN-COOLING"
              
              actions:
                - action: "调节送风温度"
                  parameter: "supply_air_temp"
                  setpoint: 16
                  unit: "°C"
                  control_method: "AHU冷冻水阀调节"
                  
                - action: "关闭再热器"
                  parameter: "reheat_valve"
                  setpoint: 0
                  unit: "%"
                  
              three_flow_impact:
                material_flow: "冷冻水阀开度 60% → 100%"
                energy_flow: "送风冷量增加"
                information_flow: "送风温度PID控制，设定值由22°C降至16°C"
                
            - response_id: "RSP-OR001-TEMP-3"
              system: "INT-BA (楼控系统)"
              role: "监控与报警"
              coupling_unit: "CU-OR001-INT_BA-MONITOR"
              
              actions:
                - action: "室内温度监测"
                  parameter: "room_temperature"
                  sampling_rate: "1 Hz"
                  display: "手术室内显示屏"
                  
                - action: "温度报警设置"
                  alarm_high: 20
                  alarm_low: 16
                  unit: "°C"
                  notification: ["BA主站", "手术室护士站"]
                  
              three_flow_impact:
                information_flow: "温度实时监测 + 趋势分析 + 报警"
                
          control_sequence:
            - step: 1
              trigger: "医生下达降温指令"
              actor: "麻醉医生/灌注师"
              
            - step: 2
              action: "BA系统接收温度设定值变更"
              system: "INT-BA"
              
            - step: 3
              action: "AHU送风温度设定值降低"
              system: "HVAC-CLN-OR"
              response_time: "即时"
              
            - step: 4
              action: "冷冻水阀开度增加"
              system: "HVAC-CLN-OR (AHU)"
              response_time: "30s"
              
            - step: 5
              action: "冷水机组负荷增加"
              system: "HVAC-CHP"
              response_time: "2-5min"
              
            - step: 6
              action: "室内温度开始下降"
              expected_rate: "1°C / 5min"
              
            - step: 7
              check: "温度达到设定值"
              action: "进入稳态控制"
              
      # ─────────────────────────────────────────────────────────────────────────
      # 压力梯度控制映射
      # ─────────────────────────────────────────────────────────────────────────
      
      pressure_control_mappings:
        
        - mapping_id: "MAP-ICU001-PRESSURE"
          
          requirement:
            source: "Agent-02"
            space: "ICU-001"
            parameter: "pressure_gradient"
            scenario: "ICU日常运行"
            value: 10
            unit: "Pa"
            reference: "相对走廊"
            direction: "正压"
            priority: "HIGH"
            
          system_responses:
            
            - response_id: "RSP-ICU001-PRES-1"
              system: "HVAC-AHU-ICU"
              role: "送排风平衡"
              coupling_unit: "CU-ICU001-HVAC_AHU-PRESSURE"
              
              actions:
                - action: "维持送排风差"
                  parameter: "supply_exhaust_ratio"
                  value: 1.1
                  note: "送风量比排风量大10%"
                  
                - action: "调节送风量"
                  parameter: "supply_air_volume"
                  setpoint: 3000
                  unit: "m³/h"
                  
                - action: "调节排风量"
                  parameter: "exhaust_air_volume"
                  setpoint: 2700
                  unit: "m³/h"
                  
              three_flow_impact:
                material_flow: "送风3000m³/h，排风2700m³/h"
                energy_flow: "送风机能耗+排风机能耗"
                information_flow: "送排风联动控制"
                
            - response_id: "RSP-ICU001-PRES-2"
              system: "INT-BA"
              role: "压差监控"
              
              actions:
                - action: "压差实时监测"
                  parameter: "differential_pressure"
                  sensor: "DP-ICU-001"
                  sampling_rate: "1 Hz"
                  
                - action: "压差报警"
                  alarm_high: 15
                  alarm_low: 5
                  unit: "Pa"
                  
                - action: "联动控制"
                  condition: "pressure < 5 Pa"
                  action: "增加送风量"
                  
      # ─────────────────────────────────────────────────────────────────────────
      # 氧气供应映射
      # ─────────────────────────────────────────────────────────────────────────
      
      oxygen_supply_mappings:
        
        - mapping_id: "MAP-OR001-O2"
          
          requirement:
            source: "Agent-02"
            space: "OR-001"
            parameter: "oxygen_supply"
            scenario: "心脏外科手术-麻醉诱导"
            phase: "P2-ANESTHESIA"
            demand:
              fio2: "100%"
              flow: "8 L/min"
            priority: "CRITICAL"
            
          system_responses:
            
            - response_id: "RSP-OR001-O2-1"
              system: "MGAS-O2"
              role: "氧气供给"
              coupling_unit: "CU-OR001-MGAS_O2-SUPPLY"
              
              actions:
                - action: "确保终端供气压力"
                  parameter: "terminal_pressure"
                  setpoint: 400
                  tolerance: 40
                  unit: "kPa"
                  
                - action: "确保流量能力"
                  parameter: "flow_capacity"
                  minimum: 15
                  unit: "L/min"
                  
              three_flow_impact:
                material_flow:
                  carrier: "医用氧气"
                  path: "液氧站→汇流排→手术部区域阀→OR-001终端"
                  flow_rate: "8-15 L/min"
                  lifecycle:
                    supply: "液氧储罐 → 汽化 → 减压"
                    consumption: "麻醉机消耗"
                    return: "无 (开式系统)"
                    
                energy_flow:
                  form: "压力势能"
                  supply_pressure: "400 kPa"
                  consumption: "麻醉机减压使用"
                  
                information_flow:
                  sensors: ["终端压力", "区域阀压力", "主管压力"]
                  alarms: ["低压报警 < 350 kPa"]
                  display: "医用气体监控面板"

  # ─────────────────────────────────────────────────────────────────────────────
  # 4.3 医疗工艺流程→系统协调
  # ─────────────────────────────────────────────────────────────────────────────
  
  Section_4_3_Medical_Process_System_Coordination:
    
    process_system_timeline:
      
      example_cardiac_surgery_timeline:
        
        process: "心脏外科手术"
        space: "OR-001"
        total_duration: "约6小时"
        
        timeline_with_system_states:
          
          - time: "T-60min"
            phase: "术前准备"
            medical_action: "手术室清洁消毒完成"
            system_states:
              HVAC-CLN:
                status: "运行"
                mode: "清洁模式"
                air_change: "20次/h"
                laminar_flow: "ON"
              HVAC-CHP:
                status: "待机"
                load: "40%"
              MGAS-O2:
                status: "待机"
                pressure: "400 kPa"
              ELEC-IT:
                status: "正常"
                load: "20%"
                
          - time: "T-30min"
            phase: "设备检查"
            medical_action: "麻醉设备、体外循环设备检查"
            system_states:
              MGAS-O2:
                status: "测试"
                action: "检查终端流量"
              MGAS-VAC:
                status: "测试"
                action: "检查吸引负压"
              ELEC-IT:
                status: "正常"
                action: "麻醉机、监护仪自检"
                
          - time: "T0"
            phase: "患者入室"
            medical_action: "患者进入手术室"
            system_states:
              HVAC-CLN:
                mode: "手术模式"
                temperature: "24°C"
                laminar_flow: "ON"
              lighting:
                mode: "高亮度"
                lux: 500
                
          - time: "T+30min"
            phase: "麻醉诱导"
            medical_action: "全麻诱导、插管"
            system_states:
              MGAS-O2:
                status: "使用中"
                demand: "8 L/min"
                fio2: "100%"
              MGAS-N2O:
                status: "使用中"
                demand: "4 L/min"
              ELEC-IT:
                load: "40%"
                devices_active: ["麻醉机", "监护仪", "输液泵"]
                
          - time: "T+60min"
            phase: "开胸、建立体外循环"
            medical_action: "正中开胸、插管、建立体外循环"
            system_states:
              HVAC-CLN:
                temperature: "22→18°C"
                mode: "降温模式"
                action: "开始降温"
              HVAC-CHP:
                load: "60%→80%"
                action: "增加冷量供给"
              ELEC-UPS:
                load: "增加"
                critical_load: "体外循环机上线"
                
          - time: "T+90min to T+210min"
            phase: "体外循环期"
            medical_action: "心脏停跳、手术操作"
            system_states:
              HVAC-CLN:
                temperature: "18°C"
                status: "维持"
              ELEC-UPS:
                load: "峰值"
                ecmo_power: "20 kW"
                priority: "CRITICAL"
              MGAS-O2:
                demand: "10 L/min (体外循环)"
              cooling:
                status: "PEAK"
                additional_load: "30 kW"
                
          - time: "T+210min"
            phase: "心脏复跳、撤离体外循环"
            medical_action: "复温、心脏复跳"
            system_states:
              HVAC-CLN:
                temperature: "18→22°C"
                action: "开始复温"
                rate: "1°C/10min"
              ELEC-UPS:
                load: "下降"
                ecmo: "逐步撤离"
                
          - time: "T+270min"
            phase: "关胸"
            medical_action: "止血、关胸"
            system_states:
              HVAC-CLN:
                temperature: "22°C"
                mode: "正常手术"
              ELEC:
                load: "正常"
                
          - time: "T+330min"
            phase: "转运"
            medical_action: "患者转ICU"
            system_states:
              HVAC-CLN:
                mode: "待机→清洁"
              MGAS:
                status: "关闭"
              lighting:
                mode: "清洁模式"

  # ─────────────────────────────────────────────────────────────────────────────
  # 4.4 空间分类与系统配置矩阵
  # ─────────────────────────────────────────────────────────────────────────────
  
  Section_4_4_Space_Classification_System_Matrix:
    
    description: |
      基于Agent-02的空间功能分类，直接映射到系统配置需求。
      这是Agent-05的核心输出之一，供Agent-06/07/08使用。
      
    classification_system_matrix:
      
      # ─────────────────────────────────────────────────────────────────────────
      # 手术室类空间
      # ─────────────────────────────────────────────────────────────────────────
      
      surgical_spaces:
        
        - classification: "手术室-I级 (心外/神外/器官移植)"
          agent02_space_types:
            - "心脏外科手术室"
            - "神经外科手术室"
            - "器官移植手术室"
            
          mandatory_systems:
            HVAC:
              - system: "HVAC-CLN"
                specification:
                  cleanliness: "ISO 5"
                  air_change: "≥25次/h (其中层流≥15)"
                  laminar_flow_area: "3.0m×3.0m"
                  filtration: "H13 HEPA"
              - system: "HVAC-CHP"
                coupling: "提供冷源"
              - system: "HVAC-HWS"
                coupling: "提供热源 (再热)"
                
            MGAS:
              - system: "MGAS-O2"
                terminals: 4
              - system: "MGAS-VAC"
                terminals: 4
              - system: "MGAS-AIR"
                terminals: 2
              - system: "MGAS-N2O"
                terminals: 1
              - system: "MGAS-CO2"
                terminals: 1
                condition: "心外科"
                
            ELEC:
              - system: "ELEC-IT"
                capacity: "10 kVA"
              - system: "ELEC-UPS"
                capacity: "60 kVA"
                note: "含体外循环机专用"
                
            INT:
              - system: "INT-BA"
              - system: "INT-NUR"
              - system: "INT-NET"
              
          environmental_parameters:
            temperature:
              range: "18-26°C"
              precision: "±1°C"
              adjustable: true
            humidity:
              range: "40-60%"
              precision: "±10%"
            pressure:
              value: "+15Pa"
              gradient: "洁净区>走廊>污物区"
              
          special_requirements:
            - "体外循环工艺冷却水接口"
            - "杂交手术室需增加射线防护"
            
        - classification: "手术室-II级 (骨科/普外/妇产)"
          agent02_space_types:
            - "骨科手术室"
            - "普外科手术室"
            - "妇产科手术室"
            
          mandatory_systems:
            HVAC:
              - system: "HVAC-CLN"
                specification:
                  cleanliness: "ISO 6"
                  air_change: "≥20次/h"
                  laminar_flow_area: "2.4m×2.4m"
                  
            MGAS:
              - system: "MGAS-O2"
                terminals: 2
              - system: "MGAS-VAC"
                terminals: 2
              - system: "MGAS-AIR"
                terminals: 1
              - system: "MGAS-N2O"
                terminals: 1
              - system: "MGAS-CO2"
                terminals: 1
                condition: "腹腔镜手术"
                
            ELEC:
              - system: "ELEC-IT"
                capacity: "8 kVA"
              - system: "ELEC-UPS"
                capacity: "15 kVA"
                
      # ─────────────────────────────────────────────────────────────────────────
      # ICU类空间
      # ─────────────────────────────────────────────────────────────────────────
      
      icu_spaces:
        
        - classification: "ICU-综合/心外术后"
          agent02_space_types:
            - "综合ICU"
            - "心外ICU"
            - "神外ICU"
            
          mandatory_systems:
            HVAC:
              - system: "HVAC-AHU-ICU"
                specification:
                  cleanliness: "ISO 7"
                  air_change: "≥12次/h"
                  pressure: "+10Pa"
                  
            MGAS:
              - system: "MGAS-O2"
                terminals_per_bed: 2
              - system: "MGAS-VAC"
                terminals_per_bed: 2
              - system: "MGAS-AIR"
                terminals_per_bed: 1
                
            ELEC:
              - system: "ELEC-IT"
                capacity: "5 kVA/4床"
              - system: "ELEC-UPS"
                scope: "生命支持设备"
                
          special_requirements:
            - "昼夜节律照明"
            - "2-3床负压隔离能力"
            
        - classification: "NICU (新生儿重症)"
          agent02_space_types:
            - "新生儿重症监护室"
            
          mandatory_systems:
            HVAC:
              - system: "HVAC-PAC"
                specification:
                  temperature_precision: "±0.5°C"
                  humidity_precision: "±5%"
                  cleanliness: "ISO 7"
                  zone_control: true
                  
            MGAS:
              - system: "MGAS-O2"
                terminals_per_bed: 2
                feature: "氧气-空气混合器"
              - system: "MGAS-VAC"
                terminals_per_bed: 2
                
            ELEC:
              - system: "ELEC-IT"
                capacity: "5 kVA/4床"
              - system: "ELEC-UPS"
                scope: "暖箱必须保障"
                
          special_requirements:
            - "恒温恒湿精密控制"
            - "噪声≤40dB(A)"
            - "可调光照明"
```

---

# Part 5: 5个关键空间耦合单元实例库

```yaml
# ═══════════════════════════════════════════════════════════════════════════════
#                    PART 5: COUPLING UNIT INSTANCE LIBRARY
#                    5个关键空间的完整耦合单元实例库
# ═══════════════════════════════════════════════════════════════════════════════

Coupling_Unit_Instance_Library:
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 5.1 手术室 OR-001 完整耦合单元集
  # ═══════════════════════════════════════════════════════════════════════════
  
  OR_001_Coupling_Units:
    
    space_id: "OR-001"
    space_name: "心脏外科手术室"
    space_type: "手术室-I级-心外"
    coupling_unit_count: 12
    
    units:
      
      # ─────────────────────────────────────────────────────────────────────────
      # CU-1: 洁净空调冷却服务
      # ─────────────────────────────────────────────────────────────────────────
      
      - unit_id: "CU-OR001-HVAC_CLN-COOLING"
        unit_name: "手术室OR-001洁净空调冷却服务"
        unit_class: "HVAC"
        criticality_grade: "CRITICAL"
        
        topology_binding:
          space_node:
            node_id: "OR-001"
            space_type: "手术室-I级-心外"
            space_topology_path: "Building/3F/SurgicalDept/OR-Zone/OR-001"
            parent_spaces: ["OR-Zone", "SurgicalDept"]
            adjacent_spaces: ["OR-002", "Corridor-OR", "Scrub-001"]
            
          system_node:
            node_id: "HVAC-CLN-OR"
            system_type: "洁净空调系统-手术部"
            system_topology_path: "MEP/HVAC/CLN/HVAC-CLN-OR"
            upstream_systems: ["HVAC-CHP", "HVAC-HWS"]
            downstream_systems: ["终端设备"]
            
          device_nodes:
            - device_id: "CH-001"
              device_type: "离心式冷水机组"
              device_role: "SOURCE"
              location: "B1冷冻站"
            - device_id: "CHWP-001"
              device_type: "冷冻水循环泵"
              device_role: "DISTRIBUTION"
              location: "B1冷冻站"
            - device_id: "AHU-OR-001"
              device_type: "组合式空调机组"
              device_role: "DISTRIBUTION"
              location: "3F空调机房"
            - device_id: "HEPA-OR-001"
              device_type: "高效过滤送风单元"
              device_role: "TERMINAL"
              location: "OR-001天花板"
              
        functional_behavior_binding:
          behavior_scenario:
            scenario_id: "SCN-OR001-CARDIAC-SURGERY"
            scenario_name: "心脏外科手术"
            scenario_phase: "P4-CPB-ON (体外循环期)"
            actors: ["主刀医生", "灌注师", "麻醉医生", "护士"]
            
          environmental_requirement:
            requirement_id: "REQ-OR001-TEMP-CPB"
            parameters:
              - parameter_name: "temperature"
                target_value: 18
                unit: "°C"
                tolerance: 1
                control_precision: "PRECISION"
                priority: "CRITICAL"
                
          behavior_trigger:
            trigger_type: "EVENT_BASED"
            trigger_condition: "phase == 'P4-CPB-ON' AND surgeon_command == 'cool_down'"
            trigger_source: "MEDICAL_PROCESS"
            
        three_flow_coupling:
          
          material_flow:
            enabled: true
            carrier: "冷冻水"
            carrier_properties:
              medium_type: "LIQUID"
              phase: "液态"
              composition: "纯水 + 乙二醇15%"
              
            flow_path:
              origin: "B1层冷冻站CH-001"
              destination: "3F手术室AHU-OR-001表冷器"
              route: ["B1竖井SH-01", "3F水平管廊", "手术部管井MR-OR"]
              pipe_id: "PIPE-CHW-OR-001"
              
            flow_parameters:
              flow_rate:
                value: 150
                unit: "m³/h"
              velocity:
                value: 1.5
                unit: "m/s"
              pressure:
                supply_pressure:
                  value: 0.6
                  unit: "MPa"
                return_pressure:
                  value: 0.4
                  unit: "MPa"
                pressure_drop:
                  value: 0.2
                  unit: "MPa"
                  
            lifecycle_phases:
              supply:
                source_capacity:
                  value: 600
                  unit: "kW"
                supply_condition:
                  temperature: 7
                  pressure: 0.6
                  unit: "°C / MPa"
                  
              consumption:
                consumption_rate:
                  design: 50
                  peak: 80
                  unit: "kW"
                consumption_pattern: "PEAK_VALLEY"
                note: "体外循环期峰值"
                
              return_or_discharge:
                return_type: "CLOSED_LOOP"
                return_condition:
                  temperature: 12
                  pressure: 0.4
                  
            agent04_physics_ref:
              equation_id: "EQ-FLUID-PIPE-001"
              model_type: "Darcy-Weisbach管道压降模型"
              
          energy_flow:
            enabled: true
            energy_form: "THERMAL_COOLING"
            energy_carrier: "冷冻水"
            
            source_specification:
              source_capacity:
                value: 600
                unit: "kW"
              source_condition:
                supply_temperature: 7
                return_temperature: 12
                unit: "°C"
                delta_t: 5
                
            demand_specification:
              design_demand:
                value: 50
                unit: "kW"
              peak_demand:
                value: 80
                unit: "kW"
                condition: "体外循环期 + 房间降温"
              average_demand:
                value: 40
                unit: "kW"
              demand_profile: "手术日高峰型"
              
            energy_balance:
              supply_energy:
                value: 80
                unit: "kW"
              consumed_energy:
                value: 78.4
                unit: "kW"
              conversion_efficiency:
                value: 98
                unit: "%"
              losses:
                transmission_loss:
                  value: 2
                  unit: "%"
                  note: "管道热损失"
                  
            surplus_handling:
              surplus_type: "NONE"
              note: "按需供给，无余能"
              
            agent04_physics_ref:
              equation_id: "EQ-THERMO-HX-001"
              model_type: "表冷器热交换模型 Q=m·Cp·ΔT"
              
          information_flow:
            enabled: true
            control_mode: "CLOSED_LOOP"
            
            sensing_layer:
              sensors:
                - sensor_id: "TS-OR-001-SA"
                  sensor_type: "温度传感器"
                  measured_parameter: "supply_air_temperature"
                  location: "AHU-OR-001送风口"
                  accuracy:
                    value: 0.1
                    unit: "°C"
                  sampling_rate:
                    value: 1
                    unit: "Hz"
                  protocol: "BACnet/IP"
                  
                - sensor_id: "TS-OR-001-RA"
                  sensor_type: "温度传感器"
                  measured_parameter: "return_air_temperature"
                  location: "OR-001回风口"
                  accuracy:
                    value: 0.1
                    unit: "°C"
                    
                - sensor_id: "TS-OR-001-RM"
                  sensor_type: "温度传感器"
                  measured_parameter: "room_temperature"
                  location: "OR-001室内"
                  accuracy:
                    value: 0.1
                    unit: "°C"
                    
            transmission_layer:
              network_type: "BACNET"
              transmission_path: "传感器→DDC-OR-001→BACnet网络→BA主站"
              latency:
                value: 100
                unit: "ms"
                
            control_layer:
              controller:
                controller_id: "DDC-OR-001"
                controller_type: "DDC控制器"
                control_algorithm: "PID温度控制"
                control_parameters:
                  Kp: 2.5
                  Ki: 0.1
                  Kd: 0.5
                  setpoint: 22
                  deadband: 0.5
                  
            actuation_layer:
              actuators:
                - actuator_id: "CV-OR-001"
                  actuator_type: "电动调节阀"
                  controlled_parameter: "冷冻水流量"
                  location: "AHU-OR-001冷冻水入口"
                  range:
                    min: 0
                    max: 100
                    unit: "%"
                  response_time:
                    value: 30
                    unit: "s"
                    
                - actuator_id: "VFD-AHU-OR-001"
                  actuator_type: "变频器"
                  controlled_parameter: "送风量"
                  location: "AHU-OR-001"
                  range:
                    min: 30
                    max: 100
                    unit: "%"
                    
            feedback_loop:
              loop_type: "CASCADE"
              loop_description: |
                外环：室温→设定值比较→送风温度设定
                内环：送风温度→PID控制→冷冻水阀开度→送风温度
              stability: "STABLE"
              response_characteristics:
                rise_time:
                  value: 5
                  unit: "min"
                settling_time:
                  value: 15
                  unit: "min"
                overshoot:
                  value: 5
                  unit: "%"
                  
            alarm_management:
              alarms:
                - alarm_id: "ALM-OR-001-TEMP-HIGH"
                  alarm_condition: "room_temperature > 26°C"
                  severity: "HIGH"
                  notification: ["BA主站", "手术室显示屏", "值班手机"]
                  response_action: "检查AHU、冷水机运行状态"
                  
                - alarm_id: "ALM-OR-001-TEMP-LOW"
                  alarm_condition: "room_temperature < 16°C"
                  severity: "MEDIUM"
                  notification: ["BA主站", "手术室显示屏"]
                  response_action: "检查控制设定"
                  
        reliability:
          reliability_grade: "CRITICAL"
          availability_target: 99.99
          redundancy:
            redundancy_type: "N+1"
            backup_system: "AHU-OR-002可部分支援"
            switchover_time:
              value: 0
              unit: "s"
              note: "冷水机N+1自动切换"
              
      # ─────────────────────────────────────────────────────────────────────────
      # CU-2: 氧气供应服务
      # ─────────────────────────────────────────────────────────────────────────
      
      - unit_id: "CU-OR001-MGAS_O2-SUPPLY"
        unit_name: "手术室OR-001氧气供应服务"
        unit_class: "MGAS"
        criticality_grade: "CRITICAL"
        
        topology_binding:
          space_node:
            node_id: "OR-001"
            space_topology_path: "Building/3F/SurgicalDept/OR-Zone/OR-001"
            
          system_node:
            node_id: "MGAS-O2"
            system_type: "医用氧气系统"
            system_topology_path: "MEP/MGAS/O2/MGAS-O2"
            
          device_nodes:
            - device_id: "LOX-001"
              device_type: "液氧储罐"
              device_role: "SOURCE"
              location: "室外液氧站"
            - device_id: "VAP-001"
              device_type: "汽化器"
              device_role: "SOURCE"
              location: "液氧站"
            - device_id: "REG-O2-001"
              device_type: "减压器"
              device_role: "DISTRIBUTION"
              location: "液氧站"
            - device_id: "ZV-OR-O2"
              device_type: "区域阀"
              device_role: "DISTRIBUTION"
              location: "手术部管井"
            - device_id: "OT-OR-001-1"
              device_type: "氧气终端"
              device_role: "TERMINAL"
              location: "OR-001设备塔"
            - device_id: "OT-OR-001-2"
              device_type: "氧气终端"
              device_role: "TERMINAL"
              location: "OR-001设备塔"
              
        functional_behavior_binding:
          behavior_scenario:
            scenario_id: "SCN-OR001-CARDIAC-SURGERY"
            scenario_name: "心脏外科手术"
            scenario_phase: "P2-ANESTHESIA + P4-CPB-ON"
            
          environmental_requirement:
            requirement_id: "REQ-OR001-O2-SUPPLY"
            parameters:
              - parameter_name: "oxygen_supply_pressure"
                target_value: 400
                unit: "kPa"
                tolerance: 40
                priority: "CRITICAL"
              - parameter_name: "oxygen_flow_capacity"
                target_value: 15
                unit: "L/min"
                priority: "CRITICAL"
                
        three_flow_coupling:
          
          material_flow:
            enabled: true
            carrier: "医用氧气"
            carrier_properties:
              medium_type: "GAS"
              phase: "气态"
              composition: "O2 ≥99.5%"
              
            flow_path:
              origin: "室外液氧储罐LOX-001"
              destination: "OR-001氧气终端OT-OR-001"
              route: ["液氧站", "氧气管井竖管", "3F水平管", "手术部区域管", "OR-001终端"]
              pipe_id: "PIPE-O2-OR-001"
              
            flow_parameters:
              flow_rate:
                麻醉用:
                  value: 8
                  unit: "L/min"
                体外循环用:
                  value: 10
                  unit: "L/min"
                总容量:
                  value: 15
                  unit: "L/min"
              pressure:
                supply_pressure:
                  value: 400
                  unit: "kPa"
                terminal_pressure:
                  value: 400
                  unit: "kPa"
                tolerance: "±10%"
                
            lifecycle_phases:
              supply:
                source_capacity:
                  liquid_capacity: "3000 L液氧"
                  days_supply: "≥7天"
                supply_condition:
                  pressure: "1.6 MPa (储罐)"
                  temperature: "-183°C (液态)"
                  
              consumption:
                consumption_pattern: "INTERMITTENT"
                peak_demand:
                  value: 15
                  unit: "L/min"
                  condition: "麻醉+体外循环同时"
                average_demand:
                  value: 8
                  unit: "L/min"
                  
              return_or_discharge:
                return_type: "OPEN_DISCHARGE"
                note: "氧气消耗后无回收"
                
          energy_flow:
            enabled: true
            energy_form: "PNEUMATIC"
            energy_carrier: "压缩氧气"
            
            source_specification:
              source_pressure: "400 kPa (减压后)"
              source_capacity: "满足所有终端同时使用"
              
            demand_specification:
              terminal_pressure: "400 kPa"
              pressure_drop_allowed: "5%"
              
          information_flow:
            enabled: true
            control_mode: "OPEN_LOOP"
            
            sensing_layer:
              sensors:
                - sensor_id: "PS-O2-OR-001"
                  sensor_type: "压力传感器"
                  measured_parameter: "terminal_pressure"
                  location: "区域阀后"
                  
                - sensor_id: "PS-O2-MAIN"
                  sensor_type: "压力传感器"
                  measured_parameter: "main_supply_pressure"
                  location: "液氧站出口"
                  
                - sensor_id: "LS-LOX-001"
                  sensor_type: "液位传感器"
                  measured_parameter: "liquid_level"
                  location: "液氧储罐"
                  
            control_layer:
              controller:
                controller_id: "MGAS-MC-001"
                controller_type: "医用气体监控主机"
                control_algorithm: "压力监测 + 切换控制"
                
            alarm_management:
              alarms:
                - alarm_id: "ALM-O2-LOW-PRESS"
                  alarm_condition: "terminal_pressure < 350 kPa"
                  severity: "CRITICAL"
                  notification: ["医用气体监控室", "手术室", "设备科"]
                  response_action: "检查气源、切换备用"
                  
                - alarm_id: "ALM-LOX-LOW-LEVEL"
                  alarm_condition: "liquid_level < 30%"
                  severity: "HIGH"
                  notification: ["设备科", "气体供应商"]
                  response_action: "安排补充液氧"
                  
        reliability:
          reliability_grade: "CRITICAL"
          availability_target: 99.999
          redundancy:
            redundancy_type: "N+1"
            primary: "液氧储罐"
            backup: "汇流排自动切换"
            emergency: "瓶装氧备用"
            
      # ─────────────────────────────────────────────────────────────────────────
      # CU-3: UPS供电服务
      # ─────────────────────────────────────────────────────────────────────────
      
      - unit_id: "CU-OR001-ELEC_UPS-POWER"
        unit_name: "手术室OR-001 UPS供电服务"
        unit_class: "ELEC"
        criticality_grade: "CRITICAL"
        
        topology_binding:
          space_node:
            node_id: "OR-001"
            
          system_node:
            node_id: "ELEC-UPS-OR"
            system_type: "手术室UPS系统"
            
          device_nodes:
            - device_id: "UPS-OR-001"
              device_type: "不间断电源"
              device_role: "SOURCE"
              location: "3F UPS室"
              capacity: "60 kVA"
            - device_id: "DB-OR-001-UPS"
              device_type: "UPS配电箱"
              device_role: "DISTRIBUTION"
              location: "OR-001"
            - device_id: "OUTLET-OR-001-UPS"
              device_type: "UPS插座组"
              device_role: "TERMINAL"
              location: "OR-001设备塔/壁面"
              
        functional_behavior_binding:
          behavior_scenario:
            scenario_id: "SCN-OR001-CARDIAC-SURGERY"
            scenario_phase: "P4-CPB-ON (体外循环期)"
            
          environmental_requirement:
            parameters:
              - parameter_name: "power_continuity"
                target_value: "0秒切换"
                priority: "CRITICAL"
              - parameter_name: "backup_duration"
                target_value: 60
                unit: "min"
                priority: "CRITICAL"
                
        three_flow_coupling:
          
          material_flow:
            enabled: true
            carrier: "电缆"
            carrier_properties:
              medium_type: "ELECTRICAL"
              composition: "铜导体电缆"
              
            flow_path:
              origin: "3F UPS室 UPS-OR-001"
              destination: "OR-001 UPS插座组"
              route: ["UPS室", "电气竖井", "OR-001配电箱", "UPS插座"]
              
          energy_flow:
            enabled: true
            energy_form: "ELECTRICAL"
            energy_carrier: "电能"
            
            source_specification:
              source_capacity:
                value: 60
                unit: "kVA"
              backup_capacity:
                value: 60
                unit: "min"
              source_condition:
                voltage: "220V"
                frequency: "50Hz"
                
            demand_specification:
              design_demand:
                value: 30
                unit: "kVA"
              peak_demand:
                value: 50
                unit: "kVA"
                condition: "体外循环机运行"
              critical_loads:
                - load: "体外循环机"
                  power: "20 kW"
                  priority: "生命攸关"
                - load: "麻醉机"
                  power: "0.5 kW"
                - load: "监护仪"
                  power: "0.2 kW"
                - load: "无影灯"
                  power: "0.8 kW"
                  
            energy_balance:
              normal_operation:
                source: "市电"
                ups_mode: "在线式"
                efficiency: "95%"
              power_failure:
                source: "电池"
                switchover: "0 ms"
                duration: "60 min"
                
          information_flow:
            enabled: true
            control_mode: "CLOSED_LOOP"
            
            sensing_layer:
              sensors:
                - sensor_id: "PM-UPS-OR-001"
                  sensor_type: "电力监测仪"
                  measured_parameter: "电压/电流/功率/频率"
                  location: "UPS-OR-001"
                - sensor_id: "BAT-UPS-OR-001"
                  sensor_type: "电池监测"
                  measured_parameter: "电池电压/温度/SOC"
                  
            alarm_management:
              alarms:
                - alarm_id: "ALM-UPS-BATTERY"
                  alarm_condition: "运行在电池模式"
                  severity: "CRITICAL"
                  notification: ["BA主站", "手术室", "电气值班室"]
                  response_action: "检查市电、启动发电机"
                  
                - alarm_id: "ALM-UPS-LOW-BAT"
                  alarm_condition: "电池电量 < 30%"
                  severity: "CRITICAL"
                  notification: ["手术室紧急广播"]
                  response_action: "准备手术暂停/转移"
                  
        reliability:
          reliability_grade: "CRITICAL"
          availability_target: 99.999
          redundancy:
            redundancy_type: "2N"
            primary: "UPS-OR-001"
            backup: "柴油发电机 (15s)"
            note: "体外循环机有手摇备用"
            
      # ─────────────────────────────────────────────────────────────────────────
      # 其他耦合单元简要列表
      # ─────────────────────────────────────────────────────────────────────────
      
      - unit_id: "CU-OR001-MGAS_VAC-SUCTION"
        unit_name: "手术室OR-001负压吸引服务"
        unit_class: "MGAS"
        criticality_grade: "CRITICAL"
        summary: "提供术野吸引，4终端，-40kPa"
        
      - unit_id: "CU-OR001-MGAS_AIR-SUPPLY"
        unit_name: "手术室OR-001压缩空气服务"
        unit_class: "MGAS"
        criticality_grade: "HIGH"
        summary: "提供气动设备驱动，2终端，400kPa"
        
      - unit_id: "CU-OR001-MGAS_N2O-ANESTHESIA"
        unit_name: "手术室OR-001笑气服务"
        unit_class: "MGAS"
        criticality_grade: "HIGH"
        summary: "麻醉用笑气，1终端"
        
      - unit_id: "CU-OR001-MGAS_CO2-INSUFFLATION"
        unit_name: "手术室OR-001二氧化碳服务"
        unit_class: "MGAS"
        criticality_grade: "MEDIUM"
        summary: "心外吹气用，1终端"
        
      - unit_id: "CU-OR001-ELEC_IT-POWER"
        unit_name: "手术室OR-001 IT系统供电"
        unit_class: "ELEC"
        criticality_grade: "CRITICAL"
        summary: "医用隔离供电，10kVA"
        
      - unit_id: "CU-OR001-HVAC_CLN-PRESSURE"
        unit_name: "手术室OR-001压力控制服务"
        unit_class: "HVAC"
        criticality_grade: "HIGH"
        summary: "维持+15Pa正压"
        
      - unit_id: "CU-OR001-HVAC_CLN-HUMIDITY"
        unit_name: "手术室OR-001湿度控制服务"
        unit_class: "HVAC"
        criticality_grade: "MEDIUM"
        summary: "维持50%±10%湿度"
        
      - unit_id: "CU-OR001-INT_BA-MONITOR"
        unit_name: "手术室OR-001环境监控服务"
        unit_class: "INT"
        criticality_grade: "HIGH"
        summary: "温湿度压差监控与报警"
        
      - unit_id: "CU-OR001-HVAC_PCW-ECMO"
        unit_name: "手术室OR-001体外循环冷却服务"
        unit_class: "HVAC"
        criticality_grade: "CRITICAL"
        summary: "体外循环机工艺冷却水"

  # ═══════════════════════════════════════════════════════════════════════════
  # 5.2 ICU-001 完整耦合单元集 (简化表示)
  # ═══════════════════════════════════════════════════════════════════════════
  
  ICU_001_Coupling_Units:
    
    space_id: "ICU-001"
    space_name: "综合ICU (10床)"
    space_type: "ICU-综合"
    coupling_unit_count: 8
    
    units_summary:
      - unit_id: "CU-ICU001-HVAC_AHU-COOLING"
        summary: "ICU空调冷却，维持24°C"
      - unit_id: "CU-ICU001-HVAC_AHU-PRESSURE"
        summary: "ICU压差控制，+10Pa"
      - unit_id: "CU-ICU001-MGAS_O2-SUPPLY"
        summary: "氧气供应，20终端(2/床)"
      - unit_id: "CU-ICU001-MGAS_VAC-SUCTION"
        summary: "负压吸引，20终端(2/床)"
      - unit_id: "CU-ICU001-ELEC_IT-POWER"
        summary: "IT系统供电，5kVA/4床"
      - unit_id: "CU-ICU001-ELEC_UPS-POWER"
        summary: "UPS供电，生命支持设备"
      - unit_id: "CU-ICU001-INT_BA-MONITOR"
        summary: "环境监控与报警"
      - unit_id: "CU-ICU001-ELEC_LTG-CIRCADIAN"
        summary: "昼夜节律照明"

  # ═══════════════════════════════════════════════════════════════════════════
  # 5.3 NICU 完整耦合单元集 (简化表示)
  # ═══════════════════════════════════════════════════════════════════════════
  
  NICU_Coupling_Units:
    
    space_id: "NICU-001"
    space_name: "新生儿重症监护室 (15床)"
    space_type: "ICU-NICU"
    coupling_unit_count: 10
    
    special_coupling_units:
      - unit_id: "CU-NICU-HVAC_PAC-PRECISION"
        unit_name: "NICU精密恒温服务"
        criticality_grade: "CRITICAL"
        summary: "24-26°C ±0.5°C精密控制"
        special: "多区独立温控"
        
      - unit_id: "CU-NICU-HVAC_PAC-HUMIDITY"
        unit_name: "NICU精密恒湿服务"
        criticality_grade: "HIGH"
        summary: "50-60% ±5%精密控制"
        
      - unit_id: "CU-NICU-ELEC_UPS-INCUBATOR"
        unit_name: "NICU暖箱专用UPS"
        criticality_grade: "CRITICAL"
        summary: "暖箱断电危及生命"
        
      - unit_id: "CU-NICU-MGAS_O2-BLENDER"
        unit_name: "NICU氧气-空气混合服务"
        criticality_grade: "CRITICAL"
        summary: "精确FiO2控制"

  # ═══════════════════════════════════════════════════════════════════════════
  # 5.4 急诊抢救室 完整耦合单元集 (简化表示)
  # ═══════════════════════════════════════════════════════════════════════════
  
  ER_Coupling_Units:
    
    space_id: "ER-RESUS-001"
    space_name: "急诊抢救室 (8床)"
    space_type: "急诊-抢救"
    coupling_unit_count: 7
    
    units_summary:
      - unit_id: "CU-ER-HVAC_AHU-COOLING"
        summary: "急诊空调"
      - unit_id: "CU-ER-MGAS_O2-SUPPLY"
        summary: "氧气供应，16终端"
      - unit_id: "CU-ER-MGAS_VAC-SUCTION"
        summary: "负压吸引，16终端"
      - unit_id: "CU-ER-ELEC_UPS-POWER"
        summary: "UPS供电，30kVA"
      - unit_id: "CU-ER-ELEC_EPS-LIGHTING"
        summary: "应急照明"
      - unit_id: "CU-ER-INT_NUR-CALL"
        summary: "护理呼叫系统"
      - unit_id: "CU-ER-INT_BA-MONITOR"
        summary: "环境监控"

  # ═══════════════════════════════════════════════════════════════════════════
  # 5.5 血液透析室 完整耦合单元集 (简化表示)
  # ═══════════════════════════════════════════════════════════════════════════
  
  HD_Coupling_Units:
    
    space_id: "HD-001"
    space_name: "血液透析室 (30床)"
    space_type: "治疗-血液透析"
    coupling_unit_count: 8
    
    special_coupling_units:
      - unit_id: "CU-HD-PLUMB_DW-DIALYSIS"
        unit_name: "透析纯水供应服务"
        criticality_grade: "CRITICAL"
        summary: "RO纯水系统，电导率≤10μS/cm"
        
        three_flow_coupling:
          material_flow:
            carrier: "透析用纯水"
            path: "RO系统→环路管道→透析机"
            flow_rate: "2000-4000 L/h"
            lifecycle:
              supply: "自来水→预处理→RO→储罐"
              consumption: "透析机消耗 200-300 L/h/台"
              return: "无回收"
              
          energy_flow:
            form: "压力势能"
            supply_pressure: "0.3-0.5 MPa"
            pump_power: "5 kW"
            
          information_flow:
            sensors: ["电导率", "压力", "流量"]
            alarms: ["电导率超标", "压力低"]
            
      - unit_id: "CU-HD-ELEC_UPS-DIALYSIS"
        unit_name: "透析机UPS供电"
        criticality_grade: "CRITICAL"
        summary: "80-100kVA，透析中断危及生命"
        
      - unit_id: "CU-HD-PLUMB_WW-DISCHARGE"
        unit_name: "透析废水排放"
        summary: "大量废水，4-12 m³/h"
```

---

## 补充完成度评估

```yaml
Priority_1_Assessment:
  
  assessment_date: "2025-01-15"
  
  completed_tasks:
    
    task_1:
      name: "通用耦合单元数据结构 (DML)"
      status: "✓ 完成"
      content:
        - "耦合单元Schema定义"
        - "拓扑节点绑定结构"
        - "功能行为场景绑定结构"
        - "三流动耦合完整定义"
        - "可靠性与冗余定义"
        
    task_2:
      name: "5个关键空间Agent-02融合"
      status: "✓ 完成"
      spaces:
        - "手术室 (心外)"
        - "ICU"
        - "NICU"
        - "急诊抢救室"
        - "血液透析室"
      content:
        - "行为场景导入"
        - "环境参数→系统响应映射"
        - "医疗工艺流程→系统协调时间线"
        
    task_3:
      name: "5个空间超图拓扑"
      status: "✓ 完成"
      content:
        - "多维超图定义"
        - "节点集定义 (空间/系统/设备)"
        - "超边集定义与实例"
        - "拓扑保持性验证要求"
        - "可视化模型"
        
  paradigm_improvements:
    before: "平面多对多映射"
    after: "超图拓扑 + 三流动耦合"
    improvements:
      - "✓ 显式拓扑保持性"
      - "✓ Agent-02行为场景融合"
      - "✓ 物质流-能量流-信息流完整建模"
      - "✓ 耦合单元原子化定义"
      
  next_priority:
    priority_2:
      timeline: "下周"
      tasks:
        - "5个空间所有耦合关系的三流动详细分析"
        - "5×N耦合单元完整实例库"
        - "Agent-04物理方程引用补充"
        
    priority_3:
      timeline: "第三周"
      tasks:
        - "扩展到20个关键空间"
        - "超图可视化实现"
        - "Agent-06对接评审"
```

---

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║              AGENT-05 V2.0 架构重构 - Priority 1 完成                         ║
║              超图拓扑 + 三流动耦合模型                                        ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  ✅ Task 1: 通用耦合单元数据结构 (CU-DML)                                     ║
║     ├─ 耦合单元完整Schema                                                    ║
║     ├─ 拓扑节点绑定 (Agent-01/02/03)                                         ║
║     ├─ 功能行为场景绑定 (Agent-02)                                           ║
║     ├─ 三流动耦合定义 (物质/能量/信息)                                       ║
║     └─ 可靠性与冗余定义                                                      ║
║                                                                               ║
║  ✅ Task 2: 5个关键空间Agent-02融合                                          ║
║     ├─ 手术室(心外): 行为场景+7阶段时间线                                    ║
║     ├─ ICU: 术后监护场景                                                     ║
║     ├─ NICU: 精密恒温场景                                                    ║
║     ├─ 急诊抢救室: 紧急场景                                                  ║
║     └─ 血液透析室: 透析治疗场景                                              ║
║                                                                               ║
║  ✅ Task 3: 超图拓扑模型                                                      ║
║     ├─ 多维超图形式化定义 H=(V,E,A)                                          ║
║     ├─ 三层节点集 (空间/系统/设备)                                           ║
║     ├─ 超边及三流动属性                                                      ║
║     ├─ 拓扑保持性验证                                                        ║
║     └─ 可视化模型                                                            ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  范式转变: 平面映射 → 超图拓扑 + 三流动                                      ║
║  版本: V2.0-ALPHA                                                            ║
║  状态: Priority 1 完成，准备进入 Priority 2                                  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

**Agent-05 V2.0 Priority 1 完成**

需要我继续执行 Priority 2 吗？

---