import os
import json
import re
from utils.helpers import load_json, save_json
from agents.retriever_agent import retrieve_concept_explanation

DOC_MAP_PATH = "docs/keywords_to_docs.json"
METADATA_PATH = "core/code_metadata.json"
SUGGESTED_FIELD = "suggested_docs"

os.makedirs(os.path.dirname(METADATA_PATH), exist_ok=True)


def suggest_docs():
    doc_map = load_json(DOC_MAP_PATH)
    all_meta = load_json(METADATA_PATH)

    for file_path, meta in all_meta.items():
        summary = meta.get("summary", "")
        found_docs = []

        seen = set()
        for keyword in re.findall(r'\b\w+\b', summary):
            if keyword in seen: continue
            seen.add(keyword)

        if keyword in doc_map:
            found_docs.append({
                "keyword": keyword,
                "source": "official",
                "url": doc_map[keyword]
            })
        else:
            explanation = retrieve_concept_explanation(keyword)
            if explanation:
                found_docs.append({
                    "keyword":keyword,
                    "source":"knowledge_base",
                    "explanation": explanation
                })

    meta[SUGGESTED_FIELD] = found_docs
    all_meta[file_path] = meta

save_json(METADATA_PATH, all_meta)
print("[Junior] Smart documentation suggestion complete.")
