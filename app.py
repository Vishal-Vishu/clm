import streamlit as st
from parser import extract_text
from llm import extract_contract_data
from database import init_db, insert_contract, get_all_contracts
from rag import build_index, search, load_index, save_index, documents

from database import get_summary_stats
import datetime

st.title("📊 Contract Intelligence Dashboard")

total, high_risk, medium_risk = get_summary_stats()

col1, col2, col3 = st.columns(3)

col1.metric("📄 Total Contracts", total)
col2.metric("⚠️ High Risk", high_risk)
col3.metric("🟡 Medium Risk", medium_risk)

from database import get_all_contracts
from datetime import datetime

st.subheader("🔔 Alerts")

contracts = get_all_contracts()

today = datetime.today()

for c in contracts:
    end_date = c[4]

    try:
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        days_left = (end_date_obj - today).days

        if days_left < 30:
            st.warning(f"⚠️ Contract {c[0]} expires in {days_left} days")
    except:
        pass

for c in contracts:
    if c[6] == "High":
        st.error(f"🚨 High Risk Contract ID: {c[0]}")

from database import get_contracts_by_filter

st.subheader("🔎 Filter Contracts")

risk_filter = st.selectbox(
    "Select Risk Level",
    ["All", "High", "Medium", "Low"]
)

if risk_filter == "All":
    filtered = get_contracts_by_filter()
else:
    filtered = get_contracts_by_filter(risk_filter)

for c in filtered:
    st.write(f"""
    **ID:** {c[0]}  
    **Party 1:** {c[1]}  
    **Party 2:** {c[2]}  
    **Start Date:** {c[3]}  
    **End Date:** {c[4]}  
    **Risk:** {c[6]}  
    """)
    st.divider()     

import pandas as pd

data = {
    "Risk": ["High", "Medium"],
    "Count": [high_risk, medium_risk]
}

df = pd.DataFrame(data)

st.bar_chart(df.set_index("Risk"))               

# -----------------------------
# INIT
# -----------------------------
init_db()

st.set_page_config(page_title="AI Contract Intelligence", layout="wide")
st.title("📄 AI Contract Intelligence Platform")

# -----------------------------
# LOAD INDEX (ON START)
# -----------------------------
if "index_ready" not in st.session_state:
    if load_index():
        st.session_state.index_ready = True
        st.success("✅ Loaded existing index")
    else:
        st.session_state.index_ready = False
        st.warning("⚠️ No index found. Please build index.")


# -----------------------------
# UPLOAD CONTRACT
# -----------------------------
st.subheader("📤 Upload Contract")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    contract_text = extract_text(uploaded_file)

    st.subheader("📜 Preview")
    st.text_area("Text", contract_text[:2000], height=200)

    if st.button("🚀 Analyze & Store Contract"):
        with st.spinner("Processing..."):
            data = extract_contract_data(contract_text)

            if data:
                # ✅ CRITICAL FIX: pass full_text
                insert_contract(data, contract_text)

                st.success("✅ Contract Stored")
                st.json(data)
            else:
                st.error("❌ Extraction failed")


# -----------------------------
# VIEW CONTRACTS
# -----------------------------
st.subheader("📚 Stored Contracts")

contracts = get_all_contracts()
st.write(f"Total contracts: {len(contracts)}")


# -----------------------------
# BUILD INDEX (MANUAL)
# -----------------------------
st.subheader("🧠 Build / Refresh Index")

if st.button("📚 Rebuild Search Index"):
    contracts = get_all_contracts()

    contract_data = [
        (c[0], c[8])
        for c in contracts
        if len(c) > 8 and c[8] and c[8].strip()
    ]

    st.write("Valid contracts:", len(contract_data))

    if len(contract_data) == 0:
        st.error("❌ No valid contract text found")
    else:
        build_index(contract_data)
        save_index()

        st.session_state.index_ready = True
        st.success("✅ Index built and saved")


# -----------------------------
# SEARCH (RAG)
# -----------------------------
st.subheader("🔎 Ask Questions")

query = st.text_input("Enter your question")

if query:
    if not st.session_state.index_ready:
        st.error("❌ Please build index first")
    else:
        results = search(query)

        st.subheader("📄 Retrieved Chunks")

        if results:
            for r in results:
                st.write(f"**Contract ID:** {r['contract_id']}")
                st.write(r['text'])
                st.divider()
        else:
            st.warning("No relevant results found")


# -----------------------------
# DEBUG PANEL
# -----------------------------
st.subheader("🧠 Debug Panel")

from rag import index

st.write("Index loaded:", index is not None)
st.write("Total chunks:", len(documents))

if documents:
    st.write("Sample chunk:")
    st.write(documents[0])