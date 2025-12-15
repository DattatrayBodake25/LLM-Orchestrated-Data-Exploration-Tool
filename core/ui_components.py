import streamlit as st

def render_chat_history():
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "figure" in msg:
                st.pyplot(msg["figure"])


def show_data_health_report():
    if st.session_state.df is None or st.session_state.data_profile is None:
        return

    with st.sidebar:
        st.markdown("---")
        st.header("📊 Data Health Report")

        df_profile = st.session_state.data_profile

        # ---- Overview metrics ----
        st.metric("Total Columns", df_profile.shape[0])
        st.metric(
            "Columns with Missing Values",
            (df_profile["Missing %"].astype(float) > 0).sum()
        )

        # ---- Column profiling table ----
        with st.expander("🔍 Column Profiling Details"):
            st.dataframe(
                df_profile,
                width="stretch"
            )

        # ---- Potential issues ----
        with st.expander("⚠️ Potential Issues"):
            issues = df_profile[
                (df_profile["Missing %"].astype(float) > 30) |
                (df_profile["Potential ID"] == "Yes")
            ]

            if issues.empty:
                st.success("No major issues detected 🎉")
            else:
                st.dataframe(
                    issues,
                    width="stretch"
                )


def show_no_data_screen():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("👈 Please upload a CSV file to start")

        st.markdown("### 💡 Example questions:")
        st.markdown("""
        - What are the main trends in my data?
        - Show me a correlation matrix
        - Create a bar chart of the top 10 categories
        - What's the average value by month?
        - Are there any outliers in the price column?
        """)