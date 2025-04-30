
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Plant Growth Data Visualizer", layout="wide")

st.title("📊 Hydroponic Plant Growth Data Visualization")
st.markdown("This dashboard enables interactive exploration of plant growth data collected from various hydroponic systems.")

# Load actual dataset
@st.cache_data
def load_data():
    import os
    dataset_path = os.path.join(os.path.dirname(__file__), "hydroponics_system_dataset.csv")
    return pd.read_csv(dataset_path)

df = load_data()

# -------------------------------
# 📘 Parameter Overview
# -------------------------------
with st.expander("📘 **Parameter Overview**"):
    st.markdown("""
    | Parameter | Description |
    |-----------|-------------|
    | `plant_id` | Unique identifier for each plant sample |
    | `plant_type` | Type of plant (e.g., Tomato, Lettuce) |
    | `temperature_c` | Temperature in °C, affecting metabolic processes |
    | `humidity_percent` | Humidity in %, influences water retention |
    | `ph_level` | Water acidity, vital for nutrient absorption |
    | `ec_level` | Electrical conductivity, proxy for nutrient concentration |
    | `light_hours` | Daily light exposure in hours |
    | `co2_ppm` | CO₂ concentration (ppm), affects photosynthesis |
    | `nitrogen_ppm` | Nitrogen level, essential for leafy growth |
    | `phosphorus_ppm` | Promotes root and flower development |
    | `potassium_ppm` | Enhances plant immunity and structure |
    | `growth_days` | Number of days since planting |
    | `growth_rate` | Growth output (e.g., cm/day or g/day) |
    | `recommended_system` | Best hydroponic system for plant type |
    | `is_failure` | True if plant failed to grow |
    | `water_flow_lpm` | Water flow in liters per minute |
    | `timestamp` | Date and time of observation |
    """)

# -------------------------------
# 📊 Summary Statistics
# -------------------------------
with st.expander("📊 **Summary Statistics**"):
    st.write("Descriptive statistics for numerical parameters:")
    st.dataframe(df.describe().style.format("{:.2f}"))

# -------------------------------
# 📈 Correlation Heatmap
# -------------------------------
with st.expander("📈 **Correlation Heatmap**"):
    st.write("Correlation between numerical parameters:")
    numeric_df = df.select_dtypes(include=np.number)
    corr = numeric_df.corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
    st.pyplot(fig)

# -------------------------------
# 🌱 Plant Type Distribution
# -------------------------------
with st.expander("🌱 **Plant Type Distribution**"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Count by plant type:")
        plant_counts = df['plant_type'].value_counts().reset_index()
        plant_counts.columns = ['Plant Type', 'Count']
        st.dataframe(plant_counts)
    
    with col2:
        st.write("Visual distribution:")
        bar_chart = alt.Chart(plant_counts).mark_bar().encode(
            x='Plant Type',
            y='Count',
            color='Plant Type',
            tooltip=['Plant Type', 'Count']
        ).properties(width=400, height=300)
        st.altair_chart(bar_chart)

# -------------------------------
# Parameter Selection
# -------------------------------
st.sidebar.header("Parameter Selection")
param = st.sidebar.selectbox("Select parameter to visualize", 
                           ["temperature_c", "ph_level", "ec_level", "light_hours", "co2_ppm", "growth_rate"])

# -------------------------------
# Time Series Line Chart
# -------------------------------
st.subheader(f"📈 Trend of {param.replace('_', ' ').title()} Over Time")
line_chart = alt.Chart(df).mark_line().encode(
    x='timestamp:T',
    y=f'{param}:Q',
    color='plant_type:N',
    tooltip=['plant_type', 'timestamp', param]
).properties(width=800, height=400).interactive()
st.altair_chart(line_chart, use_container_width=True)

# -------------------------------
# Correlation Scatter Plot
# -------------------------------
st.subheader("📌 Correlation Between Parameters")
col1, col2 = st.columns(2)
with col1:
    x_axis = st.selectbox("X-axis", df.select_dtypes(include=np.number).columns.tolist(), index=0)
with col2:
    y_axis = st.selectbox("Y-axis", df.select_dtypes(include=np.number).columns.tolist(), index=5)

scatter = alt.Chart(df).mark_circle(size=70).encode(
    x=x_axis,
    y=y_axis,
    color='plant_type',
    tooltip=[x_axis, y_axis, 'plant_type', 'growth_rate']
).interactive().properties(width=800, height=400)
st.altair_chart(scatter, use_container_width=True)

st.markdown("---")
st.markdown("🔎 Use this dashboard to monitor and optimize plant performance in different hydroponic environments.")