# 医疗建筑领域上下文

> 本文档回答核心问题: CIM-PIM-PSM 在医疗建筑领域解决什么问题, 如何解决。

## 1. 领域问题定义

### 1.1 医疗建筑的特殊性

医疗建筑远非普通商业建筑。一栋综合医院同时运行 **5 大技术系统**:

| 系统 | 典型设备 | 强制标准 | 特殊要求 |
|------|---------|---------|---------|
| HVAC 暖通 | AHU/冷机/冷塔/锅炉/VAV/FCU | GB50333 | 洁净手术室: 换气>=36ACH, 压差>=8Pa, 温度 21-25 C |
| 电气 Electrical | 变压器/ATS/UPS/发电机/配电柜 | IEC60364-710 | IT 隔离电源: 手术室强制, 双路供电+柴发 |
| 医用气体 MedicalGas | O2汇流排/真空泵/医用空压机/N2O | WS435 | 每间 OR 至少 2 终端 (O2+VAC+CAIR) |
| 消防 FireProtection | 消防泵/喷头/烟感/手报/FAS | GB50016 | 特殊功能区域防火分区划分 |
| 控制 Controls | DDC/传感器/执行器/BACnet网关 | ASHRAE 135 | 实时采集+联动控制 |

普通写字楼只需 HVAC+电气+消防, 医疗建筑多出 **医用气体** 和 **生命安全分级**:

- **LIFE_SAFETY**: 手术室、ICU、产房 -- 系统故障直接威胁生命
- **CRITICAL**: 检验科、药房、血库 -- 环境失控导致医疗差错
- **NORMAL**: 门诊、行政、后勤 -- 等同普通商业建筑

### 1.2 数据孤岛问题

医疗建筑运营依赖 3 个独立数据源, 各说各话:

| 数据源 | 内容 | 格式 | 更新频率 | 问题 |
|--------|------|------|---------|------|
| BIM/IFC | 建筑几何 + MEP 设备布局 | IFC2X3/IFC4 | 建设期一次性 | 语义薄弱, 竣工即过时 |
| BAS/BACnet | 传感器读数 + 控制状态 | ASHRAE 135 | 实时 (秒级) | 点位名称无语义标注 |
| CMMS | 维保工单 + 故障记录 | 各厂商私有 | 日/周 | 与设备台账脱钩 |

**同一台设备在三个系统中的名字**:
- IFC 说: `AHU-001` (几何实体, 有坐标无状态)
- BACnet 说: `AI:1` (模拟输入通道, 有实时值无身份)
- CMMS 说: `WO-PM-0001` (季度保养工单, 有记录无位置)

三源之间没有统一的语义层把它们关联起来。运维人员看到 BAS 报警,
要手动查 IFC 图纸找位置, 再到 CMMS 查维保记录 -- 效率极低, 且容易出错。

### 1.3 现有标准的不足

| 标准 | 类数 | 覆盖范围 | 缺失 |
|------|------|---------|------|
| Brick Schema 1.3 | ~620 | 通用建筑设备 + 传感器 | 无医疗专项 (无医气/洁净度), 无生命周期 |
| ASHRAE 223P | ~380 | HVAC 连接点 + 介质 | 无运营数据, 无消防, 无维保 |
| IFC4 | ~800 | 建筑几何 + 基础 MEP | 语义弱, 无 BAS/CMMS 映射 |
| FSO (Fire Safety Ontology) | ~90 | 消防系统基础 | 无探测器细分, 无联动预案 |

这些标准互不对齐, 无法联合查询。你不能用一条 SPARQL 同时问
"这台 AHU 的 Brick 类型、223P 连接点和 IFC 空间位置"。

## 2. CIM 的解决方案

### 2.1 三层架构 (CIM-PIM-PSM)

```
CIM (Common Information Model)     -- 领域语义层
  "什么是什么" -- 545 owl:Class, 定义医疗建筑的所有概念和关系
  例: AirHandlingUnit rdfs:subClassOf HVACEquipment

PIM (Platform Independent Model)   -- 平台服务层
  "怎么查询" -- SPARQL 端点 + Named Graph + 联邦查询
  例: SELECT ?device ?value WHERE { GRAPH <graph/bas/t0> { ... } }

PSM (Platform Specific Model)      -- 应用实例层
  "解决什么业务" -- 安防 MVP, L2 电气火灾响应
  例: 烟感报警 → 预案匹配 → 风阀关闭 → 广播疏散
```

CIM 是语义中间件: 不替代 IFC/BAS/CMMS, 而是在三者之上建立统一的语义层。

### 2.2 ISO 19650 四层本体

CIM 本体按 ISO 19650 分为 5 层 (Layer 0-4), 从抽象到具体:

| 层 | 名称 | 内容 | 文件 |
|----|------|------|------|
| Layer 0 | BFO 基础层 | 持续体/发生体区分, 时间/空间基本范畴 | `layer0_bfo.ttl` |
| Layer 1 | 概念层 | 介质/连接点/数据点/设备/空间/流动 6 大核心概念 | `layer1_concept.ttl` |
| Layer 2 | 参考层 | 标准分类/PDT (Property Data Template)/参考数据 | `layer2_reference.ttl` |
| Layer 3 | 设计层 | 性能准则/规格/负荷计算/设计参数 | `layer3_design.ttl` |
| Layer 4 | 运营层 | 资产/维护/告警/控制/安全事件/FAS/CMMS | `layer4_operation.ttl` |

Layer 0-2 相对稳定 (标准级), Layer 3-4 随项目变化 (项目级)。

### 2.3 六桥接对齐策略

CIM 通过 6 个桥接本体对齐外部标准:

| 桥接 | 外部标准 | 对齐方法 | 示例 |
|------|---------|---------|------|
| bridge_brick.ttl | Brick 1.3 | owl:equivalentClass | cim:AHU = brick:AHU |
| bridge_223p.ttl | ASHRAE 223P | owl:equivalentClass + 属性映射 | cim:ConnectionPoint ≈ s223:ConnectionPoint |
| bridge_ifc.ttl | IFC4 | owl:equivalentClass + cim:ifcGlobalId | cim:Equipment → ifc:IfcBuildingElement |
| bridge_fso.ttl | FSO | rdfs:subClassOf | cim:SmokeDetector rdfs:subClassOf fso:Detector |
| bridge_bacnet.ttl | BACnet | cim-bacnet:bacnetPointOf | 点位→设备链接 |
| bridge_iso14224.ttl | ISO 14224 | cim-cmms:failureMode | 故障模式分类 |

桥接本体是独立文件, 不修改外部标准的原始定义。

### 2.4 三源联邦

CIM 作为语义中间件, 通过 Named Graph 实现三源联邦查询:

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  IFC 数据    │     │  BAS 数据     │     │  CMMS 数据    │
│  graph/ifc  │     │  graph/bas/* │     │  graph/cmms  │
└──────┬──────┘     └──────┬───────┘     └──────┬───────┘
       │                   │                     │
       │  cim:hasEquipID   │  bacnet:pointOf     │  cmms:target
       │                   │                     │
       └───────────┬───────┴─────────────────────┘
                   │
            ┌──────▼──────┐
            │  CIM 设备    │
            │  graph/tbox  │
            └─────────────┘
```

**三角闭环**: 设备报警 (BAS) + 维修工单 (CMMS) + 物理位置 (IFC) = 完整的设备全景。
一条 SPARQL 联邦查询可跨 3 个 Named Graph 返回完整答案。

## 3. 项目规模

| 指标 | 数值 | 说明 |
|------|------|------|
| owl:Class | 545 | 17 命名空间, 覆盖 5 大系统 |
| TBox 文件 | 15 | Layer 0-4 + 6 桥接 + skeleton + index |
| ABox 文件 | 9 | IFC + BAS(t0/t1/t2) + CMMS + FAS + events + pset |
| Named Graph | 9 | tbox / ifc / bas(3) / cmms / fas / event / pset |
| 总三元组 | 61,941 | rdflib 实测 |
| 联邦数据源 | 3 | IFC + BACnet + CMMS |
| SPARQL 查询 | 14 | 9 业务 + 5 验证 |
| 验证流水线 | 12 步 | step1 (IFC解析) → step12 (MVP端到端) |
| SHACL VIOLATION | 0 | 全量 ABox 验证通过 |
| MVP | L2 电气火灾 | 10 动作节点, 5 状态机, 4 BAS 指令, 62 FAS 探测器 |

## 4. 对齐的标准清单

| 类别 | 标准 | 用途 |
|------|------|------|
| 信息管理 | ISO 19650 (4层) | 本体分层架构 |
| 上层本体 | BFO 2020 | Layer 0 基础范畴 |
| 建筑信息 | IFC 4 | BIM 几何 + MEP |
| 建筑语义 | Brick Schema 1.3 | 设备 + 传感器分类 |
| HVAC 语义 | ASHRAE 223P | 连接点 + 介质 + 流动 |
| 消防本体 | FSO | 消防系统基础 |
| 楼宇自控 | BACnet (ASHRAE 135) | BAS 数据点协议 |
| 可靠性 | ISO 14224 | 故障模式 + 维护分类 |
| 洁净室 | GB50333 | 手术部洁净度 |
| 医用气体 | WS435 | 气体终端 + 管路 |
