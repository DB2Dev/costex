from enum import Enum, auto


class TableType(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

    PROJECT = auto()
    EMPLOYEE = auto()
