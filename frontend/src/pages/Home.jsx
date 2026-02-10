import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { ArrowUpRight, Cpu, ShieldCheck } from "lucide-react";

const containerVariants = {
  hidden: {},
  show: {
    transition: { staggerChildren: 0.12 },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 16 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

export default function Home() {
  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="show"
      className="grid gap-10 lg:grid-cols-[1.1fr_0.9fr] lg:items-center"
    >
        <div className="space-y-6">
          <motion.div
            variants={itemVariants}
            className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs uppercase tracking-[0.3em] text-cyan-300 backdrop-blur-md"
          >
            <span className="relative flex h-2 w-2">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400/70" />
              <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-400" />
            </span>
            System Online
          </motion.div>

          <motion.h1
            variants={itemVariants}
            className="text-4xl font-semibold tracking-tight md:text-6xl"
          >
            <span className="text-cyan-300">I AM</span>{" "}
            <span className="text-white">B NARAYAN MAHAPATRA</span>
          </motion.h1>

          <motion.p
            variants={itemVariants}
            className="text-base text-slate-300 md:text-lg"
          >
            Calibrating high-signal systems, product interfaces, and AI workflows
            to deliver confident hiring decisions and measurable impact.
          </motion.p>

          <motion.div variants={itemVariants} className="flex flex-wrap gap-3">
            <Link
              to="/projects"
              className="inline-flex items-center gap-2 rounded-full border border-cyan-400/40 bg-cyan-400/10 px-5 py-3 text-sm font-semibold text-cyan-200 shadow-[0_0_18px_rgba(34,211,238,0.45)] transition hover:border-cyan-400/70 hover:bg-cyan-400/20"
            >
              View Protocol
              <ArrowUpRight className="h-4 w-4" />
            </Link>
            <Link
              to="/dashboard"
              className="inline-flex items-center gap-2 rounded-full border border-emerald-400/40 bg-emerald-400/10 px-5 py-3 text-sm font-semibold text-emerald-200 shadow-[0_0_18px_rgba(52,211,153,0.4)] transition hover:border-emerald-400/70 hover:bg-emerald-400/20"
            >
              Monitor Cortex
              <Cpu className="h-4 w-4" />
            </Link>
          </motion.div>
        </div>

        <div className="space-y-4">
          {[
            {
              title: "Mission Directive",
              icon: ShieldCheck,
              content:
                "Translate complex engineering into crisp outcomes recruiters can validate in seconds.",
            },
            {
              title: "Signal Matrix",
              icon: Cpu,
              content:
                "FastAPI, Python, SQL, and ERPNext with production-grade delivery metrics.",
            },
          ].map((item) => {
            const Icon = item.icon;
            return (
              <motion.div
                key={item.title}
                variants={itemVariants}
                className="rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur-md"
              >
                <div className="flex items-center gap-3 text-sm text-slate-300">
                  <Icon className="h-4 w-4 text-cyan-400" />
                  {item.title}
                </div>
                <p className="mt-3 text-sm text-slate-400">{item.content}</p>
              </motion.div>
            );
          })}
        </div>
      </motion.div>
  );
}
