# 🌊 FloodSense AP - ML Flood Risk Dashboard

**AI-powered Early Warning System** for Andhra Pradesh agricultural zones. Uses Random Forest ML model (82.4% accuracy) on rainfall data from 81+ villages.

## ✨ Features
- **ML Risk Prediction**: Rainfall + antecedent → probabilistic score (Low/Medium/High)
- **AP Geo Coverage**: 81 villages, canals/embankments overlay (robust loader)
- **Ocean UI**: Premium glassmorphism, live map (Folium), risk viz
- **Data**: IMD historical rainfall, synthetic enhanced for demo

## 🚀 Quick Start
```bash
git clone https://github.com/premprasad1707/Ap-flood-detection-system.git
cd Ap-flood-detection-system
# Windows
venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```
→ **http://localhost:8501**

## 📊 Demo Screenshots

| Dashboard | Risk Low | Risk High |
|-----------|----------|----------|
| ![Dashboard](screenshots/dashboard.png) | ![Low Risk](screenshots/ml_risk_low.png) | ![High Risk](screenshots/ml_risk_high.png) |

**Live ML**: Sliders trigger RF predictions. Model: `utils/flood_model.pkl` (train w/ `utils/train_model.py`)

## 🛠 Tech Stack
- **Frontend**: Streamlit + Folium + Custom CSS
- **ML**: scikit-learn RF Classifier
- **Data**: Pandas, GeoPandas, IMD AP rainfall
- **API Ready**: FastAPI backend (`uvicorn backend:app --reload`)

## 🔮 Future
- Real-time IMD API
- Satellite DEM slope/elevation
- Mobile alerts
- District reports

⭐ **Star/Fork** for AP flood monitoring!

[Demo Video](screenshots/) | [Live Repo](https://github.com/premprasad1707/Ap-flood-detection-system)

