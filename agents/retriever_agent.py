import json
import os
from utils.helpers import load_json, save_json
from inference.groq_client import query_llama
import requests

CACHE_PATH = "core/knowledge_base/cache.json"

def retreive_concept_explanation(term):
    cache = load_json(CACHE_PATH)
    if term in cache:
        print(f"[Junior] Retreived '{term}' from local KB. ")
        return cache[term]
    
    explanation = search_online(term)
    if not explanation:
        print(f"[Junior] Asking LLaMA 3 for '{term}'....")
        explanation = query_llama(f"Explain '{term}' in the context of programming.")
        if explanation:
            explanation = f"(AI-generated) {explanation}"

    if explanation:
        cache[term] = explanation
        save_json(CACHE_PATH, cache)
    return explanation

def search_online(term):
    print(f"[Junior] Searching online for '{term}'.....")
    try:
        url = f"https://api.duckduckgo.com/?q={term}+programming&format=json"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            return data.get("AbstractText") or data.get("RelatedTopics", [{}])[0].get("Text")
    except Exception as e :
        print(f"[Junior] Online search error {e}")
    return  None