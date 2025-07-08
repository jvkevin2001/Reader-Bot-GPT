/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}", // Le dice a Tailwind que busque clases en todos los archivos de React
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
