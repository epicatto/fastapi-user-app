from typing import List, Optional, Any

from serum import dependency, inject

from app.config.exceptions import ValidationException
from app.db.database import db_session
from app.repositories.user import UserRepository
from app.schemas.user import UserDTO, UserCreateDTO, UserDetailsDTO, UserUpdateDTO
from app.services.organization import OrganizationService
from app.services.role import RoleService


@inject
@dependency
class UserService:
    repository: UserRepository
    role_service: RoleService
    org_service: OrganizationService

    def get_all(self) -> List[UserDTO]:
        with db_session() as db:
            record_list = self.repository.get_all(db)
            return [UserDTO.from_model(i) for i in record_list]

    def get_by_id(self, id: int) -> Optional[UserDTO]:
        with db_session() as db:
            user = self.repository.get_by_id(db, id)
            if user:
                return UserDTO.from_model(user)

    def get_by_email(self, email: str) -> Optional[UserDTO]:
        with db_session() as db:
            user = self.repository.get_by_email(db, email)
            if user:
                return UserDTO.from_model(user)

    def get_details(self, id: int) -> Optional[UserDetailsDTO]:
        with db_session() as db:
            user = self.repository.get_by_id(db, id)
            if not user:
                raise ValidationException("User %s does not exist" % id)
            return UserDetailsDTO.from_model(user)

    def create(self, data: UserCreateDTO) -> Optional[UserDetailsDTO]:
        """
        Creates a new user if there is no other user with thew given email
        The given organization must exist
        :param data: data required to create a user
        :return: the new user
        """
        user = self.get_by_email(data.email)
        if user:
            raise ValidationException("Email is not available")

        org = self.org_service.get_by_id(data.organization_id)
        if not org:
            raise ValidationException("Organization %s does not exist" % data.organization_id)

        with db_session() as db:
            return UserDetailsDTO.from_model(self.repository.create(db, data))

    def update(self, id: int, data: UserUpdateDTO) -> Optional[UserDetailsDTO]:
        """
        Updates an existing user with the given data.
        It also checks if the given email is available to be used.
        The given organization must exist.
        :param id: ID of the user to be updated
        :param data: new user data
        :return: the updated user
        """
        user = self.get_by_id(id)
        if not user:
            raise ValidationException("User %s does not exist" % id)

        org = self.org_service.get_by_id(data.organization_id)
        if not org:
            raise ValidationException("Organization %s does not exist" % data.organization_id)

        with db_session() as db:
            return UserDetailsDTO.from_model(self.repository.update(db, id, data))

    def delete(self, id: int) -> Any:
        user = self.get_by_id(id)
        if not user:
            raise ValidationException("User %s does not exist" % id)

        with db_session() as db:
            return self.repository.delete(db, id)

    def add_roles(self, id: int, role_ids: List[int]) -> Optional[UserDetailsDTO]:
        """
        Adds the given roles to a user.
        The user to be updated and the given roles must exist
        :param id: ID of the user to be updated
        :param role_ids: List of role IDs to be added
        :return: The updated user
        """
        user = self.get_by_id(id)
        if not user:
            raise ValidationException("User %s does not exist" % id)

        roles = []
        for role_id in role_ids:
            role = self.role_service.get_by_id(role_id)
            if not role:
                raise ValidationException("Role %s does not exist" % role_id)

            roles.append(role.id)

        with db_session() as db:
            return UserDetailsDTO.from_model(self.repository.add_roles(db, id, roles))

    def remove_roles(self, id: int, role_ids: List[int]) -> Optional[UserDetailsDTO]:
        """
        Removes the given roles from a user.
        The user to be updated and the given roles must exist
        :param id: ID of the user to be updated
        :param role_ids: List of role IDs to be removed
        :return: The updated user
        """
        user = self.get_by_id(id)
        if not user:
            raise ValidationException("User %s does not exist" % id)

        roles = []
        for role_id in role_ids:
            role = self.role_service.get_by_id(role_id)
            if not role:
                raise ValidationException("Role %s does not exist" % role_id)

            roles.append(role.id)

        with db_session() as db:
            return UserDetailsDTO.from_model(self.repository.remove_roles(db, id, roles))
