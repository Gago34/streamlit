import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import folium_static

# Charger les données
gdf = gpd.read_parquet("maroc.geoparquet")

# Titre de l'application
st.title("Cartographie Thématique par Coordonnées")

# Ajouter une textbox pour rechercher un point par ses coordonnées
search_coords = st.text_input("Rechercher un point par ses coordonnées (format : latitude, longitude)")

if search_coords:
    try:
        lat, lon = map(float, search_coords.split(','))
        searched_point = gdf[(gdf['Latitude'] == lat) & (gdf['Longitude'] == lon)]

        # Créer une carte Folium avec le fond de carte ESRI World Street Map
        m = folium.Map(location=[lat, lon], zoom_start=8, tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}", attr="ESRI World Street Map")

        # Ajouter des cercles sur la carte
        for _, row in searched_point.iterrows():
            folium.Circle(location=[row['Latitude'], row['Longitude']], radius=1000, color='blue', fill=True, fill_color='blue').add_to(m)

        # Afficher la carte
        folium_static(m)

        # Informations sur les colonnes sélectionnées
        st.subheader("Informations sur la colonne sélectionnée")
        st.write(searched_point.describe())

        # Affichage du GeoDataFrame (pour référence)
        st.subheader("GeoDataFrame (pour référence)")
        st.write(searched_point)

    except ValueError:
        st.warning("Format de coordonnées invalide. Utilisez le format : latitude, longitude")
