from fastapi.testclient import TestClient
from starlette import status

from app.db.models import Role
from app.schemas.role import RoleCreateDTO, RoleUpdateDTO
from app.tests.integration.conftest import reverse
from app.tests.utils.utils import save_random_role, save_random_right


class TestRoleIntegration:

    def test_get_all(self, client: TestClient, db_session):
        save_random_role()
        save_random_role()

        url = reverse("role-get-all")
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
        role1 = save_random_role()

        url = reverse("role-get-details", id=role1.id)
        response = client.get(url)
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert result['id'] == role1.id
        assert result['name'] == role1.name
        assert result['description'] == role1.description
        assert result['created_date_time'] is not None

    def test_get_details_does_not_exist(self, client: TestClient, db_session):
        url = reverse("role-get-details", id=1)
        response = client.get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete(self, client: TestClient, db_session):
        role1 = save_random_role()

        url = reverse("role-delete", id=role1.id)
        response = client.delete(url)

        assert response.status_code == status.HTTP_200_OK

        result = db_session.query(Role).get(role1.id)

        assert result is None

    def test_delete_does_not_exist(self, client: TestClient, db_session):
        url = reverse("role-delete", id=1)
        response = client.delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create(self, client: TestClient, db_session):
        data = RoleCreateDTO(name="Name", description="Description")

        url = reverse("role-create")
        response = client.post(url, data=data.json())
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert result['id'] is not None
        assert result['name'] == data.name
        assert result['description'] == data.description
        assert result['created_date_time'] is not None

        result = db_session.query(Role).get(result['id'])
        assert result is not None

    def test_create_name_exists(self, client: TestClient, db_session):
        role1 = save_random_role()
        data = RoleCreateDTO(name=role1.name, description="Description")

        url = reverse("role-create")
        response = client.post(url, data=data.json())

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update(self, client: TestClient, db_session):
        role = save_random_role()

        data = RoleUpdateDTO(name="Name", description="Description")

        url = reverse("role-update", id=role.id)
        response = client.put(url, data=data.json())
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert result['id'] is not None
        assert result['name'] == data.name
        assert result['description'] == data.description
        assert result['created_date_time'] is not None
        assert result['modified_date_time'] is not None

        result = db_session.query(Role).get(role.id)
        assert result is not None
        assert result.name == data.name
        assert result.description == data.description

    def test_update_does_not_exist(self, client: TestClient, db_session):
        data = RoleUpdateDTO(name="Name", description="Description")

        url = reverse("role-update", id=1)
        response = client.put(url, data=data.json())

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_add_rights(self, client: TestClient, db_session):
        role1 = save_random_role()
        right1 = save_random_right()

        url = reverse("role-add-rights", id=role1.id)
        response = client.put(url, json=list([right1.id]))
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert result['id'] == role1.id
        assert result['name'] == role1.name
        assert result['description'] == role1.description
        assert result['created_date_time'] is not None
        assert result['rights'] is not None
        assert len(result['rights']) == 1
        assert result['rights'][0]['id'] == right1.id

        result = db_session.query(Role).get(role1.id)
        assert len(result.rights) == 1
        assert result.rights[0].id == right1.id

    def test_add_rights_right_does_not_exist(self, client: TestClient, db_session):
        role1 = save_random_role()

        url = reverse("role-add-rights", id=role1.id)
        response = client.put(url, json=list([1]))
        response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_remove_rights(self, client: TestClient, db_session):
        right1 = save_random_right()
        role1 = save_random_role(rights=[right1])

        url = reverse("role-remove-rights", id=role1.id)
        response = client.delete(url, json=list([right1.id]))
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert result['id'] == role1.id
        assert result['name'] == role1.name
        assert result['description'] == role1.description
        assert result['created_date_time'] is not None
        assert result['rights'] is not None
        assert len(result['rights']) == 0

    def test_remove_rights_right_does_not_exist(self, client: TestClient, db_session):
        role1 = save_random_role()

        url = reverse("role-remove-rights", id=role1.id)
        response = client.delete(url, json=list([1]))
        response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
