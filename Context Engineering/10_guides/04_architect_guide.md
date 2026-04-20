# 架构师CIM实施指南

**文档 ID**: `CIMU-GUIDE-04-ARCHITECT`
**版本**: v1.0
**最后更新**: 2025-12-07

---

## 面向对象

系统架构师、技术负责人、解决方案架构师

---

## 架构原则

### 1. 本体优先 (Ontology-First)

**核心思想**: 先定义概念，再设计系统

**实践**:
```
❌ 错误: 先设计数据库表，再反过来定义概念
  CREATE TABLE equipment (...);  -- 表结构驱动

✅ 正确: 先定义本体，再生成数据库
  Equipment --(hasProperty)--> PowerRating  -- 本体驱动
  ↓
  CREATE TABLE equipment (power_rating FLOAT);
```

### 2. 分层解耦 (Layered Decoupling)

```
┌─────────────────────────────────────────┐
│   应用层 (App)                           │
│   能耗分析、故障诊断、预测维护           │
├─────────────────────────────────────────┤
│   服务层 (Service)                       │
│   REST API、GraphQL、消息队列            │
├─────────────────────────────────────────┤
│   领域层 (Domain)                        │
│   CIM模型、业务逻辑、规则引擎            │
├─────────────────────────────────────────┤
│   数据层 (Data)                          │
│   时序DB、关系DB、图DB、数据湖         │
└─────────────────────────────────────────┘

层与层通过接口交互，上层不依赖下层实现
```

### 3. 事件驱动 (Event-Driven)

```
传感器产生事件 → 事件总线 → 多个消费者

示例: 温度超限
  TemperatureSensor: "T-301 超过 25°C"
    ↓ 发布到 Kafka
  消费者1: 告警服务 → 发送短信
  消费者2: 记录服务 → 写入日志
  消费者3: 优化服务 → 调整设定值
```

### 4. 弹性设计 (Resilience)

**策略**:
- 熔断 (Circuit Breaker): 服务故障快速失败
- 降级 (Degradation): 核心功能可用
- 限流 (Rate Limit): 防止过载
- 重试 (Retry): 网络抖动恢复

---

## 技术栈选型

### 数据持久化

**时序数据**: InfluxDB
```
优势:
- 专有时序存储，压缩率高
- 强大的查询语言 (Flux)
- 生态完善 (Telegraf, Chronograf)

适用场景:
- 传感器历史数据
- 能耗计量数据
- 性能趋势分析
```

**关系数据**: PostgreSQL
```
优势:
- ACID 事务强一致
- 支持 JSONB, GIS 扩展
- 开源、稳定

适用场景:
- 设备台账、空间信息
- 用户、权限、配置
- 工单、维护记录
```

**图数据**: Neo4j
```
优势:
- 原生图存储
- Cypher 查询直观
- 可视化工具强大

适用场景:
- 设备拓扑关系
- 故障传播路径
- 依赖关系分析
```

**缓存**: Redis
```
优势:
- 高性能内存缓存
- 支持 Pub/Sub
- 支持数据结构

适用场景:
- 会话管理
- 热点数据缓存
- 实时排行榜
```

### 后端服务

**主框架**: FastAPI
```python
app = FastAPI(
    title="CIM API",
    description="统一领域模型接口",
    version="1.0.0"
)

@app.get("/api/v1/equipment/{equipment_id}")
async def get_equipment(equipment_id: str):
    return cim_service.get_equipment(equipment_id)
```

优势:
- 现代框架，性能优异
- 异步支持，高并发
- 自动生成 OpenAPI 文档

**规则引擎**: Drools
```java
rule "HighEnergyUsage"
when
    $meter: Meter(energy > threshold)
    $time: Hour() >= 14 && < 18  // 尖峰时段

then
    $meter.setAlert("HIGH_ENERGY_USAGE");
    alertService.send($meter);
end
```

**工作流**: Airflow
```python
# 定时数据同步
with DAG('cim_data_sync', schedule_interval='@daily'):
    extract = PythonOperator(task_id='extract', ...)
    transform = PythonOperator(task_id='transform', ...)
    load = PythonOperator(task_id='load', ...)

    extract >> transform >> load
```

### 前端展示

**可视化**: Grafana
- 配置简单，模板丰富
- 支持多种数据源
- 支持告警

**3D 展示**: Three.js + IFC.js
```javascript
// 加载 IFC 模型
const ifcLoader = new IFCLoader();
const model = await ifcLoader.loadAsync('./model.ifc');

// 叠加实时数据
model.traverse((object) => {
  if (object.name.includes('AHU')) {
    const status = getRealTimeData(object.name);
    object.material.color.set(status === 'running' ? 0x00ff00 : 0xff0000);
  }
});
```

---

## 数据架构

### 数据流设计

```
数据源 (DDC、电表)
  ↓ (BACnet, Modbus, OPC)
数据采集层 (Telegraf, 自研采集器)
  ↓ (Kafka, MQTT)
消息总线 (事件驱动)
  ↓ (Flink, Stream Processing)
实时计算层 (规则引擎、告警检测)
  ↓ (InfluxDB, PostgreSQL)
数据存储层
  ↓ (FastAPI GraphQL)
接口服务层
  ↓ (React, Grafana)
应用层 (监控、分析、报表)
```

### 数据模型

**核心实体**: Equipment, Space, System, Meter
```python
class Equipment(BaseModel):
    equipment_id: str  # 唯一标识
    equipment_name: str
    equipment_type: str
    system_id: Optional[str]
    location_id: Optional[str]
    parent_id: Optional[str]  # 层级关系
    attributes: Dict[str, Any]  # 动态属性
    status: str  # RUNNING, STOPPED, FAULT, MAINTENANCE
    created_at: datetime
    updated_at: datetime

class System(BaseModel):
    system_id: str
    system_name: str
    system_category: str  # HVAC, ELECTRICAL, PLUMBING
    contains_equipment: List[str]
    serves_spaces: List[str]
```

**关系建模**:
- 使用图数据库存储拓扑关系
- 使用外键 + 嵌套查询实现 E-R 关系
- 支持动态关系绑定 (运行时)

```python
# 示例: 查询系统所有设备
def get_system_equipment(system_id: str):
    # 关系数据库 (JOIN)
    query = """
        SELECT e.* FROM equipment e
        WHERE e.system_id = %s
    """

    # 图数据库
    query = """
        MATCH (sys:System {id: $system_id})-[:CONTAINS]->(eq:Equipment)
        RETURN eq
    """
```

### 数据一致性

**强一致性**:
```python
@transaction.atomic
def update_equipment(equipment_id, data):
    equipment = Equipment.objects.get(id=equipment_id)
    equipment.update(data)

    # 同时更新索引
    SearchIndex.update(equipment)

    # 发送变更事件
    EventBus.publish('equipment.updated', equipment)
```

**最终一致性** (分布式):
```python
# 主库更新后立即返回
write_to_primary(equipment)

# 从库异步同步
task.delay_sync_to_replicas(equipment)

# 缓存异步刷新
task.delay_update_cache(equipment.id)
```

---

## 接口设计

### REST API 设计规范

**URL 规范**:
```
GET    /api/v1/equipment              # 列表
GET    /api/v1/equipment/{id}         # 详情
POST   /api/v1/equipment              # 创建
PUT    /api/v1/equipment/{id}         # 全量更新
PATCH  /api/v1/equipment/{id}         # 部分更新
DELETE /api/v1/equipment/{id}         # 删除
GET    /api/v1/equipment/{id}/energy  # 子资源
```

**响应格式**:
```json
{
  "success": true,
  "data": {
    "equipment_id": "CH-001",
    "equipment_name": "冷水机-001",
    ...
  },
  "meta": {
    "timestamp": "2025-12-07T10:30:00Z",
    "version": "1.0"
  },
  "error": null
}
```

**错误处理**:
```python
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "data": None,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(exc),
                "trace_id": request.state.trace_id
            }
        }
    )
```

### GraphQL 设计

**Schema 定义**:
```graphql
type Query {
  equipment(id: String!): Equipment
  equipmentList(
    systemId: String,
    locationId: String,
    type: String,
    limit: Int = 20,
    offset: Int = 0
  ): EquipmentConnection!

  system(id: String!): System

  search(keyword: String!): [SearchResult]
}

type Equipment {
  id: String!
  name: String!
  type: String!
  location: Space!
  system: System!
  status: String!
  energyConsumption(start: String, end: String): EnergyData
}

type EquipmentConnection {
  edges: [EquipmentEdge!]!
  totalCount: Int!
  pageInfo: PageInfo!
}

# 优势: 一次查询获取所有关联数据
query {
  equipment(id: "CH-001") {
    name
    status
    location {
      name
      building {
        name
      }
    }
    system {
      name
    }
    energyConsumption(start: "2025-12-01", end: "2025-12-31") {
      power
    }
  }
}
```

---

## 性能设计

### 缓存策略

**多级缓存**:
```
Request
  ↓
L1: 浏览器缓存 (静态资源)
  ↓
L2: CDN 缓存 (API 响应)
  ↓
L3: 应用缓存 (Redis)
  ↓
L4: 数据库缓存 (Query Cache)
  ↓
Storage
```

**缓存更新**:
```python
# 写穿模式 (Write-Through)
def update_equipment(equipment_id, data):
    # 1. 更新数据库
    db.update(equipment_id, data)

    # 2. 更新缓存
    redis.set(f"equipment:{equipment_id}", data)

    # 3. 失效 CDN
    cdn.invalidate(f"/api/v1/equipment/{equipment_id}")

# 缓存雪崩预防
if redis.get(key) is None:
    # 加锁，只允许一个请求加载
    with redis.lock(key):
        data = db.query(...)
        redis.set(key, data, ex=3600)
```

### 查询优化

**数据库**:
```sql
-- 添加复合索引
CREATE INDEX idx_equipment_system_location
ON equipment(system_id, location_id);

-- 查询优化
SELECT e.*, s.name as system_name
FROM equipment e
JOIN systems s ON e.system_id = s.id
WHERE e.system_id = 'HVAC-CHW-001'
  AND e.status = 'RUNNING';

-- 使用 EXPLAIN 分析
EXPLAIN ANALYZE SELECT ...;
```

**批量查询**:
```python
# ❌ 低效: N+1 查询
for equip in equipment_list:
    system = db.query("SELECT * FROM systems WHERE id = ?", equip.system_id)

# ✅ 高效: 批量查询
system_ids = [eq.system_id for eq in equipment_list]
systems = db.query(
    "SELECT * FROM systems WHERE id IN (%s)" % ','.join('?'*len(system_ids)),
    system_ids
)
system_map = {s.id: s for s in systems}
```

---

## 部署架构

### 云端 vs 本地

**云端部署 (推荐)**:
```
优势:
- 无需硬件投资
- 自动扩缩容
- 全球可访问
- 运维托管

方案:
- AWS / Azure / Aliyun
- Kubernetes 容器编排
- RDS 托管数据库

成本: 按量计费，弹性
```

**本地部署**:
```
优势:
- 数据完全控制
- 网络延迟低
- 定制化灵活

方案:
- 物理服务器 (3台)
- VMware / Hyper-V
- 自建 Kubernetes

成本: 一次性投入 + 运维人力
```

### 网络拓扑

```
Internet
  ↓
WAF (Web应用防火墙)
  ↓
Load Balancer (负载均衡)
  ↓
API Gateway (API网关)
  ↓
┌───┴───┬───┴───┬───┴───┐
App1    App2    App3   ... (多实例)
  ↓       ↓       ↓
┌───────┴───────┴───────┐
   数据库集群 (主从)
└───────────┬───────────┘
            ↓
   Redis 缓存集群
└───────────┬───────────┘
            ↓
       存储 (NAS)
```

### 监控

**指标监控 (Prometheus)**:
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'cim-api'
    static_configs:
      - targets: ['api:8080']
    metrics_path: '/metrics'

  - job_name: 'cim-db'
    static_configs:
      - targets: ['postgres:5432']
```

**日志监控 (ELK)**:
```
Application → Filebeat → Logstash → Elasticsearch → Kibana
                          (解析)          (存储)      (展示)
```

**链路追踪 (Jaeger)**:
```python
# 自动注入追踪
tracer = jaeger_client.Config(
    config={
        'sampler': {'type': 'const', 'param': 1},
        'local_agent': {'reporting_host': 'jaeger-agent'}
    },
    service_name='cim-api'
).initialize_tracer()

@app.get("/api/v1/equipment/{id}")
def get_equipment(id):
    with tracer.start_span('get_equipment') as span:
        span.set_tag('equipment_id', id)
        result = db.query(id)
        return result
```

---

## 扩展性设计

### 水平扩展

**无状态服务**:
```python
# ❌ 有状态
class EquipmentService:
    def __init__(self):
        self.cache = {}  # 本地缓存

    def get(self, id):
        if id in self.cache:
            return self.cache[id]

# ✅ 无状态
class EquipmentService:
    def get(self, id):
        # 缓存外置
        return redis.get(f"equipment:{id}") or db.query(id)
```

**负载均衡**:
```yaml
# Kubernetes Service
apiVersion: v1
kind: Service
metadata:
  name: cim-api
spec:
  selector:
    app: cim-api
  ports:
  - port: 80
  type: LoadBalancer
```

### 垂直扩展

**模块化设计**:
```python
# cim/core/__init__.py
- equipment.py      # 设备模块
- space.py          # 空间模块
- system.py         # 系统模块
- control.py        # 控制模块
- metering.py       # 计量模块

# 可独立部署
- cim-equipment-service
- cim-space-service
- cim-system-service
```

---

## 安全设计

### 认证授权

```python
from fastapi.security import OAuth2PasswordBearer
au[...]