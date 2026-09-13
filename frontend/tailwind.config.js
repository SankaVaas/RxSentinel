/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#14213D",
        paper: "#F6F7F5",
        slate: {
          DEFAULT: "#5B6472",
          light: "#8B93A0",
        },
        line: "#DDE1E6",
        teal: {
          DEFAULT: "#0B6E6E",
          dark: "#08514F",
          light: "#E3F1F0",
        },
        severity: {
          low: { fg: "#1E4E8C", bg: "#E9F0FA", border: "#B9D0EE" },
          moderate: { fg: "#8A5A0A", bg: "#FBF1DF", border: "#EBCE95" },
          high: { fg: "#B3261E", bg: "#FBEAE9", border: "#EFB6B1" },
          contraindicated: { fg: "#FFFFFF", bg: "#6E1423", border: "#6E1423" },
        },
      },
      fontFamily: {
        sans: ["IBM Plex Sans", "system-ui", "sans-serif"],
        mono: ["IBM Plex Mono", "ui-monospace", "monospace"],
      },
      boxShadow: {
        panel: "0 1px 2px rgba(20, 33, 61, 0.06)",
      },
    },
  },
  plugins: [],
};
