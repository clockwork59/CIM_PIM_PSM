# 医疗建筑数字孪生统一领域模型（CIM）技术白皮书

**副标题**: 基于 ISO 19650 + BFO 2020 的多智能体知识工程方法论与实践

**版本**: v2.0  
**日期**: 2026 年 5 月  
**作者**: CIM-PIM-PSM 项目组  
**目标读者**: 医院信息化决策者 / BIM 咨询顾问 / 智慧建筑技术负责人 / 学术研究者

---

## 摘要

医疗建筑是当代最复杂的建筑类型之一。一栋综合医院同时运行暖通空调（HVAC）、电气配电、医用气体、消防系统与楼宇自控（BAS）等五大机电系统，受 GB 50333《医院洁净手术部建筑技术规范》、WS 435《医用气体工程技术规范》、IEC 60364-710 等多部强制标准约束。然而，支撑这些系统运营的三大数据源——BIM/IFC 建筑信息模型、BAS/BACnet 楼宇自控系统和 CMMS 设备维保管理系统——长期处于割裂状态，形成严重的信息孤岛。现有行业本体标准如 Brick Schema 1.3（约 620 类）、ASHRAE 223P（约 380 类）和 IFC4（约 800 类型）各有所长，但均未覆盖医疗建筑的全部语义需求，且三者之间缺乏原生互操作能力。

本白皮书提出一种面向医疗建筑数字孪生的统一领域模型（Common Information Model, CIM），采用 OMG 模型驱动架构（MDA）的 CIM-PIM-PSM 三层分离，以 BFO 2020 基础形式本体为顶层范畴框架，按 ISO 19650 信息管理标准将本体组织为五层结构（Layer 0 基础层至 Layer 4 运营层）。CIM 本体包含 545 个 OWL 类（owl:Class），覆盖 17 个命名空间，通过 6 个桥接本体（Bridge Ontology）实现与 Brick、ASHRAE 223P、IFC4、FSO、BACnet 及 ISO 14224 的语义对齐。在实例层面，项目基于宁波大学附属医院（NBU Medical Clinic）真实 IFC 模型构建了包含 61,941 个 RDF 三元组的知识图谱，组织于 9 个 Named Graph 中，支持三源（IFC + BAS + CMMS）SPARQL 联邦查询。全部 5 条联邦验证查询通过，SHACL 形式化验证零违规（VIOLATION = 0），28 条业务场景查询全部通过。作为端到端验证，项目实现了 L2 级电气火灾安全 MVP（最小可行产品），涵盖 62 个 FAS 探测器、5 状态事件机、10 个动作节点和 4 条 BAS 联动指令，仿真耗时 840 秒，在 900 秒时限内完成。本研究证明，通过严谨的本体工程和多智能体协同建模方法，可以在医疗建筑领域实现从设计到运营的全生命周期语义互操作。

---

## 第一章 引言

### 1.1 医疗建筑数字化转型的挑战

医疗建筑远非普通商业建筑的简单放大。当一栋综合医院从设计图纸走向日常运营，它所承载的技术系统复杂性远超写字楼、酒店或商业综合体。普通商业建筑通常只需暖通空调、基础电气和消防三大系统即可满足运营需求，而医疗建筑必须同时运行五大独立却紧密耦合的机电系统，每一个系统都直接关系到患者安全和医疗质量。

第一大系统是暖通空调系统（HVAC）。在普通办公环境中，空调的职能不过是维持舒适温湿度；而在医疗建筑中，HVAC 系统承担着远更严苛的使命。洁净手术室必须达到每小时不低于 36 次换气（36 ACH），室内与相邻区域的压差不得低于 8 Pa，温度严格控制在 21~25 摄氏度范围内，这些均为 GB 50333 的强制性要求。负压隔离病房（如传染病 ICU）则需要反向压差设计，确保含有病原体的空气不会外逸。一套 HVAC 系统同时服务洁净正压区域和负压隔离区域，其控制逻辑的复杂程度远超常规建筑。

第二大系统是电气配电系统。医疗建筑的电气系统必须遵循 IEC 60364-710（医疗场所电气安装）的严格规定。手术室强制要求 IT 隔离电源系统，即采用隔离变压器将手术区域的电力供应与公共电网隔离，以避免漏电流对患者的直接伤害。整栋建筑需要双路市电供电加柴油发电机应急保障，关键生命安全区域（手术室、ICU、产房）的电力切换时间不得超过 0.5 秒。变压器、自动转换开关（ATS）、不间断电源（UPS）和应急发电机构成了多层级的供电保障体系，任何一个环节的失效都可能危及正在进行手术的患者。

第三大系统是医用气体系统。这是医疗建筑区别于所有其他建筑类型的标志性系统。根据 WS 435《医用气体工程技术规范》，每间手术室至少需要氧气（O2）、真空负压吸引（VAC）和医用压缩空气（CAIR）三种气体终端，部分手术室还需要氧化亚氮（N2O）终端。气体从中心供应站（氧气汇流排、真空泵组、医用空压机组）通过专用管路输送到各个末端，管路的材质、连接方式、压力等级和泄漏检测均有严格规范。气体供应的中断直接威胁手术台上患者的生命。

第四大系统是消防系统（Fire Protection）。医院的消防设计受 GB 50016《建筑设计防火规范》约束，但其特殊性在于：患者的行动能力有限（卧床病人、手术中病人、新生儿等），疏散时间要求更长，防火分区划分必须兼顾医疗功能分区。消防泵、喷头、烟感探测器、手动报警按钮和火灾自动报警控制器（FACU）构成的网络，需要与 HVAC 风阀联动（火灾时关闭送风、启动排烟）、与电气系统联动（切断非消防电源）、与广播系统联动（启动疏散广播），形成跨系统的联动响应链。

第五大系统是楼宇自控系统（BAS/Controls）。BAS 基于 ASHRAE 135（BACnet 协议）实现对上述四大系统的实时监控和联动控制。数以千计的传感器、执行器和直接数字控制器（DDC）通过 BACnet 网络连接，采集温度、湿度、压力、流量、CO2 浓度、功率等物理量，并下发控制指令。BAS 是五大系统的"神经系统"，但其数据模型（BACnet 对象：AI/AO/BI/BO/AV/MSV）是纯技术性的，缺乏与建筑空间、设备身份和维护历史的语义关联。

以一台正在进行心脏外科手术的 I 级洁净手术室为例，可以直观地理解五大系统的交叉依赖。HVAC 系统必须维持 ISO 5 级洁净度（即每立方米空气中 >=0.5 微米的粒子数不超过 3,520 个），送风经过三级过滤（初效 G4 + 中效 F8 + 高效 H13）处理，换气次数不低于 36 ACH。电气系统为手术区域提供 IT 隔离电源，隔离变压器的绝缘监视仪实时监测漏电流，一旦超过阈值立即发出声光报警（但不切断电源，因为手术不能中断）。麻醉工作站通过医用气体终端接入 O2（4L/min）、N2O（2L/min）和 CAIR（6L/min），真空负压吸引用于术野清洁。术中一旦触发火灾报警，消防系统必须在关闭该区域送风阀门的同时启动排烟，但不能切断手术室的电源和医用气体供应——这需要 BAS 控制逻辑精确识别报警区域与手术室的空间关系，做出差异化的联动响应。

五大系统的耦合关系使医疗建筑成为一个高度复杂的社会技术系统。HVAC 的运行依赖电气系统的稳定供电；消防联动需要同时控制 HVAC 风阀和电气开关；医用气体的压缩机和真空泵需要电力驱动和冷却水支持；BAS 则横跨所有系统进行监控和协调。任何单一系统的模型都无法捕捉这种跨系统耦合的全貌。更为关键的是，医疗建筑承载着三个等级的生命安全分类：LIFE_SAFETY 级（手术室、ICU、产房，系统故障直接威胁生命）、CRITICAL 级（检验科、药房、血库，环境失控导致医疗差错）和 NORMAL 级（门诊、行政、后勤，等同普通建筑）。这种分级制度要求信息系统能够识别每个空间和设备所属的安全等级，在故障和应急场景中实施差异化的响应策略。

### 1.2 信息孤岛：BIM、BAS 与 CMMS 的割裂

医疗建筑运营所依赖的数据散布在三个独立系统中，各自使用不同的数据模型、不同的标识体系和不同的更新频率，它们之间缺乏统一的语义层来建立关联。这种割裂不是技术选型的偶然结果，而是建筑行业分工模式的结构性产物：设计院交付 BIM 模型、自控集成商交付 BAS 系统、物业管理方使用 CMMS 软件，三方的数据标准和业务流程从未被设计为互通。

**BIM/IFC** 是建筑信息模型的工业标准（buildingSMART International），采用 IFC2X3 或 IFC4 格式。BIM 模型在几何表达方面极为丰富——每台设备的三维坐标、管道的走向路由、空间的边界尺寸都精确记录。然而，BIM 模型在语义层面却相当薄弱。IFC 文件中的一台空调箱（AHU）拥有 GlobalId、几何表示和系统归属，但不包含其运行状态、能效参数、控制策略或维护历史。更严重的问题是，BIM 模型在竣工交付后几乎不再更新。设计阶段精心构建的信息模型，在建筑进入运营期后迅速沦为"电子化的竣工图纸"，与建筑的实际运行状态脱节。

**BAS/BACnet** 是楼宇自控系统的通信协议标准（ASHRAE 135-2020）。BAS 系统擅长的是实时性——它以秒级频率采集数以千计的传感器读数，记录设备的运行状态和控制输出。但 BAS 数据的语义是极度匮乏的。一个 BACnet 模拟量输入对象 `AI:1` 的值为 23.5，这个数字本身不包含任何上下文信息：它测量的是哪台设备？在建筑的什么位置？23.5 的单位是摄氏度还是帕斯卡？是正常值还是已经超出设计范围？运维工程师必须依靠经验或查阅纸质资料才能回答这些问题。BAS 系统拥有实时数据，但不知道这些数据"意味着什么"。

**CMMS**（Computerized Maintenance Management System）是设备维保管理系统。CMMS 记录着设备的维护计划、工单执行历史、故障报告和备件消耗，这些信息对于设备全生命周期管理至关重要。然而，CMMS 系统使用各厂商私有的数据格式，缺乏标准化的设备分类和故障编码（虽然 ISO 14224 提供了参考，但实际采纳率有限）。更关键的是，CMMS 中的"设备"与 BIM 中的"几何实体"以及 BAS 中的"监控点位"之间没有自动化的对应关系。

以下具体场景可以说明三源割裂的实际后果。假设宁波大学附属医院的一台空调箱 AHU-001 出现送风温度异常：

- **在 IFC 中**，`AHU-001` 是一个 IfcAirTerminalBox 实体，拥有 GlobalId `2O2Fr$t4X7Zf8NOew3FNld`，位于三楼手术区（有精确三维坐标），但没有任何运行数据。
- **在 BACnet 中**，Device:101 下的 `AI:1` 读数为 28.5（送风温度传感器），`AI:2` 读数为 85%（相对湿度），但系统不知道这些点位属于哪台命名设备，也不知道 28.5 度是否超出了洁净手术室 21~25 度的允许范围。
- **在 CMMS 中**，工单 `WO-PM-0001`（季度滤网更换预防性维护）的目标资产标注为 `ASSET-AHU-001`，但系统无法自动关联到 BAS 当前报警状态，也无法在建筑平面图上定位该设备。

运维人员面对 BAS 报警时，需要手动查阅 IFC 图纸确定设备位置，再登录 CMMS 查看维保记录判断是否存在反复故障——这一过程效率极低，且容易因信息碎片化而导致误判。在紧急场景（如火灾报警）中，这种延迟可能带来严重后果。

**表 1-1 三源数据特征对比**

| 特征维度 | BIM/IFC | BAS/BACnet | CMMS |
|---------|---------|------------|------|
| 数据内容 | 建筑几何 + MEP 设备布局 | 传感器读数 + 控制状态 | 维保工单 + 故障记录 |
| 数据格式 | IFC2X3/IFC4 (EXPRESS) | ASHRAE 135 (BACnet 对象) | 各厂商私有格式 |
| 更新频率 | 建设期一次性交付 | 实时（秒级采集） | 日/周/月增量 |
| 标识体系 | IfcGlobalId (GUID) | BACnet Device/Object ID | 资产标签 (Asset Tag) |
| 语义强度 | 几何丰富，语义薄弱 | 实时数据，无语义标注 | 维护记录，脱离物理模型 |
| 核心缺陷 | 竣工即过时 | 点位名称无上下文 | 与设备台账脱钩 |

三源之间缺失的正是一个**统一的语义中间层**——一种能够同时理解 IFC 的空间位置、BACnet 的实时读数和 CMMS 的维护历史，并将它们关联到同一个设备实体上的知识表示框架。

### 1.3 现有标准的局限性

建筑信息化领域并非缺乏语义标准，相反，过去十年间涌现了多个有影响力的本体和数据模型。问题在于，这些标准各自覆盖领域的某个切面，没有一个标准能够满足医疗建筑从设计到运营的全部语义需求，更没有标准提供跨数据源联邦查询的原生支持。

**Brick Schema 1.3**（brickschema.org）是建筑领域最成熟的 RDF/OWL 本体之一，由斯坦福大学、加州大学伯克利分校等学术机构推动。Brick 在传感器点位（Point）和通用建筑设备（Equipment）的分类方面表现优异，约提供 620 个类定义，支持 OWL-DL 推理。然而，Brick 的设计初衷是通用建筑能效分析，缺乏医疗建筑的专项语义。Brick 没有定义洁净手术室（Operating Room）的换气次数约束，没有医用气体设备（氧气汇流排、真空泵组）的类层次，没有生命安全分级的概念，也没有设备全生命周期（从设计到退役）的过程模型。对于医院运维而言，Brick 能告诉你"这是一台空调箱"，但无法告诉你"这台空调箱服务的是洁净手术室，送风必须满足 GB 50333 的 36 ACH 要求"。

**ASHRAE Standard 223P**（ASHRAE 2023 年发布草案）专注于 HVAC 系统的语义建模，约包含 380 个类定义。223P 的核心创新是连接点（ConnectionPoint）模型和介质（Medium）层级体系，能够精确描述设备之间的物理连接方式和流经的介质类型。这对于 HVAC 系统拓扑分析极具价值。但 223P 的覆盖范围严格限定在 HVAC 领域，不涉及电气配电、消防系统和医用气体；更重要的是，223P 没有运营维护（O&M）的任何概念——没有工单、没有故障模式、没有维保计划。223P 能描述"冷水通过这个连接点流入冷冻水泵"，但无法表达"这台泵上个月因轴承故障停机了 4 小时"。

**IFC4**（buildingSMART International, ISO 16739-1:2018）是建筑信息模型的工业基础标准，约定义 800 个实体类型。IFC 在建筑几何和空间层级方面无可替代：IfcSite → IfcBuilding → IfcBuildingStorey → IfcSpace 的空间层次，以及 IfcDistributionElement 下的 MEP 设备分类体系，构成了建筑数字化的基础数据模型。然而，IFC 本质上是一个"几何优先"的标准。其数据模型以 EXPRESS 语言定义，虽然 ifcOWL 提供了 OWL 版本，但 IFC 的属性集（PropertySet）机制灵活有余、约束不足，导致不同 BIM 软件导出的 IFC 文件在语义层面差异很大。IFC 没有 BAS 数据点位的概念（"AI:1 传感器读数 23.5"在 IFC 中无法表达），也没有 CMMS 维保工单的模型。

**FSO（Fire Safety Ontology）** 约包含 90 个类，提供了消防系统的基础语义框架，但缺少探测器细分类型（烟感/温感/火焰/可燃气体）和应急联动预案的建模能力。

**表 1-2 现有标准对比分析**

| 评估维度 | Brick 1.3 | ASHRAE 223P | IFC4 | FSO | CIM (本项目) |
|---------|-----------|-------------|------|-----|-------------|
| 类定义数量 | ~620 | ~380 | ~800 | ~90 | 545 |
| HVAC 设备 | 中 | 强 | 弱 | 无 | 强 |
| 电气设备 | 弱 | 无 | 弱 | 无 | 强 |
| 医用气体 | 无 | 无 | 无 | 无 | 强 |
| 消防系统 | 弱 | 无 | 弱 | 中 | 强 |
| 传感器/点位 | 强 | 弱 | 无 | 无 | 强 (Brick 对齐) |
| 连接点/介质 | 无 | 强 | 无 | 无 | 强 (223P 对齐) |
| 空间层级 | 中 | 无 | 强 | 无 | 强 (IFC 对齐) |
| 生命周期 | 无 | 无 | 部分 | 无 | 强 (8 阶段) |
| 运维/维保 | 无 | 无 | 无 | 无 | 强 (CMMS) |
| BAS 数据映射 | 部分 | 无 | 无 | 无 | 强 (BACnet 桥接) |
| 医疗专项 | 无 | 无 | 无 | 无 | 强 |
| 跨标准对齐 | 无 | 无 | 无 | 无 | 6 桥接本体 |

上述四个标准的共同问题是**互不对齐**。不存在一条现成的 SPARQL 查询能够同时检索"这台 AHU 的 Brick 类型、223P 连接点结构和 IFC 空间位置"。每个标准都是一个独立的语义孤岛，与它们所要解决的数据孤岛问题形成了讽刺性的映射。医疗建筑需要的不是又一个单领域本体，而是一个能够横跨五大系统、纵贯全生命周期、桥接三大数据源的统一语义框架。

### 1.4 研究目标与贡献

基于上述分析，本研究的核心目标是：构建一个面向医疗建筑数字孪生的统一领域模型（CIM），实现从本体设计到运行系统的完整技术路径。具体而言，本研究提出以下四项贡献：

**贡献一：545 类统一本体，横跨五大机电系统与全生命周期。** CIM 本体包含 545 个 OWL 类定义，分布于 17 个命名空间，组织为 5 层结构（Layer 0 BFO 基础层、Layer 1 概念层、Layer 2 参考层、Layer 3 设计层、Layer 4 运营层）。与现有标准相比，CIM 不仅覆盖 HVAC（对齐 Brick + 223P）和消防（对齐 FSO），还新增了医用气体设备类层次（OxygenManifold、VacuumPump、MedicalAirCompressor、N2OManifold）、电气生命安全分级（IT 隔离电源、双路供电 + ATS）以及从概念设计到退役的 8 阶段生命周期过程模型。CIM 本体以 BFO 2020 为顶层范畴框架（Continuant / Occurrent），确保不同领域子本体之间的哲学一致性。

**贡献二：CIM-PIM-PSM 三层架构，从本体到运行服务的完整映射。** 借鉴 OMG 模型驱动架构（MDA），本项目将建筑信息建模分解为三个层次：CIM 层（计算无关模型）定义领域语义本身，回答"什么是什么"；PIM 层（平台无关模型）定义 SPARQL 端点、Named Graph 架构和 REST API 契约，回答"怎么查询"；PSM 层（平台特定模型）定义具体部署方案（Apache Jena Fuseki 三元组存储、FastAPI 服务、安全 MVP 可视化平台），回答"如何运行"。三层分离确保本体设计不受特定技术平台的绑定，同时提供从抽象概念到可运行代码的清晰变换路径。

**贡献三：三源知识图谱联邦，实现 IFC + BAS + CMMS 的语义互操作。** 基于宁波大学附属医院的真实 IFC 模型，本项目构建了包含 61,941 个 RDF 三元组的知识图谱，组织于 9 个 Named Graph 中。通过 CIM 设备节点作为三源的语义锚点（IFC 通过 cim:ifcGlobalId 关联、BAS 通过 cim-bacnet:bacnetPointOf 关联、CMMS 通过 cim-cmms:maintenanceTarget 关联），实现了三角闭环的联邦查询。全部 5 条 SPARQL 联邦验证查询通过，其中关键的 Q3 三角闭环查询返回 11 行跨源关联记录，证明 BAS 报警设备可以通过 CIM 同时定位到 IFC 物理位置和 CMMS 维保历史。

**贡献四：安全 MVP 端到端验证，证明社会技术系统建模的可行性。** 作为 CIM 的应用层验证，项目实现了 L2 级电气火灾安全响应的最小可行产品（MVP）。MVP 涵盖 62 个 FAS 探测器、5 状态事件机（IDLE → DETECTED → CONFIRMED → RESPONDING → RESOLVED）、10 个动作节点和 4 条 BAS 联动指令（风阀关闭、排烟启动、非消防电源切断、广播疏散），并融合了 7 个社会角色（监控中心值班员、安保队长、电工、护士长、科室主管、医院值班领导等）的职责分工。独立仿真验证显示 10/10 动作节点执行完成，总耗时 840 秒，在 900 秒时限内通过。

---

## 第二章 理论基础与方法论

### 2.1 模型驱动架构（MDA）与 CIM-PIM-PSM

模型驱动架构（Model Driven Architecture, MDA）是对象管理组织（OMG）于 2001 年提出的软件工程方法论，其核心思想是将系统设计分解为计算无关模型（CIM）、平台无关模型（PIM）和平台特定模型（PSM）三个层次，通过模型变换（Model Transformation）实现从业务概念到可执行代码的自动化映射。MDA 最初面向企业应用软件开发，但其三层分离的设计哲学对建筑信息领域同样具有深刻的适用性。

在传统建筑信息化实践中，本体设计和系统实现往往紧密耦合。一个 Brick Schema 的 RDF 本体被直接加载到某个特定的三元组存储（如 GraphDB 或 Stardog），查询语句写死在特定应用的代码中，部署方案与本体设计不可分离。这种做法的后果是：本体的可移植性受限于特定技术栈，更换三元组存储或前端框架可能需要重构整个数据管线。

本项目将 MDA 的三层架构适配到医疗建筑领域，赋予每一层明确的职责边界：

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   CIM (计算无关模型) — "什么是什么"                              │
│                                                                 │
│   545 owl:Class, 17 命名空间                                    │
│   Layer 0 (BFO) → Layer 1 (概念) → Layer 2 (参考)              │
│   → Layer 3 (设计) → Layer 4 (运营)                             │
│   + 6 桥接本体 (Brick/223P/IFC/FSO/BACnet/ISO14224)             │
│                                                                 │
│   纯语义定义, 不涉及任何平台技术选型                             │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   PIM (平台无关模型) — "怎么查询"                               │
│                                                                 │
│   SPARQL 端点 + Named Graph 架构 (9 图)                         │
│   REST API 契约 (6 端点)                                        │
│   联邦查询模式 (5 验证 + 9 业务)                                 │
│   TBox/ABox 分离策略, ID 治理规范                                │
│                                                                 │
│   定义数据服务接口, 不指定具体实现产品                            │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   PSM (平台特定模型) — "如何运行"                               │
│                                                                 │
│   Apache Jena Fuseki 4.10 (TDB2 持久化, OWL-micro 推理)         │
│   FastAPI 6 端点 (Python + rdflib)                              │
│   Docker 容器化部署                                              │
│   安全 MVP 可视化平台 (HTML + JavaScript + WebSocket)            │
│                                                                 │
│   具体技术选型, 可替换而不影响上层                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

CIM 层是整个架构的核心资产。545 个 OWL 类定义以 Turtle (RDF) 格式持久化于 15 个 TTL 文件中，总计 5,395 个三元组。这些定义完全独立于任何技术平台——无论使用 Fuseki、GraphDB、Blazegraph 还是 Amazon Neptune 作为三元组存储，CIM 层的本体定义不需要做任何修改。PIM 层定义了如何组织和查询 CIM 数据：9 个 Named Graph 的语义分区策略、TBox/ABox 的分离原则、ID 治理规范（{TYPE}-{MODEL}-{N} 格式）以及 14 条 SPARQL 查询模板（9 条业务查询 + 5 条验证查询）。PIM 层的设计同样是技术中立的——SPARQL 1.1 是 W3C 标准，Named Graph 是 RDF 1.1 规范的一部分，这些接口在不同三元组存储之间可移植。PSM 层则将抽象的 PIM 设计映射到具体产品：Fuseki 提供 SPARQL 端点和 Named Graph 管理，FastAPI 封装业务查询为 RESTful 服务，Docker 提供可复现的部署环境。

三层分离带来的关键价值是**可替换性**。当项目从概念验证（PoC）阶段进入生产部署时，PSM 层可以从单机 Fuseki 替换为分布式集群（如 Stardog 集群或 Amazon Neptune），而 CIM 层和 PIM 层完全不受影响。同样，前端应用从 MVP 的简单 HTML 页面升级为企业级 Web 应用时，只需要替换 PSM 层的前端实现，后端的 SPARQL 查询模式保持不变。

### 2.2 BFO 2020 基础本体对齐

基础形式本体（Basic Formal Ontology, BFO）是由哲学家 Barry Smith 等人开发的顶层本体框架，已被 ISO/IEC 21838-2:2021 标准化。BFO 的核心设计原则是将存在的一切实体划分为两个互不重叠的范畴：**持续体（Continuant）** 和 **发生体（Occurrent）**。持续体是在时间中持续存在、可以拥有不同属性的实体；发生体是在时间中展开、具有时间部分的过程。这一区分看似抽象，但对于医疗建筑领域模型而言具有深刻的实际意义。

医疗建筑中的设备和空间是典型的持续体。一台冷水机组（Chiller）从安装到退役，始终是"同一台设备"，尽管其运行参数（COP、冷量输出、运行时间）不断变化。手术室作为一个功能空间也是持续体——它可能在不同时间段被用于不同手术，其温湿度和压差在持续波动，但它始终是"同一个手术室"。流动路径（FlowPath，即冷冻水从冷机到末端的拓扑连接）也是持续体，因为管路的物理连接关系在建筑生命周期内基本不变。

相对地，HVAC 过程和维护活动是典型的发生体。冷冻水在管路中的实际流动（FluidFlowProcess）有明确的开始时间和结束时间；一次手术室的消毒维护作业（MaintenanceActivity）也是在特定时段内展开的过程。BAS 系统监测的本质上就是发生体——传感器读数是对某个时刻物理过程状态的观测。

这种区分为什么在医疗建筑领域特别重要？因为设计文档和竣工模型描述的主要是持续体（设备规格、空间布局、系统拓扑），而运营数据关注的是发生体（运行过程、维护活动、故障事件）。BIM/IFC 本质上是一个持续体模型——它记录的是建筑"是什么样的"，而不是"正在发生什么"。BAS 本质上是一个发生体监测系统——它采集的是物理过程的实时状态。将两者纳入同一个本体框架时，如果不做持续体/发生体的范畴区分，就会产生本体论层面的混淆：把设备的运行状态（发生体的属性）错误地建模为设备本身（持续体）的固有属性。

CIM 本体的 Layer 0 定义了 BFO 范畴与医疗建筑概念的映射关系：

**表 2-1 BFO 范畴映射**

| BFO 范畴 | BFO 类 | CIM 类（示例） | 说明 |
|---------|--------|--------------|------|
| 独立持续体 | bfo:IndependentContinuant | cim:Equipment, cim:Space | 设备和空间实体 |
| 对象 | bfo:Object | cim:AirHandlingUnit, cim:Chiller | 具体设备个体 |
| 场所 | bfo:Site | cim:OperatingRoom, cim:ICU | 功能空间 |
| 质量 | bfo:Quality | cim:Temperature, cim:Pressure | 可测量属性 |
| 广义依赖持续体 | bfo:GenericallyDependentContinuant | cim:DesignDocument, cim:MaintenancePlan | 信息实体 |
| 过程 | bfo:Process | cim:HVACProcess, cim:MaintenanceActivity | 运行和维护过程 |
| 过程边界 | bfo:ProcessBoundary | cim:ProcessMilestone | 阶段转换节点 |
| 时间区域 | bfo:TemporalRegion | cim:OperationalPeriod | 运营时段 |

BFO 对齐的另一个重要价值体现在生命周期过程链的建模上。CIM 定义了 8 个生命周期阶段，每个阶段本身是一个发生体（Process），阶段之间的转换通过 ProcessBoundary（里程碑节点）标记：

```
ConceptualDesign → SchematicDesign → DetailedDesign → Tendering
       │                │                │              │
       ▼                ▼                ▼              ▼
   [概念设计       [方案设计       [施工图设计      [招标采购
    里程碑]         里程碑]         里程碑]         里程碑]

→ Construction → Commissioning → Operation → Decommissioning
       │              │              │              │
       ▼              ▼              ▼              ▼
   [施工完成      [调试验收      [投入运营      [退役拆除
    里程碑]        里程碑]        里程碑]        里程碑]
```

这个过程链确保了设计态信息（Layer 3）和运营态信息（Layer 4）在本体层面有清晰的时间边界。BIM/IFC 产生于 DetailedDesign 和 Construction 阶段，其语义范围终止于 Commissioning 里程碑；BAS 数据从 Commissioning 阶段开始产生，贯穿整个 Operation 阶段；CMMS 工单则主要属于 Operation 阶段。三源数据的时间归属在 BFO 过程框架中得到了严格的本体论定位。

### 2.3 ISO 19650 四层信息管理框架

ISO 19650（Organization and digitization of information about buildings and civil engineering works）是建筑信息管理的国际标准框架，由 ISO/TC 59/SC 13 制定，分为多个部分：ISO 19650-1:2018（概念和原则）、ISO 19650-2:2018（交付阶段信息管理）、ISO 19650-3:2020（运营阶段信息管理）等。ISO 19650 定义了交换信息需求（EIR）、BIM 执行计划（BEP）、资产信息模型（AIM）和项目信息模型（PIM，注意此处 PIM 为 ISO 19650 术语，与 MDA 的 PIM 含义不同）等核心概念，为建筑信息的组织和管理提供了框架性指导。

CIM 本体的五层结构（Layer 0~4）借鉴并扩展了 ISO 19650 的信息层级理念，建立了从基础范畴到运营数据的完整映射：

**表 2-2 CIM 五层本体与 ISO 19650 的映射**

| CIM 层 | 名称 | ISO 19650 对应 | 内容 | 类数 | 三元组 | 变更频率 |
|--------|------|---------------|------|------|--------|---------|
| Layer 0 | BFO 基础层 | 跨层级通用 | 持续体/发生体范畴、时间/空间基本概念 | 12 | ~180 | 极低 |
| Layer 1 | 概念层 | 信息需求 (OIR/EIR) | 介质、连接点、数据点、设备、空间、流动 6 大核心概念 | 45 | ~520 | 低 |
| Layer 2 | 参考层 | 标准分类库 | 12 部中/国际标准引用、Uniclass/OmniClass 分类、PDT (ISO 23386/23387) | 180 | ~1,800 | 低 |
| Layer 3 | 设计层 | PIM (项目信息模型) | 性能准则（GB 50333 硬编码值）、系统/设备规格、负荷计算 | 65 | ~780 | 项目级 |
| Layer 4 | 运营层 | AIM (资产信息模型) | 资产台账、SOSA/SSN 传感器、维护告警、控制策略、安全事件、FAS、CMMS | 95 | ~1,100 | 运营级 |

Layer 0~2 属于"标准级"资产，变更频率极低——BFO 的范畴框架和行业标准的分类体系在建筑的全生命周期内基本稳定。Layer 3~4 属于"项目级"和"运营级"资产，随项目推进和建筑运营而持续变化。这种稳定性分级对数据管理有直接影响：Layer 0~2 可以作为公共库在多个项目间共享复用，Layer 3~4 则需要按项目独立维护。在 Named Graph 架构中，这种分级体现为不同的缓存策略——TBox（Layer 0~2 为主）采用长期缓存，BAS 数据（Layer 4）采用短期缓存或不缓存。

ISO 19650 还强调了信息在交付（Delivery）阶段和运营（Operational）阶段的管理差异。CIM 的五层结构恰好对应了这种差异：Layer 3 的设计本体生成于交付阶段（设计院主导），Layer 4 的运营本体在运营阶段持续增长（物业管理方主导），而 Layer 0~2 的基础和参考本体则贯穿两个阶段，提供稳定的语义锚点。

ISO 19650-1:2018 中定义的四类信息需求在 CIM 中得到了具体化落地。组织信息需求（OIR）映射到 Layer 1 的核心概念框架——组织需要理解哪些领域概念才能管理建筑资产；资产信息需求（AIR）映射到 Layer 4 的运营本体——资产管理需要哪些运行数据和维护记录；交换信息需求（EIR）映射到 Layer 2 的参考分类和桥接本体——不同利益相关方之间交换信息需要哪些公共词汇；BIM 执行计划（BEP）中的模型元素定义映射到 Layer 3 的设计规格——项目各阶段应交付哪些信息粒度的模型。这种映射关系确保了 CIM 不是一个脱离工业实践的学术产物，而是对现有信息管理标准框架的本体工程实现。

从数据治理角度看，ISO 19650 的公共数据环境（CDE, Common Data Environment）概念在 CIM 架构中通过 Named Graph 实现了语义化的落地。传统 CDE 是文件级的共享空间（如 BIM 360、ProjectWise），而 CIM 的 9 个 Named Graph 构成了三元组级的语义 CDE——每个 Graph 具有明确的数据归属、更新策略和访问权限，信息的共享和隔离在语义粒度上实现，而非文件粒度。

### 2.4 多智能体协同建模方法论

545 个 OWL 类、15 个 TBox 文件、9 个 ABox 数据集——这一规模的本体工程如果由单一建模者完成，不仅效率低下，而且难以保证跨领域的一致性。本项目采用多智能体协同建模方法论，将建模任务分解为 9 个专业化智能体（Agent），每个 Agent 负责本体的一个子域，由 Agent-09 负责最终整合与验证。

**表 2-3 九智能体职责分工**

| Agent | 角色 | 责任域 | 输入上下文 | 输出产物 | 下游依赖 |
|-------|------|--------|-----------|---------|---------|
| Agent-01 | 系统拓扑建模师 | 建筑系统分类与拓扑 | Layer 1 介质/连接点, IFC 系统清单 | 系统拓扑图, 系统 ID 注册表 | Agent-04, 05 |
| Agent-02 | 空间本体建模师 | 空间层级与功能分类 | IFC 空间层级, GB 50333 | 空间层次树 (Building→Floor→Zone→Room) | Agent-05, 08 |
| Agent-03 | 设备本体建模师 | 设备分类与属性字典 | Layer 2 设备类, bridge_brick.ttl, IFC 设备清单 | 设备层次本体, 属性字典 | Agent-04, 05, 06, 07 |
| Agent-04 | 流动模型建模师 | 质量流、能量流、信息流 | Agent-01 拓扑 + Agent-03 设备 + Layer 1 流动类 | 三流路径模型 | Agent-05, 07 |
| Agent-05 | 系统-空间耦合建模师 | 设备与空间的关联 | Agent-01 拓扑 + Agent-02 空间 + Agent-03 设备 | 设备定位, 耦合矩阵 | Agent-06, 09 |
| Agent-06 | 控制系统建模师 | 传感器、执行器、控制回路 | Layer 4 控制策略, Agent-03 设备, BAS 读数 | 传感器定义, 控制回路 | Agent-07, 09 |
| Agent-07 | 计量系统建模师 | 能源计量与分摊 | Agent-04 流动 + Agent-06 传感器 | 计量层次, 分摊模型 | Agent-08, 09 |
| Agent-08 | 运维管理建模师 | 告警、工单、维保计划 | Agent-03 设备 + Agent-02 空间 + CMMS 工单 | 告警规则, 维保计划 | Agent-09 |
| Agent-09 | 模型整合验证师 | 全量整合与形式化验证 | **全部** Agent-01~08 输出 + 全量 TBox/ABox | 验证报告, 缺口矩阵, 修复建议 | 人工审计, MVP |

多智能体协同建模的核心设计原则是**上下文隔离（Context Isolation）**。每个 Agent 在执行建模任务时，只加载与其职责相关的本体子集和实例数据，而非全量 545 类。上下文工程的实测数据表明，各 Agent 的上下文需求占全量本体的比例存在显著差异：

- Agent-01（系统拓扑）需要约 60 个类（11% 的全量），主要来自 Layer 1 的介质和连接点定义
- Agent-03（设备本体）需要约 120 个类（22%），主要来自 Layer 2 的设备参考类
- Agent-06（控制系统）需要约 80 个类（16%），主要来自 Layer 4 的控制策略定义
- Agent-09（整合验证）是唯一需要全量 545 类的 Agent

上下文隔离不仅提高了建模效率（减少无关信息的干扰），更重要的是确保了领域责任的清晰划分。Agent-06（控制系统）不需要理解 CMMS 工单模型，Agent-08（运维管理）不需要理解 223P 连接点语义——每个 Agent 在其能力范围内产出高质量的子域本体，最终由 Agent-09 进行跨域验证和整合。

Agent 之间的协作关系并非全连接，而是一个有向无环图（DAG）：

```
    Agent-01 (拓扑) ──────────────┐
         │                        │
    Agent-02 (空间) ────┐          │
         │              │          │
    Agent-03 (设备) ────┤          │
         │              │          │
         ▼              ▼          ▼
    Agent-04 (流动)  Agent-05 (耦合)
         │              │
         ▼              ▼
    Agent-06 (控制) ◄───┘
         │
         ▼
    Agent-07 (计量)
         │
         ▼
    Agent-08 (运维)
         │
         ▼
    Agent-09 (整合) ◄── 汇聚全部 Agent 输出
```

Agent-01、02、03 可以并行执行（三者无相互依赖），Agent-04 和 05 依赖前三者的输出，Agent-06、07、08 按序依赖，Agent-09 汇聚全部输出。这种拓扑结构意味着建模流水线的关键路径长度为 6（01→04→05→06→07→08→09），而非 9（全串行），理论上可将端到端建模时间缩短约 33%。

多智能体方法论的另一项实践洞察是**上下文传递协议**的选择。项目实践了三种协议模式：文件传递（Agent 输出写入 project_deliverables/ 目录，下游 Agent 从同一路径读取，简单但无子集裁剪）、SPARQL 传递（Agent 输出加载到 Named Graph，下游 Agent 通过 SPARQL 按需检索所需子集，token 高效但需要端点运行）以及混合传递（TBox 用文件传递因变化少可缓存，ABox 用 SPARQL 检索因变化多需按需获取）。实测结果表明，混合传递模式在 token 利用率方面最优：SPARQL 按需检索相比全量文件加载可节省 99% 的 token 消耗，而 TBox 的文件传递避免了为低变化频率数据维护实时 SPARQL 端点的开销。

### 2.5 社会技术系统理论与安防应用

社会技术系统理论（Socio-Technical Systems Theory）最早由 Trist 和 Bamforth 于 1951 年在对英国煤矿的研究中提出，其核心观点是：一个有效的工作系统不能仅从技术子系统或社会子系统单独理解，而必须作为技术要素与社会要素的联合优化来设计。这一理论在信息系统设计、人机交互和组织管理等领域得到了广泛应用。

将社会技术系统理论引入医疗建筑安防领域，源于一个深刻的实践观察：消防应急响应的成败不取决于技术系统（探测器、联动控制）的性能指标，而取决于技术系统与社会系统（人员角色、职责分工、决策流程）的协调程度。一套技术上完美的 FAS 系统，如果值班人员不清楚收到报警后应该通知谁、谁负责决策、谁负责执行，那么技术系统的响应速度优势将被社会系统的混乱完全抵消。

CIM 安全 MVP（L2 级电气火灾响应）将社会技术系统理论具体化为三个要素层：

**技术要素**：62 个 FAS 探测器（烟感/温感/手报/可燃气体）构成感知层，BAS/DDC 控制器执行 4 条联动指令（风阀关闭、排烟启动、非消防电源切断、广播疏散），事件引擎实现 5 状态自动机（IDLE → DETECTED → CONFIRMED → RESPONDING → RESOLVED），全部技术要素在 CIM 本体中建模为 Layer 4 的 SecurityEvent 类层次（26 个类）。

**社会要素**：7 个人员角色构成响应组织体系——监控中心值班员（首响）、安保队长（现场指挥）、电工（电气系统操作）、护士长（患者疏散）、科室主管（业务决策）、医院值班领导（最终决策）以及 119 联络员（外部资源协调）。每个角色有明确的触发条件、响应时限和交接协议。CIM 本体将这些角色建模为 SocioTechnical 子类，与事件状态机和动作链（ActionChain）形成关联。

**环境要素**：物理空间（5F 电气竖井、配电间）、时间窗口（L2 级事件响应时限 15 分钟）和环境条件（烟雾浓度、温度变化率）构成响应的边界约束。CIM 本体通过 Layer 4 的 FAS 模块（12 个类）将物理空间拓扑与探测器布置关联，通过 Layer 1 的空间层级将事件定位到具体的防火分区。

社会技术系统建模的关键创新在于：传统 FAS 系统只建模技术要素（探测器状态 → 联动动作），CIM 则将社会要素纳入本体，使得 SPARQL 查询不仅能回答"哪个探测器报警了"，还能回答"应该通知谁""该角色的响应时限是多少""当前事件状态下哪些动作已完成、哪些待执行"。这种扩展将传统的设备监控提升为完整的应急响应管理。

MVP 的独立仿真验证提供了量化证据：10/10 动作节点在规定顺序内完成执行，总耗时 840 秒（在 L2 级 900 秒时限内），4 条 BAS 联动指令全部成功下发，5 个状态转换（IDLE → DETECTED → CONFIRMED → RESPONDING → RESOLVED）无异常中断。仿真还验证了 4 个物理场景的守恒方程（手术部洁净空气质量守恒、冷站冷水能量守恒、病房温湿度照明综合守恒、烟感联动时序守恒），全部以 CRITICAL = 0 通过。这些结果表明，CIM 的社会技术系统建模不仅在理论上合理，在工程实践中也具有可操作性和可验证性。

---

## 第三章 CIM 本体架构

### 3.1 总体架构

CIM 本体采用"五层 + 六桥接"的架构，将 545 个 OWL 类组织为从基础范畴到运营应用的完整层级体系，同时通过 6 个独立的桥接本体实现与外部标准的语义对齐。这一架构的设计目标是：在纵向上实现从抽象概念到具体应用的渐进细化，在横向上实现与行业标准生态的开放互联。

```
                    ┌─────────────────────────────┐
                    │     Layer 4: 运营与扩展      │ 95 类
                    │  资产/控制/安全/FAS/CMMS     │ ~1,100 三元组
                    ├─────────────────────────────┤
                    │     Layer 3: 设计本体        │ 65 类
                    │  性能准则/规格/负荷          │ ~780 三元组
                    ├─────────────────────────────┤
                    │     Layer 2: 参考本体        │ 180 类
                    │  标准分类/PDT/参考数据       │ ~1,800 三元组
                    ├─────────────────────────────┤
                    │     Layer 1: 概念本体        │ 45 类
                    │  介质/连接点/数据点/         │ ~520 三元组
                    │  设备/空间/流动              │
                    ├─────────────────────────────┤
                    │     Layer 0: BFO 基础层      │ 12 类
                    │  Continuant / Occurrent     │ ~180 三元组
                    └──────────────┬──────────────┘
                                   │
          ┌────────┬───────┬───────┼───────┬────────┬─────────┐
          │        │       │       │       │        │         │
     ┌────▼───┐┌───▼──┐┌──▼──┐┌───▼──┐┌───▼───┐┌───▼────┐   │
     │ Brick  ││ 223P ││ IFC ││ FSO  ││BACnet ││ISO14224│   │
     │ 1.3    ││      ││ 4   ││      ││       ││       │   │
     │ 28 cls ││22 cls││35cls││15 cls││18 cls ││12 cls │   │
     └────────┘└──────┘└─────┘└──────┘└───────┘└───────┘   │
          6 桥接本体 (独立文件, 不修改外部标准)                 │
```

整个 TBox（术语层）由 15 个 TTL 文件组成，总计 5,395 个三元组和 545 个类定义。类的分布呈现明显的"中间层丰富"特征：Layer 2 参考本体以 180 个类占据最大比例（33%），这反映了五大机电系统设备分类的丰富性；Layer 4 运营层以 95 个类位居第二（17%），体现了运营场景的复杂性和多样性；Layer 3 设计层（65 类）和 Layer 1 概念层（45 类）分别提供设计参数框架和核心概念骨架；Layer 0 以 12 个基础类支撑整个体系的范畴一致性。6 个桥接本体合计 130 个类定义（部分为对齐声明），占总量的约 24%。

**表 3-1 TBox 文件清单与统计**

| 文件名 | 所属层 | 类数 | 三元组 | 用途 |
|--------|--------|------|--------|------|
| layer0_bfo.ttl | Layer 0 | 12 | ~180 | BFO 基础范畴映射 |
| layer1_concept.ttl | Layer 1 | 45 | ~520 | 六大核心概念定义 |
| layer2_reference.ttl | Layer 2 | 180 | ~1,800 | 五大系统设备参考类 |
| layer3_design.ttl | Layer 3 | 65 | ~780 | 设计参数与性能准则 |
| layer4_operation.ttl | Layer 4 | 95 | ~1,100 | 运营、控制、安全、FAS、CMMS |
| bridge_brick.ttl | 桥接 | 28 | ~160 | Brick 1.3 对齐 |
| bridge_223p.ttl | 桥接 | 22 | ~140 | ASHRAE 223P 对齐 |
| bridge_ifc.ttl | 桥接 | 35 | ~200 | IFC4 对齐 |
| bridge_fso.ttl | 桥接 | 15 | ~90 | FSO 消防对齐 |
| bridge_bacnet.ttl | 桥接 | 18 | ~110 | BACnet 点位对齐 |
| bridge_iso14224.ttl | 桥接 | 12 | ~75 | ISO 14224 故障模式对齐 |
| ontology_skeleton.ttl | 索引 | -- | ~120 | 命名空间声明 + owl:imports |
| _index_v4.ttl | 索引 | -- | ~80 | 模块化导入链 |
| equipment/mechanical.ttl | Layer 2 | ~60 | -- | HVAC 设备层次细化 |
| equipment/electrical.ttl | Layer 2 | ~58 | -- | 电气设备层次细化 |

### 3.2 Layer 0：基础本体（BFO 2020 对齐）

Layer 0 是整个 CIM 本体的哲学基础，包含 12 个从 BFO 2020 映射而来的顶层类，约 180 个三元组。这一层不直接定义任何医疗建筑领域概念，而是提供范畴框架，确保上层各层定义的类在本体论层面具有一致性。

Layer 0 的核心创新是生命周期过程链（Lifecycle Process Chain）。传统建筑本体（Brick、IFC）几乎不涉及生命周期建模——它们要么描述设计态的静态结构（IFC），要么描述运行态的动态数据（Brick/BAS）。CIM 通过 BFO 的 Process 范畴，将建筑的完整生命周期建模为一个过程序列：

```
cim:LifecycleProcess (bfo:Process 的子类)
    │
    ├── cim:ConceptualDesignPhase     概念设计阶段
    ├── cim:SchematicDesignPhase      方案设计阶段
    ├── cim:DetailedDesignPhase       施工图设计阶段
    ├── cim:TenderingPhase            招标采购阶段
    ├── cim:ConstructionPhase         施工建造阶段
    ├── cim:CommissioningPhase        调试验收阶段
    ├── cim:OperationPhase            运营使用阶段
    └── cim:DecommissioningPhase      退役拆除阶段
```

每两个相邻阶段之间由 ProcessBoundary（过程边界，BFO 中的时间瞬间实体）标记里程碑节点。这些里程碑不是抽象的管理概念，而是信息状态的切换点：竣工验收（Commissioning 里程碑）意味着 IFC 模型冻结，BAS 系统开始产生运行数据；投入运营（Operation 里程碑）意味着 CMMS 系统开始记录维保工单。三源数据的产生时间和语义范围在过程链中得到了精确的本体定位。

另一个 Layer 0 层面的重要区分是流动路径（FlowPath）与流动过程（FlowProcess）。FlowPath 是持续体——冷冻水从冷机到末端的管路连接关系在建筑使用期内基本恒定。FlowProcess 是发生体——冷冻水的实际流动有开始和结束时间，其流量、温度等参数在不断变化。设计文档描述的是 FlowPath（这条管路连接哪些设备），BAS 监测的是 FlowProcess（管路中的水此刻流速多少、温度多少）。这一区分避免了将设计参数（设计流量 180 m3/h）和运行参数（当前流量 165 m3/h）混为一谈——前者是 FlowPath 的属性（持续体的描述性属性），后者是 FlowProcess 的观测值（发生体的时序数据）。

### 3.3 Layer 1：概念本体

Layer 1 是 CIM 本体的概念核心，包含约 45 个类和 520 个三元组，定义了六大核心概念域。这些概念构成了上层各层（Layer 2~4）的语义骨架——Layer 2 的 180 个设备参考类都是 Layer 1 设备概念的细化，Layer 4 的 95 个运营类都是 Layer 1 概念在运营场景中的扩展。

**介质层级（Medium Hierarchy）**。CIM 定义了 30 余个介质类，涵盖医疗建筑五大系统中流动的所有物质和能量。这一层级与 ASHRAE 223P 的 Medium 概念直接对齐，但增加了 223P 未覆盖的医用气体介质。介质类的层级关系如下：

```
cim:Medium
    ├── cim:FluidMedium
    │   ├── cim:Water
    │   │   ├── cim:ChilledWater          冷冻水
    │   │   ├── cim:HotWater              热水
    │   │   ├── cim:CondenserWater        冷却水
    │   │   └── cim:DomesticWater         生活给水
    │   └── cim:Air
    │       ├── cim:SupplyAir             送风
    │       ├── cim:ReturnAir             回风
    │       ├── cim:OutdoorAir            新风
    │       └── cim:ExhaustAir            排风
    ├── cim:GasMedium
    │   ├── cim:Oxygen                    医用氧气 (O2)
    │   ├── cim:MedicalVacuum             医用负压 (VAC)
    │   ├── cim:MedicalCompressedAir      医用压缩空气 (CAIR)
    │   └── cim:NitrousOxide              氧化亚氮 (N2O)
    └── cim:EnergyMedium
        ├── cim:ElectricalPower           电力
        │   ├── cim:NormalPower           常规电源
        │   ├── cim:EmergencyPower        应急电源
        │   └── cim:ITIsolatedPower       IT 隔离电源
        └── cim:ThermalEnergy             热能
```

医用气体（GasMedium）和 IT 隔离电源（ITIsolatedPower）是 CIM 相对于 Brick 和 223P 的原创扩展，直接源自 WS 435 和 IEC 60364-710 的医疗建筑强制要求。

**连接点模型（ConnectionPoint Model）**。CIM 的连接点与 ASHRAE 223P 的 ConnectionPoint 概念完全对齐，定义了设备之间物理连接的标准化描述方式。每个连接点具有方向性（Inlet / Outlet / Bidirectional）和关联介质类型，使得系统拓扑可以被形式化地查询和推理。例如，一台空调箱（AHU）拥有冷冻水入口连接点（ChilledWater Inlet）、冷冻水出口连接点（ChilledWater Outlet）、送风出口连接点（SupplyAir Outlet）和回风入口连接点（ReturnAir Inlet），通过连接点之间的 connectedTo 关系构建完整的系统拓扑。

**数据点层级（DataPoint Hierarchy）**。CIM 的数据点概念与 Brick Schema 的 Point 类直接对齐，用于描述传感器读数、设定值和控制状态。DataPoint 是 BAS/BACnet 数据接入 CIM 知识图谱的语义桥梁——一个 BACnet 模拟量输入 AI:1 通过 cim-bacnet:bacnetPointOf 关系关联到 CIM 设备实体，同时声明其 pointType（如 cim:TemperatureSensor）和 hasUnit（如 qudt:DegreeCelsius），从而为原本语义匮乏的 BACnet 点位赋予完整的上下文信息。数据点层级的子类覆盖了医疗建筑中常见的全部传感器类型：TemperatureSensor、HumiditySensor、PressureSensor、FlowSensor、CO2Sensor、PowerSensor、DifferentialPressureSensor（洁净室压差监测专用）以及 ParticleCountSensor（洁净度监测专用）。后两种传感器类型是 CIM 相对于 Brick 的医疗场景扩展——Brick 没有定义洁净度相关的传感器类。

**流动模型（Flow Model）**。CIM 定义了 31 个流动相关的类，涵盖质量流（MassFlow）、能量流（EnergyFlow）和信息流（InformationFlow）三大类别。质量流描述水、空气和气体在管路中的物理运动；能量流描述冷热能量和电力在系统中的传递；信息流描述控制信号和传感器数据在 BAS 网络中的传输。三流模型使得 SPARQL 查询能够追踪从冷机到末端的完整能量传递路径，或从传感器到控制器的信息反馈回路。

### 3.4 Layer 2：参考本体

Layer 2 是 CIM 本体中类定义最为密集的层级，包含约 180 个类和 1,800 个三元组。这一层的核心功能是提供五大机电系统的设备分类参考库和标准规范引用。

**设备分类体系**。Layer 2 定义了覆盖五大系统的 94 个设备类，形成层次化的分类树：

```
cim:Equipment (Layer 1 概念类)
    │
    ├── cim:HVACEquipment                     暖通设备
    │   ├── cim:AirHandlingUnit               空调箱 (AHU)
    │   ├── cim:Chiller                       冷水机组
    │   ├── cim:CoolingTower                  冷却塔
    │   ├── cim:Boiler                        锅炉
    │   ├── cim:HeatExchanger                 换热器
    │   ├── cim:Fan                           风机
    │   ├── cim:Pump                          水泵
    │   ├── cim:VAVBox                        变风量末端 (VAV)
    │   └── cim:FCU                           风机盘管 (FCU)
    │
    ├── cim:ElectricalEquipment               电气设备
    │   ├── cim:Transformer                   变压器
    │   ├── cim:Switchgear                    开关柜
    │   ├── cim:DistributionPanel             配电柜
    │   ├── cim:UPS                           不间断电源
    │   ├── cim:EmergencyGenerator            应急发电机
    │   └── cim:ATS                           自动转换开关
    │
    ├── cim:MedicalGasEquipment               医用气体设备
    │   ├── cim:OxygenManifold                氧气汇流排
    │   ├── cim:VacuumPump                    医用真空泵
    │   ├── cim:MedicalAirCompressor          医用空压机
    │   └── cim:N2OManifold                   N2O 汇流排
    │
    ├── cim:FireProtectionEquipment           消防设备
    │   ├── cim:FirePump                      消防泵
    │   ├── cim:SprinklerHead                 喷头
    │   ├── cim:FireAlarmPanel                火灾报警控制器
    │   └── cim:SmokeDetector                 烟感探测器
    │
    └── cim:LightingEquipment                 照明设备
        ├── cim:EmergencyLighting             应急照明
        └── cim:SurgicalLight                 手术无影灯
```

**空间分类体系**。CIM 定义了 47 个空间类，远超 Brick 和 IFC 对医疗功能空间的覆盖：

```
cim:Space (Layer 1 概念类)
    │
    ├── cim:Building                          建筑
    ├── cim:Floor                             楼层
    ├── cim:Zone                              功能区域
    │   ├── cim:CleanZone                     洁净区
    │   ├── cim:FireCompartment               防火分区
    │   └── cim:MedicalGasZone                医气供应区
    │
    └── cim:Room                              房间
        ├── cim:OperatingRoom                 手术室
        │   ├── cim:ClassI_OR                 I 级洁净手术室
        │   └── cim:ClassIII_OR              III 级洁净手术室
        ├── cim:ICU                           重症监护室
        │   ├── cim:NegativePressureICU       负压隔离 ICU
        │   └── cim:NeonatalICU               新生儿 ICU
        ├── cim:WardRoom                      病房
        ├── cim:ExamRoom                      诊室
        ├── cim:PharmacyRoom                  药房
        ├── cim:LaboratoryRoom                检验科
        ├── cim:BloodBankRoom                 血库
        └── cim:MechanicalRoom                机房
```

**标准规范库**。Layer 2 引用了 12 部中国和国际标准作为参考数据源：

**表 3-2 CIM 引用标准清单**

| 标准编号 | 名称 | CIM 中的用途 |
|---------|------|-------------|
| ISO 19650-1:2018 | 建筑信息管理 | 五层本体架构指导 |
| ISO 16739-1:2018 (IFC4) | 建筑信息模型 | BIM 数据桥接 |
| ISO 14224:2016 | 石油/天然气设备可靠性数据 | 故障模式分类 |
| ISO 23386/23387 | 产品数据模板 | PDT 属性定义 |
| ASHRAE 135-2020 | BACnet 协议 | BAS 数据桥接 |
| ASHRAE 223P | HVAC 语义模型 | 连接点/介质对齐 |
| GB 50333-2013 | 医院洁净手术部 | 洁净度/换气/压差参数 |
| WS 435-2013 | 医用气体工程 | 医气终端/管路/安全 |
| IEC 60364-710 | 医疗场所电气安装 | IT 隔离电源/接地 |
| GB 50016-2014 | 建筑设计防火规范 | 防火分区/疏散 |
| Uniclass 2015 | 建筑分类体系 | 通用分类编码 |
| OmniClass | 建筑信息分类 | 补充分类编码 |

Layer 2 还引入了产品数据模板（Product Data Template, PDT）框架，遵循 ISO 23386 和 ISO 23387 标准。PDT 为每类设备定义标准化的属性集合（如冷水机组的 PDT 包含额定冷量、额定功率、COP、制冷剂类型等属性），确保不同来源的设备数据可以在统一的属性框架下比较和分析。

### 3.5 Layer 3：设计本体（PIM 阶段）

Layer 3 包含约 65 个类和 780 个三元组，专注于设计阶段的性能准则和技术规格。这一层是 ISO 19650 中"项目信息模型（PIM）"概念在 CIM 中的实现，其内容随项目而变化（不同医院的设计参数不同），但结构（类和属性的定义）是稳定的。

Layer 3 的核心特征是**硬编码的标准参数值**。以洁净手术室为例，GB 50333-2013 规定的强制参数直接作为本体中的约束条件：

```
cim:ClassI_OR (I 级洁净手术室)
    cim:minAirChangeRate         "36"^^xsd:integer    # 最低换气次数 (ACH)
    cim:minPressureDifference    "8"^^xsd:decimal     # 最低正压差 (Pa)
    cim:temperatureRange         "21-25"              # 温度范围 (°C)
    cim:humidityRange            "30-60"              # 湿度范围 (%RH)
    cim:cleanlinessClass         "ISO 5"              # 洁净度等级
    cim:regulatoryReference      "GB50333-2013 §4.0.1"

cim:ClassIII_OR (III 级洁净手术室)
    cim:minAirChangeRate         "20"^^xsd:integer
    cim:minPressureDifference    "5"^^xsd:decimal
    cim:temperatureRange         "21-25"
    cim:cleanlinessClass         "ISO 7"
```

这些硬编码值使得 SPARQL 查询可以直接比较设计标准与实际运行数据。例如，能耗异常检测模式（Pattern 3）通过比较 Layer 3 设计参数（graph/pset）与 Layer 4 BAS 实时读数（graph/bas/t0），自动识别偏离设计值超过 20% 的设备。这种跨层级的比较在传统系统中需要人工逐台核对，而在 CIM 架构中仅需一条 SPARQL 联邦查询。

Layer 3 还定义了 HVAC、电气、医用气体和给排水四大系统的设计规格框架，包括系统负荷计算的输入参数（室内设计参数、围护结构热工参数、人员密度、设备散热量等）和设备选型的约束条件（冷机 COP 下限、水泵扬程范围、风管风速上限等）。

Layer 3 在 CIM 架构中扮演着"设计基线（Design Baseline）"的角色。一旦建筑竣工投入运营，Layer 3 的设计参数就成为运营数据的参照标准。当 BAS 传感器报告某台 AHU 的实际送风温度为 28.5 度，而 Layer 3 记录的设计送风温度范围为 14~16 度（夏季工况），系统可以自动判定该设备运行异常。这种设计态与运行态的自动比较是 CIM 数据联邦的核心应用场景之一——在传统系统中，设计参数存储在纸质或 PDF 格式的设计文件中，运行参数存储在 BAS 数据库中，两者之间没有可查询的形式化关联。CIM 的 Layer 3 将设计参数形式化为 RDF 三元组，与 Layer 4 的 BAS 数据同处于 SPARQL 可查询的知识图谱中，使跨阶段比较成为标准的联邦查询操作。

### 3.6 Layer 4：运营与扩展本体

Layer 4 是 CIM 本体中最为丰富且语义最密集的层级，包含约 95 个类和 1,100 个三元组，覆盖建筑运营阶段的五个子模块。这一层对应 ISO 19650-3 定义的资产信息模型（AIM），是 BAS 和 CMMS 数据接入 CIM 知识图谱的语义入口。

**运营子模块（Operational, ~38 个类）**。这一子模块定义了资产台账管理、传感器观测和告警管理的核心概念。资产台账（Asset Register）将设备实体从 Layer 2 的"类定义"扩展为 Layer 4 的"资产个体"，附加安装日期、保修期、运行工时和折旧状态等运营属性。传感器建模采用 W3C SOSA/SSN（Sensor, Observation, Sample, and Actuator）本体的核心模式，每个传感器观测（Observation）关联一个观测属性（ObservableProperty）、一个时间戳和一个结果值，确保 BAS 时序数据在知识图谱中具有标准化的语义描述。告警管理定义了告警等级（INFO / WARNING / CRITICAL / EMERGENCY）、告警状态（ACTIVE / ACKNOWLEDGED / CLEARED）和告警-设备关联规则。

**控制策略子模块（Control Strategies, ~37 个类）**。这一子模块是 CIM 对传统建筑本体的重要扩展。它定义了 DDC 控制器、控制回路和 PID 参数的完整建模框架。项目共定义了 27 条控制回路，涵盖 HVAC 系统的典型控制场景（送风温度控制、静压控制、冷冻水温度控制、末端风量控制等）。每条控制回路由传感器（Sensor）、控制器（Controller）、执行器（Actuator）和设定值（Setpoint）四要素组成，通过 hasInput / hasOutput / hasSetpoint 关系在本体中形式化表达。PID 控制参数（比例增益 Kp、积分时间 Ti、微分时间 Td）作为控制回路的属性记录，使得控制策略的优化和审计可以基于知识图谱进行。

**安全事件子模块（Security Event, 26 个类）**。这一子模块为安全 MVP 提供本体基础，定义了事件状态机、应急预案和动作链三个核心概念。事件状态机将安全事件的完整生命周期建模为 5 个状态（IDLE → DETECTED → CONFIRMED → RESPONDING → RESOLVED），每个状态转换有明确的触发条件和超时约束。应急预案（EmergencyPlan）按事件类型和严重等级匹配，关联一系列有序的动作节点（ActionNode）。动作链（ActionChain）定义了动作节点的执行顺序、每个动作的负责角色、超时时限和完成条件。26 个类的设计确保了从探测到闭环的全过程可追踪、可审计。

**FAS 子模块（Fire Alarm System, 12 个类）**。这一子模块定义了消防自动报警系统的设备分类和拓扑关系。探测器细分为烟感探测器（SmokeDetector）、温感探测器（HeatDetector）、火焰探测器（FlameDetector）、可燃气体探测器（GasDetector）和手动报警按钮（ManualCallPoint）五种类型。火灾报警控制器（FACU）与探测器之间通过报警回路（AlarmLoop）和防火分区（FireZone）关联。FAS 子模块与 Layer 1 空间层级的关联使得 SPARQL 查询可以按楼层、功能区或防火分区检索探测器状态——项目实测中，Q4 验证查询成功返回 62 条 FAS 探测器与空间位置的关联记录。

**CMMS 子模块（Computerized Maintenance Management System, 13 个类）**。这一子模块定义了维保工单的全生命周期模型，与 ISO 14224:2016 的故障模式分类对齐。工单类型分为预防性维护（PreventiveWorkOrder, PM）、纪正性维修（CorrectiveWorkOrder, CM）和检查（InspectionWorkOrder）。每条工单关联目标设备（maintenanceTarget）、计划日期（scheduledDate）、优先级（priority）和完成状态（woStatus）。项目 ABox 中包含 735 条工单记录（669 条 PM + 64 条 CM + 2 条 Inspection），覆盖了全部设备类型的维保场景。工单与 BAS 报警的跨源关联（CMMS 工单 → CIM 设备 → BAS 告警点位）是三源联邦验证的关键链路。

### 3.7 桥接本体

CIM 的六个桥接本体是实现标准互操作的关键机制。每个桥接本体是独立的 TTL 文件，不修改外部标准的原始定义，而是通过 OWL 语义关系（owl:equivalentClass、rdfs:subClassOf）和自定义属性建立 CIM 概念与外部标准概念之间的对齐。

**Brick 1.3 桥接**（bridge_brick.ttl, 28 个类）。这是对齐关系最密集的桥接，使用约 60 条 owl:equivalentClass 声明将 CIM 设备类和传感器类与 Brick 的对应概念等价。例如，`cim:AirHandlingUnit owl:equivalentClass brick:AHU`，`cim:TemperatureSensor owl:equivalentClass brick:Temperature_Sensor`。Brick 桥接确保了 CIM 知识图谱中的设备和传感器可以被 Brick 兼容的推理引擎识别和查询。实测验证中，12/12 个 Brick 设备类在 CIM 中实现了 100% 的覆盖。

**ASHRAE 223P 桥接**（bridge_223p.ttl, 22 个类）。这一桥接聚焦于介质（Medium）和连接点（ConnectionPoint）两个概念域。CIM 的介质层级体系（30+ 类）是在 223P Medium 概念的基础上扩展而来，增加了医用气体和电力介质。连接点模型（Inlet / Outlet / Bidirectional）与 223P 完全兼容，使得 CIM 可以复用 223P 的 HVAC 拓扑推理能力。

**IFC4 桥接**（bridge_ifc.ttl, 35 个类）。IFC 桥接处理的核心问题是 BIM 几何模型与 CIM 语义模型之间的映射。IfcSpace 映射到 cim:Space，IfcSystem 映射到 cim:System，IfcDistributionElement 的子类映射到 cim:Equipment 的对应子类。每个 CIM 设备实例通过 cim:ifcGlobalId 属性保留其 IFC 原始 GlobalId，确保从 CIM 知识图谱可以回溯到 BIM 几何模型。IFC 桥接还处理了 IFC 属性集（PropertySet/Pset）到 CIM 设计参数（Layer 3）的转换。

**FSO 桥接**（bridge_fso.ttl, 15 个类）。Fire Safety Ontology 桥接采用 rdfs:subClassOf 关系，将 CIM 的消防设备类（SmokeDetector、HeatDetector 等）声明为 FSO 基础类的子类。桥接还定义了 35 个设备映射和 17 个属性映射，并提供双向 SPARQL 查询模板，确保 FSO 兼容的消防分析工具可以查询 CIM 知识图谱中的消防数据。

**BACnet 桥接**（bridge_bacnet.ttl, 18 个类）。这是连接 CIM 与 BAS 实时数据的核心桥接。它定义了 9 种 BACnet 对象类型（Analog Input / Analog Output / Binary Input / Binary Output / Analog Value / Multi-State Value 等）在 CIM 中的表示，以及关键的 cim-bacnet:bacnetPointOf 关系——这个属性将一个 BACnet 数据点关联到其所属的 CIM 设备实体。项目的 BACnet 仿真器基于 11 种设备点位模板生成了 1,055 个 BACnet 点位实例，全部通过 bacnetPointOf 链接到 CIM 设备。

**ISO 14224 桥接**（bridge_iso14224.ttl, 12 个类）。这一桥接服务于 CMMS 子模块，将 ISO 14224 的故障模式分类（FailureMode）和故障原因分类（FailureCause）引入 CIM。通过 cim-cmms:failureMode 属性，每条纠正性维修工单（CM）可以关联到标准化的故障分类编码，支持跨项目的设备可靠性分析和故障模式统计。

六个桥接本体合计约 775 个三元组。它们的独立文件设计确保了可组合性——如果某个项目不需要消防语义，可以不加载 bridge_fso.ttl，而不影响其他桥接的功能。桥接本体的存在使 CIM 不是一个"替代一切"的封闭标准，而是一个"桥接一切"的开放框架。

**表 3-3 桥接本体对齐方法汇总**

| 桥接本体 | 外部标准 | 主要对齐方法 | 对齐声明数 | 关键对齐示例 |
|---------|---------|-------------|-----------|-------------|
| bridge_brick.ttl | Brick 1.3 | owl:equivalentClass | ~60 | cim:AHU = brick:AHU |
| bridge_223p.ttl | ASHRAE 223P | owl:equivalentClass + 属性映射 | ~30 | cim:ConnectionPoint ≈ s223:ConnectionPoint |
| bridge_ifc.ttl | IFC4 | owl:equivalentClass + cim:ifcGlobalId | ~35 | cim:Equipment → ifc:IfcBuildingElement |
| bridge_fso.ttl | FSO | rdfs:subClassOf + SPARQL 双向 | 35 设备 + 17 属性 | cim:SmokeDetector ⊂ fso:Detector |
| bridge_bacnet.ttl | BACnet | cim-bacnet:bacnetPointOf | 9 对象类型 | AI/AO/BI/BO/AV/MSV/ACC/CAL/SCHED |
| bridge_iso14224.ttl | ISO 14224 | cim-cmms:failureMode | ~12 | 故障模式分类编码对齐 |

桥接本体的设计遵循"最小侵入原则"：不修改外部标准的原始定义，仅在 CIM 命名空间内声明对齐关系。这确保了当外部标准更新版本时（如 Brick 从 1.3 升级到 1.4），只需更新对应的桥接文件，而不影响 CIM 本体的其余部分。

---

## 第四章 数据联邦与知识图谱

### 4.1 IFC→CIM 实例化管线

CIM 本体的 TBox（术语层）定义了"词典"——545 个类和它们之间的关系。但本体的价值最终需要通过 ABox（断言层）的实例化来实现。本项目以宁波大学附属医院（NBU Medical Clinic）的真实 IFC 模型为数据源，建立了从 IFC 到 CIM 的五步实例化管线。

**第一步：IFC 实体盘点（Inventory）。** 从 6 个 IFC 文件（总计 3.85M 实体）中提取全部 MEP 设备实体，按 IfcDistributionElement 子类进行分类统计。盘点结果确认了 12 种核心设备类型的实体数量：AHU 12 台、Chiller 4 台、CoolingTower 4 台、Boiler 2 台、Pump 28 台、Fan 16 台、VAV 24 台、FCU 48 台、Transformer 6 台、UPS 4 台、EmergencyGenerator 2 台、SmokeDetector 62 台。

**第二步：CIM 类映射（Mapping）。** 将 IFC 实体类型映射到 CIM 类定义。映射关系通过 bridge_ifc.ttl 和 bridge_brick.ttl 两个桥接本体定义，确保每个 IFC 设备实体在 CIM 中有唯一的类归属。12 种 Brick Schema 基础设备类全部在 CIM 中找到了对应的等价类，覆盖率 100%。

**第三步：SHACL 验证（Validation）。** 使用 pyshacl 验证引擎对生成的 CIM 实例进行形式化验证。SHACL 约束定义在 rules/shacl_constraints.ttl 中，包括四项核心验证：设备必须有 cim:locatedIn 空间关联、传感器必须有 cim:hasUnit 单位声明、工单必须有 cim-cmms:maintenanceTarget 目标设备、安全事件必须有 cim:eventSeverity 等级。验证结果为 VIOLATION = 0, WARNING = 0，全部通过。

**第四步：LOD 比较（LOD Comparison）。** 对比 IFC 模型的 LOD（Level of Development）与 CIM 实例的信息丰度。IFC 模型在几何层面达到 LOD 300~400，但在语义层面仅相当于 LOD 200（缺少运行参数和控制逻辑）。CIM 实例通过 BAS 和 CMMS 数据的注入，在语义层面达到了等效 LOD 400~500 的信息丰度。

**第五步：报告生成（Report）。** 自动生成实例化报告，记录映射统计、验证结果和覆盖率指标。

五步管线的整体数据流如下图所示：

```
IFC 文件 (6个, 3.85M 实体)
    │
    ▼ Step 1: 盘点
MEP 设备实体提取 (12 类, 212 台)
    │
    ▼ Step 2: 映射
CIM 类归属 (bridge_ifc.ttl + bridge_brick.ttl)
    │
    ▼ Step 3: 验证
SHACL 约束检查 (pyshacl, 4 文件) ──→ VIOLATION = 0
    │
    ▼ Step 4: LOD 比较
IFC LOD 300-400 (几何) → CIM LOD 400-500 (语义)
    │
    ▼ Step 5: 报告
实例化报告 + global_id_registry.yaml
    │
    ▼ 输出
~1,210 CIM 实体 → graph/ifc Named Graph (~12,000 三元组)
```

通过五步管线，项目共生成约 1,210 个 CIM 实体实例（包括约 800 个 IFC 来源的设备实例和约 410 个 BAS/CMMS/FAS 来源的补充实例）。全部实例遵循 CIM 的 ID 治理规范，采用 {TYPE}-{MODEL}-{N} 格式命名（如 CHL-19XR-001 表示 19XR 型冷水机组第 1 台，SD-FST-851-001 表示 FST-851 型烟感探测器第 1 号）。每个实例通过跨源 ID 属性保留原始数据源的标识：cim:ifcGlobalId 保留 IFC GlobalId，cim:bacnetObjectId 保留 BACnet 对象 ID，cim:cmmsAssetTag 保留 CMMS 资产标签。全局 ID 注册表（global_id_registry.yaml）维护所有实例的跨源映射关系，确保从任何数据源都可以追溯到 CIM 统一实体。

三源数据通过 CIM 设备节点形成的语义链接拓扑可以用以下结构直观表达：

```
IFC 实例                              BACnet 点位
(几何+位置)                            (实时读数)
     │                                     │
     │ cim:ifcGlobalId                     │ cim-bacnet:bacnetPointOf
     │                                     │
     └──────────► CIM 设备实体 ◄────────────┘
                      │
                      │ cim-cmms:maintenanceTarget
                      │
                      ▼
                 CMMS 工单
               (维保记录)
```

CIM 设备实体是三源数据的"语义锚点"——它不存储任何一个数据源的原始数据，而是通过标准化的链接属性将三源数据关联到统一的设备标识上。这种"锚点+链接"的架构比"复制+合并"的架构更具工程优势：每个数据源保留在自己的 Named Graph 中，保持数据来源的可追溯性和更新独立性，同时通过 SPARQL 联邦查询在查询时动态组装跨源信息。

### 4.2 BAS/BACnet 实时数据联邦

BAS/BACnet 数据联邦是 CIM 知识图谱区别于静态 BIM 本体的关键能力。传统 BIM 本体（包括 Brick 和 IFC）主要处理设计态或资产态的结构化数据，而 BAS 数据是秒级更新的实时时序流。将时序数据纳入知识图谱需要解决两个核心挑战：如何为 BACnet 数据点建立语义关联，以及如何在三元组存储中管理时序数据的更新。

**BACnet 桥接本体**定义了 9 种 BACnet 对象类型在 CIM 中的表示：

**表 4-1 BACnet 对象类型映射**

| BACnet 对象类型 | 缩写 | CIM 桥接类 | 典型用途 |
|----------------|------|-----------|---------|
| Analog Input | AI | cim-bacnet:AnalogInput | 温度/湿度/压力传感器 |
| Analog Output | AO | cim-bacnet:AnalogOutput | 阀门开度/风机频率 |
| Binary Input | BI | cim-bacnet:BinaryInput | 运行状态/故障状态 |
| Binary Output | BO | cim-bacnet:BinaryOutput | 启停指令 |
| Analog Value | AV | cim-bacnet:AnalogValue | 设定值/计算值 |
| Multi-State Value | MSV | cim-bacnet:MultiStateValue | 模式选择 |
| Accumulator | ACC | cim-bacnet:Accumulator | 能耗计量 |
| Calendar | CAL | cim-bacnet:Calendar | 时间表 |
| Schedule | SCHED | cim-bacnet:Schedule | 运行计划 |

关键的语义链接通过 cim-bacnet:bacnetPointOf 属性实现。这个属性将一个 BACnet 数据点关联到它所监测或控制的 CIM 设备实体。例如：

```
cim-inst:AI-SAT-AHU39-001        # BACnet AI 点位
    a cim-bacnet:AnalogInput ;
    cim-bacnet:bacnetPointOf cim-inst:AHU-39-001 ;    # 关联到 AHU 设备
    cim:pointType cim:SupplyAirTemperatureSensor ;    # 语义类型: 送风温度
    cim:hasValue "23.5"^^xsd:decimal ;                 # 当前值
    cim:hasUnit qudt:DegreeCelsius ;                   # 单位: 摄氏度
    cim:timestamp "2026-05-12T08:00:00Z"^^xsd:dateTime .
```

通过这一映射，原本语义匮乏的 `AI:1 = 23.5` 获得了完整的上下文：它是 AHU-39-001 的送风温度传感器，读数 23.5 摄氏度，采集于 2026 年 5 月 12 日 08:00。

**BACnet 仿真器**为项目提供了在无物理 BAS 硬件条件下的数据源。仿真器基于 11 种设备点位模板（AHU 模板含送风温度/回风温度/风量/风阀开度等，Chiller 模板含冷冻水供回水温/COP/负荷率等），为全部设备实例生成了 1,055 个 BACnet 点位。点位值根据物理模型和时段（白天/夜间/告警）生成合理的模拟数据，而非随机数。仿真器输出直接写入 CIM ABox 的 BAS 数据文件。

**时序数据管理策略**采用三快照轮换机制。三元组存储不适合存储高频时序数据（这是时序数据库的职责），但对于 CIM 的语义查询场景，不需要连续的时序流，只需要代表不同运行状态的"语义快照"。项目定义了三个 BAS Named Graph：

- **graph/bas/t0**：正常态快照，包含所有点位在标准运行条件下的读数，约 8,400 个三元组
- **graph/bas/t1**：异常态快照，包含部分点位偏离设计值的读数，约 8,400 个三元组
- **graph/bas/t2**：告警态快照，包含触发报警条件的点位读数，约 8,400 个三元组

三个快照以 8 小时间隔轮换（对应白班/中班/夜班三个运营时段），每次轮换覆盖全部 1,055 个点位。这种设计使得 SPARQL 查询可以通过 UNION 操作跨三个快照获取 24 小时的时序趋势，同时避免了在三元组存储中维护海量时序数据的性能问题。未来 M6 阶段接入真实 BAS 后，三快照机制将升级为 MQTT 流式写入 + 时序数据库（如 TimescaleDB）存储，CIM Named Graph 仅保留最新的语义快照用于联邦查询。

### 4.3 CMMS 维保工单联邦

CMMS 数据联邦为 CIM 知识图谱补充了设备全生命周期管理的第三维信息——维护历史。如果说 IFC 回答的是"设备是什么、在哪里"，BAS 回答的是"设备现在怎么样"，那么 CMMS 回答的是"设备过去经历了什么"。三者的联合构成了设备的完整时空画像。

CIM 的 CMMS 子模块（Layer 4, 13 个类）与 ISO 14224:2016 的可靠性数据收集框架对齐，定义了三种工单类型和完整的工单生命周期状态：

- **PreventiveWorkOrder (PM)**：预防性维护工单，基于时间或运行时间触发（如"每季度更换一次 AHU 初效滤网"）
- **CorrectiveWorkOrder (CM)**：纠正性维修工单，由故障或异常触发（如"AHU-001 送风温度偏高，检查冷冻水阀门"）
- **InspectionWorkOrder**：检查工单，定期巡检记录

项目 ABox 中包含 735 条工单记录，其分布为：669 条 PM（90.9%）、64 条 CM（8.7%）、2 条 Inspection（0.3%）。PM 工单占绝对多数反映了规范化医院运维的特征——以预防性维护为主，纠正性维修为辅。

每条工单通过 cim-cmms:maintenanceTarget 属性关联到 CIM 设备实体，形成工单→设备→空间→系统的完整追溯链。例如：

```
cim-inst:WO-PM-0001
    a cim-cmms:PreventiveWorkOrder ;
    cim-cmms:maintenanceTarget cim-inst:AHU-39-001 ;    # 目标设备
    cim-cmms:scheduledDate "2026-06-01"^^xsd:date ;     # 计划日期
    cim-cmms:priority "HIGH" ;                           # 优先级
    cim-cmms:woStatus "SCHEDULED" ;                      # 状态
    cim-cmms:workDescription "季度滤网更换 + 皮带检查" .
```

通过 CIM 设备节点的桥接，这条工单可以自动关联到：AHU-39-001 的 IFC 物理位置（3F 手术区 OR-01）、当前 BAS 运行状态（送风温度 23.5°C、风量正常）以及同一设备的历史 CM 工单。这种三源关联在传统分离的系统中需要人工跨系统查阅，而在 CIM 知识图谱中仅需一条 SPARQL 联邦查询。

CMMS 联邦的 ISO 14224 对齐还支持故障模式和效应分析（FMEA）。纠正性维修工单通过 cim-cmms:failureMode 属性关联到标准化的故障分类编码，使得跨项目的设备可靠性统计成为可能。例如，统计某型号冷水机组在全国多个医院项目中的故障模式分布，识别高频故障类型，优化预防性维护策略。

### 4.4 三源 SPARQL 联邦验证

三源联邦查询是 CIM 知识图谱的核心价值命题的实证验证。如果 CIM 无法通过一条查询同时检索 IFC 位置、BAS 状态和 CMMS 工单，那么"统一语义层"就只是空洞的概念。项目设计了 5 条 SPARQL 联邦验证查询，全部在 rdflib 引擎上执行通过。

**表 4-2 五条联邦验证查询及结果**

| 查询 | 描述 | 跨源数据 | Named Graph | 结果行数 | 状态 |
|------|------|---------|-------------|---------|------|
| Q1 | 设备-空间关联 | IFC + TBox | graph/tbox + graph/ifc | 212 | PASS |
| Q2 | 设备-BAS 点位 | IFC + BAS | graph/ifc + graph/bas | 186 | PASS |
| Q3 | 三角闭环 (IFC+BAS+CMMS) | 全部 3 源 | graph/ifc + graph/bas/t2 + graph/cmms | 11 | PASS |
| Q4 | FAS 探测器-空间 | FAS + IFC | graph/fas + graph/ifc | 62 | PASS |
| Q5 | CMMS 工单-设备类型 | CMMS + TBox | graph/cmms + graph/tbox | 48 | PASS |

**Q1（设备-空间关联）** 验证了 IFC 来源的设备实例是否正确关联到空间层级。212 行结果覆盖了全部设备类型，确认每台设备都有有效的 cim:locatedIn 属性指向 CIM 空间实体。

**Q2（设备-BAS 点位）** 验证了 BACnet 桥接的有效性——186 行结果表明大多数关键设备实例已通过 cim-bacnet:bacnetPointOf 关联到至少一个 BAS 数据点。

**Q3（三角闭环）** 是最关键的验证查询。它要求在同一条 SPARQL 中跨越三个 Named Graph，检索满足以下条件的记录：设备在 BAS 告警态快照（graph/bas/t2）中有活跃报警，同时在 IFC 数据（graph/ifc）中有空间位置，且在 CMMS 数据（graph/cmms）中有对应的维修工单。这一查询返回了 11 行跨源关联记录，证明了三源语义闭环的可行性。这 11 条记录意味着：11 台设备的 BAS 报警可以通过 CIM 同时定位到建筑物理空间和维保历史——这正是运维人员在故障响应中最需要的信息组合。

**Q4（FAS 探测器-空间）** 验证了消防系统与空间层级的关联。62 行结果对应全部 62 个 FAS 探测器，确认每个探测器都正确关联到所在的房间和防火分区。

**Q5（CMMS 工单-设备类型）** 验证了维保工单与设备分类的关联。48 行结果覆盖了全部有 CMMS 工单的设备类型。

五条查询合计涉及 30,016 个三元组（为 61,941 总三元组的一个子集，因为部分 Named Graph 如 graph/pset 和 graph/event 不在联邦验证范围内）。全部 5/5 通过，无一失败。

值得特别讨论的是 Q3 三角闭环查询的意义。在传统分离式系统中，当 BAS 报警"AHU-001 送风温度超标"发生时，运维人员需要执行三个独立操作：登录 BAS 系统确认报警详情，打开 BIM 查看器定位 AHU-001 的物理位置，再登录 CMMS 检查该设备是否有未完成的维修工单或近期的故障历史。这三个操作涉及三个独立的软件系统、三种不同的用户界面和三套不同的数据标识体系，典型耗时 10~15 分钟。而在 CIM 联邦查询模型下，一条 SPARQL 查询在毫秒级内返回同样的信息组合——设备位置、当前报警状态和维保历史。这不仅是效率的提升，更是信息质量的提升：人工跨系统查阅容易遗漏或错误关联，而基于本体的联邦查询由形式化语义保证关联的正确性。

除了 5 条联邦验证查询，项目还设计了 9 条业务场景查询，覆盖 8 个应用模式（设备全状态、楼层看板、能耗异常检测、维保到期预警、FAS 区域状态、三源闭环验证、安全事件处置、时序趋势分析）。28 条业务场景测试查询全部通过（28/28 PASS），确认了 CIM 知识图谱在实际业务场景中的查询能力。其中能耗异常检测模式的测试发现了 1 台设备的实际功率偏离设计值超过 20%，验证了跨 Named Graph（graph/pset 设计参数 vs graph/bas/t0 实时读数）比较分析的有效性。

### 4.5 Named Graph 架构

Named Graph 是 CIM 知识图谱数据管理的基础架构。与将所有三元组放入一个默认图（Default Graph）不同，CIM 将 61,941 个三元组分布于 9 个 Named Graph 中，每个 Graph 具有独立的语义域、更新策略和访问权限。

**表 4-3 Named Graph 架构**

| Named Graph URI | 内容 | 三元组数 | 更新策略 | 访问模式 |
|-----------------|------|---------|---------|---------|
| graph/tbox | 本体定义 (TBox) | ~12,000 | 版本级 (标准更新才变) | 只读, 所有查询共享 |
| graph/ifc | BIM 静态实例 | ~8,000 | 建设期一次写入 | 只读 |
| graph/bas/t0 | BAS 正常态快照 | ~8,400 | 3 快照 / 8h 轮换 | 读写 |
| graph/bas/t1 | BAS 异常态快照 | ~8,400 | 3 快照 / 8h 轮换 | 读写 |
| graph/bas/t2 | BAS 告警态快照 | ~8,400 | 3 快照 / 8h 轮换 | 读写 |
| graph/cmms | CMMS 维保工单 | ~4,000 | 日/月增量写入 | 读写 |
| graph/fas | FAS 消防拓扑 | ~5,000 | 设计期一次写入 | 只读 |
| graph/event | 安全事件 | ~3,000 | 实时, 事件驱动 | 读写, 无缓存 |
| graph/pset | 设计参数 (Pset) | ~5,941 | 设计期写入 | 只读 |

Named Graph 隔离的设计动机源于三个考量。第一，**更新频率的差异**。BAS 数据以 8 小时为周期轮换更新，IFC 数据在建设期一次性写入后基本不变，TBox 本体定义仅在标准更新时变化。如果将这三类数据混合在一个图中，每次 BAS 更新都可能影响到 IFC 和 TBox 数据的缓存有效性。分离后，graph/bas/* 的频繁更新不会触发 graph/tbox 的缓存失效。

第二，**访问权限的差异**。在生产环境中，graph/tbox 和 graph/ifc 应设为只读，防止运行时误修改本体定义或 BIM 静态数据。graph/bas/* 和 graph/cmms 需要读写权限，支持数据的持续注入。graph/event 需要实时写入权限（事件引擎在安全事件发生时即时写入），但也需要严格的审计日志。Named Graph 级别的权限控制比三元组级别的权限控制在实现上简单一到两个数量级。

第三，**查询优化的需求**。SPARQL 的 `FROM NAMED` 子句允许查询引擎仅扫描指定的 Named Graph，而非全量 61,941 个三元组。例如，一条仅查询 FAS 探测器状态的查询只需扫描 graph/fas（~5,000 三元组），性能开销约为全量扫描的 8%。在联邦查询中，查询引擎可以并行扫描多个 Named Graph，进一步提高效率。

BAS 时序快照的管理是 Named Graph 架构中最具特色的设计。传统做法是将 BAS 时序数据存入关系型数据库或时序数据库，但这会引入额外的技术组件和跨系统查询的复杂性。CIM 的三快照策略将 BAS 数据保留在 RDF 知识图谱内部，通过 SPARQL UNION 查询跨三个快照获取时序趋势，避免了知识图谱与外部时序数据库之间的接口开发和数据同步问题。每个快照约 8,400 个三元组（1,055 个点位 × ~8 个三元组/点位），三个快照合计约 25,200 个三元组，占总图谱的 40.7%——这一比例反映了运行态数据在建筑全生命周期信息中的主导地位。

项目的验证流水线对 Named Graph 隔离进行了专项测试（step10 的 Query 10）。测试确认了 9 个 Named Graph 之间不存在三元组泄漏——每个 Graph 中的三元组仅属于该 Graph 的语义域，跨 Graph 的数据关联仅通过 SPARQL 联邦查询在查询时动态建立，而非在数据层面混合。这一隔离保证了数据治理的清晰性和可审计性。

---

本章介绍的 Named Graph 架构与第三章的五层本体结构共同构成了 CIM 知识图谱的完整数据治理框架。五层本体提供纵向的语义层级（从抽象范畴到具体运营），Named Graph 提供横向的数据分区（从静态设计到实时运行）。两个维度的交叉形成了一个矩阵式的信息管理模型，使得每一个三元组都可以被精确定位到"哪一层语义"和"哪一类数据源"的交叉点上。这种精确定位对于数据质量管理、访问权限控制和变更影响分析都具有实质性的工程价值。

项目的 12 步验证流水线从 step1（IFC 文件解析）到 step12（MVP 端到端测试）覆盖了知识图谱构建的全部环节。在本章涉及的数据联邦层面，关键验证结果包括：step1~5 的 IFC 实例化验证（12/12 Brick 类 100% 覆盖）、step6 的 SHACL 形式化验证（VIOLATION = 0, WARNING = 0）、step7 的三源联邦验证（5/5 查询通过，30,016 三元组涉及）、step8~9 的仿真门控验证（4 个场景全部通过，CRITICAL = 0）、step10 的平台查询验证（10/10 PASS，含 Named Graph 隔离测试）以及 step11 的业务场景验证（28/28 PASS）。这些验证结果共同证明了 CIM 数据联邦架构在形式化正确性、跨源互操作性和业务实用性三个维度上的有效性。

---

*（第五章至第八章及附录将在后续版本中完成）*
