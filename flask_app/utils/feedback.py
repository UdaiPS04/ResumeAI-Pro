def generate_feedback(skills: list, ats_score: int) -> list:
    """
    Generates tailored feedback recommendations based on ATS score and detected skills.
    """
    recommendations = []

    if ats_score < 70:
        recommendations.append("Formatting Notice: Ensure your resume uses standard section headings (e.g. 'Experience', 'Education', 'Skills') to ensure seamless ATS parsing.")
        recommendations.append("Quantify Achievements: Add measurable outcome metrics (e.g. 'Increased efficiency by 35%', 'Managed a team of 8') to strengthen experience impact.")
    else:
        recommendations.append("Strong Structural Integrity: Your document formatting aligns well with major Applicant Tracking Systems (Workday, Greenhouse, Lever).")

    if len(skills) < 6:
        recommendations.append("Expand Tech Stack Keywords: Consider adding missing framework keywords or tools relevant to target job roles to improve search indexing.")
    else:
        recommendations.append("Rich Skill Coverage: Detected a solid technical vocabulary. Ensure these skills are mapped to concrete project outcomes in your bullet points.")

    recommendations.append("Tailor for Target Job: Align bullet points with specific keywords found in target Job Descriptions to maximize ATS keyword matching density.")
    recommendations.append("File Format Recommendation: Keep your resume saved as clean PDF or DOCX without tables, images, or header text boxes that ATS parsers might bypass.")

    return recommendations