from models.entity import Entity


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