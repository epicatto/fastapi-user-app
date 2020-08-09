from fastapi.testclient import TestClient
from starlette import status

from app.db.models import Organization
from app.schemas.organization import OrganizationCreateDTO, OrganizationUpdateDTO
from app.tests.integration.conftest import reverse
from app.tests.utils.utils import save_random_organization


class TestOrganizationOrganization:

    def test_get_all(self, client: TestClient, db_session):
        save_random_organization()
        save_random_organization()

        url = reverse("organization-get-all")
        response = client.get(url)
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(result) == 2
        for element in result:
            assert element['id'] is not None
            assert element['name'] is not None

    def test_get_details(self, client: TestClient, db_session):
        org1 = save_random_organization()

        url = reverse("organization-get-details", id=org1.id)
        response = client.get(url)
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert result['id'] == org1.id
        assert result['name'] == org1.name

    def test_get_details_does_not_exist(self, client: TestClient, db_session):
        url = reverse("organization-get-details", id=1)
        response = client.get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete(self, client: TestClient, db_session):
        org1 = save_random_organization()

        url = reverse("organization-delete", id=org1.id)
        response = client.delete(url)

        assert response.status_code == status.HTTP_200_OK

        result = db_session.query(Organization).get(org1.id)

        assert result is None

    def test_delete_does_not_exist(self, client: TestClient, db_session):
        url = reverse("organization-delete", id=1)
        response = client.delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create(self, client: TestClient, db_session):
        data = OrganizationCreateDTO(name="Name")

        url = reverse("organization-create")
        response = client.post(url, data=data.json())
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert result['id'] is not None
        assert result['name'] == data.name

        result = db_session.query(Organization).get(result['id'])
        assert result is not None

    def test_create_name_exists(self, client: TestClient, db_session):
        org1 = save_random_organization()
        data = OrganizationCreateDTO(name=org1.name)

        url = reverse("organization-create")
        response = client.post(url, data=data.json())

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update(self, client: TestClient, db_session):
        org = save_random_organization()

        data = OrganizationUpdateDTO(name="Name")

        url = reverse("organization-update", id=org.id)
        response = client.put(url, data=data.json())
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert result['id'] is not None
        assert result['name'] == data.name

        result = db_session.query(Organization).get(org.id)
        assert result is not None
        assert result.name == data.name

    def test_update_does_not_exist(self, client: TestClient, db_session):
        data = OrganizationUpdateDTO(name="Name")

        url = reverse("organization-update", id=1)
        response = client.put(url, data=data.json())

        assert response.status_code == status.HTTP_400_BAD_REQUEST
