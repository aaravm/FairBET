import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { StateContextProvider } from './context';
import { BrowserRouter } from "react-router-dom";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <BrowserRouter>
    <StateContextProvider>
      <App />
    </StateContextProvider>
  </BrowserRouter>
);
