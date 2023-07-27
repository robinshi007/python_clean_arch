from contextlib import AbstractContextManager
from typing import Any, Callable
from pydantic import BaseModel
from sqlalchemy import and_

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from python_clean_arch.domain.error import DuplicatedError, NotFoundError

from python_clean_arch.registry.config import get_config
from python_clean_arch.utils.common_utils import merge_dict, now_ms

from python_clean_arch.utils.query_builder import dict_to_sqlalchemy_filter_options

config = get_config()


class BaseRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]], model
    ) -> None:
        self.session_factory = session_factory
        self.model = model

    def read_by_options(self, schema: BaseModel, eager=False):
        with self.session_factory() as session:
            schema_as_dict = schema.dict(exclude_none=True)
            ordering = schema_as_dict.get("ordering", config.ORDERING)
            order_query = (
                getattr(self.model, ordering[1:]).desc()
                if ordering.startswith("-")
                else getattr(self.model, ordering).asc()
            )
            page = schema_as_dict.get("page", config.PAGE)
            page_size = schema_as_dict.get("page_size", config.PAGE_SIZE)
            filter_options = dict_to_sqlalchemy_filter_options(
                self.model,
                merge_dict(schema.dict(exclude_none=True), {"deleted_at": 0}),
            )
            query = session.query(self.model)
            if eager:
                for eager in getattr(self.model, "eagers", []):
                    query = query.options(joinedload(getattr(self.model, eager)))
            filtered_query = query.filter(filter_options)
            query = filtered_query.order_by(order_query)
            if page_size == "all":
                query = query.all()
            else:
                query = query.limit(page_size).offset((page - 1) * page_size).all()
            total_count = filtered_query.count()
            return {
                "founds": query,
                "search_options": {
                    "page": page,
                    "page_size": page_size,
                    "ordering": ordering,
                    "total_count": total_count,
                },
            }

    def read_by_id(self, id: int, eager=False, include_soft_delete=False):
        with self.session_factory() as session:
            query = session.query(self.model)
            if eager:
                query = query.options(joinedload(getattr(self.model, eager)))
            if include_soft_delete:
                query = query.filter(self.model.id == id).first()
            else:
                query = query.filter(
                    and_(self.model.id == id, self.model.deleted_at == 0)
                ).first()
            if not query:
                raise NotFoundError(detail=f"not found id : {id}")
            return query

    def create(self, schema: BaseModel):
        with self.session_factory() as session:
            now_ts = now_ms()
            query = self.model(
                **merge_dict(
                    schema.dict(),
                    {"created_at": now_ts, "updated_at": now_ts, "deleted_at": 0},
                )
            )
            try:
                session.add(query)
                session.commit()
                session.refresh(query)
            except IntegrityError as ex:
                raise DuplicatedError(detail=str(ex.orig))
            return query

    def update(self, id: int, schema: BaseModel, exclude_none: bool = True):
        with self.session_factory() as session:
            session.query(self.model).filter(self.model.id == id).update(
                merge_dict(
                    schema.dict(exclude_none=exclude_none), {"updated_at": now_ms()}
                )
            )
            session.commit()
            return self.read_by_id(id)

    def update_attr(self, id: int, column: str, value: Any):
        with self.session_factory() as session:
            session.query(self.model).filter(self.model.id == id).update(
                {column: value, "updated_at": now_ms()}
            )
            session.commit()
            return self.read_by_id(id)

    def delete_by_id(self, id: int) -> None:
        with self.session_factory() as session:
            query = session.query(self.model).filter(self.model.id == id).first()
            if not query:
                raise NotFoundError(detail=f"not found id : {id}")
            session.delete(query)
            session.commit()

    def soft_delete_by_id(self, id: int) -> None:
        with self.session_factory() as session:
            query = session.query(self.model).filter(self.model.id == id).first()
            if not query:
                raise NotFoundError(detail=f"not found id : {id}")
            session.query(self.model).filter(self.model.id == id).update(
                {"deleted_at": now_ms()}
            )
            session.commit()
