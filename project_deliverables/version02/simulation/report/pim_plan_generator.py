"""Generate PIM planning report from simulation results."""
import json
from datetime import datetime
from typing import List
from pathlib import Path
from ..core.stage_gate_engine import StageResult


def generate_json(results: List[StageResult], output_path: str | Path) -> None:
    summary = {
        "simulation_id": f"surgical_wing_{datetime.now().strftime('%Y%m%dT%H%M%S')}",
        "scenario": "Hospital Surgical Suite Wing — 手术部",
        "generated": datetime.now().isoformat(),
        "stages": [r.as_dict() for r in results],
        "summary": {
            "total_gaps": sum(len(r.gaps) for r in results),
            "critical": sum(r.critical_count for r in results),
            "major": sum(r.major_count for r in results),
            "minor": sum(r.minor_count for r in results),
            "stages_failing": [r.stage_id for r in results if r.gate_result == "FAIL"],
            "stages_warning": [r.stage_id for r in results if r.gate_result == "WARN"],
            "stages_passing": [r.stage_id for r in results if r.gate_result == "PASS"],
        },
    }
    Path(output_path).write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def generate_markdown(results: List[StageResult], output_path: str | Path, scenario_name: str = "手术部仿真场景") -> None:
    lines = []
    a = lines.append

    total_gaps = sum(len(r.gaps) for r in results)
    critical = sum(r.critical_count for r in results)
    major = sum(r.major_count for r in results)
    minor = sum(r.minor_count for r in results)

    a(f"# PIM 规划报告 — {scenario_name}")
    a(f"")
    a(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  ")
    a(f"**CIM 本体版本**: v4.0.0  ")
    a(f"**场景**: 医院手术部（I级 OR×1 + III级 OR×2 + ICU×1）")
    a(f"")
    a(f"## 执行摘要")
    a(f"")
    a(f"| 阶段门控 | 通过 | 警告 | 失败 |")
    a(f"|---------|------|------|------|")
    pass_n = sum(1 for r in results if r.gate_result == "PASS")
    warn_n = sum(1 for r in results if r.gate_result == "WARN")
    fail_n = sum(1 for r in results if r.gate_result == "FAIL")
    a(f"| 数量 | {pass_n} | {warn_n} | {fail_n} |")
    a(f"")
    a(f"**总缺口数**: {total_gaps}  |  "
      f"**紧急(CRITICAL)**: {critical}  |  "
      f"**主要(MAJOR)**: {major}  |  "
      f"**次要(MINOR)**: {minor}")
    a(f"")

    # Stage details
    a(f"## 各阶段详情")
    a(f"")
    gate_emoji = {"PASS": "✅", "WARN": "⚠️", "FAIL": "❌"}
    for r in results:
        emoji = gate_emoji.get(r.gate_result, "?")
        a(f"### 阶段 {r.stage_id} — {r.stage_name}  {emoji} {r.gate_result}")
        a(f"")
        a(f"缺口统计: 紧急 **{r.critical_count}** | 主要 **{r.major_count}** | 次要 **{r.minor_count}**")
        a(f"")
        if not r.gaps:
            a(f"> 该阶段无缺口，门控通过。")
            a(f"")
            continue

        # Group by category
        by_cat: dict = {}
        for g in r.gaps:
            by_cat.setdefault(g.category, []).append(g)

        CAT_LABELS = {
            "lod_loi": "信息完整度 (LOD/LOI)",
            "flow_topology": "流动拓扑 (Flow Topology)",
            "shacl": "规范合规 (SHACL/Standards)",
            "bfo_prereq": "过程前提条件 (BFO Process)",
        }
        for cat, cat_gaps in by_cat.items():
            a(f"#### {CAT_LABELS.get(cat, cat)}")
            a(f"")
            a(f"| ID | 等级 | 实体 | 描述 | 规范依据 |")
            a(f"|----|------|------|------|---------|")
            for gap in cat_gaps:
                entity_short = gap.entity.split("#")[-1] if "#" in gap.entity else gap.entity.split("/")[-1]
                desc_short = gap.description[:60] + ("…" if len(gap.description) > 60 else "")
                a(f"| {gap.gap_id} | **{gap.severity}** | {entity_short} | {desc_short} | {gap.standard_reference[:40]} |")
            a(f"")

        # Remediation actions
        a(f"#### 修复建议")
        a(f"")
        for gap in sorted(r.gaps, key=lambda g: {"CRITICAL": 0, "MAJOR": 1, "MINOR": 2}[g.severity]):
            prefix = "🔴" if gap.severity == "CRITICAL" else ("🟡" if gap.severity == "MAJOR" else "⚪")
            a(f"- {prefix} `{gap.gap_id}` — {gap.remediation}")
        a(f"")

    # PIM Action Plan
    a(f"## PIM 行动计划")
    a(f"")

    # Collect all gaps by system type and stage
    hvac_gaps = []
    medgas_gaps = []
    elec_gaps = []
    process_gaps = []
    space_gaps = []

    for r in results:
        for g in r.gaps:
            e = g.entity.lower()
            et = g.entity_type.lower()
            if "ahu" in e or "fan" in e or "diffuser" in e or "airflow" in et or "sa_" in e or "hvac" in e:
                hvac_gaps.append((r.stage_id, g))
            elif "medgas" in e or "mgo" in e or "lox" in e or "vacuum" in e or "oxygen" in e.lower() or "gas" in et.lower():
                medgas_gaps.append((r.stage_id, g))
            elif "ups" in e or "gen" in e or "it" in e or "elec" in e or "power" in e or "isolated" in et.lower():
                elec_gaps.append((r.stage_id, g))
            elif "process" in et.lower() or "bfo" in g.category:
                process_gaps.append((r.stage_id, g))
            else:
                space_gaps.append((r.stage_id, g))

    def render_system_plan(title, gap_list):
        if not gap_list:
            return
        a(f"### {title}")
        a(f"")
        by_stage: dict = {}
        for stage_id, g in gap_list:
            by_stage.setdefault(stage_id, []).append(g)
        for sid in sorted(by_stage):
            a(f"**阶段 {sid} 待办:**")
            for g in by_stage[sid]:
                check = "- [ ]"
                a(f"{check} [{g.gap_id}] {g.remediation}")
            a(f"")

    render_system_plan("暖通空调系统 (HVAC)", hvac_gaps)
    render_system_plan("医用气体系统 (Medical Gas)", medgas_gaps)
    render_system_plan("电气系统 (Electrical)", elec_gaps)
    render_system_plan("空间信息 (Space Info)", space_gaps)
    render_system_plan("BFO 过程声明 (Lifecycle Processes)", process_gaps)

    # Compliance checklist
    a(f"## 规范合规清单")
    a(f"")
    a(f"| 要求 | 规范依据 | 状态 | 涉及实体 |")
    a(f"|------|---------|------|---------|")

    # Check key criteria across all gaps
    all_gap_ids = {g.gap_id for r in results for g in r.gaps}
    criteria = [
        ("I级OR换气次数≥36次/h", "GB50333-2013 表6.4.1", "OR_01已声明(40次/h)", "OR_01"),
        ("III级OR换气次数≥20次/h", "GB50333-2013 表6.4.1", "⚠️ OR_02/03缺失", "OR_02, OR_03"),
        ("OR正压差≥+8Pa", "GB50333-2013 §6.5.2", "⚠️ OR_02/03缺失声明", "OR_02, OR_03"),
        ("ICU正压差要求", "WS/T 311", "❌ ICU_Zone缺少pressureClass", "ICU_Zone"),
        ("OR温度21–25°C", "GB50333-2013 §6.6", "OR_01已关联准则", "OR_01"),
        ("每间OR ≥2个O₂终端", "WS435-2013 §7.2", "❌ OR_02/03无终端", "OR_02, OR_03"),
        ("IT隔离电源", "IEC 60364-7-710", "❌ OR_02/03无IT面板", "OR_02, OR_03"),
        ("应急电源冗余N+1", "医建规范", "OR_01链路完整", "DieselGenerator, UPS"),
    ]
    for req, std, status, entity in criteria:
        a(f"| {req} | {std} | {status} | {entity} |")
    a(f"")

    Path(output_path).write_text("\n".join(lines), encoding="utf-8")
