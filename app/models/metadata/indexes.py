from pydantic import BaseModel
from typing import List
from app.config import db
from app.models.table import TableType
from enum import Enum, auto


class IndexType(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

    PRIMARY = auto()
    CLUSTERED = auto()
    SECONDARY = auto()


class Index(BaseModel):
    table_name: TableType
    name: str
    column: str
    index_type: IndexType


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
    def get_indexes(cls, table_name: TableType):
        Indexes()
        return [
            [
                index.column,
                index.index_type,
            ]
            for index in cls.indexes
            if index.table_name == table_name
        ]

    @staticmethod
    def get_index_type(index_meta_data):
        is_primary: bool = index_meta_data[1]
        is_clustered: bool = index_meta_data[2]

        if is_primary and not is_clustered:
            return IndexType.PRIMARY
        elif is_clustered:
            return IndexType.CLUSTERED
        else:
            return IndexType.SECONDARY
