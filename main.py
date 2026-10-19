from abc import ABC, abstractmethod
from datetime import datetime
import threading
import time
import flet as ft
import pyautogui


class Entity(ABC):
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, v):
        self._name = v

    @abstractmethod
    def describe(self) -> str:
        ...

    def __eq__(self, other):
        return isinstance(other, Entity) and self._name == other._name

    def __repr__(self):
        return f"{type(self).__name__}({self._name!r})"

    def __str__(self):
        return self.describe()


class Click(Entity):
    def __init__(self, name, x, y, delay=0.3):
        super().__init__(name)
        self._x, self._y, self._delay = x, y, delay

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, v):
        self._x = v

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, v):
        self._y = v

    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, v):
        self._delay = v

    def describe(self):
        return f"{self.name}: ({self.x},{self.y}) задержка {self.delay}s"

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)


class Scenario(Entity):
    def __init__(self, name):
        super().__init__(name)
        self._clicks: list[Click] = []
        self._repeat = 1

    @property
    def clicks(self):
        return self._clicks

    @property
    def repeat(self):
        return self._repeat

    @repeat.setter
    def repeat(self, v):
        self._repeat = max(1, int(v))

    def add(self, click: Click):
        self._clicks.append(click)

    def clear(self):
        self._clicks.clear()

    def describe(self):
        return f"Сценарий «{self.name}»: {len(self._clicks)} кликов × {self.repeat}"

    def __len__(self):
        return len(self._clicks)


class User(Entity):
    def __init__(self, login):
        super().__init__(login)
        self._login = login
        self._time_in = datetime.now()
        self._time_out = None

    @property
    def login(self):
        return self._login

    @property
    def time_in(self):
        return self._time_in

    @property
    def time_out(self):
        return self._time_out

    def logout(self):
        self._time_out = datetime.now()

    def describe(self):
        return f"Пользователь: {self._login}"


class Clicker(Entity):
    def __init__(self, name="Clicker"):
        super().__init__(name)
        self._running = False
        self._stop = threading.Event()
        self._count = 0

    @property
    def running(self):
        return self._running

    @property
    def count(self):
        return self._count

    def _work(self, scenario: Scenario):
        for _ in range(scenario.repeat):
            for c in scenario.clicks:
                if self._stop.is_set():
                    break
                pyautogui.click(x=c.x, y=c.y)
                self._count += 1
                time.sleep(c.delay)
        self._running = False

    def start(self, scenario: Scenario):
        if self._running or not scenario.clicks:
            return False
        self._stop.clear()
        self._running = True
        threading.Thread(target=self._work, args=(scenario,), daemon=True).start()
        return True

    def stop(self):
        self._stop.set()
        self._running = False

    def describe(self):
        return f"Кликер, выполнено {self._count} кликов"

    @staticmethod
    def cursor_pos():
        return pyautogui.position()


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

    def save_report(self):
        if self.user.time_out is None:
            self.user.logout()
        with open("report.txt", "w", encoding="utf-8") as f:
            f.write("+--- | login | time_in | time_out |\n")
            f.write("|---|---|---|\n")
            f.write(
                f"| {self.user.login} "
                f"| {self.user.time_in:%d.%m.%Y %H:%M:%S} "
                f"| {self.user.time_out:%d.%m.%Y %H:%M:%S} |\n"
            )
            f.write("+---\n")

    def on_close(self, e):
        self.clicker.stop()
        self.save_report()


def main(page: ft.Page):
    app = App(page)
    page.on_close = app.on_close


if __name__ == "__main__":
    ft.run(main)