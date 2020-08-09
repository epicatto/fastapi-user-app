from typing import List, Optional, Any

from serum import dependency, inject

from app.config.exceptions import ValidationException
from app.db.database import db_session
from app.repositories.right import RightRepository
from app.schemas.right import RightDTO, RightCreateDTO, RightUpdateDTO


@inject
@dependency
class RightService:
    repository: RightRepository

    def get_all(self) -> List[RightDTO]:
        with db_session() as db:
            rights = self.repository.get_all(db)
            return [RightDTO.from_model(i) for i in rights]

    def get_by_id(self, id: int) -> Optional[RightDTO]:
        with db_session() as db:
            user = self.repository.get_by_id(db, id)
            if user:
                return RightDTO.from_model(user)

    def get_details(self, id: int) -> Optional[RightDTO]:
        with db_session() as db:
            right = self.repository.get_by_id(db, id)
            if not right:
                raise ValidationException("Right %s does not exist" % id)

            return RightDTO.from_model(right)

    def create(self, data: RightCreateDTO) -> Optional[RightDTO]:
        with db_session() as db:
            right = self.repository.get_by_name(db, data.name)
            if right:
                raise ValidationException("Right already exists with the name")
            return RightDTO.from_model(self.repository.create(db, data))

    def update(self, id: int, data: RightUpdateDTO) -> Optional[RightDTO]:
        with db_session() as db:
            right = self.repository.get_by_id(db, id)
            if not right:
                raise ValidationException("Right %s does not exist" % id)

            right_with_name = self.repository.get_by_name(db, data.name)
            if right_with_name and right_with_name.id != id:
                raise ValidationException("Right already exists with the name")

            return RightDTO.from_model(self.repository.update(db, right, data))

    def delete(self, id: int) -> Any:
        with db_session() as db:
            right = self.repository.get_by_id(db, id)
            if not right:
                raise ValidationException("Right %s does not exist" % id)

            return self.repository.delete(db, right)


right_service = RightService()
