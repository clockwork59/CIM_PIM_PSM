# PIM 规划报告 — 手术部仿真场景

**生成时间**: 2026-05-10 01:30  
**CIM 本体版本**: v4.0.0  
**场景**: 医院手术部（I级 OR×1 + III级 OR×2 + ICU×1）

## 执行摘要

| 阶段门控 | 通过 | 警告 | 失败 |
|---------|------|------|------|
| 数量 | 3 | 3 | 0 |

**总缺口数**: 36  |  **紧急(CRITICAL)**: 0  |  **主要(MAJOR)**: 0  |  **次要(MINOR)**: 36

## 各阶段详情

### 阶段 1 — Briefing / 策划阶段  ✅ PASS

缺口统计: 紧急 **0** | 主要 **0** | 次要 **0**

> 该阶段无缺口，门控通过。

### 阶段 2 — Schematic Design / 初步设计  ✅ PASS

缺口统计: 紧急 **0** | 主要 **0** | 次要 **0**

> 该阶段无缺口，门控通过。

### 阶段 3 — Detailed Design / 施工图  ⚠️ WARN

缺口统计: 紧急 **0** | 主要 **0** | 次要 **12**

#### 规范合规 (SHACL/Standards)

| ID | 等级 | 实体 | 描述 | 规范依据 |
|----|------|------|------|---------|
| SHACL-001 | **MINOR** | OR_02 | [SHACL] III级洁净手术室 OR-02: I级手术室洁净等级必须为 ISO-5 (属性: cleanliness… |  |
| SHACL-002 | **MINOR** | OR_03 | [SHACL] III级洁净手术室 OR-03: I级手术室洁净等级必须为 ISO-5 (属性: cleanliness… |  |
| SHACL-003 | **MINOR** | OR_01 | [SHACL] I级洁净手术室 OR-01: I级手术室洁净等级必须为 ISO-5 (属性: cleanlinessCl… |  |
| SHACL-004 | **MINOR** | OR_02 | [SHACL] III级洁净手术室 OR-02: II级手术室洁净等级必须为 ISO-6 (属性: cleanlines… |  |
| SHACL-005 | **MINOR** | OR_03 | [SHACL] III级洁净手术室 OR-03: II级手术室洁净等级必须为 ISO-6 (属性: cleanlines… |  |
| SHACL-006 | **MINOR** | OR_01 | [SHACL] I级洁净手术室 OR-01: II级手术室洁净等级必须为 ISO-6 (属性: cleanlinessC… |  |
| SHACL-007 | **MINOR** | OR_02 | [SHACL] III级洁净手术室 OR-02: Node <http://cim.medical/instance/s… |  |
| SHACL-008 | **MINOR** | OR_03 | [SHACL] III级洁净手术室 OR-03: Node <http://cim.medical/instance/s… |  |
| SHACL-009 | **MINOR** | OR_01 | [SHACL] I级洁净手术室 OR-01: Node <http://cim.medical/instance/sur… |  |
| SHACL-010 | **MINOR** | OR_02 | [SHACL] III级洁净手术室 OR-02: Node <http://cim.medical/instance/s… |  |
| SHACL-011 | **MINOR** | OR_03 | [SHACL] III级洁净手术室 OR-03: Node <http://cim.medical/instance/s… |  |
| SHACL-012 | **MINOR** | OR_01 | [SHACL] I级洁净手术室 OR-01: Node <http://cim.medical/instance/sur… |  |

#### 修复建议

- ⚪ `SHACL-001` — 修复 III级洁净手术室 OR-02 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-002` — 修复 III级洁净手术室 OR-03 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-003` — 修复 I级洁净手术室 OR-01 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-004` — 修复 III级洁净手术室 OR-02 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-005` — 修复 III级洁净手术室 OR-03 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-006` — 修复 I级洁净手术室 OR-01 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-007` — 修复 III级洁净手术室 OR-02 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-008` — 修复 III级洁净手术室 OR-03 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-009` — 修复 I级洁净手术室 OR-01 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-010` — 修复 III级洁净手术室 OR-02 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-011` — 修复 III级洁净手术室 OR-03 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-012` — 修复 I级洁净手术室 OR-01 的 cleanlinessClass 属性以满足 SHACL 约束

### 阶段 4 — Procurement / 招投标  ⚠️ WARN

缺口统计: 紧急 **0** | 主要 **0** | 次要 **12**

#### 规范合规 (SHACL/Standards)

| ID | 等级 | 实体 | 描述 | 规范依据 |
|----|------|------|------|---------|
| SHACL-001 | **MINOR** | OR_02 | [SHACL] III级洁净手术室 OR-02: I级手术室洁净等级必须为 ISO-5 (属性: cleanliness… |  |
| SHACL-002 | **MINOR** | OR_03 | [SHACL] III级洁净手术室 OR-03: I级手术室洁净等级必须为 ISO-5 (属性: cleanliness… |  |
| SHACL-003 | **MINOR** | OR_01 | [SHACL] I级洁净手术室 OR-01: I级手术室洁净等级必须为 ISO-5 (属性: cleanlinessCl… |  |
| SHACL-004 | **MINOR** | OR_02 | [SHACL] III级洁净手术室 OR-02: II级手术室洁净等级必须为 ISO-6 (属性: cleanlines… |  |
| SHACL-005 | **MINOR** | OR_03 | [SHACL] III级洁净手术室 OR-03: II级手术室洁净等级必须为 ISO-6 (属性: cleanlines… |  |
| SHACL-006 | **MINOR** | OR_01 | [SHACL] I级洁净手术室 OR-01: II级手术室洁净等级必须为 ISO-6 (属性: cleanlinessC… |  |
| SHACL-007 | **MINOR** | OR_02 | [SHACL] III级洁净手术室 OR-02: Node <http://cim.medical/instance/s… |  |
| SHACL-008 | **MINOR** | OR_03 | [SHACL] III级洁净手术室 OR-03: Node <http://cim.medical/instance/s… |  |
| SHACL-009 | **MINOR** | OR_01 | [SHACL] I级洁净手术室 OR-01: Node <http://cim.medical/instance/sur… |  |
| SHACL-010 | **MINOR** | OR_02 | [SHACL] III级洁净手术室 OR-02: Node <http://cim.medical/instance/s… |  |
| SHACL-011 | **MINOR** | OR_03 | [SHACL] III级洁净手术室 OR-03: Node <http://cim.medical/instance/s… |  |
| SHACL-012 | **MINOR** | OR_01 | [SHACL] I级洁净手术室 OR-01: Node <http://cim.medical/instance/sur… |  |

#### 修复建议

- ⚪ `SHACL-001` — 修复 III级洁净手术室 OR-02 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-002` — 修复 III级洁净手术室 OR-03 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-003` — 修复 I级洁净手术室 OR-01 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-004` — 修复 III级洁净手术室 OR-02 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-005` — 修复 III级洁净手术室 OR-03 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-006` — 修复 I级洁净手术室 OR-01 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-007` — 修复 III级洁净手术室 OR-02 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-008` — 修复 III级洁净手术室 OR-03 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-009` — 修复 I级洁净手术室 OR-01 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-010` — 修复 III级洁净手术室 OR-02 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-011` — 修复 III级洁净手术室 OR-03 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-012` — 修复 I级洁净手术室 OR-01 的 cleanlinessClass 属性以满足 SHACL 约束

### 阶段 5 — Construction / 施工安装  ✅ PASS

缺口统计: 紧急 **0** | 主要 **0** | 次要 **0**

> 该阶段无缺口，门控通过。

### 阶段 6 — Commissioning / 调试验收  ⚠️ WARN

缺口统计: 紧急 **0** | 主要 **0** | 次要 **12**

#### 规范合规 (SHACL/Standards)

| ID | 等级 | 实体 | 描述 | 规范依据 |
|----|------|------|------|---------|
| SHACL-001 | **MINOR** | OR_02 | [SHACL] III级洁净手术室 OR-02: I级手术室洁净等级必须为 ISO-5 (属性: cleanliness… |  |
| SHACL-002 | **MINOR** | OR_03 | [SHACL] III级洁净手术室 OR-03: I级手术室洁净等级必须为 ISO-5 (属性: cleanliness… |  |
| SHACL-003 | **MINOR** | OR_01 | [SHACL] I级洁净手术室 OR-01: I级手术室洁净等级必须为 ISO-5 (属性: cleanlinessCl… |  |
| SHACL-004 | **MINOR** | OR_02 | [SHACL] III级洁净手术室 OR-02: II级手术室洁净等级必须为 ISO-6 (属性: cleanlines… |  |
| SHACL-005 | **MINOR** | OR_03 | [SHACL] III级洁净手术室 OR-03: II级手术室洁净等级必须为 ISO-6 (属性: cleanlines… |  |
| SHACL-006 | **MINOR** | OR_01 | [SHACL] I级洁净手术室 OR-01: II级手术室洁净等级必须为 ISO-6 (属性: cleanlinessC… |  |
| SHACL-007 | **MINOR** | OR_02 | [SHACL] III级洁净手术室 OR-02: Node <http://cim.medical/instance/s… |  |
| SHACL-008 | **MINOR** | OR_03 | [SHACL] III级洁净手术室 OR-03: Node <http://cim.medical/instance/s… |  |
| SHACL-009 | **MINOR** | OR_01 | [SHACL] I级洁净手术室 OR-01: Node <http://cim.medical/instance/sur… |  |
| SHACL-010 | **MINOR** | OR_02 | [SHACL] III级洁净手术室 OR-02: Node <http://cim.medical/instance/s… |  |
| SHACL-011 | **MINOR** | OR_03 | [SHACL] III级洁净手术室 OR-03: Node <http://cim.medical/instance/s… |  |
| SHACL-012 | **MINOR** | OR_01 | [SHACL] I级洁净手术室 OR-01: Node <http://cim.medical/instance/sur… |  |

#### 修复建议

- ⚪ `SHACL-001` — 修复 III级洁净手术室 OR-02 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-002` — 修复 III级洁净手术室 OR-03 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-003` — 修复 I级洁净手术室 OR-01 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-004` — 修复 III级洁净手术室 OR-02 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-005` — 修复 III级洁净手术室 OR-03 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-006` — 修复 I级洁净手术室 OR-01 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-007` — 修复 III级洁净手术室 OR-02 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-008` — 修复 III级洁净手术室 OR-03 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-009` — 修复 I级洁净手术室 OR-01 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-010` — 修复 III级洁净手术室 OR-02 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-011` — 修复 III级洁净手术室 OR-03 的 cleanlinessClass 属性以满足 SHACL 约束
- ⚪ `SHACL-012` — 修复 I级洁净手术室 OR-01 的 cleanlinessClass 属性以满足 SHACL 约束

## PIM 行动计划

### 空间信息 (Space Info)

**阶段 3 待办:**
- [ ] [SHACL-001] 修复 III级洁净手术室 OR-02 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-002] 修复 III级洁净手术室 OR-03 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-003] 修复 I级洁净手术室 OR-01 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-004] 修复 III级洁净手术室 OR-02 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-005] 修复 III级洁净手术室 OR-03 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-006] 修复 I级洁净手术室 OR-01 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-007] 修复 III级洁净手术室 OR-02 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-008] 修复 III级洁净手术室 OR-03 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-009] 修复 I级洁净手术室 OR-01 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-010] 修复 III级洁净手术室 OR-02 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-011] 修复 III级洁净手术室 OR-03 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-012] 修复 I级洁净手术室 OR-01 的 cleanlinessClass 属性以满足 SHACL 约束

**阶段 4 待办:**
- [ ] [SHACL-001] 修复 III级洁净手术室 OR-02 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-002] 修复 III级洁净手术室 OR-03 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-003] 修复 I级洁净手术室 OR-01 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-004] 修复 III级洁净手术室 OR-02 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-005] 修复 III级洁净手术室 OR-03 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-006] 修复 I级洁净手术室 OR-01 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-007] 修复 III级洁净手术室 OR-02 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-008] 修复 III级洁净手术室 OR-03 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-009] 修复 I级洁净手术室 OR-01 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-010] 修复 III级洁净手术室 OR-02 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-011] 修复 III级洁净手术室 OR-03 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-012] 修复 I级洁净手术室 OR-01 的 cleanlinessClass 属性以满足 SHACL 约束

**阶段 6 待办:**
- [ ] [SHACL-001] 修复 III级洁净手术室 OR-02 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-002] 修复 III级洁净手术室 OR-03 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-003] 修复 I级洁净手术室 OR-01 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-004] 修复 III级洁净手术室 OR-02 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-005] 修复 III级洁净手术室 OR-03 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-006] 修复 I级洁净手术室 OR-01 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-007] 修复 III级洁净手术室 OR-02 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-008] 修复 III级洁净手术室 OR-03 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-009] 修复 I级洁净手术室 OR-01 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-010] 修复 III级洁净手术室 OR-02 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-011] 修复 III级洁净手术室 OR-03 的 cleanlinessClass 属性以满足 SHACL 约束
- [ ] [SHACL-012] 修复 I级洁净手术室 OR-01 的 cleanlinessClass 属性以满足 SHACL 约束

## 规范合规清单

| 要求 | 规范依据 | 状态 | 涉及实体 |
|------|---------|------|---------|
| I级OR换气次数≥36次/h | GB50333-2013 表6.4.1 | OR_01已声明(40次/h) | OR_01 |
| III级OR换气次数≥20次/h | GB50333-2013 表6.4.1 | ⚠️ OR_02/03缺失 | OR_02, OR_03 |
| OR正压差≥+8Pa | GB50333-2013 §6.5.2 | ⚠️ OR_02/03缺失声明 | OR_02, OR_03 |
| ICU正压差要求 | WS/T 311 | ❌ ICU_Zone缺少pressureClass | ICU_Zone |
| OR温度21–25°C | GB50333-2013 §6.6 | OR_01已关联准则 | OR_01 |
| 每间OR ≥2个O₂终端 | WS435-2013 §7.2 | ❌ OR_02/03无终端 | OR_02, OR_03 |
| IT隔离电源 | IEC 60364-7-710 | ❌ OR_02/03无IT面板 | OR_02, OR_03 |
| 应急电源冗余N+1 | 医建规范 | OR_01链路完整 | DieselGenerator, UPS |
