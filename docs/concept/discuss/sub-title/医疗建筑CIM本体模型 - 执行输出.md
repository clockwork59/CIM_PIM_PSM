## 🧑‍💻 User


你来执行上述命令的本体建模部分，你需要事先阅读和分析的知识库文档，然后开始相应的建模输出

---
## 🤖 Assistant

<div style="border: 2px solid #dddddd; border-radius: 10px;">
  <details style="padding: 5px;">
    <summary>已深度思考</summary>
    用户要求我执行上述命令的本体建模部分，这意味着我需要：<br>1. 首先分析提供的知识库文档（从之前的上下文中理解需求）<br>2. 然后生成详细的本体定义文件，不能只是简单的脚本，而是实际执行建模<br>3. 输出应该是可直接使用的JSON-LD格式的本体文件<br><br>让我分析用户的要求：<br>- "你来执行上述命令的本体建模部分" - 这意味着我需要真正生成本体，而不是写脚本<br>- "你需要事先阅读和分析的知识库文档" - 我需要回顾之前的对话，理解医疗建筑CIM模型的具体需求<br>- "然后开始相应的建模输出" - 输出应该是完整的、可直接使用的本体定义<br><br>从之前的对话中，我理解到：<br>1. 这是医疗建筑的数字孪生CIM模型<br>2. 需要集成8个Agent的数据<br>3. 本体需要覆盖：空间、设备、系统、传感器、医疗气体、消防、电气等<br>4. 需要继承和扩展Schema.org、BrickSchema、Haystack<br>5. 需要包含验证问题的定义<br><br>所以我应该直接生成完整的JSON-LD本体文件内容，而不是生成创建文件的脚本。用户想要的是"执行"结果。<br><br>让我构建一个全面、专业的医疗建筑CIM本体，包含：<br>- 完整的@context定义，引用标准本体<br>- 详细的类层次结构（空间、设备、系统、传感器、问题等）<br>- 完整的属性定义（关系类型）<br>- 医疗特定的概念（手术室、ICU、医疗气体等）<br>- 验证问题的分类<br>- 使用适当的RDF/OWL术语<br><br>我需要确保：<br>1. 所有类都有适当的rdfs:subClassOf关系<br>2. 属性有正确的定义域和值域<br>3. 医疗特定属性被明确定义<br>4. 包含单位和量纲的引用<br>5. 结构清晰，易于扩展
  </details>
</div>

# **医疗建筑CIM本体模型 - 执行输出**

基于对医疗建筑数字孪生需求的深度分析，我已完整执行本体建模任务。以下是可直接使用的JSON-LD格式本体定义文件：

---

## **文件: `ontology/cim_medical_ontology.jsonld`**

```json
{
"@context": {
 "@version": 1.1,
 "cim": "https://cim.medical/ontology/v1.0#",
 "brick": "https://brickschema.org/schema/Brick#",
 "schema": "https://schema.org/",
 "haystack": "https://project-haystack.org/def/phIoT/3.9.10#",
 "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
 "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
 "owl": "http://www.w3.org/2002/07/owl#",
 "xsd": "http://www.w3.org/2001/XMLSchema#",
 "dcterms": "http://purl.org/dc/terms/",
 "qudt": "http://qudt.org/schema/qudt/",
 "unit": "http://qudt.org/vocab/unit/",
 "sh": "http://www.w3.org/ns/shacl#",
 "skos": "http://www.w3.org/2004/02/skos/core#"
},
"@graph": [
 {
 "@id": "cim:MedicalBuildingOntology",
 "@type": "owl:Ontology",
 "owl:versionInfo": "1.0.0",
 "dcterms:title": "医疗建筑CIM数字孪生本体",
 "dcterms:description": "面向医疗建筑综合运营管理的数字孪生知识图谱本体，集成空间、设备、系统、业务多维度信息",
 "dcterms:created": "2025-01-15T08:00:00Z",
 "dcterms:creator": "Agent-09 CIM Integration System",
 "dcterms:modified": "2025-01-15T12:30:00Z",
 "owl:imports": [
 "https://brickschema.org/schema/Brick",
 "https://schema.org/",
 "https://project-haystack.org/def/phIoT/3.9.10"
 ]
 },

 {
 "@id": "cim:Space",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": ["brick:Location", "schema:Place"],
 "rdfs:label": {"en": "Space", "zh": "空间"},
 "rdfs:comment": "医疗建筑物理空间基类，表示具有明确边界的区域",
 "skos:definition": "所有建筑空间的抽象基类，包含几何、物理和环境属性"
 },
 {
 "@id": "cim:Building",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Space",
 "rdfs:label": {"en": "Building", "zh": "建筑"},
 "cim:hasProperty": ["cim:grossFloorArea", "cim:totalFloors", "cim:yearBuilt", "cim:buildingClass"]
 },
 {
 "@id": "cim:Floor",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Space",
 "rdfs:label": {"en": "Floor", "zh": "楼层"},
 "cim:level": {"@type": "xsd:integer", "rdfs:comment": "楼层编号，负数为地下层"}
 },
 {
 "@id": "cim:Zone",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Space",
 "rdfs:label": {"en": "Zone", "zh": "功能分区"},
 "rdfs:comment": "具有特定功能的空间集合，如手术区、住院区等"
 },
 {
 "@id": "cim:Room",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Space",
 "rdfs:label": {"en": "Room", "zh": "房间"},
 "cim:hasProperty": ["cim:roomCode", "cim:floorArea", "cim:isPartOf"]
 },
 {
 "@id": "cim:SurgeryRoom",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Room",
 "rdfs:label": {"en": "Surgery Room", "zh": "手术室"},
 "cim:cleanlinessClass": {"@type": "xsd:string", "rdfs:comment": "洁净等级：ISO-5/6/7/8"},
 "cim:pressureDifferential": {"qudt:unit": "unit:PA", "@type": "xsd:decimal"},
 "cim:minAirChanges": {"@type": "xsd:integer", "rdfs:comment": "最小换气次数(次/h)"},
 "cim:requiredMedicalGases": {"@type": "xsd:array", "rdfs:comment": "所需医疗气体类型"},
 "cim:requiredPowerBackup": {"@type": "xsd:boolean"},
 "cim:temperatureSetpoint": {"qudt:unit": "unit:DEG_C", "@type": "xsd:decimal"},
 "cim:humiditySetpoint": {"qudt:unit": "unit:PERCENT", "@type": "xsd:decimal"}
 },
 {
 "@id": "cim:ICU",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Room",
 "rdfs:label": {"en": "ICU", "zh": "重症监护室"},
 "cim:bedCount": {"@type": "xsd:integer"},
 "cim:isolationType": {"@type": "xsd:string", "rdfs:comment": "隔离类型：负压/正压/标准"},
 "cim:hasPatientMonitor": {"@type": "xsd:boolean"},
 "cim:hasVentilatorSupport": {"@type": "xsd:boolean"}
 },
 {
 "@id": "cim:EmergencyRoom",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Room",
 "rdfs:label": {"en": "Emergency Room", "zh": "急诊室"},
 "cim:triageLevel": {"@type": "xsd:integer", "rdfs:comment": "分诊等级"}
 },
 {
 "@id": "cim:PharmacyRoom",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Room",
 "rdfs:label": {"en": "Pharmacy", "zh": "药房"},
 "cim:drugStorageClass": {"@type": "xsd:string", "rdfs:comment": "药品储存等级"}
 },
 {
 "@id": "cim:LaboratoryRoom",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Room",
 "rdfs:label": {"en": "Laboratory", "zh": "检验室"},
 "cim:bioSafetyLevel": {"@type": "xsd:integer", "rdfs:comment": "生物安全等级BSL"}
 },
 {
 "@id": "cim:ImagingRoom",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Room",
 "rdfs:label": {"en": "Imaging Room", "zh": "影像室"},
 "cim:modalityType": {"@type": "xsd:string", "rdfs:comment": "设备类型：CT/MRI/X光"}
 },
 {
 "@id": "cim:MechanicalRoom",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Room",
 "rdfs:label": {"en": "Mechanical Room", "zh": "设备机房"},
 "rdfs:comment": "安置暖通、给排水等设备的专用空间"
 },
 {
 "@id": "cim:ElectricalRoom",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Room",
 "rdfs:label": {"en": "Electrical Room", "zh": "电气机房"}
 },
 {
 "@id": "cim:FirePumpRoom",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Room",
 "rdfs:label": {"en": "Fire Pump Room", "zh": "消防泵房"},
 "cim:hasFireRating": {"@type": "xsd:integer", "rdfs:comment": "防火等级（小时）"}
 },

 {
 "@id": "cim:Equipment",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": ["brick:Equipment", "schema:Product"],
 "rdfs:label": {"en": "Equipment", "zh": "设备"},
 "rdfs:comment": "医疗建筑机电设备的抽象基类",
 "cim:hasProperty": ["cim:equipmentCode", "cim:locatedIn", "cim:manufacturer", "cim:installDate"]
 },
 {
 "@id": "cim:HVACEquipment",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Equipment",
 "rdfs:label": {"en": "HVAC Equipment", "zh": "暖通设备"}
 },
 {
 "@id": "cim:AirHandlingUnit",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:HVACEquipment",
 "rdfs:label": {"en": "Air Handling Unit", "zh": "空调箱"},
 "cim:ratedAirflow": {"qudt:unit": "unit:M3-PER-HR", "@type": "xsd:decimal"},
 "cim:supplyFanPower": {"qudt:unit": "unit:KiloW", "@type": "xsd:decimal"},
 "cim:returnFanPower": {"qudt:unit": "unit:KiloW", "@type": "xsd:decimal"},
 "cim:coolingCoilCapacity": {"qudt:unit": "unit:KiloW", "@type": "xsd:decimal"},
 "cim:heatingCoilCapacity": {"qudt:unit": "unit:KiloW", "@type": "xsd:decimal"},
 "cim:filterEfficiency": {"@type": "xsd:string"},
 "cim:hasEnergyRecovery": {"@type": "xsd:boolean"}
 },
 {
 "@id": "cim:Chiller",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:HVACEquipment",
 "rdfs:label": {"en": "Chiller", "zh": "冷水机组"},
 "cim:ratedCapacity": {"qudt:unit": "unit:KiloW", "@type": "xsd:decimal"},
 "cim:ratedPower": {"qudt:unit": "unit:KiloW", "@type": "xsd:decimal"},
 "cim:refrigerantType": {"@type": "xsd:string"},
 "cim:chilledWaterFlowRate": {"qudt:unit": "unit:L-PER-MIN", "@type": "xsd:decimal"},
 "cim:cop": {"@type": "xsd:decimal", "rdfs:comment": "性能系数"}
 },
 {
 "@id": "cim:CoolingTower",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:HVACEquipment",
 "rdfs:label": {"en": "Cooling Tower", "zh": "冷却塔"},
 "cim:ratedCapacity": {"qudt:unit": "unit:KiloW", "@type": "xsd:decimal"},
 "cim:ratedFlow": {"qudt:unit": "unit:M3-PER-HR", "@type": "xsd:decimal"},
 "cim:approachTemperature": {"qudt:unit": "unit:K", "@type": "xsd:decimal"}
 },
 {
 "@id": "cim:Boiler",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:HVACEquipment",
 "rdfs:label": {"en": "Boiler", "zh": "锅炉"},
 "cim:fuelType": {"@type": "xsd:string", "rdfs:comment": "燃料类型：燃气/燃油/电"}
 },
 {
 "@id": "cim:HeatExchanger",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:HVACEquipment",
 "rdfs:label": {"en": "Heat Exchanger", "zh": "换热器"}
 },
 {
 "@id": "cim:Fan",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:HVACEquipment",
 "rdfs:label": {"en": "Fan", "zh": "风机"}
 },
 {
 "@id": "cim:Pump",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:HVACEquipment",
 "rdfs:label": {"en": "Pump", "zh": "水泵"}
 },
 {
 "@id": "cim:VAVBox",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:HVACEquipment",
 "rdfs:label": {"en": "VAV Box", "zh": "变风量末端"},
 "cim:minAirflow": {"qudt:unit": "unit:M3-PER-HR", "@type": "xsd:decimal"},
 "cim:maxAirflow": {"qudt:unit": "unit:M3-PER-HR", "@type": "xsd:decimal"},
 "cim:hasReheatCoil": {"@type": "xsd:boolean"}
 },
 {
 "@id": "cim:FCU",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:HVACEquipment",
 "rdfs:label": {"en": "Fan Coil Unit", "zh": "风机盘管"}
 },

 {
 "@id": "cim:ElectricalEquipment",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Equipment",
 "rdfs:label": {"en": "Electrical Equipment", "zh": "电气设备"}
 },
 {
 "@id": "cim:Transformer",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:ElectricalEquipment",
 "rdfs:label": {"en": "Transformer", "zh": "变压器"},
 "cim:ratedCapacity": {"qudt:unit": "unit:KiloV-A", "@type": "xsd:decimal"},
 "cim:primaryVoltage": {"qudt:unit": "unit:KiloV", "@type": "xsd:decimal"},
 "cim:secondaryVoltage": {"qudt:unit": "unit:KiloV", "@type": "xsd:decimal"},
 "cim:coolingType": {"@type": "xsd:string"}
 },
 {
 "@id": "cim:Switchgear",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:ElectricalEquipment",
 "rdfs:label": {"en": "Switchgear", "zh": "开关柜"}
 },
 {
 "@id": "cim:DistributionPanel",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:ElectricalEquipment",
 "rdfs:label": {"en": "Distribution Panel", "zh": "配电箱"},
 "cim:panelType": {"@type": "xsd:string", "rdfs:comment": "类型：Normal/Emergency/Critical"},
 "cim:ratedCurrent": {"qudt:unit": "unit:A", "@type": "xsd:decimal"},
 "cim:circuitCount": {"@type": "xsd:integer"},
 "cim:currentLoad": {"qudt:unit": "unit:KiloW", "@type": "xsd:decimal"},
 "cim:loadFactor": {"@type": "xsd:decimal"}
 },
 {
 "@id": "cim:UPS",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:ElectricalEquipment",
 "rdfs:label": {"en": "UPS", "zh": "不间断电源"},
 "cim:ratedCapacity": {"qudt:unit": "unit:KiloV-A", "@type": "xsd:decimal"},
 "cim:batteryRuntime": {"qudt:unit": "unit:MIN", "@type": "xsd:decimal"},
 "cim:batteryType": {"@type": "xsd:string"},
 "cim:efficiency": {"@type": "xsd:decimal"}
 },
 {
 "@id": "cim:EmergencyGenerator",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:ElectricalEquipment",
 "rdfs:label": {"en": "Emergency Generator", "zh": "应急发电机"},
 "cim:ratedCapacity": {"qudt:unit": "unit:KiloW", "@type": "xsd:decimal"},
 "cim:fuelType": {"@type": "xsd:string"},
 "cim:fuelTankCapacity": {"qudt:unit": "unit:L", "@type": "xsd:decimal"},
 "cim:startupTime": {"qudt:unit": "unit:SEC", "@type": "xsd:decimal"}
 },
 {
 "@id": "cim:ATS",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:ElectricalEquipment",
 "rdfs:label": {"en": "Automatic Transfer Switch", "zh": "自动转换开关"},
 "cim:switchoverTime": {"qudt:unit": "unit:SEC", "@type": "xsd:decimal"}
 },

 {
 "@id": "cim:PlumbingEquipment",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Equipment",
 "rdfs:label": {"en": "Plumbing Equipment", "zh": "给排水设备"}
 },
 {
 "@id": "cim:WaterTank",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:PlumbingEquipment",
 "rdfs:label": {"en": "Water Tank", "zh": "水箱"},
 "cim:tankCapacity": {"qudt:unit": "unit:M3", "@type": "xsd:decimal"},
 "cim:isPotable": {"@type": "xsd:boolean"}
 },
 {
 "@id": "cim:WaterHeater",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:PlumbingEquipment",
 "rdfs:label": {"en": "Water Heater", "zh": "热水器"}
 },
 {
 "@id": "cim:SewagePump",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:PlumbingEquipment",
 "rdfs:label": {"en": "Sewage Pump", "zh": "污水泵"}
 },

 {
 "@id": "cim:MedicalGasEquipment",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Equipment",
 "rdfs:label": {"en": "Medical Gas Equipment", "zh": "医疗气体设备"},
 "rdfs:comment": "供应医用气体（氧气、笑气、负压等）的专业设备"
 },
 {
 "@id": "cim:OxygenManifold",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:MedicalGasEquipment",
 "rdfs:label": {"en": "Oxygen Manifold", "zh": "氧气汇流排"},
 "cim:cylinderCount": {"@type": "xsd:integer"},
 "cim:outletPressure": {"qudt:unit": "unit:KiloPA", "@type": "xsd:decimal"},
 "cim:flowCapacity": {"qudt:unit": "unit:L-PER-MIN", "@type": "xsd:decimal"}
 },
 {
 "@id": "cim:VacuumPump",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:MedicalGasEquipment",
 "rdfs:label": {"en": "Vacuum Pump", "zh": "真空泵"},
 "cim:ratedVacuum": {"qudt:unit": "unit:KiloPA", "@type": "xsd:decimal"},
 "cim:flowCapacity": {"qudt:unit": "unit:M3-PER-HR", "@type": "xsd:decimal"},
 "cim:motorPower": {"qudt:unit": "unit:KiloW", "@type": "xsd:decimal"}
 },
 {
 "@id": "cim:MedicalAirCompressor",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:MedicalGasEquipment",
 "rdfs:label": {"en": "Medical Air Compressor", "zh": "医用空压机"}
 },
 {
 "@id": "cim:N2OManifold",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:MedicalGasEquipment",
 "rdfs:label": {"en": "N2O Manifold", "zh": "笑气汇流排"}
 },

 {
 "@id": "cim:FireProtectionEquipment",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Equipment",
 "rdfs:label": {"en": "Fire Protection Equipment", "zh": "消防设备"}
 },
 {
 "@id": "cim:FirePump",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:FireProtectionEquipment",
 "rdfs:label": {"en": "Fire Pump", "zh": "消防泵"},
 "cim:pumpType": {"@type": "xsd:string"},
 "cim:ratedFlow": {"qudt:unit": "unit:L-PER-SEC", "@type": "xsd:decimal"},
 "cim:ratedHead": {"qudt:unit": "unit:M", "@type": "xsd:decimal"}
 },
 {
 "@id": "cim:SprinklerHead",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:FireProtectionEquipment",
 "rdfs:label": {"en": "Sprinkler Head", "zh": "喷淋头"},
 "cim:KFactor": {"qudt:unit": "unit:L-PER-MIN-PER-BAR-ROOT", "@type": "xsd:decimal"},
 "cim:responseTimeIndex": {"qudt:unit": "unit:M-S-ROOT", "@type": "xsd:decimal"}
 },
 {
 "@id": "cim:FireAlarmPanel",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:FireProtectionEquipment",
 "rdfs:label": {"en": "Fire Alarm Panel", "zh": "火灾报警控制器"}
 },
 {
 "@id": "cim:SmokeDetector",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:FireProtectionEquipment",
 "rdfs:label": {"en": "Smoke Detector", "zh": "烟感探测器"}
 },

 {
 "@id": "cim:Sensor",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "brick:Sensor",
 "rdfs:label": {"en": "Sensor", "zh": "传感器"},
 "cim:measurementType": {"@type": "xsd:string"},
 "cim:accuracy": {"@type": "xsd:string"},
 "cim:protocol": {"@type": "xsd:string", "rdfs:comment": "通信协议：BACnet/Modbus/LON"},
 "cim:refreshInterval": {"qudt:unit": "unit:SEC", "@type": "xsd:integer"},
 "cim:monitors": {
 "@type": "rdf:Property",
 "rdfs:domain": "cim:Sensor",
 "rdfs:range": ["cim:Equipment", "cim:Space"]
 }
 },
 {
 "@id": "cim:TemperatureSensor",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Sensor",
 "rdfs:label": {"en": "Temperature Sensor", "zh": "温度传感器"},
 "cim:measurementRange": {"qudt:unit": "unit:DEG_C", "@type": "xsd:decimal"},
 "cim:measurementType": "Temperature"
 },
 {
 "@id": "cim:HumiditySensor",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Sensor",
 "rdfs:label": {"en": "Humidity Sensor", "zh": "湿度传感器"},
 "cim:measurementType": "RelativeHumidity"
 },
 {
 "@id": "cim:PressureSensor",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Sensor",
 "rdfs:label": {"en": "Pressure Sensor", "zh": "压力传感器"},
 "cim:measurementType": "Pressure"
 },
 {
 "@id": "cim:FlowSensor",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Sensor",
 "rdfs:label": {"en": "Flow Sensor", "zh": "流量传感器"},
 "cim:measurementType": "FlowRate"
 },
 {
 "@id": "cim:CO2Sensor",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Sensor",
 "rdfs:label": {"en": "CO2 Sensor", "zh": "二氧化碳传感器"},
 "cim:measurementType": "CO2Concentration"
 },
 {
 "@id": "cim:PM25Sensor",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Sensor",
 "rdfs:label": {"en": "PM2.5 Sensor", "zh": "PM2.5传感器"},
 "cim:measurementType": "PM2.5Concentration"
 },
 {
 "@id": "cim:OccupancySensor",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Sensor",
 "rdfs:label": {"en": "Occupancy Sensor", "zh": "人员存在传感器"},
 "cim:measurementType": "Occupancy"
 },
 {
 "@id": "cim:PowerMeter",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Sensor",
 "rdfs:label": {"en": "Power Meter", "zh": "电表"},
 "cim:measurementType": ["ActivePower", "ReactivePower", "Energy"],
 "cim:voltageRating": {"qudt:unit": "unit:V", "@type": "xsd:decimal"},
 "cim:currentRating": {"qudt:unit": "unit:A", "@type": "xsd:decimal"}
 },
 {
 "@id": "cim:WaterMeter",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Sensor",
 "rdfs:label": {"en": "Water Meter", "zh": "水表"},
 "cim:measurementType": "WaterFlow"
 },
 {
 "@id": "cim:GasMeter",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:Sensor",
 "rdfs:label": {"en": "Gas Meter", "zh": "气表"}
 },

 {
 "@id": "cim:System",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "brick:System",
 "rdfs:label": {"en": "System", "zh": "系统"},
 "rdfs:comment": "由多个设备组成的功能系统"
 },
 {
 "@id": "cim:HVACSystem",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:System",
 "rdfs:label": {"en": "HVAC System", "zh": "暖通系统"},
 "cim:designCapacity": {"qudt:unit": "unit:KiloW", "@type": "xsd:decimal"},
 "cim:operatingMode": {"@type": "xsd:string"},
 "cim:hasMember": {"@type": "rdf:Property", "rdfs:range": "cim:HVACEquipment"}
 },
 {
 "@id": "cim:ChilledWaterSystem",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:HVACSystem",
 "rdfs:label": {"en": "Chilled Water System", "zh": "冷冻水系统"},
 "cim:supplyTemperature": {"qudt:unit": "unit:DEG_C", "@type": "xsd:decimal"},
 "cim:returnTemperature": {"qudt:unit": "unit:DEG_C", "@type": "xsd:decimal"}
 },
 {
 "@id": "cim:HotWaterSystem",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:HVACSystem",
 "rdfs:label": {"en": "Hot Water System", "zh": "热水系统"}
 },
 {
 "@id": "cim:AirDistributionSystem",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:HVACSystem",
 "rdfs:label": {"en": "Air Distribution System", "zh": "空气分配系统"}
 },
 {
 "@id": "cim:ElectricalSystem",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:System",
 "rdfs:label": {"en": "Electrical System", "zh": "供配电系统"},
 "cim:voltage": {"qudt:unit": "unit:V", "@type": "xsd:decimal"},
 "cim:frequency": {"qudt:unit": "unit:HZ", "@type": "xsd:decimal"}
 },
 {
 "@id": "cim:NormalPowerSystem",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:ElectricalSystem",
 "rdfs:label": {"en": "Normal Power System", "zh": "正常电源系统"}
 },
 {
 "@id": "cim:EmergencyPowerSystem",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:ElectricalSystem",
 "rdfs:label": {"en": "Emergency Power System", "zh": "应急电源系统"},
 "cim:switchoverTime": {"qudt:unit": "unit:SEC", "@type": "xsd:decimal"}
 },
 {
 "@id": "cim:CriticalPowerSystem",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:ElectricalSystem",
 "rdfs:label": {"en": "Critical Power System", "zh": "关键电源系统"},
 "cim:switchoverTime": {"qudt:unit": "unit:SEC", "@type": "xsd:decimal"}
 },
 {
 "@id": "cim:PlumbingSystem",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:System",
 "rdfs:label": {"en": "Plumbing System", "zh": "给排水系统"}
 },
 {
 "@id": "cim:DomesticWaterSystem",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:PlumbingSystem",
 "rdfs:label": {"en": "Domestic Water System", "zh": "生活给水系统"}
 },
 {
 "@id": "cim:DrainageSystem",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:PlumbingSystem",
 "rdfs:label": {"en": "Drainage System", "zh": "排水系统"}
 },
 {
 "@id": "cim:MedicalGasSystem",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:System",
 "rdfs:label": {"en": "Medical Gas System", "zh": "医疗气体系统"},
 "cim:operatingPressure": {"qudt:unit": "unit:KiloPA", "@type": "xsd:decimal"},
 "cim:gasType": {"@type": "xsd:string"}
 },
 {
 "@id": "cim:OxygenSystem",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:MedicalGasSystem",
 "rdfs:label": {"en": "Oxygen System", "zh": "氧气系统"},
 "cim:gasType": "O2"
 },
 {
 "@id": "cim:VacuumSystem",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:MedicalGasSystem",
 "rdfs:label": {"en": "Vacuum System", "zh": "负压吸引系统"},
 "cim:gasType": "VACUUM",
 "cim:operatingVacuum": {"qudt:unit": "unit:KiloPA", "@type": "xsd:decimal"}
 },
 {
 "@id": "cim:MedicalAirSystem",
 "@type": "rdfs:Class",
 "rdfs:subClassOf": "cim:MedicalGasSystem",
 "rdfs:label": {"en": "Medical Air System", "zh": "医用压缩空气系统"},
 "cim:gasType": "MEDICAL_AIR"

---