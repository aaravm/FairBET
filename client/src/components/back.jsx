// ButtonComponent.js
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { IoIosArrowBack } from 'react-icons/io'; // Import the back icon
import './back.css';

const Back = () => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate('/');
  };

  return (
    <button className="top-left-button" onClick={handleClick}>
      <IoIosArrowBack size={20} style={{ marginRight: '5px' }} />
    </button>
  );
};

export default Back;
