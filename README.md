# Company-Internal-Chatbot-with-Role-Based-Access-Control-RBAC---Group-1

A secure **Company Internal Chatbot** built using **Retrieval-Augmented Generation (RAG)** and **strict Role-Based Access Control (RBAC)**.  
The system ensures that users can **only retrieve information authorized for their role**, preventing cross-department data leakage while still allowing access to company-wide documents.

---

## 🚀 Project Overview

This project implements a **secure, role-aware RAG pipeline** for internal company documents, following the project specification provided in the official PDF.

The backend enforces **authentication, authorization, secure retrieval, and grounded LLM-based responses**.

### Key Guarantees

- 🔒 Users can access **only role-permitted documents**
- 🛡️ No cross-department or privilege-escalation leakage
- 🧠 Retrieval-Augmented Generation (RAG) with grounding
- 📊 Confidence-scored responses
- 📎 Source attribution for every answer
- 📄 Company-wide (general) documents accessible to all employees
- 🧾 Access audit logging for traceability

---


## 👥 Supported Roles

- **Finance**
- **Marketing**
- **HR**
- **Engineering**
- **Employees** (general access only)
- **C-Level** (access to all departments)

## 🔐 Access Rules

| Role        | Accessible Folders                                  |
|--------------|-----------------------------------------------------|
| Finance      | `finance + general`                               |
| Marketing    | `marketing + general`                             |
| HR           | `hr + general`                                    |
| Engineering  | `engineering + general`                           |
| Employees    | `general`                                          |
| C-Level      | `finance + marketing + hr + engineering + general` |

---

## 📂 Data Organization

Documents are organized department-wise:

```bash
data/
└── Fintech-data/
    ├── finance/
    ├── marketing/
    ├── hr/
    ├── engineering/
    └── general/

```
---

## 📄 Supported File Formats

The system supports multiple document formats commonly used in internal company knowledge bases:

- **Markdown (`.md`)** – Policy documents, reports, technical notes
- **CSV (`.csv`)** – Structured data such as financial tables or analytics
- **Text (`.txt`)** – Plain text documentation and logs

All supported formats are parsed and normalized before being ingested into the vector database.

---

## 🏗️ Architecture Summary

### Core Components

#### 🔐 Authentication & Authorization
- JWT-based authentication
- SQLite-backed user database
- bcrypt password hashing
- Username as primary identifier
- Secure dependency-based RBAC enforcement

#### 🧹 Document Preprocessing Pipeline
- File parsing (```.md```, ```.csv```, ```.txt```)
- Text cleaning and normalization
- Token-safe, model-aware chunking
- Role-based metadata injection per chunk

#### 🧠 Vector Store
- SentenceTransformer-based embeddings (```all-MiniLM-L6-v2```)
- Persistent **ChromaDB** storage
- Metadata preserved for every embedded chunk

#### 🔎 Secure Retriever
- High-recall semantic similarity search
- **Post-retrieval RBAC enforcement**
- Context relevance filtering
- Duplicate and low-signal chunk suppression

#### 🤖 LLM Integration (RAG)
- Free HuggingFace LLM (flan-t5-base)
- Strict prompt grounding
- No external knowledge leakage
- Hard fallback when information is missing

#### 📎 Source Attribution
- Document-level citation extraction
- Deduplicated sources
- Transparent answer provenance

#### 📊 Confidence Scoring
- Similarity-score–based confidence
- Relevance-weighted confidence calculation
- Deterministic and explainable scoring

#### 🧾 Audit Logging
- Logs user, role, query, and result count
- Stored securely in backend auth module

---

## 🔄 Processing Pipeline

```text
User Login (JWT)
↓
RBAC Validation
↓
Secure Document Retrieval
↓
Context Relevance Filtering
↓
Prompt Augmentation
↓
LLM Answer Generation
↓
Source Attribution
↓
Confidence Scoring
↓
Final Secure Response

```


---

## 🔐 Security Model (RBAC)

Role-Based Access Control (RBAC) is enforced at the **retrieval layer**, ensuring that access control is applied even after semantic similarity search.

### Key Security Principles
- Authentication via JWT
- Authorization via RBAC metadata
- Retrieval-time access enforcement
- Generation-time grounding enforcement
- No external knowledge leakage
- Safe fallback when data is unavailable

### This Prevents
- Privilege escalation
- Hallucinated answers
- Cross-role inference
- Unauthorized document access
- Metadata tampering

---

## 📌 Milestone 1 :  Environment Setup & Document Preprocessing
### ✅ Implemented
- Project environment setup
- Role → department access mapping
- Document parsing (`.md`, `.csv`, `.txt`)
- Text cleaning and normalization
- Token-safe chunking

## 📌 Milestone 2 :  Vector Database & Secure Retrieval
### ✅ Implemented
- SentenceTransformer embeddings (MiniLM)
- Persistent ChromaDB vector store
- High-recall semantic retrieval
- RBAC-safe post-retrieval filtering
- Duplicate chunk suppression

## 📌 Milestone 3 – Authentication, RBAC API & Secure RAG
### ✅ Implemented
- FastAPI backend
- JWT-based authentication
- SQLite user database
- bcrypt password hashing
- RBAC-protected /query API
- LLM-powered RAG responses
- Source attribution
- Confidence scoring
- Audit logging
- Hallucination prevention
---

## 📊 Current Results (Verified from Demo Runs)

### ✅ Authorized Query Example

```text
User Role : Finance
Query     : financial report revenue

```

- **Total documents loaded**: 21  
- **Total chunks created**: 21  
- **Results returned**: 5  
- **Confidence score**: >0
- **RBAC validation**: **PASS**

✔️ Only finance-authorized content was returned.

### 🚫 Unauthorized Query Example

```text
User Role : Marketing
Query     : employee salary

```

- **Total documents loaded**: 35 
- **Total chunks created**: 35
- **Results returned**: 0
- **Confidence score**: 0.0
- **RBAC validation**: **PASS**

✔️ Unauthorized access was correctly blocked with zero results.

### 🚫 External Knowledge Query (Blocked)
```text
Query : What is the name of PM of India?
```

Response:
```text
The requested information is not available in the provided documents.
```

✔️ Hallucination prevented
✔️ Grounding enforced
---

## 🧪 Running the Backend

From the project root:

```bash
python -m uvicorn backend.app.main:app --reload
```
- API: http://127.0.0.1:8000

- Docs: http://127.0.0.1:8000/docs

## 📁 Project Structure (Current)
```bash
Chatbot/
├── backend/
│   ├── app/
│   │   ├── auth/                    # Authentication & authorization
│   │   │   ├── auth_utils.py        # JWT creation & verification
│   │   │   ├── password_utils.py    # bcrypt password hashing
│   │   │   ├── dependencies.py      # Auth dependency (JWT → user)
│   │   │   ├── audit_logger.py      # Access audit logging
│   │   │   └── access_audit.log     # Auth access logs
│   │   │
│   │   ├── db/                      # User database (SQLite)
│   │   │   ├── database.py          # DB engine & session
│   │   │   ├── models.py            # User table (username as PK)
│   │   │   ├── user_repository.py   # DB access layer
│   │   │   ├── init_db.py           # Add/Delete users interactively
│   │   │   └── users.db             # SQLite user database
│   │   │
│   │   ├── rag/                     # RAG + RBAC pipeline
│   │   │   ├── rbac.py              # Role → document access rules
│   │   │   ├── preprocessing.py     # Parse, clean, chunk, metadata
│   │   │   ├── vector_store.py      # Embeddings + ChromaDB
│   │   │   ├── retriever.py         # Secure RBAC-aware retrieval
│   │   │   ├── citation_utils.py    # Source attribution
│   │   │   ├── confidence_utils.py  # Confidence scoring
│   │   │   ├── rag_pipeline.py      # Full RAG orchestration
│   │   │   ├── pipeline.py          # Vector-store build pipeline
│   │   │   └── __init__.py
│   │   │
│   │   ├── llm/                     # LLM integration
│   │   │   ├── llm_client.py        # HuggingFace LLM wrapper
│   │   │   ├── prompt_templates.py  # Grounded prompt templates
│   │   │   └── __init__.py
│   │   │
│   │   ├── models/
│   │   │   └── user.py              # Pydantic User model
│   │   │
│   │   ├── routes/
│   │   │   ├── auth_routes.py       # /login endpoint
│   │   │   └── chat_routes.py       # /query (RAG + RBAC)
│   │   │
│   │   └── main.py                  # FastAPI entry point
│   │
│   └── requirements.txt             # Backend dependencies
│
├── data/
│   └── Fintech-data/
│       ├── finance/
│       ├── marketing/
│       ├── hr/
│       ├── engineering/
│       └── general/
│
├── frontend/
│   └── streamlit_app.py              # (Planned UI)
│
└── README.md
```