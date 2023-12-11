import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import folium_static
st.set_page_config(layout="wide")

# Chargement du fichier GeoParquet
file_path = "maroc.geoparquet"
gdf = gpd.read_parquet(file_path)

# Vérifier si le CRS est défini
if gdf.crs is None:
    # Si le CRS n'est pas défini, définissez-le explicitement (WGS84 dans cet exemple)
    gdf = gdf.set_crs("EPSG:4326", allow_override=True)

# Convertir la colonne de date en string
gdf['Propriete4'] = gdf['Propriete4'].astype(str)

# Titre de l'application Streamlit
st.title("Cartographie Thématique avec Folium - Symbole Proportionnel")

# Exclure certaines colonnes de la sélection
columns_to_exclude = ["Propriete1", "Propriete2", "Propriete3", "Propriete4"]
available_columns = [col for col in gdf.columns if col not in columns_to_exclude]

# Sélection de la colonne à cartographier
selected_column = st.selectbox("Sélectionnez la colonne à cartographier", available_columns)

# Obtenez l'étendue géographique du Maroc
min_lon, min_lat, max_lon, max_lat = gdf.geometry.total_bounds

# Calcul du centre
center_lat = (min_lat + max_lat) / 2
center_lon = (min_lon + max_lon) / 2

# Création de la carte thématique avec Folium - Symbole Proportionnel
m = folium.Map(location=[center_lat, center_lon], zoom_start=6)

for idx, row in gdf.iterrows():
    folium.CircleMarker(
        location=[row['geometry'].y, row['geometry'].x],
        radius=row[selected_column] / 5,  # Ajustez le facteur d'échelle au besoin
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.7,
        popup=f"{selected_column}: {row[selected_column]}",
    ).add_to(m)

# Afficher la carte avec Streamlit
folium_static(m, width=1200, height=700)
