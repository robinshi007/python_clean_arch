from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from python_clean_arch.adapter.schemas.shared import CommonMixin
from python_clean_arch.infra.database import BaseSchema
from python_clean_arch.utils.common_utils import timestamp_to_date_str


class UserSchema(BaseSchema, CommonMixin):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(32), index=True, unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name={self.name} is_active={self.is_active} {timestamp_to_date_str(self.created_at/1000)} {timestamp_to_date_str(self.updated_at/1000)})"
