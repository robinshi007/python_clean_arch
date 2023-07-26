from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session
from python_clean_arch.adapter.schemas.user_schema import UserSchema
from python_clean_arch.domain.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        super().__init__(session_factory, UserSchema)
