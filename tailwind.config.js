/** @type {import('tailwindcss').Config} */
export default {
    darkMode: 'class',
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                agentic: {
                    dark: '#0f0f0f',
                    gold: '#cba358',
                    light: '#f5f5f5'
                }
            },
            fontFamily: {
                condensed: ['"Oswald"', 'sans-serif'],
                sans: ['"Inter"', 'sans-serif'],
            },
        },
    },
    plugins: [
        require('@tailwindcss/typography'),
    ],
}
