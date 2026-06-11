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
