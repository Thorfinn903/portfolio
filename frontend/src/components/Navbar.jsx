import { Link, useLocation } from "react-router-dom";

export default function Navbar() {
  const { pathname } = useLocation();

  const navClass = (path) =>
    `nav-link ${pathname === path ? "nav-link-active" : ""}`;

  return (
    <nav className="border-b border-[#232B38] bg-[#0B0F14] px-6 py-4">
      <div className="mx-auto flex max-w-3xl flex-wrap gap-6">
        <Link to="/" className={navClass("/")}>Home</Link>
        <Link to="/about" className={navClass("/about")}>About</Link>
        <Link to="/experience" className={navClass("/experience")}>Experience</Link>
        <Link to="/education" className={navClass("/education")}>Education</Link>
        <Link to="/skills" className={navClass("/skills")}>Skills</Link>
        <Link to="/projects" className={navClass("/projects")}>Projects</Link>
        <Link to="/certificates" className={navClass("/certificates")}>Certificates</Link>
        <Link to="/contact" className={navClass("/contact")}>Contact</Link>
        <Link to="/chat" className={navClass("/chat")}>Chat</Link>
      </div>
    </nav>
  );
}
