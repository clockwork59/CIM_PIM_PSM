#!/usr/bin/env python3
"""
Step 2: 将 IFC 实体映射到 Brick Schema 1.3 类，
        然后与 CIM 模型中的已建模类型进行对比
"""
import ifcopenshell
import json
from pathlib import Path
from collections import defaultdict, Counter

# ── IFC → Brick Schema 映射表 ─────────────────────────────────
IFC_TO_BRICK = {
    "IfcChiller":               "brk:Chiller",
    "IfcChillerType":           "brk:Chiller",
    "IfcCoolingTower":          "brk:Cooling_Tower",
    "IfcBoiler":                "brk:Boiler",
    "IfcBoilerType":            "brk:Boiler",
    "IfcHeatExchanger":         "brk:Heat_Exchanger",
    "IfcUnitaryEquipment":      "brk:Air_Handler_Unit",
    "IfcUnitaryEquipmentType":  "brk:Air_Handler_Unit",
    "IfcAirTerminalBox":        "brk:VAV_Box",
    "IfcAirTerminalBoxType":    "brk:VAV_Box",
    "IfcCoil":                  "brk:Coil",
    "IfcFan":                   "brk:Fan",
    "IfcFanType":               "brk:Fan",
    "IfcFlowMovingDevice":      "brk:Exhaust_Fan",
    "IfcAirTerminal":           "brk:Diffuser",
    "IfcFlowTerminal":          "brk:Diffuser",
    "IfcFilter":                "brk:Filter",
    "IfcPump":                  "brk:Pump",
    "IfcPumpType":              "brk:Pump",
    "IfcSanitaryTerminal":      "brk:Plumbing_Fixture",
    "IfcElectricDistributionBoard": "brk:Electrical_System",
    "IfcSwitchingDevice":       "brk:Electrical_System",
    "IfcGenerator":             "brk:Electrical_System",
    "IfcTransformer":           "brk:Electrical_System",
    "IfcElectricMotor":         "brk:Electrical_System",
    "IfcLightFixture":          "brk:Lighting_System",
    "IfcLightFixtureType":      "brk:Lighting_System",
    "IfcOutlet":                "brk:Electrical_System",
    "IfcSensor":                "brk:Sensor",
    "IfcController":            "brk:Building_Automation_System",
    "IfcActuator":              "brk:Actuator",
    "IfcAlarm":                 "brk:Alarm_Panel",
    "IfcUnitaryControlElement": "brk:Building_Automation_System",
    "IfcFireSuppressionTerminal": "brk:Fire_Control_Panel",
    "IfcBuildingStorey":        "cim:Floor",
    "IfcSpace":                 "cim:Room",
    "IfcZone":                  "cim:Zone",
    "IfcEnergyConversionDevice": "brk:Energy_Conversion_Device",
    "IfcFlowStorageDevice":     "brk:Storage_Tank",
}

def refine_flow_terminal(name: str) -> str:
    name_upper = (name or "").upper()
    if "SD" in name_upper or "SUPPLY" in name_upper or "DIFFUSER" in name_upper:
        return "brk:Diffuser"
    if "RR" in name_upper or "RETURN" in name_upper or "REGISTER" in name_upper:
        return "brk:Return_Air_Grille"
    if "ER" in name_upper or "EXHAUST" in name_upper:
        return "brk:Exhaust_Air_Grille"
    return "brk:Diffuser"

def refine_flow_moving(name: str) -> str:
    name_upper = (name or "").upper()
    if "EXHAUST" in name_upper:
        return "brk:Exhaust_Fan"
    if "SUPPLY" in name_upper:
        return "brk:Supply_Fan"
    if "CENTRIFUGAL" in name_upper or "INLINE" in name_upper:
        return "brk:Supply_Fan"
    return "brk:Fan"

SYSTEM_TO_CIM = {
    "SUPPLY AIR":           "cim:HVAC-AHU-MAIN",
    "MECHANICAL SUPPLY AIR": "cim:HVAC-AHU-MAIN",
    "RETURN AIR":           "cim:HVAC-AHU-MAIN",
    "MECHANICAL RETURN AIR": "cim:HVAC-AHU-MAIN",
    "EXHAUST AIR":          "cim:HVAC-EXH",
    "MECHANICAL EXHAUST":   "cim:HVAC-EXH",
    "HYDRONIC SUPPLY":      "cim:HVAC-CHP-01",
    "HYDRONIC RETURN":      "cim:HVAC-CHP-01",
    "HOT WATER":            "cim:HVAC-HWS",
    "CHILLED WATER":        "cim:HVAC-CHP-01",
    "DOMESTIC WATER":       "cim:PLUMB-DWS",
    "SANITARY":             "cim:PLUMB-DRAIN",
    "FIRE PROTECTION":      "cim:FP-HYDRANT",
    "TILLUFT":              "cim:HVAC-AHU-MAIN",
    "AVTREKK":              "cim:HVAC-EXH",
    "INNTAK":               "cim:HVAC-OA",
    "AVKAST":               "cim:HVAC-EXH",
}

SPACE_PROGRAM_TO_CIM = {
    "OPERATING ROOM": "OR", "OR": "OR", "SURGERY": "OR", "PROCEDURE": "OR",
    "ICU": "ICU", "INTENSIVE CARE": "ICU",
    "WARD": "WARD", "PATIENT ROOM": "WARD", "PATIENT": "WARD",
    "CORRIDOR": "CORRIDOR", "HALL": "CORRIDOR",
    "WAITING": "WAITING", "RECEPTION": "RECEPTION",
    "EXAM": "EXAM", "OFFICE": "OFFICE",
    "TOILET": "TOILET", "RESTROOM": "TOILET",
    "MECHANICAL": "MECHANICAL", "ELECTRICAL": "ELECTRICAL",
    "ADMIN": "ADMIN", "STORAGE": "STORAGE", "LOBBY": "LOBBY",
}

BASE = Path(__file__).parent.parent

def map_ifc_to_cim(ifc_path: Path, model_key: str) -> dict:
    if not ifc_path.exists():
        return {"model": model_key, "error": f"文件不存在: {ifc_path}"}

    model = ifcopenshell.open(str(ifc_path))
    result = {
        "model": model_key,
        "brick_class_counts": {},
        "unmapped_entities": {},
        "mapped_instances": [],
        "space_mappings": [],
        "system_mappings": [],
    }
    brick_counts = defaultdict(int)

    for ifc_type, brick_class in IFC_TO_BRICK.items():
        try:
            entities = model.by_type(ifc_type)
        except RuntimeError:
            continue
        if not entities:
            continue
        for e in entities:
            name = getattr(e, "Name", "") or ""
            tag = getattr(e, "Tag", "") or ""
            actual_brick = brick_class
            if ifc_type in ("IfcFlowTerminal", "IfcAirTerminal"):
                actual_brick = refine_flow_terminal(name)
            elif ifc_type == "IfcFlowMovingDevice":
                actual_brick = refine_flow_moving(name)
            brick_counts[actual_brick] += 1
            result["mapped_instances"].append({
                "ifc_type": ifc_type,
                "ifc_id": e.GlobalId,
                "ifc_name": name,
                "ifc_tag": tag,
                "brick_class": actual_brick,
            })

    result["brick_class_counts"] = dict(brick_counts)

    for space in model.by_type("IfcSpace")[:100]:
        name = space.Name or ""
        long_name = (getattr(space, "LongName", "") or "").upper()
        combined = f"{name} {long_name}".upper()
        program = "UNKNOWN"
        for prog, cim_type in SPACE_PROGRAM_TO_CIM.items():
            if prog in combined:
                program = cim_type
                break
        result["space_mappings"].append({
            "ifc_id": space.GlobalId,
            "ifc_name": name,
            "ifc_program": getattr(space, "LongName", "") or "",
            "cim_type": program,
        })

    sys_types = []
    try:
        sys_types += model.by_type("IfcSystem")
    except RuntimeError:
        pass
    try:
        sys_types += model.by_type("IfcDistributionSystem")
    except RuntimeError:
        pass
    for sys in sys_types:
        sys_name = (getattr(sys, "Name", "") or "").upper()
        cim_ref = "UNKNOWN"
        for pattern, ref in SYSTEM_TO_CIM.items():
            if pattern in sys_name:
                cim_ref = ref
                break
        result["system_mappings"].append({
            "ifc_name": getattr(sys, "Name", ""),
            "ifc_type": sys.is_a(),
            "cim_ref": cim_ref,
        })

    return result


if __name__ == "__main__":
    HVAC_IFC = BASE / "docs/NBU_MedicalClinic/NBU_MedicalClinic_Eng-HVAC.ifc"
    ARCH_IFC = BASE / "docs/NBU_MedicalClinic/NBU_MedicalClinic_Arch.ifc"

    print("处理 HVAC 模型...")
    hvac_result = map_ifc_to_cim(HVAC_IFC, "NBU_MedicalClinic_HVAC")
    print("处理建筑模型...")
    arch_result = map_ifc_to_cim(ARCH_IFC, "NBU_MedicalClinic_Arch")

    out = Path(__file__).parent / "ifc_to_cim_mapping.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"hvac": hvac_result, "arch": arch_result}, f,
                  ensure_ascii=False, indent=2, default=str)

    print(f"\n{'='*60}")
    print("HVAC 模型 Brick 类分布:")
    for bc, cnt in sorted(hvac_result["brick_class_counts"].items(), key=lambda x: -x[1]):
        print(f"  {bc:<45} {cnt:>5} 实例")

    print(f"\n系统映射:")
    for sm in hvac_result["system_mappings"]:
        print(f"  [{sm['ifc_type']}] {sm['ifc_name']:<35} → {sm['cim_ref']}")

    print(f"\n建筑空间程序分布:")
    progs = Counter(s["cim_type"] for s in arch_result["space_mappings"])
    for prog, cnt in progs.most_common():
        print(f"  {prog:<20} {cnt:>4} 间")

    print(f"\n结果已保存: {out}")
