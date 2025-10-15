
def calc_trend(current, previous):
    """
    Calculate % change between current and previous KPI.
    Returns string like '+12.5%' or '-3.2%' or 'N/A'.
    """
    try:
        if previous is None or previous == 0:
            return "N/A"
        change = ((current - previous) / previous) * 100
        return f"{change:+.1f}%"
    except Exception:
        return "N/A"
