import { AnimatePresence, motion } from "framer-motion";
import { Bot, Send, X } from "lucide-react";
import ChatMessage from "./ChatMessage";

const quickPrompts = ["Tech Stack?", "View Projects", "Contact Me"];
const promptToQuestion = {
  "Tech Stack?": "What is your tech stack?",
  "View Projects": "Tell me about your projects.",
  "Contact Me": "Share your contact information.",
};

export default function ChatAssistant({
  isOpen,
  onToggle,
  onClose,
  messages,
  input,
  loading,
  onInputChange,
  onSend,
}) {
  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-3">
      <AnimatePresence>
        {isOpen && (
          <motion.aside
            initial={{ opacity: 0, y: 24, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.98 }}
            transition={{ duration: 0.22, ease: "easeOut" }}
            className="flex h-[72vh] max-h-[620px] w-[min(92vw,380px)] flex-col overflow-hidden rounded-2xl border border-white/10 bg-slate-900/80 backdrop-blur-xl shadow-[0_20px_80px_rgba(0,0,0,0.55)]"
          >
            <header className="flex items-center justify-between border-b border-white/10 px-4 py-3">
              <div>
                <p className="text-xs uppercase tracking-[0.3em] text-cyan-300">
                  PA
                </p>
                <h3 className="text-sm font-semibold text-white">
                  Portfolio Assistant
                </h3>
              </div>
              <button
                type="button"
                onClick={onClose}
                className="inline-flex h-8 w-8 items-center justify-center rounded-full border border-white/10 bg-white/5 text-slate-300 transition hover:border-cyan-400/50 hover:text-cyan-200"
                aria-label="Close chat assistant"
              >
                <X className="h-4 w-4" />
              </button>
            </header>

            <div className="flex-1 overflow-y-auto px-4 py-4">
              {messages.length === 0 && (
                <div className="rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-300">
                  Ask me about skills, projects, experience, or contact details.
                </div>
              )}

              <div className="mt-3">
                {messages.map((m, i) => (
                  <ChatMessage key={i} role={m.role} text={m.text} />
                ))}
              </div>

              {loading && (
                <p className="mt-2 text-xs text-slate-400">Thinking...</p>
              )}
            </div>

            <div className="border-t border-white/10 px-3 pb-3 pt-2">
              {messages.length === 0 && (
                <div className="mb-3 flex flex-wrap gap-2">
                  {quickPrompts.map((prompt) => (
                    <button
                      key={prompt}
                      type="button"
                      onClick={() => onSend(promptToQuestion[prompt] || prompt)}
                      className="rounded-full border border-cyan-400/30 bg-cyan-400/10 px-3 py-1 text-xs font-semibold text-cyan-200 transition hover:border-cyan-400/70 hover:bg-cyan-400/20"
                    >
                      {prompt}
                    </button>
                  ))}
                </div>
              )}

              <div className="relative">
                <input
                  className="w-full rounded-xl border border-white/10 bg-slate-950/80 px-3 py-2 pr-12 text-sm text-slate-200 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400/40"
                  placeholder="Ask anything..."
                  value={input}
                  onChange={(e) => onInputChange(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && onSend()}
                />
                <button
                  type="button"
                  onClick={() => onSend()}
                  className="absolute right-1 top-1/2 inline-flex h-8 w-8 -translate-y-1/2 items-center justify-center rounded-lg border border-cyan-400/50 bg-cyan-400/15 text-cyan-200 transition hover:border-cyan-400 hover:bg-cyan-400/25"
                  aria-label="Send message"
                >
                  <Send className="h-4 w-4" />
                </button>
              </div>
            </div>
          </motion.aside>
        )}
      </AnimatePresence>

      <motion.button
        type="button"
        onClick={onToggle}
        className="relative inline-flex h-14 w-14 items-center justify-center rounded-full border border-cyan-300/40 bg-gradient-to-br from-cyan-400 to-indigo-500 text-slate-950 shadow-[0_0_25px_rgba(34,211,238,0.7)] transition hover:scale-105"
        whileTap={{ scale: 0.96 }}
        aria-label="Toggle chat assistant"
        aria-expanded={isOpen}
      >
        <Bot className="h-6 w-6" />
      </motion.button>
    </div>
  );
}
