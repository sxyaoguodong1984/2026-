import tkinter as tk
from tkinter import ttk, messagebox
import math
import json
import os
from datetime import datetime


class CircleSectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("洛书")
        self.root.geometry("1200x900")

        # 核心配置
        self.scale_factor = 0.7
        self.center_x = 550
        self.center_y = 380
        self.base_circle_spacing = 60
        self.circle_spacing = int(self.base_circle_spacing * self.scale_factor)
        self.total_circles = 7
        self.sector_count = 8
        self.angle_step = 360 / self.sector_count
        self.circle_line_width = 2

        # 圆半径
        self.circle_radii = [self.circle_spacing * (i + 1) for i in range(self.total_circles)]
        self.circle_radii = [max(r, 20) for r in self.circle_radii]
        self.max_radius = self.circle_radii[-1]
        self.label_offset = 12
        self.char_spacing = 15

        # 外侧节气文字
        self.sector_outer_labels = {
            0: "降霜 露寒",
            1: "露白 暑处",
            2: "暑大 暑小",
            3: "种芒 满小",
            4: "雨谷 明清",
            5: "蛰惊 水雨",
            6: "寒大 寒小",
            7: "雪大 雪小"
        }

        # 旋转偏移
        self.rotation_offsets = [0] * self.total_circles

        # ======================
        # 宫位 + 六仪三奇
        # ======================
        self.palace_mapping = {
            "立春": 5,
            "春分": 4,
            "立夏": 3,
            "夏至": 2,
            "立秋": 1,
            "秋分": 0,
            "立冬": 7,
            "冬至": 6
        }
        self.palace_names = list(self.palace_mapping.keys())
        self.current_selected_palace = tk.StringVar(value="立春")
        self.current_liuyi = tk.StringVar(value="甲子戊")
        self.palace_liuyi_marks = {i: "" for i in range(8)}

        self.liuyi_sanqi_list = [
            "甲子戊", "甲戌己", "甲申庚", "甲午辛",
            "甲辰壬", "甲寅癸", "丁奇", "丙奇", "乙奇"
        ]

        # 最大圆内侧节气文字
        self.inner_palace_labels = {
            0: "秋分",
            1: "立秋",
            2: "夏至",
            3: "立夏",
            4: "春分",
            5: "立春",
            6: "冬至",
            7: "立冬"
        }

        # 中宫
        self.current_nine_star = tk.StringVar(value="天禽星")
        self.current_liu_yi_san_qi = tk.StringVar(value="甲寅癸")

        # ======================
        # ✅ 新增：中宫底部文字选择（五 / 八门）
        # ======================
        self.central_bottom_texts = ["五", "开门", "休门", "生门", "伤门", "杜门", "景门", "死门", "惊门"]
        self.current_central_bottom = tk.StringVar(value="五")

        self.nine_stars = [
            "天蓬星", "天芮星", "天冲星", "天辅星",
            "天禽星", "天心星", "天柱星", "天任星", "天英星"
        ]

        # 2026年24节气真实交接时间
        self.solar_terms_2026 = [
            ("立春", datetime(2026, 2, 4, 16, 26)),
            ("雨水", datetime(2026, 2, 19, 12, 13)),
            ("惊蛰", datetime(2026, 3, 5, 10, 22)),
            ("春分", datetime(2026, 3, 20, 11, 16)),
            ("清明", datetime(2026, 4, 4, 15, 2)),
            ("谷雨", datetime(2026, 4, 20, 22, 45)),
            ("立夏", datetime(2026, 5, 6, 8, 9)),
            ("小满", datetime(2026, 5, 21, 21, 44)),
            ("芒种", datetime(2026, 6, 6, 2, 48)),
            ("夏至", datetime(2026, 6, 21, 19, 36)),
            ("小暑", datetime(2026, 7, 7, 13, 14)),
            ("大暑", datetime(2026, 7, 23, 6, 44)),
            ("立秋", datetime(2026, 8, 8, 0, 13)),
            ("处暑", datetime(2026, 8, 23, 14, 48)),
            ("白露", datetime(2026, 9, 7, 17, 13)),
            ("秋分", datetime(2026, 9, 23, 2, 50)),
            ("寒露", datetime(2026, 10, 8, 8, 10)),
            ("霜降", datetime(2026, 10, 23, 11, 7)),
            ("立冬", datetime(2026, 11, 7, 11, 7)),
            ("小雪", datetime(2026, 11, 22, 8, 22)),
            ("大雪", datetime(2026, 12, 7, 3, 56)),
            ("冬至", datetime(2026, 12, 21, 21, 20)),
            ("小寒", datetime(2027, 1, 5, 14, 49)),
            ("大寒", datetime(2027, 1, 20, 8, 29)),
        ]

        # 清空所有数字
        self.base_texts = ["七", "二", "九", "四 ", "三", "八", "一", "六"]
        self.circle2_texts = ["九地", "朱雀", "勾陈", "六合", "太阴", "螣蛇", "直符", "九天"]

        # 八门九星八卦
        self.qimen_doors = {
            0: "天柱星丙", 1: "天芮星庚", 2: "天英星戊", 3: "天辅星壬",
            4: "天冲星辛", 5: "天任星乙", 6: "天蓬星己", 7: "天心星丁"
        }
        self.qimen_stars = {
            0: "惊门", 1: "死门", 2: "景门", 3: "杜门",
            4: "伤门", 5: "生门", 6: "休门", 7: "开门"
        }
        self.bagua = {
            0: "兑七宫", 1: "坤二宫", 2: "离九宫", 3: "巽四宫",
            4: "震三宫", 5: "艮八宫", 6: "坎一宫", 7: "乾六宫"
        }

        # ======================
        # 按钮区域
        # ======================
        self.button_frame = ttk.Frame(root)
        self.button_frame.pack(pady=10)

        ttk.Button(self.button_frame, text="直符",
                   command=lambda: self.rotate_single_circle(1),
                   width=15).pack(side=tk.LEFT, padx=3)

        ttk.Button(self.button_frame, text="星门",
                   command=lambda: self.rotate_circle_4_and_5_together(),
                   width=15).pack(side=tk.LEFT, padx=3)

        # 宫位选择
        ttk.Label(self.button_frame, text="宫位：").pack(side=tk.LEFT, padx=2)
        self.palace_cb = ttk.Combobox(
            self.button_frame, textvariable=self.current_selected_palace,
            values=self.palace_names, width=8, state="readonly"
        )
        self.palace_cb.pack(side=tk.LEFT, padx=3)

        # 六仪三奇
        ttk.Label(self.button_frame, text="六仪三奇：").pack(side=tk.LEFT, padx=2)
        self.liuyi_cb = ttk.Combobox(
            self.button_frame, textvariable=self.current_liuyi,
            values=self.liuyi_sanqi_list, width=8, state="readonly"
        )
        self.liuyi_cb.pack(side=tk.LEFT, padx=3)

        ttk.Button(self.button_frame, text="确认标注",
                   command=self.set_palace_liuyi,
                   width=12).pack(side=tk.LEFT, padx=3)

        # 中宫九星
        ttk.Label(self.button_frame, text="中宫九星：").pack(side=tk.LEFT, padx=2)
        self.nine_star_combobox = ttk.Combobox(
            self.button_frame, textvariable=self.current_nine_star,
            values=self.nine_stars, width=8, state="readonly"
        )
        self.nine_star_combobox.pack(side=tk.LEFT, padx=3)
        self.nine_star_combobox.bind("<<ComboboxSelected>>", self.on_nine_star_select)

        # 中宫六仪三奇
        ttk.Label(self.button_frame, text="中宫六仪：").pack(side=tk.LEFT, padx=2)
        self.central_liuyi_cb = ttk.Combobox(
            self.button_frame, textvariable=self.current_liu_yi_san_qi,
            values=self.liuyi_sanqi_list, width=8, state="readonly"
        )
        self.central_liuyi_cb.pack(side=tk.LEFT, padx=3)
        self.central_liuyi_cb.bind("<<ComboboxSelected>>", self.on_central_liuyi_select)

        # ======================
        # ✅ 新增：中宫底部（五/八门）选择框
        # ======================
        ttk.Label(self.button_frame, text="中宫底字：").pack(side=tk.LEFT, padx=2)
        self.central_bottom_cb = ttk.Combobox(
            self.button_frame, textvariable=self.current_central_bottom,
            values=self.central_bottom_texts, width=8, state="readonly"
        )
        self.central_bottom_cb.pack(side=tk.LEFT, padx=3)
        self.central_bottom_cb.bind("<<ComboboxSelected>>", self.on_central_bottom_select)

        # ======================
        # ✅ 新增：一键保存按钮
        # ======================
        ttk.Button(self.button_frame, text="💾 一键保存布局",
                   command=self.save_layout,
                   width=15).pack(side=tk.LEFT, padx=5)

        # 画布
        self.canvas = tk.Canvas(root, width=1100, height=700, bg="white")
        self.canvas.pack(pady=(10, 5))

        # 时间区域
        self.time_frame = ttk.Frame(root, relief=tk.RAISED, borderwidth=2)
        self.time_frame.pack(fill=tk.X, padx=20, pady=5)
        time_font = ("SimHei", 12, "bold")
        self.date_label = ttk.Label(self.time_frame, text="", font=time_font)
        self.date_label.pack(side=tk.LEFT, padx=10)
        self.time_label = ttk.Label(self.time_frame, text="", font=time_font)
        self.time_label.pack(side=tk.LEFT, padx=10)
        self.timestamp_label = ttk.Label(self.time_frame, text="", font=time_font)
        self.timestamp_label.pack(side=tk.LEFT, padx=10)

        # 节气 + 元运 + 倒计时 + 十二时辰
        self.solar_term_frame = ttk.Frame(root, relief=tk.RAISED, borderwidth=2)
        self.solar_term_frame.pack(fill=tk.X, padx=20, pady=5)
        self.solar_term_label = ttk.Label(
            self.solar_term_frame, text="", font=("SimHei", 12, "bold")
        )
        self.solar_term_label.pack(side=tk.LEFT, padx=10)

        self.time_timer = None
        self.draw_all_circles()
        self.update_datetime()
        self.start_time_timer()

        # ======================
        # ✅ 启动自动加载
        # ======================
        self.load_layout()

    # ======================
    # ✅ 新增：中宫底部文字切换
    # ======================
    def on_central_bottom_select(self, event):
        self.draw_all_circles()

    # ======================
    # ✅ 核心：保存布局（保存到 E 盘）
    # ======================
    def save_layout(self):
        # ✅ 保存路径改为 E 盘根目录
        save_path = "E:/luoshu_save.json"

        data = {
            "rotation_offsets": self.rotation_offsets,
            "palace_liuyi_marks": self.palace_liuyi_marks,
            "current_selected_palace": self.current_selected_palace.get(),
            "current_liuyi": self.current_liuyi.get(),
            "current_nine_star": self.current_nine_star.get(),
            "current_liu_yi_san_qi": self.current_liu_yi_san_qi.get(),
            "current_central_bottom": self.current_central_bottom.get(),
        }
        try:
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("保存成功", f"已保存到 E 盘！\n文件路径：{save_path}")
        except:
            messagebox.showerror("保存失败", "请检查 E 盘是否可写入")

    # ======================
    # ✅ 核心：加载布局（从 E 盘加载）
    # ======================
    def load_layout(self):
        # ✅ 从 E 盘读取
        save_path = "E:/luoshu_save.json"

        if not os.path.exists(save_path):
            return

        try:
            with open(save_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.rotation_offsets = data.get("rotation_offsets", [0] * 7)
            self.palace_liuyi_marks = data.get("palace_liuyi_marks", {str(i): "" for i in range(8)})

            # 兼容字符串key与数字key
            fixed_marks = {}
            for k in range(8):
                fixed_marks[k] = self.palace_liuyi_marks.get(str(k), "") or self.palace_liuyi_marks.get(k, "")
            self.palace_liuyi_marks = fixed_marks

            self.current_selected_palace.set(data.get("current_selected_palace", "立春"))
            self.current_liuyi.set(data.get("current_liuyi", "甲子戊"))
            self.current_nine_star.set(data.get("current_nine_star", "天禽星"))
            self.current_liu_yi_san_qi.set(data.get("current_liu_yi_san_qi", "甲寅癸"))
            self.current_central_bottom.set(data.get("current_central_bottom", "五"))

            self.draw_all_circles()
        except Exception as e:
            pass

    # ======================
    # 十二时辰
    # ======================
    def get_current_shichen(self):
        now = datetime.now()
        hour = now.hour
        shichen_list = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        index = (hour + 1) // 2
        return shichen_list[index % 12]

    def on_central_liuyi_select(self, event):
        self.draw_all_circles()

    def set_palace_liuyi(self):
        palace = self.current_selected_palace.get()
        liuyi = self.current_liuyi.get()
        idx = self.palace_mapping[palace]
        self.palace_liuyi_marks[idx] = liuyi
        self.draw_all_circles()

    def on_nine_star_select(self, event):
        self.draw_all_circles()

    # ======================
    # 节气、元运、倒计时
    # ======================
    def get_solar_info(self):
        now = datetime.now()
        current_term = None
        next_term = None
        for i in range(len(self.solar_terms_2026)):
            term_name, term_time = self.solar_terms_2026[i]
            next_i = (i + 1) % len(self.solar_terms_2026)
            next_term_name, next_term_time = self.solar_terms_2026[next_i]
            if term_time <= now < next_term_time:
                current_term = (term_name, term_time)
                next_term = (next_term_name, next_term_time)
                break
        if not current_term:
            return "未知", "未知", 0, 0, 0, 0

        term_name, term_start = current_term
        next_name, next_start = next_term
        delta = next_start - now
        days = delta.days
        seconds = delta.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        passed = (now - term_start).total_seconds()
        if passed < 5 * 86400:
            yuan = "上元"
        elif passed < 10 * 86400:
            yuan = "中元"
        else:
            yuan = "下元"

        return term_name, yuan, days, hours, minutes, secs

    def update_datetime(self):
        now = datetime.now()
        self.date_label.config(text=f"日期：{now.strftime('%Y-%m-%d')}")
        self.time_label.config(text=f"时间：{now.strftime('%H:%M:%S')}")
        self.timestamp_label.config(text=f"星期：{['日', '一', '二', '三', '四', '五', '六'][now.weekday()]}")

        term, yuan, d, h, m, s = self.get_solar_info()
        shichen = self.get_current_shichen()

        self.solar_term_label.config(
            text=f"当前节气：{term} | {yuan} | 距离下节气：{d}天{h}时{m}分{s}秒 | 当前时辰：{shichen}时"
        )

    def start_time_timer(self):
        self.update_datetime()
        self.time_timer = self.root.after(1000, self.start_time_timer)

    def stop_time_timer(self):
        if self.time_timer:
            self.root.after_cancel(self.time_timer)

    # ======================
    # 绘制函数
    # ======================
    def calculate_text_rotation_to_center(self, x, y):
        dx = x - self.center_x
        dy = y - self.center_y
        rad = math.atan2(dy, dx)
        angle = math.degrees(rad)
        return (360 - (angle + 270)) % 360

    def draw_all_circles(self):
        self.canvas.delete("all")
        for r in self.circle_radii:
            self.canvas.create_oval(
                self.center_x - r, self.center_y - r,
                self.center_x + r, self.center_y + r,
                outline="black", width=self.circle_line_width
            )
        # 中宫
        self.canvas.create_text(self.center_x, self.center_y - 20,
                                text=self.current_nine_star.get(),
                                font=("SimHei", 16, "bold"))
        self.canvas.create_text(self.center_x, self.center_y,
                                text=self.current_liu_yi_san_qi.get(),
                                font=("SimHei", 16, "bold"))
        # ======================
        # ✅ 中宫底部文字：动态切换
        # ======================
        self.canvas.create_text(self.center_x, self.center_y + 20,
                                text=self.current_central_bottom.get(),
                                font=("SimHei", 16, "bold"))

        max_r = self.max_radius
        min_r = self.circle_radii[0]
        for i in range(1, self.total_circles):
            self.draw_sectors(i, self.circle_radii[i], self.circle_radii[i - 1], max_r, min_r)

        self.draw_outer_sector_labels()
        self.draw_inner_palace_names()
        self.draw_palace_liuyi_marks()

    def draw_inner_palace_names(self):
        radius = self.max_radius - 23
        font = ("SimHei", 13, "bold")
        offset = self.rotation_offsets[6]
        for idx in range(8):
            txt = self.inner_palace_labels[idx]
            angle = idx * self.angle_step + offset - 8
            rad = math.radians(angle)
            x = self.center_x + radius * math.cos(rad)
            y = self.center_y - radius * math.sin(rad)
            ang = self.calculate_text_rotation_to_center(x, y)
            self.canvas.create_text(x, y, text=txt, font=font, fill="black", angle=ang)

    def draw_palace_liuyi_marks(self):
        radius = (self.circle_radii[6] + self.circle_radii[5]) / 2
        font = ("SimHei", 13, "bold")
        offset = self.rotation_offsets[6]
        for idx in range(8):
            txt = self.palace_liuyi_marks[idx]
            if not txt: continue
            angle = idx * self.angle_step + offset + 8
            rad = math.radians(angle)
            x = self.center_x + radius * math.cos(rad)
            y = self.center_y - radius * math.sin(rad)
            ang = self.calculate_text_rotation_to_center(x, y)
            self.canvas.create_text(x, y, text=txt, font=font, fill="red", angle=ang)

    def draw_outer_sector_labels(self):
        f = ("SimHei", 12, "bold")
        off = self.rotation_offsets[6]
        for i in range(8):
            txt = self.sector_outer_labels[i]
            a = i * 45 + off
            rad = math.radians(a)
            bx = self.center_x + (self.max_radius + 12) * math.cos(rad)
            by = self.center_y - (self.max_radius + 12) * math.sin(rad)
            ang = self.calculate_text_rotation_to_center(bx, by)
            h = (len(txt) - 1) * 15
            so = h / 2
            for j, c in enumerate(txt):
                pr = rad + math.pi / 2
                cx = bx - (j * 15 - so) * math.cos(pr)
                cy = by + (j * 15 - so) * math.sin(pr)
                self.canvas.create_text(cx, cy, text=c, font=f, angle=ang)

    def draw_sectors(self, idx, outer, inner, max_r, min_r):
        offset = self.rotation_offsets[idx]
        mid = (outer + inner) / 2
        for i in range(8):
            a = i * 45 + offset
            rad = math.radians(a)
            x = self.center_x + mid * math.cos(rad)
            y = self.center_y - mid * math.sin(rad)
            ang = self.calculate_text_rotation_to_center(x, y)

            if idx == 3:
                t = self.qimen_doors[i]
            elif idx == 4:
                t = self.qimen_stars[i]
            elif idx == 5:
                t = self.bagua[i]
            elif idx == 1:
                t = self.circle2_texts[i]
            else:
                t = self.base_texts[i]
            self.canvas.create_text(x, y, text=t, font=("simhei", 13, "bold"), fill="black", angle=ang)

        for i in range(8):
            a = i * 45 + offset + 22.5
            rad = math.radians(a)
            sx = self.center_x + min_r * math.cos(rad)
            sy = self.center_y - min_r * math.sin(rad)
            ex = self.center_x + max_r * math.cos(rad)
            ey = self.center_y - max_r * math.sin(rad)
            self.canvas.create_line(sx, sy, ex, ey, fill="gray")

    def rotate_single_circle(self, idx):
        self.rotation_offsets[idx] += 45
        self.draw_all_circles()

    def rotate_circle_4_and_5_together(self):
        self.rotation_offsets[3] += 45
        self.rotation_offsets[4] += 45
        self.draw_all_circles()

    def __del__(self):
        self.stop_time_timer()


if __name__ == "__main__":
    root = tk.Tk()
    app = CircleSectorApp(root)
    root.mainloop()