import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from datetime import date
from utils.model import calculate_risk, classify_risk
from utils.geo_utils import load_shapefiles, load_rainfall_data

st.set_page_config(
    page_title="FloodSense — AP Early Warning",
    layout="wide",
    page_icon="🌊",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
#  PREMIUM DARK OCEAN DASHBOARD — FULL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

/* ── RESET & BASE ─────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    background-color: #03080F !important;
    color: #C8D8E8 !important;
    font-family: 'Inter', sans-serif !important;
}

/* Animated deep-sea gradient mesh background */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 10% 20%, rgba(0, 80, 160, 0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 90% 80%, rgba(0, 160, 200, 0.12) 0%, transparent 55%),
        radial-gradient(ellipse 50% 40% at 50% 50%, rgba(0, 40, 90, 0.3) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

/* ── SCROLLBAR ───────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #03080F; }
::-webkit-scrollbar-thumb { background: #0A4A7A; border-radius: 3px; }

/* ── TYPOGRAPHY ──────────────────────────────── */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif !important;
    letter-spacing: -0.02em;
}

/* ── MAIN TITLE ──────────────────────────────── */
.main-header {
    padding: 2rem 0 1.5rem 0;
    position: relative;
}
.main-title {
    font-family: 'Outfit', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #E0F4FF 0%, #00C8FF 40%, #0080FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin: 0;
}
.main-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    color: #5A8AAA;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 0.4rem;
    font-weight: 300;
}
.title-badge {
    display: inline-block;
    background: linear-gradient(135deg, #00243A, #003D5C);
    border: 1px solid #005580;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.72rem;
    letter-spacing: 0.15em;
    color: #00C8FF;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 0.8rem;
    font-family: 'Inter', sans-serif;
}
.live-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    background: #00FF88;
    border-radius: 50%;
    margin-right: 6px;
    animation: pulse-dot 1.8s ease-in-out infinite;
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.7); }
}

/* ── DIVIDER ─────────────────────────────────── */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #0A4A7A 30%, #00C8FF 50%, #0A4A7A 70%, transparent);
    margin: 1.2rem 0;
    opacity: 0.6;
}

/* ── GLASS CARDS ─────────────────────────────── */
.glass-card {
    background: linear-gradient(145deg, rgba(8, 25, 48, 0.85), rgba(4, 14, 30, 0.9));
    border: 1px solid rgba(0, 140, 200, 0.18);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    backdrop-filter: blur(12px);
    box-shadow:
        0 0 0 1px rgba(0,200,255,0.04) inset,
        0 8px 32px rgba(0,0,0,0.4),
        0 0 60px rgba(0, 80, 160, 0.06);
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
}
.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,200,255,0.4), transparent);
}

/* ── METRIC CHIPS ────────────────────────────── */
.metric-row {
    display: flex;
    gap: 0.75rem;
    margin-bottom: 1.2rem;
    flex-wrap: wrap;
}
.metric-chip {
    flex: 1;
    min-width: 100px;
    background: linear-gradient(145deg, rgba(0,30,60,0.9), rgba(0,20,45,0.95));
    border: 1px solid rgba(0,150,210,0.2);
    border-radius: 12px;
    padding: 0.9rem 1rem;
    position: relative;
    overflow: hidden;
}
.metric-chip::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 0 0 12px 12px;
}
.metric-chip.rain::after  { background: linear-gradient(90deg, #0055FF, #00C8FF); }
.metric-chip.elev::after  { background: linear-gradient(90deg, #7B2FBE, #C850FF); }
.metric-chip.slope::after { background: linear-gradient(90deg, #FF6B35, #FFB347); }
.metric-chip.date::after  { background: linear-gradient(90deg, #00B894, #00CEC9); }

.metric-label {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: #4A7A9A;
    font-weight: 600;
    margin-bottom: 0.2rem;
    font-family: 'Outfit', sans-serif;
}
.metric-value {
    font-size: 1.4rem;
    font-weight: 700;
    font-family: 'Outfit', sans-serif;
    color: #E0F0FF;
    line-height: 1;
}
.metric-unit {
    font-size: 0.7rem;
    color: #4A7A9A;
    font-weight: 400;
}

/* ── SECTION HEADERS ─────────────────────────── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 1rem;
}
.section-icon {
    width: 28px; height: 28px;
    background: linear-gradient(135deg, #003D5C, #005580);
    border: 1px solid #007AA0;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem;
}
.section-title {
    font-family: 'Outfit', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: #7ABCD4;
}

/* ── RISK OUTPUT CARDS ───────────────────────── */
.risk-output-wrapper {
    margin-top: 0.5rem;
}
.risk-score-display {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.2rem 1.4rem;
    border-radius: 14px;
    margin-bottom: 0.8rem;
    position: relative;
    overflow: hidden;
}
.risk-score-display.high {
    background: linear-gradient(135deg, rgba(180, 20, 20, 0.25), rgba(100, 0, 0, 0.4));
    border: 1px solid rgba(255, 60, 60, 0.35);
    box-shadow: 0 0 30px rgba(255, 30, 30, 0.12), inset 0 0 40px rgba(180,0,0,0.08);
}
.risk-score-display.medium {
    background: linear-gradient(135deg, rgba(180, 140, 0, 0.25), rgba(100, 70, 0, 0.4));
    border: 1px solid rgba(255, 210, 60, 0.35);
    box-shadow: 0 0 30px rgba(255, 180, 0, 0.12), inset 0 0 40px rgba(180,120,0,0.08);
}
.risk-score-display.low {
    background: linear-gradient(135deg, rgba(0, 150, 80, 0.25), rgba(0, 80, 40, 0.4));
    border: 1px solid rgba(0, 230, 120, 0.35);
    box-shadow: 0 0 30px rgba(0, 200, 100, 0.12), inset 0 0 40px rgba(0,150,80,0.08);
}
.risk-label-text {
    font-family: 'Outfit', sans-serif;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    margin-bottom: 0.3rem;
    opacity: 0.8;
}
.risk-level-name {
    font-family: 'Outfit', sans-serif;
    font-size: 1.7rem;
    font-weight: 800;
    line-height: 1;
}
.risk-level-name.high   { color: #FF6060; text-shadow: 0 0 20px rgba(255,60,60,0.5); }
.risk-level-name.medium { color: #FFD060; text-shadow: 0 0 20px rgba(255,200,0,0.5); }
.risk-level-name.low    { color: #40E880; text-shadow: 0 0 20px rgba(0,220,100,0.5); }

.risk-score-number {
    font-family: 'Outfit', sans-serif;
    font-size: 3.5rem;
    font-weight: 800;
    line-height: 1;
    opacity: 0.25;
}
.risk-score-number.high   { color: #FF4040; }
.risk-score-number.medium { color: #FFD000; }
.risk-score-number.low    { color: #00E870; }

/* ── RISK BAR ────────────────────────────────── */
.risk-bar-container {
    background: rgba(255,255,255,0.05);
    border-radius: 100px;
    height: 8px;
    margin: 0.6rem 0 0.4rem 0;
    overflow: hidden;
    position: relative;
}
.risk-bar-fill {
    height: 100%;
    border-radius: 100px;
    transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
}
.risk-bar-fill.high {
    background: linear-gradient(90deg, #FF2020, #FF6060);
    box-shadow: 0 0 10px rgba(255,40,40,0.6);
}
.risk-bar-fill.medium {
    background: linear-gradient(90deg, #FF8800, #FFD060);
    box-shadow: 0 0 10px rgba(255,160,0,0.6);
}
.risk-bar-fill.low {
    background: linear-gradient(90deg, #00AA50, #40E880);
    box-shadow: 0 0 10px rgba(0,200,90,0.6);
}
.risk-bar-labels {
    display: flex;
    justify-content: space-between;
    font-size: 0.62rem;
    color: #3A6A8A;
    letter-spacing: 0.08em;
    font-family: 'Outfit', sans-serif;
    text-transform: uppercase;
    margin-top: 0.25rem;
}

/* ── ALERT BOX ───────────────────────────────── */
.alert-box {
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    font-size: 0.85rem;
    line-height: 1.5;
    font-family: 'Inter', sans-serif;
    display: flex;
    align-items: flex-start;
    gap: 0.7rem;
}
.alert-box.high   { background: rgba(180,20,20,0.15); border: 1px solid rgba(255,60,60,0.2); color: #FFB0B0; }
.alert-box.medium { background: rgba(180,130,0,0.15); border: 1px solid rgba(255,200,60,0.2); color: #FFE0A0; }
.alert-box.low    { background: rgba(0,130,70,0.15);  border: 1px solid rgba(0,200,100,0.2); color: #A0FFD0; }
.alert-icon { font-size: 1.1rem; margin-top: 1px; flex-shrink: 0; }

/* ── LOCATION INFO ───────────────────────────── */
.location-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(0, 60, 100, 0.5);
    border: 1px solid rgba(0, 150, 210, 0.25);
    border-radius: 20px;
    padding: 5px 12px;
    font-size: 0.78rem;
    color: #7ABCD4;
    font-family: 'Inter', sans-serif;
    margin-bottom: 0.8rem;
}
.location-dot {
    width: 6px; height: 6px;
    background: #00C8FF;
    border-radius: 50%;
    animation: pulse-dot 2s ease-in-out infinite;
}

/* ── MAP CONTAINER ───────────────────────────── */
.map-wrapper {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(0, 140, 200, 0.2);
    box-shadow:
        0 0 0 1px rgba(0,200,255,0.04) inset,
        0 16px 48px rgba(0,0,0,0.5),
        0 0 80px rgba(0, 60, 120, 0.08);
}

/* ── STREAMLIT WIDGET OVERRIDES ──────────────── */

/* Slider track */
[data-testid="stSlider"] > div > div > div > div {
    background: linear-gradient(90deg, #0066CC, #00C8FF) !important;
}

/* Slider thumb */
[data-testid="stSlider"] [role="slider"] {
    background: #00C8FF !important;
    border: 2px solid #004488 !important;
    box-shadow: 0 0 10px rgba(0,200,255,0.4) !important;
}

/* Number inputs */
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input {
    background: rgba(0, 20, 45, 0.8) !important;
    border: 1px solid rgba(0, 140, 200, 0.3) !important;
    border-radius: 8px !important;
    color: #C8D8E8 !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stNumberInput"] input:focus,
[data-testid="stDateInput"] input:focus {
    border-color: rgba(0, 200, 255, 0.6) !important;
    box-shadow: 0 0 12px rgba(0,200,255,0.15) !important;
}

/* Radio buttons */
[data-testid="stRadio"] label {
    background: rgba(0, 20, 45, 0.7) !important;
    border: 1px solid rgba(0, 140, 200, 0.2) !important;
    border-radius: 8px !important;
    padding: 4px 10px !important;
    font-size: 0.78rem !important;
    color: #7ABCD4 !important;
    transition: all 0.2s ease !important;
}
[data-testid="stRadio"] label:hover {
    border-color: rgba(0, 200, 255, 0.5) !important;
    color: #00C8FF !important;
}
[data-testid="stRadio"] input:checked + div {
    color: #00C8FF !important;
}

/* Checkbox */
[data-testid="stCheckbox"] label {
    color: #7ABCD4 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
}

/* Selectbox / multiselect */
[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {
    background: rgba(0, 20, 45, 0.8) !important;
    border: 1px solid rgba(0, 140, 200, 0.3) !important;
    border-radius: 8px !important;
    color: #C8D8E8 !important;
}

/* ── PREDICT BUTTON ──────────────────────────── */
[data-testid="stButton"] > button {
    width: 100% !important;
    background: linear-gradient(135deg, #0050A0, #007ACC) !important;
    color: #E0F4FF !important;
    border: 1px solid rgba(0, 180, 255, 0.35) !important;
    border-radius: 10px !important;
    padding: 0.75rem 1rem !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px rgba(0, 100, 200, 0.35) !important;
    cursor: pointer !important;
    position: relative !important;
    overflow: hidden !important;
}
[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #0070C8, #00AAFF) !important;
    border-color: rgba(0, 220, 255, 0.6) !important;
    box-shadow: 0 6px 28px rgba(0, 150, 255, 0.5), 0 0 0 1px rgba(0,200,255,0.2) inset !important;
    transform: translateY(-1px) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0px) !important;
}

/* ── INFO / WARNING / SUCCESS BOXES ──────────── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border: none !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.84rem !important;
}

/* ── SPINNER ─────────────────────────────────── */
.stSpinner > div {
    border-top-color: #00C8FF !important;
}

/* ── LABELS ABOVE SLIDERS / INPUTS ───────────── */
label, [data-testid="stWidgetLabel"] p {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.8rem !important;
    color: #5A8AAA !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
}

/* ── COLUMN PADDING FIX ──────────────────────── */
[data-testid="stHorizontalBlock"] > div {
    padding: 0 0.5rem !important;
}
[data-testid="stHorizontalBlock"] > div:first-child { padding-left: 0 !important; }
[data-testid="stHorizontalBlock"] > div:last-child  { padding-right: 0 !important; }

/* ── FOOTER ──────────────────────────────────── */
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
header { visibility: hidden; }

/* ── LEGEND ──────────────────────────────────── */
.map-legend {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    padding: 0.75rem 0 0.25rem 0;
}
.legend-item {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.75rem;
    color: #5A8AAA;
    font-family: 'Inter', sans-serif;
}
.legend-line {
    width: 20px;
    height: 3px;
    border-radius: 2px;
}
.legend-circle {
    width: 10px; height: 10px;
    border-radius: 50%;
    border: 2px solid currentColor;
    opacity: 0.6;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <div class="title-badge"><span class="live-dot"></span>Live System — Andhra Pradesh</div>
    <div class="main-title">FloodSense<br>Risk Intelligence</div>
    <div class="main-subtitle">Early Warning System · Agricultural Zone Monitor · AP 2024</div>
</div>
<div class="section-divider"></div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DATA LOADING
# ─────────────────────────────────────────────
with st.spinner("Initialising geospatial engine..."):
    canals, embankments = load_shapefiles()
    rainfall_df = load_rainfall_data()

# ─────────────────────────────────────────────
#  LAYOUT
# ─────────────────────────────────────────────
col1, col2 = st.columns([1, 2.1], gap="medium")

# ────────────────────  LEFT PANEL  ─────────────────────
with col1:

    # ── CITY SELECTION ──
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">📍</div>
        <span class="section-title">Location Selection</span>
    </div>""", unsafe_allow_html=True)

    cities = {
        # Coastal Andhra
        "Visakhapatnam": (17.6868, 83.2185),
        "Vijayawada": (16.5062, 80.6480),
        "Guntur": (16.3067, 80.4365),
        "Nellore": (14.4426, 79.9865),
        "Rajahmundry": (17.0005, 81.8040),
        "Kakinada": (16.9891, 82.2475),
        "Eluru": (16.7107, 81.1031),
        "Machilipatnam": (16.1786, 81.1352),
        "Ongole": (15.5057, 80.0499),
        "Bhimavaram": (16.5448, 81.5212),
        "Tenali": (16.2366, 80.6405),
        # North Coastal
        "Srikakulam": (18.3000, 83.9000),
        "Vizianagaram": (18.1133, 83.3977),
        # Rayalaseema
        "Kurnool": (15.8281, 78.0373),
        "Tirupati": (13.6288, 79.4192),
        "Kadapa": (14.4673, 78.8242),
        "Anantapur": (14.6819, 77.6006),
        "Chittoor": (13.2172, 79.1003),
        "Nandyal": (15.4856, 78.4839),
        "Hindupur": (13.8290, 77.4915),
        "Adoni": (15.6294, 77.2745),
        "Dharmavaram": (14.4140, 77.7176),
        "Guntakal": (15.1674, 77.3828)
    }

    selected_city = st.selectbox("Select City", list(cities.keys()), label_visibility="collapsed")
    lat, lon = cities[selected_city]
    
    # Defaults for manual input
    default_rain, default_prev = 50.0, 20.0

    st.markdown(f"""
    <div class="location-pill">
        <div class="location-dot"></div>
        {selected_city} &nbsp;·&nbsp; Lat {lat:.4f} &nbsp;·&nbsp; Lon {lon:.4f}
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ── DATE & MONTH ──
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">📅</div>
        <span class="section-title">Temporal Settings</span>
    </div>""", unsafe_allow_html=True)

    pred_date = st.date_input("Prediction Date", date.today(), label_visibility="collapsed")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ── PARAMETER SLIDERS ──
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🌧️</div>
        <span class="section-title">Hydrological Parameters</span>
    </div>""", unsafe_allow_html=True)

    rainfall      = st.slider("Current Rainfall (mm)",  0.0, 300.0, default_rain,  step=0.5)
    prev_rainfall = st.slider("Antecedent Rainfall (mm)", 0.0, 300.0, default_prev, step=0.5)
    elevation     = st.slider("Elevation (m)",          0.0, 500.0, 25.0,          step=1.0)
    slope         = st.slider("Terrain Slope (°)",      0.0, 10.0,  2.0,           step=0.1)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ── EXACT OVERRIDES ──
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🎯</div>
        <span class="section-title">Precision Overrides</span>
    </div>""", unsafe_allow_html=True)

    oc1, oc2 = st.columns(2)
    with oc1:
        exact_rainfall = st.number_input("Rainfall (mm)", value=round(rainfall, 2), format="%.2f")
    with oc2:
        exact_slope    = st.number_input("Slope (°)",     value=round(slope, 2),    format="%.2f")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── PREDICT BUTTON ──
    predict = st.button("⚡  Run Flood Risk Analysis")

    # ── RESULTS ──
    if predict:
        final_rain  = exact_rainfall if exact_rainfall != rainfall else rainfall
        final_slope = exact_slope    if exact_slope != slope       else slope

        score = calculate_risk(final_rain, prev_rainfall, elevation, final_slope)
        level = classify_risk(score)
        lvl   = level.lower()

        # Score bar fill percentage (score presumably 0–100)
        bar_pct = min(100, max(0, score))

        alert_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}[lvl]
        alert_msg  = {
            "high":   "Critical accumulation detected. Proximity to water bodies combined with terrain profile indicates imminent inundation risk. Immediate evacuation advisory recommended.",
            "medium": "Elevated monitoring required. Drainage systems may be compromised. Coordinate with district disaster management for pre-positioning resources.",
            "low":    "Conditions are within safe parameters. Continue passive monitoring. No immediate action required."
        }[lvl]

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">📊</div>
            <span class="section-title">Risk Assessment Output</span>
        </div>""", unsafe_allow_html=True)

        # Score card
        st.markdown(f"""
        <div class="risk-score-display {lvl}">
            <div>
                <div class="risk-label-text">Flood Risk Level</div>
                <div class="risk-level-name {lvl}">{level}</div>
                <div style="margin-top:0.3rem; font-size:0.75rem; color: rgba(255,255,255,0.35);
                            font-family:'Inter',sans-serif;">Score computed at {pred_date}</div>
            </div>
            <div class="risk-score-number {lvl}">{score:.0f}</div>
        </div>

        <div style="padding: 0 0.2rem;">
            <div class="risk-bar-container">
                <div class="risk-bar-fill {lvl}" style="width: {bar_pct}%;"></div>
            </div>
            <div class="risk-bar-labels">
                <span>Safe</span><span>Moderate</span><span>Critical</span>
            </div>
        </div>

        <div style="margin-top:0.8rem;">
            <div class="alert-box {lvl}">
                <span class="alert-icon">{alert_icon}</span>
                <span>{alert_msg}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Parameter summary chips
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-chip rain">
                <div class="metric-label">Rainfall</div>
                <div class="metric-value">{final_rain:.1f}<span class="metric-unit"> mm</span></div>
            </div>
            <div class="metric-chip elev">
                <div class="metric-label">Elevation</div>
                <div class="metric-value">{elevation:.0f}<span class="metric-unit"> m</span></div>
            </div>
            <div class="metric-chip slope">
                <div class="metric-label">Slope</div>
                <div class="metric-value">{final_slope:.1f}<span class="metric-unit">°</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ────────────────────  RIGHT PANEL  ────────────────────
with col2:

    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🗺️</div>
        <span class="section-title">Geospatial Context — Andhra Pradesh</span>
    </div>""", unsafe_allow_html=True)

    # Legend
    st.markdown("""
    <div class="map-legend">
        <div class="legend-item">
            <div class="legend-line" style="background:#00BFFF;"></div>
            <span>Canal Network</span>
        </div>
        <div class="legend-item">
            <div class="legend-line" style="background:#FF8C00;"></div>
            <span>Embankments</span>
        </div>
        <div class="legend-item">
            <div class="legend-circle" style="color:#FF4444; border-color:#FF4444;"></div>
            <span>Assessment Zone (8 km radius)</span>
        </div>
        <div class="legend-item">
            <div style="width:10px; height:10px; background:#FF4444; border-radius:50%;"></div>
            <span>Assessment Point</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Build map
    m = folium.Map(
        location=[lat, lon],
        zoom_start=8,
        tiles='CartoDB dark_matter',
        prefer_canvas=True
    )

    if canals is not None:
        folium.GeoJson(
            canals,
            name="Canals",
            style_function=lambda x: {
                'color': '#00BFFF',
                'weight': 2.2,
                'opacity': 0.85
            }
        ).add_to(m)

    if embankments is not None:
        folium.GeoJson(
            embankments,
            name="Embankments",
            style_function=lambda x: {
                'color': '#FF8C00',
                'weight': 2.2,
                'opacity': 0.85
            }
        ).add_to(m)

    # Outer glow ring
    folium.Circle(
        location=[lat, lon],
        radius=12000,
        color='#FF4444',
        fill=True,
        fill_color='#FF4444',
        fill_opacity=0.04,
        weight=0,
        tooltip="Outer Monitoring Zone"
    ).add_to(m)

    # Zone of interest
    folium.Circle(
        location=[lat, lon],
        radius=8000,
        color='#FF4444',
        fill=True,
        fill_color='#FF2222',
        fill_opacity=0.12,
        weight=1.5,
        dash_array='6 4',
        tooltip="Assessment Zone — 8km Radius"
    ).add_to(m)

    # Location marker with custom popup
    popup_html = f"""
    <div style='font-family:sans-serif; background:#0b1c2c; color:#00e5ff;
                border-radius:8px; padding:10px 14px; min-width:180px;
                border:1px solid #0A4A7A; font-size:13px;'>
        <b style='font-size:14px;'>📍 Assessment Point</b><br>
        <span style='color:#7ABCD4; font-size:11px;'>Lat: {lat:.4f} · Lon: {lon:.4f}</span><br><br>
        <div style='display:flex; gap:8px; flex-wrap:wrap;'>
            <span style='background:#001830; border-radius:4px; padding:3px 8px;'>🌧 {default_rain:.1f} mm</span>
            <span style='background:#001830; border-radius:4px; padding:3px 8px;'>⛰ {elevation:.0f} m</span>
        </div>
    </div>
    """

    folium.Marker(
        [lat, lon],
        popup=folium.Popup(popup_html, max_width=240),
        tooltip="Assessment Location — Click for details",
        icon=folium.Icon(color="red", icon="tint", prefix="fa")
    ).add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)

    st.markdown('<div class="map-wrapper">', unsafe_allow_html=True)
    st_folium(m, width=None, height=598, returned_objects=[], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── BOTTOM INFO ROW ──
    st.markdown("<br>", unsafe_allow_html=True)
    bi1, bi2, bi3 = st.columns(3)

    with bi1:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding: 1rem;">
            <div class="metric-label">Prediction Date</div>
            <div class="metric-value" style="font-size:1.4rem;">{pred_date.strftime("%d %b")}</div>
            <div style="font-size:0.72rem; color:#3A6A8A; margin-top:0.2rem;">{pred_date.year}</div>
        </div>""", unsafe_allow_html=True)

    with bi2:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding: 1rem;">
            <div class="metric-label">Antecedent Rain</div>
            <div class="metric-value" style="font-size:1.6rem;">{default_prev:.1f}<span class="metric-unit"> mm</span></div>
            <div style="font-size:0.72rem; color:#3A6A8A; margin-top:0.2rem;">Prior period</div>
        </div>""", unsafe_allow_html=True)

    with bi3:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding: 1rem;">
            <div class="metric-label">Terrain Slope</div>
            <div class="metric-value" style="font-size:1.6rem;">{slope:.1f}<span class="metric-unit">°</span></div>
            <div style="font-size:0.72rem; color:#3A6A8A; margin-top:0.2rem;">Current input</div>
        </div>""", unsafe_allow_html=True)
