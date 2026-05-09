"""Flow topology validator: supply/return balance, terminal coverage, orphan detection."""
from typing import List, Set, Dict
from rdflib import Graph, RDF, URIRef
from rdflib.namespace import RDFS
from ..core.stage_gate_engine import GapItem, StageConfig
from ..core.namespace_registry import CIM_SPACE, CIM_EQUIP, CIM_FLOW, CIM_C, CIM_MED

# Minimum medical gas outlets per OR per medium type (WS 435-2013)
MIN_GAS_OUTLETS = {
    str(CIM_MED.Oxygen): 2,
    str(CIM_MED.MedicalVacuum): 2,
    str(CIM_MED.MedicalAir): 2,
}
OUTLET_LABELS = {
    str(CIM_MED.Oxygen): "O₂氧气终端",
    str(CIM_MED.MedicalVacuum): "VAC负压终端",
    str(CIM_MED.MedicalAir): "CAIR医用空气终端",
}


def check_flow_topology(graph: Graph, abox: Graph, cfg: StageConfig) -> List[GapItem]:
    """Validate flow network topology in the ABox."""
    gaps = []
    gap_counter = [0]

    def next_id(prefix):
        gap_counter[0] += 1
        return f"FLOW-{prefix}-{gap_counter[0]:03d}"

    if cfg.lod_level < 200:
        return gaps  # Topology checks only from LOD 200 onwards

    # --- Check 1: Each OR must have at least one supply air terminal ---
    or_instances = list(abox.subjects(RDF.type, CIM_SPACE.OperatingRoom))
    for or_uri in or_instances:
        or_label = _get_label(abox, or_uri)
        # Find equipment locatedIn this OR with SupplyAir inlet
        supply_terminals = list(abox.subjects(CIM_SPACE.locatedIn, or_uri))
        has_supply = False
        for term in supply_terminals:
            # Check if it has a connection point with SupplyAir medium
            for cp in abox.objects(term, CIM_C.hasConnectionPoint):
                medium = abox.value(cp, CIM_C.hasMedium)
                if medium and str(medium) == str(CIM_MED.SupplyAir):
                    has_supply = True
                    break
            if has_supply:
                break
        if not has_supply:
            gaps.append(GapItem(
                gap_id=next_id("SA"),
                severity="CRITICAL",
                category="flow_topology",
                entity=str(or_uri),
                entity_type="OperatingRoom",
                description=f"{or_label}: 无送风终端装置（未找到 locatedIn 此空间的送风末端）",
                standard_reference="GB50333-2013 §6.4 — 洁净手术室必须设置送风系统",
                bfo_context="cim-f:AirFlowProcess 无法在此空间中发生——缺少连接至该空间的 FlowPath 终端",
                remediation=f"为 {or_label} 添加高效送风口实例并设置 cim-space:locatedIn",
                blocking_next_stage=True,
            ))

    # --- Check 2: Medical gas terminal coverage per OR ---
    for or_uri in or_instances:
        or_label = _get_label(abox, or_uri)
        or_clean_class = abox.value(or_uri, URIRef("https://cim.medical/ontology/v4.0/design#cleanroomClass"))

        # Find all MedicalGasOutlet in this OR
        outlets_in_or = [
            eq for eq in abox.subjects(CIM_SPACE.locatedIn, or_uri)
            if (eq, RDF.type, CIM_EQUIP.MedicalGasOutlet) in abox
        ]

        for medium_uri, min_count in MIN_GAS_OUTLETS.items():
            count = sum(
                1 for o in outlets_in_or
                if str(abox.value(o, CIM_C.hasMedium)) == medium_uri
            )
            if count < min_count:
                label = OUTLET_LABELS.get(medium_uri, medium_uri.split("#")[-1])
                gaps.append(GapItem(
                    gap_id=next_id("MG"),
                    severity="CRITICAL",
                    category="flow_topology",
                    entity=str(or_uri),
                    entity_type="OperatingRoom",
                    description=(
                        f"{or_label}: {label} 数量不足 — "
                        f"当前 {count} 个，要求 ≥ {min_count} 个"
                    ),
                    standard_reference="WS 435-2013 §7.2 — 每间手术室最低配置",
                    bfo_context="cim-f:MedicalGasFlowProcess 无法服务此空间——终端数量不满足最低要求",
                    remediation=(
                        f"为 {or_label} 添加 {min_count - count} 个 "
                        f"{label} (cim-equip:MedicalGasOutlet, cim-c:hasMedium {medium_uri.split('#')[-1]})"
                    ),
                    blocking_next_stage=True,
                ))

    # --- Check 3: Each OR must have an IT isolated power panel ---
    IT_CLASSES = [CIM_EQUIP.IsolatedPowerSystem]
    for or_uri in or_instances:
        or_label = _get_label(abox, or_uri)
        has_it = any(
            (eq, RDF.type, cls) in abox
            for eq in abox.subjects(CIM_SPACE.locatedIn, or_uri)
            for cls in IT_CLASSES
        )
        if not has_it:
            gaps.append(GapItem(
                gap_id=next_id("IT"),
                severity="CRITICAL",
                category="flow_topology",
                entity=str(or_uri),
                entity_type="OperatingRoom",
                description=f"{or_label}: 缺少 IT 隔离电源系统（IsolatedPowerSystem）",
                standard_reference="IEC 60364-7-710 §710.413 — 医疗 2 类场所强制要求",
                bfo_context="cim-f:ElectricalFlowProcess (应急电源回路) 未到达此手术室",
                remediation=f"为 {or_label} 添加 cim-equip:IsolatedPowerSystem 并通过 EmergencyPower FlowPath 连接至 UPS",
                blocking_next_stage=True,
            ))

    # --- Check 4: Orphaned equipment (has ConnectionPoint but no connections) ---
    if cfg.lod_level >= 300:
        all_equip = list(abox.subjects(RDF.type, None))
        for eq in all_equip:
            eq_types = list(abox.objects(eq, RDF.type))
            is_equip = any(
                str(t).startswith("https://cim.medical/ontology/v3.4/equipment#")
                for t in eq_types
            )
            if not is_equip:
                continue
            cps = list(abox.objects(eq, CIM_C.hasConnectionPoint))
            if not cps:
                continue
            has_any_conn = any(
                abox.value(cp, CIM_C.connectsTo) is not None
                for cp in cps
            )
            if not has_any_conn:
                eq_label = _get_label(abox, eq)
                gaps.append(GapItem(
                    gap_id=next_id("ORF"),
                    severity="MINOR",
                    category="flow_topology",
                    entity=str(eq),
                    entity_type="Equipment",
                    description=f"{eq_label}: 孤立设备——具有连接点但无 cim-c:connectsTo 连接",
                    standard_reference="ISO 19650 LOD300 — 所有连接点应建立连接关系",
                    bfo_context="此设备无法参与任何 FlowProcess（孤立持续体）",
                    remediation=f"为 {eq_label} 的连接点添加 cim-c:connectsTo 关联到对应 FlowPath",
                    blocking_next_stage=False,
                ))

    return gaps


def _get_label(g: Graph, uri) -> str:
    lbl = g.value(uri, RDFS.label)
    if lbl:
        return str(lbl)
    return str(uri).split("#")[-1]
