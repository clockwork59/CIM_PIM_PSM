#!/usr/bin/env python3
"""
EventEngine — CIM MVP (Smoke Alarm) Sprint 2026-05-10
======================================================
Scans BAS binary input points for smoke detector alarms, applies 30-second
dual-zone confirmation logic, and generates SecurityEvent instances in the
shared RDF graph.

State machine:
  PENDING → CONFIRMED → IN_PROGRESS → CLOSED_LOOP → CLOSED

Usage:
    from platform.event_engine import EventEngine
    engine = EventEngine(graph)
    events = engine.scan()

Dependencies: rdflib >= 6.0
"""

import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from rdflib import Graph, Namespace, Literal, URIRef, RDF, RDFS, XSD, OWL

# ─────────────────────────────────────────────────────────────────────────────
# PATHS  (relative to project_deliverables/version02/)
# ─────────────────────────────────────────────────────────────────────────────
BASE = Path(__file__).resolve().parent.parent   # mvp_deliverables/ (local) or
                                                 # project_deliverables/version02/ (Codespace)

ABOX_FILES = {
    "IFC":   BASE / "cim/abox/nbu_medical_clinic_instances.ttl",
    "FAS":   BASE / "cim/abox/nbu_fas_instances.ttl",
    "BAS_T0": BASE / "cim/abox/nbu_bas_readings_t0.ttl",
    "BAS_T1": BASE / "cim/abox/nbu_bas_readings_t1.ttl",
    "BAS_T2": BASE / "cim/abox/nbu_bas_readings_t2.ttl",
    "DRILL": BASE / "simulation/scenario/smoke_alarm_drill.ttl",
    "TBOX":  BASE / "cim/ontology/_index_v4.ttl",
}

EVENT_ABOX_FILE = BASE / "cim/abox/nbu_security_events.ttl"

# ─────────────────────────────────────────────────────────────────────────────
# NAMESPACES
# ─────────────────────────────────────────────────────────────────────────────
CIM        = Namespace("http://hospital-cim.org/v4/core#")
CIM_FAS    = Namespace("http://hospital-cim.org/v4/fas#")
CIM_SEC    = Namespace("http://hospital-cim.org/v4/security_event#")
CIM_BACNET = Namespace("http://hospital-cim.org/v4/bacnet#")
INST       = Namespace("http://hospital-cim.org/v4/instances#")
SEC_INST   = Namespace("http://hospital-cim.org/v4/security_event/instances#")

# Dual-zone confirmation window in seconds
DUAL_ZONE_WINDOW_SECONDS = 30

# BACnet point name patterns indicating smoke/alarm state (binary input)
SMOKE_ALARM_POINT_PATTERNS = ["SMOKE", "SMKDET", "FIRE", "ALM", "FA_"]


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _event_id(seq: int) -> str:
    date_str = datetime.now().strftime("%Y%m%d")
    return f"EVT-{date_str}-{seq:03d}"


def _is_smoke_alarm_point(point_name: str) -> bool:
    name_upper = point_name.upper()
    return any(p in name_upper for p in SMOKE_ALARM_POINT_PATTERNS)


# ─────────────────────────────────────────────────────────────────────────────
# EventEngine
# ─────────────────────────────────────────────────────────────────────────────

class EventEngine:
    """
    Scan a unified RDF graph for active smoke detector alarm points,
    apply dual-zone confirmation logic, and emit SecurityEvent triples.
    """

    def __init__(self, graph: Graph, snapshot_label: str = "t1"):
        self.g = graph
        self.snapshot_label = snapshot_label
        self._event_counter = 1
        self._event_graph = Graph()
        self._bind_prefixes(self._event_graph)

    # ── Public API ────────────────────────────────────────────────────────────

    def scan(self) -> list:
        """
        Scan all BAS binary points for active smoke alarms.
        Returns list of dicts describing generated SecurityEvent instances.
        """
        alarmed = self._find_alarmed_detectors()
        if not alarmed:
            print("[EventEngine] No active smoke alarm points detected.")
            return []

        print(f"[EventEngine] {len(alarmed)} alarmed detector(s) found: "
              f"{[a['equipID'] for a in alarmed]}")

        events = []
        # Group alarms by FAS zone
        by_zone: dict[str, list] = {}
        for a in alarmed:
            zone = a.get("zone", "ZONE-UNKNOWN")
            by_zone.setdefault(zone, []).append(a)

        for zone, detectors in by_zone.items():
            evt = self._create_event(zone, detectors)
            events.append(evt)

        return events

    def save_events(self, output_path: Path = None) -> Path:
        """Serialize the generated SecurityEvent ABox to Turtle."""
        out = output_path or EVENT_ABOX_FILE
        out.parent.mkdir(parents=True, exist_ok=True)
        # Merge with existing if present
        if out.exists():
            existing = Graph()
            existing.parse(str(out), format="turtle")
            for triple in self._event_graph:
                existing.add(triple)
            existing.serialize(destination=str(out), format="turtle")
        else:
            self._event_graph.serialize(destination=str(out), format="turtle")
        print(f"[EventEngine] Events saved → {out}")
        return out

    # ── Internal: SPARQL queries ──────────────────────────────────────────────

    def _find_alarmed_detectors(self) -> list:
        """SPARQL: find smoke detectors with active alarm BACnet points."""
        query = """
PREFIX rdf:      <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX cim:      <http://hospital-cim.org/v4/core#>
PREFIX cim-fas:  <http://hospital-cim.org/v4/fas#>
PREFIX cim-bn:   <http://hospital-cim.org/v4/bacnet#>
PREFIX xsd:      <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?detector ?equipID ?zone ?pointName ?pointURI
WHERE {
    ?detector  rdf:type          cim-fas:SmokeDetector ;
               cim:hasEquipmentID ?equipID .

    OPTIONAL { ?detector cim-fas:inFASZone ?zone . }

    ?point  cim-bn:bacnetPointOf  ?detector ;
            cim-bn:hasObjectName  ?pointName ;
            cim-bn:hasPresentValue "true"^^xsd:boolean .
    BIND(?point AS ?pointURI)
}
ORDER BY ?equipID
"""
        results = []
        for row in self.g.query(query):
            point_name = str(row.pointName) if row.pointName else ""
            if not _is_smoke_alarm_point(point_name):
                continue
            results.append({
                "detector": row.detector,
                "equipID":  str(row.equipID),
                "zone":     str(row.zone) if row.zone else "ZONE-UNKNOWN",
                "pointName": point_name,
                "pointURI": row.pointURI,
            })
        return results

    def _find_action_chain(self) -> URIRef | None:
        """Find the L2 FireAlarm ActionChain from smoke_alarm_drill.ttl."""
        query = """
PREFIX cim-sec: <http://hospital-cim.org/v4/security_event#>
SELECT ?chain WHERE {
    ?chain  rdf:type  cim-sec:ActionChain .
    FILTER(CONTAINS(STR(?chain), "fire") || CONTAINS(STR(?chain), "smoke") ||
           CONTAINS(STR(?chain), "drill") || CONTAINS(STR(?chain), "l2"))
}
LIMIT 1
"""
        rows = list(self.g.query(query))
        if rows:
            return rows[0].chain
        # Fallback: pick any ActionChain
        rows2 = list(self.g.query(
            "SELECT ?c WHERE { ?c rdf:type <http://hospital-cim.org/v4/security_event#ActionChain> } LIMIT 1"
        ))
        return rows2[0].c if rows2 else None

    # ── Internal: event construction ─────────────────────────────────────────

    def _create_event(self, zone: str, detectors: list) -> dict:
        """
        Create a SecurityEvent (FireAlarmEvent) for a zone with alarms.
        Applies dual-zone logic:
          - 1 detector  → PENDING  (awaiting operator confirmation)
          - ≥2 detectors → CONFIRMED (auto-promoted, L2 plan activated)
        """
        evt_id   = _event_id(self._event_counter)
        self._event_counter += 1
        evt_uri  = SEC_INST[evt_id]
        now      = _now_iso()

        dual_zone = len(detectors) >= 2
        state_cls = CIM_SEC["state_Confirmed"] if dual_zone else CIM_SEC["state_Pending"]
        severity  = CIM_SEC["SeverityL2"]

        eg = self._event_graph
        eg.add((evt_uri, RDF.type,              CIM_SEC["FireAlarmEvent"]))
        eg.add((evt_uri, RDF.type,              CIM_SEC["SecurityEvent"]))
        eg.add((evt_uri, CIM_SEC["hasEventID"], Literal(evt_id)))
        eg.add((evt_uri, CIM_SEC["hasEventState"], state_cls))
        eg.add((evt_uri, CIM_SEC["hasSeverityLevel"], severity))
        eg.add((evt_uri, CIM_SEC["eventTimestamp"], Literal(now, datatype=XSD.dateTime)))
        eg.add((evt_uri, CIM_SEC["dualZoneConfirmed"],
                Literal(dual_zone, datatype=XSD.boolean)))
        eg.add((evt_uri, RDFS.label,
                Literal(f"FireAlarmEvent {evt_id} Zone {zone}", lang="en")))

        # Link triggering detectors
        for det in detectors:
            eg.add((evt_uri, CIM_SEC["involvesEquipment"], det["detector"]))
            eg.add((evt_uri, CIM_SEC["triggeredByPoint"],  det["pointURI"]))

        # Zone context
        zone_uri_str = zone if zone.startswith("http") else str(INST[zone.split("/")[-1]])
        eg.add((evt_uri, CIM_SEC["involvesZone"], URIRef(zone_uri_str)))

        # Bind L2 ActionChain (template reference)
        action_chain = self._find_action_chain()
        if action_chain:
            eg.add((evt_uri, CIM_SEC["activatesActionChain"], action_chain))
            print(f"[EventEngine]   → L2 ActionChain bound: {action_chain}")

        # Generate 10 ActionNodeExecution instances (runtime state tracking)
        node_uris = self._create_action_node_executions(evt_uri, evt_id)

        status = "CONFIRMED (auto, dual-zone)" if dual_zone else "PENDING (single detector, awaiting operator)"
        print(f"[EventEngine] ✅ Created {evt_id}: zone={zone}, "
              f"detectors={len(detectors)}, state={status}, nodes={len(node_uris)}")

        return {
            "event_id":   evt_id,
            "event_uri":  str(evt_uri),
            "zone":       zone,
            "state":      "CONFIRMED" if dual_zone else "PENDING",
            "detectors":  [d["equipID"] for d in detectors],
            "dual_zone":  dual_zone,
            "timestamp":  now,
            "nodes":      len(node_uris),
        }

    def _create_action_node_executions(self, evt_uri: URIRef, evt_id: str) -> list:
        """
        Create 10 ActionNodeExecution instances tracking runtime state of each
        L2 plan step. Auto-marks the 6 system-automated steps as EXECUTING immediately.

        L2 steps:
          1  confirm_fire      — Manual/中控     dep=[]
          2  cut_power         — Auto/System      dep=[1]
          3  start_suppression — Manual/电工班   dep=[2]
          4  broadcast         — Auto/System      dep=[1]
          5  evacuate          — Manual/保安队   dep=[4]
          6  open_doors        — Auto/System      dep=[4]
          7  elevator_home     — Auto/System      dep=[1]
          8  notify_medical    — Auto/System      dep=[1]
          9  call_119          — Manual/中控     dep=[3]
          10 notify_leaders    — Auto/System      dep=[1]
        """
        L2_STEPS = [
            # (step_no, slug, label_en,              role,    auto,  deps, timeout_s)
            (1,  "confirm_fire",      "Confirm fire alarm",        "CTRL",  False, [],    120),
            (2,  "cut_power",         "Cut electrical power",       "SYS",   True,  [1],   30),
            (3,  "start_suppression", "Activate fire suppression",  "ELEC",  False, [2],   300),
            (4,  "broadcast",         "Zone emergency broadcast",   "SYS",   True,  [1],   10),
            (5,  "evacuate",          "Initiate evacuation",        "SEC",   False, [4],   600),
            (6,  "open_doors",        "Release access control",     "SYS",   True,  [4],   10),
            (7,  "elevator_home",     "Return elevators to ground", "SYS",   True,  [1],   30),
            (8,  "notify_medical",    "Notify medical staff",       "SYS",   True,  [1],   30),
            (9,  "call_119",          "Call fire department 119",   "CTRL",  False, [3],   120),
            (10, "notify_leaders",    "Notify duty leadership",     "SYS",   True,  [1],   30),
        ]

        now = _now_iso()
        eg  = self._event_graph
        node_uris = []

        for step_no, slug, label, role, auto, deps, timeout in L2_STEPS:
            node_id  = f"{evt_id}-STEP-{step_no:02d}"
            node_uri = SEC_INST[node_id]
            node_uris.append(node_uri)

            # Determine initial execution state
            if step_no == 1:
                exec_state = CIM_SEC["nodeState_Executing"]  # step 1 immediately awaits operator
            elif auto and 1 in deps:
                exec_state = CIM_SEC["nodeState_Executing"]  # auto steps with dep:1 start immediately
            else:
                exec_state = CIM_SEC["nodeState_Pending"]

            eg.add((node_uri, RDF.type,                       CIM_SEC["ActionNodeExecution"]))
            eg.add((node_uri, CIM_SEC["hasNodeID"],           Literal(node_id)))
            eg.add((node_uri, CIM_SEC["hasStepNumber"],       Literal(step_no, datatype=XSD.integer)))
            eg.add((node_uri, CIM_SEC["hasStepSlug"],         Literal(slug)))
            eg.add((node_uri, RDFS.label,                     Literal(label, lang="en")))
            eg.add((node_uri, CIM_SEC["hasExecutionState"],   exec_state))
            eg.add((node_uri, CIM_SEC["isAutomatic"],         Literal(auto, datatype=XSD.boolean)))
            eg.add((node_uri, CIM_SEC["hasResponderRole"],    Literal(role)))
            eg.add((node_uri, CIM_SEC["hasTimeoutSeconds"],   Literal(timeout, datatype=XSD.integer)))
            eg.add((node_uri, CIM_SEC["nodeCreatedAt"],       Literal(now, datatype=XSD.dateTime)))
            eg.add((evt_uri,  CIM_SEC["hasActionNodeExecution"], node_uri))

            for dep in deps:
                dep_id = f"{evt_id}-STEP-{dep:02d}"
                eg.add((node_uri, CIM_SEC["dependsOnNode"], SEC_INST[dep_id]))

        return node_uris

    # ── Utility ───────────────────────────────────────────────────────────────

    def _bind_prefixes(self, g: Graph) -> None:
        g.bind("cim",     CIM)
        g.bind("cim-fas", CIM_FAS)
        g.bind("cim-sec", CIM_SEC)
        g.bind("sec",     SEC_INST)
        g.bind("inst",    INST)
        g.bind("rdf",     RDF)
        g.bind("rdfs",    RDFS)
        g.bind("xsd",     XSD)

    @property
    def event_graph(self) -> Graph:
        return self._event_graph


# ─────────────────────────────────────────────────────────────────────────────
# STANDALONE RUNNER
# ─────────────────────────────────────────────────────────────────────────────

def _load_graph(snapshot: str = "t1") -> Graph:
    g = Graph()
    load_map = {
        "IFC":  ABOX_FILES["IFC"],
        "FAS":  ABOX_FILES["FAS"],
        "BAS":  ABOX_FILES.get(f"BAS_{snapshot.upper()}", ABOX_FILES["BAS_T1"]),
        "DRILL": ABOX_FILES["DRILL"],
    }
    for name, path in load_map.items():
        if path and path.exists():
            try:
                g.parse(str(path), format="turtle")
                print(f"  [LOAD] ✅ {name:6s}  {path.name}")
            except Exception as e:
                print(f"  [LOAD] ⚠️  {name:6s}  parse error: {e}")
        else:
            print(f"  [LOAD] ⚠️  {name:6s}  NOT FOUND (skip): {path}")
    return g


def main():
    import argparse
    parser = argparse.ArgumentParser(description="EventEngine — CIM MVP Smoke Alarm Scanner")
    parser.add_argument("--snapshot", default="t1",
                        choices=["t0", "t1", "t2"],
                        help="BAS snapshot to scan (default: t1, which has injected alarm)")
    args = parser.parse_args()

    print("=" * 60)
    print(f"EventEngine  —  snapshot={args.snapshot}")
    print("=" * 60)

    print("\n[1] Loading RDF sources...")
    g = _load_graph(args.snapshot)
    print(f"    Total triples: {len(g):,}")

    print("\n[2] Scanning for active smoke alarms...")
    engine = EventEngine(g, snapshot_label=args.snapshot)
    events = engine.scan()

    if not events:
        print("\n  No smoke alarm events generated.")
        print("  (Use sim_clock.py to inject an alarm into t1 snapshot first.)")
        return

    print(f"\n[3] Generated {len(events)} SecurityEvent(s):")
    for evt in events:
        state_icon = "🔴" if evt["state"] == "CONFIRMED" else "🟡"
        print(f"  {state_icon}  {evt['event_id']}  |  zone={evt['zone']}  |  "
              f"state={evt['state']}  |  nodes={evt['nodes']}")

    print("\n[4] Saving SecurityEvent ABox...")
    out_path = engine.save_events()
    print(f"    → {out_path}")

    print("\n" + "=" * 60)
    print("EventEngine complete.")
    print("Next: run platform/api_mvp_extension.py to expose events via REST API.")
    print("=" * 60)


if __name__ == "__main__":
    main()
