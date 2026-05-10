"""
Step 1: 从 IFC 文件提取所有功能性实体的完整清单
目标：了解 IFC 中实际存在哪些设备类型、空间类型、系统定义
"""
import ifcopenshell
import ifcopenshell.util.element as ifc_util
from collections import defaultdict, Counter
import json
from pathlib import Path

# IFC 文件路径（相对于项目根目录）
BASE = Path(__file__).parent.parent
IFC_FILES = {
    "NBU_HVAC":  BASE / "统一领域模型（CIM）/docs/NBU_MedicalClinic/NBU_MedicalClinic_Eng-HVAC.ifc",
    "NBU_ARCH":  BASE / "统一领域模型（CIM）/docs/NBU_MedicalClinic/NBU_MedicalClinic_Arch.ifc",
    "NBU_MEP":   BASE / "统一领域模型（CIM）/docs/NBU_MedicalClinic/NBU_MedicalClinic_Eng-MEP-Optimized.ifc",
    "NBU_ELE":   BASE / "统一领域模型（CIM）/docs/NBU_MedicalClinic/NBU_MedicalClinic_Eng-ELE.ifc",
    "NVW_L200_HVAC": BASE / "统一领域模型（CIM）/docs/NVW_DCR-LOD/NVW_DCR-LOD200_Eng-HVAC.ifc",
    "NVW_L300_HVAC": BASE / "统一领域模型（CIM）/docs/NVW_DCR-LOD/NVW_DCR-LOD300_Eng-HVAC.ifc",
}

# 需要关注的功能实体类型（排除纯几何类型）
FUNCTIONAL_TYPES = [
    # 空间
    "IfcProject", "IfcBuilding", "IfcBuildingStorey", "IfcSpace", "IfcZone",
    # 分配系统
    "IfcDistributionSystem", "IfcSystem", "IfcBuildingSystem",
    # HVAC 设备
    "IfcChiller", "IfcCoolingTower", "IfcBoiler", "IfcHeatExchanger",
    "IfcAirTerminalBox", "IfcAirTerminal", "IfcUnitaryEquipment",
    "IfcFan", "IfcPump", "IfcCompressor", "IfcFilter",
    "IfcFlowMovingDevice", "IfcFlowTerminal", "IfcFlowStorageDevice",
    "IfcFlowTreatmentDevice", "IfcEnergyConversionDevice",
    "IfcSanitaryTerminal", "IfcWasteTerminal",
    # 电气
    "IfcElectricDistributionBoard", "IfcSwitchingDevice",
    "IfcElectricAppliance", "IfcLightFixture", "IfcOutlet",
    "IfcElectricMotor", "IfcGenerator",
    # 传感器/控制
    "IfcSensor", "IfcController", "IfcActuator", "IfcAlarm",
    "IfcProtectiveDevice", "IfcUnitaryControlElement",
    # 管道
    "IfcPipeSegment", "IfcDuctSegment",
    # 类型定义（包含参数）
    "IfcAirTerminalBoxType", "IfcFanType", "IfcPumpType",
    "IfcBoilerType", "IfcChillerType", "IfcUnitaryEquipmentType",
    "IfcLightFixtureType",
]

def extract_inventory(ifc_path: Path) -> dict:
    """提取单个 IFC 文件的实体清单"""
    if not ifc_path.exists():
        return {"error": f"文件不存在: {ifc_path}"}

    model = ifcopenshell.open(str(ifc_path))
    result = {
        "file": ifc_path.name,
        "schema": model.schema,
        "total_entities": len(list(model)),
        "entity_counts": {},
        "spaces": [],
        "storeys": [],
        "systems": [],
        "equipment_sample": defaultdict(list),
        "psets_found": set(),
    }

    # 统计各实体类型
    for etype in FUNCTIONAL_TYPES:
        try:
            entities = model.by_type(etype)
        except RuntimeError:
            continue  # 该类型在当前schema中不存在
        if entities:
            result["entity_counts"][etype] = len(entities)
            # 采样前5个实例
            for e in entities[:5]:
                name = getattr(e, 'Name', '') or ''
                tag = getattr(e, 'Tag', '') or ''
                result["equipment_sample"][etype].append({
                    "id": e.GlobalId,
                    "name": name,
                    "tag": tag,
                })

    # 提取楼层
    for storey in model.by_type("IfcBuildingStorey"):
        result["storeys"].append({
            "name": storey.Name,
            "elevation": storey.Elevation,
        })

    # 提取空间
    for space in model.by_type("IfcSpace")[:50]:  # 只取前50
        result["spaces"].append({
            "id": space.GlobalId,
            "name": space.Name or "",
            "long_name": space.LongName or "",
        })

    # 提取系统
    systems = []
    try:
        systems.extend(model.by_type("IfcSystem"))
    except RuntimeError:
        pass
    try:
        systems.extend(model.by_type("IfcDistributionSystem"))
    except RuntimeError:
        pass
    for sys in systems:
        result["systems"].append({
            "name": getattr(sys, "Name", ""),
            "type": sys.is_a(),
        })

    # 收集 Pset 名称
    for pset in model.by_type("IfcPropertySet"):
        if pset.Name:
            result["psets_found"].add(pset.Name)

    result["psets_found"] = sorted(result["psets_found"])
    return result

# 执行并输出
inventories = {}
for key, path in IFC_FILES.items():
    print(f"处理 {key}...")
    inventories[key] = extract_inventory(path)

# 保存结果
out = Path(__file__).parent / "ifc_inventory.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(inventories, f, ensure_ascii=False, indent=2, default=str)

print(f"\n清单已保存: {out}")

# 打印摘要
for key, inv in inventories.items():
    print(f"\n{'='*60}")
    print(f"  {key}: {inv.get('file','')}")
    print(f"  Schema: {inv.get('schema','')} | 总实体: {inv.get('total_entities',0):,}")
    counts = inv.get("entity_counts", {})
    if counts:
        print(f"  功能实体类型 ({len(counts)}):")
        for etype, cnt in sorted(counts.items(), key=lambda x: -x[1]):
            print(f"    {etype:<40} {cnt:>5} 实例")
    storeys = inv.get("storeys", [])
    if storeys:
        print(f"  楼层 ({len(storeys)}):")
        for s in storeys:
            print(f"    {s['name']:<30} z={s['elevation']:.3f}m")
    systems = inv.get("systems", [])
    if systems:
        print(f"  系统 ({len(systems)}):")
        for s in systems[:10]:
            print(f"    [{s['type']}] {s['name']}")
    psets = inv.get("psets_found", [])
    print(f"  Pset 集合 ({len(psets)}): {', '.join(psets[:10])}...")
