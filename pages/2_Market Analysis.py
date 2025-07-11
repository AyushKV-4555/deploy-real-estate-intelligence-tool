import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import ast
import pickle


# Set Streamlit page config
st.set_page_config(page_title='Real Estate Analytics', layout='wide')
st.markdown("""
    <h1 style='text-align: center; color: #00c6a4; font-size: 42px;'>
        Real Estate Analytics Dashboard
    </h1>
    <hr style='border: 1px solid #444;'/>
""", unsafe_allow_html=True)

# Load Data
new_df = pd.read_csv('datasets/data_viz1.csv')
feature_text = pickle.load(open('datasets/feature_text.pkl','rb'))
wordcloud_df = pickle.load(open('datasets/wordcloud_df.pkl','rb'))

# Preprocessing
new_df = new_df.dropna(subset=['price', 'built_up_area'])

# ---------------------------------- Graph 1: Sector Price per Sqft Map ----------------------------------
st.subheader('1. Sector Price per Sqft - Geomap')
group_df = new_df.groupby('sector').mean(numeric_only=True)[['price_per_sqft', 'built_up_area', 'latitude', 'longitude']]
fig_map = px.scatter_mapbox(group_df, lat='latitude', lon='longitude', size='built_up_area', color='price_per_sqft',
                             color_continuous_scale=px.colors.cyclical.IceFire, mapbox_style='open-street-map', zoom=10,
                             width=1000, height=650, hover_name=group_df.index)
st.plotly_chart(fig_map, use_container_width=True)

# ---------------------------------- Graph 2: Features Wordcloud ----------------------------------
st.subheader('2. Property Features - Wordcloud')
sector_option = wordcloud_df['sector'].dropna().unique().tolist()
sector_option.insert(0, 'overall')
selected_sector = st.selectbox("Select Sector", sector_option)

def get_features(df, sector):
    if sector == 'overall':
        data = df['features']
    else:
        data = df[df['sector'] == sector]['features']
    features = []
    for item in data.dropna():
        try:
            features.extend(ast.literal_eval(item))
        except:
            pass
    return features

features_list = get_features(wordcloud_df, selected_sector)
if features_list:
    wc = WordCloud(width=500, height=300, background_color='white',colormap='tab10').generate(' '.join(features_list))
    fig_wc, ax_wc = plt.subplots(figsize=(6, 3))
    ax_wc.imshow(wc, interpolation='bilinear')
    ax_wc.axis('off')
    st.pyplot(fig_wc)
else:
    st.warning("No features found.")

# ---------------------------------- Graph 3: Area vs Price Scatter ----------------------------------
st.subheader('3. Area vs Price Scatter Plot')
fig1 = px.scatter(new_df, x='built_up_area', y='price', color='bedRoom',
                  title='Price vs Area colored by BHK')
st.plotly_chart(fig1, use_container_width=True)

# ---------------------------------- Graph 4: BHK Pie Chart by Sector ----------------------------------
st.subheader('4. BHK Distribution Pie Chart')
sector_list = new_df['sector'].dropna().unique().tolist()
sector_list.insert(0, 'overall')
sector_selected = st.selectbox("Select Sector for BHK Pie Chart", sector_list)
if sector_selected == 'overall':
    fig2 = px.pie(new_df, names='bedRoom', title='Overall BHK Distribution',width=600, height=600)
else:
    fig2 = px.pie(new_df[new_df['sector'] == sector_selected], names='bedRoom',
                  title=f'BHK Distribution in {sector_selected}',width=600, height=600)
st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------- Graph 5: BHK Boxplot Price ----------------------------------
st.subheader('5. BHK vs Price')
fig3 = px.box(new_df[new_df['bedRoom'] <= 5], x='bedRoom', y='price', title='Price Distribution across BHK')
st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------- Graph 6: Property Type Histogram ----------------------------------
st.subheader('6. Price by Property Type')
fig4, ax4 = plt.subplots(figsize=(6,3))
sns.histplot(new_df[new_df['property_type'] == 'flat']['price'], color='skyblue', label='Flat', ax=ax4)
sns.histplot(new_df[new_df['property_type'] == 'house']['price'], color='salmon', label='House', ax=ax4)
plt.legend()
st.pyplot(fig4)

# ---------------------------------- Graph 7: Heatmap by Sector and Property Type ----------------------------------
st.subheader('7. Sector vs Property Type Price')
pivot_df = new_df.pivot_table(index='sector', columns='property_type', values='price', aggfunc='mean')
fig5, ax5 = plt.subplots(figsize=(10,4))
sns.heatmap(pivot_df, cmap='YlOrRd', linewidths=0.5, ax=ax5)
ax5.set_title('Avg Price by Sector & Property Type')
st.pyplot(fig5)

# ---------------------------------- Graph 8: Bubble Chart - Price vs Luxury score ----------------------------------
st.subheader('8. Price vs Luxury score')
fig6 = px.scatter(new_df, x='luxury_score', y='price', size='bedRoom', color='property_type',
                 title='Price vs luxury score')
st.plotly_chart(fig6, use_container_width=True)

# ---------------------------------- Graph 9: Stacked Area Chart - Age vs Price by Property Type ----------------------------------
st.subheader('9. Price Trend by Age (Stacked Area)')
age_mapping = {
    'New Property': 0,
    'Relatively New': 1,
    'Moderately Old': 2,
    'Old Property': 3,
    'Under Construction': -1
}
new_df['age_category'] = new_df['agePossession'].map(age_mapping)
price_by_age = new_df.groupby(['age_category', 'property_type'])['price'].mean().reset_index()
fig7 = px.area(price_by_age, x='age_category', y='price', color='property_type',
              title='Price by Age Category and Property Type')
st.plotly_chart(fig7, use_container_width=True)

