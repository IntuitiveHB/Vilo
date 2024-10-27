from enum import Enum, auto


class BoardTypes(Enum):

    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

    GENERAL_USE = auto()
    CLIENT_SPECIFIC = auto()

    @classmethod
    def choices(cls):
        return tuple((i.value, i.name) for i in cls)


class TaskPriorities(Enum):

    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()

    @classmethod
    def choices(cls):
        return tuple((i.value, i.name) for i in cls)
