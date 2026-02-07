export default function ChatMessage({ role, text }) {
  const isUser = role === "user";

  return (
    <div className={`flex mb-3 fade-in ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`chat-bubble ${
          isUser ? "chat-bubble-user rounded-br-md" : "chat-bubble-bot rounded-bl-md"
        }`}
      >
        {text}
      </div>
    </div>
  );
}
