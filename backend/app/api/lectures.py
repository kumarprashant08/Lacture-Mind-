# backend/app/api/lectures.py
"""Lecture upload and CRUD endpoints.

All routes are JWT protected via ``get_current_user``. The ``upload`` route
accepts multipart ``UploadFile`` objects, validates MIME type, extension and
size, stores the file using the ``storage`` abstraction, and creates a DB record
with status ``UPLOADED``.
"""

import uuid
import os
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.config import settings
from ..services.storage import storage
from ..models import Lecture, User
from ..schemas.lecture import LectureCreate, LectureResponse, LectureListResponse
from .auth import get_current_user

router = APIRouter()

# Allowed MIME types and corresponding extensions
ALLOWED_TYPES = {
    "audio/mpeg": ".mp3",
    "audio/wav": ".wav",
    "audio/x-wav": ".wav",
    "audio/mp4": ".m4a",
    "video/mp4": ".mp4",
    "video/quicktime": ".mov",
    "video/webm": ".webm",
}

def _validate_file(upload: UploadFile):
    if upload.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type.",
        )
    # Size validation – fastapi's UploadFile streams; we need to read size.
    # We'll trust the client header ``Content-Length``. For safety we can read
    # the file into memory if it's small; otherwise, reject large files.
    # ``upload.file`` is a SpooledTemporaryFile; we can seek to end.
    upload.file.seek(0, os.SEEK_END)
    size = upload.file.tell()
    upload.file.seek(0)
    if size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File exceeds the maximum allowed size.",
        )
    return size

@router.post("/upload", response_model=LectureResponse)
async def upload_lecture(
    title: str = "",
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Validate file type and size
    file_size = _validate_file(file)

    # Determine extension (fallback to original filename if MIME not mapped)
    ext = ALLOWED_TYPES.get(file.content_type) or os.path.splitext(file.filename)[1]
    # Generate a secure random filename
    stored_name = f"{uuid.uuid4().hex}{ext}"
    # Build storage path relative to root – we store under uploads/
    storage_path = os.path.join("uploads", stored_name)

    # Save file using storage abstraction
    try:
        absolute_path = storage.save(file.file, storage_path)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to store uploaded file.",
        ) from e

    # Create DB record
    lecture = Lecture(
        user_id=current_user.id,
        title=title or os.path.splitext(file.filename)[0],
        original_filename=file.filename,
        stored_filename=stored_name,
        file_path=absolute_path,
        file_type=file.content_type,
        file_size=file_size,
        status="UPLOADED",
    )
    db.add(lecture)
    db.commit()
    db.refresh(lecture)
    return LectureResponse.from_orm(lecture)

@router.get("/", response_model=LectureListResponse)
def list_lectures(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    lectures = db.query(Lecture).filter(Lecture.user_id == current_user.id).order_by(Lecture.created_at.desc()).all()
    return LectureListResponse(lectures=[LectureResponse.from_orm(l) for l in lectures])

@router.get("/{lecture_id}", response_model=LectureResponse)
def get_lecture(lecture_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    lecture = db.query(Lecture).filter(Lecture.id == lecture_id, Lecture.user_id == current_user.id).first()
    if not lecture:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lecture not found")
    return LectureResponse.from_orm(lecture)

@router.delete("/{lecture_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lecture(lecture_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    lecture = db.query(Lecture).filter(Lecture.id == lecture_id, Lecture.user_id == current_user.id).first()
    if not lecture:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lecture not found")
    # Delete file from storage if it exists
    if storage.exists(os.path.relpath(lecture.file_path, start=settings.STORAGE_ROOT)):
        storage.delete(os.path.relpath(lecture.file_path, start=settings.STORAGE_ROOT))
    db.delete(lecture)
    db.commit()
    return None
