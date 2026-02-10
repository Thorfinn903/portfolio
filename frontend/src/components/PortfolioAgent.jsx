import { useEffect, useState } from "react";
import ChatAssistant from "./ChatAssistant";
import { apiUrl } from "../lib/api";

export default function PortfolioAgent() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [isSystemWaking, setIsSystemWaking] = useState(false);

  const handleToggle = () => {
    setIsOpen((prev) => !prev);
  };

  const handleClose = () => {
    setIsOpen(false);
  };

  const sendMessage = async (preset) => {
    const messageText = (preset ?? input).trim();
    if (!messageText) return;

    const userMessage = { role: "user", text: messageText };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);
    setIsSystemWaking(false);
    const wakeTimer = setTimeout(() => {
      setIsSystemWaking(true);
    }, 4000);

    try {
      const res = await fetch(apiUrl("/chat"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: messageText }),
      });

      const data = await res.json();

      const botMessage = { role: "bot", text: data.answer };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Something went wrong. Please try again." },
      ]);
    } finally {
      clearTimeout(wakeTimer);
      setIsSystemWaking(false);
      setLoading(false);
    }
  };

  useEffect(() => {
    const handleOpen = () => {
      setIsOpen(true);
    };

    window.addEventListener("portfolio-agent:open", handleOpen);
    return () => window.removeEventListener("portfolio-agent:open", handleOpen);
  }, []);

  return (
    <>
      <ChatAssistant
        isOpen={isOpen}
        onToggle={handleToggle}
        onClose={handleClose}
        messages={messages}
        input={input}
        loading={loading}
        isSystemWaking={isSystemWaking}
        onInputChange={setInput}
        onSend={sendMessage}
      />
    </>
  );
}
