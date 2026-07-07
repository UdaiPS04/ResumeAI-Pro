# ResumeAI Pro

An AI-powered Resume Screening and ATS Analysis web application built using **Python, Flask, Machine Learning, and NLP**. The application classifies resumes, calculates an ATS score, extracts skills, compares resumes with a Job Description, generates AI-based feedback, and allows users to download a PDF report.

---

##  Features

- Upload Resume (PDF)
- Resume Category Prediction using Machine Learning
- ATS Score Calculation
- Skill Extraction
- Resume vs Job Description Matching
- Missing Skills Detection
- AI-Based Resume Feedback
- Download PDF Report
- Responsive Flask Web Interface

---

## Tech Stack

### Backend
- Python
- Flask

### Machine Learning
- Scikit-learn
- TF-IDF Vectorizer
- Logistic Regression

### NLP
- NLTK
- PDFPlumber

### Frontend
- HTML5
- CSS3
- Bootstrap 5

### Libraries
- Pandas
- Joblib
- ReportLab

---

## Project Structure

```
ResumeAI-Pro/
│
├── app.py
├── utils.py
├── feedback.py
├── report.py
├── requirements.txt
├── README.md
│
├── dataset/
│   └── resumes.csv
│
├── model/
│   ├── resume_classifier.pkl
│   └── tfidf_vectorizer.pkl
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── icons/
│   ├── images/
│   └── report.pdf
│
├── templates/
│   ├── index.html
│   ├── result.html
│   ├── about.html
│   └── contact.html
│
└── uploads/
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/yourusername/ResumeAI-Pro.git
```

Move into the project

```bash
cd ResumeAI-Pro
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Open your browser

```
http://127.0.0.1:5000
```

---

## How It Works

1. Upload a PDF resume.
2. Extract text using **PDFPlumber**.
3. Clean the extracted text using NLP.
4. Convert text into TF-IDF vectors.
5. Predict the resume category using the trained Logistic Regression model.
6. Extract technical skills.
7. Compare resume skills with the Job Description.
8. Calculate ATS Score.
9. Generate AI-based feedback.
10. Download a PDF report.

---

## Screenshots

### Home Page

_Add screenshot here_

### Resume Analysis Dashboard

_Add screenshot here_

### ATS Score

_Add screenshot here_

### AI Feedback

_Add screenshot here_

---

## Future Improvements

- User Authentication
- Resume History
- Database Integration
- AI Resume Rewriting
- Interview Question Generator
- Resume Ranking System
- Cloud Deployment
- Multi-language Support

---

## Learning Outcomes

This project demonstrates knowledge of:

- Machine Learning
- Natural Language Processing
- Flask Web Development
- PDF Processing
- Resume Parsing
- TF-IDF Vectorization
- Logistic Regression
- Frontend Development
- Responsive UI Design

---

## Author

**Udai Pratap Singh**

B.Tech Computer Science & Engineering (Artificial Intelligence)

---

## License

This project is developed for educational and portfolio purposes.