from sqlalchemy.orm import Session
from app.models.user_model import User
class UserRepository:

#Equivalent to JpaRepository

    def save(self,db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def find_by_id(self,db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()
    
    def find_All(self,db: Session):
        return db.query(User).all()
    
    def deleteUser(self,db: Session,user:User):
         db.delete(user);
         db.commit()
         return {"message": "User deleted successfully"};