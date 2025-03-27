# Setup Guide

## Prerequisites

- Node.js >= 18.x
- Python >= 3.9
- MongoDB
- Docker (optional)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd CTax.ai
```

### 2. Backend Setup

```bash
cd backend
npm install
cp .env.example .env
# Edit .env with your configuration
mkdir logs
npm run dev
```

### 3. Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env
# Edit .env with your configuration
npm start
```

### 4. Document Processor Setup

```bash
cd document-processor
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
python app.py
```

### 5. Database Setup

**MongoDB**:
```bash
# Install MongoDB Community Edition
# Start MongoDB service
mongod --dbpath /path/to/data
```

**Chroma**:
```bash
# Chroma runs in-memory by default
# For persistent storage, configure in document-processor/.env
```

## Docker Setup

### 1. Build and Run All Services

```bash
cd docker
cp .env.example .env
# Edit .env with your configuration
docker-compose up -d
```

### 2. View Logs

```bash
docker-compose logs -f
```

### 3. Stop Services

```bash
docker-compose down
```

## Environment Variables

### Backend (.env)
```
NODE_ENV=development
PORT=5000
MONGODB_URI=mongodb://localhost:27017/taxzy-ai
JWT_SECRET=your-secret-key
CORS_ORIGIN=http://localhost:3000
DOCUMENT_PROCESSOR_URL=http://localhost:8000
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:5000/api
```

### Document Processor (.env)
```
FLASK_ENV=development
FLASK_PORT=8000
CHROMA_HOST=localhost
CHROMA_PORT=8001
HUGGINGFACE_API_KEY=your-api-key
```

## Initial Data Setup

### 1. Upload Tax Documents

```bash
curl -X POST http://localhost:8000/api/documents/upload \
  -F "file=@/path/to/california-tax-guide.pdf"
```

### 2. Verify Document Processing

```bash
curl http://localhost:8000/api/documents/stats
```

## Testing

### Backend Tests
```bash
cd backend
npm test
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Troubleshooting

### MongoDB Connection Issues
- Ensure MongoDB is running
- Check connection string in .env
- Verify firewall settings

### Document Processor Issues
- Check Python version compatibility
- Verify all dependencies are installed
- Check Chroma connection settings

### Frontend Build Issues
- Clear node_modules and reinstall
- Check Node.js version
- Verify environment variables

## Production Deployment

### AWS Deployment
1. Set up EC2 instances or ECS clusters
2. Configure RDS for MongoDB or use MongoDB Atlas
3. Set up S3 for document storage
4. Configure CloudFront for frontend CDN
5. Use Application Load Balancer for backend

### Azure Deployment
1. Use Azure App Service for backend
2. Azure Static Web Apps for frontend
3. Azure Cosmos DB for MongoDB
4. Azure Blob Storage for documents

## Support

For issues or questions:
- Check documentation in `/docs`
- Open an issue on GitHub
- Contact the development team
