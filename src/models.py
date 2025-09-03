from pydantic import BaseModel
from enum import Enum

class ApprovalStatus(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REQUIRES_REVIEW = "REQUIRES_REVIEW"

class ImageInfo(BaseModel):
    format: str
    width: int
    height: int
    size_bytes: int

class ApprovalResponse(BaseModel):
    status: ApprovalStatus
    reasons: list[str]
    image_info: ImageInfo | None = None
