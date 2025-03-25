# Taxzy.ai Architecture

## System Overview

Taxzy.ai is a full-stack RAG (Retrieval-Augmented Generation) application built with a microservices architecture.

## Components

### 1. Frontend (React + Material UI)
- **Technology**: React.js 18, Material UI 5, Redux Toolkit
- **Responsibility**: User interface and client-side state management
- **Key Features**:
  - User authentication (login/register)
  - Conversation management
  - Real-time chat interface
  - Responsive design

### 2. Backend API (Node.js + Express)
- **Technology**: Node.js, Express.js, MongoDB, Mongoose
- **Responsibility**: Business logic, authentication, and data persistence
- **Key Features**:
  - RESTful API endpoints
  - JWT-based authentication
  - User and conversation management
  - Session handling
  - API rate limiting

### 3. Document Processor (Python + Flask)
- **Technology**: Python, Flask, LlamaIndex, Chroma
- **Responsibility**: RAG system and document processing
- **Key Features**:
  - Document ingestion and processing
  - Vector embeddings generation
  - Semantic search
  - LLM-powered response generation
  - Source citation

### 4. Databases
- **MongoDB**: User data and conversation history
- **Chroma**: Vector embeddings for document retrieval

## Data Flow

1. **User Authentication**:
   ```
   Frontend → Backend API → MongoDB → JWT Token → Frontend
   ```

2. **Chat Query**:
   ```
   Frontend → Backend API → Document Processor → Chroma → LLM → Response with Sources
   ```

3. **Document Upload**:
   ```
   Frontend → Backend API → Document Processor → PDF Processing → Chunking → Embeddings → Chroma
   ```

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user

### Chat
- `POST /api/chat/conversations` - Create new conversation
- `GET /api/chat/conversations` - Get all user conversations
- `GET /api/chat/conversations/:id` - Get specific conversation
- `POST /api/chat/conversations/:id/messages` - Send message
- `DELETE /api/chat/conversations/:id` - Delete conversation

### Document Processor
- `POST /api/query` - Query the RAG system
- `POST /api/documents/upload` - Upload new document
- `GET /api/documents/stats` - Get collection statistics

## Security

- **Authentication**: JWT tokens with HTTP-only cookies
- **Authorization**: Protected routes with middleware
- **Rate Limiting**: 100 requests per 15 minutes per IP
- **CORS**: Configured for specific origins
- **Input Validation**: Express-validator middleware
- **Security Headers**: Helmet.js

## Deployment

### Development
```bash
# Backend
cd backend && npm run dev

# Frontend
cd frontend && npm start

# Document Processor
cd document-processor && python app.py
```

### Production (Docker)
```bash
cd docker
docker-compose up -d
```

## Scaling Considerations

1. **Horizontal Scaling**: Multiple backend instances behind load balancer
2. **Caching**: Redis for session management and response caching
3. **CDN**: Static assets served via CDN
4. **Database Replication**: MongoDB replica sets
5. **Vector DB Optimization**: Chroma with optimized index parameters
