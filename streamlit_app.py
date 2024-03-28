import streamlit as st
import folium
from streamlit_folium import folium_static

def find_function(path):
    row = indexed_journeys_df.loc[path]
    return row

def plot_map(row):
    m = folium.Map(location=location_a, zoom_start=5)
    for i, val in enumerate(my_row['unique_countries']):
        country = val
        location = (my_row['unique_lats'][i], my_row['unique_longs'][i])
        folium.Marker(location=location, popup=val, icon=folium.Icon(color='blue')).add_to(m)
        if i < len(my_row['unique_countries'])-1:
            location_next = (my_row['unique_lats'][i+1], my_row['unique_longs'][i+1])
            folium.PolyLine(locations=[location, location_next], color='green', weight=3).add_to(m)
    folium_static(m)

def main():
    # Set up your Streamlit app layout
    st.title("Map with Line")

    # Define the coordinates for Location A and Location B
    # These are just example coordinates, replace them with your actual coordinates
    location_a = (40.7128, -74.0060)  # New York City
    location_b = (34.0522, -118.2437)  # Los Angeles

    # Create a Folium map centered at Location A
    m = folium.Map(location=location_a, zoom_start=5)

    # Add markers for Location A and Location B
    folium.Marker(location=location_a, popup="Location A", icon=folium.Icon(color='blue')).add_to(m)
    folium.Marker(location=location_b, popup="Location B", icon=folium.Icon(color='red')).add_to(m)

    # Draw a line between Location A and Location B
    folium.PolyLine(locations=[location_a, location_b], color='green', weight=3).add_to(m)

    # Display the map in the Streamlit app
    folium_static(m)

if __name__ == "__main__":
    main()
