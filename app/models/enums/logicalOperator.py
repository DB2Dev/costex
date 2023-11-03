from enum import Enum, auto


class LogicalOperator(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

    OR = auto()
    AND = auto()
