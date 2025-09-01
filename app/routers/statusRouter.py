from fastapi import APIRouter
from ..controllers.statusController import health_check

statusRouter = APIRouter()


@statusRouter.get("/status/", tags=["status"])
async def get_health():
    return {"status": health_check()}
