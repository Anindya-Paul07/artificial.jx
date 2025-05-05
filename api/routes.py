from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Any, Optional
import os
from core.error_detector import analyze_file_for_errors
from core.problem_solver import ProblemSolver
from utils.helpers import load_json

router = APIRouter()
problem_solver = ProblemSolver()
ERROR_ANALYSIS_PATH = "core/error_analysis.json"

@router.get("/")
def read_root():
    return {"message": "Junior FastAPI is running!"}

@router.get("/status")
def get_status():
    return {"status":"running", "message":"Junior backend is active."}

@router.post("/analyze")
def trigger_analysis(file_path: str = Body(...)):
    """Manually trigger analysis on a specific file"""
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
        
    results = analyze_file_for_errors(file_path)
    return results

@router.get("/errors")
def get_errors(file_path: Optional[str] = None):
    """Get error analysis results for all files or specific file"""
    if not os.path.exists(ERROR_ANALYSIS_PATH):
        return {"errors": []}
        
    error_data = load_json(ERROR_ANALYSIS_PATH)
    
    if file_path:
        return {"errors": error_data.get(file_path, {})}
    
    return {"errors": error_data}

@router.post("/solve-problem")
def solve_problem(problem: str = Body(...), language: str = Body("python")):
    """Generate a solution for a programming problem"""
    analysis = problem_solver.analyze_problem(problem)
    solution = problem_solver.generate_solution(analysis, language)
    return {
        "analysis": analysis,
        "solution": solution
    }

@router.post("/translate-math")
def translate_math(expression: str = Body(...), language: str = Body("python")):
    """Translate mathematical expressions to code"""
    result = problem_solver.translate_math_to_code(expression, language)
    return result

@router.post("/optimize-code")
def optimize_code(
    code: str = Body(...), 
    language: str = Body("python"),
    goal: str = Body("time")
):
    """Optimize existing code for time or space efficiency"""
    result = problem_solver.optimize_solution(code, language, goal)
    return result