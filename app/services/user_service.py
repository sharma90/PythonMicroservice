from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserRequest
from sqlalchemy.orm import Session
from app.models.user_model import User
import requests
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed
import logging
from cachetools import cached, TTLCache

# cache
cache = TTLCache(maxsize=100, ttl=60)

logger = logging.getLogger(__name__)
#Equivalent to @Service

class UserService:

    def __init__(self):
        self.repo = UserRepository()

    def create_user(self, db: Session, request: UserRequest):
        user = User(name=request.name)
        return self.repo.save(db, user)
    
    def update_user(self, db: Session, user:User):
        print("inside service update check changes argocd")
        #user = User(name=request.name)
        return self.repo.save(db, user)
    
    def delete_user(self, db: Session, user:User):
        print("delete record")
        logger.info("Record deleted in delete_user:",user.id,user.name)
        #user = User(name=request.name)
        return self.repo.deleteUser(db, user)

    # 🔁 Retry (like @Retryable)
    @cached(cache, key=lambda self, db, user_id: user_id)
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def get_user(self, db: Session, user_id: int):
        #print("counting")
        #requests.get("http://localhost:8082/fetchUserById/1")

        user = self.repo.find_by_id(db, user_id)
        if not user:
            logger.error("User not found")
            raise Exception("User not found")
        return user
    
    def getAllUsers(self, db: Session):
        try:
            #raise Exception
            user = self.repo.find_All(db)
        except ValueError as e:
            raise Exception("Exception occured")
    
        if not user:
            raise Exception("User not found")
        return user
    

    