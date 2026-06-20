from fastapi import APIRouter, HTTPException, Depends, Query
from core.supabase import supabase
from middleware.auth import get_current_user

router = APIRouter()

@router.get("/")
def get_feed(
    user=Depends(get_current_user),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, le=50)
):
    try:
        follows = supabase.table("follows").select("following_id").eq("follower_id", user.id).execute()
        following_ids = [f["following_id"] for f in follows.data]
        following_ids.append(user.id)

        offset = (page - 1) * limit

        result = supabase.table("posts").select(
            "*, profiles(username, avatar_url), likes(user_id), comments(id)"
        ).in_("user_id", following_ids).order(
            "created_at", desc=True
        ).range(offset, offset + limit - 1).execute()

        posts = []
        for post in result.data:
            like_list = post.pop("likes", [])
            comment_list = post.pop("comments", [])
            post["like_count"] = len(like_list)
            post["comment_count"] = len(comment_list)
            post["liked_by_me"] = any(l["user_id"] == user.id for l in like_list)
            posts.append(post)

        return {
            "posts": posts,
            "page": page,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))