# 示例: CIM-PIM-PSM 完整转换链

**文档 ID**: `CIMU-CASE-FULL-TRANSFORM-CHAIN`  
**版本**: v1.0  
**基于**: Singh & Sood CIM + Chungoora PIM/PSM 方法  
**场景**: 手术室温度控制从需求到实现的端到端转换

---

## 概述

本示例展示一个完整的 MDA 转换链：

```
业务需求 (CIM)
    ↓ 转换规则 1
领域概念 + UML 模型 (CIM细化)
    ↓ 转换规则 2
ECLIF 本体 + API 契约 (PIM)
    ↓ 转换规则 3
Python 代码 + PostgreSQL Schema (PSM)
```

**场景**: 手术室温度控制在手术期间必须维持在 21-24°C

---

## 第一层: CIM - 计算无关模型

### 业务需求 (自然语言)

```
手术室在手术期间必须保持温度在 21-24°C 范围内。
如果温度超出此范围，系统应自动调节并在无法恢复时告警。
护士应能查看实时温度和调节历史。
```

### CIM 用例图

```plantuml
@startuml
left to right direction

actor "手术室护士" as Nurse
actor "HVAC系统" as HVAC

rectangle "手术室环境监控" {
  usecase "监控手术室温度" as UC_Monitor
  usecase "自动温度调节" as UC_Control
  usecase "接收温度告警" as UC_Alert
  usecase "查看温度历史" as UC_History
}

Nurse --> UC_Monitor
Nurse --> UC_Alert
Nurse --> UC_History
UC_Monitor ..> UC_Control : <<include>>
HVAC --> UC_Control

@enduml
```

### CIM 活动图: 温度控制流程

```plantuml
@startuml
|手术室护士|
start
:开始手术;

|温度监控系统|
:锁定温度设定值
(21-24°C);

while (手术进行中?) is (是)
  :读取温度传感器;
  
  if (温度在21-24°C?) then (是)
    :记录正常状态;
  else (否)
    if (温度<21°C?) then (是)
      :启动加热;
    else (否)
      :启动制冷;
    endif
    
    :等待5分钟;
    
    if (温度恢复?) then (否)
      :发送告警;
      
      |手术室护士|
      :接收告警;
      :评估情况;
      :手动介入或继续观察;
    endif
  endif
endwhile (否)

|手术室护士|
:结束手术;
stop
@enduml
```

### CIM 需求规格 (YAML)

```yaml
CIM_需求规格:
  需求编号: CIM-TEMP-001
  需求名称: 手术室温度控制
  
  业务规则:
    描述: "手术室在手术期间必须保持温度在21-24°C范围内"
    触发条件: "手术开始"
    约束:
      - 温度最小值: 21°C
      - 温度最大值: 24°C
      - 适用场景: 手术进行中
    
  功能需求:
    - 实时监测手术室温度
    - 自动调节温度至设定范围
    - 超限时发出告警
    - 记录所有温度数据和调节动作
    
  非功能需求:
    - 温度测量精度: ±0.5°C
    - 数据刷新频率: 每5秒
    - 告警延迟: < 30秒
    - 历史数据保留: 3年
    
  参与者:
    - 手术室护士: 监控、响应告警
    - HVAC系统: 执行温度调节
    - 温度监控系统: 监测、控制、告警
```

---

## 第二层: CIM → PIM 转换

### 转换规则

| CIM 元素 | PIM 元素 | 转换说明 |
|---------|---------|---------|
| 业务规则: 温度 21-24°C | ECLIF 完整性约束 | 形式化为逻辑约束 |
| 用例: 监控温度 | API: GET /temperature | RESTful 接口契约 |
| 用例: 自动调节 | ControlLoop 服务 | 控制回路抽象 |
| 活动: 读取传感器 | Sensor.read() | 设备接口方法 |
| 参与者: 护士 | Role: NURSE | RBAC 角色定义 |

### PIM: ECLIF 完整性约束

```eclif
; ============================================================
; PIM Level: ECLIF Constraints
; 从 CIM 业务规则转换
; ============================================================

; 类型声明
(Type OperatingRoom)
(Type TemperatureSensor)
(Type ControlLoop)
(Type SurgerySession)

; 属性
(BinaryFun currentTemperature)
(argProp currentTemperature 1 OperatingRoom)
(argProp currentTemperature 2 Float)

(BinaryFun surgeryStatus)
(argProp surgeryStatus 1 OperatingRoom)
(argProp surgeryStatus 2 SurgeryStatus)

; 完整性约束 1: 手术中温度范围
(integrityConstraint
  (=> (and (OperatingRoom ?room)
           (surgeryStatus ?room IN_PROGRESS))
      (and (exists (?temp)
             (and (TemperatureSensor ?temp)
                  (locatedIn ?temp ?room)
                  (currentTemperature ?room ?t)
                  (>= ?t 21.0)
                  (<= ?t 24.0)))))
  HardIC
  "Operating room temperature must be 21-24°C during surgery.")

; 完整性约束 2: 传感器精度
(integrityConstraint
  (=> (and (TemperatureSensor ?sensor)
           (locatedIn ?sensor ?room)
           (isCriticalSensor ?sensor true))
      (exists (?accuracy)
        (and (hasAccuracy ?sensor ?accuracy)
             (<= ?accuracy 0.5))))
  HardIC
  "Temperature sensors in operating rooms must have accuracy <= 0.5°C.")
```

### PIM: API 契约 (OpenAPI)

```yaml
# 从 CIM 用例转换的 API 契约
openapi: 3.0.0
info:
  title: Operating Room Temperature API
  version: 1.0.0

paths:
  /api/v1/rooms/{roomId}/temperature:
    get:
      summary: 获取手术室当前温度
      description: 从 CIM 用例 "监控手术室温度" 转换
      parameters:
        - name: roomId
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: 当前温度数据
          content:
            application/json:
              schema:
                type: object
                properties:
                  roomId:
                    type: string
                  temperature:
                    type: number
                    description: 当前温度 (°C)
                  timestamp:
                    type: string
                    format: date-time
                  status:
                    type: string
                    enum: [NORMAL, LOW, HIGH]
                  setpoint:
                    type: object
                    properties:
                      min:
                        type: number
                        example: 21.0
                      max:
                        type: number
                        example: 24.0
        
        '404':
          description: 手术室不存在

  /api/v1/rooms/{roomId}/temperature/history:
    get:
      summary: 获取温度历史数据
      description: 从 CIM 用例 "查看温度历史" 转换
      parameters:
        - name: roomId
          in: path
          required: true
          schema:
            type: string
        - name: startTime
          in: query
          required: true
          schema:
            type: string
            format: date-time
        - name: endTime
          in: query
          required: true
          schema:
            type: string
            format: date-time
      responses:
        '200':
          description: 历史温度数据
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    timestamp:
                      type: string
                      format: date-time
                    temperature:
                      type: number
                    controlAction:
                      type: string
                      enum: [NONE, HEATING, COOLING]

  /api/v1/rooms/{roomId}/alerts:
    post:
      summary: 创建温度告警
      description: 从 CIM 用例 "接收温度告警" 转换 (内部API)
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                alertType:
                  type: string
                  enum: [TEMP_HIGH, TEMP_LOW, SENSOR_FAULT]
                severity:
                  type: string
                  enum: [WARNING, CRITICAL]
                message:
                  type: string
      responses:
        '201':
          description: 告警已创建
```

### PIM: 服务接口定义

```python
# PIM Level: Service Interface (Platform Independent)
# 从 CIM 用例 "自动温度调节" 转换

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum

class ControlAction(Enum):
    NONE = "none"
    HEATING = "heating"
    COOLING = "cooling"

class TemperatureStatus(Enum):
    NORMAL = "normal"
    LOW = "low"
    HIGH = "high"

@dataclass
class TemperatureReading:
    """PIM: 温度读数数据类"""
    room_id: str
    temperature: float
    timestamp: datetime
    sensor_id: str

@dataclass
class TemperatureSetpoint:
    """PIM: 温度设定值"""
    min_temp: float  # 21.0
    max_temp: float  # 24.0
    
class TemperatureControlService(ABC):
    """
    PIM: 温度控制服务接口
    
    从 CIM 用例 "自动温度调节" 转换
    平台无关的控制逻辑定义
    """
    
    @abstractmethod
    def get_current_temperature(self, room_id: str) -> TemperatureReading:
        """
        获取当前温度
        
        Args:
            room_id: 手术室ID
            
        Returns:
            当前温度读数
            
        Raises:
            RoomNotFoundException: 如果手术室不存在
        """
        pass
    
    @abstractmethod
    def evaluate_temperature_status(
        self, 
        reading: TemperatureReading,
        setpoint: TemperatureSetpoint
    ) -> TemperatureStatus:
        """
        评估温度状态
        
        Args:
            reading: 温度读数
            setpoint: 设定值范围
            
        Returns:
            温度状态 (NORMAL/LOW/HIGH)
        """
        pass
    
    @abstractmethod
    def calculate_control_action(
        self,
        status: TemperatureStatus,
        current_action: ControlAction
    ) -> ControlAction:
        """
        计算控制动作
        
        Args:
            status: 当前温度状态
            current_action: 当前控制动作
            
        Returns:
            建议的控制动作
        """
        pass
    
    @abstractmethod
    def execute_control_action(
        self,
        room_id: str,
        action: ControlAction
    ) -> bool:
        """
        执行控制动作
        
        Args:
            room_id: 手术室ID
            action: 控制动作
            
        Returns:
            是否执行成功
        """
        pass
    
    @abstractmethod
    def get_temperature_history(
        self,
        room_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> List[TemperatureReading]:
        """
        获取温度历史
        
        从 CIM 用例 "查看温度历史" 转换
        """
        pass
```

---

## 第三层: PIM → PSM 转换

### 转换规则

| PIM 元素 | PSM 元素 | 技术选择 |
|---------|---------|---------|
| ECLIF 约束 | PostgreSQL CHECK + 应用验证 | 混合实现 |
| API 契约 | FastAPI 路由 | Python FastAPI |
| Service 接口 | Python 类实现 | 业务逻辑层 |
| 数据模型 | SQLAlchemy ORM | 数据访问层 |

### PSM: 数据库 Schema (PostgreSQL)

```sql
-- PSM Level: Physical Data Model
-- 从 PIM ECLIF 约束和实体转换

-- 手术室表
CREATE TABLE operating_rooms (
    room_id VARCHAR(50) PRIMARY KEY,
    room_number VARCHAR(20) NOT NULL,
    room_type VARCHAR(50) DEFAULT 'OPERATING_ROOM',
    
    -- 从 ECLIF 约束转换: 温度设定值
    temp_setpoint_min DECIMAL(4,1) NOT NULL DEFAULT 21.0,
    temp_setpoint_max DECIMAL(4,1) NOT NULL DEFAULT 24.0,
    
    -- 约束: 设定值范围验证
    CONSTRAINT chk_temp_setpoint_range 
        CHECK (temp_setpoint_min < temp_setpoint_max),
    CONSTRAINT chk_temp_setpoint_valid
        CHECK (temp_setpoint_min >= 18.0 AND temp_setpoint_max <= 26.0),
    
    -- 手术状态
    surgery_status VARCHAR(20) DEFAULT 'IDLE',
    CONSTRAINT chk_surgery_status 
        CHECK (surgery_status IN ('IDLE', 'PREPARING', 'IN_PROGRESS', 'CLEANING')),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 温度传感器表
CREATE TABLE temperature_sensors (
    sensor_id VARCHAR(50) PRIMARY KEY,
    room_id VARCHAR(50) NOT NULL,
    sensor_location VARCHAR(100),
    
    -- 从 ECLIF 约束: 精度要求
    accuracy DECIMAL(3,1) NOT NULL DEFAULT 0.5,
    CONSTRAINT chk_sensor_accuracy 
        CHECK (accuracy > 0 AND accuracy <= 1.0),
    
    is_critical BOOLEAN DEFAULT true,
    calibration_date DATE,
    
    FOREIGN KEY (room_id) REFERENCES operating_rooms(room_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 温度读数历史表
CREATE TABLE temperature_readings (
    reading_id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(50) NOT NULL,
    room_id VARCHAR(50) NOT NULL,
    
    -- 温度值 (从 ECLIF 约束: 合理范围)
    temperature DECIMAL(4,1) NOT NULL,
    CONSTRAINT chk_temperature_range 
        CHECK (temperature >= 10.0 AND temperature <= 40.0),
    
    measured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- 控制动作记录
    control_action VARCHAR(20) DEFAULT 'NONE',
    CONSTRAINT chk_control_action 
        CHECK (control_action IN ('NONE', 'HEATING', 'COOLING')),
    
    FOREIGN KEY (sensor_id) REFERENCES temperature_sensors(sensor_id),
    FOREIGN KEY (room_id) REFERENCES operating_rooms(room_id)
);

-- 索引优化
CREATE INDEX idx_temp_readings_room_time 
    ON temperature_readings(room_id, measured_at DESC);

CREATE INDEX idx_temp_readings_recent 
    ON temperature_readings(measured_at DESC) 
    WHERE measured_at > CURRENT_TIMESTAMP - INTERVAL '24 hours';

-- 物化视图: 当前温度状态
CREATE MATERIALIZED VIEW current_temperature_status AS
SELECT 
    or2.room_id,
    or2.room_number,
    or2.surgery_status,
    or2.temp_setpoint_min,
    or2.temp_setpoint_max,
    tr.temperature as current_temp,
    tr.measured_at as last_reading_time,
    CASE 
        WHEN tr.temperature < or2.temp_setpoint_min THEN 'LOW'
        WHEN tr.temperature > or2.temp_setpoint_max THEN 'HIGH'
        ELSE 'NORMAL'
    END as temp_status
FROM operating_rooms or2
LEFT JOIN LATERAL (
    SELECT temperature, measured_at
    FROM temperature_readings
    WHERE room_id = or2.room_id
    ORDER BY measured_at DESC
    LIMIT 1
) tr ON true;

-- 刷新物化视图的函数
CREATE OR REPLACE FUNCTION refresh_temp_status()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY current_temperature_status;
END;
$$ LANGUAGE plpgsql;

-- 告警表
CREATE TABLE temperature_alerts (
    alert_id SERIAL PRIMARY KEY,
    room_id VARCHAR(50) NOT NULL,
    alert_type VARCHAR(20) NOT NULL,
    CONSTRAINT chk_alert_type 
        CHECK (alert_type IN ('TEMP_HIGH', 'TEMP_LOW', 'SENSOR_FAULT')),
    
    severity VARCHAR(20) NOT NULL,
    CONSTRAINT chk_severity 
        CHECK (severity IN ('WARNING', 'CRITICAL')),
    
    message TEXT,
    acknowledged BOOLEAN DEFAULT false,
    acknowledged_by VARCHAR(50),
    acknowledged_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (room_id) REFERENCES operating_rooms(room_id)
);
```

### PSM: Python 实现 (FastAPI)

```python
# PSM Level: Concrete Implementation
# 从 PIM Service 接口和 API 契约转换

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, String, DECIMAL, Boolean, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import List, Optional
import os

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/cim_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# PSM: Database Models (from PIM entities)
class OperatingRoomDB(Base):
    __tablename__ = "operating_rooms"
    
    room_id = Column(String(50), primary_key=True)
    room_number = Column(String(20), nullable=False)
    room_type = Column(String(50), default='OPERATING_ROOM')
    temp_setpoint_min = Column(DECIMAL(4,1), nullable=False, default=21.0)
    temp_setpoint_max = Column(DECIMAL(4,1), nullable=False, default=24.0)
    surgery_status = Column(String(20), default='IDLE')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class TemperatureSensorDB(Base):
    __tablename__ = "temperature_sensors"
    
    sensor_id = Column(String(50), primary_key=True)
    room_id = Column(String(50), nullable=False)
    accuracy = Column(DECIMAL(3,1), nullable=False, default=0.5)
    is_critical = Column(Boolean, default=True)
    calibration_date = Column(DateTime)

class TemperatureReadingDB(Base):
    __tablename__ = "temperature_readings"
    
    reading_id = Column(Integer, primary_key=True)
    sensor_id = Column(String(50), nullable=False)
    room_id = Column(String(50), nullable=False)
    temperature = Column(DECIMAL(4,1), nullable=False)
    measured_at = Column(DateTime, default=datetime.utcnow)
    control_action = Column(String(20), default='NONE')

# PSM: Pydantic Models (from PIM data classes)
class TemperatureReading(BaseModel):
    room_id: str
    temperature: float = Field(..., ge=10.0, le=40.0)
    timestamp: datetime
    sensor_id: str
    
    class Config:
        from_attributes = True

class TemperatureSetpoint(BaseModel):
    min_temp: float = Field(default=21.0, ge=18.0, le=26.0)
    max_temp: float = Field(default=24.0, ge=18.0, le=26.0)
    
    @property
    def is_valid(self) -> bool:
        return self.min_temp < self.max_temp

class TemperatureResponse(BaseModel):
    room_id: str
    temperature: float
    timestamp: datetime
    status: str  # NORMAL, LOW, HIGH
    setpoint: TemperatureSetpoint

# PSM: Service Implementation (from PIM interface)
class TemperatureControlServicePSM:
    """
    PSM: 温度控制服务具体实现
    从 PIM TemperatureControlService 转换
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_current_temperature(self, room_id: str) -> TemperatureReading:
        """获取当前温度 (PIM 接口实现)"""
        # 查询最新读数
        reading = self.db.query(TemperatureReadingDB).filter(
            TemperatureReadingDB.room_id == room_id
        ).order_by(TemperatureReadingDB.measured_at.desc()).first()
        
        if not reading:
            raise HTTPException(status_code=404, detail="Room not found or no readings")
        
        return TemperatureReading(
            room_id=reading.room_id,
            temperature=float(reading.temperature),
            timestamp=reading.measured_at,
            sensor_id=reading.sensor_id
        )
    
    def evaluate_temperature_status(
        self,
        reading: TemperatureReading,
        setpoint: TemperatureSetpoint
    ) -> str:
        """评估温度状态 (PIM 接口实现)"""
        if reading.temperature < setpoint.min_temp:
            return "LOW"
        elif reading.temperature > setpoint.max_temp:
            return "HIGH"
        return "NORMAL"
    
    def calculate_control_action(self, status: str) -> str:
        """计算控制动作 (PIM 接口实现)"""
        if status == "LOW":
            return "HEATING"
        elif status == "HIGH":
            return "COOLING"
        return "NONE"
    
    def get_temperature_history(
        self,
        room_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> List[TemperatureReading]:
        """获取温度历史 (PIM 接口实现)"""
        readings = self.db.query(TemperatureReadingDB).filter(
            TemperatureReadingDB.room_id == room_id,
            TemperatureReadingDB.measured_at >= start_time,
            TemperatureReadingDB.measured_at <= end_time
        ).order_by(TemperatureReadingDB.measured_at.desc()).all()
        
        return [
            TemperatureReading(
                room_id=r.room_id,
                temperature=float(r.temperature),
                timestamp=r.measured_at,
                sensor_id=r.sensor_id
            )
            for r in readings
        ]

# PSM: FastAPI Application (from PIM API contracts)
app = FastAPI(title="Operating Room Temperature API", version="1.0.0")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_service(db: Session = Depends(get_db)):
    return TemperatureControlServicePSM(db)

# PSM: API Endpoints (from PIM API contracts)
@app.get("/api/v1/rooms/{room_id}/temperature", response_model=TemperatureResponse)
async def get_temperature(
    room_id: str,
    service: TemperatureControlServicePSM = Depends(get_service)
):
    """
    获取手术室当前温度
    从 PIM API 契约实现
    """
    # 获取读数
    reading = service.get_current_temperature(room_id)
    
    # 获取设定值
    room = service.db.query(OperatingRoomDB).filter(
        OperatingRoomDB.room_id == room_id
    ).first()
    
    setpoint = TemperatureSetpoint(
        min_temp=float(room.temp_setpoint_min),
        max_temp=float(room.temp_setpoint_max)
    )
    
    # 评估状态
    status = service.evaluate_temperature_status(reading, setpoint)
    
    return TemperatureResponse(
        room_id=room_id,
        temperature=reading.temperature,
        timestamp=reading.timestamp,
        status=status,
        setpoint=setpoint
    )

@app.get("/api/v1/rooms/{room_id}/temperature/history")
async def get_temperature_history(
    room_id: str,
    start_time: datetime,
    end_time: datetime,
    service: TemperatureControlServicePSM = Depends(get_service)
):
    """
    获取温度历史数据
    从 PIM API 契约实现
    """
    return service.get_temperature_history(room_id, start_time, end_time)

# PSM: 控制循环任务 (背景任务)
from fastapi import BackgroundTasks

async def temperature_control_loop():
    """
    PSM: 自动控制循环
    从 CIM 活动图 "自动温度调节" 转换
    """
    db = SessionLocal()
    service = TemperatureControlServicePSM(db)
    
    try:
        # 获取所有手术中的房间
        active_rooms = db.query(OperatingRoomDB).filter(
            OperatingRoomDB.surgery_status == 'IN_PROGRESS'
        ).all()
        
        for room in active_rooms:
            # 读取当前温度
            try:
                reading = service.get_current_temperature(room.room_id)
            except HTTPException:
                continue
            
            # 评估状态
            setpoint = TemperatureSetpoint(
                min_temp=float(room.temp_setpoint_min),
                max_temp=float(room.temp_setpoint_max)
            )
            status = service.evaluate_temperature_status(reading, setpoint)
            
            # 计算控制动作
            action = service.calculate_control_action(status)
            
            # 记录读数和控制动作
            new_reading = TemperatureReadingDB(
                sensor_id=reading.sensor_id,
                room_id=room.room_id,
                temperature=reading.temperature,
                control_action=action,
                measured_at=datetime.utcnow()
            )
            db.add(new_reading)
            
            # 如果超限，创建告警
            if status in ["LOW", "HIGH"]:
                # 检查是否已有未确认告警
                # ... 告警逻辑 ...
                pass
        
        db.commit()
        
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 转换追踪矩阵

### 需求追踪

| CIM 需求 | PIM 设计 | PSM 实现 | 验证方法 |
|---------|---------|---------|---------|
| 温度 21-24°C | ECLIF 约束 | DB CHECK 约束 | 自动验证 |
| 精度 ±0.5°C | ECLIF 约束 | DB CHECK 约束 | 自动验证 |
| 自动调节 | ControlLoop 服务 | Python 服务类 | 单元测试 |
| 实时监测 | GET /temperature | FastAPI 端点 | API 测试 |
| 历史查询 | GET /history | SQL 查询 | 集成测试 |
| 告警通知 | Alert API | 告警表 + 逻辑 | E2E 测试 |

### 转换规则总结

```yaml
转换规则:
  
  CIM_to_PIM:
    业务规则: 
      转换目标: ECLIF 完整性约束
      规则: "每个 CIM 业务规则映射为一个 ECLIF integrityConstraint"
    
    用例:
      转换目标: API 契约 + 服务接口
      规则: "每个用例映射为一个 REST API 端点"
    
    活动:
      转换目标: 服务方法 + 算法
      规则: "活动步骤映射为服务方法调用序列"
    
    参与者:
      转换目标: RBAC 角色定义
      规则: "参与者映射为角色，权限从活动推导"
  
  PIM_to_PSM:
    ECLIF约束:
      转换目标: DB CHECK + 应用验证
      规则: "数值范围约束转为 CHECK，复杂约束转为应用逻辑"
    
    API契约:
      转换目标: FastAPI 端点
      规则: "OpenAPI 直接映射为 FastAPI 装饰器"
    
    服务接口:
      转换目标: Python 类
      规则: "抽象方法转为具体实现，添加数据库访问"
    
    数据类:
      转换目标: SQLAlchemy Model
      规则: "Pydantic model 转为 SQLAlchemy ORM"
```

---

## 验证检查表

### CIM 验证

- [ ] 业务需求清晰、可测试
- [ ] 用例覆盖所有需求
- [ ] 非功能需求可测量

### CIM→PIM 验证

- [ ] 每个 CIM 元素有 PIM 对应
- [ ] ECLIF 约束逻辑正确
- [ ] API 契约完整
- [ ] 服务接口可测试

### PIM→PSM 验证

- [ ] 数据库 Schema 符合范式
- [ ] CHECK 约束覆盖 ECLIF 规则
- [ ] API 端点实现契约
- [ ] 服务类通过单元测试

### 端到端验证

- [ ] CIM 需求可追溯至代码
- [ ] PIM 设计可反推至需求
- [ ] PSM 实现符合设计
- [ ] 所有层次保持一致

---

## 参考

- Singh, Y. & Sood, M. "The Impact of the Computational Independent Model"
- Chungoora, N., et al. "面向制造系统互操作性和知识共享的模型驱动本体方法"
- OMG MDA Guide Version 1.0.1
- FastAPI Documentation
- SQLAlchemy Documentation
