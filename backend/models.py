from sqlalchemy import Column, Integer, String

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    first_name = Column(String)
    last_name = Column(String)

    email = Column(String, unique=True, index=True)

    password = Column(String)

class WellnessLog(Base):
    __tablename__ = "wellness_logs"

    id = Column(Integer, primary_key=True, index=True)

    sleep_hours = Column(Integer)
    water_glasses = Column(Integer)

    mood = Column(String)
