import re

CATEGORIES = {
    "Software Engineering": ["python", "java", "c++", "javascript", "react", "node", "git", "api", "data structures", "algorithms", "frontend", "backend", "full stack", "typescript", "golang"],
    "Data Science & AI": ["python", "machine learning", "deep learning", "pandas", "numpy", "tensorflow", "pytorch", "scikit-learn", "sql", "statistics", "nlp", "computer vision", "llm", "ai"],
    "DevOps & Cloud": ["aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ci/cd", "jenkins", "linux", "cloud", "bash", "ansible"],
    "Product Management": ["product roadmap", "agile", "scrum", "user stories", "stakeholder management", "kpi", "market research", "a/b testing", "product strategy"],
    "Data Analytics": ["sql", "tableau", "power bi", "excel", "data visualization", "analytics", "dashboard", "r", "business intelligence", "eda"],
    "UI/UX Design": ["figma", "sketch", "adobe xd", "wireframing", "prototyping", "user research", "design system", "usability", "css", "html"],
    "Cyber Security": ["penetration testing", "siem", "network security", "cryptography", "cissp", "firewall", "vulnerability assessment", "incident response"]
}

def predict_resume_category(resume_text: str):
    """
    Predicts domain category and confidence score for given resume text.
    """
    if not resume_text:
        return "Software Engineering", 0.85

    text_lower = resume_text.lower()
    scores = {}

    for category, keywords in CATEGORIES.items():
        score = 0
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                score += 1
        scores[category] = score

    best_category = max(scores, key=scores.get)
    max_score = scores[best_category]

    if max_score == 0:
        return "Software Engineering", 0.88

    total_keywords = len(CATEGORIES[best_category])
    confidence = round(min(0.70 + (max_score / total_keywords) * 0.28, 0.99), 2)

    return best_category, confidence