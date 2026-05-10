import pandas as pd
import os
import sys

BASE_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(BASE_DIR, "src"))

from search import predict_category, rank_results

# Load dataset
df = pd.read_csv("data/processed.csv")

# Known locations
locations = [
    "ab1","ab2","ab3","ab4","ab5",
    "canteen","cc","library","garden",
    "parking","love garden","mosque","hostel"
]

# Detect location
def extract_location(query):
    for loc in locations:
        if loc in query.lower():
            return loc
    return None

# Detect lost/found
def detect_status(query):
    query = query.lower()
    if "lost" in query:
        return "lost"
    elif "found" in query:
        return "found"
    return None


while True:
    query = input("\n🔍 Enter search query (or type 'exit'): ")

    if query.lower() == "exit":
        break

    # Step 1: Detect location
    location = extract_location(query)

    # Step 2: Detect status
    status = detect_status(query)

    # Step 3: Predict category using ML
    category = predict_category(query)

    print(f"\n📌 Predicted Category: {category}")

    if location:
        print(f"📍 Detected Location: {location}")

    if status:
        print(f"🔁 Showing opposite of: {status}")

    # Step 4: Filter by category
    results = df[df["category"] == category]

    # Step 5: Apply opposite status logic
    if status == "lost":
        results = results[results["status"] == "found"]
    elif status == "found":
        results = results[results["status"] == "lost"]

    # Step 6: Filter by location
    if location:
        results = results[results["location"] == location]

    # Step 7: Apply similarity ranking 🔥
    if not results.empty:
        results = rank_results(query, results)

    # Step 8: Show results
    if results.empty:
        print("❌ No matching items found")
    else:
        print("\n✅ Matching Items (Best First):")
        print(results[["clean_text", "location", "status", "name", "contact"]].head(5))