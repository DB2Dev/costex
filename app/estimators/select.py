import math


def file_scan(numOfBlocks: int) -> int:
    return numOfBlocks / 2


def binary_search_equal(numOfBlocks: int) -> int:
    return math.log2(numOfBlocks)


def binary_search_range(numOfBlocks: int, cardinality: int, bfr: int) -> int:
    return math.log2(numOfBlocks) + (cardinality / bfr) - 1


def primary_index_equal(height: int) -> int:
    return height + 1


def primary_index_range(height: int, numOfBlocks: int) -> int:
    return height + (numOfBlocks / 2)


def clustering_index(height: int, cardinality: int, bfr: int) -> int:
    return height + (cardinality / bfr)


def secondary_index_equal(height: int, cardinality: int) -> int:
    return height + 1 + cardinality


def secondary_index_range(height: int, first_level_blocks: int, numOfTuples) -> int:
    return height + (first_level_blocks / 2) + (numOfTuples / 2)
