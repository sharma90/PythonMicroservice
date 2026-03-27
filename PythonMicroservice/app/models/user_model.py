from sqlalchemy import Column, Integer, String
from app.db.database import Base

# Equivalent to @Entity

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)