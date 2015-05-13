import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix
plt.show()
# Load Premier League 2011/2012 data
df = pd.read_csv('PremierLeague2011-12MatchbyMatch.csv',sep=';')
# Useless columns for first analysis
columnNotUsed = ['Player Forename','Player ID','Team Id']
# Drop all useless data
df = df.drop(columnNotUsed,axis=1)
# Group by match (You see only two team per 'Opposition Id')
op= df.groupby(['Team','Opposition'])
op = df.groupby('Date')
group = dict(list(op))
small = pd.DataFrame(df[['Shots On Target inc goals','Goals']])
scatter_matrix(small, alpha=0.2, figsize=(6, 6), diagonal='kde')
plt.show()
for key in group:
	print group[key].keys()
	df_tmp = pd.DataFrame(group[key])
	for key_group in group[key]:
		print group[key]['Player Surname']
		try:
			print key_group
			df_tmp.plot(x='Player Surname',y=key_group,kind='kde')
			plt.show()
			raw_input()
		except:
			print key_group
print group.keys()
