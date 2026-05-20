import HeroBackground from "./HeroBackground.jsx";
import HeroNav from "./HeroNav.jsx";
import HeroScene from "./HeroScene.jsx";

export default function Hero() {
  return (
    <main className="hero-shell">
      <HeroBackground />
      <HeroNav />
      <aside className="hero-side-note" aria-hidden="true">
        Soft strategy, art direction, and visual systems
      </aside>
      <section className="hero-grid" aria-label="Brand design hero">
        <div className="hero-copy">
          <p className="hero-kicker">Brand and web design studio</p>
          <h1>I design brands with soul.</h1>
          <p className="hero-body">
            Thoughtful identities and digital experiences shaped with warmth,
            restraint, and a quiet sense of place.
          </p>
          <a className="hero-cta" href="#selected-work" aria-label="View selected work">
            View Selected Work <span aria-hidden="true">→</span>
          </a>
        </div>
        <div className="hero-visual" aria-label="Ceramic vase and clay base">
          <HeroScene />
        </div>
      </section>
    </main>
  );
}
