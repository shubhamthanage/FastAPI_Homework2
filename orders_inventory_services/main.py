#!/usr/bin/env python3
# main.py - Root level entry point for the FastAPI application
from app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
