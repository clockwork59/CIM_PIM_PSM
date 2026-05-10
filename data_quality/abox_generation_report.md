# ABox Generation Report — NBU Medical Clinic

**Generated**: 2026-05-10 05:56:26
**Source**: `validation/ifc_to_cim_mapping.json`
**Output**: `project_deliverables/version02/cim/abox/nbu_medical_clinic_instances.ttl`
**IFC Sections processed**: hvac, arch

## Summary

| Metric | Count |
|--------|-------|
| Total CIM instances | 1210 |
| Equipment instances | 673 |
| Space instances | 532 |
| Floor instances | 5 |
| Skipped (no CIM mapping) | 0 |

## Equipment Breakdown by CIM Class

| CIM Class | Count |
|-----------|-------|
| SupplyAirDiffuser | 279 |
| ReturnAirGrille | 206 |
| VAV_Terminal | 110 |
| ExhaustAirGrille | 57 |
| Fan | 7 |
| ExhaustFan | 6 |
| EnergyConversionDevice | 3 |
| AHU | 2 |
| SupplyFan | 2 |
| Chiller | 1 |

## Space Breakdown by CIM Type

| Space Class | Count |
|-------------|-------|
| Room | 434 |
| OperatingRoom | 47 |
| OfficeRoom | 22 |
| ToiletRoom | 10 |
| WaitingArea | 6 |
| ReceptionArea | 4 |
| ExamRoom | 4 |
| AdministrativeRoom | 3 |
| MechanicalRoom | 1 |
| WardRoom | 1 |

## CIM ID Generation Rules

ID format: `{TYPE}-{MODEL}-{N}` where MODEL is derived from ifc_name keywords.

| Brick Class | ID Pattern | Example |
|-------------|-----------|---------|
| brk:Diffuser | DIFF-{MODEL}-{N} | DIFF-SD600-001 |
| brk:Return_Air_Grille | DIFF-{MODEL}-{N} | DIFF-RR600-001 |
| brk:VAV_Box | VAV-{MODEL}-{N} | VAV-200-001 |
| brk:Fan | FAN-{MODEL}-{N} | FAN-CENT-001 |
| brk:Chiller | CHL-{N} | CHL-001 |
| cim:Floor | FLOOR-{name} | FLOOR-First_Floor |
| cim:Room | ROOM-{name} | ROOM-2A03 |

## Notes

- Instances are deduplicated by IFC GlobalId across HVAC and Arch sections
- Room-to-floor linkage uses heuristic based on room name prefix
- Space type classification uses `cim_type` from `space_mappings`
- UNKNOWN spaces default to `cim-space:Room`
- Equipment instances include `cim:hasSystemReference` inferred from Brick class
