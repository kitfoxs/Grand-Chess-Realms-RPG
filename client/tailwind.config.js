/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'white-kingdom': '#F5F5DC',
        'white-kingdom-gold': '#FFD700',
        'black-kingdom': '#2C2C2C',
        'black-kingdom-purple': '#9370DB',
        'neutral-gray': '#4A4A4A',
        'neutral-gray-light': '#7A7A7A',
      },
    },
  },
  plugins: [],
  darkMode: 'class',
}
