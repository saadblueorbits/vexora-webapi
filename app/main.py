from fastapi import FastAPI
from app.auth import auth_controller
from app.users import users_controller

app = FastAPI()

app.include_router(router=auth_controller.router, tags=['Auth'], prefix='/api/auth')
app.include_router(router=users_controller.router, tags=['Users'], prefix='/api/users')


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with MongoDB"}
