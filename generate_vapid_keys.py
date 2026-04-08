#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════
# generate_vapid_keys.py — Run ONCE to generate VAPID keys
# ═══════════════════════════════════════════════════════════

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import base64

# Generate EC key pair (P-256 curve — required for Web Push)
private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
public_key  = private_key.public_key()

# Export private key as PEM (for pywebpush)
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
).decode().strip()

# Export public key as uncompressed point, then base64url encode (for browser)
public_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.X962,
    format=serialization.PublicFormat.UncompressedPoint,
)
public_b64 = base64.urlsafe_b64encode(public_bytes).rstrip(b"=").decode()

print("=" * 60)
print("VAPID Key Pair — copy these into your .env file")
print("=" * 60)
print(f"\nVAPID_PRIVATE_KEY={private_pem}")
print(f"\nVAPID_PUBLIC_KEY={public_b64}")
print("\nVAPID_CLAIMS_EMAIL=mailto:admin@upsamail.edu.gh")
print("\n" + "=" * 60)
print("Keep PRIVATE KEY secret. PUBLIC KEY goes to the frontend.")
print("=" * 60)
