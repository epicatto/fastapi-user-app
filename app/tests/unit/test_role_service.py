from unittest import mock
from unittest.mock import call

import pytest

from app.config.exceptions import ValidationException
from app.repositories.role import RoleRepository
from app.schemas.role import RoleCreateDTO, RoleUpdateDTO
from app.services.right import RightService
from app.services.role import RoleService
from app.tests.utils.utils import create_random_role, create_random_right


class TestRoleService:

    def setup(self):
        self.service = RoleService()

    def test_get_all(self, mocker):
        role1 = create_random_role()
        role2 = create_random_role()

        mocked_get_all = mocker.patch.object(RoleRepository, 'get_all', return_value=[role1, role2])

        result = self.service.get_all()

        assert mocked_get_all.called is True
        assert result
        assert len(result) == 2

    def test_get_by_id_exits(self, mocker):
        role1 = create_random_role()

        mocked_get_all = mocker.patch.object(RoleRepository, 'get_by_id', return_value=role1)

        result = self.service.get_by_id(role1.id)

        assert mocked_get_all.called is True
        assert result
        assert result.id == role1.id

    def test_get_by_id_does_not_exist(self, mocker):
        mocked_get_all = mocker.patch.object(RoleRepository, 'get_by_id', return_value=None)

        result = self.service.get_by_id(1)

        assert mocked_get_all.called is True
        assert not result

    def test_get_details_exits(self, mocker):
        role1 = create_random_role()

        mocked_get_all = mocker.patch.object(RoleRepository, 'get_by_id', return_value=role1)

        result = self.service.get_details(role1.id)

        assert mocked_get_all.called is True
        assert result
        assert result.id == role1.id

    def test_get_details_does_not_exist(self, mocker):
        mocked_get_all = mocker.patch.object(RoleRepository, 'get_by_id', return_value=None)

        with pytest.raises(ValidationException):
            self.service.get_details(1)

        assert mocked_get_all.called is True

    def test_create(self, mocker):
        role1 = create_random_role()

        mocked_get_all = mocker.patch.object(RoleService, 'get_by_name', return_value=None)
        mocked_create = mocker.patch.object(RoleRepository, 'create', return_value=role1)

        data = RoleCreateDTO(name="Name")

        result = self.service.create(data)

        assert mocked_get_all.called is True
        assert mocked_create.called is True
        assert result
        assert result.id == role1.id

    def test_create_name_already_exists(self, mocker):
        role1 = create_random_role()

        mocked_get_all = mocker.patch.object(RoleService, 'get_by_name', return_value=role1)
        mocked_create = mocker.patch.object(RoleRepository, 'create')

        data = RoleCreateDTO(name="Name")

        with pytest.raises(ValidationException):
            self.service.create(data)

        assert mocked_get_all.called is True
        assert mocked_create.called is False

    def test_update(self, mocker):
        role1 = create_random_role()

        mocked_get_all = mocker.patch.object(RoleService, 'get_by_id', return_value=role1)
        mocked_get_by_name = mocker.patch.object(RoleService, 'get_by_name', return_value=role1)
        mocked_update = mocker.patch.object(RoleRepository, 'update', return_value=role1)

        data = RoleUpdateDTO(name="Name")

        result = self.service.update(role1.id, data)

        assert mocked_get_all.called is True
        assert mocked_get_by_name.called is True
        assert mocked_update.called is True
        assert result
        assert result.id == role1.id

    def test_update_does_not_exist(self, mocker):
        role1 = create_random_role()

        mocked_get_all = mocker.patch.object(RoleService, 'get_by_id', return_value=None)
        mocked_update = mocker.patch.object(RoleRepository, 'update')

        data = RoleUpdateDTO(name="Name")

        with pytest.raises(ValidationException):
            self.service.update(role1.id, data)

        assert mocked_get_all.called is True
        assert mocked_update.called is False

    def test_update_name_already_exists(self, mocker):
        role1 = create_random_role()
        role2 = create_random_role()

        mocked_get_all = mocker.patch.object(RoleService, 'get_by_id', return_value=role1)
        mocked_get_by_name = mocker.patch.object(RoleService, 'get_by_name', return_value=role2)
        mocked_update = mocker.patch.object(RoleRepository, 'update')

        data = RoleUpdateDTO(name="Name")

        with pytest.raises(ValidationException):
            self.service.update(role1.id, data)

        assert mocked_get_all.called is True
        assert mocked_get_by_name.called is True
        assert mocked_update.called is False

    def test_delete(self, mocker):
        role1 = create_random_role()

        mocked_get_all = mocker.patch.object(RoleService, 'get_by_id', return_value=role1)
        mocked_delete = mocker.patch.object(RoleRepository, 'delete', return_value=role1)

        result = self.service.delete(role1.id)

        assert mocked_get_all.called is True
        assert mocked_delete.called is True
        assert result
        assert result.id == role1.id

    def test_delete_does_not_exist(self, mocker):
        role1 = create_random_role()

        mocked_get_all = mocker.patch.object(RoleService, 'get_by_id', return_value=None)
        mocked_delete = mocker.patch.object(RoleRepository, 'delete')

        with pytest.raises(ValidationException):
            self.service.delete(role1.id)

        assert mocked_get_all.called is True
        assert mocked_delete.called is False

    def test_add_rights(self, mocker):
        role1 = create_random_role()
        right1 = create_random_right()
        right2 = create_random_right()

        mocked_get_role = mocker.patch.object(RoleService, 'get_by_id', return_value=role1)
        mocked_get_rights = mocker.patch.object(RightService, 'get_by_id', side_effect=[right1, right2])
        mocked_add_rights = mocker.patch.object(RoleRepository, 'add_rights', return_value=role1)

        result = self.service.add_rights(role1.id, [right1.id, right2.id])

        assert mocked_get_role.called is True
        assert mocked_get_rights.called is True
        mocked_get_rights.assert_has_calls([
            call(right1.id),
            call(right2.id)
        ])
        mocked_add_rights.assert_called_with(mock.ANY, role1.id, [right1.id, right2.id])
        assert result

    def test_add_rights_role_does_not_exist(self, mocker):
        role1 = create_random_role()
        right1 = create_random_right()
        right2 = create_random_right()

        mocked_get_role = mocker.patch.object(RoleService, 'get_by_id', return_value=None)
        mocked_get_rights = mocker.patch.object(RightService, 'get_by_id', side_effect=[right1, right2])
        mocked_add_rights = mocker.patch.object(RoleRepository, 'add_rights', return_value=role1)

        with pytest.raises(ValidationException):
            self.service.add_rights(role1.id, [right1.id, right2.id])

        assert mocked_get_role.called is True
        assert mocked_get_rights.called is False
        assert mocked_add_rights.called is False

    def test_add_rights_right_does_not_exist(self, mocker):
        role1 = create_random_role()
        right1 = create_random_right()
        right2 = create_random_right()

        mocked_get_role = mocker.patch.object(RoleService, 'get_by_id', return_value=role1)
        mocked_get_rights = mocker.patch.object(RightService, 'get_by_id', side_effect=[right1, None])
        mocked_add_rights = mocker.patch.object(RoleRepository, 'add_rights', return_value=role1)

        with pytest.raises(ValidationException):
            self.service.add_rights(role1.id, [right1.id, right2.id])

        assert mocked_get_role.called is True
        assert mocked_get_rights.called is True
        assert mocked_add_rights.called is False

    def test_remove_rights(self, mocker):
        role1 = create_random_role()
        right1 = create_random_right()
        right2 = create_random_right()

        mocked_get_role = mocker.patch.object(RoleService, 'get_by_id', return_value=role1)
        mocked_get_rights = mocker.patch.object(RightService, 'get_by_id', side_effect=[right1, right2])
        mocked_remove_rights = mocker.patch.object(RoleRepository, 'remove_rights', return_value=role1)

        result = self.service.remove_rights(role1.id, [right1.id, right2.id])

        assert mocked_get_role.called is True
        assert mocked_get_rights.called is True
        mocked_get_rights.assert_has_calls([
            call(right1.id),
            call(right2.id)
        ])
        mocked_remove_rights.assert_called_with(mock.ANY, role1.id, [right1.id, right2.id])
        assert result

    def test_remove_rights_role_does_not_exist(self, mocker):
        role1 = create_random_role()
        right1 = create_random_right()
        right2 = create_random_right()

        mocked_get_role = mocker.patch.object(RoleService, 'get_by_id', return_value=None)
        mocked_get_rights = mocker.patch.object(RightService, 'get_by_id', side_effect=[right1, right2])
        mocked_remove_rights = mocker.patch.object(RoleRepository, 'remove_rights', return_value=role1)

        with pytest.raises(ValidationException):
            self.service.remove_rights(role1.id, [right1.id, right2.id])

        assert mocked_get_role.called is True
        assert mocked_get_rights.called is False
        assert mocked_remove_rights.called is False

    def test_remove_rights_right_does_not_exist(self, mocker):
        role1 = create_random_role()
        right1 = create_random_right()
        right2 = create_random_right()

        mocked_get_role = mocker.patch.object(RoleService, 'get_by_id', return_value=role1)
        mocked_get_rights = mocker.patch.object(RightService, 'get_by_id', side_effect=[right1, None])
        mocked_remove_rights = mocker.patch.object(RoleRepository, 'remove_rights', return_value=role1)

        with pytest.raises(ValidationException):
            self.service.remove_rights(role1.id, [right1.id, right2.id])

        assert mocked_get_role.called is True
        assert mocked_get_rights.called is True
        assert mocked_remove_rights.called is False
