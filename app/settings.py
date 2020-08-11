from typing import Any, Dict, Optional

from pydantic import BaseSettings, PostgresDsn, validator
from sqlalchemy.util import portable_instancemethod


class Settings(BaseSettings):
    DB_SCHEME: str
    DB_SERVER: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        if values.get("DB_SCHEME") == "sqlite":
            return values.get("DB_SCHEME") + ":///./" + values.get('DB_NAME')
        else:
            return PostgresDsn.build(
                scheme=values.get("DB_SCHEME"),
                port=values.get("DB_PORT"),
                user=values.get("DB_USER"),
                password=values.get("DB_PASSWORD"),
                host=values.get("DB_SERVER"),
                path=f"/{values.get('DB_NAME') or ''}",
            )

    class Config:
        case_sensitive = True


settings = Settings()
