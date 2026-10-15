"use client";

import { useState, useRef, useEffect } from "react";
import {
  Download,
  Mic,
  Paperclip,
  Send,
  ThumbsUp,
  ThumbsDown,
  Bot,
  User,
  Copy,
  X
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { Card } from "@/components/ui/card"
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter"
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import axios from "axios";
import { TIMEOUT } from "dns";


type Message = {
  id: string;
  content: string;
  role: "user" | "assistant";
  timestamp: Date;
  quickReplies?: string[];
  isLoading?: boolean;
};

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [exportIframe,setExportIframe] = useState(false);
  const [copied, setCopied] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const exportTextRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    setMessages([
      {
        id: "1",
        content: "Hello! How can I assist you today?",
        role: "assistant",
        timestamp: new Date(Date.now() - 3600000),
        quickReplies: [
          "Tell me about your features",
          "How do I integrate with my website?",
          "Pricing information",
        ],
      },
      {
        id: "2",
        content: "I need help setting up document training for my bot.",
        role: "user",
        timestamp: new Date(Date.now() - 1800000),
      },
      {
        id: "3",
        content:
          "Sure, I can help with that. To train your bot with documents, you'll need to upload them in the Training Docs section. You can upload Google Docs, PDFs, or text files. Would you like me to guide you through the process?",
        role: "assistant",
        timestamp: new Date(Date.now() - 1700000),
        quickReplies: [
          "Yes, show me how",
          "What file types are supported?",
          "How long does training take?",
        ],
      },
    ]);
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
  
    const userMessage: Message = {
      id: `user-${Date.now()}`,
      content: input,
      role: "user",
      timestamp: new Date(),
    };
  
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
  
    // Show loading message
    const loadingId = `assistant-loading-${Date.now()}`;
    setMessages((prev) => [
      ...prev,
      {
        id: loadingId,
        content: "",
        role: "assistant",
        timestamp: new Date(),
        isLoading: true,
      },
    ]);
  
    try {
   
      const response = await axios.post(
        "http://10.251.75.84:8000/v1/query/prompt?user_id=67f2cedfe24b7b94d496ebb4",
        {
          query: input,
        },
        {
          headers: {
            "x-api-key": "entities-api-key"      
          },
        }
      );

      const answer = response.data.data?.answer?.data?.llm_answer || "No answer found.";
  
      // Remove loading and add assistant's response
      setMessages((prev) => {
        const newMessages = prev.filter((m) => m.id !== loadingId);
        return [
          ...newMessages,
          {
            id: `assistant-${Date.now()}`,
            content: answer,
            role: "assistant",
            timestamp: new Date(),
            quickReplies: [
              "Tell me more",
              "That's not what I meant",
              "Thank you",
            ],
          },
        ];
      });
    } catch (err) {
      setMessages((prev) => {
        const newMessages = prev.filter((m) => m.id !== loadingId);
        return [
          ...newMessages,
          {
            id: `assistant-${Date.now()}`,
            content: "Sorry, I couldn't get a response from the server.",
            role: "assistant",
            timestamp: new Date(),
          },
        ];
      });
    }
  };
  

  const handleQuickReply = async (reply: string) => {
    const userMessage: Message = {
      id: `user-${Date.now()}`,
      content: reply,
      role: "user",
      timestamp: new Date(),
    };
  
    setMessages((prev) => [...prev, userMessage]);
  
    // Show loading message
    const loadingId = `assistant-loading-${Date.now()}`;
    setMessages((prev) => [
      ...prev,
      {
        id: loadingId,
        content: "",
        role: "assistant",
        timestamp: new Date(),
        isLoading: true,
      },
    ]);
  
    try {
      const response = await axios.post(
        "http://10.251.75.84:8000/v1/query/prompt?user_id=67f2cedfe24b7b94d496ebb4",
        {
          query: reply,
        },
        {
          headers: {
            "x-api-key": "entities-api-key"
          },
        }
      );

      const answer = response.data.data?.answer?.data?.llm_answer || "No answer found.";
  
      setMessages((prev) => {
        const newMessages = prev.filter((m) => m.id !== loadingId);
        return [
          ...newMessages,
          {
            id: `assistant-${Date.now()}`,
            content: answer,
            role: "assistant",
            timestamp: new Date(),
            quickReplies: [
              "Tell me more",
              "That's not what I meant",
              "Thank you",
            ],
          },
        ];
      });
    } catch (err) {
      setMessages((prev) => {
        const newMessages = prev.filter((m) => m.id !== loadingId);
        return [
          ...newMessages,
          {
            id: `assistant-${Date.now()}`,
            content: "Sorry, I couldn't get a response from the server.",
            role: "assistant",
            timestamp: new Date(),
          },
        ];
      });
    }
  };
  

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  };

  const formatDate = (date: Date) => {
    return date.toLocaleDateString([], {
      year: "numeric",
      month: "long",
      day: "numeric",
    })
  }

  const getExportText = () => {

  return `
      <iframe
        src="http://localhost:3000/chat-iframe"
        width="400"
        height="600"
        allow="clipboard-write"
      ></iframe>
  `
  }

  const copyToClipboard = () => {
    const text = getExportText()
    navigator.clipboard.writeText(text).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    })
  }

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between border-b border-gray-200 dark:border-gray-800 p-4">
        <div className="flex items-center gap-2">
          <Bot className="h-5 w-5 text-blue-500" />
          <h2 className="text-lg font-semibold">Chat Session</h2>
        </div>
        <Button onClick={() => setExportIframe(true)} variant="outline" size="sm" className="flex items-center gap-1 cursor-pointer">
          <Download className="h-4 w-4" />
          <span>Export Chat</span>
        </Button>
      </div>
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={cn(
              "mb-4 flex",
              message.role === "user" ? "justify-end" : "justify-start"
            )}
          >
            <div
              className={cn(
                "max-w-[80%] rounded-lg p-4",
                message.role === "user"
                  ? "bg-blue-500 text-white"
                  : "bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100"
              )}
            >
              {message.isLoading ? (
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 animate-bounce rounded-full bg-current"></div>
                  <div className="h-2 w-2 animate-bounce rounded-full bg-current [animation-delay:0.2s]"></div>
                  <div className="h-2 w-2 animate-bounce rounded-full bg-current [animation-delay:0.4s]"></div>
                </div>
              ) : (
                <>
                  <div className="flex items-center gap-2 mb-1">
                    {message.role === "assistant" ? (
                      <Bot className="h-4 w-4 text-gray-500 dark:text-gray-400" />
                    ) : (
                      <User className="h-4 w-4" />
                    )}
                    <span className="text-xs opacity-70">{formatTime(message.timestamp)}</span>
                  </div>
                  <p>{message.content}</p>

                  {message.role === "assistant" && message.quickReplies && (
                    <div className="mt-2 flex flex-wrap gap-2">
                      {message.quickReplies.map((reply, index) => (
                        <Button
                          key={index}
                          variant="secondary"
                          size="sm"
                          className="text-xs bg-white/10 dark:bg-white/10 text-gray-900 dark:text-gray-100"
                          onClick={() => handleQuickReply(reply)}
                        >
                          {reply}
                        </Button>
                      ))}
                    </div>
                  )}

                  {message.role === "assistant" && (
                    <div className="mt-2 flex items-center gap-2">
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-6 w-6 text-gray-700 dark:text-gray-300"
                      >
                        <ThumbsUp className="h-3 w-3" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-6 w-6 text-gray-700 dark:text-gray-300"
                      >
                        <ThumbsDown className="h-3 w-3" />
                      </Button>
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="border-t border-gray-200 dark:border-gray-800 p-4">
        <div className="flex items-center gap-2">
          <Button variant="outline" size="icon">
            <Paperclip className="h-4 w-4" />
          </Button>
          <div className="relative flex-1">
            <Input
              placeholder="Type your message..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              className="pr-10"
            />
            <Button
              variant="ghost"
              size="icon"
              className={cn(
                "absolute right-0 top-0 h-full",
                isRecording && "text-red-500"
              )}
              onClick={() => setIsRecording(!isRecording)}
            >
              <Mic className="h-4 w-4" />
            </Button>
          </div>
          <Button
            onClick={handleSend}
            className="bg-blue-500 hover:bg-blue-600 text-white"
          >
            <Send className="h-4 w-4 mr-2" />
            Send
          </Button>
        </div>
      </div>

      {exportIframe && (
        <div
          className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
          onClick={(e) => {
            // Close the overlay when clicking the background (not the card)
            if (e.target === e.currentTarget) {
              setExportIframe(false)
            }
          }}
        >
          <Card className="w-full max-w-2xl max-h-[80vh] flex flex-col">
            <div
              ref={exportTextRef}
              className="flex-1 overflow-y-auto p-4 whitespace-pre-wrap text-orange-400 font-mono text-sm bg-gray-50 dark:bg-gray-900 rounded-b-lg"
            >
              <div className="flex justify-end">
                <Button
                    variant="outline"
                    size="sm"
                    className={cn(
                      "flex items-center gap-1 cursor-pointer",
                      copied && "bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300",
                    )}
                    onClick={copyToClipboard}
                  >
                    <Copy className="h-4 w-4" />
                  </Button>
              </div>
              <SyntaxHighlighter
                  language="html"
                  style={oneDark}
                  customStyle={{
                    background: 'transparent',
                    fontSize: '1.1rem',
                    fontFamily: 'monospace',
                    color: '#fb923c', // Tailwind orange-400
                  }}
                  codeTagProps={{
                    className: 'whitespace-pre-wrap'
                  }}
                >
                  {getExportText()}
            </SyntaxHighlighter>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}
