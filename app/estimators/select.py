import math


def file_scan(numOfBlocks: int) -> int:
    return numOfBlocks / 2


def binary_search_equal(numOfBlocks: int) -> int:
    return math.log2(numOfBlocks)


def binary_search_range(numOfBlocks: int, numOfRecords: int, cardinality: int) -> int:
    return math.log2(numOfBlocks) + (cardinality / (numOfRecords / numOfBlocks)) - 1


def primary_index_equal(height: int = 10) -> int:
    return height + 1


def primary_index_range(numOfBlocks: int, height: int = 10) -> int:
    return height + (numOfBlocks / 2)


def clustering_index(cardinality: int, bfr: int, height: int = 10) -> int:
    return height + (cardinality / bfr)


def secondary_index_equal(cardinality: int, height: int = 10) -> int:
    return height + 1 + cardinality


def secondary_index_range(
    numOfTuples, first_level_blocks: int = 400, height: int = 10
) -> int:
    return height + (first_level_blocks / 2) + (numOfTuples / 2)
