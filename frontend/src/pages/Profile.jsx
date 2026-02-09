import About from "./About";
import Skills from "./Skills";
import Experience from "./Experience";
import Education from "./Education";
import Certificates from "./Certificates";
import Contact from "./Contact";

export default function Profile() {
  return (
    <div className="section-stack">
      <section className="section-block">
        <About />
      </section>
      <section className="section-block">
        <Skills />
      </section>
      <section className="section-block">
        <Experience />
      </section>
      <section className="section-block">
        <Education />
      </section>
      <section className="section-block">
        <Certificates />
      </section>
    </div>
  );
}
