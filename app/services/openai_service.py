import json
import requests
from openai import OpenAI
from dotenv import load_dotenv
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


def get_llm_answer(prompt, chat_history):
  
  messages = [{"role": "system", "content": "You are a helpful assistant."}]
  # Pass in the entire chat history

  for message in chat_history:
    if message['isBot']:
      messages.append({"role": "system", "content": message["text"]})
    else:
      messages.append({"role": "user", "content": message["text"]})

  # Replace last message with the full prompt
  messages[-1]["content"] = prompt

  url = 'https://api.openai.com/v1/chat/completions'
  headers = {
      'content-type': 'application/json; charset=utf-8',
      'Authorization': f"Bearer {OPENAI_API_KEY}"            
  }
  data = {
      'model': CHATGPT_MODEL,
      'messages': messages,
      'temperature': 1, 
      'max_tokens': 1000
  }
  response = requests.post(url, headers=headers, data=json.dumps(data))
  response_json = response.json()
  completion = response_json["choices"][0]["message"]["content"]
  return completion