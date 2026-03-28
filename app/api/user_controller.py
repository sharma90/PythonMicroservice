from fastapi import APIRouter, Depends, Request
from app.services.user_service import UserService
from app.schemas.user_schema import UserRequest, UserResponse,ApiResponse,MessageResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.security.basic_auth import basic_auth
from app.security.dependencies import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address
import pybreaker


#Equivalent to @RestController

router = APIRouter(prefix="/users", tags=["Users"])

# For Rate limit
limiter = Limiter(key_func=get_remote_address)

# For Circuit Breaker
#   After 3 retry failed --> OPEN  --(30 sec)-->  HALF-OPEN  --(success)--> CLOSED
breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=30)

def get_user_service():
    return UserService()

@router.post("/", response_model=UserResponse)
def create_user(
    request: UserRequest,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    return service.create_user(db, request)

@router.put("/update/{userId}", response_model=UserResponse)
def create_user(
    userId: int,
    request: UserRequest,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    user = service.get_user(db, userId)
    print("Updatingggg",user.id,user.name)
    user.name=request.name
    
    return service.update_user(db,user)


@router.get("/userList", response_model=list[UserResponse])
@limiter.limit("2/minute")
def get_user_list(request:Request,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
    user: str = Depends(get_current_user)
):
    return service.getAllUsers(db)


@router.delete("/{userId}", response_model=MessageResponse)
def get_user_list(
    userId: int,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service)
):
    user = service.get_user(db, userId)
    print("Enter delete ",user.id,user.name)
    return service.delete_user(db,user)



@router.get("/{user_id}", response_model=ApiResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    service: UserService = Depends(get_user_service),
    user: str = Depends(basic_auth)
):
    try:
        print("Enter get_user method")
        print("Enter get_user method again change done")
        print("Enter get_user method again change done2222")
        user_data = breaker.call(service.get_user,db, user_id)
        return ApiResponse(success=True, data=user_data)
    except pybreaker.CircuitBreakerError as e:
        return CircuitBreakerfallback(e)
    except Exception as e:
        return fallback(e)
    

# 🔁 Fallback method
def fallback(e):
    print("Fallback triggered:", e)
    return ApiResponse(
            success=False,
            message="Something went wrong:Retry Attempt failed",
            errorCode="500",
            errorDescription="Something went wrong: Retry Attempt failed"
        ) 

# 🔁 Fallback method
def CircuitBreakerfallback(e):
    print("Fallback triggered:", e)
    return ApiResponse(
            success=False,
            message="Circuit open fallback",
            errorCode="500",
            errorDescription="Circuit open fallback"
        )

