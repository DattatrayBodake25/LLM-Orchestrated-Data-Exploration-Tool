import streamlit as st
import pandas as pd
from core.profiler import profile_dataframe

def sidebar_file_upload():
    with st.sidebar:
        st.header("📁 Data Upload")
        uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state.df = df

                st.session_state.data_summary = {
                    "shape": df.shape,
                    "columns": df.columns.tolist(),
                    "dtypes": df.dtypes.to_dict(),
                    "sample": df.head(3).to_dict(),
                    "stats": df.describe().to_dict() if not df.empty else {}
                }

                # NEW: auto profiling
                st.session_state.data_profile = profile_dataframe(df)

                st.success(f"✅ Loaded {df.shape[0]} rows × {df.shape[1]} columns")

                with st.expander("Preview Data"):
                    st.dataframe(df.head())

                with st.expander("Data Summary"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total Rows", df.shape[0])
                        st.metric("Total Columns", df.shape[1])

                    with col2:
                        st.metric("Memory Usage", f"{df.memory_usage().sum() / 1024:.1f} KB")
                        st.metric("Missing Values", df.isnull().sum().sum())

            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
                st.info("Please make sure your file is a valid CSV format.")

        else:
            st.info("👆 Upload a CSV file to start analyzing!")