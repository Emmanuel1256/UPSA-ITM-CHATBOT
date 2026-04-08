# ═══════════════════════════════════════════════════════════
# server/services/nlp_service.py  — v2
# NLP Intent Classification Engine
#
# Upgrades over v1:
#   • Level-aware classification  (100 sees L100, 200 sees L100+200, etc.)
#   • Typo auto-correction        (poniter → pointer)
#   • Synonym expansion           ("show me", "tell me" → explain)
#   • Phrase boosting             (multi-word matches score higher)
#   • Level-gate message          (topic exists but above student level)
#   • Structured fallback         (shows relevant suggestions per level)
#   • Topic listing               ("what topics can I ask about?")
#
# FR-2.1 Intent Recognition | FR-2.2 Level Filtering
# FR-2.3 Fallback Mechanism  | FR-2.4 Spell Tolerance
# ═══════════════════════════════════════════════════════════

import re
import random

from server.models.models import KnowledgeBase, Motivation

FALLBACK_THRESHOLD = 15.0

# ── Synonym map ──────────────────────────────────────────────
SYNONYM_MAP = {
    "what is":                "explain",
    "what are":               "explain",
    "how does":               "explain",
    "how do":                 "explain",
    "how to":                 "explain",
    "can you explain":        "explain",
    "tell me about":          "explain",
    "show me":                "explain",
    "teach me":               "explain",
    "define":                 "explain",
    "definition of":          "explain",
    "meaning of":             "explain",
    "give me":                "explain",
    "help me with":           "explain",
    "i need help with":       "explain",
    "i dont understand":      "explain",
    "i don't understand":     "explain",
    "c plus plus":            "c++",
    "cplusplus":              "c++",
    "cpp":                    "c++",
    "oop":                    "object oriented",
    "object oriented programming": "object oriented",
    "stl":                    "standard template library",
    "func":                   "function",
    "arr":                    "array",
    "str":                    "string",
    "ptr":                    "pointer",
    "ref":                    "reference",
    "inherit":                "inheritance",
    "polymorphic":            "polymorphism",
    "overload":               "overloading",
    "templ":                  "template",
    "except":                 "exception",
    "heap":                   "dynamic memory",
    "smart ptr":              "smart pointers",
    "unique ptr":             "smart pointers",
    "shared ptr":             "smart pointers",
    "linked list":            "data structures",
    "binary tree":            "data structures",
    "hash map":               "stl",
    "hash table":             "data structures",
    "thread":                 "multithreading",
    "concurrent":             "multithreading",
    "parallel":               "multithreading",
    "singleton":              "design patterns",
    "factory":                "design patterns",
    "observer":               "design patterns",
}

# ── Typo corrections ─────────────────────────────────────────
TYPO_MAP = {
    "varialbe":       "variable",   "varibale":    "variable",
    "varibles":       "variables",  "variabl":     "variable",
    "fuction":        "function",   "funtion":     "function",
    "functoin":       "function",   "fucntion":    "function",
    "poniter":        "pointer",    "pionter":     "pointer",
    "pinter":         "pointer",    "pointr":      "pointer",
    "inhertiance":    "inheritance","inheritence": "inheritance",
    "inheratance":    "inheritance","polymorph":   "polymorphism",
    "polymorphisim":  "polymorphism","constructur": "constructor",
    "constructer":    "constructor","exeption":    "exception",
    "excpetion":      "exception",  "tempalte":    "template",
    "templte":        "template",   "arraay":      "array",
    "arry":           "array",      "stirng":      "string",
    "srting":         "string",     "lop":         "loop",
    "looop":          "loop",       "whle":        "while",
    "conditon":       "condition",  "operater":    "operator",
    "oprator":        "operator",   "decalre":     "declare",
    "decleration":    "declaration","complie":     "compile",
    "complier":       "compiler",   "syntex":      "syntax",
    "sytax":          "syntax",     "bolean":      "boolean",
    "boolen":         "boolean",    "interger":    "integer",
    "integr":         "integer",    "recurion":    "recursion",
    "referance":      "reference",  "refernce":    "reference",
    "dyamic":         "dynamic",    "dynmic":      "dynamic",
    "allocaton":      "allocation", "allcoation":  "allocation",
    "multithreding":  "multithreading",
    "muiltithreading":"multithreading",
}

# ── Topics per level (for suggestions) ───────────────────────
LEVEL_TOPICS = {
    "100": [
        "what is C++", "variables and data types", "input and output (cin/cout)",
        "operators", "if/else statements", "loops", "functions", "arrays", "strings",
    ],
    "200": [
        "pointers", "references", "classes and objects", "constructors and destructors",
        "inheritance", "polymorphism", "file handling", "dynamic memory allocation",
    ],
    "300": [
        "templates", "the STL (vectors, maps, sets)", "exception handling",
        "smart pointers", "multithreading", "design patterns", "data structures",
    ],
}


# ════════════════════════════════════════════════════════════
# TEXT PROCESSING
# ════════════════════════════════════════════════════════════

def _correct_typos(text: str) -> str:
    for typo, correct in TYPO_MAP.items():
        text = re.sub(r"\b" + re.escape(typo) + r"\b", correct, text)
    return text


def _expand_synonyms(text: str) -> str:
    for phrase, canonical in SYNONYM_MAP.items():
        text = text.replace(phrase, canonical)
    return text


def _preprocess(text: str) -> str:
    text = text.lower()
    text = _correct_typos(text)
    text = _expand_synonyms(text)
    text = re.sub(r"[^\w\s\+]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _tokenize(text: str) -> list:
    return [w for w in text.split() if len(w) > 1]


# ════════════════════════════════════════════════════════════
# SCORING
# ════════════════════════════════════════════════════════════

def _score(tokens: list, raw: str, kb_item) -> float:
    keywords = [k.strip().lower() for k in kb_item.keywords.split(",") if k.strip()]
    if not keywords:
        return 0.0

    exact_matches  = 0
    partial_bonus  = 0.0
    phrase_matches = 0

    for kw in keywords:
        kw_clean  = _preprocess(kw)
        kw_tokens = kw_clean.split()

        if len(kw_tokens) > 1:
            if kw_clean in raw:
                phrase_matches += 1
                exact_matches  += 1
            elif any(t in kw_clean for t in tokens):
                partial_bonus += 0.6
        else:
            if kw_clean in tokens:
                exact_matches += 1
            elif kw_clean in raw:
                partial_bonus += 0.6
            elif any(t.startswith(kw_clean) or kw_clean.startswith(t)
                     for t in tokens if len(t) > 2):
                partial_bonus += 0.4

    base_score   = (exact_matches / len(keywords)) * 80
    bonus        = min(partial_bonus * 10, 20)
    phrase_boost = phrase_matches * 15
    raw_score    = base_score + bonus + phrase_boost

    if exact_matches > 0 and raw_score < 25:
        raw_score = 25.0

    return min(raw_score, 98.0)


# ════════════════════════════════════════════════════════════
# LEVEL HELPERS
# ════════════════════════════════════════════════════════════

def _levels_accessible(student_level: str) -> list:
    """Level 100 → [100, all], Level 200 → [100, 200, all], etc."""
    order = ["100", "200", "300"]
    try:
        idx = order.index(str(student_level))
        return order[:idx + 1] + ["all"]
    except ValueError:
        return ["100", "all"]


def _level_gate_response(matched_level: str, student_level: str) -> str:
    label_map  = {"200": "Intermediate (Level 200)", "300": "Advanced (Level 300)"}
    label      = label_map.get(str(matched_level), f"Level {matched_level}")
    suggestions = LEVEL_TOPICS.get(str(student_level), LEVEL_TOPICS["100"])
    tip_list   = "\n".join(f"• *\"{t}\"*" for t in suggestions[:5])
    return (
        f"That topic belongs to the **{label}** C++ curriculum — "
        f"it's a bit ahead of Level {student_level} for now. "
        f"Keep studying and you'll get there soon! 💪\n\n"
        f"**Topics perfect for your level right now:**\n{tip_list}\n\n"
        f"Try asking about any of these!"
    )


def _topics_response(student_level: str) -> str:
    accessible = _levels_accessible(student_level)
    label_map  = {"100": "🟢 Fundamentals", "200": "🟡 Intermediate", "300": "🔴 Advanced"}
    lines      = ["📚 **Here are all the C++ topics you can ask me about:**\n"]
    for lvl in ["100", "200", "300"]:
        if lvl not in accessible:
            continue
        lines.append(f"**{label_map[lvl]} — Level {lvl}**")
        for t in LEVEL_TOPICS.get(lvl, []):
            lines.append(f"  • {t}")
        lines.append("")
    lines.append("Just ask naturally — e.g. *\"explain pointers\"* or *\"how do loops work?\"*")
    return "\n".join(lines)


# ════════════════════════════════════════════════════════════
# MAIN CLASSIFIER
# ════════════════════════════════════════════════════════════

def classify(user_input: str, student_level: str = "100") -> dict:
    """
    Classify user input against the live KnowledgeBase.

    Returns dict with keys:
        response, confidence, intent, fallback, corrected
    """
    if not user_input or not user_input.strip():
        return {
            "response": None, "confidence": 0.0,
            "intent": None,   "fallback": True, "corrected": None,
        }

    original  = user_input.strip()
    processed = _preprocess(original)
    tokens    = _tokenize(processed)
    corrected = processed if processed.lower() != original.lower() else None

    # ── Topic listing intent ───────────────────────────────
    topic_triggers = [
        "what topics", "what can i ask", "what can you teach",
        "list topics", "available topics", "what do you know",
        "what subjects", "help topics", "show topics",
        "what questions", "topics available",
    ]
    if any(t in processed for t in topic_triggers):
        return {
            "response":   _topics_response(student_level),
            "confidence": 99.0,
            "intent":     "list_topics",
            "fallback":   False,
            "corrected":  corrected,
        }

    # ── Score all KB entries ───────────────────────────────
    kb_items          = KnowledgeBase.query.all()
    accessible_levels = _levels_accessible(student_level)
    best_match        = None
    best_score        = 0.0
    best_any          = None
    best_any_score    = 0.0

    for item in kb_items:
        score      = _score(tokens, processed, item)
        item_level = str(item.level) if item.level else "all"

        if score > best_any_score:
            best_any_score = score
            best_any       = item

        if item_level in accessible_levels:
            if score > best_score:
                best_score = score
                best_match = item

    # ── Below threshold ────────────────────────────────────
    if best_score < FALLBACK_THRESHOLD:
        # Topic exists but at a higher level?
        if best_any_score >= FALLBACK_THRESHOLD and best_any and best_any != best_match:
            return {
                "response":   _level_gate_response(best_any.level, student_level),
                "confidence": round(best_any_score, 1),
                "intent":     "level_gate",
                "fallback":   False,
                "corrected":  corrected,
            }

        # Pure fallback with curated suggestions
        suggestions = LEVEL_TOPICS.get(str(student_level), LEVEL_TOPICS["100"])
        sample      = random.sample(suggestions, min(4, len(suggestions)))
        tip_list    = "\n".join(f"• *\"{t}\"*" for t in sample)

        return {
            "response": (
                "I couldn't find a confident match for that. "
                "Here are some topics you can ask me about right now:\n\n"
                f"{tip_list}\n\n"
                "You can also ask: **\"what topics can I learn about?\"** "
                "to see the full list."
            ),
            "confidence": round(best_score, 1),
            "intent":     None,
            "fallback":   True,
            "corrected":  corrected,
        }

    # ── Successful match ───────────────────────────────────
    return {
        "response":   best_match.response_text,
        "confidence": round(best_score, 1),
        "intent":     best_match.intent_name,
        "fallback":   False,
        "corrected":  corrected,
    }


# ════════════════════════════════════════════════════════════
# MOTIVATIONAL MESSAGE
# ════════════════════════════════════════════════════════════

def get_motivation() -> str | None:
    """FR-3.3: Return a random motivational message (~13% probability)."""
    if random.random() > 0.13:
        return None
    motivations = Motivation.query.all()
    if not motivations:
        return None
    return random.choice(motivations).message
