from typing import List, Optional, Any

from serum import inject, dependency

from app.config.exceptions import ValidationException
from app.db.database import db_session
from app.repositories.role import RoleRepository
from app.schemas.role import RoleDTO, RoleDetailsDTO, RoleCreateDTO, RoleUpdateDTO
from app.services.right import RightService


@inject
@dependency
class RoleService:
    repository: RoleRepository
    right_service: RightService

    def get_all(self) -> List[RoleDTO]:
        with db_session() as db:
            roles = self.repository.get_all(db)
            return [RoleDTO.from_model(i) for i in roles]

    def get_by_id(self, id: int) -> Optional[RoleDTO]:
        with db_session() as db:
            role = self.repository.get_by_id(db, id)
            if role:
                return RoleDTO.from_model(role)

    def get_by_name(self, name: str) -> Optional[RoleDetailsDTO]:
        with db_session() as db:
            role = self.repository.get_by_name(db, name)
            if role:
                return RoleDetailsDTO.from_model(role)

    def get_details(self, id: int) -> Optional[RoleDetailsDTO]:
        with db_session() as db:
            role = self.repository.get_by_id(db, id)
            if not role:
                raise ValidationException("Role %s does not exist" % id)
            return RoleDetailsDTO.from_model(role)

    def create(self, data: RoleCreateDTO) -> Optional[RoleDetailsDTO]:
        role = self.get_by_name(data.name)
        if role:
            raise ValidationException("Role already exists with the name")

        with db_session() as db:
            return RoleDetailsDTO.from_model(self.repository.create(db, data))

    def update(self, id: int, data: RoleUpdateDTO) -> Optional[RoleDetailsDTO]:
        role = self.get_by_id(id)
        if not role:
            raise ValidationException("Role %s does not exist" % id)

        role_with_name = self.get_by_name(data.name)
        if role_with_name and role_with_name.id != id:
            raise ValidationException("Role already exists with the name")

        with db_session() as db:
            return RoleDetailsDTO.from_model(self.repository.update(db, id, data))

    def delete(self, id: int) -> Any:
        role = self.get_by_id(id)
        if not role:
            raise ValidationException("Role %s does not exist" % id)

        with db_session() as db:
            return self.repository.delete(db, id)

    def add_rights(self, id: int, right_ids: List[int]) -> Optional[RoleDetailsDTO]:
        role = self.get_by_id(id)
        if not role:
            raise ValidationException("Role %s does not exist" % id)

        rights = []
        for right_id in right_ids:
            right = self.right_service.get_by_id(right_id)
            if not right:
                raise ValidationException("Right %s does not exist" % right_id)
            rights.append(right.id)

        with db_session() as db:
            return RoleDetailsDTO.from_model(self.repository.add_rights(db, id, rights))

    def remove_rights(self, id: int, right_ids: List[int]) -> Optional[RoleDetailsDTO]:
        role = self.get_by_id(id)
        if not role:
            raise ValidationException("Role %s does not exist" % id)

        rights = []
        for right_id in right_ids:
            right = self.right_service.get_by_id(right_id)
            if not right:
                raise ValidationException("Right %s does not exist" % right_id)
            rights.append(right.id)

        with db_session() as db:
            return RoleDetailsDTO.from_model(self.repository.remove_rights(db, id, rights))
