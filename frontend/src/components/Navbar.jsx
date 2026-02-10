import { Link, useLocation } from "react-router-dom";
import { motion } from "framer-motion";
import { Cpu, FolderGit2, LayoutDashboard, User } from "lucide-react";

export default function Navbar() {
  const { pathname } = useLocation();

  const navItems = [
    { to: "/", label: "Home", icon: Cpu },
    { to: "/profile", label: "Profile", icon: User },
    { to: "/projects", label: "Projects", icon: FolderGit2 },
    { to: "/dashboard", label: "Cortex", icon: LayoutDashboard },
  ];

  return (
    <nav className="sticky top-0 z-40 border-b border-white/10 bg-slate-950/70 backdrop-blur-md">
      <div className="pointer-events-none absolute inset-0 opacity-40 [background-size:24px_24px] [background-image:linear-gradient(to_right,rgba(34,211,238,0.08)_1px,transparent_1px),linear-gradient(to_bottom,rgba(34,211,238,0.08)_1px,transparent_1px)]" />
      <div className="relative mx-auto flex max-w-[1200px] flex-wrap items-center gap-4 px-6 py-4">
        {navItems.map((item) => {
          const isActive = pathname === item.to;
          const Icon = item.icon;
          return (
            <Link
              key={item.to}
              to={item.to}
              className={`group relative inline-flex items-center gap-2 rounded-full px-3 py-2 text-xs font-semibold uppercase tracking-[0.2em] transition-colors ${
                isActive ? "text-cyan-200" : "text-slate-400 hover:text-cyan-200"
              }`}
            >
              <Icon className="h-4 w-4 text-cyan-400" />
              <span className="relative">
                {item.label}
                {isActive ? (
                  <motion.span
                    layoutId="nav-underline"
                    className="absolute -bottom-2 left-0 h-[2px] w-full rounded-full bg-cyan-400 shadow-[0_0_12px_rgba(34,211,238,0.9)]"
                  />
                ) : null}
              </span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
