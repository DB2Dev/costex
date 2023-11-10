import math


def join_selectivity(ndv_a: int, ndv_b: int) -> float:
    return 1 / max(ndv_a, ndv_b)

# don't need to calculate


def join_cardinality(tup_r: int, tup_s: int, ndv_a: int, ndv_b: int) -> int:
    return math.ceil(join_selectivity(ndv_a, ndv_b) * tup_r * tup_s)


def nested_loop_join(tup_r: int, tup_s: int, ndv_a: int, ndv_b: int):
    pass


def sort_merge_join():
    pass


def indexed_nested_loop_join():
    pass
