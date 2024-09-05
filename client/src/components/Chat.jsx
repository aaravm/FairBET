import React, { useState, useEffect } from 'react'
import { Form, Button } from 'react-bootstrap'
import axios from 'axios'
import { GoogleGenerativeAI } from "@google/generative-ai";

const Chat = () => {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([])
  const [response, setResponse] = useState('')

  const handleChange = (e) => {
    setInput(e.target.value);
  }

  // Load messages from localStorage when the component mounts
  useEffect(() => {
    const savedMessages = JSON.parse(localStorage.getItem('messages'));
    if (savedMessages) {
      setMessages(savedMessages);
    }
  }, []);

  // Save messages to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('messages', JSON.stringify(messages));
  }, [messages]);

  const handleSendMessage = async () => {
    if (input.trim()) {
      setMessages([...messages, input.trim()]);
      const data = input;
      setInput(''); // Clear the input box after sending
      try {
        const Your_API_Key = "AIzaSyCIAMgozAJIGHNQWpzmJgGCYY64QRMAwUo";
        console.log("hi", Your_API_Key);
        const genAI = new GoogleGenerativeAI(Your_API_Key);
        const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash-latest" });

        const prompt = `Tell me only in True or False that if I should ban the user if it uses this language: "${data}"`;

        const result = await model.generateContent(prompt);
        console.log("result:", result);
        const response = await result.response;
        const text = response.text();
        console.log(text);
        if (text.trim() === 'True.') {
          console.log("hey")
          setMessages([...messages, "WARNING: Don't use any vulgar words, else you'll get banned"]);
          alert("WARNING: Don't use any vulgar words, else you'll get banned");
        }
      } catch (error) {
        console.error('Error making API call:', error);
      }
    }
  }

  // Handle Enter key press
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();  // Prevent default action (submitting the form)
      handleSendMessage();
    }
  }

  return (
    <div>
      {/* <Header template="panel_user" details={page} lang={lang} /> */}
      <Form className="chat_form">
        <div id="chatmessages" className="input_light">
          <div className='messages'>
            {messages.map((message, index) => (
              <div key={index} className='message'>
                {message}
              </div>
            ))}
          </div>
        </div>
        <input 
          className="input_light" 
          type="text" 
          value={input} 
          onChange={(e) => { handleChange(e) }} 
          onKeyDown={handleKeyPress} // Add this to capture Enter key
        />
        <Button 
          type="button" 
          onClick={handleSendMessage} 
          className="mybutton button_fullcolor shadow_convex">
          Send
        </Button>
      </Form>
      {/* <ChatList list={chatRoomUsers} /> */}
    </div>
  )
}

export default Chat
