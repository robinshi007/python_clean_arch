from dependency_injector import containers, providers
from python_clean_arch.adapter.repositories.user_repository import UserRepository
from python_clean_arch.infra.database import Database
from python_clean_arch.registry.config import get_config
from python_clean_arch.usecases.user_usecase import UserUsecase

config = get_config()


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "python_clean_arch.adapter.rest.v1.endpoints.user",
            "python_clean_arch.adapter.graphql.context",
        ]
    )

    db = providers.Singleton(Database, db_url=config.DATABASE_URI)

    user_repository = providers.Factory(
        UserRepository, session_factory=db.provided.session
    )
    user_usecase = providers.Factory(UserUsecase, user_repository=user_repository)
