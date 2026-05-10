# MVP Sprint — Codespace Deployment Guide
# 宣武安防MVP（烟感）— Codespace部署指南

## 前提
M5 Codespace分支 `feature/recent-updates-2026-05` (HEAD: 5f70d56) 已验证28/28 PASS。

---

## Step 1: 复制4个新文件到Codespace

```bash
# 在 Codespace repo 根目录执行:

# 1a. EventEngine
cp mvp_deliverables/platform/event_engine.py \
   project_deliverables/version02/platform/event_engine.py

# 1b. SimClock
cp mvp_deliverables/platform/sim_clock.py \
   project_deliverables/version02/platform/sim_clock.py

# 1c. ActionExecutor API 扩展
cp mvp_deliverables/platform/api_mvp_extension.py \
   project_deliverables/version02/platform/api_mvp_extension.py

# 1d. MVP Frontend
mkdir -p project_deliverables/version02/platform/frontend
cp mvp_deliverables/platform/frontend/index_mvp.html \
   project_deliverables/version02/platform/frontend/index_mvp.html

# 1e. Step 12 验证脚本
cp mvp_deliverables/validation/step12_mvp_validation.py \
   project_deliverables/version02/validation/step12_mvp_validation.py
```

---

## Step 2: 注入烟感报警到BAS t1快照

```bash
cd project_deliverables/version02

# 注入双点报警 (SD-F5-001 + SD-F5-003) → 触发自动确认
python platform/sim_clock.py --run-drill
```

预期输出:
```
[T+00s] Injecting primary alarm: SD-F5-001
[SimClock] ✅ Alarm injected → cim/abox/nbu_bas_readings_t1.ttl
[T+30s] Injecting secondary alarm: SD-F5-003
[SimClock] ✅ Alarm injected → cim/abox/nbu_bas_readings_t1.ttl
[T+31s] Running EventEngine on t1 snapshot...
[EventEngine] 2 alarmed detector(s) found: ['SD-F5-001', 'SD-F5-003']
[EventEngine] ✅ Created EVT-20260510-001: zone=FAS-ZONE-05, state=CONFIRMED (auto, dual-zone), nodes=10
```

---

## Step 3: 运行EventEngine（如果Step 2未自动运行）

```bash
cd project_deliverables/version02
python platform/event_engine.py --snapshot t1
```

验证输出: `nbu_security_events.ttl` 已生成

---

## Step 4: 启动ActionExecutor API

```bash
cd project_deliverables/version02
pip install fastapi uvicorn --break-system-packages

# 独立模式（端口8001）
python -m uvicorn platform.api_mvp_extension:app --reload --port 8001

# 或集成到现有main.py: 在main.py中加入:
# from platform.api_mvp_extension import mvp_router
# app.include_router(mvp_router)
```

验证:
```bash
curl http://localhost:8001/mvp/events
```

---

## Step 5: 运行Step 12验证

```bash
cd project_deliverables/version02
python validation/step12_mvp_validation.py
```

目标: **12/12 PASS** (API未启动时API测试自动SKIP，不影响RDF测试计分)

---

## Step 6: 打开前端

```bash
# 在Codespace中通过端口转发打开:
# Ports → 8001 → Open in Browser
# 然后访问: http://localhost:8001/docs (API文档)

# 前端直接在浏览器打开文件:
# platform/frontend/index_mvp.html
```

---

## Step 7: Git Commit

```bash
cd project_deliverables/version02  # or repo root

git add platform/event_engine.py
git add platform/sim_clock.py
git add platform/api_mvp_extension.py
git add platform/frontend/index_mvp.html
git add validation/step12_mvp_validation.py
git add cim/abox/nbu_security_events.ttl   # generated
git add cim/abox/nbu_bas_readings_t1.ttl   # updated with alarm injection

git commit -m "feat(MVP): smoke alarm incident handling — EventEngine + SimClock + ActionExecutor API + frontend

Components:
- event_engine.py: BAS binary scan → SecurityEvent generation, 30s dual-zone logic
- sim_clock.py: BAS snapshot time progression, alarm injection (SD-F5-001/003)
- api_mvp_extension.py: FastAPI 6 endpoints (create/list/confirm/complete/timeline)
- index_mvp.html: 3-panel dashboard (alarm board + L2 action panel + timeline)
- step12_mvp_validation.py: 12/12 acceptance tests

L2 Action Chain: 10 steps, 6 auto-system + 4 manual operator tasks
Simulation mode: rdflib in-memory, no real BACnet/CMMS connection
Dual-zone logic: single → PENDING, dual → auto-CONFIRMED

Sprint: MVP-2026-05-10"
```

---

## MVP 端到端演示路径

```
1. 打开前端 index_mvp.html
2. 点击 [⚡ 注入烟感报警] → 双点联动 → 事件自动确认
3. 在告警看板看到 EVT-20260510-001 (已确认/L2)
4. 切换到"L2预案执行"面板 → 6个系统步骤自动完成 (绿色)
5. 手动点击步骤3"启动灭火"[完成] → 步骤9"拨打119"解锁
6. 手动点击步骤5"启动疏散"[完成]
7. 手动点击步骤9"拨打119"[完成]
8. 所有10步完成 → 事件状态变为"已闭环"
9. 时序面板显示完整10条时序记录
```

---

## 文件结构（新增）

```
project_deliverables/version02/
├── platform/
│   ├── event_engine.py          ← NEW: smoke alarm → SecurityEvent
│   ├── sim_clock.py             ← NEW: BAS snapshot + alarm injection
│   ├── api_mvp_extension.py     ← NEW: 6 ActionExecutor endpoints
│   └── frontend/
│       ├── index.html           (M5 existing)
│       └── index_mvp.html       ← NEW: alarm board + action panel + timeline
└── validation/
    └── step12_mvp_validation.py ← NEW: 12/12 acceptance tests
```
