from typing import List, Optional

from pydantic import BaseModel

from app.db.models import Organization


class OrganizationDTO(BaseModel):
    id: int
    name: str

    @classmethod
    def from_model(cls, instance: Organization):
        """
        Convert a DB Organization model instance to an OrganizationDTO instance.
        """
        return cls(
            id=instance.id,
            name=instance.name,
        )


class OrganizationDetailsDTO(OrganizationDTO):
    from app.schemas.user import UserDTO
    users: Optional[List[UserDTO]] = []

    @classmethod
    def from_model(cls, instance: Organization):
        from app.schemas.user import UserDTO
        """
        Convert a DB Organization model instance to an OrganizationDetailsDTO instance.
        """
        return cls(
            id=instance.id,
            name=instance.name,
            users=[UserDTO.from_model(i) for i in instance.users],
        )


class OrganizationCreateDTO(BaseModel):
    name: str


class OrganizationUpdateDTO(OrganizationCreateDTO):
    pass
