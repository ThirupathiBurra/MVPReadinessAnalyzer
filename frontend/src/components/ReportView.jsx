import React from 'react';

const ReportView = ({ report }) => {
    if (!report) return null;

    const { scores, structured_data } = report;

    // Determine color scale for the hero score
    const scoreColor = scores.overall_readiness > 70 ? 'var(--color-success)' : scores.overall_readiness > 40 ? 'var(--color-warning)' : 'var(--color-danger)';

    return (
        <div className="report-container">
            {/* Executive Hero */}
            <div className="section" style={{ border: 'none', paddingBottom: '0' }}>
                <div style={{ display: 'flex', gap: '3rem', alignItems: 'center' }}>

                    {/* Giant Numerical Score */}
                    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
                        <h4 style={{ color: 'var(--text-tertiary)' }}>Overall Score</h4>
                        <div className="score-glow" style={{
                            fontSize: '5rem',
                            fontWeight: 700,
                            lineHeight: 1,
                            letterSpacing: '-0.05em',
                            color: scoreColor
                        }}>
                            {scores.overall_readiness}
                        </div>
                    </div>

                    {/* Verdict & Actions */}
                    <div style={{ flex: 1, paddingLeft: '2rem', borderLeft: '1px solid var(--border-default)' }}>
                        <h3 style={{ fontSize: '1.1rem', marginBottom: '0.75rem', color: 'var(--text-primary)' }}>
                            {structured_data.why_this_score}
                        </h3>
                        <div>
                            <h4 style={{ marginBottom: '0.25rem' }}>Primary Recommendation</h4>
                            <p style={{ margin: 0, fontWeight: 500, color: 'var(--text-primary)' }}>
                                {structured_data.next_actions}
                            </p>
                        </div>
                    </div>

                </div>
            </div>

            <hr />

            {/* Category Breakdown (Grid) */}
            <div className="section">
                <h2 style={{ marginBottom: '1.5rem' }}>Category Breakdown</h2>
                <div className="grid-2">
                    <div className="insight-block">
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <h4>Problem Understanding</h4>
                            <span style={{ fontWeight: 600 }}>{scores.problem_understanding}</span>
                        </div>
                        <p>{structured_data.problem_clarity}</p>
                    </div>

                    <div className="insight-block">
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <h4>Market Viability</h4>
                            <span style={{ fontWeight: 600 }}>{scores.market_viability}</span>
                        </div>
                        <p>{structured_data.market_risks}</p>
                    </div>

                    <div className="insight-block">
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <h4>Tech Feasibility</h4>
                            <span style={{ fontWeight: 600 }}>{scores.technical_feasibility}</span>
                        </div>
                        <p>{structured_data.technical_unknowns}</p>
                    </div>

                    <div className="insight-block">
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <h4>Scope Realism</h4>
                            <span style={{ fontWeight: 600 }}>{scores.scope_realism}</span>
                        </div>
                        <p>{structured_data.feature_scope_classification}</p>
                    </div>
                </div>
            </div>

            <hr />

            {/* Rule Trace (List) */}
            <div className="section" style={{ border: 'none' }}>
                <h2>Evaluation Trace</h2>
                <p>Determinants applied by the scoring engine to calculate the final output.</p>

                <div style={{ display: 'flex', flexDirection: 'column', marginTop: '1.5rem' }}>
                    {scores.triggered_rules && scores.triggered_rules.map((rule, idx) => {
                        const isPositive = rule.delta > 0;
                        const isNegative = rule.delta < 0;
                        const sign = isPositive ? '+' : '';
                        const color = isPositive ? 'var(--color-success)' : isNegative ? 'var(--color-danger)' : 'var(--text-primary)';

                        return (
                            <div key={idx} style={{
                                display: 'flex',
                                justifyContent: 'space-between',
                                alignItems: 'center',
                                padding: '1rem 0',
                                borderBottom: idx !== scores.triggered_rules.length - 1 ? '1px solid var(--border-subtle)' : 'none'
                            }}>
                                <div style={{ paddingRight: '1rem' }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.25rem' }}>
                                        <span style={{ fontWeight: 500, fontSize: '0.95rem', color: 'var(--text-primary)' }}>{rule.rule_name}</span>
                                        <span className="pill" style={{ fontSize: '0.65rem' }}>{rule.category.replace('_', ' ')}</span>
                                    </div>
                                    {rule.reason && <div className="text-secondary text-sm">{rule.reason}</div>}
                                </div>
                                <div style={{
                                    fontWeight: 600,
                                    fontSize: '1rem',
                                    color: color,
                                    whiteSpace: 'nowrap'
                                }}>
                                    {sign}{rule.delta}
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>

        </div>
    );
};

export default ReportView;
