import React from 'react';

export default function Footer() {
    return (
        <footer className="relative z-50 py-6 px-8 flex justify-between items-center text-sm"
            style={{
                color: 'var(--text-secondary)',
                borderTop: '1px solid var(--border-color)',
                backgroundColor: 'var(--overlay)',
                backdropFilter: 'blur(12px)',
            }}
        >
            <p>&copy; {new Date().getFullYear()} Agentic Cinema. All rights reserved.</p>
            <div className="flex space-x-6">
                <a href="#" className="hover:opacity-80 transition" style={{ color: 'var(--gold)' }}>Terms</a>
                <a href="#" className="hover:opacity-80 transition" style={{ color: 'var(--gold)' }}>Privacy</a>
                <a href="#" className="hover:opacity-80 transition" style={{ color: 'var(--gold)' }}>Credits</a>
            </div>
        </footer>
    );
}
