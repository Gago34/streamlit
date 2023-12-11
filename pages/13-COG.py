import streamlit as st
import leafmap.foliumap as leafmap
import os

st.set_page_config(layout="wide")

# Sélection du jour
selected_day = st.slider("Sélectionnez le jour", -6, 0, -1)

# Sélection de l'attribut
selected_attribute = st.selectbox("Choisissez l'attribut", ["Attibut1", "Attibut2", "Attibut3"])

# Construction du chemin du fichier image
image_path = os.path.join("COG", f"{selected_attribute}Jour{selected_day}_cog.tif")

# Création de la carte Leaflet
legend_dict = {
    "Faible": "#f1eef6",
    "Moyen": "#bdc9e1",
    "Fort": "#74a9cf",
    "Tres fort": "#0570b0",
}

m = leafmap.Map()
style = {
    'position': 'fixed',
    'z-index': '9999',
    'border': '2px solid grey',
    'background-color': 'rgba(255, 255, 255, 0.8)',
    'border-radius': '10px',
    'padding': '5px',
    'font-size': '14px',
    'bottom': '20px',
    'right': '5px',
}

m.add_legend(
    title='Legende', legend_dict=legend_dict, draggable=False, style=style
)

m.add_raster(image_path, colormap='terrain', layer_name='carte')

# Affichage de la carte dans Streamlit
m.to_streamlit(height=700)
