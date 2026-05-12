# 标准对齐映射 (Standards Alignment)

**文档 ID**: `CIMU-REF-02-标准对齐`
**最后更新**: 2026-05-11

---

## 概述

CIM v4.0 对齐 **11 项行业标准**，采用 owl:equivalentClass、bridge ontology、SHACL 约束等多种对齐方法。

---

## 标准对齐总览

| # | 标准 | 版本 | 对齐方法 | 映射数量 | CIM 实现文件 |
|---|------|------|----------|----------|-------------|
| 1 | **IFC** | IFC4 / IFC2X3 | `owl:equivalentClass` + bridge ontology | ~80 class mappings | `bridge/bridge_ifc.ttl` |
| 2 | **Brick Schema** | 1.3 | `owl:equivalentClass` | ~60 equivalentClass | `bridge/bridge_brick.ttl` |
| 3 | **ASHRAE 223P** | Draft | bridge ontology (Medium, ConnectionPoint) | ~20 class mappings | `bridge/bridge_ashrae223p.ttl` |
| 4 | **FSO** | v0.1.0 | bridge ontology + SPARQL 验证 | 35 equipment mappings | `bridge/bridge_fso.ttl` |
| 5 | **BACnet** | ASHRAE 135-2020 | bridge ontology (9 object types) | 9 class mappings | `bridge/bridge_bacnet.ttl` |
| 6 | **ISO 14224** | 2016 | WorkOrder 数据模型 | CMMS 结构对齐 | `layer4_cmms.ttl` |
| 7 | **BFO** | 2020 | `rdfs:subClassOf` 上层本体 | Continuant/Occurrent 全对齐 | `layer0_foundational.ttl` |
| 8 | **ISO 19650** | 2018 | 4-layer architecture 设计 | 架构级对齐 | 4层TBox设计 |
| 9 | **GB 50333-2013** | 2013 | SHACL 约束 + 设计准则 | 洁净室温湿度/压差 | `rules/shacl_constraints.ttl` |
| 10 | **WS 435-2013** | 2013 | SHACL 约束 | 医院建筑分级 | `rules/shacl_constraints.ttl` |
| 11 | **IEC 60364-7-710** | 2002 | SHACL 约束 | 医疗电气安全 | `rules/shacl_constraints.ttl` |

---

## 对齐方法详解

### 方法 1: owl:equivalentClass (等价类映射)

用于 IFC、Brick 等成熟本体，建立双向语义等价关系。

```turtle
cim-equip:AirHandlingUnit owl:equivalentClass brick:AHU .
cim-equip:Chiller owl:equivalentClass ifc:IfcChiller .
```

### 方法 2: Bridge Ontology (桥接本体)

为每个外部标准创建独立桥接文件，保持 CIM 核心本体的独立性。
桥接文件位于 `project_deliverables/version02/cim/ontology/bridge/`。

### 方法 3: SHACL Constraints (约束验证)

将国标/行标的数值要求编码为 SHACL 形状约束：

```turtle
# GB 50333-2013 洁净手术室温度约束
:ORTemperatureShape a sh:NodeShape ;
    sh:targetClass cim-space:SurgeryRoom ;
    sh:property [
        sh:path cim-pt:hasTemperatureSetpoint ;
        sh:minInclusive 22.0 ;
        sh:maxInclusive 25.0 ;
    ] .
```

### 方法 4: 架构级对齐 (ISO 19650)

CIM 4层 TBox 架构对应 ISO 19650 信息管理框架：

| CIM 层级 | ISO 19650 对应 | 内容 |
|----------|---------------|------|
| Layer 0 | 信息标准 | BFO 上层本体 |
| Layer 1 | 信息模型 | 概念层 (Flow, Space) |
| Layer 2 | 信息容器 | 参考层 (Medium, Standard) |
| Layer 3-4 | 信息交付 | 设计+运营层 |

---

## 验证状态

所有桥接文件通过 `cross_agent_validation.sparql` 验证：
- IFC bridge: PASS (M2 验证)
- Brick bridge: PASS (M2 验证)
- ASHRAE 223P bridge: PASS (M3 验证)
- FSO bridge: PASS (M3 验证)
- BACnet bridge: PASS (M5 验证)

---

## 相关文件

- 标准对齐理论: `Context Engineering/00_foundations/10_ontology_integration.md`
- SHACL 约束: `project_deliverables/version02/cim/rules/shacl_constraints.ttl`
- SPARQL 验证: `project_deliverables/version02/cim/rules/cross_agent_validation.sparql`
