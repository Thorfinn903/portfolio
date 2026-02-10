import ChatMessage from "./ChatMessage";

export default function AgentPanel({
  isOpen,
  isHalfOpen,
  onClose,
  showIntro,
  messages,
  input,
  loading,
  onInputChange,
  onSend,
}) {
  const stateClass = isOpen
    ? isHalfOpen
      ? "agent-panel-half"
      : "agent-panel-open"
    : "agent-panel-closed";

  return (
    <aside className={`agent-panel ${stateClass}`} aria-hidden={!isOpen}>
      <header className="agent-panel-header">
        <div className="agent-header-title">
          <span className="text-body font-semibold text-[color:var(--color-text)]">
            Portfolio Agent
          </span>
          <span className="agent-header-pill">Recruiter View</span>
        </div>
        <button
          type="button"
          onClick={onClose}
          className="agent-close"
          aria-label="Close Portfolio Agent"
        >
          Close
        </button>
      </header>

      <div className="agent-panel-body">
        {showIntro && (
          <div className="agent-intro">
            I’m the Portfolio Agent. I can quickly summarize Narayan’s profile,
            skills, and projects to support hiring decisions.
          </div>
        )}
        <div className="agent-chat">
          {messages.length === 0 && !showIntro && (
            <div className="agent-empty">
              Ask me about skills, projects, or role fit.
            </div>
          )}

          {messages.map((m, i) => (
            <ChatMessage key={i} role={m.role} text={m.text} />
          ))}

          {loading && (
            <div className="text-body-sm text-[color:var(--color-text-muted)]">
              Thinking...
            </div>
          )}
        </div>

        <div className="agent-input">
          <input
            className="chat-field"
            placeholder="Ask about skills, projects, or role fit..."
            value={input}
            onChange={(e) => onInputChange(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && onSend()}
          />
          <button type="button" className="btn btn-primary" onClick={onSend}>
            Send
          </button>
        </div>
      </div>
    </aside>
  );
}
