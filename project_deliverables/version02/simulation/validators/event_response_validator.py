"""Emergency response plan completeness and timeline validation engine.

Validates that emergency plans in the ABox are structurally complete,
action chains are properly ordered and free of circular dependencies,
response timelines comply with severity-based limits, responder roles
are resolvable, and automatic actions carry BAS command references.
"""
from typing import List, Dict, Set, Optional
from datetime import datetime
from rdflib import Graph, RDF, URIRef, Literal
from rdflib.namespace import RDFS, XSD
from ..core.stage_gate_engine import GapItem, StageConfig
from ..core.namespace_registry import CIM, CIM_SE


# ── Severity-level response time limits (seconds) ──────────────────────────
SEVERITY_TIME_LIMITS: Dict[str, int] = {
    str(CIM_SE.SeverityL1): 1800,
    str(CIM_SE.SeverityL2): 900,
    str(CIM_SE.SeverityL3): 300,
}

# Action time tolerance (20 %)
ACTION_TIME_TOLERANCE = 1.20

# Required datatype properties on ActionNode
REQUIRED_ACTION_NODE_PROPS = [
    CIM_SE.actionSequence,
    CIM_SE.actionTimeLimit,
]
# Required object properties on ActionNode (assignedToRole only for non-automatic actions)
REQUIRED_ACTION_NODE_OBJ_PROPS = [
    CIM_SE.hasExecutionMode,
]


def check_event_response(graph: Graph, abox: Graph, cfg: StageConfig) -> List[GapItem]:
    """Check emergency response plan completeness and timeline integrity.

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
        Detected gaps in emergency response plans.
    """
    gaps: List[GapItem] = []
    counter = [0]

    def next_id(prefix: str) -> str:
        counter[0] += 1
        return f"EVTR-{prefix}-{counter[0]:03d}"

    # Event response validation is relevant from LOD 300 (Detailed Design)
    if cfg.lod_level < 300:
        return gaps

    # 1. Plan completeness
    gaps.extend(_check_plan_completeness(graph, abox, next_id))

    # 2. Action chain integrity
    gaps.extend(_check_action_chain_integrity(graph, abox, next_id))

    # 3. Timeline validation
    gaps.extend(_check_timeline(graph, abox, next_id))

    # 4. Role coverage
    gaps.extend(_check_role_coverage(graph, abox, next_id))

    # 5. BAS command validation
    gaps.extend(_check_bas_commands(graph, abox, next_id))

    return gaps


# ═════════════════════════════════════════════════════════════════════════════
# 1. Plan Completeness
# ═════════════════════════════════════════════════════════════════════════════

def _check_plan_completeness(graph: Graph, abox: Graph, next_id) -> List[GapItem]:
    """Every EmergencyPlan must have actionChain, triggerCondition, planVersion."""
    gaps: List[GapItem] = []

    plan_classes = [CIM_SE.EmergencyPlan, CIM_SE.FireResponsePlan, CIM_SE.EvacuationPlan]
    plans: Set[URIRef] = set()
    for pcls in plan_classes:
        for s in abox.subjects(RDF.type, pcls):
            plans.add(s)

    for plan in sorted(plans, key=str):
        missing: List[str] = []

        # hasActionChain -> ActionChain
        chains = list(abox.objects(plan, CIM_SE.hasActionChain))
        if not chains:
            missing.append("hasActionChain")
        else:
            # At least one ActionNode in the chain
            for chain in chains:
                nodes = list(abox.objects(chain, CIM_SE.hasActionNode))
                if not nodes:
                    missing.append(f"hasActionNode on chain {chain}")

        # hasTriggerCondition
        triggers = list(abox.objects(plan, CIM_SE.hasTriggerCondition))
        if not triggers:
            missing.append("hasTriggerCondition")

        # planVersion
        versions = list(abox.objects(plan, CIM_SE.planVersion))
        if not versions:
            missing.append("planVersion")

        if missing:
            gaps.append(GapItem(
                gap_id=next_id("PLAN"),
                severity="CRITICAL",
                category="event_response",
                entity=str(plan),
                entity_type="EmergencyPlan",
                description=f"Emergency plan incomplete: missing {', '.join(missing)}",
                standard_reference="GB/T 38315-2019",
                remediation="Add missing plan components to ensure completeness",
                blocking_next_stage=True,
            ))

    return gaps


# ═════════════════════════════════════════════════════════════════════════════
# 2. Action Chain Integrity
# ═════════════════════════════════════════════════════════════════════════════

def _check_action_chain_integrity(graph: Graph, abox: Graph, next_id) -> List[GapItem]:
    """Validate required properties and dependency ordering on ActionNodes."""
    gaps: List[GapItem] = []

    chain_classes = [CIM_SE.ActionChain]
    chains: Set[URIRef] = set()
    for ccls in chain_classes:
        for s in abox.subjects(RDF.type, ccls):
            chains.add(s)

    for chain in sorted(chains, key=str):
        nodes = list(abox.objects(chain, CIM_SE.hasActionNode))
        node_seq: Dict[URIRef, int] = {}

        for node in nodes:
            # Check required datatype properties
            for prop in REQUIRED_ACTION_NODE_PROPS:
                vals = list(abox.objects(node, prop))
                if not vals:
                    prop_name = str(prop).split("#")[-1]
                    gaps.append(GapItem(
                        gap_id=next_id("ACHN"),
                        severity="MAJOR",
                        category="event_response",
                        entity=str(node),
                        entity_type="ActionNode",
                        description=f"ActionNode missing required property: {prop_name}",
                        remediation=f"Add {prop_name} to ActionNode {node}",
                    ))

            # Check required object properties
            for prop in REQUIRED_ACTION_NODE_OBJ_PROPS:
                vals = list(abox.objects(node, prop))
                if not vals:
                    prop_name = str(prop).split("#")[-1]
                    gaps.append(GapItem(
                        gap_id=next_id("ACHN"),
                        severity="MAJOR",
                        category="event_response",
                        entity=str(node),
                        entity_type="ActionNode",
                        description=f"ActionNode missing required property: {prop_name}",
                        remediation=f"Add {prop_name} to ActionNode {node}",
                    ))

            # Record sequence number for dependency check
            seq_vals = list(abox.objects(node, CIM_SE.actionSequence))
            if seq_vals:
                try:
                    node_seq[node] = int(seq_vals[0])
                except (ValueError, TypeError):
                    pass

        # Dependency ordering validation
        for node in nodes:
            deps = list(abox.objects(node, CIM_SE.dependsOnAction))
            for dep in deps:
                if node in node_seq and dep in node_seq:
                    if node_seq[dep] >= node_seq[node]:
                        gaps.append(GapItem(
                            gap_id=next_id("ACHN"),
                            severity="MAJOR",
                            category="event_response",
                            entity=str(node),
                            entity_type="ActionNode",
                            description=(
                                f"Dependency ordering violation: node seq={node_seq[node]} "
                                f"depends on node seq={node_seq[dep]} "
                                f"(dependency must have lower sequence number)"
                            ),
                            remediation="Fix action sequence numbers to respect dependency ordering",
                        ))

        # Circular dependency detection (DFS)
        circular = _detect_circular_deps(nodes, abox)
        if circular:
            gaps.append(GapItem(
                gap_id=next_id("ACHN"),
                severity="MAJOR",
                category="event_response",
                entity=str(chain),
                entity_type="ActionChain",
                description=f"Circular dependency detected in action chain: {circular}",
                remediation="Remove circular dependencies among action nodes",
            ))

    return gaps


def _detect_circular_deps(nodes: list, abox: Graph) -> Optional[str]:
    """Detect circular dependencies via DFS; return cycle description or None."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color: Dict[URIRef, int] = {n: WHITE for n in nodes}
    node_set = set(nodes)

    def dfs(u: URIRef) -> Optional[str]:
        color[u] = GRAY
        for v in abox.objects(u, CIM_SE.dependsOnAction):
            if v not in node_set:
                continue
            if color.get(v) == GRAY:
                return f"{u} -> {v} (back edge)"
            if color.get(v) == WHITE:
                result = dfs(v)
                if result:
                    return result
        color[u] = BLACK
        return None

    for node in nodes:
        if color[node] == WHITE:
            result = dfs(node)
            if result:
                return result
    return None


# ═════════════════════════════════════════════════════════════════════════════
# 3. Timeline Validation
# ═════════════════════════════════════════════════════════════════════════════

def _check_timeline(graph: Graph, abox: Graph, next_id) -> List[GapItem]:
    """Check action time limits and overall event response time compliance."""
    gaps: List[GapItem] = []

    # Find SecurityEvents with InProgress or Closed status
    active_statuses = {CIM_SE.StatusInProgress, CIM_SE.StatusClosed}
    events: Set[URIRef] = set()
    for s in abox.subjects(RDF.type, CIM_SE.SecurityEvent):
        events.add(s)
    # Also check subclasses
    for subcls in [CIM_SE.FireEvent, CIM_SE.IntrusionEvent,
                   CIM_SE.EquipmentFailureEvent, CIM_SE.MedicalEmergencyEvent]:
        for s in abox.subjects(RDF.type, subcls):
            events.add(s)

    for event in sorted(events, key=str):
        status_vals = list(abox.objects(event, CIM_SE.hasEventStatus))
        if not any(URIRef(str(st)) in active_statuses for st in status_vals):
            continue

        # Find matched plan and its action chains
        plans = list(abox.objects(event, CIM_SE.matchesPlan))
        all_nodes: List[URIRef] = []
        for plan in plans:
            for chain in abox.objects(plan, CIM_SE.hasActionChain):
                for node in abox.objects(chain, CIM_SE.hasActionNode):
                    all_nodes.append(node)

        earliest_start = None
        latest_end = None

        for node in all_nodes:
            start_vals = list(abox.objects(node, CIM_SE.actionStartTime))
            end_vals = list(abox.objects(node, CIM_SE.actionEndTime))

            if start_vals and end_vals:
                try:
                    start_dt = _parse_datetime(str(start_vals[0]))
                    end_dt = _parse_datetime(str(end_vals[0]))
                except (ValueError, TypeError):
                    continue

                # Verify end > start
                if end_dt <= start_dt:
                    gaps.append(GapItem(
                        gap_id=next_id("TIME"),
                        severity="MAJOR",
                        category="event_response",
                        entity=str(node),
                        entity_type="ActionNode",
                        description=(
                            f"actionEndTime ({end_dt}) <= actionStartTime ({start_dt})"
                        ),
                        remediation="Fix action timestamps to ensure end > start",
                    ))
                    continue

                actual_duration = (end_dt - start_dt).total_seconds()

                # Check against actionTimeLimit with 20% tolerance
                limit_vals = list(abox.objects(node, CIM_SE.actionTimeLimit))
                if limit_vals:
                    try:
                        time_limit = int(limit_vals[0])
                        if actual_duration > time_limit * ACTION_TIME_TOLERANCE:
                            gaps.append(GapItem(
                                gap_id=next_id("TIME"),
                                severity="MAJOR",
                                category="event_response",
                                entity=str(node),
                                entity_type="ActionNode",
                                description=(
                                    f"Action overtime: actual {actual_duration:.0f}s "
                                    f"> limit {time_limit}s (+20% tolerance = "
                                    f"{time_limit * ACTION_TIME_TOLERANCE:.0f}s)"
                                ),
                                remediation="Investigate cause of action delay",
                            ))
                    except (ValueError, TypeError):
                        pass

                # Track overall event timeline
                if earliest_start is None or start_dt < earliest_start:
                    earliest_start = start_dt
                if latest_end is None or end_dt > latest_end:
                    latest_end = end_dt

        # Event total time vs severity response time limit
        if earliest_start and latest_end:
            total_time = (latest_end - earliest_start).total_seconds()
            severity_vals = list(abox.objects(event, CIM_SE.hasSeverityLevel))
            for sev in severity_vals:
                sev_str = str(sev)
                if sev_str in SEVERITY_TIME_LIMITS:
                    limit = SEVERITY_TIME_LIMITS[sev_str]
                    if total_time > limit:
                        gaps.append(GapItem(
                            gap_id=next_id("TIME"),
                            severity="CRITICAL",
                            category="event_response",
                            entity=str(event),
                            entity_type="SecurityEvent",
                            description=(
                                f"Event total response time {total_time:.0f}s "
                                f"exceeds severity limit {limit}s"
                            ),
                            standard_reference="GB/T 38315-2019",
                            remediation="Optimize response workflow to meet time target",
                            blocking_next_stage=True,
                        ))

    return gaps


def _parse_datetime(value: str) -> datetime:
    """Parse xsd:dateTime string to Python datetime."""
    # Handle common xsd:dateTime formats
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S.%f%z"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse datetime: {value}")


# ═════════════════════════════════════════════════════════════════════════════
# 4. Role Coverage
# ═════════════════════════════════════════════════════════════════════════════

def _check_role_coverage(graph: Graph, abox: Graph, next_id) -> List[GapItem]:
    """Verify human role assignments and role existence."""
    gaps: List[GapItem] = []

    plan_classes = [CIM_SE.EmergencyPlan, CIM_SE.FireResponsePlan, CIM_SE.EvacuationPlan]
    plans: Set[URIRef] = set()
    for pcls in plan_classes:
        for s in abox.subjects(RDF.type, pcls):
            plans.add(s)

    # Collect all known ResponderRole instances from the full graph
    known_roles: Set[URIRef] = set()
    for s in graph.subjects(RDF.type, CIM_SE.ResponderRole):
        known_roles.add(s)

    for plan in sorted(plans, key=str):
        chains = list(abox.objects(plan, CIM_SE.hasActionChain))
        has_human_role = False
        all_nodes: List[URIRef] = []

        for chain in chains:
            for node in abox.objects(chain, CIM_SE.hasActionNode):
                all_nodes.append(node)

        for node in all_nodes:
            roles = list(abox.objects(node, CIM_SE.assignedToRole))
            exec_modes = list(abox.objects(node, CIM_SE.hasExecutionMode))

            # Check if any role is a human (non-automatic) role
            is_auto = any(
                URIRef(str(m)) == CIM_SE.AutomaticExecution for m in exec_modes
            )
            if roles and not is_auto:
                has_human_role = True

            # Verify all referenced roles exist
            for role in roles:
                if URIRef(str(role)) not in known_roles:
                    gaps.append(GapItem(
                        gap_id=next_id("ROLE"),
                        severity="MAJOR",
                        category="event_response",
                        entity=str(role),
                        entity_type="ResponderRole",
                        description=f"Referenced ResponderRole not found in graph: {role}",
                        remediation="Define the ResponderRole or fix the reference",
                    ))

        if all_nodes and not has_human_role:
            gaps.append(GapItem(
                gap_id=next_id("ROLE"),
                severity="MAJOR",
                category="event_response",
                entity=str(plan),
                entity_type="EmergencyPlan",
                description="Emergency plan has no human-assigned action nodes",
                remediation="At least one action node must be assigned to a human role",
            ))

    return gaps


# ═════════════════════════════════════════════════════════════════════════════
# 5. BAS Command Validation
# ═════════════════════════════════════════════════════════════════════════════

def _check_bas_commands(graph: Graph, abox: Graph, next_id) -> List[GapItem]:
    """Automatic actions should reference a BAS command."""
    gaps: List[GapItem] = []

    for node in abox.subjects(RDF.type, CIM_SE.ActionNode):
        exec_modes = list(abox.objects(node, CIM_SE.hasExecutionMode))
        is_auto = any(
            URIRef(str(m)) == CIM_SE.AutomaticExecution for m in exec_modes
        )
        if not is_auto:
            continue

        bas_cmds = list(abox.objects(node, CIM_SE.issuesBASCommand))
        if not bas_cmds:
            gaps.append(GapItem(
                gap_id=next_id("BAS"),
                severity="MINOR",
                category="event_response",
                entity=str(node),
                entity_type="ActionNode",
                description="Automatic action has no issuesBASCommand (may be notification-only)",
                remediation="Add BAS command reference if this is a BAS-controlled action",
            ))

    return gaps
