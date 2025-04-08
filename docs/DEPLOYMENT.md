# Deployment Guide

## Table of Contents
1. [Production Checklist](#production-checklist)
2. [Environment Configuration](#environment-configuration)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Security Considerations](#security-considerations)
6. [Monitoring](#monitoring)

## Production Checklist

Before deploying to production:

- [ ] All environment variables configured
- [ ] MongoDB database set up and secured
- [ ] Chroma vector database configured
- [ ] SSL certificates obtained
- [ ] Domain names configured
- [ ] Firewall rules configured
- [ ] Backup strategy implemented
- [ ] Monitoring tools set up
- [ ] Error tracking configured
- [ ] Load testing completed

## Environment Configuration

### Required Environment Variables

#### Backend
```env
NODE_ENV=production
PORT=5000
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/taxzy-ai
JWT_SECRET=<strong-random-secret>
JWT_EXPIRE=7d
CORS_ORIGIN=https://yourdomain.com
DOCUMENT_PROCESSOR_URL=https://processor.yourdomain.com
```

#### Frontend
```env
REACT_APP_API_URL=https://api.yourdomain.com/api
REACT_APP_ENV=production
```

#### Document Processor
```env
FLASK_ENV=production
FLASK_PORT=8000
CHROMA_HOST=chroma
CHROMA_PORT=8000
HUGGINGFACE_API_KEY=<your-api-key>
```

## Docker Deployment

### Build Images

```bash
# Backend
docker build -t taxzy-backend:latest -f backend/Dockerfile ./backend

# Frontend
docker build -t taxzy-frontend:latest -f frontend/Dockerfile ./frontend

# Document Processor
docker build -t taxzy-processor:latest -f document-processor/Dockerfile ./document-processor
```

### Run with Docker Compose

```bash
cd docker
docker-compose up -d
```

### View Logs

```bash
docker-compose logs -f
```

### Scale Services

```bash
docker-compose up -d --scale backend=3
```

## Cloud Deployment

### AWS Deployment

#### Architecture
- **Frontend**: S3 + CloudFront
- **Backend**: ECS Fargate or EC2 with Auto Scaling
- **Database**: MongoDB Atlas or DocumentDB
- **Vector DB**: EC2 instance
- **Load Balancer**: Application Load Balancer

#### Steps

1. **Set up VPC and Security Groups**
```bash
aws ec2 create-vpc --cidr-block 10.0.0.0/16
```

2. **Deploy Backend to ECS**
```bash
# Create ECR repositories
aws ecr create-repository --repository-name taxzy-backend

# Push images
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/taxzy-backend:latest

# Create ECS cluster and services
aws ecs create-cluster --cluster-name taxzy-cluster
```

3. **Deploy Frontend to S3 + CloudFront**
```bash
# Build frontend
cd frontend && npm run build

# Upload to S3
aws s3 sync build/ s3://taxzy-frontend

# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id <id> --paths "/*"
```

### Azure Deployment

#### Architecture
- **Frontend**: Azure Static Web Apps
- **Backend**: Azure Container Instances or App Service
- **Database**: MongoDB Atlas or Cosmos DB
- **Vector DB**: Azure Container Instances

#### Steps

1. **Deploy Frontend**
```bash
az staticwebapp create \
  --name taxzy-frontend \
  --resource-group taxzy-rg \
  --source https://github.com/yourorg/taxzy-ai \
  --location "westus2" \
  --branch main \
  --app-location "/frontend" \
  --api-location "" \
  --output-location "build"
```

2. **Deploy Backend**
```bash
az containerapp up \
  --name taxzy-backend \
  --resource-group taxzy-rg \
  --location westus2 \
  --environment taxzy-env \
  --image <your-acr>.azurecr.io/taxzy-backend:latest \
  --target-port 5000 \
  --ingress external
```

## Security Considerations

### SSL/TLS Configuration

Use Let's Encrypt for free SSL certificates:

```bash
certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Environment Secrets

Use secret management services:
- **AWS**: AWS Secrets Manager
- **Azure**: Azure Key Vault
- **GCP**: Secret Manager

### API Security

- Enable rate limiting
- Use HTTPS only
- Implement CORS properly
- Sanitize all inputs
- Use helmet.js for security headers

## Monitoring

### Application Monitoring

**Recommended Tools**:
- New Relic
- Datadog
- Application Insights (Azure)
- CloudWatch (AWS)

### Log Aggregation

**Recommended Tools**:
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Splunk
- CloudWatch Logs

### Error Tracking

**Recommended Tools**:
- Sentry
- Rollbar
- Bugsnag

### Health Checks

Set up health check endpoints:

```javascript
// Backend health check
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
  });
});
```

## Backup Strategy

### Database Backups

**MongoDB**:
```bash
# Daily automated backups
mongodump --uri="mongodb+srv://..." --out=/backups/$(date +%Y%m%d)
```

**Chroma**:
- Regular snapshots of vector store data
- Store in S3 or Azure Blob Storage

### Disaster Recovery

- Maintain backups in multiple regions
- Test restore procedures regularly
- Document recovery procedures
- Set RTO and RPO targets

## Performance Optimization

### Frontend
- Enable gzip compression
- Minimize bundle size
- Use CDN for static assets
- Implement lazy loading
- Cache API responses

### Backend
- Enable response compression
- Implement caching (Redis)
- Optimize database queries
- Use connection pooling
- Horizontal scaling

### Database
- Index frequently queried fields
- Use read replicas
- Implement query optimization
- Monitor slow queries

## Scaling Strategy

### Horizontal Scaling
- Use load balancers
- Implement stateless services
- Use shared session storage (Redis)
- Auto-scaling based on metrics

### Vertical Scaling
- Monitor resource usage
- Upgrade instance sizes as needed
- Optimize resource allocation

## Support

For deployment issues:
- Check logs first
- Verify all environment variables
- Test connectivity between services
- Review security group rules
- Contact support team
