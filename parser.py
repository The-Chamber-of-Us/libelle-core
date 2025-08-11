import re
from typing import List, Dict


# -------------------------
# 1. Basic Information Parsers
# -------------------------

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


# -------------------------
# 2. Section: Skills
# -------------------------

def extract_skills(text: str) -> List[str]:
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    skills_lines = []
    in_skills_section = False

    for line in lines:
        if re.match(r'^\s*(SKILLS)\s*$', line, re.IGNORECASE):
            in_skills_section = True
            continue
        elif in_skills_section and re.match(r'^[A-Z\s&]+$', line) and len(line) < 50:
            break
        elif in_skills_section:
            skills_lines.append(line)

    combined_skills = " ".join(skills_lines)
    skills = re.split(r'•|,|·|;', combined_skills)
    return [skill.strip() for skill in skills if skill.strip()]


# -------------------------
# 3. Section: Education
# -------------------------

def extract_education(text: str) -> List[str]:
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    education_lines = []
    in_education_section = False

    for line in lines:
        if re.match(r'^(education(\s*&\s*certificate)?|education & certification)$', line.strip(), re.IGNORECASE):
            in_education_section = True
            continue

        elif in_education_section and re.match(r'^[A-Z\s&]+$', line.strip()) and len(line.strip()) < 50:
            break

        elif in_education_section:
            education_lines.append(line)

    return [line for line in education_lines if line.strip()]


# -------------------------
# 4. Section Parsing Utilities
# -------------------------

def _get_lines(text: str) -> List[str]:
    return [line.rstrip() for line in text.splitlines()]


def _is_section_header(line: str) -> bool:
    if not line or len(line.strip()) == 0:
        return False
    s = line.strip()
    headers = [
        r'^(summary|objective|contact|education|certifi|certificate|skills|work experience|work|experience|employment|projects|project experience|project|research|publications|awards|volunteer|honors|activities)$'
    ]
    if re.match(headers[0], s.lower()):
        return True
    if s == s.upper() and len(s) < 60 and ' ' in s:
        return True
    return False


def _collect_section_lines(lines: List[str], start_patterns: List[str], stop_when_header: bool = True):
    """
    Returns a tuple: (section_lines, end_index)
    """
    start_re = re.compile(r'|'.join([f'({p})' for p in start_patterns]), re.IGNORECASE)
    collected = []
    capturing = False
    end_index = len(lines)

    for i, line in enumerate(lines):
        if not capturing and start_re.search(line or ""):
            capturing = True
            continue
        if capturing:
            if stop_when_header and _is_section_header(line.strip()):
                end_index = i
                break
            collected.append(line)

    return collected, end_index



def _group_into_entries(section_lines: List[str]) -> List[str]:
    entries = []
    current = []

    def flush_current():
        if current:
            text = " ".join([ln.strip() for ln in current if ln.strip()])
            text = re.sub(r'\s+', ' ', text).strip()
            if text:
                entries.append(text)
            current.clear()

    date_like = re.compile(r'\b(?:\d{4}|\d{4}\s*-\s*\d{4}|Present|present|\bJan(?:uary)?|\bFeb(?:ruary)?|\bMar(?:ch)?|'
                           r'\bApr(?:il)?|\bMay\b|\bJun(?:e)?|\bJul(?:y)?|\bAug(?:ust)?|\bSep(?:t(?:ember)?)?|'
                           r'\bOct(?:ober)?|\bNov(?:ember)?|\bDec(?:ember)?)', re.IGNORECASE)

    for line in section_lines:
        stripped = line.strip()
        if not stripped:
            flush_current()
            continue

        if stripped.startswith(('•', '-', '—')):
            flush_current()
            current.append(re.sub(r'^[•\-\—]\s*', '', stripped))
            continue

        if (date_like.search(stripped) and len(current) > 0) and len(current[-1].strip()) > 0:
            current.append(stripped)
            continue

        if re.search(r'\|', stripped) and date_like.search(stripped):
            flush_current()
            current.append(stripped)
            continue

        if re.match(r'^[A-Z][\w&\.\-]+', stripped) and date_like.search(stripped) and not current:
            current.append(stripped)
            continue

        current.append(stripped)

    flush_current()
    return entries


# -------------------------
# 5. Experience Sections
# -------------------------

def extract_work_experience(text: str):
    lines = _get_lines(text)
    work_start_patterns = [r'work experience', r'experience', r'employment']
    work_lines, work_end = _collect_section_lines(lines, work_start_patterns)
    return _group_into_entries(work_lines), work_end

def extract_project_experience(text: str, start_index: int):
    lines = _get_lines(text)
    lines = lines[start_index:] 
    project_start_patterns = [r'project experience', r'projects', r'project']
    project_lines, _ = _collect_section_lines(lines, project_start_patterns)
    return _group_into_entries(project_lines)


# -------------------------
# 6. Main Parser
# -------------------------

def parse_resume(text: str) -> Dict[str, any]:
    work_experience, work_end_index = extract_work_experience(text)
    project_experience = extract_project_experience(text, work_end_index)

    return {
        "name": extract_name(text),
        "emails": extract_email(text),
        "phones": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "work_experience": work_experience,
        "project_experience": project_experience
    }
