/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'tea': {
          '50': '#fdfbf7',
          '100': '#f9f2e6',
          '200': '#f2e4c9',
          '300': '#e8d0a0',
          '400': '#d9b474',
          '500': '#c9994b',
          '600': '#b57f35',
          '700': '#93632c',
          '800': '#775029',
          '900': '#624225',
          '950': '#362112',
        },
        'sunny': {
          '50': '#fffbeb',
          '100': '#fef3c7',
          '200': '#fde68a',
          '300': '#fcd34d',
          '400': '#fbbf24',
          '500': '#f59e0b',
          '600': '#d97706',
          '700': '#b45309',
          '800': '#92400e',
          '900': '#78350f',
        },
        'cream': {
          '50': '#fffef7',
          '100': '#fffbeb',
          '200': '#fef9c3',
          '300': '#fef08a',
          '400': '#fde047',
          '500': '#facc15',
        }
      },
      fontFamily: {
        'sans': ['PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'sans-serif'],
      },
      animation: {
        'float': 'float 3s ease-in-out infinite',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'bounce-slow': 'bounce 2s infinite',
        'shake': 'shake 0.5s ease-in-out',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        shake: {
          '0%, 100%': { transform: 'translateX(0)' },
          '25%': { transform: 'translateX(-5px)' },
          '75%': { transform: 'translateX(5px)' },
        }
      }
    },
  },
  plugins: [],
}