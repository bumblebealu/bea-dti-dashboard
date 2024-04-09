import streamlit as st
import pandas as pd
import folium
import requests
from streamlit_folium import folium_static

# Function to load data and preprocess
@st.cache
def load_data():
    df = pd.read_csv('country_chlor_df.csv')
    return df

@st.cache
def load_geojson():
    return requests.get("https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/world-countries.json").json()

def find_pairs(countries, target_country):
    entering_pairs = []
    leaving_pairs = []
    for i in range(1, len(countries)):
        if countries[i] == target_country and countries[i-1] != target_country:
            entering_pairs.append(countries[i-1])
        elif countries[i-1] == target_country and countries[i] != target_country:
            leaving_pairs.append(countries[i])
    return entering_pairs, leaving_pairs

def process_data(df, target_country):
    entering = []
    leaving = []
    for _, row in df.iterrows():
        e, l = find_pairs(row['country'], target_country)
        entering.extend(e)
        leaving.extend(l)
    
    entering_freq = pd.Series(entering).value_counts().reset_index(name='frequency')
    leaving_freq = pd.Series(leaving).value_counts().reset_index(name='frequency')
    entering_freq['country'] = entering_freq['from_country']
    leaving_freq['country'] = leaving_freq['to_country']
    entering_freq['entering_frequency'] = entering_freq['frequency']
    leaving_freq['leaving_frequency'] = leaving_freq['frequency']

    merged_df = pd.merge(
        entering_freq[['country', 'entering_frequency']],
        leaving_freq[['country', 'leaving_frequency']],
        on='country',
        how='outer'
    ).fillna(0) 

    merged_df['net_frequency'] = merged_df['entering_frequency'] - merged_df['leaving_frequency']
    net_df = merged_df[['country', 'net_frequency']]

    frequency_entering_dict = entering_freq.set_index('from_country')['frequency'].to_dict()
    frequency_leaving_dict = leaving_freq.set_index('to_country')['frequency'].to_dict()
    frequency_net_dict = net_df.set_index('country')['net_frequency'].to_dict()

    return frequency_entering_dict, frequency_leaving_dict, frequency_net_dict

def plot_choropleth(geojson_data, entering_dict, leaving_dict, net_dict, target_country):
    m = folium.Map(location=[20, 0], zoom_start=2)

    folium.Choropleth(
        geo_data=geojson_data,
        name=f'Entering {target_country}',
        data=entering_dict,
        key_on='feature.properties.name',
        fill_color='YlGnBu',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f'Entering {target_country}'
    ).add_to(m)

    folium.Choropleth(
        geo_data=geojson_data,
        name=f'Leaving {target_country}',
        data=leaving_dict,
        key_on='feature.properties.name',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f'Leaving {target_country}'
    ).add_to(m)

    folium.Choropleth(
        geo_data=geojson_data,
        name=f'Net Movement in relation to {target_country}',
        data=net_dict,
        key_on='feature.properties.name',
        fill_color='PiYG',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f'Net Movement in relation to {target_country}'
    ).add_to(m)

    folium.LayerControl().add_to(m)
    return m

def main():
    st.title('Choropleth Map for Research Migration')
    
    df = load_data()
    geojson_data = load_geojson()
    
    countries = [
        'Portugal', 'United States of America', 'United Kingdom', 'France',
        # Add the remaining countries as needed...
    ]
    
    target_country = st.selectbox('Select a Country', countries)
    if target_country:
        entering_dict, leaving_dict, net_dict = process_data(df, target_country)
        m = plot_choropleth(geojson_data, entering_dict, leaving_dict, net_dict, target_country)
        folium_static(m)

if __name__ == '__main__':
    main()
