# Agent 协作体系

> 本文档介绍9个专业Agent的分工与协作方式，是理解CIM建模流程的关键。

## Agent 体系总览

```
                    ┌───────────────────────────────────────┐
                    │         Agent-09 模型整合验证师          │
                    │      (Model Integration Validator)    │
                    │              质量守门员                 │
                    └───────────────────────────────────────┘
                                      ↑
    ┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
    ↓         ↓         ↓         ↓         ↓         ↓         ↓
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│Agent-01│ │Agent-02│ │Agent-03│ │Agent-04│ │Agent-05│ │Agent-06│ │Agent-07│
│系统拓扑 │ │空间本体 │ │设备本体 │ │流动模型 │ │系统空间 │ │控制系统 │ │计量体系 │
│建模师   │ │建模师   │ │建模师   │ │建模师   │ │耦合建模师│ │建模师   │ │建模师   │
└───────┘ └───────┘ └───────┘ └───────┘ └───────┘ └───────┘ └───────┘
                                                                        ↓
                                                                  ┌───────────┐
                                                                  │Agent-08   │
                                                                  │运维管理   │
                                                                  │建模师     │
                                                                  └───────────┘
```

## 五阶段建模流程

```
阶段一：基础模型层
├── Agent-01 (系统拓扑) → 技术系统列表、拓扑结构
└── Agent-02 (空间本体) → 空间层级模型

阶段二：实体模型层
├── Agent-03 (设备本体) → 设备分类、属性模型
└── Agent-04 (流动模型) → 物质/能量/信息流模型

阶段三：关系耦合层
├── Agent-05 (系统-空间耦合) → 设备定位、服务范围
└── Agent-06 (控制系统) → 传感器、执行器、控制回路

阶段四：管理集成层
├── Agent-07 (计量体系) → 计量点、能耗分摊规则
└── Agent-08 (运维管理) → 告警、工单、维护计划

阶段五：模型整合层
└── Agent-09 (模型整合验证) → CIM数据包、验证报告
```

## Agent 详细说明

---

### Agent-01: 系统拓扑建模师 (System Topology Architect)

**阶段**: 阶段一（基础模型层）

**依赖**: 无（基础Agent）

**被依赖**: Agent-03, Agent-04, Agent-05, Agent-06, Agent-07

**核心职责**:
1. 技术系统识别与列项：全面梳理医疗建筑中涉及的所有技术系统
2. 系统分类与层级定义：建立系统分类体系和层级结构
3. 系统拓扑建模：为每个系统构建源-输配-末端的拓扑网络模型
4. 系统间依赖关系定义：识别系统间的依赖、供给关系

**理论基础 - 拓扑网络元模型**:

任何技术系统都是一个**有向图（Directed Graph）**，包含：

- **节点类型（Node Types）**:
  - `Source_Node`: 系统的能量/介质输入端（如市电、冷机产冷）
  - `Sink_Node`: 系统的能量/介质消耗端（如末端设备）
  - `Distribution_Node`: 中间节点
    - `Junction`: 多路汇聚（如集水器）
    - `Splitter`: 一路分配为多路（如分水器）
    - `Regulator`: 调节节点（如调节阀、变频器）
    - `Transformer`: 形态转换（如换热器、变压器）

- **边类型（Edge Types）**:
  - `Trunk`: 主要传输通道（如冷冻水主管）
  - `Branch`: 次级通道（如楼层水平管）
  - `Terminal_Connection`: 末端连接

**输出物**:
- 系统目录（System Catalog）
- 各系统拓扑模型（System Topologies）
- 系统间依赖关系（System Dependencies）

---

### Agent-02: 空间本体建模师 (Space Ontology Architect)

**阶段**: 阶段一（基础模型层）

**依赖**: 无（基础Agent）

**被依赖**: Agent-05, Agent-06, Agent-07, Agent-08

**核心职责**:
1. 建筑空间层级建模：Site→Building→Floor→Zone→Room→SubSpace
2. 功能区域分类：医疗区域、辅助区域、公共区域
3. 医疗专用空间模型：手术室、ICU、病房等特殊要求
4. 空间属性定义：面积、体积、环境要求等

**六层空间模型**:
```yaml
L0_Site: 站点（完整地块）
L1_Building: 建筑（独立功能建筑）
L2_Floor: 楼层（横向分层）
L3_Zone: 区域（功能相近的房间组）
L4_Room: 房间（基本功能单元）
L5_SubSpace: 子空间（房间内的局部空间）
```

**输出物**:
- 空间层级模型（Space Hierarchy）
- 功能区域分类（Zone Classification）
- 医疗专用空间模型（Medical Space Models）
- 空间属性与要求（Space Attributes & Requirements）

---

### Agent-03: 设备本体建模师 (Equipment Ontology Architect)

**阶段**: 阶段二（实体模型层）

**依赖**: Agent-01（系统拓扑）

**被依赖**: Agent-05, Agent-06, Agent-07, Agent-08

**核心职责**:
1. 设备分类体系：建立设备类型层次结构
2. 设备属性模型：定义各类设备的属性集合
3. 设备组件结构：复杂设备的子设备关系
4. 控制与告警规则：设备级控制参数和告警条件

**设备分类示例**:
```yaml
HVAC设备:
  - 冷水机组 (Chiller)
  - 空调机组 (AHU)
  - 风机盘管 (FCU)
  - 水泵 (Pump)
  - 冷却塔 (CoolingTower)

电气设备:
  - 变压器 (Transformer)
  - 发电机 (Generator)
  - 配电箱 (DistributionPanel)
  - UPS

给排水设备:
  - 水泵
  - 水箱 (WaterTank)
  - 热水器 (WaterHeater)
```

**输出物**:
- 设备分类体系（Equipment Taxonomy）
- 设备属性模型（Equipment Attribute Models）
- 设备组件结构（Equipment Component Structure）
- 控制与告警规则（Control & Alarm Rules）

---

### Agent-04: 流动模型建模师 (Flow Model Architect)

**阶段**: 阶段二（实体模型层）

**依赖**: Agent-01（系统拓扑）

**被依赖**: Agent-06（控制系统）

**核心职责**:
1. 物质流模型：水、空气、蒸汽等介质的流动
2. 能量流模型：热能、电能的传输与转换
3. 信息流模型：控制信号、监测数据的流动
4. 流动路径与守恒：基于第一性原理的流动计算

**流动类型**:
```yaml
物质流:
  冷冻水: 冷水机组 → 水泵 → AHU → 末端 → 回水
  空气: 新风 → 处理 → 送风 → 房间 → 回风/排风

能量流:
  热能: 锅炉 → 换热器 → 末端
  电能: 变压器 → 配电箱 → 设备

信息流:
  控制: 传感器 → DDC → 执行器
  数据: 设备 → 网关 → 平台
```

**输出物**:
- 物质流模型（Material Flow Models）
- 能量流模型（Energy Flow Models）
- 信息流模型（Information Flow Models）
- 流动路径与守恒计算（Flow Paths & Conservation）

---

### Agent-05: 系统-空间耦合建模师 (System-Space Coupling Architect)

**阶段**: 阶段三（关系耦合层）

**依赖**: Agent-01（系统拓扑）, Agent-02（空间本体）, Agent-03（设备本体）

**被依赖**: Agent-07（计量体系）, Agent-08（运维管理）

**核心职责**:
1. 设备-位置关系：设备在哪个空间
2. 管路-穿越空间关系：管路经过哪些空间
3. 系统-服务空间关系：系统服务哪些空间
4. 空间环境要求映射：空间需求如何映射到系统设计

**耦合关系示例**:
```yaml
设备定位:
  设备: CH-3F-01 (冷水机组)
  所在空间: BLDG01-L3-MECH (3层空调机房)

系统服务空间:
  系统: HVAC-AHU-3F-01
  服务区域: BLDG01-L3-ZMED-OP (3层门诊医疗区)
  包含房间: [ROOM-301, ROOM-302, ROOM-303, ...]
  总服务面积: 800 m²

空间负荷需求:
  空间: ROOM-301 (内科诊室, 20m²)
  冷负荷: 3496W
  热负荷: 2000W
  新风量: 100m³/h
```

**输出物**:
- 设备-位置关系（Equipment-Location Mapping）
- 管路-穿越空间关系（Routing-Space Relations）
- 系统-服务空间关系（System-Space Service Relations）
- 空间环境要求映射（Space Requirement Mapping）

---

### Agent-06: 控制系统建模师 (Control System Architect)

**阶段**: 阶段三（关系耦合层）

**依赖**: Agent-01（系统拓扑）, Agent-03（设备本体）, Agent-04（流动模型）

**被依赖**: Agent-08（运维管理）

**核心职责**:
1. 传感器模型：类型、位置、量程、精度
2. 执行器模型：阀门、风门、变频器等
3. 控制器模型：DDC、PLC等控制设备
4. 控制回路模型：控制策略、设定值、PID参数

**控制系统要素**:
```yaml
传感器:
  - 温度传感器 (Temperature Sensor)
  - 湿度传感器 (Humidity Sensor)
  - 压力传感器 (Pressure Sensor)
  - 流量传感器 (Flow Sensor)
  - CO2传感器 (CO2 Sensor)
  - 功率传感器 (Power Sensor)

执行器:
  - 阀门执行器 (Valve Actuator)
  - 风门执行器 (Damper Actuator)
  - 变频器 (VFD - Variable Frequency Drive)

控制器:
  - DDC控制器 (Direct Digital Controller)
  - PLC控制器 (Programmable Logic Controller)

控制策略:
  - ON_OFF: 开关控制
  - PID: 比例积分微分控制
  - Cascade: 串级控制
  - Schedule: 时间表控制
```

**输出物**:
- 传感器模型（Sensor Models）
- 执行器模型（Actuator Models）
- 控制器模型（Controller Models）
- 控制回路模型（Control Loop Models）

---

### Agent-07: 计量体系建模师 (Metering System Architect)

**阶段**: 阶段四（管理集成层）

**依赖**: Agent-01（系统拓扑）, Agent-03（设备本体）, Agent-05（系统-空间耦合）

**被依赖**: Agent-08（运维管理）

**核心职责**:
1. 计量层级结构：Site→Building→Floor→Zone→Room→Equipment
2. 能源介质分类：电、水、气、热、冷
3. 分户分项计量模型：计量点配置、采集参数
4. 能耗分摊规则：按面积、按人员、按时间等

**计量层级**:
```yaml
L0_Site: 总表（站点总能耗）
L1_Building: 建筑表（建筑能耗）
L2_Floor: 楼层表（楼层能耗）
L3_Zone: 区域表（区域能耗）
L4_Room: 房间表（房间能耗）
L5_Equipment: 设备表（设备能耗）
```

**分摊规则**:
```yaml
按面积分摊: 各区域按面积比例分摊总能耗
按人员分摊: 按人员密度或实际人数分摊
按使用时间分摊: 按设备运行时间分摊
按负荷分摊: 按实际负荷比例分摊
```

**输出物**:
- 计量层级结构（Metering Hierarchy）
- 能源介质分类（Energy Medium Classification）
- 分户分项计量模型（Sub-metering Models）
- 能耗分摊规则（Energy Allocation Rules）

---

### Agent-08: 运维管理建模师 (O&M Management Architect)

**阶段**: 阶段四（管理集成层）

**依赖**: Agent-03（设备本体）, Agent-06（控制系统）, Agent-07（计量体系）

**被依赖**: Agent-09（模型整合验证）

**核心职责**:
1. 告警事件模型：告警级别、类型、通知方式
2. 工单流程模型：工单类型、状态流转、优先级
3. 维护策略模型：维护周期、内容、SOP
4. 资产生命周期模型：采购、安装、运维、报废

**运维要素**:
```yaml
告警:
  级别:
    - CRITICAL: 紧急（影响生命安全）
    - HIGH: 高（影响系统运行）
    - MEDIUM: 中（需要关注）
    - LOW: 低（提示性）
  类型:
    - 超限告警: 温度/压力/流量超出范围
    - 离线告警: 设备通信中断
    - 故障告警: 设备故障状态
  通知方式: 短信、邮件、APP推送、声光报警

工单:
  类型: 维修、保养、巡检、改造
  状态: 待处理、处理中、已完成、已关闭
  优先级: 紧急、高、中、低

维护:
  周期: 日、周、月、季、年
  内容: 检查、清洁、润滑、更换、校准
  标准: SOP（Standard Operating Procedure）
```

**输出物**:
- 告警事件模型（Alarm Event Models）
- 工单流程模型（Work Order Flow Models）
- 维护策略模型（Maintenance Strategy Models）
- 资产生命周期模型（Asset Lifecycle Models）

---

### Agent-09: 模型整合验证师 (Model Integration Validator)

**阶段**: 阶段五（模型整合层）

**依赖**: Agent-01~08（全部前置Agent）

**被依赖**: 无（最终Agent）

**核心职责**:
1. 整合Agent-01至Agent-08的输出
2. 验证模型一致性：命名、单位、关系、编码
3. 验证模型完整性：必填属性、关系完整性、引用有效性
4. 生成CIM数据包：统一领域模型、验证报告

**验证维度**:
```yaml
一致性检查:
  - 命名一致性: 同一概念使用相同名称
  - 单位一致性: 相同物理量使用相同单位
  - 关系一致性: 双向关系保持一致
  - 编码一致性: 遵循编码规范

完整性检查:
  - 必填属性: 必填字段是否完整
  - 关系完整: 关联关系是否完整
  - 引用有效: 引用的实体是否存在

合理性检查:
  - 参数范围: 参数值是否在合理范围
  - 计算结果: 计算结果是否合理
  - 配置冲突: 是否存在配置冲突
```

**输出物**:
- 统一领域模型（Unified CIM Model）
- 模型一致性报告（Consistency Report）
- 模型完整性报告（Completeness Report）
- 交叉引用索引（Cross-reference Index）
- CIM数据包（CIM Bundle）

---

## Agent 依赖关系图

```
                    ┌─────────┐     ┌─────────┐
                    │Agent-01 │     │Agent-02 │
                    │系统拓扑 │     │空间本体 │
                    └────┬────┘     └────┬────┘
                         │               │
         ┌───────────────┼───────────────┼───────────────┐
         │               │               │               │
         ▼               ▼               ▼               │
    ┌─────────┐     ┌─────────┐     ┌─────────┐          │
    │Agent-03 │     │Agent-04 │     │         │          │
    │设备本体 │     │流动模型 │     │         │          │
    └────┬────┘     └────┬────┘     │         │          │
         │               │          │         │          │
         ├───────────────┼──────────┘         │          │
         │               │                    │          │
         ▼               ▼                    ▼          │
    ┌─────────┐     ┌─────────┐          ┌─────────┐     │
    │Agent-05 │◄────│Agent-06 │          │         │     │
    │系统-空间│     │控制系统 │          │         │     │
    └────┬────┘     └────┬────┘          │         │     │
         │               │               │         │     │
         ├───────────────┘               │         │     │
         │                               │         │     │
         ▼                               │         │     │
    ┌─────────┐                          │         │     │
    │Agent-07 │                          │         │     │
    │计量体系 │                          │         │     │
    └────┬────┘                          │         │     │
         │                               │         │     │
         └───────────────┬───────────────┘         │     │
                         │                         │     │
                         ▼                         │     │
                    ┌─────────┐                    │     │
                    │Agent-08 │◄───────────────────┘     │
                    │运维管理 │◄─────────────────────────┘
                    └────┬────┘
                         │
                         ▼
                    ┌─────────┐
                    │Agent-09 │
                    │模型整合 │
                    └─────────┘
```

## 协作接口示例

**Agent-02 → Agent-05（空间→耦合）**:
```yaml
空间定义:
  zone_id: "BLDG01-L3-ZMED-OP"
  zone_name: "3层门诊医疗区"
  area_m2: 800
  rooms: ["ROOM-301", "ROOM-302", ...]
```

**Agent-01 → Agent-05（系统→耦合）**:
```yaml
系统定义:
  system_id: "HVAC-AHU-3F-01"
  system_type: "AHU"
  capacity: "50000 m³/h"
```

**Agent-05 整合输出**:
```yaml
耦合关系:
  system_id: "HVAC-AHU-3F-01"
  serves_zones: ["BLDG01-L3-ZMED-OP"]
  serves_rooms: ["ROOM-301", "ROOM-302", ...]
  total_area: 800
```

## 使用 generate_cim_bundle.sh

一键生成完整CIM数据包：

```bash
./generate_cim_bundle.sh
```

该脚本由Agent-09设计，会：
1. 创建标准化目录结构
2. 生成本体定义文件 (JSON-LD)
3. 整合各Agent输出到 `Raw_Agent_Outputs/`
4. 运行一致性验证
5. 生成验证报告
6. 打包为可交付的CIM Bundle

输出位置：`project_deliverables/CIM_Bundle/`

## 快速参考表

| Agent | 阶段 | 依赖 | 核心输出 | 关键技能 |
|-------|------|------|----------|----------|
| **Agent-01** | 阶段一 | 无 | 系统拓扑 | 机电系统知识 |
| **Agent-02** | 阶段一 | 无 | 空间层级 | 建筑知识 |
| **Agent-03** | 阶段二 | Agent-01 | 设备本体 | 设备知识 |
| **Agent-04** | 阶段二 | Agent-01 | 流动模型 | 流体力学/热力学 |
| **Agent-05** | 阶段三 | Agent-01,02,03 | 系统-空间耦合 | 负荷计算 |
| **Agent-06** | 阶段三 | Agent-01,03,04 | 控制系统 | 自动化控制 |
| **Agent-07** | 阶段四 | Agent-01,03,05 | 计量体系 | 能源管理 |
| **Agent-08** | 阶段四 | Agent-03,06,07 | 运维管理 | 运维管理 |
| **Agent-09** | 阶段五 | Agent-01~08 | CIM数据包 | 系统集成 |
