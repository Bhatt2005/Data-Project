import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# PAGE CONFIG

st.set_page_config(page_title="Sports Endurance Analytics", layout="wide")
st.title("Sports Endurance Analytics Dashboard")

# LOAD DATA + SCALE TO 100

@st.cache_data
def load_data():
    df = pd.read_csv("sports_training_dataset_expanded.csv")
    # Scale Endurance_Score so max becomes 100
    max_score = df["Endurance_Score"].max()
    df["Endurance_Score"] = (df["Endurance_Score"] / max_score) * 100
    return df

df = load_data()

# SIDEBAR FILTERS

st.sidebar.header("Filters & Inputs")

gender = st.sidebar.selectbox("Gender", df["Gender"].unique())
sport = st.sidebar.selectbox("Sport Type", df["Sport_Type"].unique())

age = st.sidebar.slider("Age",
                        int(df["Age"].min()),
                        int(df["Age"].max()),
                        20)

session_duration = st.sidebar.slider("Session Duration (min)",
                                     int(df["Session_Duration"].min()),
                                     int(df["Session_Duration"].max()),
                                     int(df["Session_Duration"].mean()))

heart_rate = st.sidebar.slider(
    "Heart Rate Avg (bpm) — lower is better for endurance",
    int(df["Heart_Rate_Avg"].min()),
    int(df["Heart_Rate_Avg"].max()),
    int(df["Heart_Rate_Avg"].mean())
)

speed = st.sidebar.slider("Speed Avg (km/h)",
                          float(df["Speed_Avg"].min()),
                          float(df["Speed_Avg"].max()),
                          float(df["Speed_Avg"].mean()))

distance = st.sidebar.slider("Distance Covered (m)",
                             float(df["Distance_Covered"].min()),
                             float(df["Distance_Covered"].max()),
                             float(df["Distance_Covered"].mean()))

technique = st.sidebar.slider("Technique Score",
                              float(df["Technique_Score"].min()),
                              float(df["Technique_Score"].max()),
                              float(df["Technique_Score"].mean()))


# FILTER DATA

filtered_df = df[
    (df["Gender"] == gender) &
    (df["Sport_Type"] == sport)
]

if filtered_df.empty:
    st.warning("No data matches selected filters.")
    st.stop()

# SIMPLE PREDICTION (Normalized to 0-100 using dataset min/max)

SESSION_MIN, SESSION_MAX = df["Session_Duration"].min(), df["Session_Duration"].max()
DISTANCE_MIN, DISTANCE_MAX = df["Distance_Covered"].min(), df["Distance_Covered"].max()
SPEED_MIN, SPEED_MAX = df["Speed_Avg"].min(), df["Speed_Avg"].max()
TECHNIQUE_MIN, TECHNIQUE_MAX = df["Technique_Score"].min(), df["Technique_Score"].max()
HR_MIN, HR_MAX = df["Heart_Rate_Avg"].min(), df["Heart_Rate_Avg"].max()

# Normalize inputs 0-100
session_norm = (session_duration - SESSION_MIN) / (SESSION_MAX - SESSION_MIN) * 100
distance_norm = (distance - DISTANCE_MIN) / (DISTANCE_MAX - DISTANCE_MIN) * 100
speed_norm = (speed - SPEED_MIN) / (SPEED_MAX - SPEED_MIN) * 100
technique_norm = (technique - TECHNIQUE_MIN) / (TECHNIQUE_MAX - TECHNIQUE_MIN) * 100
heart_rate_norm = (HR_MAX - heart_rate) / (HR_MAX - HR_MIN) * 100  # lower HR = better endurance

# Weighted average
predicted_score = (
    0.2 * session_norm +
    0.2 * distance_norm +
    0.2 * speed_norm +
    0.2 * technique_norm +
    0.2 * heart_rate_norm
)
predicted_score = min(predicted_score, 100)

# KPI SECTION

colk1, colk2, colk3 = st.columns(3)

with colk1:
    st.metric("Predicted Endurance", f"{predicted_score:.2f}")

with colk2:
    st.metric("Max Endurance (Dataset)", f"{df['Endurance_Score'].max():.2f}")

with colk3:
    st.metric("Average Endurance", f"{filtered_df['Endurance_Score'].mean():.2f}")

# VISUALIZATION SECTION

col1, col2 = st.columns(2)

# SCATTER: Session Duration vs Endurance
with col1:
    st.subheader("Session Duration vs Endurance")
    fig1, ax1 = plt.subplots()
    ax1.scatter(filtered_df["Session_Duration"], filtered_df["Endurance_Score"])
    ax1.scatter(session_duration, predicted_score, color='red', label='Prediction')
    ax1.set_xlabel("Session Duration")
    ax1.set_ylabel("Endurance Score")
    ax1.set_ylim(0, 100)
    ax1.legend()
    st.pyplot(fig1)

# SCATTER: Speed vs Endurance
with col2:
    st.subheader("Speed vs Endurance")
    fig2, ax2 = plt.subplots()
    ax2.scatter(filtered_df["Speed_Avg"], filtered_df["Endurance_Score"])
    ax2.scatter(speed, predicted_score, color='red', label='Prediction')
    ax2.set_xlabel("Speed Avg")
    ax2.set_ylabel("Endurance Score")
    ax2.set_ylim(0, 100)
    ax2.legend()
    st.pyplot(fig2)

# LINE CHART: Average Endurance by Age
st.subheader("Average Endurance by Age")
age_group = filtered_df.groupby("Age")["Endurance_Score"].mean()
fig3, ax3 = plt.subplots()
ax3.plot(age_group.index, age_group.values)
ax3.set_xlabel("Age")
ax3.set_ylabel("Average Endurance Score")
ax3.set_ylim(0, 100)
st.pyplot(fig3)

# BAR CHART: Average Endurance by Sport Type
st.subheader("Average Endurance by Sport Type")
sport_avg = df.groupby("Sport_Type")["Endurance_Score"].mean()
fig4, ax4 = plt.subplots()
ax4.bar(sport_avg.index, sport_avg.values)
ax4.set_ylabel("Average Endurance Score")
ax4.set_ylim(0, 100)
plt.xticks(rotation=45)
st.pyplot(fig4)

# HISTOGRAM: Endurance Score Distribution
st.subheader("Endurance Score Distribution")
fig5, ax5 = plt.subplots()
ax5.hist(filtered_df["Endurance_Score"], bins=20)
ax5.set_xlabel("Endurance Score")
ax5.set_ylabel("Frequency")
ax5.set_xlim(0, 100)
st.pyplot(fig5)

# TOP 10 ATHLETES WITH PERFORMANCE_LEVEL
st.subheader("Top 10 Athletes by Endurance")

top10 = filtered_df.sort_values(by="Endurance_Score", ascending=False).head(10).copy()

# Assign tiered performance levels
def endurance_performance(score):
    if score >= 80:
        return "Excellent"
    elif score >= 70:
        return "Very Good"
    elif score >= 60:
        return "Good"
    elif score >= 50:
        return "Average"
    elif score >= 40:
        return "Needs Improvement"
    else:
        return "Poor"

top10["Performance_Level"] = top10["Endurance_Score"].apply(endurance_performance)
st.dataframe(top10)

# COLLAPSIBLE FILTERED DATA PREVIEW
with st.expander("View Filtered Data (optional)"):
    st.dataframe(filtered_df.head(20))