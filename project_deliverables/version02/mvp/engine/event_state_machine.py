"""
Event state machine: PendingConfirmation -> Confirmed -> InProgress -> Closed -> Archived

5-state lifecycle for SecurityEvent, aligned with cim-se:EventStatus ontology classes:
  cim-se:StatusPendingConfirmation -> cim-se:StatusConfirmed -> cim-se:StatusInProgress
  -> cim-se:StatusClosed -> cim-se:StatusArchived

False alarm shortcut: PENDING -> ARCHIVED (skip intermediate states)
"""

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


class EventStatus(Enum):
    """Maps 1:1 to cim-se:EventStatus individuals."""
    PENDING = "待确认"         # cim-se:StatusPendingConfirmation
    CONFIRMED = "已确认"       # cim-se:StatusConfirmed
    IN_PROGRESS = "处理中"     # cim-se:StatusInProgress
    CLOSED = "已闭环"          # cim-se:StatusClosed
    ARCHIVED = "已归档"        # cim-se:StatusArchived


# Valid state transitions (directed edges in the state machine)
VALID_TRANSITIONS = {
    EventStatus.PENDING:     [EventStatus.CONFIRMED, EventStatus.ARCHIVED],  # confirmed or false alarm
    EventStatus.CONFIRMED:   [EventStatus.IN_PROGRESS],
    EventStatus.IN_PROGRESS: [EventStatus.CLOSED],
    EventStatus.CLOSED:      [EventStatus.ARCHIVED],
    EventStatus.ARCHIVED:    [],
}

# Display icons for terminal rendering
STATUS_ICONS = {
    EventStatus.PENDING:     "🔔",
    EventStatus.CONFIRMED:   "⚠️",
    EventStatus.IN_PROGRESS: "🔥",
    EventStatus.CLOSED:      "✅",
    EventStatus.ARCHIVED:    "📦",
}


@dataclass
class SecurityEvent:
    """
    Runtime representation of a cim-se:SecurityEvent instance.
    Tracks state transitions with timestamps for audit trail.
    """
    event_id: str                          # e.g. EVT-20240115-001
    event_type: str                        # FireEvent / IntrusionEvent / ...
    severity: str                          # L1 / L2 / L3
    location: str                          # human-readable location
    device_id: str                         # triggering device ID
    status: EventStatus = EventStatus.PENDING
    timestamp: datetime = field(default_factory=datetime.now)
    plan_id: Optional[str] = None          # matched emergency plan
    transitions: list = field(default_factory=list)

    def transition_to(self, new_status: EventStatus) -> bool:
        """
        Attempt a state transition. Returns True if valid, False if rejected.
        Records transition with timestamp for audit trail.
        """
        if new_status not in VALID_TRANSITIONS[self.status]:
            return False
        old = self.status
        self.status = new_status
        self.transitions.append({
            "from": old.value,
            "to": new_status.value,
            "time": datetime.now().isoformat(),
        })
        return True

    @property
    def icon(self) -> str:
        return STATUS_ICONS.get(self.status, "?")

    @property
    def elapsed_seconds(self) -> float:
        """Seconds since event creation."""
        return (datetime.now() - self.timestamp).total_seconds()

    def to_dict(self) -> dict:
        """Serialize to JSON-compatible dict."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "severity": self.severity,
            "location": self.location,
            "device_id": self.device_id,
            "status": self.status.value,
            "timestamp": self.timestamp.isoformat(),
            "plan_id": self.plan_id,
            "transitions": self.transitions,
        }

    def __str__(self) -> str:
        return (
            f"{self.icon} [{self.event_id}] {self.event_type} "
            f"| {self.severity} | {self.status.value} | {self.location}"
        )
