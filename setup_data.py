import os
import shutil
import pandas as pd

def main():
    os.makedirs('data', exist_ok=True)
    
    # 1. Move Canals and Embankments to data/ if they exist in the root
    for folder in ['Canals', 'Embankments']:
        if os.path.exists(folder):
            print(f"Moving {folder} to data/{folder}...")
            shutil.move(folder, f"data/{folder}")
        elif os.path.exists(f"data/{folder}"):
            print(f"Folder data/{folder} already exists.")
        else:
            print(f"Warning: {folder} not found in root or data/ directory!")
            
    # 2. Process rainfall data
    source_rainfall_file = 'IMD_AP_Historical Rain Fall/AP_Village_Daily_Rainfall_21_r.csv'
    target_rainfall_file = 'data/rainfall.csv'
    
    if os.path.exists(source_rainfall_file):
        print(f"Processing {source_rainfall_file} into {target_rainfall_file}...")
        # Read 5000 valid, sequential rows
        df = pd.read_csv(source_rainfall_file, nrows=10000)
        
        df_sample = pd.DataFrame()
        df_sample['location'] = df['district'] + ' - ' + df['village']
        df_sample['latitude'] = df['centroid_lat']
        df_sample['longitude'] = df['centroid_lon']
        df_sample['rainfall'] = df['rainfall_mm']
        df_sample['prev_rainfall'] = df['rainfall_mm'].shift(1).fillna(0.0)
        
        # Drop rows with NAs (especially for coordinates or rainfall)
        df_sample.dropna(subset=['latitude', 'longitude', 'rainfall', 'location'], inplace=True)
        
        # Keep only valid coordinates for AP generally if there are weird outliers
        # AP is roughly between Lat 12-20, Lon 76-85
        df_sample = df_sample[(df_sample['latitude'] > 12) & (df_sample['latitude'] < 20) &
                              (df_sample['longitude'] > 76) & (df_sample['longitude'] < 85)]
                              
        # Take exactly 5000 rows
        df_sample = df_sample.head(5000)
        
        df_sample.to_csv(target_rainfall_file, index=False)
        print(f"Wrote {len(df_sample)} records to {target_rainfall_file}.")
    else:
        print(f"Error: Could not find {source_rainfall_file}")

if __name__ == '__main__':
    main()
