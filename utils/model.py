import joblib
import numpy as np

try:
    model = joblib.load('flood_model.pkl')
    scaler = joblib.load('scaler.pkl')
    ML_MODEL_AVAILABLE = True
except:
    ML_MODEL_AVAILABLE = False
    model = scaler = None

def calculate_risk(rainfall, prev_rainfall, elevation=25.0, slope=2.0):
    if ML_MODEL_AVAILABLE:
        features = scaler.transform([[rainfall, prev_rainfall]])
        risk_prob = model.predict_proba(features)[0][1]  # High risk prob
        score = risk_prob * 100
    else:
        # Fallback rule-based
        score = (
            float(rainfall) * 0.5 +
            float(prev_rainfall) * 0.3 +
            max(0, 100 - float(elevation)) * 0.1 +
            max(0, 10 - float(slope)) * 0.1
        )
    return score

def classify_risk(score):
    if score > 70:
        return "High"
    elif score > 40:
        return "Medium"
    else:
        return "Low"
    
print('Flood model loaded' if ML_MODEL_AVAILABLE else 'Using rule-based fallback')
