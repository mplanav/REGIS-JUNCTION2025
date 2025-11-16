# Regis – Regulatory Intelligence System

Regis is an AI-powered regulatory intelligence system built for the **Bank of Finland Challenge (Junction 2025)**. It addresses the core challenge in financial supervision: regulations are massive, complex, and often inconsistent — making manual analysis slow and error‑prone.

---

## 🚨 Problem

Financial institutions must interpret thousands of pages of EU and national regulations. These documents frequently contain:
- Redundant requirements  
- Overlapping obligations  
- Conflicting legal interpretations  
- Highly technical, fragmented structures  

Manual review cannot scale to this complexity.

---

## ✅ Solution Overview

Regis transforms regulatory complexity into structured, machine‑generated intelligence using:
- **Chunking** of regulations into article‑/paragraph‑level units  
- **LLM‑based risk classification**  
- **Embedding generation**  
- **Semantic similarity analysis** for overlap detection  
- **Natural Language Inference (NLI)** for contradiction detection  

This creates a clear, analysable map of risks and inconsistencies across regulatory documents.

---

## 🧠 AI Pipeline

### 1. Document Chunking
Regulatory texts are parsed and broken into smaller segments with metadata, enabling consistent analysis.

### 2. Risk Classification
Zero‑shot LLMs assign risk labels such as:
AML, Cybersecurity, Governance, Privacy, Operational, Compliance, etc.

### 3. Embedding Generation
High‑dimensional embeddings capture the meaning of each chunk for comparison.

### 4. Overlap Detection
Cosine similarity identifies redundant or strongly related requirements.

### 5. Contradiction Detection
Using NLI models (e.g., **RoBERTa-MNLI**), the system classifies relationships as:
- Entailment  
- Contradiction  
- Neutral  

---

## ⚠️ Hackathon GPU Limitation

We successfully implemented the full pipeline — chunking, embedding generation, and NLI evaluation — on sample documents.

However, due to limited GPU and storage resources, we could not:
- host the complete embedding database, or  
- run large-scale vector similarity queries directly from the frontend.

To demonstrate the system realistically, our dashboard uses **mock values structured exactly like the real outputs** from our backend pipeline.

A production version will run on **Google Cloud’s managed LLM and vector search services** for true scalability.

---

## 🏗️ System Architecture

```
Raw Regulations
      │
 XML Parsing → Chunking → LLM Classification → Embeddings
      │                        │
      └────→ NLI Contradiction / Overlap Detection
                           │
                        FastAPI
                           │
                        React UI
```

---

## 🖥️ Tech Stack

### Backend
- FastAPI  
- Python  
- HuggingFace Transformers  
- RoBERTa-MNLI  
- pgvector (planned)  
- Google Cloud LLM APIs (production)  

### Frontend
- React (Vite)  
- Chart.js  
- REST API Integration  

---

## 🎯 Vision

Regis aims to:
- Automate risk extraction  
- Detect contradictions across EU & national regulations  
- Highlight regulatory redundancies  
- Provide clear visual intelligence for compliance teams  
- Enable scalable regulatory analysis  

**Regis — where compliance meets intelligence.**
