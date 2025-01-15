# Taxzy.ai - California Tax Assistant for International Students

A specialized Retrieval-Augmented Generation (RAG) chatbot providing accurate, sourced California tax information for international students and employees on various visa types (F-1, J-1, H-1B, OPT/CPT).

## Project Overview

Taxzy.ai is a modern web application that helps international students navigate complex California tax regulations by providing AI-powered assistance grounded in official California Franchise Tax Board (FTB) documents.

## Features

- **Responsive Web Interface**: Built with React.js and Material UI
- **Accurate Tax Information**: RAG-powered responses sourced from official FTB documents
- **Visa-Specific Guidance**: Specialized content for F-1, J-1, H-1B, OPT/CPT visa holders
- **Source Citations**: All responses include references to official documents
- **Stateful Conversations**: Session management for context-aware interactions
- **Secure Authentication**: JWT-based user authentication

## Technology Stack

### Frontend
- React.js
- Material UI
- Redux (state management)
- Axios (API requests)

### Backend
- Node.js
- Express.js
- RESTful API architecture
- JWT authentication

### Database
- MongoDB (user data and sessions)
- Chroma (vector database for embeddings)

### NLP/ML
- LlamaIndex
- BAAI/bge-base-en-v1.5 embeddings
- Llama 3.1 8B Instruct

### Document Processing
- PyMuPDF/PyPDF2
- Microservices architecture

### Deployment
- Docker containers
- CI/CD with GitHub Actions
- Cloud hosting (AWS/Azure)

## Project Structure

```
taxzy.ai/
├── frontend/           # React application
├── backend/            # Node.js/Express API
├── document-processor/ # Python document processing service
├── docker/             # Docker configuration
├── docs/               # Documentation
└── .github/            # CI/CD workflows
```

## Getting Started

### Prerequisites
- Node.js >= 18.x
- Python >= 3.9
- MongoDB
- Docker (optional)

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd CTax.ai
```

2. Install frontend dependencies
```bash
cd frontend
npm install
```

3. Install backend dependencies
```bash
cd ../backend
npm install
```

4. Install document processor dependencies
```bash
cd ../document-processor
pip install -r requirements.txt
```

5. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

6. Start the application
```bash
# Start backend
cd backend
npm start

# Start frontend (in a new terminal)
cd frontend
npm start

# Start document processor (in a new terminal)
cd document-processor
python app.py
```

## Development

- Frontend runs on `http://localhost:3000`
- Backend API runs on `http://localhost:5000`
- Document processor runs on `http://localhost:8000`

## Contributing

This project was developed as part of academic work at San Jose State University.

## License

MIT License

## Contact

For questions or support, please open an issue in the repository.
