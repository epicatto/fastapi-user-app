from typing import List, Any

from fastapi import Depends, APIRouter

from app.schemas.organization import OrganizationDTO, OrganizationDetailsDTO, OrganizationCreateDTO, \
    OrganizationUpdateDTO
from app.services.organization import OrganizationService

router = APIRouter()
service = OrganizationService()


def get_service():
    return service


@router.get("/", name="organization-get-all", response_model=List[OrganizationDTO])
def show_records(service: OrganizationService = Depends(get_service)) -> List[OrganizationDTO]:
    """
    Retrieve all organizations.
    """
    return service.get_all()


@router.get("/{id}", name="organization-get-details", response_model=OrganizationDetailsDTO)
def details(id: int, service: OrganizationService = Depends(get_service)) -> OrganizationDetailsDTO:
    """
    Retrieve organization details.
    """
    return service.get_details(id)


@router.delete("/{id}", name="organization-delete")
def delete(id: int, service: OrganizationService = Depends(get_service)) -> Any:
    """
    Delete an organization.
    """
    return service.delete(id)


@router.post("/", name="organization-create", response_model=OrganizationDetailsDTO)
def create(data: OrganizationCreateDTO, service: OrganizationService = Depends(get_service)) -> OrganizationDetailsDTO:
    """
    Create a new organization.
    """
    return service.create(data)


@router.put("/{id}", name="organization-update", response_model=OrganizationDetailsDTO)
def update(id: int, data: OrganizationUpdateDTO,
           service: OrganizationService = Depends(get_service)) -> OrganizationDetailsDTO:
    """
    Update an organization.
    """
    return service.update(id, data)
