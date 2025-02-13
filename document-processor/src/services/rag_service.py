import os
import logging
from typing import List, Dict, Any
from llama_index.core import VectorStoreIndex, ServiceContext, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface import HuggingFaceInferenceAPI
import chromadb

logger = logging.getLogger(__name__)

class RAGService:
    """
    Retrieval-Augmented Generation service for querying California tax documents
    """

    def __init__(self):
        self.collection_name = os.getenv('CHROMA_COLLECTION_NAME', 'california-tax-documents')
        self.embedding_model_name = os.getenv('EMBEDDING_MODEL', 'BAAI/bge-base-en-v1.5')
        self.llm_model_name = os.getenv('LLM_MODEL', 'meta-llama/Llama-3.1-8B-Instruct')

        # Initialize embedding model
        logger.info(f"Loading embedding model: {self.embedding_model_name}")
        self.embed_model = HuggingFaceEmbedding(
            model_name=self.embedding_model_name
        )

        # Initialize LLM
        logger.info(f"Initializing LLM: {self.llm_model_name}")
        self.llm = HuggingFaceInferenceAPI(
            model_name=self.llm_model_name,
            token=os.getenv('HUGGINGFACE_API_KEY')
        )

        # Initialize Chroma client
        self.chroma_client = chromadb.HttpClient(
            host=os.getenv('CHROMA_HOST', 'localhost'),
            port=int(os.getenv('CHROMA_PORT', 8001))
        )

        # Get or create collection
        self.collection = self.chroma_client.get_or_create_collection(
            name=self.collection_name
        )

        # Create vector store
        self.vector_store = ChromaVectorStore(chroma_collection=self.collection)

        # Create storage context
        self.storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store
        )

        # Create service context
        self.service_context = ServiceContext.from_defaults(
            embed_model=self.embed_model,
            llm=self.llm
        )

        # Create index
        try:
            self.index = VectorStoreIndex.from_vector_store(
                vector_store=self.vector_store,
                service_context=self.service_context
            )
            logger.info("RAG service initialized successfully")
        except Exception as e:
            logger.warning(f"Could not load existing index: {e}")
            self.index = None

    def query(
        self,
        query: str,
        context: Dict[str, Any],
        conversation_history: List[Dict[str, str]] = None,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Query the RAG system with context-aware retrieval

        Args:
            query: User's question
            context: User context (visa type, tax year, etc.)
            conversation_history: Previous messages in conversation
            top_k: Number of relevant chunks to retrieve

        Returns:
            Dictionary with answer and sources
        """
        try:
            if self.index is None:
                return {
                    'answer': 'The knowledge base is not yet initialized. Please contact support.',
                    'sources': [],
                    'confidence': 0.0
                }

            # Build context-aware query
            enhanced_query = self._enhance_query(query, context)

            # Query the index
            query_engine = self.index.as_query_engine(
                similarity_top_k=top_k,
                response_mode='compact'
            )

            response = query_engine.query(enhanced_query)

            # Extract sources
            sources = self._extract_sources(response)

            return {
                'answer': str(response),
                'sources': sources,
                'confidence': self._calculate_confidence(response)
            }

        except Exception as e:
            logger.error(f"Query error: {str(e)}")
            return {
                'answer': 'I apologize, but I encountered an error processing your question. Please try rephrasing or contact support.',
                'sources': [],
                'confidence': 0.0
            }

    def _enhance_query(self, query: str, context: Dict[str, Any]) -> str:
        """Enhance query with context information"""
        visa_type = context.get('visaType', '')
        tax_year = context.get('taxYear', '')
        state = context.get('state', 'California')

        enhanced = f"{query}"

        if visa_type:
            enhanced += f" (for {visa_type} visa holders)"

        if tax_year:
            enhanced += f" for tax year {tax_year}"

        enhanced += f" in {state}"

        return enhanced

    def _extract_sources(self, response) -> List[Dict[str, Any]]:
        """Extract source documents from response"""
        sources = []

        try:
            if hasattr(response, 'source_nodes'):
                for node in response.source_nodes:
                    source = {
                        'documentName': node.metadata.get('file_name', 'Unknown'),
                        'pageNumber': node.metadata.get('page_number', 0),
                        'excerpt': node.text[:200] + '...' if len(node.text) > 200 else node.text,
                        'relevanceScore': node.score if hasattr(node, 'score') else 0.0
                    }
                    sources.append(source)
        except Exception as e:
            logger.error(f"Error extracting sources: {str(e)}")

        return sources

    def _calculate_confidence(self, response) -> float:
        """Calculate confidence score for the response"""
        try:
            if hasattr(response, 'source_nodes') and response.source_nodes:
                # Average of top source scores
                scores = [node.score for node in response.source_nodes if hasattr(node, 'score')]
                return sum(scores) / len(scores) if scores else 0.0
            return 0.0
        except Exception:
            return 0.0

    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the document collection"""
        try:
            count = self.collection.count()
            return {
                'totalDocuments': count,
                'collectionName': self.collection_name,
                'embeddingModel': self.embedding_model_name
            }
        except Exception as e:
            logger.error(f"Error getting stats: {str(e)}")
            return {
                'totalDocuments': 0,
                'error': str(e)
            }
