from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue

from app.services.embedding_service import create_embedding

# Connect to local Qdrant server
client = QdrantClient(url="http://localhost:6333")

COLLECTION_NAME = "customer_invoices"
VECTOR_SIZE = 384


def create_collection():
    """Create the invoice collection if it doesn't exist."""
    collections = client.get_collections().collections
    collection_names = [item.name for item in collections]

    if COLLECTION_NAME not in collection_names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )


def store_invoice(
    invoice_id: int,
    customer_id: int,
    invoice_text: str,
):
    """Store an invoice embedding with its customer ID."""
    create_collection()

    vector = create_embedding(invoice_text)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=invoice_id,
                vector=vector,
                payload={
                    "customer_id": customer_id,
                    "invoice_id": invoice_id,
                    "invoice_text": invoice_text,
                },
            )
        ],
        wait=True,
    )

    return {"message": "Invoice stored successfully"}


def search_invoices(
    query: str,
    customer_id: int,
    limit: int = 5,
):
    """Search invoices belonging to a specific customer."""
    query_vector = create_embedding(query)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="customer_id",
                    match=MatchValue(value=customer_id),
                )
            ]
        ),
        limit=limit,
        with_payload=True,
    ).points

    return [
        {
            "invoice_id": point.payload["invoice_id"],
            "invoice_text": point.payload["invoice_text"],
        }
        for point in results
    ]