import streamlit as st
import pandas as pd
import warnings
import openai
import datetime
import os

from dotenv import load_dotenv

from core.state import init_session_state
from core.data_loader import sidebar_file_upload
from core.export_report import export_conversation
from core.prompts import build_system_prompt
from core.llm_client import generate_llm_response
from core.code_runner import execute_code_blocks
from core.ui_components import (
    render_chat_history,
    show_no_data_screen,
    show_data_health_report
)

# SQL mode imports (NEW)
from core.sql_prompt import build_sql_prompt
from core.sql_engine import execute_sql_query

# Load .env file
load_dotenv()

st.set_page_config(
    page_title="Ask Your CSV",
    page_icon="📊",
    layout="wide"
)

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("❌ OPENAI_API_KEY missing! Check your .env file.")
else:
    client = openai.OpenAI(api_key=api_key)

# Initialize session state
init_session_state()

st.title("📊 Ask Your CSV")
st.markdown("Upload your data and ask questions in plain English!")

# Sidebar for data upload
sidebar_file_upload()

# ---- Analysis Engine Toggle (NEW) ----
with st.sidebar:
    st.markdown("---")
    st.header("🧠 Analysis Engine")

    st.session_state.analysis_engine = st.radio(
        "Choose execution mode",
        ["Python", "SQL"],
        index=0,
        help="Python = flexible analysis | SQL = fast, large datasets"
    )

# ---- Data Health Report (existing feature) ----
show_data_health_report()

# ---- Export report ----
if st.session_state.messages:
    with st.sidebar:
        st.markdown("---")
        st.header("💾 Export Options")
        if st.button("Generate Report"):
            export_html = export_conversation()
            st.download_button(
                label="📥 Download Report (HTML)",
                data=export_html,
                file_name=f"data_analysis_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.html",
                mime="text/html"
            )
            st.info("💡 Tip: Open the HTML file and print to PDF for best results")

# ---- Main interface ----
if st.session_state.df is not None:

    render_chat_history()

    user_input = st.chat_input("Ask a question about your data")

    if user_input:

        # Store user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Show user message
        with st.chat_message("user"):
            st.markdown(user_input)

        engine = st.session_state.analysis_engine

        # ---- SQL MODE ----
        if engine == "SQL":
            sql_prompt = build_sql_prompt(st.session_state.data_summary)

            with st.chat_message("assistant"):
                with st.spinner("Running SQL analysis..."):

                    sql_query = generate_llm_response(
                        client=client,
                        system_prompt=sql_prompt,
                        user_input=user_input
                    )

                    st.code(sql_query, language="sql")

                    try:
                        result_df = execute_sql_query(
                            st.session_state.df,
                            sql_query
                        )

                        st.write(result_df)

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"SQL Query:\n{sql_query}",
                            "output": result_df
                        })

                    except Exception as e:
                        st.error(str(e))

        # ---- PYTHON MODE (UNCHANGED) ----
        else:
            system_prompt = build_system_prompt()

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.spinner("Analyzing your data..."):

                    reply = generate_llm_response(
                        client=client,
                        system_prompt=system_prompt,
                        user_input=user_input
                    )

                    message_placeholder.markdown(reply)

                    # Execute python code if found
                    execute_code_blocks(reply)

else:
    show_no_data_screen()

# ---- Footer ----
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 12px;'>
    💡 Tip: Be specific with your questions for better results | 
    🔒 Your data stays private and is not stored
    </div>
    """,
    unsafe_allow_html=True
)