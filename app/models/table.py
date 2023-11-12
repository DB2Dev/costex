from pydantic import BaseModel, Field, model_validator
from typing import Optional, List
from .enums.tableType import TableType
from .column import Column
from models.metadata.indexes import IndexType, Index, Indexes
from models.metadata.attrs_constraints import Constraints


class Table(BaseModel):
    name: TableType
    columns: List[Column] = Field(default_factory=list)
    primary_key: Optional[Column]
    indexes: Optional[List[Index]] = Field(default_factory=list)

    @model_validator(mode="before")
    def gen_table(cls, data, name):
        cons = Constraints.get_columns(data.get("name"))
        indices = Indexes.get_indexes(data.get("name"))
        data["columns"] = [
            Column(
                name=column.attribute_name,
                is_unique=any(
                    constraint.condition
                    if constraint.name == "is_unique"
                    or constraint.name == "is_primary_key"
                    else False
                    for constraint in cons
                    if constraint.attribute_name == column.attribute_name
                ),
                is_primary_key=any(
                    constraint.condition
                    if constraint.name == "is_unique"
                    or constraint.name == "is_primary_key"
                    else False
                    for constraint in cons
                    if constraint.attribute_name == column.attribute_name
                ),
                has_index=any(column.attribute_name == ind.column for ind in indices),
                index_type=IndexType(
                    next(
                        (
                            ind.index_type
                            for ind in indices
                            if ind.column == column.attribute_name
                        ),
                        IndexType.NONE,
                    )
                ),
            )
            for column in cons
        ]
        data["primary_key"] = next(
            (column for column in data["columns"] if column.is_primary_key), None
        )
        data["indexes"] = indices

        return data
