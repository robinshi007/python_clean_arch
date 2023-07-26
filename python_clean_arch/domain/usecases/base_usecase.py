from python_clean_arch.domain.repositories.base_repository import BaseRepository


class BaseUsecase:
    def __init__(self, repository: BaseRepository) -> None:
        self._repository = repository

    def get_list(self, schema):
        return self._repository.read_by_options(schema)

    def get_by_id(self, id: int):
        return self._repository.read_by_id(id)

    def add(self, schema):
        return self._repository.create(schema)

    def update(self, id: int, schema):
        return self._repository.update(id, schema)

    def update_attr(self, id: int, attr: str, value):
        return self._repository.update_attr(id, attr, value)

    def remove_by_id(self, id: int):
        return self._repository.soft_delete_by_id(id)
