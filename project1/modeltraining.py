from xml.parsers.expat import model
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import pickle
import os

# Load dataset
df = pd.read_csv(r'D:/final project AI/data/laptop_price - dataset.csv')

# -------------------------------
# 🔥 0. STANDARDIZE COLUMN NAMES
# -------------------------------
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

print("Columns:", df.columns)  # DEBUG

# -------------------------------
# 1. Drop unnecessary columns
# -------------------------------
df = df.drop(['laptop_id', 'product'], axis=1, errors='ignore')

# -------------------------------
# 2. FIX COLUMN NAME MAPPING
# -------------------------------
# Detect correct column names dynamically

ram_col = [c for c in df.columns if 'ram' in c][0]
weight_col = [c for c in df.columns if 'weight' in c][0]
price_col = [c for c in df.columns if 'price' in c][0]
inches_col = [c for c in df.columns if 'inch' in c][0]
cpu_col = [c for c in df.columns if 'cpu' in c][0]
memory_col = [c for c in df.columns if 'memory' in c][0]
company_col = [c for c in df.columns if 'company' in c][0]

# -------------------------------
# 3. Clean data
# -------------------------------
df[ram_col] = df[ram_col].astype(str).str.replace('gb', '', regex=False)
df[weight_col] = df[weight_col].astype(str).str.replace('kg', '', regex=False)

df[ram_col] = pd.to_numeric(df[ram_col], errors='coerce')
df[weight_col] = pd.to_numeric(df[weight_col], errors='coerce')

# -------------------------------
# 4. Handle missing values
# -------------------------------
for col in [inches_col, ram_col, weight_col, price_col]:
    df[col] = df[col].fillna(df[col].median())

# -------------------------------
# 5. Feature Engineering
# -------------------------------
df['cpu_brand'] = df[cpu_col].apply(
    lambda x: 'intel' if 'intel' in str(x).lower()
    else ('amd' if 'amd' in str(x).lower() else 'other')
)

df['ssd'] = df[memory_col].apply(lambda x: 1 if 'ssd' in str(x).lower() else 0)
df['hdd'] = df[memory_col].apply(lambda x: 1 if 'hdd' in str(x).lower() else 0)

# -------------------------------
# 6. Select required columns
# -------------------------------
df = df[[inches_col, ram_col, weight_col, 'ssd', 'hdd', company_col, 'cpu_brand', price_col]]

# Rename to standard names
df.columns = ['inches', 'ram', 'weight', 'ssd', 'hdd', 'company', 'cpu_brand', 'price']

# -------------------------------
# 7. Handle outliers
# -------------------------------
lower = df['price'].quantile(0.01)
upper = df['price'].quantile(0.99)
df = df[(df['price'] >= lower) & (df['price'] <= upper)]

# -------------------------------
# 8. Encode categorical
# -------------------------------
df = pd.get_dummies(df, drop_first=True)

# -------------------------------
# 9. Split
# -------------------------------
X = df.drop('price', axis=1)
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------
# 10. Scaling
# -------------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -------------------------------
# 11. Train model
# -------------------------------
knn = KNeighborsRegressor(n_neighbors=5)
knn.fit(X_train_scaled, y_train)

# -------------------------------
# ✅ CREATE MODELS FOLDER
# -------------------------------
models_dir = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(models_dir, exist_ok=True)

# -------------------------------
# ✅ PATHS
# -------------------------------
model_path = os.path.join(models_dir, "model.pkl")
columns_path = os.path.join(models_dir, "columns.pkl")
scaler_path = os.path.join(models_dir, "scaler.pkl")

# -------------------------------
# ✅ SAVE ALL FILES
# -------------------------------
with open(model_path, "wb") as f:
    pickle.dump(knn, f)

with open(columns_path, "wb") as f:
    pickle.dump(X.columns, f)

with open(scaler_path, "wb") as f:
    pickle.dump(scaler, f)

print("✅ Model, columns, scaler saved successfully!")