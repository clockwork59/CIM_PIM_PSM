"""LOD/LOI information completeness validator."""
from typing import List
from rdflib import Graph, RDF, URIRef
from rdflib.namespace import RDFS
from ..core.stage_gate_engine import GapItem, StageConfig
from ..core.namespace_registry import CIM_SPACE, CIM_EQUIP, CIM_D, CIM_C, CIM_MED

# Required properties per entity type per LOD level
LOD_REQUIREMENTS = {
    "OperatingRoom": {
        100: [
            (CIM_D.cleanroomClass, "CRITICAL", "洁净级别", "GB50333-2013 §3"),
            (CIM_D.requiredAreaSqm, "MAJOR", "面积要求", "GB50333-2013 表5.1.1"),
        ],
        200: [
            (CIM_D.airChangesPerHour, "CRITICAL", "换气次数", "GB50333-2013 表6.4.1"),
            (CIM_D.pressureClass, "CRITICAL", "压差类别", "GB50333-2013 §6.5"),
        ],
        300: [
            (CIM_D.minValue, "MAJOR", "温度下限(criterion)", "GB50333-2013 §6.6"),
        ],
    },
    "IntensiveCareUnit": {
        100: [
            (CIM_D.requiredAreaSqm, "MAJOR", "面积要求", "WS435-2013"),
        ],
        200: [
            (CIM_D.airChangesPerHour, "CRITICAL", "换气次数≥12次/h", "WS435-2013 §6"),
            (CIM_D.pressureClass, "CRITICAL", "压差类别（正压）", "WS/T 311"),
        ],
    },
    "Clean_AHU": {
        200: [
            (CIM_D.ratedCapacity, "MAJOR", "额定风量(m³/h)", "ISO 19650 LOD200"),
            (CIM_D.redundancyStrategy, "MAJOR", "冗余配置", "医疗建筑设计规范"),
        ],
        300: [
            (CIM_D.designTag, "MAJOR", "设计位号", "ISO 19650 LOD300"),
            (CIM_D.ratedPower, "MAJOR", "额定功率(kW)", "ISO 19650 LOD300"),
        ],
    },
    "MedicalGasOutlet": {
        200: [
            (CIM_C.hasMedium, "CRITICAL", "介质类型", "WS435-2013"),
        ],
        300: [
            (CIM_D.designTag, "MINOR", "设计位号", "ISO 19650 LOD300"),
        ],
    },
    "UPS": {
        200: [
            (CIM_D.ratedCapacity, "CRITICAL", "额定容量(kVA)", "IEC 60364-7-710"),
            (CIM_D.redundancyStrategy, "CRITICAL", "冗余配置", "医疗建筑电气设计规范"),
        ],
    },
    "IsolatedPowerSystem": {
        200: [
            (CIM_D.designTag, "CRITICAL", "设计位号（IT隔离系统）", "IEC 60364-7-710"),
        ],
    },
    "LiquidOxygenStation": {
        200: [
            (CIM_D.ratedCapacity, "CRITICAL", "额定供气量(L/min)", "WS435-2013"),
            (CIM_D.redundancyStrategy, "CRITICAL", "冗余配置", "WS435-2013 §8"),
        ],
    },
}

# Mapping from ontology class local name to requirement key
CLASS_MAPPING = {
    str(CIM_SPACE.OperatingRoom): "OperatingRoom",
    str(CIM_SPACE.IntensiveCareUnit): "IntensiveCareUnit",
    str(CIM_EQUIP.Clean_AHU): "Clean_AHU",
    str(CIM_EQUIP.MedicalGasOutlet): "MedicalGasOutlet",
    str(CIM_EQUIP.UPS): "UPS",
    str(CIM_EQUIP.IsolatedPowerSystem): "IsolatedPowerSystem",
    str(CIM_EQUIP.LiquidOxygenStation): "LiquidOxygenStation",
}


def check_lod_loi(graph: Graph, abox: Graph, cfg: StageConfig) -> List[GapItem]:
    """Check LOD/LOI completeness of instance data for the given stage."""
    gaps = []
    lod = cfg.lod_level
    gap_counter = [0]

    def next_id(prefix):
        gap_counter[0] += 1
        return f"LOD-{prefix}-{gap_counter[0]:03d}"

    for class_uri, req_key in CLASS_MAPPING.items():
        if req_key not in LOD_REQUIREMENTS:
            continue

        # Find all instances of this class in the ABox
        instances = list(abox.subjects(RDF.type, URIRef(class_uri)))
        if not instances:
            continue

        # Check required properties for each LOD level up to current
        for check_lod, requirements in LOD_REQUIREMENTS[req_key].items():
            if check_lod > lod:
                continue
            for prop, severity, label, std_ref in requirements:
                for inst in instances:
                    has_val = (inst, prop, None) in abox
                    if not has_val:
                        inst_label = _get_label(abox, inst)
                        gaps.append(GapItem(
                            gap_id=next_id("LOD"),
                            severity=severity,
                            category="lod_loi",
                            entity=str(inst),
                            entity_type=req_key,
                            description=f"[LOD{check_lod}] {inst_label} 缺少属性 '{label}' ({prop.split('#')[-1]})",
                            standard_reference=std_ref,
                            bfo_context=f"设计阶段信息制品(GDC)在LOD{check_lod}应包含此属性",
                            remediation=f"为 {inst_label} 添加 cim-d:{prop.split('#')[-1]} 属性",
                            blocking_next_stage=(severity == "CRITICAL"),
                        ))

    return gaps


def _get_label(g: Graph, uri: URIRef) -> str:
    lbl = g.value(uri, RDFS.label)
    if lbl:
        return str(lbl)
    return str(uri).split("#")[-1]
