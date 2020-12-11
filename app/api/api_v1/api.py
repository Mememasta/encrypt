from fastapi import APIRouter

from app.api.api_v1.endpoints import utils


api_router_v1 = APIRouter()
api_router_v1.include_router(utils.router, prefix="/utils", tags=["utils"])