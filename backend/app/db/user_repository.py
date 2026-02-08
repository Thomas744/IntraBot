from backend.app.db.database import SessionLocal
from backend.app.db.models import UserDB
from backend.app.models.user import User


def get_user_by_username(username: str):
    db = SessionLocal()
    try:
        user = db.query(UserDB).filter(UserDB.username == username).first()
        if not user:
            return None

        return User(
            username=user.username,
            role=user.role,
            hashed_password=user.hashed_password,
        )
    finally:
        db.close()
