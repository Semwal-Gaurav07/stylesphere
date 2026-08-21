/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './store/templates/**/*.html',
    './accounts/templates/**/*.html',
    './payment/templates/**/*.html',
    './static/js/**/*.js',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        brand: {
          dark: '#0D0D12',
          surface: '#16161F',
          border: 'rgba(255, 255, 255, 0.08)',
          indigo: '#6366F1',
        }
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('daisyui'),
  ],
  daisyui: {
    themes: ["dark", "light"],
    defaultTheme: "dark",
  },
}