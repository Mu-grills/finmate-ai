import os
import re
from typing import List, Tuple

KB_DIR = "knowledge_base"

def _read_all_md() -> str:
    parts = []
    for name in sorted(os.listdir(KB_DIR)):
        if name.endswith(".md"):
            with open(os.path.join(KB_DIR, name), "r", encoding="utf-8") as f:
                parts.append(f"\n\n### Fonte: {name}\n" + f.read())
    return "\n".join(parts)

def _chunk_text(text: str, max_chars: int = 900) -> List[str]:
    # quebra por blocos, mantendo trechos “mastigáveis”
    chunks, buf = [], ""
    for para in text.split("\n\n"):
        para = para.strip()
        if not para:
            continue
        if len(buf) + len(para) + 2 <= max_chars:
            buf = (buf + "\n\n" + para).strip()
        else:
            if buf:
                chunks.append(buf)
            buf = para
    if buf:
        chunks.append(buf)
    return chunks

def _tokenize(s: str) -> List[str]:
    s = s.lower()
    s = re.sub(r"[^a-zà-ú0-9\s]", " ", s)
    return [t for t in s.split() if len(t) >= 3]

def retrieve_context(query: str, top_k: int = 3) -> Tuple[str, List[Tuple[int, str]]]:
    """
    Retorna um contexto (string) com os top_k trechos mais relevantes,
    e também uma lista (score, chunk) para depuração.
    """
    raw = _read_all_md()
    chunks = _chunk_text(raw)
    q_tokens = set(_tokenize(query))

    scored = []
    for ch in chunks:
        c_tokens = _tokenize(ch)
        score = sum(1 for t in c_tokens if t in q_tokens)
        if score > 0:
            scored.append((score, ch))

    scored.sort(key=lambda x: x[0], reverse=True)
    best = scored[:top_k]

    context = "\n\n---\n\n".join([c for _, c in best]) if best else ""
    return context, best
