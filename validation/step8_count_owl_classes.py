#!/usr/bin/env python3
"""
Step 8: owl:Class 权威计数
统计口径: 所有被 _index_v4.ttl 直接或间接 import 的 TTL 文件
+ v3.4 遗留模块 (equipment/spaces/control/metering)
"""
from rdflib import Graph, OWL, RDF, RDFS
from pathlib import Path
from collections import Counter
import json

BASE = Path(__file__).parent.parent / "project_deliverables/version02/cim"

# 待加载的TTL文件
TTL_FILES = sorted(set([
    *BASE.glob("ontology/*.ttl"),
    *BASE.glob("ontology/bridge/*.ttl"),
    *BASE.glob("equipment/*.ttl"),
    *BASE.glob("spaces/*.ttl"),
    *BASE.glob("control/*.ttl"),
    *BASE.glob("metering/*.ttl"),
    *BASE.glob("coupling/*.ttl"),
    *([BASE / "ontology_skeleton.ttl"] if (BASE / "ontology_skeleton.ttl").exists() else []),
]))

g = Graph()
parse_errors = []
loaded_files = []
for ttl in TTL_FILES:
    if not ttl.exists():
        continue
    try:
        g.parse(str(ttl), format="turtle")
        loaded_files.append(str(ttl.relative_to(BASE.parent.parent)))
    except Exception as e:
        parse_errors.append(f"{ttl.name}: {e}")

# Count owl:Class (explicit declarations)
classes_explicit = sorted(set(
    str(s) for s, p, o in g.triples((None, RDF.type, OWL.Class))
    if not str(s).startswith("_")
))

# Also count rdfs:subClassOf subjects (some classes declared only via subClassOf)
subclass_subjects = set(
    str(s) for s, p, o in g.triples((None, RDFS.subClassOf, None))
    if not str(s).startswith("_") and not str(s).startswith("http://www.w3.org")
    and not str(s).startswith("http://purl.obolibrary.org")
)

# Union
all_classes = sorted(set(classes_explicit) | subclass_subjects)

# Separate: v4.0 ontology/ only
v4_classes = [c for c in all_classes if "v4.0" in c or "v3.4" in c]

# By namespace
ns_counts = Counter()
for c in all_classes:
    ns = c.rsplit("#", 1)[0] if "#" in c else c.rsplit("/", 1)[0]
    ns_counts[ns] += 1

print(f"\n{'='*60}")
print(f"  CIM owl:Class 权威计数")
print(f"{'='*60}")
print(f"\n  口径 A (a owl:Class 显式声明):     {len(classes_explicit)}")
print(f"  口径 B (A + rdfs:subClassOf 主语): {len(all_classes)}")
print(f"  加载文件数:                         {len(loaded_files)}")
print(f"  总三元组:                           {len(g)}")

print(f"\n按命名空间分布 (口径 B):")
for ns, cnt in ns_counts.most_common():
    print(f"  {cnt:>4}  {ns}")

if parse_errors:
    print(f"\n解析失败 ({len(parse_errors)}):")
    for e in parse_errors:
        print(f"  ⚠️  {e}")

# Save
out = Path(__file__).parent / "owl_class_count_report.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump({
        "count_explicit_owl_class": len(classes_explicit),
        "count_with_subclass": len(all_classes),
        "by_namespace": dict(ns_counts.most_common()),
        "files_loaded": loaded_files,
        "parse_errors": parse_errors,
        "total_triples": len(g),
    }, f, ensure_ascii=False, indent=2)
print(f"\n详细报告: {out}")
