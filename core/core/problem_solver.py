from typing import Dict, Any, List
from inference.groq_client import query_llama

class ProblemSolver:
    """Advanced problem-solving system that can generate solutions for complex programming problems"""
    
    @staticmethod
    def analyze_problem(problem_description: str) -> Dict[str, Any]:
        """Analyze a problem description to identify key components"""
        prompt = f"""
        Analyze the following programming problem description and break it down into components:
        
        {problem_description}
        
        Please identify:
        1. The main problem type (e.g., sorting, search, optimization)
        2. Input constraints and data structures needed
        3. Key algorithms or techniques that might be applicable
        4. Potential edge cases to consider
        5. Time and space complexity requirements if specified
        
        Format your response as a structured analysis.
        """
        
        analysis = query_llama(prompt)
        return {
            "description": problem_description,
            "analysis": analysis
        }
    
    @staticmethod
    def generate_solution(problem_analysis: Dict[str, Any], language: str = "python") -> Dict[str, Any]:
        """Generate a solution for the analyzed problem"""
        prompt = f"""
        Based on the following problem analysis, generate a {language} solution:
        
        PROBLEM DESCRIPTION:
        {problem_analysis['description']}
        
        ANALYSIS:
        {problem_analysis['analysis']}
        
        Please provide:
        1. A step-by-step approach to solving this problem
        2. Complete {language} code implementation
        3. Explanation of your solution's time and space complexity
        4. Any alternative approaches that could be considered
        """
        
        solution = query_llama(prompt)
        return {
            "language": language,
            "solution": solution
        }
    
    @staticmethod
    def translate_math_to_code(math_expression: str, language: str = "python") -> Dict[str, Any]:
        """Translate mathematical expressions or equations into code"""
        prompt = f"""
        Translate the following mathematical expression into {language} code:
        
        {math_expression}
        
        Please provide:
        1. The complete code implementation
        2. Explanation of how the implementation works
        3. Any necessary imports or libraries
        4. Example usage of the implementation
        """
        
        translated_code = query_llama(prompt)
        return {
            "original_math": math_expression,
            "language": language,
            "code": translated_code
        }
    
    @staticmethod
    def optimize_solution(code: str, language: str, optimization_goal: str = "time") -> Dict[str, Any]:
        """Optimize an existing solution based on specified goals"""
        prompt = f"""
        Optimize the following {language} code for {optimization_goal}:
        
        ```{language}
        {code}
        ```
        
        Please provide:
        1. The optimized code
        2. Explanation of the optimizations made
        3. Before and after complexity analysis
        4. Any tradeoffs involved in your optimization
        """
        
        optimized_solution = query_llama(prompt)
        return {
            "original_code": code,
            "optimization_goal": optimization_goal,
            "optimized_solution": optimized_solution
        }