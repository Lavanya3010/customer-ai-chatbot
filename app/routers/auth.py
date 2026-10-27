import secrets
import time

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

otp_store = {}
resend_store = {}

OTP_EXPIRY_SECONDS = 300
RESEND_COOLDOWN_SECONDS = 60
MAX_ATTEMPTS = 5


class OTPRequest(BaseModel):
    mobile: str = Field(min_length=10, max_length=20)


class OTPVerify(BaseModel):
    mobile: str = Field(min_length=10, max_length=20)
    otp: str = Field(pattern=r"^\d{6}$")


def normalize_mobile(mobile: str) -> str:
    return "".join(ch for ch in mobile if ch.isdigit())


@router.post("/request-otp")
def request_otp(payload: OTPRequest):
    mobile = normalize_mobile(payload.mobile)

    if len(mobile) < 10 or len(mobile) > 15:
        raise HTTPException(
            status_code=400,
            detail="Invalid mobile number",
        )

    now = time.time()
    last_sent = resend_store.get(mobile, 0)

    if now - last_sent < RESEND_COOLDOWN_SECONDS:
        remaining = int(
            RESEND_COOLDOWN_SECONDS - (now - last_sent)
        )

        raise HTTPException(
            status_code=429,
            detail=f"Please wait {remaining} seconds before requesting another OTP",
        )

    otp = f"{secrets.randbelow(1_000_000):06d}"

    otp_store[mobile] = {
        "otp": otp,
        "expires_at": now + OTP_EXPIRY_SECONDS,
        "attempts": 0,
    }

    resend_store[mobile] = now

    print(f"DEV OTP for {mobile}: {otp}")

    return {
        "message": "OTP generated. Check the development server terminal.",
        "expires_in_seconds": OTP_EXPIRY_SECONDS,
    }



@router.post("/verify-otp")
def verify_otp(payload: OTPVerify):
    mobile = normalize_mobile(payload.mobile)
    record = otp_store.get(mobile)

    if not record:
        raise HTTPException(
            status_code=400,
            detail="OTP not found or already used",
        )

    
    if time.time() >= record["expires_at"]:
        otp_store.pop(mobile, None)

        raise HTTPException(
            status_code=400,
            detail="OTP expired",
        )

    
    if record["attempts"] >= MAX_ATTEMPTS:
        otp_store.pop(mobile, None)

        raise HTTPException(
            status_code=429,
            detail="Maximum OTP attempts exceeded",
        )

    record["attempts"] += 1

    
    if not secrets.compare_digest(record["otp"], payload.otp):
        if record["attempts"] >= MAX_ATTEMPTS:
            otp_store.pop(mobile, None)

            raise HTTPException(
                status_code=429,
                detail="Maximum OTP attempts exceeded",
            )

        raise HTTPException(
            status_code=400,
            detail="Invalid OTP",
        )

   
    otp_store.pop(mobile, None)

    
    access_token = create_access_token(mobile)

    return {
        "message": "OTP verified successfully",
        "mobile": mobile,
        "verified": True,
        "access_token": access_token,
        "token_type": "bearer",
    }