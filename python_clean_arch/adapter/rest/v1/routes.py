from fastapi import APIRouter

from python_clean_arch.adapter.rest.v1.endpoints.user import router as user_router

routers = APIRouter()
router_list = [user_router]

for router in router_list:
    router.tags.append("v1")
    routers.include_router(router)
