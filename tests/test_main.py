import pytest
from fastapi.testclient import TestClient
from src.main import app
from PIL import Image
import io

client = TestClient(app)

# helper to generate tiny images
def make_img(w=100, h=100, color=128):
    img = Image.new("RGB", (w, h), (color, color, color))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_health_endpoint():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


def test_creative_happy_path():
    img_bytes = make_img()
    files = {"file": ("good.png", img_bytes, "image/png")}
    r = client.post("/creative-approval", files=files)
    assert r.status_code == 200
    body = r.json()
    assert body["status"] in ["APPROVED", "REQUIRES_REVIEW"]


def test_creative_reject_invalid_file():
    files = {"file": ("bad.png", b"notanimage", "image/png")}
    r = client.post("/creative-approval", files=files)
    assert r.status_code == 200
    assert r.json()["status"] == "REJECTED"


def test_creative_missing_file():
    # simulate user sending no file
    r = client.post("/creative-approval", files={})
    assert r.status_code == 422
