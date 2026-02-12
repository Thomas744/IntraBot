from backend.db.database import SessionLocal
from backend.db.models import UserDB
from backend.models.user import User
from backend.auth.password_utils import hash_password

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

def get_all_users():
    db = SessionLocal()
    try:
        users = db.query(UserDB).all()
        return [
            {"username": u.username, "role": u.role}
            for u in users
        ]
    finally:
        db.close()


def create_user(username: str, role: str, password: str):
    db = SessionLocal()
    try:
        existing = db.query(UserDB).filter(UserDB.username == username).first()
        if existing:
            return None

        user = UserDB(
            username=username,
            role=role.lower(),
            hashed_password=hash_password(password),
        )

        db.add(user)
        db.commit()
        return {"username": username, "role": role.lower()}
    finally:
        db.close()


def delete_user(username: str):
    db = SessionLocal()
    try:
        user = db.query(UserDB).filter(UserDB.username == username).first()
        if not user:
            return False

        db.delete(user)
        db.commit()
        return True
    finally:
        db.close()
