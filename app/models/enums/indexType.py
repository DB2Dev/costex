from enum import Enum, auto


class IndexType(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

    PRIMARY = auto()
    CLUSTERED = auto()
    SECONDARY = auto()
    NONE = auto()
