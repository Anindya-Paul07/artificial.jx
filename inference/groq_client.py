import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()


llm = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    model_name="llama3-70b-8192",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.3,
    max_completion_tokens= 1024
)



def query_llama(prompt: str) -> str:
    try:
        res = llm.invoke([
            SystemMessage(content="You are a helpful programming assistant.Who implement code, find bug, debug it.Also suggest documentation related to my code."),
            HumanMessage(content=prompt)
        ])
        return res.content.strip()
    except Exception as e:
        print(f"[Junior] Groq LLaMa query error: {e}")
        return None