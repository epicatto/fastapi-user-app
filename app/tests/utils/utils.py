import random
import string
from typing import List, Optional

from app.db.database import db_session
from app.db.models import Organization, Role, User, Right
from app.main import app

reverse = app.router.url_path_for


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_id() -> int:
    return random.randint(1, 999999)


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def create_random_user(is_admin: bool = False, organization: Optional[Organization] = None,
                       roles: Optional[List[Role]] = None) -> User:
    email = random_email()
    id = random_id()
    user = User(id=id, first_name='FirstName', last_name='LastName', email=email,
                is_admin=is_admin, is_active=True)
    if organization:
        user.organization = organization
    if roles:
        user.roles = roles
    return user


def create_random_role(name: str = None, description: str = None,
                       rights: Optional[List[Right]] = None) -> Role:
    if not name:
        name = random_lower_string()
    if not description:
        description = random_lower_string()
    id = random_id()
    role = Role(id=id, name=name, description=description)
    if rights:
        role.rights = rights
    return role


def create_random_right(name: str = None, description: str = None) -> Right:
    if not name:
        name = random_lower_string()
    if not description:
        description = random_lower_string()
    id = random_id()
    right = Right(id=id, name=name, description=description)
    return right


def create_random_organization(name: str = None) -> Organization:
    if not name:
        name = random_lower_string()
    id = random_id()
    org = Organization(id=id, name=name)
    return org


def save_random_right(name: str = None, description: str = None) -> Right:
    with db_session() as db:
        right = create_random_right(name=name, description=description)
        db.add(right)
        db.commit()
        return right


def save_random_organization(name: str = None) -> Organization:
    with db_session() as db:
        org = create_random_organization(name=name)
        db.add(org)
        db.commit()
        return org


def save_random_role(name: str = None, description: str = None,
                     rights: Optional[List[Right]] = None) -> Role:
    with db_session() as db:
        role = create_random_role(name=name, description=description, rights=rights)
        db.add(role)
        db.commit()
        return role


def save_random_user(is_admin: bool = False, organization: Optional[Organization] = None,
                     roles: Optional[List[Role]] = None) -> User:
    with db_session() as db:
        user = create_random_user(is_admin=is_admin, organization=organization, roles=roles)
        db.add(user)
        db.commit()
        return user
