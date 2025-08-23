# app/core/security.py
# small helpers - not used heavily here but placeholder for future auth
from fastapi import HTTPException, status

def require_api_key(key: str | None):
    # in production, check against env-stored API keys
    if key != "devapikey":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")