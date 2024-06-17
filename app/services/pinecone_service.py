import pinecone
from app.services.openai_service import get_embedding
import os
from pinecone import Pinecone, ServerlessSpec

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')

# make sure to enter your actual Pinecone environment
pinecone = Pinecone(api_key=PINECONE_API_KEY)

EMBEDDING_DIMENSION = 1536

def embed_chunks_and_upload_to_pinecone(chunks, index_name):
    
    # delete the index if it already exists. 
    # as Pinecone's free plan only allows one index
    if index_name in pinecone.list_indexes():
        pinecone.delete_index(name=index_name)
    
    # create a new index in Pinecone
    # the EMBEDDING_DIMENSION is based on what the
    # OpenAI embedding model outputs
    pinecone.create_index(name=index_name,
                          dimension=EMBEDDING_DIMENSION, metric='cosine')
    index = pinecone.Index(index_name)
    # embed each chunk and aggregate these embeddings
    embeddings_with_ids = []
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        embeddings_with_ids.append((str(i), embedding, chunk))
    # upload the embeddings and relevant texts for each chunk
    # to the Pinecone index
    upserts = [(id, vec, {"chunk_text": text}) for id, vec, text in embeddings_with_ids]
    index.upsert(vectors=upserts)


def get_most_similar_chunks_for_query(query, index_name):
    question_embedding = get_embedding(query)
    index = pinecone.Index(index_name)
    query_results = index.query(question_embedding, top_k=3, include_metadata=True)
    context_chunks = [x['metadata']['chunk_text'] for x in query_results['matches']]
    return context_chunks