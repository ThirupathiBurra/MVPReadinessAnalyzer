import pytest
from services.scoring import score_idea

def test_scoring_invariant_bounds():
    # An entirely blank or neutral idea should not crash and should respect bounds
    data = {
        "personas": "",
        "problem_clarity": "",
        "core_value_proposition": "",
        "feature_scope_classification": "",
        "technical_unknowns": "",
        "market_risks": "",
        "missing_components": ""
    }
    scores, why, actions, triggered = score_idea(data)
    
    # Invariants are 0-100
    for k, v in scores.items():
        if isinstance(v, (int, float)):
            assert 0 <= v <= 100

def test_ideal_mvp_scenario():
    data = {
        "personas": "Freelance web designers who struggle with billing.",
        "problem_clarity": "Highly specific, clear and well-defined.",
        "core_value_proposition": "Automated clear client invoicing.",
        "feature_scope_classification": "Minimal and tight MVP.",
        "technical_unknowns": "Straightforward integration with Stripe.",
        "market_risks": "Low risk, manageable niche.",
        "missing_components": "None."
    }
    
    scores, why, actions, triggered = score_idea(data)
    rules_fired = [r['rule_name'] for r in triggered]
    
    assert scores["overall_readiness"] > 75
    assert "Clear Target User" in rules_fired
    assert "Manageable Market Risk" in rules_fired
    assert "Tight Scope" in rules_fired
    assert "High Technical Feasibility" in rules_fired

def test_overscoped_scenario():
    data = {
        "personas": "Everyone.",
        "problem_clarity": "Vague problem.",
        "core_value_proposition": "An app that does everything.",
        "feature_scope_classification": "Over-scoped bloat with too many features.",
        "technical_unknowns": "Complex legacy AI integrations unknown.",
        "market_risks": "High, crowded market competition.",
        "missing_components": "Everything."
    }
    
    scores, why, actions, triggered = score_idea(data)
    rules_fired = [r['rule_name'] for r in triggered]
    
    assert scores["overall_readiness"] < 50
    assert "Scope Bloat" in rules_fired
    assert "Vague Target User" in rules_fired
    assert "Market Weakness" in rules_fired
    assert "Low Technical Feasibility" in rules_fired
    
    # Assert blocker directly reduces score
    assert scores["scope_realism"] < 50

def test_vague_user_scenario():
    data = {
        "personas": "Broad, everyone in the world.",
        "problem_clarity": "Unclear and vague.",
        "core_value_proposition": "Networking.",
        "feature_scope_classification": "Standard.",
        "technical_unknowns": "None.",
        "market_risks": "None.",
        "missing_components": "None."
    }
    
    scores, why, actions, triggered = score_idea(data)
    rules_fired = [r['rule_name'] for r in triggered]
    
    assert "Vague Target User" in rules_fired
    assert scores["problem_understanding"] < 50 # Base is 50, -20 = 30

def test_multi_feature_bloat_scenario():
    data = {
        "personas": "Small businesses.",
        "problem_clarity": "Clear.",
        "core_value_proposition": "An all-in-one suite bridging hr and accounting.",
        "feature_scope_classification": "A massive platform with multiple workflows including chat, billing, and tasks.",
        "technical_unknowns": "Standard.",
        "market_risks": "Low.",
        "missing_components": "None."
    }
    scores, why, actions, triggered = score_idea(data)
    rules_fired = [r['rule_name'] for r in triggered]
    
    assert "Multi-Workflow Bloat" in rules_fired
    assert scores["scope_realism"] <= 50 # -40 penalty on base 50
    assert scores["overall_readiness"] <= 50 # Should trigger balancing cap

def test_weak_market_cap_scenario():
    data = {
        "personas": "To-do list users.",
        "problem_clarity": "Highly specific.",
        "core_value_proposition": "Another simple to-do list.",
        "feature_scope_classification": "A single-purpose minimal MVP.",
        "technical_unknowns": "Simple crud tool.",
        "market_risks": "Highly saturated market with no differentiation and low urgency.",
        "missing_components": "None."
    }
    scores, why, actions, triggered = score_idea(data)
    rules_fired = [r['rule_name'] for r in triggered]
    
    assert "Market Weakness" in rules_fired
    assert "High Technical Feasibility" in rules_fired
    assert "Tight Scope" in rules_fired
    
    # Even with tight scope (+30) and high feasibility (+30), the max score must be capped at 60
    assert scores["overall_readiness"] <= 60

def test_high_feasibility_scenario():
    data = {
        "personas": "Local restaurant managers.",
        "problem_clarity": "Specific, clear.",
        "core_value_proposition": "Push notification alerts for low inventory.",
        "feature_scope_classification": "Single-purpose crud tool with basic alerts.",
        "technical_unknowns": "Simple straightforward notification system.",
        "market_risks": "Niche clear path.",
        "missing_components": "None."
    }
    
    scores, why, actions, triggered = score_idea(data)
    rules_fired = [r['rule_name'] for r in triggered]
    
    assert "High Technical Feasibility" in rules_fired
    assert scores["technical_feasibility"] >= 80 # Base 50 + 30

