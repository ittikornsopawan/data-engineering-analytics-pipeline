import pandas as pd

from src.config import MATCHES_FILE

def extract_matches_csv():
    return pd.read_csv(MATCHES_FILE)