# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**CIM Unified Domain Model for Healthcare Buildings (医疗建筑统一领域模型)**

A knowledge engineering project applying multi-agent AI methodologies to healthcare building domain modeling. Creates a Common Information Model (CIM) for medical building technical systems to enable digital twin implementation from design to operations.

The three-layer architecture is **CIM → PIM → PSM** (platform-independent → platform-specific). See `Context Engineering/00_foundations/04_cim_pim_psm_architecture.md` for details.

## Project Structure

```
/
├── Context Engineering/       # 35+ documentation files (theory, guides, templates, examples, references)
│   ├── 00_foundations/       # 12 theoretical foundation docs
│   ├── 10_guides/            # 6 role-specific implementation guides
│   ├── 20_templates/         # 5 modeling templates
│   ├── 30_examples/          # 5 case studies
│   └── 40_reference/         # 6 reference catalogs
├── codex/                     # HTML visualizations for each agent domain
├── docs/
│   ├── agents/               # 9 agent definition files (Agent-01 through Agent-09)
│   ├── concept/              # Concept documentation
│   └── issues/               # Issue tracking
├── plans/                     # Project milestones (M1–M7 in 项目总控计划.md)
├── project_deliverables/      # Generated CIM bundles (version01, version02, etc.)
└── generate_cim_bundle.sh     # CIM data package generator
```

## Document ID Convention

All documents follow the naming convention: `CIMU-分类-编号-标题`

- **CIMU**: CIM Unified prefix
- **分类**: FOUND (foundations), GUIDE (guides), TEMP (templates), CASE (examples), REF (reference)
- **编号**: Sequential number (01, 02, ...)

## Key Commands

### Generate CIM Bundle

```bash
./generate_cim_bundle.sh
```

Generates a complete CIM data package in `project_deliverables/CIM_Bundle/` containing:
- `ontology/cim_medical_ontology.jsonld` — JSON-LD ontology (156 class definitions)
- `entities/` — 2000+ entity instances
- `relationships/` — topology relationships (upstreamOf, downstreamOf, powers, etc.)
- `index/` — entity indexes
- `Validation_Report/` — validation reports
- `Raw_Agent_Outputs/` — outputs by Agent-01 to Agent-08
- `Design_Documents/` and `Deployment_Scripts/`

### Inspect current deliverables

The most complete deliverable is `project_deliverables/version02/cim/`, which includes:
- `ontology_skeleton.ttl` — RDF/Turtle ontology
- `equipment/mechanical.ttl`, `equipment/electrical.ttl` — equipment hierarchies
- `rules/shacl_constraints.ttl` — SHACL validation constraints
- `rules/cross_agent_validation.sparql` — SPARQL validation queries
- `data_dictionary.yaml`, `global_id_registry.yaml` — structured metadata

## Multi-Agent Architecture

9 specialized agents produce outputs that are integrated by Agent-09. Agent definitions are in `docs/agents/`.

| Agent | Role | Responsibility |
|-------|------|----------------|
| Agent-01 | System Topology Architect | Building systems (HVAC, electrical, plumbing, etc.) |
| Agent-02 | Space Ontology Architect | Spatial hierarchy (building→floor→zone→room) |
| Agent-03 | Equipment Ontology Architect | Equipment and devices |
| Agent-04 | Flow Model Architect | Mass, energy, and information flows |
| Agent-05 | System-Space Coupling Architect | Links systems to spaces |
| Agent-06 | Control System Architect | Sensors, actuators, and control loops |
| Agent-07 | Metering System Architect | Energy metering and allocation |
| Agent-08 | O&M Management Architect | Alarms, work orders, maintenance |
| Agent-09 | Model Integration Validator | Integrates and validates all models |

Each agent has a defined input/output contract; outputs are written to `docs/agents/` and `docs/cim/`. CLI execution instructions for Agent-09 are in `docs/agents/Agent-09 CIM数据包生成器 - CLI执行指令.md`.

## Core Ontology Classes

**Space Hierarchy**: `Space` → `Building` → `Floor` → `Zone` → `Room` (with specialized types: `SurgeryRoom`, `ICU`, `EmergencyRoom`)

**Equipment Categories**:
- `HVACEquipment`: `AirHandlingUnit`, `Chiller`, `CoolingTower`, `Boiler`, `HeatExchanger`, `Fan`, `Pump`, `VAVBox`, `FCU`
- `ElectricalEquipment`: `Transformer`, `Switchgear`, `DistributionPanel`, `UPS`, `EmergencyGenerator`, `ATS`
- `PlumbingEquipment`: `WaterTank`, `WaterHeater`, `SewagePump`
- `MedicalGasEquipment`: `OxygenManifold`, `VacuumPump`, `MedicalAirCompressor`, `N2OManifold`
- `FireProtectionEquipment`: `FirePump`, `SprinklerHead`, `FireAlarmPanel`, `SmokeDetector`

**Sensors**: `TemperatureSensor`, `HumiditySensor`, `PressureSensor`, `FlowSensor`, `CO2Sensor`, `PowerSensor`

## Key Documents

**Navigation hubs**:
- `Context Engineering/README.md` — full document map with links
- `EVALUATION_REPORT.md` — progress metrics and agent completion status
- `plans/项目总控计划.md` — M1–M7 milestone plan

**Core theory**:
- `Context Engineering/00_foundations/01_vision_and_goals.md` — project vision and strategic goals
- `Context Engineering/00_foundations/04_cim_pim_psm_architecture.md` — three-layer MDA architecture (622 lines)
- `Context Engineering/00_foundations/10_ontology_integration.md` — IFC/Brick/ASHRAE/Haystack alignment

**Role-specific guides** (`Context Engineering/10_guides/`):
- `02_bim_engineer_guide.md` — IFC-to-CIM mapping with Python pseudocode
- `03_data_engineer_guide.md` — data pipeline and integration
- `04_architect_guide.md` — system design perspective
- `06_knowledge_contributor_guide.md` — how to author and extend the model

**Case studies** (`Context Engineering/30_examples/`):
- `cim_operating_room_modeling.md` — end-to-end OR room example
- `cim_pim_psm_transformation_chain.md` — full transformation chain walkthrough

## Output Formats

- **Markdown** (.md) — documentation and reports
- **YAML** (.yaml) — structured data (data dictionary, ID registry, schedules)
- **JSON-LD** (.jsonld) — ontology definitions and entity graphs
- **Turtle/RDF** (.ttl) — formal ontology (equipment hierarchies, SHACL constraints)
- **SPARQL** (.sparql) — cross-agent validation queries
- **HTML** (.html) — interactive visualizations in `codex/`

## Standards Alignment

- **IFC** (Industry Foundation Classes) — BIM compatibility
- **Brick Schema** — building energy modeling
- **ASHRAE** — HVAC systems
- **Project Haystack** — semantic tagging
