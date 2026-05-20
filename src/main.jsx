import React from "react";
import { createRoot } from "react-dom/client";
import Hero from "./components/Hero.jsx";
import "./styles.css";

createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <Hero />
  </React.StrictMode>,
);
