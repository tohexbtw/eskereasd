import random
import tkinter as tk
from tkinter import ttk
import threading
import string
import time
import psutil  # системные данные
from collections import deque

try:
    from BlurWindow.blurWindow import blur
except:
    def blur(*args, **kwargs): pass

width, height = 60, 25

class ArtApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)      
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.9) 
        self.root.configure(bg="black")

        # Акриловый эффект
        try: 
            hWnd = self.root.winfo_id()
            blur(hWnd, hexColor='#1a1a1aff', Acrylic=True, Dark=True)
        except: pass

        self.speed_val = 0.05
        self.is_paused = False
        self.snake_chars = "01"

        # Холст (выделение отключено)
        self.text_area = tk.Text(self.root, width=width, height=height, 
                                 bg="black", font=("Courier", 12, "bold"),
                                 borderwidth=0, highlightthickness=0,
                                 state=tk.DISABLED, cursor="arrow")
        self.text_area.pack(padx=5, pady=5)
        
        self.colors = ["#ff00ff", "#00ffff", "#ffff00", "#ff0000", "#00ff00", "#ff8800"]
        for i, color in enumerate(self.colors):
            self.text_area.tag_configure(f"col{i}", foreground=color)

        # Нижняя панель
        self.input_frame = tk.Frame(self.root, bg="#111")
        self.input_frame.pack(fill=tk.X, padx=5, pady=2)

        self.entry = tk.Entry(self.input_frame, bg="#111", fg="white", borderwidth=0, 
                              insertbackground="white", font=("Courier", 11))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.entry.bind("<Return>", lambda e: self.handle_input())

        self.clock_label = tk.Label(self.input_frame, text="", bg="#111", fg="#555", font=("Courier", 10))
        self.clock_label.pack(side=tk.RIGHT, padx=5)

        # ПАНЕЛЬ ВИДЖЕТОВ (CPU/RAM)
        self.widget_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.sys_label = tk.Label(self.widget_frame, text="CPU: 0% | RAM: 0%", bg="#1a1a1a", fg="#0f0", font=("Courier", 8))
        self.sys_label.pack(side=tk.LEFT, padx=10)
        tk.Button(self.widget_frame, text="CLEAR", command=self.clear_all, bg="#222", fg="#fff", bd=0).pack(side=tk.RIGHT, padx=5)

        # ЛОГИКА ПЕРЕМЕЩЕНИЯ (ПКМ за любое место)
        self.offset_x, self.offset_y = 0, 0
        for widget in [self.root, self.text_area, self.input_frame, self.clock_label]:
            widget.bind("<Button-3>", self.start_drag)
            widget.bind("<B3-Motion>", self.drag_window)

        self.root.bind("<space>", lambda e: self.toggle_pause())
        self.root.bind("<Escape>", lambda e: self.root.destroy()) 

        self.canvas = [[(" ", "col0") for _ in range(width)] for _ in range(height)]
        self.snake_body = deque()
        self.sx, self.sy = width // 2, height // 2
        self.dx, self.dy = 1, 0
        self.auto_mode = False

        self.update_clock()
        self.update_sys_stats() # запуск мониторинга
        threading.Thread(target=self.snake_logic, daemon=True).start()

    def start_drag(self, event):
        self.offset_x, self.offset_y = event.x, event.y

    def drag_window(self, event):
        x = self.root.winfo_x() + event.x - self.offset_x
        y = self.root.winfo_y() + event.y - self.offset_y
        self.root.geometry(f"+{x}+{y}")

    def update_sys_stats(self):
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            self.sys_label.config(text=f"CPU: {cpu}% | RAM: {ram}%")
        except: pass
        self.root.after(1000, self.update_sys_stats)

    def update_clock(self):
        self.clock_label.config(text=time.strftime("%H:%M:%S"))
        self.root.after(1000, self.update_clock)

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused: self.widget_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=2)
        else: self.widget_frame.pack_forget()

    def clear_all(self):
        self.canvas = [[(" ", "col0") for _ in range(width)] for _ in range(height)]
        self.snake_body.clear()
        self.update_display()

    def handle_input(self):
        word = self.entry.get().strip()
        self.entry.delete(0, tk.END)
        if not word:
            self.auto_mode = not self.auto_mode
            if self.auto_mode: self.sx, self.sy = width // 2, height // 2
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
            if self.auto_mode and not self.is_paused:
                self.sx %= width
                self.sy %= height
                
                # ИСПРАВЛЕНО: берем только символ (индекс 0) из кортежа
                char_at_pos = self.canvas[self.sy][self.sx][0]
                
                if char_at_pos in self.snake_chars:
                    while self.snake_body:
                        tx, ty = self.snake_body.popleft()
                        rx, ry = random.randint(0, width-1), random.randint(0, height-1)
                        self.canvas[ry][rx] = (random.choice(string.ascii_uppercase), f"col{random.randint(0, 5)}")
                        self.canvas[ty][tx] = (" ", "col0")
                    self.sx, self.sy = random.randint(0, width-1), random.randint(0, height-1)
                    time.sleep(0.2)
                    continue

                tag = f"col{random.randint(0, 5)}"
                self.canvas[self.sy][self.sx] = (random.choice(self.snake_chars), tag)
                self.snake_body.append((self.sx, self.sy))
                
                if len(self.snake_body) > 15:
                    tx, ty = self.snake_body.popleft()
                    # ИСПРАВЛЕНО: проверяем символ
                    if self.canvas[ty][tx][0] in self.snake_chars:
                        self.canvas[ty][tx] = (" ", "col0")

                if random.random() < 0.1:
                    new_move = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
                    if not (new_move[0] == -self.dx and new_move[1] == -self.dy):
                        self.dx, self.dy = new_move[0], new_move[1]

                self.sx = (self.sx + self.dx) % width
                self.sy = (self.sy + self.dy) % height
                self.root.after(0, self.update_display)
                time.sleep(self.speed_val)
            else:
                time.sleep(0.1)

app = ArtApp()
app.root.mainloop()
