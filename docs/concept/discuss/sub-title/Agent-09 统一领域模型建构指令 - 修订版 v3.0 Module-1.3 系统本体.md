## 🧑‍💻 User


继续

---
## 🤖 Assistant


继续输出剩余模块的完整定义：

---

## **Module-1.3: 系统本体**

### **文件: `ontology/system_ontology.jsonld`**

```json
{
  "@context": ["ontology/namespaces.jsonld"],
  "@graph": [
    {
      "@id": "cim-system:SystemOntology",
      "@type": "owl:Ontology",
      "owl:versionInfo": "3.0.0",
      "owl:imports": ["fso:", "s4syst:"],
      "dcterms:title": "医疗建筑CIM系统本体",
      "cim:sourceAgent": "Agent-01",
      "cim:systemCount": 26,
      "cim:subsystemCount": 156
    },

    {
      "@id": "cim-system:━━━━━ System of Systems元模型 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-system:System",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": ["fso:System", "s4syst:System", "cim:SystemNode"],
      "rdfs:label": {"@value": "系统", "@language": "zh"},
      "rdfs:comment": "由多个组件组成的功能系统",
      "cim:properties": [
        {"@id": "cim-system:systemCode", "rdfs:range": "xsd:string"},
        {"@id": "cim-system:systemName", "rdfs:range": "xsd:string"},
        {"@id": "cim-system:systemType", "rdfs:range": "cim-system:SystemType"},
        {"@id": "cim-system:operatingMode", "rdfs:range": "xsd:string"},
        {"@id": "cim-system:designCapacity", "rdfs:range": "xsd:decimal"},
        {"@id": "cim-system:redundancyLevel", "rdfs:range": "xsd:string"}
      ]
    },

    {
      "@id": "cim-system:SystemType",
      "@type": "rdfs:Class",
      "rdfs:label": "系统类型",
      "owl:oneOf": [
        {"@id": "cim-system:LOOP_SYSTEM", "rdfs:label": "闭环循环系统"},
        {"@id": "cim-system:BRANCH_SYSTEM", "rdfs:label": "分支分配系统"},
        {"@id": "cim-system:DISSIPATION_SYSTEM", "rdfs:label": "开式消耗系统"},
        {"@id": "cim-system:HYBRID_SYSTEM", "rdfs:label": "混合型系统"}
      ]
    },

    {
      "@id": "cim-system:Subsystem",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:System",
      "rdfs:label": {"@value": "子系统", "@language": "zh"},
      "rdfs:comment": "系统内的逻辑分组"
    },

    {
      "@id": "cim-system:━━━━━ 8大系统分类 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-system:HVACSystem",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:System",
      "rdfs:label": {"@value": "暖通空调系统", "@language": "zh"},
      "cim:systemCode": "HVAC",
      "cim:subsystems": [
        "ChilledWaterPlant", "CondenserWaterPlant", "HotWaterPlant",
        "AirHandlingSystem", "CleanAirSystem", "ExhaustSystem"
      ]
    },

    {
      "@id": "cim-system:ChilledWaterPlant",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:HVACSystem",
      "rdfs:label": {"@value": "冷冻水站", "@language": "zh"},
      "owl:equivalentClass": "fso-eng:CirculationSystem",
      "cim:flowPattern": "LOOP",
      "cim:medium": "cim-flow:ChilledWaterFlow",
      "cim:typicalComponents": [
        "Chiller", "PrimaryPump", "SecondaryPump", 
        "SupplyHeader", "ReturnHeader", "ExpansionTank"
      ]
    },

    {
      "@id": "cim-system:CondenserWaterPlant",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:HVACSystem",
      "rdfs:label": {"@value": "冷却水站", "@language": "zh"},
      "cim:flowPattern": "LOOP",
      "cim:medium": "cim-flow:CondenserWaterFlow"
    },

    {
      "@id": "cim-system:HotWaterPlant",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:HVACSystem",
      "rdfs:label": {"@value": "热水站", "@language": "zh"},
      "cim:flowPattern": "LOOP",
      "cim:medium": "cim-flow:HotWaterFlow"
    },

    {
      "@id": "cim-system:SteamSystem",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:HVACSystem",
      "rdfs:label": {"@value": "蒸汽系统", "@language": "zh"},
      "cim:flowPattern": "BRANCH",
      "cim:medium": "cim-flow:SteamFlow"
    },

    {
      "@id": "cim-system:AirHandlingSystem",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:HVACSystem",
      "rdfs:label": {"@value": "空气处理系统", "@language": "zh"},
      "cim:medium": "cim-flow:AirFlow"
    },

    {
      "@id": "cim-system:CleanAirSystem",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:AirHandlingSystem",
      "rdfs:label": {"@value": "洁净空调系统", "@language": "zh"},
      "cim:serves": ["SurgeryRoom", "ICU", "CleanRoom"]
    },

    {
      "@id": "cim-system:ExhaustSystem",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:AirHandlingSystem",
      "rdfs:label": {"@value": "排风系统", "@language": "zh"},
      "cim:flowPattern": "DISSIPATION"
    },

    {
      "@id": "cim-system:ElectricalSystem",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:System",
      "rdfs:label": {"@value": "供配电系统", "@language": "zh"},
      "cim:systemCode": "ELEC",
      "cim:medium": "cim-flow:ElectricalEnergyFlow",
      "cim:subsystems": [
        "HighVoltageDistribution", "LowVoltageDistribution",
        "NormalPowerSystem", "EmergencyPowerSystem", "CriticalPowerSystem"
      ]
    },

    {
      "@id": "cim-system:HighVoltageDistribution",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:ElectricalSystem",
      "rdfs:label": {"@value": "高压配电系统", "@language": "zh"},
      "cim:voltageLevel": "10kV"
    },

    {
      "@id": "cim-system:LowVoltageDistribution",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:ElectricalSystem",
      "rdfs:label": {"@value": "低压配电系统", "@language": "zh"},
      "cim:voltageLevel": "0.4kV"
    },

    {
      "@id": "cim-system:NormalPowerSystem",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:ElectricalSystem",
      "rdfs:label": {"@value": "正常电源系统", "@language": "zh"},
      "cim:powerType": "NORMAL"
    },

    {
      "@id": "cim-system:EmergencyPowerSystem",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:ElectricalSystem",
      "rdfs:label": {"@value": "应急电源系统", "@language": "zh"},
      "cim:powerType": "EMERGENCY",
      "cim:switchoverTime": {"@value": 10, "qudt:unit": "unit:SEC"},
      "cim:typicalComponents": ["EmergencyGenerator", "ATS", "EmergencyPanel"]
    },

    {
      "@id": "cim-system:CriticalPowerSystem",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:ElectricalSystem",
      "rdfs:label": {"@value": "关键电源系统", "@language": "zh"},
      "cim:powerType": "CRITICAL",
      "cim:switchoverTime": {"@value": 0, "qudt:unit": "unit:SEC"},
      "cim:typicalComponents": ["UPS", "IPS", "STS", "CriticalPanel"]
    },

    {
      "@id": "cim-system:PlumbingSystem",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:System",
      "rdfs:label": {"@value": "给排水系统", "@language": "zh"},
      "cim:systemCode": "PLMB",
      "cim:subsystems": [
        "DomesticColdWater", "DomesticHotWater",
        "SanitaryDrainage", "StormDrainage"
      ]
    },

    {
      "@id": "cim-system:DomesticColdWater",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:PlumbingSystem",
      "rdfs:label": {"@value": "生活冷水系统", "@language": "zh"},
      "cim:flowPattern": "BRANCH",
      "cim:medium": "cim-flow:DomesticWaterFlow"
    },

    {
      "@id": "cim-system:DomesticHotWater",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:PlumbingSystem",
      "rdfs:label": {"@value": "生活热水系统", "@language": "zh"},
      "cim:flowPattern": "LOOP"
    },

    {
      "@id": "cim-system:SanitaryDrainage",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:PlumbingSystem",
      "rdfs:label": {"@value": "卫生排水系统", "@language": "zh"},
      "cim:flowPattern": "DISSIPATION"
    },

    {
      "@id": "cim-system:StormDrainage",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:PlumbingSystem",
      "rdfs:label": {"@value": "雨水排水系统", "@language": "zh"}
    },

    {
      "@id": "cim-system:MedicalGasSystem",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:System",
      "rdfs:label": {"@value": "医疗气体系统", "@language": "zh"},
      "cim:systemCode": "MGAS",
      "cim:flowPattern": "DISSIPATION",
      "cim:subsystems": [
        "OxygenSystem", "VacuumSystem", "MedicalAirSystem", 
        "N2OSystem", "NitrogenSystem", "CO2System", "AGSS"
      ]
    },

    {
      "@id": "cim-system:OxygenSystem",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:MedicalGasSystem",
      "rdfs:label": {"@value": "氧气系统", "@language": "zh"},
      "cim:gasType": "O2",
      "cim:medium": "cim-flow:OxygenFlow",
      "cim:operatingPressure": {"@value": 400, "qudt:unit": "unit:KiloPA"}
    },

    {
      "@id": "cim-system:VacuumSystem",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:MedicalGasSystem",
      "rdfs:label": {"@value": "负压吸引系统", "@language": "zh"},
      "cim:gasType": "VACUUM",
      "cim:medium": "cim-flow:VacuumFlow",
      "cim:operatingVacuum": {"@value": -60, "qudt:unit": "unit:KiloPA"}
    },

    {
      "@id": "cim-system:MedicalAirSystem",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:MedicalGasSystem",
      "rdfs:label": {"@value": "医用压缩空气系统", "@language": "zh"},
      "cim:gasType": "MEDICAL_AIR",
      "cim:medium": "cim-flow:MedicalAirFlow"
    },

    {
      "@id": "cim-system:N2OSystem",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:MedicalGasSystem",
      "rdfs:label": {"@value": "笑气系统", "@language": "zh"},
      "cim:gasType": "N2O"
    },

    {
      "@id": "cim-system:NitrogenSystem",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:MedicalGasSystem",
      "rdfs:label": {"@value": "氮气系统", "@language": "zh"},
      "cim:gasType": "N2"
    },

    {
      "@id": "cim-system:AGSS",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:MedicalGasSystem",
      "rdfs:label": {"@value": "麻醉废气排放系统", "@language": "zh"},
      "cim:gasType": "AGSS"
    },

    {
      "@id": "cim-system:FireProtectionSystem",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:System",
      "rdfs:label": {"@value": "消防系统", "@language": "zh"},
      "cim:systemCode": "FIRE",
      "cim:subsystems": [
        "SprinklerSystem", "FireAlarmSystem", 
        "GasExtinguishingSystem", "SmokeControlSystem"
      ]
    },

    {
      "@id": "cim-system:SprinklerSystem",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:FireProtectionSystem",
      "rdfs:label": {"@value": "自动喷淋系统", "@language": "zh"},
      "cim:systemType": {"@type": "xsd:string", "rdfs:comment": "湿式/干式/预作用/雨淋"}
    },

    {
      "@id": "cim-system:FireAlarmSystem",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:FireProtectionSystem",
      "rdfs:label": {"@value": "火灾报警系统", "@language": "zh"}
    },

    {
      "@id": "cim-system:GasExtinguishingSystem",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:FireProtectionSystem",
      "rdfs:label": {"@value": "气体灭火系统", "@language": "zh"}
    },

    {
      "@id": "cim-system:SmokeControlSystem",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:FireProtectionSystem",
      "rdfs:label": {"@value": "防排烟系统", "@language": "zh"}
    },

    {
      "@id": "cim-system:BASSystem",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:System",
      "rdfs:label": {"@value": "楼宇自控系统", "@language": "zh"},
      "cim:systemCode": "BAS"
    },

    {
      "@id": "cim-system:SecuritySystem",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:System",
      "rdfs:label": {"@value": "安防系统", "@language": "zh"},
      "cim:systemCode": "SEC"
    },

    {
      "@id": "cim-system:ElevatorSystem",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-system:System",
      "rdfs:label": {"@value": "电梯系统", "@language": "zh"},
      "cim:systemCode": "ELEV"
    },

    {
      "@id": "cim-system:━━━━━ 系统关系 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-system:hasComponent",
      "@type": "rdf:Property",
      "rdfs:subPropertyOf": ["fso:hasComponent", "s4syst:hasSubSystem"],
      "rdfs:label": {"@value": "包含组件", "@language": "zh"},
      "rdfs:domain": "cim-system:System",
      "rdfs:range": "cim-equip:Equipment",
      "owl:inverseOf": "cim-system:componentOf"
    },

    {
      "@id": "cim-system:componentOf",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "隶属系统", "@language": "zh"},
      "owl:inverseOf": "cim-system:hasComponent"
    },

    {
      "@id": "cim-system:hasSubsystem",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "包含子系统", "@language": "zh"},
      "rdfs:domain": "cim-system:System",
      "rdfs:range": "cim-system:Subsystem"
    },

    {
      "@id": "cim-system:servesSpace",
      "@type": "rdf:Property",
      "rdfs:subPropertyOf": "fso-eng:servesSpace",
      "rdfs:label": {"@value": "服务空间", "@language": "zh"},
      "rdfs:domain": "cim-system:System",
      "rdfs:range": "cim-space:Space"
    },

    {
      "@id": "cim-system:interfacesWith",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "接口系统", "@language": "zh"},
      "rdfs:domain": "cim-system:System",
      "rdfs:range": "cim-system:System",
      "@type": "owl:SymmetricProperty"
    },

    {
      "@id": "cim-system:dependsOn",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "依赖系统", "@language": "zh"},
      "rdfs:domain": "cim-system:System",
      "rdfs:range": "cim-system:System"
    },

    {
      "@id": "cim-system:backupSystem",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "备用系统", "@language": "zh"},
      "rdfs:domain": "cim-system:System",
      "rdfs:range": "cim-system:System"
    }
  ]
}
```

---

# **PHASE-2: 流动本体层实例化**

## **Module-2.1: 流动路径定义**

### **文件: `ontology/flow_path_ontology.jsonld`**

```json
{
  "@context": ["ontology/namespaces.jsonld"],
  "@graph": [
    {
      "@id": "cim-flow:FlowPathOntology",
      "@type": "owl:Ontology",
      "owl:versionInfo": "3.0.0",
      "dcterms:title": "流动路径本体",
      "cim:sourceAgent": "Agent-04"
    },

    {
      "@id": "cim-flow:━━━━━ 流动路径基类 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-flow:FlowPath",
      "@type": "rdfs:Class",
      "rdfs:label": {"@value": "流动路径", "@language": "zh"},
      "rdfs:comment": "流动介质在系统中的传输路径",
      "cim:properties": [
        {"@id": "cim-flow:pathId", "rdfs:range": "xsd:string"},
        {"@id": "cim-flow:sourceNode", "rdfs:range": "cim:FlowNode"},
        {"@id": "cim-flow:sinkNode", "rdfs:range": "cim:FlowNode"},
        {"@id": "cim-flow:intermediateNodes", "rdfs:range": "cim:FlowNode[]"},
        {"@id": "cim-flow:medium", "rdfs:range": "cim-flow:Flow"},
        {"@id": "cim-flow:flowDirection", "rdfs:range": "cim-flow:FlowDirection"}
      ]
    },

    {
      "@id": "cim-flow:FlowSegment",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "fso:Segment",
      "rdfs:label": {"@value": "流动段", "@language": "zh"},
      "rdfs:comment": "路径中两节点间的单一流动段",
      "cim:properties": [
        {"@id": "cim-flow:upstreamNode", "rdfs:range": "cim:ComponentNode"},
        {"@id": "cim-flow:downstreamNode", "rdfs:range": "cim:ComponentNode"},
        {"@id": "cim-flow:segmentType", "rdfs:range": "xsd:string"},
        {"@id": "cim-flow:length", "qudt:unit": "unit:M"},
        {"@id": "cim-flow:diameter", "qudt:unit": "unit:MilliM"},
        {"@id": "cim-flow:material", "rdfs:range": "xsd:string"},
        {"@id": "cim-flow:insulationType", "rdfs:range": "xsd:string"}
      ]
    },

    {
      "@id": "cim-flow:━━━━━ 流动节点角色 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-flow:SourceNode",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim:FlowNode",
      "rdfs:label": {"@value": "源节点", "@language": "zh"},
      "rdfs:comment": "流动的起始点，如冷水机组、水箱、气源",
      "cim:nodeRole": "SOURCE"
    },

    {
      "@id": "cim-flow:SinkNode",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim:FlowNode",
      "rdfs:label": {"@value": "汇节点", "@language": "zh"},
      "rdfs:comment": "流动的终点，如末端设备、排放口",
      "cim:nodeRole": "SINK"
    },

    {
      "@id": "cim-flow:DistributionNode",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim:FlowNode",
      "rdfs:label": {"@value": "分配节点", "@language": "zh"},
      "rdfs:comment": "将流量分配到多个下游的节点，如分水器",
      "cim:nodeRole": "DISTRIBUTION"
    },

    {
      "@id": "cim-flow:JunctionNode",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim:FlowNode",
      "rdfs:label": {"@value": "汇集节点", "@language": "zh"},
      "rdfs:comment": "汇集多个上游流量的节点，如集水器",
      "cim:nodeRole": "JUNCTION"
    },

    {
      "@id": "cim-flow:SplitterNode",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim:FlowNode",
      "rdfs:label": {"@value": "分流节点", "@language": "zh"},
      "cim:nodeRole": "SPLITTER"
    },

    {
      "@id": "cim-flow:RegulatorNode",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim:FlowNode",
      "rdfs:label": {"@value": "调节节点", "@language": "zh"},
      "rdfs:comment": "调节流量、压力或温度的节点",
      "cim:nodeRole": "REGULATOR"
    },

    {
      "@id": "cim-flow:TransformerNode",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim:FlowNode",
      "rdfs:label": {"@value": "转换节点", "@language": "zh"},
      "rdfs:comment": "能量形式转换的节点，如换热器",
      "cim:nodeRole": "TRANSFORMER"
    },

    {
      "@id": "cim-flow:━━━━━ 边类型定义 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-flow:FlowEdge",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim:BinaryEdge",
      "rdfs:label": {"@value": "流动边", "@language": "zh"},
      "cim:properties": [
        {"@id": "cim-flow:edgeType", "rdfs:range": "cim-flow:EdgeType"},
        {"@id": "cim-flow:capacity", "rdfs:range": "xsd:decimal"},
        {"@id": "cim-flow:medium", "rdfs:range": "cim-flow:Flow"}
      ]
    },

    {
      "@id": "cim-flow:EdgeType",
      "@type": "rdfs:Class",
      "owl:oneOf": [
        {"@id": "cim-flow:TRUNK_EDGE", "rdfs:label": "主干边"},
        {"@id": "cim-flow:BRANCH_EDGE", "rdfs:label": "分支边"},
        {"@id": "cim-flow:TERMINAL_EDGE", "rdfs:label": "末端边"},
        {"@id": "cim-flow:BYPASS_EDGE", "rdfs:label": "旁通边"},
        {"@id": "cim-flow:RETURN_EDGE", "rdfs:label": "回流边"}
      ]
    },

    {
      "@id": "cim-flow:━━━━━ 流动关系（基于FSO） ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-flow:suppliesFluidTo",
      "@type": "rdf:Property",
      "rdfs:subPropertyOf": "fso:suppliesFluidTo",
      "rdfs:label": {"@value": "供给流体至", "@language": "zh"},
      "rdfs:domain": ["cim-equip:Equipment", "cim-system:System"],
      "rdfs:range": ["cim-equip:Equipment", "cim-space:Space"],
      "cim:directedEdge": true
    },

    {
      "@id": "cim-flow:returnsFluidTo",
      "@type": "rdf:Property",
      "rdfs:subPropertyOf": "fso:returnsFluidTo",
      "rdfs:label": {"@value": "回流流体至", "@language": "zh"},
      "cim:directedEdge": true
    },

    {
      "@id": "cim-flow:transfersHeatTo",
      "@type": "rdf:Property",
      "rdfs:subPropertyOf": "fso:transfersHeatTo",
      "rdfs:label": {"@value": "传递热量至", "@language": "zh"},
      "cim:directedEdge": true
    },

    {
      "@id": "cim-flow:exchangesElectricChargeWith",
      "@type": "rdf:Property",
      "rdfs:subPropertyOf": "fso:exchangesElectricChargeWith",
      "rdfs:label": {"@value": "交换电荷", "@language": "zh"},
      "cim:directedEdge": false
    },

    {
      "@id": "cim-flow:suppliesAirTo",
      "@type": "rdf:Property",
      "rdfs:subPropertyOf": "cim-flow:suppliesFluidTo",
      "rdfs:label": {"@value": "送风至", "@language": "zh"}
    },

    {
      "@id": "cim-flow:exhaustsAirFrom",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "排风自", "@language": "zh"}
    },

    {
      "@id": "cim-flow:suppliesGasTo",
      "@type": "rdf:Property",
      "rdfs:subPropertyOf": "cim-flow:suppliesFluidTo",
      "rdfs:label": {"@value": "供气至", "@language": "zh"}
    },

    {
      "@id": "cim-flow:powersTo",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "供电至", "@language": "zh"},
      "cim:medium": "cim-flow:ElectricalEnergyFlow",
      "cim:properties": [
        {"@id": "cim-flow:powerType", "rdfs:range": "xsd:string"},
        {"@id": "cim-flow:voltage", "qudt:unit": "unit:V"},
        {"@id": "cim-flow:ratedLoad", "qudt:unit": "unit:KiloW"}
      ]
    },

    {
      "@id": "cim-flow:━━━━━ 典型流动路径模式 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-flow:ChilledWaterLoopPath",
      "@type": "cim-flow:FlowPath",
      "rdfs:label": {"@value": "冷冻水循环路径", "@language": "zh"},
      "cim:pattern": "LOOP",
      "cim:typicalSequence": [
        "Chiller.evaporator_out",
        "PrimaryPump",
        "SupplyHeader",
        "SecondaryPump",
        "AHU.coolingCoil_in",
        "AHU.coolingCoil_out",
        "ReturnHeader",
        "Chiller.evaporator_in"
      ],
      "cim:medium": "cim-flow:ChilledWaterFlow"
    },

    {
      "@id": "cim-flow:SupplyAirPath",
      "@type": "cim-flow:FlowPath",
      "rdfs:label": {"@value": "送风路径", "@language": "zh"},
      "cim:pattern": "BRANCH",
      "cim:typicalSequence": [
        "AHU.supplyFan_out",
        "SupplyDuct.main",
        "VAVBox",
        "SupplyDuct.branch",
        "Diffuser",
        "Room"
      ],
      "cim:medium": "cim-flow:SupplyAirFlow"
    },

    {
      "@id": "cim-flow:MedicalOxygenPath",
      "@type": "cim-flow:FlowPath",
      "rdfs:label": {"@value": "医用氧气路径", "@language": "zh"},
      "cim:pattern": "DISSIPATION",
      "cim:typicalSequence": [
        "LiquidOxygenTank or OxygenManifold",
        "Vaporizer",
        "PressureRegulator",
        "MainPipe",
        "FloorRiser",
        "ZoneValveBox",
        "BranchPipe",
        "GasOutlet.O2",
        "Patient"
      ],
      "cim:medium": "cim-flow:OxygenFlow"
    },

    {
      "@id": "cim-flow:NormalPowerPath",
      "@type": "cim-flow:FlowPath",
      "rdfs:label": {"@value": "正常电源路径", "@language": "zh"},
      "cim:pattern": "BRANCH",
      "cim:typicalSequence": [
        "UtilityGrid",
        "HVSwitchgear",
        "Transformer",
        "LVSwitchgear",
        "DistributionPanel",
        "CircuitBreaker",
        "Load"
      ],
      "cim:medium": "cim-flow:ElectricalEnergyFlow"
    },

    {
      "@id": "cim-flow:CriticalPowerPath",
      "@type": "cim-flow:FlowPath",
      "rdfs:label": {"@value": "关键电源路径", "@language": "zh"},
      "cim:pattern": "BRANCH",
      "cim:typicalSequence": [
        "NormalPower or EmergencyGenerator",
        "ATS",
        "UPS.input",
        "UPS.output",
        "CriticalPanel",
        "IPS (optional)",
        "CriticalLoad"
      ],
      "cim:medium": "cim-flow:ElectricalEnergyFlow",
      "cim:redundancy": "N+1"
    }
  ]
}
```

---

# **PHASE-3: 耦合本体层**

## **Module-3.1: 系统-空间耦合本体**

### **文件: `ontology/coupling_ontology.jsonld`**

```json
{
  "@context": ["ontology/namespaces.jsonld"],
  "@graph": [
    {
      "@id": "cim-couple:CouplingOntology",
      "@type": "owl:Ontology",
      "owl:versionInfo": "3.0.0",
      "dcterms:title": "系统-空间耦合本体",
      "cim:sourceAgent": "Agent-05"
    },

    {
      "@id": "cim-couple:━━━━━ 耦合类型 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-couple:Coupling",
      "@type": "rdfs:Class",
      "rdfs:label": {"@value": "耦合", "@language": "zh"},
      "rdfs:comment": "定义两个或多个实体间的相互作用关系"
    },

    {
      "@id": "cim-couple:SystemSpaceCoupling",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-couple:Coupling",
      "rdfs:label": {"@value": "系统-空间耦合", "@language": "zh"},
      "rdfs:comment": "系统或设备服务空间的关系",
      "cim:couplingTypes": [
        {"@id": "cim-couple:SERVES", "rdfs:label": "服务"},
        {"@id": "cim-couple:LOCATED_IN", "rdfs:label": "位于"},
        {"@id": "cim-couple:PASSES_THROUGH", "rdfs:label": "穿越"}
      ]
    },

    {
      "@id": "cim-couple:CarrierPayloadCoupling",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-couple:Coupling",
      "rdfs:label": {"@value": "载体-荷载耦合", "@language": "zh"},
      "rdfs:comment": "物质流与能量流的耦合",
      "cim:equation": "Energy = f(MassFlow, Properties)"
    },

    {
      "@id": "cim-couple:ControlCoupling",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-couple:Coupling",
      "rdfs:label": {"@value": "控制耦合", "@language": "zh"},
      "rdfs:comment": "传感器-控制器-执行器的控制关系"
    },

    {
      "@id": "cim-couple:ThermalCoupling",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-couple:Coupling",
      "rdfs:label": {"@value": "热耦合", "@language": "zh"},
      "rdfs:comment": "热量交换或传递关系"
    },

    {
      "@id": "cim-couple:ElectricalCoupling",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-couple:Coupling",
      "rdfs:label": {"@value": "电气耦合", "@language": "zh"},
      "rdfs:comment": "电源供电关系"
    },

    {
      "@id": "cim-couple:━━━━━ 空间服务规则 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-couple:SpaceServiceRule",
      "@type": "rdfs:Class",
      "rdfs:label": {"@value": "空间服务规则", "@language": "zh"},
      "rdfs:comment": "定义特定空间类型所需的系统和设备"
    },

    {
      "@id": "cim-couple:SurgeryRoomServiceRule",
      "@type": "cim-couple:SpaceServiceRule",
      "rdfs:label": "手术室服务规则",
      "cim:targetSpaceType": "cim-space:SurgeryRoom",
      "cim:requiredSystems": [
        {
          "system": "cim-system:CleanAirSystem",
          "requirement": "MANDATORY",
          "parameters": {
            "cleanlinessClass": "ISO-5 to ISO-7",
            "minAirChanges": 25,
            "pressureDifferential": ">15Pa"
          }
        },
        {
          "system": "cim-system:CriticalPowerSystem",
          "requirement": "MANDATORY",
          "parameters": {
            "backupTime": ">=30min",
            "switchoverTime": "0s"
          }
        },
        {
          "system": "cim-system:OxygenSystem",
          "requirement": "MANDATORY",
          "parameters": {
            "outletCount": ">=2",
            "pressure": "400kPa"
          }
        },
        {
          "system": "cim-system:VacuumSystem",
          "requirement": "MANDATORY",
          "parameters": {
            "outletCount": ">=2",
            "vacuum": "-60kPa"
          }
        },
        {
          "system": "cim-system:N2OSystem",
          "requirement": "CONDITIONAL",
          "condition": "全麻手术室"
        },
        {
          "system": "cim-system:MedicalAirSystem",
          "requirement": "MANDATORY"
        }
      ],
      "cim:requiredEquipment": [
        {"type": "cim-equip:SurgicalLight", "count": ">=1"},
        {"type": "cim-equip:UPS", "count": ">=1"},
        {"type": "cim-equip:GasOutlet", "gasTypes": ["O2", "N2O", "VAC", "MA"]}
      ]
    },

    {
      "@id": "cim-couple:ICUServiceRule",
      "@type": "cim-couple:SpaceServiceRule",
      "rdfs:label": "ICU服务规则",
      "cim:targetSpaceType": "cim-space:ICU",
      "cim:requiredSystems": [
        {
          "system": "cim-system:AirHandlingSystem",
          "requirement": "MANDATORY",
          "parameters": {
            "minAirChanges": 12,
            "filtration": "HEPA"
          }
        },
        {
          "system": "cim-system:CriticalPowerSystem",
          "requirement": "MANDATORY"
        },
        {
          "system": "cim-system:OxygenSystem",
          "requirement": "MANDATORY"
        },
        {
          "system": "cim-system:VacuumSystem",
          "requirement": "MANDATORY"
        },
        {
          "system": "cim-system:MedicalAirSystem",
          "requirement": "MANDATORY"
        }
      ]
    },

    {
      "@id": "cim-couple:NegativePressureRoomServiceRule",
      "@type": "cim-couple:SpaceServiceRule",
      "rdfs:label": "负压隔离病房服务规则",
      "cim:targetSpaceType": "cim-space:NegativePressureIsolation",
      "cim:requiredSystems": [
        {
          "system": "cim-system:ExhaustSystem",
          "requirement": "MANDATORY",
          "parameters": {
            "pressureDifferential": "<-15Pa",
            "exhaustAirTreatment": "HEPA+UV"
          }
        }
      ]
    },

    {
      "@id": "cim-couple:━━━━━ 设备位置规则 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-couple:EquipmentLocationRule",
      "@type": "rdfs:Class",
      "rdfs:label": {"@value": "设备位置规则", "@language": "zh"}
    },

    {
      "@id": "cim-couple:ChillerLocationRule",
      "@type": "cim-couple:EquipmentLocationRule",
      "cim:equipmentType": "cim-equip:Chiller",
      "cim:allowedLocations": ["cim-space:MechanicalRoom.CHILLER_PLANT"],
      "cim:constraints": [
        {"type": "minFloorLoad", "value": 1500, "unit": "kg/m2"},
        {"type": "minCeilingHeight", "value": 5, "unit": "m"},
        {"type": "vibrationIsolation", "required": true}
      ]
    },

    {
      "@id": "cim-couple:CoolingTowerLocationRule",
      "@type": "cim-couple:EquipmentLocationRule",
      "cim:equipmentType": "cim-equip:CoolingTower",
      "cim:allowedLocations": ["cim-space:Roof", "cim-space:OutdoorArea"],
      "cim:constraints": [
        {"type": "minDistanceFromIntake", "value": 15, "unit": "m"},
        {"type": "noiseLimit", "value": 65, "unit": "dB(A)"}
      ]
    },

    {
      "@id": "cim-couple:EmergencyGeneratorLocationRule",
      "@type": "cim-couple:EquipmentLocationRule",
      "cim:equipmentType": "cim-equip:EmergencyGenerator",
      "cim:allowedLocations": ["cim-space:MechanicalRoom.GENERATOR_ROOM", "cim-space:OutdoorArea"],
      "cim:constraints": [
        {"type": "ventilation", "value": "adequate for combustion and cooling"},
        {"type": "fuelStorage", "value": "fire-rated room or outdoor"},
        {"type": "exhaustTreatment", "required": true}
      ]
    },

    {
      "@id": "cim-couple:━━━━━ 管路穿越规则 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-couple:PipePassThroughRule",
      "@type": "rdfs:Class",
      "rdfs:label": {"@value": "管路穿越规则", "@language": "zh"}
    },

    {
      "@id": "cim-couple:FireBarrierPenetrationRule",
      "@type": "cim-couple:PipePassThroughRule",
      "rdfs:label": "防火分区穿越规则",
      "cim:constraint": "所有穿越防火分区的管道必须安装防火阀或防火封堵",
      "cim:requiredEquipment": ["cim-equip:FireDamper", "FireStop"]
    },

    {
      "@id": "cim-couple:CleanZonePenetrationRule",
      "@type": "cim-couple:PipePassThroughRule",
      "rdfs:label": "洁净区穿越规则",
      "cim:constraint": "穿越洁净区的管道需密封处理，不得形成污染通道"
    },

    {
      "@id": "cim-couple:━━━━━ 服务关系属性 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-couple:serves",
      "@type": "rdf:Property",
      "rdfs:subPropertyOf": "fso-eng:servesSpace",
      "rdfs:label": {"@value": "服务", "@language": "zh"},
      "rdfs:domain": ["cim-equip:Equipment", "cim-system:System"],
      "rdfs:range": "cim-space:Space",
      "cim:properties": [
        {"@id": "cim-couple:serviceType", "rdfs:range": "xsd:string"},
        {"@id": "cim-couple:capacity", "rdfs:range": "xsd:decimal"},
        {"@id": "cim-couple:priority", "rdfs:range": "xsd:integer"}
      ]
    },

    {
      "@id": "cim-couple:locatedIn",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "位于", "@language": "zh"},
      "rdfs:domain": "cim-equip:Equipment",
      "rdfs:range": "cim-space:Space"
    },

    {
      "@id": "cim-couple:passesThrough",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "穿越", "@language": "zh"},
      "rdfs:domain": "cim-flow:FlowSegment",
      "rdfs:range": "cim-space:Space"
    },

    {
      "@id": "cim-couple:controls",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "控制", "@language": "zh"},
      "rdfs:domain": "cim-equip:Controller",
      "rdfs:range": "cim-equip:Equipment"
    },

    {
      "@id": "cim-couple:monitors",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "监测", "@language": "zh"},
      "rdfs:domain": "cim-equip:Sensor",
      "rdfs:range": ["cim-equip:Equipment", "cim-space:Space"]
    },

    {
      "@id": "cim-couple:actuates",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "驱动", "@language": "zh"},
      "rdfs:domain": "cim-equip:Controller",
      "rdfs:range": "cim-equip:Actuator"
    }
  ]
}
```

---

# **PHASE-4: 运维本体层**

## **Module-4.1: 计量本体**

### **文件: `ontology/metering_ontology.jsonld`**

```json
{
  "@context": ["ontology/namespaces.jsonld"],
  "@graph": [
    {
      "@id": "cim-meter:MeteringOntology",
      "@type": "owl:Ontology",
      "owl:versionInfo": "3.0.0",
      "dcterms:title": "计量体系本体",
      "cim:sourceAgent": "Agent-07",
      "cim:meteringPoints": 189
    },

    {
      "@id": "cim-meter:━━━━━ 4级计量层级 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-meter:MeteringPoint",
      "@type": "rdfs:Class",
      "rdfs:label": {"@value": "计量点", "@language": "zh"},
      "cim:properties": [
        {"@id": "cim-meter:meterCode", "rdfs:range": "xsd:string"},
        {"@id": "cim-meter:meteringLevel", "rdfs:range": "cim-meter:MeteringLevel"},
        {"@id": "cim-meter:energyType", "rdfs:range": "cim-meter:EnergyType"},
        {"@id": "cim-meter:meterRef", "rdfs:range": "cim-equip:Meter"},
        {"@id": "cim-meter:accuracy", "rdfs:range": "xsd:string"}
      ]
    },

    {
      "@id": "cim-meter:MeteringLevel",
      "@type": "rdfs:Class",
      "owl:oneOf": [
        {
          "@id": "cim-meter:L0_TOTAL",
          "rdfs:label": {"@value": "L0-总表", "@language": "zh"},
          "rdfs:comment": "建筑总进线计量",
          "cim:level": 0
        },
        {
          "@id": "cim-meter:L1_AREA",
          "rdfs:label": {"@value": "L1-区域表", "@language": "zh"},
          "rdfs:comment": "功能区域或楼层计量",
          "cim:level": 1
        },
        {
          "@id": "cim-meter:L2_TENANT",
          "rdfs:label": {"@value": "L2-分户表", "@language": "zh"},
          "rdfs:comment": "科室或租户计量",
          "cim:level": 2
        },
        {
          "@id": "cim-meter:L3_SUBITEM",
          "rdfs:label": {"@value": "L3-分项表", "@language": "zh"},
          "rdfs:comment": "分项用途计量（照明/插座/空调等）",
          "cim:level": 3
        }
      ]
    },

    {
      "@id": "cim-meter:EnergyType",
      "@type": "rdfs:Class",
      "owl:oneOf": [
        {"@id": "cim-meter:ELECTRICITY", "rdfs:label": "电能"},
        {"@id": "cim-meter:NATURAL_GAS", "rdfs:label": "天然气"},
        {"@id": "cim-meter:MUNICIPAL_WATER", "rdfs:label": "市政水"},
        {"@id": "cim-meter:CHILLED_WATER", "rdfs:label": "冷冻水"},
        {"@id": "cim-meter:HOT_WATER", "rdfs:label": "热水"},
        {"@id": "cim-meter:STEAM", "rdfs:label": "蒸汽"},
        {"@id": "cim-meter:MEDICAL_GAS", "rdfs:label": "医疗气体"}
      ]
    },

    {
      "@id": "cim-meter:VirtualMeter",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-meter:MeteringPoint",
      "rdfs:label": {"@value": "虚拟计量点", "@language": "zh"},
      "rdfs:comment": "通过计算得出的计量值，非物理仪表",
      "cim:properties": [
        {"@id": "cim-meter:calculationFormula", "rdfs:range": "xsd:string"},
        {"@id": "cim-meter:sourceMeters", "rdfs:range": "cim-meter:MeteringPoint[]"}
      ]
    },

    {
      "@id": "cim-meter:━━━━━ 分摊规则 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-meter:AllocationRule",
      "@type": "rdfs:Class",
      "rdfs:label": {"@value": "分摊规则", "@language": "zh"}
    },

    {
      "@id": "cim-meter:AreaBasedAllocation",
      "@type": "cim-meter:AllocationRule",
      "rdfs:label": {"@value": "按面积分摊", "@language": "zh"},
      "cim:formula": "Allocation_i = Total × (Area_i / Σ Area)"
    },

    {
      "@id": "cim-meter:ConsumptionBasedAllocation",
      "@type": "cim-meter:AllocationRule",
      "rdfs:label": {"@value": "按用量分摊", "@language": "zh"},
      "cim:formula": "Allocation_i = SubMeter_i + (Unmetered × SubMeter_i / Σ SubMeter)"
    },

    {
      "@id": "cim-meter:TimeBasedAllocation",
      "@type": "cim-meter:AllocationRule",
      "rdfs:label": {"@value": "按时间分摊", "@language": "zh"},
      "cim:formula": "Allocation_i = Total × (OperatingHours_i / Σ OperatingHours)"
    },

    {
      "@id": "cim-meter:━━━━━ 计量关系 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-meter:meters",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "计量", "@language": "zh"},
      "rdfs:domain": "cim-meter:MeteringPoint",
      "rdfs:range": ["cim-equip:Equipment", "cim-space:Space", "cim-system:System"]
    },

    {
      "@id": "cim-meter:allocatesTo",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "分摊至", "@language": "zh"},
      "rdfs:domain": "cim-meter:MeteringPoint",
      "rdfs:range": "cim-meter:MeteringPoint"
    },

    {
      "@id": "cim-meter:parentMeter",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "上级计量点", "@language": "zh"},
      "rdfs:domain": "cim-meter:MeteringPoint",
      "rdfs:range": "cim-meter:MeteringPoint"
    },

    {
      "@id": "cim-meter:childMeters",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "下级计量点", "@language": "zh"},
      "owl:inverseOf": "cim-meter:parentMeter"
    }
  ]
}
```

---

## **Module-4.2: 告警本体**

### **文件: `ontology/alarm_ontology.jsonld`**

```json
{
  "@context": ["ontology/namespaces.jsonld"],
  "@graph": [
    {
      "@id": "cim-ops:AlarmOntology",
      "@type": "owl:Ontology",
      "owl:versionInfo": "3.0.0",
      "dcterms:title": "告警管理本体",
      "cim:sourceAgent": "Agent-08"
    },

    {
      "@id": "cim-ops:━━━━━ 告警优先级 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-ops:Alarm",
      "@type": "rdfs:Class",
      "rdfs:label": {"@value": "告警", "@language": "zh"},
      "cim:properties": [
        {"@id": "cim-ops:alarmCode", "rdfs:range": "xsd:string"},
        {"@id": "cim-ops:alarmType", "rdfs:range": "cim-ops:AlarmType"},
        {"@id": "cim-ops:priority", "rdfs:range": "cim-ops:AlarmPriority"},
        {"@id": "cim-ops:source", "rdfs:range": ["cim-equip:Equipment", "cim-system:System"]},
        {"@id": "cim-ops:timestamp", "rdfs:range": "xsd:dateTime"},
        {"@id": "cim-ops:status", "rdfs:range": "cim-ops:AlarmStatus"},
        {"@id": "cim-ops:acknowledgedBy", "rdfs:range": "xsd:string"},
        {"@id": "cim-ops:clearedAt", "rdfs:range": "xsd:dateTime"}
      ]
    },

    {
      "@id": "cim-ops:AlarmPriority",
      "@type": "rdfs:Class",
      "owl:oneOf": [
        {
          "@id": "cim-ops:P0_LIFE_SAFETY",
          "rdfs:label": {"@value": "P0-生命安全", "@language": "zh"},
          "cim:priority": 0,
          "cim:responseTime": "立即",
          "cim:escalation": "自动通知应急团队",
          "cim:examples": ["火灾报警", "医疗气体故障", "手术室电源故障"]
        },
        {
          "@id": "cim-ops:P1_CRITICAL",
          "rdfs:label": {"@value": "P1-关键", "@language": "zh"},
          "cim:priority": 1,
          "cim:responseTime": "15分钟",
          "cim:escalation": "通知值班工程师和管理人员",
          "cim:examples": ["冷水机组故障", "UPS电池低电量", "ICU空调故障"]
        },
        {
          "@id": "cim-ops:P2_IMPORTANT",
          "rdfs:label": {"@value": "P2-重要", "@language": "zh"},
          "cim:priority": 2,
          "cim:responseTime": "1小时",
          "cim:escalation": "通知值班工程师",
          "cim:examples": ["普通区域空调故障", "非关键设备告警"]
        },
        {
          "@id": "cim-ops:P3_GENERAL",
          "rdfs:label": {"@value": "P3-一般", "@language": "zh"},
          "cim:priority": 3,
          "cim:responseTime": "4小时",
          "cim:escalation": "记录待处理",
          "cim:examples": ["维护提醒", "参数超限预警"]
        }
      ]
    },

    {
      "@id": "cim-ops:AlarmType",
      "@type": "rdfs:Class",
      "owl:oneOf": [
        {"@id": "cim-ops:THRESHOLD_ALARM", "rdfs:label": "阈值告警"},
        {"@id": "cim-ops:STATUS_ALARM", "rdfs:label": "状态告警"},
        {"@id": "cim-ops:COMMUNICATION_ALARM", "rdfs:label": "通讯告警"},
        {"@id": "cim-ops:MAINTENANCE_ALARM", "rdfs:label": "维护告警"},
        {"@id": "cim-ops:SAFETY_ALARM", "rdfs:label": "安全告警"}
      ]
    },

    {
      "@id": "cim-ops:AlarmStatus",
      "@type": "rdfs:Class",
      "owl:oneOf": [
        {"@id": "cim-ops:ACTIVE", "rdfs:label": "活动"},
        {"@id": "cim-ops:ACKNOWLEDGED", "rdfs:label": "已确认"},
        {"@id": "cim-ops:CLEARED", "rdfs:label": "已清除"},
        {"@id": "cim-ops:SUPPRESSED", "rdfs:label": "已抑制"}
      ]
    },

    {
      "@id": "cim-ops:━━━━━ 告警关系 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-ops:triggersAlarm",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "触发告警", "@language": "zh"},
      "rdfs:domain": ["cim-equip:Equipment", "cim-equip:Sensor"],
      "rdfs:range": "cim-ops:Alarm"
    },

    {
      "@id": "cim-ops:escalatesTo",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "升级至", "@language": "zh"},
      "rdfs:domain": "cim-ops:Alarm",
      "rdfs:range": "cim-ops:Alarm"
    },

    {
      "@id": "cim-ops:correlatedWith",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "关联告警", "@language": "zh"},
      "rdfs:domain": "cim-ops:Alarm",
      "rdfs:range": "cim-ops:Alarm",
      "@type": "owl:SymmetricProperty"
    },

    {
      "@id": "cim-ops:rootCauseOf",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "根因", "@language": "zh"},
      "rdfs:domain": "cim-ops:Alarm",
      "rdfs:range": "cim-ops:Alarm"
    }
  ]
}
```

---

## **Module-4.3: 维护本体**

### **文件: `ontology/maintenance_ontology.jsonld`**

```json
{
  "@context": ["ontology/namespaces.jsonld"],
  "@graph": [
    {
      "@id": "cim-ops:MaintenanceOntology",
      "@type": "owl:Ontology",
      "owl:versionInfo": "3.0.0",
      "dcterms:title": "维护管理本体",
      "cim:sourceAgent": "Agent-08"
    },

    {
      "@id": "cim-ops:━━━━━ 工单类型 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-ops:WorkOrder",
      "@type": "rdfs:Class",
      "rdfs:label": {"@value": "工单", "@language": "zh"},
      "cim:properties": [
        {"@id": "cim-ops:workOrderId", "rdfs:range": "xsd:string"},
        {"@id": "cim-ops:workOrderType", "rdfs:range": "cim-ops:WorkOrderType"},
        {"@id": "cim-ops:priority", "rdfs:range": "xsd:integer"},
        {"@id": "cim-ops:status", "rdfs:range": "cim-ops:WorkOrderStatus"},
        {"@id": "cim-ops:targetEquipment", "rdfs:range": "cim-equip:Equipment"},
        {"@id": "cim-ops:createdAt", "rdfs:range": "xsd:dateTime"},
        {"@id": "cim-ops:dueDate", "rdfs:range": "xsd:dateTime"},
        {"@id": "cim-ops:completedAt", "rdfs:range": "xsd:dateTime"},
        {"@id": "cim-ops:assignedTo", "rdfs:range": "xsd:string"},
        {"@id": "cim-ops:laborHours", "rdfs:range": "xsd:decimal"},
        {"@id": "cim-ops:materialsCost", "rdfs:range": "xsd:decimal"}
      ]
    },

    {
      "@id": "cim-ops:WorkOrderType",
      "@type": "rdfs:Class",
      "owl:oneOf": [
        {"@id": "cim-ops:CORRECTIVE", "rdfs:label": "报修工单", "rdfs:comment": "故障后维修"},
        {"@id": "cim-ops:PREVENTIVE", "rdfs:label": "预防性维护工单", "rdfs:comment": "计划性维护"},
        {"@id": "cim-ops:PREDICTIVE", "rdfs:label": "预测性维护工单", "rdfs:comment": "基于状态预测"},
        {"@id": "cim-ops:INSPECTION", "rdfs:label": "巡检工单"},
        {"@id": "cim-ops:PROJECT", "rdfs:label": "项目工单", "rdfs:comment": "改造或升级"}
      ]
    },

    {
      "@id": "cim-ops:WorkOrderStatus",
      "@type": "rdfs:Class",
      "owl:oneOf": [
        {"@id": "cim-ops:WO_CREATED", "rdfs:label": "已创建"},
        {"@id": "cim-ops:WO_ASSIGNED", "rdfs:label": "已派单"},
        {"@id": "cim-ops:WO_IN_PROGRESS", "rdfs:label": "处理中"},
        {"@id": "cim-ops:WO_PENDING", "rdfs:label": "待料/待件"},
        {"@id": "cim-ops:WO_COMPLETED", "rdfs:label": "已完成"},
        {"@id": "cim-ops:WO_VERIFIED", "rdfs:label": "已验收"},
        {"@id": "cim-ops:WO_CLOSED", "rdfs:label": "已关闭"}
      ]
    },

    {
      "@id": "cim-ops:━━━━━ 资产生命周期 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-ops:AssetLifecycleStage",
      "@type": "rdfs:Class",
      "rdfs:label": {"@value": "资产生命周期阶段", "@language": "zh"},
      "owl:oneOf": [
        {"@id": "cim-ops:PROCUREMENT", "rdfs:label": "采购阶段", "cim:order": 1},
        {"@id": "cim-ops:INSTALLATION", "rdfs:label": "安装阶段", "cim:order": 2},
        {"@id": "cim-ops:COMMISSIONING", "rdfs:label": "调试阶段", "cim:order": 3},
        {"@id": "cim-ops:OPERATION", "rdfs:label": "运行阶段", "cim:order": 4},
        {"@id": "cim-ops:MAINTENANCE", "rdfs:label": "维护阶段", "cim:order": 5},
        {"@id": "cim-ops:UPGRADE", "rdfs:label": "升级阶段", "cim:order": 6},
        {"@id": "cim-ops:DECOMMISSION", "rdfs:label": "退役阶段", "cim:order": 7},
        {"@id": "cim-ops:DISPOSAL", "rdfs:label": "报废阶段", "cim:order": 8}
      ]
    },

    {
      "@id": "cim-ops:━━━━━ KPI指标 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-ops:MaintenanceKPI",
      "@type": "rdfs:Class",
      "rdfs:label": {"@value": "维护KPI", "@language": "zh"}
    },

    {
      "@id": "cim-ops:MTBF",
      "@type": "cim-ops:MaintenanceKPI",
      "rdfs:label": {"@value": "平均无故障时间", "@language": "zh"},
      "cim:formula": "MTBF = Total Operating Time / Number of Failures",
      "qudt:unit": "unit:HR"
    },

    {
      "@id": "cim-ops:MTTR",
      "@type": "cim-ops:MaintenanceKPI",
      "rdfs:label": {"@value": "平均修复时间", "@language": "zh"},
      "cim:formula": "MTTR = Total Repair Time / Number of Repairs",
      "qudt:unit": "unit:HR"
    },

    {
      "@id": "cim-ops:Availability",
      "@type": "cim-ops:MaintenanceKPI",
      "rdfs:label": {"@value": "可用率", "@language": "zh"},
      "cim:formula": "Availability = MTBF / (MTBF + MTTR)",
      "qudt:unit": "unit:PERCENT"
    },

    {
      "@id": "cim-ops:PMCompliance",
      "@type": "cim-ops:MaintenanceKPI",
      "rdfs:label": {"@value": "预防性维护完成率", "@language": "zh"},
      "cim:formula": "PM Compliance = Completed PM Work Orders / Scheduled PM Work Orders",
      "qudt:unit": "unit:PERCENT"
    },

    {
      "@id": "cim-ops:━━━━━ 维护关系 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-ops:hasWorkOrder",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "关联工单", "@language": "zh"},
      "rdfs:domain": "cim-equip:Equipment",
      "rdfs:range": "cim-ops:WorkOrder"
    },

    {
      "@id": "cim-ops:maintainedBy",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "维护方", "@language": "zh"},
      "rdfs:domain": "cim-equip:Equipment",
      "rdfs:range": "schema:Organization"
    },

    {
      "@id": "cim-ops:triggeredBy",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "触发来源", "@language": "zh"},
      "rdfs:domain": "cim-ops:WorkOrder",
      "rdfs:range": "cim-ops:Alarm"
    },

    {
      "@id": "cim-ops:hasMaintenanceSchedule",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "维护计划", "@language": "zh"},
      "rdfs:domain": "cim-equip:Equipment",
      "rdfs:range": "xsd:string"
    }
  ]
}
```

---

# **PHASE-5: 验证本体层**

## **Module-5.1: 验证问题本体**

### **文件: `ontology/validation_ontology.jsonld`**

```json
{
  "@context": ["ontology/namespaces.jsonld"],
  "@graph": [
    {
      "@id": "cim-valid:ValidationOntology",
      "@type": "owl:Ontology",
      "owl:versionInfo": "3.0.0",
      "dcterms:title": "CIM验证本体",
      "cim:sourceAgent": "Agent-09"
    },

    {
      "@id": "cim-valid:━━━━━ 验证问题分类 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-valid:ValidationIssue",
      "@type": "rdfs:Class",
      "rdfs:label": {"@value": "验证问题", "@language": "zh"},
      "rdfs:comment": "CIM模型验证过程中发现的结构或语义问题",
      "cim:properties": [
        {"@id": "cim-valid:issueCode", "rdfs:range": "xsd:string"},
        {"@id": "cim-valid:severity", "rdfs:range": "cim-valid:IssueSeverity"},
        {"@id": "cim-valid:title", "rdfs:range": "xsd:string"},
        {"@id": "cim-valid:description", "rdfs:range": "xsd:string"},
        {"@id": "cim-valid:affectsNode", "rdfs:range": ["cim-equip:Equipment", "cim-space:Space", "cim-system:System"]},
        {"@id": "cim-valid:detectedDate", "rdfs:range": "xsd:dateTime"},
        {"@id": "cim-valid:detectedBy", "rdfs:range": "xsd:string"},
        {"@id": "cim-valid:suggestedFix", "rdfs:range": "xsd:string"},
        {"@id": "cim-valid:estimatedCost", "qudt:unit": "unit:CNY"},
        {"@id": "cim-valid:status", "rdfs:range": "cim-valid:IssueStatus"}
      ]
    },

    {
      "@id": "cim-valid:IssueSeverity",
      "@type": "rdfs:Class",
      "owl:oneOf": [
        {
          "@id": "cim-valid:CRITICAL",
          "rdfs:label": {"@value": "严重", "@language": "zh"},
          "cim:priority": 1,
          "rdfs:comment": "影响系统安全运行或合规性的关键问题，需立即处理"
        },
        {
          "@id": "cim-valid:HIGH",
          "rdfs:label": {"@value": "高", "@language": "zh"},
          "cim:priority": 2,
          "rdfs:comment": "影响系统性能或可靠性的重要问题，需短期处理"
        },
        {
          "@id": "cim-valid:MEDIUM",
          "rdfs:label": {"@value": "中", "@language": "zh"},
          "cim:priority": 3,
          "rdfs:comment": "影响运营效率或维护成本的问题，需中期处理"
        },
        {
          "@id": "cim-valid:LOW",
          "rdfs:label": {"@value": "低", "@language": "zh"},
          "cim:priority": 4,
          "rdfs:comment": "轻微问题或优化建议，可长期规划"
        }
      ]
    },

    {
      "@id": "cim-valid:IssueStatus",
      "@type": "rdfs:Class",
      "owl:oneOf": [
        {"@id": "cim-valid:OPEN", "rdfs:label": "待处理"},
        {"@id": "cim-valid:IN_PROGRESS", "rdfs:label": "处理中"},
        {"@id": "cim-valid:RESOLVED", "rdfs:label": "已解决"},
        {"@id": "cim-valid:CLOSED", "rdfs:label": "已关闭"},
        {"@id": "cim-valid:WONT_FIX", "rdfs:label": "不修复"}
      ]
    },

    {
      "@id": "cim-valid:━━━━━ 问题类型分类 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-valid:StructuralIssue",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-valid:ValidationIssue",
      "rdfs:label": {"@value": "结构问题", "@language": "zh"},
      "cim:issueCodePrefix": "STR"
    },

    {
      "@id": "cim-valid:OrphanNodeIssue",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-valid:StructuralIssue",
      "rdfs:label": {"@value": "孤立节点", "@language": "zh"},
      "cim:issueCode": "STR-001"
    },

    {
      "@id": "cim-valid:DanglingReferenceIssue",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-valid:StructuralIssue",
      "rdfs:label": {"@value": "悬空引用", "@language": "zh"},
      "cim:issueCode": "STR-002"
    },

    {
      "@id": "cim-valid:CircularReferenceIssue",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-valid:StructuralIssue",
      "rdfs:label": {"@value": "循环引用", "@language": "zh"},
      "cim:issueCode": "STR-003"
    },

    {
      "@id": "cim-valid:SemanticIssue",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-valid:ValidationIssue",
      "rdfs:label": {"@value": "语义问题", "@language": "zh"},
      "cim:issueCodePrefix": "SEM"
    },

    {
      "@id": "cim-valid:MissingRequiredPropertyIssue",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-valid:SemanticIssue",
      "rdfs:label": {"@value": "缺失必要属性", "@language": "zh"},
      "cim:issueCode": "SEM-001"
    },

    {
      "@id": "cim-valid:MissingRequiredEquipmentIssue",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-valid:SemanticIssue",
      "rdfs:label": {"@value": "缺失必要设备", "@language": "zh"},
      "cim:issueCode": "SEM-002"
    },

    {
      "@id": "cim-valid:CapacityOverloadIssue",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-valid:SemanticIssue",
      "rdfs:label": {"@value": "容量超载", "@language": "zh"},
      "cim:issueCode": "SEM-003"
    },

    {
      "@id": "cim-valid:RedundancyDeficiencyIssue",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-valid:SemanticIssue",
      "rdfs:label": {"@value": "冗余不足", "@language": "zh"},
      "cim:issueCode": "SEM-004"
    },

    {
      "@id": "cim-valid:ConservationViolationIssue",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-valid:SemanticIssue",
      "rdfs:label": {"@value": "守恒违规", "@language": "zh"},
      "cim:issueCode": "SEM-005"
    },

    {
      "@id": "cim-valid:ComplianceIssue",
      "@type": "rdfs:Class",
      "rdfs:subClassOf": "cim-valid:ValidationIssue",
      "rdfs:label": {"@value": "合规问题", "@language": "zh"},
      "cim:issueCodePrefix": "COM"
    },

    {
      "@id": "cim-valid:━━━━━ 验证规则 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-valid:ValidationRule",
      "@type": "rdfs:Class",
      "rdfs:label": {"@value": "验证规则", "@language": "zh"},
      "cim:properties": [
        {"@id": "cim-valid:ruleId", "rdfs:range": "xsd:string"},
        {"@id": "cim-valid:ruleName", "rdfs:range": "xsd:string"},
        {"@id": "cim-valid:ruleCategory", "rdfs:range": "xsd:string"},
        {"@id": "cim-valid:appliesTo", "rdfs:range": "rdfs:Class"},
        {"@id": "cim-valid:condition", "rdfs:range": "xsd:string"},
        {"@id": "cim-valid:severityIfFailed", "rdfs:range": "cim-valid:IssueSeverity"}
      ]
    },

    {
      "@id": "cim-valid:SurgeryRoomEquipmentRule",
      "@type": "cim-valid:ValidationRule",
      "cim-valid:ruleId": "RULE-SUR-001",
      "cim-valid:ruleName": "手术室必要设备检查",
      "cim-valid:appliesTo": "cim-space:SurgeryRoom",
      "cim-valid:condition": "MUST have UPS AND O2 outlet AND VAC outlet AND N2O outlet (for GA)",
      "cim-valid:severityIfFailed": "cim-valid:CRITICAL"
    },

    {
      "@id": "cim-valid:PanelLoadRule",
      "@type": "cim-valid:ValidationRule",
      "cim-valid:ruleId": "RULE-ELEC-001",
      "cim-valid:ruleName": "配电箱负载检查",
      "cim-valid:appliesTo": "cim-equip:DistributionPanel",
      "cim-valid:condition": "currentLoad <= ratedCapacity * 0.8",
      "cim-valid:severityIfFailed": "cim-valid:HIGH"
    },

    {
      "@id": "cim-valid:ChillerRedundancyRule",
      "@type": "cim-valid:ValidationRule",
      "cim-valid:ruleId": "RULE-HVAC-001",
      "cim-valid:ruleName": "冷水机组N+1冗余检查",
      "cim-valid:appliesTo": "cim-system:ChilledWaterPlant",
      "cim-valid:condition": "N_chillers >= ceil(peak_load / single_capacity) + 1",
      "cim-valid:severityIfFailed": "cim-valid:MEDIUM"
    },

    {
      "@id": "cim-valid:━━━━━ 问题关系 ━━━━━",
      "@type": "rdfs:Comment"
    },

    {
      "@id": "cim-valid:hasIssue",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "存在问题", "@language": "zh"},
      "rdfs:domain": ["cim-equip:Equipment", "cim-space:Space", "cim-system:System"],
      "rdfs:range": "cim-valid:ValidationIssue",
      "owl:inverseOf": "cim-valid:affectsNode"
    },

    {
      "@id": "cim-valid:causedBy",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "由...引起", "@language": "zh"},
      "rdfs:domain": "cim-valid:ValidationIssue",
      "rdfs:range": "cim-valid:ValidationIssue"
    },

    {
      "@id": "cim-valid:relatedTo",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "关联问题", "@language": "zh"},
      "rdfs:domain": "cim-valid:ValidationIssue",
      "rdfs:range": "cim-valid:ValidationIssue",
      "@type": "owl:SymmetricProperty"
    }
  ]
}
```

---

## **Module-5.2: 守恒规则本体**

### **文件: `ontology/conservation_rules.jsonld`**

```json
{
"@context": ["ontology/namespaces.jsonld"],
"@graph": [
 {
 "@id": "cim-valid:ConservationRulesOntology",
 "@type": "owl:Ontology",
 "owl:versionInfo": "3.0.0",
 "dcterms:title": "守恒规则本体"
 },

 {
 "@id": "cim-valid:ConservationRule",
 "@type": "rdfs:Class",
 "rdfs:label": {"@value": "守恒规则", "@language": "zh"},
 "rdfs:comment": "用于验证模型物理一致性的守恒方程"
 },

 {
 "@id": "cim-valid:MassConservationRule",
 "@type": "cim-valid:ConservationRule",
 "rdfs:label": {"@value": "质量守恒规则", "@language": "zh"},
 "cim:equation": "Σṁ_in = Σṁ_out",
 "cim:appliesTo": ["cim-flow:WaterFlow", "cim-flow:AirFlow", "cim-flow:MedicalGasFlow"],
 "cim:tolerancePercent": 0.5,
 "cim:checkPoints": ["Junction", "Splitter", "HeatExchanger"]
 },

 {
 "@id": "cim-valid:EnergyConservationRule",
 "@type": "cim-valid:ConservationRule",
 "rdfs:label": {"@value": "能量守恒规则", "@language": "zh"},
 "cim:equation": "Q_in = Q_out + Q_loss",
 "cim:appliesTo": ["cim-flow:ThermalEnergyFlow"],
 "cim:tolerancePercent": 5.0,
 "cim:checkPoints": ["Chiller", "Boiler", "HeatExchanger", "AHU"]
 },

 {
 "@id": "cim-valid:PowerBalanceRule",
 "@type": "cim-valid:ConservationRule",

---