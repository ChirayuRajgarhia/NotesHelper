
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

def embed_chunks(chunks):

    if not chunks: 
        raise ValueError("No valid text chunks to embed")

    result = client.models.embed_content(
            model="gemini-embedding-001",
            contents= chunks,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT",output_dimensionality=768))

    return [embedding.values for embedding in result.embeddings]
