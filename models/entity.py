from abc import ABC, abstractmethod


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