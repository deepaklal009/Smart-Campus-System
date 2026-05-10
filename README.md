# 🚀 AI Projects Dashboard

A multi-project AI dashboard built with Streamlit that integrates multiple machine learning and AI applications into one modern interface.

---

# 📌 Overview

This project combines multiple AI-powered systems into one centralized dashboard:

- 💻 Laptop Price Predictor
- 🔍 Lost & Found AI Search System
- 🎓 Smart FYP Team Matcher

The dashboard provides:
- Clean UI
- Sidebar navigation
- Modular architecture
- Multiple AI integrations

---

# 💻 1. Laptop Price Predictor

A machine learning regression system that predicts laptop prices based on:

- RAM
- Weight
- Screen Size
- CPU Type
- SSD/HDD
- Brand

## 🔧 Technologies Used

- Scikit-learn
- KNN Regressor
- StandardScaler
- Streamlit

## ✨ Features

- Real-time prediction
- Feature scaling
- Encoded categorical inputs
- Modern UI

---

# 🔍 2. Lost & Found AI

An NLP-powered search system for finding lost items intelligently using semantic similarity.

## 🔧 Technologies Used

- NLP
- TF-IDF Vectorizer
- Cosine Similarity
- Scikit-learn
- Streamlit

## ✨ Features

- AI-powered search
- Similarity ranking
- Lost/found filtering
- Location detection
- Interactive UI

---

# 🎓 3. Smart FYP Team Matcher

A recommendation system that matches students with compatible teammates based on:

- GPA
- Skills
- Interested Domain
- Technical Strengths

## 🔧 Technologies Used

- KNN Recommendation System
- Label Encoding
- Streamlit

## ✨ Features

- Compatibility scoring
- Domain similarity matching
- Skill analysis
- Smart recommendations

---

# 🏗️ Project Structure

```plaintext
AI_Dashboard/
│
├── app.py
│
├── project1/
│   ├── app1.py
│   ├── models/
│   └── data/
│
├── project2/
│   ├── app2.py
│   ├── src/
│   ├── models/
│   └── data/
│
├── project3/
│   ├── app3.py
│   ├── models/
│   └── data/
│
└── requirements.txt


🚀 Installation
1️⃣ Clone Repository

git clone <repository-link>
cd AI_Dashboard

2️⃣ Create Virtual Environment
python -m venv venv
Activate Environment
Windows
venv\Scripts\activate
Linux / Mac
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

▶️ Run The Dashboard
streamlit run app.py
🛠️ Technologies
Python
Streamlit
Scikit-learn
Pandas
NumPy
NLP
Machine Learning
🔥 Future Improvements
User authentication
Cloud deployment
Database integration
Mobile responsiveness
More AI projects
👨‍💻 Author

Developed as a multi-project AI dashboard using Python, Streamlit, and Machine Learning.