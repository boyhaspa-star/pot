const links = ["Work", "About", "Journal", "Contact"];

export default function HeroNav() {
  return (
    <nav className="hero-nav" aria-label="Primary navigation">
      <a className="hero-logo" href="/" aria-label="Auren home">
        Auren
      </a>
      <div className="hero-links">
        {links.map((link) => (
          <a href={`#${link.toLowerCase()}`} key={link}>
            {link}
          </a>
        ))}
      </div>
      <button className="hero-menu" type="button" aria-label="Open menu">
        <span />
        <span />
      </button>
    </nav>
  );
}
