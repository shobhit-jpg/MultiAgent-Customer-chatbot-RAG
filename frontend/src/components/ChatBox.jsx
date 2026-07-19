import { useState, useEffect, useRef } from "react";
import axios from "axios";
import Message from "./Message";

function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState("");
  const [sessionId, setSessionId] = useState(null);
  const [loading, setLoading] = useState(false);

  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  // Create a new chat session
  useEffect(() => {
    const createSession = async () => {
      try {
        const res = await axios.post("/new-chat");

        console.log("New Session:", res.data);

        setSessionId(res.data.session_id);
      } catch (err) {
        console.error("Failed to create session:", err);
      }
    };

    createSession();
  }, []);

  useEffect(() => {
    console.log("Current Session ID:", sessionId);
  }, [sessionId]);

  // Auto scroll
  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  const sendMessage = async () => {
    if (!query.trim()) return;

    if (!sessionId) {
      alert("Session is not ready yet.");
      return;
    }

    const currentQuery = query.trim();

    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: currentQuery,
      },
    ]);

    setQuery("");
    setLoading(true);

    console.log("Sending:", {
      message: currentQuery,
      session_id: sessionId,
    });

    try {
      const res = await axios.post("/chat", {
        message: currentQuery,
        session_id: sessionId,
      });

      console.log("Response:", res.data);

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: res.data.response,
        },
      ]);
    } catch (err) {
      console.error(err);

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "Sorry, I couldn't connect to the server.",
        },
      ]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  return (
    <div className="chat">
      <header className="header">
        <h2>TechMart Chat Support</h2>
      </header>

      <div className="messages">
        {messages.length === 0 && (
          <div className="welcome">
            <div className="welcomeIcon">💬</div>
            <h1>TechMart Chat Support</h1>
            <p>Welcome to TechMart AI Support.</p>
            <p>
              Ask me about products, billing, warranty, refunds or technical
              support.
            </p>
          </div>
        )}

        {messages.map((msg, index) => (
          <Message key={index} message={msg} />
        ))}

        {loading && (
          <div className="typing">TechMart is typing...</div>
        )}

        <div ref={bottomRef}></div>
      </div>

      <div className="inputContainer">
        <div className="inputArea">
          <textarea
            ref={inputRef}
            rows="1"
            value={query}
            placeholder="Message TechMart..."
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
              }
            }}
          />

          <button onClick={sendMessage} disabled={loading}>
            ↑
          </button>
        </div>

        <p className="footerText">
          Session: {sessionId || "Creating..."}
        </p>

        <p className="footerText">
          Powered by TechMart AI Assistant
        </p>
      </div>
    </div>
  );
}

export default ChatBox;