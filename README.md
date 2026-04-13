# 👗 Virtual Try-On API

A production-grade **FastAPI** backend that accepts a model photo + garment image,
runs them through **Replicate's flux-vton** model, and returns the generated try-on URL.

---

## Architecture

```
Client
  │
  ▼
POST /try-on  ──►  Validate images  ──►  Save to disk  ──►  Queue background task
                                                                      │
                                                                      ▼
                                                           Replicate flux-vton API
                                                                      │
                                                                      ▼
GET /jobs/{id}  ◄──────────────────────────────────  Store result in JOB_STORE
```

**Flow:**
1. Client uploads two images → `POST /try-on`
2. API validates, saves temporarily, queues async job → returns `job_id` instantly (202)
3. Background task calls Replicate, stores result
4. Client polls `GET /jobs/{job_id}` until `status: done`

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health ping |
| `GET` | `/health` | Detailed health + config check |
| `POST` | `/try-on` | Submit model + cloth images |
| `GET` | `/jobs/{job_id}` | Poll job status / get result URL |
| `DELETE` | `/jobs/{job_id}` | Clean up a finished job |

### POST `/try-on`

**Form fields:**

| Field | Type | Description |
|-------|------|-------------|
| `model_image` | `File` | Photo of the person wearing the garment |
| `cloth_image` | `File` | Photo of the standalone garment |

**Response (202):**
```json
{
  "job_id": "a1b2c3d4e5f6...",
  "status": "pending",
  "poll_url": "http://localhost:8000/jobs/a1b2c3d4e5f6...",
  "message": "Job queued. Poll the status URL for updates."
}
```

### GET `/jobs/{job_id}`

```json
{
  "job_id": "a1b2c3d4e5f6...",
  "status": "done",
  "result_url": "https://replicate.delivery/pbxt/...",
  "error": null,
  "message": "Try-on complete! Use result_url to view the image."
}
```

Status values: `pending` → `processing` → `done` | `failed`

---

## Setup

### 1. Prerequisites

- Python 3.11+
- A [Replicate](https://replicate.com) account with an API token

### 2. Install

```bash
cd vton-api
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure

```bash
cp .env.example .env
# Edit .env and set REPLICATE_API_TOKEN=r8_xxxx
export $(cat .env | xargs)
```

### 4. Run

```bash
uvicorn main:app --reload --port 8000
```

Interactive docs → [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Docker

```bash
docker build -t vton-api .
docker run -p 8000:8000 -e REPLICATE_API_TOKEN=r8_xxx vton-api
```

---

## Quick Test

```bash
chmod +x test.sh
./test.sh model.jpg cloth.jpg
```

Or with curl directly:

```bash
# Step 1 — submit
curl -X POST http://localhost:8000/try-on \
  -F "model_image=@model.jpg;type=image/jpeg" \
  -F "cloth_image=@cloth.jpg;type=image/jpeg"

# Step 2 — poll (replace JOB_ID)
curl http://localhost:8000/jobs/JOB_ID
```

---

## Constraints & Limits

| Parameter | Value |
|-----------|-------|
| Max file size | 10 MB per image |
| Accepted formats | JPEG, PNG, WebP |
| Replicate model | `zsxkib/flux-pulid` (flux-vton) |
| Job storage | In-memory (use Redis for multi-worker prod) |

---

## Production Checklist

- [ ] Replace in-memory `JOB_STORE` with Redis / database
- [ ] Add authentication (API key / OAuth)
- [ ] Store uploaded images in S3 / GCS instead of local disk
- [ ] Set `--workers` based on CPU count in Dockerfile
- [ ] Add rate limiting (e.g. `slowapi`)
- [ ] Add structured logging (JSON) for log aggregation
- [ ] Configure `CORS` origins to your frontend domain only
