import pandas as pd
from pathlib import Path 
import sys

df_week = pd.read_csv('data/scores_w{}.csv'.format(sys.argv[1]))
df_week = df_week.rename(columns={"Unnamed: 0": "user"})
df_week.head()

df_full = pd.read_csv('data/full_scores.csv')
df_full.head()

# Update the full table
df_week['week'] = sys.argv[1]
df_full = df_full.append(df_week, ignore_index=True)

# Save
filepath = Path('data/full_scores.csv')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
df_full.to_csv(filepath, index=False)

# Print the season ranking
ranking  = df_full.groupby('user')['result'].sum()
ranking = ranking.sort_values(ascending=False)
ranking.reset_index()
print(ranking.head())
