## 🧑‍💻 User


专家给出了两份意见，你需要综合这些意见，完成新的修订版V3.4

---
## 🤖 Assistant


根据两位专家（Gemini和Claude）的深度审计意见，我将对Agent-09 v3.3进行全面修订，生成v3.4版本。

---

# **Agent-09 统一领域模型建构指令 v3.4**

## **医疗建筑CIM集成框架 - 工程完备版**

---

# **版本修订说明**

```yaml
meta:
  document_id: "Agent-09-UDM-v3.4"
  version: "3.4.0"
  version_type: "ENGINEERING_COMPLETE"
  previous_version: "3.3.0"
  updated_date: "2025-01-17"
  
  expert_review_sources:
    - reviewer: "Gemini-Pro"
      rating: "A-"
      key_findings:
        - "N元关系超边陷阱"
        - "ID语义刚性风险"
        - "隐式关系推导黑盒化"
        - "缺乏构建清单"
    
    - reviewer: "Claude"
      rating: "8.5/10"
      key_findings:
        - "ID冲突检测不足"
        - "单位映射不全"
        - "列表合并策略不明确"
        - "缺少SHACL形式化约束"
        - "本体版本演进策略缺失"
        - "E2E验证示例缺失"
        - "错误处理策略缺失"
  
  v34_critical_additions:
    from_gemini:
      - "PHASE-E: 超边重构化模式（Hyperedge Reification）"
      - "PHASE-F: ID语义策略与别名机制"
      - "PHASE-G: 隐式关系推导规则集"
      - "PHASE-H: 构建清单与校验机制"
    
    from_claude:
      - "A.1.4: 内容寻址ID与去重机制"
      - "A.1.5: 完整单位映射表"
      - "A.1.6: 属性类型验证规则"
      - "B.2: 列表合并策略细化"
      - "B.3: 复杂冲突场景处理"
      - "B.4: 未定义属性处理策略"
      - "C.4: 索引性能与一致性机制"
      - "C.5: 索引查询API定义"
      - "D.2: SHACL形式化约束"
      - "D.3: OWL约束条件"
      - "D.4: 本体版本演进策略"
      - "D.5: 术语词汇表"
      - "PHASE-I: E2E验证示例"
      - "PHASE-J: 错误处理与恢复策略"
      - "PHASE-K: 性能优化指南"
  
  production_readiness:
    v33: "92%"
    v34_target: "98%"
```

---

# **修订内容索引**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Agent-09 v3.4 修订内容总览                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ 🔴 CRITICAL 修订（来自Gemini + Claude）                               │  │
│  ├───────────────────────────────────────────────────────────────────────┤  │
│  │ PHASE-E: 超边重构化模式（解决N元关系陷阱）                            │  │
│  │ PHASE-F: ID语义策略与别名机制（解决ID刚性风险）                       │  │
│  │ PHASE-G: 隐式关系推导规则集（消除推导黑盒）                           │  │
│  │ PHASE-H: 构建清单与校验机制（生产级完整性）                           │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ 🟠 HIGH 修订（PHASE-A/B/C/D 补强）                                    │  │
│  ├───────────────────────────────────────────────────────────────────────┤  │
│  │ A.1.4: 内容寻址ID与去重机制                                           │  │
│  │ A.1.5: 完整单位映射表（+40行）                                        │  │
│  │ A.1.6: 属性类型验证规则                                               │  │
│  │ B.2: 列表合并策略细化（+60行）                                        │  │
│  │ B.3: 复杂冲突场景处理（+80行）                                        │  │
│  │ B.4: 未定义属性处理策略（+70行）                                      │  │
│  │ C.4: 索引性能与一致性机制（+180行）                                   │  │
│  │ C.5: 索引查询API定义（+100行）                                        │  │
│  │ D.2: SHACL形式化约束（+200行）                                        │  │
│  │ D.3: OWL约束条件（+120行）                                            │  │
│  │ D.4: 本体版本演进策略（+100行）                                       │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ 🟡 MEDIUM 修订（跨阶段增强）                                          │  │
│  ├───────────────────────────────────────────────────────────────────────┤  │
│  │ PHASE-I: E2E验证示例（+300行）                                        │  │
│  │ PHASE-J: 错误处理与恢复策略（+150行）                                 │  │
│  │ PHASE-K: 性能优化指南（+100行）                                       │  │
│  │ D.5: 术语词汇表（+500行，独立文档）                                   │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  预计新增代码/规范行数: ~2,000行                                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# **PHASE-E: 超边重构化模式（Hyperedge Reification）**

## **Module-E.1: N元关系的RDF表示规范**

```yaml
hyperedge_reification_pattern:
  meta:
    purpose: "解决Gemini指出的'N元关系超边陷阱'——RDF本质是二元图，无法直接表示超边"
    solution: "采用重构化(Reification)模式，将超边转化为一等实体"
    priority: "🔴 CRITICAL"
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 问题分析
  # ═══════════════════════════════════════════════════════════════════════════
  problem_analysis:
    issue: |
      v3.3定义了 cim:Hyperedge 和 cim:FluidCircuitHyperedge，
      但未说明如何用属性描述超边连接的多个实体。
      
      Agent-09遇到连接 [Chiller, Pump, AHU] 的流体回路时，
      不知道该用什么属性把这三个设备关联起来。
    
    rdf_limitation: |
      RDF三元组结构：(Subject, Predicate, Object)
      本质上只能表示二元关系，无法直接画一条边连接三个节点。
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 重构化模式定义
  # ═══════════════════════════════════════════════════════════════════════════
  reification_pattern:
    description: "将N元关系转化为一个独立实体（超边实例），通过属性连接参与者"
    
    core_properties:
      - property: "cim:hasParticipant"
        description: "连接参与该超边关系的所有实体"
        range: "cim:Entity"
        cardinality: "2..*"
        
      - property: "cim:participantRole"
        description: "描述参与者在超边中的角色"
        range: "cim:ParticipantRole"
        
      - property: "cim:participantOrder"
        description: "参与者在序列中的顺序（用于有序超边）"
        range: "xsd:integer"
    
    role_enumeration:
      - "cim:SourceRole"      # 源头（如冷水机）
      - "cim:LoadRole"        # 负载（如AHU）
      - "cim:DriverRole"      # 驱动（如泵）
      - "cim:TransferRole"    # 传递（如管道）
      - "cim:ControlRole"     # 控制（如阀门）
      - "cim:MeteringRole"    # 计量（如流量计）
      - "cim:DistributionRole" # 分配（如分水器）
      - "cim:CollectionRole"  # 汇集（如集水器）
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 本体定义补充
  # ═══════════════════════════════════════════════════════════════════════════
  ontology_additions: |
    {
      "@id": "cim:Hyperedge",
      "@type": "owl:Class",
      "rdfs:label": {"@value": "超边", "@language": "zh"},
      "rdfs:comment": "连接多个顶点的N元关系实体，采用重构化模式表示"
    },
    
    {
      "@id": "cim:hasParticipant",
      "@type": "owl:ObjectProperty",
      "rdfs:domain": {"@id": "cim:Hyperedge"},
      "rdfs:range": {"@id": "cim:Entity"},
      "rdfs:label": {"@value": "有参与者", "@language": "zh"},
      "rdfs:comment": "连接超边与其参与实体"
    },
    
    {
      "@id": "cim:Participation",
      "@type": "owl:Class",
      "rdfs:label": {"@value": "参与关系", "@language": "zh"},
      "rdfs:comment": "描述实体在超边中的参与详情，包括角色和顺序"
    },
    
    {
      "@id": "cim:hasParticipation",
      "@type": "owl:ObjectProperty",
      "rdfs:domain": {"@id": "cim:Hyperedge"},
      "rdfs:range": {"@id": "cim:Participation"},
      "rdfs:label": {"@value": "有参与详情", "@language": "zh"}
    },
    
    {
      "@id": "cim:participant",
      "@type": "owl:ObjectProperty",
      "rdfs:domain": {"@id": "cim:Participation"},
      "rdfs:range": {"@id": "cim:Entity"},
      "rdfs:label": {"@value": "参与者", "@language": "zh"}
    },
    
    {
      "@id": "cim:participantRole",
      "@type": "owl:ObjectProperty",
      "rdfs:domain": {"@id": "cim:Participation"},
      "rdfs:range": {"@id": "cim:ParticipantRole"},
      "rdfs:label": {"@value": "参与角色", "@language": "zh"}
    },
    
    {
      "@id": "cim:participantOrder",
      "@type": "owl:DatatypeProperty",
      "rdfs:domain": {"@id": "cim:Participation"},
      "rdfs:range": {"@id": "xsd:integer"},
      "rdfs:label": {"@value": "参与顺序", "@language": "zh"}
    },
    
    {
      "@id": "cim:ParticipantRole",
      "@type": "owl:Class",
      "rdfs:label": {"@value": "参与者角色", "@language": "zh"},
      "owl:oneOf": [
        {"@id": "cim:SourceRole"},
        {"@id": "cim:LoadRole"},
        {"@id": "cim:DriverRole"},
        {"@id": "cim:TransferRole"},
        {"@id": "cim:ControlRole"},
        {"@id": "cim:MeteringRole"},
        {"@id": "cim:DistributionRole"},
        {"@id": "cim:CollectionRole"}
      ]
    }
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 完整JSON-LD示例
  # ═══════════════════════════════════════════════════════════════════════════
  complete_example: |
    {
      "@context": "ontology/cim_context.jsonld",
      "@id": "HYP-CHW-LOOP-001",
      "@type": ["cim:FluidCircuitHyperedge", "cim:Hyperedge"],
      "rdfs:label": {"@value": "冷冻水主回路", "@language": "zh"},
      
      "cim:circuitMedium": "cim-flow:ChilledWater",
      "cim:closedLoop": true,
      
      "cim:hasParticipation": [
        {
          "@type": "cim:Participation",
          "cim:participant": {"@id": "EQP-HVAC-CH-001"},
          "cim:participantRole": {"@id": "cim:SourceRole"},
          "cim:participantOrder": 1,
          "rdfs:comment": "冷水机组作为冷源"
        },
        {
          "@type": "cim:Participation",
          "cim:participant": {"@id": "EQP-HVAC-CHWP-PRI-001"},
          "cim:participantRole": {"@id": "cim:DriverRole"},
          "cim:participantOrder": 2,
          "rdfs:comment": "一次泵驱动流动"
        },
        {
          "@type": "cim:Participation",
          "cim:participant": {"@id": "NODE-CHW-HEADER-SUPPLY"},
          "cim:participantRole": {"@id": "cim:DistributionRole"},
          "cim:participantOrder": 3,
          "rdfs:comment": "供水分水器分配"
        },
        {
          "@type": "cim:Participation",
          "cim:participant": {"@id": "EQP-HVAC-AHU-001"},
          "cim:participantRole": {"@id": "cim:LoadRole"},
          "cim:participantOrder": 4,
          "rdfs:comment": "空调箱作为负载"
        },
        {
          "@type": "cim:Participation",
          "cim:participant": {"@id": "NODE-CHW-HEADER-RETURN"},
          "cim:participantRole": {"@id": "cim:CollectionRole"},
          "cim:participantOrder": 5,
          "rdfs:comment": "回水集水器汇集"
        }
      ],
      
      "cim:sourceAgent": ["Agent-04", "Agent-05"]
    }
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 简化表示法（向后兼容）
  # ═══════════════════════════════════════════════════════════════════════════
  simplified_representation:
    description: "对于不需要角色和顺序的简单场景，可使用简化形式"
    
    example: |
      {
        "@id": "HYP-POWER-FEED-001",
        "@type": "cim:ElectricalCircuitHyperedge",
        "cim:hasParticipant": [
          {"@id": "EQP-ELEC-TX-001"},
          {"@id": "EQP-ELEC-MDB-001"},
          {"@id": "EQP-ELEC-DP-L3-001"}
        ],
        "rdfs:comment": "简化形式：仅列出参与者，不指定角色和顺序"
      }
    
    conversion_rule: |
      当需要详细信息时，可将简化形式展开为完整形式：
      
      hasParticipant: [A, B, C]
        ↓ 转换为
      hasParticipation: [
        {participant: A, order: 1},
        {participant: B, order: 2},
        {participant: C, order: 3}
      ]
```

---

# **PHASE-F: ID语义策略与别名机制**

## **Module-F.1: 解决ID语义刚性问题**

```yaml
id_semantic_strategy:
  meta:
    purpose: "解决Gemini指出的'ID语义刚性风险'——ID中包含易变属性导致系统脆弱"
    solution: "采用半透明ID + 别名机制"
    priority: "🔴 CRITICAL"
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 问题场景分析
  # ═══════════════════════════════════════════════════════════════════════════
  problem_scenarios:
    
    scenario_1_space_function_change:
      description: "空间功能变更"
      example: |
        原始：SPC-L3-OR-001（手术室）
        变更：改建为ICU
        问题：按规则ID应变为 SPC-L3-ICU-xxx
        后果：所有引用该空间的外键失效
    
    scenario_2_cross_floor_space:
      description: "跨层空间"
      example: |
        中庭跨越 L1-L3
        问题：{floor}字段该填什么？
        后果：填L1会导致L3索引查不到
    
    scenario_3_equipment_relocation:
      description: "设备迁移"
      example: |
        原始：EQP-HVAC-AHU-L3-001
        变更：从L3迁移到L4
        问题：ID中的L3需要更新
        后果：资产管理系统引用失效
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 解决方案：半透明ID + 别名机制
  # ═══════════════════════════════════════════════════════════════════════════
  solution_design:
    
    strategy_1_semi_opaque_id:
      description: "半透明ID：保留类型前缀，但移除易变属性"
      
      old_pattern: "SPC-{floor}-{type}-{seq:03d}"
      new_pattern: "SPC-{hash8}-{seq:03d}"
      
      hash_composition: |
        hash8 = SHA256(
          initial_type +      # 创建时的类型
          initial_location +  # 创建时的位置
          creation_timestamp  # 创建时间戳
        )[:8]
      
      examples:
        - old: "SPC-L3-OR-001"
          new: "SPC-a1b2c3d4-001"
          comment: "hash基于初始属性，变更后ID不变"
        
        - old: "EQP-HVAC-CH-L3-001"
          new: "EQP-7f8e9d0c-001"
          comment: "设备ID不再包含位置"
    
    strategy_2_alias_mechanism:
      description: "别名机制：为每个实体维护人类可读的别名"
      
      ontology_addition: |
        {
          "@id": "cim:hasAlias",
          "@type": "owl:DatatypeProperty",
          "rdfs:domain": {"@id": "cim:Entity"},
          "rdfs:range": {"@id": "xsd:string"},
          "rdfs:label": {"@value": "别名", "@language": "zh"},
          "rdfs:comment": "人类可读的别名，可随实体属性变化而更新"
        },
        
        {
          "@id": "cim:canonicalAlias",
          "@type": "owl:DatatypeProperty",
          "rdfs:subPropertyOf": {"@id": "cim:hasAlias"},
          "rdfs:label": {"@value": "规范别名", "@language": "zh"},
          "rdfs:comment": "当前有效的主别名，遵循命名规范"
        },
        
        {
          "@id": "cim:historicalAlias",
          "@type": "owl:DatatypeProperty",
          "rdfs:subPropertyOf": {"@id": "cim:hasAlias"},
          "rdfs:label": {"@value": "历史别名", "@language": "zh"},
          "rdfs:comment": "曾经使用过的别名，保留用于向后兼容"
        }
      
      example: |
        {
          "@id": "SPC-a1b2c3d4-001",
          "@type": "cim-space:ICU",
          
          "cim:canonicalAlias": "L3-ICU-01",
          "cim:historicalAlias": ["L3-OR-01"],
          
          "rdfs:comment": "原为手术室(L3-OR-01)，2025年改建为ICU"
        }
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 别名注册表
  # ═══════════════════════════════════════════════════════════════════════════
  alias_registry:
    description: "维护ID到别名的双向映射"
    
    structure: |
      {
        "registry_version": "1.0",
        "updated_at": "2025-01-17T12:00:00Z",
        
        "id_to_alias": {
          "SPC-a1b2c3d4-001": {
            "canonical": "L3-ICU-01",
            "historical": ["L3-OR-01"],
            "valid_from": "2025-01-01"
          }
        },
        
        "alias_to_id": {
          "L3-ICU-01": "SPC-a1b2c3d4-001",
          "L3-OR-01": "SPC-a1b2c3d4-001"
        }
      }
    
    lookup_algorithm: |
      def resolve_id(reference: str) -> str:
          """
          解析引用，支持ID或别名
          """
          # 如果是完整ID格式，直接返回
          if matches_id_pattern(reference):
              return reference
          
          # 否则视为别名，查找注册表
          if reference in alias_registry["alias_to_id"]:
              return alias_registry["alias_to_id"][reference]
          
          raise AliasNotFoundError(f"Unknown reference: {reference}")
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 跨层空间处理
  # ═══════════════════════════════════════════════════════════════════════════
  cross_floor_handling:
    description: "处理跨越多层的空间（中庭、电梯井等）"
    
    solution: |
      1. ID不包含楼层信息（采用半透明ID）
      2. 使用新增属性描述跨层关系
    
    ontology_addition: |
      {
        "@id": "cim-space:spansFloors",
        "@type": "owl:ObjectProperty",
        "rdfs:domain": {"@id": "cim-space:Space"},
        "rdfs:range": {"@id": "cim-space:Floor"},
        "rdfs:label": {"@value": "跨越楼层", "@language": "zh"},
        "rdfs:comment": "空间跨越的所有楼层"
      },
      
      {
        "@id": "cim-space:primaryFloor",
        "@type": "owl:ObjectProperty",
        "rdfs:domain": {"@id": "cim-space:Space"},
        "rdfs:range": {"@id": "cim-space:Floor"},
        "rdfs:label": {"@value": "主楼层", "@language": "zh"},
        "rdfs:comment": "空间的主要所属楼层（用于默认索引）"
      }
    
    example: |
      {
        "@id": "SPC-e5f6g7h8-001",
        "@type": "cim-space:Atrium",
        "rdfs:label": "主中庭",
        
        "cim-space:primaryFloor": {"@id": "FLR-L1"},
        "cim-space:spansFloors": [
          {"@id": "FLR-L1"},
          {"@id": "FLR-L2"},
          {"@id": "FLR-L3"}
        ],
        
        "cim:canonicalAlias": "ATRIUM-MAIN"
      }
```

---

# **PHASE-G: 隐式关系推导规则集**

## **Module-G.1: 显性化关系推导逻辑**

```yaml
implicit_relationship_rules:
  meta:
    purpose: "解决Gemini指出的'隐式关系推导黑盒化'——'从上下文推导'是危险的黑盒"
    solution: "将推导逻辑显性化为规则集"
    priority: "🔴 CRITICAL"
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 规则引擎框架
  # ═══════════════════════════════════════════════════════════════════════════
  rule_engine_framework:
    description: "基于条件-动作的关系推导规则引擎"
    
    rule_structure:
      - rule_id: "规则唯一标识"
      - rule_name: "规则名称"
      - priority: "执行优先级（数字越小优先级越高）"
      - conditions: "触发条件（SPARQL模式或逻辑表达式）"
      - actions: "执行动作（创建关系）"
      - confidence: "推导置信度（0-1）"
      - source_agents: "规则依赖的Agent来源"
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 服务关系推导规则
  # ═══════════════════════════════════════════════════════════════════════════
  serves_relationship_rules:
    
    rule_1_equipment_in_same_service_zone:
      rule_id: "RULE-SERVES-001"
      rule_name: "服务区内设备服务关系"
      priority: 1
      
      conditions: |
        # 条件：设备和空间位于同一个服务区
        Equipment(?eq) ∧ Space(?sp) ∧ ServiceZone(?sz) ∧
        locatedInZone(?eq, ?sz) ∧ containsSpace(?sz, ?sp)
      
      actions: |
        # 动作：创建服务关系
        CREATE cim-couple:serves(?eq, ?sp)
      
      confidence: 0.95
      source_agents: ["Agent-03", "Agent-05"]
      
      example: |
        前提：
          - AHU-001 位于 ServiceZone-OR-3F
          - OR-01 位于 ServiceZone-OR-3F
        推导：
          - AHU-001 cim-couple:serves OR-01
    
    rule_2_ahu_serves_downstream_spaces:
      rule_id: "RULE-SERVES-002"
      rule_name: "AHU下游风管服务关系"
      priority: 2
      
      conditions: |
        # 条件：AHU通过风管连接到空间的送风口
        AHU(?ahu) ∧ Space(?sp) ∧ DiffuserTerminal(?diff) ∧
        feedsTo(?ahu, ?duct) ∧ feedsTo+(?duct, ?diff) ∧
        locatedIn(?diff, ?sp)
      
      actions: |
        CREATE cim-couple:serves(?ahu, ?sp)
        SET cim-couple:serviceType = "Air_Conditioning"
      
      confidence: 0.98
      source_agents: ["Agent-01", "Agent-04"]
    
    rule_3_chiller_indirect_serves:
      rule_id: "RULE-SERVES-003"
      rule_name: "冷水机间接服务关系"
      priority: 3
      
      conditions: |
        # 条件：冷水机通过冷冻水管路连接到AHU，AHU服务于空间
        Chiller(?ch) ∧ AHU(?ahu) ∧ Space(?sp) ∧
        ChilledWaterPath+(?ch, ?ahu) ∧ serves(?ahu, ?sp)
      
      actions: |
        CREATE cim-couple:indirectlyServes(?ch, ?sp)
        SET cim-couple:mediatedBy = ?ahu
      
      confidence: 0.90
      source_agents: ["Agent-01", "Agent-04", "Agent-05"]
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 流动关系推导规则
  # ═══════════════════════════════════════════════════════════════════════════
  flow_relationship_rules:
    
    rule_4_pipe_segment_feeds:
      rule_id: "RULE-FLOW-001"
      rule_name: "管段流动方向推导"
      priority: 1
      
      conditions: |
        # 条件：两个设备通过管段连接，且管段有定义的流动方向
        Equipment(?eq1) ∧ Equipment(?eq2) ∧ PipeSegment(?pipe) ∧
        connectedTo(?eq1, ?pipe) ∧ connectedTo(?eq2, ?pipe) ∧
        flowDirection(?pipe, ?dir) ∧
        upstreamConnection(?pipe, ?eq1) ∧ downstreamConnection(?pipe, ?eq2)
      
      actions: |
        CREATE cim-flow:feedsTo(?eq1, ?eq2)
        SET cim-flow:medium = medium(?pipe)
        SET cim-flow:viaPipe = ?pipe
      
      confidence: 0.99
      source_agents: ["Agent-01", "Agent-04"]
    
    rule_5_pump_creates_flow:
      rule_id: "RULE-FLOW-002"
      rule_name: "泵驱动流动推导"
      priority: 2
      
      conditions: |
        # 条件：泵的进出口连接
        Pump(?pump) ∧ Equipment(?inlet_eq) ∧ Equipment(?outlet_eq) ∧
        hasInlet(?pump, ?inlet) ∧ connectedTo(?inlet, ?inlet_eq) ∧
        hasOutlet(?pump, ?outlet) ∧ connectedTo(?outlet, ?outlet_eq)
      
      actions: |
        CREATE cim-flow:feedsTo(?inlet_eq, ?pump)
        CREATE cim-flow:feedsTo(?pump, ?outlet_eq)
        SET cim-flow:flowDriver = ?pump
      
      confidence: 0.99
      source_agents: ["Agent-01", "Agent-04"]
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 空间层级关系推导规则
  # ═══════════════════════════════════════════════════════════════════════════
  spatial_relationship_rules:
    
    rule_6_floor_contains_rooms:
      rule_id: "RULE-SPATIAL-001"
      rule_name: "楼层包含房间关系"
      priority: 1
      
      conditions: |
        Floor(?floor) ∧ Room(?room) ∧
        floorCode(?floor, ?fc) ∧ roomFloorCode(?room, ?fc)
      
      actions: |
        CREATE cim-space:contains(?floor, ?room)
        CREATE cim-space:isPartOf(?room, ?floor)
      
      confidence: 1.0
      source_agents: ["Agent-02"]
    
    rule_7_zone_aggregates_rooms:
      rule_id: "RULE-SPATIAL-002"
      rule_name: "功能区聚合房间关系"
      priority: 2
      
      conditions: |
        FunctionalZone(?zone) ∧ Room(?room) ∧
        zoneType(?zone, ?zt) ∧ roomFunction(?room, ?rf) ∧
        zoneFunctionMatch(?zt, ?rf)
      
      actions: |
        CREATE cim-space:aggregates(?zone, ?room)
      
      confidence: 0.85
      source_agents: ["Agent-02", "Agent-05"]
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 推导执行流程
  # ═══════════════════════════════════════════════════════════════════════════
  derivation_execution:
    algorithm: |
      def derive_implicit_relationships(entities: List, explicit_rels: List) -> List:
          """
          基于规则集推导隐式关系
          """
          derived_relationships = []
          rules = load_rules_sorted_by_priority()
          
          for rule in rules:
              # 1. 检查规则依赖的Agent数据是否可用
              if not all_agents_available(rule.source_agents):
                  log_warning(f"Skipping {rule.rule_id}: missing agent data")
                  continue
              
              # 2. 执行规则条件匹配
              matches = execute_sparql_pattern(rule.conditions, entities, explicit_rels)
              
              for match in matches:
                  # 3. 执行规则动作
                  new_rel = create_relationship(rule.actions, match)
                  new_rel["cim:derivedBy"] = rule.rule_id
                  new_rel["cim:derivationConfidence"] = rule.confidence
                  
                  # 4. 检查是否已存在（避免重复）
                  if not relationship_exists(new_rel, derived_relationships + explicit_rels):
                      derived_relationships.append(new_rel)
                      log_info(f"Derived: {new_rel['@id']} by {rule.rule_id}")
          
          return derived_relationships
    
    output_annotation: |
      所有推导的关系必须标注来源：
      
      {
        "@id": "REL-SERVES-AHU001-OR001",
        "@type": "cim-couple:ServesRelation",
        "cim:source": {"@id": "EQP-HVAC-AHU-001"},
        "cim:target": {"@id": "SPC-L3-OR-001"},
        
        "cim:derivedBy": "RULE-SERVES-001",
        "cim:derivationConfidence": 0.95,
        "cim:derivationTimestamp": "2025-01-17T12:00:00Z"
      }
```

---

# **PHASE-H: 构建清单与校验机制**

## **Module-H.1: Build Manifest定义**

```yaml
build_manifest_specification:
  meta:
    purpose: "解决Gemini指出的'缺乏构建清单'——生产级系统需要完整性验证"
    solution: "定义标准化的manifest.json结构"
    priority: "🔴 CRITICAL"
  
  # ═══════════════════════════════════════════════════════════════════════════
  # Manifest文件结构
  # ═══════════════════════════════════════════════════════════════════════════
  manifest_structure: |
    {
      "$schema": "https://cim.medical/schemas/manifest-v1.json",
      
      "build": {
        "id": "bld-20250117-001",
        "timestamp": "2025-01-17T12:00:00Z",
        "builder": "Agent-09",
        "builder_version": "3.4.0",
        "build_duration_seconds": 120
      },
      
      "bundle": {
        "name": "CIM_Bundle_XuanwuXiongan",
        "version": "2.0.0",
        "description": "宣武雄安医院CIM统一领域模型"
      },
      
      "ontology": {
        "version": "3.4.0",
        "namespace": "https://cim.medical/ontology/v3.4#",
        "hash": "sha256:a1b2c3d4e5f6..."
      },
      
      "files": {
        "ontology/cim_medical_ontology.jsonld": {
          "size_bytes": 16000,
          "sha256": "...",
          "entity_count": null,
          "type": "ontology"
        },
        "ontology/cim_medical_shapes.ttl": {
          "size_bytes": 8000,
          "sha256": "...",
          "constraint_count": 120,
          "type": "shacl"
        },
        "entities/cim_entities.jsonld": {
          "size_bytes": 840000,
          "sha256": "...",
          "entity_count": 2185,
          "type": "entities"
        },
        "relationships/cim_relationships.jsonld": {
          "size_bytes": 600000,
          "sha256": "...",
          "relationship_count": 4012,
          "derived_count": 1500,
          "explicit_count": 2512,
          "type": "relationships"
        },
        "index/global_xref_index.json": {
          "size_bytes": 24000,
          "sha256": "...",
          "type": "index"
        }
      },
      
      "agents": {
        "Agent-01": {"version": "1.0", "last_output": "2025-01-15T10:00:00Z"},
        "Agent-02": {"version": "1.2", "last_output": "2025-01-15T11:00:00Z"},
        "Agent-03": {"version": "2.2", "last_output": "2025-01-15T12:00:00Z"},
        "Agent-04": {"version": "1.0", "last_output": "2025-01-15T13:00:00Z"},
        "Agent-05": {"version": "2.1", "last_output": "2025-01-15T14:00:00Z"},
        "Agent-06": {"version": "1.0", "last_output": "2025-01-15T15:00:00Z"},
        "Agent-07": {"version": "1.0", "last_output": "2025-01-15T16:00:00Z"},
        "Agent-08": {"version": "3.0", "last_output": "2025-01-15T17:00:00Z"}
      },
      
      "validation": {
        "shacl_validation": {
          "passed": true,
          "violations": 0,
          "warnings": 5,
          "info": 12
        },
        "referential_integrity": {
          "passed": true,
          "dangling_references": 0
        },
        "schema_compliance": {
          "passed": true,
          "unknown_types": 0,
          "unknown_properties": 3
        }
      },
      
      "statistics": {
        "total_entities": 2185,
        "total_relationships": 4012,
        "by_type": {
          "cim-space:Space": 420,
          "cim-equip:Equipment": 1200,
          "cim-system:System": 25,
          "sosa:Sensor": 500,
          "other": 40
        },
        "by_agent": {
          "Agent-01": 320,
          "Agent-02": 420,
          "Agent-03": 1200,
          "Agent-05": 180,
          "Agent-06": 45,
          "Agent-07": 15,
          "Agent-08": 5
        }
      },
      
      "checksums": {
        "bundle_sha256": "sha256:final_bundle_hash...",
        "algorithm": "SHA-256"
      }
    }
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 校验流程
  # ═══════════════════════════════════════════════════════════════════════════
  verification_process:
    
    step_1_file_integrity:
      description: "验证所有文件的SHA256校验和"
      algorithm: |
        def verify_file_integrity(manifest: Dict, bundle_path: str) -> bool:
            for filename, meta in manifest["files"].items():
                file_path = os.path.join(bundle_path, filename)
                computed_hash = sha256_file(file_path)
                
                if computed_hash != meta["sha256"]:
                    log_error(f"File integrity check failed: {filename}")
                    return False
            
            log_info("All file integrity checks passed")
            return True
    
    step_2_referential_integrity:
      description: "验证所有引用的实体确实存在"
      algorithm: |
        def verify_referential_integrity(entities: List, relationships: List) -> Dict:
            entity_ids = {e["@id"] for e in entities}
            errors = []
            
            for rel in relationships:
                source = rel.get("cim:source", {}).get("@id")
                target = rel.get("cim:target", {}).get("@id")
                
                if source and source not in entity_ids:
                    errors.append(f"Dangling source: {source} in {rel['@id']}")
                if target and target not in entity_ids:
                    errors.append(f"Dangling target: {target} in {rel['@id']}")
            
            return {
                "passed": len(errors) == 0,
                "errors": errors
            }
    
    step_3_shacl_validation:
      description: "使用SHACL shapes验证数据符合约束"
      tool: "pyshacl 或 Apache Jena SHACL"
      command: |
        pyshacl -s ontology/cim_medical_shapes.ttl \
                -d entities/cim_entities.jsonld \
                -f human
    
    step_4_bundle_checksum:
      description: "计算整个Bundle的总校验和"
      algorithm: |
        def compute_bundle_checksum(bundle_path: str) -> str:
            """
            计算Bundle目录的综合校验和
            """
            hasher = hashlib.sha256()
            
            # 按固定顺序遍历所有文件
            for root, dirs, files in sorted(os.walk(bundle_path)):
                dirs.sort()
                for filename in sorted(files):
                    if filename == "manifest.json":
                        continue  # 跳过manifest本身
                    
                    file_path = os.path.join(root, filename)
                    with open(file_path, "rb") as f:
                        hasher.update(f.read())
            
            return f"sha256:{hasher.hexdigest()}"
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 生成脚本
  # ═══════════════════════════════════════════════════════════════════════════
  generation_script: |
    #!/usr/bin/env python3
    """
    generate_manifest.py - 生成CIM Bundle的manifest.json
    """
    
    import json
    import hashlib
    import os
    from datetime import datetime
    from pathlib import Path
    
    def generate_manifest(bundle_path: str) -> Dict:
        manifest = {
            "build": {
                "id": f"bld-{datetime.now().strftime('%Y%m%d')}-001",
                "timestamp": datetime.now().isoformat(),
                "builder": "Agent-09",
                "builder_version": "3.4.0"
            },
            "files": {},
            "validation": {},
            "statistics": {}
        }
        
        # 遍历文件计算校验和
        for file_path in Path(bundle_path).rglob("*.jsonld"):
            rel_path = str(file_path.relative_to(bundle_path))
            
            with open(file_path, "rb") as f:
                content = f.read()
                sha256 = hashlib.sha256(content).hexdigest()
            
            manifest["files"][rel_path] = {
                "size_bytes": len(content),
                "sha256": sha256
            }
        
        # 统计实体数量
        entities_file = Path(bundle_path) / "entities" / "cim_entities.jsonld"
        if entities_file.exists():
            with open(entities_file) as f:
                data = json.load(f)
                manifest["statistics"]["total_entities"] = len(data.get("@graph", []))
        
        return manifest
    
    if __name__ == "__main__":
        import sys
        bundle_path = sys.argv[1] if len(sys.argv) > 1 else "."
        manifest = generate_manifest(bundle_path)
        print(json.dumps(manifest, indent=2, ensure_ascii=False))
```

---

# **PHASE-A 补强（Claude审计修复）**

## **Module-A.1.4: 内容寻址ID与去重机制**

```yaml
content_addressable_id:
  meta:
    purpose: "解决Claude指出的'ID冲突检测不足'——合并时可能产生隐性冲突"
    solution: "基于内容哈希的确定性ID生成"
    priority: "🟠 HIGH"
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 内容寻址ID生成
  # ═══════════════════════════════════════════════════════════════════════════
  cai_generation:
    description: "基于实体内容的确定性ID，确保相同实体生成相同ID"
    
    algorithm: |
      def generate_deterministic_id(entity_dict: Dict, entity_type: str) -> str:
          """
          生成基于内容的确定性ID
          确保相同实体（来自不同Agent）生成相同ID
          """
          # 1. 提取规范化内容（排除易变属性）
          canonical_content = {
              "type": sorted(entity_dict.get("@type", [])),
              "key_attributes": extract_key_attributes(entity_dict, entity_type)
          }
          
          # 2. 计算内容哈希
          content_json = json.dumps(canonical_content, sort_keys=True)
          content_hash = hashlib.sha256(content_json.encode()).hexdigest()[:8]
          
          # 3. 生成ID
          type_prefix = TYPE_PREFIXES.get(entity_type, "ENT")
          seq = get_sequence_number(type_prefix, content_hash)
          
          return f"{type_prefix}-{content_hash}-{seq:03d}"
      
      def extract_key_attributes(entity: Dict, entity_type: str) -> Dict:
          """
          提取用于标识实体的关键属性
          """
          key_attrs = {}
          
          if entity_type == "Equipment":
              key_attrs = {
                  "manufacturer": entity.get("cim-equip:manufacturer"),
                  "model": entity.get("cim-equip:model"),
                  "serial": entity.get("cim-equip:serialNumber")
              }
          elif entity_type == "Space":
              key_attrs = {
                  "room_code": entity.get("cim-space:roomCode"),
                  "floor": entity.get("cim-space:floorCode")
              }
          elif entity_type == "System":
              key_attrs = {
                  "system_code": entity.get("cim-system:systemCode"),
                  "domain": entity.get("cim-system:domain")
              }
          
          # 移除None值
          return {k: v for k, v in key_attrs.items() if v is not None}
    
    deduplication: |
      def deduplicate_entities(entities: List[Dict]) -> List[Dict]:
          """
          基于内容哈希去重
          """
          seen_hashes = {}
          deduplicated = []
          
          for entity in entities:
              entity_type = entity["@type"][0]
              deterministic_id = generate_deterministic_id(entity, entity_type)
              
              if deterministic_id in seen_hashes:
                  # 发现重复，执行合并
                  existing = seen_hashes[deterministic_id]
                  merged = merge_duplicate_entities(existing, entity)
                  seen_hashes[deterministic_id] = merged
                  log_info(f"Merged duplicate: {deterministic_id}")
              else:
                  entity["@id"] = deterministic_id
                  seen_hashes[deterministic_id] = entity
          
          return list(seen_hashes.values())
```

## **Module-A.1.5: 完整单位映射表**

```yaml
complete_unit_mapping:
  meta:
    purpose: "解决Claude指出的'单位映射不全'"
    priority: "🟠 HIGH"
  
  unit_mappings:
    
    # 温度
    temperature:
      "degC": "unit:DEG_C"
      "℃": "unit:DEG_C"
      "°C": "unit:DEG_C"
      "K": "unit:K"
      "degF": "unit:DEG_F"
    
    # 功率与能量
    power:
      "kW": "unit:KiloW"
      "W": "unit:W"
      "MW": "unit:MegaW"
      "HP": "unit:HP"
      "RT": "unit:TON_FG"  # 冷吨
      "kWh": "unit:KiloW-HR"
      "MWh": "unit:MegaW-HR"
    
    # 流量
    flow_rate:
      "m³/h": "unit:M3-PER-HR"
      "m3/h": "unit:M3-PER-HR"
      "CMH": "unit:M3-PER-HR"
      "L/s": "unit:L-PER-SEC"
      "L/min": "unit:L-PER-MIN"
      "GPM": "unit:GAL_US-PER-MIN"
      "CFM": "unit:FT3-PER-MIN"
    
    # 压力
    pressure:
      "Pa": "unit:PA"
      "kPa": "unit:KiloPA"
      "MPa": "unit:MegaPA"
      "bar": "unit:BAR"
      "mbar": "unit:MilliBAR"
      "psi": "unit:PSI"
      "mmHg": "unit:MilliM_HG"
      "mmH2O": "unit:MilliM_H2O"
    
    # 面积与体积
    area:
      "m²": "unit:M2"
      "㎡": "unit:M2"
      "m2": "unit:M2"
      "ft²": "unit:FT2"
    
    volume:
      "m³": "unit:M3"
      "m3": "unit:M3"
      "L": "unit:L"
      "mL": "unit:MilliL"
    
    # 长度
    length:
      "m": "unit:M"
      "mm": "unit:MilliM"
      "cm": "unit:CentiM"
      "km": "unit:KiloM"
      "ft": "unit:FT"
      "in": "unit:IN"
    
    # 频率与转速
    frequency:
      "Hz": "unit:HZ"
      "kHz": "unit:KiloHZ"
      "rpm": "unit:REV-PER-MIN"
      "RPM": "unit:REV-PER-MIN"
    
    # 湿度与浓度
    humidity:
      "%RH": "unit:PERCENT_RH"
      "g/kg": "unit:GM-PER-KiloGM"
    
    concentration:
      "ppm": "unit:PPM"
      "ppb": "unit:PPB"
      "mg/L": "unit:MilliGM-PER-L"
      "mg/m³": "unit:MilliGM-PER-M3"
    
    # 效率与比值
    efficiency:
      "%": "unit:PERCENT"
      "COP": "unit:UNITLESS"
      "EER": "unit:UNITLESS"
      "SEER": "unit:UNITLESS"
    
    # 质量流量
    mass_flow:
      "kg/s": "unit:KiloGM-PER-SEC"
      "kg/h": "unit:KiloGM-PER-HR"
      "t/h": "unit:TONNE-PER-HR"
    
    # 时间
    time:
      "s": "unit:SEC"
      "min": "unit:MIN"
      "h": "unit:HR"
      "d": "unit:DAY"
    
    # 医疗特定单位
    medical:
      "mL/min": "unit:MilliL-PER-MIN"    # 医用气体流速
      "L/min/m²": "unit:L-PER-MIN-M2"    # 体表面积流速
      "ACH": "unit:PER-HR"               # 换气次数
      "particles/ft³": "unit:NUM-PER-FT3" # 颗粒计数
```

## **Module-A.1.6: 属性类型验证规则**

```yaml
property_validation_rules:
  meta:
    purpose: "解决Claude指出的'属性类型验证缺失'"
    priority: "🟠 HIGH"
  
  validation_framework:
    description: "在转换前进行严格的类型和值域检查"
    
    rules:
      
      # 数值属性验证
      numeric_properties:
        - property: "cim-equip:ratedCapacity"
          expected_type: "decimal"
          constraints:
            min: 0
            max: 100000  # kW
          on_violation: "LOG_WARNING + USE_DEFAULT"
          default_value: null
        
        - property: "cim-equip:cop"
          expected_type: "decimal"
          constraints:
            min: 1.0
            max: 15.0  # COP合理范围
          on_violation: "LOG_WARNING"
        
        - property: "cim-space:floorArea"
          expected_type: "decimal"
          constraints:
            min: 0.1
            max: 10000  # m²
          on_violation: "LOG_ERROR"
        
        - property: "cim-space:pressureDifferential"
          expected_type: "decimal"
          constraints:
            min: -100  # Pa
            max: 100
          on_violation: "LOG_WARNING"
      
      # 字符串属性验证
      string_properties:
        - property: "rdfs:label"
          constraints:
            max_length: 200
            required: true
            pattern: "^[\\p{L}\\p{N}\\s\\-_]+$"  # 字母、数字、空格、连字符、下划线
          on_violation: "LOG_ERROR + TRUNCATE"
        
        - property: "cim-equip:manufacturer"
          constraints:
            max_length: 100
            required: false
          on_violation: "LOG_WARNING"
        
        - property: "cim-equip:model"
          constraints:
            max_length: 100
          on_violation: "LOG_WARNING"
      
      # 引用属性验证
      reference_properties:
        - property: "cim:locatedIn"
          constraints:
            must_exist_in: "entities_graph"
            allowed_types: ["cim-space:Space"]
          on_violation: "FAIL_MERGE"
        
        - property: "cim-system:componentOf"
          constraints:
            must_exist_in: "entities_graph"
            allowed_types: ["cim-system:System"]
          on_violation: "LOG_ERROR + SKIP_PROPERTY"
      
      # 枚举属性验证
      enum_properties:
        - property: "cim-space:cleanlinessClass"
          allowed_values: ["ISO-1", "ISO-2", "ISO-3", "ISO-4", "ISO-5", "ISO-6", "ISO-7", "ISO-8", "ISO-9"]
          on_violation: "LOG_ERROR + USE_DEFAULT"
          default_value: "ISO-8"
        
        - property: "cim-equip:operationalStatus"
          allowed_values: ["Operational", "Standby", "Maintenance", "Faulty", "Decommissioned"]
          on_violation: "LOG_WARNING + USE_DEFAULT"
          default_value: "Operational"
    
    implementation: |
      def validate_property(entity: Dict, prop_name: str, prop_value: Any, rules: Dict) -> ValidationResult:
          """
          验证单个属性
          """
          rule = rules.get(prop_name)
          if not rule:
              return ValidationResult(valid=True)  # 无规则时跳过
          
          result = ValidationResult(valid=True)
          
          # 类型检查
          if rule.get("expected_type") == "decimal":
              if not isinstance(prop_value, (int, float)):
                  result.add_error(f"{prop_name} should be numeric, got {type(prop_value)}")
          
          # 范围检查
          constraints = rule.get("constraints", {})
          if "min" in constraints and prop_value < constraints["min"]:
              result.add_error(f"{prop_name} value {prop_value} below min {constraints['min']}")
          if "max" in constraints and prop_value > constraints["max"]:
              result.add_error(f"{prop_name} value {prop_value} above max {constraints['max']}")
          
          # 必填检查
          if constraints.get("required") and prop_value is None:
              result.add_error(f"{prop_name} is required but missing")
          
          # 引用存在性检查
          if "must_exist_in" in constraints:
              if not entity_exists(prop_value, constraints["must_exist_in"]):
                  result.add_error(f"{prop_name} references non-existent entity {prop_value}")
          
          # 枚举值检查
          if "allowed_values" in rule:
              if prop_value not in rule["allowed_values"]:
                  result.add_error(f"{prop_name} value '{prop_value}' not in allowed values")
          
          return result
```

---

# **PHASE-B 补强（Claude审计修复）**

## **Module-B.2: 列表合并策略细化**

```yaml
list_merge_strategies:
  meta:
    purpose: "解决Claude指出的'列表合并策略不明确'"
    priority: "🟠 HIGH"
  
  strategies:
    
    # 简单列表合并（去重+排序）
    simple_list_union:
      description: "对简单值列表执行并集操作"
      
      example:
        agent_05: 'serves: [OR-01, OR-02]'
        agent_06: 'serves: [OR-02, OR-03]'
        result: 'serves: [OR-01, OR-02, OR-03]'
      
      algorithm: |
        def merge_simple_lists(list1: List, list2: List) -> List:
            """简单列表并集"""
            merged = list(set(list1) | set(list2))
            return sorted(merged)  # 排序确保确定性
    
    # 引用列表合并（含别名解析）
    reference_list_union:
      description: "对引用列表执行并集，需先解析别名"
      
      example:
        agent_01: 'upstream: [CHWP-1]'
        agent_06: 'upstream: [CHWP-1, ALT-CHWP-2]'
        alias_mapping: 'CHWP-1 == EQP-HVAC-CHWP-001, ALT-CHWP-2 == EQP-HVAC-CHWP-001'
        result: 'upstream: [EQP-HVAC-CHWP-001]'
      
      algorithm: |
        def merge_reference_lists(list1: List, list2: List, alias_registry: Dict) -> List:
            """引用列表并集，含别名解析"""
            # 1. 解析所有别名到标准ID
            normalized1 = [alias_registry.get(ref, ref) for ref in list1]
            normalized2 = [alias_registry.get(ref, ref) for ref in list2]
            
            # 2. 执行并集
            merged = list(set(normalized1) | set(normalized2))
            
            # 3. 返回标准ID列表
            return sorted(merged)
    
    # 有序列表合并（保持拓扑顺序）
    ordered_list_merge:
      description: "对有序列表执行合并，保持因果顺序"
      
      example:
        agent_04_path_1: '[CH-1 → CHWP-1 → AHU-1]'
        agent_04_path_2: '[CH-2 → CHWP-2 → AHU-1]'
        constraint: "顺序表示流动方向，不可随意排序"
      
      algorithm: |
        def merge_ordered_lists(lists: List[List]) -> List:
            """保持拓扑序的有序列表合并"""
            # 1. 构建顺序约束图
            order_graph = build_order_graph(lists)
            
            # 2. 检测循环
            if has_cycle(order_graph):
                raise OrderConflictError("Cycle detected in order constraints")
            
            # 3. 拓扑排序
            return topological_sort(order_graph)
        
        def build_order_graph(lists: List[List]) -> Dict:
            """从多个有序列表构建顺序约束图"""
            graph = defaultdict(set)
            for lst in lists:
                for i in range(len(lst) - 1):
                    graph[lst[i]].add(lst[i + 1])
            return dict(graph)
    
    # 嵌套对象列表合并
    nested_object_list_merge:
      description: "对嵌套对象列表按主键合并"
      
      example:
        agent_03: |
          sensors:
            - id: SNS-001
              type: Temperature
              location: supply
            - id: SNS-002
              type: Humidity
        agent_06: |
          sensors:
            - id: SNS-001
              type: Temperature
              accuracy: 0.1
            - id: SNS-003
              type: Pressure
        result: |
          sensors:
            - id: SNS-001
              type: Temperature
              location: supply
              accuracy: 0.1  # 合并属性
            - id: SNS-002
              type: Humidity
            - id: SNS-003
              type: Pressure
      
      algorithm: |
        def merge_nested_object_lists(list1: List[Dict], list2: List[Dict], key_field: str) -> List[Dict]:
            """按主键合并嵌套对象列表"""
            merged = {}
            
            for item in list1:
                key = item.get(key_field)
                merged[key] = item.copy()
            
            for item in list2:
                key = item.get(key_field)
                if key in merged:
                    # 合并属性
                    merged[key] = merge_entity_properties(merged[key], item)
                else:
                    merged[key] = item.copy()
            
            return list(merged.values())
```

## **Module-B.3: 复杂冲突场景处理**

```yaml
complex_conflict_handling:
  meta:
    purpose: "解决Claude指出的'缺少复杂冲突场景示例'"
    priority: "🟠 HIGH"
  
  scenarios:
    
    # 场景1：嵌套对象冲突
    nested_object_conflict:
      description: "嵌套对象的字段级别冲突"
      
      example:
        agent_02: |
          environmental_requirements:
            temperature:
              setpoint: 22
              tolerance: 2
        agent_06: |
          environmental_requirements:
            temperature:
              setpoint: 22.5
              tolerance: 1.5
      
      resolution: |
        # 按字段级别应用冲突规则
        def resolve_nested_conflict(obj1: Dict, obj2: Dict, rules: Dict) -> Dict:
            merged = {}
            all_keys = set(obj1.keys()) | set(obj2.keys())
            
            for key in all_keys:
                val1 = obj1.get(key)
                val2 = obj2.get(key)
                
                if val1 is None:
                    merged[key] = val2
                elif val2 is None:
                    merged[key] = val1
                elif val1 == val2:
                    merged[key] = val1
                elif isinstance(val1, dict) and isinstance(val2, dict):
                    # 递归合并嵌套对象
                    merged[key] = resolve_nested_conflict(val1, val2, rules)
                else:
                    # 应用冲突解决规则
                    merged[key] = apply_conflict_rule(key, val1, val2, rules)
            
            return merged
        
        # 结果
        result:
          temperature:
            setpoint: 22     # 选择Agent-02（权威高）
            tolerance: 1.5   # 选择Agent-06（更严格）
    
    # 场景2：布尔值冲突
    boolean_conflict:
      description: "布尔值冲突的保守处理"
      
      example:
        agent_01: 'closed_loop: true'
        agent_03: 'closed_loop: false'
      
      resolution: |
        def resolve_boolean_conflict(val1: bool, val2: bool, property_name: str) -> bool:
            """
            布尔值冲突采用保守策略
            """
            # 对安全相关属性，取更严格的值
            safety_properties = ["closed_loop", "emergency_enabled", "redundancy_required"]
            
            if property_name in safety_properties:
                merged_value = True  # 保守：取True（更严格）
            else:
                merged_value = val1  # 否则取高权威来源
            
            # 记录高级别警告
            log_warning(f"Boolean conflict on {property_name}: {val1} vs {val2}, resolved to {merged_value}")
            
            return merged_value
    
    # 场景3：枚举值冲突
    enum_conflict:
      description: "枚举值冲突的严格性选择"
      
      example:
        agent_02: 'cleanlinessClass: ISO-6'
        agent_05: 'cleanlinessClass: ISO-7'
      
      resolution: |
        def resolve_enum_conflict(val1: str, val2: str, enum_type: str) -> str:
            """
            枚举值冲突选择更严格的值
            """
            # 定义枚举的严格性顺序
            strictness_order = {
                "cleanlinessClass": ["ISO-1", "ISO-2", "ISO-3", "ISO-4", "ISO-5", "ISO-6", "ISO-7", "ISO-8", "ISO-9"],
                "criticalityLevel": ["CRITICAL", "HIGH", "MEDIUM", "LOW", "NEGLIGIBLE"]
            }
            
            if enum_type in strictness_order:
                order = strictness_order[enum_type]
                idx1 = order.index(val1) if val1 in order else len(order)
                idx2 = order.index(val2) if val2 in order else len(order)
                
                # 选择索引更小的（更严格）
                merged_value = val1 if idx1 <= idx2 else val2
            else:
                # 无严格性定义时，取高权威来源
                merged_value = val1
            
            log_warning(f"Enum conflict on {enum_type}: {val1} vs {val2}, resolved to {merged_value}")
            return merged_value
        
        # 结果
        result: 'cleanlinessClass: ISO-6'  # ISO-6 比 ISO-7 更严格
```

## **Module-B.4: 未定义属性处理策略**

```yaml
undefined_property_handling:
  meta:
    purpose: "解决Claude指出的'缺少未定义属性处理策略'"
    priority: "🟠 HIGH"
  
  strategies:
    
    strategy_strict:
      name: "STRICT_REJECT"
      description: "严格模式：拒绝本体中未定义的属性"
      behavior: "报错，拒绝合并，等待修正"
      use_case: "FDA认证的医疗系统，0容错"
      
      implementation: |
        def handle_undefined_strict(entity: Dict, ontology: Dict) -> Dict:
            defined_properties = get_all_defined_properties(ontology)
            
            for prop in entity.keys():
                if prop.startswith("@"):
                    continue  # 跳过JSON-LD关键字
                if prop not in defined_properties:
                    raise UndefinedPropertyError(f"Property '{prop}' not in ontology")
            
            return entity
    
    strategy_lenient:
      name: "LENIENT_PRESERVE"
      description: "宽松模式：保留未定义属性，标注为自定义"
      behavior: "保留属性，不参与推理"
      use_case: "生产环境，允许向后兼容扩展"
      recommended: true
      
      implementation: |
        def handle_undefined_lenient(entity: Dict, ontology: Dict) -> Dict:
            defined_properties = get_all_defined_properties(ontology)
            custom_properties = []
            
            for prop, value in list(entity.items()):
                if prop.startswith("@"):
                    continue
                if prop not in defined_properties:
                    # 移动到自定义属性容器
                    custom_properties.append({
                        "cim:propertyName": prop,
                        "cim:propertyValue": value,
                        "cim:schemaStatus": "NOT_IN_ONTOLOGY"
                    })
                    del entity[prop]
            
            if custom_properties:
                entity["cim:customProperties"] = custom_properties
            
            return entity
      
      example: |
        # 输入（含未定义属性）
        {
          "@id": "EQP-HVAC-CH-001",
          "cim-equip:ratedCapacity": 1200,
          "vendor_custom_field_A": "some_value"  # 未定义
        }
        
        # 输出（宽松模式）
        {
          "@id": "EQP-HVAC-CH-001",
          "cim-equip:ratedCapacity": 1200,
          "cim:customProperties": [
            {
              "cim:propertyName": "vendor_custom_field_A",
              "cim:propertyValue": "some_value",
              "cim:schemaStatus": "NOT_IN_ONTOLOGY"
            }
          ]
        }
    
    strategy_inference:
      name: "SCHEMA_INFERENCE"
      description: "推断模式：自动推断属性类型"
      behavior: "根据值推断类型，扩展本体"
      use_case: "智能系统，自适应本体扩展"
      
      implementation: |
        def handle_undefined_inference(entity: Dict, ontology: Dict) -> Tuple[Dict, Dict]:
            """返回处理后的实体和推断的新属性定义"""
            inferred_properties = []
            
            for prop, value in entity.items():
                if prop not in ontology["properties"]:
                    # 推断属性类型
                    inferred_type = infer_property_type(value)
                    inferred_properties.append({
                        "@id": prop,
                        "@type": "owl:DatatypeProperty",
                        "rdfs:range": {"@id": inferred_type},
                        "cim:inferredFrom": entity["@id"],
                        "cim:inferenceConfidence": 0.8
                    })
            
            return entity, inferred_properties
```

---

# **PHASE-C 补强（Claude审计修复）**

## **Module-C.4: 索引性能与一致性机制**

```yaml
index_performance_and_consistency:
  meta:
    purpose: "解决Claude指出的'索引性能和一致性机制缺失'"
    priority: "🟠 HIGH"
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 性能指标定义
  # ═══════════════════════════════════════════════════════════════════════════
  performance_slas:
    query_latency:
      by_type: "< 10ms"
      by_system: "< 50ms"
      by_floor: "< 20ms"
      space_to_equipment: "< 20ms"
      full_traversal: "< 500ms (paginated)"
    
    index_size:
      target: "< 15% of entity data size"
      current_benchmark: "2185 entities, 840KB data, 24KB index (2.8%)"
    
    build_time:
      target: "< 5 min for 10,000 entities"
      incremental_update: "< 10 sec for 100 entity changes"
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 一致性保证机制
  # ═══════════════════════════════════════════════════════════════════════════
  consistency_mechanisms:
    
    version_tagging:
      description: "索引与数据的版本对齐"
      implementation: |
        {
          "@id": "EQP-HVAC-CH-001",
          "cim:dataVersion": "2025-01-17T12:00:00Z#v1"
        }
        
        # 索引元数据
        {
          "index_version": "2025-01-17T12:00:00Z#v1",
          "data_version": "2025-01-17T12:00:00Z#v1",
          "is_stale": false
        }
      
      staleness_check: |
        def check_index_staleness(index_meta: Dict, data_meta: Dict) -> bool:
            if index_meta["data_version"] != data_meta["version"]:
                log_warning("Index is stale, rebuild required")
                return True
            return False
    
    hash_verification:
      description: "基于哈希的一致性验证"
      implementation: |
        def verify_index_consistency(entities: List, index: Dict) -> bool:
            """验证索引与实体数据的一致性"""
            for entity_id, entity_data in entities_by_id.items():
                entity_hash = compute_entity_hash(entity_data)
                indexed_hash = index.get("entity_hashes", {}).get(entity_id)
                
                if entity_hash != indexed_hash:
                    log_error(f"Hash mismatch for {entity_id}")
                    return False
            
            return True
    
    incremental_update:
      description: "增量索引更新机制"
      implementation: |
        class IncrementalIndex:
            def __init__(self, base_index: Dict):
                self.base = base_index
                self.pending_adds = []
                self.pending_removes = []
            
            def add_entity(self, entity: Dict):
                """添加实体到待更新列表"""
                self.pending_adds.append(entity)
            
            def remove_entity(self, entity_id: str):
                """标记实体待删除"""
                self.pending_removes.append(entity_id)
            
            def apply_changes(self) -> Dict:
                """应用增量变更"""
                new_index = copy.deepcopy(self.base)
                
                # 处理删除
                for entity_id in self.pending_removes:
                    remove_from_all_indices(new_index, entity_id)
                
                # 处理添加
                for entity in self.pending_adds:
                    add_to_all_indices(new_index, entity)
                
                # 更新版本
                new_index["meta"]["version"] = generate_new_version()
                
                return new_index
  
  # ═══════════════════════════════════════════════════════════════════════════
  # 优化策略
  # ═══════════════════════════════════════════════════════════════════════════
  optimization_strategies:
    
    sharded_index:
      description: "分片索引，按楼层/系统存储"
      structure: |
        index/
        ├── by_floor/
        │   ├── L1_index.json
        │   ├── L2_index.json
        │   └── L3_index.json
        ├── by_system/
        │   ├── HVAC_index.json
        │   └── ELEC_index.json
        └── global_xref_index.json  # 轻量级全局索引
    
    compressed_storage:
      description: "压缩存储减少I/O"
      options:
        - format: "MessagePack"
          compression_ratio: "60%"
          read_speed: "fast"
        - format: "gzip JSON"
          compression_ratio: "80%"
          read_speed: "medium"
```

## **Module-C.5: 索引查询API定义**

```yaml
index_query_api:
  meta:
    purpose: "解决Claude指出的'缺少索引查询API定义'"
    priority: "🟠 HIGH"
  
  api_specification:
    
    # 按类型查询
    query_by_type:
      method: "GET /index/by_type/{type}"
      parameters:
        - name: "type"
          type: "string"
          description: "实体类型URI或缩写"
        - name: "limit"
          type: "integer"
          default: 100
        - name: "offset"
          type: "integer"
          default: 0
      
      example:
        request: "GET /index/by_type/cim-equip:Chiller?limit=10"
        response: |
          {
            "type": "cim-equip:Chiller",
            "total_count": 4,
            "returned_count": 4,
            "ids": [
              "EQP-HVAC-CH-001",
              "EQP-HVAC-CH-002",
              "EQP-HVAC-CH-003",
              "EQP-HVAC-CH-004"
            ]
          }
    
    # 按系统查询
    query_by_system:
      method: "GET /index/by_system/{system_id}/components"
      parameters:
        - name: "system_id"
          type: "string"
        - name: "component_type"
          type: "string"
          optional: true
      
      example:
        request: "GET /index/by_system/SYS-HVAC-CHW-PLANT/components?component_type=cim-equip:Pump"
        response: |
          {
            "system_id": "SYS-HVAC-CHW-PLANT",
            "component_type": "cim-equip:Pump",
            "components": [
              "EQP-HVAC-CHWP-PRI-001",
              "EQP-HVAC-CHWP-PRI-002",
              "EQP-HVAC-CHWP-SEC-001"
            ]
          }
    
    # 空间到设备查询
    query_space_to_equipment:
      method: "GET /index/cross_ref/space-to-equipment/{space_id}"
      parameters:
        - name: "space_id"
          type: "string"
        - name: "category"
          type: "string"
          optional: true
          description: "设备类别过滤：hvac, electrical, medical_gas, sensors"
      
      example:
        request: "GET /index/cross_ref/space-to-equipment/SPC-L3-OR-001"
        response: |
          {
            "space_id": "SPC-L3-OR-001",
            "equipment": {
              "hvac": ["EQP-HVAC-AHU-001", "EQP-HVAC-FCU-001"],
              "electrical": ["EQP-ELEC-DP-L3-001"],
              "medical_gas": ["EQP-MGAS-O2-001", "EQP-MGAS-VAC-001"],
              "sensors": ["SNS-TEMP-L3OR01-001", "SNS-HUM-L3OR01-001"]
            }
          }
    
    # 反向依赖查询
    query_reverse_dependency:
      method: "GET /index/reverse/{entity_id}"
      parameters:
        - name: "entity_id"
          type: "string"
        - name: "relation"
          type: "string"
          optional: true
      
      example:
        request: "GET /index/reverse/EQP-HVAC-AHU-001?relation=serves"
        response: |
          {
            "entity_id": "EQP-HVAC-AHU-001",
            "reverse_relations": {
              "serves": ["SPC-L3-OR-001", "SPC-L3-OR-002"],
              "componentOf": ["SYS-HVAC-AHU-OR"],
              "meteredBy": ["MTR-ELEC-AHU-001"]
            }
          }
  
  implementation_hint: |
    实现方式选择：
    1. 内存加载：将索引JSON加载到内存，使用字典查找
    2. SQLite：转换为关系数据库，支持复杂查询
    3. GraphDB：加载到RDF三元组库，使用SPARQL查询
```

---

# **PHASE-D 补强（Claude审计修复）**

## **Module-D.2: SHACL形式化约束**

```turtle
# ═══════════════════════════════════════════════════════════════════════════
# 文件: ontology/cim_medical_shapes.ttl
# 描述: CIM医疗建筑SHACL形式化约束
# ═══════════════════════════════════════════════════════════════════════════

@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix cim: <https://cim.medical/ontology/v3.4#> .
@prefix cim-space: <https://cim.medical/ontology/v3.4/space#> .
@prefix cim-equip: <https://cim.medical/ontology/v3.4/equipment#> .
@prefix cim-system: <https://cim.medical/ontology/v3.4/system#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

# ═══════════════════════════════════════════════════════════════════════════
# 手术室约束
# ═══════════════════════════════════════════════════════════════════════════

cim:SurgeryRoomShape
    a sh:NodeShape ;
    sh:targetClass cim-space:SurgeryRoom ;
    sh:name "手术室约束" ;
    
    # 必填属性：洁净等级
    sh:property [
        sh:path cim-space:cleanlinessClass ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:in ( "ISO-5" "ISO-6" "ISO-7" ) ;
        sh:severity sh:Violation ;
        sh:message "手术室必须指定洁净等级(ISO-5/6/7)"
    ] ;
    
    # 必填属性：压差
    sh:property [
        sh:path cim-space:pressureDifferential ;
        sh:minCount 1 ;
        sh:datatype xsd:decimal ;
        sh:minInclusive 10 ;
        sh:maxInclusive 50 ;
        sh:severity sh:Warning ;
        sh:message "手术室压差应在10-50Pa之间"
    ] ;
    
    # 必填属性：换气次数
    sh:property [
        sh:path cim-space:minAirChanges ;
        sh:minCount 1 ;
        sh:datatype xsd:integer ;
        sh:minInclusive 15 ;
        sh:severity sh:Violation ;
        sh:message "手术室最少换气次数不得低于15次/小时"
    ] ;
    
    # 必须由HVAC系统服务
    sh:property [
        sh:path [ sh:inversePath cim-couple:serves ] ;
        sh:minCount 1 ;
        sh:class cim-equip:HVACEquipment ;
        sh:severity sh:Violation ;
        sh:message "手术室必须由至少一个HVAC设备服务"
    ] .

# ═══════════════════════════════════════════════════════════════════════════
# 冷水机组约束
# ═══════════════════════════════════════════════════════════════════════════

cim:ChillerShape
    a sh:NodeShape ;
    sh:targetClass cim-equip:Chiller ;
    sh:name "冷水机组约束" ;
    
    # 必填属性：额定容量
    sh:property [
        sh:path cim-equip:ratedCapacity ;
        sh:minCount 1 ;
        sh:datatype xsd:decimal ;
        sh:minExclusive 0 ;
        sh:severity sh:Violation ;
        sh:message "冷水机组必须指定额定容量且大于0"
    ] ;
    
    # 必填属性：COP
    sh:property [
        sh:path cim-equip:cop ;
        sh:minCount 1 ;
        sh:datatype xsd:decimal ;
        sh:minInclusive 3.0 ;
        sh:maxInclusive 10.0 ;
        sh:severity sh:Warning ;
        sh:message "冷水机组COP应在3.0-10.0之间"
    ] ;
    
    # 必须属于某个系统
    sh:property [
        sh:path cim-system:componentOf ;
        sh:minCount 1 ;
        sh:class cim-system:ChilledWaterSystem ;
        sh:severity sh:Violation ;
        sh:message "冷水机组必须属于一个冷冻水系统"
    ] ;
    
    # 必须有位置
    sh:property [
        sh:path cim:locatedIn ;
        sh:minCount 1 ;
        sh:class cim-space:Space ;
        sh:severity sh:Violation ;
        sh:message "冷水机组必须指定位置"
    ] .

# ═══════════════════════════════════════════════════════════════════════════
# 设备通用约束
# ═══════════════════════════════════════════════════════════════════════════

cim:EquipmentShape
    a sh:NodeShape ;
    sh:targetClass cim-equip:Equipment ;
    sh:name "设备通用约束" ;
    
    # 必填属性：名称
    sh:property [
        sh:path rdfs:label ;
        sh:minCount 1 ;
        sh:severity sh:Warning ;
        sh:message "设备应有名称标签"
    ] ;
    
    # 必填属性：来源Agent
    sh:property [
        sh:path cim:sourceAgent ;
        sh:minCount 1 ;
        sh:severity sh:Info ;
        sh:message "设备应标注来源Agent"
    ] ;
    
    # 必填属性：最后修改时间
    sh:property [
        sh:path cim:lastModified ;
        sh:minCount 1 ;
        sh:datatype xsd:dateTime ;
        sh:severity sh:Info ;
        sh:message "设备应有最后修改时间"
    ] .

# ═══════════════════════════════════════════════════════════════════════════
# 系统完整性约束
# ═══════════════════════════════════════════════════════════════════════════

cim:SystemShape
    a sh:NodeShape ;
    sh:targetClass cim-system:System ;
    sh:name "系统完整性约束" ;
    
    # 系统必须有组件
    sh:property [
        sh:path cim-system:hasComponent ;
        sh:minCount 1 ;
        sh:severity sh:Warning ;
        sh:message "系统应至少有一个组件"
    ] .

# ═══════════════════════════════════════════════════════════════════════════
# 引用完整性约束
# ═══════════════════════════════════════════════════════════════════════════

cim:ReferentialIntegrityShape
    a sh:NodeShape ;
    sh:targetClass cim:Entity ;
    sh:name "引用完整性约束" ;
    
    # locatedIn 引用的空间必须存在
    sh:property [
        sh:path cim:locatedIn ;
        sh:class cim-space:Space ;
        sh:severity sh:Violation ;
        sh:message "locatedIn引用的空间必须存在"
    ] ;
    
    # componentOf 引用的系统必须存在
    sh:property [
        sh:path cim-system:componentOf ;
        sh:class cim-system:System ;
        sh:severity sh:Violation ;
        sh:message "componentOf引用的系统必须存在"
    ] .
```

## **Module-D.3: OWL约束条件**

```yaml
owl_restrictions:
meta:
 purpose: "解决Claude指出的'缺少约束条件定义'"
 priority: "🟡 MEDIUM"

axioms:

 # 约束1：所有设备必须属于某个系统
 equipment_must_be_in_system:
 description: "所有设备必须属于某个系统"
 owl_axiom: |
 {
 "@id": "cim-equip:Equipment",
 "@type": "owl:Class",
 "rdfs:subClassOf": {
 "@type": "owl:Restriction",
 "owl:onProperty": {"@id": "cim-system:componentOf"},
 "owl:someValuesFrom": {"@id": "cim-system:System"}
 }
 }

 # 约束2：医疗空间必须由HVAC系统服务
 medical_space_requires_hvac:
 description: "医疗空间必须由某个HVAC设备服务"
 owl_axiom: |
 {
 "@id": "cim-space:MedicalSpace",
 "@type": "owl:Class",
 "rdfs:subClassOf": {
 "@type": "owl:Restriction",
 "owl:onProperty": {
 "@id": "_:inverseServes",
 "owl:inverseOf": {"@id": "cim-couple:serves"}
 },
 "owl:someValuesFrom": {"@id": "cim-equip:HVACEquipment"}
 }
 }

 # 约束3：冷冻水系统必须有冷水机组
 chw_system_requires_chiller:
 description: "冷冻水系统必须包含至少一个冷水机组"
 owl_axiom: |
 {
 "@id": "cim-system:ChilledWaterSystem",
 "@type": "owl:Class",
 "rdfs:subClassOf": {
 "@type": "owl:Restriction",
 "owl:onProperty": {"@id": "cim-system:hasComponent"},
 "owl:someValuesFrom": {"@id": "cim-equip:Chiller"}
 }
 }

 # 约束4：传感器必须监测某个属性
 sensor_
[^1]: [Agent-03 v2.2  设备本体建模师 (Equipment Ontology Architect) 完整输出.md](http://file/6c1c1929-d310-442c-8bd3-24228af83d28.md)

[^2]: [AGENT-05 V2.1-RELEASE 最终发布文档.md](http://file/1b6473f6-fd9c-4a20-babe-cafb56b0d6e8.md)

[^3]: [Agent-03 v2.2  设备本体建模师 (Equipment Ontology Architect) 完整输出.md](http://file/6c1c1929-d310-442c-8bd3-24228af83d28.md)

[^4]: [Agent-03 v2.2  设备本体建模师 (Equipment Ontology Architect) 完整输出.md](http://file/6c1c1929-d310-442c-8bd3-24228af83d28.md)

[^5]: [Agent-02  空间本体建模师 (Space Ontology Architect).md](http://file/35de1547-3b35-4ab4-a98a-37fb6cf0b0b6.md)

[^6]: [Agent-08  运维管理建模师 (O&M Management Architect).md](http://file/30a23d3c-0fe7-41b0-b314-3ad848cd347d.md)
---