from fastapi import FastAPI
from app.api import user_controller, auth_controller
from app.exceptions.global_exception import register_exceptions
from app.db.database import Base, engine
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address


logging.basicConfig(
    level=logging.INFO,   # or INFO
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create rate limiter
limiter = Limiter(key_func=get_remote_address)

# ✅ THIS CREATES TABLES Automatically
Base.metadata.create_all(bind=engine)

#Spring Boot equivalent: @SpringBootApplication

app = FastAPI(title="User Service")

# Register routes
app.include_router(user_controller.router)
app.include_router(auth_controller.router)

# Register global exception
register_exceptions(app)

@app.get("/")
def health():
    return {"App":"UP", "status": "User Service Running"}