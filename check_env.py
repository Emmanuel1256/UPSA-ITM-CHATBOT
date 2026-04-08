#!/usr/bin/env python3
"""
Run this to diagnose what Flask sees for VAPID keys.
Usage: python check_env.py
"""
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ dotenv loaded")
except ImportError:
    print("⚠️  python-dotenv not installed")

priv = os.environ.get("VAPID_PRIVATE_KEY", "")
pub  = os.environ.get("VAPID_PUBLIC_KEY",  "")

print(f"\nVAPID_PRIVATE_KEY length : {len(priv)} chars")
print(f"VAPID_PRIVATE_KEY preview: {repr(priv[:60])}")
print(f"\nVAPID_PUBLIC_KEY  length : {len(pub)} chars")
print(f"VAPID_PUBLIC_KEY  value  : {pub}")
print()

if not priv:
    print("❌ PRIVATE KEY is empty — check your .env file")
elif "BEGIN PRIVATE KEY" not in priv and "\\n" not in priv:
    print("❌ PRIVATE KEY looks malformed")
else:
    print("✅ PRIVATE KEY looks present")

if not pub:
    print("❌ PUBLIC KEY is empty — check your .env file")
elif len(pub) < 50:
    print("❌ PUBLIC KEY looks too short")
else:
    print("✅ PUBLIC KEY looks present")
