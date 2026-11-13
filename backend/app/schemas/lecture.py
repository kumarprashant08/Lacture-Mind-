# backend/app/schemas/lecture.py
"""Pydantic schemas for Lecture model."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

class LectureStatus(str, Enum):
    UPLOADED = "UPLOADED"
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class LectureBase(BaseModel):
    title: str = Field(..., max_length=200)

class LectureCreate(LectureBase):
    # The file will be sent as multipart, not represented here
    pass

class LectureResponse(LectureBase):
    id: int
    user_id: int
    original_filename: str
    stored_filename: str
    file_path: str
    file_type: str
    file_size: int
    status: LectureStatus
    created_at: datetime

    class Config:
        orm_mode = True

class LectureListResponse(BaseModel):
    lectures: list[LectureResponse]
