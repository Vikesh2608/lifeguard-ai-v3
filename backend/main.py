from fastapi import FastAPI

from database import SessionLocal
from database import engine

import models
import schemas

app = FastAPI(
    title="LifeGuard AI"
)

models.Base.metadata.create_all(
    bind=engine
)


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

    new_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=user.password
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
            models.User.email == user.email,
            models.User.password == user.password
        )
        .first()
    )

    if existing_user:
        return {
            "message": "Login Successful"
        }

    return {
        "message": "Invalid Credentials"
    }
