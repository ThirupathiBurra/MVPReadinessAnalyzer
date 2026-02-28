# MVP Readiness Analyzer

## 1. Project Overview
The MVP Readiness Analyzer is an engineering tool that evaluates early-stage startup ideas for technical and market viability. It solves a common problem: founders building over-scoped, poorly targeted minimum viable products based on unstructured or hallucinated AI advice.
**System Philosophy:** Decouple natural language understanding from mathematical business logic to deliver deterministic, change-resilient scoring.

## 2. Live Demo Flow
1. **Idea Input**: User submits Problem, Target User, Current Solution, and Proposed MVP text.
2. **Analysis State**: System displays transparent lifecycle progress while routing data.
3. **Decision Report**: User receives a high-contrast executive document detailing the final score, category breakdowns, and a trace of triggered business rules.

## 3. System Architecture
User Input → AI Structuring (JSON Extraction) → Deterministic Rule Engine (Python) → Decision Report

## 4. Backend Design
The Python backend is strictly layered for separation of concerns:
- **API Layer**: Route handlers for HTTP requests, schema validation, and traffic control.
- **AI Client**: Integration layer for LLMs (OpenAI, OpenRouter, Nvidia). Responsible only for secure transmission and JSON parsing.
- **Scoring Engine**: The core domain logic. Evaluates structured data using registered Python rule classes to calculate scores.
- **Persistence Layer**: SQLAlchemy ORM and SQLite database for storing raw inputs, structured analysis, and final reports.

## 5. Scoring Engine (Core Differentiator)
- **Composable Rule Pipeline**: Scoring is not a nested `if/else` block. It uses independent `Rule` classes (e.g., `ScopeBloatRule`, `ClearTargetUserRule`).
- **Adding Logic**: New product constraints are added by defining a new class and appending it to the `REGISTERED_RULES` list.
- **Score Invariants**: The engine enforces mathematical bounds, ensuring the final score never exceeds 100 or drops below 0.
- **Category Caps**: Severe risks (like extreme market weakness) trigger invariants that cap the maximum possible overall score.
- **Why Deterministic?**: Deterministic scoring ensures identical inputs yield identical scores, enabling strict regression testing and removing AI hallucinations from the decision process.

## 6. AI Usage Strategy
- **Signal Extraction, Not Decision-Making**: The LLM is used strictly as a parser to convert unstructured text into a known JSON schema. It does not judge the idea.
- **Strict Schema Validation**: Pydantic models enforce the expected AI output structure.
- **Fallback Mode**: The client safely handles diverse API environments via dynamic provider detection.
- **Why AI Doesn't Score**: Keeping AI away from the final math guarantees predictable rules and eliminates hallucination-driven advice.

## 7. Correctness & Verification
- **Scenario-Based Testing**: Test payloads representing "Ideal MVPs" and "Over-scoped Bloats" are evaluated in the CI pipeline.
- **Rule-Trigger Assertions**: Tests assert *exactly which internal rules* must trigger for a given payload, not just the final score.
- **Regression Safety**: Any modification to existing rule logic instantly breaks the assertions, preventing accidental business logic degradation.
- **Bounded Score Guarantees**: Code-level invariants assert that scores remain mathematically valid under all conditions.

## 8. Change Resilience
- **Independent Evolution**: The product logic (scoring rules) can evolve drastically without requiring a single change to the LLM system prompt, database schema, or frontend React components.
- **Why This Matters**: In real product development, business rules change daily. This architecture allows product engineers to tune weights and logic safely without coordinating full-stack database migrations.

## 9. Observability & Lifecycle
- **Status Flow**: The frontend securely tracks the backend lifecycle state (e.g., "Structuring idea", "Applying scoring pipeline").
- **Metrics Endpoint**: System throughput and health are exposed via a `/api/metrics` route.
- **Transparent Rule Trace**: The final UI exposes the exact pipeline evaluation trace, showing the user the precise variables that impacted their score.

## 10. Demo Mode
- **Why It Exists**: To allow zero-latency, highly predictable technical walkthroughs without relying on rate-limited, paid third-party APIs.
- **How It Works**: A predefined `seed_demo.sh` script injects mocked payloads and deterministic reports directly into the local SQLite database. The frontend renders these instantly.

## 11. Frontend Philosophy
- **Decision-Document Layout**: The interface acts as a professional SaaS executive summary, not a chatbox.
- **Typography-Driven Hierarchy**: Relies heavily on font scale and spacing instead of borders to guide the user's eye to the massive "Hero Score".
- **Fast Scannability**: Deeply nested data is flattened into clear grids and concise UI lists.

## 12. Tech Stack
- **Backend**: Python, Flask, SQLAlchemy, Pydantic
- **Frontend**: React, Vite, Vanilla CSS
- **Database**: SQLite
- **AI Integration**: OpenAI, OpenRouter, or Nvidia (dynamically routed)

## 13. Local Development Setup
**Backend:**
*Requires a `.env` file in the `/backend` directory containing an API key (e.g., `OPENAI_API_KEY=sk-...` or `OPENROUTER_API_KEY=sk-or-v1-...`).*
*Note: The SQLite database instance is automatically generated on the first run.*
```bash
cd backend
uv sync
uv run app.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Demo Data:**
```bash
./seed_demo.sh
```

**Running Tests:**
```bash
cd backend
uv run pytest -v
```

## 14. Key Engineering Tradeoffs
- **Used SQLite**: Provides a zero-configuration, self-contained environment perfect for a readiness assessment, avoiding the overhead of Docker or cloud infrastructure.
- **Skipped Auth**: This is an evaluation tool, not a multi-tenant B2B platform. Adding auth would needlessly complicate the technical demonstration of the core AI-to-Deterministic engine.
- **Avoided Background Workers**: The synchronous HTTP flow was intentionally retained to keep the setup simple and easy to reason about during a single-user review.

## 15. How This Would Scale in Production
- Migrate SQLite to PostgreSQL.
- Move the LLM generation step out of the HTTP request cycle and into an asynchronous task queue (e.g., Celery/Redis).
- Implement Server-Sent Events (SSE) or WebSockets to stream exact state updates to the frontend instead of relying on frontend interval polling.

## 16. Assessment Alignment
- **Structure**: Deeply layered architecture separating API, AI, Domain Logic, and Persistence.
- **Simplicity**: Zero-config database, vanilla CSS, and standard HTTP conventions.
- **Correctness**: Enforced boundaries, unit-tested rule triggers, and robust Pydantic schemas.
- **Change Resilience**: Composable Python classes allow logic tuning without full-stack disruption.
- **AI Guidance**: The LLM is leashed to a strict JSON extraction task, never permitted to execute business logic.

## 17. AI Guidance & Prompts
The core system prompt that forces the LLM to act strictly as a structured data extractor (preventing it from acting as a product evaluator) is securely configured in `backend/ai/client.py`. There are no hidden agent frameworks or magic abstraction layers; prompt behavior is fully exposed in a single, traceable client.
