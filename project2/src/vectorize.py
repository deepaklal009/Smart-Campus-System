import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def vectorize_text(df):
    # Convert to lowercase (important)
    df["clean_text"] = df["clean_text"].str.lower()
    
    # Initialize TF-IDF
    vectorizer = TfidfVectorizer()
    
    # Fit + transform text
    X_vec = vectorizer.fit_transform(df["clean_text"])
    
    return X_vec, vectorizer