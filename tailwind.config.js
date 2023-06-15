/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        'brandgreen': {
          DEFAULT: '#28705a',
          100: '#caece2',
          200: '#95d9c5',
          300: '#61c6a7',
          400: '#3ba584',
          500: '#28705a',
          600: '#205a48',
          700: '#184336',
          800: '#102d24',
          900: '#081612',
        },
      },
    },
    fontFamily: {
      sans: ['Graphik', 'ui-sans-serif', 'system-ui'],
      serif: ['ui-serif', 'Georgia'],
      mono: ['ui-monospace', 'SFMono-Regular']
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}