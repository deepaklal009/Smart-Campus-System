import pandas as pd
from sklearn.model_selection import train_test_split

def prepare_data(df, X_vec):
    # Target (what we want to predict)
    y = df["category"]
    
    # Split data into training and testing
    X_train, X_test, y_train, y_test = train_test_split(
        X_vec, y, test_size=0.2, random_state=42
    )
    
    return X_train, X_test, y_train, y_test