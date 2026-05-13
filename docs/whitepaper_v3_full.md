# 医疗建筑数字孪生统一领域模型（CIM）技术白皮书

**副标题**: 四模式驱动的知识工程方法论 — MBSE 架构 / BFO 动态本体 / ISO 19650 全域覆盖 / 社会技术系统

**版本**: v3.0
**日期**: 2026 年 5 月
**作者**: CIM-PIM-PSM 项目组
**目标读者**: 医院信息化决策者 / BIM 咨询顾问 / 智慧建筑技术负责人 / 学术研究者

---

## 摘要

医疗建筑是当代最复杂的建筑类型。一栋综合医院同时运行暖通空调（HVAC）、电气配电、医用气体、消防与楼宇自控（BAS）五大机电系统，受 GB 50333、WS 435、IEC 60364-710 等多部强制标准约束，而支撑运营的三大数据源——BIM/IFC、BAS/BACnet 与 CMMS——长期割裂，形成结构性信息孤岛。现有行业本体标准 Brick Schema 1.3（约 620 类）、ASHRAE 223P（约 380 类）、IFC4（约 800 类型）各覆盖领域的一个切面，彼此缺乏原生互操作能力，且无一覆盖医疗建筑的全部语义需求。

本白皮书提出一种面向医疗建筑数字孪生的统一领域模型（Common Information Model, CIM），以**四个相互联锁的模式**（Pattern）作为智识骨架，从理论到实现构成完整闭环。**模式一：MBSE 三层架构**（CIM-PIM-PSM）将系统组织为领域知识层、系统工程层与项目实例层三个抽象级别——三层之间是约束-实例化关系，而非并列-拼装关系。**模式二：BFO 动态本体**引入 BFO 2020 的持续体/发生体（Continuant/Occurrent）范畴区分，使本体不仅能描述"什么存在"，还能描述"什么发生"，解决了静态 BIM 本体无法表达运营过程的根本缺陷。**模式三：ISO 19650 全域业务覆盖**将本体组织为五层结构（Layer 0 BFO 基础至 Layer 4 运营生态），通过 6 个桥接本体实现与 Brick、223P、IFC、FSO、BACnet、ISO 14224 的语义对齐，545 个 OWL 类覆盖 17 个命名空间。**模式四：社会技术系统**将技术要素（传感器、BAS 联动）与社会要素（7 个角色、职责分工、决策权限）纳入同一本体框架，使安防系统从"监设备"升级为"处置态势"。

项目基于宁波大学附属医院真实 IFC 模型构建了包含 61,941 个 RDF 三元组的知识图谱，组织于 9 个 Named Graph 中。全部 5 条联邦验证查询通过（5/5 SPARQL PASS），SHACL 形式化验证零违规（VIOLATION = 0），28 条业务场景查询全部通过（28/28 PASS）。作为四模式融合的端到端验证，L2 级电气火灾安全 MVP 涵盖 62 个 FAS 探测器、5 状态事件机、10 个动作节点（4 自动 + 4 人工 + 2 确认）和 4 条 BAS 联动指令，仿真耗时 840 秒，在 900 秒时限内完成。

---

## 第一章 问题与愿景

### 1.1 医疗建筑：最复杂的建筑类型

医疗建筑远非普通商业建筑的简单放大。普通写字楼只需暖通空调、基础电气和消防三大系统，而医疗建筑必须同时运行五大独立却紧密耦合的机电系统，每一个系统都直接关系到患者安全和医疗质量。

| 系统 | 典型设备 | 强制标准 | 特殊要求 |
|------|---------|---------|---------|
| HVAC 暖通 | AHU/冷机/冷塔/锅炉/VAV/FCU | GB 50333 | 洁净手术室: 换气>=36ACH, 压差>=8Pa, 温度21-25C |
| 电气 Electrical | 变压器/ATS/UPS/发电机/配电柜 | IEC 60364-710 | IT隔离电源: 手术室强制, 双路供电+柴发 |
| 医用气体 MedicalGas | O2汇流排/真空泵/医用空压机/N2O | WS 435 | 每间OR至少2终端 (O2+VAC+CAIR) |
| 消防 FireProtection | 消防泵/喷头/烟感/手报/FAS | GB 50016 | 特殊功能区域防火分区划分 |
| 控制 Controls | DDC/传感器/执行器/BACnet网关 | ASHRAE 135 | 实时采集+联动控制 |

医用气体系统是医疗建筑区别于所有其他建筑类型的标志性系统。气体供应的中断直接威胁手术台上患者的生命。五大系统的耦合关系使医疗建筑成为一个高度复杂的系统：HVAC依赖电气供电；消防联动需同时控制HVAC风阀和电气开关；医用气体的压缩机需电力驱动和冷却水支持；BAS横跨所有系统进行监控和协调。

医疗建筑承载着三个等级的生命安全分类：**LIFE_SAFETY**（手术室、ICU、产房——系统故障直接威胁生命）、**CRITICAL**（检验科、药房、血库——环境失控导致医疗差错）、**NORMAL**（门诊、行政、后勤——等同普通商业建筑）。

### 1.2 三源数据孤岛

医疗建筑运营依赖三个独立数据源，各说各话：

| 特征维度 | BIM/IFC | BAS/BACnet | CMMS |
|---------|---------|------------|------|
| 数据内容 | 建筑几何+MEP设备布局 | 传感器读数+控制状态 | 维保工单+故障记录 |
| 数据格式 | IFC2X3/IFC4 (EXPRESS) | ASHRAE 135 (BACnet对象) | 各厂商私有格式 |
| 更新频率 | 建设期一次性交付 | 实时（秒级采集） | 日/周/月增量 |
| 标识体系 | IfcGlobalId (GUID) | BACnet Device/Object ID | 资产标签 (Asset Tag) |
| 核心缺陷 | 竣工即过时 | 点位名称无上下文 | 与设备台账脱钩 |

同一台设备在三个系统中的身份完全割裂。以宁波大学附属医院的一台空调箱AHU-001为例：IFC称其为`AHU-001`（有坐标无状态），BACnet称其为`Device:101/AI:1`（有实时值无身份），CMMS称其为`WO-PM-0001`（有记录无位置）。三源之间缺失的是一个**统一的语义中间层**。

### 1.3 现有标准的碎片化

**表 1-1 现有标准对比分析**

| 评估维度 | Brick 1.3 | ASHRAE 223P | IFC4 | FSO | CIM (本项目) |
|---------|-----------|-------------|------|-----|-------------|
| 类定义数量 | ~620 | ~380 | ~800 | ~90 | 545 |
| HVAC设备 | 中 | 强 | 弱 | 无 | 强 |
| 电气设备 | 弱 | 无 | 弱 | 无 | 强 |
| 医用气体 | 无 | 无 | 无 | 无 | 强 |
| 消防系统 | 弱 | 无 | 弱 | 中 | 强 |
| 传感器/点位 | 强 | 弱 | 无 | 无 | 强 (Brick对齐) |
| 连接点/介质 | 无 | 强 | 无 | 无 | 强 (223P对齐) |
| 空间层级 | 中 | 无 | 强 | 无 | 强 (IFC对齐) |
| 生命周期 | 无 | 无 | 部分 | 无 | 强 (8阶段) |
| 运维/维保 | 无 | 无 | 无 | 无 | 强 (CMMS) |
| 医疗专项 | 无 | 无 | 无 | 无 | 强 |
| 跨标准对齐 | 无 | 无 | 无 | 无 | 6桥接本体 |

这四个标准的共同问题是**互不对齐**。不存在一条现成的SPARQL查询能够同时检索"这台AHU的Brick类型、223P连接点结构和IFC空间位置"。

### 1.4 本白皮书的主张

本白皮书提出四模式联锁的解决框架。四个模式不是并列的理论综述，而是相互联锁的设计决策：

| 模式 | 解决的问题 | 核心机制 | 实现对应 |
|------|-----------|---------|---------|
| **模式一：MBSE三层架构** | HOW--架构如何组织 | CIM-PIM-PSM约束-实例化 | 三层资产分离 |
| **模式二：BFO动态本体** | WHY--为什么需要过程性 | Continuant/Occurrent范畴 | Flow双重性、生命周期链 |
| **模式三：ISO 19650全域覆盖** | WHAT--本体覆盖什么领域 | 五层本体+六桥接 | 545类、17命名空间 |
| **模式四：社会技术系统** | WHO & HOW--人如何与系统交互 | 技术-社会-环境三要素 | 安防MVP、7角色 |

模式一提供架构骨架，模式二提供本体论基础，模式三填充领域内容，模式四将技术系统与人类组织桥接。四者联锁才构成完整的解决方案。

---

## 第二章 模式一：MBSE三层架构 (CIM-PIM-PSM)

### 2.1 从OMG MDA到医疗建筑MBSE

CIM-PIM-PSM源自OMG的MDA（Model Driven Architecture）规范，是MBSE（Model-Based Systems Engineering）的核心实现逻辑。

**关键认知**：CIM、PIM、PSM不是三个独立的产出物或三套文件，而是对同一系统在三个抽象层级上的描述。它们之间是**约束-实例化**关系，不是**并列-拼装**关系。

- **CIM（计算无关模型）= 领域知识和惯例认知，以本体和图谱表达。** 医疗建筑有哪些系统？手术室需要什么条件？火灾时谁做什么？不涉及任何技术实现——纯粹的领域语义。
- **PIM（平台无关模型）= 面向领域的系统方法/逻辑/组件，CIM的工程化。** 如何验证本体完整性？如何组织多源数据？如何执行预案逻辑？与用什么数据库、什么编程语言无关。
- **PSM（平台特定模型）= 具体落地项目的技术选型/实现/数据装载，PIM的实例化。** 用Fuseki还是GraphDB？用Python还是Java？NBU医院的具体数据是什么？

| 层级 | 正确理解 | 常见误解 |
|------|---------|---------|
| CIM | 领域知识与惯例认知，以本体和图谱表达 | ~~"就是那些.ttl文件"~~ |
| PIM | 面向领域的系统方法/逻辑/组件，CIM的工程化 | ~~"就是平台中间件"~~ |
| PSM | 具体落地项目的技术选型/实现/数据装载，PIM的实例化 | ~~"就是部署脚本"~~ |

### 2.2 分层依赖与约束传播

```
CIM 约束 PIM --> PIM 约束 PSM --> PSM 可替换

CIM (最稳定，年级变化)
 |  constrains
 v
PIM (中等稳定，月级迭代)
 |  constrains
 v
PSM (最易变，日/时级更新)
```

- **CIM约束PIM**：本体中定义了"手术室必须正压"，PIM中的控制逻辑就必须包含压差维持回路。本体中定义了"安全事件有5个状态"，PIM中的状态机就必须实现全部5个状态转换。
- **PIM约束PSM**：PIM定义了"12步验证管线"，PSM必须实现每一步。PIM定义了"9个Named Graph的语义分区"，PSM的三元组存储必须支持Named Graph管理。
- **PSM可替换**：同一套CIM+PIM可以映射到不同的PSM——不同的医院（NBU vs ZJU）、不同的技术栈（Fuseki vs GraphDB，FastAPI vs Spring Boot）。

这种分层使得"敏捷"和"分阶段"互补——CIM层稳定后，PIM和PSM可以独立快速迭代。在本项目的M1到MVP里程碑路径中，CIM层的每一次扩展（如新增安全事件26类）自然传导到PIM层和PSM层，无需全局重构。

### 2.3 本项目的三层资产映射

**表 2-1 三层资产完整映射**

| 层级 | 资产类别 | 具体内容 | 稳定性 |
|------|---------|---------|--------|
| **CIM** | 本体定义 | 545 owl:Class, 17命名空间, 5层结构(Layer 0-4) | 年级 |
| CIM | 桥接本体 | 6桥接(Brick/223P/IFC/FSO/BACnet/ISO14224), 775三元组 | 年级 |
| CIM | FMEA故障模式 | 设备故障模式库, ISO 14224对齐 | 年级 |
| CIM | 标准准则 | GB50333/WS435/IEC60364硬编码值 | 年级 |
| CIM | 安全事件模型 | 26类, 5状态机, EmergencyPlan/ActionChain | 年级 |
| CIM | BFO生命周期 | 8阶段过程链, ProcessBoundary里程碑 | 年级 |
| **PIM** | 仿真引擎 | 守恒方程4场景, ISO 19650 6阶段门控 | 月级 |
| PIM | 状态机逻辑 | 5态转换(PENDING->CONFIRMED->IN_PROGRESS->CLOSED->ARCHIVED) | 月级 |
| PIM | 动作链执行器 | DAG拓扑排序, 依赖解析, 并行调度 | 月级 |
| PIM | Named Graph架构 | 9图语义分区, 更新策略, 访问权限 | 月级 |
| PIM | SPARQL模板 | 9业务+5验证, 参数化查询 | 月级 |
| PIM | 12步验证管线 | step1(IFC解析)->step12(MVP端到端) | 月级 |
| **PSM** | 三元组存储 | Apache Jena Fuseki 4.10 (TDB2, OWL-micro) | 日级 |
| PSM | REST API | FastAPI 6端点, JSON-LD输出 | 日级 |
| PSM | NBU实例数据 | 1,210设备实例, 212台IFC设备 | 日级 |
| PSM | BAS仿真数据 | 1,055 BACnet点位, 3快照(t0/t1/t2) | 日级 |
| PSM | CMMS工单数据 | 735工单(669PM+64CM+2Inspection) | 日级 |
| PSM | 可视化平台 | HTML 677行, 5面板, JavaScript仿真 | 日级 |

```
+-------------------------------------------------------------+
|  CIM (领域知识层) -- 不依赖任何技术平台                         |
|  "医疗建筑的世界是什么样的"                                    |
|  545 owl:Class | 本体 | 标准 | 惯例 | FMEA | 预案知识          |
|  <- 最稳定，年级变化                                           |
+-------------------------------------------------------------+
|  PIM (系统工程层) -- CIM的工程化，与技术无关                    |
|  "系统需要什么功能、怎么验证"                                  |
|  仿真引擎 | 状态机 | Named Graph | SPARQL | 验证管线           |
|  <- 中等稳定，月级迭代                                         |
+-------------------------------------------------------------+
|  PSM (项目实例层) -- PIM的实例化，面向现实约束                  |
|  "用什么技术、装什么数据"                                      |
|  Fuseki | FastAPI | NBU 1,210实例 | BAS | CMMS | HTML         |
|  <- 最易变，日/时级更新                                        |
+-------------------------------------------------------------+

分层依赖: CIM约束PIM -> PIM约束PSM -> PSM可替换
复用价值: 同一CIM+PIM映射到不同医院的PSM
```

PSM可替换性已通过rdflib-fallback机制验证——全部SPARQL查询在Fuseki和rdflib两个引擎上均执行通过。

---

## 第三章 模式二：BFO动态本体

### 3.1 为什么医疗建筑需要"过程性"

传统建筑本体——Brick Schema和IFC——本质上是静态本体，善于描述"什么存在"。但医疗建筑的核心运营场景是动态的"发生"：

- **手术周期**：排程->术前准备(升温/升湿/正压建立)->术中维持(36ACH,8Pa)->术后消毒->空间释放
- **冷机启动**：预热->载入冷负荷->稳态运行->卸载->停机
- **火灾响应**：烟感报警->确认火情->切断电源->启动灭火->疏散->闭环->恢复

这些场景都是**过程**——在时间中展开、有明确的开始和结束。如果本体只能描述"存在"而不能描述"发生"，就无法建模医疗建筑运营的核心语义。

### 3.2 BFO范畴映射

BFO（ISO/IEC 21838-2:2021）将一切实体划分为**持续体（Continuant）**与**发生体（Occurrent）**两个互不重叠的范畴。

**表 3-1 BFO范畴映射表**

| BFO范畴 | BFO类 | CIM类（示例） | 医疗建筑语义 |
|---------|--------|--------------|-------------|
| 对象 | bfo:Object | cim:AirHandlingUnit, cim:Chiller | AHU-001从安装到退役始终是"同一台设备" |
| 场所 | bfo:Site | cim:OperatingRoom, cim:ICU | OR-01是非物质实体(空间) |
| 质量 | bfo:Quality | cim:FlowRateQuality | 某一瞬间的流速值 |
| 功能 | bfo:Function | cim:CoolingFunction | 冷机的冷却功能(是其存在的目的) |
| 广义依赖持续体 | bfo:GDC | cim:DesignDocument, cim:MaintenancePlan | 信息实体 |
| 过程 | bfo:Process | cim:FluidFlowProcess, cim:MaintenanceActivity | 冷冻水流动、维保作业 |
| 过程边界 | bfo:ProcessBoundary | cim:HandoverMilestone | PIM->AIM信息移交瞬间 |
| 时间区域 | bfo:TemporalRegion | cim:OperationalPeriod | 运营时段 |

BIM/IFC本质上是持续体模型——记录建筑"是什么样的"；BAS本质上是发生体监测系统——采集物理过程的实时状态。将两者纳入同一本体框架时，如果不做持续体/发生体的范畴区分，就会产生本体论层面的混淆。

### 3.3 Flow的双重性：FlowPath vs FlowProcess

CIM的关键创新是将"流动"分解为两个本体论上截然不同的概念：

```
FlowPath (持续体/Continuant)           FluidFlowProcess (发生体/Occurrent)
  |                                       |
  | 描述: 管路拓扑连接关系                  | 描述: 介质在管路中的实际流动
  | 属性: 设计流量 180 m3/h               | 属性: 当前流量 165 m3/h
  | 生命期: 建筑使用期内恒定               | 生命期: 有开始时间和结束时间
  | 数据来源: IFC/设计文档                 | 数据来源: BAS/传感器
  | 用途: 设计验证(检查拓扑)               | 用途: 运营监控(检查流态)
```

这一区分使跨Named Graph（graph/pset设计参数 vs graph/bas/t0实时读数）的比较分析成为可能。能耗异常检测模式通过比较Layer 3设计参数与Layer 4 BAS实时读数，自动识别偏离设计值超过20%的设备。

### 3.4 设施生命周期过程链

CIM通过BFO的Process范畴，将建筑的完整生命周期建模为8阶段过程序列：

```
ConceptualDesign --> SchematicDesign --> DetailedDesign --> Tendering
     |                   |                  |               |
     v                   v                  v               v
  [概念设计           [方案设计          [施工图设计       [招标采购
   里程碑]            里程碑]            里程碑]          里程碑]

--> Construction --> Commissioning --> Operation --> Decommissioning
         |               |               |               |
         v               v               v               v
      [施工完成       [调试验收        [投入运营        [退役拆除
       里程碑]        里程碑]          里程碑]          里程碑]
```

里程碑是信息状态的切换点：竣工验收意味着IFC模型冻结、BAS开始产生数据；投入运营意味着CMMS开始记录工单。三源数据的产生时间和语义范围在过程链中得到精确的本体定位——模式二（BFO）与模式三（ISO 19650）在此处汇合。

---

## 第四章 模式三：ISO 19650全领域业务覆盖

### 4.1 四层到五层：ISO 19650的本体化实现

CIM本体的五层结构借鉴并扩展了ISO 19650的信息层级理念，增加了Layer 0（BFO基础层）：

**表 4-1 CIM五层本体与ISO 19650映射**

| CIM层 | 名称 | ISO 19650对应 | 内容 | 类数 | 三元组 | 变更频率 |
|--------|------|---------------|------|------|--------|---------|
| Layer 0 | BFO基础层 | 跨层级通用 | 持续体/发生体范畴 | 12 | ~180 | 极低 |
| Layer 1 | 概念层 | 信息需求(OIR/EIR) | 介质/连接点/数据点/设备/空间/流动 | 45 | ~520 | 低 |
| Layer 2 | 参考层 | 标准分类库 | 12部标准引用、PDT属性定义 | 180 | ~1,800 | 低 |
| Layer 3 | 设计层 | PIM(项目信息模型) | 性能准则(GB50333硬编码值) | 65 | ~780 | 项目级 |
| Layer 4 | 运营层 | AIM(资产信息模型) | 资产/传感器/控制/安全/FAS/CMMS | 95 | ~1,100 | 运营级 |

```
                +---------------------------------+
                |     Layer 4: 运营与扩展          | 95 类
                |  资产/控制/安全/FAS/CMMS         | ~1,100 三元组
                +---------------------------------+
                |     Layer 3: 设计本体            | 65 类
                |  性能准则/规格/负荷              | ~780 三元组
                +---------------------------------+
                |     Layer 2: 参考本体            | 180 类
                |  标准分类/PDT/参考数据           | ~1,800 三元组
                +---------------------------------+
                |     Layer 1: 概念本体            | 45 类
                |  介质/连接点/数据点/             | ~520 三元组
                |  设备/空间/流动                  |
                +---------------------------------+
                |     Layer 0: BFO 基础层          | 12 类
                |  Continuant / Occurrent         | ~180 三元组
                +---------+-----------------------+
                          |
      +--------+------+---+---+-------+--------+---------+
      |        |      |       |       |        |         |
  +---v----++--v---++--v--++--v---++---v---++---v----+    |
  | Brick  || 223P || IFC || FSO ||BACnet ||ISO14224|    |
  | 28 cls ||22 cls||35cls||15cls||18 cls ||12 cls  |    |
  +--------++------++-----++-----++-------++--------+    |
       6 桥接本体 (独立文件, 不修改外部标准)               |
```

### 4.2 Layer 0-1: 基础与概念

**介质层级（Medium Hierarchy）** 是Layer 1的关键创新，连接HVAC到MedGas到Electrical的统一桥梁：

```
cim:Medium
    +-- cim:FluidMedium
    |   +-- cim:Water (ChilledWater/HotWater/CondenserWater/DomesticWater)
    |   +-- cim:Air (SupplyAir/ReturnAir/OutdoorAir/ExhaustAir)
    +-- cim:GasMedium
    |   +-- cim:Oxygen / cim:MedicalVacuum / cim:MedicalCompressedAir / cim:NitrousOxide
    +-- cim:EnergyMedium
        +-- cim:ElectricalPower (NormalPower/EmergencyPower/ITIsolatedPower)
        +-- cim:ThermalEnergy
```

GasMedium和ITIsolatedPower是CIM相对于Brick和223P的原创扩展。Layer 1还定义了连接点模型（与223P对齐）、数据点层级（与Brick对齐，含DifferentialPressureSensor和ParticleCountSensor等医疗专项传感器）以及流动模型（31个类，覆盖MassFlow/EnergyFlow/InformationFlow）。

### 4.3 Layer 2-3: 参考与设计

**Layer 2**（180类）提供五大系统的94个设备类、47个空间类和12部标准引用（ISO 19650/BFO 2020/IFC4/Brick 1.3/ASHRAE 223P/FSO/BACnet/ISO 14224/GB50333/WS435/IEC60364-710/GB50016）。

**Layer 3**（65类）的核心特征是**硬编码标准参数值**：

```
cim:ClassI_OR (I级洁净手术室)
    cim:minAirChangeRate         "36"^^xsd:integer    # >= 36 ACH
    cim:minPressureDifference    "8"^^xsd:decimal     # >= 8 Pa
    cim:temperatureRange         "21-25"              # 21~25 C
    cim:cleanlinessClass         "ISO 5"
    cim:regulatoryReference      "GB50333-2013 S4.0.1"
```

### 4.4 Layer 4: 运营生态系统

Layer 4（95类）覆盖五个子模块：

- **运营子模块（~38类）**：SOSA/SSN传感器观测、资产台账、告警管理（四级三态）
- **DDC控制子模块（~37类）**：27条控制回路，PID/级联/联锁三种模式
- **安全事件子模块（26类）**：5状态机+EmergencyPlan+ActionChain（详见第五章）
- **FAS子模块（12类）**：烟感/温感/火焰/可燃气体/手报五种探测器类型
- **CMMS子模块（13类）**：PM/CM/Inspection三种工单类型，ISO 14224对齐

### 4.5 六桥接：标准互操作的工程实现

CIM不是"替代一切"的封闭标准，而是"桥接一切"的开放框架。

**表 4-2 桥接本体对齐方法汇总**

| 桥接本体 | 外部标准 | 主要对齐方法 | 对齐声明数 | 关键对齐示例 |
|---------|---------|-------------|-----------|-------------|
| bridge_brick.ttl | Brick 1.3 | owl:equivalentClass | ~60 | cim:AHU = brick:AHU |
| bridge_223p.ttl | ASHRAE 223P | owl:equivalentClass+属性映射 | ~30 | cim:ConnectionPoint ~ s223:CP |
| bridge_ifc.ttl | IFC4 | owl:equivalentClass+ifcGlobalId | ~35 | cim:Equipment -> ifc:IfcBE |
| bridge_fso.ttl | FSO | rdfs:subClassOf+SPARQL双向 | 35设备+17属性 | cim:SmokeDetector < fso:Detector |
| bridge_bacnet.ttl | BACnet | cim-bacnet:bacnetPointOf | 9对象类型 | AI/AO/BI/BO/AV/MSV |
| bridge_iso14224.ttl | ISO 14224 | cim-cmms:failureMode | ~12 | 故障模式编码对齐 |

桥接本体合计775三元组。实测12/12个Brick设备类在CIM中实现100%覆盖。

### 4.6 545类分布全景

**表 4-3 CIM 545类按命名空间分布**

| # | 命名空间 | 类数 | 占比 | 代表性类 |
|---|---------|------|------|---------|
| 1 | cim-equip | 94 | 17.2% | AHU, Chiller, Transformer, OxygenManifold |
| 2 | cim-f | 56 | 10.3% | Continuant, Occurrent, FlowProcess, Quality |
| 3 | cim-space | 47 | 8.6% | Building, Floor, Zone, SurgeryRoom, ICU |
| 4 | cim-pt | 43 | 7.9% | TemperatureSensor, HumiditySensor, PressureSensor |
| 5 | cim-d | 41 | 7.5% | DesignRequirement, PerformanceCriteria |
| 6 | cim-o | 38 | 7.0% | AssetRecord, MaintenanceOrder, AlarmRecord |
| 7 | cim-cs | 37 | 6.8% | DDCStrategy, SequenceOfOperation, PIDLoop |
| 8 | cim-flow | 31 | 5.7% | FlowPath, FlowSegment, MassFlow, EnergyFlow |
| 9 | cim-med | 28 | 5.1% | ChilledWater, Oxygen, MedicalAir, N2O |
| 10 | cim-se | 26 | 4.8% | SecurityEvent, FireEvent, ActionChain |
| 11 | cim-ctrl | 21 | 3.9% | Sensor, Actuator, ControlLoop, Damper |
| 12 | cim-cmms | 13 | 2.4% | WorkOrder, PreventiveMaintenance |
| 13 | cim | 12 | 2.2% | System, Equipment, Space, Point, Flow |
| 14 | cim-fas | 12 | 2.2% | FireAlarmPanel, SprinklerHead, FirePump |
| 15 | cim-ref | 11 | 2.0% | Standard, Regulation, GB50333, WS435 |
| 16 | cim-bacnet | 9 | 1.7% | AnalogInput, AnalogOutput, BinaryInput |
| 17 | 其他 | ~26 | 4.8% | bridge对齐类 |
| | **合计** | **545** | **100%** | |

---

## 第五章 模式四：社会技术系统与安防应用

### 5.1 社会技术系统理论在医疗建筑中的应用

社会技术系统理论（Trist & Bamforth, 1951）的核心观点：一个有效的工作系统必须作为技术要素与社会要素的联合优化来设计。消防应急响应的成败不取决于技术系统的性能指标，而取决于技术系统与社会系统的协调程度。

CIM安全MVP将社会技术系统理论具体化为三个要素层：

**技术要素**：62个FAS探测器、4条BAS联动指令、5状态自动机，建模为Layer 4的SecurityEvent类层次（26类）。

**社会要素**：7个人员角色，权限从R1（执行级）到R5（最高决策级）。

| 角色代码 | 角色名称 | 权限等级 | 主要职责 |
|---------|---------|---------|---------|
| R1-OPR | 中控值班员 | R2 | 报警确认、预案启动、119联络 |
| R1-SEC | 安保队长 | R2 | 现场指挥、疏散组织 |
| R1-ELC | 电工班技术员 | R1 | 电气灭火、电源操作 |
| R1-GRD | 保安员 | R1 | 门禁管理、人员引导 |
| R1-NRS | 值班护士 | R1 | 患者疏散配合 |
| R3-SUP | 科室值班主管 | R3 | 事件升级决策 |
| R5-DIR | 医院值班领导 | R5 | L3级事件最终决策 |

**环境要素**：物理空间（5F配电间）、时间窗口（L2级900秒）、环境条件（烟雾浓度、温度变化率）。

### 5.2 安全事件本体：技术与社会的桥梁

安全事件子模块（26类）组织为事件模型（SecurityEvent基类, 对齐BFO Occurrent）、预案模型（EmergencyPlan, SPARQL查询自动匹配）和执行模型（ActionNode原子单位，同时携带BAS指令和角色分派）三个概念域。

事件状态机：
```
PENDING --> CONFIRMED --> IN_PROGRESS --> CLOSED --> ARCHIVED
误报捷径: PENDING --> ARCHIVED
```

### 5.3 L2电气火灾处置：四模式融合的实证

**四模式在L2场景中的角色**：
- **MBSE**：CIM定义语义模型，PIM提供执行引擎，PSM运行仿真
- **BFO**：火灾是Process(Occurrent)，建筑是Site(Continuant)，报警是ProcessBoundary
- **ISO 19650**：FAS探测器是Layer 4运营资产，设计准则是Layer 3
- **社会技术**：7角色、10动作节点（4自动+4人工+2确认）、4条BAS指令

**L2预案动作表**

| 序号 | 动作名称 | 负责角色 | 执行方式 | 时限(s) | 前置依赖 | BAS指令 |
|------|---------|---------|---------|---------|---------|---------|
| 1 | 确认火情 | 中控值班员 | 人工确认 | 120 | -- | -- |
| 2 | 切断电源 | 系统 | 自动 | 30 | [1] | PowerCutoff |
| 3 | 启动灭火 | 电工班 | 人工 | 300 | [2] | -- |
| 4 | 区域广播 | 系统 | 自动 | 10 | [1] | Broadcast |
| 5 | 启动疏散 | 安保队长 | 人工 | 600 | [4] | -- |
| 6 | 打开门禁 | 系统 | 自动 | 10 | [4] | DoorRelease |
| 7 | 电梯迫降 | 系统 | 自动 | 30 | [1] | ElevatorRecall |
| 8 | 通知医护 | 系统 | 自动 | 30 | [1] | -- |
| 9 | 拨打119 | 中控值班员 | 人工确认 | 120 | [3] | -- |
| 10 | 通知领导 | 系统 | 自动 | 30 | [1] | -- |

```
               确认火情 (1)
             /    |    |   \    \
            v     v    v    v    v
         切电源  广播  迫降 通知  通知
          (2)   (4)  (7) 医护  领导
           |     |  \        (8) (10)
           v     v   v
         灭火  疏散 门禁
          (3)  (5)  (6)
           |
           v
        拨打119 (9)
```

**仿真验证结果**：

```
场景:   内科楼5F配电室烟感报警 -> L2级电气火灾
状态:   PENDING->CONFIRMED->IN_PROGRESS->CLOSED->ARCHIVED (5态全通)
动作:   10/10完成, 0超时
时间:   840s模拟时间 < 900s L2时限 (安全裕度60s, 6.7%)
BAS:    4指令下发 (切电源/广播/门禁/电梯)
角色:   3人核心调度 (中控值班员/电工班/安保队长)
守恒:   4场景CRITICAL=0 (空气质量/冷水能量/温湿度/烟感联动)
```

---

## 第六章 数据联邦与验证

### 6.1 三源联邦架构

```
IFC实例                              BACnet点位
(几何+位置)                            (实时读数)
     |                                     |
     | cim:ifcGlobalId                     | cim-bacnet:bacnetPointOf
     |                                     |
     +-----------> CIM设备实体 <-----------+
                      |
                      | cim-cmms:maintenanceTarget
                      v
                 CMMS工单 (维保记录)
```

**Named Graph 9图架构**

| Named Graph | 内容 | 三元组数 | 更新策略 | 访问模式 |
|-------------|------|---------|---------|---------|
| graph/tbox | 本体定义 | ~12,000 | 版本级 | 只读 |
| graph/ifc | BIM静态实例 | ~8,000 | 一次写入 | 只读 |
| graph/bas/t0 | BAS正常态 | ~8,400 | 8h轮换 | 读写 |
| graph/bas/t1 | BAS异常态 | ~8,400 | 8h轮换 | 读写 |
| graph/bas/t2 | BAS告警态 | ~8,400 | 8h轮换 | 读写 |
| graph/cmms | CMMS工单 | ~4,000 | 日/月增量 | 读写 |
| graph/fas | FAS消防拓扑 | ~5,000 | 一次写入 | 只读 |
| graph/event | 安全事件 | ~3,000 | 实时 | 读写 |
| graph/pset | 设计参数 | ~5,941 | 一次写入 | 只读 |

### 6.2 SPARQL作为系统功能（PIM层）

| # | 模式名 | 业务问题 | 涉及Named Graph |
|---|--------|---------|-----------------|
| 1 | eq_full_status | "AHU-001当前什么状态？" | tbox+ifc+bas+cmms |
| 3 | energy_anomaly | "哪台设备功率偏离设计值>20%？" | bas+pset |
| 6 | ifc_bas_cmms_triangle | "BAS报警设备的CMMS工单在哪？" | ALL |
| 7 | safety_event_mvp | "烟感报警->预案匹配->动作执行" | fas+bas+event |
| 9 | cleanroom_compliance | "手术室洁净度是否达标？" | pset+bas+ifc |

### 6.3 12步验证管线

**表 6-1 12步验证流水线**

| 步骤 | 验证内容 | 方法 | 关键指标 | 结果 |
|------|---------|------|---------|------|
| step1-5 | IFC实体覆盖率 | BIM解析+Brick类映射 | 12/12覆盖率 | 100% PASS |
| step6 | SHACL形式化验证 | pyshacl+rdflib | VIOLATION/WARNING | 0/0 |
| step7 | 三源联邦SPARQL | ConjunctiveGraph | 5/5查询通过 | 30,016三元组 |
| step8-9 | 仿真门控 | ISO 19650+守恒方程 | CRITICAL=0 | 4场景通过 |
| step10 | 平台查询验证 | SPARQL端点+NG | 10/10 PASS | 含隔离测试 |
| step11 | 业务场景验证 | 8模式x28查询 | 28/28 PASS | 含能耗异常 |
| step12 | MVP端到端 | RDF+前端+仿真 | 10/10动作 | 840s<900s |

### 6.4 关键验证结果

**BIM实测覆盖率**：NBU 6个IFC文件(3.85M实体)，AHU12/Chiller4/CoolingTower4/Boiler2/Pump28/Fan16/VAV24/FCU48/Transformer6/UPS4/EmergencyGenerator2/SmokeDetector62。**12/12 Brick基础类100%覆盖**，合计212台。LOD从几何300-400提升到语义400-500。

**SHACL形式化验证**：4个ABox文件，**VIOLATION=0, WARNING=0**。

**三源联邦查询**：

| 查询 | 描述 | 结果行数 | 状态 |
|------|------|---------|------|
| Q1 | 设备-空间关联 | 212 | PASS |
| Q2 | 设备-BAS点位 | 186 | PASS |
| Q3 | 三角闭环(IFC+BAS+CMMS) | 11 | PASS |
| Q4 | FAS探测器-空间 | 62 | PASS |
| Q5 | CMMS工单-设备类型 | 48 | PASS |

**仿真门控**：4场景**CRITICAL=0**。**业务场景**：**28/28 PASS**。**MVP端到端**：**10/10动作，840s<900s**。

---

## 第七章 实现路径与工程实践

### 7.1 里程碑路径(M1->MVP)

| 里程碑 | 主要交付 | CIM层贡献 | PIM层贡献 | PSM层贡献 |
|--------|---------|-----------|-----------|-----------|
| M1骨架 | TBox骨架+9-Agent | 本体骨架(L0-1) | 验证框架 | -- |
| M2本体 | 545类完整TBox | 全量类(L0-4)+6桥接 | SHACL约束 | -- |
| M3实例 | NBU ABox+联邦 | 标准准则硬编码 | NG架构+SPARQL | Fuseki+ABox |
| M4验证 | 12步流水线 | FMEA故障模式 | 仿真引擎+守恒 | 验证脚本 |
| M5平台 | REST API+前端 | -- | API契约+模板 | FastAPI+HTML |
| MVP | L2安全预案 | 安全事件26类 | 状态机+动作链 | 仿真+可视化 |

### 7.2 风险管理与审计闭环

11个问题发现，5个CRITICAL，全部修复。代表性问题：hasSystemReference为空（修复：BRICK_TO_SYSTEM推理规则）、设备ID格式违规（修复：全量替换+registry更新）、命名空间冲突（修复：属性名映射）、CHL前缀缺失导致Q4失败（修复：前缀声明补充）。

三条核心原则：（1）先原型后全量；（2）数字必须实测；（3）ID对照治理规范。

### 7.3 可视化平台作为PSM实证

HTML平台（677行，零依赖）含5面板（事件中心/态势中心全功能，预案中心/调度中心/系统设置配置展示）。同一套CIM+PIM可驱动完全不同的PSM前端。

---

## 第八章 结论与展望

### 8.1 四模式的协同贡献

**模式一（MBSE）**：三层分离确保CIM(545类)/PIM(9SPARQL+6API+9NG)/PSM(Fuseki+FastAPI)可独立演化。rdflib-fallback验证PSM可替换性。

**模式二（BFO）**：Continuant/Occurrent解决静态本体无法表达运营过程的缺陷。FlowPath/FlowProcess双重性使设计验证与运营监控共存。8阶段生命周期链为三源数据提供时间定位。

**模式三（ISO 19650）**：545类覆盖5大系统，6桥接对齐6个标准。61,941三元组的三源联邦验证了互操作可行性（5/5 SPARQL, 28/28业务, SHACL=0）。

**模式四（社会技术）**：L2 MVP涵盖62 FAS探测器、26类、10动作、7角色。10/10完成，840s<900s。8项CIM资产直接复用。

### 8.2 局限性

**单一医院验证**：全部数据基于NBU一个项目的IFC模型。**仿真BAS**：1,055点位由仿真器生成，缺乏真实噪声特征。**Docker未启动**：Fuseki容器未实际运行，验证基于rdflib。**DDC手动枚举**：27条回路基于规范枚举，真实DDC通常200-500条。**MVP场景有限**：仅验证L2电气火灾一种场景。

### 8.3 从PSM到规模化

**M6（真实BAS接入）**：MQTT/OPC-UA网关替代仿真器，三快照升级为滑动窗口+时序数据库。验收标准：三源联邦不因数据源切换而退化。

**M7（多医院站点）**："TBox共享、ABox隔离"原则，Named Graph增加站点维度（graph/NBU/ifc, graph/ZJU/ifc）。核心目标：跨站点同类设备对标分析。

这正是四模式联锁的最终价值：CIM层的545类定义（模式三）以BFO范畴保证本体一致性（模式二），通过MBSE三层分离实现跨项目复用（模式一），在每个具体项目中桥接技术系统与社会组织（模式四）。四模式不是四个独立的理论贡献，而是一个完整的方法论闭环。

---

## 附录

### 附录A：545类命名空间分布表

**表 A-1 CIM项目核心指标汇总**

| 指标类别 | 指标名 | 数值 | 验证来源 |
|---------|--------|------|---------|
| 本体规模 | OWL类总数 | 545 | TBox文件统计 |
| 本体规模 | 命名空间 | 17 | ontology_skeleton.ttl |
| 本体规模 | TBox三元组 | 5,395 | rdflib加载统计 |
| 本体规模 | 桥接本体三元组 | 775 | bridge/*.ttl |
| 实例规模 | ABox三元组总数 | 61,941 | ConjunctiveGraph |
| 实例规模 | Named Graph数量 | 9 | step10验证 |
| 实例规模 | 设备实例 | 212 | step1-5盘点 |
| 实例规模 | BACnet点位 | 1,055 | BAS仿真器输出 |
| 实例规模 | CMMS工单 | 735 | nbu_cmms_workorders.ttl |
| 实例规模 | FAS探测器 | 62 | nbu_fas_instances.ttl |
| 验证结果 | SHACL VIOLATION | 0 | step6 |
| 验证结果 | 联邦查询通过率 | 5/5 | step7 |
| 验证结果 | 业务场景通过率 | 28/28 | step11 |
| 验证结果 | 仿真门控CRITICAL | 0 | step8-9 |
| MVP | 动作节点完成率 | 10/10 | smoke_alarm_scenario.py |
| MVP | 处置总时间 | 840s(<900s) | 独立仿真 |
| MVP | BAS联动指令 | 4 | 切电源/广播/门禁/电梯 |
| MVP | 代码总量 | 2,747行 | 15文件 |

### 附录B：L2预案10动作完整表

**表 B-1 L2电气火灾处置预案--完整10节点动作定义**

| 序号 | ActionNode ID | 动作名称 | 负责角色 | 执行方式 | 时限(s) | 前置依赖 | BAS指令类型 | BAS目标设备 |
|------|-------------|---------|---------|---------|---------|---------|-------------|-------------|
| 1 | ACTION-001 | 确认火情 | 中控值班员(R1-OPR) | ManualConfirmation | 120 | -- | -- | -- |
| 2 | ACTION-002 | 切断电源 | 系统 | AutomaticExecution | 30 | ACTION-001 | PowerCutoffCommand | ATS-5F-001 |
| 3 | ACTION-003 | 启动灭火 | 电工班(R1-ELC) | ManualExecution | 300 | ACTION-002 | -- | -- |
| 4 | ACTION-004 | 区域广播 | 系统 | AutomaticExecution | 10 | ACTION-001 | BroadcastCommand | PA-5F-001 |
| 5 | ACTION-005 | 启动疏散 | 安保队长(R1-SEC) | ManualExecution | 600 | ACTION-004 | -- | -- |
| 6 | ACTION-006 | 打开门禁 | 系统 | AutomaticExecution | 10 | ACTION-004 | DoorReleaseCommand | ACC-5F-EAST |
| 7 | ACTION-007 | 电梯迫降 | 系统 | AutomaticExecution | 30 | ACTION-001 | ElevatorRecallCommand | ELV-5F-001 |
| 8 | ACTION-008 | 通知医护 | 系统 | AutomaticExecution | 30 | ACTION-001 | -- | -- |
| 9 | ACTION-009 | 拨打119 | 中控值班员(R1-OPR) | ManualConfirmation | 120 | ACTION-003 | -- | -- |
| 10 | ACTION-010 | 通知领导 | 系统 | AutomaticExecution | 30 | ACTION-001 | -- | -- |

仿真结果: 10/10完成, 0超时, 总耗时840s<900s时限, 4条BAS指令全部下发。DAG关键路径: ACTION-001->ACTION-002->ACTION-003->ACTION-009, 总时限570s(占900s的63.3%)。

### 附录C：核心术语表(30项)

| # | 术语 | 英文 | 定义 |
|---|------|------|------|
| 1 | ABox | Assertion Box | RDF知识图谱的实例层 |
| 2 | ACH | Air Changes per Hour | 每小时换气次数，洁净手术室>=36 |
| 3 | AHU | Air Handling Unit | 空调箱 |
| 4 | ATS | Automatic Transfer Switch | 自动转换开关 |
| 5 | BAS | Building Automation System | 楼宇自控系统 |
| 6 | BFO | Basic Formal Ontology | 基础形式本体(ISO/IEC 21838-2) |
| 7 | BIM | Building Information Modeling | 建筑信息模型 |
| 8 | CIM | Common Information Model | 统一信息模型，本项目核心本体 |
| 9 | CMMS | Computerized Maintenance Management System | 设备维保管理系统 |
| 10 | Continuant | 持续体 | BFO范畴：时间中持续存在的实体 |
| 11 | DAG | Directed Acyclic Graph | 有向无环图 |
| 12 | DDC | Direct Digital Control | 直接数字控制 |
| 13 | FACU | Fire Alarm Control Unit | 火灾报警控制器 |
| 14 | FAS | Fire Alarm System | 消防自动报警系统 |
| 15 | FlowPath | 流动路径 | 持续体：管路拓扑连接关系 |
| 16 | FlowProcess | 流动过程 | 发生体：介质实际流动 |
| 17 | IFC | Industry Foundation Classes | BIM数据交换标准(ISO 16739) |
| 18 | JSON-LD | JSON for Linking Data | 嵌入RDF语义的JSON格式 |
| 19 | MBSE | Model-Based Systems Engineering | 基于模型的系统工程 |
| 20 | MDA | Model Driven Architecture | 模型驱动架构(OMG) |
| 21 | MVP | Minimum Viable Product | 最小可行产品 |
| 22 | Named Graph | 命名图 | RDF 1.1逻辑分区机制 |
| 23 | Occurrent | 发生体 | BFO范畴：时间中展开的过程 |
| 24 | OWL | Web Ontology Language | W3C本体描述语言 |
| 25 | PIM | Platform Independent Model | 平台无关模型(CIM的工程化) |
| 26 | PSM | Platform Specific Model | 平台特定模型(PIM的实例化) |
| 27 | SHACL | Shapes Constraint Language | W3C RDF验证语言 |
| 28 | SPARQL | SPARQL Protocol and RDF Query Language | W3C RDF查询语言 |
| 29 | TBox | Terminological Box | RDF知识图谱的术语层 |
| 30 | 社会技术系统 | Socio-Technical System | 技术与社会联合优化的系统设计理论 |

---

**全文总结**

本白皮书以四个相互联锁的模式——MBSE三层架构、BFO动态本体、ISO 19650全域覆盖、社会技术系统——为智识骨架，系统阐述了CIM统一领域模型的设计、实现与验证。模式一提供架构分层（第二章），模式二解决静态本体的过程性缺陷（第三章），模式三以545类五层本体实现全域覆盖（第四章），模式四桥接技术系统与社会组织（第五章）。四模式在L2电气火灾MVP中融合验证——840秒完成10动作处置，在900秒时限内闭环。四模式联锁的方法论不仅适用于医疗建筑，其架构设计具有向数据中心、GMP洁净厂房和生物安全实验室迁移的潜力——同一CIM+PIM，不同的PSM，这正是MBSE的承诺。
