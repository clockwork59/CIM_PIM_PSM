# 空间定义模板

**模板 ID**: `CIMU-TEMPLATE-SPACE-DEFINITION`
**版本**: v1.0
**最后更新**: 2025-12-07

---

## 模板结构

```yaml
space_definition:
  # 1. 基本信息
  info:
    space_id: "SP-001"                    # 空间唯一标识
    space_name: "内科诊室-301"           # 空间名称
    space_type: "MEDICAL_CONSULTING"    # 空间类型枚举
    space_level: 4                       # 层级: 4=Room
    space_category: "MEDICAL"            # 类别: MEDICAL/SUPPORT/PUBLIC
    parent_space: "BLDG01-L3-ZMED"       # 父级空间ID

  # 2. 物理属性
  physical:
    area_m2: 20                          # 面积 (平方米)
    volume_m3: 64                        # 体积 (立方米 = area × height)
    ceiling_height_m: 3.2                # 层高
    floor_type: "ANTI_BACTERIAL"         # 地板类型
    wall_type: "ANTI_BACTERIAL_PAINT"    # 墙面类型

  # 3. 功能属性
  functional:
    occupancy_max: 6                    # 最大容纳人数
    occupancy_typical: 4                # 典型使用人数
    usage_hours:                        # 使用时段
      start: "08:00"
      end: "17:00"
    usage_days: ["MON", "TUE", "WED", "THU", "FRI"]  # 使用日期

  # 4. 环境要求
  environmental:
    temperature:
      setpoint_cooling: 24              # 夏季设定温度 (°C)
      setpoint_heating: 22              # 冬季设定温度 (°C)
      tolerance: ±1                     # 允许偏差
    humidity:
      setpoint: 50                      # 设定湿度 (%RH)
      tolerance_min: 45                 # 最低允许湿度
      tolerance_max: 60                 # 最高允许湿度
    air_quality:
      fresh_air_rate: 100               # 新风量 (m³/h)
      air_changes: 3                    # 换气次数 (ACH)
    pressure:
      relationship: "POSITIVE"          # 相对关系: POSITIVE/NEGATIVE/EQUAL
      value_pa: 5                       # 压差值 (Pa)

  # 5. 机电需求
  mep_requirements:
    hvac:
      system_type: "FCU+OA"             # HVAC系统类型
      capacity_kw: 8                    # 制冷/制热需求 (kW)
      equipment:
        - "FCU-301"                     # 设备ID列表
        - "D-301-01"                    # 散流器

    electrical:
      power_category: "NORMAL"          # 供电类别: NORMAL/EMERGENCY/LIFE_SAFETY
      estimated_load_kw: 2              # 估算负荷 (照明+设备)
      outlet_count: 8                   # 插座数量
      special_equipment:
        - name: "电脑"
          power_kw: 0.5
        - name: "医疗设备"
          power_kw: 1.5

    lighting:
      illuminance_lux: 300              # 照度标准 (勒克斯)
      lighting_type: "LED_PANEL"        # 灯具类型
      fixture_count: 4                  # 灯具数量

    medical_gas:
      required_gases: ["OXYGEN"]        # 需要气体: OXYGEN/AIR/VACUUM
      outlet_count:
        oxygen: 1

  # 6. 负荷计算
  load_calculation:
    internal:
      people_sensible_kw: 0.4           # 人员显热 (4人 × 100W)
      people_latent_kw: 0.2            # 人员潜热
      lighting_kw: 0.1                 # 照明负荷 (4 × 25W)
      equipment_kw: 2.0                # 设备负荷

    external:
      solar_gain_kw: 0.5               # 太阳辐射得热
      conductive_gain_kw: 0.3          # 围护结构传热

    total:
      cooling_kw: 3.4                  # 总冷负荷
      heating_kw: 1.2                  # 总热负荷

  # 7. 关联资源
  resources:
    equipment:
      - type: "FCU"
        count: 1
      - type: "DIFFUSER"
        count: 2
      - type: "RETURN_GRILLE"
        count: 1

    furniture:
      - type: "DESK"
        count: 2
      - type: "CHAIR"
        count: 4
      - type: "EXAM_TABLE"
        count: 1

  # 8. 特殊要求
  special_requirements:
    accessibility: true                # 无障碍要求
    noise_level_nc: 35                 # 噪音标准 (NC值)
    acoustic_treatment: true           # 声学处理

  # 9. 合规标准
  compliance:
    gb51039: true                      # 综合医院建筑设计规范
    ashrae170: false                   # 是否医疗设施 (默认false)
    gb50736: true                      # 民用建筑供暖通风与空气调节

  # 10. 模型关联
  bim_correlation:
    ifc_space_guid: "2QRJSY$9L6oB7KJw4"  # IFC空间GlobalId
    revit_element_id: "1234567"        # Revit元素ID

  # 11. 变更历史
  changelog:
    - version: "1.0"
      date: "2025-12-07"
      author: "李工"
      changes: "初始版本"

  # 12. 验证签名
  verification:
    designer: "张工"
    reviewer: "王工"
    date: "2025-12-08"
    status: "APPROVED"
```

---

## 空间类型枚举

**医疗空间**:
- `OPERATING_ROOM`: 手术室
- `ICU`: ICU病房
- `ISOLATION_ROOM`: 隔离病房
- `PATIENT_ROOM`: 普通病房
- `CONSULTING_ROOM`: 诊室
- `TREATMENT_ROOM`: 治疗室
- `EXAM_ROOM`: 检查室
- `EMERGENCY_ROOM`: 急诊室

**辅助空间**:
- `NURSE_STATION`: 护士站
- `MEDICATION_ROOM`: 配药室
- `CLEANING_ROOM`: 处置室
- `STORAGE`: 库房
- `TOILET`: 卫生间

**公共空间**:
- `LOBBY`: 门厅
- `WAITING_ROOM`: 候诊区
- `CORRIDOR`: 走廊
- `ELEVATOR_HALL`: 电梯厅

---

## 使用说明

**填写步骤**:

1. **信息采集**: 从设计图纸提取面积、层高
2. **规范查询**: 查询 GB 50736、GB 51039 等标准
3. **负荷计算**: 使用负荷计算软件
4. **参数填写**: 逐项填写模板
5. **审核确认**: 设计师审核签字

**Excel 批量导入**:
```python
import pandas as pd
from cim_sdk import Space

df = pd.read_excel('spaces.xlsx')

for _, row in df.iterrows():
    space = Space(
        space_id=row['space_id'],
        space_name=row['space_name'],
        area_m2=row['area_m2'],
        # ... 其他字段
    )
    cim_client.create_space(space)
```

---

## 常见问题

**Q: 如何估算设备负荷？**

A: 参考标准:
- 电脑: 0.2-0.3 kW
- 打印机: 0.5-1.0 kW
- 医疗设备: 查产品样本或 1-3 kW

**Q: 新风量如何计算？**

A: 按 GB 50736:
- 诊室: 2-3 ACH 或 30 m³/h·人
- 手术室: 15 ACH (全新风部分)

---

*"空间是机电系统服务的对象，精确的空间定义是CIM建模的基础。"*
