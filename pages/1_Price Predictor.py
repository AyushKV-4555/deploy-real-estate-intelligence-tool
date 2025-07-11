import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Property Price Predictor",
    layout="wide"
)

# Load assets
with open('df.pkl','rb') as file:
    df = pickle.load(file)

# with open('pipeline.pkl','rb') as file:
#     pipeline = pickle.load(file)

import requests, pickle, io

file_id = "https://drive.google.com/file/d/10V1zwQLr8lulYk-opoYlbPZaknwga0Dg/view?usp=sharing"
url = f"https://drive.google.com/uc?export=download&id={file_id}"

response = requests.get(url)
response.raise_for_status()  # raises an error if download fails

pipeline = pickle.load(io.BytesIO(response.content))

# Header
st.markdown("""
    <h1 style='text-align: center; color: #00c6a4; font-size: 42px;'>
        Enter Property Details
    </h1>
    <hr style='border: 1px solid #444;'/>
""", unsafe_allow_html=True)

# Layout columns
col1, col2, col3 = st.columns(3)

with col1:
    property_type = st.selectbox('Property Type', ['flat', 'house'])
    bedrooms = float(st.selectbox('Bedrooms', sorted(df['bedRoom'].unique().tolist())))
    built_up_area = float(st.number_input('Built Up Area (sq ft)'))
    servant_room = float(st.selectbox('Servant Room', [0.0, 1.0]))

with col2:
    sector = st.selectbox('Select Sector', sorted(df['sector'].unique().tolist()))
    bathrooms = float(st.selectbox('Bathrooms', sorted(df['bathroom'].unique().tolist())))
    store_room = float(st.selectbox('Store Room', [0.0, 1.0]))
    property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))

with col3:
    balcony = st.selectbox('Number of Balconies', sorted(df['balcony'].unique().tolist()))
    furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))
    luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))
    floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))

# Center the predict button
st.markdown("<br>", unsafe_allow_html=True)
center_col = st.columns([1, 2, 1])[1]
with center_col:
    if st.button('Predict Price', use_container_width=True):
        data = [[property_type, sector, bedrooms, bathrooms, balcony, property_age,
                 built_up_area, servant_room, store_room, furnishing_type,
                 luxury_category, floor_category]]

        columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
                   'agePossession', 'built_up_area', 'servant room', 'store room',
                   'furnishing_type', 'luxury_category', 'floor_category']

        one_df = pd.DataFrame(data, columns=columns)
        base_price = np.expm1(pipeline.predict(one_df))[0]
        low = round(base_price - 0.22, 2)
        high = round(base_price + 0.22, 2)

        # Result box
        st.markdown(f"""
        <div style='background-color: #00353f; padding: 25px; border-radius: 10px; text-align: center;'>
            <h2 style='color: #00f5d4;'>Estimated Price Range</h2>
            <h3 style='color: #ffffff; font-size: 28px;'>₹ {low} Cr - ₹ {high} Cr</h3>
        </div>
        """, unsafe_allow_html=True)
