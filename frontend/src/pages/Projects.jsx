import { useEffect, useState } from "react";

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

  if (loading) return <p className="state-loading">Loading...</p>;
  if (error) return <p className="state-error">Error: {error}</p>;

  return (
    <div className="space-y-6">
      <h1 className="text-h1 mb-6">Projects</h1>

      <div className="space-y-6">
        {projects.map((project) => (
          <div
            key={project.id}
            className="card"
          >
            <h2 className="card-title">{project.title}</h2>
            <p className="card-body mt-2">{project.description}</p>

            <div className="mt-3">
              <span className="text-body-sm font-semibold text-[#E6EAF2]">
                Tech Stack
              </span>
              <ul className="mt-2 list-disc list-inside text-[#A7B0BF]">
                {project.tech_stack.map((tech) => (
                  <li key={tech}>{tech}</li>
                ))}
              </ul>
            </div>

            <p className="card-meta mt-3">
              Status: {project.status}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
