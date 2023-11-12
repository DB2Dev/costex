from pydantic import BaseModel
from typing import List
from config import db
from models.enums.tableType import TableType


class Constraint(BaseModel):
    table_name: TableType
    attribute_name: str
    name: str = "is_unique"
    condition: bool


class Constraints(BaseModel):
    constraints: List[Constraint] = []

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Constraints, cls).__new__(cls)
            cls.constraints: List[Constraint] = []
            cls.set_constraints()
        return cls.constraints

    @classmethod
    def set_constraints(cls):
        connection = db.get_connection()
        cursor = connection.cursor()

        select_query = "SELECT * FROM attributes_details;"

        cursor.execute(select_query)

        rows = cursor.fetchall()
        cls.constraints = [
            Constraint(
                table_name=TableType.EMPLOYEE
                if row[0].upper() == "EMPLOYEE"
                else TableType.PROJECT,
                attribute_name=row[1],
                condition=row[2],
            )
            for row in rows
        ]

        cursor.close()
        connection.close()

    @classmethod
    def get_columns(cls, table_name: TableType) -> List[Constraint]:
        Constraints()
        return [
            constraint
            for constraint in cls.constraints
            if constraint.table_name == table_name
        ]
