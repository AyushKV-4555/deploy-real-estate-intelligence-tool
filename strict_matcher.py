import re

# STRICT allowed AI / DS titles
ALLOWED_TITLES = [
    "ai engineer",
    "machine learning engineer",
    "ml engineer",
    "data scientist",
    "applied scientist",
    "research scientist",
    "ai applied scientist",
    "genai engineer",
]

def normalize(title: str) -> str:
    title = title.lower()
    title = re.sub(r"[^a-z0-9 ]", "", title)
    title = re.sub(r"\s+", " ", title).strip()
    return title

def is_strict_ai_role(title: str) -> bool:
    norm = normalize(title)

    # Exact or strong partial match
    for allowed in ALLOWED_TITLES:
        if norm == allowed:
            return True
        if norm.startswith(allowed):
            return True
        if allowed in norm and len(norm.split()) <= len(allowed.split()) + 1:
            return True

    return False
