from pydantic import BaseModel
from typing import List
from config import db
from models.enums.tableType import TableType
from models.enums.indexType import IndexType


class Index(BaseModel):
    table_name: TableType
    name: str
    column: str
    index_type: IndexType

    def to_dict(self):
        return {
            "table_name": self.table_name.value,
            "name": self.name,
            "column": self.column,
            "index_type": self.index_type.value,
        }


class Indexes(BaseModel):
    indexes: List[Index] = []

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Indexes, cls).__new__(cls)
            cls.indexes: List[Index] = []
            cls.set_indexes()
        return cls.indexes

    @classmethod
    def set_indexes(cls):
        connection = db.get_connection()
        cursor = connection.cursor()

        select_query = "SELECT * FROM indexes_details;"

        cursor.execute(select_query)

        rows = cursor.fetchall()
        cls.indexes = [
            Index(
                table_name=TableType.EMPLOYEE
                if row[0] == "employee"
                else TableType.PROJECT,
                name=row[1],
                column=row[2][0],
                index_type=Indexes.get_index_type(row[3:]),
            )
            for row in rows
        ]
        cursor.close()
        connection.close()

    @classmethod
    def get_indexes(cls, table_name: TableType) -> List[Index]:
        Indexes()
        return [index for index in cls.indexes if index.table_name == table_name]

    @staticmethod
    def get_index_type(index_meta_data) -> IndexType:
        is_unique: bool = index_meta_data[0]
        is_primary: bool = index_meta_data[1]
        is_clustered: bool = index_meta_data[2]

        if is_primary and is_clustered:
            return IndexType.PRIMARY
        elif is_clustered and not is_unique:
            return IndexType.CLUSTERED
        else:
            return IndexType.SECONDARY
