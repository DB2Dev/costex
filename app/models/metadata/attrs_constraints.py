from pydantic import BaseModel
from typing import List
from app.config import db
from app.models.table import TableType


class Constraint(BaseModel):
    table_name: TableType
    attribute_name: str
    constraint_name: str = "is_unique"
    constraint_condition: bool


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
                constraint_condition=row[2],
            )
            for row in rows
        ]

        cursor.close()
        connection.close()

    @classmethod
    def get_columns(cls, table_name: TableType):
        Constraints()
        return [
            [
                constraint.attribute_name,
                constraint.constraint_name,
                constraint.constraint_condition,
            ]
            for constraint in cls.constraints
            if constraint.table_name == table_name
        ]
