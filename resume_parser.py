import re
import fitz  # PyMuPDF
import spacy
import nltk

# Download necessary NLTK data
nltk.download('punkt')

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# ---------------------------- Extract Name ----------------------------

def extract_name(doc, text):
    lines = text.strip().split('\n')
    for line in lines:
        line = line.strip()
        words = line.split()
        if 1 < len(words) <= 4 and all(word.istitle() for word in words):
            return line
    name_candidates = [ent.text.strip() for ent in doc.ents if ent.label_ == "PERSON"]
    top_lines = lines[:10]
    for candidate in name_candidates:
        for line in top_lines:
            if candidate in line:
                if not re.search(r'curriculum vitae|resume|cv', candidate, re.I):
                    return candidate
    return ""

# ---------------------------- Extract Email ----------------------------

def extract_email(text):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    matches = re.findall(email_regex, text)
    return matches[0] if matches else ""

# ---------------------------- Extract Phone ----------------------------

def extract_contact_number(text):
    pattern = r'\b(?:\+?\d{1,3}[\s\-\.]?)?(?:\(?\d{2,4}\)?[\s\-\.]?)?\d{3,4}[\s\-\.]?\d{4}\b'
    match = re.search(pattern, text)
    return match.group() if match else ""

# ---------------------------- PDF Text Extraction ----------------------------

def extract_resume_info_from_pdf(uploaded_file_bytes):
    if not isinstance(uploaded_file_bytes, (bytes, bytearray)):
        raise TypeError("Uploaded file must be bytes-like for PDF parsing.")
    pdf = fitz.open(stream=uploaded_file_bytes, filetype="pdf")
    text = ""
    for page in pdf:
        text += page.get_text()
    spacy_doc = nlp(text)
    return spacy_doc, text

# ---------------------------- Resume Info as Dictionary ----------------------------

def extract_resume_info(doc, text):
    return {
        'name': extract_name(doc, text),
        'email': extract_email(text),
        'phone': extract_contact_number(text),
    }

# ---------------------------- Skills Extraction ----------------------------

def extract_skills(text, skill_keywords):
    lower_text = text.lower()
    return list(set(skill for skill in skill_keywords if skill.lower() in lower_text))

# ---------------------------- Resume Scoring ----------------------------

def calculate_resume_score(info, skills_found, skill_keywords=None):
    score = 0
    if info.get("name"): score += 10
    if info.get("email"): score += 10
    if info.get("phone"): score += 10
    score += min(70, len(skills_found) * 10)
    return score

# ---------------------------- Skill Suggestions ----------------------------

def suggest_skills_for_job(job_title):
    skills = {
        "data scientist": ["Python", "SQL", "Machine Learning", "Data Analysis", "Deep Learning", "AI"],
        "web developer": ["HTML", "CSS", "JavaScript", "React", "Node.js", "SQL"],
        "data analyst": ["Excel", "SQL", "Python", "R", "Power BI", "Data Visualization"],
        "developer":[ "Python", "Java","Data Structures and Algorithms","Git & GitHub","SQL","HTML/CSS/JavaScript",
        "RESTful APIs","Object-Oriented Programming (OOP)","Debugging and Testing","Agile and SDLC Knowledge"],
        "Business Analyst": ["Data Analysis","SQL","Communication Skills","Microsoft Excel","Business Intelligence Tools "],
        "Human Resources": ["Recruitment","Employee Relations","HR Software (e.g., SAP, Workday)","Onboarding & Training",
        "Compliance Knowledge"],
        "Marketing": ["Digital Marketing","SEO/SEM","Content Creation","Data Analytics","Social Media Management"],
        "Sales Executive": ["Customer Relationship Management","Negotiation","Lead Generation", "CRM Software (e.g., Salesforce)",
        "Communication & Persuasion"]

    }
    return skills.get(job_title.lower(), [])

# ---------------------------- Load Required Skills (Optional Utility) ----------------------------

def load_required_skills():
    return ['python', 'sql', 'machine learning']

# ---------------------------- Fix: Missing Function (for Recruiter, Admin, etc.) ----------------------------

def extract_candidate_info(uploaded_file_bytes):
    doc, text = extract_resume_info_from_pdf(uploaded_file_bytes)
    info = extract_resume_info(doc, text)
    return info, text, doc
