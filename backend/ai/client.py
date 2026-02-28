import os
import time
import json
import logging
from typing import Dict, Any, Optional
from openai import OpenAI
from pydantic import ValidationError
from domain.schemas import AIAnalysisContract, StructuredIdeaInput

logger = logging.getLogger('ai.observability')

class AIClient:
    """Wrapper for AI interactions.
    If OPENAI_API_KEY is not set, returns a deterministic mock response.
    Handles strict JSON output and fallback validation."""
    
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.base_url = None
        self.model = "gpt-4o"
        
        # OpenRouter support detection
        if self.api_key and self.api_key.startswith("sk-or-v1-"):
            self.base_url = "https://openrouter.ai/api/v1"
            self.model = "openai/gpt-4o"
            
        # Nvidia API support detection
        elif self.api_key and self.api_key.startswith("nvapi-"):
            self.base_url = "https://integrate.api.nvidia.com/v1"
            self.model = "meta/llama-3.1-70b-instruct"

        if self.api_key and self.api_key != "dummy":
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
        else:
            self.client = None

    def structure_idea(self, idea_data: StructuredIdeaInput) -> Dict[str, Any]:
        """Takes an idea description and restructures it into standard components."""
        start_time = time.time()
        
        # Format the prompt context
        context = f"""
        Problem: {idea_data.problem}
        Target User: {idea_data.target_user}
        Current Solution: {idea_data.current_solution}
        Proposed MVP: {idea_data.proposed_mvp}
        """

        try:
            if not self.client:
                logger.info("OPENAI_API_KEY missing or dummy. Using deterministic mock.")
                result = self._mock_structure(context)
            else:
                result = self._live_structure(context)
            
            # Validate output matches contract
            validated = AIAnalysisContract(**result)
            
            latency = time.time() - start_time
            logger.info(f"AI Analysis Succeeded. Latency: {latency:.2f}s")
            return validated.model_dump()
            
        except ValidationError as e:
            logger.error(f"AI output failed validation: {str(e)}")
            return {"status": "failed", "reason": "Contract Validation Error"}
        except Exception as e:
            latency = time.time() - start_time
            logger.error(f"AI Analysis Failed. Error: {str(e)}. Latency: {latency:.2f}s")
            return {"status": "failed", "reason": "AI Execution Error"}
            
    def _mock_structure(self, description: str) -> Dict[str, Any]:
        """Fallback deterministic behavior for Phase 1/offline."""
        return {
            "personas": "Small business owners seeking simple alternatives",
            "problem_clarity": "High. The problem is well-defined.",
            "core_value_proposition": "Time savings through automation.",
            "feature_scope_classification": "MVP scoped properly.",
            "technical_unknowns": "Integration with legacy APIs.",
            "market_risks": "High competition in the space.",
            "missing_components": "No clear billing or subscription limits."
        }

    def _live_structure(self, description: str) -> Dict[str, Any]:
        """Real OpenAI call utilizing strict JSON generation."""
        # Using a system prompt that mandates the specific JSON keys
        response = self.client.chat.completions.create(
            model=getattr(self, "model", "gpt-4o"), # Standard or OpenRouter model
            response_format={ "type": "json_object" },
            messages=[
                {
                    "role": "system", 
                    "content": "You are a Startup Advisor AI. You only reply in strict JSON. The JSON keys MUST EXACTLY MATCH: personas, problem_clarity, core_value_proposition, feature_scope_classification, technical_unknowns, market_risks, missing_components. CRITICAL: Every single value in the JSON MUST be a simple STRING (e.g. \"High risk\" or \"Small Business\"). Do NOT use nested lists, objects, booleans, or integers."
                },
                {
                    "role": "user",
                    "content": f"Analyze this startup idea context and provide the JSON assessment:\n{description}"
                }
            ]
        )
        
        # It's highly probable exact json due to format and prompt
        content = response.choices[0].message.content
        return json.loads(content)
