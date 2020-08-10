from typing import List, Any

from fastapi import Depends, APIRouter

from app.schemas.user import UserDTO, UserDetailsDTO, UserCreateDTO, UserUpdateDTO
from app.services.user import UserService

router = APIRouter()
service = UserService()


def get_service():
    return service


@router.get("/", name="user-get-all", response_model=List[UserDTO])
def get_all(service: UserService = Depends(get_service)) -> List[UserDTO]:
    """
    Retrieve all users.
    """
    return service.get_all()


@router.get("/{id}", name="user-get-details", response_model=UserDetailsDTO)
def details(id: int, service: UserService = Depends(get_service)) -> UserDetailsDTO:
    """
    Retrieve user details.
    """
    return service.get_details(id)


@router.delete("/{id}", name="user-delete")
def delete(id: int, service: UserService = Depends(get_service)) -> Any:
    """
    Delete user.
    """
    return service.delete(id)


@router.post("/", name="user-create", response_model=UserDetailsDTO)
def create(data: UserCreateDTO, service: UserService = Depends(get_service)) -> UserDetailsDTO:
    """
    Create a new user.
    """
    return service.create(data)


@router.put("/{id}", name="user-update", response_model=UserDetailsDTO)
def update(id: int, data: UserUpdateDTO, service: UserService = Depends(get_service)) -> UserDetailsDTO:
    """
    Update user.
    """
    return service.update(id, data)


@router.put("/{id}/roles", name="user-add-roles", response_model=UserDetailsDTO)
def add_roles(id: int, roles_ids: List[int], service: UserService = Depends(get_service)) -> UserDetailsDTO:
    """
    Add roles to user.
    """
    return service.add_roles(id, roles_ids)


@router.delete("/{id}/roles", name="user-remove-roles", response_model=UserDetailsDTO)
def remove_roles(id: int, roles_ids: List[int], service: UserService = Depends(get_service)) -> UserDetailsDTO:
    """
    Remove roles from user.
    """
    return service.remove_roles(id, roles_ids)
