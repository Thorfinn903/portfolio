import { useEffect, useState } from "react";
import { apiUrl } from "../lib/api";

export default function Skills() {
  const [skills, setSkills] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(apiUrl("/skills"))
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch skills");
        }
        return res.json();
      })
      .then((data) => {
        setSkills(data);
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
      <h1 className="text-h1 mb-6">Skills</h1>

      {Object.entries(skills).map(([category, items]) => (
        <div key={category} className="card mb-4">
          <h2 className="text-h3 capitalize">
            {category.replace("_", " ")}
          </h2>

          <ul className="mt-2 list-disc list-inside text-[#A7B0BF]">
            {Array.isArray(items)
              ? items.map((item) => <li key={item}>{item}</li>)
              : Object.values(items).flat().map((item) => (
                  <li key={item}>{item}</li>
                ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
