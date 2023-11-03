from enum import Enum, auto


class QueryOperation(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

    SELECT = auto()
    JOIN = auto()
