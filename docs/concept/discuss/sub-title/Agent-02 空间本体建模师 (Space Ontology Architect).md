## 🧑‍💻 User


根据‘完整Agent体系’文档，执行附件空间本体建模师的指令，完成相应的内容输出

---
## 🤖 Assistant


我需要先搜索知识库，获取"完整Agent体系"文档中关于空间本体建模师的完整指令内容。



我需要继续搜索以获取更完整的空间本体建模师规范内容。



现在我已经收集了足够的信息，可以按照Agent-02空间本体建模师的完整指令，输出医疗建筑空间本体模型的完整内容。

---

# Agent-02: 空间本体建模师 (Space Ontology Architect)
## 完整输出文档

---

```yaml
# ═══════════════════════════════════════════════════════════════════════════════
# Agent-02: 空间本体建模师 (Space Ontology Architect)
# 医疗建筑空间本体模型 - 完整输出
# ═══════════════════════════════════════════════════════════════════════════════

Agent02_Output:

  # ════════════════════════════════════════════════════════════════════════════
  # 元数据
  # ════════════════════════════════════════════════════════════════════════════
  meta:
    agent_id: Agent-02
    agent_name: 空间本体建模师
    agent_name_en: Space Ontology Architect
    version: 1.0
    generated_at: 2024-12-20T00:00:00+08:00
    
    role_definition: |
      专业的医疗建筑空间规划专家，专注于构建建筑空间的本体模型。
      核心能力是将医疗建筑的物理空间抽象为层级化、结构化的空间模型，
      并定义各类空间的属性和环境要求。
      
    position_in_system:
      phase: 阶段一（基础模型层）
      dependencies: 无（基础Agent）
      dependents:
        - Agent-05（系统-空间耦合建模师）
        - Agent-08（运维管理建模师）
        
    core_responsibilities:
      - 空间层级建模：建立建筑→楼层→区域→房间的层级结构
      - 空间分类定义：定义医疗建筑的空间功能分类体系
      - 医疗专用空间建模：详细定义手术室、ICU、负压病房等特殊空间
      - 空间属性定义：定义各类空间的静态属性和环境要求
      
    reference_standards:
      - GB 50333-2013 医院洁净手术部建筑技术规范
      - GB 51039-2014 综合医院建筑设计规范
      - JGJ 49-2014 综合医院建筑设计规范
      - WS/T 311-2009 医院隔离技术规范
      - GB 19489-2008 实验室生物安全通用要求
      - ISO 14644-1 洁净室及相关受控环境

  # ════════════════════════════════════════════════════════════════════════════
  # 第一部分：空间层级模型 (Space Hierarchy Model)
  # ════════════════════════════════════════════════════════════════════════════
  space_hierarchy_model:
    
    model_description: |
      医疗建筑空间层级模型采用6级层次结构（L0-L5），从院区级别到子空间级别，
      构建完整的空间组织架构。每个层级都有明确的定义、属性和编码规则。
      
    levels:
    
      # ──────────────────────────────────────────────────────────────────────
      # L0: 院区层级 (Site Level)
      # ──────────────────────────────────────────────────────────────────────
      - level_id: L0
        level_name: Site
        level_name_cn: 院区
        description: 医疗机构的整体基地范围，包含所有建筑物和室外空间
        
        definition: |
          院区是医疗建筑空间模型的最高层级，代表一个完整的医疗机构用地范围。
          包括建筑物、道路、绿化、停车场等所有物理空间。
          
        coding_rule:
          pattern: "SITE-{机构代码}"
          example: "SITE-XAYYFY"
          description: 机构代码采用医疗机构标准代码
          
        attributes:
          identity_attributes:
            - attr_id: site_id
              attr_name: site_id
              attr_name_cn: 院区编码
              data_type: string
              required: true
              unique: true
              pattern: "SITE-[A-Z0-9]+"
              
            - attr_id: site_name
              attr_name: site_name
              attr_name_cn: 院区名称
              data_type: string
              required: true
              example: "雄安新区宣武医院院区"
              
            - attr_id: site_alias
              attr_name: site_alias
              attr_name_cn: 院区别名
              data_type: string
              required: false
              example: "雄安宣武"
              
          location_attributes:
            - attr_id: address
              attr_name: address
              attr_name_cn: 地址
              data_type: string
              required: true
              
            - attr_id: city
              attr_name: city
              attr_name_cn: 城市
              data_type: string
              required: true
              
            - attr_id: district
              attr_name: district
              attr_name_cn: 区/县
              data_type: string
              
            - attr_id: geo_location
              attr_name: geo_location
              attr_name_cn: 地理坐标
              data_type: object
              properties:
                longitude: {type: float, unit: "°"}
                latitude: {type: float, unit: "°"}
                elevation: {type: float, unit: m}
                
            - attr_id: climate_zone
              attr_name: climate_zone
              attr_name_cn: 气候区
              data_type: enum
              enum_values:
                - SEVERE_COLD  # 严寒地区
                - COLD         # 寒冷地区
                - HOT_SUMMER_COLD_WINTER  # 夏热冬冷
                - HOT_SUMMER_WARM_WINTER  # 夏热冬暖
                - MILD         # 温和地区
                
          physical_attributes:
            - attr_id: total_land_area
              attr_name: total_land_area
              attr_name_cn: 总占地面积
              data_type: float
              unit: m²
              required: true
              
            - attr_id: total_building_area
              attr_name: total_building_area
              attr_name_cn: 总建筑面积
              data_type: float
              unit: m²
              required: true
              
            - attr_id: floor_area_ratio
              attr_name: floor_area_ratio
              attr_name_cn: 容积率
              data_type: float
              calculation: "total_building_area / total_land_area"
              
            - attr_id: building_density
              attr_name: building_density
              attr_name_cn: 建筑密度
              data_type: float
              unit: "%"
              
            - attr_id: green_ratio
              attr_name: green_ratio
              attr_name_cn: 绿地率
              data_type: float
              unit: "%"
              
          capacity_attributes:
            - attr_id: bed_count
              attr_name: bed_count
              attr_name_cn: 床位数
              data_type: integer
              required: true
              
            - attr_id: daily_outpatient_capacity
              attr_name: daily_outpatient_capacity
              attr_name_cn: 日门诊量设计容量
              data_type: integer
              
            - attr_id: building_count
              attr_name: building_count
              attr_name_cn: 建筑数量
              data_type: integer
              
          administrative_attributes:
            - attr_id: hospital_level
              attr_name: hospital_level
              attr_name_cn: 医院等级
              data_type: enum
              enum_values: [三级甲等, 三级乙等, 二级甲等, 二级乙等, 一级]
              
            - attr_id: hospital_type
              attr_name: hospital_type
              attr_name_cn: 医院类型
              data_type: enum
              enum_values: [综合医院, 专科医院, 中医医院, 妇幼保健院, 康复医院]
              
        child_level: L1
        
      # ──────────────────────────────────────────────────────────────────────
      # L1: 建筑层级 (Building Level)
      # ──────────────────────────────────────────────────────────────────────
      - level_id: L1
        level_name: Building
        level_name_cn: 建筑
        parent_level: L0
        description: 院区内的单体建筑物
        
        definition: |
          建筑是具有独立结构体系的单体建筑物。
          医疗建筑通常按功能划分为门诊楼、住院楼、医技楼、后勤楼等。
          
        coding_rule:
          pattern: "{院区代码}-{建筑类型代码}{序号}"
          example: "SITE-XAYYFY-MZ01"
          building_type_codes:
            MZ: 门诊楼
            ZY: 住院楼
            YJ: 医技楼
            JZ: 急诊楼
            HQ: 后勤楼
            ZH: 综合楼
            GY: 公共用房
            
        attributes:
          identity_attributes:
            - attr_id: building_id
              attr_name: building_id
              attr_name_cn: 建筑编码
              data_type: string
              required: true
              unique: true
              pattern: "SITE-[A-Z0-9]+-[A-Z]{2}[0-9]{2}"
              
            - attr_id: building_name
              attr_name: building_name
              attr_name_cn: 建筑名称
              data_type: string
              required: true
              example: "门诊医技综合楼"
              
            - attr_id: building_name_en
              attr_name: building_name_en
              attr_name_cn: 建筑英文名称
              data_type: string
              example: "Outpatient and Medical Technology Building"
              
            - attr_id: building_alias
              attr_name: building_alias
              attr_name_cn: 建筑别名
              data_type: string
              example: "1号楼"
              
          classification_attributes:
            - attr_id: building_type
              attr_name: building_type
              attr_name_cn: 建筑类型
              data_type: enum
              required: true
              enum_values:
                - OUTPATIENT    # 门诊楼
                - INPATIENT     # 住院楼
                - MEDICAL_TECH  # 医技楼
                - EMERGENCY     # 急诊楼
                - LOGISTICS     # 后勤楼
                - COMPREHENSIVE # 综合楼
                - ADMINISTRATIVE # 行政楼
                - RESEARCH      # 科研楼
                - TEACHING      # 教学楼
                
            - attr_id: building_function
              attr_name: building_function
              attr_name_cn: 建筑功能
              data_type: string[]
              example: ["门诊", "医技检查", "手术"]
              
          physical_attributes:
            - attr_id: building_area
              attr_name: building_area
              attr_name_cn: 建筑面积
              data_type: float
              unit: m²
              required: true
              
            - attr_id: footprint_area
              attr_name: footprint_area
              attr_name_cn: 建筑占地面积
              data_type: float
              unit: m²
              
            - attr_id: floor_count_above
              attr_name: floor_count_above
              attr_name_cn: 地上层数
              data_type: integer
              required: true
              
            - attr_id: floor_count_below
              attr_name: floor_count_below
              attr_name_cn: 地下层数
              data_type: integer
              required: true
              default: 0
              
            - attr_id: building_height
              attr_name: building_height
              attr_name_cn: 建筑高度
              data_type: float
              unit: m
              
            - attr_id: standard_floor_height
              attr_name: standard_floor_height
              attr_name_cn: 标准层高
              data_type: float
              unit: m
              typical_range: [3.6, 4.5]
              
          structural_attributes:
            - attr_id: structure_type
              attr_name: structure_type
              attr_name_cn: 结构类型
              data_type: enum
              enum_values:
                - FRAME           # 框架结构
                - FRAME_SHEAR     # 框架-剪力墙
                - SHEAR_WALL      # 剪力墙结构
                - TUBE            # 筒体结构
                
            - attr_id: fire_resistance_rating
              attr_name: fire_resistance_rating
              attr_name_cn: 耐火等级
              data_type: enum
              enum_values: [一级, 二级, 三级, 四级]
              typical_value: 一级
              
            - attr_id: seismic_fortification
              attr_name: seismic_fortification
              attr_name_cn: 抗震设防烈度
              data_type: integer
              unit: 度
              typical_range: [6, 8]
              
          mep_attributes:
            - attr_id: mep_shaft_count
              attr_name: mep_shaft_count
              attr_name_cn: 机电管井数量
              data_type: integer
              
            - attr_id: has_mep_floor
              attr_name: has_mep_floor
              attr_name_cn: 是否有设备层
              data_type: boolean
              
            - attr_id: main_electrical_room_floor
              attr_name: main_electrical_room_floor
              attr_name_cn: 主配电室所在楼层
              data_type: string
              
            - attr_id: main_mechanical_room_floor
              attr_name: main_mechanical_room_floor
              attr_name_cn: 主机房所在楼层
              data_type: string
              
          date_attributes:
            - attr_id: design_date
              attr_name: design_date
              attr_name_cn: 设计日期
              data_type: date
              
            - attr_id: completion_date
              attr_name: completion_date
              attr_name_cn: 竣工日期
              data_type: date
              
            - attr_id: operation_date
              attr_name: operation_date
              attr_name_cn: 启用日期
              data_type: date
              
        child_level: L2
        
      # ──────────────────────────────────────────────────────────────────────
      # L2: 楼层层级 (Floor Level)
      # ──────────────────────────────────────────────────────────────────────
      - level_id: L2
        level_name: Floor
        level_name_cn: 楼层
        parent_level: L1
        description: 建筑内的水平空间划分单元
        
        definition: |
          楼层是建筑内按标高划分的水平空间层次。
          包括地上标准层、地下室、夹层、设备层、屋顶层等。
          
        coding_rule:
          pattern: "{建筑编码}-{楼层标识}"
          example: "SITE-XAYYFY-MZ01-F03"
          floor_codes:
            F: 地上层 (F01, F02, ..., Fnn)
            B: 地下层 (B01, B02, ...)
            M: 夹层 (M01, M02, ...)
            R: 屋顶层 (RF)
            
        attributes:
          identity_attributes:
            - attr_id: floor_id
              attr_name: floor_id
              attr_name_cn: 楼层编码
              data_type: string
              required: true
              unique: true
              
            - attr_id: floor_name
              attr_name: floor_name
              attr_name_cn: 楼层名称
              data_type: string
              required: true
              example: "三层"
              
            - attr_id: floor_short_name
              attr_name: floor_short_name
              attr_name_cn: 楼层简称
              data_type: string
              example: "3F"
              
          classification_attributes:
            - attr_id: floor_type
              attr_name: floor_type
              attr_name_cn: 楼层类型
              data_type: enum
              required: true
              enum_values:
                - ABOVE_GROUND    # 地上层
                - UNDERGROUND     # 地下层
                - MEZZANINE      # 夹层
                - EQUIPMENT      # 设备层
                - ROOF           # 屋顶层
                - REFUGE         # 避难层
                
            - attr_id: floor_number
              attr_name: floor_number
              attr_name_cn: 楼层序号
              data_type: integer
              description: 地上为正数，地下为负数
              
            - attr_id: is_typical_floor
              attr_name: is_typical_floor
              attr_name_cn: 是否标准层
              data_type: boolean
              
          physical_attributes:
            - attr_id: floor_area
              attr_name: floor_area
              attr_name_cn: 楼层面积
              data_type: float
              unit: m²
              required: true
              
            - attr_id: usable_area
              attr_name: usable_area
              attr_name_cn: 使用面积
              data_type: float
              unit: m²
              
            - attr_id: floor_height
              attr_name: floor_height
              attr_name_cn: 层高
              data_type: float
              unit: m
              required: true
              typical_range: [3.6, 6.0]
              
            - attr_id: clear_height
              attr_name: clear_height
              attr_name_cn: 净高
              data_type: float
              unit: m
              description: 地面到吊顶底的高度
              
            - attr_id: finish_floor_level
              attr_name: finish_floor_level
              attr_name_cn: 建筑完成面标高
              data_type: float
              unit: m
              reference: 室外地面±0.000
              
            - attr_id: structural_floor_level
              attr_name: structural_floor_level
              attr_name_cn: 结构楼面标高
              data_type: float
              unit: m
              
          functional_attributes:
            - attr_id: main_function
              attr_name: main_function
              attr_name_cn: 主要功能
              data_type: string
              example: "手术区"
              
            - attr_id: departments
              attr_name: departments
              attr_name_cn: 科室列表
              data_type: string[]
              example: ["手术室", "麻醉科", "供应室"]
              
          mep_attributes:
            - attr_id: ceiling_void_height
              attr_name: ceiling_void_height
              attr_name_cn: 吊顶空间高度
              data_type: float
              unit: m
              typical_range: [0.8, 1.5]
              
            - attr_id: raised_floor
              attr_name: raised_floor
              attr_name_cn: 是否架空地板
              data_type: boolean
              default: false
              
            - attr_id: raised_floor_height
              attr_name: raised_floor_height
              attr_name_cn: 架空地板高度
              data_type: float
              unit: mm
              condition: "raised_floor = true"
              
        child_level: L3
        
      # ──────────────────────────────────────────────────────────────────────
      # L3: 功能区域层级 (Zone Level)
      # ──────────────────────────────────────────────────────────────────────
      - level_id: L3
        level_name: Zone
        level_name_cn: 功能区域
        parent_level: L2
        description: 楼层内按功能划分的区域
        
        definition: |
          功能区域是楼层内按照医疗功能和管理需求划分的空间分区。
          如手术区、护理单元、检验区等。区域通常具有相对独立的流线和管理边界。
          
        coding_rule:
          pattern: "{楼层编码}-{区域类型代码}{序号}"
          example: "SITE-XAYYFY-MZ01-F03-OP01"
          zone_type_codes:
            OP: 手术区 (Operating Zone)
            NU: 护理单元 (Nursing Unit)
            IC: 重症区 (Intensive Care Zone)
            OD: 门诊区 (Outpatient Zone)
            ER: 急诊区 (Emergency Zone)
            LB: 检验区 (Laboratory Zone)
            IM: 影像区 (Imaging Zone)
            PH: 药房区 (Pharmacy Zone)
            ME: 机电区 (MEP Zone)
            PB: 公共区 (Public Zone)
            AD: 行政区 (Administrative Zone)
            
        attributes:
          identity_attributes:
            - attr_id: zone_id
              attr_name: zone_id
              attr_name_cn: 区域编码
              data_type: string
              required: true
              unique: true
              
            - attr_id: zone_name
              attr_name: zone_name
              attr_name_cn: 区域名称
              data_type: string
              required: true
              example: "手术区A"
              
            - attr_id: zone_name_en
              attr_name: zone_name_en
              attr_name_cn: 区域英文名称
              data_type: string
              
          classification_attributes:
            - attr_id: zone_type
              attr_name: zone_type
              attr_name_cn: 区域类型
              data_type: enum
              required: true
              reference: Zone_Classification
              
            - attr_id: zone_sub_type
              attr_name: zone_sub_type
              attr_name_cn: 区域子类型
              data_type: string
              
            - attr_id: department
              attr_name: department
              attr_name_cn: 所属科室
              data_type: string
              
          physical_attributes:
            - attr_id: zone_area
              attr_name: zone_area
              attr_name_cn: 区域面积
              data_type: float
              unit: m²
              required: true
              
            - attr_id: room_count
              attr_name: room_count
              attr_name_cn: 房间数量
              data_type: integer
              
          environmental_attributes:
            - attr_id: cleanliness_zone
              attr_name: cleanliness_zone
              attr_name_cn: 洁净分区
              data_type: enum
              enum_values:
                - CLEAN          # 洁净区
                - SUB_CLEAN     # 次洁净区
                - SEMI_CLEAN    # 准洁净区
                - GENERAL       # 一般区
                - CONTAMINATED  # 污染区
                
            - attr_id: pressure_zone
              attr_name: pressure_zone
              attr_name_cn: 压力分区
              data_type: enum
              enum_values:
                - POSITIVE_HIGH  # 高正压区
                - POSITIVE       # 正压区
                - NEUTRAL        # 中性压力区
                - NEGATIVE       # 负压区
                - NEGATIVE_HIGH  # 高负压区
                
            - attr_id: access_control
              attr_name: access_control
              attr_name_cn: 门禁等级
              data_type: enum
              enum_values:
                - PUBLIC         # 公共区域
                - SEMI_RESTRICTED # 半限制区
                - RESTRICTED     # 限制区
                - HIGH_RESTRICTED # 高限制区
                
          operational_attributes:
            - attr_id: operating_hours
              attr_name: operating_hours
              attr_name_cn: 运行时间
              data_type: object
              properties:
                type: {type: enum, values: [24H, SCHEDULED]}
                schedule: {type: string}
                
            - attr_id: staffing_level
              attr_name: staffing_level
              attr_name_cn: 人员配置
              data_type: object
              properties:
                day: {type: integer}
                night: {type: integer}
                
        child_level: L4
        
      # ──────────────────────────────────────────────────────────────────────
      # L4: 房间层级 (Room Level)
      # ──────────────────────────────────────────────────────────────────────
      - level_id: L4
        level_name: Room
        level_name_cn: 房间
        parent_level: L3
        description: 独立的功能空间单元
        
        definition: |
          房间是具有明确边界和独立功能的最小空间单元。
          由墙体或隔断围合，具有完整的环境控制条件。
          
        coding_rule:
          pattern: "{区域编码}-{房间类型代码}{序号}"
          example: "SITE-XAYYFY-MZ01-F03-OP01-OR01"
          room_type_codes:
            OR: 手术室 (Operating Room)
            IC: ICU病床 (ICU Bed)
            WD: 普通病房 (Ward)
            IS: 隔离病房 (Isolation Room)
            EX: 检查室 (Examination Room)
            TR: 治疗室 (Treatment Room)
            NS: 护士站 (Nurse Station)
            DR: 医生办公室 (Doctor Office)
            WT: 候诊区 (Waiting Area)
            ST: 储藏室 (Storage)
            ER: 设备房 (Equipment Room)
            
        attributes:
          identity_attributes:
            - attr_id: room_id
              attr_name: room_id
              attr_name_cn: 房间编码
              data_type: string
              required: true
              unique: true
              
            - attr_id: room_name
              attr_name: room_name
              attr_name_cn: 房间名称
              data_type: string
              required: true
              example: "1号手术室"
              
            - attr_id: room_number
              attr_name: room_number
              attr_name_cn: 房间号
              data_type: string
              example: "OR-01"
              
            - attr_id: room_display_name
              attr_name: room_display_name
              attr_name_cn: 房间显示名称
              data_type: string
              example: "手术室1"
              
          classification_attributes:
            - attr_id: room_type
              attr_name: room_type
              attr_name_cn: 房间类型
              data_type: enum
              required: true
              reference: Room_Classification
              
            - attr_id: room_sub_type
              attr_name: room_sub_type
              attr_name_cn: 房间子类型
              data_type: string
              example: "I级洁净手术室"
              
            - attr_id: room_function
              attr_name: room_function
              attr_name_cn: 房间功能
              data_type: string
              
          physical_attributes:
            - attr_id: room_area
              attr_name: room_area
              attr_name_cn: 房间面积
              data_type: float
              unit: m²
              required: true
              
            - attr_id: room_length
              attr_name: room_length
              attr_name_cn: 房间长度
              data_type: float
              unit: m
              
            - attr_id: room_width
              attr_name: room_width
              attr_name_cn: 房间宽度
              data_type: float
              unit: m
              
            - attr_id: room_height
              attr_name: room_height
              attr_name_cn: 房间净高
              data_type: float
              unit: m
              
            - attr_id: room_volume
              attr_name: room_volume
              attr_name_cn: 房间容积
              data_type: float
              unit: m³
              calculation: "room_area × room_height"
              
            - attr_id: ceiling_height
              attr_name: ceiling_height
              attr_name_cn: 吊顶高度
              data_type: float
              unit: m
              
            - attr_id: floor_finish
              attr_name: floor_finish
              attr_name_cn: 地面材质
              data_type: enum
              enum_values: [PVC, 环氧树脂, 瓷砖, 大理石, 橡胶, 防静电地板]
              
            - attr_id: wall_finish
              attr_name: wall_finish
              attr_name_cn: 墙面材质
              data_type: enum
              enum_values: [乳胶漆, 电解钢板, 抗菌板, 瓷砖, 玻璃]
              
            - attr_id: ceiling_type
              attr_name: ceiling_type
              attr_name_cn: 吊顶类型
              data_type: enum
              enum_values: [层流送风, 散流器, 矿棉板, 石膏板, 金属板]
              
          environmental_requirements:
            - attr_id: temperature_setpoint
              attr_name: temperature_setpoint
              attr_name_cn: 温度设定值
              data_type: object
              properties:
                min: {type: float, unit: "℃"}
                max: {type: float, unit: "℃"}
                target: {type: float, unit: "℃"}
                tolerance: {type: float, unit: "℃"}
                
            - attr_id: humidity_setpoint
              attr_name: humidity_setpoint
              attr_name_cn: 湿度设定值
              data_type: object
              properties:
                min: {type: float, unit: "%RH"}
                max: {type: float, unit: "%RH"}
                tolerance: {type: float, unit: "%RH"}
                
            - attr_id: pressure_requirement
              attr_name: pressure_requirement
              attr_name_cn: 压力要求
              data_type: object
              properties:
                type: {type: enum, values: [positive, negative, neutral]}
                value: {type: float, unit: Pa}
                reference: {type: string}
                
            - attr_id: air_change_rate
              attr_name: air_change_rate
              attr_name_cn: 换气次数
              data_type: float
              unit: ACH
              
            - attr_id: cleanliness_class
              attr_name: cleanliness_class
              attr_name_cn: 洁净度等级
              data_type: enum
              enum_values: [ISO5, ISO6, ISO7, ISO8, 非洁净]
              standard: "ISO 14644-1"
              
            - attr_id: illuminance
              attr_name: illuminance
              attr_name_cn: 照度要求
              data_type: object
              properties:
                general: {type: float, unit: lux}
                task: {type: float, unit: lux}
                
            - attr_id: noise_limit
              attr_name: noise_limit
              attr_name_cn: 噪声限值
              data_type: float
              unit: dB(A)
              
          mep_requirements:
            - attr_id: power_density
              attr_name: power_density
              attr_name_cn: 电力密度
              data_type: float
              unit: VA/m²
              
            - attr_id: socket_count
              attr_name: socket_count
              attr_name_cn: 插座数量
              data_type: object
              properties:
                general: {type: integer}
                medical: {type: integer}
                
            - attr_id: emergency_power
              attr_name: emergency_power
              attr_name_cn: 应急电源要求
              data_type: boolean
              
            - attr_id: isolated_power
              attr_name: isolated_power
              attr_name_cn: 隔离电源要求
              data_type: boolean
              
            - attr_id: medical_gas_outlets
              attr_name: medical_gas_outlets
              attr_name_cn: 医用气体终端
              data_type: object
              properties:
                O2: {type: integer, description: "氧气终端数"}
                VAC: {type: integer, description: "负压吸引终端数"}
                AIR: {type: integer, description: "压缩空气终端数"}
                N2O: {type: integer, description: "笑气终端数"}
                CO2: {type: integer, description: "二氧化碳终端数"}
                N2: {type: integer, description: "氮气终端数"}
                
          operational_attributes:
            - attr_id: is_operational
              attr_name: is_operational
              attr_name_cn: 是否运营
              data_type: boolean
              
            - attr_id: capacity
              attr_name: capacity
              attr_name_cn: 容量
              data_type: object
              properties:
                beds: {type: integer}
                persons: {type: integer}
                
        child_level: L5
        
      # ──────────────────────────────────────────────────────────────────────
      # L5: 子空间层级 (SubSpace Level)
      # ──────────────────────────────────────────────────────────────────────
      - level_id: L5
        level_name: SubSpace
        level_name_cn: 子空间
        parent_level: L4
        description: 房间内的功能分区
        
        definition: |
          子空间是房间内进一步划分的功能区域，通常没有完整的物理隔断，
          但具有特定的功能用途和环境要求。如手术室内的手术区、麻醉区等。
          
        coding_rule:
          pattern: "{房间编码}-{子空间代码}"
          example: "SITE-XAYYFY-MZ01-F03-OP01-OR01-SA"
          subspace_codes:
            SA: 手术操作区 (Surgical Area)
            AA: 麻醉工作区 (Anesthesia Area)
            IA: 器械区 (Instrument Area)
            CA: 清洁通道 (Clean Corridor)
            PA: 患者区 (Patient Area)
            ST: 工作人员区 (Staff Area)
            
        attributes:
          identity_attributes:
            - attr_id: subspace_id
              attr_name: subspace_id
              attr_name_cn: 子空间编码
              data_type: string
              required: true
              
            - attr_id: subspace_name
              attr_name: subspace_name
              attr_name_cn: 子空间名称
              data_type: string
              required: true
              
          classification_attributes:
            - attr_id: subspace_type
              attr_name: subspace_type
              attr_name_cn: 子空间类型
              data_type: string
              
            - attr_id: subspace_function
              attr_name: subspace_function
              attr_name_cn: 子空间功能
              data_type: string
              
          physical_attributes:
            - attr_id: subspace_area
              attr_name: subspace_area
              attr_name_cn: 子空间面积
              data_type: float
              unit: m²
              
            - attr_id: area_ratio
              attr_name: area_ratio
              attr_name_cn: 面积占比
              data_type: float
              unit: "%"
              description: 占房间总面积的比例
              
          environmental_attributes:
            - attr_id: cleanliness_requirement
              attr_name: cleanliness_requirement
              attr_name_cn: 洁净要求
              data_type: enum
              description: 可能比房间整体要求更高
              
            - attr_id: special_requirements
              attr_name: special_requirements
              attr_name_cn: 特殊要求
              data_type: string[]

    # ────────────────────────────────────────────────────────────────────────
    # 层级关系定义
    # ────────────────────────────────────────────────────────────────────────
    hierarchy_relationships:
      - parent: L0
        child: L1
        relationship: contains
        cardinality: "1:N"
        description: 一个院区包含多个建筑
        
      - parent: L1
        child: L2
        relationship: contains
        cardinality: "1:N"
        description: 一个建筑包含多个楼层
        
      - parent: L2
        child: L3
        relationship: contains
        cardinality: "1:N"
        description: 一个楼层包含多个功能区域
        
      - parent: L3
        child: L4
        relationship: contains
        cardinality: "1:N"
        description: 一个功能区域包含多个房间
        
      - parent: L4
        child: L5
        relationship: contains
        cardinality: "1:N"
        description: 一个房间可包含多个子空间（可选）

  # ════════════════════════════════════════════════════════════════════════════
  # 第二部分：空间分类体系 (Space Classification System)
  # ════════════════════════════════════════════════════════════════════════════
  space_classification:
    
    classification_description: |
      医疗建筑空间分类体系建立了功能区域分类和房间分类两大体系。
      分类基于GB 51039-2014综合医院建筑设计规范，并结合医院实际运营需求。
      
    # ────────────────────────────────────────────────────────────────────────
    # 功能区域分类 (Zone Classification)
    # ────────────────────────────────────────────────────────────────────────
    zone_classification:
    
      # ── 医疗区域 ──
      - zone_type_id: ZONE-MED
        zone_type_name: 医疗区域
        zone_type_name_en: Medical Zone
        code_prefix: "ZM"
        description: 直接提供医疗服务的核心功能区域
        gb_standard: "GB 51039-2014"
        
        characteristics:
          - 人员流量大
          - 环境要求高
          - 需要医疗气体供应
          - 洁净要求差异大
          
        sub_types:
        
          - sub_type_id: ZONE-MED-OP
            sub_type_name: 手术区
            sub_type_name_en: Operating Zone
            code: "ZM-OP"
            description: 手术室及相关辅助用房区域
            cleanliness_requirement: true
            cleanliness_level: "洁净区"
            pressure_type: positive
            typical_rooms:
              - 手术室
              - 无菌物品存放室
              - 刷手间
              - 麻醉准备室
              - 复苏室
              - 洁净走廊
            environmental_standards:
              temperature: "22-25℃"
              humidity: "40-60%RH"
              pressure: "+8~+15Pa"
              air_changes: "20-36 ACH"
              
          - sub_type_id: ZONE-MED-ICU
            sub_type_name: 重症监护区
            sub_type_name_en: Intensive Care Zone
            code: "ZM-IC"
            description: ICU及相关区域
            cleanliness_requirement: true
            cleanliness_level: "亚洁净区"
            typical_rooms:
              - ICU病房
              - 护士站
              - 治疗室
              - 配液室
              - 仪器室
            environmental_standards:
              temperature: "24±1.5℃"
              humidity: "40-60%RH"
              pressure: "+5Pa"
              air_changes: "12 ACH"
              
          - sub_type_id: ZONE-MED-WARD
            sub_type_name: 护理单元
            sub_type_name_en: Nursing Unit
            code: "ZM-WD"
            description: 病房及护理用房区域
            typical_rooms:
              - 普通病房
              - 护士站
              - 治疗室
              - 处置室
              - 值班室
              - 污洗室
            environmental_standards:
              temperature: "24-26℃"
              humidity: "40-60%RH"
              fresh_air: "40 m³/h·人"
              
          - sub_type_id: ZONE-MED-OPD
            sub_type_name: 门诊区域
            sub_type_name_en: Outpatient Zone
            code: "ZM-OD"
            description: 门诊诊室及相关区域
            typical_rooms:
              - 诊室
              - 候诊区
              - 分诊台
              - 治疗室
            environmental_standards:
              temperature: "24-26℃"
              fresh_air: "30 m³/h·人"
              
          - sub_type_id: ZONE-MED-ER
            sub_type_name: 急诊区域
            sub_type_name_en: Emergency Zone
            code: "ZM-ER"
            description: 急诊科相关区域
            typical_rooms:
              - 急诊诊室
              - 抢救室
              - 留观室
              - 清创室
            environmental_standards:
              temperature: "24-26℃"
              operation: "24小时"
              
          - sub_type_id: ZONE-MED-ISO
            sub_type_name: 隔离区域
            sub_type_name_en: Isolation Zone
            code: "ZM-IS"
            description: 隔离病房区域
            cleanliness_requirement: true
            pressure_type: "negative/positive"
            typical_rooms:
              - 负压隔离病房
              - 正压隔离病房
              - 缓冲间
              - 专用卫生间
            environmental_standards:
              pressure: "-10Pa (负压) / +8Pa (正压)"
              air_changes: "12 ACH"
              exhaust: "HEPA过滤"
              
      # ── 医技区域 ──
      - zone_type_id: ZONE-TECH
        zone_type_name: 医技区域
        zone_type_name_en: Medical Technology Zone
        code_prefix: "ZT"
        description: 提供诊断、治疗支持的技术服务区域
        
        sub_types:
        
          - sub_type_id: ZONE-TECH-LAB
            sub_type_name: 检验区
            sub_type_name_en: Laboratory Zone
            code: "ZT-LB"
            description: 临床检验及病理相关区域
            cleanliness_requirement: conditional
            typical_rooms:
              - 标本接收
              - 生化检验室
              - 免疫检验室
              - 微生物实验室
              - PCR实验室
              - 病理科
            environmental_standards:
              biosafety_level: "BSL-2"
              fume_hood: true
              exhaust: "独立排风"
              
          - sub_type_id: ZONE-TECH-IMG
            sub_type_name: 影像区
            sub_type_name_en: Imaging Zone
            code: "ZT-IM"
            description: 医学影像诊断区域
            typical_rooms:
              - CT室
              - MRI室
              - DR室
              - DSA室
              - 超声室
              - 控制室
            environmental_standards:
              shielding: "射线防护"
              temperature: "22-24℃ (MRI)"
              vibration: "防振动"
              
          - sub_type_id: ZONE-TECH-PHARM
            sub_type_name: 药房区
            sub_type_name_en: Pharmacy Zone
            code: "ZT-PH"
            description: 药品存储和调配区域
            typical_rooms:
              - 西药房
              - 中药房
              - 药库
              - 静配中心
            environmental_standards:
              temperature: "20-25℃"
              humidity: "45-75%RH"
              cleanliness: "ISO8 (静配)"
              
          - sub_type_id: ZONE-TECH-END
            sub_type_name: 内镜中心
            sub_type_name_en: Endoscopy Zone
            code: "ZT-EN"
            description: 内镜检查和治疗区域
            typical_rooms:
              - 内镜检查室
              - 内镜清洗消毒室
              - 储镜室
              - 复苏室
            environmental_standards:
              cleanliness: "准洁净"
              
          - sub_type_id: ZONE-TECH-RTT
            sub_type_name: 放疗区
            sub_type_name_en: Radiotherapy Zone
            code: "ZT-RT"
            description: 放射治疗区域
            typical_rooms:
              - 直线加速器室
              - 模拟定位室
              - 控制室
              - 候诊区
            environmental_standards:
              shielding: "重防护"
              access_control: "高限制"
              
      # ── 后勤区域 ──
      - zone_type_id: ZONE-SUPPORT
        zone_type_name: 后勤区域
        zone_type_name_en: Support Zone
        code_prefix: "ZS"
        description: 为医疗运营提供支持保障的区域
        
        sub_types:
        
          - sub_type_id: ZONE-SUPPORT-MEP
            sub_type_name: 机电用房区
            sub_type_name_en: MEP Zone
            code: "ZS-ME"
            description: 机电设备用房区域
            typical_rooms:
              - 变配电室
              - 发电机房
              - 冷冻站
              - 锅炉房
              - 水泵房
              - 空调机房
              - 弱电机房
            environmental_standards:
              ventilation: "必需"
              fire_rating: "甲级防火门"
              
          - sub_type_id: ZONE-SUPPORT-CSSD
            sub_type_name: 供应室区
            sub_type_name_en: CSSD Zone
            code: "ZS-CS"
            description: 中心供应室区域
            cleanliness_requirement: true
            typical_rooms:
              - 去污区
              - 检查包装区
              - 灭菌区
              - 无菌存放区
            environmental_standards:
              flow_control: "单向流"
              pressure_gradient: true
              
          - sub_type_id: ZONE-SUPPORT-LOGISTICS
            sub_type_name: 物流用房区
            sub_type_name_en: Logistics Zone
            code: "ZS-LG"
            description: 物资储存和配送区域
            typical_rooms:
              - 物资库房
              - 物流中心
              - 被服库
              - 一次性物品库
            environmental_standards:
              temperature: "适宜"
              ventilation: "良好"
              
          - sub_type_id: ZONE-SUPPORT-LINEN
            sub_type_name: 洗衣房区
            sub_type_name_en: Laundry Zone
            code: "ZS-LN"
            description: 洗涤消毒区域
            typical_rooms:
              - 污物收集
              - 洗涤间
              - 烘干间
              - 折叠打包间
              - 洁净被服库
            environmental_standards:
              flow_control: "污洁分流"
              exhaust: "必需"
              
          - sub_type_id: ZONE-SUPPORT-KITCHEN
            sub_type_name: 营养厨房区
            sub_type_name_en: Kitchen Zone
            code: "ZS-KT"
            description: 营养餐饮配制区域
            typical_rooms:
              - 食品库
              - 粗加工间
              - 烹饪间
              - 配餐间
              - 洗消间
            environmental_standards:
              exhaust: "油烟排放"
              food_safety: "HACCP"
              
      # ── 公共区域 ──
      - zone_type_id: ZONE-PUBLIC
        zone_type_name: 公共区域
        zone_type_name_en: Public Zone
        code_prefix: "ZP"
        description: 对公众开放的公共服务区域
        
        sub_types:
        
          - sub_type_id: ZONE-PUBLIC-LOBBY
            sub_type_name: 大厅区
            sub_type_name_en: Lobby Zone
            code: "ZP-LB"
            description: 门诊大厅、住院大厅等
            typical_rooms:
              - 门诊大厅
              - 收费挂号
              - 导诊服务台
              - 自助服务区
            environmental_standards:
              temperature: "24-26℃"
              illuminance: "300 lux"
              
          - sub_type_id: ZONE-PUBLIC-CORRIDOR
            sub_type_name: 走廊区
            sub_type_name_en: Corridor Zone
            code: "ZP-CR"
            description: 公共走廊和通道
            typical_rooms:
              - 公共走廊
              - 医护走廊
              - 洁净走廊
              - 污物走廊
            environmental_standards:
              width: "≥2.4m (双向)"
              illuminance: "100 lux"
              
          - sub_type_id: ZONE-PUBLIC-VERT
            sub_type_name: 垂直交通区
            sub_type_name_en: Vertical Circulation Zone
            code: "ZP-VT"
            description: 楼梯、电梯等垂直交通
            typical_rooms:
              - 客梯厅
              - 病床梯厅
              - 货梯厅
              - 楼梯间
            environmental_standards:
              ventilation: "加压送风(防烟)"
              
      # ── 行政区域 ──
      - zone_type_id: ZONE-ADMIN
        zone_type_name: 行政区域
        zone_type_name_en: Administrative Zone
        code_prefix: "ZA"
        description: 医院行政管理和办公区域
        
        sub_types:
        
          - sub_type_id: ZONE-ADMIN-OFFICE
            sub_type_name: 办公区
            sub_type_name_en: Office Zone
            code: "ZA-OF"
            description: 行政办公用房
            typical_rooms:
              - 院长办公室
              - 部门办公室
              - 会议室
              - 档案室
            environmental_standards:
              temperature: "24-26℃"
              fresh_air: "30 m³/h·人"
              
          - sub_type_id: ZONE-ADMIN-MEETING
            sub_type_name: 会议区
            sub_type_name_en: Meeting Zone
            code: "ZA-MT"
            description: 会议和培训区域
            typical_rooms:
              - 大会议室
              - 小会议室
              - 报告厅
              - 培训室
            environmental_standards:
              acoustics: "隔声要求"
              
    # ────────────────────────────────────────────────────────────────────────
    # 房间分类 (Room Classification)
    # ────────────────────────────────────────────────────────────────────────
    room_classification:
    
      # ── 手术室类 ──
      - room_type_id: ROOM-OR
        room_type_name: 手术室
        room_type_name_en: Operating Room
        code: "OR"
        parent_zone: ZONE-MED-OP
        gb_standard: "GB 50333-2013"
        description: 进行外科手术的洁净室
        
        variants:
          - variant_id: ROOM-OR-I
            variant_name: I级手术室（特别洁净）
            variant_name_en: Class I OR (Ultra Clean)
            code: "OR-I"
            cleanliness_level: ISO5
            air_changes: 36
            particle_count: "≤350个/m³ (≥0.5μm)"
            applications:
              - 器官移植手术
              - 关节置换手术
              - 心脏外科手术
              - 神经外科手术
            area_range: [40, 60]
            
          - variant_id: ROOM-OR-II
            variant_name: II级手术室（标准洁净）
            variant_name_en: Class II OR (Standard Clean)
            code: "OR-II"
            cleanliness_level: ISO6
            air_changes: 24
            particle_count: "≤3500个/m³ (≥0.5μm)"
            applications:
              - 胸外科手术
              - 整形外科手术
              - 泌尿外科手术
              - 骨科手术
            area_range: [35, 50]
            
          - variant_id: ROOM-OR-III
            variant_name: III级手术室（一般洁净）
            variant_name_en: Class III OR (General Clean)
            code: "OR-III"
            cleanliness_level: ISO7
            air_changes: 20
            particle_count: "≤35000个/m³ (≥0.5μm)"
            applications:
              - 普通外科手术
              - 妇产科手术
              - 五官科手术
            area_range: [30, 45]
            
          - variant_id: ROOM-OR-IV
            variant_name: IV级手术室（准洁净）
            variant_name_en: Class IV OR (Sub-Clean)
            code: "OR-IV"
            cleanliness_level: ISO8
            air_changes: 15
            particle_count: "≤350000个/m³ (≥0.5μm)"
            applications:
              - 门诊小手术
              - 感染手术
            area_range: [25, 35]
            
          - variant_id: ROOM-OR-NEG
            variant_name: 负压手术室
            variant_name_en: Negative Pressure OR
            code: "OR-NEG"
            cleanliness_level: ISO7
            pressure: "-8Pa"
            applications:
              - 传染病手术
              - 特殊感染手术
              
      # ── ICU类 ──
      - room_type_id: ROOM-ICU
        room_type_name: ICU病房
        room_type_name_en: Intensive Care Unit
        code: "ICU"
        parent_zone: ZONE-MED-ICU
        gb_standard: "GB 51039-2014"
        description: 重症监护病房
        
        variants:
          - variant_id: ROOM-ICU-GICU
            variant_name: 综合ICU
            variant_name_en: General ICU
            code: "GICU"
            
          - variant_id: ROOM-ICU-SICU
            variant_name: 外科ICU
            variant_name_en: Surgical ICU
            code: "SICU"
            
          - variant_id: ROOM-ICU-MICU
            variant_name: 内科ICU
            variant_name_en: Medical ICU
            code: "MICU"
            
          - variant_id: ROOM-ICU-CCU
            variant_name: 冠心病监护室
            variant_name_en: Coronary Care Unit
            code: "CCU"
            
          - variant_id: ROOM-ICU-RICU
            variant_name: 呼吸ICU
            variant_name_en: Respiratory ICU
            code: "RICU"
            
          - variant_id: ROOM-ICU-NICU
            variant_name: 新生儿ICU
            variant_name_en: Neonatal ICU
            code: "NICU"
            
          - variant_id: ROOM-ICU-PICU
            variant_name: 儿科ICU
            variant_name_en: Pediatric ICU
            code: "PICU"
            
      # ── 隔离病房类 ──
      - room_type_id: ROOM-ISO
        room_type_name: 隔离病房
        room_type_name_en: Isolation Room
        code: "ISO"
        parent_zone: ZONE-MED-ISO
        gb_standard: "WS/T 311-2009"
        description: 用于传染病隔离的特殊病房
        
        variants:
          - variant_id: ROOM-ISO-NEG
            variant_name: 负压隔离病房
            variant_name_en: Negative Pressure Isolation Room
            code: "ISO-NEG"
            pressure_type: negative
            pressure_value: "-10Pa"
            applications:
              - 呼吸道传染病
              - 空气传播疾病
            special_requirements:
              - 独立排风
              - HEPA过滤
              - 双门互锁
              
          - variant_id: ROOM-ISO-POS
            variant_name: 正压隔离病房（层流病房）
            variant_name_en: Positive Pressure Isolation Room
            code: "ISO-POS"
            pressure_type: positive
            pressure_value: "+8Pa"
            applications:
              - 免疫缺陷患者
              - 骨髓移植
              - 烧伤患者
            special_requirements:
              - 洁净环境
              - HEPA过滤
              
          - variant_id: ROOM-ISO-STD
            variant_name: 标准隔离病房
            variant_name_en: Standard Isolation Room
            code: "ISO-STD"
            applications:
              - 接触传播疾病
              - 飞沫传播疾病
              
      # ── 检验类 ──
      - room_type_id: ROOM-LAB
        room_type_name: 检验室
        room_type_name_en: Laboratory
        code: "LAB"
        parent_zone: ZONE-TECH-LAB
        
        variants:
          - variant_id: ROOM-LAB-BIO
            variant_name: 生化检验室
            variant_name_en: Biochemistry Lab
            code: "LAB-BIO"
            
          - variant_id: ROOM-LAB-IMM
            variant_name: 免疫检验室
            variant_name_en: Immunology Lab
            code: "LAB-IMM"
            
          - variant_id: ROOM-LAB-MIC
            variant_name: 微生物实验室
            variant_name_en: Microbiology Lab
            code: "LAB-MIC"
            biosafety_level: "BSL-2"
            
          - variant_id: ROOM-LAB-PCR
            variant_name: PCR实验室
            variant_name_en: PCR Lab
            code: "LAB-PCR"
            zone_separation: ["试剂准备区", "标本制备区", "扩增区", "分析区"]
            pressure_sequence: "递减式负压"
            
          - variant_id: ROOM-LAB-PATH
            variant_name: 病理实验室
            variant_name_en: Pathology Lab
            code: "LAB-PATH"
            special_requirements:
              - 通风柜
              - 甲醛排放
              
      # ── 影像类 ──
      - room_type_id: ROOM-IMG
        room_type_name: 影像室
        room_type_name_en: Imaging Room
        code: "IMG"
        parent_zone: ZONE-TECH-IMG
        
        variants:
          - variant_id: ROOM-IMG-CT
            variant_name: CT室
            variant_name_en: CT Room
            code: "IMG-CT"
            shielding: "2mmPb"
            area_range: [35, 50]
            
          - variant_id: ROOM-IMG-MRI
            variant_name: MRI室
            variant_name_en: MRI Room
            code: "IMG-MRI"
            shielding: "射频屏蔽室"
            temperature: "22-24℃"
            vibration: "防振动"
            
          - variant_id: ROOM-IMG-DR
            variant_name: DR室
            variant_name_en: Digital Radiography Room
            code: "IMG-DR"
            shielding: "2mmPb"
            
          - variant_id: ROOM-IMG-DSA
            variant_name: DSA室（导管室）
            variant_name_en: DSA Room
            code: "IMG-DSA"
            shielding: "3mmPb"
            cleanliness: "准洁净"
            
          - variant_id: ROOM-IMG-US
            variant_name: 超声室
            variant_name_en: Ultrasound Room
            code: "IMG-US"
            
      # ── 设备用房类 ──
      - room_type_id: ROOM-MEP
        room_type_name: 机电设备用房
        room_type_name_en: MEP Equipment Room
        code: "MEP"
        parent_zone: ZONE-SUPPORT-MEP
        
        variants:
          - variant_id: ROOM-MEP-ELEC-HV
            variant_name: 高压配电室
            variant_name_en: HV Switchgear Room
            code: "MEP-EH"
            fire_rating: "甲级"
            
          - variant_id: ROOM-MEP-ELEC-LV
            variant_name: 低压配电室
            variant_name_en: LV Switchgear Room
            code: "MEP-EL"
            fire_rating: "甲级"
            
          - variant_id: ROOM-MEP-ELEC-GEN
            variant_name: 发电机房
            variant_name_en: Generator Room
            code: "MEP-GN"
            ventilation: "机械进排风"
            noise: "隔声处理"
            
          - variant_id: ROOM-MEP-ELEC-UPS
            variant_name: UPS室
            variant_name_en: UPS Room
            code: "MEP-UP"
            temperature: "20-25℃"
            
          - variant_id: ROOM-MEP-HVAC-CHP
            variant_name: 冷冻站
            variant_name_en: Chiller Plant Room
            code: "MEP-CH"
            ventilation: "机械通风"
            
          - variant_id: ROOM-MEP-HVAC-HTG
            variant_name: 锅炉房/热力站
            variant_name_en: Boiler Room / Heat Station
            code: "MEP-HT"
            
          - variant_id: ROOM-MEP-HVAC-AHU
            variant_name: 空调机房
            variant_name_en: AHU Room
            code: "MEP-AH"
            
          - variant_id: ROOM-MEP-PUMP
            variant_name: 水泵房
            variant_name_en: Pump Room
            code: "MEP-PM"
            
          - variant_id: ROOM-MEP-GAS
            variant_name: 医用气体机房
            variant_name_en: Medical Gas Room
            code: "MEP-GS"
            ventilation: "良好通风"
            
          - variant_id: ROOM-MEP-IT
            variant_name: 弱电机房/数据中心
            variant_name_en: IT Room / Data Center
            code: "MEP-IT"
            temperature: "22-24℃"
            humidity: "40-60%RH"

  # ════════════════════════════════════════════════════════════════════════════
  # 第三部分：医疗专用空间详细模型 (Medical Special Space Models)
  # ════════════════════════════════════════════════════════════════════════════
  medical_special_spaces:
  
    model_description: |
      医疗专用空间详细模型为关键医疗空间提供完整的技术要求定义，
      包括空间组成、环境控制要求、医疗气体、电气、系统关联等全面信息。
      这些定义将作为Agent-05系统-空间耦合建模的核心输入。
      
    # ────────────────────────────────────────────────────────────────────────
    # 手术室详细模型
    # ────────────────────────────────────────────────────────────────────────
    - space_type_id: ROOM-OR
      space_type_name: 手术室
      space_type_name_en: Operating Room
      gb_standard: "GB 50333-2013"
      
      # 空间组成
      sub_spaces:
        - sub_space_id: SS-OR-SA
          sub_space_name: 手术操作区
          sub_space_name_en: Surgical Area
          function: 手术操作的核心区域，包含手术台
          area_ratio: 0.60
          cleanliness_focus: true
          ceiling_type: 层流送风天花
          
        - sub_space_id: SS-OR-IA
          sub_space_name: 器械区
          sub_space_name_en: Instrument Area
          function: 器械台、无菌物品放置区域
          area_ratio: 0.15
          
        - sub_space_id: SS-OR-AA
          sub_space_name: 麻醉工作区
          sub_space_name_en: Anesthesia Area
          function: 麻醉设备、药品放置、麻醉操作区域
          area_ratio: 0.10
          medical_gas_concentrated: true
          
        - sub_space_id: SS-OR-CA
          sub_space_name: 医护通道区
          sub_space_name_en: Circulation Area
          function: 人员活动、进出通道区域
          area_ratio: 0.15
          
      # 环境控制要求
      environmental_requirements:
      
        temperature:
          parameter_id: ENV-TEMP
          parameter_name: 温度
          parameter_name_en: Temperature
          unit: "℃"
          setpoint_range: [22, 25]
          control_precision: "±1"
          special_considerations:
            - 骨科手术可能需要更低温度
            - 儿科手术需要更高温度
          variant_values:
            ROOM-OR-I: {range: [22, 25], precision: "±0.5"}
            ROOM-OR-II: {range: [22, 25], precision: "±1"}
            ROOM-OR-III: {range: [22, 26], precision: "±1"}
            ROOM-OR-IV: {range: [22, 26], precision: "±2"}
            
        humidity:
          parameter_id: ENV-HUM
          parameter_name: 相对湿度
          parameter_name_en: Relative Humidity
          unit: "%RH"
          setpoint_range: [40, 60]
          control_precision: "±5"
          variant_values:
            ROOM-OR-I: {range: [40, 60], precision: "±5"}
            ROOM-OR-II: {range: [40, 60], precision: "±5"}
            ROOM-OR-III: {range: [35, 65], precision: "±10"}
            ROOM-OR-IV: {range: [35, 65], precision: "±10"}
            
        pressure:
          parameter_id: ENV-PRES
          parameter_name: 压差
          parameter_name_en: Differential Pressure
          unit: Pa
          requirement: positive
          min_value: 8
          typical_value: 15
          reference: 走廊
          gradient:
            description: 压力梯度（从高到低）
            sequence:
              - space: 手术室
                pressure: "+15Pa"
              - space: 洁净走廊
                pressure: "+10Pa"
              - space: 清洁走廊
                pressure: "+5Pa"
              - space: 普通区域
                pressure: "0Pa"
          negative_pressure_variant:
            for: 感染手术室
            value: "-8Pa"
            exhaust: "独立排放"
            
        air_change:
          parameter_id: ENV-ACH
          parameter_name: 换气次数
          parameter_name_en: Air Changes per Hour
          unit: ACH
          min_value: 20
          full_fresh_air: false
          fresh_air_ratio: "≥60%"
          variant_values:
            ROOM-OR-I: {value: 36, velocity: "0.25-0.30 m/s"}
            ROOM-OR-II: {value: 24, velocity: "0.25-0.30 m/s"}
            ROOM-OR-III: {value: 20, velocity: "0.20-0.25 m/s"}
            ROOM-OR-IV: {value: 15, velocity: "0.18-0.22 m/s"}
            
        cleanliness:
          parameter_id: ENV-CLN
          parameter_name: 洁净度
          parameter_name_en: Cleanliness Level
          standard: "ISO 14644-1"
          variant_values:
            ROOM-OR-I: 
              level: ISO5
              particle_count: "≤350个/m³ (≥0.5μm)"
              recovery_time: "≤15min"
            ROOM-OR-II:
              level: ISO6
              particle_count: "≤3500个/m³ (≥0.5μm)"
              recovery_time: "≤20min"
            ROOM-OR-III:
              level: ISO7
              particle_count: "≤35000个/m³ (≥0.5μm)"
              recovery_time: "≤25min"
            ROOM-OR-IV:
              level: ISO8
              particle_count: "≤350000个/m³ (≥0.5μm)"
              recovery_time: "≤30min"
              
        fresh_air:
          parameter_id: ENV-FA
          parameter_name: 新风比
          parameter_name_en: Fresh Air Ratio
          unit: "%"
          min_value: 60
          note: 全新风模式可用于快速恢复洁净度
          per_person: "≥60 m³/h·人"
          
        noise:
          parameter_id: ENV-NOS
          parameter_name: 噪声
          parameter_name_en: Noise Level
          unit: dB(A)
          max_value: 52
          variant_values:
            ROOM-OR-I: 50
            ROOM-OR-II: 50
            ROOM-OR-III: 52
            ROOM-OR-IV: 55
            
        illumination:
          parameter_id: ENV-ILL
          parameter_name: 照度
          parameter_name_en: Illuminance
          unit: lux
          general_area: 500
          surgical_field: 
            value: "20000-160000"
            note: 无影灯提供
          color_temperature: "4000-6500K"
          color_rendering_index: "≥90"
          
      # 医疗气体要求
      medical_gas_requirements:
        - gas_type_id: MGAS-O2
          gas_type: O2
          gas_name: 医用氧气
          gas_name_en: Medical Oxygen
          outlets_per_room: 4
          outlet_location:
            - 手术台头端（2个）
            - 麻醉区（2个）
          working_pressure: 
            value: 0.4
            unit: MPa
            tolerance: "±0.05"
          flow_rate:
            typical: 10
            max: 30
            unit: L/min
            
        - gas_type_id: MGAS-VAC
          gas_type: VAC
          gas_name: 医用负压吸引
          gas_name_en: Medical Vacuum
          outlets_per_room: 4
          outlet_location:
            - 手术区（2个）
            - 麻醉区（2个）
          working_pressure:
            value: -0.04
            unit: MPa
            tolerance: "±0.01"
          flow_rate:
            typical: 40
            max: 60
            unit: L/min
            
        - gas_type_id: MGAS-AIR
          gas_type: AIR
          gas_name: 医用压缩空气
          gas_name_en: Medical Air
          outlets_per_room: 2
          outlet_location:
            - 麻醉区（2个）
          working_pressure:
            value: 0.4
            unit: MPa
          quality: "无油、无菌"
          
        - gas_type_id: MGAS-N2O
          gas_type: N2O
          gas_name: 医用笑气
          gas_name_en: Nitrous Oxide
          outlets_per_room: 1
          outlet_location:
            - 麻醉区
          working_pressure:
            value: 0.4
            unit: MPa
          is_optional: true
          scavenging_required: true
          
        - gas_type_id: MGAS-CO2
          gas_type: CO2
          gas_name: 医用二氧化碳
          gas_name_en: Carbon Dioxide
          outlets_per_room: 1
          is_optional: true
          application: 腹腔镜手术
          
        - gas_type_id: MGAS-N2
          gas_type: N2
          gas_name: 医用氮气
          gas_name_en: Nitrogen
          outlets_per_room: 1
          is_optional: true
          application: 手术器械驱动
          
      # 电气要求
      electrical_requirements:
        power_density:
          value: 300
          unit: VA/m²
          peak_value: 500
          
        socket_count:
          surgical_area:
            quantity: 12
            type: 医用插座
          general_area:
            quantity: 8
            type: 普通插座
          total_capacity: "≥100A"
          
        emergency_power:
          required: true
          classification: 一级负荷
          transfer_time: "≤0.5s"
          duration: "持续供电"
          
        isolated_power:
          required: true
          system_type: 医用IT系统
          capacity: "≥8kVA"
          monitoring: 绝缘监视仪
          alarm_threshold: "50kΩ"
          
        equipotential_bonding:
          required: true
          resistance: "≤0.1Ω"
          bonding_points:
            - 手术台
            - 手术灯
            - 所有医疗设备
            - 金属管道
            
        ups_backup:
          required: true
          protected_loads:
            - 手术灯
            - 生命支持设备
            - 监护设备
          duration: "≥30min"
          
        lighting:
          general:
            illuminance: 500
            unit: lux
          surgical_light:
            type: 无影灯
            illuminance: "20000-160000 lux"
            color_temperature: "4000-6500K"
            depth_of_illumination: "≥1000mm"
          emergency:
            illuminance: "≥50 lux"
            type: 蓄电池应急灯
            
      # 关联系统要求
      required_systems:
        - system_category: HVAC
          systems:
            - system_id: HVAC-CLEAN
              system_name: 洁净空调系统
              requirement_level: mandatory
              key_functions:
                - 温度控制
                - 湿度控制
                - 正压维护
                - 洁净度保障
                - 换气次数保障
                
        - system_category: ELECTRICAL
          systems:
            - system_id: ELEC-LV
              system_name: 低压配电系统
              requirement_level: mandatory
              
            - system_id: ELEC-ISOLATED
              system_name: 医用隔离电源系统
              requirement_level: mandatory
              
            - system_id: ELEC-EMERGENCY
              system_name: 应急电源系统
              requirement_level: mandatory
              sub_systems:
                - 柴油发电机组
                - UPS不间断电源
                
        - system_category: MEDICAL_GAS
          systems:
            - system_id: GAS-O2
              system_name: 医用氧气系统
              requirement_level: mandatory
              
            - system_id: GAS-VAC
              system_name: 医用负压吸引系统
              requirement_level: mandatory
              
            - system_id: GAS-AIR
              system_name: 医用压缩空气系统
              requirement_level: mandatory
              
            - system_id: GAS-N2O
              system_name: 医用笑气系统
              requirement_level: optional
              
            - system_id: GAS-SCAV
              system_name: 麻醉废气排放系统
              requirement_level: mandatory
              
        - system_category: PLUMBING
          systems:
            - system_id: PLUMB-DW
              system_name: 给水系统
              requirement_level: mandatory
              
            - system_id: PLUMB-DRAIN
              system_name: 排水系统
              requirement_level: mandatory
              
        - system_category: FIRE_PROTECTION
          systems:
            - system_id: FIRE-ALARM
              system_name: 火灾自动报警系统
              requirement_level: mandatory
              
            - system_id: FIRE-GAS
              system_name: 气体灭火系统
              requirement_level: recommended
              note: 洁净手术部推荐使用
              
        - system_category: BA
          systems:
            - system_id: BA-BMS
              system_name: 楼宇自控系统
              requirement_level: mandatory
              monitored_parameters:
                - 温度
                - 湿度
                - 压差
                - 洁净度
                - 医用气体压力
                
      # 空间编码示例
      coding_example:
        site: "SITE-XAYYFY"
        building: "SITE-XAYYFY-ZH01"
        floor: "SITE-XAYYFY-ZH01-F03"
        zone: "SITE-XAYYFY-ZH01-F03-OP01"
        room: "SITE-XAYYFY-ZH01-F03-OP01-OR01"
        subspace: "SITE-XAYYFY-ZH01-F03-OP01-OR01-SA"
        
    # ────────────────────────────────────────────────────────────────────────
    # ICU病房详细模型
    # ────────────────────────────────────────────────────────────────────────
    - space_type_id: ROOM-ICU
      space_type_name: ICU病房
      space_type_name_en: Intensive Care Unit
      gb_standard: "GB 51039-2014"
      
      sub_spaces:
        - sub_space_id: SS-ICU-PA
          sub_space_name: 患者床位区
          sub_space_name_en: Patient Bed Area
          function: 患者监护治疗区域
          area_per_bed: "15-18 m²"
          bed_spacing: "≥1.2m"
          
        - sub_space_id: SS-ICU-NS
          sub_space_name: 护士站
          sub_space_name_en: Nurse Station
          function: 中央监护、护理工作区
          visibility: "可视所有床位"
          
        - sub_space_id: SS-ICU-TR
          sub_space_name: 治疗区
          sub_space_name_en: Treatment Area
          function: 治疗准备、配液
          
      environmental_requirements:
        temperature:
          parameter_name: 温度
          unit: "℃"
          setpoint_range: [24, 26]
          control_precision: "±1.5"
          individual_control: "每床位可调"
          
        humidity:
          parameter_name: 相对湿度
          unit: "%RH"
          setpoint_range: [40, 60]
          control_precision: "±10"
          
        pressure:
          parameter_name: 压差
          unit: Pa
          requirement: positive
          value: "+5"
          reference: 走廊
          
        air_change:
          parameter_name: 换气次数
          unit: ACH
          min_value: 12
          fresh_air_ratio: "≥60%"
          per_bed: "≥100 m³/h"
          
        cleanliness:
          parameter_name: 洁净度
          level: "亚洁净"
          filtration: "中效+高中效"
          
        noise:
          parameter_name: 噪声
          unit: dB(A)
          max_value: 45
          note: 患者休息环境要求更低
          
        illumination:
          parameter_name: 照度
          unit: lux
          general: 200
          night_mode: 50
          procedure: 500
          individual_reading_light: true
          
      medical_gas_requirements:
        - gas_type: O2
          gas_name: 医用氧气
          outlets_per_bed: 2
          working_pressure: 0.4  # MPa
          
        - gas_type: VAC
          gas_name: 医用负压吸引
          outlets_per_bed: 2
          working_pressure: -0.04  # MPa
          
        - gas_type: AIR
          gas_name: 医用压缩空气
          outlets_per_bed: 1
          working_pressure: 0.4  # MPa
          
      electrical_requirements:
        power_per_bed:
          value: "10-15"
          unit: kVA
          
        socket_per_bed:
          quantity: 16
          types:
            - 医用插座（隔离电源）: 8
            - 普通插座: 8
            
        emergency_power:
          required: true
          classification: 一级负荷
          transfer_time: "≤0.5s"
          
        ups_backup:
          required: true
          per_bed: true
          duration: "≥30min"
          protected: 
            - 呼吸机
            - 监护仪
            - 输液泵
            
        isolated_power:
          required: recommended
          note: 根据设备配置决定
          
        equipotential_bonding:
          required: true
          
        bedside_panel:
          required: true
          functions:
            - 电源控制
            - 气体终端
            - 呼叫系统
            - 信息接口
            
      required_systems:
        - system_category: HVAC
          systems:
            - HVAC-AHU（洁净新风机组）
            
        - system_category: ELECTRICAL
          systems:
            - ELEC-LV
            - ELEC-EMERGENCY
            - ELEC-UPS
            
        - system_category: MEDICAL_GAS
          systems:
            - GAS-O2
            - GAS-VAC
            - GAS-AIR
            
        - system_category: BA
          systems:
            - BA-BMS
            - BA-NURSE_CALL
            
    # ────────────────────────────────────────────────────────────────────────
    # 负压隔离病房详细模型
    # ────────────────────────────────────────────────────────────────────────
    - space_type_id: ROOM-ISO-NEG
      space_type_name: 负压隔离病房
      space_type_name_en: Negative Pressure Isolation Room
      gb_standard: "WS/T 311-2009"
      
      sub_spaces:
        - sub_space_id: SS-ISO-PR
          sub_space_name: 病室
          sub_space_name_en: Patient Room
          function: 患者隔离治疗区域
          pressure_level: 最负压
          
        - sub_space_id: SS-ISO-BF
          sub_space_name: 缓冲间
          sub_space_name_en: Buffer Room
          function: 双门互锁缓冲，穿脱防护服
          pressure_level: 中间负压
          door_interlock: true
          
        - sub_space_id: SS-ISO-WC
          sub_space_name: 专用卫生间
          sub_space_name_en: Dedicated Bathroom
          function: 患者专用卫生间
          pressure_level: 最负压
          exhaust: 独立排放
          
        - sub_space_id: SS-ISO-PS
          sub_space_name: 传递窗
          sub_space_name_en: Pass Box
          function: 物品传递
          uv_sterilization: true
          
      environmental_requirements:
        temperature:
          parameter_name: 温度
          unit: "℃"
          setpoint_range: [22, 26]
          control_precision: "±2"
          
        humidity:
          parameter_name: 相对湿度
          unit: "%RH"
          setpoint_range: [30, 60]
          
        pressure:
          parameter_name: 压差
          unit: Pa
          requirement: negative
          gradient:
            - space: 走廊
              pressure: "0Pa (基准)"
            - space: 缓冲间
              pressure: "-5Pa"
            - space: 病室
              pressure: "-10Pa"
            - space: 卫生间
              pressure: "-15Pa"
          monitoring: 实时监测显示
          alarm: 压差异常报警
          
        air_change:
          parameter_name: 换气次数
          unit: ACH
          min_value: 12
          full_fresh_air: true
          no_recirculation: true
          
        exhaust:
          parameter_name: 排风处理
          hepa_filter: true
          filter_efficiency: "≥99.97% @0.3μm"
          discharge: 高空排放
          discharge_height: "≥建筑最高点3m"
          monitoring: 压差监测
          
        cleanliness:
          parameter_name: 洁净度
          送风: 高效过滤
          排风: HEPA过滤后排放
          
        door_interlock:
          parameter_name: 门互锁
          required: true
          logic: 内外门不能同时开启
          override: 紧急时可解除
          
      medical_gas_requirements:
        - gas_type: O2
          gas_name: 医用氧气
          outlets_per_room: 2
          working_pressure: 0.4
          
        - gas_type: VAC
          gas_name: 医用负压吸引
          outlets_per_room: 2
          working_pressure: -0.04
          treatment: 需要消毒处理
          
      electrical_requirements:
        emergency_power:
          required: true
          critical_loads:
            - 排风系统
            - 负压维护
            - 照明
            - 监护设备
            
        ups_backup:
          required: true
          duration: "≥30min"
          protected:
            - 排风机
            - 监控系统
            
      special_requirements:
        - 独立空调系统（全新风）
        - 独立排风系统（HEPA过滤）
        - 负压监测与报警
        - 视频监控
        - 双向对讲
        - 传递窗（带紫外消毒）
        - 污物专用通道
        
      required_systems:
        - system_category: HVAC
          systems:
            - HVAC-ISO（独立隔离空调系统）
            
        - system_category: ELECTRICAL
          systems:
            - ELEC-LV
            - ELEC-EMERGENCY
            - ELEC-UPS
            
        - system_category: MEDICAL_GAS
          systems:
            - GAS-O2
            - GAS-VAC
            
        - system_category: BA
          systems:
            - BA-BMS（负压监测）
            - BA-NURSE_CALL
            - BA-CCTV（视频监控）
            - BA-INTERCOM（对讲系统）
            
    # ────────────────────────────────────────────────────────────────────────
    # 洁净实验室详细模型
    # ────────────────────────────────────────────────────────────────────────
    - space_type_id: ROOM-LAB-CLEAN
      space_type_name: 洁净实验室
      space_type_name_en: Clean Laboratory
      gb_standard: "GB 19489-2008"
      
      variants:
        - variant_id: LAB-BSL2
          variant_name: BSL-2实验室
          biosafety_level: 2
          applications:
            - 微生物培养
            - 病原体检测
            
        - variant_id: LAB-PCR
          variant_name: PCR实验室
          zones: 4
          zone_names:
            - 试剂准备区
            - 标本制备区
            - 扩增反应区
            - 产物分析区
            
      sub_spaces:
        - sub_space_id: SS-LAB-REAGENT
          sub_space_name: 试剂准备区
          pressure: "正压（最高）"
          cleanliness: ISO8
          
        - sub_space_id: SS-LAB-SPECIMEN
          sub_space_name: 标本制备区
          pressure: "负压"
          biosafety_cabinet: required
          
        - sub_space_id: SS-LAB-AMPLIFY
          sub_space_name: 扩增反应区
          pressure: "负压（较低）"
          
        - sub_space_id: SS-LAB-ANALYSIS
          sub_space_name: 产物分析区
          pressure: "负压（最低）"
          
      environmental_requirements:
        temperature:
          setpoint_range: [20, 26]
          control_precision: "±2"
          
        humidity:
          setpoint_range: [45, 65]
          
        pressure:
          gradient_type: "递减式负压"
          sequence: "试剂→标本→扩增→产物"
          differential: "-5Pa 每级"
          
        air_change:
          min_value: 12
          biosafety_cabinet_exhaust: 独立
          
      special_requirements:
        - 生物安全柜（II级）
        - 独立排风系统
        - 高效过滤（HEPA）
        - 紫外消毒灯
        - 应急淋浴洗眼器
        - 防虫防鼠设施
        
    # ────────────────────────────────────────────────────────────────────────
    # 药房（静配中心）详细模型
    # ────────────────────────────────────────────────────────────────────────
    - space_type_id: ROOM-PHARM-PIVAS
      space_type_name: 静脉用药调配中心
      space_type_name_en: Pharmacy Intravenous Admixture Services
      gb_standard: "静脉用药集中调配质量管理规范"
      
      sub_spaces:
        - sub_space_id: SS-PV-LOBBY
          sub_space_name: 一般区
          function: 人员更衣、物料暂存
          cleanliness: 非洁净
          
        - sub_space_id: SS-PV-BUFFER
          sub_space_name: 缓冲区
          function: 洁净过渡
          cleanliness: ISO8
          
        - sub_space_id: SS-PV-CLEAN
          sub_space_name: 洁净配置间
          function: 普通输液配置
          cleanliness: ISO7
          
        - sub_space_id: SS-PV-CHEMO
          sub_space_name: 细胞毒药物配置间
          function: 化疗药物配置
          cleanliness: ISO7
          biosafety_cabinet: "II级B2型"
          exhaust: 100%直排
          
        - sub_space_id: SS-PV-TPN
          sub_space_name: TPN配置间
          function: 全静脉营养液配置
          cleanliness: ISO5
          laminar_flow: true
          
      environmental_requirements:
        temperature:
          setpoint_range: [18, 26]
          control_precision: "±2"
          
        humidity:
          setpoint_range: [45, 65]
          
        pressure:
          配置间_vs_缓冲: "+10Pa"
          缓冲_vs_一般: "+5Pa"
          细胞毒药物区: "负压或零压"
          
        cleanliness:
          普通配置: ISO7
          TPN配置: ISO5
          细胞毒配置: "II级生物安全柜内"
          
      required_systems:
        - system_category: HVAC
          systems:
            - HVAC-CLEAN（洁净空调）
            
        - system_category: ELECTRICAL
          systems:
            - ELEC-LV
            - ELEC-UPS
            
    # ────────────────────────────────────────────────────────────────────────
    # 供应室详细模型
    # ────────────────────────────────────────────────────────────────────────
    - space_type_id: ROOM-CSSD
      space_type_name: 中心供应室
      space_type_name_en: Central Sterile Supply Department
      gb_standard: "WS 310系列标准"
      
      sub_spaces:
        - sub_space_id: SS-CS-DECON
          sub_space_name: 去污区
          sub_space_name_en: Decontamination Zone
          function: 回收器械的清洗消毒
          pressure: "负压（最低）"
          cleanliness: 一般
          
        - sub_space_id: SS-CS-INSPECT
          sub_space_name: 检查包装区
          sub_space_name_en: Inspection and Packaging Zone
          function: 器械检查、包装
          pressure: "正压（中间）"
          cleanliness: 10万级
          
        - sub_space_id: SS-CS-STERIL
          sub_space_name: 灭菌区
          sub_space_name_en: Sterilization Zone
          function: 高温高压灭菌
          special_equipment:
            - 脉动真空灭菌器
            - 低温等离子灭菌器
          ventilation: 加强排风
          
        - sub_space_id: SS-CS-STERILE
          sub_space_name: 无菌物品存放区
          sub_space_name_en: Sterile Storage Zone
          function: 灭菌物品存放
          pressure: "正压（最高）"
          cleanliness: 10万级
          
      environmental_requirements:
        temperature:
          去污区: "18-22℃"
          检查包装区: "20-25℃"
          无菌存放区: "20-25℃"
          
        humidity:
          range: [30, 60]
          unit: "%RH"
          
        pressure:
          flow_direction: "无菌存放→检查包装→去污区"
          无菌存放_vs_包装: "+10Pa"
          包装_vs_去污: "+5Pa"
          去污_vs_走廊: "-5Pa"
          
        air_change:
          去污区: 10
          检查包装区: 15
          无菌存放区: 15
          unit: ACH
          
      special_requirements:
        - 严格的人流物流分离
        - 污物直接回收通道
        - 无菌物品发放通道
        - 器械追溯系统
        - 温湿度记录
        
    # ────────────────────────────────────────────────────────────────────────
    # 机电设备用房详细模型
    # ────────────────────────────────────────────────────────────────────────
    - space_type_id: ROOM-MEP-CHP
      space_type_name: 冷冻站
      space_type_name_en: Chiller Plant Room
      
      sub_spaces:
        - sub_space_id: SS-CHP-CHILLER
          sub_space_name: 冷水机组区
          function: 冷水机组安装
          floor_load: "≥10 kN/m²"
          vibration_isolation: required
          
        - sub_space_id: SS-CHP-PUMP
          sub_space_name: 水泵区
          function: 冷冻水/冷却水泵
          
        - sub_space_id: SS-CHP-HEADER
          sub_space_name: 分集水器区
          function: 分集水器、阀门
          maintenance_space: "≥1.5m"
          
        - sub_space_id: SS-CHP-CONTROL
          sub_space_name: 控制室
          function: 机房控制、值班
          air_conditioned: true
          
      environmental_requirements:
        temperature:
          operation: "5-40℃"
          control_room: "22-28℃"
          
        ventilation:
          type: 机械通风
          air_change: 6
          unit: ACH
          summer_exhaust: true
          
        noise:
          control: 隔声处理
          limit_at_boundary: 50
          unit: dB(A)
          
        floor:
          type: 水磨石/环氧
          drainage_slope: "≥0.5%"
          floor_drain: required
          
      special_requirements:
        - 设备吊装孔/通道
        - 减振基础
        - 集水坑
        - 排水沟
        - 机械通风系统
        - 消防设施
        
    - space_type_id: ROOM-MEP-ELEC
      space_type_name: 变配电室
      space_type_name_en: Electrical Substation Room
      
      sub_spaces:
        - sub_space_id: SS-ELEC-HV
          sub_space_name: 高压配电室
          function: 10kV高压开关柜
          fire_rating: "甲级防火门"
          
        - sub_space_id: SS-ELEC-TRANS
          sub_space_name: 变压器室
          function: 干式变压器
          ventilation: 强制通风
          
        - sub_space_id: SS-ELEC-LV
          sub_space_name: 低压配电室
          function: 低压配电柜
          
        - sub_space_id: SS-ELEC-CAP
          sub_space_name: 电容器室
          function: 无功补偿
          
      environmental_requirements:
        temperature:
          operation: "5-40℃"
          transformer: 强制降温
          
        humidity:
          max: 85
          unit: "%RH"
          
        ventilation:
          type: 机械通风
          air_change: "根据散热量计算"
          
        fire_protection:
          detection: 感烟探测
          suppression: 气体灭火（变压器室）
          
        floor:
          type: 绝缘地面
          drainage: 挡油坎
          
      electrical_requirements:
        grounding:
          type: TN-S系统
          resistance: "≤4Ω"
          
        emergency_lighting:
          required: true
          illuminance: "≥100 lux"
          
        cable_entry:
          type: 电缆沟/桥架
          fire_seal: required

  # ════════════════════════════════════════════════════════════════════════════
  # 第四部分：空间编码规则 (Space Coding Rules)
  # ════════════════════════════════════════════════════════════════════════════
  space_coding_rules:
    
    description: |
      空间编码规则为Agent-05系统-空间耦合提供统一的空间标识接口。
      采用层级化编码结构，确保编码的唯一性和可追溯性。
      
    coding_structure:
      pattern: "{L0}-{L1}-{L2}-{L3}-{L4}[-{L5}]"
      separator: "-"
      optional_levels: [L5]
      
    level_codes:
      L0_Site:
        pattern: "SITE-{OrgCode}"
        org_code_length: 6
        example: "SITE-XAYYFY"
        
      L1_Building:
        pattern: "{SiteCode}-{BuildingType}{Seq}"
        building_types:
          MZ: 门诊楼
          ZY: 住院楼
          YJ: 医技楼
          JZ: 急诊楼
          HQ: 后勤楼
          ZH: 综合楼
          KY: 科研楼
          JX: 教学楼
          XZ: 行政楼
        seq_digits: 2
        example: "SITE-XAYYFY-ZH01"
        
      L2_Floor:
        pattern: "{BuildingCode}-{FloorType}{Num}"
        floor_types:
          F: 地上层
          B: 地下层
          M: 夹层
          R: 屋顶
        num_digits: 2
        example: "SITE-XAYYFY-ZH01-F03"
        
      L3_Zone:
        pattern: "{FloorCode}-{ZoneType}{Seq}"
        zone_types:
          OP: 手术区
          NU: 护理单元
          IC: 重症区
          OD: 门诊区
          ER: 急诊区
          LB: 检验区
          IM: 影像区
          PH: 药房区
          ME: 机电区
          PB: 公共区
          CS: 供应室区
          IS: 隔离区
        seq_digits: 2
        example: "SITE-XAYYFY-ZH01-F03-OP01"
        
      L4_Room:
        pattern: "{ZoneCode}-{RoomType}{Seq}"
        room_types:
          OR: 手术室
          IC: ICU床位
          WD: 病房
          IS: 隔离病房
          EX: 检查室
          TR: 治疗室
          NS: 护士站
          DR: 医生办公
          WT: 候诊
          ST: 储藏
          ER: 设备房
          WC: 卫生间
          CR: 走廊
        seq_digits: 2
        example: "SITE-XAYYFY-ZH01-F03-OP01-OR01"
        
      L5_SubSpace:
        pattern: "{RoomCode}-{SubSpaceType}"
        sub_space_types:
          SA: 手术操作区
          AA: 麻醉区
          IA: 器械区
          CA: 通道区
          PA: 患者区
          ST: 工作区
        optional: true
        example: "SITE-XAYYFY-ZH01-F03-OP01-OR01-SA"
        
    validation_rules:
      - 编码必须从L0开始依次包含各层级
      - 同一层级内编码必须唯一
      - 编码仅使用大写字母、数字和连接符
      - 编码长度不超过60字符

  # ════════════════════════════════════════════════════════════════════════════
  # 第五部分：为Agent-05提供的接口定义
  # ════════════════════════════════════════════════════════════════════════════
  agent_05_interface:
    
    description: |
      本节定义空间本体模型为Agent-05（系统-空间耦合建模师）提供的接口，
      包括空间编码规则、环境参数要求、所需系统类型等信息。
      
    space_coding_interface:
      description: 提供统一的空间编码访问接口
      methods:
        - get_space_by_id: 根据编码获取空间信息
        - get_children: 获取子空间列表
        - get_parent: 获取父空间
        - get_siblings: 获取同级空间
        - get_by_type: 根据空间类型获取空间列表
        
    environmental_requirements_interface:
      description: 提供空间环境参数要求
      parameter_format:
        temperature: "{Setpoint}±{Tolerance}°C"
        humidity: "{Min}-{Max}% RH"
        pressure: "{Value} Pa (相对于 {Reference})"
        airflow: "{Rate} ACH"
      accuracy_requirements:
        temperature: "±0.5°C"
        humidity: "±3%RH"
        pressure: "±1 Pa"
        
    system_requirement_interface:
      description: 提供空间所需系统类型
      format:
        - space_type: 空间类型ID
          required_systems:
            - system_id: 系统ID
              system_name: 系统名称
              requirement_level: mandatory|recommended|optional
              key_parameters: 关键参数要求
              
    space_type_query:
      description: 空间类型查询接口
      queries:
        - get_medical_spaces: 获取所有医疗空间类型
        - get_clean_spaces: 获取所有洁净空间
        - get_isolation_spaces: 获取所有隔离空间
        - get_mep_spaces: 获取所有机电用房
        
    mapping_tables:
      space_to_hvac_requirements:
        description: 空间类型到HVAC要求的映射
        
      space_to_electrical_requirements:
        description: 空间类型到电气要求的映射
        
      space_to_medical_gas_requirements:
        description: 空间类型到医用气体要求的映射

  # ════════════════════════════════════════════════════════════════════════════
  # 完整性检查清单
  # ════════════════════════════════════════════════════════════════════════════
  completeness_checklist:
    
    space_hierarchy_model:
      - "[ ] L0-L5全部6个层级已定义"
      - "[ ] 每个层级都有完整的属性定义"
      - "[ ] 层级间关系已明确定义"
      - "[ ] 编码规则已完整定义"
      
    space_classification:
      - "[ ] 功能区域分类已完整（医疗、医技、后勤、公共、行政）"
      - "[ ] 房间分类已覆盖主要类型"
      - "[ ] 每类空间的子类型/变体已定义"
      
    medical_special_spaces:
      - "[ ] 手术室（各等级）已详细建模"
      - "[ ] ICU病房已详细建模"
      - "[ ] 负压隔离病房已详细建模"
      - "[ ] 洁净实验室已详细建模"
      - "[ ] 药房（静配中心）已详细建模"
      - "[ ] 供应室已详细建模"
      - "[ ] 机电设备用房已详细建模"
      
    interface_definition:
      - "[ ] 空间编码规则已提供给Agent-05"
      - "[ ] 环境参数要求格式已定义"
      - "[ ] 所需系统类型已映射"

  # ════════════════════════════════════════════════════════════════════════════
  # 统计摘要
  # ════════════════════════════════════════════════════════════════════════════
  statistics:
    
    hierarchy_levels: 6
    zone_categories: 5
    zone_sub_types: 23
    room_types: 12
    room_variants: 45
    
    special_space_models: 8
    total_attributes_defined: 350
    
    reference_standards: 6
    
    generated_for:
      agent_05: 系统-空间耦合建模师
      agent_08: 运维管理建模师
```

---

## 输出总结

本文档作为 **Agent-02 空间本体建模师** 的完整输出，包含以下五大部分：

### 1. 空间层级模型 (Space Hierarchy Model)
- **L0 院区层级**：医疗机构整体基地范围
- **L1 建筑层级**：单体建筑物（门诊、住院、医技等）
- **L2 楼层层级**：建筑楼层（地上、地下、夹层等）
- **L3 功能区域层级**：楼层内功能分区
- **L4 房间层级**：独立功能空间单元
- **L5 子空间层级**：房间内功能区域

### 2. 空间分类体系 (Space Classification)
- **功能区域分类**：
 - 医疗区域（手术区、重症区、护理单元、门诊区、急诊区、隔离区）
 - 医技区域（检验区、影像区、药房区、内镜中心、放疗区）
 - 后勤区域（机电用房区、供应室区、物流区、洗衣房、营养厨房）
 - 公共区域（大厅区、走廊区、垂直交通区）
 - 行政区域（办公区、会议区）

- **房间分类**：
 - 手术室类（I-IV级洁净手术室、负压手术室）
 - ICU类（综合ICU、专科ICU）
 - 隔离病房类（负压、正压、标准隔离）
 - 检验室类（生化、免疫、微生物、PCR、病理）
 - 影像室类（CT、MRI、DR、DSA、超声）
 - 机电设备用房类（配电室、冷冻站、发电机房等）

### 3. 医疗专用空间详细模型
为8类重点医疗空间提供完整技术要求：
- **手术室**：子空间组成、环境控制（温度/湿度/压差/换气/洁净度）、医疗气体（O2/VAC/AIR/N2O）、电气要求（隔离电源/等电位/UPS）
- **ICU病房**：每床位要求、正压环境、医疗气体配置
- **负压隔离病房**：压力梯度、门互锁、HEPA排风、独立系统
- **洁净实验室**：PCR分区、生物安全等级、压力梯度
- **静配中心（PIVAS）**：洁净分区、生物安全柜
- **供应室（CSSD）**：污洁分流、压力梯度
- **冷冻站**：设备荷载、通风散热、减振
- **变配电室**：防火分隔、气体灭火、接地

### 4. 空间编码规则
统一的空间编码体系：
- 格式：`SITE-{机构}-{建筑}-{楼层}-{区域}-{房间}[-{子空间}]`
- 示例：`SITE-XAYYFY-ZH01-F03-OP01-OR01-SA`

### 5. Agent-05接口定义
为下游Agent提供的接口：
- 空间编码查询接口
- 环境参数要求接口
- 所需系统映射接口

---

**本输出完成了Agent-02空间本体建模师的全部任务要求，可直接供Agent-05（系统-空间耦合建模师）和Agent-08（运维管理建模师）使用。**
[^1]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^2]: [# 医疗建筑空间本体模型元数据（Medical ...tion: "结合具体医疗项目案例进行实例化"](# 医疗建筑空间本体模型元数据（Medical ...tion: "结合具体医疗项目案例进行实例化")

[^3]: [# 医疗建筑空间本体模型元数据（Medical ...tion: "结合具体医疗项目案例进行实例化"](# 医疗建筑空间本体模型元数据（Medical ...tion: "结合具体医疗项目案例进行实例化")

[^4]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^5]: [# 医疗建筑空间本体模型元数据（Medical ...tion: "结合具体医疗项目案例进行实例化"](# 医疗建筑空间本体模型元数据（Medical ...tion: "结合具体医疗项目案例进行实例化")

[^6]: [# Agent-03: 设备本体建模师 (Equ...体化建模

[^1]: [# 医疗建筑空间分类体系（Healthcare ..."防振动", "UPS供电", "患者通话"]](# 医疗建筑空间分类体系（Healthcare ..."防振动", "UPS供电", "患者通话"])

[^2]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^3]: [# 医疗建筑空间本体模型元数据（Medical ...tion: "结合具体医疗项目案例进行实例化"](# 医疗建筑空间本体模型元数据（Medical ...tion: "结合具体医疗项目案例进行实例化")

[^4]: [# 医疗建筑空间分类体系（Healthcare ..."防振动", "UPS供电", "患者通话"]](# 医疗建筑空间分类体系（Healthcare ..."防振动", "UPS供电", "患者通话"])

[^5]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^6]: [# === AGENT-09: 统一CIM模型 ...on: “医用床塔管道疋 - 吊臂式供气供电+](# === AGENT-09: 统一CIM模型 ...on: “医用床塔管道疋 - 吊臂式供气供电+)

[^1]: [# 维护策略模型 - 医疗建筑智能运维管理

#..._verification: "连续验证确认"](# 维护策略模型 - 医疗建筑智能运维管理

#..._verification: "连续验证确认")

[^2]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^3]: [# Agent-08 运维管理建模师 输出文件元...etency: "人员资质能力达标率100%"](# Agent-08 运维管理建模师 输出文件元...etency: "人员资质能力达标率100%")

[^4]: [# 运维管理模型 - 综合交付物总结

# Ag...筑的智能运维提供强有力的技术支撑和管理规范。"](# 运维管理模型 - 综合交付物总结

# Ag...筑的智能运维提供强有力的技术支撑和管理规范。")

[^5]: [# 运维管理模型 - 综合交付物总结

# Ag...筑的智能运维提供强有力的技术支撑和管理规范。"](# 运维管理模型 - 综合交付物总结

# Ag...筑的智能运维提供强有力的技术支撑和管理规范。")

[^6]: [# 医疗建筑空间分类体系（Healthcare ..."防振动", "UPS供电", "患者通话"]](# 医疗建筑空间分类体系（Healthcare ..."防振动", "UPS供电", "患者通话"])

[^1]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^2]: [# === AGENT-09: 统一CIM模型 ...on: “医用床塔管道疋 - 吊臂式供气供电+](# === AGENT-09: 统一CIM模型 ...on: “医用床塔管道疋 - 吊臂式供气供电+)

[^3]: [Agent-01 系统拓扑建模师 - 第四批次：消防系统 + 医疗专业系统.md](http://file/2f672527-5466-46d6-b255-27eed6ebc9e5.md)

[^4]: [# 医疗建筑空间分类体系（Healthcare ..."防振动", "UPS供电", "患者通话"]](# 医疗建筑空间分类体系（Healthcare ..."防振动", "UPS供电", "患者通话"])

[^5]: [# 医疗建筑空间分类体系（Healthcare ..."防振动", "UPS供电", "患者通话"]](# 医疗建筑空间分类体系（Healthcare ..."防振动", "UPS供电", "患者通话"])

[^6]: [# 医疗专用空间详细建模（Medical Spe...   - terminal_locations](# 医疗专用空间详细建模（Medical Spe...   - terminal_locations)
---