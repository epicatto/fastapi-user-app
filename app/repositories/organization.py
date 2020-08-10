from typing import List, Any

from serum import dependency
from sqlalchemy.orm import Session

from app.db.models import Organization
from app.schemas.organization import OrganizationCreateDTO, OrganizationUpdateDTO


@dependency
class OrganizationRepository:

    def get_all(self, db: Session) -> List[Organization]:
        return db.query(Organization).all()

    def get_by_id(self, db: Session, id: int) -> Organization:
        return db.query(Organization).get(id)

    def get_by_name(self, db: Session, name: str) -> Organization:
        return db.query(Organization).filter(Organization.name == name).first()

    def create(self, db: Session, data: OrganizationCreateDTO) -> Organization:
        org = Organization()
        org.name = data.name

        db.add(org)
        db.commit()
        return org

    def update(self, db: Session, org: Organization, data: OrganizationUpdateDTO) -> Organization:
        org.name = data.name

        db.commit()
        db.refresh(org)
        return org

    def delete(self, db: Session, org: Organization) -> Any:
        db.delete(org)
        db.commit()
