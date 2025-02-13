import os
import logging
import hashlib
from typing import Dict, Any, List
from pathlib import Path
import PyPDF2
import fitz  # PyMuPDF
from llama_index.core import Document
from llama_index.core.node_parser import SimpleNodeParser

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """
    Process and extract text from California tax documents
    """

    def __init__(self):
        self.data_dir = Path(__file__).parent.parent.parent / 'data'
        self.raw_dir = self.data_dir / 'raw'
        self.processed_dir = self.data_dir / 'processed'

        # Create directories if they don't exist
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

        # Initialize node parser for chunking
        self.node_parser = SimpleNodeParser.from_defaults(
            chunk_size=512,
            chunk_overlap=50
        )

    def process_document(self, file) -> Dict[str, Any]:
        """
        Process an uploaded document

        Args:
            file: Uploaded file object

        Returns:
            Dictionary with processing results
        """
        try:
            # Save file
            filename = file.filename
            file_path = self.raw_dir / filename
            file.save(str(file_path))

            logger.info(f"Processing document: {filename}")

            # Extract text based on file type
            if filename.lower().endswith('.pdf'):
                text_content = self._extract_pdf_text(file_path)
            else:
                raise ValueError(f"Unsupported file type: {filename}")

            # Create document ID
            doc_id = self._generate_document_id(filename)

            # Create chunks
            chunks = self._create_chunks(text_content, filename)

            logger.info(f"Created {len(chunks)} chunks from {filename}")

            return {
                'document_id': doc_id,
                'filename': filename,
                'chunks_created': len(chunks),
                'chunks': chunks
            }

        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            raise

    def _extract_pdf_text(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Extract text from PDF using PyMuPDF for better formatting

        Returns:
            List of dictionaries with page content and metadata
        """
        text_content = []

        try:
            # Use PyMuPDF for better text extraction
            doc = fitz.open(str(file_path))

            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()

                if text.strip():
                    text_content.append({
                        'page_number': page_num + 1,
                        'text': text,
                        'metadata': {
                            'file_name': file_path.name,
                            'page_number': page_num + 1
                        }
                    })

            doc.close()
            logger.info(f"Extracted text from {len(text_content)} pages")

        except Exception as e:
            logger.error(f"Error extracting PDF text: {str(e)}")
            # Fallback to PyPDF2
            text_content = self._extract_pdf_text_pypdf2(file_path)

        return text_content

    def _extract_pdf_text_pypdf2(self, file_path: Path) -> List[Dict[str, Any]]:
        """Fallback PDF text extraction using PyPDF2"""
        text_content = []

        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()

                if text.strip():
                    text_content.append({
                        'page_number': page_num + 1,
                        'text': text,
                        'metadata': {
                            'file_name': file_path.name,
                            'page_number': page_num + 1
                        }
                    })

        return text_content

    def _create_chunks(
        self,
        text_content: List[Dict[str, Any]],
        filename: str
    ) -> List[Dict[str, Any]]:
        """
        Create semantic chunks from extracted text
        """
        chunks = []

        for page_data in text_content:
            # Create LlamaIndex Document
            doc = Document(
                text=page_data['text'],
                metadata={
                    'file_name': filename,
                    'page_number': page_data['page_number']
                }
            )

            # Parse into nodes (chunks)
            nodes = self.node_parser.get_nodes_from_documents([doc])

            for node in nodes:
                chunks.append({
                    'text': node.text,
                    'metadata': node.metadata
                })

        return chunks

    def _generate_document_id(self, filename: str) -> str:
        """Generate unique document ID"""
        return hashlib.md5(filename.encode()).hexdigest()

    def get_processed_documents(self) -> List[str]:
        """Get list of processed documents"""
        return [f.name for f in self.processed_dir.iterdir() if f.is_file()]
