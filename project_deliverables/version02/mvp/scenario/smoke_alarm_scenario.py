#!/usr/bin/env python3
"""
MVP Safety Simulation -- Smoke Alarm Fire Response (L2 Electrical Fire)

Full lifecycle simulation:
  1. Create SecurityEvent (smoke alarm in 5F electrical room)
  2. Load L2 fire response plan from config/
  3. State machine: PENDING -> CONFIRMED -> IN_PROGRESS
  4. Execute action chain (10 actions with dependency resolution)
  5. State machine: IN_PROGRESS -> CLOSED -> ARCHIVED
  6. Generate situation report + JSON output
  7. Print terminal dashboard

Usage:
    python project_deliverables/version02/mvp/scenario/smoke_alarm_scenario.py

Ontology alignment:
    cim-se:FireEvent + cim-se:FireResponsePlan + cim-se:ActionChain
    smoke_alarm_drill.ttl ABox scenario data
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Resolve project paths
SCRIPT_DIR = Path(__file__).resolve().parent
MVP_ROOT = SCRIPT_DIR.parent
ENGINE_DIR = MVP_ROOT / "engine"
CONFIG_DIR = MVP_ROOT / "config"
OUTPUT_DIR = MVP_ROOT / "output"

# Add engine to path
sys.path.insert(0, str(MVP_ROOT))

from engine.event_state_machine import SecurityEvent, EventStatus
from engine.action_chain_executor import ActionChainExecutor
from engine.situation_report import generate_situation_report, generate_event_timeline


def print_header():
    """Print simulation header banner."""
    print("=" * 72)
    print("  CIM Safety MVP -- L2 Electrical Fire Response Simulation")
    print("  CIM 安防 MVP -- L2级电气火灾处置仿真")
    print("=" * 72)
    print()


def print_state_transition(event: SecurityEvent, new_status: EventStatus):
    """Print and execute a state transition."""
    old_icon = event.icon
    old_status = event.status.value
    success = event.transition_to(new_status)
    if success:
        print(f"  {old_icon} {old_status}  -->  {event.icon} {event.status.value}")
    else:
        print(f"  [REJECTED] Cannot transition from {old_status} to {new_status.value}")
    return success


def print_action_table(sim_result: dict):
    """Print the action execution summary table."""
    print()
    print("-" * 72)
    print(f"  {'#':>2}  {'Action':<20} {'Role':<22} {'Time':>7}  {'Status'}")
    print("-" * 72)
    for a in sim_result["actions"]:
        dur = f"{a['duration_sec']:.1f}s" if a['duration_sec'] is not None else "  -  "
        print(f"  {a['id']:>2}  {a['name']:<20} {a['role']:<22} {dur:>7}  {a['status_label']}")
    print("-" * 72)


def print_bas_commands(sim_result: dict):
    """Print BAS commands issued."""
    cmds = sim_result.get("bas_commands_issued", [])
    print(f"\n  BAS Commands Issued: {len(cmds)}")
    for cmd in cmds:
        print(f"    -> {cmd['command']}  (from [{cmd['action_id']}] {cmd['action_name']})")


def print_kpi(sim_result: dict):
    """Print KPI summary."""
    print()
    print("  KPI Summary:")
    print(f"    Total actions:       {sim_result['total_actions']}")
    print(f"    Completed:           {sim_result['completed']}")
    print(f"    Timed out:           {sim_result['timed_out']}")
    print(f"    Simulated time:      {sim_result['total_simulated_time_sec']}s")
    print(f"    Severity limit (L2): {sim_result['severity_limit_sec']}s")
    verdict = "PASS" if sim_result['within_severity_limit'] else "FAIL"
    print(f"    Within limit:        {verdict}")
    print(f"    Real elapsed:        {sim_result['real_elapsed_sec']}s")


def run():
    """Main simulation entry point."""
    print_header()

    # ── Step 1: Create SecurityEvent ────────────────────────────────────────
    print("[Step 1] Creating SecurityEvent (smoke alarm in 5F electrical room)...")
    event = SecurityEvent(
        event_id="EVT-20240115-001",
        event_type="FireEvent",
        severity="L2",
        location="内科楼5F配电室",
        device_id="SD-5F-ER-001",
        timestamp=datetime.now(),
    )
    print(f"  {event}")
    print()

    # ── Step 2: Load plan ───────────────────────────────────────────────────
    plan_path = CONFIG_DIR / "plan_l2_electrical_fire.json"
    print(f"[Step 2] Loading plan: {plan_path.name}")
    executor = ActionChainExecutor(plan_path)
    event.plan_id = executor.plan["plan_id"]
    print(f"  Plan: {executor.plan['plan_id']} -- {executor.plan['plan_name']}")
    print(f"  Actions: {len(executor.actions)}")
    print(f"  Roles: {', '.join(executor.plan['roles'].keys())}")
    print()

    # ── Step 3: State transitions PENDING -> CONFIRMED -> IN_PROGRESS ──────
    print("[Step 3] Event state machine transitions:")
    print_state_transition(event, EventStatus.CONFIRMED)
    print_state_transition(event, EventStatus.IN_PROGRESS)
    print()

    # ── Step 4: Execute action chain ────────────────────────────────────────
    print("[Step 4] Executing action chain (10 actions)...")
    sim_result = executor.run_simulation(speed_factor=200.0)
    print_action_table(sim_result)
    print_bas_commands(sim_result)
    print_kpi(sim_result)
    print()

    # ── Step 5: State transitions IN_PROGRESS -> CLOSED -> ARCHIVED ────────
    print("[Step 5] Closing event:")
    print_state_transition(event, EventStatus.CLOSED)
    print_state_transition(event, EventStatus.ARCHIVED)
    print()

    # ── Step 6: Generate reports ────────────────────────────────────────────
    print("[Step 6] Generating reports...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Situation report (markdown)
    sit_report = generate_situation_report(sim_result, event.to_dict())
    sit_path = OUTPUT_DIR / "situation_report.md"
    sit_path.write_text(sit_report, encoding="utf-8")
    print(f"  -> {sit_path.relative_to(MVP_ROOT)}")

    # Simulation result (JSON)
    result_path = OUTPUT_DIR / "simulation_result.json"
    full_result = {
        "event": event.to_dict(),
        "simulation": sim_result,
        "generated_at": datetime.now().isoformat(),
    }
    result_path.write_text(
        json.dumps(full_result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"  -> {result_path.relative_to(MVP_ROOT)}")

    # Event timeline (markdown)
    timeline = generate_event_timeline(sim_result)
    timeline_path = OUTPUT_DIR / "event_timeline.md"
    timeline_path.write_text(timeline, encoding="utf-8")
    print(f"  -> {timeline_path.relative_to(MVP_ROOT)}")

    # ── Step 7: Final summary ───────────────────────────────────────────────
    print()
    print("=" * 72)
    print("  SIMULATION COMPLETE")
    print(f"  Event:  {event}")
    print(f"  Result: {sim_result['completed']}/{sim_result['total_actions']} actions completed")
    bas_count = len(sim_result.get('bas_commands_issued', []))
    print(f"  BAS:    {bas_count} commands issued")
    roles_dispatched = set(
        a['role'] for a in sim_result['actions']
        if a['role'] != 'SYSTEM' and a.get('dispatched_to')
    )
    print(f"  Roles:  {len(roles_dispatched)} roles dispatched ({', '.join(roles_dispatched)})")
    print("=" * 72)

    return full_result


if __name__ == "__main__":
    run()
