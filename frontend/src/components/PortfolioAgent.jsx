import { useEffect, useMemo, useRef, useState } from "react";
import { useLocation } from "react-router-dom";
import AgentButton from "./AgentButton";
import AgentPanel from "./AgentPanel";

const INTRO_KEY = "seenAgentIntro";

export default function PortfolioAgent() {
  const { pathname } = useLocation();
  const isHome = useMemo(() => pathname === "/", [pathname]);
  const [isOpen, setIsOpen] = useState(false);
  const [isHalfOpen, setIsHalfOpen] = useState(false);
  const [showIntro, setShowIntro] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const autoOpenTimer = useRef(null);

  useEffect(() => {
    if (!isHome) return;

    const hasSeen = sessionStorage.getItem(INTRO_KEY) === "true";
    if (hasSeen) return;

    autoOpenTimer.current = setTimeout(() => {
      setIsOpen(true);
      setIsHalfOpen(true);
      setShowIntro(true);
      sessionStorage.setItem(INTRO_KEY, "true");
    }, 3000);

    return () => {
      if (autoOpenTimer.current) {
        clearTimeout(autoOpenTimer.current);
      }
    };
  }, [isHome]);

  const handleToggle = () => {
    if (autoOpenTimer.current) {
      clearTimeout(autoOpenTimer.current);
    }
    setIsOpen((prev) => {
      const next = !prev;
      setIsHalfOpen(false);
      setShowIntro(false);
      return next;
    });
  };

  const handleClose = () => {
    setIsOpen(false);
    setIsHalfOpen(false);
    setShowIntro(false);
    setMessages([]);
    setInput("");
    setLoading(false);
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: input }),
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
      setLoading(false);
    }
  };

  useEffect(() => {
    const handleOpen = () => {
      setIsOpen(true);
      setIsHalfOpen(false);
      setShowIntro(false);
    };

    window.addEventListener("portfolio-agent:open", handleOpen);
    return () => window.removeEventListener("portfolio-agent:open", handleOpen);
  }, []);

  return (
    <>
      <AgentButton isOpen={isOpen} onToggle={handleToggle} />
      <AgentPanel
        isOpen={isOpen}
        isHalfOpen={isHalfOpen}
        onClose={handleClose}
        showIntro={showIntro}
        messages={messages}
        input={input}
        loading={loading}
        onInputChange={setInput}
        onSend={sendMessage}
      />
    </>
  );
}
