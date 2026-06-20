from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from middleware.auth import get_current_user, get_token
from core.supabase import supabase, get_authed_client

router = APIRouter()

class PostData(BaseModel):
    content: str
    media_url: Optional[str] = None
    media_type: Optional[str] = None

@router.post("/")
def create_post(data: PostData, user=Depends(get_current_user), token: str = Depends(get_token)):
    try:
        client = get_authed_client(token)
        result = client.table("posts").insert({
            "user_id": user.id,
            "content": data.content,
            "media_url": data.media_url,
            "media_type": data.media_type
        }).execute()

        post_id = result.data[0]["id"]
        full_post = client.table("posts").select("*, profiles(username, avatar_url)").eq("id", post_id).single().execute()

        return {"message": "Post created", "post": full_post.data}
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
def like_post(post_id: str, user=Depends(get_current_user), token: str = Depends(get_token)):
    try:
        client = get_authed_client(token)
        client.table("likes").insert({
            "user_id": user.id,
            "post_id": post_id
        }).execute()
        return {"message": "Post liked"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{post_id}/like")
def unlike_post(post_id: str, user=Depends(get_current_user), token: str = Depends(get_token)):
    try:
        client = get_authed_client(token)
        client.table("likes").delete().match({
            "user_id": user.id,
            "post_id": post_id
        }).execute()
        return {"message": "Post unliked"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class CommentData(BaseModel):
    content: str

@router.post("/{post_id}/comment")
def add_comment(post_id: str, data: CommentData, user=Depends(get_current_user), token: str = Depends(get_token)):
    try:
        client = get_authed_client(token)
        result = client.table("comments").insert({
            "user_id": user.id,
            "post_id": post_id,
            "content": data.content
        }).execute()

        comment_id = result.data[0]["id"]
        full_comment = client.table("comments").select("*, profiles(username, avatar_url)").eq("id", comment_id).single().execute()

        return {"message": "Comment added", "comment": full_comment.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{post_id}/comments")
def get_comments(post_id: str):
    try:
        result = supabase.table("comments").select("*, profiles(username, avatar_url)").eq("post_id", post_id).order("created_at").execute()
        return {"comments": result.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/{post_id}")
def delete_post(post_id: str, user=Depends(get_current_user), token: str = Depends(get_token)):
    try:
        client = get_authed_client(token)
        post = client.table("posts").select("user_id").eq("id", post_id).single().execute()
        
        if post.data["user_id"] != user.id:
            raise HTTPException(status_code=403, detail="You can only delete your own posts")
        
        client.table("posts").delete().eq("id", post_id).execute()
        return {"message": "Post deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))