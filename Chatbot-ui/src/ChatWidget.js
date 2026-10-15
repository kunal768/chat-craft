import React, { useState, useRef, useEffect } from 'react';

const ChatWidget = ({ theme = 'light', showExportButton = false }) => {
  const [messages, setMessages] = useState([
    { id: 1, text: 'Hello, how can I assist you?', sender: 'system', timestamp: new Date(), status: 'read' },
  ]);
  const [newMessage, setNewMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  // Theme configurations
  const themes = {
    light: {
      primary: '#3498db',
      secondary: '#ecf0f1',
      text: '#2c3e50',
      chatBg: '#ffffff',
      userBubble: '#3498db',
      userText: '#ffffff',
      systemBubble: '#ecf0f1',
      systemText: '#2c3e50',
      inputBg: '#ffffff',
      border: '#e0e0e0',
      typingColor: '#95a5a6'
    },
    dark: {
      primary: '#2980b9',
      secondary: '#34495e',
      text: '#ecf0f1',
      chatBg: '#2c3e50',
      userBubble: '#2980b9',
      userText: '#ffffff',
      systemBubble: '#34495e',
      systemText: '#ecf0f1',
      inputBg: '#34495e',
      border: '#4a6380',
      typingColor: '#7f8c8d'
    },
  };

  const currentTheme = themes[theme] || themes.light;

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  // Embed code snippet to be copied by the Export button.
  const embedCode = `<iframe src="https://yourdomain.com/embed.html" width="720" height="600" frameborder="0" style="border: none; overflow: hidden;"></iframe>`;

  // Handler to copy embed code to clipboard
  const handleExport = () => {
    navigator.clipboard.writeText(embedCode)
      .then(() => {
        alert("Embed code copied to clipboard!");
      })
      .catch(() => {
        alert("Failed to copy to clipboard. Please try manually.");
      });
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (newMessage.trim() === '') return;
    
    const newMsg = {
      id: messages.length + 1,
      text: newMessage,
      sender: 'user',
      timestamp: new Date(),
      status: 'sending',
      animate: true
    };
    
    setMessages([...messages, newMsg]);
    setNewMessage('');
    
    setTimeout(() => {
      setMessages(prev => 
        prev.map(msg => 
          msg.id === newMsg.id ? { ...msg, status: 'delivered', animate: false } : msg
        )
      );
      setIsTyping(true);
    }, 300);
    
    setTimeout(() => {
      setIsTyping(false);
      
      const responseMsg = {
        id: newMsg.id + 1,
        text: `Thank you for your message! This is a simulated response.`,
        sender: 'system',
        timestamp: new Date(),
        status: 'read',
        animate: true
      };
      
      setMessages(prev => [
        ...prev.map(msg => 
          msg.id === newMsg.id ? { ...msg, status: 'read', animate: false } : msg
        ),
        responseMsg
      ]);
      
      setTimeout(() => {
        setMessages(prev => 
          prev.map(msg => 
            msg.id === responseMsg.id ? { ...msg, animate: false } : msg
          )
        );
      }, 200);
    }, 1000);
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const renderStatus = (status) => {
    switch (status) {
      case 'sending':
        return '• Sending';
      case 'delivered':
        return '• Delivered';
      case 'read':
        return '• Read';
      default:
        return '';
    }
  };

  // Typing indicator component
  const TypingIndicator = () => (
    <div style={{
      alignSelf: 'flex-start',
      backgroundColor: currentTheme.systemBubble,
      padding: '12px 16px',
      borderRadius: '18px 18px 18px 0',
      marginBottom: '10px',
      display: 'flex',
      alignItems: 'center',
      gap: '4px'
    }}>
      {[0, 150, 300].map((delay, idx) => (
        <div
          key={idx}
          style={{
            height: '8px',
            width: '8px',
            borderRadius: '50%',
            background: currentTheme.typingColor,
            animation: 'typingAnimation 0.8s infinite ease-in-out',
            animationDelay: `${delay}ms`
          }}
        />
      ))}
      <style>
        {`
          @keyframes typingAnimation {
            0%   { transform: translateY(0px); }
            50%  { transform: translateY(-5px); }
            100% { transform: translateY(0px); }
          }
        `}
      </style>
    </div>
  );

  return (
    // Outer wrapper: use block display with a fixed width (centered) and extra top margin when export button is shown.
    <div style={{ 
      position: 'relative', 
      display: 'block', 
      width: 'fit-content', 
      margin: showExportButton ? '80px auto 0 auto' : '0 auto'
    }}>
      {showExportButton && (
        // Export button is positioned in the extra top margin (outside the chat widget border)
        <button 
          onClick={handleExport}
          style={{
            position: 'absolute',
            top: '-50px',  // Adjust this value as needed for separation
            right: '0',
            zIndex: 100,
            backgroundColor: '#2f2f2f', // Matches header dark color
            color: '#fff',
            border: 'none',
            borderRadius: '4px',
            padding: '6px 12px',
            cursor: 'pointer'
          }}
        >
          Export Chat
        </button>
      )}

      {/* Chat Widget container with fixed height */}
      <div
        style={{
          width: '100%',
          maxWidth: '720px',
          height: '80vh',
          border: `1px solid ${currentTheme.border}`,
          borderRadius: '8px',
          boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
          backgroundColor: currentTheme.chatBg,
          overflow: 'hidden',
          display: 'flex',
          flexDirection: 'column'
        }}
      >
        {/* Chat Messages Area */}
        <div
          style={{
            flex: 1,
            overflowY: 'auto',
            padding: '16px',
            display: 'flex',
            flexDirection: 'column',
            gap: '12px'
          }}
        >
          {messages.map((message) => (
            <div
              key={message.id}
              style={{
                alignSelf: message.sender === 'user' ? 'flex-end' : 'flex-start',
                maxWidth: '75%',
                transform: message.animate 
                  ? (message.sender === 'user' ? 'translateX(20px)' : 'translateX(-20px)')
                  : 'translateX(0)',
                opacity: message.animate ? 0 : 1,
                transition: 'all 0.2s ease-out'
              }}
            >
              <div
                style={{
                  backgroundColor: message.sender === 'user' ? currentTheme.userBubble : currentTheme.systemBubble,
                  color: message.sender === 'user' ? currentTheme.userText : currentTheme.systemText,
                  padding: '10px 14px',
                  borderRadius: message.sender === 'user' ? '18px 18px 0 18px' : '18px 18px 18px 0',
                  fontSize: '14px',
                  wordBreak: 'break-word'
                }}
              >
                {message.text}
              </div>
              <div
                style={{
                  fontSize: '11px',
                  marginTop: '4px',
                  textAlign: message.sender === 'user' ? 'right' : 'left',
                  color: currentTheme.text,
                  opacity: 0.7,
                  display: 'flex',
                  justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
                  gap: '4px'
                }}
              >
                <span>{formatTime(message.timestamp)}</span>
                {message.sender === 'user' && (
                  <span style={{ color: message.status === 'read' ? '#2ecc71' : currentTheme.text }}>
                    {renderStatus(message.status)}
                  </span>
                )}
              </div>
            </div>
          ))}
          
          {isTyping && <TypingIndicator />}
          <div ref={messagesEndRef} />
        </div>
        
        {/* Input Area */}
        <form
          onSubmit={handleSendMessage}
          style={{
            display: 'flex',
            padding: '12px',
            backgroundColor: currentTheme.secondary,
            borderTop: `1px solid ${currentTheme.border}`
          }}
        >
          <input
            type="text"
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            placeholder="Type a message..."
            style={{
              flex: 1,
              padding: '10px 14px',
              borderRadius: '20px',
              border: `1px solid ${currentTheme.border}`,
              backgroundColor: currentTheme.inputBg,
              color: currentTheme.text,
              outline: 'none'
            }}
          />
          <button
            type="submit"
            style={{
              marginLeft: '8px',
              backgroundColor: currentTheme.primary,
              color: '#ffffff',
              border: 'none',
              padding: '0 16px',
              borderRadius: '20px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'background-color 0.2s'
            }}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" 
                 xmlns="http://www.w3.org/2000/svg">
              <path d="M22 2L11 13" stroke="white" strokeWidth="2" 
                    strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="white" strokeWidth="2" 
                    strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatWidget;
