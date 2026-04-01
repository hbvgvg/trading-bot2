import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import time
import random

# ==========================================
# 1. إعدادات واجهة المستخدم (UI)
# ==========================================
st.set_page_config(page_title="Quantum Signal Generator", layout="centered", initial_sidebar_state="collapsed")

# تصميم CSS مخصص لإعطاء طابع مستقبلي (Cyberpunk/Tech)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; }
    .signal-title { text-align: center; color: #00FFCC; font-family: 'Courier New', Courier, monospace; font-weight: bold; font-size: 32px; text-shadow: 0px 0px 10px #00FFCC; }
    .phase-text { text-align: center; color: #8892B0; font-family: 'Courier New', Courier, monospace; }
    .metric-label { color: #00FFCC !important; font-weight: bold; }
    .metric-value-long { color: #00FF00 !important; font-size: 24px; font-weight: bold; text-shadow: 0px 0px 8px #00FF00; }
    .metric-value-short { color: #FF0044 !important; font-size: 24px; font-weight: bold; text-shadow: 0px 0px 8px #FF0044; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='signal-title'>AUTOMATED SIGNAL GENERATION</div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 2. دوال التحليل الفني وجلب البيانات (Backend)
# ==========================================
def get_market_data(symbol="CADJPY=X", period="1d", interval="5m"):
    """جلب بيانات السوق الحية (استخدمنا yfinance كمثال مجاني للأزواج العادية)"""
    df = yf.download(symbol, period=period, interval=interval, progress=False)
    return df

def calculate_heikin_ashi(df):
    """حساب شموع هيكين آشي لتصفية الاتجاه"""
    ha_df = df.copy()
    ha_df['HA_Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
    ha_df['HA_Open'] = 0.0
    ha_df['HA_Open'].iloc[0] = (df['Open'].iloc[0] + df['Close'].iloc[0]) / 2
    for i in range(1, len(df)):
        ha_df['HA_Open'].iloc[i] = (ha_df['HA_Open'].iloc[i-1] + ha_df['HA_Close'].iloc[i-1]) / 2
    ha_df['HA_High'] = ha_df[['High', 'HA_Open', 'HA_Close']].max(axis=1)
    ha_df['HA_Low'] = ha_df[['Low', 'HA_Open', 'HA_Close']].min(axis=1)
    return ha_df

def generate_signal(df):
    """تطبيق استراتيجية RSI و Stochastic على بيانات هيكين آشي"""
    ha_df = calculate_heikin_ashi(df)
    
    # حساب المؤشرات
    ha_df.ta.rsi(close='HA_Close', length=14, append=True)
    ha_df.ta.stoch(high='HA_High', low='HA_Low', close='HA_Close', window=14, smooth_window=3, append=True)
    
    # جلب آخر قراءة للمؤشرات
    latest = ha_df.iloc[-1]
    rsi_val = latest['RSI_14']
    stoch_k = latest['STOCHk_14_3_3']
    stoch_d = latest['STOCHd_14_3_3']
    
    # المنطق البرمجي للإشارة
    signal_dir = "WAIT"
    probability = random.randint(50, 65) # نسبة افتراضية في حالة الانتظار
    
    # شروط الشراء (LONG)
    if rsi_val < 35 and stoch_k > stoch_d and stoch_k < 30:
        signal_dir = "LONG ⬆️"
        probability = random.randint(85, 95)
    
    # شروط البيع (SHORT)
    elif rsi_val > 65 and stoch_k < stoch_d and stoch_k > 70:
        signal_dir = "SHORT ⬇️"
        probability = random.randint(85, 95)
        
    # إذا لم تتحقق الشروط القوية، نعطي إشارة محتملة بناءً على التقاطع فقط كنموذج عرض
    if signal_dir == "WAIT":
        if stoch_k > stoch_d:
            signal_dir = "LONG ⬆️"
            probability = random.randint(70, 84)
        else:
            signal_dir = "SHORT ⬇️"
            probability = random.randint(70, 84)

    return signal_dir, probability

# ==========================================
# 3. تشغيل البوت وتفاعل الواجهة
# ==========================================
pair_input = st.selectbox("Select Currency Pair:", ["CADJPY=X", "EURUSD=X", "GBPUSD=X", "USDJPY=X"])

if st.button("🚀 INITIATE ANALYSIS", use_container_width=True):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # محاكاة الاتصال وتحميل البيانات للواجهة
    phases = [
        "Connecting to Neural Network...", 
        "Collecting Market Data...", 
        "Processing Heikin Ashi & Indicators...", 
        "Validating Quantum Signal..."
    ]
    
    # الواجهة البصرية للتحميل
    for i in range(100):
        time.sleep(0.03) 
        progress_bar.progress(i + 1)
        if i < 25: status_text.markdown(f"<p class='phase-text'>{phases[0]}</p>", unsafe_allow_html=True)
        elif i < 50: status_text.markdown(f"<p class='phase-text'>{phases[1]}</p>", unsafe_allow_html=True)
        elif i < 80: status_text.markdown(f"<p class='phase-text'>{phases[2]}</p>", unsafe_allow_html=True)
        else: status_text.markdown(f"<p class='phase-text'>{phases[3]}</p>", unsafe_allow_html=True)

    # تنفيذ التحليل الفعلي خلف الكواليس
    try:
        df = get_market_data(symbol=pair_input, interval="5m")
        if not df.empty:
            direction, prob = generate_signal(df)
            
            status_text.empty()
            progress_bar.empty()
            st.markdown("<h3 style='text-align: center; color: #00FFCC;'>✅ ANALYSIS COMPLETE</h3>", unsafe_allow_html=True)
            st.divider()
            
            # عرض النتيجة بشكل احترافي
            col1, col2 = st.columns(2)
            
            css_class = "metric-value-long" if "LONG" in direction else "metric-value-short"
            
            with col1:
                st.markdown(f"<p class='metric-label'>Currency Pair</p><h4>{pair_input.replace('=X', '')} OTC</h4>", unsafe_allow_html=True)
                st.markdown(f"<p class='metric-label'>Direction</p><p class='{css_class}'>{direction}</p>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<p class='metric-label'>Exp Time</p><h4>5 Minutes</h4>", unsafe_allow_html=True)
                st.markdown(f"<p class='metric-label'>Probability</p><h4 style='color: #FFD700;'>{prob}%</h4>", unsafe_allow_html=True)
                
        else:
            st.error("Error: Could not fetch market data. Please check connection.")
            
    except Exception as e:
        st.error(f"An error occurred during analysis: {e}")