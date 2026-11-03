import os
import uuid

import aiofiles
from fastapi import HTTPException, UploadFile, status
from app.core.config import settings

UPLOAD_DIR = settings.COMPLAINT_UPLOAD_DIR
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = settings.MAX_FILE_SIZE


async def upload_image(file: UploadFile , upload_dir: str):
    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPG, JPEG and PNG images are allowed",
        )

    os.makedirs(upload_dir, exist_ok=True)

    filename = f"{uuid.uuid4().hex}{extension}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    file_size = 0

    async with aiofiles.open(file_path, "wb") as image:
        while chunk := await file.read(1024 * 1024):
            file_size += len(chunk)

            if file_size > MAX_FILE_SIZE:
                await image.close()
                os.remove(file_path)

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Image size must not exceed 5 MB",
                )

            await image.write(chunk)

    return file_path
