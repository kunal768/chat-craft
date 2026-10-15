import React from 'react';
import './App.css';
import ChatWidget from './ChatWidget.js';

function App() {
  return (
    <div className="App">
      {/* Top bar with dark background */}
      <div className="top-bar">
        <div className="top-bar-left">
          Enterprise AI
        </div>
        <div className="top-bar-right">
          Chat Session
        </div>
      </div>

      {/* Main layout: Left empty, center (chat), right empty */}
      <div className="main-container">
        <div className="side-empty">
          {/* Left side content (currently empty) */}
        </div>

        <div className="center-container">
          {/* Chat Widget with export button enabled */}
          <ChatWidget theme="light" showExportButton={true} />
        </div>

        <div className="side-empty">
          {/* Right side content (currently empty) */}
        </div>
      </div>
    </div>
  );
}

export default App;
