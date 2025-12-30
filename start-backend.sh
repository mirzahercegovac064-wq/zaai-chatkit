#!/bin/bash

# Start the backend server
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/.installed" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    touch venv/.installed
fi

# Load environment variables and start server
echo "Starting backend server on http://localhost:8000"
export $(cat ../.env | xargs) 2>/dev/null || echo "Warning: .env file not found. Make sure to set environment variables."
python server.py

