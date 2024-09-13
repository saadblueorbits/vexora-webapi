from contextlib import asynccontextmanager
from fastapi import APIRouter
from app.speakers.speaker_service import speakerService




@asynccontextmanager
async def router_lifespan(app: APIRouter):
    print("router_start")
    await speakerService.add_initial_speakers()
    yield
    print("router_end")

router = APIRouter(lifespan=router_lifespan)


@router.get("/")
async def get_speakers(page:int,count:int):
    return await speakerService.get_speakers(page,count)
