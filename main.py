from src.database import get_engine
from src.extract import extract_matches_csv
from src.load import load_dataframe_to_postgres
from src.transform import (
    transform_match_statics
)

def main():

    # ELT Raw Data and Summary per country

    print("Starting World Cup ELT pipeline...")
    engine = get_engine()

    print("Extracting matches CSV...")
    raw_matches = extract_matches_csv()

    print("Loading raw matches to PostgreSQL...")
    load_dataframe_to_postgres(
        df=raw_matches,
        table_name="raw_matches",
        engine=engine,
        if_exists="replace",
    )

    print("Done raw matches to PostgreSQL...")

    # 01 Match summary
    print("Start: Transform team summary")
    team_summary = transform_match_statics(raw_matches)

    print("End: Transform team summary")

    print("Loading: Transform team summary")
    load_dataframe_to_postgres(
        df=team_summary,
        table_name="team_summary",
        engine=engine,
        if_exists="replace",
    )

    print("Done: Transform team summary")


if __name__ == "__main__":
    main()