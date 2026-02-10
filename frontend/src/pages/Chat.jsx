import { useEffect, useState } from "react";
import ChatMessage from "../components/ChatMessage";
import { apiUrl } from "../lib/api";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("checking");

  useEffect(() => {
    fetch(apiUrl("/system/health"))
      .then((res) => res.json())
      .then((data) => setStatus(data.status))
      .catch(() => setStatus("offline"));
  }, []);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(apiUrl("/chat"), {
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

  return (
    <div className="page-compact space-y-4">
      <div>
        <h1 className="text-h1">Chat with me</h1>
        <p className="text-body-sm text-[#A7B0BF]">
          Ask about projects, experience, or technical decisions.
        </p>
      </div>

      <section className="chat-panel">
        <header className="chat-header">
          <div>
            <p className="text-body-sm font-semibold text-[#E6EAF2]">
              Portfolio Assistant
            </p>
            <div className="flex items-center gap-2 text-body-sm text-[#A7B0BF]">
              <span
                className={`status-dot ${status}`}
                title={`System Status: ${status}`}
              />
              FastAPI + LLM
            </div>
          </div>
          <span className="flex items-center gap-2 text-body-sm text-[#A7B0BF]">
            <span className={`status-dot ${loading ? "animate-pulse" : ""}`} />
            {loading ? "Thinking..." : "Ready"}
          </span>
        </header>

        <div className="chat-messages">
          {messages.length === 0 && (
            <p className="chat-empty">
              Start with: "Summarize your most impactful project."
            </p>
          )}

          {messages.map((m, i) => (
            <ChatMessage key={i} role={m.role} text={m.text} />
          ))}

          {loading && (
            <div className="mt-2 text-body-sm text-[#A7B0BF] animate-pulse">
              Bot is thinking...
            </div>
          )}
        </div>

        <div className="chat-input">
          <input
            className="chat-field"
            placeholder="Ask about my skills, projects..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button onClick={sendMessage} className="btn btn-primary">
            Send
          </button>
        </div>
      </section>
    </div>
  );
}
