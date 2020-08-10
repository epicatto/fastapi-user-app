import pytest

from app.config.exceptions import ValidationException
from app.repositories.right import RightRepository
from app.schemas.right import RightCreateDTO, RightUpdateDTO
from app.services.right import RightService
from app.tests.utils.utils import create_random_right


class TestRightService:

    def setup(self):
        self.service = RightService()

    def test_get_all(self, mocker):
        right1 = create_random_right()
        right2 = create_random_right()

        mocked_get_all = mocker.patch.object(RightRepository, 'get_all', return_value=[right1, right2])

        result = self.service.get_all()

        assert mocked_get_all.called is True
        assert result
        assert len(result) == 2

    def test_get_by_id_exits(self, mocker):
        right1 = create_random_right()

        mocked_get_all = mocker.patch.object(RightRepository, 'get_by_id', return_value=right1)

        result = self.service.get_by_id(right1.id)

        assert mocked_get_all.called is True
        assert result
        assert result.id == right1.id

    def test_get_by_id_does_not_exist(self, mocker):
        mocked_get_all = mocker.patch.object(RightRepository, 'get_by_id', return_value=None)

        result = self.service.get_by_id(1)

        assert mocked_get_all.called is True
        assert not result

    def test_get_details_exits(self, mocker):
        right1 = create_random_right()

        mocked_get_all = mocker.patch.object(RightRepository, 'get_by_id', return_value=right1)

        result = self.service.get_details(right1.id)

        assert mocked_get_all.called is True
        assert result
        assert result.id == right1.id

    def test_get_details_does_not_exist(self, mocker):
        mocked_get_all = mocker.patch.object(RightRepository, 'get_by_id', return_value=None)

        with pytest.raises(ValidationException):
            self.service.get_details(1)

        assert mocked_get_all.called is True

    def test_create(self, mocker):
        right1 = create_random_right()

        mocked_get_all = mocker.patch.object(RightService, 'get_by_name', return_value=None)
        mocked_create = mocker.patch.object(RightRepository, 'create', return_value=right1)

        data = RightCreateDTO(name="Name")

        result = self.service.create(data)

        assert mocked_get_all.called is True
        assert mocked_create.called is True
        assert result
        assert result.id == right1.id

    def test_create_name_already_exists(self, mocker):
        right1 = create_random_right()

        mocked_get_all = mocker.patch.object(RightService, 'get_by_name', return_value=right1)
        mocked_create = mocker.patch.object(RightRepository, 'create')

        data = RightCreateDTO(name="Name")

        with pytest.raises(ValidationException):
            self.service.create(data)

        assert mocked_get_all.called is True
        assert mocked_create.called is False

    def test_update(self, mocker):
        right1 = create_random_right()

        mocked_get_by_id = mocker.patch.object(RightService, 'get_by_id', return_value=right1)
        mocked_get_by_name = mocker.patch.object(RightService, 'get_by_name', return_value=right1)
        mocked_update = mocker.patch.object(RightRepository, 'update', return_value=right1)

        data = RightUpdateDTO(name="Name")

        result = self.service.update(right1.id, data)

        assert mocked_get_by_id.called is True
        assert mocked_get_by_name.called is True
        assert mocked_update.called is True
        assert result
        assert result.id == right1.id

    def test_update_does_not_exist(self, mocker):
        right1 = create_random_right()

        mocked_get_all = mocker.patch.object(RightService, 'get_by_id', return_value=None)
        mocked_update = mocker.patch.object(RightRepository, 'update')

        data = RightCreateDTO(name="Name")

        with pytest.raises(ValidationException):
            self.service.update(right1.id, data)

        assert mocked_get_all.called is True
        assert mocked_update.called is False

    def test_update_name_already_exists(self, mocker):
        right1 = create_random_right()
        right2 = create_random_right()

        mocked_get_all = mocker.patch.object(RightService, 'get_by_id', return_value=right1)
        mocked_get_by_name = mocker.patch.object(RightService, 'get_by_name', return_value=right2)
        mocked_update = mocker.patch.object(RightRepository, 'update')

        data = RightCreateDTO(name="Name")

        with pytest.raises(ValidationException):
            self.service.update(right1.id, data)

        assert mocked_get_all.called is True
        assert mocked_get_by_name.called is True
        assert mocked_update.called is False

    def test_delete(self, mocker):
        right1 = create_random_right()

        mocked_get_all = mocker.patch.object(RightService, 'get_by_id', return_value=right1)
        mocked_delete = mocker.patch.object(RightRepository, 'delete', return_value=right1)

        result = self.service.delete(right1.id)

        assert mocked_get_all.called is True
        assert mocked_delete.called is True
        assert result
        assert result.id == right1.id

    def test_delete_does_not_exist(self, mocker):
        right1 = create_random_right()

        mocked_get_all = mocker.patch.object(RightService, 'get_by_id', return_value=None)
        mocked_delete = mocker.patch.object(RightRepository, 'delete')

        with pytest.raises(ValidationException):
            self.service.delete(right1.id)

        assert mocked_get_all.called is True
        assert mocked_delete.called is False
