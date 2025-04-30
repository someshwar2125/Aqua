import streamlit as st
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="Hydroponic Systems Overview", layout="wide")

# Title
st.title("🌱 Detailed Overview of Hydroponic Systems")

# Introduction
st.markdown("""
Hydroponics is a method of growing plants without soil, using nutrient-rich water solutions instead. 
It offers a sustainable, space-efficient, and highly productive way to cultivate crops. 
Various systems have been developed to optimize plant growth under different environmental conditions.
""")

st.header("🔎 Major Types of Hydroponic Systems")

# 1. Nutrient Film Technique (NFT)
st.subheader("🌊 Nutrient Film Technique (NFT)")

st.markdown("""
In the Nutrient Film Technique (NFT) system, a very shallow stream of nutrient solution is recirculated past the bare roots of plants.
- **Roots** are exposed to both oxygen and nutrients.
- Ideal for **lightweight plants** like **lettuce**, **spinach**, and **herbs**.
- **Key Advantage**: Minimal water and nutrient waste.
""")

# Simple schematic for NFT
fig, ax = plt.subplots()
ax.plot([0, 1], [0.5, 0.5], color='blue', linewidth=10, label="Nutrient Flow")
ax.plot([0.2, 0.2], [0.5, 1.0], color='green', marker='o', markersize=15, label="Plant")
ax.plot([0.5, 0.5], [0.5, 1.0], color='green', marker='o', markersize=15)
ax.plot([0.8, 0.8], [0.5, 1.0], color='green', marker='o', markersize=15)
ax.set_ylim(0, 1.2)
ax.axis('off')
ax.legend()
st.pyplot(fig)

# Divider
st.markdown("---")

# 2. Ebb & Flow (Flood and Drain)
st.subheader("🔄 Ebb and Flow (Flood and Drain)")

st.markdown("""
In this system, the **grow tray is flooded** with nutrient solution at set intervals, then drained back into a reservoir.
- Plants get **periodic access to nutrients and oxygen**.
- Works best for **root vegetables**, **strawberries**, **flowers**.
- **Key Advantage**: Encourages strong root structures through wet-dry cycles.
""")

st.image(
    "https://www.researchgate.net/publication/348003824/figure/fig2/AS:974471137607680@1609343432536/Ebb-and-flow-system-of-hydroponics.jpg",
    caption="Ebb and Flow System Working",width=500,
    #use_container_width=True
)



# Divider
st.markdown("---")

# 3. Drip System
st.subheader("💧 Drip Irrigation Hydroponic System")

st.markdown("""
The Drip System delivers nutrient solution **directly to the base of each plant** via a network of small emitters.
- Perfect for **larger crops** like **tomatoes**, **peppers**, **cucumbers**.
- **Highly customizable** drip rates for each plant.
- **Key Advantage**: Precision watering saves nutrients and water.
""")

# Bar chart comparing water consumption
water_data = {
    "NFT": 5,
    "Ebb & Flow": 8,
    "Drip System": 6,
    "Soil-Based Farming": 20
}

fig2, ax2 = plt.subplots()
ax2.barh(list(water_data.keys()), list(water_data.values()), color=['blue', 'cyan', 'green', 'brown'])
ax2.set_xlabel('Liters of Water per Plant (Weekly)')
ax2.set_title('💧 Water Usage Comparison')
st.pyplot(fig2)

# Divider
st.markdown("---")

# Summary Table
st.header("📋 Quick Comparison of Systems")
comparison_data = {
    "Feature": ["Water Use", "Best Crops", "Maintenance", "Cost"],
    "NFT": ["Very Low", "Leafy greens", "Low", "Medium"],
    "Ebb & Flow": ["Moderate", "Root vegetables", "Medium", "Low"],
    "Drip System": ["Low", "Fruiting crops", "High", "High"]
}
st.table(comparison_data)

# Footer
st.markdown("""
---
**© 2025 AquaGrowth Technologies**
""")
