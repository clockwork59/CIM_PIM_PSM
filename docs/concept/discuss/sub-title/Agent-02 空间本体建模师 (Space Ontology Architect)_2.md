## 🧑‍💻 User




---
## 🤖 Assistant


根据评审意见的深入分析，我现在完善Agent-02的输出，补充三个关键部分：
1. **设施设备配置模型**
2. **系统硬件-空间耦合模型**
3. **信息系统与空间耦合模型**

---

# Agent-02: 空间本体建模师 (Space Ontology Architect)
## 完善版输出文档 v1.2

---

```yaml
# ═══════════════════════════════════════════════════════════════════════════════
# Agent-02: 空间本体建模师 (Space Ontology Architect)
# 医疗建筑空间本体模型 - 完善版 v1.2
# 新增内容：设施设备配置 + 系统硬件耦合 + 信息系统耦合
# ═══════════════════════════════════════════════════════════════════════════════

Agent02_Output:

meta:
 agent_id: Agent-02
 agent_name: 空间本体建模师
 version: 1.2
 version_note: |
 v1.2更新内容：
 1. 新增"设施设备配置模型"（医疗设备、家具设施、服务终端）
 2. 新增"系统硬件-空间耦合模型"（HVAC/电气/医气/给排水在空间中的布置）
 3. 新增"信息系统与空间耦合模型"（IT基础设施、医疗物联网）
 4. 完善Agent-05接口（设备需求、系统末端位置）
 generated_at: 2024-12-20T00:00:00+08:00

# ════════════════════════════════════════════════════════════════════════════
# 第六部分：设施设备配置模型（v1.2新增）
# ════════════════════════════════════════════════════════════════════════════
facility_equipment_configuration:

 model_description: |
 本模型定义医疗建筑中各类空间所需的标准设施设备配置。
 包括设备清单、技术参数、空间占用、安装约束、系统接口需求。
 这是Agent-05进行系统容量设计和末端布置的基础输入。

 设备分类逻辑：
 - 医疗设备（Medical Equipment）：直接用于诊疗的专业设备
 - 家具设施（Furniture & Fixtures）：房间基本家具和固定装置
 - 服务终端（Service Terminals）：系统的空间末端接口
 - 辅助设备（Auxiliary Equipment）：支持性办公和服务设备

 # ────────────────────────────────────────────────────────────────────────
 # 设备分类体系
 # ────────────────────────────────────────────────────────────────────────
 equipment_classification:

 - category_id: EQUIP-MED
 category_name: 医疗设备
 category_name_en: Medical Equipment
 description: 直接用于患者诊断、治疗、监护的专业医疗设备

 sub_categories:
 - sub_id: EQUIP-MED-SURG
 sub_name: 手术设备
 examples: [手术台, 无影灯, 手术显微镜, 电刀, C臂X光机]

 - sub_id: EQUIP-MED-ANES
 sub_name: 麻醉设备
 examples: [麻醉机, 麻醉气体监测仪, 麻醉废气排放装置]

 - sub_id: EQUIP-MED-MONITOR
 sub_name: 监护设备
 examples: [多参数监护仪, 心电监护仪, 血氧仪]

 - sub_id: EQUIP-MED-LIFE
 sub_name: 生命支持设备
 examples: [呼吸机, 除颤仪, ECMO, 主动脉内球囊反搏]

 - sub_id: EQUIP-MED-INFUSION
 sub_name: 输注设备
 examples: [输液泵, 注射泵, 肠内营养泵]

 - sub_id: EQUIP-MED-IMAGING
 sub_name: 影像设备
 examples: [CT, MRI, DR, DSA, 超声]

 - sub_id: EQUIP-MED-LAB
 sub_name: 检验设备
 examples: [生化分析仪, 血球计数仪, PCR仪]

 - category_id: EQUIP-FURN
 category_name: 家具设施
 category_name_en: Furniture & Fixtures
 description: 房间的基本家具和固定装置

 sub_categories:
 - sub_id: EQUIP-FURN-BED
 sub_name: 病床类
 examples: [普通病床, ICU电动床, 婴儿床, 担架车]

 - sub_id: EQUIP-FURN-WORK
 sub_name: 工作台类
 examples: [诊桌, 治疗台, 器械台, 护士站工作台]

 - sub_id: EQUIP-FURN-STORAGE
 sub_name: 储存类
 examples: [药品柜, 器械柜, 更衣柜, 污物柜]

 - sub_id: EQUIP-FURN-SEAT
 sub_name: 座椅类
 examples: [医生椅, 患者候诊椅, 陪护椅]

 - category_id: EQUIP-TERM
 category_name: 服务终端
 category_name_en: Service Terminals
 description: 各系统的空间末端接口设备

 sub_categories:
 - sub_id: EQUIP-TERM-GAS
 sub_name: 医用气体终端
 examples: [氧气终端, 负压吸引终端, 压缩空气终端]

 - sub_id: EQUIP-TERM-ELEC
 sub_name: 电气终端
 examples: [医用插座, 普通插座, 等电位接地端子]

 - sub_id: EQUIP-TERM-HVAC
 sub_name: 暖通终端
 examples: [送风口, 回风口, 排风口, 温控面板]

 - sub_id: EQUIP-TERM-INFO
 sub_name: 信息终端
 examples: [网络接口, 呼叫按钮, 床头信息面板]

 - sub_id: EQUIP-TERM-WATER
 sub_name: 给排水终端
 examples: [洗手池, 地漏, 紧急洗眼器]

 - category_id: EQUIP-AUX
 category_name: 辅助设备
 category_name_en: Auxiliary Equipment
 description: 支持医疗工作的辅助性设备

 sub_categories:
 - sub_id: EQUIP-AUX-IT
 sub_name: 信息设备
 examples: [计算机工作站, 打印机, 条码扫描仪]

 - sub_id: EQUIP-AUX-CLEAN
 sub_name: 清洁消毒设备
 examples: [空气消毒机, 紫外灯, 手卫生设备]

 - sub_id: EQUIP-AUX-TRANS
 sub_name: 转运设备
 examples: [转运车, 药品车, 病历车]

 # ────────────────────────────────────────────────────────────────────────
 # 手术室设备配置详细模型
 # ────────────────────────────────────────────────────────────────────────
 room_equipment_configurations:

 - room_type_id: ROOM-OR-I
 room_type_name: I级洁净手术室
 room_area_range: [40, 60]
 room_area_unit: m²

 # 医疗设备清单
 medical_equipment:

 - equipment_id: EQUIP-OR-TABLE
 equipment_name: 手术台
 equipment_name_en: Surgical Table
 category: EQUIP-MED-SURG
 quantity: 1

 specifications:
 dimensions:
 length: 2100 # mm
 width: 700 # mm
 height_range: [700, 1100] # mm，可调节
 weight: 350 # kg（空载）
 max_patient_weight: 250 # kg
 movement:
 tilting: ±25° # 侧倾/头足倾
 height_adjustment: 400 # mm升降范围
 longitudinal_slide: 300 # mm纵向移动
 materials: 不锈钢台面 + 碳纤维基座（透X线）

 system_requirements:
 electrical:
 voltage: 220V
 power: 1.5 # kVA
 circuit_type: 隔离电源
 outlets_needed: 1
 control: 脚踏开关
 medical_gas:
 O2: 1 # 终端数（床旁供应）
 VAC: 1 # 终端数（吸引）

 space_requirements:
 footprint: 2.5×1.2 # m（设备占地）
 clearance:
 front: 1.5 # m（主刀侧）
 back: 1.2 # m（助手侧）
 head: 1.5 # m（麻醉工作区）
 foot: 1.0 # m
 installation:
 floor_type: 防滑垫固定或螺栓锚固
 floor_load: 500 # kg/m²
 vibration_isolation: 推荐

 positioning:
 location: 手术操作区中心
 orientation: 长轴与层流送风口平行
 reference_point: 距墙≥2m

 maintenance:
 cleaning: 每次手术后表面消毒
 calibration: 每年校准一次
 service_life: 15年
 maintenance_space: 设备四周≥0.5m

 - equipment_id: EQUIP-OR-LIGHT
 equipment_name: 无影灯
 equipment_name_en: Surgical Shadowless Light
 category: EQUIP-MED-SURG
 quantity: 1

 specifications:
 type: LED悬臂式
 main_light:
 diameter: 700 # mm
 illuminance: "40000-160000 lux"
 color_temperature: "4000-6500K"
 color_rendering_index: ≥95
 satellite_light:
 diameter: 500 # mm
 illuminance: "40000-120000 lux"
 arm_reach: 2500 # mm
 rotation: 360°
 depth_of_illumination: ≥1200 # mm

 system_requirements:
 electrical:
 voltage: 220V
 power: 1.2 # kVA
 circuit_type: 隔离电源
 outlets_needed: 1
 control: 面板/手控/脚踏
 dimming: 0-100%可调

 space_requirements:
 suspension_point: 吊顶承重点
 ceiling_structure: 承重≥500kg
 ceiling_void_height: ≥600 # mm（安装高度）
 rotation_clearance: 3000 # mm直径范围内无障碍物
 minimum_ceiling_height: 3000 # mm

 positioning:
 location: 手术台正上方
 vertical_alignment: 手术台中心

 installation:
 type: 吊顶预埋件
 reinforcement: 吊顶需加强
 anti_sway: 需要防晃装置

 - equipment_id: EQUIP-OR-ANESTHESIA
 equipment_name: 麻醉机
 equipment_name_en: Anesthesia Machine
 category: EQUIP-MED-ANES
 quantity: 1

 specifications:
 type: 全功能麻醉工作站
 functions:
 - 气体混合与输送
 - 机械通气
 - 挥发性麻醉剂蒸发
 - 患者监测
 dimensions:
 width: 900 # mm
 depth: 750 # mm
 height: 1500 # mm
 weight: 200 # kg

 system_requirements:
 electrical:
 voltage: 220V
 power: 2.5 # kVA
 circuit_type: 隔离电源
 ups_backup: 必需
 outlets_needed: 3
 medical_gas:
 O2:
 quantity: 2 # 终端
 pressure: 0.4 # MPa
 flow_rate: "0-15 L/min"
 N2O:
 quantity: 1 # 终端（可选）
 pressure: 0.4 # MPa
 AIR:
 quantity: 1 # 终端
 pressure: 0.4 # MPa
 VAC:
 quantity: 2 # 终端
 pressure: -0.04 # MPa
 scavenging:
 required: true
 connection: 麻醉废气排放系统

 space_requirements:
 footprint: 1.2×0.9 # m
 clearance:
 front: 1.0 # m（操作空间）
 sides: 0.6 # m
 back: 0.3 # m（靠墙）
 gas_outlet_proximity: ≤1.5 # m

 positioning:
 location: 患者头端
 orientation: 面向麻醉医生工作位
 distance_to_patient: 0.5-1.0 # m

 - equipment_id: EQUIP-OR-MONITOR
 equipment_name: 多参数监护仪
 equipment_name_en: Multi-parameter Monitor
 category: EQUIP-MED-MONITOR
 quantity: 1

 specifications:
 display: 15-17寸彩色触摸屏
 parameters:
 - ECG (3/5/12导)
 - SpO2 (血氧饱和度)
 - NIBP (无创血压)
 - IBP (有创血压，可选)
 - TEMP (体温)
 - EtCO2 (呼末二氧化碳)
 - BIS (脑电双频指数，可选)
 dimensions:
 width: 380 # mm
 height: 300 # mm
 depth: 180 # mm
 weight: 8 # kg

 system_requirements:
 electrical:
 voltage: 220V
 power: 0.3 # kVA
 circuit_type: 隔离电源
 ups_backup: 必需（≥30min）
 outlets_needed: 1
 network:
 interface: RJ45
 protocol: HL7
 function: 数据传输至护士站

 positioning:
 location: 麻醉工作区
 viewing_distance: 1.0-2.0 # m
 visibility: 麻醉医生视线范围
 mounting: 吊臂/推车/壁挂

 - equipment_id: EQUIP-OR-ELECTROSURG
 equipment_name: 高频电刀
 equipment_name_en: Electrosurgical Unit
 category: EQUIP-MED-SURG
 quantity: 1

 specifications:
 type: 多功能高频电外科设备
 power_output: 300-400W（切割）
 modes:
 - 单极切割
 - 单极凝固
 - 双极凝固
 dimensions:
 width: 380 # mm
 height: 150 # mm
 depth: 350 # mm

 system_requirements:
 electrical:
 voltage: 220V
 power: 1.0 # kVA
 circuit_type: 隔离电源
 grounding: 专用接地
 outlets_needed: 1
 safety:
 grounding_pad: 一次性接地极板
 alarm: 接地不良报警

 positioning:
 location: 器械区
 distance_to_patient: 1.5-2.0 # m
 foot_switch_placement: 主刀医生脚边

 - equipment_id: EQUIP-OR-SUCTION
 equipment_name: 中央吸引终端
 equipment_name_en: Central Suction Terminal
 category: EQUIP-TERM-GAS
 quantity: 4

 specifications:
 type: 壁挂式/吊塔式终端
 vacuum_pressure: -0.04 MPa
 flow_rate: 40 # L/min
 outlet_standard: DISS或国标

 positioning:
 locations:
 - 手术操作区×2（吸引污血）
 - 麻醉区×2（吸引分泌物）
 height: 1.5-1.8 # m
 proximity_to_patient: ≤1.5 # m

 - equipment_id: EQUIP-OR-C-ARM
 equipment_name: C臂X光机
 equipment_name_en: C-arm X-ray System
 category: EQUIP-MED-IMAGING
 quantity: 0-1 # 根据手术类型
 optional: true

 specifications:
 type: 移动式C臂
 image_intensifier: 12寸
 dimensions:
 footprint: 1.5×1.0 # m
 height: 2.0 # m
 weight: 400 # kg

 system_requirements:
 electrical:
 voltage: 220V
 power: 5.0 # kVA
 circuit_type: 普通电源（需大容量）
 outlets_needed: 1
 shielding:
 required: false（移动设备）
 protective_screens: 铅屏风

 space_requirements:
 storage_area: 手术室角落或相邻储存间
 movement_path: 无障碍通行

 # 家具设施清单
 furniture_fixtures:

 - item_id: FURN-OR-INSTRUMENT-TABLE
 item_name: 手术器械台
 item_name_en: Instrument Table
 category: EQUIP-FURN-WORK
 quantity: 2

 specifications:
 dimensions:
 length: 1500 # mm
 width: 600 # mm
 height: 900 # mm（与手术台平齐）
 material: 不锈钢
 features:
 - 可升降
 - 可倾斜
 - 带围栏
 surface_area: 0.9 # m²（展开无菌器械）

 positioning:
 location: 手术台两侧
 distance_to_table: 0.6-1.0 # m

 - item_id: FURN-OR-MAYO-STAND
 item_name: 托盘架（Mayo Stand）
 item_name_en: Mayo Stand
 category: EQUIP-FURN-WORK
 quantity: 1

 specifications:
 dimensions:
 tray_size: 500×400 # mm
 height_range: [800, 1200] # mm
 material: 不锈钢
 features: 可升降、可旋转

 positioning:
 location: 主刀医生侧
 function: 放置常用器械

 - item_id: FURN-OR-STERILE-CABINET
 item_name: 无菌物品柜
 item_name_en: Sterile Supply Cabinet
 category: EQUIP-FURN-STORAGE
 quantity: 1

 specifications:
 dimensions:
 width: 1200 # mm
 depth: 500 # mm
 height: 1800 # mm
 material: 不锈钢或抗菌层压板
 features:
 - 密闭门
 - 可调层板
 - 洁净存放

 positioning:
 location: 手术室内或相邻无菌物品间
 accessibility: 洁净走廊可达

 - item_id: FURN-OR-STEP-STOOL
 item_name: 脚踏凳
 item_name_en: Step Stool
 category: EQUIP-FURN-SEAT
 quantity: 2

 specifications:
 dimensions:
 platform_size: 400×350 # mm
 height_range: [200, 300] # mm
 material: 不锈钢
 features:
 - 防滑表面
 - 可堆叠

 - item_id: FURN-OR-WORK-STOOL
 item_name: 医护工作凳
 item_name_en: Surgical Stool
 category: EQUIP-FURN-SEAT
 quantity: 3

 specifications:
 dimensions:
 seat_diameter: 350 # mm
 height_range: [450, 650] # mm
 features:
 - 气压升降
 - 脚轮
 - 可旋转
 - 靠背（可选）

 # 服务终端配置
 service_terminals:

 - terminal_type: 医用气体终端
 gas_outlets:
 O2:
 quantity: 4
 locations:
 - position: 手术台头端墙面
 count: 2
 height: 1500 # mm
 - position: 麻醉区吊塔
 count: 2
 outlet_standard: DISS/国标GB
 pressure: 0.4 # MPa
 flow_capacity: 30 # L/min

 VAC:
 quantity: 4
 locations:
 - position: 手术操作区
 count: 2
 - position: 麻醉区
 count: 2
 outlet_standard: DISS/国标GB
 pressure: -0.04 # MPa
 flow_capacity: 60 # L/min

 AIR:
 quantity: 2
 locations:
 - position: 麻醉区
 count: 2
 pressure: 0.4 # MPa

 N2O:
 quantity: 1
 locations:
 - position: 麻醉区
 count: 1
 optional: true

 CO2:
 quantity: 1
 optional: true
 application: 腹腔镜手术

 N2:
 quantity: 1
 optional: true
 application: 手术器械驱动

 - terminal_type: 电源插座
 configurations:
 medical_grade:
 quantity: 12
 type: 医用安全插座
 voltage: 220V
 current_rating: 16A
 circuit: 隔离电源IT系统
 locations:
 - position: 手术台周围墙面
 count: 4
 height: 300-500 # mm
 - position: 麻醉区墙面
 count: 3
 height: 500-1000 # mm
 - position: 器械区墙面
 count: 2
 - position: 吊塔
 count: 3
 spacing: ≤2000 # mm（相邻插座间距）

 general:
 quantity: 8
 type: 普通电源插座
 voltage: 220V
 circuit: 普通供电回路
 locations:
 - position: 辅助区域墙面
 count: 8

 - terminal_type: 等电位接地
 configurations:
 bonding_terminal:
 quantity: 8
 locations:
 - 手术台周围：4个
 - 设备区域：4个
 height: 300 # mm
 resistance: ≤0.1Ω
 connected_items:
 - 手术台金属框架
 - 无影灯金属部分
 - 所有医疗设备外壳
 - 金属管道和框架

 - terminal_type: HVAC终端
 configurations:
 supply_air:
 type: 层流送风口
 dimensions: 2000×2500 # mm
 location: 手术台正上方吊顶
 velocity: 0.25-0.35 # m/s
 filtration: HEPA H14

 return_air:
 type: 回风口
 quantity: 4
 dimensions: 400×300 # mm each
 locations:
 - position: 房间两侧下部墙面
 count: 4
 height: 200-500 # mm

 exhaust:
 type: 排风口
 quantity: 2
 locations:
 - position: 房间对角上部
 height: 距吊顶200 # mm

 temperature_control:
 type: 温控面板
 location: 入口门旁墙面
 height: 1400 # mm
 functions:
 - 温度显示
 - 温度设定
 - 湿度显示
 - 压差显示

 - terminal_type: 信息终端
 configurations:
 network:
 quantity: 4
 type: RJ45千兆网口
 locations:
 - 麻醉区：2个
 - 器械区：1个
 - 入口处：1个

 nurse_call:
 quantity: 2
 locations:
 - 手术台头端
 - 入口门旁

 intercom:
 quantity: 1
 location: 入口门旁
 function: 与护士站对讲

 display:
 quantity: 2
 type: 医用显示器
 locations:
 - 术野对面墙面（影像显示）
 - 入口门旁（患者信息）

 - terminal_type: 给排水终端
 configurations:
 floor_drain:
 quantity: 2
 locations:
 - 手术台下方（排污血）
 - 洗手池附近
 floor_slope: ≥0.5%
 trap_type: 防臭水封

 equipment_drain:
 optional: true
 for: 冷却水排放

 # 设备系统需求汇总
 equipment_system_requirements_summary:

 electrical:
 total_power: 15 # kVA
 isolated_power: 10 # kVA
 general_power: 5 # kVA
 ups_capacity: 8 # kVA
 ups_duration: 30 # min

 medical_gas:
 O2:
 peak_flow: 60 # L/min
 terminals: 4
 VAC:
 peak_flow: 120 # L/min
 terminals: 4
 AIR:
 peak_flow: 30 # L/min
 terminals: 2
 N2O:
 peak_flow: 10 # L/min
 terminals: 1

 hvac:
 supply_air_volume: 4500 # m³/h
 air_changes: 36 # ACH
 fresh_air_ratio: 60 # %
 supply_temperature: 18-20 # °C
 room_temperature: 22-25 # °C
 room_humidity: 40-60 # %RH
 room_pressure: +15 # Pa

 network:
 data_points: 4
 bandwidth: 100 # Mbps

 # ────────────────────────────────────────────────────────────────────────
 # ICU病房设备配置
 # ────────────────────────────────────────────────────────────────────────
 - room_type_id: ROOM-ICU
 room_type_name: ICU病房（单床位）
 room_area_range: [15, 20]
 room_area_unit: m²

 medical_equipment:

 - equipment_id: EQUIP-ICU-BED
 equipment_name: ICU电动病床
 equipment_name_en: ICU Electric Bed
 quantity: 1

 specifications:
 type: 多功能ICU电动床
 dimensions:
 length: 2200 # mm
 width: 1000 # mm
 height_range: [400, 800] # mm
 weight: 300 # kg
 max_patient_weight: 250 # kg
 functions:
 - 电动升降
 - 背板角度调节
 - 腿板角度调节
 - 倾斜功能
 - CPR快速放平
 - 称重功能

 system_requirements:
 electrical:
 voltage: 220V
 power: 0.5 # kVA
 circuit_type: 隔离电源
 ups_backup: 推荐

 space_requirements:
 clearance:
 head: 1.0 # m（操作空间）
 sides: 1.2 # m（双侧护理通道）
 foot: 1.0 # m

 - equipment_id: EQUIP-ICU-MONITOR
 equipment_name: ICU多参数监护仪
 quantity: 1
 specifications:
 display: 17寸及以上
 parameters:
 - ECG (5/12导)
 - SpO2
 - NIBP/IBP
 - CVP
 - TEMP
 - EtCO2
 - CO (心输出量，可选)
 system_requirements:
 electrical:
 power: 0.3 # kVA
 ups_backup: 必需
 network:
 interface: RJ45/WiFi
 integration: 中央监护系统

 - equipment_id: EQUIP-ICU-VENT
 equipment_name: 呼吸机
 quantity: 1
 specifications:
 type: 有创/无创一体机
 modes: [IPPV, SIMV, PSV, CPAP, BiPAP]
 system_requirements:
 electrical:
 power: 0.8 # kVA
 ups_backup: 必需（≥60min）
 medical_gas:
 O2: 1终端
 AIR: 1终端

 - equipment_id: EQUIP-ICU-INFUSION
 equipment_name: 输液泵/注射泵
 quantity: 6-10
 specifications:
 types:
 - 大容量输液泵×4
 - 精密注射泵×4-6
 system_requirements:
 electrical:
 power: 0.3 # kVA（全部）
 outlets: 10

 - equipment_id: EQUIP-ICU-DEFIB
 equipment_name: 除颤仪
 quantity: 1（可共用）
 specifications:
 type: 双相波除颤+起搏+监护
 positioning:
 location: 床旁或病区共用

 service_terminals:

 medical_gas:
 O2:
 quantity: 2
 locations: 床头板两侧
 VAC:
 quantity: 2
 locations: 床头板两侧
 AIR:
 quantity: 1
 locations: 床头板

 electrical:
 medical_outlet:
 quantity: 16
 locations: 床头板+墙面
 circuit: 隔离电源
 general_outlet:
 quantity: 4

 bedside_panel:
 functions:
 - 电源控制
 - 气体终端
 - 呼叫按钮
 - 阅读灯控制
 - 网络接口

 equipment_system_requirements_summary:
 electrical:
 per_bed_power: 10 # kVA
 medical_gas:
 O2_flow: 30 # L/min
 VAC_flow: 60 # L/min

 # ────────────────────────────────────────────────────────────────────────
 # 负压隔离病房设备配置
 # ────────────────────────────────────────────────────────────────────────
 - room_type_id: ROOM-ISO-NEG
 room_type_name: 负压隔离病房
 room_area_range: [18, 25]

 medical_equipment:
 # （类似ICU，但增加隔离相关设备）

 - equipment_id: EQUIP-ISO-AIRLOCK
 equipment_name: 门互锁控制器
 quantity: 1
 specifications:
 function: 双门互锁
 display: 门状态指示
 override: 紧急解除按钮
 positioning:
 location: 缓冲间

 - equipment_id: EQUIP-ISO-PRESSURE
 equipment_name: 压差显示器
 quantity: 2
 specifications:
 display: 数字显示+趋势
 alarm: 压差异常声光报警
 locations:
 - 病室内
 - 缓冲间

 - equipment_id: EQUIP-ISO-PASSBOX
 equipment_name: 传递窗
 quantity: 1
 specifications:
 type: 双门互锁+紫外消毒
 dimensions: 600×600×600 # mm
 positioning:
 location: 病室与走廊之间墙面

 service_terminals:
 hvac:
 supply_air:
 type: 高效过滤送风口
 location: 病室吊顶
 exhaust:
 type: HEPA过滤排风口
 location: 病室下部（靠近床头）
 filtration: HEPA H14
 discharge: 独立排放至屋顶

 pressure_monitoring:
 sensors:
 - location: 病室
 setpoint: -15Pa
 - location: 缓冲间
 setpoint: -5Pa
 - location: 卫生间
 setpoint: -20Pa

# ════════════════════════════════════════════════════════════════════════════
# 第七部分：系统硬件-空间耦合模型（v1.2新增）
# ════════════════════════════════════════════════════════════════════════════
hardware_system_space_coupling:

 model_description: |
 本模型定义机电系统在空间中的具体布置方式。
 为Agent-05提供系统末端位置、管线路由、设备安装约束等信息。

 耦合维度：
 - 主机安装位置（设备房在哪里）
 - 末端位置（送风口/插座/气体终端的具体位置）
 - 管线路由（竖井位置、吊顶走管、穿墙穿板）
 - 维护空间（检修通道、更换滤网空间）

 # ────────────────────────────────────────────────────────────────────────
 # HVAC系统-空间耦合
 # ────────────────────────────────────────────────────────────────────────
 hvac_space_coupling:

 # 以I级洁净手术室为例
 room_type: ROOM-OR-I

 air_supply_system:

 source_equipment:
 type: 洁净空调机组
 location: 空调机房（手术区同层或相邻层）
 distance_to_room: ≤50m（推荐）

 supply_air_path:
 trunk_duct:
 location: 技术走廊吊顶内
 material: 镀锌钢板
 size: 500×500mm（至分支前）
 insulation: 40mm橡塑保温

 branch_duct:
 location: 洁净走廊吊顶内
 size: 400×300mm

 final_connection:
 location: 手术室吊顶内
 size: 根据静压箱设计

 terminal_in_room:
 type: 层流送风口+HEPA过滤器
 quantity: 1
 dimensions: 2400×2600mm
 location:
 position: 手术台正上方
 ceiling_coordinates: 房间中心偏床头方向
 ceiling_cutout: 需预留安装孔
 installation:
 frame: 嵌入式安装框
 seal: 四周密封
 access: 过滤器可从吊顶下方更换
 maintenance_space:
 above_ceiling: ≥800mm高度
 filter_change_direction: 向下抽取

 air_return_system:

 return_air_path:
 location: 房间两侧下部墙面→吊顶内回风管

 terminal_in_room:
 type: 回风口
 quantity: 4
 dimensions: 400×300mm each
 locations:
 - position: 左侧墙面下部
 count: 2
 height: 200-400mm
 - position: 右侧墙面下部
 count: 2
 height: 200-400mm
 installation:
 frame: 嵌入式百叶格栅
 filter: 初效过滤器（可选）

 air_exhaust_system:

 terminal_in_room:
 type: 排风口
 quantity: 2
 dimensions: 300×200mm
 locations:
 - position: 房间对角上部
 height: 距吊顶200mm
 connection:
 duct: 连接至排风竖井

 pressure_control:

 sensor_location:
 type: 微压差传感器
 position: 侧墙中部
 height: 1500mm
 quantity: 1
 reference: 走廊（测量室内外压差）

 control_method:
 type: 定压变风量
 actuator: 送风变频+定压阀
 actuator_location: 空调机房

 display:
 location: 入口门旁墙面
 content: 实时压差值、温度、湿度
 alarm: 压差<10Pa报警

 temperature_humidity_control:

 temperature_sensor:
 location: 房间中部
 height: 1500mm
 type: PT100
 signal: 4-20mA或网络

 humidity_sensor:
 location: 与温度传感器组合
 type: 电容式

 control_actuator:
 type: 电动调节阀
 location: 空调机组冷/热水管

 ductwork_routing:

 vertical_shaft:
 location: 手术区核心竖井
 size: 1500×1200mm（共用）
 contents:
 - 送风主管
 - 回风主管
 - 排风管
 - 冷冻水管
 - 蒸汽管

 horizontal_routing:
 location: 技术走廊吊顶内
 ceiling_void_height: ≥1200mm
 coordination:
 sequence: 电气桥架→水管→风管（从上到下）
 separation: 强弱电分离≥300mm

 penetrations:
 wall_penetration:
 type: 套管+防火封堵
 location: 从技术走廊进入手术室
 ceiling_penetration:
 type: 密封接口
 location: 送风口与吊顶结合部

 maintenance_access:

 filter_change:
 access_method: 吊顶检修口
 access_size: ≥600×600mm
 frequency: 每6-12个月

 duct_cleaning:
 access_method: 风管检修门
 frequency: 每2年

 sensor_calibration:
 access: 墙面传感器可直接操作
 frequency: 每年

 # ────────────────────────────────────────────────────────────────────────
 # 医用气体系统-空间耦合
 # ────────────────────────────────────────────────────────────────────────
 medical_gas_space_coupling:

 room_type: ROOM-OR-I

 oxygen_system:

 source:
 type: 液氧罐或汇流排
 location: 医用气体站房（室外或独立建筑）

 distribution:
 main_trunk:
 material: 脱脂铜管
 size: DN25（主干）
 location: 医用气体竖井

 floor_distribution:
 size: DN20
 location: 技术走廊吊顶内

 branch_to_room:
 size: DN15
 location: 吊顶内至墙面终端

 terminal_in_room:
 type: 快速自封接头
 standard: DISS或GB国标
 quantity: 4
 locations:
 - position: 手术台头端墙面
 count: 2
 height: 1500mm
 - position: 麻醉吊塔
 count: 2
 pressure: 0.4±0.05 MPa
 flow_capacity: 30 L/min each

 pressure_regulation:
 main_regulator:
 location: 医用气体站房
 output_pressure: 0.4 MPa

 area_regulator:
 location: 手术区走廊气体阀门箱
 function: 区域关断+压力显示

 monitoring:
 pressure_sensor:
 location: 气体阀门箱内
 alarm: 低压报警（<0.3MPa）
 signal: 传输至BMS和护士站

 vacuum_system:

 source:
 type: 真空泵组（3台轮换）
 location: 医用气体站房
 power: 15-30kW

 distribution:
 material: 脱脂铜管
 main_size: DN40
 branch_size: DN25
 location: 与氧气管平行但分开

 terminal_in_room:
 quantity: 4
 locations:
 - 手术操作区×2
 - 麻醉区×2
 height: 1500mm
 pressure: -0.04±0.01 MPa
 flow_capacity: 60 L/min

 pollution_control:
 liquid_trap:
 location: 终端前端
 function: 防止液体进入管道
 filter:
 location: 真空泵入口
 function: 过滤杂质

 compressed_air_system:

 source:
 type: 无油空气压缩机
 location: 医用气体站房

 terminal_in_room:
 quantity: 2
 location: 麻醉区
 pressure: 0.4 MPa

 nitrous_oxide_system:

 source:
 type: 高压气瓶汇流排
 location: 医用气体站房

 terminal_in_room:
 quantity: 1
 location: 麻醉区
 optional: true

 scavenging:
 connection: 麻醉机废气出口
 routing: 独立管道至排风系统
 discharge: 屋顶高空排放

 gas_alarm_panel:

 location: 手术区护士站
 display:
 - 各气体压力状态
 - 正常/报警指示
 - 区域开关状态
 alarm:
 type: 声光报警
 conditions:
 - 压力过低
 - 压力过高
 - 系统故障

 # ────────────────────────────────────────────────────────────────────────
 # 电气系统-空间耦合
 # ────────────────────────────────────────────────────────────────────────
 electrical_space_coupling:

 room_type: ROOM-OR-I

 power_distribution_path:

 source:
 type: 低压配电室
 location: 建筑地下层或首层

 distribution_levels:
 level_1:
 type: 低压配电柜
 location: 低压配电室

 level_2:
 type: 楼层配电箱
 location: 手术区电气间
 distance_to_room: ≤30m

 level_3:
 type: 隔离变压器
 location: 手术区电气间或走廊配电柜
 capacity: 8-10kVA
 function: IT隔离电源

 level_4:
 type: 房间配电箱
 location: 手术室入口门旁墙内
 access: 检修门
 contents:
 - 隔离电源回路开关
 - 普通电源回路开关
 - 绝缘监视仪

 cable_routing:

 vertical:
 location: 电气竖井
 tray_size: 600mm宽电缆桥架
 separation: 强弱电分离

 horizontal:
 location: 吊顶内电缆桥架
 height: 距结构板300mm

 to_room:
 method: PVC管穿墙
 conduit_size: DN25-50
 fire_seal: 防火封堵

 socket_installation:

 medical_socket:
 circuit: 隔离电源IT系统
 quantity: 12
 installations:
 - location: 手术台周围墙面
 count: 4
 height: 300-500mm
 mounting: 暗装

 - location: 麻醉区墙面
 count: 3
 height: 500-1000mm

 - location: 器械区墙面
 count: 2
 height: 500mm

 - location: 吊塔
 count: 3

 general_socket:
 circuit: 普通供电
 quantity: 8
 location: 辅助区域墙面

 equipotential_bonding:

 bonding_bar:
 location: 房间配电箱内或墙面明装
 material: 铜排

 bonding_terminals:
 quantity: 8
 locations:
 - 手术台区域：4个
 - 设备区域：4个
 height: 300mm

 bonding_conductors:
 material: ≥6mm²铜软线
 color: 黄绿双色

 connected_items:
 - 手术台金属框架
 - 无影灯金属部分
 - 所有医疗设备金属外壳
 - 金属管道
 - 吊顶金属龙骨

 resistance_requirement: ≤0.1Ω

 insulation_monitoring:

 device: 绝缘监视仪
 location: 房间配电箱内
 display: 房间入口处
 alarm_threshold: 50kΩ
 alarm_type: 声光报警

 emergency_power:

 ups:
 capacity: 8kVA
 location: UPS室（手术区）
 backup_time: ≥30min
 protected_circuits:
 - 手术灯
 - 监护仪
 - 麻醉机
 - 应急照明

 generator_backup:
 transfer_time: ≤0.5s（ATS切换）

 lighting:

 general_lighting:
 type: LED洁净灯
 illuminance: 500 lux
 quantity: 6
 location: 吊顶嵌入式
 circuit: 独立回路
 control: 入口处开关

 surgical_lighting:
 type: 无影灯
 circuit: 隔离电源
 control: 面板/脚踏

 emergency_lighting:
 type: 蓄电池应急灯
 illuminance: ≥50 lux
 quantity: 2
 duration: ≥90min
 location: 入口处+手术台上方

 # ────────────────────────────────────────────────────────────────────────
 # 给排水系统-空间耦合
 # ────────────────────────────────────────────────────────────────────────
 plumbing_space_coupling:

 room_type: ROOM-OR-I

 water_supply:

 source: 医院给水系统

 distribution:
 vertical_riser:
 location: 给排水竖井
 material: 不锈钢管

 horizontal_branch:
 location: 吊顶内

 terminal_in_room:
 type: 不锈钢洗手池
 quantity: 0（刷手间在室外）
 note: 手术室内一般不设洗手池

 drainage:

 floor_drain:
 quantity: 2
 locations:
 - position: 手术台下方区域
 purpose: 手术污水排放
 - position: 入口附近
 purpose: 清洁用水排放
 specifications:
 type: 防臭地漏
 size: DN75
 trap: 水封≥50mm

 floor_slope:
 gradient: ≥0.5%
 direction: 坡向地漏

 drainage_pipe:
 location: 地下暗敷
 material: UPVC
 connection: 至污水立管

 sterile_water:

 supply: 来自灭菌供水系统（可选）
 terminal: 手术室内或相邻储存
 use: 手术冲洗用水

 # ────────────────────────────────────────────────────────────────────────
 # 消防系统-空间耦合
 # ────────────────────────────────────────────────────────────────────────
 fire_protection_space_coupling:

 room_type: ROOM-OR-I

 fire_detection:

 smoke_detector:
 quantity: 2
 location: 吊顶嵌入
 spacing: ≤保护半径
 type: 感烟探测器
 note: 洁净区使用抽样式或特殊类型

 manual_call_point:
 location: 手术区走廊
 height: 1400mm

 fire_suppression:

 preferred_system: 气体灭火

 gas_suppression:
 agent: 七氟丙烷或IG541
 storage:
 location: 手术区灭火气体储存间
 distance: ≤50m
 distribution:
 pipe: 镀锌钢管
 routing: 吊顶内至房间
 nozzle:
 quantity: 4-6
 location: 吊顶均匀分布
 coverage: 全覆盖
 integration:
 hvac_shutdown: 灭火时自动关闭HVAC
 door_release: 门禁解除
 alarm: 声光警报

 alternative_sprinkler:
 condition: 如无气体灭火
 type: 快速响应喷头
 temperature_rating: 68°C

 evacuation:

 exit_doors:
 quantity: ≥2
 width: ≥900mm
 type: 自闭防火门

 exit_signage:
 location: 出口上方
 type: 电光源疏散指示

 emergency_lighting:
 coverage: 疏散通道全覆盖

 # ────────────────────────────────────────────────────────────────────────
 # 楼宇自控系统-空间耦合
 # ────────────────────────────────────────────────────────────────────────
 building_automation_coupling:

 room_type: ROOM-OR-I

 sensor_deployment:

 temperature_sensor:
 quantity: 1
 location: 房间中部墙面
 height: 1500mm
 type: PT100
 accuracy: ±0.3°C
 signal: 4-20mA或Modbus

 humidity_sensor:
 quantity: 1
 location: 与温度传感器组合
 accuracy: ±3%RH

 pressure_sensor:
 quantity: 1
 location: 侧墙中部
 height: 1500mm
 range: -100 to +100 Pa
 accuracy: ±1Pa
 reference: 走廊（测量压差）

 particle_counter:
 quantity: 1
 location: 手术区域
 optional: true
 function: 洁净度实时监测

 door_contact:
 quantity: 2
 location: 入口门+紧急出口门
 function: 门状态监测

 actuator_deployment:

 supply_air_damper:
 location: 送风管分支处
 type: 电动调节阀
 function: 调节送风量
 signal: 0-10V

 return_air_damper:
 location: 回风管分支处
 function: 调节回风量

 pressure_relief_damper:
 location: 排风管
 function: 维持正压

 chw_valve:
 location: 空调机组冷水管
 type: 电动二通阀
 function: 温度调节

 hw_valve:
 location: 空调机组热水管
 type: 电动二通阀
 function: 冬季供热

 control_panels:

 room_display:
 location: 入口门旁墙面
 height: 1400mm
 display_content:
 - 温度当前值/设定值
 - 湿度当前值/设定值
 - 压差当前值
 - 系统状态
 controls:
 - 温度设定调节
 - 灯光控制（可选）
 alarms:
 - 温度超限
 - 湿度超限
 - 压差不足
 - 设备故障

 nurse_station_display:
 location: 手术区护士站
 display: 所有手术室状态汇总
 functions:
 - 实时监测
 - 历史曲线
 - 报警处理
 - 维护提醒

 data_transmission:

 field_bus:
 type: Modbus RTU或BACnet MS/TP
 cable: 屏蔽双绞线
 routing: 弱电桥架

 controller:
 type: DDC控制器
 location: 手术区弱电间
 function: 采集数据、执行控制逻辑

 integration:
 to_bms: 网络上传至中央BMS服务器
 to_his: 可选集成至医院信息系统
 data_storage: ≥1年历史数据

# ════════════════════════════════════════════════════════════════════════════
# 第八部分：信息系统与空间耦合模型（v1.2新增）
# ════════════════════════════════════════════════════════════════════════════
information_system_space_coupling:

 model_description: |
 本模型定义医院信息系统基础设施与建筑空间的关系。
 包括IT基础设施、网络布线、医疗物联网、远程医疗等。
 为Agent-05和Agent-08提供信息化系统的空间需求。

 # ────────────────────────────────────────────────────────────────────────
 # IT基础设施
 # ────────────────────────────────────────────────────────────────────────
 it_infrastructure:

 data_center:

 room_type: ROOM-MEP-IT

 location_requirements:
 building: 医技楼或综合楼中部
 floor: 1-3层（便于布线和维护）
 proximity: 靠近主干竖井
 avoidance:
 - 水管上方
 - 外墙（防止渗水）
 - 振动源附近

 area_calculation:
 formula: "面积(m²) = 床位数 × 0.05 + 基础面积50m²"
 example_1500_beds: 125 # m²

 space_layout:
 zones:
 - zone: 主机房区
 function: 服务器、存储、网络设备
 area_ratio: 60%

 - zone: UPS电池区
 function: UPS及电池组
 area_ratio: 20%
 fire_separation: 独立防火分区

 - zone: 监控操作区
 function: 值班监控
 area_ratio: 15%

 - zone: 备件储存
 area_ratio: 5%

 environmental_requirements:
 temperature:
 setpoint: 23±2°C
 control: 精密空调
 humidity:
 setpoint: 45-55%RH
 air_changes: 30 ACH
 cleanliness: 万级

 power_requirements:
 power_density: 2-3 # kW/m²
 redundancy: N+1或2N
 ups:
 capacity: 覆盖全部IT设备
 autonomy: 30-60min
 generator: 柴发备电

 cooling_requirements:
 type: 精密空调（机房专用）
 configuration: N+1冗余
 cooling_capacity: 3×IT负载

 cable_management:
 floor_type: 防静电架空地板
 floor_height: 400-600mm
 cable_routing:
 - 强电在地板下
 - 弱电在架空地板下或桥架
 separation: 强弱电分离≥300mm

 fire_protection:
 detection: 极早期烟雾探测
 suppression: 气体灭火（七氟丙烷或IG541）

 access_control:
 type

---