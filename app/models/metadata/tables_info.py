from pydantic import BaseModel
from typing import List
from config import db
from models.enums.tableType import TableType


class TablesDetails(BaseModel):
    tables_details: List[str] = []

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super(TablesDetails, cls).__new__(cls)
            cls.tables_details: List[str] = []
            cls.set_content()
        return cls.tables_details

    @classmethod
    def set_content(cls):
        connection = db.get_connection()
        cursor = connection.cursor()

        select_query = "SELECT * FROM tables_details;"

        cursor.execute(select_query)

        rows = cursor.fetchall()
        cls.tables_details = [row for row in rows]

        cursor.close()
        connection.close()

    @classmethod
    def get_no_of_blocks(cls, table_name: TableType) -> int or None:
        details = cls()

        for row in details:
            if row[0] == table_name.value:
                return row[1]
        return None

    @classmethod
    def get_no_of_records(cls, table_name: TableType) -> int or None:
        details = cls()

        for row in details:
            if row[0] == table_name.value:
                return row[2]
        return None
