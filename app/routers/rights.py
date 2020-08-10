from typing import List, Any

from fastapi import Depends, APIRouter

from app.schemas.right import RightDTO, RightCreateDTO, \
    RightUpdateDTO
from app.services.right import RightService

router = APIRouter()
service = RightService()


def get_service():
    return service


@router.get("/", name="right-get-all", response_model=List[RightDTO])
def show_records(service: RightService = Depends(get_service)) -> List[RightDTO]:
    """
    Retrieve all rights.
    """
    return service.get_all()


@router.get("/{id}", name="right-get-details", response_model=RightDTO)
def details(id: int, service: RightService = Depends(get_service)) -> RightDTO:
    """
    Retrieve right details.
    """
    return service.get_details(id)


@router.delete("/{id}", name="right-delete")
def delete(id: int, service: RightService = Depends(get_service)) -> Any:
    """
    Delete a right.
    """
    return service.delete(id)


@router.post("/", name="right-create", response_model=RightDTO)
def create(data: RightCreateDTO, service: RightService = Depends(get_service)) -> RightDTO:
    """
    Create a new right.
    """
    return service.create(data)


@router.put("/{id}", name="right-update", response_model=RightDTO)
def update(id: int, data: RightUpdateDTO,
           service: RightService = Depends(get_service)) -> RightDTO:
    """
    Update a right.
    """
    return service.update(id, data)
