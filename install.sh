#!/usr/bin/env bash

# Install backend dependencies
echo "Installing backend dependencies mapping to pyproject.toml..."
cd backend
uv sync

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd ../frontend
npm install

echo "Installation complete."
