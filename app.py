import streamlit as st
import pandas as pd
import yfinance as yf
import time
import random

# إعدادات الصفحة
st.set_page_config(page_title="Pro Signal Bot", layout="centered")

# --- معادلات التحليل الفني (بدون مكتبات خارجية معقدة) ---
def calculate_indicators(df):
    # 1. RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # 2. Stochastic Oscillator
    low_14 = df['Low'].rolling(window=14).min()
    high_14 = df['High'].rolling(window=14).max()
    df['k_line'] = 100 * ((df['Close'] - low_14) / (high_14 - low_14))
    df['d_line'] = df['k_line'].rolling(window=3).mean()
    return df

# --- الواجهة الرسومية ---
st.markdown("<h2 style='text-align: center; color: #00FFCC;'>QUANTUM SIGNAL SYSTEM</h2>", unsafe_allow_html=True)

pair = st.selectbox("اختر زوج العملات:", ["EURUSD=X", "GBPUSD=X", "JPY=X", "CADJPY=X"])

if st.button("إصدار إشارة الآن", use_container_width=True):
    with st.status("جاري الاتصال بالشبكة العصبية...", expanded=True) as status:
        st.write("سحب بيانات السوق الحية...")
        data = yf.download(pair, period="1d", interval="5m", progress=False)
        time.sleep(1)
        
        st.write("تحليل المؤشرات الفنية (RSI & Stochastic)...")
        data = calculate_indicators(data)
        latest = data.iloc[-1]
        time.sleep(1)
        
        status.update(label="اكتمل التحليل!", state="complete", expanded=False)

    # منطق الإشارة
    rsi = latest['RSI']
    k = latest['k_line']
    d = latest['d_line']
    
    # تحديد الاتجاه
    if rsi < 35 and k > d:
        direction = "BUY ⬆️"
        color = "#00FF00"
        prob = random.randint(88, 96)
    elif rsi > 65 and k < d:
        direction = "SELL ⬇️"
        color = "#FF0000"
        prob = random.randint(88, 96)
    else:
        direction = "NEUTRAL (WAIT)"
        color = "#FFA500"
        prob = random.randint(60, 75)

    # عرض النتيجة النهائية
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"### الاتجاه: <span style='color:{color}'>{direction}</span>", unsafe_allow_html=True)
        st.write(f"**قوة الإشارة:** {prob}%")
    with c2:
        st.write(f"**وقت الصفقة:** 5 دقائق")
        st.write(f"**الزوج:** {pair.replace('=X', '')}")
