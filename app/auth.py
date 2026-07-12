# app/auth.py
from fastapi import Header, HTTPException
from app.config import API_KEY

def check_auth(x_api_key: str):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
