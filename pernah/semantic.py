from __future__ import annotations

import math
import re
from collections import Counter

from .storage import Storage


_STOPWORDS = {
    'aku', 'gue', 'saya', 'kita', 'lu', 'lo', 'yang', 'dan', 'di', 'ke', 'dari',
    'ini', 'itu', 'ada', 'dengan', 'sama', 'pernah', 'apa', 'apakah', 'gue',
    'the', 'a', 'an', 'i', 'we', 'you', 'is', 'are', 'was', 'were', 'did',
    'with', 'about', 'where', 'when', 'what', 'my', 'me', 'this', 'that',
}

# Small deterministic concept map. It is intentionally local and rebuildable;
# it is not an AI/provider dependency and does not alter canonical records.
_SYNONYMS = {
    # Purchase
    'beli': 'purchase', 'beliin': 'purchase', 'membeli': 'purchase',
    'buy': 'purchase', 'bought': 'purchase', 'pembelian': 'purchase',
    # Food
    'makan': 'food', 'makanan': 'food', 'kuliner': 'food',
    'sarapan': 'food', 'breakfast': 'food', 'dinner': 'food', 'lunch': 'food',
    # Conversation
    'ngobrol': 'conversation', 'obrolan': 'conversation', 'chat': 'conversation',
    'bicara': 'conversation', 'berbicara': 'conversation',
    'conversation': 'conversation',
    # Call
    'telepon': 'call', 'telefon': 'call', 'nelpon': 'call',
    'panggilan': 'call', 'call': 'call', 'calling': 'call', 'called': 'call',
    # Meeting
    'ketemu': 'meeting', 'bertemu': 'meeting', 'meet': 'meeting', 'meeting': 'meeting',
    # Collaboration
    'kerja': 'collaboration', 'bekerja': 'collaboration',
    'kolaborasi': 'collaboration', 'collaboration': 'collaboration',
    # Devices
    'laptop': 'computer', 'komputer': 'computer', 'computer': 'computer', 'pc': 'computer',
    'handphone': 'phone', 'hp': 'phone', 'smartphone': 'phone', 'phone': 'phone',
    # Passport
    'paspor': 'passport', 'passport': 'passport',
    # Commitment / decision
    'janji': 'commitment', 'berjanji': 'commitment', 'commitment': 'commitment',
    'promise': 'commitment', 'keputusan': 'decision', 'memutuskan': 'decision',
    'decision': 'decision',
}

_CONCEPT_TOKENS = set(_SYNONYMS.values())



def _tokens(text: str):
    raw = re.findall(r"[a-z0-9]+", text.lower())
    return [_SYNONYMS.get(token, token) for token in raw if token not in _STOPWORDS and len(token) > 1]


def _cosine(a: Counter, b: Counter) -> float:
    if not a or not b:
        return 0.0
    dot = sum(value * b.get(key, 0.0) for key, value in a.items())
    na = math.sqrt(sum(value * value for value in a.values()))
    nb = math.sqrt(sum(value * value for value in b.values()))
    return dot / (na * nb) if na and nb else 0.0


class SemanticIndex:
    """Rebuildable, deterministic TF-IDF index over canonical memories.

    The index exists only in memory. Canonical SQLite data remains authoritative;
    rebuilding the index from the same canonical rows produces the same ranking.
    """

    def __init__(self, rows):
        self.rows = list(rows)
        documents = [_tokens(row.get('content', '')) for row in self.rows]
        document_frequency = Counter()
        for tokens in documents:
            document_frequency.update(set(tokens))
        count = len(documents)
        self.idf = {token: math.log((1 + count) / (1 + df)) + 1 for token, df in document_frequency.items()}
        self.vectors = []
        for tokens in documents:
            counts = Counter(tokens)
            vector = Counter()
            for token, tf in counts.items():
                vector[token] = tf * self.idf[token]
            self.vectors.append(vector)

    def search(self, text: str, limit: int = 10, min_score: float = 0.0):
        query_tokens = _tokens(text)
        if not query_tokens:
            return []
        query_concepts = set(query_tokens) & _CONCEPT_TOKENS
        # A recognized concept acts as a deterministic relevance boundary.
        # Shared generic tokens (for example a person's name) must not make
        # an unrelated concept win merely because it has lexical overlap.
        # Query weights use the same corpus-independent representation for deterministic rebuilds.
        query_counts = Counter(query_tokens)
        query_vector = Counter({token: float(tf) * self.idf.get(token, 0.0) for token, tf in query_counts.items()})
        scored = []
        for index, (row, vector) in enumerate(zip(self.rows, self.vectors)):
            if query_concepts:
                document_concepts = set(_tokens(row.get('content', ''))) & _CONCEPT_TOKENS
                if not (query_concepts & document_concepts):
                    continue
            score = _cosine(query_vector, vector)
            if score > min_score:
                result = dict(row)
                result['score'] = round(score, 6)
                scored.append((score, row.get('occurred_at') or '', row.get('created_at') or '', row.get('id') or '', result))
        scored.sort(key=lambda item: (-item[0], item[1], item[2], item[3]))
        return [item[-1] for item in scored[:limit]]


def build_index(db: Storage) -> SemanticIndex:
    """Build a fresh derived index from canonical memory rows."""
    return SemanticIndex(db.list_memories())


def semantic_search(db: Storage, text: str, limit: int = 10, min_score: float = 0.0):
    """Search canonical memories through a rebuildable deterministic derived index."""
    return build_index(db).search(text, limit=limit, min_score=min_score)
