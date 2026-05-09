"""BFO prerequisite checker: validates lifecycle process ordering and milestone existence."""
from typing import List
from rdflib import Graph, RDF, URIRef
from rdflib.namespace import RDFS
from ..core.stage_gate_engine import GapItem, StageConfig
from ..core.namespace_registry import CIM_F

# Required process types per stage (must be instantiated)
STAGE_PROCESS_REQS = {
    1: [(CIM_F.ConceptualDesignProcess, "方案设计过程", "MAJOR")],
    2: [(CIM_F.SchematicDesignProcess, "初步设计过程", "MAJOR")],
    3: [(CIM_F.DetailedDesignProcess, "施工图设计过程", "MAJOR"),
        (CIM_F.InformationDeliveryMilestone, "信息交付里程碑", "MAJOR")],
    4: [(CIM_F.TenderingProcess, "招投标过程", "MINOR")],
    5: [(CIM_F.ConstructionProcess, "施工过程", "MAJOR"),
        (CIM_F.ConstructionCompletionMilestone, "竣工验收里程碑", "MAJOR")],
    6: [(CIM_F.CommissioningProcess, "调试验收过程", "CRITICAL"),
        (CIM_F.HandoverMilestone, "移交里程碑", "CRITICAL"),
        (CIM_F.MedicalGasValidationProcess, "医用气体验证过程", "CRITICAL"),
        (CIM_F.CleanroomQualificationProcess, "洁净室验收过程", "CRITICAL")],
}


def check_bfo_prereqs(graph: Graph, abox: Graph, cfg: StageConfig) -> List[GapItem]:
    """Check BFO process instances and temporal ordering in the ABox."""
    gaps = []
    gap_counter = [0]

    def next_id():
        gap_counter[0] += 1
        return f"BFO-{gap_counter[0]:03d}"

    reqs = STAGE_PROCESS_REQS.get(cfg.stage_id, [])
    for process_class, label, severity in reqs:
        instances = list(abox.subjects(RDF.type, process_class))
        if not instances:
            gaps.append(GapItem(
                gap_id=next_id(),
                severity=severity,
                category="bfo_prereq",
                entity=str(process_class),
                entity_type="FacilityLifecycleProcess",
                description=f"[阶段{cfg.stage_id}] 缺少 {label} 过程实例 ({process_class.split('#')[-1]})",
                standard_reference="ISO 19650-2 §5 — 信息管理过程需显式声明",
                bfo_context="BFO:Process 实例未声明——无法验证过程时序约束",
                remediation=(
                    f"在场景数据中添加:\n"
                    f"  :YourProcess a cim-f:{process_class.split('#')[-1]} ;\n"
                    f"      cim-f:processStageCode '...' ;\n"
                    f"      cim-f:processStartDate 'YYYY-MM-DD'^^xsd:date ."
                ),
                blocking_next_stage=(severity == "CRITICAL"),
            ))

    # Check temporallyPrecedes chain for lifecycle processes
    if cfg.stage_id >= 2:
        _check_temporal_chain(abox, gaps, next_id, cfg)

    return gaps


def _check_temporal_chain(abox: Graph, gaps: List[GapItem], next_id, cfg: StageConfig):
    """Verify that declared processes have proper temporal ordering."""
    PRECEDES = CIM_F.temporallyPrecedes

    # Collect all lifecycle process instances
    lc_instances = []
    for cls in [
        CIM_F.ConceptualDesignProcess, CIM_F.SchematicDesignProcess,
        CIM_F.DetailedDesignProcess, CIM_F.TenderingProcess,
        CIM_F.ConstructionProcess, CIM_F.CommissioningProcess,
    ]:
        lc_instances.extend(list(abox.subjects(RDF.type, cls)))

    if len(lc_instances) < 2:
        return  # Not enough instances to check ordering

    # Check that there's at least one temporallyPrecedes relation
    precedes_triples = list(abox.triples((None, PRECEDES, None)))
    if len(lc_instances) >= 2 and not precedes_triples:
        gaps.append(GapItem(
            gap_id=next_id(),
            severity="MINOR",
            category="bfo_prereq",
            entity="(project)",
            entity_type="FacilityLifecycleProcess",
            description=(
                f"声明了 {len(lc_instances)} 个生命周期过程实例，"
                f"但未发现 cim-f:temporallyPrecedes 时序关系"
            ),
            standard_reference="ISO 19650 — 过程阶段应有明确的时序依赖",
            bfo_context="BFO:Process 实例间缺少 temporallyPrecedes 关系，推理器无法验证过程顺序",
            remediation="添加: :ProcessA cim-f:temporallyPrecedes :ProcessB .",
            blocking_next_stage=False,
        ))
