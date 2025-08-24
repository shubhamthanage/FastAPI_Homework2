#!/usr/bin/env python3
# main.py - Root level entry point for the FastAPI application
# This file should be in the FastAPI_Homework2 root directory
import os
from orders_inventory_services.app.main import app

if __name__ == "__main__":
    import uvicorn
    # Get port from environment variable (Render provides this) or default to 8000
    port = int(os.environ.get("PORT", 8000))
    # Bind to 0.0.0.0 to accept external connections (required for Render)
    uvicorn.run(app, host="0.0.0.0", port=port)
