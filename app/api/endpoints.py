from typing import List

from fastapi import Depends, APIRouter
from starlette.responses import RedirectResponse

from app.api.schemas import RecordDTO
from app.usecases.records import RecordsUseCase

router = APIRouter()
records_usecase = RecordsUseCase()


def get_records_usecase():
    return records_usecase


@router.get("/", name="home")
def main():
    return RedirectResponse(url="/docs/")


@router.get("/records/", name="record-get-all", response_model=List[RecordDTO])
def show_records(usecase: RecordsUseCase = Depends(get_records_usecase)):
    return usecase.get_all()