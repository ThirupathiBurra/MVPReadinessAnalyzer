from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime

# ==========================================
# Phase 2: Input Payload Schemas
# ==========================================
class StructuredIdeaInput(BaseModel):
    problem: str = Field(..., min_length=10, description="The problem being solved")
    target_user: str = Field(..., min_length=5, description="Who experiences this problem")
    current_solution: str = Field(..., min_length=5, description="How they solve it today")
    proposed_mvp: str = Field(..., min_length=10, description="The proposed solution")

class IdeaCreate(BaseModel):
    structured_idea: StructuredIdeaInput

class IdeaResponse(BaseModel):
    id: int
    description: str # Stores the serialized structured_idea
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# ==========================================
# Phase 2: AI Contract Schemas
# ==========================================
class AIAnalysisContract(BaseModel):
    personas: str = Field(description="Target personas breakdown")
    problem_clarity: str = Field(description="Evaluation of problem clarity")
    core_value_proposition: str = Field(description="The core value proposition")
    feature_scope_classification: str = Field(description="Scope assessment (e.g., MVP, Over-scoped)")
    technical_unknowns: str = Field(description="Potential technical risks")
    market_risks: str = Field(description="Potential market or distribution risks")
    missing_components: str = Field(description="What is obviously missing from the idea")

# ==========================================
# Output & Report Schemas
# ==========================================
class ReportResponse(BaseModel):
    id: int
    idea_id: int
    structured_data: Dict[str, Any]
    scores: Dict[str, Any]
    created_at: datetime
    
    class Config:
        from_attributes = True
