from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from database import SessionLocal, engine
import models
import schemas

from auth import hash_password, verify_password
from ai_assistant import ask_lifeguard_ai

app = FastAPI(
    title="LifeGuard AI",
    version="4.0"
)

# ==========================
# CORS
# ==========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# DATABASE
# ==========================

models.Base.metadata.create_all(bind=engine)

# ==========================
# HOME
# ==========================

@app.get("/")
def home():
    return {
        "message": "LifeGuard AI v4 Running Successfully"
    }


@app.get("/debug")
def debug():
    return {
        "version": "v4",
        "status": "Backend Running"
    }


@app.get("/vikesh-test")
def test():
    return {
        "status": "SUCCESS",
        "message": "Backend Connected"
    }


# ==========================
# USER REGISTRATION
# ==========================

@app.post("/register")
def register_user(user: schemas.UserCreate):

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


# ==========================
# LOGIN
# ==========================

@app.post("/login")
def login_user(user: schemas.UserLogin):

    db = SessionLocal()

    existing_user = (
        db.query(models.User)
        .filter(models.User.email == user.email)
        .first()
    )

    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="Email not found"
        )

    if not verify_password(
        user.password,
        existing_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )

    return {
        "message": "Login Successful",
        "user": {
            "first_name": existing_user.first_name,
            "last_name": existing_user.last_name,
            "email": existing_user.email
        }
    }

