from typing import List, Any

from fastapi import Depends, APIRouter

from app.schemas.role import RoleDTO, RoleDetailsDTO, RoleCreateDTO, \
    RoleUpdateDTO
from app.services.role import RoleService

router = APIRouter()
service = RoleService()


def get_service():
    return service


@router.get("/", name="role-get-all", response_model=List[RoleDTO])
def show_records(service: RoleService = Depends(get_service)) -> List[RoleDTO]:
    """
    Retrieve all role.
    """
    return service.get_all()


@router.get("/{id}", name="role-get-details", response_model=RoleDetailsDTO)
def details(id: int, service: RoleService = Depends(get_service)) -> RoleDetailsDTO:
    """
    Retrieve role details.
    """
    return service.get_details(id)


@router.delete("/{id}", name="role-delete")
def delete(id: int, service: RoleService = Depends(get_service)) -> Any:
    """
    Delete a role.
    """
    return service.delete(id)


@router.post("/", name="role-create", response_model=RoleDetailsDTO)
def create(data: RoleCreateDTO, service: RoleService = Depends(get_service)) -> RoleDetailsDTO:
    """
    Create a new role.
    """
    return service.create(data)


@router.put("/{id}", name="role-update", response_model=RoleDetailsDTO)
def update(id: int, data: RoleUpdateDTO,
           service: RoleService = Depends(get_service)) -> RoleDetailsDTO:
    """
    Update a role.
    """
    return service.update(id, data)


@router.put("/{id}/rights", name="role-add-rights", response_model=RoleDetailsDTO)
def add_rights(id: int, right_ids: List[int],
               service: RoleService = Depends(get_service)) -> RoleDetailsDTO:
    """
    Add roles to a role.
    """
    return service.add_rights(id, right_ids)


@router.delete("/{id}/rights", name="role-remove-rights", response_model=RoleDetailsDTO)
def remove_rights(id: int, right_ids: List[int],
                  service: RoleService = Depends(get_service)) -> RoleDetailsDTO:
    """
    Remove roles from a role.
    """
    return service.remove_rights(id, right_ids)
