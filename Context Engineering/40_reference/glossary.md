# 术语表 (Glossary)

**文档 ID**: `CIMU-REF-03-术语表`
**最后更新**: 2026-05-11

---

## MDA 架构

| 术语 | 英文 | 定义 |
|------|------|------|
| CIM | Common Information Model | 通用信息模型，平台无关的领域知识表示 |
| PIM | Platform-Independent Model | 平台无关模型，可部署到任何图数据库 |
| PSM | Platform-Specific Model | 平台特定模型，如 Apache Jena Fuseki 实例 |
| TBox | Terminological Box | 术语盒，定义类(owl:Class)和属性(owl:ObjectProperty) |
| ABox | Assertion Box | 断言盒，定义实例(个体)及其属性值 |

## 本体工程

| 术语 | 英文 | 定义 |
|------|------|------|
| owl:Class | OWL Class | OWL 类定义，本体中的概念节点 |
| owl:equivalentClass | Equivalent Class | 等价类映射，用于跨本体对齐 |
| rdfs:subClassOf | Subclass Relation | 子类关系，构建类层次结构 |
| SPARQL | SPARQL Protocol and RDF Query Language | RDF 图查询语言 |
| Named Graph | Named Graph | 命名图，RDF四元组中的图标识符 |
| SHACL | Shapes Constraint Language | 形状约束语言，用于 RDF 数据验证 |
| Triple | 三元组 | RDF 最小数据单元：主语-谓语-宾语 |

## BFO 上层本体

| 术语 | 英文 | 定义 |
|------|------|------|
| BFO | Basic Formal Ontology | 基础形式本体，ISO/IEC 21838-2 标准 |
| Continuant | 持续体 | 在时间中持续存在的实体（设备、空间） |
| Occurrent | 发生体 | 在时间中展开的过程（事件、流动） |

## 流动模型

| 术语 | 英文 | 定义 |
|------|------|------|
| FlowPath | 流动路径 | 介质从源到汇的完整路径 |
| FlowSegment | 流动段 | FlowPath 中的一个管段/线段 |
| ConnectionPoint | 连接点 | 设备上的流体/电气/信号接口 |
| MassFlow | 质量流 | 物质（水、气体、蒸汽）的流动 |
| EnergyFlow | 能量流 | 电力、热能、冷量的传递 |
| InformationFlow | 信息流 | 控制信号、传感数据的传输 |

## 安全事件处置

| 术语 | 英文 | 定义 |
|------|------|------|
| SecurityEvent | 安全事件 | 需要人员响应的事件实体，具有5态状态机 |
| ActionChain | 动作链 | 预案中的有序动作序列，支持顺序/并行/条件分支 |
| ActionNode | 动作节点 | 动作链中的单个可执行原子动作 |
| ResponderRole | 响应者角色 | 执行动作的人员角色（操作员、技术员、安保组长） |
| BASCommand | BAS指令 | 发送给楼宇自控系统的联动指令 |
| EmergencyPlan | 应急预案 | 结构化的应急处置模板 |
| EventClosureReport | 事件闭环报告 | 事件处置完成后的总结报告 |

## 设计与验证

| 术语 | 英文 | 定义 |
|------|------|------|
| LOD | Level of Development | 模型开发深度等级 |
| LOI | Level of Information | 信息深度等级 |
| FMEA | Failure Mode and Effects Analysis | 失效模式与影响分析 |
| pyshacl | Python SHACL Validator | Python SHACL 验证器 |

## 行业标准

| 术语 | 英文 | 定义 |
|------|------|------|
| IFC | Industry Foundation Classes | 建筑信息模型交换标准 |
| Brick | Brick Schema | 建筑能源建模语义框架 |
| ASHRAE 223P | ASHRAE Standard 223P | HVAC 语义数据模型标准 |
| FSO | Flow Systems Ontology | 流体系统本体 |
| BACnet | Building Automation and Control Networks | 楼宇自控网络协议 |
| GB 50333 | 医院洁净手术部建筑技术规范 | 中国国标，洁净手术室温湿度/压差要求 |
| WS 435 | 医疗机构建筑标准 | 中国卫生行业标准 |
| IEC 60364-7-710 | 医疗场所电气安装 | 国际电工委员会标准 |

---

## 相关文件

- 本体导论: `Context Engineering/00_foundations/03_cim_ontology_introduction.md`
- 类目录: `Context Engineering/40_reference/cim_class_catalog.md`
- 标准对齐: `Context Engineering/40_reference/standards_alignment.md`
