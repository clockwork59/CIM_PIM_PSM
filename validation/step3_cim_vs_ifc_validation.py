#!/usr/bin/env python3
"""
Step 3: 核心验证 — 将 IFC 提取的实体与 CIM v4.0 本体进行多维度对比
输出：结构化差距矩阵 + 优先级排序补充建模清单
"""
import json
from pathlib import Path
from collections import defaultdict, Counter
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, OWL

BASE = Path(__file__).parent.parent
VALIDATION = Path(__file__).parent

# ── 1. 从 CIM v4.0 本体 TTL 文件加载已建模的类 ──────────────────
def load_cim_ontology_classes() -> dict:
    """从 v4.0 本体 TTL 文件加载所有 owl:Class 声明"""
    onto_dir = BASE / "project_deliverables/version02/cim/ontology"
    cim_dir = BASE / "project_deliverables/version02/cim"
    g = Graph()
    ttl_files = (list(onto_dir.glob("*.ttl"))
                 + list(onto_dir.glob("bridge/*.ttl"))
                 + list(cim_dir.glob("equipment/*.ttl"))
                 + list(cim_dir.glob("*.ttl")))
    for f in ttl_files:
        try:
            g.parse(str(f), format="turtle")
        except Exception as e:
            print(f"  [WARN] 解析 {f.name} 失败: {e}")

    # 收集所有 owl:Class
    classes = set()
    for s, _, _ in g.triples((None, RDF.type, OWL.Class)):
        local = str(s).split("#")[-1].split("/")[-1]
        classes.add(local)
    # 也收集 rdfs:subClassOf 的主语
    for s, _, _ in g.triples((None, RDFS.subClassOf, None)):
        local = str(s).split("#")[-1].split("/")[-1]
        classes.add(local)

    return {
        "total_classes": len(classes),
        "classes": sorted(classes),
        "graph_triples": len(g),
    }


# ── 2. Brick 类 → CIM 类 映射表 ──────────────────────────────────
BRICK_TO_CIM_CLASS = {
    "brk:Chiller":                  "Chiller",
    "brk:Cooling_Tower":            "CoolingTower",
    "brk:Boiler":                   "Boiler",
    "brk:Heat_Exchanger":           "HeatExchanger",
    "brk:Air_Handler_Unit":         "AHU",
    "brk:VAV_Box":                  "VAV_Terminal",
    "brk:Fan":                      "Fan",
    "brk:Supply_Fan":               "SupplyFan",
    "brk:Exhaust_Fan":              "ExhaustFan",
    "brk:Diffuser":                 "SupplyAirDiffuser",
    "brk:Return_Air_Grille":        "ReturnAirGrille",
    "brk:Exhaust_Air_Grille":       "ExhaustAirGrille",
    "brk:Filter":                   "HEPA_Filter",
    "brk:Pump":                     "Pump",
    "brk:Coil":                     None,             # P1 gap
    "brk:Sensor":                   "Sensor",
    "brk:Actuator":                 "Actuator",
    "brk:Building_Automation_System": None,
    "brk:Alarm_Panel":              "FireAlarmPanel",
    "brk:Electrical_System":        "Electrical_Equipment",
    "brk:Lighting_System":          None,             # P2 gap
    "brk:Plumbing_Fixture":         None,
    "brk:Fire_Control_Panel":       "FireAlarmPanel",
    "brk:Energy_Conversion_Device": "Chiller",  # CIM maps via Chiller/Boiler/HX subClassOf fso:EnergyConversionDevice
    "brk:Storage_Tank":             "WaterTank",
    "cim:Floor":                    "Floor",
    "cim:Room":                     "Room",
    "cim:Zone":                     "Zone",
}

# ── 3. 执行对比 ─────────────────────────────────────────────────
if __name__ == "__main__":
    # 加载 IFC 映射结果
    mapping_file = VALIDATION / "ifc_to_cim_mapping.json"
    if not mapping_file.exists():
        raise FileNotFoundError("先运行 step2_ifc_to_brick_mapping.py")
    with open(mapping_file) as f:
        ifc_mappings = json.load(f)

    # 加载 CIM 本体
    print("[1/3] 加载 CIM v4.0 本体...")
    cim = load_cim_ontology_classes()
    print(f"  CIM 类总数: {cim['total_classes']}, 三元组: {cim['graph_triples']}")

    # 汇总 IFC Brick 类计数
    ifc_brick_counts = defaultdict(int)
    for inst in ifc_mappings["hvac"].get("mapped_instances", []):
        ifc_brick_counts[inst["brick_class"]] += 1

    print(f"\n{'='*70}")
    print("  CIM × IFC 对比矩阵 — Brick Schema 类")
    print("="*70)
    print(f"{'Brick 类':<45} {'IFC实例':>8} {'CIM类':>12} {'状态':>12}")
    print("-"*70)

    coverage_items = []
    for bc in sorted(set(list(ifc_brick_counts.keys()) + list(BRICK_TO_CIM_CLASS.keys()))):
        ifc_cnt = ifc_brick_counts.get(bc, 0)
        cim_class = BRICK_TO_CIM_CLASS.get(bc)
        cim_has = cim_class and cim_class in cim["classes"]

        if ifc_cnt > 0 and cim_has:
            status = "✅ 已覆盖"
        elif ifc_cnt > 0 and not cim_has:
            status = "❌ IFC有/CIM无"
        elif ifc_cnt == 0 and cim_has:
            status = "⬜ CIM有/IFC无"
        else:
            continue

        cim_label = cim_class or "(未映射)"
        print(f"{bc:<45} {ifc_cnt:>8} {cim_label:>12} {status}")
        coverage_items.append({
            "class": bc,
            "ifc": ifc_cnt,
            "cim_class": cim_label,
            "cim_exists": bool(cim_has),
            "status": status,
        })

    # 统计
    covered = [x for x in coverage_items if "已覆盖" in x["status"]]
    missing = [x for x in coverage_items if "IFC有/CIM无" in x["status"]]
    only_cim = [x for x in coverage_items if "CIM有/IFC无" in x["status"]]
    total_ifc = len(covered) + len(missing)
    rate = len(covered) / max(total_ifc, 1) * 100

    print(f"\n{'='*70}")
    print(f"  覆盖率: {len(covered)}/{total_ifc} = {rate:.1f}%")
    print(f"  IFC有/CIM无(缺口): {len(missing)} 类")
    for m in missing:
        print(f"    ❌ {m['class']} ({m['ifc']} 实例)")

    # ── 4. 系统拓扑对比 ─────────────────────────────────────────
    print(f"\n{'='*70}")
    print("  系统映射验证")
    print("="*70)
    print(f"{'IFC 系统名称':<40} {'映射CIM引用':<25}")
    print("-"*65)
    for sm in ifc_mappings["hvac"].get("system_mappings", []):
        print(f"  {sm['ifc_name']:<38} → {sm['cim_ref']}")

    # ── 5. 空间层级对比 ─────────────────────────────────────────
    print(f"\n{'='*70}")
    print("  空间程序对比")
    print("="*70)
    space_progs = Counter(
        s["cim_type"] for s in ifc_mappings["arch"].get("space_mappings", [])
    )
    for prog, cnt in space_progs.most_common():
        print(f"  {prog:<20} {cnt:>4} 间")

    # ── 6. 属性完整性 ───────────────────────────────────────────
    print(f"\n{'='*70}")
    print("  IFC Pset 属性 → CIM 属性映射")
    print("="*70)
    inv_file = VALIDATION / "ifc_inventory.json"
    pset_coverage = 0
    pset_total = 0
    if inv_file.exists():
        with open(inv_file) as f:
            inv = json.load(f)
        PSET_TO_CIM = {
            "Pset_AirTerminalTypeCommon": ("cim-d:ratedCapacity", True),
            "Pset_DuctSegmentTypeCommon": ("cim-flow:FlowPath", True),
            "Pset_DuctFittingTypeCommon": ("cim-c:ConnectionPoint", True),
            "Pset_FlowTerminalAirTerminal": ("cim-equip:HEPA_Filter", True),
            "Pset_ManufacturerTypeInformation": ("cim-d:EquipmentSpecification", True),
            "Pset_PipeSegmentTypeCommon": ("cim-flow:FlowPath", True),
            "Pset_PipeFittingTypeCommon": ("cim-c:ConnectionPoint", True),
            "Pset_FlowSegmentDuctSegment": ("cim-flow:SupplyAirFlow", True),
            "Pset_FlowSegmentPipeSegment": ("cim-flow:ChilledWaterFlow", True),
            "Constraints": ("cim-d:DesignRequirement", True),
            "Dimensions": ("cim-d:requiredAreaSqm", True),
            "Electrical": ("cim-equip:Electrical_Equipment", True),
            "Electrical - Loads": ("cim-d:ratedPower", True),
            "Energy Analysis": ("cim-o:EnergyConsumptionRecord", True),
            "Identity Data": ("cim-d:designTag", True),
            "Insulation": ("(no CIM equivalent)", False),
            "Fire Protection": ("cim-equip:FireProtectionEquipment", True),
        }
        all_psets = set()
        for key in inv:
            all_psets.update(inv[key].get("psets_found", []))
        for p in sorted(all_psets):
            mapping_info = PSET_TO_CIM.get(p)
            if mapping_info:
                cim_prop, has = mapping_info
                flag = "✅" if has else "❌"
                if has:
                    pset_coverage += 1
            else:
                cim_prop = "? 待映射"
                flag = "⚠️"
            pset_total += 1
            print(f"  {flag} {p:<45} → {cim_prop}")
        if pset_total > 0:
            print(f"\n  Pset 属性映射率: {pset_coverage}/{pset_total} = {pset_coverage/pset_total*100:.0f}%")

    # ── 7. 保存差距矩阵 ────────────────────────────────────────
    gap_report = {
        "summary": {
            "total_ifc_brick_types": total_ifc,
            "covered": len(covered),
            "missing_in_cim": len(missing),
            "only_in_cim": len(only_cim),
            "coverage_rate_pct": round(rate, 1),
            "cim_total_classes": cim["total_classes"],
            "pset_coverage_pct": round(pset_coverage / max(pset_total, 1) * 100, 1),
        },
        "coverage_matrix": coverage_items,
        "missing_in_cim": missing,
        "only_in_cim": only_cim,
        "covered": covered,
    }
    out = VALIDATION / "gap_analysis.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(gap_report, f, ensure_ascii=False, indent=2)
    print(f"\n差距矩阵已保存: {out}")
