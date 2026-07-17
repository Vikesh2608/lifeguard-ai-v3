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

from typing import Optional

from typing import Optional

class FamilyMemberCreate(BaseModel):

    owner_email: str

    first_name: str

    last_name: str

    relationship: str

    phone: Optional[str] = ""

    email: Optional[str] = ""

    medical_notes: Optional[str] = ""

    blood_group: Optional[str] = ""

    allergies: Optional[str] = ""

    medications: Optional[str] = ""

    doctor: Optional[str] = ""

    hospital: Optional[str] = ""
