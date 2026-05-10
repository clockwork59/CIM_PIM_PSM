"""
Generate situation awareness report -- the MVP core display.

Produces a markdown situation report from simulation results, showing:
- Event summary header
- Action progress table with status icons
- BAS commands issued
- Personnel dispatched
- Timeline visualization
- KPI summary
"""

from datetime import datetime


def generate_situation_report(sim_result: dict, event: dict) -> str:
    """
    Generate a markdown situation report from simulation results.

    Args:
        sim_result: Output from ActionChainExecutor.run_simulation()
        event: SecurityEvent.to_dict() output
    Returns:
        Markdown string for the situation awareness display
    """
    lines = []

    # ── Header ──────────────────────────────────────────────────────────────
    lines.append("# 态势感知报告 (Situation Awareness Report)")
    lines.append("")
    lines.append(f"**事件ID**: {event['event_id']}")
    lines.append(f"**事件类型**: {event['event_type']}")
    lines.append(f"**严重等级**: {event['severity']}")
    lines.append(f"**发生位置**: {event['location']}")
    lines.append(f"**触发设备**: {event['device_id']}")
    lines.append(f"**事件时间**: {event['timestamp']}")
    lines.append(f"**当前状态**: {event['status']}")
    lines.append(f"**匹配预案**: {sim_result['plan_id']} ({sim_result['plan_name']})")
    lines.append("")

    # ── KPI Summary ─────────────────────────────────────────────────────────
    lines.append("## KPI 指标")
    lines.append("")
    lines.append(f"| 指标 | 值 |")
    lines.append(f"|------|-----|")
    lines.append(f"| 总动作数 | {sim_result['total_actions']} |")
    lines.append(f"| 已完成 | {sim_result['completed']} |")
    lines.append(f"| 已超时 | {sim_result['timed_out']} |")
    lines.append(f"| 仿真总时长 | {sim_result['total_simulated_time_sec']}s |")
    lines.append(f"| 等级时限 | {sim_result['severity_limit_sec']}s |")
    pass_fail = "PASS" if sim_result['within_severity_limit'] else "FAIL"
    lines.append(f"| 时限达标 | {pass_fail} |")
    lines.append(f"| 实际运行耗时 | {sim_result['real_elapsed_sec']}s |")
    lines.append("")

    # ── Action Progress Table ───────────────────────────────────────────────
    lines.append("## 动作执行进度")
    lines.append("")
    lines.append("| # | 动作 | Action | 角色 | 模式 | 时限(s) | 耗时(s) | 达标 | 状态 |")
    lines.append("|---|------|--------|------|------|---------|---------|------|------|")
    for a in sim_result["actions"]:
        dur = f"{a['duration_sec']}" if a['duration_sec'] is not None else "-"
        wl = "Y" if a.get('within_limit') else ("N" if a.get('within_limit') is False else "-")
        status_icon = a.get('status_label', a['status'])
        lines.append(
            f"| {a['id']} | {a['name']} | {a['name_en']} | {a['role']} | "
            f"{a['mode']} | {a['time_limit_sec']} | {dur} | {wl} | {status_icon} |"
        )
    lines.append("")

    # ── BAS Commands ────────────────────────────────────────────────────────
    bas_cmds = sim_result.get("bas_commands_issued", [])
    lines.append(f"## BAS 联动指令 ({len(bas_cmds)} commands)")
    lines.append("")
    if bas_cmds:
        lines.append("| # | 指令 | 来源动作 | 下发时间 |")
        lines.append("|---|------|----------|----------|")
        for i, cmd in enumerate(bas_cmds, 1):
            lines.append(
                f"| {i} | {cmd['command']} | "
                f"[{cmd['action_id']}] {cmd['action_name']} | {cmd['issued_at']} |"
            )
    else:
        lines.append("(none)")
    lines.append("")

    # ── Personnel Dispatched ────────────────────────────────────────────────
    dispatched = {}
    for a in sim_result["actions"]:
        if a["role"] != "SYSTEM" and a.get("dispatched_to"):
            role = a["role"]
            if role not in dispatched:
                dispatched[role] = []
            dispatched[role].append(f"[{a['id']}] {a['name']}")

    lines.append(f"## 人员调度 ({len(dispatched)} roles)")
    lines.append("")
    if dispatched:
        lines.append("| 角色 | 调度标签 | 执行动作 |")
        lines.append("|------|----------|----------|")
        for role, tasks in dispatched.items():
            # Find label from any action with this dispatched_to
            label = next(
                (a["dispatched_to"] for a in sim_result["actions"] if a["role"] == role and a.get("dispatched_to")),
                role,
            )
            lines.append(f"| {role} | {label} | {', '.join(tasks)} |")
    lines.append("")

    # ── Event State Transitions ─────────────────────────────────────────────
    transitions = event.get("transitions", [])
    lines.append(f"## 事件状态转换 ({len(transitions)} transitions)")
    lines.append("")
    if transitions:
        lines.append("| # | 从 | 到 | 时间 |")
        lines.append("|---|----|----|------|")
        for i, t in enumerate(transitions, 1):
            lines.append(f"| {i} | {t['from']} | {t['to']} | {t['time']} |")
    lines.append("")

    # ── Event Log (Timeline) ────────────────────────────────────────────────
    event_log = sim_result.get("event_log", [])
    lines.append(f"## 事件时间线 ({len(event_log)} entries)")
    lines.append("")
    lines.append("```")
    for entry in event_log:
        ts = entry.get("time", "")
        if ts and len(ts) > 19:
            ts = ts[:19]  # trim microseconds
        action_id = entry.get("action_id", "")
        action = entry.get("action", "")
        evt = entry.get("event", "")
        extra = ""
        if evt == "COMPLETE":
            dur = entry.get("duration_sec", "?")
            wl = "OK" if entry.get("within_limit") else "OVER"
            extra = f" [{dur}s] {wl}"
        elif evt == "START":
            extra = f" -> {entry.get('executor', '')}"
        lines.append(f"  {ts}  [{action_id:>2}] {action:<8} {evt}{extra}")
    lines.append("```")
    lines.append("")

    # ── Footer ──────────────────────────────────────────────────────────────
    lines.append("---")
    lines.append(f"*Generated: {datetime.now().isoformat()[:19]}*")
    lines.append(f"*Plan: {sim_result['plan_id']} {sim_result.get('plan_version', '')}*")
    lines.append(f"*Ontology: cim-se:SituationAwareness / cim-se:EventClosureReport*")
    lines.append("")

    return "\n".join(lines)


def generate_event_timeline(sim_result: dict) -> str:
    """Generate a standalone timeline markdown from simulation results."""
    lines = []
    lines.append("# Event Execution Timeline")
    lines.append("")
    lines.append(f"**Plan**: {sim_result['plan_id']} -- {sim_result['plan_name']}")
    lines.append(f"**Total simulated time**: {sim_result['total_simulated_time_sec']}s")
    lines.append("")

    # Build a Gantt-like text representation
    lines.append("## Action Gantt (text)")
    lines.append("")
    lines.append("```")
    lines.append(f"{'Action':<20} {'Role':<22} {'Duration':>8}  Bar")
    lines.append("-" * 75)

    max_time = max(
        (a["duration_sec"] for a in sim_result["actions"] if a["duration_sec"]),
        default=1,
    )
    bar_width = 30

    for a in sim_result["actions"]:
        dur = a["duration_sec"] if a["duration_sec"] else 0
        bar_len = int((dur / max_time) * bar_width) if max_time > 0 else 0
        bar = "=" * max(bar_len, 1)
        mode_marker = "[A]" if a["mode"] == "AutomaticExecution" else "[M]"
        lines.append(f"{a['name']:<20} {a['role']:<22} {dur:>7.1f}s  {mode_marker}{bar}")
    lines.append("```")
    lines.append("")
    lines.append("Legend: [A] = Automatic, [M] = Manual")
    lines.append("")
    return "\n".join(lines)
