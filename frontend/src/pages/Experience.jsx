import { useEffect, useState } from "react";

export default function Experience() {
  const [experience, setExperience] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/experience")
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch experience data");
        }
        return res.json();
      })
      .then((data) => {
        setExperience(data);
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
    <div className="page-narrow">
      <h1 className="text-h1 mb-6">Experience</h1>

      <div className="space-y-6">
        {experience.map((job, index) => (
          <div key={index} className="card">
            <h2 className="card-title">
              {job.role} - {job.company}
            </h2>

            <p className="card-meta">
              {job.duration} | {job.location}
            </p>

            <ul className="mt-2 list-disc list-inside text-[#A7B0BF]">
              {job.responsibilities.slice(0, 3).map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}
