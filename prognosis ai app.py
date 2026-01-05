import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="PrognosAI Dashboard",
    layout="wide"
)

# --------------------------------------------------
# BACKGROUND IMAGE FUNCTION
# --------------------------------------------------
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpg;base64,{encoded_string});
            background-size: cover;
            background-attachment: fixed;
        }}

        h1, h2, h3, h4, h5, h6, p, span {{
            color: white;
        }}

        .metric-card {{
            background-color: rgba(0, 0, 0, 0.65);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# APPLY BACKGROUND IMAGE
add_bg_from_local("aircraft_bg.jpg")

# --------------------------------------------------
# TITLE
# --------------------------------------------------
st.markdown(
    "<h1 style='color:black; text-align:center;'>✈️ PrognosAI: AI-Driven Aircraft Engine Predictive Maintenance</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='color:black; text-align:center;'>Remaining Useful Life (RUL) Prediction & Maintenance Alerts</p>",
    unsafe_allow_html=True
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("all_fd_rul_alert_results.csv")

df = load_data()

# --------------------------------------------------
# SIDEBAR CONTROLS
# --------------------------------------------------
st.sidebar.header("⚙️ Dashboard Controls")

fd_choice = st.sidebar.selectbox(
    "Select FD Dataset",
    ["FD001", "FD002", "FD003", "FD004"]
)

fd_ranges = {
    "FD001": range(1, 101),
    "FD002": range(101, 201),
    "FD003": range(201, 301),
    "FD004": range(301, 401)
}

df_fd = df[df["Engine_ID"].isin(fd_ranges[fd_choice])]

engine_id = st.sidebar.selectbox(
    "Select Engine ID",
    sorted(df_fd["Engine_ID"].unique())
)

engine_data = df_fd[df_fd["Engine_ID"] == engine_id]

# --------------------------------------------------
# KPI METRICS
# --------------------------------------------------
current_rul = engine_data.iloc[-1]["Predicted_RUL"]
current_alert = engine_data.iloc[-1]["Alert"]

alert_map = {
    "SAFE": "🟢 SAFE",
    "WARNING": "🟡 WARNING",
    "CRITICAL": "🔴 CRITICAL"
}

st.subheader("📊 Current Engine Health")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"<div class='metric-card'><h3>Engine ID</h3><h2>{engine_id}</h2></div>",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"<div class='metric-card'><h3>Predicted RUL</h3><h2>{current_rul:.2f} cycles</h2></div>",
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"<div class='metric-card'><h3>Alert Level</h3><h2>{alert_map[current_alert]}</h2></div>",
        unsafe_allow_html=True
    )

# --------------------------------------------------
# RUL DEGRADATION TREND (IMPROVED)
# --------------------------------------------------
st.subheader("📈 RUL Degradation Trend (Over Time)")

fig, ax = plt.subplots(figsize=(9, 4))

ax.plot(
    engine_data.index,
    engine_data["Predicted_RUL"],
    marker="o",
    linewidth=2,
    label="Predicted RUL"
)

ax.fill_between(
    engine_data.index,
    engine_data["Predicted_RUL"],
    alpha=0.2
)

ax.axhline(50, linestyle="--", linewidth=2, label="Safe Threshold")
ax.axhline(20, linestyle="--", linewidth=2, label="Critical Threshold")

ax.set_xlabel("Time / Cycles")
ax.set_ylabel("Remaining Useful Life (RUL)")
ax.set_title(f"{fd_choice} – Engine {engine_id} RUL Degradation")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# --------------------------------------------------
# ALERT DISTRIBUTION (IMPROVED)
# --------------------------------------------------
st.subheader("🚨 Alert Distribution Across Engines")

alert_counts = df_fd["Alert"].value_counts()

fig2, ax2 = plt.subplots(figsize=(7, 4))
bars = ax2.bar(alert_counts.index, alert_counts.values)

ax2.set_xlabel("Alert Level")
ax2.set_ylabel("Number of Engines")
ax2.set_title(f"{fd_choice} – Alert Summary")
ax2.grid(axis="y")

# Show values on bars
for bar in bars:
    height = bar.get_height()
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        int(height),
        ha="center",
        va="bottom"
    )

st.pyplot(fig2)

# --------------------------------------------------
# FULL DATA VIEW (NOT SAMPLE)
# --------------------------------------------------
with st.expander("📄 View Complete Dataset"):
    st.dataframe(df_fd)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")
st.caption("PrognosAI | AI-Driven Predictive Maintenance System | Final Year Major Project")
