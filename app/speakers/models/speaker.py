from datetime import datetime
from enum import Enum
from bson import ObjectId
from pydantic import BaseModel


class Gender(Enum):
    Male="Male"
    Female="Female"

class AgeGroup(Enum):
    Adult="Adult"
    Child="Child"

class Languages(Enum):
    English="English"

class Accents(Enum):
    US="US"
    British="British"
    Australian="Australian"

class Speaker(BaseModel):
    id:str|None
    created_on:datetime|None
    modified_on:datetime|None
    speakerName:str
    gender:Gender
    ageGroup:AgeGroup
    language:Languages
    accent:Accents
    owner_id:str
    audio_url:str
    local_path:str

