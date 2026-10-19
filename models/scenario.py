from models.entity import Entity
from models.click import Click


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