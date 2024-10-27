from enum import Enum, auto


class UserTypes(Enum):

    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

    INTERNAL = auto()
    CLIENT = auto()

    @classmethod
    def choices(cls):
        return tuple((i.value, i.name) for i in cls)


class ClientTypes(Enum):

    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

    INDIVIDUAL = auto()
    COMPANY = auto()

    @classmethod
    def choices(cls):
        return tuple((i.value, i.name) for i in cls)
