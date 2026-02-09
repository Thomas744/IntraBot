from pydantic import BaseModel

class User(BaseModel):
    username: str
    role: str
    hashed_password: str
