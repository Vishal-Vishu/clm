import streamlit as st
from parser import extract_text
from llm import extract_contract_data
from database import init_db, insert_contract, get_all_contracts
from rag import build_index, search, documents
from database import get_all_contracts

# Initialize DB
init_db()

st.set_page_config(page_title="AI Contract Intelligence", layout="wide")

st.title("📄 AI Contract Intelligence Platform (Phase 2)")

# --- Upload Section ---
uploaded_file = st.file_uploader("Upload Contract (PDF)", type="pdf")

if uploaded_file:

    contract_text = extract_text(uploaded_file)

    st.subheader("📜 Contract Preview")
    st.text_area("Text", contract_text[:2000], height=200)

    if st.button("🚀 Analyze & Store Contract"):

        with st.spinner("Analyzing with AI..."):

            data = extract_contract_data(contract_text)

            if data:
                insert_contract(data)

                st.success("✅ Contract Stored Successfully")

                st.subheader("📊 Extracted Data")
                st.json(data)
            else:
                st.error("❌ Failed to extract structured data")

# --- Database View ---
st.subheader("📚 Stored Contracts")

contracts = get_all_contracts()

if contracts:
    for c in contracts:
        st.write(f"""
        **ID:** {c[0]}  
        **Party 1:** {c[1]}  
        **Party 2:** {c[2]}  
        **Start Date:** {c[3]}  
        **End Date:** {c[4]}  
        **Payment:** {c[5]}  
        **Risk:** {c[6]}  
        """)
        st.divider()
else:
    st.info("No contracts stored yet.")

if st.button("📚 Build Search Index"):
    contracts = get_all_contracts()

    # Use raw_json or store full text separately ideally
    contract_data = [(c[0], c[7]) for c in contracts]

    build_index(contract_data)

    st.success("✅ Index built successfully")

query = st.text_input("Ask a question across contracts")

if query:
    results = search(query)
    print('Results ', results)
    st.subheader("📄 Relevant Results")
    st.write(results)

contracts = get_all_contracts()
st.write("DEBUG: Contracts in DB →", contracts)    

st.subheader("📚 RAG Stored Chunks")

if documents:
    for i, doc in enumerate(documents[:10]):  # show first 10
        st.write(f"Chunk {i+1}")
        st.write(f"Contract ID: {doc['contract_id']}")
        st.write(doc['text'])
        st.divider()
else:
    st.warning("No documents in RAG yet")