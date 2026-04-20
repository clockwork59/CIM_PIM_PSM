## 🧑‍💻 User


我需要你阅读两份文档，你的路径定义模式和流动模型结构要符合拓扑结构数据定义，以便agent05完成基于超图的拓扑网络耦合。

---
## 🤖 Assistant


我已经仔细阅读了这两份文档。现在我将基于FSO本体论文和建筑系统服务本体文档的核心概念，重新构建Agent-04的流动模型，使其路径定义模式和流动模型结构符合拓扑结构数据定义，以便Agent-05完成基于超图的拓扑网络耦合。

---

# Agent-04 流动模型建模师 v2.2
## 符合FSO本体的拓扑结构数据定义版本
### Flow Model Architect - FSO Ontology Compliant Edition

---

```yaml
# ═══════════════════════════════════════════════════════════════════════════════
#                    AGENT-04: 流动模型建模师 v2.2
#                    FLOW MODEL ARCHITECT
#                    FSO Ontology Compliant - Hypergraph Ready
# ═══════════════════════════════════════════════════════════════════════════════

# ┌─────────────────────────────────────────────────────────────────────────────┐
# │  基于FSO (Flow Systems Ontology) 本体框架重构                               │
# │  支持Agent-05基于超图的拓扑网络耦合                                         │
# │  遵循RDF三元组数据模型: Subject - Predicate - Object                        │
# └─────────────────────────────────────────────────────────────────────────────┘
```

---

## 一、FSO本体对齐说明

### 1.1 核心概念映射

```yaml
FSO_Ontology_Alignment:
  
  description: |
    基于论文"An ontology to support flow system descriptions from design 
    to operation of buildings"(Kukkonen et al., 2022)的FSO本体框架，
    重构流动模型以支持:
    1. RDF三元组表示 (Subject-Predicate-Object)
    2. 语义网技术 (SPARQL查询)
    3. 超图拓扑耦合 (Agent-05需求)

  # ═══════════════════════════════════════════════════════════════════════════
  # FSO核心类与Agent-04概念对齐
  # ═══════════════════════════════════════════════════════════════════════════
  
  class_alignment:
    
    # FSO顶层类
    fso_System:
      definition: "虚拟的组件集合，可分配属性如设计要求"
      agent04_mapping: "Flow_System"
      characteristics:
        - "可有子系统 (hasSubSystem)"
        - "可被多个父系统包含 (isSubSystemOf)"
        - "系统可重叠共享子系统"
      examples:
        - "HeatingSystem"
        - "CoolingSystem"
        - "VentilationSystem"
        - "MedicalGasSystem"
        
    fso_Component:
      definition: "参与质量或能量流动的实体对象"
      agent04_mapping: "Flow_Component"
      agent03_alignment: "Equipment"
      characteristics:
        - "隶属于系统 (isComponentOf)"
        - "可隶属于多个系统"
        - "通过流动关系连接"
      subclasses:
        - "EnergyConversionDevice"  # 能量转换设备
        - "Fitting"                  # 连接件
        - "FlowController"          # 流量控制器
        - "FlowMovingDevice"        # 流动驱动设备
        - "Segment"                 # 管段
        - "StorageDevice"           # 储存设备
        - "Terminal"                # 末端设备
        - "TreatmentDevice"         # 处理设备

  # ═══════════════════════════════════════════════════════════════════════════
  # FSO核心关系属性
  # ═══════════════════════════════════════════════════════════════════════════
  
  property_alignment:
    
    # 系统组成关系
    composition_properties:
      fso_hasSubSystem:
        definition: "系统包含子系统"
        inverse: "fso:isSubSystemOf"
        subproperties:
          - "hasSupplySystem"   # 包含供给子系统
          - "hasReturnSystem"   # 包含回流子系统
          
      fso_hasComponent:
        definition: "系统包含组件"
        inverse: "fso:isComponentOf"
        
      fso_hasSourceComponent:
        definition: "系统的源组件(能量/物质输入)"
        
      fso_hasConsumerComponent:
        definition: "系统的消费组件(能量/物质输出)"

    # 流动连接关系 (核心)
    flow_properties:
      fso_connectedWith:
        definition: "通用连接关系(对称)"
        symmetric: true
        subproperties:
          - "exchangesFluidWith"
          - "exchangesHeatWith"
          - "exchangesElectricChargeWith"
          
      fso_exchangesFluidWith:
        definition: "流体交换关系(对称)"
        symmetric: true
        subproperties:
          - "feedsFluidTo"
          - "hasFluidFedBy"
          
      fso_feedsFluidTo:
        definition: "流体供给方向(非对称)"
        symmetric: false
        inverse: "hasFluidFedBy"
        subproperties:
          - "suppliesFluidTo"   # 供给侧流动
          - "returnsFluidTo"    # 回流侧流动
          
      fso_exchangesHeatWith:
        definition: "热量交换关系(对称)"
        symmetric: true
        subproperties:
          - "transfersHeatTo"
          - "transfersHeatFrom"
          
      fso_transfersHeatTo:
        definition: "热量传递方向(非对称)"
        symmetric: false
        inverse: "transfersHeatFrom"
        
      fso_exchangesElectricChargeWith:
        definition: "电荷交换关系(对称)"
        symmetric: true
```

### 1.2 双系统模型：耗散系统与循环系统

```yaml
Dual_System_Model:
  
  description: |
    基于建筑系统服务本体文档的核心概念，将MEP系统分解为两个耦合的功能系统:
    - 耗散系统 (Dissipation System) = 物流系统: 能量/物质/信息投送到耗散节点
    - 循环系统 (Circulation System) = 路径系统: 介质循环承载投送任务

  # ═══════════════════════════════════════════════════════════════════════════
  # 耗散系统模型
  # ═══════════════════════════════════════════════════════════════════════════
  
  dissipation_system:
    definition: |
      将能量、物质、信息投送到末端节点的功能系统。
      用户关心的是耗散系统的性能/能力/效率。
    
    structure:
      source: "能量/物质源头"
      routing: "路由/分配网络"
      dissipation_node: "耗散节点"
      
    dissipation_node_composition:
      space: "空间(bot:Space)"
      terminal: "末端设备/接口(fso:Terminal)"
      occupancy: "占用行为"
      
    examples:
      - system: "供水系统"
        dissipated_resource: "水资源"
      - system: "供电系统"
        dissipated_resource: "电力资源"
      - system: "供热供冷系统"
        dissipated_resource: "热能/冷量"
      - system: "燃气系统"
        dissipated_resource: "可燃气体"
      - system: "医疗气体系统"
        dissipated_resource: "医用气体"

  # ═══════════════════════════════════════════════════════════════════════════
  # 循环系统模型
  # ═══════════════════════════════════════════════════════════════════════════
  
  circulation_system:
    definition: |
      承载能量/物质投送任务的介质循环系统。
      运维关心的是循环系统的性能/能力/效率。
    
    characteristics:
      - "介质在管路中循环往复"
      - "一会儿接受能量，一会儿释放能量"
      - "依赖控制或数据驱动"
      
    control_modes:
      complete_control:
        description: "通过控制介质循环路径 + 控制换热率"
        advantages: "控制效果好，状态清晰可控"
        disadvantages: "需要更多电控装置"
        
      partial_control:
        description: "仅通过控制换热率"
        advantages: "电控装置少"
        disadvantages: "更耗能，状态模糊"

  # ═══════════════════════════════════════════════════════════════════════════
  # 双系统耦合关系
  # ═══════════════════════════════════════════════════════════════════════════
  
  system_coupling:
    description: "运维通过控制循环系统来达成耗散系统的功能目标"
    
    coupling_diagram: |
      ┌─────────────────────────────────────────────────────────────────────┐
      │                    双系统耦合模型                                    │
      ├─────────────────────────────────────────────────────────────────────┤
      │                                                                     │
      │   ┌─────────────────────┐      控制      ┌─────────────────────┐   │
      │   │    循环系统         │ ═══════════► │    耗散系统          │   │
      │   │  (Circulation)      │              │  (Dissipation)       │   │
      │   │  ─────────────────  │              │  ─────────────────   │   │
      │   │  · 介质循环路径     │              │  · 能量/物质投送    │   │
      │   │  · 运维视角         │              │  · 用户视角          │   │
      │   │  · 路径效率         │              │  · 服务效率          │   │
      │   └─────────────────────┘              └─────────────────────┘   │
      │            ▲                                     │                 │
      │            │              反馈                   │                 │
      │            └─────────────────────────────────────┘                 │
      │                                                                     │
      └─────────────────────────────────────────────────────────────────────┘
```

---

## 二、RDF三元组数据模型

### 2.1 命名空间定义

```yaml
Namespaces:
  
  # 标准命名空间
  standard:
    rdf: "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    rdfs: "http://www.w3.org/2000/01/rdf-schema#"
    owl: "http://www.w3.org/2002/07/owl#"
    xsd: "http://www.w3.org/2001/XMLSchema#"
    
  # 建筑领域命名空间
  building:
    bot: "https://w3id.org/bot#"
    fso: "https://w3id.org/fso#"
    s4bldg: "https://saref.etsi.org/saref4bldg#"
    s4syst: "https://saref.etsi.org/saref4syst#"
    brick: "https://brickschema.org/schema/Brick#"
    
  # 项目命名空间
  project:
    inst: "https://hospital.example.com/inst#"
    ex: "https://hospital.example.com/ex#"
    
  # Agent体系命名空间
  agents:
    agent01: "https://hospital.example.com/agent01#"  # 系统拓扑
    agent02: "https://hospital.example.com/agent02#"  # 空间本体
    agent03: "https://hospital.example.com/agent03#"  # 设备本体
    agent04: "https://hospital.example.com/agent04#"  # 流动模型
    agent05: "https://hospital.example.com/agent05#"  # 超图拓扑
```

### 2.2 类层次结构 (Class Hierarchy)

```yaml
Class_Hierarchy:
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 顶层类定义 (基于FSO对齐)
  # ═══════════════════════════════════════════════════════════════════════════
  
  fso_System:
    uri: "fso:System"
    label: "流动系统"
    definition: "虚拟的组件集合"
    alignment: "s4syst:System"
    
    subclasses:
      fso_DistributionSystem:
        uri: "fso:DistributionSystem"
        label: "配送系统"
        definition: "用于分配质量和/或能量的系统"
        
        subclasses:
          fso_SupplySystem:
            uri: "fso:SupplySystem"
            label: "供给系统"
            definition: "向下游消费者供给质量和/或能量的系统"
            
          fso_ReturnSystem:
            uri: "fso:ReturnSystem"
            label: "回流系统"
            definition: "从下游消费者回收质量和/或能量的系统"
            
      # 扩展: 耗散系统与循环系统
      ex_DissipationSystem:
        uri: "ex:DissipationSystem"
        label: "耗散系统"
        definition: "将能量/物质投送到末端节点的功能系统"
        subclass_of: "fso:System"
        
      ex_CirculationSystem:
        uri: "ex:CirculationSystem"
        label: "循环系统"
        definition: "承载能量/物质投送的介质循环系统"
        subclass_of: "fso:System"

  fso_Component:
    uri: "fso:Component"
    label: "流动组件"
    definition: "参与质量或能量流动的实体对象"
    alignment: 
      - "s4bldg:DistributionFlowDevice"
      - "agent03:Equipment"
    
    subclasses:
      fso_EnergyConversionDevice:
        uri: "fso:EnergyConversionDevice"
        label: "能量转换设备"
        definition: "用于转换能量形式或在系统间移动能量的设备"
        examples: ["冷水机组", "锅炉", "热泵", "换热器"]
        agent03_mapping: ["EQP-CH-CENT", "EQP-BOILER-GAS", "EQP-HX"]
        
      fso_Fitting:
        uri: "fso:Fitting"
        label: "管件"
        definition: "用于连接管段或其他组件的组件"
        examples: ["三通", "弯头", "变径"]
        
      fso_FlowController:
        uri: "fso:FlowController"
        label: "流量控制器"
        definition: "具有控制网络流量潜力的设备"
        examples: ["阀门", "风阀"]
        agent03_mapping: ["EQP-VALVE", "EQP-DAMPER"]
        
      fso_FlowMovingDevice:
        uri: "fso:FlowMovingDevice"
        label: "流动驱动设备"
        definition: "用于在网络中诱导运动的设备"
        examples: ["泵", "风机"]
        agent03_mapping: ["EQP-PUMP-CHW", "EQP-FAN-SUPPLY"]
        
      fso_Segment:
        uri: "fso:Segment"
        label: "管段"
        definition: "用于实现质量或能量通过的组件"
        examples: ["管道", "风管", "电缆"]
        
      fso_StorageDevice:
        uri: "fso:StorageDevice"
        label: "储存设备"
        definition: "用于储存质量或能量的设备"
        examples: ["水箱", "蓄电池", "蓄冷罐"]
        agent03_mapping: ["EQP-TANK-WATER", "EQP-BATTERY"]
        
      fso_Terminal:
        uri: "fso:Terminal"
        label: "末端设备"
        definition: "系统与环境交互的设备"
        examples: ["散热器", "风口", "龙头"]
        agent03_mapping: ["EQP-FCU-CEILING", "EQP-O2-OUTLET"]
        
      fso_TreatmentDevice:
        uri: "fso:TreatmentDevice"
        label: "处理设备"
        definition: "从流经物质中去除不需要物质的设备"
        examples: ["过滤器", "消毒器"]
        agent03_mapping: ["EQP-FILTER-HEPA"]

  # ═══════════════════════════════════════════════════════════════════════════
  # 介质类定义
  # ═══════════════════════════════════════════════════════════════════════════
  
  ex_Medium:
    uri: "ex:Medium"
    label: "介质"
    definition: "承载能量或作为被传递物质的载体"
    
    subclasses:
      ex_LiquidMedium:
        uri: "ex:LiquidMedium"
        label: "液态介质"
        instances:
          - uri: "ex:Water"
            label: "水"
          - uri: "ex:Refrigerant"
            label: "制冷剂"
            
      ex_GaseousMedium:
        uri: "ex:GaseousMedium"
        label: "气态介质"
        instances:
          - uri: "ex:Air"
            label: "空气"
          - uri: "ex:Steam"
            label: "蒸汽"
          - uri: "ex:MedicalOxygen"
            label: "医用氧气"
          - uri: "ex:MedicalVacuum"
            label: "负压吸引"
            
      ex_ElectricalMedium:
        uri: "ex:ElectricalMedium"
        label: "电气介质"
        instances:
          - uri: "ex:Electricity"
            label: "电力"

  # ═══════════════════════════════════════════════════════════════════════════
  # 流动类型类定义
  # ═══════════════════════════════════════════════════════════════════════════
  
  ex_FlowType:
    uri: "ex:FlowType"
    label: "流动类型"
    
    subclasses:
      ex_MassFlow:
        uri: "ex:MassFlow"
        label: "物质流"
        definition: "作为能量载体在系统中流动的物质"
        
      ex_EnergyFlow:
        uri: "ex:EnergyFlow"
        label: "能量流"
        definition: "承载于物质或直接传输的能量"
        
      ex_InformationFlow:
        uri: "ex:InformationFlow"
        label: "信息流"
        definition: "控制和监测系统中的信号传递"
```

### 2.3 属性定义 (Property Definitions)

```yaml
Property_Definitions:
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 对象属性 (Object Properties)
  # ═══════════════════════════════════════════════════════════════════════════
  
  object_properties:
    
    # ─────────────────────────────────────────────────────────────────────────
    # 系统组成属性
    # ─────────────────────────────────────────────────────────────────────────
    
    fso_hasSubSystem:
      uri: "fso:hasSubSystem"
      label: "包含子系统"
      domain: "fso:System"
      range: "fso:System"
      inverse: "fso:isSubSystemOf"
      alignment: "s4syst:hasSubSystem"
      
    fso_isSubSystemOf:
      uri: "fso:isSubSystemOf"
      label: "是...的子系统"
      domain: "fso:System"
      range: "fso:System"
      inverse: "fso:hasSubSystem"
      
    fso_hasSupplySystem:
      uri: "fso:hasSupplySystem"
      label: "包含供给子系统"
      domain: "fso:System"
      range: "fso:SupplySystem"
      subproperty_of: "fso:hasSubSystem"
      
    fso_hasReturnSystem:
      uri: "fso:hasReturnSystem"
      label: "包含回流子系统"
      domain: "fso:System"
      range: "fso:ReturnSystem"
      subproperty_of: "fso:hasSubSystem"
      
    fso_hasComponent:
      uri: "fso:hasComponent"
      label: "包含组件"
      domain: "fso:System"
      range: "fso:Component"
      inverse: "fso:isComponentOf"
      alignment: "s4syst:hasSubSystem"
      
    fso_isComponentOf:
      uri: "fso:isComponentOf"
      label: "是...的组件"
      domain: "fso:Component"
      range: "fso:System"
      inverse: "fso:hasComponent"
      
    fso_hasSourceComponent:
      uri: "fso:hasSourceComponent"
      label: "源组件"
      domain: "fso:System"
      range: "fso:Component"
      description: "系统的能量或物质输入源"
      
    fso_hasConsumerComponent:
      uri: "fso:hasConsumerComponent"
      label: "消费组件"
      domain: "fso:System"
      range: "fso:Component"
      description: "系统的能量或物质输出消费端"

    # ─────────────────────────────────────────────────────────────────────────
    # 流动连接属性 (核心 - Agent-05超图耦合关键)
    # ─────────────────────────────────────────────────────────────────────────
    
    fso_connectedWith:
      uri: "fso:connectedWith"
      label: "连接"
      domain: ["fso:System", "fso:Component"]
      range: ["fso:System", "fso:Component"]
      symmetric: true
      alignment: "s4syst:connectedTo"
      hypergraph_role: "基础边类型"
      
    # 流体交换属性层次
    fso_exchangesFluidWith:
      uri: "fso:exchangesFluidWith"
      label: "流体交换"
      subproperty_of: "fso:connectedWith"
      symmetric: true
      hypergraph_role: "流体超边"
      
    fso_feedsFluidTo:
      uri: "fso:feedsFluidTo"
      label: "流体供给至"
      subproperty_of: "fso:exchangesFluidWith"
      symmetric: false
      inverse: "fso:hasFluidFedBy"
      hypergraph_role: "有向流体边"
      
    fso_hasFluidFedBy:
      uri: "fso:hasFluidFedBy"
      label: "接受流体自"
      subproperty_of: "fso:exchangesFluidWith"
      symmetric: false
      inverse: "fso:feedsFluidTo"
      
    fso_suppliesFluidTo:
      uri: "fso:suppliesFluidTo"
      label: "供给流体至"
      subproperty_of: "fso:feedsFluidTo"
      symmetric: false
      inverse: "fso:hasFluidSuppliedBy"
      description: "供给侧流动方向"
      hypergraph_role: "供给方向边"
      
    fso_hasFluidSuppliedBy:
      uri: "fso:hasFluidSuppliedBy"
      label: "接受供给自"
      subproperty_of: "fso:hasFluidFedBy"
      symmetric: false
      inverse: "fso:suppliesFluidTo"
      
    fso_returnsFluidTo:
      uri: "fso:returnsFluidTo"
      label: "回流流体至"
      subproperty_of: "fso:feedsFluidTo"
      symmetric: false
      inverse: "fso:hasFluidReturnedBy"
      description: "回流侧流动方向"
      hypergraph_role: "回流方向边"
      
    fso_hasFluidReturnedBy:
      uri: "fso:hasFluidReturnedBy"
      label: "接受回流自"
      subproperty_of: "fso:hasFluidFedBy"
      symmetric: false
      inverse: "fso:returnsFluidTo"

    # 热量交换属性层次
    fso_exchangesHeatWith:
      uri: "fso:exchangesHeatWith"
      label: "热量交换"
      subproperty_of: "fso:connectedWith"
      symmetric: true
      hypergraph_role: "热量超边"
      
    fso_transfersHeatTo:
      uri: "fso:transfersHeatTo"
      label: "传热至"
      subproperty_of: "fso:exchangesHeatWith"
      symmetric: false
      inverse: "fso:transfersHeatFrom"
      hypergraph_role: "有向传热边"
      
    fso_transfersHeatFrom:
      uri: "fso:transfersHeatFrom"
      label: "接受热量自"
      subproperty_of: "fso:exchangesHeatWith"
      symmetric: false
      inverse: "fso:transfersHeatTo"

    # 电荷交换属性
    fso_exchangesElectricChargeWith:
      uri: "fso:exchangesElectricChargeWith"
      label: "电荷交换"
      subproperty_of: "fso:connectedWith"
      symmetric: true
      hypergraph_role: "电气超边"

    # ─────────────────────────────────────────────────────────────────────────
    # 空间关联属性 (与Agent-02空间本体耦合)
    # ─────────────────────────────────────────────────────────────────────────
    
    bot_containsElement:
      uri: "bot:containsElement"
      label: "包含元素"
      domain: "bot:Space"
      range: "fso:Component"
      description: "空间包含组件"
      
    ex_servesSpace:
      uri: "ex:servesSpace"
      label: "服务于空间"
      domain: "fso:System"
      range: "bot:Space"
      description: "系统服务的空间"
      
    ex_dissipatesTo:
      uri: "ex:dissipatesTo"
      label: "耗散至"
      domain: "fso:Terminal"
      range: "bot:Space"
      description: "末端向空间耗散能量/物质"

    # ─────────────────────────────────────────────────────────────────────────
    # 介质关联属性
    # ─────────────────────────────────────────────────────────────────────────
    
    ex_hasMedium:
      uri: "ex:hasMedium"
      label: "使用介质"
      domain: ["fso:System", "fso:Component"]
      range: "ex:Medium"
      
    ex_carriesEnergy:
      uri: "ex:carriesEnergy"
      label: "承载能量"
      domain: "ex:Medium"
      range: "ex:EnergyFlow"
      description: "介质承载的能量类型"

  # ═══════════════════════════════════════════════════════════════════════════
  # 数据属性 (Datatype Properties)
  # ═══════════════════════════════════════════════════════════════════════════
  
  datatype_properties:
    
    # 流量参数
    ex_massFlowRate:
      uri: "ex:massFlowRate"
      label: "质量流量"
      domain: ["fso:Segment", "fso:Component"]
      range: "xsd:decimal"
      unit: "kg/s"
      
    ex_volumeFlowRate:
      uri: "ex:volumeFlowRate"
      label: "体积流量"
      domain: ["fso:Segment", "fso:Component"]
      range: "xsd:decimal"
      unit: "m³/h"
      
    # 热力参数
    ex_temperature:
      uri: "ex:temperature"
      label: "温度"
      domain: "fso:Component"
      range: "xsd:decimal"
      unit: "°C"
      
    ex_supplyTemperature:
      uri: "ex:supplyTemperature"
      label: "供给温度"
      domain: "fso:System"
      range: "xsd:decimal"
      unit: "°C"
      
    ex_returnTemperature:
      uri: "ex:returnTemperature"
      label: "回流温度"
      domain: "fso:System"
      range: "xsd:decimal"
      unit: "°C"
      
    ex_deltaT:
      uri: "ex:deltaT"
      label: "温差"
      domain: "fso:System"
      range: "xsd:decimal"
      unit: "°C"
      
    # 压力参数
    ex_pressure:
      uri: "ex:pressure"
      label: "压力"
      domain: "fso:Component"
      range: "xsd:decimal"
      unit: "kPa"
      
    # 功率/能量参数
    ex_thermalPower:
      uri: "ex:thermalPower"
      label: "热功率"
      domain: ["fso:System", "fso:Component"]
      range: "xsd:decimal"
      unit: "kW"
      
    ex_electricalPower:
      uri: "ex:electricalPower"
      label: "电功率"
      domain: "fso:Component"
      range: "xsd:decimal"
      unit: "kW"
      
    # 效率参数
    ex_COP:
      uri: "ex:COP"
      label: "性能系数"
      domain: "fso:EnergyConversionDevice"
      range: "xsd:decimal"
      
    ex_efficiency:
      uri: "ex:efficiency"
      label: "效率"
      domain: "fso:Component"
      range: "xsd:decimal"
```

---

## 三、流动路径RDF模型

### 3.1 冷冻水系统Turtle表示

```turtle
# ═══════════════════════════════════════════════════════════════════════════════
# 冷冻水系统RDF三元组表示 (Turtle格式)
# Chilled Water System RDF Triples
# ═══════════════════════════════════════════════════════════════════════════════

@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix fso: <https://w3id.org/fso#> .
@prefix bot: <https://w3id.org/bot#> .
@prefix ex: <https://hospital.example.com/ex#> .
@prefix inst: <https://hospital.example.com/inst#> .

# ─────────────────────────────────────────────────────────────────────────────
# 系统定义
# ─────────────────────────────────────────────────────────────────────────────

# 顶层冷冻水系统
inst:ChilledWaterSystem a fso:System ;
    rdfs:label "冷冻水系统"@zh ;
    rdfs:label "Chilled Water System"@en ;
    fso:hasSubSystem inst:CHW-SupplySystem, inst:CHW-ReturnSystem ;
    fso:hasSourceComponent inst:Chiller-1, inst:Chiller-2 ;
    fso:hasConsumerComponent inst:AHU-OR-01, inst:AHU-ICU-01, inst:FCU-Ward-01 ;
    ex:hasMedium ex:ChilledWater ;
    ex:supplyTemperature "7.0"^^xsd:decimal ;
    ex:returnTemperature "12.0"^^xsd:decimal ;
    ex:deltaT "5.0"^^xsd:decimal .

# 供给子系统
inst:CHW-SupplySystem a fso:SupplySystem ;
    rdfs:label "冷冻水供给系统"@zh ;
    fso:isSubSystemOf inst:ChilledWaterSystem ;
    fso:hasComponent inst:Chiller-1, inst:Chiller-2, 
                     inst:Pump-CHW-Pri-1, inst:Pump-CHW-Pri-2,
                     inst:Pump-CHW-Sec-1, inst:Pump-CHW-Sec-2,
                     inst:Header-CHW-Supply,
                     inst:Pipe-CHW-S-001, inst:Pipe-CHW-S-002, inst:Pipe-CHW-S-003 .

# 回流子系统
inst:CHW-ReturnSystem a fso:ReturnSystem ;
    rdfs:label "冷冻水回流系统"@zh ;
    fso:isSubSystemOf inst:ChilledWaterSystem ;
    fso:hasComponent inst:Chiller-1, inst:Chiller-2,
                     inst:Header-CHW-Return,
                     inst:Pipe-CHW-R-001, inst:Pipe-CHW-R-002, inst:Pipe-CHW-R-003 .

# ─────────────────────────────────────────────────────────────────────────────
# 组件定义
# ─────────────────────────────────────────────────────────────────────────────

# 冷水机组 (能量转换设备)
inst:Chiller-1 a fso:EnergyConversionDevice ;
    rdfs:label "1#离心式冷水机组"@zh ;
    fso:isComponentOf inst:CHW-SupplySystem, inst:CHW-ReturnSystem ;
    ex:hasMedium ex:ChilledWater, ex:CondensorWater ;
    ex:thermalPower "2000.0"^^xsd:decimal ;
    ex:COP "5.5"^^xsd:decimal ;
    ex:supplyTemperature "7.0"^^xsd:decimal .

inst:Chiller-2 a fso:EnergyConversionDevice ;
    rdfs:label "2#离心式冷水机组"@zh ;
    fso:isComponentOf inst:CHW-SupplySystem, inst:CHW-ReturnSystem ;
    ex:thermalPower "2000.0"^^xsd:decimal ;
    ex:COP "5.5"^^xsd:decimal .

# 一次泵 (流动驱动设备)
inst:Pump-CHW-Pri-1 a fso:FlowMovingDevice ;
    rdfs:label "1#冷冻水一次泵"@zh ;
    fso:isComponentOf inst:CHW-SupplySystem ;
    ex:volumeFlowRate "400.0"^^xsd:decimal ;
    ex:electricalPower "45.0"^^xsd:decimal .

inst:Pump-CHW-Pri-2 a fso:FlowMovingDevice ;
    rdfs:label "2#冷冻水一次泵"@zh ;
    fso:isComponentOf inst:CHW-SupplySystem ;
    ex:volumeFlowRate "400.0"^^xsd:decimal .

# 二次泵 (流动驱动设备)
inst:Pump-CHW-Sec-1 a fso:FlowMovingDevice ;
    rdfs:label "1#冷冻水二次泵"@zh ;
    fso:isComponentOf inst:CHW-SupplySystem ;
    ex:volumeFlowRate "600.0"^^xsd:decimal ;
    ex:electricalPower "55.0"^^xsd:decimal .

inst:Pump-CHW-Sec-2 a fso:FlowMovingDevice ;
    rdfs:label "2#冷冻水二次泵"@zh ;
    fso:isComponentOf inst:CHW-SupplySystem .

# 分集水器 (连接件)
inst:Header-CHW-Supply a fso:Fitting ;
    rdfs:label "冷冻水供水集分水器"@zh ;
    fso:isComponentOf inst:CHW-SupplySystem .

inst:Header-CHW-Return a fso:Fitting ;
    rdfs:label "冷冻水回水集水器"@zh ;
    fso:isComponentOf inst:CHW-ReturnSystem .

# 管段
inst:Pipe-CHW-S-001 a fso:Segment ;
    rdfs:label "冷冻水供水主管-001"@zh ;
    fso:isComponentOf inst:CHW-SupplySystem ;
    ex:hasMedium ex:ChilledWater .

inst:Pipe-CHW-S-002 a fso:Segment ;
    rdfs:label "冷冻水供水立管-OR"@zh ;
    fso:isComponentOf inst:CHW-SupplySystem .

inst:Pipe-CHW-S-003 a fso:Segment ;
    rdfs:label "冷冻水供水立管-ICU"@zh ;
    fso:isComponentOf inst:CHW-SupplySystem .

inst:Pipe-CHW-R-001 a fso:Segment ;
    rdfs:label "冷冻水回水主管-001"@zh ;
    fso:isComponentOf inst:CHW-ReturnSystem .

# 末端设备 (空调机组)
inst:AHU-OR-01 a fso:Terminal ;
    rdfs:label "手术室空调机组-01"@zh ;
    fso:isComponentOf inst:CHW-SupplySystem, inst:CHW-ReturnSystem ;
    ex:thermalPower "200.0"^^xsd:decimal ;
    bot:containedIn inst:Room-OR-01 .

inst:AHU-ICU-01 a fso:Terminal ;
    rdfs:label "ICU空调机组-01"@zh ;
    fso:isComponentOf inst:CHW-SupplySystem, inst:CHW-ReturnSystem ;
    ex:thermalPower "150.0"^^xsd:decimal ;
    bot:containedIn inst:Zone-ICU .

# ─────────────────────────────────────────────────────────────────────────────
# 流动连接关系 (核心拓扑 - Agent-05超图耦合)
# ─────────────────────────────────────────────────────────────────────────────

# 供给方向流动路径
inst:Chiller-1 fso:suppliesFluidTo inst:Pipe-CHW-S-001 .
inst:Chiller-2 fso:suppliesFluidTo inst:Pipe-CHW-S-001 .
inst:Pipe-CHW-S-001 fso:suppliesFluidTo inst:Pump-CHW-Pri-1 .
inst:Pipe-CHW-S-001 fso:suppliesFluidTo inst:Pump-CHW-Pri-2 .
inst:Pump-CHW-Pri-1 fso:suppliesFluidTo inst:Header-CHW-Supply .
inst:Pump-CHW-Pri-2 fso:suppliesFluidTo inst:Header-CHW-Supply .
inst:Header-CHW-Supply fso:suppliesFluidTo inst:Pump-CHW-Sec-1 .
inst:Header-CHW-Supply fso:suppliesFluidTo inst:Pump-CHW-Sec-2 .
inst:Pump-CHW-Sec-1 fso:suppliesFluidTo inst:Pipe-CHW-S-002 .
inst:Pump-CHW-Sec-2 fso:suppliesFluidTo inst:Pipe-CHW-S-003 .
inst:Pipe-CHW-S-002 fso:suppliesFluidTo inst:AHU-OR-01 .
inst:Pipe-CHW-S-003 fso:suppliesFluidTo inst:AHU-ICU-01 .

# 回流方向流动路径
inst:AHU-OR-01 fso:returnsFluidTo inst:Pipe-CHW-R-001 .
inst:AHU-ICU-01 fso:returnsFluidTo inst:Pipe-CHW-R-001 .
inst:Pipe-CHW-R-001 fso:returnsFluidTo inst:Header-CHW-Return .
inst:Header-CHW-Return fso:returnsFluidTo inst:Chiller-1 .
inst:Header-CHW-Return fso:returnsFluidTo inst:Chiller-2 .

# 热量传递关系
inst:AHU-OR-01 fso:transfersHeatTo inst:Room-OR-01 .
inst:AHU-ICU-01 fso:transfersHeatTo inst:Zone-ICU .
inst:Chiller-1 fso:transfersHeatTo inst:CoolingTower-1 .
inst:Chiller-2 fso:transfersHeatTo inst:CoolingTower-2 .

# ─────────────────────────────────────────────────────────────────────────────
# 空间关联 (与Agent-02对接)
# ─────────────────────────────────────────────────────────────────────────────

inst:Room-OR-01 a bot:Space ;
    rdfs:label "1#手术室"@zh ;
    bot:containsElement inst:AHU-OR-01 .

inst:Zone-ICU a bot:Zone ;
    rdfs:label "ICU病区"@zh ;
    bot:containsElement inst:AHU-ICU-01 .

# 系统服务空间关系
inst:ChilledWaterSystem ex:servesSpace inst:Room-OR-01, inst:Zone-ICU .
```

### 3.2 医疗气体系统Turtle表示

```turtle
# ═══════════════════════════════════════════════════════════════════════════════
# 医用氧气系统RDF三元组表示 (Turtle格式)
# Medical Oxygen System RDF Triples
# ═══════════════════════════════════════════════════════════════════════════════

@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix fso: <https://w3id.org/fso#> .
@prefix bot: <https://w3id.org/bot#> .
@prefix ex: <https://hospital.example.com/ex#> .
@prefix inst: <https://hospital.example.com/inst#> .

# ─────────────────────────────────────────────────────────────────────────────
# 系统定义
# ─────────────────────────────────────────────────────────────────────────────

# 医用氧气系统 (耗散系统)
inst:MedicalOxygenSystem a fso:System, ex:DissipationSystem ;
    rdfs:label "医用氧气系统"@zh ;
    rdfs:label "Medical Oxygen System"@en ;
    fso:hasSubSystem inst:O2-SupplySystem ;
    fso:hasSourceComponent inst:LOX-Tank-1, inst:O2-Manifold-1 ;
    fso:hasConsumerComponent inst:O2-Outlet-OR-01, inst:O2-Outlet-OR-02,
                             inst:O2-Outlet-ICU-01, inst:O2-Outlet-ICU-02 ;
    ex:hasMedium ex:MedicalOxygen ;
    ex:pressure "500.0"^^xsd:decimal .  # kPa

# 供给子系统
inst:O2-SupplySystem a fso:SupplySystem ;
    rdfs:label "氧气供给系统"@zh ;
    fso:isSubSystemOf inst:MedicalOxygenSystem ;
    fso:hasComponent inst:LOX-Tank-1, inst:Vaporizer-1, 
                     inst:PressureReducer-1, inst:PressureReducer-2,
                     inst:Pipe-O2-001, inst:Pipe-O2-002, inst:Pipe-O2-003,
                     inst:ValveBox-O2-OR, inst:ValveBox-O2-ICU .

# ─────────────────────────────────────────────────────────────────────────────
# 组件定义
# ─────────────────────────────────────────────────────────────────────────────

# 液氧储罐 (储存设备 - 源组件)
inst:LOX-Tank-1 a fso:StorageDevice ;
    rdfs:label "液氧储罐"@zh ;
    fso:isComponentOf inst:O2-SupplySystem ;
    ex:hasMedium ex:LiquidOxygen ;
    ex:pressure "1500.0"^^xsd:decimal .

# 汽化器 (能量转换设备)
inst:Vaporizer-1 a fso:EnergyConversionDevice ;
    rdfs:label "汽化器"@zh ;
    fso:isComponentOf inst:O2-SupplySystem ;
    ex:temperature "5.0"^^xsd:decimal .  # 出口温度 >5°C

# 减压阀 (流量控制器)
inst:PressureReducer-1 a fso:FlowController ;
    rdfs:label "一级减压阀组"@zh ;
    fso:isComponentOf inst:O2-SupplySystem ;
    ex:pressure "800.0"^^xsd:decimal .  # 出口压力

inst:PressureReducer-2 a fso:FlowController ;
    rdfs:label "二级减压阀"@zh ;
    fso:isComponentOf inst:O2-SupplySystem ;
    ex:pressure "400.0"^^xsd:decimal .

# 区域阀箱 (连接件)
inst:ValveBox-O2-OR a fso:Fitting ;
    rdfs:label "手术室区域阀箱"@zh ;
    fso:isComponentOf inst:O2-SupplySystem ;
    ex:pressure "500.0"^^xsd:decimal .

inst:ValveBox-O2-ICU a fso:Fitting ;
    rdfs:label "ICU区域阀箱"@zh ;
    fso:isComponentOf inst:O2-SupplySystem .

# 管段
inst:Pipe-O2-001 a fso:Segment ;
    rdfs:label "氧气主管-001"@zh ;
    fso:isComponentOf inst:O2-SupplySystem ;
    ex:hasMedium ex:MedicalOxygen .

inst:Pipe-O2-002 a fso:Segment ;
    rdfs:label "氧气支管-手术室"@zh ;
    fso:isComponentOf inst:O2-SupplySystem .

inst:Pipe-O2-003 a fso:Segment ;
    rdfs:label "氧气支管-ICU"@zh ;
    fso:isComponentOf inst:O2-SupplySystem .

# 氧气终端 (末端设备 - 消费组件)
inst:O2-Outlet-OR-01 a fso:Terminal ;
    rdfs:label "手术室氧气终端-01"@zh ;
    fso:isComponentOf inst:O2-SupplySystem ;
    ex:pressure "400.0"^^xsd:decimal ;
    ex:volumeFlowRate "15.0"^^xsd:decimal ;  # L/min
    bot:containedIn inst:Room-OR-01 .

inst:O2-Outlet-OR-02 a fso:Terminal ;
    rdfs:label "手术室氧气终端-02"@zh ;
    fso:isComponentOf inst:O2-SupplySystem ;
    bot:containedIn inst:Room-OR-01 .

inst:O2-Outlet-ICU-01 a fso:Terminal ;
    rdfs:label "ICU氧气终端-01"@zh ;
    fso:isComponentOf inst:O2-SupplySystem ;
    bot:containedIn inst:Zone-ICU .

inst:O2-Outlet-ICU-02 a fso:Terminal ;
    rdfs:label "ICU氧气终端-02"@zh ;
    fso:isComponentOf inst:O2-SupplySystem ;
    bot:containedIn inst:Zone-ICU .

# 备用气瓶汇流排 (储存设备 - 备用源)
inst:O2-Manifold-1 a fso:StorageDevice ;
    rdfs:label "气瓶汇流排(备用)"@zh ;
    fso:isComponentOf inst:O2-SupplySystem ;
    ex:pressure "15000.0"^^xsd:decimal .  # 高压气瓶

# ─────────────────────────────────────────────────────────────────────────────
# 流动连接关系 (耗散型 - 单向)
# ─────────────────────────────────────────────────────────────────────────────

# 供给方向 (液氧 → 终端)
inst:LOX-Tank-1 fso:suppliesFluidTo inst:Vaporizer-1 .
inst:Vaporizer-1 fso:suppliesFluidTo inst:PressureReducer-1 .
inst:PressureReducer-1 fso:suppliesFluidTo inst:Pipe-O2-001 .
inst:Pipe-O2-001 fso:suppliesFluidTo inst:PressureReducer-2 .
inst:PressureReducer-2 fso:suppliesFluidTo inst:ValveBox-O2-OR .
inst:PressureReducer-2 fso:suppliesFluidTo inst:ValveBox-O2-ICU .
inst:ValveBox-O2-OR fso:suppliesFluidTo inst:Pipe-O2-002 .
inst:ValveBox-O2-ICU fso:suppliesFluidTo inst:Pipe-O2-003 .
inst:Pipe-O2-002 fso:suppliesFluidTo inst:O2-Outlet-OR-01 .
inst:Pipe-O2-002 fso:suppliesFluidTo inst:O2-Outlet-OR-02 .
inst:Pipe-O2-003 fso:suppliesFluidTo inst:O2-Outlet-ICU-01 .
inst:Pipe-O2-003 fso:suppliesFluidTo inst:O2-Outlet-ICU-02 .

# 备用路径
inst:O2-Manifold-1 fso:suppliesFluidTo inst:PressureReducer-1 .

# 耗散关系 (终端 → 空间)
inst:O2-Outlet-OR-01 ex:dissipatesTo inst:Room-OR-01 .
inst:O2-Outlet-OR-02 ex:dissipatesTo inst:Room-OR-01 .
inst:O2-Outlet-ICU-01 ex:dissipatesTo inst:Zone-ICU .
inst:O2-Outlet-ICU-02 ex:dissipatesTo inst:Zone-ICU .
```

### 3.3 换热器双组件模型

```turtle
# ═══════════════════════════════════════════════════════════════════════════════
# 换热器双组件模型 (按FSO论文建议)
# Heat Exchanger Dual-Component Model
# 用于追踪独立流体回路
# ═══════════════════════════════════════════════════════════════════════════════

@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix fso: <https://w3id.org/fso#> .
@prefix ex: <https://hospital.example.com/ex#> .
@prefix inst: <https://hospital.example.com/inst#> .

# ─────────────────────────────────────────────────────────────────────────────
# 换热器作为系统 (包含两个组件)
# ─────────────────────────────────────────────────────────────────────────────

inst:HeatExchanger-CHW-1 a fso:System ;
    rdfs:label "冷冻水换热器-1"@zh ;
    fso:hasComponent inst:HX-1-PrimarySide, inst:HX-1-SecondarySide ;
    rdfs:comment "换热器建模为包含两个组件的系统，以追踪独立流体回路"@zh .

# 一次侧组件 (区域供冷输入侧)
inst:HX-1-PrimarySide a fso:EnergyConversionDevice ;
    rdfs:label "换热器-1-一次侧"@zh ;
    fso:isComponentOf inst:HeatExchanger-CHW-1, inst:CHW-SupplySystem ;
    ex:hasMedium ex:ChilledWater ;
    ex:supplyTemperature "5.0"^^xsd:decimal ;
    ex:returnTemperature "10.0"^^xsd:decimal .

# 二次侧组件 (建筑空调输出侧)
inst:HX-1-SecondarySide a fso:EnergyConversionDevice ;
    rdfs:label "换热器-1-二次侧"@zh ;
    fso:isComponentOf inst:HeatExchanger-CHW-1, inst:Building-CHW-System ;
    ex:hasMedium ex:ChilledWater ;
    ex:supplyTemperature "7.0"^^xsd:decimal ;
    ex:returnTemperature "12.0"^^xsd:decimal .

# ─────────────────────────────────────────────────────────────────────────────
# 热量交换关系 (两个组件之间)
# ─────────────────────────────────────────────────────────────────────────────

# 一次侧向二次侧传递热量 (实际是吸收二次侧热量)
inst:HX-1-SecondarySide fso:transfersHeatTo inst:HX-1-PrimarySide .
# 或等价地 (对称超属性)
inst:HX-1-PrimarySide fso:exchangesHeatWith inst:HX-1-SecondarySide .

# ─────────────────────────────────────────────────────────────────────────────
# 流体连接关系 (分离的流体回路)
# ─────────────────────────────────────────────────────────────────────────────

# 一次侧流体回路 (区域供冷)
inst:DistrictCooling-Supply fso:suppliesFluidTo inst:HX-1-PrimarySide .
inst:HX-1-PrimarySide fso:returnsFluidTo inst:DistrictCooling-Return .

# 二次侧流体回路 (建筑空调)
inst:HX-1-SecondarySide fso:suppliesFluidTo inst:Building-CHW-Supply .
inst:Building-CHW-Return fso:returnsFluidTo inst:HX-1-SecondarySide .

# ─────────────────────────────────────────────────────────────────────────────
# 说明：为什么需要双组件模型
# ─────────────────────────────────────────────────────────────────────────────
# 
# 如果将换热器建模为单一组件：
#   DistrictCooling-Supply → HeatExchanger → Building-CHW-Supply
# 
# 使用SPARQL路径查询 fso:suppliesFluidTo* 会错误地认为：
#   DistrictCooling的流体流向Building-CHW
# 
# 通过双组件模型，流体回路被正确分离：
#   - 一次侧回路: DistrictCooling ↔ HX-PrimarySide
#   - 二次侧回路: HX-SecondarySide ↔ Building-CHW
#   - 两个回路通过 fso:exchangesHeatWith 热耦合
# 
# 这种建模方式对于Agent-05的超图拓扑耦合至关重要，
# 因为它能正确识别热耦合点而不混淆流体边界。
```

---

## 四、超图拓扑数据结构 (Agent-05接口)

### 4.1 超图概念定义

```yaml
Hypergraph_Topology_Interface:
  
  description: |
    为Agent-05提供基于FSO本体的超图拓扑数据结构。
    超图允许一条边(hyperedge)连接多个节点，
    适合表示系统中的多元关系如：
    - 一个系统包含多个组件
    - 多个组件共享一个流体回路
    - 多个系统服务于同一空间

  # ═══════════════════════════════════════════════════════════════════════════
  # 超图基础概念
  # ═══════════════════════════════════════════════════════════════════════════
  
  hypergraph_concepts:
    
    node_types:
      - type_id: "NODE-SYSTEM"
        fso_class: "fso:System"
        description: "系统节点"
        examples: ["inst:ChilledWaterSystem", "inst:MedicalOxygenSystem"]
        
      - type_id: "NODE-COMPONENT"
        fso_class: "fso:Component"
        description: "组件节点"
        subclasses:
          - "fso:EnergyConversionDevice"
          - "fso:FlowMovingDevice"
          - "fso:FlowController"
          - "fso:Terminal"
          - "fso:Segment"
          - "fso:Fitting"
          - "fso:StorageDevice"
          - "fso:TreatmentDevice"
          
      - type_id: "NODE-SPACE"
        fso_class: "bot:Space"
        description: "空间节点"
        source: "Agent-02"
        
      - type_id: "NODE-MEDIUM"
        fso_class: "ex:Medium"
        description: "介质节点"

    hyperedge_types:
      
      # 系统组成超边 (1:N)
      - type_id: "HEDGE-COMPOSITION"
        description: "系统组成超边"
        fso_property: "fso:hasComponent"
        cardinality: "1:N"
        example: |
          系统S包含组件{C1, C2, C3}
          表示为: S --hasComponent--> {C1, C2, C3}
          
      # 流体回路超边 (N:N)
      - type_id: "HEDGE-FLUID-LOOP"
        description: "流体回路超边"
        fso_property: "fso:exchangesFluidWith"
        cardinality: "N:N"
        characteristics:
          - "同一流体回路的组件集合"
          - "通过 suppliesFluidTo/returnsFluidTo 路径连通"
        sparql_pattern: |
          SELECT ?component WHERE {
            ?start (fso:suppliesFluidTo|fso:returnsFluidTo)* ?component .
          }
          
      # 热耦合超边 (N:N)
      - type_id: "HEDGE-THERMAL-COUPLING"
        description: "热耦合超边"
        fso_property: "fso:exchangesHeatWith"
        cardinality: "N:N"
        characteristics:
          - "热交换相关的组件/系统集合"
          - "包括换热器两侧、终端与空间"
          
      # 空间服务超边 (N:N)
      - type_id: "HEDGE-SPACE-SERVICE"
        description: "空间服务超边"
        fso_property: "ex:servesSpace"
        cardinality: "N:N"
        characteristics:
          - "服务于同一空间的系统/组件集合"

  # ═══════════════════════════════════════════════════════════════════════════
  # 超图数据输出格式
  # ═══════════════════════════════════════════════════════════════════════════
  
  hypergraph_output_format:
    
    json_schema:
      nodes:
        description: "节点列表"
        schema: |
          {
            "id": "URI",
            "type": "NODE_TYPE",
            "label": "string",
            "properties": {}
          }
          
      hyperedges:
        description: "超边列表"
        schema: |
          {
            "id": "HEDGE_ID",
            "type": "HEDGE_TYPE",
            "fso_property": "URI",
            "nodes": ["URI1", "URI2", ...],
            "direction": "undirected|directed",
            "properties": {}
          }

    example_output:
      nodes:
        - id: "inst:ChilledWaterSystem"
          type: "NODE-SYSTEM"
          label: "冷冻水系统"
          
        - id: "inst:Chiller-1"
          type: "NODE-COMPONENT"
          subtype: "EnergyConversionDevice"
          label: "1#冷水机组"
          
        - id: "inst:Room-OR-01"
          type: "NODE-SPACE"
          label: "1#手术室"
          
      hyperedges:
        - id: "HEDGE-COMP-CHW-001"
          type: "HEDGE-COMPOSITION"
          fso_property: "fso:hasComponent"
          nodes:
            - head: "inst:ChilledWaterSystem"
            - members:
              - "inst:Chiller-1"
              - "inst:Chiller-2"
              - "inst:Pump-CHW-Pri-1"
              - "inst:Pump-CHW-Sec-1"
          direction: "directed"
          
        - id: "HEDGE-FLUID-CHW-LOOP-001"
          type: "HEDGE-FLUID-LOOP"
          fso_property: "fso:exchangesFluidWith"
          nodes:
            - "inst:Chiller-1"
            - "inst:Pump-CHW-Pri-1"
            - "inst:Header-CHW-Supply"
            - "inst:Pump-CHW-Sec-1"
            - "inst:AHU-OR-01"
            - "inst:Header-CHW-Return"
          direction: "undirected"
          medium: "ex:ChilledWater"
          
        - id: "HEDGE-THERMAL-001"
          type: "HEDGE-THERMAL-COUPLING"
          fso_property: "fso:exchangesHeatWith"
          nodes:
            - "inst:HX-1-PrimarySide"
            - "inst:HX-1-SecondarySide"
          direction: "undirected"
          
        - id: "HEDGE-SPACE-OR-01"
          type: "HEDGE-SPACE-SERVICE"
          fso_property: "ex:servesSpace"
          nodes:
            - systems:
              - "inst:ChilledWaterSystem"
              - "inst:VentilationSystem"
              - "inst:MedicalOxygenSystem"
              - "inst:MedicalVacuumSystem"
            - space: "inst:Room-OR-01"
          direction: "directed"
```

### 4.2 SPARQL查询接口 (Agent-05使用)

```yaml
SPARQL_Query_Interface:
  
  description: |
    提供标准SPARQL查询供Agent-05构建超图拓扑。
    所有查询基于FSO本体属性定义。

  # ═══════════════════════════════════════════════════════════════════════════
  # 系统组成查询
  # ═══════════════════════════════════════════════════════════════════════════
  
  composition_queries:
    
    # CQ1: 系统包含哪些组件？
    query_system_components:
      id: "CQ1"
      description: "查询系统包含的所有组件"
      sparql: |
        PREFIX fso: <https://w3id.org/fso#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?system ?component ?componentType ?label
        WHERE {
          ?system a fso:System ;
                  fso:hasComponent ?component .
          ?component a ?componentType ;
                     rdfs:label ?label .
          FILTER(?componentType != fso:Component)
        }
        ORDER BY ?system ?componentType
        
    # CQ2: 系统包含哪些子系统？
    query_subsystems:
      id: "CQ2"
      description: "查询系统的子系统层次"
      sparql: |
        PREFIX fso: <https://w3id.org/fso#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?system ?subsystem ?subsystemType
        WHERE {
          ?system a fso:System ;
                  fso:hasSubSystem ?subsystem .
          ?subsystem a ?subsystemType .
        }

  # ═══════════════════════════════════════════════════════════════════════════
  # 流体回路查询
  # ═══════════════════════════════════════════════════════════════════════════
  
  fluid_loop_queries:
    
    # CQ3: 同一流体回路的组件
    query_fluid_loop_components:
      id: "CQ3"
      description: "查询与指定组件在同一流体回路的所有组件"
      sparql: |
        PREFIX fso: <https://w3id.org/fso#>
        
        SELECT DISTINCT ?component
        WHERE {
          # 从指定起点沿供给/回流方向遍历
          ?start (fso:suppliesFluidTo|fso:returnsFluidTo)* ?component .
          
          # 或反向遍历
          UNION {
            ?start ^(fso:suppliesFluidTo|fso:returnsFluidTo)* ?component .
          }
        }
      note: "将?start绑定到具体组件URI执行"
      
    # CQ4: 上游/下游组件查询
    query_upstream_components:
      id: "CQ4"
      description: "查询指定组件的上游组件及距离"
      sparql: |
        PREFIX fso: <https://w3id.org/fso#>
        
        SELECT ?upstreamComponent (COUNT(?mid) AS ?distance)
        WHERE {
          ?target ^fso:suppliesFluidTo+ ?upstreamComponent .
          ?target ^fso:suppliesFluidTo* ?mid .
          ?mid ^fso:suppliesFluidTo+ ?upstreamComponent .
        }
        GROUP BY ?upstreamComponent
        ORDER BY ?distance
        
    query_downstream_components:
      id: "CQ4b"
      description: "查询指定组件的下游组件"
      sparql: |
        PREFIX fso: <https://w3id.org/fso#>
        
        SELECT ?downstreamComponent (COUNT(?mid) AS ?distance)
        WHERE {
          ?target fso:suppliesFluidTo+ ?downstreamComponent .
          ?target fso:suppliesFluidTo* ?mid .
          ?mid fso:suppliesFluidTo+ ?downstreamComponent .
        }
        GROUP BY ?downstreamComponent
        ORDER BY ?distance

  # ═══════════════════════════════════════════════════════════════════════════
  # 热耦合查询
  # ═══════════════════════════════════════════════════════════════════════════
  
  thermal_coupling_queries:
    
    # 查询热交换连接
    query_heat_exchange:
      id: "CQ5"
      description: "查询所有热交换关系"
      sparql: |
        PREFIX fso: <https://w3id.org/fso#>
        
        SELECT ?source ?target
        WHERE {
          ?source fso:transfersHeatTo ?target .
        }
        
    # 查询换热器两侧
    query_heat_exchanger_sides:
      id: "CQ6"
      description: "查询换热器的一次侧和二次侧"
      sparql: |
        PREFIX fso: <https://w3id.org/fso#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT ?hxSystem ?primarySide ?secondarySide
        WHERE {
          ?hxSystem a fso:System ;
                    fso:hasComponent ?primarySide, ?secondarySide .
          ?primarySide fso:exchangesHeatWith ?secondarySide .
          FILTER(?primarySide != ?secondarySide)
        }

  # ═══════════════════════════════════════════════════════════════════════════
  # 空间服务查询
  # ═══════════════════════════════════════════════════════════════════════════
  
  space_service_queries:
    
    # CQ7: 服务于指定空间的系统
    query_systems_serving_space:
      id: "CQ7"
      description: "查询服务于指定空间的所有系统"
      sparql: |
        PREFIX fso: <https://w3id.org/fso#>
        PREFIX bot: <https://w3id.org/bot#>
        PREFIX ex: <https://hospital.example.com/ex#>
        
        SELECT ?system ?systemLabel
        WHERE {
          ?space a bot:Space .
          ?system ex:servesSpace ?space ;
                  rdfs:label ?systemLabel .
        }
        
    # CQ8: 空间中的终端设备
    query_terminals_in_space:
      id: "CQ8"
      description: "查询空间中的所有终端设备"
      sparql: |
        PREFIX fso: <https://w3id.org/fso#>
        PREFIX bot: <https://w3id.org/bot#>
        
        SELECT ?space ?terminal ?terminalType
        WHERE {
          ?space a bot:Space ;
                 bot:containsElement ?terminal .
          ?terminal a fso:Terminal ;
                    a ?terminalType .
          FILTER(?terminalType != fso:Terminal && ?terminalType != fso:Component)
        }

  # ═══════════════════════════════════════════════════════════════════════════
  # 超图构建查询
  # ═══════════════════════════════════════════════════════════════════════════
  
  hypergraph_construction_queries:
    
    # 构建系统组成超边
    construct_composition_hyperedge:
      id: "HQ1"
      description: "构建系统组成超边图"
      sparql: |
        PREFIX fso: <https://w3id.org/fso#>
        
        CONSTRUCT {
          ?system <http://hypergraph#hasHyperedge> ?hedge .
          ?hedge <http://hypergraph#type> "HEDGE-COMPOSITION" .
          ?hedge <http://hypergraph#containsNode> ?component .
        }
        WHERE {
          ?system a fso:System ;
                  fso:hasComponent ?component .
          BIND(IRI(CONCAT(STR(?system), "-composition")) AS ?hedge)
        }
        
    # 构建流体回路超边
    construct_fluid_loop_hyperedge:
      id: "HQ2"
      description: "构建流体回路超边"
      sparql: |
        PREFIX fso: <https://w3id.org/fso#>
        PREFIX ex: <https://hospital.example.com/ex#>
        
        SELECT ?medium (GROUP_CONCAT(DISTINCT ?component; separator=",") AS ?loopComponents)
        WHERE {
          ?component ex:hasMedium ?medium .
          ?component (fso:suppliesFluidTo|fso:returnsFluidTo|
                      ^fso:suppliesFluidTo|^fso:returnsFluidTo)* ?other .
          ?other ex:hasMedium ?medium .
        }
        GROUP BY ?medium
```

---

## 五、载体-荷载耦合模型 (FSO对齐版)

### 5.1 耦合关系RDF表示

```yaml
Carrier_Payload_Coupling_RDF:
  
  description: |
    基于FSO本体和双系统模型(耗散/循环)，
    将载体-荷载耦合关系表示为RDF三元组。
    
    核心概念：
    - 载体(Carrier): 物质流 - 通过fso:exchangesFluidWith连接
    - 荷载(Payload): 能量流 - 通过fso:exchangesHeatWith传递
    - 耦合方程: 作为属性附加到组件/系统

  # ═══════════════════════════════════════════════════════════════════════════
  # 耦合类型定义
  # ═══════════════════════════════════════════════════════════════════════════
  
  coupling_types:
    
    # 水-热能耦合
    water_thermal_coupling:
      coupling_id: "ex:WaterThermalCoupling"
      carrier:
        type: "ex:Water"
        flow_property: "fso:exchangesFluidWith"
      payload:
        type: "ex:ThermalEnergy"
        flow_property: "fso:exchangesHeatWith"
      coupling_equation:
        formula: "Q = ρ × V̇ × Cp × ΔT"
        simplified: "Q(kW) = V̇(m³/h) × ΔT(°C) × 1.163"
        
      rdf_representation: |
        @prefix ex: <https://hospital.example.com/ex#> .
        @prefix fso: <https://w3id.org/fso#> .
        
        ex:WaterThermalCoupling a ex:CarrierPayloadCoupling ;
            ex:hasCarrier ex:Water ;
            ex:hasPayload ex:ThermalEnergy ;
            ex:carrierProperty fso:exchangesFluidWith ;
            ex:payloadProperty fso:exchangesHeatWith ;
            ex:couplingEquation "Q = V × ΔT × 1.163"^^xsd:string ;
            ex:couplingFactor "1.163"^^xsd:decimal ;
            ex:couplingFactorUnit "kW/(m³/h·°C)" .

    # 空气-热能耦合 (显热)
    air_sensible_coupling:
      coupling_id: "ex:AirSensibleCoupling"
      carrier: "ex:Air"
      payload: "ex:SensibleHeat"
      coupling_equation:
        formula: "Qs = ρ × V̇ × Cp × ΔT"
        simplified: "Qs(kW) = V̇(m³/h) × ΔT(°C) × 0.335"
        
    # 空气-热能耦合 (潜热)
    air_latent_coupling:
      coupling_id: "ex:AirLatentCoupling"
      carrier: "ex:Air"
      payload: "ex:LatentHeat"
      coupling_equation:
        formula: "Ql = ρ × V̇ × Δd × γ"
        simplified: "Ql(kW) = V̇(m³/h) × Δd(g/kg) × 0.833"

    # 电力耦合
    electrical_coupling:
      coupling_id: "ex:ElectricalCoupling"
      carrier: "ex:Electricity"
      payload: "ex:ElectricalEnergy"
      flow_property: "fso:exchangesElectricChargeWith"
      coupling_equation:
        three_phase: "P = √3 × U × I × cosφ"

  # ═══════════════════════════════════════════════════════════════════════════
  # 组件耦合参数RDF表示
  # ═══════════════════════════════════════════════════════════════════════════
  
  component_coupling_rdf:
    
    example_chiller: |
      @prefix ex: <https://hospital.example.com/ex#> .
      @prefix inst: <https://hospital.example.com/inst#> .
      @prefix fso: <https://w3id.org/fso#> .
      @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
      
      # 冷水机组耦合参数
      inst:Chiller-1 a fso:EnergyConversionDevice ;
          # 蒸发器侧 (冷冻水)
          ex:evaporatorCoupling [
              a ex:WaterThermalCoupling ;
              ex:volumeFlowRate "350.0"^^xsd:decimal ;  # m³/h
              ex:supplyTemperature "7.0"^^xsd:decimal ;
              ex:returnTemperature "12.0"^^xsd:decimal ;
              ex:deltaT "5.0"^^xsd:decimal ;
              ex:thermalPower "2000.0"^^xsd:decimal ;   # kW
              ex:calculatedAs "350 × 5 × 1.163 = 2035 kW"
          ] ;
          # 冷凝器侧 (冷却水)
          ex:condenserCoupling [
              a ex:WaterThermalCoupling ;
              ex:volumeFlowRate "420.0"^^xsd:decimal ;
              ex:supplyTemperature "32.0"^^xsd:decimal ;
              ex:returnTemperature "37.0"^^xsd:decimal ;
              ex:deltaT "5.0"^^xsd:decimal ;
              ex:thermalPower "2440.0"^^xsd:decimal ;
              ex:note "Q_cond = Q_evap + P_comp"
          ] ;
          # 电力消耗
          ex:electricalInput [
              a ex:ElectricalCoupling ;
              ex:electricalPower "400.0"^^xsd:decimal ;  # kW
          ] ;
          # 性能系数
          ex:COP "5.0"^^xsd:decimal .

    example_ahu: |
      @prefix ex: <https://hospital.example.com/ex#> .
      @prefix inst: <https://hospital.example.com/inst#> .
      @prefix fso: <https://w3id.org/fso#> .
      
      # 空调机组耦合参数
      inst:AHU-OR-01 a fso:Terminal ;
          # 空气侧耦合
          ex:airSideCoupling [
              a ex:AirSensibleCoupling, ex:AirLatentCoupling ;
              ex:volumeFlowRate "12000.0"^^xsd:decimal ;  # m³/h
              ex:supplyTemperature "18.0"^^xsd:decimal ;
              ex:returnTemperature "25.0"^^xsd:decimal ;
              ex:deltaT "7.0"^^xsd:decimal ;
              ex:sensiblePower "28.14"^^xsd:decimal ;  # kW
              ex:latentPower "27.97"^^xsd:decimal ;
              ex:totalPower "56.11"^^xsd:decimal
          ] ;
          # 水侧耦合 (冷冻水)
          ex:waterSideCoupling [
              a ex:WaterThermalCoupling ;
              ex:volumeFlowRate "10.0"^^xsd:decimal ;  # m³/h
              ex:supplyTemperature "7.0"^^xsd:decimal ;
              ex:returnTemperature "12.0"^^xsd:decimal ;
              ex:deltaT "5.0"^^xsd:decimal ;
              ex:thermalPower "58.15"^^xsd:decimal
          ] ;
          # 风机电力
          ex:fanPower "15.0"^^xsd:decimal .
```

### 5.2 能量平衡推理规则

```yaml
Energy_Balance_Inference:
  
  description: |
    基于FSO本体定义推理规则，支持:
    - 能量守恒验证
    - 系统级能量汇总
    - 效率计算

  # ═══════════════════════════════════════════════════════════════════════════
  # SPARQL推理查询
  # ═══════════════════════════════════════════════════════════════════════════
  
  inference_queries:
    
    # 系统能量平衡计算
    system_energy_balance:
      id: "INF-1"
      description: "计算系统的能量输入与输出平衡"
      sparql: |
        PREFIX fso: <https://w3id.org/fso#>
        PREFIX ex: <https://hospital.example.com/ex#>
        
        SELECT ?system 
               (SUM(?sourcePower) AS ?totalInput)
               (SUM(?consumerPower) AS ?totalOutput)
               (SUM(?sourcePower) - SUM(?consumerPower) AS ?balance)
        WHERE {
          ?system a fso:System .
          
          # 源组件能量
          {
            ?system fso:hasSourceComponent ?source .
            ?source ex:thermalPower ?sourcePower .
          }
          UNION
          # 消费组件能量
          {
            ?system fso:hasConsumerComponent ?consumer .
            ?consumer ex:thermalPower ?consumerPower .
          }
        }
        GROUP BY ?system
        
    # 流体回路热量传递链
    fluid_loop_energy_chain:
      id: "INF-2"
      description: "追踪流体回路中的能量传递"
      sparql: |
        PREFIX fso: <https://w3id.org/fso#>
        PREFIX ex: <https://hospital.example.com/ex#>
        
        SELECT ?source ?target ?power
        WHERE {
          ?source fso:transfersHeatTo ?target .
          ?source ex:thermalPower ?power .
        }
        
    # 系统COP计算
    system_cop_calculation:
      id: "INF-3"
      description: "计算系统综合性能系数"
      sparql: |
        PREFIX fso: <https://w3id.org/fso#>
        PREFIX ex: <https://hospital.example.com/ex#>
        
        SELECT ?system 
               (SUM(?coolingOutput) AS ?totalCooling)
               (SUM(?electricInput) AS ?totalElectric)
               (SUM(?coolingOutput) / SUM(?electricInput) AS ?systemCOP)
        WHERE {
          ?system a fso:System ;
                  fso:hasComponent ?component .
          
          OPTIONAL { ?component ex:thermalPower ?coolingOutput }
          OPTIONAL { ?component ex:electricalPower ?electricInput }
        }
        GROUP BY ?system
```

---

## 六、Agent间接口定义

### 6.1 与Agent-01/02/03对接

```yaml
Upstream_Agent_Interface:
  
  # ═══════════════════════════════════════════════════════════════════════════
  # Agent-01 系统拓扑 → Agent-04 流动模型
  # ═══════════════════════════════════════════════════════════════════════════
  
  agent01_interface:
    input_format: "YAML (Agent-01拓扑节点定义)"
    
    mapping_rules:
      topology_node_to_fso:
        - agent01_node_type: "SOURCE"
          fso_class: "fso:EnergyConversionDevice | fso:StorageDevice"
          fso_role: "fso:hasSourceComponent"
          
        - agent01_node_type: "DISTRIBUTION"
          fso_class: "fso:FlowMovingDevice | fso:Segment | fso:Fitting"
          fso_role: "fso:hasComponent"
          
        - agent01_node_type: "TERMINAL"
          fso_class: "fso:Terminal"
          fso_role: "fso:hasConsumerComponent"
          
        - agent01_node_type: "CONTROL"
          fso_class: "fso:FlowController"
          fso_role: "fso:hasComponent"
          
      system_dependency_to_fso:
        - dependency_type: "POWER_SUPPLY"
          fso_property: "fso:exchangesElectricChargeWith"
          
        - dependency_type: "THERMAL_SUPPLY"
          fso_property: "fso:exchangesHeatWith"
          
        - dependency_type: "FLUID_SUPPLY"
          fso_property: "fso:exchangesFluidWith"

  # ═══════════════════════════════════════════════════════════════════════════
  # Agent-02 空间本体 → Agent-04 流动模型
  # ═══════════════════════════════════════════════════════════════════════════
  
  agent02_interface:
    input_format: "YAML (Agent-02空间层级定义)"
    
    mapping_rules:
      space_to_bot:
        - agent02_space_type: "L4_Room"
          bot_class: "bot:Space"
          
        - agent02_space_type: "L3_Zone"
          bot_class: "bot:Zone"
          
        - agent02_space_type: "L2_Floor"
          bot_class: "bot:Storey"
          
      environmental_requirement_to_flow:
        - requirement_type: "temperature"
          generates: "HVAC流动服务需求"
          
        - requirement_type: "cleanliness"
          generates: "洁净送风需求"
          
        - requirement_type: "medical_gas"
          generates: "医疗气体流动需求"

  # ═══════════════════════════════════════════════════════════════════════════
  # Agent-03 设备本体 → Agent-04 流动模型
  # ═══════════════════════════════════════════════════════════════════════════
  
  agent03_interface:
    input_format: "YAML (Agent-03设备分类)"
    
    mapping_rules:
      equipment_to_fso_component:
        - agent03_type: "EQP-CH-CENT"
          fso_class: "fso:EnergyConversionDevice"
          flow_roles:
            - produces: "MASS-WATER-CHW"
            - consumes: "ENERGY-ELEC-LV"
            - rejects: "ENERGY-THERMAL-REJECT"
            
        - agent03_type: "EQP-PUMP-CHW"
          fso_class: "fso:FlowMovingDevice"
          flow_roles:
            - transports: "MASS-WATER-CHW"
            - consumes: "ENERGY-ELEC-LV"
            
        - agent03_type: "EQP-AHU-CLEAN"
          fso_class: "fso:Terminal"
          flow_roles:
            - consumes: "MASS-WATER-CHW"
            - produces: "MASS-AIR-CLEAN"
            - consumes: "ENERGY-ELEC-LV"
            
        - agent03_type: "EQP-O2-OUTLET"
          fso_class: "fso:Terminal"
          flow_roles:
            - dissipates: "MASS-MGAS-O2"

### 6.2 输出到Agent-05 (超图拓扑)

```yaml
Agent05_Output_Interface:

description: |
 为Agent-05提供符合超图拓扑耦合需求的数据结构。
 基于FSO本体的RDF三元组格式，支持SPARQL查询。

# ═══════════════════════════════════════════════════════════════════════════
# 输出数据包结构
# ═══════════════════════════════════════════════════════════════════════════

output_package:

 # RDF数据文件
 rdf_files:
 - file: "Agent04_FlowSystems.ttl"
 format: "Turtle"
 content: "所有流动系统的RDF三元组表示"

 - file: "Agent04_FlowConnections.ttl"
 format: "Turtle"
 content: "所有流动连接关系(fso:connectedWith及子属性)"

 - file: "Agent04_CouplingParameters.ttl"
 format: "Turtle"
 content: "载体-荷载耦合参数"

 # 超图构建辅助数据
 hypergraph_support:
 - file: "Agent04_NodeIndex.json"
 content: "所有节点URI及类型索引"
 schema: |
 {
 "nodes": [
 {
 "uri": "inst:Chiller-1",
 "type": "fso:EnergyConversionDevice",
 "systems": ["inst:ChilledWaterSystem"],
 "label": "1#冷水机组"
 }
 ]
 }

 - file: "Agent04_HyperedgeSuggestions.json"
 content: "超边构建建议"
 schema: |
 {
 "hyperedges": [
 {
 "type": "COMPOSITION",
 "head": "inst:ChilledWaterSystem",
 "members": ["inst:Chiller-1", "inst:Pump-CHW-Pri-1", ...]
 },
 {
 "type": "FLUID_LOOP",
 "medium": "ex:ChilledWater",
 "members": ["inst:Chiller-1", "inst:Pump-CHW-Pri-1", ...]
 },
 {
 "type": "THERMAL_COUPLING",
 "members": ["inst:HX-1-PrimarySide", "inst:HX-1-SecondarySide"]
 }
 ]
 }

 # SPARQL端点配置
 sparql_endpoint:
 config:
 endpoint_url: "http://localhost:3030/hospital/sparql"
 graph_uri: "https://hospital.example.com/agent04/flowmodel"

 predefined_queries:
 - query_id: "HQ-COMPOSITION"
 file: "queries/composition_hyperedges.rq"
 - query_id: "HQ-FLUID-LOOP"
 file: "queries/fluid_loop_hyperedges.rq"
 - query_id: "HQ-THERMAL"
 file: "queries/thermal_coupling_hyperedges.rq"

# ═══════════════════════════════════════════════════════════════════════════
# Agent-05所需的关键数据结构
# ═══════════════════════════════════════════════════════════════════════════

agent05_required_data:

 # 1. 节点清单 (超图顶点)
 nodes:
 description: "所有可作为超图顶点的实体"
 sources:
 - class: "fso:System"
 type: "SYSTEM_NODE"
 - class: "fso:Component"
 type: "COMPONENT_NODE"
 - class: "bot:Space"
 type: "SPACE_NODE"

 # 2. 二元边 (普通图边 - fso关系)
 binary_edges:
 description: "所有FSO流动连接关系"
 properties:
 - "fso:suppliesFluidTo"
 - "fso:returnsFluidTo"
 - "fso:transfersHeatTo"
 - "fso:exchangesElectricChargeWith"

 # 3. 超边候选 (多元关系)
 hyperedge_candidates:
 description: "可构建超边的多元关系"
 types:
 - type: "SYSTEM_COMPOSITION"
 source: "fso:hasComponent"
 pattern: "一个系统包含多个组件"

 - type: "FLUID_CIRCUIT"
 source: "fso:exchangesFluidWith路径"
 pattern: "同一流体回路的组件集合"

 - type: "THERMAL_NETWORK"
 source: "fso:exchangesHeatWith路径"
 pattern: "热耦合的组件/系统集合"

 - type: "SPACE_SERVICE"
 source: "ex:servesSpace"
 pattern: "服务同一空间的系统集合"

 # 4. 耦合参数 (边属

---