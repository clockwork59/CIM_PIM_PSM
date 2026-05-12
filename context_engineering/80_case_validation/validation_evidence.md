# CIM 验证证据链

> 本文档汇总 CIM 的全部验证结果 -- 不是理论, 是实测数据和可复现的脚本。

## 验证全景

| 阶段 | 方法 | 结果 | 脚本 |
|------|------|------|------|
| step1-5 | IFC 实体覆盖率 | 12/12 Brick 类 100% | validation/step1-5 |
| step6 | SHACL 形式化验证 | VIOLATION=0, WARNING=0 | validation/step6 |
| step7 | 三源联邦 SPARQL | 5/5 通过, 30,016 三元组 | validation/step7 |
| step8-9 | 仿真门控 ISO 19650 | CRITICAL=0, 4 场景 | validation/step8-9 |
| step10 | 平台查询验证 | 10/10 PASS | validation/step10 |
| step11 | 业务场景验证 | 28/28 PASS | validation/step11 |
| step12 | MVP 端到端 | 6/7 RDF + 前端通过 | validation/step12 |

## 1. BIM 实测覆盖率 (step1-5)

**数据源**: NBU_MedicalClinic (宁波大学附属医院)
- 6 个 IFC 文件, 3.85M 实体
- 提取 MEP 设备实体, 映射到 Brick Schema 类

**结果**:

| Brick 类 | IFC 实体数 | CIM 类覆盖 | 状态 |
|-----------|-----------|-----------|------|
| AHU | 12 | cim:AirHandlingUnit | PASS |
| Chiller | 4 | cim:Chiller | PASS |
| CoolingTower | 4 | cim:CoolingTower | PASS |
| Boiler | 2 | cim:Boiler | PASS |
| Pump | 28 | cim:Pump | PASS |
| Fan | 16 | cim:Fan | PASS |
| VAV | 24 | cim:VAVBox | PASS |
| FCU | 48 | cim:FCU | PASS |
| Transformer | 6 | cim:Transformer | PASS |
| UPS | 4 | cim:UPS | PASS |
| EmergencyGenerator | 2 | cim:EmergencyGenerator | PASS |
| SmokeDetector | 62 | cim:SmokeDetector | PASS |

12/12 Brick 类覆盖率 **100%**。

## 2. SHACL 形式化验证 (step6)

**工具**: pyshacl + rdflib, inference=rdfs

**范围**: 4 个核心 ABox 文件
- `nbu_ifc_entities.ttl` (BIM 静态)
- `nbu_bas_readings_t0.ttl` (BAS 正常)
- `nbu_cmms_workorders.ttl` (CMMS 工单)
- `nbu_drill_scenario.ttl` (演练场景)

**约束**:
- 设备必须有 `cim:locatedIn` 空间关联
- 传感器必须有 `cim:hasUnit` 单位
- 工单必须有 `cim-cmms:maintenanceTarget` 目标设备
- 安全事件必须有 `cim:eventSeverity` 等级

**结果**: VIOLATION = 0, WARNING = 0 (全部通过)

## 3. 三源联邦验证 (step7)

**5 条 SPARQL 联邦查询**:

| 查询 | 描述 | 跨源 | 结果行 | 状态 |
|------|------|------|--------|------|
| Q1 | 设备-空间关联 | IFC+TBox | 212 | PASS |
| Q2 | 设备-BAS 点位 | IFC+BAS | 186 | PASS |
| Q3 | 三角闭环 (IFC+BAS+CMMS) | 全部 3 源 | 11 | PASS |
| Q4 | FAS 探测器-空间 | FAS+IFC | 62 | PASS |
| Q5 | CMMS 工单-设备类型 | CMMS+TBox | 48 | PASS |

**Q3 三角闭环** 是核心验证: 11 行记录证明 BAS 报警设备可通过 CIM 同时关联到 IFC 位置和 CMMS 维保历史。

**总三元组**: 30,016 (联邦查询涉及的三元组子集)

## 4. 仿真门控验证 (step8-9)

**方法**: 6 阶段 ISO 19650 门控, 4 场景

| 场景 | 系统 | 守恒检查 | 结果 |
|------|------|---------|------|
| 手术部洁净 | HVAC | 空气质量守恒 (ACH/压差) | PASS, CRITICAL=0 |
| 冷站能效 | HVAC | 冷水能量守恒 (COP) | PASS, CRITICAL=0 |
| 病房环境 | HVAC+电气 | 温湿度+照明 | PASS, CRITICAL=0 |
| 烟感联动 | FAS+BAS | 探测→联动时序 | PASS, CRITICAL=0 |

守恒方程覆盖: 空气 / 冷水 / 医气 / 电气 4 类物理量。

## 5. 平台查询验证 (step10)

10 条验证查询, 覆盖 SPARQL 端点和 Named Graph 功能:

| # | 查询类型 | 目标 | 状态 |
|---|---------|------|------|
| 1-8 | SPARQL SELECT/CONSTRUCT | 各业务模式 | 8/8 PASS |
| 9 | Named Graph 列表 | 9 Graph 完整性 | PASS |
| 10 | Named Graph 隔离 | 跨 Graph 无泄漏 | PASS |

## 6. 业务场景验证 (step11)

28 条业务场景查询, 覆盖 8 个应用模式:

| 模式 | 查询数 | 通过 | 关键发现 |
|------|--------|------|---------|
| 设备全状态 | 4 | 4/4 | -- |
| 楼层看板 | 3 | 3/3 | -- |
| 能耗异常 | 3 | 3/3 | 1 台设备偏差 >20% |
| 维保预警 | 3 | 3/3 | -- |
| FAS 区域 | 4 | 4/4 | 124 行 FAS 记录 |
| 三源闭环 | 4 | 4/4 | -- |
| 安全事件 | 4 | 4/4 | -- |
| 时序趋势 | 3 | 3/3 | -- |

**28/28 全部 PASS**。

## 7. MVP 端到端验证 (step12)

**RDF 验证**: 7 个 TTL 文件语法检查
- 6/7 通过 (1 个 BAS 快照有 minor 格式问题, 不影响语义)

**前端验证**: 可视化平台功能
- 态势面板: 渲染正常
- 事件时间线: 10 动作节点全部显示
- BAS 指令面板: 4 指令状态正确

**独立仿真验证**:
- 10/10 动作节点执行完成
- 总耗时 840s < 900s 时限
- 4 条 BAS 指令全部下发
- 5 状态转换: IDLE → DETECTED → CONFIRMED → RESPONDING → RESOLVED

## 可复现性

所有验证步骤均有对应脚本, 位于 `validation/` 目录:

```bash
# 运行完整验证流水线
python validation/run_all_steps.py

# 单步验证
python validation/step6_shacl.py          # SHACL
python validation/step7_federation.py     # 三源联邦
python validation/step12_mvp_e2e.py       # MVP 端到端
```

每次 TBox/ABox 变更后应重新运行验证, 确保回归安全。
