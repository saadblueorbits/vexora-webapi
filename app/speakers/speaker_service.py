from datetime import datetime
import json
import os
from app.speakers.models.speaker import Accents, AgeGroup, Gender, Languages, Speaker
from app.database import Speakers

class SpeakerService:

    def get_speaker_path(self,speakerName:str):
        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)
        script_dir = script_dir.replace('/app/speakers','/voices/'+speakerName+'.mp3')
        return script_dir

    async def add_initial_speakers(self):
        speakers = [
            Speaker(
                speakerName="Joey",gender=Gender.Male,
                ageGroup=AgeGroup.Adult,language=Languages.English,
                accent=Accents.US,local_path=self.get_speaker_path("Joey"),
                audio_url="https://firebasestorage.googleapis.com/v0/b/voxera-41bee.appspot.com/o/voices%2FJoey.mp3?alt=media&token=f88c50fa-8365-4171-9ecb-b654cd18f3b0",
                owner_id="system",created_on=datetime.now(),modified_on=datetime.now(),id=None
            ),
            Speaker(
                speakerName="Justin",gender=Gender.Male,
                ageGroup=AgeGroup.Child,language=Languages.English,
                accent=Accents.US,local_path=self.get_speaker_path("Justin"),
                audio_url="https://firebasestorage.googleapis.com/v0/b/voxera-41bee.appspot.com/o/voices%2FJustin.mp3?alt=media&token=917b088b-4b0c-41a3-a2ae-eb2f6da7dac3",
                owner_id="system",created_on=datetime.now(),modified_on=datetime.now(),id=None
            ),
            Speaker(
                speakerName="Mathew",gender=Gender.Male,
                ageGroup=AgeGroup.Adult,language=Languages.English,
                accent=Accents.US,local_path=self.get_speaker_path("Mathew"),
                audio_url="https://firebasestorage.googleapis.com/v0/b/voxera-41bee.appspot.com/o/voices%2FMatthew.mp3?alt=media&token=1a0a43aa-a6f0-4af2-a90a-0e7fd137374f",
                owner_id="system",created_on=datetime.now(),modified_on=datetime.now(),id=None
            ),
            Speaker(
                speakerName="Brian",gender=Gender.Male,
                ageGroup=AgeGroup.Adult,language=Languages.English,
                accent=Accents.British,local_path=self.get_speaker_path("Brian"),
                audio_url="https://firebasestorage.googleapis.com/v0/b/voxera-41bee.appspot.com/o/voices%2FBrian.mp3?alt=media&token=9549111b-3b56-4c4b-9230-38d20b61f57d",
                owner_id="system",created_on=datetime.now(),modified_on=datetime.now(),id=None
            ),
            Speaker(
                speakerName="Olivia",gender=Gender.Female,
                ageGroup=AgeGroup.Adult,language=Languages.English,
                accent=Accents.Australian,local_path=self.get_speaker_path("Olivia"),
                audio_url="https://firebasestorage.googleapis.com/v0/b/voxera-41bee.appspot.com/o/voices%2FOlivia.mp3?alt=media&token=8e013ba1-dfc9-4030-9d82-36af03b7b406",
                owner_id="system",created_on=datetime.now(),modified_on=datetime.now(),id=None
            ),
            Speaker(
                speakerName="Amy",gender=Gender.Female,
                ageGroup=AgeGroup.Adult,language=Languages.English,
                accent=Accents.British,local_path=self.get_speaker_path("Amy"),
                audio_url="https://firebasestorage.googleapis.com/v0/b/voxera-41bee.appspot.com/o/voices%2FAmy.mp3?alt=media&token=99fdf280-487e-4243-bf28-441f5ff3e5be",
                owner_id="system",created_on=datetime.now(),modified_on=datetime.now(),id=None
            ),
            Speaker(
                speakerName="Kimberly",gender=Gender.Female,
                ageGroup=AgeGroup.Adult,language=Languages.English,
                accent=Accents.US,local_path=self.get_speaker_path("Kimberly"),
                audio_url="https://firebasestorage.googleapis.com/v0/b/voxera-41bee.appspot.com/o/voices%2FKimberly.mp3?alt=media&token=8456f35e-edd2-4ee6-bd6e-b1ee8343e2b4",
                owner_id="system",created_on=datetime.now(),modified_on=datetime.now(),id=None
            ),
            Speaker(
                speakerName="Ivy",gender=Gender.Female,
                ageGroup=AgeGroup.Child,language=Languages.English,
                accent=Accents.US,local_path=self.get_speaker_path("Ivy"),
                audio_url="https://firebasestorage.googleapis.com/v0/b/voxera-41bee.appspot.com/o/voices%2FIvy.mp3?alt=media&token=7b87140a-7376-4fde-90e8-41372415b934",
                owner_id="system",created_on=datetime.now(),modified_on=datetime.now(),id=None
            )
        ]
        for speaker in speakers:
            speakerJSON = json.loads(speaker.model_dump_json()) 
            del speakerJSON['id']
            await Speakers.find_one_and_update({"speakerName":speaker.speakerName},{"$set":speakerJSON},upsert=True)

    async def get_speakers(self,page:int,count:int):
        totalCount = await Speakers.count_documents({})
        speakersJSON = await Speakers.find({}).skip((page-1)*count).limit(count).to_list(length=count)
        speakers_objects = map(lambda speaker_dict: Speaker(**speaker_dict,id= str(speaker_dict["_id"])), speakersJSON)
        speakers = list(speakers_objects)
        return {'data':speakers,'totalcount':totalCount}

speakerService = SpeakerService()