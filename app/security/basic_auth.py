# Token creation logic
# Basic Authentication
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

def basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    if not (
        secrets.compare_digest(credentials.username, "admin") and
        secrets.compare_digest(credentials.password, "password")
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return credentials.username