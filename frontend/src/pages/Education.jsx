import { useEffect, useState } from "react";
import { apiUrl } from "../lib/api";

export default function Education() {
  const [education, setEducation] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(apiUrl("/education"))
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch education data");
        }
        return res.json();
      })
      .then((data) => {
        setEducation(data);
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
      <h1 className="text-h1 mb-6">Education</h1>

      <div className="space-y-6">
        {education.map((edu, index) => (
          <div key={index} className="card">
            <h2 className="card-title">{edu.degree}</h2>
            <p className="card-body">{edu.institution}</p>
            <p className="card-meta">
              {edu.location} | {edu.duration}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
