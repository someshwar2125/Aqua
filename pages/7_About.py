import streamlit as st

st.set_page_config(page_title="About Hydroponics AI", layout="wide")
st.title("ℹ️ About Hydroponics AI")

st.markdown("""
Hydroponics AI is revolutionizing modern agriculture by combining **smart sensors**, **artificial intelligence**, and **data science** to empower growers and hobbyists alike. 🌿🤖
""")

st.header("🎯 Our Mission")
st.markdown("""
To democratize hydroponic farming by providing AI-powered monitoring, analysis, and actionable recommendations that make growing smarter, not harder.
""")

st.header("🔍 How It Works")
st.markdown("""
1. 📡 **Data Collection**: Real-time input from IoT sensors tracking pH, EC, temperature, humidity, light, and water levels.  
2. 🧠 **Smart Analysis**: Our AI models identify patterns and detect anomalies in your system.  
3. 🌱 **Customized Recommendations**: Grow-specific tips for nutrient adjustment, lighting, and environmental optimization.
""")

st.header("🚀 Key Features")
st.markdown("""
- ✅ **Live System Monitoring**  
- ✅ **Plant-specific Care Guidance**  
- ✅ **Automated Alerts for Issues**  
- ✅ **Growth Optimization Models**  
- ✅ **User Dashboard with Interactive Visuals**  
- ✅ **Historical Data & Trends**  
- ✅ **AI-driven Nutrient & Light Adjustment Tips**
""")

st.header("🧪 Technology Stack")
tech_col1, tech_col2 = st.columns(2)
with tech_col1:
    st.markdown("""
    - 🐍 **Python**: Core logic and backend  
    - 🎈 **Streamlit**: Interactive dashboards  
    - 📊 **Altair** & **Plotly**: Visualization & reporting   
    - 🤖 **Scikit-learn / TensorFlow**: Machine learning models 
    """)

st.header("🌍 Our Vision")
st.markdown("""
We envision a future where **sustainable food production** is possible in every home, school, and community, regardless of climate or soil condition — powered by **data, not dirt**.
""")


st.header("⚠️ Disclaimer")
st.markdown("""
This application is intended for **educational and research purposes**. For large-scale commercial farming, always consult local agricultural experts and certified agronomists.
""")

st.header("👥 Meet the Team")
st.markdown("We're an engineers dedicated to building the future of smart agriculture.")

team_col1, team_col2, team_col3 = st.columns(3)
with team_col1:
    st.image("https://via.placeholder.com/150", width=120)
    st.markdown("""
    **Someshwar Singh**  
    🧪 *Machine learning Engineer*  
    Expert in implementing machine learning model.
    """)
with team_col2:
    st.image("https://via.placeholder.com/150", width=120)
    st.markdown("""
    **Rases Pathak**  
    📊 *Full Stack Developer*  
    Builds dynamic and responsive website and contents.
    """)
with team_col3:
    st.image("https://via.placeholder.com/150", width=120)
    st.markdown("""
    **Shivangi Yadav**  
    🔧 *Full Stack Developer*  
    Build dynamic and responsive website and contents.
    """)

st.markdown("---")
st.markdown("🌱 *Together, we're growing a greener future—one root at a time.*")
