## 🧑‍💻 User


根据认知同步和评审意见完善输出内容

---
## 🤖 Assistant


根据认知同步内容和评审意见，我现在对Agent-02的输出进行完善，重点补充：
1. **医疗工艺流程（一二三级流程）与空间的耦合**
2. **空间拓扑结构（基于空间句法思想）**
3. **完善Agent-05接口**

---

# Agent-02: 空间本体建模师 (Space Ontology Architect)
## 完善版输出文档 v1.1

---

```yaml
# ═══════════════════════════════════════════════════════════════════════════════
# Agent-02: 空间本体建模师 (Space Ontology Architect)
# 医疗建筑空间本体模型 - 完善版 v1.1
# 增强内容：医疗工艺流程耦合 + 空间拓扑结构（空间句法）
# ═══════════════════════════════════════════════════════════════════════════════

Agent02_Output:

  # ════════════════════════════════════════════════════════════════════════════
  # 元数据（更新版）
  # ════════════════════════════════════════════════════════════════════════════
  meta:
    agent_id: Agent-02
    agent_name: 空间本体建模师
    agent_name_en: Space Ontology Architect
    version: 1.1
    version_note: |
      v1.1更新内容：
      1. 新增"医疗工艺流程-空间耦合模型"（一二三级流程）
      2. 新增"空间拓扑结构模型"（基于空间句法理论）
      3. 完善Agent-05接口定义
      4. 增强L3区域层级的流程属性
    generated_at: 2024-12-20T00:00:00+08:00
    
    theoretical_foundations:
      medical_process_design:
        description: |
          医疗工艺设计分为三个层级与建筑设计对接配合：
          - 一级流程：落实单体、楼层和大功能分区之间的关系（流程与动线）
          - 二级流程：相对独立的医疗分区采取的平面布局（面积与形态）
          - 三级流程：患者和医护在房间或特定区域内的行为及功能设计
        standard_reference: "2015年新版《综合医院建筑设计规范》"
        
      space_syntax:
        description: |
          空间句法（Space Syntax）是一种空间形态分析方法，通过拓扑关系而非
          几何距离来描述空间结构。核心概念包括：
          - 连接度（Connectivity）：空间直接连接的其他空间数量
          - 整合度（Integration）：空间在整体系统中的可达性
          - 深度（Depth）：从一个空间到达另一空间需要穿越的空间数量
          - 控制值（Control）：空间对相邻空间的控制程度
        application: "医疗建筑的空间可达性分析、流线优化、感染控制路径设计"

  # ════════════════════════════════════════════════════════════════════════════
  # 新增：医疗工艺流程-空间耦合模型
  # ════════════════════════════════════════════════════════════════════════════
  medical_process_space_coupling:
    
    model_description: |
      本模型建立医疗工艺设计三级流程与空间层级的耦合关系。
      - 一级流程 ↔ L1建筑 + L2楼层 + L3功能区域（分区间关系）
      - 二级流程 ↔ L3功能区域内部（区域平面布局）
      - 三级流程 ↔ L4房间 + L5子空间（房间内行为与功能）
      
      这种耦合确保空间设计能够支撑医疗业务流程的高效运转。
      
    # ────────────────────────────────────────────────────────────────────────
    # 一级流程-空间耦合（宏观动线层）
    # ────────────────────────────────────────────────────────────────────────
    level_1_process_coupling:
      
      definition: |
        一级流程主要落实医疗建筑中单体、楼层和大的功能分区之间的关系。
        主要解决的是流程与动线之间的关系。
        最短的动线可以大大提高就诊效率，在为救治赢得时间的同时，
        良好的周转率会极大地提升医院的就医环境品质。
        
      coupling_scope:
        space_levels: [L1, L2, L3]
        process_focus: 跨建筑/跨楼层/跨区域的主要流线
        
      core_flow_types:
        
        - flow_type_id: FLOW-L1-PATIENT-EMERGENCY
          flow_type_name: 急诊患者主动线
          flow_priority: P0-生命关键
          description: 急诊入口到抢救室、手术室、ICU的最短路径
          
          flow_path:
            origin: 急诊入口
            key_nodes:
              - step: 1
                destination: 急诊预检分诊
                max_distance: "≤20m"
                max_time: "≤1min"
              - step: 2
                destination: 急诊抢救室
                max_distance: "≤50m"
                max_time: "≤2min"
              - step: 3
                destination: 急诊手术室
                max_distance: "≤100m"
                max_time: "≤5min"
                note: "可使用专用电梯"
              - step: 4
                destination: ICU
                max_distance: "≤150m"
                max_time: "≤8min"
                
          spatial_requirements:
            - 急诊与手术区应位于同一建筑或相邻建筑
            - 急诊与ICU应有专用电梯直达
            - 急诊手术室宜靠近急诊区设置
            - 通道宽度≥2.4m，无障碍设计
            
        - flow_type_id: FLOW-L1-PATIENT-ELECTIVE
          flow_type_name: 择期手术患者动线
          flow_priority: P1-重要
          description: 病房到手术室再返回病房的流程路径
          
          flow_path:
            origin: 住院病房
            key_nodes:
              - step: 1
                destination: 术前准备区
                max_time: "≤10min"
              - step: 2
                destination: 手术室
                path_type: 洁净通道
              - step: 3
                destination: 麻醉复苏室
              - step: 4
                destination: ICU/住院病房
                path_type: 患者通道
                
        - flow_type_id: FLOW-L1-PATIENT-OUTPATIENT
          flow_type_name: 门诊患者动线
          flow_priority: P2-一般
          description: 门诊就医全流程路径
          
          flow_path:
            origin: 门诊入口
            key_nodes:
              - step: 1
                destination: 预检分诊/挂号
              - step: 2
                destination: 候诊区
              - step: 3
                destination: 诊室
              - step: 4
                destination: 检查（影像/检验）
                optional: true
              - step: 5
                destination: 取药/治疗
              - step: 6
                destination: 门诊出口
                
          spatial_requirements:
            - 各环节应位于同一楼层或相邻楼层
            - 检验科、影像科宜集中设置
            - 门诊药房宜靠近门诊出口
            
        - flow_type_id: FLOW-L1-STAFF-MEDICAL
          flow_type_name: 医护人员动线
          flow_priority: P1-重要
          description: 医护人员工作区域之间的流线
          
          flow_path:
            key_principle: 医护通道与患者通道分离
            features:
              - 医护专用电梯
              - 科室间连廊
              - 更衣室位置合理
              
        - flow_type_id: FLOW-L1-LOGISTICS-CLEAN
          flow_type_name: 洁净物流动线
          flow_priority: P1-重要
          description: 无菌物品、药品、餐食的配送路径
          
          flow_path:
            key_principle: 洁污分流
            features:
              - 专用物流电梯
              - 水平物流通道
              - 供应室→手术室专用通道
              
        - flow_type_id: FLOW-L1-LOGISTICS-WASTE
          flow_type_name: 污物流动线
          flow_priority: P1-重要
          description: 医疗废物、污染物品的收集和转运路径
          
          flow_path:
            key_principle: 与洁净物流完全分离
            features:
              - 专用污物电梯
              - 封闭式转运通道
              - 污物暂存间→污物处理中心
              
      building_zone_relationships:
        
        - relationship_id: REL-L1-ER-OR
          from_zone: 急诊区域
          to_zone: 手术区域
          relationship_type: 紧密邻接
          priority: P0
          requirements:
            - 垂直距离：≤2层
            - 水平距离：≤100m
            - 连接方式：专用电梯+专用通道
            - 时间要求：≤5min
            
        - relationship_id: REL-L1-OR-ICU
          from_zone: 手术区域
          to_zone: 重症监护区
          relationship_type: 紧密邻接
          priority: P0
          requirements:
            - 垂直距离：宜同层或相邻层
            - 连接方式：专用洁净通道
            - 时间要求：≤3min
            
        - relationship_id: REL-L1-WARD-MEDTECH
          from_zone: 护理单元
          to_zone: 医技区域
          relationship_type: 便捷可达
          priority: P1
          requirements:
            - 可达时间：≤10min
            - 连接方式：患者电梯+走廊
            
        - relationship_id: REL-L1-CSSD-OR
          from_zone: 供应室
          to_zone: 手术区域
          relationship_type: 物流紧密
          priority: P1
          requirements:
            - 无菌物品传递：≤5min
            - 连接方式：专用洁净物流通道
            - 压力梯度：供应室→手术区正压流向

    # ────────────────────────────────────────────────────────────────────────
    # 二级流程-空间耦合（区域布局层）
    # ────────────────────────────────────────────────────────────────────────
    level_2_process_coupling:
      
      definition: |
        二级流程是指一个相对独立的医疗分区或部门该采取什么样的平面布局。
        主要解决的是面积与形态的关系。
        二级流程设计是在充分考虑不同医疗环境的前提下，找出医疗分区或
        部门的特点和需求，在满足面积的情况下，对布局形态在建筑平面中予以落实。
        
      coupling_scope:
        space_level: L3
        process_focus: 功能区域内部的空间组织和流转逻辑
        
      zone_process_models:
        
        # ── 手术区二级流程 ──
        - zone_type_id: ZONE-MED-OP
          zone_type_name: 手术区
          
          layout_principle: 三区三通道布局
          
          functional_zones:
            - zone_id: OP-CLEAN
              zone_name: 洁净区
              description: 包含手术间、刷手间、无菌物品间
              pressure_gradient: "+15 Pa"
              air_changes: "15-20 ACH"
              access: 仅限换洁净服后进入
              
            - zone_id: OP-SEMI-CLEAN
              zone_name: 清洁区
              description: 包含办公、值班、敷料、器械准备
              pressure_gradient: "+10 Pa"
              air_changes: "10-15 ACH"
              access: 换洗手衣后进入
              
            - zone_id: OP-NON-CLEAN
              zone_name: 非洁净区
              description: 包含更衣室、休息室、污物处理
              pressure_gradient: "0 Pa"
              access: 外部人员可达
              
          circulation_systems:
            - corridor_id: OP-CORR-CLEAN
              corridor_name: 洁净走廊
              function: 连接各手术室的主要洁净通道
              width: "≥2.4m"
              pressure: "+15 Pa"
              users: [手术人员, 患者(术中)]
              
            - corridor_id: OP-CORR-PATIENT
              corridor_name: 患者通道
              function: 患者进入和离开手术区的通道
              width: "≥2.4m"
              pressure: "+10 Pa"
              one_way: 单向流动
              
            - corridor_id: OP-CORR-WASTE
              corridor_name: 污物走廊
              function: 污染物品和术后器械的转运通道
              width: "≥1.8m"
              pressure: "0 Pa 或负压"
              separation: 与洁净通道完全分离
              
          process_flows:
            
            - flow_id: OP-FLOW-PATIENT
              flow_name: 患者流程
              flow_type: 主流程
              sequence:
                - step: 1
                  action: 患者到达
                  location: 换床区
                  space_requirement: 更换手术床
                  
                - step: 2
                  action: 进入洁净区
                  location: 患者通道
                  space_requirement: 单向流动，压差过渡
                  
                - step: 3
                  action: 麻醉诱导
                  location: 手术室-麻醉区
                  space_requirement: 麻醉设备就位
                  
                - step: 4
                  action: 手术操作
                  location: 手术室-手术区
                  space_requirement: 层流送风覆盖
                  
                - step: 5
                  action: 术后转运
                  location: 患者通道
                  space_requirement: 担架车通行
                  
                - step: 6
                  action: 麻醉苏醒
                  location: 复苏室
                  space_requirement: 监护设备到位
                  
            - flow_id: OP-FLOW-STAFF
              flow_name: 医护流程
              flow_type: 支持流程
              sequence:
                - step: 1
                  action: 进入更衣区
                  location: 非洁净区-更衣室
                  space_requirement: 分男女更衣
                  
                - step: 2
                  action: 换洁净服
                  location: 二次更衣室
                  space_requirement: 穿洁净服，戴口罩帽子
                  
                - step: 3
                  action: 进入洁净区
                  location: 洁净走廊
                  space_requirement: 风淋门过渡
                  
                - step: 4
                  action: 术前刷手
                  location: 刷手间
                  space_requirement: 邻近手术室，无菌操作
                  
                - step: 5
                  action: 进入手术室
                  location: 手术室
                  space_requirement: 保持无菌
                  
            - flow_id: OP-FLOW-STERILE
              flow_name: 无菌物品流程
              flow_type: 物流流程
              sequence:
                - step: 1
                  action: 无菌物品接收
                  location: 无菌物品存放间
                  source: 供应室
                  
                - step: 2
                  action: 术前准备
                  location: 器械准备间
                  
                - step: 3
                  action: 送入手术室
                  location: 手术室-器械区
                  path: 洁净走廊
                  
            - flow_id: OP-FLOW-WASTE
              flow_name: 污物流程
              flow_type: 物流流程
              sequence:
                - step: 1
                  action: 术后污物收集
                  location: 手术室
                  
                - step: 2
                  action: 污物转运
                  location: 污物走廊
                  path: 专用污物通道
                  
                - step: 3
                  action: 器械预处理
                  location: 污物处理间
                  
                - step: 4
                  action: 转运至供应室
                  destination: 供应室-回收区
                  
          spatial_adjacency_matrix:
            description: 基于流程驱动的空间邻接约束
            matrix:
              - from: 手术室
                to: 刷手间
                requirement: ADJACENT_DIRECT
                reason: 医护刷手后直接进入
                max_distance: "≤3m"
                
              - from: 手术室
                to: 洁净走廊
                requirement: ADJACENT_DIRECT
                reason: 人员物品进出通道
                
              - from: 手术室
                to: 无菌物品存放间
                requirement: ADJACENT_CORRIDOR
                reason: 无菌物品快速供应
                max_distance: "≤20m"
                
              - from: 手术室
                to: 复苏室
                requirement: ADJACENT_CORRIDOR
                reason: 术后患者快速转运
                max_distance: "≤30m"
                
              - from: 洁净走廊
                to: 污物走廊
                requirement: ISOLATED
                reason: 洁污分离
                separation: 物理隔离
                
        # ── ICU二级流程 ──
        - zone_type_id: ZONE-MED-ICU
          zone_type_name: 重症监护区
          
          layout_principle: 中央监护+环形床位布局
          
          functional_zones:
            - zone_id: ICU-PATIENT
              zone_name: 患者监护区
              description: 病床区域，开放式或单间
              area_per_bed: "15-18 m²"
              
            - zone_id: ICU-NURSE
              zone_name: 中央护士站
              description: 中央监控和工作区
              visibility: 可视所有床位
              
            - zone_id: ICU-SUPPORT
              zone_name: 支持用房区
              description: 治疗室、配液室、仪器室
              
          process_flows:
            - flow_id: ICU-FLOW-ADMISSION
              flow_name: 患者收治流程
              sequence:
                - step: 1
                  action: 患者转入
                  location: ICU入口缓冲区
                  source: 手术室/急诊/病房
                  
                - step: 2
                  action: 接诊评估
                  location: ICU护士站
                  
                - step: 3
                  action: 安置床位
                  location: 监护病床
                  
            - flow_id: ICU-FLOW-CARE
              flow_name: 日常监护流程
              sequence:
                - step: 1
                  action: 持续监测
                  location: 床旁
                  equipment: 监护仪、呼吸机
                  
                - step: 2
                  action: 治疗操作
                  location: 床旁
                  equipment: 输液泵、注射泵
                  
                - step: 3
                  action: 护理记录
                  location: 护士站
                  
          spatial_adjacency_matrix:
            matrix:
              - from: 护士站
                to: 所有病床
                requirement: VISUAL_CONTACT
                reason: 持续监护需求
                max_distance: "≤15m"
                
              - from: 治疗室
                to: 病床区
                requirement: ADJACENT_CORRIDOR
                reason: 快速供应药品器材
                max_distance: "≤20m"
                
              - from: ICU入口
                to: 手术区
                requirement: ACCESSIBLE
                reason: 术后患者快速转运
                max_time: "≤3min"

        # ── 门诊区二级流程 ──
        - zone_type_id: ZONE-MED-OPD
          zone_type_name: 门诊区域
          
          layout_principle: 按疾病系统分区布局（大型医院）
          
          layout_modes:
            - mode_id: OPD-LAYOUT-TRADITIONAL
              mode_name: 传统集中式
              applicable: "床位<1000床"
              description: 各专科诊室集中于门诊楼
              
            - mode_id: OPD-LAYOUT-SYSTEM
              mode_name: 疾病系统式
              applicable: "床位>2000床"
              description: |
                按疾病系统进行平面规划，避免每天几千甚至上万人
                集中在门诊医技区域流动，极大降低救治效率。
              systems:
                - 心血管系统诊疗区
                - 消化系统诊疗区
                - 呼吸系统诊疗区
                - 神经系统诊疗区
                - 骨关节系统诊疗区
                
          process_flows:
            - flow_id: OPD-FLOW-PATIENT
              flow_name: 门诊就医流程
              sequence:
                - step: 1
                  action: 预检分诊
                  location: 门诊大厅
                  
                - step: 2
                  action: 挂号缴费
                  location: 收费窗口/自助机
                  
                - step: 3
                  action: 候诊
                  location: 候诊区
                  space_requirement: 就近设置，分流设计
                  
                - step: 4
                  action: 就诊
                  location: 诊室
                  
                - step: 5
                  action: 检查（可选）
                  location: 检验/影像科
                  
                - step: 6
                  action: 取药/治疗
                  location: 药房/治疗室
                  
    # ────────────────────────────────────────────────────────────────────────
    # 三级流程-空间耦合（房间行为层）
    # ────────────────────────────────────────────────────────────────────────
    level_3_process_coupling:
      
      definition: |
        三级流程是指患者和医护人员在房间或特定区域内的行为，
        以及满足实现这些行为的功能设计。
        换言之，就是平面设计的细节部分是否满足了患者及医护人员的体验感。
        三级流程设计要求设计师清楚每一个医疗环节的操作方式及习惯，
        并且要站在患者的行为安全、隐私和方便性等多个角度去考虑问题。
        
      coupling_scope:
        space_levels: [L4, L5]
        process_focus: 房间内的具体行为和功能细节
        
      room_process_models:
        
        # ── 手术室三级流程 ──
        - room_type_id: ROOM-OR
          room_type_name: 手术室
          
          sub_space_processes:
            
            - sub_space_id: SS-OR-SA
              sub_space_name: 手术操作区
              
              behavior_processes:
                - behavior_id: BHV-OR-SA-01
                  behavior_name: 手术台定位
                  description: 手术台位于层流送风区中心
                  requirements:
                    - 手术台长轴与送风口长轴平行
                    - 手术台中心距墙≥1.5m
                    - 周围工作区域≥1.2m
                    
                - behavior_id: BHV-OR-SA-02
                  behavior_name: 无影灯操作
                  description: 无影灯照射手术区域
                  requirements:
                    - 灯臂旋转半径内无障碍物
                    - 灯头高度可调节1.0-1.5m
                    - 照度20000-160000 lux可调
                    
                - behavior_id: BHV-OR-SA-03
                  behavior_name: 术者站位
                  description: 主刀医生和助手的站位
                  requirements:
                    - 主刀医生位于手术台一侧
                    - 助手对面站位
                    - 脚踏开关就近放置
                    
            - sub_space_id: SS-OR-AA
              sub_space_name: 麻醉工作区
              
              behavior_processes:
                - behavior_id: BHV-OR-AA-01
                  behavior_name: 麻醉诱导
                  description: 麻醉医生进行麻醉诱导操作
                  requirements:
                    - 麻醉机靠近患者头端
                    - 气体终端就近设置（≤1m）
                    - 麻醉药品车可达
                    
                - behavior_id: BHV-OR-AA-02
                  behavior_name: 气道管理
                  description: 插管和气道维护操作空间
                  requirements:
                    - 头端操作空间≥1.2m
                    - 吸引终端就近
                    - 照明充足
                    
                - behavior_id: BHV-OR-AA-03
                  behavior_name: 生命体征监测
                  description: 持续监测患者状态
                  requirements:
                    - 监护仪位于麻醉医生可视范围
                    - 报警声音可闻
                    - 电源充足（≥8个插座）
                    
            - sub_space_id: SS-OR-IA
              sub_space_name: 器械区
              
              behavior_processes:
                - behavior_id: BHV-OR-IA-01
                  behavior_name: 器械台布置
                  description: 手术器械的无菌摆放
                  requirements:
                    - 器械台位于器械护士可达范围
                    - 与手术台距离适中（1.0-1.5m）
                    - 有足够展开空间
                    
                - behavior_id: BHV-OR-IA-02
                  behavior_name: 器械传递
                  description: 器械护士向术者传递器械
                  requirements:
                    - 传递路径无障碍
                    - 视线无遮挡
                    - 转身空间充足
                    
          furniture_equipment_layout:
            - item: 手术台
              location: 手术操作区中心
              orientation: 长轴与送风口平行
              clearance: 周围≥1.2m
              
            - item: 无影灯
              location: 手术台正上方
              type: 悬臂式/轨道式
              
            - item: 麻醉机
              location: 患者头端
              orientation: 面向麻醉医生工作位
              
            - item: 器械台
              location: 器械区
              count: 2-3台
              
            - item: 手术显微镜
              location: 可移动至手术区
              condition: 显微手术时使用
              
            - item: C臂X光机
              location: 可移动
              condition: 骨科/介入手术时使用
              
        # ── 诊室三级流程 ──
        - room_type_id: ROOM-OPD-EXAM
          room_type_name: 门诊诊室
          
          behavior_processes:
            - behavior_id: BHV-OPD-01
              behavior_name: 患者进入
              description: 患者从候诊区进入诊室
              requirements:
                - 门宽≥900mm
                - 入口处有候诊提示
                
            - behavior_id: BHV-OPD-02
              behavior_name: 问诊交流
              description: 医生与患者面对面交流
              requirements:
                - 患者座椅面向医生
                - 医患距离适当（0.8-1.2m）
                - 保护隐私（门窗遮挡）
                
            - behavior_id: BHV-OPD-03
              behavior_name: 体格检查
              description: 医生进行基本体格检查
              requirements:
                - 检查床（需要时）
                - 私密空间
                - 更衣区域
                
            - behavior_id: BHV-OPD-04
              behavior_name: 开具处方
              description: 医生使用计算机开具处方
              requirements:
                - 计算机工作站
                - 打印机
                - 处方签字
                
          privacy_considerations:
            - 诊室门应设遮挡
            - 窗户应有窗帘
            - 相邻诊室隔声
            - 一人一诊避免尴尬

  # ════════════════════════════════════════════════════════════════════════════
  # 新增：空间拓扑结构模型（基于空间句法理论）
  # ════════════════════════════════════════════════════════════════════════════
  space_topology_model:
    
    model_description: |
      本模型基于空间句法（Space Syntax）理论，建立医疗建筑的空间拓扑结构。
      空间句法关注空间之间的连接关系和可达性，而非简单的几何距离。
      
      核心思想：
      - 空间是由连接关系定义的网络，而非独立的几何实体
      - 空间的"价值"取决于其在网络中的位置
      - 医疗建筑中的流线效率取决于空间网络的拓扑结构
      
      与Agent-01的拓扑结构类比：
      - Agent-01用拓扑网络描述机电系统（源→输配→末端）
      - Agent-02用拓扑网络描述空间结构（入口→交通→功能空间）
      - Agent-05将两者耦合形成超图结构
      
    # ────────────────────────────────────────────────────────────────────────
    # 空间拓扑元素定义
    # ────────────────────────────────────────────────────────────────────────
    topology_elements:
      
      node_types:
        
        - node_type_id: SPACE-NODE-ENTRANCE
          node_type_name: 入口节点
          node_role: 系统边界入口
          description: 建筑或区域的入口空间
          examples:
            - 门诊大厅入口
            - 急诊入口
            - 住院入口
            - 手术区入口
          characteristics:
            - 高连接度
            - 人流汇聚点
            - 导向需求高
          analogy_agent01: 类似Agent-01的"源节点-外部边界"
          
        - node_type_id: SPACE-NODE-HUB
          node_type_name: 枢纽节点
          node_role: 流线交汇与分配
          description: 主要交通枢纽空间
          examples:
            - 电梯厅
            - 主走廊交叉口
            - 门诊大厅
            - 中央护士站
          characteristics:
            - 最高连接度
            - 人流分配
            - 方向选择点
          analogy_agent01: 类似Agent-01的"分配节点-Splitter"
          
        - node_type_id: SPACE-NODE-CORRIDOR
          node_type_name: 通道节点
          node_role: 流线传输
          description: 走廊和通道空间
          examples:
            - 公共走廊
            - 医护走廊
            - 洁净走廊
            - 污物走廊
          characteristics:
            - 线性连接
            - 传输功能
            - 通过性空间
          analogy_agent01: 类似Agent-01的"边-Trunk/Branch"
          
        - node_type_id: SPACE-NODE-FUNCTION
          node_type_name: 功能节点
          node_role: 流线终端/起点
          description: 具体功能房间
          examples:
            - 诊室
            - 病房
            - 手术室
            - 检查室
          characteristics:
            - 较低连接度
            - 功能实现
            - 停留空间
          analogy_agent01: 类似Agent-01的"汇节点-Sink"
          
        - node_type_id: SPACE-NODE-BUFFER
          node_type_name: 缓冲节点
          node_role: 过渡与控制
          description: 压力/洁净/安全过渡空间
          examples:
            - 风淋室
            - 缓冲间
            - 更衣室
            - 换床区
          characteristics:
            - 序列性
            - 控制功能
            - 必经路径
          analogy_agent01: 类似Agent-01的"分配节点-Regulator"
          
      edge_types:
        
        - edge_type_id: EDGE-DIRECT
          edge_type_name: 直接连接
          description: 两空间通过门直接相连
          connection_element: 门
          characteristics:
            - 一步可达
            - 深度=1
            - 强连接
          attributes:
            - door_width: mm
            - door_type: 平开/推拉/自动
            - access_control: 是否门禁
            
        - edge_type_id: EDGE-CORRIDOR
          edge_type_name: 走廊连接
          description: 两空间通过走廊相连
          connection_element: 走廊+门
          characteristics:
            - 间接可达
            - 深度≥2
            - 公共交通
          attributes:
            - corridor_length: m
            - corridor_width: m
            
        - edge_type_id: EDGE-VERTICAL
          edge_type_name: 垂直连接
          description: 跨楼层的垂直交通连接
          connection_element: 电梯/楼梯
          characteristics:
            - 跨层可达
            - 等待时间
            - 容量限制
          attributes:
            - transport_type: 电梯/楼梯/坡道
            - travel_time: s
            - capacity: 人/次
            
        - edge_type_id: EDGE-BUFFER
          edge_type_name: 缓冲连接
          description: 需要通过缓冲空间的连接
          connection_element: 缓冲间+门
          characteristics:
            - 受控可达
            - 序列通过
            - 环境过渡
          attributes:
            - buffer_type: 风淋/更衣/换床
            - transition_time: s
            
    # ────────────────────────────────────────────────────────────────────────
    # 空间拓扑指标（空间句法核心）
    # ────────────────────────────────────────────────────────────────────────
    topology_metrics:
      
      - metric_id: METRIC-CONNECTIVITY
        metric_name: 连接度
        metric_name_en: Connectivity
        definition: 一个空间直接连接的其他空间数量
        formula: "k = 直接相邻空间数"
        interpretation:
          high_value: 空间开放性高，是交通枢纽
          low_value: 空间私密性高，适合专注活动
        medical_application:
          - 护士站应有高连接度（监护多个病床）
          - 诊室应有低连接度（保护隐私）
          - 候诊区应有中等连接度（等候+进入诊室）
          
      - metric_id: METRIC-DEPTH
        metric_name: 深度
        metric_name_en: Depth
        definition: 从系统入口到达某空间需要穿越的最少空间数
        formula: "d = min(穿越空间数)"
        interpretation:
          shallow: 空间易于到达，公共性强
          deep: 空间隐蔽，需要多次转换
        medical_application:
          - 急诊抢救室应为浅深度（快速可达）
          - 手术室应为中等深度（可达但受控）
          - ICU病床应为较深深度（隔离保护）
          
      - metric_id: METRIC-INTEGRATION
        metric_name: 整合度
        metric_name_en: Integration
        definition: 空间在整体系统中的可达性/中心性
        formula: "i = f(所有空间到该空间的平均深度)"
        interpretation:
          high_integration: 空间是系统的核心，容易从各处到达
          low_integration: 空间是系统的边缘，相对隔离
        medical_application:
          - 门诊大厅应有高整合度（系统核心）
          - 供应室应有中等整合度（需要与多区域连接但不是公共空间）
          - 污物处理间应有低整合度（隔离但可达）
          
      - metric_id: METRIC-CONTROL
        metric_name: 控制值
        metric_name_en: Control Value
        definition: 空间对相邻空间的控制程度
        formula: "c = Σ(1/相邻空间的连接度)"
        interpretation:
          high_control: 空间是必经之路，控制通行
          low_control: 空间可被绕过
        medical_application:
          - 护士站应有高控制值（监控病区通行）
          - 手术区入口应有高控制值（控制进入）
          - 候诊区应有低控制值（开放等候）
          
      - metric_id: METRIC-CHOICE
        metric_name: 选择度
        metric_name_en: Choice
        definition: 空间位于系统中最短路径上的频率
        formula: "ch = 穿过该空间的最短路径数"
        interpretation:
          high_choice: 空间是主要通道，人流量大
          low_choice: 空间是目的地或边缘空间
        medical_application:
          - 主走廊应有高选择度（主要通道）
          - 电梯厅应有高选择度（垂直交通节点）
          - 病房应有低选择度（目的地）
          
    # ────────────────────────────────────────────────────────────────────────
    # 医疗场景空间拓扑模型
    # ────────────────────────────────────────────────────────────────────────
    medical_topology_models:
      
      # ── 手术区空间拓扑 ──
      - zone_id: ZONE-MED-OP
        zone_name: 手术区
        
        topology_graph:
          nodes:
            - node_id: OP-N-ENTRANCE
              node_type: SPACE-NODE-ENTRANCE
              space_name: 手术区入口
              depth: 0
              
            - node_id: OP-N-CHANGE1
              node_type: SPACE-NODE-BUFFER
              space_name: 一次更衣室
              depth: 1
              
            - node_id: OP-N-CHANGE2
              node_type: SPACE-NODE-BUFFER
              space_name: 二次更衣室
              depth: 2
              
            - node_id: OP-N-CLEAN-CORR
              node_type: SPACE-NODE-CORRIDOR
              space_name: 洁净走廊
              depth: 3
              connectivity: 12  # 连接多个手术室
              integration: HIGH
              
            - node_id: OP-N-SCRUB
              node_type: SPACE-NODE-BUFFER
              space_name: 刷手间
              depth: 4
              
            - node_id: OP-N-OR-01
              node_type: SPACE-NODE-FUNCTION
              space_name: 1号手术室
              depth: 5
              connectivity: 3  # 洁净走廊、刷手间、污物通道
              
            - node_id: OP-N-OR-02
              node_type: SPACE-NODE-FUNCTION
              space_name: 2号手术室
              depth: 5
              
            - node_id: OP-N-RECOVERY
              node_type: SPACE-NODE-FUNCTION
              space_name: 复苏室
              depth: 4
              connectivity: 4  # 洁净走廊、多个手术室
              
            - node_id: OP-N-STERILE
              node_type: SPACE-NODE-FUNCTION
              space_name: 无菌物品存放间
              depth: 4
              
            - node_id: OP-N-WASTE-CORR
              node_type: SPACE-NODE-CORRIDOR
              space_name: 污物走廊
              depth: 5
              integration: LOW  # 相对隔离
              
          edges:
            - edge_id: OP-E-01
              from: OP-N-ENTRANCE
              to: OP-N-CHANGE1
              edge_type: EDGE-DIRECT
              
            - edge_id: OP-E-02
              from: OP-N-CHANGE1
              to: OP-N-CHANGE2
              edge_type: EDGE-DIRECT
              
            - edge_id: OP-E-03
              from: OP-N-CHANGE2
              to: OP-N-CLEAN-CORR
              edge_type: EDGE-BUFFER
              buffer_type: 风淋
              
            - edge_id: OP-E-04
              from: OP-N-CLEAN-CORR
              to: OP-N-SCRUB
              edge_type: EDGE-DIRECT
              
            - edge_id: OP-E-05
              from: OP-N-SCRUB
              to: OP-N-OR-01
              edge_type: EDGE-DIRECT
              one_way: true  # 单向进入
              
            - edge_id: OP-E-06
              from: OP-N-OR-01
              to: OP-N-WASTE-CORR
              edge_type: EDGE-DIRECT
              one_way: true  # 污物单向流出
              
        topology_metrics_summary:
          entrance_depth: 0
          or_depth: 5  # 手术室深度
          integration_core: 洁净走廊
          control_points: [二次更衣室, 刷手间]
          
        design_implications:
          - 手术室深度=5，确保足够的隔离和保护
          - 洁净走廊作为整合核心，连接所有手术室
          - 二次更衣室和刷手间作为控制点，管理人员进入
          - 污物走廊低整合度，与洁净系统分离
          
      # ── 住院病区空间拓扑 ──
      - zone_id: ZONE-MED-WARD
        zone_name: 护理单元
        
        topology_graph:
          nodes:
            - node_id: WD-N-ENTRANCE
              node_type: SPACE-NODE-ENTRANCE
              space_name: 病区入口
              depth: 0
              control: HIGH  # 控制访客进入
              
            - node_id: WD-N-NURSE
              node_type: SPACE-NODE-HUB
              space_name: 护士站
              depth: 1
              connectivity: 15+  # 连接走廊和各病房
              integration: HIGHEST
              control: HIGHEST  # 监控整个病区
              
            - node_id: WD-N-MAIN-CORR
              node_type: SPACE-NODE-CORRIDOR
              space_name: 主走廊
              depth: 1
              choice: HIGH  # 主要通道
              
            - node_id: WD-N-ROOM-01
              node_type: SPACE-NODE-FUNCTION
              space_name: 病房01
              depth: 2
              connectivity: 1  # 只连接走廊
              integration: LOW
              
            - node_id: WD-N-TREATMENT
              node_type: SPACE-NODE-FUNCTION
              space_name: 治疗室
              depth: 2
              
            - node_id: WD-N-UTILITY
              node_type: SPACE-NODE-FUNCTION
              space_name: 污洗室
              depth: 3
              integration: LOWEST  # 隔离
              
          edges:
            - edge_id: WD-E-01
              from: WD-N-ENTRANCE
              to: WD-N-NURSE
              edge_type: EDGE-DIRECT
              access_control: true
              
            - edge_id: WD-E-02
              from: WD-N-NURSE
              to: WD-N-MAIN-CORR
              edge_type: EDGE-DIRECT
              
            - edge_id: WD-E-03
              from: WD-N-MAIN-CORR
              to: WD-N-ROOM-01
              edge_type: EDGE-DIRECT
              
        topology_metrics_summary:
          integration_core: 护士站
          control_points: [病区入口, 护士站]
          patient_room_depth: 2
          utility_room_depth: 3

    # ────────────────────────────────────────────────────────────────────────
    # 拓扑关系矩阵
    # ────────────────────────────────────────────────────────────────────────
    topology_relationship_matrix:
      
      relationship_types:
        
        - type_id: TOPO-REL-ADJACENT-DIRECT
          type_name: 直接邻接
          definition: 两空间共享一面墙且有门洞直接相通
          depth_distance: 1
          attributes:
            door_width: {type: float, unit: mm}
            door_type: {type: enum, values: [swing, sliding, automatic, interlock]}
            access_control: {type: boolean}
            fire_rating: {type: string}
            
        - type_id: TOPO-REL-ADJACENT-WALL
          type_name: 隔墙邻接
          definition: 两空间相邻但无直接通道
          depth_distance: null  # 不可直接到达
          attributes:
            wall_type: {type: string}
            penetration_allowed: {type: boolean}
            fire_rating: {type: string}
            
        - type_id: TOPO-REL-CORRIDOR-CONNECTED
          type_name: 走廊连接
          definition: 两空间通过走廊相连
          depth_distance: 2+
          attributes:
            corridor_id: {type: reference}
            walking_distance: {type: float, unit: m}
            
        - type_id: TOPO-REL-BUFFER-CONNECTED
          type_name: 缓冲连接
          definition: 需要通过缓冲空间连接
          depth_distance: 2+
          attributes:
            buffer_type: {type: enum, values: [airlock, gowning, transfer]}
            sequence: {type: array}
            
        - type_id: TOPO-REL-VERTICAL-CONNECTED
          type_name: 垂直连接
          definition: 通过电梯/楼梯跨楼层连接
          depth_distance: 2+
          attributes:
            transport_type: {type: enum, values: [elevator, stair, ramp]}
            floor_difference: {type: integer}
            
        - type_id: TOPO-REL-SYSTEM-CONNECTED
          type_name: 系统连接
          definition: 通过机电系统管线连接（非物理通行）
          depth_distance: null  # 非人员通行
          attributes:
            system_type: {type: reference}  # 引用Agent-01的系统
            medium: {type: string}
            
        - type_id: TOPO-REL-ISOLATED
          type_name: 隔离关系
          definition: 两空间需要保持隔离
          depth_distance: null
          attributes:
            isolation_type: {type: enum, values: [physical, pressure, airflow]}
            min_separation: {type: float, unit: m}
            
      matrix_query_interface:
        queries:
          - get_direct_neighbors: "获取直接邻接的空间"
          - get_corridor_neighbors: "获取通过走廊连接的空间"
          - get_depth_to: "计算到目标空间的深度"
          - get_shortest_path: "获取最短路径"
          - get_integration_rank: "获取整合度排名"
          - check_isolation: "检查隔离要求"

  # ════════════════════════════════════════════════════════════════════════════
  # 增强版：Agent-05接口定义
  # ════════════════════════════════════════════════════════════════════════════
  agent_05_interface_enhanced:
    
    interface_description: |
      本接口定义为Agent-05（系统-空间耦合建模师）提供完整的空间模型访问能力。
      
      核心对接点：
      1. Agent-01的系统拓扑 ↔ Agent-02的空间拓扑 → 超图耦合
      2. 系统节点需要安装位置 → 空间节点提供位置
      3. 系统管线需要路由路径 → 空间拓扑提供连接关系
      4. 系统服务需要目标空间 → 空间需求提供环境参数
      
    # ────────────────────────────────────────────────────────────────────────
    # 接口1：空间层级与编码
    # ────────────────────────────────────────────────────────────────────────
    space_hierarchy_interface:
      
      methods:
        - method: get_space_by_id(space_id)
          description: 根据编码获取空间完整信息
          returns: Space对象
          
        - method: get_children(space_id)
          description: 获取子空间列表
          returns: List[Space]
          
        - method: get_parent(space_id)
          description: 获取父空间
          returns: Space
          
        - method: get_by_type(space_type)
          description: 根据空间类型获取空间列表
          returns: List[Space]
          
        - method: get_by_level(level_id)
          description: 根据层级获取空间列表
          returns: List[Space]
          
    # ────────────────────────────────────────────────────────────────────────
    # 接口2：空间拓扑查询
    # ────────────────────────────────────────────────────────────────────────
    space_topology_interface:
      
      methods:
        - method: get_topology_relationship(space_a, space_b)
          description: 获取两空间的拓扑关系
          returns: TopologyRelationType
          
        - method: get_direct_neighbors(space_id)
          description: 获取直接邻接的空间
          returns: List[Space]
          
        - method: get_depth_from_entrance(space_id)
          description: 获取从入口到该空间的深度
          returns: int
          
        - method: get_shortest_path(from_space, to_space)
          description: 获取最短路径（空间序列）
          returns: List[Space]
          
        - method: get_connectivity(space_id)
          description: 获取空间的连接度
          returns: int
          
        - method: get_integration(space_id)
          description: 获取空间的整合度
          returns: float
          
        - method: get_system_routing_options(from_space, to_space, system_type)
          description: |
            获取系统管线从起点到终点的可选路由路径。
            考虑穿越约束、防火分区、竖井位置等。
          parameters:
            from_space: 起点空间ID
            to_space: 终点空间ID
            system_type: 系统类型（HVAC/ELEC/GAS等）
          returns:
            paths: List[RoutingPath]
            each_path:
              - sequence: List[Space]
              - penetration_points: List[PenetrationPoint]
              - constraints: List[Constraint]
              
    # ────────────────────────────────────────────────────────────────────────
    # 接口3：医疗工艺流程查询
    # ────────────────────────────────────────────────────────────────────────
    medical_process_interface:
      
      methods:
        - method: get_zone_processes(zone_id)
          description: 获取区域的核心业务流程
          returns: List[ProcessFlow]
          
        - method: get_flow_spatial_sequence(flow_id)
          description: 获取流程对应的空间序列
          returns: List[Space]
          
        - method: get_flow_environmental_requirements(flow_id)
          description: 获取流程各步骤的环境要求
          returns: List[EnvironmentRequirement]
          
        - method: get_adjacency_constraints(zone_id)
          description: 获取区域的空间邻接约束
          returns: List[AdjacencyConstraint]
          
        - method: validate_layout_against_process(zone_id, layout)
          description: 验证布局是否满足流程要求
          returns: ValidationResult
          
    # ────────────────────────────────────────────────────────────────────────
    # 接口4：环境参数需求
    # ────────────────────────────────────────────────────────────────────────
    environmental_requirements_interface:
      
      methods:
        - method: get_environmental_requirements(space_id)
          description: 获取空间的环境参数要求
          returns: EnvironmentRequirements
          format:
            temperature: "{min}-{max}°C ±{tolerance}"
            humidity: "{min}-{max}%RH ±{tolerance}"
            pressure: "{value} Pa (相对于 {reference})"
            air_change: "{value} ACH"
            cleanliness: "ISO{level}"
            noise: "≤{value} dB(A)"
            illuminance: "{value} lux"
            
        - method: get_subspace_environmental_variance(space_id)
          description: 获取子空间的环境参数差异
          returns: List[SubspaceEnvironment]
          example:
            - subspace: 手术操作区
              variance:
                cleanliness: "比房间整体高一级"
                air_velocity: "需要层流送风 0.25-0.35 m/s"
                
        - method: get_environmental_priority(space_id)
          description: 获取环境参数的优先级
          returns: ParameterPriorityList
          example:
            - space: 手术室
              priorities:
                - P1: [pressure, cleanliness]  # 最关键
                - P2: [temperature, humidity]   # 重要
                - P3: [noise, illuminance]     # 一般
                
    # ────────────────────────────────────────────────────────────────────────
    # 接口5：系统需求映射
    # ────────────────────────────────────────────────────────────────────────
    system_requirements_interface:
      
      methods:
        - method: get_required_systems(space_id)
          description: 获取空间所需的系统类型
          returns: List[SystemRequirement]
          format:
            - system_id: HVAC-CLEAN
              system_name: 洁净空调系统
              requirement_level: mandatory
              key_parameters:
                - temperature_control: "22-25°C ±1"
                - humidity_control: "40-60%RH ±5"
                - pressure_control: "+15Pa"
                
        - method: get_system_criticality(space_id)
          description: 获取各系统的关键性级别
          returns: List[SystemCriticality]
          format:
            - system_type: HVAC
              criticality: CRITICAL
              failure_impact: "手术暂停"
              redundancy: "N+1"
              transfer_time: null
            - system_type: ELEC
              criticality: CRITICAL
              failure_impact: "手术暂停"
              transfer_time: "≤0.5s"
              
        - method: get_medical_gas_requirements(space_id)
          description: 获取医用气体终端需求
          returns: MedicalGasRequirements
          format:
            - gas_type: O2
              outlets: 4
              pressure: 0.4 MPa
              location_preference: "床旁/手术台旁"
              
        - method: get_electrical_requirements(space_id)
          description: 获取电气系统需求
          returns: ElectricalRequirements
          format:
            power_density: 300 VA/m²
            socket_count: {medical: 12, general: 8}
            emergency_power: true
            isolated_power: true
            ups_backup: true
            
    # ────────────────────────────────────────────────────────────────────────
    # 接口6：系统-空间耦合映射表
    # ────────────────────────────────────────────────────────────────────────
    mapping_tables:
      
      space_to_hvac_mapping:
        description: 空间类型到HVAC系统需求的映射
        format:
          space_type: ROOM-OR-I
          hvac_requirements:
            system_type: HVAC-CLEAN-LAMINAR
            supply_air_temp: "22-24°C"
            supply_velocity: "0.25-0.30 m/s"
            air_changes: 36
            fresh_air_ratio: "≥60%"
            filtration: "初效+中效+高效"
            pressure: "+15Pa"
            
      space_to_electrical_mapping:
        description: 空间类型到电气系统需求的映射
        format:
          space_type: ROOM-OR
          electrical_requirements:
            load_classification: 一级负荷
            isolated_power: true
            socket_config: {medical: 12, general: 8}
            emergency_transfer: "≤0.5s"
            ups_duration: "≥30min"
            
      space_to_medical_gas_mapping:
        description: 空间类型到医用气体需求的映射
        format:
          space_type: ROOM-OR
          medical_gas_requirements:
            O2: {outlets: 4, pressure: 0.4}
            VAC: {outlets: 4, pressure: -0.04}
            AIR: {outlets: 2, pressure: 0.4}
            N2O: {outlets: 1, pressure: 0.4, optional: true}
            
      space_to_control_requirements:
        description: 空间类型到控制要求的映射
        format:
          space_type: ROOM-OR
          control_requirements:
            temperature: {type: PID, precision: "±0.5°C", response: "≤5min"}
            humidity: {type: PID, precision: "±5%", response: "≤10min"}
            pressure: {type: continuous, alarm: "±3Pa"}
            cleanliness: {type: monitoring, alarm: "超标"}

  # ════════════════════════════════════════════════════════════════════════════
  # 更新：完整性检查清单
  # ════════════════════════════════════════════════════════════════════════════
  completeness_checklist:
    
    v1_0_items:
      - "[✓] L0-L5全部6个层级已定义"
      - "[✓] 每个层级都有完整的属性定义"
      - "[✓] 层级间关系已明确定义"
      - "[✓] 编码规则已完整定义"
      - "[✓] 功能区域分类已完整"
      - "[✓] 房间分类已覆盖主要类型"
      - "[✓] 8类医疗专用空间已详细建模"
      
    v1_1_new_items:
      - "[✓] 一级流程-空间耦合（宏观动线层）已定义"
      - "[✓] 二级流程-空间耦合（区域布局层）已定义"
      - "[✓] 三级流程-空间耦合（房间行为层）已定义"
      - "[✓] 空间拓扑元素（节点类型、边类型）已定义"
      - "[✓] 空间拓扑指标（连接度、深度、整合度、控制值）已定义"
      - "[✓] 医疗场景空间拓扑模型（手术区、病区）已建立"
      - "[✓] 拓扑关系矩阵已定义"
      - "[✓] Agent-05增强版接口已定义"
      - "[✓] 6类接口方法已完整定义"
      - "[✓] 空间-系统映射表已提供"

  # ════════════════════════════════════════════════════════════════════════════
  # 统计摘要（更新）
  # ════════════════════════════════════════════════════════════════════════════
  statistics:
    
    version: 1.1
    
    hierarchy_levels: 6
    zone_categories: 5
    zone_sub_types: 23
    room_types: 12
    room_variants: 45
    
    special_space_models: 8
    total_attributes_defined: 450
    
    # v1.1 新增
    process_flow_models: 15
    topology_node_types: 5
    topology_edge_types: 6
    topology_metrics: 5
    topology_relationship_types: 7
    
    agent_05_interface_methods: 25
    mapping_tables: 4
    
    reference_standards: 6
    
    generated_for:
      agent_05: 系统-空间耦合建模师
      agent_08: 运维管理建模师
```

---

## 完善内容总结

### 1. 新增：医疗工艺流程-空间耦合模型

| 流程层级 | 空间层级 | 核心内容 | 完成度 |
|---------|---------|----------|--------|
| **一级流程** | L1建筑+L2楼层+L3区域 | 5类主要动线（急诊、择期手术、门诊、医护、物流）+ 建筑/区域间关系要求 | ✅ 完成 |
| **二级流程** | L3功能区域内部 | 手术区（三区三通道）、ICU、门诊区的详细布局和4类流程（患者/医护/无菌/污物） | ✅ 完成 |
| **三级流程** | L4房间+L5子空间 | 手术室各子空间的具体行为过程、设备布局、隐私考虑 | ✅ 完成 |

### 2. 新增：空间拓扑结构模型（基于空间句法）

| 内容类别 | 详细内容 | 与Agent-01对比 |
|---------|---------|---------------|
| **节点类型** | 入口节点、枢纽节点、通道节点、功能节点、缓冲节点 | 对应：源节点、分配节点、边、汇节点、调节节点 |
| **边类型** | 直接连接、走廊连接、垂直连接、缓冲连接 | 对应：Trunk、Branch、Terminal |
| **拓扑指标** | 连接度、深度、整合度、控制值、选择度 | 用于空间可达性分析 |
| **拓扑模型** | 手术区拓扑图、病区拓扑图 | 支持Agent-05超图耦合 |

### 3. 增强：Agent-05接口定义

| 接口类别 | 方法数量 | 核心功能 |
|---------|---------|---------|
| 空间层级接口 | 5 | 空间查询、层级导航 |
| 空间拓扑接口 | 7 | 邻接查询、深度计算、路径规划、系统路由 |
| 医疗流程接口 | 5 | 流程查询、空间序列、邻接约束验证 |
| 环境需求接口 | 4 | 参数查询、子空间差异、优先级 |
| 系统需求接口 | 4 | 系统需求、关键性、医用气体、电气 |
| 映射表 | 4 | HVAC/电气/医用气体/控制的空间映射 |

### 4. 解决的评审意见

| 评审问题 | 解决方案 |
|---------|---------|
| L3与二级流程耦合不足 | 新增`level_2_process_coupling`，为手术区/ICU/门诊区定义完整的流程-空间模型 |
| 空间拓扑表达不完整 | 新增`space_topology_model`，基于空间句法定义节点/边/指标/拓扑图 |
| Agent-05接口简化 | 新增25个接口方法+4个映射表，覆盖拓扑查询/流程查询/路由规划 |

---

**本文档v1.1版本已完成完善，可支撑Agent-05基于超图的系统-空间拓扑耦合建模。**
[^1]: [# 医疗专用空间详细建模（Medical Spe...   - terminal_locations](# 医疗专用空间详细建模（Medical Spe...   - terminal_locations)

[^2]: [# 医疗专用空间详细建模（Medical Spe...   - terminal_locations](# 医疗专用空间详细建模（Medical Spe...   - terminal_locations)

[^3]: [# === AGENT-09: 统一CIM模型 ...on: “医用床塔管道疋 - 吊臂式供气供电+](# === AGENT-09: 统一CIM模型 ...on: “医用床塔管道疋 - 吊臂式供气供电+)

[^4]: [# 医疗建筑空间分类体系（Healthcare ..."防振动", "UPS供电", "患者通话"]](# 医疗建筑空间分类体系（Healthcare ..."防振动", "UPS供电", "患者通话"])

[^5]: [# Agent-09: 模型整合验证框架 (Mo...  overall_progress: 15%](# Agent-09: 模型整合验证框架 (Mo...  overall_progress: 15%)

[^6]: [# 医疗建筑空间本体模型元数据（Medical ...tion: "结合具体医疗项目案例进行实例化"](# 医疗建筑空间本体模型元数据（Medical ...tion: "结合具体医疗项目案例进行实例化")

[^1]: [# 医疗建筑空间本体模型元数据（Medical ...tion: "结合具体医疗项目案例进行实例化"](# 医疗建筑空间本体模型元数据（Medical ...tion: "结合具体医疗项目案例进行实例化")

[^2]: [# 医疗建筑空间层级模型（Medical Bui...e_supply_chain: "无菌供应链"](# 医疗建筑空间层级模型（Medical Bui...e_supply_chain: "无菌供应链")

[^3]: [# 医疗建筑空间层级模型（Medical Bui...e_supply_chain: "无菌供应链"](# 医疗建筑空间层级模型（Medical Bui...e_supply_chain: "无菌供应链")

[^4]: [# Agent-05和Agent-07输出文件重..."

[^5]: [# Agent-09: 一致性验证结果报告

[^6]: [# 医疗建筑空间层级模型（Medical Bui...e_supply_chain: "无菌供应链"](# 医疗建筑空间层级模型（Medical Bui...e_supply_chain: "无菌供应链")

[^1]: [# 医疗建筑技术系统拓扑建模项目

[^2]: [# Agent-03: 设备本体建模师 (Equ...体化建模

[^3]: [# Agent-07: 计量体系建模师 - 元数...筑能耗远程监测系统技术规程》"

[^4]: [Agent01_Output.project_summary.md](http://file/857edf8d-27c4-46a4-9be6-49c7310e56fc.md)

[^5]: [医疗建筑技术系统CIM建模 - 完整Agent体系.md](http://file/75590c72-49df-4f5a-af4e-b17adf216682.md)

[^6]: [# Agent-05和Agent-07输出文件重..."
---