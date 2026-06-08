from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from core.supabase import supabase
from middleware.auth import get_current_user
import uuid

router = APIRouter()

ALLOWED_TYPES = {
    # Images
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
    # Videos
    "video/mp4",
    "video/quicktime",  # .mov
    "video/webm",
}

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

@router.post("/upload")
async def upload_media(
    file: UploadFile = File(...),
    user=Depends(get_current_user)
):
    try:
        # Validate file type
        if file.content_type not in ALLOWED_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file.content_type} not allowed"
            )

        # Read and validate file size
        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="File too large. Maximum size is 50MB"
            )

        # Generate unique filename
        extension = file.filename.split(".")[-1]
        filename = f"{user.id}/{uuid.uuid4()}.{extension}"

        # Upload to Supabase Storage
        supabase.storage.from_("media").upload(
            path=filename,
            file=content,
            file_options={"content-type": file.content_type}
        )

        # Get public URL
        url = supabase.storage.from_("media").get_public_url(filename)

        return {
            "url": url,
            "media_type": "video" if file.content_type.startswith("video") else "image"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))