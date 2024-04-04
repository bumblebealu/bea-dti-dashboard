import streamlit as st
import folium
import pandas as pd
from streamlit_folium import folium_static
import scipy.sparse

@st.cache
def load_tfidf():
    auths = scipy.sparse.load_npz("transformed_authors.npz")
    titles = scipy.sparse.load_npz("transformed_titles.npz")
    return auths, titles


def find_function(path,indexed_journeys_df):
    row = indexed_journeys_df.loc[path]
    return row

def plot_map(my_row):
    start_loc = (my_row['latitude'][0],my_row['longitude'][0])
    m = folium.Map(location=start_loc, zoom_start=5)
    for i, val in enumerate(my_row['country']):
        country = val
        location = (my_row['latitude'][i], my_row['longitude'][i])
        popup = f"{my_row['title'][i]} {val} {my_row['year'][i]}"
        folium.Marker(location=location, popup=popup, icon=folium.Icon(color='blue')).add_to(m)
        if i < len(my_row['country'])-1:
            location_next = (my_row['latitude'][i+1], my_row['longitude'][i+1])
            folium.PolyLine(locations=[location, location_next], color='green', weight=3).add_to(m)
    folium_static(m)

def main():
    alt_df = pd.read_hdf('Path_By_Researchers_With_Year.h5')
    journeys_df = pd.read_hdf('author_journeys.h5')
    journeys_df = alt_df
    indexed_journeys_df = journeys_df.set_index('@path', inplace=False)

    auths, titles = load_tfidf()
    
    st.title('Researcher Migration')
    path = '/0000-0003-4998-7259'
    path = st.text_input("Write Path Here",path)
    on = st.toggle('Advanced Search')
    if on:
        name = st.text_input("Input researcher name")
        title = st.text_input("Input a paper title to assist the search")
    row = find_function(path,indexed_journeys_df)
    plot_map(row)

if __name__ == "__main__":
    main()
