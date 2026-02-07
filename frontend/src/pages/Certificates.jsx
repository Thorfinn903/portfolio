import { useEffect, useState } from "react";

export default function Certificates() {
  const [certificates, setCertificates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/certificates")
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch certificates");
        }
        return res.json();
      })
      .then((data) => {
        setCertificates(data);
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
      <h1 className="text-h1 mb-6">Certificates</h1>

      <ul className="space-y-4">
        {certificates.map((cert, index) => (
          <li key={index} className="card">
            <p className="card-title">{cert.title}</p>
            <p className="card-meta">{cert.platform}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
