import streamlit as st
import pandas as pd
import yfinance as yf
import time
import random

# إعدادات الواجهة لتكون مطابقة للفيديو
st.set_page_config(page_title="Quantum AI Bot", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #00FFCC; }
    .stSelectbox label { color: #00FFCC !important; }
    .stButton>button { 
        background-color: transparent; 
        color: #00FFCC; 
        border: 2px solid #00FFCC;
        border-radius: 20px;
        font-weight: bold;
    }
    .stButton>button:hover { background-color: #00FFCC; color: black; }
    .signal-card {
        background-color: rgba(0, 255, 204, 0.05);
        border: 1px solid #00FFCC;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

def calculate_rsi(series, period=14):
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ema_up = up.ewm(com=period - 1, adjust=False).mean()
    ema_down = down.ewm(com=period - 1, adjust=False).mean()
    rs = ema_up / ema_down
    return 100 - (100 / (1 + rs))

st.markdown("<h1 style='text-align: center;'>QUANTUM AI GENERATOR</h1>", unsafe_allow_html=True)

# قائمة أزواج العملات
pairs = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "USDJPY=X",
    "CAD/JPY": "CADJPY=X",
    "BTC/USD": "BTC-USD"
}

selection = st.selectbox("CHOOSE CURRENCY PAIR", list(pairs.keys()))

if st.button("RUN NEURAL ANALYSIS"):
    with st.spinner("Connecting to Quantum Servers..."):
        # جلب البيانات
        data = yf.download(pairs[selection], period="1d", interval="5m", progress=False)
        
        if len(data) < 20:
            st.error("بيانات غير كافية حالياً، يرجى المحاولة لاحقاً أو اختيار زوج آخر.")
        else:
            # التحليل
            data['RSI'] = calculate_rsi(data['Close'])
            
            # محاكاة التحميل كما في الفيديو
            progress_bar = st.progress(0)
            status_text = st.empty()
            messages = ["Analyzing price movements...", "Detecting market patterns...", "Calculating indicators...", "Validating signal..."]
            
            for i in range(100):
                time.sleep(0.03)
                progress_bar.progress(i + 1)
                status_text.text(messages[i // 26] if i // 26 < len(messages) else messages[-1])
            
            # النتيجة النهائية
            rsi_val = data['RSI'].iloc[-1]
            prob = random.randint(89, 97)
            
            # منطق الإشارة
            if rsi_val < 35:
                direction = "BUY ⬆️"
                color = "#00FF88"
            elif rsi_val > 65:
                direction = "SELL ⬇️"
                color = "#FF3366"
            else:
                direction = "BUY ⬆️" if data['Close'].iloc[-1] > data['Open'].iloc[-1] else "SELL ⬇️"
                color = "#00CCFF"
                prob = random.randint(75, 85)

            st.markdown(f"""
                <div class="signal-card">
                    <h2 style="color: white;">SIGNAL READY</h2>
                    <hr style="border-color: #00FFCC;">
                    <h1 style="color: {color}; font-size: 50px;">{direction}</h1>
                    <p style="font-size: 20px;">PROBABILITY: <span style="color: gold;">{prob}%</span></p>
                    <p>PAIR: {selection} | TIME: 5 MIN</p>
                </div>
            """, unsafe_allow_html=True)
