import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from python_clean_arch.registry.config import get_config
from python_clean_arch.registry.container import Container
from python_clean_arch.adapter.rest.v1.routes import routers as routers_v1
from python_clean_arch.registry.fastapi_creator import FastAPICreator


app_creator = FastAPICreator()
app = app_creator.app

if __name__ == "__main__":
    uvicorn.run(
        app="http_server_cli:app",
        host="127.0.0.1",
        port=5000,
        reload=True,
    )
