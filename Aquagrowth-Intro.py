import streamlit as st
from PIL import Image
import io

# Configure the page with green theme
st.set_page_config(
    page_title="AquaGrowth - Hydroponics AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create a simple logo (in a real app, you'd use an actual image file)
def create_simple_logo():
    img = Image.new('RGB', (200, 60), color=(73, 109, 137))
    return img

logo = create_simple_logo()

# Custom CSS with background image and enhanced styling
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        '''background: linear-gradient(rgba(232, 245, 233, 0.9), rgba(200, 230, 201, 0.9)), 
                    url('https://images.unsplash.com/photo-1586771107445-d3ca888129ce?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80');'''
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }
    .main-title {
        font-size: 3.5rem !important;
        #color: #1b5e20 !important;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    }
    .main-subtitle {
        font-size: 1.5rem !important;
        color: #2e7d32 !important;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .feature-box {
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        box-shadow: 0 4px 15px rgba(0,100,0,0.15);
        height: 100%;
        border-left: 5px solid #2e7d32;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .feature-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,100,0,0.2);
    }
    .features-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 20px;
    }
    .divider {
        height: 2px;
        background: linear-gradient(90deg, #c8e6c9, #2e7d32, #c8e6c9);
        margin: 30px 0;
        border: none;
    }
    .how-to-use {
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 15px;
        padding: 25px;
        color: #1b5e20;
        border: 1px solid #81c784;
        box-shadow: 0 4px 8px rgba(0,100,0,0.1);
    }
    .hydroponics-info {
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 25px;
        border-left: 5px solid #2e7d32;
        '''color: #1b5e20;'''
        box-shadow: 0 4px 8px rgba(0,100,0,0.1);
    }
    .feature-title {
        color: #1b5e20 !important;
        border-bottom: 2px solid #81c784;
        padding-bottom: 10px;
        font-size: 1.4rem !important;
    }
    ul.feature-list {
        color: #2e7d32;
        padding-left: 25px;
    }
    li.feature-item {
        margin-bottom: 10px;
        font-size: 1rem;
    }
    .stButton>button {
        background-color: #2e7d32;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: bold;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
        transform: scale(1.05);
    }
    /* Horizontal navigation */
    .nav-container {
        display: flex;
        justify-content: center;
        margin-bottom: 30px;
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .nav-item {
        padding: 10px 20px;
        margin: 0 5px;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
        color: #2e7d32;
        transition: all 0.3s;
    }
    .nav-item:hover {
        background-color: #e8f5e9;
        color: #1b5e20;
    }
    .nav-item.active {
        background-color: #2e7d32;
        color: white;
    }
    /* Metrics cards */
    .metric-card {
        '''background-color: rgba(255, 255, 255, 0.9);'''
        border-radius: 10px;
        padding: 15px;
        margin: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        text-align: center;
        border-top: 4px solid #2e7d32;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1b5e20;
        margin: 5px 0;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #2e7d32;
    }
    /* Tooltip */
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted #2e7d32;
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #1b5e20;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

# Interactive Metrics Section
def create_metrics():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Current pH Level</div>
            <div class="metric-value">6.2</div>
            <div class="tooltip">Optimal Range
                <span class="tooltiptext">Ideal pH range: 5.5-6.5 for most plants</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Water Temp</div>
            <div class="metric-value">22°C</div>
            <div class="tooltip">Optimal Range
                <span class="tooltiptext">Ideal temperature: 18-26°C</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">EC Level</div>
            <div class="metric-value">1.8</div>
            <div class="tooltip">Optimal Range
                <span class="tooltiptext">Ideal EC range: 1.2-2.4 mS/cm</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Growth Rate</div>
            <div class="metric-value">+32%</div>
            <div class="tooltip">vs Soil
                <span class="tooltiptext">Compared to traditional soil growth</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Main Content
def main():
    create_metrics()
    
    st.markdown('<h1 class="main-title">🌱 AquaGrowth</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="main-subtitle">Smart Hydroponic Monitoring System</h2>', unsafe_allow_html=True)

    # Hydroponics Introduction (Green)
    with st.expander("What is Hydroponics?", expanded=True):
        st.markdown("""
        <div class="hydroponics-info">
            <p style='color:#2e7d32; font-size: 1.1rem;'>Hydroponics is a method of growing plants without soil, using mineral nutrient solutions in an aqueous solvent.</p>
            <ul class="feature-list">
                <li class="feature-item">🌊 <b>Water Efficient:</b> Uses 90% less water than soil farming</li>
                <li class="feature-item">🚀 <b>Faster Growth:</b> Plants grow 30-50% faster</li>
                <li class="feature-item">⚡ <b>Precision Control:</b> Optimal nutrient delivery</li>
                <li class="feature-item">🌍 <b>Space Saving:</b> Grow vertically in urban areas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Divider
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Feature Highlights - Horizontal Layout (Green)
    st.markdown('<h3 style="color:#1b5e20; text-align: center;">Key Features</h3>', unsafe_allow_html=True)

    st.markdown('<div class="features-container">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="feature-box">
            <h4 class="feature-title">🌿 Plant Growth Prediction</h4>
            <ul class="feature-list">
                <li class="feature-item">📊 Monitors pH (5.5-6.5 optimal)</li>
                <li class="feature-item">🧪 Tracks EC levels (1.2-2.4)</li>
                <li class="feature-item">🌡️ Maintains 18-26°C temperature</li>
                <li class="feature-item">💡 Optimizes light cycles</li>
            </ul>
            <p style='color:#2e7d32;'>92% accurate growth forecasting</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-box">
            <h4 class="feature-title">⚙️ System Recommendations</h4>
            <ul class="feature-list">
                <li class="feature-item"><b>NFT:</b> Perfect for lettuce & herbs</li>
                <li class="feature-item"><b>Drip:</b> Best for tomatoes & peppers</li>
                <li class="feature-item"><b>Ebb & Flow:</b> Versatile for flowers</li>
            </ul>
            <p style='color:#2e7d32;'>Customized for your space and goals</p>
        </div>
        """, unsafe_allow_html=True)

    

    st.markdown('</div>', unsafe_allow_html=True)  # Close features-container

    # Divider
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # How to Use Section (Green)
    st.markdown("""
    <div class="how-to-use">
        <h3 style='color:#1b5e20; text-align: center;'>How AquaGrowth Works</h3>
        <ol style='color:#2e7d32; font-size: 1.1rem;'>
            <li><b>Setup Your Profile</b> - Enter your hydroponic configuration</li>
            <li><b>AI Analysis</b> - We process 15+ growth factors</li>
            <li><b>Get Insights</b> - Receive customized recommendations</li>
            <li><b>Grow Smarter</b> - Implement and track improvements</li>
        </ol>
        <p style='text-align: center; color: #1b5e20; font-style: italic; margin-top: 20px;'>
            Begin your optimized hydroponic journey today!
        </p>
    </div>
    """, unsafe_allow_html=True)


    # Footer
    st.markdown("""
    <div class="divider"></div>
    <p style='text-align: center; color: #2e7d32; font-size: 0.9rem;'>
        <b>AquaGrowth</b> | 🌱 Sustainable Growing Through AI | contact@aquagrowth.tech | © 2025
    </p>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()


