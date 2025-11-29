#!/usr/bin/env node

const apiKey = process.env.IPASIS_API_KEY;
if (!apiKey) {
  console.error("ERROR: IPASIS_API_KEY environment variable is not set.");
  process.exit(1);
}

const base = (process.env.IPASIS_API_BASE || "https://api.ipasis.com").replace(/\/+$/, "");
const ip = process.argv[2] || "8.8.8.8";

async function main() {
  const url = `${base}/v1/lookup?ip=${encodeURIComponent(ip)}&details=true`;

  try {
    const res = await fetch(url, {
      method: "GET",
      headers: {
        "X-API-Key": apiKey,
      },
    });

    console.log(`HTTP ${res.status}`);
    const text = await res.text();

    try {
      const json = JSON.parse(text);
      console.log(JSON.stringify(json, null, 2));
    } catch {
      console.log(text);
    }

    if (!res.ok) {
      process.exit(1);
    }
  } catch (err) {
    console.error("ERROR: request failed:", err);
    process.exit(1);
  }
}

main();

