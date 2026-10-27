
from fastapi import FastAPI

from app.database import engine
from app.models import Base
from app.routers.auth import router as auth_router
from app.routers.customers import router as customers_router
from app.routers.invoices import router as invoices_router
from app.routers.conversations import router as conversations_router
from app.routers.messages import router as messages_router

app = FastAPI(
    title="Customer AI Chatbot",
    description="Secure AI-powered customer support assistant",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(customers_router)
app.include_router(invoices_router)
app.include_router(conversations_router)
app.include_router(messages_router)

@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Customer AI Chatbot is running!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
