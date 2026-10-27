from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Customer, Invoice
from app.security import decode_access_token

router = APIRouter(prefix="/customers", tags=["Customers"])

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


@router.get("/")
def get_customers(
    current_customer: Customer = Depends(get_current_customer),
):
    # Customers can access only their own details.
    return [
        {
            "id": current_customer.id,
            "name": current_customer.name,
            "mobile": current_customer.mobile,
        }
    ]


@router.get("/{customer_id}")
def get_customer(
    customer_id: int,
    current_customer: Customer = Depends(get_current_customer),
):
    if customer_id != current_customer.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot access another customer's details",
        )

    return {
        "id": current_customer.id,
        "name": current_customer.name,
        "mobile": current_customer.mobile,
    }


@router.get("/{customer_id}/invoices")
def get_customer_invoices(
    customer_id: int,
    db: Session = Depends(get_db),
    current_customer: Customer = Depends(get_current_customer),
):
    if customer_id != current_customer.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot access another customer's invoices",
        )

    invoices = (
        db.query(Invoice)
        .filter(Invoice.customer_id == current_customer.id)
        .all()
    )

    return [
        {
            "id": invoice.id,
            "customer_id": invoice.customer_id,
            "invoice_number": invoice.invoice_number,
            "amount": float(invoice.amount),
            "invoice_date": invoice.invoice_date,
            "description": invoice.description,
        }
        for invoice in invoices
    ]