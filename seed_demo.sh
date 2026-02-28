#!/usr/bin/env bash
cd backend
echo "Seeding deterministic demo ideas..."
uv run python seed_demo.py
echo "Seed complete. You can now click the Demo scenarios in the Frontend."
