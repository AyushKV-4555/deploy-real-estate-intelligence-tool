import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline

# --- Load data ---
df = pd.read_csv("datasets/gurgaon_properties_post_feature_selection_v2.csv")
df = df.drop(columns=['store room', 'floor_category', 'balcony'])

age_map = {'New Property': 0.1, 'Ready to Move': 0.5, 'Under Construction': 0.9}
df['age_score'] = df['agePossession'].map(age_map)

df = df.drop(columns=['property_type', 'sector', 'luxury_category', 'agePossession'])

# --- Train model ---

X = df.drop(columns=['price'])
y = df['price']

model = make_pipeline(
    SimpleImputer(strategy='mean'),     # 🧽 Handles NaN values
    StandardScaler(),
    Ridge()
)
model.fit(X, y)
x_sample = X.mean().to_frame().T

st.markdown("""
    <h1 style='text-align: center; color: #00c6a4; font-size: 42px;'>
        Feature Impact on Price
    </h1>
    <hr style='border: 1px solid #444;'/>
""", unsafe_allow_html=True)

st.markdown("Predict how much **property price** changes when a specific feature is increased.")

# Feature selection
feature_options = {
    'Area (sqft)': 'built_up_area',
    'Bedrooms': 'bedRoom',
    'Bathrooms': 'bathroom',
    'Furnishing Type': 'furnishing_type',
    'Property Age Score 0-1': 'age_score'
}


# Create two columns for side-by-side inputs
col1, col2 = st.columns(2)

with col1:
    feature_label = st.selectbox("Choose Feature to Change", list(feature_options.keys()))
    selected_feature = feature_options[feature_label]

with col2:
    change_value = st.number_input(
        f"Enter how much to increase **{feature_label}** by",
        step=1.0,
        format="%.2f"
    )


# --- Predict function ---
def predict_change(feature, change):
    x_new = x_sample.copy()
    x_new[feature] += change
    price_before = model.predict(x_sample)[0]
    price_after = model.predict(x_new)[0]
    diff = price_after - price_before
    percent = (diff / price_before) * 100

    return {
        'Price Before': round(price_before, 2),
        'Price After': round(price_after, 2),
        'Increase in ₹ Cr': round(diff, 2),
        'Percent Increase': round(percent, 2)
    }

# Estimate Impact Button

# Estimate Impact Button
if st.button("Estimate Impact"):
    result = predict_change(selected_feature, change_value)

    col3, col4 = st.columns(2)
    with col3:
        st.metric("Price Before", f"₹ {result['Price Before']} Cr")
        st.metric("Price Increase", f"₹ {result['Increase in ₹ Cr']} Cr")
    with col4:
        st.metric("Price After", f"₹ {result['Price After']} Cr")
        st.metric("Percent Increase", f"{result['Percent Increase']} %")



