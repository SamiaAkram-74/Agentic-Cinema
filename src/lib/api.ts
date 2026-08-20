export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export type AnalysisResult = {
    script_analysis: any;
    production_plan: any;
    schedule: any;
    readiness?: any;
};

export type AssistantResponse = { answer: string; source: string; data: Record<string, unknown> };

export const api = {
    /**
     * Check if the backend is running.
     * Hits the root endpoint `/` instead of `/health` since that's what's active in `app.py`.
     */
    async checkHealth(): Promise<boolean> {
        try {
            const response = await fetch(`${API_BASE_URL}/`);
            if (response.ok) {
                return true;
            }
            return false;
        } catch (err) {
            return false;
        }
    },

    /**
     * Upload a script PDF and ask the backend agents to analyze it.
     */
    async analyzeScript(file: File): Promise<AnalysisResult> {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            body: formData,
            mode: 'cors',
            credentials: 'omit',
        });

        if (!response.ok) {
            if (response.status === 400) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Bad Request');
            }
            throw new Error(`Analysis failed. Server responded with status ${response.status}. Ensure FastAPI is running on ${API_BASE_URL}.`);
        }

        return await response.json();
    },

    async askAssistant(question: string): Promise<AssistantResponse> {
        const response = await fetch(`${API_BASE_URL}/assistant`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question }),
        });
        const payload = await response.json();
        if (!response.ok) throw new Error(payload.detail || 'Assistant request failed.');
        return payload;
    }
};
