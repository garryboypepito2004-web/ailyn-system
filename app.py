import streamlit as st
import smtplib
import pandas as pd
from datetime import datetime
from email.message import EmailMessage

# ═════════════════ CONFIGURATION ═════════════════
SENDER_EMAIL = "garryboypepito71@gmail.com"
SENDER_PASSWORD = "fhyv cimp gync wjmj"
# ailyn_peps0678@yahoo.com is temporarily removed
RECEIVER_EMAILS = ["garryboypepito2004@gmail.com"] 
# ═════════════════════════════════════════════════

st.set_page_config(page_title="Ailyn Construction", layout="centered")

if 'records' not in st.session_state:
    st.session_state.records = []
if 'budget' not in st.session_state:
    st.session_state.budget = 0.0

def send_email_report(records, budget, balance):
    msg = EmailMessage()
    msg["Subject"] = f"CONSTRUCTION REPORT - {datetime.now().strftime('%d %b %Y')}"
    msg["From"] = f"AILYN CONSTRUCTION <{SENDER_EMAIL}>"
    msg["To"] = ", ".join(RECEIVER_EMAILS)

    rows = ""
    for r in records:
        rows += f"""
        <tr>
            <td style='padding:8px; border:1px solid #ddd;'>{r['Date']}</td>
            <td style='padding:8px; border:1px solid #ddd;'>{r['Who']}</td>
            <td style='padding:8px; border:1px solid #ddd;'>{r['What']}</td>
            <td style='padding:8px; border:1px solid #ddd; text-align:right;'>PHP {r['Amount']:,.2f}</td>
        </tr>
        """

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <div style="background-color: #1b5e20; padding: 15px; color: white; text-align: center;">
            <h2 style="margin: 0;">AILYN CONSTRUCTION: SITE UPDATE</h2>
        </div>
        <p><b>Project:</b> Two-Story Residential Building (Davao City)</p>
        <p><b>Date:</b> {datetime.now().strftime('%B %d, %Y')}</p>
        <p><b>Current Balance:</b> <span style="color: #d32f2f;">PHP {balance:,.2f}</span></p>
        <hr>
        <table style="width: 100%; border-collapse: collapse;">
            <tr style="background-color: #f2f2f2;">
                <th style="padding:8px; border:1px solid #ddd; text-align:left;">Date</th>
                <th style="padding:8px; border:1px solid #ddd; text-align:left;">Who (Supplier/Worker)</th>
                <th style="padding:8px; border:1px solid #ddd; text-align:left;">What (Item/Service)</th>
                <th style="padding:8px; border:1px solid #ddd; text-align:right;">Amount</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """
    msg.add_alternative(html_body, subtype='html')

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        st.success("✅ Report successfully sent!")
    except Exception as e:
        st.error(f"❌ Email Error: {e}")

# --- APP UI ---
st.markdown('<h1 style="text-align:center; color:#1b5e20;">🏗️ AILYN CONSTRUCTION</h1>', unsafe_allow_html=True)

mat_total = sum(r['Amount'] for r in st.session_state.records)
current_balance = st.session_state.budget - mat_total

col_b1, col_b2 = st.columns(2)
with col_b1:
    st.session_state.budget = st.number_input("Set Total Budget (PHP)", value=st.session_state.budget)
with col_b2:
    st.metric("Running Balance", f"PHP {current_balance:,.2f}")

with st.form("entry_form", clear_on_submit=True):
    c1, c2 = st.columns(2)
    with c1:
        who_input = st.text_input("WHO (Person or Store)").upper()
    with c2:
        what_input = st.text_input("WHAT (Material or Labor)").upper()
    amt_input = st.number_input("Amount (PHP)", min_value=0.0)
    if st.form_submit_button("ADD TO LIST"):
        if who_input and what_input and amt_input > 0:
            st.session_state.records.append({
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Who": who_input, "What": what_input, "Amount": amt_input
            })
            st.rerun()

if st.session_state.records:
    st.table(pd.DataFrame(st.session_state.records))
    if st.button("🚀 SEND FULL REPORT TO GMAIL"):
        send_email_report(st.session_state.records, st.session_state.budget, current_balance)

if st.button("🗑️ Reset All Data"):
    st.session_state.records = []
    st.rerun()