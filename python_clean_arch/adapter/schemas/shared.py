from dataclasses import dataclass
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column


class CommonMixin(MappedAsDataclass):
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    created_at: Mapped[int] = mapped_column()  # ms
    updated_at: Mapped[int] = mapped_column()  # ms
    deleted_at: Mapped[int] = mapped_column(index=True)
