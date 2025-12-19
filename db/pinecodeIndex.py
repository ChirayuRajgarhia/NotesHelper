# Import the Pinecone library
from pinecone import Pinecone , ServerlessSpec

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key using os.getenv()
api_key = os.getenv("PINECONE_API_KEY")
# Initialize a Pinecone client with your API key
pc = Pinecone(api_key)

# Create a dense index with integrated embedding
index_name = "noteshelper-index"

def get_index():
    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            vector_type="dense",#no need to mention as "dense" is default 
            dimension=768,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")#no need to mention bcoz if not mentioned it takes spec itself
        )

    return pc.Index(index_name) 
