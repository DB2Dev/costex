from app.models.enums.tableType import TableType

# if unique+equality -> cardinality = 1
# if non unique + equality -> cardinality = no of tuples / distinct  (on average)
# if range average r/2

def cardinality(attr_name: str, table_name: TableType) -> float:
    pass

