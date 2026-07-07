import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

from skills import SKILLS

def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        if skill in text:

            found_skills.append(skill)

    return sorted(list(set(found_skills)))

def match_resume_to_jd(resume_skills, job_description):

    job_description = job_description.lower()

    jd_skills = []

    for skill in resume_skills:

        if skill in job_description:
            jd_skills.append(skill)

    return jd_skills
from skills import SKILLS

def missing_skills(job_description, resume_skills):

    job_description = job_description.lower()

    missing = []

    for skill in SKILLS:

        if skill in job_description and skill not in resume_skills:

            missing.append(skill)

    return missing

def clean_text(text):

    # Lowercase
    text = text.lower()

    # Remove special characters
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)

    # Tokenize
    words = word_tokenize(text)

    # Remove stopwords and lemmatize
    cleaned_words = []

    for word in words:

        if word not in stop_words:
            cleaned_words.append(lemmatizer.lemmatize(word))

    return " ".join(cleaned_words)

