import os
import sys
import json
from core.error_detector import analyze_file_for_errors

def display_error_report(file_path):
    """Display a formatted error report for a file"""
    print(f"\n{'='*80}")
    print(f"ANALYZING: {file_path}")
    print(f"{'='*80}")
    
    # Analyze the file
    results = analyze_file_for_errors(file_path)
    
    if not results or not results.get("errors"):
        print("✅ No errors detected in this file.")
        return
    
    errors = results