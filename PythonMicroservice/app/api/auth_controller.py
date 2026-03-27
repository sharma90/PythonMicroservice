# JWT Authentication
# endpoint to generate jwt token which you can use to call user controller endpoints
from fastapi import APIRouter
from app.security.jwt_handler import create_access_token

router = APIRouter(prefix="/auth")

@router.post("/login")
def login():
    # validate user from DB (skip for now)
    token = create_access_token({"sub": "admin"})
    return {"access_token": token, "token_type": "bearer"}