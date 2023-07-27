from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from python_clean_arch.registry.config import get_config
from python_clean_arch.registry.container import Container
from python_clean_arch.utils.class_object import singleton

from python_clean_arch.adapter.rest.v1.routes import routers as routers_v1
from python_clean_arch.adapter.graphql.router import router as router_graphql


@singleton
class FastAPICreator:
    def __init__(self) -> None:
        self.config = get_config()
        self.app = FastAPI(
            title=self.config.PROJECT_NAME,
            openapi_url=f"{self.config.API}/openapi.json",
            version="0.0.1",
        )
        if self.config.BACKEND_CORS_ORIGINS:
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=[
                    str(origin) for origin in self.config.BACKEND_CORS_ORIGINS
                ],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        self.container = Container()
        self.db = self.container.db()
        self.db.create_database()

        @self.app.get("/")
        def root():
            return {"status": "ok"}

        self.app.include_router(routers_v1, prefix=self.config.API_V1_STR)
        self.app.include_router(
            router_graphql, prefix="/graphql", include_in_schema=True
        )
