import { Link, useLocation } from "react-router-dom";

export default function Navbar() {
  const { pathname } = useLocation();

  const navClass = (path) =>
    `nav-link ${pathname === path ? "nav-link-active" : ""}`;

  return (
    <nav className="border-b border-[#232B38] bg-[#0B0F14] px-6 py-4">
      <div className="mx-auto flex max-w-[1200px] flex-wrap gap-6">
        <Link to="/" className={navClass("/")}>Home</Link>
        <Link to="/profile" className={navClass("/profile")}>Profile</Link>
        <Link to="/projects" className={navClass("/projects")}>Projects</Link>
      </div>
    </nav>
  );
}
