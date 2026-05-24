import aboutBowl from "../assets/about-bowl.png";
import aboutVase from "../assets/about-vase.png";
import ctaVase from "../assets/cta-vase.png";
import featureWork from "../assets/feature-work.png";
import heroReference from "../assets/hero-reference.png";
import workAurora from "../assets/work-card-aurora.png";
import workHaevn from "../assets/work-card-haevn.png";
import workNorda from "../assets/work-card-norda.png";
import HeroNav from "./HeroNav.jsx";

const workCards = [
  { number: "01", title: "Aurora Studio", type: "Brand Identity", image: workAurora },
  { number: "02", title: "Norda", type: "Web Design", image: workNorda },
  { number: "03", title: "Haevn", type: "Packaging", image: workHaevn },
];

const capabilities = [
  "Brand Identity",
  "Web Design",
  "Art Direction",
  "UI/UX Design",
  "Creative Development",
];

function SitePath() {
  return (
    <svg className="site-path" viewBox="0 0 864 1821" preserveAspectRatio="none" aria-hidden="true">
      <path
        d="M0 512C82 488 164 507 184 453C210 383 382 468 520 436C664 402 728 398 864 412V574C742 554 603 536 442 548C330 556 238 579 257 657C275 731 230 802 204 873C179 942 197 1013 285 1042C445 1096 673 1061 864 1122V1212C635 1182 441 1200 220 1219C118 1228 23 1183 20 1089C17 980 76 913 48 828C22 750 -8 723 0 642Z"
        fill="currentColor"
      />
      <path
        d="M0 1429C82 1461 104 1518 128 1580C151 1639 190 1665 257 1687C387 1730 547 1692 681 1694C760 1696 825 1728 864 1771V1821H0Z"
        fill="currentColor"
      />
      <path
        d="M0 1188C100 1228 109 1314 93 1392C80 1458 27 1510 0 1570Z"
        fill="currentColor"
      />
    </svg>
  );
}

export default function Hero() {
  return (
    <main className="hero-shell">
      <SitePath />
      <HeroNav />
      <aside className="hero-side-note" aria-hidden="true">
        Design and meaningful connections
      </aside>

      <section className="hero-grid" aria-label="Brand design hero">
        <div className="hero-copy">
          <h1>I design brands with soul.</h1>
          <p className="hero-body">
            Brand & Web Designer crafting thoughtful identities and digital experiences.
          </p>
          <a className="hero-cta" href="#selected-work" aria-label="View selected work">
            View Selected Work <span aria-hidden="true">→</span>
          </a>
        </div>
        <div className="hero-visual" aria-label="Ceramic vase and clay base">
          <img className="hero-reference-image" src={heroReference} alt="" />
        </div>
      </section>

      <section className="featured-work" id="selected-work" aria-label="Selected project">
        <div className="featured-count">
          <span>Selected Work</span>
          <strong>01</strong>
          <em>/ 04</em>
        </div>
        <div className="featured-copy">
          <h2>Aurora Studio</h2>
          <p>Brand identity for a calm lifestyle brand.</p>
          <ul>
            <li>Brand Strategy</li>
            <li>Visual Identity</li>
            <li>Packaging</li>
            <li>Website</li>
          </ul>
          <a className="text-link" href="#case-study">
            View Case Study <span aria-hidden="true">→</span>
          </a>
        </div>
        <img className="featured-image" src={featureWork} alt="" />
      </section>

      <section className="work-gallery" id="work" aria-label="Selected work gallery">
        <div className="section-head">
          <h2>Selected Work</h2>
          <a href="#work">See All Work <span aria-hidden="true">→</span></a>
        </div>
        <div className="work-cards">
          {workCards.map((card) => (
            <article className="work-card" key={card.title}>
              <img src={card.image} alt="" />
              <span className="work-number">{card.number}</span>
              <div className="work-card-copy">
                <h3>{card.title}</h3>
                <p>{card.type}</p>
              </div>
              <span className="work-arrow" aria-hidden="true">→</span>
            </article>
          ))}
        </div>
      </section>

      <section className="about-section" id="about" aria-label="About and capabilities">
        <div className="about-copy">
          <h2>Designing quiet systems with emotional clarity.</h2>
          <p>
            I work with founders and creative teams to shape brands, websites, and digital
            experiences that feel intentional.
          </p>
          <span className="signature">Auren</span>
        </div>
        <div className="about-object">
          <img src={aboutVase} alt="" />
        </div>
        <div className="stats">
          <div><strong>08</strong><span>Years Experience</span></div>
          <div><strong>42</strong><span>Selected Projects</span></div>
          <div><strong>16</strong><span>Brand Systems</span></div>
        </div>
        <div className="capabilities">
          <h2>Capabilities</h2>
          <ol>
            {capabilities.map((item, index) => (
              <li key={item}>
                <span>{String(index + 1).padStart(2, "0")}</span>
                {item}
              </li>
            ))}
          </ol>
        </div>
        <img className="about-bowl" src={aboutBowl} alt="" />
      </section>

      <section className="cta-section" id="contact" aria-label="Project inquiry">
        <p className="footer-note" aria-hidden="true">Let us create something meaningful</p>
        <div className="cta-copy">
          <h2>Have a project with soul?</h2>
          <p>Let's build something quiet, beautiful, and useful.</p>
          <a className="cta-button" href="mailto:hello@auren.studio">
            Start a Project <span aria-hidden="true">→</span>
          </a>
        </div>
        <img src={ctaVase} alt="" />
      </section>
    </main>
  );
}
