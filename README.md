# 🔧 AI Showroom — Backend

> The powerful Python/FastAPI backend driving the AI Showroom platform. Serving intelligent APIs, managing AI product data, and enabling real-time automation workflows.

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

---

## 🌟 Overview

The **AI Showroom Backend** is a robust, scalable API server built with Python. It powers the AI Showroom platform by handling product data management, AI integrations, user requests, and automation workflows. Designed for high performance with containerized deployment via Docker.

This backend connects to the frontend at [ai-showroom-frontend](https://github.com/salikahmed595/ai-showroom-frontend) and integrates with various AI services including OpenAI, Vapi, and n8n.

---

## ✨ Features

- 🚀 **High-Performance REST API** — FastAPI with async support for blazing-fast responses
- 🤖 **AI Integrations** — OpenAI GPT, embedding models, and custom AI pipelines
- 🐳 **Dockerized** — Containerized deployment for easy scaling and portability
- 📦 **Static File Serving** — Efficient media and asset delivery
- 🔐 **Secure by Design** — Environment variable management, .gitignore for secrets
- 📊 **Structured Data** — Organized file management for AI store assets
- 🌐 **CORS Enabled** — Seamless frontend-backend communication
- 📝 **Auto-Documentation** — Swagger UI & ReDoc built into FastAPI

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.11+ | Core programming language |
| FastAPI | High-performance web framework |
| Docker | Containerization & deployment |
| Uvicorn | ASGI server |
| OpenAI API | AI model integrations |
| Pydantic | Data validation & serialization |
| python-dotenv | Environment variable management |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Docker (optional, for containerized setup)
- pip or uv package manager

### Installation (Local)

```bash
# Clone the repository
git clone https://github.com/salikahmed595/ai-showroom-backend.git
cd ai-showroom-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Installation (Docker)

```bash
# Build and run with Docker
docker build -t ai-showroom-backend .
docker run -d -p 8000:8000 --env-file .env ai-showroom-backend

# Or use Docker Compose (if available)
docker-compose up -d
```

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory:

```env
# AI API Keys
OPENAI_API_KEY=your_openai_api_key
VAPI_API_KEY=your_vapi_api_key

# Database
DATABASE_URL=your_database_url

# Server
PORT=8000
ENVIRONMENT=development

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://ai-showroom-frontend.vercel.app
```

> ⚠️ Never commit your `.env` file. It is already in `.gitignore`.

---

## 📁 Project Structure

```
ai-showroom-backend/
│
├── main.py                     # FastAPI app entry point
├── Dockerfile                  # Container configuration
├── .gitignore                  # Git ignore rules
├── .env                        # Environment variables (not committed)
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── claude.md                   # AI context file
│
├── Files for ai store/         # AI product assets & data
│   ├── products/
│   └── media/
│
└── static/                     # Static file serving
    └── images/
```

---

## 📡 API Endpoints

Once running, access the auto-generated API docs:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/api/products` | Get all AI products |
| GET | `/api/products/{id}` | Get product by ID |
| POST | `/api/products` | Create new product |
| PUT | `/api/products/{id}` | Update product |
| DELETE | `/api/products/{id}` | Delete product |

---

## 🔗 Related Repositories

| Repository | Description |
|------------|-------------|
| 🌐 [ai-showroom-frontend](https://github.com/salikahmed595/ai-showroom-frontend) | Frontend UI for the AI Showroom |
| 📞 [ai-calling-agent](https://github.com/salikahmed595/ai-calling-agent) | Automated AI voice calling system |
| 🎓 [AI-Basics](https://github.com/salikahmed595/AI-Basics) | Beginner-friendly AI/ML resources |
| 🏠 [real-estate-leads-n8n](https://github.com/salikahmed595/real-estate-leads-n8n) | n8n automation for lead management |

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/new-api-endpoint`
3. Commit your changes: `git commit -m 'Add new endpoint'`
4. Push to branch: `git push origin feature/new-api-endpoint`
5. Open a Pull Request

---

## 👤 Author

**Salik Ahmed** — AI Engineer & Automation Architect

> Specializing in AI product development, voice agents, and intelligent automation systems.

- 🐙 GitHub: [@salikahmed595](https://github.com/salikahmed595)
- 💼 LinkedIn: [salikahmed110](https://linkedin.com/in/salikahmed110)
- 📺 YouTube: [@salikahmed686](https://youtube.com/@salikahmed686)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <strong>⭐ Star this repo if you find it useful!</strong><br/>
  Made with ❤️ and AI by <a href="https://github.com/salikahmed595">Salik Ahmed</a>
</div>
