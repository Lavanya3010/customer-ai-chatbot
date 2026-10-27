# Customer AI Chatbot

An AI-powered customer support chatbot built using FastAPI, PostgreSQL, Google Gemini, and Retrieval-Augmented Generation (RAG).

## Project Overview

The Customer AI Chatbot helps customers retrieve invoice information and get AI-generated responses to their queries. It provides APIs for customer management, invoice retrieval, authentication, and conversation history.

## Features

- Customer information retrieval
- Invoice details and payment status retrieval
- OTP-based authentication
- Customer-specific access protection
- AI-powered question answering using Google Gemini
- Retrieval-Augmented Generation (RAG) for invoice-related queries
- Conversation creation and message history
- PostgreSQL database integration
- API documentation using Swagger UI

## Technologies Used

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Google Gemini API
- Qdrant Vector Database
- Python-dotenv
- Git and GitHub

## Project Structure

```text
customer-ai-chatbot/
├── alembic/
│   └── versions/
├── app/
│   ├── rag/
│   │   ├── index_invoices.py
│   │   └── vector_store.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── conversations.py
│   │   ├── customers.py
│   │   ├── invoices.py
│   │   └── messages.py
│   ├── services/
│   │   ├── embedding_service.py
│   │   └── llm_service.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── security.py
│   └── seed.py
├── .gitignore
├── alembic.ini
└── requirements.txt
```

## Prerequisites

Install the following before running the project:

- Python
- PostgreSQL
- A Google Gemini API key
- Qdrant configuration required by the project

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Lavanya3010/customer-ai-chatbot.git
cd customer-ai-chatbot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root. Add the environment variable names expected by your application, for example:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Configure the PostgreSQL connection and any other required settings using the names expected by your application code.

**Security:** Never commit `.env` files, API keys, database passwords, or authentication secrets to GitHub.

### 5. Start the application

```bash
uvicorn app.main:app --reload
```

### 6. Open API documentation

Swagger UI:

http://127.0.0.1:8000/docs

Health endpoint:

http://127.0.0.1:8000/health

## API Modules

| Module | Purpose |
|---|---|
| Authentication | OTP request and verification |
| Customers | Retrieve customer information |
| Invoices | Retrieve invoice information |
| Conversations | Create and manage conversations |
| Messages | Submit questions and retrieve chat history |

Refer to the Swagger UI documentation for the available endpoints and request formats.

## Security

- Environment variables are used to manage sensitive configuration.
- Customer-specific access restrictions help protect customer and invoice information.
- Secret keys and credentials must not be committed to the repository.

## Future Improvements

- Add automated tests for API endpoints.
- Improve error handling and logging.
- Add a frontend chat interface.
- Improve deployment and production configuration.

## Author

Developed as a Customer AI Chatbot project.