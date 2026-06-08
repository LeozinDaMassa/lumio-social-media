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

@router.post("/{post_id}/like")
def like_post(post_id: str, user=Depends(get_current_user)):
    try:
        result = supabase.table("likes").insert({
            "user_id": user.id,
            "post_id": post_id
        }).execute()
        return {"message": "Post liked"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{post_id}/like")
def unlike_post(post_id: str, user=Depends(get_current_user)):
    try:
        supabase.table("likes").delete().match({
            "user_id": user.id,
            "post_id": post_id
        }).execute()
        return {"message": "Post unliked"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class CommentData(BaseModel):
    content: str

@router.post("/{post_id}/comment")
def add_comment(post_id: str, data: CommentData, user=Depends(get_current_user)):
    try:
        result = supabase.table("comments").insert({
            "user_id": user.id,
            "post_id": post_id,
            "content": data.content
        }).execute()
        return {"message": "Comment added", "comment": result.data[0]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{post_id}/comments")
def get_comments(post_id: str):
    try:
        result = supabase.table("comments").select("*, profiles(username, avatar_url)").eq("post_id", post_id).order("created_at").execute()
        return {"comments": result.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))