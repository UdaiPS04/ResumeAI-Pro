def generate_feedback(skills, ats_score, missing):

    feedback = []

    # Overall Feedback
    if ats_score >= 80:
        feedback.append("Excellent resume. It is well optimized.")

    elif ats_score >= 60:
        feedback.append("Good resume but there is room for improvement.")

    else:
        feedback.append("Resume needs significant improvement.")

    # Skill Suggestions
    if "python" not in skills:
        feedback.append("Add Python if you have experience.")

    if "sql" not in skills:
        feedback.append("Mention SQL projects.")

    if "github" not in skills:
        feedback.append("Include your GitHub profile.")

    if "docker" in missing:
        feedback.append("Docker is required for this job.")

    if "aws" in missing:
        feedback.append("AWS knowledge will improve your chances.")

    if "git" not in skills:
        feedback.append("Mention Git version control.")

    return feedback