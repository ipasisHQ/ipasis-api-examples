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
https://api.ipasis.com/v1/lookup?ip=8.8.8.8
```

Authentication:
- Send `X-API-Key: <your_api_key>` or
- `Authorization: Bearer <your_api_key>` or
- As a query parameter: `?key=<your_api_key>`

## 3. Endpoints

### 3.1 Request

- Method: `GET`
- Path: `/v1/lookup`
- Query parameters:
  - `ip` (required) — IPv4 or IPv6 address.
  - `key` (optional) — API key, when you prefer query-string auth instead of headers.

Example request:

```txt
https://api.ipasis.com/v1/lookup?ip=136.179.39.31&key=ipasis_53f9b76e0066_54ce31f11158cd7bc1b5d12e6b72a3da
```

### 3.2 Response

On success (`200 OK`), the API returns a JSON document describing the IP. The exact schema may evolve, but at a high level it includes:

- Basic identity: IP, version, country/region.
- Privacy / risk signals: Tor, VPN, hosting, datacenter, etc.
- Network and ownership: ASN, organization / company.
- Abuse / blocklist context.

Concrete example for the request above:

```json
{
  "ip": "136.179.39.31",
  "city": "Irvine",
  "region": "California",
  "country": "US",
  "loc": "33.7074,-117.7054",
  "postal": "92618",
  "timezone": "America/Los_Angeles",
  "asn": {
    "ASN": "AS23005",
    "Name": "SWITCH-LTD",
    "Domain": "",
    "Route": "",
    "Type": ""
  },
  "company": {
    "Name": "SWITCH-LTD",
    "Domain": "",
    "Type": ""
  },
  "privacy": {
    "VPN": false,
    "Proxy": false,
    "Tor": false,
    "Relay": false,
    "Hosting": false,
    "Abuse": false,
    "AI": false,
    "Crawler": false,
    "Service": ""
  },
  "abuse": {
    "Address": "",
    "Country": "",
    "Email": "",
    "Name": "",
    "Network": "",
    "Phone": ""
  },
  "domains": {
    "Page": 0,
    "Total": 0,
    "Domains": null
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
