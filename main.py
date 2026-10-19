import flet as ft
from ui import App


def main(page: ft.Page):
    app = App(page)
    page.on_close = app.on_close


if __name__ == "__main__":
    ft.run(main)