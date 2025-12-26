import pandas as pd
from collections import defaultdict

def build_trend(topic_data, dates):
    """
    Build topic trend table.
    Rows: Topics
    Columns: Dates (chronological order enforced)
    Values: Frequency counts
    """

    table = defaultdict(dict)

    for date in dates:
        for topic in topic_data.get(date, []):
            table[topic][date] = table[topic].get(date, 0) + 1

    df = pd.DataFrame(table).fillna(0).T

    # Ensure columns are ordered exactly as provided
    return df[dates]
