from app.auth.dtos.register_user import RegisterUserDTO

class User(RegisterUserDTO):
    id:str
    isEmailVerified: bool = False
    
    