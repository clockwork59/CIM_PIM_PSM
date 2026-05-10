"""Load CIM ontology TBox into a merged rdflib Graph."""
from pathlib import Path
from rdflib import Graph, ConjunctiveGraph
from .namespace_registry import ALL_NS

ONTOLOGY_FILES = [
    "layer0_foundational.ttl",
    "layer1_conceptual.ttl",
    "layer2_reference.ttl",
    "layer3_design.ttl",
    "layer4_operational.ttl",
    "layer4_control_strategies.ttl",
    "layer4_security_event.ttl",
    "layer4_fas_security.ttl",
    "layer4_cmms.ttl",
    "bridge/bridge_bacnet.ttl",
    "bridge/bridge_brick.ttl",
    "bridge/bridge_ashrae223p.ttl",
    "bridge/bridge_fso.ttl",
    "bridge/bridge_ifc.ttl",
]

_CACHED_TBOX: Graph | None = None


def load_tbox(onto_dir: str | Path, force_reload: bool = False) -> Graph:
    """Parse all CIM ontology TTL files into one merged Graph (TBox)."""
    global _CACHED_TBOX
    if _CACHED_TBOX is not None and not force_reload:
        return _CACHED_TBOX

    onto_dir = Path(onto_dir)
    g = Graph()
    for ns_prefix, ns_uri in ALL_NS.items():
        g.bind(ns_prefix, ns_uri)

    loaded, failed = [], []
    for fname in ONTOLOGY_FILES:
        fpath = onto_dir / fname
        try:
            g.parse(str(fpath), format="turtle")
            loaded.append(fname)
        except Exception as e:
            failed.append((fname, str(e)[:80]))

    if failed:
        print(f"[WARN] {len(failed)} ontology file(s) failed to load:")
        for f, e in failed:
            print(f"       {f}: {e}")

    print(f"[INFO] TBox loaded: {len(loaded)} files, {len(g):,} triples")
    _CACHED_TBOX = g
    return g


def load_scenario(scenario_path: str | Path) -> Graph:
    """Parse a scenario TTL (ABox) into a separate Graph."""
    g = Graph()
    for ns_prefix, ns_uri in ALL_NS.items():
        g.bind(ns_prefix, ns_uri)
    g.parse(str(scenario_path), format="turtle")
    print(f"[INFO] Scenario loaded: {len(g):,} triples from {Path(scenario_path).name}")
    return g


def make_query_graph(tbox: Graph, abox: Graph) -> Graph:
    """Union TBox + ABox into a single graph for SPARQL queries."""
    merged = Graph()
    for ns_prefix, ns_uri in ALL_NS.items():
        merged.bind(ns_prefix, ns_uri)
    for triple in tbox:
        merged.add(triple)
    for triple in abox:
        merged.add(triple)
    return merged
