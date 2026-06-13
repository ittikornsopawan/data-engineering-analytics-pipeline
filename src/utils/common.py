def get_match_result(row):
    if row["goals_for"] > row["goals_against"]:
        return "W"
    elif row["goals_for"] == row["goals_against"]:
        return "D"
    else:
        return "L"