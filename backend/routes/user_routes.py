from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from backend.auth.dependencies import get_current_user
from backend.db.user_repository import (
    get_all_users,
    create_user,
    delete_user,
)

router = APIRouter(prefix="/users", tags=["User Management"])


class CreateUserRequest(BaseModel):
    username: str
    role: str
    password: str


@router.get("/")
def list_users(user=Depends(get_current_user)):
    if user.role != "c_level":
        raise HTTPException(status_code=403, detail="Access denied")

    return get_all_users()


@router.post("/")
def add_user(request: CreateUserRequest, user=Depends(get_current_user)):
    if user.role != "c_level":
        raise HTTPException(status_code=403, detail="Access denied")

    new_user = create_user(
        request.username,
        request.role,
        request.password,
    )

    if not new_user:
        raise HTTPException(status_code=400, detail="User already exists")

    return new_user


@router.delete("/{username}")
def remove_user(username: str, user=Depends(get_current_user)):
    if user.role != "c_level":
        raise HTTPException(status_code=403, detail="Access denied")

    success = delete_user(username)

    if not success:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}
