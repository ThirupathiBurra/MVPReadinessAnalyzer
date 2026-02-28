import React, { useState } from 'react';
import { submitIdea } from '../api';

const IdeaForm = ({ onIdeaCreated }) => {
    const [formData, setFormData] = useState({
        problem: '',
        target_user: '',
        current_solution: '',
        proposed_mvp: ''
    });

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleChange = (field, value) => {
        setFormData(prev => ({ ...prev, [field]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            const idea = await submitIdea(formData);
            onIdeaCreated(idea);
        } catch (err) {
            setError(err.response?.data?.error || err.response?.data?.errors?.[0]?.msg || "Failed to submit idea.");
        } finally {
            setLoading(false);
        }
    };

    // Check validity
    const isValid = formData.problem.length >= 10 &&
        formData.target_user.length >= 5 &&
        formData.current_solution.length >= 5 &&
        formData.proposed_mvp.length >= 10;

    return (
        <div className="section" style={{ padding: '2.5rem' }}>
            <h2>Describe your idea</h2>
            <p className="text-secondary" style={{ marginBottom: '2.5rem' }}>
                A structured, detailed idea produces a more accurate readiness evaluation.
            </p>

            {error && <div className="error-block">{error}</div>}

            <form onSubmit={handleSubmit}>

                <div className="form-group">
                    <label>1. The Problem</label>
                    <textarea
                        value={formData.problem}
                        onChange={(e) => handleChange('problem', e.target.value)}
                        placeholder="What specific problem are you trying to solve?"
                        rows={3}
                        disabled={loading}
                        required
                    />
                    <div className="input-hint">
                        <span>Needs to be a real pain point.</span>
                        {formData.problem.length > 0 && formData.problem.length < 10 && <span style={{ color: 'var(--color-warning)' }}>Too short</span>}
                    </div>
                </div>

                <div className="form-group">
                    <label>2. Target User</label>
                    <input
                        type="text"
                        value={formData.target_user}
                        onChange={(e) => handleChange('target_user', e.target.value)}
                        placeholder="Who exactly has this problem?"
                        disabled={loading}
                        required
                    />
                    <div className="input-hint">
                        <span>Be as specific as possible.</span>
                    </div>
                </div>

                <div className="form-group">
                    <label>3. Current Solution</label>
                    <input
                        type="text"
                        value={formData.current_solution}
                        onChange={(e) => handleChange('current_solution', e.target.value)}
                        placeholder="How do they solve it today? (e.g. Excel, Pen & Paper)"
                        disabled={loading}
                        required
                    />
                </div>

                <div className="form-group">
                    <label>4. Proposed MVP</label>
                    <textarea
                        value={formData.proposed_mvp}
                        onChange={(e) => handleChange('proposed_mvp', e.target.value)}
                        placeholder="What is the simplest version of your product that solves this?"
                        rows={4}
                        disabled={loading}
                        required
                    />
                    <div className="input-hint">
                        <span>Focus on the core workflow.</span>
                        {formData.proposed_mvp.length > 0 && formData.proposed_mvp.length < 10 && <span style={{ color: 'var(--color-warning)' }}>Too short</span>}
                    </div>
                </div>

                <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '3rem' }}>
                    <button type="submit" disabled={loading || !isValid}>
                        {loading ? 'Submitting...' : 'Analyze Idea'}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default IdeaForm;
