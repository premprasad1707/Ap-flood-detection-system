def calculate_risk(rainfall, prev_rainfall, elevation, slope):
    """
    Calculate the risk score based on rule-based criteria:
    risk_score = (rainfall * 0.5) + (prev_rainfall * 0.3) + ((100 - elevation) * 0.1) + ((10 - slope) * 0.1)
    """
    score = (
        (float(rainfall) * 0.5) +
        (float(prev_rainfall) * 0.3) +
        (max(0, 100 - float(elevation)) * 0.1) +
        (max(0, 10 - float(slope)) * 0.1)
    )
    return score

def classify_risk(score):
    """
    Classify risk into Low, Medium, High based on score.
    if score > 70 → High
    elif score > 40 → Medium
    else → Low
    """
    if score > 70:
        return "High"
    elif score > 40:
        return "Medium"
    else:
        return "Low"
