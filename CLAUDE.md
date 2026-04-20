# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**CIM Unified Domain Model for Healthcare Buildings (医疗建筑统一领域模型)**

A knowledge engineering project that applies multi-agent AI methodologies to healthcare building domain modeling. The project creates a Common Information Model (CIM) for medical building technical systems, enabling digital twin implementation from design to operations.

## Project Structure

```
统一领域模型（CIM）/
├── Context Engineering/       # Main documentation (35+ documents)
│   ├── 00_foundations/       # 12 theoretical foundation docs
│   ├── 10_guides/            # 6 practical guides
│   ├── 20_templates/         # 5 modeling templates
│   ├── 30_examples/          # 5 case studies
│   └── 40_reference/         # 6 reference docs
├── codex/                     # Code assets and visualizations (HTML)
├── docs/                      # Agent definitions and concept docs
│   ├── agents/               # 9 Agent definitions (01-09)
│   ├── concept/              # Concept documentation
│   └── issues/               # Issue tracking
├── plans/                     # Project plans and milestones
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
- `ontology/cim_medical_ontology.jsonld` - JSON-LD ontology definition
- `entities/` - Entity instances
- `relationships/` - Relationship definitions
- `index/` - Entity indexes
- `Validation_Report/` - Validation reports
- `Raw_Agent_Outputs/` - Agent outputs organized by Agent-01 to Agent-08
- `Design_Documents/` - Design documentation
- `Deployment_Scripts/` - Deployment scripts

## Multi-Agent Architecture

The project uses 9 specialized agents for collaborative modeling:

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

Agent definitions are in `docs/agents/` with detailed CLI instructions in `Agent-09 CIM数据包生成器 - CLI执行指令.md`.

## Core Ontology Classes

Key entity classes defined in the CIM ontology:

**Space Hierarchy**: `Space` → `Building` → `Floor` → `Zone` → `Room` (with specialized types like `SurgeryRoom`, `ICU`, `EmergencyRoom`)

**Equipment Categories**:
- `HVACEquipment`: `AirHandlingUnit`, `Chiller`, `CoolingTower`, `Boiler`, `HeatExchanger`, `Fan`, `Pump`, `VAVBox`, `FCU`
- `ElectricalEquipment`: `Transformer`, `Switchgear`, `DistributionPanel`, `UPS`, `EmergencyGenerator`, `ATS`
- `PlumbingEquipment`: `WaterTank`, `WaterHeater`, `SewagePump`
- `MedicalGasEquipment`: `OxygenManifold`, `VacuumPump`, `MedicalAirCompressor`, `N2OManifold`
- `FireProtectionEquipment`: `FirePump`, `SprinklerHead`, `FireAlarmPanel`, `SmokeDetector`

**Sensors**: `TemperatureSensor`, `HumiditySensor`, `PressureSensor`, `FlowSensor`, `CO2Sensor`, `PowerSensor`

## Key Documents

**Entry Points**:
- `Context Engineering/README.md` - Document navigation
- `EVALUATION_REPORT.md` - Project evaluation and progress tracking
- `docs/agents/README.md` - Agent system overview

**Core Foundations**:
- `Context Engineering/00_foundations/01_vision_and_goals.md` - Project vision
- `Context Engineering/00_foundations/03_cim_ontology_introduction.md` - CIM ontology intro
- `Context Engineering/00_foundations/04_cim_pim_psm_architecture.md` - CIM-PIM-PSM three-layer architecture

**Implementation Guide**:
- `Context Engineering/10_guides/02_bim_engineer_guide.md` - BIM engineer implementation guide with code examples

## Current Phase

**M1: CIM Basic Schema and Examples** (65% complete as of 2025-12-07)

Planned completion: 2025-12-31

## Standards Alignment

The CIM model aligns with:
- **IFC** (Industry Foundation Classes) - for BIM compatibility
- **Brick Schema** - for building energy modeling
- **ASHRAE** standards - for HVAC systems
- **Project Haystack** - for semantic tagging

## Output Formats

Agent outputs are generated in:
- **Markdown** (.md) - Documentation and reports
- **YAML** (.yaml) - Structured data and templates
- **JSON-LD** (.jsonld) - Ontology definitions and entity graphs
- **HTML** (.html) - Visualizations in `codex/`
