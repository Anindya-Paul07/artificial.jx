#!/usr/bin/env python3
"""
Demo Backend Test Script for J.A.R.V.I.S Assistant

This script tests various API endpoints of the J.A.R.V.I.S backend service.
It demonstrates how to interact with the backend programmatically.
"""

import requests
import json
import os
import time
import sys
from typing import Dict, Any, List, Optional

# Configuration
API_BASE_URL = "http://localhost:8000"  # FastAPI default port
TEST_FILE_PATH = "test_samples/test_code.py"  # Path to test file


class JarvisApiTester:
    """Client for testing J.A.R.V.I.S API functionality"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        
    def test_connection(self) -> bool:
        """Test if the API is running and accessible"""
        try:
            response = requests.get(f"{self.base_url}/status")
            data = response.json()
            if response.status_code == 200 and data.get("status") == "running":
                print("✅ Backend connection successful")
                return True
            else:
                print(f"❌ Backend connection issue: {data}")
                return False
        except Exception as e:
            print(f"❌ Cannot connect to backend: {e}")
            return False
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Test file analysis endpoint"""
        if not os.path.exists(file_path):
            print(f"❌ Test file not found: {file_path}")
            return {}
            
        try:
            response = requests.post(
                f"{self.base_url}/analyze",
                json={"file_path": os.path.abspath(file_path)}
            )
            
            if response.status_code == 200:
                result = response.json()
                error_count = len(result.get("errors", []))
                suggestion_count = len(result.get("suggestions", []))
                print(f"✅ File analysis complete: {error_count} errors, {suggestion_count} suggestions")
                return result
            else:
                print(f"❌ File analysis failed: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"❌ Error during file analysis: {e}")
            return {}
    
    def get_errors(self, file_path: Optional[str] = None) -> Dict[str, Any]:
        """Test error retrieval endpoint"""
        params = {}
        if file_path:
            params["file_path"] = os.path.abspath(file_path)
            
        try:
            response = requests.get(f"{self.base_url}/errors", params=params)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Retrieved error data successfully")
                return result
            else:
                print(f"❌ Error retrieval failed: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"❌ Error during error retrieval: {e}")
            return {}
    
    def solve_problem(self, problem: str, language: str = "python") -> Dict[str, Any]:
        """Test problem solving endpoint"""
        try:
            response = requests.post(
                f"{self.base_url}/solve-problem",
                json={"problem": problem, "language": language}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Problem solution generated successfully")
                return result
            else:
                print(f"❌ Problem solving failed: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"❌ Error during problem solving: {e}")
            return {}
    
    def translate_math(self, expression: str, language: str = "python") -> Dict[str, Any]:
        """Test math translation endpoint"""
        try:
            response = requests.post(
                f"{self.base_url}/translate-math",
                json={"expression": expression, "language": language}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Math translation completed successfully")
                return result
            else:
                print(f"❌ Math translation failed: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"❌ Error during math translation: {e}")
            return {}
    
    def optimize_code(self, code: str, language: str = "python", goal: str = "time") -> Dict[str, Any]:
        """Test code optimization endpoint"""
        try:
            response = requests.post(
                f"{self.base_url}/optimize-code",
                json={"code": code, "language": language, "goal": goal}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Code optimization completed successfully")
                return result
            else:
                print(f"❌ Code optimization failed: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"❌ Error during code optimization: {e}")
            return {}
    
    def suggest_docs(self) -> Dict[str, Any]:
        """Test documentation suggestion endpoint"""
        try:
            response = requests.get(f"{self.base_url}/suggest-docs")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Retrieved {len(result.get('suggestions', []))} documentation suggestions")
                return result
            else:
                print(f"❌ Documentation suggestion failed: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"❌ Error during doc suggestion: {e}")
            return {}
    
    def start_watcher(self, paths: List[str], file_types: List[str]) -> Dict[str, Any]:
        """Test folder watching endpoint"""
        try:
            response = requests.post(
                f"{self.base_url}/start-watch",
                json={"paths": paths, "file_types": file_types}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Folder watcher started successfully")
                return result
            else:
                print(f"❌ Folder watcher start failed: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"❌ Error starting folder watcher: {e}")
            return {}


def create_test_file():
    """Create a test Python file with intentional issues for testing"""
    os.makedirs(os.path.dirname(TEST_FILE_PATH), exist_ok=True)
    
    test_code = """
import numpy
import pandas
import re
import os
import json
import time
from datetime import datetime

# Unused import
import math

def calculate_average(numbers):
    # Inefficient implementation
    total = 0
    for num in numbers:
        total = total + num
    return total / len(numbers)

# Function with a bug
def find_max(lst):
    if len(lst) == 0:
        return None
    max_val = lst[0]
    for i in range(len(lst)):
        if lst[i] > max_val:
            max_val = lst[i]
    return max_val

class DataProcessor:
    def __init__(self, data):
        self.data = data
        
    def process(self):
        # Dummy method
        results = []
        for item in self.data:
            # Bare except clause (intentional issue)
            try:
                processed = self.transform(item)
                results.append(processed)
            except:
                pass
        return results
        
    def transform(self, item):
        # Another issue: double sorting (intentional)
        sorted_item = sorted(item)
        return sorted(sorted_item)
        
# Main functionality
if __name__ == "__main__":
    # Some test data
    test_data = [1, 2, 3, 4, 5]
    avg = calculate_average(test_data)
    print(f"Average: {avg}")
    
    max_val = find_max(test_data)
    print(f"Max value: {max_val}")
"""
    
    with open(TEST_FILE_PATH, "w") as f:
        f.write(test_code)
    
    print(f"✅ Created test file at {TEST_FILE_PATH}")


def run_demo():
    """Run the complete demo test suite"""
    print("=" * 50)
    print("J.A.R.V.I.S Backend Test Demo")
    print("=" * 50)
    
    # Create test client
    tester = JarvisApiTester(API_BASE_URL)
    
    # Check if backend is running
    if not tester.test_connection():
        print("\n❌ Backend server is not running. Please start it with:")
        print("   uvicorn fastapi_app:app --reload")
        return
    
    # Create test file if it doesn't exist
    if not os.path.exists(TEST_FILE_PATH):
        create_test_file()
    
    # Run tests with clear separation
    def section(name):
        print("\n" + "-" * 50)
        print(f"Testing: {name}")
        print("-" * 50)
    
    # Test file analysis
    section("File Analysis")
    analysis_result = tester.analyze_file(TEST_FILE_PATH)
    if analysis_result and analysis_result.get("errors"):
        for i, error in enumerate(analysis_result.get("errors")[:3], 1):  # Show first 3
            print(f"  Error {i}: {error.get('message')} (Line {error.get('line', '?')})")
    
    # Test error retrieval
    section("Error Retrieval")
    errors = tester.get_errors(TEST_FILE_PATH)
    
    # Test problem solving
    section("Problem Solving")
    problem = "Write a function to find the longest common subsequence of two strings"
    solution = tester.solve_problem(problem)
    
    # Test math translation
    section("Math Translation")
    math_expr = "∑(i=1 to n) i²"
    math_code = tester.translate_math(math_expr)
    
    # Test code optimization
    section("Code Optimization")
    code_to_optimize = """
def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
    """
    optimized = tester.optimize_code(code_to_optimize)
    
    # Test doc suggestions
    section("Documentation Suggestions")
    docs = tester.suggest_docs()
    
    # Test folder watcher
    section("Folder Watcher")
    watch_result = tester.start_watcher(["test_samples"], [".py", ".js"])
    
    print("\n" + "=" * 50)
    print("Demo completed!")
    print("=" * 50)


if __name__ == "__main__":
    run_demo()