# 设备建模模板

**模板 ID**: `CIMU-TEMPLATE-EQUIPMENT-MODELING`
**版本**: v1.0
**最后更新**: 2025-12-07

---

## 模板结构

```yaml
equipment_model:
  # 1. 基本信息
  info:
    equipment_id: "CH-001-A"                    # 设备唯一ID
    equipment_name: "冷水机组-1号"             # 设备名称
    equipment_type: "SCREW_CHILLER"            # 设备类型枚举
    manufacturer: "York"                        # 制造商
    model_number: "YK-1055"                     # 型号
    serial_number: "SN-2024-001"                # 序列号
    installation_date: "2024-03-15"             # 安装日期
    warranty_until: "2027-03-15"                # 质保到期

  # 2. 分类信息
  classification:
    system_category: "HVAC"                     # 系统大类
    system_subcategory: "CHILLED_WATER_PLANT"  # 子系统
    asset_class: "CRITICAL"                     # 资产等级: CRITICAL/IMPORTANT/GENERAL
    life_safety: false                          # 是否生命支持设备

  # 3. 技术参数
  specifications:
    capacity:
      nominal_cooling_kw: 1055                  # 额定制冷量
      input_power_kw: 185                       # 输入功率
      cop: 5.7                                  # 性能系数
      iplv: 6.8                                 # 综合部分负荷性能

    operating_conditions:
      chilled_water:
        supply_temp_c: 7                        # 供水温度
        return_temp_c: 12                       # 回水温度
        flow_rate_m3h: 180                      # 流量
      condenser_water:
        supply_temp_c: 32
        return_temp_c: 37
        flow_rate_m3h: 220
      refrigerant:
        type: "R134a"                           # 制冷剂类型
        charge_kg: 450                          # 充注量

    physical:
      dimensions:
        length_mm: 4500
        width_mm: 1800
        height_mm: 2300
      weight_kg: 8500
      sound_level_db: 75                        # 噪音水平

  # 4. 性能特性
  performance:
    part_load_efficiency:
      - load_percent: 25
        cop: 4.2
      - load_percent: 50
        cop: 5.5
      - load_percent: 75
        cop: 6.1
      - load_percent: 100
        cop: 5.7

    degradation:
      annual_efficiency_loss: 0.02             # 年衰减率
      major_overhaul_interval_years: 8        # 大修周期

  # 5. 连接关系
  relationships:
    component_of:
      system_id: "HVAC-CHP-001"                # 所属系统
    located_in:
      space_id: "BLDG01-L3-MECHROOM-01"       # 所在空间
    connected_to:
      - equipment_id: "CHWP-001-A"             # 冷冻水泵
        connection_type: "CHILLED_WATER_SUPPLY"
      - equipment_id: "CWP-001-A"              # 冷却水泵
        connection_type: "CONDENSER_WATER_SUPPLY"
      - equipment_id: "CT-001-A"               # 冷却塔
        connection_type: "CONDENSER_WATER_RETURN"
      - equipment_id: "MDB-3F-01"              # 配电柜
        connection_type: "POWER_FEED"

  # 6. 控制接口
  control_points:
    analog_inputs:
      - point_id: "CH-001-T-SUPPLY"
        description: "冷冻水供水温度"
        unit: "°C"
        range: [0, 20]
        accuracy: 0.5
      - point_id: "CH-001-T-RETURN"
        description: "冷冻水回水温度"
        unit: "°C"
        range: [5, 25]
        accuracy: 0.5
      - point_id: "CH-001-P-EVAP"
        description: "蒸发压力"
        unit: "kPa"
        range: [200, 600]

    analog_outputs:
      - point_id: "CH-001-SPT-TEMP"
        description: "冷冻水温度设定"
        unit: "°C"
        range: [5, 10]
      - point_id: "CH-001-CAPACITY"
        description: "容量控制"
        unit: "%"
        range: [0, 100]

    binary_inputs:
      - point_id: "CH-001-STATUS"
        description: "运行状态"
        value_map: {0: "停止", 1: "运行"}
      - point_id: "CH-001-FAULT"
        description: "故障信号"
        value_map: {0: "正常", 1: "故障"}

    binary_outputs:
      - point_id: "CH-001-START"
        description: "启停控制"
      - point_id: "CH-001-RESET"
        description: "故障复位"

  # 7. 计量点
  meters:
    - meter_id: "METER-CH-001-PWR"
      meter_type: "ELECTRICITY"
      description: "冷机电表"
      measurements:
        - parameter: "ACTIVE_POWER"
          unit: "kW"
        - parameter: "ENERGY_COUNTER"
          unit: "kWh"

  # 8. 维护计划
  maintenance:
    schedule: "QUARTERLY"                              # 维护周期
    last_service_date: "2025-09-15"
    next_service_date: "2025-12-15"

    service_tasks:
      - task: "更换油过滤器"
        frequency: "QUARTERLY"
        estimated_hours: 1
        spare_parts:
          - part_number: "OF-123"
            quantity: 1
            description: "油过滤器"

      - task: "检查制冷剂压力和泄漏"
        frequency: "QUARTERLY"
        estimated_hours: 0.5

      - task: "清洗冷凝器和蒸发器"
        frequency: "QUARTERLY"
        estimated_hours: 4

      - task: "压缩机大修"
        frequency: "ANNUALLY"
        estimated_hours: 8
        last_performed: "2025-03-20"

  # 9. 故障诊断规则
  fault_diagnosis:
    - fault_code: "HIGH_CONDENSING_PRESSURE"
      description: "冷凝压力过高"
      severity: "HIGH"
      possible_causes:
        - "冷却水流量不足"
        - "冷却塔风机故障"
        - "冷凝器结垢"
        - "制冷剂充注过量"
      check_sequence:
        - step: 1
          action: "检查冷却水泵运行状态"
          expected: "运行正常，流量达到设计值"
        - step: 2
          action: "检查冷却塔风机"
          expected: "风机运行，出风正常"
        - step: 3
          action: "测量冷却水进出温差"
          expected: "温差 < 4K"
        - step: 4
          action: "检查冷凝器换热效果"
          expected: "温差 < 5K"
      solutions:
        - "清洗冷却塔填料"
        - "清洗冷凝器铜管"
        - "排放多余制冷剂"

    - fault_code: "LOW_OIL_PRESSURE"
      description: "油压差过低"
      severity: "HIGH"
      possible_causes:
        - "油过滤器堵塞"
        - "润滑油不足"
        - "油泵故障"
      solutions:
        - "更换油过滤器"
        - "补充润滑油至正常油位"
        - "检查油泵及电路"

  # 10. 运行限制
  operational_constraints:
    min_on_time_minutes: 15                         # 最短运行时间 (保护压缩机)
    min_off_time_minutes: 20                        # 最短停机时间
    max_starts_per_hour: 3                          # 每小时最大启停次数

    low_temp_protection:
      enabled: true
      setpoint_c: 2                                 # 蒸发器防冻

    high_pressure_protection:
      enabled: true
      setpoint_kpa: 2000                            # 高压保护设定

  # 11. 成本信息
  costs:
    purchase_price_rmb: 2_800_000                  # 采购价
    installation_cost_rmb: 150_000                # 安装费
    annual_operating_cost_rmb: 450_000            # 年运行费用 (电费)
    annual_maintenance_cost_rmb: 30_000           # 年维护费

  # 12. 文档关联
  documents:
    - type: "产品样本"
      filename: "YK-1055-Catalog.pdf"
      version: "2024"
    - type: "安装手册"
      filename: "YK-1055-Installation-Manual.pdf"
    - type: "操作手册"
      filename: "YK-1055-Operation-Manual.pdf"
    - type: "维护手册"
      filename: "YK-1055-Maintenance-Manual.pdf"

  # 13. 图片/附件
  attachments:
    - type: "设备照片"
      filename: "CH-001-photo.jpg"
      description: "设备安装完成照片"
    - type: "铭牌照片"
      filename: "CH-001-nameplate.jpg"
      description: "设备铭牌信息"
    - type: "P&ID图纸"
      filename: "HVAC-CHP-PID-001.dwg"

  # 14. 变更历史
  changelog:
    - version: "1.0"
      date: "2024-03-15"
      author: "安装工程师"
      changes: "设备安装完成，记录初始参数"
    - version: "1.1"
      date: "2024-12-10"
      author: "运维工程师"
      changes: "首次年度维护，更新油过滤器"

  # 15. 验证签名
  verification:
    installer: "赵工 (York)"
    acceptance_date: "2024-03-20"
    status: "ACCEPTED"
```

---

## 设备类型枚举

**HVAC 主要设备**:
- `SCREW_CHILLER`: 螺杆式冷机
- `CENTRIFUGAL_CHILLER`: 离心式冷机
- `CHILLED_WATER_PUMP`: 冷冻水泵
- `CONDENSER_WATER_PUMP`: 冷却水泵
- `COOLING_TOWER`: 冷却塔
- `AHU`: 空调机组
- `MAU`: 新风机组
- `FCU`: 风机盘管
- `VAV_BOX`: 变风量末端
- `BOILER`: 锅炉
- `HEAT_EXCHANGER`: 换热器

**电气设备**:
- `TRANSFORMER`: 变压器
- `GENERATOR`: 发电机
- `UPS`: 不间断电源
- `SWITCHGEAR`: 开关柜

**医疗设备**:
- `MEDICAL_OXYGEN_STATION`: 氧气站
- `AIR_COMPRESSOR`: 空压机
- `VACUUM_PUMP`: 负压泵

---

## 使用说明

**新建设备时**:

1. **选择模板**: 从模板库选择最接近的设备类型
2. **复制修改**: 复制模板，修改设备ID、名称
3. **填写实际参数**: 填写实际铭牌参数
4. **拍照存档**: 拍摄设备、铭牌照片
5. **审核验证**: 技术主管审核

**批量导入**:
```python
template = load_template("EQUIP-CHILLER-SCREW.yaml")

equipments = [
    {"id": "CH-001", "name": "冷水机-1号"},
    {"id": "CH-002", "name": "冷水机-2号"},
    {"id": "CH-003", "name": "冷水机-3号"},
]

for eq in equipments:
    config = deepcopy(template)
    config['equipment_id'] = eq['id']
    config['equipment_name'] = eq['name']
    cim_client.create_equipment(config)
```

---

## 常见问题

**Q: 模板参数不全怎么办？**

A: 分情况处理:
- 运行中设备: 查询 BMS 历史数据
- 新设备: 查产品样本、联系厂家
- 缺失: 先用典型值，标记为"待补充"

**Q: 如何确定控制点？**

A: 参考:
- 设备操作手册
- 点位表
- 控制系统图纸
- 现场实物核对

**Q: 不同类型设备能否用同一模板？**

A: 可以继承:
```yaml
# 螺杆机模板 (基础)
# 离心机模板 (扩展，增加部分属性)
equipment_model:
  extends: "SCREW_CHILLER_BASE"
  additional_specs:
    guide_vane_control: true
    surge_protection: true
```

---

*"设备是系统的原子，精确的设备建模是CIM成功的基础。"*
