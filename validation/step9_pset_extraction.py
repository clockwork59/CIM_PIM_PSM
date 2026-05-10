#!/usr/bin/env python3
"""
step9_pset_extraction.py
========================
Extract quantitative PropertySet values from the NBU Medical Clinic IFC-HVAC
file and generate a CIM ABox enrichment Turtle file.

Workflow:
  1. Parse IFC with ifcopenshell
  2. For target entity types, extract quantitative properties (airflow, pressure
     drop, power, dimensions)
  3. Match extracted data to existing ABox instances via cim:ifcGlobalId
  4. Write enrichment triples to nbu_pset_enrichment.ttl
"""

from __future__ import annotations

import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from datetime import date

import ifcopenshell
try:
    from ifcopenshell.util.element import get_psets
    USE_GET_PSETS = True
except ImportError:
    USE_GET_PSETS = False

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
IFC_PATH = Path("/workspaces/CIM_PIM_PSM/docs/NBU_MedicalClinic/NBU_MedicalClinic_Eng-HVAC.ifc")
ABOX_PATH = Path("/workspaces/CIM_PIM_PSM/project_deliverables/version02/cim/abox/nbu_medical_clinic_instances.ttl")
OUT_PATH  = Path("/workspaces/CIM_PIM_PSM/project_deliverables/version02/cim/abox/nbu_pset_enrichment.ttl")

# Target IFC entity types
TARGET_TYPES = [
    "IfcFlowTerminal",
    "IfcFlowMovingDevice",
    "IfcFlowController",        # VAV box instances (typed by IfcAirTerminalBoxType)
    "IfcEnergyConversionDevice",
]

# ---------------------------------------------------------------------------
# Property extraction rules
# ---------------------------------------------------------------------------
# Each rule: (cim_property, pset_names, prop_names)
# pset_names=None means "any pset"
EXTRACTION_RULES: list[tuple[str, list[str] | None, list[str]]] = [
    # Airflow
    ("cim-d:ratedAirflowRate",
     ["Mechanical - Flow", "Pset_AirTerminalTypeCommon"],
     ["Flow", "Air Flow", "AirflowRate", "Supply Airflow"]),
    # Return airflow (AHUs have separate return)
    ("cim-d:returnAirflowRate",
     ["Mechanical - Flow"],
     ["Return Airflow"]),
    # Pressure drop
    ("cim-d:pressureDrop",
     None,  # any pset
     ["Pressure Drop", "Supply Air Pressure Drop"]),
    # Static pressure
    ("cim-d:staticPressure",
     None,
     ["Static Pressure", "External Static Pressure", "External Static Presure"]),
    # Power / apparent load
    ("cim-d:ratedPower",
     ["Electrical - Loads", "Electrical"],
     ["Apparent Load", "Power"]),
    # Dimensional — width
    ("cim-d:nominalWidth",
     ["Dimensions"],
     ["Width", "Diffuser Width"]),
    # Dimensional — height
    ("cim-d:nominalHeight",
     ["Dimensions"],
     ["Height", "Diffuser Height"]),
]


def _get_psets_manual(element, model):
    """Fallback when ifcopenshell.util.element.get_psets is unavailable."""
    result: dict[str, dict[str, object]] = {}
    for rel in model.by_type("IfcRelDefinesByProperties"):
        if element not in rel.RelatedObjects:
            continue
        pset = rel.RelatingPropertyDefinition
        if pset.is_a("IfcPropertySet"):
            props = {}
            for prop in pset.HasProperties:
                if prop.is_a("IfcPropertySingleValue") and prop.NominalValue is not None:
                    props[prop.Name] = prop.NominalValue.wrappedValue
            if props:
                result[pset.Name] = props
    return result


def get_element_psets(element, model):
    if USE_GET_PSETS:
        return get_psets(element)
    return _get_psets_manual(element, model)


def extract_numeric(value) -> float | None:
    """Try to coerce a property value to a float."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        # Strip units/currency and try parsing
        cleaned = re.sub(r"[^\d.\-eE+]", "", value.strip())
        if cleaned:
            try:
                return float(cleaned)
            except ValueError:
                return None
    return None


def extract_properties(psets: dict, rules: list) -> dict[str, float]:
    """Apply extraction rules to a dict of property sets, return {cim_prop: value}."""
    extracted: dict[str, float] = {}
    for cim_prop, pset_names, prop_names in rules:
        if cim_prop in extracted:
            continue
        # Determine which psets to search
        search_psets = {}
        if pset_names is None:
            search_psets = psets
        else:
            for pn in pset_names:
                if pn in psets:
                    search_psets[pn] = psets[pn]
        # Search for property names
        for _pset_name, props in search_psets.items():
            for target_name in prop_names:
                if target_name in props:
                    val = extract_numeric(props[target_name])
                    if val is not None and val != 0.0:
                        extracted[cim_prop] = val
                        break
            if cim_prop in extracted:
                break
    return extracted


def build_abox_gid_index(abox_path: Path) -> dict[str, str]:
    """
    Parse the ABox Turtle file to build {ifcGlobalId -> inst:LOCAL_NAME}.
    We use a regex approach since the file is simple and well-structured.
    """
    text = abox_path.read_text(encoding="utf-8")
    # Pattern: inst:SOME_ID ... cim:ifcGlobalId "GUID" .
    # Instances span multiple lines — find (inst:XXX, globalId) pairs.
    inst_pattern = re.compile(
        r'^(inst:\S+)\s+a\s+\S+',
        re.MULTILINE,
    )
    gid_pattern = re.compile(
        r'cim:ifcGlobalId\s+"([^"]+)"',
    )

    gid_to_inst: dict[str, str] = {}
    # Split by blank lines to get blocks
    blocks = re.split(r'\n\s*\n', text)
    for block in blocks:
        inst_m = inst_pattern.search(block)
        gid_m = gid_pattern.search(block)
        if inst_m and gid_m:
            inst_uri = inst_m.group(1)
            gid = gid_m.group(1)
            gid_to_inst[gid] = inst_uri
    return gid_to_inst


def format_decimal(val: float) -> str:
    """Format a float for Turtle xsd:decimal."""
    if val == int(val) and abs(val) < 1e12:
        return f"{int(val)}.0"
    # Use enough precision
    formatted = f"{val:.6f}".rstrip("0")
    if formatted.endswith("."):
        formatted += "0"
    return formatted


def main():
    print("=" * 72)
    print("Step 9: IFC PropertySet Extraction → CIM ABox Enrichment")
    print("=" * 72)

    # ------------------------------------------------------------------
    # 1. Open IFC
    # ------------------------------------------------------------------
    print(f"\n[1] Opening IFC file: {IFC_PATH.name}")
    model = ifcopenshell.open(str(IFC_PATH))
    print(f"    Schema: {model.schema}")

    # ------------------------------------------------------------------
    # 2. Extract properties from target entities
    # ------------------------------------------------------------------
    print("\n[2] Extracting PropertySet values from target IFC entities...")
    # {global_id: {cim_prop: value}}
    ifc_data: dict[str, dict[str, float]] = {}
    ifc_meta: dict[str, str] = {}  # gid -> element name for debug
    entity_counts: dict[str, int] = Counter()
    prop_frequency: Counter = Counter()

    for ifc_type in TARGET_TYPES:
        elements = model.by_type(ifc_type)
        for el in elements:
            gid = el.GlobalId
            psets = get_element_psets(el, model)
            extracted = extract_properties(psets, EXTRACTION_RULES)
            if extracted:
                ifc_data[gid] = extracted
                ifc_meta[gid] = el.Name or "(unnamed)"
                entity_counts[ifc_type] += 1
                for prop_name in extracted:
                    prop_frequency[prop_name] += 1

    total_with_data = len(ifc_data)
    print(f"    Entities with extractable PSet data: {total_with_data}")
    for ifc_type, cnt in sorted(entity_counts.items()):
        print(f"      {ifc_type}: {cnt}")

    # ------------------------------------------------------------------
    # 3. Build ABox GlobalId index
    # ------------------------------------------------------------------
    print(f"\n[3] Indexing ABox instances from: {ABOX_PATH.name}")
    gid_to_inst = build_abox_gid_index(ABOX_PATH)
    print(f"    ABox instances with ifcGlobalId: {len(gid_to_inst)}")

    # ------------------------------------------------------------------
    # 4. Match & generate enrichment triples
    # ------------------------------------------------------------------
    print("\n[4] Matching IFC data to ABox instances...")
    matched: dict[str, tuple[str, dict[str, float]]] = {}
    unmatched_gids: list[str] = []

    for gid, props in ifc_data.items():
        if gid in gid_to_inst:
            matched[gid] = (gid_to_inst[gid], props)
        else:
            unmatched_gids.append(gid)

    print(f"    Matched to ABox: {len(matched)}")
    print(f"    Unmatched (no ABox instance): {len(unmatched_gids)}")

    # ------------------------------------------------------------------
    # 5. Write enrichment Turtle
    # ------------------------------------------------------------------
    print(f"\n[5] Writing enrichment Turtle to: {OUT_PATH.name}")
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    lines.append("# =============================================================================")
    lines.append("# CIM ABox Enrichment — IFC PropertySet Quantitative Data")
    lines.append(f"# Generated by step9_pset_extraction.py on {date.today().isoformat()}")
    lines.append(f"# Source: {IFC_PATH.name}")
    lines.append(f"# Matched instances: {len(matched)}")
    lines.append("# =============================================================================")
    lines.append("")
    lines.append("@prefix rdf:       <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .")
    lines.append("@prefix rdfs:      <http://www.w3.org/2000/01/rdf-schema#> .")
    lines.append("@prefix xsd:       <http://www.w3.org/2001/XMLSchema#> .")
    lines.append("")
    lines.append("@prefix cim:       <https://cim.medical/ontology/v3.4#> .")
    lines.append("@prefix cim-d:     <https://cim.medical/ontology/v4.0/design#> .")
    lines.append("@prefix inst:      <https://cim.medical/instance/nbu_medical_clinic/> .")
    lines.append("")

    enriched_prop_counts: Counter = Counter()

    for gid in sorted(matched.keys(), key=lambda g: matched[g][0]):
        inst_uri, props = matched[gid]
        prop_lines = []
        for cim_prop, value in sorted(props.items()):
            dec_str = format_decimal(value)
            prop_lines.append(f'    {cim_prop} "{dec_str}"^^xsd:decimal')
            enriched_prop_counts[cim_prop] += 1

        if prop_lines:
            lines.append(f"# IFC GlobalId: {gid}")
            lines.append(f"{inst_uri}")
            for i, pl in enumerate(prop_lines):
                sep = " ;" if i < len(prop_lines) - 1 else " ."
                lines.append(pl + sep)
            lines.append("")

    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"    Written {len(lines)} lines")

    # ------------------------------------------------------------------
    # 6. Summary
    # ------------------------------------------------------------------
    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"  IFC entities scanned (target types):     "
          f"{sum(len(model.by_type(t)) for t in TARGET_TYPES)}")
    print(f"  Entities with extractable PSet data:     {total_with_data}")
    print(f"  Matched to ABox instances:               {len(matched)}")
    print(f"  Unmatched (no ABox instance):             {len(unmatched_gids)}")
    print()
    print("  Properties found (frequency):")
    for prop, cnt in prop_frequency.most_common():
        print(f"    {prop:40s} {cnt:>5d}")
    print()
    print("  Enrichment triples written (by property):")
    for prop, cnt in enriched_prop_counts.most_common():
        print(f"    {prop:40s} {cnt:>5d}")
    print()
    print(f"  Output file: {OUT_PATH}")
    print("=" * 72)


if __name__ == "__main__":
    main()
