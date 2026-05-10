from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression

def train_knn(X_train, y_train):
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train, y_train)
    return knn

def train_decision_tree(X_train, y_train):
    dt = DecisionTreeClassifier(random_state=42)
    dt.fit(X_train, y_train)
    return dt

def train_logistic_regression(X_train, y_train):
    # Initialize model
    lr = LogisticRegression(max_iter=1000)
    
    # Train model
    lr.fit(X_train, y_train)
    
    return lr