# Generated main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine
import models, schemas
from auth import hash_password, verify_password
from ai_assistant import ask_lifeguard_ai

app=FastAPI(title="LifeGuard AI",version="4.0")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def home(): return {"message":"LifeGuard AI v4 Running Successfully"}

@app.get("/debug")
def debug(): return {"version":"v4","status":"Backend Running"}

@app.get("/vikesh-test")
def test(): return {"status":"SUCCESS","message":"Backend Connected"}

@app.post("/register")
def register_user(user:schemas.UserCreate):
    db=SessionLocal()
    try:
        if db.query(models.User).filter(models.User.email==user.email).first():
            raise HTTPException(status_code=400,detail="Email already registered")
        db.add(models.User(first_name=user.first_name,last_name=user.last_name,email=user.email,password=hash_password(user.password)))
        db.commit()
        return {"message":"User Registered Successfully"}
    finally: db.close()

@app.post("/login")
def login_user(user:schemas.UserLogin):
    db=SessionLocal()
    try:
        u=db.query(models.User).filter(models.User.email==user.email).first()
        if not u: raise HTTPException(status_code=404,detail="Email not found")
        if not verify_password(user.password,u.password): raise HTTPException(status_code=401,detail="Incorrect password")
        return {"message":"Login Successful","user":{"id":u.id,"first_name":u.first_name,"last_name":u.last_name,"email":u.email}}
    finally: db.close()

@app.post("/ai-chat")
def ai(req:schemas.AIRequest): return {"response":ask_lifeguard_ai(req.message)}

@app.post("/wellness")
def wellness(data:schemas.WellnessCreate):
    db=SessionLocal()
    try:
        db.add(models.Wellness(email=data.email,mood=data.mood,sleep_hours=data.sleep_hours,stress_level=data.stress_level))
        db.commit()
        return {"message":"Wellness record saved successfully"}
    finally: db.close()

@app.get("/wellness/{email}")
def wellness_history(email:str):
    db=SessionLocal()
    try: return db.query(models.Wellness).filter(models.Wellness.email==email).order_by(models.Wellness.created_at.desc()).all()
    finally: db.close()

@app.get("/health-score/{email}")
def health(email:str):
    db=SessionLocal()
    try:
        rows=db.query(models.Wellness).filter(models.Wellness.email==email).all()
        if not rows: return {"health_score":0,"message":"No wellness records found."}
        r=rows[-1]; score=max(0,min(100,100-r.stress_level*5-max(0,7-r.sleep_hours)*5))
        return {"health_score":score,"mood":r.mood,"sleep_hours":r.sleep_hours,"stress_level":r.stress_level}
    finally: db.close()

@app.post("/family")
def add(member:schemas.FamilyMemberCreate):
    db=SessionLocal()
    try:
        obj=models.FamilyMember(**member.model_dump())
        db.add(obj); db.commit(); db.refresh(obj)
        return {"message":"Family member added successfully","id":obj.id}
    finally: db.close()

@app.get("/family/{email}")
def getfam(email:str):
    db=SessionLocal()
    try: return db.query(models.FamilyMember).filter(models.FamilyMember.owner_email==email).all()
    finally: db.close()

@app.put("/family/{member_id}")
def update(member_id:int, member:schemas.FamilyMemberCreate):
    db=SessionLocal()
    try:
        obj=db.query(models.FamilyMember).filter(models.FamilyMember.id==member_id).first()
        if not obj: raise HTTPException(status_code=404,detail="Family member not found")
        for k,v in member.model_dump().items(): setattr(obj,k,v)
        db.commit()
        return {"message":"Family member updated successfully"}
    finally: db.close()

@app.delete("/family/{member_id}")
def delete(member_id:int):
    db=SessionLocal()
    try:
        obj=db.query(models.FamilyMember).filter(models.FamilyMember.id==member_id).first()
        if not obj: raise HTTPException(status_code=404,detail="Family member not found")
        db.delete(obj); db.commit()
        return {"message":"Family member deleted successfully"}
    finally: db.close()
