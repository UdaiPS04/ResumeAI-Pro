from flask_app.utils.utils import extract_skills, COMMON_SKILLS

def categorize_skills(skills: list) -> dict:
    """
    Categorizes extracted candidate skills into Technical, Cloud/DevOps, Data/AI, and Soft Skills.
    """
    categories = {
        "Technical": [],
        "Cloud & DevOps": [],
        "Data & AI": [],
        "Soft Skills": []
    }

    cloud_keywords = {"AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "CI/CD", "Git", "GitHub", "Linux", "Bash", "Microservices"}
    data_keywords = {"Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Scikit-Learn", "Pandas", "NumPy", "OpenCV", "NLP", "LLM", "Data Analysis", "Tableau", "Power BI", "SQL", "Excel"}
    soft_keywords = {"Communication", "Project Management", "Time Management", "Critical Thinking", "Problem Solving", "Team Leadership", "Agile", "Scrum"}

    for skill in skills:
        if skill in cloud_keywords:
            categories["Cloud & DevOps"].append(skill)
        elif skill in data_keywords:
            categories["Data & AI"].append(skill)
        elif skill in soft_keywords:
            categories["Soft Skills"].append(skill)
        else:
            categories["Technical"].append(skill)

    return categories