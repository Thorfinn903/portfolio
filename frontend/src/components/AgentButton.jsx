export default function AgentButton({ isOpen, onToggle }) {
  return (
    <button
      type="button"
      aria-label="Toggle Portfolio Agent"
      aria-expanded={isOpen}
      onClick={onToggle}
      className="agent-button"
    >
      PA
    </button>
  );
}
