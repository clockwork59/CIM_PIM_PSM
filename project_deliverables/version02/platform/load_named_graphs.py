#!/usr/bin/env python3
"""
Load CIM TBox and ABox into Named Graphs for TripleStore or local query.

Usage:
    python load_named_graphs.py [--serialize nquads|trig] [--output PATH]

Named Graph layout:
    tbox   — All ontology/*.ttl + ontology/bridge/*.ttl (TBox schema)
    ifc    — abox/nbu_medical_clinic_instances.ttl  (IFC-derived ABox)
    pset   — abox/nbu_pset_enrichment.ttl           (IFC Pset quantities)
    bas_t0 — abox/nbu_bas_readings_t0.ttl           (BAS snapshot T0)
    bas_t1 — abox/nbu_bas_readings_t1.ttl           (BAS snapshot T1)
    bas_t2 — abox/nbu_bas_readings_t2.ttl           (BAS snapshot T2)
    cmms   — abox/nbu_cmms_workorders.ttl           (CMMS work orders)
    event  — scenario/smoke_alarm_drill.ttl         (optional event scenario)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rdflib import ConjunctiveGraph, URIRef

# ---------------------------------------------------------------------------
# Named-graph URIs
# ---------------------------------------------------------------------------
GRAPH_URIS = {
    "tbox":   "https://cim.medical/graph/tbox",
    "ifc":    "https://cim.medical/graph/ifc",
    "pset":   "https://cim.medical/graph/pset",
    "bas_t0": "https://cim.medical/graph/bas/2026-05-10T08:00",
    "bas_t1": "https://cim.medical/graph/bas/2026-05-10T16:00",
    "bas_t2": "https://cim.medical/graph/bas/2026-05-11T00:00",
    "cmms":   "https://cim.medical/graph/cmms/2026-05",
    "event":  "https://cim.medical/graph/event",
    "fas":    "https://cim.medical/graph/fas",
}

# ---------------------------------------------------------------------------
# Directory layout
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent / "cim"
ONTOLOGY_DIR = BASE_DIR / "ontology"
BRIDGE_DIR   = ONTOLOGY_DIR / "bridge"
ABOX_DIR     = BASE_DIR / "abox"
SCENARIO_DIR = Path(__file__).resolve().parent.parent / "simulation" / "scenario"

# Map graph keys to file sources
FILE_MAP: dict[str, list[Path]] = {
    "ifc":    [ABOX_DIR / "nbu_medical_clinic_instances.ttl"],
    "pset":   [ABOX_DIR / "nbu_pset_enrichment.ttl"],
    "bas_t0": [ABOX_DIR / "nbu_bas_readings_t0.ttl"],
    "bas_t1": [ABOX_DIR / "nbu_bas_readings_t1.ttl"],
    "bas_t2": [ABOX_DIR / "nbu_bas_readings_t2.ttl"],
    "cmms":   [ABOX_DIR / "nbu_cmms_workorders.ttl"],
    "event":  [SCENARIO_DIR / "smoke_alarm_drill.ttl"],
    "fas":    [ABOX_DIR / "nbu_fas_instances.ttl"],
}


def _collect_tbox_files() -> list[Path]:
    """Gather all .ttl files from the ontology and bridge directories."""
    files: list[Path] = []
    if ONTOLOGY_DIR.exists():
        files.extend(sorted(ONTOLOGY_DIR.glob("*.ttl")))
    if BRIDGE_DIR.exists():
        files.extend(sorted(BRIDGE_DIR.glob("*.ttl")))
    return files


def load_named_graphs(*, verbose: bool = True) -> ConjunctiveGraph:
    """Load all TTL sources into a ConjunctiveGraph with named graphs."""
    cg = ConjunctiveGraph()

    # --- TBox (multiple files merged into one named graph) ---
    tbox_uri = URIRef(GRAPH_URIS["tbox"])
    tbox_graph = cg.get_context(tbox_uri)
    tbox_files = _collect_tbox_files()
    for ttl in tbox_files:
        if ttl.exists():
            tbox_graph.parse(str(ttl), format="turtle")
    if verbose:
        print(f"[tbox]   {len(tbox_graph):>6} triples  ({len(tbox_files)} files)")

    # --- ABox / event named graphs ---
    for key, files in FILE_MAP.items():
        graph_uri = URIRef(GRAPH_URIS[key])
        g = cg.get_context(graph_uri)
        loaded = False
        for ttl in files:
            if ttl.exists():
                g.parse(str(ttl), format="turtle")
                loaded = True
            elif verbose:
                print(f"[{key:6s}] SKIP (file not found: {ttl.name})")
        if loaded and verbose:
            print(f"[{key:6s}] {len(g):>6} triples")

    # --- Summary ---
    total = sum(len(cg.get_context(URIRef(u))) for u in GRAPH_URIS.values())
    if verbose:
        print(f"\n{'='*50}")
        print(f"Total triples across all named graphs: {total}")
        print(f"Named graphs loaded: {len(GRAPH_URIS)}")
        print(f"Quads in ConjunctiveGraph:             {len(cg)}")

    return cg


def serialize_output(cg: ConjunctiveGraph, fmt: str, output: Path) -> None:
    """Serialize the ConjunctiveGraph to a file."""
    fmt_map = {"nquads": "nquads", "trig": "trig"}
    rdf_fmt = fmt_map.get(fmt, "nquads")
    ext_map = {"nquads": ".nq", "trig": ".trig"}
    ext = ext_map.get(fmt, ".nq")

    out_path = output / f"cim_all_graphs{ext}"
    data = cg.serialize(format=rdf_fmt)
    out_path.write_text(data, encoding="utf-8")
    print(f"\nSerialized to: {out_path}  ({out_path.stat().st_size / 1024:.1f} KB)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Load CIM Named Graphs")
    parser.add_argument(
        "--serialize", choices=["nquads", "trig"], default=None,
        help="Serialize ConjunctiveGraph to file (nquads or trig)",
    )
    parser.add_argument(
        "--output", type=Path,
        default=Path(__file__).resolve().parent / "output",
        help="Output directory for serialized file",
    )
    args = parser.parse_args()

    cg = load_named_graphs()

    if args.serialize:
        args.output.mkdir(parents=True, exist_ok=True)
        serialize_output(cg, args.serialize, args.output)

    print("\nDone.")


if __name__ == "__main__":
    main()
