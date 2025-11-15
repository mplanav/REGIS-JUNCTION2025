
# Backend Architecture – RiskReg Navigator

This document explains how the backend is structured, how to run it, and how it interacts with PostgreSQL + pgvector and DataCrunch.

---

## 📁 Project Structure

```
backend/
├── docker-compose.yml
├── requirements.txt
└── app/
    ├── Dockerfile
    ├── main.py
    ├── core/
    │   └── config.py
    ├── db/
    │   ├── session.py
    │   ├── models/
    │   └── schemas/
    ├── api/
    │   ├── router_documents.py
    │   ├── router_chunks.py
    │   ├── router_chat.py
    │   └── router_analytics.py
    ├── ingestion/
    │   ├── xml_scanner.py
    │   ├── xml_parser.py
    │   └── chunker.py
    └── nlp/
        ├── embeddings.py
        ├── risk_classifier.py
        └── contradictions.py
```

---

## 🚀 Setup Instructions

### 1. Install Docker & Docker Compose
Make sure Docker is installed on the DataCrunch server.

### 2. Project Clone
```
git clone <your_repo>
cd backend
```

### 3. Create `.env` file inside `backend/`
```
DATABASE_URL=postgresql+psycopg2://postgres:postgres@postgres:5432/riskreg
OPENAI_API_KEY=YOUR_KEY_HERE
```

---

## 🐳 Running the backend

### 1. Build and start all services
```
docker-compose up --build -d
```

### 2. Access FastAPI documentation
```
http://<YOUR-DATACRUNCH-IP>:8000/docs
```

### 3. Restart services
```
docker-compose restart
```

### 4. Stop
```
docker-compose down
```

---

## 🗄 Database Structure

The backend uses:

- **PostgreSQL**
- **pgvector extension** for embeddings
- SQLAlchemy models:
  - `Document`
  - `Chunk`
  - (future) `RequirementPair`

Connections run through `backend/app/db/session.py`.

---

## 📂 Dataset Location

Place the dataset under:

```
/home/<user>/project/data/
```

This folder is mounted into the FastAPI container automatically in `docker-compose.yml`.

Recommended structure:

```
data/
    gold/
        eu_leg/
        financial_regulation/
        national_laws/
    silver/
    bronze/
```

---

## 🔌 API Overview

The backend exposes:

- `/documents/*` → document listing & metadata  
- `/chunks/*` → chunk query + semantic search  
- `/chat/*` → chatbot interface  
- `/analytics/*` → dashboards & regulatory metrics  

Routers are located in `backend/app/api/`.

---

## 🧠 NLP Layer

Located in `backend/app/nlp/`.

Includes:

- `embeddings.py` → vector generation  
- `risk_classifier.py` → multilabel risk classification via LLM  
- `contradictions.py` → NLI-based contradiction detection  

These functions are used after chunking to enrich each document.

---

## ⚙️ Ingestion Pipeline

Located in `backend/app/ingestion/`.

Steps:
1. `xml_scanner.py` → detect all XML files  
2. `xml_parser.py` → extract metadata & text  
3. `chunker.py` → split text into semantic units (chunks)

---

## 🤝 Contributions

Each backend component is modular:
- ingestion
- database
- NLP
- API routing

This allows multiple team members to work in parallel.

---

## 🛠 Troubleshooting

### Check logs:
```
docker logs riskreg-backend
docker logs riskreg-postgres
```

### Rebuild everything:
```
docker-compose down -v
docker-compose up --build
```

---