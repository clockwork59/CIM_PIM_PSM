# M3 Deliverables — Codespace Deployment Guide

## 1. Copy TTL files to ontology directory

```bash
# From repo root in Codespace:
cp m3_deliverables/ontology/layer4_fas_security.ttl \
   project_deliverables/version02/cim/ontology/

cp m3_deliverables/ontology/layer4_cmms.ttl \
   project_deliverables/version02/cim/ontology/

cp m3_deliverables/ontology/bridge_bacnet.ttl \
   project_deliverables/version02/cim/ontology/bridge/

cp m3_deliverables/simulation/bas_bacnet_simulator.py \
   project_deliverables/version02/simulation/

cp m3_deliverables/simulation/cmms_simulator.py \
   project_deliverables/version02/simulation/

cp m3_deliverables/validation/step9_federation_validation.py \
   project_deliverables/version02/validation/
```

## 2. Patch _index_v4.ttl — add 3 new owl:imports

Open `project_deliverables/version02/cim/ontology/_index_v4.ttl` and add these
lines inside the `owl:Ontology` block, after the existing imports:

```turtle
    owl:imports <http://hospital-cim.org/v4/fas> ;
    owl:imports <http://hospital-cim.org/v4/cmms> ;
    owl:imports <http://hospital-cim.org/v4/bacnet> ;
```

Full example of what the imports section should look like:
```turtle
<http://hospital-cim.org/v4/index_v4>
    a owl:Ontology ;
    ...existing imports...
    owl:imports <http://hospital-cim.org/v4/fas> ;        # NEW M3
    owl:imports <http://hospital-cim.org/v4/cmms> ;       # NEW M3
    owl:imports <http://hospital-cim.org/v4/bacnet> ;     # NEW M3
    ...
```

## 3. Run simulators

```bash
cd project_deliverables/version02

# Generate BAS/BACnet readings ABox (~3,600 BACnet point instances)
python simulation/bas_bacnet_simulator.py --noise

# Generate CMMS work order ABox (~480 WorkOrder instances)
python simulation/cmms_simulator.py
```

Expected output files:
- `cim/abox/nbu_bas_readings.ttl`
- `cim/abox/nbu_cmms_workorders.ttl`

## 4. Run federation validation

```bash
python validation/step9_federation_validation.py
```

All 5 queries must return ≥ 1 row (Q3 is allowed to return 0 — see note in script).

## 5. Run SHACL on new ABox files

```bash
python validation/step7_shacl_full_validation.py
# Add new ABox files to DATA_FILES list in step7 script if not auto-discovered
```

Target: VIOLATION=0, WARNING=0 on all files.

## 6. Update owl:Class count

```bash
python validation/step8_count_owl_classes.py
```

Expected: 口径B ≥ 509 (482 existing + ~29 new classes across 3 modules)

## 7. Commit

```bash
git add project_deliverables/version02/cim/ontology/layer4_fas_security.ttl
git add project_deliverables/version02/cim/ontology/layer4_cmms.ttl
git add project_deliverables/version02/cim/ontology/bridge/bridge_bacnet.ttl
git add project_deliverables/version02/cim/ontology/_index_v4.ttl
git add project_deliverables/version02/cim/abox/nbu_bas_readings.ttl
git add project_deliverables/version02/cim/abox/nbu_cmms_workorders.ttl
git add project_deliverables/version02/simulation/bas_bacnet_simulator.py
git add project_deliverables/version02/simulation/cmms_simulator.py
git add project_deliverables/version02/validation/step9_federation_validation.py
git commit -m "feat(M3): add FAS/BACnet/CMMS TBox + federation simulation ABox

- layer4_fas_security.ttl: 12 owl:Class FAS device hierarchy (BFO aligned)
- bridge_bacnet.ttl: 9 owl:Class BACnet object model (ASHRAE 135-2020)
- layer4_cmms.ttl: 8 owl:Class CMMS work order lifecycle model (ISO 14224)
- nbu_bas_readings.ttl: ~3,600 synthetic BACnet point instances
- nbu_cmms_workorders.ttl: ~480 synthetic work order instances
- step9_federation_validation.py: 5 cross-source SPARQL queries

M3 federation triangle: IFC(1,210) ↔ BAS(~3,600) ↔ CMMS(~480)
Sprint: 2026-05-10 → 05-13"
```
