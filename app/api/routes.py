from . import api_blueprint
import os
from flask import request, jsonify, Response, stream_with_context, json
import requests
import sseclient
from app.services import openai_service, pinecone_service, scraping_service
from app.utils.helper_functions import chunk_text, build_prompt, construct_messages_list

PINECONE_INDEX_NAME = 'index237'


@api_blueprint.route('/handle-query', methods=['POST'])
def handle_query():
    question = request.json['question']
    chat_history = request.json['chatHistory']
    context_chunks = pinecone_service.get_most_similar_chunks_for_query(question, PINECONE_INDEX_NAME)
    
    # prompt = build_prompt(question, context_chunks)
    # print("\n==== PROMPT ====\n")
    # print(prompt)
    # answer = openai_service.get_llm_answer(prompt)
    # return jsonify({ "question": question, "answer": answer }) 

    headers, data = openai_service.construct_llm_payload(question, context_chunks, chat_history)
    def generate():
        url = 'https://api.openai.com/v1/chat/completions'
        response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)
        client = sseclient.SSEClient(response)
        for event in client.events():
            if event.data != '[DONE]':
                try:
                    text = json.loads(event.data)['choices'][0]['delta']['content']
                    yield(text)
                except:
                    yield('')
    
    return Response(stream_with_context(generate()))

@api_blueprint.route('/embed-and-store', methods=['POST'])
def embed_and_store():
    print("I am in the delete index function")
    url = request.json['url']
    url_text = scraping_service.scrape_website(url)
    chunks = chunk_text(url_text)
    pinecone_service.embed_chunks_and_upload_to_pinecone(chunks, PINECONE_INDEX_NAME)
    response_json = {
        "message": "Chunks embedded and stored successfully"
    }
    return jsonify(response_json)

@api_blueprint.route('/delete-index', methods=['POST'])
def delete_index():
    pinecone_service.delete_index(PINECONE_INDEX_NAME)
    return jsonify({"message": f"Index {PINECONE_INDEX_NAME} deleted successfully"})