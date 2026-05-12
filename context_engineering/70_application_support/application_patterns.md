# CIM 领域应用支撑模式

> 本文档回答: CIM 如何支撑具体的业务应用 -- 8 个查询模式, 每个 = 业务场景 + SPARQL 模式 + CIM 支撑方式。

## 模式总览

| # | 模式名 | 业务问题 | 跨源 | Named Graph |
|---|--------|---------|------|-------------|
| 1 | eq_full_status | 设备全状态 | IFC+BAS+CMMS | tbox+ifc+bas+cmms |
| 2 | floor_dashboard | 楼层设备看板 | IFC+BAS | tbox+ifc+bas |
| 3 | energy_anomaly | 能耗异常检测 | BAS+Pset | bas+pset |
| 4 | maintenance_due | 维保到期预警 | CMMS | cmms |
| 5 | fas_zone_status | 消防区域状态 | FAS+BAS | fas+bas |
| 6 | ifc_bas_cmms_triangle | 三源闭环验证 | IFC+BAS+CMMS | ALL |
| 7 | safety_event_mvp | 安全事件处置 | FAS+BAS+Event | fas+bas+event |
| 8 | bas_trend_24h | 时序趋势分析 | BAS(t0/t1/t2) | bas/* |

---

## 1. 设备全状态查询 (eq_full_status)

**业务需求**: "AHU-001 当前什么状态? 有没有未完成工单? BAS 读数正常吗?"

```sparql
SELECT ?device ?location ?basValue ?basUnit ?woStatus ?woDate
WHERE {
  GRAPH <graph/tbox> { ?device a cim:AirHandlingUnit }
  GRAPH <graph/ifc>  { ?device cim:locatedIn ?location }
  GRAPH <graph/bas/t0> {
    ?point cim-bacnet:bacnetPointOf ?device ;
           cim:hasValue ?basValue ;
           cim:hasUnit ?basUnit .
  }
  OPTIONAL {
    GRAPH <graph/cmms> {
      ?wo cim-cmms:maintenanceTarget ?device ;
          cim-cmms:woStatus ?woStatus ;
          cim-cmms:scheduledDate ?woDate .
      FILTER(?woStatus != "COMPLETED")
    }
  }
}
```

**CIM 支撑**: 三个 Named Graph 联邦, 一条查询返回设备位置+实时状态+维保情况。

## 2. 楼层设备看板 (floor_dashboard)

**业务需求**: "5 楼有哪些设备? 当前运行状况如何?"

```sparql
SELECT ?device ?type ?status ?value
WHERE {
  GRAPH <graph/ifc> {
    ?device cim:locatedIn ?room .
    ?room cim:isPartOf ?floor .
    ?floor rdfs:label "5F" .
  }
  GRAPH <graph/tbox> { ?device a ?type }
  OPTIONAL {
    GRAPH <graph/bas/t0> {
      ?point cim-bacnet:bacnetPointOf ?device ;
             cim:hasValue ?value .
    }
  }
}
```

**CIM 支撑**: 空间层次 (Building/Floor/Zone/Room) 与设备关联, 支持任意粒度的空间过滤。

## 3. 能耗异常检测 (energy_anomaly)

**业务需求**: "哪台设备功率偏离设计值超过 20%?"

```sparql
SELECT ?device ?designPower ?actualPower
       ((?actualPower - ?designPower) / ?designPower * 100 AS ?deviation)
WHERE {
  GRAPH <graph/pset> {
    ?device cim:designRatedPower ?designPower .
  }
  GRAPH <graph/bas/t0> {
    ?point cim-bacnet:bacnetPointOf ?device ;
           cim:pointType cim:PowerSensor ;
           cim:hasValue ?actualPower .
  }
  FILTER(ABS(?actualPower - ?designPower) / ?designPower > 0.20)
}
```

**CIM 支撑**: 设计参数 (Pset) 与 BAS 实时值的跨源比较 -- 这在传统系统中需要人工逐台核对。

## 4. 维保到期预警 (maintenance_due_30d)

**业务需求**: "未来 30 天有哪些 PM 工单到期? 涉及哪些关键设备?"

```sparql
SELECT ?wo ?device ?deviceType ?dueDate ?priority
WHERE {
  GRAPH <graph/cmms> {
    ?wo a cim-cmms:PreventiveWorkOrder ;
        cim-cmms:maintenanceTarget ?device ;
        cim-cmms:scheduledDate ?dueDate ;
        cim-cmms:priority ?priority .
    FILTER(?dueDate <= NOW() + "P30D"^^xsd:duration)
  }
  GRAPH <graph/tbox> { ?device a ?deviceType }
}
ORDER BY ?dueDate
```

**CIM 支撑**: CMMS 工单与 CIM 设备类型关联, 可按设备类型/生命安全等级排序优先级。

## 5. FAS 区域状态 (fas_zone_status)

**业务需求**: "2F 手术区消防探测器状态如何? 有无报警?"

```sparql
SELECT ?detector ?type ?status ?zone
WHERE {
  GRAPH <graph/fas> {
    ?detector a ?type ;
              cim:locatedIn ?room ;
              cim-fas:detectorStatus ?status .
    ?room cim:isPartOf ?zone .
    ?zone rdfs:label "2F-手术区" .
    FILTER(?type IN (cim:SmokeDetector, cim:HeatDetector, cim:ManualCallPoint))
  }
}
```

**CIM 支撑**: FAS 拓扑与空间层次关联, 支持按防火分区/楼层/功能区查询探测器状态。

## 6. 三源闭环验证 (ifc_bas_cmms_triangle)

**业务需求**: "BAS 报警的设备, CMMS 是否有对应维修工单?"

```sparql
SELECT ?device ?basAlarm ?alarmTime ?wo ?woStatus
WHERE {
  GRAPH <graph/bas/t2> {
    ?point cim-bacnet:bacnetPointOf ?device ;
           cim:alarmState "ACTIVE" ;
           cim:timestamp ?alarmTime .
  }
  GRAPH <graph/ifc> {
    ?device cim:locatedIn ?location .
  }
  OPTIONAL {
    GRAPH <graph/cmms> {
      ?wo cim-cmms:maintenanceTarget ?device ;
          cim-cmms:woStatus ?woStatus .
    }
  }
}
```

**CIM 支撑**: M3 的核心价值 -- 发现 BAS 报警但 CMMS 无工单的设备 (维修遗漏), 或 CMMS 有工单但 BAS 无异常的设备 (虚假工单)。验证结果: 11 行跨源关联记录。

## 7. 安全事件处置 (MVP -- L2 电气火灾)

**业务需求**: "烟感报警 → 预案匹配 → 动作执行 → 态势呈现 → 闭环"

**5 状态事件机**:
```
IDLE → DETECTED → CONFIRMED → RESPONDING → RESOLVED
```

**10 动作节点** (ActionChain 顺序执行):
1. 烟感信号确认 (BAS 读取)
2. 联动确认 (双探测器交叉验证)
3. 区域定位 (CIM 空间查询)
4. 预案匹配 (事件类型 → 预案库)
5. 风阀关闭 (BAS 指令 #1)
6. 排烟启动 (BAS 指令 #2)
7. 非消防电源切断 (BAS 指令 #3)
8. 广播疏散 (BAS 指令 #4)
9. 态势推送 (WebSocket → 可视化平台)
10. 事件闭环 (状态 → RESOLVED)

**4 条 BAS 指令**: 风阀关闭 / 排烟启动 / 非消防电源切断 / 广播疏散

**CIM 支撑**: 62 FAS 探测器 + 26 类 SecurityEvent + Named Graph `<graph/event>` 实时写入。
仿真验证: 10/10 动作完成, 840s < 900s 时限, 4 BAS 指令全部下发。

## 8. 时序趋势分析 (bas_trend_24h)

**业务需求**: "冷机 COP 24 小时变化趋势"

```sparql
SELECT ?timestamp ?cop
WHERE {
  { GRAPH <graph/bas/t0> {
      ?point cim-bacnet:bacnetPointOf cim-inst:CHL-19XR-001 ;
             cim:pointType cim:COPSensor ;
             cim:hasValue ?cop ;
             cim:timestamp ?timestamp .
    }
  } UNION {
    GRAPH <graph/bas/t1> {
      ?point cim-bacnet:bacnetPointOf cim-inst:CHL-19XR-001 ;
             cim:pointType cim:COPSensor ;
             cim:hasValue ?cop ;
             cim:timestamp ?timestamp .
    }
  } UNION {
    GRAPH <graph/bas/t2> {
      ?point cim-bacnet:bacnetPointOf cim-inst:CHL-19XR-001 ;
             cim:pointType cim:COPSensor ;
             cim:hasValue ?cop ;
             cim:timestamp ?timestamp .
    }
  }
}
ORDER BY ?timestamp
```

**CIM 支撑**: 3 个 BAS Named Graph 快照 (t0/t1/t2) 覆盖不同时间点, UNION 查询拼接时序。
未来 M6 接入真实 BAS 后, 可替换为 MQTT 流式写入 + 时序数据库。

---

## 上下文契约模板 (从旧 50_templates 迁移)

每个应用模式可定义为标准化的上下文契约:

```yaml
pattern_id: eq_full_status
context_input:
  required:
    - source: "graph/tbox"
      subset: "设备类定义"
      retrieval: sparql_select
      cache_ttl: long
    - source: "graph/ifc"
      subset: "设备-空间关联"
      retrieval: sparql_select
      cache_ttl: long
    - source: "graph/bas/t0"
      subset: "当前 BAS 读数"
      retrieval: sparql_select
      cache_ttl: none
  optional:
    - source: "graph/cmms"
      subset: "未完成工单"
      retrieval: sparql_select
      cache_ttl: short
quality_gate:
  shacl_violation: 0
  cross_source_match: ">= 1 row"
```

此模板格式源自 Agent 上下文契约模板, 适配为应用查询模式的上下文定义。
详见原始模板: `context_engineering/50_templates_old/agent_context_template.md`
