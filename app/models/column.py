from pydantic import BaseModel, model_validator
from typing import Optional
from app.models.enums.indexType import IndexType


class Column(BaseModel):
    name: str
    is_unique: bool = False
    is_primary_key: bool = False
    has_index: bool = False
    index_type: Optional[IndexType] = IndexType.NONE

    @model_validator(mode="before")
    def has_index_validator(cls, values):
        has_index = values.get("has_index", False)
        index_type = values.get("index_type", IndexType.NONE)
        if has_index and index_type == IndexType.NONE:
            raise ValueError("Index type must be specified if has_index is True")
        elif not has_index and index_type is not IndexType.NONE:
            raise ValueError("Index type must be None if has_index is False")
        return values
