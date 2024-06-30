**Summary**

Hello friends! I followed a colleague's tutorial on building a full stack LLM app leveraging Retrieval-Augmented Generation (RAG). His name is Ashwin Kumar, and his tutorial is an excellent introduction to RAG and its impact on creating LLM chatbots. 

**Here is a breakdown of the app:**

1. The client sends a URL via an HTTP POST request to the Flask server (see client/src/components/UrlInput.js).

2. The server receives the URL at an endpoint (see app/api/routes.py), scrapes/parses the URL using BeautifulSoup, and then chunks it into segments of 200 characters (see app/utils/helper_functions.py).

3. The chunks are sent to the "embed_chunks_and_upload_to_pinecone" function (see app/services/pinecone_service.py). This function creates a new Pinecone index, embeds the text chunks into vectors using OpenAI, and uploads these vectors to the index, including metadata for each chunk, ensuring the index is fresh by deleting any existing one with the same name.

4. The chatbot is now ready to take questions. The "handleSendMessage" function (see client/src/components/ChatInterface.js) captures the user's message and sends it to the server. It then appends a placeholder bot message to the chat history and streams the server's response to update the bot message dynamically, ensuring smooth and continuous message updates, similar to ChatGPT.

5. Once the "handle-query" POST request (triggered by "handleSendMessage") reaches the server, the handle_query route handler retrieves the user's question and chat history. Three big things are happening for us:
    1. The "context_chunks" varaiable calls a pinecone service function to find the most relevant context chunks from Pinecone
    2. It then uses the chunks to constructs a payload to send to OpenAI's API for a response. Note thatthe payload construction function can also adjust the model and itspreferences.
    3. the payload ("header","data") is then sent to OPENAI to generate a response.

6. The final step of this route handler streams the response from OpenAI back to the client in real-time.
<br></br>


I encouraged ya'll to give the app a try. You can look at Ashwin's github for starter steps, but they are also copied here:

Install Python dependencies
```
pip install -r requirements.txt
```

Install React dependencies
```
cd client
npm install
```
Create .env file
```
OPENAI_API_KEY=<YOUR_API_KEY>
PINECONE_API_KEY=<YOUR_API_KEY>
```
Start the Flask server
```
# In root directory
python run.py
```
Start the React app
```
cd client
npm start
```
<br></br>
Below are some items that I either included or wanted to make note of. 

1. CORS Handling
    - Had some CORS issues earlier on, so I decided to manually include headers with all outgoing responses.

2. Updated Pincone access
    - Pinecone's pc.init is deprecated. [Docs](https://docs.pinecone.io/guides/get-started/quickstart) prefer you instantiate a new pc variable as such:
    
      ```
      pc = Pinecone(api_key=PINECONE_API_KEY)
      ```
     - You can then create indexes as such:

        ```
        if index_name not in pc.list_indexes().names():
          pc.create_index(
            name=index_name,
            dimension=EMBEDDING_DIMENSION,
            metric='cosine',
            spec=ServerlessSpec(
                cloud='#someCloud',
                region='#someRegion'  
            )
        )
        ```
3. OPENAI Service access

   - Make sure you have a small amount of money in your account. Free tier access is always changing.
<br></br>

Here are links to Ashwin's original posts:

- https://shwinda.medium.com/build-a-full-stack-llm-application-with-openai-flask-react-and-pinecone-part-1-f3844429a5ef

- https://shwinda.medium.com/build-a-full-stack-llm-application-with-openai-flask-react-and-pinecone-part-2-ceda4e290c33


Follow Ashwin's Github:
- https://github.com/ashnkumar

