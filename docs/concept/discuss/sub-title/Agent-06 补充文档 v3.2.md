## 🧑‍💻 User


继续，你卡在了【sub_tests:
 - id: "01-A"
 name: "室温传感器精度"
 procedure:
 - "使用校准过的便携温度计（精度±0.1°C）"
 - "在手术室内4个位置测量温度"
 - "位置：头部区、脚部区、中部、靠墙侧"
 - "每个位置稳定10分钟后读数"
 - "记录BMS显示值和实测值"
 acceptance: "|BMS值 - 实测值| ≤ 0.5°C"
 result】

---
## 🤖 Assistant


继续生成SAT验收测试清单及后续补充内容。

---

```yaml
            result:
              location_1_head:
                bms_reading: "____°C"
                measured: "____°C"
                deviation: "____°C"
                pass_fail: "☐ PASS  ☐ FAIL"
              location_2_foot:
                bms_reading: "____°C"
                measured: "____°C"
                deviation: "____°C"
                pass_fail: "☐ PASS  ☐ FAIL"
              location_3_center:
                bms_reading: "____°C"
                measured: "____°C"
                deviation: "____°C"
                pass_fail: "☐ PASS  ☐ FAIL"
              location_4_wall:
                bms_reading: "____°C"
                measured: "____°C"
                deviation: "____°C"
                pass_fail: "☐ PASS  ☐ FAIL"
                
          - id: "01-B"
            name: "压差传感器精度"
            procedure:
              - "使用校准过的微压计（精度±0.5Pa）"
              - "在门缝位置测量实际压差"
              - "记录BMS显示的压差值"
              - "双传感器均需验证"
            acceptance: "|BMS值 - 实测值| ≤ 2Pa"
            result:
              sensor_A:
                bms_reading: "____Pa"
                measured: "____Pa"
                deviation: "____Pa"
                pass_fail: "☐ PASS  ☐ FAIL"
              sensor_B:
                bms_reading: "____Pa"
                measured: "____Pa"
                deviation: "____Pa"
                pass_fail: "☐ PASS  ☐ FAIL"
                
          - id: "01-C"
            name: "湿度传感器精度"
            procedure:
              - "使用校准过的湿度计（精度±2%RH）"
              - "在房间中部测量"
              - "传感器与实测值对比"
            acceptance: "|BMS值 - 实测值| ≤ 5%RH"
            result:
              bms_reading: "____%RH"
              measured: "____%RH"
              deviation: "____%RH"
              pass_fail: "☐ PASS  ☐ FAIL"
              
          - id: "01-D"
            name: "送风温度传感器精度"
            procedure:
              - "在送风口附近用温度计测量"
              - "对比BMS送风温度显示值"
            acceptance: "|BMS值 - 实测值| ≤ 0.5°C"
            result:
              bms_reading: "____°C"
              measured: "____°C"
              pass_fail: "☐ PASS  ☐ FAIL"
              
      TEST_02:
        name: "控制回路响应测试"
        objective: "验证温度、压差控制回路的响应性和稳定性"
        
        sub_tests:
          - id: "02-A"
            name: "温度阶跃响应"
            procedure:
              - "确保系统在稳态运行（温度波动<0.5°C）"
              - "记录当前设定值和实际温度"
              - "在BMS上将温度设定值从22°C改为20°C"
              - "每1分钟记录一次室温"
              - "记录30分钟或直到稳定"
              - "绘制响应曲线"
            measurements:
              initial_setpoint: "22°C"
              final_setpoint: "20°C"
              time_log: |
                时间(min) | 室温(°C) | 送风温度(°C) | 冷水阀位(%)
                0         | ____     | ____         | ____
                5         | ____     | ____         | ____
                10        | ____     | ____         | ____
                15        | ____     | ____         | ____
                20        | ____     | ____         | ____
                25        | ____     | ____         | ____
                30        | ____     | ____         | ____
            acceptance:
              settling_time: "< 30分钟"
              overshoot: "< 2°C"
              steady_state_error: "< 0.5°C"
            result:
              actual_settling_time: "____分钟"
              actual_overshoot: "____°C"
              actual_error: "____°C"
              pass_fail: "☐ PASS  ☐ FAIL"
              
          - id: "02-B"
            name: "压差控制稳定性"
            procedure:
              - "确保系统稳态运行"
              - "记录30分钟的压差数据（BMS趋势，1秒采样）"
              - "导出数据进行统计分析"
            measurements:
              recording_duration: "30分钟"
              sample_interval: "1秒"
              data_points: "1800点"
            analysis:
              mean: "____Pa"
              std_deviation: "____Pa"
              max_value: "____Pa"
              min_value: "____Pa"
              range: "____Pa"
            acceptance:
              mean: "15±2Pa"
              std_dev: "< 2Pa"
              max_deviation: "< 5Pa"
            result:
              pass_fail: "☐ PASS  ☐ FAIL"
              
          - id: "02-C"
            name: "湿度控制响应"
            procedure:
              - "记录当前湿度设定值和实际值"
              - "将湿度设定值从50%改为55%"
              - "记录湿度变化直到稳定"
            acceptance:
              settling_time: "< 60分钟"
              steady_state_error: "< 3%RH"
            result:
              actual_settling_time: "____分钟"
              actual_error: "____%RH"
              pass_fail: "☐ PASS  ☐ FAIL"
              
      TEST_03:
        name: "开门扰动补偿测试"
        objective: "验证开门时压差能快速恢复"
        
        procedure:
          - "确保压差稳定在+15Pa左右"
          - "启动BMS趋势记录（1秒采样）"
          - "快速打开手术室主门（约3秒）"
          - "保持门开10秒"
          - "关闭门"
          - "继续记录60秒"
          - "分析压差变化曲线"
        
        measurements:
          before_open: "____Pa"
          min_during_open: "____Pa"
          time_to_min: "____秒"
          after_close_30s: "____Pa"
          after_close_60s: "____Pa"
          
        acceptance:
          max_drop: "不低于+5Pa"
          recovery_time: "门关后30秒内恢复到+12Pa以上"
          
        result:
          actual_min: "____Pa"
          actual_recovery_time: "____秒"
          pass_fail: "☐ PASS  ☐ FAIL"
          
      TEST_04:
        name: "模式切换测试"
        objective: "验证FSM状态机各模式切换正确"
        
        sub_tests:
          - id: "04-A"
            name: "值班→手术模式"
            procedure:
              - "将系统设置为值班模式"
              - "确认设定值：温度26°C，压差+8Pa"
              - "触发手术模式（按面板按钮或BMS指令）"
              - "记录切换过程"
            observations:
              - "送风量是否逐步增加到100%？ ☐ 是  ☐ 否"
              - "温度设定值是否切换到22°C？ ☐ 是  ☐ 否"
              - "压差设定值是否切换到+15Pa？ ☐ 是  ☐ 否"
              - "切换过程是否平滑无抖动？ ☐ 是  ☐ 否"
            transition_time: "____分钟"
            pass_fail: "☐ PASS  ☐ FAIL"
            
          - id: "04-B"
            name: "手术→消毒模式"
            procedure:
              - "在手术模式稳定运行"
              - "触发消毒模式"
              - "观察消毒序列执行"
            observations:
              phase_1_self_clean:
                duration: "____分钟"
                fresh_air: "100%？ ☐ 是  ☐ 否"
              phase_2_disinfection:
                duration: "____分钟"
                dampers_closed: "☐ 是  ☐ 否"
                uv_lamp_on: "☐ 是  ☐ 否"
              phase_3_exhaust:
                duration: "____分钟"
                full_ventilation: "☐ 是  ☐ 否"
            pass_fail: "☐ PASS  ☐ FAIL"
            
      TEST_05:
        name: "网络中断孤岛模式测试"
        objective: "验证DDC断网后能维持本地控制"
        
        procedure:
          - "确保系统在手术模式稳定运行"
          - "记录当前各参数"
          - "断开DDC的网络连接（拔网线，保持电源）"
          - "观察30分钟"
          - "每5分钟记录温度、压差"
          - "恢复网络连接"
          - "验证数据同步"
          
        measurements:
          before_disconnect:
            room_temp: "____°C"
            supply_temp: "____°C"
            pressure: "____Pa"
            chw_valve: "____%"
            
          during_offline_5min: "____°C / ____Pa"
          during_offline_10min: "____°C / ____Pa"
          during_offline_15min: "____°C / ____Pa"
          during_offline_20min: "____°C / ____Pa"
          during_offline_25min: "____°C / ____Pa"
          during_offline_30min: "____°C / ____Pa"
          
        acceptance:
          temp_deviation: "< 1°C from setpoint"
          pressure_deviation: "维持正压>+10Pa"
          no_equipment_stop: "设备不应停机"
          alarm_generated: "应有通信中断报警"
          data_sync_after_reconnect: "离线数据应补传"
          
        result:
          temp_maintained: "☐ PASS  ☐ FAIL"
          pressure_maintained: "☐ PASS  ☐ FAIL"
          alarm_received: "☐ PASS  ☐ FAIL"
          data_synced: "☐ PASS  ☐ FAIL"
          overall: "☐ PASS  ☐ FAIL"
          
      TEST_06:
        name: "传感器故障切换测试"
        objective: "验证双传感器冗余切换逻辑"
        
        sub_tests:
          - id: "06-A"
            name: "室温传感器A故障"
            procedure:
              - "系统使用传感器A作为主传感器"
              - "断开传感器A接线"
              - "观察系统响应"
            observations:
              - "是否在5秒内检测到故障？ ☐ 是  ☐ 否"
              - "是否自动切换到传感器B？ ☐ 是  ☐ 否"
              - "是否产生HIGH报警？ ☐ 是  ☐ 否"
              - "控制是否继续正常？ ☐ 是  ☐ 否"
            pass_fail: "☐ PASS  ☐ FAIL"
            
          - id: "06-B"
            name: "压差传感器双故障"
            procedure:
              - "依次断开两个压差传感器"
              - "观察系统降级响应"
            observations:
              - "是否切换到固定排风阀开度（30%）？ ☐ 是  ☐ 否"
              - "是否产生CRITICAL报警？ ☐ 是  ☐ 否"
            pass_fail: "☐ PASS  ☐ FAIL"
            
      TEST_07:
        name: "启动/停止序列测试"
        objective: "验证AHU启动和停止序列正确执行"
        
        sub_tests:
          - id: "07-A"
            name: "冷态启动序列"
            procedure:
              - "确保AHU完全停止"
              - "发送启动命令"
              - "逐步记录启动序列"
            sequence_verification:
              - step: "冷冻水系统就绪确认"
                observed: "☐ 执行  ☐ 跳过"
                time: "____"
              - step: "新风阀开至10%"
                observed: "☐ 执行  ☐ 跳过"
                time: "____"
              - step: "冷水阀预定位30%"
                observed: "☐ 执行  ☐ 跳过"
                time: "____"
              - step: "送风机启动"
                observed: "☐ 执行  ☐ 跳过"
                time: "____"
              - step: "排风机启动"
                observed: "☐ 执行  ☐ 跳过"
                time: "____"
              - step: "压差控制使能"
                observed: "☐ 执行  ☐ 跳过"
                time: "____"
              - step: "新风阀逐步开大"
                observed: "☐ 执行  ☐ 跳过"
                time: "____"
              - step: "温湿度控制使能"
                observed: "☐ 执行  ☐ 跳过"
                time: "____"
            total_startup_time: "____分钟"
            pass_fail: "☐ PASS  ☐ FAIL"
            
          - id: "07-B"
            name: "正常停机序列"
            procedure:
              - "系统稳态运行中"
              - "发送停机命令"
              - "记录停机顺序"
            sequence_verification:
              - step: "温湿度控制禁用"
                observed: "☐ 执行  ☐ 跳过"
              - step: "新风阀关至10%"
                observed: "☐ 执行  ☐ 跳过"
              - step: "冷水阀关闭"
                observed: "☐ 执行  ☐ 跳过"
              - step: "热水阀开启（防冻）"
                observed: "☐ 执行  ☐ 跳过"
              - step: "排风机停止"
                observed: "☐ 执行  ☐ 跳过"
              - step: "送风机停止"
                observed: "☐ 执行  ☐ 跳过"
              - step: "新风阀关闭"
                observed: "☐ 执行  ☐ 跳过"
            pass_fail: "☐ PASS  ☐ FAIL"
            
      TEST_08:
        name: "消防联动测试"
        objective: "验证火警时AHU正确响应"
        
        procedure:
          - "协调消防调试单位"
          - "触发测试火警信号（到该区域）"
          - "观察AHU响应"
          
        observations:
          - "AHU是否停止？ ☐ 是  ☐ 否"
          - "新风阀是否关闭？ ☐ 是  ☐ 否"
          - "防火阀是否动作？ ☐ 是  ☐ 否"
          - "响应时间是否<30秒？ ☐ 是  ☐ 否"
          - "BMS是否收到联动状态？ ☐ 是  ☐ 否"
          
        recovery_test:
          - "复位火警信号"
          - "手动确认安全后重启AHU"
          - "验证系统恢复正常"
          
        pass_fail: "☐ PASS  ☐ FAIL"
        
    # ─────────────────────────────────────────────────────────────────────
    # 测试总结
    # ─────────────────────────────────────────────────────────────────────
    test_summary:
      test_date_start: "____________"
      test_date_end: "____________"
      
      total_tests: 8
      total_sub_tests: 16
      
      results:
        passed: "____"
        failed: "____"
        not_tested: "____"
        
      failed_items:
        description: |
          列出未通过项目及原因：
          1. ________________________________
          2. ________________________________
          3. ________________________________
          
      corrective_actions:
        description: |
          针对未通过项的整改措施：
          1. ________________________________
          2. ________________________________
          3. ________________________________
          
      retest_required: "☐ 是  ☐ 否"
      retest_date: "____________"
      
    # ─────────────────────────────────────────────────────────────────────
    # 签字确认
    # ─────────────────────────────────────────────────────────────────────
    approvals:
      contractor_engineer:
        name: "________________"
        company: "________________"
        signature: "________________"
        date: "____________"
        
      hospital_engineer:
        name: "________________"
        department: "工程设备科"
        signature: "________________"
        date: "____________"
        
      commissioning_agent:
        name: "________________"
        company: "________________"
        signature: "________________"
        date: "____________"
        
      project_manager:
        name: "________________"
        signature: "________________"
        date: "____________"
```

---

# 补充E：极端工况控制策略 (P2)

```yaml
Extreme_Operating_Conditions:
  
  # ═══════════════════════════════════════════════════════════════════════════
  # E.1 极端高温工况
  # ═══════════════════════════════════════════════════════════════════════════
  
  EXTREME_HEAT_WAVE:
    id: "EOC-001"
    name: "极端高温工况"
    
    trigger:
      condition: "室外湿球温度 > 28°C 持续 > 4小时"
      OR: "室外干球温度 > 38°C"
      data_source: "室外气象站"
      
    impact_assessment:
      cooling_capacity:
        description: "冷却塔效率下降，冷机冷凝温度升高"
        capacity_reduction: "10-20%"
      chiller_efficiency:
        description: "冷机COP下降"
        cop_reduction: "15-25%"
      terminal_comfort:
        description: "末端可能无法维持设定温度"
        risk: "HIGH"
        
    control_response:
      
      phase_1_pre_cooling:
        trigger: "天气预报预测高温"
        timing: "高温到来前12小时"
        actions:
          - action: "夜间深度预冷建筑"
            setpoint: "温度设定降低2°C"
            duration: "夜间低电价时段"
          - action: "蓄冷系统满蓄（如配置）"
          - action: "检查备用冷机状态"
            
      phase_2_peak_management:
        trigger: "进入高温时段"
        actions:
          - action: "优先保障关键区域"
            priority_sequence:
              1: "手术室"
              2: "ICU"
              3: "产房/新生儿"
              4: "住院病房"
              5: "门诊"
              6: "办公/后勤"
              
          - action: "冷冻水温度下调"
            from: "7°C"
            to: "6°C"
            note: "增加除湿能力和冷量传递"
            
          - action: "末端温度设定值调整"
            OR_setpoint: "22→23°C（不超过25°C）"
            ICU_setpoint: "24→25°C"
            general_setpoint: "26→27°C"
            
          - action: "非关键区域限制冷量"
            method: "限制冷水阀最大开度80%"
            areas: ["办公区", "走廊", "大厅"]
            
          - action: "增加冷却塔风机频率"
            target: "100%"
            
          - action: "启动所有可用冷机"
            staging: "按需全开"
            
      phase_3_emergency:
        trigger: "手术室温度 > 25°C"
        actions:
          - action: "紧急通知"
            recipients: ["手术室护士长", "设备科长", "值班院长"]
            content: "手术室温度超限，请评估手术安排"
            
          - action: "临时措施"
            options:
              - "部署移动式冷风机"
              - "冰块物理降温"
              - "调整手术排班避开高峰时段"
              
    recovery:
      trigger: "室外温度回落到正常范围"
      actions:
        - "逐步恢复正常设定值"
        - "记录事件日志"
        - "分析系统表现，优化预案"
        
  # ═══════════════════════════════════════════════════════════════════════════
  # E.2 极端低温工况
  # ═══════════════════════════════════════════════════════════════════════════
  
  EXTREME_COLD_SNAP:
    id: "EOC-002"
    name: "极端低温工况"
    
    trigger:
      condition: "室外温度 < -10°C 持续 > 6小时"
      OR: "室外温度 < -15°C"
      
    impact_assessment:
      freeze_risk:
        locations: ["新风段表冷器", "屋顶管道", "外墙水管"]
        severity: "CRITICAL"
      heating_capacity:
        description: "热负荷大增，可能供热不足"
        risk: "HIGH"
        
    control_response:
      
      freeze_protection:
        priority: "HIGHEST"
        actions:
          - action: "确认所有防冻开关正常"
            check_points: ["AHU新风段", "PAU", "屋顶设备"]
            
          - action: "新风量最小化"
            method: "关小新风阀，仅维持最小新风量"
            OR_fresh_air: "维持30%（洁净度需要）"
            general_fresh_air: "可降至设计值50%"
            
          - action: "热水阀预开"
            condition: "混风温度 < 10°C"
            action: "热水阀最小开度20%"
            
          - action: "全热交换器效率最大化"
            method: "ERV风机全速"
            bypass: "关闭旁通"
            
          - action: "监控关键点温度"
            points:
              - "新风段盘管后温度"
              - "混风温度"
              - "回水温度"
            alarm: "任一点 < 5°C 立即报警"
            
      heating_priority:
        actions:
          - action: "锅炉全出力"
          - action: "优先供应医疗区域"
          - action: "非关键区域温度设定下调"
            office: "22→20°C"
            lobby: "20→18°C"
            
    emergency_response:
      trigger: "防冻开关动作 OR 盘管温度 < 3°C"
      actions:
        - "立即关闭新风阀"
        - "停止送风机"
        - "热水阀全开"
        - "派人现场检查"
        - "确认无冻裂后方可恢复"
        
  # ═══════════════════════════════════════════════════════════════════════════
  # E.3 高负荷工况
  # ═══════════════════════════════════════════════════════════════════════════
  
  HIGH_LOAD_SCENARIO:
    id: "EOC-003"
    name: "超高负荷工况"
    
    trigger:
      condition: "手术部 > 80% 手术室同时使用"
      OR: "系统冷负荷 > 90% 设计容量"
      duration: "> 2小时"
      
    control_response:
      actions:
        - action: "启动所有备用冷机"
        - action: "冷冻水温度降至最低（6°C）"
        - action: "需求响应"
          method: "按优先级限制非关键区域"
        - action: "通知运维值班"
          content: "系统接近满负荷，请关注"
          
  # ═══════════════════════════════════════════════════════════════════════════
  # E.4 完全停电工况
  # ═══════════════════════════════════════════════════════════════════════════
  
  TOTAL_BLACKOUT:
    id: "EOC-004"
    name: "完全停电工况"
    
    trigger: "市电失电 AND 柴油发电机未能启动"
    duration_scenario: "可能持续数小时"
    
    phases:
      
      phase_1_immediate:
        duration: "0-10分钟"
        situation: "UPS供电关键负载"
        control_response:
          - "L3硬件保护生效"
            - "防冻开关：如温度<5°C，热水阀机械开启"
            - "弹簧复位：阀门回到安全位置"
          - "DDC掉电，无控制输出"
          - "医疗设备靠UPS/电池运行"
        operational_response:
          - "手术室团队评估是否终止手术"
          - "通知所有病区准备应急"
          
      phase_2_extended:
        duration: "10-30分钟"
        situation: "UPS电池耗尽"
        control_response:
          - "所有自动控制停止"
          - "阀门保持在弹簧复位位置"
          - "医疗设备需人工操作"
        operational_response:
          - "手动隔离手术室（关门保持残余正压）"
          - "使用手电筒照明"
          - "医用气体靠储罐/钢瓶供应"
          
      phase_3_recovery:
        trigger: "电力恢复"
        control_response:
          - "DDC上电自检"
          - "按预设顺序启动设备"
            sequence:
              1: "冷热源系统"
              2: "关键区域AHU（手术室、ICU）"
              3: "普通区域AHU"
          - "逐步恢复控制回路"
          - "验证所有参数后投入自动"
        operational_response:
          - "巡检所有系统状态"
          - "确认无设备损坏"
          - "报告恢复正常"
```

---

# 补充F：分户计量与权限管理 (P2)

```yaml
Metering_And_Authorization:
  
  # ═══════════════════════════════════════════════════════════════════════════
  # F.1 分户计量逻辑
  # ═══════════════════════════════════════════════════════════════════════════
  
  Metering_Framework:
    
    principle: |
      按"医疗科室"维度统计能耗，支持部门级成本核算。
      分户计量基于以下层级：
      - L1: 全院总量
      - L2: 楼栋/分区
      - L3: 科室/部门
      - L4: 特定设备（可选）
      
    # ─────────────────────────────────────────────────────────────────────
    # 虚拟电表
    # ─────────────────────────────────────────────────────────────────────
    virtual_electricity_meters:
      
      - meter_id: "VEM-OR-DEPT"
        name: "手术部电能计量"
        scope: "手术部所有用电设备"
        method: |
          汇总手术部配电回路电表：
          E_total = Σ E_sub_meter_i
        sub_meters:
          - "手术室照明回路"
          - "手术室设备回路"
          - "手术部空调回路（AHU用电）"
          - "手术部医疗设备回路"
        output:
          daily_kwh: "每日累计"
          monthly_kwh: "每月累计"
          power_demand_kw: "峰值功率"
          
      - meter_id: "VEM-ICU-DEPT"
        name: "ICU电能计量"
        scope: "ICU所有用电"
        sub_meters:
          - "ICU照明"
          - "ICU设备"
          - "ICU空调"
          - "ICU医疗设备"
          
      - meter_id: "VEM-WARD-A"
        name: "住院楼A电能计量"
        scope: "住院楼A全部"
        # ... 类似结构
        
    # ─────────────────────────────────────────────────────────────────────
    # 虚拟冷量表
    # ─────────────────────────────────────────────────────────────────────
    virtual_cooling_meters:
      
      - meter_id: "VCM-OR-DEPT"
        name: "手术部冷量计量"
        method: |
          基于AHU冷量计算：
          Q = Σ Q_AHU_i
          Q_AHU = ρ × V × Cp × (T_return - T_supply)
        data_sources:
          - AHU_flow: "送风量（或估算）"
          - T_return: "回风温度"
          - T_supply: "送风温度"
        output:
          daily_kwh: "每日冷量 (kWh)"
          monthly_kwh: "每月冷量"
          peak_load_kw: "峰值冷负荷"
        accuracy: "±10%（取决于送风量测量精度）"
        
      - meter_id: "VCM-ICU-DEPT"
        name: "ICU冷量计量"
        # 类似结构
        
    # ─────────────────────────────────────────────────────────────────────
    # 计量数据应用
    # ─────────────────────────────────────────────────────────────────────
    analytics:
      
      department_ranking:
        name: "科室能耗排名"
        metrics:
          - "每月电耗 kWh"
          - "每月冷量 kWh"
          - "单位面积能耗 kWh/m²"
          - "单位床位能耗 kWh/床"
        output: "月度报表Top N"
        
      trend_analysis:
        name: "能耗趋势分析"
        comparisons:
          - "同比（去年同期）"
          - "环比（上月）"
          - "与基准对比"
        alerts:
          warning: "环比增长 > 10%"
          investigate: "同比增长 > 20%"
          
      cost_allocation:
        name: "成本分摊"
        method: |
          将冷站/热源的运行成本按冷量/热量比例分摊：
          Cost_dept = Cost_total × (Q_dept / Q_total)
        frequency: "月度"
        
  # ═══════════════════════════════════════════════════════════════════════════
  # F.2 权限管理
  # ═══════════════════════════════════════════════════════════════════════════
  
  Authorization_Matrix:
    
    levels:
      
      Level_1_Local_Operator:
        name: "本地操作员"
        typical_users:
          - "手术室护士"
          - "病房护士"
          - "门诊护士"
        access_location: "各科室本地面板/触摸屏"
        
        capabilities:
          can_do:
            - "查看本科室环境参数（温度、湿度、压差）"
            - "调节温度设定值 ±2°C（在预设范围内）"
              - "手术室：21-27°C"
              - "病房：22-26°C"
            - "查看当前运行模式"
            - "发起报修请求"
            
          cannot_do:
            - "更改其他科室设定"
            - "更改压差设定值"
            - "更改运行模式（需授权）"
            - "启停设备"
            
        interface: "本地触摸屏 或 Web门户（只读+有限调节）"
        
      Level_2_Building_Engineer:
        name: "楼宇工程师"
        typical_users:
          - "中控室值班员"
          - "设备科运维人员"
        access_location: "中央控制室 / 工程部"
        
        capabilities:
          can_do:
            - "查看全院所有参数"
            - "手动启停末端设备（AHU、FCU）"
            - "调节冷站参数（冷冻水温度等）"
            - "确认报警"
            - "生成运行报表"
            - "查看历史趋势"
            - "修改时间程序（经审批）"
            
          cannot_do:
            - "修改控制逻辑/PID参数"
            - "修改消防联动设置"
            - "修改安全相关参数"
            
        interface: "SCADA工作站"
        
      Level_3_System_Administrator:
        name: "系统管理员"
        typical_users:
          - "设备科长"
          - "信息科负责人"
        access_location: "工程部办公室 / 远程VPN"
        
        capabilities:
          can_do:
            - "Level_2所有权限"
            - "修改所有控制参数（PID等）"
            - "修改报警阈值"
            - "修改用户权限"
            - "备份/恢复配置"
            - "系统固件升级（经审批）"
            
          cannot_do:
            - "修改消防联动逻辑（需消防部门）"
            
        authorization: "需部门负责人审批"
        audit: "所有操作记录"
        
      Level_4_Factory_Engineer:
        name: "厂家工程师"
        typical_users:
          - "控制系统供应商技术人员"
        access_location: "VPN远程 或 现场"
        
        capabilities:
          can_do:
            - "故障诊断"
            - "程序调试"
            - "固件升级"
            - "高级参数修改"
            
        restrictions:
          duration: "仅维保期内或按合同"
          authorization: "每次访问需医院授权"
          supervision: "建议有医院人员陪同"
          
    # ─────────────────────────────────────────────────────────────────────
    # 权限实现
    # ─────────────────────────────────────────────────────────────────────
    implementation:
      
      authentication:
        method: "用户名/密码 + 可选2FA"
        integration: "与医院AD/LDAP集成"
        session_timeout: "15分钟无操作自动登出"
        
      authorization:
        method: "基于角色的访问控制（RBAC）"
        granularity:
          - "按系统（HVAC/ELEC/MGAS...）"
          - "按区域（手术部/ICU/病房...）"
          - "按操作类型（只读/可写/控制）"
          
      audit_trail:
        content:
          - "用户ID"
          - "操作时间"
          - "操作内容"
          - "操作前值"
          - "操作后值"
          - "操作IP地址"
        retention: "至少3年"
        tamper_proof: "日志不可删除/修改"
```

---

# 补充G：下游Agent交接计划 (P2)

```yaml
Downstream_Handover:
  
  # ═══════════════════════════════════════════════════════════════════════════
  # G.1 移交给Agent-07（系统集成师）
  # ═══════════════════════════════════════════════════════════════════════════
  
  To_Agent_07_System_Integration:
    
    deliverables:
      - item: "全域I/O点位矩阵"
        format: "Excel + YAML"
        content: "992设备，6974点位完整清单"
        usage: "网络规划、DDC选型、点位地址分配"
        
      - item: "通信协议规范"
        format: "文档"
        content: "BACnet/IP、MS/TP、Modbus配置参数"
        usage: "网络设计、协议转换配置"
        
      - item: "消防联动矩阵"
        format: "Excel"
        content: "FAS-BMS接口点位和联动逻辑"
        usage: "与FAS厂家接口协调"
        
      - item: "控制网络拓扑"
        format: "CAD + 文档"
        content: "L1/L2/L3层级架构"
        usage: "网络布线设计"
        
    interface_agreements:
      
      FAS_BMS_Interface:
        name: "消防-BMS接口协议"
        points:
          inputs_from_FAS:
            - "火警确认信号（分区）"
            - "消防泵运行状态"
            - "排烟风机状态"
            - "防火阀状态"
          outputs_to_FAS:
            - "AHU运行状态"
            - "联动确认信号"
        protocol: "硬接点 或 Modbus"
        coordination: "需与FAS厂家共同确认"
        
      HIS_BMS_Interface:
        name: "HIS-BMS接口"
        data_exchange:
          from_HIS:
            - "手术排程（预约时间、手术室号）"
            - "隔离病房启用状态"
          to_HIS:
            - "手术室环境状态（可选）"
        protocol: "RESTful API 或 消息队列"
        security: "医院内网，加密传输"
        
    joint_testing:
      - test: "消防联动综合测试"
        participants: ["Agent-06", "Agent-07", "FAS厂家", "消防验收"]
        content: "验证火警触发后HVAC响应"
        
      - test: "网络通信测试"
        participants: ["Agent-06", "Agent-07", "BMS厂家"]
        content: "验证所有通信链路"
        
    target_completion: "系统集成测试阶段"
    
  # ═══════════════════════════════════════════════════════════════════════════
  # G.2 移交给Agent-08（医疗流程建模师）
  # ═══════════════════════════════════════════════════════════════════════════
  
  To_Agent_08_Medical_Workflow:
    
    deliverables:
      - item: "手术室状态机完整定义"
        format: "YAML"
        content: "FSM-OR001-HVAC及所有手术室模板"
        usage: "与手术流程对接"
        
      - item: "医疗空间环境需求表"
        format: "Excel"
        content: "各类空间的温湿度、压差、换气指标"
        source: "Agent-02 + Agent-06实现"
        
      - item: "模式切换触发接口"
        format: "API文档"
        content: "如何从HIS触发PREP/SURGERY/DECON模式"
        
      - item: "温度调节权限说明"
        format: "文档"
        content: "手术室面板可调范围和限制"
        
    coordination_items:
      
      surgery_schedule_integration:
        description: "手术排程与HVAC预启动的对接"
        questions:
          - "手术排程数据格式是什么？"
          - "提前多久发送预启动信号？"
          - "如何处理临时手术？"
        resolution: "需Agent-08提供HIS接口规范"
        
      isolation_workflow:
        description: "负压隔离病房启用流程"
        questions:
          - "谁有权限启动隔离模式？"
          - "启动后需要哪些确认？"
          - "恢复正常需要哪些步骤？"
        resolution: "需Agent-08定义临床流程"
        
    training:
      content: "帮助Agent-08理解FSM的医学含义"
      format: "工作坊"
      duration: "2小时"
      
    target_completion: "系统设计第2个月"
    
  # ═══════════════════════════════════════════════════════════════════════════
  # G.3 移交给Agent-09（运维建模师）
  # ═══════════════════════════════════════════════════════════════════════════
  
  To_Agent_09_Operations:
    
    deliverables:
      - item: "全域I/O点位矩阵"
        format: "Excel"
        usage: "维护管理、备件规划"
        
      - item: "故障诊断决策树"
        format: "文档 + 流程图"
        content: "常见故障的排查步骤"
        usage: "运维人员培训和现场使用"
        
      - item: "SAT验收测试清单"
        format: "表格"
        usage: "定期复测、性能评估"
        
      - item: "降级策略表"
        format: "文档"
        content: "各级故障的响应策略"
        usage: "应急预案、值班手册"
        
      - item: "KPI定义表"
        format: "Excel"
        content:
          - "温度达标率"
          - "压差达标率"
          - "设备可用率"
          - "能效指标"
        usage: "运维绩效考核"
        
      - item: "分户计量报表模板"
        format: "BI仪表板模板"
        usage: "能耗管理"
        
    training_plan:
      
      course_1:
        name: "BMS操作培训"
        audience: "中控室值班员"
        duration: "8小时"
        content:
          - "界面操作"
          - "报警处理"
          - "趋势查看"
          - "报表生成"
          
      course_2:
        name: "故障诊断培训"
        audience: "设备科技术员"
        duration: "16小时"
        content:
          - "故障诊断决策树使用"
          - "常见故障处理"
          - "与厂家沟通要点"
          
      course_3:
        name: "应急响应演练"
        audience: "全体值班人员"
        duration: "4小时"
        content:
          - "停电应急"
          - "火灾响应"
          - "极端天气应对"
          
    ongoing_support:
      warranty_period: "2年"
      annual_review: "每年复核控制参数和策略"
      continuous_improvement: "收集运维反馈优化系统"
      
    target_completion: "竣工前1个月"
```

---

# 文档版本演进计划

```yaml
Document_Maintenance_Plan:
  
  current_version:
    version: "v3.2"
    date: "2025-01-XX"
    status: "审核后补充发布"
    content:
      - "v3.1基础版（架构、典型对象、FSM）"
      - "补充A：全域I/O点位矩阵"
      - "补充B：Agent-04物理方程集成"
      - "补充C：故障诊断决策树"
      - "补充D：SAT验收测试清单"
      - "补充E：极端工况控制策略"
      - "补充F：分户计量与权限管理"
      - "补充G：下游Agent交接计划"
      
  next_version:
    version: "v3.3"
    planned_date: "2025 Q2"
    planned_content:
      - "完整ICU/负压病房FSM详细展开"
      - "冷站MPC优化算法详细设计"
      - "BACnet对象模型详细定义"
      - "与实际DDC厂家的编程指南对接"
    trigger: "DDC编程合同签订后"
    
  production_version:
    version: "v4.0"
    planned_date: "2025 Q4（系统投运后）"
    planned_content:
      - "集成SAT实测数据"
      - "优化后的PID参数"
      - "运维反馈的改进"
      - "AI故障预测逻辑（基于历史数据）"
    trigger: "首次投运后6个月"
    
  annual_review:
    frequency: "每年"
    content:
      - "对比设计值和实际运行数据"
      - "收集运维改进建议"
      - "对标最新行业标准"
      - "评估是否需要大版本升级"
```

---

# 补充文档完成总结

```yaml
Supplement_Summary:
  
  completed_items:
    
    P0_Critical:
      - name: "补充A：全域I/O点位矩阵"
        content: "992设备，6974点位统计；手术室完整67点清单"
        status: "✅ 完成"
        
      - name: "补充B：Agent-04物理方程集成"
        content: "前馈控制算法、虚拟传感器、冷站优化、压差快速控制"
        status: "✅ 完成"
        
    P1_Important:
      - name: "补充C：故障诊断决策树"
        content: "温度高/压差低/冷机故障的完整决策树"
        status: "✅ 完成"
        
      - name: "补充D：SAT验收测试清单"
        content: "8大类16项测试，含传感器、控制回路、网络中断等"
        status: "✅ 完成"
        
    P2_Enhancement:
      - name: "补充E：极端工况控制策略"
        content: "高温、低温、高负荷、停电四类工况"
        status: "✅ 完成"
        
      - name: "补充F：分户计量与权限管理"
        content: "虚拟电表/冷量表、四级权限体系"
        status: "✅ 完成"
        
      - name: "补充G：下游Agent交接计划"
        content: "与Agent-07/08/09的交付物和协调事项"
        status: "✅ 完成"
        
  document_statistics:
    total_yaml_lines: "~4500行"
    control_objects_detailed: 15
    io_points_defined: 6974
    fsm_states: 18
    control_loops: 12
    test_cases: 16
    fault_diagnosis_trees: 3
    
  readiness_assessment:
    for_ddc_programming: "70% → 85%（补充后）"
    for_sat_testing: "40% → 80%（补充后）"
    for_operations: "50% → 75%（补充后）"
    
  remaining_gaps:
    - "其他空间（ICU、负压病房）的完整FSM展开"
    - "与具体DDC厂家的编程接口对接"
    - "实际PID参数的现场整定"
    - "BACnet对象ID的具体分配"
```

---

**Agent-06 补充文档 v3.2 完成**

本补充文档响应了技术审核的全部7条改进建议（P0×2 + P1×2 + P2×3），显著提升了文档的工程实施性和可操作性。

后续建议：
1. **立即行动**：将全域I/O点位矩阵转为Excel格式，分发给DDC编程团队
2. **签订合同前**：与DDC厂家确认编程接口和对象模型兼容性
3. **SAT阶段**：使用本文档的测试清单进行验收，收集实测数据用于v4.0更新

---