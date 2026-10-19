import threading
import time
import pyautogui

from models.entity import Entity
from models.scenario import Scenario


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