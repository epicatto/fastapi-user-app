from datetime import date
from pydantic import BaseModel

from app.db.models import Record


class RecordDTO(BaseModel):
    id: int
    date: date
    country: str
    cases: int
    deaths: int
    recoveries: int

    @classmethod
    def from_model(cls, instance: Record):
        """
        Convert Record model instance to an RecordDTO instance.
        """
        return cls(
            id=instance.id,
            date=instance.date,
            country=instance.country,
            cases=instance.cases,
            deaths=instance.deaths,
            recoveries=instance.recoveries,
        )

    # class Config:
    #     orm_mode = True