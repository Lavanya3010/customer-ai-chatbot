
from datetime import date
from decimal import Decimal

from app.database import SessionLocal
from app.models import Customer, Invoice


def seed_data():
    db = SessionLocal()

    try:
        customers_data = [
            {
                "name": "Arun Kumar",
                "mobile": "9000000001",
            },
            {
                "name": "Priya Devi",
                "mobile": "9000000002",
            },
        ]

        for customer_data in customers_data:
            customer = (
                db.query(Customer)
                .filter_by(mobile=customer_data["mobile"])
                .first()
            )

            if not customer:
                customer = Customer(**customer_data)
                db.add(customer)
                db.flush()

            existing_invoices = (
                db.query(Invoice)
                .filter_by(customer_id=customer.id)
                .count()
            )

            for number in range(existing_invoices + 1, 6):
                invoice = Invoice(
                    customer_id=customer.id,
                    invoice_number=f"INV-{customer.id}-{number:03d}",
                    amount=Decimal("1500.00") + Decimal(number * 100),
                    invoice_date=date(2026, 10, min(number, 28)),
                    description=f"Sample service invoice {number}",
                )
                db.add(invoice)

        db.commit()
        print("Sample customers and invoices added successfully!")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
