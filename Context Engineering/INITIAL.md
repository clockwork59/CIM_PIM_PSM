# INITIAL: CIM Context Engineering 扩展需求

**基于文档**:
1. `The Computational Independent Model for Enterprise Information System Development` - Singh & Sood
2. `面向制造系统互操作性和知识共享的模型驱动本体方法` - Chungoora et al.

**目标**: 基于两篇学术论文的理论贡献，扩展 CIM 项目的 Context Engineering 体系，建立从需求捕获到本体形式化的完整方法论。

---

## FEATURE: 建立扩展的 CIM Context 体系

### 1. CIM 需求捕获框架（基于 Singh & Sood）

扩展当前 CIM 层定义，引入四层需求模型：

```
CIM 需求金字塔:
┌─────────────────────────────────────┐
│  组织需求 (Organizational)           │
│  - 组织结构、流程、用户类别           │
├─────────────────────────────────────┤
│  非功能需求 (Non-Functional)         │
│  - 可靠性、可用性、效率、可扩展性      │
├─────────────────────────────────────┤
│  功能需求 (Functional)               │
│  - 业务流程、系统功能、实现规格        │
├─────────────────────────────────────┤
│  用户需求 (User Requirements)        │
│  - 用例图、业务需求、交付物规格        │
└─────────────────────────────────────┘
```

**所需 UML 图表**:
- 用例图 (Use Case Diagram) - 捕获用户视角
- 活动图 (Activity Diagram) - 业务流程工作流
- 序列图 (Sequence Diagram) - 系统交互时序

### 2. 本体驱动的 PIM 形式化（基于 Chungoora et al.）

引入制造核心本体方法到医疗建筑领域：

**核心概念**:
- **领域核心本体** (Domain Core Ontology): 医疗建筑技术系统的通用概念
- **ECLIF 形式化**: 使用扩展通用逻辑交换格式表达语义约束
- **知识验证机制**: 基于完整性约束的跨系统知识验证

**UML 到 ECLIF 映射**:
| UML 元素 | ECLIF 元素 |
|---------|-----------|
| Class | Type |
| Generalisation | sup (超类型关系) |
| Binary Association | BinaryRel |
| n-ary Association | TernaryRel/QuaternRel |
| Attribute (Boolean) | UnaryRel |
| Stereotype | n-ary Function |
| Powertype | Metaproperty |

### 3. PIM 级互操作性框架

基于 IMKS (Interoperable Manufacturing Knowledge Systems) 方法：

**关键机制**:
- **专业化 (Specialization)**: 通过约束进行领域特定化
- **知识验证约束**: PIM 级别的完整性约束定义
- **跨域映射**: 不同领域 PIM 间的概念映射

### 4. 模型转换规范

**CIM → PIM 转换规则**:
1. 业务规则 → 逻辑约束
2. 用例场景 → 服务接口
3. 活动流程 → 控制逻辑

**PIM → PSM 转换规则**:
1. ECLIF 类型 → 数据库 Schema
2. 完整性约束 → 验证规则
3. 服务接口 → API 实现

---

## EXAMPLES: 需要创建的示例

### 示例 1: 手术室环境控制 CIM 建模
基于 Singh & Sood 的 Physician's Activity System (PAS) 方法，展示完整 CIM 捕获：
- 用例图: 手术医生、护士、运维工程师交互
- 活动图: 手术室准备流程
- 序列图: 环境参数调控时序

### 示例 2: 医疗建筑核心本体 (Healthcare Building Core Ontology)
基于 Chungoora 的制造核心本体，创建医疗建筑领域核心本体：
- UML 类图 (轻量级表示)
- ECLIF 形式化 (重量级本体)
- 完整性约束示例

### 示例 3: HVAC 系统 PIM 级互操作
展示 PIM 级知识验证：
- 设计域 PIM (空调末端设计)
- 制造域 PIM (设备生产规格)
- 知识验证约束 (设计可制造性检查)

### 示例 4: CIM-PIM-PSM 完整转换链
从业务需求到代码实现的端到端示例：
- CIM: 业务规则 "手术室温度必须保持在21-24°C"
- PIM: ECLIF 约束 + API 契约
- PSM: Python 实现 + PostgreSQL Schema

---

## DOCUMENTATION: 参考资源

### 学术论文
1. **Singh & Sood** - CIM 需求捕获方法论
   - 重点: 四层需求模型、UML 图表应用
   - 应用: 医疗建筑需求工程

2. **Chungoora et al.** - 模型驱动本体方法
   - 重点: ECLIF、制造核心本体、知识验证
   - 应用: 跨系统互操作性、PIM 级语义约束

### 标准规范
- **ISO/IEC 24707** - Common Logic 框架
- **OMG MDA** - 模型驱动架构指南
- **ISO 10303 (STEP)** - 产品模型数据交换

### 本体语言
- **ECLIF** - 扩展通用逻辑交换格式
- **CLIF** - 通用逻辑交换格式语法
- **OWL** - Web 本体语言 (对比参考)

---

## OTHER CONSIDERATIONS

### 关键区别: 制造 vs 医疗建筑
| 维度 | 制造领域 (Chungoora) | 医疗建筑领域 (本项目) |
|-----|---------------------|---------------------|
| 核心实体 | PartFamily, Feature | Space, System, Equipment |
| 关注点 | 零件设计、加工特征 | 空间环境、系统运行 |
| 互操作性 | CAD/CAM/PLM 系统 | BIM/BMS/IoT 平台 |
| 验证焦点 | 可制造性 | 合规性、安全性 |

### 适配要点
1. **核心本体重构**: 从制造概念映射到建筑概念
2. **约束类型调整**: 从加工约束调整为运行约束
3. **验证目标变化**: 从可制造性验证调整为合规性验证

### 技术实现注意
- ECLIF 工具链在医疗建筑领域的可用性
- UML 到 ECLIF 转换的自动化程度
- 与现有 BIM/IFC 标准的兼容性

---

## SUCCESS CRITERIA

- [ ] 创建 4 个完整示例文档
- [ ] 建立 UML-to-ECLIF 映射规范
- [ ] 定义医疗建筑核心本体框架
- [ ] 提供 CIM-PIM-PSM 转换模板
- [ ] 与现有 Context Engineering 体系集成
