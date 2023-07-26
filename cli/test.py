from pydantic import BaseModel
import traceback
from sqlalchemy import String, select

from sqlalchemy.orm import Mapped, mapped_column
from python_clean_arch.adapter.repositories.user_repository import UserRepository
from python_clean_arch.adapter.schemas.shared import CommonMixin

from python_clean_arch.adapter.schemas.user_schema import UserSchema
from python_clean_arch.infra.database import BaseSchema, Database
from python_clean_arch.usecases.user_usecase import UserUsecase


# class UserSchema(CommonMixin, BaseSchema):
#     __tablename__ = "users"
#     name: Mapped[str] = mapped_column(String(32), index=True, unique=True)


class UserDTO(BaseModel):
    name: str


class SearchOption(BaseModel):
    ordering: str = "-id"
    page: int = 1
    page_size: int = 20


if __name__ == "__main__":
    echo = False
    db = Database("sqlite:////home/robin/projects/python_clean_arch/test.db", echo=echo)
    db.create_database()

    # with db.session() as s:
    #     bin = UserSchema(name="robin")
    #     s.add(bin)
    #     s.commit()

    # with db.session() as s:
    #     res = s.scalars(select(UserSchema))
    #     for d in list(res):
    #         print(d)
    repo = UserRepository(db.session)
    usecase = UserUsecase(repo)
    try:
        usecase.add(UserDTO(name="hi"))
    except Exception as ex:
        print(ex.detail)
        # traceback.print_exc()
        ...

    # print(repo.read_by_id(1))
    # print(repo.read_by_options(SearchOption(page=1, page_size=10, ordering="-id")))
    # print(repo.update_attr(1, "name", "rob"))
    # print(repo.soft_delete_by_id(3))
    print(usecase.get_by_id(1))
    print(usecase.get_list(SearchOption(page=1, page_size=10, ordering="-id")))
