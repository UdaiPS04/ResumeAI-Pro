import re
from flask_app.utils.utils import extract_skills

def match_resume_with_jd(resume_text: str, jd_text: str):
    """
    Compares resume text against job description text and returns match score, matching skills, and missing skills.
    """
    if not jd_text or not jd_text.strip():
        jd_skills = ["Python", "SQL", "Machine Learning", "System Design", "AWS", "Docker", "Git"]
    else:
        jd_skills = extract_skills(jd_text)
        if not jd_skills:
            words = re.findall(r'\b[A-Za-z]{3,}\b', jd_text)
            jd_skills = list(set([w.capitalize() for w in words if w.lower() in ["python", "sql", "excel", "tableau", "power bi", "java", "react", "aws", "docker", "agile"]]))
            if not jd_skills:
                jd_skills = ["Python", "SQL", "Data Analysis", "Communication"]

    resume_skills = extract_skills(resume_text)

    matching_skills = sorted(list(set(resume_skills).intersection(set(jd_skills))))
    missing_skills = sorted(list(set(jd_skills) - set(resume_skills)))

    if len(jd_skills) > 0:
        match_score = int((len(matching_skills) / len(jd_skills)) * 100)
    else:
        match_score = 80

    match_score = min(max(match_score, 40), 96)

    return match_score, matching_skills, missing_skills