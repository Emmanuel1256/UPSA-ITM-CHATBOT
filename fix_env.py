#!/usr/bin/env python3
"""
Run this once to fix the .env file so the multi-line VAPID private key
is stored as a single line (required by python-dotenv).

Usage:
    python fix_env.py
"""

import os
import re

env_path = os.path.join(os.path.dirname(__file__), ".env")

if not os.path.exists(env_path):
    print("ERROR: .env file not found. Copy .env.example to .env first.")
    exit(1)

with open(env_path, "r") as f:
    content = f.read()

# Extract the private key block (handles multi-line PEM)
pem_match = re.search(
    r'VAPID_PRIVATE_KEY=(-----BEGIN PRIVATE KEY-----.*?-----END PRIVATE KEY-----)',
    content, re.DOTALL
)

if not pem_match:
    print("No multi-line private key found — .env looks fine already.")
    exit(0)

raw_pem = pem_match.group(1)

# Collapse to single line with literal \n
single_line = raw_pem.replace("\n", "\\n")

# Replace in content
content = content[:pem_match.start(1)] + single_line + content[pem_match.end(1):]

with open(env_path, "w") as f:
    f.write(content)

print("✅ .env fixed — VAPID_PRIVATE_KEY is now a single line.")
print("   Restart Flask: python run.py")
