import streamlit as st
import pandas as pd
import folium
import requests
from streamlit_folium import folium_static

# Function to load data and preprocess
@st.cache
def load_data():
    df = pd.read_hdf('country_chlor_df.csv')
    return df

@st.cache
def load_geojson():
    return requests.get("https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/world-countries.json").json()

def find_pairs(countries, target_country):
    entering_pairs = []
    leaving_pairs = []
    for i in range(1, len(countries)):
        if countries[i] == target_country and countries[i-1] != target_country:
            entering_pairs.append((countries[i-1], countries[i]))
        elif countries[i-1] == target_country and countries[i] != target_country:
            leaving_pairs.append((countries[i-1], countries[i]))
    return entering_pairs, leaving_pairs

def process_data(df, target_country):
    entering = []
    leaving = []
    for _, row in df.iterrows():
        e, l = find_pairs(row['country'], target_country)
        entering.extend(e)
        leaving.extend(l)
    
    entering_df = pd.DataFrame(entering, columns=['from_country', 'to_country'])
    leaving_df = pd.DataFrame(leaving, columns=['from_country', 'to_country'])

    entering_freq = entering_df['from_country'].value_counts().reset_index(name='frequency')
    leaving_freq = leaving_df['to_country'].value_counts().reset_index(name='frequency')
    
    return entering_freq, leaving_freq

def plot_choropleth(geojson_data, data, title, fill_color):
    m = folium.Map(location=[20, 0], zoom_start=2)
    folium.Choropleth(
        geo_data=geojson_data,
        name=title,
        data=data,
        columns=['index', 'frequency'],
        key_on='feature.properties.name',
        fill_color=fill_color,
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=title
    ).add_to(m)
    folium.LayerControl().add_to(m)
    return m

def main():
    st.title('Choropleth Map for Research Migration')
    
    df = load_data()
    geojson_data = load_geojson()
    
    countries = [
        'Portugal', 'United States of America', 'United Kingdom', 'France',
        'South Africa', 'Italy', 'Japan', 'Denmark', 'Taiwan', 'Russia',
        # Add the remaining countries as needed...
    ]
    
    target_country = st.selectbox('Select a Country', countries)
    
    entering_freq, leaving_freq = process_data(df, target_country)
    
    if st.button('Show Entering Map'):
        m_entering = plot_choropleth(geojson_data, entering_freq, f'Entering {target_country}', 'YlGnBu')
        folium_static(m_entering)
    
    if st.button('Show Leaving Map'):
        m_leaving = plot_choropleth(geojson_data, leaving_freq, f'Leaving {target_country}', 'YlOrRd')
        folium_static(m_leaving)

if __name__ == '__main__':
    main()



# import streamlit as st
# import folium
# import pandas as pd
# from streamlit_folium import folium_static
# import scipy.sparse
# from sklearn.metrics.pairwise import cosine_similarity

# @st.cache
# def load_tfidf():
#     auths = scipy.sparse.load_npz("transformed_authors.npz")
#     titles = scipy.sparse.load_npz("transformed_titles.npz")
#     return auths, titles


# def find_function(path,indexed_journeys_df):
#     row = indexed_journeys_df.loc[path]
#     return row

# def plot_map(my_row):
#     start_loc = (my_row['latitude'][0],my_row['longitude'][0])
#     m = folium.Map(location=start_loc, zoom_start=5)
#     for i, val in enumerate(my_row['country']):
#         country = val
#         location = (my_row['latitude'][i], my_row['longitude'][i])
#         popup = f"{my_row['title'][i]} {val} {my_row['year'][i]}"
#         folium.Marker(location=location, popup=popup, icon=folium.Icon(color='blue')).add_to(m)
#         if i < len(my_row['country'])-1:
#             location_next = (my_row['latitude'][i+1], my_row['longitude'][i+1])
#             folium.PolyLine(locations=[location, location_next], color='green', weight=3).add_to(m)
#     folium_static(m)

# def advanced_find(name, title):
#     name_vector = auths.transform([name])
#     ##title_vector = titles.transform([title])
#     #power_search = st.text_input("Search Papers by Title")
#     #power_vector = trainer.transform([power_search])
#     # word_list = power_search.split(" ") 
#     # word_vector = trainer.transform(word_list) 
#     # st.write(word_vector)
#     # find the cosine similarity between the power search and the first 200 papers
    
#     cos_sim = cosine_similarity(name_vector, tester)
#     # find the index of the paper with the highest cosine similarity
#     matching_index = cos_sim.argmax()
#     # find the indexis of the top 10 papers with the highest cosine similarity
#     top_ten = cos_sim.argsort()[0][-10:]
#     top_ten = top_ten[::-1]
#     top_sim = cos_sim[0][top_ten]
#     # find the title of the paper with the highest cosine similarity
#     matching_data = journeys_df.iloc[matching_index,:]
    
#     # change the index of top_ten_titles to the similarity scores
#     matching_data.index = top_sim
#     matching_data.index.name = "Similarity Score"
#     st.write("Top Ten Results")
#     st.write(matching_data)

# def main():
#     alt_df = pd.read_hdf('Path_By_Researchers_With_Year.h5')
#     journeys_df = pd.read_hdf('author_journeys.h5')
#     journeys_df = alt_df
#     indexed_journeys_df = journeys_df.set_index('@path', inplace=False)

#     auths, titles = load_tfidf()
    
#     st.title('Researcher Migration')
#     path = '/0000-0003-4998-7259'
#     path = st.text_input("Write Path Here",path)
#     on = st.toggle('Advanced Search')
#     if on:
#         name = st.text_input("Input researcher name")
#         title = st.text_input("Input a paper title to assist the search")
#         advanced_find(name, title)
#     row = find_function(path,indexed_journeys_df)
#     plot_map(row)

# if __name__ == "__main__":
#     main()
