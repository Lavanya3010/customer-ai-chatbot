import base64
import binascii
import hashlib
import hmac
import json
import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv


load_dotenv()


SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is missing from environment")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



def create_access_token(mobile: str) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    header = {"alg": ALGORITHM, "typ": "JWT"}
    payload = {"sub": mobile, "exp": int(expires_at.timestamp())}

    encoded_header = _encode_segment(header)
    encoded_payload = _encode_segment(payload)
    signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")
    signature = hmac.new(SECRET_KEY.encode("utf-8"), signing_input, hashlib.sha256).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).rstrip(b"=").decode("ascii")

    return f"{encoded_header}.{encoded_payload}.{encoded_signature}"



def decode_access_token(token: str) -> dict:
    try:
        encoded_header, encoded_payload, encoded_signature = token.split(".")
        header = _decode_segment(encoded_header)
        payload = _decode_segment(encoded_payload)
        if header.get("alg") != ALGORITHM or not isinstance(payload, dict):
            raise ValueError("Invalid token")

        signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")
        expected_signature = hmac.new(
            SECRET_KEY.encode("utf-8"), signing_input, hashlib.sha256
        ).digest()
        signature = _decode_base64url(encoded_signature)
        if not hmac.compare_digest(signature, expected_signature):
            raise ValueError("Invalid token signature")

        expiration = payload.get("exp")
        if not isinstance(expiration, (int, float)) or expiration <= datetime.now(timezone.utc).timestamp():
            raise ValueError("Token has expired or has no expiration")

        return payload

    except (binascii.Error, UnicodeDecodeError, ValueError, TypeError, AttributeError) as exc:
        raise ValueError("Invalid or expired access token") from exc


def _encode_segment(value: dict) -> str:
    encoded = json.dumps(value, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(encoded).rstrip(b"=").decode("ascii")


def _decode_segment(segment: str) -> dict:
    decoded = _decode_base64url(segment)
    value = json.loads(decoded.decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError("Invalid token segment")
    return value


def _decode_base64url(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))