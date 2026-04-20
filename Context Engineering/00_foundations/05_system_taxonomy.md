# 医疗建筑系统分类体系

**文档 ID**: `CIMU-FOUND-05-TAXONOMY`
**版本**: v1.0
**最后更新**: 2025-12-07

---

## 目录

1. [分类原则](#分类原则)
2. [五大主系统](#五大主系统)
3. [系统详细分类](#系统详细分类)
4. [编码规则](#编码规则)
5. [应用示例](#应用示例)

---

## 分类原则

### 原则 1：功能完整性
每个系统应能独立完成一项完整的功能。

### 原则 2：边界清晰性
系统之间耦合度尽量低，接口明确。

### 原则 3：符合行业标准
参考 ASHRAE、ASHPE、NFPA 等行业标准。

### 原则 4：便于管理
便于运行维护、能耗计量、故障诊断。

---

## 五大主系统

```
医疗建筑系统
├── HVAC (暖通空调系统)
├── PLUMBING (给排水系统)
├── ELECTRICAL (电气系统)
├── AUTOMATION (智能化系统)
└── MEDICAL_GAS (医疗气体系统)
```

---

## 系统详细分类

### 1. HVAC 系统 (暖通空调系统)

#### 1.1 冷源系统 (CHP - Chilled Water Plant)
**功能**: 生产冷冻水

**主要设备**:
- 冷水机组 (Chiller)
- 冷冻水泵 (Chilled Water Pump)
- 冷却水泵 (Condenser Water Pump)
- 冷却塔 (Cooling Tower)
- 板式换热器 (Plate Heat Exchanger)

**关键参数**:
- 制冷量 (kW)
- 供水温度 (°C)
- 回水温度 (°C)
- 流量 (m³/h)

#### 1.2 热源系统 (HWP - Hot Water Plant)
**功能**: 生产热水

**主要设备**:
- 锅炉 (Boiler)
- 热水泵 (Hot Water Pump)
- 换热器 (Heat Exchanger)
- 热回收装置 (Heat Recovery)

**关键参数**:
- 制热量 (kW)
- 供水温度 (°C)
- 回水温度 (°C)
- 工作压力 (MPa)

#### 1.3 空气处理系统 (AHU - Air Handling Units)
**功能**: 处理空气（制冷、制热、加湿、除湿、净化）

**分类**:
- MAU (Make-up Air Unit): 新风机组
- AHU (Air Handling Unit): 空调机组
- FAU (Fresh Air Unit): 新风处理机
- PAU (Pre-conditioned Air Unit): 预冷空调机组

**主要设备**:
- 风机 (Fan)
- 盘管 (Coil: 冷盘管/热盘管)
- 过滤器 (Filter)
- 加湿器 (Humidifier)

#### 1.4 洁净空调系统 (Clean HVAC)
**功能**: 为洁净区域提供洁净空气

**应用区域**:
- 手术室 (Operating Room)
- ICU (Intensive Care Unit)
- 无菌病房 (Sterile Ward)
- 中心供应室 (Central Sterile Supply)

**关键要求**:
- 洁净度 (ISO Class 5-8)
- 换气次数 (ACH: Air Changes per Hour)
- 压差控制 (+5Pa ~ +15Pa)
- 温湿度精确控制 (±1°C, ±5%RH)

**主要设备**:
- 洁净 AHU (Clean AHU)
- HEPA 过滤器 (High Efficiency Particulate Air Filter)
- 层流送风装置 (Laminar Flow Diffuser)
- 压差传感器 (Differential Pressure Sensor)

#### 1.5 末端设备 (Terminal Units)
**功能**: 房间级别的空调末端

**类型**:
- FCU (Fan Coil Unit): 风机盘管
- VAV Box (Variable Air Volume): 变风量末端
- CAV Box (Constant Air Volume): 定风量末端
- 散热器 (Radiator)
- 地板采暖 (Floor Heating)

#### 1.6 排风系统 (Exhaust System)
**功能**: 排出室内污浊空气

**类型**:
- 一般排风 (General Exhaust)
- 卫生间排风 (Toilet Exhaust)
- 厨房排风 (Kitchen Exhaust)
- 设备用房排风 (Equipment Room Exhaust)
- 负压隔离病房排风 (Negative Pressure Isolation Exhaust)

#### 1.7 特殊空调系统 (Special HVAC)
**功能**: 满足特殊环境需求

**类型**:
- 精密空调 (Precision AC): 用于 IT 机房
- 恒温恒湿空调 (Constant Temp & Humidity): 用于实验室
- 防腐空调 (Corrosion-resistant AC): 用于检验科
- 防爆空调 (Explosion-proof AC): 用于危险品仓库

---

### 2. PLUMBING 系统 (给排水系统)

#### 2.1 生活给水系统 (Domestic Cold Water)
**功能**: 提供生活用冷水

**主要设备**:
- 生活水泵 (Domestic Water Pump)
- 水箱/水池 (Water Tank)
- 变频供水设备 (Variable Frequency Water Supply)
- 减压阀 (Pressure Reducing Valve)
- 紫外线消毒器 (UV Sterilizer)

**水质要求**: 符合 GB 5749《生活饮用水卫生标准》

#### 2.2 热水系统 (Hot Water System)
**功能**: 提供生活用热水

**主要设备**:
- 热水器 (Water Heater)
- 热水循环泵 (Hot Water Circulation Pump)
- 热交换器 (Heat Exchanger)
- 膨胀罐 (Expansion Tank)

**供应温度**: 60°C (防烫伤) or 50°C (常规)

#### 2.3 排水系统 (Drainage System)
**功能**: 收集和排出废水

**类型**:
- 污水系统 (Sewage): 卫生间排水
- 废水系统 (Waste Water): 洗手盆、淋浴排水
n- 雨水系统 (Storm Water): 屋面雨水

**主要设备**:
- 污水提升泵 (Sewage Lift Pump)
- 隔油池 (Grease Trap)
- 化粪池 (Septic Tank)
- 污水处理设备 (Sewage Treatment)

#### 2.4 特殊水系统 (Special Water)
**功能**: 医疗或特殊工艺用水

**类型**:
- 纯水系统 (Purified Water): 用于检验科、制剂室
- 蒸馏水系统 (Distilled Water): 用于消毒供应中心
- 酸性氧化电位水 (Electrolyzed Oxidizing Water): 用于内镜清洗
- 软化水系统 (Softened Water): 用于锅炉、冷水机组

---

### 3. ELECTRICAL 系统 (电气系统)

#### 3.1 供配电系统 (Power Distribution)
**功能**: 提供电力供应

**分类**:
- 高压系统 (High Voltage): 10kV or 35kV
- 低压系统 (Low Voltage): 380V/220V

**主要设备**:
- 变压器 (Transformer)
- 高压开关柜 (HV Switchgear)
- 低压开关柜 (LV Switchgear)
- 母线槽 (Busway)
- 配电箱 (Distribution Board)

#### 3.2 应急电源系统 (Emergency Power)
**功能**: 保障生命安全负荷的供电

**生命安全负荷包括**:
- 手术室、ICU 设备
- 消防系统
- 应急照明
- 重要医疗设备

**主要设备**:
- 柴油发电机 (Diesel Generator)
- UPS (Uninterruptible Power Supply)
- EPS (Emergency Power Supply)
- ATS (Automatic Transfer Switch)

**要求**: 切换时间 ≤ 10s (医疗建筑)

#### 3.3 照明系统 (Lighting System)
**功能**: 提供室内外照明

**分类**:
- 一般照明 (General Lighting)
- 应急照明 (Emergency Lighting)
- 医疗照明 (Medical Lighting): 手术室无影灯
- 景观照明 (Landscape Lighting)

**主要设备**:
- 照明配电箱 (Lighting DB)
- 智能照明控制器 (Smart Lighting Controller)
- LED 灯具 (LED Luminaires)

#### 3.4 智能化系统 (Smart Systems)
**功能**: 智能化控制与管理

**子系统**:
- 楼宇自控系统 (BAS - Building Automation System)
- 能源管理系统 (EMS - Energy Management System)
- 智能照明系统
- 智能安防系统 (门禁、监控)

**主要设备**:
- DDC 控制器 (Direct Digital Controller)
- 传感器 (温度、湿度、CO2、光照)
- 执行器 (阀门、风门执行器)
- 网关 (Gateway)

#### 3.5 医疗设备配电 (Medical Equipment Power)
**功能**: 为医疗设备供电

**特殊要求**:
- 医疗 IT 系统 (Medical IT System): 防微电击
- 隔离电源 (Isolated Power)
- 漏电保护 (RCD - Residual Current Device)
- 接地系统 ( grounding system )

---

### 4. AUTOMATION 系统 (智能化系统)

#### 4.1 楼宇自控系统 (BAS)
**功能**: 自动化控制建筑设备

**监控范围**:
- HVAC 设备 (冷机、水泵、AHU、FCU)
- 给排水设备 (水泵、水箱)
- 电气设备 (发电机、变压器)
- 照明系统
- 电梯系统

**主要设备**:
- 中央监控站 (Central Monitoring Station)
- DDC 控制器 (DDC Controller)
- 传感器网络 (Sensor Network)
- 通信网络 (BACnet/Modbus/LonWorks)

#### 4.2 能源管理系统 (EMS)
**功能**: 监测、分析、优化能源使用

**主要功能**:
- 能耗监测 (Energy Consumption Monitoring)
- 能效分析 (Efficiency Analysis)
- 负荷预测 (Load Forecasting)
- 优化控制 (Optimization Control)

**主要设备**:
- 能源数据采集器 (Energy Data Logger)
- 智能电表 (Smart Meter)
- 能耗分析软件 (Energy Analysis Software)

#### 4.3 环境监测系统 (Environmental Monitoring)
**功能**: 监测室内环境质量

**监测参数**:
- 温度、湿度
- CO2 浓度
- PM2.5/PM10
- 压差 (洁净区域)
- 照度

#### 4.4 安全防范系统 (Security System)
**功能**: 保障建筑安全

**子系统**:
- 视频监控 (CCTV)
- 门禁控制 (Access Control)
- 防盗报警 (Intrusion Detection)
- 电子巡更 (Guard Tour)

---

### 5. MEDICAL_GAS 系统 (医疗气体系统)

#### 5.1 中心供氧系统 (Central Oxygen Supply)
**功能**: 提供医用氧气

**主要设备**:
- 氧气汇流排 (Oxygen Manifold)
- 液氧储罐 (Liquid Oxygen Tank)
- 氧气压缩机 (Oxygen Compressor)
- 区域阀门箱 (Zone Valve Box)
- 氧气终端 (Oxygen Outlet)

**供应压力**: 0.4 ~ 0.6 MPa

#### 5.2 压缩空气系统 (Compressed Air)
**功能**: 提供医疗用压缩空气

**主要设备**:
- 空压机 (Air Compressor)
- 储气罐 (Air Receiver)
- 干燥机 (Dryer)
- 过滤器 (Filter)
- 压缩空气终端 (Compressed Air Outlet)

**供应压力**: 0.6 ~ 0.8 MPa

#### 5.3 负压吸引系统 (Vacuum System)
**功能**: 提供负压吸引

**主要设备**:
- 负压泵 (Vacuum Pump)
- 储气罐 (Vacuum Tank)
- 负压终端 (Vacuum Outlet)

**负压值**: -0.04 ~ -0.09 MPa (表压)

#### 5.4 特殊气体系统 (Special Medical Gases)
**功能**: 提供特殊医疗气体（根据需求）

**类型**:
- 笑气 (N2O): 麻醉
- 氮气 (N2): 仪器驱动
- 二氧化碳 (CO2): 腹腔镜
- 氩气 (Ar): 手术

---

## 编码规则

### 系统 ID 格式

```
系统ID: CATEGORY-SUBSYSTEM-NUMBER

CATEGORY:
  - HVAC: 暖通空调
  - PLM: 给排水
  - ELE: 电气
  - AUT: 智能化
  - GAS: 医疗气体

SUBSYSTEM (示例):
  - CHP: Chilled Water Plant (冷源)
  - HWP: Hot Water Plant (热源)
  - AHU: Air Handling Unit (空气处理)
  - CWV: Clean HVAC (洁净空调)
  - DCW: Domestic Cold Water (生活给水)
  - DHW: Domestic Hot Water (生活热水)
  - POW: Power Distribution (配电)
  - EPR: Emergency Power (应急电源)
  - BAS: Building Automation System (楼控)
  - EMS: Energy Management System (能源管理)
  - OXY: Medical Oxygen (医用氧气)
  - AIR: Medical Compressed Air (医疗空气)
  - VAC: Medical Vacuum (医疗负压)

NUMBER: 3位数字，如 001, 002
```

**示例**:
- `HVAC-CHP-001`: 1号冷冻水系统
- `PLM-DCW-001`: 1号生活给水系统
- `ELE-POW-001`: 1号配电系统
- `GAS-OXY-001`: 1号氧气系统

### 设备 ID 格式

```
设备ID: TYPE-LOCATION-NUMBER

TYPE (设备类型):
  - CH: Chiller (冷水机组)
  - CHWP: Chilled Water Pump (冷冻水泵)
  - CWP: Condenser Water Pump (冷却水泵)
  - CT: Cooling Tower (冷却塔)
  - AHU: Air Handling Unit (空调机组)
  - FCU: Fan Coil Unit (风机盘管)
  - VAV: Variable Air Volume (变风量末端)
  - WP: Water Pump (水泵)
  - BL: Boiler (锅炉)
  - TR: Transformer (变压器)
  - GEN: Generator (发电机)
  - DDC: Direct Digital Controller (DDC控制器)
  - OX: Oxygen Equipment (氧气设备)

LOCATION: 位置编码，如 3F (3楼), B1 (地下1层)
NUMBER: 2位数字，如 01, 02
```

**示例**:
- `CH-3F-01`: 3楼1号冷机
- `AHU-3F-01`: 3楼1号空调机组
- `WP-B1-01`: 地下1层1号水泵

---

## 应用示例

### 示例 1: 手术室空调系统

```yaml
系统: HVAC-CWV-001
名称: "手术室洁净空调系统"
服务范围: ["OR-301", "OR-302", "OR-303"]

设备清单:
  - MAU-3F-01 (新风机组)
  - AHU-3F-01 (循环空调机组)
  - HEPA-3F-01..06 (高效过滤器)
  - VAV-301..303 (变风量末端)
  - SUP-DIFF-301..303 (送风装置)
  - RET-GRILLE-301..303 (回风口)

关键参数:
  洁净度: "ISO Class 5"
  换气次数: "20 ACH"
  温度: "21 ± 1°C"
  湿度: "50 ± 5% RH"
  压差: "+10 Pa (相对走廊)"
```

### 示例 2: 医疗气体系统

```yaml
系统: GAS-OXY-001
名称: "中心供氧系统"
服务楼层: ["L3", "L4", "L5"]

主要设备:
  - OX-SOURCE-01 (液氧储罐, 5m³)
  - OX-MANIFOLD-01 (氧气汇流排, 10瓶)
  - OX-REDUCER-01 (减压阀)
  - ZVB-L3-01..03 (3楼层区域阀门箱)
  - OX-OUTLET-L3-01..30 (30个氧气终端)

设计参数:
  供应压力: "0.6 MPa"
  使用压力: "0.4 MPa"
  流量: "100 L/min (每个终端)"
  纯度: "≥ 99.5%"
```

---

## 小结

医疗建筑系统分类体系是 CIM 建模的基础，通过标准化的分类和编码，实现：

1. **统一语言**: 所有参与方使用相同的术语
2. **快速识别**: 通过系统 ID 快速了解系统功能
3. **数据关联**: 便于系统间数据关联与分析
4. **知识积累**: 建立可复用的系统模板

**下一步**: 根据分类体系，为每个系统定义详细的属性模型和拓扑结构。

---

## 参考标准

- ASHRAE Handbook: HVAC Systems and Equipment
- ASHRAE 170: Ventilation of Health Care Facilities
- GB 51039: 综合医院建筑设计规范
- GB 50736: 民用建筑供暖通风与空气调节设计规范

---

*"分类是认知世界的第一步。清晰的分类体系是构建 CIM 模型的坚实基础。"*
