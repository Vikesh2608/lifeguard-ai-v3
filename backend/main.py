from fastapi import FastAPI
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models
import schemas

from auth import hash_password, verify_password

app = FastAPI(
    title="LifeGuard AI"
)

# Create database tables
models.Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "LifeGuard AI v3 Running Successfully"
    }


@app.get("/debug")
def debug():
    return {
        "version": "v3",
        "status": "debug endpoint working"
    }


@app.get("/vikesh-test")
def test():
    return {
        "status": "SUCCESS",
        "message": "Backend Connected"
    }


@app.post("/register")
def register_user(
    user: schemas.UserCreate
):
    db = SessionLocal()

    existing_user = (
        db.query(models.User)
        .filter(models.User.email == user.email)
        .first()
    )

    if existing_user:
        return {
            "message": "Email already registered"
        }

    new_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()

    return {
        "message": "User Registered Successfully"
    }


@app.post("/login")
def login_user(
    user: schemas.UserLogin
):
    db = SessionLocal()

    existing_user = (
        db.query(models.User)
        .filter(
            models.User.email == user.email
        )
        .first()
    )

    if existing_user and verify_password(
        user.password,
        existing_user.password
    ):
        return {
            "message": "Login Successful"
        }

    return {
        "message": "Invalid Credentials"
    }

@app.post("/wellness")
def create_wellness(
    wellness: schemas.WellnessCreate
):
    db = SessionLocal()

    new_log = models.WellnessLog(
        sleep_hours=wellness.sleep_hours,
        water_glasses=wellness.water_glasses,
        mood=wellness.mood
    )

    db.add(new_log)
    db.commit()

    return {
        "message": "Wellness Log Saved"
    }


@app.get("/wellness")
def get_wellness():
    db = SessionLocal()

    logs = db.query(
        models.WellnessLog
    ).all()

    return logs

@app.post("/wellness")
def save_wellness(
    wellness: schemas.WellnessCreate
):
    db = SessionLocal()

    new_record = models.Wellness(
        email=wellness.email,
        mood=wellness.mood,
        sleep_hours=wellness.sleep_hours,
        stress_level=wellness.stress_level
    )

    db.add(new_record)
    db.commit()

    return {
        "message": "Wellness Saved Successfully"
    }
