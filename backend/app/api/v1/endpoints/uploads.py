import os
import shutil
import uuid

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import aiofiles

from app.core.config import settings
from app.core.dependencies import get_current_user, get_db
from app.repositories.upload_repo import UploadRepository
from app.models.upload import Upload
from app.workers.file_tasks import process_upload

router = APIRouter()


@router.post("/uploads")
async def create_upload(file: UploadFile = File(...), db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    # Ensure storage dir
    storage_dir = settings.storage_local_path
    os.makedirs(storage_dir, exist_ok=True)
    # generate filename
    uid = uuid.uuid4()
    filename = f"{uid.hex}_{file.filename}"
    dest_path = os.path.join(storage_dir, filename)
    try:
        # stream to disk
        async with aiofiles.open(dest_path, "wb") as out_file:
            while True:
                chunk = await file.read(1024 * 64)
                if not chunk:
                    break
                await out_file.write(chunk)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to store file")

    # create DB record
    repo = UploadRepository(db)
    upload = await repo.create(
        {
            "user_id": user.id,
            "original_filename": file.filename,
            "file_type": file.content_type.split("/")[1] if "/" in file.content_type else file.content_type,
            "file_size_bytes": os.path.getsize(dest_path),
            "storage_path": dest_path,
            "mime_type": file.content_type,
            "processing_status": "pending",
        }
    )

    # enqueue Celery task
    try:
        process_upload.delay(str(upload.id), dest_path, file.filename)
    except Exception:
        # don't fail the request on task enqueue error; mark status
        await repo.update(upload.id, {"processing_status": "queued_error"})

    return {"id": str(upload.id), "status": "queued"}
