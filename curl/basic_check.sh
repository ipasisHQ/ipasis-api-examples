#!/usr/bin/env bash
set -euo pipefail

BASE="${IPASIS_API_BASE:-https://api.ipasis.com}"
BASE="${BASE%/}"
API_KEY="${IPASIS_API_KEY:-}"
IP="${1:-8.8.8.8}"

if [[ -z "${API_KEY}" ]]; then
  echo "ERROR: IPASIS_API_KEY environment variable is not set." >&2
  exit 1
fi

URL="${BASE}/v1/lookup?ip=${IP}&details=true"

echo "GET ${URL}"
echo

set +e
HTTP_RESPONSE=$(curl -sS -w "HTTP_STATUS:%{http_code}" -H "X-API-Key: ${API_KEY}" "${URL}")
STATUS="${HTTP_RESPONSE##*HTTP_STATUS:}"
BODY="${HTTP_RESPONSE%HTTP_STATUS:*}"
set -e

echo "HTTP ${STATUS}"
echo "${BODY}"

if [[ "${STATUS}" -lt 200 || "${STATUS}" -ge 300 ]]; then
  exit 1
fi

