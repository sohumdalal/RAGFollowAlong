import React, { useState, useEffect } from 'react';
import UrlInput from './components/UrlInput';
import ChatInterface from './components/ChatInterface';

function App() {
  const [showChat, setShowChat] = useState(false); // Add state to control UI transition
  const handleUrlSubmitted = () => {
    setShowChat(true); // Transition to the ChatInterface
  };

  // Delete the Pinecone index when the user leaves the page
  useEffect(() => {
    return () => {
      fetch('/delete-index', {
        method: 'POST',
      })
        .then((response) => {
          if (!response.ok) {
            console.error('Error deleting index:', response.statusText);
          }
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    };
  }, []);

  return (
    <div className="App">
      {!showChat ? (
        <UrlInput onSubmit={handleUrlSubmitted} />
      ) : (
        <ChatInterface />
      )}
    </div>
  );
}

export default App;