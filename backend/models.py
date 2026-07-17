from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    first_name = Column(String)

    last_name = Column(String)

    email = Column(String, unique=True, index=True)

    password = Column(String)


class Wellness(Base):
    __tablename__ = "wellness"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String)

    mood = Column(String)

    sleep_hours = Column(Integer)

    stress_level = Column(Integer)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class FamilyMember(Base):
    __tablename__ = "family_members"

    id = Column(Integer, primary_key=True, index=True)

    owner_email = Column(String, index=True)

    first_name = Column(String)
    last_name = Column(String)

    relationship = Column(String)

    phone = Column(String)

    email = Column(String)

    medical_notes = Column(String)

    blood_group = Column(String)

    allergies = Column(String)

    medications = Column(String)

    doctor = Column(String)

    hospital = Column(String)
