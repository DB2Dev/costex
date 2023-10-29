class Table:
    def __init__(self, name, total_records, primary_key):
        self.name = name
        self.total_records = total_records
        self.primary_key = primary_key
        self.columns = {}  # Dictionary {column_name: Column object}

    def add_column(self, column):
        self.columns[column.name] = column


class Column:
    def __init__(self, name, distribution, has_index=False, index_type=None):
        self.name = name
        self.distribution = distribution  # could be a histogram or other data structure
        self.has_index = has_index
        self.index_type = index_type
