import flet as ft

def main(page: ft.Page):
    page.add(ft.text("hello world"))

    ft.run(target=main, view="web_browser")