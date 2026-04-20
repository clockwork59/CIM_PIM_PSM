# CIM 统一领域模型 - 目录结构定义

## 版本信息
- 版本: v0.2.0-Alpha
- 生成日期: 2025-01-17
- 生成工具: Gemini CLI (本体工程索引与协调者)
- 目标路径: `/project_deliverables/version02/cim/`

## 目录树结构

```
cim/
├── core/
│   ├── base_entities.ttl
│   ├── relationships.ttl
│   └── datatypes.ttl
├── topology/
│   ├── node_types.ttl
│   ├── edge_types.ttl
│   └── system_catalog.ttl
├── spaces/
│   ├── spatial_hierarchy.ttl
│   ├── zone_classification.ttl
│   └── medical_special_spaces.ttl
├── equipment/
│   ├── equipment_hierarchy.ttl
│   ├── mechanical.ttl
│   ├── electrical.ttl
│   ├── plumbing.ttl
│   ├── medical_gas.ttl
│   ├── fire_protection.ttl
│   ├── vertical_transport.ttl
│   └── reliability_classification.ttl
├── flow/
│   ├── flow_layers.ttl
│   ├── flow_media.ttl
│   └── flow_sequences.ttl
├── coupling/
│   ├── equipment_location.ttl
│   ├── routing_space.ttl
│   └── service_relations.ttl
├── control/
│   ├── sensors.ttl
│   ├── actuators.ttl
│   ├── controllers.ttl
│   └── control_loops.ttl
├── metering/
│   ├── metering_hierarchy.ttl
│   ├── energy_media.ttl
│   └── allocation_rules.ttl
├── operations/
│   ├── work_orders.ttl
│   ├── maintenance_strategies.ttl
│   ├── asset_lifecycle.ttl
│   └── alarm_system.ttl
├── services/
│   ├── chilled_water_service.ttl
│   ├── hot_water_service.ttl
│   └── clean_air_service.ttl
├── rules/
│   ├── equipment_merging_rules.sparql
│   ├── service_inference_rules.sparql
│   ├── cross_agent_validation.sparql
│   └── shacl_constraints.ttl
├── medical_constraints/
│   ├── gb50333_cleanroom.ttl
│   ├── gb51039_hospital.ttl
│   └── medical_gas_safety.ttl
├── _index.ttl
├── _config.json
└── _glossary.json
```

## 文件-Agent来源映射表

| 目录 | 主要来源Agent | 次要依赖Agent | 文件数 |
|------|--------------|---------------|--------|
| core/ | Agent-09 | - | 3 |
| topology/ | Agent-01 | - | 3 |
| spaces/ | Agent-02 | - | 3 |
| equipment/ | Agent-03 | Agent-01 | 8 |
| flow/ | Agent-04 | Agent-01 | 3 |
| coupling/ | Agent-05 | Agent-01, 02, 03 | 3 |
| control/ | Agent-06 | Agent-01, 03, 04 | 4 |
| metering/ | Agent-07 | Agent-01, 03, 05 | 3 |
| operations/ | Agent-08 | Agent-03, 06, 07 | 4 |
| services/ | Agent-04, 05 | - | 3 |
| rules/ | Agent-09 | All | 4 |
| medical_constraints/ | Agent-02, 09 | - | 3 |

## 命名空间定义

```turtle
@prefix cim:        <https://cim.medical/ontology/v3.4#> .
@prefix cim-topo:   <https://cim.medical/ontology/v3.4/topology#> .
@prefix cim-space:  <https://cim.medical/ontology/v3.4/space#> .
@prefix cim-equip:  <https://cim.medical/ontology/v3.4/equipment#> .
@prefix cim-flow:   <https://cim.medical/ontology/v3.4/flow#> .
@prefix cim-couple: <https://cim.medical/ontology/v3.4/coupling#> .
@prefix cim-ctrl:   <https://cim.medical/ontology/v3.4/control#> .
@prefix cim-meter:  <https://cim.medical/ontology/v3.4/metering#> .
@prefix cim-om:     <https://cim.medical/ontology/v3.4/operations#> .
@prefix cim-svc:    <https://cim.medical/ontology/v3.4/services#> .
@prefix cim-med:    <https://cim.medical/ontology/v3.4/medical#> .
```
