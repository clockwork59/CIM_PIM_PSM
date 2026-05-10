#!/usr/bin/env python3
"""
ActionExecutor API — CIM MVP Extension (FastAPI)
=================================================
Extends the M4/M5 FastAPI platform with 6 new endpoints for the
宣武安防MVP smoke-alarm incident handling workflow.

New endpoints:
  POST /events                    → Manually create/inject a security event
  GET  /events                    → List all active security events
  GET  /events/{event_id}         → Get event details + action node progress
  POST /events/{event_id}/confirm → Operator confirms alarm (PENDING → CONFIRMED)
  POST /actions/{node_id}/complete → Mark an action node as completed
  GET  /events/{event_id}/timeline → Return full event timeline JSON

Design:
  - Pure in-memory state (dict) + rdflib graph for persistence
  - No framework dependencies beyond FastAPI + rdflib
  - Supports both standalone run and import into existing main.py

Usage (standalone):
    cd project_deliverables/version02
    uvicorn platform.api_mvp_extension:app --reload --port 8001

Import into existing main.py:
    from platform.api_mvp_extension import mvp_router
    app.include_router(mvp_router, prefix="/mvp")

Dependencies: fastapi, uvicorn, rdflib >= 6.0
"""

import sys
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

try:
    from fastapi import FastAPI, HTTPException, APIRouter
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel
except ImportError:
    print("[ERROR] FastAPI not installed. Run: pip install fastapi uvicorn --break-system-packages")
    sys.exit(1)

from rdflib import Graph, Namespace, Literal, URIRef, RDF, RDFS, XSD

# ─────────────────────────────────────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────────────────────────────────────
BASE      = Path(__file__).resolve().parent.parent.parent  # project_deliverables/version02/
ABOX_DIR  = BASE / "cim/abox"
EVENT_TTL = ABOX_DIR / "nbu_security_events.ttl"

# Source files for graph loading
SOURCE_FILES = {
    "IFC":    ABOX_DIR / "nbu_medical_clinic_instances.ttl",
    "FAS":    ABOX_DIR / "nbu_fas_instances.ttl",
    "BAS_T1": ABOX_DIR / "nbu_bas_readings_t1.ttl",
    "DRILL":  BASE / "simulation/scenario/smoke_alarm_drill.ttl",
    "EVENTS": EVENT_TTL,
}

# ─────────────────────────────────────────────────────────────────────────────
# NAMESPACES
# ─────────────────────────────────────────────────────────────────────────────
CIM_SEC  = Namespace("https://cim.medical/ontology/v4.0/security_event#")
SEC_INST = Namespace("https://cim.medical/ontology/v4.0/security_event/instances#")

# ─────────────────────────────────────────────────────────────────────────────
# IN-MEMORY STATE STORE
# ─────────────────────────────────────────────────────────────────────────────

_events: dict[str, dict] = {}       # event_id → event state dict
_action_nodes: dict[str, dict] = {} # node_id → node state dict


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _seq() -> str:
    date_str = datetime.now().strftime("%Y%m%d")
    n = len(_events) + 1
    return f"EVT-{date_str}-{n:03d}"


# L2 Action Plan template (10 steps)
L2_PLAN = [
    {"step": 1,  "slug": "confirm_fire",      "label": "确认火情",     "role": "CTRL", "auto": False, "deps": [],  "timeout": 120},
    {"step": 2,  "slug": "cut_power",         "label": "切断电源",     "role": "SYS",  "auto": True,  "deps": [1], "timeout": 30},
    {"step": 3,  "slug": "start_suppression", "label": "启动灭火",     "role": "ELEC", "auto": False, "deps": [2], "timeout": 300},
    {"step": 4,  "slug": "broadcast",         "label": "区域广播",     "role": "SYS",  "auto": True,  "deps": [1], "timeout": 10},
    {"step": 5,  "slug": "evacuate",          "label": "启动疏散",     "role": "SEC",  "auto": False, "deps": [4], "timeout": 600},
    {"step": 6,  "slug": "open_doors",        "label": "打开门禁",     "role": "SYS",  "auto": True,  "deps": [4], "timeout": 10},
    {"step": 7,  "slug": "elevator_home",     "label": "电梯归首",     "role": "SYS",  "auto": True,  "deps": [1], "timeout": 30},
    {"step": 8,  "slug": "notify_medical",    "label": "通知医护",     "role": "SYS",  "auto": True,  "deps": [1], "timeout": 30},
    {"step": 9,  "slug": "call_119",          "label": "拨打119",      "role": "CTRL", "auto": False, "deps": [3], "timeout": 120},
    {"step": 10, "slug": "notify_leaders",    "label": "通知领导",     "role": "SYS",  "auto": True,  "deps": [1], "timeout": 30},
]


def _make_nodes(event_id: str, auto_execute: bool = True) -> list[dict]:
    """Create runtime action node list for an event."""
    nodes = []
    for step in L2_PLAN:
        node_id = f"{event_id}-STEP-{step['step']:02d}"
        # Auto-execute system actions with dep=[1] immediately when event is CONFIRMED
        if auto_execute and step["auto"] and (1 in step["deps"] or not step["deps"]):
            state = "EXECUTING"
        elif step["step"] == 1:
            state = "EXECUTING"
        else:
            state = "PENDING"

        node = {
            "node_id":   node_id,
            "event_id":  event_id,
            "step":      step["step"],
            "slug":      step["slug"],
            "label":     step["label"],
            "role":      step["role"],
            "auto":      step["auto"],
            "deps":      step["deps"],
            "timeout":   step["timeout"],
            "state":     state,
            "created_at": _now(),
            "started_at": _now() if state == "EXECUTING" else None,
            "completed_at": None,
            "completed_by": None,
            "notes":     None,
        }
        nodes.append(node)
        _action_nodes[node_id] = node
    return nodes


def _check_event_closure(event_id: str) -> bool:
    """Check if all 10 steps are completed and close the event."""
    evt = _events.get(event_id)
    if not evt:
        return False
    nodes = [_action_nodes[n] for n in evt["node_ids"] if n in _action_nodes]
    all_done = all(n["state"] in ("COMPLETED", "SKIPPED") for n in nodes)
    if all_done and evt["state"] not in ("CLOSED_LOOP", "CLOSED"):
        evt["state"] = "CLOSED_LOOP"
        evt["closed_at"] = _now()
        return True
    return False


# ─────────────────────────────────────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────────────────────────────────────

mvp_router = APIRouter(prefix="/mvp", tags=["MVP Security Events"])


# ── Request models ─────────────────────────────────────────────────────────

class EventCreateRequest(BaseModel):
    trigger_device: str = "SD-F5-001"
    zone:           str = "FAS-ZONE-05"
    severity:       str = "L2"
    dual_zone:      bool = True
    notes:          Optional[str] = None


class ActionCompleteRequest(BaseModel):
    completed_by: Optional[str] = "CTRL-DUTY-001"
    notes:        Optional[str] = None


# ── POST /events ────────────────────────────────────────────────────────────

@mvp_router.post("/events", summary="Create / inject a security event")
async def create_event(req: EventCreateRequest):
    """
    Manually inject a SecurityEvent (simulates EventEngine trigger).
    Returns the created event with its full action node list.
    """
    evt_id = _seq()
    state  = "CONFIRMED" if req.dual_zone else "PENDING"

    nodes  = _make_nodes(evt_id, auto_execute=(state == "CONFIRMED"))
    node_ids = [n["node_id"] for n in nodes]

    # Auto-complete system actions immediately if CONFIRMED
    auto_completed = []
    if state == "CONFIRMED":
        for node in nodes:
            if node["auto"] and node["state"] == "EXECUTING":
                node["state"] = "COMPLETED"
                node["completed_at"] = _now()
                node["completed_by"] = "SYSTEM"
                auto_completed.append(node["slug"])

    evt = {
        "event_id":      evt_id,
        "state":         state,
        "severity":      req.severity,
        "trigger_device": req.trigger_device,
        "zone":          req.zone,
        "dual_zone":     req.dual_zone,
        "created_at":    _now(),
        "confirmed_at":  _now() if state == "CONFIRMED" else None,
        "closed_at":     None,
        "node_ids":      node_ids,
        "notes":         req.notes,
    }
    _events[evt_id] = evt

    return {
        "event_id":       evt_id,
        "state":          state,
        "nodes_created":  len(nodes),
        "auto_completed": auto_completed,
        "message":        f"SecurityEvent {evt_id} created. State={state}.",
    }


# ── GET /events ─────────────────────────────────────────────────────────────

@mvp_router.get("/events", summary="List all security events")
async def list_events():
    """Returns all active security events with summary status."""
    result = []
    for evt in _events.values():
        nodes = [_action_nodes[n] for n in evt["node_ids"] if n in _action_nodes]
        completed = sum(1 for n in nodes if n["state"] == "COMPLETED")
        result.append({
            "event_id":      evt["event_id"],
            "state":         evt["state"],
            "severity":      evt["severity"],
            "trigger_device": evt["trigger_device"],
            "zone":          evt["zone"],
            "created_at":    evt["created_at"],
            "progress":      f"{completed}/{len(nodes)}",
        })
    return {"total": len(result), "events": result}


# ── GET /events/{event_id} ──────────────────────────────────────────────────

@mvp_router.get("/events/{event_id}", summary="Get event details and action chain progress")
async def get_event(event_id: str):
    """Returns full event detail including all 10 action node states."""
    evt = _events.get(event_id)
    if not evt:
        raise HTTPException(status_code=404, detail=f"Event {event_id} not found")

    nodes = [_action_nodes[n] for n in evt["node_ids"] if n in _action_nodes]
    completed = sum(1 for n in nodes if n["state"] == "COMPLETED")

    return {
        **evt,
        "progress":  f"{completed}/{len(nodes)}",
        "action_nodes": nodes,
    }


# ── POST /events/{event_id}/confirm ─────────────────────────────────────────

@mvp_router.post("/events/{event_id}/confirm",
                 summary="Operator confirms alarm (PENDING → CONFIRMED)")
async def confirm_event(event_id: str, confirmed_by: str = "CTRL-DUTY-001"):
    """
    中控值班员确认报警。
    Transitions event from PENDING to CONFIRMED and activates the L2 action plan.
    """
    evt = _events.get(event_id)
    if not evt:
        raise HTTPException(status_code=404, detail=f"Event {event_id} not found")

    if evt["state"] == "CONFIRMED":
        return {"message": f"Event {event_id} already CONFIRMED.", "state": "CONFIRMED"}

    if evt["state"] not in ("PENDING",):
        raise HTTPException(status_code=400,
                            detail=f"Cannot confirm event in state {evt['state']}")

    evt["state"]        = "CONFIRMED"
    evt["confirmed_at"] = _now()
    evt["confirmed_by"] = confirmed_by

    # Activate auto system actions
    auto_completed = []
    nodes = [_action_nodes[n] for n in evt["node_ids"] if n in _action_nodes]
    for node in nodes:
        if node["auto"] and (1 in node["deps"] or not node["deps"]):
            node["state"]        = "COMPLETED"
            node["started_at"]   = _now()
            node["completed_at"] = _now()
            node["completed_by"] = "SYSTEM"
            auto_completed.append(node["slug"])

    return {
        "event_id":      event_id,
        "state":         "CONFIRMED",
        "confirmed_by":  confirmed_by,
        "confirmed_at":  evt["confirmed_at"],
        "auto_completed": auto_completed,
        "message":       f"Event confirmed. {len(auto_completed)} system actions auto-executed.",
    }


# ── POST /actions/{node_id}/complete ────────────────────────────────────────

@mvp_router.post("/actions/{node_id}/complete",
                 summary="Mark an action node as completed (human task report)")
async def complete_action(node_id: str, req: ActionCompleteRequest):
    """
    电工班/保安队/中控通过Mobile APP或PC回报动作完成。
    Marks the specified action node as COMPLETED and checks if dependent
    nodes can be activated.
    """
    node = _action_nodes.get(node_id)
    if not node:
        raise HTTPException(status_code=404, detail=f"ActionNode {node_id} not found")

    if node["state"] == "COMPLETED":
        return {"message": f"Node {node_id} already COMPLETED.", "state": "COMPLETED"}

    node["state"]        = "COMPLETED"
    node["completed_at"] = _now()
    node["completed_by"] = req.completed_by
    node["notes"]        = req.notes

    # Unlock dependent nodes
    evt_id = node["event_id"]
    evt    = _events.get(evt_id)
    unlocked = []

    if evt:
        all_nodes = [_action_nodes[n] for n in evt["node_ids"] if n in _action_nodes]
        step_no   = node["step"]

        for n in all_nodes:
            if step_no in n["deps"] and n["state"] == "PENDING":
                n["state"]      = "EXECUTING"
                n["started_at"] = _now()
                # Auto-complete system actions immediately
                if n["auto"]:
                    n["state"]        = "COMPLETED"
                    n["completed_at"] = _now()
                    n["completed_by"] = "SYSTEM"
                unlocked.append(n["slug"])

        # Check overall event closure
        _check_event_closure(evt_id)

    return {
        "node_id":       node_id,
        "state":         "COMPLETED",
        "completed_by":  req.completed_by,
        "completed_at":  node["completed_at"],
        "unlocked_nodes": unlocked,
        "event_state":   evt["state"] if evt else "UNKNOWN",
    }


# ── GET /events/{event_id}/timeline ─────────────────────────────────────────

@mvp_router.get("/events/{event_id}/timeline",
                summary="Return full event timeline for situational awareness")
async def get_timeline(event_id: str):
    """
    Returns a time-ordered list of all events and action completions
    for the specified SecurityEvent. Used by the 态势时序 frontend panel.
    """
    evt = _events.get(event_id)
    if not evt:
        raise HTTPException(status_code=404, detail=f"Event {event_id} not found")

    timeline = []

    # Event creation
    timeline.append({
        "timestamp": evt["created_at"],
        "type":      "EVENT_CREATED",
        "label":     f"烟感报警触发 — {evt['trigger_device']} ({evt['zone']})",
        "state":     "PENDING" if not evt.get("dual_zone") else "PENDING→CONFIRMED",
        "actor":     "SYSTEM",
    })

    # Confirmation
    if evt.get("confirmed_at"):
        timeline.append({
            "timestamp": evt["confirmed_at"],
            "type":      "EVENT_CONFIRMED",
            "label":     "中控确认火情，L2预案激活",
            "state":     "CONFIRMED",
            "actor":     evt.get("confirmed_by", "CTRL"),
        })

    # Action node completions
    nodes = [_action_nodes[n] for n in evt["node_ids"] if n in _action_nodes]
    for node in sorted(nodes, key=lambda n: n.get("completed_at") or "9999"):
        if node.get("completed_at"):
            timeline.append({
                "timestamp":  node["completed_at"],
                "type":       "ACTION_COMPLETED",
                "label":      f"步骤{node['step']} {node['label']}",
                "state":      "COMPLETED",
                "actor":      node.get("completed_by", "?"),
                "node_id":    node["node_id"],
                "auto":       node["auto"],
            })

    # Event closure
    if evt.get("closed_at"):
        timeline.append({
            "timestamp": evt["closed_at"],
            "type":      "EVENT_CLOSED_LOOP",
            "label":     "处置闭环 — 全部动作完成",
            "state":     "CLOSED_LOOP",
            "actor":     "SYSTEM",
        })

    timeline.sort(key=lambda x: x["timestamp"])

    return {
        "event_id":      event_id,
        "event_state":   evt["state"],
        "timeline_items": len(timeline),
        "timeline":      timeline,
    }


# ─────────────────────────────────────────────────────────────────────────────
# STANDALONE APP
# ─────────────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="CIM Security MVP — ActionExecutor API",
    description="宣武安防MVP (烟感) ActionExecutor REST API",
    version="1.0.0-mvp",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(mvp_router)


@app.get("/", include_in_schema=False)
async def root():
    return {
        "service": "CIM Security MVP ActionExecutor API",
        "version": "1.0.0-mvp",
        "docs":    "/docs",
        "endpoints": [
            "POST /mvp/events",
            "GET  /mvp/events",
            "GET  /mvp/events/{event_id}",
            "POST /mvp/events/{event_id}/confirm",
            "POST /mvp/actions/{node_id}/complete",
            "GET  /mvp/events/{event_id}/timeline",
        ],
    }


# ─────────────────────────────────────────────────────────────────────────────
# INTEGRATION HELPER — import into existing main.py
# ─────────────────────────────────────────────────────────────────────────────

"""
To integrate into existing platform/api/main.py, add these lines:

    from platform.api_mvp_extension import mvp_router
    app.include_router(mvp_router)

The existing M4/M5 endpoints (/equipment, /floors, etc.) remain unchanged.
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("platform.api_mvp_extension:app", host="0.0.0.0", port=8001, reload=True)
