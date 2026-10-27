from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Invoice, Customer
from app.security import decode_access_token

router = APIRouter(prefix="/invoices", tags=["Invoices"])

bearer_scheme = HTTPBearer()


def get_current_customer(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        payload = decode_access_token(token)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

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
            detail="Customer account not found",
        )

    return customer


@router.get("/")
def get_invoices(
    customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    invoices = (
        db.query(Invoice)
        .filter(Invoice.customer_id == customer.id)
        .all()
    )

    return [
        {
            "id": invoice.id,
            "customer_id": invoice.customer_id,
            "invoice_number": invoice.invoice_number,
            "amount": float(invoice.amount),
            "currency": invoice.currency,
            "invoice_date": invoice.invoice_date,
            "payment_status": invoice.payment_status,
            "description": invoice.description,
        }
        for invoice in invoices
    ]


@router.get("/{invoice_id}")
def get_invoice(
    invoice_id: int,
    customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    invoice = (
        db.query(Invoice)
        .filter(
            Invoice.id == invoice_id,
            Invoice.customer_id == customer.id,
        )
        .first()
    )

    if invoice is None:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found",
        )

    return {
        "id": invoice.id,
        "customer_id": invoice.customer_id,
        "invoice_number": invoice.invoice_number,
        "amount": float(invoice.amount),
        "currency": invoice.currency,
        "invoice_date": invoice.invoice_date,
        "payment_status": invoice.payment_status,
        "description": invoice.description,
    }