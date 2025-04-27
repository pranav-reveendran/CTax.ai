"""
Advanced preprocessing for California tax documents
"""
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import spacy
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')


class TaxDocumentPreprocessor:
    """
    Advanced preprocessing for tax documents with domain-specific handling
    """

    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        # Remove tax-specific terms from stop words
        self.stop_words -= {'not', 'no', 'nor', 'only', 'must', 'should', 'can'}

        # Load spaCy model for NER
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            logger.warning("spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None

    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s\.\,\;\:\-\$\%\(\)]', '', text)

        # Normalize currency amounts
        text = re.sub(r'\$\s*(\d+(?:,\d{3})*(?:\.\d{2})?)', r'$\1', text)

        # Normalize percentages
        text = re.sub(r'(\d+(?:\.\d+)?)\s*%', r'\1%', text)

        return text.strip()

    def extract_tax_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract tax-specific entities (forms, amounts, dates, visa types)
        """
        entities = {
            'forms': [],
            'amounts': [],
            'dates': [],
            'visa_types': [],
            'organizations': []
        }

        # Extract form numbers (e.g., Form 1040, Form W-2)
        forms = re.findall(r'Form\s+(\d+[-A-Z]*)', text, re.IGNORECASE)
        entities['forms'] = list(set(forms))

        # Extract monetary amounts
        amounts = re.findall(r'\$\d+(?:,\d{3})*(?:\.\d{2})?', text)
        entities['amounts'] = amounts

        # Extract dates
        dates = re.findall(
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
            text
        )
        entities['dates'] = dates

        # Extract visa types
        visa_types = re.findall(r'\b([FJH]-\d[AB]?|OPT|CPT)\b', text)
        entities['visa_types'] = list(set(visa_types))

        # Use spaCy for organization extraction
        if self.nlp:
            doc = self.nlp(text)
            entities['organizations'] = [ent.text for ent in doc.ents if ent.label_ == 'ORG']

        return entities

    def segment_by_topic(self, text: str) -> List[Dict[str, str]]:
        """
        Segment document into topic-based sections
        """
        sections = []

        # Common section headers in tax documents
        section_patterns = [
            r'(?:^|\n)(INTRODUCTION|OVERVIEW|GENERAL INFORMATION)',
            r'(?:^|\n)(WHO MUST FILE|FILING REQUIREMENTS)',
            r'(?:^|\n)(INCOME|TAXABLE INCOME)',
            r'(?:^|\n)(DEDUCTIONS|CREDITS)',
            r'(?:^|\n)(EXEMPTIONS|EXCLUSIONS)',
            r'(?:^|\n)(TAX RATES|TAX COMPUTATION)',
            r'(?:^|\n)(DEADLINES|IMPORTANT DATES)',
            r'(?:^|\n)(PENALTIES|INTEREST)',
        ]

        # Split by sections
        current_section = {'title': 'Introduction', 'content': ''}

        for line in text.split('\n'):
            # Check if line is a section header
            is_header = False
            for pattern in section_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    # Save previous section
                    if current_section['content']:
                        sections.append(current_section)

                    # Start new section
                    current_section = {
                        'title': line.strip(),
                        'content': ''
                    }
                    is_header = True
                    break

            if not is_header:
                current_section['content'] += line + '\n'

        # Add last section
        if current_section['content']:
            sections.append(current_section)

        return sections

    def create_qa_pairs(self, text: str) -> List[Dict[str, str]]:
        """
        Extract question-answer pairs from FAQ-style sections
        """
        qa_pairs = []

        # Pattern for Q&A format
        qa_pattern = r'Q\d*[:\.]?\s*(.+?)\s*A\d*[:\.]?\s*(.+?)(?=Q\d*[:\.?]|\Z)'

        matches = re.finditer(qa_pattern, text, re.DOTALL | re.IGNORECASE)

        for match in matches:
            question = match.group(1).strip()
            answer = match.group(2).strip()

            qa_pairs.append({
                'question': question,
                'answer': answer
            })

        return qa_pairs

    def extract_definitions(self, text: str) -> Dict[str, str]:
        """
        Extract term definitions from text
        """
        definitions = {}

        # Pattern for definitions: "Term means/is defined as..."
        pattern = r'([A-Z][a-z\s]+?)\s+(?:means|is defined as|refers to)\s+(.+?)(?:\.|;|\n)'

        matches = re.finditer(pattern, text)

        for match in matches:
            term = match.group(1).strip()
            definition = match.group(2).strip()
            definitions[term] = definition

        return definitions

    def chunk_with_overlap(
        self,
        text: str,
        chunk_size: int = 512,
        overlap: int = 50
    ) -> List[str]:
        """
        Create overlapping chunks for better context preservation
        """
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence_length = len(sentence.split())

            if current_length + sentence_length > chunk_size:
                # Save current chunk
                chunks.append(' '.join(current_chunk))

                # Start new chunk with overlap
                overlap_sentences = current_chunk[-overlap:] if len(current_chunk) >= overlap else current_chunk
                current_chunk = overlap_sentences + [sentence]
                current_length = sum(len(s.split()) for s in current_chunk)
            else:
                current_chunk.append(sentence)
                current_length += sentence_length

        # Add last chunk
        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks

    def enrich_metadata(self, chunk: str, doc_metadata: Dict) -> Dict:
        """
        Enrich chunk with extracted metadata
        """
        entities = self.extract_tax_entities(chunk)

        metadata = {
            **doc_metadata,
            'forms_mentioned': entities['forms'],
            'visa_types_mentioned': entities['visa_types'],
            'has_monetary_amounts': len(entities['amounts']) > 0,
            'has_dates': len(entities['dates']) > 0,
            'num_sentences': len(sent_tokenize(chunk)),
            'num_words': len(word_tokenize(chunk))
        }

        return metadata


if __name__ == '__main__':
    # Example usage
    preprocessor = TaxDocumentPreprocessor()

    sample_text = """
    Form 1040-NR must be filed by all nonresident aliens who have US source income.
    F-1 students are generally considered nonresident aliens for their first 5 calendar years.
    The filing deadline is April 15, 2024. Penalties for late filing can be $435 or more.
    """

    # Clean text
    cleaned = preprocessor.clean_text(sample_text)
    logger.info(f"Cleaned text: {cleaned}")

    # Extract entities
    entities = preprocessor.extract_tax_entities(sample_text)
    logger.info(f"Extracted entities: {entities}")

    # Create chunks
    chunks = preprocessor.chunk_with_overlap(sample_text, chunk_size=50, overlap=10)
    logger.info(f"Created {len(chunks)} chunks")
