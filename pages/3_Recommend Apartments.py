import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Apartment Recommender",
    page_icon="",
    layout="wide"
)

# Load data
location_df = pickle.load(open('datasets/location_distance2.pkl', 'rb'))
cosine_sim1 = pickle.load(open('datasets/cosine_sim1.pkl', 'rb'))
cosine_sim2 = pickle.load(open('datasets/cosine_sim2.pkl', 'rb'))
cosine_sim3 = pickle.load(open('datasets/cosine_sim3.pkl', 'rb'))

# Load property data with links
# ADD THIS - Load your property data that contains the 'Link' column
properties_df = pd.read_csv(
    'datasets/real_estate_data - real_estate_data.csv')

st.markdown("""
    <h1 style='text-align: center; color: #00c6a4; font-size: 42px;'>
        Apartment Finder & Recommender
    </h1>
    <hr style='border: 1px solid #444;'/>
""", unsafe_allow_html=True)


# Recommendation logic
def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = 0.25 * cosine_sim1 + 0.45 * cosine_sim2 + 0.3 * cosine_sim3
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]
    top_properties = location_df.index[top_indices].tolist()
    recommendations_df = pd.DataFrame({
        'Property Name': top_properties,
        'Similarity Score': [round(score, 4) for score in top_scores]
    })
    return recommendations_df


# Session state for selection tracking
if 'nearby_result' not in st.session_state:
    st.session_state.nearby_result = None
if 'selected_from_nearby' not in st.session_state:
    st.session_state.selected_from_nearby = None

st.markdown("""
### Find Apartments Near a Location
""")

col1, col2 = st.columns([2, 1])
with col1:
    input_location = st.selectbox('Choose a Location', sorted(location_df.columns.to_list()))
with col2:
    input_radius = st.number_input('Radius (in km)', min_value=0.5, max_value=45.0, step=0.5, value=4.0)

if st.button('Search Apartments'):
    result = location_df[location_df[input_location] < input_radius * 1000][input_location].sort_values()
    if len(result) > 0:
        st.session_state.nearby_result = result
        st.session_state.selected_from_nearby = None  # Reset selection
    else:
        st.warning('No Apartments found in the given radius.')
        st.session_state.nearby_result = None
        st.session_state.selected_from_nearby = None

# Show radio button only if nearby_result exists
if st.session_state.nearby_result is not None:
    st.session_state.selected_from_nearby = st.radio(
        "Select an apartment to get recommendations:",
        options=st.session_state.nearby_result.index.tolist(),
        index=None,
        key='apartment_radio'
    )

# Assuming you have a DataFrame called properties_df with 'PropertyName' and 'Link'
property_links = dict(zip(properties_df['PropertyName'], properties_df['Link']))


# Recommendation Section
if st.session_state.selected_from_nearby:
    st.markdown("""
    ---
    ### Recommended Apartments Based on Your Selection
    """)
    recommendation_df = recommend_properties_with_scores(st.session_state.selected_from_nearby)

    cols = st.columns(len(recommendation_df))
    for idx, row in recommendation_df.iterrows():
        with cols[idx]:
            # Get the URL for this property
            link = property_links.get(row['Property Name'], '#')
            st.markdown(
                f"""
                <div style='background-color: #222; border-radius: 12px; padding: 24px 16px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center;'>
                    <div style='font-size: 20px; font-weight: 600; color: #00c6a4; margin-bottom: 8px;'>{row['Property Name']}</div>
                    <div style='font-size: 15px; color: #bbb; margin-bottom: 18px;'>Similarity Score: <b>{row['Similarity Score']:.4f}</b></div>
                    <a href="{link}" target="_blank">
                        <button style='background-color: #00c6a4; color: #fff; border: none; border-radius: 6px; padding: 10px 20px; font-size: 16px; cursor: pointer; transition: background 0.2s;'>
                            View Details
                        </button>
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )
