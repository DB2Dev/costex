from app.models.enums.tableType import TableType
from app.models.metadata.distributions import Distributions
from app.models.enums.queryType import QueryType
from app.models.column import Column
from app.models.metadata.tables_info import TablesDetails


def cardinality(attr: Column, table_name: TableType, query_type: QueryType) -> float:
    if query_type == QueryType.EQUALITY and attr.is_unique:
        return 1
    elif query_type == QueryType.EQUALITY and not attr.is_unique:
        for row in Distributions():
            if row[0] == table_name.value:
                no_of_distinct = row[3]
        return TablesDetails.get_no_of_records(table_name) / no_of_distinct
    elif query_type == QueryType.RANGE:
        return TablesDetails.get_no_of_records(table_name) / 2
