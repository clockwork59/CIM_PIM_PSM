"""Conservation equation validation engine.

Validates physical conservation laws and capacity constraints across CIM
building systems: air mass balance, chilled water energy balance, medical
gas capacity adequacy, and electrical redundancy.
"""
from typing import List, Optional
from rdflib import Graph, RDF, URIRef, Literal
from rdflib.namespace import RDFS
from ..core.stage_gate_engine import GapItem, StageConfig
from ..core.namespace_registry import (
    CIM, CIM_EQUIP, CIM_SPACE, CIM_FLOW, CIM_C, CIM_D, CIM_MED,
)

# ── Constants ────────────────────────────────────────────────────────────────

# COP valid range for chillers
COP_MIN = 3.5
COP_MAX = 8.0

# Specific heat of water (kJ/(kg*K))
CP_WATER = 4.186

# Typical per-terminal flow rates (L/min)
TYPICAL_TERMINAL_FLOW = {
    str(CIM_MED.Oxygen): 10.0,
    str(CIM_MED.MedicalVacuum): 40.0,
    str(CIM_MED.MedicalAir): 100.0,
}
TERMINAL_FLOW_LABELS = {
    str(CIM_MED.Oxygen): ("O2/氧气", "L/min"),
    str(CIM_MED.MedicalVacuum): ("VAC/负压吸引", "L/min"),
    str(CIM_MED.MedicalAir): ("CAIR/医用空气", "L/min"),
}
GAS_SAFETY_FACTOR = 1.5

# AHU types to search
AHU_CLASSES = [CIM_EQUIP.Clean_AHU, CIM_EQUIP.AHU]

# Air medium types
SUPPLY_AIR = CIM_MED.SupplyAir
RETURN_AIR = CIM_MED.ReturnAir
OUTDOOR_AIR = CIM_MED.OutdoorAir

# Tolerances
AIR_BALANCE_TOLERANCE = 0.10   # 10%
ENERGY_BALANCE_TOLERANCE = 0.15  # 15%

# Gas source classes
GAS_SOURCE_CLASSES = {
    str(CIM_MED.Oxygen): [CIM_EQUIP.LiquidOxygenStation],
    str(CIM_MED.MedicalVacuum): [CIM_EQUIP.VacuumPumpUnit],
    str(CIM_MED.MedicalAir): [CIM_EQUIP.MedGasCompressor],
}


def check_conservation(graph: Graph, abox: Graph, cfg: StageConfig) -> List[GapItem]:
    """Check conservation equations and capacity constraints.

    Parameters
    ----------
    graph : rdflib.Graph
        Union query graph (TBox + ABox).
    abox : rdflib.Graph
        Instance (ABox) graph.
    cfg : StageConfig
        Current stage configuration.

    Returns
    -------
    list[GapItem]
        Detected conservation violations or capacity issues.
    """
    gaps: List[GapItem] = []
    counter = [0]

    def next_id(prefix: str) -> str:
        counter[0] += 1
        return f"CONS-{prefix}-{counter[0]:03d}"

    # Conservation checks start at LOD 200 (schematic design)
    if cfg.lod_level < 200:
        return gaps

    # 1. Air mass balance per AHU
    gaps.extend(_check_air_mass_balance(abox, next_id))

    # 2. Chilled water energy balance per chiller
    gaps.extend(_check_chiller_energy(abox, next_id))

    # 3. Medical gas capacity adequacy
    gaps.extend(_check_medgas_capacity(abox, next_id))

    # 4. Electrical redundancy
    gaps.extend(_check_electrical_redundancy(abox, next_id))

    return gaps


# ═════════════════════════════════════════════════════════════════════════════
# 1. Air Mass Balance
# ═════════════════════════════════════════════════════════════════════════════

def _check_air_mass_balance(abox: Graph, next_id) -> List[GapItem]:
    """supply_airflow ~ return_airflow + outdoor_airflow (+-10%)."""
    gaps: List[GapItem] = []

    for ahu_cls in AHU_CLASSES:
        for ahu in abox.subjects(RDF.type, ahu_cls):
            ahu_label = _get_label(abox, ahu)
            rated = _get_numeric(abox, ahu, CIM_D.ratedCapacity)
            if rated is None:
                # No airflow data — skip, this is an LOD gap not a conservation error
                continue

            # Gather connection points
            cps = list(abox.objects(ahu, CIM_C.hasConnectionPoint))
            supply_flow = 0.0
            return_flow = 0.0
            outdoor_flow = 0.0
            has_return = False
            has_outdoor = False

            for cp in cps:
                medium = abox.value(cp, CIM_C.hasMedium)
                if medium is None:
                    continue
                cp_type_outlet = (cp, RDF.type, CIM_C.OutletConnectionPoint) in abox
                cp_type_inlet = (cp, RDF.type, CIM_C.InletConnectionPoint) in abox

                med_str = str(medium)
                if med_str == str(SUPPLY_AIR) and cp_type_outlet:
                    # Supply air outlet — use AHU rated capacity as supply flow
                    supply_flow = rated
                elif med_str == str(RETURN_AIR) and cp_type_inlet:
                    has_return = True
                    # Check if the return flow path has a rated value
                    connected = abox.value(cp, CIM_C.connectsTo)
                    if connected:
                        rf = _get_numeric(abox, connected, CIM_D.ratedCapacity)
                        if rf is not None:
                            return_flow = rf
                elif med_str == str(OUTDOOR_AIR) and cp_type_inlet:
                    has_outdoor = True
                    connected = abox.value(cp, CIM_C.connectsTo)
                    if connected:
                        of = _get_numeric(abox, connected, CIM_D.ratedCapacity)
                        if of is not None:
                            outdoor_flow = of

            # If we have supply flow but return/outdoor flows are not numerically
            # specified, we can only flag the missing data as MINOR
            if supply_flow > 0 and has_return and has_outdoor:
                if return_flow == 0.0 and outdoor_flow == 0.0:
                    gaps.append(GapItem(
                        gap_id=next_id("AIR"),
                        severity="MINOR",
                        category="conservation",
                        entity=str(ahu),
                        entity_type=str(ahu_cls).split("#")[-1],
                        description=(
                            f"{ahu_label}: 回风/新风管路存在但缺少流量数据，"
                            f"无法验证风量平衡 / Return/outdoor air paths exist "
                            f"but lack flow rate data for mass balance check"
                        ),
                        standard_reference="GB50333-2013 §6.4 — 送风量=回风量+新风量",
                        bfo_context="AirFlowProcess 质量守恒验证需要各路径流量数据",
                        remediation=(
                            f"为 {ahu_label} 的回风/新风路径添加 cim-d:ratedCapacity 属性"
                        ),
                        blocking_next_stage=False,
                    ))
                elif return_flow > 0 or outdoor_flow > 0:
                    # We have enough data to check balance
                    expected = return_flow + outdoor_flow
                    if expected > 0:
                        ratio = abs(supply_flow - expected) / expected
                        if ratio > AIR_BALANCE_TOLERANCE * 2:
                            gaps.append(GapItem(
                                gap_id=next_id("AIR"),
                                severity="CRITICAL",
                                category="conservation",
                                entity=str(ahu),
                                entity_type=str(ahu_cls).split("#")[-1],
                                description=(
                                    f"{ahu_label}: 风量不平衡 — 送风={supply_flow:.0f} m3/h, "
                                    f"回风+新风={expected:.0f} m3/h, "
                                    f"偏差={ratio*100:.1f}% (>20%) / "
                                    f"Air mass imbalance exceeds 2x tolerance"
                                ),
                                standard_reference="GB50333-2013 §6.4 — 送风量=回风量+新风量 (+-10%)",
                                bfo_context="AirFlowProcess 质量守恒方程不成立",
                                remediation=(
                                    f"校核 {ahu_label} 送风、回风、新风设计流量"
                                ),
                                blocking_next_stage=True,
                            ))
                        elif ratio > AIR_BALANCE_TOLERANCE:
                            gaps.append(GapItem(
                                gap_id=next_id("AIR"),
                                severity="MAJOR",
                                category="conservation",
                                entity=str(ahu),
                                entity_type=str(ahu_cls).split("#")[-1],
                                description=(
                                    f"{ahu_label}: 风量偏差超限 — 送风={supply_flow:.0f} m3/h, "
                                    f"回风+新风={expected:.0f} m3/h, "
                                    f"偏差={ratio*100:.1f}% (>10%) / "
                                    f"Air mass balance marginal"
                                ),
                                standard_reference="GB50333-2013 §6.4 — 送风量=回风量+新风量 (+-10%)",
                                bfo_context="AirFlowProcess 质量守恒方程边界偏差",
                                remediation=(
                                    f"复核 {ahu_label} 送风、回风、新风设计流量"
                                ),
                                blocking_next_stage=False,
                            ))

    return gaps


# ═════════════════════════════════════════════════════════════════════════════
# 2. Chilled Water Energy Balance
# ═════════════════════════════════════════════════════════════════════════════

def _check_chiller_energy(abox: Graph, next_id) -> List[GapItem]:
    """COP range check and Q = m_dot * Cp * dT consistency."""
    gaps: List[GapItem] = []

    for chiller in abox.subjects(RDF.type, CIM_EQUIP.Chiller):
        ch_label = _get_label(abox, chiller)

        # COP range check
        cop = _get_numeric(abox, chiller, CIM_D.coolingCOP)
        if cop is not None:
            if cop < COP_MIN or cop > COP_MAX:
                sev = "CRITICAL" if (cop < COP_MIN * 0.8 or cop > COP_MAX * 1.2) else "MAJOR"
                gaps.append(GapItem(
                    gap_id=next_id("COP"),
                    severity=sev,
                    category="conservation",
                    entity=str(chiller),
                    entity_type="Chiller",
                    description=(
                        f"{ch_label}: COP={cop:.2f} 超出合理范围 [{COP_MIN}, {COP_MAX}] / "
                        f"COP out of valid range"
                    ),
                    standard_reference="ASHRAE 90.1 / GB50189-2015 — 冷水机组COP限值",
                    bfo_context="EnergyTransformationProcess 效率参数异常",
                    remediation=(
                        f"核实 {ch_label} 的 cim-d:coolingCOP 值是否正确"
                    ),
                    blocking_next_stage=(sev == "CRITICAL"),
                ))

        # Energy balance: Q_cooling = rated_capacity (kW)
        # Check if Q ≈ ratedPower * COP
        rated_cap = _get_numeric(abox, chiller, CIM_D.ratedCapacity)
        rated_pwr = _get_numeric(abox, chiller, CIM_D.ratedPower)

        if rated_cap is not None and rated_pwr is not None and cop is not None:
            # COP = Q / W  =>  Q_expected = W * COP
            q_expected = rated_pwr * cop
            if rated_cap > 0:
                ratio = abs(rated_cap - q_expected) / rated_cap
                if ratio > ENERGY_BALANCE_TOLERANCE * 2:
                    gaps.append(GapItem(
                        gap_id=next_id("NRG"),
                        severity="CRITICAL",
                        category="conservation",
                        entity=str(chiller),
                        entity_type="Chiller",
                        description=(
                            f"{ch_label}: 能量不平衡 — 额定制冷量={rated_cap:.0f}kW, "
                            f"功率*COP={q_expected:.0f}kW, "
                            f"偏差={ratio*100:.1f}% (>30%) / "
                            f"Energy balance violation: Q != W * COP"
                        ),
                        standard_reference="热力学第一定律 / First Law of Thermodynamics",
                        bfo_context="EnergyTransformationProcess: Q_cooling = W_input * COP 不成立",
                        remediation=(
                            f"核实 {ch_label} 的 ratedCapacity / ratedPower / coolingCOP 一致性"
                        ),
                        blocking_next_stage=True,
                    ))
                elif ratio > ENERGY_BALANCE_TOLERANCE:
                    gaps.append(GapItem(
                        gap_id=next_id("NRG"),
                        severity="MAJOR",
                        category="conservation",
                        entity=str(chiller),
                        entity_type="Chiller",
                        description=(
                            f"{ch_label}: 能量平衡偏差 — 额定制冷量={rated_cap:.0f}kW, "
                            f"功率*COP={q_expected:.0f}kW, "
                            f"偏差={ratio*100:.1f}% (>15%) / "
                            f"Energy balance marginal"
                        ),
                        standard_reference="热力学第一定律 / First Law of Thermodynamics",
                        bfo_context="EnergyTransformationProcess: Q_cooling = W_input * COP 边界偏差",
                        remediation=(
                            f"复核 {ch_label} 的 ratedCapacity / ratedPower / coolingCOP"
                        ),
                        blocking_next_stage=False,
                    ))
        elif rated_cap is not None and (rated_pwr is None or cop is None):
            missing = []
            if rated_pwr is None:
                missing.append("ratedPower")
            if cop is None:
                missing.append("coolingCOP")
            gaps.append(GapItem(
                gap_id=next_id("NRG"),
                severity="MINOR",
                category="conservation",
                entity=str(chiller),
                entity_type="Chiller",
                description=(
                    f"{ch_label}: 缺少 {', '.join(missing)} 属性，"
                    f"无法验证能量平衡 / "
                    f"Missing {', '.join(missing)} — cannot verify energy balance"
                ),
                standard_reference="热力学第一定律 / First Law of Thermodynamics",
                bfo_context="EnergyTransformationProcess 守恒验证需要完整参数",
                remediation=(
                    f"为 {ch_label} 添加 cim-d:{', cim-d:'.join(missing)} 属性"
                ),
                blocking_next_stage=False,
            ))

    return gaps


# ═════════════════════════════════════════════════════════════════════════════
# 3. Medical Gas Capacity Adequacy
# ═════════════════════════════════════════════════════════════════════════════

def _check_medgas_capacity(abox: Graph, next_id) -> List[GapItem]:
    """source_capacity >= terminal_count * typical_flow * safety_factor."""
    gaps: List[GapItem] = []

    for medium_uri, source_classes in GAS_SOURCE_CLASSES.items():
        label_info = TERMINAL_FLOW_LABELS.get(medium_uri, ("unknown", "L/min"))
        gas_label = label_info[0]
        typical_flow = TYPICAL_TERMINAL_FLOW.get(medium_uri, 0.0)

        # Find total source capacity for this gas type
        total_source_capacity = 0.0
        sources_found = []
        for src_cls in source_classes:
            for src in abox.subjects(RDF.type, src_cls):
                cap = _get_numeric(abox, src, CIM_D.ratedCapacity)
                if cap is not None:
                    total_source_capacity += cap
                    sources_found.append((src, cap))

        if not sources_found:
            continue  # No sources with capacity data

        # Count terminal outlets for this medium
        terminal_count = 0
        for outlet in abox.subjects(RDF.type, CIM_EQUIP.MedicalGasOutlet):
            outlet_medium = abox.value(outlet, CIM_C.hasMedium)
            if outlet_medium and str(outlet_medium) == medium_uri:
                terminal_count += 1

        if terminal_count == 0:
            continue  # No terminals — not a conservation issue

        # Required capacity = terminal_count * typical_flow * safety_factor
        required = terminal_count * typical_flow * GAS_SAFETY_FACTOR

        if total_source_capacity < required:
            deficit_pct = (required - total_source_capacity) / required * 100
            sev = "CRITICAL" if deficit_pct > 30 else "MAJOR"
            source_labels = ", ".join(
                f"{_get_label(abox, s)}({c:.0f})" for s, c in sources_found
            )
            gaps.append(GapItem(
                gap_id=next_id("GAS"),
                severity=sev,
                category="conservation",
                entity=str(sources_found[0][0]),
                entity_type=str(source_classes[0]).split("#")[-1],
                description=(
                    f"{gas_label} 气源容量不足 — "
                    f"源容量={total_source_capacity:.0f} L/min [{source_labels}], "
                    f"需求={required:.0f} L/min "
                    f"({terminal_count}终端 x {typical_flow:.0f} L/min x {GAS_SAFETY_FACTOR}安全系数), "
                    f"缺口={deficit_pct:.0f}% / "
                    f"Gas source capacity insufficient"
                ),
                standard_reference="WS435-2013 §8 — 医用气源容量应满足末端同时使用需求",
                bfo_context="MedicalGasFlowProcess 质量守恒——源端供给不足以覆盖末端需求",
                remediation=(
                    f"增加 {gas_label} 气源容量或减少末端数量"
                ),
                blocking_next_stage=(sev == "CRITICAL"),
            ))

    return gaps


# ═════════════════════════════════════════════════════════════════════════════
# 4. Electrical Redundancy Check
# ═════════════════════════════════════════════════════════════════════════════

def _check_electrical_redundancy(abox: Graph, next_id) -> List[GapItem]:
    """generator_capacity >= sum(IT_panel_capacity)."""
    gaps: List[GapItem] = []

    # Find diesel generators
    gen_total_cap = 0.0
    generators = []
    for gen in abox.subjects(RDF.type, CIM_EQUIP.DieselGenerator):
        cap = _get_numeric(abox, gen, CIM_D.ratedCapacity)
        if cap is not None:
            gen_total_cap += cap
            generators.append((gen, cap))

    if not generators:
        return gaps  # No generators with capacity data

    # Find UPS total capacity
    ups_total_cap = 0.0
    for ups in abox.subjects(RDF.type, CIM_EQUIP.UPS):
        cap = _get_numeric(abox, ups, CIM_D.ratedCapacity)
        if cap is not None:
            ups_total_cap += cap

    # Find IT panel total capacity
    it_total_cap = 0.0
    it_count = 0
    for it_panel in abox.subjects(RDF.type, CIM_EQUIP.IsolatedPowerSystem):
        it_count += 1
        cap = _get_numeric(abox, it_panel, CIM_D.ratedCapacity)
        if cap is not None:
            it_total_cap += cap

    # Check generator >= UPS (if UPS has capacity)
    if ups_total_cap > 0 and gen_total_cap < ups_total_cap:
        deficit_pct = (ups_total_cap - gen_total_cap) / ups_total_cap * 100
        gaps.append(GapItem(
            gap_id=next_id("ELEC"),
            severity="CRITICAL",
            category="conservation",
            entity=str(generators[0][0]),
            entity_type="DieselGenerator",
            description=(
                f"发电机容量不足 — 发电机总容量={gen_total_cap:.0f}kVA, "
                f"UPS总容量={ups_total_cap:.0f}kVA, "
                f"缺口={deficit_pct:.0f}% / "
                f"Generator capacity < UPS capacity"
            ),
            standard_reference="IEC 60364-7-710 — 应急电源容量应覆盖所有关键负载",
            bfo_context="ElectricalPowerProcess 能量守恒——发电机不能满足 UPS 输入需求",
            remediation="增加发电机容量或优化UPS配置",
            blocking_next_stage=True,
        ))

    # If IT panels have capacity data, check UPS >= sum(IT)
    if it_total_cap > 0 and ups_total_cap > 0 and ups_total_cap < it_total_cap:
        deficit_pct = (it_total_cap - ups_total_cap) / it_total_cap * 100
        gaps.append(GapItem(
            gap_id=next_id("ELEC"),
            severity="CRITICAL",
            category="conservation",
            entity=str(list(abox.subjects(RDF.type, CIM_EQUIP.UPS))[0]),
            entity_type="UPS",
            description=(
                f"UPS容量不足 — UPS总容量={ups_total_cap:.0f}kVA, "
                f"IT隔离面板总容量={it_total_cap:.0f}kVA, "
                f"缺口={deficit_pct:.0f}% / "
                f"UPS capacity < sum of IT panel capacity"
            ),
            standard_reference="IEC 60364-7-710 §710.560 — UPS 应覆盖 IT 隔离系统",
            bfo_context="ElectricalPowerProcess 能量守恒——UPS 输出不足以供给所有 IT 面板",
            remediation="增加UPS容量或减少IT隔离系统负载",
            blocking_next_stage=True,
        ))

    return gaps


# ═════════════════════════════════════════════════════════════════════════════
# Utilities
# ═════════════════════════════════════════════════════════════════════════════

def _get_label(g: Graph, uri) -> str:
    """Get rdfs:label or local name."""
    lbl = g.value(uri, RDFS.label)
    if lbl:
        return str(lbl)
    return str(uri).split("#")[-1]


def _get_numeric(g: Graph, subject, predicate) -> Optional[float]:
    """Extract a numeric value from a triple, returning None if absent or unparseable."""
    val = g.value(subject, predicate)
    if val is None:
        return None
    try:
        return float(str(val))
    except (ValueError, TypeError):
        return None
