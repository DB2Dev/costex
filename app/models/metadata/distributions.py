from pydantic import BaseModel
from typing import List
from app.config import db


class Distributions(BaseModel):
    tables_details: List[str] = []

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Distributions, cls).__new__(cls)
            cls.tables_details: List[str] = []
            cls.set_content()
        return cls.tables_details

    @classmethod
    def set_content(cls):
        connection = db.get_connection()
        cursor = connection.cursor()

        select_query = "SELECT * FROM distributions;"

        cursor.execute(select_query)

        rows = cursor.fetchall()
        cls.tables_details = [row for row in rows]

        cursor.close()
        connection.close()
