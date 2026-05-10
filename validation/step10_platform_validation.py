#!/usr/bin/env python3
"""
Step 10: M4 Platform Validation -- test all SPARQL queries locally

Loads all CIM TBox + ABox into an rdflib ConjunctiveGraph (no Fuseki required),
runs each .sparql file from platform/queries/, and reports results.

Usage:
    python validation/step10_platform_validation.py

Exit codes:
    0 — all queries executed successfully
    1 — one or more queries failed
"""
from __future__ import annotations

import json
import sys
import time
import traceback
from pathlib import Path

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
V02_ROOT = PROJECT_ROOT / "project_deliverables" / "version02"
PLATFORM_DIR = V02_ROOT / "platform"
QUERIES_DIR = PLATFORM_DIR / "queries"

sys.path.insert(0, str(PROJECT_ROOT))


def load_conjunctive_graph():
    """Load all named graphs via load_named_graphs.py."""
    from project_deliverables.version02.platform.load_named_graphs import load_named_graphs
    return load_named_graphs(verbose=True)


def run_single_query(cg, query_path: Path) -> dict:
    """Execute one SPARQL file and return result metadata."""
    query_text = query_path.read_text(encoding="utf-8")
    name = query_path.stem

    t0 = time.time()
    try:
        results = cg.query(query_text)
        elapsed = time.time() - t0

        rows = list(results)
        row_count = len(rows)

        # Extract variable names
        var_names = [str(v) for v in results.vars] if results.vars else []

        # Sample first row for display
        sample = {}
        if rows and var_names:
            first = rows[0]
            sample = {
                var_names[i]: str(val)[:80] if val is not None else None
                for i, val in enumerate(first)
            }

        return {
            "query": name,
            "status": "PASS",
            "rows": row_count,
            "vars": var_names,
            "elapsed_ms": round(elapsed * 1000, 1),
            "sample": sample,
        }

    except Exception as exc:
        elapsed = time.time() - t0
        return {
            "query": name,
            "status": "FAIL",
            "rows": 0,
            "vars": [],
            "elapsed_ms": round(elapsed * 1000, 1),
            "error": str(exc),
            "traceback": traceback.format_exc(),
        }


def run_named_graph_test(cg) -> dict:
    """Test that Named Graph queries work (GRAPH ?g { ... })."""
    query = """
    SELECT ?g (COUNT(?s) AS ?triples)
    WHERE {
        GRAPH ?g { ?s ?p ?o }
    }
    GROUP BY ?g
    ORDER BY DESC(?triples)
    """
    t0 = time.time()
    try:
        results = cg.query(query)
        elapsed = time.time() - t0
        rows = list(results)

        graph_summary = {}
        for row in rows:
            g_name = str(row[0]).split("/")[-1] if row[0] else "default"
            count = int(row[1]) if row[1] else 0
            graph_summary[g_name] = count

        return {
            "query": "NAMED_GRAPH_ENUMERATION",
            "status": "PASS",
            "rows": len(rows),
            "vars": ["graph", "triples"],
            "elapsed_ms": round(elapsed * 1000, 1),
            "sample": graph_summary,
        }
    except Exception as exc:
        elapsed = time.time() - t0
        return {
            "query": "NAMED_GRAPH_ENUMERATION",
            "status": "FAIL",
            "rows": 0,
            "vars": [],
            "elapsed_ms": round(elapsed * 1000, 1),
            "error": str(exc),
        }


def run_cross_graph_test(cg) -> dict:
    """Test cross-graph query: IFC equipment + BAS point from different graphs."""
    query = """
    PREFIX cim:       <https://cim.medical/ontology/v3.4#>
    PREFIX cim-bacnet: <https://cim.medical/ontology/v4.0/bacnet#>
    PREFIX rdfs:      <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?equipID ?pointName ?value
    WHERE {
        ?equip cim:hasEquipmentID ?equipID .
        ?pt cim-bacnet:bacnetPointOf ?equip ;
            cim-bacnet:hasObjectName ?pointName ;
            cim-bacnet:hasPresentValue ?value .
    }
    LIMIT 5
    """
    t0 = time.time()
    try:
        results = cg.query(query)
        elapsed = time.time() - t0
        rows = list(results)
        return {
            "query": "CROSS_GRAPH_IFC_BAS",
            "status": "PASS" if rows else "WARN_EMPTY",
            "rows": len(rows),
            "vars": ["equipID", "pointName", "value"],
            "elapsed_ms": round(elapsed * 1000, 1),
            "sample": {
                str(results.vars[i]): str(rows[0][i])[:60]
                for i in range(len(results.vars))
            } if rows else {},
        }
    except Exception as exc:
        elapsed = time.time() - t0
        return {
            "query": "CROSS_GRAPH_IFC_BAS",
            "status": "FAIL",
            "rows": 0,
            "elapsed_ms": round(elapsed * 1000, 1),
            "error": str(exc),
        }


def main() -> int:
    print("=" * 70)
    print("M4 Platform Validation -- SPARQL Query Test Suite")
    print("=" * 70)
    print()

    # Load graph
    print("Loading ConjunctiveGraph ...")
    cg = load_conjunctive_graph()
    print()

    # Collect all .sparql query files
    query_files = sorted(QUERIES_DIR.glob("*.sparql"))
    if not query_files:
        print("ERROR: No .sparql files found in", QUERIES_DIR)
        return 1

    print(f"Found {len(query_files)} SPARQL query files")
    print("-" * 70)

    results_all: list[dict] = []

    # Run each query file
    for qf in query_files:
        result = run_single_query(cg, qf)
        results_all.append(result)
        status_icon = "PASS" if result["status"] == "PASS" else "FAIL"
        print(f"  [{status_icon}] {result['query']:35s}  rows={result['rows']:>5}  "
              f"time={result['elapsed_ms']:>8.1f}ms")
        if result["status"] == "FAIL":
            print(f"         ERROR: {result.get('error', 'unknown')}")

    print("-" * 70)

    # Named Graph tests
    print("\nNamed Graph integration tests:")
    ng_result = run_named_graph_test(cg)
    results_all.append(ng_result)
    print(f"  [{ng_result['status']}] Named graph enumeration: "
          f"{ng_result['rows']} graphs, {ng_result['elapsed_ms']:.1f}ms")
    if ng_result.get("sample"):
        for gname, cnt in ng_result["sample"].items():
            print(f"         {gname}: {cnt} triples")

    cg_result = run_cross_graph_test(cg)
    results_all.append(cg_result)
    print(f"  [{cg_result['status']}] Cross-graph IFC+BAS join: "
          f"{cg_result['rows']} rows, {cg_result['elapsed_ms']:.1f}ms")

    # Summary
    print("\n" + "=" * 70)
    total = len(results_all)
    passed = sum(1 for r in results_all if r["status"] == "PASS")
    failed = sum(1 for r in results_all if r["status"] == "FAIL")
    warned = sum(1 for r in results_all if "WARN" in r["status"])
    print(f"TOTAL: {total}  PASS: {passed}  FAIL: {failed}  WARN: {warned}")
    print("=" * 70)

    # Write JSON report
    report_path = PROJECT_ROOT / "validation" / "platform_validation_report.json"
    report = {
        "milestone": "M4",
        "test_suite": "platform_sparql_validation",
        "total_queries": total,
        "passed": passed,
        "failed": failed,
        "warned": warned,
        "results": results_all,
    }
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nReport written to: {report_path}")

    return 1 if failed > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
