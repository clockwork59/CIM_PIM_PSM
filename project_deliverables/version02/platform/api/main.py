#!/usr/bin/env python3
"""
CIM PIM API -- Platform Independent Model REST Service

Provides a RESTful interface to the CIM Medical Building Knowledge Graph.
Connects to Apache Jena Fuseki for SPARQL queries, with fallback to local
rdflib ConjunctiveGraph if Fuseki is unavailable.

Endpoints:
    GET  /api/v1/equipment/{equipment_id}   -- Equipment full status
    GET  /api/v1/floor/{floor_id}/dashboard -- Floor-level dashboard
    GET  /api/v1/maintenance/due            -- Maintenance due within N days
    GET  /api/v1/energy/anomaly             -- Energy anomaly detection
    GET  /api/v1/fas/zone/{zone_id}         -- FAS zone status
    POST /api/v1/sparql                     -- Raw SPARQL query

Usage:
    uvicorn project_deliverables.version02.platform.api.main:app --reload
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse

logger = logging.getLogger("cim-pim-api")

app = FastAPI(
    title="CIM PIM API",
    version="4.0.0",
    description="CIM Medical Building Knowledge Graph REST API",
)

FUSEKI_URL = "http://localhost:3030/cim/sparql"
QUERIES_DIR = Path(__file__).resolve().parent.parent / "queries"
CONTEXT_FILE = Path(__file__).resolve().parent / "jsonld_context.json"

# ---------------------------------------------------------------------------
# JSON-LD context (loaded once at startup)
# ---------------------------------------------------------------------------
_jsonld_context: dict[str, Any] = {}


@app.on_event("startup")
async def _load_context() -> None:
    global _jsonld_context
    if CONTEXT_FILE.exists():
        _jsonld_context = json.loads(CONTEXT_FILE.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# SPARQL execution helper
# ---------------------------------------------------------------------------
async def run_sparql(query: str) -> list[dict[str, Any]]:
    """Execute a SPARQL SELECT query against Fuseki, falling back to local rdflib."""
    # Try Fuseki first
    try:
        import httpx

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                FUSEKI_URL,
                data={"query": query},
                headers={"Accept": "application/sparql-results+json"},
            )
            if resp.status_code == 200:
                data = resp.json()
                bindings = data.get("results", {}).get("bindings", [])
                return [
                    {k: v.get("value") for k, v in row.items()} for row in bindings
                ]
            logger.warning("Fuseki returned %d, falling back to local.", resp.status_code)
    except Exception as exc:
        logger.info("Fuseki unavailable (%s), using local rdflib graph.", exc)

    # Fallback: load local graph
    return _run_local(query)


def _run_local(query: str) -> list[dict[str, Any]]:
    """Run SPARQL against a local rdflib ConjunctiveGraph."""
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
    from project_deliverables.version02.platform.load_named_graphs import load_named_graphs

    cg = load_named_graphs(verbose=False)
    results = cg.query(query)
    rows: list[dict[str, Any]] = []
    if results.vars:
        var_names = [str(v) for v in results.vars]
        for row in results:
            rows.append(
                {var_names[i]: str(val) if val is not None else None for i, val in enumerate(row)}
            )
    return rows


def _load_query(name: str, **replacements: str) -> str:
    """Load a .sparql file from the queries directory."""
    path = QUERIES_DIR / name
    if not path.exists():
        raise HTTPException(status_code=500, detail=f"Query file not found: {name}")
    text = path.read_text(encoding="utf-8")
    for key, val in replacements.items():
        text = text.replace(key, val)
    return text


def _wrap_jsonld(rows: list[dict], query_name: str) -> dict:
    """Wrap SPARQL results in a JSON-LD-ish envelope."""
    return {
        "@context": _jsonld_context.get("@context", {}),
        "query": query_name,
        "resultCount": len(rows),
        "results": rows,
    }


# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------
@app.get("/api/v1/equipment/{equipment_id}")
async def get_equipment(equipment_id: str) -> JSONResponse:
    """Get full status of a single equipment: design + BAS + CMMS."""
    query = _load_query("eq_full_status.sparql")
    # Inject a VALUES clause to filter by equipment ID
    filter_clause = f'FILTER(?equipID = "{equipment_id}")'
    query = query.replace("ORDER BY", f"{filter_clause}\n}}\nORDER BY").replace(
        "\n}\nORDER BY", "\nORDER BY", 1
    )
    # Simpler approach: just add a FILTER before the closing brace
    # Re-load cleanly
    query = _load_query("eq_full_status.sparql")
    inject = f'\n    FILTER(?equipID = "{equipment_id}")\n'
    query = query.replace("\n}\nORDER BY", f"{inject}}}\nORDER BY")
    rows = await run_sparql(query)
    if not rows:
        raise HTTPException(status_code=404, detail=f"Equipment '{equipment_id}' not found")
    return JSONResponse(_wrap_jsonld(rows, "eq_full_status"))


@app.get("/api/v1/floor/{floor_id}/dashboard")
async def floor_dashboard(floor_id: str) -> JSONResponse:
    """Get all equipment and BAS status on a specific floor."""
    query = _load_query("floor_dashboard.sparql")
    inject = f'\n    FILTER(CONTAINS(STR(?floor), "{floor_id}"))\n'
    query = query.replace("\n}\nORDER BY", f"{inject}}}\nORDER BY")
    rows = await run_sparql(query)
    return JSONResponse(_wrap_jsonld(rows, "floor_dashboard"))


@app.get("/api/v1/maintenance/due")
async def maintenance_due(days: int = Query(default=30, ge=1, le=365)) -> JSONResponse:
    """Get work orders due within N days."""
    query = _load_query("maintenance_due_30d.sparql")
    rows = await run_sparql(query)
    return JSONResponse(_wrap_jsonld(rows, "maintenance_due"))


@app.get("/api/v1/energy/anomaly")
async def energy_anomaly(threshold: float = Query(default=1.2, ge=1.0, le=5.0)) -> JSONResponse:
    """Detect equipment where BAS power reading exceeds design rating."""
    query = _load_query("energy_anomaly.sparql")
    # Replace the hardcoded 1.2 threshold
    query = query.replace("FILTER(?ratedPower > 0 && ?ratio > 1.2)",
                          f"FILTER(?ratedPower > 0 && ?ratio > {threshold})")
    rows = await run_sparql(query)
    return JSONResponse(_wrap_jsonld(rows, "energy_anomaly"))


@app.get("/api/v1/fas/zone/{zone_id}")
async def fas_zone(zone_id: str) -> JSONResponse:
    """Get FAS detector states for a specific alarm zone."""
    query = _load_query("fas_zone_status.sparql")
    inject = f'\n    FILTER(?zoneID = "{zone_id}" || CONTAINS(STR(?zoneID), "{zone_id}"))\n'
    query = query.replace("\n}\nORDER BY", f"{inject}}}\nORDER BY")
    rows = await run_sparql(query)
    return JSONResponse(_wrap_jsonld(rows, "fas_zone_status"))


@app.post("/api/v1/sparql")
async def raw_sparql(body: dict) -> JSONResponse:
    """Execute a raw SPARQL query (SELECT only for safety)."""
    query = body.get("query", "")
    if not query.strip():
        raise HTTPException(status_code=400, detail="Missing 'query' field in request body")
    # Safety: only allow SELECT queries
    normalized = query.strip().upper()
    if not normalized.startswith("SELECT") and not normalized.startswith("PREFIX"):
        raise HTTPException(status_code=403, detail="Only SELECT queries are allowed")
    if any(kw in normalized for kw in ("DELETE", "INSERT", "DROP", "CLEAR", "LOAD")):
        raise HTTPException(status_code=403, detail="Mutation queries are not allowed")
    rows = await run_sparql(query)
    return JSONResponse({"resultCount": len(rows), "results": rows})


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "version": "4.0.0", "queries": len(list(QUERIES_DIR.glob("*.sparql")))}
