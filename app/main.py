from app.celery.worker import create_task
from fastapi import FastAPI
from app.auth import auth_controller
from app.users import users_controller
from app.speakers import speaker_controller






app = FastAPI()

app.include_router(router=auth_controller.router, tags=['Auth'], prefix='/api/auth')
app.include_router(router=users_controller.router, tags=['Users'], prefix='/api/users')
app.include_router(router=speaker_controller.router, tags=['Speakers'], prefix='/api/speakers')

@app.get("/api/")
def health_check():
    return "running"

@app.get("/api/healthchecker")
def root():
    task = create_task.delay(int("1"))
    return {"message": "Welcome to FastAPI with MongoDB"}
 