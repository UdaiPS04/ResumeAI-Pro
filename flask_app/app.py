import os
import sys
import json
import re
from pathlib import Path
from collections import Counter
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file, session
from werkzeug.utils import secure_filename

# ---------------- 1. Configure Absolute Paths with Pathlib ----------------
BASE_DIR = Path(__file__).resolve().parent

FLASK_APP_DIR = BASE_DIR / "flask_app"
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if str(FLASK_APP_DIR) not in sys.path:
    sys.path.insert(0, str(FLASK_APP_DIR))

# ---------------- 2. Configure Single Flask Application Instance ----------------
app = Flask(
    __name__,
    template_folder=str(FLASK_APP_DIR / "templates"),
    static_folder=str(FLASK_APP_DIR / "static")
)
app.secret_key = "resumeai_pro_secret_key_2026"

# ---------------- 3. Directory Configurations via Pathlib ----------------
UPLOAD_FOLDER = FLASK_APP_DIR / "uploads"
REPORT_FOLDER = BASE_DIR / "reports"
MODEL_FOLDER = BASE_DIR / "model"
DATASET_FOLDER = BASE_DIR / "dataset"

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
REPORT_FOLDER.mkdir(parents=True, exist_ok=True)
MODEL_FOLDER.mkdir(parents=True, exist_ok=True)
DATASET_FOLDER.mkdir(parents=True, exist_ok=True)

app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB Limit
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------------- 4. Import Utility Modules ----------------
try:
    from flask_app.utils.resume_parser import extract_text, extract_candidate_contact
except ImportError:
    from utils.resume_parser import extract_text, extract_candidate_contact

try:
    from flask_app.utils.predict import predict_resume_category
except ImportError:
    from utils.predict import predict_resume_category

try:
    from flask_app.utils.utils import extract_skills
except ImportError:
    from utils.utils import extract_skills

try:
    from flask_app.utils.ats import calculate_ats_score
except ImportError:
    from utils.ats import calculate_ats_score

try:
    from flask_app.utils.feedback import generate_feedback
except ImportError:
    from utils.feedback import generate_feedback

try:
    from flask_app.utils.jd_match import match_resume_with_jd
except ImportError:
    from utils.jd_match import match_resume_with_jd


# ---------------- Helper Parsers ----------------

def detect_section_coverage(text: str) -> dict:
    """Detects presence of key resume sections."""
    text_lower = text.lower()
    return {
        "contact": 100 if ('@' in text or 'phone' in text_lower or 'mobile' in text_lower) else 50,
        "skills": 100 if 'skill' in text_lower or 'technologies' in text_lower else 40,
        "experience": 100 if ('experience' in text_lower or 'employment' in text_lower or 'work' in text_lower) else 30,
        "education": 100 if ('education' in text_lower or 'degree' in text_lower or 'university' in text_lower or 'b.tech' in text_lower) else 30,
        "projects": 100 if ('project' in text_lower or 'built' in text_lower or 'developed' in text_lower) else 20
    }


def compute_keyword_frequencies(text: str) -> dict:
    stopwords = {
        'the', 'and', 'to', 'of', 'a', 'in', 'for', 'is', 'on', 'that', 'by', 'this',
        'with', 'i', 'you', 'it', 'not', 'or', 'be', 'are', 'from', 'at', 'as', 'your',
        'all', 'have', 'new', 'more', 'an', 'was', 'we', 'will', 'home', 'can', 'us',
        'about', 'page', 'if', 'has', 'search', 'free', 'but', 'our', 'one', 'other',
        'do', 'no', 'information', 'time', 'they', 'site', 'he', 'up', 'may', 'what',
        'which', 'their', 'news', 'out', 'use', 'any', 'there', 'see', 'only', 'so',
        'his', 'when', 'contact', 'here', 'business', 'who', 'web', 'also', 'now',
        'help', 'get', 'pm', 'view', 'online', 'c', 'e', 'first', 'am', 'been', 'would',
        'how', 'were', 'me', 'services', 'some', 'these', 'click', 'its', 'like', 'service'
    }
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    filtered_words = [w.capitalize() for w in words if w not in stopwords]
    counts = Counter(filtered_words).most_common(8)
    return {
        "labels": [item[0] for item in counts],
        "data": [item[1] for item in counts]
    }


def generate_real_recommendations(contact: dict, skills: list, word_count: int, missing_skills: list, coverage: dict) -> list:
    recs = []
    if contact["email"] == "Not Specified":
        recs.append("Add a clear email address in the contact section for recruiter outreach.")
    if contact["phone"] == "Not Specified":
        recs.append("Add a telephone number in the contact header.")
    if contact["linkedin"] == "Not Specified":
        recs.append("Include a LinkedIn profile URL for recruiter validation.")
    if contact["github"] == "Not Specified":
        recs.append("Include a GitHub profile link to showcase code repositories.")
    if coverage["projects"] < 100:
        recs.append("Projects section is weak or missing. Include technical project details and links.")
    if len(skills) < 5:
        recs.append("Skill density is low. List explicit technical tools, frameworks, and languages.")
    if word_count < 200:
        recs.append("Document text is brief. Expand bullet points under work experience and projects.")
    if missing_skills:
        recs.append(f"Incorporate missing job keywords: {', '.join(missing_skills[:4])}.")
    if not recs:
        recs.append("Resume formatting and keyword density meet standard ATS compliance benchmarks.")
    return recs


# ---------------- Application Routes ----------------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume_file' not in request.files:
        flash('No file provided in request.', 'error')
        return redirect(url_for('upload'))

    file = request.files['resume_file']
    if file.filename == '':
        flash('No file selected.', 'error')
        return redirect(url_for('upload'))

    if not allowed_file(file.filename):
        flash('Unsupported file format. Please upload a PDF or DOCX resume.', 'error')
        return redirect(url_for('upload'))

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        with open(filepath, 'rb') as f:
            resume_text = extract_text(f)

        if not resume_text or not resume_text.strip():
            flash('Unable to extract text from document. File may be image-based or empty.', 'error')
            return redirect(url_for('upload'))

        contact_info = extract_candidate_contact(resume_text)
        coverage = detect_section_coverage(resume_text)
        words = re.findall(r'\b\w+\b', resume_text)
        word_count = len(words)

        category, confidence = predict_resume_category(resume_text)
        skills = extract_skills(resume_text)

        jd_text = request.form.get('job_description', '').strip()
        jd_provided = bool(jd_text)

        if jd_provided:
            match_score, matching_skills, missing_skills = match_resume_with_jd(resume_text, jd_text)
            jd_message = ""
        else:
            match_score = 0
            matching_skills = []
            missing_skills = []
            jd_message = "Upload or paste a Job Description to calculate compatibility."

        ats_breakdown = calculate_ats_score(
            resume_text=resume_text,
            skills=skills,
            jd_text=jd_text,
            confidence=confidence,
            contact_info=contact_info,
            word_count=word_count,
            match_score=match_score
        )

        frequencies = compute_keyword_frequencies(resume_text)
        recommendations = generate_real_recommendations(contact_info, skills, word_count, missing_skills, coverage)

        results = {
            "filename": filename,
            "contact": contact_info,
            "category": category,
            "confidence": float(confidence),
            "ats_score": ats_breakdown["total_ats"],
            "breakdown": ats_breakdown,
            "coverage": coverage,
            "skills": skills,
            "frequencies": frequencies,
            "recommendations": recommendations,
            "jd_provided": jd_provided,
            "jd_message": jd_message,
            "match_score": int(match_score),
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "stats": {
                "word_count": word_count,
                "skills_count": len(skills)
            }
        }

        session['latest_results'] = results
        analysis_json = json.dumps(results)

        return render_template('result.html', results=results, analysis_json=analysis_json)

    except Exception as e:
        flash(f'Processing error: {str(e)}', 'error')
        return redirect(url_for('upload'))


@app.route('/job-match', methods=['GET', 'POST'])
def job_match():
    if request.method == 'POST':
        resume_text = request.form.get('resume_text', '').strip()
        jd_text = request.form.get('job_description', '').strip()

        if not resume_text or not jd_text:
            flash('Please provide both resume text and job description.', 'error')
            return render_template('job_match.html', match_results=None)

        match_score, matching_skills, missing_skills = match_resume_with_jd(resume_text, jd_text)
        match_results = {
            "match_score": match_score,
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "resume_text": resume_text,
            "jd_text": jd_text
        }
        return render_template('job_match.html', match_results=match_results)

    latest = session.get('latest_results', {})
    initial_resume = latest.get('resume_text', '')
    return render_template('job_match.html', match_results=None, initial_resume=initial_resume)


@app.route('/download-report', methods=['POST'])
def download_report():
    analysis_json = request.form.get('analysis_data', '')
    if not analysis_json and 'latest_results' in session:
        results = session['latest_results']
    elif analysis_json:
        try:
            results = json.loads(analysis_json)
        except Exception:
            results = session.get('latest_results', {})
    else:
        results = {}

    if not results:
        flash('No analysis results available to generate report.', 'error')
        return redirect(url_for('upload'))

    contact = results.get('contact', {})
    stats = results.get('stats', {})
    breakdown = results.get('breakdown', {})

    report_content = f"""================================================================
RESUMEAI PRO - RESUME ANALYSIS & ATS AUDIT REPORT
================================================================
Candidate Name: {contact.get('name', 'N/A')}
Email Address: {contact.get('email', 'N/A')}
Phone Number: {contact.get('phone', 'N/A')}
LinkedIn: {contact.get('linkedin', 'N/A')}
GitHub: {contact.get('github', 'N/A')}

Filename: {results.get('filename', 'Resume')}
Predicted Role Category: {results.get('category', 'N/A')}
Classifier Confidence: {results.get('confidence', 0.95)*100:.2f}%
ATS Score: {results.get('ats_score', 0)}/100
----------------------------------------------------------------
ATS FACTOR BREAKDOWN:
- Contact Information: {breakdown.get('contact_score', 0)}/{breakdown.get('contact_max', 10)}
- Skills Portfolio: {breakdown.get('skills_score', 0)}/{breakdown.get('skills_max', 25)}
- Education Section: {breakdown.get('education_score', 0)}/{breakdown.get('education_max', 10)}
- Projects Section: {breakdown.get('projects_score', 0)}/{breakdown.get('projects_max', 20)}
- Work Experience: {breakdown.get('experience_score', 0)}/{breakdown.get('experience_max', 15)}
- Certifications Section: {breakdown.get('certifications_score', 0)}/{breakdown.get('certifications_max', 10)}
- Formatting & Length: {breakdown.get('formatting_score', 0)}/{breakdown.get('formatting_max', 5)}
- Keyword Match Alignment: {breakdown.get('keyword_score', 0)}/{breakdown.get('keyword_max', 5)}
----------------------------------------------------------------
DOCUMENT STATISTICS:
Total Word Count: {stats.get('word_count', 0)}
Extracted Skills Count: {len(results.get('skills', []))}
----------------------------------------------------------------
EXTRACTED SKILLS PORTFOLIO:
{', '.join(results.get('skills', []))}
----------------------------------------------------------------
JOB DESCRIPTION MATCH ANALYSIS:
JD Requirement Match Index: {results.get('match_score', 0) if results.get('jd_provided') else 'N/A'}
Matched Keywords: {', '.join(results.get('matching_skills', []))}
Missing Skill Gaps: {', '.join(results.get('missing_skills', []))}
----------------------------------------------------------------
RECOMMENDATIONS & AUDIT ACTION ITEMS:
""" + "\n".join([f"- {rec}" for rec in results.get('recommendations', [])]) + """
----------------------------------------------------------------
Developer: Udai Pratap Singh (+91 7007906932 | udailps5151@gmail.com)
Generated by ResumeAI Pro Resume Analysis Platform.
================================================================
"""

    report_filename = f"ATS_Audit_Report_{secure_filename(contact.get('name', 'Candidate'))}.txt"
    report_path = REPORT_FOLDER / report_filename

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    return send_file(str(report_path), as_attachment=True, download_name=report_filename)


@app.route('/about')
def about():
    return render_template('about.html')


# ---------------- Error Handlers ----------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('layout.html', content="<div class='container py-5 text-center'><h2>404 - Page Not Found</h2><p class='text-muted'>The requested page could not be located.</p><a href='/' class='btn btn-primary-custom'>Return Home</a></div>"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('layout.html', content="<div class='container py-5 text-center'><h2>500 - Internal Server Error</h2><p class='text-muted'>An unexpected error occurred on the server.</p><a href='/' class='btn btn-primary-custom'>Return Home</a></div>"), 500


# ---------------- Main Execution ----------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)