# JanSeva AI: Hackathon Project Overview

## 1. Technology Stack

JanSeva AI is built using a modern, scalable, and AI-first technology stack designed for rapid development and production readiness.

### Frontend (Client)
- **Framework:** React 19 + Vite
- **Styling:** Tailwind CSS (with Glassmorphism UI)
- **Animations:** Framer Motion
- **Icons:** Lucide React
- **State Management:** React Context API
- **HTTP Client:** Axios
- **Routing:** React Router DOM

### Backend (Server)
- **Framework:** FastAPI (Python)
- **Authentication:** JWT (JSON Web Tokens), Passlib (Bcrypt hashing)
- **Database ORM:** SQLAlchemy
- **Database Engine:** PostgreSQL (with SQLite fallback for local development)
- **Server:** Uvicorn

### Artificial Intelligence (AI Engine)
- **Framework:** LangChain
- **Vector Database:** ChromaDB (for local vector storage)
- **LLM Engine:** Google Gemini (Gemini 1.5 Pro via API)
- **Embeddings:** Google `models/text-embedding-004` (for Retrieval Augmented Generation - RAG)

---

## 2. System Architecture

The application relies on a decoupled frontend and backend. The core intelligence comes from a Retrieval-Augmented Generation (RAG) pipeline embedded directly into the FastAPI server.

```mermaid
graph TD
    %% Define Styles
    classDef frontend fill:#3B82F6,stroke:#1D4ED8,stroke-width:2px,color:#fff;
    classDef backend fill:#10B981,stroke:#047857,stroke-width:2px,color:#fff;
    classDef database fill:#F59E0B,stroke:#B45309,stroke-width:2px,color:#fff;
    classDef ai fill:#8B5CF6,stroke:#5B21B6,stroke-width:2px,color:#fff;

    %% Nodes
    Client["Client Browser<br/>(React, Tailwind)"]:::frontend
    
    subgap Backend Layer
        API["FastAPI Server<br/>(REST APIs)"]:::backend
        Auth["Auth Service<br/>(JWT, Passlib)"]:::backend
        RAG["RAG Engine<br/>(LangChain)"]:::backend
    end
    
    subgap Data Layer
        PostgreSQL[("Relational DB<br/>(PostgreSQL/SQLite)")]:::database
        ChromaDB[("Vector DB<br/>(ChromaDB)")]:::database
    end
    
    subgap External APIs
        Gemini["Google Gemini API<br/>(LLM & Embeddings)"]:::ai
    end

    %% Connections
    Client <-->|HTTPS / JSON| API
    
    API <-->|Validates| Auth
    API <-->|SQLAlchemy ORM| PostgreSQL
    API <-->|Queries| RAG
    
    RAG <-->|Fetch relevant docs| ChromaDB
    RAG <-->|Generate Answer / Embed| Gemini
```

### Flow Summary
1. **User interaction:** The user updates their profile on the React frontend.
2. **Standard API:** FastAPI uses demographic info to run basic matching rules against the relational database and returns eligible schemes.
3. **AI Chatbot (RAG):** When the user asks a question, LangChain converts the question into an embedding via the Gemini API, retrieves mathematically similar government schemes from ChromaDB, and passes that context back to the Gemini LLM to generate a plain-language answer.

---

## 3. The Dataset

The initial dataset used to seed the application consists of authentic Indian government welfare schemes. These are stored relationally for the dashboard matching engine, and their text contents are vectorized into ChromaDB for the chatbot.

### Current Seeded Schemes

| Scheme Name | Category | Eligibility Target | Benefits | Required Documents |
| :--- | :--- | :--- | :--- | :--- |
| **PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)** | Agriculture | Small/marginal farmer families | ₹6,000 per year income support | Land records, Aadhaar, Bank account |
| **Ayushman Bharat (PM-JAY)** | Healthcare | Economically vulnerable families | Health insurance cover up to ₹5 lakh/family/year | Aadhaar, Ration card, Income certificate |
| **National Scholarship Portal — Post-Matric Scholarship** | Education | Students from SC/ST/OBC/minority/weaker backgrounds | Financial aid for post-matriculation education | Income certificate, Caste certificate, Mark sheets, Aadhaar |

### Data Model Structure
For each scheme, the database tracks the following fields:
- `id`: Unique Identifier
- `name`: Full Government Title
- `description`: Detailed breakdown of the scheme
- `eligibility`: Rules (Income, Age, Occupation, Demographics)
- `benefits`: What the citizen receives
- `documents`: Paperwork required to apply
- `state`: Geographic applicability (e.g., 'All', 'Telangana')
- `category`: Functional tag (Agriculture, Education, Healthcare, etc.)
- `officialLink`: Direct URL to the authentic government application portal

*Note: The dataset is designed to be easily expandable. Admins can insert new rows into the `schemes` table and run the vectorization script to instantly teach the AI about new government policies.*
