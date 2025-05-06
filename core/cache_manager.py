import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from pathlib import Path
import sqlite3
from utils.helpers import load_json, save_json

class CacheManager:
    def __init__(self):
        self.cache_dir = Path("core/cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize different cache layers
        self.caches = {
            "short_term": LRUCache(100),  # In-memory cache for quick access
            "medium_term": FileCache(self.cache_dir / "medium_term"),  # Disk-based cache
            "long_term": SQLiteCache(self.cache_dir / "long_term.db"),  # Persistent storage
            "context": ContextCache(self.cache_dir / "context.json"),  # Context tracking
            "memory": MemoryCache(self.cache_dir / "memory.json")  # Step memory
        }
        
        # Initialize RAG components
        self.knowledge_base = KnowledgeBase()
        self.embeddings = Embeddings()
        
    def get(self, key: str, cache_type: str = "short_term") -> Optional[Any]:
        """Get value from specified cache layer"""
        return self.caches[cache_type].get(key)
        
    def set(self, key: str, value: Any, cache_type: str = "short_term", ttl: Optional[timedelta] = None) -> None:
        """Set value in specified cache layer"""
        self.caches[cache_type].set(key, value, ttl)
        
    def add_to_context(self, context: Dict[str, Any]) -> None:
        """Add new context information"""
        self.caches["context"].add(context)
        
    def add_to_memory(self, step: Dict[str, Any]) -> None:
        """Add a new step to memory"""
        self.caches["memory"].add(step)
        
    def get_recent_context(self) -> List[Dict[str, Any]]:
        """Get recent context information"""
        return self.caches["context"].get_recent()
        
    def get_memory_steps(self) -> List[Dict[str, Any]]:
        """Get all memory steps"""
        return self.caches["memory"].get_steps()
        
    def search_knowledge_base(self, query: str) -> List[Dict[str, Any]]:
        """Search knowledge base using RAG"""
        return self.knowledge_base.search(query)

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.order = []
        
    def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        return None
        
    def set(self, key: str, value: Any, ttl: Optional[timedelta] = None) -> None:
        if len(self.cache) >= self.capacity:
            oldest = self.order.pop(0)
            del self.cache[oldest]
            
        self.cache[key] = value
        self.order.append(key)

class FileCache:
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def get(self, key: str) -> Optional[Any]:
        file_path = self.cache_dir / f"{key}.json"
        if file_path.exists():
            return load_json(file_path)
        return None
        
    def set(self, key: str, value: Any, ttl: Optional[timedelta] = None) -> None:
        file_path = self.cache_dir / f"{key}.json"
        save_json(file_path, value)

class SQLiteCache:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.conn = sqlite3.connect(str(db_path))
        self._create_tables()
        
    def _create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    created_at TIMESTAMP,
                    expires_at TIMESTAMP
                )
            """)
            
    def get(self, key: str) -> Optional[Any]:
        with self.conn:
            result = self.conn.execute(
                "SELECT value FROM cache WHERE key = ? AND expires_at > ?",
                (key, datetime.now())
            ).fetchone()
            if result:
                return json.loads(result[0])
        return None
        
    def set(self, key: str, value: Any, ttl: Optional[timedelta] = None) -> None:
        expires_at = None
        if ttl:
            expires_at = datetime.now() + ttl
            
        with self.conn:
            self.conn.execute(
                """
                INSERT OR REPLACE INTO cache (key, value, created_at, expires_at)
                VALUES (?, ?, ?, ?)
                """,
                (key, json.dumps(value), datetime.now(), expires_at)
            )

class ContextCache:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.context = []
        self.max_context = 5
        
    def add(self, context: Dict[str, Any]):
        self.context.append({
            "timestamp": datetime.now().isoformat(),
            "data": context
        })
        self.context = self.context[-self.max_context:]
        self._save()
        
    def get_recent(self) -> List[Dict[str, Any]]:
        return self.context
        
    def _save(self):
        save_json(self.file_path, self.context)

class MemoryCache:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.steps = []
        self.max_steps = 10
        
    def add(self, step: Dict[str, Any]):
        self.steps.append({
            "timestamp": datetime.now().isoformat(),
            "step": step
        })
        self.steps = self.steps[-self.max_steps:]
        self._save()
        
    def get_steps(self) -> List[Dict[str, Any]]:
        return self.steps
        
    def _save(self):
        save_json(self.file_path, self.steps)

class KnowledgeBase:
    def __init__(self):
        self.docs = []
        self.embeddings = Embeddings()
        
    def add_document(self, doc: Dict[str, Any]):
        self.docs.append(doc)
        
    def search(self, query: str) -> List[Dict[str, Any]]:
        query_embedding = self.embeddings.get_embedding(query)
        return self._semantic_search(query_embedding)
        
    def _semantic_search(self, query_embedding: List[float]) -> List[Dict[str, Any]]:
        results = []
        for doc in self.docs:
            score = self.embeddings.calculate_similarity(
                query_embedding,
                doc["embedding"]
            )
            results.append({
                "doc": doc,
                "score": score
            })
        return sorted(results, key=lambda x: x["score"], reverse=True)[:5]

class Embeddings:
    def __init__(self):
        self.model = "text-embedding-ada-002"  # Using OpenAI's embedding model
        
    def get_embedding(self, text: str) -> List[float]:
        # This would be replaced with actual OpenAI API call
        return [0.0] * 1536  # Placeholder
        
    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        # Simple cosine similarity calculation
        dot_product = sum(a*b for a,b in zip(embedding1, embedding2))
        norm1 = sum(x*x for x in embedding1) ** 0.5
        norm2 = sum(x*x for x in embedding2) ** 0.5
        return dot_product / (norm1 * norm2)

# Initialize cache manager
cache_manager = CacheManager()
