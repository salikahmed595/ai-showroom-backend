from __future__ import annotations

# ─── ENV ─────────────────────────────────────────────────────────────
import os
from dotenv import load_dotenv

load_dotenv()
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN or ""

print("TOKEN loaded:", bool(REPLICATE_API_TOKEN))

# ─── IMPORTS ─────────────────────────────────────────────────────────
import uuid
import asyncio
import logging
import base64
from pathlib import Path
from typing import Optional

import replicate
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import aiofiles

# ─── LOGGING ─────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("vton")

# ─── CONFIG ──────────────────────────────────────────────────────────
UPLOAD_DIR = Path("uploads")
STATIC_DIR = Path("static")
UPLOAD_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)

# IDM-VTON on Replicate
MODEL_ID = "cuuupid/idm-vton:906425dbca90663ff5427624839572cc56ea7d380343d13e2a4c4b09d3f0c30f"

POSES = [
    {"key": "front", "label": "Front View", "garment_des": "A photorealistic front view of the garment fitted on the model", "seed": 42},
]

# ─── APP ─────────────────────────────────────────────────────────────
app = FastAPI(title="AI Digital Showroom")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── MODELS ──────────────────────────────────────────────────────────
class PoseResult(BaseModel):
    pose: str
    label: str
    status: str
    image_url: Optional[str] = None
    error: Optional[str] = None

# ─── HELPERS ─────────────────────────────────────────────────────────
ALLOWED_TYPES = {
    "image/jpeg", "image/jpg", "image/png", "image/webp",
    "image/jfif", "image/pjpeg", "image/x-jfif",
}

def detect_mime(data: bytes) -> str:
    """Detect image MIME type from magic bytes."""
    if data[:2] == b'\xff\xd8':
        return "image/jpeg"          # JPEG / JFIF
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        return "image/png"
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        return "image/webp"
    return "image/jpeg"              # safe default

def bytes_to_data_uri(data: bytes) -> str:
    """Encode image bytes as a base64 data URI (what Replicate expects)."""
    mime = detect_mime(data)
    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:{mime};base64,{b64}"

def extract_url(output) -> str:
    """
    Pull a plain URL string out of whatever replicate.run() returns.
    replicate SDK ≥1.0 wraps file outputs in FileOutput objects.
    """
    # List / tuple → take first element
    if isinstance(output, (list, tuple)):
        output = output[0]

    # replicate.helpers.FileOutput  →  has .url
    if hasattr(output, "url"):
        return str(output.url)

    # Already a string (URL)
    if isinstance(output, str):
        return output

    # Raw bytes → save locally, serve via /static
    if isinstance(output, bytes):
        fname = f"{uuid.uuid4().hex}.png"
        (STATIC_DIR / fname).write_bytes(output)
        return f"/static/{fname}"

    # Last resort
    return str(output)

async def validate_and_read(file: UploadFile) -> bytes:
    """Read upload, enforce size limit."""
    data = await file.read()
    if not data:
        raise HTTPException(400, "Empty file uploaded.")
    if len(data) > 15 * 1024 * 1024:
        raise HTTPException(400, "File too large — max 15 MB.")
    return data

def cleanup(path: Path):
    try:
        path.unlink(missing_ok=True)
    except Exception:
        pass

# ─── AI CALL ─────────────────────────────────────────────────────────
async def run_single_pose(
    job_id: str,
    pose: dict,
    model_uri: str,   # base64 data URI
    cloth_uri: str,   # base64 data URI
    loop,
) -> PoseResult:
    try:
        log.info(f"[{job_id}] starting pose={pose['key']}")

        client = replicate.Client(api_token=REPLICATE_API_TOKEN)

        # ── Run synchronously inside thread pool ──────────────────────
        # We pass data URIs (plain strings) so JSON serialization never
        # touches bytes → no "Object of type bytes is not JSON serializable"
        def _sync():
            return client.run(
                MODEL_ID,
                input={
                    "human_img":    model_uri,
                    "garm_img":     cloth_uri,
                    "garment_des":  pose["garment_des"],
                    "is_checked":       True,
                    "is_checked_crop":  False,
                    "denoise_steps":    30,
                    "seed":         pose["seed"],
                },
            )

        output = await loop.run_in_executor(None, _sync)
        image_url = extract_url(output)

        log.info(f"[{job_id}] pose={pose['key']} OK → {image_url[:80]}")
        return PoseResult(pose=pose["key"], label=pose["label"],
                          status="done", image_url=image_url)

    except Exception as e:
        log.error(f"[{job_id}] pose={pose['key']} FAILED: {e}")
        return PoseResult(pose=pose["key"], label=pose["label"],
                          status="failed", error=str(e))

# ─── JOB RUNNER ──────────────────────────────────────────────────────
JOB_STORE: dict = {}

async def run_job(job_id: str, model_path: Path, cloth_path: Path):
    try:
        if not REPLICATE_API_TOKEN:
            raise ValueError("REPLICATE_API_TOKEN is missing in .env")

        # Read files and convert to base64 data URIs ONCE
        async with aiofiles.open(model_path, "rb") as f:
            model_bytes = await f.read()
        async with aiofiles.open(cloth_path, "rb") as f:
            cloth_bytes = await f.read()

        model_uri = bytes_to_data_uri(model_bytes)
        cloth_uri = bytes_to_data_uri(cloth_bytes)

        loop = asyncio.get_running_loop()

        results = await asyncio.gather(*[
            run_single_pose(job_id, pose, model_uri, cloth_uri, loop)
            for pose in POSES
        ])

        variations = [r.model_dump() for r in results]
        all_failed  = all(r.status == "failed" for r in results)

        JOB_STORE[job_id] = {
            "status":     "failed" if all_failed else "done",
            "variations": variations,
        }
        log.info(f"[{job_id}] job complete status={JOB_STORE[job_id]['status']}")

    except Exception as e:
        log.error(f"[{job_id}] job crash: {e}")
        JOB_STORE[job_id] = {"status": "failed", "error": str(e), "variations": []}

    finally:
        cleanup(model_path)
        cleanup(cloth_path)

# ─── ROUTES ──────────────────────────────────────────────────────────
@app.get("/")
async def root():
    return RedirectResponse("/static/index.html")

@app.get("/health")
async def health():
    return {"status": "ok", "token_set": bool(REPLICATE_API_TOKEN), "model": MODEL_ID}

@app.post("/try-on")
async def try_on(
    background_tasks: BackgroundTasks,
    model_image: UploadFile = File(...),
    cloth_image: UploadFile = File(...),
):
    if not REPLICATE_API_TOKEN:
        raise HTTPException(500, "Server misconfigured: REPLICATE_API_TOKEN not set.")

    model_data = await validate_and_read(model_image)
    cloth_data = await validate_and_read(cloth_image)

    # Save to disk so background task can read them
    model_path = UPLOAD_DIR / f"{uuid.uuid4().hex}.jpg"
    cloth_path = UPLOAD_DIR / f"{uuid.uuid4().hex}.jpg"
    model_path.write_bytes(model_data)
    cloth_path.write_bytes(cloth_data)

    job_id = uuid.uuid4().hex
    JOB_STORE[job_id] = {"status": "processing", "variations": []}
    background_tasks.add_task(run_job, job_id, model_path, cloth_path)

    log.info(f"Job {job_id} queued")
    return {"job_id": job_id}

@app.get("/jobs/{job_id}")
async def get_job(job_id: str):
    return JOB_STORE.get(job_id, {"status": "not_found"})

# ─── STATIC (must be last) ────────────────────────────────────────────
app.mount("/static", StaticFiles(directory="static"), name="static")