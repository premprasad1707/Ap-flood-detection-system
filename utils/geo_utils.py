import geopandas as gpd
import os
import streamlit as st

@st.cache_data
def load_shapefiles(canals_path="data/Canals", embankments_path="data/Embankments"):
    """
    Load Canals and Embankments shapefiles using GeoPandas.
    Fixes CRS to epsg=4326 for Folium compatibility.
    """
    
    canals = None
    embankments = None
    
    if os.path.exists(canals_path):
        canals = gpd.read_file(canals_path)
        # Assume CRS is already correct to speed up loading
        if canals.crs is None:
            canals = canals.set_crs(epsg=4326)
            
    if os.path.exists(embankments_path):
        embankments = gpd.read_file(embankments_path)
        # Assume CRS is already correct to speed up loading
        if embankments.crs is None:
            embankments = embankments.set_crs(epsg=4326)
            
    return canals, embankments

@st.cache_data
def load_rainfall_data(csv_path="data/rainfall.csv"):
    import pandas as pd
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        return df
    return None
