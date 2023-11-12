from models.enums.tableType import TableType
from models.metadata.distributions import Distributions
from models.enums.queryType import QueryType
from models.column import Column
from models.metadata.tables_info import TablesDetails


def cardinality(attr: Column, table_name: TableType, query_type: QueryType) -> float:
    if query_type == QueryType.EQUALITY and attr.is_unique:
        return 1
    elif query_type == QueryType.EQUALITY and not attr.is_unique:
        for row in Distributions():
            if row[1] == attr.name:
                no_of_distinct = row[3]
                if no_of_distinct < 0:
                    no_of_distinct = abs(
                        no_of_distinct
                    ) * TablesDetails.get_no_of_records(table_name)
        return TablesDetails.get_no_of_records(table_name) / no_of_distinct
    elif query_type == QueryType.RANGE:
        return TablesDetails.get_no_of_records(table_name) / 2
