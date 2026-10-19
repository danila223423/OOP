import flet as ft

from models import Click, Scenario, User, Clicker
from services import save_report


class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.user = User("UserName")
        self.scenario = Scenario("Main")
        self.clicker = Clicker()

        for i in range(10):
            self.scenario.add(Click(f"Click-{i+1}", 100 + i * 40, 200 + i * 30, 0.3))

        self._build_ui()
        self._refresh_list()

    def _build_ui(self):
        self.status = ft.Text("Готов", color=ft.Colors.BLUE)
        self.counter = ft.Text(f"Кликов: {self.clicker.count}")
        self.xf = ft.TextField(label="X", value="500", width=90)
        self.yf = ft.TextField(label="Y", value="400", width=90)
        self.df = ft.TextField(label="Задержка", value="0.3", width=110)
        self.rf = ft.TextField(label="Повторов", value="2", width=100)
        self.list_view = ft.ListView(height=180, spacing=3)

        self.btn_start = ft.Button("▶ Старт", on_click=self.on_start)
        self.btn_stop = ft.Button("■ Стоп", on_click=self.on_stop, disabled=True)
        self.btn_pick = ft.OutlinedButton("📍 Позиция курсора", on_click=self.on_pick)
        self.btn_add = ft.OutlinedButton("➕ Добавить", on_click=self.on_add)
        self.btn_clear = ft.OutlinedButton("🗑 Очистить", on_click=self.on_clear)

        self.page.title = "Автокликер"
        self.page.window.width = 620
        self.page.window.height = 640
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.page.add(
            ft.Text("🖱 Автокликер", size=24, weight=ft.FontWeight.BOLD),
            ft.Text(self.user.describe(), size=12, color=ft.Colors.GREY),
            ft.Divider(),
            ft.Row(
                [self.xf, self.yf, self.df, self.rf],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [self.btn_pick, self.btn_add, self.btn_clear],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Text("Сценарий:", weight=ft.FontWeight.BOLD),
            ft.Container(
                self.list_view,
                border=ft.Border.all(1, ft.Colors.GREY),
                padding=8,
                width=520,
            ),
            ft.Row(
                [self.btn_start, self.btn_stop],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Divider(),
            self.status,
            self.counter,
        )

    def _refresh_list(self):
        self.list_view.controls = [
            ft.Text(f"{i+1}. {c.describe()}", size=12)
            for i, c in enumerate(self.scenario.clicks)
        ]
        self.page.update()

    def on_add(self, e):
        try:
            c = Click(
                f"Click-{len(self.scenario.clicks)+1}",
                int(self.xf.value),
                int(self.yf.value),
                float(self.df.value),
            )
        except ValueError:
            self.status.value = "❌ Неверные данные"
            self.status.color = ft.Colors.RED
            self.page.update()
            return
        self.scenario.add(c)
        self.status.value = f"✅ Добавлено: {c.describe()}"
        self.status.color = ft.Colors.GREEN
        self._refresh_list()

    def on_clear(self, e):
        self.scenario.clear()
        self.status.value = "Сценарий очищен"
        self._refresh_list()

    def on_pick(self, e):
        x, y = Clicker.cursor_pos()
        self.xf.value, self.yf.value = str(x), str(y)
        self.page.update()

    def on_start(self, e):
        try:
            self.scenario.repeat = int(self.rf.value)
        except ValueError:
            self.status.value = "❌ Неверное число повторов"
            self.status.color = ft.Colors.RED
            self.page.update()
            return

        if self.clicker.start(self.scenario):
            self.btn_start.disabled = True
            self.btn_stop.disabled = False
            self.status.value = f"▶ {self.scenario.describe()}"
            self.page.update()

    def on_stop(self, e):
        self.clicker.stop()
        self.btn_start.disabled = False
        self.btn_stop.disabled = True
        self.counter.value = f"Кликов: {self.clicker.count}"
        self.status.value = "■ Остановлено"
        self.page.update()

    def on_close(self, e):
        self.clicker.stop()
        save_report([self.user])