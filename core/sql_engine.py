import duckdb
import pandas as pd

def execute_sql_query(df: pd.DataFrame, sql: str) -> pd.DataFrame:
    # Safety guard: allow SELECT only
    forbidden = ["insert", "update", "delete", "drop", "create", "alter"]
    if any(word in sql.lower() for word in forbidden):
        raise ValueError("Only SELECT queries are allowed in SQL mode.")

    con = duckdb.connect(database=":memory:")
    con.register("df", df)

    result = con.execute(sql).fetchdf()
    con.close()

    return result