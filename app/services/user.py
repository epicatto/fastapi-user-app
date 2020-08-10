from typing import List, Optional, Any

from serum import dependency, inject

from app.config.exceptions import ValidationException
from app.db.database import db_session
from app.repositories.organization import OrganizationRepository
from app.repositories.role import RoleRepository
from app.repositories.user import UserRepository
from app.schemas.user import UserDTO, UserCreateDTO, UserDetailsDTO, UserUpdateDTO


@inject
@dependency
class UserService:
    repository: UserRepository
    role_repository: RoleRepository
    org_repository: OrganizationRepository

    def get_all(self) -> List[UserDTO]:
        with db_session() as db:
            record_list = self.repository.get_all(db)
            return [UserDTO.from_model(i) for i in record_list]

    def get_by_id(self, id: int) -> Optional[UserDetailsDTO]:
        with db_session() as db:
            user = self.repository.get_by_id(db, id)
            if user:
                return UserDetailsDTO.from_model(user)

    def get_details(self, id: int) -> Optional[UserDetailsDTO]:
        with db_session() as db:
            user = self.repository.get_by_id(db, id)
            if not user:
                raise ValidationException("User %s does not exist" % id)
            return UserDetailsDTO.from_model(user)

    def create(self, data: UserCreateDTO) -> Optional[UserDetailsDTO]:
        with db_session() as db:
            user = self.repository.get_by_email(db, data.email)
            if user:
                raise ValidationException("Email is not available")

            org = self.org_repository.get_by_id(db, data.organization_id)
            if not org:
                raise ValidationException("Organization %s does not exist" % data.organization_id)

            return UserDetailsDTO.from_model(self.repository.create(db, data))

    def update(self, id: int, data: UserUpdateDTO) -> Optional[UserDetailsDTO]:
        with db_session() as db:
            user = self.repository.get_by_id(db, id)
            if not user:
                raise ValidationException("User %s does not exist" % id)

            org = self.org_repository.get_by_id(db, data.organization_id)
            if not org:
                raise ValidationException("Organization %s does not exist" % data.organization_id)

            return UserDetailsDTO.from_model(self.repository.update(db, user, data))

    def delete(self, id: int) -> Any:
        with db_session() as db:
            user = self.repository.get_by_id(db, id)
            if not user:
                raise ValidationException("User %s does not exist" % id)

            return self.repository.delete(db, user)

    def add_roles(self, id: int, role_ids: List[int]) -> Optional[UserDetailsDTO]:
        with db_session() as db:
            user = self.repository.get_by_id(db, id)
            if not user:
                raise ValidationException("User %s does not exist" % id)

            roles = []
            for role_id in role_ids:
                role = self.role_repository.get_by_id(db, role_id)
                if not role:
                    raise ValidationException("Role %s does not exist" % role_id)

                roles.append(role)

            return UserDetailsDTO.from_model(self.repository.add_roles(db, user, roles))

    def remove_roles(self, id: int, role_ids: List[int]) -> Optional[UserDetailsDTO]:
        with db_session() as db:
            user = self.repository.get_by_id(db, id)
            if not user:
                raise ValidationException("User %s does not exist" % id)

            roles = []
            for role_id in role_ids:
                role = self.role_repository.get_by_id(db, role_id)
                if not role:
                    raise ValidationException("Role %s does not exist" % role_id)

                roles.append(role)

            return UserDetailsDTO.from_model(self.repository.remove_roles(db, user, roles))
