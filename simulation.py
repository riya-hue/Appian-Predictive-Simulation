def calculate_risk(df):
    """
    Calculates a simple SLA risk score (0–100) for each case
    """
    risk_scores = []

    for _, row in df.iterrows():
        base_risk = (row["ProcessingTime"] / row["SLA"]) * 50

        complexity_weight = {
            "Low": 5,
            "Medium": 15,
            "High": 30
        }.get(row["Complexity"], 10)

        status_weight = {
            "Pending": 15,
            "InProgress": 8,
            "Completed": 0
        }.get(row["Status"], 5)

        risk = base_risk + complexity_weight + status_weight
        risk_scores.append(min(round(risk, 2), 100))

    df["RiskScore"] = risk_scores
    return df


def suggest_reassignment(df):
    """
    Generates human-readable operational recommendations
    """
    high_risk_cases = df.sort_values("RiskScore", ascending=False).head(2)

    suggestions = []
    for _, row in high_risk_cases.iterrows():
        suggestions.append(
            f"Case {row['CaseID']} shows elevated SLA risk. "
            f"Reallocating capacity to the {row['Team']} team may reduce backlog risk."
        )

    return suggestions
