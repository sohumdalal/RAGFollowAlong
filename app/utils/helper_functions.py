def chunk_text(text, chunk_size=200):
    # Split the text by sentences to avoid breaking in the middle of a sentence
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        # Check if adding the next sentence exceeds the chunk size
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += sentence + '. '
        else:
            # If the chunk reaches the desired size, add it to the chunks list
            chunks.append(current_chunk)
            current_chunk = sentence + '. '
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk)
    return chunks