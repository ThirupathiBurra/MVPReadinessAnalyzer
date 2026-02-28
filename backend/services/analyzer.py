import json
from typing import Optional, Dict, Any
from db.database import db
from db.models import Idea, Report
from ai.client import AIClient
from services.scoring import score_idea
from domain.schemas import StructuredIdeaInput

class AnalyzerService:
    def __init__(self, ai_client: Optional[AIClient] = None):
        self.ai = ai_client or AIClient()

    def create_idea(self, structured_input: StructuredIdeaInput) -> Idea:
        # We store the structured content as a JSON string in the description text field
        description_json = structured_input.model_dump_json()
        idea = Idea(description=description_json, status="pending")
        db.session.add(idea)
        db.session.commit()
        db.session.refresh(idea)
        return idea

    def get_idea(self, idea_id: int) -> Optional[Idea]:
        return db.session.get(Idea, idea_id)

    def analyze_idea(self, idea_id: int) -> Optional[Report]:
        idea = self.get_idea(idea_id)
        if not idea:
            return None
            
        idea.status = "analyzing"
        db.session.commit()
            
        try:
            # Reconstruct the structured data
            idea_data = StructuredIdeaInput.model_validate_json(idea.description)
            
            # Structure the idea using AI
            structured_ai_data = self.ai.structure_idea(idea_data)
            
            if structured_ai_data.get("status") == "failed":
                idea.status = "failed"
                db.session.commit()
                return None
            
            # Calculate scores deterministically
            scores, why, actions, triggered_rules = score_idea(structured_ai_data)
            
            # Enrich AI data with explains
            structured_ai_data["why_this_score"] = why
            structured_ai_data["next_actions"] = actions
            
            # Since DB shouldn't change, stick triggered_rules into scores JSON column
            scores["triggered_rules"] = triggered_rules
            
            # Save the report
            report = Report(
                idea_id=idea.id,
                structured_data=structured_ai_data,
                scores=scores
            )
            db.session.add(report)
            
            idea.status = "completed"
            db.session.commit()
            db.session.refresh(report)
            return report
            
        except Exception as e:
            idea.status = "failed"
            db.session.commit()
            raise e

    def get_latest_report(self, idea_id: int) -> Optional[Report]:
        return db.session.query(Report)\
            .filter_by(idea_id=idea_id)\
            .order_by(Report.created_at.desc())\
            .first()
