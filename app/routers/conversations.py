from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Conversation, Customer
from app.security import decode_access_token

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)

security = HTTPBearer()


def get_current_customer(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    try:
        payload = decode_access_token(credentials.credentials)
    except Exception as exc:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token",
        ) from exc

    mobile = payload.get("sub")

    if not mobile:
        raise HTTPException(
            status_code=401,
            detail="Invalid access token",
        )

    customer = (
        db.query(Customer)
        .filter(Customer.mobile == mobile)
        .first()
    )

    if customer is None:
        raise HTTPException(
            status_code=401,
            detail="Customer not found",
        )

    return customer


@router.post("/")
def create_conversation(
    title: str = "Customer Support",
    db: Session = Depends(get_db),
    current_customer: Customer = Depends(get_current_customer),
):
    conversation = Conversation(
        customer_id=current_customer.id,
        title=title,
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return {
        "id": conversation.id,
        "customer_id": conversation.customer_id,
        "title": conversation.title,
        "created_at": conversation.created_at,
    }


@router.get("/")
def get_conversations(
    db: Session = Depends(get_db),
    current_customer: Customer = Depends(get_current_customer),
):
    conversations = (
        db.query(Conversation)
        .filter(Conversation.customer_id == current_customer.id)
        .all()
    )

    return conversations