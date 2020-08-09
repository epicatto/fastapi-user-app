from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.db.models import Right


class RightDTO(BaseModel):
    id: int
    name: str
    description: Optional[str] = ""
    created_date_time: Optional[datetime] = None
    modified_date_time: Optional[datetime] = None

    @classmethod
    def from_model(cls, instance: Right):
        """
        Convert a DB Right model instance to an RightDTO instance.
        """
        return cls(
            id=instance.id,
            name=instance.name,
            description=instance.description,
            created_date_time=instance.created_date_time,
            modified_date_time=instance.modified_date_time,
        )


class RightCreateDTO(BaseModel):
    name: str
    description: Optional[str] = None


class RightUpdateDTO(RightCreateDTO):
    pass
