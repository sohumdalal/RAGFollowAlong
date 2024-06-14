from . import api_blueprint

@api_blueprint.route('/embed-and-store', methods=['POST'])
def embed_and_store():
  # handles scraping the URL, embedding the texts, and
  # uploading to the vector database.
  pass

@api_blueprint.route('/handle-query', methods=['POST'])
def handle_query():
  # handles embedding the user's question,
  # finding relevant context from the vector database,
  # building the prompt for the LLM,
  # and sending the prompt to the LLM's API to get an answer.
  pass