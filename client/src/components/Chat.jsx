import React, { useState, useEffect } from 'react';
import { Button, Container, Row, Col, InputGroup, FormControl } from 'react-bootstrap';
import { GoogleGenerativeAI } from "@google/generative-ai";
import './Chat.css'; // Assuming custom CSS is being used
import {useStateContext} from "../context/index"
import { useNavigate } from 'react-router-dom';
import {
  SignProtocolClient,
  SpMode,
  EvmChains,
  IndexService,
  delegateSignAttestation,
  delegateSignRevokeAttestation,
  delegateSignSchema,
} from "@ethsign/sp-sdk";
import { privateKeyToAccount } from "viem/accounts";
import { FaComments } from 'react-icons/fa'; // Add your preferred icon library

const Chat = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [isChatVisible, setIsChatVisible] = useState(false); // Manage chat visibility
  const {account, setAccount} = useStateContext();
  const {ip, setIp} = useStateContext();
  const navigate = useNavigate()

  const privateKey = "0x2b45672b49ed7422d2cc12239c884fc9e7d4dc023a2f119c8873890c4771a49d"; // Optional
  const handleChange = (e) => {
    setInput(e.target.value);
  };

  // Remove user's account when he gets banned
  // useEffect = () => {
  //   setAccount('')
  //   navigate('../')
  // }

  const client = new SignProtocolClient(SpMode.OnChain, {
    chain: EvmChains.baseSepolia,
    account: privateKeyToAccount(privateKey), // Optional if you are using an injected provider
  });
  
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

  const checkIfUserIsBanned = async (address) => {
    const indexService = new IndexService("testnet");
    const res = await indexService.queryAttestationList({
      schemaId : "onchain_evm_84532_0x1cc",
      attester:"0xBA2570e298E8111caB760b6614D84879D6957414",
      mode: "onchain",
      page: 1,
    });
    let count=0;
    let count1=0;
    console.log(ip);
    res.rows.forEach((element) => {
      console.log("element",element.indexingValue);
      if(element.indexingValue === address ){
        count++;
      }
      if(element.indexingValue === ip){
        count1++;
      }
    });
    console.log("count",count);
    if(count>=3 || count1>=3){
      setAccount('')
      setIp('')
      navigate('../')
      alert("You are banned");
    }
  }

  const handleSendMessage = async () => {
    if (input.trim()) {
      setMessages([...messages, { text: input.trim(), sender: 'user' }]);
      const data = input;
      setInput(''); // Clear the input box after sending
      try {
        const Your_API_Key = "AIzaSyCIAMgozAJIGHNQWpzmJgGCYY64QRMAwUo";
        console.log("data",Your_API_Key)
        const genAI = new GoogleGenerativeAI(Your_API_Key);
        const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash-latest" });

        const prompt = `Tell me only in True or False that if it is a vulgar language: "${data}"`;

        const result = await model.generateContent(prompt);
        console.log("result",result)
        const response = await result.response;
        const text = await response.text();
        console.log("text",text)
        checkIfUserIsBanned(account);

        if (text.trim() === 'True.' || text.trim() === 'True') {
          setMessages([...messages, { text: "WARNING: Don't use any vulgar words, else you'll get banned", sender: 'system' }]);
          alert("WARNING: Don't use any vulgar words, else you'll get banned");
          console.log("create attestation");
          const createAttestationRes = await client.createAttestation({
            schemaId: "0x1cc",
            data: { user_address: account },
            indexingValue: account,
          });
          const createAttestationReswithIp = await client.createAttestation({
            schemaId: "0x1cc",
            data: { user_address: account },
            indexingValue: ip,
          });

        }
      } catch (error) {
        console.error('Error making API call:', error);
      }
    }
  };

  // Handle Enter key press
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();  // Prevent default action (like form submission)
      handleSendMessage();  // Call the send message function
    }
  };

  const toggleChat = () => {
    setIsChatVisible(!isChatVisible);
  };

  return (
    <>
      <Container className={`chat-container ${isChatVisible ? 'chat-visible' : 'chat-hidden'}`}>
        <Row>
          <Col xs={12} md={8} className="mx-auto">
            <div className="chat-box">
              <div className="messages-box">
                {messages.length === 0 && <div className="message system-message">Start chatting with the AI</div>}
                {!(messages.length === 0) && messages.map((message, index) => (
                  <div key={index} className={`message ${message.sender === 'user' ? 'user-message' : 'system-message'}`}>
                    {message.text}
                  </div>
                ))}
              </div>
              <InputGroup className="mb-3 chat-input-group">
                <FormControl
                  placeholder="Type a message..."
                  value={input}
                  onChange={handleChange}
                  onKeyDown={handleKeyPress}  // Capture the Enter key press here
                  className="chat-input"
                />
                <Button variant="primary" onClick={handleSendMessage} className="send-button">
                  Send
                </Button>
              </InputGroup>
            </div>
          </Col>
        </Row>
      </Container>
      <Button className="chat-toggle-button" onClick={toggleChat}>
        <FaComments />
      </Button>
    </>
  );
};

export default Chat;
