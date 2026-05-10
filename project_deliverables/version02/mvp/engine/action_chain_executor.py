"""
Action chain executor -- resolves dependencies, dispatches tasks, tracks completion.

Core engine for the safety MVP simulation. Parses the plan JSON, builds a dependency
graph, executes actions in topological order (parallel where dependencies allow),
simulates timing for both automatic and manual actions, and produces a full event log.

Aligned with cim-se:ActionChain / cim-se:ActionNode / cim-se:ActionStatus ontology.
"""

import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
from pathlib import Path


class ActionStatus(Enum):
    """Maps to cim-se:ActionStatus individuals."""
    PENDING     = "PENDING     等待中"
    IN_PROGRESS = "IN_PROGRESS 进行中"
    COMPLETED   = "COMPLETED   已完成"
    TIMED_OUT   = "TIMED_OUT   已超时"
    SKIPPED     = "SKIPPED     已跳过"


# Display icons
ACTION_ICONS = {
    ActionStatus.PENDING:     "⏳",
    ActionStatus.IN_PROGRESS: "🔥",
    ActionStatus.COMPLETED:   "✅",
    ActionStatus.TIMED_OUT:   "⏰",
    ActionStatus.SKIPPED:     "⏭️",
}


@dataclass
class ActionExecution:
    """Runtime state for a single action node execution."""
    action_id: int
    name: str
    name_en: str
    role: str
    mode: str
    time_limit: int               # seconds
    depends_on: list
    bas_command: Optional[str]
    status: ActionStatus = ActionStatus.PENDING
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    dispatched_to: Optional[str] = None

    @property
    def actual_duration(self) -> Optional[float]:
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

    @property
    def is_overdue(self) -> bool:
        if self.start_time and not self.end_time:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            return elapsed > self.time_limit
        return False

    @property
    def icon(self) -> str:
        return ACTION_ICONS.get(self.status, "?")


class ActionChainExecutor:
    """
    Loads a plan JSON and executes the action chain with simulated timing.

    Execution rules:
    - Actions with no unmet dependencies are "ready" and can start in parallel
    - AutomaticExecution actions complete instantly (simulated BAS command)
    - ManualExecution / ManualConfirmation actions simulate human response time
    - Each action has a time_limit; exceeding it marks TIMED_OUT
    """

    def __init__(self, plan_path: str | Path):
        with open(plan_path, encoding="utf-8") as f:
            self.plan = json.load(f)
        self.actions: dict[int, ActionExecution] = {}
        for a in self.plan["actions"]:
            self.actions[a["id"]] = ActionExecution(
                action_id=a["id"],
                name=a["name"],
                name_en=a.get("name_en", a["name"]),
                role=a["role"],
                mode=a["mode"],
                time_limit=a["time_limit_sec"],
                depends_on=a["depends_on"],
                bas_command=a.get("bas_command"),
            )
        self.event_log: list[dict] = []
        self.bas_commands_issued: list[dict] = []

    def can_start(self, action_id: int) -> bool:
        """Check if all dependencies are completed."""
        action = self.actions[action_id]
        if action.status != ActionStatus.PENDING:
            return False
        for dep_id in action.depends_on:
            if self.actions[dep_id].status != ActionStatus.COMPLETED:
                return False
        return True

    def get_ready_actions(self) -> list[int]:
        """Return all actions whose dependencies are satisfied (parallel dispatch)."""
        return [aid for aid in self.actions if self.can_start(aid)]

    def start_action(self, action_id: int, executor: str = "SYSTEM") -> dict:
        """Mark an action as started and log the event."""
        action = self.actions[action_id]
        action.status = ActionStatus.IN_PROGRESS
        action.start_time = datetime.now()
        action.dispatched_to = executor
        entry = {
            "time": action.start_time.isoformat(),
            "action_id": action_id,
            "action": action.name,
            "action_en": action.name_en,
            "event": "START",
            "executor": executor,
            "mode": action.mode,
        }
        self.event_log.append(entry)
        return entry

    def complete_action(self, action_id: int, sim_duration: float = 0) -> dict:
        """Mark an action as completed and log the event."""
        action = self.actions[action_id]
        # Simulate elapsed time
        if sim_duration > 0 and action.start_time:
            action.end_time = action.start_time + timedelta(seconds=sim_duration)
        else:
            action.end_time = datetime.now()
        action.status = ActionStatus.COMPLETED
        duration = action.actual_duration or 0
        within_limit = duration <= action.time_limit

        # Track BAS commands
        if action.bas_command:
            self.bas_commands_issued.append({
                "command": action.bas_command,
                "action_id": action_id,
                "action_name": action.name,
                "issued_at": action.start_time.isoformat() if action.start_time else None,
            })

        entry = {
            "time": action.end_time.isoformat() if action.end_time else None,
            "action_id": action_id,
            "action": action.name,
            "action_en": action.name_en,
            "event": "COMPLETE",
            "duration_sec": round(duration, 1),
            "within_limit": within_limit,
        }
        self.event_log.append(entry)
        return entry

    def run_simulation(self, speed_factor: float = 100.0) -> dict:
        """
        Run the full action chain simulation with accelerated time.

        speed_factor=100 means 1 real second = 100 simulated seconds.
        Manual actions simulate completion at ~70% of their time limit.
        Automatic actions complete near-instantly.
        """
        sim_start = datetime.now()
        total_sim_time = 0.0
        iteration = 0
        max_iterations = 100  # safety guard

        while iteration < max_iterations:
            iteration += 1
            ready = self.get_ready_actions()

            if not ready:
                # Check if all done or deadlocked
                pending_or_ip = [
                    a for a in self.actions.values()
                    if a.status in (ActionStatus.PENDING, ActionStatus.IN_PROGRESS)
                ]
                if not pending_or_ip:
                    break  # all done

                # Complete any in-progress actions
                in_progress = [
                    a for a in self.actions.values()
                    if a.status == ActionStatus.IN_PROGRESS
                ]
                if not in_progress:
                    break  # deadlock

                # Simulate fastest in-progress action completing
                fastest = min(in_progress, key=lambda a: a.time_limit)
                sim_duration = fastest.time_limit * 0.7
                real_wait = sim_duration / speed_factor
                time.sleep(min(real_wait, 0.05))
                total_sim_time += sim_duration
                self.complete_action(fastest.action_id, sim_duration)
                continue

            # Start all ready actions
            for aid in ready:
                action = self.actions[aid]
                if action.mode == "AutomaticExecution":
                    # Auto actions: start and complete immediately
                    self.start_action(aid, "SYSTEM")
                    sim_duration = min(action.time_limit * 0.3, 10)
                    total_sim_time += sim_duration
                    self.complete_action(aid, sim_duration)
                else:
                    # Human actions: start, will be completed in next iteration
                    role_label = self.plan["roles"].get(action.role, {}).get("label", action.role)
                    self.start_action(aid, role_label)

        sim_end = datetime.now()

        # Build per-action summary
        action_summaries = []
        for a in self.actions.values():
            action_summaries.append({
                "id": a.action_id,
                "name": a.name,
                "name_en": a.name_en,
                "role": a.role,
                "status": a.status.name,
                "status_label": a.icon + " " + a.status.value,
                "mode": a.mode,
                "time_limit_sec": a.time_limit,
                "duration_sec": round(a.actual_duration, 1) if a.actual_duration else None,
                "within_limit": (a.actual_duration <= a.time_limit) if a.actual_duration else None,
                "bas_command": a.bas_command,
                "dispatched_to": a.dispatched_to,
            })

        return {
            "plan_id": self.plan["plan_id"],
            "plan_name": self.plan["plan_name"],
            "plan_version": self.plan["version"],
            "total_actions": len(self.actions),
            "completed": sum(1 for a in self.actions.values() if a.status == ActionStatus.COMPLETED),
            "timed_out": sum(1 for a in self.actions.values() if a.status == ActionStatus.TIMED_OUT),
            "skipped": sum(1 for a in self.actions.values() if a.status == ActionStatus.SKIPPED),
            "total_simulated_time_sec": round(total_sim_time, 1),
            "real_elapsed_sec": round((sim_end - sim_start).total_seconds(), 3),
            "severity_limit_sec": self.plan["severity_limits"].get("L2", 900),
            "within_severity_limit": total_sim_time <= self.plan["severity_limits"].get("L2", 900),
            "bas_commands_issued": self.bas_commands_issued,
            "actions": action_summaries,
            "event_log": self.event_log,
        }
