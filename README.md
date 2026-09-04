# ⚡ OmniTransform: GenAI Platform for Automated Content Transformation
> **Problem Statement ID:** 26154 | **Category:** Generative AI & Automation  
> **Architecture:** 100% Privacy-Preserving, Air-Gapped Local LLM Engine (Ollama)

---

## 📌 Executive Overview
Enterprises, cybersecurity units, and government institutions frequently produce dense reports, advisories, policy updates, and research papers. Manually tailoring this content for different stakeholders (executives, technical engineers, public media) is resource-intensive and error-prone.

**OmniTransform** is an automated, multimodal content transformation platform. With a single click, an operator ingests raw documents and produces **seven cross-platform communication deliverables** conditioned on customizable parameters (Audience, Tone, Objective, and Detail Level).

---

## 🌟 Key Features
- **7-in-1 Parallel Generation:** Generates LinkedIn posts, Twitter/X threads (<280 char validation), Structured Security Advisories, Executive Summaries (BLUF), Video Storyboard packages, Infographic blueprints, and Presentation decks simultaneously.
- **Real PowerPoint (.pptx) Export:** Compiles slide titles, bullet points, visual concepts, and speaker notes directly into an editable 16:9 `.pptx` file.
- **100% Air-Gapped Privacy:** Powered by local Ollama (`llama3.1`). Zero data exfiltration—ideal for classified or proprietary enterprise documents.
- **Deterministic Schema Enforcement:** Uses strict Pydantic v2 schemas to eliminate LLM hallucinations and malformed output.
- **Multi-Modal Ingestion:** Ingests `.pdf`, `.docx`, `.txt`, and raw text prompts.

---

## 🛠️ Tech Stack
| Component | Technology | Role |
| :--- | :--- | :--- |
| **Frontend** | React 18, Vite, Tailwind CSS, Lucide Icons | Responsive multi-tab dashboard & card viewers |
| **Backend Gateway** | FastAPI, Uvicorn, Python 3.11 | High-throughput REST API with async processing |
| **Local LLM Engine** | Ollama (`llama3.1:8b` / `llama3.2:3b`) | Local inference with JSON Schema decoding |
| **Document Parsers** | `pypdf`, `python-docx` | Text extraction and metadata normalization |
| **Export Engines** | `python-pptx`, `reportlab` | Native Microsoft PowerPoint generation |
| **Local Database** | SQLite (`sqlite3`) | Transformation history and run tracking |

---

## 🚀 Quick Start (3 Steps)

### Step 1: Start Local Ollama
Download Ollama from [ollama.com](https://ollama.com) and pull the model:
```bash
ollama run llama3.1
