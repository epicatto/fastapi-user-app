from typing import List, Optional, Any

from serum import inject, dependency

from app.config.exceptions import ValidationException
from app.db.database import db_session
from app.repositories.right import RightRepository
from app.repositories.role import RoleRepository
from app.schemas.role import RoleDTO, RoleDetailsDTO, RoleCreateDTO, RoleUpdateDTO


@inject
@dependency
class RoleService:
    repository: RoleRepository
    right_repository: RightRepository

    def get_all(self) -> List[RoleDTO]:
        with db_session() as db:
            roles = self.repository.get_all(db)
            return [RoleDTO.from_model(i) for i in roles]

    def get_by_id(self, id: int) -> Optional[RoleDetailsDTO]:
        with db_session() as db:
            role = self.repository.get_by_id(db, id)
            if role:
                return RoleDetailsDTO.from_model(role)

    def get_details(self, id: int) -> Optional[RoleDetailsDTO]:
        with db_session() as db:
            role = self.repository.get_by_id(db, id)
            if not role:
                raise ValidationException("Role %s does not exist" % id)
            return RoleDetailsDTO.from_model(role)

    def create(self, data: RoleCreateDTO) -> Optional[RoleDetailsDTO]:
        with db_session() as db:
            role = self.repository.get_by_name(db, data.name)
            if role:
                raise ValidationException("Role already exists with the name")
            return RoleDetailsDTO.from_model(self.repository.create(db, data))

    def update(self, id: int, data: RoleUpdateDTO) -> Optional[RoleDetailsDTO]:
        with db_session() as db:
            role = self.repository.get_by_id(db, id)
            if not role:
                raise ValidationException("Role %s does not exist" % id)

            role_with_name = self.repository.get_by_name(db, data.name)
            if role_with_name and role_with_name.id != id:
                raise ValidationException("Role already exists with the name")

            return RoleDetailsDTO.from_model(self.repository.update(db, role, data))

    def delete(self, id: int) -> Any:
        with db_session() as db:
            role = self.repository.get_by_id(db, id)
            if not role:
                raise ValidationException("Role %s does not exist" % id)

            return self.repository.delete(db, role)

    def add_rights(self, id: int, right_ids: List[int]) -> Optional[RoleDetailsDTO]:
        with db_session() as db:
            role = self.repository.get_by_id(db, id)
            if not role:
                raise ValidationException("Role %s does not exist" % id)

            rights = []
            for right_id in right_ids:
                right = self.right_repository.get_by_id(db, right_id)
                if not right:
                    raise ValidationException("Right %s does not exist" % right_id)

                rights.append(right)

            return RoleDetailsDTO.from_model(self.repository.add_rights(db, role, rights))

    def remove_rights(self, id: int, right_ids: List[int]) -> Optional[RoleDetailsDTO]:
        with db_session() as db:
            role = self.repository.get_by_id(db, id)
            if not role:
                raise ValidationException("Role %s does not exist" % id)

            rights = []
            for right_id in right_ids:
                right = self.right_repository.get_by_id(db, right_id)
                if not right:
                    raise ValidationException("Right %s does not exist" % right_id)

                rights.append(right)

            return RoleDetailsDTO.from_model(self.repository.remove_rights(db, role, rights))
