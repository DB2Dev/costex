from enum import Enum, auto


class AlgoChoice(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

    FILE_SCAN = auto()
    BINARY_SEARCH = auto()
    PRIMARY_INDEX = auto()
    CLUSTERED_INDEX = auto()
    SECONDARY_INDEX = auto()
    NESTED_LOOP_JOIN = auto()
    INDEXED_NESTED_LOOP_JOIN = auto()
    SORT_MERGE_JOIN = auto()
