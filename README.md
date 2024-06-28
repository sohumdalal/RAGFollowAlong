**Summary**

I followed Ashwin Kumar's tutorial on building a full stack LLM app leveraging RAG. Here is a breakdown of the app:

  1. The client sends any URL via HTTP POST request to the Flask server (see client/src/components/UrlInput.js)
  2. The server receives URL at an endpoint (see app/api/routes.py), which firsts scrapes/parses the URL (using BeauitfulSoup), and then chunks it (we set chunk size to 200) (see app/utils/helper_functions.py)
  3. We then send our chunks to the "embed_chunks_and_upload_to_pinecone" function (see app/services/pinecone_service.py). The function creates a new Pinecone index, embeds text chunks into vectors using OpenAI, and uploads these vectors to the index, including metadata for each chunk. It ensures the index is fresh by deleting any existing index with the same name before creation.
  4. Now the chatbot is ready to take questions. The handleSendMessage function (see client/src/components/ChatInterface.js) captures the user's message, sends it to the server. The function will also append a placeholder bot message to the chat history, and then stream the server's response to update the bot message dynamically, ensuring smooth and continuous message updates by appending received data chunks to the bot message in real-time, just like ChatGPT.
  5. Once handle-query (POST request trigged by handleSendMessage) reaches the server, The handle_query route handler retrieves the user's question and chat history, and uses two functions to find the most relevant context chunks from Pinecone, and construct a payload to send to OpenAI's API for a response. The payload construction function can also adjust the model and its preferences. The very last line of this route handler streams the response from OpenAI back to the client in real-time.














  3. the system queries a retrieval system (e.g., Pinecone) for relevant documents or information based on the input     message. This step enhances the language model's understanding by providing additional context.
  4. The retrieved information is combined with the input message and sent to the OpenAI API. The OpenAI model uses this augmented input to generate a more informed and accurate response.
  5. Generating the Response: The OpenAI API returns a response that incorporates both the user's message and the retrieved context.
  6. Sending the Response Back to the Client: The processed response is sent back to the client, which updates the user interface with the generated response.

Here are some key adds on my end:

**1. CORS Handling
**

**2. Updated Pincone access
**

**3. OPENAI Service access
**

Here are links to Ashwin's original posts:

- https://shwinda.medium.com/build-a-full-stack-llm-application-with-openai-flask-react-and-pinecone-part-1-f3844429a5ef

- https://shwinda.medium.com/build-a-full-stack-llm-application-with-openai-flask-react-and-pinecone-part-2-ceda4e290c33

Follow Ashwin's Github:
- https://github.com/ashnkumar

