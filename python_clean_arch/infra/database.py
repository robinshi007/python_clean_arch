from typing import Callable, Any
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    MappedAsDataclass,
    Session,
    as_declarative,
    declared_attr,
    sessionmaker,
    scoped_session,
)

from contextlib import AbstractContextManager, contextmanager


class BaseSchema(MappedAsDataclass, DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


# @as_declarative()
# class BaseSchema:
#     id: Any
# __name__: str
#
# @declared_attr
# def __tablename__(cls) -> str:
#     return cls.__name__.lower()


class Database:
    def __init__(self, db_url: str, echo: bool = False) -> None:
        self._engine = create_engine(db_url, echo=echo)
        self._session_factory = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
        )

    def create_database(self) -> None:
        BaseSchema.metadata.create_all(self._engine)

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
