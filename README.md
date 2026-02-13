# 🏢 Company Internal Chatbot with Role-Based Access Control (RBAC)

A secure **Company Internal Chatbot** built using **Retrieval-Augmented Generation (RAG)** and **strict Role-Based Access Control (RBAC)**.  
The system ensures that users can retrieve **only role-authorized internal company information**, preventing cross-department data leakage while maintaining transparency, traceability, and grounded AI responses.

---

## 🚀 Project Overview

This project implements a **secure, role-aware RAG pipeline** for internal company documents, fully aligned with the official project specification PDF.

The system enforces **authentication, authorization, secure retrieval, grounded generation, confidence scoring, and source attribution** across all user queries.

---

## 🔐 Key Guarantees

- 🔒 Strict **role-based document access**
- 🛡️ Zero cross-department or privilege-escalation leakage
- 🧠 Retrieval-Augmented Generation (RAG)
- 📎 Source attribution for every answer
- 📊 Confidence-scored responses
- 🧾 Access audit logging
- 🚫 Hallucination prevention (no external knowledge)
- 📄 Company-wide documents accessible to all employees

---

### 👥 Supported Roles

- **Employees**
- **Finance**
- **HR**
- **Marketing**
- **Engineering**
- **C-Level**

---

### 📄 Department Access Matrix

| Role        | Finance Docs | HR Docs | Marketing Docs | Engineering Docs | General Docs |
|------------|--------------|---------|----------------|------------------|--------------|
| Employees  | ❌ No        | ❌ No   | ❌ No          | ❌ No            | ✅ Yes       |
| Finance    | ✅ Yes       | ❌ No   | ❌ No          | ❌ No            | ✅ Yes       |
| HR         | ❌ No        | ✅ Yes  | ❌ No          | ❌ No            | ✅ Yes       |
| Marketing  | ❌ No        | ❌ No   | ✅ Yes         | ❌ No            | ✅ Yes       |
| Engineering| ❌ No        | ❌ No   | ❌ No          | ✅ Yes           | ✅ Yes       |
| C-Level    | ✅ Yes       | ✅ Yes  | ✅ Yes         | ✅ Yes           | ✅ Yes       |

---

## 📂 Data Organization

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
- SQLite user database
- bcrypt password hashing
- Dependency-based RBAC enforcement

#### 🧹 Document Preprocessing Pipeline
- File parsing (```.md```, ```.csv```, ```.txt```)
- Text cleaning and normalization
- Token-safe chunking (model-aware)
- Role metadata injection per chunk
- Department-wise ingestion tracking

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
- Gemini API (free-tier)
- Strictly grounded prompts
- No external knowledge usage
- Safe fallback responses

#### 📎 Source Attribution
- Document-level citation extraction
- Deduplicated sources
- Transparent answer provenance

#### 📊 Confidence Scoring
- Similarity-score–based confidence
- Deterministic and explainable scoring

#### 🧾 Audit Logging
- Logs user, role, query, and result count
- Stored securely in backend auth module

---

## 🔄 Processing Pipeline

```text
User Login  
↓  
JWT Authentication  
↓  
RBAC Validation  
↓  
Secure Vector Retrieval  
↓  
RBAC Filtering  
↓  
Context Construction  
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

## 🔐 RBAC Role Matrix

The system enforces **strict Role-Based Access Control (RBAC)** to ensure users can only access information permitted by their role.

Each document chunk is tagged with role metadata, and access is enforced at both the **API layer** and **vector retrieval layer**.

---

## 📁 Project Structure
```bash
Chatbot/
├── backend/
│   ├── auth/                    # Authentication & authorization
│   │   ├── auth_utils.py        # JWT creation & verification
│   │   ├── password_utils.py    # bcrypt password hashing
│   │   ├── dependencies.py      # Auth dependency (JWT → user)
│   │   └── audit_logger.py      # Access audit logging
│   │
│   ├── db/                      # User database (SQLite)
│   │   ├── database.py          # DB engine & session
│   │   ├── models.py            # User table (username as PK)
│   │   ├── user_repository.py   # DB access layer
│   │   ├── init_db.py           # Add/Delete users interactively
│   │   └── users.db             # SQLite user database
│   │
│   ├── rag/                     # RAG + RBAC pipeline
│   │   ├── rbac.py              # Role → document access rules
│   │   ├── preprocessing.py     # Parse, clean, chunk, metadata
│   │   ├── vector_store.py      # Embeddings + ChromaDB
│   │   ├── retriever.py         # Secure RBAC-aware retrieval
│   │   ├── citation_utils.py    # Source attribution
│   │   ├── confidence_utils.py  # Confidence scoring
│   │   ├── rag_pipeline.py      # Full RAG orchestration
│   │   ├── pipeline.py          # Vector-store build pipeline
│   │   └── __init__.py
│   │
│   ├── llm/                     # LLM integration
│   │   ├── llm_client.py        # HuggingFace LLM wrapper
│   │   ├── prompt_templates.py  # Grounded prompt templates
│   │   └── __init__.py
│   │
│   ├── models/
│   │   └── user.py              # Pydantic User model
│   │
│   ├── routes/
│   │   ├── auth_routes.py       # /login endpoint
│   │   ├── chat_routes.py       # /query (RAG + RBAC)
│   │   └── user_routes.py       # manage users (ADD/DELETE users)
│   │
│   └── main.py                  # FastAPI entry point
│
├── data/
│   └── Fintech-data/
│       ├── finance/
│       ├── marketing/
│       ├── hr/
│       ├── engineering/
│       └── general/
│
├── frontend/                 # Streamlit User Interface
│   ├── api_client.py         # Connects UI to Backend
│   └── streamlit_app.py      # Main UI Logic
│
├──  .env                     # Gemini Api and Backend Url
├──  requirements.txt         # dependencies
└── README.md
```


## 🚀 Installation

### 🔧 1. Clone the Repository
```bash
git clone https://github.com/arman61-hub/IntraBot.git
cd IntraBot
```

### 🧪 2. Create and Activate Virtual Environment

It is recommended to use a Python virtual environment to isolate project dependencies.

#### 🪟 Windows
```bash
python -m venv venv
venv\Scripts\activate
```
#### 🐧 Linux / 🍎 macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

### ⚙️ 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 🔐 4. Configure Environment Variables
Create a .env file and add:
```bash
GEMINI_API_KEY=
JWT_SECRET_KEY=
DEFAULT_ADMIN_USERNAME=admin
DEFAULT_ADMIN_PASSWORD=admin123
DEFAULT_ADMIN_ROLE=c_level
FRONTEND_URL=http://localhost:8501
DATA_DIR=/var/data

BACKEND_URL=http://127.0.0.1:8000
```

### 🚀 5. Start Backend
```bash
python -m uvicorn backend.main:app --reload
```
- API: http://127.0.0.1:8000

- Docs: http://127.0.0.1:8000/docs

### 💻 6. Start Frontend
```bash
streamlit run frontend/streamlit_app.py  
```
- UI: http://localhost:8501

## 🖼️ Screenshots

The following screenshots demonstrate the key functionalities of the system, including authentication, role-based access control, and RAG-based responses.

---

### 🔐 User Login Interface
Shows the Streamlit-based login screen where users authenticate using their credentials.

![Login Screen](data/screenshots/login.png)

---

### 🚫 Role-Based Access Control (RBAC) – Access Denied (Wrong IDP)
Illustrates access denial when a user attempts to authenticate or query the system using an incorrect or unauthorized Identity Provider (IDP).

![Access Denied – Wrong IDP](data/screenshots/access_denied_wrong_idp.png)

---

### 💬 Chat Interface with RAG Response
Demonstrates a successful query response generated using the RAG pipeline, including:
- Context-aware answer
- Source document attribution

![Chat Interface](data/screenshots/chat_response.png)

---

## 🔑 Demo Credentials

The system includes preconfigured demo users:


| Username  | Password | Role        |
|-----------|----------|-------------|
| admin     | admin123 | C-Level     |
| carol     | carol123 | HR          |
| alice     | alice123 | Finance     |
| eve       | eve123   | Employees   |
| bob       | bob123   | Marketing   |
| dave      | dave123  | Engineering |

---


### 🖥️ Backend
| Component | Technology |
|---------|------------|
| Web Framework | FastAPI |
| API Server | Uvicorn |
| Authentication | JWT (python-jose) |
| Password Security | bcrypt (passlib) |
| Database | SQLite (SQLAlchemy ORM) |
| Access Control | Dependency-based RBAC enforcement |
| Environment Config | python-dotenv |

---

### 🧠 Retrieval & AI
| Component | Technology |
|---------|------------|
| Embedding Model | sentence-transformers/all-MiniLM-L6-v2 |
| Vector Database | ChromaDB (Persistent Storage) |
| LLM | Gemini API (gemini-2.5-flash) |
| RAG Strategy | Secure Retrieval-Augmented Generation (RBAC-aware) |
| Prompt Engineering | Custom grounded prompt templates |
| Confidence Scoring | Vector-distance-based scoring |

---

### 📄 Data Processing
| Component | Technology |
|---------|------------|
| Document Formats | Markdown (`.md`), CSV (`.csv`), Text (`.txt`) |
| Text Processing | Regex cleaning + SentenceTransformer tokenizer |
|Chunking Strategy | Token-aware sliding window chunking|
|Metadata Injection | Role-based department metadata per chunk|
|Data Handling | Pandas|

---

### 🖥️ Frontend
| Component | Technology |
|---------|------------|
|Web Interface | Streamlit|
|User Interaction | Chat-based conversational UI|
|Authentication Flow | JWT-based secure login|
|Source Display | Inline source citations|
|API Communication | Requests (HTTP client)|

---

### 🔧 Dev & Utilities
| Component | Technology |
|---------|------------|
|Language | Python 3.11+|
|Version Control | Git & GitHub|
|Logging | Python Logging (audit logging enabled)|
|HTTP Client | Requests|
|ORM | SQLAlchemy|
|Environment Management | venv (Virtual Environment)|

---

## 🔒 Security Considerations

- **JWT-Based Authentication**  
  All protected endpoints require a valid token.

- **Password Hashing**  
  Passwords hashed using bcrypt before storage.

- **Multi-Layer RBAC Enforcement**  
  - API dependency layer  
  - Vector retrieval filtering  
  - RAG pipeline validation  

- **No Data Leakage**  
  Users cannot access documents outside assigned roles.

- **Audit Logging**  
  All access attempts logged in access_audit.log.

This ensures secure handling of sensitive internal company data.

---

## 📌 Assumptions

- All users are internal company users.
- Documents are trusted and pre-validated.
- Role assignments are managed by an administrator.
- Deployment occurs in a controlled internal environment.

---

## 🤝 Contributing

We welcome contributions to improve **IntraBot**!

### 🧩 How to Contribute

#### 1. Fork the Repository  
   Click the **Fork** button on the top right of this page.

#### 2. Clone Your Fork 
   Open terminal and run:
   ```bash
   git clone https://github.com/yourusername/IntraBot.git
   cd IntraBot
   ```

#### 3. Create a feature branch:
   Use a clear naming convention:
   ```bash
   git checkout -b feature/new-feature
   ```
   
#### 4. Make & Commit Your Changes
   Write clean, documented code and commit:
   ```bash
   git add .
   git commit -m "✨ Added: your change description"
   ```
   
#### 5. Push to GitHub & Submit PR
   ```bash
   git push origin feature/your-feature-name
   ```
#### 6. Then go to your forked repo on GitHub and open a Pull Request.

---

## ⭐ Motivation

> 💡**PS:** If you found this project helpful or inspiring, please **[⭐ star the repository](https://github.com/arman61-hub/IntraBot)** — it keeps me motivated to build and share more awesome projects like this one!