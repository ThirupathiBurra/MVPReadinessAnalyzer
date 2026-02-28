import React, { useState, useEffect } from 'react';
import IdeaForm from './components/IdeaForm';
import ReportView from './components/ReportView';
import AnalysisLoading from './components/AnalysisLoading';
import { triggerAnalysis, fetchReport, fetchMetrics } from './api';
import './App.css';

function App() {
  const [currentIdea, setCurrentIdea] = useState(null);
  const [report, setReport] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState(null);
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    fetchMetrics().then(setMetrics).catch(console.error);
  }, []);

  const handleIdeaCreated = async (idea) => {
    setCurrentIdea(idea);
    setReport(null);
    setError(null);
    setAnalyzing(true);

    try {
      if (idea.status !== 'completed') {
        await triggerAnalysis(idea.id);
      }

      let fetched = false;
      let attempts = 0;
      while (!fetched && attempts < 10) {
        await new Promise(r => setTimeout(r, 1000));
        try {
          const data = await fetchReport(idea.id);
          if (data) {
            setReport(data);
            fetched = true;
          }
        } catch (e) {
          if (e.response?.status !== 404 && e.response?.status !== 409) {
            throw new Error("Analysis failed");
          }
        }
        attempts++;
      }

    } catch (err) {
      setError(err.message || "Failed to trigger analysis.");
    } finally {
      setAnalyzing(false);
    }
  };

  const handleReset = () => {
    setCurrentIdea(null);
    setReport(null);
    setError(null);
    setAnalyzing(false);
    fetchMetrics().then(setMetrics).catch(console.error);
  }

  const loadDemo = async (ideaId) => {
    // Bypasses creation directly to trigger/fetch for pre-seeded database items
    try {
      setCurrentIdea({ id: ideaId, status: 'completed' });
      setAnalyzing(true);
      const data = await fetchReport(ideaId);
      setReport(data);
      setAnalyzing(false);
    } catch (err) {
      setError("Demo idea not found. Did you run `npm run demo` in the backend?");
      setAnalyzing(false);
    }
  }

  return (
    <div className="page-container">
      <header className="app-header">
        <div>
          <h1 style={{ marginBottom: '0.25rem' }}>MVP Readiness Analyzer</h1>
          {metrics && (
            <div className="text-secondary text-sm">
              {metrics.total_reports} Reports Generated
            </div>
          )}
        </div>

        {!currentIdea && (
          <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
            <span className="text-tertiary text-sm" style={{ fontWeight: 500 }}>Demo Scenarios:</span>
            <button onClick={() => loadDemo(1)} className="pill btn-secondary">Ideal MVP</button>
            <button onClick={() => loadDemo(2)} className="pill btn-secondary">Over-scoped Bloat</button>
          </div>
        )}
      </header>

      <main>
        {!currentIdea && (
          <IdeaForm onIdeaCreated={handleIdeaCreated} />
        )}

        {currentIdea && analyzing && !report && !error && (
          <AnalysisLoading />
        )}

        {error && (
          <div className="section">
            <div className="error-block">{error}</div>
            <button onClick={handleReset} className="btn-secondary">Start Over</button>
          </div>
        )}

        {report && (
          <>
            <ReportView report={report} />
            <div style={{ marginTop: '3rem', textAlign: 'center' }}>
              <button className="btn-secondary" onClick={handleReset}>
                Analyze Another Idea
              </button>
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
