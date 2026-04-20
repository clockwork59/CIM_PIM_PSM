# 核心概念：CIM-PIM-PSM 三层架构

> 本文档详解模型驱动架构（MDA）在医疗建筑领域的具体实践。

## 架构总览

```
┌─────────────────────────────────────────────────┐
│         CIM (Computation Independent Model)     │
│         计算无关模型                             │
│  领域概念、业务规则、自然语言描述                  │
│  "WHAT" - 做什么                                │
│  受众：业务专家、医院管理者、医生                  │
├─────────────────────────────────────────────────┤
│         PIM (Platform Independent Model)        │
│         平台无关模型                             │
│  逻辑结构、API契约、技术中立设计                   │
│  "HOW TO DESIGN" - 如何设计                      │
│  受众：架构师、系统分析师                         │
├─────────────────────────────────────────────────┤
│         PSM (Platform Specific Model)           │
│         平台特定模型                             │
│  具体实现、代码生成、平台相关部署                  │
│  "HOW TO CODE" - 如何编码                        │
│  受众：开发人员、DevOps工程师                     │
└─────────────────────────────────────────────────┘
```

## CIM 层：计算无关模型

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

## PIM 层：平台无关模型

### 核心要素

#### 1. 逻辑数据模型

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
```

#### 2. API 契约

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

错误响应:
  404 Not Found: 系统不存在
  400 Bad Request: 参数错误
```

#### 3. 服务接口

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
}
```

### PIM → PSM 转换

```python
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

## PSM 层：平台特定模型

### 核心要素

#### 1. 物理数据模型

**示例：PostgreSQL 实现**
```sql
-- PSM 层实现
CREATE TABLE systems (
    system_id VARCHAR(50) PRIMARY KEY,
    system_name VARCHAR(200) NOT NULL,
    system_type VARCHAR(50) CHECK (system_type IN ('HVAC', 'PLUMBING', 'ELECTRICAL')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE equipment (
    equipment_id VARCHAR(50) PRIMARY KEY,
    equipment_name VARCHAR(200) NOT NULL,
    rated_power DECIMAL(10, 2),  -- kW
    system_id VARCHAR(50) REFERENCES systems(system_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_equipment_system ON equipment(system_id);
```

#### 2. 具体实现代码

**示例：Java Spring Boot 实现**
```java
@RestController
@RequestMapping("/api/v1/systems")
public class SystemController {
    @Autowired
    private SystemService systemService;

    @GetMapping("/{systemId}")
    public ResponseEntity<SystemDTO> getSystem(
        @PathVariable String systemId,
        @RequestParam(defaultValue = "false") boolean includeEquipment
    ) {
        try {
            SystemDTO system = systemService.findById(systemId, includeEquipment);
            return ResponseEntity.ok(system);
        } catch (SystemNotFoundException e) {
            return ResponseEntity.notFound().build();
        }
    }
}
```

#### 3. 部署配置

**示例：Kubernetes 部署**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cim-service
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: cim-service
        image: cim-service:1.0.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
```

## 跨层次映射示例

### 手术室温湿度控制

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

## 层次对比总结

| 层次 | 受众 | 关注点 | 工具 | 可变性 |
|-----|------|--------|------|--------|
| **CIM** | 业务专家 | 做什么 | 自然语言、流程图 | 高（需求变化） |
| **PIM** | 架构师 | 如何设计 | UML、OpenAPI | 中（设计演进） |
| **PSM** | 开发者 | 如何编码 | 代码、配置 | 低（实现稳定） |

## 核心价值

- **分离关注点**：业务 vs 技术分离
- **提高复用性**：PIM 可生成多种 PSM
- **隔离变化**：CIM 变化不直接影响 PSM
- **自动化生成**：减少手工编码

## 应用原则

1. 先 CIM，后 PIM，再 PSM
2. 每层都有明确的验证标准
3. 使用工具链支持自动转换
4. 保持层次间的追溯性
