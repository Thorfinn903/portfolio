import { useEffect, useState } from "react";

export default function About() {
  const [aboutText, setAboutText] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/about")
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch about data");
        }
        return res.json();
      })
      .then((data) => {
        setAboutText(data.content);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <p className="state-loading">Loading...</p>;
  }

  if (error) {
    return <p className="state-error">Error: {error}</p>;
  }

  return (
    <div className="page-narrow">
      <h1 className="text-h1 mb-4">About Me</h1>
      <pre className="whitespace-pre-wrap text-body text-[#A7B0BF]">
        {aboutText}
      </pre>
    </div>
  );
}
