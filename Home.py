import streamlit as st
from PIL import Image

# Page configuration
st.set_page_config(page_title="Property Investment Analytics Platform", layout="wide")

# Title
st.markdown("<h1 style='color:#00d4b1; text-align: center;'>🏡 Property Investment Analytics Platform</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: white;'>Your Intelligent Partner to Predict Prices, "
            "Decode Market Trends & Find Your Ideal Home</h4>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<div style='font-size:18px; text-align: justify; color:#cfcfcf;'>
<div style='margin-bottom: 14px;'>
✅ <b>Predict Property Prices</b> accurately based on real-time inputs like sector, area, BHK, furnishing, floor category, luxury score, and more.
</div>
<div style='margin-bottom: 14px;'>
✅ <b>Analyze Market Trends</b> with 9+ smart visual tools – including Geo heatmaps, BHK distributions, and luxury score correlations.
</div>
<div style='margin-bottom: 14px;'>
✅ <b>Find the Best Apartments</b> near any landmark (like <i>AIIMS, Dwarka</i>) using similarity-based recommendations.
</div>
<div style='margin-bottom: 14px;'>
✅ <b>Explore Feature Insights</b> – Discover how factors like area or number of bathrooms affect property prices.
</div>
<div style='margin-bottom: 14px;'>
✅ <b>Property Investment Insights</b> – Get instant analysis of your potential investment: see estimated rental income, annual cash flow, ROI, and key market assumptions for any property in Gurgaon.
</div>
<i>“We turn real estate data into decisions – so you don’t buy blindly.”</i>
</div>
""", unsafe_allow_html=True)


st.markdown("---")
