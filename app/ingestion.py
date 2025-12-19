from db.pinecodeIndex import get_index
from embedding.gemini_embed import embed_chunks
from utils.chunker import chunk_text

def ingest(text):
    chunks = chunk_text(text)
    embeddings = embed_chunks(chunks)
    index = get_index()
    upsert_chunks(chunks,embeddings,index)


def upsert_chunks(chunks, embeddings,index): 
    vectors = [] 
    
    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)): 
        vectors.append({ "id": f"chunk-{i}",
                         "values": emb, 
                         "metadata": { "text": chunk } 
                        }) 
        
    index.upsert(vectors=vectors)