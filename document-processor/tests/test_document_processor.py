import unittest
from src.services.document_processor import DocumentProcessor

class TestDocumentProcessor(unittest.TestCase):

    def setUp(self):
        self.processor = DocumentProcessor()

    def test_generate_document_id(self):
        """Test document ID generation"""
        filename = "test.pdf"
        doc_id = self.processor._generate_document_id(filename)
        self.assertIsNotNone(doc_id)
        self.assertIsInstance(doc_id, str)

    def test_chunk_creation(self):
        """Test chunk creation from text"""
        text_content = [
            {
                'page_number': 1,
                'text': 'This is test content for document processing.',
                'metadata': {
                    'file_name': 'test.pdf',
                    'page_number': 1
                }
            }
        ]

        chunks = self.processor._create_chunks(text_content, 'test.pdf')
        self.assertGreater(len(chunks), 0)
        self.assertIn('text', chunks[0])
        self.assertIn('metadata', chunks[0])

if __name__ == '__main__':
    unittest.main()
