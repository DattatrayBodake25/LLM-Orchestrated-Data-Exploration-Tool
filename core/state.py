import streamlit as st

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "df" not in st.session_state:
        st.session_state.df = None

    if "data_summary" not in st.session_state:
        st.session_state.data_summary = None

    if "data_profile" not in st.session_state:
        st.session_state.data_profile = None

    # SQL / Python engine toggle
    if "analysis_engine" not in st.session_state:
        st.session_state.analysis_engine = "Python"