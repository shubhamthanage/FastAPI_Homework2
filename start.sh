#!/bin/bash
# start.sh - Startup script for Render deployment

# Make sure we're in the right directory
cd /opt/render/project/src

# Install dependencies if needed
pip install -r requirements.txt

# Start the FastAPI application
exec uvicorn main:app --host 0.0.0.0 --port $PORT
