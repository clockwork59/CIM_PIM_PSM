# 数据工程师CIM接入指南

**文档 ID**: `CIMU-GUIDE-03-DATA-ENGINEER`
**版本**: v1.0
**最后更新**: 2025-12-07

---

## 面向对象

数据工程师、数据分析师、数据架构师

---

## 工作流程

```
数据源 → 数据采集 → 数据清洗 → 数据映射 → CIM存储 → 接口开放
                                                              ↓
                                                       应用/BI/ML
```

---

## 数据源梳理

### 常见数据源

| 系统 | 数据源 | 格式 | 频率 | 重要性 |
|-----|--------|------|------|--------|
| BMS | DDC控制器 | BACnet | 10秒 | ★★★★★ |
| EMS | 能源计量表 | Modbus | 1分钟 | ★★★★★ |
| CMMS | 工单系统 | API/DB | 事件触发 | ★★★★☆ |
| BIM | IFC模型 | IFC2x3/4 | 一次性 | ★★★★★ |
| IoT | 传感器 | MQTT | 1秒 | ★★★★☆ |

### 数据类型

**实时数据**:
```
温度、压力、流量、电流、电压、功率、频率、状态
```

**历史数据**:
```
1秒 ~ 5分钟采样，保留 1年
```

**事件数据**:
```
故障报警、工单、维护记录、系统变更
```

**静态数据**:
```
设备清单、点位表、BIM模型、图纸、协议
```

---

## 数据采集

### 协议支持

**1. BACnet (建筑自动化控制网络)**

```python
# 使用 BACpypes 库
from bacpypes.core import run
from bacpypes.app import BIPSimpleApplication
from bacpypes.object import AnalogInputObject

# 读取温度传感器
app = BIPSimpleApplication()

def read_bacnet_point(device_ip, point_id):
    request = ReadPropertyRequest(
        objectIdentifier=point_id,
        propertyIdentifier='presentValue'
    )
    request.pduDestination = device_ip
    response = app.request(request)
    return response.propertyValue

# 批量读取
temps = []
for sensor in sensors:
    value = read_bacnet_point(sensor.ip, sensor.bacnet_id)
    temps.append({
        'sensor_id': sensor.id,
        'timestamp': datetime.now(),
        'value': value
    })
```

**2. Modbus (能源计量)**

```python
# pymodbus
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient('192.168.1.100')

# 读取电表
result = client.read_holding_registers(
    address=0,
    count=2,
    slave=1
)

# 解析 (根据电表协议)
power = (result.registers[0] << 16 | result.registers[1]) * 0.01  # kW
energy = client.read_holding_registers(address=2, count=4, slave=1)
```

**3. OPC UA (工业标准)**

```python
# asyncua
from asyncua import Client
async with Client(url='opc.tcp://192.168.1.100:4840') as client:
    node = client.get_node('ns=2;i=1025')  # 温度测点
    value = await node.read_value()
```

**4. API (工单系统)**

```python
# REST API
def fetch_workorders():
    response = requests.get(
        'https://cmms.example.com/api/v1/workorders',
        params={'status': 'open'},
        headers={'Authorization': 'Bearer Token'}
    )
    return response.json()
```

### 采集架构

```
分布式采集器 (边缘计算)
  ↓
消息队列 (Kafka/RabbitMQ)
  ↓
流处理 (Flink/Spark)
  ↓
时序数据库 (InfluxDB/TimescaleDB)
  ↓
CIM 接口服务
```

**示例**: 实时数据流

```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'bms-sensors',
    bootstrap_servers=['kafka:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    data = message.value
    # 写入 InfluxDB
    influx.write_points([{
        "measurement": "sensor_data",
        "tags": {
            "sensor_id": data['sensor_id'],
            "location": data['location']
        },
        "fields": {
            "value": data['value']
        },
        "time": data['timestamp']
    }])
```

---

## 数据清洗

### 常见问题

**1. 缺失值**
```python
data = [22.5, 22.6, None, 22.7, None, 22.8]

# 处理: 前向填充或插值
cleaned = pd.Series(data).fillna(method='ffill')
```

**2. 异常值**
```python
# 3σ原则
def detect_outliers(series):
    mean = series.mean()
    std = series.std()
    lower = mean - 3 * std
    upper = mean + 3 * std
    return series[(series < lower) | (series > upper)]

# 业务规则
valid_range = (10, 35)  # 室内温度
outliers = data[~data['temp'].between(*valid_range)]
```

**3. 重复值**
```python
df.drop_duplicates(
    subset=['sensor_id', 'timestamp'],
    keep='last'
)
```

**4. 时间戳对齐**
```python
# 统一为 UTC
df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize('UTC')

# 重采样 (对齐到分钟)
df.resample('1T', on='timestamp').mean()
```

### 质量规则

```yaml
质量规则库:
  - 规则ID: R001
    描述: "冷冻水温度范围"
    参数: T_CHW
    有效范围: [5, 15]
    单位: °C
    异常处理: 告警 + 标记

  - 规则ID: R002
    描述: "数据连续性"
    参数: 任意测点
    最大间隔: 300秒
    异常处理: 标记为缺失

  - 规则ID: R003
    描述: "数值变化率"
    参数: T_Room
    最大变化: 5°C/分钟
    异常处理: 平滑处理
```

---

## 数据映射

### 点位表映射

**Excel 点位表**:
```
| 点位编号 | 点位名称 | 设备类型 | 位置 | 协议 | 地址 |
|---------|---------|---------|------|------|------|
| AI-301 | 冷冻水供水温度 | 传感器 | 3F-机房 | BACnet | 192.168.1.100:AI:1 |
| DO-101 | 冷机启停 | 执行器 | 3F-机房 | BACnet | 192.168.1.100:DO:1 |
```

**映射到 CIM**:
```python
# 读取点位表
df = pd.read_excel('point_list.xlsx')

# 映射字典
point_type_map = {
    'AI': 'ANALOG_INPUT',
    'AO': 'ANALOG_OUTPUT',
    'BI': 'BINARY_INPUT',
    'BO': 'BINARY_OUTPUT'
}

# 批量映射
for _, row in df.iterrows():
    point = CIM_Point()
    point.point_id = row['点位编号']
    point.point_name = row['点位名称']
    point.point_type = point_type_map[row['点位编号'][:2]]
    point.device_id = row['设备类型']
    point.location = row['位置']

    # 解析协议地址
    if row['协议'] == 'BACnet':
        ip, type, idx = row['地址'].split(':')
        point.protocol = 'BACNET/IP'
        point.protocol_address = {
            'device_ip': ip,
            'object_type': type,
            'object_id': int(idx)
        }

    cim_model.add_point(point)
```

### 设备映射

**BMS 设备 → CIM 设备**:
```python
# BMS DDC 设备列表
bms_devices = [
    {'name': 'DDC-3F-01', 'ip': '192.168.1.100', 'vendor': 'Johnson'},
    {'name': 'DDC-3F-02', 'ip': '192.168.1.101', 'vendor': 'Siemens'}
]

# 映射到 CIM Controller
for dev in bms_devices:
    controller = CIM_Controller()
    controller.controller_id = dev['name']
    controller.controller_type = 'DDC'
    controller.communication = {
        'protocol': 'BACNET/IP',
        'ip_address': dev['ip'],
        'vendor': dev['vendor'],
        'port': 47808
    }
    cim_model.add_equipment(controller)
```

### 能耗数据映射

**电表数据**:
```python
def map_energy_data(meter_data):
    """将电表数据映射到 CIM Meter 和 Measurement"""

    # 创建计量设备
    meter = CIM_Meter()
    meter.meter_id = meter_data['meter_id']
    meter.meter_type = 'ELECTRICITY'
    meter.location = meter_data['location']
    meter.phase = meter_data.get('phase', '3P')
    cim_model.add_meter(meter)

    # 创建测量值
    measurement = CIM_Measurement()
    measurement.measurement_id = f"{meter.meter_id}_{meter_data['timestamp']}"
    measurement.meter_id = meter.meter_id
    measurement.timestamp = meter_data['timestamp']
    measurement.parameters = {
        'active_power_kw': meter_data['power_kw'],
        'cumulative_energy_kwh': meter_data['energy_kwh'],
        'power_factor': meter_data.get('pf'),
        'voltage_v': meter_data.get('voltage')
    }
    cim_model.add_measurement(measurement)
```

---

## CIM 存储

### 数据库设计

**时序数据 (InfluxDB)**:
```sql
-- 创建数据库
CREATE DATABASE cim_timeseries

-- 数据保留策略
CREATE RETENTION POLICY "one_year" ON "cim_timeseries" DURATION 365d REPLICATION 1

-- 典型查询
SELECT mean("value") FROM "sensor_data"
WHERE "sensor_id" = 'AI-301'
  AND time >= now() - 24h
GROUP BY time(1h)
```

**关系数据 (PostgreSQL)**:
```sql
-- 设备表
CREATE TABLE equipment (
    equipment_id VARCHAR(50) PRIMARY KEY,
    equipment_name VARCHAR(200),
    equipment_type VARCHAR(100),
    system_id VARCHAR(50) REFERENCES systems(system_id),
    location_id VARCHAR(50) REFERENCES spaces(space_id),
    installed_date DATE,
    warranty_until DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引优化
CREATE INDEX idx_equipment_type ON equipment(equipment_type);
CREATE INDEX idx_equipment_system ON equipment(system_id);
CREATE INDEX idx_equipment_location ON equipment(location_id);
```

**图数据 (Neo4j)**:
```cypher
-- 创建设备节点
CREATE (ch:Equipment {id:'CH-001', name:'冷水机-001', type:'Chiller'})

-- 创建系统节点
CREATE (sys:System {id:'HVAC-CHW-001', name:'冷冻水系统'})

-- 建立关系
CREATE (ch)-[:COMPONENT_OF]->(sys)

-- 查询系统所有设备
MATCH (sys:System {id:'HVAC-CHW-001'})<-[:COMPONENT_OF]-(eq)
RETURN eq.name, eq.type
```

### API 接口

**REST API (FastAPI)**:
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class EquipmentCreate(BaseModel):
    equipment_id: str
    equipment_name: str
    equipment_type: str

@app.post("/api/v1/equipment")
async def create_equipment(equip: EquipmentCreate):
    """创建设备"""
    try:
        equipment = cim_model.create_equipment(equip.dict())
        return {"success": True, "data": equipment}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/equipment/{equipment_id}")
async def get_equipment(equipment_id: str):
    """获取设备详情"""
    equipment = cim_model.get_equipment(equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="设备不存在")
    return equipment

@app.get("/api/v1/systems/{system_id}/energy")
async def get_system_energy(
    system_id: str,
    start: str,
    end: str
):
    """获取系统能耗数据"""
    energy_data = await cim_model.get_energy_consumption(
        system_id, start, end
    )
    return energy_data
```

**GraphQL (查询灵活)**:
```graphql
type Query {
  equipment(id: String!): Equipment
  system(id: String!): System
}

type Equipment {
  id: String!
  name: String!
  type: String!
  location: Space
  system: System
  children: [Equipment]
}

query {
  equipment(id: "CH-001") {
    name
    type
    location {
      name
    }
    system {
      name
    }
  }
}
```

---

## 数据质量监控

### 完整性监控

```python
# 检查数据缺失率
CREATE MATERIALIZED VIEW data_completeness AS
SELECT
  sensor_id,
  COUNT(*) as total_points,
  COUNT(value) as non_null_points,
  ROUND(
    COUNT(value)::numeric / COUNT(*), 4
  ) as completeness_ratio,
  NOW() as last_checked
FROM sensor_data
WHERE time >= NOW() - INTERVAL '24 hours'
GROUP BY sensor_id

# 告警
delete FROM sensor_data WHERE completeness_ratio < 0.95
```

### 准确性监控

```python
# 异常检测
from sklearn.ensemble import IsolationForest

# 训练模型
model = IsolationForest(contamination=0.05)
model.fit(training_data)

# 实时预测
for new_data in stream_data:
    anomaly = model.predict([new_data])
    if anomaly == -1:  # 异常
        send_alert(f"数据异常: {new_data}")
```

### 及时性监控

```python
# 检查数据延迟
SELECT
  sensor_id,
  EXTRACT(EPOCH FROM (NOW() - max(time))) as delay_seconds
FROM sensor_data
GROUP BY sensor_id
HAVING delay_seconds > 300  -- 超过5分钟
```

---

## 性能优化

### 批量写入

```python
# 批量写入 InfluxDB (1000条/批)
points = []
for i, record in enumerate(data_stream):
    points.append({
        "measurement": "sensor_data",
        "tags": {"sensor_id": record['id']},
        "fields": {"value": record['value']},
        "time": record['timestamp']
    })

    if len(points) >= 1000:
        influx.write_points(points, batch_size=1000)
        points = []

influx.write_points(points)  # 剩余
```

### 时间分区

```sql
-- PostgreSQL 按月分区
CREATE TABLE sensor_data (
    time TIMESTAMP,
    sensor_id VARCHAR,
    value DOUBLE PRECISION
) PARTITION BY RANGE (time);

CREATE TABLE sensor_data_2025_12
PARTITION OF sensor_data
FOR VALUES FROM ('2025-12-01') TO ('2026-01-01');
```

### 缓存

```python
from functools import lru_cache

@lru_cache(maxsize=1024)
def get_equipment_info(equipment_id):
    """缓存设备信息"""
    return db.query("SELECT * FROM equipment WHERE id = ?", equipment_id)
```

---

## 数据安全

### 权限控制

**RBAC (角色权限) **:
```python
class DataAccessControl:
    def check_permission(user, resource):
        # 管理员: 读写所有
        if user.role == 'ADMIN':
            return True

        # 运维工程师: 读写本区域
        if user.role == 'ENGINEER' and user.zone == resource.zone:
            return True

        # 临床用户: 只读
        if user.role == 'CLINICAL':
            return resource.action == 'READ'

        return False
```

### 数据脱敏

```python
def mask_sensitive_data(record):
    """脱敏处理"""
    if 'patient_id' in record:
        record['patient_id'] = hash(record['patient_id'])

    if 'equipment_location' in record:
        # 只保留到楼层
        record['equipment_location'] = record['location'].split('-')[2]

    return record
```

---

## 运维工具

### 数据质量看板

```python
# Grafana 看板
 panels:
  - 标题: " 数据完整性 "
    type: stat
    query: SELECT completene[...]