import os
import pdfplumber
import joblib

from flask import Flask, render_template, request

from utils import (
    clean_text,
    extract_skills,
    match_resume_to_jd,
    missing_skills
)

from feedback import generate_feedback
from report import create_report

app = Flask(__name__)

# -----------------------------
# Load Model and Vectorizer
# -----------------------------
model = joblib.load("model/resume_classifier.pkl")
vectorizer = joblib.load("model/tfidf_vectorizer.pkl")

# -----------------------------
# Upload Folder
# -----------------------------
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -----------------------------
# Extract Text from PDF
# -----------------------------
def extract_text(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + " "

    return text


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Upload Resume
# -----------------------------
@app.route("/upload", methods=["POST"])
def upload():

    # Check whether file is uploaded
    if "resume" not in request.files:
        return "No Resume Uploaded"

    file = request.files["resume"]

    if file.filename == "":
        return "Please Select a PDF File"

    # Save uploaded PDF
    save_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(save_path)

    # Get Job Description
    job_description = request.form.get(
        "job_description",
        ""
    )

    # Extract Resume Text
    text = extract_text(save_path)

    # Clean Resume
    cleaned_text = clean_text(text)

    # Convert to TF-IDF
    vector = vectorizer.transform([cleaned_text])

    # Predict Category
    prediction = model.predict(vector)[0]

    # Extract Resume Skills
    skills = extract_skills(text)

    # Resume vs Job Description Matching
    matched = match_resume_to_jd(
        skills,
        job_description
    )

    missing = missing_skills(
        job_description,
        skills
    )

    # Match Percentage
    if len(skills) > 0:
        match_percentage = int(
            (len(matched) / len(skills)) * 100
        )
    else:
        match_percentage = 0

    # ATS Score
    ats_score = min(len(skills) * 5, 100)

    # Suggestions
    suggestions = []

    if ats_score < 40:
        suggestions.append(
            "Add more technical skills."
        )

    if "github" not in skills:
        suggestions.append(
            "Add your GitHub profile."
        )

    if "docker" not in skills:
        suggestions.append(
            "Learn Docker and mention it if applicable."
        )

    if "aws" not in skills:
        suggestions.append(
            "Learn AWS Cloud basics."
        )

    # AI Feedback
    feedback = generate_feedback(
        skills,
        ats_score,
        missing
    )

    # Generate PDF Report
    report_path = "static/report.pdf"

    create_report(
        report_path,
        prediction,
        ats_score,
        skills,
        missing,
        suggestions
    )

    # Show Dashboard
    return render_template(
        "result.html",
        prediction=prediction,
        ats_score=ats_score,
        skills=skills,
        matched=matched,
        missing=missing,
        match_percentage=match_percentage,
        suggestions=suggestions,
        feedback=feedback,
        report_path="report.pdf"
    )


# -----------------------------
# Run Flask
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)