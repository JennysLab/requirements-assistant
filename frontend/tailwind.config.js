/**
 * /**
 * Tailwind-Konfiguration: das "Farb- und Stil-Skript" des Prototyps.
 *
 * Tailwind ist ein CSS-Werkzeug. Statt Stile in eigenen Dateien zu schreiben,
 * werden im Code kurze Klassennamen verwendet (z. B. "bg-accent text-white").
 * Diese Datei legt fest, welche eigenen Namen es gibt. So steckt das gesamte
 * Aussehen an einer Stelle (Design Tokens): Aendert man hier eine Farbe,
 * passt sich die ganze Oberflaeche an.
 *
 * Die Statusfarben machen den Human-in-the-Loop-Ablauf sichtbar:
 * Entwurf (orange) -> Bestaetigt (gruen) oder Verworfen (rot).
 */
export default {
  // Dateien, in denen Tailwind nach verwendeten Klassen sucht.
  // Nur diese Stile landen in der fertigen Seite (haelt sie klein).
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    // "extend" ergaenzt den Standard-Farbkasten, statt ihn zu ersetzen.
    extend: {
      colors: {
        // Grundfarben der Oberflaeche
        paper: "#FAFAF9",        // Seitenhintergrund
        surface: "#FFFFFF",      // Karten und Eingabefelder
        sidebar: "#16213E",      // Seitenmenue (dunkelblau)
        sidebarmuted: "#8D97B5", // gedaempfter Text im Menue
        ink: "#1B1F27",          // normaler Text
        muted: "#6B7280",        // Nebentexte und Hinweise
        border: "#E4E7EC",       // Rahmenlinien
        // Hauptfarbe fuer Buttons und Hervorhebungen
        // (normal / beim Darueberfahren / heller Hintergrund)
        accent: { DEFAULT: "#3A5BA0", hover: "#2D4A85", soft: "#EAF0FB" },
        // Statusfarben (Human-in-the-Loop); "soft" = heller Hintergrund
        status: {
          draft: "#8B8F98",        // grau: derzeit nicht verwendet
          review: "#C98A2E",       // orange: Entwurf, wartet auf Pruefung
          reviewsoft: "#FBF1E1",
          accepted: "#2F8F5B",     // gruen: vom Menschen bestaetigt
          acceptedsoft: "#E8F5EE",
          rework: "#C1503D",       // rot: verworfen
          reworksoft: "#FBEAE7",
        },
      },
      // Schriften mit Ersatzplan, falls eine Schrift auf dem Geraet fehlt
      fontFamily: {
        sans: ["\"IBM Plex Sans\"", "system-ui", "sans-serif"], // Fliesstext
        mono: ["\"IBM Plex Mono\"", "ui-monospace", "monospace"], // IDs, Code
      },
      // Rundung der Ecken: sm = leicht, md = deutlicher
      borderRadius: { sm: "4px", md: "8px" },
    },
  },
  plugins: [], // keine Zusatzpakete
};
