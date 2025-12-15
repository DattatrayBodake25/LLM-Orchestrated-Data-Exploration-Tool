import pandas as pd
import warnings

def profile_dataframe(df: pd.DataFrame):
    total_rows = len(df)
    profile = []

    for col in df.columns:
        series = df[col]
        non_null = series.dropna()

        unique_count = series.nunique(dropna=True)
        missing_count = series.isna().sum()
        missing_pct = round((missing_count / total_rows) * 100, 2) if total_rows else 0

        col_name_lower = col.lower()

        # -------- Detect basic column type --------
        if pd.api.types.is_numeric_dtype(series):
            detected_type = "Numeric"

        elif pd.api.types.is_datetime64_any_dtype(series):
            detected_type = "Datetime"

        else:
            detected_type = "Text"

            # Try parsing datetime safely (no warnings)
            if not non_null.empty:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    try:
                        pd.to_datetime(non_null.iloc[:5], errors="raise")
                        detected_type = "Datetime (parsed)"
                    except Exception:
                        if unique_count / max(total_rows, 1) < 0.2:
                            detected_type = "Categorical"

        # -------- Heuristics --------
        is_id = (
            unique_count == total_rows and
            missing_count == 0 and
            any(x in col_name_lower for x in ["id", "order", "user"])
        )

        is_date = (
            "date" in col_name_lower or
            "time" in col_name_lower or
            detected_type.startswith("Datetime")
        )

        # -------- Sample values (Arrow-safe) --------
        # IMPORTANT: convert to string to avoid Arrow crashes
        sample_values = ", ".join(map(str, non_null.head(3).tolist()))

        profile.append({
            "Column": col,
            "Detected Type": detected_type,
            "Pandas Dtype": str(series.dtype),
            "Unique Values": unique_count,
            "Missing %": missing_pct,
            "Potential ID": "Yes" if is_id else "No",
            "Possible Date": "Yes" if is_date else "No",
            "Sample Values": sample_values
        })

    # -------- Final Arrow-safe DataFrame --------
    return pd.DataFrame(profile).astype(str)