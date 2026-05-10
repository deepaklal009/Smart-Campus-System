import pandas as pd
from src.vectorize import vectorize_text
from src.prepare import prepare_data
from src.train import train_knn, train_decision_tree, train_logistic_regression
from src.evaluate import evaluate_model
from src.save_model import save_model

# Load data
df = pd.read_csv("data/processed.csv")

# Step 1: Vectorize
X_vec, vectorizer = vectorize_text(df)

# Step 2: Prepare data
X_train, X_test, y_train, y_test = prepare_data(df, X_vec)


# Train KNN
print("\n--- KNN Results ---")
knn_model = train_knn(X_train, y_train)
evaluate_model(knn_model, X_test, y_test)

# Train Decision Tree
print("\n--- Decision Tree Results ---")
dt_model = train_decision_tree(X_train, y_train)
evaluate_model(dt_model, X_test, y_test)

# Train Logistic Regression
print("\n--- Logistic Regression Results ---")
lr_model = train_logistic_regression(X_train, y_train)
evaluate_model(lr_model, X_test, y_test)

# Save best model
save_model(lr_model, vectorizer)