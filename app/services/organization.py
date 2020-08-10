from typing import List, Optional, Any

from serum import inject, dependency

from app.config.exceptions import ValidationException
from app.db.database import db_session
from app.repositories.organization import OrganizationRepository
from app.schemas.organization import OrganizationDTO, OrganizationCreateDTO, OrganizationUpdateDTO, \
    OrganizationDetailsDTO


@inject
@dependency
class OrganizationService:
    repository: OrganizationRepository

    def get_all(self) -> List[OrganizationDTO]:
        with db_session() as db:
            orgs = self.repository.get_all(db)
            return [OrganizationDTO.from_model(i) for i in orgs]

    def get_by_id(self, id: int) -> Optional[OrganizationDTO]:
        with db_session() as db:
            org = self.repository.get_by_id(db, id)
            if org:
                return OrganizationDTO.from_model(org)

    def get_by_name(self, name: str) -> Optional[OrganizationDTO]:
        with db_session() as db:
            org = self.repository.get_by_name(db, name)
            if org:
                return OrganizationDTO.from_model(org)

    def get_details(self, id: int) -> Optional[OrganizationDetailsDTO]:
        with db_session() as db:
            org = self.repository.get_by_id(db, id)
            if not org:
                raise ValidationException("Organization %s does not exist" % id)

            return OrganizationDetailsDTO.from_model(org)

    def create(self, data: OrganizationCreateDTO) -> Optional[OrganizationDetailsDTO]:
        org = self.get_by_name(data.name)
        if org:
            raise ValidationException("Organization already exists with the name")

        with db_session() as db:
            return OrganizationDetailsDTO.from_model(self.repository.create(db, data))

    def update(self, id: int, data: OrganizationUpdateDTO) -> Optional[OrganizationDetailsDTO]:
        org = self.get_by_id(id)
        if not org:
            raise ValidationException("Organization %s does not exist" % id)

        org_with_name = self.get_by_name(data.name)
        if org_with_name and org_with_name.id != id:
            raise ValidationException("Organization already exists with the name")

        with db_session() as db:
            return OrganizationDetailsDTO.from_model(self.repository.update(db, id, data))

    def delete(self, id: int) -> Any:
        org = self.get_by_id(id)
        if not org:
            raise ValidationException("Organization %s does not exist" % id)

        with db_session() as db:
            return self.repository.delete(db, id)
