import streamlit as st
import folium
import pandas as pd
from streamlit_folium import folium_static

def find_function(path,indexed_journeys_df):
    row = indexed_journeys_df.loc[path]
    return row

def plot_map(my_row):
    start_loc = (my_row['unique_lats'][0],my_row['unique_longs'][0])
    m = folium.Map(location=start_loc, zoom_start=5)
    for i, val in enumerate(my_row['unique_countries']):
        country = val
        location = (my_row['unique_lats'][i], my_row['unique_longs'][i])
        folium.Marker(location=location, popup=val, icon=folium.Icon(color='blue')).add_to(m)
        if i < len(my_row['unique_countries'])-1:
            location_next = (my_row['unique_lats'][i+1], my_row['unique_longs'][i+1])
            folium.PolyLine(locations=[location, location_next], color='green', weight=3).add_to(m)
    folium_static(m)

def main():
    alt_df = pd.read_hdf('Path_By_Researchers_With_Year.h5')
    journeys_df = pd.read_hdf('author_journeys.h5')
    journeys_df = alt_df
    indexed_journeys_df = journeys_df.set_index('@path', inplace=False)
    # Set up your Streamlit app layout
    st.title('Researcher Migration')
    path = '/0000-0003-4998-7259'
    path = st.text_input("Write Path Here",path)
    row = find_function(path,indexed_journeys_df)
    plot_map(row)

if __name__ == "__main__":
    main()
