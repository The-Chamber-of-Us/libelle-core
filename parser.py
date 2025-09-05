import re
from typing import List, Dict

SKILL_KEYWORDS = ["python", "java", "sql", "machine learning", "aws", "excel"]

def extract_email(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)

def extract_phone(text: str) -> List[str]:
    pattern = r"(\+?\d[\d\s().-]{8,}\d)"
    raw_matches = re.findall(pattern, text)
    
    cleaned = []
    for number in raw_matches:
        digits = re.sub(r"[^\d]", "", number)
        if 9 <= len(digits) <= 15:
            cleaned.append(digits)
    
    return cleaned

def extract_name(text: str) -> str:
    for line in text.splitlines():
        if not line.strip() or re.search(r'\d|\@', line):
            continue
        words = line.strip().split()
        if 2 <= len(words) <= 4:
            return line.strip()
    return "Name Not Found"

def extract_skills(text: str) -> List[str]:
    text_lower = text.lower()
    return [skill for skill in SKILL_KEYWORDS if skill in text_lower]

def extract_education(text: str) -> List[str]:
    deg_pattern = r"(Bachelor|Master|Ph\.?D\.?|B\.Sc\.|M\.Sc\.).*"
    return re.findall(deg_pattern, text, re.IGNORECASE)

def extract_experience(text: str) -> List[str]:
    lines = text.splitlines()
    exp_section = []
    capture = False
    for line in lines:
        if re.search(r"experience", line, re.IGNORECASE):
            capture = True
            continue
        if capture:
            if re.match(r"^\s*[A-Z][A-Za-z\s]+:$", line):  # e.g., "Skills:"
                break
            if line.strip():
                exp_section.append(line.strip())
    return exp_section

def parse_resume(text: str) -> Dict[str, any]:
    return {
        "name": extract_name(text),
        "emails": extract_email(text),
        "phones": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text)
    }
