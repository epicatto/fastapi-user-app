import pytest

from app.config.exceptions import ValidationException
from app.repositories.organization import OrganizationRepository
from app.schemas.organization import OrganizationCreateDTO, OrganizationUpdateDTO
from app.services.organization import OrganizationService
from app.tests.utils.utils import create_random_organization


class TestOrganizationService:

    def setup(self):
        self.service = OrganizationService()

    def test_get_all(self, mocker):
        org1 = create_random_organization()
        org2 = create_random_organization()

        mocked_get_all = mocker.patch.object(OrganizationRepository, 'get_all', return_value=[org1, org2])

        result = self.service.get_all()

        assert mocked_get_all.called is True
        assert result
        assert len(result) == 2

    def test_get_by_id_exits(self, mocker):
        org1 = create_random_organization()

        mocked_get_all = mocker.patch.object(OrganizationRepository, 'get_by_id', return_value=org1)

        result = self.service.get_by_id(org1.id)

        assert mocked_get_all.called is True
        assert result
        assert result.id == org1.id

    def test_get_by_id_does_not_exist(self, mocker):
        mocked_get_all = mocker.patch.object(OrganizationRepository, 'get_by_id', return_value=None)

        result = self.service.get_by_id(1)

        assert mocked_get_all.called is True
        assert not result

    def test_get_details_exits(self, mocker):
        org1 = create_random_organization()

        mocked_get_all = mocker.patch.object(OrganizationRepository, 'get_by_id', return_value=org1)

        result = self.service.get_details(org1.id)

        assert mocked_get_all.called is True
        assert result
        assert result.id == org1.id

    def test_get_details_does_not_exist(self, mocker):
        mocked_get_all = mocker.patch.object(OrganizationRepository, 'get_by_id', return_value=None)

        with pytest.raises(ValidationException):
            self.service.get_details(1)

        assert mocked_get_all.called is True

    def test_create(self, mocker):
        org1 = create_random_organization()

        mocked_get_all = mocker.patch.object(OrganizationService, 'get_by_name', return_value=None)
        mocked_create = mocker.patch.object(OrganizationRepository, 'create', return_value=org1)

        data = OrganizationCreateDTO(name="Name")

        result = self.service.create(data)

        assert mocked_get_all.called is True
        assert mocked_create.called is True
        assert result
        assert result.id == org1.id

    def test_create_name_already_exists(self, mocker):
        org1 = create_random_organization()

        mocked_get_all = mocker.patch.object(OrganizationService, 'get_by_name', return_value=org1)
        mocked_create = mocker.patch.object(OrganizationRepository, 'create')

        data = OrganizationCreateDTO(name="Name")

        with pytest.raises(ValidationException):
            self.service.create(data)

        assert mocked_get_all.called is True
        assert mocked_create.called is False

    def test_update(self, mocker):
        org1 = create_random_organization()

        mocked_get_all = mocker.patch.object(OrganizationService, 'get_by_id', return_value=org1)
        mocked_get_by_name = mocker.patch.object(OrganizationService, 'get_by_name', return_value=org1)
        mocked_update = mocker.patch.object(OrganizationRepository, 'update', return_value=org1)

        data = OrganizationUpdateDTO(name="Name")

        result = self.service.update(org1.id, data)

        assert mocked_get_all.called is True
        assert mocked_get_by_name.called is True
        assert mocked_update.called is True
        assert result
        assert result.id == org1.id

    def test_update_does_not_exist(self, mocker):
        org1 = create_random_organization()

        mocked_get_all = mocker.patch.object(OrganizationService, 'get_by_id', return_value=None)
        mocked_update = mocker.patch.object(OrganizationRepository, 'update')

        data = OrganizationCreateDTO(name="Name")

        with pytest.raises(ValidationException):
            self.service.update(org1.id, data)

        assert mocked_get_all.called is True
        assert mocked_update.called is False

    def test_update_name_already_exists(self, mocker):
        org1 = create_random_organization()
        org2 = create_random_organization()

        mocked_get_all = mocker.patch.object(OrganizationService, 'get_by_id', return_value=org1)
        mocked_get_by_name = mocker.patch.object(OrganizationService, 'get_by_name', return_value=org2)
        mocked_update = mocker.patch.object(OrganizationRepository, 'update')

        data = OrganizationCreateDTO(name="Name")

        with pytest.raises(ValidationException):
            self.service.update(org1.id, data)

        assert mocked_get_all.called is True
        assert mocked_get_by_name.called is True
        assert mocked_update.called is False

    def test_delete(self, mocker):
        org1 = create_random_organization()

        mocked_get_all = mocker.patch.object(OrganizationRepository, 'get_by_id', return_value=org1)
        mocked_delete = mocker.patch.object(OrganizationRepository, 'delete', return_value=org1)

        result = self.service.delete(org1.id)

        assert mocked_get_all.called is True
        assert mocked_delete.called is True
        assert result
        assert result.id == org1.id

    def test_delete_does_not_exist(self, mocker):
        org1 = create_random_organization()

        mocked_get_all = mocker.patch.object(OrganizationRepository, 'get_by_id', return_value=None)
        mocked_delete = mocker.patch.object(OrganizationRepository, 'delete')

        with pytest.raises(ValidationException):
            self.service.delete(org1.id)

        assert mocked_get_all.called is True
        assert mocked_delete.called is False
