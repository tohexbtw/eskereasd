import random
import tkinter as tk
from tkinter import ttk, Canvas
import threading
import string
import time
import psutil
from collections import deque
import math
import calendar

width, height = 60, 25

class WidgetMenu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.9)
        self.root.configure(bg="#1a1a1a")
        
        self.root.geometry("250x500")
        self.root.title("Widgets")
        
        self.widgets = {}
        
        frame = tk.Frame(self.root, bg="#1a1a1a")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(frame, text="виджеты", bg="#1a1a1a", fg="#fff", font=("Courier", 14, "bold")).pack(pady=15)
        
        self.create_widget_button(frame, "змейка", self.toggle_snake)
        self.create_widget_button(frame, "cpu/ram", self.toggle_system)
        self.create_widget_button(frame, "настенные часы", self.toggle_clock)
        self.create_widget_button(frame, "календарь", self.toggle_calendar)
        self.create_widget_button(frame, "заметки", self.toggle_notes)
        self.create_widget_button(frame, "секундомер", self.toggle_stopwatch)
        self.create_widget_button(frame, "слоты", self.toggle_slots)
        
        self.offset_x, self.offset_y = 0, 0
        self.root.bind("<Button-3>", self.start_drag)
        self.root.bind("<B3-Motion>", self.drag_window)
        frame.bind("<Button-3>", self.start_drag)
        frame.bind("<B3-Motion>", self.drag_window)
        
        self.root.bind("<Escape>", lambda e: self.root.destroy())
    
    def create_widget_button(self, parent, text, command):
        btn = tk.Button(parent, text=text, command=command, bg="#333", fg="#fff", 
                       bd=0, font=("Courier", 10), width=25, pady=8)
        btn.pack(pady=5)
    
    def toggle_snake(self):
        if "snake" in self.widgets:
            try:
                if self.widgets["snake"].root.winfo_exists():
                    self.widgets["snake"].root.destroy()
            except:
                pass
            del self.widgets["snake"]
        else:
            widget = ArtApp()
            widget.menu = self
            widget.key = "snake"
            self.widgets["snake"] = widget
    
    def toggle_system(self):
        if "system_stats" in self.widgets:
            try:
                if self.widgets["system_stats"].root.winfo_exists():
                    self.widgets["system_stats"].root.destroy()
            except:
                pass
            del self.widgets["system_stats"]
        else:
            widget = SystemStatsWidget()
            widget.menu = self
            widget.key = "system_stats"
            self.widgets["system_stats"] = widget
    
    def toggle_clock(self):
        if "clock" in self.widgets:
            try:
                if self.widgets["clock"].root.winfo_exists():
                    self.widgets["clock"].root.destroy()
            except:
                pass
            del self.widgets["clock"]
        else:
            widget = ClockWidget()
            widget.menu = self
            widget.key = "clock"
            self.widgets["clock"] = widget
    
    def toggle_calendar(self):
        if "calendar" in self.widgets:
            try:
                if self.widgets["calendar"].root.winfo_exists():
                    self.widgets["calendar"].root.destroy()
            except:
                pass
            del self.widgets["calendar"]
        else:
            widget = CalendarWidget()
            widget.menu = self
            widget.key = "calendar"
            self.widgets["calendar"] = widget
    
    def toggle_notes(self):
        if "notes" in self.widgets:
            try:
                if self.widgets["notes"].root.winfo_exists():
                    self.widgets["notes"].root.destroy()
            except:
                pass
            del self.widgets["notes"]
        else:
            widget = NotesWidget()
            widget.menu = self
            widget.key = "notes"
            self.widgets["notes"] = widget
    
    def toggle_stopwatch(self):
        if "stopwatch" in self.widgets:
            try:
                if self.widgets["stopwatch"].root.winfo_exists():
                    self.widgets["stopwatch"].root.destroy()
            except:
                pass
            del self.widgets["stopwatch"]
        else:
            widget = StopwatchWidget()
            widget.menu = self
            widget.key = "stopwatch"
            self.widgets["stopwatch"] = widget
    
    def toggle_slots(self):
        if "slots" in self.widgets:
            try:
                if self.widgets["slots"].root.winfo_exists():
                    self.widgets["slots"].root.destroy()
            except:
                pass
            del self.widgets["slots"]
        else:
            widget = SlotMachineWidget()
            widget.menu = self
            widget.key = "slots"
            self.widgets["slots"] = widget
    
    def remove_widget(self, key):
        if key in self.widgets:
            try:
                del self.widgets[key]
            except:
                pass
    
    def start_drag(self, event):
        self.offset_x, self.offset_y = event.x, event.y
    
    def drag_window(self, event):
        x = self.root.winfo_x() + event.x - self.offset_x
        y = self.root.winfo_y() + event.y - self.offset_y
        self.root.geometry(f"+{x}+{y}")

class SystemStatsWidget:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.9)
        self.root.configure(bg="#1a1a1a")
        
        self.root.geometry("250x80")
        
        frame = tk.Frame(self.root, bg="#1a1a1a")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.label = tk.Label(frame, text="CPU: 0% | RAM: 0%", bg="#1a1a1a", 
                             fg="#0f0", font=("Courier", 12, "bold"))
        self.label.pack()
        
        self.offset_x, self.offset_y = 0, 0
        self.bind_drag(frame)
        self.bind_drag(self.label)
        
        self.root.bind("<Escape>", lambda e: self.on_close())
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.closed = False
        self.update_stats()
    
    def on_close(self):
        self.closed = True
        try:
            if hasattr(self, 'menu') and hasattr(self, 'key'):
                self.menu.remove_widget(self.key)
        except:
            pass
        try:
            self.root.destroy()
        except:
            pass
    
    def bind_drag(self, widget):
        widget.bind("<Button-3>", self.start_drag)
        widget.bind("<B3-Motion>", self.drag_window)
    
    def update_stats(self):
        try:
            if hasattr(self, 'closed') and self.closed:
                return
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            self.label.config(text=f"CPU: {cpu:.1f}% | RAM: {ram:.1f}%")
            self.root.after(1000, self.update_stats)
        except:
            pass
    
    def start_drag(self, event):
        self.offset_x, self.offset_y = event.x, event.y
    
    def drag_window(self, event):
        x = self.root.winfo_x() + event.x - self.offset_x
        y = self.root.winfo_y() + event.y - self.offset_y
        self.root.geometry(f"+{x}+{y}")

class ClockWidget:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.9)
        self.root.configure(bg="#1a1a1a")
        
        size = 300
        self.root.geometry(f"{size}x{size}")
        
        self.canvas = Canvas(self.root, bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.center_x = size // 2
        self.center_y = size // 2
        self.radius = size // 2 - 20
        
        self.offset_x, self.offset_y = 0, 0
        self.canvas.bind("<Button-3>", self.start_drag)
        self.canvas.bind("<B3-Motion>", self.drag_window)
        
        self.root.bind("<Escape>", lambda e: self.on_close())
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.closed = False
        self.update_time()
    
    def on_close(self):
        self.closed = True
        try:
            if hasattr(self, 'menu') and hasattr(self, 'key'):
                self.menu.remove_widget(self.key)
        except:
            pass
        try:
            self.root.destroy()
        except:
            pass
    
    def update_time(self):
        if hasattr(self, 'closed') and self.closed:
            return
        self.canvas.delete("all")
        
        now = time.localtime()
        hours = now.tm_hour % 12
        minutes = now.tm_min
        seconds = now.tm_sec
        
        self.canvas.create_oval(self.center_x - self.radius, self.center_y - self.radius,
                               self.center_x + self.radius, self.center_y + self.radius,
                               outline="#0ff", width=3)
        
        for i in range(12):
            angle = math.radians(i * 30 - 90)
            x1 = self.center_x + (self.radius - 15) * math.cos(angle)
            y1 = self.center_y + (self.radius - 15) * math.sin(angle)
            x2 = self.center_x + self.radius * math.cos(angle)
            y2 = self.center_y + self.radius * math.sin(angle)
            self.canvas.create_line(x1, y1, x2, y2, fill="#0ff", width=2)
            
            num_x = self.center_x + (self.radius - 30) * math.cos(angle)
            num_y = self.center_y + (self.radius - 30) * math.sin(angle)
            num = 12 if i == 0 else i
            self.canvas.create_text(num_x, num_y, text=str(num), fill="#0ff", font=("Courier", 12, "bold"))
        
        hour_angle = math.radians((hours * 30 + minutes * 0.5) - 90)
        hour_length = self.radius * 0.5
        hour_x = self.center_x + hour_length * math.cos(hour_angle)
        hour_y = self.center_y + hour_length * math.sin(hour_angle)
        self.canvas.create_line(self.center_x, self.center_y, hour_x, hour_y, fill="#fff", width=4)
        
        minute_angle = math.radians((minutes * 6 + seconds * 0.1) - 90)
        minute_length = self.radius * 0.7
        minute_x = self.center_x + minute_length * math.cos(minute_angle)
        minute_y = self.center_y + minute_length * math.sin(minute_angle)
        self.canvas.create_line(self.center_x, self.center_y, minute_x, minute_y, fill="#0ff", width=2)
        
        second_angle = math.radians((seconds * 6) - 90)
        second_length = self.radius * 0.8
        second_x = self.center_x + second_length * math.cos(second_angle)
        second_y = self.center_y + second_length * math.sin(second_angle)
        self.canvas.create_line(self.center_x, self.center_y, second_x, second_y, fill="#f00", width=1)
        
        self.canvas.create_oval(self.center_x - 5, self.center_y - 5,
                               self.center_x + 5, self.center_y + 5,
                               fill="#0ff", outline="#0ff")
        
        self.root.after(100, self.update_time)
    
    def start_drag(self, event):
        self.offset_x, self.offset_y = event.x, event.y
    
    def drag_window(self, event):
        x = self.root.winfo_x() + event.x - self.offset_x
        y = self.root.winfo_y() + event.y - self.offset_y
        self.root.geometry(f"+{x}+{y}")

class CalendarWidget:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.9)
        self.root.configure(bg="#1a1a1a")
        
        self.root.geometry("280x250")
        
        frame = tk.Frame(self.root, bg="#1a1a1a")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        now = time.localtime()
        self.current_year = now.tm_year
        self.current_month = now.tm_mon
        
        header = tk.Frame(frame, bg="#1a1a1a")
        header.pack(fill=tk.X, pady=5)
        
        tk.Button(header, text="<", command=self.prev_month, bg="#333", fg="#fff", bd=0, width=3).pack(side=tk.LEFT)
        self.month_label = tk.Label(header, text="", bg="#1a1a1a", fg="#0ff", font=("Courier", 12, "bold"))
        self.month_label.pack(side=tk.LEFT, expand=True)
        tk.Button(header, text=">", command=self.next_month, bg="#333", fg="#fff", bd=0, width=3).pack(side=tk.RIGHT)
        
        self.cal_frame = tk.Frame(frame, bg="#1a1a1a")
        self.cal_frame.pack()
        
        self.offset_x, self.offset_y = 0, 0
        self.bind_drag(frame)
        
        self.root.bind("<Escape>", lambda e: self.on_close())
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.closed = False
        self.update_calendar()
    
    def on_close(self):
        self.closed = True
        try:
            if hasattr(self, 'menu') and hasattr(self, 'key'):
                self.menu.remove_widget(self.key)
        except:
            pass
        try:
            self.root.destroy()
        except:
            pass
    
    def bind_drag(self, widget):
        widget.bind("<Button-3>", self.start_drag)
        widget.bind("<B3-Motion>", self.drag_window)
    
    def prev_month(self):
        self.current_month -= 1
        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.update_calendar()
    
    def next_month(self):
        self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        self.update_calendar()
    
    def update_calendar(self):
        for widget in self.cal_frame.winfo_children():
            widget.destroy()
        
        month_names = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                      "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
        self.month_label.config(text=f"{month_names[self.current_month-1]} {self.current_year}")
        
        cal = calendar.monthcalendar(self.current_year, self.current_month)
        
        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        for i, day in enumerate(days):
            label = tk.Label(self.cal_frame, text=day, bg="#1a1a1a", fg="#0ff", 
                           font=("Courier", 9, "bold"), width=4)
            label.grid(row=0, column=i)
        
        now = time.localtime()
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                if day == 0:
                    continue
                is_today = (day == now.tm_mday and self.current_month == now.tm_mon and 
                          self.current_year == now.tm_year)
                color = "#fff" if is_today else "#aaa"
                bg_color = "#333" if is_today else "#1a1a1a"
                label = tk.Label(self.cal_frame, text=str(day), bg=bg_color, fg=color, 
                               font=("Courier", 9), width=4)
                label.grid(row=week_num+1, column=day_num)
    
    def start_drag(self, event):
        self.offset_x, self.offset_y = event.x, event.y
    
    def drag_window(self, event):
        x = self.root.winfo_x() + event.x - self.offset_x
        y = self.root.winfo_y() + event.y - self.offset_y
        self.root.geometry(f"+{x}+{y}")

class NotesWidget:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.9)
        self.root.configure(bg="#1a1a1a")
        
        self.root.geometry("300x400")
        
        self.notes_file = "notes.txt"
        
        frame = tk.Frame(self.root, bg="#1a1a1a")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(frame, text="ЗАМЕТКИ", bg="#1a1a1a", fg="#fff", font=("Courier", 12, "bold")).pack(pady=5)
        
        self.text_area = tk.Text(frame, bg="#222", fg="#fff", font=("Courier", 10),
                                insertbackground="white", wrap=tk.WORD, width=30, height=15)
        self.text_area.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.load_notes()
        
        self.offset_x, self.offset_y = 0, 0
        self.bind_drag(frame)
        
        self.root.bind("<Escape>", lambda e: self.close_with_save())
        self.root.protocol("WM_DELETE_WINDOW", self.close_with_save)
    
    def load_notes(self):
        try:
            with open(self.notes_file, "r", encoding="utf-8") as f:
                content = f.read()
                self.text_area.insert("1.0", content)
        except FileNotFoundError:
            pass
        except Exception:
            pass
    
    def save_notes(self):
        try:
            content = self.text_area.get("1.0", tk.END)
            with open(self.notes_file, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception:
            pass
    
    def close_with_save(self):
        self.closed = True
        self.save_notes()
        try:
            if hasattr(self, 'menu') and hasattr(self, 'key'):
                self.menu.remove_widget(self.key)
        except:
            pass
        try:
            self.root.destroy()
        except:
            pass
    
    def bind_drag(self, widget):
        widget.bind("<Button-3>", self.start_drag)
        widget.bind("<B3-Motion>", self.drag_window)
    
    def start_drag(self, event):
        self.offset_x, self.offset_y = event.x, event.y
    
    def drag_window(self, event):
        x = self.root.winfo_x() + event.x - self.offset_x
        y = self.root.winfo_y() + event.y - self.offset_y
        self.root.geometry(f"+{x}+{y}")

class StopwatchWidget:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.9)
        self.root.configure(bg="#1a1a1a")
        
        self.root.geometry("250x150")
        
        frame = tk.Frame(self.root, bg="#1a1a1a")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.label = tk.Label(frame, text="00:00:00.000", bg="#1a1a1a", fg="#0ff", 
                             font=("Courier", 18, "bold"))
        self.label.pack(pady=10)
        
        btn_frame = tk.Frame(frame, bg="#1a1a1a")
        btn_frame.pack()
        
        self.running = False
        self.start_time = 0
        self.elapsed = 0
        
        self.start_btn = tk.Button(btn_frame, text="Старт", command=self.start_stop, 
                                  bg="#333", fg="#fff", bd=0, width=8)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Сброс", command=self.reset, 
                 bg="#333", fg="#fff", bd=0, width=8).pack(side=tk.LEFT, padx=5)
        
        self.offset_x, self.offset_y = 0, 0
        self.bind_drag(frame)
        
        self.root.bind("<Escape>", lambda e: self.on_close())
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.closed = False
        self.update()
    
    def on_close(self):
        self.closed = True
        try:
            if hasattr(self, 'menu') and hasattr(self, 'key'):
                self.menu.remove_widget(self.key)
        except:
            pass
        try:
            self.root.destroy()
        except:
            pass
    
    def bind_drag(self, widget):
        widget.bind("<Button-3>", self.start_drag)
        widget.bind("<B3-Motion>", self.drag_window)
    
    def start_stop(self):
        if self.running:
            self.running = False
            self.start_btn.config(text="Старт")
        else:
            self.running = True
            self.start_time = time.time() - self.elapsed
            self.start_btn.config(text="Стоп")
    
    def reset(self):
        self.running = False
        self.elapsed = 0
        self.start_btn.config(text="Старт")
        self.update()
    
    def update(self):
        if hasattr(self, 'closed') and self.closed:
            return
        if self.running:
            self.elapsed = time.time() - self.start_time
        
        hours = int(self.elapsed // 3600)
        minutes = int((self.elapsed % 3600) // 60)
        seconds = int(self.elapsed % 60)
        milliseconds = int((self.elapsed % 1) * 1000)
        
        self.label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}")
        self.root.after(10, self.update)
    
    def start_drag(self, event):
        self.offset_x, self.offset_y = event.x, event.y
    
    def drag_window(self, event):
        x = self.root.winfo_x() + event.x - self.offset_x
        y = self.root.winfo_y() + event.y - self.offset_y
        self.root.geometry(f"+{x}+{y}")

class SlotMachineWidget:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.9)
        self.root.configure(bg="#1a1a1a")
        
        self.root.geometry("400x300")
        
        frame = tk.Frame(self.root, bg="#1a1a1a")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(frame, text="СЛОТЫ", bg="#1a1a1a", fg="#0ff", font=("Courier", 16, "bold")).pack(pady=5)
        
        reels_frame = tk.Frame(frame, bg="#1a1a1a")
        reels_frame.pack(pady=10)
        
        self.symbols = ["🍒", "🍋", "🔔", "⭐", "💎", "7️⃣"]
        self.reels = []
        self.reel_labels = []
        
        for i in range(3):
            reel_frame = tk.Frame(reels_frame, bg="#000", relief=tk.RAISED, bd=2)
            reel_frame.pack(side=tk.LEFT, padx=5)
            
            label = tk.Label(reel_frame, text="?", bg="#000", fg="#0ff", 
                           font=("Courier", 40, "bold"), width=3, height=2)
            label.pack(padx=5, pady=5)
            
            self.reels.append(0)
            self.reel_labels.append(label)
        
        self.result_label = tk.Label(frame, text="", bg="#1a1a1a", fg="#0f0", 
                                    font=("Courier", 12, "bold"))
        self.result_label.pack(pady=5)
        
        btn_frame = tk.Frame(frame, bg="#1a1a1a")
        btn_frame.pack()
        
        self.spin_btn = tk.Button(btn_frame, text="крутить", command=self.spin, 
                                 bg="#333", fg="#fff", bd=0, width=12, font=("Courier", 12))
        self.spin_btn.pack(side=tk.LEFT, padx=5)
        
        self.spinning = False
        self.spin_count = 0
        
        self.offset_x, self.offset_y = 0, 0
        self.bind_drag(frame)
        
        self.root.bind("<Escape>", lambda e: self.on_close())
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def on_close(self):
        self.closed = True
        try:
            if hasattr(self, 'menu') and hasattr(self, 'key'):
                self.menu.remove_widget(self.key)
        except:
            pass
        try:
            self.root.destroy()
        except:
            pass
    
    def bind_drag(self, widget):
        widget.bind("<Button-3>", self.start_drag)
        widget.bind("<B3-Motion>", self.drag_window)
    
    def spin(self):
        if self.spinning or (hasattr(self, 'closed') and self.closed):
            return
        
        self.spinning = True
        self.spin_btn.config(state=tk.DISABLED, text="бэм бэм бэм...")
        self.result_label.config(text="")
        self.spin_count = 0
        
        self.animate_spin()
    
    def animate_spin(self):
        if hasattr(self, 'closed') and self.closed:
            return
        if self.spin_count < 20:
            for i in range(3):
                self.reels[i] = random.randint(0, len(self.symbols) - 1)
                self.reel_labels[i].config(text=self.symbols[self.reels[i]])
            self.spin_count += 1
            self.root.after(50, self.animate_spin)
        else:
            self.finalize_spin()
    
    def finalize_spin(self):
        for i in range(3):
            self.reels[i] = random.randint(0, len(self.symbols) - 1)
            self.reel_labels[i].config(text=self.symbols[self.reels[i]])
        
        if self.reels[0] == self.reels[1] == self.reels[2]:
            if self.reels[0] == 5:
                self.result_label.config(text="занос", fg="#ff0")
            else:
                self.result_label.config(text="выигрыш", fg="#0f0")
        elif self.reels[0] == self.reels[1] or self.reels[1] == self.reels[2] or self.reels[0] == self.reels[2]:
            self.result_label.config(text="малый выигрыш", fg="#0ff")
        else:
            self.result_label.config(text="еще посидим", fg="#f00")
        
        self.spinning = False
        self.spin_btn.config(state=tk.NORMAL, text="крутить")
    
    def start_drag(self, event):
        self.offset_x, self.offset_y = event.x, event.y
    
    def drag_window(self, event):
        x = self.root.winfo_x() + event.x - self.offset_x
        y = self.root.winfo_y() + event.y - self.offset_y
        self.root.geometry(f"+{x}+{y}")

class ArtApp:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.overrideredirect(True)      
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.9) 
        self.root.configure(bg="black")

        self.speed_val = 0.05
        self.is_paused = False
        
        self.snake_modes = {
            "binary": "01",
            "hex": "0123456789ABCDEF",
            "digits": "0123456789",
            "ascii": string.ascii_letters + string.digits,
            "symbols": "!@#$%^&*()_+-=[]{}|;:,.<>?/~`",
            "matrix": "01",
            "word": None
        }
        self.current_mode = "binary"
        self.snake_chars = self.snake_modes[self.current_mode]
        self.word_mode_word = "SNAKE"
        self.word_mode_index = 0

        self.text_area = tk.Text(self.root, width=width, height=height, 
                                 bg="black", font=("Courier", 12, "bold"),
                                 borderwidth=0, highlightthickness=0,
                                 state=tk.DISABLED, cursor="arrow")
        self.text_area.pack(padx=5, pady=5)
        
        self.colors = ["#ff00ff", "#00ffff", "#ffff00", "#ff0000", "#00ff00", "#ff8800"]
        for i, color in enumerate(self.colors):
            self.text_area.tag_configure(f"col{i}", foreground=color)

        self.input_frame = tk.Frame(self.root, bg="#111")
        self.input_frame.pack(fill=tk.X, padx=5, pady=2)

        self.entry = tk.Entry(self.input_frame, bg="#111", fg="white", borderwidth=0, 
                              insertbackground="white", font=("Courier", 11))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.entry.bind("<Return>", lambda e: self.handle_input())

        self.clock_label = tk.Label(self.input_frame, text="", bg="#111", fg="#555", font=("Courier", 10))
        self.clock_label.pack(side=tk.RIGHT, padx=5)

        self.widget_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.mode_label = tk.Label(self.widget_frame, text="MODE: BINARY", bg="#1a1a1a", fg="#0ff", font=("Courier", 8))
        self.mode_label.pack(side=tk.LEFT, padx=10)
        tk.Button(self.widget_frame, text="CLEAR", command=self.clear_all, bg="#222", fg="#fff", bd=0).pack(side=tk.RIGHT, padx=5)
        
        self.control_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.control_frame.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(self.control_frame, text="Mode:", bg="#1a1a1a", fg="#fff", font=("Courier", 9)).pack(side=tk.LEFT, padx=5)
        
        self.mode_combo = ttk.Combobox(self.control_frame, values=list(self.snake_modes.keys()), 
                                       state="readonly", width=12, font=("Courier", 9))
        self.mode_combo.set(self.current_mode)
        self.mode_combo.pack(side=tk.LEFT, padx=5)
        self.mode_combo.bind("<<ComboboxSelected>>", self.change_mode)
        
        tk.Label(self.control_frame, text="Word:", bg="#1a1a1a", fg="#fff", font=("Courier", 9)).pack(side=tk.LEFT, padx=(10, 5))
        
        self.word_entry = tk.Entry(self.control_frame, bg="#222", fg="white", borderwidth=1, 
                                   insertbackground="white", font=("Courier", 9), width=15)
        self.word_entry.pack(side=tk.LEFT, padx=5)
        self.word_entry.insert(0, self.word_mode_word)
        self.word_entry.bind("<Return>", lambda e: self.apply_word())
        
        self.word_button = tk.Button(self.control_frame, text="Apply", command=self.apply_word, 
                                    bg="#333", fg="#fff", bd=0, font=("Courier", 8))
        self.word_button.pack(side=tk.LEFT, padx=5)
        
        self.update_word_visibility()

        self.offset_x, self.offset_y = 0, 0
        for widget in [self.root, self.text_area, self.input_frame, self.clock_label]:
            widget.bind("<Button-3>", self.start_drag)
            widget.bind("<B3-Motion>", self.drag_window)

        self.root.bind("<space>", lambda e: self.toggle_pause())
        self.root.bind("<Escape>", lambda e: self.on_close())
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.canvas = [[(" ", "col0") for _ in range(width)] for _ in range(height)]
        self.snake_body = deque()
        self.sx, self.sy = width // 2, height // 2
        self.dx, self.dy = 1, 0
        self.auto_mode = False
        self.snake_positions = set()
        self.closed = False

        self.update_clock()
        threading.Thread(target=self.snake_logic, daemon=True).start()

    def on_close(self):
        self.closed = True
        try:
            if hasattr(self, 'menu') and hasattr(self, 'key'):
                self.menu.remove_widget(self.key)
        except:
            pass
        try:
            self.root.destroy()
        except:
            pass

    def start_drag(self, event):
        self.offset_x, self.offset_y = event.x, event.y

    def drag_window(self, event):
        x = self.root.winfo_x() + event.x - self.offset_x
        y = self.root.winfo_y() + event.y - self.offset_y
        self.root.geometry(f"+{x}+{y}")

    def update_clock(self):
        if hasattr(self, 'closed') and self.closed:
            return
        try:
            self.clock_label.config(text=time.strftime("%H:%M:%S"))
            self.root.after(1000, self.update_clock)
        except:
            pass

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused: 
            self.widget_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=2)
        else: 
            self.widget_frame.pack_forget()
    
    def change_mode(self, event=None):
        selected_mode = self.mode_combo.get()
        if selected_mode and selected_mode in self.snake_modes:
            self.set_snake_mode(selected_mode)
            self.update_word_visibility()
    
    def apply_word(self):
        word = self.word_entry.get().strip().upper()
        if word:
            self.word_mode_word = word
            self.word_mode_index = 0
            if self.current_mode == "word":
                self.set_snake_mode("word")
    
    def update_word_visibility(self):
        if self.current_mode == "word":
            self.word_entry.config(state=tk.NORMAL)
            self.word_button.config(state=tk.NORMAL)
        else:
            self.word_entry.config(state=tk.DISABLED)
            self.word_button.config(state=tk.DISABLED)

    def clear_all(self):
        self.canvas = [[(" ", "col0") for _ in range(width)] for _ in range(height)]
        self.snake_body.clear()
        self.snake_positions.clear()
        self.update_display()
    
    def set_snake_mode(self, mode):
        if mode in self.snake_modes:
            self.current_mode = mode
            if mode == "word":
                self.word_mode_index = 0
                if hasattr(self, 'word_mode_word') and self.word_mode_word:
                    self.snake_chars = self.word_mode_word
                else:
                    self.snake_chars = "SNAKE"
            else:
                self.snake_chars = self.snake_modes[mode]
            
            if hasattr(self, 'mode_combo'):
                self.mode_combo.set(mode)
            
            mode_display = mode.upper()
            if mode == "word" and hasattr(self, 'word_mode_word'):
                mode_display += f" ({self.word_mode_word})"
            self.mode_label.config(text=f"MODE: {mode_display}")
            
            if hasattr(self, 'word_entry'):
                self.update_word_visibility()
            
            return True
        return False
    
    def get_snake_char(self):
        if self.current_mode == "word":
            char = self.word_mode_word[self.word_mode_index % len(self.word_mode_word)]
            self.word_mode_index = (self.word_mode_index + 1) % len(self.word_mode_word)
            return char
        else:
            return random.choice(self.snake_chars)

    def handle_input(self):
        word = self.entry.get().strip()
        self.entry.delete(0, tk.END)
        if not word:
            self.auto_mode = not self.auto_mode
            if self.auto_mode: self.sx, self.sy = width // 2, height // 2
        elif word.lower().startswith("mode "):
            parts = word.split()
            if len(parts) >= 2:
                mode_name = parts[1].lower()
                if len(parts) >= 3 and mode_name == "word":
                    self.word_mode_word = " ".join(parts[2:]).upper()
                    self.word_mode_index = 0
                if self.set_snake_mode(mode_name):
                    mode_display = mode_name.upper()
                    if mode_name == "word":
                        mode_display += f" ({self.word_mode_word})"
                    print(f"Режим змейки: {mode_display}")
        elif word.lower().startswith("word "):
            self.word_mode_word = word[5:].upper()
            self.word_mode_index = 0
            if self.set_snake_mode("word"):
                print(f"Режим змейки: WORD ({self.word_mode_word})")
        else:
            x, y = random.randint(0, max(0, width-len(word))), random.randint(0, height-1)
            tag = f"col{random.randint(0, 5)}"
            for i, c in enumerate(word):
                if x+i < width: self.canvas[y][x+i] = (c.upper(), tag)
            self.update_display()

    def update_display(self):
        self.text_area.configure(state=tk.NORMAL)
        self.text_area.delete("1.0", tk.END)
        for row in self.canvas:
            for char, tag in row:
                self.text_area.insert(tk.END, char, tag)
            self.text_area.insert(tk.END, "\n")
        self.text_area.configure(state=tk.DISABLED)

    def snake_logic(self):
        while True:
            if hasattr(self, 'closed') and self.closed:
                break
            if self.auto_mode and not self.is_paused:
                self.sx %= width
                self.sy %= height
                
                if (self.sx, self.sy) in self.snake_positions:
                    while self.snake_body:
                        tx, ty = self.snake_body.popleft()
                        self.snake_positions.discard((tx, ty))
                        rx, ry = random.randint(0, width-1), random.randint(0, height-1)
                        self.canvas[ry][rx] = (random.choice(string.ascii_uppercase), f"col{random.randint(0, 5)}")
                        self.canvas[ty][tx] = (" ", "col0")
                    self.snake_positions.clear()
                    self.sx, self.sy = random.randint(0, width-1), random.randint(0, height-1)
                    time.sleep(0.2)
                    continue

                tag = f"col{random.randint(0, 5)}"
                self.canvas[self.sy][self.sx] = (self.get_snake_char(), tag)
                self.snake_body.append((self.sx, self.sy))
                self.snake_positions.add((self.sx, self.sy))
                
                if len(self.snake_body) > 15:
                    tx, ty = self.snake_body.popleft()
                    self.snake_positions.discard((tx, ty))
                    if self.canvas[ty][tx][0] != " ":
                        self.canvas[ty][tx] = (" ", "col0")

                if random.random() < 0.1:
                    new_move = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
                    if not (new_move[0] == -self.dx and new_move[1] == -self.dy):
                        self.dx, self.dy = new_move[0], new_move[1]

                self.sx = (self.sx + self.dx) % width
                self.sy = (self.sy + self.dy) % height
                try:
                    self.root.after(0, self.update_display)
                except:
                    pass
                time.sleep(self.speed_val)
            else:
                time.sleep(0.1)

if __name__ == "__main__":
    menu = WidgetMenu()
    menu.root.mainloop()
