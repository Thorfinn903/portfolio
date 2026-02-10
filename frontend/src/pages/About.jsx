import { useEffect, useState } from "react";
import { apiUrl } from "../lib/api";

export default function About() {
  const [aboutText, setAboutText] = useState("");
  const [contact, setContact] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([
      fetch(apiUrl("/about")).then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch about data");
        }
        return res.json();
      }),
      fetch(apiUrl("/contact")).then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch contact data");
        }
        return res.json();
      }),
    ])
      .then(([aboutData, contactData]) => {
        setAboutText(aboutData.content);
        setContact(contactData);
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

      {contact && (
        <div className="mt-6 space-y-2">
          <p className="text-body text-[#A7B0BF]">
            <span className="text-[#E6EAF2] font-semibold">Name:</span>{" "}
            {contact.name}
          </p>
          <p className="text-body text-[#A7B0BF]">
            <span className="text-[#E6EAF2] font-semibold">Email:</span>{" "}
            {contact.email}
          </p>
          <p className="text-body text-[#A7B0BF]">
            <span className="text-[#E6EAF2] font-semibold">Location:</span>{" "}
            {contact.location}
          </p>

          <div className="mt-4 flex flex-wrap gap-3">
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
      )}
    </div>
  );
}
