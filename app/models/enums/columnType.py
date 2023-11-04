from enum import Enum, auto


class ColumnType(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

    NUMBER = auto()
    TEXT = auto()
    DATE = auto()
    BOOLEAN = auto()
