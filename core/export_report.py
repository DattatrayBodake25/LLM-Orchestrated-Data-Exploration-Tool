import streamlit as st
import datetime

def export_conversation():
    if not st.session_state.messages:
        return None

    html_content = f"""
    <html>
    <head>
    <style>
    body {{
        font-family: Arial;
        margin: 40px;
    }}
    </style>
    </head>

    <body>
        <h1>Data Analysis Report</h1>
        <p>Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    """

    if st.session_state.df is not None:
        df = st.session_state.df
        html_content += f"""
        <h2>Dataset Info</h2>
        Rows: {df.shape[0]}<br>
        Columns: {df.shape[1]}<br>
        Column Names: {', '.join(df.columns)}<br>
        """

    html_content += "<h2>Conversation</h2>"

    for msg in st.session_state.messages:
        role = "Question" if msg["role"] == "user" else "Analysis"
        content = msg["content"].replace("```python", "<pre><code>").replace("```", "</code></pre>")

        html_content += f"<h3>{role}</h3>{content}<br>"

    html_content += "</body></html>"

    return html_content