"""
Step 2: 将 IFC 实体映射到 Brick Schema 1.3 类，
        然后与 CIM 模型中的已建模类型进行对比
"""
import ifcopenshell
import json
from pathlib import Path
from collections import defaultdict, Counter

# ============================================================
# IFC → Brick Schema 映射表
# 来源: data_governance_standard.md + Brick Schema 1.3
# ============================================================
IFC_TO_BRICK = {
    # ── HVAC 冷热源 ──────────────────────────────────────────
    "IfcChiller":               "brk:Chiller",
    "IfcChillerType":           "brk:Chiller",
    "IfcCoolingTower":          "brk:Cooling_Tower",
    "IfcBoiler":                "brk:Boiler",
    "IfcBoilerType":            "brk:Boiler",
    "IfcHeatExchanger":         "brk:Heat_Exchanger",

    # ── HVAC 空调机组 ─────────────────────────────────────────
    "IfcUnitaryEquipment":      "brk:Air_Handler_Unit",
    "IfcUnitaryEquipmentType":  "brk:Air_Handler_Unit",
    "IfcAirTerminalBox":        "brk:Fan_Coil_Unit",   # VAV 箱
    "IfcAirTerminalBoxType":    "brk:Fan_Coil_Unit",
    "IfcCoil":                  "brk:Coil",

    # ── HVAC 风机/末端 ────────────────────────────────────────
    "IfcFan":                   "brk:Fan",
    "IfcFanType":               "brk:Fan",
    "IfcFlowMovingDevice":      "brk:Exhaust_Fan",     # 根据系统类型细化
    "IfcAirTerminal":           "brk:Diffuser",
    "IfcFlowTerminal":          "brk:Diffuser",        # 细化: SD→Diffuser, RR→Return_Air_Grille
    "IfcFilter":                "brk:Filter",

    # ── 泵 ───────────────────────────────────────────────────
    "IfcPump":                  "brk:Pump",
    "IfcPumpType":              "brk:Pump",

    # ── 医疗气体 ─────────────────────────────────────────────
    "IfcMedicalDevice":         "brk:Oxygen_System",
    "IfcSanitaryTerminal":      "brk:Plumbing_Fixture",

    # ── 电气 ─────────────────────────────────────────────────
    "IfcElectricDistributionBoard": "brk:Electrical_System",
    "IfcSwitchingDevice":       "brk:Electrical_System",
    "IfcGenerator":             "brk:Electrical_System",
    "IfcTransformer":           "brk:Electrical_System",
    "IfcElectricMotor":         "brk:Electrical_System",
    "IfcLightFixture":          "brk:Lighting_System",
    "IfcLightFixtureType":      "brk:Lighting_System",
    "IfcOutlet":                "brk:Electrical_System",

    # ── 传感器/控制 ───────────────────────────────────────────
    "IfcSensor":                "brk:Sensor",
    "IfcController":            "brk:Building_Automation_System",
    "IfcActuator":              "brk:Actuator",
    "IfcAlarm":                 "brk:Alarm_Panel",
    "IfcUnitaryControlElement": "brk:Building_Automation_System",

    # ── 消防 ─────────────────────────────────────────────────
    "IfcFireSuppressionTerminal": "brk:Fire_Control_Panel",

    # ── 空间 ─────────────────────────────────────────────────
    "IfcBuildingStorey":        "cim:Floor",
    "IfcSpace":                 "cim:Room",
    "IfcZone":                  "cim:Zone",
}

# ── FlowTerminal 类型细化规则（基于 Name 字段）─────────────────
def refine_flow_terminal(name: str) -> str:
    n = (name or "").upper()
    if "SD" in n or "SUPPLY DIFFUSER" in n or "SUPPLY AIR" in n:
        return "brk:Diffuser"
    if "RR" in n or "RETURN REGISTER" in n or "RETURN AIR" in n:
        return "brk:Return_Air_Grille"
    if "ER" in n or "EXHAUST" in n:
        return "brk:Exhaust_Air_Grille"
    return "brk:Diffuser"  # 默认

# ── FlowMovingDevice 类型细化规则 ──────────────────────────────
def refine_flow_moving(name: str) -> str:
    n = (name or "").upper()
    if "EXHAUST" in n:
        return "brk:Exhaust_Fan"
    if "SUPPLY" in n:
        return "brk:Supply_Fan"
    if "CENTRIFUGAL" in n:
        return "brk:Fan"
    return "brk:Fan"

# ── 系统名称 → CIM 系统引用映射 ────────────────────────────────
SYSTEM_TO_CIM = {
    "SUPPLY AIR":             "cim:HVAC-AHU-MAIN",
    "MECHANICAL SUPPLY AIR":  "cim:HVAC-AHU-MAIN",
    "RETURN AIR":             "cim:HVAC-AHU-MAIN",
    "MECHANICAL RETURN AIR":  "cim:HVAC-AHU-MAIN",
    "EXHAUST AIR":            "cim:HVAC-EXH",
    "MECHANICAL EXHAUST":     "cim:HVAC-EXH",
    "HYDRONIC SUPPLY":        "cim:HVAC-CHP-01",
    "HYDRONIC RETURN":        "cim:HVAC-CHP-01",
    "HOT WATER":              "cim:HVAC-HWS",
    "CHILLED WATER":          "cim:HVAC-CHP-01",
    "DOMESTIC WATER":         "cim:PLUMB-DWS",
    "SANITARY":               "cim:PLUMB-DRAIN",
    "FIRE PROTECTION":        "cim:FP-HYDRANT",
}

# ── IFC 楼层名称 → CIM 楼层标识 映射 ──────────────────────────
STOREY_TO_CIM = {
    "TOF FOOTING":  "B2",
    "BASEMENT":     "B1",
    "GROUND":       "1F",
    "FIRST FLOOR":  "1F",
    "1F":           "1F",
    "LEVEL 1":      "1F",
    "SECOND FLOOR": "2F",
    "LEVEL 2":      "2F",
    "THIRD FLOOR":  "3F",
    "LEVEL 3":      "3F",
    "ROOF":         "RF",
    "ROOF - MAIN":  "RF",
    "MECHANICAL":   "RF",
}

# ── 空间程序 → CIM 空间类型 映射 ──────────────────────────────
SPACE_PROGRAM_TO_CIM = {
    "OPERATING ROOM": "OR",
    "OR":             "OR",
    "SURGERY":        "OR",
    "PROCEDURE":      "OR",
    "ICU":            "ICU",
    "INTENSIVE CARE": "ICU",
    "WARD":           "WARD",
    "PATIENT ROOM":   "WARD",
    "CORRIDOR":       "CORRIDOR",
    "WAITING":        "WAITING",
    "RECEPTION":      "RECEPTION",
    "EXAM":           "EXAM",
    "OFFICE":         "OFFICE",
    "TOILET":         "TOILET",
    "MECHANICAL":     "MECHANICAL",
    "ELECTRICAL":     "ELECTRICAL",
}

# ── 主处理逻辑 ─────────────────────────────────────────────────
BASE     = Path(__file__).parent.parent
HVAC_IFC = BASE / "统一领域模型（CIM）/docs/NBU_MedicalClinic/NBU_MedicalClinic_Eng-HVAC.ifc"
ARCH_IFC = BASE / "统一领域模型（CIM）/docs/NBU_MedicalClinic/NBU_MedicalClinic_Arch.ifc"


def map_ifc_to_cim(ifc_path: Path, model_key: str) -> dict:
    if not ifc_path.exists():
        print(f"  ⚠️  文件不存在: {ifc_path.name}")
        return {"model": model_key, "brick_class_counts": {}, "mapped_instances": [],
                "space_mappings": [], "system_mappings": []}

    model = ifcopenshell.open(str(ifc_path))
    result = {
        "model": model_key,
        "brick_class_counts": defaultdict(int),
        "unmapped_entities": defaultdict(int),
        "mapped_instances": [],
        "space_mappings": [],
        "system_mappings": [],
    }

    for ifc_type, brick_class in IFC_TO_BRICK.items():
        if not ifc_type.startswith("Ifc"):
            continue
        try:
            entities = model.by_type(ifc_type)
        except RuntimeError:
            continue
        if not entities:
            continue
        for e in entities:
            name = getattr(e, "Name", "") or ""
            tag  = getattr(e, "Tag",  "") or ""

            # 细化映射
            refined = brick_class
            if ifc_type == "IfcFlowTerminal":
                refined = refine_flow_terminal(name)
            elif ifc_type == "IfcFlowMovingDevice":
                refined = refine_flow_moving(name)

            result["brick_class_counts"][refined] += 1
            result["mapped_instances"].append({
                "ifc_type":   ifc_type,
                "ifc_id":     e.GlobalId,
                "ifc_name":   name,
                "ifc_tag":    tag,
                "brick_class": refined,
            })

    # 空间映射
    try:
        for space in model.by_type("IfcSpace"):
            name      = space.Name or ""
            long_name = (space.LongName or "").upper()
            program   = "UNKNOWN"
            for prog, cim_type in SPACE_PROGRAM_TO_CIM.items():
                if prog in long_name or prog in name.upper():
                    program = cim_type
                    break
            result["space_mappings"].append({
                "ifc_id":      space.GlobalId,
                "ifc_name":    name,
                "ifc_program": space.LongName or "",
                "cim_type":    program,
            })
    except RuntimeError:
        pass

    # 系统映射
    systems = []
    for stype in ("IfcSystem", "IfcDistributionSystem"):
        try:
            systems.extend(model.by_type(stype))
        except RuntimeError:
            pass
    for sys in systems:
        sys_name = (getattr(sys, "Name", "") or "").upper()
        cim_ref  = "UNKNOWN"
        for pattern, ref in SYSTEM_TO_CIM.items():
            if pattern in sys_name:
                cim_ref = ref
                break
        result["system_mappings"].append({
            "ifc_name": getattr(sys, "Name", ""),
            "ifc_type": sys.is_a(),
            "cim_ref":  cim_ref,
        })

    result["brick_class_counts"] = dict(result["brick_class_counts"])
    return result


print("处理 HVAC 模型...")
hvac_result = map_ifc_to_cim(HVAC_IFC, "NBU_MedicalClinic_HVAC")
print("处理建筑模型...")
arch_result = map_ifc_to_cim(ARCH_IFC, "NBU_MedicalClinic_Arch")

# 保存
out = Path(__file__).parent / "ifc_to_cim_mapping.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump({"hvac": hvac_result, "arch": arch_result}, f, ensure_ascii=False, indent=2, default=str)

# 打印摘要
print(f"\n{'='*60}")
print("HVAC 模型 Brick 类分布:")
for bc, cnt in sorted(hvac_result["brick_class_counts"].items(), key=lambda x: -x[1]):
    print(f"  {bc:<45} {cnt:>5} 实例")

print(f"\n系统映射:")
for sm in hvac_result.get("system_mappings", []):
    print(f"  [{sm['ifc_type']}] {sm['ifc_name']:<35} → {sm['cim_ref']}")

print(f"\n建筑空间程序分布:")
progs = Counter(s["cim_type"] for s in arch_result.get("space_mappings", []))
for prog, cnt in progs.most_common():
    print(f"  {prog:<20} {cnt:>4} 间")

print(f"\n✅ 结果已保存: {out}")
