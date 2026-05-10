import joblib
import re
from sklearn.metrics.pairwise import cosine_similarity
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Load model + vectorizer
model_path = os.path.join(BASE_DIR, "models", "model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "models", "vectorizer.pkl")

model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)


# 🔧 Clean query (typo + noise handling)
def clean_query(text):
    text = text.lower()
    
    corrections = {
        "walet": "wallet",
        "walett": "wallet",
        "fone": "phone",
        "phne": "phone",
        "libary": "library",
        "mousque": "mosque",
        "watchh": "watch",
        "watc": "watch",
        "last": "lost"
    }
    
    for wrong, correct in corrections.items():
        text = text.replace(wrong, correct)
    
    text = re.sub(r'[^a-z\s]', '', text)
    
    return text


# 🤖 Predict category
def predict_category(query):
    query = clean_query(query)
    query_vec = vectorizer.transform([query])
    return model.predict(query_vec)[0]


# 🔥 NEW: rank results by similarity
def rank_results(query, results_df):
    query = clean_query(query)
    
    # Convert text to vectors
    query_vec = vectorizer.transform([query])
    result_vecs = vectorizer.transform(results_df["clean_text"])
    
    # Compute similarity
    similarities = cosine_similarity(query_vec, result_vecs).flatten()
    
    # Add similarity score
    results_df = results_df.copy()
    results_df["similarity"] = similarities
    
    # Sort by best match
    results_df = results_df.sort_values(by="similarity", ascending=False)
    
    return results_df