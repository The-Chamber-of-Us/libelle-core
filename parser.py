from nameparser import HumanName
from names_dataset import NameDataset
import re
from typing import List, Dict

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

nd = NameDataset()

def extract_name(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    stop_headers = [
        "education", "work", "experience", "employment", "projects",
        "skills", "summary", "objective", "volunteer", "leadership"
    ]

    for line in lines:
        if any(h in line.lower() for h in stop_headers):
            break

        line_no_email = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "", line).strip()
        if not line_no_email:
            continue

        line_no_contact = re.sub(r"\+?\d[\d\s().-]{8,}\d", "", line_no_email).strip()
        if not line_no_contact:
            continue

        if line_no_contact.isupper() and 2 <= len(line_no_contact.split()) <= 4:
            candidate = HumanName(line_no_contact.title())
            if candidate.first and candidate.last:
                return str(candidate)

        tokens = re.findall(r"[A-Za-z]+", line_no_contact)
        if len(tokens) >= 2:
            first, last = tokens[0], tokens[1]
            if nd.search_first_name(first.capitalize()) and nd.search_last_name(last.capitalize()):
                candidate = HumanName(" ".join(tokens[:3]))
                return str(candidate)

    for line in lines[:3]:
        if any(h in line.lower() for h in stop_headers):
            break
        candidate = HumanName(line)
        if candidate.first and candidate.last:
            return str(candidate)

    return "Name Not Found"

def extract_location(text: str) -> List[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    candidate_lines = []
    
    for line in lines[:5]:
        if re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", line):
            continue
        if re.search(r"\+?\d[\d\s().-]{8,}\d", line):
            continue
        candidate_lines.append(line)
    
    locations = []
    pattern_city_first = re.compile(r'\b([A-Z][a-zA-Z]+(?: [A-Z][a-zA-Z]+)*),\s*([A-Z]{2})(?:,\s*(\d{5}))?\b')
    pattern_state_first = re.compile(r'\b([A-Z]{2}),\s*([A-Z][a-zA-Z]+(?: [A-Z][a-zA-Z]+)*)(?:,\s*(\d{5}))?\b')
    
    for line in candidate_lines:
        match = pattern_city_first.search(line)
        if match:
            city, state, zip_code = match.groups()
            loc = f"{city}, {state}"
            if zip_code:
                loc += f", {zip_code}"
            locations.append(loc)
            return locations 
        
        match = pattern_state_first.search(line)
        if match:
            state, city, zip_code = match.groups()
            loc = f"{city}, {state}"
            if zip_code:
                loc += f", {zip_code}"
            locations.append(loc)
            return locations 
    
    return locations


def extract_skills(text: str) -> List[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    skills_lines = []
    in_skills_section = False

    for line in lines:
        if re.search(r'\bskills\b', line, re.IGNORECASE):
            in_skills_section = True
            continue
        elif in_skills_section and re.match(r'^[A-Z][A-Z\s&]+$', line) and len(line) < 50:
            break
        elif in_skills_section:
            skills_lines.append(line)

    skills = []
    for line in skills_lines:
        parts = re.split(r'•|,|·|;', line)
        for part in parts:
            clean_part = part.strip()
            if clean_part:
                skills.append(clean_part)

    return skills


def extract_education(text: str) -> List[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    education_lines = []
    in_education_section = False

    for line in lines:
        if re.search(r'\beducation\b', line, re.IGNORECASE):
            in_education_section = True
            continue
        elif in_education_section and re.match(r'^[A-Z][A-Z\s&]+$', line) and len(line) < 50:
            break
        elif in_education_section:
            education_lines.append(line)

    return [line for line in education_lines if line.strip()]


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


def parse_resume(text: str) -> Dict[str, any]:
    work_experience, work_end_index = extract_work_experience(text)
    project_experience = extract_project_experience(text, work_end_index)

    return {
        "name": extract_name(text),
        "emails": extract_email(text),
        "phones": extract_phone(text),
        "locations": extract_location(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "work_experience": work_experience,
        "project_experience": project_experience
    }
