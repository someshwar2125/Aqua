import streamlit as st
import pandas as pd

st.set_page_config(page_title="Previous Work in Hydroponics", layout="wide")

st.title("📚 Previous Work in Hydroponics (2023–2024)")
st.markdown("Explore recent research and innovations in hydroponic farming.")

# Sample data of recent hydroponics research
research_data = [
    {
        "Title": "Hydroponic Design Horizons: Transforming Urban Landscapes for Sustainable Agriculture in the Indian Context",
        "Authors": "Kirti Nishant Nikam, Nishant V. Nikam",
        "Year": "2024",
        "Summary": "Explores the integration of hydroponics into urban environments in India to enhance food security and sustainability.",
        "Link": "https://www.tandfonline.com/doi/abs/10.1080/23748834.2024.2393476"
    },
    {
        "Title": "Assessing Opportunities and Difficulties in Hydroponic Farming",
        "Authors": "Suresh Kumar, Satish Kumar, Jawahar Lal",
        "Year": "2023",
        "Summary": "Evaluates the prospects and challenges of hydroponic farming, particularly in regions with declining groundwater levels.",
        "Link": "https://www.arccjournals.com/journal/bhartiya-krishi-anusandhan-patrika/BKAP556"
    },
    {
        "Title": "Impact of Four Hydroponic Nutrient Solutions and Regrowth on Yield, Safety, and Essential Oil Profile of Basil",
        "Authors": "Saeid Hazrati et al.",
        "Year": "2025",
        "Summary": "Investigates how different nutrient solutions affect basil yield, safety, and essential oil composition in soilless systems.",
        "Link": "https://sciendo.com/article/10.2478/fhort-2024-0034"
    },
    {
        "Title": "Trends in Hydroponics Practice/Technology in Horticultural Crops: A Review",
        "Authors": "Vikanksha Arun Kumar, Jatinder Singh",
        "Year": "2023",
        "Summary": "Reviews current practices and technological advancements in hydroponic cultivation of horticultural crops.",
        "Link": "https://journalijpss.com/index.php/IJPSS/article/view/2759"
    },
    {
        "Title": "Hydroponics: The Potential to Enhance Sustainable Food Production in Non-Arable Areas",
        "Authors": "Sahil Sharma et al.",
        "Year": "2023",
        "Summary": "Discusses hydroponics as a solution for sustainable food production in regions unsuitable for traditional agriculture.",
        "Link": "https://journalcjast.com/index.php/CJAST/article/view/4253"
    },
    {
        "Title": "A Nitrogen Alternative: Use of Plasma Activated Water as Nitrogen Source in Hydroponic Solution for Radish Growth",
        "Authors": "Vikas Rathore, Sudhir Kumar Nema",
        "Year": "2024",
        "Summary": "Explores the use of plasma-activated water as an alternative nitrogen source in hydroponic radish cultivation.",
        "Link": "https://arxiv.org/abs/2404.16910"
    },
    {
        "Title": "Hydroponics: A Review on Revolutionary Technology for Sustainable Agriculture",
        "Authors": "Simerjit Kaur, Bhavin Dewan",
        "Year": "2023",
        "Summary": "Provides an overview of hydroponics as a sustainable agricultural technology addressing soil degradation and water scarcity.",
        "Link": "https://journalajahr.com/index.php/AJAHR/article/view/270"
    },
    {
        "Title": "Hydroponics: An Innovative Approach to Urban Agriculture",
        "Authors": "Aarati Ghimire, Manasha Dahal, Rojan Karki",
        "Year": "2023",
        "Summary": "Examines hydroponics as a viable method for urban agriculture, focusing on techniques and crop yields.",
        "Link": "https://www.researchgate.net/publication/373902683_Hydroponics_An_Innovative_Approach_to_Urban_Agriculture"
    },
    {
        "Title": "Artificial Intelligence in Sustainable Vertical Farming",
        "Authors": "Hribhu Chowdhury et al.",
        "Year": "2023",
        "Summary": "Analyzes the role of AI in optimizing resource usage and decision-making in vertical farming systems.",
        "Link": "https://arxiv.org/abs/2312.00030"
    },
    {
        "Title": "Optimal Control for Indoor Vertical Farms Based on Crop Growth",
        "Authors": "Annalena Daniels et al.",
        "Year": "2023",
        "Summary": "Presents an optimal control approach to enhance crop yields and resource efficiency in indoor vertical farms.",
        "Link": "https://arxiv.org/abs/2309.07540"
    },
    {
        "Title": "Development of IoT Smart Greenhouse System for Hydroponic Gardens",
        "Authors": "Arcel Christian H. Austria et al.",
        "Year": "2023",
        "Summary": "Describes the development of an IoT-based smart greenhouse system for monitoring hydroponic gardens.",
        "Link": "https://arxiv.org/abs/2305.01189"
    }
]

# Convert to DataFrame
df = pd.DataFrame(research_data)

# Display the research papers
for index, row in df.iterrows():
    st.subheader(f"{row['Title']} ({row['Year']})")
    st.markdown(f"**Authors:** {row['Authors']}")
    st.markdown(f"**Summary:** {row['Summary']}")
    st.markdown(f"[Read Full Paper]({row['Link']})")
    st.markdown("---")
