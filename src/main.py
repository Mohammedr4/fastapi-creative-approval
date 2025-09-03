from fastapi import FastAPI, UploadFile, File, HTTPException, status
from collections import defaultdict
from .models import ApprovalResponse, ImageInfo, ApprovalStatus
from .rules import check_creative_rules
from PIL import Image
import io

# keep counts of decisions
decision_count = defaultdict(int)

app = FastAPI(
    title="Creative Approval API",
    version="1.0.0",
    description="Checks simple ad rules on uploaded images"
)

@app.post("/creative-approval", response_model=ApprovalResponse)
async def upload_creative(file: UploadFile = File(...)):
    if not file or not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file uploaded"
        )

    img_bytes = await file.read()
    result, reasons = check_creative_rules(img_bytes)
    decision_count[result.value] += 1

    info = None
    try:
        img = Image.open(io.BytesIO(img_bytes))
        w, h = img.size
        info = ImageInfo(
            format=img.format or "unknown",
            width=w,
            height=h,
            size_bytes=len(img_bytes)
        )
    except Exception:
        # just skip image info if something breaks
        pass

    return ApprovalResponse(
        status=result,
        reasons=reasons,
        image_info=info
    )

@app.get("/metrics")
def get_metrics():
    return dict(decision_count)

@app.get("/health")
def health_check():
    return {"status": "healthy"}
