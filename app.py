import streamlit as st
import pandas as pd
import joblib
import google.generativeai as genai
from openai import OpenAI

# --- PAGE CONFIG ---
st.set_page_config(page_title="AutoEdge AI | Vehicle Recommender", page_icon="🚗", layout="wide")

# --- GCORE INSPIRED DARK & ORANGE UI + SMOOTH ANIMATIONS ---
st.markdown("""
<style>
@import url('https://googleapis.com');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #09090B;
    color: #FFFFFF;
}

/* Smooth Entrance Animation */
@keyframes fadeSlideUp {
    0% { opacity: 0; transform: translateY(30px); }
    100% { opacity: 1; transform: translateY(0); }
}

.hero-box {
    background: radial-gradient(circle at top right, rgba(255, 85, 0, 0.35), rgba(9, 9, 11, 0.95) 60%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 50px 30px;
    text-align: center;
    animation: fadeSlideUp 0.9s ease-out;
    margin-bottom: 30px;
}

.hero-title {
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #FFFFFF, #FF7733);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.gcore-card {
    background: #121216;
    border: 1px solid #242429;
    border-radius: 16px;
    padding: 24px;
    transition: all 0.35s cubic-bezier(0.25, 0.8, 0.25, 1);
    animation: fadeSlideUp 1.1s ease-out;
    height: 100%;
}

.gcore-card:hover {
    transform: translateY(-8px) scale(1.02);
    border-color: #FF5500;
    box-shadow: 0 12px 30px rgba(255, 85, 0, 0.2);
}

.badge-orange {
    background-color: #FF5500;
    color: white;
    padding: 5px 14px;
    border-radius: 50px;
    font-size: 0.8rem;
    font-weight: 600;
    display: inline-block;
    margin-bottom: 12px;
}

/* Active Buttons */
.stButton>button {
    background: linear-gradient(90deg, #FF5500, #FF7700);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 28px;
    font-weight: 600;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(255, 85, 0, 0.6);
}
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA & MODEL ---
@st.cache_data
def load_data():
    return pd.read_csv('vehicles_data.csv')

df = load_data()

# --- TOP NAVBAR (GCORE STYLE) ---
col_nav1, col_nav2, col_nav3 = st.columns([2, 5, 2])
with col_nav1:
    st.markdown("### 🟠 **AUTOEDGE AI**")
with col_nav2:
    nav_choice = st.radio("", ["🏠 Home", "🚘 Recommender", "⚖️ Compare Vehicles"], horizontal=True, label_visibility="collapsed")
with col_nav3:
    st.markdown("<div style='text-align:right;'><span class='badge-orange'>Live AI Engine</span></div>", unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown("""
<div class="hero-box">
    <span class="badge-orange">⚡ AI-Powered Vehicle Intelligence</span>
    <div class="hero-title">Smart Vehicle Selection at the Edge</div>
    <p style="color:#A1A1AA; font-size:1.1rem; max-width:650px; margin:15px auto;">
        Apna budget aur vehicle type enter karein. Hamara ML model aap ko best options recommend karega aur unka live comparison dikhayega.
    </p>
</div>
""", unsafe_allow_html=True)

# --- BUDGET & FILTER SECTION ---
st.markdown("### 🎯 Apna Budget Aur Pasand Select Karein")
c1, c2, c3 = st.columns([2, 2, 1])
with c1:
    budget = st.number_input("Maximum Budget (PKR)", min_value=1000000, max_value=50000000, value=8000000, step=500000)
with c2:
    v_type = st.selectbox("Vehicle Type", ["All", "Sedan", "Hatchback", "SUV"])
with c3:
    st.write("")
    st.write("")
    search_btn = st.button("Find Vehicles 🚀")

# --- FILTERING & RECOMMENDATIONS ---
filtered_df = df[df['Price'] <= budget]
if v_type != "All":
    filtered_df = filtered_df[filtered_df['Type'] == v_type]

if not filtered_df.empty:
    # Sort by Comfort Score & Mileage
    recommended = filtered_df.sort_values(by=['Comfort_Score', 'Mileage_kmpl'], ascending=False)
    
    st.markdown("### 🏆 Top Recommended Vehicles (Based on Advantages)")
    cols = st.columns(min(3, len(recommended)))
    for idx, (_, row) in enumerate(recommended.head(3).iterrows()):
        with cols[idx]:
            st.markdown(f"""
            <div class="gcore-card">
                <span class="badge-orange">#{idx+1} Best Match</span>
                <h3>{row['Vehicle_Name']}</h3>
                <p style="color:#FF7733; font-weight:700; font-size:1.2rem;">PKR {row['Price']:,}</p>
                <p style="color:#D4D4D8;"><b>Type:</b> {row['Type']} | <b>Avg:</b> {row['Mileage_kmpl']} km/l</p>
                <p style="color:#A1A1AA; font-size:0.9rem;">✨ <b>Key Advantage:</b> {row['Advantage']}</p>
            </div>
            """, unsafe_allow_html=True)

    # --- COMPARISON SECTION ---
    st.markdown("---")
    st.markdown("### ⚖️ Side-by-Side Vehicle Comparison")
    selected_cars = st.multiselect(
        "Compare karne ke liye gaariyan select karein:",
        options=filtered_df['Vehicle_Name'].tolist(),
        default=filtered_df['Vehicle_Name'].tolist()[:min(3, len(filtered_df))]
    )
    if selected_cars:
        comp_df = filtered_df[filtered_df['Vehicle_Name'].isin(selected_cars)].set_index('Vehicle_Name')
        st.dataframe(comp_df[['Type', 'Price', 'Mileage_kmpl', 'Maintenance_Cost', 'Comfort_Score', 'Resale_Value', 'Advantage']], use_container_width=True)
else:
    st.warning("Is budget mein koi vehicle nahi mili. Budget thora barha kar check karein!")

# --- MULTI-API CHATBOT (SIDEBAR / CORNER WIDGET) ---
# Apni 3 API keys yahan ya Streamlit Secrets mein lagayein
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", "APNI_GEMINI_KEY_YAHAN_LAGAYEIN")
GROQ_KEY = st.secrets.get("GROQ_API_KEY", "APNI_GROQ_KEY_YAHAN_LAGAYEIN")
OPENAI_KEY = st.secrets.get("OPENAI_API_KEY", "APNI_OPENAI_KEY_YAHAN_LAGAYEIN")

def multi_llm_chatbot(user_prompt):
    # API 1: Google Gemini
    try:
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"You are an expert car advisor. Answer concisely: {user_prompt}")
        return f"🟢 [Gemini]: {res.text}"
    except Exception:
        pass

    # API 2: Groq (Llama-3) Fallback
    try:
        client = OpenAI(base_url="https://groq.com", api_key=GROQ_KEY)
        res = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": user_prompt}]
        )
        return f"🟠 [Groq AI]: {res.choices[0].message.content}"
    except Exception:
        pass

    # API 3: OpenAI Fallback
    try:
        client = OpenAI(api_key=OPENAI_KEY)
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_prompt}]
        )
        return f"🔵 [OpenAI]: {res.choices[0].message.content}"
    except Exception:
        return "⚠️ Teeno API keys check karein! Streamlit Secrets mein valid keys add karein."

# Corner Chatbot Popover with Emoji
with st.sidebar:
    st.markdown("## 🤖 AutoBot AI Assistant")
    st.caption("Powered by 3 Multi-LLM APIs (Gemini + Groq + OpenAI)")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Salam! 🚗 Mujh se kisi bhi gaari, budget ya comparison ke baray mein poochein."}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask anything about vehicles..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        reply = multi_llm_chatbot(prompt)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)
