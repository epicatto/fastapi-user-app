from unittest import mock
from unittest.mock import call

import pytest

from app.config.exceptions import ValidationException
from app.repositories.organization import OrganizationRepository
from app.repositories.role import RoleRepository
from app.repositories.user import UserRepository
from app.schemas.user import UserCreateDTO, UserUpdateDTO
from app.services.user import UserService
from app.tests.utils.utils import create_random_user, create_random_organization, create_random_role


class TestUserService:

    def setup(self):
        self.service = UserService()

    def test_get_all(self, mocker):
        org = create_random_organization()
        user1 = create_random_user(organization=org)
        user2 = create_random_user(organization=org)

        mocked_get_all = mocker.patch.object(UserRepository, 'get_all', return_value=[user1, user2])

        result = self.service.get_all()

        assert mocked_get_all.called is True
        assert result
        assert len(result) == 2

    def test_get_by_id_exits(self, mocker):
        org = create_random_organization()
        user1 = create_random_user(organization=org)

        mocked_get_all = mocker.patch.object(UserRepository, 'get_by_id', return_value=user1)

        result = self.service.get_by_id(user1.id)

        assert mocked_get_all.called is True
        assert result
        assert result.id == user1.id

    def test_get_by_id_does_not_exist(self, mocker):
        mocked_get_all = mocker.patch.object(UserRepository, 'get_by_id', return_value=None)

        result = self.service.get_by_id(1)

        assert mocked_get_all.called is True
        assert not result

    def test_get_details_exits(self, mocker):
        org = create_random_organization()
        user1 = create_random_user(organization=org)

        mocked_get_all = mocker.patch.object(UserRepository, 'get_by_id', return_value=user1)

        result = self.service.get_details(user1.id)

        assert mocked_get_all.called is True
        assert result
        assert result.id == user1.id

    def test_get_details_does_not_exist(self, mocker):
        mocked_get_all = mocker.patch.object(UserRepository, 'get_by_id', return_value=None)

        with pytest.raises(ValidationException):
            self.service.get_details(1)

        assert mocked_get_all.called is True

    def test_create(self, mocker):
        org = create_random_organization()
        user1 = create_random_user(organization=org)

        mocked_get_all = mocker.patch.object(UserRepository, 'get_by_email', return_value=None)
        mocked_create = mocker.patch.object(UserRepository, 'create', return_value=user1)
        mocked_org = mocker.patch.object(OrganizationRepository, 'get_by_id', return_value=org)

        data = UserCreateDTO(email="test@test.com")

        result = self.service.create(data)

        assert mocked_get_all.called is True
        assert mocked_create.called is True
        assert mocked_org.called is True
        assert result
        assert result.id == user1.id

    def test_create_email_already_exists(self, mocker):
        org = create_random_organization()
        user1 = create_random_user(organization=org)

        mocked_get_all = mocker.patch.object(UserRepository, 'get_by_email', return_value=user1)
        mocked_create = mocker.patch.object(UserRepository, 'create')

        data = UserCreateDTO(email="test@test.com")

        with pytest.raises(ValidationException):
            self.service.create(data)

        assert mocked_get_all.called is True
        assert mocked_create.called is False

    def test_create_org_does_not_exists(self, mocker):
        mocked_get_all = mocker.patch.object(UserRepository, 'get_by_email', return_value=None)
        mocked_org = mocker.patch.object(OrganizationRepository, 'get_by_id', return_value=None)
        mocked_create = mocker.patch.object(UserRepository, 'create')

        data = UserCreateDTO(email="test@test.com")

        with pytest.raises(ValidationException):
            self.service.create(data)

        assert mocked_get_all.called is True
        assert mocked_org.called is True
        assert mocked_create.called is False

    def test_update(self, mocker):
        org = create_random_organization()
        user1 = create_random_user(organization=org)

        mocked_get_all = mocker.patch.object(UserRepository, 'get_by_id', return_value=user1)
        mocked_org = mocker.patch.object(OrganizationRepository, 'get_by_id', return_value=org)
        mocked_update = mocker.patch.object(UserRepository, 'update', return_value=user1)

        data = UserUpdateDTO(first_name="Name")

        result = self.service.update(user1.id, data)

        assert mocked_get_all.called is True
        assert mocked_update.called is True
        assert mocked_org.called is True
        assert result
        assert result.id == user1.id

    def test_update_does_not_exist(self, mocker):
        org = create_random_organization()
        user1 = create_random_user(organization=org)

        mocked_get_all = mocker.patch.object(UserRepository, 'get_by_id', return_value=None)
        mocked_update = mocker.patch.object(UserRepository, 'update')

        data = UserUpdateDTO(first_name="Name")

        with pytest.raises(ValidationException):
            self.service.update(user1.id, data)

        assert mocked_get_all.called is True
        assert mocked_update.called is False

    def test_update_org_does_not_exists(self, mocker):
        org = create_random_organization()
        user1 = create_random_user(organization=org)

        mocked_get_all = mocker.patch.object(UserRepository, 'get_by_id', return_value=user1)
        mocked_org = mocker.patch.object(OrganizationRepository, 'get_by_id', return_value=None)
        mocked_create = mocker.patch.object(UserRepository, 'update')

        data = UserUpdateDTO(email="test@test.com")

        with pytest.raises(ValidationException):
            self.service.update(user1.id, data)

        assert mocked_get_all.called is True
        assert mocked_org.called is True
        assert mocked_create.called is False

    def test_delete(self, mocker):
        org = create_random_organization()
        user1 = create_random_user(organization=org)

        mocked_get_all = mocker.patch.object(UserRepository, 'get_by_id', return_value=user1)
        mocked_delete = mocker.patch.object(UserRepository, 'delete', return_value=user1)

        result = self.service.delete(user1.id)

        assert mocked_get_all.called is True
        assert mocked_delete.called is True
        assert result
        assert result.id == user1.id

    def test_delete_does_not_exist(self, mocker):
        org = create_random_organization()
        user1 = create_random_user(organization=org)

        mocked_get_all = mocker.patch.object(UserRepository, 'get_by_id', return_value=None)
        mocked_delete = mocker.patch.object(UserRepository, 'delete')

        with pytest.raises(ValidationException):
            self.service.delete(user1.id)

        assert mocked_get_all.called is True
        assert mocked_delete.called is False

    def test_add_roles(self, mocker):
        org = create_random_organization()
        user1 = create_random_user(organization=org)
        role1 = create_random_role()
        role2 = create_random_role()

        mocked_get_role = mocker.patch.object(UserRepository, 'get_by_id', return_value=user1)
        mocked_get_rights = mocker.patch.object(RoleRepository, 'get_by_id', side_effect=[role1, role2])
        mocked_add_roles = mocker.patch.object(UserRepository, 'add_roles', return_value=user1)

        result = self.service.add_roles(user1.id, [role1.id, role2.id])

        assert mocked_get_role.called is True
        assert mocked_get_rights.called is True
        mocked_get_rights.assert_has_calls([
            call(mock.ANY, role1.id),
            call(mock.ANY, role2.id)
        ])
        mocked_add_roles.assert_called_with(mock.ANY, user1, [role1, role2])
        assert result

    def test_add_roles_user_does_not_exist(self, mocker):
        org = create_random_organization()
        user1 = create_random_user(organization=org)
        role1 = create_random_role()
        role2 = create_random_role()

        mocked_get_role = mocker.patch.object(UserRepository, 'get_by_id', return_value=None)
        mocked_get_rights = mocker.patch.object(RoleRepository, 'get_by_id', side_effect=[role1, role2])
        mocked_add_roles = mocker.patch.object(UserRepository, 'add_roles', return_value=user1)

        with pytest.raises(ValidationException):
            self.service.add_roles(user1.id, [role1.id, role2.id])

        assert mocked_get_role.called is True
        assert mocked_get_rights.called is False
        assert mocked_add_roles.called is False

    def test_add_roles_role_does_not_exist(self, mocker):
        org = create_random_organization()
        user1 = create_random_user(organization=org)
        role1 = create_random_role()
        role2 = create_random_role()

        mocked_get_role = mocker.patch.object(UserRepository, 'get_by_id', return_value=user1)
        mocked_get_rights = mocker.patch.object(RoleRepository, 'get_by_id', side_effect=[role1, None])
        mocked_add_roles = mocker.patch.object(UserRepository, 'add_roles', return_value=user1)

        with pytest.raises(ValidationException):
            self.service.add_roles(user1.id, [role1.id, role2.id])

        assert mocked_get_role.called is True
        assert mocked_get_rights.called is True
        assert mocked_add_roles.called is False

    def test_remove_roles(self, mocker):
        org = create_random_organization()
        user1 = create_random_user(organization=org)
        role1 = create_random_role()
        role2 = create_random_role()

        mocked_get_role = mocker.patch.object(UserRepository, 'get_by_id', return_value=user1)
        mocked_get_rights = mocker.patch.object(RoleRepository, 'get_by_id', side_effect=[role1, role2])
        mocked_remove_roles = mocker.patch.object(UserRepository, 'remove_roles', return_value=user1)

        result = self.service.remove_roles(user1.id, [role1.id, role2.id])

        assert mocked_get_role.called is True
        assert mocked_get_rights.called is True
        mocked_get_rights.assert_has_calls([
            call(mock.ANY, role1.id),
            call(mock.ANY, role2.id)
        ])
        mocked_remove_roles.assert_called_with(mock.ANY, user1, [role1, role2])
        assert result

    def test_remove_roles_role_does_not_exist(self, mocker):
        org = create_random_organization()
        user1 = create_random_user(organization=org)
        role1 = create_random_role()
        role2 = create_random_role()

        mocked_get_role = mocker.patch.object(UserRepository, 'get_by_id', return_value=None)
        mocked_get_rights = mocker.patch.object(RoleRepository, 'get_by_id', side_effect=[role1, role2])
        mocked_remove_roles = mocker.patch.object(UserRepository, 'remove_roles', return_value=role1)

        with pytest.raises(ValidationException):
            self.service.remove_roles(user1.id, [role1.id, role2.id])

        assert mocked_get_role.called is True
        assert mocked_get_rights.called is False
        assert mocked_remove_roles.called is False

    def test_remove_roles_right_does_not_exist(self, mocker):
        org = create_random_organization()
        user1 = create_random_user(organization=org)
        role1 = create_random_role()
        role2 = create_random_role()

        mocked_get_role = mocker.patch.object(UserRepository, 'get_by_id', return_value=user1)
        mocked_get_rights = mocker.patch.object(RoleRepository, 'get_by_id', side_effect=[role1, None])
        mocked_remove_roles = mocker.patch.object(UserRepository, 'remove_roles', return_value=role1)

        with pytest.raises(ValidationException):
            self.service.remove_roles(user1.id, [role1.id, role2.id])

        assert mocked_get_role.called is True
        assert mocked_get_rights.called is True
        assert mocked_remove_roles.called is False
