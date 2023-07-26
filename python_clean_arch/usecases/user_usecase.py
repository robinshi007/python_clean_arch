from python_clean_arch.adapter.repositories.user_repository import UserRepository
from python_clean_arch.domain.usecases.base_usecase import BaseUsecase


class UserUsecase(BaseUsecase):
    def __init__(self, user_repository: UserRepository) -> None:
        # self.user_repository = user_repository
        super().__init__(user_repository)
