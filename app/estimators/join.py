import math
from app.models.enums.tableType import TableType

from app.models.metadata.distributions import Distributions
from app.models.metadata.tables_info import TablesDetails


def join_selectivity(ndv_a: int, ndv_b: int) -> float:
    return 1 / max(ndv_a, ndv_b)

# don't need to calculate


def join_cardinality(table1_name: TableType, table2_name: TableType, ndv_a: int, ndv_b: int) -> int:
    return math.ceil(join_selectivity(ndv_a, ndv_b) * TablesDetails.get_no_of_records(table1_name), TablesDetails.get_no_of_records(table2_name))


def bfr_result() -> int:
    dist = Distributions()
    record_size = 0
    for i in dist:
        if i[1] != 'mgr_ssn':
            record_size += i[2]
    block_size = 8192
    return math.floor(block_size / record_size)


def nested_loop_join(table1_name: TableType, table2_name: TableType, ndv_a: int, ndv_b: int):
    return TablesDetails.get_no_of_blocks(table1_name) \
        + (TablesDetails.get_no_of_blocks(table1_name) * TablesDetails.get_no_of_blocks(table2_name)) \
        + (join_cardinality(table1_name, table2_name, ndv_a, ndv_b) / bfr_result)


def indexed_nested_loop_join(table1_name: TableType, table2_name: TableType, ndv_a: int, ndv_b: int, height_b: int = 10):
    return TablesDetails.get_no_of_blocks(table1_name) \
        + (TablesDetails.get_no_of_records(table1_name) * (height_b + 1 + TablesDetails.get_no_of_records(table2_name))) \
        + (join_cardinality(table1_name, table2_name, ndv_a, ndv_b) / bfr_result)


def sort_merge_join(table1_name: TableType, table2_name: TableType, ndv_a: int, ndv_b: int):
    return TablesDetails.get_no_of_blocks(table1_name) \
        + TablesDetails.get_no_of_blocks(table2_name) \
        + (join_cardinality(table1_name, table2_name, ndv_a, ndv_b) / bfr_result)
