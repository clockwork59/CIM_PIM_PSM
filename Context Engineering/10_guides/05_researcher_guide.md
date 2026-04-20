# 研究员与分析师指南

**文档 ID**: `CIMU-GUIDE-05-RESEARCHER`
**版本**: v1.0
**最后更新**: 2025-12-07

---

## 面向对象

能源研究员、建筑分析师、运维分析师、数据科学家

---

## 研究框架

```
问题定义 → 数据收集 → 数据分析 → 模型建立 → 验证优化 → 结论输出
     ↓                                                        ↓
CIM提供标准化模型                                    CIM支持仿真验证
```

---

## 数据获取

### 标准API接口

**REST API**:
```python
import requests

# 获取设备数据
response = requests.get('https://cim-api.example.com/api/v1/equipment')
equipment_list = response.json()['data']

# 获取能耗数据
params = {
    'start': '2025-12-01T00:00:00Z',
    'end': '2025-12-31T23:59:59Z',
    'granularity': '1h'
}
energy = requests.get(
    f'https://cim-api.example.com/api/v1/systems/HVAC-CHW-001/energy',
    params=params
)
```

**GraphQL (灵活查询)**:
```python
query = """
query GetOperatingRooms {
  spaces(spaceType: "OPERATING_ROOM") {
    name
    servedBySystems {
      name
      type
      energyConsumption(start: "2025-12-01", end: "2025-12-31") {
        total_kwh
        avg_kw
      }
    }
  }
}
"""

response = requests.post(
    'https://cim-api.example.com/graphql',
    json={'query': query}
)
data = response.json()['data']
```

**Python SDK** (推荐):
```python
from cim_sdk import CIMClient

client = CIMClient(api_key='your-key')

# 设备查询
chillers = client.query(
    entity_type='Equipment',
    filters={'equipment_type': 'CHILLER'}
)

# 时间序列数据
data = client.get_timeseries(
    entity_ids=['CH-001', 'CH-002'],
    parameters=['power_kw', 'cop'],
    start='2025-12-01',
    end='2025-12-31',
    aggregate='1h'
)

# 导出到 DataFrame
df = data.to_dataframe()
```

### 批量导出

**大数据量导出**:
```python
# 分页加载
all_data = []
page = 0
while True:
    response = requests.get(
        url,
        params={'limit': 1000, 'offset': page*1000}
    )
    data = response.json()['data']
    if not data:
        break
    all_data.extend(data)
    page += 1

# 导出到 CSV
pd.DataFrame(all_data).to_csv('export.csv')
```

**增量同步**:
```python
# 记录上次同步时间
last_sync = load_last_sync_time()

# 获取增量数据
delta = client.get_changes(
    since=last_sync,
    entity_types=['Equipment', 'Meter']
)

# 更新本地数据库
update_local_db(delta)

# 保存新的同步时间
save_last_sync_time(delta.latest_timestamp)
```

---

## 数据分析方法

### 描述性分析

**基础统计**:
```python
import pandas as pd
import numpy as np

# 加载数据
df = pd.read_csv('energy_data.csv')

# 描述性统计
desc = df['power_kw'].describe()
print(desc)

# 分组统计
stats = df.groupby('equipment_type').agg({
    'power_kw': ['mean', 'std', 'max'],
    'cop': 'mean'
})
```

**能耗分布分析**:
```python
# 按系统类型统计能耗占比
energy_by_system = df.groupby('system_category')['energy_kwh'].sum()
print("能耗占比:")
print(energy_by_system / energy_by_system.sum() * 100)

# 输出示例:
# HVAC:    65%
# ELECTRICAL: 25%
# PLUMBING:  8%
# OTHER:     2%
```

### 诊断性分析

**故障模式挖掘**:
```python
# 分析故障与参数的关系
from sklearn.association_rules import association_rules

# 准备数据 (告警 + 运行参数)
data = []
for alert in alerts:
    record = {
        'alert_type': alert['type'],
        'temp_high': alert['temp'] > 30,
        'flow_low': alert['flow'] < 80,
        'chiller_fault': alert['chiller_status'] == 'FAULT'
    }
    data.append(record)

# 关联规则
rules = association_rules(pd.DataFrame(data))
print(rules[rules['confidence'] > 0.7])

# 发现: 冷却水流量低 → 冷机高压告警 (置信度 85%)
```

**根因分析**:
```python
# 使用决策树分析故障根因
from sklearn.tree import DecisionTreeClassifier

# 特征
X = df[['temp_supply', 'temp_return', 'flow_rate',
        'pressure_diff', 'outdoor_temp']]

# 标签: 故障类型
y = df['fault_type']

# 训练模型
model = DecisionTreeClassifier(max_depth=4)
model.fit(X, y)

# 输出规则
from sklearn.tree import export_text
print(export_text(model, feature_names=X.columns))

# 规则示例:
# if flow_rate < 100 and pressure_diff > 50:
#    fault = "过滤器堵塞"
```

### 预测性分析

**负荷预测**:
```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# 特征工程
feature_cols = [
    'hour_of_day',         # 时刻
    'day_of_week',         # 星期几
    'outdoor_temp',        # 室外温度
    'outdoor_humidity',    # 室外湿度
    'solar_radiation',     # 太阳辐射
    'occupancy_count',     # 人员数量
    'is_holiday'           # 是否节假日
]

X = df[feature_cols]
y = df['cooling_load_kw']

# 分割数据
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 训练模型
model = RandomForestRegressor(n_estimators=100)
model.fit(X_train, y_train)

# 评估
score = model.score(X_test, y_test)
print(f"预测准确率: {score:.2%}")

# 预测未来24小时
tomorrow = generate_features_for_tomorrow()
prediction = model.predict(tomorrow)
```

**故障预测**:
```python
# 使用时间序列分析预测设备故障
from statsmodels.tsa.statespace.sarimax import SARIMAX

# 振动数据
vibration = df['vibration_mm/s'].values

# 构建时间序列模型
model = SARIMAX(vibration, order=(2,1,2), seasonal_order=(0,1,1,24))
results = model.fit()

# 预测未来趋势
forecast = results.get_forecast(steps=7*24)  # 7天每小时

# 判断是否有异常上升
if forecast.mean()[-1] > threshold:
    print("警告: 预计7天后振动超标，可能发生故障")
```

### 规范性分析

**优化分析**:
```python
from scipy.optimize import minimize

# 目标函数: 最小化总能耗
def total_energy(x):
    ch1_load, ch2_load, ch3_load = x

    # COP 曲线 (负荷率 → COP)
    cop1 = get_cop(ch1_load / 1055)
    cop2 = get_cop(ch2_load / 1055)
    cop3 = get_cop(ch3_load / 1055)

    power = ch1_load/cop1 + ch2_load/cop2 + ch3_load/cop3
    return power

# 约束
constraints = [
    {'type': 'eq', 'fun': lambda x: x[0] + x[1] + x[2] - 2000},  # 总负荷=2000kW
]
bounds = [(0, 1055), (0, 1055), (0, 1055)]

# 求解
result = minimize(total_energy, [667, 667, 667], bounds=bounds, constraints=constraints)

print(f"优化结果: {result.x}")  # 各台冷机最佳负荷分配
```

---

## 研究案例

### 案例 1: 医院能耗基准分析

**研究问题**: 我院能耗水平在行业中处于什么位置？

**数据集**:
- 10家同类医院 (500床, 区域气候相同)
- 3年历史能耗数据
- 建筑面积、床位数、门诊量

**分析方法**:
```python
# 计算 EUI (Energy Use Intensity)
df['eui'] = df['annual_energy_kwh'] / df['floor_area_m2']

# 分位数分析
percentiles = df['eui'].quantile([0.25, 0.5, 0.75])
print(f"行业 EUI 分布:")
print(f"Q1 (前25%): {percentiles[0.25]}")
print(f"中位数: {percentiles[0.5]}")
print(f"Q3 (前75%): {percentiles[0.75]}")

# 我院位置
my_hospital_eui = 95
if my_hospital_eui < percentiles[0.25]:
    print("我院属于优秀 (Top 25%)")
elif my_hospital_eui < percentiles[0.5]:
    print("我院属于良好 (Top 50%)")
else:
    print("我院需要改进 (Bottom 50%)")

# 回归分析: 影响因素
from sklearn.linear_model import LinearRegression

X = df[['bed_count', 'outpatient_per_year', 'climate_zone']]
y = df['eui']

model = LinearRegression()
model.fit(X, y)

print("影响因素权重:")
for feature, coef in zip(X.columns, model.coef_):
    print(f"  {feature}: {coef:.2f}")
```

**研究发现**:
- 我院 EUI = 95 kWh/m²/y
- 行业中位数 = 88 kWh/m²/y
- 我院偏高 8%
- 主要因素: 设备老旧、运行时间长

**改进建议**:
- 冷机更新 (COP 从 3.5 提升到 5.5) → 节能 36%
- 水泵变频改造 → 节能 15%
- 预计总投资 200 万元，年节约 80 万元，回收期 2.5 年

---

### 案例 2: 手术室环境优化

**研究问题**: 手术室温湿度不达标的原因和优化方案

**数据**:
- 5间手术室，3个月环境数据
- 每间 12个传感器 (温度×4, 湿度×4, 压差×4)
- 手术排班、人员进出

**分析方法**:
```python
# 统计达标率
df['temp_ok'] = (df['temp'] >= 21) & (df['temp'] <= 24)
df['rh_ok'] = (df['rh'] >= 45) & (df['rh'] <= 60)
df['overall_ok'] = df['temp_ok'] & df['rh_ok']

compliance_rate = df['overall_ok'].mean()
print(f"综合达标率: {compliance_rate:.2%}")

# 时段分析
hourly_rate = df.groupby(df['timestamp'].hour)['overall_ok'].mean()

# 发现问题点
print(f"最差时段: {hourly_rate.idxmin()}:00 ({hourly_rate.min():.2%})")
print(f"最佳时段: {hourly_rate.idxmax()}:00 ({hourly_rate.max():.2%})")

# 关联因素
correlation = df[['occupancy', 'door_open_duration', 'overall_ok']].corr()
print("关联性分析:")
print(correlation['overall_ok'])

# 发现:
# - 开门时长与达标率负相关 (-0.65)
# - 人员数量与达标率负相关 (-0.43)
```

**优化方案**:
1. 增加缓冲间 (减少开门影响)
2. 提高新风量 (稀释人员热负荷)
3. 优化控制参数 (提前预冷)

**仿真验证**:
```python
# 使用 EnergyPlus 仿真
def simulate(params):
    # 参数: 新风量, 换气次数, 预冷时间
    hvac_config = build_hvac_model(params)
    results = run_energyplus(hvac_config, weather_file)
    return results.compliance_rate

# 网格搜索
best_params = None
best_rate = 0
for ventilation in [15, 18, 20, 22]:
    for pre_cool in [0.5, 1, 1.5, 2]:
        rate = simulate(ventilation=ventilation, pre_cool_hours=pre_cool)
        if rate > best_rate:
            best_rate = rate
            best_params = (ventilation, pre_cool)

print(f"最佳配置: 新风量 {best_params[0]} ACH, 预冷 {best_params[1]}h")
print(f"预计达标率: {best_rate:.2%}")
```

**实施效果**:
- 实施前达标率: 78%
- 实施后达标率: 96%
- 患者感染率下降 (间接效果)

---

## 工具推荐

### 必备工具

1. **Python 生态**
   - Pandas: 数据处理
   - NumPy: 数值计算
   - Scikit-learn: 机器学习
   - Matplotlib/Seaborn: 可视化
   - Jupyter: 交互式分析

2. **专用工具**
   - EnergyPlus: 建筑能耗仿真
   - Tableau/PowerBI: 商业智能
   - Grafana: 时序可视化
   - DBeaver: 数据库管理

3. **CIM 集成**
   - CIM Python SDK: 连接 CIM 模型
   - CIM Exporter: 数据导出
   - CIM Simulator: 场景仿真

---

## 最佳实践

### 1. 数据准备

```python
# 数据质量检查清单
def validate_data(df):
    checks = {
        'missing_rate': df.isnull().mean(),
        'duplicate_rate': df.duplicated().mean(),
        'outlier_rate': detect_outliers(df),
        'time_gap': check_time_continuity(df)
    }

    for check, value in checks.items():
        if value > threshold[check]:
            logging.warning(f"数据质量问题: {check} = {value:.2%}")

    return df.dropna()  # 或填充
df = validate_data(raw_data)
```

### 2. 可重复研究

```python
# 使用 Papermill 参数化 Notebook
import papermill as pm

# 模板 Notebook (template.ipynb)
# 参数: start_date, end_date, building_id

pm.execute_notebook(
    'template.ipynb',
    'output.ipynb',  # 带参数的输出
    parameters=dict(
        start_date='2025-01-01',
        end_date='2025-12-31',
        building_id='BLDG01'
    )
)
```

### 3. 结果验证

```python
# 交叉验证
def cross_validate(model, X, y, cv=5):
    scores = cross_val_score(model, X, y, cv=cv)
    print(f"CV 平均分: {scores.mean():.3f} (+/- {scores.std()*2:.3f})")
    return scores

# 外部验证
# 用 2024 年数据训练，预测 2025 年，对比实际
pred_2025 = model.predict(X_2025)
mape = mean_abs_percentage_error(y_2025, pred_2025)
print(f"外部验证 MAPE: {mape:.2%}")
```

---

## 发表与分享

### 学术发表

**适合期刊**:
- Energy and Buildings
- Building and Environment
- Applied Energy
- 暖通空调 (中文)
- 建筑节能 (中文)

**论文结构**:
1. Introduction (问题描述)
2. Methodology (CIM方法)
3. Case Study (案例研究)
4. Results (结果分析)
5. Discussion (讨论对比)
6. Conclusion (结论)

### 成果共享

**CIM 社区**:
- 提交研究报告
- 分享 Jupyter Notebook
- 贡献分析模板
- 开源算法代码

**模板库**:
```
研究类型/
├── 能耗分析/
│   ├── 模板_按系统分析.ipynb
│   └── 模板_同比环比.ipynb
├── 故障诊断/
│   └── 模板_根因分析.ipynb
├── 负荷预测/
│   └── 模板_时间序列.ipynb
└── 优化研究/
    └── 模板_全局优化.ipynb
```

---

## 技术支持

**获取数据**:
- 联系 CIM 管理员
- API 密钥申请
- 数据使用规范

**技术讨论**:
- CIM 用户论坛
- 每月研究会议
- GitHub Issues

---

## 总结

研究员利用 CIM 模型可以:

1. **快速获取数据**: 标准化接口，无需清洗
2. **专注核心问题**: 无需处理数据格式、单位等琐事
3. **验证更简单**: CIM 提供仿真环境，对比实际
4. **成果可复用**: 模板化研究，他人可重现
5. **知识可积累**: 算法模型可沉淀到 CIM 平台

**核心优势**: 数据就绪 + 工具就绪 + 社区支持

---

**一句话对研究员说**: "CIM 为您提供干净、完整、结构化的研究数据，让您专注于发现洞见，而不是数据清洗。"
