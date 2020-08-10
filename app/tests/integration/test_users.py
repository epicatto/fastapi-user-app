from fastapi.testclient import TestClient
from starlette import status

from app.db.models import User
from app.schemas.user import UserCreateDTO, UserUpdateDTO
from app.tests.integration.conftest import reverse
from app.tests.utils.utils import save_random_user, save_random_organization, save_random_role


class TestUserIntegration:

    def test_get_all(self, client: TestClient, db_session):
        org1 = save_random_organization()
        save_random_user(organization=org1)
        save_random_user(organization=org1)

        url = reverse("user-get-all")
        response = client.get(url)
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(result) == 2
        for element in result:
            assert element['id'] is not None
            assert element['email'] is not None
            assert element['first_name'] is not None
            assert element['last_name'] is not None
            assert element['is_admin'] is not None
            assert element['is_active'] is not None

    def test_get_details(self, client: TestClient, db_session):
        org = save_random_organization()
        user1 = save_random_user(organization=org)

        url = reverse("user-get-details", id=user1.id)
        response = client.get(url)
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert result['id'] == user1.id
        assert result['email'] == user1.email
        assert result['first_name'] == user1.first_name
        assert result['last_name'] == user1.last_name
        assert result['is_admin'] == user1.is_admin
        assert result['is_active'] == user1.is_active
        assert result['organization']['id'] == user1.organization.id

    def test_get_details_does_not_exist(self, client: TestClient, db_session):
        url = reverse("user-get-details", id=1)
        response = client.get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete(self, client: TestClient, db_session):
        org = save_random_organization()
        user1 = save_random_user(organization=org)
        id = user1.id

        url = reverse("user-delete", id=id)
        response = client.delete(url)

        assert response.status_code == status.HTTP_200_OK

        result = db_session.query(User).get(id)
        assert result is None

    def test_delete_does_not_exist(self, client: TestClient, db_session):
        url = reverse("user-delete", id=1)
        response = client.delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create(self, client: TestClient, db_session):
        org = save_random_organization()
        data = UserCreateDTO(email="test@test.com",
                             first_name="FirstName",
                             last_name="LastName",
                             is_admin=True,
                             organization_id=org.id)

        url = reverse("user-create")
        response = client.post(url, data=data.json())
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert result['id'] is not None
        assert result['email'] == data.email
        assert result['first_name'] == data.first_name
        assert result['last_name'] == data.last_name
        assert result['is_admin'] == data.is_admin
        assert result['is_active']
        assert result['organization']['id'] == data.organization_id

        result = db_session.query(User).get(result['id'])
        assert result is not None
        assert result.email == data.email
        assert result.first_name == data.first_name
        assert result.last_name == data.last_name
        assert result.is_admin == data.is_admin
        assert result.organization.id == data.organization_id

    def test_create_email_exists(self, client: TestClient, db_session):
        org = save_random_organization()
        user1 = save_random_user(organization=org)

        data = UserCreateDTO(email=user1.email,
                             first_name="FirstName",
                             last_name="LastName",
                             is_admin=True,
                             organization_id=org.id)

        url = reverse("user-create")
        response = client.post(url, data=data.json())

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update(self, client: TestClient, db_session):
        org1 = save_random_organization()
        org2 = save_random_organization()
        user = save_random_user(organization=org1)

        data = UserUpdateDTO(first_name="FirstName2",
                             last_name="LastName2",
                             is_admin=False,
                             is_active=False,
                             organization_id=org2.id)

        url = reverse("user-update", id=user.id)
        response = client.put(url, data=data.json())
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert result['id'] is not None
        assert result['first_name'] == data.first_name
        assert result['last_name'] == data.last_name
        assert result['is_admin'] == data.is_admin
        assert result['is_active'] == data.is_active
        assert result['organization']['id'] == data.organization_id

        result = db_session.query(User).get(result['id'])
        assert result is not None
        assert result.first_name == data.first_name
        assert result.last_name == data.last_name
        assert result.is_admin == data.is_admin
        assert result.organization.id == data.organization_id

    def test_update_does_not_exist(self, client: TestClient, db_session):
        org = save_random_organization()
        data = UserUpdateDTO(first_name="FirstName",
                             last_name="LastName",
                             is_admin=True,
                             organization_id=org.id)

        url = reverse("user-update", id=1)
        response = client.put(url, data=data.json())

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_add_roles(self, client: TestClient, db_session):
        org1 = save_random_organization()
        user1 = save_random_user(organization=org1)
        role1 = save_random_role()

        url = reverse("user-add-roles", id=user1.id)
        response = client.put(url, json=list([role1.id]))
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert result['id'] == user1.id
        assert result['email'] == user1.email
        assert result['first_name'] == user1.first_name
        assert result['last_name'] == user1.last_name
        assert result['is_admin'] == user1.is_admin
        assert result['is_active'] == user1.is_active
        assert result['organization']['id'] == user1.organization.id
        assert len(result['roles']) == 1
        assert result['roles'][0]['id'] == role1.id

        result = db_session.query(User).get(user1.id)
        assert len(result.roles) == 1
        assert result.roles[0].id == role1.id

    def test_add_roles_role_does_not_exist(self, client: TestClient, db_session):
        org1 = save_random_organization()
        user1 = save_random_user(organization=org1)

        url = reverse("user-add-roles", id=user1.id)
        response = client.put(url, json=list([1]))
        response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_remove_roles(self, client: TestClient, db_session):
        role1 = save_random_role()
        org1 = save_random_organization()
        user1 = save_random_user(organization=org1, roles=[role1])

        url = reverse("user-remove-roles", id=user1.id)
        response = client.delete(url, json=list([role1.id]))
        result = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert result['id'] == user1.id
        assert result['email'] == user1.email
        assert result['first_name'] == user1.first_name
        assert result['last_name'] == user1.last_name
        assert result['is_admin'] == user1.is_admin
        assert result['is_active'] == user1.is_active
        assert result['organization']['id'] == user1.organization.id
        assert len(result['roles']) == 0

    def test_remove_roles_role_does_not_exist(self, client: TestClient, db_session):
        role1 = save_random_role()
        org1 = save_random_organization()
        user1 = save_random_user(organization=org1, roles=[role1])

        url = reverse("user-remove-roles", id=user1.id)
        response = client.delete(url, json=list([1]))
        response.json()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
