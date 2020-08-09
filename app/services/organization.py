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

    def get_by_id(self, id: int) -> Optional[OrganizationDetailsDTO]:
        with db_session() as db:
            org = self.repository.get_by_id(db, id)
            if org:
                return OrganizationDetailsDTO.from_model(org)

    def get_details(self, id: int) -> Optional[OrganizationDetailsDTO]:
        with db_session() as db:
            org = self.repository.get_by_id(db, id)
            if not org:
                raise ValidationException("Organization %s does not exist" % id)

            return OrganizationDetailsDTO.from_model(org)

    def create(self, data: OrganizationCreateDTO) -> Optional[OrganizationDetailsDTO]:
        with db_session() as db:
            org = self.repository.get_by_name(db, data.name)
            if org:
                raise ValidationException("Organization already exists with the name")
            return OrganizationDetailsDTO.from_model(self.repository.create(db, data))

    def update(self, id: int, data: OrganizationUpdateDTO) -> Optional[OrganizationDetailsDTO]:
        with db_session() as db:
            org = self.repository.get_by_id(db, id)
            if not org:
                raise ValidationException("Organization %s does not exist" % id)

            return OrganizationDetailsDTO.from_model(self.repository.update(db, org, data))

    def delete(self, id: int) -> Any:
        with db_session() as db:
            org = self.repository.get_by_id(db, id)
            if not org:
                raise ValidationException("Organization %s does not exist" % id)

            return self.repository.delete(db, org)


org_service = OrganizationService()
