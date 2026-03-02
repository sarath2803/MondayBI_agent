import streamlit as st
from agent import run_agent

st.set_page_config(page_title="Monday BI Agent")

st.title("📊 Monday.com Business Intelligence Agent")

if "history" not in st.session_state:
    st.session_state.history = []

query = st.chat_input("Ask a business question...")

if query:
    st.chat_message("user").write(query)

    with st.spinner("Analyzing live data..."):
        response, trace = run_agent(query)

    st.chat_message("assistant").write(response)

    with st.expander("🔍 Agent Actions"):
        for t in trace:
            st.write(t)