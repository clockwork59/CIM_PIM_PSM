# CIM 数据组织架构

> 本文档回答: CIM 如何组织数据 -- TBox/ABox 分离、Named Graph 隔离、ID 治理。

## 1. TBox/ABox 分离原则

本体工程的基本分离:

- **TBox (术语层)**: 类定义、属性定义、约束规则 -- "词典"
- **ABox (断言层)**: 实体实例、属性值、关系断言 -- "事实"

为什么分离: TBox 是项目级稳定资产 (标准不常变), ABox 是运营级动态资产 (BAS 秒级更新)。
分离后可以独立版本控制、独立缓存、独立验证。

### 1.1 CIM TBox 结构 (15 文件, 5,395 三元组)

| 文件 | 层 | 类数 | 三元组 | 用途 |
|------|-----|------|--------|------|
| `layer0_bfo.ttl` | L0 | 12 | ~180 | BFO 基础范畴 (持续体/发生体) |
| `layer1_concept.ttl` | L1 | 45 | ~520 | 核心概念 (介质/连接点/设备/空间/流动/数据点) |
| `layer2_reference.ttl` | L2 | 180 | ~1,800 | 参考分类 (5大系统设备类型) |
| `layer3_design.ttl` | L3 | 65 | ~780 | 设计参数 (性能准则/规格/负荷) |
| `layer4_operation.ttl` | L4 | 95 | ~1,100 | 运营概念 (告警/工单/事件/维保) |
| `bridge_brick.ttl` | 桥接 | 28 | ~160 | Brick 1.3 对齐 |
| `bridge_223p.ttl` | 桥接 | 22 | ~140 | ASHRAE 223P 对齐 |
| `bridge_ifc.ttl` | 桥接 | 35 | ~200 | IFC4 对齐 |
| `bridge_fso.ttl` | 桥接 | 15 | ~90 | FSO 消防对齐 |
| `bridge_bacnet.ttl` | 桥接 | 18 | ~110 | BACnet 点位对齐 |
| `bridge_iso14224.ttl` | 桥接 | 12 | ~75 | ISO 14224 故障模式对齐 |
| `ontology_skeleton.ttl` | 索引 | -- | ~120 | 命名空间声明 + owl:imports |
| `_index_v4.ttl` | 索引 | -- | ~80 | 模块化导入链 |
| `equipment/mechanical.ttl` | L2 | ~60 | -- | HVAC 设备层次 |
| `equipment/electrical.ttl` | L2 | ~58 | -- | 电气设备层次 |

### 1.2 CIM ABox 结构 (9 文件, ~56,546 三元组)

| 文件 | 数据源 | 实例数 | 三元组 | 更新频率 |
|------|--------|--------|--------|---------|
| `nbu_ifc_entities.ttl` | IFC/BIM | ~800 | ~12,000 | 建设期 (静态) |
| `nbu_bas_readings_t0.ttl` | BACnet | ~1,055 | ~8,400 | 3快照轮换 |
| `nbu_bas_readings_t1.ttl` | BACnet | ~1,055 | ~8,400 | 3快照轮换 |
| `nbu_bas_readings_t2.ttl` | BACnet | ~1,055 | ~8,400 | 3快照轮换 |
| `nbu_cmms_workorders.ttl` | CMMS | ~120 | ~2,400 | 日/周 |
| `nbu_fas_topology.ttl` | FAS | ~62 | ~1,200 | 设计期 (静态) |
| `nbu_security_events.ttl` | 事件引擎 | ~30 | ~600 | 实时 |
| `nbu_pset_design.ttl` | 设计参数 | ~200 | ~3,000 | 设计期 (静态) |
| `nbu_drill_scenario.ttl` | 仿真 | ~50 | ~746 | 演练时 |

## 2. Named Graph 隔离

9 个 Named Graph 提供语义分区, 每个 Graph 有独立的更新策略:

| Named Graph URI | 内容 | 更新策略 | 访问模式 |
|-----------------|------|---------|---------|
| `<graph/tbox>` | 本体定义 (TBox) | 版本级 (标准更新才变) | 只读, 所有查询共享 |
| `<graph/ifc>` | BIM 静态实例 | 建设期一次写入 | 只读 |
| `<graph/bas/t0>` | BAS 正常快照 | 3快照轮换 (秒级) | 读写 |
| `<graph/bas/t1>` | BAS 异常快照 | 同上 | 读写 |
| `<graph/bas/t2>` | BAS 告警快照 | 同上 | 读写 |
| `<graph/cmms>` | CMMS 维保工单 | 日/月增量 | 读写 |
| `<graph/fas>` | FAS 消防拓扑 | 设计期写入 | 只读 |
| `<graph/event>` | 安全事件 | 实时, 无缓存 | 读写, 事件驱动 |
| `<graph/pset>` | 设计参数 (Pset) | 设计期写入 | 只读 |

**为什么用 Named Graph 而不是文件隔离?**

- BAS 时序 Graph 可独立更新/过期, 不影响 IFC 静态 Graph
- SPARQL `FROM NAMED` 支持跨 Graph 联邦查询
- 权限可按 Graph 粒度控制 (BAS 读写 vs IFC 只读)
- 验证时 Agent-09 跨越所有边界, 生成时每个 Agent 只写自己的 Graph

## 3. ID 治理规范

### 3.1 CIM 设备 ID 格式

```
{TYPE}-{MODEL}-{N}
```

示例:
- `CHL-19XR-001` -- 19XR 型冷机第 1 台
- `AHU-39-001` -- 39 型空调箱第 1 台
- `SD-FST-851-001` -- FST-851 型烟感探测器第 1 号

### 3.2 跨源 ID 追溯

| 属性 | 用途 | 示例 |
|------|------|------|
| `cim:ifcGlobalId` | 保留 IFC 原始 GlobalId | `"2O2Fr$t4X7Zf8NOew3FNld"` |
| `cim:bacnetObjectId` | BACnet 对象 ID | `"AI:1"` |
| `cim:cmmsAssetTag` | CMMS 资产标签 | `"ASSET-AHU-001"` |
| `rdfs:label` | 人类可读名称 | `"1号空调箱"` |

### 3.3 全局 ID 注册表

`global_id_registry.yaml` 维护所有实体的跨源映射:

```yaml
AHU-39-001:
  cim_uri: "cim-inst:AHU-39-001"
  ifc_global_id: "2O2Fr$t4X7Zf8NOew3FNld"
  bacnet_device: "Device:101"
  bacnet_points: ["AI:1", "AI:2", "AO:1"]
  cmms_asset: "ASSET-AHU-001"
  location: "Building-A/Floor-3/Zone-OR/Room-OR01"
```

## 4. 语义链接拓扑

三源通过 CIM 设备节点链接, 形成三角闭环:

```
IFC 实例                          BACnet 点位
(几何+位置)                       (实时读数)
     │                                │
     │ cim:ifcGlobalId                │ cim-bacnet:bacnetPointOf
     │                                │
     └──────────► CIM 设备 ◄──────────┘
                     │
                     │ cim-cmms:maintenanceTarget
                     │
                     ▼
                CMMS 工单
              (维保记录)
```

**闭环价值**:
- BAS 报警 → 通过 CIM 找到 IFC 位置 → 运维人员知道去哪里
- BAS 报警 → 通过 CIM 找到 CMMS 历史 → 判断是否反复故障
- CMMS 工单到期 → 通过 CIM 找到 BAS 当前状态 → 判断是否需要紧急处理

这就是 M3 三源联邦的核心价值: 一条 SPARQL 跨 3 个 Named Graph, 返回设备的完整生命周期视图。
