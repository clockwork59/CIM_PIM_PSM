# CIM-PIM-PSM 三层架构详解

**文档 ID**: `CIMU-FOUND-04-ARCHITECTURE`
**版本**: v1.0
**最后更新**: 2025-12-07

---

## 架构概述

CIM-PIM-PSM 是模型驱动架构（MDA）在医疗建筑领域的具体实践，通过三个层次的模型实现从业务概念到技术实现的完整映射。

```
┌─────────────────────────────────────────────────┐
│         CIM (计算无关模型)                        │
│  领域概念、业务规则、自然语言描述                  │
│  "WHAT" - 做什么                                │
├─────────────────────────────────────────────────┤
│         PIM (平台无关模型)                        │
│  逻辑结构、API契约、技术中立设计                   │
│  "HOW TO DESIGN" - 如何设计                      │
├─────────────────────────────────────────────────┤
│         PSM (平台特定模型)                        │
│  具体实现、代码生成、平台相关部署                  │
│  "HOW TO CODE" - 如何编码                        │
└─────────────────────────────────────────────────┘
```

---

## CIM 层：计算无关模型

### 定义

CIM（Computation Independent Model）是业务专家眼中的世界，完全不受技术实现细节的约束。

### 核心要素

#### 1. 领域概念（Domain Concepts）

**示例：冷冻水系统**
```yaml
CIM层描述:
  概念: "冷冻水系统"
  定义: "为空调末端提供冷水的系统"
  组成:
    - 冷水机组: "制冷的设备"
    - 冷冻水泵: "输送冷水的设备"
    - 管道系统: "输送介质的通道"
  功能: "移除室内热量，维持舒适环境"
```

**特点**：
- 使用自然语言
- 面向业务人员
- 无需技术背景即可理解
- 关注"是什么"而非"如何实现"

#### 2. 业务规则（Business Rules）

**示例：手术室温度控制**
```yaml
业务规则: "手术室温度控制"
描述: "手术室的温湿度必须严格控制在特定范围内"
条件:
  - 空间类型: "手术室"
  - 手术状态: "进行中"
要求:
  - 温度: "21°C ~ 24°C"
  - 湿度: "45% ~ 60% RH"
  - 压差: "+5Pa ~ +15Pa"
违反后果: "影响手术安全，可能导致感染"
```

**特点**：
- 用业务语言表达
- 可验证、可测试
- 与具体技术无关
- 易于业务专家审查

#### 3. 用例场景（Use Case Scenarios）

**示例：急诊室扩容**
```yaml
用例: "急诊室从10床扩容到20床"
参与者:
  - 医院管理者
  - 运维工程师
  - 设计顾问

场景步骤:
  1. 修改急诊室空间属性 (床位数: 10 → 20)
  2. CIM系统自动计算新的负荷需求
  3. CIM系统验证现有系统容量
  4. CIM系统生成改造建议报告
  5. 专家审查并确认方案
  6. CIM模型更新，指导施工
```

### CIM 建模工具

- **语言**: 自然语言、业务流程图、用例图
- **格式**: Markdown、YAML、流程图
- **验证**: 业务专家评审、用例测试

---

## PIM 层：平台无关模型

### 定义

PIM（Platform Independent Model）是架构师的设计，定义系统的逻辑结构，但不涉及具体技术平台。

### 核心要素

#### 1. 逻辑数据模型（Logical Data Model）

**示例：冷冻水系统 PIM**
```yaml
PIM层设计:

  实体类 - System:
    properties:
      system_id: String (唯一标识)
      system_name: String (系统名称)
      system_type: Enum [HVAC, PLUMBING, ELECTRICAL]
    relationships:
      contains_equipment: List<Equipment> (1:N)
      serves_spaces: List<Space> (N:N)

  实体类 - Equipment:
    properties:
      equipment_id: String (唯一标识)
      equipment_type: String (设备类型)
      rated_power: Float (额定功率, kW)
      location: Reference<Space> (所在空间)
    relationships:
      component_of_system: Reference<System> (N:1)
      connected_to: List<Equipment> (N:N)

  实体类 - Space:
    properties:
      space_id: String (唯一标识)
      space_type: Enum [OPERATING_ROOM, ICU, WARD]
      area_m2: Float (面积)
      volume_m3: Float (体积)
    relationships:
      served_by_systems: List<System> (N:N)
      contains_subspaces: List<Space> (1:N)
```

**特点**：
- 技术中立（Technology-Neutral）
- 不指定编程语言、数据库、中间件
- 关注"结构"而非"实现"
- 可由工具自动验证一致性

#### 2. API 契约（API Contracts）

**示例：系统查询 API**
```yaml
API: GET /api/v1/systems/{system_id}

请求:
  path_parameters:
    system_id: String (系统唯一标识)
  query_parameters:
    include_equipment: Boolean (是否包含设备详情, 默认: false)
    depth: Integer (关联查询深度, 默认: 1)

响应:
  status_code: 200 OK
  body:
    system_id: String
    system_name: String
    system_type: String
    equipment_count: Integer
    served_spaces_count: Integer
    energy_efficiency: Float (能效比)
    _links:
      self: URL
      equipment: URL
      served_spaces: URL

错误响应:
  404 Not Found: 系统不存在
  400 Bad Request: 参数错误
```

**特点**：
- 与实现技术无关（可用 REST、GraphQL、gRPC 实现）
- 明确定义请求/响应格式
- 包含错误处理规范
- 支持版本管理

#### 3. 服务接口（Service Interfaces）

**示例：能耗计算服务**
```java
// PIM 层定义（伪代码）
interface EnergyCalculationService {

  // 计算系统实时能耗
  function calculateRealTimePower(
    systemId: String,
    timestamp: DateTime
  ): Float
    // 前置条件: 系统必须存在
    // 后置条件: 返回系统总功率(kW)
    // 异常: SystemNotFoundException

  // 计算系统能效比
  function calculateEnergyEfficiency(
    systemId: String,
    startTime: DateTime,
    endTime: DateTime
  ): Float
    // 前置条件: 时间区间有效
    // 后置条件: 返回平均能效比(EER)
    // 异常: InvalidTimeRangeException
}
```

**特点**：
- 接口契约明确
- 包含前置/后置条件
- 无具体实现代码
- 可由多种语言实现

### PIM 建模工具

- **语言**: UML、接口定义语言（IDL）、OpenAPI/Swagger
- **格式**: YAML、JSON、XML
- **验证**: 接口一致性检查、契约测试

---

## PSM 层：平台特定模型

### 定义

PSM（Platform Specific Model）是开发者的实现，针对特定技术平台（Java/Python、PostgreSQL/MongoDB、Linux/Windows）的具体代码和配置。

### 核心要素

#### 1. 物理数据模型（Physical Data Model）

**示例：PostgreSQL 实现**
```sql
-- PSM 层实现
CREATE TABLE systems (
    system_id VARCHAR(50) PRIMARY KEY,
    system_name VARCHAR(200) NOT NULL,
    system_type VARCHAR(50) CHECK (system_type IN ('HVAC', 'PLUMBING', 'ELECTRICAL')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE equipment (
    equipment_id VARCHAR(50) PRIMARY KEY,
    equipment_name VARCHAR(200) NOT NULL,
    equipment_type VARCHAR(100),
    rated_power DECIMAL(10, 2),  -- kW
    system_id VARCHAR(50) REFERENCES systems(system_id),
    space_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_equipment_system ON equipment(system_id);
CREATE INDEX idx_equipment_space ON equipment(space_id);

-- 物化视图：系统能效
CREATE MATERIALIZED VIEW system_efficiency AS
SELECT
    s.system_id,
    s.system_name,
    AVG(e.rated_power) as avg_power,
    SUM(CASE WHEN e.operational_state = 'RUNNING' THEN 1 ELSE 0 END) as running_count
FROM systems s
LEFT JOIN equipment e ON s.system_id = e.system_id
GROUP BY s.system_id, s.system_name;
```

**特点**：
- 平台特定（PostgreSQL）
- 包含性能优化（索引、物化视图）
- 考虑存储限制（数据类型选择）
- 包含数据库特定特性

#### 2. 具体实现代码（Concrete Implementation）

**示例：Java Spring Boot 实现**
```java
// PSM 层实现
@RestController
@RequestMapping("/api/v1/systems")
public class SystemController {

    @Autowired
    private SystemService systemService;

    @GetMapping("/{systemId}")
    public ResponseEntity<SystemDTO> getSystem(
        @PathVariable String systemId,
        @RequestParam(defaultValue = "false") boolean includeEquipment,
        @RequestParam(defaultValue = "1") int depth
    ) {
        try {
            SystemDTO system = systemService.findById(systemId, includeEquipment, depth);
            return ResponseEntity.ok(system);
        } catch (SystemNotFoundException e) {
            return ResponseEntity.notFound().build();
        }
    }
}

@Service
public class SystemService {

    @Autowired
    private SystemRepository systemRepository;

    public SystemDTO findById(String systemId, boolean includeEquipment, int depth) {
        // 使用 JPA 查询优化
        System system = systemRepository.findByIdWithEagerLoading(systemId)
            .orElseThrow(() -> new SystemNotFoundException(systemId));

        // 深度控制，防止递归溢出
        if (depth > 3) {
            depth = 3;
        }

        return SystemMapper.toDTO(system, includeEquipment, depth);
    }
}
```

**特点**：
- 框架特定（Spring Boot）
- 包含框架最佳实践
- 考虑性能优化（查询优化、缓存）
- 包含错误处理、日志、监控

#### 3. 部署配置（Deployment Configuration）

**示例：Kubernetes 部署**
```yaml
# PSM 层配置
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cim-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cim-service
  template:
    metadata:
      labels:
        app: cim-service
    spec:
      containers:
      - name: cim-service
        image: cim-service:1.0.0
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: cim-service
spec:
  selector:
    app: cim-service
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

**特点**：
- 平台特定（Kubernetes）
- 包含可观测性配置（健康检查）
- 资源限制与自动扩缩
- 服务发现与负载均衡

### PSM 建模工具

- **语言**: Java、Python、SQL、YAML、Dockerfile
- **格式**: 源代码、配置文件、部署清单
- **验证**: 单元测试、集成测试、性能测试

---

## 三层次协作流程

### 跨层次映射示例

#### 示例：手术室温湿度控制

**CIM 层（业务）**：
```yaml
业务需求: "手术室温湿度必须在手术期间保持在舒适范围内"
约束条件:
  温度: "21°C ~ 24°C"
  湿度: "45% ~ 60%"
触发条件: "手术开始"
相关人员: ["手术医生", "麻醉医生", "护士", "运维工程师"]
```

**PIM 层（设计）**：
```yaml
接口定义:
  - ControlLoop:
      - inputs: [SupplyTemp, ReturnTemp, Humidity]
      - setpoint: OperatingRoomClimateSetpoint
      - outputs: [ChilledWaterValve, HotWaterValve, Humidifier]
      - control_algorithm: PID_Cascade

  - Alert:
      - condition: TempOutOfRange OR HumidityOutOfRange
      - recipients: [BMS, MaintenanceTeam, OR_Supervisor]
      - priority: HIGH
```

**PSM 层（实现）**：
```python
# Python 实现
class OperatingRoomController:
    def __init__(self, room_id):
        self.room_id = room_id
        self.pid_temp = PID(Kp=2.0, Ki=0.5, Kd=0.1)
        self.pid_humidity = PID(Kp=1.5, Ki=0.3, Kd=0.05)

    def control(self, sensor_data):
        temp_error = OPERATING_ROOM_SETPOINT - sensor_data.temperature
        humidity_error = HUMIDITY_SETPOINT - sensor_data.humidity

        valve_command = self.pid_temp.calculate(temp_error)
        humidifier_command = self.pid_humidity.calculate(humidity_error)

        if abs(temp_error) > 1.0 or abs(humidity_error) > 5:
            self.send_alert("OPERATING_ROOM_CLIMATE_ALERT", priority="HIGH")

        return ControlCommand(valve=valve_command, humidifier=humidifier_command)
```

---

## 层次转换工具链

### CIM → PIM 转换

```python
# 示例：从自然语言需求生成 API 契约
class CIMtoPIMConverter:

    def convert_requirement_to_api(self, cim_requirement):
        """
        CIM: "查询冷冻水系统的实时能耗"
        ↓
        PIM: GET /api/v1/systems/{system_id}/energy?realtime=true
        """
        pass

    def convert_constraint_to_validation(self, cim_constraint):
        """
        CIM: "手术室温度必须保持在21-24°C"
        ↓
        PIM:
          - temperature: Float
          - validation: 21.0 ≤ value ≤ 24.0
        """
        pass
```

工具：NLP 需求分析、领域驱动设计（DDD）

### PIM → PSM 转换

```python
# 示例：从 API 契约生成代码
class PIMtoPSMConverter:

    def generate_controller(self, api_spec):
        """
        PIM: OpenAPI spec
        ↓
        PSM: Spring Boot Controller / FastAPI Router
        """
        pass

    def generate_database_schema(self, logical_model):
        """
        PIM: Logical Data Model
        ↓
        PSM: PostgreSQL DDL / MongoDB Schema
        """
        pass
```

工具：代码生成器（OpenAPI Generator）、ORM 框架（JPA、SQLAlchemy）

---

## 架构验证与质量保证

### 一致性检查

1. **CIM ↔ PIM 一致性**
   - 检查 PIM 中的每个概念是否在 CIM 中有定义
   - 验证业务规则是否正确映射为 API 契约
   - 工具：需求追踪矩阵

2. **PIM ↔ PSM 一致性**
   - 检查 PSM 是否正确实现 PIM 接口
   - 验证数据库 Schema 是否符合逻辑模型
   - 工具：契约测试（Pact）、Schema 验证

### 完整性检查

**CIM 完整性**：
- [ ] 所有核心概念已定义
- [ ] 业务规则完整、无冲突
- [ ] 用例场景覆盖主要流程

**PIM 完整性**：
- [ ] 所有实体类有增删改查接口
- [ ] API 契约包含错误处理
- [ ] 服务接口定义完整

**PSM 完整性**：
- [ ] 所有接口有具体实现
- [ ] 包含单元测试和集成测试
- [ ] 有部署和监控配置

---

## 最佳实践

### 1. 分层开发，迭代演进

**推荐流程**：
```
迭代 1: 核心 CIM 概念 → 基础 PIM → MVP PSM
迭代 2: 扩展 CIM → 完善 PIM → 增强 PSM
迭代 3: 优化 CIM → 优化 PIM → 优化 PSM
```

**避免**：一次性完成所有层次的完美设计

### 2. 自动化转换

- 尽可能使用工具自动转换（CIM→PIM，PIM→PSM）
- 减少手工编码错误
- 提高开发效率

**工具栈**：
- CIM → PIM: NLP + DDD 工具
- PIM → PSM: OpenAPI Generator, JHipster

### 3. 多层次验证

- CIM 验证：业务专家评审
- PIM 验证：技术评审 + 契约测试
- PSM 验证：代码审查 + 自动化测试

---

## 总结

| 层次 | 受众 | 关注点 | 工具 | 可变性 |
|-----|------|--------|------|--------|
| **CIM** | 业务专家 | 做什么 | 自然语言、流程图 | 高（需求变化） |
| **PIM** | 架构师 | 如何设计 | UML、OpenAPI | 中（设计演进） |
| **PSM** | 开发者 | 如何编码 | 代码、配置 | 低（实现稳定） |

**核心价值**：
- 分离关注点（业务 vs 技术）
- 提高复用性（PIM 可生成多种 PSM）
- 隔离变化（CIM 变化不直接影响 PSM）
- 自动化生成（减少手工编码）

**应用原则**：
- 先 CIM，后 PIM，再 PSM
- 每层都有明确的验证标准
- 使用工具链支持自动转换
- 保持层次间的追溯性

---

## 延伸阅读

- [模型驱动架构（MDA）官方指南](http://www.omg.org/mda/)
- [领域驱动设计（DDD）- Eric Evans](../40_reference/academic_foundations.md)
- [OpenAPI 规范 v3.0](../40_reference/standards_mapping.md)
- [CIM 本体导论](../00_foundations/03_cim_ontology_introduction.md)
- [BIM 工程师实施指南](../10_guides/02_bim_engineer_guide.md)

---

*"好的架构不是一蹴而就的，而是通过清晰的分层和持续的演进逐步构建的。"*
