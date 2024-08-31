import React, { useState, useEffect } from 'react'
import { Form, Button } from 'react-bootstrap'

const Chat = () => {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([])

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

  const handleSendMessage = () => {
    if (input.trim()) {
      setMessages([...messages, input.trim()]);
      setInput(''); // Clear the input box after sending
    }
  };
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
        <input className="input_light" type="text" value={input} onChange={(e) => { handleChange(e) }} />
        <Button type="button" onClick={handleSendMessage} className="mybutton button_fullcolor shadow_convex">
        </Button>
      </Form>
      {/* <ChatList list={chatRoomUsers} /> */}
    </div>
  )
}

export default Chat