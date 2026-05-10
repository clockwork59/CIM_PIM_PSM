#!/usr/bin/env python3
"""
SimClock — BAS Snapshot Time-Progression Simulator
===================================================
Manages time-based stepping through BAS snapshot files and injects a
smoke-detector alarm at t1 to trigger the EventEngine fire-drill scenario.

Timeline:
  t0  baseline (all detectors NORMAL, all readings steady)
  t1  +60s  → SD-F5-001 alarm injected (single detector, PENDING state)
  t1' +30s  → SD-F5-003 alarm injected (dual-zone → auto-CONFIRMED + L2 plan)
  t2  +120s → Post-response state (alarm points cleared after suppression)

Usage:
    # Step 1: inject alarm into t1 snapshot
    python platform/sim_clock.py --inject t1

    # Step 2: run EventEngine on alarmed t1
    python platform/event_engine.py --snapshot t1

    # Step 3: advance to t2 (clear alarm, post-response)
    python platform/sim_clock.py --clear t2

    # One-shot full drill (inject + scan + advance):
    python platform/sim_clock.py --run-drill

Dependencies: rdflib >= 6.0
"""

import sys
import shutil
import argparse
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path
from rdflib import Graph, Namespace, Literal, URIRef, RDF, RDFS, XSD

# ─────────────────────────────────────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────────────────────────────────────
BASE      = Path(__file__).resolve().parent.parent.parent  # project_deliverables/version02/
ABOX_DIR  = BASE / "cim/abox"

T0_FILE   = ABOX_DIR / "nbu_bas_readings_t0.ttl"
T1_FILE   = ABOX_DIR / "nbu_bas_readings_t1.ttl"
T2_FILE   = ABOX_DIR / "nbu_bas_readings_t2.ttl"
IFC_FILE  = ABOX_DIR / "nbu_medical_clinic_instances.ttl"
FAS_FILE  = ABOX_DIR / "nbu_fas_instances.ttl"

# ─────────────────────────────────────────────────────────────────────────────
# NAMESPACES
# ─────────────────────────────────────────────────────────────────────────────
CIM        = Namespace("https://cim.medical/ontology/v3.4#")
CIM_FAS    = Namespace("https://cim.medical/ontology/v4.0/fas#")
CIM_BACNET = Namespace("https://cim.medical/ontology/v4.0/bacnet#")
INST       = Namespace("https://cim.medical/instance/nbu_medical_clinic/")
FAS_INST   = Namespace("https://cim.medical/instance/fas/")
BAS_INST   = Namespace("https://cim.medical/ontology/v4.0/bacnet/instances#")

# ─────────────────────────────────────────────────────────────────────────────
# ALARM INJECTION TARGETS
# ─────────────────────────────────────────────────────────────────────────────
# These are the two smoke detectors in FAS Zone 5 West Wing
# SD-F5-001 triggers at t1; SD-F5-003 triggers 30s later (dual-zone)

ALARM_TARGETS = {
    "t1_primary": {
        "equip_id":   "SD-2F-OR-01",
        "point_name": "SD-2F-OR-01-SMOKE_ALARM",
        "zone":       "ZONE-2F-OR",
        "delay":      0,
    },
    "t1_secondary": {
        "equip_id":   "SD-2F-OR-03",
        "point_name": "SD-2F-OR-03-SMOKE_ALARM",
        "zone":       "ZONE-2F-OR",
        "delay":      30,
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _now_ts(offset_seconds: int = 0) -> str:
    base = datetime(2026, 5, 10, 9, 0, 0, tzinfo=timezone.utc)
    ts   = base + timedelta(seconds=offset_seconds)
    return ts.strftime("%Y-%m-%dT%H:%M:%SZ")


def _backup(path: Path) -> Path:
    backup = path.with_suffix(".ttl.bak")
    shutil.copy2(str(path), str(backup))
    return backup


def _find_point_uri(g: Graph, equip_id: str, point_name: str) -> URIRef | None:
    """Find the BACnet point URI by equipment ID + point name."""
    query = f"""
PREFIX cim:    <https://cim.medical/ontology/v3.4#>
PREFIX cim-bn: <https://cim.medical/ontology/v4.0/bacnet#>
SELECT ?point WHERE {{
    ?equip cim:hasEquipmentID "{equip_id}" .
    ?point cim-bn:bacnetPointOf ?equip ;
           cim-bn:hasObjectName "{point_name}" .
}} LIMIT 1
"""
    rows = list(g.query(query))
    return rows[0].point if rows else None


def _find_equip_uri(g: Graph, equip_id: str) -> URIRef | None:
    """Find equipment URI by hasEquipmentID."""
    query = f"""
PREFIX cim: <https://cim.medical/ontology/v3.4#>
SELECT ?equip WHERE {{ ?equip cim:hasEquipmentID "{equip_id}" . }} LIMIT 1
"""
    rows = list(g.query(query))
    return rows[0].equip if rows else None


# ─────────────────────────────────────────────────────────────────────────────
# SimClock
# ─────────────────────────────────────────────────────────────────────────────

class SimClock:
    """
    Controls BAS snapshot state and injects alarm scenarios.
    """

    def __init__(self):
        self._check_baseline()

    def _check_baseline(self):
        missing = []
        for f in [T0_FILE, IFC_FILE, FAS_FILE]:
            if not f.exists():
                missing.append(str(f))
        if missing:
            print("[SimClock] ⚠️  Missing baseline files (OK if running in local workspace):")
            for m in missing:
                print(f"   {m}")

    # ── Inject alarm ──────────────────────────────────────────────────────────

    def inject_alarm(self, snapshot_file: Path, target_key: str) -> bool:
        """
        Inject a smoke alarm into a BAS snapshot file.
        Modifies the existing BACnet binary point's presentValue to true,
        or creates a new binary point if the detector doesn't have one yet.
        """
        if not snapshot_file.exists():
            print(f"[SimClock] ❌ Snapshot not found: {snapshot_file}")
            print(f"           Creating from t0 baseline...")
            if T0_FILE.exists():
                shutil.copy2(str(T0_FILE), str(snapshot_file))
            else:
                print("[SimClock] ❌ No t0 baseline found. Cannot inject.")
                return False

        target = ALARM_TARGETS[target_key]
        equip_id   = target["equip_id"]
        point_name = target["point_name"]

        print(f"\n[SimClock] Injecting alarm → {equip_id} / {point_name}")
        backup = _backup(snapshot_file)
        print(f"           Backup: {backup}")

        g = Graph()
        g.parse(str(snapshot_file), format="turtle")

        # Try to find existing point
        point_uri = _find_point_uri(g, equip_id, point_name)
        equip_uri = _find_equip_uri(g, equip_id)

        if equip_uri is None:
            # Load FAS + IFC to find the equipment URI
            fg = Graph()
            if FAS_FILE.exists():
                fg.parse(str(FAS_FILE), format="turtle")
            if IFC_FILE.exists():
                fg.parse(str(IFC_FILE), format="turtle")
            equip_uri = _find_equip_uri(fg, equip_id)

        if equip_uri is None:
            # Synthesize a URI for the detector
            equip_uri = URIRef(f"https://cim.medical/instance/fas/{equip_id}")
            print(f"[SimClock]   ⚠️  Equipment not found in graph, using synthesized URI")

        if point_uri is None:
            # Create a new BACnet BinaryInput point for this detector
            safe_name  = equip_id.replace("-", "_")
            point_uri  = BAS_INST[f"{safe_name}_SMKDET_BI"]
            point_time = _now_ts(target["delay"])

            print(f"[SimClock]   Creating new BACnet point: {point_uri}")
            g.add((point_uri, RDF.type,                       CIM_BACNET["BACnetBinaryInput"]))
            g.add((point_uri, RDFS.label,
                   Literal(f"{equip_id} Smoke Detector Alarm", lang="en")))
            g.add((point_uri, CIM_BACNET["bacnetPointOf"],    equip_uri))
            g.add((point_uri, CIM_BACNET["hasObjectName"],    Literal(point_name)))
            g.add((point_uri, CIM_BACNET["hasObjectInstance"],Literal(8001, datatype=XSD.integer)))
            g.add((point_uri, CIM_BACNET["hasPresentValue"],  Literal(True, datatype=XSD.boolean)))
            g.add((point_uri, CIM_BACNET["hasStatusFlags"],   Literal("IN-ALARM")))
            g.add((point_uri, CIM_BACNET["readingTimestamp"], Literal(point_time, datatype=XSD.dateTime)))
            g.add((point_uri, CIM_BACNET["hasUnitsID"],       Literal("binary")))
        else:
            # Update existing point presentValue to true
            print(f"[SimClock]   Updating existing point: {point_uri}")
            HAS_PV = CIM_BACNET["hasPresentValue"]
            # Remove old value(s)
            g.remove((point_uri, HAS_PV, None))
            g.add((point_uri, HAS_PV, Literal(True, datatype=XSD.boolean)))
            # Update status flags
            g.remove((point_uri, CIM_BACNET["hasStatusFlags"], None))
            g.add((point_uri, CIM_BACNET["hasStatusFlags"], Literal("IN-ALARM")))

        g.serialize(destination=str(snapshot_file), format="turtle")
        print(f"[SimClock] ✅ Alarm injected → {snapshot_file}")
        return True

    def clear_alarm(self, snapshot_file: Path) -> bool:
        """Clear all smoke alarm points in a snapshot (post-response state)."""
        if not snapshot_file.exists():
            print(f"[SimClock] ❌ Snapshot not found: {snapshot_file}")
            return False

        g = Graph()
        g.parse(str(snapshot_file), format="turtle")

        cleared = 0
        HAS_PV = CIM_BACNET["hasPresentValue"]
        STATUS = CIM_BACNET["hasStatusFlags"]

        for point, _, _ in g.triples((None, RDF.type, CIM_BACNET["BACnetBinaryInput"])):
            # Check if it's an alarm point
            pv_vals = list(g.objects(point, HAS_PV))
            if any(str(v) == "True" or v == Literal(True, datatype=XSD.boolean)
                   for v in pv_vals):
                g.remove((point, HAS_PV, None))
                g.add((point, HAS_PV, Literal(False, datatype=XSD.boolean)))
                g.remove((point, STATUS, None))
                g.add((point, STATUS, Literal("NORMAL")))
                cleared += 1

        g.serialize(destination=str(snapshot_file), format="turtle")
        print(f"[SimClock] ✅ Cleared {cleared} alarm point(s) in {snapshot_file}")
        return True

    # ── Full drill orchestration ──────────────────────────────────────────────

    def run_drill(self):
        """
        Full drill sequence:
          1. Inject SD-F5-001 into t1 (single detector → PENDING)
          2. Inject SD-F5-003 into t1 (dual-zone → auto-CONFIRMED)
          3. Run EventEngine on t1
          4. Clear alarms in t2 (post-response)
        """
        print("=" * 60)
        print("SimClock — Full L2 Fire Drill Simulation")
        print("=" * 60)

        # Step 1: primary alarm
        print("\n[T+00s] Injecting primary alarm: SD-F5-001")
        ok1 = self.inject_alarm(T1_FILE, "t1_primary")

        # Step 2: secondary alarm (dual-zone)
        print("\n[T+30s] Injecting secondary alarm: SD-F5-003 (dual-zone)")
        ok2 = self.inject_alarm(T1_FILE, "t1_secondary")

        if not (ok1 and ok2):
            print("\n[SimClock] ⚠️  One or more injections failed. Proceeding anyway.")

        # Step 3: run EventEngine
        print("\n[T+31s] Running EventEngine on t1 snapshot...")
        try:
            import subprocess
            result = subprocess.run(
                [sys.executable, str(Path(__file__).parent / "event_engine.py"),
                 "--snapshot", "t1"],
                capture_output=True, text=True
            )
            print(result.stdout)
            if result.returncode != 0:
                print(f"[SimClock] ⚠️  EventEngine stderr:\n{result.stderr}")
        except Exception as e:
            print(f"[SimClock] ⚠️  Could not run EventEngine directly: {e}")
            print("         Run manually: python platform/event_engine.py --snapshot t1")

        # Step 4: clear alarms in t2
        if T2_FILE.exists():
            print("\n[T+120s] Advancing to t2: clearing alarm points (post-response)")
            self.clear_alarm(T2_FILE)

        print("\n" + "=" * 60)
        print("Drill complete.")
        print("Next steps:")
        print("  1. Start API:    uvicorn platform.api_mvp_extension:app --reload")
        print("  2. Open browser: platform/frontend/index_mvp.html")
        print("  3. Validate:     python validation/step12_mvp_validation.py")
        print("=" * 60)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="SimClock — BAS snapshot progression")
    group  = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--inject", metavar="SNAPSHOT",
                       help="Inject smoke alarm into snapshot file (t1 or t2)")
    group.add_argument("--clear",  metavar="SNAPSHOT",
                       help="Clear all alarm points in snapshot file")
    group.add_argument("--run-drill", action="store_true",
                       help="Run full L2 fire drill sequence automatically")
    parser.add_argument("--target", default="t1_primary",
                        choices=list(ALARM_TARGETS.keys()),
                        help="Which alarm target to inject (default: t1_primary)")
    args = parser.parse_args()

    clock = SimClock()

    if args.run_drill:
        clock.run_drill()

    elif args.inject:
        snap_map = {"t0": T0_FILE, "t1": T1_FILE, "t2": T2_FILE}
        snap_file = snap_map.get(args.inject)
        if snap_file is None:
            print(f"[ERROR] Unknown snapshot: {args.inject}. Use t0, t1, or t2.")
            sys.exit(1)
        ok = clock.inject_alarm(snap_file, args.target)
        sys.exit(0 if ok else 1)

    elif args.clear:
        snap_map = {"t0": T0_FILE, "t1": T1_FILE, "t2": T2_FILE}
        snap_file = snap_map.get(args.clear)
        if snap_file is None:
            print(f"[ERROR] Unknown snapshot: {args.clear}. Use t0, t1, or t2.")
            sys.exit(1)
        ok = clock.clear_alarm(snap_file)
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
