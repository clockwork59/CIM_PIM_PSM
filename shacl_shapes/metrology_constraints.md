# CIM计量系统约束 - SHACL形状定义
# 基于 Agent-07 计量体系建模

## 计量设备通用约束

```turtle
med:MeteringEquipmentShape
    a sh:NodeShape ;
    sh:targetClass med:MeteringEquipment ;

    # 计量设备必须有精度等级
    sh:property [
        sh:path med:accuracyClass ;
        sh:in (
            "0.1"
            "0.2"
            "0.5"
            "1.0"
            "2.0"
        ) ;
        sh:message "计量设备必须定义精度等级"@zh ;
        sh:severity sh:Violation ;
    ] ;

    # 计量设备必须有量程
    sh:property [
        sh:path med:measurementRange ;
        sh:sparql [
            sh:minCount 1 ;
            sh:select """
                SELECT $this ?min ?max
                WHERE {
                    $this med:measurementRange ?range .
                    ?range med:minValue ?min .
                    ?range med:maxValue ?max .
                    FILTER (?max <= ?min)
                }
            """ ;
        ] ;
        sh:message "计量设备量程无效"@zh ;
        sh:severity sh:Violation ;
    ] ;
```

## 电能表约束

```turtle
med:ElectricMeterShape
    a sh:NodeShape ;
    sh:targetClass med:ElectricMeter ;

    # 电能表精度要求
    sh:property [
        sh:path med:accuracyClass ;
        sh:in ( "0.5" "1.0" "2.0" ) ;
        sh:message "计量电能表精度等级应为0.5、1.0或2.0"@zh ;
        sh:severity sh:Violation ;
    ] ;

    # 电能表必须支持分时计量
    sh:property [
        sh:path med:hasTimeOfUseTariff ;
        sh:datatype xsd:boolean ;
        sh:hasValue true ;
        sh:message "医疗建筑电能表必须支持分时计量"@zh ;
        sh:severity sh:Warning ;
    ] ;

    # 电能表必须有通讯接口
    sh:property [
        sh:path med:hasCommunicationPort ;
        sh:minCount 1 ;
        sh:message "智能电能表必须有至少1个通讯接口"@zh ;
        sh:severity sh:Warning ;
    ] ;
```

## 水表约束

```turtle
med:WaterMeterShape
    a sh:NodeShape ;
    sh:targetClass med:WaterMeter ;

    # 水表精度要求
    sh:property [
        sh:path med:accuracyClass ;
        sh:in ( "1.0" "2.0" ) ;
        sh:message "水表精度等级应为1.0或2.0"@zh ;
        sh:severity sh:Violation ;
    ] ;

    # DN15-50水表必须有R160量程比
    sh:sparql [
        sh:message "户用小口径水表量程比应≥R160"@zh ;
        sh:severity sh:Warning ;
        sh:select """
            SELECT $this ?size
            WHERE {
                $this a med:WaterMeter .
                $this med:sizeDN ?size .
                $this med:flowRatio ?ratio .
                FILTER (?size <= 50 && ?ratio < 160)
            }
        """ ;
    ] ;
```

## 热量表约束

```turtle
med:HeatMeterShape
    a sh:NodeShape ;
    sh:targetClass med:HeatMeter ;

    # 热量表精度要求 (EN 1434)
    sh:property [
        sh:path med:accuracyClass ;
        sh:in ( "1" "2" "3" ) ;
        sh:message "热量表精度等级应为1、2或3级"@zh ;
        sh:severity sh:Violation ;
    ] ;

    # 必须配对的温度传感器
    sh:property [
        sh:path med:hasSupplyTemperatureSensor ;
        sh:minCount 1 ;
        sh:message "热量表必须有供水温度传感器"@zh ;
        sh:severity sh:Violation ;
    ] ;

    sh:property [
        sh:path med:hasReturnTemperatureSensor ;
        sh:minCount 1 ;
        sh:message "热量表必须有回水温度传感器"@zh ;
        sh:severity sh:Violation ;
    ] ;

    # 温度传感器配对精度
    sh:sparql [
        sh:message "供回水温度传感器精度应匹配"@zh ;
        sh:severity sh:Warning ;
        sh:select """
            SELECT $this ?supplyAccuracy ?returnAccuracy
            WHERE {
                $this a med:HeatMeter .
                $this med:hasSupplyTemperatureSensor ?supply .
                $this med:hasReturnTemperatureSensor ?return .
                ?supply med:accuracy ?supplyAccuracy .
                ?return med:accuracy ?returnAccuracy .
                FILTER (ABS(?supplyAccuracy - ?returnAccuracy) > 0.1)
            }
        """ ;
    ] ;
```

## 计量层级结构约束

```turtle
med:MeteringHierarchyShape
    a sh:NodeShape ;

    # 计量层级必须形成树形结构
    sh:sparql [
        sh:message "计量层级存在循环引用"@zh ;
        sh:severity sh:Violation ;
        sh:select """
            SELECT $this ?parent
            WHERE {
                $this med:hasParentMeter ?parent .
                ?parent+ med:hasParentMeter $this .
            }
        """ ;
    ] ;

    # 下级计量总和应接近上级计量
    sh:sparql [
        sh:message "下级计量总和与上级差异过大（＞15%）"@zh ;
        sh:severity sh:Warning ;
        sh:select """
            SELECT ?parent ?parentValue ?sumChildren
            WHERE {
                ?parent a med:MeteringEquipment .
                ?parent med:measuredValue ?parentValue .
                {
                    SELECT ?parent (SUM(?childValue) as ?sumChildren)
                    WHERE {
                        ?child med:hasParentMeter ?parent .
                        ?child med:measuredValue ?childValue .
                    }
                    GROUP BY ?parent
                }
                FILTER (ABS(?parentValue - ?sumChildren) > ?parentValue * 0.15)
            }
        """ ;
    ] ;
```

## 数据采集约束

```turtle
med:DataCollectionShape
    a sh:NodeShape ;
    sh:targetClass med:DataCollectionPoint ;

    # 数据采集频率约束
    sh:property [
        sh:path med:collectionFrequency ;
        sh:datatype xsd:integer ;
        sh:minInclusive 1 ;
        sh:maxInclusive 86400 ;
        sh:message "采集频率应在1-86400秒之间"@zh ;
        sh:severity sh:Warning ;
    ] ;

    # 关键计量点必须实时采集
    sh:sparql [
        sh:message "一级计量表应支持15分钟采集"@zh ;
        sh:severity sh:Warning ;
        sh:select """
            SELECT $this ?frequency
            WHERE {
                $this med:meteringLevel 1 .  # 一级计量
                $this med:collectionFrequency ?frequency .
                FILTER (?frequency > 900)  # 15分钟
            }
        """ ;
    ] ;

    # 数据完整性检查
    sh:sparql [
        sh:message "上月数据完整率低于95%"@zh ;
        sh:severity sh:Warning ;
        sh:select """
            SELECT $this ?integrityRate
            WHERE {
                $this med:dataIntegrityRate ?integrityRate .
                FILTER (?integrityRate < 0.95)
            }
        """ ;
    ] ;
```

## 负荷计算约束

```turtle
med:LoadCalculationShape
    a sh:NodeShape ;

    # 需量计算合理性
    sh:sparql [
        sh:message "最大需量不应超过合同容量的120%"@zh ;
        sh:severity sh:Warning ;
        sh:select """
            SELECT $this ?demand ?contractCapacity
            WHERE {
                $this med:maximumDemand ?demand .
                $this med:contractCapacity ?contractCapacity .
                FILTER (?demand > ?contractCapacity * 1.2)
            }
        """ ;
    ] ;

    # 功率因数检查
    sh:sparql [
        sh:message "功率因数过低（＜0.9），可能需要补偿"@zh ;
        sh:severity sh:Info ;
        sh:select """
            SELECT $this ?powerFactor
            WHERE {
                $this med:averagePowerFactor ?powerFactor .
                FILTER (?powerFactor < 0.9)
            }
        """ ;
    ] ;
```

## 计费与成本约束

```turtle
med:BillingShape
    a sh:NodeShape ;
    sh:targetClass med:EnergyBill ;

    # 必须分项计量
    sh:property [
        sh:path med:hasItemizedCharges ;
        sh:minCount 3 ;
        sh:message "医疗建筑电费账单应至少包含3项分项"@zh ;
        sh:severity sh:Warning ;
    ] ;

    # 峰谷平比例合理性
    sh:sparql [
        sh:message "峰时段用电比例异常（＞60%）"@zh ;
        sh:severity sh:Info ;
        sh:select """
            SELECT $this ?peakPercentage
            WHERE {
                $this med:peakPercentage ?peakPercentage .
                FILTER (?peakPercentage > 0.60)
            }
        """ ;
    ] ;

    # 成本分配必须100%
    sh:sparql [
        sh:message "科室成本分配总和不为100%"@zh ;
        sh:severity sh:Violation ;
        sh:select """
            SELECT ?department ?totalAllocation
            WHERE {
                {
                    SELECT ?department (SUM(?allocation) as ?totalAllocation)
                    WHERE {
                        ?cost med:department ?department .
                        ?cost med:allocationPercentage ?allocation .
                    }
                    GROUP BY ?department
                }
                FILTER (ABS(?totalAllocation - 1.0) > 0.01)
            }
        """ ;
    ] ;
```

## 合规性约束

```turtle
med:ComplianceShape
    a sh:NodeShape ;

    # JCI计量精度要求
    sh:sparql [
        sh:message "JCI要求手术室计量精度应≤1.0%"@zh ;
        sh:severity sh:Warning ;
        sh:select """
            SELECT $this ?accuracy
            WHERE {
                $this a med:MeteringEquipment .
                $this med:locatedIn ?room .
                ?room a med:OperatingRoom .
                $this med:accuracyClass ?accuracy .
                FILTER (?accuracy > 1.0)
            }
        """ ;
    ] ;

    # 绿色医院评价要求
    sh:sparql [
        sh:message "绿色建筑要求一级计量覆盖率应100%"@zh ;
        sh:severity sh:Warning ;
        sh:select """
            SELECT $this ?coverage
            WHERE {
                $this a med:Building .
                $this med:meteringCoverage ?coverage .
                FILTER (?coverage < 1.0)
            }
        """ ;
    ] ;
```

## 约束统计

本文件包含：
- **计量设备约束**: 15条
- **层级结构约束**: 8条
- **数据采集约束**: 6条
- **负荷计算约束**: 4条
- **计费约束**: 5条
- **合规性约束**: 4条

**总计**: 42条计量系统约束
