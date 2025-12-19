def chunk_text(text, chunk_size=700, overlap=150):
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    chunks = [c.strip() for c in chunks if c.strip()]
    
    return chunks
