#!/usr/bin/env python3
"""
CMMS Work Order Simulator — CIM M3 Sprint 2026-05-10
=====================================================
Reads the existing IFC ABox (nbu_medical_clinic_instances.ttl) and generates
synthetic CMMS work order instances linked to CIM equipment.

Output: project_deliverables/version02/cim/abox/nbu_cmms_workorders.ttl
        (~480 WorkOrder instances: PM + CM + Inspection)

Usage (in Codespace):
    cd project_deliverables/version02
    python simulation/cmms_simulator.py

Dependencies: rdflib >= 6.0
"""

import sys
import random
from datetime import datetime, timedelta
from pathlib import Path
from rdflib import Graph, Namespace, Literal, URIRef, RDF, RDFS, OWL, XSD

# ──────────────────────────────────────────────────────────────────────────────
# PATHS
# ──────────────────────────────────────────────────────────────────────────────
BASE      = Path(__file__).resolve().parent.parent
ABOX_IFC  = BASE / "cim/abox/nbu_medical_clinic_instances.ttl"
OUT_FILE  = BASE / "cim/abox/nbu_cmms_workorders.ttl"

# ──────────────────────────────────────────────────────────────────────────────
# NAMESPACES
# ──────────────────────────────────────────────────────────────────────────────
CIM        = Namespace("http://hospital-cim.org/v4/core#")
CIM_CMMS   = Namespace("http://hospital-cim.org/v4/cmms#")
CMMS_INST  = Namespace("http://hospital-cim.org/v4/cmms/instances#")
INST       = Namespace("http://hospital-cim.org/v4/instances#")

# ──────────────────────────────────────────────────────────────────────────────
# MAINTENANCE SCHEDULE CONFIGURATION
# Maps equipment type prefix → (PM interval, estimated hours, team)
# ──────────────────────────────────────────────────────────────────────────────
PM_SCHEDULE = {
    "AHU":   ("QUARTERLY",   4.0,  "HVAC"),
    "VAV":   ("SEMI-ANNUAL", 1.0,  "HVAC"),
    "CH":    ("ANNUAL",     16.0,  "HVAC"),
    "CT":    ("SEMI-ANNUAL", 4.0,  "HVAC"),
    "PUMP":  ("SEMI-ANNUAL", 2.0,  "HVAC"),
    "FCU":   ("SEMI-ANNUAL", 1.5,  "HVAC"),
    "EF":    ("QUARTERLY",   1.5,  "HVAC"),
    "SF":    ("QUARTERLY",   1.5,  "HVAC"),
    "SMOKE": ("ANNUAL",      0.5,  "FAS"),
    "HEAT":  ("ANNUAL",      0.5,  "FAS"),
    "DIFF":  ("ANNUAL",      0.5,  "HVAC"),
}

# FMEA failure modes per equipment type (subset; aligns to CIM FMEA module 200+ modes)
FAILURE_MODES = {
    "AHU": [
        "FM-AHU-001: Belt drive failure — fan speed drop > 20%",
        "FM-AHU-002: Filter clogging — supply pressure drop > 150 Pa above baseline",
        "FM-AHU-003: Cooling coil fouling — supply air temperature > 18°C under full load",
        "FM-AHU-004: VFD overtemperature fault — shutdown triggered",
        "FM-AHU-005: Damper actuator failure — stuck at last position",
    ],
    "VAV": [
        "FM-VAV-001: Damper actuator seized — zero flow condition",
        "FM-VAV-002: Flow sensor failure — unreliable flow reading",
        "FM-VAV-003: Room temperature sensor drift > 2°C",
    ],
    "CH": [
        "FM-CH-001: Refrigerant leak — COP decline > 25%",
        "FM-CH-002: Compressor motor high current trip",
        "FM-CH-003: Condenser tube fouling — approach temperature > 3°C",
        "FM-CH-004: Low chilled water flow alarm",
        "FM-CH-005: Evaporator freeze protection trip",
    ],
    "PUMP": [
        "FM-PUMP-001: Bearing wear — vibration > 4 mm/s RMS",
        "FM-PUMP-002: Seal leak — water ingress to motor",
        "FM-PUMP-003: Cavitation — suction pressure below NPSHr",
    ],
    "SMOKE": [
        "FM-SMOKE-001: Sensing chamber contamination — nuisance alarm",
        "FM-SMOKE-002: Communication loop fault — device offline",
    ],
    "HEAT": [
        "FM-HEAT-001: Fixed-temperature element failure — no alarm on test",
        "FM-HEAT-002: Wiring short — circuit fault at FACU",
    ],
}

# Work order status distribution
STATUS_WEIGHTS = {
    "PM": [
        ("status_Open",      0.40),
        ("status_InProgress",0.25),
        ("status_Completed", 0.30),
        ("status_Cancelled", 0.05),
    ],
    "CM": [
        ("status_Open",      0.30),
        ("status_InProgress",0.35),
        ("status_Completed", 0.25),
        ("status_OnHold",    0.10),
    ],
    "INSP": [
        ("status_Completed", 0.60),
        ("status_Open",      0.30),
        ("status_InProgress",0.10),
    ],
}

PRIORITY_MAP = {
    "CH":    "priority_High",
    "AHU":   "priority_Medium",
    "SMOKE": "priority_Critical",
    "HEAT":  "priority_Critical",
    "VAV":   "priority_Low",
    "PUMP":  "priority_Medium",
    "FCU":   "priority_Low",
    "EF":    "priority_Medium",
    "SF":    "priority_Medium",
    "CT":    "priority_Medium",
    "DIFF":  "priority_Low",
}

TECHNICIANS = [
    "TECH-HVAC-001", "TECH-HVAC-002", "TECH-HVAC-003",
    "TECH-FAS-001",  "TECH-FAS-002",
    "TECH-ELEC-001", "TECH-ELEC-002",
]


def get_equip_type(equip_id: str) -> str:
    prefix = equip_id.split("-")[0].upper()
    aliases = {"CHILLER": "CH", "CHW": "PUMP", "CWP": "PUMP",
               "FAN": "EF", "EXHAUST": "EF", "SUPPLY": "SF"}
    return aliases.get(prefix, prefix)


def weighted_choice(choices: list) -> str:
    labels, weights = zip(*choices)
    return random.choices(list(labels), weights=list(weights), k=1)[0]


def iso_date(base: datetime, delta_days: int = 0) -> str:
    d = base + timedelta(days=delta_days)
    return d.strftime("%Y-%m-%dT%H:%M:%S+08:00")


def build_cmms_graph(equipment: list, seed_date: datetime) -> tuple:
    random.seed(20260510)  # reproducible

    g = Graph()
    g.bind("owl",      OWL)
    g.bind("rdf",      RDF)
    g.bind("rdfs",     RDFS)
    g.bind("xsd",      XSD)
    g.bind("cim-cmms", CIM_CMMS)
    g.bind("cmms",     CMMS_INST)
    g.bind("inst",     INST)

    wo_count = 0
    pm_count = cm_count = insp_count = 0

    # Add technician instances
    for tech_id in TECHNICIANS:
        tech_uri = CMMS_INST[tech_id]
        g.add((tech_uri, RDF.type, CIM_CMMS["MaintenanceTechnician"]))
        g.add((tech_uri, RDFS.label, Literal(tech_id, lang="en")))

    # Add team instances
    for team_id in ["TEAM-HVAC", "TEAM-FAS", "TEAM-ELEC"]:
        team_uri = CMMS_INST[team_id]
        g.add((team_uri, RDF.type, CIM_CMMS["MaintenanceTeam"]))
        g.add((team_uri, RDFS.label, Literal(team_id, lang="en")))

    for equip_id, equip_uri in equipment:
        etype = get_equip_type(equip_id)
        pm_info = PM_SCHEDULE.get(etype)
        if not pm_info:
            continue

        interval, est_hours, team_code = pm_info
        priority = PRIORITY_MAP.get(etype, "priority_Low")
        team_uri = CMMS_INST[f"TEAM-{team_code}"]

        # ── Generate 1 PM Work Order per equipment ──────────────────────────
        wo_count += 1
        pm_count += 1
        wo_id = f"WO-PM-202605-{wo_count:04d}"
        wo_uri = CMMS_INST[wo_id]
        status = weighted_choice(STATUS_WEIGHTS["PM"])

        g.add((wo_uri, RDF.type,                     CIM_CMMS["PreventiveMaintenance"]))
        g.add((wo_uri, RDFS.label,                   Literal(f"PM: {equip_id} {interval} maintenance", lang="en")))
        g.add((wo_uri, CIM_CMMS["hasWorkOrderID"],   Literal(wo_id)))
        g.add((wo_uri, CIM_CMMS["maintenanceTarget"],equip_uri))
        g.add((wo_uri, CIM_CMMS["hasWorkOrderStatus"], CIM_CMMS[status]))
        g.add((wo_uri, CIM_CMMS["hasWorkOrderPriority"], CIM_CMMS[priority]))
        g.add((wo_uri, CIM_CMMS["hasMaintenanceInterval"], Literal(interval)))
        g.add((wo_uri, CIM_CMMS["estimatedDurationHours"], Literal(est_hours, datatype=XSD.decimal)))
        g.add((wo_uri, CIM_CMMS["managedByTeam"],    team_uri))
        g.add((wo_uri, CIM_CMMS["scheduledStartDate"], Literal(iso_date(seed_date, random.randint(0, 30)), datatype=XSD.dateTime)))
        tech_uri = CMMS_INST[random.choice([t for t in TECHNICIANS if team_code in t or "HVAC" in t])]
        g.add((wo_uri, CIM_CMMS["assignedTo"],       tech_uri))

        if status == "status_Completed":
            g.add((wo_uri, CIM_CMMS["completedDate"], Literal(iso_date(seed_date, -random.randint(1, 14)), datatype=XSD.dateTime)))

        # ── Conditionally generate 1 CM Work Order (10% of equipment) ────────
        if random.random() < 0.10:
            wo_count += 1
            cm_count += 1
            wo_id_cm = f"WO-CM-202605-{wo_count:04d}"
            wo_cm_uri = CMMS_INST[wo_id_cm]
            status_cm = weighted_choice(STATUS_WEIGHTS["CM"])
            failure_modes = FAILURE_MODES.get(etype, ["FM-GEN-001: General equipment fault"])
            failure = random.choice(failure_modes)
            cm_priority = "priority_Critical" if etype in ("SMOKE", "HEAT", "CH") else "priority_High"

            g.add((wo_cm_uri, RDF.type,                     CIM_CMMS["CorrectiveMaintenance"]))
            g.add((wo_cm_uri, RDFS.label,                   Literal(f"CM: {equip_id} fault repair", lang="en")))
            g.add((wo_cm_uri, CIM_CMMS["hasWorkOrderID"],   Literal(wo_id_cm)))
            g.add((wo_cm_uri, CIM_CMMS["maintenanceTarget"],equip_uri))
            g.add((wo_cm_uri, CIM_CMMS["hasWorkOrderStatus"], CIM_CMMS[status_cm]))
            g.add((wo_cm_uri, CIM_CMMS["hasWorkOrderPriority"], CIM_CMMS[cm_priority]))
            g.add((wo_cm_uri, CIM_CMMS["hasFailureMode"],   Literal(failure)))
            g.add((wo_cm_uri, CIM_CMMS["estimatedDurationHours"], Literal(round(est_hours * 0.5, 1), datatype=XSD.decimal)))
            g.add((wo_cm_uri, CIM_CMMS["managedByTeam"],    team_uri))
            g.add((wo_cm_uri, CIM_CMMS["scheduledStartDate"], Literal(iso_date(seed_date, -random.randint(0, 3)), datatype=XSD.dateTime)))
            g.add((wo_cm_uri, CIM_CMMS["assignedTo"],        tech_uri))

        # ── Generate Inspection Work Order for safety-critical equipment ──────
        if etype in ("SMOKE", "HEAT", "CH", "AHU"):
            wo_count += 1
            insp_count += 1
            wo_id_insp = f"WO-INSP-202605-{wo_count:04d}"
            wo_insp_uri = CMMS_INST[wo_id_insp]
            status_insp = weighted_choice(STATUS_WEIGHTS["INSP"])

            g.add((wo_insp_uri, RDF.type,                     CIM_CMMS["InspectionOrder"]))
            g.add((wo_insp_uri, RDFS.label,                   Literal(f"INSP: {equip_id} routine inspection", lang="en")))
            g.add((wo_insp_uri, CIM_CMMS["hasWorkOrderID"],   Literal(wo_id_insp)))
            g.add((wo_insp_uri, CIM_CMMS["maintenanceTarget"],equip_uri))
            g.add((wo_insp_uri, CIM_CMMS["hasWorkOrderStatus"], CIM_CMMS[status_insp]))
            g.add((wo_insp_uri, CIM_CMMS["hasWorkOrderPriority"], CIM_CMMS[priority]))
            g.add((wo_insp_uri, CIM_CMMS["estimatedDurationHours"], Literal(0.5, datatype=XSD.decimal)))
            g.add((wo_insp_uri, CIM_CMMS["managedByTeam"],    team_uri))
            g.add((wo_insp_uri, CIM_CMMS["scheduledStartDate"], Literal(iso_date(seed_date, random.randint(0, 7)), datatype=XSD.dateTime)))

            if status_insp == "status_Completed":
                g.add((wo_insp_uri, CIM_CMMS["completedDate"], Literal(iso_date(seed_date, -1), datatype=XSD.dateTime)))
                g.add((wo_insp_uri, CIM_CMMS["hasResolutionDescription"], Literal("Inspection passed. No faults detected.")))

    return g, wo_count, pm_count, cm_count, insp_count


def main():
    if not ABOX_IFC.exists():
        print(f"[ERROR] IFC ABox not found: {ABOX_IFC}", file=sys.stderr)
        sys.exit(1)

    print(f"[CMMS-SIM] Loading IFC ABox: {ABOX_IFC.name}")
    ifc_g = Graph()
    ifc_g.parse(str(ABOX_IFC), format="turtle")

    HAS_EQUIP_ID = CIM["hasEquipmentID"]
    equipment = [(str(eid), inst_uri)
                 for inst_uri, _, eid in ifc_g.triples((None, HAS_EQUIP_ID, None))]
    print(f"[CMMS-SIM] Found {len(equipment)} equipment instances")

    seed_date = datetime(2026, 5, 10, 8, 0, 0)
    g, total, pm, cm, insp = build_cmms_graph(equipment, seed_date)

    # Ontology header
    ont_uri = URIRef("http://hospital-cim.org/v4/abox/cmms-workorders")
    g.add((ont_uri, RDF.type,    OWL.Ontology))
    g.add((ont_uri, RDFS.label,  Literal("NBU Medical Clinic CMMS Work Orders (Simulated)", lang="en")))
    g.add((ont_uri, RDFS.comment, Literal("Generated by cmms_simulator.py for M3 multi-source federation validation.", lang="en")))
    g.add((ont_uri, OWL.imports, URIRef("http://hospital-cim.org/v4/cmms")))

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    g.serialize(destination=str(OUT_FILE), format="turtle")

    print(f"[CMMS-SIM] ✅ Done.")
    print(f"          Total work orders : {total}")
    print(f"            PM work orders  : {pm}")
    print(f"            CM work orders  : {cm}")
    print(f"            Inspections     : {insp}")
    print(f"          Output: {OUT_FILE}")
    print()
    print("[CMMS-SIM] Next step: run validation/step9_federation_validation.py")


if __name__ == "__main__":
    main()
