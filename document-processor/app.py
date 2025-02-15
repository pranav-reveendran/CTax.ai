from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
from src.services.rag_service import RAGService
from src.services.document_processor import DocumentProcessor

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize services
rag_service = RAGService()
doc_processor = DocumentProcessor()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'document-processor',
        'version': '1.0.0'
    }), 200

@app.route('/api/query', methods=['POST'])
def query():
    """
    Query the RAG system with a user question

    Expected JSON body:
    {
        "query": "What are the tax implications for F-1 students?",
        "context": {
            "visaType": "F-1",
            "taxYear": 2024,
            "state": "California"
        },
        "conversationHistory": []
    }
    """
    try:
        data = request.get_json()

        if not data or 'query' not in data:
            return jsonify({
                'error': 'Query is required'
            }), 400

        user_query = data['query']
        context = data.get('context', {})
        conversation_history = data.get('conversationHistory', [])

        logger.info(f"Processing query: {user_query[:100]}...")

        # Get response from RAG service
        response = rag_service.query(
            query=user_query,
            context=context,
            conversation_history=conversation_history
        )

        return jsonify({
            'success': True,
            'answer': response['answer'],
            'sources': response['sources'],
            'confidence': response.get('confidence', 0.0)
        }), 200

    except Exception as e:
        logger.error(f"Query error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An error occurred processing your query',
            'details': str(e) if os.getenv('FLASK_ENV') == 'development' else None
        }), 500

@app.route('/api/documents/upload', methods=['POST'])
def upload_document():
    """Upload and process a new document"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'error': 'No file provided'
            }), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({
                'error': 'No file selected'
            }), 400

        # Process document
        result = doc_processor.process_document(file)

        return jsonify({
            'success': True,
            'message': 'Document processed successfully',
            'documentId': result['document_id'],
            'chunks': result['chunks_created']
        }), 201

    except Exception as e:
        logger.error(f"Document upload error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An error occurred processing the document'
        }), 500

@app.route('/api/documents/stats', methods=['GET'])
def document_stats():
    """Get statistics about indexed documents"""
    try:
        stats = rag_service.get_collection_stats()

        return jsonify({
            'success': True,
            'stats': stats
        }), 200

    except Exception as e:
        logger.error(f"Stats error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An error occurred fetching stats'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 8000))
    debug = os.getenv('FLASK_ENV') == 'development'

    logger.info(f"Starting Document Processor service on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
