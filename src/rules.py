from .models import ApprovalStatus
from PIL import Image
import io
import numpy as np

MAX_FILE_MB = 10
MAX_FILE_BYTES = MAX_FILE_MB * 1024 * 1024

PREFERRED_RATIO = 16 / 9
RATIO_TOLERANCE = 0.1

MIN_CONTRAST = 15  # approximate std-dev threshold

def check_creative_rules(data: bytes) -> tuple[ApprovalStatus, list[str]]:
    reasons: list[str] = []
    status = ApprovalStatus.APPROVED

    if len(data) > MAX_FILE_BYTES:
        return ApprovalStatus.REJECTED, [f"File too big ({len(data)/1024/1024:.2f}MB), limit {MAX_FILE_MB}MB"]

    try:
        img = Image.open(io.BytesIO(data))
        img.verify()  # quick check
        img = Image.open(io.BytesIO(data))  # reopen for size
        w, h = img.size
    except Exception:
        return ApprovalStatus.REJECTED, ["Bad or invalid image"]

    # aspect ratio
    if h == 0:
        return ApprovalStatus.REJECTED, ["Height is zero"]
    ratio = w / h
    if abs(ratio - PREFERRED_RATIO) > RATIO_TOLERANCE:
        reasons.append(f"Aspect ratio {ratio:.2f} not close to {PREFERRED_RATIO:.2f}")
        status = ApprovalStatus.REQUIRES_REVIEW

    # low contrast check
    gray = img.convert("L")
    contrast_val = float(np.std(np.array(gray)))
    if contrast_val < MIN_CONTRAST:
        reasons.append(f"Low contrast ({contrast_val:.2f})")
        status = ApprovalStatus.REQUIRES_REVIEW

    if not reasons:
        reasons.append("All checks passed")

    return status, reasons
