from fastapi.testclient import TestClient
from starlette import status

from app.db.models import Right
from app.schemas.right import RightCreateDTO, RightUpdateDTO
from app.tests.integration.conftest import reverse
from app.tests.utils.utils import save_random_right


class TestRightIntegration:

    def test_get_all(self, client: TestClient, db_session):
        save_random_right()
        save_random_right()

        url = reverse("right-get-all")
        response = client.get(url)
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(result) == 2
        for element in result:
            assert element['id'] is not None
            assert element['name'] is not None
            assert element['description'] is not None
            assert element['created_date_time'] is not None

    def test_get_details(self, client: TestClient, db_session):
        right1 = save_random_right()

        url = reverse("right-get-details", id=right1.id)
        response = client.get(url)
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert result['id'] == right1.id
        assert result['name'] == right1.name
        assert result['description'] == right1.description
        assert result['created_date_time'] is not None

    def test_get_details_does_not_exist(self, client: TestClient, db_session):
        url = reverse("right-get-details", id=1)
        response = client.get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete(self, client: TestClient, db_session):
        right1 = save_random_right()

        url = reverse("right-delete", id=right1.id)
        response = client.delete(url)

        assert response.status_code == status.HTTP_200_OK

        result = db_session.query(Right).get(right1.id)

        assert result is None

    def test_delete_does_not_exist(self, client: TestClient, db_session):
        url = reverse("right-delete", id=1)
        response = client.delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create(self, client: TestClient, db_session):
        data = RightCreateDTO(name="Name", description="Description")

        url = reverse("right-create")
        response = client.post(url, data=data.json())
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert result['id'] is not None
        assert result['name'] == data.name
        assert result['description'] == data.description
        assert result['created_date_time'] is not None

        result = db_session.query(Right).get(result['id'])
        assert result is not None

    def test_create_name_exists(self, client: TestClient, db_session):
        right1 = save_random_right()
        data = RightCreateDTO(name=right1.name, description="Description")

        url = reverse("right-create")
        response = client.post(url, data=data.json())

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update(self, client: TestClient, db_session):
        right = save_random_right()

        data = RightUpdateDTO(name="Name", description="Description")

        url = reverse("right-update", id=right.id)
        response = client.put(url, data=data.json())
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert result['id'] is not None
        assert result['name'] == data.name
        assert result['description'] == data.description
        assert result['created_date_time'] is not None
        assert result['modified_date_time'] is not None

        result = db_session.query(Right).get(right.id)
        assert result is not None
        assert result.name == data.name
        assert result.description == data.description

    def test_update_does_not_exist(self, client: TestClient, db_session):
        data = RightUpdateDTO(name="Name", description="Description")

        url = reverse("right-update", id=1)
        response = client.put(url, data=data.json())

        assert response.status_code == status.HTTP_400_BAD_REQUEST
