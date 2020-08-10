from typing import Optional, List

from pydantic import BaseModel, EmailStr

from app.db.models import User
from app.schemas.role import RoleDTO


class UserDTO(BaseModel):
    id: int
    email: EmailStr = None
    is_active: Optional[bool] = True
    is_admin: bool = False
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    @classmethod
    def from_model(cls, instance: User):
        """
        Convert a DB User model instance to an UserDTO instance.
        """
        return cls(
            id=instance.id,
            email=instance.email,
            is_active=instance.is_active,
            is_admin=instance.is_admin,
            first_name=instance.first_name,
            last_name=instance.last_name,
        )


class UserDetailsDTO(UserDTO):
    from app.schemas.organization import OrganizationDTO
    organization: OrganizationDTO
    roles: Optional[List[RoleDTO]] = None

    @classmethod
    def from_model(cls, instance: User):
        """
        Convert a DB User model instance to an UserDTO instance.
        """
        from app.schemas.organization import OrganizationDTO
        return cls(
            id=instance.id,
            email=instance.email,
            is_active=instance.is_active,
            is_admin=instance.is_admin,
            first_name=instance.first_name,
            last_name=instance.last_name,
            organization=OrganizationDTO.from_model(instance.organization),
            roles=[RoleDTO.from_model(i) for i in instance.roles],
        )


class UserUpdateDTO(BaseModel):
    is_admin: Optional[bool] = False
    is_active: Optional[bool] = True
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    organization_id: int = None


class UserCreateDTO(UserUpdateDTO):
    email: EmailStr
