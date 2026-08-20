import React, { useState } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import { Upload, FileText, Calendar, Layers, Activity, AlertTriangle, Download, Printer, CheckCircle2 } from 'lucide-react';
import { api, AnalysisResult } from './lib/api';
import { useTheme } from './lib/ThemeContext';

export default function App() {
    const [file, setFile] = useState<File | null>(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<AnalysisResult | null>(null);
    const [activeTab, setActiveTab] = useState<'analysis' | 'production' | 'schedule'>('analysis');
    const [error, setError] = useState<string | null>(null);
    const [question, setQuestion] = useState('');
    const [assistantAnswer, setAssistantAnswer] = useState<string | null>(null);
    const [assistantLoading, setAssistantLoading] = useState(false);
    const { theme } = useTheme();

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!file) return;
        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const data = await api.analyzeScript(file);
            setResult(data);
            setActiveTab('analysis');
        } catch (err: any) {
            setError(err.message || 'An unexpected API error occurred.');
        } finally {
            setLoading(false);
        }
    };

    const askAssistant = async () => {
        if (!question.trim()) return;
        setAssistantLoading(true);
        try {
            const response = await api.askAssistant(question.trim());
            setAssistantAnswer(response.answer);
        } catch (err: any) {
            setAssistantAnswer(err.message || 'Assistant request failed.');
        } finally {
            setAssistantLoading(false);
        }
    };

    const downloadPlan = () => {
        if (!result) return;
        const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const anchor = document.createElement('a');
        anchor.href = url;
        anchor.download = `${result.script_analysis.title.replace(/\s+/g, '-').toLowerCase()}-production-plan.json`;
        anchor.click();
        URL.revokeObjectURL(url);
    };

    // Dynamic styles based on theme
    const isDark = theme === 'dark';
    const readiness = result?.readiness || (result ? {
        score: Math.max(0, 100 - ((result.production_plan?.required_locations || []).filter((location: any) => location.permit_required).length * 7) - ((result.production_plan?.required_locations || []).filter((location: any) => String(location.complexity).toLowerCase() === 'high').length * 5)),
        label: 'Review before lock',
        risk_flags: (result.production_plan?.required_locations || []).filter((location: any) => location.permit_required).map((location: any) => `${location.name} requires a permit`),
        agent_trace: ['PDF Reader', 'Script Analysis Agent', 'Production Planning Agent', 'Scheduling Agent'],
    } : null);

    return (
        <div className="relative min-h-screen overflow-x-hidden flex flex-col transition-colors duration-300"
            style={{ backgroundColor: 'var(--bg-primary)' }}
        >
            {/* Background Cinematic Gradient */}
            <div
                className="fixed inset-0 z-0 transition-all duration-500"
                style={{
                    backgroundImage: isDark
                        ? 'radial-gradient(ellipse at center, rgba(203, 163, 88, 0.15) 0%, rgba(15, 15, 15, 1) 70%)'
                        : 'radial-gradient(ellipse at center, rgba(184, 146, 63, 0.08) 0%, rgba(250, 248, 245, 1) 70%)'
                }}
            />
            <div
                className="fixed inset-0 z-0 pointer-events-none transition-all duration-500"
                style={{
                    backgroundImage: isDark
                        ? 'linear-gradient(to top, #0f0f0f, transparent, rgba(15,15,15,0.8))'
                        : 'linear-gradient(to top, #faf8f5, transparent, rgba(250,248,245,0.8))'
                }}
            />

            <Header />

            <main className="relative z-10 flex-grow flex flex-col items-center px-4 w-full max-w-5xl mx-auto pt-32 pb-24">

                {/* Upload Section */}
                {!result && !loading && (
                    <div className="text-center flex flex-col items-center justify-center mt-12 mb-16 max-w-3xl">
                        <h2 className="text-sm md:text-base font-sans font-semibold tracking-[0.3em] uppercase mb-4"
                            style={{ color: 'var(--gold)' }}
                        >
                            Multi-Agent Production Crew
                        </h2>
                        <h1 className="text-6xl md:text-8xl font-condensed font-bold uppercase tracking-tighter mb-8 leading-none"
                            style={{ color: 'var(--text-primary)' }}
                        >
                            Agentic Cinema
                        </h1>
                        <p className="text-lg md:text-xl font-sans mb-12 font-light leading-relaxed"
                            style={{ color: 'var(--text-secondary)' }}
                        >
                            Upload a screenplay and our agents break down the script, plan the production and lay out a day-by-day shooting schedule.
                        </p>

                        <div className="flex flex-col items-center p-8 rounded-2xl backdrop-blur shadow-2xl w-full max-w-lg transition-colors duration-300"
                            style={{
                                backgroundColor: 'var(--bg-card)',
                                border: '1px solid var(--border-color)',
                            }}
                        >
                            <label className="cursor-pointer flex flex-col items-center justify-center w-full h-40 border-2 border-dashed rounded-xl mb-6 transition-all"
                                style={{
                                    borderColor: isDark ? '#6b7280' : '#c4b99a',
                                }}
                                onMouseEnter={e => {
                                    (e.currentTarget as HTMLElement).style.borderColor = 'var(--gold)';
                                    (e.currentTarget as HTMLElement).style.backgroundColor = isDark ? 'rgba(203,163,88,0.05)' : 'rgba(184,146,63,0.05)';
                                }}
                                onMouseLeave={e => {
                                    (e.currentTarget as HTMLElement).style.borderColor = isDark ? '#6b7280' : '#c4b99a';
                                    (e.currentTarget as HTMLElement).style.backgroundColor = 'transparent';
                                }}
                            >
                                <Upload className="w-10 h-10 mb-3" style={{ color: 'var(--text-secondary)' }} />
                                <span className="font-sans" style={{ color: 'var(--text-secondary)' }}>
                                    {file ? file.name : "Select Script PDF"}
                                </span>
                                <input
                                    type="file"
                                    accept=".pdf"
                                    className="hidden"
                                    onChange={handleFileChange}
                                />
                            </label>

                            <button
                                onClick={handleUpload}
                                disabled={!file}
                                className="w-full py-4 font-condensed tracking-widest font-bold uppercase disabled:opacity-50 disabled:cursor-not-allowed transition-colors rounded-xl"
                                style={{
                                    backgroundColor: 'var(--gold)',
                                    color: isDark ? '#000' : '#fff',
                                    boxShadow: isDark ? '0 0 20px rgba(203,163,88,0.3)' : '0 4px 16px rgba(184,146,63,0.25)',
                                }}
                            >
                                Assemble Agents & Analyze
                            </button>
                            {error && <p className="text-red-500 mt-4 text-sm">{error}</p>}
                        </div>
                    </div>
                )}

                {/* Loading State */}
                {loading && (
                    <div className="flex flex-col items-center justify-center h-96 w-full text-center">
                        <Activity className="w-16 h-16 animate-bounce mb-6" style={{ color: 'var(--gold)' }} />
                        <h3 className="text-2xl font-condensed tracking-wider uppercase"
                            style={{ color: 'var(--text-primary)' }}
                        >
                            Agents are working...
                        </h3>
                        <p className="mt-2" style={{ color: 'var(--text-secondary)' }}>
                            Reading script, consulting directors, mapping out production.
                        </p>
                    </div>
                )}

                {/* Results Section */}
                {result && (
                    <div className="w-full mt-12">
                        <h2 className="text-4xl font-condensed uppercase tracking-wider mb-8 text-center"
                            style={{ color: 'var(--gold)' }}
                        >
                            Analysis Complete
                        </h2>

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8 text-left">
                            <div className="p-5 rounded-xl" style={{ backgroundColor: 'var(--bg-card)', border: '1px solid var(--border-color)' }}>
                                <p className="text-xs uppercase tracking-widest" style={{ color: 'var(--text-secondary)' }}>Production readiness</p>
                                <div className="flex items-end gap-2 mt-2"><span className="text-4xl font-bold" style={{ color: 'var(--gold)' }}>{readiness?.score ?? 'N/A'}</span><span className="mb-1" style={{ color: 'var(--text-secondary)' }}>/ 100</span></div>
                                <p className="text-sm mt-1" style={{ color: 'var(--text-secondary)' }}>{readiness?.label}</p>
                            </div>
                            <div className="p-5 rounded-xl" style={{ backgroundColor: 'var(--bg-card)', border: '1px solid var(--border-color)' }}>
                                <p className="text-xs uppercase tracking-widest" style={{ color: 'var(--text-secondary)' }}>Risk alerts</p>
                                <p className="text-4xl font-bold mt-2" style={{ color: readiness?.risk_flags?.length ? '#d97706' : '#16a34a' }}>{readiness?.risk_flags?.length ?? 0}</p>
                                <p className="text-sm mt-1" style={{ color: 'var(--text-secondary)' }}>items requiring attention</p>
                            </div>
                            <div className="p-5 rounded-xl" style={{ backgroundColor: 'var(--bg-card)', border: '1px solid var(--border-color)' }}>
                                <p className="text-xs uppercase tracking-widest" style={{ color: 'var(--text-secondary)' }}>AI crew trace</p>
                                <p className="text-4xl font-bold mt-2" style={{ color: 'var(--gold)' }}>{readiness?.agent_trace?.length ?? 0}</p>
                                <p className="text-sm mt-1" style={{ color: 'var(--text-secondary)' }}>specialized steps completed</p>
                            </div>
                        </div>

                        <div className="flex justify-end gap-3 mb-6">
                            <button onClick={downloadPlan} className="flex items-center gap-2 px-4 py-2 rounded-lg" style={{ backgroundColor: 'var(--bg-card)', color: 'var(--text-secondary)', border: '1px solid var(--border-color)' }}><Download className="w-4 h-4" /> Export plan</button>
                            <button onClick={() => window.print()} className="flex items-center gap-2 px-4 py-2 rounded-lg" style={{ backgroundColor: 'var(--bg-card)', color: 'var(--text-secondary)', border: '1px solid var(--border-color)' }}><Printer className="w-4 h-4" /> Print report</button>
                        </div>

                        {/* Tab Navigation */}
                        <div className="flex justify-center space-x-2 md:space-x-4 mb-8">
                            {[
                                { key: 'analysis' as const, icon: FileText, label: 'Analysis' },
                                { key: 'production' as const, icon: Layers, label: 'Production' },
                                { key: 'schedule' as const, icon: Calendar, label: 'Schedule' },
                            ].map(tab => (
                                <button
                                    key={tab.key}
                                    onClick={() => setActiveTab(tab.key)}
                                    className="flex items-center space-x-2 px-4 md:px-6 py-3 rounded-xl font-condensed tracking-wider uppercase transition-all"
                                    style={activeTab === tab.key ? {
                                        backgroundColor: 'var(--gold)',
                                        color: isDark ? '#000' : '#fff',
                                        boxShadow: '0 4px 16px rgba(203,163,88,0.2)',
                                    } : {
                                        backgroundColor: 'var(--bg-card)',
                                        color: 'var(--text-secondary)',
                                        border: '1px solid var(--border-color)',
                                    }}
                                >
                                    <tab.icon className="w-5 h-5" /> <span>{tab.label}</span>
                                </button>
                            ))}
                        </div>

                        {/* Content Panel */}
                        <div className="p-6 md:p-10 rounded-2xl shadow-2xl min-h-[500px] transition-colors duration-300"
                            style={{
                                backgroundColor: isDark ? 'rgba(15,15,15,0.6)' : 'rgba(255,255,255,0.8)',
                                border: '1px solid var(--border-color)',
                                backdropFilter: 'blur(16px)',
                            }}
                        >
                            <div className="mb-10 p-6 rounded-xl text-left" style={{ backgroundColor: 'var(--bg-card)', border: '1px solid var(--border-color)' }}>
                                <h3 className="font-condensed tracking-wider uppercase mb-3" style={{ color: 'var(--gold)' }}>Production Assistant</h3>
                                <div className="flex flex-col md:flex-row gap-3">
                                    <input value={question} onChange={e => setQuestion(e.target.value)} onKeyDown={e => e.key === 'Enter' && askAssistant()} placeholder="Ask about permits, lighting, or a location" className="flex-1 px-4 py-3 rounded-lg outline-none" style={{ backgroundColor: 'var(--bg-secondary)', color: 'var(--text-primary)', border: '1px solid var(--border-color)' }} />
                                    <button onClick={askAssistant} disabled={assistantLoading || !question.trim()} className="px-5 py-3 rounded-lg font-condensed uppercase tracking-wider disabled:opacity-50" style={{ backgroundColor: 'var(--gold)', color: isDark ? '#000' : '#fff' }}>{assistantLoading ? 'Checking...' : 'Ask Agent'}</button>
                                </div>
                                {assistantAnswer && <p className="mt-4 leading-relaxed" style={{ color: 'var(--text-secondary)' }}>{assistantAnswer}</p>}
                            </div>

                            {activeTab === 'production' && readiness && (
                                <div className="mb-8 grid grid-cols-1 md:grid-cols-2 gap-6 text-left">
                                    <div className="p-6 rounded-xl" style={{ backgroundColor: 'var(--bg-card)', border: '1px solid var(--border-color)' }}>
                                        <h3 className="font-condensed tracking-wider uppercase mb-4 flex items-center gap-2" style={{ color: '#d97706' }}><AlertTriangle className="w-5 h-5" /> Risk register</h3>
                                        {(readiness.risk_flags || []).map((risk: string, index: number) => <p key={index} className="flex gap-2 mb-3" style={{ color: 'var(--text-secondary)' }}><AlertTriangle className="w-4 h-4 shrink-0" style={{ color: '#d97706' }} /> {risk}</p>)}
                                    </div>
                                    <div className="p-6 rounded-xl" style={{ backgroundColor: 'var(--bg-card)', border: '1px solid var(--border-color)' }}>
                                        <h3 className="font-condensed tracking-wider uppercase mb-4 flex items-center gap-2" style={{ color: 'var(--gold)' }}><CheckCircle2 className="w-5 h-5" /> Next actions</h3>
                                        {(readiness.next_actions || []).map((action: string, index: number) => <p key={index} className="flex gap-2 mb-3" style={{ color: 'var(--text-secondary)' }}><CheckCircle2 className="w-4 h-4 shrink-0" style={{ color: 'var(--gold)' }} /> {action}</p>)}
                                    </div>
                                </div>
                            )}
                            {/* === ANALYSIS TAB === */}
                            {activeTab === 'analysis' && result.script_analysis && (
                                <div className="space-y-8 text-left">
                                    <div style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '1.5rem' }}>
                                        <h3 className="text-sm font-condensed tracking-[0.3em] uppercase mb-2" style={{ color: 'var(--gold)' }}>
                                            Screenplay Title
                                        </h3>
                                        <h2 className="text-4xl font-bold" style={{ color: 'var(--text-primary)' }}>
                                            {result.script_analysis.title || 'Untitled Project'}
                                        </h2>
                                    </div>
                                    <div className="p-6 rounded-xl" style={{ backgroundColor: 'var(--bg-card)', border: '1px solid var(--border-color)' }}>
                                        <h3 className="font-condensed tracking-wider uppercase mb-3 flex items-center gap-2" style={{ color: 'var(--gold)' }}>
                                            <FileText className="w-5 h-5" /> Logline / Summary
                                        </h3>
                                        <p className="leading-relaxed text-lg" style={{ color: 'var(--text-secondary)' }}>
                                            {result.script_analysis.summary}
                                        </p>
                                    </div>
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                        <div className="p-6 rounded-xl" style={{ backgroundColor: 'var(--bg-card)', border: '1px solid var(--border-color)' }}>
                                            <h3 className="font-condensed tracking-wider uppercase mb-4 flex items-center gap-2" style={{ color: 'var(--gold)' }}>
                                                <Layers className="w-5 h-5" /> Cast & Characters
                                            </h3>
                                            <ul className="space-y-2">
                                                {(result.script_analysis.characters || []).map((char: string, i: number) => (
                                                    <li key={i} className="px-4 py-2 rounded-lg flex items-center gap-3"
                                                        style={{ backgroundColor: 'var(--bg-secondary)', color: 'var(--text-secondary)', border: '1px solid var(--border-color)' }}
                                                    >
                                                        <div className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: 'var(--gold)' }} /> {char}
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                        <div className="p-6 rounded-xl" style={{ backgroundColor: 'var(--bg-card)', border: '1px solid var(--border-color)' }}>
                                            <h3 className="font-condensed tracking-wider uppercase mb-4 flex items-center gap-2" style={{ color: 'var(--gold)' }}>
                                                <Layers className="w-5 h-5" /> Primary Locations
                                            </h3>
                                            <ul className="space-y-2">
                                                {(result.script_analysis.locations || []).map((loc: string, i: number) => (
                                                    <li key={i} className="px-4 py-2 rounded-lg flex items-center gap-3"
                                                        style={{ backgroundColor: 'var(--bg-secondary)', color: 'var(--text-secondary)', border: '1px solid var(--border-color)' }}
                                                    >
                                                        <div className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: 'var(--gold)' }} /> {loc}
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* === PRODUCTION TAB === */}
                            {activeTab === 'production' && result.production_plan && (
                                <div className="space-y-6 text-left">
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                                        <div className="p-8 rounded-2xl flex flex-col items-center justify-center text-center"
                                            style={{
                                                backgroundColor: 'var(--bg-card)',
                                                border: '1px solid var(--gold)',
                                                boxShadow: isDark ? '0 0 30px rgba(203,163,88,0.1)' : '0 4px 20px rgba(184,146,63,0.1)',
                                            }}
                                        >
                                            <Calendar className="w-10 h-10 mb-4" style={{ color: 'var(--gold)' }} />
                                            <h3 className="text-sm font-condensed tracking-widest uppercase mb-2" style={{ color: 'var(--text-secondary)' }}>
                                                Estimated Setup
                                            </h3>
                                            <p className="text-5xl font-bold" style={{ color: 'var(--text-primary)' }}>
                                                {result.production_plan.estimated_shooting_days || 'N/A'}
                                            </p>
                                            <p className="mt-2 font-condensed uppercase tracking-wider" style={{ color: 'var(--gold)' }}>Days</p>
                                        </div>
                                        <div className="p-8 rounded-2xl flex flex-col items-center justify-center text-center"
                                            style={{ backgroundColor: 'var(--bg-card)', border: '1px solid var(--border-color)' }}
                                        >
                                            <Activity className="w-10 h-10 mb-4" style={{ color: 'var(--gold)' }} />
                                            <h3 className="text-sm font-condensed tracking-widest uppercase mb-2" style={{ color: 'var(--text-secondary)' }}>
                                                Shooting Complexity
                                            </h3>
                                            <p className="text-xl font-bold capitalize" style={{ color: 'var(--text-primary)' }}>
                                                {result.production_plan.shooting_complexity || 'Standard'}
                                            </p>
                                        </div>
                                    </div>
                                    <div className="p-6 rounded-xl" style={{ backgroundColor: 'var(--bg-card)', border: '1px solid var(--border-color)' }}>
                                        <h3 className="font-condensed tracking-wider uppercase mb-3 flex items-center gap-2" style={{ color: 'var(--gold)' }}>
                                            <Layers className="w-5 h-5" /> Required Locations / Gear
                                        </h3>
                                        <p className="leading-relaxed whitespace-pre-line" style={{ color: 'var(--text-secondary)' }}>
                                            {typeof result.production_plan.required_locations === 'string'
                                                ? result.production_plan.required_locations
                                                : JSON.stringify(result.production_plan.required_locations, null, 2)}
                                        </p>
                                    </div>
                                    <div className="p-6 rounded-xl" style={{ backgroundColor: 'var(--bg-card)', border: '1px solid var(--border-color)' }}>
                                        <h3 className="font-condensed tracking-wider uppercase mb-3 flex items-center gap-2" style={{ color: 'var(--gold)' }}>
                                            <FileText className="w-5 h-5" /> Production Notes
                                        </h3>
                                        <p className="leading-relaxed whitespace-pre-line" style={{ color: 'var(--text-secondary)' }}>
                                            {result.production_plan.production_notes}
                                        </p>
                                    </div>
                                </div>
                            )}

                            {/* === SCHEDULE TAB === */}
                            {activeTab === 'schedule' && result.schedule && (
                                <div className="space-y-8 text-left">
                                    <div className="flex items-center justify-between pb-6" style={{ borderBottom: '1px solid var(--border-color)' }}>
                                        <h2 className="text-3xl font-condensed tracking-wider uppercase" style={{ color: 'var(--text-primary)' }}>
                                            Shooting Schedule
                                        </h2>
                                        <div className="px-4 py-2 rounded-lg" style={{ backgroundColor: isDark ? 'rgba(203,163,88,0.1)' : 'rgba(184,146,63,0.1)', border: '1px solid var(--gold)' }}>
                                            <span className="font-bold" style={{ color: 'var(--gold)' }}>{result.schedule.total_shooting_days}</span>
                                            <span style={{ color: 'var(--text-secondary)' }}> Total Days</span>
                                        </div>
                                    </div>

                                    <div className="space-y-6">
                                        {(result.schedule.schedule || []).map((dayData: any, idx: number) => (
                                            <div key={idx} className="rounded-xl overflow-hidden"
                                                style={{ backgroundColor: 'var(--bg-card)', border: '1px solid var(--border-color)' }}
                                            >
                                                <div className="px-6 py-4 flex items-center justify-between"
                                                    style={{
                                                        backgroundColor: isDark ? 'rgba(0,0,0,0.4)' : 'var(--bg-secondary)',
                                                        borderBottom: '1px solid var(--border-color)',
                                                    }}
                                                >
                                                    <div className="flex items-center gap-4">
                                                        <div className="font-bold font-condensed w-10 h-10 rounded-full flex items-center justify-center text-xl"
                                                            style={{ backgroundColor: 'var(--gold)', color: isDark ? '#000' : '#fff' }}
                                                        >
                                                            {dayData.day}
                                                        </div>
                                                        <h3 className="text-xl font-bold flex items-center gap-2" style={{ color: 'var(--text-primary)' }}>
                                                            <Layers className="w-5 h-5" style={{ color: 'var(--text-secondary)' }} /> {dayData.location}
                                                        </h3>
                                                    </div>
                                                </div>
                                                <div className="p-6">
                                                    <div className="mb-6">
                                                        <h4 className="text-sm font-condensed tracking-widest uppercase mb-3" style={{ color: 'var(--gold)' }}>
                                                            Scheduled Scenes
                                                        </h4>
                                                        <div className="flex flex-wrap gap-2">
                                                            {(dayData.scenes || []).map((scene: string, sIdx: number) => (
                                                                <span key={sIdx} className="px-3 py-1.5 rounded text-sm flex items-center gap-2"
                                                                    style={{
                                                                        backgroundColor: 'var(--bg-secondary)',
                                                                        color: 'var(--text-secondary)',
                                                                        border: '1px solid var(--border-color)',
                                                                    }}
                                                                >
                                                                    <FileText className="w-4 h-4" style={{ color: 'var(--text-secondary)' }} /> {scene}
                                                                </span>
                                                            ))}
                                                        </div>
                                                    </div>
                                                    {dayData.notes && (
                                                        <div className="p-4 rounded-lg" style={{ backgroundColor: isDark ? 'rgba(0,0,0,0.2)' : 'var(--bg-secondary)', borderLeft: '4px solid var(--gold)' }}>
                                                            <p className="text-sm italic" style={{ color: 'var(--text-secondary)' }}>{dayData.notes}</p>
                                                        </div>
                                                    )}
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}

                        </div>

                        <div className="flex justify-center mt-12">
                            <button
                                onClick={() => { setResult(null); setFile(null); }}
                                className="underline underline-offset-4 transition-colors"
                                style={{ color: 'var(--text-secondary)' }}
                            >
                                Upload another script
                            </button>
                        </div>
                    </div>
                )}

            </main>
            <Footer />
        </div>
    );
}
