from datetime import datetime
from typing import List, Any

from serum import dependency
from sqlalchemy.orm import Session

from app.db.models import Role, Right
from app.schemas.role import RoleCreateDTO, RoleUpdateDTO


@dependency
class RoleRepository:

    def get_all(self, db: Session) -> List[Role]:
        return db.query(Role).all()

    def get_by_id(self, db: Session, id: int) -> Role:
        return db.query(Role).get(id)

    def get_by_name(self, db: Session, name: str) -> Role:
        return db.query(Role).filter(Role.name == name).first()

    def create(self, db: Session, data: RoleCreateDTO) -> Role:
        role = Role()
        role.name = data.name
        role.description = data.description

        db.add(role)
        db.commit()
        return role

    def update(self, db: Session, id: int, data: RoleUpdateDTO) -> Role:
        role = self.get_by_id(db, id)
        role.name = data.name
        role.description = data.description
        role.modified_date_time = datetime.utcnow()

        db.commit()
        db.refresh(role)
        return role

    def delete(self, db: Session, id: int) -> Any:
        role = self.get_by_id(db, id)
        db.delete(role)
        db.commit()

    def add_rights(self, db: Session, id: int, right_ids: List[int]):
        role = self.get_by_id(db, id)
        for right_id in right_ids:
            right = db.query(Right).get(right_id)
            role.rights.append(right)

        db.commit()
        db.refresh(role)
        return role

    def remove_rights(self, db: Session, id: int, right_ids: List[int]):
        role = self.get_by_id(db, id)
        for right_id in right_ids:
            right = db.query(Right).get(right_id)
            role.rights.remove(right)

        db.commit()
        db.refresh(role)
        return role
