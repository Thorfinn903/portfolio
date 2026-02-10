import { useEffect, useState } from "react";
import { apiUrl } from "../lib/api";

export default function Contact() {
  const [contact, setContact] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(apiUrl("/contact"))
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch contact data");
        }
        return res.json();
      })
      .then((data) => {
        setContact(data);
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
    <div className="page-compact space-y-2">
      <h1 className="text-h1 mb-2">Contact</h1>

      <p className="text-body text-[#A7B0BF]">
        <span className="text-[#E6EAF2] font-semibold">Name:</span> {contact.name}
      </p>
      <p className="text-body text-[#A7B0BF]">
        <span className="text-[#E6EAF2] font-semibold">Email:</span> {contact.email}
      </p>
      <p className="text-body text-[#A7B0BF]">
        <span className="text-[#E6EAF2] font-semibold">Location:</span> {contact.location}
      </p>

      <div className="mt-6 flex flex-wrap gap-3">
        <a
          href={contact.github}
          target="_blank"
          rel="noreferrer"
          className="btn btn-outline"
        >
          GitHub
        </a>
        <a
          href={contact.linkedin}
          target="_blank"
          rel="noreferrer"
          className="btn btn-outline"
        >
          LinkedIn
        </a>
      </div>
    </div>
  );
}
