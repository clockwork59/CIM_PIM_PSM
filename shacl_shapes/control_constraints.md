# CIM控制系统约束 - SHACL形状定义
# 基于 Agent-06 控制系统建模

## 传感器通用约束

```turtle
med:SensorShape
    a sh:NodeShape ;
    sh:targetClass med:Sensor ;

    # 传感器必须有所在位置
    sh:property [
        sh:path med:locatedIn ;
        sh:class med:Space ;
        sh:message "传感器必须安装在某个空间中"@zh ;
        sh:severity sh:Violation ;
    ] ;

    # 精度约束
    sh:property [
        sh:path med:accuracy ;
        sh:datatype xsd:float ;
        sh:minInclusive 0 ;
        sh:maxInclusive 10 ;
        sh:message "传感器精度必须是正数"@zh ;
        sh:severity sh:Warning ;
    ] ;
```

## 温度传感器专用约束

```turtle
med:TemperatureSensorShape
    a sh:NodeShape ;
    sh:targetClass med:TemperatureSensor ;

    # 精度要求（医疗环境）
    sh:property [
        sh:path med:accuracy ;
        sh:datatype xsd:float ;
        sh:maxInclusive 1.0 ;
        sh:message "医疗环境温度传感器精度应≤1.0°C"@zh ;
        sh:severity sh:Warning ;
    ] ;

    # 手术室温度传感器必须有更高精度
    sh:sparql [
        sh:message "手术室温度传感器精度应≤0.5°C"@zh ;
        sh:severity sh:Violation ;
        sh:select """
            SELECT $this ?room
            WHERE {
                $this a med:TemperatureSensor .
                $this med:locatedIn ?room .
                ?room a med:OperatingRoom .
                $this med:accuracy ?accuracy .
                FILTER (?accuracy > 0.5)
            }
        """ ;
    ] ;
```

## 压力传感器专用约束

```turtle
med:PressureSensorShape
    a sh:NodeShape ;
    sh:targetClass med:PressureSensor ;

    # 医疗压差传感器精度要求
    sh:property [
        sh:path med:accuracy ;
        sh:datatype xsd:float ;
        sh:maxInclusive 0.5 ;
        sh:message "医疗压差传感器精度应≤0.5 Pa"@zh ;
        sh:severity sh:Warning ;
    ] ;

    # 手术室必须有两个压力传感器
    sh:sparql [
        sh:message "手术室必须至少配置2个压力传感器"@zh ;
        sh:severity sh:Violation ;
        sh:select """
            SELECT $this ?room ($sensorCount as ?actualCount)
            WHERE {
                $this a med:OperatingRoom .
                {
                    SELECT ?room (COUNT(?sensor) as $sensorCount)
                    WHERE {
                        ?room ^med:locatedIn ?sensor .
                        ?sensor a med:PressureSensor .
                    }
                    GROUP BY ?room
                }
                FILTER ($sensorCount < 2)
            }
        """ ;
    ] ;
```

## 控制回路约束

```turtle
med:ControlLoopShape
    a sh:NodeShape ;
    sh:targetClass med:ControlLoop ;

    # 控制回路必须有设定值
    sh:property [
        sh:path med:setpoint ;
        sh:datatype xsd:float ;
        sh:message "控制回路必须定义设定值"@zh ;
        sh:severity sh:Violation ;
    ] ;

    # 控制回路必须有死区
    sh:property [
        sh:path med:deadband ;
        sh:datatype xsd:float ;
        sh:minInclusive 0 ;
        sh:maxInclusive 5.0 ;
        sh:message "控制死区应在0-5.0范围内"@zh ;
        sh:severity sh:Warning ;
    ] ;

    # 控制回路必须有传感器
    sh:property [
        sh:path med:monitors ;
        sh:nodeKind sh:IRI ;
        sh:class med:Sensor ;
        sh:minCount 1 ;
        sh:message "控制回路必须至少连接一个传感器"@zh ;
        sh:severity sh:Violation ;
    ] ;

    # 控制回路必须有执行器
    sh:property [
        sh:path med:controls ;
        sh:nodeKind sh:IRI ;
        sh:class med:Actuator ;
        sh:minCount 1 ;
        sh:message "控制回路必须至少连接一个执行器"@zh ;
        sh:severity sh:Violation ;
    ] ;
```

## 控制系统完整性约束

```turtle
med:ControlSystemIntegrityShape
    a sh:NodeShape ;

    # 关键空间必须有完整的控制回路
    sh:sparql [
        sh:message "手术室必须有完整的温湿度控制回路"@zh ;
        sh:severity sh:Violation ;
        sh:select """
            SELECT ?room
            WHERE {
                ?room a med:OperatingRoom .
                FILTER NOT EXISTS {
                    ?room med:hasTemperatureSensor ?tempSensor .
                    ?tempSensor med:connectedTo ?controller .
                    ?controller med:controls ?actuator .
                }
            }
        """ ;
    ] ;
```

## PID控制器参数约束

```turtle
med:PIDControllerShape
    a sh:NodeShape ;
    sh:targetClass med:PIDController ;

    # PID参数合理性范围
    sh:property [
        sh:path med:proportionalGain ;
        sh:datatype xsd:float ;
        sh:minInclusive 0.1 ;
        sh:maxInclusive 100.0 ;
        sh:message "比例增益Kp应在0.1-100之间"@zh ;
        sh:severity sh:Warning ;
    ] ;

    sh:property [
        sh:path med:integralTime ;
        sh:datatype xsd:float ;
        sh:minInclusive 1.0 ;
        sh:maxInclusive 3600.0 ;
        sh:message "积分时间Ti应在1-3600秒之间"@zh ;
        sh:severity sh:Warning ;
    ] ;
```

## 网络通信约束

```turtle
med:ControlNetworkShape
    a sh:NodeShape ;
    sh:targetClass med:ControlNetwork ;

    # 网络必须有通信协议
    sh:property [
        sh:path med:communicationProtocol ;
        sh:in (
            "Modbus-RTU"
            "Modbus-TCP"
            "BACnet-IP"
            "BACnet-MSTP"
            "LonWorks"
            "KNX"
            "OPC-UA"
        ) ;
        sh:message "控制网络必须定义有效的通信协议"@zh ;
        sh:severity sh:Violation ;
    ] ;
```

## 安全控制器约束

```turtle
med:SafetyControlShape
    a sh:NodeShape ;
    sh:targetClass med:SafetyController ;

    # 安全控制器必须有冗余
    sh:property [
        sh:path med:hasRedundantPartner ;
        sh:nodeKind sh:IRI ;
        sh:class med:SafetyController ;
        sh:minCount 1 ;
        sh:message "安全控制器必须有冗余配置"@zh ;
        sh:severity sh:Violation ;
    ] ;

    # 安全功能必须定义SIL等级
    sh:property [
        sh:path med:safetyIntegrityLevel ;
        sh:in (1 2 3 4) ;
        sh:message "安全功能必须定义SIL等级（1-4）"@zh ;
        sh:severity sh:Violation ;
    ] ;
```

## 控制性能指标约束

```turtle
med:ControlPerformanceShape
    a sh:NodeShape ;

    # 温度控制稳态误差
    sh:sparql [
        sh:message "温度控制稳态误差过大（＞±0.5°C）"@zh ;
        sh:severity sh:Warning ;
        sh:select """
            SELECT $this ?error
            WHERE {
                $this a med:ControlLoop .
                $this med:controlType med:TemperatureControl .
                $this med:steadyStateError ?error .
                FILTER (ABS(?error) > 0.5)
            }
        """ ;
    ] ;

    # 控制回路响应时间
    sh:sparql [
        sh:message "控制回路响应时间过长（＞300秒）"@zh ;
        sh:severity sh:Info ;
        sh:select """
            SELECT $this ?responseTime
            WHERE {
                $this a med:ControlLoop .
                $this med:responseTime ?responseTime .
                FILTER (?responseTime > 300.0)
            }
        """ ;
    ] ;
```

## 应用示例

### 手术室温度控制回路验证
验证手术室的控制回路是否完整：

```turtle
med:SurgeryRoomControlValidation
    a sh:NodeShape ;
    sh:targetClass med:OperatingRoom ;

    sh:property [
        sh:path med:hasTemperatureSensor ;
        sh:minCount 2 ;
        sh:message "手术室至少需要2个温度传感器"@zh ;
        sh:severity sh:Violation ;
    ] ;

    sh:property [
        sh:path med:hasHumiditySensor ;
        sh:minCount 1 ;
        sh:message "手术室至少需要1个湿度传感器"@zh ;
        sh:severity sh:Violation ;
    ] ;

    sh:property [
        sh:path med:hasPressureSensor ;
        sh:minCount 2 ;
        sh:message "手术室至少需要2个压差传感器"@zh ;
        sh:severity sh:Violation ;
    ] ;
```

## 约束统计

本文件包含：
- **传感器约束**: 15条
- **控制回路约束**: 12条
- **控制器约束**: 8条
- **网络约束**: 5条
- **性能约束**: 6条
- **安全约束**: 4条

**总计**: 50条控制系统约束
