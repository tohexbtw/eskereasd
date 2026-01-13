import flet as ft
import asyncio
import json
import os

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"habits": [], "tasks": [], "state": None}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main(page: ft.Page):
    page.title = "lifemng"
    page.window_width = 420
    page.window_height = 720
    page.bgcolor = "#0f172a"
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.START

    data = load_data()

    # ---------- HELPERS ----------
    def refresh():
        habits_column.controls.clear()
        tasks_column.controls.clear()

        for h in data["habits"]:
            habits_column.controls.append(habit_tile(h))

        for t in data["tasks"]:
            tasks_column.controls.append(task_tile(t))

        # Animate progress bar change
        old_value = progress_bar.value
        new_value = calc_progress()
        
        async def animate_progress():
            step = (new_value - old_value) / 10
            current = old_value
            for _ in range(10):
                current += step
                progress_bar.value = current
                page.update()
                await asyncio.sleep(20)
            progress_bar.value = new_value
            progress_bar.color = (
                "#ef4444" if new_value < 0.33
                else "#facc15" if new_value < 0.66
                else "#22c55e"
            )
            page.update()
        
        asyncio.create_task(animate_progress())

        state_label.value = f"State of your day: {data.get('state') or '—'}"
        save_data(data)

    def calc_progress():
        total = len(data["habits"]) + len(data["tasks"])
        if total == 0:
            return 0
        done = sum(1 for h in data["habits"] if h["done"]) + sum(1 for t in data["tasks"] if t["done"])
        return done / total

    # ---------- HABITS ----------
    def habit_tile(habit):
        checkbox = ft.Checkbox(
            value=habit["done"],
            on_change=lambda e, h=habit: toggle_habit(h),
            scale=1.5,
            active_color="#6366f1",
        )
        text = ft.Text(
            habit["title"], 
            color="white", 
            expand=True,
            style=ft.TextStyle(
                decoration=ft.TextDecoration.LINE_THROUGH if habit["done"] else None,
                color="#94a3b8" if habit["done"] else "white"
            )
        )
        delete_btn = ft.IconButton(
            icon="delete",
            icon_color="white",
            on_click=lambda e, h=habit: remove_habit(h)
        )
        row = ft.Row([checkbox, text, delete_btn], 
                     vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        # Create container with animation properties
        container = ft.Container(
            content=row,
            padding=10,
            border_radius=12,
            bgcolor="#1e293b" if habit["done"] else "#020617",
            animate_opacity=300,
            animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            opacity=0,  # Start invisible
            scale=1.0,
        )
        
        # Animate appearance after adding to page
        async def animate_appearance():
            await asyncio.sleep(0.1)
            container.opacity = 1
            page.update()
        
        asyncio.create_task(animate_appearance())
        return container

    def remove_habit(habit):
        # Animate removal
        for ctrl in habits_column.controls[:]:
            if isinstance(ctrl.content, ft.Row):
                row_items = ctrl.content.controls
                if len(row_items) >= 2 and isinstance(row_items[1], ft.Text):
                    if row_items[1].value == habit["title"]:
                        # Shrink and fade out animation
                        async def animate_removal():
                            ctrl.scale = 0.9
                            ctrl.opacity = 0
                            page.update()
                            await asyncio.sleep(0.3)
                            data["habits"].remove(habit)
                            refresh()
                        asyncio.create_task(animate_removal())
                        return
        
        # If animation didn't trigger, just remove
        data["habits"].remove(habit)
        refresh()

    def toggle_habit(habit):
        habit["done"] = not habit["done"]
        
        # Find and animate the container
        for ctrl in habits_column.controls:
            if isinstance(ctrl.content, ft.Row):
                row_items = ctrl.content.controls
                if len(row_items) >= 2 and isinstance(row_items[1], ft.Text):
                    if row_items[1].value == habit["title"]:
                        text = row_items[1]
                        
                        async def animate_toggle():
                            # Scale up animation
                            ctrl.scale = 1.1
                            page.update()
                            await asyncio.sleep(150)
                            
                            # Scale back down
                            ctrl.scale = 1.0
                            
                            # Update visual state
                            if habit["done"]:
                                ctrl.bgcolor = "#1e293b"
                                text.style = ft.TextStyle(
                                    color="#94a3b8",
                                    decoration=ft.TextDecoration.LINE_THROUGH,
                                    decoration_color="#94a3b8",
                                )
                            else:
                                ctrl.bgcolor = "#020617"
                                text.style = ft.TextStyle(color="white")
                            
                            page.update()
                            refresh()
                        
                        asyncio.create_task(animate_toggle())
                        return
        
        refresh()

    def add_habit(e):
        if habit_input.value.strip():
            data["habits"].append({"title": habit_input.value.strip(), "done": False})
            habit_input.value = ""
            refresh()

    # ---------- TASKS ----------
    def task_tile(task):
        checkbox = ft.Checkbox(
            value=task["done"],
            on_change=lambda e, t=task: toggle_task(t),
            scale=1.5,
            active_color="#6366f1",
        )
        text = ft.Text(
            task["title"], 
            color="white", 
            expand=True,
            style=ft.TextStyle(
                decoration=ft.TextDecoration.LINE_THROUGH if task["done"] else None,
                color="#94a3b8" if task["done"] else "white"
            )
        )
        delete_btn = ft.IconButton(
            icon="delete",
            icon_color="white",
            on_click=lambda e, t=task: remove_task(t)
        )
        row = ft.Row([checkbox, text, delete_btn], 
                     vertical_alignment=ft.CrossAxisAlignment.CENTER)
        
        # Create container with animation properties
        container = ft.Container(
            content=row,
            padding=10,
            border_radius=12,
            bgcolor="#1e293b" if task["done"] else "#020617",
            animate_opacity=300,
            animate_scale=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            opacity=0,  # Start invisible
            scale=1.0,
        )
        
        # Animate appearance after adding to page
        async def animate_appearance():
            await asyncio.sleep(0.1)
            container.opacity = 1
            page.update()
        
        asyncio.create_task(animate_appearance())
        return container

    def remove_task(task):
        # Animate removal
        for ctrl in tasks_column.controls[:]:
            if isinstance(ctrl.content, ft.Row):
                row_items = ctrl.content.controls
                if len(row_items) >= 2 and isinstance(row_items[1], ft.Text):
                    if row_items[1].value == task["title"]:
                        # Shrink and fade out animation
                        async def animate_removal():
                            ctrl.scale = 0.9
                            ctrl.opacity = 0
                            page.update()
                            await asyncio.sleep(0.3)
                            data["tasks"].remove(task)
                            refresh()
                        asyncio.create_task(animate_removal())
                        return
        
        # If animation didn't trigger, just remove
        data["tasks"].remove(task)
        refresh()

    def toggle_task(task):
        task["done"] = not task["done"]
        
        # Find and animate the container
        for ctrl in tasks_column.controls:
            if isinstance(ctrl.content, ft.Row):
                row_items = ctrl.content.controls
                if len(row_items) >= 2 and isinstance(row_items[1], ft.Text):
                    if row_items[1].value == task["title"]:
                        text = row_items[1]
                        
                        async def animate_toggle():
                            # Scale up animation
                            ctrl.scale = 1.1
                            page.update()
                            await asyncio.sleep(150)
                            
                            # Scale back down
                            ctrl.scale = 1.0
                            
                            # Update visual state
                            if task["done"]:
                                ctrl.bgcolor = "#1e293b"
                                text.style = ft.TextStyle(
                                    color="#94a3b8",
                                    decoration=ft.TextDecoration.LINE_THROUGH,
                                    decoration_color="#94a3b8",
                                )
                            else:
                                ctrl.bgcolor = "#020617"
                                text.style = ft.TextStyle(color="white")
                            
                            page.update()
                            refresh()
                        
                        asyncio.create_task(animate_toggle())
                        return
        
        refresh()

    def add_task(e):
        if task_input.value.strip():
            data["tasks"].append({"title": task_input.value.strip(), "done": False})
            task_input.value = ""
            refresh()

    # ---------- STATE ----------
    def set_state(state):
        data["state"] = state
        
        # Reset all button colors first
        for btn in state_buttons_row.controls:
            if isinstance(btn, ft.ElevatedButton):
                if "OK" in btn.text:
                    btn.bgcolor = "#22c55e"
                elif "Tired" in btn.text:
                    btn.bgcolor = "#f59e0b"
                elif "Crashout" in btn.text:
                    btn.bgcolor = "#a855f7"
        
        # Highlight the selected button
        for btn in state_buttons_row.controls:
            if isinstance(btn, ft.ElevatedButton):
                if (state == "ok" and "OK" in btn.text) or \
                   (state == "tired" and "Tired" in btn.text) or \
                   (state == "crashout" and "Crashout" in btn.text):
                    btn.bgcolor = "#ffffff"
                    btn.text = "✓"
                    
                    # Reset after animation
                    async def reset_button():
                        await asyncio.sleep(300)
                        if state == "ok":
                            btn.bgcolor = "#22c55e"
                            btn.text = "OK"
                        elif state == "tired":
                            btn.bgcolor = "#f59e0b"
                            btn.text = "Tired"
                        elif state == "crashout":
                            btn.bgcolor = "#a855f7"
                            btn.text = "Crashout"
                        page.update()
                    
                    asyncio.create_task(reset_button())
                    break
        
        refresh()

    # ---------- UI ELEMENTS ----------
    title = ft.Text("lifemng", size=28, weight=ft.FontWeight.BOLD, color="white")
    progress_bar = ft.ProgressBar(
        value=0, 
        bgcolor="#020617", 
        color="#6366f1", 
        height=8,
    )
    state_label = ft.Text("State of your day: —", color="#94a3b8")

    habit_input = ft.TextField(
        hint_text="New habit", 
        bgcolor="#020617",
        border_radius=12, 
        text_style=ft.TextStyle(color="white"),
        on_submit=add_habit
    )
    task_input = ft.TextField(
        hint_text="New task", 
        bgcolor="#020617",
        border_radius=12, 
        text_style=ft.TextStyle(color="white"),
        on_submit=add_task
    )

    habits_column = ft.Column(spacing=10)
    tasks_column = ft.Column(spacing=10)
    
    # Create state buttons row with proper references
    state_buttons_row = ft.Row([
        ft.ElevatedButton("OK", on_click=lambda e: set_state("ok"), bgcolor="#22c55e"),
        ft.ElevatedButton("Tired", on_click=lambda e: set_state("tired"), bgcolor="#f59e0b"),
        ft.ElevatedButton("Crashout", on_click=lambda e: set_state("crashout"), bgcolor="#a855f7"),
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    # Create the main scrollable column
    main_column = ft.Column(
        [
            title,
            progress_bar,
            ft.Container(height=10),
            state_label,
            state_buttons_row,
            ft.Container(height=20),
            ft.Text("Habits", size=20, color="white"),
            habit_input,
            ft.ElevatedButton("Add Habit", on_click=add_habit),
            habits_column,
            ft.Container(height=20),
            ft.Text("Tasks", size=20, color="white"),
            task_input,
            ft.ElevatedButton("Add Task", on_click=add_task),
            tasks_column,
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
    
    page.add(main_column)

    refresh()

ft.app(target=main)