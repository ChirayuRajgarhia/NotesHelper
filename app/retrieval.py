from db.pinecodeIndex import get_index
from embedding.gemini_embed import embed_chunks
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Initialize clients
index = get_index()
gemini_client = genai.Client()

#retrieve_relevant_chunks
def semantic_search(query: str, namespace, top_k: int = 5):
    """
    Step 1–4:
    - Embed user query
    - Semantic search in Pinecone
    - Return top-k relevant chunks
    """

    # 1. Embed query (single text, wrapped as list)
    query_embedding = embed_chunks([query])[0]

    # 2. Query Pinecone
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        namespace=namespace
    )#results = dictionary with 3 key one of the key is matches (see document)

    # 3. Extract matched text chunks
    retrieved_chunks = [
        match["metadata"]["text"]   # from match take value of "metadata" then from "metadata" take value of "text" 
        for match in results["matches"] #matches contains list of many dict so match = dict
    ]
    print(retrieved_chunks)
    return retrieved_chunks


def generate_answer(query: str, context_chunks: list[str]):
    """
    Step 5–6:
    - Feed retrieved context + question to Gemini
    - Generate grounded answer
    """

    context = "\n\n".join(context_chunks)

    prompt = f"""
                You are an intelligent assistant.
                Answer the question using ONLY the context below.
                If the answer is not present, say "Not found in provided notes."

                Context:
                {context}

                Question:
                {query}
                """

    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def answer_question(query: str,namespace):
    """
    Full retrieval pipeline
    """

    # Retrieve relevant chunks
    chunks = semantic_search(query,namespace)

    if not chunks:
        return "No relevant information found."

    # Generate final answer
    answer = generate_answer(query, chunks)

    return answer
