from sqlalchemy import Column, Integer, String
from database import Base


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
