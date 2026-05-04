import geopandas as gpd
import os
import streamlit as st

@st.cache_data
def load_shapefiles(canals_path="data/Canals", embankments_path="data/Embankments"):
    """
    Load Canals and Embankments shapefiles using GeoPandas.
    Mock if empty/permission denied (for demo).
    """
    canals = None
    embankments = None
    
    try:
        if os.path.exists(canals_path) and os.path.isdir(canals_path):
            # Try to find .shp
            shp_file = None
            for f in os.listdir(canals_path):
                if f.endswith('.shp'):
                    shp_file = os.path.join(canals_path, f)
                    break
            if shp_file:
                canals = gpd.read_file(shp_file)
                if canals.crs is None:
                    canals = canals.set_crs(epsg=4326)
    except Exception as e:
        print(f'Canals load failed ({e}): using mock')
        canals = None
    
    try:
        if os.path.exists(embankments_path) and os.path.isdir(embankments_path):
            shp_file = None
            for f in os.listdir(embankments_path):
                if f.endswith('.shp'):
                    shp_file = os.path.join(embankments_path, f)
                    break
            if shp_file:
                embankments = gpd.read_file(shp_file)
                if embankments.crs is None:
                    embankments = embankments.set_crs(epsg=4326)
    except Exception as e:
        print(f'Embankments load failed ({e}): using mock')
        embankments = None
        
    return canals, embankments

@st.cache_data
def load_rainfall_data(csv_path="data/rainfall.csv"):
    import pandas as pd
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        return df
    return None
