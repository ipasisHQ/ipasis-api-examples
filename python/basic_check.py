#!/usr/bin/env python3

import os
import sys
import json
from typing import Any

import requests


def main() -> None:
  api_key = os.getenv("IPASIS_API_KEY")
  if not api_key:
    print("ERROR: IPASIS_API_KEY environment variable is not set.", file=sys.stderr)
    sys.exit(1)

  base = os.getenv("IPASIS_API_BASE", "https://api.ipasis.com")
  ip = sys.argv[1] if len(sys.argv) > 1 else "8.8.8.8"

  url = f"{base.rstrip('/')}/v1/lookup"
  params = {"ip": ip, "details": "true"}
  headers = {"X-API-Key": api_key}

  try:
    resp = requests.get(url, params=params, headers=headers, timeout=5)
  except Exception as exc:  # noqa: BLE001
    print(f"ERROR: request failed: {exc}", file=sys.stderr)
    sys.exit(1)

  print(f"HTTP {resp.status_code}")
  try:
    data: Any = resp.json()
    print(json.dumps(data, indent=2, sort_keys=True))
  except ValueError:
    print(resp.text)

  if not resp.ok:
    sys.exit(1)


if __name__ == "__main__":
  main()

