"""Stage-gate simulation engine: drives lifecycle stage progression."""
from dataclasses import dataclass, field
from typing import List, Optional
from rdflib import Graph


@dataclass
class GapItem:
    gap_id: str
    severity: str          # CRITICAL / MAJOR / MINOR
    category: str          # flow_topology / lod_loi / shacl / bfo_prereq
    entity: str            # URI of affected entity
    entity_type: str
    description: str
    standard_reference: str = ""
    bfo_context: str = ""
    remediation: str = ""
    blocking_next_stage: bool = False

    def as_dict(self):
        return self.__dict__


@dataclass
class StageResult:
    stage_id: int
    stage_name: str
    gate_result: str       # PASS / WARN / FAIL
    gaps: List[GapItem] = field(default_factory=list)

    @property
    def critical_count(self):
        return sum(1 for g in self.gaps if g.severity == "CRITICAL")

    @property
    def major_count(self):
        return sum(1 for g in self.gaps if g.severity == "MAJOR")

    @property
    def minor_count(self):
        return sum(1 for g in self.gaps if g.severity == "MINOR")

    def as_dict(self):
        return {
            "stage_id": self.stage_id,
            "stage_name": self.stage_name,
            "gate_result": self.gate_result,
            "critical": self.critical_count,
            "major": self.major_count,
            "minor": self.minor_count,
            "gaps": [g.as_dict() for g in self.gaps],
        }


@dataclass
class StageConfig:
    stage_id: int
    name: str
    lod_level: int
    validators: List[str]   # names of validators to run
    description: str = ""


STAGE_CONFIGS = [
    StageConfig(1, "Briefing / 策划阶段", 100,
                ["lod_loi", "bfo_prereq"],
                "空间计划确认，系统类型声明，LOD100"),
    StageConfig(2, "Schematic Design / 初步设计", 200,
                ["lod_loi", "flow_topology", "bfo_prereq"],
                "系统方案设计，管网拓扑建立，LOD200"),
    StageConfig(3, "Detailed Design / 施工图", 300,
                ["lod_loi", "flow_topology", "shacl", "bfo_prereq"],
                "施工图设计，设备选型，LOD300"),
    StageConfig(4, "Procurement / 招投标", 300,
                ["lod_loi", "shacl"],
                "招标文件发布，设备认证核查，LOD300"),
    StageConfig(5, "Construction / 施工安装", 400,
                ["lod_loi", "flow_topology"],
                "机电安装，竣工信息更新，LOD400"),
    StageConfig(6, "Commissioning / 调试验收", 500,
                ["lod_loi", "flow_topology", "shacl", "bfo_prereq"],
                "调试验收，洁净度检测，移交AIM，LOD500"),
]


def run_simulation(
    query_graph: Graph,
    abox: Graph,
    validators: dict,
    stages: Optional[List[int]] = None,
) -> List[StageResult]:
    """
    Run stage-gate simulation.
    validators: dict mapping name -> callable(graph, abox, stage_config) -> List[GapItem]
    """
    results = []
    for cfg in STAGE_CONFIGS:
        if stages and cfg.stage_id not in stages:
            continue

        gaps: List[GapItem] = []
        for vname in cfg.validators:
            if vname in validators:
                try:
                    new_gaps = validators[vname](query_graph, abox, cfg)
                    gaps.extend(new_gaps)
                except Exception as e:
                    gaps.append(GapItem(
                        gap_id=f"{vname.upper()}-ERR",
                        severity="MAJOR",
                        category=vname,
                        entity="(validator)",
                        entity_type="",
                        description=f"Validator '{vname}' raised: {e}",
                        remediation="Check validator implementation",
                    ))

        # Determine gate result
        critical = sum(1 for g in gaps if g.severity == "CRITICAL")
        if critical > 0:
            gate = "FAIL"
        elif gaps:
            gate = "WARN"
        else:
            gate = "PASS"

        results.append(StageResult(cfg.stage_id, cfg.name, gate, gaps))

    return results
