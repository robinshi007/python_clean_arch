import os
from typing import List

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

from python_clean_arch.utils.common_utils import get_project_root

load_dotenv()

ENV: str = ""


class Configs(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
    )
    # base
    ENV: str = os.getenv("ENV", "dev")
    PROJECT_NAME: str = "pca"
    PROJECT_ROOT: str = get_project_root()
    API: str = "/api"
    API_V1_STR: str = "/api/v1"

    ENV_DATABASE_MAPPER: dict = {
        "prod": "pca",
        "dev": "pca_dev",
        "test": "pca_test",
    }
    DB_ENGINE_MAPPER: dict = {
        "sqlite": "sqlite",
        "postgresql": "postgresql",
        "mysql": "mysql+pymysql",
    }

    # date
    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"

    # auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = (
        60 * 24 * 3
    )  # 60 minutes * 24 hours * 3 days = 3 days

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # database
    DB: str = os.getenv("DB", "postgresql")
    DB_USER: str = os.getenv("DB_USER", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "")
    DB_PORT: str = os.getenv("DB_PORT", "3306")
    DB_ENGINE: str = DB_ENGINE_MAPPER.get(DB, "postgresql")

    DATABASE_URI: str = (
        f"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{ENV_DATABASE_MAPPER[ENV]}"
        if DB != "sqlite"
        else f"sqlite:///{PROJECT_ROOT}/{ENV_DATABASE_MAPPER[ENV]}.db"
    )

    # find query
    PAGE: int = 1
    PAGE_SIZE: int = 20
    ORDERING: str = "-id"


class TestConfigs(Configs):
    ENV: str = "test"
