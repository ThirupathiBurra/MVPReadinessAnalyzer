import os
import sys
from app import create_app
from db.database import db
from db.models import Idea, Report
from domain.schemas import StructuredIdeaInput
from services.scoring import score_idea

def seed_demo_data():
    app = create_app()
    with app.app_context():
        # Clear existing
        db.drop_all()
        db.create_all()

        scenarios = [
            {
                "input": {
                    "problem": "Freelancers struggle to track invoice status and chase late payments.",
                    "target_user": "Independent web designers and developers.",
                    "current_solution": "Manually checking bank accounts and sending awkward emails.",
                    "proposed_mvp": "A simple dashboard that connects to Stripe and sends automated polite follow-up emails for unpaid invoices."
                },
                "ai": {
                    "personas": "Freelancers.",
                    "problem_clarity": "Specific and clear.",
                    "core_value_proposition": "Automated invoice chasing.",
                    "feature_scope_classification": "Minimal and properly scoped.",
                    "technical_unknowns": "Standard Stripe integration.",
                    "market_risks": "Low risk, targeted niche.",
                    "missing_components": "None."
                }
            },
            {
                "input": {
                    "problem": "People are lonely and want to make friends.",
                    "target_user": "Everyone in the world.",
                    "current_solution": "Going outside or using Facebook.",
                    "proposed_mvp": "A massive social network with video calling, VR chat, crypto payments, and AI matching."
                },
                "ai": {
                    "personas": "Vague audience. Everyone.",
                    "problem_clarity": "Unclear and broad.",
                    "core_value_proposition": "Everything app.",
                    "feature_scope_classification": "Over-scoped bloat.",
                    "technical_unknowns": "VR and Crypto are highly complex unknowns.",
                    "market_risks": "Extremely high competition with existing giants.",
                    "missing_components": "A wedge or initial realistic feature."
                }
            }
        ]

        for s in scenarios:
            structured_input = StructuredIdeaInput(**s["input"])
            idea = Idea(description=structured_input.model_dump_json(), status="completed")
            db.session.add(idea)
            db.session.commit()
            db.session.refresh(idea)
            
            # Predict scores
            scores, why, actions, rules = score_idea(s["ai"])
            ai_data = s["ai"]
            ai_data["why_this_score"] = why
            ai_data["next_actions"] = actions
            scores["triggered_rules"] = rules

            report = Report(
                idea_id=idea.id,
                structured_data=ai_data,
                scores=scores
            )
            db.session.add(report)
            db.session.commit()
            
        print("Successfully seeded demo deterministic ideas.")

if __name__ == "__main__":
    seed_demo_data()
