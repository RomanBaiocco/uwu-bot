import os

from sqlmodel import SQLModel, Field, JSON, create_engine, Session, select
from typing import Optional, Dict


class Guild(SQLModel, table=True):
    id: str = Field(primary_key=True)
    target: Optional[str] = None
    level: int = Field(default=0)
    webhooks: str = Field(sa_type=JSON)
    off_limits_channels: str = Field(sa_type=JSON)


DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False)


def init_db():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()


def get_session():
    return Session(engine)
