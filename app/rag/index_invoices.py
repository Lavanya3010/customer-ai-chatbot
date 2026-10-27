from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Invoice
from app.rag.vector_store import store_invoice


def index_all_invoices():
    """Fetch invoices from PostgreSQL and store them in Qdrant."""
    db: Session = SessionLocal()

    try:
        invoices = db.query(Invoice).all()

        if not invoices:
            print("No invoices found in PostgreSQL.")
            return

        for invoice in invoices:
            invoice_text = (
                f"Invoice number: {invoice.invoice_number}. "
                f"Amount: {invoice.currency} {invoice.amount}. "
                f"Status: {invoice.payment_status}. "
                f"Date: {invoice.invoice_date}. "
                f"Description: {invoice.description or 'No description'}."
            )

            store_invoice(
                invoice_id=invoice.id,
                customer_id=invoice.customer_id,
                invoice_text=invoice_text,
            )

            print(
                f"Indexed invoice {invoice.invoice_number} "
                f"for customer ID {invoice.customer_id}"
            )

        print("Invoice indexing completed successfully!")

    finally:
        db.close()


if __name__ == "__main__":
    index_all_invoices()