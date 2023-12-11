import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import folium_static

# Charger les données
gdf = gpd.read_parquet("maroc.geoparquet")

# Titre de l'application
st.title("Cartographie Thématique par Coordonnées")

# Créer une carte Folium de base avec le fond de carte ESRI World Street Map
m = folium.Map(location=[gdf["Latitude"].mean(), gdf["Longitude"].mean()], zoom_start=8,
               tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
               attr="ESRI World Street Map")

# Possibilité de filtrer les données
attribute_filters = st.text_area("Filtrer par attribut (ex: Propriete2 > 50)\nUtilisez une condition par ligne")

# Diviser les conditions attributaires en une liste
attribute_conditions = attribute_filters.split('\n')

# Appliquer les filtres attributaires
if attribute_filters.strip():  # Check if attribute_filters is not empty after stripping whitespace
    try:
        filtered_gdf = gdf
        for condition in attribute_conditions:
            filtered_gdf = filtered_gdf.query(condition)

        # Ajouter les cercles filtrés sur la carte
        for _, row in filtered_gdf.iterrows():
            folium.Circle(
                location=[row['Latitude'], row['Longitude']],
                radius=500,  # Adjust the radius as needed
                popup=str(row),  # Use the entire row as popup content
                color='blue',  # Set the circle color
                fill=True,
                fill_color='blue',  # Set the fill color
            ).add_to(m)

    except pd.errors.ParserError as e:
        st.warning(f"Erreur de syntaxe dans la requête attributaire : {str(e)}")

# Afficher la carte
folium_static(m, width=1200, height=700)
# Affichage du GeoDataFrame (pour référence)
st.subheader("GeoDataFrame (pour référence)") 
st.write(filtered_gdf)  # Display the filtered GeoDataFrame