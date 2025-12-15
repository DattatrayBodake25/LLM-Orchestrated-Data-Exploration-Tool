import streamlit as st
import warnings
import matplotlib.pyplot as plt
import sys
import io
import pandas as pd

def sanitize_value(value):
    """Sanitize DataFrame/Series for Arrow compatibility."""
    if isinstance(value, pd.Series):
        return value.to_frame().astype(str)
    if isinstance(value, pd.DataFrame):
        return value.astype(str)
    return value


def execute_code_blocks(reply):
    df = st.session_state.df

    # If no python code is found, just store the assistant message
    if "```python" not in reply:
        st.session_state.messages.append({
            "role": "assistant",
            "content": reply
        })
        return

    code_blocks = reply.split("```python")

    for i in range(1, len(code_blocks)):
        code = code_blocks[i].split("```")[0].strip()

        try:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")

                # Prepare matplotlib
                plt.figure(figsize=(10, 6))

                # Prepare execution environment
                exec_globals = {
                    "df": df,
                    "pd": __import__("pandas"),
                    "plt": plt,
                    "sns": __import__("seaborn"),
                    "st": st
                }
                local_vars = {}

                # ---- Capture print() output ----
                stdout_buffer = io.StringIO()
                sys_stdout_original = sys.stdout
                sys.stdout = stdout_buffer

                # Execute code
                exec(code, exec_globals, local_vars)

                # Restore stdout
                sys.stdout = sys_stdout_original
                printed_output = stdout_buffer.getvalue().strip()

                # ---- Detect last expression value ----
                last_line = code.split("\n")[-1].strip()

                value_to_display = None

                # Case 1: last line is a variable in globals
                if last_line in exec_globals:
                    value_to_display = exec_globals[last_line]

                # Case 2: last line is a variable in locals
                elif last_line in local_vars:
                    value_to_display = local_vars[last_line]

                # ---- Display outputs ----
                # container to show all results together
                output_box = st.container()

                # Printed output
                if printed_output:
                    with output_box:
                        st.write(printed_output)

                # Main result (Series, DataFrame, number, etc.)
                if value_to_display is not None:
                    safe_value = sanitize_value(value_to_display)
                    with output_box:
                        st.write(safe_value)

                # ---- Save result for chat persistence ----
                stored_output = {
                    "printed": printed_output,
                    "result": sanitize_value(value_to_display) if value_to_display is not None else None,
                    "figure": None
                }

                # ---- Plot handling ----
                fig = plt.gcf()
                if fig.get_axes():
                    with output_box:
                        st.pyplot(fig)

                    stored_output["figure"] = fig

                # Save assistant history message
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply,
                    "output": stored_output
                })

                plt.close()

                # ---- Show warnings ----
                if w:
                    for warning in w:
                        st.info(f"Note: {warning.message}")

        except Exception as e:
            # Restore stdout in case of crash
            sys.stdout = sys_stdout_original

            st.error(f"Code execution failed: {type(e).__name__}")
            st.code(code, language="python")

            error_msg = str(e)

            if "NameError" in error_msg:
                st.info("Possibly a wrong column name.")
            elif "TypeError" in error_msg:
                st.info("Likely non-numeric data in a numeric operation.")
            elif "KeyError" in error_msg:
                st.info("The specified column does not exist in your dataset.")
            else:
                st.info("Try rephrasing your question.")