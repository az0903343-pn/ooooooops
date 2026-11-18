import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import urllib.parse
import re

st.set_page_config(page_title="VEHICLE FINDER | AI Edge", page_icon="🚀", layout="wide")

# --- CATEGORY ICONS & ADVANTAGE DETAILS ---
CAT_ICONS = {
    'Cycle': '🚲',
    'Petrol Bike': '🏍️',
    'Rickshaw': '🛺',
    'Car': '🚗',
    'Van': '🚐',
    'Truck': '🚚',
    'Yacht / Boat': '🛥️',
    'Helicopter': '🚁'
}

DETAILED_ADVANTAGES = {
    'Cycle': [
        "Zero fuel expense & 100% eco-friendly travel",
        "Improves daily cardiovascular health & fitness",
        "No license, registration, or traffic jam delays"
    ],
    'Petrol Bike': [
        "Beats heavy city traffic with nimble handling",
        "Ultra-low fuel consumption (40–65 km/l)",
        "Lowest spare parts & maintenance cost"
    ],
    'Rickshaw': [
        "High daily commercial income & passenger capacity",
        "Easy U-turns in narrow city streets",
        "Affordable CNG/Petrol dual-fuel running cost"
    ],
    'Car': [
        "All-weather climate-controlled family comfort",
        "High crash safety, airbags & highway stability",
        "Strong market resale value & long-distance ease"
    ],
    'Van': [
        "Spacious 7 to 15-seater cabin for big families",
        "Massive luggage space for tours & commercial use",
        "Sliding doors for effortless entry & exit"
    ],
    'Truck': [
        "Heavy-duty torque for multi-ton cargo transport",
        "Built on reinforced chassis for rough highways",
        "High return on investment for logistics business"
    ],
    'Yacht / Boat': [
        "Private luxury marine cruising & ocean parties",
        "Panoramic sea views with onboard cabin comfort",
        "High-prestige lifestyle & charter rental asset"
    ],
    'Helicopter': [
        "Zero road traffic — fly directly point-to-point",
        "Vertical takeoff & landing (no airport runway needed)",
        "Fastest VIP executive & emergency air transport"
    ]
}

# --- CUSTOM CSS: GCORE ANIMATION + CORNER CHATBOT + ADVANCED CONTROLS ---
st.markdown("""
<style>
@import url('https://googleapis.com');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #08080A;
    color: #FFFFFF;
}

@keyframes gcoreZoomIn {
    0% { opacity: 0; transform: scale(0.88) translateY(20px); }
    100% { opacity: 1; transform: scale(1) translateY(0); }
}

.gcore-intro {
    background: radial-gradient(circle at center, rgba(255, 85, 0, 0.32) 0%, #0D0D11 72%);
    border: 1px solid rgba(255, 85, 0, 0.45);
    border-radius: 22px;
    padding: 36px 20px;
    text-align: center;
    animation: gcoreZoomIn 0.9s ease-out forwards;
    margin-bottom: 24px;
    box-shadow: 0 0 35px rgba(255, 85, 0, 0.25);
}

.gcore-logo-text {
    font-size: 3.3rem;
    font-weight: 900;
    letter-spacing: 3px;
    background: linear-gradient(90deg, #FFFFFF 20%, #FF5500 80%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}

.stat-card {
    background: #121217;
    border: 1px solid #26262E;
    border-radius: 16px;
    padding: 18px;
    text-align: center;
    transition: all 0.3s ease;
}
.stat-card:hover {
    border-color: #FF5500;
    transform: translateY(-4px);
}

.vehicle-card {
    background: linear-gradient(145deg, #15151C, #0E0E13);
    border: 1px solid #2A2A35;
    border-radius: 18px;
    padding: 22px;
    transition: all 0.35s ease;
    margin-bottom: 16px;
}
.vehicle-card:hover {
    border-color: #FF5500;
    transform: translateY(-6px);
    box-shadow: 0 12px 30px rgba(255, 85, 0, 0.25);
}

.visit-btn {
    display: inline-block;
    background: linear-gradient(90deg, #FF5500, #FF7722);
    color: #FFFFFF !important;
    text-decoration: none;
    padding: 10px 18px;
    border-radius: 10px;
    font-weight: 700;
    font-size: 0.9rem;
    margin-top: 12px;
    transition: 0.3s;
}
.visit-btn:hover {
    box-shadow: 0 0 18px rgba(255, 85, 0, 0.85);
    transform: scale(1.03);
}

/* FIXED BOTTOM-RIGHT FLOATING CORNER CHATBOT */
div[data-testid="stPopover"] {
    position: fixed !important;
    bottom: 28px !important;
    right: 28px !important;
    z-index: 999999 !important;
    width: auto !important;
}
div[data-testid="stPopover"] > button {
    background: linear-gradient(135deg, #FF5500, #7C3AED) !important;
    color: white !important;
    border-radius: 50px !important;
    padding: 14px 22px !important;
    font-size: 1.15rem !important;
    font-weight: 800 !important;
    border: 2px solid rgba(255,255,255,0.3) !important;
    box-shadow: 0 8px 30px rgba(255, 85, 0, 0.75) !important;
}
div[data-testid="stPopover"] > button:hover {
    transform: scale(1.08) !important;
}
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_vehicles():
    return pd.read_csv('vehicles_15k.csv')

df = load_vehicles()

# --- ANIMATED HERO ---
st.markdown("""
<div class="gcore-intro">
    <div style="display:inline-block; background:#FF5500; color:#fff; padding:4px 16px; border-radius:50px; font-weight:700; font-size:0.82rem; margin-bottom:10px;">
        ⚡ LIVE AI ENGINE • 15,000+ VEHICLES (CYCLE TO HELICOPTER)
    </div>
    <h1 class="gcore-logo-text">🟠 VEHICLE FINDER</h1>
    <p style="color:#B4B4C0; font-size:1.05rem; max-width:680px; margin:10px auto 0 auto;">
        Apna budget set karein, smart advantages dekhein, interactive comparison studio use karein, aur bottom-right <b>🤖 V-Bot</b> se baat karein!
    </p>
</div>
""", unsafe_allow_html=True)

# --- ADVANCED BUDGET & FILTER PANEL ---
if "budget_val" not in st.session_state:
    st.session_state.budget_val = 5000000

st.markdown("### 🎛️ Smart Budget & Filter Controls")
q1, q2, q3, q4, q5 = st.columns(5)
if q1.button("🚲 2 Lakh (Bike/Cycle)", use_container_width=True):
    st.session_state.budget_val = 200000
if q2.button("🛺 10 Lakh (Rickshaw/Used)", use_container_width=True):
    st.session_state.budget_val = 1000000
if q3.button("🚗 50 Lakh (Sedan/SUV)", use_container_width=True):
    st.session_state.budget_val = 5000000
if q4.button("🚚 3 Crore (Luxury/Truck)", use_container_width=True):
    st.session_state.budget_val = 30000000
if q5.button("🚁 25 Crore (Yacht/Chopper)", use_container_width=True):
    st.session_state.budget_val = 250000000

c1, c2, c3, c4 = st.columns([2, 1.5, 1.5, 1.5])
with c1:
    budget = st.number_input("💰 Exact Maximum Budget (PKR)", min_value=15000, max_value=1000000000, value=st.session_state.budget_val, step=50000)
    st.session_state.budget_val = budget
with c2:
    all_cats = ["All Categories"] + sorted(df['Category'].unique().tolist())
    selected_cat = st.selectbox("🚘 Vehicle Category", all_cats)
with c3:
    temp_df = df if selected_cat == "All Categories" else df[df['Category'] == selected_cat]
    all_brands = ["All Brands"] + sorted(temp_df['Brand'].unique().tolist())
    selected_brand = st.selectbox("🏷️ Brand Filter", all_brands)
with c4:
    sort_by = st.selectbox("⚡ Sort By Advantage", ["Best Comfort & Value", "Highest Top Speed", "Highest Mileage", "Lowest Price"])

# Filter Dataset
affordable_df = df[df['Price'] <= budget].copy()
if selected_cat != "All Categories":
    affordable_df = affordable_df[affordable_df['Category'] == selected_cat]
if selected_brand != "All Brands":
    affordable_df = affordable_df[affordable_df['Brand'] == selected_brand]

if sort_by == "Best Comfort & Value":
    affordable_df = affordable_df.sort_values(by=['Comfort_Score', 'Price'], ascending=[False, False])
elif sort_by == "Highest Top Speed":
    affordable_df = affordable_df.sort_values(by='Top_Speed_kmh', ascending=False)
elif sort_by == "Highest Mileage":
    affordable_df = affordable_df.sort_values(by='Mileage_kmpl', ascending=False)
else:
    affordable_df = affordable_df.sort_values(by='Price', ascending=True)

# --- METRICS (CLEAN VARIABLES WITHOUT BACKSLASHES) ---
total_count = f"{len(affordable_df):,}"
cat_count = f"{affordable_df['Category'].nunique()}" if not affordable_df.empty else "0"
best_buy_str = f"Rs {affordable_df['Price'].max():,}" if not affordable_df.empty else "N/A"
start_from_str = f"Rs {affordable_df['Price'].min():,}" if not affordable_df.empty else "N/A"

m1, m2, m3, m4 = st.columns(4)
m1.markdown(f"<div class='stat-card'><h2 style='color:#FF5500;margin:0;'>{total_count}</h2><p style='color:#A1A1AA;margin:0;'>VEHICLES IN BUDGET</p></div>", unsafe_allow_html=True)
m2.markdown(f"<div class='stat-card'><h2 style='color:#FF5500;margin:0;'>{cat_count}</h2><p style='color:#A1A1AA;margin:0;'>CATEGORIES FIT</p></div>", unsafe_allow_html=True)
m3.markdown(f"<div class='stat-card'><h2 style='color:#FF5500;margin:0;'>{best_buy_str}</h2><p style='color:#A1A1AA;margin:0;'>BEST YOU CAN BUY</p></div>", unsafe_allow_html=True)
m4.markdown(f"<div class='stat-card'><h2 style='color:#FF5500;margin:0;'>{start_from_str}</h2><p style='color:#A1A1AA;margin:0;'>STARTING FROM</p></div>", unsafe_allow_html=True)

st.write("")

# --- SEPARATE TABS FOR RECOMMENDATIONS & COMPARISON STUDIO ---
tab1, tab2 = st.tabs(["🏆 Top Recommended Vehicles", "⚖️ Comparison & Advantages Studio"])

with tab1:
    if not affordable_df.empty:
        top_vehicles = affordable_df.head(9)
        cols = st.columns(3)
        for idx, (_, row) in enumerate(top_vehicles.iterrows()):
            icon = CAT_ICONS.get(row['Category'], '🚘')
            safe_query = urllib.parse.quote(f"{row['Vehicle_Name']} official specs price")
            working_url = f"https://google.com{safe_query}"
            
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="vehicle-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
