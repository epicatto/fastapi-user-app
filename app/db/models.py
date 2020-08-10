from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref

from app.db.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    organization_id = Column(Integer, ForeignKey("organization.id"), nullable=False, index=True)
    organization = relationship("Organization", backref="users")
    roles = relationship('Role', secondary="user_role")


class Organization(Base):
    __tablename__ = "organization"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, index=True, nullable=False)


class Right(Base):
    __tablename__ = "right"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, index=True, nullable=False)
    description = Column(String(200))
    created_date_time = Column(DateTime, default=datetime.utcnow(), nullable=False)
    modified_date_time = Column(DateTime)
    roles = relationship('Role', secondary="role_right")


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, index=True, nullable=False)
    description = Column(String(200))
    created_date_time = Column(DateTime, default=datetime.utcnow(), nullable=False)
    modified_date_time = Column(DateTime)
    rights = relationship('Right', secondary="role_right")
    users = relationship('User', secondary="user_role")


class RoleRight(Base):
    __tablename__ = "role_right"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False, index=True)
    role = relationship("Role", backref=backref("role_rights", cascade="all, delete, delete-orphan"))
    right_id = Column(Integer, ForeignKey("right.id"), nullable=False, index=True)
    right = relationship("Right", backref=backref("role_rights", cascade="all, delete, delete-orphan"))
    created_date_time = Column(DateTime, default=datetime.utcnow(), nullable=False)


class UserRole(Base):
    __tablename__ = "user_role"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    user = relationship("User", backref=backref("user_roles", cascade="all, delete, delete-orphan"))
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False, index=True)
    role = relationship("Role", backref=backref("user_roles", cascade="all, delete, delete-orphan"))
    created_date_time = Column(DateTime, default=datetime.utcnow(), nullable=False)
