import React, { useState, useEffect } from 'react';

const steps = [
    "Structuring unstructured idea...",
    "Extracting personas and core value...",
    "Evaluating scope and market saturation...",
    "Assessing technical feasibility...",
    "Calculating final readiness score..."
];

const AnalysisLoading = () => {
    const [step, setStep] = useState(0);

    useEffect(() => {
        const timer = setInterval(() => {
            setStep((prev) => (prev < steps.length - 1 ? prev + 1 : prev));
        }, 1800);
        return () => clearInterval(timer);
    }, []);

    return (
        <div className="section" style={{ textAlign: 'center', padding: '4rem 1.5rem', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <div style={{
                width: '32px', height: '32px',
                border: '2px solid var(--border-default)',
                borderTopColor: 'var(--accent-primary)',
                borderRadius: '50%',
                animation: 'spin 1s linear infinite',
                marginBottom: '2rem'
            }}></div>

            <h3 style={{ marginBottom: '2rem' }}>Analyzing MVP Viability</h3>

            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start', gap: '0.75rem', textAlign: 'left', minWidth: '300px' }}>
                {steps.map((text, idx) => {
                    const isActive = idx === step;
                    const isPast = idx < step;

                    return (
                        <div key={idx} style={{
                            fontSize: '0.9rem',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '0.75rem',
                            color: isActive ? 'var(--text-primary)' : isPast ? 'var(--text-secondary)' : 'var(--text-tertiary)',
                            fontWeight: isActive ? 500 : 400,
                            transition: 'all 0.3s ease'
                        }}>
                            <span style={{
                                display: 'inline-block', width: '16px', textAlign: 'center',
                                color: isPast ? 'var(--color-success)' : 'inherit'
                            }}>
                                {isPast ? '✓' : isActive ? '→' : '○'}
                            </span>
                            {text}
                        </div>
                    );
                })}
            </div>
            <style>{`
                @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            `}</style>
        </div>
    );
};

export default AnalysisLoading;
