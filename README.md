# IPASIS API Examples

This repository contains minimal, copy‑pasteable examples for calling the IPASIS HTTP API from different environments.

Currently included:
- `python/basic_check.py`
- `node/basic_check.js`
- `curl/basic_check.sh`

## 1. Prerequisites

- An IPASIS account and API key (from the dashboard on `ipasis.com`).
- Network access to the public API.
- For language-specific examples:
  - Python 3.8+ and `requests` (`pip install requests`)
  - Node.js 18+ (for built-in `fetch`)
  - `curl` (any recent version)

All examples read your key from the `IPASIS_API_KEY` environment variable:

```bash
export IPASIS_API_KEY="your_api_key_here"
```

Optionally, you can override the base URL with `IPASIS_API_BASE` (defaults to production).

## 2. Base URL

- Production base URL: `https://api.ipasis.com`
- Primary endpoint path: `GET /v1/lookup`

Example full URL:

```txt
https://api.ipasis.com/v1/lookup?ip=8.8.8.8&details=true
```

Authentication:
- Send `X-API-Key: <your_api_key>` or
- `Authorization: Bearer <your_api_key>`

## 3. Endpoints

### 3.1 Request

- Method: `GET`
- Path: `/v1/lookup`
- Query parameters:
  - `ip` (required) — IPv4 or IPv6 address.
  - `details` (optional, default `false`) — when `true`, include enriched provenance/details.

Example request (curl):

```bash
curl -s "https://api.ipasis.com/v1/lookup?ip=8.8.8.8&details=true" \
  -H "X-API-Key: <your_api_key>"
```

### 3.2 Response

On success (`200 OK`), the API returns a JSON document describing the IP. The exact schema may evolve, but at a high level it includes:

- Basic identity: IP, version, country/region.
- Privacy / risk signals: Tor, VPN, hosting, datacenter, etc.
- Network and ownership: ASN, organization / company.
- Abuse / blocklist context.
- Optional `details` sub-objects when `details=true`.

Example (truncated) response shape:

```json
{
  "ip": "8.8.8.8",
  "is_tor": false,
  "is_vpn": false,
  "asn": {
    "number": 15169,
    "name": "Google LLC"
  },
  "company": {
    "name": "Google LLC",
    "domain": "google.com"
  },
  "abuse": {
    "score": 5
  },
  "details": {
    "sources": [/* provenance data, when enabled */]
  }
}
```

On error, you will receive consistent JSON with an HTTP status such as:
- `400` for invalid IPs or parameters.
- `401` / `403` for missing/invalid API key.
- `429` when rate limits are exceeded.

## 4. Example scripts

### 4.1 Python — `python/basic_check.py`

Usage:

```bash
export IPASIS_API_KEY="your_api_key"
python python/basic_check.py 8.8.8.8
```

### 4.2 Node.js — `node/basic_check.js`

Usage:

```bash
export IPASIS_API_KEY="your_api_key"
node node/basic_check.js 8.8.8.8
```

### 4.3 curl — `curl/basic_check.sh`

Usage:

```bash
export IPASIS_API_KEY="your_api_key"
bash curl/basic_check.sh 8.8.8.8
```

Each script prints the HTTP status code (if applicable) and the JSON response body so you can quickly verify that your key and environment are wired correctly.
