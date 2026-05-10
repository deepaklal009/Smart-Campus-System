import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors
import joblib
import os
def run():
    BASE_DIR = os.path.dirname(__file__)

    # ---------------- PAGE CONFIG ----------------
    st.set_page_config(
        page_title="Smart FYP Team Matcher",
        page_icon="🎓",
        layout="centered"
    )

    # ---------------- CUSTOM CSS ----------------
    st.markdown("""
    <style>

    .main {
        background-color: #0E1117;
    }

    .stButton > button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        padding: 12px 24px;
        border: none;
        font-size: 18px;
        font-weight: bold;
    }

    .stButton > button:hover {
        background-color: #ff2e2e;
        color: white;
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------------- LOAD DATA ----------------
    df = pd.read_csv(
        os.path.join(BASE_DIR, "data", "cs_students.csv")
    )

    # Remove duplicates
    df = df.drop_duplicates()

    # ---------------- SKILL MAPPING ----------------
    skill_map = {
        "Weak": 1,
        "Average": 2,
        "Strong": 3
    }

    # Encode skills
    df["Python_num"] = df["Python"].map(skill_map)
    df["SQL_num"] = df["SQL"].map(skill_map)
    df["Java_num"] = df["Java"].map(skill_map)

    # ---------------- RELATED DOMAINS ----------------
    related_domains = {

        "Machine Learning": [
            "Artificial Intelligence",
            "Data Science",
            "Natural Language Processing",
            "Computer Vision"
        ],

        "Artificial Intelligence": [
            "Machine Learning",
            "Data Science",
            "Natural Language Processing",
            "Computer Vision"
        ],

        "Web Development": [
            "Software Development",
            "Cloud Computing"
        ],

        "Cloud Computing": [
            "Web Development",
            "Distributed Systems"
        ],

        "Cybersecurity": [
            "Network Security",
            "Digital Forensics",
            "Data Privacy"
        ]
    }

    # ---------------- LOAD MODELS ----------------
    knn = joblib.load(os.path.join(BASE_DIR, "models", "knn.pkl"))
    scaler = joblib.load(os.path.join(BASE_DIR, "models", "scaler.pkl"))
    domain_encoder = joblib.load(os.path.join(BASE_DIR, "models", "domain_encoder.pkl"))
    df = joblib.load(os.path.join(BASE_DIR, "models", "data.pkl"))
    # ---------------- FEATURE MATRIX ----------------


    # ---------------- UI ----------------
    st.title("🎓 Smart FYP Team Matcher")

    st.markdown(
        "Find teammates based on GPA, domain & skills"
    )

    st.write("")

    st.subheader("Enter Your Details")

    name = st.text_input("Your Name")

    col1, col2 = st.columns(2)

    with col1:

        python_skill = st.selectbox(
            "Python Skill",
            ["Weak", "Average", "Strong"]
        )

        sql_skill = st.selectbox(
            "SQL Skill",
            ["Weak", "Average", "Strong"]
        )

        java_skill = st.selectbox(
            "Java Skill",
            ["Weak", "Average", "Strong"]
        )

    with col2:

        gpa = st.slider(
            "GPA",
            2.0,
            4.0,
            3.0,
            0.01
        )

        domain = st.selectbox(
            "Interested Domain",
            sorted(df["Interested Domain"].unique())
        )

    # ---------------- COMPATIBILITY FUNCTION ----------------
    def calculate_compatibility(user, student):

        # -------- DOMAIN SCORE --------
        if user["domain"] == student["Interested Domain"]:
            domain_score = 40

        elif (
            user["domain"] in related_domains
            and student["Interested Domain"]
            in related_domains[user["domain"]]
        ):
            domain_score = 25

        else:
            domain_score = 0

        # -------- GPA SCORE --------
        gpa_diff = abs(user["gpa"] - student["GPA"])

        gpa_score = max(0, 20 - (gpa_diff * 20))

        # -------- PYTHON SCORE --------
        python_diff = abs(
            user["python"] - student["Python_num"]
        )

        python_score = max(0, 15 - (python_diff * 7))

        # -------- SQL SCORE --------
        sql_diff = abs(
            user["sql"] - student["SQL_num"]
        )

        sql_score = max(0, 15 - (sql_diff * 7))

        # -------- JAVA SCORE --------
        java_diff = abs(
            user["java"] - student["Java_num"]
        )

        java_score = max(0, 10 - (java_diff * 5))

        # -------- FINAL SCORE --------
        total_score = (
            domain_score +
            gpa_score +
            python_score +
            sql_score +
            java_score
        )

        return round(total_score, 2)

    # ---------------- FIND TEAM ----------------
    if st.button("🚀 Find Team"):

        # -------- USER VECTOR --------
        user_vector = np.array([[
            gpa,
            domain_encoder.transform([domain])[0],
            skill_map[python_skill],
            skill_map[sql_skill],
            skill_map[java_skill]
        ]])

        user_vector_scaled = scaler.transform(user_vector)

        # -------- KNN SEARCH --------
        distances, indices = knn.kneighbors(user_vector_scaled)

        recommended = df.iloc[indices[0]].copy()

        # Remove same user if exists
        if name.strip() != "":
            recommended = recommended[
                recommended["Name"].str.lower()
                != name.lower()
            ]

        # -------- USER DATA --------
        user_data = {
            "gpa": gpa,
            "domain": domain,
            "python": skill_map[python_skill],
            "sql": skill_map[sql_skill],
            "java": skill_map[java_skill]
        }

        # -------- CALCULATE COMPATIBILITY --------
        recommended["Compatibility"] = recommended.apply(
            lambda row: calculate_compatibility(
                user_data,
                row
            ),
            axis=1
        )

        # -------- SORT RESULTS --------
        recommended = recommended.sort_values(
            by="Compatibility",
            ascending=False
        )

        # -------- WARNINGS --------
        exact_match = any(
            recommended["Interested Domain"] == domain
        )

        if not exact_match:
            st.warning(
                "⚠️ No exact domain match found. Showing related domains."
            )

        # ---------------- OUTPUT ----------------
        st.write("---")

        st.subheader("🎯 Recommended Teammates")

        for _, row in recommended.head(5).iterrows():

            compatibility = row["Compatibility"]

            if compatibility >= 70:
                compatibility_color = "#00ff99"

            elif compatibility >= 50:
                compatibility_color = "#ffcc00"

            else:
                compatibility_color = "#ff6666"

            card_html = f"""
    <div style="background:#1c1f26;padding:25px;border-radius:18px;margin-bottom:20px;border:1px solid #333;box-shadow:0px 0px 15px rgba(0,0,0,0.3);">

    <h2 style="color:white;margin-bottom:15px;">
    👤 {row['Name']}
    </h2>

    <p style="font-size:17px;color:#d1d1d1;">
    🎯 <b>Domain:</b> {row['Interested Domain']}
    </p>

    <p style="font-size:17px;color:#d1d1d1;">
    📊 <b>GPA:</b> {row['GPA']}
    </p>

    <p style="font-size:17px;color:#d1d1d1;">
    💻 <b>Python:</b> {row['Python']}
    &nbsp;&nbsp;&nbsp;
    🗄 <b>SQL:</b> {row['SQL']}
    &nbsp;&nbsp;&nbsp;
    ☕ <b>Java:</b> {row['Java']}
    </p>

    <div style="margin-top:15px;background:#2a2f3a;border-radius:12px;overflow:hidden;">

    <div style="width:{compatibility}%;background:{compatibility_color};padding:10px;color:black;font-weight:bold;text-align:center;">

    🤝 Compatibility {compatibility}%

    </div>

    </div>

    </div>
    """

            st.markdown(
                card_html,
                unsafe_allow_html=True
            )

        # ---------------- ANALYTICS ----------------
        st.write("---")

        avg_score = recommended["Compatibility"].mean()

        st.info(
            f"📈 Average Team Compatibility: "
            f"{round(avg_score, 2)}%"
        )