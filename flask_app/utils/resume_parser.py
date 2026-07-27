import os
import re
from pathlib import Path

def extract_text(file) -> str:
    """
    Extracts text from PDF, DOCX, or plain text uploaded files.
    """
    if file is None:
        return ""

    filename = getattr(file, 'filename', None) or getattr(file, 'name', '') or str(file)
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ""
    text = ""

    if ext == "pdf":
        try:
            import pypdf
            reader = pypdf.PdfReader(file)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        except Exception:
            try:
                import PyPDF2
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
            except Exception:
                try:
                    if hasattr(file, 'read'):
                        file.seek(0)
                        text = file.read().decode('utf-8', errors='ignore')
                except Exception:
                    pass

    elif ext in ["docx", "doc"]:
        try:
            import docx
            doc = docx.Document(file)
            text = "\n".join([para.text for para in doc.paragraphs if para.text])
        except Exception:
            try:
                if hasattr(file, 'read'):
                    file.seek(0)
                    text = file.read().decode('utf-8', errors='ignore')
            except Exception:
                pass

    else:
        try:
            if hasattr(file, 'read'):
                file.seek(0)
                text = file.read().decode('utf-8', errors='ignore')
            elif isinstance(file, (str, Path)) and os.path.exists(file):
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
        except Exception:
            text = str(file)

    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_candidate_contact(text: str) -> dict:
    """
    Advanced regex & NLP extraction for Email, Phone, LinkedIn, GitHub, and Candidate Name.
    """
    if not text:
        return {
            "name": "Candidate",
            "email": "Not Specified",
            "phone": "Not Specified",
            "linkedin": "Not Specified",
            "github": "Not Specified"
        }

    # 1. Email Extraction (abc@gmail.com, firstname.lastname@company.co.in)
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    email = emails[0] if emails else "Not Specified"

    # 2. Phone Extraction (Supports Indian 10-digit formats & +91 prefix)
    phone_pattern = r'(?:\+?91[\s-]?)?[6-9]\d{9}\b'
    phones = re.findall(phone_pattern, text)
    phone = phones[0] if phones else "Not Specified"

    # 3. LinkedIn Extraction
    linkedin_pattern = r'(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+/?'
    linkedins = re.findall(linkedin_pattern, text, re.IGNORECASE)
    linkedin = linkedins[0] if linkedins else "Not Specified"

    # 4. GitHub Extraction
    github_pattern = r'(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9_-]+/?'
    githubs = re.findall(github_pattern, text, re.IGNORECASE)
    github = githubs[0] if githubs else "Not Specified"

    # 5. Candidate Name Extraction
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    invalid_headers = {"resume", "curriculum vitae", "cv", "profile", "summary", "contact", "experience", "education", "skills", "projects"}
    name = "Candidate"

    for line in lines[:5]:
        clean_line = re.sub(r'[^a-zA-Z\s]', '', line).strip()
        words = clean_line.split()
        if 1 <= len(words) <= 4 and clean_line.lower() not in invalid_headers:
            if all(w[0].isupper() for w in words if w):
                name = clean_line
                break

    if name == "Candidate":
        try:
            import spacy
            nlp = spacy.load("en_core_web_sm")
            doc = nlp(text[:500])
            for ent in doc.ents:
                if ent.label_ == "PERSON" and len(ent.text.split()) <= 4:
                    name = ent.text.strip()
                    break
        except Exception:
            pass

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "linkedin": linkedin,
        "github": github
    }