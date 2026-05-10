import streamlit as st
import pickle
import pandas as pd
import os

def run():

    BASE_DIR = os.path.dirname(__file__)

    # Load model files
    with open(os.path.join(BASE_DIR, "models", "model.pkl"), "rb") as f:
        model = pickle.load(f)

    with open(os.path.join(BASE_DIR, "models", "columns.pkl"), "rb") as f:
        columns = pickle.load(f)

    with open(os.path.join(BASE_DIR, "models", "scaler.pkl"), "rb") as f:
        scaler = pickle.load(f)

    # UI
    st.title("💻 Laptop Price Predictor")
    st.markdown("Predict realistic laptop prices based on specs")

    col1, col2 = st.columns(2)

    with col1:
        inches = st.slider("Screen Size (Inches)", 10.0, 20.0, 14.0)
        ram = st.selectbox("RAM (GB)", [4, 8, 16, 32])
        weight = st.slider("Weight (kg)", 0.8, 3.5, 1.5)
        cpu = st.selectbox("CPU Type", ["Intel", "AMD", "Other"])

    with col2:
        ssd = st.selectbox("SSD", ["Yes", "No"])
        hdd = st.selectbox("HDD", ["Yes", "No"])
        company = st.selectbox("Brand", ["Dell", "HP", "Apple", "Lenovo", "Asus"])

    ssd = 1 if ssd == "Yes" else 0
    hdd = 1 if hdd == "Yes" else 0

    if st.button("Predict Price"):

        input_data = {
            "inches": inches,
            "ram": ram,
            "weight": weight,
            "ssd": ssd,
            "hdd": hdd
        }

        input_df = pd.DataFrame([input_data])

        # encoding
        for col in columns:
            if col.startswith("company_"):
                input_df[col] = 1 if col == f"company_{company.lower()}" else 0

        for col in columns:
            if col.startswith("cpu_brand_"):
                input_df[col] = 1 if col == f"cpu_brand_{cpu.lower()}" else 0

        for col in columns:
            if col not in input_df.columns:
                input_df[col] = 0

        input_df = input_df[columns]

        input_scaled = scaler.transform(input_df)

        prediction = model.predict(input_scaled)[0]

        prediction = max(300, min(prediction, 3000))

        st.success(f"💰 Estimated Price: €{round(prediction, 2)}")

        if prediction < 600:
            st.info("💡 Budget range laptop")
        elif prediction < 1200:
            st.info("💡 Mid-range laptop")
        else:
            st.info("💡 High-end laptop")


if __name__ == "__main__":
    run()