import os
import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.tools import tool
from langchain_core.utils import get_from_dict_or_env
from typing import Any, Dict, List, Optional, Mapping
from langchain_core.messages import BaseMessage
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.prompts.base import StringPromptValue
from langchain_core.prompts.chat import ChatPromptValue
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from core.cache_manager import cache_manager

# Initialize Groq client with OpenAI compatibility
llm = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    model_name="llama3-70b-8192",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.3,
    max_completion_tokens=1024
)

class AIAnalyzer:
    def __init__(self):
        self.llm = llm
        self.parser = JsonOutputParser()
        self.prompts = {
            "code_analysis": """
            You are a senior software engineer analyzing code. 
            Analyze the following code and provide:
            1. Potential bugs and issues
            2. Code optimization suggestions
            3. Documentation improvements
            4. Security concerns
            5. Performance bottlenecks
            
            Current Context: {context}
            Previous Steps: {steps}
            
            Code: {code}
            """,
            "error_fix": """
            You are a code error fixer. Analyze the error and suggest a fix.
            Error: {error}
            Code: {code}
            Context: {context}
            Previous Steps: {steps}
            """,
        }

    async def analyze_code(self, code: str, file_path: str = "") -> Dict[str, Any]:
        try:
            # Check cache first
            cache_key = f"analysis_{file_path}"
            cached_result = cache_manager.get(cache_key, "short_term")
            if cached_result:
                return cached_result

            # Create system message
            system_message = SystemMessage(content=self.prompts["code_analysis"])
            
            # Create human message with code
            human_message = HumanMessage(content=code)
            
            # Get response using existing Groq implementation
            response = self.llm.invoke([system_message, human_message])
            result = self.parser.parse(response.content)
            
            # Cache the result
            cache_manager.set(cache_key, result, "short_term", timedelta(hours=1))
            
            return result
        except Exception as e:
            print(f"Error analyzing code: {str(e)}")
            return {
                "suggestions": ["Failed to analyze code. Please try again."],
                "errors": [str(e)],
                "security_issues": [],
                "performance": [],
                "documentation": []
            }
            
    def fix_error(self, error: str, code: str, context: str) -> Dict[str, Any]:
        """Generate error fix suggestions using AI"""
        prompt = PromptTemplate.from_template(self.prompts["error_fix"])
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        try:
            result = chain.invoke({
                "error": error,
                "code": code,
                "context": context
            })
            return self._parse_fix(result)
        except Exception as e:
            return {"error": str(e)}
            
    def _parse_analysis(self, result: str) -> Dict[str, Any]:
        """Parse AI analysis results"""
        try:
            # Try to parse as JSON first
            return json.loads(result)
        except json.JSONDecodeError:
            # If not JSON, create structured response
            return {
                "raw_analysis": result,
                "parsed": self._extract_key_points(result)
            }
            
    def _extract_key_points(self, text: str) -> Dict[str, List[str]]:
        """Extract key points from free-form text"""
        key_points = {
            "bugs": [],
            "optimizations": [],
            "documentation": [],
            "security": [],
            "performance": []
        }
        
        # Simple pattern matching for common sections
        sections = text.split("\n\n")
        for section in sections:
            if "bug" in section.lower():
                key_points["bugs"].append(section)
            elif "optimize" in section.lower():
                key_points["optimizations"].append(section)
            elif "doc" in section.lower():
                key_points["documentation"].append(section)
            elif "security" in section.lower():
                key_points["security"].append(section)
            elif "performance" in section.lower():
                key_points["performance"].append(section)
        
        return key_points
        
    def _save_analysis(self, file_path: str, analysis: Dict[str, Any]):
        """Save analysis results to persistent storage"""
        analysis_path = "core/analysis_results.json"
        existing_data = load_json(analysis_path, default={})
        existing_data[file_path] = {
            "timestamp": time.time(),
            "analysis": analysis
        }
        save_json(analysis_path, existing_data)

# Initialize the analyzer
ai_analyzer = AIAnalyzer()
