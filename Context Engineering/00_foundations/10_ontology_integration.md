# 本体整合：CIM与行业标准

**文档 ID**: `CIMU-FOUND-10-INTEGRATION`
**版本**: v1.0
**最后更新**: 2025-12-07

---

## 概述

CIM（统一领域模型）不是孤立的标准，而是与现有行业标准（IFC、Brick、REC、ASHRAE）的整合与扩展。通过语义对齐和映射，CIM 吸收各标准的优势，形成医疗建筑领域的统一本体。

---

## 标准体系全景

```
                                               ┌──────────────┐
                                               │   CIM (顶层)  │
                                               │  医疗建筑统一  │
                                               └──────┬───────┘
                                                      │
        ┌───────────────┬───────────────┬──────────┼───────────┬──────────────┐
        │               │               │          │           │              │
┌───────▼──────┐ ┌─────▼───────┐ ┌─────▼──────┐ ┌──▼──────┐ ┌──▼──────┐ ┌──▼──────┐
│   IFC/BIM    │ │   Brick    │ │    REC     │ │ ASHRAE  │ │ SNOMED  │ │ SNOMED  │
│  (几何/建筑) │ │  (能耗/楼控)│ │  (物业/资产)│ │ (技术/标准)│ │ (临床流程) │ │ (医疗气体) │
└──────────────┘ └─────────────┘ └────────────┘ └─────────┘ └──────────┘ └──────────┘
```

---

## IFC 整合

### IFC 简介
- **全称**: Industry Foundation Classes (工业基础类)
- **组织**: buildingSMART International
- **目的**: 建筑信息模型（BIM）的行业标准数据格式
- **技术**: EXPRESS 数据建模、STEP 文件格式

### IFC 核心概念

**空间 (Spatial)**:
```
IfcSite → IfcBuilding → IfcBuildingStorey → IfcSpace
```

**设备 (Distribution)**:
```
IfcDistributionElement
├── IfcDistributionSystem
├── IfcDistributionCircuit
└── IfcDistributionFlowElement
    ├── IfcFlowSegment (管道、风管)
    ├── IfcFlowFitting (阀门、三通)
    └── IfcFlowTerminal (末端设备)
```

### IFC → CIM 映射

**空间映射**:
```yaml
IFC: IfcSpace
  - GlobalId: "2QRJSY$9L6oB7KJw4"
  - Name: "301"
  - LongName: "内科诊室-301"
  - ObjectType: "CONSULTING_ROOM"
  - NetFloorArea: 20 m²
  - Volume: 64 m³

CIM: Space
  - space_id: "BLDG01-L3-ROOM-301"
  - space_name: "内科诊室-301"
  - space_type: "MEDICAL_CONSULTING"
  - area_m2: 20
  - volume_m3: 64

映射关系:
  ifc_space_id: "2QRJSY$9L6oB7KJw4"  (IFC原始ID)
  ifc_building_storey: "3F"
  ifc_building: "BLDG-01"
```

**设备映射**:
```yaml
IFC: IfcPump
  - GlobalId: "1RkJZP$9L3nB4VWq9"
  - Name: "CHWP-3F-01"
  - PredefinedType: "CIRCULATOR"  (循环泵)
  - Pset_PumpOccurrence
    - FlowRate: 180 m³/h
    - Head: 32 m
    - Power: 22 kW

CIM: Equipment
  - equipment_id: "CHWP-3F-01"
  - equipment_type: "CHW_PUMP"
  - flow_rate_m3h: 180
  - head_m: 32
  - rated_power_kw: 22

映射关系:
  ifc_equipment_id: "1RkJZP$9L3nB4VWq9"
  ifc_system: "HVAC-CHW-P001"
```

### IFC 的局限性

1. **几何强，语义弱**: 擅长几何表达，但运行参数不足
2. **静态模型**: 缺少动态运行数据接口
3. **系统逻辑模糊**: 拓扑关系不够明确

### CIM 的价值

1. **补充运行参数**: COP、控制策略、维护周期
2. **明确系统关系**: contains、connected_to、serves
3. **动态数据集成**: 传感器数据、能耗数据
4. **计算能力**: 能效计算、故障诊断

---

## Brick Schema 整合

### Brick 简介
- **全称**: Building Reference Information Catalog and Knowledge (建筑信息目录与知识)
- **组织**: brickschema.org
- **技术**: RDF/OWL 本体，基于三元组
- **优势**: 强大的推理能力和语义表达

### Brick 核心概念

**空间 (Locations)**:
```turtle
brick:Building
brick:Floor
brick:Room
brick:Zone
```

**设备 (Equipment)**:
```turtle
brick:Equipment
brick:HVAC_Equipment
brick:Chiller
brick:Air_Handler_Unit
brick:Variable_Frequency_Drive
```

**点 (Points)**:
```turtle
brick:Point
brick:Temperature_Sensor
brick:Temperature_Setpoint
brick:Run_Status
```

### Brick → CIM 映射

**设备类型映射**:
```yaml
Brick: brick:Chiller
  - 继承自: brick:HVAC_Equipment
  - 特征: 冷源设备，蒸发器-冷凝器循环
  - 属性: capacity, cop, refrigerant_type

CIM: HVAC_Chiller
  - 继承自: HVAC_Equipment
  - 补充: medical_specialty, maintenance_cycle
  - 属性: rated_cooling_capacity, rated_power, cop

映射:
  brick_class: "brick:Chiller"
  cim_class: "HVAC_Chiller"
  bridge_properties:
    - brick:hasRefrigerant → cim:refrigerant_type
    - brick:coolingCapacity → cim:rated_cooling_capacity
    - brick:compressorType → 待补充 (CIM扩展)
```

**点类型映射**:
```yaml
Brick: brick:Supply_Air_Temperature_Sensor
  - 类型: brick:Temperature_Sensor
  - 关联: 测量 Supply_Air 温度

CIM: Sensor:SupplyAirTemperature
  - 类型: TEMPERATURE_SENSOR
  - 关联: monitors: TerminalUnit/AHU
  - 额外: unit: °C, accuracy: ±0.5°C

映射:
  brick_point_type: "brick:Supply_Air_Temperature_Sensor"
  cim_point_type: "AI-SA-TEMP"
  definition: "送风温度传感器"
```

### Brick 的优势与 CIM 的扩展

**Brick 优势**:
- 成熟的本体库 (1000+ 类)
- 强大的推理 (OWL-DL)
- 社区支持 (Stanford、JCI)

**CIM 扩展**:
- 医疗场景特殊设备 (洁净空调、医疗气体)
- 中国标准适配 (GB 规范)
- 运维管理集成 (维护、告警)

---

## REC 整合

### REC 简介
- **全称**: RealEstateCore (房地产核心)
- **组织**: RealEstateCore Consortium
- **技术**: DTDL (Digital Twins Definition Language)
- **优势**: 微软 Azure Digital Twins 原生支持

### REC 核心概念

**资产 (Assets)**:
```typescript
interface Asset {
  id: string;
  name: string;
  externalIds?: { [key: string]: string };
  assetType: AssetType;
  assetStatus: AssetStatus;
  locatedIn?: Space;
}
```

**空间 (Spaces)**:
```typescript
interface Space {
  id: string;
  name: string;
  spaceType: SpaceType;
  containedIn?: Building;
  areas: Area[];
}
```

### REC → CIM 映射

**资产关联**:
```yaml
REC: asset-001
  - id: "asset-chiller-001"
  - name: "冷水机组-001"
  - assetType: Chiller
  - externalIds:
      ifcId: "1RkJZP$9L3nB4VWq9"
      brickUri: "brick:Chiller:chiller-001"
  - locatedIn: building-01

CIM: Equipment
  - equipment_id: "CH-001"
  - equipment_name: "冷水机组-001"
  - external_ids:
      rec_asset_id: "asset-chiller-001"
      ifc_id: "1RkJZP$9L3nB4VWq9"
      brick_uri: "brick:Chiller:chiller-001"
  - located_in: "BLDG01-MECHROOM-01"
```

### 整合价值

1. **打通数字孪生平台**: CIM → Azure Digital Twins → 应用
2. **统一身份管理**: REC 的 externalIds 连接多标准
3. **时间序列数据**: 与 Azure Time Series Insights 集成

---

## ASHRAE 标准整合

### 设计标准

**ASHRAE 170: 医疗设施通风**
- 手术室换气次数: ≥20 ACH
- 洁净走廊正压: +2.5 Pa
- 室外空气量: 15 ACH or 3 ACH per person

**CIM 映射**:
```yaml
cim:OperatingRoom
  - 标准引用: ASHRAE 170-2021
  - ventilation_rate: 20 ACH
  - pressure_relationship: POSITIVE
  - pressure_value: 5 Pa
  - outdoor_air_rate: 15 ACH
```

### 控制标准

**ASHRAE Guideline 36: 高级控制序列**

提供标准化的 HVAC 控制序列，如：
- 送风温度重置
- 静压重置
- 经济器控制

**CIM 映射**:
```yaml
Sequence: Supply_Air_Temperature_Reset
  Source: "ASHRAEA Guideline 36-2021, Section 5.1"

CIM 控制逻辑:
  - name: SAT_Reset_Based_On_Zone_Demand
  - algorithm: "IF T_zone_max < T_setpoint - 1°C THEN
                 T_SAT_setpoint += 0.5°C (up to max 13°C)
               ELSE IF T_zone_min > T_setpoint + 1°C THEN
                 T_SAT_setpoint -= 0.5°C (down to min 10°C)"
```

### 设备标准

**ASHRAE Standard 90.1: 建筑能效**
- 冷机最低能效要求 (EER, COP)
- 水泵效率要求
- 风机效率要求

**CIM 映射**:
```yaml
cim:Chiller
  - cop: 5.7
  - ieer: 6.2 (综合能效)
  - compliance: "ASHRAE 90.1-2019"
  - exceeds_minimum_by: 25% (比最低要求高 25%)
```

---

## SNOMED CT 整合 (医疗领域)

### SNOMED 简介
- **全称**: Systematized Nomenclature of Medicine (医学系统化命名)
- **组织**: IHTSDO
- **用途**: 临床术语标准

### SNOMED → CIM 映射 (医疗气体)

```yaml
SNOMED:
- 309368000: Surgeon (手术医生)
- 309367005: Anesthesiologist (麻醉医生)
- 309346004: Nurse (护士)

CIM: MedicalGasOutlet
  - 位置: OR-301 (手术室)
  - 服务对象:
      - role: "SURGEON"
        snomed_code: "309368000"
      - role: "ANESTHESIOLOGIST"
        snomed_code: "309367005"
  - gas_type: MEDICAL_OXYGEN
  - flow_rate: 40 L/min (麻醉机需求)
```

### 临床应用

**氧气用量统计 (按科室)**:
```sql
SELECT
  space.department,
  SUM(gas.volume) as total_oxygen_consumption
FROM
  gas_consumption
JOIN cim_space space ON gas.location = space.space_id
JOIN snomed_department dept ON space.department = dept.code
WHERE
  gas.gas_type = 'MEDICAL_OXYGEN'
  AND date BETWEEN '2025-12-01' AND '2025-12-31'
GROUP BY space.department
```

---

## 整合策略

### 1. 核心概念对齐

```yaml
概念: "温度传感器"

IFC: IfcSensor (几何位置)
Brick: brick:Temperature_Sensor (语义)
REC: asset-temp-sensor-001 (资产)
CIM: Sensor/Temperature (综合)

CIM 整合:
  - 继承 IFC 的位置: located_in_space
  - 继承 Brick 的语义: measures_temperature
  - 关联 REC 的资产: asset_id
  - 扩展 CIM 属性: accuracy, calibration_date
```

### 2. 属性互补

```yaml
冷机属性:
  型号参数:
    - 制冷量: 1055 kW (产品样本)
    - 输入功率: 185 kW (产品样本, 设计工况)
    - COP: 5.7 (产品样本)

  运行参数 (来自 Brick):
    - 蒸发温度: 7°C (实测)
    - 冷凝温度: 35°C (实测)
    - 实际 COP: 5.2 (计算)

  性能参数 (来自 ASHRAE):
    - IPLV: 6.8 (综合部分负荷性能)
    - 是否符合最低能效: YES

  维护参数 (来自 CIM):
    - 上次维护: 2025-11-15
    - 下次维护: 2026-02-15
    - PM 周期: QUARTERLY
```

### 3. 关系增强

```yaml
IFC: 设备放置在空间
  IfcPump --(ContainedIn)--> IfcSpace

Brick: 设备属于哪个系统
  brick:Chiller --(brick:isPartOf)--> brick:HVAC_System

CIM: 综合关系
  - Equipment --(located_in)--> Space (IFC)
  - Equipment --(component_of)--> System (Brick)
  - Equipment --(serves)--> Zone (CIM 扩展)
  - Equipment --(meters_by)--> Meter (CIM 自有)
```

---

## 实现路径

### 阶段 1: 建立映射表

创建 Excel/数据库表:

| CIM 类 | IFC 类 | Brick 类 | REC 类 | 属性映射 |
|-------|--------|----------|--------|----------|
| Chiller | IfcUnitaryEquipment | brick:Chiller | Chiller | 见下表 |
| AHU | IfcUnitaryEquipment | brick:AHU | AirHandler | ... |
| Room | IfcSpace | brick:Room | Room | ... |

### 阶段 2: 开发转换工具

```python
def ifc_to_cim(ifc_file):
    """IFC → CIM 转换"""
    cim_model = CIMModel()

    # 提取空间
    for ifc_space in ifc_file.by_type('IfcSpace'):
        cim_space = Space(
            space_id=generate_cim_id(ifc_space),
            ifc_id=ifc_space.GlobalId,
            area_m2=get_area(ifc_space),
            # ...
        )
        cim_model.add_space(cim_space)

    # 提取设备
    for ifc_equip in ifc_file.by_type('IfcDistributionElement'):
        cim_equip = map_to_cim_equipment(ifc_equip)
        cim_model.add_equipment(cim_equip)

    return cim_model

def cim_to_brick(cim_model):
    """CIM → Brick RDF"""
    graph = rdflib.Graph()

    for equipment in cim_model.equipment:
        brick_uri = f"brick:{equipment.equipment_type}_{equipment.equipment_id}"
        graph.add((brick_uri, RDF.type, BRICK[equipment.brick_class]))
        graph.add((brick_uri, BRICK.hasTag, BRICK.Equipment))
        # ...

    return graph
```

### 阶段 3: 建立本体桥

```turtle
# CIM-Bridge.ttl
@prefix cim: <http://cim.healthcare.org/ontology#> .
@prefix brick: <https://brickschema.org/schema/Brick#> .
@prefix ifc: <http://ifc-ontology.org/IFC4_ADD2#> .
@prefix rec: <https://w3id.org/rec#> .

cim:Chiller a owl:Class ;
    rdfs:subClassOf cim:HVAC_Equipment ;
    owl:equivalentClass brick:Chiller ;
    skos:closeMatch rec:Chiller ;
    skos:relatedMatch ifc:IfcUnitaryEquipment .

cim:Supply_Air_Temperature_Sensor a owl:Class ;
    owl:equivalentClass brick:Supply_Air_Temperature_Sensor ;
    cim:mapsTo ifc:IfcSensor :TEMPERATURE_SENSOR .
```

---

## 整合价值

### 1. 数据互操作

单一数据模型，导出多种格式:
```
CIM (JSON-LD)
  ├── 导出 IFC → BIM 软件
  ├── 导出 Brick → 楼控系统
  ├── 导出 REC → Azure Digital Twins
  └── 导出 ASHRAE → 合规报告
```

### 2. 工具链支持

```
建模工具: Revit (IFC) → CIM Toolchain → CIM Model
楼控系统: Niagara (Brick) ← CIM Agent ← CIM Model
数字孪生: Azure ADT (REC) ← CIM Sync ← CIM Model
合规检查: DC pro (ASHRAE) ← CIM Export ← CIM Model
```

### 3. 知识积累

```
标准更新:
  ASHRAE 170-2021 → 2025 (IFC更新)
  ↓
  CIM 自动更新约束
  ↓
  已建项目 CIM 模型验证
  ↓
  生成改造建议
```

---

## 挑战与对策

### 挑战 1: 标准版本差异

问题: IFC2x3 vs IFC4 vs IFC4.3 属性命名不同

对策:
```python
def normalize_ifc_props(ifc_props):
    # 统一不同版本的属性名
    if 'Pset_PumpFlow' in ifc_props:  # IFC2x3
        flow = ifc_props['Pset_PumpFlow'].FlowRate
    elif 'FlowRate' in ifc_props:  # IFC4
        flow = ifc_props['FlowRate']
    elif 'NominalFlowRate' in ifc_props:  # IFC4.3
        flow = ifc_props['NominalFlowRate']

    return flow
```

### 挑战 2: 属性粒度差异

问题: Brick 有 1000+ 属性，IFC 只有基础属性

对策:
- CIM 作为超集
- 用默认值模板补充
```yaml
cim_chiller_default_props:
  min_condensing_temp: 15°C  (ASHRAE 要求)
  max_evaporating_temp: 12°C (ASHRAE 要求)
  refrigerant_charge: 500 kg (典型值，需核实)

IFC import → Fill with defaults → Review by expert
```

### 挑战 3: 语义歧义

问题: "Temperature" 可以指供水温度、回水温度、室外温度

对策:
```turtle
brick:Supply_Water_Temperature a brick:Point ;
    skos:prefLabel "Supply Water Temperature"@en ;
    brick:hasQuantity brick:Temperature ;
    brick:isLocatedIn brick:Water_System ;
    brick:hasRole brick:Supply ;

cim:CHW_Supply_Temperature a cim:Point ;
    rdfs:subPropertyOf brick:Supply_Water_Temperature ;
    cim:medium_type cim:CHW ;  # 进一步限定介质
```

---

## 未来展望

### 1. 标准融合

未来方向:
```
IFC + Brick + REC + CIM → BuildingMeta (单一标准)
                          ↓
                        Iso 19650 (统一数据环境)
```

### 2. AI 辅助对齐

```
利用 NLP + 知识图谱:
输入: IFC属性描述、Brick类名、CIM术语
输出: 自动映射建议 + 置信度

人工验证: 高置信度自动确认，低置信度人工审核
```

### 3. 跨行业本体

```
医疗建筑本体 <-> 制造业本体 (ISA-95) <-> 智慧城市 (CityGML)
       ↓                          ↓                      ↓
工艺流程管理                生产线控制       城市能源网格
```

---

## 小结

CIM 与行业标准的整合策略:

1. **互补**: IFC 提供几何，Brick 提供楼控语义，CIM 提供医疗领域知识
2. **桥接**: REC 提供资产框架，统一身份管理
3. **增效**: ASHRAE 提供技术规范，SNOMED 提供临床背景
4. **开放**: 支持导入/导出多种格式，不锁定单一供应商

**核心价值**: 单一数据源，多方受益。

---

## 参考链接

- IFC Standard: https://standards.buildingsmart.org/
- Brick Schema: https://brickschema.org/
- RealEstateCore: https://w3id.org/rec
- ASHRAE: https://www.ashrae.org/
- SNOMED CT: https://www.snomed.org/

---

*"标准不应该是束缚，而应该是基石。CIM 站在巨人的肩膀上，看得更远。"*
