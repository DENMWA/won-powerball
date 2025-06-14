
import streamlit as st
import pandas as pd
from mode_a_random import generate_mode_a_predictions
from mode_c_engine import generate_mode_c_predictions
from drake_post_filter import apply_drake_filter

st.set_page_config(page_title="Won Powerball 🎯", layout="centered")
st.title("💸 Won Powerball – Predict Like a Pro")

mode = st.radio("Choose a prediction mode:", ["Mode A – Absolute Random", "Mode C – Filtered Prediction", "Mode D – Drake Post-Scoring"])

if mode == "Mode A – Absolute Random":
    st.write("Generate 100 totally random Powerball entries.")
    if st.button("Generate"):
        df = generate_mode_a_predictions()
        st.dataframe(df)
        st.download_button("⬇️ Download Predictions", df.to_csv(index=False), file_name="mode_a_predictions.csv")

elif mode == "Mode C – Filtered Prediction":
    uploaded_file = st.file_uploader("Upload your historical Powerball data (CSV)", type="csv")
    if uploaded_file:
        with open("powerball_data.csv", "wb") as f:
            f.write(uploaded_file.getbuffer())
        if st.button("Run Mode C Prediction"):
            df = generate_mode_c_predictions("powerball_data.csv")
            st.dataframe(df)
            st.download_button("⬇️ Download Mode C Predictions", df.to_csv(index=False), file_name="mode_c_predictions.csv")

elif mode == "Mode D – Drake Post-Scoring":
    st.write("Upload prediction set and historical data to compute DrakeScore.")
    pred_file = st.file_uploader("Upload Predictions CSV (7 numbers + Powerball)", type="csv", key="pred")
    hist_file = st.file_uploader("Upload Historical Draws CSV", type="csv", key="hist")
    if pred_file and hist_file:
        with open("predictions.csv", "wb") as f:
            f.write(pred_file.getbuffer())
        with open("history.csv", "wb") as f:
            f.write(hist_file.getbuffer())
        if st.button("Apply Drake Filter"):
            apply_drake_filter("predictions.csv", "history.csv", output_path="scored_predictions.csv")
            df = pd.read_csv("scored_predictions.csv")
            st.dataframe(df)
            st.download_button("⬇️ Download Scored Predictions", df.to_csv(index=False), file_name="scored_predictions.csv")
