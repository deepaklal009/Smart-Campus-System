import streamlit as st

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(page_title="AI Dashboard", layout="wide")

# -------------------------------
# GLOBAL CSS
# -------------------------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: #0b0f17;
    color: #e6edf3;
}

/* Container */
.block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0f1624;
    border-right: 1px solid #1f2a3a;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #c9d1d9 !important;
}

/* Titles */
h1, h2, h3 {
    color: #e6edf3;
    font-weight: 600;
}

/* Buttons */
.stButton > button {
    background: #2563eb;
    color: white;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    border: none;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background: #1d4ed8;
    transform: scale(1.03);
}

/* Cards */
.custom-card {
    background: #111827;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #1f2937;
    margin-bottom: 15px;
}

/* Divider */
hr {
    border: 1px solid #1f2937;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------
st.markdown("""
<div class="custom-card">
    <h2>🚀 AI Powered Smart campus Plateform</h2>
    <p>Switch between your AI applications</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# SIDEBAR NAVIGATION
# -------------------------------
st.sidebar.title("⚡ Navigation")

menu = st.sidebar.radio(
    "Go to",
    ["Home", "Laptop Price Predictor", "Lost & Found AI","FYP team Matching"]
)

# -------------------------------
# ROUTING
# -------------------------------
if menu == "Home":

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="custom-card">
            <h3>💻 Laptop Price Predictor</h3>
            <p>Predict laptop prices using machine learning.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="custom-card">
            <h3>🔍 Lost & Found AI</h3>
            <p>Search lost items using NLP & similarity ranking.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
    <div class="custom-card">
        <h3>🎓 FYP Team Matching</h3>
        <p>Find compatible teammates using AI recommendation system.</p>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------
# PROJECT 1
# -------------------------------
elif menu == "Laptop Price Predictor":
    from project1 import app1
    app1.run()

# -------------------------------
# PROJECT 2
# -------------------------------
elif menu == "Lost & Found AI":
    from project2 import app2
    app2.main()


elif menu == "FYP team Matching":
    from project3 import app3
    app3.run()
    

