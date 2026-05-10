#!/usr/bin/env python3
"""
Step 7: pyshacl 全量验证
验证对象: ABox + 仿真场景
SHACL形状: shacl_constraints.ttl (v2.1.0 cleanroomClass修复版)
"""
from pathlib import Path

BASE = Path(__file__).parent.parent / "project_deliverables/version02"
SHAPES = BASE / "cim/rules/shacl_constraints.ttl"

DATA_FILES = [
    BASE / "simulation/scenario/surgical_wing.ttl",
    BASE / "simulation/scenario/ward_floor_5f.ttl",
    BASE / "simulation/scenario/chiller_plant.ttl",
    BASE / "cim/abox/nbu_medical_clinic_instances.ttl",
]

# Load all ontology TTLs for ont_graph
ONT_DIR = BASE / "cim/ontology"
ONT_TTLS = list(ONT_DIR.glob("*.ttl")) + list(ONT_DIR.glob("bridge/*.ttl"))
# Also load v3.4 modules
V34_DIR = BASE / "cim"
for subdir in ["equipment", "spaces", "control", "metering", "coupling"]:
    d = V34_DIR / subdir
    if d.exists():
        ONT_TTLS.extend(d.glob("*.ttl"))
skeleton = V34_DIR / "ontology_skeleton.ttl"
if skeleton.exists():
    ONT_TTLS.append(skeleton)


def run_validation():
    try:
        from pyshacl import validate
    except ImportError:
        print("ERROR: pyshacl not installed. Run: pip install pyshacl")
        return

    from rdflib import Graph

    # Build ontology graph
    print("[1/3] Loading ontology (TBox)...")
    ont_g = Graph()
    for ttl in ONT_TTLS:
        try:
            ont_g.parse(str(ttl), format="turtle")
        except Exception as e:
            print(f"  WARN: {ttl.name}: {e}")
    print(f"  Loaded {len(ont_g)} ontology triples from {len(ONT_TTLS)} files")

    # Load SHACL shapes
    print("[2/3] Loading SHACL shapes...")
    shacl_g = Graph()
    shacl_g.parse(str(SHAPES), format="turtle")
    print(f"  Loaded {len(shacl_g)} SHACL triples")

    # Validate each data file
    print("[3/3] Running validation...\n")
    results = {}

    for df in DATA_FILES:
        if not df.exists():
            print(f"SKIP (not found): {df.name}")
            continue

        data_g = Graph()
        try:
            data_g.parse(str(df), format="turtle")
        except Exception as e:
            print(f"PARSE ERROR: {df.name}: {e}")
            continue

        try:
            conforms, results_graph, results_text = validate(
                data_g,
                shacl_graph=shacl_g,
                ont_graph=ont_g,
                inference="rdfs",
                abort_on_first=False,
                allow_infos=True,
                meta_shacl=False,
            )
        except Exception as e:
            print(f"VALIDATION ERROR: {df.name}: {e}")
            results[df.name] = {"conforms": False, "violation": -1, "warning": -1, "info": -1, "error": str(e), "raw": ""}
            continue

        # Count severities
        counts = {"violation": 0, "warning": 0, "info": 0}
        for line in results_text.splitlines():
            ll = line.strip().lower()
            if "violation" in ll and "severity" in ll:
                counts["violation"] += 1
            elif "warning" in ll and "severity" in ll:
                counts["warning"] += 1
            elif "info" in ll and "severity" in ll:
                counts["info"] += 1

        results[df.name] = {
            "conforms": conforms,
            "violation": counts["violation"],
            "warning": counts["warning"],
            "info": counts["info"],
            "raw": results_text,
        }

        status = "✅ PASS" if conforms else "❌ FAIL"
        print(f"{'='*60}")
        print(f"  {df.name}  {status}")
        print(f"  VIOLATION: {counts['violation']}  WARNING: {counts['warning']}  INFO: {counts['info']}")

    # Summary
    total_v = sum(r["violation"] for r in results.values() if r["violation"] >= 0)
    total_w = sum(r["warning"] for r in results.values() if r["warning"] >= 0)
    all_conform = all(r.get("conforms", False) for r in results.values())

    print(f"\n{'='*60}")
    print(f"  SHACL 全量验证汇总")
    print(f"{'='*60}")
    print(f"  验证文件数  : {len(results)}")
    print(f"  总 VIOLATION: {total_v}")
    print(f"  总 WARNING  : {total_w}")
    print(f"  结论: {'PASS ✅ — VIOLATION=0' if total_v == 0 else 'FAIL ❌'}")

    # Save detailed report
    out = Path(__file__).parent / "shacl_full_validation_report.txt"
    with open(out, "w", encoding="utf-8") as f:
        f.write(f"SHACL Full Validation Report\n")
        f.write(f"Date: 2026-05-11\n")
        f.write(f"Total VIOLATION: {total_v}\n")
        f.write(f"Total WARNING: {total_w}\n")
        f.write(f"Overall: {'PASS' if total_v == 0 else 'FAIL'}\n\n")
        for name, r in results.items():
            f.write(f"\n{'='*60}\n{name}\nconforms={r['conforms']}\n{'='*60}\n")
            f.write(r.get("raw", r.get("error", "N/A")))
            f.write("\n")
    print(f"\n  详细报告: {out}")


if __name__ == "__main__":
    run_validation()
