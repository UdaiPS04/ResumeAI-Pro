import re

def clean_text(text: str) -> str:
    """
    Cleans raw text by converting to lowercase, removing URLs, emails, special symbols, and extra whitespace.
    """
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'http\S+\s*', ' ', text)
    text = re.sub(r'RT|cc', ' ', text)
    text = re.sub(r'#\S+', '', text)
    text = re.sub(r'@\S+', '  ', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize_and_remove_stopwords(text: str) -> list:
    """
    Tokenizes text and removes common English stop words.
    """
    stopwords = {
        'the', 'and', 'to', 'of', 'a', 'in', 'for', 'is', 'on', 'that', 'by', 'this',
        'with', 'i', 'you', 'it', 'not', 'or', 'be', 'are', 'from', 'at', 'as', 'your',
        'all', 'have', 'new', 'more', 'an', 'was', 'we', 'will', 'home', 'can', 'us'
    }
    cleaned = clean_text(text)
    tokens = cleaned.split()
    return [t for t in tokens if t not in stopwords and len(t) > 2]