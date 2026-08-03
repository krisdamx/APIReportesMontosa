from pydantic import BaseModel, ConfigDict


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CurrentUserResponse(BaseModel):
    id: int
    username: str
    nombre: str

    model_config = ConfigDict(from_attributes=True)

class LogoutResponse(BaseModel):
    """
    Respuesta al cerrar sesión.
    """

    message: str

class RegisterRequest(BaseModel):
    username: str
    nombre: str
    password: str


class RegisterResponse(BaseModel):
    id: int
    username: str
    nombre: str
    message: str