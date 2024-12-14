import pandas as pd

def create_cumulative_returns_table(base_returns, sensitivity_returns):
    """
    Create a table of cumulative returns for different time intervals
    """
    time_intervals = {
        "1 Month": 21,
        "3 Months": 63,
        "6 Months": 126,
        "1 Year": 252
    }
    cumulative_returns_table = {
        "Time Interval": [],
        "Base Cumulative Returns": [],
    }
    for label, days in time_intervals.items():
        cumulative_returns_table["Time Interval"].append(label)
        cumulative_returns_table["Base Cumulative Returns"].append(base_returns[days - 1])
    for label, metrics in sensitivity_returns.items():
        for i, (time_label, days) in enumerate(time_intervals.items()):
            cumulative_returns_table.setdefault(f"{label} Cumulative Returns", [None] * len(time_intervals))
            cumulative_returns_table[f"{label} Cumulative Returns"][i] = metrics[days - 1]
    return pd.DataFrame(cumulative_returns_table)