// tailwind.config.ts
import type { Config } from 'tailwindcss';

const config: Config = {
  darkMode: 'class',
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
    '*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      borderColor: {
        DEFAULT: 'hsl(var(--border))', // Use --border variable as the default
      },
      colors: {
        border: 'hsl(var(--border))',
        // Other color configurations
      },
    },
  },
  plugins: [],
};

export default config;
