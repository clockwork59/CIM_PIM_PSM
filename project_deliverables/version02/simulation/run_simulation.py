#!/usr/bin/env python3
"""
CIM PIM 仿真系统入口
使用方法:
    python run_simulation.py [--scenario PATH] [--onto-dir PATH] [--stage N] [--output DIR]
"""
import argparse
import sys
from pathlib import Path

# Allow running from any directory
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from project_deliverables.version02.simulation.core.ontology_loader import (
    load_tbox, load_scenario, make_query_graph
)
from project_deliverables.version02.simulation.core.stage_gate_engine import run_simulation
from project_deliverables.version02.simulation.validators.lod_loi_checker import check_lod_loi
from project_deliverables.version02.simulation.validators.flow_topology import check_flow_topology
from project_deliverables.version02.simulation.validators.bfo_prereq import check_bfo_prereqs
from project_deliverables.version02.simulation.report.pim_plan_generator import (
    generate_json, generate_markdown
)

DEFAULT_ONTO = Path(__file__).parent.parent / "cim/ontology"
DEFAULT_SCENARIO = Path(__file__).parent / "scenario/surgical_wing.ttl"
DEFAULT_OUTPUT = Path(__file__).parent / "output"


def main():
    parser = argparse.ArgumentParser(description="CIM PIM Simulation System")
    parser.add_argument("--onto-dir",  default=str(DEFAULT_ONTO),     help="CIM ontology directory")
    parser.add_argument("--scenario",  default=str(DEFAULT_SCENARIO), help="Scenario TTL file path")
    parser.add_argument("--output",    default=str(DEFAULT_OUTPUT),   help="Output directory")
    parser.add_argument("--stage",     type=int, nargs="+",           help="Run only specified stages")
    parser.add_argument("--format",    choices=["json", "md", "both"], default="both")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "="*60)
    print("  CIM PIM 仿真系统 — 医疗建筑 PIM 验证与规划")
    print("="*60)

    # 1. Load ontology TBox
    print(f"\n[1/4] 加载 CIM 本体 (TBox)...")
    tbox = load_tbox(args.onto_dir)

    # 2. Load scenario ABox
    print(f"\n[2/4] 加载仿真场景 (ABox)...")
    abox = load_scenario(args.scenario)

    # 3. Build query graph
    print(f"\n[3/4] 构建查询图 (TBox + ABox Union)...")
    query_graph = make_query_graph(tbox, abox)
    print(f"      合并后三元组: {len(query_graph):,}")

    # 4. Run simulation
    print(f"\n[4/4] 运行阶段门控仿真...")
    validators = {
        "lod_loi":      check_lod_loi,
        "flow_topology": check_flow_topology,
        "bfo_prereq":   check_bfo_prereqs,
    }

    results = run_simulation(
        query_graph=query_graph,
        abox=abox,
        validators=validators,
        stages=args.stage,
    )

    # Print console summary
    print("\n" + "="*60)
    print("  仿真结果摘要")
    print("="*60)
    gate_sym = {"PASS": "✅ PASS", "WARN": "⚠️  WARN", "FAIL": "❌ FAIL"}
    for r in results:
        sym = gate_sym.get(r.gate_result, r.gate_result)
        print(f"  阶段 {r.stage_id}: {r.stage_name:<30} {sym}")
        if r.gaps:
            print(f"           缺口: 紧急={r.critical_count}  主要={r.major_count}  次要={r.minor_count}")

    total = sum(len(r.gaps) for r in results)
    crit  = sum(r.critical_count for r in results)
    print(f"\n  总缺口: {total}  |  CRITICAL: {crit}")

    # 5. Generate reports
    print(f"\n[输出] 生成报告到 {output_dir}/")
    if args.format in ("json", "both"):
        json_path = output_dir / "gap_analysis.json"
        generate_json(results, json_path)
        print(f"       ✓ {json_path.name}")

    if args.format in ("md", "both"):
        md_path = output_dir / "pim_plan_report.md"
        generate_markdown(results, md_path)
        print(f"       ✓ {md_path.name}")

    print("\n" + "="*60)
    return 0 if crit == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
