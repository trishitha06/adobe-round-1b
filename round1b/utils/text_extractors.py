import fitz
import re
import difflib

def is_bold(span):
    return bool(span.get("flags", 0) & 2)

def is_all_caps(text):
    return text.isupper() and 1 < len(text.split()) <= 8

def is_likely_heading(text):
    if not text:
        return False
    text = text.strip()
    if len(text) < 3 or len(text) > 150:
        return False
    if text.count(" ") > 20:
        return False
    if re.search(r"^(the|a|an|it|this|that|which|is|are|was|were)\b", text.lower()):
        return False
    if text.count('.') > 1 or text.count(',') > 1:
        return False
    if not re.search(r"[a-zA-Z]", text):
        return False
    return True

def keyword_match(text, keywords):
    text_words = text.lower().split()
    return any(
        word in text_words or difflib.get_close_matches(word, text_words, cutoff=0.8)
        for word in keywords
    )

def extract_relevant_sections(pdf_path, persona, job):
    doc = fitz.open(pdf_path)
    sections, refined = [], []
    keywords = set(re.findall(r"\b\w+\b", job.lower()))

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "").strip()
                    if not text or not is_likely_heading(text):
                        continue
                    score = 0
                    if is_bold(span): score += 1
                    if is_all_caps(text): score += 0.5
                    if keyword_match(text, keywords): score += 1.5
                    if score > 0:
                        # Refined text block (next paragraph)
                        refined_text = ""
                        for b in blocks:
                            if abs(b["bbox"][1] - span["origin"][1]) < 100 and b.get("text", "") != text:
                                refined_text = b.get("text", "").strip()
                                break
                        sections.append({"page_number": page_num, "section_title": text, "score": score})
                        refined.append({
                            "page_number": page_num,
                            "section_title": text,
                            "refined_text": refined_text or text,
                            "score": score
                        })

    sections = sorted(sections, key=lambda x: -x["score"])[:5]
    refined = sorted(refined, key=lambda x: -x["score"])[:5]
    return sections, refined