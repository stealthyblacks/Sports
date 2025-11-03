#!/usr/bin/env python3
"""
Minimal Test Server to diagnose issues
"""
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Test server is working!", "status": "ok"}

@app.get("/test")
def test_endpoint():
    return {"test": "success", "data": [1, 2, 3]}

if __name__ == "__main__":
    print("🧪 Starting minimal test server...")
    uvicorn.run(app, host="127.0.0.1", port=8001)