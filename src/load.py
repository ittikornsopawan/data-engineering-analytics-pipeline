import pandas as pd
from sqlalchemy.engine import Engine

def load_dataframe_to_postgres(
    df: pd.DataFrame,
    table_name: str,
    engine: Engine,
    if_exists: str = "replace",
):
    df.to_sql(
        table_name,
        engine,
        if_exists=if_exists,
        index=False,
    )