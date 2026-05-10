# ABox Generation Report — NBU Medical Clinic

**Generated**: 2026-05-10 04:19:21
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

| Brick Class | ID Pattern | Example |
|-------------|-----------|---------|
| brk:Diffuser | DIFF-SD-{seq:03d} | DIFF-SD-001 |
| brk:Return_Air_Grille | DIFF-RR-{seq:03d} | DIFF-RR-001 |
| brk:Exhaust_Air_Grille | DIFF-ER-{seq:03d} | DIFF-ER-001 |
| brk:Fan | FAN-GN-{seq:03d} | FAN-GN-001 |
| brk:Supply_Fan | FAN-SF-{seq:03d} | FAN-SF-001 |
| brk:Exhaust_Fan | FAN-EF-{seq:03d} | FAN-EF-001 |
| brk:VAV_Box | VAV-BOX-{seq:03d} | VAV-BOX-001 |
| brk:Air_Handler_Unit | AHU-{seq:03d} | AHU-001 |
| brk:Chiller | CH-{seq:03d} | CH-001 |
| cim:Floor | FLOOR-{name} | FLOOR-First_Floor |
| cim:Room | ROOM-{name} | ROOM-2A03 |

## Notes

- Instances are deduplicated by IFC GlobalId across HVAC and Arch sections
- Room-to-floor linkage uses heuristic based on room name prefix
- Space type classification uses `cim_type` from `space_mappings`
- UNKNOWN spaces default to `cim-space:Room`
