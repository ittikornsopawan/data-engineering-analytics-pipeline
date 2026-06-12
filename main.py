from src.database import get_engine
from src.extract import extract_matches_csv
from src.load import load_dataframe_to_postgres
from src.transform import (
    create_team_matches,
    add_match_result,
    create_team_summary_by_year,
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

    print("Transforming team matches...")
    team_matches = create_team_matches(raw_matches)
    team_matches = add_match_result(team_matches)

    print("Loading team matches to PostgreSQL...")
    load_dataframe_to_postgres(
        df=team_matches,
        table_name="team_matches",
        engine=engine,
        if_exists="replace",
    )

    print("Creating team summary by year...")
    team_summary_by_year = create_team_summary_by_year(team_matches)

    print("Loading team summary by year to PostgreSQL...")
    load_dataframe_to_postgres(
        df=team_summary_by_year,
        table_name="team_summary_by_year",
        engine=engine,
        if_exists="replace",
    )

    print("ELT pipeline completed successfully.")

    # 1. 


if __name__ == "__main__":
    main()