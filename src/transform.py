import pandas as pd

def create_team_matches(matches: pd.DataFrame) -> pd.DataFrame:
    base_matches = matches[[
        "home_team",
        "away_team",
        "Year",
        "home_score",
        "away_score"
    ]].copy()

    home_matches = base_matches[[
        "home_team",
        "away_team",
        "Year",
        "home_score",
        "away_score"
    ]].copy()

    home_matches = home_matches.rename(columns={
        "home_team": "team",
        "away_team": "opponent",
        "Year": "year",
        "home_score": "goals_for",
        "away_score": "goals_against",
    })

    away_matches = base_matches[[
        "away_team",
        "home_team",
        "Year",
        "away_score",
        "home_score"
    ]].copy()

    away_matches = away_matches.rename(columns={
        "away_team": "team",
        "home_team": "opponent",
        "Year": "year",
        "away_score": "goals_for",
        "home_score": "goals_against",
    })

    team_matches = pd.concat(
        [home_matches, away_matches],
        ignore_index=True
    )

    return team_matches


def add_match_result(team_matches: pd.DataFrame) -> pd.DataFrame:
    team_matches = team_matches.copy()

    def get_match_result(row):
        if row["goals_for"] > row["goals_against"]:
            return "W"
        elif row["goals_for"] == row["goals_against"]:
            return "D"
        else:
            return "L"

    team_matches["result"] = team_matches.apply(get_match_result, axis=1)

    return team_matches


def create_team_summary_by_year(team_matches: pd.DataFrame) -> pd.DataFrame:
    team_summary = (
        team_matches
        .groupby(["team", "year", "result"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    team_summary.columns.name = None

    for col in ["W", "D", "L"]:
        if col not in team_summary.columns:
            team_summary[col] = 0

    team_summary["total_matches"] = (
        team_summary["W"] +
        team_summary["D"] +
        team_summary["L"]
    )

    team_summary["total_point"] = (
        team_summary["W"] * 3 +
        team_summary["D"] * 1
    )

    team_summary["point_per_match"] = (
        team_summary["total_point"] / team_summary["total_matches"]
    ).round(2)

    team_summary = team_summary.rename(columns={
        "W": "win_matches",
        "D": "draw_matches",
        "L": "lost_matches",
    })

    team_summary = team_summary[[
        "team",
        "year",
        "total_matches",
        "win_matches",
        "draw_matches",
        "lost_matches",
        "total_point",
        "point_per_match",
    ]]

    team_summary = team_summary.sort_values(
        ["year", "total_matches", "win_matches"],
        ascending=[False, False, False],
    ).reset_index(drop=True)

    return team_summary