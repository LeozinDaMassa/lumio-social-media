from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from core.supabase import supabase
from middleware.auth import get_current_user

router = APIRouter()

class PostData(BaseModel):
    content: str
    media_url: str = None
    media_type: str = None

@router.post("/")
def create_post(data: PostData, user=Depends(get_current_user)):
    try:
        result = supabase.table("posts").insert({
            "user_id": user.id,
            "content": data.content,
            "media_url": data.media_url,
            "media_type": data.media_type
        }).execute()
        return {"message": "Post created", "post": result.data[0]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def get_posts():
    try:
        result = supabase.table("posts").select("*, profiles(username, avatar_url)").order("created_at", desc=True).execute()
        return {"posts": result.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))