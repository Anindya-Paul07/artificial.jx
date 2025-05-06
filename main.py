from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import yaml
from core.ai_analyzer import AIAnalyzer
from core.cache_manager import CacheManager
import os
from github import Github
from pathlib import Path

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    code: str
    file_path: str
    context: Optional[str] = None

class GitHubRepo(BaseModel):
    owner: str
    repo: str
    path: Optional[str] = None

# Initialize components
ai_analyzer = AIAnalyzer()
cache_manager = CacheManager()

@app.post("/analyze")
async def analyze_code(request: AnalysisRequest):
    try:
        result = await ai_analyzer.analyze_code(request.code, request.file_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save uploaded file temporarily
        file_location = f"uploads/{file.filename}"
        os.makedirs("uploads", exist_ok=True)
        
        with open(file_location, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
            
        # Analyze the file
        with open(file_location, "r") as f:
            code = f.read()
            result = await ai_analyzer.analyze_code(code, file_location)
            
        # Clean up
        os.remove(file_location)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/github/repo")
async def analyze_github_repo(repo: GitHubRepo):
    try:
        # Initialize GitHub client
        g = Github(os.getenv("GROQ_API_KEY"))
        repository = g.get_repo(f"{repo.owner}/{repo.repo}")
        
        # Get files from repository
        contents = repository.get_contents(repo.path or "")
        
        results = []
        
        # Analyze each file
        for content in contents:
            if content.type == "file":
                file_content = repository.get_contents(content.path).decoded_content.decode()
                analysis = await ai_analyzer.analyze_code(
                    file_content,
                    content.path
                )
                results.append({
                    "file": content.path,
                    "analysis": analysis
                })
        
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)