import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import joblib

from streamlit_app.utils.utils import clean_text

print("========== STEP 1 ==========")
print("Loading Dataset...")

# Load Dataset
df = pd.read_csv("dataset/resumes.csv")

print("Dataset Loaded Successfully")
print()

print("========== STEP 2 ==========")
print("Cleaning Resumes...")

# Clean Resume Text
df["Cleaned_Resume"] = df["Resume_str"].apply(clean_text)

print("Cleaning Completed")
print()

print("========== STEP 3 ==========")
print("Creating Features and Labels...")

# Features
X = df["Cleaned_Resume"]

# Labels
y = df["Category"]

print("Features and Labels Created")
print()

print("========== STEP 4 ==========")
print("Converting Text to TF-IDF...")

# TF-IDF
vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(X)

print("TF-IDF Completed")
print("Shape :", X.shape)
print()

print("========== STEP 5 ==========")
print("Splitting Dataset...")

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training Samples :", X_train.shape[0])
print("Testing Samples  :", X_test.shape[0])
print()

print("========== STEP 6 ==========")
print("Training Logistic Regression Model...")

# Create Model
model = LogisticRegression(max_iter=1000)

# Train Model
model.fit(X_train, y_train)

print("Model Training Completed")
print()

print("========== STEP 7 ==========")
print("Making Predictions...")

# Prediction
predictions = model.predict(X_test)

print("Prediction Completed")
print()

print("========== STEP 8 ==========")

# Accuracy
accuracy = accuracy_score(y_test, predictions)

print("Final Accuracy :", accuracy)
print("\n========== Classification Report ==========\n")

print(classification_report(y_test, predictions))
print("\n========== Confusion Matrix ==========\n")

cm = confusion_matrix(y_test, predictions)

print(cm)
joblib.dump(model, "model/resume_classifier.pkl")
joblib.dump(vectorizer, "model/tfidf_vectorizer.pkl")
print("\nModel Saved Successfully!")



'''print("\nFirst 10 Predictions")

for actual, predicted in zip(y_test.iloc[:10], predictions[:10]):
    print(f"Actual: {actual} | Predicted: {predicted}")'''