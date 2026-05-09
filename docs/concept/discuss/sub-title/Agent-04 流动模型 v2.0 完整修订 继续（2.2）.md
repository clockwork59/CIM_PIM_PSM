## 🧑‍💻 User


你卡在了【2.2 统一输出格式规范
<YAML>
# ═══════════════════════════════════════════════════════════════════════════════
# 2.2 统一输出格式规范 (Unified Output Format)
# ═══════════════════════════════════════════════════════════════════════════════
Unified_Output_Format:

meta:
 spec】，继续

---
## 🤖 Assistant


继续完成统一输出格式规范及后续内容。

---

## A.2 统一输出格式规范（续）

```yaml
# ═══════════════════════════════════════════════════════════════════════════════
# A.2 统一输出格式规范 (Unified Output Format)
# ═══════════════════════════════════════════════════════════════════════════════

Unified_Output_Format:
  
  meta:
    spec_id: "UOF-001"
    version: "1.0"
    effective_date: "2025-01-XX"
    mandatory: true
    applies_to: "Agent-01至Agent-08及Agent-09 CIM"
    
  # ─────────────────────────────────────────────────────────────────────────────
  # A.2.1 标准Agent输出结构
  # ─────────────────────────────────────────────────────────────────────────────
  
  standard_agent_output_structure:
    
    description: "所有Agent输出文件必须遵循此结构模板"
    
    template:
      
      # ─────────────────────────────────────────
      # 元数据区 (必须)
      # ─────────────────────────────────────────
      meta:
        agent_id: 
          type: "string"
          format: "Agent-NN"
          required: true
          example: "Agent-04"
          
        agent_name:
          type: "string"
          required: true
          example: "流动模型建模师 (Flow Model Architect)"
          
        version:
          type: "string"
          format: "semver (MAJOR.MINOR.PATCH)"
          required: true
          example: "2.0.0"
          
        generated_at:
          type: "string"
          format: "ISO 8601 datetime"
          required: true
          example: "2025-01-15T14:30:00+08:00"
          
        revision_notes:
          type: "string"
          required: false
          example: "修正守恒方程，提升拓扑一致性至97.2%"
          
        status:
          type: "enum"
          values: ["DRAFT", "REVIEW", "APPROVED", "RELEASED"]
          required: true
          
      # ─────────────────────────────────────────
      # 上游依赖区 (必须)
      # ─────────────────────────────────────────
      upstream_dependencies:
        type: "array"
        required: true
        item_structure:
          agent_ref:
            type: "string"
            format: "@Agent-NN"
            example: "@Agent-01"
            
          asset_type:
            type: "string"
            example: "SystemTopology"
            
          asset_ids:
            type: "array"
            example: ["SYS-HVAC-CHP", "SYS-MGAS-O2"]
            
          version_required:
            type: "string"
            example: ">=1.0.0"
            
          usage:
            type: "string"
            example: "获取拓扑结构作为流动路径基础"
            
      # ─────────────────────────────────────────
      # 输出资产区 (必须)
      # ─────────────────────────────────────────
      output_assets:
        type: "array"
        required: true
        item_structure:
          asset_id:
            type: "string"
            example: "Agent04_FlowPaths"
            
          asset_type:
            type: "enum"
            values: ["MODEL", "CATALOG", "MAPPING", "RULES", "EQUATIONS"]
            
          description:
            type: "string"
            example: "各系统流动路径定义"
            
          entity_count:
            type: "integer"
            example: 85
            
          schema_ref:
            type: "string"
            format: "URI"
            example: "#/schemas/FlowPath"
            
      # ─────────────────────────────────────────
      # 下游接口区 (必须)
      # ─────────────────────────────────────────
      downstream_interfaces:
        type: "array"
        required: true
        item_structure:
          target_agent:
            type: "string"
            format: "Agent-NN"
            example: "Agent-06"
            
          interface_type:
            type: "enum"
            values: ["DATA_PROVISION", "EVENT_TRIGGER", "QUERY_SERVICE"]
            
          data_contract:
            type: "object"
            properties:
              entities_provided:
                type: "array"
                example: ["FlowPath", "ConservationEquation"]
                
              required_by_target:
                type: "boolean"
                example: true
                
      # ─────────────────────────────────────────
      # 质量指标区 (必须)
      # ─────────────────────────────────────────
      quality_metrics:
        type: "object"
        required: true
        properties:
          completeness:
            type: "string"
            format: "percentage"
            example: "100%"
            
          consistency_score:
            type: "string"
            format: "percentage"
            example: "97.2%"
            
          validation_status:
            type: "enum"
            values: ["PASSED", "FAILED", "PENDING", "PARTIAL"]
            
          validation_date:
            type: "string"
            format: "ISO 8601 date"
            
          known_issues:
            type: "array"
            item_type: "string"
            
  # ─────────────────────────────────────────────────────────────────────────────
  # A.2.2 文件命名规范
  # ─────────────────────────────────────────────────────────────────────────────
  
  file_naming_convention:
    
    primary_output:
      pattern: "Agent{NN}_{AssetName}_v{VERSION}.yaml"
      components:
        NN: "两位数字Agent编号 (01-09)"
        AssetName: "PascalCase资产名称"
        VERSION: "语义版本号 (MAJOR.MINOR.PATCH 或 MAJOR.MINOR)"
        
      examples:
        - "Agent01_SystemTopology_v1.0.yaml"
        - "Agent04_FlowModels_v2.0.yaml"
        - "Agent05_CouplingUnits_v2.1.yaml"
        - "Agent07_MeteringHierarchy_v1.0.yaml"
        
    supplementary_output:
      pattern: "Agent{NN}_{AssetName}_{Suffix}_v{VERSION}.yaml"
      suffixes:
        - "Validation"   # 验证报告
        - "Mapping"      # 映射表
        - "Schema"       # 数据模式
        - "Examples"     # 示例数据
        
      examples:
        - "Agent04_FlowModels_Validation_v2.0.yaml"
        - "Agent07_Metering_PlatformMapping_v1.0.yaml"
        
    patch_files:
      pattern: "Agent{NN}_Patch_{PatchName}_v{VERSION}.yaml"
      examples:
        - "Agent01_Patch_IDNormalization_v1.0.1.yaml"
        
  # ─────────────────────────────────────────────────────────────────────────────
  # A.2.3 版本控制规范
  # ─────────────────────────────────────────────────────────────────────────────
  
  versioning_convention:
    
    semantic_versioning:
      format: "MAJOR.MINOR.PATCH"
      
      rules:
        MAJOR:
          increment_when: "不兼容的结构变更"
          examples:
            - "删除必需字段"
            - "更改ID格式"
            - "重构核心模型结构"
            
        MINOR:
          increment_when: "向后兼容的功能新增"
          examples:
            - "新增可选字段"
            - "新增实体类型"
            - "扩展枚举值"
            
        PATCH:
          increment_when: "向后兼容的问题修复"
          examples:
            - "修正数据错误"
            - "补充遗漏内容"
            - "格式归一化"
            
    version_history:
      required: true
      structure:
        - version: "string"
          date: "ISO 8601 date"
          author: "string"
          changes: "array of strings"
          
  # ─────────────────────────────────────────────────────────────────────────────
  # A.2.4 数据类型规范
  # ─────────────────────────────────────────────────────────────────────────────
  
  data_type_conventions:
    
    basic_types:
      string:
        yaml_type: "string"
        encoding: "UTF-8"
        
      integer:
        yaml_type: "integer"
        format: "无前导零"
        
      number:
        yaml_type: "number"
        decimal_separator: "."
        precision: "根据工程需要，通常保留2-4位小数"
        
      boolean:
        yaml_type: "boolean"
        values: [true, false]
        note: "不使用 yes/no 或 on/off"
        
    datetime_formats:
      date:
        format: "YYYY-MM-DD"
        example: "2025-01-15"
        
      datetime:
        format: "ISO 8601"
        example: "2025-01-15T14:30:00+08:00"
        
      time:
        format: "HH:MM:SS"
        example: "14:30:00"
        
    physical_quantities:
      format: "value + unit"
      structure:
        value:
          type: "number"
        unit:
          type: "string"
          standard: "SI单位优先，行业惯用单位可接受"
          
      examples:
        temperature:
          value: 22.5
          unit: "°C"
          
        pressure:
          value: 0.45
          unit: "MPa"
          
        flow_rate:
          value: 516
          unit: "m³/h"
          
        power:
          value: 1200
          unit: "kW"
          
        cooling_capacity:
          value: 3400
          unit: "RT"
          note: "冷吨，行业惯用"
          
    percentage:
      format: "string with %"
      example: "97.2%"
      alternate:
        format: "decimal (0-1)"
        example: 0.972
        
    enumeration:
      convention: "UPPER_SNAKE_CASE"
      examples:
        - "RUNNING"
        - "STOPPED"
        - "CLASS_I"
        - "CRITICAL"
        
  # ─────────────────────────────────────────────────────────────────────────────
  # A.2.5 跨域引用格式
  # ─────────────────────────────────────────────────────────────────────────────
  
  cross_reference_format:
    
    external_reference:
      description: "引用其他Agent定义的实体"
      format: "@Agent-{NN}.{ENTITY_ID}"
      
      examples:
        - ref: "@Agent-01.SYS-HVAC-CHP-SRC-001"
          meaning: "引用Agent-01的HVAC冷源系统源节点001"
          
        - ref: "@Agent-03.EQP-HVAC- CHL-19XR-001"
          meaning: "引用Agent-03的冷水机组001"
          
        - ref: "@Agent-05.CU-HVAC-OR-001"
          meaning: "引用Agent-05的HVAC与手术室耦合单元001"
          
    internal_reference:
      description: "引用同一Agent内的其他实体"
      format: "#/{PATH}/{ENTITY_ID}"
      
      examples:
        - ref: "#/flow_paths/FLW-CHW-PATH-001"
          meaning: "引用本文档中的冷冻水流动路径001"
          
        - ref: "#/equations/FLW-CHW-EQ-CONS-001"
          meaning: "引用本文档中的守恒方程001"
          
    schema_reference:
      description: "引用数据模式定义"
      format: "#/schemas/{SCHEMA_NAME}"
      
      examples:
        - ref: "#/schemas/FlowPath"
          meaning: "引用流动路径的数据模式定义"
          
  # ─────────────────────────────────────────────────────────────────────────────
  # A.2.6 注释规范
  # ─────────────────────────────────────────────────────────────────────────────
  
  comment_convention:
    
    section_header:
      format: |
        # ─────────────────────────────────────────────────────────────────
        # {SECTION_NUMBER} {SECTION_TITLE}
        # ─────────────────────────────────────────────────────────────────
        
    inline_comment:
      format: "# {comment}"
      placement: "行尾或单独一行"
      
    documentation_comment:
      format: |
        # @description: {description}
        # @author: {author}
        # @since: {version}
        
    todo_comment:
      format: "# TODO: {task description}"
      
    note_comment:
      format: "# NOTE: {important information}"
```

## A.3 平台数据字典对齐规范

```yaml
# ═══════════════════════════════════════════════════════════════════════════════
# A.3 平台数据字典对齐规范
# 目标平台: 医疗建筑能源管理平台 v2.0/v3.0
# ═══════════════════════════════════════════════════════════════════════════════

Platform_Data_Dictionary_Alignment:
  
  meta:
    spec_id: "PDA-001"
    version: "1.0"
    target_platform: "医疗建筑能源管理平台"
    platform_version: "v2.0/v3.0"
    
  # ─────────────────────────────────────────────────────────────────────────────
  # A.3.1 DIM维度表映射
  # ─────────────────────────────────────────────────────────────────────────────
  
  dim_tables:
    
    dim_space:
      description: "空间维度表"
      source_agent: "Agent-02"
      
      field_mapping:
        - platform_field: "space_id"
          platform_type: "VARCHAR(50)"
          agent_field: "id"
          agent_format: "SPC-*"
          transformation: "直接映射"
          example:
            agent_value: "SPC-L4-SURG-OR1-001"
            platform_value: "SPC-L4-SURG-OR1-001"
            
        - platform_field: "space_name"
          platform_type: "VARCHAR(100)"
          agent_field: "name"
          transformation: "直接映射"
          
        - platform_field: "space_type"
          platform_type: "VARCHAR(50)"
          agent_field: "space_type"
          transformation: "枚举映射"
          enum_mapping:
            OR_CLASS_I: "手术室-I级"
            OR_CLASS_II: "手术室-II级"
            OR_CLASS_III: "手术室-III级"
            OR_HYBRID: "复合手术室"
            ICU_GENERAL: "ICU-综合"
            ICU_NICU: "ICU-新生儿"
            ICU_CCU: "ICU-心脏"
            ICU_PICU: "ICU-儿童"
            ISO_POS: "隔离病房-正压"
            ISO_NEG: "隔离病房-负压"
            WARD_SINGLE: "病房-单人"
            WARD_DOUBLE: "病房-双人"
            WARD_MULTI: "病房-多人"
            
        - platform_field: "space_level"
          platform_type: "VARCHAR(10)"
          agent_field: "level"
          transformation: "直接映射 (L0-L5)"
          
        - platform_field: "parent_space_id"
          platform_type: "VARCHAR(50)"
          agent_field: "parent_ref"
          transformation: "提取ID部分"
          
        - platform_field: "building_id"
          platform_type: "VARCHAR(50)"
          agent_field: "hierarchy_path"
          transformation: "从层级路径提取L1级ID"
          
        - platform_field: "floor"
          platform_type: "VARCHAR(20)"
          agent_field: "hierarchy_path"
          transformation: "从层级路径提取L2级楼层信息"
          
        - platform_field: "area_m2"
          platform_type: "DECIMAL(10,2)"
          agent_field: "area"
          transformation: "直接映射"
          
        - platform_field: "status"
          platform_type: "VARCHAR(20)"
          agent_field: "status"
          default: "ACTIVE"
          
    dim_equipment:
      description: "设备维度表"
      source_agent: "Agent-03"
      
      field_mapping:
        - platform_field: "equipment_id"
          platform_type: "VARCHAR(50)"
          agent_field: "id"
          agent_format: "EQP-*"
          transformation: "直接映射"
          
        - platform_field: "equipment_name"
          platform_type: "VARCHAR(100)"
          agent_field: "name"
          transformation: "直接映射"
          
        - platform_field: "equipment_type"
          platform_type: "VARCHAR(50)"
          agent_field: "type_code"
          transformation: "直接映射"
          
        - platform_field: "equipment_category"
          platform_type: "VARCHAR(50)"
          agent_field: "system_ref"
          transformation: "提取系统类别 (HVAC/ELEC/MGAS等)"
          
        - platform_field: "space_id"
          platform_type: "VARCHAR(50)"
          agent_field: "location_ref"
          transformation: "提取@Agent-02引用的ID"
          
        - platform_field: "rated_power_kw"
          platform_type: "DECIMAL(10,2)"
          agent_field: "rated_power"
          transformation: "单位转换为kW"
          
        - platform_field: "manufacturer"
          platform_type: "VARCHAR(100)"
          agent_field: "manufacturer"
          transformation: "直接映射"
          
        - platform_field: "model"
          platform_type: "VARCHAR(100)"
          agent_field: "model"
          transformation: "直接映射"
          
        - platform_field: "install_date"
          platform_type: "DATE"
          agent_field: "installation_date"
          transformation: "日期格式化 YYYY-MM-DD"
          
        - platform_field: "status"
          platform_type: "VARCHAR(20)"
          agent_field: "status"
          enum_mapping:
            ACTIVE: "运行中"
            MAINTENANCE: "维护中"
            DECOMMISSIONED: "已停用"
            
    dim_meter:
      description: "计量点维度表"
      source_agent: "Agent-07"
      
      field_mapping:
        - platform_field: "meter_id"
          platform_type: "VARCHAR(50)"
          agent_field: "id"
          agent_format: "MTR-*"
          transformation: "直接映射"
          
        - platform_field: "meter_name"
          platform_type: "VARCHAR(100)"
          agent_field: "name"
          transformation: "直接映射"
          
        - platform_field: "energy_type"
          platform_type: "VARCHAR(30)"
          agent_field: "media_type"
          transformation: "枚举映射"
          enum_mapping:
            ELEC: "ELECTRICITY"
            CHW: "COOLING"
            HW: "HEATING"
            WATER: "WATER"
            GAS: "GAS"
            STM: "STEAM"
            O2: "MEDICAL_GAS_O2"
            VAC: "MEDICAL_GAS_VAC"
            CAIR: "MEDICAL_GAS_AIR"
            
        - platform_field: "meter_level"
          platform_type: "VARCHAR(10)"
          agent_field: "level"
          transformation: "直接映射 (L0-L4)"
          
        - platform_field: "meter_type"
          platform_type: "VARCHAR(20)"
          agent_field: "meter_type"
          enum_mapping:
            PHYSICAL: "ACTUAL"
            VIRTUAL: "VIRTUAL"
            
        - platform_field: "equipment_id"
          platform_type: "VARCHAR(50)"
          agent_field: "equipment_ref"
          transformation: "提取@Agent-03引用的ID"
          
        - platform_field: "space_id"
          platform_type: "VARCHAR(50)"
          agent_field: "space_ref"
          transformation: "提取@Agent-02引用的ID"
          
        - platform_field: "accuracy_grade"
          platform_type: "VARCHAR(10)"
          agent_field: "accuracy_class"
          transformation: "直接映射 (A-F)"
          
    dim_control_point:
      description: "控制点维度表"
      source_agent: "Agent-06"
      
      field_mapping:
        - platform_field: "control_point_id"
          platform_type: "VARCHAR(50)"
          agent_field: "id"
          agent_format: "CTL-*"
          transformation: "直接映射"
          
        - platform_field: "point_name"
          platform_type: "VARCHAR(100)"
          agent_field: "name"
          transformation: "直接映射"
          
        - platform_field: "point_type"
          platform_type: "VARCHAR(20)"
          agent_field: "type_code"
          transformation: "枚举映射"
          enum_mapping:
            SNS: "SENSOR"
            ACT: "ACTUATOR"
            
        - platform_field: "io_type"
          platform_type: "VARCHAR(10)"
          agent_field: "io_type"
          transformation: "直接映射 (AI/AO/DI/DO)"
          
        - platform_field: "equipment_id"
          platform_type: "VARCHAR(50)"
          agent_field: "equipment_ref"
          transformation: "提取@Agent-03引用的ID"
          
        - platform_field: "engineering_unit"
          platform_type: "VARCHAR(20)"
          agent_field: "unit"
          transformation: "直接映射"
          
    dim_alarm_rule:
      description: "告警规则维度表"
      source_agent: "Agent-08"
      
      field_mapping:
        - platform_field: "alarm_rule_id"
          platform_type: "VARCHAR(50)"
          agent_field: "id"
          agent_format: "OM-ALM-*"
          transformation: "直接映射"
          
        - platform_field: "rule_name"
          platform_type: "VARCHAR(100)"
          agent_field: "name"
          transformation: "直接映射"
          
        - platform_field: "alarm_level"
          platform_type: "VARCHAR(20)"
          agent_field: "severity"
          transformation: "枚举映射"
          enum_mapping:
            P0: "CRITICAL"
            P1: "HIGH"
            P2: "MEDIUM"
            P3: "LOW"
            
        - platform_field: "condition_expression"
          platform_type: "TEXT"
          agent_field: "condition"
          transformation: "直接映射"
          
        - platform_field: "equipment_types"
          platform_type: "VARCHAR(200)"
          agent_field: "applicable_equipment_types"
          transformation: "数组转逗号分隔字符串"
          
  # ─────────────────────────────────────────────────────────────────────────────
  # A.3.2 DWD明细表映射
  # ─────────────────────────────────────────────────────────────────────────────
  
  dwd_tables:
    
    dwd_energy_meter_reading:
      description: "能耗抄表数据明细表"
      source_agent: "Agent-07 (运行时数据)"
      
      field_mapping:
        - platform_field: "id"
          platform_type: "BIGINT AUTO_INCREMENT"
          agent_field: "auto_generated"
          
        - platform_field: "meter_id"
          platform_type: "VARCHAR(50)"
          agent_field: "meter_id"
          transformation: "直接映射"
          
        - platform_field: "reading_time"
          platform_type: "DATETIME"
          agent_field: "timestamp"
          transformation: "ISO 8601 转 DATETIME"
          
        - platform_field: "total_energy"
          platform_type: "DECIMAL(15,3)"
          agent_field: "value"
          transformation: "直接映射"
          
        - platform_field: "data_quality_score"
          platform_type: "DECIMAL(3,2)"
          agent_field: "confidence_score"
          transformation: "0-1范围"
          
        - platform_field: "data_source"
          platform_type: "VARCHAR(20)"
          agent_field: "source_type"
          transformation: "枚举映射"
          enum_mapping:
            PHYSICAL_METER: "ACTUAL"
            VIRTUAL_CALCULATED: "VIRTUAL"
            INTERPOLATED: "ESTIMATED"
            MANUAL_INPUT: "MANUAL"
            
    dwd_equipment_status:
      description: "设备状态明细表"
      source_agent: "Agent-06 (运行时数据)"
      
      field_mapping:
        - platform_field: "id"
          platform_type: "BIGINT AUTO_INCREMENT"
          agent_field: "auto_generated"
          
        - platform_field: "equipment_id"
          platform_type: "VARCHAR(50)"
          agent_field: "equipment_ref"
          transformation: "提取@Agent-03引用的ID"
          
        - platform_field: "status_time"
          platform_type: "DATETIME"
          agent_field: "timestamp"
          
        - platform_field: "run_status"
          platform_type: "VARCHAR(20)"
          agent_field: "DI_RUN.value"
          transformation: "枚举映射"
          enum_mapping:
            1: "RUNNING"
            0: "STOPPED"
            
        - platform_field: "alarm_status"
          platform_type: "TINYINT"
          agent_field: "DI_ALARM.value"
          transformation: "0=正常, 1=告警"
          
        - platform_field: "mode"
          platform_type: "VARCHAR(30)"
          agent_field: "state_machine.current_state"
          
    dwd_environment_measure:
      description: "环境测量明细表"
      source_agent: "Agent-02 + Agent-06 (运行时数据)"
      
      field_mapping:
        - platform_field: "id"
          platform_type: "BIGINT AUTO_INCREMENT"
          agent_field: "auto_generated"
          
        - platform_field: "space_id"
          platform_type: "VARCHAR(50)"
          agent_field: "space_ref"
          transformation: "提取@Agent-02引用的ID"
          
        - platform_field: "measure_time"
          platform_type: "DATETIME"
          agent_field: "timestamp"
          
        - platform_field: "temperature"
          platform_type: "DECIMAL(5,2)"
          agent_field: "CTL-SNS-TEMP.value"
          unit: "°C"
          
        - platform_field: "humidity"
          platform_type: "DECIMAL(5,2)"
          agent_field: "CTL-SNS-HUMID.value"
          unit: "%RH"
          
        - platform_field: "pressure_diff"
          platform_type: "DECIMAL(6,2)"
          agent_field: "CTL-SNS-PRESS.value"
          unit: "Pa"
          
        - platform_field: "co2_concentration"
          platform_type: "DECIMAL(6,1)"
          agent_field: "CTL-SNS-CO2.value"
          unit: "ppm"
          
        - platform_field: "particle_count"
          platform_type: "INT"
          agent_field: "CTL-SNS-PARTICLE.value"
          unit: "个/m³"
          
    dwd_alarm_event:
      description: "告警事件明细表"
      source_agent: "Agent-08 (运行时数据)"
      
      field_mapping:
        - platform_field: "alarm_id"
          platform_type: "VARCHAR(50)"
          agent_field: "auto_generated UUID"
          
        - platform_field: "alarm_time"
          platform_type: "DATETIME"
          agent_field: "trigger_time"
          
        - platform_field: "alarm_rule_id"
          platform_type: "VARCHAR(50)"
          agent_field: "rule_ref"
          transformation: "提取OM-ALM-* ID"
          
        - platform_field: "equipment_id"
          platform_type: "VARCHAR(50)"
          agent_field: "source_equipment"
          
        - platform_field: "alarm_level"
          platform_type: "VARCHAR(20)"
          agent_field: "severity"
          transformation: "枚举映射 (P0→CRITICAL等)"
          
        - platform_field: "alarm_value"
          platform_type: "VARCHAR(100)"
          agent_field: "trigger_value"
          
        - platform_field: "alarm_desc"
          platform_type: "TEXT"
          agent_field: "description"
          
        - platform_field: "status"
          platform_type: "VARCHAR(20)"
          agent_field: "current_status"
          enum_mapping:
            ACTIVE: "active"
            ACKNOWLEDGED: "acknowledged"
            CLEARED: "cleared"
            
        - platform_field: "ack_time"
          platform_type: "DATETIME"
          agent_field: "acknowledged_time"
          
        - platform_field: "clear_time"
          platform_type: "DATETIME"
          agent_field: "cleared_time"
          
    dwd_work_order:
      description: "工单明细表"
      source_agent: "Agent-08 (运行时数据)"
      
      field_mapping:
        - platform_field: "wo_id"
          platform_type: "VARCHAR(50)"
          agent_field: "work_order_id"
          
        - platform_field: "wo_type"
          platform_type: "VARCHAR(30)"
          agent_field: "order_type"
          enum_mapping:
            CORRECTIVE: "故障报修"
            PREVENTIVE: "计划维护"
            INSPECTION: "巡检工单"
            MODIFICATION: "改造工单"
            
        - platform_field: "equipment_id"
          platform_type: "VARCHAR(50)"
          agent_field: "equipment_ref"
          
        - platform_field: "priority"
          platform_type: "VARCHAR(10)"
          agent_field: "priority"
          enum_mapping:
            P0: "紧急"
            P1: "高"
            P2: "中"
            P3: "低"
            
        - platform_field: "create_time"
          platform_type: "DATETIME"
          agent_field: "created_at"
          
        - platform_field: "due_time"
          platform_type: "DATETIME"
          agent_field: "due_at"
          
        - platform_field: "complete_time"
          platform_type: "DATETIME"
          agent_field: "completed_at"
          
        - platform_field: "status"
          platform_type: "VARCHAR(20)"
          agent_field: "status"
          enum_mapping:
            OPEN: "待处理"
            IN_PROGRESS: "处理中"
            COMPLETED: "已完成"
            CANCELLED: "已取消"
            
    dwd_business_activity:
      description: "业务活动明细表"
      source_agent: "需外部系统(HIS)提供"
      
      gap_analysis:
        issue: "Agent-02未定义业务活动模型"
        impact: "无法直接从Agent输出填充此表"
        resolution: "CIM阶段补充业务活动本体，或从HIS系统集成"
        
      proposed_structure:
        - field: "activity_id"
          source: "HIS系统"
          
        - field: "activity_type"
          enum: ["手术", "检查", "治疗", "门诊", "住院"]
          
        - field: "space_id"
          source: "@Agent-02.SPC-*"
          
        - field: "start_time"
          source: "HIS系统"
          
        - field: "end_time"
          source: "HIS系统"
          
        - field: "patient_count"
          source: "HIS系统"
          
        - field: "staff_count"
          source: "HIS系统"
          
      status: "⚠️ 需CIM阶段或平台集成阶段补充"
      
  # ─────────────────────────────────────────────────────────────────────────────
  # A.3.3 数据转换规则
  # ─────────────────────────────────────────────────────────────────────────────
  
  transformation_rules:
    
    id_extraction:
      description: "从跨域引用中提取ID"
      input_format: "@Agent-NN.{ID}"
      output_format: "{ID}"
      example:
        input: "@Agent-03.EQP-HVAC- CHL-19XR-001"
        output: "EQP-HVAC- CHL-19XR-001"
        
    enum_mapping:
      description: "枚举值转换"
      method: "查找映射表"
      fallback: "保留原值或设为NULL"
      
    datetime_conversion:
      description: "时间格式转换"
      input_format: "ISO 8601 (2025-01-15T14:30:00+08:00)"
      output_format: "MySQL DATETIME (2025-01-15 14:30:00)"
      
    array_to_string:
      description: "数组转字符串"
      method: "逗号分隔"
      example:
        input: ["TYPE_A", "TYPE_B", "TYPE_C"]
        output: "TYPE_A,TYPE_B,TYPE_C"
        
    null_handling:
      description: "空值处理"
      rules:
        optional_field_missing: "NULL"
        empty_string: "保留空字符串"
        explicit_null: "NULL"
```

---

## A.4 跨Agent依赖关系矩阵

```yaml
# ═══════════════════════════════════════════════════════════════════════════════
# A.4 跨Agent依赖关系矩阵
# ═══════════════════════════════════════════════════════════════════════════════

Cross_Agent_Dependency_Matrix:
  
  meta:
    version: "1.0"
    description: "定义Agent间的数据依赖和接口关系"
    
  # ─────────────────────────────────────────────────────────────────────────────
  # A.4.1 依赖关系矩阵
  # ─────────────────────────────────────────────────────────────────────────────
  
  dependency_matrix:
    description: |
      行 = 消费者Agent (Consumer)
      列 = 提供者Agent (Provider)
      ✓ = 存在依赖关系
      x = 无依赖关系
      - = 自身
      
    matrix:
      #           Provider →
      #           A01  A02  A03  A04  A05  A06  A07  A08
      Agent_01:  ["-", "x", "x", "x", "x", "x", "x", "x"]
      Agent_02:  ["x", "-", "x", "x", "x", "x", "x", "x"]
      Agent_03:  ["✓", "✓", "-", "x", "x", "x", "x", "x"]
      Agent_04:  ["✓", "x", "✓", "-", "x", "x", "x", "x"]
      Agent_05:  ["✓", "✓", "✓", "✓", "-", "x", "x", "x"]
      Agent_06:  ["✓", "✓", "✓", "✓", "✓", "-", "x", "x"]
      Agent_07:  ["✓", "✓", "✓", "✓", "✓", "✓", "-", "x"]
      Agent_08:  ["x", "✓", "✓", "x", "✓", "✓", "✓", "-"]
      
  # ─────────────────────────────────────────────────────────────────────────────
  # A.4.2 详细依赖说明
  # ─────────────────────────────────────────────────────────────────────────────
  
  dependency_details:
    
    Agent_03_dependencies:
      - provider: "@Agent-01"
        assets: ["SYS-* (系统拓扑节点)"]
        usage: "确定设备所属系统和拓扑位置"
        
      - provider: "@Agent-02"
        assets: ["SPC-* (空间定义)"]
        usage: "确定设备安装位置"
        
    Agent_04_dependencies:
      - provider: "@Agent-01"
        assets: ["SYS-* (系统拓扑)"]
        usage: "流动路径必须与拓扑结构对齐"
        
      - provider: "@Agent-03"
        assets: ["EQP-* (设备参数)"]
        usage: "获取设备容量、效率等参数用于方程计算"
        
    Agent_05_dependencies:
      - provider: "@Agent-01"
        assets: ["SYS-* (系统拓扑)"]
        usage: "确定耦合单元涉及的系统"
        
      - provider: "@Agent-02"
        assets: ["SPC-* (空间定义)"]
        usage: "确定耦合单元对应的空间"
        
      - provider: "@Agent-03"
        assets: ["EQP-* (设备)"]
        usage: "绑定服务于空间的设备"
        
      - provider: "@Agent-04"
        assets: ["FLW-* (流动模型)"]
        usage: "定义三流动（物质流/能量流/信息流）"
        
    Agent_06_dependencies:
      - provider: "@Agent-01"
        assets: ["SYS-* (系统拓扑)"]
        usage: "控制网络架构"
        
      - provider: "@Agent-02"
        assets: ["SPC-* (空间, 环境参数)"]
        usage: "控制设定值来源"
        
      - provider: "@Agent-03"
        assets: ["EQP-* (设备I/O点)"]
        usage: "传感器/执行器绑定"
        
      - provider: "@Agent-04"
        assets: ["FLW-EQ-* (物理方程)"]
        usage: "前馈控制算法"
        
      - provider: "@Agent-05"
        assets: ["CU-* (耦合单元)"]
        usage: "闭环控制策略上下文"
        
    Agent_07_dependencies:
      - provider: "@Agent-01"
        assets: ["SYS-* (系统拓扑)"]
        usage: "计量边界定义"
        
      - provider: "@Agent-02"
        assets: ["SPC-* (空间)"]
        usage: "区域/科室计量分配"
        
      - provider: "@Agent-03"
        assets: ["EQP-* (设备)"]
        usage: "设备级计量绑定"
        
      - provider: "@Agent-04"
        assets: ["FLW-* (流动路径)"]
        usage: "确定计量点位置合理性"
        
      - provider: "@Agent-05"
        assets: ["CU-* (耦合单元)"]
        usage: "分摊边界定义"
        
      - provider: "@Agent-06"
        assets: ["CTL-SNS-* (传感器)"]
        usage: "虚拟计量点数据来源"
        
    Agent_08_dependencies:
      - provider: "@Agent-02"
        assets: ["SPC-* (空间)"]
        usage: "告警推送范围"
        
      - provider: "@Agent-03"
        assets: ["EQP-* (设备)"]
        usage: "告警规则适用设备"
        
      - provider: "@Agent-05"
        assets: ["CU-* (耦合单元)"]
        usage: "级联影响分析"
        
      - provider: "@Agent-06"
        assets: ["CTL-* (控制点)"]
        usage: "告警触发数据源"
        
      - provider: "@Agent-07"
        assets: ["MTR-* (计量点)"]
        usage: "能效告警数据源"
        
  # ─────────────────────────────────────────────────────────────────────────────
  # A.4.3 接口规范
  # ─────────────────────────────────────────────────────────────────────────────
  
  interface_specifications:
    
    Agent_05_to_Agent_06:
      interface_id: "IF-05-06-001"
      type: "DATA_PROVISION"
      
      provided_entities:
        - entity: "CouplingUnit"
          attributes:
            - "cu_id"
            - "system_refs"
            - "space_ref"
            - "device_bindings"
            - "control_requirements"
            
        - entity: "ControlRequirement"
          attributes:
            - "controlled_parameter"
            - "setpoint_source"
            - "control_mode"
            - "priority"
            
    Agent_05_to_Agent_07:
      interface_id: "IF-05-07-001"
      type: "DATA_PROVISION"
      
      provided_entities:
        - entity: "CouplingUnit"
          attributes:
            - "cu_id"
            - "energy_flow_definition"
            - "metering_boundary"
            - "allocation_basis"
            
    Agent_06_to_Agent_08:
      interface_id: "IF-06-08-001"
      type: "EVENT_TRIGGER"
      
      event_types:
        - event: "EQUIPMENT_ALARM"
          payload:
            equipment_id: "string"
            alarm_type: "string"
            value: "number"
            timestamp: "datetime"
            
        - event: "STATUS_CHANGE"
          payload:
            equipment_id: "string"
            old_status: "string"
            new_status: "string"
            timestamp: "datetime"
            
    Agent_07_to_Agent_08:
      interface_id: "IF-07-08-001"
      type: "EVENT_TRIGGER"
      
      event_types:
        - event: "EFFICIENCY_ALERT"
          payload:
            equipment_id: "string"
            metric: "string"
            current_value: "number"
            threshold: "number"
            recommended_action: "string"
            
        - event: "ANOMALY_DETECTED"
          payload:
            meter_id: "string"
            anomaly_type: "string"
            deviation: "number"
            confidence: "number"
```

---

现在继续 **Part B: Agent-04 流动模型 v2.0 完整修订** 的剩余内容，以及后续Part。是否需要我继续输出？

---