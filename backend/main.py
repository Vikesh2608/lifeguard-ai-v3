from fastapi import FastAPI

app = FastAPI(title="LifeGuard AI")

@app.get("/")
def home():
    return {"message": "LifeGuard AI v3 Running Successfully"}

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
