from fastapi import APIRouter, HTTPException, Depends
from core.supabase import supabase
from middleware.auth import get_current_user
from pydantic import BaseModel

router = APIRouter()

@router.get("/{user_id}")
def get_profile(user_id: str):
    try:
        result = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
        return {"profile": result.data}
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found")

@router.post("/{user_id}/follow")
def follow_user(user_id: str, user=Depends(get_current_user)):
    try:
        supabase.table("follows").insert({
            "follower_id": user.id,
            "following_id": user_id
        }).execute()
        return {"message": "User followed"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}/follow")
def unfollow_user(user_id: str, user=Depends(get_current_user)):
    try:
        supabase.table("follows").delete().match({
            "follower_id": user.id,
            "following_id": user_id
        }).execute()
        return {"message": "User unfollowed"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}/followers")
def get_followers(user_id: str):
    try:
        result = supabase.table("follows").select("follower_id, profiles!follows_follower_id_fkey(username, avatar_url)").eq("following_id", user_id).execute()
        return {"followers": result.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}/following")
def get_following(user_id: str):
    try:
        result = supabase.table("follows").select("following_id, profiles!follows_following_id_fkey(username, avatar_url)").eq("follower_id", user_id).execute()
        return {"following": result.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class ProfileUpdate(BaseModel):
    username: str = None
    bio: str = None
    avatar_url: str = None

@router.patch("/me")
def update_profile(data: ProfileUpdate, user=Depends(get_current_user)):
    try:
        updates = {k: v for k, v in data.dict().items() if v is not None}
        result = supabase.table("profiles").update(updates).eq("id", user.id).execute()
        return {"profile": result.data[0]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))