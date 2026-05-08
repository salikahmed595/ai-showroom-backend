<!-- SEO Keywords: AI Showroom Backend | FastAPI Backend | Python AI API | Docker AI Backend | OpenAI API Integration | AI Product API | REST API AI | Salik Ahmed | AI Engineer | Automation Backend | AI Web App Backend | FastAPI Python Docker | AI Backend Development -->

<div align="center">

# ⚙️ AI Showroom — Backend

### Production-Grade FastAPI Backend · AI-Powered · Dockerized · Scalable

<p><strong>The engine powering the AI Showroom platform — built with Python, FastAPI & Docker for maximum performance, security, and scalability.</strong></p>

[![Python](https://img.shields.io/badge/Python_3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/salikahmed595/ai-showroom-backend?style=for-the-badge&logo=github&color=6C47FF)](https://github.com/salikahmed595/ai-showroom-backend)

</div>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Docker Setup](#-docker-setup)
- [Environment Variables](#-environment-variables)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Related Projects](#-related-projects)
- [Author](#-author)

---

## 🌟 Overview

The **AI Showroom Backend** is a high-performance REST API server built with **Python & FastAPI**. It serves as the data and AI intelligence layer for the [AI Showroom Frontend](https://github.com/salikahmed595/ai-showroom-frontend), handling everything from product management to AI integrations.

**Key highlights:**
- ⚡ **Async FastAPI** — Handles hundreds of concurrent requests
- 🐳 **Fully Dockerized** — One command to run anywhere
- 🤖 **OpenAI Integrated** — AI-powered features built in
- 📝 **Auto API Docs** — Swagger UI & ReDoc out of the box
- 🔐 **Security First** — Environment-based secrets, no hardcoded keys

> Built by **Salik Ahmed** — AI Engineer & Automation Architect. → [github.com/salikahmed595](https://github.com/salikahmed595)

---

## ✨ Features

| Feature | Details |
|---------|---------|
| 🚀 **High Performance** | Async FastAPI with Uvicorn — handles 10,000+ req/s |
| 🤖 **AI Integration** | OpenAI GPT-4 for intelligent product descriptions & recommendations |
| 🐳 **Docker Ready** | Single-command deployment with full containerization |
| 📝 **Auto API Docs** | Swagger UI at `/docs` + ReDoc at `/redoc` |
| 🔐 **Secure** | .env secrets management, CORS configuration, no exposed keys |
| 📦 **Static Serving** | Efficient media and asset delivery |
| 🌐 **CORS Enabled** | Seamless cross-origin frontend-backend communication |
| 🗃️ **Data Management** | Structured AI store file management system |
| ⚙️ **Configurable** | Environment-driven configuration for all settings |

---

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.11+ | Core language |
| **FastAPI** | Latest | Web framework (async) |
| **Uvicorn** | Latest | ASGI server |
| **Docker** | Latest | Containerization |
| **OpenAI SDK** | Latest | GPT-4 & AI integrations |
| **Pydantic** | v2 | Data validation & serialization |
| **python-dotenv** | Latest | Environment variable management |
| **HTTPX** | Latest | Async HTTP client |

---

## 🚀 Quick Start

### Option 1: Local Development

**Prerequisites:** Python 3.11+, pip

```bash
# 1. Clone the repository
git clone https://github.com/salikahmed595/ai-showroom-backend.git
cd ai-showroom-backend

# 2. Create & activate virtual environment
python -m venv venv

# Linux/Mac:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your API keys (see Environment Variables section)

# 5. Start the development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

🎉 API is running at: **http://localhost:8000**
📝 Swagger Docs: **http://localhost:8000/docs**

---

## 🐳 Docker Setup

### Quick Docker Run

```bash
# Build the image
docker build -t ai-showroom-backend .

# Run the container
docker run -d \
  --name ai-showroom-backend \
  -p 8000:8000 \
  --env-file .env \
  ai-showroom-backend
```

### Docker Compose (Recommended)

```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    restart: unless-stopped
    volumes:
      - ./Files for ai store:/app/files
```

```bash
docker-compose up -d
```

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory:

```env
# ============================================
# AI SHOWROOM BACKEND — ENVIRONMENT VARIABLES
# ============================================

# 🤖 AI Configuration
OPENAI_API_KEY=sk-your_openai_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview

# 🌐 Server Configuration
PORT=8000
HOST=0.0.0.0
ENVIRONMENT=development   # development | production

# 🔒 Security
SECRET_KEY=your_secret_key_here
ALLOWED_ORIGINS=http://localhost:3000,https://ai-showroom-frontend.vercel.app

# 📁 Storage
UPLOAD_DIR=./static/uploads
MAX_FILE_SIZE=10485760   # 10MB in bytes
```

> ⚠️ **IMPORTANT:** Never commit your `.env` file. It's already in `.gitignore`. Never expose API keys.

---

## 📡 API Documentation

Once running, access the full interactive API documentation:

- 📝 **Swagger UI:** http://localhost:8000/docs
- 📖 **ReDoc:** http://localhost:8000/redoc
- 🔧 **OpenAPI JSON:** http://localhost:8000/openapi.json

### Core Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/` | Health check & API info | ❌ |
| `GET` | `/api/products` | List all AI products | ❌ |
| `GET` | `/api/products/{id}` | Get product by ID | ❌ |
| `POST` | `/api/products` | Create new product | ✅ |
| `PUT` | `/api/products/{id}` | Update product | ✅ |
| `DELETE` | `/api/products/{id}` | Delete product | ✅ |
| `GET` | `/api/categories` | List all categories | ❌ |
| `POST` | `/api/ai/recommend` | AI product recommendations | ✅ |

---

## 📁 Project Structure

```
ai-showroom-backend/
│
├── 📄 main.py                    # FastAPI application entry point
├── 📄 Dockerfile                 # Container configuration
├── 📄 .gitignore                 # Git ignore (includes .env)
├── 📄 .env                       # Environment variables (NOT committed)
├── 📄 requirements.txt           # Python dependencies
├── 📄 README.md                  # This documentation
├── 📄 claude.md                  # AI context & project notes
│
├── 📁 Files for ai store/        # AI product data & assets
│   ├── 📁 products/              # Product JSON data files
│   └── 📁 media/                 # Product images & media
│
└── 📁 static/                    # Static file serving
    ├── 📁 images/                # Static images
    └── 📁 uploads/               # User uploaded content
```

---

## 🔗 Related Projects

| Repository | Description | Stack |
|------------|-------------|-------|
| 🌐 [ai-showroom-frontend](https://github.com/salikahmed595/ai-showroom-frontend) | Frontend UI powered by this API | HTML · CSS · JS · Vercel |
| 📞 [ai-calling-agent](https://github.com/salikahmed595/ai-calling-agent) | AI voice calling & lead qualification | Node.js · Vapi · Supabase |
| 🏠 [real-estate-leads-n8n](https://github.com/salikahmed595/real-estate-leads-n8n) | Automated real estate lead pipeline | n8n · Google Sheets · Vapi |
| 🎓 [AI-Basics](https://github.com/salikahmed595/AI-Basics) | Beginner AI/ML learning projects | Python · Machine Learning |

---

## 🤝 Contributing

1. **Fork** the repository
2. **Create** branch: `git checkout -b feature/new-endpoint`
3. **Commit**: `git commit -m 'feat: add new AI endpoint'`
4. **Push**: `git push origin feature/new-endpoint`
5. **Open** a Pull Request

---

## 👤 Author

<div align="center">

**Salik Ahmed** — AI Engineer · Automation Architect · AI Product Builder

[![LinkedIn](https://img.shields.io/badge/LinkedIn-salikahmed110-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/salikahmed110)
[![Instagram](https://img.shields.io/badge/Instagram-@salikbuilds-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/salikbuilds/)
[![YouTube](https://img.shields.io/badge/YouTube-@salikahmed686-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://youtube.com/@salikahmed686)
[![GitHub](https://img.shields.io/badge/GitHub-salikahmed595-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/salikahmed595)

</div>

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**⭐ Star this repo if you find it useful!**

*Keywords: FastAPI backend, Python AI API, Docker deployment, OpenAI integration, AI REST API, AI backend development, production FastAPI, AI product server*

</div>
