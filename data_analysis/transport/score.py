"""
Calculates the final accesibility score for each school in the Copiapó and Santiago.
The score considers the values obtained on 'city_accessibility_scores.csv'
"""
import pandas as pd

# Load the data
df_Santiago_score = pd.read_csv('Santiago_accessibility_scores.csv')
df_Santiago_schools = pd.read_csv('closest_schools_santiago.csv')
df_Copiapo_score = pd.read_csv('Copiapó_accessibility_scores.csv')
df_Copiapo_schools = pd.read_csv('closest_schools_copiapo.csv')

# Merge the data
df_Santiago = df_Santiago_schools.merge(df_Santiago_score, how='left', on='stop_id')
df_Copiapo = df_Copiapo_schools.merge(df_Copiapo_score, how='left', on='stop_id')

# Recalculate the score considering the distance to the school
# Min-Max normaliztion of the distance
df_Santiago['distance'] = (df_Santiago['distance'] - df_Santiago['distance'].min())/(df_Santiago['distance'].max() - df_Santiago['distance'].min())
df_Santiago['score'] = df_Santiago['score'] + df_Santiago['distance']

df_Copiapo['distance'] = (df_Copiapo['distance'] - df_Copiapo['distance'].min())/(df_Copiapo['distance'].max() - df_Copiapo['distance'].min())
df_Copiapo['score'] = df_Copiapo['score'] + df_Copiapo['distance']

# Save the data
df_Santiago.to_csv('santiago_scores.csv', index=False)
df_Copiapo.to_csv('copiapo_scores.csv', index=False)