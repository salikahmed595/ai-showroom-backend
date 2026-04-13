#!/usr/bin/env bash
# Quick smoke-test for the Virtual Try-On API
# Usage: bash test.sh <model_image.jpg> <cloth_image.jpg>

BASE="http://localhost:8000"
MODEL="${1:-model.jpg}"
CLOTH="${2:-cloth.jpg}"

echo "─── Submitting try-on job ───────────────────────────────"
RESPONSE=$(curl -s -X POST "$BASE/try-on" \
  -F "model_image=@$MODEL;type=image/jpeg" \
  -F "cloth_image=@$CLOTH;type=image/jpeg")

echo "$RESPONSE" | python3 -m json.tool
JOB_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['job_id'])")

echo ""
echo "─── Polling job: $JOB_ID ────────────────────────────────"
for i in $(seq 1 30); do
  sleep 5
  STATUS=$(curl -s "$BASE/jobs/$JOB_ID")
  echo "$STATUS" | python3 -m json.tool
  STATE=$(echo "$STATUS" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
  if [[ "$STATE" == "done" || "$STATE" == "failed" ]]; then
    break
  fi
  echo "  ... still $STATE, retrying ($i/30)"
done
