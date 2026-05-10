#!/usr/bin/env python3
"""
BAS/BACnet Simulator — CIM M3 Sprint 2026-05-10
================================================
Reads the existing IFC ABox (nbu_medical_clinic_instances.ttl) and generates
synthetic BACnet data point instances for each piece of equipment.

Output: project_deliverables/version02/cim/abox/nbu_bas_readings.ttl
        (~3,600 BACnetObject instances with simulated present-values)

Usage (in Codespace):
    cd project_deliverables/version02
    python simulation/bas_bacnet_simulator.py

    # With custom snapshot time:
    python simulation/bas_bacnet_simulator.py --timestamp "2026-05-10T08:00:00+08:00"
    # With noise enabled (±5% variation on base values):
    python simulation/bas_bacnet_simulator.py --noise

Dependencies: rdflib >= 6.0
"""

import argparse
import random
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from rdflib import Graph, Namespace, Literal, URIRef, RDF, RDFS, OWL, XSD
from rdflib.namespace import NamespaceManager

# ──────────────────────────────────────────────────────────────────────────────
# PATHS
# ──────────────────────────────────────────────────────────────────────────────
BASE = Path(__file__).resolve().parent.parent  # project_deliverables/version02/
ABOX_IFC   = BASE / "cim/abox/nbu_medical_clinic_instances.ttl"
ABOX_DDC   = BASE / "cim/abox/nbu_pset_enrichment.ttl"
OUT_FILE   = BASE / "cim/abox/nbu_bas_readings.ttl"
ONT_BACNET = BASE / "cim/ontology/bridge/bridge_bacnet.ttl"

# ──────────────────────────────────────────────────────────────────────────────
# NAMESPACES
# ──────────────────────────────────────────────────────────────────────────────
CIM        = Namespace("https://cim.medical/ontology/v3.4#")
CIM_EQUIP  = Namespace("https://cim.medical/ontology/v3.4/equipment#")
CIM_BACNET = Namespace("https://cim.medical/ontology/v4.0/bacnet#")
INST       = Namespace("https://cim.medical/instance/nbu_medical_clinic#")
BACNET     = Namespace("https://cim.medical/ontology/v4.0/bacnet/instances#")
XSD_NS     = XSD

# ──────────────────────────────────────────────────────────────────────────────
# EQUIPMENT TYPE → BACnet POINT TEMPLATE
# Each entry: (short_name, object_class_suffix, units, base_value, noise_range)
# object_class_suffix: "AnalogInput"|"BinaryInput"|"AnalogValue"|"MultiStateValue"
# ──────────────────────────────────────────────────────────────────────────────
POINT_TEMPLATES = {
    # Air Handling Units — 8 points each
    "AHU": [
        ("SAT",    "AnalogInput",  "degrees-celsius",         14.0,  2.0),   # Supply Air Temp
        ("RAT",    "AnalogInput",  "degrees-celsius",         24.0,  1.5),   # Return Air Temp
        ("SAP",    "AnalogInput",  "pascals",                 800.0, 50.0),  # Supply Air Pressure
        ("SAF",    "AnalogInput",  "cubic-meters-per-hour",  3600.0, 300.0), # Supply Air Flow
        ("FANKW",  "AnalogInput",  "kilowatts",               22.0,  3.0),   # Fan Power
        ("FANSS",  "BinaryInput",  "no-units",                  1,    0),    # Fan Start/Stop (1=run)
        ("FANSP",  "AnalogValue",  "percent",                 85.0,  5.0),   # Fan Speed Setpoint
        ("MODE",   "MultiStateValue", "no-units",               2,    0),    # Op Mode: 1=OFF 2=RUN 3=FAULT
    ],

    # VAV Terminal Units — 4 points each
    "VAV": [
        ("FLOW",   "AnalogInput",  "cubic-meters-per-hour",  400.0, 80.0),   # Airflow
        ("POS",    "AnalogInput",  "percent",                 65.0,  10.0),  # Damper Position
        ("RMTMP",  "AnalogInput",  "degrees-celsius",         22.5,  1.0),   # Room Temperature
        ("RMSP",   "AnalogValue",  "degrees-celsius",         22.0,  0.5),   # Room Temp Setpoint
    ],

    # Chillers — 12 points each
    "CH": [
        ("CHWST",  "AnalogInput",  "degrees-celsius",          7.0,  0.5),   # CHW Supply Temp
        ("CHWRT",  "AnalogInput",  "degrees-celsius",         12.0,  0.8),   # CHW Return Temp
        ("CDST",   "AnalogInput",  "degrees-celsius",         37.0,  1.0),   # Condenser Supply Temp
        ("CDRT",   "AnalogInput",  "degrees-celsius",         32.0,  1.0),   # Condenser Return Temp
        ("CHWF",   "AnalogInput",  "cubic-meters-per-hour",  180.0, 10.0),   # CHW Flow Rate
        ("KW",     "AnalogInput",  "kilowatts",              350.0, 25.0),   # Compressor Power
        ("COP",    "AnalogValue",  "no-units",                 5.5,  0.5),   # Calculated COP
        ("EVAP_P", "AnalogInput",  "kilopascals",             62.0,  3.0),   # Evaporator Pressure
        ("COND_P", "AnalogInput",  "kilopascals",            185.0,  8.0),   # Condenser Pressure
        ("SS",     "BinaryInput",  "no-units",                  1,    0),    # Run/Stop
        ("ALM",    "BinaryInput",  "no-units",                  0,    0),    # Fault Alarm
        ("MODE",   "MultiStateValue", "no-units",               3,    0),    # 1=OFF 2=STANDBY 3=RUN 4=FAULT
    ],

    # Cooling Tower — 5 points each
    "CT": [
        ("BASIN",  "AnalogInput",  "degrees-celsius",         28.0,  1.0),
        ("OUTLET", "AnalogInput",  "degrees-celsius",         32.0,  1.0),
        ("FANSS",  "BinaryInput",  "no-units",                  1,    0),
        ("FANSP",  "AnalogValue",  "percent",                 75.0,  5.0),
        ("ALM",    "BinaryInput",  "no-units",                  0,    0),
    ],

    # Chilled Water Pumps — 4 points each
    "PUMP": [
        ("FLOW",   "AnalogInput",  "cubic-meters-per-hour",  180.0, 15.0),
        ("HEAD",   "AnalogInput",  "kilopascals",            220.0, 20.0),
        ("KW",     "AnalogInput",  "kilowatts",               18.5,  2.0),
        ("SS",     "BinaryInput",  "no-units",                  1,    0),
    ],

    # Smoke Detectors — 2 points each
    "SMOKE": [
        ("ALM",    "BinaryInput",  "no-units",                  0,    0),    # Alarm state (0=normal)
        ("FAULT",  "BinaryInput",  "no-units",                  0,    0),    # Fault state
    ],

    # Heat Detectors — 2 points each
    "HEAT": [
        ("TEMP",   "AnalogInput",  "degrees-celsius",         22.5,  3.0),  # Ambient temp at sensor
        ("ALM",    "BinaryInput",  "no-units",                  0,    0),
    ],

    # Fan Coil Units (patient rooms) — 3 points each
    "FCU": [
        ("RMTMP",  "AnalogInput",  "degrees-celsius",         23.0,  1.0),
        ("SS",     "BinaryInput",  "no-units",                  1,    0),
        ("VLVPOS", "AnalogOutput", "percent",                 45.0,  10.0),  # Valve position
    ],

    # Exhaust/Supply Air Fans — 3 points each
    "EF": [
        ("SS",     "BinaryInput",  "no-units",                  1,    0),
        ("KW",     "AnalogInput",  "kilowatts",                5.5,  0.8),
        ("ALM",    "BinaryInput",  "no-units",                  0,    0),
    ],
    "SF": [
        ("SS",     "BinaryInput",  "no-units",                  1,    0),
        ("KW",     "AnalogInput",  "kilowatts",                7.5,  1.0),
        ("ALM",    "BinaryInput",  "no-units",                  0,    0),
    ],

    # Supply Air Diffusers — 1 point (generic presence/airflow indicator)
    "DIFF": [
        ("AIRFLOW_OK", "BinaryInput", "no-units",               1,    0),
    ],
}

# Equipment type prefix extraction: maps leading alpha chars to template key
def get_equip_type(equip_id: str) -> str:
    """
    Extract equipment type prefix from ID like 'AHU-001', 'VAV-200MM-001',
    'DIFF-SD600X-001', 'PUMP-CHW-001'.
    """
    prefix = equip_id.split("-")[0].upper()
    # normalize aliases
    aliases = {
        "CHILLER": "CH",
        "CHW":     "PUMP",
        "CWP":     "PUMP",
        "FAN":     "EF",
        "EXHAUST":  "EF",
        "SUPPLY":   "SF",
    }
    return aliases.get(prefix, prefix)


def make_point_uri(equip_id: str, point_name: str) -> URIRef:
    safe_id = equip_id.replace("/", "-").replace(" ", "_")
    return BACNET[f"{safe_id}-{point_name}"]


def make_device_uri(equip_id: str) -> URIRef:
    safe_id = equip_id.replace("/", "-").replace(" ", "_")
    return BACNET[f"CTRL-{safe_id}"]


def simulated_value(base: float, noise: float, add_noise: bool, is_binary: bool, is_msv: bool):
    """Return a realistic simulated value."""
    if is_binary:
        return Literal(bool(int(base)), datatype=XSD.boolean)
    if is_msv:
        return Literal(int(base), datatype=XSD.integer)
    if add_noise and noise > 0:
        val = base + random.uniform(-noise, noise)
    else:
        val = base
    return Literal(round(val, 2), datatype=XSD.decimal)


def load_equipment_ids(g: Graph) -> list[tuple[str, URIRef]]:
    """
    Extract (equipmentID, instanceURI) pairs from loaded IFC ABox.
    """
    HAS_EQUIP_ID = CIM["hasEquipmentID"]
    results = []
    for inst_uri, _, eid_lit in g.triples((None, HAS_EQUIP_ID, None)):
        results.append((str(eid_lit), inst_uri))
    return results


def build_bas_graph(equipment: list[tuple[str, URIRef]],
                    snapshot_ts: str,
                    add_noise: bool) -> Graph:
    g = Graph()
    g.bind("owl",      OWL)
    g.bind("rdf",      RDF)
    g.bind("rdfs",     RDFS)
    g.bind("xsd",      XSD)
    g.bind("cim",      CIM)
    g.bind("cim-bacnet", CIM_BACNET)
    g.bind("bacnet",   BACNET)
    g.bind("inst",     INST)

    ts_lit = Literal(snapshot_ts, datatype=XSD.dateTime)
    point_count = 0

    for equip_id, equip_uri in equipment:
        etype = get_equip_type(equip_id)
        templates = POINT_TEMPLATES.get(etype)
        if not templates:
            continue  # skip equipment types with no BACnet template

        # Create a BACnet Device (DDC controller) per equipment
        dev_uri = make_device_uri(equip_id)
        g.add((dev_uri, RDF.type, CIM_BACNET["BACnetDevice"]))
        g.add((dev_uri, RDFS.label, Literal(f"DDC Controller for {equip_id}", lang="en")))
        g.add((dev_uri, CIM_BACNET["hasDeviceInstance"], Literal(hash(equip_id) % 4194302, datatype=XSD.integer)))
        g.add((dev_uri, CIM_BACNET["hasControllerLink"], equip_uri))

        for (pname, obj_type, units, base, noise) in templates:
            pt_uri = make_point_uri(equip_id, pname)
            class_uri = CIM_BACNET[f"BACnet{obj_type}"]
            is_binary = obj_type == "BinaryInput" or obj_type == "BinaryOutput"
            is_msv    = obj_type == "MultiStateValue"

            g.add((pt_uri, RDF.type,                     class_uri))
            g.add((pt_uri, RDFS.label,                   Literal(f"{equip_id} {pname}", lang="en")))
            g.add((pt_uri, CIM_BACNET["hasObjectIdentifier"], Literal(f"{obj_type.lower()}:{point_count % 1000}")))
            g.add((pt_uri, CIM_BACNET["hasObjectType"],  Literal(obj_type.lower().replace("BACnet", "").lower())))
            g.add((pt_uri, CIM_BACNET["hasObjectName"],  Literal(f"{equip_id}-{pname}")))
            g.add((pt_uri, CIM_BACNET["hasUnitsID"],     Literal(units)))
            g.add((pt_uri, CIM_BACNET["hasTimestamp"],   ts_lit))
            g.add((pt_uri, CIM_BACNET["bacnetPointOf"],  equip_uri))
            g.add((pt_uri, CIM_BACNET["hostedBy"],       dev_uri))

            val_lit = simulated_value(base, noise, add_noise, is_binary, is_msv)
            g.add((pt_uri, CIM_BACNET["hasPresentValue"], val_lit))

            if not is_binary and not is_msv and noise > 0:
                g.add((pt_uri, CIM_BACNET["hasCovIncrement"], Literal(round(noise * 0.1, 3), datatype=XSD.decimal)))

            point_count += 1

    return g, point_count


def main():
    parser = argparse.ArgumentParser(description="BAS/BACnet Simulator for CIM M3")
    parser.add_argument(
        "--timestamp",
        default="2026-05-10T08:00:00+08:00",
        help="ISO 8601 snapshot timestamp (default: 2026-05-10T08:00:00+08:00)"
    )
    parser.add_argument(
        "--noise",
        action="store_true",
        help="Add ±noise to analog values for realism"
    )
    parser.add_argument(
        "--output",
        default=str(OUT_FILE),
        help=f"Output TTL file path (default: {OUT_FILE})"
    )
    args = parser.parse_args()

    # ── Load IFC ABox ──────────────────────────────────────────────────────────
    if not ABOX_IFC.exists():
        print(f"[ERROR] IFC ABox not found: {ABOX_IFC}", file=sys.stderr)
        print("  Run from project_deliverables/version02/ directory.", file=sys.stderr)
        sys.exit(1)

    print(f"[BAS-SIM] Loading IFC ABox: {ABOX_IFC.name}")
    ifc_g = Graph()
    ifc_g.parse(str(ABOX_IFC), format="turtle")

    # Optionally also load DDC instances for cross-reference
    if ABOX_DDC.exists():
        ifc_g.parse(str(ABOX_DDC), format="turtle")
        print(f"[BAS-SIM] Loaded DDC ABox: {ABOX_DDC.name}")

    equipment = load_equipment_ids(ifc_g)
    print(f"[BAS-SIM] Found {len(equipment)} equipment instances")

    # ── Build BACnet Graph ─────────────────────────────────────────────────────
    print(f"[BAS-SIM] Generating BACnet points (noise={args.noise}, ts={args.timestamp})")
    if args.noise:
        random.seed(20260510)  # reproducible seed for audit

    bas_g, n_points = build_bas_graph(equipment, args.timestamp, args.noise)

    # ── Write output ──────────────────────────────────────────────────────────
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Add ontology header
    ont_uri = URIRef("http://hospital-cim.org/v4/abox/bas-readings")
    bas_g.add((ont_uri, RDF.type,        OWL.Ontology))
    bas_g.add((ont_uri, RDFS.label,      Literal("NBU Medical Clinic BAS Readings (Simulated)", lang="en")))
    bas_g.add((ont_uri, RDFS.comment,    Literal(f"Generated by bas_bacnet_simulator.py at {args.timestamp}. Snapshot of BACnet present-values for M3 federation validation.", lang="en")))
    bas_g.add((ont_uri, OWL.imports,     URIRef("https://cim.medical/ontology/v4.0/bacnet")))

    bas_g.serialize(destination=str(out_path), format="turtle")

    print(f"[BAS-SIM] ✅ Done.")
    print(f"          Equipment processed : {len(equipment)}")
    print(f"          BACnet points written: {n_points}")
    print(f"          Output: {out_path}")
    print()
    print("[BAS-SIM] Next step: run validation/step9_federation_validation.py")


if __name__ == "__main__":
    main()
