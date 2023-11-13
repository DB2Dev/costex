from models.enums.tableType import TableType
from models.metadata.tables_info import TablesDetails


def nested_loop_join(table1_name: TableType, table2_name: TableType):
    return TablesDetails.get_no_of_blocks(table1_name) + (
        TablesDetails.get_no_of_blocks(table1_name)
        * TablesDetails.get_no_of_blocks(table2_name)
    )


def indexed_nested_loop_join(
    table1_name: TableType,
    table2_name: TableType,
    height_b: int = 10,
):
    return TablesDetails.get_no_of_blocks(table1_name) + (
        TablesDetails.get_no_of_records(table1_name)
        * (height_b + 1 + TablesDetails.get_no_of_records(table2_name))
    )


def sort_merge_join(table1_name: TableType, table2_name: TableType):
    return TablesDetails.get_no_of_blocks(table1_name) + TablesDetails.get_no_of_blocks(
        table2_name
    )
