/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        severity: {
          low: "#2563eb",
          moderate: "#d97706",
          high: "#dc2626",
          contraindicated: "#7f1d1d",
        },
      },
    },
  },
  plugins: [],
};
