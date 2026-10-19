from datetime import datetime
from models.entity import Entity


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