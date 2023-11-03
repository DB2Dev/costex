from enum import Enum, auto


class QueryType(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

    EQUALITY = auto()
    RANGE = auto()
