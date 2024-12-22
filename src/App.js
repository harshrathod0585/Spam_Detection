import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [result, setResult] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult(''); // Clear previous result

    if (!message.trim()) {
      setResult('Please enter a message.');
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:5000/predict', { message });
      setResult(`Prediction: ${response.data.prediction}`);
    } catch (error) {
      if (error.response) {
        setResult(`Error: ${error.response.data.error || 'Something went wrong!'}`);
      } else {
        setResult('Error: Unable to connect to server.');
      }
    }
  };

  return (
    <div className="App">
      <div className="content">
        <h1 className="title">Spam Detector</h1>
        <form onSubmit={handleSubmit} className="form">
          <textarea
            className="input-text"
            rows="5"
            placeholder="Enter your message here..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
          />
          <button type="submit" className="submit-button">Check</button>
        </form>
        {result && <h1 className="result">{result}</h1>}
      </div>
    </div>
  );
}

export default App;
