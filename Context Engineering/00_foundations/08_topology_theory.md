# 拓扑网络理论：机电系统的图论表达

**文档 ID**: `CIMU-FOUND-08-TOPOLOGY`
**版本**: v1.0
**最后更新**: 2025-12-07

---

## 概述

拓扑网络理论将机电系统抽象为图（Graph）结构，通过节点（Node）和边（Edge）描述系统的连接关系。这是 CIM 模型的核心数学基础，支持路径分析、连通性检查、故障传播模拟等高级应用。

---

## 图论基础

### 基本概念

**图 (Graph)**:
```
G = (V, E)
V: 节点集合 (Vertices)
E: 边集合 (Edges)
```

**有向图 vs 无向图**:
- **有向图**: 边有方向，用于描述单向流动（如供水、供电）
- **无向图**: 边无方向，用于描述双向关系（如通信、连通性）

**加权图 (Weighted Graph)**:
每条边有权重，表示：
- 管道长度 (m)
- 设备容量 (kW)
- 流动阻力 (kPa)

---

## 节点类型

### 1. 源节点 (Source Node)
**定义**: 物质的产生点或能量的输入点

**特征**:
- 只有输出，没有输入（或有外部输入）
- 代表能源或介质源头

**示例**:
```yaml
节点ID: "HVAC-CHP-SOURCE-001"
名称: "冷水机组-001"
类型: "CHILLER"
额定容量: 1055 kW
输出功率: 185 kW (电输入)
COP: 5.7
输出介质: "CHW" (冷冻水)
输出温度: 7°C
```

**HVAC 系统中的源**:
- 冷水机组 (制冷)
- 锅炉 (制热)
- 冷却塔 (散热)
- 新风入口 (室外空气)

**电气系统中的源**:
- 变压器 (供电)
- 发电机 (应急电源)
- UPS (不间断电源)

### 2. 汇节点 (Sink Node)
**定义**: 物质的消耗点或能量的使用点

**特征**:
- 只有输入，没有输出
- 代表负荷或末端

**示例**:
```yaml
节点ID: "HVAC-FCU-SINK-001"
名称: "风机盘管-3F-08"
类型: "FCU"
服务区域: "ROOM-301 (内科诊室)"
负荷: 8.0 kW (制冷)
空气流量: 1200 m³/h
水流量: 1.4 m³/h
```

**HVAC 系统中的汇**:
- FCU (风机盘管)
- AHU (空气处理机组)
- VAV Box (变风量末端)
- 新风出口 (排风)

**电气系统中的汇**:
- 照明灯具
- 医疗设备
- 电脑、办公设备
- 电动机

### 3. 分配节点 (Distribution Node)
**定义**: 物质或能量的分配、汇集、调节点

**子类型**:

**3.1 分配器 (Splitter)**
```yaml
功能: 1 路输入, N 路输出 (分流)
示例: 分水器 (Header)

节点ID: "HVAC-CHW-HEADER"
名称: "冷冻水分水器"
输入: CHWP-3F-01 (主管)
输出:
  - 支路1 → FCU-3F-01..04
  - 支路2 → FCU-3F-05..08
  - 支路3 → FCU-3F-09..12
  - 支路4 → AHU-3F-01
各支路流量按比例分配
```

**3.2 汇集器 (Junction/Mixer)**
```yaml
功能: N 路输入, 1 路输出 (汇流)
示例: 集水器 (Return Header)

节点ID: "HVAC-CHW-RETURN"
名称: "冷冻水集水器"
输入:
  - 支路1 ← FCU-3F-01..04
  - 支路2 ← FCU-3F-05..08
  - 支路3 ← FCU-3F-09..12
  - 支路4 ← AHU-3F-01
输出: CHW-Return → 冷水机组蒸发器
各支路回水温度混合
```

**3.3 调节器 (Regulator/Adjuster)**
```yaml
功能: 调节流量、压力、温度
示例: 调节阀、三通阀

节点ID: "HVAC-CHW-VLV-301"
名称: "冷冻水调节阀-ROOM301"
输入: 分水器支路 (7°C)
输出: FCU-FCU-3F-08
调节: 根据室温调节开度 (0-100%)
控制信号: AO (0-10V or 4-20mA)
```

**3.4 转换器 (Transformer)**
```yaml
功能: 转换介质形式或能量形式
示例: 换热器、压缩机

节点ID: "HVAC-HX-001"
名称: "板式换热器"
一次侧: 市政热水 (85°C / 60°C)
二次侧: 空调热水 (45°C / 40°C)
换热量: 2000 kW
效率: 95%
```

---

## 边类型

### 1. 主管 (Trunk/Primary)
**特征**:
- 大直径 / 大容量
- 连接到源或主分配节点
- 承担主要流量

**示例**:
- 冷冻水主管: DN250
- 主母线: 2000A
- 主风管: 2000mm x 500mm

### 2. 支管 (Branch/Secondary)
**特征**:
- 中等直径
- 从主管分支
- 服务一个区域

**示例**:
- 冷冻水支管: DN150
- 分支风管: 800mm x 320mm
- 区域配电: 400A 母线

### 3. 末端连接 (Terminal Connection)
**特征**:
- 小直径
- 连接末端设备
- 可变流量 (根据负荷调节)

**示例**:
- FCU 接管: DN20
- VAV Box 柔性风管: φ150mm
- 插座回路: 2.5mm² 电线

---

## 网络拓扑类型

### 1. 串联拓扑 (Series Topology)

```
Source → Node1 → Node2 → Node3 → Sink
            ↓        ↵        ↵
          Serial   Serial   Serial
```

**特征**:
- 单一路径
- 前一个节点的输出是下一个节点的输入
- 任一节点故障，整个系统瘫痪

**示例**: 三级泵系统
```
一次泵 → 冷水机 → 二次泵 → 末端
  (P1)       (CH)       (P2)      (FCU)
```

### 2. 并联拓扑 (Parallel Topology)

```
          → Node1 →
         ↙          ↘
Source →   NodeX   → Sink
         ↘          ↙
          → Node2 →
```

**特征**:
- 多条并行路径
- 流量分配由阻力决定
- 单台设备故障不影响系统
- 便于扩容

**示例**: 多台冷水机组并联
```
冷水主管 → 分水器
            ↓
       ┌----┴----┐
   Chiller-1  Chiller-2  Chiller-3
   1055kW     1055kW     1055kW
       └----┬----┘
            ↓
         集水器 → 冷冻水回水
```

### 3. 环形拓扑 (Loop Topology)

```
    Node1 → Node2
    ↑           ↓
    Node4 ← Node3
     ↘       ↙
      Sink
```

**特征**:
- 闭合回路
- 双向供应，可靠性高
- 水力平衡复杂

**示例**: 环形供水管网
- 市政供水环网
- 消防环网
- 医疗气体环网

### 4. 星形拓扑 (Star Topology)

```
          Node1
         ↗
Source → NodeX
         ↘
          Node2
```

**特征**:
- 中心节点到各终端
- 易于控制和管理
- 中心节点是瓶颈

**示例**: VAV 空调系统
```
AHU (中心)
  ↓
┌──┴──┬──┬──┬──┐
VAV1 VAV2 VAV3 VAV4 VAV5
(各房间末端)
```

### 5. 树形拓扑 (Tree Topology)

```
Source
  ↓
NodeA (分支点)
  ↓
┌──┴──┐
NodeB NodeC (子分支点)
  ↓     ↓
┌┴┐   ┌┴┐
S1 S2 S3 S4 (末端)
```

**特征**:
- 层次化的分支结构
- HVAC 系统最常见
- 从主管到支管再到末端

**示例**: 空调冷冻水系统
```
冷水机 (Source)
  ↓
一次泵
  ↓
分水器 (NodeA)
  ├→ 东区支路 (NodeB)
  │   ├→ FCU-301 (S1)
  │   └→ FCU-302 (S2)
  └→ 西区支路 (NodeC)
      ├→ FCU-303 (S3)
      └→ FCU-304 (S4)
```

---

## 图论在 CIM 中的应用

### 1. 路径分析 (Path Analysis)

**最短路径 (Shortest Path)**
```
应用场景: 寻找两个设备之间的最短连接路径
算法: Dijkstra 算法

示例:
  从 "CH-001" 到 "FCU-301"
  路径1: CH-001 → Header → Branch1 → FCU-301 (长度: 45m)
  路径2: CH-001 → Header → Branch2 → Branch3 → FCU-301 (长度: 67m)
  最短路径: 路径1 (45m)
```

**关键路径 (Critical Path)**
```
应用场景: 寻找影响系统性能的关键路径
（阻力最大、流量最大或重要度最高的路径）

示例: 冷冻水系统
  计算各环路阻力:
  - Loop1: 45 kPa (最远端)
  - Loop2: 38 kPa
  - Loop3: 32 kPa

  关键路径: Loop1 (决定水泵扬程)
```

### 2. 连通性检查 (Connectivity Check)

**检查所有节点是否从源可达**
```python
def check_connectivity(graph, source):
    """检查所有末端节点是否可达"""
    visited = set()

    def dfs(node):
        visited.add(node)
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                dfs(neighbor)

    dfs(source)

    # 检查所有末端节点是否在 visited 中
    all_sinks_connected = all(
        sink in visited
        for sink in graph.sink_nodes()
    )

    return all_sinks_connected
```

**应用场景**: 建模完成后验证拓扑完整性

### 3. 环路检测 (Cycle Detection)

```python
def detect_cycles(graph):
    """检测拓扑中是否有环路"""
    visited = set()
    stack = set()

    def dfs(node):
        visited.add(node)
        stack.add(node)

        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in stack:
                # 发现环路
                return True

        stack.remove(node)
        return False

    for node in graph.nodes():
        if node not in visited:
            if dfs(node):
                return True  # 发现环路

    return False  # 无环路
```

**应用场景**: HVAC冷冻水系统必须无环路（避免短路），但医疗气体环网需要有环路。

### 4. 故障传播分析 (Failure Propagation)

```python
def simulate_failure_impact(graph, failed_node):
    """
    模拟某节点故障的影响范围
    返回受影响的所有下游节点
    """
    affected_nodes = set()

    # BFS 向前搜索
    queue = [failed_node]
    visited = set()

    while queue:
        node = queue.pop(0)
        if node in visited:
            continue
        visited.add(node)
        affected_nodes.add(node)

        # 所有下游节点
        for successor in graph.successors(node):
            queue.append(successor)

    return affected_nodes

# 示例
failed_node = "CHWP-001"  (1号冷冻水泵故障)
affected = simulate_failure_impact(hvac_graph, failed_node)

结果: {
    "CHWP-001",          (故障泵本身)
    "HEADER-CHW",       (分水器 - 流量不足)
    "FCU-301".."FCU-320", (末端 - 流量不足导致供冷不足)
    "AHU-301",          (空调机组 - 流量不足)
    "BLDG01-L3-Z1"      (区域 - 舒适度下降)
}
```

### 5. 冗余路径分析 (Redundancy Analysis)

```python
def find_redundant_paths(graph, source, sink, k=2):
    """
    寻找从源到汇的前 k 条最短路径
    用于分析冗余度
    """
    paths = []

    def dfs(current, target, path, visited):
        if len(paths) >= k:
            return

        if current == target:
            paths.append(path.copy())
            return

        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                dfs(neighbor, target, path, visited)
                path.pop()
                visited.remove(neighbor)

    visited = {source}
    dfs(source, sink, [source], visited)
    return paths

# 示例: 应急电源的冗余供电路径
paths = find_redundant_paths(power_graph, "GEN-001", "OR-301", k=2)

结果:
  Path1: GEN-001 → TSW-01 → MDB-01 → PDB-01 → OR-301
         (主路径，自动切换)

  Path2: GEN-001 → TSW-02 → MDB-02 → PDB-01 → OR-301
         (备用路径，手动切换)

结论: 有两条独立路径，冗余良好
```

### 6. 网络中心性分析 (Centrality Analysis)

```python
from networkx import betweenness_centrality

def find_critical_nodes(graph):
    """
    找出拓扑中的关键节点
    使用介数中心性 (Betweenness Centrality)
    """
    centrality = betweenness_centrality(graph)

    # 按中心性排序
    sorted_nodes = sorted(
        centrality.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_nodes[:10]  # Top 10

# 示例: 冷冻水系统关键性分析
critical_nodes = find_critical_nodes(chw_graph)

结果:
  1. HEADER-CHW: 中心性 0.85 (分水器)
  2. CHWP-001: 中心性 0.72 (1号冷冻水泵)
  3. AHU-EF-01: 中心性 0.68 (急诊空调机组)
  4. OR-301: 中心性 0.65 (手术室301)

建议: 重点监控和保护这些节点
```

---

## 图的可视化

### 1. 层次化布局 (Hierarchical Layout)

```
源节点在上层
  ↓ (垂直流动)
分配层
  ↓
中间节点
  ↓
末端汇节点在下层

适用于: HVAC 水系统、供电系统
```

### 2. 环形布局 (Circular Layout)

```
      Node1
  Node5    Node2
      Node4
  Node4    Node3

中央: 源节点
外围: 汇节点
适用于: 气体环网、网络拓扑
```

### 3. 地理布局 (Geographic Layout)

```
根据实际空间位置布局
节点位置对应 BIM 坐标

适用于: 故障定位、巡检路径规划
```

---

## 拓扑建模最佳实践

### 1. 命名规范

```
节点ID: TYPE-LOCATION-FUNCTION-NUMBER
示例: CHWP-3F-SUPPLY-01
      (冷冻水泵-3F-供水-01号)

边ID: FROM-TO-CONNECTION-TYPE
示例: CHWP01-TOPUMP01-TRUNK
      (从1号泵到分水器-主管)
```

### 2. 属性完整

每个节点应有:
```yaml
基本属性:
  - node_id (唯一)
  - node_name (可读名称)
  - node_type (Source/Sink/Distribution)
  - equipment_id (关联设备)

性能属性:
  - capacity (容量)
  - efficiency (效率)
  - status (运行状态)
  - cost (成本/权重)

关系属性:
  - upstream_nodes (上游节点)
  - downstream_nodes (下游节点)
```

### 3. 避免常见错误

**错误1: 环路遗漏**
```
症状: 流量不足，能耗异常
检查: 用算法验证环路完整性
```

**错误2: 节点孤立**
```
症状: 设备未连接到系统
检查: 连通性分析 (DFS/BFS)
```

**错误3: 流向相反**
```
症状: 有向图出现负流量
检查: 基于物理原理验证流向
```

**错误4: 参数缺失**
```
症状: 优化计算无法进行
检查: 所有节点应有容量、效率等参数
```

---

## 拓扑验证工具

```python
def validate_topology(graph):
    """完整的拓扑验证"""
    errors = []

    # 1. 连通性检查
    if not check_connectivity(graph, graph.source_nodes()[0]):
        errors.append("存在不可达节点")

    # 2. 环路检查 (冷冻水系统不应有环)
    if detect_cycles(graph) and graph.system_type == "CHW":
        errors.append("冷冻水系统存在环路")

    # 3. 节点完整性
    for node in graph.nodes():
        if not node.has_required_attributes():
            errors.append(f"节点 {node.id} 缺少必要属性")

    # 4. 孤点检查
    isolated = [n for n in graph.nodes() if graph.degree(n) == 0]
    if isolated:
        errors.append(f"存在孤立节点: {isolated}")

    return errors

# 应用
topologyErrors = validate_topology(hvac_graph)
if topologyErrors:
    print("拓扑验证失败:", topologyErrors)
else:
    print("拓扑验证通过 ✓")
```

---

## 小结

拓扑网络理论为机电系统提供了:

1. **数学基础**: 图的表示与算法
2. **分析工具**: 路径、连通性、环路检测
3. **故障分析**: 故障传播与影响范围
4. **优化能力**: 关键路径识别与冗余分析
5. **可视化**: 图布局与交互
6. **验证手段**: 拓扑完整性检查

**核心思想**: 将机电系统抽象为图，利用图论算法解决工程问题。

**计算复杂度**: 大多数图算法为 O(V+E)，可处理大型系统。

**下一步**: 基于拓扑分析，进行系统可靠性评估与优化。

---

## 参考资源

- Graph Theory in Network Analysis - IEEE
- NetworkX: Graph Analysis Library
- BIM 拓扑数据: IFC Space Boundary
- 复杂网络理论: Complex Network Theory

---

*"万物皆图。理解拓扑，就是理解系统的骨架。"*
