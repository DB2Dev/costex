from enum import Enum, auto


class FilterOperator(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

    GT = auto()
    LT = auto()
    EQ = auto()
    NE = auto()
    GE = auto()
    LE = auto()
    BETWEEN = auto()
