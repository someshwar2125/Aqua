import streamlit as st

st.set_page_config(page_title="Hydroponics Growing Guide", layout="wide")
st.title("📚 Hydroponics Growing Guide")
st.markdown("Welcome to your interactive guide for mastering hydroponic farming! 🌱")

# Getting Started Section
with st.expander("🌿 Getting Started with Hydroponics"):
    st.markdown("""
    **Hydroponics** is a method of growing plants without soil, using nutrient-rich water instead. Here's what you need to begin:

    ### 🔧 Basic Requirements:
    - 💧 **Water**: Use clean, pH-balanced water (pH 5.5–6.5).
    - 🌱 **Nutrients**: Provide a complete hydroponic nutrient solution.
    - 🔆 **Light**: Ensure 12–16 hours of daily light (natural or artificial).
    - 🌀 **Oxygen**: Keep roots oxygenated with proper aeration or air stones.
    - 🪴 **Support Medium**: Use Rockwool, clay pellets, or coco coir for plant support.

    ### 🛠️ First Steps:
    1. Select a system type: NFT, DWC, Drip, or Ebb & Flow.
    2. Choose beginner-friendly plants like lettuce, basil, or spinach.
    3. Monitor **pH** and **EC** (electrical conductivity) daily.
    4. Maintain environmental conditions: Temp 18–26°C, RH 40–70%.
    """)

# Problems and Solutions Section
with st.expander("⚠️ Common Problems & Solutions"):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🌕 Yellow Leaves")
        st.write("**Cause**: Nutrient deficiency (esp. Nitrogen)")
        st.write("**Fix**: Check EC level, adjust nutrient concentration")

        st.subheader("🐢 Slow Growth")
        st.write("**Cause**: Low light or cold temperatures")
        st.write("**Fix**: Increase light hours, raise ambient temperature")
    with col2:
        st.subheader("🦠 Root Rot")
        st.write("**Cause**: Lack of oxygen or fungal pathogens")
        st.write("**Fix**: Use air stones, monitor water temperature (<22°C)")

        st.subheader("🍃 Leaf Curling")
        st.write("**Cause**: pH imbalance or heat stress")
        st.write("**Fix**: Adjust pH, improve airflow")

# Advanced Techniques
with st.expander("📈 Advanced Techniques"):
    st.markdown("""
    ### ⚙️ Nutrient Film Technique (NFT) Tips:
    - Maintain a slope of **1:30 to 1:40**.
    - **Flow rate**: 1–2 L/min for continuous thin film.
    - Keep channel length under **12 meters** to ensure even nutrient delivery.

    ### 🌡️ Environmental Control:
    - **Temperature**: 18–26°C (day), slightly lower at night.
    - **Humidity**: 40–70% relative humidity.
    - **CO2 Enrichment**: 1000–1500 ppm to enhance growth up to 30%.

    ### 🤖 Automation Ideas:
    - pH auto-dosing systems
    - EC-controlled nutrient dispensers
    - Integrated sensors for light, temp, humidity
    - IoT systems with mobile monitoring apps
    """)

# Interactive Quiz
with st.expander("🧠 Test Your Knowledge"):
    st.markdown("Take this short quiz to see how much you've learned!")

    score = 0

    q1 = st.radio("What pH level is ideal for most hydroponic systems?", ["4.5", "5.5–6.5", "7.5–8.0"])
    if q1 == "5.5–6.5":
        score += 1

    q2 = st.radio("Which is NOT a common hydroponic growing medium?", ["Clay pellets", "Soil", "Rockwool"])
    if q2 == "Soil":
        score += 1

    q3 = st.radio("What does EC stand for in hydroponics?", ["Electrical Charge", "Energy Calibration", "Electrical Conductivity"])
    if q3 == "Electrical Conductivity":
        score += 1

    if st.button("Submit Quiz"):
        st.success(f"🎉 You scored {score}/3!")
        if score == 3:
            st.balloons()
        elif score == 2:
            st.info("Great job! You're getting the hang of it.")
        else:
            st.warning("Keep studying — you're almost there!")

# Footer
st.markdown("---")
st.markdown("💡 **Tip**: Bookmark this guide and revisit it while building or maintaining your hydroponic system.")
