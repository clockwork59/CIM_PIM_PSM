"""
Step 3: 核心验证 — 将 IFC 提取的实体与 CIM 模型进行多维度对比
输出：结构化差距矩阵 + 优先级排序补充建模清单
"""
import json
import sys
from pathlib import Path
from collections import defaultdict, Counter
from rdflib import Graph, Namespace
from rdflib.namespace import RDF

BASE = Path(__file__).parent.parent
BRK  = Namespace("https://brickschema.org/schema/1.3/Brick#")
CIM  = Namespace("https://pim.example.com/cim#")


# ── 1. 从 Python 转换器提取 CIM 已建模实体 ──────────────────────
def load_cim_from_converter() -> dict:
    """动态加载转换器并提取设备清单"""
    sys.path.insert(0, str(BASE))
    try:
        from md_to_rdf_converter_phase2_full import PHASE2_FULL_EQUIPMENT
        by_brick  = defaultdict(list)
        by_system = defaultdict(list)
        for eq in PHASE2_FULL_EQUIPMENT:
            by_brick[eq["brick_class"]].append(eq["id"])
            by_system[eq["system"]].append(eq["id"])
        return {
            "total":            len(PHASE2_FULL_EQUIPMENT),
            "by_brick_class":   dict(by_brick),
            "by_system":        dict(by_system),
            "all_ids":          [eq["id"] for eq in PHASE2_FULL_EQUIPMENT],
            "all_brick_classes": list(set(eq["brick_class"] for eq in PHASE2_FULL_EQUIPMENT)),
        }
    except ImportError as e:
        print(f"⚠️  无法导入转换器 ({e})，回退至 TTL 文件")
        return load_cim_from_ttl()


def load_cim_from_ttl() -> dict:
    """备用：从 TTL 文件加载（仅含 Canonical Stub 代表性实例）"""
    ttl_path = BASE / "cim_phase2_full_model.ttl"
    g = Graph()
    g.parse(str(ttl_path), format="turtle")
    by_brick = defaultdict(list)
    for subj, _, obj in g.triples((None, RDF.type, None)):
        by_brick[str(obj)].append(str(subj))
    return {
        "total":            sum(len(v) for v in by_brick.values()),
        "by_brick_class":   {k: v for k, v in by_brick.items() if "pim.example.com" not in k},
        "by_system":        {},
        "all_ids":          [],
        "all_brick_classes": list(by_brick.keys()),
    }


# ── 2. 加载 IFC 映射结果 ──────────────────────────────────────
mapping_file = Path(__file__).parent / "ifc_to_cim_mapping.json"
if not mapping_file.exists():
    raise FileNotFoundError("请先运行 step2_ifc_to_brick_mapping.py")
with open(mapping_file) as f:
    ifc_mappings = json.load(f)


# ── 3. 对比分析 ────────────────────────────────────────────────
cim = load_cim_from_converter()

ifc_brick_counts = defaultdict(int)
for inst in ifc_mappings["hvac"].get("mapped_instances", []):
    ifc_brick_counts[inst["brick_class"]] += 1

print("\n" + "="*70)
print("  CIM × IFC 对比矩阵 — Brick Schema 类")
print("="*70)
print(f"{'Brick 类':<45} {'IFC实例':>8} {'CIM建模':>8} {'状态':>12}")
print("-"*70)

all_classes    = sorted(set(list(ifc_brick_counts.keys()) + list(cim["by_brick_class"].keys())))
coverage_items = []

for bc in all_classes:
    ifc_cnt = ifc_brick_counts.get(bc, 0)
    cim_cnt = len(cim["by_brick_class"].get(bc, []))
    if ifc_cnt > 0 and cim_cnt > 0:
        status = "✅ 已覆盖"
    elif ifc_cnt > 0 and cim_cnt == 0:
        status = "❌ IFC有/CIM无"
    elif ifc_cnt == 0 and cim_cnt > 0:
        status = "⬜ CIM有/IFC无"
    else:
        continue
    print(f"{bc:<45} {ifc_cnt:>8} {cim_cnt:>8} {status:>12}")
    coverage_items.append({"class": bc, "ifc": ifc_cnt, "cim": cim_cnt, "status": status})


# ── 4. 系统拓扑对比 ────────────────────────────────────────────
print("\n" + "="*70)
print("  系统映射验证")
print("="*70)
print(f"{'IFC 系统名称':<40} {'映射CIM引用':<25} {'覆盖':>6}")
print("-"*70)
cim_system_strs = str(cim.get("by_system", {}))
for sm in ifc_mappings["hvac"].get("system_mappings", []):
    in_cim = sm["cim_ref"] in cim_system_strs
    flag   = "✅" if in_cim else "❌"
    print(f"{sm['ifc_name']:<40} {sm['cim_ref']:<25} {flag:>6}")


# ── 5. 空间层级对比 ────────────────────────────────────────────
print("\n" + "="*70)
print("  空间程序对比")
print("="*70)
ifc_space_programs = Counter(
    s["cim_type"] for s in ifc_mappings["arch"].get("space_mappings", [])
)
CIM_SPACE_COVERAGE = {
    "OR":       12,
    "ICU":       6,
    "WARD":     10,
    "CORRIDOR":  0,
    "WAITING":   0,
    "EXAM":      0,
}
print(f"{'空间类型':<15} {'IFC实际间数':>12} {'CIM AHU/传感器':>15} {'状态':>8}")
print("-"*55)
for stype, cim_cnt in CIM_SPACE_COVERAGE.items():
    ifc_cnt = ifc_space_programs.get(stype, 0)
    if ifc_cnt > 0 and cim_cnt > 0:
        status = "✅"
    elif ifc_cnt > 0 and cim_cnt == 0:
        status = "⬜ CIM扩展"
    else:
        status = ""
    print(f"{stype:<15} {ifc_cnt:>12} {cim_cnt:>15} {status:>8}")


# ── 6. Pset 属性映射率 ───────────────────────────────────────────
inventory_file = Path(__file__).parent / "ifc_inventory.json"
if inventory_file.exists():
    with open(inventory_file) as f:
        inv = json.load(f)
    print("\n" + "="*70)
    print("  IFC Pset 属性 → CIM 属性映射覆盖率")
    print("="*70)
    PSET_TO_CIM = {
        "Pressure Drop":          "cim:hasPressureDrop",
        "Flow":                   "cim:hasFlowRate / cim:hasAirflowRate",
        "System Name":            "cim:hasSystemReference",
        "System Type":            "cim:hasSystemReference",
        "System Classification":  "cim:hasSystemReference",
        "Level":                  "brk:hasLocation",
        "Height":                 "(geometry, no CIM equivalent)",
        "Width":                  "(geometry, no CIM equivalent)",
        "ASHRAE Table":           "(no CIM equivalent)",
        "Insulation Thickness":   "(no CIM equivalent)",
        "Slope":                  "(no CIM equivalent)",
        "Offset":                 "(no CIM equivalent)",
    }
    psets_found = inv.get("NBU_HVAC", {}).get("psets_found", [])
    covered = 0
    for p in psets_found[:20]:
        mapped   = PSET_TO_CIM.get(p, "? 待映射")
        has_map  = mapped != "? 待映射" and "(no CIM" not in mapped
        flag     = "✅" if has_map else ("❌" if "(no CIM" in mapped else "⚠️")
        if has_map:
            covered += 1
        print(f"  {flag} {p:<35} → {mapped}")
    if psets_found:
        print(f"\n  Pset 属性映射率: {covered}/{min(len(psets_found),20)} = "
              f"{covered/min(len(psets_found),20)*100:.0f}%")


# ── 7. 保存差距矩阵 ─────────────────────────────────────────────
gap_report = {
    "coverage_matrix": coverage_items,
    "missing_in_cim":  [x for x in coverage_items if "IFC有/CIM无" in x["status"]],
    "only_in_cim":     [x for x in coverage_items if "CIM有/IFC无" in x["status"]],
    "covered":         [x for x in coverage_items if "已覆盖"      in x["status"]],
}
out = Path(__file__).parent / "gap_analysis.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(gap_report, f, ensure_ascii=False, indent=2)

covered_cnt = len(gap_report["covered"])
missing_cnt = len(gap_report["missing_in_cim"])
total_cnt   = covered_cnt + missing_cnt
rate        = covered_cnt / max(total_cnt, 1) * 100
print(f"\n{'='*70}")
print(f"  实体类型覆盖率: {covered_cnt}/{total_cnt} = {rate:.1f}%")
print(f"  P0缺口数量:     {missing_cnt} 类")
print(f"\n✅ 差距矩阵已保存: {out}")
