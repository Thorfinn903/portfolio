import { useEffect, useMemo, useState } from "react";
import { motion } from "framer-motion";
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ResponsiveContainer,
} from "recharts";
import {
  Activity,
  Cpu,
  Gauge,
  Radar as RadarIcon,
  Terminal,
  WifiOff,
} from "lucide-react";
import { apiUrl } from "../lib/api";

const containerVariants = {
  hidden: {},
  show: {
    transition: { staggerChildren: 0.12 },
  },
};

const cardVariants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

export default function Dashboard() {
  const [health, setHealth] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [offline, setOffline] = useState(false);
  const [tick, setTick] = useState(0);

  useEffect(() => {
    let cancelled = false;

    const fetchAll = async () => {
      try {
        const [healthRes, analyticsRes] = await Promise.all([
          fetch(apiUrl("/system/health")),
          fetch(apiUrl("/system/analytics")),
        ]);

        if (!healthRes.ok || !analyticsRes.ok) {
          throw new Error("backend_unreachable");
        }

        const [healthData, analyticsData] = await Promise.all([
          healthRes.json(),
          analyticsRes.json(),
        ]);

        if (!cancelled) {
          setHealth(healthData);
          setAnalytics(analyticsData);
          setOffline(false);
          setTick((t) => t + 1);
        }
      } catch {
        if (!cancelled) {
          setOffline(true);
        }
      }
    };

    fetchAll();
    const interval = setInterval(fetchAll, 5000);
    return () => {
      cancelled = true;
      clearInterval(interval);
    };
  }, []);

  const status = offline ? "offline" : health?.status || "processing";
  const statusStyles =
    status === "healthy"
      ? "text-emerald-400 shadow-[0_0_15px_rgba(52,211,153,0.5)]"
      : status === "degraded"
      ? "text-rose-500"
      : "text-cyan-400 animate-pulse";

  const totalRequests = health?.pipeline_requests_total ?? "--";
  const avgLatency = health?.average_latency_ms ?? "--";
  const llmFailures = health?.llm_failures_total ?? 0;
  const llmRequests = health?.llm_requests_total ?? 0;
  const successRate =
    llmRequests > 0
      ? `${Math.max(0, Math.round(((llmRequests - llmFailures) / llmRequests) * 100))}%`
      : "--";

  const intents = analytics?.intent_counts || [];
  const recruiters = analytics?.recruiter_types || [];

  const radarData = useMemo(() => {
    const map = new Map(recruiters);
    return [
      { name: "TECH", value: map.get("TECH_LEAD") || 0 },
      { name: "HR", value: map.get("HR_MANAGER") || 0 },
      { name: "PRODUCT", value: map.get("PRODUCT_MANAGER") || 0 },
      { name: "GENERAL", value: map.get("GENERALIST") || 0 },
    ];
  }, [recruiters]);

  const liveLog = useMemo(() => {
    if (!intents.length) return ["[SYSTEM] Waiting for signals..."];
    return intents.slice(0, 6).map(
      ([name, count]) => `[SYSTEM] Detected: ${name} (${count})`
    );
  }, [intents, tick]);

  return (
      <div className="px-6 py-12 md:px-10">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="flex flex-wrap items-center justify-between gap-6"
        >
          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-cyan-400">
              V4.0 Intelligence Dashboard
            </p>
            <h1 className="mt-2 text-3xl font-semibold md:text-4xl">
              AI System Intelligence
            </h1>
            <p className="mt-2 text-sm text-slate-400">
              Monitoring real-time behavior, latency, and recruiter patterns.
            </p>
          </div>
          <div className="flex items-center gap-3 rounded-full border border-white/10 bg-white/5 px-4 py-2 backdrop-blur-md">
            <motion.span
              className={`inline-flex items-center gap-2 text-sm font-semibold ${statusStyles}`}
              animate={{ opacity: [0.6, 1, 0.6] }}
              transition={{ duration: 1.6, repeat: Infinity }}
            >
              <span className="relative flex h-2 w-2">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-cyan-400/70" />
                <span className="relative inline-flex h-2 w-2 rounded-full bg-cyan-400" />
              </span>
              {status.toUpperCase()}
            </motion.span>
            {offline && <WifiOff className="h-4 w-4 text-rose-500" />}
          </div>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="show"
          className="mt-10 grid gap-4 md:grid-cols-3"
        >
          <motion.div
            variants={cardVariants}
            className="rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur-md"
          >
            <div className="flex items-center justify-between">
              <p className="text-sm text-slate-400">Total Requests</p>
              <Activity className="h-5 w-5 text-cyan-400" />
            </div>
            <p className="mt-4 text-3xl font-semibold text-cyan-300">
              {totalRequests}
            </p>
          </motion.div>

          <motion.div
            variants={cardVariants}
            className="rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur-md"
          >
            <div className="flex items-center justify-between">
              <p className="text-sm text-slate-400">Avg Latency (ms)</p>
              <Gauge className="h-5 w-5 text-emerald-400" />
            </div>
            <p className="mt-4 text-3xl font-semibold text-emerald-300">
              {avgLatency}
            </p>
          </motion.div>

          <motion.div
            variants={cardVariants}
            className="rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur-md"
          >
            <div className="flex items-center justify-between">
              <p className="text-sm text-slate-400">Success Rate</p>
              <Cpu className="h-5 w-5 text-emerald-400" />
            </div>
            <p className="mt-4 text-3xl font-semibold text-emerald-300">
              {successRate}
            </p>
            <p className="mt-2 text-xs text-slate-500">
              LLM Failures: {llmFailures}
            </p>
          </motion.div>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="show"
          className="mt-6 grid grid-cols-1 gap-4 lg:grid-cols-3"
        >
          <motion.div
            variants={cardVariants}
            className="relative flex h-full flex-col rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur-md lg:col-span-2"
          >
            <div className="flex items-center gap-3 text-sm text-slate-300">
              <Terminal className="h-4 w-4 text-cyan-400" />
              Live Activity Log
            </div>
            <div className="mt-4 h-44 overflow-hidden rounded-xl border border-white/10 bg-black/40 px-4 py-3 font-mono text-xs text-emerald-300">
              <motion.div
                className="absolute right-8 top-6 h-40 w-px bg-cyan-400/60"
                animate={{ y: [0, 40, 0] }}
                transition={{ duration: 3.2, repeat: Infinity }}
              />
              <div className="space-y-2">
                {liveLog.map((line, idx) => (
                  <p key={`${line}-${idx}`}>{line}</p>
                ))}
              </div>
            </div>
          </motion.div>

          <motion.div
            variants={cardVariants}
            className="flex h-full flex-col rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur-md"
          >
            <div className="flex items-center gap-3 text-sm text-slate-300">
              <RadarIcon className="h-4 w-4 text-cyan-400" />
              Recruiter Radar
            </div>
            <div className="mt-4 h-44">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart
                  data={radarData}
                  outerRadius="65%"
                  margin={{ top: 0, right: 40, bottom: 0, left: 40 }}
                >
                  <PolarGrid stroke="rgba(148,163,184,0.25)" />
                  <PolarAngleAxis
                    dataKey="name"
                    tick={{ fontSize: 10, fill: "#94a3b8" }}
                  />
                  <PolarRadiusAxis
                    tick={{ fill: "#64748b" }}
                    axisLine={false}
                  />
                  <Radar
                    dataKey="value"
                    stroke="#22d3ee"
                    fill="#22d3ee"
                    fillOpacity={0.25}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </motion.div>
        </motion.div>
      </div>
  );
}
