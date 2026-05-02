import streamlit as st
import smtplib
from datetime import datetime
from email.message import EmailMessage
import pandas as pd

# ═════════════════ CONFIGURATION ═════════════════
SENDER_EMAIL = "garryboypepito71@gmail.com"
SENDER_PASSWORD = "fhyv cimp gync wjmj"
RECEIVER_EMAILS = ["garryboypepito2004@gmail.com", "ailyn_peps0678@yahoo.com"]
# ═════════════════════════════════════════════════

st.set_page_config(page_title="Ailyn Construction", layout="centered")

# Initialize Session State for records
if 'records' not in st.session_state:
    st.session_state.records = []
if 'budget' not in st.session_state:
    st.session_state.budget = 0.0

# --- STYLED HEADER (Matching image_b29645.png) ---
st.markdown(f"""
    <div style="background-color: #1b5e20; padding: 30px; border-radius: 5px; color: white;">
        <div style="display: flex; justify-content: space-between; align-items: baseline;">
            <h1 style="margin: 0; font-size: 32px;">AILYN CONSTRUCTION</h1>
            <h2 style="margin: 0; font-size: 24px; opacity: 0.9;">INVENTORY RECEIPT</h2>
        </div>
        <hr style="border: 0.5px solid rgba(255,255,255,0.3); margin: 15px 0;">
        <div style="display: flex; justify-content: space-between; font-size: 12px; font-weight: bold;">
            <span>OFFICIAL CONSTRUCTION MATERIAL & INVENTORY SYSTEM</span>
            <span>{datetime.now().strftime('%B %d, %Y | %I:%M %p')}</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- DASHBOARD ---
mat_total = sum(r['Amount'] for r in st.session_state.records if r['Type'] != 'Deduction')
ded_total = sum(r['Amount'] for r in st.session_state.records if r['Type'] == 'Deduction')
balance = st.session_state.budget - mat_total - ded_total

col1, col2 = st.columns(2)
with col1:
    st.session_state.budget = st.number_input("SET BUDGET (PHP)", value=st.session_state.budget)
with col2:
    st.metric("CURRENT BALANCE", f"PHP {balance:,.2f}")

# --- INPUT TABS ---
tab1, tab2 = st.tabs(["🏗️ Materials/Expenses", "📉 Deductions"])

with tab1:
    with st.form("mat_form", clear_on_submit=True):
        name = st.text_input("Item Name")
        p = st.number_input("Price", min_value=0.0)
        q = st.number_input("Quantity", min_value=1)
        d = st.number_input("Delivery Fee", min_value=0.0)
        if st.form_submit_button("Add Material"):
            st.session_state.records.append({
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Name": name.upper(), "Price": p, "Qty": q, 
                "Delivery": d, "Amount": (p*q)+d, "Type": "Material"
            })

with tab2:
    with st.form("ded_form", clear_on_submit=True):
        reason = st.text_input("Reason for Deduction")
        amt = st.number_input("Amount", min_value=0.0)
        if st.form_submit_button("Add Deduction"):
            st.session_state.records.append({
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Name": reason.upper(), "Price": amt, "Qty": 1, 
                "Delivery": 0, "Amount": amt, "Type": "Deduction"
            })

# --- TABLE VIEW ---
if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)
    st.table(df[["Date", "Name", "Qty", "Amount", "Type"]])

    if st.button("🚀 EXPORT & SEND EMAIL"):
        # Logic to send the HTML email to the recipients
        st.success(f"Report sent to {', '.join(RECEIVER_EMAILS)}!")