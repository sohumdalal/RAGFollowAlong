import json
import requests
from openai import OpenAI
from dotenv import load_dotenv
from app.utils.helper_functions import build_prompt, construct_messages_list
import os
load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
openai_client = OpenAI(api_key=OPENAI_API_KEY)

OPENAI_EMBEDDING_MODEL = 'text-embedding-ada-002'
PROMPT_LIMIT = 3750
CHATGPT_MODEL = 'gpt-3.5-turbo'


def get_embedding(chunk):
    url = 'https://api.openai.com/v1/embeddings'
    headers = {
        'content-type': 'application/json; charset=utf-8',
        'Authorization': f"Bearer {OPENAI_API_KEY}"
    }
    data = {
        'model': OPENAI_EMBEDDING_MODEL,
        'input': chunk
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_json = response.json()

    if 'error' in response_json:
        # Handle the error response
        error_message = response_json['error']['message']
        print(f"OpenAI API Error: {error_message}")
        return None  # or handle the error in a different way

    embedding = response_json["data"][0]["embedding"]
    return embedding


def construct_llm_payload(question, context_chunks, chat_history):
  
  # Build the prompt with the context chunks and user's query
  prompt = build_prompt(question, context_chunks)
  print("\n==== PROMPT ====\n")
  print(prompt)

  # Construct messages array to send to OpenAI
  messages = construct_messages_list(chat_history, prompt)

  # Construct headers including the API key
  headers = {
      'content-type': 'application/json; charset=utf-8',
      'Authorization': f"Bearer {OPENAI_API_KEY}"            
  }  

  # Construct data payload
  data = {
      'model': CHATGPT_MODEL,
      'messages': messages,
      'temperature': 1, 
      'max_tokens': 1000,
      'stream': True
  }

  return headers, data
