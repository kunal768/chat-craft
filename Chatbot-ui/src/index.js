// Create a file named index.js in your src directory
import React from 'react';
import ReactDOM from 'react-dom/client';
import './App.css';
import App from './App.jsx'; // Importing your main component

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);