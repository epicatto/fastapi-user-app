from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from app.db.models import Role
from app.schemas.right import RightDTO


class RoleDTO(BaseModel):
    id: int
    name: str
    description: Optional[str] = ""
    created_date_time: Optional[datetime] = None
    modified_date_time: Optional[datetime] = None

    @classmethod
    def from_model(cls, instance: Role):
        """
        Convert a DB Role model instance to an RoleDTO instance.
        """
        return cls(
            id=instance.id,
            name=instance.name,
            description=instance.description,
            created_date_time=instance.created_date_time,
            modified_date_time=instance.modified_date_time,
        )


class RoleDetailsDTO(RoleDTO):
    rights: Optional[List[RightDTO]] = []

    @classmethod
    def from_model(cls, instance: Role):
        """
        Convert a DB Role model instance to an RoleDTO instance.
        """
        return cls(
            id=instance.id,
            name=instance.name,
            description=instance.description,
            created_date_time=instance.created_date_time,
            modified_date_time=instance.modified_date_time,
            rights=[RightDTO.from_model(i) for i in instance.rights],
        )


class RoleCreateDTO(BaseModel):
    name: str
    description: Optional[str] = None


class RoleUpdateDTO(RoleCreateDTO):
    pass
