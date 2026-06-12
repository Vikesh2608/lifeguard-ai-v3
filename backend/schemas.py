from pydantic import BaseModel


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class WellnessCreate(BaseModel):
    email: str
    mood: str
    sleep_hours: int
    stress_level: int

class AIRequest(BaseModel):
    message: str
