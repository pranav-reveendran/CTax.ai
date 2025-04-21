# Changelog

All notable changes to Taxzy.ai will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-15

### Added
- Initial release of Taxzy.ai
- User authentication system with JWT
- Chat interface for tax questions
- RAG system powered by LlamaIndex
- Support for F-1, J-1, H-1B, OPT, and CPT visa types
- Integration with California FTB documents
- Vector database using Chroma
- RESTful API backend with Express.js
- React frontend with Material UI
- Redux state management
- MongoDB database integration
- Docker containerization
- CI/CD pipeline with GitHub Actions
- Comprehensive documentation

### Features

#### Backend
- User registration and authentication
- Conversation management
- Session persistence
- Rate limiting
- Error handling
- Input validation
- Logging with Winston

#### Frontend
- Responsive Material UI design
- User dashboard
- Real-time chat interface
- Source citation display
- Conversation history
- Loading states
- Error handling

#### Document Processor
- PDF document processing
- Text extraction with PyMuPDF
- Semantic chunking
- Vector embeddings with BAAI/bge-base-en-v1.5
- Query processing with Llama 3.1 8B Instruct
- Source citation

#### Infrastructure
- Multi-container Docker setup
- MongoDB for user data
- Chroma for vector storage
- Automated CI/CD testing
- Production-ready deployment configurations

### Documentation
- Comprehensive README
- API documentation
- Architecture overview
- Setup guide
- Deployment guide
- Security policy
- Contributing guidelines
- FAQ
- Visa types guide

### Security
- JWT-based authentication
- Password hashing with bcrypt
- HTTPS support
- CORS configuration
- Rate limiting
- Input sanitization
- Security headers with Helmet.js

## [Unreleased]

### Planned Features
- Multi-factor authentication
- Document upload from users
- Export conversation to PDF
- Email notifications
- Advanced analytics
- Mobile application
- Multi-language support
- Voice input
- Real-time collaboration
- Integration with tax filing software

### Improvements
- Enhanced RAG accuracy
- Faster response times
- Better error messages
- More comprehensive test coverage
- Performance optimizations
- UI/UX enhancements
