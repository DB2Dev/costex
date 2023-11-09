import math


def file_scan(numOfBlocks: int = 55) -> int:
    return numOfBlocks / 2


def binary_search_equal(numOfBlocks: int) -> int:
    return math.log2(numOfBlocks)


def binary_search_range(numOfBlocks: int, selectivity: int, bfr: int) -> int:
    return math.log2(numOfBlocks) + (selectivity / bfr) - 1


# primary index
# secondary index
# clustered index

# range query
# equality query
