export default function Home() {
  return (
    <div className="section-stack">
      <section className="grid gap-10 lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
        <div className="section-block">
          <p className="text-meta">Recruiter view</p>
          <h1 className="hero-title text-[color:var(--color-text)]">
            AI portfolio built for fast, confident hiring decisions.
          </h1>
          <p className="hero-subtitle">
            The Portfolio Agent can surface skills, impact, and project depth in
            seconds with a recruiter-first lens.
          </p>
          <div className="flex flex-wrap gap-3">
            <button
              type="button"
              className="btn btn-primary"
              onClick={() => window.dispatchEvent(new Event("portfolio-agent:open"))}
            >
              Ask Portfolio Agent
            </button>
            <a href="/projects" className="btn btn-outline">
              View Projects
            </a>
          </div>
        </div>

        <div className="card section-block">
          <div className="text-meta">At a glance</div>
          <div className="space-y-3">
            {[
              "Production-grade systems with clear outcomes",
              "Product-first engineering and clean execution",
              "Low-friction onboarding and documentation",
            ].map((signal) => (
              <div key={signal} className="text-body text-[color:var(--color-text)]">
                {signal}
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="section-block">
        <div className="card section-block">
          <div className="text-meta">Featured project</div>
          <h2 className="text-h2 text-[color:var(--color-text)]">
            Agent-selected: Intelligent Portfolio Platform
          </h2>
          <p className="text-body text-[color:var(--color-text-muted)]">
            A unified system that connects recruiter intent with real project
            depth, combining FastAPI services with a high-signal UI layer.
          </p>
          <a href="/projects" className="btn btn-outline w-fit">
            Review project details
          </a>
        </div>
      </section>
    </div>
  );
}
