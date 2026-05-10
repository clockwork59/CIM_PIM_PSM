# M3 Sprint Plan: 多数据源联邦仿真系统
**Sprint 2026-05-10 → 05-13**  
**目标**: CIM v4.0 TBox 补全 + BAS/BACnet & CMMS 仿真数据源 + 多源联邦 SPARQL 验证

---

## 背景与范围

M2 已完成单数据源 IFC→CIM 映射贯通（1,210 实例，SHACL VIOLATION=0）。  
M3 目标：**三数据源联邦仿真**，验证 CIM v4.0 作为集成语义层的能力。

| 数据源 | M2 状态 | M3 目标 |
|--------|---------|---------|
| IFC 静态 BIM | ✅ 1,210 实例完成 | 继续作为基础 |
| BAS/BACnet 实时传感 | ❌ TBox 稀疏，无仿真 | 补全本体 + 仿真生成 |
| CMMS 维护工单 | ❌ TBox 缺失，无仿真 | 补全本体 + 仿真生成 |

### M3 范围边界（已确认）
- **在范围内**: TBox 补全 + 仿真数据生成 + 联邦 SPARQL 验证
- **不在范围内**: 完整安防 MVP 应用、事件层设计、PIM 平台（Fuseki/GraphDB 部署）

---

## TBox 差距分析

### 现有 FAS/BACnet 覆盖（Grep 实测）
仅 2 个文件命中 `SmokeDetector|FireAlarm|FAS|BACnet|bacnet`：
- `layer1_conceptual.ttl` — 包含抽象设备类（仅类定义，无操作语义）
- `bridge/bridge_ifc.ttl` — IFC FAS 实体映射（桥接，非原生类）

`layer4_operational.ttl`、设备模块、spaces 模块均无 FAS 具体类和 BACnet 绑定属性。

### 现有 CMMS 覆盖
`layer4_operational.ttl` 包含 `MaintenanceRecord`/`Sensor`/`Alarm`，但：
- 无 `WorkOrder` 类层次（PM/CM/紧急工单区分）
- 无工单状态机语义（Open→InProgress→Completed）
- 无技术人员/团队分配属性

### 需新增的三个 TBox 模块

| 模块文件 | 位置 | 类数 | 属性数 | 用途 |
|---------|------|------|--------|------|
| `layer4_fas_security.ttl` | `cim/ontology/` | 12 | 8 | FAS 设备操作类 |
| `bridge/bridge_bacnet.ttl` | `cim/ontology/bridge/` | 9 | 10 | BACnet 协议绑定 |
| `layer4_cmms.ttl` | `cim/ontology/` | 8 | 11 | CMMS 工单模型 |

---

## 交付物清单

### TBox 扩展（3 个新 TTL 文件）

```
project_deliverables/version02/cim/ontology/
├── layer4_fas_security.ttl     ← NEW (12 owl:Class, BFO 对齐)
├── layer4_cmms.ttl             ← NEW (8 owl:Class, 工单状态机)
└── bridge/
    └── bridge_bacnet.ttl       ← NEW (9 owl:Class, BACnet 840-2020)
```

需同步更新：
- `_index_v4.ttl` — 新增 3 条 `owl:imports`

### ABox 仿真生成（2 个脚本 + 2 个输出 TTL）

```
simulation/
├── bas_bacnet_simulator.py     ← NEW: 读 IFC ABox → 生成 BACnet 传感点 RDF
├── cmms_simulator.py           ← NEW: 读 IFC ABox → 生成工单 RDF
abox/
├── nbu_bas_readings.ttl        ← 生成: ~3,600 BACnetPoint + 传感读数实例
└── nbu_cmms_workorders.ttl     ← 生成: ~480 WorkOrder 实例
```

### 联邦验证（1 个脚本）

```
validation/
└── step9_federation_validation.py  ← NEW: 5 条跨源 SPARQL 查询验证
```

---

## Sprint 任务分解

### Day 1 (05-10): TBox 扩展
- [x] Gap 分析确认（本文档）
- [ ] 写 `layer4_fas_security.ttl`
- [ ] 写 `bridge/bridge_bacnet.ttl`
- [ ] 写 `layer4_cmms.ttl`
- [ ] 更新 `_index_v4.ttl` imports

### Day 2 (05-11): 仿真脚本
- [ ] 写 `bas_bacnet_simulator.py`（BACnet 点生成）
- [ ] 写 `cmms_simulator.py`（工单生成）
- [ ] 运行脚本，生成 `nbu_bas_readings.ttl` & `nbu_cmms_workorders.ttl`

### Day 3 (05-12): 联邦验证
- [ ] 写 `step9_federation_validation.py`
- [ ] 运行 5 条 SPARQL 联邦查询
- [ ] 修复发现的命名空间/实例对齐问题

### Day 4 (05-13): 审核关闭
- [ ] SHACL 对新 ABox 运行全量验证（VIOLATION=0 目标）
- [ ] owl:Class 统计更新（预期: 482+29 = 511 口径B）
- [ ] Sprint 报告定稿

---

## M3 质量门控

| 检查项 | 通过条件 |
|--------|---------|
| TBox SHACL | 3 个新模块 VIOLATION=0 |
| BAS 联邦查询 Q1-Q3 | 返回结果非空，变量绑定正确 |
| CMMS 联邦查询 Q4-Q5 | 返回结果非空，设备 URI 与 IFC ABox 一致 |
| 跨源连接 | IFC 设备实例 ↔ BACnet 点 ↔ CMMS 工单三角闭环 |
| owl:Class 计数 | 口径B ≥ 509（482 + 27 新增） |

---

## 仿真数据设计

### BAS/BACnet 仿真策略
- **覆盖设备**: AHU（23台）、VAV（156台）、Chiller（3台）、Pump（18台）、FAS detector（60点）
- **每设备点数**: AHU=8点, VAV=4点, Chiller=12点, Pump=3点, Detector=2点
- **输出实例估算**: ~3,600 BACnetPoint instances
- **时间戳**: 仿真单时刻快照（`xsd:dateTime "2026-05-10T08:00:00+08:00"`）
- **数值范围**: 沿用 conservation_engine.py 中的参数（COP 3.5~8.0，风量按 design 值 ±15%）

### CMMS 工单仿真策略
- **PM 工单**: 按设备类型周期生成（AHU 季检 × 23 = 23 条；Chiller 年检 × 3 = 3 条；VAV 半年检 × 156 = 78 条等）
- **CM 工单**: 按 FMEA 故障模式随机注入（200+ 故障类型；10% 设备有 CM 工单）
- **输出实例估算**: ~480 WorkOrder instances
- **状态分布**: Open 40% / InProgress 30% / Completed 25% / Cancelled 5%
