import { useEffect, useMemo, useState } from "react";
import { motion } from "framer-motion";
import {
  Award,
  BriefcaseBusiness,
  Cpu,
  GraduationCap,
  MapPin,
  ScanFace,
  ScrollText,
  Sparkles,
} from "lucide-react";

const revealProps = {
  initial: { opacity: 0, y: 50 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true, amount: 0.2 },
  transition: { duration: 0.5, ease: "easeOut" },
};

function normalizeSkills(skillsPayload) {
  if (!skillsPayload || typeof skillsPayload !== "object") return [];

  return Object.entries(skillsPayload).map(([category, value]) => {
    const items = Array.isArray(value)
      ? value
      : Object.values(value || {}).flat().filter(Boolean);

    return {
      category: category.replaceAll("_", " "),
      items,
    };
  });
}

export default function Profile() {
  const [profileData, setProfileData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;

    const loadData = async () => {
      try {
        const [
          aboutRes,
          contactRes,
          expRes,
          educationRes,
          skillsRes,
          certificatesRes,
          projectsRes,
        ] = await Promise.all([
          fetch("http://127.0.0.1:8000/about"),
          fetch("http://127.0.0.1:8000/contact"),
          fetch("http://127.0.0.1:8000/experience"),
          fetch("http://127.0.0.1:8000/education"),
          fetch("http://127.0.0.1:8000/skills"),
          fetch("http://127.0.0.1:8000/certificates"),
          fetch("http://127.0.0.1:8000/projects"),
        ]);

        const responses = [
          aboutRes,
          contactRes,
          expRes,
          educationRes,
          skillsRes,
          certificatesRes,
          projectsRes,
        ];

        if (responses.some((res) => !res.ok)) {
          throw new Error("Failed to load dossier data");
        }

        const [
          aboutData,
          contactData,
          experienceData,
          educationData,
          skillsData,
          certificatesData,
          projectsData,
        ] = await Promise.all(responses.map((res) => res.json()));

        if (!cancelled) {
          setProfileData({
            about: aboutData?.content || "",
            contact: contactData || {},
            experience: Array.isArray(experienceData) ? experienceData : [],
            education: Array.isArray(educationData) ? educationData : [],
            skills: skillsData || {},
            certificates: Array.isArray(certificatesData) ? certificatesData : [],
            projects: Array.isArray(projectsData) ? projectsData : [],
          });
          setLoading(false);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message || "Unable to load profile");
          setLoading(false);
        }
      }
    };

    loadData();

    return () => {
      cancelled = true;
    };
  }, []);

  const skillGroups = useMemo(
    () => normalizeSkills(profileData?.skills),
    [profileData?.skills]
  );

  if (loading) return <p className="state-loading">Loading dossier...</p>;
  if (error) return <p className="state-error">Error: {error}</p>;

  const headerName = profileData?.contact?.name || "B Narayan Mahapatra";
  const headerRole = "Student & Backend Engineer";
  const headerLocation =
    profileData?.contact?.location || "Surat, Gujarat (Roots in Odisha)";

  return (
    <div className="space-y-8">
      <motion.section
        {...revealProps}
        className="rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur-md"
      >
        <div className="flex flex-wrap items-start justify-between gap-6">
          <div>
            <p className="text-xs uppercase tracking-[0.35em] text-cyan-400">
              Personnel Dossier
            </p>
            <h1 className="mt-2 text-3xl font-semibold text-slate-100">
              {headerName}
            </h1>
            <p className="mt-2 flex items-center gap-2 text-sm text-slate-300">
              <ScanFace className="h-4 w-4 text-cyan-400" />
              {headerRole}
            </p>
            <p className="mt-1 flex items-center gap-2 text-sm text-slate-400">
              <MapPin className="h-4 w-4 text-cyan-400" />
              {headerLocation}
            </p>
          </div>
          <div className="rounded-xl border border-cyan-400/30 bg-cyan-400/10 px-4 py-2 text-xs uppercase tracking-[0.25em] text-cyan-200 shadow-[0_0_16px_rgba(34,211,238,0.28)]">
            AI Portfolio Node
          </div>
        </div>
        <p className="mt-6 rounded-xl border border-white/10 bg-black/30 px-4 py-3 text-sm leading-6 text-slate-300">
          {profileData.about || "Backend architecture, ERPNext, and AI systems."}
        </p>
      </motion.section>

      <motion.section
        {...revealProps}
        className="rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur-md"
      >
        <div className="mb-5 flex items-center gap-2">
          <BriefcaseBusiness className="h-4 w-4 text-cyan-400" />
          <h2 className="text-sm uppercase tracking-[0.25em] text-cyan-400">
            Experience
          </h2>
        </div>
        <div className="space-y-4">
          {profileData.experience.map((item, index) => (
            <div
              key={`${item.company}-${item.role}-${index}`}
              className="rounded-xl border border-white/10 bg-black/30 p-4"
            >
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <h3 className="text-lg font-semibold text-slate-100">
                    {item.role}
                  </h3>
                  <p className="text-sm text-cyan-300">{item.company}</p>
                </div>
                <div className="text-right text-xs uppercase tracking-[0.2em] text-slate-400">
                  <p>{item.duration}</p>
                  <p>{item.location}</p>
                </div>
              </div>
              <ul className="mt-3 list-disc space-y-1 pl-5 text-sm text-slate-300">
                {(item.responsibilities || []).map((point) => (
                  <li key={point}>{point}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </motion.section>

      <motion.section
        {...revealProps}
        className="rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur-md"
      >
        <div className="mb-5 flex items-center gap-2">
          <GraduationCap className="h-4 w-4 text-cyan-400" />
          <h2 className="text-sm uppercase tracking-[0.25em] text-cyan-400">
            Education
          </h2>
        </div>
        <div className="grid gap-4 md:grid-cols-2">
          {profileData.education.map((item, index) => (
            <div
              key={`${item.institution}-${index}`}
              className="rounded-xl border border-white/10 bg-black/30 p-4"
            >
              <p className="text-base font-semibold text-slate-100">{item.degree}</p>
              <p className="mt-1 text-sm text-cyan-300">{item.institution}</p>
              <p className="mt-2 text-xs uppercase tracking-[0.2em] text-slate-400">
                {item.location}
              </p>
              <p className="mt-1 text-xs uppercase tracking-[0.2em] text-slate-400">
                {item.duration}
              </p>
            </div>
          ))}
        </div>
      </motion.section>

      <motion.section
        {...revealProps}
        className="rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur-md"
      >
        <div className="mb-5 flex items-center gap-2">
          <Cpu className="h-4 w-4 text-cyan-400" />
          <h2 className="text-sm uppercase tracking-[0.25em] text-cyan-400">
            Skills Matrix
          </h2>
        </div>
        <div className="space-y-4">
          {skillGroups.map((group) => (
            <div key={group.category} className="space-y-2">
              <p className="text-xs uppercase tracking-[0.2em] text-slate-400">
                {group.category}
              </p>
              <div className="flex flex-wrap gap-2">
                {group.items.map((item) => (
                  <span
                    key={`${group.category}-${item}`}
                    className="rounded-full border border-cyan-400/30 bg-cyan-400/10 px-3 py-1 text-xs font-semibold text-cyan-200 shadow-[0_0_14px_rgba(34,211,238,0.2)]"
                  >
                    {item}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </motion.section>

      <motion.section
        {...revealProps}
        className="rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur-md"
      >
        <div className="mb-5 flex items-center gap-2">
          <Award className="h-4 w-4 text-cyan-400" />
          <h2 className="text-sm uppercase tracking-[0.25em] text-cyan-400">
            Certificates
          </h2>
        </div>
        <div className="grid gap-3 md:grid-cols-2">
          {profileData.certificates.map((cert, index) => (
            <div
              key={`${cert.title}-${index}`}
              className="rounded-xl border border-white/10 bg-black/30 px-4 py-3"
            >
              <p className="text-sm font-semibold text-slate-100">{cert.title}</p>
              <p className="mt-1 text-xs uppercase tracking-[0.2em] text-slate-400">
                {cert.platform}
              </p>
            </div>
          ))}
        </div>
      </motion.section>

      <motion.section
        {...revealProps}
        className="rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur-md"
      >
        <div className="mb-5 flex items-center gap-2">
          <ScrollText className="h-4 w-4 text-cyan-400" />
          <h2 className="text-sm uppercase tracking-[0.25em] text-cyan-400">
            Project Archive
          </h2>
        </div>
        <div className="space-y-4">
          {profileData.projects.map((project) => (
            <div
              key={project.id}
              className="rounded-xl border border-white/10 bg-black/30 p-4"
            >
              <div className="flex flex-wrap items-center justify-between gap-3">
                <h3 className="text-base font-semibold text-slate-100">
                  {project.title}
                </h3>
                <span className="rounded-full border border-emerald-400/30 bg-emerald-400/10 px-2 py-0.5 text-[10px] uppercase tracking-[0.2em] text-emerald-200">
                  {project.status}
                </span>
              </div>
              <p className="mt-2 text-sm text-slate-300">{project.description}</p>
              <div className="mt-3 flex flex-wrap gap-2">
                {(project.tech_stack || []).map((tech) => (
                  <span
                    key={`${project.id}-${tech}`}
                    className="rounded-full border border-cyan-400/30 bg-cyan-400/10 px-2.5 py-1 text-xs text-cyan-200"
                  >
                    {tech}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </motion.section>

      <motion.section
        {...revealProps}
        className="rounded-2xl border border-white/10 bg-white/5 p-5 backdrop-blur-md"
      >
        <div className="flex items-center gap-2 text-sm text-emerald-300">
          <Sparkles className="h-4 w-4" />
          Neural Roadmap: Building backend architecture and AI systems for high-trust B2B products.
        </div>
      </motion.section>
    </div>
  );
}
