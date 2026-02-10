import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Github } from "lucide-react";

const containerVariants = {
  hidden: {},
  show: { transition: { staggerChildren: 0.12 } },
};

const cardVariants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

export default function Projects() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/projects")
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch projects");
        }
        return res.json();
      })
      .then((data) => {
        setProjects(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  let content = null;
  if (loading) {
    content = <p className="state-loading">Loading...</p>;
  } else if (error) {
    content = <p className="state-error">Error: {error}</p>;
  } else {
    content = (
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="show"
        className="grid gap-6 lg:grid-cols-2"
      >
        {projects.map((project) => {
          const githubUrl = project.link;

          return (
            <motion.div
              key={project.id}
              variants={cardVariants}
              className="group rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur-md transition duration-300 hover:-translate-y-1 hover:scale-[1.01] hover:border-cyan-400/40 hover:shadow-[0_0_30px_rgba(34,211,238,0.35)]"
            >
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="text-xs uppercase tracking-[0.3em] text-emerald-300">
                    {project.domain || "Field Ops"}
                  </p>
                  <h2 className="mt-2 text-xl font-semibold text-white">
                    {project.title}
                  </h2>
                </div>
                <span className="whitespace-nowrap rounded-full border border-white/10 bg-white/5 px-2 py-0.5 text-[10px] uppercase tracking-[0.18em] text-cyan-200">
                  {project.status}
                </span>
              </div>

              <p className="mt-3 text-sm text-slate-400">
                {project.description}
              </p>

              <div className="mt-4 flex flex-wrap gap-2">
                {project.tech_stack.map((tech) => (
                  <span
                    key={tech}
                    className="rounded-full border border-cyan-400/30 bg-cyan-400/10 px-3 py-1 text-xs font-semibold text-cyan-200"
                  >
                    {tech}
                  </span>
                ))}
              </div>

              <div className="mt-6 flex flex-wrap gap-3">
                <a
                  href={githubUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs font-semibold uppercase tracking-[0.2em] text-white transition hover:border-cyan-400/60 hover:text-cyan-200"
                >
                  <Github className="h-4 w-4 text-cyan-400" />
                  GitHub
                </a>
              </div>
            </motion.div>
          );
        })}
      </motion.div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <p className="text-xs uppercase tracking-[0.35em] text-cyan-400">
          Data Pads
        </p>
        <h1 className="mt-2 text-3xl font-semibold">Projects</h1>
        <p className="mt-2 text-sm text-slate-400">
          High-signal work with clear outcomes and measurable impact.
        </p>
      </div>

      {content}
    </div>
  );
}
