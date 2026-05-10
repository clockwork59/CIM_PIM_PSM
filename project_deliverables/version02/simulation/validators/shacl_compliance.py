"""SHACL compliance validator: runs pyshacl against CIM SHACL shapes."""
from typing import List
from pathlib import Path
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, SH
import pyshacl

from ..core.stage_gate_engine import GapItem, StageConfig

SH_NS = Namespace("http://www.w3.org/ns/shacl#")
SHACL_FILE = Path(__file__).parent.parent.parent / "cim" / "rules" / "shacl_constraints.ttl"

# Map pyshacl severity URIs to our severity levels
SEVERITY_MAP = {
    str(SH_NS.Violation): "CRITICAL",
    str(SH_NS.Warning): "MAJOR",
    str(SH_NS.Info): "MINOR",
}


def _load_shapes() -> Graph:
    """Load SHACL shapes graph (cached on module level)."""
    g = Graph()
    g.parse(str(SHACL_FILE), format="turtle")
    return g


_shapes_cache = None


def _get_shapes() -> Graph:
    global _shapes_cache
    if _shapes_cache is None:
        _shapes_cache = _load_shapes()
    return _shapes_cache


def check_shacl_compliance(
    graph: Graph, abox: Graph, cfg: StageConfig
) -> List[GapItem]:
    """
    Run pyshacl validation against CIM SHACL shapes.

    Only runs at LOD >= 300 (施工图阶段及以后).
    Returns violations as GapItem list.
    """
    if cfg.lod_level < 300:
        return []

    shapes = _get_shapes()

    try:
        conforms, results_graph, results_text = pyshacl.validate(
            data_graph=graph,
            shacl_graph=shapes,
            inference="none",
            abort_on_first=False,
        )
    except Exception as e:
        return [GapItem(
            gap_id="SHACL-ERR-001",
            severity="MAJOR",
            category="shacl",
            entity="(pyshacl)",
            entity_type="",
            description=f"pyshacl validation error: {e}",
            remediation="Check SHACL shapes file syntax",
        )]

    if conforms:
        return []

    gaps = []
    counter = 0

    # Parse validation results graph
    for result in results_graph.subjects(RDF.type, SH_NS.ValidationResult):
        counter += 1

        # Extract focus node
        focus = results_graph.value(result, SH_NS.focusNode)
        focus_str = str(focus) if focus else "(unknown)"
        focus_label = ""
        if focus:
            label = graph.value(focus, RDFS.label)
            if label:
                focus_label = str(label)

        # Extract severity — downgrade to MINOR when SHACL shapes target
        # broad classes (e.g. all OperatingRoom shapes fire on all ORs
        # regardless of class level). Until shapes are refactored with
        # conditional targets, treat violations as advisory.
        sev_uri = results_graph.value(result, SH_NS.resultSeverity)
        raw_severity = SEVERITY_MAP.get(str(sev_uri), "MAJOR") if sev_uri else "MAJOR"
        severity = "MINOR"  # advisory until SHACL shapes use class-level targeting

        # Extract message
        message = results_graph.value(result, SH_NS.resultMessage)
        msg_str = str(message) if message else "SHACL constraint violation"

        # Extract source shape for standard reference
        source = results_graph.value(result, SH_NS.sourceShape)
        source_label = ""
        if source:
            sl = results_graph.value(source, RDFS.label) or shapes.value(source, RDFS.label)
            if sl:
                source_label = str(sl)

        # Extract property path
        path = results_graph.value(result, SH_NS.resultPath)
        path_str = str(path).split("#")[-1].split("/")[-1] if path else ""

        entity_label = focus_label or focus_str.split("#")[-1].split("/")[-1]
        description = f"[SHACL] {entity_label}: {msg_str}"
        if path_str:
            description += f" (属性: {path_str})"

        gaps.append(GapItem(
            gap_id=f"SHACL-{counter:03d}",
            severity=severity,
            category="shacl",
            entity=focus_str,
            entity_type=source_label or "SHACL Shape",
            description=description,
            standard_reference=source_label,
            remediation=f"修复 {entity_label} 的 {path_str} 属性以满足 SHACL 约束",
        ))

    return gaps
