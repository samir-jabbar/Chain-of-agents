from typing import List
import logging
import fitz  # PyMuPDF

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_pdf(pdf_path: str) -> str:
    """
    Read text content from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        text = []
        with fitz.open(pdf_path) as doc:
            logger.info(f"Processing PDF with {len(doc)} pages")
            for page in doc:
                text.append(page.get_text())
        
        return "\n".join(filter(None, text))  # Filter out empty strings
    except Exception as e:
        logger.error(f"Error reading PDF: {str(e)}")
        raise

def split_into_chunks(text: str, chunk_size: int, model: str = "open-mistral-7b") -> List[str]:
    """
    Split text into chunks based on word count.
    
    Args:
        text: The input text to split
        chunk_size: Maximum number of words per chunk
        model: Not used, kept for compatibility
        
    Returns:
        List[str]: List of text chunks
    """
    # Split by paragraphs first to maintain context
    paragraphs = text.split('\n\n')
    words = []
    current_chunk = []
    chunks = []
    
    for paragraph in paragraphs:
        # Skip empty paragraphs
        if not paragraph.strip():
            continue
            
        paragraph_words = paragraph.split()
        
        # If adding this paragraph exceeds chunk size, save current chunk and start new one
        if len(current_chunk) + len(paragraph_words) > chunk_size:
            if current_chunk:  # Save current chunk if it exists
                chunks.append(' '.join(current_chunk))
                current_chunk = []
            
            # Handle paragraphs larger than chunk_size
            while len(paragraph_words) > chunk_size:
                chunks.append(' '.join(paragraph_words[:chunk_size]))
                paragraph_words = paragraph_words[chunk_size:]
            
            current_chunk = paragraph_words
        else:
            current_chunk.extend(paragraph_words)
    
    # Add any remaining text
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    logger.info(f"Split text into {len(chunks)} chunks")
    return chunks

def count_tokens(text: str, model: str = "open-mistral-7b") -> int:
    """
    Count the number of words in a text string.
    
    Args:
        text: The input text
        model: Not used, kept for compatibility
        
    Returns:
        int: Number of words
    """
    return len(text.split())

def get_default_prompts() -> tuple[str, str]:
    """
    Get default system prompts for worker and manager agents.
    
    Returns:
        tuple[str, str]: (worker_prompt, manager_prompt)
    """
    
    worker_prompt = """You are a helpful assistant in building an ontology. You are fluent in the W3C Semantic Web stack and RDF, RDFS, and OWL languages.
    Use the given text to construct an OWL ontology in the Turtle format. Use this namespace: http://example.org/example#. Return only the turtle file.
    Extract all the possible classes and subclasses.

    keep in mind that the syntax has to be like the following:
        -For classes ":ClassName rdf:type owl:Class;"
        -For ObjectProperty: "Name of the object property rdf:type owl:ObjectProperty ;"
    """
    
    manager_prompt = """You are an ontology learning expert and your goal is to integrate the given ontologies with all their classes
     into a coherent ontology while ensuring no reddandancy.
    Your response should be structured, modular, and ready for further reasoning and inference."""

    return worker_prompt, manager_prompt 