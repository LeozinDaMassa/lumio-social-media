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
        # Get list of users the current user follows
        follows = supabase.table("follows").select("following_id").eq("follower_id", user.id).execute()
        following_ids = [f["following_id"] for f in follows.data]

        # Include the user's own posts in their feed
        following_ids.append(user.id)

        # Calculate pagination offset
        offset = (page - 1) * limit

        # Fetch posts from followed users
        result = supabase.table("posts").select(
            "*, profiles(username, avatar_url)"
        ).in_("user_id", following_ids).order(
            "created_at", desc=True
        ).range(offset, offset + limit - 1).execute()

        return {
            "posts": result.data,
            "page": page,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))