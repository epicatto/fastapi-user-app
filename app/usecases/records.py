from app.api.schemas import RecordDTO
from app.db import models
from app.db.database import db_session


class RecordsUseCase:

    def get_all(self):
        with db_session() as db:
            record_list = db.query(models.Record).all()
            return [RecordDTO.from_model(i) for i in record_list]