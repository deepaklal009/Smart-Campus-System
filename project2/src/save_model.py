import os
import pickle

def save_model(model, vectorizer):

    # base directory (go back from src → project root)
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    # create models folder
    models_dir = os.path.join(BASE_DIR, "models")
    os.makedirs(models_dir, exist_ok=True)

    # paths
    model_path = os.path.join(models_dir, "model.pkl")
    vectorizer_path = os.path.join(models_dir, "vectorizer.pkl")

    # save model
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    # save vectorizer
    with open(vectorizer_path, "wb") as f:
        pickle.dump(vectorizer, f)

    print("✅ Model and vectorizer saved in models folder")