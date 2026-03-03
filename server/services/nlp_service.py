# ═══════════════════════════════════════════════════════════
# server/services/nlp_service.py
# NLP Intent Classification Engine
# Keyword-based scorer against live KnowledgeBase table
# FR-2.1 Intent Recognition | FR-2.3 Fallback Mechanism
# ═══════════════════════════════════════════════════════════

import re
import random

from server.models.models import KnowledgeBase, Motivation

# Minimum confidence score to accept a match (below → fallback)
# Lowered from 40.0 — old formula made even perfect single-keyword
# matches score too low (e.g. 1 match out of 8 keywords = 10 points)
FALLBACK_THRESHOLD = 15.0

FALLBACK_RESPONSE = (
    "I'm not fully confident I understood your question. "
    "Could you please rephrase? Try mentioning a specific topic — "
    'for example: "explain Python functions", "what is the OSI model?", '
    'or "when is the assignment due?".'
)


def _preprocess(text: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _tokenize(text: str) -> list:
    return [w for w in text.split() if len(w) > 1]


def _score(tokens: list, raw: str, kb_item) -> float:
    """
    Compute keyword-match confidence score for a single KB entry.

    Scoring logic:
    - Each matched keyword contributes points toward a 100-point scale
    - A single strong keyword match should always clear the threshold
    - Score = (matched_keywords / total_keywords) * 80  +  partial_bonus
    - BUT: if ANY keyword matches exactly, minimum score is 25 (always above threshold)
    """
    keywords = [k.strip().lower() for k in kb_item.keywords.split(",") if k.strip()]
    if not keywords:
        return 0.0

    exact_matches = 0
    partial_bonus = 0.0

    for kw in keywords:
        kw_tokens = kw.split()
        if len(kw_tokens) > 1:
            # Multi-word keyword — check if full phrase appears in raw text
            if kw in raw:
                exact_matches += 1
            elif any(t in kw for t in tokens):
                partial_bonus += 0.5
        else:
            if kw in tokens:
                exact_matches += 1
            elif kw in raw:
                # substring match (e.g. "loop" matching "loops")
                partial_bonus += 0.6
            elif any(t.startswith(kw) or kw.startswith(t) for t in tokens if len(t) > 2):
                partial_bonus += 0.4

    base_score = (exact_matches / len(keywords)) * 80
    bonus      = min(partial_bonus * 10, 20)
    raw_score  = base_score + bonus

    # Guarantee: any exact keyword match scores at least 25
    # This ensures a query like "explain loops" always matches loops_cpp
    if exact_matches > 0 and raw_score < 25:
        raw_score = 25.0

    return min(raw_score, 95.0)


def classify(user_input: str) -> dict:
    """
    Classify user input against the live KnowledgeBase in SQLite.

    Returns:
        {
            "response":   str | None,
            "confidence": float,
            "intent":     str | None,
            "fallback":   bool,
        }
    """
    if not user_input or not user_input.strip():
        return {"response": None, "confidence": 0.0, "intent": None, "fallback": True}

    processed  = _preprocess(user_input)
    tokens     = _tokenize(processed)
    kb_items   = KnowledgeBase.query.all()
    best_match = None
    best_score = 0.0

    for item in kb_items:
        score = _score(tokens, processed, item)
        if score > best_score:
            best_score = score
            best_match = item

    if best_score < FALLBACK_THRESHOLD or not best_match:
        return {
            "response":   None,
            "confidence": round(best_score, 1),
            "intent":     None,
            "fallback":   True,
        }

    return {
        "response":   best_match.response_text,
        "confidence": round(best_score, 1),
        "intent":     best_match.intent_name,
        "fallback":   False,
    }


def get_motivation() -> str | None:
    """
    FR-3.3: Return a random motivational message with ~13% probability.
    Fetched live from the Motivations table so lecturers can update it.
    """
    if random.random() > 0.13:
        return None
    motivations = Motivation.query.all()
    if not motivations:
        return None
    return random.choice(motivations).message
