from sqlalchemy import Column, String
from backend.app.db.database import Base


class UserDB(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, index=True)
    role = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
