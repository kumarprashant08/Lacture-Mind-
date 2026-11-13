// tailwind.config.js
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}"
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: "#0ff", // cyan accent
        secondary: "#a0f", // purple accent
        background: "#0a0a0a", // deep charcoal
        surface: "rgba(255,255,255,0.08)"
      },
      backdropBlur: {
        xs: "2px"
      }
    }
  },
  plugins: []
};
