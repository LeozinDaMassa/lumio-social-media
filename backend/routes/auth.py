from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.supabase import supabase

router = APIRouter()

class RegisterData(BaseModel):
    email: str
    password: str
    username: str

class LoginData(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(data: RegisterData):
    try:
        response = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password,
            "options": {
                "data": {
                    "username": data.username
                }
            }
        })
        return {"message": "User created successfully", "user": response.user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(data: LoginData):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": data.email,
            "password": data.password
        })
        return {"token": response.session.access_token, "user": response.user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))