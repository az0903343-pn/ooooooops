import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re

st.set_page_config(page_title="VEHICLE FINDER | AI Edge", page_icon="🚀", layout="wide")

# --- CUSTOM CSS: GCORE INTRO ANIMATION + FLOATING CORNER CHATBOT + CARDS ---
st.markdown("""
<style>
@import url('https://googleapis.com');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #08080A;
    color: #FFFFFF;
}

/* Gcore Style Intro Banner Animation */
@keyframes gcoreZoomIn {
    0% { opacity: 0; transform: scale(0.85) translateY(20px); filter: blur(8px); }
    60% { opacity: 1; transform: scale(1.03) translateY(0); filter: blur(0px); }
    100% { opacity: 1; transform: scale(1) translateY(0); }
}

@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 25px rgba(255, 85, 0, 0.35); }
    50% { box-shadow: 0 0 55px rgba(255, 85, 0, 0.75); }
}

.gcore-intro {
    background: radial-gradient(circle at center, rgba(255, 85, 0, 0.28) 0%, #0D0D11 70%);
    border: 1px solid rgba(255, 85, 0, 0.4);
    border-radius: 22px;
    padding: 45px 20px;
    text-align: center;
    animation: gcoreZoomIn 1.2s cubic-bezier(0.22, 1, 0.36, 1) forwards, pulseGlow 4s infinite;
    margin-bottom: 28px;
}

.gcore-logo-text {
    font-size: 3.6rem;
    font-weight: 900;
    letter-spacing: 4px;
    background: linear-gradient(90deg, #FFFFFF 20%, #FF5500 80%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}

.stat-card {
    background: #121217;
    border: 1px solid #26262E;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    transition: all 0.3s ease;
}
.stat-card:hover {
    border-color: #FF5500;
    transform: translateY(-5px);
}

.vehicle-card {
    background: linear-gradient(145deg, #14141A, #0E0E12);
    border: 1px solid #272730;
    border-radius: 18px;
    padding: 22px;
    transition: all 0.35s ease;
    margin-bottom: 16px;
}
.vehicle-card:hover {
    border-color: #FF5500;
    transform: translateY(-6px) scale(1.01);
    box-shadow: 0 12px 30px rgba(255, 85, 0, 0.22);
}

.visit-btn {
    display: inline-block;
    background: linear-gradient(90deg, #FF5500, #FF7722);
    color: white !important;
    text-decoration: none;
    padding: 10px 18px;
    border-radius: 10px;
    font-weight: 700;
    font-size: 0.9rem;
    margin-top: 12px;
    transition: 0.3s;
}
.visit-btn:hover {
    box-shadow: 0 0 18px rgba(255, 85, 0, 0.8);
    transform: scale(1.04);
}

/* Floating Bottom-Right Corner Chatbot Styling */
div[data-testid="stPopover"] {
    position: fixed;
    bottom: 24px;
    right: 24px;
    z-index: 99999;
}
div[data-testid="stPopover"] > button {
    background: linear-gradient(135deg, #FF5500, #8B26FF) !important;
    color: white !important;
    border-radius: 50px !important;
    padding: 14px 22px !important;
    font-size: 1.2rem !important;
    font-weight: 800 !important;
    border: 2px solid rgba(255,255,255,0.25) !important;
    box-shadow: 0 8px 30px rgba(255, 85, 0, 0.6) !important;
    transition: all 0.3s ease !important;
}
div[data-testid="stPopover"] > button:hover {
    transform: scale(1.1) rotate(-3deg) !important;
}
</style>
""", unsafe_allow_html=True)

# --- LOAD 15,000 VEHICLES DATA ---
@st.cache_data
def load_vehicles():
    return pd.read_csv('vehicles_15k.csv')

df = load_vehicles()

# --- GCORE ANIMATED INTRO HERO ---
st.markdown("""
<div class="gcore-intro">
    <div style="display:inline-block; background:#FF5500; color:#fff; padding:5px 16px; border-radius:50px; font-weight:700; font-size:0.85rem; margin-bottom:12px;">
        ⚡ LIVE AI ENGINE • 15,000+ VEHICLES DATABASE
    </div>
    <h1 class="gcore-logo-text">🟠 VEHICLE FINDER</h1>
    <p style="color:#B4B4C0; font-size:1.15rem; max-width:700px; margin:12px auto 0 auto;">
        Cycle se lekar Helicopter tak — apna budget enter karein, smart advantages dekhein, visual charts se compare karein, aur direct official link par jayein!
    </p>
</div>
""", unsafe_allow_html=True)

# --- BUDGET & CATEGORY CONTROLS ---
c1, c2, c3 = st.columns([2, 2, 1.5])
with c1:
    budget = st.number_input("💰 Apna Maximum Budget Likhein (PKR)", min_value=15000, max_value=1000000000, value=5000000, step=50000)
with c2:
    all_cats = ["All Categories"] + sorted(df['Category'].unique().tolist())
    selected_cat = st.selectbox("🚘 Vehicle Category Chunein", all_cats)
with c3:
    sort_by = st.selectbox("⚡ Priority / Advantage", ["Best Comfort & Value", "Highest Mileage", "Highest Top Speed", "Lowest Price"])

# Filter Logic
affordable_df = df[df['Price'] <= budget].copy()
if selected_cat != "All Categories":
    affordable_df = affordable_df[affordable_df['Category'] == selected_cat]

if sort_by == "Best Comfort & Value":
    affordable_df = affordable_df.sort_values(by=['Comfort_Score', 'Price'], ascending=[False, False])
elif sort_by == "Highest Mileage":
    affordable_df = affordable_df.sort_values(by='Mileage_kmpl', ascending=False)
elif sort_by == "Highest Top Speed":
    affordable_df = affordable_df.sort_values(by='Top_Speed_kmh', ascending=False)
else:
    affordable_df = affordable_df.sort_values(by='Price', ascending=True)

# --- LIVE METRICS ROW ---
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f"<div class='stat-card'><h2 style='color:#FF5500;margin:0;'>{len(affordable_df):,}</h2><p style='color:#A1A1AA;margin:0;'>VEHICLES IN BUDGET</p></div>", unsafe_allow_html=True)
with m2:
    cats_fit = affordable_df['Category'].nunique() if not affordable_df.empty else 0
    st.markdown(f"<div class='stat-card'><h2 style='color:#FF5500;margin:0;'>{cats_fit}</h2><p style='color:#A1A1AA;margin:0;'>CATEGORIES FIT</p></div>", unsafe_allow_html=True)
with m3:
    max_fit = f"Rs {affordable_df['Price'].max():,}" if not affordable_df.empty else "N/A"
    st.markdown(f"<div class='stat-card'><h2 style='color:#FF5500;margin:0;'>{max_fit}</h2><p style='color:#A1A1AA;margin:0;'>BEST YOU CAN BUY</p></div>", unsafe_allow_html=True)
with m4:
    min_fit = f"Rs {affordable_df['Price'].min():,}" if not affordable_df.empty else "N/A"
    st.markdown(f"<div class='stat-card'><h2 style='color:#FF5500;margin:0;'>{min_fit}</h2><p style='color:#A1A1AA;margin:0;'>STARTING FROM</p></div>", unsafe_allow_html=True)

st.write("")

# --- RECOMMENDED VEHICLES WITH DIRECT WEBSITE BUTTONS ---
if not affordable_df.empty:
    st.markdown("### 🏆 Top Recommended Vehicles (With Direct Website Links)")
    top_vehicles = affordable_df.head(6)
    cols = st.columns(3)
    for idx, (_, row) in enumerate(top_vehicles.iterrows()):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="vehicle-card">
                <span style="background:#24242E; color:#FF7733; padding:4px 12px; border-radius:20px; font-size:0.8rem; font-weight:700;">
                    {row['Category']} • {row['Year']}
                </span>
                <h3 style="margin:10px 0 4px 0;">{row['Vehicle_Name']}</h3>
                <p style="color:#FF5500; font-size:1.3rem; font-weight:800; margin:0;">PKR {row['Price']:,}</p>
                <p style="color:#D4D4D8; font-size:0.9rem; margin:8px 0;">
                    ⚡ <b>Speed:</b> {row['Top_Speed_kmh']} km/h | ⛽ <b>Avg:</b> {row['Mileage_kmpl']} km/l | ⭐ <b>Score:</b> {row['Comfort_Score']}/10
                </p>
                <p style="color:#A1A1AA; font-size:0.88rem; margin:6px 0;">
                    ✅ <b>Advantage:</b> {row['Advantage']}
                </p>
                <a href="{row['Direct_Link']}" target="_blank" class="visit-btn">🔗 Open Official / Market Page</a>
            </div>
            """, unsafe_allow_html=True)

    # --- INTERACTIVE MOVING VISUAL COMPARISON (NO BORING TABLES!) ---
    st.markdown("---")
    st.markdown("### 📊 Interactive Visual Comparison Studio")
    comp_choices = st.multiselect(
        "Compare karne ke liye koi bhi 2 se 5 vehicles select karein:",
        options=affordable_df['Vehicle_Name'].head(100).tolist(),
        default=affordable_df['Vehicle_Name'].head(3).tolist()
    )

    if len(comp_choices) >= 2:
        comp_data = affordable_df[affordable_df['Vehicle_Name'].isin(comp_choices)].drop_duplicates(subset=['Vehicle_Name'])
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            fig_bar = px.bar(
                comp_data,
                x='Vehicle_Name',
                y=['Top_Speed_kmh', 'Mileage_kmpl', 'Comfort_Score'],
                barmode='group',
                title="⚡ Performance, Mileage & Comfort Comparison",
                color_discrete_sequence=['#FF5500', '#00E5FF', '#A855F7']
            )
            fig_bar.update_layout(paper_bgcolor='#121217', plot_bgcolor='#121217', font_color='white')
            st.plotly_chart(fig_bar, use_container_width=True)

        with chart_col2:
            fig_radar = go.Figure()
            for _, r in comp_data.iterrows():
                fig_radar.add_trace(go.Scatterpolar(
                    r=[r['Comfort_Score']*10, min(r['Top_Speed_kmh']/3.2, 100), min(r['Mileage_kmpl']*1.5, 100), r['Comfort_Score']*10],
                    theta=['Comfort', 'Top Speed', 'Fuel Efficiency', 'Comfort'],
                    fill='toself',
                    name=r['Vehicle_Name']
                ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor='#2A2A35')),
                paper_bgcolor='#121217',
                font_color='white',
                title="🎯 Multi-Axis Advantage Radar"
            )
            st.plotly_chart(fig_radar, use_container_width=True)
else:
    st.warning("Is budget mein koi vehicle nahi mili! Kam az kam Rs 15,000 (Cycle ke liye) enter karein.")

# --- API-FREE INTELLIGENT CHATGPT-STYLE CORNER CHATBOT ---
def smart_vehicle_assistant(user_msg, data_df, current_budget):
    msg = user_msg.lower().strip()
    
