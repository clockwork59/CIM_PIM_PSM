# Medical Domain Constraints

**Status**: ⏳ Planned / Reserved
**Agent**: Agent-09 (Medical Specialist)
**Priority**: P1 - Important

## Module Purpose

This directory is reserved for **medical-specific business rules and constraints** that extend the base SHACL constraints in `rules/shacl_constraints.ttl`.

## Reserved for Future Implementation

This directory is intentionally left empty in v2.0 to be implemented in v3.0 with detailed medical compliance rules.

## Planned Components

- `medical_compliance_rules.ttl` - Detailed medical standards compliance
- `hospital_accreditation.ttl` - JCI and NABH accreditation rules
- `infection_control.ttl` - Infection control protocols
- `medical_equipment_regulations.ttl` - Medical device regulations

## Standards Alignment

Planned standards to be integrated:
- GB 50333-2013 (Hospital clean operating rooms)
- GB 51039-2014 (Medical buildings electrical)
- WS/T 311-2009 (Isolation technology)
- GB 19489-2008 (Lab biosafety)
- ANSI/ASHRAE 170-2021 (Healthcare ventilation)

## Dependencies

- Depends on: spaces/, equipment/, rules/
- Extends: SHACL constraints from rules/shacl_constraints.ttl

## Related SHACL Shapes

The base SHACL shapes are defined in `../rules/shacl_constraints.ttl`:
- `OperatingRoom_Class_I_Shape`
- `IsolationWard_NegativePressure_Shape`
- `CleanLab_BSL3_Shape`
- `EquipmentMustHaveLocationShape`
- `NodeMustHaveEquipmentShape`

---

*Last Updated: 2025-12-12*
*Version: 2.0.0-Reserved*
