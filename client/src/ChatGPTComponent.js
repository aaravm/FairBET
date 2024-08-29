import React, { useState } from 'react';
import axios from 'axios';

const ChatGPTComponent = () => {
  const [response, setResponse] = useState('');
  const [input, setInput] = useState('');

  const handleSubmit = async () => {
    try {
      const result = await axios.post(
        'https://api.openai.com/v1/completions',  // Endpoint for the API
        {
          model: 'text-davinci-003',  // Specify the model
          prompt:  `Please answer with only "true" or "false" that it is vulgar language or not: ${input}`,
          max_tokens: 5,
          temperature: 0,
        },
        {
          headers: {
            'Authorization': `Bearer ${process.env.REACT_APP_OPENAI_API_KEY}`,  // Replace with your API key
            'Content-Type': 'application/json'
          }
        }
      );
      setResponse(result.data.choices[0].text.trim());
      if(response==="true"){
        alert("This is a vulgar language");
        
      }
    } catch (error) {
      console.error('Error making API call:', error);
    }
  };

  return (
    <div>
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Enter your prompt here"
      />
      <button onClick={handleSubmit}>Submit</button>
      <div>
        <h3>Response:</h3>
        <p>{response}</p>
      </div>
    </div>
  );
};

export default ChatGPTComponent;
