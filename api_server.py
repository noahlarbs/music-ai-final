#!/usr/bin/env python3
"""
FastAPI server for AI Guitar Solo Generator
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import json
import os
from pathlib import Path

from guitar_solo_backend import GuitarSoloAPI, GuitarStyle

# Initialize FastAPI app
app = FastAPI(
    title="AI Guitar Solo Generator",
    description="Generate guitar solos in different styles using AI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the guitar solo API
guitar_api = GuitarSoloAPI()

# Pydantic models for request/response
class SoloRequest(BaseModel):
    style: str
    length_bars: int = 8
    tempo: int = 120
    complexity: str = "medium"
    custom_description: Optional[str] = None
    chord_progression: Optional[List[str]] = None
    model: str = "musiclm"

class SoloResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    html_file = Path("guitar_solo_generator.html")
    if html_file.exists():
        return html_file.read_text()
    else:
        return """
        <html>
            <head><title>AI Guitar Solo Generator</title></head>
            <body>
                <h1>AI Guitar Solo Generator</h1>
                <p>API is running. Use /docs for API documentation.</p>
            </body>
        </html>
        """

@app.on_event("startup")
async def startup_event():
    """Initialize the guitar solo API on startup"""
    await guitar_api.initialize()

@app.post("/api/generate-solo", response_model=SoloResponse)
async def generate_solo(request: SoloRequest):
    """Generate a guitar solo based on the provided parameters"""
    try:
        result = await guitar_api.generate_solo(
            style=request.style,
            length_bars=request.length_bars,
            tempo=request.tempo,
            complexity=request.complexity,
            custom_description=request.custom_description,
            chord_progression=request.chord_progression,
            model=request.model
        )
        
        if "error" in result:
            return SoloResponse(success=False, error=result["error"])
        
        return SoloResponse(success=True, data=result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/styles")
async def get_available_styles():
    """Get list of available guitar styles"""
    styles = [style.value for style in GuitarStyle]
    return {"styles": styles}

@app.get("/api/models")
async def get_available_models():
    """Get list of available AI models"""
    models = list(guitar_api.generators.keys())
    return {"models": models}

@app.post("/api/upload-midi")
async def upload_midi(file: UploadFile = File(...)):
    """Upload a MIDI file for influence"""
    try:
        # Validate file type
        if not file.filename.endswith(('.mid', '.midi')):
            raise HTTPException(status_code=400, detail="Only MIDI files are allowed")
        
        # Save the file temporarily
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        
        file_path = upload_dir / file.filename
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return {
            "success": True,
            "filename": file.filename,
            "size": len(content)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "api_initialized": guitar_api.initialized}

# Example usage endpoints
@app.get("/api/example/blues")
async def example_blues_solo():
    """Generate an example blues solo"""
    result = await guitar_api.generate_solo(
        style="blues",
        length_bars=4,
        tempo=80,
        complexity="medium"
    )
    return result

@app.get("/api/example/metal")
async def example_metal_solo():
    """Generate an example metal solo"""
    result = await guitar_api.generate_solo(
        style="metal",
        length_bars=8,
        tempo=160,
        complexity="virtuoso"
    )
    return result

if __name__ == "__main__":
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 