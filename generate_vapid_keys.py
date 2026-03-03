#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════
# generate_vapid_keys.py
# Run ONCE to generate your VAPID key pair for Web Push.
#
# Usage:
#   python generate_vapid_keys.py
#
# Copy the output into your .env file:
#   VAPID_PRIVATE_KEY=<private key>
#   VAPID_PUBLIC_KEY=<public key>
# ═══════════════════════════════════════════════════════════

from py_vapid import Vapid

vapid = Vapid()
vapid.generate_keys()

print("=" * 60)
print("VAPID Key Pair — copy these into your .env file")
print("=" * 60)
print(f"\nVAPID_PRIVATE_KEY={vapid.private_pem().decode().strip()}")
print(f"\nVAPID_PUBLIC_KEY={vapid.public_key}")
print("\n" + "=" * 60)
print("Keep PRIVATE KEY secret. PUBLIC KEY goes to the frontend.")
print("=" * 60)