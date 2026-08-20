import React, { useState, useEffect } from 'react';
import { Clapperboard, Moon, Sun } from 'lucide-react';
import { api } from '../lib/api';
import { useTheme } from '../lib/ThemeContext';

export default function Header() {
    const [apiStatus, setApiStatus] = useState<'checking' | 'online' | 'offline'>('checking');
    const { theme, toggleTheme } = useTheme();

    useEffect(() => {
        let mounted = true;
        const checkStatus = async () => {
            const isOnline = await api.checkHealth();
            if (mounted) {
                setApiStatus(isOnline ? 'online' : 'offline');
            }
        };
        checkStatus();
        const interval = setInterval(checkStatus, 10000);
        return () => {
            mounted = false;
            clearInterval(interval);
        };
    }, []);

    return (
        <header className="absolute top-0 w-full z-50 flex items-center justify-between px-8 py-5"
            style={{
                background: theme === 'dark'
                    ? 'linear-gradient(to bottom, rgba(15,15,15,0.8), transparent)'
                    : 'linear-gradient(to bottom, rgba(250,248,245,0.9), transparent)'
            }}
        >
            <div className="flex items-center space-x-3">
                <Clapperboard className="w-8 h-8" style={{ color: 'var(--gold)' }} />
                <span className="font-condensed font-bold text-2xl tracking-widest uppercase"
                    style={{ color: 'var(--text-primary)' }}
                >
                    Agentic Cinema
                </span>
            </div>

            <div className="flex items-center space-x-6">
                <div className="flex items-center space-x-2">
                    <span className="text-sm font-sans tracking-wide" style={{ color: 'var(--text-secondary)' }}>API</span>
                    <div
                        className={`w-3 h-3 rounded-full shadow-md ${apiStatus === 'online' ? 'bg-green-500 shadow-green-500/50' :
                                apiStatus === 'checking' ? 'bg-yellow-500 animate-pulse' :
                                    'bg-red-500 shadow-red-500/50'
                            }`}
                        title={`Backend Status: ${apiStatus}`}
                    />
                </div>
                <button
                    onClick={toggleTheme}
                    className="p-2 rounded-full transition-colors"
                    style={{ color: 'var(--text-secondary)' }}
                    aria-label="Toggle Theme"
                >
                    {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
                </button>
            </div>
        </header>
    );
}
