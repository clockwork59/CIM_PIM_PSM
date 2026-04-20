# 系统拓扑模板

**模板 ID**: `CIMU-TEMPLATE-SYSTEM-TOPOLOGY`
**版本**: v1.0
**最后更新**: 2025-12-07

---

## 模板说明

**用途**：定义机电系统的拓扑结构，包括节点、连接关系、流动方向
**适用系统**：HVAC、给排水、医疗气体、电气系统
**输出格式**：JSON/YAML/RDF（可导入CIM模型）

---

## 模板结构

```yaml
# CIM系统拓扑模板
system_topology:
  # 1. 基本信息
  基本信息:
    系统ID: "HVAC-CHP-001"                    # 格式: CATEGORY-SUBSYSTEM-NUMBER
    系统名称: "3号楼冷冻水系统"
    系统类别: "HVAC"                         # HVAC/PLUMBING/ELECTRICAL/MEDICAL_GAS/AUTOMATION
    子系统类型: "CHP"                        # CHP: Chilled Water Plant
    服务范围: ["L2-ZONE-03", "L3-ZONE-12"]  # 服务的空间ID列表
    优先级: 1                               # 1:最高 5:最低
    建模日期: "2025-12-07"
    建模工程师: "张三"

  # 2. 节点定义
  节点定义:
    - 节点ID: "HVAC-CHP-SRC-001"
      节点类型: "Source_Node"               # Source/Sink/Distribution
      节点名称: "冷机-001"
      设备ID: "CH-001-A"
      子系统: "CHILLER"
      额定容量: 1055                         # kW
      额定功率: 185                          # kW
      额定COP: 5.7
      冷媒类型: "R134a"

    - 节点ID: "HVAC-CHP-DIST-001"
      节点类型: "Distribution_Node"
      节点名称: "冷冻水泵-主管段"
      节点子类型: "Junction"                # Junction/Splitter/Regulator/Transformer
      设备ID: "CHWP-001-A"
      流量: 180                              # m³/h
      扬程: 32                               # m

    - 节点ID: "HVAC-CHP-SINK-001"
      节点类型: "Sink_Node"
      节点名称: "AHU-3F-01"
      设备ID: "AHU-0301"
      服务区域: "L3-ZONE-08"

  # 3. 连接关系
  连接关系:
    - 连接ID: "CONN-001"
      源节点: "HVAC-CHP-SRC-001"
      目标节点: "HVAC-CHP-DIST-001"
      介质类型: "CHW"                        # 冷冻水
      流动方向: "forward"                    # forward/backward/bidirectional
      连接类型: "Trunk"                      # Trunk:主干/Branch:分支/Terminal:末端
      管径: "DN250"

    - 连接ID: "CONN-002"
      源节点: "HVAC-CHP-DIST-001"
      目标节点: "HVAC-CHP-SINK-001"
      介质类型: "CHW"
      流动方向: "forward"
      连接类型: "Branch"
      管径: "DN150"

  # 4. 控制逻辑
  控制逻辑:
    - 控制ID: "CTRL-001"
      被控节点: "HVAC-CHP-SRC-001"
      控制变量: "setpoint_supply_temp"       # 设定值: 供水温度
      设定值: 7.0                            # °C
      实际值数据源: "AI-TEMP-CHW-SPLY"
      控制策略: "ON_OFF"                    # ON_OFF/MODULATING/FLOATING
      优先级: 1

    - 控制ID: "CTRL-002"
      被控节点: "HVAC-CHP-DIST-001"
      控制变量: "enable_pump"
      设定值: "AUTO"                        # AUTO/ON/OFF
      控制策略: "ON_OFF"
      联锁条件: "CHILLER_RUNNING"          # 冷机运行后延迟启动水泵
      延迟时间: 30                          # 秒

  # 5. 计量点
  计量点:
    - 计量ID: "METER-CHW-001"
      计量类型: "FLOW"
      被计量节点: "HVAC-CHP-DIST-001"
      计量单位: "m³/h"
      精度: 0.1
      刷新周期: 60                         # 秒

    - 计量ID: "METER-PWR-001"
      计量类型: "POWER"
      被计量节点: "HVAC-CHP-SRC-001"
      计量单位: "kW"
      精度: 1.0
      刷新周期: 30

  # 6. 运行参数
  运行参数:
    设计供回水温差: 5                      # °C
    设计供水温度: 7                        # °C
    设计回水温度: 12                       # °C
    工作压力: 1.0                          # MPa
    水质要求: "GB/T 29044"

  # 7. 维护信息
  维护信息:
    维护周期: "QUARTERLY"                  # DAILY/WEEKLY/MONTHLY/QUARTERLY/YEARLY
    关键检查项:
      - "检查冷机压缩机运行状态"
      - "检查水泵振动和噪音"
      - "检查管道保温完整性"
    上次维护日期: "2025-11-15"
    下次维护日期: "2026-02-15"

  # 8. 关联文档
  关联文档:
    - 类型: "P&ID图纸"
      文件名: "HVAC-CHP-PID-001.dwg"
      版本: "v2.1"

    - 类型: "设备样本"
      文件名: "Chiller-001-Manual.pdf"
      设备型号: "York-YK-1055"

  # 9. 版本信息
  版本信息:
    版本号: "1.0"
    创建日期: "2025-12-07"
    创建人: "张三"
    变更历史:
      - 版本: "0.9"
        日期: "2025-12-01"
        变更: "初版，仅包含核心设备"
      - 版本: "1.0"
        日期: "2025-12-07"
        变更: "增加计量点和控制逻辑"

  # 10. 验证签名
  验证签名:
    建模工程师: "张三"
    审核工程师: "李四"
    审核日期: "2025-12-08"
    状态: "APPROVED"                      # DRAFT/REVIEW/APPROVED
```

---

## 节点类型说明

### 1. Source_Node（源节点）
- **定义**：能量或介质的输入源
- **示例**：冷机、锅炉、变压器、发电机
- **属性**：有输出，无输入（或只有能源输入）

### 2. Sink_Node（汇节点）
- **定义**：能量或介质的消耗端
- **示例**：AHU、FCU、照明灯具、医疗设备
- **属性**：有输入，无输出（或输出为废弃物）

### 3. Distribution_Node（分配节点）
- **定义**：分配、汇集、调节的中间节点
- **子类型**：
  - **Junction**：多路输入汇聚（如：分集水器）
  - **Splitter**：一路输入分配（如：分配器）
  - **Regulator**：流量/压力调节（如：阀门）
  - **Transformer**：介质形态转换（如：换热器）

---

## 连接类型说明

### 1. Trunk（主干）
- **定义**：主要能量/介质传输通道
- **特点**：大管径、高流量
- **示例**：主管、主母线

### 2. Branch（分支）
- **定义**：次级传输通道
- **特点**：中等流量
- **示例**：支管、分配管线

### 3. Terminal_Connection（末端连接）
- **定义**：到最终设备或端口的连接
- **特点**：小管径、低流量
- **示例**：到FCU的连接、到插座的电缆

---

## 使用示例

### 示例1：简单的FCU系统

```yaml
节点:
  - 节点ID: "HVAC-FCU-SRC"
    节点类型: "Source_Node"
    节点名称: "供水分水器"

  - 节点ID: "HVAC-FCU-EQUIP"
    节点类型: "Sink_Node"
    节点名称: "FCU-301"

连接:
  - 源节点: "HVAC-FCU-SRC"
    目标节点: "HVAC-FCU-EQUIP"
    介质类型: "HW"
    连接类型: "Branch"
```

### 示例2：带旁通的冷机系统

```yaml
节点:
  - 节点ID: "HVAC-CHWP-001"
    节点类型: "Distribution_Node"
    节点子类型: "Junction"

  - 节点ID: "HVAC-CHILLER-001"
    节点类型: "Source_Node"

  - 节点ID: "HVAC-BYPASS"
    节点类型: "Distribution_Node"
    节点子类型: "Regulator"

连接:
  # 主路径
  - 源节点: "HVAC-CHWP-001"
    目标节点: "HVAC-CHILLER-001"

  # 旁通路径
  - 源节点: "HVAC-CHWP-001"
    目标节点: "HVAC-BYPASS"
```

---

## 质量标准

### 完整性要求
- [ ] 所有节点必须有唯一ID
- [ ] 所有连接必须有源节点和目标节点
- [ ] 所有设备节点必须关联到设备ID
- [ ] 所有末端节点必须关联到服务空间

### 逻辑一致性
- [ ] 没有孤立节点（至少1个连接）
- [ ] Source节点没有输入连接
- [ ] Sink节点没有输出连接
- [ ] 介质类型在连接路径上保持一致

### 可实现性
- [ ] 所有设定的属性值在设备规格范围内
- [ ] 控制逻辑清晰且可实现
- [ ] 所有计量点都有对应的数据源

---

## 导出选项

### 1. JSON格式（推荐）
```bash
# 直接导出为JSON，便于程序处理
python export_topology.py --format json --output system.json
```

### 2. RDF格式（语义网）
```bash
# 导出为RDF/OWL，支持推理
python export_topology.py --format rdf --output system.ttl
```

### 3. GraphML格式（图可视化）
```bash
# 导出为GraphML，可在Gephi中可视化
python export_topology.py --format graphml --output system.graphml
```

---

## 相关资源

- 案例：[医院HVAC系统CIM建模案例](../../30_examples/hospital_hvac_cim_case.md)
- 模板：[控制回路模板](../control_loop_template.md)
- 指南：[BIM工程师实施指南](../../10_guides/02_bim_engineer_guide.md)
- 参考：[拓扑网络理论](../../00_foundations/08_topology_theory.md)

---

**提示**：本模板为YAML格式，可直接导入CIM建模工具或转换为JSON/RDF格式。建议与BIM模型、P&ID图纸对照使用，确保拓扑准确性。
