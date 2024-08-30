import React, {useState} from 'react'
import { Form, Button } from 'react-bootstrap'

const Chat = () => {
  const [input, setInput] =  useState('')

  const handleChange = (e) => {
    setInput(e.target.value);
  }

  const handleSubmit = (e) => {

  }
  return (
    <div>
    {/* <Header template="panel_user" details={page} lang={lang} /> */}
        <Form className="chat_form">
            <div id="chatmessages" className="input_light">
                {/* <ChatMessages messages={messages} lang={lang} height={height} /> */}
            </div>
            <input className="input_light" type="text" value={input} onChange={(e)=>{handleChange(e)}}/>
            <Button type="button" onClick={(e)=>handleSubmit(e)} className="mybutton button_fullcolor shadow_convex">
            </Button>
        </Form>
        {/* <ChatList list={chatRoomUsers} /> */}
    </div>
  )
}

export default Chat