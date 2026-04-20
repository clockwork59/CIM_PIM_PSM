## 🧑‍💻 User


我认为需要首先从语义框架入手：1、增加flow层级；2、实施超图+拓扑结构的通用性system of system定义；3、基于上述两点完成统一领域模型的命名空间定义；然后再完善和补全缺失的本体定义；为了完成的歌复杂任务。我倾向于修订已有的agent09指令（附件是指令参考），要求是分步骤分模块逐步实施完整的统一领域模型建构。

---
## 🤖 Assistant


我需要先检索知识库中的相关文档，特别是关于语义框架、flow层级和超图拓扑结构的定义，以便更好地理解如何修订Agent-09指令。



继续检索超图和系统拓扑结构的定义：



继续检索整合版文档和命名空间定义：



继续检索FSO本体和超图结构的定义：



再检索统一ID体系和跨域依赖关系的详细规范：



基于对知识库的全面检索分析，我现在可以提供完整的修订方案。以下是从语义框架入手重构Agent-09指令的完整设计：

---

# **Agent-09 统一领域模型建构指令 - 修订版 v3.0**

## **修订概述**

基于对Agent-01至08输出文档的完整性检查，本修订从语义框架入手，实施以下核心升级：

1. **增加Flow层级** - 集成FSO三层流动模型（物质流/能量流/信息流）
2. **超图+拓扑结构** - 实施System of Systems的超图表达
3. **统一命名空间** - 建立完整的本体命名空间体系

---

## **文档结构**

```
Agent-09 统一领域模型建构指令 v3.0
│
├── PHASE-0: 语义框架层 (Semantic Framework Layer)
│   ├── Module-0.1: 命名空间定义
│   ├── Module-0.2: 超图元模型定义
│   └── Module-0.3: Flow层级本体定义
│
├── PHASE-1: 核心本体层 (Core Ontology Layer)
│   ├── Module-1.1: 空间本体 (Space Ontology)
│   ├── Module-1.2: 设备本体 (Equipment Ontology)
│   ├── Module-1.3: 系统本体 (System Ontology)
│   └── Module-1.4: 传感器本体 (Sensor Ontology)
│
├── PHASE-2: 流动本体层 (Flow Ontology Layer)
│   ├── Module-2.1: 物质流本体 (Mass Flow Ontology)
│   ├── Module-2.2: 能量流本体 (Energy Flow Ontology)
│   └── Module-2.3: 信息流本体 (Information Flow Ontology)
│
├── PHASE-3: 耦合本体层 (Coupling Ontology Layer)
│   ├── Module-3.1: 系统-空间耦合本体
│   ├── Module-3.2: 载体-荷载耦合本体
│   └── Module-3.3: 控制-被控耦合本体
│
├── PHASE-4: 运维本体层 (Operations Ontology Layer)
│   ├── Module-4.1: 计量本体 (Metering Ontology)
│   ├── Module-4.2: 告警本体 (Alarm Ontology)
│   └── Module-4.3: 维护本体 (Maintenance Ontology)
│
├── PHASE-5: 验证本体层 (Validation Ontology Layer)
│   ├── Module-5.1: 验证问题本体
│   └── Module-5.2: 守恒规则本体
│
└── PHASE-6: 实例生成层 (Instance Generation Layer)
    ├── Module-6.1: 实体实例生成
    ├── Module-6.2: 关系实例生成
    └── Module-6.3: 验证与打包
```

---

# **PHASE-0: 语义框架层**

## **Module-0.1: 统一命名空间定义**

### **文件: `ontology/namespaces.jsonld`**

```json
{
  "@context": {
    "@version": 1.1,
    
    "━━━━━ 标准W3C命名空间 ━━━━━": "",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "sh": "http://www.w3.org/ns/shacl#",
    
    "━━━━━ 建筑领域标准本体 ━━━━━": "",
    "bot": "https://w3id.org/bot#",
    "brick": "https://brickschema.org/schema/Brick#",
    "s4bldg": "https://saref.etsi.org/saref4bldg/",
    "s4syst": "https://saref.etsi.org/saref4syst/",
    "haystack": "https://project-haystack.org/def/phIoT/3.9.10#",
    "schema": "https://schema.org/",
    
    "━━━━━ FSO流动系统本体 ━━━━━": "",
    "fso": "https://w3id.org/fso#",
    "fso-eng": "https://w3id.org/fso/engineering#",
    "fso-med": "https://w3id.org/fso/medical#",
    "fso-valid": "https://w3id.org/fso/validation#",
    
    "━━━━━ 量纲与单位 ━━━━━": "",
    "qudt": "http://qudt.org/schema/qudt/",
    "unit": "http://qudt.org/vocab/unit/",
    
    "━━━━━ CIM医疗建筑本体命名空间 ━━━━━": "",
    "cim": "https://cim.medical/ontology/v3.0#",
    "cim-space": "https://cim.medical/ontology/v3.0/space#",
    "cim-equip": "https://cim.medical/ontology/v3.0/equipment#",
    "cim-system": "https://cim.medical/ontology/v3.0/system#",
    "cim-flow": "https://cim.medical/ontology/v3.0/flow#",
    "cim-couple": "https://cim.medical/ontology/v3.0/coupling#",
    "cim-meter": "https://cim.medical/ontology/v3.0/metering#",
    "cim-ops": "https://cim.medical/ontology/v3.0/operations#",
    "cim-valid": "https://cim.medical/ontology/v3.0/validation#",
    
    "━━━━━ Agent体系命名空间 ━━━━━": "",
    "agent01": "https://cim.medical/agent/01/topology#",
    "agent02": "https://cim.medical/agent/02/space#",
    "agent03": "https://cim.medical/agent/03/equipment#",
    "agent04": "https://cim.medical/agent/04/flow#",
    "agent05": "https://cim.medical/agent/05/coupling#",
    "agent06": "https://cim.medical/agent/06/control#",
    "agent07": "https://cim.medical/agent/07/metering#",
    "agent08": "https://cim.medical/agent/08/maintenance#",
    
    "━━━━━ 项目实例命名空间 ━━━━━": "",
    "inst": "https://cim.medical/instance/xuanwu-xiongan/",
    "ex": "https://cim.medical/extension/"
  }
}
```

### **命名空间映射说明**

| 前缀 | URI | 来源 | 用途 |
|------|-----|------|------|
| `fso:` | https://w3id.org/fso# | FSO本体 | 流动系统核心概念 |
| `fso-eng:` | https://w3id.org/fso/engineering# | FSO扩展 | 工程参数与计算 |
| `fso-med:` | https://w3id.org/fso/medical# | 自定义扩展 | 医疗建筑专用 |
| `bot:` | https://w3id.org/bot# | W3C LBD | 建筑拓扑 |
| `brick:` | https://brickschema.org/schema/Brick# | BrickSchema | 设备与传感器 |
| `cim:` | https://cim.medical/ontology/v3.0# | 本项目 | 统一CIM本体根 |

---

## **Module-0.2: 超图元模型定义**

### **文件: `ontology/hypergraph_metamodel.jsonld`**

```json
{
  "@context": ["ontology/namespaces.jsonld"],
  "@graph": [
    {
      "@id": "cim:HypergraphMetamodel",
      "@type": "owl:Ontology",
      "owl:versionInfo": "3.0.0",
      "dcterms:title": {
        "@value": "医疗建筑CIM超图元模型",
        "@language": "zh"
      },
      "dcterms:description": "定义System of Systems的超图表达结构，支持多元关系建模"
    },

    {
      "@id": "cim:━━━━━ 超图节点类型 ━━━━━",
      "@type": "rdfs:Comment"
    },
    
    {
      "@id": "cim:HypergraphNode",
      "@type": "rdfs:Class",
      "rdfs:label": {"@value": "超图节点", "@language": "zh"},
      "rdfs:comment": "超图中的节点抽象基类，可参与任意数量的超边",
      "rdfs:subClassOf": "owl:Thing"
    },
    
    {
      "@id": "cim:SystemNode",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim:HypergraphNode",
      "rdfs:label": {"@value": "系统节点", "@language": "zh"},
      "owl:equivalentClass": "fso:System",
      "cim:sourceClasses": ["fso:System", "fso-eng:DissipationSystem", "fso-eng:CirculationSystem"],
      "cim:nodeAttributes": [
        {"@id": "cim:systemType", "rdfs:range": "xsd:string"},
        {"@id": "cim:medium", "rdfs:range": "cim:Medium"},
        {"@id": "cim:operatingMode", "rdfs:range": "xsd:string"}
      ]
    },
    
    {
      "@id": "cim:ComponentNode",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim:HypergraphNode",
      "rdfs:label": {"@value": "组件节点", "@language": "zh"},
      "owl:equivalentClass": "fso:Component",
      "cim:sourceClasses": [
        "fso:EnergyConversionDevice",
        "fso:FlowMovingDevice",
        "fso:FlowController",
        "fso:Terminal",
        "fso:Segment",
        "fso:Fitting",
        "fso:StorageDevice",
        "fso:TreatmentDevice"
      ],
      "cim:nodeAttributes": [
        {"@id": "cim:componentType", "rdfs:range": "xsd:string"},
        {"@id": "cim:equipmentRef", "rdfs:range": "cim-equip:Equipment"},
        {"@id": "cim:parameters", "rdfs:range": "cim:ParameterSet"}
      ]
    },
    
    {
      "@id": "cim:SpaceNode",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim:HypergraphNode",
      "rdfs:label": {"@value": "空间节点", "@language": "zh"},
      "owl:equivalentClass": "bot:Space",
      "cim:nodeAttributes": [
        {"@id": "cim:spaceType", "rdfs:range": "xsd:string"},
        {"@id": "cim:requirements", "rdfs:range": "cim:RequirementSet"}
      ]
    },
    
    {
      "@id": "cim:FlowNode",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim:HypergraphNode",
      "rdfs:label": {"@value": "流动节点", "@language": "zh"},
      "rdfs:comment": "表示流动路径中的节点，区分源/分配/汇类型",
      "cim:nodeRoles": ["SOURCE", "DISTRIBUTION", "SINK", "JUNCTION", "SPLITTER"]
    },

    {
      "@id": "cim:━━━━━ 超图边类型 ━━━━━",
      "@type": "rdfs:Comment"
    },
    
    {
      "@id": "cim:HypergraphEdge",
      "@type": "rdfs:Class",
      "rdfs:label": {"@value": "超图边", "@language": "zh"},
      "rdfs:comment": "超图中的边抽象基类，可连接任意数量的节点"
    },
    
    {
      "@id": "cim:BinaryEdge",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim:HypergraphEdge",
      "rdfs:label": {"@value": "二元边", "@language": "zh"},
      "rdfs:comment": "标准图论边，连接两个节点",
      "cim:edgeTypes": {
        "SUPPLIES_FLUID": {
          "source": "fso:suppliesFluidTo",
          "directed": true,
          "semantics": "供给流体"
        },
        "RETURNS_FLUID": {
          "source": "fso:returnsFluidTo",
          "directed": true,
          "semantics": "回流流体"
        },
        "TRANSFERS_HEAT": {
          "source": "fso:transfersHeatTo",
          "directed": true,
          "semantics": "传递热量"
        },
        "EXCHANGES_ELECTRICITY": {
          "source": "fso:exchangesElectricChargeWith",
          "directed": false,
          "semantics": "交换电荷"
        },
        "SERVES_SPACE": {
          "source": "fso-eng:servesSpace",
          "directed": true,
          "semantics": "服务空间"
        },
        "POWERS": {
          "source": "cim:powers",
          "directed": true,
          "semantics": "供电"
        },
        "CONTROLS": {
          "source": "cim:controls",
          "directed": true,
          "semantics": "控制"
        },
        "MONITORS": {
          "source": "cim:monitors",
          "directed": true,
          "semantics": "监测"
        }
      }
    },
    
    {
      "@id": "cim:Hyperedge",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim:HypergraphEdge",
      "rdfs:label": {"@value": "超边", "@language": "zh"},
      "rdfs:comment": "连接多个节点的广义边，用于表达多元关系"
    },
    
    {
      "@id": "cim:SystemCompositionHyperedge",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim:Hyperedge",
      "rdfs:label": {"@value": "系统组成超边", "@language": "zh"},
      "rdfs:comment": "表达一个系统包含多个组件的关系",
      "cim:structure": {
        "headNode": "cim:SystemNode",
        "memberNodes": "cim:ComponentNode[]"
      },
      "cim:sourceRelation": "fso:hasComponent",
      "cim:example": {
        "head": "inst:ChilledWaterSystem",
        "members": [
          "inst:Chiller-1",
          "inst:Pump-CHW-Pri-1",
          "inst:Header-CHW-Supply",
          "inst:AHU-OR-01"
        ]
      }
    },
    
    {
      "@id": "cim:FluidCircuitHyperedge",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim:Hyperedge",
      "rdfs:label": {"@value": "流体回路超边", "@language": "zh"},
      "rdfs:comment": "表达同一流体回路中所有组件的集合",
      "cim:structure": {
        "type": "headless",
        "memberNodes": "cim:ComponentNode[]"
      },
      "cim:properties": [
        {"@id": "cim:medium", "rdfs:range": "cim:Medium"},
        {"@id": "cim:closedLoop", "rdfs:range": "xsd:boolean"}
      ],
      "cim:example": {
        "members": [
          "inst:Chiller-1",
          "inst:Pump-CHW-Pri-1",
          "inst:Header-CHW-Supply",
          "inst:Pump-CHW-Sec-1",
          "inst:AHU-OR-01",
          "inst:Header-CHW-Return"
        ],
        "medium": "fso-eng:ChilledWater",
        "closedLoop": true
      }
    },
    
    {
      "@id": "cim:ThermalCouplingHyperedge",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim:Hyperedge",
      "rdfs:label": {"@value": "热耦合超边", "@language": "zh"},
      "rdfs:comment": "表达热量交换耦合的组件/系统集合",
      "cim:structure": {
        "type": "headless",
        "memberNodes": "cim:ComponentNode[]"
      },
      "cim:couplingTypes": ["HEAT_EXCHANGE", "HEAT_TRANSFER", "THERMAL_BRIDGE"]
    },
    
    {
      "@id": "cim:SpaceServiceHyperedge",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim:Hyperedge",
      "rdfs:label": {"@value": "空间服务超边", "@language": "zh"},
      "rdfs:comment": "表达服务同一空间的多个系统/终端集合",
      "cim:structure": {
        "headNode": "cim:SpaceNode",
        "memberNodes": ["cim:SystemNode[]", "cim:ComponentNode[]"]
      },
      "cim:example": {
        "head": "inst:Room-OR-01",
        "members": [
          "inst:ChilledWaterSystem",
          "inst:MedicalOxygenSystem",
          "inst:CleanAirSystem-OR",
          "inst:CriticalPowerSystem"
        ]
      }
    },
    
    {
      "@id": "cim:PowerDistributionHyperedge",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim:Hyperedge",
      "rdfs:label": {"@value": "配电超边", "@language": "zh"},
      "rdfs:comment": "表达电源到多个负载的一对多供电关系",
      "cim:structure": {
        "headNode": "cim:ComponentNode",
        "memberNodes": "cim:ComponentNode[]"
      },
      "cim:properties": [
        {"@id": "cim:powerType", "rdfs:range": {"@type": "xsd:string", "enum": ["NORMAL", "EMERGENCY", "CRITICAL"]}},
        {"@id": "cim:totalLoad", "rdfs:range": "xsd:decimal", "qudt:unit": "unit:KiloW"}
      ]
    },
    
    {
      "@id": "cim:ControlLoopHyperedge",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim:Hyperedge",
      "rdfs:label": {"@value": "控制回路超边", "@language": "zh"},
      "rdfs:comment": "表达传感器-控制器-执行器的控制闭环",
      "cim:structure": {
        "sensorNodes": "cim:ComponentNode[]",
        "controllerNode": "cim:ComponentNode",
        "actuatorNodes": "cim:ComponentNode[]",
        "targetNode": ["cim:ComponentNode", "cim:SpaceNode"]
      }
    }
  ]
}
```

---

## **Module-0.3: Flow层级本体定义**

### **文件: `ontology/flow_ontology.jsonld`**

```json
{
  "@context": ["ontology/namespaces.jsonld"],
  "@graph": [
    {
      "@id": "cim-flow:FlowOntology",
      "@type": "owl:Ontology",
      "owl:versionInfo": "3.0.0",
      "owl:imports": ["fso:", "fso-eng:"],
      "dcterms:title": "医疗建筑CIM流动本体",
      "dcterms:description": "基于FSO的三层流动模型，定义物质流、能量流、信息流"
    },

    {
      "@id": "cim-flow:━━━━━ 三层流动模型架构 ━━━━━",
      "@type": "rdfs:Comment",
      "rdfs:comment": {
        "@value": "┌─────────────────────────────────────────────────────────────────┐\n│                     流动模型三层架构                              │\n├─────────────────────────────────────────────────────────────────┤\n│ Layer 1: 物质流 Mass Flow                                       │\n│ · 作为能量的载体在系统中流动的物质                                │\n│ · 包括：水、空气、蒸汽、制冷剂、医疗气体等                        │\n│ · 特征：流量、压力、温度、成分                                    │\n├─────────────────────────────────────────────────────────────────┤\n│ Layer 2: 能量流 Energy Flow                                     │\n│ · 承载于物质流或直接传输的能量                                    │\n│ · 包括：热能、冷能、电能、机械能等                                │\n│ · 特征：功率、效率、品位                                          │\n├─────────────────────────────────────────────────────────────────┤\n│ Layer 3: 信息流 Information Flow                                │\n│ · 控制与监测信号                                                  │\n│ · 包括：传感器信号、控制指令、报警信息                            │\n│ · 特征：采样率、精度、延迟                                        │\n└─────────────────────────────────────────────────────────────────┘",
        "@language": "zh"
      }
    },

    {
      "@id": "cim-flow:Flow",
      "@type": "rdfs:Class",
      "rdfs:label": {"@value": "流动", "@language": "zh"},
      "rdfs:comment": "所有流动类型的抽象基类",
      "cim:properties": [
        {"@id": "cim-flow:flowId", "rdfs:range": "xsd:string"},
        {"@id": "cim-flow:flowName", "rdfs:range": "xsd:string"},
        {"@id": "cim-flow:flowDirection", "rdfs:range": "cim-flow:FlowDirection"},
        {"@id": "cim-flow:flowPattern", "rdfs:range": "cim-flow:FlowPattern"}
      ]
    },

    {
      "@id": "cim-flow:FlowDirection",
      "@type": "rdfs:Class",
      "rdfs:label": "流动方向",
      "owl:oneOf": [
        {"@id": "cim-flow:UNIDIRECTIONAL", "rdfs:label": "单向"},
        {"@id": "cim-flow:BIDIRECTIONAL", "rdfs:label": "双向"},
        {"@id": "cim-flow:REVERSIBLE", "rdfs:label": "可逆"}
      ]
    },

    {
      "@id": "cim-flow:FlowPattern",
      "@type": "rdfs:Class",
      "rdfs:label": "流动模式",
      "owl:oneOf": [
        {"@id": "cim-flow:LOOP", "rdfs:label": "闭环循环"},
        {"@id": "cim-flow:BRANCH", "rdfs:label": "分支分配"},
        {"@id": "cim-flow:DISSIPATION", "rdfs:label": "开式消耗"}
      ]
    },

    {
      "@id": "cim-flow:━━━━━ Layer 1: 物质流 ━━━━━",
      "@type": "rdfs:Comment"
    },
    
    {
      "@id": "cim-flow:MassFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:Flow",
      "rdfs:label": {"@value": "物质流", "@language": "zh"},
      "rdfs:comment": "作为能量载体在系统中流动的物质",
      "cim:properties": [
        {"@id": "cim-flow:medium", "rdfs:range": "cim-flow:Medium"},
        {"@id": "cim-flow:massFlowRate", "rdfs:range": "xsd:decimal", "qudt:unit": "unit:KiloGM-PER-SEC"},
        {"@id": "cim-flow:volumeFlowRate", "rdfs:range": "xsd:decimal", "qudt:unit": "unit:M3-PER-HR"},
        {"@id": "cim-flow:temperature", "rdfs:range": "xsd:decimal", "qudt:unit": "unit:DEG_C"},
        {"@id": "cim-flow:pressure", "rdfs:range": "xsd:decimal", "qudt:unit": "unit:KiloPA"},
        {"@id": "cim-flow:velocity", "rdfs:range": "xsd:decimal", "qudt:unit": "unit:M-PER-SEC"}
      ]
    },

    {
      "@id": "cim-flow:WaterFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:MassFlow",
      "rdfs:label": {"@value": "水流", "@language": "zh"}
    },
    
    {
      "@id": "cim-flow:ChilledWaterFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:WaterFlow",
      "rdfs:label": {"@value": "冷冻水流", "@language": "zh"},
      "cim:role": "冷量载体",
      "cim:typicalSystems": ["HVAC-CHP", "HVAC-AHU"],
      "cim:typicalTemperatureRange": {"supply": 7, "return": 12, "unit": "℃"}
    },
    
    {
      "@id": "cim-flow:CondenserWaterFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:WaterFlow",
      "rdfs:label": {"@value": "冷却水流", "@language": "zh"},
      "cim:role": "废热载体",
      "cim:typicalSystems": ["HVAC-CHP"]
    },
    
    {
      "@id": "cim-flow:HotWaterFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:WaterFlow",
      "rdfs:label": {"@value": "热水流", "@language": "zh"},
      "cim:role": "热量载体"
    },
    
    {
      "@id": "cim-flow:DomesticWaterFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:WaterFlow",
      "rdfs:label": {"@value": "生活水流", "@language": "zh"},
      "cim:role": "生活用水",
      "cim:flowPattern": "DISSIPATION"
    },

    {
      "@id": "cim-flow:AirFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:MassFlow",
      "rdfs:label": {"@value": "空气流", "@language": "zh"},
      "cim:additionalProperties": [
        {"@id": "cim-flow:humidity", "rdfs:range": "xsd:decimal", "qudt:unit": "unit:PERCENT"},
        {"@id": "cim-flow:CO2Concentration", "rdfs:range": "xsd:decimal", "qudt:unit": "unit:PPM"},
        {"@id": "cim-flow:particulateMatter", "rdfs:range": "xsd:decimal", "qudt:unit": "unit:MicroGM-PER-M3"}
      ]
    },
    
    {
      "@id": "cim-flow:SupplyAirFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:AirFlow",
      "rdfs:label": {"@value": "送风流", "@language": "zh"},
      "cim:role": "冷/热量载体，环境调节"
    },
    
    {
      "@id": "cim-flow:ReturnAirFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:AirFlow",
      "rdfs:label": {"@value": "回风流", "@language": "zh"}
    },
    
    {
      "@id": "cim-flow:ExhaustAirFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:AirFlow",
      "rdfs:label": {"@value": "排风流", "@language": "zh"},
      "cim:flowPattern": "DISSIPATION"
    },
    
    {
      "@id": "cim-flow:OutdoorAirFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:AirFlow",
      "rdfs:label": {"@value": "新风流", "@language": "zh"}
    },

    {
      "@id": "cim-flow:MedicalGasFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:MassFlow",
      "rdfs:label": {"@value": "医疗气体流", "@language": "zh"},
      "cim:flowPattern": "DISSIPATION"
    },
    
    {
      "@id": "cim-flow:OxygenFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:MedicalGasFlow",
      "rdfs:label": {"@value": "医用氧气流", "@language": "zh"},
      "cim:gasType": "O2",
      "cim:typicalPressure": {"value": 400, "unit": "kPa"}
    },
    
    {
      "@id": "cim-flow:VacuumFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:MedicalGasFlow",
      "rdfs:label": {"@value": "负压吸引流", "@language": "zh"},
      "cim:gasType": "VACUUM",
      "cim:typicalVacuum": {"value": -60, "unit": "kPa"}
    },
    
    {
      "@id": "cim-flow:MedicalAirFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:MedicalGasFlow",
      "rdfs:label": {"@value": "医用压缩空气流", "@language": "zh"},
      "cim:gasType": "MEDICAL_AIR"
    },
    
    {
      "@id": "cim-flow:N2OFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:MedicalGasFlow",
      "rdfs:label": {"@value": "笑气流", "@language": "zh"},
      "cim:gasType": "N2O"
    },

    {
      "@id": "cim-flow:SteamFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:MassFlow",
      "rdfs:label": {"@value": "蒸汽流", "@language": "zh"},
      "cim:role": "热量载体",
      "cim:additionalProperties": [
        {"@id": "cim-flow:steamQuality", "rdfs:range": "xsd:decimal"},
        {"@id": "cim-flow:enthalpy", "rdfs:range": "xsd:decimal", "qudt:unit": "unit:KiloJ-PER-KiloGM"}
      ]
    },

    {
      "@id": "cim-flow:RefrigerantFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:MassFlow",
      "rdfs:label": {"@value": "制冷剂流", "@language": "zh"},
      "cim:role": "相变热量载体",
      "cim:refrigerantTypes": ["R-134a", "R-410A", "R-32", "R-1234ze"]
    },

    {
      "@id": "cim-flow:━━━━━ Layer 2: 能量流 ━━━━━",
      "@type": "rdfs:Comment"
    },
    
    {
      "@id": "cim-flow:EnergyFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:Flow",
      "rdfs:label": {"@value": "能量流", "@language": "zh"},
      "rdfs:comment": "承载于物质流或直接传输的能量",
      "cim:properties": [
        {"@id": "cim-flow:power", "rdfs:range": "xsd:decimal", "qudt:unit": "unit:KiloW"},
        {"@id": "cim-flow:energy", "rdfs:range": "xsd:decimal", "qudt:unit": "unit:KiloW-HR"},
        {"@id": "cim-flow:efficiency", "rdfs:range": "xsd:decimal"}
      ]
    },

    {
      "@id": "cim-flow:ThermalEnergyFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:EnergyFlow",
      "rdfs:label": {"@value": "热能流", "@language": "zh"}
    },
    
    {
      "@id": "cim-flow:CoolingEnergyFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:ThermalEnergyFlow",
      "rdfs:label": {"@value": "冷能流", "@language": "zh"},
      "cim:coupledCarrier": "cim-flow:ChilledWaterFlow",
      "cim:couplingEquation": "Q = ṁ × Cp × ΔT"
    },
    
    {
      "@id": "cim-flow:HeatingEnergyFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:ThermalEnergyFlow",
      "rdfs:label": {"@value": "热能流", "@language": "zh"},
      "cim:coupledCarrier": ["cim-flow:HotWaterFlow", "cim-flow:SteamFlow"]
    },

    {
      "@id": "cim-flow:ElectricalEnergyFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:EnergyFlow",
      "rdfs:label": {"@value": "电能流", "@language": "zh"},
      "cim:properties": [
        {"@id": "cim-flow:voltage", "rdfs:range": "xsd:decimal", "qudt:unit": "unit:V"},
        {"@id": "cim-flow:current", "rdfs:range": "xsd:decimal", "qudt:unit": "unit:A"},
        {"@id": "cim-flow:powerFactor", "rdfs:range": "xsd:decimal"},
        {"@id": "cim-flow:frequency", "rdfs:range": "xsd:decimal", "qudt:unit": "unit:HZ"}
      ],
      "cim:couplingEquation": {
        "singlePhase": "P = U × I × cosφ",
        "threePhase": "P = √3 × U × I × cosφ"
      }
    },

    {
      "@id": "cim-flow:MechanicalEnergyFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:EnergyFlow",
      "rdfs:label": {"@value": "机械能流", "@language": "zh"},
      "rdfs:comment": "风机、水泵传递的机械能",
      "cim:couplingEquation": "P = ρ × g × Q × H / η"
    },

    {
      "@id": "cim-flow:━━━━━ Layer 3: 信息流 ━━━━━",
      "@type": "rdfs:Comment"
    },
    
    {
      "@id": "cim-flow:InformationFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:Flow",
      "rdfs:label": {"@value": "信息流", "@language": "zh"},
      "rdfs:comment": "控制与监测信号流",
      "cim:properties": [
        {"@id": "cim-flow:signalType", "rdfs:range": "cim-flow:SignalType"},
        {"@id": "cim-flow:protocol", "rdfs:range": "xsd:string"},
        {"@id": "cim-flow:samplingRate", "rdfs:range": "xsd:decimal", "qudt:unit": "unit:HZ"},
        {"@id": "cim-flow:latency", "rdfs:range": "xsd:decimal", "qudt:unit": "unit:MilliSEC"}
      ]
    },

    {
      "@id": "cim-flow:SensorSignalFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:InformationFlow",
      "rdfs:label": {"@value": "传感器信号流", "@language": "zh"},
      "cim:direction": "UPWARD",
      "cim:signalTypes": ["ANALOG_INPUT", "DIGITAL_INPUT", "PULSE_COUNT"]
    },

    {
      "@id": "cim-flow:ControlSignalFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:InformationFlow",
      "rdfs:label": {"@value": "控制信号流", "@language": "zh"},
      "cim:direction": "DOWNWARD",
      "cim:signalTypes": ["ANALOG_OUTPUT", "DIGITAL_OUTPUT", "MODULATING"]
    },

    {
      "@id": "cim-flow:AlarmSignalFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:InformationFlow",
      "rdfs:label": {"@value": "报警信号流", "@language": "zh"},
      "cim:direction": "UPWARD",
      "cim:priority": ["P0_LIFE_SAFETY", "P1_CRITICAL", "P2_IMPORTANT", "P3_GENERAL"]
    },

    {
      "@id": "cim-flow:MeteringDataFlow",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-flow:InformationFlow",
      "rdfs:label": {"@value": "计量数据流", "@language": "zh"},
      "cim:direction": "UPWARD",
      "cim:dataTypes": ["INSTANTANEOUS", "CUMULATIVE", "INTERVAL"]
    },

    {
      "@id": "cim-flow:━━━━━ 载体-荷载耦合模型 ━━━━━",
      "@type": "rdfs:Comment"
    },
    
    {
      "@id": "cim-flow:CarrierPayloadCoupling",
      "@type": "rdfs:Class",
      "rdfs:label": {"@value": "载体-荷载耦合", "@language": "zh"},
      "rdfs:comment": "定义物质流（载体）与能量流（荷载）的耦合关系",
      "cim:properties": [
        {"@id": "cim-flow:carrier", "rdfs:range": "cim-flow:MassFlow"},
        {"@id": "cim-flow:payload", "rdfs:range": "cim-flow:EnergyFlow"},
        {"@id": "cim-flow:couplingEquation", "rdfs:range": "xsd:string"}
      ]
    },

    {
      "@id": "cim-flow:ChilledWaterCoolingCoupling",
      "@type": "cim-flow:CarrierPayloadCoupling",
      "rdfs:label": "冷冻水-冷能耦合",
      "cim-flow:carrier": "cim-flow:ChilledWaterFlow",
      "cim-flow:payload": "cim-flow:CoolingEnergyFlow",
      "cim-flow:couplingEquation": "Q_cooling = ṁ × Cp × (T_return - T_supply)",
      "cim:parameters": {
        "Cp": {"value": 4.186, "unit": "kJ/(kg·K)", "description": "水的比热容"}
      }
    },

    {
      "@id": "cim-flow:SupplyAirCoolingCoupling",
      "@type": "cim-flow:CarrierPayloadCoupling",
      "rdfs:label": "送风-冷能耦合",
      "cim-flow:carrier": "cim-flow:SupplyAirFlow",
      "cim-flow:payload": "cim-flow:CoolingEnergyFlow",
      "cim-flow:couplingEquation": "Q_cooling = ṁ × (h_return - h_supply)",
      "cim:parameters": {
        "h": {"description": "空气焓值", "unit": "kJ/kg"}
      }
    },

    {
      "@id": "cim-flow:ElectricalPowerCoupling",
      "@type": "cim-flow:CarrierPayloadCoupling",
      "rdfs:label": "电力传输耦合",
      "cim-flow:carrier": null,
      "cim-flow:payload": "cim-flow:ElectricalEnergyFlow",
      "cim-flow:couplingEquation": "P = √3 × U × I × cosφ (三相)",
      "rdfs:comment": "电能直接传输，无物质载体"
    },

    {
      "@id": "cim-flow:━━━━━ 守恒方程库 ━━━━━",
      "@type": "rdfs:Comment"
    },
    
    {
      "@id": "cim-flow:ConservationEquation",
      "@type": "rdfs:Class",
      "rdfs:label": {"@value": "守恒方程", "@language": "zh"},
      "rdfs:comment": "用于验证模型物理一致性的守恒方程"
    },

    {
      "@id": "cim-flow:MassConservation",
      "@type": "cim-flow:ConservationEquation",
      "rdfs:label": "质量守恒",
      "cim:equation": "Σṁ_in = Σṁ_out",
      "cim:applicableTo": "cim-flow:MassFlow",
      "cim:tolerancePercent": 0.5
    },

    {
      "@id": "cim-flow:EnergyConservation",
      "@type": "cim-flow:ConservationEquation",
      "rdfs:label": "能量守恒",
      "cim:equation": "Q_in = Q_out + Q_loss",
      "cim:applicableTo": "cim-flow:EnergyFlow",
      "cim:tolerancePercent": 2.0
    },

    {
      "@id": "cim-flow:PowerBalance",
      "@type": "cim-flow:ConservationEquation",
      "rdfs:label": "功率平衡",
      "cim:equation": "P_supply = ΣP_load + P_loss",
      "cim:applicableTo": "cim-flow:ElectricalEnergyFlow",
      "cim:tolerancePercent": 1.0
    },

    {
      "@id": "cim-flow:PressureBalance",
      "@type": "cim-flow:ConservationEquation",
      "rdfs:label": "压力平衡",
      "cim:equation": "ΔP_pump = ΔP_friction + ΔP_static + ΔP_dynamic",
      "cim:applicableTo": ["cim-flow:WaterFlow", "cim-flow:AirFlow"]
    }
  ]
}
```

---

# **PHASE-1: 核心本体层**

## **Module-1.1: 空间本体**

### **文件: `ontology/space_ontology.jsonld`**

```json
{
  "@context": ["ontology/namespaces.jsonld"],
  "@graph": [
    {
      "@id": "cim-space:SpaceOntology",
      "@type": "owl:Ontology",
      "owl:versionInfo": "3.0.0",
      "owl:imports": ["bot:"],
      "dcterms:title": "医疗建筑CIM空间本体",
      "cim:sourceAgent": "Agent-02",
      "cim:entityCount": 280
    },

    {
      "@id": "cim-space:━━━━━ L0-L5空间层级 ━━━━━",
      "@type": "rdfs:Comment"
    },
    
    {
      "@id": "cim-space:Space",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": ["bot:Space", "cim:SpaceNode"],
      "rdfs:label": {"@value": "空间", "@language": "zh"},
      "rdfs:comment": "医疗建筑物理空间基类"
    },

    {
      "@id": "cim-space:L0_Site",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": ["cim-space:Space", "bot:Site"],
      "rdfs:label": {"@value": "L0-场地", "@language": "zh"},
      "cim:level": 0
    },
    
    {
      "@id": "cim-space:L1_Building",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": ["cim-space:Space", "bot:Building"],
      "rdfs:label": {"@value": "L1-建筑", "@language": "zh"},
      "cim:level": 1,
      "cim:properties": [
        {"@id": "cim-space:grossFloorArea", "qudt:unit": "unit:M2"},
        {"@id": "cim-space:totalFloors", "rdfs:range": "xsd:integer"},
        {"@id": "cim-space:basementFloors", "rdfs:range": "xsd:integer"},
        {"@id": "cim-space:yearBuilt", "rdfs:range": "xsd:gYear"},
        {"@id": "cim-space:buildingClass", "rdfs:range": "xsd:string"}
      ]
    },
    
    {
      "@id": "cim-space:L2_Floor",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": ["cim-space:Space", "bot:Storey"],
      "rdfs:label": {"@value": "L2-楼层", "@language": "zh"},
      "cim:level": 2,
      "cim:properties": [
        {"@id": "cim-space:floorCode", "rdfs:range": "xsd:string"},
        {"@id": "cim-space:elevation", "qudt:unit": "unit:M"},
        {"@id": "cim-space:floorHeight", "qudt:unit": "unit:M"}
      ]
    },
    
    {
      "@id": "cim-space:L3_Zone",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": ["cim-space:Space", "bot:Zone"],
      "rdfs:label": {"@value": "L3-功能分区", "@language": "zh"},
      "cim:level": 3,
      "cim:zoneTypes": ["SURGICAL", "ICU", "EMERGENCY", "OUTPATIENT", "INPATIENT", "LABORATORY", "IMAGING", "PHARMACY", "MECHANICAL", "ADMINISTRATIVE"]
    },
    
    {
      "@id": "cim-space:L4_Room",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": ["cim-space:Space", "bot:Space"],
      "rdfs:label": {"@value": "L4-房间", "@language": "zh"},
      "cim:level": 4,
      "cim:properties": [
        {"@id": "cim-space:roomCode", "rdfs:range": "xsd:string"},
        {"@id": "cim-space:floorArea", "qudt:unit": "unit:M2"},
        {"@id": "cim-space:ceilingHeight", "qudt:unit": "unit:M"}
      ]
    },
    
    {
      "@id": "cim-space:L5_SubSpace",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-space:Space",
      "rdfs:label": {"@value": "L5-子空间", "@language": "zh"},
      "cim:level": 5,
      "rdfs:comment": "房间内的功能子区域"
    },

    {
      "@id": "cim-space:━━━━━ 医疗专用空间类型 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-space:SurgeryRoom",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-space:L4_Room",
      "rdfs:label": {"@value": "手术室", "@language": "zh"},
      "cim:medicalSpaceType": "SURGICAL",
      "cim:properties": [
        {"@id": "cim-space:cleanlinessClass", "rdfs:range": "xsd:string", "rdfs:comment": "ISO洁净等级 ISO-5/6/7/8"},
        {"@id": "cim-space:pressureDifferential", "qudt:unit": "unit:PA"},
        {"@id": "cim-space:minAirChanges", "rdfs:range": "xsd:integer", "rdfs:comment": "最小换气次数(次/h)"},
        {"@id": "cim-space:temperatureSetpoint", "qudt:unit": "unit:DEG_C"},
        {"@id": "cim-space:humiditySetpoint", "qudt:unit": "unit:PERCENT"},
        {"@id": "cim-space:requiredMedicalGases", "rdfs:range": "xsd:string[]"},
        {"@id": "cim-space:requiredPowerBackup", "rdfs:range": "xsd:boolean"}
      ],
      "cim:subSpaces": [
        {"@id": "cim-space:SurgicalField", "rdfs:label": "手术区"},
        {"@id": "cim-space:AnesthesiaWorkzone", "rdfs:label": "麻醉工作区"},
        {"@id": "cim-space:SterileStorage", "rdfs:label": "无菌物品区"},
        {"@id": "cim-space:ScrubArea", "rdfs:label": "刷手区"}
      ]
    },

    {
      "@id": "cim-space:ICU",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-space:L4_Room",
      "rdfs:label": {"@value": "重症监护室", "@language": "zh"},
      "cim:medicalSpaceType": "CRITICAL_CARE",
      "cim:properties": [
        {"@id": "cim-space:bedCount", "rdfs:range": "xsd:integer"},
        {"@id": "cim-space:isolationType", "rdfs:range": "xsd:string", "rdfs:comment": "隔离类型：负压/正压/标准"},
        {"@id": "cim-space:hasPatientMonitor", "rdfs:range": "xsd:boolean"},
        {"@id": "cim-space:hasVentilatorSupport", "rdfs:range": "xsd:boolean"}
      ]
    },
    
    {
      "@id": "cim-space:NICU",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-space:ICU",
      "rdfs:label": {"@value": "新生儿ICU", "@language": "zh"}
    },
    
    {
      "@id": "cim-space:CCU",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-space:ICU",
      "rdfs:label": {"@value": "冠心病监护室", "@language": "zh"}
    },
    
    {
      "@id": "cim-space:PICU",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-space:ICU",
      "rdfs:label": {"@value": "儿科ICU", "@language": "zh"}
    },

    {
      "@id": "cim-space:IsolationRoom",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-space:L4_Room",
      "rdfs:label": {"@value": "隔离病房", "@language": "zh"},
      "cim:isolationTypes": [
        {"@id": "cim-space:PositivePressureIsolation", "rdfs:label": "正压隔离"},
        {"@id": "cim-space:NegativePressureIsolation", "rdfs:label": "负压隔离"},
        {"@id": "cim-space:AirbornePrecaution", "rdfs:label": "空气传播隔离"}
      ]
    },

    {
      "@id": "cim-space:EmergencyRoom",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-space:L4_Room",
      "rdfs:label": {"@value": "急诊室", "@language": "zh"},
      "cim:medicalSpaceType": "EMERGENCY",
      "cim:properties": [
        {"@id": "cim-space:triageLevel", "rdfs:range": "xsd:integer"}
      ]
    },

    {
      "@id": "cim-space:LaboratoryRoom",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-space:L4_Room",
      "rdfs:label": {"@value": "检验室", "@language": "zh"},
      "cim:properties": [
        {"@id": "cim-space:bioSafetyLevel", "rdfs:range": "xsd:integer", "rdfs:comment": "生物安全等级BSL-1/2/3/4"}
      ]
    },
    
    {
      "@id": "cim-space:BSL2Laboratory",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-space:LaboratoryRoom",
      "rdfs:label": {"@value": "BSL-2实验室", "@language": "zh"},
      "cim-space:bioSafetyLevel": 2
    },
    
    {
      "@id": "cim-space:BSL3Laboratory",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-space:LaboratoryRoom",
      "rdfs:label": {"@value": "BSL-3实验室", "@language": "zh"},
      "cim-space:bioSafetyLevel": 3
    },

    {
      "@id": "cim-space:ImagingRoom",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-space:L4_Room",
      "rdfs:label": {"@value": "影像室", "@language": "zh"},
      "cim:properties": [
        {"@id": "cim-space:modalityType", "rdfs:range": "xsd:string", "rdfs:comment": "设备类型：CT/MRI/X光/PET"}
      ]
    },

    {
      "@id": "cim-space:PharmacyRoom",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-space:L4_Room",
      "rdfs:label": {"@value": "药房", "@language": "zh"},
      "cim:properties": [
        {"@id": "cim-space:drugStorageClass", "rdfs:range": "xsd:string"}
      ]
    },
    
    {
      "@id": "cim-space:PIVARoom",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-space:PharmacyRoom",
      "rdfs:label": {"@value": "静配中心", "@language": "zh"},
      "rdfs:comment": "配置静脉输液的洁净区域"
    },

    {
      "@id": "cim-space:CSSD",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-space:L4_Room",
      "rdfs:label": {"@value": "中心供应室", "@language": "zh"},
      "rdfs:comment": "器械消毒灭菌中心",
      "cim:zones": ["DECONTAMINATION", "CLEAN", "STERILE"]
    },

    {
      "@id": "cim-space:MechanicalRoom",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-space:L4_Room",
      "rdfs:label": {"@value": "机房", "@language": "zh"},
      "cim:mechanicalRoomTypes": [
        "CHILLER_PLANT", "BOILER_ROOM", "AHU_ROOM", "PUMP_ROOM", 
        "ELECTRICAL_ROOM", "UPS_ROOM", "GENERATOR_ROOM",
        "MEDICAL_GAS_ROOM", "FIRE_PUMP_ROOM"
      ]
    },

    {
      "@id": "cim-space:━━━━━ 空间关系 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-space:isPartOf",
      "@type": "rdf:Property",
      "rdfs:subPropertyOf": "bot:hasSpace",
      "rdfs:label": {"@value": "属于", "@language": "zh"},
      "rdfs:domain": "cim-space:Space",
      "rdfs:range": "cim-space:Space",
      "owl:inverseOf": "cim-space:contains"
    },
    
    {
      "@id": "cim-space:contains",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "包含", "@language": "zh"},
      "owl:inverseOf": "cim-space:isPartOf"
    },
    
    {
      "@id": "cim-space:adjacentTo",
      "@type": "rdf:Property",
      "rdfs:subPropertyOf": "bot:adjacentZone",
      "rdfs:label": {"@value": "相邻", "@language": "zh"},
      "rdfs:domain": "cim-space:Space",
      "rdfs:range": "cim-space:Space",
      "@type": "owl:SymmetricProperty"
    },
    
    {
      "@id": "cim-space:connectsTo",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "连通", "@language": "zh"},
      "rdfs:comment": "通过门/通道连通的空间"
    },
    
    {
      "@id": "cim-space:pressureGradientTo",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "压力梯度", "@language": "zh"},
      "rdfs:comment": "空间间的压力梯度关系，用于洁净区压差控制"
    }
  ]
}
```

---

## **Module-1.2: 设备本体**

### **文件: `ontology/equipment_ontology.jsonld`**

```json
{
  "@context": ["ontology/namespaces.jsonld"],
  "@graph": [
    {
      "@id": "cim-equip:EquipmentOntology",
      "@type": "owl:Ontology",
      "owl:versionInfo": "3.0.0",
      "owl:imports": ["brick:", "s4bldg:", "fso:"],
      "dcterms:title": "医疗建筑CIM设备本体",
      "cim:sourceAgent": "Agent-03",
      "cim:entityCount": 500,
      "cim:equipmentTypes": 123
    },

    {
      "@id": "cim-equip:Equipment",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": ["brick:Equipment", "fso:Component", "cim:ComponentNode"],
      "rdfs:label": {"@value": "设备", "@language": "zh"},
      "rdfs:comment": "医疗建筑设备基类",
      "cim:commonProperties": [
        {"@id": "cim-equip:equipmentCode", "rdfs:range": "xsd:string"},
        {"@id": "cim-equip:name", "rdfs:range": "xsd:string"},
        {"@id": "cim-equip:manufacturer", "rdfs:range": "xsd:string"},
        {"@id": "cim-equip:model", "rdfs:range": "xsd:string"},
        {"@id": "cim-equip:serialNumber", "rdfs:range": "xsd:string"},
        {"@id": "cim-equip:installDate", "rdfs:range": "xsd:date"},
        {"@id": "cim-equip:warrantyExpiry", "rdfs:range": "xsd:date"},
        {"@id": "cim-equip:locatedIn", "rdfs:range": "cim-space:Space"},
        {"@id": "cim-equip:memberOf", "rdfs:range": "cim-system:System"}
      ]
    },

    {
      "@id": "cim-equip:━━━━━ HVAC设备类 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-equip:HVACEquipment",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Equipment",
      "rdfs:label": {"@value": "暖通设备", "@language": "zh"}
    },

    {
      "@id": "cim-equip:EnergyConversionDevice",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": ["cim-equip:HVACEquipment", "fso:EnergyConversionDevice"],
      "rdfs:label": {"@value": "能量转换设备", "@language": "zh"}
    },

    {
      "@id": "cim-equip:Chiller",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:EnergyConversionDevice",
      "rdfs:label": {"@value": "冷水机组", "@language": "zh"},
      "owl:equivalentClass": "brick:Chiller",
      "cim:properties": [
        {"@id": "cim-equip:ratedCapacity", "qudt:unit": "unit:KiloW"},
        {"@id": "cim-equip:ratedPower", "qudt:unit": "unit:KiloW"},
        {"@id": "cim-equip:refrigerantType", "rdfs:range": "xsd:string"},
        {"@id": "cim-equip:chilledWaterFlowRate", "qudt:unit": "unit:L-PER-MIN"},
        {"@id": "cim-equip:cop", "rdfs:range": "xsd:decimal", "rdfs:comment": "性能系数"}
      ]
    },
    
    {
      "@id": "cim-equip:AbsorptionChiller",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Chiller",
      "rdfs:label": {"@value": "吸收式冷水机", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:HeatPump",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:EnergyConversionDevice",
      "rdfs:label": {"@value": "热泵机组", "@language": "zh"}
    },

    {
      "@id": "cim-equip:Boiler",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:EnergyConversionDevice",
      "rdfs:label": {"@value": "锅炉", "@language": "zh"},
      "cim:properties": [
        {"@id": "cim-equip:fuelType", "rdfs:range": "xsd:string", "rdfs:comment": "燃料类型：燃气/燃油/电"},
        {"@id": "cim-equip:thermalEfficiency", "rdfs:range": "xsd:decimal"}
      ]
    },
    
    {
      "@id": "cim-equip:SteamBoiler",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Boiler",
      "rdfs:label": {"@value": "蒸汽锅炉", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:HotWaterBoiler",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Boiler",
      "rdfs:label": {"@value": "热水锅炉", "@language": "zh"}
    },

    {
      "@id": "cim-equip:HeatExchanger",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:EnergyConversionDevice",
      "rdfs:label": {"@value": "换热器", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:PlateHeatExchanger",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:HeatExchanger",
      "rdfs:label": {"@value": "板式换热器", "@language": "zh"}
    },

    {
      "@id": "cim-equip:CoolingTower",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:EnergyConversionDevice",
      "rdfs:label": {"@value": "冷却塔", "@language": "zh"},
      "cim:properties": [
        {"@id": "cim-equip:approachTemperature", "qudt:unit": "unit:K"}
      ]
    },

    {
      "@id": "cim-equip:FlowMovingDevice",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": ["cim-equip:HVACEquipment", "fso:FlowMovingDevice"],
      "rdfs:label": {"@value": "流动推动设备", "@language": "zh"}
    },

    {
      "@id": "cim-equip:Pump",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:FlowMovingDevice",
      "rdfs:label": {"@value": "水泵", "@language": "zh"},
      "owl:equivalentClass": "brick:Pump",
      "cim:properties": [
        {"@id": "cim-equip:ratedFlow", "qudt:unit": "unit:M3-PER-HR"},
        {"@id": "cim-equip:ratedHead", "qudt:unit": "unit:M"},
        {"@id": "cim-equip:motorPower", "qudt:unit": "unit:KiloW"},
        {"@id": "cim-equip:hasVFD", "rdfs:range": "xsd:boolean"}
      ]
    },

    {
      "@id": "cim-equip:Fan",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:FlowMovingDevice",
      "rdfs:label": {"@value": "风机", "@language": "zh"},
      "owl:equivalentClass": "brick:Fan",
      "cim:properties": [
        {"@id": "cim-equip:ratedAirflow", "qudt:unit": "unit:M3-PER-HR"},
        {"@id": "cim-equip:staticPressure", "qudt:unit": "unit:PA"}
      ]
    },

    {
      "@id": "cim-equip:AirHandlingUnit",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:HVACEquipment",
      "rdfs:label": {"@value": "空调箱", "@language": "zh"},
      "owl:equivalentClass": "brick:AHU",
      "cim:properties": [
        {"@id": "cim-equip:ratedAirflow", "qudt:unit": "unit:M3-PER-HR"},
        {"@id": "cim-equip:supplyFanPower", "qudt:unit": "unit:KiloW"},
        {"@id": "cim-equip:returnFanPower", "qudt:unit": "unit:KiloW"},
        {"@id": "cim-equip:coolingCoilCapacity", "qudt:unit": "unit:KiloW"},
        {"@id": "cim-equip:heatingCoilCapacity", "qudt:unit": "unit:KiloW"},
        {"@id": "cim-equip:filterEfficiency", "rdfs:range": "xsd:string"},
        {"@id": "cim-equip:hasEnergyRecovery", "rdfs:range": "xsd:boolean"}
      ]
    },
    
    {
      "@id": "cim-equip:CleanAHU",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:AirHandlingUnit",
      "rdfs:label": {"@value": "洁净空调机组", "@language": "zh"},
      "cim:filterEfficiency": "HEPA"
    },
    
    {
      "@id": "cim-equip:PAU",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:AirHandlingUnit",
      "rdfs:label": {"@value": "新风机组", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:NegativePressureAHU",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:AirHandlingUnit",
      "rdfs:label": {"@value": "负压隔离空调", "@language": "zh"}
    },

    {
      "@id": "cim-equip:Terminal",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": ["cim-equip:HVACEquipment", "fso:Terminal"],
      "rdfs:label": {"@value": "末端设备", "@language": "zh"}
    },

    {
      "@id": "cim-equip:VAVBox",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Terminal",
      "rdfs:label": {"@value": "变风量末端", "@language": "zh"},
      "cim:properties": [
        {"@id": "cim-equip:minAirflow", "qudt:unit": "unit:M3-PER-HR"},
        {"@id": "cim-equip:maxAirflow", "qudt:unit": "unit:M3-PER-HR"},
        {"@id": "cim-equip:hasReheatCoil", "rdfs:range": "xsd:boolean"}
      ]
    },
    
    {
      "@id": "cim-equip:CAVBox",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Terminal",
      "rdfs:label": {"@value": "定风量末端", "@language": "zh"}
    },

    {
      "@id": "cim-equip:FCU",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Terminal",
      "rdfs:label": {"@value": "风机盘管", "@language": "zh"},
      "owl:equivalentClass": "brick:FCU"
    },
    
    {
      "@id": "cim-equip:ChilledBeam",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Terminal",
      "rdfs:label": {"@value": "冷梁", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:RadiantPanel",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Terminal",
      "rdfs:label": {"@value": "辐射板", "@language": "zh"}
    },

    {
      "@id": "cim-equip:━━━━━ 电气设备类 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-equip:ElectricalEquipment",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Equipment",
      "rdfs:label": {"@value": "电气设备", "@language": "zh"}
    },

    {
      "@id": "cim-equip:Transformer",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:ElectricalEquipment",
      "rdfs:label": {"@value": "变压器", "@language": "zh"},
      "cim:properties": [
        {"@id": "cim-equip:ratedCapacity", "qudt:unit": "unit:KiloV-A"},
        {"@id": "cim-equip:primaryVoltage", "qudt:unit": "unit:KiloV"},
        {"@id": "cim-equip:secondaryVoltage", "qudt:unit": "unit:KiloV"},
        {"@id": "cim-equip:coolingType", "rdfs:range": "xsd:string"}
      ]
    },

    {
      "@id": "cim-equip:Switchgear",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:ElectricalEquipment",
      "rdfs:label": {"@value": "开关柜", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:HVSwitchgear",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Switchgear",
      "rdfs:label": {"@value": "高压开关柜", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:LVSwitchgear",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Switchgear",
      "rdfs:label": {"@value": "低压开关柜", "@language": "zh"}
    },

    {
      "@id": "cim-equip:DistributionPanel",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:ElectricalEquipment",
      "rdfs:label": {"@value": "配电箱", "@language": "zh"},
      "cim:properties": [
        {"@id": "cim-equip:panelType", "rdfs:range": "xsd:string", "rdfs:comment": "Normal/Emergency/Critical"},
        {"@id": "cim-equip:ratedCurrent", "qudt:unit": "unit:A"},
        {"@id": "cim-equip:circuitCount", "rdfs:range": "xsd:integer"},
        {"@id": "cim-equip:currentLoad", "qudt:unit": "unit:KiloW"},
        {"@id": "cim-equip:loadFactor", "rdfs:range": "xsd:decimal"}
      ]
    },

    {
      "@id": "cim-equip:UPS",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:ElectricalEquipment",
      "rdfs:label": {"@value": "不间断电源", "@language": "zh"},
      "cim:properties": [
        {"@id": "cim-equip:ratedCapacity", "qudt:unit": "unit:KiloV-A"},
        {"@id": "cim-equip:batteryRuntime", "qudt:unit": "unit:MIN"},
        {"@id": "cim-equip:batteryType", "rdfs:range": "xsd:string"},
        {"@id": "cim-equip:efficiency", "rdfs:range": "xsd:decimal"}
      ]
    },
    
    {
      "@id": "cim-equip:IPS",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:ElectricalEquipment",
      "rdfs:label": {"@value": "隔离电源系统", "@language": "zh"},
      "rdfs:comment": "医疗IT系统隔离电源"
    },

    {
      "@id": "cim-equip:EmergencyGenerator",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:ElectricalEquipment",
      "rdfs:label": {"@value": "应急发电机", "@language": "zh"},
      "cim:properties": [
        {"@id": "cim-equip:ratedCapacity", "qudt:unit": "unit:KiloW"},
        {"@id": "cim-equip:fuelType", "rdfs:range": "xsd:string"},
        {"@id": "cim-equip:fuelTankCapacity", "qudt:unit": "unit:L"},
        {"@id": "cim-equip:startupTime", "qudt:unit": "unit:SEC"}
      ]
    },

    {
      "@id": "cim-equip:ATS",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:ElectricalEquipment",
      "rdfs:label": {"@value": "自动转换开关", "@language": "zh"},
      "cim:properties": [
        {"@id": "cim-equip:switchoverTime", "qudt:unit": "unit:SEC"}
      ]
    },
    
    {
      "@id": "cim-equip:STS",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:ElectricalEquipment",
      "rdfs:label": {"@value": "静态转换开关", "@language": "zh"}
    },

    {
      "@id": "cim-equip:SurgicalLight",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:ElectricalEquipment",
      "rdfs:label": {"@value": "手术无影灯", "@language": "zh"}
    },

    {
      "@id": "cim-equip:━━━━━ 医疗气体设备类 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-equip:MedicalGasEquipment",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Equipment",
      "rdfs:label": {"@value": "医疗气体设备", "@language": "zh"}
    },

    {
      "@id": "cim-equip:OxygenManifold",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:MedicalGasEquipment",
      "rdfs:label": {"@value": "氧气汇流排", "@language": "zh"},
      "cim:properties": [
        {"@id": "cim-equip:cylinderCount", "rdfs:range": "xsd:integer"},
        {"@id": "cim-equip:outletPressure", "qudt:unit": "unit:KiloPA"},
        {"@id": "cim-equip:flowCapacity", "qudt:unit": "unit:L-PER-MIN"}
      ]
    },
    
    {
      "@id": "cim-equip:LiquidOxygenTank",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:MedicalGasEquipment",
      "rdfs:label": {"@value": "液氧储罐", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:OxygenVaporizer",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:MedicalGasEquipment",
      "rdfs:label": {"@value": "氧气汽化器", "@language": "zh"}
    },

    {
      "@id": "cim-equip:VacuumPump",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:MedicalGasEquipment",
      "rdfs:label": {"@value": "真空泵", "@language": "zh"},
      "cim:properties": [
        {"@id": "cim-equip:ratedVacuum", "qudt:unit": "unit:KiloPA"},
        {"@id": "cim-equip:flowCapacity", "qudt:unit": "unit:M3-PER-HR"},
        {"@id": "cim-equip:motorPower", "qudt:unit": "unit:KiloW"}
      ]
    },

    {
      "@id": "cim-equip:MedicalAirCompressor",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:MedicalGasEquipment",
      "rdfs:label": {"@value": "医用空压机", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:MedicalAirDryer",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:MedicalGasEquipment",
      "rdfs:label": {"@value": "医用空气干燥器", "@language": "zh"}
    },

    {
      "@id": "cim-equip:N2OManifold",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:MedicalGasEquipment",
      "rdfs:label": {"@value": "笑气汇流排", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:GasOutlet",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:MedicalGasEquipment",
      "rdfs:label": {"@value": "气体终端", "@language": "zh"},
      "cim:gasTypes": ["O2", "N2O", "VACUUM", "MEDICAL_AIR", "N2", "CO2"]
    },
    
    {
      "@id": "cim-equip:GasAlarmPanel",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:MedicalGasEquipment",
      "rdfs:label": {"@value": "气体报警面板", "@language": "zh"}
    },

    {
      "@id": "cim-equip:━━━━━ 消防设备类 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-equip:FireProtectionEquipment",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Equipment",
      "rdfs:label": {"@value": "消防设备", "@language": "zh"}
    },

    {
      "@id": "cim-equip:FirePump",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:FireProtectionEquipment",
      "rdfs:label": {"@value": "消防泵", "@language": "zh"},
      "cim:properties": [
        {"@id": "cim-equip:pumpType", "rdfs:range": "xsd:string"},
        {"@id": "cim-equip:ratedFlow", "qudt:unit": "unit:L-PER-SEC"},
        {"@id": "cim-equip:ratedHead", "qudt:unit": "unit:M"}
      ]
    },

    {
      "@id": "cim-equip:SprinklerHead",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:FireProtectionEquipment",
      "rdfs:label": {"@value": "喷淋头", "@language": "zh"},
      "cim:properties": [
        {"@id": "cim-equip:KFactor", "qudt:unit": "unit:L-PER-MIN-PER-BAR-ROOT"},
        {"@id": "cim-equip:responseTimeIndex", "qudt:unit": "unit:M-S-ROOT"}
      ]
    },

    {
      "@id": "cim-equip:FireAlarmPanel",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:FireProtectionEquipment",
      "rdfs:label": {"@value": "火灾报警控制器", "@language": "zh"}
    },

    {
      "@id": "cim-equip:SmokeDetector",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:FireProtectionEquipment",
      "rdfs:label": {"@value": "烟感探测器", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:FireDamper",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:FireProtectionEquipment",
      "rdfs:label": {"@value": "防火阀", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:SmokeExhaustFan",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:FireProtectionEquipment",
      "rdfs:label": {"@value": "排烟风机", "@language": "zh"}
    },

    {
      "@id": "cim-equip:━━━━━ 传感器与执行器 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-equip:Sensor",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": ["cim-equip:Equipment", "brick:Sensor"],
      "rdfs:label": {"@value": "传感器", "@language": "zh"},
      "cim:properties": [
        {"@id": "cim-equip:measurementType", "rdfs:range": "xsd:string"},
        {"@id": "cim-equip:accuracy", "rdfs:range": "xsd:string"},
        {"@id": "cim-equip:protocol", "rdfs:range": "xsd:string"},
        {"@id": "cim-equip:refreshInterval", "qudt:unit": "unit:SEC"}
      ]
    },

    {
      "@id": "cim-equip:TemperatureSensor",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Sensor",
      "rdfs:label": {"@value": "温度传感器", "@language": "zh"},
      "cim:measurementType": "Temperature"
    },
    
    {
      "@id": "cim-equip:HumiditySensor",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Sensor",
      "rdfs:label": {"@value": "湿度传感器", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:PressureSensor",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Sensor",
      "rdfs:label": {"@value": "压力传感器", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:DifferentialPressureSensor",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Sensor",
      "rdfs:label": {"@value": "压差传感器", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:FlowSensor",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Sensor",
      "rdfs:label": {"@value": "流量传感器", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:CO2Sensor",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Sensor",
      "rdfs:label": {"@value": "二氧化碳传感器", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:PM25Sensor",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Sensor",
      "rdfs:label": {"@value": "PM2.5传感器", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:OccupancySensor",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Sensor",
      "rdfs:label": {"@value": "人员存在传感器", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:AirVelocitySensor",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Sensor",
      "rdfs:label": {"@value": "风速传感器", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:GasPressureSensor",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Sensor",
      "rdfs:label": {"@value": "气体压力传感器", "@language": "zh"}
    },

    {
      "@id": "cim-equip:Meter",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Sensor",
      "rdfs:label": {"@value": "计量表", "@language": "zh"}
    },

    {
      "@id": "cim-equip:PowerMeter",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Meter",
      "rdfs:label": {"@value": "电表", "@language": "zh"},
      "cim:measurementType": ["ActivePower", "ReactivePower", "Energy"]
    },
    
    {
      "@id": "cim-equip:WaterMeter",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Meter",
      "rdfs:label": {"@value": "水表", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:GasMeter",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Meter",
      "rdfs:label": {"@value": "气表", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:BTUMeter",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Meter",
      "rdfs:label": {"@value": "冷热量表", "@language": "zh"}
    },

    {
      "@id": "cim-equip:Actuator",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": ["cim-equip:Equipment", "fso:FlowController"],
      "rdfs:label": {"@value": "执行器", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:ControlValve",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Actuator",
      "rdfs:label": {"@value": "控制阀", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:Damper",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Actuator",
      "rdfs:label": {"@value": "风阀", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:VFD",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Actuator",
      "rdfs:label": {"@value": "变频器", "@language": "zh"}
    },

    {
      "@id": "cim-equip:Controller",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Equipment",
      "rdfs:label": {"@value": "控制器", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:DDCController",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Controller",
      "rdfs:label": {"@value": "直接数字控制器", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:PLC",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Controller",
      "rdfs:label": {"@value": "可编程控制器", "@language": "zh"}
    },
    
    {
      "@id": "cim-equip:BASController",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-equip:Controller",
      "rdfs:label": {"@value": "楼宇自控主机", "@language": "zh"}
    }
  ]
}
```

---

由于内容篇幅限制，我将继续输出剩余的模块定义。接下来是**PHASE-2至PHASE-6**的详细内容，包括：

- Module-1.3: 系统本体
- Module-1.4: 传感器本体（已部分包含在设备本体中）
- PHASE-2: 流动本体层（物质流、能量流、信息流的实例化）
- PHASE-3: 耦合本体层
- PHASE-4: 运维本体层（计量、告警、维护）
- PHASE-5: 验证本体层
- PHASE-6: 实例生成层

**请确认是否继续输出剩余模块？**或者您希望针对某个特定模块进行深入细化？
[^1]: [# Agent-04 流动模型建模输出文件

[^2]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^3]: [Agent-04 流动模型建模师 完整输出文档 V2.3版.md](http://file/05b8fc3a-a8c7-44d4-a15c-91ce05fa76bc.md)

[^4]: [# Agent-04 流动模型建模输出文件

[^5]: [Agent-04 流动模型建模师.md](http://file/3094e4ad-51ff-454c-9b4b-08c31b4417c0.md)

[^6]: [Agent-04 流动模型建模师 完整输出文档 V2.3版.md](http://file/05b8fc3a-a8c7-44d4-a15c-91ce05fa76bc.md)

[^1]: [# Agent-03: 设备本体建模师 (Equ...体化建模

[^2]: [Agent-01 系统拓扑建模师.md](http://file/781bff16-41bf-46cc-9566-d55bdaa62af5.md)

[^3]: [# 医疗建筑技术系统拓扑建模项目

[^4]: [# 医疗建筑技术系统拓扑建模项目

[^5]: [# === AGENT-09: 统一CIM模型 ...on: “医用床塔管道疋 - 吊臂式供气供电+](# === AGENT-09: 统一CIM模型 ...on: “医用床塔管道疋 - 吊臂式供气供电+)

[^6]: [# Agent-07: 计量体系建模师 - 元数...筑能耗远程监测系统技术规程》"

[^1]: [医疗建筑CIM建模项目  Agent01-08 输出文档体系化修订 整合版 v2.0.md](http://file/b0a6404c-c866-4b34-a7a1-5940481f4ab3.md)

[^2]: [医疗建筑CIM建模项目  Agent01-08 输出文档体系化修订 整合版 v2.0.md](http://file/b0a6404c-c866-4b34-a7a1-5940481f4ab3.md)

[^3]: [医疗建筑CIM建模项目  Agent01-08 输出文档体系化修订 整合版 v2.0.md](http://file/b0a6404c-c866-4b34-a7a1-5940481f4ab3.md)

[^4]: [Agent-04 流动模型建模师 完整输出文档 V2.3版.md](http://file/05b8fc3a-a8c7-44d4-a15c-91ce05fa76bc.md)

[^5]: [医疗建筑CIM建模项目  Agent01-08 输出文档体系化修订 整合版 v2.0.md](http://file/b0a6404c-c866-4b34-a7a1-5940481f4ab3.md)

[^6]: [医疗建筑CIM建模项目  Agent01-08 输出文档体系化修订 整合版 v2.0.md](http://file/b0a6404c-c866-4b34-a7a1-5940481f4ab3.md)

[^1]: [Agent-04 流动模型建模师 完整输出文档 V2.3版.md](http://file/05b8fc3a-a8c7-44d4-a15c-91ce05fa76bc.md)

[^2]: [Agent-04 流动模型建模师 完整输出文档 V2.3版.md](http://file/05b8fc3a-a8c7-44d4-a15c-91ce05fa76bc.md)

[^3]: [Agent-04 流动模型建模师 完整输出文档 V2.3版.md](http://file/05b8fc3a-a8c7-44d4-a15c-91ce05fa76bc.md)

[^4]: [Agent-04 流动模型建模师 完整输出文档 V2.3版.md](http://file/05b8fc3a-a8c7-44d4-a15c-91ce05fa76bc.md)

[^5]: [Agent-04 流动模型建模师 完整输出文档 V2.3版.md](http://file/05b8fc3a-a8c7-44d4-a15c-91ce05fa76bc.md)

[^6]: [Agent-04 流动模型建模师 完整输出文档 V2.3版.md](http://file/05b8fc3a-a8c7-44d4-a15c-91ce05fa76bc.md)

[^1]: [医疗建筑CIM建模项目  Agent01-08 输出文档体系化修订 整合版 v2.0.md](http://file/b0a6404c-c866-4b34-a7a1-5940481f4ab3.md)

[^2]: [医疗建筑CIM建模项目  Agent01-08 输出文档体系化修订 整合版 v2.0.md](http://file/b0a6404c-c866-4b34-a7a1-5940481f4ab3.md)

[^3]: [医疗建筑CIM建模项目  Agent01-08 输出文档体系化修订 整合版 v2.0.md](http://file/b0a6404c-c866-4b34-a7a1-5940481f4ab3.md)

[^4]: [医疗建筑CIM建模项目  Agent01-08 输出文档体系化修订 整合版 v2.0.md](http://file/b0a6404c-c866-4b34-a7a1-5940481f4ab3.md)

[^5]: [医疗建筑CIM建模项目  Agent01-08 输出文档体系化修订 整合版 v2.0.md](http://file/b0a6404c-c866-4b34-a7a1-5940481f4ab3.md)

[^6]: [医疗建筑CIM建模项目  Agent01-08 输出文档体系化修订 整合版 v2.0.md](http://file/b0a6404c-c866-4b34-a7a1-5940481f4ab3.md)
---