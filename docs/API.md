# API Documentation

## Base URL

- Development: `http://localhost:5000/api`
- Production: `https://api.taxzy.ai/api`

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

## Endpoints

### Authentication

#### Register User

```http
POST /auth/register
```

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "visaType": "F-1",
  "university": "San Jose State University"
}
```

**Response:**
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "user_id",
    "name": "John Doe",
    "email": "john@example.com",
    "visaType": "F-1",
    "role": "user"
  }
}
```

#### Login

```http
POST /auth/login
```

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "user_id",
    "name": "John Doe",
    "email": "john@example.com",
    "visaType": "F-1",
    "role": "user"
  }
}
```

#### Get Current User

```http
GET /auth/me
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "user_id",
    "name": "John Doe",
    "email": "john@example.com",
    "visaType": "F-1",
    "university": "San Jose State University"
  }
}
```

### Chat

#### Create Conversation

```http
POST /chat/conversations
```

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "title": "Tax Questions 2024",
  "visaType": "F-1",
  "taxYear": 2024
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "_id": "conversation_id",
    "user": "user_id",
    "title": "Tax Questions 2024",
    "context": {
      "visaType": "F-1",
      "taxYear": 2024,
      "state": "California"
    },
    "messages": [],
    "createdAt": "2024-01-15T10:30:00.000Z"
  }
}
```

#### Get All Conversations

```http
GET /chat/conversations
```

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "count": 5,
  "data": [
    {
      "_id": "conversation_id",
      "title": "Tax Questions 2024",
      "metadata": {
        "totalMessages": 10,
        "lastMessageAt": "2024-01-15T11:00:00.000Z"
      },
      "updatedAt": "2024-01-15T11:00:00.000Z"
    }
  ]
}
```

#### Send Message

```http
POST /chat/conversations/:id/messages
```

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "message": "What are the tax filing requirements for F-1 students in California?"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "conversationId": "conversation_id",
    "message": "F-1 students in California must file federal tax returns...",
    "sources": [
      {
        "documentName": "California Tax Guide.pdf",
        "pageNumber": 15,
        "excerpt": "F-1 students are considered nonresident aliens...",
        "relevanceScore": 0.92
      }
    ]
  }
}
```

### Document Processor

#### Query RAG System

```http
POST /api/query
```

**Request Body:**
```json
{
  "query": "What is the California state tax rate?",
  "context": {
    "visaType": "F-1",
    "taxYear": 2024,
    "state": "California"
  },
  "conversationHistory": []
}
```

**Response:**
```json
{
  "success": true,
  "answer": "California state tax rates for 2024 range from 1% to 12.3%...",
  "sources": [
    {
      "documentName": "FTB Publication 1032.pdf",
      "pageNumber": 8,
      "excerpt": "Tax rates for 2024...",
      "relevanceScore": 0.95
    }
  ],
  "confidence": 0.92
}
```

#### Upload Document

```http
POST /api/documents/upload
```

**Request:**
```
Content-Type: multipart/form-data
file: <PDF file>
```

**Response:**
```json
{
  "success": true,
  "message": "Document processed successfully",
  "documentId": "doc_id_hash",
  "chunks": 45
}
```

## Error Responses

All errors follow this format:

```json
{
  "success": false,
  "error": "Error message",
  "details": "Additional error details (development only)"
}
```

### Common Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `429` - Too Many Requests
- `500` - Internal Server Error

## Rate Limiting

- 100 requests per 15 minutes per IP address
- Rate limit headers included in response:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`
