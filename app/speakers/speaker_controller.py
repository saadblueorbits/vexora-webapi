from contextlib import asynccontextmanager
from fastapi import APIRouter, Depends
from app import oauth2
from app.speakers.speaker_service import speakerService
from app.users.models.user import User




@asynccontextmanager
async def router_lifespan(app: APIRouter):
    print("router_start")
    await speakerService.add_initial_speakers()
    yield
    print("router_end")

router = APIRouter(lifespan=router_lifespan)


@router.get("/")
async def get_speakers(page:int,count:int,user:User = Depends(oauth2.get_current_user)):
    return await speakerService.get_speakers(page,count)
