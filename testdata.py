import pandas as pd

def getData():# Create MultiIndex tuples for rows
    index_tuples = [
        ('TeamA', '5v5', 'Skater'),
        ('TeamA', '5v5', 'Goalie'),
        ('TeamA', '4v4', 'Team'),
        ('TeamB', '5v5', 'Skater'),
        ('TeamB', '5v4', 'Goalie'),
        ('TeamB', '5v4', 'Team'),
    ]

    # Define index levels
    index = pd.MultiIndex.from_tuples(index_tuples, names=['Team', 'Situation', 'Role'])

    # Create example data
    data = {
        'Shots on Net': [15, 3, 25, 20, 5, 30],
        'Saves': [10, 2, 18, 14, 3, 22],
        'Playtime (min)': [60, 60, 60, 55, 55, 55]
    }

    # Create the DataFrame
    df = pd.DataFrame(data, index=index)
    df = df.to_html
    return df

