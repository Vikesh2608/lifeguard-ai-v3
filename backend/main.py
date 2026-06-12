from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import SessionLocal, engine
import models
import schemas

from auth import hash_password, verify_password
from ai_assistant import ask_lifeguard_ai

app = FastAPI(
    title="LifeGuard AI"
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

# ==========================
# WELLNESS SAVE
# ==========================

@app.post("/wellness")
def save_wellness(wellness: schemas.WellnessCreate):

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

# ==========================
# WELLNESS HISTORY
# ==========================

@app.get("/wellness-history/{email}")
def get_wellness_history(email: str):

    db = SessionLocal()

    records = (
        db.query(models.Wellness)
        .filter(models.Wellness.email == email)
        .all()
    )

    return records

# ==========================
# AI ASSISTANT
# ==========================

@app.post("/ai-chat")
def ai_chat(request: schemas.AIRequest):

    try:

        response = ask_lifeguard_ai(
            request.message
        )

        return {
            "response": response
        }

    except Exception as e:

        return {
            "response": f"❌ AI Error: {str(e)}"
        }
