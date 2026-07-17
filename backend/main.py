from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from database import SessionLocal, engine
import models
import schemas

from auth import hash_password, verify_password
from ai_assistant import ask_lifeguard_ai

# ==========================================
# APP
# ==========================================

app = FastAPI(
    title="LifeGuard AI",
    version="4.0"
)

# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# DATABASE
# ==========================================

models.Base.metadata.create_all(bind=engine)

# ==========================================
# HOME
# ==========================================

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


# ==========================================
# REGISTER
# ==========================================

@app.post("/register")
def register_user(user: schemas.UserCreate):

    db = SessionLocal()

    try:

        existing_user = (
            db.query(models.User)
            .filter(models.User.email == user.email)
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

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

    finally:
        db.close()


# ==========================================
# LOGIN
# ==========================================

@app.post("/login")
def login_user(user: schemas.UserLogin):

    db = SessionLocal()

    try:

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
                "id": existing_user.id,
                "first_name": existing_user.first_name,
                "last_name": existing_user.last_name,
                "email": existing_user.email
            }
        }

    finally:
        db.close()

# ==========================================
# AI ASSISTANT
# ==========================================

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

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==========================================
# WELLNESS CHECK-IN
# ==========================================

@app.post("/wellness")
def save_wellness(data: schemas.WellnessCreate):

    db = SessionLocal()

    try:

        record = models.Wellness(
            email=data.email,
            mood=data.mood,
            sleep_hours=data.sleep_hours,
            stress_level=data.stress_level
        )

        db.add(record)
        db.commit()

        return {
            "message": "Wellness record saved successfully"
        }

    finally:
        db.close()


# ==========================================
# WELLNESS HISTORY
# ==========================================

@app.get("/wellness/{email}")
def get_wellness(email: str):

    db = SessionLocal()

    try:

        records = (
            db.query(models.Wellness)
            .filter(models.Wellness.email == email)
            .order_by(models.Wellness.created_at.desc())
            .all()
        )

        return records

    finally:
        db.close()


# ==========================================
# HEALTH SCORE
# ==========================================

@app.get("/health-score/{email}")
def calculate_health_score(email: str):

    db = SessionLocal()

    try:

        records = (
            db.query(models.Wellness)
            .filter(models.Wellness.email == email)
            .all()
        )

        if not records:

            return {
                "health_score": 0,
                "message": "No wellness records found."
            }

        score = 100

        latest = records[-1]

        # Stress impact
        score -= latest.stress_level * 5

        # Sleep impact
        if latest.sleep_hours < 7:
            score -= (7 - latest.sleep_hours) * 5

        if score < 0:
            score = 0

        if score > 100:
            score = 100

        return {
            "health_score": score,
            "mood": latest.mood,
            "sleep_hours": latest.sleep_hours,
            "stress_level": latest.stress_level
        }

    finally:
        db.close()

# ==========================================
# FAMILY - ADD MEMBER
# ==========================================

@app.post("/family")
def add_family_member(member: schemas.FamilyMemberCreate):

    db = SessionLocal()

    try:

        new_member = models.FamilyMember(
            owner_email=member.owner_email,
            first_name=member.first_name,
            last_name=member.last_name,
            relationship=member.relationship,
            phone=member.phone,
            email=member.email,
            medical_notes=member.medical_notes,
            blood_group=member.blood_group,
            allergies=member.allergies,
            medications=member.medications,
            doctor=member.doctor,
            hospital=member.hospital
        )

        db.add(new_member)
        db.commit()
        db.refresh(new_member)

        return {
            "message": "Family member added successfully",
            "id": new_member.id
        }

    finally:
        db.close()


# ==========================================
# FAMILY - GET MEMBERS
# ==========================================

@app.get("/family/{email}")
def get_family_members(email: str):

    db = SessionLocal()

    try:

        members = (
            db.query(models.FamilyMember)
            .filter(models.FamilyMember.owner_email == email)
            .all()
        )

        return members

    finally:
        db.close()


# ==========================================
# FAMILY - UPDATE MEMBER
# ==========================================

@app.put("/family/{member_id}")
def update_family_member(
    member_id: int,
    member: schemas.FamilyMemberCreate
):

    db = SessionLocal()

    try:

        existing = (
            db.query(models.FamilyMember)
            .filter(models.FamilyMember.id == member_id)
            .first()
        )

        if not existing:
            raise HTTPException(
                status_code=404,
                detail="Family member not found"
            )

        existing.owner_email = member.owner_email
        existing.first_name = member.first_name
        existing.last_name = member.last_name
        existing.relationship = member.relationship
        existing.phone = member.phone
        existing.email = member.email
        existing.medical_notes = member.medical_notes
        existing.blood_group = member.blood_group
        existing.allergies = member.allergies
        existing.medications = member.medications
        existing.doctor = member.doctor
        existing.hospital = member.hospital

        db.commit()
        db.refresh(existing)

        return {
            "message": "Family member updated successfully"
        }

    finally:
        db.close()


# ==========================================
# FAMILY - DELETE MEMBER
# ==========================================

@app.delete("/family/{member_id}")
def delete_family_member(member_id: int):

    db = SessionLocal()

    try:

        existing = (
            db.query(models.FamilyMember)
            .filter(models.FamilyMember.id == member_id)
            .first()
        )

        if not existing:
            raise HTTPException(
                status_code=404,
                detail="Family member not found"
            )

        db.delete(existing)
        db.commit()

        return {
            "message": "Family member deleted successfully"
        }

    finally:
        db.close()
