import re

def calculate_ats_score(
    resume_text: str = "",
    skills: list = None,
    jd_text: str = "",
    confidence: float = 0.0,
    contact_info: dict = None,
    education: list = None,
    experience: list = None,
    projects: list = None,
    certifications: list = None,
    word_count: int = 300,
    match_score: int = 0
) -> dict:
    """
    Weighted ATS Scoring Engine for ResumeAI Pro.
    Calculates dynamic ATS Score out of 100 along with granular factor breakdown:
    - Contact Details: max 10
    - Skills Portfolio: max 25
    - Education Section: max 10
    - Projects Section: max 20
    - Work Experience: max 15
    - Certifications: max 10
    - Resume Formatting: max 5
    - Keyword Match Alignment: max 5
    """
    if skills is None:
        skills = []

    text_lower = resume_text.lower() if resume_text else ""

    # 1. Contact Details (Max 10)
    contact_score = 0
    if contact_info:
        if contact_info.get("email") and contact_info.get("email") != "Not Specified":
            contact_score += 5
        if contact_info.get("phone") and contact_info.get("phone") != "Not Specified":
            contact_score += 5
    else:
        contact_score = 6

    # 2. Skills Portfolio (Max 25)
    skills_score = min(len(skills) * 3, 25)

    # 3. Education Section (Max 10)
    edu_keywords = ['b.tech', 'b.e', 'bachelor', 'degree', 'university', 'college', 'institute', 'education', 'master', 'm.tech', 'b.sc', 'm.sc']
    edu_matches = sum(1 for kw in edu_keywords if kw in text_lower)
    education_score = 10 if edu_matches > 0 else 4

    # 4. Projects Section (Max 20)
    proj_keywords = ['project', 'developed', 'built', 'implemented', 'designed', 'created', 'github', 'deployed']
    proj_matches = sum(1 for kw in proj_keywords if kw in text_lower)
    projects_score = min(10 + (proj_matches * 2), 20) if proj_matches > 0 else 5

    # 5. Work Experience (Max 15)
    exp_keywords = ['experience', 'employment', 'work history', 'internship', 'developer', 'engineer', 'analyst', 'manager', 'lead']
    exp_matches = sum(1 for kw in exp_keywords if kw in text_lower)
    experience_score = min(7 + (exp_matches * 2), 15) if exp_matches > 0 else 4

    # 6. Certifications Section (Max 10)
    cert_keywords = ['certification', 'certified', 'certificate', 'coursera', 'udemy', 'nptel', 'aws certified', 'azure certified']
    cert_matches = sum(1 for kw in cert_keywords if kw in text_lower)
    certifications_score = 10 if cert_matches > 0 else 5

    # 7. Resume Formatting & Word Count (Max 5)
    if 300 <= word_count <= 1200:
        formatting_score = 5
    elif 150 <= word_count < 300 or 1200 < word_count <= 1800:
        formatting_score = 3
    else:
        formatting_score = 2

    # 8. Keyword Match Alignment (Max 5)
    if match_score > 0:
        keyword_score = min(int((match_score / 100) * 5), 5)
    else:
        keyword_score = min(max(len(skills) // 3, 2), 5)

    total_score = min(max(contact_score + skills_score + education_score + projects_score + experience_score + certifications_score + formatting_score + keyword_score, 20), 98)

    breakdown = {
        "contact_score": contact_score,
        "contact_max": 10,
        "skills_score": skills_score,
        "skills_max": 25,
        "education_score": education_score,
        "education_max": 10,
        "projects_score": projects_score,
        "projects_max": 20,
        "experience_score": experience_score,
        "experience_max": 15,
        "certifications_score": certifications_score,
        "certifications_max": 10,
        "formatting_score": formatting_score,
        "formatting_max": 5,
        "keyword_score": keyword_score,
        "keyword_max": 5,
        "total_ats": total_score
    }

    return breakdown