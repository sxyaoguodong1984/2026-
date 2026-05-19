import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import math
import json
import os
from datetime import datetime, timedelta


class ConcentricCirclesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("日家奇门")
        self.root.geometry("1400x900")

        # ========== 核心参数配置 ==========
        self.canvas_width = 800
        self.canvas_height = 800
        self.center_x = self.canvas_width // 2
        self.center_y = self.canvas_height // 2
        self.base_radius = 50
        self.radius_gap = 60

        self.dizhi_list = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        self.yang_tiangan = ["甲", "丙", "戊", "庚", "壬"]
        self.yin_tiangan = ["乙", "丁", "己", "辛", "癸"]
        self.shichen_var_list = []
        self.comment_text_list = []
        self.comment_frame_list = []

        # ========== 界面布局 ==========
        main_container = tk.Frame(root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        left_frame = tk.Frame(main_container)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        right_main_frame = tk.Frame(main_container)
        right_main_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        right_canvas = tk.Canvas(right_main_frame)
        right_scroll_y = ttk.Scrollbar(right_main_frame, orient=tk.VERTICAL, command=right_canvas.yview)
        right_scroll_x = ttk.Scrollbar(right_main_frame, orient=tk.HORIZONTAL, command=right_canvas.xview)
        right_scrollable_frame = tk.Frame(right_canvas)

        right_scrollable_frame.bind(
            "<Configure>",
            lambda e: right_canvas.configure(scrollregion=right_canvas.bbox("all"))
        )

        right_canvas.create_window((0, 0), window=right_scrollable_frame, anchor="nw")
        right_canvas.configure(yscrollcommand=right_scroll_y.set, xscrollcommand=right_scroll_x.set)

        right_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        right_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # ========== 左侧功能区 ==========
        self.btn_frame = tk.Frame(left_frame)
        self.btn_frame.pack(pady=10)

        self.time_btn = tk.Button(
            self.btn_frame, text="切换时辰",
            command=self.on_time_click, font=("SimHei", 12)
        )
        self.time_btn.pack(side=tk.LEFT, padx=5)

        self.reset_btn = tk.Button(
            self.btn_frame, text="重置甲子",
            command=self.on_reset_click, font=("SimHei", 12)
        )
        self.reset_btn.pack(side=tk.LEFT, padx=5)

        self.gate_cw_btn = tk.Button(
            self.btn_frame, text="八门顺转",
            command=self.on_gate_cw_click, font=("SimHei", 12)
        )
        self.gate_cw_btn.pack(side=tk.LEFT, padx=5)

        self.gate_ccw_btn = tk.Button(
            self.btn_frame, text="八门逆转",
            command=self.on_gate_ccw_click, font=("SimHei", 12)
        )
        self.gate_ccw_btn.pack(side=tk.LEFT, padx=5)

        self.yd_switch_btn = tk.Button(
            self.btn_frame, text="切换为阴遁",
            command=self.on_yd_switch_click, font=("SimHei", 12)
        )
        self.yd_switch_btn.pack(side=tk.LEFT, padx=5)

        # ======================
        # ✅ 一键保存按钮
        # ======================
        self.save_btn = tk.Button(
            self.btn_frame, text="💾 一键保存",
            command=self.save_all_data, font=("SimHei", 12)
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)

        self.jieqi_frame = tk.Frame(left_frame)
        self.jieqi_frame.pack(pady=10, fill=tk.X)
        self.jieqi_label = tk.Label(self.jieqi_frame, text="", font=("SimHei", 12))
        self.jieqi_label.pack(side=tk.LEFT, padx=5)
        self.yuan_label = tk.Label(self.jieqi_frame, text="", font=("SimHei", 12))
        self.yuan_label.pack(side=tk.LEFT, padx=5)
        self.countdown_label = tk.Label(self.jieqi_frame, text="", font=("SimHei", 12))
        self.countdown_label.pack(side=tk.LEFT, padx=5)

        self.canvas = tk.Canvas(left_frame, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        # ========== 右侧12时辰评论区 ==========
        tk.Label(right_scrollable_frame, text="12时辰吉凶评论", font=("SimHei", 14, "bold")).pack(pady=5)

        for i, dizhi in enumerate(self.dizhi_list):
            shichen_frame = tk.Frame(right_scrollable_frame)
            shichen_frame.pack(fill=tk.X, pady=5)

            tk.Label(shichen_frame, text=f"{dizhi}时", font=("SimHei", 12), width=6).pack(side=tk.LEFT)

            if dizhi in ["子", "寅", "辰", "午", "申", "戌"]:
                gan_list = self.yang_tiangan
            else:
                gan_list = self.yin_tiangan
            ganzhi_options = [f"{gan}{dizhi}" for gan in gan_list]
            var = tk.StringVar(value=ganzhi_options[0])
            combo = ttk.Combobox(shichen_frame, textvariable=var, values=ganzhi_options, font=("SimHei", 12), width=8)
            combo.pack(side=tk.LEFT, padx=5)
            self.shichen_var_list.append(var)

            tk.Label(shichen_frame, text="评论：", font=("SimHei", 12), width=6).pack(side=tk.LEFT)

            comment_container = tk.Frame(shichen_frame)
            comment_container.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

            comment_text = scrolledtext.ScrolledText(comment_container, font=("SimHei", 12), width=20, height=2)
            comment_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
            comment_text.insert(tk.END, "吉凶平/自定义评论（可输入多行文字）")
            self.comment_text_list.append(comment_text)
            self.comment_frame_list.append(comment_container)

            btn_frame = tk.Frame(comment_container)
            btn_frame.pack(side=tk.RIGHT, padx=2)

            enlarge_btn = tk.Button(btn_frame, text="↑", font=("SimHei", 10), width=2,
                                    command=lambda idx=i: self.resize_comment(idx, "enlarge"))
            enlarge_btn.pack(side=tk.TOP, pady=1)

            shrink_btn = tk.Button(btn_frame, text="↓", font=("SimHei", 10), width=2,
                                   command=lambda idx=i: self.resize_comment(idx, "shrink"))
            shrink_btn.pack(side=tk.BOTTOM, pady=1)

        # ========== 状态变量 ==========
        self.current_time_idx = 0
        self.gate_shift_step = 0
        self.is_yin_du = False

        self.time_list = [
            "甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉",
            "甲戌", "乙亥", "丙子", "丁丑", "戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未",
            "甲申", "乙酉", "丙戌", "丁亥", "戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳",
            "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥", "庚子", "辛丑", "壬寅", "癸卯",
            "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥", "壬子", "癸丑",
            "甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥"
        ]

        self.center_text_cycle_yang = ["咸池", "青龙", "天符", "招摇", "轩辕", "摄提", "太乙", "天乙", "太阴"]
        self.center_text_cycle_yin = ["咸池", "白虎", "天符", "招摇", "轩辕", "摄提", "太乙", "天乙", "太阴"]

        self.base_position_mapping_yin = {
            0: {"坎": "摄提", "乾": "白虎", "兑": "天符", "坤": "太乙", "离": "轩辕", "巽": "太阴", "震": "天乙",
                "艮": "招摇"},
            1: {"坎": "太乙", "乾": "天符", "兑": "招摇", "坤": "天乙", "离": "摄提", "巽": "白虎", "震": "太阴",
                "艮": "轩辕"},
            2: {"坎": "天乙", "乾": "招摇", "兑": "轩辕", "坤": "太阴", "离": "太乙", "巽": "白虎", "震": "咸池",
                "艮": "摄提"},
            3: {"坎": "太阴", "乾": "轩辕", "兑": "摄提", "坤": "咸池", "离": "天乙", "巽": "天符", "震": "白虎",
                "艮": "太乙"},
            4: {"坎": "咸池", "乾": "摄提", "兑": "太乙", "坤": "白虎", "离": "太阴", "巽": "招摇", "震": "天符",
                "艮": "天乙"},
            5: {"坎": "白虎", "乾": "太乙", "兑": "天乙", "坤": "天符", "离": "咸池", "巽": "轩辕", "震": "招摇",
                "艮": "太阴"},
            6: {"坎": "天符", "乾": "天乙", "兑": "太阴", "坤": "招摇", "离": "白虎", "巽": "摄提", "震": "轩辕",
                "艮": "咸池"},
            7: {"坎": "招摇", "乾": "太阴", "兑": "咸池", "坤": "轩辕", "离": "天符", "巽": "太乙", "震": "摄提",
                "艮": "白虎"},
            8: {"坎": "轩辕", "乾": "咸池", "兑": "白虎", "坤": "摄提", "离": "招摇", "巽": "天乙", "震": "太乙",
                "艮": "天符"}
        }

        self.base_position_mapping_yang = {
            0: {"坎": "轩辕", "乾": "太阴", "兑": "天乙", "坤": "招摇", "离": "摄提", "巽": "青龙", "震": "天符",
                "艮": "太乙"},
            1: {"坎": "摄提", "乾": "咸池", "兑": "太阴", "坤": "轩辕", "离": "太乙", "巽": "天符", "震": "招摇",
                "艮": "天乙"},
            2: {"坎": "太乙", "乾": "青龙", "兑": "咸池", "坤": "摄提", "离": "天乙", "巽": "招摇", "震": "轩辕",
                "艮": "太阴"},
            3: {"坎": "天乙", "乾": "天符", "兑": "青龙", "坤": "太乙", "离": "太阴", "巽": "轩辕", "震": "摄提",
                "艮": "咸池"},
            4: {"坎": "太阴", "乾": "招摇", "兑": "天符", "坤": "天乙", "离": "咸池", "巽": "摄提", "震": "太乙",
                "艮": "青龙"},
            5: {"坎": "咸池", "乾": "轩辕", "兑": "招摇", "坤": "太阴", "离": "青龙", "巽": "太乙", "震": "天乙",
                "艮": "天符"},
            6: {"坎": "青龙", "乾": "摄提", "兑": "轩辕", "坤": "咸池", "离": "天符", "巽": "天乙", "震": "太阴",
                "艮": "招摇"},
            7: {"坎": "天符", "乾": "太乙", "兑": "摄提", "坤": "青龙", "离": "招摇", "巽": "太阴", "震": "咸池",
                "艮": "轩辕"},
            8: {"坎": "招摇", "乾": "天乙", "兑": "太乙", "坤": "天符", "离": "轩辕", "巽": "咸池", "震": "青龙",
                "艮": "摄提"}
        }

        self.second_circle_bagua = ["兑", "坤", "离", "巽", "震", "艮", "坎", "乾"]
        self.gate_texts = ["开", "休", "生", "伤", "杜", "景", "死", "惊"]
        self.yang_stems = ["甲", "丙", "戊", "庚", "壬"]
        self.yin_stems = ["乙", "丁", "己", "辛", "癸"]

        self.gate_map = {}
        self.init_gate_config()
        self.time_mapping_index = [i % 9 for i in range(60)]
        self.update_system_info()
        self.redraw_all()

        # ======================
        # ✅ 自动加载 E 盘数据
        # ======================
        self.load_saved_data()

        self.root.after(1000, self.update_system_info)

    # ======================
    # ✅ 保存到 E 盘
    # ======================
    def save_all_data(self):
        # 保存路径：E盘根目录
        save_path = "E:/rijia_qimen_save.json"

        try:
            shichen_values = [var.get() for var in self.shichen_var_list]

            comment_values = []
            comment_sizes = []
            for txt in self.comment_text_list:
                content = txt.get("1.0", tk.END).strip()
                comment_values.append(content)
                w = txt["width"]
                h = txt["height"]
                comment_sizes.append([w, h])

            data = {
                "current_time_idx": self.current_time_idx,
                "gate_shift_step": self.gate_shift_step,
                "is_yin_du": self.is_yin_du,
                "shichen_values": shichen_values,
                "comment_values": comment_values,
                "comment_sizes": comment_sizes
            }

            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            messagebox.showinfo("保存成功", f"✅ 已保存到 E 盘！\n路径：{save_path}")

        except Exception as e:
            messagebox.showerror("保存失败", f"请检查 E 盘是否可写入\n错误：{str(e)}")

    # ======================
    # ✅ 从 E 盘加载
    # ======================
    def load_saved_data(self):
        save_path = "E:/rijia_qimen_save.json"

        if not os.path.exists(save_path):
            return

        try:
            with open(save_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.current_time_idx = data.get("current_time_idx", 0)
            self.gate_shift_step = data.get("gate_shift_step", 0)
            self.is_yin_du = data.get("is_yin_du", False)

            shichen_vals = data.get("shichen_values", [])
            for i, var in enumerate(self.shichen_var_list):
                if i < len(shichen_vals):
                    var.set(shichen_vals[i])

            comment_vals = data.get("comment_values", [])
            comment_sizes = data.get("comment_sizes", [])
            for i, txt in enumerate(self.comment_text_list):
                txt.delete("1.0", tk.END)
                if i < len(comment_vals):
                    txt.insert("1.0", comment_vals[i])
                if i < len(comment_sizes):
                    w, h = comment_sizes[i]
                    txt.config(width=w, height=h)

            self.init_gate_config()
            self.redraw_all()
            self.on_yd_switch_click_refresh()

        except Exception as e:
            pass

    def on_yd_switch_click_refresh(self):
        if self.is_yin_du:
            self.yd_switch_btn.config(text="切换为阳遁")
        else:
            self.yd_switch_btn.config(text="切换为阴遁")
        current_time = self.time_list[self.current_time_idx]
        dun_type = "阴遁" if self.is_yin_du else "阳遁"
        self.root.title(f"日家奇门（{dun_type}，当前：{current_time}时）")

    # ========== 评论框放大缩小 ==========
    def resize_comment(self, idx, action):
        text_widget = self.comment_text_list[idx]
        current_width = text_widget["width"]
        current_height = text_widget["height"]

        if action == "enlarge":
            new_width = min(current_width + 5, 50)
            new_height = min(current_height + 1, 10)
        else:
            new_width = max(current_width - 5, 15)
            new_height = max(current_height - 1, 1)

        text_widget.config(width=new_width, height=new_height)
        self.comment_frame_list[idx].update_idletasks()
        self.root.update_idletasks()

    # ========== 原有核心方法 ==========
    def init_gate_config(self):
        self.gate_shift_step = self.gate_shift_step
        current_time = self.time_list[self.current_time_idx]
        stem = current_time[0]
        if stem in self.yang_stems:
            self.base_gate_bagua_map = {
                "乾": "开", "坎": "休", "艮": "生", "震": "伤",
                "巽": "杜", "离": "景", "坤": "死", "兑": "惊"
            }
        else:
            self.base_gate_bagua_map = {
                "乾": "开", "兑": "休", "坤": "生", "离": "伤",
                "巽": "杜", "震": "景", "艮": "死", "坎": "惊"
            }
        self.update_gate_map()

    def update_gate_map(self):
        base_gates = [self.base_gate_bagua_map[bagua] for bagua in self.second_circle_bagua]
        shifted_gates = []
        for i in range(8):
            original_idx = (i - self.gate_shift_step) % 8
            shifted_gates.append(base_gates[original_idx])
        self.gate_map = dict(zip(self.second_circle_bagua, shifted_gates))

    def get_current_center_text(self):
        current_dt = datetime.now()
        jieqi_name, _, _, _ = self.get_current_jieqi(current_dt)
        jieqi_order = ["立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑",
                       "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"]
        current_idx = jieqi_order.index(jieqi_name)
        winter_idx = jieqi_order.index("冬至")
        summer_idx = jieqi_order.index("夏至")
        is_winter_period = (current_idx >= winter_idx) or (current_idx < summer_idx)

        if self.is_yin_du or not is_winter_period:
            return self.center_text_cycle_yin[self.current_time_idx % len(self.center_text_cycle_yin)]
        else:
            return self.center_text_cycle_yang[self.current_time_idx % len(self.center_text_cycle_yang)]

    def get_current_position_map(self):
        base_idx = self.time_mapping_index[self.current_time_idx]
        current_dt = datetime.now()
        jieqi_name, _, _, _ = self.get_current_jieqi(current_dt)
        jieqi_order = ["立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑",
                       "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"]
        current_idx = jieqi_order.index(jieqi_name)
        winter_idx = jieqi_order.index("冬至")
        summer_idx = jieqi_order.index("夏至")
        is_winter_period = (current_idx >= winter_idx) or (current_idx < summer_idx)

        if self.is_yin_du or not is_winter_period:
            return self.base_position_mapping_yin[base_idx].copy()
        else:
            return self.base_position_mapping_yang[base_idx].copy()

    def redraw_all(self):
        self.canvas.delete("all")
        self.draw_concentric_circles()
        self.draw_sector_lines()
        self.draw_text_in_smallest_circle()
        self.draw_second_circle_bagua()
        self.draw_third_circle_gate()
        self.draw_max_circle_text()
        self.draw_current_datetime_text()

    def draw_concentric_circles(self):
        for i in range(4):
            radius = self.base_radius + i * self.radius_gap
            self.canvas.create_oval(
                self.center_x - radius, self.center_y - radius,
                self.center_x + radius, self.center_y + radius,
                outline="black", width=2
            )

    def draw_sector_lines(self):
        angles = [22.5, 67.5, 112.5, 157.5, 202.5, 247.5, 292.5, 337.5]
        max_radius = self.base_radius + 3 * self.radius_gap
        for angle in angles:
            angle_rad = math.radians(angle)
            start_x = self.center_x + self.base_radius * math.cos(angle_rad)
            start_y = self.center_y + self.base_radius * math.sin(angle_rad)
            end_x = self.center_x + max_radius * math.cos(angle_rad)
            end_y = self.center_y + max_radius * math.sin(angle_rad)
            self.canvas.create_line(start_x, start_y, end_x, end_y, fill="gray", width=1)

    def draw_text_in_smallest_circle(self):
        font = ("SimHei", 20, "bold")
        current_text = self.get_current_center_text()
        if len(current_text) == 2:
            self.canvas.create_text(self.center_x, self.center_y - 20, text=current_text[0], font=font, fill="darkred",
                                    anchor="center")
            self.canvas.create_text(self.center_x, self.center_y + 20, text=current_text[1], font=font, fill="darkred",
                                    anchor="center")
        else:
            self.canvas.create_text(self.center_x, self.center_y, text=current_text, font=font, fill="darkred",
                                    anchor="center")

    def draw_second_circle_bagua(self):
        text_angles = [0, 45, 90, 135, 180, 225, 270, 315]
        text_radius = self.base_radius + self.radius_gap // 2
        font = ("SimHei", 16, "bold")
        for idx, center_angle in enumerate(text_angles):
            current_text = self.second_circle_bagua[idx]
            angle_rad = math.radians(center_angle)
            cos_val = math.cos(angle_rad)
            sin_val = -math.sin(angle_rad)
            text_x = self.center_x + text_radius * cos_val
            text_y = self.center_y + text_radius * sin_val
            self.canvas.create_text(text_x, text_y, text=current_text, font=font, fill="darkblue", anchor="center")

    def draw_third_circle_gate(self):
        text_angles = [0, 45, 90, 135, 180, 225, 270, 315]
        text_radius = self.base_radius + self.radius_gap + self.radius_gap // 2
        font = ("SimHei", 18, "bold")
        for idx, center_angle in enumerate(text_angles):
            bagua = self.second_circle_bagua[idx]
            current_text = self.gate_map.get(bagua, "")
            angle_rad = math.radians(center_angle)
            cos_val = math.cos(angle_rad)
            sin_val = -math.sin(angle_rad)
            text_x = self.center_x + text_radius * cos_val
            text_y = self.center_y + text_radius * sin_val
            self.canvas.create_text(text_x, text_y, text=current_text, font=font, fill="darkgreen", anchor="center")

    def draw_max_circle_text(self):
        text_angles = [0, 45, 90, 135, 180, 225, 270, 315]
        text_radius = self.base_radius + 2 * self.radius_gap + self.radius_gap // 2
        font = ("SimHei", 20, "bold")
        current_pos_map = self.get_current_position_map()
        for idx, center_angle in enumerate(text_angles):
            bagua = self.second_circle_bagua[idx]
            current_text = current_pos_map.get(bagua, "")
            angle_rad = math.radians(center_angle)
            cos_val = math.cos(angle_rad)
            sin_val = -math.sin(angle_rad)
            text_x = self.center_x + text_radius * cos_val
            text_y = self.center_y + text_radius * sin_val
            self.canvas.create_text(text_x, text_y, text=current_text, font=font, fill="black", anchor="center")

    def draw_current_datetime_text(self):
        max_radius = self.base_radius + 3 * self.radius_gap
        text_y = self.center_y + max_radius + 50
        current_datetime = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        self.canvas.create_text(self.center_x, text_y, text=current_datetime, font=("SimHei", 14, "bold"),
                                fill="darkred", anchor="center")

    def get_traditional_date(self, current_dt):
        if current_dt.hour >= 23:
            traditional_dt = current_dt + timedelta(days=1)
        else:
            traditional_dt = current_dt
        return datetime(traditional_dt.year, traditional_dt.month, traditional_dt.day)

    def get_current_jieqi(self, current_dt):
        jieqi_2026 = {
            "立春": datetime(2026, 2, 4, 17, 5),
            "雨水": datetime(2026, 2, 19, 12, 59),
            "惊蛰": datetime(2026, 3, 6, 11, 13),
            "春分": datetime(2026, 3, 21, 12, 7),
            "清明": datetime(2026, 4, 5, 15, 59),
            "谷雨": datetime(2026, 4, 20, 23, 2),
            "立夏": datetime(2026, 5, 6, 9, 14),
            "小满": datetime(2026, 5, 21, 22, 17),
            "芒种": datetime(2026, 6, 6, 13, 36),
            "夏至": datetime(2026, 6, 22, 6, 13),
            "小暑": datetime(2026, 7, 7, 23, 48),
            "大暑": datetime(2026, 7, 23, 17, 1),
            "立秋": datetime(2026, 8, 7, 9, 29),
            "处暑": datetime(2026, 8, 23, 23, 59),
            "白露": datetime(2026, 9, 8, 12, 11),
            "秋分": datetime(2026, 9, 23, 21, 30),
            "寒露": datetime(2026, 10, 8, 23, 47),
            "霜降": datetime(2026, 10, 24, 2, 51),
            "立冬": datetime(2026, 11, 7, 2, 54),
            "小雪": datetime(2026, 11, 22, 0, 15),
            "大雪": datetime(2026, 12, 6, 19, 2),
            "冬至": datetime(2026, 12, 21, 13, 10),
            "小寒": datetime(2027, 1, 5, 6, 23),
            "大寒": datetime(2027, 1, 20, 23, 43),
            "2025小寒": datetime(2025, 1, 6, 0, 46),
            "2025大寒": datetime(2025, 1, 20, 18, 9)
        }
        jieqi_order = ["立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑",
                       "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"]

        next_jieqi_name = "立春"
        next_jieqi_time = jieqi_2026["立春"]

        if current_dt.year == 2026 and current_dt.month == 1:
            if current_dt < jieqi_2026["小寒"]:
                jieqi_name = "小寒"
            elif current_dt < jieqi_2026["大寒"]:
                jieqi_name = "大寒"
            else:
                jieqi_name = "立春"
        else:
            for i in range(len(jieqi_order)):
                jieqi_name = jieqi_order[i]
                jieqi_time = jieqi_2026[jieqi_name]
                next_i = (i + 1) % len(jieqi_order)
                next_jieqi_name = jieqi_order[next_i]
                next_jieqi_time = jieqi_2026[next_jieqi_name]
                if jieqi_time <= current_dt < next_jieqi_time:
                    break
            else:
                jieqi_name = "立春"

        return jieqi_name, jieqi_2026, next_jieqi_name, next_jieqi_time

    def get_jieqi_day_and_yuan(self, jieqi_name, jieqi_2026, current_dt):
        jieqi_start = jieqi_2026[jieqi_name]
        current_trad_dt = self.get_traditional_date(current_dt)
        jieqi_start_trad_dt = self.get_traditional_date(jieqi_start)
        days_diff = (current_trad_dt - jieqi_start_trad_dt).days
        day_num = days_diff + 1
        day_num = min(day_num, 15)
        if 1 <= day_num <= 5:
            yuan_type = "上元"
        elif 6 <= day_num <= 10:
            yuan_type = "中元"
        elif 11 <= day_num <= 15:
            yuan_type = "下元"
        else:
            yuan_type = "上元"
        return day_num, yuan_type

    def update_system_info(self):
        current_dt = datetime.now()
        jieqi_name, jieqi_2026, next_jieqi_name, next_jieqi_time = self.get_current_jieqi(current_dt)
        day_num, yuan_type = self.get_jieqi_day_and_yuan(jieqi_name, jieqi_2026, current_dt)
        time_diff = next_jieqi_time - current_dt
        days = time_diff.days
        hours = time_diff.seconds // 3600
        minutes = (time_diff.seconds % 3600) // 60
        seconds = time_diff.seconds % 60

        self.jieqi_label.config(text=f"当前节气：{jieqi_name}")
        self.yuan_label.config(text=f"{jieqi_name}第{day_num}天（{yuan_type}）")
        self.countdown_label.config(text=f"距离{next_jieqi_name}：{days}天{hours}时{minutes}分{seconds}秒")
        self.root.after(1000, self.update_system_info)

    # ========== 按钮事件 ==========
    def on_time_click(self):
        self.current_time_idx = (self.current_time_idx + 1) % len(self.time_list)
        self.init_gate_config()
        current_time = self.time_list[self.current_time_idx]
        dun_type = "阴遁" if self.is_yin_du else "阳遁"
        self.root.title(f"日家奇门（{dun_type}，当前：{current_time}时）")
        self.redraw_all()

    def on_reset_click(self):
        self.current_time_idx = 0
        self.init_gate_config()
        current_time = self.time_list[self.current_time_idx]
        dun_type = "阴遁" if self.is_yin_du else "阳遁"
        self.root.title(f"日家奇门（{dun_type}，当前：{current_time}时）")
        self.redraw_all()

    def on_gate_cw_click(self):
        self.gate_shift_step = (self.gate_shift_step + 1) % 8
        self.update_gate_map()
        self.redraw_all()

    def on_gate_ccw_click(self):
        self.gate_shift_step = (self.gate_shift_step - 1) % 8
        self.update_gate_map()
        self.redraw_all()

    def on_yd_switch_click(self):
        self.is_yin_du = not self.is_yin_du
        self.on_yd_switch_click_refresh()
        self.redraw_all()


if __name__ == "__main__":
    root = tk.Tk()
    app = ConcentricCirclesApp(root)
    root.mainloop()