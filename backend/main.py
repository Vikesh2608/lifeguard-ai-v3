from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException

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

    # Email does not exist
    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="Email not found"
        )

    # Wrong password
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
# HEALTH SCORE
# ==========================

@app.get("/health-score/{email}")
def get_health_score(email: str):

    db = SessionLocal()

    records = (
        db.query(models.Wellness)
        .filter(models.Wellness.email == email)
        .all()
    )

    if not records:
        return {
            "overall_score": 0,
            "sleep_score": 0,
            "stress_score": 0,
            "mood_score": 0,
            "message": "No wellness records found"
        }

    latest = records[-1]

    # Sleep Score
    sleep_score = min(
        (latest.sleep_hours / 8) * 100,
        100
    )

    # Stress Score
    stress_score = max(
        100 - (latest.stress_level * 10),
        0
    )

    # Mood Score
    mood = latest.mood.lower()

    if mood == "happy":
        mood_score = 100
    elif mood == "good":
        mood_score = 90
    elif mood == "okay":
        mood_score = 70
    elif mood == "sad":
        mood_score = 40
    else:
        mood_score = 60

    overall_score = round(
        (sleep_score + stress_score + mood_score) / 3
    )

    return {
        "overall_score": overall_score,
        "sleep_score": round(sleep_score),
        "stress_score": round(stress_score),
        "mood_score": round(mood_score)
    }

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

# ==========================
# ADD FAMILY MEMBER
# ==========================

@app.post("/family")
def add_family_member(member: schemas.FamilyMemberCreate):

    db = SessionLocal()

    new_member = models.FamilyMember(
        owner_email=member.owner_email,
        first_name=member.first_name,
        last_name=member.last_name,
        relationship=member.relationship,
        phone=member.phone,
        email=member.email,
        medical_notes=member.medical_notes,
    )

    db.add(new_member)
    db.commit()

    return {
        "message": "Family member added successfully"
    }


# ==========================
# GET FAMILY MEMBERS
# ==========================

@app.get("/family/{email}")
def get_family(email: str):

    db = SessionLocal()

    members = (
        db.query(models.FamilyMember)
        .filter(models.FamilyMember.owner_email == email)
        .all()
    )

    return members
