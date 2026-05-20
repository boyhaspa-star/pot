export default function HeroBackground() {
  return (
    <div className="hero-background" aria-hidden="true">
      <svg className="hero-blob" viewBox="0 0 520 620" preserveAspectRatio="none">
        <path
          d="M291 16C379 23 452 96 475 188c24 94-18 174-15 251 3 76 48 152 8 192-40 39-165 11-245-10-80-22-154-38-184-92-29-54 7-129 24-198 18-70 18-143 56-196C157 82 203 9 291 16Z"
          fill="currentColor"
        />
      </svg>
      <svg className="hero-path" viewBox="0 0 1440 280" preserveAspectRatio="none">
        <path
          d="M0 180C168 132 296 134 431 166C588 203 701 214 854 170C1039 118 1209 43 1440 71V280H0V180Z"
          fill="currentColor"
        />
      </svg>
    </div>
  );
}
