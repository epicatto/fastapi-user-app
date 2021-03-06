from typing import List, Any

from serum import dependency
from sqlalchemy.orm import Session

from app.db.models import User, Role
from app.schemas.user import UserCreateDTO, UserUpdateDTO


@dependency
class UserRepository:

    def get_all(self, db: Session) -> List[User]:
        return db.query(User).all()

    def get_by_id(self, db: Session, id: int) -> User:
        return db.query(User).get(id)

    def create(self, db: Session, data: UserCreateDTO) -> User:
        user = User()
        user.first_name = data.first_name
        user.last_name = data.last_name
        user.email = data.email
        user.is_admin = data.is_admin
        user.organization_id = data.organization_id

        db.add(user)
        db.commit()
        return user

    def update(self, db: Session, id: int, data: UserUpdateDTO) -> User:
        user = self.get_by_id(db, id)
        user.first_name = data.first_name
        user.last_name = data.last_name
        user.is_admin = data.is_admin
        user.is_active = data.is_active
        user.organization_id = data.organization_id

        db.commit()
        db.refresh(user)
        return user

    def delete(self, db: Session, id: int) -> Any:
        user = self.get_by_id(db, id)
        db.delete(user)
        db.commit()

    def get_by_email(self, db: Session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()

    def add_roles(self, db: Session, id: int, role_ids: List[int]) -> User:
        user = self.get_by_id(db, id)
        for role_id in role_ids:
            role = db.query(Role).get(role_id)
            user.roles.append(role)

        db.commit()
        db.refresh(user)
        return user

    def remove_roles(self, db: Session, id: int, role_ids: List[int]) -> User:
        user = self.get_by_id(db, id)
        for role_id in role_ids:
            role = db.query(Role).get(role_id)
            user.roles.remove(role)

        db.commit()
        db.refresh(user)
        return user
