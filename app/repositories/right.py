from datetime import datetime
from typing import List, Any

from serum import dependency
from sqlalchemy.orm import Session

from app.db.models import Right
from app.schemas.right import RightCreateDTO, RightUpdateDTO


@dependency
class RightRepository:

    def get_all(self, db: Session) -> List[Right]:
        return db.query(Right).all()

    def get_by_id(self, db: Session, id: int) -> Right:
        return db.query(Right).get(id)

    def get_by_name(self, db: Session, name: str) -> Right:
        return db.query(Right).filter(Right.name == name).first()

    def create(self, db: Session, data: RightCreateDTO) -> Right:
        right = Right()
        right.name = data.name
        right.description = data.description

        db.add(right)
        db.commit()
        return right

    def update(self, db: Session, id: int, data: RightUpdateDTO) -> Right:
        right = self.get_by_id(db, id)
        right.name = data.name
        right.description = data.description
        right.modified_date_time = datetime.utcnow()

        db.commit()
        db.refresh(right)
        return right

    def delete(self, db: Session, id: int) -> Any:
        right = self.get_by_id(db, id)
        db.delete(right)
        db.commit()
