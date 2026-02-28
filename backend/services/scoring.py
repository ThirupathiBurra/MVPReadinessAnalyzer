from typing import Dict, Any, List, Tuple
from domain.schemas import AIAnalysisContract

class Rule:
    """Base abstraction for a scoring rule."""
    name = "Base Rule"
    description = "Description of what this rule evaluates."
    category = "general"

    def evaluate(self, data: AIAnalysisContract) -> Tuple[bool, int, str, str]:
        """
        Returns (triggered: bool, score_delta: int, reason: str, action: str)
        """
        return False, 0, "", ""

class ClearTargetUserRule(Rule):
    name = "Clear Target User"
    description = "Rewards highly specific and well-defined target audiences."
    category = "problem_understanding"
    
    def evaluate(self, data: AIAnalysisContract) -> Tuple[bool, int, str, str]:
        text = data.problem_clarity.lower() + " " + data.personas.lower()
        
        has_clear_words = any(w in text for w in ['high', 'well-defined', 'specific']) or ('clear' in text and 'unclear' not in text)
        if has_clear_words:
            return True, 30, "The problem and target user are highly focused.", ""
        return False, 0, "", ""

class VagueTargetUserRule(Rule):
    name = "Vague Target User"
    description = "Penalizes vague or overly broad target audiences."
    category = "problem_understanding"
    
    def evaluate(self, data: AIAnalysisContract) -> Tuple[bool, int, str, str]:
        text = data.problem_clarity.lower() + " " + data.personas.lower()
        if 'vague' in text or 'broad' in text or 'unclear' in text or 'everyone' in text:
            return True, -20, "Target audience is too broad or poorly defined.", "Define a specific niche audience who feels this problem most acutely."
        return False, 0, "", ""

class MarketWeaknessRule(Rule):
    name = "Market Weakness"
    description = "Penalizes saturated markets with no differentiation or low urgency."
    category = "market_viability"

    def evaluate(self, data: AIAnalysisContract) -> Tuple[bool, int, str, str]:
        text = data.market_risks.lower()
        if any(w in text for w in ['saturated', 'no differentiation', 'low urgency', 'crowded', 'high competition']):
            return True, -30, "Market is highly saturated or lacks urgent demand.", "Identify a highly specific niche or wedge strategy to enter."
        return False, 0, "", ""

class ManageableMarketRiskRule(Rule):
    name = "Manageable Market Risk"
    description = "Rewards manageable market dynamics."
    category = "market_viability"

    def evaluate(self, data: AIAnalysisContract) -> Tuple[bool, int, str, str]:
        text = data.market_risks.lower()
        if 'low' in text or 'manageable' in text or 'niche' in text or 'clear path' in text:
            return True, 20, "Market risks appear manageable.", ""
        return False, 0, "", ""

class HighFeasibilityRule(Rule):
    name = "High Technical Feasibility"
    description = "Rewards straightforward technical builds."
    category = "technical_feasibility"

    def evaluate(self, data: AIAnalysisContract) -> Tuple[bool, int, str, str]:
        text = data.technical_unknowns.lower() + " " + data.feature_scope_classification.lower()
        if any(w in text for w in ['crud', 'notification', 'single-purpose', 'simple tool', 'straightforward', 'standard']):
            return True, 30, "Technical path is well-understood and straightforward.", ""
        return False, 0, "", ""

class MediumFeasibilityRule(Rule):
    name = "Medium Technical Feasibility"
    description = "Rewards standard integrations and multi-role workflows."
    category = "technical_feasibility"

    def evaluate(self, data: AIAnalysisContract) -> Tuple[bool, int, str, str]:
        text = data.technical_unknowns.lower() + " " + data.feature_scope_classification.lower()
        if any(w in text for w in ['integration', 'dashboard', 'multi-role']):
            # Ensure it doesn't overlap with high feasibility implicitly if they co-occur, but medium is standard
            return True, 10, "Technical path requires standard integrations.", ""
        return False, 0, "", ""

class LowFeasibilityRule(Rule):
    name = "Low Technical Feasibility"
    description = "Penalizes projects with deep-tech or distributed complexities."
    category = "technical_feasibility"

    def evaluate(self, data: AIAnalysisContract) -> Tuple[bool, int, str, str]:
        text = data.technical_unknowns.lower()
        if any(w in text for w in ['deep-tech', 'hardware', 'research', 'distributed', 'blockchain', 'ai model training', 'complex', 'impossibilities']):
            return True, -40, "Significant technical uncertainties or hardware/deep-tech requirements exist.", "Build a small proof-of-concept for the riskiest technical component first."
        return False, 0, "", ""

class MultiWorkflowBloatRule(Rule):
    name = "Multi-Workflow Bloat"
    description = "Penalizes heavily if multiple workflows or platforms are bundled."
    category = "scope_realism"

    def evaluate(self, data: AIAnalysisContract) -> Tuple[bool, int, str, str]:
        text = data.feature_scope_classification.lower() + " " + data.problem_clarity.lower()
        if any(w in text for w in ['multiple', 'platform', 'suite', 'bundle', 'all-in-one']):
            return True, -40, "The MVP bundles multiple workflows or is scoped as a platform.", "Cut features aggressively. Focus on answering ONE core user job to start."
        return False, 0, "", ""

class ScopeBloatRule(Rule):
    name = "Scope Bloat"
    description = "Penalizes general over-scoped MVPs."
    category = "scope_realism"

    def evaluate(self, data: AIAnalysisContract) -> Tuple[bool, int, str, str]:
        text = data.feature_scope_classification.lower()
        if 'over' in text or 'bloat' in text or 'too many' in text or 'large' in text:
            return True, -30, "The proposed MVP is likely over-scoped.", "Wait, cut features. What is the single core feature?"
        return False, 0, "", ""

class TightScopeRule(Rule):
    name = "Tight Scope"
    description = "Rewards a tightly defined MVP."
    category = "scope_realism"

    def evaluate(self, data: AIAnalysisContract) -> Tuple[bool, int, str, str]:
        text = data.feature_scope_classification.lower()
        if 'tight' in text or 'mvp' in text or 'focused' in text or 'minimal' in text:
            # But wait, 'mvp' is common. We'll check for tight/minimal mostly or 'properly scoped'
            if 'over' not in text and 'bloat' not in text:
                return True, 30, "The MVP scope is tight and realistic.", ""
        return False, 0, "", ""

class ValidCoreValueRule(Rule):
    name = "Valid Core Value"
    description = "Rewards a strong, clear core value proposition."
    category = "problem_understanding"
    
    def evaluate(self, data: AIAnalysisContract) -> Tuple[bool, int, str, str]:
        text = data.core_value_proposition.lower()
        if 'clear' in text or 'strong' in text or 'compelling' in text or len(text) > 15:
            return True, 10, "Has a clear core value proposition.", ""
        return False, 0, "", ""

# Registry of all active rules
REGISTERED_RULES = [
    ClearTargetUserRule(),
    VagueTargetUserRule(),
    MarketWeaknessRule(),
    ManageableMarketRiskRule(),
    HighFeasibilityRule(),
    MediumFeasibilityRule(),
    LowFeasibilityRule(),
    MultiWorkflowBloatRule(),
    ScopeBloatRule(),
    TightScopeRule(),
    ValidCoreValueRule()
]

def score_idea(ai_data: Dict[str, Any]) -> Tuple[Dict[str, int], str, str, List[Dict[str, Any]]]:
    """
    Evaluates all registered rules against the structured AI data.
    Returns:
       scores (dict), why_this_score (str), next_actions (str), triggered_rules (list of dicts)
    """
    try:
        data = AIAnalysisContract(**ai_data)
    except Exception:
        return {"overall_readiness": 0}, "Invalid AI data.", "Please run analysis again.", []

    category_scores = {
        "problem_understanding": 50,
        "market_viability": 50,
        "technical_feasibility": 50,
        "scope_realism": 50,
    }

    reasons = []
    actions = []
    triggered_rules = []

    for rule in REGISTERED_RULES:
        triggered, delta, reason, action = rule.evaluate(data)
        if triggered:
            # Apply delta
            if rule.category in category_scores:
                category_scores[rule.category] += delta
            
            if reason: reasons.append(reason)
            if action: actions.append(action)
            
            triggered_rules.append({
                "rule_name": rule.name,
                "category": rule.category,
                "delta": delta,
                "reason": reason
            })

    # Clamp scores and calculate overall
    def clamp(v): return max(0, min(100, v))
    
    final_scores = {k: clamp(v) for k, v in category_scores.items()}
    
    # Mathematical Invariants for Phase 4
    # 1. Market Cap Rule
    market_weakness_triggered = any(r['rule_name'] == "Market Weakness" for r in triggered_rules)
    
    # Base calculation
    overall = int(sum(final_scores.values()) / len(final_scores))
    
    # Apply score balancing invariants
    if market_weakness_triggered:
        overall = min(overall, 60)
        
    if final_scores["market_viability"] < 30 or final_scores["scope_realism"] < 30:
        overall = min(overall, 50)
        
    final_scores["overall_readiness"] = overall

    why_this_score = " ".join(reasons) if reasons else "Base score applied."
    next_actions = " ".join(actions) if actions else "Proceed to build the MVP."

    return final_scores, why_this_score, next_actions, triggered_rules

def get_architecture() -> List[Dict[str, Any]]:
    """Returns static metadata about the scoring system for the visibility endpoint."""
    return [
        {
            "name": r.name,
            "description": r.description,
            "category": r.category
        } for r in REGISTERED_RULES
    ]
